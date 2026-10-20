Prompt templates
================

The templates the :doc:`prompting` method fills and sends to the model,
as defined in the code (``PROMPT_BANK`` in
``diversify_text/method/prompting/prompts.py``).  ``[STYLE EXAMPLES]``
is replaced by the example texts of the target style, ``[STYLE NAME]``
by its name and ``[DOCUMENT SEGMENT]`` by the input text.  Select one
with ``method_kwargs={"prompt": "<key>"}``.

.. include:: _generated/prompt_bank.inc
