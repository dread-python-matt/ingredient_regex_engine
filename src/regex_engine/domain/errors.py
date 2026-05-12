from dataclasses import dataclass

from regex_engine.domain.models.ingredient_record import IngredientRecord


class NameNotDetectedError(Exception):
    """Raised when a name cannot be detected."""

    def __init__(self, *, ingredient: str) -> None:
        self.ingredient = ingredient
        super().__init__("Name could not be detected")


class AmbiguousParsingError(Exception):
    """Raised when multiple equally frequent parsing results are found."""


class AmbiguousCategoryError(Exception):
    """Raised when multiple equally frequent parsing results are found."""


@dataclass(frozen=True, slots=True)
class AttemptFailure:
    attempt: int
    cause: Exception


class WordAnalysisParseError(ValueError):
    pass


class AttemptFailedError(Exception):
    action_verb = "process"

    def __init__(self, ingredient: str, errors: list[Exception]):
        self.ingredient = ingredient
        self.errors = errors
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        details = "; ".join(f"{type(error).__name__}: {error}" for error in self.errors)
        return f"All attempts to {self.action_verb} '{self.ingredient}' failed. Errors: {details}"


class DetailedIngredientError(Exception):
    action_verb = "process"

    def __init__(self, ingredient: str, failures: list[AttemptFailure]):
        self.ingredient = ingredient
        self.failures = failures
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        parts: list[str] = [f"Failed to {self.action_verb} ingredient '{self.ingredient}'"]
        for failure in self.failures:
            parts.append(
                f"attempt={failure.attempt} error={type(failure.cause).__name__}: {failure.cause}"
            )
        return " | ".join(parts)


class ParsingAttemptFailedError(AttemptFailedError):
    action_verb = "parsing"


class CategorizingAttemptFailedError(AttemptFailedError):
    action_verb = "categorizing"


class IngredientParsingError(DetailedIngredientError):
    action_verb = "parse"


class CategorizingError(DetailedIngredientError):
    action_verb = "categorize"


class ReducingRecordsError(Exception):
    def __init__(self, message: str, *, record: IngredientRecord | None = None):
        super().__init__(message)
        self.record = record


class RecordSelectionError(Exception):
    def __init__(
        self,
        message: str,
        *,
        records_count: int,
    ):
        super().__init__(message)
        self.records_count = records_count


class EveryRecordIterated(Exception):
    pass


class ConfigurationError(Exception):
    pass


class DemoModeError(RuntimeError):
    pass


class UnfeasibleStandardisation(Exception):
    pass


class AmountExtractionError(ValueError):
    pass


class InvalidModelError(Exception):
    pass


class EngineCreationError(Exception):
    pass
