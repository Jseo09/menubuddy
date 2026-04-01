# Risk Management Table – MenuBuddy

| ID | Potential Risk | Probability (1-5) | Impact (1-5) | Mitigation Strategy | Status |
|----|--------------|------------------|-------------|-------------------|--------|
| 1 | Web scraping fails due to website structure changes | 4 | 5 | Use multiple parsing strategies (HTML + fallback heuristics) and test on multiple sites | Open |
| 2 | Anti-bot protection blocks scraping (e.g., DoorDash) | 5 | 4 | Restrict supported sources to scrape-friendly websites and document limitations | Open |
| 3 | Poor menu extraction accuracy (missing items) | 4 | 5 | Improve parsing logic, filter noise, and validate extracted items before storing | Open |
| 4 | LLM hallucinates menu items not in data | 3 | 5 | Enforce strict grounding prompt + add verification step (validator module) | Open |
| 5 | Missing allergen/ingredient information | 5 | 4 | Always return safe fallback response and include disclaimer | Open |
| 6 | Vector database retrieval returns irrelevant items | 3 | 4 | Improve formatting of stored data and refine query embeddings | Open |
| 7 | API failures or rate limits (LLM/embedding) | 3 | 5 | Add error handling, retries, and fallback messages | Open |
| 8 | OCR errors when extracting from images | 4 | 3 | Use high-quality images and refine OCR prompt for better extraction | Open |
| 9 | System crash due to unexpected input or empty data | 2 | 5 | Add input validation, error handling, and safe fallback responses | Open |
