from dataclasses import dataclass, field
from typing import Optional

from regex_engine.domain.models.grammar import (
    GradationDegree,
    GrammaticalCase,
    GrammaticalGender,
    GrammaticalNumber,
    SentencePart,
)


@dataclass(slots=True, frozen=True, kw_only=True)
class BaseWord:
    lemma: str
    surface: str
    part: SentencePart
    is_negation: bool = False
    is_pluralia_tantum: bool = False
    number: frozenset[GrammaticalNumber] = field(default_factory=frozenset)
    case: frozenset[GrammaticalCase] = field(default_factory=frozenset)
    gender: frozenset[GrammaticalGender] = field(default_factory=frozenset)
    degree: Optional[GradationDegree] = None
    annotations: tuple[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "number", frozenset(self.number))
        object.__setattr__(self, "case", frozenset(self.case))
        object.__setattr__(self, "gender", frozenset(self.gender))
        object.__setattr__(self, "annotations", tuple(self.annotations))

    @classmethod
    def _split_tag(cls, value: str, index: int) -> list[str]:
        parts = value.split(":")
        if index >= len(parts):
            return []
        return parts[index].split(".")

    @classmethod
    def _to_part(cls, tag: str) -> SentencePart:
        try:
            part = SentencePart(tag)
        except ValueError:
            part = SentencePart.UNKNOWN
        return part
