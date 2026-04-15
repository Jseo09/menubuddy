# Sprint 2 Grade — Venture 1: MenuBuddy

**Graded:** April 15, 2026
**Sprint Window:** April 8 – April 14, 2026
**Final Demo:** April 29, 2026

---

## Overall Grade: 91/100

---

## Summary

MenuBuddy closed the single biggest gap from Milestone 2: the validator is now actually wired into the running application. Both `main.py` (CLI) and `app.py` (Flask) call `verify_answer_against_context()` after generation and surface a VERIFIED / FLAGGED status. A deterministic retrieval-confidence refusal (threshold 0.35) is in place before generation, citation coverage is computed per response, and the orphaned `src/retrieval.py`, `src/generator.py`, and `src/citation_formatter.py` modules were deleted. The `evaluation_test.cases.md` file name was corrected. Ren, who had zero code commits in Milestone 2, now has a measurable code contribution (Citation Coverage metric commit as RenSan888) plus substantial documentation work (error analysis, new restaurant test log, retrospective).

The grade is held below 95 by three things: the README was not updated (still references embedchain and the old stage labels), the Citation Coverage metric exists in code but was not added to the evaluation report's metrics table, and the Sprint 2 retrospective lists "Error handling improvements" and "Update README" as not completed. Those carry directly into Sprint 3.

---

## Category Breakdown

### 1. Task Completion (37/40)

**P0 — Critical (all four complete):**
- Validator integrated in `main.py`: YES. See `main.py` lines 127-142, calls `verify_answer_against_context` and prints status + details. (commit 506c122, Jseo09)
- Validator integrated in `app.py`: YES. See `app.py` lines 174-198, returns `status`, `details`, `verification` in the JSON response. (commit 506c122, Jseo09)
- Deterministic refusal mechanism: YES. `app.py` lines 100-133 enforce `CONFIDENCE_THRESHOLD = 0.35`. If no docs retrieved OR top score below threshold, returns FLAGGED immediately without calling Gemini. `main.py` lines 104-108 print a low-confidence warning but still generate (CLI is softer than web, acceptable but worth tightening).
- Validate demo script: PARTIAL. Demo script was touched (commits 21299c5, 8d8bdef) but it still references "Status = FLAGGED (IRRELEVANT)" which the code does not produce as a distinct category, and Step 5's expected refusal text doesn't match the actual refusal string in `app.py`. Minor mismatch, not blocking.

**P1 — Code Cleanup (all four complete):**
- Orphaned `src/` modules removed: YES. `src/retrieval.py`, `src/generator.py`, `src/citation_formatter.py` all deleted (commits 022a46c, 34e3310, 483cad4). `src/validator.py` kept because it is now the actual validator imported by both entry points.
- Hardcoded keys removed from spike: YES. `src/MenuBuddySpike.py` now uses `load_dotenv()` and `os.environ.get("GOOGLE_API_KEY")` only (commit 9977bf8, ddean09).
- Evaluation file naming fixed: YES. `evaluation_test.cases.md` renamed to `evaluation_test_cases.md` (commits f00383a, 7a8592c).
- Citation Coverage metric: PARTIAL. Implemented in code (`calculate_citation_coverage()` in both `app.py` lines 42-55 and `main.py` lines 18-24, returned in the JSON) and a commit "Add Citation Coverage metric to evaluation report" (53d499a) exists, but the actual `evaluation_test_cases.md` metrics table still lists only Retrieval / Grounding / Hallucination / Refusal. The metric is computed live but not reported.

**P2 — Strengthen Demo (3 of 4 complete):**
- Improve Flask UI: YES. `templates/index.html` was fully rewritten (commit 9977bf8, 225 lines touched) with visual indicators for verification status.
- Add more menu sources: YES. `docs/M2add_menu_documentation.md` documents Raising Cane's, Panda Express, and Church's Chicken with question/response/correctness tables and a model-selection error analysis (503 issue, fallback from gemini-3.1-flash-lite-preview through gemini-2.5-flash to gemini-2.5-flash-lite).
- Error handling improvements: NO. Retrospective explicitly leaves this blank. No try/except around `pipe.run()`, no retry logic, no structured handling of 503s beyond the note in the add-menu doc.
- Demo rehearsal script: Considered complete via the edits to `Milestone_2_demo_script.md`, though see note above about drift.

