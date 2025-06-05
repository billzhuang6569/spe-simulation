# Project Lucidity
*Stanf​ord-Prison-Style LLM Sandbox*  
**Version** 1.1  **Date** 2025-06-05  
**Author** CIO / Bill Zhuang  

---

## 1 Purpose
Build an “AI-prison‐game” in which multiple LLM agents play *prisoners* and *guards* on a grid map.  
A single command such as

```bash
lucidity start --map=default.json --agents=9 --model=gpt-4o

must spin up a full game, stream every turn to a web UI, and persist all data for replay or analysis.

⸻

2 Key Requirements

ID	Requirement	Must
FR-1	Turn Engine – fixed-time loop, AP settlement, Δ-matrix state changes	✔
FR-2	Plugin LLM – default GPT-4o, swappable via OpenRouter key	✔
FR-3	Persona Builder – YAML → prompt w/ max 180 tokens	✔
FR-4	JSON Schema Validator – reject / retry non-JSON outputs	✔
FR-5	World Model – grid map, doors, items, agent stats (HP, HUNGER, ANGER, MORALE, FATIGUE, STRESS)	✔
FR-6	SQLite-WAL Persistence – event log, snapshot replay	✔
FR-7	WebSocket API – push JSON-patch diffs to UI	✔
FR-8	React SPA – 4 panes: Dashboard, Map, Agent Sidebar, Event Stream	✔
FR-9	One-click “Pause / Rewind / Resume”	✔
FR-10	Docker-Compose up boots everything	✔
NFR-1	≥80 % test coverage, GitHub Actions green	✔


⸻

3 System Blueprint

┌─ frontend (React+Canvas) ───────────────────────────┐
│ WS: /stream < JSON Patch for Map + Agents + Log   │
└────────────────────────────────────────────────────┘
                ▲
                │
┌─ game_core (FastAPI) ─ TurnLoop · EventBus · WS Hub ┐
└────────────────────────────────────────────────────┘
       ▲              ▲
       │ RPC          │ async
       ▼              ▼
┌── plugins/llm.py ─────┐     SQLite-WAL (state.db)
└───────────────────────┘


⸻

4 Persona Schema (YAML)

id: P03
major: Psychology
family_background: Working-class, only child
personality:
  introvert: 40
  agreeableness: 65
  neuroticism: 35
motivation: "Earn extra cash; curious about research"
stress_tolerance: 70

The Persona Builder injects only 4 lines (major, background, key traits, motivation) into the LLM system prompt; names are never revealed.

⸻

5 Turn-Loop Contract

Prompt Stub passed to LLM

{
  "system": "You are agent #P03 (prisoner)...",
  "context": { /*  <  40 tokens */ },
  "functions": [/* MOVE, OPEN_DOOR,… */]
}

Expected LLM output (strict)

{
  "name": "MOVE",
  "arguments": { "target": [4,6] }
}

If the reply is not valid JSON or exceeds 200 chars → auto-retry up to 3 times, else skip turn.

⸻

6 Front-End UX

Pane	Key Elements
Dashboard	Turn #, elapsed time, total violent acts, start/stop buttons
Map	16×9 grid, locked doors, item icons, agent avatars
Sidebar	HP bar + radar (ANGER…); inventory; last 3 actions
Event Stream	Virtualized list [T12] G02 ⚡️ hits P03 (-20 HP) with filters

All panes update via a single WebSocket endpoint pushing JSON-patch diffs.

⸻

7 Sprint Plan (1-week Sprints, fully automated by Codex bots)

Sprint	Goal	Assigned Bot(s)	Definition of Done
0	Repo, CI skeleton	DevOps-Bot	gh actions lint & pytest pass
1	TurnLoop + Tile/Agent dataclasses	Backend-Bot	lucidity start --dummy prints 10 events
2	LLM plugin + JSON validator	Backend-Bot, QA-Bot	200-turn fuzz run, 99 % JSON OK
3	SQLite-WAL + replay CLI	Backend-Bot	lucidity replay save001 deterministic
4	WS hub + live MapCanvas	Frontend-Bot	Avatars move in browser (<1 s latency)
5	Sidebar + Event Stream	Frontend-Bot	HP / ANGER bars animate correctly
6	Config Wizard + Persona builder	Frontend-Bot, Backend-Bot	No-code game launch via UI
7	Pause / Rewind / Auto-stop ethics	Backend-Bot	Exhaustion > 90 triggers stop
8	E2E Smoke, docs	QA-Bot, PM-Bot	docker-compose up → UI live in 60 s

Total: 8 weeks (can overlap if bots parallelize).

⸻

8 Deliverables

Artifact	Path
Core engine	/engine/
LLM plugin	/plugins/llm.py
Persona samples	/persona/*.yaml
SPA code	/web/
Integration tests	/tests/e2e/
Docker-compose	/deploy/docker-compose.yml
Docs	/docs/README.md, /docs/PRD.md


⸻

9 Run Commands

# local dev
poetry install
lucidity start --map=default.json --agents=9 --model=gpt-4o

# replay
lucidity replay 2025-06-12T10-45-00

# docker all-in-one
docker-compose up --build


⸻

10 Acceptance Criteria
	•	Game starts with one CLI or one button.
	•	UI shows every turn, dialogue, stat change in real time.
	•	Replay of a saved session reproduces identical event hashes.
	•	≥80 % unit-test coverage; all GitHub Actions checks pass.
