import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.genai as genai
import re

load_dotenv()
from src.config import CONFIDENCE_THRESHOLD
from src.question_filter import is_irrelevant_question
from src.scraper import extract_menu_data
from src.validator import verify_answer_against_context

from haystack import Pipeline, Document
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage

from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator

app = Flask(__name__)

# Validator client for answer checking
validator_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Persistent storage
document_store = ChromaDocumentStore(persist_path="./chroma_db")

# Components
cleaner = DocumentCleaner()
splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=20)
retriever = ChromaQueryTextRetriever(document_store=document_store)
genai_chat = GoogleGenAIChatGenerator(model="gemini-2.5-flash-lite")
prompt_builder = ChatPromptBuilder()

# Generation pipeline
pipe = Pipeline()
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("genai", genai_chat)
pipe.connect("prompt_builder.prompt", "genai.messages")

def calculate_citation_coverage(text):
    """
    Calculates the percentage of sentences that include a citation [n].
    """
    # Split text into sentences (handles . ! ? followed by a space)
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]
    
    if not sentences:
        return 0.0
    
    # Count sentences containing at least one citation like [1], [2, 3], etc.
    cited_count = sum(1 for s in sentences if re.search(r'\[\d+\]', s))
    
    return round(cited_count / len(sentences), 2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/import_menu", methods=["POST"])
def import_menu():
    source = None

    if "image" in request.files:
        file = request.files["image"]
        source = os.path.join("uploads", file.filename)
        file.save(source)
    elif request.is_json and "url" in request.json:
        source = request.json["url"]

    if not source:
        return jsonify({"error": "No source provided."}), 400

    raw_markdown = extract_menu_data(source)
    if not raw_markdown:
        return jsonify({"error": "Processing failed."}), 500

    doc = Document(content=raw_markdown, meta={"source": source})
    cleaned = cleaner.run(documents=[doc])
    chunks = splitter.run(documents=cleaned["documents"])
    document_store.write_documents(chunks["documents"])

    return jsonify({
        "message": f"Successfully saved to ChromaDB: {source}",
        "chunks_saved": len(chunks["documents"])
    })

@app.route("/ask_menu", methods=["POST"])
def ask_menu():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON."}), 400

    query = request.json.get("question", "").strip()
    if not query:
        return jsonify({"error": "No question provided."}), 400

    if is_irrelevant_question(query):
        return jsonify({
            "answer": "I'm sorry, that question is outside the menu domain. I can only answer questions about menu items, prices, and menu-related details.",
            "status": "FLAGGED (IRRELEVANT)",
            "details": "Prefilter refusal: question classified as out of scope before retrieval.",
            "verification": "Sources Found:\nNone",
            "sources": [],
            "top_score": None
        })

    # 1. Retrieve top chunks
    retrieval_res = retriever.run(query=query, top_k=5)
    docs = retrieval_res.get("documents", [])

    if not docs:
        return jsonify({
            "answer": "I'm sorry, I don't have enough reliable menu information to answer that from the stored menu data.",
            "status": "FLAGGED",
            "details": "Deterministic refusal: no documents retrieved.",
            "verification": "Sources Found:\nNone",
            "sources": [],
            "top_score": None
        })

    # 2. Check top retrieval score before generation
    top_score = getattr(docs[0], "score", None)
    
    if top_score is None or top_score < CONFIDENCE_THRESHOLD:
        source_mapping = [f"[{i + 1}] {d.meta['source']}" for i, d in enumerate(docs)]
        verification_log = "Sources Found:\n" + "\n".join(source_mapping)

        

        return jsonify({
            "answer": "I'm sorry, I don't have enough reliable menu information to answer that from the stored menu data.",
            "status": "FLAGGED",
            "details": f"Deterministic refusal: top retrieval score {top_score} is below threshold {CONFIDENCE_THRESHOLD}.",
            "verification": verification_log,
            "sources": [d.meta["source"] for d in docs],
            "top_score": top_score
        })

    # 3. Prompt template
    template = [
        ChatMessage.from_user(
            """You are MenuBuddy. Answer the question using the numbered context chunks below.

RULES:
- Every single sentence must end with a citation bracket. If a sentence summarizes multiple chunks, include all relevant numbers (e.g., [1, 2]).
- Do NOT include file paths like 'uploads/Wendy's.png' in your descriptions.
- If the information isn't in the chunks, say you don't know.
- Do NOT invent ingredients, prices, or menu items.

Context:
{% for doc in documents %}
Chunk [{{ loop.index }}]:
(Source: {{ doc.meta['source'] }})
{{ doc.content }}
---
{% endfor %}

Question: {{ query }}
Answer:"""
        )
    ]

    # 4. Generate answer
    res = pipe.run(data={
        "prompt_builder": {
            "template_variables": {"documents": docs, "query": query},
            "template": template
        }
    })

    answer_text = res["genai"]["replies"][0].text

    # 5. Build context block for validator
    context_block = "\n".join(
        [f"[{i + 1}] {d.content} (SOURCE: {d.meta['source']})" for i, d in enumerate(docs)]
    )

    # 6. Validate answer
    validation_text, verdict = verify_answer_against_context(
    validator_client,
    query,
    answer_text,
    context_block
)

    status = "VERIFIED" if verdict == "OK" else "FLAGGED"

    # 7. Build verification/source mapping
    source_mapping = [f"[{i + 1}] {d.meta['source']}" for i, d in enumerate(docs)]
    verification_log = "Sources Found:\n" + "\n".join(source_mapping)

    # 8. Calculate citation coverage
    coverage = calculate_citation_coverage(answer_text)

    return jsonify({
        "answer": answer_text,
        "status": status,
        "details": validation_text,
        "verification": verification_log,
        "sources": [d.meta["source"] for d in docs],
        "top_score": top_score,
        "citation_coverage": coverage
    })

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True, port=5001)
