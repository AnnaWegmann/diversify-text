Open and proprietary LLMs
=========================

The ``prompting`` and ``zero_shot`` methods generate paraphrases with a
general-purpose language model: an open model that runs locally, or a
proprietary model queried through its provider's API (see
:ref:`api-models`).

Prompting
---------

The ``prompting`` method generates paraphrases by sending input texts to a
local HuggingFace causal language model with a prompt template. The default
model is `HuggingFaceTB/SmolLM3-3B <https://huggingface.co/HuggingFaceTB/SmolLM3-3B>`_
using insights from `The Synthetic Data Playbook <https://huggingface.co/spaces/HuggingFaceFW/finephrase>`_.

.. code-block:: python

   results = diversify("The cat sat on the mat.", method="prompting")

**Choosing a model.** Any HuggingFace causal LM can be used, as can a
proprietary model such as ``gpt-5-mini`` (see :ref:`api-models`). Pass
the model identifier directly to :func:`~diversify_text.diversify`:

.. code-block:: python

   results = diversify(
       "The cat sat on the mat.",
       method="prompting",
       model="Qwen/Qwen3-4B-Instruct-2507",
   )

or to the method constructor:

.. code-block:: python

   from diversify_text import Diversifier
   from diversify_text.method.prompting import PromptingMethod

   method = PromptingMethod(model="mistralai/Mistral-7B-Instruct-v0.3")
   results = Diversifier(method=method).diversify("The cat sat on the mat.")

``model`` works for the ``prompting`` and ``zero_shot`` methods. If no
method is given, passing ``model`` selects the ``prompting`` method.
The ``tinystyler`` method has a fixed model, so passing ``model`` with
it raises an error. See :ref:`which-model` below for insights into which models to use based on our practical experience.

Instruct-tuned models are recommended. Chat templates are applied automatically
when the tokenizer provides one.

.. note::

   Thinking/reasoning models (e.g. HuggingFaceTB/SmolLM3-3B) are detected automatically and
   have their thinking mode turned off (``enable_thinking=False``) during
   generation. Thinking tokens add overhead without improving paraphrase
   quality in this setting.

**Inference backend.** Open models run through the ``transformers``
library; proprietary models are queried through ``litellm``.

.. note::

   `vLLM <https://vllm.ai/>`_ support, batched inference, and streaming from
   large files are planned for a future release.

**Prompt templates.** All templates are example-based style transfer prompts:
the target style is demonstrated through example texts inserted into the
prompt; prompts without style examples are intentionally not supported. The
default template is ``style_transfer``; ``humanize_transfer`` (inspired by
`Zhang et al. (2024) <https://arxiv.org/abs/2401.05952>`_) additionally
instructs the model to imitate human imperfections found in the style
examples. Select a template — or pass your own — via the ``prompt`` option:

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

Zero-shot
---------

The ``zero_shot`` method defines each style by a rewrite *instruction*
instead of example texts, and sends one instruction per style to a
causal language model (same default model and options — ``model``,
``precision`` — as the prompting method).

Its own style bank maps style names to instructions
(``ZeroShotMethod.style_bank``:
``formal``, ``simple``, ``complex``, ``caps``, ``lowercase``, and
more), so ``styles`` and ``n`` select from these:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="zero_shot",
       styles=["formal", "caps"],
   )

With this method, ``style_texts`` are instructions — exactly one per
style. An instruction can place the input text itself with
``[DOCUMENT SEGMENT]``; otherwise the text is appended at the end:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="zero_shot",
       style_texts={"pirate": ["Rewrite the text as an old-timey pirate would say it."]},
   )

.. _api-models:

Proprietary models via API
--------------------------

Instead of a HuggingFace identifier, ``model`` can be the name of a
proprietary model. A name that is not on the HuggingFace Hub is sent to
the model's provider through the `litellm <https://docs.litellm.ai/docs/providers>`_
library, which supports OpenAI, Anthropic, Google Gemini, Mistral and
many more. The same prompts are used as for open models. Set the
provider's API key as an environment variable before running Python:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Provider
     - Environment variable
     - Model name, for example
   * - OpenAI
     - ``OPENAI_API_KEY``
     - ``gpt-5-mini``
   * - Anthropic
     - ``ANTHROPIC_API_KEY``
     - ``anthropic/claude-haiku-4-5``
   * - Google Gemini
     - ``GEMINI_API_KEY``
     - ``gemini/gemini-2.5-flash`` (not tested by us)

