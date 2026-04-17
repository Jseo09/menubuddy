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
    r"\bvip\b",
    r"\bowner\b",
    r"\bpresident\b",
    r"\bmanager\b",
    r"\bwho bought\b",
    r"\bwho owns\b",
    r"\bwho runs\b",
    r"\bwho is current\b",
    r"\bmost burgers sold\b",
    r"\bbest selling\b",
    r"\bmost popular customer\b",
]

def is_irrelevant_question(question: str) -> bool:
    q = (question or "").strip().lower()
    return any(re.search(pattern, q, re.I) for pattern in IRRELEVANT_PATTERNS)
