"""
HyperStyler wrapper module for text style transfer.

Provides a small interface around the HyperStyler model
(https://huggingface.co/JKSHINPG/HyperStyler) for batched
style-transfer generation.
"""

from __future__ import annotations

import logging
from typing import Any

from transformers import AutoModel

from diversify_text._cache import model_cache
from diversify_text._utils import default_device, spinner, suppress_hf_load_noise

logger = logging.getLogger(__name__)

_REPO_ID = "JKSHINPG/HyperStyler"


class HyperStyler:
    """Loads the HyperStyler model and exposes its style transfer."""

    def __init__(self, device: str | None = None) -> None:
        self.device = device or default_device()
        self._model = self._load_model()

    def transfer(
        self,
        texts: list[str],
        style_examples: list[str],
        **generation_kwargs: Any,
    ) -> list[str]:
        """Rewrite each text in the style of *style_examples*.

        *generation_kwargs* (``max_new_tokens``, ``temperature``,
        ``top_p``) are passed on to the model; anything left out uses
        the model's own default.
        """
        with suppress_hf_load_noise():
            return self._model.transfer(texts, style_examples, **generation_kwargs)

    def _load_model(self):
        # The model class lives in the Hugging Face repository, not in
        # the transformers library, so loading it runs code from there.
        with spinner(f"Loading HyperStyler ({self.device})"):
            with suppress_hf_load_noise():
                model = AutoModel.from_pretrained(_REPO_ID, trust_remote_code=True)
                return model.to(self.device).eval()


@model_cache
def _load_hyperstyler(device: str) -> HyperStyler:
    """Load the HyperStyler model (cached, shared across method instances)."""
    return HyperStyler(device=device)
