from typing import Optional, Sequence

from regex_engine.domain.enums import RegexKind
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.ports.regex_registry import RegexRegistry


class RegexRegistryDefault(RegexRegistry):
    def __init__(self, kind: RegexKind, entries: list[RegexEntry]) -> None:
        self._kind = kind
        self._entries: list[RegexEntry] = entries
        self._by_stem: dict[str, RegexEntry] = self._create_by_stem()

    def _create_by_stem(self) -> dict[str, RegexEntry]:
        by_stem = {}
        for entry in self._entries:
            if entry.stem in by_stem:
                raise ValueError(f"Duplicate regex stem detected: {entry.stem}")
            by_stem[entry.stem] = entry
        return by_stem

    @property
    def kind(self) -> RegexKind:
        return self._kind

    def add_entry(self, entry: RegexEntry) -> None:
        if entry.stem in self._by_stem:
            raise ValueError(f"Stem '{entry.stem}' already exists")

        self._entries.append(entry)
        self._by_stem[entry.stem] = entry

    def remove_entry(self, stem: str) -> None:
        """
        Raises:
            KeyError: If stem does not exist.
        """
        entry = self._by_stem.pop(stem)
        self._entries.remove(entry)

    def add_variant(self, *, stem: str, variant: str) -> None:
        """
        Raises:
            KeyError: If stem does not exist.
        """
        entry = self._by_stem[stem]
        entry.add_variant(variant)

    def remove_variant(self, *, stem: str, variant: str) -> None:
        """
        Raises:
            KeyError: If stem does not exist.
        """
        entry = self._by_stem[stem]
        entry.remove_variant(variant)

    def match_best(self, text: str) -> Optional[RegexEntry]:
        text = text.strip()
        if not text:
            return None

        best: Optional[RegexEntry] = None
        best_len = -1

        for entry in self._entries:
            matching = entry.find(text)
            if not matching:
                continue

            length = len(matching[0])

            if length > best_len:
                best = entry
                best_len = length

        return best

    def swap_match(self, text: str, replacement: str) -> str:
        best: Optional[RegexEntry] = None
        best_len = -1
        best_start = None
        best_end = None

        for entry in self._entries:
            span = entry.find_spans(text)
            if not span:
                continue

            start, end = span[0]
            length = end - start

            if length > best_len:
                best = entry
                best_len = length
                best_start = start
                best_end = end

        if best is None:
            return text

        swapped = text[:best_start] + replacement + text[best_end:]

        return self.swap_match(swapped, replacement)

    def get(self, stem: str) -> Optional[RegexEntry]:
        return self._by_stem.get(stem)

    def get_all(self) -> Sequence[RegexEntry]:
        return tuple(sorted(self._entries, key=lambda entry: entry.stem))
