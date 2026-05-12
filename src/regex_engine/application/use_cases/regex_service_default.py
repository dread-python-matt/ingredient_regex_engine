import logging

from regex_engine.domain.enums import EnsureWordStatus
from regex_engine.domain.models.orchestrator import EnsureWordResult
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.ports.regex_registry import RegexRegistryReader, RegexRegistryWriter
from regex_engine.ports.token_normalizer import TokenNormalizer

logger = logging.getLogger("regex_service")


class RegexServiceDefault:
    def __init__(
        self,
        normalizer: TokenNormalizer,
        regex_registry_writer: RegexRegistryWriter,
        regex_registry_reader: RegexRegistryReader,
    ):
        self._normalizer = normalizer
        self._regex_registry_reader: RegexRegistryReader = regex_registry_reader
        self._regex_registry_writer: RegexRegistryWriter = regex_registry_writer

    async def ensure_word_included_in_registry(self, word: str) -> EnsureWordResult:
        kind = self._regex_registry_reader.kind
        try:
            w = word.strip()
            if not w:
                logger.info("Word is empty")
                return EnsureWordResult(
                    kind=kind, status=EnsureWordStatus.SKIPPED_EMPTY, stem=w, word=w
                )

            hit = self._regex_registry_reader.match_best(w)
            if hit:
                logger.info("Word: %s can be matched by: %s", w, hit)
                return EnsureWordResult(
                    kind=kind, status=EnsureWordStatus.ALREADY_MATCHED, stem=w, word=w
                )

            stem = await self._normalizer.stem(w)

            existing = self._regex_registry_reader.get(stem)

            if existing:
                logger.info("Found word %s stem: %s", w, existing)
                logger.info("Updating %s regex", stem)
                self._regex_registry_writer.add_variant(stem=stem, variant=w)
                logger.info("Done")
                return EnsureWordResult(
                    kind=kind, status=EnsureWordStatus.UPDATED_EXISTING, stem=existing.stem, word=w
                )

            logger.info("Creating word variants...")
            word_variants = await self._normalizer.inflect(stem)
            logger.info("Done")

            entry = RegexEntry(stem, variants=word_variants)
            entry.add_variant(w)
            logger.info("Adding %s to database...", entry)
            self._regex_registry_writer.add_entry(entry)
            logger.info("Done")
            return EnsureWordResult(
                kind=kind, status=EnsureWordStatus.CREATED_NEW, stem=stem, word=w
            )

        except Exception as e:
            logger.error("Error encountered: %s", e)
            return EnsureWordResult(
                kind=kind, status=EnsureWordStatus.FAILED, stem=word, word=word, exception=e
            )
