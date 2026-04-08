# Sprint 2 Plan — Venture 1: MenuBuddy

**Sprint Duration:** April 8 – April 14, 2026
**Sprint Goal:** Integrate validation into the running pipeline, clean up orphaned code, and strengthen the demo experience.
**Final Demo:** April 29, 2026

---

## Context

After Milestone 2, MenuBuddy has a working RAG pipeline with URL and image ingestion, ChromaDB storage, and Gemini-powered generation with citation prompting. The biggest gap is that **validation/fact-checking is not integrated** into the running application — `validator.py` exists but is never called. The demo script describes verification behavior the code doesn't produce. Sprint 2 closes this gap and prepares for a polished final demo.

---

## Sprint 2 Tasks

### P0 — Critical: Integrate Validation (Days 1–3)

| Task | Owner | Description |
|---|---|---|
| Integrate validator into main.py | Jseo09 | Import and call `validator.py` after answer generation. Display verification status (VERIFIED/FLAGGED) with details |
| Integrate validator into app.py | ddean09 | Add verification step to Flask `/ask_menu` endpoint. Show verification result in web UI |
| Deterministic refusal mechanism | Jseo09 | Add confidence threshold check beyond prompt-only grounding. If retrieval similarity score is below threshold, refuse instead of generating |
| Validate demo script accuracy | Ren | Run through `Milestone_2_demo_script.md` step-by-step and update to match actual code behavior |

### P1 — Code Cleanup (Days 2–4)

| Task | Owner | Description |
|---|---|---|
| Resolve orphaned src/ modules | Jseo09 | Either integrate `src/retrieval.py`, `src/generator.py`, `src/citation_formatter.py` into the Haystack pipeline or remove them |
| Remove hardcoded keys from spike | ddean09 | Clean up `MenuBuddySpike.py` — remove hardcoded API key lines |
| Fix evaluation file naming | Ren | Rename `evaluation_test.cases.md` → `evaluation_test_cases.md` |
| Add Citation Coverage metric | Ren | Add Citation Coverage metric to evaluation report as required by M2 spec |

### P2 — Strengthen Demo (Days 4–6)

| Task | Owner | Description |
|---|---|---|
| Improve Flask UI | ddean09 | Add visual indicators for verification status, citation highlights, and refusal styling |
| Add more menu sources | Ren | Test with 2+ additional restaurant menus and document results |
| Error handling improvements | Jacob | Add graceful handling for network failures, invalid URLs, unsupported image formats |
| Demo rehearsal script | Jseo09 | Create a reliable demo flow showing: ingest → query → cited answer → verification → refusal case |

### P3 — Documentation & Polish (Days 6–7)

| Task | Owner | Description |
|---|---|---|
| Update README | Jacob | Document both CLI and Flask UI usage, all dependencies, environment setup |
| Update architecture diagram | ddean09 | Ensure diagram matches actual implemented components (especially if orphaned modules are removed) |
| Sprint 2 retrospective doc | Ren | Document what was completed, what remains |

---

## Definition of Done (Sprint 2)

- [ ] `validator.py` is called in both `main.py` and `app.py` pipelines
- [ ] Verification status (VERIFIED/FLAGGED) is displayed in both CLI and web UI
- [ ] Deterministic refusal mechanism works when retrieval confidence is low
- [ ] No orphaned source modules remain
- [ ] Demo script matches actual code behavior
- [ ] Citation Coverage metric added to evaluation
- [ ] Each team member has code commits this sprint

---

## Contribution Expectations

Currently, Jseo09 (29 commits) and Demetrio (20 commits) did all the core engineering. **Ren** (17 commits, all evaluation docs) and **Jacob** (3 commits, all milestone docs) need to contribute code this sprint. Tasks have been assigned accordingly — Ren takes evaluation and demo validation, Jacob takes error handling and documentation with real code changes.

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 2 (this sprint) | Apr 8–14 | Validation integration, code cleanup, demo strengthening |
| Sprint 3 | Apr 15–21 | UI polish, edge cases, additional menu testing |
| Sprint 4 | Apr 22–28 | Final integration, presentation prep, final deliverables |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |
