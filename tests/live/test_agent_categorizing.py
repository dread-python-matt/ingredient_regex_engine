import asyncio

import pytest

from regex_engine.adapters.categorizer.agent_categorizer import AgentCategorizer
from regex_engine.domain.enums import Category


@pytest.fixture
def categorizer() -> AgentCategorizer:
    return AgentCategorizer()


params = [
    pytest.param("truskawki", Category.FRUITS),
    pytest.param("mąka pszenna typu drugiego", Category.GRAINS),
    pytest.param("mleko", Category.DAIRY),
    pytest.param("jogurt naturalny", Category.DAIRY),
    pytest.param("ser cheddar", Category.DAIRY),
    pytest.param("pierś z kurczaka", Category.MEAT),
    pytest.param("wołowina mielona", Category.MEAT),
    pytest.param("łosoś świeży", Category.FISH_AND_SEAFOOD),
    pytest.param("jajka kurze", Category.EGGS),
    pytest.param("ryż biały", Category.GRAINS),
    pytest.param("makaron pełnoziarnisty", Category.GRAINS),
    pytest.param("marchew", Category.VEGETABLES),
    pytest.param("brokuł", Category.VEGETABLES),
    pytest.param("jabłko", Category.FRUITS),
    pytest.param("banan", Category.FRUITS),
    pytest.param("soczewica", Category.LEGUMES),
    pytest.param("ciecierzyca", Category.LEGUMES),
    pytest.param("migdały", Category.NUTS_AND_SEEDS),
    pytest.param("nasiona chia", Category.NUTS_AND_SEEDS),
    pytest.param("oliwa z oliwek", Category.FATS_AND_OILS),
    pytest.param("masło", Category.FATS_AND_OILS),
    pytest.param("cukier biały", Category.SUGARS_AND_SWEETENERS),
    pytest.param("miód", Category.SUGARS_AND_SWEETENERS),
    pytest.param("sól", Category.SPICES_AND_HERBS),
    pytest.param("bazylia suszona", Category.SPICES_AND_HERBS),
    pytest.param("ketchup", Category.SAUCES_AND_DRESSINGS),
    pytest.param("majonez", Category.SAUCES_AND_DRESSINGS),
    pytest.param("pieczarki", Category.MUSHROOMS),
    pytest.param("chipsy ziemniaczane", Category.PROCESSED),
    pytest.param("konserwa mięsna", Category.PROCESSED),
    pytest.param("pizza mrożona", Category.PREPARED_MEALS),
    pytest.param("lasagne gotowe", Category.PREPARED_MEALS),
    pytest.param("rosół", Category.SOUPS),
    pytest.param("woda mineralna", Category.BEVERAGES),
    pytest.param("sok pomarańczowy", Category.BEVERAGES),
    pytest.param("piwo", Category.ALCOHOL),
    pytest.param("wino czerwone", Category.ALCOHOL),
    pytest.param("folia aluminiowa", Category.NON_FOOD),
    pytest.param("mix", Category.OTHER),
]


@pytest.mark.asyncio
@pytest.mark.live_ai
@pytest.mark.parametrize("ingredient, expected", params)
async def test_categorizer_happy_path(ingredient, expected, categorizer):
    actual = await asyncio.wait_for(categorizer.categorize(ingredient), timeout=30)

    assert actual == expected
