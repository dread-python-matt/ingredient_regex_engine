import logging

import morfeusz2

from regex_engine.adapters.db.regex.demo_regex_repository import DemoRegexRepository
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
from regex_engine.adapters.parser.demo_parser import DemoIngredientParser
from regex_engine.application.dto.agent.parsed_ingredient import ParsedIngredient
from regex_engine.application.use_cases.amount_extractor_default import AmountExtractorDefault
from regex_engine.application.use_cases.ingredient_learning_engine import (
    IngredientLearningEngineDefault,
)
from regex_engine.application.use_cases.ingredient_regex_engine_demo import (
    IngredientRegexEngineDemo,
)
from regex_engine.application.use_cases.learning_rules_default import LearningRulesDefaults
from regex_engine.application.use_cases.regex_orchestrator_default import RegexOrchestratorDefault
from regex_engine.application.use_cases.regex_resolver_default import RegexResolverDefault
from regex_engine.application.use_cases.regex_service_default import RegexServiceDefault
from regex_engine.domain.enums import RegexKind
from regex_engine.domain.models.registry_container import RegistryContainerReader
from regex_engine.ports.ingredient_regex_engine import IngredientRegexEngine

logger = logging.getLogger(__name__)


def create_demo_ingredient_regex_engine(
    mapping: dict[str:ParsedIngredient],
) -> IngredientRegexEngine:
    logger.info("Creating ingredient regex engine demo ...")

    morfeusz = morfeusz2.Morfeusz()

    inflector = Inflector(morfeusz)
    phrase_analyser = PhraseAnalyser(morfeusz)

    ingredient_normalizer = MorfeuszIngredientNameNormalizer(
        inflector=inflector, phrase_analyser=phrase_analyser
    )
    unit_normalizer = MorfeuszUnitNormalizer(inflector=inflector, morfeusz=morfeusz)
    unit_size_normalizer = MorfeuszAdjectiveNormalizer(inflector=inflector, morfeusz=morfeusz)
    condition_normalizer = MorfeuszAdjectiveNormalizer(inflector=inflector, morfeusz=morfeusz)

    regex_repository = DemoRegexRepository()

    ingredient_registry = regex_repository.load(RegexKind.INGREDIENT_NAME)
    unit_registry = regex_repository.load(RegexKind.UNIT)
    unit_size_registry = regex_repository.load(RegexKind.UNIT_SIZE)
    condition_registry = regex_repository.load(RegexKind.INGREDIENT_CONDITION)
    or_conjunctions_registry = regex_repository.load(RegexKind.OR_CONJUNCTIONS)
    and_conjunctions_registry = regex_repository.load(RegexKind.AND_CONJUNCTIONS)

    registry_container = RegistryContainerReader(
        ingredient_registry=ingredient_registry,
        unit_registry=unit_registry,
        unit_size_registry=unit_size_registry,
        condition_registry=condition_registry,
        or_conjunctions_registry=or_conjunctions_registry,
        and_conjunctions_registry=and_conjunctions_registry,
    )

    ingredient_service = RegexServiceDefault(
        normalizer=ingredient_normalizer,
        regex_registry_writer=ingredient_registry,
        regex_registry_reader=ingredient_registry,
    )

    unit_service = RegexServiceDefault(
        normalizer=unit_normalizer,
        regex_registry_writer=unit_registry,
        regex_registry_reader=unit_registry,
    )

    unit_size_service = RegexServiceDefault(
        normalizer=unit_size_normalizer,
        regex_registry_writer=unit_size_registry,
        regex_registry_reader=unit_size_registry,
    )

    condition_service = RegexServiceDefault(
        normalizer=condition_normalizer,
        regex_registry_writer=condition_registry,
        regex_registry_reader=condition_registry,
    )

    services_by_kind = {
        RegexKind.INGREDIENT_NAME: ingredient_service,
        RegexKind.UNIT: unit_service,
        RegexKind.UNIT_SIZE: unit_size_service,
        RegexKind.INGREDIENT_CONDITION: condition_service,
    }

    regex_orchestrator = RegexOrchestratorDefault(services_by_kind=services_by_kind)

    amount_extractor = AmountExtractorDefault(and_conjunctions_registry)

    resolver = RegexResolverDefault(
        amount_extractor=amount_extractor,
        ingredient_names=ingredient_registry,
        ingredient_conditions=condition_registry,
        unit_sizes=unit_size_registry,
        units=unit_registry,
        or_conjunctions=or_conjunctions_registry,
        and_conjunctions=and_conjunctions_registry,
    )

    parser = DemoIngredientParser(mapping)

    learning_rules = LearningRulesDefaults(resolver, and_conjunctions=and_conjunctions_registry)

    filter_engine = IngredientLearningEngineDefault(
        regex_orchestrator=regex_orchestrator,
        learning_rules=learning_rules,
        parser=parser,
    )

    input_adapters = [StringInputAdapter(), StringListInputAdapter(), PandasInputAdapter()]

    input_router_adapter = InputRouter(*input_adapters)

    ingredient_regex_engine = IngredientRegexEngineDemo(
        filter_engine=filter_engine,
        input_adapter=input_router_adapter,
        registries=registry_container,
        resolver=resolver,
    )

    logger.info("Successfully created demo IngredientRegexEngine")
    return ingredient_regex_engine
