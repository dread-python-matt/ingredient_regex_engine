import pytest

from regex_engine.adapters.normalizers.morfeusz.inflector.inflector_paradigm import InflectionParadigm
from regex_engine.application.dto.generated_word import GeneratedWord
from regex_engine.domain.models.grammar import SentencePart, GradationDegree
from regex_engine.application.dto.base_word import BaseWord
from regex_engine.domain.models.grammar import GrammaticalNumber, GrammaticalCase, GrammaticalGender
from regex_engine.adapters.normalizers.morfeusz.inflector.inflection_request import InflectionRequest



pytest.importorskip("morfeusz2")

import morfeusz2

@pytest.fixture(scope="session")
def morfeusz():
    return morfeusz2.Morfeusz()


@pytest.fixture
def generate_variations(morfeusz):
    def _generate(word:BaseWord) -> list[GeneratedWord]:
        return [GeneratedWord.from_tuple(t) for t in morfeusz.generate(word.lemma)]

    return _generate


@pytest.fixture
def noun_requests():
    return [
        InflectionRequest(number, case)
        for number in GrammaticalNumber
        for case in GrammaticalCase
    ]

@pytest.fixture
def adjective_requests():
    return [
        InflectionRequest(number, case, gender)
        for number in GrammaticalNumber
        for case in GrammaticalCase
        for gender in GrammaticalGender
    ]


BASE_NOUNS = {
    "białko": BaseWord(
            lemma="białko",
            surface="białko",
            part=SentencePart.NOUN,
            number={GrammaticalNumber.SINGULAR},
            case={GrammaticalCase.NOMINATIVE},
            gender={GrammaticalGender.NEUTER},
    ),
    "drożdże": BaseWord(
        lemma="drożdże",
        surface="drożdże",
        part=SentencePart.NOUN,
        is_pluralia_tantum=True,
        number={GrammaticalNumber.PLURAL},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.NEUTER},
    ),
    "kakao": BaseWord(
        lemma="kakao",
        surface="kakao",
        part=SentencePart.NOUN,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.NEUTER},
        annotations=['niezal.']
    ),
    "masło": BaseWord(
        lemma="masło",
        surface="masło",
        part=SentencePart.NOUN,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.NEUTER},
    ),
    "woda": BaseWord(
        lemma="woda",
        surface="woda",
        part=SentencePart.NOUN,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.FEMININE},
    ),
    "poziomka": BaseWord(
        lemma="poziomka",
        surface="poziomka",
        part=SentencePart.NOUN,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.FEMININE},
    ),
    "naleśnik": BaseWord(
        lemma="naleśnik",
        surface="naleśnik",
        part=SentencePart.NOUN,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
    "żółtko": BaseWord(
        lemma="żółtko",
        surface="żółtko",
        part=SentencePart.NOUN,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
}

EXPECTED_FORMS = {
    "białko": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "białko",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "białka",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "białku",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "białko",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "białkiem",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "białku",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "białko",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "białka",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "białek",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "białkom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "białka",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "białkami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "białkach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "białka",
    },
    "drożdże": {
        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "drożdże",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "drożdży",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "drożdżom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "drożdże",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "drożdżami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "drożdżach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "drożdże",
    },
    "kakao": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "kakao",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "kakao",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "kakao",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "kakao",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "kakao",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "kakao",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "kakao",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "kakao",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "kakao",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "kakao",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "kakao",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "kakao",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "kakao",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "kakao",
    },
    "masło": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "masło",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "masła",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "masłu",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "masło",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "masłem",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "maśle",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "masło",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "masła",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "maseł",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "masłom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "masła",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "masłami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "masłach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "masła",
    },
    "woda": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "woda",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "wody",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "wodzie",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "wodę",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "wodą",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "wodzie",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "wodo",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "wody",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "wód",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "wodom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "wody",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "wodami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "wodach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "wody",
    },
    "poziomka": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "poziomka",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "poziomki",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "poziomce",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "poziomkę",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "poziomką",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "poziomce",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "poziomko",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "poziomki",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "poziomek",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "poziomkom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "poziomki",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "poziomkami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "poziomkach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "poziomki",
    },
    "naleśnik": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "naleśnik",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "naleśnika",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "naleśnikowi",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "naleśnik",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "naleśnikiem",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "naleśniku",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "naleśniku",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "naleśniki",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "naleśników",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "naleśnikom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "naleśniki",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "naleśnikami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "naleśnikach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "naleśniki",
    },
    "żółtko": {
        (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE): "żółtko",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE): "żółtka",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.DATIVE): "żółtku",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE): "żółtko",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL): "żółtkiem",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.LOCATIVE): "żółtku",
        (GrammaticalNumber.SINGULAR, GrammaticalCase.VOCATIVE): "żółtko",

        (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE): "żółtka",
        (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE): "żółtek",
        (GrammaticalNumber.PLURAL, GrammaticalCase.DATIVE): "żółtkom",
        (GrammaticalNumber.PLURAL, GrammaticalCase.ACCUSATIVE): "żółtka",
        (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL): "żółtkami",
        (GrammaticalNumber.PLURAL, GrammaticalCase.LOCATIVE): "żółtkach",
        (GrammaticalNumber.PLURAL, GrammaticalCase.VOCATIVE): "żółtka",
    }
}


