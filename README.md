# 🧬 Ingredient Regex Engine — Hybrid LLM + Regex NLP

> A hybrid **LLM + regex** NLP engine that extracts and normalizes structured ingredient data from
> semi-structured Polish recipe text, then compiles reusable regex registries so that runtime
> recognition needs **no language model at all**.

<p>
  <img alt="CI" src="https://github.com/romanroman008/ingredient_regex_engine/actions/workflows/ci.yml/badge.svg">
  <a href="https://codecov.io/gh/romanroman008/ingredient_regex_engine"><img alt="codecov" src="https://codecov.io/gh/romanroman008/ingredient_regex_engine/graph/badge.svg"></a>
  <img alt="Language" src="https://img.shields.io/badge/Python-3.10%2B-3776AB">
  <img alt="Pydantic" src="https://img.shields.io/badge/Pydantic-v2-E92063">
  <img alt="LLM" src="https://img.shields.io/badge/LLM-OpenAI%20Agents%20SDK-412991">
  <img alt="NLP" src="https://img.shields.io/badge/NLP-Morfeusz2-1F8AC0">
  <img alt="Persistence" src="https://img.shields.io/badge/persistence-SQLAlchemy%20%2F%20PostgreSQL-D71F00">
  <img alt="Architecture" src="https://img.shields.io/badge/architecture-Hexagonal-8A2BE2">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## 📑 Table of Contents

