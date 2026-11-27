"""TinyStyler-backed diversification method."""

from __future__ import annotations

import logging
from typing import Any

from diversify_text._utils import default_device
from diversify_text.method.base import DiversificationMethod
from diversify_text.method.tinystyler.bank import (
    TINYSTYLER_STYLE_BANK,
    TINYSTYLER_SURFACE_STYLE_BANK,
    TINYSTYLER_UNUSUAL_STYLE_BANK,
)
from diversify_text.method.tinystyler.model import TinyStyler, _load_tinystyler

logger = logging.getLogger(__name__)

_DEFAULT_TEMPERATURE = 0.7
_DEFAULT_TOP_P = 0.9
_MAX_NEW_TOKENS_FACTOR = 2.0
_MAX_NEW_TOKENS_FLOOR = 10
_MAX_NEW_TOKENS_CAP = 256


class TinyStylerMethod(DiversificationMethod):
    """Diversification method backed by TinyStyler."""

    name = "tinystyler"
    # TinyStyler uses its own banks — see tinystyler/bank.py for why.
    style_bank = TINYSTYLER_STYLE_BANK
    unusual_style_bank = TINYSTYLER_UNUSUAL_STYLE_BANK
    surface_style_bank = TINYSTYLER_SURFACE_STYLE_BANK

    def __init__(self, device: str | None = None) -> None:
        self.device = device
        self._model: TinyStyler | None = None

    def prepare(self) -> None:
        self._ensure_model()

    def _ensure_model(self) -> TinyStyler:
        """Fetch the shared model on first use."""
        if self._model is None:
            self._model = _load_tinystyler(self.device or default_device())
        return self._model

    def generate(
        self,
        pairs: list[tuple[str, str]],
        style_dict: dict[str, list[str]],
        *,
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        **kwargs: Any,
    ) -> list[str]:
        """Generate one paraphrase per (text, style name) pair.

        The model is run once per style, with all texts paired with
        that style.

        Parameters
        ----------
        pairs : list[tuple[str, str]]
            Each input text together with the name of the style to
            paraphrase it in.
        style_dict : dict[str, list[str]]
            Maps each target style name to its example texts (as built
            by :func:`~diversify_text.styles.resolve_style_dict`).
        max_new_tokens, temperature, top_p
            Generation parameters; ``None`` uses defaults.

        Returns
        -------
        list[str]
            One generated string per pair, in the order of *pairs*.
        """
        model = self._ensure_model()

        # Apply TinyStyler-specific defaults for parameters not set by
        # the caller.
        temperature = temperature if temperature is not None else _DEFAULT_TEMPERATURE
        top_p = top_p if top_p is not None else _DEFAULT_TOP_P

        # An explicit max_new_tokens is used as-is; otherwise scale with
        # the longest input, capped between _MAX_NEW_TOKENS_FLOOR and
        # _MAX_NEW_TOKENS_CAP.
        if max_new_tokens is None:
            input_token_counts = [
                len(ids)
                for ids in model._tokenizer(
                    [text for text, _ in pairs], truncation=True
                )["input_ids"]
            ]
            max_new_tokens = max(
                _MAX_NEW_TOKENS_FLOOR,
                min(
                    int(max(input_token_counts) * _MAX_NEW_TOKENS_FACTOR),
                    _MAX_NEW_TOKENS_CAP,
                ),
            )

        paraphrases: list[str] = [""] * len(pairs)

        for style in dict.fromkeys(style for _, style in pairs):
            pair_indices = [i for i, (_, s) in enumerate(pairs) if s == style]
            batch = model.transfer(
                [pairs[i][0] for i in pair_indices],
                style_dict[style],
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            for i, generated in zip(pair_indices, batch):
                paraphrases[i] = generated
        return paraphrases
