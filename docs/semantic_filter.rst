.. _semantic-filter:

Semantic filter
===============

A paraphrase can lose or change part of what the original says.  With
``semantic_filter=True``, every paraphrase is generated several times
and checked against the original, and the attempt that keeps the
meaning is returned:

.. code-block:: python

   from diversify_text import diversify

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       semantic_filter=True,
   )

The result looks the same as without the filter: one paraphrase per
style.  The filter never removes a paraphrase, and the attempts are
compared within one style, so you get the same styles as without the
filter.

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
