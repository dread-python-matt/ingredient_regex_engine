from dataclasses import dataclass, field
from typing import Optional

from regex_engine.application.dto.positioned_word import PositionedWord


@dataclass(frozen=True)
class AnalysedPhrase:
    subject: PositionedWord
    phrase: dict[int, str]
    dependent_noun: Optional[PositionedWord] = None
    subject_adjectives: list[PositionedWord] = field(default_factory=list)
    dependent_noun_adjectives: list[PositionedWord] = field(default_factory=list)
