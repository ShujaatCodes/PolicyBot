import re

REFUSAL_MESSAGE = "I can only answer questions about company policy documents."

_MAX_LENGTH = 500

_SQL_PATTERNS = [
    r"\bdrop\b",
    r"\bdelete\b",
    r"\binsert\b",
    r"\bupdate\b",
    r"\bselect\b",
    r"\bunion\b",
    r"--",
    r";--",
    r"\bor\s+1\s*=\s*1\b",
    r"1\s*=\s*1",
    r"\bxp_",
]

_INJECTION_PATTERNS = [
    r"ignore\s+previous",
    r"ignore\s+above",
    r"you\s+are\s+now",
    r"forget\s+your",
    r"new\s+persona",
    r"jailbreak",
    r"act\s+as",
    r"pretend\s+you",
    r"\bdisregard\b",
    r"override\s+instructions",
]

_SCRIPT_PATTERNS = [
    r"<script",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*=",
]

_ALL_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in _SQL_PATTERNS + _INJECTION_PATTERNS + _SCRIPT_PATTERNS
]


def is_blocked(question: str) -> tuple[bool, str]:
    if len(question) > _MAX_LENGTH:
        return True, REFUSAL_MESSAGE
    for pattern in _ALL_PATTERNS:
        if pattern.search(question):
            return True, REFUSAL_MESSAGE
    return False, ""
