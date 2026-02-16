# Problems + Target Users

Restaurant menus frequently present comprehension challenges due to:

- Small font sizes  
- Ambiguous descriptions  
- Insufficient accessibility features  
- Language barriers  

Seniors, individuals with visual impairments, non-English speakers, and diners with dietary restrictions often struggle to efficiently identify safe and appropriate menu options.

These challenges can lead to:

- User frustration  
- Potential safety risks (e.g., allergen exposure)  
- Increased demands on restaurant staff for clarification  

**Menu Buddy** aims to enhance menu accessibility, clarity, and safety through AI-powered question answering.

---

# Goal / Success Metrics

The primary objective of Menu Buddy is to enhance menu accessibility and safety by providing accurate, evidence-based AI-powered question answering.

## 1. Answer Accuracy (Grounded Q&A Quality)

- ≥85% of menu-related questions answered correctly  
- Answers must rely exclusively on extracted menu data (validated manually)  
- Hallucination rate <10% during testing  

## 2. Time Saved per User Task

- Users locate relevant menu information in **<30 seconds on average**
- Compared to manual menu scanning

## 3. User Satisfaction and Usability

- Average satisfaction score ≥4/5 (pilot survey)
- ≥70% of test users report easier menu navigation

---

# MVP User Stories

- **Senior diner**  
  As a senior diner, I want to ask simple questions in clear language so I can understand available dishes without reading small or complex text.

- **Non-English speaker**  
  As a non-English speaker, I want to ask questions in my preferred language so I can understand menu options without language barriers.

- **Visually impaired user**  
  As a visually impaired user, I want the system to read aloud or summarize menu items clearly so I can independently access menu information.

- **Diner with food allergies**  
  As a diner with allergies, I want to ask whether a dish contains specific ingredients so I can avoid unsafe food choices.

- **Health-conscious diner**  
  As a health-conscious diner, I want recommendations based on dietary preferences (e.g., vegetarian, low-carb) so I can choose appropriate meals.

- **Restaurant staff member**  
  As a restaurant staff member, I want common menu questions answered automatically so I can reduce repetitive explanations.

---

# MVP Scope vs Non-Goals

## In Scope (MVP)

### Menu Extraction & Cleaning
- Scrape and extract menu text from webpages  
- Structure into usable data (dish names, descriptions, categories)

### LLM + RAG-Based Q&A
- Answer natural-language questions  
- Responses grounded exclusively in extracted menu data  

### Basic Dietary & Allergy Keyword Handling
- Handle common queries (vegetarian, gluten, nuts, etc.)
- Only use explicitly available menu information  

### Simple Recommendation Logic
- Recommend items based on query preferences (e.g., spicy, vegetarian)

### Basic Web Interface
- Text input box  
- Answer display  
- Python backend integration  

### QR Code Menu Access
- Users access menu webpage via QR code scan  

---

## Nice to Have

- Multi-language translation support  
- Voice input and output  
- Popularity-based ranking for recommendations  
- Persistent database caching  
- Accessibility enhancements (large font toggle, high contrast mode)

---

## Explicit Non-Goals

- **Full Restaurant Management Integration**  
  No POS or internal database integration  

- **Guaranteed Allergen Certification**  
  No medical-grade allergen verification  
  Users must confirm with staff  

- **Personal User Accounts or Data Storage**  
  No collection or storage of personal data  

- **Automated Menu Updates Across All Restaurants**  
  Limited to selected test webpages  

- **Advanced Nutrition Calculations**  
  Calories/macros only shown if explicitly listed in menu  

---

# Acceptance Criteria

## 1. End-to-End QR → Answer Flow

- User scans QR code  
- Menu webpage loads successfully  
- ≥80% of visible menu items extracted and structured  
- Users submit natural-language questions  
- Response generated within **5 seconds**

System fails if:
- It crashes  
- It times out  
- It does not respond  

---

## 2. Grounded Menu Q&A (RAG Behavior)

- Answers generated exclusively from extracted menu data  
- ≥85% of evaluated test questions answered correctly  
- Hallucination rate <10%  
- Fail if referencing items not present in extracted data  

---

## 3. Allergy & Dietary Handling

- Users can ask ingredient/allergen questions  
- If allergen info missing, respond:  
  > “The menu does not provide enough information. Please confirm with the restaurant staff.”

- Include safety disclaimer  
- Must NOT generate unsupported ingredient/allergen info  

---

## 4. Basic Recommendation Logic

- Support recommendation queries (e.g., “Recommend a vegetarian dish.”)  
- Provide 1–3 relevant items  
- Do not recommend items that conflict with stated preferences  

---

## 5. Error Handling & Edge Cases

- Handle empty/ambiguous questions:  
  > “Can you clarify your request?”

- Safe failure scenarios:
  - Menu webpage inaccessible  
  - Extracted data empty  
  - LLM response unsuccessful  

- Display user-friendly error message instead of crashing  

---

# Assumptions

## Data Access

- Restaurant menus are publicly accessible and legally scrapable  
- Menu information is reasonably structured  
- Allergy/dietary information, when present, is explicit  
- Users access via smartphones with QR scanning  

## User Behavior

- Users ask straightforward menu-related questions  
- AI responses are informational only (not medical advice)

## Technical Feasibility

- LLM and embedding APIs remain accessible  
- Menu data size is manageable within session constraints  

---

# Constraints

## Time Constraints (Milestone 2 Scope)

- Limited number of test restaurant webpages  
- Advanced features may remain incomplete  
- MVP prioritizes:
  - QR scanning  
  - Data extraction  
  - Q&A functionality  

---

## Ethics & Privacy Limits

- No personal data collection or storage  
- No medical-grade allergen accuracy  
- Disclaimer shown for allergy/health inquiries  
- Only publicly available menu data processed  

---

## Platform & Technical Constraints

- Scraping reliability depends on website structure  
- LLM API costs and rate limits may restrict testing volume  
- Scalability depends on hosting environment  
- Extraction accuracy may decrease for large or poorly formatted menus  
