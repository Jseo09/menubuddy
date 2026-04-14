import os
import re
from dotenv import load_dotenv
import google.genai as genai

from src.validator import verify_answer_against_context
from src.scraper import extract_menu_data

from haystack import Pipeline, Document
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage

from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator

def calculate_citation_coverage(text):
    """Calculates the percentage of sentences that include a citation [n]."""
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]
    if not sentences:
        return 0.0
    cited_count = sum(1 for s in sentences if re.search(r'\[\d+\]', s))
    return round(cited_count / len(sentences), 2)

def setup_pipeline():
    document_store = ChromaDocumentStore(persist_path="./chroma_db")

    retriever = ChromaQueryTextRetriever(document_store=document_store)
    genai_chat = GoogleGenAIChatGenerator(model="gemini-2.5-flash-lite")
    prompt_builder = ChatPromptBuilder()

    pipe = Pipeline()
    pipe.add_component("prompt_builder", prompt_builder)
    pipe.add_component("genai", genai_chat)
    pipe.connect("prompt_builder.prompt", "genai.messages")

    return document_store, retriever, pipe


def main():
    load_dotenv()

    validator_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    doc_store, retriever, pipe = setup_pipeline()
    cleaner = DocumentCleaner()
    splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=20)

    print("\n=== MenuBuddy: Modular CLI (v3.1) ===")
    choice = input("Import menu (1=URL, 2=Image, 3=Skip to Chat): ").strip()

    if choice in ["1", "2"]:
        source = input("Enter URL or Image Path: ").strip()
        print(f"\n[STAGE: INGESTION] Processing {source} with Docling...")

        raw_markdown = extract_menu_data(source)

        if raw_markdown:
            doc = Document(content=raw_markdown, meta={"source": source})
            cleaned = cleaner.run(documents=[doc])
            chunks = splitter.run(documents=cleaned["documents"])

            doc_store.write_documents(chunks["documents"])
            print(f"[OK] {len(chunks['documents'])} chunks saved to local ChromaDB.")
        else:
            print("[ERROR] Could not process source.")
            return

    print("\n" + "=" * 40)
    print("READY: Ask MenuBuddy about the stored menus")
    print("=" * 40)

    template = [
        ChatMessage.from_user(
            """Answer based on the menu chunks. Use numbered citations like [1].

Context:
{% for doc in documents %}
Chunk [{{ loop.index }}] (Source: {{ doc.meta['source'] }}):
{{ doc.content }}
---
{% endfor %}

Question: {{ query }}
Answer:"""
        )
    ]

    while True:
        query = input("\nUser Query: ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        print("[STAGE: RETRIEVAL] Searching ChromaDB...")
        retrieval_res = retriever.run(query=query, top_k=5)
        docs = retrieval_res["documents"]

        if not docs:
            print("No relevant menu data found in the database.")
            continue

        # Check retrieval confidence
        top_score = getattr(docs[0], "score", 0.0)
        CONFIDENCE_THRESHOLD = 0.35

        if top_score < CONFIDENCE_THRESHOLD:
            print(f"[WARNING] Low retrieval confidence ({top_score:.2f}). Result might be unreliable.")

        print("[STAGE: GENERATION] Generating cited answer...")
        res = pipe.run(data={
            "prompt_builder": {
                "template_variables": {"documents": docs, "query": query},
                "template": template
            }
        })

        answer = res["genai"]["replies"][0].text

        # --- Calculate Metric ---
        coverage = calculate_citation_coverage(answer)

        context_block = "\n".join(
            [f"[{i + 1}] {d.content} (SOURCE: {d.meta['source']})" for i, d in enumerate(docs)]
        )

        validation_text, verdict = verify_answer_against_context(
            validator_client,
            answer,
            context_block
        )

        status = "VERIFIED" if verdict == "OK" else "FLAGGED"

        print("\n--- MENU BUDDY ANSWER ---")
        print(answer)

        print("\n--- VALIDATION STATUS ---")
        print(f"Status: {status}")

        print("\n--- VALIDATION DETAILS ---")
        print(validation_text)

        print("\nSources:")
        for i, d in enumerate(docs):
            print(f"[{i + 1}] {d.meta['source']}")


if __name__ == "__main__":
    main()
