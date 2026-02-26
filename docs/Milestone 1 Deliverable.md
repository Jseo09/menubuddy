# Milestone 1 Deliverables  
## Team: MenuBuddy  
### Focus: Grounded, Verifiable Menu-Based Food Assistant  

---

## Context

The team successfully demoed a spike showing:

- Menu scraping from restaurant websites  
- Storing menu data in a database  
- LLM generating answers grounded to stored menu data  

However:

- Answers are not currently cited  
- There is no explicit source verification layer  
- There is no measurable grounding evaluation  
- There is no hallucination detection or fact-checking mechanism  

Milestone 1 must elevate the system from a working prototype to a **verifiable grounded retrieval system with measurable reliability**.

---

# Milestone 1 Objective

By Milestone 1, your team must demonstrate:

- A working ingestion → storage → retrieval → generation pipeline  
- Explicit grounding to scraped menu data  
- Inline citation or source mapping in every answer  
- A fact-checking / verification layer  
- Measurable evaluation of grounding accuracy  
- Clean GitHub structure with engineering artifacts  

---

# 1. Final PRD-Lite (Updated)

Your PRD must clearly define the product as:

> A grounded restaurant menu assistant that provides verifiable answers sourced directly from scraped menu data.

## The PRD must include:

### A. Grounding Requirement (Non-Negotiable)

- Every answer must be traceable to specific menu item(s) in the database  
- The system must not generate dishes not present in stored data  
- If requested information is not available in the menu data, the system must refuse to answer  

### B. MVP Scope (April 5 Demo)

Must include:

- URL ingestion of restaurant menu  
- Structured storage (items, categories, prices, dietary info if available)  
- Retrieval-based answer generation  
- Inline citation markers or source mapping  
- Refusal behavior when unsupported  

### C. Acceptance Criteria (Testable)

Examples:

- 100% of answers include citation markers  
- No invented menu items  
- Refusal triggered when data absent  
- Retrieval returns correct menu items ≥ 85% of test cases  

---

# 2. Source Citation & Traceability Layer (Required)

You must implement:

- Inline citation markers in output (e.g., [1], [2])  
- Mapping from answer segments to menu items in database  
- Optional snippet display (menu item text shown below answer)

If the LLM mentions a menu item not in the database, the system must:

- Block the response  
- Or regenerate using constrained context  

Manual inspection does not count as fact-checking.

---

# 3. Fact-Checking / Hallucination Guard (Required)

You must implement at least one of the following:

- Post-generation validation: verify all named menu items exist in retrieved results  
- Token-level comparison between answer and retrieved data  
- Schema enforcement (only allow values from structured fields)  

If validation fails, system must:

- Reject answer  
- Or regenerate with stricter constraints  

---

# 4. Evaluation Starter Kit (Minimum 20 Test Queries)

Create:

/docs/evaluation_test_cases.md

Include:

- 20 user queries  
- Expected menu item(s)  
- Retrieved menu item(s)  
- Generated answer  
- Verification result (Pass/Fail grounding)  

Required metrics:

- Retrieval accuracy  
- Grounding accuracy  
- Hallucination rate  
- Refusal accuracy  

---

# 5. Spike Results Update

Create:

/docs/spike_results.md

Must include:

- What worked in scraping  
- What worked in generation  
- Identified weaknesses (citation absence, hallucination risk)  
- Architectural changes made for Milestone 1  
- Plan to strengthen grounding  

---

# 6. Architecture Diagram (Updated)

Create:

/docs/architecture.png

Must clearly show:

URL  
→ Scraper  
→ Structured Database  
→ Query Embedding  
→ Retrieval  
→ LLM Generation  
→ Citation Formatter  
→ Fact-Check Validator  
→ Output  

Clearly label deterministic vs generative components.

---

# 7. Required Technical Walkthrough Video (No UI Required)

Submit a short technical walkthrough video (5–8 minutes) showing:

- Scraper execution  
- Stored structured data  
- Retrieval results (console/log)  
- LLM context injection  
- Citation formatting  
- Fact-check validation logic running  

UI polish is not required. Engineering transparency is required.

---

# 8. GitHub Repository Requirements

Your repository must include:

- /docs/PRD.md  
- /docs/spike_results.md  
- /docs/evaluation_test_cases.md  
- /docs/architecture.png  
- /src/scraper.py  
- /src/retrieval.py  
- /src/generator.py  
- /src/citation_formatter.py  
- /src/validator.py  

Additionally:

- Updated README with setup and run instructions  
- requirements.txt  
- .env.example  
- At least one meaningful commit per team member  
- Sprint 1 issue board with assigned owners  

---

# Required Live Demo for Milestone 1

You must demonstrate:

1. Menu ingestion from a URL  
2. Stored structured menu data  
3. Retrieval results shown  
4. Generated answer with citations  
5. Fact-check validation step  
6. A refusal case when unsupported  

If answers are generated without citation and validation, Milestone 1 is incomplete.

---

# Milestone 1 Standard

Your project must evolve from:

“We scrape menus and ask GPT.”

To:

“We engineered a grounded, citation-based menu assistant with measurable hallucination control and verifiable outputs.”

This is the expected senior-level standard.
