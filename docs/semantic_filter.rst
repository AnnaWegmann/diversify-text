.. _semantic-filter:

Semantic filter
===============

A paraphrase can lose or change part of what the original says.  With
``semantic_filter=True``, every paraphrase is checked against the
original, and the ones that changed too much are generated again:

.. code-block:: python

   from diversify_text import diversify

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       semantic_filter=True,
   )

The result looks the same as without the filter: one paraphrase per
style.  The filter never removes a paraphrase, and a new attempt is
always written in the same style as the one it replaces, so you get
the same styles as without the filter.

What the filter does
--------------------

1. Every paraphrase gets a score between 0 and 1 from the
   `Mutual Implication Score <https://huggingface.co/s-nlp/Mutual_Implication_Score>`_
   model.  The score is high when the paraphrase and the original
   imply each other, that is, when they say the same thing.
2. A paraphrase that scores at least ``min_score`` is kept.
3. A paraphrase that scores below ``min_score`` is generated again and
   scored again.  This is repeated until an attempt reaches
   ``min_score`` or the paraphrase has been generated ``max_attempts``
   times.
4. If no attempt reaches ``min_score``, the attempt with the highest
   score is kept and a warning is logged.

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
  Raise it to keep more of the original's meaning; more paraphrases
  are then generated again.
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
