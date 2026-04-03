import os
import chromadb
from chromadb.utils import embedding_functions


def setup_rag_app():
    # Local Persistence
    client = chromadb.PersistentClient(path="./menu_db")

    # UPDATED: Using the new 2026 multimodal embedding model
    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model_name="models/gemini-embedding-2-preview"  # <--- Updated ID
    )

    return client.get_or_create_collection(
        name="menu_items",
        embedding_function=gemini_ef
    )


def retrieve_menu_context(collection, query):
    # Search for the top 3 most relevant menu parts
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    # Format into the list structure your main.py expects
    contexts = []
    for i, text in enumerate(results['documents'][0]):
        contexts.append({
            "id": results['ids'][0][i],
            "text": text,
            "source": results['metadatas'][0][i].get("source", "Unknown")
        })
    return contexts