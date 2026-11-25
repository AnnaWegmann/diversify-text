"""diversify-text -- generate stylistic paraphrases of texts."""

import logging

from diversify_text._cache import clear_cache
from diversify_text.core import (
    Diversifier,
    diversify,
)
from diversify_text._evaluate import evaluate, EvaluationResult
from diversify_text._metrics import Metric, METRIC_REGISTRY
from diversify_text._diversity import (
    DiversityMetric,
    DIVERSITY_METRIC_REGISTRY,
    evaluate_diversity,
)

__all__ = [
    "DIVERSITY_METRIC_REGISTRY",
    "Diversifier",
    "DiversityMetric",
    "EvaluationResult",
    "METRIC_REGISTRY",
    "Metric",
    "clear_cache",
    "diversify",
    "evaluate",
    "evaluate_diversity",
]

# Configure a clean handler for the diversify logger so INFO/WARNING messages
# are visible without requiring the user to set up logging themselves.
_logger = logging.getLogger("diversify_text")
_logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
_logger.addHandler(_handler)
# Prevent messages from bubbling up to the root logger (avoids duplicate output
# if the user has already configured logging globally).
_logger.propagate = False
