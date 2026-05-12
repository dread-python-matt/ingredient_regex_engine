import json
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from regex_engine.domain.enums import Category
from regex_engine.ports.categories_repository import CategoryRepository

logger = logging.getLogger(__name__)

VALID_WORD_RE = re.compile(r"^[\w\sąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+$")


def is_valid_word(value: str) -> bool:
    if not value or not value.strip():
        return False

    if not any(c.isalpha() for c in value):
        return False

    return bool(VALID_WORD_RE.fullmatch(value))


def _load(payload: dict[str, list]) -> dict[str, Category]:
    if not isinstance(payload, dict):
        raise TypeError("Expected payload to be a dict")

    result = {}

    for raw_category, ingredients in payload.items():
        try:
            category = Category(raw_category)
        except (ValueError, TypeError):
            logger.exception(f"Failed to parse category {raw_category}. Skipping.")
            continue

        if not isinstance(ingredients, Iterable) or isinstance(ingredients, (str, bytes)):
            logger.warning(f"Invalid ingredients for {raw_category}. Skipping.")
            continue

        for ingredient in ingredients:
            try:
                if not is_valid_word(ingredient):
                    raise TypeError(f"Invalid ingredient {ingredient}. Skipping.")
                result[ingredient] = category
            except (TypeError, AttributeError):
                logger.warning("Failed to parse ingredient %s in %s", ingredient, raw_category)
                continue
    return result


class FileCategoryRepository(CategoryRepository):
    def __init__(self, output_dir: Path):
        self._path = (output_dir / "categorized_ingredients").with_suffix(".json")

    def save(self, categorized_ingredients: dict[str, Category]) -> None:
        payload = defaultdict(list)

        for ingredient, category in categorized_ingredients.items():
            payload[category.value].append(ingredient)

        try:
            with self._path.open(mode="w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
        except OSError:
            logger.exception("Failed to save categorized ingredients to: %s", self._path)
            raise

        logger.info(
            "Saved categorized %s ingredients to: %s", len(categorized_ingredients), self._path
        )

    def load(self) -> dict[str, Category]:
        logger.info("Loading categories ...")

        if not self._path.exists():
            logger.info("No categories found at %s", self._path)
            return {}

        try:
            content = self._path.read_text(encoding="utf-8")
            if not content.strip():
                logger.info("No categories found at %s", self._path)
                return {}

            payload = json.loads(content)
        except json.JSONDecodeError as e:
            logger.exception("Invalid JSON in %s: %s. Returning empty categories", self._path, e)
            return {}
        except OSError as e:
            logger.exception("Failed to read %s: %s. Returning empty categories", self._path, e)
            return {}

        return _load(payload)