def build_noun_params():
    params = []

    for word_key, forms in EXPECTED_FORMS.items():
        for (number, case), expected_surface in forms.items():
            params.append(
                pytest.param(
                    word_key,
                    InflectionRequest(number=number, case=case),
                    expected_surface,
                    id=f"{word_key}-{number.value}-{case.value}",
                )
            )

    return params





@pytest.mark.parametrize(
    "word_key, inflection_request, expected_surface",
    build_noun_params(),
)
def test_inflect_noun_all_variants(word_key, inflection_request, expected_surface, generate_variations):
    # Arrange
    word = BASE_NOUNS[word_key]
    variations = generate_variations(word)
    inflection_paradigm = InflectionParadigm(word, variations)

    # Act
    actual = inflection_paradigm.inflect(inflection_request)

    # Assert
    assert actual.surface == expected_surface



BASE_ADJECTIVES = {
    "czarny": BaseWord(
        lemma="czarny",
        surface="czarny",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
    "świeży": BaseWord(
        lemma="świeży",
        surface="świeży",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
    "czerwony": BaseWord(
        lemma="czerwony",
        surface="czerwony",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
    "zimny": BaseWord(
        lemma="zimny",
        surface="zimny",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
    "gorący": BaseWord(
        lemma="gorący",
        surface="gorący",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
    "duży": BaseWord(
        lemma="duży",
        surface="duży",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
    "mały": BaseWord(
        lemma="mały",
        surface="mały",
        part=SentencePart.ADJECTIVE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
        degree=GradationDegree.POSITIVE,
    ),
}

EXPECTED_ADJECTIVES = {
    "czarny": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "czarna",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "czarne",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "czarnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "czarnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "czarnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "czarnej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "czarnego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "czarnemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "czarnemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "czarnemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "czarnej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "czarnemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "czarnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "czarnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "czarną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "czarne",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "czarnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "czarnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "czarnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "czarną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "czarnym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "czarnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "czarnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "czarnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "czarnej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "czarnym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "czarny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "czarna",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "czarne",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "czarni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "czarne",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "czarnych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "czarnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "czarnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "czarnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "czarnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "czarnym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "czarne",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "czarnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "czarnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "czarnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "czarnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "czarnymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "czarnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "czarnych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "czarni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "czarne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "czarne",
    },

    "świeży": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "świeża",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "świeże",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "świeżego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "świeżego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "świeżego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "świeżej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "świeżego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "świeżemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "świeżemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "świeżemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "świeżej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "świeżemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "świeżego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "świeżego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "świeżą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "świeże",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "świeżym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "świeżym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "świeżym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "świeżą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "świeżym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "świeżym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "świeżym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "świeżym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "świeżej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "świeżym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "świeży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "świeża",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "świeże",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "świeży",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "świeże",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "świeżych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "świeżym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "świeżym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "świeżym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "świeżym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "świeżym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "świeże",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "świeżymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "świeżymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "świeżymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "świeżymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "świeżymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "świeżych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "świeżych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "świeży",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "świeże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "świeże",
    },

    "czerwony": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "czerwona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "czerwone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "czerwonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "czerwonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "czerwonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "czerwonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "czerwonego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "czerwonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "czerwonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "czerwonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "czerwonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "czerwonemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "czerwonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "czerwonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "czerwoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "czerwone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "czerwonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "czerwonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "czerwonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "czerwoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "czerwonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "czerwonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "czerwonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "czerwonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "czerwonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "czerwonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "czerwony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "czerwona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "czerwone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "czerwoni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "czerwone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "czerwonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "czerwonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "czerwonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "czerwonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "czerwonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "czerwonym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "czerwone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "czerwonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "czerwonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "czerwonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "czerwonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "czerwonymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "czerwonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "czerwonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "czerwoni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "czerwone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "czerwone",
    },

    "zimny": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "zimna",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "zimne",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "zimnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "zimnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "zimnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "zimnej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "zimnego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "zimnemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "zimnemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "zimnemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "zimnej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "zimnemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "zimnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "zimnego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "zimną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "zimne",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "zimnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "zimnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "zimnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "zimną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "zimnym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "zimnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "zimnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "zimnym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "zimnej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "zimnym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "zimny",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "zimna",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "zimne",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "zimni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "zimne",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "zimnych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "zimnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "zimnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "zimnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "zimnym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "zimnym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "zimne",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "zimnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "zimnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "zimnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "zimnymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "zimnymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "zimnych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "zimnych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "zimni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "zimne",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "zimne",
    },

    "gorący": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "gorąca",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "gorące",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "gorącego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "gorącego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "gorącego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "gorącej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "gorącego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "gorącemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "gorącemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "gorącemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "gorącej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "gorącemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "gorącego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "gorącego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "gorącą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "gorące",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "gorącym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "gorącym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "gorącym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "gorącą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "gorącym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "gorącym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "gorącym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "gorącym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "gorącej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "gorącym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "gorący",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "gorąca",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "gorące",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "gorący",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "gorące",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "gorących",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "gorącym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "gorącym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "gorącym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "gorącym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "gorącym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "gorące",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "gorącymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "gorącymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "gorącymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "gorącymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "gorącymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "gorących",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "gorących",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "gorący",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "gorące",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "gorące",
    },

    "duży": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "duża",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "duże",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "dużego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "dużego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "dużego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "dużej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "dużego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "dużemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "dużemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "dużemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "dużej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "dużemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "dużego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "dużego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "dużą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "duże",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "dużym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "dużym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "dużym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "dużą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "dużym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "dużym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "dużym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "dużym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "dużej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "dużym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "duży",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "duża",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "duże",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "duzi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "duże",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "dużych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "dużym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "dużym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "dużym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "dużym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "dużym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "duże",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "dużymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "dużymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "dużymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "dużymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "dużymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "dużych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "dużych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "duzi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "duże",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "duże",
    },

    "mały": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "mała",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "małe",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "małego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "małego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "małego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "małej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "małego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "małemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "małemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "małemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "małej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "małemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "małego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "małego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "małą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "małe",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "małym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "małym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "małym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "małą",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "małym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "małym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "małym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "małym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "małej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "małym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "mały",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "mała",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "małe",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "mali",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "małe",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "małych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "małym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "małym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "małym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "małym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "małym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "małe",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "małymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "małymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "małymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "małymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "małymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "małych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "małych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "mali",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "małe",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "małe",
    },
}


