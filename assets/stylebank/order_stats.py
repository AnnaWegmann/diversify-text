"""Print statistics for the current order of the default style bank (``_BANK_ORDER`` in bank.py).

Run from this folder:

    python order_stats.py
"""

from diversify_text.styles.bank import DEFAULT_STYLE_BANK
from ordering import print_report, style_distances

print_report(list(DEFAULT_STYLE_BANK), style_distances())
