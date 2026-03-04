# Product Requirements Document (PRD): MenuBuddy

## 1. Product Definition
**MenuBuddy** is a grounded restaurant menu assistant designed to provide verifiable, hallucination-free answers sourced directly from scraped menu data.

---

## 2. Core Requirements

### A. Grounding & Integrity (Non-Negotiable)
* **Traceability:** Every response must be traceable to specific menu item(s) currently stored in the system database.
* **Zero Hallucination:** The system is strictly prohibited from generating dishes, prices, or ingredients not explicitly present in the stored data.
* **Hard Refusal:** If requested information (e.g., a specific dish or dietary detail) is not available in the menu data, the system must explicitly refuse to answer rather than providing an estimate.

### B. MVP Scope (Target: April 5 Demo)
The following features must be functional for the initial demonstration:
1.  **URL Ingestion:** Capability to scrape and parse restaurant menu data from provided web links.
2.  **Structured Storage:** Data must be organized by:
    * Item Name
    * Category (Appetizers, Mains, etc.)
    * Price
    * Dietary Info (if listed)
3.  **Retrieval-Based Generation:** An RAG (Retrieval-Augmented Generation) pipeline that pulls context before generating a response.
4.  **Inline Citations:** Automatic mapping of answers to sources using citation markers (e.g., `[1]`).
5.  **Refusal Logic:** A programmed behavior to trigger a "Data Unavailable" response when the retrieval score is below the confidence threshold.

---

## 3. Technical Specifications

| Component | Requirement |
| :--- | :--- |
| **Input Type** | URL (Web Scraping) |
| **Data Format** | JSON / Vector Embeddings |
| **Architecture** | RAG (Retrieval-Augmented Generation) |
| **Citations** | Numerical or Source Mapping (e.g., [Source: Dinner Menu]) |

---

## 4. Acceptance Criteria (Testable)

The MVP will be considered successful if it meets the following metrics during the April 5 Demo:

* **Citation Accuracy:** 100% of factual answers must include visible citation markers.
* **Data Integrity:** 0 instances of "invented" menu items during stress testing.
* **Refusal Reliability:** 100% trigger rate for the refusal message when querying items not present in the database.
* **Retrieval Performance:** The system must return the correct menu items in **≥ 85%** of test cases.

---

