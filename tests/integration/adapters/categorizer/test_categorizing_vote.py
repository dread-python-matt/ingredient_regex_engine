import pytest

from regex_engine.adapters.categorizer.categorizing_vote import choose_proper_category
from regex_engine.application.dto.agent.categorized_ingredient_agent import (
    CategorizedIngredientAgent,
)
from regex_engine.domain.enums import Category


def categorized_ingredient(category: Category) -> CategorizedIngredientAgent:
    return CategorizedIngredientAgent(
        category=category,
        name="test ingredient",
        description="test description",
        reason="test reason",
    )


def test_choose_proper_category__multiple_categories__returns_most_common_category():
    # Arrange
    ingredients = [
        categorized_ingredient(Category.DAIRY),
        categorized_ingredient(Category.MEAT),
        categorized_ingredient(Category.DAIRY),
    ]

    # Act
    result = choose_proper_category(ingredients)

    # Assert
    assert result == Category.DAIRY


def test_choose_proper_category__empty_list__raises_value_error():
    with pytest.raises(ValueError, match="No categorized ingredients provided"):
        choose_proper_category([])
