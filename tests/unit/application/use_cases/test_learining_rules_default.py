from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from regex_engine.application.use_cases.learning_rules_default import LearningRulesDefaults


def make_record(name: str):
    return SimpleNamespace(name=name)


@pytest.fixture()
def regex_resolver():
    return Mock()


@pytest.fixture()
def and_conjunctions():
    registry = Mock()
    registry.match_best.return_value = None
    registry.swap_match.side_effect = lambda text, replacement: text.replace(
        " i ", f" {replacement} "
    )
    return registry


@pytest.fixture()
def learning_rules(regex_resolver, and_conjunctions):
    return LearningRulesDefaults(
        regex_resolver=regex_resolver,
        and_conjunctions=and_conjunctions,
    )


@pytest.mark.parametrize(
    "ingredient",
    [
        "mąka pszenna",
        "szklanka mleka",
        "2 jajka",
    ],
    ids=[
        "ingredient_name_only",
        "unit_and_ingredient_name",
        "amount_and_ingredient_name",
    ],
)
def test_should_not_filter_record_when_ingredient_does_not_contain_and_conjunction(
    learning_rules,
    and_conjunctions,
    ingredient,
):
    record = make_record(ingredient)
    and_conjunctions.match_best.return_value = None

    result = learning_rules.filter_records([record])

    assert result == [record]
    and_conjunctions.match_best.assert_called_once_with(ingredient)
    and_conjunctions.swap_match.assert_not_called()


@pytest.mark.parametrize(
    "ingredient",
    [
        "sól i pieprz",
        "mąka i cukier",
        "jajka i mleko",
    ],
    ids=[
        "two_ingredient_names",
        "two_names_without_amount",
        "two_names_with_plural",
    ],
)
def test_should_filter_record_when_and_conjunction_separates_ingredients(
    learning_rules,
    and_conjunctions,
    ingredient,
):
    record = make_record(ingredient)
    and_conjunctions.match_best.return_value = Mock()
    and_conjunctions.swap_match.side_effect = lambda text, replacement: text.replace(
        " i ", f" {replacement} "
    )

    result = learning_rules.filter_records([record])

    assert result == []


@pytest.mark.parametrize(
    "ingredient",
    [
        "1 i 1/2 szklanki mleka",
        "2 i 1/4 szklanki mąki",
        "3 i 3/4 łyżki oliwy",
    ],
    ids=[
        "one_and_half",
        "two_and_quarter",
        "three_and_three_quarters",
    ],
)
def test_should_not_filter_record_when_and_conjunction_is_between_mixed_fraction_amounts(
    learning_rules,
    and_conjunctions,
    ingredient,
):
    record = make_record(ingredient)
    and_conjunctions.match_best.return_value = Mock()
    and_conjunctions.swap_match.side_effect = lambda text, replacement: text.replace(
        " i ", f" {replacement} "
    )

    result = learning_rules.filter_records([record])

    assert result == [record]


@pytest.mark.parametrize(
    "ingredient",
    [
        "1 i 0.5 szklanki mleka",
        "2 i 0.25 szklanki mąki",
    ],
    ids=[
        "integer_and_decimal_half",
        "integer_and_decimal_quarter",
    ],
)
def test_should_not_filter_record_when_and_conjunction_is_between_mixed_decimal_amounts(
    learning_rules,
    and_conjunctions,
    ingredient,
):
    record = make_record(ingredient)
    and_conjunctions.match_best.return_value = Mock()
    and_conjunctions.swap_match.side_effect = lambda text, replacement: text.replace(
        " i ", f" {replacement} "
    )

    result = learning_rules.filter_records([record])

    assert result == [record]


def test_should_filter_only_records_with_non_numeric_and_conjunction(
    learning_rules,
    and_conjunctions,
):
    records = [
        make_record("sól i pieprz"),
        make_record("1 i 1/2 szklanki mleka"),
        make_record("mąka pszenna"),
    ]

    def match_best(text):
        return Mock() if " i " in text else None

    and_conjunctions.match_best.side_effect = match_best
    and_conjunctions.swap_match.side_effect = lambda text, replacement: text.replace(
        " i ", f" {replacement} "
    )

    result = learning_rules.filter_records(records)

    assert result == [
        records[1],
        records[2],
    ]


@pytest.mark.parametrize(
    ("ingredient", "swapped"),
    [
        ("sól i pieprz", "sól SWAP pieprz"),
        ("1 i 1/2 szklanki mleka", "1 SWAP 1/2 szklanki mleka"),
    ],
    ids=[
        "ingredient_conjunction",
        "numeric_conjunction",
    ],
)
def test_should_swap_and_conjunctions(
    learning_rules,
    and_conjunctions,
    ingredient,
    swapped,
):
    and_conjunctions.swap_match.return_value = swapped

    result = learning_rules._swap_conjunctions(ingredient)

    assert result == swapped
    and_conjunctions.swap_match.assert_called_once_with(ingredient, "SWAP")


@pytest.mark.parametrize(
    ("ingredient", "expected"),
    [
        ("sól SWAP pieprz", True),
        ("1 SWAP 1/2 szklanki mleka", True),
        ("szklanka mleka", False),
        ("SWAP", True),
    ],
    ids=[
        "swap_between_words",
        "swap_between_numbers",
        "without_swap",
        "only_swap",
    ],
)
def test_should_detect_swap_token(learning_rules, ingredient, expected):
    assert learning_rules._contains_swap(ingredient) is expected


@pytest.mark.parametrize(
    ("ingredient", "expected"),
    [
        ("1 SWAP 1/2 szklanki mleka", "szklanki mleka"),
        ("2 SWAP 1/4 szklanki mąki", "szklanki mąki"),
        ("sól SWAP pieprz", "sól SWAP pieprz"),
    ],
    ids=[
        "one_and_half",
        "two_and_quarter",
        "non_numeric_swap",
    ],
)
def test_should_remove_swap_only_when_it_is_between_numbers(
    learning_rules,
    ingredient,
    expected,
):
    assert learning_rules._remove_swap_between_numbers(ingredient) == expected


@pytest.mark.parametrize(
    ("ingredient", "can_be_standardized"),
    [
        ("2 szklanki mleka", True),
        ("sól i pieprz", False),
        ("nieznany składnik", False),
    ],
    ids=[
        "standardized_record",
        "compound_unstandardized_record",
        "unknown_record",
    ],
)
def test_should_reduce_records_by_removing_records_that_can_be_standardized(
    learning_rules,
    regex_resolver,
    ingredient,
    can_be_standardized,
):
    record = make_record(ingredient)
    regex_resolver.can_be_standardized.return_value = can_be_standardized

    result = learning_rules.reduce_records([record])

    expected = [] if can_be_standardized else [record]

    assert result == expected
    regex_resolver.can_be_standardized.assert_called_once_with(ingredient)


def test_should_reduce_multiple_records_by_keeping_only_unstandardized_records(
    learning_rules,
    regex_resolver,
):
    records = [
        make_record("2 szklanki mleka"),
        make_record("sól i pieprz"),
        make_record("nieznany składnik"),
    ]

    regex_resolver.can_be_standardized.side_effect = [
        True,
        False,
        False,
    ]

    result = learning_rules.reduce_records(records)

    assert result == [
        records[1],
        records[2],
    ]

    assert regex_resolver.can_be_standardized.call_args_list == [
        ((records[0].name,),),
        ((records[1].name,),),
        ((records[2].name,),),
    ]
