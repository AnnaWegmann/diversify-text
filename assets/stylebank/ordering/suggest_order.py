"""Suggest an order for the default style bank and print its statistics.

The order starts with the most distinct style, lets the categories take
turns and always adds the style farthest from those already placed, using
all three measures (see style_order/suggest.py).  The rules below are
judgement calls on top of the distances.  The suggested list is printed
in the format of ``_BANK_ORDER`` in bank.py.

Run from this folder:

    python suggest_order.py
"""

from style_order import most_distinct, print_report, style_distances, suggest_order

FIXED = {"formal": 2}  # show the informal/formal contrast right away
NEXT_IN_CATEGORY = ("age_child", "lyrical")  # first diastratic style; next diaphasic style after formal
AT_MOST_ONE = ("creole", 20)  # at most one creole in the first 20

distances = style_distances()
first = most_distinct(distances)
order = suggest_order(distances, first, fixed=FIXED, next_in_category=NEXT_IN_CATEGORY, at_most_one=AT_MOST_ONE)
print_report(order, distances)
print("\n_BANK_ORDER: list[str] = [")
for name in order:
    print(f'    "{name}",  # {distances["categories"][distances["names"].index(name)]}')
print("]")
