"""Tests for the MIS content preservation filter.

The real MIS model is not used to score: every test sets the scores
itself, so it is visible which paraphrase counts as too far from the
original (a score below ``min_score``).
"""

import unittest
from unittest.mock import MagicMock

from diversify_text import Diversifier
from diversify_text.filter.mis import MISFilter

from tests.fixtures import AttemptMethod


class TestReplaceLowScoring(unittest.TestCase):
    """MISFilter.replace_low_scoring: paraphrases that score below
    min_score are generated again, the others are kept."""

    def test_only_paraphrases_below_min_score_are_regenerated(self):
        mis_filter = MISFilter(min_score=0.7)
        scores = {
            "The night was dark and stormy.": 0.9,
            "It was a bright and sunny day.": 0.4,
            "A storm raged through the dark night.": 0.8,
        }
        mis_filter.score = lambda originals, paraphrases: [scores[p] for p in paraphrases]
        regenerate = MagicMock(return_value=["A storm raged through the dark night."])

        mis_filter.replace_low_scoring(
            originals=["It was a dark and stormy night."],
            paraphrases_by_text=[
                ["The night was dark and stormy.", "It was a bright and sunny day."]
            ],
            regenerate=regenerate,
        )

        # (0, 1) is paraphrase 1 of text 0: the one that scored 0.4.
        regenerate.assert_called_once_with([(0, 1)])

    def test_regenerated_paraphrase_replaces_the_low_scoring_one(self):
        mis_filter = MISFilter(min_score=0.7)
        scores = {
            "The night was dark and stormy.": 0.9,
            "It was a bright and sunny day.": 0.4,
            "A storm raged through the dark night.": 0.8,
        }
        mis_filter.score = lambda originals, paraphrases: [scores[p] for p in paraphrases]
        regenerate = MagicMock(return_value=["A storm raged through the dark night."])

        paraphrases = mis_filter.replace_low_scoring(
            originals=["It was a dark and stormy night."],
            paraphrases_by_text=[
                ["The night was dark and stormy.", "It was a bright and sunny day."]
            ],
            regenerate=regenerate,
        )

        self.assertEqual(
            paraphrases,
            [["The night was dark and stormy.", "A storm raged through the dark night."]],
        )

    def test_nothing_is_regenerated_when_all_reach_min_score(self):
        mis_filter = MISFilter(min_score=0.7)
        scores = {
            "The night was dark and stormy.": 0.9,
            "A storm raged through the dark night.": 0.8,
        }
        mis_filter.score = lambda originals, paraphrases: [scores[p] for p in paraphrases]
        regenerate = MagicMock()

        mis_filter.replace_low_scoring(
            originals=["It was a dark and stormy night."],
            paraphrases_by_text=[
                ["The night was dark and stormy.", "A storm raged through the dark night."]
            ],
            regenerate=regenerate,
        )

        regenerate.assert_not_called()

    def test_best_attempt_is_kept_when_none_reaches_min_score(self):
        mis_filter = MISFilter(min_score=0.7, max_attempts=3)
        scores = {
            "It was a bright and sunny day.": 0.3,
            "The night was stormy.": 0.6,
            "The weather was bad.": 0.5,
        }
        mis_filter.score = lambda originals, paraphrases: [scores[p] for p in paraphrases]
        # The second and the third attempt.
        regenerate = MagicMock(
            side_effect=[["The night was stormy."], ["The weather was bad."]]
        )

        paraphrases = mis_filter.replace_low_scoring(
            originals=["It was a dark and stormy night."],
            paraphrases_by_text=[["It was a bright and sunny day."]],
            regenerate=regenerate,
        )

        self.assertEqual(paraphrases, [["The night was stormy."]])

    def test_paraphrase_is_generated_at_most_max_attempts_times(self):
        mis_filter = MISFilter(min_score=0.7, max_attempts=3)
        # Every attempt scores too low.
        mis_filter.score = lambda originals, paraphrases: [0.3 for _ in paraphrases]
        regenerate = MagicMock(return_value=["It was a bright and sunny day."])

        mis_filter.replace_low_scoring(
            originals=["It was a dark and stormy night."],
            paraphrases_by_text=[["It was a bright and sunny day."]],
            regenerate=regenerate,
        )

        # The first paraphrase counts as attempt one, so two more follow.
        self.assertEqual(regenerate.call_count, 2)


class TestMISFilterIntegration(unittest.TestCase):
    """MISFilter wired into Diversifier.

    AttemptMethod does not paraphrase: it appends the style and the
    number of the generate() call to the text, so each output shows in
    which attempt it was made.
    """

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
        # Only the first informal paraphrase scores below min_score (0.70).
        div._mis_filter.score = lambda originals, paraphrases: [
            0.4 if "(informal, attempt 1)" in p else 0.9 for p in paraphrases
        ]

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
        # Both first paraphrases score below min_score (0.70).
        div._mis_filter.score = lambda originals, paraphrases: [
            0.4 if "attempt 1" in p else 0.9 for p in paraphrases
        ]

        results = div.diversify(
            "It was a dark and stormy night.", styles=["formal", "informal"]
        )

        # Both are from attempt 2: one generate() call made both.
        self.assertEqual(
            results[0]["paraphrases"],
            [
                {"style": "formal", "text": "It was a dark and stormy night. (formal, attempt 2)"},
                {"style": "informal", "text": "It was a dark and stormy night. (informal, attempt 2)"},
            ],
        )

    def test_low_scoring_repeat_is_regenerated_in_its_style(self):
        div = Diversifier(method=AttemptMethod(), semantic_filter=True)
        # With repeats=2, attempt 1 is the first round of styles and
        # attempt 2 the second.  Only the second informal paraphrase
        # scores below min_score (0.70).
        div._mis_filter.score = lambda originals, paraphrases: [
            0.4 if "(informal, attempt 2)" in p else 0.9 for p in paraphrases
        ]

        results = div.diversify(
            "It was a dark and stormy night.", styles=["formal", "informal"], repeats=2
        )

        self.assertEqual(
            results[0]["paraphrases"][3],
            {"style": "informal", "text": "It was a dark and stormy night. (informal, attempt 3)"},
        )

    def test_low_scoring_texts_split_into_sentences_are_regenerated_whole(self):
        div = Diversifier(method=AttemptMethod(), semantic_filter=True)
        # The first paraphrase of both texts scores below min_score (0.70).
        div._mis_filter.score = lambda originals, paraphrases: [
            0.4 if "attempt 1" in p else 0.9 for p in paraphrases
        ]

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
