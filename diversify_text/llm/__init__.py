"""Language model backends.

An :class:`LLMBackend` runs prompts through a language model.  The
prompt-based methods (``prompting``, ``zero_shot``) build their prompts
and hand them to the backend returned by :func:`load_backend`.  Each
backend lives in its own module and knows nothing about the others:

* :mod:`~diversify_text.llm.transformers_backend` runs an open model
  locally with the ``transformers`` library.
* :mod:`~diversify_text.llm.litellm_backend` queries a proprietary
  model through its provider's API with the ``litellm`` library.

Which backend runs a model follows from its id: an id found on the
HuggingFace Hub runs locally, anything else is treated as a provider
model name.
"""

from __future__ import annotations

import logging

from huggingface_hub import repo_exists

from diversify_text._cache import model_cache
from diversify_text._utils import default_device
from diversify_text.llm.base import LLMBackend
from diversify_text.llm.litellm_backend import LiteLLMBackend
from diversify_text.llm.transformers_backend import TransformersBackend

logger = logging.getLogger(__name__)

__all__ = [
    "LLMBackend",
    "LiteLLMBackend",
    "TransformersBackend",
    "load_backend",
]


def _is_on_hub(model_id: str) -> bool:
    """Whether the HuggingFace Hub has a model repository *model_id*.

    A metadata lookup, no download.  Gated repositories count as
    existing.  ``False`` when there is no such repository or the id is
    not a valid repository id.  When the Hub cannot be reached (for
    example offline), the id is assumed to be a Hub model, so cached
    models keep working.
    """
    from huggingface_hub.errors import HFValidationError

    try:
        return repo_exists(model_id)
    except HFValidationError:
        return False
    except Exception as error:  # no network, Hub down, ...
        logger.warning(
            "Could not reach the HuggingFace Hub (%s); assuming %r is a "
            "model there.",
            error,
            model_id,
        )
        return True


def load_backend(
    model_id: str,
    device: str | None = None,
    precision: str | None = "auto",
) -> LLMBackend:
    """Return the backend for a model (cached, shared across methods).

    A model id found on the HuggingFace Hub is run locally; any other
    id is treated as a provider model name and queried through the
    provider's API.  Defaults are filled in here, before the cache
    lookup, so one effective configuration maps to one cached backend.

    Parameters
    ----------
    model_id : str
        HuggingFace model identifier or provider model name.
    device : str or None
        Torch device for local models; ``None`` resolves to
        :func:`default_device`.
    precision : str or None
        Weight precision for local models; see
        :class:`TransformersBackend`.
    """
    return _load_backend(model_id, device or default_device(), precision)


@model_cache
def _load_backend(
    model_id: str,
    device: str,
    precision: str | None,
) -> LLMBackend:
    """Load the backend for a model (expensive, cached)."""
    if _is_on_hub(model_id):
        backend: LLMBackend = TransformersBackend(
            model_id=model_id, device=device, precision=precision
        )
    else:
        backend = LiteLLMBackend(model_id=model_id)
    backend.load()
    return backend
