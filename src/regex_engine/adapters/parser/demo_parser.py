from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.domain.errors import DemoModeError


class DemoIngredientParser:
    def __init__(self, mapping: dict[str, ParsedIngredient]):
        self._mapping = mapping

    async def parse(self, ingredient: str) -> ParsedIngredient:
        parsed = self._mapping.get(ingredient)
        if parsed is None:
            raise DemoModeError(f"The ingredient {ingredient} is not available in demo version")

        return parsed
