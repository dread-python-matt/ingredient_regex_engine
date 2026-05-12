import re
from dataclasses import dataclass
from unittest.mock import Mock

import pytest
from regex_engine import ResolvedIngredient
from regex_engine.application.use_cases.regex_resolver_default import RegexResolverDefault, is_number

from regex_engine.domain.enums import RegexKind
from regex_engine.domain.errors import UnfeasibleStandardisation


# ^ dostosuj importy do realnej ścieżki modułu


@dataclass(frozen=True)
class FakeMatch:
    stem: str


class FakeRegistry:
    def __init__(self, kind: RegexKind, entries: dict[str, str]):
        self.kind = kind
        self._entries = entries
        self.swap_calls: list[tuple[str, str]] = []

    def match_best(self, text: str):
        for phrase, stem in self._sorted_entries():
            if self._contains_phrase(text, phrase):
                return FakeMatch(stem=stem)
        return None

    def swap_match(self, text: str, replacement: str) -> str:
        self.swap_calls.append((text, replacement))

        result = text
        for phrase, _ in self._sorted_entries():
            result = re.sub(
                self._phrase_pattern(phrase),
                replacement,
                result,
                flags=re.IGNORECASE,
            )

        return " ".join(result.split())

    def _sorted_entries(self):
        return sorted(
            self._entries.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

    def _contains_phrase(self, text: str, phrase: str) -> bool:
        return bool(re.search(self._phrase_pattern(phrase), text, flags=re.IGNORECASE))

    @staticmethod
    def _phrase_pattern(phrase: str) -> str:
        return rf"(?<!\w){re.escape(phrase)}(?!\w)"


@pytest.fixture()
def amount_extractor():
    extractor = Mock()
    extractor.extract.return_value = 2.0
    return extractor


@pytest.fixture()
def ingredient_names():
    return FakeRegistry(
        RegexKind.INGREDIENT_NAME,
        {
            "mąki pszennej": "mąka pszenna",
            "jajka": "jajko",
            "mleka": "mleko",
        },
    )


@pytest.fixture()
def ingredient_conditions():
    return FakeRegistry(
        RegexKind.INGREDIENT_CONDITION,
        {
            "przesianej": "przesiana",
            "posiekane": "posiekane",
        },
    )


@pytest.fixture()
def unit_sizes():
    return FakeRegistry(
        RegexKind.UNIT_SIZE,
        {
            "duże": "duży",
            "małe": "mały",
        },
    )


@pytest.fixture()
def units():
    return FakeRegistry(
        RegexKind.UNIT,
        {
            "szklanki": "szklanka",
            "łyżki": "łyżka",
            "sztuki": "sztuka",
        },
    )


@pytest.fixture()
def or_conjunctions():
    return FakeRegistry(
        RegexKind.OR_CONJUNCTIONS,
        {
            "lub": "lub",
            "albo": "albo",
        },
    )


@pytest.fixture()
def and_conjunctions():
    return FakeRegistry(
        RegexKind.AND_CONJUNCTIONS,
        {
            "i": "i",
            "oraz": "oraz",
        },
    )


@pytest.fixture()
def resolver(
    amount_extractor,
    ingredient_names,
    ingredient_conditions,
    unit_sizes,
    units,
    or_conjunctions,
    and_conjunctions,
):
    return RegexResolverDefault(
        amount_extractor=amount_extractor,
        ingredient_names=ingredient_names,
        ingredient_conditions=ingredient_conditions,
        unit_sizes=unit_sizes,
        units=units,
        or_conjunctions=or_conjunctions,
        and_conjunctions=and_conjunctions,
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1", True),
        ("1.5", True),
        ("0", True),
        ("-2", True),
        ("mąka", False),
        ("1/2", False),
        ("", False),
    ],
    ids=[
        "integer",
        "decimal",
        "zero",
        "negative_number",
        "text",
        "fraction",
        "empty_string",
    ],
)
def test_should_detect_float_compatible_numbers(value, expected):
    assert is_number(value) is expected


@pytest.mark.parametrize(
    "ingredient",
    [
        "2 szklanki mąki pszennej",
        "2 duże szklanki przesianej mąki pszennej",
        "jajka",
        "2 szklanki mąki pszennej (opcjonalnie)",
    ],
    ids=[
        "amount_unit_and_ingredient_name",
        "amount_size_unit_condition_and_ingredient_name",
        "ingredient_name_without_amount",
        "extra_should_be_ignored",
    ],
)
def test_should_return_true_when_ingredient_can_be_standardized(resolver, ingredient):
    assert resolver.can_be_standardized(ingredient) is True


