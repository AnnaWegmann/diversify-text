"""Surface patterns of a style: punctuation, capitals, emoji, word and sentence length.

The counts are taken over all example texts of a style together, so that
short texts still add up to a usable profile.
"""

import re
from collections import Counter

WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
TOKEN = re.compile(r"\S+")
SENTENCE_END = re.compile(r"[.!?]+(?=\s|$)|\n+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
PUNCTUATION = {
    "period": ".", "comma": ",", "exclamation": "!", "question": "?",
    "apostrophe": "'’", "quote": "\"“”", "colon": ":", "semicolon": ";",
    "dash": "-–—", "parenthesis": "()", "slash": "/", "asterisk": "*",
}
PATTERNS = {
    "hashtags": r"#\w", "mentions": r"@\w", "urls": r"https?://|www\.",
    "stretched_letters": r"([A-Za-z])\1\1", "ellipses": r"\.\.\.|…",
    "repeated_punctuation": r"[!?]{2,}", "space_before_punctuation": r" [.,!?;:]",
}


def surface_profile(texts: list[str]) -> dict[str, float]:
    """Rates of surface features over all ``texts`` of one style."""
    c = Counter()
    for text in texts:
        words = WORD.findall(text)
        letters = [ch for ch in text if ch.isalpha()]
        c["chars"] += len(text)
        c["letters"] += len(letters)
        c["tokens"] += len(TOKEN.findall(text))
        c["words"] += len(words)
        c["sentences"] += max(1, len(SENTENCE_END.findall(text.strip())))
        c["word_letters"] += sum(len(w) for w in words)
        c["uppercase"] += sum(ch.isupper() for ch in letters)
        c["allcaps_words"] += sum(len(w) > 1 and w.isupper() for w in words)
        c["lowercase_i"] += sum(w == "i" for w in words)
        c["digits"] += sum(ch.isdigit() for ch in text)
        c["non_ascii"] += sum(ord(ch) > 127 and not EMOJI.match(ch) for ch in text)
        c["emoji"] += len(EMOJI.findall(text))
        c["newlines"] += text.count("\n")
        for name, pattern in PATTERNS.items():
            c[name] += len(re.findall(pattern, text))
        for name, chars in PUNCTUATION.items():
            c["punctuation_" + name] += sum(text.count(ch) for ch in chars)

    chars, words, tokens = max(c["chars"], 1), max(c["words"], 1), max(c["tokens"], 1)
    profile = {
        "mean_word_length": c["word_letters"] / words,
        "words_per_sentence": words / c["sentences"],
        "uppercase_letters": c["uppercase"] / max(c["letters"], 1),
        "allcaps_words": c["allcaps_words"] / words,
        "lowercase_i": c["lowercase_i"] / words,
        "digits": c["digits"] / chars,
        "non_ascii": c["non_ascii"] / chars,
        "emoji": c["emoji"] / tokens,
        "newlines": c["newlines"] / tokens,
        "tokens_that_are_not_words": 1 - min(words / tokens, 1),
    }
    for name in list(PATTERNS) + ["punctuation_" + p for p in PUNCTUATION]:
        profile[name] = c[name] / tokens
    return profile
