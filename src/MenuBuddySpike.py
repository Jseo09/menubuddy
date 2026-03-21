import os
import requests
import PIL.Image
from bs4 import BeautifulSoup
import google.genai as genai
from embedchain import App

# ---------------------------------------------------
# API KEYS
# ---------------------------------------------------
os.environ["OPENAI_API_KEY"] = "KEY"
os.environ["GOOGLE_API_KEY"] = "KEY"

# ---------------------------------------------------
# HTML Extraction
# ---------------------------------------------------

def extract_menu_items_from_html(url, gem_client):
    print(f"\n[PARSING] Accessing: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"[ERROR] Site returned status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        menu_items = []

        # Method 1: div layout
        blocks = soup.find_all("div", class_="chooseBar")
        for block in blocks:
            name = block.get("data-food")
            price = block.get("data-price")
            if name and price:
                clean_price = f"${price}" if "$" not in price else price
                menu_items.append({"item": name, "price": clean_price})

        # Method 2: table layout
        if not menu_items:
            rows = soup.find_all(
                "tr",
                class_=lambda x: x and ("tr-0" in x or "tr-1" in x),
            )

            for row in rows:
                cols = row.find_all("td")

                if len(cols) >= 3:

                    name_tag = cols[0].find("span", class_="prc-food-new")
                    price_tag = cols[2]

                    if name_tag and price_tag:

                        name = name_tag.get_text(strip=True)
                        price = price_tag.get_text(strip=True)

                        if name and price:
                            menu_items.append({"item": name, "price": price})

        # Gemini fallback
        if not menu_items:

            print("[INFO] Falling back to Gemini extraction...")

            for noise in soup(["script", "style", "nav", "footer", "header", "svg"]):
                noise.decompose()

            clean_text = soup.get_text(separator="\n", strip=True)

            extraction = gem_client.generate_content(
                model="models/gemini-2.5-flash",
                contents=[
                    (
                        "Extract menu items. Return format 'Item: Price'.\n\n"
                        + clean_text[:12000]
                    )
                ],
            )

            if extraction and extraction.text:

                for line in extraction.text.split("\n"):

                    if ":" in line:

                        item, price = line.split(":", 1)

                        menu_items.append({
                            "item": item.strip(),
                            "price": price.strip()
                        })

        return menu_items

    except Exception as e:
        print("[ERROR] Scraper failed:", e)
        return []


# ---------------------------------------------------
# Retrieval
# ---------------------------------------------------

def retrieve_menu_context(app, question, num_documents=5):

    try:
        results = app.search(question, num_documents=num_documents)
    except Exception as e:
        print("[ERROR] Retrieval failed:", e)
        return []

    contexts = []

    for idx, res in enumerate(results, start=1):

        text = res.get("context", "") or ""
        metadata = res.get("metadata", {}) or {}

        source = (
            metadata.get("source")
            or metadata.get("url")
            or metadata.get("data_value")
            or "menu_data"
        )

        if text.strip():

            contexts.append({
                "id": idx,
                "text": text.strip(),
                "source": source
            })

    return contexts


def build_context_block(contexts):

    lines = []

    for c in contexts:
        lines.append(f"[{c['id']}] {c['text']} (SOURCE: {c['source']})")

    return "\n".join(lines)


# ---------------------------------------------------
# Generation
# ---------------------------------------------------

def generate_grounded_answer(gem_client, question, context_block):

    prompt = f"""
You are MenuBuddy.

Use ONLY the context below.

Context:
{context_block}

Question:
{question}

Cite sources like [1].
"""

    model = gem_client.GenerativeModel("models/gemini-2.5-flash")

    resp = model.generate_content(prompt)

    return (resp.text or "").strip()


# ---------------------------------------------------
# Verification
# ---------------------------------------------------
def verify_answer_against_context(gem_client, answer, context_block):

    prompt = f"""
You are a strict fact-checking assistant.

Context:
{context_block}

Answer:
{answer}

Check if every claim in the answer is supported by the context.

Output exactly one line:

VERDICT: OK
or
VERDICT: UNSUPPORTED
"""

    model = gem_client.GenerativeModel("models/gemini-2.5-flash")

    resp = model.generate_content(prompt)

    return (resp.text or "").strip()


# ---------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------

def menubuddy_basic_rag():

    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("[ERROR] GOOGLE_API_KEY not set")
        return

    genai.configure(api_key=api_key)

    config = {
        "llm": {
            "provider": "openai",
            "config": {"model": "gpt-4o", "temperature": 0.1},
        },
        "embedder": {
            "provider": "google",
            "config": {"model": "models/gemini-embedding-001"},
        },
        "vectordb": {
            "provider": "chroma",
            "config": {"dir": "menubuddy_basic_db", "allow_reset": True},
        },
    }

    app = App.from_config(config=config)

    print("\n=== MenuBuddy Basic RAG ===")

    mode = input("Import menu (1=URL, 2=Image): ").strip()


# ---------------------------------------------------
# URL MODE (UNCHANGED)
# ---------------------------------------------------

    if mode == "1":

        url = input("Enter menu URL: ").strip()

        menu_items = extract_menu_items_from_html(url, genai)

        if menu_items:

            formatted = "\n".join(
                [f"{m['item']} - {m['price']}" for m in menu_items]
            )

            app.add(
                formatted,
                data_type="text",
                metadata={"source": url, "type": "menu_text"},
            )

            print("\n[SUCCESS] Menu added to vector DB.")

        else:

            print("[!] No menu items extracted.")
            return


# ---------------------------------------------------
# IMAGE MODE (FIXED QR SUPPORT)
# ---------------------------------------------------

    elif mode == "2":

        path = input("Enter image path: ").strip()

        try:

            import cv2
            from pyzbar.pyzbar import decode

            img_cv = cv2.imread(path)

            if img_cv is None:
                print("[ERROR] Image not found")
                return

            print("Image shape:", img_cv.shape)

            qr_url = ""

            qr_results = decode(PIL.Image.open(path))

            if qr_results:
                qr_url = qr_results[0].data.decode("utf-8")

            print("QR result:", qr_url)

            # QR → scrape menu
            if qr_url.startswith("http"):

                print("\n[QR CODE DETECTED]")
                print(qr_url)

                menu_items = extract_menu_items_from_html(qr_url, genai)

                if menu_items:

                    formatted = "\n".join(
                        [f"{m['item']} - {m['price']}" for m in menu_items]
                    )

                    app.add(
                        formatted,
                        data_type="text",
                        metadata={"source": qr_url, "type": "menu_qr"},
                    )

                    print("\n[SUCCESS] Menu added from QR URL.")

            # Original OCR fallback
            img = PIL.Image.open(path)

            model = genai.GenerativeModel("models/gemini-2.5-flash")

            vision_resp = model.generate_content([
                "Extract menu items and prices. Format: Item: Price.",
                img
            ])

            vision_text = (vision_resp.text or "").strip()

            if not vision_text:
                print("[ERROR] Empty vision output.")
                return

            app.add(
                vision_text,
                data_type="text",
                metadata={"source": path, "type": "menu_image_ocr"},
            )

            print("\n[OK] Image menu added to vector DB.")

        except Exception as e:

            print(f"[ERROR] Vision extraction failed: {e}")
            return


    else:
        print("[ERROR] Invalid mode.")
        return


# ---------------------------------------------------
# QUESTION LOOP
# ---------------------------------------------------

    print("\nYou can now ask questions about the menu.")
    print("Type 'exit' to stop.\n")

    while True:

        q = input("Ask about the menu: ").strip()

        if q.lower() in ["exit", "quit"]:
            break

        contexts = retrieve_menu_context(app, q)

        if not contexts:
            print("[INFO] No context found.")
            continue

        context_block = build_context_block(contexts)

        answer = generate_grounded_answer(genai, q, context_block)

        verification = verify_answer_against_context(
            genai,
            answer,
            context_block
        )

        print("\n---------------- MENU BUDDY ANSWER ----------------")
        print(answer)
        print("---------------------------------------------------")
        print(verification)


if __name__ == "__main__":
    menubuddy_basic_rag()
