from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from regex_engine.application.use_cases.ingredient_learning_engine import IngredientLearningEngineDefault
from regex_engine.domain.errors import EveryRecordIterated, IngredientParsingError, AttemptFailure


def make_record(name: str, count: int = 1):
    return SimpleNamespace(name=name, count=count)


def make_ensure_result(*, failed: bool = False):
    return SimpleNamespace(
        failed=failed,
        iter_errors=Mock(return_value=["error"]),
    )


@pytest.fixture()
def regex_orchestrator():
    orchestrator = Mock()
    orchestrator.ensure_ingredient_included_in_registry = AsyncMock()
    return orchestrator


@pytest.fixture()
def parser():
    parser_mock = Mock()
    parser_mock.parse = AsyncMock()
    return parser_mock


@pytest.fixture()
def learning_rules():
    rules = Mock()
    rules.filter_records.side_effect = lambda records: records
    rules.reduce_records.side_effect = lambda records: records
    return rules


@pytest.fixture()
def engine(regex_orchestrator, parser, learning_rules):
    return IngredientLearningEngineDefault(
        regex_orchestrator=regex_orchestrator,
        parser=parser,
        learning_rules=learning_rules,
    )


def test_should_filter_records_using_learning_rules(engine, learning_rules):
    records = [
        make_record("sól i pieprz", count=10),
        make_record("2 szklanki mleka", count=5),
    ]
    filtered_records = [records[1]]

    learning_rules.filter_records.return_value = filtered_records
    learning_rules.filter_records.side_effect = None

    result = engine._filter_records(records)

    assert result == filtered_records
    learning_rules.filter_records.assert_called_once_with(records)


def test_should_reduce_records_using_learning_rules(engine, learning_rules):
    records = [
        make_record("2 szklanki mleka", count=10),
        make_record("nieznany składnik", count=5),
    ]
    reduced_records = [records[1]]

    learning_rules.reduce_records.return_value = reduced_records
    learning_rules.reduce_records.side_effect = None

    result = engine._reduce_records(records)

    assert result == reduced_records
    learning_rules.reduce_records.assert_called_once_with(records)


def test_should_select_record_with_highest_count(engine):
    records = [
        make_record("mleko", count=5),
        make_record("mąka pszenna", count=20),
        make_record("jajka", count=10),
    ]
    processed = set()

    result = engine._select_next_record(records, processed)

    assert result == records[1]
    assert processed == {"mąka pszenna"}


def test_should_skip_already_processed_records_when_selecting_next_record(engine):
    records = [
        make_record("mleko", count=50),
        make_record("mąka pszenna", count=20),
        make_record("jajka", count=10),
    ]
    processed = {"mleko"}

    result = engine._select_next_record(records, processed)

    assert result == records[1]
    assert processed == {"mleko", "mąka pszenna"}


def test_should_raise_every_record_iterated_when_all_records_are_processed(engine):
    records = [
        make_record("mleko", count=50),
        make_record("mąka pszenna", count=20),
    ]
    processed = {"mleko", "mąka pszenna"}

    with pytest.raises(EveryRecordIterated, match="No non-iterated records available"):
        engine._select_next_record(records, processed)


@pytest.mark.asyncio
async def test_should_process_selected_record_and_include_parsed_ingredient_when_learning_succeeds(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("mleko", count=5),
        make_record("mąka pszenna", count=20),
    ]
    parsed_ingredient = Mock()
    ensure_result = make_ensure_result(failed=False)

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = records
    learning_rules.reduce_records.side_effect = None

    parser.parse.return_value = parsed_ingredient
    regex_orchestrator.ensure_ingredient_included_in_registry.return_value = ensure_result

    await engine.learn(records, max_rounds=1)

    learning_rules.filter_records.assert_called_once_with(records)
    learning_rules.reduce_records.assert_called_once_with(records)

    parser.parse.assert_awaited_once_with("mąka pszenna")
    regex_orchestrator.ensure_ingredient_included_in_registry.assert_awaited_once_with(
        parsed_ingredient
    )

    ensure_result.iter_errors.assert_not_called()


@pytest.mark.asyncio
async def test_should_respect_max_rounds(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("mleko", count=30),
        make_record("mąka pszenna", count=20),
        make_record("jajka", count=10),
    ]

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = records
    learning_rules.reduce_records.side_effect = None

    parser.parse.return_value = Mock()
    regex_orchestrator.ensure_ingredient_included_in_registry.return_value = (
        make_ensure_result(failed=False)
    )

    await engine.learn(records, max_rounds=2)

    assert learning_rules.reduce_records.call_count == 2
    assert parser.parse.await_count == 2
    assert regex_orchestrator.ensure_ingredient_included_in_registry.await_count == 2

    parser.parse.assert_any_await("mleko")
    parser.parse.assert_any_await("mąka pszenna")


