import re

IRRELEVANT_PATTERNS = [
    r"\bceo\b",
    r"\bfounder\b",
    r"\bheadquarters\b",
    r"\bstock\b",
    r"\bshare price\b",
    r"\bmarket cap\b",
    r"\brevenue\b",
    r"\bnet worth\b",
    r"\bcorporate\b",
    r"\bhistory of the company\b",
]

def is_irrelevant_question(question: str) -> bool:
    q = (question or "").strip().lower()
    return any(re.search(pattern, q, re.I) for pattern in IRRELEVANT_PATTERNS)
