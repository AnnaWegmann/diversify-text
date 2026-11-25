"""Output diversity of diversify output.

Where :func:`~diversify_text.evaluate` scores each ``(original,
paraphrase)`` pair, the metrics here score how different the
paraphrases of one input text are from *each other*.  Every input text
(data point) gets one score per metric, computed over its paraphrases
only -- the original is not part of the set.  The dataset score is the
mean over data points, so each input text counts once however many
paraphrases it has.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from diversify_text._evaluate import EvaluationResult, _load_records, _mean
from diversify_text._metrics import _cached

GRANULARITIES = ("text", "dataset", "all")


# ------------------------------------------------------------------
# Base class
# ------------------------------------------------------------------


class DiversityMetric:
    """Base class for output-diversity metrics.

    Subclasses set the class attributes below and implement
    :meth:`prepare` and :meth:`compute`.

    Attributes
    ----------
    name : str
        Registry name and result key.
    accepts_model : bool
        Whether the metric takes a ``model`` argument.
    default_model : str or None
        Model used when the caller does not pass one.
    min_size : int
        Smallest number of paraphrases the metric can score; smaller
        sets score ``None``.
    """

    name: str = ""
    accepts_model: bool = False
    default_model: str | None = None
    min_size: int = 2

    def __init__(self, *, device: str = "cpu", model: str | None = None) -> None:
        self.device = device
        if model is not None and not self.accepts_model:
            raise ValueError(
                f"Metric {self.name!r} has a fixed model and does not "
                f"accept a 'model' argument."
            )
        if model is not None and not isinstance(model, str):
            raise ValueError(
                f"Metric {self.name!r} expects 'model' as a string "
                f"identifier, got {type(model).__name__}."
            )
        self.model = model if model is not None else self.default_model

    def prepare(self) -> None:
        """Import dependencies and load models.  Called once before use."""

    def compute(self, paraphrase_sets: list[list[str]]) -> list[float | None]:
        """Score each set of paraphrases.

        Returns one score per set, in input order.  ``None`` marks a set
        the metric cannot score (fewer than :attr:`min_size`
        paraphrases); averages skip it.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}(model={self.model!r}, device={self.device!r})"


# ------------------------------------------------------------------
# Metrics
# ------------------------------------------------------------------


class VendiScore(DiversityMetric):
    """Vendi score: the effective number of distinct paraphrases.

    The paraphrases of a data point are embedded with a
    sentence-transformers model and scored with ``emb-diversity``'s
    ``vendi_score`` (Friedman & Dieng, 2023).  It ranges from 1 (all
    paraphrases identical) to *n* (all fully dissimilar), so it is only
    comparable between runs with the same number of paraphrases per
    text.

    The default model is the one ``emb-diversity`` uses for semantic
    diversity, so by default this measures diversity of meaning.
    """

    name = "vendi"
    accepts_model = True
    default_model = "all-mpnet-base-v2"

    def prepare(self) -> None:
        from emb_diversity import vendi_score
        from sentence_transformers import SentenceTransformer

        self._vendi = vendi_score
        self._encoder = _cached(
            (self.name, self.model, self.device),
            lambda: SentenceTransformer(self.model, device=self.device),
        )

    def compute(self, paraphrase_sets):
        # Embed every paraphrase in one pass, then score each set.
        flat = [text for texts in paraphrase_sets for text in texts]
        vectors = self._encoder.encode(flat, convert_to_numpy=True) if flat else []

        scores: list[float | None] = []
        start = 0
        for texts in paraphrase_sets:
            block = vectors[start:start + len(texts)]
            start += len(texts)
            if len(texts) < self.min_size:
                scores.append(None)
            else:
                scores.append(float(self._vendi(block)["value"]))
        return scores


DIVERSITY_METRIC_REGISTRY: dict[str, type[DiversityMetric]] = {
    cls.name: cls for cls in (VendiScore,)
}


