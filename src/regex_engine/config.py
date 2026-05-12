from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

PathLike = Union[str, Path]


def _resolve_dir(path: PathLike, base_dir: Optional[Path] = None) -> Path:
    p = Path(path).expanduser()

    if not p.is_absolute():
        if base_dir is not None:
            p = base_dir / p
        else:
            p = p.resolve()

    p = p.resolve()

    if p.exists() and not p.is_dir():
        raise ValueError(f"Expected directory, got file: {p}")

    p.mkdir(parents=True, exist_ok=True)
    return p


@dataclass
class AgentConfig:
    model: str = "gpt-4o-mini"
    timeout: int = 20
    ensemble_size: int = 5
    max_retries: int = 3


@dataclass(slots=True)
class EngineConfig:
    output_dir: Path
    parser: "AgentConfig"
    categorizer: "AgentConfig"

    def __post_init__(self):
        self.output_dir = _resolve_dir(self.output_dir)

    @classmethod
    def create(
        cls,
        output_dir: PathLike,
        parser: "AgentConfig",
        categorizer: "AgentConfig",
        base_dir: Optional[PathLike] = None,
    ) -> "EngineConfig":
        base = Path(base_dir).resolve() if base_dir else None
        resolved_output = _resolve_dir(output_dir, base)

        return cls(
            output_dir=resolved_output,
            parser=parser,
            categorizer=categorizer,
        )
