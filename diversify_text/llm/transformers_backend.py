"""Backend that runs an open model locally with the ``transformers`` library.

Loads the model with ``AutoModelForCausalLM`` (falling back to
``AutoModelForImageTextToText`` for multimodal wrapper configs) and
generates with its ``generate()`` API.

.. note:: vLLM support is planned for a future release.
"""

from __future__ import annotations

import logging

import torch
from huggingface_hub import snapshot_download

from diversify_text._utils import default_device, spinner, suppress_hf_load_noise
from diversify_text.llm.base import LLMBackend

logger = logging.getLogger(__name__)

_DEFAULT_TEMPERATURE = 0.7
_DEFAULT_TOP_P = 0.9
_MAX_NEW_TOKENS_FACTOR = 2.0
_MAX_NEW_TOKENS_FLOOR = 10
_MAX_NEW_TOKENS_CAP = 2048


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


class TransformersBackend(LLMBackend):
    """Runs a causal LM locally through ``transformers``."""

    def __init__(
        self,
        model_id: str,
        device: str | None = None,
        precision: str | None = "auto",
    ) -> None:
        """Initialise the backend.

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
        """Download and load the model."""
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
        ``max_new_tokens`` value.  Local generation always needs a
        cap, so every entry of *max_new_tokens_per_prompt* must be an
        integer (see :meth:`token_budgets` for the defaults).  Unset
        sampling parameters fall back to ``_DEFAULT_TEMPERATURE`` and
        ``_DEFAULT_TOP_P``.
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
        """Download weights (if needed) and load the model into memory."""
        from transformers import AutoTokenizer

        with spinner(f"Downloading {self.model_id}"):
            snapshot_download(self.model_id)
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
