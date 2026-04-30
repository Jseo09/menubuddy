import os
import time
import re
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.genai as genai

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

def clean_source_label(path):
    """Strips 'uploads/' and extensions for a cleaner UI label."""
    if not path:
        return "Unknown Source"
    if path.startswith("http"):
        return f"{path} (URL)"
    clean_name = path.replace("uploads/", "")
    display_name = os.path.splitext(clean_name)[0]
    return f"{display_name} (image)"

def safe_run(func, *args, **kwargs):
    """Retries a function once after 2 seconds on failure."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Attempt failed: {e}. Retrying in 2 seconds...")
        time.sleep(2)
        return func(*args, **kwargs)

def calculate_citation_coverage(text):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]
    if not sentences: return 0.0
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
        "message": f"Saved to ChromaDB: {clean_source_label(source)}",
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
            "answer": "I'm sorry, that question is outside the menu domain.",
            "status": "FLAGGED (IRRELEVANT)",
            "details": "Prefilter refusal.",
            "sources": []
        })

    try:
        retrieval_res = safe_run(retriever.run, query=query, top_k=5)
        docs = retrieval_res.get("documents", [])
    except Exception as e:
        return jsonify({"answer": "Database error.", "status": "FLAGGED (ERROR)", "details": str(e)}), 503

    if not docs:
        return jsonify({"answer": "No menu data found.", "status": "FLAGGED", "sources": []})

    top_score = getattr(docs[0], "score", None)
    if top_score is None or top_score < CONFIDENCE_THRESHOLD:
        source_mapping = [f"[{i + 1}] {clean_source_label(d.meta['source'])}" for i, d in enumerate(docs)]
        return jsonify({
            "answer": "I don't have enough reliable information.",
            "status": "FLAGGED",
            "details": f"Confidence {top_score} below threshold.",
            "verification": "Sources Found:\n" + "\n".join(source_mapping),
            "sources": [clean_source_label(d.meta["source"]) for d in docs]
        })

    template = [ChatMessage.from_user("""Answer using the context. 
    IMPORTANT:
        - Use information from ONLY ONE restaurant.
        - Ignore any content from other restaurants.
        - Do NOT mix menu items from different sources.
    Cite every sentence with [n]. Context: {% for doc in documents %}Chunk [{{ loop.index }}]: (Source: {{ doc.meta['source'] }}) {{ doc.content }} --- {% endfor %} Question: {{ query }} Answer:""")]

    try:
        res = safe_run(pipe.run, data={"prompt_builder": {"template_variables": {"documents": docs, "query": query}, "template": template}})
        answer_text = res["genai"]["replies"][0].text
    except Exception as e:
        return jsonify({"answer": "Generation failed.", "status": "FLAGGED (ERROR)", "details": str(e)}), 503

    context_block = "\n".join([f"[{i + 1}] {d.content} (SOURCE: {d.meta['source']})" for i, d in enumerate(docs)])
    validation_text, verdict = verify_answer_against_context(validator_client, query, answer_text, context_block)

    source_mapping = [f"[{i + 1}] {clean_source_label(d.meta['source'])}" for i, d in enumerate(docs)]
    return jsonify({
        "answer": answer_text,
        "status": "VERIFIED" if verdict == "OK" else "FLAGGED",
        "details": validation_text,
        "verification": "Sources Found:\n" + "\n".join(source_mapping),
        "sources": [clean_source_label(d.meta["source"]) for d in docs],
        "top_score": top_score,
        "citation_coverage": calculate_citation_coverage(answer_text)
    })

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=False, port=5001)
