# Milestone 2 Grade — Venture 1: MenuBuddy

**Graded:** April 8, 2026
**Deadline:** April 5, 2026 (end of day)
**Late Commits:** None — all 69 commits are on or before 4/5/2026.

---

## Overall Grade: 90/100

---

## Summary

MenuBuddy demonstrates a working RAG-based menu assistant with both CLI and Flask web UI, supporting URL and image ingestion via Docling, ChromaDB vector storage, and Gemini-powered answer generation with citation prompting. The evaluation suite covers 20 test queries across 4 real restaurant menus with strong retrieval accuracy (95%). However, the **validation/fact-checking layer is not integrated** into the running application despite being a core Milestone 2 requirement — `validator.py` exists but is never called by `main.py` or `app.py`. Several `src/` modules are orphaned, and the demo script describes behavior the code doesn't actually produce.

### Video Review Notes
The demo video is a 3-minute silent screen recording showing the Flask web UI at localhost:5000. **Strengths observed:** Image ingestion works (Wendy's and Jersey Mike's menus uploaded via OCR), 5+ questions answered with numbered citations, and **two strong refusal cases** — Jersey Mike's desserts ("I do not know...the provided menu information only lists cold and hot subs [1,2,3,4,5]") and a customization question ("the provided text does not contain information regarding custom order requests"). **Gaps:** URL ingestion not demonstrated (only image), no app launch shown, validation step is opaque in the Process Log (shows "Sources Found" but no explicit fact-checking), no explanation of known limitations (silent video), and no display of stored structured data.

---

## Category Breakdown

### 1. End-to-End Demo Path (22/25)
- Both URL and image ingestion paths work via Docling with QR code detection — nice touch.
- CLI (`main.py`) and web GUI (`app.py` with Flask) both exist and run.
- ChromaDB persistent storage with proper chunking (150 words, 20 overlap).
- Citation-based prompting with source mapping displayed to user.
- **Critical Gap:** Validation/fact-checking is NOT in the running pipeline. `validator.py` exists but is never imported or called. The demo script references "VERIFIED - OK" output, but the code does not produce this. Milestone 2 explicitly requires validation "stronger than prompt-only grounding."
- Refusal logic is prompt-only ("If the information isn't in the chunks, say you don't know") — no deterministic refusal mechanism.

### 2. Code Quality & Architecture (17/20)
- Haystack framework integration with ChromaDB and Gemini is well done.
- Clean pipeline: DocumentConverter → Cleaner → Splitter → Embedder → ChromaDB → Retriever → ChatPromptBuilder → Generator.
- **Issue:** `src/retrieval.py`, `src/generator.py`, `src/citation_formatter.py`, `src/validator.py` are orphaned — not used by the actual application. The real pipeline uses Haystack components directly. These should be removed or integrated.
- `MenuBuddySpike.py` contains hardcoded API key placeholders — bad practice even with placeholder values.
- Architecture diagram shows a 3-stage flow including fact-checking, but stage 3 is not implemented in the actual code.

### 3. Documentation & Deliverables (22/25)
- PRD.md — concise but adequate. ✓
- MVP_definition.md — present and clear. ✓
- Milestone_2_demo_script.md — detailed with questions and expected outcomes. ✓ (But describes aspirational behavior re: verification.)
- risk_log.md — present with risk table. ✓
- evaluation_test_cases.md — 20 test queries across 4 restaurants. ✓
- Sprint 1 Plan.md — very brief (15 lines), could be more detailed.
- **Issue:** File named `evaluation_test.cases.md` (period) vs required `evaluation_test_cases.md` (underscore).
- **Missing:** "Citation Coverage" metric in evaluation, which was explicitly required.
- .env.example present. ✓
- requirements.txt present. ✓

### 4. Evaluation Evidence (15/15)
- 20 test queries across Red Lobster, Pizza Hut, Starbucks, Olive Garden.
- Retrieval Accuracy: 95% (19/20).
- Grounding Accuracy: 100%.
- Hallucination Rate: 5% (1 instance — Herb-Grilled Salmon in query 19).
- Refusal Accuracy: 100%.
- Honest reporting of the one failure case is appreciated.

### 5. Repository Hygiene (14/15)
- `.gitignore`, `.env.example`, `requirements.txt` all present.
- README has setup/run instructions.
- Minor: file naming inconsistency, orphaned source modules, spike file with hardcoded keys.

---

## Individual Grades

| Team Member | Commits | Contribution Area | Grade |
|---|---|---|---|
| Jseo09 | 29 | Core code, spike refactoring, evaluation, MVP/demo docs | 95/100 |
| Demetrio Deanda (ddean09) | 20 | RAG/OCR framework, GUI (Flask app), README, architecture diagram | 92/100 |
| Ren | 17 | Evaluation test cases documentation (all 17 commits are test case docs — no code) | 82/100 |

**Note:** Ren contributed significantly to evaluation documentation but has zero code commits. The core engineering was done by Jseo09 and Demetrio Deanda. For the final sprint, Ren needs to take on coding tasks.

---

## Key Recommendations for Sprint 2
1. **Integrate validation into the running pipeline** — this is the single most important gap. Call `validator.py` from `main.py` and `app.py`.
2. Remove or integrate orphaned `src/` modules.
3. Add deterministic refusal mechanism beyond prompt-only grounding.
4. Add Citation Coverage metric to evaluation.
5. Fix evaluation file naming (`evaluation_test.cases.md` → `evaluation_test_cases.md`).
6. Clean up `MenuBuddySpike.py` hardcoded key references.
7. Ren needs to contribute code, not just documentation.
