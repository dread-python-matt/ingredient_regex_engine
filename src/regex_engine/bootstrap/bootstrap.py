import logging
import os
from dataclasses import dataclass
from pathlib import Path


import morfeusz2
from sqlalchemy.orm.session import sessionmaker, Session

from regex_engine.adapters.categorizer.agent_categorizer import AgentCategorizer
from regex_engine.adapters.categorizer.agent_categorizer_client import AgentCategorizerClient
from regex_engine.adapters.categorizer.categorizer_service_default import CategorizerServiceDefault
from regex_engine.adapters.db.file.category.file_category_repository import FileCategoryRepository
from regex_engine.adapters.db.file.regex.file_categorized_ingredient_regex_repository import (
    FileCategorizedIngredientRegexRepository,
)
from regex_engine.adapters.db.sqlalchemy.models import Base
from regex_engine.adapters.db.sqlalchemy.sql_category_repository import SQLAlchemyCategoryRepository
from regex_engine.adapters.db.sqlalchemy.sql_regex_repository import SQLAlchemyRegexRepository
from regex_engine.adapters.input_adapters.input_router import InputRouter
from regex_engine.adapters.input_adapters.pandas_input_adapter import PandasInputAdapter
from regex_engine.adapters.input_adapters.string_input_adapter import StringInputAdapter
from regex_engine.adapters.input_adapters.string_iterable_input_adapter import (
    StringListInputAdapter,
)
from regex_engine.adapters.normalizers.morfeusz.adjective_normalizer import (
    MorfeuszAdjectiveNormalizer,
)
from regex_engine.adapters.normalizers.morfeusz.inflector.inflector import Inflector
from regex_engine.adapters.normalizers.morfeusz.ingredient_name import (
    MorfeuszIngredientNameNormalizer,
)
from regex_engine.adapters.normalizers.morfeusz.phrase_analyzer import PhraseAnalyser
from regex_engine.adapters.normalizers.morfeusz.unit_normalizer import MorfeuszUnitNormalizer
from regex_engine.adapters.parser.agent_ingredient_parser.agent_client import AgentParserClient
from regex_engine.adapters.parser.agent_ingredient_parser.agent_ingredient_parser import (
    AgentIngredientParser,
)
from regex_engine.application.use_cases.amount_extractor_default import AmountExtractorDefault
from regex_engine.application.use_cases.ingredient_learning_engine import (
    IngredientLearningEngineDefault,
)
from regex_engine.application.use_cases.ingredient_regex_engine import IngredientRegexEngineDefault
from regex_engine.application.use_cases.learning_rules_default import LearningRulesDefaults
from regex_engine.application.use_cases.regex_orchestrator_default import RegexOrchestratorDefault
from regex_engine.application.use_cases.regex_resolver_default import RegexResolverDefault
from regex_engine.application.use_cases.regex_service_default import RegexServiceDefault
from regex_engine.config import AgentConfig, EngineConfig, StorageConfig, PathLike, FileStorageConfig, \
    DatabaseStorageConfig
from regex_engine.domain.enums import RegexKind
from regex_engine.domain.errors import ConfigurationError, InvalidModelError
from regex_engine.domain.models.regex_entry import RegexEntry
from regex_engine.domain.models.regex_registry_default import RegexRegistryDefault
from regex_engine.domain.models.registry_container import (
    RegistryContainer,
    RegistryContainerReader,
    RegistryContainerWriter,
)
from regex_engine.ports.categories_repository import CategoryRepository
from regex_engine.ports.categorizer import Categorizer
from regex_engine.ports.categorizer_service import CategorizerService
from regex_engine.ports.ingredient_parser import IngredientParser
from regex_engine.ports.ingredient_regex_engine import IngredientRegexEngine
from regex_engine.ports.regex_registry import RegexRegistry, RegexRegistryRepository
from sqlalchemy import create_engine

logger = logging.getLogger("bootstrap")


@dataclass(frozen=True, slots=True)
class RepositoryBundle:
    regex_repository: RegexRegistryRepository
    category_repository: CategoryRepository


async def create_ingredient_regex_engine(config: EngineConfig) -> IngredientRegexEngine:
    logger.info("Creating IngredientRegexEngine ...")
    validate_environment()

    repository_bundle = _build_repository(config.storage)

    categorizer = await create_categorizer(config.categorizer)

    parser = await create_parser(config.parser)

    categorizer_service = CategorizerServiceDefault(
        categorizer=categorizer,
        repository=repository_bundle.category_repository,
    )
    engine = _build_engine(
        regex_repository=repository_bundle.regex_repository, categorizer_service=categorizer_service, parser=parser
    )
    logger.info("Successfully created IngredientRegexEngine")

    return engine


