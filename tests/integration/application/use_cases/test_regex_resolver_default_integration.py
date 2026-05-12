import pytest
from regex_engine.application.use_cases.amount_extractor_default import AmountExtractorDefault
from regex_engine.application.use_cases.regex_resolver_default import RegexResolverDefault

from regex_engine.domain.enums import RegexKind
from regex_engine.domain.errors import UnfeasibleStandardisation
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.domain.models.regex_registry_default import RegexRegistryDefault




def make_entry(stem: str, *variants: str) -> RegexEntry:
    return RegexEntry(stem=stem, variants=variants)


def make_registry(kind: RegexKind, *entries: RegexEntry) -> RegexRegistryDefault:
    return RegexRegistryDefault(kind=kind, entries=list(entries))


@pytest.fixture()
def ingredient_names() -> RegexRegistryDefault:
    return make_registry(
        RegexKind.INGREDIENT_NAME,
        make_entry("mąka_pszenna", "mąka pszenna", "mąki pszennej", "mąki"),
        make_entry("mleko", "mleko", "mleka"),
        make_entry("oliwa", "oliwa", "oliwy"),
        make_entry("jajko", "jajko", "jajka", "jajek"),
        make_entry("sól", "sól", "soli"),
    )


@pytest.fixture()
def ingredient_conditions() -> RegexRegistryDefault:
    return make_registry(
        RegexKind.INGREDIENT_CONDITION,
        make_entry("przesiana", "przesiana", "przesianej"),
        make_entry("posiekany", "posiekany", "posiekana", "posiekane", "posiekanej"),
    )


@pytest.fixture()
def unit_sizes() -> RegexRegistryDefault:
    return make_registry(
        RegexKind.UNIT_SIZE,
        make_entry("duży", "duży", "duża", "duże", "dużych"),
        make_entry("mały", "mały", "mała", "małe", "małych"),
    )


@pytest.fixture()
def units() -> RegexRegistryDefault:
    return make_registry(
        RegexKind.UNIT,
        make_entry("szklanka", "szklanka", "szklanki", "szklanek"),
        make_entry("łyżka", "łyżka", "łyżki", "łyżek"),
        make_entry("łyżeczka", "łyżeczka", "łyżeczki", "łyżeczek"),
        make_entry("sztuka", "sztuka", "sztuki", "sztuk"),
        make_entry("szczypta", "szczypta", "szczypty"),
    )


@pytest.fixture()
def or_conjunctions() -> RegexRegistryDefault:
    return make_registry(
        RegexKind.OR_CONJUNCTIONS,
        make_entry("lub", "lub"),
        make_entry("albo", "albo"),
    )


@pytest.fixture()
def and_conjunctions() -> RegexRegistryDefault:
    return make_registry(
        RegexKind.AND_CONJUNCTIONS,
        make_entry("i", "i"),
        make_entry("oraz", "oraz"),
    )


@pytest.fixture()
def amount_extractor(and_conjunctions: RegexRegistryDefault) -> AmountExtractorDefault:
    return AmountExtractorDefault(and_conjunctions=and_conjunctions)


@pytest.fixture()
def resolver(
    amount_extractor: AmountExtractorDefault,
    ingredient_names: RegexRegistryDefault,
    ingredient_conditions: RegexRegistryDefault,
    unit_sizes: RegexRegistryDefault,
    units: RegexRegistryDefault,
    or_conjunctions: RegexRegistryDefault,
    and_conjunctions: RegexRegistryDefault,
) -> RegexResolverDefault:
    return RegexResolverDefault(
        amount_extractor=amount_extractor,
        ingredient_names=ingredient_names,
        ingredient_conditions=ingredient_conditions,
        unit_sizes=unit_sizes,
        units=units,
        or_conjunctions=or_conjunctions,
        and_conjunctions=and_conjunctions,
    )


def test_should_resolve_full_ingredient_with_real_registries(resolver):
    ingredient = "2 duże szklanki przesianej mąki pszennej (opcjonalnie)"

    result = resolver.resolve_ingredient(ingredient)

    assert result.raw_input == ingredient
    assert result.amount == 2.0
    assert result.unit_size == "duży"
    assert result.unit == "szklanka"
    assert result.condition == "przesiana"
    assert result.name == "mąka_pszenna"
    assert result.extra == "opcjonalnie"


