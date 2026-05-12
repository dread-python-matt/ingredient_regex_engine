from collections import Counter

import pytest

from regex_engine.adapters.normalizers.morfeusz.phrase_analyzer import PhraseAnalyser
from regex_engine.application.dto.analysed_phrase import AnalysedPhrase

pytest.importorskip("morfeusz2")

import morfeusz2


@pytest.fixture(scope="session")
def morfeusz():
    return morfeusz2.Morfeusz()


@pytest.fixture
def analyser(morfeusz):
    return PhraseAnalyser(morfeusz)

def analysed_phrase_to_dict(actual: AnalysedPhrase):
    return {
        "subject": (actual.subject.word.surface, actual.subject.position),
        "dependent_noun": (
            None if actual.dependent_noun is None
            else (actual.dependent_noun.word.surface, actual.dependent_noun.position)
        ),
        "subject_adjectives": [
            (w.word.surface, w.position) for w in actual.subject_adjectives
        ],
        "dependent_noun_adjectives": [
            (w.word.surface, w.position) for w in actual.dependent_noun_adjectives
        ],
        "phrase": actual.phrase,
    }


@pytest.mark.parametrize(
    "phrase, expected",
    [
    pytest.param(
        "jajka",
        {
            "subject": ("jajka", 0),
            "dependent_noun": None,
            "subject_adjectives": [],
            "dependent_noun_adjectives": [],
            "phrase": {0: "jajka"},
        },
        id="jajka",
    ),
        pytest.param(
            "gotowane żółtka jaj",
            {
                "subject": ("żółtka", 1),
                "dependent_noun": ("jaj", 2),
                "subject_adjectives": [("gotowane", 0)],
                "dependent_noun_adjectives": [],
                "phrase": {0: "gotowane", 1: "żółtka", 2: "jajka"},
            },
            id="gotowane żółtka jaj",
        ),

        pytest.param(
            "kolorowa mąka typu drugiego",
            {
                "subject": ("mąka", 1),
                "dependent_noun": ("typu", 2),
                "subject_adjectives": [("kolorowa", 0)],
                "dependent_noun_adjectives": [("drugiego", 3)],
                "phrase": {0: "kolorowa", 1: "mąka", 2: "typu", 3: "drugiego"},
            },
            id="kolorowa mąka typu drugiego",
        ),

        pytest.param(
            "kakao",
            {
                "subject": ("kakao", 0),
                "dependent_noun": None,
                "subject_adjectives": [],
                "dependent_noun_adjectives": [],
                "phrase": {0: "kakao"},
            },
            id="kakao",
        ),

        pytest.param(
            "świeże masło z dodatkiem kakao",
            {
                "subject": ("masło", 1),
                "dependent_noun": None,
                "subject_adjectives": [("świeże", 0)],
                "dependent_noun_adjectives": [],
                "phrase": {0: "świeże", 1: "masło", 2: "z", 3: "dodatkiem", 4: "kakao"},
            },
            id="świeże masło z dodatkiem kakao",
        ),

        pytest.param(
            "gotowane, zielone nasiona fasoli czerwonej w puszce zwykłej, zamkniętej",
            {
                "subject": ("nasiona", 3),
                "dependent_noun": ("fasoli", 4),
                "subject_adjectives": [("gotowane", 0), ("zielone", 2)],
                "dependent_noun_adjectives": [("czerwonej", 5)],
                "phrase": {
                    0: "gotowane",
                    1: ",",
                    2: "zielone",
                    3: "nasiona",
                    4: "fasoli",
                    5: "czerwonej",
                    6: "w",
                    7: "puszce",
                    8: "zwykłej",
                    9: ",",
                    10: "zamkniętej",
                },
            },
            id="gotowane, zielone nasiona fasoli czerwonej w puszce zwykłej, zamkniętej",
        ),
    ]
)
def test_analyse_happy_path(phrase:str, expected:dict, analyser):
    # Act
    actual_analysed = analyser.analyse(phrase)
    actual = analysed_phrase_to_dict(actual_analysed)

    # Assert
    assert actual["subject"] == expected["subject"]
    assert actual["dependent_noun"] == expected["dependent_noun"]
    assert Counter(actual["dependent_noun_adjectives"]) == Counter(expected["dependent_noun_adjectives"])
    assert Counter(actual["subject_adjectives"]) == Counter(expected["subject_adjectives"])




@pytest.mark.parametrize(
    "phrase",
    [
        "kolorowy",
        "czarny",
        "z gotowanym",
        "obrane i upieczone",
    ]

)
def test_analyse__no_subject__raise_value_error(phrase:str, analyser):
    # Act / Assert
    with pytest.raises(ValueError):
        analyser.analyse(phrase)



@pytest.mark.parametrize(
    "phrase",
    [
        "kolorowy jajko",
        "gotowane fasola czerwona",
        "smażony łosoś niebieska",
        "gotowany pstrąg jajka zwykły"
    ]
)
def test_analyse__invalid_inflection__raise_value_error(phrase:str, analyser):
    # Act / Assert
    with pytest.raises(ValueError):
        analyser.analyse(phrase)