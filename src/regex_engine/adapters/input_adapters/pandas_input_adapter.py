from collections import Counter
from typing import Any

import pandas as pd

from regex_engine.domain.models.ingredient_record import IngredientRecord


class PandasInputAdapter:
    """
    Supports pandas DataFrame input.
    Expects a column with ingredient names.
    Optionally supports a count column.
    """

    def __init__(self, name_column: str = "ingredient", count_column: str | None = None) -> None:
        self._name_column = name_column
        self._count_column = count_column

    def supports(self, data: Any) -> bool:
        return isinstance(data, pd.DataFrame)

    def to_records(self, data: Any) -> list[IngredientRecord]:
        if not self.supports(data):
            raise TypeError(f"Unsupported data type: {type(data).__name__}")

        if self._name_column not in data.columns:
            raise ValueError(f"Missing column: {self._name_column}")

        if self._count_column and self._count_column in data.columns:
            return [
                IngredientRecord(
                    name=str(row[self._name_column]).strip(),
                    count=int(row[self._count_column]),
                )
                for _, row in data.iterrows()
                if pd.notna(row[self._name_column]) and str(row[self._name_column]).strip()
            ]

        names = [
            str(x).strip()
            for x in data[self._name_column].tolist()
            if pd.notna(x) and str(x).strip()
        ]

        counter = Counter(names)

        return [IngredientRecord(name=name, count=count) for name, count in counter.items()]
