"""Statistics for an order of the default bank, printed as plain-text tables.

For the first n styles: how many of each category, how many PASTEL
styles, the closest pair and the mean distance per measure, and the mean
pairwise Style-Embedding distance between the styles (one averaged vector
per style, unscaled cosine distance).  For every position: the style's
distinctiveness rank and the distance to the nearest style ranked above
it, per measure.  All per-measure distances are scaled so that an average
pair of styles in the bank is 1.0 (see ``distances.py``).
"""

from collections import Counter

import numpy as np

from .distances import MEASURES
from .suggest import is_pastel

FIRST_N = (5, 10, 21, 40)


def print_report(order: list[str], distances: dict) -> None:
    names, categories = distances["names"], distances["categories"]
    idx = [names.index(n) for n in order]
    measures = MEASURES + ("smallest_of_three",)

    print("Distances are scaled per measure: 1.0 = an average pair of styles in the bank.")
    print("mean_embedding_distance: mean cosine distance between the styles' averaged embedding vectors (not scaled).")
    print("First n styles: closest pair / mean distance per measure")
    print(f"{'n':>3}  {'categories':<44} pastel  " + "  ".join(f"{m:>16}" for m in measures) + "  mean_embedding_distance")
    for n in FIRST_N:
        first = idx[:n]
        per_category = Counter(categories[i] for i in first)
        cats = ", ".join(f"{c} {k}" for c, k in sorted(per_category.items()))
        cells = []
        for m in measures:
            pairs = distances[m][np.ix_(first, first)][~np.eye(n, dtype=bool)]
            cells.append(f"{pairs.min():.2f} / {pairs.mean():.2f}".rjust(16))
        print(f"{n:>3}  {cats:<44} {sum(is_pastel(names[i]) for i in first):>6}  " + "  ".join(cells)
              + f"  {_mean_pairwise(distances['centroids'][first]):>17.2f}")

    combined = distances["smallest_of_three"]
    mean = combined.sum(axis=1) / (len(names) - 1)
    rank = {names[i]: r + 1 for r, i in enumerate(np.argsort(-mean))}
    print("\nPer position: distinctiveness rank (1 = most different), distance to the nearest style above")
    print(f"{'#':>3}  {'style':<46} {'category':<11} {'rank':>4}  " + "  ".join(f"{m:>14}" for m in measures))
    for k, i in enumerate(idx):
        above = idx[:k]
        cells = [f"{distances[m][i, above].min():14.2f}" if above else f"{'-':>14}" for m in measures]
        print(f"{k + 1:>3}  {names[i]:<46} {categories[i]:<11} {rank[names[i]]:>4}  " + "  ".join(cells))


def _mean_pairwise(vectors: np.ndarray) -> float:
    """Mean cosine distance over all pairs of the given style vectors."""
    similarities = vectors @ vectors.T
    upper = np.triu_indices(len(vectors), 1)
    return float((1 - similarities[upper]).mean())