def test_should_resolve_ingredient_without_numeric_amount_as_default_amount(resolver):
    result = resolver.resolve_ingredient("szczypta soli")

    assert result.raw_input == "szczypta soli"
    assert result.amount == 1.0
    assert result.unit == "szczypta"
    assert result.name == "sól"
    assert result.unit_size is None
    assert result.condition is None
    assert result.extra == ""


@pytest.mark.parametrize(
    ("ingredient", "expected_amount", "expected_unit", "expected_name"),
    [
        ("1/2 szklanki mleka", 0.5, "szklanka", "mleko"),
        ("1.5 łyżki oliwy", 1.5, "łyżka", "oliwa"),
        ("2 jajka", 2.0, None, "jajko"),
    ],
    ids=[
        "fraction_amount",
        "decimal_amount",
        "integer_amount_without_unit",
    ],
)
def test_should_resolve_supported_amount_formats(
    resolver,
    ingredient,
    expected_amount,
    expected_unit,
    expected_name,
):
    result = resolver.resolve_ingredient(ingredient)

    assert result.raw_input == ingredient
    assert result.amount == pytest.approx(expected_amount)
    assert result.unit == expected_unit
    assert result.name == expected_name


@pytest.mark.parametrize(
    ("ingredient", "expected_amount"),
    [
        ("1 i 1/2 szklanki mleka", 1.5),
        ("2 i 1/4 szklanki mleka", 2.25),
        ("1 oraz 0.5 łyżki oliwy", 1.5),
    ],
    ids=[
        "integer_and_fraction_with_i",
        "integer_and_quarter_fraction_with_i",
        "integer_and_decimal_with_oraz",
    ],
)
def test_should_resolve_mixed_amount_joined_by_and_conjunction(
    resolver,
    ingredient,
    expected_amount,
):
    result = resolver.resolve_ingredient(ingredient)

    assert result.raw_input == ingredient
    assert result.amount == pytest.approx(expected_amount)


def test_should_resolve_mixed_fraction_amount_with_unit_and_name(resolver):
    result = resolver.resolve_ingredient("1 i 1/2 szklanki mleka")

    assert result.amount == pytest.approx(1.5)
    assert result.unit == "szklanka"
    assert result.name == "mleko"


def test_should_resolve_ingredient_with_condition_but_without_unit_size(resolver):
    result = resolver.resolve_ingredient("2 łyżki posiekanej oliwy")

    assert result.amount == 2.0
    assert result.unit == "łyżka"
    assert result.condition == "posiekany"
    assert result.name == "oliwa"
    assert result.unit_size is None


def test_should_resolve_ingredient_with_unit_size_but_without_condition(resolver):
    result = resolver.resolve_ingredient("2 duże jajka")

    assert result.amount == 2.0
    assert result.unit_size == "duży"
    assert result.name == "jajko"
    assert result.unit is None
    assert result.condition is None


def test_should_standardize_ingredient_using_real_registry_pipeline(resolver):
    result = resolver.standardize("2 duże szklanki przesianej mąki pszennej")

    assert result == (
        f"2 {RegexKind.UNIT_SIZE.name} "
        f"{RegexKind.UNIT.name} "
        f"{RegexKind.INGREDIENT_CONDITION.name} "
        f"{RegexKind.INGREDIENT_NAME.name}"
    )


@pytest.mark.parametrize(
    "ingredient",
    [
        "2 szklanki kamieni",
        "2 garście mąki pszennej",
        "2 szklanki mąki pszennej premium",
    ],
    ids=[
        "unknown_ingredient_name",
        "unknown_unit",
        "unknown_remainder",
    ],
)
def test_should_raise_unfeasible_standardisation_when_ingredient_cannot_be_fully_standardized(
    resolver,
    ingredient,
):
    with pytest.raises(
        UnfeasibleStandardisation,
        match="could not be fully standardized",
    ):
        resolver.resolve_ingredient(ingredient)