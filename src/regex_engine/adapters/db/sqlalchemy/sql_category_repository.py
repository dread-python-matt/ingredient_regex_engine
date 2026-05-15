import logging

from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy.sql.expression import select

from regex_engine.adapters.db.sqlalchemy.mapping.mappers import (
    category_to_record,
    records_to_categorized_ingredients,
)
from regex_engine.adapters.db.sqlalchemy.models import CategorizedIngredientRecord, RegexEntryRecord
from regex_engine.domain.enums import RegexKind
from regex_engine.domain.models.categorized_ingredient import CategorizedIngredient
from regex_engine.ports.categories_repository import CategoryRepository

logger = logging.getLogger("__name__")


class SQLAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session_factory:sessionmaker[Session]):
        self._session_factory = session_factory


    def load(self) -> dict[str,CategorizedIngredient]:
        with (self._session_factory.begin() as session):
            categorized_ingredient_records = list(
                session.scalars(
                    select(CategorizedIngredientRecord)
                )
            )

            mapping_result = records_to_categorized_ingredients(categorized_ingredient_records)

            if mapping_result.has_issues:
                logger.warning(
                    "Skipped %d invalid records",
                    len(mapping_result.issues),
                )
                for issue in mapping_result.issues:
                    logger.warning(
                        "Invalid categorized ingredient record: %r",
                        issue.to_log_dict(),
                    )

            result = {
                ingredient.stem:ingredient
                for ingredient in mapping_result.items
            }

            return result

    def save(self, categorized_ingredients:dict[str,CategorizedIngredient]):
        ingredients_by_id = {
            ingredient.id:ingredient
            for ingredient in categorized_ingredients.values()
        }

        if len(ingredients_by_id) != len(categorized_ingredients):
            raise ValueError("CategorizedIngredients contains duplicated ids")


        with self._session_factory.begin() as session:
            existing_ingredients = list(
                session.scalars(
                    select(CategorizedIngredientRecord)
                )
            )

            existing_by_id = {
                ingredient.id:ingredient
                for ingredient in existing_ingredients
            }

            current_ids = set(ingredients_by_id)
            existing_ids = set(existing_by_id)

            new_ingredients_ids = current_ids - existing_ids

            for ingredient_id in new_ingredients_ids:
                session.add(
                    category_to_record(
                        ingredients_by_id[ingredient_id]
                    )
                )

            for ingredient_id in existing_ids & current_ids:
                existing = existing_by_id[ingredient_id]
                incoming = ingredients_by_id[ingredient_id]
                existing.stem = incoming.stem
                existing.category = incoming.category.value


            for ingredient_id in existing_ids - current_ids:
                session.delete(existing_by_id[ingredient_id])

            session.flush()



            self._attach_category_to_regex_entries(
                session=session,
                stems = {
                    ingredients_by_id[ingredient_id].stem
                    for ingredient_id in new_ingredients_ids
                }
            )



    def _attach_category_to_regex_entries(self,
                                          *,
                                          session: Session,
                                          stems:set[str],
                                          ) -> None:

        if not stems:
            return

        regex_entries = list(
            session.scalars(
                select(RegexEntryRecord)
                .where(RegexEntryRecord.regex_kind == RegexKind.INGREDIENT_NAME)
                .where(RegexEntryRecord.stem.in_(stems))
            )
        )

        categorized_ingredient_records = list(
            session.scalars(
                select(CategorizedIngredientRecord)
                .where(CategorizedIngredientRecord.stem.in_(stems))
            )
        )

        categorized_ingredients_by_stem = {
            ingredient.stem:ingredient
            for ingredient in categorized_ingredient_records
        }

        for entry in regex_entries:
            entry.categorized_ingredient = categorized_ingredients_by_stem[entry.stem]
