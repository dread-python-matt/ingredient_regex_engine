import re

from regex_engine.domain.models.ingredient_record import IngredientRecord
from regex_engine.ports.regex_registry import RegexRegistryReader
from regex_engine.ports.regex_resolver import RegexResolver


class LearningRulesDefaults:
    def __init__(self, regex_resolver: RegexResolver, and_conjunctions: RegexRegistryReader):
        self._swap = "SWAP"
        self._swap_regex = re.compile(rf"\b{self._swap}\b")
        self._swap_between_number_regex = re.compile(rf"\b\d+\s+{self._swap}\s+\d+(?:/\d+)?\.?\b")
        self._and_conjunctions = and_conjunctions
        self._regex_resolver = regex_resolver

    def filter_records(self, records: list[IngredientRecord]) -> list[IngredientRecord]:
        result = []
        for record in records:
            if not self._should_record_be_filtered(record):
                result.append(record)

        return result

    def reduce_records(self, records: list[IngredientRecord]) -> list[IngredientRecord]:
        result = []
        for record in records:
            if not self._regex_resolver.can_be_standardized(record.name):
                result.append(record)

        return result

    def _should_record_be_filtered(self, ingredient: IngredientRecord) -> bool:
        if not self._contains_and_conjunction(ingredient.name):
            return False

        swapped = self._swap_conjunctions(ingredient.name)
        clear = self._remove_swap_between_numbers(swapped)
        if self._contains_swap(clear):
            return True
        return False

    def _swap_conjunctions(self, ingredient: str) -> str:
        return self._and_conjunctions.swap_match(ingredient, self._swap)

    def _contains_swap(self, ingredient: str) -> bool:
        return bool(self._swap_regex.search(ingredient))

    def _contains_and_conjunction(self, ingredient: str) -> bool:
        if self._and_conjunctions.match_best(ingredient):
            return True
        return False

    def _remove_swap_between_numbers(self, ingredient: str) -> str:
        return self._swap_between_number_regex.sub("", ingredient).strip()
