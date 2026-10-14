"""Language model backends.

An :class:`LLMBackend` runs prompts through a language model.  The
prompt-based methods (``prompting``, ``zero_shot``) build their prompts
and hand them to the backend returned by :func:`load_backend`.  Each
backend lives in its own module and knows nothing about the others:

* :mod:`~diversify_text.llm.transformers_backend` runs an open model
  locally with the ``transformers`` library.
"""

from __future__ import annotations

from diversify_text._cache import model_cache
from diversify_text.llm.base import LLMBackend
from diversify_text.llm.transformers_backend import TransformersBackend

__all__ = [
    "LLMBackend",
    "TransformersBackend",
    "load_backend",
]


@model_cache
def load_backend(
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
