"""Shared base class for methods that generate from causal LMs."""

from __future__ import annotations

from diversify_text.llm import LLMBackend, load_backend
from diversify_text.method.base import DiversificationMethod

#: Default causal language model for prompt-based methods.
_DEFAULT_LLM = "HuggingFaceTB/SmolLM3-3B"

#: Placeholder in prompt texts where the input text is inserted.
PLACEHOLDER_TEXT = "[DOCUMENT SEGMENT]"


class CausalLMMethod(DiversificationMethod):
    """Shared base for methods that generate via a causal language model.

    Handles the model configuration and lazy loading; subclasses
    implement :meth:`generate` and hand their prompts to
    :meth:`_run_prompts`.
    """

    def __init__(
        self,
        model: str = _DEFAULT_LLM,
        device: str | None = None,
        precision: str | None = "auto",
    ) -> None:
        """Initialise the method.

        Parameters
        ----------
        model : str
            Model identifier; :func:`~diversify_text.llm.load_backend`
            decides which backend runs it: a HuggingFace model id runs
            locally, a provider model name (e.g. ``"gpt-5-mini"``,
            ``"anthropic/claude-haiku-4-5"``) is queried through the
            provider's API.
        device : str or None
            Torch device (e.g. ``"cpu"``, ``"mps"``, ``"cuda"``).
            Defaults to auto-detection via :func:`default_device`.
            Does not apply to API models.
        precision : str or None
            Model weight precision: ``"auto"`` (bfloat16), ``"float16"``,
            ``"bfloat16"``, or ``None`` (float32).  Does not apply to
            API models.
        """
        self.model_id = model
        self.device = device
        self.precision = precision
        self._backend: LLMBackend | None = None

    def prepare(self) -> None:
        """Load the backend for the configured model."""
        self._ensure_backend()

    @property
    def seedable(self) -> bool:
        """Whether a random seed affects the output; decided by the backend."""
        return self._ensure_backend().seedable

    def _ensure_backend(self) -> LLMBackend:
        """Fetch the shared backend on first use."""
        if self._backend is None:
            self._backend = load_backend(
                self.model_id, self.device, self.precision
            )
        return self._backend

    def _compute_max_new_tokens(
        self,
        texts: list[str],
        n: int,
        max_new_tokens: int | None,
    ) -> list[int | None]:
        """Compute per-prompt max_new_tokens for the full n × texts grid.

        When *max_new_tokens* is explicit, every prompt gets that value.
        Otherwise the backend chooses a default per text
        (:meth:`LLMBackend.default_token_budgets`).

        Returns a flat list of length ``n * len(texts)`` in the same
        order as the prompt loop: for each style index *i*, for each
        text *j*.
        """
        if max_new_tokens is not None:
            return [max_new_tokens] * (n * len(texts))
        budgets = self._ensure_backend().default_token_budgets(texts)
        return budgets * n

    def _run_prompts(
        self,
        all_prompts: list[str],
        texts: list[str],
        *,
        max_new_tokens: int | None,
        temperature: float | None,
        top_p: float | None,
    ) -> list[list[str]]:
        """Generate all prompts and reshape into one row per input text.

        *all_prompts* must be built style by style, texts within each
        style (so it holds ``n * len(texts)`` prompts for n styles).
        Computes per-prompt token budgets, generates (the backend
        fills in defaults for unset sampling parameters), and returns
        for each input text one string per style, in prompt order.
        """
        num_texts = len(texts)
        n = len(all_prompts) // num_texts
        all_max_new_tokens = self._compute_max_new_tokens(texts, n, max_new_tokens)
        backend = self._ensure_backend()

        # Generate one prompt at a time (each with its own max_new_tokens).
        flat_results = backend.generate_text(
            all_prompts,
            max_new_tokens_per_prompt=all_max_new_tokens,
            temperature=temperature,
            top_p=top_p,
        )

        # Reshape flat results back into list[list[str]] (len(texts) x n).
        paraphrases_per_text: list[list[str]] = [[] for _ in texts]
        for i in range(n):
            for row_idx in range(num_texts):
                # TODO: decide what to do with thinking models
                paraphrases_per_text[row_idx].append(
                    flat_results[i * num_texts + row_idx].strip()
                )
        return paraphrases_per_text
