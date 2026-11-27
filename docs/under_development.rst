Under development
=================

.. note::

   The features on this page are not part of the main use of
   ``diversify-text``.  They may change or be removed in a future
   release.

Longer texts
------------

``diversify`` is designed for **short texts**: single sentences or
short paragraphs.  For longer texts, there are two approaches: raising
the token limit and splitting on punctuation.

Raising ``max_new_tokens``
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default the output length is limited based on the input length (see
:ref:`output-length`).  You can raise the limit with
``max_new_tokens``.  The example below uses TinyStyler, whose limit is
at most 256 tokens:

.. code-block:: python

   from diversify_text import diversify

   results = diversify(
       "Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking. "
       "Despite their families' financial constraints, both parents attended "
       "the University of Oxford.",
       method="tinystyler",
       max_new_tokens=512,
   )

.. code-block:: python

   [{
       "original": "Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking. Despite their families' financial constraints, both parents attended the University of Oxford.",
       "paraphrases": [
           {"style": "informal", "text": "Frank and Isobel Hawking went to Oxford in 1942"},
           {"style": "formal", "text": "I believe Stephen Hawking was born on 8 January 1942."},
           {"style": "question", "text": "Is this true? Both parents went to Oxford and were born on 8 January 1942."},
           {"style": "question_answer_forum", "text": "Isn't it interesting that both parents attended Oxford? Stephen Hawking was born on 8 January 1942."},
           {"style": "discussion_forum", "text": "I think you are right, Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking. I think it was a lot of money for them to go to the University of Oxford."},
       ]
   }]

Note how information gets lost in several paraphrases.

.. warning::

   The models were not tested for long-form generation and may
   hallucinate, repeat themselves, or drift off-topic.

Splitting on punctuation
^^^^^^^^^^^^^^^^^^^^^^^^

Splitting on punctuation cuts each input into sentences, paraphrases
each sentence on its own (where the models work best), and joins the
results:

.. code-block:: python

   results = diversify(
       "Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking. "
       "Despite their families' financial constraints, both parents attended "
       "the University of Oxford.",
       method="tinystyler",
       preprocess_kwargs={"split_on_punctuation": True},
   )

.. code-block:: python

   [{
       "original": "Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking. Despite their families' financial constraints, both parents attended the University of Oxford.",
       "paraphrases": [
           {"style": "informal", "text": "i mean Stephen Hawking was born on 8 Jan 1942 to Frank and Isobel Hawking... both parents went to Oxford despite their families financial constraints."},
           {"style": "formal", "text": "Stephen Hawking was born 8 January 1942 to Frank and Isobel Hawking. I heard that both parents went to Oxford despite their families financial constraints."},
           {"style": "question", "text": "Did you know Stephen Hawking was born on 8 January 1942? His parents were Frank and Isobel Hawking. Is that true? Both parents went to Oxford despite their families financial constraints."},
           {"style": "question_answer_forum", "text": "Isn't Stephen Hawking born on 8 January 1942 to Frank and Isobel Hawking? Isn't it interesting that both parents went to Oxford despite their families financial constraints?"},
           {"style": "discussion_forum", "text": "I'm not sure if it is true, but Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking. I think it is interesting that both parents went to the University of Oxford despite their families financial constraints."},
       ]
   }]

The paraphrases keep more information than with a raised token limit
alone.  Both approaches can be combined: pass
``preprocess_kwargs={"split_on_punctuation": True}`` together with
``max_new_tokens``.

.. _creating-a-custom-method:

Creating a custom method
------------------------

A method is a subclass of
:class:`~diversify_text.method.base.DiversificationMethod` with a
``name`` and a ``generate`` method:

.. code-block:: python

   from diversify_text import Diversifier
   from diversify_text.method import DiversificationMethod


   class MyMethod(DiversificationMethod):
       name = "my_method"

       def generate(self, pairs, style_dict, *, max_new_tokens=None,
                    temperature=None, top_p=None, **kwargs):
           # pairs holds each text with the name of the style to write it in,
           # e.g. [("It was a dark and stormy night.", "scottish_english"), ...].
           # style_dict maps each target style name to its example texts,
           # e.g. {"scottish_english": ["The boat I had, was a seventy-two foot boat...", ...]}.
           return [f"{text} :: {name}" for text, name in pairs]


   results = Diversifier(method=MyMethod()).diversify(
       "It was a dark and stormy night.", styles=["scottish_english", "opinion"],
   )

.. code-block:: python

   [{"original": "It was a dark and stormy night.", "paraphrases": [
       {"style": "scottish_english", "text": "It was a dark and stormy night. :: scottish_english"},
       {"style": "opinion", "text": "It was a dark and stormy night. :: opinion"},
   ]}]

``generate`` receives ``pairs`` and ``style_dict``.  Each pair is an
input text together with the name of the style to write it in.  A text
can come with any number of the styles, so do not assume that every
text appears with every style.  ``style_dict`` maps each style name to
its example texts, built from the caller's ``styles`` and
``style_texts``; every style name in ``pairs`` is one of its keys.
``generate`` returns one generated string per
pair, in the order of ``pairs`` (a ``list[str]`` as long as
``pairs``).  The style labels are attached afterwards, and
``generate`` is called once per repeat, so a method does not need to
handle ``repeats``.

``max_new_tokens``, ``temperature`` and ``top_p`` are always passed as
keyword arguments, so ``generate`` must accept them, but it may ignore
them.  Anything the caller passes in ``method_kwargs`` arrives as extra
keyword arguments.

A method can also set these class attributes:

* ``style_bank``: the styles that ``n`` and ``styles`` select from
  (default: the default style bank).
* ``unusual_style_bank`` and ``surface_style_bank``: styles selectable
  by name only.  A method with its own ``style_bank`` usually sets these
  to ``{}``.
* ``seedable``: whether a seed affects the output (default ``True``);
  when ``False``, seeding is skipped.
* ``truncate_style_texts``: whether example texts are cut to
  ``max_len_style_text`` words (default ``True``).

To load models before generation starts, override ``prepare()``; it is
called once before the first ``generate``.
