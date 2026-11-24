"""Function-word patterns of a style: how often it uses small grammatical words.

Also counts contractions and vocabulary variety (distinct words per
10-word window).  The counts are taken over all example texts of a style
together.
"""

import re
from collections import Counter

WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
FUNCTION_WORDS = """
a about above after again against all am an and any are as at be because been
before being below between both but by can could did do does doing down during
each few for from further had has have having he her here hers herself him
himself his how i if in into is it its itself just me more most my myself no nor
not now of off on once only or other our ours ourselves out over own same she
should so some such than that the their theirs them themselves then there these
they this those through to too under until up very was we were what when where
which while who whom why will with would you your yours yourself yourselves
yeah oh well like really gonna wanna got get also however thus therefore may
might must shall upon whilst ye thee thou thy hath doth ain y'all u ur lol
""".split()
WINDOW = 10


def function_word_profile(texts: list[str]) -> dict[str, float]:
    """Rates of function words, contractions and vocabulary variety over all ``texts``."""
    counts, n_words, contractions = Counter(), 0, 0
    variety_sum, variety_windows = 0.0, 0
    known = set(FUNCTION_WORDS)
    for text in texts:
        words = [w.lower().replace("’", "'") for w in WORD.findall(text)]
        n_words += len(words)
        contractions += sum("'" in w for w in words)
        counts.update(w for w in words if w in known)
        for i in range(len(words) - WINDOW + 1):
            variety_sum += len(set(words[i:i + WINDOW])) / WINDOW
            variety_windows += 1

    n_words = max(n_words, 1)
    profile = {"word_" + w: counts[w] / n_words for w in FUNCTION_WORDS}
    profile["function_word_share"] = sum(counts.values()) / n_words
    profile["contractions"] = contractions / n_words
    profile["vocabulary_variety"] = variety_sum / variety_windows if variety_windows else float("nan")
    return profile
