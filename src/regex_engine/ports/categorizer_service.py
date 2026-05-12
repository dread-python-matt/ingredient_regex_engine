from typing import Protocol

from regex_engine.domain.enums import Category
from regex_engine.ports.regex_registry import RegexRegistryReader


class CategorizerService(Protocol):
    async def categorize(self, ingredient_registry: RegexRegistryReader) -> dict[str, Category]: ...
    def save(self) -> None: ...
