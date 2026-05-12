from typing import Protocol

from regex_engine.domain.models.ingredient_record import IngredientRecord


class LearningRules(Protocol):
    def filter_records(self, records: list[IngredientRecord]) -> list[IngredientRecord]: ...
    def reduce_records(self, records: list[IngredientRecord]) -> list[IngredientRecord]: ...
