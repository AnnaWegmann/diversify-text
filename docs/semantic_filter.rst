.. _semantic-filter:

Semantic filter
===============

A paraphrase can deviate quite a lot from the original.  With
``semantic_filter=True``, every paraphrase is generated several times
and checked against the original, and the attempt that keeps the
meaning the most is returned:

.. code-block:: python

   from diversify_text import diversify

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       semantic_filter=True,
   )

The output looks the same as without the filter: one paraphrase per
style, it just runs a bit longer.  

Example
-------

The same text with the filter off and on.  Both calls use the same
seed, so they start from the same paraphrases:

.. code-block:: python

   text = "idk.....but i have faith in you lol"

   without_filter = diversify(text, seed=51173)
   with_filter = diversify(text, seed=51173, semantic_filter=True)

Without the filter:

.. code-block:: python

   [{
       "original": "idk.....but i have faith in you lol",
       "paraphrases": [
           {"style": "informal", "text": "i dunno... but i totally believe in you haha"},
           {"style": "formal", "text": "I have confidence in you."},
           {"style": "britneyspears", "text": "Sending you some serious good vibes! ✨ I totally have faith in you, girl! 💖💖"},
           {"style": "bahamian_creole", "text": "Mi dunno... but mi got faith in yuh, lol."},
           {"style": "late_modern_english", "text": "Alas, I confess I harbor a certain trust in your being."},
       ]
   }]

With the filter:

.. code-block:: python

   [{
       "original": "idk.....but i have faith in you lol",
       "paraphrases": [
           {"style": "informal", "text": "i dunno... but i totally believe in you haha"},
           {"style": "formal", "text": "I have confidence in you."},
           {"style": "britneyspears", "text": "\"Honestly, I totally have faith in you, you know? 😉\""},
           {"style": "bahamian_creole", "text": "Mi dunno... but mi got faith in yuh, lol."},
           {"style": "late_modern_english", "text": "Alas, I confess I harbor a certain trust in your being."},
       ]
   }]

Four of the five paraphrases are the same.  The ``britneyspears``
paraphrase without the filter starts with a sentence that is not in
the original, and scored 0.60, below the default ``min_score`` of
0.70.  With the filter it is replaced by another attempt, which scored
0.78.

What the filter does
--------------------

1. Every paraphrase is generated ``max_attempts`` times.
2. The first attempt gets a score between 0 and 1 from the
   `Mutual Implication Score <https://huggingface.co/s-nlp/Mutual_Implication_Score>`_
   model.  The score is high when the paraphrase and the original
   imply each other, that is, when they say the same thing.
3. If the first attempt scores at least ``min_score``, it is kept.
4. Otherwise the other attempts are scored too, and the attempt with
   the highest score is kept.  If none of them reaches ``min_score``,
   a warning is logged.

Settings
--------

Pass the settings of the filter in ``filter_kwargs``:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       semantic_filter=True,
       filter_kwargs={"min_score": 0.8, "max_attempts": 5},
   )

* ``min_score`` (default 0.70) is the score a paraphrase should reach.
  Raise it to keep more of the original's meaning.
* ``max_attempts`` (default 3) is how many times each paraphrase is
  generated.

With a :class:`~diversify_text.Diversifier`, pass the same arguments to
the constructor:
``Diversifier(semantic_filter=True, filter_kwargs={"min_score": 0.8})``.

Cost
----

All attempts are always generated, so generation takes
``max_attempts`` times as long as without the filter: styles ×
``repeats`` × ``max_attempts`` paraphrases per input text.  With a
proprietary model, that is also the number of requests to the provider.

The filter also loads the Mutual Implication Score model and scores
the attempts with it.

To see the scores of the paraphrases you got, use the ``mis`` metric
(see :doc:`evaluation`):

.. code-block:: python

   scores = results.evaluate(metrics=["mis"])