@pytest.mark.asyncio
async def test_should_not_process_any_record_when_all_records_are_filtered_out(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("sól i pieprz", count=10),
        make_record("mleko i jajka", count=5),
    ]

    learning_rules.filter_records.return_value = []
    learning_rules.filter_records.side_effect = None

    await engine.learn(records, max_rounds=10)

    learning_rules.filter_records.assert_called_once_with(records)
    learning_rules.reduce_records.assert_not_called()
    parser.parse.assert_not_awaited()
    regex_orchestrator.ensure_ingredient_included_in_registry.assert_not_awaited()


@pytest.mark.asyncio
async def test_should_stop_learning_when_no_record_left_after_reduction(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("2 szklanki mleka", count=10),
    ]

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = []
    learning_rules.reduce_records.side_effect = None

    await engine.learn(records, max_rounds=10)

    learning_rules.reduce_records.assert_called_once_with(records)
    parser.parse.assert_not_awaited()
    regex_orchestrator.ensure_ingredient_included_in_registry.assert_not_awaited()


@pytest.mark.asyncio
async def test_should_continue_learning_when_parser_raises_ingredient_parsing_error(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("mleko", count=30),
        make_record("mąka pszenna", count=20),
    ]

    parsing_error = IngredientParsingError(
        "mleko",
        [
            AttemptFailure(
                attempt=1,
                cause=ValueError("invalid ingredient"),
            )
        ],
    )

    parsed_ingredient = Mock()

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = records
    learning_rules.reduce_records.side_effect = None

    parser.parse.side_effect = [
        parsing_error,
        parsed_ingredient,
    ]
    regex_orchestrator.ensure_ingredient_included_in_registry.return_value = (
        make_ensure_result(failed=False)
    )

    await engine.learn(records, max_rounds=2)

    assert parser.parse.await_count == 2
    parser.parse.assert_any_await("mleko")
    parser.parse.assert_any_await("mąka pszenna")

    regex_orchestrator.ensure_ingredient_included_in_registry.assert_awaited_once_with(
        parsed_ingredient
    )


@pytest.mark.asyncio
async def test_should_continue_learning_when_orchestrator_raises_unexpected_exception(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("mleko", count=30),
        make_record("mąka pszenna", count=20),
    ]

    first_parsed_ingredient = Mock()
    second_parsed_ingredient = Mock()

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = records
    learning_rules.reduce_records.side_effect = None

    parser.parse.side_effect = [
        first_parsed_ingredient,
        second_parsed_ingredient,
    ]

    regex_orchestrator.ensure_ingredient_included_in_registry.side_effect = [
        RuntimeError("registry error"),
        make_ensure_result(failed=False),
    ]

    await engine.learn(records, max_rounds=2)

    assert parser.parse.await_count == 2
    assert regex_orchestrator.ensure_ingredient_included_in_registry.await_count == 2

    regex_orchestrator.ensure_ingredient_included_in_registry.assert_any_await(
        first_parsed_ingredient
    )
    regex_orchestrator.ensure_ingredient_included_in_registry.assert_any_await(
        second_parsed_ingredient
    )


@pytest.mark.asyncio
async def test_should_continue_learning_when_ensure_result_failed(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("mleko", count=10),
    ]
    parsed_ingredient = Mock()
    ensure_result = make_ensure_result(failed=True)

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = records
    learning_rules.reduce_records.side_effect = None

    parser.parse.return_value = parsed_ingredient
    regex_orchestrator.ensure_ingredient_included_in_registry.return_value = ensure_result

    await engine.learn(records, max_rounds=1)

    parser.parse.assert_awaited_once_with("mleko")
    regex_orchestrator.ensure_ingredient_included_in_registry.assert_awaited_once_with(
        parsed_ingredient
    )
    ensure_result.iter_errors.assert_called_once_with()


@pytest.mark.asyncio
async def test_should_process_records_by_descending_count_across_iterations(
    engine,
    learning_rules,
    parser,
    regex_orchestrator,
):
    records = [
        make_record("jajka", count=10),
        make_record("mleko", count=30),
        make_record("mąka pszenna", count=20),
    ]

    learning_rules.filter_records.return_value = records
    learning_rules.filter_records.side_effect = None
    learning_rules.reduce_records.return_value = records
    learning_rules.reduce_records.side_effect = None

    parser.parse.return_value = Mock()
    regex_orchestrator.ensure_ingredient_included_in_registry.return_value = (
        make_ensure_result(failed=False)
    )

    await engine.learn(records, max_rounds=3)

    assert parser.parse.await_args_list[0].args == ("mleko",)
    assert parser.parse.await_args_list[1].args == ("mąka pszenna",)
    assert parser.parse.await_args_list[2].args == ("jajka",)