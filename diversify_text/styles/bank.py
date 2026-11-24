"""Building the style bank that is used by the package.

Loads ``stylebank.json`` via  :mod:`diversify_text.styles._load`.
This module decides which styles are exposed in which order.

Together the two lists must contain every leaf of ``stylebank.json``
exactly once; importing this module fails otherwise, so editing the
JSON forces a conscious ordering decision here.
"""

from __future__ import annotations

from diversify_text.styles._load import load_style_bank

# ``n`` selects the first *n* styles -> curate _BANK_ORDER to make
#   first *n* style set is as diverse as possible
#   Manually editable and created
_BANK_ORDER: list[str] = [
    "informal",  # diaphasic
    "formal",  # diaphasic
    "britneyspears",  # idiolect
    "bahamian_creole",  # diatopic
    "late_modern_english",  # diachronic
    "age_child",  # diastratic
    "digital_communication",  # diamesic
    "gender_female",  # diastratic
    "earlier_african_american_vernacular_english",  # diatopic
    "lyrical",  # diaphasic
    "cristiano",  # idiolect
    "early_modern_english",  # diachronic
    "spoken_communication",  # diamesic
    "instructional",  # diaphasic
    "katyperry",  # idiolect
    "welsh_english",  # diatopic
    "age_under-25",  # diastratic
    "ladygaga",  # idiolect
    "manx_english",  # diatopic
    "informational",  # diaphasic
    "gender_male",  # diastratic
    "vincentian_creole",  # diatopic
    "taylorswift13",  # idiolect
    "interactive",  # diaphasic
    #
    "age_50-plus",  # diastratic
    "arianagrande",  # idiolect
    "belizean_creole",  # diatopic
    "prose", # diaphasic
    "age_25-49",  # diastratic
    "selenagomez",  # idiolect
    "australian_english",  # diatopic
    "opinion",  # diaphasic
    "jimmyfallon",  # idiolect
    "aboriginal_english",  # diatopic
    "persuasive",  # diaphasic
    "justinbieber",  # idiolect
    "kenyan_english",  # diatopic
    "narrative",  # diaphasic
    "rihanna",  # idiolect
    "english_dialects_in_the_southwest_of_england",  # diatopic
    "ddlovato",  # idiolect
    "croker_island_english",  # diatopic
    "jtimberlake",  # idiolect
    "white_zimbabwean_english",  # diatopic
    "pakistani_english",  # diatopic
    "barackobama",  # idiolect
    "ugandan_english",  # diatopic
    "shakira",  # idiolect
    "jamaican_creole",  # diatopic
    "vernacular_liberian_english",  # diatopic
    "irish_english",  # diatopic
    "barbadian_creole",  # diatopic
    "falkland_islands_english",  # diatopic
    "indian_english",  # diatopic
    "tanzanian_english",  # diatopic
    "ghanaian_english",  # diatopic
    "indian_south_african_english",  # diatopic
    "palmerston_english",  # diatopic
    "trinidadian_creole",  # diatopic
    "liberian_settler_english",  # diatopic
    "newfoundland_english",  # diatopic
    "malaysian_english",  # diatopic
    "hong_kong_english",  # diatopic
    "eastern_maroon_creole",  # diatopic
    "scottish_english",  # diatopic
    "jamaican_english",  # diatopic
    "channel_islands_english",  # diatopic
    "education_some_highschool_no_diploma",  # diastratic
    "education_doctorate",  # diastratic
    "education_highschool",  # diastratic
    "ethnic_other",  # diastratic
    "ethnic_african",  # diastratic
    "education_edu-associatedegree",  # diastratic
    "ethnic_eastasian",  # diastratic
    "ethnic_hispanicorlatino",  # diastratic
    # maybe leave out?
    "politics_rightwing",  # diastratic
    "politics_centrist",  # diastratic
    "politics_leftwing",  # diastratic
    "education_bachelor",  # diastratic
    "education_master",  # diastratic
    "education_tradeortechnicalorvocationaltraining",  # diastratic
    "ethnic_caucasian",  # diastratic
    "ethnic_southasian",  # diastratic
    "education_nodegree",  # diastratic
]

# ``_UNUSUAL_ORDER`` holds styles of :data:`UNUSUAL_STYLE_BANK`:
#   kept out of the default bank because they are too far from
#   contemporary English to be a useful default rewrite target, but still
#   selectable by name (never via ``n`` or an index).
_UNUSUAL_ORDER: list[str] = [
    "middle_english",  # diachronic
    "old_english",  # diachronic
]

_FLAT = load_style_bank()

_listed = _BANK_ORDER + _UNUSUAL_ORDER
if sorted(_listed) != sorted(_FLAT):  # hand-written ordering and selection is not complete/ contains an error
    raise ValueError(
        "stylebank.json and the order lists in diversify_text/styles/bank.py are out of sync "
        f"missing keys: {sorted(set(_FLAT) - set(_listed))}, "
        f"unknown or duplicated {sorted(n for n in set(_listed) if n not in _FLAT or _listed.count(n) > 1)}."
    )

#: The default style bank: every style selectable via ``n`` or index.
DEFAULT_STYLE_BANK: dict[str, list[str]] = {
    name: _FLAT[name] for name in _BANK_ORDER
}

#: Styles selectable by name only. Might delete later.
UNUSUAL_STYLE_BANK: dict[str, list[str]] = {
    name: _FLAT[name] for name in _UNUSUAL_ORDER
}

#: Surface-level rewrites (all caps, passive voice, ...), loaded from
#: ``surfacebank.json``. The file's order is the
#: bank's order.  Selectable by name only, like ``UNUSUAL_STYLE_BANK``.
SURFACE_STYLE_BANK: dict[str, list[str]] = load_style_bank("surfacebank.json")
