"""Tests for choosing the backend that runs a model."""

import unittest
from unittest.mock import patch

import diversify_text._cache as _cache
from diversify_text.llm import LiteLLMBackend, TransformersBackend, load_backend


class TestBackendSelection(unittest.TestCase):

    def setUp(self):
        _cache.clear_cache()

    @patch("diversify_text.llm.LiteLLMBackend.load")
    @patch("diversify_text.llm._is_on_hub", return_value=False)
    def test_model_not_on_hub_is_queried_through_the_api(self, _hub, _load):
        backend = load_backend("gpt-5-mini")
        self.assertIsInstance(backend, LiteLLMBackend)

    @patch("diversify_text.llm.TransformersBackend.load")
    @patch("diversify_text.llm._is_on_hub", return_value=True)
    def test_model_on_hub_runs_locally(self, _hub, _load):
        backend = load_backend("Qwen/Qwen3-4B-Instruct-2507")
        self.assertIsInstance(backend, TransformersBackend)


if __name__ == "__main__":
    unittest.main()
