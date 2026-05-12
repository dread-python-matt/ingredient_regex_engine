from typing import Protocol

from regex_engine.domain.enums import Category


class Categorizer(Protocol):
    async def categorize(self, ingredient_name: str) -> Category: ...
