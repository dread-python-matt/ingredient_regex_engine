import logging
import re
import string
from typing import Sequence

from regex_engine.application.dto.base_word import BaseWord
from regex_engine.application.dto.generated_word import GeneratedWord
from regex_engine.application.dto.word_analysis import WordAnalysis
from regex_engine.domain.models.grammar import GrammaticalGender, SentencePart

logger = logging.getLogger(__name__)


def get_word_analysis_by_index(analysis: Sequence[WordAnalysis], index: int):
    return [word for word in analysis if word.position == index]


def find_first_noun_index(analysis: Sequence[WordAnalysis]) -> int:
    sorted_analysis = sorted(analysis, key=lambda w: w.position)
    for word in sorted_analysis:
        if word.part == SentencePart.NOUN.value:
            return word.position
    return -1


def filter_non_cooking_related(analysis: Sequence[WordAnalysis]) -> list[WordAnalysis]:
    return [word for word in analysis if is_word_cooking_related(word)]


def tuples_to_word_analysis(tuples: list[tuple]) -> list[WordAnalysis]:
    return [WordAnalysis.from_tuple(t) for t in tuples]


def tuples_to_generated_word(tuples: list[tuple]) -> list[GeneratedWord]:
    return [GeneratedWord.from_tuple(t) for t in tuples]


def is_word_cooking_related(word: BaseWord) -> bool:
    return not (
        is_word_colloquial(word)
        or is_word_former(word)
        or is_word_abusive(word)
        or is_word_masculine_personal_only(word)
    )


def is_word_inflectionally_independent(word: BaseWord) -> bool:
    return "niezal." in word.annotations or len(word.case) == 7


def is_word_former(word: BaseWord) -> bool:
    return "daw." in word.annotations


def is_word_colloquial(word: BaseWord) -> bool:
    return "pot." in word.annotations


def is_word_abusive(word: BaseWord) -> bool:
    return "pogard." in word.annotations


def is_word_masculine_personal_only(word: BaseWord) -> bool:
    return len(word.gender) == 1 and GrammaticalGender.MASC_PERSONAL in word.gender


def split_phrase(phrase: str) -> dict[int, str]:
    tokens = re.findall(r"\w+|[^\w\s]", phrase)
    return {i: v for i, v in enumerate(tokens)}


def join_tokens(tokens: dict) -> str:
    result = []
    punct = set(string.punctuation)

    for token in tokens.values():
        if result and token not in punct:
            result.append(" ")
        result.append(token)

    return "".join(result)
