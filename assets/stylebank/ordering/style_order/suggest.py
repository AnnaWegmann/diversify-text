"""Suggest an order for the default bank: categories take turns, farthest style first.

The next style is the one whose closest already-placed style is farthest
away ("smallest" distance, see ``distances.py``).  A category does not get
a second style until every other category that still has styles left has
had one in the current round.  PASTEL styles (education_*, ethnic_*,
politics_*) come after all other styles.
"""

import numpy as np

PASTEL_PREFIXES = ("education_", "ethnic_", "politics_")


def is_pastel(name: str) -> bool:
    return name.startswith(PASTEL_PREFIXES)


def most_distinct(distances: dict) -> str:
    """The non-PASTEL style with the highest mean distance to all other styles."""
    D, names = distances["smallest"], distances["names"]
    mean = (D.sum(axis=1)) / (len(names) - 1)
    return max((n for n in names if not is_pastel(n)), key=lambda n: mean[names.index(n)])


def suggest_order(distances: dict, first: str, fixed: dict[str, int] | None = None,
                  next_in_category: tuple[str, ...] = (), at_most_one: tuple[str, int] | None = None) -> list[str]:
    """Return all style names in the suggested order.

    first: the style at position 1.
    fixed: styles placed at a given position, e.g. ``{"formal": 2}``.
    next_in_category: styles that come before every other style of their
        category that is not placed yet, e.g. ``("age_child",)``.
    at_most_one: ``(word, n)``: at most one style whose name contains
        ``word`` in the first ``n`` positions, e.g. ``("creole", 20)``.
    """
    names, categories, D = distances["names"], distances["categories"], distances["smallest"]
    fixed = fixed or {}
    order = [first]
    round_categories = {categories[names.index(first)]}
    while len(order) < len(names):
        rest = [n for n in names if n not in order]
        if any(not is_pastel(n) for n in rest):
            rest = [n for n in rest if not is_pastel(n)]
        if not any(categories[names.index(n)] not in round_categories for n in rest):
            round_categories = set()  # every category with styles left has had its turn
        candidates = [n for n in rest if categories[names.index(n)] not in round_categories]
        for style in next_in_category:
            if style not in order:
                category = categories[names.index(style)]
                candidates = [n for n in candidates if categories[names.index(n)] != category or n == style] or candidates
        if at_most_one and len(order) < at_most_one[1] and any(at_most_one[0] in n for n in order):
            candidates = [n for n in candidates if at_most_one[0] not in n] or candidates
        position = len(order) + 1
        pinned = [n for n, p in fixed.items() if p == position and n not in order]
        if pinned:
            candidates = pinned
        else:
            candidates = [n for n in candidates if n not in fixed] or candidates
        placed = [names.index(n) for n in order]
        best = max(candidates, key=lambda n: D[names.index(n), placed].min())
        order.append(best)
        round_categories.add(categories[names.index(best)])
    return order
