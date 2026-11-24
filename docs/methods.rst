Methods
=======

A method is the way the paraphrases are generated.  The package offers
two kinds: methods that prompt a general-purpose language model
(``prompting`` and ``zero_shot``), and models trained specifically for
style transfer (``tinystyler``).  Choose one with ``method=``.

.. note::

   The default, used when no ``method`` is given, is ``prompting``.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Method
     - Model size
     - Description
   * - ``prompting``
     - ~5B params (default), or an API model
     - Prompts a language model with example texts of the target style
   * - ``zero_shot``
     - ~5B params (default), or an API model
     - Prompts a language model with a rewrite instruction for the
       target style, instead of example texts
   * - ``tinystyler``
     - ~800M params
     - Model trained for style transfer; uses example texts of the
       target style

.. toctree::
   :maxdepth: 1

   prompting
   zero_shot
   tinystyler
