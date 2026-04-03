import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

from src.scraper import extract_menu_data
from haystack import Pipeline, Document
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage

from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator

app = Flask(__name__)

# 1. Persistent Storage
document_store = ChromaDocumentStore(persist_path="./chroma_db")

# 2. Components
cleaner = DocumentCleaner()
splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=20)
retriever = ChromaQueryTextRetriever(document_store=document_store)
genai_chat = GoogleGenAIChatGenerator(model="gemini-3.1-flash-lite-preview")
prompt_builder = ChatPromptBuilder()

# 3. Pipeline (FIXED: Only connecting prompt to genai)
pipe = Pipeline()
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("genai", genai_chat)
pipe.connect("prompt_builder.prompt", "genai.messages")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/import_menu", methods=["POST"])
def import_menu():
    source = None
    if 'image' in request.files:
        file = request.files["image"]
        source = os.path.join("uploads", file.filename)
        file.save(source)
    elif request.is_json and 'url' in request.json:
        source = request.json['url']

    if not source:
        return jsonify({"error": "No source"}), 400

    raw_markdown = extract_menu_data(source)
    if raw_markdown:
        doc = Document(content=raw_markdown, meta={"source": source})
        cleaned = cleaner.run(documents=[doc])
        chunks = splitter.run(documents=cleaned["documents"])
        document_store.write_documents(chunks["documents"])
        return jsonify({"message": f"Successfully saved to ChromaDB: {source}"})

    return jsonify({"error": "Processing failed"}), 500


@app.route("/ask_menu", methods=["POST"])
def ask_menu():
    query = request.json.get("question")

    # 1. Retrieve the top 5 most relevant chunks from ChromaDB
    retrieval_res = retriever.run(query=query, top_k=5)
    docs = retrieval_res["documents"]

    # 2. Updated Template for Numbered Citations
    template = [
        ChatMessage.from_user(
            """You are MenuBuddy. Answer the question using the numbered context chunks below.

            RULES:
            - Use numbered citations like [1] or [1, 2] at the end of sentences.
            - Do NOT include file paths like 'uploads/Wendy's.png' in your descriptions.
            - If the information isn't in the chunks, say you don't know.

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

    # 3. Run the generation pipeline
    res = pipe.run(data={
        "prompt_builder": {
            "template_variables": {"documents": docs, "query": query},
            "template": template
        }
    })

    answer_text = res["genai"]["replies"][0].text

    # 4. Create a "Source Key" for your dashboard's Log Window
    # This maps the numbers back to the filenames for your own verification
    source_mapping = [f"[{i + 1}] {d.meta['source']}" for i, d in enumerate(docs)]
    verification_log = "Sources Found:\n" + "\n".join(source_mapping)

    return jsonify({
        "answer": answer_text,
        "verification": verification_log
    })


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True, port=5001)