import os
import PIL.Image
import google.genai as genai
from dotenv import load_dotenv

# Import your modules
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
    choice = input("Import menu (1=URL, 2=Image): ").strip()

    # --- OPTION 1: URL ---
    if choice == "1":
        url = input("Enter menu URL: ").strip()
        menu_items = extract_menu_items_from_html(url, client)

        if menu_items:
            formatted = "\n".join([f"{m['item']} - {m['price']}" for m in menu_items])
            app.add(formatted, data_type="text", metadata={"source": url})
            print(f"\n[OK] Added {len(menu_items)} items from URL.")
        else:
            print("[ERROR] No items found at that URL.")
            return

    # --- OPTION 2: IMAGE ---
    elif choice == "2":
        path = input("Enter image path: ").strip()
        try:
            img = PIL.Image.open(path)
            vision_resp = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["Extract menu items and prices. Format: Item: Price.", img],
            )
            app.add(vision_resp.text, data_type="text", metadata={"source": path})
            print("\n[OK] Image menu processed and added.")
        except Exception as e:
            print(f"[ERROR] Vision failed: {e}")
            return

    # --- THE CHAT LOOP ---
    print("\nAsk anything about the menu (type 'exit' to quit):")
    while True:
        query = input("\nQuery: ").strip()
        if query.lower() in ["exit", "quit"]: break

        # 1. Get Context
        contexts = retrieve_menu_context(app, query)
        context_block = build_context_block(contexts)

        # 2. Generate Answer
        answer = generate_grounded_answer(client, query, context_block)

        # 3. Validate
        _, verdict = verify_answer_against_context(client, answer, context_block)

        print(f"\n--- ANSWER ({verdict}) ---\n{answer}\n-----------------------")


if __name__ == "__main__":
    main()