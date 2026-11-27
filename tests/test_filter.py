"""Tests for the MIS content preservation filter."""

import unittest
from unittest.mock import MagicMock

from diversify_text import Diversifier
from diversify_text.filter.mis import MISFilter

from tests.fixtures import AttemptMethod


class TestReplaceLowScoring(unittest.TestCase):
    """MISFilter.replace_low_scoring with a mocked MIS model."""

    def test_only_paraphrases_below_min_score_are_regenerated(self):
        mis_filter = MISFilter(min_score=0.7)
        mis_filter.score = MagicMock(side_effect=[[0.9, 0.4], [0.8]])
        regenerate = MagicMock(return_value=["A storm raged through the dark night."])

        mis_filter.replace_low_scoring(
            ["It was a dark and stormy night."],
            [["The night was dark and stormy.", "It was a bright and sunny day."]],
            regenerate,
        )

        regenerate.assert_called_once_with([(0, 1)])

    def test_regenerated_paraphrase_replaces_the_low_scoring_one(self):
        mis_filter = MISFilter(min_score=0.7)
        mis_filter.score = MagicMock(side_effect=[[0.9, 0.4], [0.8]])
        regenerate = MagicMock(return_value=["A storm raged through the dark night."])

        paraphrases = mis_filter.replace_low_scoring(
            ["It was a dark and stormy night."],
            [["The night was dark and stormy.", "It was a bright and sunny day."]],
            regenerate,
        )

        self.assertEqual(
            paraphrases,
            [["The night was dark and stormy.", "A storm raged through the dark night."]],
        )

    def test_nothing_is_regenerated_when_all_reach_min_score(self):
        mis_filter = MISFilter(min_score=0.7)
        mis_filter.score = MagicMock(return_value=[0.9, 0.8])
        regenerate = MagicMock()

        mis_filter.replace_low_scoring(
            ["It was a dark and stormy night."],
            [["The night was dark and stormy.", "A storm raged through the dark night."]],
            regenerate,
        )

        regenerate.assert_not_called()

    def test_best_attempt_is_kept_when_none_reaches_min_score(self):
        mis_filter = MISFilter(min_score=0.7, max_attempts=3)
        mis_filter.score = MagicMock(side_effect=[[0.3], [0.6], [0.5]])
        regenerate = MagicMock(
            side_effect=[["The night was stormy."], ["The weather was bad."]]
        )

        paraphrases = mis_filter.replace_low_scoring(
            ["It was a dark and stormy night."],
            [["It was a bright and sunny day."]],
            regenerate,
        )

        self.assertEqual(paraphrases, [["The night was stormy."]])

    def test_paraphrase_is_generated_at_most_max_attempts_times(self):
        mis_filter = MISFilter(min_score=0.7, max_attempts=3)
        mis_filter.score = MagicMock(return_value=[0.3])
        regenerate = MagicMock(return_value=["It was a bright and sunny day."])

        mis_filter.replace_low_scoring(
            ["It was a dark and stormy night."],
            [["It was a bright and sunny day."]],
            regenerate,
        )

        self.assertEqual(regenerate.call_count, 2)


class TestMISFilterIntegration(unittest.TestCase):
    """Integration tests: MISFilter wired into Diversifier."""

    def test_no_filter_by_default(self):
        div = Diversifier(method="echo")
        self.assertIsNone(div._mis_filter)

    def test_constructor_stores_params(self):
        div = Diversifier(
            method="echo",
            semantic_filter=True,
            filter_kwargs={"min_score": 0.90, "max_attempts": 3},
        )
        self.assertIsNotNone(div._mis_filter)
        self.assertEqual(div._mis_filter.min_score, 0.90)
        self.assertEqual(div._mis_filter.max_attempts, 3)

    def test_low_scoring_paraphrase_is_regenerated_in_its_style(self):
        div = Diversifier(method=AttemptMethod(), semantic_filter=True)
        div._mis_filter.score = MagicMock(side_effect=[[0.9, 0.4], [0.8]])

        results = div.diversify(
            "It was a dark and stormy night.", styles=["formal", "informal"]
        )

        self.assertEqual(
            results[0]["paraphrases"],
            [
                {"style": "formal", "text": "It was a dark and stormy night. (formal, attempt 1)"},
                {"style": "informal", "text": "It was a dark and stormy night. (informal, attempt 2)"},
            ],
        )

    def test_low_scoring_paraphrases_of_different_styles_are_regenerated_together(self):
        div = Diversifier(method=AttemptMethod(), semantic_filter=True)
        div._mis_filter.score = MagicMock(side_effect=[[0.4, 0.4], [0.8, 0.8]])

        results = div.diversify(
            "It was a dark and stormy night.", styles=["formal", "informal"]
        )

        self.assertEqual(
            results[0]["paraphrases"],
            [
                {"style": "formal", "text": "It was a dark and stormy night. (formal, attempt 2)"},
                {"style": "informal", "text": "It was a dark and stormy night. (informal, attempt 2)"},
            ],
        )

    def test_low_scoring_repeat_is_regenerated_in_its_style(self):
        div = Diversifier(method=AttemptMethod(), semantic_filter=True)
        div._mis_filter.score = MagicMock(side_effect=[[0.9, 0.9, 0.9, 0.4], [0.8]])

        results = div.diversify(
            "It was a dark and stormy night.", styles=["formal", "informal"], repeats=2
        )

        self.assertEqual(
            results[0]["paraphrases"][3],
            {"style": "informal", "text": "It was a dark and stormy night. (informal, attempt 3)"},
        )

    def test_low_scoring_texts_split_into_sentences_are_regenerated_whole(self):
        div = Diversifier(method=AttemptMethod(), semantic_filter=True)
        div._mis_filter.score = MagicMock(side_effect=[[0.4, 0.4], [0.8, 0.8]])

        results = div.diversify(
            ["It was a dark and stormy night. The rain fell in torrents.", "Call me Ishmael."],
            styles=["formal"],
            preprocess_kwargs={"split_on_punctuation": True},
        )

        self.assertEqual(
            [result["paraphrases"][0]["text"] for result in results],
            [
                "It was a dark and stormy night. (formal, attempt 2) "
                "The rain fell in torrents. (formal, attempt 2)",
                "Call me Ishmael. (formal, attempt 2)",
            ],
        )


if __name__ == "__main__":
    unittest.main()
