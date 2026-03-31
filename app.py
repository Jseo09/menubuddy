import os
import PIL.Image
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import google.genai as genai

# Import the "Brain" from your src folder
from src.scraper import extract_menu_items_from_html
from src.retrieval import setup_rag_app, retrieve_menu_context
# Note: Ensure these exist in your src folder based on your first main.py
from src.citation_formatter import build_context_block
from src.generator import generate_grounded_answer
from src.validator import verify_answer_against_context

# --- CONFIGURATION ---
load_dotenv()
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize shared resources
# Ensure your .env has GOOGLE_API_KEY and OPENAI_API_KEY
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
rag_app = setup_rag_app()


@app.route("/")
def index():
    return render_template("index.html")


# --- STAGE 1: DATA INGESTION (URL or Image) ---
@app.route("/import_menu", methods=["POST"])
def import_menu():
    # 1. URL INPUT
    if request.is_json:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"message": "No URL provided"}), 400

        menu_items = extract_menu_items_from_html(url, client)
        if not menu_items:
            return jsonify({"message": "No menu items found"}), 400

        formatted = "\n".join([f"{m['item']} - {m['price']}" for m in menu_items])
        rag_app.add(formatted, data_type="text", metadata={"source": url})

        return jsonify({"message": f"Added {len(menu_items)} items from URL."})

    # 2. IMAGE INPUT
    if "image" in request.files:
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"message": "No file selected"}), 400

        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        try:
            img = PIL.Image.open(path)
            # Using 1.5-flash for speed/cost in the web app
            vision_resp = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["Extract menu items and prices. Format: Item: Price.", img],
            )

            vision_text = (vision_resp.text or "").strip()
            if not vision_text:
                return jsonify({"message": "OCR failed to extract text"}), 400

            rag_app.add(vision_text, data_type="text", metadata={"source": path})
            return jsonify({"message": "Image menu added to database."})
        except Exception as e:
            return jsonify({"message": f"Vision error: {str(e)}"}), 500

    return jsonify({"message": "Invalid request"}), 400


# --- STAGE 2: CHAT / RAG PIPELINE ---
@app.route("/ask_menu", methods=["POST"])
def ask_menu():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"message": "No question provided"}), 400

    # 1. Retrieval
    contexts = retrieve_menu_context(rag_app, question)
    if not contexts:
        return jsonify({"answer": "I don't have any info on that menu yet.", "verification": "NONE"})

    context_block = build_context_block(contexts)

    # 2. Generation
    answer = generate_grounded_answer(client, question, context_block)

    # 3. Validation
    # verify_answer_against_context returns (raw_response, verdict)
    _, verdict = verify_answer_against_context(client, answer, context_block)

    return jsonify({
        "answer": answer,
        "verification": verdict
    })


if __name__ == "__main__":
    # Run on port 5000 by default
    app.run(debug=True, port=5000)