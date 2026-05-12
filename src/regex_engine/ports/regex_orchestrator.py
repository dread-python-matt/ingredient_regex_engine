from typing import Protocol

from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.domain.models.orchestrator import EnsureIngredientResult


class RegexOrchestrator(Protocol):
    async def ensure_ingredient_included_in_registry(
        self, ingredient: ParsedIngredient
    ) -> EnsureIngredientResult: ...
