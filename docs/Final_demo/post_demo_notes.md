
## Summary
The MenuBuddy system successfully demonstrated a complete end-to-end RAG pipeline, including menu ingestion, retrieval, grounded answer generation with citations, and both pre-generation and post-generation safety mechanisms. The system showed strong performance in handling irrelevant queries and provided explainable, citation-supported answers for valid questions.

---

## Demo Observations

| Category | Observation |
|---------|------------|
| Pipeline Functionality | End-to-end flow (ingestion → retrieval → generation → validation) worked as expected |
| Irrelevant Question Handling | Correctly refused out-of-scope queries (e.g., “Who is the CEO?”) before retrieval |
| Explainability | Answers included citations, improving transparency and trust |
| Retrieval Behavior | Retrieved data from multiple restaurant menus in some cases |
| Validation Results | Some valid questions were flagged due to noisy or mixed context |
| UI Output | Source labels were not fully cleaned, reducing clarity |

---

## Issues Identified

| Issue | Impact |
|------|--------|
| Multi-menu retrieval | Introduced noise in context and reduced grounding accuracy |
| Overly strict validation | Caused false negatives on valid menu-related queries |
| Unrefined source labels | Made output less clear and less user-friendly |

---

## Improvements for Next Iteration

| Area | Improvement |
|------|------------|
| Retrieval | Limit to a single menu source per session to improve relevance |
| Source Display | Clean and standardize source labels for better readability |
| Validation | Tune validator to reduce false negatives while maintaining safety |
| Overall Consistency | Improve alignment between retrieval, generation, and validation |

---

## Conclusion
The MenuBuddy system demonstrated a robust RAG pipeline from scratch to finish, including menu ingestion, menu retrieval, grounded answer generation with citations, pre-generation safety measures, and post-generation measures. In particular, the MenuBuddy system excelled at answering irrelevant questions (for example, “Who is the CEO?”) with an early refusal and was quite explainable through answer generation that provided citations for support. Nevertheless, during the demo, some valid menu-related questions were marked up since the retrieval module retrieved information about multiple restaurants’ menus, causing noise in context that negatively impacted grounding certainty. Moreover, the source labeling in the interface was not fully cleaned, resulting in unappealing outputs for end users. As possible improvements, we would limit retrieval to one menu source per session and improve our source labeling practices to provide more accurate labels. We would also fine-tune the validator to lower false negatives on valid answers.
