"""Shared language model backends for prompt-based methods.

:class:`CausalLMMethod` is the shared base class for methods that
generate from prompts.  It hands the prompts to one of two backends,
both of which expose the same ``generate_text`` interface:

* :class:`PromptingModel` runs an open model locally with the
  ``transformers`` library (``AutoModelForCausalLM``, with a fallback
  to ``AutoModelForImageTextToText`` for multimodal wrapper configs).
* :class:`ApiModel` queries a proprietary model through its provider's
  API with the ``litellm`` library.

Which backend is used follows from the model id: an id found on the
HuggingFace Hub runs locally, anything else is treated as a provider
model name (see :func:`_load_llm`).

.. note:: vLLM support is planned for a future release.
"""

from __future__ import annotations

import logging

import torch
from huggingface_hub import snapshot_download

from diversify_text._cache import model_cache
from diversify_text._utils import default_device, spinner, suppress_hf_load_noise
from diversify_text.method.base import DiversificationMethod

logger = logging.getLogger(__name__)

#: Default causal language model for prompt-based methods.
_DEFAULT_LLM = "HuggingFaceTB/SmolLM3-3B"
_DEFAULT_TEMPERATURE = 0.7
_DEFAULT_TOP_P = 0.9
_MAX_NEW_TOKENS_FACTOR = 2.0
_MAX_NEW_TOKENS_FLOOR = 10
_MAX_NEW_TOKENS_CAP = 2048
#: How often a failed API request is retried before giving up.
_API_RETRIES = 3


def _load_text_generation_model(model_id: str, **load_kwargs):
    """Load a model for text generation, whatever its config type.

    Multimodal wrapper configs (e.g. Ministral 3) might not be registered as
    causal LMs, so ``AutoModelForCausalLM`` rejects them; those load via
    the image-text class instead, which generates text the same way for
    text-only inputs.
    """
    from transformers import AutoModelForCausalLM

    try:
        return AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
    except ValueError as error:
        if "Unrecognized configuration class" not in str(error):
            raise
        from transformers import AutoModelForImageTextToText

        return AutoModelForImageTextToText.from_pretrained(
            model_id, **load_kwargs
        )


def _max_context_window(config) -> int | None:
    """Context window size from a model config, or ``None`` if unknown.

    Multimodal models keep the text settings in a sub-config;
    ``get_text_config()`` returns that (and the config itself for plain
    text models).
    """
    if hasattr(config, "get_text_config"):
        config = config.get_text_config()
    return getattr(config, "max_position_embeddings", None)


#: Placeholder in prompt texts where the input text is inserted.
PLACEHOLDER_TEXT = "[DOCUMENT SEGMENT]"


