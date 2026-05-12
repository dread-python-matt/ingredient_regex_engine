from regex_engine.domain.enums import RegexKind
from regex_engine.domain.errors import DemoModeError
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.domain.models.regex_registry_default import RegexRegistryDefault
from regex_engine.ports.regex_registry import RegexRegistry


def _build_entry(word):
    return RegexEntry(stem=word, variants=[word])


def _build_registry(kind: RegexKind, words: dict[str, list[str]]) -> RegexRegistry:
    return RegexRegistryDefault(kind, [_build_entry(word) for word in words])


class DemoRegexRepository:
    or_conjunctions = {
        "albo": ["albo"],
        "bądź": ["bądź"],
        "ewentualnie": ["ewentualnie"],
        "lub": ["lub"],
        "lub_też": ["lub też"],
    }
    and_conjunctions = {"i": ["i"], "oraz": ["oraz"]}

    mapping = {
        RegexKind.OR_CONJUNCTIONS: _build_registry(RegexKind.OR_CONJUNCTIONS, or_conjunctions),
        RegexKind.AND_CONJUNCTIONS: _build_registry(RegexKind.AND_CONJUNCTIONS, and_conjunctions),
        RegexKind.INGREDIENT_NAME: _build_registry(RegexKind.INGREDIENT_NAME, {}),
        RegexKind.INGREDIENT_CONDITION: _build_registry(RegexKind.INGREDIENT_CONDITION, {}),
        RegexKind.UNIT: _build_registry(RegexKind.UNIT, {}),
        RegexKind.UNIT_SIZE: _build_registry(RegexKind.UNIT_SIZE, {}),
    }

    def load(self, kind: RegexKind) -> RegexRegistry:
        return self.mapping[kind]

    def save(self, registry: RegexRegistry) -> None:
        raise DemoModeError("Save is not supported")
