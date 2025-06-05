# Project Lucidity

An experimental "AI-prison-game" where large language model (LLM) agents play prisoners and guards on a grid-based map. The goal is to simulate interactions and events in a turn-based environment, persist them for replay, and stream updates to a web interface.

See [PRD.md](PRD.md) for the detailed product requirements and system design.

## Installation

Use [Poetry](https://python-poetry.org/) for dependency management:

```bash
poetry install
```

## Usage

Start a new game with the default map and GPT-4o as the LLM model:

```bash
lucidity start --map=default.json --agents=9 --model=gpt-4o --log session.db
```

Replay a saved session:

```bash
lucidity replay session.db
```

Replay and stream over WebSocket:

```bash
lucidity replay session.db --ws
```

For an all-in-one setup via Docker:

```bash
docker-compose up --build
```

---

This repository is under active development. Refer to the PRD for the sprint plan, acceptance criteria, and overall vision for the project.

