"""Tests for HyperStyler's generate()."""

import unittest
from unittest.mock import MagicMock

from diversify_text.method.hyperstyler import HyperStylerMethod


class TestGenerateFromStyleDict(unittest.TestCase):

    def test_one_output_per_style_per_text_in_dict_order(self):
        method = HyperStylerMethod()
        # Stand-in model that returns '<text> -> <first style example>'.
        method._model = MagicMock()
        method._model.transfer.side_effect = (
            lambda texts, style_examples, **kw: [
                f"{text} -> {style_examples[0]}" for text in texts
            ]
        )
        result = method.generate(
            ["We should leave early.", "The meeting ran long."],
            {"informal": ["lol yeah same"], "formal": ["Kind regards."]},
        )
        self.assertEqual(
            result,
            [
                [
                    "We should leave early. -> lol yeah same",
                    "We should leave early. -> Kind regards.",
                ],
                [
                    "The meeting ran long. -> lol yeah same",
                    "The meeting ran long. -> Kind regards.",
                ],
            ],
        )


if __name__ == "__main__":
    unittest.main()
