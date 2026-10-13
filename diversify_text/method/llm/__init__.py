"""Language model backends shared by the prompt-based methods.

:class:`CausalLMMethod` is the base class of the ``prompting`` and
``zero_shot`` methods.  It builds nothing itself: subclasses produce
prompts, and an :class:`LLMBackend` runs them.  Each backend lives in
its own module and knows nothing about the others:

* :mod:`~diversify_text.method.llm.transformers_backend` runs an open
  model locally with the ``transformers`` library.
"""

from diversify_text.method.llm.base import PLACEHOLDER_TEXT, LLMBackend
from diversify_text.method.llm.method import CausalLMMethod
from diversify_text.method.llm.transformers_backend import TransformersBackend

__all__ = [
    "CausalLMMethod",
    "LLMBackend",
    "PLACEHOLDER_TEXT",
    "TransformersBackend",
]
