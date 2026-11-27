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

The same question with the filter off and on, with the same seed:

.. code-block:: python

   text = "Where did you put the keys to the bike shed?"
   styles = ["informal", "formal", "gender_female"]

   without_filter = diversify(text, styles=styles, seed=1)
   with_filter = diversify(text, styles=styles, seed=1, semantic_filter=True)

Without the filter:

.. code-block:: python

   [{
       "original": "Where did you put the keys to the bike shed?",
       "paraphrases": [
           {"style": "informal", "text": "\"Yo, where'd you stash the bike shed keys?\""},
           {"style": "formal", "text": "Could you please inform me of the location of the keys to the bike shed?"},
           {"style": "gender_female", "text": "\"Ugh, where did I put the keys to the bike shed? I can't find them anywhere!\""},
       ]
   }]

With the filter:

.. code-block:: python

   [{
       "original": "Where did you put the keys to the bike shed?",
       "paraphrases": [
           {"style": "informal", "text": "\"Yo, where'd you stash the bike shed keys?\""},
           {"style": "formal", "text": "Could you please inform me of the location of the keys to the bike shed?"},
           {"style": "gender_female", "text": "Ugh, where did you put the keys to the bike shed?"},
       ]
   }]

The ``informal`` and ``formal`` paraphrases are the same.  Without the
filter, the ``gender_female`` paraphrase asks where *I* put the keys
and no longer where *you* put them.  It scored 0.15, below the
default ``min_score`` of 0.70.  With the filter it is replaced by
another attempt, which asks the original question and scored 0.90.

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

How the score treats different styles
-------------------------------------

The Mutual Implication Score is lower for some styles than for others,
also when a paraphrase keeps the meaning.  We paraphrased 17 short
texts (6 statements and 11 questions) into the first ten styles, with
the default model and the filter off:

.. list-table::
   :header-rows: 1
   :widths: 50 25 25

   * - Style
     - Average score
     - Below 0.70
   * - ``informal``
     - 0.89
     - 0 of 17
   * - ``age_child``
     - 0.87
     - 2 of 17
   * - ``formal``
     - 0.87
     - 1 of 17
   * - ``earlier_african_american_vernacular_english``
     - 0.86
     - 2 of 17
   * - ``gender_female``
     - 0.86
     - 1 of 17
   * - ``digital_communication``
     - 0.85
     - 2 of 17
   * - ``britneyspears``
     - 0.83
     - 2 of 17
   * - ``bahamian_creole``
     - 0.81
     - 3 of 17
   * - ``late_modern_english``
     - 0.78
     - 5 of 17
   * - ``lyrical``
     - 0.60
     - 10 of 17

The same sentence in three styles.  All three paraphrases keep the
date and the names of the parents, but the ``lyrical`` one scores far
below the default ``min_score`` of 0.70:

Original: "Stephen Hawking was born on 8 January 1942 to Frank and Isobel Hawking."

.. list-table::
   :header-rows: 1
   :widths: 22 66 12

   * - Style
     - Paraphrase
     - Score
   * - ``informal``
     - So, Stephen Hawking was born on January 8th, 1942, to Frank and Isobel Hawking.
     - 0.97
   * - ``late_modern_english``
     - It is a matter of record that Stephen Hawking came into the world on the eighth day of January in the year of our Lord nineteen forty-two, being the issue of Frank and Isobel Hawking.
     - 0.91
   * - ``lyrical``
     - Born on January eighth, nineteen forty-two, that's when Stephen Hawking came to light, / From Frank and Isobel, a pair of light.
     - 0.24

And a question that keeps its meaning in all three styles:

Original: "How long does it take to get from the airport to the city centre by bus?"

.. list-table::
   :header-rows: 1
   :widths: 22 66 12

   * - Style
     - Paraphrase
     - Score
   * - ``informal``
     - "so how long does it take to get from the airport to downtown by bus?"
     - 0.72
   * - ``lyrical``
     - Oh, the journey from the airport to the city's heart, / By bus, is that the path we gotta take? / How long will that ride take, I wonder, / For the city lights that we're gonna make.
     - 0.52
   * - ``late_modern_english``
     - How long doth the journey from the aerodrome to the heart of the city by omnibus require?
     - 0.41

With the filter on, such paraphrases are generated again although
they keep the meaning, and the new attempt can be plainer in style.

.. note::

   Asking a language model to judge whether a paraphrase keeps the
   meaning (an LLM as a judge) might work better for such styles.
   This is under construction.

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
