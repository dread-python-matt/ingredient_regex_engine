import logging
from collections import defaultdict
from typing import Optional

from morfeusz2 import Morfeusz

from regex_engine.adapters.normalizers.morfeusz.morfeusz_utils import (
    filter_non_cooking_related,
    is_word_inflectionally_independent,
    join_tokens,
    split_phrase,
    tuples_to_word_analysis,
)
from regex_engine.application.dto.analysed_phrase import AnalysedPhrase
from regex_engine.application.dto.positioned_word import PositionedWord
from regex_engine.application.dto.word_analysis import WordAnalysis
from regex_engine.domain.models.grammar import GrammaticalCase, GrammaticalNumber, SentencePart

logger = logging.getLogger("phrase_analyzer")


class PhraseAnalyser:
    def __init__(self, morfeusz: Morfeusz):
        self.morfeusz = morfeusz

        self._numbered_phrase: dict[int, str] = {}
        self._phrase_analysis: list[WordAnalysis] = []

        self._subject_index: int = -1
        self._subject: Optional[WordAnalysis] = None
        self._subject_variations: list[WordAnalysis] = []

        self._subject_related_adjectives: dict[int, WordAnalysis] = {}
        self._subject_related_adjectives_variations: dict[int, list[WordAnalysis]] = {}

        self._dependent_noun: Optional[WordAnalysis] = None
        self._dependent_noun_variations: list[WordAnalysis] = []

        self._dependent_noun_related_adjectives: dict[int, WordAnalysis] = {}
        self._dependent_noun_related_adjectives_variations: dict[int, list[WordAnalysis]] = {}

    def analyse(self, phrase: str) -> AnalysedPhrase:
        try:
            self._prepare(phrase)
            self._prepare_subject_variations()
            self._prepare_dependent_noun_variations()
            self._prepare_subject_related_adjectives()
            self._prepare_dependent_noun_related_adjectives()

            self._determine_correct_subject()
            self._determine_correct_dependent_noun()
            self._determine_subject_related_adjectives()
            self._determine_dependent_noun_adjectives()

            return self._create_analysed_phrase()
        finally:
            self._clear()

    def _prepare(self, phrase: str):
        phrase_analysis = self.morfeusz.analyse(phrase)

        self._numbered_phrase = split_phrase(phrase)

        word_analysis = tuples_to_word_analysis(phrase_analysis)

        self._phrase_analysis = filter_non_cooking_related(word_analysis)

        subject_index = self._find_first_noun_index()
        self._subject_index = subject_index

    def _prepare_subject_variations(self):
        if self._subject_index == -1:
            raise ValueError("Subject index is undefined")
        self._subject_variations = self._get_word_analysis_by_index(self._subject_index)

    def _prepare_dependent_noun_variations(self):
        right_neighbour_variations = self._get_word_analysis_by_index(self._subject_index + 1)
        self._dependent_noun_variations = [
            word for word in right_neighbour_variations if word.part == SentencePart.NOUN.value
        ]

    def _prepare_subject_related_adjectives(self):
        if self._dependent_noun_variations:
            self._subject_related_adjectives_variations = self._get_related_adjectives(
                self._subject_index, -1
            )
        else:
            self._subject_related_adjectives_variations = self._get_related_adjectives(
                self._subject_index, -1
            )
            self._subject_related_adjectives_variations.update(
                self._get_related_adjectives(self._subject_index, 1)
            )

    def _prepare_dependent_noun_related_adjectives(self):
        if not self._dependent_noun_variations:
            return
        self._dependent_noun_related_adjectives_variations = self._get_related_adjectives(
            self._subject_index + 1, 1
        )

    def _determine_correct_subject(self):
        if len(self._subject_variations) == 1:
            self._subject = self._subject_variations[0]
            return

        for variation in self._subject_variations:
            if is_word_inflectionally_independent(variation):
                self._subject = variation
                return

        def _matches_adjective(subject, adjective):
            return (
                subject.gender & adjective.gender
                and subject.case & adjective.case
                and subject.number & adjective.number
            )

        if self._subject_related_adjectives_variations:
            subject_combinations = defaultdict(int)

            for subject_variation in self._subject_variations:
                for adjective_variations in self._subject_related_adjectives_variations.values():
                    for adjective_variation in adjective_variations:
                        if _matches_adjective(subject_variation, adjective_variation):
                            subject_combinations[subject_variation] += 1
                            break

            self._subject = max(subject_combinations, key=subject_combinations.get)
            return

        self._subject = self._subject_variations[0]

    def _determine_correct_dependent_noun(self):
        if not self._dependent_noun_variations:
            return

        if len(self._dependent_noun_variations) == 1:
            self._dependent_noun = self._dependent_noun_variations[0]
            return

        for variation in self._dependent_noun_variations:
            if is_word_inflectionally_independent(variation):
                self._dependent_noun = variation

        def _matches_adjective(noun, adjective):
            return (
                noun.gender & adjective.gender
                and noun.case & adjective.case
                and noun.number & adjective.number
            )

        if self._dependent_noun_related_adjectives_variations:
            noun_combinations = defaultdict(int)

            for noun_variation in self._dependent_noun_variations:
                for (
                    adjective_variations
                ) in self._dependent_noun_related_adjectives_variations.values():
                    for adjective_variation in adjective_variations:
                        if _matches_adjective(noun_variation, adjective_variation):
                            noun_combinations[noun_variation] += 1
                            break

            self._dependent_noun = max(noun_combinations, key=noun_combinations.get)
            return

        self._dependent_noun = self._dependent_noun_variations[0]

    def _determine_dependent_noun_adjectives(self) -> None:
        if not self._dependent_noun_variations:
            return

        if not self._dependent_noun:
            raise ValueError("Dependent noun not specified")

        noun = self._dependent_noun
        noun_number = {GrammaticalNumber.PLURAL} if noun.is_pluralia_tantum else noun.number
        noun_case = noun.case
        noun_gender = noun.gender

        def matches_noun(adjective) -> bool:
            return (
                noun_number & adjective.number
                and noun_case & adjective.case
                and noun_gender & adjective.gender
            )

        for index, adjectives in self._dependent_noun_related_adjectives_variations.items():
            match = next((adjective for adjective in adjectives if matches_noun(adjective)), None)
            if not match:
                logger.warning(
                    "Could not determine dependent noun adjective: %s.", adjectives[0].surface
                )
                raise ValueError(
                    f"Could not determine dependent noun adjective: {adjectives[0].surface}."
                )

            self._dependent_noun_related_adjectives[index] = match

    def _determine_subject_related_adjectives(self) -> None:
        if not self._subject_related_adjectives_variations:
            return

        if not self._subject:
            raise ValueError("Subject not specified")

        subject = self._subject
        subject_number = (
            {GrammaticalNumber.PLURAL} if subject.is_pluralia_tantum else subject.number
        )

        subject_case = (
            set(GrammaticalCase) if is_word_inflectionally_independent(subject) else subject.case
        )
        subject_gender = subject.gender

        def matches_subject(adjective) -> bool:
            return (
                subject_number & adjective.number
                and subject_case & adjective.case
                and subject_gender & adjective.gender
            )

        for index, adjectives in self._subject_related_adjectives_variations.items():
            match = next(
                (adjective for adjective in adjectives if matches_subject(adjective)), None
            )

            if match is None:
                logger.warning(
                    "Could not determine subject related adjective: %s. ",
                    adjectives[0].surface,
                )
                raise ValueError(
                    f"Could not determine subject related adjective: {adjectives[0].surface}."
                )

            self._subject_related_adjectives[index] = match

    def _create_analysed_phrase(self) -> AnalysedPhrase:
        n_subject = PositionedWord(self._subject.position, self._subject)
        n_dependent_noun = None
        n_subject_adjectives = []
        n_dependent_noun_adjectives = []
        if self._dependent_noun:
            n_dependent_noun = PositionedWord(self._dependent_noun.position, self._dependent_noun)
            for position, adjective in self._dependent_noun_related_adjectives.items():
                n_dependent_noun_adjectives.append(PositionedWord(position, adjective))

        for position, subj_adj in self._subject_related_adjectives.items():
            n_subject_adjectives.append(PositionedWord(position, subj_adj))

        return AnalysedPhrase(
            subject=n_subject,
            dependent_noun=n_dependent_noun,
            subject_adjectives=n_subject_adjectives,
            dependent_noun_adjectives=n_dependent_noun_adjectives,
            phrase=self._numbered_phrase.copy(),
        )

    def _clear(self):
        self._numbered_phrase.clear()
        self._phrase_analysis.clear()

        self._subject_index: int = -1
        self._subject: Optional[WordAnalysis] = None
        self._subject_variations.clear()

        self._subject_related_adjectives.clear()
        self._subject_related_adjectives_variations.clear()

        self._dependent_noun: Optional[WordAnalysis] = None
        self._dependent_noun_variations.clear()

        self._dependent_noun_related_adjectives.clear()
        self._dependent_noun_related_adjectives_variations.clear()

    def _get_related_adjectives(self, index: int, direction: int) -> dict[int, list[WordAnalysis]]:
        allowed_parts = {
            SentencePart.ADJECTIVE,
            SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
        }
        bridge_parts = {
            SentencePart.PUNCTUATION_MARK,
            SentencePart.CONJUNCTION,
        }
        result: dict[int, list[WordAnalysis]] = {}

        if direction not in (-1, 1):
            raise ValueError("direction must be -1 or 1")

        if direction == 1:
            start = index + 1
            stop = len(self._numbered_phrase)
        else:
            start = index - 1
            stop = -1

        for index in range(start, stop, direction):
            variations = self._get_word_analysis_by_index(index)
            parts = {variation.part for variation in variations}

            adjective_variations = [
                variation for variation in variations if variation.part in allowed_parts
            ]

            if adjective_variations:
                result[index] = adjective_variations

            if not (parts & allowed_parts or parts & bridge_parts):
                break

        return result

    def _find_first_noun_index(self) -> int:
        def _does_index_has_any_adjectives(index: int) -> bool:
            for analysis in self._get_word_analysis_by_index(index):
                if analysis.part == SentencePart.ADJECTIVE:
                    return True
            return False

        sorted_analysis = sorted(self._phrase_analysis, key=lambda w: w.position)

        for word in sorted_analysis:
            if word.part == SentencePart.NOUN.value:
                if not _does_index_has_any_adjectives(word.position):
                    return word.position

        raise ValueError(
            "Could not determine subject in phrase: %s", join_tokens(self._numbered_phrase)
        )

    def _get_word_analysis_by_index(self, index: int):
        return [word for word in self._phrase_analysis if word.position == index]