def _build_repository(config:StorageConfig):
    match config:
        case FileStorageConfig(output_dir=output_dir):
            output_path = _resolve_output_dir(output_dir)

            category_repository = FileCategoryRepository(output_path)
            categorized_ingredients = category_repository.load()

            regex_repository = FileCategorizedIngredientRegexRepository(
                output_path,
                categorized_ingredients,
            )

            return RepositoryBundle(
                regex_repository=regex_repository,
                category_repository=category_repository,
            )

        case DatabaseStorageConfig() as db_config:
            engine = create_engine(
                db_config.database_url,
                echo=db_config.echo,
                pool_pre_ping=db_config.pool_pre_ping,
                **db_config.engine_options,
            )
            if config.create_schema:
                Base.metadata.create_all(engine)

            session_factory = sessionmaker(
                bind=engine,
                class_=Session,
                expire_on_commit=False,
            )

            return RepositoryBundle(
                regex_repository=SQLAlchemyRegexRepository(session_factory),
                category_repository=SQLAlchemyCategoryRepository(session_factory),
            )

        case _:
            raise ConfigurationError(f"Unsupported storage config: {config!r}")


def _resolve_output_dir(path: PathLike) -> Path:
    output_dir = Path(path).expanduser().resolve()

    if output_dir.exists() and not output_dir.is_dir():
        raise ConfigurationError(f"Expected directory, got file: {output_dir}")

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ConfigurationError(
            f"Could not create output directory: {output_dir}"
        ) from exc

    return output_dir


def validate_environment() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise ConfigurationError("Missing OPENAI_API_KEY")


async def create_categorizer(config: AgentConfig) -> Categorizer:
    logger.info("Creating Categorizer ...")
    try:
        categorizer_agent_client = await AgentCategorizerClient.create(
            model=config.model, timeout=config.timeout
        )
        categorizer = AgentCategorizer(
            categorizer_agent_client=categorizer_agent_client,
            ensemble_size=config.ensemble_size,
            max_retries=config.max_retries,
        )
        logger.info("Successfully created Categorizer")
        return categorizer
    except InvalidModelError as e:
        logger.error("Failed to create Categorizer | reason=%s", e)
        raise ConfigurationError(f"Invalid categorizer model: {config.model}")


async def create_parser(config: AgentConfig) -> IngredientParser:
    logger.info("Creating Parser ...")
    try:
        parser_agent_client = await AgentParserClient.create(
            model=config.model, timeout=config.timeout
        )
        parser = AgentIngredientParser(
            ensemble_size=config.ensemble_size,
            max_retries=config.max_retries,
            parser_client=parser_agent_client,
        )
        logger.info("Successfully created Parser")
        return parser
    except InvalidModelError as e:
        logger.error("Failed to create IngredientParser | reason=%s", e)
        raise ConfigurationError(f"Invalid parser model: {config.model}")


def _load_regex_registries(regex_repository: RegexRegistryRepository) -> RegistryContainer:
    ingredient_registry = regex_repository.load(RegexKind.INGREDIENT_NAME)
    unit_registry = regex_repository.load(RegexKind.UNIT)
    unit_size_registry = regex_repository.load(RegexKind.UNIT_SIZE)
    condition_registry = regex_repository.load(RegexKind.INGREDIENT_CONDITION)
    or_conjunctions_registry = regex_repository.load(RegexKind.OR_CONJUNCTIONS)
    and_conjunctions_registry = regex_repository.load(RegexKind.AND_CONJUNCTIONS)

    if not or_conjunctions_registry.get_all():
        or_conjunctions_registry = _create_or_conjunction_registry()

    if not and_conjunctions_registry.get_all():
        and_conjunctions_registry = _create_and_conjunction_registry()

    reader_container = RegistryContainerReader(
        ingredient_registry=ingredient_registry,
        unit_registry=unit_registry,
        unit_size_registry=unit_size_registry,
        condition_registry=condition_registry,
        or_conjunctions_registry=or_conjunctions_registry,
        and_conjunctions_registry=and_conjunctions_registry,
    )

    writer_container = RegistryContainerWriter(
        ingredient_registry=ingredient_registry,
        unit_registry=unit_registry,
        unit_size_registry=unit_size_registry,
        condition_registry=condition_registry,
        or_conjunctions_registry=or_conjunctions_registry,
        and_conjunctions_registry=and_conjunctions_registry,
    )

    return RegistryContainer(
        reader=reader_container,
        writer=writer_container,
    )


