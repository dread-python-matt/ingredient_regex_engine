from typing import Protocol

from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient


class IngredientParser(Protocol):
    async def parse(self, ingredient: str) -> ParsedIngredient: ...
