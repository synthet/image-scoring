---
type: Guide
title: Jev engineering adoption (coding agents)
description: Maps the Jev Engineering working note to Image Scoring harness and MCP wiring.
resource: guides/JEV_ENGINEERING_ADOPTION.md
tags: [docs, jev, agents, harness, typesafe]
timestamp: 2026-09-27T00:00:00Z
okf_version: 0.1
---

# Jev engineering adoption

**Source (canonical in this repo):** [`docs/raw/Jev-Engineering-for-Coding-Agents.pdf`](../raw/Jev-Engineering-for-Coding-Agents.pdf)  
**Text extract (searchable):** [`docs/raw/jev-engineering-for-coding-agents.extracted.txt`](../raw/jev-engineering-for-coding-agents.extracted.txt)  
**Working note:** independent synthesis of TypeSafe design notes (September 2026); not an official TypeSafe publication.

## Thesis (one paragraph)

Coding agents are a loop; **leverage is what the harness feeds each turn**. Jev is the **decision layer** beside frontier models: structured state + a narrow question → typed **choice**, **score**, or **noul** with probabilities. The harness validates and branches without parsing prose. Image Scoring implements much of this in **image-scoring-pipeline** (hooks, packs, policy, MCP search rerank); the hub documents cross-repo adoption and wires **jev-mcp** for ad-hoc judgments in the umbrella workspace.

## PDF concepts → where we implement

| Jev decision (PDF Table I) | Idea | Image Scoring implementation |
|----------------------------|------|------------------------------|
| Context visibility | hide / short / full per chunk | `harness.context.visibility`; rule packs in `.cursor/rules/*.mdc` → Claude hooks (`UserPromptSubmit`) |
| Cache reuse | cost-aware rebuild vs prefix | Design target; not fully automated — visibility ladder reduces re-sent text |
| Routing | priced subtasks, small briefs | `scripts/agent_harness/cli.py route`; `/decompose`, `autonomous-run-contract` |
| Tool pick | ranked intent → tool | `is-be-mcp` / `is-ui-mcp` **search + dispatch**; optional `harness.tool.pick` rerank |
| Permissions | allow / ask / deny | `policy.check_command`, `PreToolUse(Bash)`, script body inspection |
| Security / sensitivity | route by file trust | `harness.review.sensitivity` on external reviewer MCP; restricted globs |
| Subgoal dedup | never launch duplicate work | `cli.py subgoal add` + `harness.subgoal.duplicate` |
| Shared retrieval | one bundle, many read-only reviewers | `cli.py bundle` → `.agent-runs/bundle-*.md` |
| Tiered tools | snippets first, schema on demand | MCP compact index; skills with short descriptions |
| Conditional instructions | AGENTS/rules per area | Cursor `globs` + Jev pack ladder; footguns packs per domain |

**Operator doc (detail):** `image-scoring-pipeline/docs/technical/JEV_AGENT_HARNESS.md`  
**Gallery:** hooks delegate to backend `scripts/agent_harness/hook.py` with `--repo`.

## Hub agent assets

| Asset | Path |
|-------|------|
| MCP judgments (interactive) | Skill `jev-mcp`; MCP `jev-rw-systemone` in `.cursor/mcp.example.json` |
| When to use harness vs MCP | Skill `jev-harness-ecosystem` |
| Umbrella rule | `.claude/rules/umbrella-hub.md` (Jev + wiki pointers) |

## MCP setup (workstation)

1. Checkout **`jev-mcp`** at `D:\Projects\jev-mcp` (in workspace as `jev-mcp`).
2. `cp env.example .env` and set `JEV_TOKEN` (or `TYPESAFE_API_KEY`).
3. Optional installer: `python D:\Projects\jev-mcp\scripts\install_jev_mcp_workstation.py`
4. Hub: copy `.cursor/mcp.example.json` → `.cursor/mcp.json`; reload MCP.

**Paid API:** every `jev_*` tool spends quota. Batch with `jev_system_one`. Harness hooks use the same pin (`jev-1.13.0`) with session budget and cache — see backend `.agent/jev_harness.json`.

## Principles (from PDF + backend harness)

1. **Deterministic first, Jev second** — cheap rules settle clear cases.
2. **Fail safe** — no key / timeout → deterministic behaviour; hooks exit 0 on error where required.
3. **Jev only tightens** — permissions and review sensitivity may escalate, never relax.
4. **Redact before Jev** — no secrets, tokens, or raw restricted file bodies in state.
5. **Do not use Jev as a chat model** — narrow semantic questions only; code owns arithmetic and I/O.

## Optional: ingest into LLM Wiki

To query the note via `llmwiki-ro-core` with citations:

```bash
llmwiki --root "D:\Projects\synthet-llm-wiki" ingest "D:\Projects\image-scoring\docs\raw\Jev-Engineering-for-Coding-Agents.pdf" --title "Jev Engineering for Coding Agents (working note)"
llmwiki --root "D:\Projects\synthet-llm-wiki" validate
llmwiki --root "D:\Projects\synthet-llm-wiki" render
```

Then human-review promoted claims per wiki workflow (`docs/mcp-and-editors.md` in synthet-llm-wiki).

## Related

- [`docs/FRAMEWORK_AND_WIKI.md`](../FRAMEWORK_AND_WIKI.md) — scaffold + evidence wiki
- [`docs/ECOSYSTEM.md`](../ECOSYSTEM.md) — repo map
- Backend MCP: `docs/technical/MCP_SEARCH_DISPATCH.md`
