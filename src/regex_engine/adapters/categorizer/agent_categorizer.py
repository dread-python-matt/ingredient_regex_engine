import asyncio
import logging

from regex_engine.domain.enums import Category
from regex_engine.adapters.categorizer.categorizing_vote import choose_proper_category
from regex_engine.domain.errors import CategorizingAttemptFailedError, CategorizingError, \
    AttemptFailure, AmbiguousCategoryError
from regex_engine.application.dto.agent.categorized_ingredient import CategorizedIngredient
from regex_engine.adapters.categorizer.agent_categorizer_client import AgentCategorizerClient

logger = logging.getLogger("categorizer")

class AgentCategorizer:
    def __init__(
        self,
        categorizer_agent_client:AgentCategorizerClient,
        ensemble_size: int,
        max_retries: int,
    ):
        self.ensemble_size = ensemble_size
        self.max_retries = max_retries
        self.categorizer_client = categorizer_agent_client
        
    async def _categorize_once(self, ingredient:str):
        results = await asyncio.gather(
            *(
                self.categorizer_client.categorize(ingredient, instance)
                for instance in range(self.ensemble_size)
            ),
            return_exceptions=True,
        )

        valid_results: list[CategorizedIngredient] = []
        errors: list[Exception] = []

        for result in results:
            if isinstance(result, Exception):
                errors.append(result)
            else:
                valid_results.append(result)

        for error in errors:
            logger.warning("Agent parsing call failed for %s: %s", ingredient, error)

        if not valid_results:
            raise CategorizingAttemptFailedError(ingredient, errors)

        return choose_proper_category(valid_results)



    async def categorize(self, ingredient:str) -> Category:
        if not ingredient or not ingredient.strip():
            raise ValueError("Ingredient cannot be empty")

        logger.info("Categorizing ingredient %s ...", ingredient)
        failures: list[AttemptFailure] = []

        for attempt in range(1, self.max_retries + 1):
            try:
                parsed_ingredient = await self._categorize_once(ingredient)
                logger.info("Successfully categorized %s", ingredient)
                return parsed_ingredient

            except (AmbiguousCategoryError, CategorizingAttemptFailedError) as e:
                failures.append(AttemptFailure(attempt, e))
                logger.warning(
                    "Could not categorize %s. Attempt %s/%s. Retrying.",
                    ingredient,
                    attempt,
                    self.max_retries,
                )

        logger.error(
            "Could not categorize %s. Reached max retries %s. Aborting.",
            ingredient,
            self.max_retries,
        )
        raise CategorizingError(ingredient, failures)



