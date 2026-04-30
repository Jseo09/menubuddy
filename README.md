# MenuBuddy AI Assistant

---

MenuBuddy is a specialized Retrieval-Augmented Generation (RAG) system that converts restaurant menus (via URL scraping or QR Code) into an interactive assistant. It utilizes a Haystack-based pipeline and the Google Gemini 2 Flash model to ensure accuracy and prevent price hallucinations.

---

## Modular Architecture
### Ingestion Module
- **Scraper**: Uses Docling and BeautifulSoup to extract structured item/price data from HTML or images.
- **Vision OCR**: Leverages Gemini 2 Flash to transcribe physical menu images.
- **Vector DB**: Stores menu "chunks" in **ChromaDB** for high-speed retrieval.

### Retrieval & Generation
- **Context Retrieval**: Finds the top 5 most relevant menu sections using a semantic retriever.
- **Grounded Generation**: Gemini 2 Flash synthesizes answers using **ONLY** the provided menu context and strictly formatted citations (e.g., `[1]`).

### Validation Gatekeeper
- **Fact-Checker**: A final verification stage that compares the LLM’s claims against the original source data using a separate validator client.
- **Status Verdicts**: Every response is categorized to ensure the user knows the reliability of the information.

---

# Getting Started

## Prerequisites
- **Python 3.10+**
- **Google Gemini API Key**: Required for both the RAG pipeline and the verification stage.

## 1. Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/Jseo09/menubuddy.git](https://github.com/Jseo09/menubuddy.git)
cd MenuBuddy
pip install -r requirements.txt
```

## 2. Using MenuBuddy
```bash
python app.py
```