@pytest.mark.parametrize(
    "ingredient",
    [
        "2 szklanki kamieni",
        "2 duże garście mąki pszennej",
        "mąka pszenna z czymś nieznanym",
    ],
    ids=[
        "unknown_ingredient_name",
        "unknown_unit",
        "unknown_remainder",
    ],
)
def test_should_return_false_when_ingredient_contains_unknown_remainder(
    resolver,
    ingredient,
):
    assert resolver.can_be_standardized(ingredient) is False


def test_should_standardize_ingredient_by_replacing_known_parts_with_regex_kind_tokens(
    resolver,
):
    result = resolver.standardize("2 duże szklanki przesianej mąki pszennej")

    assert result == (
        "2 "
        f"{RegexKind.UNIT_SIZE.name} "
        f"{RegexKind.UNIT.name} "
        f"{RegexKind.INGREDIENT_CONDITION.name} "
        f"{RegexKind.INGREDIENT_NAME.name}"
    )


@pytest.mark.parametrize(
    ("ingredient", "expected"),
    [
        ("2 szklanki mąki pszennej (opcjonalnie)", "opcjonalnie"),
        ("2 szklanki mąki pszennej", ""),
        ("2 szklanki mąki pszennej (najlepiej świeżej)", "najlepiej świeżej"),
    ],
    ids=[
        "extra_present",
        "extra_missing",
        "extra_with_multiple_words",
    ],
)
def test_should_extract_extra_from_parentheses(resolver, ingredient, expected):
    assert resolver._extract_extra(ingredient) == expected


def test_should_remove_extra_from_ingredient(resolver):
    result = resolver._remove_extra("2 szklanki mąki pszennej (opcjonalnie)")

    assert result == "2 szklanki mąki pszennej"


def test_should_resolve_ingredient_when_input_can_be_fully_standardized(
    monkeypatch,
    resolver,
    amount_extractor,
    ingredient_names,
    ingredient_conditions,
    unit_sizes,
    units,
):
    def fake_from_dict(data):
        return data

    monkeypatch.setattr(
        ResolvedIngredient,
        "from_dict",
        staticmethod(fake_from_dict),
    )

    ingredient = "2 duże szklanki przesianej mąki pszennej (opcjonalnie)"

    result = resolver.resolve_ingredient(ingredient)

    assert result == {
        "raw_input": ingredient,
        "extra": "opcjonalnie",
        "amount": 2.0,
        RegexKind.INGREDIENT_NAME.value: "mąka pszenna",
        RegexKind.INGREDIENT_CONDITION.value: "przesiana",
        RegexKind.UNIT_SIZE.value: "duży",
        RegexKind.UNIT.value: "szklanka",
    }

    amount_extractor.extract.assert_called_once_with(ingredient)

    clean_ingredient = "2 duże szklanki przesianej mąki pszennej"

    assert (clean_ingredient, "") in ingredient_names.swap_calls
    assert (clean_ingredient, "") in ingredient_conditions.swap_calls
    assert (clean_ingredient, "") in unit_sizes.swap_calls
    assert (clean_ingredient, "") in units.swap_calls


def test_should_raise_unfeasible_standardisation_when_ingredient_cannot_be_standardized(
    resolver,
    amount_extractor,
):
    ingredient = "2 szklanki kamieni"

    with pytest.raises(
        UnfeasibleStandardisation,
        match="could not be fully standardized",
    ):
        resolver.resolve_ingredient(ingredient)

    amount_extractor.extract.assert_not_called()


def test_should_wrap_model_validation_error_as_unfeasible_standardisation(
    monkeypatch,
    resolver,
):
    def fake_from_dict(_data):
        raise ValueError("invalid resolved ingredient")

    monkeypatch.setattr(
        ResolvedIngredient,
        "from_dict",
        staticmethod(fake_from_dict),
    )

    with pytest.raises(
        UnfeasibleStandardisation,
        match="Failed to resolve ingredient",
    ) as exc_info:
        resolver.resolve_ingredient("2 szklanki mąki pszennej")

    assert isinstance(exc_info.value.__cause__, ValueError)