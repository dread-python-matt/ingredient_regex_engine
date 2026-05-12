from collections import Counter
from typing import Any

from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.domain.errors import AmbiguousParsingError, NameNotDetectedError


def get_most_occurred_value(values: list[Any]) -> Any:
    counter = Counter(values)
    most_common = counter.most_common()

    if not most_common:
        raise AmbiguousParsingError("No values to choose from")

    _, top_count = most_common[0]
    winners = [value for value, count in most_common if count == top_count]

    if len(winners) == 1:
        return winners[0]

    raise AmbiguousParsingError("Ambiguous parsing result")


def choose_proper_parsing(
    raw_input: str,
    ingredients: list[ParsedIngredient],
) -> ParsedIngredient:
    if not ingredients:
        raise AmbiguousParsingError("No parsed ingredients provided")

    amounts = []
    unit_sizes = []
    units = []
    conditions = []
    names = []
    extras = []

    for ingredient in ingredients:
        amounts.append(ingredient.amount)
        unit_sizes.append(ingredient.unit_size)
        units.append(ingredient.unit)
        conditions.append(ingredient.condition)
        names.append(ingredient.name)
        extras.append(ingredient.extra)

    raw_input = raw_input
    amount = get_most_occurred_value(amounts)
    unit_size = get_most_occurred_value(unit_sizes)
    unit = get_most_occurred_value(units)
    condition = get_most_occurred_value(conditions)
    name = get_most_occurred_value(names)
    extra = get_most_occurred_value(extras)

    if not name:
        raise NameNotDetectedError(ingredient=raw_input)

    return ParsedIngredient(
        raw_input=raw_input,
        amount=amount,
        unit_size=unit_size,
        unit=unit,
        condition=condition,
        name=name,
        extra=extra,
    )
