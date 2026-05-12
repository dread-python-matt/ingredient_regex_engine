import json

import pytest

from regex_engine.adapters.db.category.file_category_repository import FileCategoryRepository
from regex_engine.domain.enums import Category


@pytest.fixture
def repository(tmp_path):
    full_path = tmp_path
    return FileCategoryRepository(full_path)




@pytest.mark.parametrize(
    "categorized_ingredients, expected_json",
    [
        pytest.param(
            {
                "jabłko":Category.FRUITS,
                "sezam":Category.NUTS_AND_SEEDS,
                "jajka":Category.EGGS,
                "maliny":Category.FRUITS,
                "kakao":Category.NUTS_AND_SEEDS,
            },
            {
                "owoce": ["jabłko", "maliny"],
                "orzechy i nasiona": ["sezam", "kakao"],
                "jajka": ["jajka"]
            },
            id="multiple_categories",
        ),
        pytest.param(
            {
                "jabłko":Category.FRUITS,
                "sezam":Category.NUTS_AND_SEEDS,
                "jajka":Category.EGGS,
            },
            {
                "owoce": ["jabłko"],
                "orzechy i nasiona": ["sezam"],
                "jajka": ["jajka"]
            },
            id="single_categories",
        ),
        pytest.param(
            {},
            {},
            id="empty",
        ),

    ]
)
def test_save__happy_path(repository, categorized_ingredients, expected_json):
    # Act
    repository.save(categorized_ingredients)

    # Assert
    with repository._path.open(encoding="utf-8") as f:
        actual = json.load(f)

    assert actual == expected_json



@pytest.mark.parametrize(
    "payload, expected",
    [
        pytest.param(
              {
                "owoce": ["jabłko", "maliny"],
                "orzechy i nasiona": ["sezam", "kakao"],
                "jajka": ["jajka"]
            },
            {
                "jabłko": Category.FRUITS,
                "sezam": Category.NUTS_AND_SEEDS,
                "jajka": Category.EGGS,
                "maliny": Category.FRUITS,
                "kakao": Category.NUTS_AND_SEEDS,
            },
            id="multiple_categories",
        ),
        pytest.param(
            {
                "owoce": ["jabłko"],
                "orzechy i nasiona": ["sezam"],
                "jajka": ["jajka"]
            },
            {
                "jabłko": Category.FRUITS,
                "sezam": Category.NUTS_AND_SEEDS,
                "jajka": Category.EGGS,
            },
            id="single_categories",
        ),
pytest.param(
              {
                "owoce": [1, "maliny"],
                "orzechy i nasiona": ["sezam", "kakao"],
                "jajka": [],
                "rośliny strączkowe": ["fasola"],

            },
            {
                "maliny": Category.FRUITS,
                "sezam": Category.NUTS_AND_SEEDS,
                "kakao": Category.NUTS_AND_SEEDS,
                "fasola": Category.LEGUMES,
            },
            id="some_invalid_elements",
        ),
pytest.param(
                {
                    "owoce": ["jabłko", "maliny"],
                    "orzechy i nasiona": ["sezam", "kakao"],
                    "jajca": ["jajka"],
                    "rośliny": ["fasola", "ciecierzyca"],
                    "zupy/buliony":["zupa pomidorowa"]
                },
            {
                "jabłko": Category.FRUITS,
                "maliny": Category.FRUITS,
                "sezam": Category.NUTS_AND_SEEDS,
                "kakao": Category.NUTS_AND_SEEDS,
                "zupa pomidorowa": Category.SOUPS,
            },
            id="some_invalid_categories",
        ),
    ]
)
def test_load__happy_path(repository, payload, expected):
    # Arrange
    repository._path.write_text(json.dumps(payload))

    # Act
    actual = repository.load()

    # Assert
    assert actual == expected


