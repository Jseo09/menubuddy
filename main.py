import os
import re
import time
from dotenv import load_dotenv
import google.genai as genai

from src.validator import verify_answer_against_context
from src.scraper import extract_menu_data
from src.config import CONFIDENCE_THRESHOLD
from haystack import Pipeline, Document
from src.question_filter import is_irrelevant_question
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage

from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator


def safe_run(func, *args, **kwargs):
    """
    Attempts to run a Haystack component.
    On failure, waits 2 seconds and retries once.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"  [!] Primary attempt failed: {e}. Retrying in 2 seconds...")
        time.sleep(2)
        return func(*args, **kwargs)


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

        if is_irrelevant_question(query):
            print("\n--- MENU BUDDY ANSWER ---")
            print(
                "I'm sorry, that question is outside the menu domain. I can only answer questions about menu items, prices, and menu-related details.")
            print("\n--- VALIDATION STATUS ---")
            print("Status: FLAGGED (IRRELEVANT)")
            print("\n--- VALIDATION DETAILS ---")
            print("Prefilter refusal: question classified as out of scope before retrieval.")
            continue

        print("[STAGE: RETRIEVAL] Searching ChromaDB...")
        try:
            # Wrapped retrieval with safe_run
            retrieval_res = safe_run(retriever.run, query=query, top_k=5)
            docs = retrieval_res["documents"]
        except Exception as e:
            print("\n--- ERROR ---")
            print("I'm having trouble accessing my menu database right now.")
            print(f"Status: FLAGGED\nDetails: {e}")
            continue

        if not docs:
            print("No relevant menu data found in the database.")
            continue

        top_score = getattr(docs[0], "score", None)
        if top_score is None or top_score < CONFIDENCE_THRESHOLD:
            print("\n--- MENU BUDDY ANSWER ---")
            print("I'm sorry, I don't have enough reliable menu information to answer that.")
            print("\n--- VALIDATION STATUS ---\nStatus: FLAGGED")
            print(
                f"\n--- VALIDATION DETAILS ---\nTop retrieval score {top_score} below threshold {CONFIDENCE_THRESHOLD}.")
            continue

        print("[STAGE: GENERATION] Generating cited answer...")
        try:
            # Wrapped generation with safe_run
            res = safe_run(pipe.run, data={
                "prompt_builder": {
                    "template_variables": {"documents": docs, "query": query},
                    "template": template
                }
            })
            answer = res["genai"]["replies"][0].text
        except Exception as e:
            print("\n--- MENU BUDDY ANSWER ---")
            print("I'm currently having trouble generating an answer due to a service error. Please try again.")
            print("\n--- VALIDATION STATUS ---\nStatus: FLAGGED (CONNECTION ERROR)")
            print(f"Details: {e}")
            continue

        # --- Calculate Metric ---
        coverage = calculate_citation_coverage(answer)
        context_block = "\n".join(
            [f"[{i + 1}] {d.content} (SOURCE: {d.meta['source']})" for i, d in enumerate(docs)]
        )

        validation_text, verdict = verify_answer_against_context(
            validator_client,
            query,
            answer,
            context_block
        )

        status = "VERIFIED" if verdict == "OK" else "FLAGGED"
        if verdict == "IRRELEVANT":
            status = "FLAGGED (IRRELEVANT)"

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