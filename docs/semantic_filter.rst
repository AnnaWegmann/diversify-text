.. _semantic-filter:

Semantic filter
===============

A paraphrase can deviate quite a lot from the original.  With
``semantic_filter=True``, every paraphrase is checked against the
original, and a paraphrase that deviates too much is generated again:

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

1. Every paraphrase gets a score between 0 and 1 from the
   `Mutual Implication Score <https://huggingface.co/s-nlp/Mutual_Implication_Score>`_
   model.  The score is high when the paraphrase and the original
   imply each other, that is, when they say the same thing.
2. A paraphrase that scores at least ``min_score`` is kept.
3. A paraphrase that scores below ``min_score`` is generated again, in
   the same style, and scored again.  This is repeated until an
   attempt reaches ``min_score`` or the paraphrase has been generated
   ``max_attempts`` times.
4. If no attempt reaches ``min_score``, the attempt with the highest
   score is kept and a warning is logged.

.. note::

   The Mutual Implication Score may not work well for styles that are
   very different from the original.  It can give a low score to a
   paraphrase that keeps the meaning, for example in
   ``late_modern_english``.  Asking a language model to judge whether
   a paraphrase keeps the meaning (an LLM as a judge) might work better
   for such styles.  This is under construction.

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
* ``max_attempts`` (default 3) is how many times a paraphrase is
  generated at most, counting the first time.  With the default, a
  paraphrase that scores too low gets up to two new attempts.

With a :class:`~diversify_text.Diversifier`, pass the same arguments to
the constructor:
``Diversifier(semantic_filter=True, filter_kwargs={"min_score": 0.8})``.

Cost
----

A paraphrase that reaches ``min_score`` on the first attempt is
generated once, as without the filter.  Only the paraphrases that score
too low are generated again, so the extra generation depends on how
often that happens.  At most, every paraphrase is generated
``max_attempts`` times.  With a proprietary model, each new attempt is
one more request to the provider.

The filter also loads the Mutual Implication Score model and scores
every attempt with it.

To see the scores of the paraphrases you got, use the ``mis`` metric
(see :doc:`evaluation`):

.. code-block:: python

   scores = results.evaluate(metrics=["mis"])
