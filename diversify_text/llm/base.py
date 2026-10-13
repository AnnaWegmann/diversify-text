"""Interface that every language model backend implements."""

from __future__ import annotations

from abc import ABC, abstractmethod

#: Placeholder in prompt texts where the input text is inserted.
PLACEHOLDER_TEXT = "[DOCUMENT SEGMENT]"


class LLMBackend(ABC):
    """One way of running prompts through a language model.

    The prompt-based methods (``prompting``, ``zero_shot``) build their
    prompts and hand them to a backend; the backend decides how the
    model is run.  Backends are loaded once and shared across methods
    (see :mod:`diversify_text._cache`).
    """

    @abstractmethod
    def load(self) -> None:
        """Make the model ready for generation (download, load into memory)."""

    @abstractmethod
    def token_budgets(self, texts: list[str]) -> list[int | None]:
        """Default ``max_new_tokens`` for each input text.

        Used when the caller does not set ``max_new_tokens``.  ``None``
        for a text means no cap.
        """

    @abstractmethod
    def generate_text(
        self,
        prompts: list[str],
        *,
        max_new_tokens_per_prompt: list[int | None],
        temperature: float | None,
        top_p: float | None,
    ) -> list[str]:
        """Generate one completion per prompt.

        Parameters
        ----------
        prompts : list[str]
            Prompts to generate completions for.
        max_new_tokens_per_prompt : list[int or None]
            Maximum tokens to generate for each prompt (same length
            as *prompts*); ``None`` means no cap.
        temperature, top_p
            Sampling parameters; ``None`` means the backend's default.
        """
