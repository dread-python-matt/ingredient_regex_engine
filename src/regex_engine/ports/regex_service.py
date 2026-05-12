from typing import Protocol

from regex_engine.domain.models.orchestrator import EnsureWordResult


class RegexService(Protocol):
    async def ensure_word_included_in_registry(self, word: str) -> EnsureWordResult: ...
