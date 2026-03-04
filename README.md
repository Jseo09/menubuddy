# MenuBuddy AI Assistant


---


MenuBuddy is a specialized Retrieval-Augmented Generation (RAG) system that converts restaurant menus by URL scraping or Vision OCR
into an interactive assistant. It is designed with a strict architecture to prevent price hallucinations and menu errors.


---


## Modular Architecture
### Ingestion Module
- Scraper: Uses BeautifulSoup to extract structured item/price data from HTML.
- Vision OCR: Uses Gemini 1.5 Flash to transcribe physical menu images.
- Vector DB: Stores menu "chunks" in ChromaDB for high-speed retrieval.


## Retrieval & Generation
- Context Retrieval: Finds the most relevant menu sections
- Grounded Generation: Gemini 2.0/2.5 synthesizes answers using ONLY the provided menu context and formatted citations [ID].


## Validation Gatekeeper
- Fact-Checker: A final verification stage that compares the LLM’s claims against the original source data.
- Refusal Logic: If a claim (like a price) cannot be verified, the system triggers a "Refusal Case" rather than providing false info.


---


# Getting Started


---


## Prerequisites
- Python 3.9
- A Google Gemini API Key required
- A OpenAI API (Embedchain LLM Provider)


## 2. Installation
Clone the repository and install dependencies:


`git clone https://github.com/Jseo09/menubuddy.git`


`cd MenuBuddy`


`pip install -r requirements.txt`


## Environment Setup
Create a new `.env` file in the root directory and add your API keys:


`GOOGLE_API_KEY=your_gemini_key_here`


`OPENAI_API_KEY=your_openai_key_here`


---
# Usage
Run the application by using the command:
`python main.py`


## Transparency Logs
Notice when running MenuBuddy the console will display labels at each stage:
- `[DETERMINISTIC STAGE: SCRAPING]` — Shows the raw data found.
- `[DETERMINISTIC STAGE: RETRIEVAL]` - Shows the specific menu chunks used for the answer.
- `[GENERATIVE STAGE: LLM]` - Shows the AI-synthesized response.
- `[DETERMINISTIC STAGE: VALIDATION]` - Confirms the verdict by stating `OK` or `UNSUPPORTED`
---

