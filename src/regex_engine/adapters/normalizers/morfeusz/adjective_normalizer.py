from morfeusz2 import Morfeusz

from regex_engine.adapters.normalizers.morfeusz.inflector.inflection_request import (
    InflectionRequest,
)
from regex_engine.adapters.normalizers.morfeusz.inflector.inflector import Inflector
from regex_engine.adapters.normalizers.morfeusz.inflector.inflector_paradigm import (
    InflectionParadigm,
)
from regex_engine.adapters.normalizers.morfeusz.morfeusz_utils import tuples_to_word_analysis
from regex_engine.application.dto.base_word import BaseWord
from regex_engine.domain.models.grammar import (
    GrammaticalCase,
    GrammaticalGender,
    GrammaticalNumber,
    SentencePart,
)


def _choose_first_adj_or_pap(words: list[BaseWord]) -> BaseWord:
    for word in words:
        part = word.part
        if part == SentencePart.ADJECTIVE or part == SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE:
            return word

    raise ValueError(f"Could not find adjective or passive adjective participle in {words}")


class MorfeuszAdjectiveNormalizer:
    def __init__(self, inflector: Inflector, morfeusz: Morfeusz):
        self._inflector = inflector
        self._morfeusz = morfeusz
        self._inflections = [
            InflectionRequest(number, case, gender)
            for number, case in [
                (GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE),
                (GrammaticalNumber.SINGULAR, GrammaticalCase.GENITIVE),
                (GrammaticalNumber.SINGULAR, GrammaticalCase.ACCUSATIVE),
                (GrammaticalNumber.SINGULAR, GrammaticalCase.INSTRUMENTAL),
                (GrammaticalNumber.PLURAL, GrammaticalCase.NOMINATIVE),
                (GrammaticalNumber.PLURAL, GrammaticalCase.GENITIVE),
                (GrammaticalNumber.PLURAL, GrammaticalCase.INSTRUMENTAL),
            ]
            for gender in [
                GrammaticalGender.MASC_INANIMATE,
                GrammaticalGender.FEMININE,
                GrammaticalGender.NEUTER,
            ]
        ]

        self._adjective: BaseWord | None = None
        self._adjective_inflector: InflectionParadigm | None = None

    async def stem(self, adjective: str) -> str:
        self._prepare(adjective)
        return self._adjective_inflector.inflect(
            InflectionRequest(
                GrammaticalNumber.SINGULAR,
                GrammaticalCase.NOMINATIVE,
                GrammaticalGender.MASC_INANIMATE,
            )
        ).surface

    async def inflect(self, stem: str) -> set[str]:
        self._prepare(stem)

        return set(
            self._adjective_inflector.inflect(inflection).surface
            for inflection in self._inflections
        )

    def _prepare(self, adjective: str) -> None:
        converted = self._convert_to_single_base_word(adjective)
        adjective_word = _choose_first_adj_or_pap(converted)
        self._adjective = adjective_word
        self._adjective_inflector = self._inflector.prepare(adjective_word)

    def _convert_to_single_base_word(self, adjective: str) -> list[BaseWord]:
        analyses = self._morfeusz.analyse(adjective)
        last_analyse_position = analyses[-1][0]
        if last_analyse_position != 0:
            raise ValueError(f"Multiple words detected {adjective}")

        return tuples_to_word_analysis(analyses)
