Inputs and outputs
==================

``diversify`` takes a single text, a list of texts, any other iterable
of texts, or the path to a CSV, TSV or TXT file.  Texts given in Python
come back as a Python list; texts read from a file or an iterable are
written to a JSONL file.

Single text or list of texts
----------------------------

.. code-block:: python

   from diversify_text import diversify

   results = diversify(
       [
           "The experiment was conducted in a controlled lab setting.",
           "She graduated from MIT in 2019.",
       ],
   )

The result is a list with one entry per input text, in input order:

.. code-block:: python

   [
       {"original": "The experiment ...", "paraphrases": [{"style": "informal", "text": "..."}, ...]},
       {"original": "She graduated ...", "paraphrases": [{"style": "informal", "text": "..."}, ...]},
   ]

A single string gives a list with one entry.

CSV or TSV file
---------------

The texts are read from the column named by ``text_column`` (default
``"text"``); a file without that column raises an error.  The output is
written to ``<input>_diversified.jsonl`` next to the input file:

.. code-block:: python

   results = diversify("bios.csv", text_column="bio")
   # writes bios_diversified.jsonl and returns its path

A ``.tsv`` file works the same way, with tab-separated columns.

TXT file
--------

Each non-empty line is one text.  The output is written to
``<input>.jsonl`` next to the input file:

.. code-block:: python

   results = diversify("texts.txt")
   # writes texts.jsonl and returns its path

Other iterables
---------------

A generator or any other iterable of strings is read in batches, so
the texts never all have to be in memory.  The output is written to
``diversified_output.jsonl`` in the current working directory:

.. code-block:: python

   def read_texts():
       with open("corpus.txt") as f:
           for line in f:
               yield line.strip()

   results = diversify(read_texts())
   # writes ./diversified_output.jsonl and returns its path

JSONL output
------------

Each line of a JSONL output file holds the result for one input text,
in the same format as the entries of the Python list:

.. code-block:: json

   {"original": "Jane is a ...", "paraphrases": [{"style": "...", "text": "..."}]}
   {"original": "John studied ...", "paraphrases": [{"style": "...", "text": "..."}]}

When the output goes to a file, ``diversify`` returns the file's path
(a ``pathlib.Path``) instead of a list.

Choosing where the output goes
------------------------------

``output_dir`` sets the directory and ``output_name`` the file name.
The ``.jsonl`` extension is always added:

.. code-block:: python

   # Write to a specific directory
   results = diversify("bios.csv", text_column="bio", output_dir="/results")
   # writes /results/bios_diversified.jsonl

   # Also set the file name
   results = diversify("bios.csv", text_column="bio", output_dir="/results", output_name="bios_paraphrased")
   # writes /results/bios_paraphrased.jsonl

   # Write a list of texts to disk instead of returning a list
   results = diversify(["The cat sat on the mat.", "It was a dark and stormy night."], output_dir=".")
   # writes ./diversified_output.jsonl
