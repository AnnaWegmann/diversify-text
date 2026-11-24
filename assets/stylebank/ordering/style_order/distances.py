"""Distances between the styles of the default bank, in three ways.

- surface: how different two styles' surface patterns are (``surface.py``)
- function_words: how different their function-word patterns are (``function_words.py``)
- embedding: mean cosine distance between every example of one style and
  every example of the other, with the Style-Embedding model

For surface patterns and function words, every feature is first expressed
as how many standard deviations a style lies above or below the average
style; the distance between two styles is the mean difference over all
features.

The three measures have different ranges, so each matrix is scaled so
that the average pair of styles is 1.0: 0.5 is half as far apart as an
average pair, 1.5 half again as far.  "smallest_of_three" is, per pair,
the smallest of the three scaled distances, so two styles count as close
if any one of them says so.
"""

import json
from importlib import resources

import numpy as np

from diversify_text._metrics import StyleSimilarity
from diversify_text.styles._load import flatten_style_bank
from diversify_text.styles.bank import DEFAULT_STYLE_BANK
from diversify_text.styles.resolve import DEFAULT_MAX_LEN_STYLE_TEXT, _truncate_words

from .function_words import function_word_profile
from .surface import surface_profile

MEASURES = ("surface", "function_words", "embedding")


def style_distances() -> dict:
    """Return ``{"names", "categories", "surface", "function_words", "embedding", "smallest_of_three", "centroids"}``."""
    names = list(DEFAULT_STYLE_BANK)
    # cut texts the way the package does before passing them to a method
    texts = [[_truncate_words(t, DEFAULT_MAX_LEN_STYLE_TEXT) for t in DEFAULT_STYLE_BANK[n]] for n in names]
    embedding, centroids = _embedding_distances(texts)
    category = _categories()
    result = {
        "names": names,
        "categories": [category[name] for name in names],
        "surface": _feature_distances([surface_profile(t) for t in texts]),
        "function_words": _feature_distances([function_word_profile(t) for t in texts]),
        "embedding": embedding,
        "centroids": centroids,
    }
    off_diagonal = ~np.eye(len(names), dtype=bool)
    for m in MEASURES:
        result[m] = result[m] / result[m][off_diagonal].mean()
    result["smallest_of_three"] = np.minimum.reduce([result[m] for m in MEASURES])
    np.fill_diagonal(result["smallest_of_three"], 0)
    return result


def _feature_distances(profiles: list[dict]) -> np.ndarray:
    """Mean difference between two styles over all features, each in standard deviations."""
    keys = list(profiles[0])
    X = np.array([[p[k] for k in keys] for p in profiles])
    spread = np.nanstd(X, axis=0)
    X = X[:, spread > 0]
    standardized = (X - np.nanmean(X, axis=0)) / spread[spread > 0]
    return np.nanmean(np.abs(standardized[:, None, :] - standardized[None, :, :]), axis=-1)


def _embedding_distances(texts: list[list[str]]) -> tuple[np.ndarray, np.ndarray]:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(StyleSimilarity.default_model)
    vectors = [model.encode(t, normalize_embeddings=True) for t in texts]
    distances = np.array([[1 - (a @ b.T).mean() for b in vectors] for a in vectors])
    centroids = np.array([v.mean(axis=0) for v in vectors])
    centroids /= np.linalg.norm(centroids, axis=1, keepdims=True)
    return distances, centroids


def _categories() -> dict[str, str]:
    """Style name -> its category in ``stylebank.json``, e.g. "diatopic"."""
    raw = json.loads(resources.files("diversify_text.styles").joinpath("stylebank.json").read_text("utf-8"))
    return {
        name: category
        for group in raw["language_variation"].values()
        for category, styles in group.items()
        for name in flatten_style_bank(styles)
    }
