"""Prompting-based diversification method."""

from __future__ import annotations

import logging
# import re  # TODO: decide what to do with thinking models
from typing import Any

from diversify_text.method.causal_lm import CausalLMMethod
from diversify_text.method.prompting.prompts import (
    DEFAULT_PROMPT,
    PLACEHOLDER_STYLE_EXAMPLES,
    PLACEHOLDER_STYLE_NAME,
    PLACEHOLDER_TEXT,
    PROMPT_BANK,
    REQUIRED_PLACEHOLDERS,
)

logger = logging.getLogger(__name__)

_DEFAULT_N_STYLE_EXAMPLES = 16


class PromptingMethod(CausalLMMethod):
    """Diversification method that prompts a causal LM for paraphrases."""

    name = "prompting"

    @staticmethod
    def _resolve_prompt(prompt: str | None = None) -> tuple[str, str]:
        """Resolve the *prompt* option into a single ``(key, template)`` pair.

        Exactly one template is active per call, and *prompt* selects
        which one:

        * ``None`` — use the default built-in template
          (:data:`DEFAULT_PROMPT`).
        * the name of a built-in template from :data:`PROMPT_BANK`
          (e.g. ``"humanize_transfer"``).
        * the full text of your own template (any string that is not a
          built-in name, recognised by containing placeholder tokens).
          It must contain **all** required placeholders
          (``[DOCUMENT SEGMENT]`` and ``[STYLE EXAMPLES]``);
          ``[STYLE NAME]`` is optional.  Unknown bracket tokens are left
          as literal text.

        Returns
        -------
        tuple[str, str]
            The ``(key, template)`` pair; custom templates get the key
            ``"custom"``.

        Raises
        ------
        ValueError
            If a custom template is missing required placeholders (the
            error names every missing one), or if *prompt* is neither a
            known key nor a template.
        """
        if prompt is None:
            return DEFAULT_PROMPT, PROMPT_BANK[DEFAULT_PROMPT]
        if prompt in PROMPT_BANK:
            return prompt, PROMPT_BANK[prompt]
        # A string containing any placeholder is a custom template.
        placeholders = (
            PLACEHOLDER_TEXT,
            PLACEHOLDER_STYLE_EXAMPLES,
            PLACEHOLDER_STYLE_NAME,
        )
        if any(p in prompt for p in placeholders):
            missing = [p for p in REQUIRED_PLACEHOLDERS if p not in prompt]
            if missing:
                raise ValueError(
                    "Custom prompt template is missing required "
                    f"placeholder(s): {', '.join(missing)}. Every template "
                    "must contain both "
                    f"{PLACEHOLDER_TEXT} and {PLACEHOLDER_STYLE_EXAMPLES} "
                    f"({PLACEHOLDER_STYLE_NAME} is optional)."
                )
            return "custom", prompt
        raise ValueError(
            f"Unknown prompt {prompt!r}. Available keys: "
            f"{sorted(PROMPT_BANK)}. To use your own template instead, pass "
            "a string containing the "
            f"{PLACEHOLDER_TEXT} and {PLACEHOLDER_STYLE_EXAMPLES} placeholders."
        )

    @staticmethod
    def _format_style_examples(
        examples: list[str],
        n: int = _DEFAULT_N_STYLE_EXAMPLES,
    ) -> str:
        """Format a style set into a bullet list for the prompt.

        Parameters
        ----------
        examples : list[str]
            Example sentences from a style set.
        n : int
            Maximum number of examples to include.

        Returns
        -------
        str
            Formatted string with one example per line.
        """
        selected = examples[:n]
        return "\n".join(f'- "{ex}"' for ex in selected)


    def _fill_template(
        self,
        template: str,
        text: str,
        style_name: str,
        style_examples: list[str],
        n_style_examples: int = _DEFAULT_N_STYLE_EXAMPLES,
    ) -> str:
        """Replace all placeholders in a template to produce a ready prompt.

        Parameters
        ----------
        template : str
            Prompt template containing ``[DOCUMENT SEGMENT]`` and
            ``[STYLE EXAMPLES]``, and optionally ``[STYLE NAME]``.
        text : str
            The input text to insert at ``[DOCUMENT SEGMENT]``.
        style_name : str
            Name of the target style, inserted at ``[STYLE NAME]``.
        style_examples : list[str]
            Example sentences of the target style, inserted at
            ``[STYLE EXAMPLES]``.
        n_style_examples : int
            Maximum number of example sentences to include.

        Returns
        -------
        str
            Fully filled prompt string, ready for generation.
        """
        # Style example placeholders (example-based templates).
        style_block = self._format_style_examples(
            style_examples, n=n_style_examples
        )
        template = template.replace(PLACEHOLDER_STYLE_EXAMPLES, style_block)

        # Style name placeholder (example-based and name-based templates).
        name = (
            style_name
            .replace("_tinystyler", "")
            .replace("_stel", "")
            .replace("_", " ")
        )
        template = template.replace(PLACEHOLDER_STYLE_NAME, name)

        # Document placeholder (all templates).
        template = template.replace(PLACEHOLDER_TEXT, text)
        return template

    def generate(
        self,
        pairs: list[tuple[str, str]],
        style_dict: dict[str, list[str]],
        *,
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        prompt: str | None = None,
        n_style_examples: int = _DEFAULT_N_STYLE_EXAMPLES,
        **kwargs: Any,
    ) -> list[str]:
        """Generate one paraphrase per (text, style name) pair.

        Parameters
        ----------
        pairs : list[tuple[str, str]]
            Each input text together with the name of the style to
            paraphrase it in.
        style_dict : dict[str, list[str]]
            Maps each target style name to its example texts (as built
            by :func:`~diversify_text.styles.resolve_style_dict`).
        max_new_tokens, temperature, top_p
            As in :meth:`generate`; ``None`` uses defaults.
        prompt : str or None
            Prompt selection, see :meth:`_resolve_prompt`.
        n_style_examples : int
            Maximum number of example texts inserted per prompt.

        Returns
        -------
        list[str]
            One generated string per pair, in the order of *pairs*.
        """
        prompt_key, prompt_template = self._resolve_prompt(prompt)
        logger.info(
            "Using prompt template %r for %d paraphrase(s).", prompt_key, len(pairs)
        )
        logger.info("Style sets: %s", ", ".join(style_dict.keys()))

        # TODO: accept texts as an Iterable (not just list) to support
        #       streaming from large files without materialising everything
        #       in memory.
        all_prompts = [
            self._fill_template(
                template=prompt_template,
                text=text,
                style_name=style,
                style_examples=style_dict[style],
                n_style_examples=n_style_examples,
            )
            for text, style in pairs
        ]

        return self._run_prompts(
            all_prompts,
            [text for text, _ in pairs],
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
        )
