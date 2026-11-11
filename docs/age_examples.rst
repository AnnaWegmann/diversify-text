Sources of the age examples
===========================

The style bank has three age styles:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Style
     - Texts
     - Where the texts come from
   * - ``age_under-25``
     - 39
     - 12 blog posts by writers aged 13–17, 8 blog posts by writers
       aged 23–24, 17 hotel reviews by writers aged 18–24, 2 examples
       printed in a study (ages 17 and 19)
   * - ``age_25-49``
     - 40
     - 10 blog posts by writers aged 25–34, 10 blog posts by writers
       aged 35–48, 10 hotel reviews by writers aged 25–34, 9 hotel
       reviews by writers aged 35–49, 1 example printed in a study
       (age 47)
   * - ``age_50-plus``
     - 39
     - 19 hotel reviews by writers aged 50–64, 19 hotel reviews by
       writers aged 65 and over, 1 example printed in a study (age 73)

The age groups are broad on purpose.  The sources record age in
different ways (exact age for the blogs, groups such as 35–49 for the
reviews), and with broad groups more than one source can contribute to
a style.

The prompting method uses the first 16 texts of a style.  The texts
are stored so that the sources take turns, and women and men take
turns within a source.  The file
`age_sources.json <https://github.com/AnnaWegmann/diversify_text/blob/main/assets/stylebank/additional_info/age_sources.json>`_
lists, for every text in the order it is stored, its source, the
writer's age or age group, gender and the writer's id in the source.

Limitations
-----------

- **The kind of text differs between the styles.**  ``age_under-25``
  and ``age_25-49`` are half blog posts and half hotel reviews;
  ``age_50-plus`` is almost only hotel reviews, because the blog corpus
  has no writers over 48.  A rewrite as ``age_50-plus`` may therefore
  read like a hotel review.
- **Teenagers appear only in blogs.**  The hotel reviews start at 18.
- **Topic changes with age.**  Teenage bloggers write about school and
  friends, older bloggers about work and family.  The hotel reviews all
  have the same topic.
- **The age differences in the reviews are small.**  In our counts,
  reviewers of all ages use words of about the same length and the same
  share of *the*, *a* and *an*; only informal habits such as writing
  *i* in lower case become rarer with age.  The blogs differ much more
  by age.
- **Ages are not verified.**  The bloggers' ages are what they stated
  in an online profile.  For the reviews, the corpus page does not say
  how the ages were obtained.
- **Time.**  The blog posts are from 2004.  The reviews were published
  for a 2014 competition; the few that name a year name 2005 to 2008.
- **Hand-picked from a random draw.**  We removed texts by hand (see
  "How the texts were chosen"), so the styles are cleaner than the
  corpora they come from.
- **Terms of use.**  The blog corpus is offered "for non-commercial
  research purposes"; the page of the review corpus states no licence.
  Neither says whether excerpts may be passed on.

How the texts were chosen
-------------------------

For each source and age group we drew random candidate texts with these
rules: one text per writer, as many women as men, no links, at least
40 words, and at most 110 words for blog posts or 130 words for hotel
reviews.  We then read the candidates and removed poems and song
lyrics, quotations of other people's words, lists, announcements and
advertisements, texts that are not in standard English, and texts that
name private persons with their full name.  Among the reviews by
writers aged 18–24 only 17 passed the rules, and all 17 are used.

The texts are stored as they are in the corpora, including spelling
mistakes.  In the hotel reviews the title of a review comes first and
runs straight into the text, without a full stop in between.

Blog posts
----------

Schler, J., Koppel, M., Argamon, S. & Pennebaker, J. W. (2006).
Effects of age and gender on blogging. *AAAI Spring Symposium on
Computational Approaches to Analyzing Weblogs*.
`Corpus page <https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm>`__,
`copy used <https://huggingface.co/datasets/tasksource/blog_authorship_corpus>`__

