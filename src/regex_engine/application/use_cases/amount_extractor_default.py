import re
from fractions import Fraction

from regex_engine.domain.errors import AmountExtractionError
from regex_engine.ports.regex_registry import RegexRegistryReader


class AmountExtractorDefault:
    def __init__(self, and_conjunctions: RegexRegistryReader):
        self._and_conjunctions = and_conjunctions
        self._fraction_regex = re.compile(r"\d+/\d+|\d+\.\d+")

    def extract(self, ingredient: str) -> float:
        words = ingredient.split()
        if not words:
            raise AmountExtractionError("Ingredient is empty")

        try:
            if not self._is_digit(words[0]):
                return 1

            elif self._first_digits_are_separated_by_conjunction(words):
                first_number = Fraction(words[0])
                second_number = Fraction(words[2])
                return float(first_number + second_number)
            else:
                return float(Fraction(words[0]))

        except (ValueError, ZeroDivisionError, TypeError, AttributeError) as e:
            raise AmountExtractionError(f"Could not extract amount from: {ingredient}") from e

    def _first_digits_are_separated_by_conjunction(self, words: list[str]):
        length = len(words)
        if length < 3:
            return False

        if self._is_digit(words[0]) and self._is_conjunction(words[1]) and self._is_digit(words[2]):
            return True

        return False

    def _is_conjunction(self, word: str) -> bool:
        return bool(self._and_conjunctions.match_best(word))

    def _is_digit(self, word: str) -> bool:
        if word.isdigit() or self._is_fraction(word):
            return True
        return False

    def _is_fraction(self, number: str) -> bool:
        return bool(re.search(self._fraction_regex, number))
