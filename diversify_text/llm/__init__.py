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

from huggingface_hub import snapshot_download

from diversify_text._cache import model_cache
from diversify_text._utils import spinner
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
    """Download *model_id* from the HuggingFace Hub if it exists there.

    Returns ``False`` when the Hub has no repository with that id, or
    the id is not a valid repository id at all.  Errors for gated
    repositories propagate.
    """
    from huggingface_hub.errors import HFValidationError, RepositoryNotFoundError

    try:
        with spinner(f"Fetching {model_id} from the HuggingFace Hub"):
            snapshot_download(model_id)
    except (RepositoryNotFoundError, HFValidationError):
        return False
    return True


@model_cache
def load_backend(
    model_id: str,
    device: str,
    precision: str | None,
) -> LLMBackend:
    """Load the backend for a model (cached, shared across methods).

    A model id found on the HuggingFace Hub is run locally; any other
    id is treated as a provider model name and queried through the
    provider's API, for which *device* and *precision* do not apply.
    """
    if _is_on_hub(model_id):
        backend: LLMBackend = TransformersBackend(
            model_id=model_id, device=device, precision=precision
        )
    else:
        logger.info(
            "%r is not on the HuggingFace Hub; treating it as a provider "
            "model name. The device and precision settings do not apply.",
            model_id,
        )
        backend = LiteLLMBackend(model_id=model_id)
    backend.load()
    return backend
