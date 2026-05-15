from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Mapping, Union

PathLike = Union[str, Path]



@dataclass(frozen=True, slots=True, kw_only=True)
class AgentConfig:
    model: str = "gpt-4o-mini"
    timeout: int = 20
    ensemble_size: int = 5
    max_retries: int = 3

@dataclass(frozen=True, slots=True, kw_only=True)
class FileStorageConfig:
    kind:Literal["file"] = "file"
    output_dir:PathLike

@dataclass(frozen=True, slots=True, kw_only=True)
class DatabaseStorageConfig:
    kind: Literal["database"] = "database"
    database_url: str
    echo: bool = False
    pool_pre_ping: bool = True
    create_schema: bool = False
    engine_options: Mapping[str, Any] = field(default_factory=dict)

StorageConfig = FileStorageConfig | DatabaseStorageConfig


@dataclass(frozen=True, slots=True, kw_only=True)
class EngineConfig:
    storage: StorageConfig
    parser: AgentConfig = field(default_factory=AgentConfig)
    categorizer: AgentConfig = field(default_factory=AgentConfig)



