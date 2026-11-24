"""Measure how different the styles of the default bank are, and suggest an order.

Used by ``order_stats.py`` and ``suggest_order.py`` in the folder above.
Run from ``assets/stylebank``:

    from ordering import style_distances, suggest_order, most_distinct, print_report

    distances = style_distances()  # takes a few minutes: embeds every example text
    order = suggest_order(distances, first=most_distinct(distances))
    print_report(order, distances)
"""

from .distances import style_distances
from .stats import print_report
from .suggest import most_distinct, suggest_order

__all__ = ["style_distances", "suggest_order", "most_distinct", "print_report"]
