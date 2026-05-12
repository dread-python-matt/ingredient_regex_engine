from typing import Protocol

from regex_engine.domain.models.ingredient_record import IngredientRecord
from regex_engine.domain.models.resolved_ingredient import ResolvedIngredient


class IngredientLearningEngine(Protocol):
    async def learn(
        self, ingredients: list[IngredientRecord], max_rounds: int
    ) -> list[ResolvedIngredient]: ...
