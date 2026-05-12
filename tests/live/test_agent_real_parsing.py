import asyncio

import pytest

from regex_engine.adapters.parser.agent_ingredient_parser.agent_ingredient_parser import (
    AgentIngredientParser,
)
from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient


@pytest.fixture(scope="module")
def parser() -> AgentIngredientParser:
    return AgentIngredientParser()


TEST_CASES = [
    ParsedIngredient(
        raw_input="skórka starta z 1/2 cytryny (lub z jednej limonki)",
        amount=1 / 2,
        unit_size="",
        unit="",
        condition="starta",
        name="skórka z cytryny",
        extra="lub z jednej limonki",
    ),
    ParsedIngredient(
        raw_input="kawałeczek papryczki chili",
        amount=1,
        unit_size="",
        unit="kawałeczek",
        condition="",
        name="papryczki chili",
        extra="",
    ),
    ParsedIngredient(
        raw_input="150 ml ciepłej wody",
        amount=150,
        unit_size="",
        unit="ml",
        condition="ciepłej",
        name="wody",
        extra="",
    ),
    ParsedIngredient(
        raw_input="papryczka chili",
        amount=1,
        unit_size="",
        unit="",
        condition="",
        name="papryczka chili",
        extra="",
    ),
    ParsedIngredient(
        raw_input="2 łyżki posiekanego szczypiorku",
        amount=2,
        unit_size="",
        unit="łyżki",
        condition="posiekanego",
        name="szczypiorku",
        extra="",
    ),
    ParsedIngredient(
        raw_input="500 g kiszonej kapusty",
        amount=500,
        unit_size="",
        unit="g",
        condition="",
        name="kiszonej kapusty",
        extra="",
    ),
    ParsedIngredient(
        raw_input="4 łyżki słodkiego sosu chili",
        amount=4,
        unit_size="",
        unit="łyżki",
        condition="",
        name="słodkiego sosu chili",
        extra="",
    ),
    ParsedIngredient(
        raw_input="1 łyżeczka suszonego majeranku",
        amount=1,
        unit_size="",
        unit="łyżeczka",
        condition="",
        name="suszonego majeranku",
        extra="",
    ),
    ParsedIngredient(
        raw_input="1/3 szklanki gorzkiego kakao",
        amount=1 / 3,
        unit_size="",
        unit="szklanki",
        condition="",
        name="gorzkiego kakao",
        extra="",
    ),
    ParsedIngredient(
        raw_input="5 dużych garści świeżego szpinaku",
        amount=5,
        unit_size="dużych",
        unit="garści",
        condition="",
        name="świeżego szpinaku",
        extra="",
    ),
    ParsedIngredient(
        raw_input="100 g kaszy gryczanej (1 woreczek)",
        amount=100,
        unit_size="",
        unit="g",
        condition="",
        name="kaszy gryczanej",
        extra="1 woreczek",
    ),
]


@pytest.mark.asyncio
@pytest.mark.live_ai
async def test_real_agent_parsing():
    parser = AgentIngredientParser()

    result = await asyncio.wait_for(
        parser.parse("2 śmietanki kremówki"),
        timeout=30,
    )

    assert result.name == "śmietanki kremówki"
    assert result.amount == 2
    assert result.unit == ""
    assert result.unit_size == ""
    assert result.condition == ""


@pytest.mark.asyncio
@pytest.mark.live_ai
async def test_real_agent_parsing_2():
    parser = AgentIngredientParser()

    result = await asyncio.wait_for(
        parser.parse("2 jajka kurki zielononóżki"),
        timeout=30,
    )

    assert result.name == "jajka kurki zielononóżki"
    assert result.amount == 2
    assert result.unit == ""
    assert result.unit_size == ""
    assert result.condition == ""


@pytest.mark.asyncio
@pytest.mark.live_ai
@pytest.mark.parametrize("ingredient", TEST_CASES, ids=lambda ingredient: ingredient.raw_input)
async def test_real_agent_parsing_happy_path(ingredient, parser):

    result = await asyncio.wait_for(
        parser.parse(ingredient.raw_input),
        timeout=30,
    )

    assert result.name == ingredient.name
    assert result.amount == pytest.approx(ingredient.amount)
    assert result.unit == ingredient.unit
    assert result.unit_size == ingredient.unit_size
    assert result.condition == ingredient.condition