def resolve_diversity_metrics(
    metrics: list[str | DiversityMetric] | None = None,
    metric_kwargs: dict[str, dict[str, Any]] | None = None,
    device: str = "cpu",
) -> list[DiversityMetric]:
    """Turn metric names and keyword arguments into metric instances.

    Works like :func:`~diversify_text._metrics.resolve_metrics`, with
    :data:`DIVERSITY_METRIC_REGISTRY`.
    """
    remaining = dict(metric_kwargs or {})
    names: list[str | DiversityMetric] = (
        list(DIVERSITY_METRIC_REGISTRY) if metrics is None else list(metrics)
    )

    resolved: list[DiversityMetric] = []
    for entry in names:
        if isinstance(entry, DiversityMetric):
            resolved.append(entry)
        elif isinstance(entry, str):
            if entry not in DIVERSITY_METRIC_REGISTRY:
                raise ValueError(
                    f"Unknown diversity metric {entry!r}. "
                    f"Available: {sorted(DIVERSITY_METRIC_REGISTRY)}."
                )
            resolved.append(
                DIVERSITY_METRIC_REGISTRY[entry](
                    device=device, **remaining.pop(entry, {})
                )
            )
        else:
            raise TypeError(
                f"metrics entries must be a name or a DiversityMetric, got "
                f"{type(entry).__name__}."
            )

    if remaining:
        raise ValueError(
            f"metric_kwargs entries were not applied: {sorted(remaining)}. "
            f"They name a metric that was not selected, is unknown, or was "
            f"passed as a pre-built instance."
        )
    return resolved


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------


def evaluate_diversity(
    output,
    *,
    metrics: list[str | DiversityMetric] | None = None,
    metric_kwargs: dict[str, dict[str, Any]] | None = None,
    granularity: str = "dataset",
    device: str | None = None,
) -> EvaluationResult:
    """Measure how diverse the paraphrases of each input text are.

    Each input text (data point) is scored on its own set of
    paraphrases; the original text is not included.  The dataset score
    is the mean over data points.

    Parameters
    ----------
    output : DiversifyResult | list[dict] | str | Path
        The value returned by :func:`diversify`, or a path to a
        ``.jsonl`` file it wrote.
    metrics : list of str or DiversityMetric, optional
        Which metrics to run.  ``None`` runs all of them: ``vendi``.
    metric_kwargs : dict, optional
        Per-metric keyword arguments keyed by metric name, e.g.
        ``{"vendi": {"model": "all-MiniLM-L6-v2"}}``.
    granularity : {"text", "dataset", "all"}
        ``"text"`` reports one score per input text, ``"dataset"`` the
        mean over input texts, and ``"all"`` both.
    device : str, optional
        Device for the model-based metrics.  Defaults to the device the
        output was generated on, and to ``"cpu"`` when that is unknown.

    Returns
    -------
    EvaluationResult
        With ``pair`` always ``None``.  Input texts with fewer than two
        paraphrases score ``None`` and are left out of the mean.

    Example
    -------
    >>> from diversify_text import diversify, evaluate_diversity
    >>> evaluate_diversity(diversify("The experiment was conducted in a lab."))
    """
    if granularity not in GRANULARITIES:
        raise ValueError(
            f"Unknown granularity {granularity!r}. Available: {list(GRANULARITIES)}."
        )

    if metrics is not None:
        counts = Counter(m for m in metrics if isinstance(m, str))
        repeated = sorted(name for name, n in counts.items() if n > 1)
        if repeated:
            raise ValueError(f"Metrics selected more than once: {repeated}.")

    records = _load_records(output)
    if device is None:
        device = getattr(output, "device", None) or "cpu"

    resolved = resolve_diversity_metrics(metrics, metric_kwargs, device=device)
    if not resolved:
        raise ValueError("No metrics selected.")

    paraphrase_sets = [
        [e["text"] if isinstance(e, dict) else e for e in record["paraphrases"]]
        for record in records
    ]
    if not any(paraphrase_sets):
        raise ValueError("Nothing to evaluate: the output contains no paraphrases.")

    scores: dict[str, list[float | None]] = {}
    for metric in resolved:
        if metric.name in scores:
            raise ValueError(
                f"Metric {metric.name!r} reports score {metric.name!r}, which "
                f"another selected metric already reported."
            )
        metric.prepare()
        values = metric.compute(paraphrase_sets)
        if len(values) != len(records):
            raise ValueError(
                f"Metric {metric.name!r} returned {len(values)} scores "
                f"for {len(records)} texts."
            )
        scores[metric.name] = values

    columns = list(scores)
    result = EvaluationResult(granularity=granularity, metrics=columns)

    if granularity in ("text", "all"):
        result.text = [
            {
                "text_index": i,
                "original": record["original"],
                "n_paraphrases": len(paraphrase_sets[i]),
                **{c: scores[c][i] for c in columns},
            }
            for i, record in enumerate(records)
        ]

    if granularity in ("dataset", "all"):
        result.dataset = {c: _mean(scores[c]) for c in columns}

    return result
