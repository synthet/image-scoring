---
type: Guide
title: jev-mcp integration (hub)
description: Install, MCP wiring, and workstation bootstrap for D:\Projects\jev-mcp.
resource: guides/JEV_MCP_INTEGRATION.md
tags: [docs, jev, mcp, typesafe]
timestamp: 2026-09-27T00:00:00Z
okf_version: 0.1
---

# jev-mcp integration

Checkout: **`D:\Projects\jev-mcp`** (workspace folder `jev-mcp`, MCP key **`jev-rw-systemone`**).

## One-shot (hub)

```powershell
cd D:\Projects\image-scoring
.\scripts\jev-mcp-integrate.ps1
```

This:

1. `uv sync --extra dev` in `jev-mcp`
2. Creates `jev-mcp/.env` from `env.example` if missing (**set `JEV_TOKEN`**)
3. Copies the canonical **`jev-mcp`** skill into hub `.claude/skills/`
4. Merges `jev-rw-systemone` into gitignored `.cursor/mcp.json`
5. Runs `python scripts/sync_assistant_trees.py` in the hub
6. Runs `jev-mcp doctor` (no API spend)

Reload MCP in Cursor after integration.

## Workstation-wide (optional)

Registers the same server in user-level Cursor/Claude/Codex/Gemini configs and refreshes the
`jev-mcp` skill in all `TARGET_PROJECTS` (includes **`image-scoring`** and app siblings):

```powershell
.\scripts\jev-mcp-integrate.ps1 -Workstation
```

Or from the jev-mcp repo:

```bash
cd D:\Projects\jev-mcp
python scripts/install_jev_mcp_workstation.py
```

Secrets stay in **`jev-mcp/.env`** via `JEV_ENV_FILE` — not written into JSON/TOML.

## MCP shape (multi-root Cursor)

From [`.cursor/mcp.example.json`](../../.cursor/mcp.example.json):

- **Command:** `uv run --project <jev-mcp> python scripts/run_jev_mcp.py`
- **Env:** `JEV_ENV_FILE` → `jev-mcp/.env`, `JEV_MODEL=jev-1.13.0`
- **Tools:** `jev_choice`, `jev_score`, `jev_noul`, `jev_system_one` (paid API per call)

Open **`image-scoring.code-workspace`** so `${workspaceFolder:jev-mcp}` resolves.

## Clone if missing

```powershell
.\scripts\clone-siblings.ps1   # product repos
git clone https://github.com/synthet/jev-mcp.git D:\Projects\jev-mcp
```

(`repos.manifest.json` → `infrastructure[].jev-mcp` includes clone URLs.)

## Relation to backend harness

| Layer | Repo | Role |
|-------|------|------|
| **Hooks / packs / policy** | `image-scoring-backend` | Per-turn Jev via `scripts/agent_harness/` |
| **Interactive MCP** | `jev-mcp` | Ad-hoc judgments in chat |
| **Design note** | hub `docs/raw/Jev-Engineering-for-Coding-Agents.pdf` | [`JEV_ENGINEERING_ADOPTION.md`](JEV_ENGINEERING_ADOPTION.md) |

Canonical server docs: `jev-mcp/AGENTS.md`, `jev-mcp/README.md`.
