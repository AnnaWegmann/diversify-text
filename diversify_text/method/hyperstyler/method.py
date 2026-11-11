"""HyperStyler-backed diversification method."""

from __future__ import annotations

import logging
from typing import Any

from diversify_text._utils import default_device
from diversify_text.method.base import DiversificationMethod
from diversify_text.method.hyperstyler.model import HyperStyler, _load_hyperstyler
from diversify_text.method.tinystyler.bank import (
    TINYSTYLER_STYLE_BANK,
    TINYSTYLER_SURFACE_STYLE_BANK,
    TINYSTYLER_UNUSUAL_STYLE_BANK,
)

logger = logging.getLogger(__name__)


class HyperStylerMethod(DiversificationMethod):
    """Diversification method backed by HyperStyler."""

    name = "hyperstyler"
    # HyperStyler builds on the same style embeddings as TinyStyler and
    # was also trained on Reddit, so it uses TinyStyler's banks.
    style_bank = TINYSTYLER_STYLE_BANK
    unusual_style_bank = TINYSTYLER_UNUSUAL_STYLE_BANK
    surface_style_bank = TINYSTYLER_SURFACE_STYLE_BANK

    def __init__(self, device: str | None = None) -> None:
        self.device = device
        self._model: HyperStyler | None = None

    def prepare(self) -> None:
        self._ensure_model()

    def _ensure_model(self) -> HyperStyler:
        """Fetch the shared model on first use."""
        if self._model is None:
            self._model = _load_hyperstyler(self.device or default_device())
        return self._model

    def generate(
        self,
        texts: list[str],
        style_dict: dict[str, list[str]],
        *,
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        **kwargs: Any,
    ) -> list[list[str]]:
        """Generate one paraphrase per style in *style_dict* for each text.

        Parameters
        ----------
        texts : list[str]
            Input texts to paraphrase.  HyperStyler reads at most 80
            tokens of each text; anything beyond that is cut off.
        style_dict : dict[str, list[str]]
            Maps each target style name to its example texts (as built
            by :func:`~diversify_text.styles.resolve_style_dict`).
        max_new_tokens, temperature, top_p
            Generation parameters; ``None`` uses the model's own
            defaults (80 new tokens, temperature 0.8, top_p 1.0).

        Returns
        -------
        list[list[str]]
            For each input text, one generated string per style, in
            *style_dict* order.
        """
        model = self._ensure_model()

        generation_kwargs = {
            name: value
            for name, value in (
                ("max_new_tokens", max_new_tokens),
                ("temperature", temperature),
                ("top_p", top_p),
            )
            if value is not None
        }

        paraphrases_per_text = [[] for _ in texts]

        for style_examples in style_dict.values():
            batch = model.transfer(texts, style_examples, **generation_kwargs)
            for row_idx, generated in enumerate(batch):
                paraphrases_per_text[row_idx].append(generated)
        return paraphrases_per_text
