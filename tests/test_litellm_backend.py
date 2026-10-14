"""Tests for querying proprietary models through their provider's API."""

import unittest
from unittest.mock import MagicMock, patch

from diversify_text.llm import LiteLLMBackend


def _reply(text: str) -> MagicMock:
    """A litellm completion response whose first choice says *text*."""
    response = MagicMock()
    response.choices[0].message.content = text
    return response


class TestLiteLLMBackend(unittest.TestCase):

    def test_load_logs_the_resolved_provider(self):
        with self.assertLogs("diversify_text.llm.litellm_backend", level="INFO") as logs:
            LiteLLMBackend("gpt-5-mini").load()
        self.assertEqual(
            logs.output,
            ["INFO:diversify_text.llm.litellm_backend:Querying 'gpt-5-mini' "
             "through the openai API."],
        )

    def test_unknown_model_name_raises(self):
        with self.assertRaises(ValueError) as cm:
            LiteLLMBackend("not-a-model-anyone-offers").load()
        self.assertEqual(
            str(cm.exception),
            "Model 'not-a-model-anyone-offers' was not found on the "
            "HuggingFace Hub and is not a model name litellm recognises. "
            "Pass a HuggingFace model id (e.g. 'Qwen/Qwen3-4B-Instruct-2507') "
            "or a provider model name (e.g. 'gpt-5-mini', "
            "'anthropic/claude-haiku-4-5', 'gemini/gemini-2.5-flash'). "
            "For a private HuggingFace repository, log in with "
            "`hf auth login` first.",
        )

    @patch("litellm.completion")
    def test_prompt_is_sent_as_one_user_message(self, mock_completion):
        mock_completion.return_value = _reply("The feline rested on the rug.")
        replies = LiteLLMBackend("gpt-5-mini").generate_text(
            ["Paraphrase: The cat sat on the mat."],
            max_new_tokens_per_prompt=[None],
            temperature=None,
            top_p=None,
        )
        self.assertEqual(
            mock_completion.call_args.kwargs["messages"],
            [{"role": "user", "content": "Paraphrase: The cat sat on the mat."}],
        )
        self.assertEqual(replies, ["The feline rested on the rug."])

    @patch("litellm.completion")
    def test_unset_parameters_are_left_to_the_provider(self, mock_completion):
        mock_completion.return_value = _reply("MOCK REPLY")
        LiteLLMBackend("gpt-5-mini").generate_text(
            ["Paraphrase: The cat sat on the mat."],
            max_new_tokens_per_prompt=[None],
            temperature=None,
            top_p=None,
        )
        sent = mock_completion.call_args.kwargs
        self.assertFalse({"max_tokens", "temperature", "top_p"} & sent.keys())

    @patch("litellm.completion")
    def test_explicit_parameters_are_forwarded(self, mock_completion):
        mock_completion.return_value = _reply("MOCK REPLY")
        LiteLLMBackend("gpt-5-mini").generate_text(
            ["Paraphrase: The cat sat on the mat."],
            max_new_tokens_per_prompt=[64],
            temperature=0.5,
            top_p=0.8,
        )
        sent = mock_completion.call_args.kwargs
        self.assertEqual(
            (sent["max_tokens"], sent["temperature"], sent["top_p"]),
            (64, 0.5, 0.8),
        )

    def test_no_default_output_cap(self):
        budgets = LiteLLMBackend("gpt-5-mini").default_token_budgets(
            ["The cat sat on the mat.", "It was a dark and stormy night."]
        )
        self.assertEqual(budgets, [None, None])


if __name__ == "__main__":
    unittest.main()
