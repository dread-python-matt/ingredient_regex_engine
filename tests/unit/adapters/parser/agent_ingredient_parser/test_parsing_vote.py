import pytest

from regex_engine.adapters.parser.agent_ingredient_parser.parsing_vote import (
    choose_proper_parsing,
    get_most_occurred_value,
)
from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.domain.errors import AmbiguousParsingError, NameNotDetectedError


def make_parsed_ingredient(
    raw_input: str,
    amount: int | float,
    unit_size: str = "",
    unit: str = "",
    condition: str = "",
    name: str = "",
    extra: str = "",
) -> ParsedIngredient:
    return ParsedIngredient(
        raw_input=raw_input,
        amount=amount,
        unit_size=unit_size,
        unit=unit,
        condition=condition,
        name=name,
        extra=extra,
    )


class TestGetMostOccurredValue:
    def test_should_return_most_common_value_when_there_is_single_winner(self):
        values = ["g", "g", "ml"]

        result = get_most_occurred_value(values)

        assert result == "g"

    def test_should_return_empty_string_when_empty_string_is_most_common_value(self):
        values = ["", "", "g"]

        result = get_most_occurred_value(values)

        assert result == ""

    def test_should_raise_ambiguous_parsing_error_when_values_list_is_empty(self):
        with pytest.raises(AmbiguousParsingError, match="No values to choose from"):
            get_most_occurred_value([])

    def test_should_raise_ambiguous_parsing_error_when_there_is_a_tie(self):
        values = ["g", "ml"]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            get_most_occurred_value(values)

    def test_should_raise_ambiguous_parsing_error_when_multiple_values_have_same_top_count(self):
        values = ["g", "ml", "g", "ml"]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            get_most_occurred_value(values)


class TestChooseProperParsing:
    def test_should_return_parsed_ingredient_with_most_common_values(self):
        raw_input = "150 g masła, schłodzonego"
        ingredients = [
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=150,
                unit_size="",
                unit="g",
                condition="schłodzonego",
                name="masła",
                extra="",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=200,
                unit_size="",
                unit="g",
                condition="schłodzonego",
                name="masła",
                extra="",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=150,
                unit_size="małe",
                unit="g",
                condition="schłodzonego",
                name="masła",
                extra="",
            ),
        ]

        result = choose_proper_parsing(raw_input, ingredients)

        assert result == make_parsed_ingredient(
            raw_input=raw_input,
            amount=150,
            unit_size="",
            unit="g",
            condition="schłodzonego",
            name="masła",
            extra="",
        )

    def test_should_raise_ambiguous_parsing_error_when_ingredients_list_is_empty(self):
        with pytest.raises(AmbiguousParsingError, match="No parsed ingredients provided"):
            choose_proper_parsing("150 g masła, schłodzonego", [])

    def test_should_raise_ambiguous_parsing_error_when_amount_is_ambiguous(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="g", name="masła"),
            make_parsed_ingredient(raw_input=raw_input, amount=200, unit="g", name="masła"),
        ]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            choose_proper_parsing(raw_input, ingredients)

    def test_should_raise_ambiguous_parsing_error_when_unit_size_is_ambiguous(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=100,
                unit_size="małe",
                unit="g",
                name="masła",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=100,
                unit_size="duże",
                unit="g",
                name="masła",
            ),
        ]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            choose_proper_parsing(raw_input, ingredients)

    def test_should_raise_ambiguous_parsing_error_when_unit_is_ambiguous(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="g", name="masła"),
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="ml", name="masła"),
        ]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            choose_proper_parsing(raw_input, ingredients)

    def test_should_raise_ambiguous_parsing_error_when_condition_is_ambiguous(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=100,
                unit="g",
                condition="schłodzonego",
                name="masła",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=100,
                unit="g",
                condition="roztopionego",
                name="masła",
            ),
        ]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            choose_proper_parsing(raw_input, ingredients)

    def test_should_raise_ambiguous_parsing_error_when_name_is_ambiguous(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="g", name="masła"),
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="g", name="margaryny"),
        ]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            choose_proper_parsing(raw_input, ingredients)

    def test_should_raise_ambiguous_parsing_error_when_extra_is_ambiguous(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=100,
                unit="g",
                name="masła",
                extra="bio",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=100,
                unit="g",
                name="masła",
                extra="eko",
            ),
        ]

        with pytest.raises(AmbiguousParsingError, match="Ambiguous parsing result"):
            choose_proper_parsing(raw_input, ingredients)

    def test_should_allow_empty_strings_as_valid_majority_values_for_non_name_fields(self):
        raw_input = "1 pomarańcza"
        ingredients = [
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=1,
                unit_size="",
                unit="",
                condition="",
                name="pomarańcza",
                extra="",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=1,
                unit_size="",
                unit="",
                condition="",
                name="pomarańcza",
                extra="",
            ),
            make_parsed_ingredient(
                raw_input=raw_input,
                amount=1,
                unit_size="duża",
                unit="szt",
                condition="soczysta",
                name="pomarańcza",
                extra="bio",
            ),
        ]

        result = choose_proper_parsing(raw_input, ingredients)

        assert result == make_parsed_ingredient(
            raw_input=raw_input,
            amount=1,
            unit_size="",
            unit="",
            condition="",
            name="pomarańcza",
            extra="",
        )

    def test_should_raise_name_not_detected_error_when_name_is_empty(self):
        raw_input = "x"
        ingredients = [
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="g", name=""),
            make_parsed_ingredient(raw_input=raw_input, amount=100, unit="g", name=""),
        ]

        with pytest.raises(NameNotDetectedError):
            choose_proper_parsing(raw_input, ingredients)