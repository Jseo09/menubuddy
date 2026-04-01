# Risk Management Log – MenuBuddy

This document identifies, tracks, and provides mitigation strategies for risks associated with the MenuBuddy AI-powered RAG system.

| ID | Potential Risk                                            | Prob (1-5) | Impact (1-5) | Mitigation Strategy                                                                     | Status |
|:---|:----------------------------------------------------------|:----------:|:------------:|:----------------------------------------------------------------------------------------|:-------|
| 1  | Web scraping fails due to website structure changes       |     4      |      5       | Use multiple parsing strategies (HTML + fallback heuristics) and test on multiple sites | Open   |
| 2  | Anti-bot protection blocks scraping (DoorDash, UberEats)  |     5      |      4       | Restrict supported sources to scrape-friendly websites and document limitations         | Open   |
| 3  | Poor menu extraction accuracy (missing items)             |     4      |      5       | Improve parsing logic, filter noise, and validate extracted items before storing        | Open   |
| 4  | LLM hallucinates menu items not in data                   |     3      |      5       | Enforce strict grounding prompt and add verification step (validator module)            | Open   |
| 5  | Missing allergen/ingredient information                   |     5      |      4       | Always return safe fallback response and include disclaimer                             | Open   |
| 6  | Vector database retrieval returns irrelevant items        |     3      |      4       | Improve formatting of stored data and refine query embeddings                           | Open   |
| 7  | API failures or rate limits (LLM/embedding)               |     3      |      5       | Add error handling, retries, and fallback messages                                      | Open   |
| 8  | OCR errors when extracting from images                    |     4      |      3       | Use high-quality images and refine OCR prompt for better extraction                     | Open   |
| 9  | System crash due to unexpected input or empty data        |     2      |      5       | Add input validation, error handling, and safe fallback responses                       | Open   |
| 10 | High API Costs: LLM/Embedding usage exceeds budget        |     4      |      4       | Implement local caching for common queries and use smaller models for basic tasks       | Open   |
| 11 | Latency/Slow Response: Pipeline takes too long to process |     4      |      3       | Use asynchronous processing and provide a "loading" state in the CLI/UI                 | Open   |
| 12 | Vector Collisions: Data from different restaurants mix up |     2      |      4       | Use metadata filtering in Vector DB to isolate searches by Restaurant ID                | Open   |
| 13 | Stale Data: Menu prices change after the initial scrape   |     5      |      3       | Implement a timestamp system and display a "Last Updated" notice to users               | Open   |
| 14 | Inconsistent Formatting: Menus vary wildly in layout      |     4      |      4       | Normalize all scraped data into a standardized JSON schema before LLM processing        | Open   |
| 15 | Context Window Limits: Menu is too large for LLM          |     3      |      4       | Implement a chunking strategy or recursive summarization for massive menus              | Open   |
| 16 | Dependency Updates: Library updates break existing code   |     3      |      3       | Pin versions in `requirements.txt` and use a virtual environment                        | Open   |
| 17 | Unstructured Specials: Fails to parse daily specials      |     4      |      2       | Flag unstructured sections as "See Restaurant for Details" to avoid errors              | Open   |
| 18 | Prompt Injection: Users try to "jailbreak" the LLM        |     2      |      4       | Sanitize user inputs and use a strict system prompt for menu-only tasks                 | Open   |
| 19 | Environment Drift: Code fails on VM vs local machine      |     3      |      4       | Use Docker or consistent environment configs across the Mac and VM                      | Open   |
| 20 | Storage Overflow: Scraped images/logs fill disk space     |     2      |      3       | Implement a cleanup script to rotate logs and delete old image files                    | Open   |