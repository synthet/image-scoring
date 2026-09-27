---
type: Guide
title: Framework and LLM Wiki integration
description: How the hub adopts synthet-code-framework and wires synthet-llm-wiki MCP.
resource: FRAMEWORK_AND_WIKI.md
tags: [docs, agents, llm-wiki]
timestamp: 2026-09-27T00:00:00Z
okf_version: 0.1
---

# synthet-code-framework + synthet-llm-wiki

How the umbrella hub relates to upstream agent scaffolding and the shared evidence wiki.

## synthet-code-framework (upstream scaffold)

| Item | Location on disk | Role |
|------|------------------|------|
| Upstream repo | `D:\Projects\synthet-code-framework` | Generic agent SDLC, skills, `.agent/` governance |
| This hub | `D:\Projects\image-scoring` | **Adopted** scaffold + ecosystem manifest/workspace |

**Bootstrap / refresh** (merge agent assets without overwriting hub `README.md` / product docs):

```powershell
.\scripts\framework-adopt.ps1
# or manually:
python D:\Projects\synthet-code-framework\bootstrap.py `
  --target D:\Projects\image-scoring `
  --name "Image Scoring" --slug image-scoring `
  --desc "Meta workspace hub for the Vexlum Scoring ecosystem." `
  --stack generic --mcp-prefix is-hub `
  --repo-url https://github.com/synthet/image-scoring `
  --adopt --no-include-ci
```

After editing `.claude/` assets:

```bash
python scripts/sync_assistant_trees.py
python scripts/sync_assistant_trees.py --check   # CI
```

### Fork policy vs app repos

| Repo class | Agent SOT | Notes |
|------------|-----------|-------|
| **Hub** (`image-scoring`) | `.claude/` → `.cursor/` (framework default) | SDLC commands, safety, memory; no product runtime |
| **Backend / gallery / …** | `.cursor/` → `.claude/` (domain fork) | See `image-scoring-pipeline/docs/raw/framework-adoption-port-manifest.md` |

Cherry-pick generic improvements from framework into app repos; never blind-merge domain MCP rules or pipeline docs.

## synthet-llm-wiki (shared evidence)

| Item | Location | Role |
|------|----------|------|
| Wiki product | `D:\Projects\synthet-llm-wiki` | SQLite + reviewed claims; `llmwiki` CLI + MCP |
| MCP key | `llmwiki-ro-core` | Read/search in Cursor (copy hub `.cursor/mcp.example.json` → `.cursor/mcp.json`) |

The hub workspace includes **`synthet-llm-wiki`** so `${workspaceFolder:synthet-llm-wiki}` resolves in MCP config.

**Agent skill:** `.claude/skills/llm-wiki/SKILL.md` (mirrored to `.cursor/skills/` after sync).

**When to use wiki vs repo docs**

| Question type | Prefer |
|---------------|--------|
| Shipped API, schema, ports, canonical names | Repo `docs/CANONICAL_SOURCES.md` + wiki **after** ingest |
| Cross-repo history, reviewed decisions, compiled notes | `llmwiki-ro-core` search/ask |
| Live debugging, doctor output | Repo `scripts/doctor.py` / MCP `is-be-*` / `is-ui-*` |

Install wiki once per machine (`uv sync --extra dev` in `synthet-llm-wiki`). Launcher:
`uv run --project D:\Projects\synthet-llm-wiki python scripts/run_llmwiki_mcp.py`.

## Jev engineering (coding agents)

| Item | Location |
|------|----------|
| Working note PDF | [`docs/raw/Jev-Engineering-for-Coding-Agents.pdf`](raw/Jev-Engineering-for-Coding-Agents.pdf) |
| Adoption map | [`docs/guides/JEV_ENGINEERING_ADOPTION.md`](guides/JEV_ENGINEERING_ADOPTION.md) |
| Live harness | `image-scoring-pipeline/docs/technical/JEV_AGENT_HARNESS.md` |
| MCP judgments | `jev-mcp` workspace folder + `jev-rw-systemone` in `.cursor/mcp.example.json` |

Skills: `jev-harness-ecosystem` (where to edit hooks/packs), `jev-mcp` (interactive System One calls).

**Setup:** `.\scripts\jev-mcp-integrate.ps1` — see [`docs/guides/JEV_MCP_INTEGRATION.md`](guides/JEV_MCP_INTEGRATION.md).

## Image Scoring OKF bundle (LLM Wiki)

Comprehensive cross-repo docs: **`synthet-llm-wiki/docs/ecosystems/image-scoring/`**. Refresh evidence store: `.\scripts\llmwiki-sync-ecosystem.ps1` ([`docs/llm-wiki/README.md`](llm-wiki/README.md)).
