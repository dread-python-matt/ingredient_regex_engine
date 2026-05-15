import logging

from regex_engine.domain.enums import Category
from regex_engine.domain.errors import CategorizingError
from regex_engine.domain.models.categorized_ingredient import CategorizedIngredient
from regex_engine.ports.categories_repository import CategoryRepository
from regex_engine.ports.categorizer import Categorizer
from regex_engine.ports.categorizer_service import CategorizerService
from regex_engine.ports.regex_registry import RegexRegistryReader

logger = logging.getLogger("categorizer_service")


class CategorizerServiceDefault(CategorizerService):
    def __init__(
        self,
        categorizer: Categorizer,
        repository: CategoryRepository,
    ) -> None:
        self._categorizer = categorizer
        self._categorized_ingredients:dict[str, CategorizedIngredient] = repository.load()
        self._repository = repository


    async def categorize(self,
                         ingredient_registry: RegexRegistryReader
                         ) -> dict[str,CategorizedIngredient]:
        ingredients = ingredient_registry.get_all()
        total = len(ingredients)

        logger.info("Categorizing %s ingredients ...", total)

        for i, ingredient in enumerate(ingredients):
            logger.info("Categorizing ingredient %s/%s", i, total)
            existing_ingredient = self._categorized_ingredients.get(ingredient.stem)
            if existing_ingredient and existing_ingredient.category != Category.UNKNOWN:
                logger.info("Already categorized. Continuing.")
                continue

            if not existing_ingredient:
                existing_ingredient = CategorizedIngredient.create(stem=ingredient.stem)

            try:
                category = await self._categorizer.categorize(ingredient.stem)
                existing_ingredient.category = category
                self._categorized_ingredients[ingredient.stem] = existing_ingredient

            except CategorizingError as e:
                logger.error(
                    "Ingredient categorizing failed.",
                    extra={
                        "ingredient": e.ingredient,
                        "failures": [
                            {
                                "attempt": f.attempt,
                                "error_type": type(f.cause).__name__,
                                "error": str(f.cause),
                            }
                            for f in e.failures
                        ],
                    },
                    exc_info=True,
                )
                continue

        logger.info("Categorizing %s ingredients completed.", total)

        return self._categorized_ingredients







    def save(self) -> None:
        self._repository.save(self._categorized_ingredients)