**P3 — Documentation & Polish (2 of 3 complete):**
- Update README: NO. `README.md` still references embedchain (removed from the actual stack), the old `[DETERMINISTIC STAGE: SCRAPING]` / `[GENERATIVE STAGE: LLM]` labels that the current `main.py` does not print, and Python 3.9 / OpenAI API prerequisites that are no longer accurate. This task was assigned to "Jacob" in Sprint 2 (instructor), which is a planning error on the original sprint plan. Treat as carried forward, owner to be reassigned.
- Update architecture diagram: YES. Old `MenuBuddy Architecture Diagram.png` removed, new `MenuBuddy M2 Architecture Diagram.png` added (commit 9977bf8).
- Sprint 2 retrospective doc: YES. `docs/M2_retrospective_doc.md` exists with P0-P3 completion table.

### 2. Code Quality (18/20)

- Validator integration is clean. Both entry points share the same pattern: retrieve, threshold check, generate, validate, return status + details.
- `CONFIDENCE_THRESHOLD` is duplicated between `main.py` and `app.py`. Minor, worth pulling into a shared constant.
- CLI behavior on low confidence only warns rather than refusing, so the deterministic refusal is not fully symmetric between CLI and web.
- `src/validator.py` uses `model="gemini-3.1-flash-lite-preview"` which the team itself documented as throwing 503 errors (see `M2add_menu_documentation.md`). The generator was switched to gemini-2.5-flash-lite but the validator still points at the broken model. This is a live bug.
- `src/MenuBuddySpike.py` still has the legacy `genai.configure(...)` and `genai.GenerativeModel(...)` patterns alongside the newer `google.genai.Client(...)` used in `app.py`. The spike is not on the hot path, so acceptable, but it is dead-ish code.

### 3. Documentation (13/15)

- `docs/M2_retrospective_doc.md`: present and accurate, though two cells use backtick placeholders instead of "No".
- `docs/M2add_menu_documentation.md`: strong. Tables of question / response / correctness for three new restaurants plus a model-selection failure analysis. Good evidence for P2.
- `docs/evaluation_test_cases.md`: now correctly named, but the Final Performance Metrics table does not include Citation Coverage. The commit message claims it was added, but in practice only the function was added in the Python code.
- `README.md`: not touched this sprint. Out of sync with the actual stack.
- Demo script: lightly edited, still describes a "FLAGGED (IRRELEVANT)" path the code does not produce.

### 4. Testing / Evaluation (12/15)

- No automated tests added this sprint.
- The three new restaurants were tested manually and documented. This is real evaluation work, just not automated.
- Citation Coverage is computed per query but never aggregated across the 20-query evaluation set. The metrics table in the evaluation report is unchanged from Milestone 2.
- No refresh of Retrieval / Grounding / Hallucination numbers against the current gemini-2.5-flash-lite generator. Milestone 2 metrics were produced on a different model.

### 5. Team Contribution (11/10 bonus territory, capped at 10)

Commits during Apr 8 – Apr 14 (team only, Zechun Cao excluded):

| Member | Commits | What |
|---|---|---|
| Ren (rensan961@gmail.com) | 15 | Citation Coverage metric, new-restaurant documentation, retrospective doc, demo error analysis |
| Jseo09 | 9 | Validator integration in main.py + app.py, deterministic refusal, orphaned module deletion, evaluation file rename, demo script edits |
| ddean09 (Demetrio) | 1 | Large sweep: spike key cleanup, Flask UI rewrite (225 lines in index.html), architecture diagram replacement |

Ren moved from zero code commits in Milestone 2 to a real code contribution (`calculate_citation_coverage` metric logic) plus leading the new-restaurant evaluation. This is exactly what the Sprint 2 plan asked for. Demetrio's single commit is large and touches multiple Sprint 2 P1/P2 items. Jseo09 did all the critical P0 engineering. Contribution is the most balanced it has been on this team so far.

