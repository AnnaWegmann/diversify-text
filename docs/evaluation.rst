Evaluating paraphrases
======================

Evaluation answers four questions about the paraphrases:

* **Content:** do they keep the meaning of the original?
* **Surface similarity:** how different is their wording from the
  original?  A paraphrase should usually say the same thing in other
  words.
* **Style:** does each paraphrase match its target style?  This
  applies to the styles in the built-in style bank.
* **Output diversity:** how different are the paraphrases of one text
  from each other?

How much each question matters depends on what you need the
paraphrases for.  If the goal is a set of different, creative or
diverse alternatives, rather than an exact imitation of a style, style
faithfulness matters less.

.. list-table::
   :header-rows: 1
   :widths: 22 28 50

   * - Question
     - Metrics
     - Preferred
   * - Content
     - ``bertscore``, ``mis``
     - Higher: more of the original's meaning is kept.
   * - Surface similarity
     - ``rouge``, ``bleu``, ``chrf``
     - Lower: fewer words and characters are shared with the original,
       so the text is rewritten instead of copied.
   * - Style
     - ``style_similarity``
     - Higher: closer to the example texts of the target style.
   * - Output diversity
     - Under construction
     - Higher: the paraphrases of one text differ more from each
       other.

Call ``.evaluate()`` on what ``diversify`` returned, or pass it to
``evaluate()``.  Both work the same, also when ``diversify`` wrote the
paraphrases to a file:

.. code-block:: python

   from diversify_text import diversify, evaluate

   results = diversify("The experiment was conducted in a controlled lab setting.")

   scores = results.evaluate()
   scores = evaluate(results)  # the same

   output = diversify("bios.csv", text_column="bio")
   scores = evaluate(output)

A file written earlier can also be passed by its name:
``evaluate("bios_diversified.jsonl")``.

Choosing metrics
----------------

All six metrics run by default.  Pick a subset with ``metrics``, and
configure single metrics with ``metric_kwargs``:

.. code-block:: python

   results.evaluate(
       metrics=["bertscore", "rouge"],
       metric_kwargs={
           "bertscore": {"model": "microsoft/deberta-xlarge-mnli"},
           "rouge": {"variants": ["rouge1", "rougeL"]},
       },
   )

Some metrics come in several versions, and each version is reported as
its own score.  ``variants`` picks which versions are reported.  The
sections below list the versions of each metric.

Content
-------

Two metrics score how much of the original's meaning a paraphrase
keeps.  Higher is better for both.

* ``bertscore`` compares the words of the two texts by their meaning
  in context, using the language model ``roberta-large``.  Choose
  another model with ``model``.  Versions: ``precision`` (how much of
  the paraphrase is found in the original), ``recall`` (how much of
  the original is found in the paraphrase) and ``f1`` (both combined).
  Default: ``f1``.
* ``mis``, the `Mutual Implication Score
  <https://huggingface.co/s-nlp/Mutual_Implication_Score>`_, scores
  whether each text implies the other.  It was tested for paraphrasing:
  in a large comparison of content scores, it agreed best with human
  judgments on paraphrase datasets, and as well as the best other
  scores on style transfer datasets (`Babakov et al., 2022
  <https://aclanthology.org/2022.acl-srw.23/>`_).  Its model is fixed.

Surface similarity
------------------

Three metrics count the words and characters a paraphrase shares with
its original.  They need no model.  Lower usually means the text was
rewritten rather than copied, but read them together with the content
scores: low surface similarity with low content scores usually means
the meaning was lost.

* ``rouge``: shared single words (``rouge1``), shared word pairs
  (``rouge2``), the longest shared word sequence (``rougeL``), and the
  same with every line treated as its own sentence (``rougeLsum``).
  Default: ``rouge1``, ``rouge2`` and ``rougeL``.
* ``bleu``: shared word sequences of up to four words, as one score.
* ``chrf``: shared character sequences (``chrf``), or shared character
  sequences plus shared words and word pairs (``chrf++``).  Default:
  ``chrf++``.

.. _style-similarity:

Style
-----

``style_similarity`` scores how close a paraphrase is to its target
style.  Higher is better.  It compares the paraphrase with the example
texts of its style in `stylebank.json
<https://github.com/AnnaWegmann/diversify_text/blob/main/diversify_text/styles/stylebank.json>`_
(the default and unusual styles), using the style embedding model
`AnnaWegmann/Style-Embedding
<https://huggingface.co/AnnaWegmann/Style-Embedding>`_, which
represents how a text is written rather than what it says.  All
examples of the style are turned into one reference, and the score is
how close the paraphrase is to it.

``pooling`` sets how the examples are combined into the reference:
``"mean"`` (default), ``"max"`` or ``"min"``.  ``model`` replaces the
embedding model with another `sentence-transformers
<https://sbert.net>`_ model:

.. code-block:: python

   results.evaluate(
       metric_kwargs={"style_similarity": {"pooling": "max"}},
   )

