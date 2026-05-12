from dataclasses import dataclass
from typing import Optional

from regex_engine.application.dto.base_word import BaseWord
from regex_engine.domain.models.grammar import (
    GradationDegree,
    GrammaticalCase,
    GrammaticalGender,
    GrammaticalNumber,
    SentencePart,
)


@dataclass(slots=True, frozen=True)
class WordAnalysis(BaseWord):
    position: int

    @classmethod
    def _build(
        cls,
        position: int,
        lemma: str,
        surface: str,
        part: SentencePart,
        is_negation: bool = False,
        is_pluralia_tantum=False,
        number: Optional[set[GrammaticalNumber]] = None,
        case: Optional[set[GrammaticalCase]] = None,
        gender: Optional[set[GrammaticalGender]] = None,
        degree: Optional[GradationDegree] = None,
        annotations: Optional[list[str]] = None,
    ) -> "WordAnalysis":
        return cls(
            position=position,
            lemma=lemma,
            surface=surface,
            part=part,
            is_negation=is_negation,
            is_pluralia_tantum=is_pluralia_tantum,
            number=number or frozenset(),
            case=case or frozenset(),
            gender=gender or frozenset(),
            degree=degree,
            annotations=annotations or tuple(),
        )

    @classmethod
    def from_tuple(cls, analysis: tuple) -> "WordAnalysis":
        position, _, data = analysis
        surface, lemma, morph_tag, _, annotations = data

        tags = morph_tag.split(":")
        part = cls._to_part(tags[0])

        base = {
            "position": position,
            "lemma": lemma,
            "surface": surface,
            "part": part,
            "annotations": annotations,
        }

        common_inflected_parts = {
            SentencePart.NOUN,
            SentencePart.ADJECTIVE,
            SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE,
            SentencePart.ACTIVE_PARTICIPLE,
        }

        if part in common_inflected_parts:
            base["number"] = set(cls._split_tag(morph_tag, 1))
            base["case"] = set(cls._split_tag(morph_tag, 2))
            base["gender"] = set(cls._split_tag(morph_tag, 3))

        if part in (SentencePart.PASSIVE_ADJECTIVAL_PARTICIPLE, SentencePart.ACTIVE_PARTICIPLE):
            base["is_negation"] = "neg" in tags

        if part is SentencePart.NOUN:
            base["is_pluralia_tantum"] = "pt" in tags

        if part is SentencePart.ADJECTIVE:
            degree_values = cls._split_tag(morph_tag, 4)
            base["degree"] = GradationDegree(degree_values[0]) if degree_values else None

        return cls._build(**base)
