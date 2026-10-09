import re
from collections import Counter


# --------------------------------------------------
# COMMON RESUME BUZZWORDS
# --------------------------------------------------

BUZZWORDS = [
    "hardworking",
    "passionate",
    "motivated",
    "team player",
    "results-driven",
    "results oriented",
    "responsible",
    "innovative",
    "fast learner",
    "detail-oriented",
    "self-motivated",
    "dynamic",
    "dedicated",
    "excellent communication",
    "go-getter",
    "proactive"
]


# --------------------------------------------------
# ACTION VERBS
# --------------------------------------------------

ACTION_VERBS = [
    "developed",
    "built",
    "implemented",
    "designed",
    "created",
    "engineered",
    "optimized",
    "automated",
    "integrated",
    "deployed",
    "configured",
    "tested",
    "analyzed",
    "improved",
    "managed",
    "led",
    "delivered",
    "maintained",
    "architected"
]


# --------------------------------------------------
# WEAK RESUME PHRASES
# --------------------------------------------------

WEAK_PHRASES = [
    "worked on",
    "responsible for",
    "helped with",
    "worked with",
    "was involved in",
    "assisted with",
    "participated in"
]


# --------------------------------------------------
# BUZZWORD DETECTOR
# --------------------------------------------------

def detect_buzzwords(text):
    """
    Detect common resume buzzwords.
    """

    text_lower = text.lower()

    found = []

    for buzzword in BUZZWORDS:

        if buzzword in text_lower:
            found.append(buzzword)

    return found


# --------------------------------------------------
# ACTION VERB ANALYZER
# --------------------------------------------------

def detect_action_verbs(text):
    """
    Detect strong action verbs used in the resume.
    """

    text_lower = text.lower()

    found = []

    for verb in ACTION_VERBS:

        pattern = rf"\b{re.escape(verb)}\b"

        if re.search(pattern, text_lower):
            found.append(verb)

    return found


# --------------------------------------------------
# WEAK PHRASE DETECTOR
# --------------------------------------------------

def detect_weak_phrases(text):
    """
    Detect weak or passive resume phrases.
    """

    text_lower = text.lower()

    found = []

    for phrase in WEAK_PHRASES:

        if phrase in text_lower:
            found.append(phrase)

    return found


# --------------------------------------------------
# REPEATED WORD ANALYZER
# --------------------------------------------------

def detect_repeated_words(text, min_length=4):
    """
    Find frequently repeated words.

    Common English stop words are excluded.
    """

    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "your",
        "have",
        "will",
        "using",
        "into",
        "were",
        "been",
        "they",
        "their",
        "about",
        "which",
        "there",
        "where",
        "when",
        "what",
        "then",
        "than",
        "also",
        "more",
        "such",
        "over",
        "under"
    }

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )

    filtered_words = [
        word
        for word in words
        if len(word) >= min_length
        and word not in stop_words
    ]

    word_counts = Counter(filtered_words)

    repeated = {
        word: count
        for word, count in word_counts.items()
        if count >= 4
    }

    return dict(
        sorted(
            repeated.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )


# --------------------------------------------------
# METRICS DETECTOR
# --------------------------------------------------

def detect_metrics(text):
    """
    Detect measurable information such as:
    percentages, numbers, counts, time periods, etc.
    """

    patterns = [
        r"\b\d+%",
        r"\b\d+\+",
        r"\b\d+\s*(?:users|projects|apis|products|modules|years|months|days)\b",
        r"\b\d+\.\d+\b",
        r"\b\d+\b"
    ]

    metrics = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        metrics.extend(matches)

    return list(dict.fromkeys(metrics))