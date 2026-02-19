# MenuBuddy
# Engineering Spike Plan

## Riskiest Assumption

We assume that it is feasible to reliably scrape and structure real-world restaurant menus, and to generate grounded large language model (LLM) answers using retrieval-augmented generation (RAG) without introducing hallucinated menu items.

---

## Spike Goal

Within **10-20 days**, build a working prototype that:

- Scrapes **one real public restaurant menu webpage**
- Structures at least **80% of the menu items correctly**
- Using **RAG produce **5 different test cases
- Produces **grounded answers (no invented dishes)** in under **5 seconds**

---

## Inputs to Outputs

### Inputs

- URL of the public restaurant menu webpage
- User's natural-language question  
  Example:  
  > “Do you have vegetarian soup?”

---

### Processing

1. Scrape and extract textual content from the menu.
2. Organize the extracted data into **item-level JSON format**.
3. Generate vector embeddings for each menu item.
4. Retrieve relevant menu items using vector-based search.
5. Provide the retrieved contextual information to the language model using a grounding prompt.

---

### Outputs

- Answer based on menu context
- Names of referenced menu items
- Default response when information is unavailable

---

## 2–3 Minute Demo Plan (Live)

1. Scanning the QR code loads the menu URL.
2. Display the extracted structured menu items as a JSON preview.
3. Allow users to submit questions regarding the menu:
   - “Do you have vegetarian options?”
   - “Does this contain nuts?”
4. Present the language model's answer, ensuring it is grounded in the extracted menu text.
5. Demonstrate an edge case, such as missing allergen information, where the system responds:
   > "Menu does not provide enough information."

---

## Owners + Tasks

### Backend Lead

- Develop web scraping functionality and organize extracted data into a structured menu format.
- Create a temporary in-memory data store for menu information.
- Implement embedding generation and enable vector-based search capabilities.
- Design a grounding prompt for model initialization.
- Integrate the large language model (LLM) API.

---

### Frontend / Integration

- Build a simple web UI.
- Implement QR link flow.
- Display answers cleanly.

---

## Exit Criteria (Pass/Fail Checks)

### Pass if:

- ≥80% of menu items are correctly extracted
- ≥85% of test questions are answered correctly
- Hallucination rate <10% in test set
- Response time <5 seconds
- Demo runs without crashing

---

### Fail if:

- Scraping fails on the selected test menu
- LLM invents menu items repeatedly
- Response time exceeds 8–10 seconds
- Demo cannot run end-to-end

---

## If It Fails

### If data scraping yields inconsistent results:

- Utilize a manually curated static menu JSON for the MVP.
- Restrict the demonstration to one or two structured restaurant examples.

### If the rate of model hallucination is excessive:

- Implement a more stringent grounding prompt.
- Add answer validation (check item names against retrieved items).
- Decrease the context window size to enhance response precision.
- Cite specific item or line from scraped menu explicitly stating the criteria of request.

### If API cost or latency is too high:

- Cache embedding vectors to reduce redundant computations.
- Select a smaller embedding model to decrease computational requirements.
- Restrict the number of top-K retrieved items to optimize performance.
