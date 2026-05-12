from collections import Counter
from typing import Any

from regex_engine.domain.models.ingredient_record import IngredientRecord


class StringListInputAdapter:
    """
    Supports list[str] input.
    Normalizes values by stripping whitespace.
    Ignores empty strings.
    Aggregates duplicated ingredient names.
    """

    def supports(self, data: Any) -> bool:
        return isinstance(data, list) and all(isinstance(item, str) for item in data)

    def to_records(self, data: Any) -> list[IngredientRecord]:
        if not self.supports(data):
            raise TypeError(f"Unsupported data type: {type(data).__name__}")

        names = [
            item.strip()
            for item in data
            if item.strip()
        ]

        counter = Counter(names)

        return [
            IngredientRecord(name=name, count=count)
            for name, count in counter.items()
        ]