from dataclasses import dataclass

from regex_engine.ports.regex_registry import RegexRegistryReader, RegexRegistryWriter


@dataclass(slots=True)
class RegistryContainerReader:
    ingredient_registry: RegexRegistryReader
    unit_registry: RegexRegistryReader
    unit_size_registry: RegexRegistryReader
    condition_registry: RegexRegistryReader
    or_conjunctions_registry: RegexRegistryReader
    and_conjunctions_registry: RegexRegistryReader


@dataclass(slots=True)
class RegistryContainerWriter:
    ingredient_registry: RegexRegistryWriter
    unit_registry: RegexRegistryWriter
    unit_size_registry: RegexRegistryWriter
    condition_registry: RegexRegistryWriter
    or_conjunctions_registry: RegexRegistryWriter
    and_conjunctions_registry: RegexRegistryWriter


@dataclass(slots=True)
class RegistryContainer:
    reader: RegistryContainerReader
    writer: RegistryContainerWriter
