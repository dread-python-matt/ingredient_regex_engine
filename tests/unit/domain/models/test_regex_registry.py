import pytest

from regex_engine.domain.enums import RegexKind
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.domain.models.regex_registry_default import RegexRegistryDefault


def _entry(stem:str, variants: list[str]) -> RegexEntry:
    return RegexEntry(stem, variants)


class TestRegexRegistryInit:

    def test_init_happy_path(self):
        entries = [
            _entry("mleko", ["mleko"]),
            _entry("masło", ["masło"])
            ]

        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME,entries)

        assert r.get("mleko") is not None
        assert r.get("masło") is not None


    def test_init_duplicate_entries(self):
        entries = [
            _entry("mleko", ["mleko"]),
            _entry("mleko", ["masło"])
        ]
        with pytest.raises(ValueError):
            RegexRegistryDefault(RegexKind.INGREDIENT_NAME,entries)


class TestRegexRegistryAddEntry:

    @pytest.mark.parametrize(
         "entry",
        [
            _entry("mleko", ["mleko"]),
            _entry("masło", ["mleko"]),
            _entry("masło", []),
            _entry("ml", ["ml"]),

        ]
    )
    def test_add_entry_happy_path(self, entry):
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME,[])
        r.add_entry(entry)
        assert r.get(entry.stem) is not None


    @pytest.mark.parametrize(
         "entry",
        [
            _entry("mleko", [""]),
            _entry("mleko", ["mleko"]),
            _entry("mleko", ["mleko", "mleka"]),

        ]
    )
    def test_add_entry_duplicate(self, entry):
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME,[_entry("mleko", ["mleko"])])

        with pytest.raises(ValueError):
            r.add_entry(entry)


class TestRegexRegistryRemoveEntry:

    @pytest.mark.parametrize(
        "initial_stems, stem_to_remove",
        [
            (["mleko"], "mleko"),
            (["mleko", "maslo"], "maslo"),
            (["a", "b", "c"], "b"),
        ],
    )
    def test_remove_entry_happy_path(self, initial_stems, stem_to_remove):
        entries = [_entry(stem, [stem]) for stem in initial_stems]
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME,entries)

        r.remove_entry(stem_to_remove)

        assert r.get(stem_to_remove) is None
        assert stem_to_remove not in [e.stem for e in r.get_all()]


    @pytest.mark.parametrize(
        "initial_stems, stem_to_remove",
        [
            ([], "mleko"),
            (["mleko"], "maslo"),
            (["a", "b"], "c"),
        ],
    )
    def test_remove_entry_missing_raises(self, initial_stems, stem_to_remove):
        entries = [_entry(stem, [stem]) for stem in initial_stems]
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME, entries)

        with pytest.raises(KeyError):
            r.remove_entry(stem_to_remove)


class TestRegexRegistryAddVariant:

    @pytest.mark.parametrize(
        "initial_stem, initial_variants, new_variant",
        [
            ("mleko", ["mleko"], "mleka"),
            ("maslo", ["maslo"], "masła"),
            ("kakao", [], "kakaoo"),
        ],
    )
    def test_add_variant_happy_path(self, initial_stem, initial_variants, new_variant):
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME, [_entry(initial_stem, initial_variants)])

        r.add_variant(stem=initial_stem, variant=new_variant)

        entry = r.get(initial_stem)
        assert entry is not None
        assert new_variant.strip() in entry.variants
        assert entry.contains(new_variant.strip())


    @pytest.mark.parametrize(
        "stem",
        [
            "brak",
            "nieistnieje",
        ],

    )
    def test_add_variant_missing_stem_raises(self, stem):
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME, [_entry("mleko", ["mleko"])])

        with pytest.raises(KeyError):
            r.add_variant(stem=stem, variant="x")


class TestRegexRegistryRemoveVariant:

    @pytest.mark.parametrize(
        "initial_stem, initial_variants, variant_to_remove",
        [
            ("mleko", ["mleko", "mleka"], "mleka"),
            ("maslo", ["maslo", "masła"], "masła"),
        ],
    )
    def test_remove_variant_happy_path(self, initial_stem, initial_variants, variant_to_remove):
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME, [_entry(initial_stem, initial_variants)])

        r.remove_variant(stem=initial_stem, variant=variant_to_remove)

        entry = r.get(initial_stem)
        assert entry is not None
        assert variant_to_remove not in entry.variants


    @pytest.mark.parametrize(
        "stem",
        [
            "brak",
            "nieistnieje",
        ],
    )
    def test_remove_variant_missing_stem_raises(self, stem):
        r = RegexRegistryDefault(RegexKind.INGREDIENT_NAME, [_entry("mleko", ["mleko"])])

        with pytest.raises(KeyError):
            r.remove_variant(stem=stem, variant="x")

@pytest.fixture
def entries():
    milk = _entry("mleko", ["mleko", "mleka"])
    pudding = _entry("budyń", ["budyń", "budynie", "budyniu"])
    vanilla_pudding = _entry("budyń_waniliowy", ["budyń waniliowy", "budynie waniliowe", "budyniu waniliowego"])
    cocoa = _entry("kakao", ["kakao"])
    return {
        "milk": milk,
        "pudding": pudding,
        "vanilla_pudding": vanilla_pudding,
        "cocoa": cocoa,
    }

@pytest.fixture
def registry(entries):
    return RegexRegistryDefault(RegexKind.INGREDIENT_NAME, list(entries.values()))

class TestRegexRegistryMatchBest:
        @pytest.mark.parametrize(
            "text, expected_key",
            [
                ("2 mleka", "milk"),
                ("budyń waniliowy", "vanilla_pudding"),
                ("5 łyżek budyniu", "pudding"),
                ("5 łyżek budyniu wanilinowego", "pudding"),
                ("5 łyżek budyniu waniliowego", "vanilla_pudding"),
                ("5 łyżek kakao", "cocoa"),
            ],
        )
        def test_match_best_returns_value(self, registry, entries, text, expected_key):
            assert registry.match_best(text) == entries[expected_key]


        @pytest.mark.parametrize(
            "text",
            [
                "mleczny koktail",
                "kakaowy",
                "5 budyni",
                "masło"
            ]
        )
        def test_match_best_returns_none(self, registry, entries, text):
            assert registry.match_best(text) is None


class TestRegexRegistrySwapMatch:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("2 mleka", "2 SWAP"),
            ("budyń waniliowy", "SWAP"),
            ("5 łyżek budyniu", "5 łyżek SWAP"),
            ("5 łyżek budyniu wanilinowego", "5 łyżek SWAP wanilinowego"),
            ("5 łyżek budyniu waniliowego", "5 łyżek SWAP"),
            ("5 łyżek kakao", "5 łyżek SWAP"),
            ("karmel", "karmel"),
            ("5 lasek wanilii", "5 lasek wanilii"),
            ("5 łyżek budyniu wanilinowego i 2 łyżki budyniu waniliowego", "5 łyżek SWAP wanilinowego i 2 łyżki SWAP"),
            ("5 łyżek budyniu i 4 łyżki budyniu waniliowego", "5 łyżek SWAP i 4 łyżki SWAP"),
        ],
    )
    def test_match_best_returns_value(self, registry, entries, text, expected):
        assert registry.swap_match(text, "SWAP") == expected
