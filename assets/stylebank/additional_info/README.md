# Additional information

Files in this folder describe texts of the StyleBank. No script reads them, and they are not needed to build `stylebank.json`.

## `age_sources.json`

Where each text of the three age styles (`age_under-25`, `age_25-49`, `age_50-plus`) comes from. `stylebank.json` stores only the texts, so this file is the only record of which corpus and writer a text belongs to.

For each style it has one entry per text, in the same order as the texts in `stylebank.json`:

| Field       | Meaning                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `source`    | `Blog Authorship Corpus`, `PAN14 hotel reviews` or `Nguyen, Smith & Rosé (2011)`                          |
| `age`       | The writer's exact age (blogs, Nguyen) or age group (reviews, e.g. `35-49`, `65-plus`)                     |
| `gender`    | `female`, `male`, or `not given`                                                                          |
| `author_id` | The writer's id in the source corpus; for Nguyen, the kind of text and the page of the paper              |
| `begins`    | The first six words of the text, to match the entry to its text                                           |

Use it to trace a text back to its source, to remove the texts of a particular writer, or to check how the styles are balanced by source, age and gender. The sources themselves are described in `docs/age_examples.rst`.

If you change the texts of an age style in `stylebank.json`, change this file in the same way; nothing checks that the two still match.

## `child_sources.json`

Where each text of the `age_child` style comes from. It has one entry per text, in the same order as the texts in `stylebank.json`:

| Field    | Meaning                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------- |
| `source` | `UD-English-CHILDES`, `Frog stories (Berman & Slobin)` or `Growth in Grammar corpus (Durrant & Brenchley 2019)` |
| `age`    | The child's age in years;months, or the school year                                                        |
| `child`  | The child's name in the treebank, the child's letter in the frog stories, or `not given`                   |
| `id`     | The treebank's `sent_id` of the utterance, the frog-story code of the child, or the text number in the paper |
| `begins` | The first six words of the text, to match the entry to its text                                           |

If you change the texts of this style in `stylebank.json`, change this file in the same way; nothing checks that the two still match.
