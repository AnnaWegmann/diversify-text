HyperStyler
===========

`HyperStyler <https://huggingface.co/JKSHINPG/HyperStyler>`_ is a T5-based
model that rewrites a text in the style of a few example texts. Like
:doc:`tinystyler`, it represents the example texts with
`CISR <https://huggingface.co/AnnaWegmann/Style-Embedding>`_ style embeddings.

.. code-block:: python

   from diversify_text import diversify

   diversify("I really think we should leave early tomorrow.", method="hyperstyler")

.. note::

   HyperStyler reads at most 80 tokens of each input text and writes at most
   80 tokens by default. Longer texts are cut off; see :doc:`longer_texts`
   for splitting a text on punctuation first.

.. warning::

   The model was trained on Reddit posts. Generated text may contain
   profanity, offensive, or discriminatory language.

**Loading.** The model's code is stored in its Hugging Face repository
rather than in the ``transformers`` library, so loading the model downloads
and runs that code (``trust_remote_code=True``). The weights are about
3.5 GB.

**Style bank.** HyperStyler uses the same style bank as TinyStyler; the
:doc:`styles` page lists the styles. The bank was selected by rating
TinyStyler's outputs, not HyperStyler's.

**Paper:** `HyperStyler: Low-resource Authorship Style Transfer via
Context-aware Style Navigation and Hypernetworks
<https://aclanthology.org/2026.emnlp-main.1045/>`_ (EMNLP 2026).
