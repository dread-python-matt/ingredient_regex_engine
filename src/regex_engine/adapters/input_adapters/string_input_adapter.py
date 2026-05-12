from collections import Counter
from typing import Any

from regex_engine.domain.models.ingredient_record import IngredientRecord


class StringInputAdapter:
    """
    If input is string instance it separates the elements by a newline character.
    """

    def supports(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        return False

    def to_records(self, data: Any) -> list[IngredientRecord]:
        if not self.supports(data):
            raise TypeError(f"Unsupported data type: {type(data).__name__}")

        lines = [line.strip() for line in data.splitlines() if line.strip()]

        counter = Counter(lines)

        return [IngredientRecord(name=name, count=count) for name, count in counter.items()]
