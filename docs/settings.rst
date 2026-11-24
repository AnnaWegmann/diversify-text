Settings
========

Options that change how paraphrases are generated, how models are
loaded, and what gets logged.  Every option on this page is a keyword
argument of :func:`~diversify_text.diversify`.

Reproducibility (seed)
----------------------

The first ``diversify`` call in a Python session seeds Python's
``random``, PyTorch (CPU and CUDA) and NumPy with the default seed
``51173`` and logs it.  Later calls that do not pass ``seed`` are not
seeded again, so running the same call twice in one session gives
different paraphrases.

To seed every call, pass a seed explicitly; to get a different set of
paraphrases, pass a different one:

.. code-block:: python

   results = diversify("It was a dark and stormy night.", seed=123)

To turn seeding off, even on the first call:

.. code-block:: python

   results = diversify("It was a dark and stormy night.", seed=None)

Seeding makes runs more reproducible, but exact results are **not**
guaranteed across different hardware, library versions, or backends.
For proprietary models the provider does the sampling, so ``seed`` has
no effect; passing one logs a warning.

.. _output-length:

Output length
-------------

``max_new_tokens`` is the maximum number of tokens generated per
paraphrase.  When it is not set, each method picks a limit from the
length of the input:

* ``prompting`` and ``zero_shot`` with an open model: twice the length
  of each input text, at least 128 and at most 2048 tokens.
* ``tinystyler``: twice the length of the longest text in the batch,
  at least 10 and at most 256 tokens.
* Proprietary models: no limit, unless you set one.

.. code-block:: python

   results = diversify("It was a dark and stormy night.", max_new_tokens=64)

A paraphrase that reaches the limit is cut off mid-sentence.

Sampling
--------

``temperature`` and ``top_p`` control how much randomness goes into
sampling.  Open models and TinyStyler use ``temperature=0.7`` and
``top_p=0.9`` by default.  For proprietary models they are only sent
when you set them, so the provider's defaults apply otherwise.

.. code-block:: python

   results = diversify(
       "It was a dark and stormy night.",
       temperature=1.0,
       top_p=0.95,
   )

Device
------

``device`` sets the torch device the models run on (``"cuda"``,
``"mps"``, ``"cpu"``, ...).  By default the best available one is
used: ``"cuda"``, then ``"mps"``, then ``"cpu"``.  It does not apply to
proprietary models.

.. code-block:: python

   results = diversify("It was a dark and stormy night.", device="cpu")

Batch size
----------

``batch_size`` (default 32) is how many input texts are read at once.
For file inputs and other iterables, this bounds how many texts are in
memory at the same time.

Caching
-------

``diversify`` keeps loaded models in memory between calls, so only the
first call loads a model.  One model of each kind is kept: calling with
a different model replaces the cached one.  Call ``clear_cache()`` to
drop the cached models and let their memory be reclaimed:

.. code-block:: python

   from diversify_text import clear_cache

   clear_cache()

``clear_cache()`` also drops the models loaded by
:doc:`evaluate <evaluation>`.

Using the Diversifier class
---------------------------

``diversify`` creates a :class:`~diversify_text.Diversifier` for each
call.  You can also create one yourself and reuse it for several
batches with the same method and settings:

.. code-block:: python

   from diversify_text import Diversifier

   div = Diversifier(device="cuda")

   batch_1 = div.diversify(texts_1, styles=["scottish_english", "informational"])
   batch_2 = div.diversify(texts_2, style_texts=my_examples)

A ``Diversifier`` loads its models through the same cache as
``diversify``, so creating a second one with a different model replaces
the first one's model in the cache.

Seeing the prompts
------------------

To see the exact prompts sent to the model, turn on debug logging:

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)
