import pytest
from unittest.mock import AsyncMock

from regex_engine.domain.errors import (
    AmbiguousParsingError,
    IngredientParsingError,
    ParsingAttemptFailedError,
)
from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.adapters.parser.agent_ingredient_parser.agent_ingredient_parser import (
    AgentIngredientParser,
)


@pytest.fixture
def parser_client():
    client = AsyncMock()
    client.parse = AsyncMock()
    return client


def make_parsed_ingredient(
    raw_input: str,
    amount: int,
    unit: str = "g",
    name: str = "masła",
    unit_size: str = "",
    condition: str = "",
    extra: str = "",
) -> ParsedIngredient:
    return ParsedIngredient(
        raw_input=raw_input,
        amount=amount,
        unit_size=unit_size,
        unit=unit,
        condition=condition,
        name=name,
        extra=extra,
    )


class TestParseOnce:
    @pytest.mark.asyncio
    async def test_should_call_parser_client_parse_ensemble_size_times(self, parser_client):
        ingredient = "150 g masła, schłodzonego"
        parser = AgentIngredientParser(
            ensemble_size=3,
            max_retries=3,
            parser_client=parser_client,
        )

        parser_client.parse.side_effect = [
            make_parsed_ingredient(
                raw_input=ingredient,
                amount=150,
                condition="schłodzonego",
                name="masła",
            ),
            make_parsed_ingredient(
                raw_input=ingredient,
                amount=150,
                condition="schłodzonego",
                name="masła",
            ),
            make_parsed_ingredient(
                raw_input=ingredient,
                amount=200,
                condition="schłodzonego",
                name="masła",
            ),
        ]

        result = await parser._parse_once(ingredient)

        assert result == make_parsed_ingredient(
            raw_input=ingredient,
            amount=150,
            condition="schłodzonego",
            name="masła",
        )
        assert parser_client.parse.await_count == 3
        parser_client.parse.assert_any_await(ingredient, 0)
        parser_client.parse.assert_any_await(ingredient, 1)
        parser_client.parse.assert_any_await(ingredient, 2)

    @pytest.mark.asyncio
    async def test_should_raise_ambiguous_parsing_error_when_vote_is_ambiguous(self, parser_client):
        ingredient = "150 g masła"
        parser = AgentIngredientParser(
            ensemble_size=2,
            max_retries=3,
            parser_client=parser_client,
        )

        parser_client.parse.side_effect = [
            make_parsed_ingredient(raw_input=ingredient, amount=100),
            make_parsed_ingredient(raw_input=ingredient, amount=200),
        ]

        with pytest.raises(AmbiguousParsingError):
            await parser._parse_once(ingredient)

    @pytest.mark.asyncio
    async def test_should_ignore_failed_calls_and_choose_from_valid_results(self, parser_client):
        ingredient = "150 g masła"
        parser = AgentIngredientParser(
            ensemble_size=3,
            max_retries=3,
            parser_client=parser_client,
        )

        parser_client.parse.side_effect = [
            RuntimeError("temporary failure"),
            make_parsed_ingredient(raw_input=ingredient, amount=150),
            make_parsed_ingredient(raw_input=ingredient, amount=150),
        ]

        result = await parser._parse_once(ingredient)

        assert result == make_parsed_ingredient(raw_input=ingredient, amount=150)
        assert parser_client.parse.await_count == 3

    @pytest.mark.asyncio
    async def test_should_raise_parsing_attempt_failed_error_when_all_calls_fail(self, parser_client):
        ingredient = "150 g masła"
        parser = AgentIngredientParser(
            ensemble_size=3,
            max_retries=3,
            parser_client=parser_client,
        )

        parser_client.parse.side_effect = [
            TimeoutError("timeout"),
            RuntimeError("runner failed"),
            ValueError("invalid response"),
        ]

        with pytest.raises(ParsingAttemptFailedError):
            await parser._parse_once(ingredient)


class TestParse:
    @pytest.mark.asyncio
    async def test_should_return_parsed_ingredient_on_first_successful_attempt(
        self,
        parser_client,
        monkeypatch,
    ):
        ingredient = "150 g masła"
        parser = AgentIngredientParser(
            ensemble_size=3,
            max_retries=3,
            parser_client=parser_client,
        )

        expected = make_parsed_ingredient(raw_input=ingredient, amount=150)

        parse_once_mock = AsyncMock(return_value=expected)
        monkeypatch.setattr(parser, "_parse_once", parse_once_mock)

        result = await parser.parse(ingredient)

        assert result == expected
        parse_once_mock.assert_awaited_once_with(ingredient)

    @pytest.mark.asyncio
    async def test_should_retry_when_ambiguous_parsing_error_occurs_and_then_return_result(
        self,
        parser_client,
        monkeypatch,
    ):
        ingredient = "150 g masła"
        parser = AgentIngredientParser(
            ensemble_size=3,
            max_retries=3,
            parser_client=parser_client,
        )

        expected = make_parsed_ingredient(raw_input=ingredient, amount=150)

        parse_once_mock = AsyncMock(
            side_effect=[
                AmbiguousParsingError("Ambiguous parsing result"),
                expected,
            ]
        )
        monkeypatch.setattr(parser, "_parse_once", parse_once_mock)

        result = await parser.parse(ingredient)

        assert result == expected
        assert parse_once_mock.await_count == 2

    @pytest.mark.asyncio
    async def test_should_raise_ingredient_parsing_error_after_max_retries(
        self,
        parser_client,
        monkeypatch,
    ):
        ingredient = "150 g masła"
        parser = AgentIngredientParser(
            ensemble_size=3,
            max_retries=3,
            parser_client=parser_client,
        )

        parse_once_mock = AsyncMock(
            side_effect=AmbiguousParsingError("Ambiguous parsing result")
        )
        monkeypatch.setattr(parser, "_parse_once", parse_once_mock)

        with pytest.raises(
            IngredientParsingError,
        ):
            await parser.parse(ingredient)

        assert parse_once_mock.await_count == 3