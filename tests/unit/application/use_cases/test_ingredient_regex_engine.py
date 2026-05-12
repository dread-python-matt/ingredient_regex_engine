from dataclasses import dataclass
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, call

import pytest

from regex_engine.application.use_cases.ingredient_regex_engine import IngredientRegexEngineDefault
from regex_engine.domain.errors import AmountExtractionError, UnfeasibleStandardisation


@dataclass(frozen=True)
class FakeRegistryContainer:
    ingredient_registry: object
    unit_registry: object
    condition_registry: object


def make_record(name: str):
    return SimpleNamespace(name=name)


@pytest.fixture()
def filter_engine():
    engine = Mock()
    engine.learn = AsyncMock()
    return engine


@pytest.fixture()
def input_adapter():
    return Mock()


@pytest.fixture()
def regex_repository():
    return Mock()


@pytest.fixture()
def registries():
    return FakeRegistryContainer(
        ingredient_registry=Mock(name="ingredient_registry"),
        unit_registry=Mock(name="unit_registry"),
        condition_registry=Mock(name="condition_registry"),
    )


@pytest.fixture()
def categorizer_service():
    service = Mock()
    service.categorize = AsyncMock()
    return service


@pytest.fixture()
def resolver():
    return Mock()


@pytest.fixture()
def engine(
    filter_engine,
    input_adapter,
    regex_repository,
    registries,
    categorizer_service,
    resolver,
):
    return IngredientRegexEngineDefault(
        filter_engine=filter_engine,
        input_adapter=input_adapter,
        regex_repository=regex_repository,
        registries=registries,
        categorizer_service=categorizer_service,
        resolver=resolver,
    )


@pytest.mark.asyncio
async def test_should_learn_using_records_from_input_adapter(
    engine,
    input_adapter,
    filter_engine,
):
    data = object()
    records = [
        make_record("mleko"),
        make_record("mąka pszenna"),
        make_record("jajka"),
    ]

    input_adapter.to_records.return_value = records

    await engine.learn(data, max_iterations=10)

    input_adapter.to_records.assert_called_once_with(data)
    filter_engine.learn.assert_awaited_once_with(records, 3)


@pytest.mark.asyncio
async def test_should_respect_max_iterations_when_learning(
    engine,
    input_adapter,
    filter_engine,
):
    data = object()
    records = [
        make_record("mleko"),
        make_record("mąka pszenna"),
        make_record("jajka"),
    ]

    input_adapter.to_records.return_value = records

    await engine.learn(data, max_iterations=2)

    filter_engine.learn.assert_awaited_once_with(records, 2)


@pytest.mark.asyncio
async def test_should_call_learning_engine_with_zero_iterations_when_input_is_empty(
    engine,
    input_adapter,
    filter_engine,
):
    data = object()
    input_adapter.to_records.return_value = []

    await engine.learn(data, max_iterations=100)

    filter_engine.learn.assert_awaited_once_with([], 0)


def test_should_recognize_ingredients_using_resolver(
    engine,
    input_adapter,
    resolver,
):
    data = object()
    records = [
        make_record("2 szklanki mleka"),
        make_record("1 jajko"),
    ]

    resolved_milk = Mock(name="resolved_milk")
    resolved_egg = Mock(name="resolved_egg")

    input_adapter.to_records.return_value = records
    resolver.resolve_ingredient.side_effect = [
        resolved_milk,
        resolved_egg,
    ]

    result = engine.recognize_ingredients(data)

    assert result == [
        resolved_milk,
        resolved_egg,
    ]

    input_adapter.to_records.assert_called_once_with(data)

    assert resolver.resolve_ingredient.call_args_list == [
        call("2 szklanki mleka"),
        call("1 jajko"),
    ]


def test_should_skip_ingredient_when_standardisation_is_unfeasible(
    engine,
    input_adapter,
    resolver,
):
    data = object()
    records = [
        make_record("2 szklanki kamieni"),
        make_record("1 szklanka mleka"),
    ]

    resolved_milk = Mock(name="resolved_milk")

    input_adapter.to_records.return_value = records
    resolver.resolve_ingredient.side_effect = [
        UnfeasibleStandardisation("Ingredient could not be standardized"),
        resolved_milk,
    ]

    result = engine.recognize_ingredients(data)

    assert result == [resolved_milk]

    assert resolver.resolve_ingredient.call_args_list == [
        call("2 szklanki kamieni"),
        call("1 szklanka mleka"),
    ]


def test_should_skip_ingredient_when_amount_extraction_fails(
    engine,
    input_adapter,
    resolver,
):
    data = object()
    records = [
        make_record("1/0 szklanki mleka"),
        make_record("2 jajka"),
    ]

    resolved_eggs = Mock(name="resolved_eggs")

    input_adapter.to_records.return_value = records
    resolver.resolve_ingredient.side_effect = [
        AmountExtractionError("Could not extract amount"),
        resolved_eggs,
    ]

    result = engine.recognize_ingredients(data)

    assert result == [resolved_eggs]

    assert resolver.resolve_ingredient.call_args_list == [
        call("1/0 szklanki mleka"),
        call("2 jajka"),
    ]


def test_should_return_empty_list_when_all_ingredients_are_skipped(
    engine,
    input_adapter,
    resolver,
):
    data = object()
    records = [
        make_record("2 szklanki kamieni"),
        make_record("1/0 szklanki mleka"),
    ]

    input_adapter.to_records.return_value = records
    resolver.resolve_ingredient.side_effect = [
        UnfeasibleStandardisation("Ingredient could not be standardized"),
        AmountExtractionError("Could not extract amount"),
    ]

    result = engine.recognize_ingredients(data)

    assert result == []


@pytest.mark.asyncio
async def test_should_categorize_ingredient_registry(
    engine,
    registries,
    categorizer_service,
):
    expected_categories = {
        "mleko": Mock(name="dairy_category"),
        "mąka_pszenna": Mock(name="flour_category"),
    }

    categorizer_service.categorize.return_value = expected_categories

    result = await engine.categorize_registries()

    assert result == expected_categories
    categorizer_service.categorize.assert_awaited_once_with(registries.ingredient_registry)


def test_should_save_all_registries(
    engine,
    registries,
    regex_repository,
):
    engine.save_registries()

    assert regex_repository.save.call_args_list == [
        call(registries.ingredient_registry),
        call(registries.unit_registry),
        call(registries.condition_registry),
    ]


def test_should_return_registry_container(engine, registries):
    result = engine.get_registries()

    assert result is registries


def test_should_save_categories(engine, categorizer_service):
    engine.save_categories()

    categorizer_service.save.assert_called_once_with()
