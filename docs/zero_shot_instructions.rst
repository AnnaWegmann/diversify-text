Instructions
============

The instructions of the :doc:`zero_shot` method's style bank, by style,
as defined in the code (``ZERO_SHOT_STYLE_BANK`` in
``diversify_text/method/zero_shot/bank.py``).  Select a style with
``styles=["<name>"]`` or by index.

.. include:: _generated/zero_shot_instructions.inc

Writing your own
----------------

An instruction is one string, passed via ``style_texts``.  It can place
the input text itself with ``[DOCUMENT SEGMENT]``; otherwise the text
is appended at the end, together with a request to output only the
rewrite.  For the input *The cat sat on the mat.*:

.. include:: _generated/zero_shot_example.inc