1. [Purpose](#-purpose)
2. [Feature Overview](#-feature-overview)
3. [Tech Stack](#-tech-stack)
4. [Architecture](#-architecture)
5. [Workflow](#-workflow)
6. [Quickstart](#-quickstart)
7. [Cost Profile](#-cost-profile)
8. [Public API Surface](#-public-api-surface)
9. [Credits & License](#-credits--license)

---

## 🎯 Purpose

Recipe and food data is written by humans in free text: `"3 duże garści świeżego szpinaku
(lub rukoli)"`. Downstream systems (shopping lists, diet planners, e-commerce catalogs) need clean
structured records:

```json
{
  "raw_input": "3 duże garści świeżego szpinaku (lub rukoli)",
  "amount": 3.0,
  "unit_size": "duży",
  "unit": "garść",
  "condition": "świeży",
  "name": "szpinak",
  "extra": "lub rukoli"
}
```

Doing this naïvely with an LLM for every request is slow, non-deterministic, and costs money per
call. This project's thesis is a **two-phase design**:

1. **Learning phase (LLM, one-time / offline)** — an LLM ensemble parses each *distinct* ingredient
   into fields, then Polish morphological analysis (Morfeusz2) expands each field into all its
   inflected forms and compiles them into a regex.
2. **Runtime phase (pure regex, zero LLM cost)** — new inputs are matched against the accumulated
   regex registries deterministically and instantly.

The genuinely hard part — and the project's real intellectual weight — is **handling Polish
inflection**: nouns and adjectives change form across 7 grammatical cases × 2 numbers × 3 genders,
plus phenomena like *pluralia tantum* and multi-noun compounds (`żółtko jajka`, `śmietanka
kremówka`). The engine reconstructs the base lemma and generates the full paradigm so a single stem
matches every surface form.

---

## ✨ Feature Overview

| Feature | Description |
|---|---|
| **LLM → Regex compilation** | Turns LLM-parsed ingredients into reusable, deterministic regex patterns. |
| **Inflection-aware normalization** | Morfeusz2-based lemma recovery + paradigm generation for Polish nouns, adjectives, and units. |
| **Zero LLM cost at runtime** | After learning, `recognize_ingredients()` is pure regex — no API calls. |
| **Fine-grained decomposition** | Extracts `amount`, `unit`, `unit_size`, `condition`, `name`, `extra`. |
| **Self-expanding registries** | New variants are merged into existing `RegexEntry` stems; coverage grows with input. |
| **Ensemble LLM parsing** | Runs N parallel LLM calls and majority-votes the result, with retry-on-failure. |
| **Two storage backends** | File (JSON) repository and SQLAlchemy/PostgreSQL repository, selected by config. |
| **Amount arithmetic** | Understands fractions and `4 i 1/2` (number + conjunction + number → 4.5). |
| **Categorization** | LLM assigns ingredient stems to 22 food categories (`Category` enum). |
| **Demo mode** | `create_demo()` runs the full pipeline with hand-annotated parses — no API key. |

---

## 🧰 Tech Stack

**Language / runtime**
- Python **3.10+** (`pyproject.toml` declares `>=3.10`)

**Core libraries**
- **Pydantic v2** (`2.12.2`) — typed DTOs / LLM structured output
- **openai-agents** (`>=0.2.0`) — Agents SDK for the parsing & categorization pipeline
- **Morfeusz2** (`>=1.99`) — Polish morphological analyzer/generator (the NLP core)
- **SQLAlchemy 2.0** + **Alembic** + **psycopg[binary]** — Postgres persistence & migrations
- **pandas** — DataFrame input adapter
- **python-dotenv** — `.env` / API-key loading

**Tooling / quality**
- **pytest**, **pytest-asyncio**, **pytest-cov**, **coverage** (branch coverage on)
- **testcontainers[postgres]** — real Postgres in integration tests
- **ruff** — lint + import sorting (`E`, `F`, `I`)
- **uv** — dependency resolution / lockfile (`uv.lock`)
- **GitHub Actions** CI + **Codecov** coverage reporting

---

## 🏛 Architecture

The codebase is a textbook **Ports & Adapters (Hexagonal) / Clean Architecture** layout.
Dependencies point inward: adapters depend on ports, ports and use-cases depend on the domain; the
domain depends on nothing.

```mermaid
flowchart TB
    API["api.py — create_engine() / create_demo()"]
    subgraph APP["application (use-cases)"]
        UC["Engine · LearningEngine · Resolver · Orchestrator · Services"]
    end
    subgraph DOMAIN["domain (pure core — no framework imports)"]
        MODELS["models: RegexEntry · RegexRegistry · ResolvedIngredient · grammar"]
        PORTS["ports (typing.Protocol): IngredientParser ·<br/>RegexRegistry · TokenNormalizer · …"]
    end
    subgraph ADAPTERS["adapters (concrete implementations)"]
        PARSE["parser — LLM ensemble (openai-agents)"]
        CAT["categorizer — LLM + majority voting"]
        MORF["normalizers/morfeusz — phrase analysis, inflector"]
        IN["input_adapters — str / list[str] / pandas router"]
        DB["db — file (JSON) + SQLAlchemy repositories"]
    end
    BOOT["bootstrap — composition root (DI)"]

    API --> APP
    APP --> MODELS
    APP -->|"depends on ports"| PORTS
    ADAPTERS -. implements .-> PORTS
    BOOT --> APP
    BOOT --> ADAPTERS
```

Source layout:

```
src/regex_engine/
├── api.py                  # public entrypoints: create_engine(), create_demo()
├── config.py               # frozen dataclass configs (Engine/Agent/Storage)
├── domain/                 # pure business core — no framework imports
│   ├── enums.py            #   RegexKind, Category, status enums
│   ├── errors.py           #   rich exception taxonomy
│   └── models/             #   RegexEntry, RegexRegistry, ResolvedIngredient, grammar…
├── ports/                  # Protocol interfaces (structural typing) — the "ports"
│   ├── ingredient_parser.py, regex_registry.py, token_normalizer.py, …
├── application/            # use-cases orchestrating the domain
│   ├── use_cases/          #   engine, learning engine, resolver, orchestrator, services
│   └── dto/                #   agent + Morfeusz data-transfer objects
├── adapters/               # concrete implementations of the ports
│   ├── parser/             #   LLM ensemble parser (openai-agents)
│   ├── categorizer/        #   LLM categorizer + voting
│   ├── normalizers/morfeusz/  # phrase analysis, inflector, adjective/unit/name normalizers
│   ├── input_adapters/     #   str / list[str] / pandas → IngredientRecord (router)
│   └── db/                 #   file (JSON) + sqlalchemy repositories + manual mappers
└── bootstrap/              # composition root: wires everything via DI
    ├── bootstrap.py        #   production wiring (storage switch, Morfeusz, agents)
    └── bootstap_demo.py    #   demo wiring (no LLM)
```

### Notable design decisions

- **Protocol-based ports.** Interfaces are `typing.Protocol` classes (structural typing), so adapters
  need not inherit from them — clean, Pythonic dependency inversion.
- **Reader/Writer segregation.** Each registry is exposed through separate `RegexRegistryReader` /
  `RegexRegistryWriter` views (a lightweight CQRS split), so recognition code can't accidentally
  mutate registries.
- **Composition root.** `bootstrap.py` is the single place objects are constructed and wired; the rest
  of the code receives dependencies via constructors. No global singletons.
- **Storage strategy via `match`.** `_build_repository()` pattern-matches on a `FileStorageConfig |
  DatabaseStorageConfig` union to pick the backend.
- **Domain/persistence isolation.** SQLAlchemy `RegexEntryRecord`/`CategorizedIngredientRecord` are
  separate from domain `RegexEntry`; explicit mappers translate between them.

---

## 🔄 Workflow

The two-phase thesis at a glance:

```mermaid
flowchart LR
    subgraph LEARN["Learning phase — LLM, offline / one-time"]
        L1["ingredient text"] --> L2["LLM ensemble parse → fields"]
        L2 --> L3["Morfeusz: lemma + full paradigm"]
        L3 --> L4["compile RegexEntry into registries"]
    end
    subgraph RUN["Runtime phase — pure regex, $0 LLM"]
        R1["new input"] --> R2["match against registries"]
        R2 --> R3["ResolvedIngredient"]
    end
    LEARN -. accumulated registries .-> RUN
```

### 1. Learning — `await engine.learn(data, max_iterations=100)`

1. **Input adaptation.** `InputRouter` dispatches `str` / `list[str]` / `pandas` input to the right
   adapter, producing `IngredientRecord`s (with occurrence `count`).
2. **Filtering.** `LearningRules.filter_records` drops records containing conjunctions — *except* when
   the conjunction sits between numbers (`4 i 1/2`) or inside parentheses.
3. **Iterative loop** (`IngredientLearningEngineDefault.learn`):
   - `reduce_records` removes anything already recognizable by current regexes.
   - The **highest-frequency** unprocessed record is selected (maximize coverage per LLM call).
   - The ingredient is parsed by the **LLM ensemble** (`AgentIngredientParser`): N parallel calls →
     majority vote (`choose_proper_parsing`) → retry up to `max_retries`.
   - `RegexOrchestrator` routes each parsed field to its `RegexService`, which **normalizes**
     (Morfeusz), **generates the inflection paradigm**, and either creates a new `RegexEntry` or merges
     variants into an existing stem.
4. Errors are counted and logged per iteration; the loop is resilient to individual failures.

### 2. Normalization & inflection (the NLP core)

- **`PhraseAnalyser`** decomposes a noun phrase into head noun, dependent noun, and related
  adjectives, resolving grammatical ambiguity by intersecting case/gender/number bitsets between
  candidate nouns and their adjectives.
- **Normalizers** reduce each field to a canonical lemma: names → nominative singular (both nouns for
  compounds), adjectives (`unit_size`, `condition`) → nominative singular masculine, units → nominative
  singular.
- **`Inflector`** uses `morfeusz.generate()` to expand the lemma into its paradigm; invariant words
  (e.g. `mango`) are detected and left untouched.
- **`RegexEntry`** compiles the variant set into `\b(?:v1|v2|…)\b` (longest-first, case-insensitive)
  and recompiles when variants are added.

### 3. Recognition — `engine.recognize_ingredients(data)` *(no LLM)*

1. Extract parenthetical `extra`; extract `amount` (`AmountExtractor` — handles digits, fractions, and
   `number + and-conjunction + number` summation).
2. Run each field registry over the cleaned string via a **resolver pipeline**, consuming matched spans
   as it goes, and build a `ResolvedIngredient`.
3. Inputs that can't be fully standardized raise `UnfeasibleStandardisation` and are skipped (logged),
   so a bad row never crashes a batch.

### 4. Categorization & persistence

- `await engine.categorize_registries()` — LLM ensemble assigns each stem to a `Category`.
- `engine.save_registries()` / `save_categories()` / `save()` — persist to the configured backend. The
  file backend groups regexes by category and is intended for **human validation** before promotion.

---

## 🚀 Quickstart

> ⚠️ **API note:** the public API is `EngineConfig(storage=…)`. The verified usage below reflects the
> actual code in `config.py` / `bootstrap.py`.

### Install

```bash
git clone https://github.com/romanroman008/ingredient_regex_engine.git
cd ingredient_regex_engine
python -m pip install -e ".[dev]"     # or: uv sync --extra dev
```

### Configure credentials

```env
# .env
OPENAI_API_KEY=your_api_key_here
```

### Run (file storage backend)

```python
import asyncio
from dotenv import load_dotenv
from regex_engine import EngineConfig, AgentConfig, FileStorageConfig, create_engine

load_dotenv()

async def main():
    config = EngineConfig(
        storage=FileStorageConfig(output_dir="./output"),
        parser=AgentConfig(model="gpt-4o-mini", ensemble_size=5, max_retries=3, timeout=20),
        categorizer=AgentConfig(model="gpt-4o-mini"),
    )
    engine = await create_engine(config)

    await engine.learn(
        """
        2 duże łyżki ciepłego mleka
        1 szklanka wody
        3 jajka
        5 czubatych łyżek śmietany
        """,
        max_iterations=100,
    )

    results = engine.recognize_ingredients(["szklankę ciepłego mleka", "2 jajka"])
    for r in results:
        print(r)

    engine.save()

asyncio.run(main())
```

### Postgres backend

```python
from regex_engine import EngineConfig, DatabaseStorageConfig, create_engine

config = EngineConfig(
    storage=DatabaseStorageConfig(
        database_url="postgresql+psycopg://user:pass@localhost:5432/regex_engine",
        create_schema=True,
    ),
)
```

### Demo (no API key)

```python
from regex_engine import create_demo
engine = create_demo(mapping)   # mapping: dict[str, ParsedIngredient]
```

See `examples/quickstart.ipynb` (needs a key) and `examples/quickstart_demo.ipynb` (offline).

### Tests

```bash
pytest                # unit + integration (spins up Postgres via testcontainers)
uv run pytest
```

The suite has ~**226 test functions across 32 files**, split into `unit/`, `integration/` (real
Postgres, Morfeusz), and `live/` (real LLM) tiers.

---

## 💰 Cost Profile

Measured: learning 100 ingredients with `gpt-4o-mini`, `ensemble_size=5`, `max_retries=3` ≈
**$0.09**, scaling roughly linearly with the number of *distinct* ingredients. Because recognition is
pure regex, per-request runtime cost is **$0**. (Categorization uses the same LLM mechanism, so its
cost profile is comparable to the learning phase.)

---

## 🧩 Public API Surface

```python
from regex_engine import (
    create_engine,          # async: build a production engine from EngineConfig
    create_demo,            # sync: build an offline demo engine
    EngineConfig,
    AgentConfig,
    FileStorageConfig,
    DatabaseStorageConfig,
    IngredientRegexEngine,  # Protocol
    ResolvedIngredient,     # result DTO
)
```

`IngredientRegexEngine` protocol: `learn`, `recognize_ingredients`, `categorize_registries`,
`save_registries`, `save_categories`, `save`, `get_registries`.

---

## 📄 Credits & License

- **Morfeusz2** — morphological analysis of the Polish language.
- **OpenAI models** (via the Agents SDK) — ingredient parsing and categorization.

Released under the **MIT License**.
