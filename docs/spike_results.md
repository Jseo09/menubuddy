# Spike Results – MenuBuddy RAG System

## Overview

This spike assessed the feasibility of developing a retrieval-augmented generation (RAG) system that ingests restaurant menus from web pages or images, stores them in a vector database, and answers user questions about menu items and prices. The objective was to validate core pipeline components before building a more reliable and verifiable grounded system for Milestone 1.

The prototype confirmed the ability to scrape menu data, store it in a vector database, retrieve relevant information, and generate answers using a language model. Several limitations were identified, prompting architectural improvements for the Milestone 1 implementation.

---

# What Worked

## Scraping Menus and Prices

The system successfully extracted menu items and prices from multiple restaurant websites. HTML parsing was effective when menu data used predictable structures, such as table rows or consistent HTML classes.

The scraper detected menu items using common patterns, including structured tables and specific HTML tags found on menu aggregation sites. With consistent HTML structure, the system reliably extracted item–price pairs and converted them into structured text.

The prototype included a fallback extraction step using a language model when direct HTML parsing was unsuccessful. This enabled the system to recover menu information from less structured pages where traditional scraping was insufficient.

---

## Generation of Menu Answers

Once the menu data was stored in the vector database, the retrieval system could locate relevant menu entries based on user queries. The language model could then generate natural responses that summarized the retrieved information.

For example, when a user asked about lemonade options, the system retrieved related menu entries and generated an answer listing the available lemonade beverages and their prices. The responses were generally accurate when the relevant items were successfully retrieved from the vector database.

This confirmed that the ingestion → storage → retrieval → generation pipeline was functional and capable of answering menu-related queries.

---

# Identified Weaknesses

## Lack of Reliable Citations

The initial prototype did not include explicit source mapping or inline citations. While the system used retrieved data internally, the answers themselves did not clearly show which menu entries the information came from. This made it difficult to verify whether the generated answer was fully grounded in the retrieved data.

---

## Risk of Hallucination

Because the language model was allowed to generate answers freely, there was a risk that the model could introduce menu items or prices that were not present in the retrieved data. This is a known issue in LLM-based systems and highlights the need for stronger grounding mechanisms.

---

## Website Formatting Differences

Another major limitation was the variability of restaurant websites. Many menu pages use different HTML structures, JSON-based rendering, or dynamically generated content.

Because of this, scraping logic that works well for one website may fail on another. The spike confirmed that menu extraction needs to support multiple parsing strategies and fallback mechanisms to handle diverse website formats.

---
## System Evolution

The initial prototype used a simple pipeline: restaurant menu pages were scraped, and the extracted text was sent directly to a language model to answer user questions. While this demonstrated the feasibility of menu question answering, it lacked reliability, transparency, and verification. Generated answers could not be traced to the original data, and there was a risk of the model inventing menu items or prices.

For Milestone 1, we redesigned the system architecture to achieve a higher engineering standard. Rather than using direct prompts, we implemented a structured Retrieval-Augmented Generation (RAG) pipeline with explicit grounding. Menu data is ingested, stored in a vector database, retrieved by semantic similarity, and provided to the model as structured context. Each retrieved entry receives an identifier and source metadata, enabling the model to generate answers with inline citations referencing the exact menu data used.

We also introduced a verification layer to assess whether generated responses are fully supported by the retrieved context. This mechanism detects unsupported claims and provides a measurable indication of hallucination risk. As a result, the system has evolved from a basic scraping prototype to a grounded, citation-based menu assistant with verifiable outputs and greater transparency.

This transition marks a shift from a proof-of-concept to a robust engineering solution that emphasizes traceability, reliability, and measurable grounding of model responses.

---

# Architectural Changes Made for Milestone 1

Based on the findings from the spike, several architectural improvements were implemented:

**Grounded Retrieval Context**
Retrieved menu entries are now assigned unique IDs and source metadata. These IDs are used when generating answers so that each claim can reference the exact piece of retrieved data.

**Citation-Based Answer Generation**
The generation prompt now requires the language model to include citations (e.g., [1], [2]) for every factual claim. This ensures that responses are explicitly grounded in retrieved context.

**Verification Layer**
A separate verification step was introduced to evaluate whether the generated answer is fully supported by the retrieved context. The system outputs a verification verdict such as `VERDICT: OK` or `VERDICT: UNSUPPORTED`.

**Improved Scraping Strategy**
The scraper now attempts multiple extraction strategies including structured HTML parsing and LLM-based extraction for unstructured pages.

These changes transform the system from a simple prototype into a more reliable and transparent grounded retrieval system.

---

# Plan to Strengthen Grounding

To further improve reliability and reduce hallucination risk, the following improvements are planned:

1. Expand scraping support to handle additional website formats and dynamic menu structures.
2. Improve metadata tracking so every retrieved chunk includes clear source references.
3. Implement stricter generation rules that prevent the model from answering when supporting context is missing.
4. Add automated evaluation tests to measure grounding accuracy and retrieval precision.
5. Continue refining the verification layer to detect unsupported claims more effectively.

These improvements will help ensure that the system produces answers that are transparent, verifiable, and fully grounded in the original menu data.

---

# Summary

The spike successfully demonstrated the feasibility of building a menu-based RAG system. While the initial prototype was functional, it revealed several limitations related to grounding, citation transparency, and scraping robustness. The architectural improvements introduced in Milestone 1 address these issues by enforcing citation-based answers, introducing verification checks, and improving the ingestion pipeline. These changes significantly strengthen the reliability and trustworthiness of the system.
