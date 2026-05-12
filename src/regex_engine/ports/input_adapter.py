from typing import Any, Protocol

from regex_engine.domain.models.ingredient_record import IngredientRecord


class InputAdapter(Protocol):
    def supports(self, data: Any) -> bool: ...
    def to_records(self, data: Any) -> list[IngredientRecord]: ...
