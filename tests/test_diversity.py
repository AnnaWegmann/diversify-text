"""Tests for output diversity (diversify_text._diversity).

The plumbing tests use a stub metric, so nothing is loaded.  The Vendi
tests use a fake encoder with known vectors, and one class runs the
real embedding model (downloaded on first use, about 420 MB).
"""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from diversify_text import (
    DIVERSITY_METRIC_REGISTRY,
    DiversityMetric,
    evaluate_diversity,
)
from diversify_text._diversity import VendiScore, resolve_diversity_metrics
from diversify_text._metrics import _MODEL_CACHE, clear_metric_cache

DEVICE = os.environ.get("DIVERSIFY_TEST_DEVICE", "cpu")


def installed(*modules):
    """True when every named module can be imported."""
    return all(importlib.util.find_spec(m) is not None for m in modules)


# ------------------------------------------------------------------
# Stubs
# ------------------------------------------------------------------


class DistinctCount(DiversityMetric):
    """Number of distinct paraphrases — a metric with known values."""

    name = "distinct"

    def compute(self, paraphrase_sets):
        return [len(set(s)) if len(s) >= self.min_size else None
                for s in paraphrase_sets]


class ModelBacked(DiversityMetric):
    """Takes a model, so model handling can be tested without downloads."""

    name = "model_backed"
    accepts_model = True
    default_model = "default-model"

    def compute(self, paraphrase_sets):
        offset = 0.0 if self.model == self.default_model else 10.0
        return [offset + len(s) for s in paraphrase_sets]


class FakeEncoder:
    """Maps each text to a fixed vector, like a SentenceTransformer."""

    def __init__(self, vectors):
        self.vectors = vectors
        self.calls = 0

    def encode(self, texts, convert_to_numpy=True):
        self.calls += 1
        return np.array([self.vectors[t] for t in texts], dtype=float)


# Distinct counts: 2 and 3, so the dataset mean is 2.5.
RECORDS = [
    {
        "original": "first",
        "paraphrases": [
            {"style": "informal", "text": "a"},
            {"style": "formal", "text": "a"},
            {"style": "poetic", "text": "b"},
        ],
    },
    {
        "original": "second",
        "paraphrases": [
            {"style": "informal", "text": "x"},
            {"style": "formal", "text": "y"},
            {"style": "poetic", "text": "z"},
        ],
    },
]


# ------------------------------------------------------------------
# Plumbing
# ------------------------------------------------------------------


