# Sprint 3 Grade, Venture 1: MenuBuddy

**Graded:** April 28, 2026
**Sprint Window:** April 15 – April 24, 2026 (extended from April 21)
**Final Demo:** April 29, 2026
**Final Deliverables Due:** May 3, 2026

---

## Overall Grade: 94/100

**Note on individual grades:** This is the venture-level grade. Members who severely under-contributed during Sprint 3 may receive a reduced individual grade applied separately.

**Note on grading scope:** Final-presentation prep items (rehearsal logs, slide deck drafts, pitch deck refreshes, backup recordings) are not counted against the Sprint 3 grade. They appear in the "Items to Complete by May 3" section instead.

---

## Summary

Sprint 3 closed every Sprint 2 carryover and the live validator bug surfaced during Milestone 2 grading. The validator now runs on `gemini-2.5-flash-lite` (matching the generator), `safe_run` wraps both `pipe.run()` and `retriever.run()` in `app.py` and `main.py` with retry-once-on-503 behavior, and a new `question_filter.py` adds a lightweight irrelevant-question prefilter that complements the retrieval-confidence threshold. `CONFIDENCE_THRESHOLD` was pulled into `src/config.py` so CLI and web read from one source. Citation Coverage is now in the evaluation report's Final Performance Metrics table at 99.5%, computed against the current model. The README has been rewritten to reflect Haystack + ChromaDB + Google GenAI, the demo script is renamed `Final_demo_script.md` and aligned with real code behavior, and a Sprint 3 retrospective is in `docs/`.

Contribution is healthy across all three members. Ren's 12 in-window commits (Apr 22-24) deliver every task assigned to Ren in the plan: Citation Coverage in the eval table, performance metrics refresh, demo script rename and content, multi-menu prompt scoping, irrelevant-query response refinement, retrospective. Jseo09 owned the validator model fix, question filter, and shared config. Demetrio shipped the `safe_run` error handling sweep across both entry points.

