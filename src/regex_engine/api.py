import logging

from regex_engine.bootstrap.bootstap_demo import create_demo_ingredient_regex_engine
from regex_engine.bootstrap.bootstrap import create_ingredient_regex_engine
from regex_engine.config import EngineConfig
from regex_engine.ports.ingredient_regex_engine import IngredientRegexEngine

from .application.dto.agent.parsed_ingredient import ParsedIngredient
from .domain.errors import ConfigurationError, EngineCreationError

logger = logging.getLogger(__name__)


async def create_engine(config: EngineConfig) -> IngredientRegexEngine:
    try:
        return await create_ingredient_regex_engine(config)
    except ConfigurationError as e:
        raise EngineCreationError("Failed to create engine") from e


def create_demo(mapping: dict[str, ParsedIngredient]) -> IngredientRegexEngine:
    return create_demo_ingredient_regex_engine(mapping)
