"""Deterministic fallback diversification method."""

from __future__ import annotations

from typing import Any

from diversify_text.method.base import DiversificationMethod


class EchoMethod(DiversificationMethod):
    """Echoes the input text of every pair."""

    name = "echo"

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
        return [text for text, _ in pairs]
