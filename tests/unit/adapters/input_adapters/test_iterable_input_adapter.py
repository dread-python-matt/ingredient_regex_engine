import pytest
from regex_engine.adapters.input_adapters.string_iterable_input_adapter import StringListInputAdapter

from regex_engine.domain.models.ingredient_record import IngredientRecord



def records_to_tuples(records: list[IngredientRecord]) -> list[tuple[str, int]]:
    return [(record.name, record.count) for record in records]


@pytest.fixture
def adapter() -> StringListInputAdapter:
    return StringListInputAdapter()


class TestStringListInputAdapterSupports:
    def test_supports_list_of_strings(self, adapter: StringListInputAdapter) -> None:
        result = adapter.supports(["sugar", "salt"])

        assert result is True

    def test_supports_empty_list(self, adapter: StringListInputAdapter) -> None:
        result = adapter.supports([])

        assert result is True

    @pytest.mark.parametrize(
        "data",
        [
            None,
            "sugar",
            ("sugar", "salt"),
            {"ingredient": "sugar"},
            123,
            object(),
        ],
    )
    def test_does_not_support_non_list_inputs(
        self,
        adapter: StringListInputAdapter,
        data: object,
    ) -> None:
        result = adapter.supports(data)

        assert result is False

    @pytest.mark.parametrize(
        "data",
        [
            ["sugar", 123],
            ["sugar", None],
            ["sugar", {"name": "salt"}],
            [1, 2, 3],
        ],
    )
    def test_does_not_support_list_with_non_string_elements(
        self,
        adapter: StringListInputAdapter,
        data: list[object],
    ) -> None:
        result = adapter.supports(data)

        assert result is False


class TestStringListInputAdapterToRecords:
    @pytest.mark.parametrize(
        "data",
        [
            None,
            "sugar",
            ("sugar", "salt"),
            {"ingredient": "sugar"},
            123,
            ["sugar", 123],
            ["sugar", None],
        ],
    )
    def test_raises_type_error_for_unsupported_input(
        self,
        adapter: StringListInputAdapter,
        data: object,
    ) -> None:
        with pytest.raises(TypeError, match="Unsupported data type"):
            adapter.to_records(data)

    def test_returns_empty_list_for_empty_input(
        self,
        adapter: StringListInputAdapter,
    ) -> None:
        result = adapter.to_records([])

        assert result == []

    def test_converts_single_string_to_record(
        self,
        adapter: StringListInputAdapter,
    ) -> None:
        result = adapter.to_records(["sugar"])

        assert records_to_tuples(result) == [
            ("sugar", 1),
        ]

    def test_aggregates_duplicate_strings(
        self,
        adapter: StringListInputAdapter,
    ) -> None:
        data = ["sugar", "salt", "sugar", "flour", "salt", "sugar"]

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 3),
            ("salt", 2),
            ("flour", 1),
        ]

    def test_strips_whitespace_and_aggregates_normalized_values(
        self,
        adapter: StringListInputAdapter,
    ) -> None:
        data = [" sugar ", "sugar", "\tsugar\n", " salt "]

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 3),
            ("salt", 1),
        ]

    def test_ignores_empty_and_whitespace_only_strings(
        self,
        adapter: StringListInputAdapter,
    ) -> None:
        data = ["", "   ", "\t", "\n", "sugar"]

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 1),
        ]

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            ([], []),
            (["sugar"], [("sugar", 1)]),
            (["sugar", "sugar"], [("sugar", 2)]),
            ([" sugar ", "sugar"], [("sugar", 2)]),
            (["", "   ", "salt"], [("salt", 1)]),
            (["sugar", "salt", "sugar"], [("sugar", 2), ("salt", 1)]),
        ],
    )
    def test_to_records_parametrized_cases(
        self,
        adapter: StringListInputAdapter,
        data: list[str],
        expected: list[tuple[str, int]],
    ) -> None:
        result = adapter.to_records(data)

        assert records_to_tuples(result) == expected