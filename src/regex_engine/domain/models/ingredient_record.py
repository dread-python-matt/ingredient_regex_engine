from dataclasses import dataclass


@dataclass(slots=True)
class IngredientRecord:
    name: str
    count: int
