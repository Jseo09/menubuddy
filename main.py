import os
import PIL.Image
import google.genai as genai
from dotenv import load_dotenv

# Import your custom modules
from src.scraper import extract_menu_items_from_html
from src.retrieval import setup_rag_app, retrieve_menu_context
from src.citation_formatter import build_context_block
from src.generator import generate_grounded_answer
from src.validator import verify_answer_against_context


def main():
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    app = setup_rag_app()

    print("\n=== MenuBuddy: Modular Edition ===")
    print("[SYSTEM] RAG Pipeline Initialized.")
    choice = input("Import menu (1=URL, 2=Image): ").strip()

    # --- STAGE 1: DATA INGESTION (Deterministic) ---
    if choice == "1":
        url = input("Enter menu URL: ").strip()
        print(f"\n[DETERMINISTIC STAGE: SCRAPING] Extracting structured data from {url}...")
        menu_items = extract_menu_items_from_html(url, client)

        if menu_items:
            # Transparency: Show the structured data extracted before vectorization
            print(f"--- STORED STRUCTURED DATA ({len(menu_items)} items) ---")
            for m in menu_items[:3]:  # Show a sample for transparency
                print(f"DEBUG: Found '{m['item']}' at {m['price']}")

            formatted = "\n".join([f"{m['item']} - {m['price']}" for m in menu_items])
            app.add(formatted, data_type="text", metadata={"source": url})
            print(f"[OK] Menu data vectorized and stored in ChromaDB.")
        else:
            print("[ERROR] No items found at that URL.")
            return

    elif choice == "2":
        path = input("Enter image path: ").strip()
        print(f"\n[GENERATIVE STAGE: VISION OCR] Processing image at {path}...")
        try:
            img = PIL.Image.open(path)
            vision_resp = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["Extract menu items and prices. Format: Item: Price.", img],
            )
            app.add(vision_resp.text, data_type="text", metadata={"source": path})
            print("[OK] Image menu processed and added to Vector DB.")
        except Exception as e:
            print(f"[ERROR] Vision failed: {e}")
            return

    # --- THE CHAT LOOP (Transparency & Refusal Logic) ---
    print("\n" + "=" * 40)
    print("READY: Ask MenuBuddy about the menu (type 'exit' to quit)")
    print("=" * 40)

    while True:
        query = input("\nUser Query: ").strip()
        if query.lower() in ["exit", "quit"]: break

        # 2. RETRIEVAL (Deterministic: Searching the Vector DB)
        print(f"\n[DETERMINISTIC STAGE: RETRIEVAL] Querying Vector DB for: '{query}'")
        contexts = retrieve_menu_context(app, query)

        # Engineering Transparency: Show exactly what was found
        print("--- TOP RETRIEVED CHUNKS ---")
        for c in contexts:
            print(f"ID [{c['id']}] | Content: {c['text'][:80]}... | Source: {c['source']}")

        context_block = build_context_block(contexts)

        # 3. GENERATION (Generative: Synthesizing the LLM Answer)
        print("\n[GENERATIVE STAGE: LLM] Synthesizing answer with citations...")
        answer = generate_grounded_answer(client, query, context_block)

        # 4. VALIDATION (Deterministic: The Fact-Check Gatekeeper)
        print("[DETERMINISTIC STAGE: VALIDATION] Verifying answer against source context...")
        _, verdict = verify_answer_against_context(client, answer, context_block)

        # 5. FINAL OUTPUT (Handling Refusal Cases)
        if verdict == "UNSUPPORTED":
            print(f"\n--- ANSWER (STATUS: REFUSED - {verdict}) ---")
            print("Refusal Reason: I found some information, but it couldn't be verified against the menu data.")
            print("Please try rephrasing or ask about a different item.")
        else:
            print(f"\n--- ANSWER (STATUS: VERIFIED - {verdict}) ---")
            print(answer)

        print("\n" + "-" * 30)


if __name__ == "__main__":
    main()