# First steps

<!-- The install instructions and the first examples live in README.md
     (between the install-start/install-end and
     quickstart-start/quickstart-end markers) so they are maintained in
     exactly one place. -->

## Installation

```{include} ../README.md
:start-after: <!-- install-start -->
:end-before: <!-- install-end -->
```

## First paraphrases

```{include} ../README.md
:start-after: <!-- quickstart-start -->
:end-before: <!-- quickstart-end -->
```

## Keeping the meaning of the original

A paraphrase can lose or change part of what the original says. With
`semantic_filter=True`, every paraphrase is checked against the
original, and a paraphrase that changed too much is generated again:

```python
results = diversify(
    "I required an alcoholic beverage after viewing the referenced subject.",
    semantic_filter=True,
)
```

See {doc}`semantic_filter` for how the check works and what it costs.
