"""Suggest an order for the default style bank and print its statistics.

The order starts with the most distinct style, lets the categories take
turns and always adds the style farthest from those already placed, using
all three measures (see style_order/suggest.py).  The rules below are
judgement calls on top of the distances.  The suggested list is printed
in the format of ``_BANK_ORDER`` in bank.py.

Run from this folder:

    python suggest_order.py
"""

from diversify_text.styles.bank import DEFAULT_STYLE_BANK
from style_order import most_distinct, print_report, style_distances, suggest_order

FIXED = {"formal": 2}  # show the informal/formal contrast right away
NEXT_IN_CATEGORY = ("age_child", "lyrical")  # first diastratic style; next diaphasic style after formal
AT_MOST_ONE = ("creole", 20)  # at most one creole in the first 20

print(f"""SUGGESTED ORDER

Unlike order_stats.py, which only reports on the current _BANK_ORDER in
diversify_text/styles/bank.py, this script builds a new order from the
distances between the styles. It does not change bank.py: it prints the
suggested list at the end, to be copied into bank.py by hand if wanted.

How the order is built:
- Position 1 is the style most different from all others (PASTEL left out).
- Categories take turns: a category gets its next style only after every other
  category that still has styles left has had one in the current round.
- Each time, the style whose closest already-placed style is farthest away is
  added. Two styles count as close if any one of surface patterns, function
  words or the Style-Embedding says so.
- PASTEL styles (education_*, ethnic_*, politics_*) come after all others.

Rules on top of the distances (set at the top of suggest_order.py):
- fixed positions: {", ".join(f"{name} at {pos}" for name, pos in FIXED.items())}
- comes first among the remaining styles of its category: {", ".join(NEXT_IN_CATEGORY)}
- at most one style with "{AT_MOST_ONE[0]}" in its name in the first {AT_MOST_ONE[1]}

Computing the distances embeds every example text and takes a few minutes ...
""")

distances = style_distances()
first = most_distinct(distances)
order = suggest_order(distances, first, fixed=FIXED, next_in_category=NEXT_IN_CATEGORY, at_most_one=AT_MOST_ONE)
print(f"Most different style, used as position 1: {first}\n")
print_report(order, distances)

current = list(DEFAULT_STYLE_BANK)
moved = sum(a != b for a, b in zip(order, current))
print(f"\nCompared with the current _BANK_ORDER: {moved} of {len(order)} positions differ.")
if moved:
    k = next(i for i, (a, b) in enumerate(zip(order, current)) if a != b)
    print(f"First difference at position {k + 1}: suggested {order[k]}, current {current[k]}.")
print("\nSuggested _BANK_ORDER (copy into diversify_text/styles/bank.py to use it):")
print("_BANK_ORDER: list[str] = [")
for name in order:
    print(f'    "{name}",  # {distances["categories"][distances["names"].index(name)]}')
print("]")
