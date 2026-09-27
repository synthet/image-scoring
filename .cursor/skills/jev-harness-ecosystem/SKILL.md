---
name: jev-harness-ecosystem
description: Use when changing agent hooks, Jev harness modes, rule packs, programmable permissions, routing, review bundles, or MCP search rerank across image-scoring-pipeline and image-scoring-gallery; or when the user cites Jev Engineering for Coding Agents.
capability: "Image Scoring Jev harness operator guide"
side_effect_level: local_write
approval_required: false
requires_tools: "image-scoring-pipeline scripts/agent_harness/cli.py; optional jev-rw-systemone for ad-hoc judgments"
output_schema: "Concrete file paths and mode changes"
risk_class: medium
---

# Jev harness (Image Scoring ecosystem)

The **working note** *Jev Engineering for Coding Agents* is adopted in this monorepo layout as **backend-owned harness code** plus hub documentation — not a second harness in `image-scoring`.

## Read first

| Doc | Repo |
|-----|------|
| `image-scoring/docs/guides/JEV_ENGINEERING_ADOPTION.md` | hub — PDF → implementation map |
| `image-scoring-pipeline/docs/technical/JEV_AGENT_HARNESS.md` | backend — modes, hooks, files |
| PDF | `image-scoring/docs/raw/Jev-Engineering-for-Coding-Agents.pdf` |

## When to edit what

| Task | Where |
|------|--------|
| Hook behaviour, rubrics, policy | `image-scoring-pipeline/scripts/agent_harness/` |
| Per-repo pack triggers, route prices | `.agent/jev_harness.json` in backend **and** gallery |
| Rule packs (visibility ladder) | `.cursor/rules/*.mdc` in target app repo → sync to `.claude/` |
| MCP search rerank | backend `config.json` `typesafe.mcp_search_rerank` + `typesafe.enabled` |
| Ad-hoc semantic judgment in chat | `jev-mcp` skill + `jev-rw-systemone` MCP (hub or user-level) |

## Operator CLI (backend)

```bash
cd image-scoring-pipeline
python scripts/agent_harness/cli.py budget
python scripts/agent_harness/cli.py packs
python scripts/agent_harness/cli.py route --task "..." --files path1,path2
python scripts/agent_harness/cli.py bundle --base origin/main
```

Gallery Claude Code hooks call backend `hook.py` with `--repo` when the sibling checkout exists.

## Modes

`JEV_HARNESS_MODE=off|shadow|on` overrides `.agent/jev_harness.json`. **Permission** defaults to **shadow** — flip to `on` only after reviewing `.agent/scratch/jev-harness/decisions.jsonl`.

## Do not

- Put API keys in rules, skills, or MCP JSON (env / `secrets.json` only).
- Use Jev to relax deny/ask policy (harness may only tighten).
- Reimplement harness logic in the hub meta repo — link and change backend instead.
