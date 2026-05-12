import pytest

from regex_engine.domain.models.regex_entry import RegexEntry



class TestRegexEntryInit:

    @pytest.mark.parametrize(
        "stem, expected_stem , variants, expected_variants",
        [
            ("mleko", "mleko", ["mleko", "mleka"], {"mleko", "mleka"}),
            ("masło","masło", ["masło", "masła", "masła"], {"masło", "masła"}),
            ("kakao", "kakao", ["kakao"], {"kakao"}),
            ("sok pomarańczowy","sok_pomarańczowy", ["sok pomarańczowy"], {"sok pomarańczowy"}),
            ("sok  pomarańczowy", "sok_pomarańczowy", ["sok pomarańczowy"], {"sok pomarańczowy"}),
        ]

    )
    def test_happy_path(self, stem, expected_stem, variants, expected_variants):
        entry = RegexEntry(stem, variants)
        assert entry._stem == expected_stem
        assert entry._variants == expected_variants


    @pytest.mark.parametrize(
        "stem, variants",
        [
            ("", ["mleko"]),
            ("", [""]),
            ("    ", ["\n"]),
            ("\t", ["  "]),
        ]
    )
    def test_invalid_inputs(self, stem, variants):
        with pytest.raises(ValueError):
            RegexEntry(stem, variants)



class TestRegexEntryMatching:

    @pytest.mark.parametrize(
        "text",
        [
            "2 mleka w sklepie",
            "mleko",
            "masło i mleko",
            "Mleko",
            "2 Mleka i masła",
        ]
    )
    def test_contains_returns_true(self, text):
        entry = RegexEntry("mleko", ["mleko", "mleka"])
        assert entry.contains(text)

    @pytest.mark.parametrize(
        "text",
        [
            "2 mleczne batoniki w sklepie",
            "mlekowy",
            "masło i mlekoo",
            "mlek",
            "2mleka i masło",
            "mmlekoi",
        ]
    )
    def test_contains_returns_false(self, text):
        entry = RegexEntry("mleko", ["mleko", "mleka"])
        assert not entry.contains(text)

    @pytest.mark.parametrize(
        "text, entry, expected",
        [
            pytest.param(
                "5 szklanek płatków migdałowych",
                RegexEntry("płatki_migdałowe", ["płatki_migdałowe", "płatków migdałowych"]),
                True,
            ),
            pytest.param(
                "5 szklanek mąki typu 2",
                RegexEntry("mąka_typu_2", ["mąka typu 2", "mąki typu 2"]),
                True,
            ),
            pytest.param(
                "dwie łyżki mąki typu 2",
                RegexEntry("mąka_typu_2", ["mąka typu 2", "mąki typu 2"]),
                True,
            ),
            pytest.param(
                "pół kilograma mąki typu 2",
                RegexEntry("mąka_typu_2", ["mąka typu 2", "mąki typu 2"]),
                True,
            ),
            pytest.param(
                "3 sztuki jajek kurki zielononóżki",
                RegexEntry(
                    "jajka_kurki_zielononóżki",
                    ["jajka kurki zielononóżki", "jajek kurki zielononóżki"],
                ),
                True,
            ),
            pytest.param(
                "6 jajek kurki zielononóżki",
                RegexEntry(
                    "jajka_kurki_zielononóżki",
                    ["jajka kurki zielononóżki", "jajek kurki zielononóżki"],
                ),
                True,
            ),
            pytest.param(
                "kilka jajek kurki zielononóżki",
                RegexEntry(
                    "jajka_kurki_zielononóżki",
                    ["jajka kurki zielononóżki", "jajek kurki zielononóżki"],
                ),
                True,
            ),
            pytest.param(
                "2 łyżki oliwy z oliwek extra virgin",
                RegexEntry(
                    "oliwa_extra_virgin",
                    ["oliwa z oliwek extra virgin", "oliwy z oliwek extra virgin"],
                ),
                True,
            ),
            pytest.param(
                "kilka kropel oliwy z oliwek extra virgin",
                RegexEntry(
                    "oliwa_extra_virgin",
                    ["oliwa z oliwek extra virgin", "oliwy z oliwek extra virgin"],
                ),
                True,
            ),
            pytest.param(
                "100 ml oliwy z oliwek extra virgin",
                RegexEntry(
                    "oliwa_extra_virgin",
                    ["oliwa z oliwek extra virgin", "oliwy z oliwek extra virgin"],
                ),
                True,
            ),
            pytest.param(
                "3 łyżki cukru trzcinowego nierafinowanego",
                RegexEntry(
                    "cukier_trzcinowy",
                    ["cukier trzcinowy nierafinowany", "cukru trzcinowego nierafinowanego"],
                ),
                True,
            ),
            pytest.param(
                "szczypta cukru trzcinowego nierafinowanego",
                RegexEntry(
                    "cukier_trzcinowy",
                    ["cukier trzcinowy nierafinowany", "cukru trzcinowego nierafinowanego"],
                ),
                True,
            ),
            pytest.param(
                "pół szklanki cukru trzcinowego nierafinowanego",
                RegexEntry(
                    "cukier_trzcinowy",
                    ["cukier trzcinowy nierafinowany", "cukru trzcinowego nierafinowanego"],
                ),
                True,
            ),
            pytest.param(
                "50 g sera dojrzewającego typu parmezan",
                RegexEntry(
                    "ser_parmezan",
                    ["ser dojrzewający typu parmezan", "sera dojrzewającego typu parmezan"],
                ),
                True,
            ),
            pytest.param(
                "dwie łyżki sera dojrzewającego typu parmezan",
                RegexEntry(
                    "ser_parmezan",
                    ["ser dojrzewający typu parmezan", "sera dojrzewającego typu parmezan"],
                ),
                True,
            ),
            pytest.param(
                "odrobina sera dojrzewającego typu parmezan",
                RegexEntry(
                    "ser_parmezan",
                    ["ser dojrzewający typu parmezan", "sera dojrzewającego typu parmezan"],
                ),
                True,
            ),
        ]
    )
    def test_contains__multiple_words(self, text, entry, expected):
        assert expected == entry.contains(text)



