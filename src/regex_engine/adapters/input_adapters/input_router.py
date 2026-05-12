from typing import Any

from regex_engine.domain.models.ingredient_record import IngredientRecord
from regex_engine.ports.input_adapter import InputAdapter


class InputRouter:
    def __init__(self, *adapters:InputAdapter):
        self._adapters = adapters

    def supports(self, data:Any) -> bool:
        for adapter in self._adapters:
            if adapter.supports(data):
                return True
        return False


    def to_records(self, data:Any) -> list[IngredientRecord]:
        for adapter in self._adapters:
            if adapter.supports(data):
                return adapter.to_records(data)

        raise TypeError(f"Unsupported data type: {type(data).__name__}")