# StyleBank

Code to build the **StyleBank**.

## Reproduction

### 1. Download the source files

Download the missing source files required by the individual corpus extraction scripts and place them in the appropriate corpus directories. Most source files are already included in the related directories (cf. `.gitignore`).

The required source files can be downloaded from the following resources:

| Corpus                                 | Source                                                                                                      |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Tweets Dataset (`tweets`)              | [Kaggle](https://www.kaggle.com/datasets/mmmarchetti/tweets-dataset/data)                                   |
| NPEGL (`korp`)                         | [Språkbanken](https://spraakbanken.gu.se/en/resources/npegl-eng)                                            |
| Middle English Corpus (`chaucer`)      | [GitHub](https://github.com/BenLambright/Middle-English-to-Modern-English-NMT)                              |
| eWAVE (`ewave`)                        | [GitHub](https://github.com/cldf-datasets/ewave/blob/master/cldf/examples.csv)                              |
| PASTEL (`pastel`)                      | [GitHub](https://github.com/dykang/PASTEL)                                                                  |
| CORE Corpus (`core`)                   | [GitHub](https://github.com/TurkuNLP/CORE-corpus)                                                           |
| This American Life Transcripts (`tal`) | [Kaggle](https://www.kaggle.com/datasets/shuyangli94/this-american-life-podcast-transcriptsalignments/data) |
| STEL formality sample (`stel`)         | [GitHub](https://github.com/nlpsoc/STEL/blob/main/Data/STEL/dimensions/quad_stel-dimension_formal-100_sample.tsv) |

### 2. Extract corpus samples

Run each individual `extract_[corpus]_sample.py` script to extract the required sample from each corpus.

For example:

```bash
python extract_ewave_sample.py
```

The resulting samples will be stored inside the corresponding `ewave` folder.

### 3. Create the StyleBank

Once all corpus samples have been generated, run:

```bash
python create_stylebank.py
```

This generates the first:

```text
stylebank.json
```

### 4. Changes after the first version.

We manually scanned, removed and edited the examples to make sure they are of high quality (i.e., no noise and representing the style in question).

We also made more additions: 

We run `XGENRE_lyrical_sample.py` extract ALL 78 lyrical/prose texts across train/dev/test from https://huggingface.co/datasets/TajaKuzmanPungersek/X-GENRE-text-genre-dataset. Then starting from the first example, we manually went through the generated json file to fill up the `lyrical` leaf to 13 (some lyrics had been removed in the manual edits). Additionally, we created the `prose` leaf and filled it up to 10 as well starting from the first of the 78 example texts going until 10 high quality samples had been added.


We replaced all texts of the `gender_female` and `gender_male` leaves, which came from PASTEL, with examples printed in published studies on how women and men write and speak. The sources of each text are listed in `docs/gender_examples.rst`.


We replaced the five PASTEL age leaves (`age_18-24`, `age_25-34`, `age_35-44`, `age_45-54`, `age_55-74`) with three broader ones (`age_under-25`, `age_25-49`, `age_50-plus`). Their texts are blog posts from the Blog Authorship Corpus, hotel reviews from the PAN14 author profiling corpus, and four examples printed in Nguyen, Smith & Rosé (2011). We drew random candidates (one text per author, 40-110 words for blogs, 40-130 words for reviews, no links, balanced by gender) and removed poems, quotations, lists, advertisements and texts not in standard English by hand. `additional_info/age_sources.json` lists the source, age, gender and author id of every text; `docs/age_examples.rst` describes the sources.


We added the `formal` leaf (36 sentences) and the `informal` leaf (64 sentences). `extract_stel_sample.py` reads the 100 formal/informal tasks of the STEL sample. Each task holds two sentence pairs, and a pair is the same content written once formally and once informally. The script keeps the pairs of the tasks on which at least 4 of 5 annotators agreed. From these pairs we picked sentences by hand. For `formal` we kept only sentences that read as formal on their own; most formal sentences in STEL are only formal next to their informal version ("How old are you?"). For `informal` we left out STEL sentences that read as standard English, and insults, jokes, lists and song lyrics. The `informal` leaf also holds 25 example sentences from `generation/target_styles/informal.txt` in the [TinyStyler repository](https://github.com/zacharyhorvitz/TinyStyler), which we kept as they are. In both leaves the texts that show the style most clearly come first, because the prompting method uses only the first 16 texts of a style.

We replaced the texts of the `barackobama` leaf. It held 59 tweets from the Tweets Dataset, but the account was run by staff, and many of its tweets speak about Obama in the third person, so they do not show how he writes or speaks. The leaf now holds 48 texts from three of his speeches, taken from the White House transcripts:

- 27 single sentences from the opening of his [final press conference](https://obamawhitehouse.archives.gov/the-press-office/2017/01/18/remarks-president-final-press-conference) (18 January 2017). These are the example sentences in `generation/target_styles/obama.txt` of the [TinyStyler repository](https://github.com/zacharyhorvitz/TinyStyler).
- 8 passages from the rest of that press conference, most of them from his answers to reporters' questions.
- 7 passages from his [farewell address](https://obamawhitehouse.archives.gov/the-press-office/2017/01/10/remarks-president-farewell-address) (10 January 2017).
- 6 passages from his speech at the [50th anniversary of the Selma marches](https://obamawhitehouse.archives.gov/the-press-office/2015/03/07/remarks-president-50th-anniversary-selma-montgomery-marches) (7 March 2015).

A passage is two to six consecutive sentences (24 to 105 words). We added passages because a single sentence often does not show a speaker's style. We picked them by hand from the first part of each transcript and left out exchanges with the audience, reporters' questions, long lists of names and quotations. "(Applause.)" notes are removed, "(Laughter.)" notes are kept, and curly quotation marks are replaced by straight ones. The leaf alternates between a passage and a single sentence, and the passages alternate between the three speeches, so its first texts cover all of them.

We added the `age_child` leaf with 61 texts by children aged 4 to 7, from three sources:

- 42 single utterances of speech at home, ages 4;0 to 5;2, from the [UD-English-CHILDES](https://github.com/UniversalDependencies/UD_English-CHILDES) treebank (children Abe, Adam, Laura, Roman and Sarah). The treebank holds single utterances that do not follow one another, so each text is one utterance (11 to 21 words); we picked the longer ones.
- 12 texts from the English [frog stories](https://talkbank.org/childes/topics/frogs.doc) in CHILDES (Berman & Slobin; recorded by Tanya Renner): four- and five-year-olds telling the story of a wordless picture book. Each text is a run of up to 12 consecutive clauses of one child. We removed the interviewer's turns, the transcription marks for stress and intonation and unclear stretches, kept the pauses ("..."), and wrote the first word of a sentence with a capital letter.
- 7 school texts by Year 2 pupils (ages 6 to 7) from the Growth in Grammar corpus, printed in the supplementary material of Durrant & Brenchley (2019). Their spelling was corrected by the authors. We removed the placeholder for a pupil's name ("Love from Personname.") from one text.

The leaf alternates between the three sources. The first 16 texts are 6 utterances, 5 frog-story texts and 5 school texts. `additional_info/child_sources.json` lists the source, age and child of every text.


### 5. Generate statistics (optional)

To generate statistics for the resulting StyleBank, run:

```bash
python stylebank_stats.py --input stylebank.json --output stylebank_stats.json
```

This produces:

```text
stylebank_stats.json
```

The file contains various statistics describing the StyleBank.