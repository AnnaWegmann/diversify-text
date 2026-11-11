Sources of the gender examples
==============================

The example texts of the styles ``gender_female`` and ``gender_male``
are taken from published studies on how women and men write and speak.
All other styles of the default style bank come from corpora; these
are listed in the `style bank README
<https://github.com/AnnaWegmann/diversify_text/blob/main/diversify_text/styles/README.md>`_.

The examples are about style only: how people write or speak, not what
they write about.  Every text was checked against the full text of the
source at the stated location.  Page numbers are the journal's printed
pages unless marked "preprint".

The texts are copied as printed in the source.  This includes spelling
mistakes and the marks used in the transcripts of speech: ``/`` and
``//`` for pauses in Holmes; ``.``, ``(.)``, ``-`` and ``(-)`` for
pauses, ``#`` and ``=`` in Coates.  Marks printed above a word to show
the rise or fall of the voice are left out.

``gender_female`` has 32 texts and ``gender_male`` has 20.  The
prompting method uses the first 16 texts of a style.  The texts are
stored so that the sources take turns, and the first 16 texts of each
style contain texts from every source of that style.

Limitations
-----------

The two styles are a small, hand-picked set of examples, not a sample
of how women and men write.  Keep the following in mind when you use
them:

- **Different kinds of text are mixed.**  Each style contains student
  essays, academic articles, novel openings, transcribed speech, tweets
  and restaurant reviews.  A rewrite in one of these styles may pick up
  the kind of text as much as anything related to gender.
- **The two styles are not built from the same material.**  The
  conversation turns from Coates (14 texts) exist only for women, so
  ``gender_female`` contains much more transcribed speech than
  ``gender_male``.
- **Most texts were chosen by the researchers to make a point.**  They
  were picked because they show a difference clearly, or because they
  show what a particular phrase does.  The differences the studies
  measured across many texts are small.
- **Some labels are a program's guess.**  For the tweets and reviews,
  "female" and "male" are the guesses of a program, and half of these
  texts were rewritten by a program (see the last section).
- **Some texts are very short.**  The shortest has two words.
- **Place and time differ.**  The texts come from the United States,
  Britain and New Zealand and were written or recorded between 1967 and
  2016.
- **Only two groups.**  All sources sort people into women and men.

Student essays
--------------

Newman, M. L., Groom, C. J., Handelman, L. D. & Pennebaker, J. W.
(2008). Gender differences in language use: An analysis of 14,000 text
samples. *Discourse Processes* 45(3), 211–236.
`PDF <https://scispace.com/pdf/gender-differences-in-language-use-an-analysis-of-14-000-3x3ua9ub7y.pdf>`__

**How the texts were collected.**  College students in at least ten
introductory psychology classes wrote down their thoughts and feelings
as they occurred, as a class assignment (p. 222).  The paper analyses
1,033 such essays by women and 793 by men.  The authors picked the
printed excerpts as "representative examples" (p. 223) and do not say
how.

Four excerpts by women and four by men (pp. 224–225).  The authors
chose this kind of essay for their examples because it "imposed the
fewest constraints on the content".  According to the authors, the
women's excerpts show "references to psychological processes …, social
processes …, verbs … and negations", and the men "used longer words and
more articles (e.g., 'a bit,' 'the music,' 'a journal')".  Across all
essays of this kind the measured differences are small.  The full
collection is not public; the paper says it is available from James W.
Pennebaker on request (p. 220).

.. list-table::
   :header-rows: 1
   :widths: 15 70 15

   * - Style
     - Text begins with
     - Location
   * - ``gender_female``
     - Okay, well, I am watching this movie.
     - p. 224
   * - ``gender_female``
     - Palms are sweaty, my stomach is uneasy, …
     - p. 224
   * - ``gender_female``
     - okay, so I'm sitting here talking to my friends.
     - p. 224
   * - ``gender_female``
     - Right now, I am thinking about my chemistry homework and test.
     - p. 224
   * - ``gender_male``
     - Sorry for any grammar mistakes in this timed writing.
     - p. 224
   * - ``gender_male``
     - I find it amusing that in writing a stream of consciousness …
     - p. 224
   * - ``gender_male``
     - Stream of Consciousness? How do you start something so vague.
     - p. 224
   * - ``gender_male``
     - Cool. I'm currently sitting in the campus library …
     - p. 225

Published articles and novels
-----------------------------

Argamon, S., Koppel, M., Fine, J. & Shimoni, A. R. (2003). Gender,
genre, and writing style in formal written texts. *Text* 23(3).
`Author preprint <https://u.cs.biu.ac.il/~koppel/papers/male-female-text-final.pdf>`__,
section "Sample Texts", preprint pp. 15–17.

