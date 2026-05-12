import re
from dataclasses import dataclass, field
from typing import Iterable


def _is_empty(word: str) -> bool:
    if len(word.strip()) == 0:
        return True
    return False


def _normalize_stem(stem: str):
    return "_".join(stem.split())


@dataclass(eq=False)
class RegexEntry:
    _stem: str
    _pattern: re.Pattern
    _variants: set[str] = field(default_factory=set)

    def __init__(self, stem: str, variants: Iterable[str]):
        if _is_empty(stem):
            raise ValueError(f"stem {stem} cannot be empty")
        self._stem = _normalize_stem(stem)
        self._variants = set(variants)
        self._compile()

    def _compile(self) -> None:
        variants = sorted(
            {v.strip() for v in self.variants if v and v.strip()},
            key=lambda s: (-len(s), s),
        )
        alts = "|".join(map(re.escape, variants))
        self._pattern = re.compile(rf"\b(?:{alts})\b", re.IGNORECASE)

    @property
    def stem(self):
        return self._stem

    @property
    def variants(self):
        return frozenset(self._variants)

    @property
    def pattern(self):
        return self._pattern

    def contains(self, text: str) -> bool:
        return bool(self._pattern.search(text))

    def find(self, text: str) -> list[str]:
        return [m.group(0) for m in self._pattern.finditer(text)]

    def find_spans(self, text: str) -> list[tuple[int, int]]:
        return [(m.start(), m.end()) for m in self._pattern.finditer(text)]

    def add_variant(self, variant: str) -> None:
        variant = variant.strip()
        if not variant:
            return

        if variant in self._variants:
            return

        self._variants.add(variant)

        self._compile()

    def remove_variant(self, variant: str) -> None:
        variant = variant.strip()
        if not variant:
            return

        if variant not in self.variants:
            return

        self._variants.remove(variant)
        self._compile()

    def __hash__(self) -> int:
        return hash(self.stem)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RegexEntry) and self.stem == other.stem
