import logging
from dataclasses import fields

from regex_engine.adapters.input_adapters.types import EngineInput
from regex_engine.domain.enums import Category
from regex_engine.domain.errors import AmountExtractionError, UnfeasibleStandardisation
from regex_engine.domain.models.registry_container import RegistryContainerReader
from regex_engine.domain.models.resolved_ingredient import ResolvedIngredient
from regex_engine.ports.categorizer_service import CategorizerService
from regex_engine.ports.input_adapter import InputAdapter
from regex_engine.ports.learning_engine import IngredientLearningEngine
from regex_engine.ports.regex_registry import RegexRegistryRepository
from regex_engine.ports.regex_resolver import RegexResolver

logger = logging.getLogger(__name__)


class IngredientRegexEngineDefault:
    def __init__(
        self,
        filter_engine: IngredientLearningEngine,
        input_adapter: InputAdapter,
        regex_repository: RegexRegistryRepository,
        registries: RegistryContainerReader,
        categorizer_service: CategorizerService,
        resolver: RegexResolver,
    ):
        self._filter_engine = filter_engine
        self._input_adapter = input_adapter
        self._regex_repository = regex_repository
        self._registries = registries
        self._category_service = categorizer_service
        self._resolver = resolver

    async def learn(self, data: EngineInput, max_iterations: int = 100):
        ingredients = self._input_adapter.to_records(data)

        max_iterations = min(max_iterations, len(ingredients))

        await self._filter_engine.learn(ingredients, max_iterations)

    def recognize_ingredients(self, data: EngineInput) -> list[ResolvedIngredient]:
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
        return await self._category_service.categorize(self._registries.ingredient_registry)

    def save_registries(self) -> None:
        for field in fields(self._registries):
            name = field.name
            registry = getattr(self._registries, name)
            self._regex_repository.save(registry)

    def get_registries(self) -> RegistryContainerReader:
        return self._registries

    def save_categories(self) -> None:
        self._category_service.save()
