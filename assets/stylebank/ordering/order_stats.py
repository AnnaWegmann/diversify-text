"""Print statistics for the current order of the default style bank (``_BANK_ORDER`` in bank.py).

Run from this folder:

    python order_stats.py
"""

from diversify_text.styles.bank import DEFAULT_STYLE_BANK
from style_order import print_report, style_distances

print("""ORDER STATISTICS FOR THE CURRENT ORDER

This script reports on the order that is in the package now: _BANK_ORDER in
diversify_text/styles/bank.py, the order in which `n` picks styles. It does not
change anything. To compute a new, suggested order, run suggest_order.py.

Styles are compared in three ways: surface patterns (punctuation, capitals,
emoji, word and sentence length), function words (how often a style uses small
words such as "the", "she" or "whilst") and the Style-Embedding model.
"smallest_of_three" is the lowest of the three, so a pair counts as close if
any one measure says so.

Computing the distances embeds every example text and takes a few minutes ...
""")
print_report(list(DEFAULT_STYLE_BANK), style_distances())
