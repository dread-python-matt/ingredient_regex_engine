from pydantic import BaseModel


class ParsedIngredient(BaseModel):
    raw_input: str
    amount: float
    unit_size: str
    unit: str
    condition: str
    name: str
    extra: str