class PromptingModel:
    """Manages a causal LM for prompt-based generation."""

    def __init__(
        self,
        model_id: str,
        device: str | None = None,
        precision: str | None = "auto",
    ) -> None:
        """Initialise the model wrapper.

        Parameters
        ----------
        model_id : str
            HuggingFace model identifier.
        device : str or None
            Torch device. Defaults to auto-detection.
        precision : str or None
            Weight precision: ``"auto"`` (bfloat16), ``"float16"``,
            ``"bfloat16"``, or ``None`` (float32).
        """
        self.model_id = model_id
        self.device = device or default_device()
        self.precision = precision
        self._torch_dtype = self._resolve_dtype()
        self._tokenizer = None
        self._model = None

    def _resolve_dtype(self) -> torch.dtype | None:
        """Map *precision* string to a ``torch.dtype``.

        Returns
        -------
        torch.dtype or None
            The dtype to pass to ``from_pretrained``, or ``None``
            for full precision (float32).
        """
        if self.precision == "auto":
            return torch.bfloat16
        if self.precision is None:
            return None  # full precision (float32)
        mapping: dict[str, torch.dtype] = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
        }
        if self.precision not in mapping:
            raise ValueError(
                f"Unknown precision {self.precision!r}. "
                f"Choose from: 'auto', 'float16', 'bfloat16', or None (float32)"
            )
        return mapping[self.precision]

    def load(self) -> None:
        """Load the (already downloaded) model."""
        # TODO: add vLLM backend support in a future release.
        self._load_transformers()

    def token_budgets(self, texts: list[str]) -> list[int]:
        """Default ``max_new_tokens`` for each input text.

        Each text gets a budget scaled from its own token count
        (factor ``_MAX_NEW_TOKENS_FACTOR``, clamped between
        ``_MAX_NEW_TOKENS_FLOOR`` and ``_MAX_NEW_TOKENS_CAP``).
        """
        token_counts = [
            len(ids)
            for ids in self._tokenizer(texts, truncation=True)["input_ids"]
        ]
        # TODO: decide what to do with thinking models
        # if self._is_thinking_model:
        #     return [_MAX_NEW_TOKENS_CAP] * len(texts)
        return [
            max(
                _MAX_NEW_TOKENS_FLOOR,
                min(int(count * _MAX_NEW_TOKENS_FACTOR), _MAX_NEW_TOKENS_CAP),
            )
            for count in token_counts
        ]

    def generate_text(
        self,
        prompts: list[str],
        *,
        max_new_tokens_per_prompt: list[int | None],
        temperature: float | None,
        top_p: float | None,
    ) -> list[str]:
        """Generate completions for a list of prompts.

        Each prompt is processed individually with its own
        ``max_new_tokens`` value.

        Parameters
        ----------
        prompts : list[str]
            Prompts to generate completions for.
        max_new_tokens_per_prompt : list[int]
            Maximum tokens to generate for each prompt (same length
            as *prompts*).  Local generation always needs a budget;
            use :meth:`token_budgets` for the defaults.
        temperature, top_p
            Sampling parameters; ``None`` uses the defaults
            (``_DEFAULT_TEMPERATURE``, ``_DEFAULT_TOP_P``).
        """
        temperature = temperature if temperature is not None else _DEFAULT_TEMPERATURE
        top_p = top_p if top_p is not None else _DEFAULT_TOP_P
        # TODO: add batching and vLLM backend support in a future release.
        results: list[str] = []
        for prompt, max_new_tokens in zip(prompts, max_new_tokens_per_prompt):
            results.extend(
                self._generate_transformers(
                    [prompt],
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                )
            )
        return results

    def _load_transformers(self) -> None:
        """Load the model into memory."""
        from transformers import AutoTokenizer

        with spinner(f"Loading {self.model_id} (transformers, {self.device})"):
            with suppress_hf_load_noise():
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
                if self._tokenizer.pad_token is None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token
                self._tokenizer.padding_side = "left"  # required for decoder-only models
                load_kwargs: dict = {}
                if self._torch_dtype is not None:
                    load_kwargs["torch_dtype"] = self._torch_dtype
                self._model = _load_text_generation_model(
                    self.model_id, **load_kwargs
                )
                self._model.to(self.device)
                self._model.eval()
        # TODO: decide what to do with thinking models
        self._is_thinking_model = (
            hasattr(self._tokenizer, "chat_template")
            and self._tokenizer.chat_template is not None
            and "<think>" in self._tokenizer.chat_template
        )

    # -- vLLM backend ---------------------------------------------------------
    # TBD

    # -- transformers backend -------------------------------------------------

    def _generate_transformers(
        self,
        prompts: list[str],
        *,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
    ) -> list[str]:
        """Run batched generation via the transformers ``generate()`` API."""
        formatted = self._apply_chat_template(prompts)
        inputs = self._tokenizer(
            formatted, padding=True, return_tensors="pt", truncation=True
        ).to(self.device)
        input_len = inputs["input_ids"].shape[1]

        max_context = _max_context_window(self._model.config)
        if max_context is None:
            logger.warning(
                "Model %r does not expose 'max_position_embeddings' in "
                "its config; skipping the context window check.",
                self.model_id,
            )
        elif input_len > max_context:
            logger.warning(
                "Input length (%d tokens) exceeds model context window (%d). "
                "Output quality may degrade.",
                input_len,
                max_context,
            )

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
                pad_token_id=self._tokenizer.eos_token_id,
            )

        new_tokens = output_ids[:, input_len:]
        return self._tokenizer.batch_decode(new_tokens, skip_special_tokens=True)

    def _apply_chat_template(self, prompts: list[str]) -> list[str]:
        """Format prompts for instruct models when a chat template exists."""
        if (
            hasattr(self._tokenizer, "chat_template")
            and self._tokenizer.chat_template is not None
        ):
            conversations = [[{"role": "user", "content": p}] for p in prompts]
            # TODO: decide what to do with thinking models
            kwargs = {}
            if self._is_thinking_model:
                kwargs["enable_thinking"] = False
            return self._tokenizer.apply_chat_template(
                conversations,
                tokenize=False,
                add_generation_prompt=True,
                **kwargs,
            )
        return prompts


