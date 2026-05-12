import re
from typing import Any

from regex_engine.domain.models.resolved_ingredient import ResolvedIngredient
from regex_engine.domain.enums import RegexKind
from regex_engine.domain.errors import UnfeasibleStandardisation
from regex_engine.ports.amount_extractor import AmountExtractor
from regex_engine.ports.regex_registry import RegexRegistryReader


def is_number(s:str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


class RegexResolverDefault:
    def __init__(
            self,
            amount_extractor:AmountExtractor,
            ingredient_names: RegexRegistryReader,
            ingredient_conditions: RegexRegistryReader,
            unit_sizes: RegexRegistryReader,
            units: RegexRegistryReader,
            or_conjunctions: RegexRegistryReader,
            and_conjunctions: RegexRegistryReader
    ):
        self.pipeline: list[tuple[RegexKind, RegexRegistryReader]] = [
            (RegexKind.INGREDIENT_NAME, ingredient_names),
            (RegexKind.INGREDIENT_CONDITION, ingredient_conditions),
            (RegexKind.UNIT_SIZE, unit_sizes),
            (RegexKind.UNIT, units),
            (RegexKind.OR_CONJUNCTIONS, or_conjunctions),
            (RegexKind.AND_CONJUNCTIONS, and_conjunctions),
        ]
        self._amount_extractor = amount_extractor
        self._extra_regex = re.compile(r"\(([^)]*)\)")
        self._regex_kind_token_regex = re.compile(
            "|".join(
                re.escape(k.name)
                for k in sorted(RegexKind, key=lambda x: len(x.name), reverse=True)
            )
        )
        self._trash_regex = re.compile(
            r"[,\.;:()\[\]{}\"'“”‘’\-–—/\\*+=|~^]"
        )


    def resolve_ingredient(self, ingredient:str) -> ResolvedIngredient:
        if not self.can_be_standardized(ingredient):
            raise UnfeasibleStandardisation(f"Ingredient {ingredient} could not be fully standardized")

        results:dict[str, Any] = {"raw_input": ingredient}

        extra = self._extract_extra(ingredient)

        results["extra"] = extra

        results["amount"] = self._amount_extractor.extract(ingredient)

        clean_ingredient = self._remove_extra(ingredient)

        for kind, registry in self.pipeline:
            match = registry.match_best(clean_ingredient)
            if match:
                results[registry.kind.value] = match.stem
                registry.swap_match(clean_ingredient, "")
        try:
            return ResolvedIngredient.from_dict(results)
        except (ValueError, TypeError, KeyError) as exc:
            raise UnfeasibleStandardisation(
                f"Failed to resolve ingredient: {ingredient!r}"
            ) from exc


    def standardize(self, ingredient: str) -> str:
        result = ingredient
        for kind, lookup in self.pipeline:
            result = lookup.swap_match(result, kind.name)
        return result

    def can_be_standardized(self, ingredient: str) -> bool:
        removed_extra = self._remove_extra(ingredient)
        standardized = self.standardize(removed_extra)
        remainders = self._regex_kind_token_regex.sub("", standardized).strip()
        clean = self._trash_regex.sub("", remainders).strip()

        parts = clean.split()

        if not parts:
            return True

        return all(is_number(part) for part in parts)


    def _extract_extra(self, text: str) -> str:
        match = self._extra_regex.search(text)
        return match.group(1) if match else ""

    def _contains_extra(self, text: str) -> bool:
        return bool(self._extract_extra(text))

    def _remove_extra(self, text: str) -> str:
        return self._extra_regex.sub("", text).strip()