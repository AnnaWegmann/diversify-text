"""Backend that queries a proprietary model through its provider's API.

Requests go through the ``litellm`` library, which supports OpenAI,
Anthropic, Google Gemini, Mistral and many other providers.  The
provider's API key is read from the environment (for example
``OPENAI_API_KEY``, ``ANTHROPIC_API_KEY``, ``GEMINI_API_KEY``).
"""

from __future__ import annotations

import logging
import time

from diversify_text.llm.base import LLMBackend

logger = logging.getLogger(__name__)

#: How often a request that failed for a transient reason (rate limit,
#: connection problem, timeout, server error) is retried before giving up.
#: Other failures, such as a wrong API key, are raised at once.
_API_RETRIES = 3


class LiteLLMBackend(LLMBackend):
    """Sends prompts to a provider's API through ``litellm``.

    Each prompt is sent as a single user message, exactly as it would
    be given to a local model.  Sampling parameters and the output
    length are only sent when set explicitly; otherwise the provider's
    defaults apply.  Requests that fail for a transient reason are
    retried ``_API_RETRIES`` times with increasing waits.
    """

    seedable = False  # the provider samples; a local seed has no effect

    def __init__(self, model_id: str) -> None:
        """Initialise the backend.

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
            _, provider, _, _ = litellm.get_llm_provider(self.model_id)
        except litellm.exceptions.BadRequestError as error:
            raise ValueError(unknown_model_message(self.model_id)) from error
        logger.info("Querying %r through the %s API.", self.model_id, provider)

    def default_token_budgets(self, texts: list[str]) -> list[None]:
        """No default output cap (``None`` per text): the provider's default applies."""
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
        results: list[str] = []
        for prompt, max_new_tokens in zip(prompts, max_new_tokens_per_prompt):
            request: dict = {}
            if max_new_tokens is not None:
                request["max_tokens"] = max_new_tokens
            if temperature is not None:
                request["temperature"] = temperature
            if top_p is not None:
                request["top_p"] = top_p
            results.append(self._complete(prompt, request))
        return results

    def _complete(self, prompt: str, request: dict) -> str:
        """Send one prompt, retrying transient failures."""
        import litellm

        transient_errors = (
            litellm.exceptions.RateLimitError,
            litellm.exceptions.APIConnectionError,
            litellm.exceptions.Timeout,
            litellm.exceptions.ServiceUnavailableError,
            litellm.exceptions.InternalServerError,
            litellm.exceptions.BadGatewayError,
        )
        for attempt in range(_API_RETRIES + 1):
            try:
                response = litellm.completion(
                    model=self.model_id,
                    messages=[{"role": "user", "content": prompt}],
                    **request,
                )
            except transient_errors as error:
                if attempt == _API_RETRIES:
                    raise
                wait = 2**attempt
                logger.warning(
                    "Request to %r failed (%s); retrying in %d s.",
                    self.model_id,
                    type(error).__name__,
                    wait,
                )
                time.sleep(wait)
            else:
                return response.choices[0].message.content or ""
        raise AssertionError("unreachable")


def unknown_model_message(model_id: str) -> str:
    """Error text for a model id that neither the Hub nor ``litellm`` knows."""
    return (
        f"Model {model_id!r} was not found on the HuggingFace Hub and is "
        "not a model name litellm recognises. Pass a HuggingFace model id "
        "(e.g. 'Qwen/Qwen3-4B-Instruct-2507') or a provider model name "
        "(e.g. 'gpt-5-mini', 'anthropic/claude-haiku-4-5', "
        "'gemini/gemini-2.5-flash'). For a private HuggingFace "
        "repository, log in with `hf auth login` first."
    )
