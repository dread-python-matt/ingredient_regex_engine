import json


import pytest


from regex_engine.adapters.db.regex.file_categorized_ingredient_regex_repository import \
    FileCategorizedIngredientRegexRepository
from regex_engine.domain.enums import RegexKind
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.domain.models.regex_registry_default import RegexRegistryDefault





@pytest.fixture
def repository(tmp_path):
    return FileCategorizedIngredientRegexRepository(tmp_path, {})


def normalize_json(items):
    return sorted(
        (item["stem"], tuple(sorted(item["variants"])))
        for item in items
    )

def normalize_entries(entries):
    return sorted(
        (entry.stem, tuple(sorted(entry.variants)))
        for entry in entries
    )


@pytest.mark.parametrize(
    "registry, expected",
    [
        pytest.param(
            RegexRegistryDefault(
                kind=RegexKind.UNIT,
                entries=[
                    RegexEntry("gram", ["g", "gram", "gramy"]),
                    RegexEntry("mililitr", ["ml", "mililitr", "mililitrów"]),
                    RegexEntry("łyżeczka", ["łyżeczka", "łyżeczek", "łyżeczki"])
                ]
            ),
            [
                {
                    "stem": "gram",
                    "variants": ["g", "gram", "gramy"],
                },
                {
                    "stem":"mililitr",
                    "variants":["ml", "mililitr", "mililitrów"]
                },
                {
                    "stem":"łyżeczka",
                    "variants":["łyżeczka", "łyżeczek", "łyżeczki"]

                },
            ]
        ),
        pytest.param(
            RegexRegistryDefault(
                kind=RegexKind.AND_CONJUNCTIONS,
                entries=[
                    RegexEntry("i", ["i"]),
                    RegexEntry("oraz", ["oraz"]),
                ]
            ),
            [
                {"stem": "i", "variants": ["i"]},
                {"stem": "oraz", "variants": ["oraz"]},
            ]
        ),
        pytest.param(
            RegexRegistryDefault(
                kind=RegexKind.OR_CONJUNCTIONS,
                entries=[
                    RegexEntry("lub", ["lub"]),
                    RegexEntry("albo", ["albo"]),
                    RegexEntry("bądź", ["bądź"]),
                ]
            ),
            [
                {"stem": "lub", "variants": ["lub"]},
                {"stem": "albo", "variants": ["albo"]},
                {"stem": "bądź", "variants": ["bądź"]},
            ]
        ),
        pytest.param(
            RegexRegistryDefault(
                kind=RegexKind.INGREDIENT_CONDITION,
                entries=[
                    RegexEntry("posiekany", ["posiekany", "posiekana", "posiekane"]),
                    RegexEntry("pokrojony", ["pokrojony", "pokrojona", "pokrojone"]),
                    RegexEntry("starty", ["starty", "starta", "starte"]),
                ]
            ),
            [
                {"stem": "posiekany", "variants": ["posiekany", "posiekana", "posiekane"]},
                {"stem": "pokrojony", "variants": ["pokrojony", "pokrojona", "pokrojone"]},
                {"stem": "starty", "variants": ["starty", "starta", "starte"]},
            ]
        ),
        pytest.param(
            RegexRegistryDefault(
                kind=RegexKind.UNIT_SIZE,
                entries=[
                    RegexEntry("mały", ["mały", "mała", "małe"]),
                    RegexEntry("średni", ["średni", "średnia", "średnie"]),
                    RegexEntry("duży", ["duży", "duża", "duże"]),
                ]
            ),
            [
                {"stem": "mały", "variants": ["mały", "mała", "małe"]},
                {"stem": "średni", "variants": ["średni", "średnia", "średnie"]},
                {"stem": "duży", "variants": ["duży", "duża", "duże"]},
            ]
        )

    ]
)
def test_save__happy_path(repository, registry, expected):
    # Arrange
    repository.save(registry)

    # Assert
    with repository._create_path(registry.kind).open(encoding="utf-8") as file:
        actual = json.load(file)

    assert normalize_json(actual) == normalize_json(expected)