**How the texts were collected.**  The corpus holds 681,288 posts by
19,320 bloggers, gathered from blogger.com in August 2004.  Age and
gender are what each blogger entered in their profile.  The corpus
only contains bloggers aged 13–17, 23–27 and 33–48.

We used the first of the two data files of the copy on Hugging Face
(430,000 posts by 11,926 bloggers).  In one random post per blogger,
the youngest group differs clearly from the older ones:

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - Per 1,000 words
     - 13–17
     - 23–27
     - 33–47
   * - *lol*, *haha*
     - 2.4
     - 0.3
     - 0.1
   * - *u*, *ur*, *im*
     - 2.7
     - 0.5
     - 0.2
   * - *i* written in lower case
     - 13.7
     - 5.3
     - 1.7
   * - *the*, *a*, *an*
     - 52.4
     - 65.5
     - 70.1
   * - two or more exclamation marks in a row
     - 2.5
     - 1.0
     - 0.5

Hotel reviews
-------------

Rangel, F., Rosso, P., Chugur, I., Potthast, M., Trenkmann, M., Stein,
B., Verhoeven, B. & Daelemans, W. (2014). Overview of the 2nd author
profiling task at PAN 2014. *CLEF 2014 Working Notes*.
`Corpus <https://zenodo.org/records/3716008>`__ (English reviews,
training set)

**How the texts were collected.**  The corpus was built for a
competition on guessing a writer's age and gender from text.  The
English review part holds hotel reviews by 4,160 writers, each labelled
with gender and one of five age groups (18–24, 25–34, 35–49, 50–64, 65
and over).  The corpus page does not say where the reviews were collected
or how the writers' ages were obtained; the task paper above describes
this and was not checked for this page.

The same corpus also contains blogs, social media posts and tweets.
We did not use them: the tweets are given as links only, and the blogs
and social media posts contain much advertising.

Examples printed in a study
---------------------------

Nguyen, D., Smith, N. A. & Rosé, C. P. (2011). Author age prediction
from text using linear regression. *Proceedings of the 5th ACL-HLT
Workshop on Language Technology for Cultural Heritage, Social Sciences,
and Humanities*, 115–123.
`PDF <https://aclanthology.org/W11-1515.pdf>`__

**How the texts were collected.**  The study predicts a writer's age
from blog posts (the corpus above) and from transcribed telephone
conversations between strangers, recorded in 2002–03.  The bloggers'
ages come from their profiles; the paper says the callers' ages "were
recorded".  The authors picked the printed examples by hand to show
where their program works well and where it fails (p. 121), and
shortened most of them: ``[...]`` marks where they left text out.  In
the telephone examples each line is one turn of the speaker, marked
``T:``, and the turns are a selection.

.. list-table::
   :header-rows: 1
   :widths: 20 10 40 15 15

   * - Style
     - Age
     - Text begins with
     - Kind of text
     - Location
   * - ``age_under-25``
     - 17
     - I can't sleep, but this time I have school tommorow, …
     - blog
     - p. 121
   * - ``age_under-25``
     - 19
     - T: yeah it's too i just just freaked out [...]
     - telephone speech
     - p. 122
   * - ``age_25-49``
     - 47
     - [...]In the weeks leading up to this meeting …
     - blog
     - p. 122
   * - ``age_50-plus``
     - 73
     - T: ah thoughts i'm retired right now
     - telephone speech
     - p. 122

The paper prints two more examples, from a forum for people with
breast cancer.  They are left out because the writers describe their
own illness.  The paper's program guessed 34 for the 47-year-old
blogger, so the authors do not present that text as typical.

Studies on age and style
------------------------

The styles do not contain examples from the sociolinguistic studies on
age, because those print only a few short utterances per age group.
Their findings agree with the counts above: teenagers use the newest
forms most (Tagliamonte & D'Arcy 2009, *Language* 85(1)), and
abbreviations and *lol* in instant messages become rarer between 15 and
20 (Tagliamonte & Denis 2008, *American Speech* 83(1)).
