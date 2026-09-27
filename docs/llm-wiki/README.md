---
type: Documentation Hub
title: LLM Wiki — Image Scoring OKF bundle
description: Canonical comprehensive OKF documentation lives in synthet-llm-wiki; this page points agents to ingest and query paths.
resource: llm-wiki/README.md
tags: [llm-wiki, okf, image-scoring]
timestamp: 2026-09-27T00:00:00Z
okf_version: 0.1
---

# LLM Wiki (Image Scoring)

The **common comprehensive OKF bundle** for this ecosystem is maintained in the evidence wiki product repo, not duplicated here:

**`D:\Projects\synthet-llm-wiki\docs\ecosystems\image-scoring\`**

| Action | Command |
|--------|---------|
| Edit OKF pages | Edit files in that folder; run `okf_lint` in `synthet-llm-wiki` |
| Ingest into SQLite | `cd D:\Projects\synthet-llm-wiki` → `python scripts/ingest_image_scoring_ecosystem.py` |
| From hub | `.\scripts\llmwiki-sync-ecosystem.ps1` |
| Query (reviewed) | MCP `llmwiki-ro-core` — skill `llm-wiki` |

Hub-local summaries (`ECOSYSTEM.md`, `guides/*`) remain for offline/git; **prefer the llm-wiki bundle** for cited cross-repo answers after ingest + review.
