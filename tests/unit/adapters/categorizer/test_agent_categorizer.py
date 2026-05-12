import pytest
from unittest.mock import Mock, AsyncMock

from regex_engine.adapters.categorizer.agent_categorizer import AgentCategorizer
from regex_engine.adapters.categorizer.agent_categorizer_client import AgentCategorizerClient
from regex_engine.domain.enums import Category
from regex_engine.domain.errors import CategorizingAttemptFailedError, CategorizingError


@pytest.fixture
def agent_client_mock():
    client = Mock(spec=AgentCategorizerClient)
    client.categorize = AsyncMock()
    return client


@pytest.fixture
def categorizer(agent_client_mock):
    return AgentCategorizer(agent_client_mock, 5, 3)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ingredient, expected",
    [
        pytest.param("masło", Category.DAIRY, id="dairy"),
        pytest.param("mleko", Category.DAIRY, id="milk"),
        pytest.param("ser cheddar", Category.DAIRY, id="cheese"),

        pytest.param("wołowina", Category.MEAT, id="meat"),
        pytest.param("kurczak", Category.MEAT, id="chicken"),

        pytest.param("łosoś", Category.FISH_AND_SEAFOOD, id="fish"),
        pytest.param("krewetki", Category.FISH_AND_SEAFOOD, id="seafood"),

        pytest.param("jajko", Category.EGGS, id="eggs"),

        pytest.param("mąka pszenna", Category.GRAINS, id="grains"),
        pytest.param("ryż", Category.GRAINS, id="rice"),

        pytest.param("marchew", Category.VEGETABLES, id="vegetable"),
        pytest.param("pomidor", Category.VEGETABLES, id="tomato"),

        pytest.param("wino czerwone", Category.ALCOHOL, id="alcohol"),

        pytest.param("papier do pieczenia", Category.NON_FOOD, id="non-food"),

        pytest.param("xyz nieznany składnik", Category.UNKNOWN, id="unknown"),
    ],
)
async def test_categorize__happy_path(categorizer, ingredient, expected, monkeypatch):
    # Arrange
    monkeypatch.setattr(
        categorizer,
        "_categorize_once",
        AsyncMock(return_value=expected)
    )

    # Act
    result = await categorizer.categorize(ingredient)

    # Assert
    assert result == expected


@pytest.mark.asyncio
async def test_categorize__empty_input__raise_value_error(categorizer):
    # Act / Assert

    with pytest.raises(ValueError):
        await categorizer.categorize("")

@pytest.mark.asyncio
async def test_categorize__ingredient_could_not_be_parsed__raise_categorizing_error(categorizer, monkeypatch):
    # Arrange
    ingredient = "pomidor"

    attempt_error = CategorizingAttemptFailedError(
        ingredient,
        [RuntimeError("agent could not parse ingredient")],
    )

    monkeypatch.setattr(
        categorizer,
        "_categorize_once",
        AsyncMock(side_effect=attempt_error)
    )

    # Act /Assert

    with pytest.raises(CategorizingError):
        await categorizer.categorize(ingredient)

