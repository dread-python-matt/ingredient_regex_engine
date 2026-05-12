from typing import Counter

import pytest

from regex_engine.adapters.normalizers.morfeusz.inflector.inflector import Inflector
from regex_engine.adapters.normalizers.morfeusz.adjective_normalizer import MorfeuszAdjectiveNormalizer

pytest.importorskip("morfeusz2")

import morfeusz2

@pytest.fixture(scope="session")
def morfeusz():
    return morfeusz2.Morfeusz()

@pytest.fixture
def inflector(morfeusz):
    return Inflector(morfeusz)

@pytest.fixture
def morfeusz_adjective_normalizer(morfeusz, inflector):
    return MorfeuszAdjectiveNormalizer(inflector,morfeusz)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "adjective, expected",
    [
        ("kolorowy", "kolorowy"),
        ("duże", "duży"),
        ("większych", "większy"),
        ("malutki", "malutki"),
        ("mały", "mały"),
        ("największej", "największy"),
        ("niewyobrażalnych", "niewyobrażalny"),
    ]
)
async def test_stem_single_adjectives(adjective, expected, morfeusz_adjective_normalizer):
    result = await morfeusz_adjective_normalizer.stem(adjective)

    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "adjective, expected",
    [
        ("wędzonych", "wędzony"),
        ("surowe", "surowy"),
        ("gotowanych", "gotowany"),
        ("poszatkowanych", "poszatkowany"),
        ("pokrojonych", "pokrojony"),
        ("największej", "największy"),
        ("niewyobrażalnych", "niewyobrażalny"),
    ]
)
async def test_stem_adjectival_participles(adjective, expected, morfeusz_adjective_normalizer):
    result = await morfeusz_adjective_normalizer.stem(adjective)

    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "adjective, expected",
    [
        ("kolorowy", [
            "kolorowy", "kolorowa", "kolorowe",
            "kolorowego", "kolorowej",
            "kolorową",
            "kolorowym",
            "kolorowych",
            "kolorowymi"
        ]),
        ("czerwony", [
            "czerwony", "czerwona", "czerwone",
            "czerwonego", "czerwonej",
            "czerwoną",
            "czerwonym",
            "czerwonych",
            "czerwonymi"
        ]),
        ("duży", [
            "duży", "duża", "duże",
            "dużego", "dużej",
            "dużą",
            "dużym",
            "dużych",
            "dużymi"
        ]),
        ("największy", [
            "największy", "największa", "największe",
            "największego", "największej",
            "największą",
            "największym",
            "największych",
            "największymi"
        ]),
        ("najmniejszy", [
            "najmniejszy", "najmniejsza", "najmniejsze",
            "najmniejszego", "najmniejszej",
            "najmniejszą",
            "najmniejszym",
            "najmniejszych",
            "najmniejszymi"
        ]),
        ("większy", [
            "większy", "większa", "większe",
            "większego", "większej",
            "większą",
            "większym",
            "większych",
            "większymi"
        ])
    ]
)
async def test_inflect_happy_path(adjective, expected, morfeusz_adjective_normalizer):
    result = await morfeusz_adjective_normalizer.inflect(adjective)

    assert Counter(result) == Counter(expected)
