"""Distances between the styles of the default bank, in three ways.

- surface: Burrows' Delta over the surface patterns (``surface.py``)
- function_words: Burrows' Delta over the function-word patterns (``function_words.py``)
- embedding: mean cosine distance between every example of one style and
  every example of the other, with the Style-Embedding model

The three measures have different ranges, so each matrix is scaled so
that the average pair of styles is 1.0: 0.5 is half as far apart as an
average pair, 1.5 half again as far.  "smallest" is, per pair, the
smallest of the three scaled distances, so two styles count as close if
any one of them says so.
"""

import json
from importlib import resources

import numpy as np

from diversify_text.styles._load import _RENAMES
from diversify_text.styles.bank import DEFAULT_STYLE_BANK
from diversify_text.styles.resolve import DEFAULT_MAX_LEN_STYLE_TEXT

from .function_words import function_word_profile
from .surface import surface_profile

EMBEDDING_MODEL = "AnnaWegmann/Style-Embedding"
MEASURES = ("surface", "function_words", "embedding")


def style_distances() -> dict:
    """Return ``{"names", "categories", "surface", "function_words", "embedding", "smallest", "centroids"}``."""
    names = list(DEFAULT_STYLE_BANK)
    texts = [[_cut(t) for t in DEFAULT_STYLE_BANK[name]] for name in names]
    embedding, centroids = _embedding_distances(texts)
    result = {
        "names": names,
        "categories": [_categories()[name] for name in names],
        "surface": _delta([surface_profile(t) for t in texts]),
        "function_words": _delta([function_word_profile(t) for t in texts]),
        "embedding": embedding,
        "centroids": centroids,
    }
    off_diagonal = ~np.eye(len(names), dtype=bool)
    for m in MEASURES:
        result[m] = result[m] / result[m][off_diagonal].mean()
    result["smallest"] = np.minimum.reduce([result[m] for m in MEASURES])
    np.fill_diagonal(result["smallest"], 0)
    return result


def _cut(text: str) -> str:
    """Keep the words a method sees: the first ``DEFAULT_MAX_LEN_STYLE_TEXT``."""
    return " ".join(text.split(" ")[:DEFAULT_MAX_LEN_STYLE_TEXT])


def _delta(profiles: list[dict]) -> np.ndarray:
    """Burrows' Delta: mean absolute difference of the styles' z-scored features."""
    keys = list(profiles[0])
    X = np.array([[p[k] for k in keys] for p in profiles])
    spread = np.nanstd(X, axis=0)
    X = X[:, spread > 0]
    Z = (X - np.nanmean(X, axis=0)) / spread[spread > 0]
    return np.nanmean(np.abs(Z[:, None, :] - Z[None, :, :]), axis=-1)


def _embedding_distances(texts: list[list[str]]) -> tuple[np.ndarray, np.ndarray]:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(EMBEDDING_MODEL)
    vectors = [model.encode(t, normalize_embeddings=True) for t in texts]
    distances = np.array([[1 - (a @ b.T).mean() for b in vectors] for a in vectors])
    centroids = np.array([v.mean(axis=0) for v in vectors])
    centroids /= np.linalg.norm(centroids, axis=1, keepdims=True)
    return distances, centroids


def _categories() -> dict[str, str]:
    """Style name -> its category in the taxonomy of ``stylebank.json`` (e.g. "diatopic")."""
    raw = json.loads(resources.files("diversify_text.styles").joinpath("stylebank.json").read_text("utf-8"))
    found = {}

    def walk(node: dict, parent: str) -> None:
        for key, value in node.items():
            if isinstance(value, dict):
                walk(value, key)
            else:
                found[_RENAMES.get(key, key)] = parent

    walk(raw, "")
    return found
