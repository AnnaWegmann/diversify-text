Styles
======

Every paraphrase is the input text rewritten in one target style, and
each target style is defined by a set of example texts.  Pick styles
from a built-in bank, or define your own.

Each method has its own style bank, so which style names exist depends
on the method.  The examples on this page use the default method
(prompting) and its style bank; all banks are listed under
:ref:`available-styles` below.

Number of styles
----------------

``n`` sets how many styles are used (default 5).  They are the first
``n`` styles of the method's bank, in bank order, with one paraphrase
per style:

.. code-block:: python

   from diversify_text import diversify

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       n=3,
   )

Asking for more styles than the bank contains raises an error.

Pick styles by name
-------------------

Select built-in styles by name with ``styles``.  An unknown name raises
an error that lists the available ones:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       styles=["scottish_english", "informational"],
   )

A style can also be picked by its 0-based index in the bank.  Indices
follow bank order, which may change between releases, so names are the
stable way to pin a style.

Some styles are selectable by name only: they have no index and are
never picked by ``n``.  With the prompting method these are the
:ref:`unusual styles <unusual-styles>` (``old_english``,
``middle_english``), which are too far from contemporary English to be
useful defaults, and the :ref:`surface-level styles <surface-styles>`
(``all_caps``, ``passive_voice``, ...):

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       styles=["all_caps", "active_voice"],
   )

.. code-block:: python

   [{'original': 'The experiment was conducted in a controlled lab setting.',
     'paraphrases': [
       {'style': 'all_caps', 'text': 'THE EXPERIMENT TOOK PLACE IN A CONTROLLED LAB ENVIRONMENT.'},
       {'style': 'active_voice', 'text': 'The researchers conducted the experiment in a controlled lab setting.'}
     ]
   }]

Bring your own style examples
-----------------------------

Pass ``style_texts`` to define target styles with your own texts.  A
flat list is one style, a list of lists is several styles, and a dict
maps style names to example texts:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       style_texts={
           "academic": [
               "The results demonstrate a statistically significant effect.",
               "Participants were randomly assigned to one of two conditions.",
           ],
           "enthusiastic": [
               "We found something really interesting — check this out!",
               "You won't believe how well this worked!",
           ],
       },
   )

.. code-block:: python

   [{
       "original": "The experiment was conducted in a controlled lab setting.",
       "paraphrases": [
           {"style": "academic", "text": "The experiment was carried out under controlled laboratory conditions."},
           {"style": "enthusiastic", "text": "Guess what — we ran the whole experiment in a controlled lab, how cool is that!"},
       ]
   }]

``styles`` and ``style_texts`` can be combined in one call; the bank
styles come first in the output.  ``n`` cannot be combined with either,
because the number of styles is already given, so passing it raises an
error.

The prompting method puts at most the first 16 example texts of a style
into the prompt.  Change this with
``method_kwargs={"n_style_examples": 8}``.

Example texts longer than 500 words (such as the long prose excerpts in
the style bank) are cut after their first 500 words before they reach
the model.  Change the limit with ``max_len_style_text``, or pass
``max_len_style_text=None`` to keep full texts.  The zero-shot method
never cuts its instructions.

With the :doc:`zero_shot` method, ``style_texts`` are rewrite
instructions instead of example texts, exactly one per style.

Several paraphrases per style
-----------------------------

``repeats`` sets how many paraphrases are generated per style (default
1).  With more than one repeat, the styles take turns in the output:

.. code-block:: python

   results = diversify(
       "The experiment was conducted in a controlled lab setting.",
       styles=["scottish_english", "informational"],
       repeats=2,
   )

.. code-block:: python

   # order: scottish_english, informational, scottish_english, informational
   [{
       "original": "The experiment was conducted in a controlled lab setting.",
       "paraphrases": [
           {"style": "scottish_english", "text": "..."},
           {"style": "informational", "text": "..."},
           {"style": "scottish_english", "text": "..."},
           {"style": "informational", "text": "..."},
       ]
   }]

