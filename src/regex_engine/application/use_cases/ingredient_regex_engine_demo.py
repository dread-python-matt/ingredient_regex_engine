import logging


from regex_engine.domain.models.resolved_ingredient import ResolvedIngredient
from regex_engine.adapters.input_adapters.types import EngineInput
from regex_engine.domain.enums import Category
from regex_engine.domain.errors import DemoModeError, UnfeasibleStandardisation, AmountExtractionError
from regex_engine.domain.models.registry_container import RegistryContainerReader

from regex_engine.ports.input_adapter import InputAdapter
from regex_engine.ports.learning_engine import IngredientLearningEngine
from regex_engine.ports.regex_resolver import RegexResolver

logger = logging.getLogger(__name__)

class IngredientRegexEngineDemo:
    def __init__(self,
                 filter_engine: IngredientLearningEngine,
                 input_adapter: InputAdapter,
                 registries: RegistryContainerReader,
                 resolver:RegexResolver,
                 ):
        self._filter_engine = filter_engine
        self._input_adapter = input_adapter
        self._registries = registries
        self._resolver = resolver

    async def learn(self, data:EngineInput, iterations:int = 10) -> list[ResolvedIngredient]:
        ingredients = self._input_adapter.to_records(data)

        iterations = min(iterations, len(ingredients))

        resolved_ingredients = await self._filter_engine.learn(ingredients, iterations)

        return resolved_ingredients

    def recognize_ingredients(self, data:EngineInput) -> list[ResolvedIngredient]:
        ingredients = self._input_adapter.to_records(data)

        results = []
        for ingredient in ingredients:
            try:
                results.append(self._resolver.resolve_ingredient(ingredient.name))
            except UnfeasibleStandardisation:
                logger.error(f"Unfeasible standardization: {ingredient}. Try to learn it first")
                continue
            except AmountExtractionError:
                logger.exception(
                    "Could not resolve amount from ingredient: %s. Skipping it",
                    ingredient,
                )
                continue

        return results

    async def categorize_registries(self) -> dict[str, Category]:
        raise DemoModeError("Categorizing registries is not available in demo mode")

    def save_registries(self) -> None:
        raise DemoModeError("Saving registries is not available in demo mode")

    def get_registries(self) -> RegistryContainerReader:
        return self._registries

    def save_categories(self) -> None:
        raise DemoModeError("Saving categories is not available in demo mode")