def _build_entry(word: str, variants: list[str]):
    return RegexEntry(stem=word, variants=variants)


def _build_registry(kind: RegexKind, words: dict[str, list[str]]) -> RegexRegistry:
    return RegexRegistryDefault(
        kind, [_build_entry(word, variants) for word, variants in words.items()]
    )


def _create_and_conjunction_registry():
    and_conjunctions = {"i": ["i"], "oraz": ["oraz"]}
    return _build_registry(RegexKind.AND_CONJUNCTIONS, and_conjunctions)


def _create_or_conjunction_registry():
    or_conjunctions = {
        "albo": ["albo"],
        "bądź": ["bądź"],
        "ewentualnie": ["ewentualnie"],
        "lub": ["lub"],
        "lub_też": ["lub też"],
    }
    return _build_registry(RegexKind.OR_CONJUNCTIONS, or_conjunctions)


def _build_engine(
    regex_repository: RegexRegistryRepository,
    categorizer_service: CategorizerService,
    parser: IngredientParser,
):

    registries = _load_regex_registries(regex_repository)

    morfeusz = morfeusz2.Morfeusz()

    inflector = Inflector(morfeusz)
    phrase_analyser = PhraseAnalyser(morfeusz)

    ingredient_normalizer = MorfeuszIngredientNameNormalizer(
        inflector=inflector, phrase_analyser=phrase_analyser
    )
    unit_normalizer = MorfeuszUnitNormalizer(inflector=inflector, morfeusz=morfeusz)
    unit_size_normalizer = MorfeuszAdjectiveNormalizer(inflector=inflector, morfeusz=morfeusz)
    ingredient_condition_normalizer = MorfeuszAdjectiveNormalizer(
        inflector=inflector, morfeusz=morfeusz
    )

    ingredient_service = RegexServiceDefault(
        normalizer=ingredient_normalizer,
        regex_registry_writer=registries.writer.ingredient_registry,
        regex_registry_reader=registries.reader.ingredient_registry,
    )

    unit_service = RegexServiceDefault(
        normalizer=unit_normalizer,
        regex_registry_reader=registries.reader.unit_registry,
        regex_registry_writer=registries.writer.unit_registry,
    )

    unit_size_service = RegexServiceDefault(
        normalizer=unit_size_normalizer,
        regex_registry_reader=registries.reader.unit_size_registry,
        regex_registry_writer=registries.writer.unit_size_registry,
    )

    ingredient_condition_service = RegexServiceDefault(
        normalizer=ingredient_condition_normalizer,
        regex_registry_reader=registries.reader.condition_registry,
        regex_registry_writer=registries.writer.condition_registry,
    )

    services_by_kind = {
        registries.reader.ingredient_registry.kind: ingredient_service,
        registries.reader.unit_registry.kind: unit_service,
        registries.reader.unit_size_registry.kind: unit_size_service,
        registries.reader.condition_registry.kind: ingredient_condition_service,
    }

    regex_orchestrator = RegexOrchestratorDefault(
        services_by_kind=services_by_kind,
    )

    amount_extractor = AmountExtractorDefault(registries.reader.and_conjunctions_registry)

    resolver = RegexResolverDefault(
        amount_extractor=amount_extractor,
        ingredient_names=registries.reader.ingredient_registry,
        ingredient_conditions=registries.reader.condition_registry,
        unit_sizes=registries.reader.unit_size_registry,
        units=registries.reader.unit_registry,
        or_conjunctions=registries.reader.or_conjunctions_registry,
        and_conjunctions=registries.reader.and_conjunctions_registry,
    )

    learning_rules = LearningRulesDefaults(
        resolver, and_conjunctions=registries.reader.and_conjunctions_registry
    )

    filter_engine = IngredientLearningEngineDefault(
        regex_orchestrator=regex_orchestrator, learning_rules=learning_rules, parser=parser
    )

    input_adapters = [StringInputAdapter(), StringListInputAdapter(), PandasInputAdapter()]

    input_router_adapter = InputRouter(*input_adapters)

    return IngredientRegexEngineDefault(
        filter_engine=filter_engine,
        input_adapter=input_router_adapter,
        regex_repository=regex_repository,
        registries=registries.reader,
        categorizer_service=categorizer_service,
        resolver=resolver,
    )
