from typing import Optional

import pytest

from regex_engine.adapters.normalizers.morfeusz.morfeusz_utils import is_word_masculine_personal_only
from regex_engine.domain.models.grammar import (
    SentencePart, GrammaticalNumber, GrammaticalCase, GrammaticalGender, GradationDegree,

)
from regex_engine.application.dto.base_word import BaseWord




def create_base_word(
        surface:str="surface",
        lemma:str="lemma",
        part:SentencePart=SentencePart.UNKNOWN,
        is_negation:bool=False,
        number:set[GrammaticalNumber]={GrammaticalNumber.SINGULAR},
        case:set[GrammaticalCase]={GrammaticalCase.NOMINATIVE},
        gender:set[GrammaticalGender] = {GrammaticalGender.MASC_INANIMATE},
        degree:Optional[GradationDegree]=None,
        annotations:tuple[str] = ()
):
    return BaseWord(
        surface=surface,
        lemma=lemma,
        part=part,
        is_negation=is_negation,
        number=number,
        case=case,
        gender=gender,
        degree=degree,
        annotations=annotations
    )



@pytest.mark.parametrize(
    "word, expected",
    [
        pytest.param(
            create_base_word(gender={GrammaticalGender.MASC_INANIMATE}),
            False,
        ),
        pytest.param(
            create_base_word(gender={GrammaticalGender.MASC_INANIMATE, GrammaticalGender.MASC_ANIMATE}),
            False,
        ),
        pytest.param(
            create_base_word(gender={GrammaticalGender.MASC_INANIMATE, GrammaticalGender.MASC_ANIMATE, GrammaticalGender.MASC_PERSONAL}),
            False,
        ),
        pytest.param(
            create_base_word(gender={GrammaticalGender.MASC_PERSONAL}),
            True,
        ),
    ]
)
def test_is_word_masculine_personal_only(word, expected):
    # Act
    actual = is_word_masculine_personal_only(word)

    # Assert
    assert actual == expected


