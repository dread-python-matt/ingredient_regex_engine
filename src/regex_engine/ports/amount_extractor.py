from typing import Protocol


class AmountExtractor(Protocol):
    def extract(self, ingredient: str) -> float: ...
