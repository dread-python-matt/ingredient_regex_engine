import pandas as pd
import pytest

from regex_engine.adapters.input_adapters.pandas_input_adapter import PandasInputAdapter
from regex_engine.domain.models.ingredient_record import IngredientRecord


def records_to_tuples(records: list[IngredientRecord]) -> list[tuple[str, int]]:
    return [(record.name, record.count) for record in records]


@pytest.fixture
def adapter() -> PandasInputAdapter:
    return PandasInputAdapter()


@pytest.fixture
def ingredients_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ingredient": [
                "sugar",
                " salt ",
                "sugar",
                None,
                "",
                "   ",
            ]
        }
    )


class TestPandasInputAdapterSupports:
    def test_supports_pandas_dataframe(self, adapter: PandasInputAdapter) -> None:
        data = pd.DataFrame({"ingredient": ["sugar"]})

        result = adapter.supports(data)

        assert result is True

    @pytest.mark.parametrize(
        "data",
        [
            None,
            [],
            {},
            "ingredient",
            123,
        ],
    )
    def test_does_not_support_non_dataframe_inputs(
        self,
        adapter: PandasInputAdapter,
        data: object,
    ) -> None:
        result = adapter.supports(data)

        assert result is False


class TestPandasInputAdapterToRecords:
    @pytest.mark.parametrize(
        "data",
        [
            None,
            [],
            {},
            "ingredient",
        ],
    )
    def test_raises_type_error_for_unsupported_input(
        self,
        adapter: PandasInputAdapter,
        data: object,
    ) -> None:
        with pytest.raises(TypeError, match="Unsupported data type"):
            adapter.to_records(data)

    def test_raises_value_error_when_name_column_is_missing(
        self,
        adapter: PandasInputAdapter,
    ) -> None:
        data = pd.DataFrame({"name": ["sugar"]})

        with pytest.raises(ValueError, match="Missing column: ingredient"):
            adapter.to_records(data)

    def test_aggregates_ingredients_when_count_column_is_not_configured(
        self,
        adapter: PandasInputAdapter,
        ingredients_df: pd.DataFrame,
    ) -> None:
        result = adapter.to_records(ingredients_df)

        assert records_to_tuples(result) == [
            ("sugar", 2),
            ("salt", 1),
        ]

    def test_uses_custom_name_column(self) -> None:
        adapter = PandasInputAdapter(name_column="name")
        data = pd.DataFrame(
            {
                "name": [
                    "sugar",
                    "salt",
                    "sugar",
                ]
            }
        )

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 2),
            ("salt", 1),
        ]

    def test_uses_count_column_when_present(self) -> None:
        adapter = PandasInputAdapter(count_column="count")
        data = pd.DataFrame(
            {
                "ingredient": ["sugar", "salt", "flour"],
                "count": [3, 2, 5],
            }
        )

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 3),
            ("salt", 2),
            ("flour", 5),
        ]

    def test_does_not_aggregate_when_count_column_is_present(self) -> None:
        adapter = PandasInputAdapter(count_column="count")
        data = pd.DataFrame(
            {
                "ingredient": ["sugar", "sugar"],
                "count": [3, 2],
            }
        )

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 3),
            ("sugar", 2),
        ]

    @pytest.mark.parametrize(
        ("raw_count", "expected_count"),
        [
            ("3", 3),
            (3.0, 3),
            (3, 3),
        ],
    )
    def test_casts_count_column_to_int(
        self,
        raw_count: object,
        expected_count: int,
    ) -> None:
        adapter = PandasInputAdapter(count_column="count")
        data = pd.DataFrame(
            {
                "ingredient": ["sugar"],
                "count": [raw_count],
            }
        )

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [("sugar", expected_count)]

    def test_falls_back_to_aggregation_when_configured_count_column_is_missing(self) -> None:
        adapter = PandasInputAdapter(count_column="count")
        data = pd.DataFrame(
            {
                "ingredient": ["sugar", "salt", "sugar"],
            }
        )

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [
            ("sugar", 2),
            ("salt", 1),
        ]

    def test_skips_empty_names_without_count_column(self) -> None:
        adapter = PandasInputAdapter()
        data = pd.DataFrame(
            {
                "ingredient": [
                    None,
                    "",
                    "   ",
                    "sugar",
                ]
            }
        )

        result = adapter.to_records(data)

        assert records_to_tuples(result) == [("sugar", 1)]
