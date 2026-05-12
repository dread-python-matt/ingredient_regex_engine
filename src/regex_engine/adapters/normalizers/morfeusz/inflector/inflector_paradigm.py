from typing import Sequence

from regex_engine.adapters.normalizers.morfeusz.inflector.inflection_request import (
    InflectionRequest,
)
from regex_engine.adapters.normalizers.morfeusz.morfeusz_utils import (
    is_word_inflectionally_independent,
)
from regex_engine.application.dto.base_word import BaseWord
from regex_engine.application.dto.generated_word import GeneratedWord
from regex_engine.domain.models.grammar import GrammaticalCase, GrammaticalNumber, SentencePart


class InflectionParadigm:
    def __init__(self, word: BaseWord, variations: Sequence[GeneratedWord]) -> None:
        self.word: BaseWord = word
        self.variations = list(variations)

    def inflect(self, request: InflectionRequest) -> BaseWord:
        match self.word.part:
            case SentencePart.ABBREVIATION:
                return self._inflect_abbreviation(request.number, request.case)
            case SentencePart.NOUN:
                return self._inflect_noun(request.number, request.case)
            case SentencePart.ADJECTIVE:
                return self._inflect_adjective(request)
            case SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE:
                return self._inflect_passive_adjectival_participle(request)
            case _:
                raise NotImplementedError(f"Unsupported part: {self.word.part}")

    def _inflect_abbreviation(self, number: GrammaticalNumber, case: GrammaticalCase) -> BaseWord:
        for variation in self.variations:
            if case in variation.case and number in variation.number:
                return variation
        raise ValueError(f"Cannot inflect abbreviation: {self.word}")

    def _inflect_noun(
        self,
        number: GrammaticalNumber,
        case: GrammaticalCase,
    ) -> BaseWord:

        if is_word_inflectionally_independent(self.word):
            return self.word

        effective_number = GrammaticalNumber.PLURAL if self.word.is_pluralia_tantum else number
        for variation in self.variations:
            if case in variation.case and effective_number in variation.number:
                return variation

        raise ValueError(f"Cannot inflect noun: {self.word}")

    def _inflect_adjective(self, request: InflectionRequest) -> BaseWord:
        for variation in self.variations:
            if (
                request.number in variation.number
                and request.case in variation.case
                and request.gender in variation.gender
                and self.word.degree == variation.degree
                and variation.part == SentencePart.ADJECTIVE
            ):
                return variation

        raise ValueError(f"Cannot inflect adjective: {self.word}")

    def _inflect_passive_adjectival_participle(
        self,
        request: InflectionRequest,
    ) -> BaseWord:
        for variation in self.variations:
            if variation.part != SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE:
                continue
            if (
                request.number in variation.number
                and request.case in variation.case
                and request.gender in variation.gender
                and self.word.is_negation == variation.is_negation
            ):
                return variation

        raise ValueError(f"Cannot inflect passive adjectival participle: {self.word}")
