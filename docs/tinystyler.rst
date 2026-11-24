TinyStyler
==========

`TinyStyler <https://huggingface.co/tinystyler/tinystyler>`_ is a T5-based
model that performs few-shot text style transfer by conditioning on
authorship-embedding representations.

Given a source text and a set of style example sentences, TinyStyler generates
a paraphrase that preserves the content while shifting toward the demonstrated
writing style. ``diversify-text`` runs it once per target style to produce
multiple stylistically diverse outputs.

.. note::

   TinyStyler is one of several models trained specifically for style
   transfer that could be used here.  We intend to add more of them and
   compare how well they work.  So far, TinyStyler has been fast, with
   outputs of acceptable quality.

Select it with ``method="tinystyler"``:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="tinystyler",
   )

.. code-block:: python

   [{
       "original": "The experiment was conducted in a controlled lab setting.",
       "paraphrases": [
           {"style": "informal", "text": "yeah but the experiment was done in a controlled lab setting."},
           {"style": "formal", "text": "The experiment was conducted in a controlled lab setting, I believe."},
           {"style": "question", "text": "The experiment was conducted in a controlled lab setting? I don't see how this could be a problem."},
           {"style": "question_answer_forum", "text": "Isn't it just because the experiment was conducted in a controlled lab setting?"},
           {"style": "discussion_forum", "text": "I think it was done in a controlled lab setting. I'm not sure how the experiment went though, but"},
       ]
   }]

TinyStyler has a fixed model, so passing ``model`` with it raises an
error.

.. note::

   TinyStyler is based on `CISR <https://huggingface.co/AnnaWegmann/Style-Embedding>`_
   style embeddings, which have been shown to work well for **social-media-like
   settings** and **formality transfer**. The model may not perform as expected
   when reproducing other styles.

**Style bank.** TinyStyler has its own small bank of styles it
demonstrably handles (``informal``, ``formal``, ``question``, ...),
selected by running the model on every available style and comparing
outputs (``evaluations/tinystyler_style_ratings.txt`` in the
repository).  The examples of ``formal`` and ``informal`` are the ones
in the package's default style bank.  They have changed since the
comparison was made, so the ratings of these two styles were made with
other example texts.
A few additional styles work but are more likely to produce swearing;
they are selectable by name only.  The :doc:`styles` page lists all of
them, along with the default bank used by the prompting method.

**Citation:**

.. code-block:: bibtex

   @inproceedings{horvitz-etal-2024-tinystyler,
       title = "{T}iny{S}tyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings",
       author = "Horvitz, Zachary  and
         Patel, Ajay  and
         Singh, Kanishk  and
         Callison-Burch, Chris  and
         McKeown, Kathleen  and
         Yu, Zhou",
       editor = "Al-Onaizan, Yaser  and
         Bansal, Mohit  and
         Chen, Yun-Nung",
       booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
       month = nov,
       year = "2024",
       address = "Miami, Florida, USA",
       publisher = "Association for Computational Linguistics",
       url = "https://aclanthology.org/2024.findings-emnlp.781",
       pages = "13376--13390",
   }
