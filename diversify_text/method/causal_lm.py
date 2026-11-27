"""Shared base class for methods that generate from causal LMs."""

from __future__ import annotations

from diversify_text.llm import LLMBackend, load_backend
from diversify_text.method.base import DiversificationMethod

#: Default causal language model for prompt-based methods.
_DEFAULT_LLM = "google/gemma-4-E2B-it"

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
        max_new_tokens: int | None,
    ) -> list[int | None]:
        """Compute max_new_tokens for each prompt.

        *texts* holds the input text of each prompt.  When
        *max_new_tokens* is explicit, every prompt gets that value.
        Otherwise the backend chooses a default per text
        (:meth:`LLMBackend.default_token_budgets`).
        """
        if max_new_tokens is not None:
            return [max_new_tokens] * len(texts)
        return self._ensure_backend().default_token_budgets(texts)

    def _run_prompts(
        self,
        all_prompts: list[str],
        texts: list[str],
        *,
        max_new_tokens: int | None,
        temperature: float | None,
        top_p: float | None,
    ) -> list[str]:
        """Generate one output per prompt.

        *texts* holds the input text of each prompt, in the order of
        *all_prompts*.  Computes per-prompt token budgets, generates
        (the backend fills in defaults for unset sampling parameters),
        and returns the outputs in prompt order.
        """
        all_max_new_tokens = self._compute_max_new_tokens(texts, max_new_tokens)
        backend = self._ensure_backend()

        # Generate all prompts (each with its own max_new_tokens).
        flat_results = backend.generate_text(
            all_prompts,
            max_new_tokens_per_prompt=all_max_new_tokens,
            temperature=temperature,
            top_p=top_p,
        )

        # TODO: decide what to do with thinking models
        return [result.strip() for result in flat_results]