**How the texts were collected.**  The study uses 604 published books
and articles from the British National Corpus, all in British English
from after 1960, with the same number by women and by men in each kind
of text (preprint p. 5).  From these the authors picked four opening
passages to show the differences they had counted.

The passages are the openings of two articles from the same journal
(*Language and Literature*) and of two novels, each about the main
character's move to a new city.  The authors describe the texts by
women as "involved" (more pronouns) and the texts by men as
"informational" (more determiners and words that specify nouns).  They
say that the two novel openings show the differences "in extreme
fashion" (preprint p. 17).

The passages are stored in full, as printed in the preprint.  The
passage from *Saigon* stops in the middle of a sentence in the preprint,
and the last sentence of Blakemore's passage is printed with words
missing.  Words that the preprint splits across two lines are joined.

.. list-table::
   :header-rows: 1
   :widths: 15 45 25 15

   * - Style
     - Text begins with
     - Author and work
     - Location
   * - ``gender_female``
     - My aim in this article is to show that …
     - Blakemore, *Language and Literature* 2 (1993)
     - preprint p. 15
   * - ``gender_female``
     - Clara never failed to be astonished …
     - Drabble, *Jerusalem the Golden*
     - preprint pp. 16–17
   * - ``gender_male``
     - The main aim of this article is to propose …
     - Simpson, *Language and Literature* 1 (1992)
     - preprint p. 15
   * - ``gender_male``
     - BY 1925 present-day Vietnam was divided …
     - Grey, *Saigon*
     - preprint p. 16

Conversation among women friends
--------------------------------

Coates, J. (1988). Women's speech, women's strength? *York Papers in
Linguistics* 13, 65–76.
`Copy <https://files.eric.ed.gov/fulltext/ED320398.pdf>`__

**How the texts were collected.**  Coates recorded a group of women
friends, without their knowing at the time, over nine months in
1983–84.  The women had been friends for eight years and met in the
evening at each other's houses (p. 68).