def build_adjective_params():
    params = []

    for adjective_key, forms in EXPECTED_ADJECTIVES.items():
        for (number, gender, case), expected_surface in forms.items():
            params.append(
                pytest.param(
                    adjective_key,
                    InflectionRequest(number=number, case=case, gender=gender),
                    expected_surface,
                    id=f"{adjective_key}-{number.value}-{case.value}-{gender.value}",
                )
            )

    return params


@pytest.mark.parametrize(
    "adjective_key, inflection_request, expected_surface",
    build_adjective_params(),
)
def test_inflect_adjective__happy_path(adjective_key, inflection_request, expected_surface, generate_variations):
    # Arrange
    adjective = BASE_ADJECTIVES[adjective_key]
    variations = generate_variations(adjective)
    inflection_paradigm = InflectionParadigm(adjective, variations)

    # Act
    actual = inflection_paradigm.inflect(inflection_request)

    # Asser
    assert actual.surface == expected_surface


BASE_PPAS = {
    "wędzić": BaseWord(
        lemma="wędzić",
        surface="wędzony",
        part=SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
    "gotować": BaseWord(
        lemma="gotować",
        surface="gotowany",
        part=SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
    "poszatkować": BaseWord(
        lemma="poszatkować",
        surface="poszatkowany",
        part=SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
    "kroić": BaseWord(
        lemma="kroić",
        surface="krojony",
        part=SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
    "smażyć": BaseWord(
        lemma="smażyć",
        surface="smażony",
        part=SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
        number={GrammaticalNumber.SINGULAR},
        case={GrammaticalCase.NOMINATIVE},
        gender={GrammaticalGender.MASC_INANIMATE},
    ),
}

EXPECTED_PPAS = {
    "wędzić": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "wędzona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "wędzone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "wędzonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "wędzonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "wędzonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "wędzonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "wędzonego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "wędzonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "wędzonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "wędzonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "wędzonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "wędzonemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "wędzonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "wędzonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "wędzoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "wędzone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "wędzonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "wędzonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "wędzonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "wędzoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "wędzonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "wędzonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "wędzonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "wędzonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "wędzonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "wędzonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "wędzony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "wędzona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "wędzone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "wędzeni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "wędzone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "wędzonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "wędzonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "wędzonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "wędzonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "wędzonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "wędzonym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "wędzone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "wędzonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "wędzonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "wędzonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "wędzonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "wędzonymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "wędzonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "wędzonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "wędzeni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "wędzone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "wędzone",
    },

    "gotować": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "gotowana",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "gotowane",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "gotowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "gotowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "gotowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "gotowanej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "gotowanego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "gotowanemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "gotowanemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "gotowanemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "gotowanej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "gotowanemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "gotowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "gotowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "gotowaną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "gotowane",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "gotowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "gotowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "gotowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "gotowaną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "gotowanym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "gotowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "gotowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "gotowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "gotowanej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "gotowanym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "gotowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "gotowana",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "gotowane",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "gotowani",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "gotowane",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "gotowanych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "gotowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "gotowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "gotowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "gotowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "gotowanym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "gotowane",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "gotowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "gotowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "gotowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "gotowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "gotowanymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "gotowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "gotowanych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "gotowani",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "gotowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "gotowane",
    },

    "poszatkować": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "poszatkowana",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "poszatkowane",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "poszatkowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "poszatkowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "poszatkowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "poszatkowanej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "poszatkowanego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "poszatkowanemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "poszatkowanemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "poszatkowanemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "poszatkowanej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "poszatkowanemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "poszatkowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "poszatkowanego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "poszatkowaną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "poszatkowane",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "poszatkowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "poszatkowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "poszatkowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "poszatkowaną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "poszatkowanym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "poszatkowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "poszatkowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "poszatkowanym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "poszatkowanej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "poszatkowanym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "poszatkowany",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "poszatkowana",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "poszatkowane",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "poszatkowani",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "poszatkowane",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "poszatkowanych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "poszatkowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "poszatkowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "poszatkowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "poszatkowanym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "poszatkowanym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "poszatkowane",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "poszatkowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "poszatkowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "poszatkowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "poszatkowanymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "poszatkowanymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "poszatkowanych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "poszatkowanych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "poszatkowani",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "poszatkowane",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "poszatkowane",
    },

    "kroić": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "krojona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "krojone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "krojonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "krojonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "krojonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "krojonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "krojonego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "krojonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "krojonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "krojonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "krojonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "krojonemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "krojonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "krojonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "krojoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "krojone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "krojonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "krojonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "krojonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "krojoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "krojonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "krojonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "krojonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "krojonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "krojonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "krojonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "krojony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "krojona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "krojone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "krojeni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "krojone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "krojonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "krojonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "krojonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "krojonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "krojonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "krojonym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "krojone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "krojonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "krojonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "krojonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "krojonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "krojonymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "krojonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "krojonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "krojeni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "krojone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "krojone",
    },

    "smażyć": {
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "smażona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "smażone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "smażonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "smażonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "smażonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "smażonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "smażonego",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "smażonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "smażonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "smażonemu",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "smażonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "smażonemu",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "smażonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "smażonego",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "smażoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "smażone",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "smażonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "smażonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "smażonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "smażoną",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "smażonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "smażonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "smażonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "smażonym",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "smażonej",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "smażonym",

        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "smażony",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "smażona",
        (GrammaticalNumber.SINGULAR, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "smażone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.NOMINATIVE): "smażeni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.NOMINATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.NOMINATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.NOMINATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.NOMINATIVE): "smażone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.GENITIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.GENITIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.GENITIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.GENITIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.GENITIVE): "smażonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.DATIVE): "smażonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.DATIVE): "smażonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.DATIVE): "smażonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.DATIVE): "smażonym",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.DATIVE): "smażonym",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.ACCUSATIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.ACCUSATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.ACCUSATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.ACCUSATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.ACCUSATIVE): "smażone",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.INSTRUMENTAL): "smażonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.INSTRUMENTAL): "smażonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.INSTRUMENTAL): "smażonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.INSTRUMENTAL): "smażonymi",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.INSTRUMENTAL): "smażonymi",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.LOCATIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.LOCATIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.LOCATIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.LOCATIVE): "smażonych",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.LOCATIVE): "smażonych",

        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_PERSONAL, GrammaticalCase.VOCATIVE): "smażeni",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_ANIMATE, GrammaticalCase.VOCATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.MASC_INANIMATE, GrammaticalCase.VOCATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.FEMININE, GrammaticalCase.VOCATIVE): "smażone",
        (GrammaticalNumber.PLURAL, GrammaticalGender.NEUTER, GrammaticalCase.VOCATIVE): "smażone",
    },
}


def build_passive_adjectival_participle():
    params = []

    for ppas_key, forms in EXPECTED_PPAS.items():
        for (number, gender, case), expected_surface in forms.items():
            params.append(
                pytest.param(
                    ppas_key,
                    InflectionRequest(number=number, case=case, gender=gender),
                    expected_surface,
                    id=f"{ppas_key}-{number.value}-{case.value}-{gender.value}",
                )
            )

    return params


@pytest.mark.parametrize(
    "ppas_key, inflection_request, expected_surface",
    build_passive_adjectival_participle(),
)
def test_inflect_passive_adjectival_participle__happy_path(ppas_key, inflection_request, expected_surface, generate_variations):
    # Arrange
    adjective = BASE_PPAS[ppas_key]
    variations = generate_variations(adjective)
    inflection_paradigm = InflectionParadigm(adjective, variations)

    # Act
    actual = inflection_paradigm.inflect(inflection_request)

    # Asser
    assert actual.surface == expected_surface