.. code-block:: bash

   export OPENAI_API_KEY="sk-..."

.. code-block:: python

   results = diversify(
       "The cat sat on the mat.",
       method="prompting",
       model="gpt-5-mini",
   )

Other providers and their name formats are listed in the
`litellm provider docs <https://docs.litellm.ai/docs/providers>`_. A
name that neither the HuggingFace Hub nor ``litellm`` recognises raises
an error that says so.

A few things work differently for API models:

* ``temperature``, ``top_p`` and ``max_new_tokens`` are only sent when
  you set them; otherwise the provider's defaults apply. In particular,
  there is no default output cap, so paraphrases are never cut short by
  an estimated budget.
* ``seed`` has no effect: the provider does the sampling. Passing one
  explicitly logs a warning.
* ``device`` and ``precision`` do not apply.
* Each paraphrase is one request to the provider, sent one after the
  other. Requests that fail for a transient reason (rate limit,
  connection problem, timeout, server error) are retried three times
  with increasing waits; other errors, such as a wrong API key, are
  raised at once.
* Keep an eye on cost: with ``n`` styles and ``repeats``, the number of
  requests is ``n * repeats`` per input text (times ``n_candidates``
  with the semantic filter on).

.. _which-model:

Which model?
------------

.. note::

    These notes are based on manually trying the models on a small set of sentences and styles, not a systematic evaluation.
    We tried well-known small models up to 5B, following the insight from `The Synthetic Data Playbook <https://huggingface.co/spaces/HuggingFaceFW/finephrase>`_ that small models are effective at paraphrasing tasks, and two small proprietary models through their API.
    Which model works best can change with your texts, styles, and hardware.


.. list-table::
   :header-rows: 1
   :widths: 30 12 58

   * - Model
     - Parameters
     - Notes
   * - `google/gemma-3-1b-it <https://huggingface.co/google/gemma-3-1b-it>`_
     - 1B
     - Fast, but unreliable. Invents content and does not rephrase the input at times.
   * - `HuggingFaceTB/SmolLM3-3B <https://huggingface.co/HuggingFaceTB/SmolLM3-3B>`_
     - 3B
     - The **default** because fastest. Quality ok-ish. Tends to add info that is not in the input. Sometimes starts replies with "Here\'s a paraphrased version of the document in the same style as the examples provided:"
   * - `mistralai/Ministral-3-3B-Instruct-2512 <https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512>`_
     - 3B
     - Outputs often contain commentary
       and formatting ("Here's a paraphrase: ..."). Not recommended.
   * - `Qwen/Qwen3-4B-Instruct-2507 <https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507>`_
     - 4B
     - Best 4B. Mostly faithful to the input and concise.
   * - `Qwen/Qwen3.5-4B <https://huggingface.co/Qwen/Qwen3.5-4B>`_
     - 4B
     - Similar to Qwen/Qwen3-4B-Instruct-2507. Occasionally repeats an
       emoji many times.
   * - `google/gemma-4-E2B-it <https://huggingface.co/google/gemma-4-E2B-it>`_
     - 5B
     - Best 5B. Best of tested **overall**. The most natural-sounding outputs. Some emoji repetitions happening though.
   * - ``gpt-5-mini`` (OpenAI API)
     - API
     - Faithful and concise on most styles. Pads short inputs with
       repetitions on some styles (``lyrical``, ``scottish_english``),
       and declines to imitate a named person's exact voice: the
       ``arianagrande`` output starts with a disclaimer before the
       paraphrase. About 5 s per paraphrase in our runs.
   * - ``anthropic/claude-haiku-4-5`` (Anthropic API)
     - API
     - Natural-sounding and faithful; on the ``informational`` style it
       added content that is not in the input. About 1 s per paraphrase
       in our runs.

For local models, generation speed depends mostly on model size:
producing a token requires reading all model weights from memory once,
so on the same machine, expect speed to scale roughly with one over the
parameter count. For API models it depends on the provider.

Some bank styles exceed what models of this size can do:
``old_english``, for example, produces Old-English-looking text with
much of the content lost, with every model above.

Example outputs
^^^^^^^^^^^^^^^

Outputs are shown as generated. The examples show how differently
the models behave.

``all_caps`` — input: *She graduated from MIT in 2019 and now works as
a data scientist.*

