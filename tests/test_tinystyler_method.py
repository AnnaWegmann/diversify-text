"""Tests for TinyStyler's generate()."""

import unittest
from unittest.mock import MagicMock

from diversify_text.method.tinystyler import TinyStylerMethod


def _method_with_mock_model() -> TinyStylerMethod:
    """TinyStylerMethod whose model echoes '<text>|<first style example>'."""
    method = TinyStylerMethod()
    mock_model = MagicMock()
    mock_model.transfer.side_effect = (
        lambda texts, style_examples, **kw: [
            f"{t}|{style_examples[0]}" for t in texts
        ]
    )
    method._model = mock_model
    return method


class TestGenerateFromPairs(unittest.TestCase):

    def test_one_output_per_pair_in_pair_order(self):
        method = _method_with_mock_model()
        # Explicit max_new_tokens skips the automatic token budget,
        # which would otherwise need the model's tokenizer.
        result = method.generate(
            [
                ("It was a dark and stormy night.", "casual"),
                ("Call me Ishmael.", "formal"),
                ("Call me Ishmael.", "casual"),
            ],
            {"casual": ["hey there"], "formal": ["Good day."]},
            max_new_tokens=32,
        )
        self.assertEqual(
            result,
            [
                "It was a dark and stormy night.|hey there",
                "Call me Ishmael.|Good day.",
                "Call me Ishmael.|hey there",
            ],
        )


if __name__ == "__main__":
    unittest.main()
