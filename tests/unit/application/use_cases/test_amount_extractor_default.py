import pytest
from unittest.mock import Mock

from regex_engine.application.use_cases.amount_extractor_default import AmountExtractorDefault
from regex_engine.domain.errors import AmountExtractionError


@pytest.fixture()
def and_conjunctions_registry():
    registry = Mock()

    def match_best(word: str):
        return word if word in {"i", "oraz"} else None

    registry.match_best.side_effect = match_best
    return registry


@pytest.fixture()
def extractor(and_conjunctions_registry):
    return AmountExtractorDefault(and_conjunctions_registry)


@pytest.mark.parametrize(
    ("ingredient", "expected"),
    [
        ("2 jajka", 2.0),
        ("1/2 szklanki mleka", 0.5),
        ("1.5 łyżki oliwy", 1.5),
        ("0 cukru", 0.0),
    ],
    ids=[
        "integer_amount",
        "fraction_amount",
        "decimal_amount",
        "zero_amount",
    ],
)
def test_should_extract_single_amount_when_ingredient_starts_with_number(
    extractor,
    ingredient,
    expected,
):
    assert extractor.extract(ingredient) == expected


@pytest.mark.parametrize(
    ("ingredient", "expected"),
    [
        ("1 i 1/2 szklanki mąki", 1.5),
        ("2 i 1/4 litra wody", 2.25),
        ("1 oraz 0.5 łyżki oleju", 1.5),
    ],
    ids=[
        "and_conjunction_with_fraction",
        "and_conjunction_with_quarter_fraction",
        "oraz_conjunction_with_decimal",
    ],
)
def test_should_sum_first_two_amounts_when_separated_by_registered_conjunction(
    extractor,
    ingredient,
    expected,
):
    assert extractor.extract(ingredient) == expected


@pytest.mark.parametrize(
    "ingredient",
    [
        "jajko",
        "szczypta soli",
        "świeża bazylia",
    ],
    ids=[
        "single_ingredient_without_amount",
        "phrase_without_amount",
        "ingredient_name_without_amount",
    ],
)
def test_should_return_default_amount_when_ingredient_does_not_start_with_number(
    extractor,
    ingredient,
):
    assert extractor.extract(ingredient) == 1


def test_should_extract_only_first_amount_when_separator_is_not_registered_conjunction(
    extractor,
):
    assert extractor.extract("1 plus 1/2 szklanki mleka") == 1.0


@pytest.mark.parametrize(
    "ingredient",
    [
        "",
        " ",
        "\n\t",
    ],
    ids=[
        "empty_string",
        "spaces_only",
        "whitespace_only",
    ],
)
def test_should_raise_amount_extraction_error_when_ingredient_is_empty(
    extractor,
    ingredient,
):
    with pytest.raises(AmountExtractionError, match="Ingredient is empty"):
        extractor.extract(ingredient)


@pytest.mark.parametrize(
    "ingredient",
    [
        "1/0 szklanki mleka",
        "1.2.3 szklanki mąki",
        "1/2/3 łyżki oleju",
    ],
    ids=[
        "fraction_with_zero_denominator",
        "invalid_decimal",
        "invalid_fraction",
    ],
)
def test_should_raise_amount_extraction_error_when_amount_format_is_invalid(
    extractor,
    ingredient,
):
    with pytest.raises(
        AmountExtractionError,
        match=f"Could not extract amount from: {ingredient}",
    ) as exc_info:
        extractor.extract(ingredient)

    assert exc_info.value.__cause__ is not None