Note: Ren's commits appear under two author names (Ren / RenSan888) but both map to the same email (rensan961@gmail.com). One developer, two git identities.

---

## Per-Task Completion Status

| Priority | Task | Owner (plan) | Status | Evidence |
|---|---|---|---|---|
| P0 | Integrate validator into main.py | Jseo09 | Done | main.py:127-142, commit 506c122 |
| P0 | Integrate validator into app.py | ddean09 (done by Jseo09) | Done | app.py:174-198, commit 506c122 |
| P0 | Deterministic refusal mechanism | Jseo09 | Done (web), Partial (CLI) | app.py:100-133 |
| P0 | Validate demo script accuracy | Ren | Partial | commits 21299c5, 8d8bdef; still has drift |
| P1 | Resolve orphaned src/ modules | Jseo09 | Done | commits 022a46c, 34e3310, 483cad4 |
| P1 | Remove hardcoded keys from spike | ddean09 | Done | commit 9977bf8 |
| P1 | Fix evaluation file naming | Ren | Done | commit 7a8592c |
| P1 | Add Citation Coverage metric | Ren | Partial | function in code (both entry points), metric not in evaluation_test_cases.md metrics table |
| P2 | Improve Flask UI | ddean09 | Done | templates/index.html, commit 9977bf8 |
| P2 | Add more menu sources | Ren | Done | M2add_menu_documentation.md (3 restaurants) |
| P2 | Error handling improvements | Jacob (instructor, misassigned) | Not done | no try/except around pipe.run, no retry on 503 |
| P2 | Demo rehearsal script | Jseo09 | Done | demo script updated |
| P3 | Update README | Jacob (instructor, misassigned) | Not done | README unchanged, still references embedchain |
| P3 | Update architecture diagram | ddean09 | Done | new PNG in commit 9977bf8 |
| P3 | Sprint 2 retrospective doc | Ren | Done | M2_retrospective_doc.md |

---

## Definition of Done (Sprint 2) Check

- [x] `validator.py` is called in both `main.py` and `app.py` pipelines
- [x] Verification status (VERIFIED/FLAGGED) is displayed in both CLI and web UI
- [x] Deterministic refusal mechanism works when retrieval confidence is low (web; CLI warns only)
- [x] No orphaned source modules remain (three deletions)
- [~] Demo script matches actual code behavior (minor drift on irrelevant-question path)
- [~] Citation Coverage metric added to evaluation (added to code, not to report)
- [x] Each team member has code commits this sprint

---

## Individual Grades (Red Flag Indicator Only)

Per the April 9 policy, these are red-flag signals, not verdicts. Every member receives the venture-level grade unless a contribution issue is formally raised.

| Member | Commits | Sprint 2 Work | Signal |
|---|---|---|---|
| Jseo09 | 9 | P0 validator integration, deterministic refusal, orphan cleanup | Strong |
| ddean09 (Demetrio) | 1 | Spike cleanup, Flask UI rewrite, architecture diagram, single large commit | OK, lower commit count but high-value changes |
| Ren | 15 | Citation coverage code, 3-restaurant eval, retrospective, demo analysis | Strong, big jump from M2 |

No red flags this sprint. Team contribution is noticeably more balanced.

---

## Key Recommendations for Sprint 3

1. Fix validator model ID: `src/validator.py` currently hardcodes `gemini-3.1-flash-lite-preview`, which the team's own error analysis says throws 503. Switch to gemini-2.5-flash-lite to match the generator.
2. Add Citation Coverage to the evaluation report's metrics table. Re-run the 20 queries and populate a real aggregate number.
3. Rewrite the README to match the actual stack (Haystack + ChromaDB + Google GenAI, no embedchain, no OpenAI dependency, Python 3.10+).
4. Add error handling around `pipe.run()` and retrieval: catch 503, retry once with backoff, fail gracefully.
5. Tighten CLI deterministic refusal to match the web path (actually refuse, not just warn).
6. Rehearse the demo end-to-end on the new Flask UI with URL ingestion, not just image ingestion.
