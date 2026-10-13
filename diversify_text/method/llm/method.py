"""Shared base class for methods that generate from prompts."""

from __future__ import annotations

from diversify_text._cache import model_cache
from diversify_text._utils import default_device
from diversify_text.method.base import DiversificationMethod
from diversify_text.method.llm.base import LLMBackend
from diversify_text.method.llm.transformers_backend import TransformersBackend

#: Default causal language model for prompt-based methods.
_DEFAULT_LLM = "HuggingFaceTB/SmolLM3-3B"


@model_cache
def _load_llm(
    model_id: str,
    device: str,
    precision: str | None,
) -> LLMBackend:
    """Load the backend for a model (cached, shared across methods)."""
    backend = TransformersBackend(
        model_id=model_id, device=device, precision=precision
    )
    backend.load()
    return backend


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
            HuggingFace model identifier.
        device : str or None
            Torch device (e.g. ``"cpu"``, ``"mps"``, ``"cuda"``).
            Defaults to auto-detection via :func:`default_device`.
        precision : str or None
            Model weight precision: ``"auto"`` (bfloat16), ``"float16"``,
            ``"bfloat16"``, or ``None`` (float32).
        """
        self.model_id = model
        self.device = device
        self.precision = precision
        self._model: LLMBackend | None = None

    def prepare(self) -> None:
        """Download and load the underlying language model."""
        self._ensure_model()

    def _ensure_model(self) -> LLMBackend:
        """Fetch the shared backend on first use."""
        if self._model is None:
            self._model = _load_llm(
                self.model_id, self.device or default_device(), self.precision
            )
        return self._model

    def _compute_max_new_tokens(
        self,
        texts: list[str],
        n: int,
        max_new_tokens: int | None,
    ) -> list[int | None]:
        """Compute per-prompt max_new_tokens for the full n × texts grid.

        When *max_new_tokens* is explicit, every prompt gets that value.
        Otherwise the backend chooses a default per text
        (:meth:`LLMBackend.token_budgets`).

        Returns a flat list of length ``n * len(texts)`` in the same
        order as the prompt loop: for each style index *i*, for each
        text *j*.
        """
        if max_new_tokens is not None:
            return [max_new_tokens] * (n * len(texts))
        budgets = self._ensure_model().token_budgets(texts)
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
        model = self._ensure_model()

        # Generate one prompt at a time (each with its own max_new_tokens).
        flat_results = model.generate_text(
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
