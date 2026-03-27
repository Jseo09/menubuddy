# MVP Definition – MenuBuddy

## 1. MVP Workflow

The MVP follows a simple end-to-end pipeline:

1. User scans a QR code or inputs a restaurant menu URL  
2. System retrieves the menu webpage  
3. Menu data is extracted using web scraping (HTML parsing) or OCR (for images)  
4. Extracted menu items are cleaned and formatted into structured text  
5. Menu data is stored in a vector database using embeddings  
6. User submits a natural-language question about the menu  
7. System retrieves relevant menu items using semantic search (RAG)  
8. LLM generates a grounded answer using only retrieved context  
9. System verifies whether the answer is supported by the context  
10. Final output is returned:  
   - Grounded answer with citations, or  
   - Refusal if the information is not supported  

---

## 2. What a User Can Do in the MVP

- Scan a QR code or input a menu URL  
- Ask questions about:
  - Menu items  
  - Prices  
  - Basic dietary preferences (e.g., vegetarian, spicy)  
- Receive:
  - Grounded answers based on menu data  
  - Citations referencing menu entries  
- Receive a safe fallback response when information is missing  

---

## 3. Out of Scope for Milestone 2

- Integration with restaurant POS systems  
- Real-time menu updates  
- Guaranteed allergen or nutritional accuracy  
- Advanced personalization (user profiles, history)  
- Multi-language support  
- Voice input/output  
- Advanced UI/UX (only basic interface included)  
- Full support for all restaurant websites  

---

## 4. Supported Menu Source Types

- Public restaurant menu webpages (HTML-based)  
- Menu aggregation websites  
- Images containing menus (via OCR)  
- QR codes linking to supported menu pages  

---

## 5. Known Limitations

- Web scraping may fail on:
  - JavaScript-heavy websites  
  - Anti-bot protected platforms (e.g., DoorDash)  
- Extracted menu data may be incomplete or noisy  
- Some menus lack ingredient or allergen details  
- OCR accuracy depends on image quality  
- LLM responses depend on retrieved context quality  
- System may fail if relevant data is missing  
- Performance may vary due to API latency  

---

## 6. Definition of Done

The MVP is complete when:

- Users can input a URL or scan a QR code successfully  
- At least 80% of menu items are correctly extracted  
- Users can ask natural-language questions  
- Relevant menu data is retrieved using RAG  
- Answers are generated using only retrieved context  
- Responses include citations  
- Unsupported questions return a safe refusal  
- Verification confirms answers are grounded  
- Response time is ≤ 5 seconds  
- System runs end-to-end without crashing  

---

## 7. Example Scenario

A user scans a QR code and asks:

> “Do you have any vegetarian options?”

System response:

> “Yes, the menu includes Garden Salad [1] and Vegetable Soup [2].”

If information is missing:

> “The menu does not provide enough information. Please confirm with restaurant staff.”
