import asyncio
import logging

from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.domain.enums import RegexKind
from regex_engine.domain.errors import ConfigurationError, NameNotDetectedError
from regex_engine.domain.models.orchestrator import EnsureIngredientResult, EnsureWordResult
from regex_engine.ports.regex_service import RegexService

logger = logging.getLogger("regex_orchestrator")


def _build_ensure_output(
    ensure_results: list[EnsureWordResult], raw_input: str
) -> EnsureIngredientResult:
    failed = False
    by_kind = {}
    for result in ensure_results:
        if result.exception:
            failed = True
        by_kind[result.kind] = result

    name = by_kind[RegexKind.INGREDIENT_NAME]

    return EnsureIngredientResult(failed=failed, raw_input=raw_input, name=name, items=by_kind)


def _log_ensure_items(items: list[EnsureWordResult], *, context: str) -> None:
    for item in items:
        status, stem = item.status, item.stem

        logger.info("[%s] %s=%s -> %s (stem: %s)", context, item.kind, item.word, status.name, stem)


def _build_ensure_plan(ingredient: ParsedIngredient) -> dict[RegexKind, str]:
    if not ingredient.name:
        raise NameNotDetectedError(ingredient=ingredient.raw_input)

    plan = {}
    for field, kind in FIELD_TO_KIND:
        value = getattr(ingredient, field)
        if value:
            plan[kind] = value

    return plan


FIELD_TO_KIND = (
    ("unit_size", RegexKind.UNIT_SIZE),
    ("unit", RegexKind.UNIT),
    ("condition", RegexKind.INGREDIENT_CONDITION),
    ("name", RegexKind.INGREDIENT_NAME),
)


class RegexOrchestratorDefault:
    REQUIRED_KINDS = {
        RegexKind.INGREDIENT_NAME,
        RegexKind.UNIT,
        RegexKind.UNIT_SIZE,
        RegexKind.INGREDIENT_CONDITION,
    }

    def __init__(
        self,
        services_by_kind: dict[RegexKind, RegexService],
    ):
        missing = self.REQUIRED_KINDS - services_by_kind.keys()
        if missing:
            raise ConfigurationError(f"Missing services: {missing}")

        self._services: dict[RegexKind, RegexService] = dict(services_by_kind)

    async def ensure_ingredient_included_in_registry(
        self, ingredient: ParsedIngredient
    ) -> EnsureIngredientResult:
        plan = _build_ensure_plan(ingredient)

        results = await asyncio.gather(
            *(
                self._services[kind].ensure_word_included_in_registry(value)
                for kind, value in plan.items()
            ),
        )

        _log_ensure_items(results, context=ingredient.raw_input)

        return _build_ensure_output(results, ingredient.raw_input)

    async def _ensure_word_included_in_registry(
        self, kind: RegexKind, value: str
    ) -> EnsureWordResult:
        return await self._services[kind].ensure_word_included_in_registry(value)
