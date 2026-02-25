import os
import requests
import PIL.Image
from google import genai
from embedchain import App

# 1. Configuration - Set BOTH keys
os.environ["OPENAI_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""


def run_hybrid_menubuddy():
    # We still need the Gemini client for the initial Image-to-Text conversion
    gemini_client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    # 2. Setup the App with OpenAI LLM + Gemini Embeddings
    config = {
        'llm': {
            'provider': 'openai',
            'config': {
                'model': 'gpt-4o',  # Using OpenAI's strongest reasoning model
                'temperature': 0.2  # Lower temperature for better menu accuracy
            }
        },
        'embedder': {
            'provider': 'google',
            'config': {
                'model': 'models/gemini-embedding-001'  # Keeping the stable Google embedder
            }
        },
        'vectordb': {
            'provider': 'chroma',
            'config': {
                'dir': 'menubuddy_db',
                'allow_reset': True
            }
        }
    }

    app = App.from_config(config=config)

    print("\n--- MenuBuddy Hybrid Spike (OpenAI LLM) ---")
    mode = input("Choose source (1 for Web URL, 2 for Image File): ")

    if mode == "1":
        url = input("Paste the menu URL: ")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        try:
            res = requests.get(url, headers=headers, timeout=15)
            app.add(res.text, data_type="text")
        except Exception as e:
            print(f"Scrape Error: {e}")
            return

    elif mode == "2":
        path = input("Enter image path: ")
        img = PIL.Image.open(path)
        # We use Gemini's vision because it's already set up, but the RAG will use GPT
        response = gemini_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=["Extract all items and prices as a list.", img]
        )
        app.add(response.text, data_type="text")

    # 3. Interactive Querying with GPT-4o
    print(f"\nKnowledge Base Ready. Reasoning handled by GPT-4o.")
    for i in range(1, 4):
        query = input(f"\nQuestion {i}: ")
        answer = app.query(query)
        print(f"MenuBuddy: {answer}")


if __name__ == "__main__":
    run_hybrid_menubuddy()