The grade sits at 94 rather than higher because some items landed in the back half of the window rather than spread across days 1-5 (Ren's burst is concentrated Apr 22-24), and the P2 source-label display cleanup is not visible in the diff. None are demo blockers.

---

## Category Breakdown

### 1. Task Completion (39/40)

**P0 (4 of 4 complete):**
- Validator model fix: `src/validator.py` line 33 now uses `gemini-2.5-flash-lite`. Fixed.
- CLI deterministic refusal tightened: refusal is now consistent between the CLI and web paths.
- Error handling around `pipe.run()` and `retriever.run()`: `safe_run` wrapper in both `main.py` and `app.py` catches exceptions, retries once, and returns a clean error response.
- Citation Coverage in evaluation report: added to the Final Performance Metrics table at 99.5% (target was 95%+).

**P1 (3 of 4 complete, 1 partial):**
- README rewrite: shipped. Haystack + ChromaDB + Google GenAI, Python 3.10+, no embedchain, no OpenAI prerequisite. Both CLI and web run instructions present.
- Demo script aligned with real code: shipped. Renamed `Milestone_2_demo_script.md` → `Final_demo_script.md`. Step 5/6 outputs match what the code actually returns.
- Evaluation metrics refreshed on current model: shipped. Performance metrics table updated.
- `CONFIDENCE_THRESHOLD` extracted to shared config: shipped. `src/config.py` is now the single source.

**P2 (3 of 4 complete):**
- Irrelevant question classifier: shipped as `src/question_filter.py`.
- Multi-menu disambiguation: prompt template updated to scope answers to the restaurant implied by the question.
- Per-query Citation Coverage column in eval matrix: shipped.
- Source-label display cleanup (strip `uploads/` prefix in web UI): not visible in the diff. Carries to May 3.

**P3 (1 of 1 graded; rehearsal log and slide deck deferred to final-prep):**
- Sprint 3 retrospective doc: shipped (`docs/Sprint3_retrospective_doc.md`).
- End-to-end demo rehearsal #1: deferred to final-prep (May 3 deliverables).
- Slide deck draft: deferred to final-prep (May 3 deliverables).

### 2. Code Quality (18/20)

- `safe_run` wrapper is a clean abstraction. Both `app.py` and `main.py` use it consistently.
- Shared config in `src/config.py` removes the previous duplication. Good.
- `question_filter.py` is a new module with a clear single responsibility.
- Validator model ID is now correct, but `MenuBuddySpike.py` still uses the older `genai.configure(...)` pattern. Spike is off the hot path, so acceptable.

### 3. Documentation (14/15)

- README is now accurate to the running stack.
- `Final_demo_script.md` matches code behavior.
- `Sprint3_retrospective_doc.md` documents what shipped.
- Evaluation report has Citation Coverage in both the metrics table and the per-query matrix.

### 4. Testing / Evaluation (13/15)

- Evaluation rerun against `gemini-2.5-flash-lite` is recorded.
- Citation Coverage at 99.5% on the current model is a solid number.
- No automated unit tests added this sprint (consistent with prior sprints; not required by plan).

### 5. Team Contribution (10/10)

| Member | In-window Commits | Sprint 3 Work | Signal |
|---|---|---|---|
| Jseo09 | 7 | Validator model fix, question_filter, shared config | Strong |
| Demetrio Deanda / ddean09 | 3 | `safe_run` wrapper across both entry points, README touchups | Strong |
| Ren | 12 | Citation Coverage in eval table, eval rerun on current model, demo script rename + alignment, multi-menu prompt fix, irrelevant-query response, Sprint 3 retrospective | Strong (concentrated Apr 22-24) |

All three members have meaningful contributions. Ren's work is real and substantial; the timing concentrated late but every assigned task landed.

---

## Per-Task Completion Status

| Priority | Task | Owner | Status |
|---|---|---|---|
| P0 | Fix validator model ID | Jseo09 | Done |
| P0 | Tighten CLI deterministic refusal | Jseo09 | Done |
| P0 | Error handling around `pipe.run()` | ddean09 | Done |
| P0 | Citation Coverage in evaluation report | Ren | Done |
| P1 | Rewrite README | ddean09 | Done |
| P1 | Align demo script with real code | Ren | Done |
| P1 | Refresh evaluation metrics on current model | Ren | Done |
| P1 | Extract CONFIDENCE_THRESHOLD to shared config | Jseo09 | Done |
| P2 | Irrelevant question classifier | Jseo09 | Done (`question_filter.py`) |
| P2 | Source-label display cleanup | ddean09 | Not done |
| P2 | Multi-menu disambiguation | Ren | Done (prompt scoping) |
| P2 | Per-query Citation Coverage column | Ren | Done |
| P3 | End-to-end demo rehearsal #1 | All | Deferred to final-prep |
| P3 | Sprint 3 retrospective | Ren | Done |
| P3 | Presentation slides draft | ddean09 | Deferred to final-prep |

---

## Definition of Done (Sprint 3) Check

- [x] Validator model ID fixed and at least 5 test queries return real VERIFIED verdicts
- [x] CLI and web both refuse deterministically on low retrieval score
- [x] `pipe.run()` and `retriever.run()` wrapped in try/except with retry-once on 503
- [x] `evaluation_test_cases.md` includes Citation Coverage in metrics table and per-query matrix
- [x] README reflects actual current stack
- [x] Demo script matches real code behavior
- [~] At least one full timed rehearsal completed on a clean DB (deferred to final-prep)
- [~] Presentation slides exist in draft form (deferred to final-prep)

---

## Items to Complete by May 3 (Final Deliverables)

The May 3 package is required to be under `docs/Final_Demo/` in the repo. Save the following items there:

1. **Final demo slides** (PDF or PPTX). Cover: problem, stack and architecture, key features (validator + deterministic refusal + question filter + citations), eval numbers, live-demo plan. Not yet in repo.
2. **Runbook**. A single Markdown file under `docs/Final_Demo/Runbook.md` with: prerequisites, env setup (`GEMINI_API_KEY`), how to run CLI (`python main.py`), how to run web (`python app.py` then visit `http://127.0.0.1:5001`), how to ingest a URL menu, how to ingest an image menu, what VERIFIED / FLAGGED mean, common errors and recovery.
3. **Final demo video**. Recorded screen capture of the working flow as a backup if live demo fails. Save under `docs/Final_Demo/Final_Demo_Video.mp4` (or link from `Final_Demo_Video.md` if hosted on Drive).
4. **Final code on `main`**. Confirm `main` reflects the demo state after Apr 29. No half-merged branches.

Smaller carryovers worth closing the same window:

5. **Source-label display cleanup** in web UI: strip `uploads/` prefix and show `"<restaurant> (image)"` instead of raw paths. Small frontend tweak in `templates/index.html` and the source-mapping code in `app.py`.
6. **Rehearsal log**. After the Apr 29 demo, write a short post-demo notes file at `docs/Final_Demo/post_demo_notes.md` capturing what worked and what would change for next time. Useful for the final deliverables narrative.
