from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True, slots=True)
class ResolvedIngredient:
    raw_input: str
    amount: float = -1
    unit_size: Optional[str] = None
    unit: Optional[str] = None
    condition: Optional[str] = None
    name: Optional[str] = None
    extra: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ResolvedIngredient":
        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping")

        if "raw_input" not in data:
            raise ValueError("Missing required field: raw_input")

        return cls(
            raw_input=data["raw_input"],
            amount=data.get("amount", -1),
            unit_size=data.get("unit_size"),
            unit=data.get("unit"),
            condition=data.get("condition"),
            name=data.get("name"),
            extra=data.get("extra", ""),
        )

    def __str__(self):
        extra = f"Extra: {self.extra}"

        return (
            f"Input: {self.raw_input}\n"
            f"Amount: {self.amount}\n"
            f"Unit size: {self.unit_size}\n"
            f"Unit: {self.unit}\n"
            f"Condition: {self.condition}\n"
            f"Name: {self.name}\n"
            f"{extra if self.extra else ''}\n"
        )
