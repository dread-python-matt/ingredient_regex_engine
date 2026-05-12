import logging

from regex_engine.domain.errors import EveryRecordIterated, IngredientParsingError
from regex_engine.domain.models.ingredient_record import IngredientRecord
from regex_engine.ports.ingredient_parser import IngredientParser
from regex_engine.ports.learing_rules import LearningRules
from regex_engine.ports.regex_orchestrator import RegexOrchestrator

logger = logging.getLogger("regex_engine")


class IngredientLearningEngineDefault:
    def __init__(
        self,
        regex_orchestrator: RegexOrchestrator,
        parser: IngredientParser,
        learning_rules: LearningRules,
    ):
        self._regex_orchestrator = regex_orchestrator
        self._parser = parser
        self._learning_rules = learning_rules

    def _filter_records(self, records: list[IngredientRecord]) -> list[IngredientRecord]:
        logger.info("Filtering %s records", len(records))
        clean = self._learning_rules.filter_records(records)
        records_with_conj = len(records) - len(clean)
        logger.info("Found %s records with conjunction", records_with_conj)

        return clean

    def _reduce_records(self, records: list[IngredientRecord]) -> list[IngredientRecord]:
        logger.info("Reducing records ...")
        remaining_records = self._learning_rules.reduce_records(records)
        logger.info("Reduced %s records", len(records) - len(remaining_records))
        logger.info(f"Remaining {len(remaining_records)} records")
        return remaining_records

    def _select_next_record(
        self, records: list[IngredientRecord], processed: set[str]
    ) -> IngredientRecord:
        record = max(
            (r for r in records if r.name not in processed),
            key=lambda r: r.count,
            default=None,
        )
        if record is None:
            raise EveryRecordIterated("No non-iterated records available")

        processed.add(record.name)
        return record

    async def learn(self, ingredients: list[IngredientRecord], max_rounds: int = 10):
        records_left = self._filter_records(ingredients)
        conj_records_number = len(ingredients) - len(records_left)
        processed = set()

        success = 0
        failed = 0

        iterations = min(max_rounds, len(records_left))

        for i in range(iterations):
            try:
                logger.info("Iteration %s of %s ...", i + 1, iterations)

                records_left = self._reduce_records(records_left)

                ingredient = self._select_next_record(records_left, processed)

                parsed_ingredient = await self._parser.parse(ingredient.name)

                ensure_result = (
                    await self._regex_orchestrator.ensure_ingredient_included_in_registry(
                        parsed_ingredient
                    )
                )

                if ensure_result.failed:
                    logger.warning("Issues occurred in iteration %s/%s", i + 1, iterations)
                    logger.warning(ensure_result.iter_errors())
                    failed += 1

                else:
                    logger.info("Iteration %s/%s completed successfully", i + 1, iterations)
                    success += 1

            except EveryRecordIterated:
                break

            except IngredientParsingError as e:
                logger.error(
                    "Ingredient parsing failed",
                    extra={
                        "ingredient": e.ingredient,
                        "failures": [
                            {
                                "attempt": f.attempt,
                                "error_type": type(f.cause).__name__,
                                "error": str(f.cause),
                            }
                            for f in e.failures
                        ],
                    },
                    exc_info=True,
                )
                failed += 1
                continue

            except Exception as e:
                logger.exception("Error in iteration %s: %s", i + 1, e)
                failed += 1
                continue

        logger.info(
            f"Finished learning records {iterations}. "
            f"Success: {success}, "
            f"Failed: {failed}. "
            f"Already included: {iterations - (failed + success)}. "
            f"Omitted records with conjunction: {conj_records_number}."
        )
