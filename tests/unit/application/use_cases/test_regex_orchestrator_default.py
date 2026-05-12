from typing import Optional
from unittest.mock import create_autospec

import pytest

from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.application.use_cases.regex_orchestrator_default import RegexOrchestratorDefault
from regex_engine.domain.enums import RegexKind, EnsureWordStatus
from regex_engine.domain.models.orchestrator import EnsureIngredientResult, EnsureWordResult

from regex_engine.ports.regex_service import RegexService


@pytest.fixture
def services_by_kind():
    return {
        RegexKind.INGREDIENT_NAME: create_autospec(RegexService, instance=True),
        RegexKind.UNIT: create_autospec(RegexService, instance=True),
        RegexKind.UNIT_SIZE: create_autospec(RegexService, instance=True),
        RegexKind.INGREDIENT_CONDITION: create_autospec(RegexService, instance=True),
    }


@pytest.fixture
def orchestrator(services_by_kind):
    return RegexOrchestratorDefault(services_by_kind)


def _build_ensure_word_result(kind:RegexKind,
                              status:EnsureWordStatus,
                              stem:str="stem",
                              word:str="word",
                              exception:Optional[Exception] = None
                              ):
    return EnsureWordResult(kind, status, stem, word, exception)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ingredient, expected",
    [
        pytest.param(
            ParsedIngredient(
                raw_input="2 czubate łyżki cukru trzcinowego",
                amount=2.0,
                unit_size="czubate",
                unit="łyżki",
                condition="",
                name="cukru trzcinowego",
                extra=""
            ),
            EnsureIngredientResult(
                failed=False,
                raw_input="2 czubate łyżki cukru trzcinowego",
                name=_build_ensure_word_result(RegexKind.INGREDIENT_NAME, EnsureWordStatus.CREATED_NEW),
                items={
                    RegexKind.INGREDIENT_NAME: _build_ensure_word_result(RegexKind.INGREDIENT_NAME, EnsureWordStatus.CREATED_NEW),
                    RegexKind.UNIT: _build_ensure_word_result(RegexKind.UNIT, EnsureWordStatus.CREATED_NEW),
                    RegexKind.UNIT_SIZE: _build_ensure_word_result(RegexKind.UNIT_SIZE, EnsureWordStatus.CREATED_NEW),
                }
            ),
        ),
        pytest.param(
            ParsedIngredient(
                raw_input="2 czubate łyżki zmielonego cukru trzcinowego",
                amount=2.0,
                unit_size="czubate",
                unit="łyżki",
                condition="zmielonego",
                name="cukru trzcinowego",
                extra=""
            ),
            EnsureIngredientResult(
                failed=False,
                raw_input="2 czubate łyżki zmielonego cukru trzcinowego",
                name=_build_ensure_word_result(RegexKind.INGREDIENT_NAME, EnsureWordStatus.CREATED_NEW),
                items={
                    RegexKind.INGREDIENT_NAME: _build_ensure_word_result(RegexKind.INGREDIENT_NAME,
                                                                         EnsureWordStatus.CREATED_NEW),
                    RegexKind.INGREDIENT_CONDITION : _build_ensure_word_result(RegexKind.INGREDIENT_CONDITION, EnsureWordStatus.CREATED_NEW),
                    RegexKind.UNIT: _build_ensure_word_result(RegexKind.UNIT, EnsureWordStatus.CREATED_NEW),
                    RegexKind.UNIT_SIZE: _build_ensure_word_result(RegexKind.UNIT_SIZE, EnsureWordStatus.CREATED_NEW),
                }
            ),
        ),

    ]
)
async def test_ensure_ingredient_included_in_registry__happy_path(orchestrator, services_by_kind, ingredient, expected):
    # Arrange
    services_by_kind[RegexKind.INGREDIENT_NAME].ensure_word_included_in_registry.return_value = (
        _build_ensure_word_result(RegexKind.INGREDIENT_NAME, EnsureWordStatus.CREATED_NEW)
    )
    services_by_kind[RegexKind.INGREDIENT_CONDITION].ensure_word_included_in_registry.return_value = (
        _build_ensure_word_result(RegexKind.INGREDIENT_CONDITION, EnsureWordStatus.CREATED_NEW)
    )
    services_by_kind[RegexKind.UNIT].ensure_word_included_in_registry.return_value = (
        _build_ensure_word_result(RegexKind.UNIT, EnsureWordStatus.CREATED_NEW)
    )
    services_by_kind[RegexKind.UNIT_SIZE].ensure_word_included_in_registry.return_value = (
        _build_ensure_word_result(RegexKind.UNIT_SIZE, EnsureWordStatus.CREATED_NEW)
    )

    # Act
    actual = await orchestrator.ensure_ingredient_included_in_registry(ingredient)

    # Assert
    assert actual == expected
