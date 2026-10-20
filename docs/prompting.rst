Prompting
=========

The ``prompting`` method generates paraphrases by sending input texts to a
causal language model with a prompt template. The default model is
`HuggingFaceTB/SmolLM3-3B <https://huggingface.co/HuggingFaceTB/SmolLM3-3B>`_
using insights from `The Synthetic Data Playbook <https://huggingface.co/spaces/HuggingFaceFW/finephrase>`_;
any open or proprietary model can be used instead, see :doc:`model_backend`.

.. code-block:: python

   results = diversify("The cat sat on the mat.", method="prompting")

**Prompt templates.** All templates are example-based style transfer prompts:
the target style is demonstrated through example texts inserted into the
prompt. The default template is ``style_transfer``; ``humanize_transfer``
(inspired by `Zhang et al. (2024) <https://arxiv.org/abs/2401.05952>`_)
additionally instructs the model to imitate human imperfections found in
the style examples. The full text of every template is on the
:doc:`prompts` page. Select a template — or pass your own — via the
``prompt`` option:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="prompting",
       method_kwargs={"prompt": "humanize_transfer"},
   )

A custom template must contain both the ``[DOCUMENT SEGMENT]`` and
``[STYLE EXAMPLES]`` placeholders (``[STYLE NAME]`` is optional):

.. code-block:: python

   my_prompt = (
       "Study these examples:\n[STYLE EXAMPLES]\n"
       "Rewrite the following text in the same style. "
       "Text: [DOCUMENT SEGMENT]"
   )

   results = diversify(
       "The cat sat on the mat.",
       method="prompting",
       method_kwargs={"prompt": my_prompt},
   )

**Style examples.** The prompting method uses the default style bank,
loaded from ``stylebank.json``: styles organized in a
language-variation taxonomy — individual styles (idiolects) and
group-level variation across time (diachronic), region (diatopic),
social group (diastratic), register (diaphasic), and medium
(diamesic).  See :data:`diversify_text.styles.DEFAULT_STYLE_BANK` and
the :doc:`styles` page.  Select styles with the top-level ``styles``
parameter (or pass your own via ``style_texts``):

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="prompting",
       styles=["informational"],
   )

.. toctree::
   :hidden:

   prompts
