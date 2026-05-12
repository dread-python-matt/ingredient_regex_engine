from collections import Counter
from unittest.mock import AsyncMock, create_autospec

import pytest

from regex_engine.application.use_cases.regex_service_default import RegexServiceDefault
from regex_engine.domain.enums import EnsureWordStatus, RegexKind
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.ports.regex_registry import RegexRegistryReader, RegexRegistryWriter
from regex_engine.ports.token_normalizer import TokenNormalizer

@pytest.fixture
def kind() -> RegexKind:
    return next(iter(RegexKind))

@pytest.fixture
def normalizer() -> TokenNormalizer:
    mock = create_autospec(TokenNormalizer, instance=True, spec_set=True)
    mock.stem = AsyncMock()
    mock.inflect = AsyncMock()
    return mock


@pytest.fixture
def reader(kind: RegexKind) -> RegexRegistryReader:
    mock = create_autospec(RegexRegistryReader, instance=True, spec_set=True)
    mock.kind = kind
    mock.match_best.return_value = None
    mock.get.return_value = None
    return mock


@pytest.fixture
def writer() -> RegexRegistryWriter:
    mock = create_autospec(RegexRegistryWriter, instance=True, spec_set=True)
    mock.add_variant.return_value = None
    mock.add_entry.return_value = None
    return mock


@pytest.fixture
def service(
    normalizer: TokenNormalizer,
    reader: RegexRegistryReader,
    writer: RegexRegistryWriter,
) -> RegexServiceDefault:
    return RegexServiceDefault(
        normalizer=normalizer,
        regex_registry_writer=writer,
        regex_registry_reader=reader,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("word", ["", "  ", "\n", "\n\t "])
async def test_ensure_word_skips_empty_input(
    service: RegexServiceDefault,
    reader: RegexRegistryReader,
    writer: RegexRegistryWriter,
    normalizer: TokenNormalizer,
    kind: RegexKind,
    word: str,
) -> None:
    result = await service.ensure_word_included_in_registry(word)

    assert result.kind == kind
    assert result.status == EnsureWordStatus.SKIPPED_EMPTY
    assert result.stem == ""
    assert result.word == ""

    reader.match_best.assert_not_called()
    reader.get.assert_not_called()
    writer.add_variant.assert_not_called()
    writer.add_entry.assert_not_called()
    normalizer.stem.assert_not_called()
    normalizer.inflect.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("word", "expected_word"),
    [
        ("masło", "masło"),
        ("  vanilia", "vanilia"),
        ("sok  pomarańczowy", "sok  pomarańczowy"),
        ("  masło  \n ", "masło"),
    ],
)
async def test_ensure_word_returns_already_matched_when_registry_matches_input(
    service: RegexServiceDefault,
    reader: RegexRegistryReader,
    writer: RegexRegistryWriter,
    normalizer: TokenNormalizer,
    kind: RegexKind,
    word: str,
    expected_word: str,
) -> None:
    reader.match_best.return_value = RegexEntry("dummy_stem", ("dummy",))

    result = await service.ensure_word_included_in_registry(word)

    assert result.kind == kind
    assert result.status == EnsureWordStatus.ALREADY_MATCHED
    assert result.stem == expected_word
    assert result.word == expected_word

    reader.match_best.assert_called_once_with(expected_word)
    reader.get.assert_not_called()
    normalizer.stem.assert_not_called()
    normalizer.inflect.assert_not_called()
    writer.add_variant.assert_not_called()
    writer.add_entry.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("word", "expected_word", "expected_stem"),
    [
        ("mleka", "mleka", "mleko"),
        ("ciasta czekoladowego", "ciasta czekoladowego", "ciasto_czekoladowe"),
        ("\n maślanki  ", "maślanki", "maślanka"),
    ],
)
async def test_ensure_word_adds_variant_when_stem_already_exists(
    service: RegexServiceDefault,
    reader: RegexRegistryReader,
    writer: RegexRegistryWriter,
    normalizer: TokenNormalizer,
    kind: RegexKind,
    word: str,
    expected_word: str,
    expected_stem: str,
) -> None:
    existing_entry = RegexEntry(expected_stem, (expected_stem,))
    normalizer.stem.return_value = expected_stem
    reader.get.return_value = existing_entry

    result = await service.ensure_word_included_in_registry(word)

    assert result.kind == kind
    assert result.status == EnsureWordStatus.UPDATED_EXISTING
    assert result.stem == expected_stem
    assert result.word == expected_word

    reader.match_best.assert_called_once_with(expected_word)
    normalizer.stem.assert_awaited_once_with(expected_word)
    reader.get.assert_called_once_with(expected_stem)
    writer.add_variant.assert_called_once_with(stem=expected_stem, variant=expected_word)

    normalizer.inflect.assert_not_called()
    writer.add_entry.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("word", "expected_word", "expected_stem", "inflected_variants"),
    [
        ("masło", "masło", "masło", ("masło",)),
        ("mleka", "mleka", "mleko", ("mleko", "mleka")),
    ],
)
async def test_ensure_word_creates_new_entry_when_stem_does_not_exist(
    service: RegexServiceDefault,
    reader: RegexRegistryReader,
    writer: RegexRegistryWriter,
    normalizer: TokenNormalizer,
    kind: RegexKind,
    word: str,
    expected_word: str,
    expected_stem: str,
    inflected_variants: tuple[str, ...],
) -> None:
    normalizer.stem.return_value = expected_stem
    normalizer.inflect.return_value = inflected_variants
    reader.get.return_value = None

    result = await service.ensure_word_included_in_registry(word)

    assert result.kind == kind
    assert result.status == EnsureWordStatus.CREATED_NEW
    assert result.stem == expected_stem
    assert result.word == expected_word

    reader.match_best.assert_called_once_with(expected_word)
    normalizer.stem.assert_awaited_once_with(expected_word)
    reader.get.assert_called_once_with(expected_stem)
    normalizer.inflect.assert_awaited_once_with(expected_stem)
    writer.add_entry.assert_called_once()

    added_entry = writer.add_entry.call_args.args[0]
    assert isinstance(added_entry, RegexEntry)
    assert added_entry.stem == expected_stem
    assert Counter(added_entry.variants) == Counter(set(inflected_variants) | {expected_word})

    writer.add_variant.assert_not_called()


@pytest.mark.asyncio
async def test_ensure_word_returns_failed_when_stem_raises(
    service: RegexServiceDefault,
    reader: RegexRegistryReader,
    writer: RegexRegistryWriter,
    normalizer: TokenNormalizer,
    kind: RegexKind,
) -> None:
    normalizer.stem.side_effect = RuntimeError("stem failure")
    word = "  mleka  "

    result = await service.ensure_word_included_in_registry(word)

    assert result.kind == kind
    assert result.status == EnsureWordStatus.FAILED
    assert result.stem == word
    assert result.word == word
    assert isinstance(result.exception, RuntimeError)

    reader.match_best.assert_called_once_with("mleka")
    normalizer.stem.assert_awaited_once_with("mleka")
    reader.get.assert_not_called()
    normalizer.inflect.assert_not_called()
    writer.add_variant.assert_not_called()
    writer.add_entry.assert_not_called()