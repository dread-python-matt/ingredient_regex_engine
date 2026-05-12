from dataclasses import dataclass
from typing import Optional

from regex_engine.domain.enums import EnsureWordStatus, RegexKind


@dataclass(slots=True, frozen=True)
class EnsureWordResult:
    kind: RegexKind
    status: EnsureWordStatus
    stem: str
    word: str
    exception: Optional[Exception] = None


@dataclass(slots=True, frozen=True)
class EnsureIngredientResult:
    failed: bool
    raw_input: str
    name: EnsureWordResult
    items: dict[RegexKind, EnsureWordResult]

    def iter_errors(self):
        for r in self.items.values():
            if r.exception:
                yield r

        if self.name.exception:
            yield self.name
