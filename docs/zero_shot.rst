Zero-shot
=========

The ``zero_shot`` method defines each style by a zero-shot rewrite
*instruction* with style labels instead of example texts. The method
sends one instruction per style to a causal language model (same
default model and options — ``model``, ``precision`` — as the
:doc:`prompting` method, see :doc:`model_backend`).

Its own style bank maps style names to instructions
(``ZeroShotMethod.style_bank``:
``formal``, ``simple``, ``complex``, ``caps``, ``lowercase``, and
more; the full text of every instruction is on the
:doc:`zero_shot_instructions` page). ``styles`` selects from these by
name or index, and ``n`` takes the first *n* styles of the bank in
order:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="zero_shot",
       styles=["formal", "caps"],
   )

With this method, ``style_texts`` are instructions — exactly one per
style. An instruction can place the input text itself with
``[DOCUMENT SEGMENT]``; otherwise the text is appended at the end:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       method="zero_shot",
       style_texts={"pirate": ["Rewrite the text as an old-timey pirate would say it."]},
   )

.. toctree::
   :hidden:

   zero_shot_instructions