Paraphrases in a style that has no examples in ``stylebank.json``, such
as surface-level styles, zero-shot styles or your own ``style_texts``,
score ``None``, and averages leave them out.

Output diversity
----------------

Under construction.  No metric compares the paraphrases of one text
with each other yet.  Once one is added, a higher score will mean the
paraphrases differ more from each other.

Level of detail
---------------

By default, ``evaluate`` returns one average per score over all
paraphrases.  That is enough to compare, for example, two models or
methods on the same texts.  ``granularity`` gives more detail:

* ``"dataset"`` (default): one average per score over all paraphrases.
  Use it to compare settings.
* ``"text"``: one average per input text, over that text's
  paraphrases.  Use it if you care about a specific input text.
* ``"pair"``: one score for every paraphrase, next to its original and
  its style.  Use it to find single bad paraphrases.
* ``"all"``: all three.

Each level is an attribute of the result: ``scores.dataset``,
``scores.text`` and ``scores.pair``.  For example, for two texts with
two paraphrases each, scored with all default metrics.  The first text
gets two good paraphrases, the second two poor ones: an exact copy and
one that loses the meaning:

.. code-block:: python

   results = [
       {"original": "She missed the last train home, so she walked through the rain.",
        "paraphrases": [
            {"style": "scottish_english", "text": "She didnae catch the last train hame, so she had tae walk through the rain."},
            {"style": "informational", "text": "After missing the final train, she made her way home on foot in the rain."},
        ]},
       {"original": "The cat sat on the mat.",
        "paraphrases": [
            {"style": "scottish_english", "text": "The cat sat on the mat."},
            {"style": "informational", "text": "Dogs usually sleep in their baskets."},
        ]},
   ]

   scores = evaluate(results, granularity="all")

Scores rounded to two decimals, with the texts shortened:

.. code-block:: python

   scores.dataset
   {"style_similarity": 0.51, "bertscore_f1": 0.95, "rouge1": 0.53, "rouge2": 0.37,
    "rougeL": 0.51, "bleu": 36.14, "chrf++": 52.5, "mis": 0.71}

   scores.text
   [{"text_index": 0, "original": "She missed the last train ...", "n_paraphrases": 2,
     "style_similarity": 0.62, "bertscore_f1": 0.94, "rouge1": 0.56, "rouge2": 0.24,
     "rougeL": 0.52, "bleu": 18.99, "chrf++": 48.42, "mis": 0.94},
    {"text_index": 1, "original": "The cat sat ...", "n_paraphrases": 2,
     "style_similarity": 0.4, "bertscore_f1": 0.95, "rouge1": 0.5, "rouge2": 0.5,
     "rougeL": 0.5, "bleu": 53.28, "chrf++": 56.58, "mis": 0.48}]

   scores.pair
   [{"text_index": 0, "original": "She missed the last train ...",
     "style": "scottish_english", "paraphrase": "She didnae catch ...",
     "style_similarity": 0.67, "bertscore_f1": 0.94, "rouge1": 0.67, "rouge2": 0.4,
     "rougeL": 0.67, "bleu": 27.1, "chrf++": 63.71, "mis": 0.92},
    {"text_index": 0, "original": "She missed the last train ...",
     "style": "informational", "paraphrase": "After missing the final train ...",
     "style_similarity": 0.57, "bertscore_f1": 0.95, "rouge1": 0.44, "rouge2": 0.08,
     "rougeL": 0.37, "bleu": 10.88, "chrf++": 33.12, "mis": 0.96},
    {"text_index": 1, "original": "The cat sat ...",
     "style": "scottish_english", "paraphrase": "The cat sat on the mat.",
     "style_similarity": 0.35, "bertscore_f1": 1.0, "rouge1": 1.0, "rouge2": 1.0,
     "rougeL": 1.0, "bleu": 100.0, "chrf++": 100.0, "mis": 0.97},
    {"text_index": 1, "original": "The cat sat ...",
     "style": "informational", "paraphrase": "Dogs usually sleep ...",
     "style_similarity": 0.45, "bertscore_f1": 0.91, "rouge1": 0.0, "rouge2": 0.0,
     "rougeL": 0.0, "bleu": 6.57, "chrf++": 13.17, "mis": 0.0}]

``bleu`` and ``chrf++`` run from 0 to 100, the other scores from 0 to 1.

The dataset averages hide the problem.  The text level shows that the
second text loses meaning (``mis`` 0.48 against 0.94).  The pair level
shows why: one paraphrase is an exact copy (all surface scores at their
maximum) and so does not take on the Scottish style
(``style_similarity`` 0.35, against 0.67 for the real Scots
paraphrase); the other keeps none of the meaning (``mis`` 0.0).

Write the scores to a file with ``.to_jsonl(path)``:

.. code-block:: python

   scores = results.evaluate(granularity="pair")
   scores.to_jsonl("scores.jsonl")

Device
------

The metrics that use a model run on the CPU unless you pass
``device``:

.. code-block:: python

   results.evaluate(device="cuda")