class TestGranularity(unittest.TestCase):

    def test_dataset_is_the_default(self):
        result = evaluate_diversity(RECORDS, metrics=[DistinctCount()])
        self.assertEqual(result.dataset, {"distinct": 2.5})
        self.assertIsNone(result.text)
        self.assertIsNone(result.pair)

    def test_text_level_scores_each_data_point(self):
        result = evaluate_diversity(
            RECORDS, metrics=[DistinctCount()], granularity="text"
        )
        self.assertEqual([r["distinct"] for r in result.text], [2, 3])
        self.assertEqual(result.text[0]["original"], "first")
        self.assertEqual(result.text[0]["n_paraphrases"], 3)
        self.assertIsNone(result.dataset)

    def test_dataset_is_the_mean_over_data_points(self):
        # 2 paraphrases in one text, 4 in the other: a mean over
        # paraphrases would weigh the second text twice as much.
        records = [
            {"original": "a", "paraphrases": ["p", "q"]},
            {"original": "b", "paraphrases": ["r", "r", "r", "r"]},
        ]
        result = evaluate_diversity(records, metrics=[DistinctCount()])
        self.assertEqual(result.dataset["distinct"], 1.5)

    def test_all_reports_text_and_dataset_but_no_pairs(self):
        result = evaluate_diversity(
            RECORDS, metrics=[DistinctCount()], granularity="all"
        )
        self.assertIsNotNone(result.text)
        self.assertIsNotNone(result.dataset)
        self.assertIsNone(result.pair)

    def test_pair_granularity_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=[DistinctCount()], granularity="pair")

    def test_too_small_sets_score_none_and_are_skipped(self):
        records = RECORDS + [
            {"original": "one", "paraphrases": ["only"]},
            {"original": "none", "paraphrases": []},
        ]
        result = evaluate_diversity(
            records, metrics=[DistinctCount()], granularity="all"
        )
        self.assertEqual([r["distinct"] for r in result.text], [2, 3, None, None])
        self.assertEqual(result.dataset["distinct"], 2.5)

    def test_plain_string_paraphrases_are_accepted(self):
        records = [{"original": "o", "paraphrases": ["a", "b"]}]
        result = evaluate_diversity(records, metrics=[DistinctCount()])
        self.assertEqual(result.dataset["distinct"], 2)

    def test_reads_a_jsonl_file(self):
        import json

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.jsonl"
            path.write_text("\n".join(json.dumps(r) for r in RECORDS))
            result = evaluate_diversity(path, metrics=[DistinctCount()])
        self.assertEqual(result.dataset["distinct"], 2.5)

    def test_to_jsonl_tags_each_row_with_its_level(self):
        import json

        result = evaluate_diversity(
            RECORDS, metrics=[DistinctCount()], granularity="all"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = result.to_jsonl(Path(tmp) / "scores.jsonl")
            rows = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual([r["level"] for r in rows], ["text", "text", "dataset"])


class TestErrors(unittest.TestCase):

    def test_no_paraphrases_at_all(self):
        records = [{"original": "o", "paraphrases": []}]
        with self.assertRaises(ValueError):
            evaluate_diversity(records, metrics=[DistinctCount()])

    def test_empty_metric_list(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=[])

    def test_unknown_metric_name(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=["nope"])

    def test_pair_metric_name_is_not_a_diversity_metric(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=["bertscore"])

    def test_repeated_metric_name(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=["vendi", "vendi"])

    def test_two_instances_of_one_metric(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=[DistinctCount(), DistinctCount()])

    def test_unapplied_metric_kwargs(self):
        with self.assertRaises(ValueError):
            evaluate_diversity(
                RECORDS, metrics=[DistinctCount()],
                metric_kwargs={"vendi": {"model": "x"}},
            )

    def test_model_on_a_fixed_model_metric(self):
        with self.assertRaises(ValueError):
            DistinctCount(model="x")

    def test_wrong_number_of_scores(self):
        class Short(DiversityMetric):
            name = "short"

            def compute(self, paraphrase_sets):
                return [1.0]

        with self.assertRaises(ValueError):
            evaluate_diversity(RECORDS, metrics=[Short()])


class TestMetricSelection(unittest.TestCase):

    def test_registry_lists_vendi(self):
        self.assertIs(DIVERSITY_METRIC_REGISTRY["vendi"], VendiScore)

    def test_none_selects_every_registered_metric(self):
        resolved = resolve_diversity_metrics(None)
        self.assertEqual([m.name for m in resolved], list(DIVERSITY_METRIC_REGISTRY))

    def test_device_reaches_registry_metrics(self):
        (metric,) = resolve_diversity_metrics(["vendi"], device="cuda")
        self.assertEqual(metric.device, "cuda")

    def test_model_argument_via_metric_kwargs(self):
        DIVERSITY_METRIC_REGISTRY["model_backed"] = ModelBacked
        try:
            result = evaluate_diversity(
                RECORDS,
                metrics=["model_backed"],
                metric_kwargs={"model_backed": {"model": "other"}},
            )
            self.assertGreater(result.dataset["model_backed"], 10.0)
        finally:
            del DIVERSITY_METRIC_REGISTRY["model_backed"]


# ------------------------------------------------------------------
# Vendi score with known vectors
# ------------------------------------------------------------------


@unittest.skipUnless(installed("emb_diversity"), "emb_diversity not installed")
class TestVendiScoreValues(unittest.TestCase):
    """Vendi is the effective number of distinct items: n for orthogonal
    vectors, 1 for identical ones."""

    VECTORS = {
        "a": [1.0, 0.0, 0.0],
        "b": [0.0, 1.0, 0.0],
        "c": [0.0, 0.0, 1.0],
        "a again": [2.0, 0.0, 0.0],  # same direction as "a"
    }

    def make_metric(self):
        from emb_diversity import vendi_score

        metric = VendiScore()
        metric.prepare = lambda: None
        metric._vendi = vendi_score
        metric._encoder = FakeEncoder(self.VECTORS)
        return metric

    def run_on(self, *paraphrase_sets):
        records = [{"original": "o", "paraphrases": list(s)} for s in paraphrase_sets]
        metric = self.make_metric()
        result = evaluate_diversity(records, metrics=[metric], granularity="all")
        return metric, result

    def test_orthogonal_paraphrases_score_n(self):
        _, result = self.run_on(["a", "b", "c"])
        self.assertAlmostEqual(result.text[0]["vendi"], 3.0, places=5)

    def test_identical_paraphrases_score_one(self):
        _, result = self.run_on(["a", "a again", "a"])
        self.assertAlmostEqual(result.text[0]["vendi"], 1.0, places=5)

    def test_each_data_point_is_scored_on_its_own_paraphrases(self):
        _, result = self.run_on(["a", "b", "c"], ["a", "a"], ["b", "c"])
        self.assertEqual(
            [round(r["vendi"], 5) for r in result.text], [3.0, 1.0, 2.0]
        )
        self.assertAlmostEqual(result.dataset["vendi"], 2.0, places=5)

    def test_single_paraphrase_scores_none(self):
        _, result = self.run_on(["a", "b"], ["c"])
        self.assertIsNone(result.text[1]["vendi"])
        self.assertAlmostEqual(result.dataset["vendi"], 2.0, places=5)

    def test_all_paraphrases_are_embedded_in_one_pass(self):
        metric, _ = self.run_on(["a", "b"], ["c", "a"], ["b", "c"])
        self.assertEqual(metric._encoder.calls, 1)


# ------------------------------------------------------------------
# Vendi score with the real model
# ------------------------------------------------------------------


@unittest.skipUnless(
    installed("emb_diversity", "sentence_transformers"),
    "emb_diversity not installed",
)
class TestVendiScoreModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        records = [
            {
                "original": "The experiment was conducted in a lab.",
                "paraphrases": [
                    "The experiment was conducted in a lab.",
                    "The experiment was carried out in a laboratory.",
                    "They did the experiment in a lab.",
                ],
            },
            {
                "original": "The experiment was conducted in a lab.",
                "paraphrases": [
                    "The experiment was conducted in a lab.",
                    "The cat knocked a mug off the kitchen table.",
                    "Stock markets fell sharply this morning.",
                ],
            },
        ]
        cls.result = evaluate_diversity(records, granularity="text", device=DEVICE)

    def test_unrelated_texts_are_more_diverse_than_paraphrases(self):
        close, unrelated = (r["vendi"] for r in self.result.text)
        self.assertLess(close, unrelated)

    def test_scores_lie_between_one_and_n(self):
        for row in self.result.text:
            self.assertGreaterEqual(row["vendi"], 1.0 - 1e-6)
            self.assertLessEqual(row["vendi"], row["n_paraphrases"] + 1e-6)

    def test_model_is_shared_with_the_metric_cache(self):
        self.assertIn(("vendi", "all-mpnet-base-v2", DEVICE), _MODEL_CACHE)
        clear_metric_cache()
        self.assertNotIn(("vendi", "all-mpnet-base-v2", DEVICE), _MODEL_CACHE)


if __name__ == "__main__":
    unittest.main()