@pytest.mark.parametrize(
    "registry, expected",
    [
        pytest.param(
            RegexRegistryDefault(
                kind=RegexKind.INGREDIENT_NAME,
                entries=[
                    RegexEntry("cukier", ["cukier", "cukru", "cukrem"]),
                    RegexEntry("mleko", ["mleko", "mleka", "mlekiem"]),
                    RegexEntry("masło", ["masło", "masła", "masłem"]),
                ]
            ),
            [
                {
                    "stem": "cukier",
                    "variants": ["cukier", "cukru", "cukrem"],
                },
                {
                    "stem": "mleko",
                    "variants": ["mleko", "mleka", "mlekiem"],
                },
                {
                    "stem": "masło",
                    "variants": ["masło", "masła", "masłem"],
                },
            ]

        )
    ]
)
def test_save_ingredient__happy_path(repository, registry, expected):
    # Act
    repository.save(registry)

    # Assert
    with repository._create_path(registry.kind).open(encoding="utf-8") as file:
        actual = json.load(file)["nieznane"]

    assert normalize_json(actual) == normalize_json(expected)




@pytest.mark.parametrize(
    "kind, payload, expected",
    [
        pytest.param(
            RegexKind.UNIT,
            [
                {
                    "stem": "gram",
                    "variants": ["g", "gram", "gramy"],
                },
                {
                    "stem": "mililitr",
                    "variants": ["ml", "mililitr", "mililitrów"],
                },
                {
                    "stem": "łyżeczka",
                    "variants": ["łyżeczka", "łyżeczek", "łyżeczki"],
                },
            ],
            [
                RegexEntry("gram", ["g", "gram", "gramy"]),
                RegexEntry("mililitr", ["ml", "mililitr", "mililitrów"]),
                RegexEntry("łyżeczka", ["łyżeczka", "łyżeczek", "łyżeczki"]),
            ],
        ),
        pytest.param(
            RegexKind.AND_CONJUNCTIONS,
            [
                {"stem": "i", "variants": ["i"]},
                {"stem": "oraz", "variants": ["oraz"]},
            ],
            [
                RegexEntry("i", ["i"]),
                RegexEntry("oraz", ["oraz"]),
            ],
        ),
        pytest.param(
            RegexKind.OR_CONJUNCTIONS,
            [
                {"stem": "lub", "variants": ["lub"]},
                {"stem": "albo", "variants": ["albo"]},
                {"stem": "bądź", "variants": ["bądź"]},
            ],
            [
                RegexEntry("lub", ["lub"]),
                RegexEntry("albo", ["albo"]),
                RegexEntry("bądź", ["bądź"]),
            ],
        ),
        pytest.param(
            RegexKind.INGREDIENT_CONDITION,
            [
                {"stem": "posiekany", "variants": ["posiekany", "posiekana", "posiekane"]},
                {"stem": "pokrojony", "variants": ["pokrojony", "pokrojona", "pokrojone"]},
                {"stem": "starty", "variants": ["starty", "starta", "starte"]},
            ],
            [
                RegexEntry("posiekany", ["posiekany", "posiekana", "posiekane"]),
                RegexEntry("pokrojony", ["pokrojony", "pokrojona", "pokrojone"]),
                RegexEntry("starty", ["starty", "starta", "starte"]),
            ],
        ),
        pytest.param(
            RegexKind.UNIT_SIZE,
            [
                {"stem": "mały", "variants": ["mały", "mała", "małe"]},
                {"stem": "średni", "variants": ["średni", "średnia", "średnie"]},
                {"stem": "duży", "variants": ["duży", "duża", "duże"]},
            ],
            [
                RegexEntry("mały", ["mały", "mała", "małe"]),
                RegexEntry("średni", ["średni", "średnia", "średnie"]),
                RegexEntry("duży", ["duży", "duża", "duże"]),
            ],
        ),
    ],
)
def test_load__happy_path(repository, kind, payload, expected):
    # Arrange
    path = repository._create_path(kind)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Act
    actual = repository.load(kind)

    # Assert
    assert normalize_entries(actual._entries) == normalize_entries(expected)



