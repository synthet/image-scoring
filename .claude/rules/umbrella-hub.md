---
description: Umbrella hub conventions — multi-root workspace, sibling repos, and delegation.
alwaysApply: true
---

# Umbrella hub (`image-scoring`)

This repository is the **meta workspace** for the Vexlum Scoring ecosystem. Product code lives in
sibling folders listed in `repos.manifest.json`.

- Open `image-scoring.code-workspace` for multi-root work (backend, gallery, mobile, model, UI, skills, LLM Wiki).
- Implement features in the **owning** sibling repo; change the hub only for manifest, workspace, agent scaffold, and cross-repo docs.
- **Evidence-bound facts** about the ecosystem: prefer `llmwiki-ro-core` MCP (`synthet-llm-wiki`) over inventing URLs, ports, or schema names.
- **Jev:** per-turn harness lives in `image-scoring-pipeline` (`JEV_AGENT_HARNESS.md`); ad-hoc typed judgments use skill `jev-mcp` + MCP `jev-rw-systemone`. Design note: `docs/raw/Jev-Engineering-for-Coding-Agents.pdf`, map `docs/guides/JEV_ENGINEERING_ADOPTION.md`.
- App repos (`image-scoring-pipeline`, `image-scoring-gallery`, `image-scoring-mobile`, …) use **Cursor-first** agent trees; this hub follows **framework default** (`.claude/` canonical) per `docs/FRAMEWORK_AND_WIKI.md`.