.. _available-styles:

Available styles
----------------

Every built-in style, by name.  To print the style names and the
examples of one style from Python:

.. code-block:: python

   from diversify_text.method.tinystyler import TinyStylerMethod
   from diversify_text.styles import DEFAULT_STYLE_BANK

   print(list(DEFAULT_STYLE_BANK))
   print(list(TinyStylerMethod.style_bank))
   print(DEFAULT_STYLE_BANK["scottish_english"][:3])

The listings below (with two example texts per style) are generated
from the code at every docs build.

Default style bank
^^^^^^^^^^^^^^^^^^

Used by the prompting method.  The example texts for these styles
(and for the unusual styles below) are in `stylebank.json
<https://github.com/AnnaWegmann/diversify_text/blob/main/diversify_text/styles/stylebank.json>`_.
Selectable via ``n``, by name, or by 0-based index.  The examples of
``gender_female`` and ``gender_male`` come from published studies; see
:doc:`gender_examples`.  The examples of the three age styles come
from blog posts and hotel reviews; see :doc:`age_examples`.
The examples of ``formal`` and ``informal`` come from the `STEL
<https://github.com/nlpsoc/STEL>`_ formality sample and the `TinyStyler
<https://github.com/zacharyhorvitz/TinyStyler>`_ repository.
The examples of ``age_child`` are speech and school writing of children
aged 4 to 7, from the CHILDES database and from Durrant & Brenchley
(2019).
The examples of ``barackobama`` are sentences and short passages from
three of Barack Obama's speeches, taken from the White House
transcripts: his final press conference and his farewell address (both
January 2017) and his speech at the 50th anniversary of the Selma
marches (March 2015).

.. include:: _generated/default_bank.inc

.. _unusual-styles:

Unusual styles
^^^^^^^^^^^^^^

Used by the prompting method.  Too far from contemporary English to be
useful defaults.  Selectable by name only.  Examples are in
`stylebank.json
<https://github.com/AnnaWegmann/diversify_text/blob/main/diversify_text/styles/stylebank.json>`_.

.. include:: _generated/default_unusual.inc

.. _surface-styles:

Surface-level styles
^^^^^^^^^^^^^^^^^^^^

Used by the prompting method.  Surface changes to the text, defined by
example texts.  The examples are in `surfacebank.json
<https://github.com/AnnaWegmann/diversify_text/blob/main/diversify_text/styles/surfacebank.json>`_.
Selectable by name only:

.. include:: _generated/surface_bank.inc

Zero-shot bank
^^^^^^^^^^^^^^

Used by the :doc:`zero_shot` method.  Each style is defined by one
rewrite *instruction* for the language model instead of example texts
(full text and sources on the :doc:`zero_shot_instructions` page).
Selectable via ``n``, by name, or by 0-based index.  The zero-shot
method has no name-only styles:

.. include:: _generated/zero_shot_bank.inc

TinyStyler bank
^^^^^^^^^^^^^^^

Used by the :doc:`tinystyler` method.  TinyStyler transfers formality and
social-media voice well, but not dialects, historical English, or most
genres, so it uses its own bank of styles it demonstrably handles
(selected by comparing model outputs for every style; see
``evaluations/tinystyler_style_ratings.txt`` in the repository).
The examples of ``formal``, ``informal`` and ``barackobama`` are the
ones in the default style bank; they have changed since that comparison
was made.

.. include:: _generated/tinystyler_bank.inc

By name only — these work but are more likely to produce swearing:

.. include:: _generated/tinystyler_unusual.inc

Of the surface-level styles, TinyStyler supports the following
(by name only):

.. include:: _generated/tinystyler_surface.inc

The default bank's unusual styles (``old_english``, ...) and its other
surface-level styles (``passive_voice``, ...) are not available with
TinyStyler.

.. toctree::
   :hidden:

   gender_examples
   age_examples
