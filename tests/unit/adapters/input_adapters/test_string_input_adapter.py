import pytest
from regex_engine.adapters.input_adapters.string_input_adapter import StringInputAdapter

from regex_engine.domain.models.ingredient_record import IngredientRecord



def records_to_tuples(records: list[IngredientRecord]) -> list[tuple[str, int]]:
    return [(record.name, record.count) for record in records]


@pytest.fixture
def adapter() -> StringInputAdapter:
    return StringInputAdapter()


class TestStringInputAdapterSupports:
    def test_supports_string_input(self, adapter: StringInputAdapter) -> None:
        result = adapter.supports("sugar\nsalt")

        assert result is True

    @pytest.mark.parametrize(
        "data",
        [
            None,
            [],
            {},
            123,
            1.5,
            object(),
        ],
    )
    def test_does_not_support_non_string_input(
        self,
        adapter: StringInputAdapter,
        data: object,
    ) -> None:
        result = adapter.supports(data)

        assert result is False


class TestStringInputAdapterToRecords:
    @pytest.mark.parametrize(
        "data",
        [
            None,
            [],
            {},
            123,
        ],
    )
    def test_raises_type_error_for_unsupported_input(
        self,
        adapter: StringInputAdapter,
        data: object,
    ) -> None:
        with pytest.raises(TypeError, match="Unsupported data type"):
            adapter.to_records(data)

    def test_converts_single_line_to_record(self, adapter: StringInputAdapter) -> None:
        result = adapter.to_records("sugar")

        assert records_to_tuples(result) == [
            ("sugar", 1),
        ]

    def test_splits_input_by_new_lines(self, adapter: StringInputAdapter) -> None:
        data = "sugar\nsalt\nflour"

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 1),
            ("salt", 1),
            ("flour", 1),
        ]

    def test_strips_whitespace_from_lines(self, adapter: StringInputAdapter) -> None:
        data = " sugar \n\t salt\t\n flour "

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 1),
            ("salt", 1),
            ("flour", 1),
        ]

    def test_ignores_empty_lines(self, adapter: StringInputAdapter) -> None:
        data = "\n\nsugar\n\n   \nsalt\n"

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 1),
            ("salt", 1),
        ]

    def test_aggregates_duplicate_lines(self, adapter: StringInputAdapter) -> None:
        data = "sugar\nsalt\nsugar\nflour\nsalt\nsugar"

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 3),
            ("salt", 2),
            ("flour", 1),
        ]

    def test_returns_empty_list_for_empty_string(self, adapter: StringInputAdapter) -> None:
        result = adapter.to_records("")

        assert result == []

    def test_returns_empty_list_for_whitespace_only_string(
        self,
        adapter: StringInputAdapter,
    ) -> None:
        result = adapter.to_records("   \n\t\n")

        assert result == []

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            ("sugar", [("sugar", 1)]),
            ("sugar\nsugar", [("sugar", 2)]),
            (" sugar \n\nsalt", [("sugar", 1), ("salt", 1)]),
            ("", []),
            ("   ", []),
        ],
    )
    def test_to_records_parametrized_cases(
        self,
        adapter: StringInputAdapter,
        data: str,
        expected: list[tuple[str, int]],
    ) -> None:
        result = adapter.to_records(data)

        assert records_to_tuples(result) == expected