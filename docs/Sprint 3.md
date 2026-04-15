# Sprint 3 Plan — Venture 1: MenuBuddy

**Sprint Duration:** April 15 – April 21, 2026
**Sprint Goal:** Fix the validator model bug, finish the Citation Coverage reporting, bring the README and error handling up to final-demo quality, and start rehearsing the full April 29 demo flow.
**Final Demo:** April 29, 2026

---

## Context

Sprint 2 closed the big Milestone 2 gap: the validator now runs inside both `main.py` and `app.py`, deterministic refusal is live on the web path, orphaned `src/` modules are gone, and Ren shipped real code (Citation Coverage function) plus three new-restaurant evaluation tables. Sprint 2 grade was 91/100.

Three Sprint 2 items carry into Sprint 3:
1. Error handling around `pipe.run()` (P2, not done).
2. README refresh to match the actual Haystack + ChromaDB + Google GenAI stack (P3, not done, originally misassigned to "Jacob").
3. Citation Coverage aggregate metric in `evaluation_test_cases.md` (P1, function added but evaluation report's metrics table was not updated).

Plus a live bug surfaced during grading: `src/validator.py` hardcodes `model="gemini-3.1-flash-lite-preview"`, which the team's own `M2add_menu_documentation.md` says throws 503 UNAVAILABLE. The generator was switched to `gemini-2.5-flash-lite` but the validator was not. This needs to be fixed on day 1 or the validator will silently default to UNSUPPORTED on every query during the demo.

With two sprints left before the final demo, Sprint 3 is the last sprint where the team can land new features and fixes safely. Sprint 4 (Apr 22-28) should be pure polish and rehearsal.

---

## Sprint 3 Tasks

### P0 — Critical Fixes & Final Demo Blockers (Days 1–2)

| Task | Owner | Description |
|---|---|---|
| Fix validator model ID | Jseo09 | Change `src/validator.py` line 18 from `gemini-3.1-flash-lite-preview` to `gemini-2.5-flash-lite` (match the generator). Verify that VERIFIED verdicts come back cleanly on at least 5 real queries. |
| Tighten CLI deterministic refusal | Jseo09 | `main.py` lines 104-108 currently only print a warning when `top_score < 0.35`. Make CLI return a refusal message and skip generation, matching the web path in `app.py` lines 120-133. |
| Add error handling around pipe.run | ddean09 | Wrap `pipe.run(...)` in both `app.py` and `main.py` with try/except. On 503 UNAVAILABLE or network error, retry once with a 2-second backoff, then return a user-friendly error + FLAGGED status. Include the same for `retriever.run()`. |
| Citation Coverage in evaluation report | Ren | Re-run the 20 evaluation queries with the current gemini-2.5-flash-lite generator, compute the Citation Coverage per query and an aggregate, and add a `Citation Coverage` row to the Final Performance Metrics table in `docs/evaluation_test_cases.md`. Target: >= 95%. |

### P1 — Documentation & Demo Readiness (Days 2–4)

| Task | Owner | Description |
|---|---|---|
| Rewrite README | ddean09 | Update `README.md` to remove embedchain references, drop the OpenAI API prerequisite, update Python to 3.10+, list actual dependencies from `requirements.txt`, and document both CLI (`python main.py`) and web (`python app.py` → http://127.0.0.1:5001) usage. Add a short "Verification & Refusal" section explaining VERIFIED / FLAGGED and the 0.35 threshold. |
| Align demo script with real code | Ren | `Milestone_2_demo_script.md` Step 6 references a "FLAGGED (IRRELEVANT)" status the code does not produce. Replace with the real refusal flow (deterministic refusal when retrieval score is low). Update Step 5 expected output to match the exact string in `app.py` line 109. Rename the script to `Final_Demo_Script.md` or add a `Final_Demo_Script.md` for Apr 29. |
| Refresh evaluation metrics on current model | Ren | The Milestone 2 metrics (95% retrieval, 100% grounding, 5% hallucination) were produced on an older model config. Re-run the 20-query matrix against gemini-2.5-flash-lite and record new numbers next to the old ones in the evaluation report. |
| Extract CONFIDENCE_THRESHOLD to shared config | Jseo09 | Currently duplicated in `main.py` line 105 and `app.py` line 101. Pull into a single module-level constant in `src/` and import in both. Prevents drift. |

### P2 — Polish & Robustness (Days 4–5)

| Task | Owner | Description |
|---|---|---|
| Add an "irrelevant question" classifier step | Jseo09 | The demo script promises handling of questions like "Who is the CEO of Wendy's?" but the current pipeline only refuses on low retrieval score. Add a lightweight prefilter (keyword heuristic or a zero-shot Gemini call) that rejects out-of-scope questions before retrieval runs. |
| Improve source-label display | ddean09 | In the web UI, strip `uploads/` prefix from image sources and show a cleaner label (e.g., "Wendy's (image)"). The model-side rule in `app.py` prompt already asks for this but source mapping still shows raw paths. |
| Multi-menu disambiguation | Ren | `M2add_menu_documentation.md` notes that with multiple menus stored, the model sometimes mixes restaurants. Add a short note in the prompt template telling the model to scope answers to the restaurant implied by the question when possible. Document any improvement. |
| Evaluation report: add per-query Citation Coverage | Ren | Extend the 20-query matrix with a new "Citation Coverage" column (value from `calculate_citation_coverage()`). |

### P3 — Final Demo Prep (Days 5–7)

| Task | Owner | Description |
|---|---|---|
| End-to-end demo rehearsal #1 | Full team | Run the full Apr 29 demo flow on a clean ChromaDB: URL ingest → image ingest → 3 supported questions → 1 refusal case → 1 irrelevant question. Time it. Target: under 4 minutes. Record any bugs in `docs/demo_rehearsal_log.md`. |
| Sprint 3 retrospective doc | Ren | Document what was completed, what remains for Sprint 4. |
| Prepare presentation slides (draft) | ddean09 | Start the final-demo slides: problem, stack, architecture diagram, key features (validator + deterministic refusal + citations), eval numbers, live-demo plan. Draft only, polish in Sprint 4. |

---

## Definition of Done (Sprint 3)

- [ ] Validator model ID fixed and at least 5 test queries return a real VERIFIED verdict
- [ ] CLI and web both refuse deterministically on low retrieval score
- [ ] `pipe.run()` and `retriever.run()` are wrapped in try/except with retry-once on 503
- [ ] `evaluation_test_cases.md` includes Citation Coverage in both the metrics table and the per-query matrix, re-computed on gemini-2.5-flash-lite
- [ ] README reflects the actual current stack; a new user following it can run `python app.py` successfully
- [ ] Demo script matches the real code behavior for every step
- [ ] At least one full timed rehearsal has been completed on a clean DB
- [ ] Presentation slides exist in draft form

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 2 (done) | Apr 8–14 | Validation integration, cleanup, new menu sources (Grade: 91) |
| Sprint 3 (this sprint) | Apr 15–21 | Bug fixes, CitationCoverage in report, README, demo rehearsal #1 |
| Sprint 4 | Apr 22–28 | Final polish, 2-3 more timed rehearsals, slide polish, backup plans |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |

---

## Risk Notes

- **Gemini API instability.** Sprint 2 already surfaced 503 errors on gemini-3.1-flash-lite-preview. The retry/backoff work in P0 is not optional. Plan the demo so a 10-second API hiccup does not look like a system failure.
- **Multi-menu contamination.** When several restaurants are in ChromaDB, questions sometimes pull from the wrong menu. P2 item addresses this, but if it does not fully solve the issue, plan the demo to reset the DB between restaurants.
- **README drift is visible.** External graders and teammates will read `README.md` first. Leaving embedchain and OpenAI listed as prerequisites misrepresents the system.
- **Ren's code contribution momentum.** Ren landed real code in Sprint 2 (citation coverage function). Sprint 3 keeps Ren on evaluation and docs, which is the natural fit. No red flags.

---

## Final Demo Day Heads-Up (April 29)

Two weeks out. Rehearse toward this format during Sprint 3 and Sprint 4.

**12 minutes per team, hard cap.** I will cut you off at 12:00 to keep all 8 teams on schedule, so rehearse to 10:30 or 11:00 to leave margin. Suggested split:

1. **About 3 min: overall design.** What the product does, the core pipeline, and the architectural decisions that matter (retrieval strategy, validator or grounding approach, refusal policy). No code walkthroughs.
2. **About 4 min: individual contributions.** Every team member speaks briefly about what they personally owned this semester. Plan what you will say, roughly 45 to 60 seconds each.
3. **About 4 min: live demo of the highlights.** Pick 2 or 3 scenarios from your existing demo script. Required: at least one refusal or failure case and at least one end-to-end grounded answer. Do not spend this time on UI polish.
4. **About 1 min: Q&A**, included in the 12 minutes.

**Running order** is Venture 1 through Venture 8 in order, so MenuBuddy presents first.

**Backup plan:** have a prerecorded screen capture of the working path ready in case the live demo fails. Internet or API hiccups are not an excuse on demo day.

**Slides and runbook:** not due before the presentation, but both are required artifacts in the final deliverables package due May 3. Save them under `docs/Final_Demo/` in your repo.

**Avoid:** narrating code, reading slides verbatim, skipping the refusal case, opening with missing features. Present the version you are proud of.

Rehearse the full 12 minutes end to end at least twice, at least once with a timer.