.. list-table::
   :widths: 25 75

   * - google/gemma-3-1b-it
     - “I CANNOT BELIEVE THIS IS HAPPENING RIGHT NOW!”
   * - HuggingFaceTB/SmolLM3-3B
     - THE WOMAN WHO CAME FROM MIT IN 2019 IS NOW A DATA SCIENTIST.
   * - mistralai/Ministral-3-3B-Instruct-2512
     - I DIDN'T EXPECT SHE WOULD GET THIS FAR IN HER CAREER SO
       QUICKLY—GRADUATING FROM MIT IN 2019 IS A MAJOR ACHIEVEMENT.
       NOW, AS A DATA SCIENTIST, SHE IS
   * - Qwen/Qwen3.5-4B
     - SHE GRADUATED FROM MIT IN 2019 AND NOW WORKS AS A DATA SCIENTIST.
   * - Qwen/Qwen3-4B-Instruct-2507
     - SHE GRADUATED FROM MIT IN 2019 AND NOW WORKS AS A DATA SCIENTIST.
   * - google/gemma-4-E2B-it
     - SHE GRADUATED FROM MIT IN TWO THOUSAND NINETEEN AND NOW WORKS AS
       A DATA SCIENTIST.
   * - gpt-5-mini
     - IN 2019 SHE EARNED HER DEGREE FROM MIT AND IS CURRENTLY EMPLOYED
       AS A DATA SCIENTIST.
   * - anthropic/claude-haiku-4-5
     - SHE COMPLETED HER DEGREE AT MIT BACK IN 2019 AND IS CURRENTLY
       EMPLOYED AS A DATA SCIENTIST.

``arianagrande`` (from the bank's individual-styles group) — input:
*I loved the movie, but the ending felt rushed.*

.. list-table::
   :widths: 25 75

   * - google/gemma-3-1b-it
     - “That movie was amazing! 😭 I really enjoyed it, but the ending felt a little bit too quick.
   * - HuggingFaceTB/SmolLM3-3B
     - OMG, I just watched that flick and it was so good, but the
       ending was like a roller coaster - too fast, too much. I was
       like "WTF, where's the drama?" But the whole movie was worth
       it! [...]
   * - mistralai/Ministral-3-3B-Instruct-2512
     - ☁️❤️❤️❤️❤️❤️ Ohhh, I *knew* this film was gonna steal my
       heart—until... well, that last act? *Whew.*
   * - Qwen/Qwen3.5-4B
     - i loved the movie but the ending felt so rushed 🌑🌑🌑🌑🌑
   * - Qwen/Qwen3-4B-Instruct-2507
     - omg i absolutely loved the movie 💛 but the ending? so fast 🙈
       like i didn't even get to breathe before it was over. 🌌
   * - google/gemma-4-E2B-it
     - omg the movie was fire 🔥 but the ending kinda rushed me 😩
   * - gpt-5-mini
     - Sorry—I can't write in Ariana Grande's exact voice, but I can
       write a paraphrase that captures her style:

       omg i loved the movie sooo much ✨ but the ending felt kinda
       rushed and i wanted more 💔
   * - anthropic/claude-haiku-4-5
     - omg the movie was sooo good but ngl that ending just felt like
       it went by way too fast 🌙 they coulda slowed it down a lil bit ♡

``scottish_english`` — input: *Could you send me the report before
Friday?*

.. list-table::
   :widths: 25 75

   * - google/gemma-3-1b-it
     - “Could ye send me that report afore Friday, please?”
   * - HuggingFaceTB/SmolLM3-3B
     - Ye'll want tae send me that report afore Friday, that's for sure.
   * - mistralai/Ministral-3-3B-Instruct-2512
     - The report's due by Friday afore. — Aye, I'll send it to you
       befo' Friday proper.
   * - Qwen/Qwen3.5-4B
     - Could you post the report to me before Friday?
   * - Qwen/Qwen3-4B-Instruct-2507
     - Could ye send me the report before Friday?
   * - google/gemma-4-E2B-it
     - Could ye send oot the report afore Friday?
   * - gpt-5-mini
     - Could ye send it tae me afore Friday?
   * - anthropic/claude-haiku-4-5
     - Could ye no send me yon report afore the Friday, like?

Development
-----------

To see the exact prompts sent to the model, enable debug logging:

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)