class ApiModel:
    """Queries a proprietary model through its provider's API.

    Requests go through the ``litellm`` library, which supports OpenAI,
    Anthropic, Google Gemini, Mistral and many other providers.  The
    provider's API key is read from the environment (for example
    ``OPENAI_API_KEY``, ``ANTHROPIC_API_KEY``, ``GEMINI_API_KEY``).

    Each prompt is sent as a single user message, exactly as it would
    be given to a local model.  Sampling parameters and the output
    length are only sent when set explicitly; otherwise the provider's
    defaults apply.  Failed requests are retried ``_API_RETRIES`` times.
    """

    def __init__(self, model_id: str) -> None:
        """Initialise the API model wrapper.

        Parameters
        ----------
        model_id : str
            Provider model name as ``litellm`` expects it, for example
            ``"gpt-5-mini"``, ``"anthropic/claude-haiku-4-5"`` or
            ``"gemini/gemini-2.5-flash"``.
        """
        self.model_id = model_id

    def load(self) -> None:
        """Check that ``litellm`` recognises the model name.

        Raises
        ------
        ValueError
            If the model name cannot be mapped to a provider.
        """
        import litellm

        litellm.suppress_debug_info = True  # no "Give Feedback" banner on errors
        try:
            litellm.get_llm_provider(self.model_id)
        except litellm.exceptions.BadRequestError as error:
            raise ValueError(_unknown_model_message(self.model_id)) from error
        logger.info("Using %r through its provider's API.", self.model_id)

    def token_budgets(self, texts: list[str]) -> list[None]:
        """No default output cap for API models (``None`` per text).

        The provider's default applies, so paraphrases are never cut
        short by an estimated budget.
        """
        return [None] * len(texts)

    def generate_text(
        self,
        prompts: list[str],
        *,
        max_new_tokens_per_prompt: list[int | None],
        temperature: float | None,
        top_p: float | None,
    ) -> list[str]:
        """Send each prompt to the provider and return the replies.

        Parameters
        ----------
        prompts : list[str]
            Prompts, each sent as one user message.
        max_new_tokens_per_prompt : list[int or None]
            Output cap per prompt; ``None`` leaves the provider default.
        temperature, top_p
            Sampling parameters; ``None`` leaves the provider default.
        """
        import litellm

        results: list[str] = []
        for prompt, max_new_tokens in zip(prompts, max_new_tokens_per_prompt):
            request: dict = {}
            if max_new_tokens is not None:
                request["max_tokens"] = max_new_tokens
            if temperature is not None:
                request["temperature"] = temperature
            if top_p is not None:
                request["top_p"] = top_p
            response = litellm.completion(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                num_retries=_API_RETRIES,
                **request,
            )
            results.append(response.choices[0].message.content or "")
        return results


def _unknown_model_message(model_id: str) -> str:
    return (
        f"Model {model_id!r} was not found on the HuggingFace Hub and is "
        "not a model name litellm recognises. Pass a HuggingFace model id "
        "(e.g. 'Qwen/Qwen3-4B-Instruct-2507') or a provider model name "
        "(e.g. 'gpt-5-mini', 'anthropic/claude-haiku-4-5', "
        "'gemini/gemini-2.5-flash'). For a private HuggingFace "
        "repository, log in with `hf auth login` first."
    )


def _is_on_hub(model_id: str) -> bool:
    """Download *model_id* from the HuggingFace Hub if it exists there.

    Returns ``False`` when the Hub has no repository with that id, or
    the id is not a valid repository id at all; the model is then
    treated as a provider model name.  Errors for gated repositories
    propagate.
    """
    from huggingface_hub.errors import HFValidationError, RepositoryNotFoundError

    try:
        with spinner(f"Fetching {model_id} from the HuggingFace Hub"):
            snapshot_download(model_id)
    except (RepositoryNotFoundError, HFValidationError):
        return False
    return True


@model_cache
def _load_llm(
    model_id: str,
    device: str,
    precision: str | None,
) -> PromptingModel | ApiModel:
    """Load a language model (cached, shared across methods).

    A model id found on the HuggingFace Hub is loaded locally; any
    other id is treated as a provider model name and queried through
    the provider's API, for which *device* and *precision* do not
    apply.
    """
    if _is_on_hub(model_id):
        llm = PromptingModel(model_id=model_id, device=device, precision=precision)
    else:
        logger.info(
            "%r is not on the HuggingFace Hub; treating it as a provider "
            "model name. The device and precision settings do not apply.",
            model_id,
        )
        llm = ApiModel(model_id=model_id)
    llm.load()
    return llm


class CausalLMMethod(DiversificationMethod):
    """Shared base for methods that generate via a language model.

    Handles the model configuration and lazy loading; subclasses
    implement :meth:`generate`.
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
            HuggingFace model identifier of an open model to run
            locally, or the name of a proprietary model to query
            through its provider's API (e.g. ``"gpt-5-mini"``,
            ``"anthropic/claude-haiku-4-5"``; see :class:`ApiModel`).
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
        self._model: PromptingModel | ApiModel | None = None

    def prepare(self) -> None:
        """Download and load the underlying language model."""
        self._ensure_model()

    def _ensure_model(self) -> PromptingModel | ApiModel:
        """Fetch the shared model on first use."""
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
        (``token_budgets``): a budget scaled from the text's token
        count for local models, no cap for API models.

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
