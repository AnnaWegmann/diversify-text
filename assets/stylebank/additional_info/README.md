

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