@pytest.mark.parametrize(
    "kind, payload, expected",
    [
        pytest.param(
            RegexKind.UNIT,
            [
                {
                    "stem": "gram",
                    "variants": ["g", "gram", "gramy"],
                },
                {
                    "stem": "mililitr",
                    "variants": ["ml", "mililitr", "mililitrów"],
                },
                {
                    "stem": "łyżeczka",
                    "variants": ["łyżeczka", "łyżeczek", "łyżeczki"],
                },
            ],
            [
                RegexEntry("gram", ["g", "gram", "gramy"]),
                RegexEntry("mililitr", ["ml", "mililitr", "mililitrów"]),
                RegexEntry("łyżeczka", ["łyżeczka", "łyżeczek", "łyżeczki"]),
            ],
            id="unit",
        ),
        pytest.param(
            RegexKind.AND_CONJUNCTIONS,
            [
                {"stem": "i", "variants": ["i"]},
                {"stem": "oraz", "variants": ["oraz"]},
            ],
            [
                RegexEntry("i", ["i"]),
                RegexEntry("oraz", ["oraz"]),
            ],
            id="and-conjunctions",
        ),
        pytest.param(
            RegexKind.OR_CONJUNCTIONS,
            [
                {"stem": "lub", "variants": ["lub"]},
                {"stem": "albo", "variants": ["albo"]},
                {"stem": "bądź", "variants": ["bądź"]},
            ],
            [
                RegexEntry("lub", ["lub"]),
                RegexEntry("albo", ["albo"]),
                RegexEntry("bądź", ["bądź"]),
            ],
            id="or-conjunctions",
        ),
        pytest.param(
            RegexKind.INGREDIENT_CONDITION,
            [
                {"stem": "posiekany", "variants": ["posiekany", "posiekana", "posiekane"]},
                {"stem": "pokrojony", "variants": ["pokrojony", "pokrojona", "pokrojone"]},
                {"stem": "starty", "variants": ["starty", "starta", "starte"]},
            ],
            [
                RegexEntry("posiekany", ["posiekany", "posiekana", "posiekane"]),
                RegexEntry("pokrojony", ["pokrojony", "pokrojona", "pokrojone"]),
                RegexEntry("starty", ["starty", "starta", "starte"]),
            ],
            id="ingredient-condition",
        ),
        pytest.param(
            RegexKind.UNIT_SIZE,
            [
                {"stem": "mały", "variants": ["mała", "małe", "mały"]},
                {"stem": "średni", "variants": ["średnia", "średnie", "średni"]},
                {"stem": "duży", "variants": ["duża", "duże", "duży"]},
            ],
            [
                RegexEntry("mały", ["mały", "mała", "małe"]),
                RegexEntry("średni", ["średni", "średnia", "średnie"]),
                RegexEntry("duży", ["duży", "duża", "duże"]),
            ],
            id="unit-size",
        ),
        pytest.param(
            RegexKind.INGREDIENT_NAME,
            {
                "nabiał": [
                    {"stem": "mleko", "variants": ["mleko", "mleka", "mlekiem"]},
                    {"stem": "masło", "variants": ["masło", "masła", "masłem"]},
                ],
                "mięso": [
                    {"stem": "kurczak", "variants": ["kurczak", "kurczaka", "kurczakiem"]},
                ],
                "warzywa": [
                    {"stem": "marchew", "variants": ["marchew", "marchwi", "marchwią"]},
                    {"stem": "cebula", "variants": ["cebula", "cebuli", "cebulą"]},
                ],
                "przyprawy i zioła": [
                    {"stem": "bazylia", "variants": ["bazylia", "bazylii"]},
                ],
                "nieznane": [
                    {"stem": "xanthan", "variants": ["xanthan"]},
                ],
            },
            [
                RegexEntry("mleko", ["mleko", "mleka", "mlekiem"]),
                RegexEntry("masło", ["masło", "masła", "masłem"]),
                RegexEntry("kurczak", ["kurczak", "kurczaka", "kurczakiem"]),
                RegexEntry("marchew", ["marchew", "marchwi", "marchwią"]),
                RegexEntry("cebula", ["cebula", "cebuli", "cebulą"]),
                RegexEntry("bazylia", ["bazylia", "bazylii"]),
                RegexEntry("xanthan", ["xanthan"]),
            ],
            id="ingredient-name-categorized",
        ),
    ],
)
def test_load_ingredients__happy_path(repository, kind, payload, expected):
    path = repository._create_path(kind)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    actual = repository.load(kind)

    assert actual.kind == kind
    assert normalize_entries(actual.get_all()) == normalize_entries(expected)









