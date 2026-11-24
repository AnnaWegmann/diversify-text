Zero-shot
=========

The ``zero_shot`` method works like the :doc:`prompting` method: it
sends input texts to a causal language model with a prompt, and it uses
the same default model and the same ``model`` and ``precision`` options
(see :doc:`model_backend`).  The only difference is how the prompt
describes the target style: instead of example texts of the style, it
gives a rewrite *instruction*, such as "Here is a rewrite of the text,
which is more formal:".

.. note::

   This method is under construction.  Its instructions are a first
   set and will be replaced with prompts that have been shown to work
   in other work.

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
