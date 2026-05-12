from typing import NamedTuple

from regex_engine.adapters.normalizers.morfeusz.inflector.inflection_request import (
    InflectionRequest,
)
from regex_engine.adapters.normalizers.morfeusz.inflector.inflector import Inflector
from regex_engine.adapters.normalizers.morfeusz.inflector.inflector_paradigm import (
    InflectionParadigm,
)
from regex_engine.adapters.normalizers.morfeusz.morfeusz_utils import join_tokens
from regex_engine.adapters.normalizers.morfeusz.phrase_analyzer import PhraseAnalyser
from regex_engine.application.dto.analysed_phrase import AnalysedPhrase
from regex_engine.domain.models.grammar import GrammaticalCase, GrammaticalNumber


class InflectionPair(NamedTuple):
    subject: InflectionRequest
    dependent_noun: InflectionRequest


class MorfeuszIngredientNameNormalizer:
    CASES_BY_NUMBER = {
        GrammaticalNumber.SINGULAR: [
            GrammaticalCase.NOMINATIVE,
            GrammaticalCase.GENITIVE,
            GrammaticalCase.ACCUSATIVE,
            GrammaticalCase.INSTRUMENTAL,
        ],
        GrammaticalNumber.PLURAL: [
            GrammaticalCase.NOMINATIVE,
            GrammaticalCase.GENITIVE,
            GrammaticalCase.INSTRUMENTAL,
        ],
    }

    DEFAULT_STEM_VARIATION = InflectionPair(
        subject=InflectionRequest(GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE),
        dependent_noun=InflectionRequest(GrammaticalNumber.SINGULAR, GrammaticalCase.NOMINATIVE),
    )

    def __init__(
        self,
        inflector: Inflector,
        phrase_analyser: PhraseAnalyser,
        stem_variant: InflectionPair | None = None,
        inflection_variations: tuple[InflectionPair] = tuple(),
    ):
        self._inflector = inflector
        self._phrase_analyser = phrase_analyser

        self._stem_variant = stem_variant if stem_variant else self.DEFAULT_STEM_VARIATION

        self._inflection_variations = (
            inflection_variations
            if inflection_variations
            else self._build_default_inflection_variations()
        )

        self._analysed_phrase: AnalysedPhrase | None = None

        self._subject_inflector = None
        self._subject_adjectives_inflectors: dict[int, InflectionParadigm] = {}
        self._dependent_noun_inflector = None
        self._dependent_adjectives_inflectors: dict[int, InflectionParadigm] = {}

    async def stem(self, ingredient_name: str) -> str:
        self._prepare(ingredient_name)

        return self._inflect(self._stem_variant)

    async def inflect(self, stem: str) -> set[str]:
        self._prepare(stem)
        result = []
        for inflection in self._inflection_variations:
            result.append(self._inflect(inflection))

        return set(result)

    def _build_default_inflection_variations(self):
        result = []

        for number, cases in self.CASES_BY_NUMBER.items():
            for case in cases:
                result.append(
                    InflectionPair(
                        subject=InflectionRequest(number, case),
                        dependent_noun=InflectionRequest(number, case),
                    )
                )

        for number, cases in self.CASES_BY_NUMBER.items():
            for case in cases:
                result.append(
                    InflectionPair(
                        subject=InflectionRequest(number, case),
                        dependent_noun=InflectionRequest(number, GrammaticalCase.GENITIVE),
                    )
                )

        return tuple(result)

    def _inflect(self, inflection_pair: InflectionPair) -> str:
        analysed_phrase = self._analysed_phrase
        inflected: dict[int, str] = analysed_phrase.phrase

        subject = self._subject_inflector.inflect(inflection_pair.subject)
        inflected[analysed_phrase.subject.position] = subject.surface
        sub_gender = subject.gender

        sub_number, sub_case = inflection_pair.subject.number, inflection_pair.subject.case
        if analysed_phrase.subject.word.is_pluralia_tantum:
            sub_number = GrammaticalNumber.PLURAL

        for sub_adj in analysed_phrase.subject_adjectives:
            inflected[sub_adj.position] = (
                self._subject_adjectives_inflectors[sub_adj.position].inflect(
                    InflectionRequest(sub_number, sub_case, sub_gender)
                )
            ).surface

        if analysed_phrase.dependent_noun:
            dep_noun_number = inflection_pair.dependent_noun.number
            dep_noun_case = inflection_pair.dependent_noun.case
            dependent_noun = self._dependent_noun_inflector.inflect(
                InflectionRequest(dep_noun_number, dep_noun_case)
            )
            dep_noun_gender = dependent_noun.gender
            inflected[analysed_phrase.dependent_noun.position] = dependent_noun.surface

            if analysed_phrase.dependent_noun.word.is_pluralia_tantum:
                dep_noun_number = GrammaticalNumber.PLURAL

            for dep_noun_adj in analysed_phrase.dependent_noun_adjectives:
                inflected[dep_noun_adj.position] = (
                    self._dependent_adjectives_inflectors[dep_noun_adj.position].inflect(
                        InflectionRequest(dep_noun_number, dep_noun_case, dep_noun_gender)
                    )
                ).surface

        return join_tokens(inflected)

    def _clear(self):
        self._analysed_phrase = None
        self._subject_inflector = None
        self._subject_adjectives_inflectors.clear()
        self._dependent_noun_inflector = None
        self._dependent_adjectives_inflectors.clear()

    def _prepare(self, ingredient_name: str):
        self._clear()
        analysed_phrase = self._phrase_analyser.analyse(ingredient_name)
        self._analysed_phrase = analysed_phrase

        self._subject_inflector = self._inflector.prepare(analysed_phrase.subject.word)

        for subj_adj in analysed_phrase.subject_adjectives:
            self._subject_adjectives_inflectors[subj_adj.position] = self._inflector.prepare(
                subj_adj.word
            )

        if analysed_phrase.dependent_noun:
            self._dependent_noun_inflector = self._inflector.prepare(
                analysed_phrase.dependent_noun.word
            )
            for noun_adjective in analysed_phrase.dependent_noun_adjectives:
                self._dependent_adjectives_inflectors[noun_adjective.position] = (
                    self._inflector.prepare(noun_adjective.word)
                )