class TestRegexEntryFind:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("mleko", ["mleko"]),
            ("Mleko", ["Mleko"]),
            ("2 mleka i masło", ["mleka"]),
            ("Jedno mleko", ["mleko"]),
            ("", []),
            ("2 mleczne", []),
            ("2 mleka i 1 mleko", ["mleka", "mleko"])

        ]
    )
    def test_find_happy_path(self, text, expected):
        entry = RegexEntry("mleko", ["mleko", "mleka"])
        assert entry.find(text) == expected




class TestRegexEntryFindSpan:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("mleko", [(0,5)]),
            ("2 mleka", [(2, 7)]),
            ("", []),
            ("mleko czekoladowe i 2 mleka waniliowe", [(0,5), (22, 27)]),
            ("43 masła", []),
            ("43 masła", []),
        ]
    )
    def test_find_span_happy_path(self, text, expected):
        entry = RegexEntry("mleko", ["mleko", "mleka"])
        assert entry.find_spans(text) == expected


class TestRegexEntryAddVariant:

    def test_add_variant_adds_new_value(self):
        entry = RegexEntry("mleko", ["mleko"])
        entry.add_variant("mleka")

        assert "mleka" in entry.variants
        assert entry.contains("mleka")

    def test_add_variant_strips_whitespace(self):
        entry = RegexEntry("mleko", ["mleko"])
        entry.add_variant("  mleka  ")

        assert "mleka" in entry.variants

    def test_add_variant_ignores_empty_string(self):
        entry = RegexEntry("mleko", ["mleko"])
        entry.add_variant("   ")

        assert entry.variants == {"mleko"}



class TestRegexEntryRemoveVariant:

    def test_remove_existing_variant(self):
        entry = RegexEntry("mleko", ["mleko", "mleka"])
        entry.remove_variant("mleka")

        assert "mleka" not in entry.variants
        assert not entry.contains("mleka")



    def test_remove_ignores_non_existing_variant(self):
        entry = RegexEntry("mleko", ["mleko"])
        entry.remove_variant("masło")

        assert entry.variants == {"mleko"}

    def test_remove_ignores_empty_string(self):
        entry = RegexEntry("mleko", ["mleko"])
        entry.remove_variant("   ")

        assert entry.variants == {"mleko"}



class TestRegexEntryEquality:

    def test_entries_with_same_stem_are_equal(self):
        e1 = RegexEntry("mleko", ["mleko"])
        e2 = RegexEntry("mleko", ["mleko", "mleka"])

        assert e1 == e2
        assert hash(e1) == hash(e2)

    def test_entries_with_different_stem_are_not_equal(self):
        e1 = RegexEntry("mleko", ["mleko"])
        e2 = RegexEntry("maslo", ["maslo"])

        assert e1 != e2

    def test_entry_can_be_used_in_set(self):
        e1 = RegexEntry("mleko", ["mleko"])
        e2 = RegexEntry("mleko", ["mleka"])

        s = {e1, e2}
        assert len(s) == 1