Fourteen turns from these conversations.  Each text is what one woman
says in one of the paper's eleven examples; what the other women say in
between is left out.  Single-word responses such as *mm* and *yeah* are
not stored as texts.  Coates uses the examples to show hedges (*sort
of*, *I mean*, *I think*) that soften a statement on a sensitive topic,
and tag questions (*isn't it*) that invite the others to join in.

The paper prints no speech by men.  Men appear only in a count of
hedges in one 40-minute conversation among men, which Coates compares
with one among women and calls a very small sample (p. 70).

.. list-table::
   :header-rows: 1
   :widths: 15 55 15 15

   * - Style
     - Text begins with
     - Speaker
     - Location
   * - ``gender_female``
     - I think I would go now because …
     - C
     - ex. (1), p. 68
   * - ``gender_female``
     - this bloke I met today who's doing …
     - A
     - ex. (2), p. 69
   * - ``gender_female``
     - there's two things aren't there# …
     - D
     - ex. (3), p. 69
   * - ``gender_female``
     - she looks very sort of um - kind of matronly really
     - not given
     - ex. (4), p. 71
   * - ``gender_female``
     - I mean I think it really depends on the attitude …
     - not given
     - ex. (5), p. 71
   * - ``gender_female``
     - oh god yes well I mean we were living in Yorkshire …
     - not given
     - ex. (6), p. 71
   * - ``gender_female``
     - but I mean so much research is male-dominated# …
     - E
     - ex. (7), p. 72
   * - ``gender_female``
     - it was dreadful wasn't it=
     - D
     - ex. (8), p. 73
   * - ``gender_female``
     - =appalling Caroline absolutely appalling
     - E
     - ex. (8), p. 73
   * - ``gender_female``
     - I think the most difficult thing is is that …
     - not given
     - ex. (9), p. 73
   * - ``gender_female``
     - and they had they had a very accurate picture of him …
     - A
     - ex. (10), p. 73
   * - ``gender_female``
     - = at one point they knew about his gap teeth too …
     - D
     - ex. (10), p. 73
   * - ``gender_female``
     - cos I'm fed up of travelling to conferences …
     - D
     - ex. (11), p. 73
   * - ``gender_female``
     - oh it's so typical isn't it
     - B
     - ex. (11), p. 73

New Zealand speech
------------------

Holmes, J. (1990). Hedges and boosters in women's and men's speech.
*Language & Communication* 10(3), 185–205.
`Copy <https://www.academia.edu/2311466/>`__

**How the texts were collected.**  Holmes and several helpers recorded and
transcribed 60,000 words of New Zealand speech, with equal amounts from
women and men (p. 202).  The recordings range from relaxed talk in people's
homes and private interviews to broadcast interviews.  Most speakers
are middle-class and well educated, from schoolchildren to people in
their sixties (p. 196).

Ten utterances.  Every example in the paper for which Holmes says
whether a woman or a man is speaking is included.  Holmes uses the
examples to show what a phrase such as *you know* or *I think* does in
a sentence, not as typical speech of women or men.  Her counts show
that women and men use the same phrases for different purposes.  The
last column gives, for each text, who used the phrase for this purpose
more often in her counts.

.. list-table::
   :header-rows: 1
   :widths: 12 30 20 13 25

   * - Style
     - Text begins with
     - Speaker, as described by Holmes
     - Location
     - Who uses the phrase this way more
   * - ``gender_female``
     - I think that's absolutely right//
     - interviewee on TV (Holmes refers to her as "she")
     - ex. (5), p. 187
     - women: 62% of their uses of *I think* add weight, 36% for men
       (p. 200)
   * - ``gender_female``
     - I'm the boss around here you know
     - young woman joking to neighbour
     - ex. (11), p. 189
     - women: 54% of their uses of *you know* express confidence, 36%
       for men (p. 199)
   * - ``gender_female``
     - and it was quite //well it was …
     - young woman to close friend
     - ex. (12), p. 189
     - men: 64% of their uses of *you know* express uncertainty, 46%
       for women (p. 199)
   * - ``gender_female``
     - he said well now I c/ I can't do it …
     - woman telling her daughter about a past experience
     - ex. (16), p. 191
     - too few cases of *of course* to say (pp. 200–201)
   * - ``gender_male``
     - time to go eh//
     - young man to his friend
     - ex. (2), p. 186
     - Holmes does not say what the tag does here
   * - ``gender_male``
     - it'd be about two o'clock I think
     - elderly man telling friends about a past experience
     - ex. (9), p. 188
     - men: 59% of their uses of *I think* are tentative, 31% for
       women (p. 200)
   * - ``gender_male``
     - better/ entertainment product or …
     - young man asking his flat-mate what he meant
     - ex. (13), p. 189
     - men: uncertain *you know*, as above
   * - ``gender_male``
     - they were all telling lies of course // …
     - male radio interviewee
     - ex. (15), p. 190
     - too few cases of *of course* to say (pp. 200–201)
   * - ``gender_male``
     - and literally sort of quite out of phase/ …
     - young man to friends in his home
     - ex. (17), p. 195
     - Holmes does not say what *sort of* does here
   * - ``gender_male``
     - he's got a sort of a skirty thing on …
     - male student describing a picture to a male interviewer
     - ex. (18), p. 198
     - no clear difference: 54% of men's and 43% of women's uses of
       *sort of* signal that a word is not exact (p. 198)

Example (16) ends in the paper with an unfinished clause ("and he
said. . . ."), which is left out.

Tweets and reviews rewritten by a program
-----------------------------------------

Reddy, S. & Knight, K. (2016). Obfuscating gender in social media
writing. *Proceedings of the EMNLP Workshop on NLP and Computational
Social Science*, 17–26.
`PDF <https://aclanthology.org/W16-5603.pdf>`__, Table 3, p. 23.

.. warning::

   In these sixteen texts, "female" and "male" are the guesses of a
   program, not the gender of the person who wrote the text.  Eight of
   the texts were not written by a person: a program produced them by
   changing words in a real tweet or review.

**How the texts were collected.**  The tweets are a random sample of
tweets sent from the United States in July 2013; the reviews are from
the Yelp Dataset Challenge of 2016.  Nobody asked the writers for their
gender: it was guessed from their first names with a list of baby names
(p. 20).  A program trained on these guesses labels a text as written
by a woman or a man; it agrees with the name-based guess for about 70%
of the Twitter users and 75% of the Yelp users (p. 23).  A second
program swaps words for similar words that are more typical of the
other gender, including misspellings such as *tommorrow*, until the
first program changes its label.  The authors picked the pairs in
Table 3 as examples and judged themselves whether meaning and fluency
were kept.

Eight pairs of an original and its rewrite.  Only pairs that the
authors marked "Yes" for similar meaning and fluency, and that change
style and not topic, are included.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - ``gender_female``
     - ``gender_male``
     - Data
   * - Yeaaah.. it's gonna be a goood day (rewrite)
     - Yeah.. it's gonna be a good day
     - Twitter
   * - who's up?! (rewrite)
     - who's up?
     - Twitter
   * - I'm so excited about tomorrow
     - I'm so pumped about tommorrow (rewrite)
     - Twitter
   * - the drinks are wonderful, too!! (rewrite)
     - the drinks are great, too!
     - Yelp
   * - and food still amazing (rewrite)
     - and food still outstanding
     - Yelp
   * - Impeccable view, amazing service, wonderful quality (rewrite)
     - Exceptional view, excellent service, great quality
     - Yelp
   * - Took my friend here
     - Took my buddy here (rewrite)
     - Yelp
   * - tasted as amazing as the first sip I took! Definitely would recommend
     - tasted as awsome as the first sip I took; certainly would recommend (rewrite)
     - Yelp
