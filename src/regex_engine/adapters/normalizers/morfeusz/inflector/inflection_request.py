from dataclasses import dataclass

from regex_engine.domain.models.grammar import GrammaticalCase, GrammaticalGender, GrammaticalNumber


@dataclass(frozen=True, slots=True)
class InflectionRequest:
    number: GrammaticalNumber
    case: GrammaticalCase
    gender: GrammaticalGender | None = None

    def __post_init__(self):
        if isinstance(self.number, (set, frozenset)):
            if len(self.number) == 1:
                object.__setattr__(self, "number", next(iter(self.number)))
            elif len(self.number) == 0:
                raise ValueError(f"No number found for {self.number}")
            else:
                raise ValueError(f"Ambiguous numbers: {self.number}")

        if isinstance(self.case, (set, frozenset)):
            if len(self.case) == 1:
                object.__setattr__(self, "case", next(iter(self.case)))
            elif len(self.case) == 0:
                raise ValueError(f"No case found for {self.case}")
            else:
                raise ValueError(f"Ambiguous cases: {self.case}")

        if isinstance(self.gender, (set, frozenset)):
            if len(self.gender) == 1:
                object.__setattr__(self, "gender", next(iter(self.gender)))
            elif len(self.gender) == 0:
                object.__setattr__(self, "gender", None)
            else:
                raise ValueError(f"Ambiguous gender: {self.gender}")

        elif self.gender is not None and not isinstance(self.gender, GrammaticalGender):
            raise TypeError(f"Invalid gender type: {type(self.gender)}")
