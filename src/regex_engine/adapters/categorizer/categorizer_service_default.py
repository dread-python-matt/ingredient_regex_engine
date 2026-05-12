import logging

from regex_engine.domain.enums import Category
from regex_engine.domain.errors import CategorizingError
from regex_engine.ports.categories_repository import CategoryRepository
from regex_engine.ports.categorizer import Categorizer
from regex_engine.ports.categorizer_service import CategorizerService
from regex_engine.ports.regex_registry import RegexRegistryReader

logger = logging.getLogger("categorizer_service")


class CategorizerServiceDefault(CategorizerService):
    def __init__(
        self,
        categorizer: Categorizer,
        categorized_ingredients: dict[str, Category],
        repository: CategoryRepository,
    ) -> None:
        self._categorizer = categorizer
        self._categorized_ingredients = categorized_ingredients
        self._repository = repository

    async def categorize(self, ingredient_registry: RegexRegistryReader) -> dict[str, Category]:
        ingredients = ingredient_registry.get_all()
        total = len(ingredients)

        logger.info("Categorizing %s ingredients ...", total)

        for i, ingredient in enumerate(ingredients):
            logger.info("Categorizing ingredient %s/%s", i, total)
            existing_category = self._categorized_ingredients.get(ingredient.stem)
            if existing_category and existing_category != Category.UNKNOWN:
                logger.info("Already categorized. Continuing.")
                continue

            category = Category.UNKNOWN
            try:
                category = await self._categorizer.categorize(ingredient.stem)

            except CategorizingError as e:
                logger.error(
                    "Ingredient categorizing failedCategory set to UNKNOWN",
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

            finally:
                self._categorized_ingredients[ingredient.stem] = category

        logger.info("Categorizing %s ingredients completed.", total)

        return dict(self._categorized_ingredients)

    def save(self) -> None:
        self._repository.save(self._categorized_ingredients)
