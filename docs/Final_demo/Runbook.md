# Runbook: MenuBuddy AI Assistant

## 1. Overview
MenuBuddy is a specialized Retrieval-Augmented Generation (RAG) system that converts restaurant menus (via URL scraping or QR codes) into an interactive assistant. It utilizes a Haystack-based pipeline and the Google Gemini 2 Flash model to ensure accuracy and prevent price hallucinations.

## 2. Technical Stack
* **LLM:** Google Gemini 2 Flash
* **Orchestration:** Haystack (RAG Pipeline)
* **Vector Database:** ChromaDB
* **Extraction:** Docling, BeautifulSoup (Web), Gemini Vision (OCR for QR/Images)
* **Frontend:** Flask (Python)

---

## 3. Setup & Installation

### Prerequisites
* Python 3.10+
* Google Gemini API Key

### Installation Steps
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Jseo09/menubuddy.git](https://github.com/Jseo09/menubuddy.git)
   cd menubuddy
   
## 4. Getting MenuBuddy Started
1. ** Use python to run app python file:**
    ```bash
    python app.py
   
## 5. Troubleshooting and Maintenance 

## 5. Troubleshooting & Maintenance

| Issue | Potential Cause | Resolution                                                                                                   |
| :--- | :--- |:-------------------------------------------------------------------------------------------------------------|
| **Authentication Error** | Missing or invalid API Key | Verify `GOOGLE_API_KEY` is correctly set in your `.env` file.                                                |
| **Extraction Failure (Web)** | Dynamic JS or Bot Protection | If a URL fails to scrape, take a screenshot of the menu and upload it via the **Vision OCR** module instead. |
| **Price Hallucinations** | Context Window Gaps | Check the "Status Verdict" in the UI; re-ingest the menu if data is incomplete.                              |
| **Database Bloat** | Old Sessions | Periodically clear the `uploads/` folder and reset the ChromaDB collection if necessary.                     |
| **OCR Inaccuracy** | Low Image Quality | Ensure uploaded menu photos are well-lit and legible for the Gemini Vision OCR module.                       |
| **Dependency Conflicts** | Python Version Mismatch | Ensure you are using **Python 3.10+** and install requirements in a clean environment.                       |
| **Flask Server Error** | Port 5000 in use | Verify no other processes are using port 5000 before running `app.py`.                                       |
