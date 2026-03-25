# Milestone 2 Deliverables
## Team: MenuBuddy
### Due: April 5, 2026
### Focus: MVP of a Reliable, Grounded Menu Assistant

---

## Context

Milestone 1 established the project direction: a menu ingestion and question-answering pipeline with citation and validation goals.

Sprint 1 asked the team to narrow the MVP and add a minimal demo experience. Milestone 2 is where that work must become concrete. This checkpoint is the MVP review.

Milestone 2 is not about adding broad new scope. It is about demonstrating one narrow, stable, honest product slice that works end-to-end.

---

# Milestone 2 Objective

By Milestone 2, your team must demonstrate:

- One clearly defined MVP workflow
- Reliable ingestion for the chosen workflow
- Grounded answer generation with visible citations
- Validation that meaningfully checks the answer against retrieved data
- Correct refusal behavior when information is unsupported
- A usable demo experience that another person can run
- Clear documentation of scope, quality, and known limitations

---

# 1. Required MVP Scope

You must choose and fully support at least one primary workflow:

- URL -> scrape menu -> ask menu questions -> receive cited answer
- Image -> OCR menu -> ask menu questions -> receive cited answer

You may support both only if both are stable. If one path is fragile, declare one official MVP path and treat the other as stretch work.

## The MVP must support:

- Menu ingestion from the chosen input path
- Storage of menu entries in a structured form
- Retrieval of relevant menu entries for a user question
- Grounded answer generation using retrieved context
- Refusal when the answer is unsupported
- Visible citations in the final answer
- A demoable interaction layer

The interaction layer may be:

- A minimal web UI
- A Streamlit app
- A clean terminal experience with repeatable commands

If you choose CLI only, it must be clear and reproducible enough for another person to run without hidden setup or verbal coaching.

---

# 2. MVP Quality Bar

Your MVP is complete only if all of the following are true:

- The workflow runs end-to-end during demo without manual patching
- The supported input path works on at least two real menu sources or two representative test menus
- Every factual answer displays citations
- Unsupported answers are refused instead of guessed
- At least one validation mechanism checks the final answer against retrieved data
- The README is sufficient for another team to run the system

---

# 3. Required Deliverables

Create or update the following:

- `/docs/MVP_definition.md`
- `/docs/Milestone_2_demo_script.md`
- `/docs/evaluation_test_cases.md`
- `/docs/risk_log.md`
- `/README.md`

Your repository must also include:

- The working application code
- `requirements.txt`
- `.env.example`
- A clearly identified launch command

---

# 4. MVP Definition Document

Create:

`/docs/MVP_definition.md`

This file must include:

- The exact MVP workflow selected
- What a user can do in the MVP
- What is explicitly out of scope for Milestone 2
- Supported menu source types
- Known limitations
- Definition of done for the MVP

Example:

> Users can provide a supported restaurant menu URL, ask questions about menu items and prices, and receive either a cited grounded answer or a refusal if the information is not supported by the menu data.

---

# 5. Demo Script

Create:

`/docs/Milestone_2_demo_script.md`

This file must include:

- Setup commands
- Run commands
- The exact menu URLs or test inputs to use
- At least 5 demo questions
- At least 1 refusal-case question
- The expected outcome for each question

The goal is reproducibility. Another person should be able to follow the script and obtain the intended demo.

---

# 6. Evaluation Update

Update:

`/docs/evaluation_test_cases.md`

Requirements:

- At least 20 test queries
- Only count queries against the officially supported MVP workflow
- Fix any metric inconsistencies from Milestone 1
- Include a short explanation of how each metric is computed

Required metrics:

- Retrieval accuracy
- Citation coverage
- Grounding accuracy
- Hallucination rate
- Refusal accuracy

If there are failures, report them clearly and explain them honestly.

---

# 7. Validation Requirement

Your validation layer must be stronger than prompt-only grounding.

Acceptable approaches include:

- Rule-based verification that all mentioned menu items are present in retrieved results
- Field-level validation against structured menu records
- Constrained generation followed by deterministic checking

If you continue using an LLM judge, you must justify why it is adequate and pair it with at least one deterministic check.

---

# 8. Demo Experience Requirement

You must provide a usable demo interaction.

At minimum:

- The evaluator can load a menu
- The evaluator can ask a question
- The evaluator can see the retrieved support
- The evaluator can see the cited answer
- The evaluator can see the refusal path

For Milestone 2, usability matters more than visual polish.

---

# 9. Repository Requirements

By Milestone 2, the repository must include:

- A corrected and complete README
- `.env.example`
- Consistent file names referenced by deliverable docs
- Clear labeling of prototype-only files
- No hard-coded secrets
- Evidence of team contributions in commit history

If a required artifact lives outside the repo, link it from the repo.

---

# Required Live Demo Video for Milestone 2

You must demonstrate:

1. Launching the MVP from a clean starting point
2. Ingesting a supported menu input
3. Displaying or logging the stored structured data
4. Showing retrieved supporting context for a question
5. Producing a cited answer
6. Showing the validation step
7. Showing at least one correct refusal case
8. Explaining one known limitation honestly

If the demo only works with instructor help, the MVP is incomplete.

---

# Milestone 2 Standard

Your project must evolve from:

“We have components that mostly work.”

To:

“We have a narrow but credible MVP that another person can run, test, and trust within its stated scope.”
