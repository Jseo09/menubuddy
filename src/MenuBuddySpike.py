import os
import requests
import PIL.Image
from bs4 import BeautifulSoup
import google.genai as genai
from embedchain import App

# ---------------------------------------------------
# API KEYS
# ---------------------------------------------------
os.environ["OPENAI_API_KEY"] = "API KEY"
os.environ["GOOGLE_API_KEY"] = "API KEY"

# ---------------------------------------------------
# Extraction Here
# ---------------------------------------------------

def extract_menu_items_from_html(url, gem_client):
    print(f"\n[PARSING] Accessing: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        menu_items = []

        blocks = soup.find_all("div", class_="chooseBar")
        for block in blocks:
            name = block.get('data-food')
            price = block.get('data-price')
            
            if name and price:
         
                clean_price = f"${price}" if "$" not in price else price
                menu_items.append({"item": name, "price": clean_price})


        if not menu_items:

            rows = soup.find_all("tr", class_=lambda x: x and ("tr-0" in x or "tr-1" in x))
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    name_tag = cols[0].find("span", class_="prc-food-new")
                    price_tag = cols[2] 
                    
                    if name_tag and price_tag:
                        menu_items.append({
                            "item": name_tag.get_text(strip=True),
                            "price": price_tag.get_text(strip=True)
                        })

        if not menu_items:
            print("[INFO] Falling back to Gemini Intelligence...")
            for noise in soup(["script", "style", "nav", "footer", "header", "svg"]):
                noise.decompose()
            clean_text = soup.get_text(separator="\n", strip=True)
            
            extraction = gem_client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=[f"Extract 'Item: Price' from this text. Keep item names exactly as written:\n\n{clean_text[:12000]}"]
            )
            for line in extraction.text.split('\n'):
                if ":" in line:
                    parts = line.split(":", 1)
                    menu_items.append({"item": parts[0].strip("- *"), "price": parts[1].strip()})
        
        return menu_items

    except Exception as e:
        print(f"[ERROR] Scraper failed: {e}")
        return []
    
# ---------------------------------------------------
# MAIN RAG FUNCTION
# ---------------------------------------------------
def menubuddy_basic_rag():
 
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[ERROR] GOOGLE_API_KEY environment variable not set.")
        return

    gem_client = genai.Client(api_key=api_key)

    config = {
        "llm": {
            "provider": "openai",
            "config": {"model": "gpt-4o", "temperature": 0.1}
        },
        "embedder": {
            "provider": "google",
            "config": {"model": "models/gemini-embedding-001"}
        },
        "vectordb": {
            "provider": "chroma",
            "config": {"dir": "menubuddy_basic_db", "allow_reset": True}
        }
    }

    app = App.from_config(config=config)

    print("\n=== MenuBuddy Basic RAG ===")
    mode = input("Import menu (1=URL, 2=Image): ")

    if mode == "1":
        url = input("Enter URL: ")
        menu_items = extract_menu_items_from_html(url, gem_client)

        if menu_items:
            print(f"\n[OK] Extracted {len(menu_items)} items.")
            formatted = "\n".join([f"{m['item']} - {m['price']}" for m in menu_items])
            app.add(formatted, data_type="text")
            print("\n[SUCCESS] Menu successfully added to vector DB.")
        else:
            print("\n[!] Could not extract any items. Site access might be blocked.")
            return

    elif mode == "2":
        path = input("Enter image path: ")
        try:
            img = PIL.Image.open(path)
            vision_text = gem_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["Extract a list of all menu items and prices from this image.", img]
            )
            app.add(vision_text.text, data_type="text")
            print("\n[OK] Image menu successfully added.")
        except Exception as e:
            print(f"[ERROR] Vision extraction failed: {e}")
            return

    # QUERY LOOP
    while True:
        q = input("\nAsk about the menu (or 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break
        
        answer = app.query(q)
        print(f"\nMenuBuddy: {answer}")

if __name__ == "__main__":
    menubuddy_basic_rag()
