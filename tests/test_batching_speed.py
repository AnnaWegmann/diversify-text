"""Speed of batched generation with a real model on a GPU.

Skipped by default, because it downloads model weights and needs a
CUDA GPU.  To run it::

    DIVERSIFY_TEST_SPEED=1 DIVERSIFY_TEST_DEVICE=cuda \
        python -m pytest tests/test_batching_speed.py -s

``-s`` shows the measured tokens per second.
"""

import os
import time
import unittest
from unittest.mock import patch

MODEL = "google/gemma-4-E2B-it"

RUN = (
    os.environ.get("DIVERSIFY_TEST_SPEED") == "1"
    and os.environ.get("DIVERSIFY_TEST_DEVICE", "cpu").startswith("cuda")
)

SENTENCES = [
    "It was a dark and stormy night; the rain fell in torrents.",
    "Call me Ishmael.",
    "All happy families are alike; each unhappy family is unhappy in its own way.",
    "It is a truth universally acknowledged, that a single man in possession "
    "of a good fortune, must be in want of a wife.",
    "The past is a foreign country; they do things differently there.",
    "In a hole in the ground there lived a hobbit.",
    "It was the best of times, it was the worst of times.",
    "Last night I dreamt I went to Manderley again.",
]


def tokens_per_second(backend, prompts):
    """Generate *prompts* and return the generated tokens per second."""
    start = time.perf_counter()
    outputs = backend.generate_text(
        prompts,
        max_new_tokens_per_prompt=[64] * len(prompts),
        temperature=None,
        top_p=None,
    )
    seconds = time.perf_counter() - start
    tokens = sum(len(ids) for ids in backend._tokenizer(outputs)["input_ids"])
    return tokens / seconds


@unittest.skipUnless(
    RUN, "set DIVERSIFY_TEST_SPEED=1 and DIVERSIFY_TEST_DEVICE=cuda to run"
)
class TestBatchingSpeed(unittest.TestCase):
    def test_batches_generate_faster_than_single_prompts(self):
        from diversify_text.llm import load_backend

        backend = load_backend(MODEL, os.environ["DIVERSIFY_TEST_DEVICE"])
        prompts = [
            f"Rewrite this sentence in {style} English: {sentence}"
            for style in ("formal", "casual")
            for sentence in SENTENCES
        ]
        # The first generation on a GPU is slow, so it is not timed.
        tokens_per_second(backend, prompts[:1])

        with patch("diversify_text.llm.transformers_backend._BATCH_SIZE", 1):
            single = tokens_per_second(backend, prompts)
        batched = tokens_per_second(backend, prompts)

        print(
            f"\none prompt at a time: {single:.0f} tokens/s, "
            f"in batches: {batched:.0f} tokens/s ({batched / single:.1f}x)"
        )
        self.assertGreater(batched, single)
