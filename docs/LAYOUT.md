---
type: Guide
title: Folder layout
description: Expected sibling directory layout for the Image Scoring workspace.
resource: LAYOUT.md
tags: [docs, layout]
timestamp: 2026-09-27T00:00:00Z
okf_version: 0.1
---

# Folder layout

## Expected tree

```
D:\Projects\image-scoring              # hub (meta)
D:\Projects\image-scoring-gallery
D:\Projects\image-scoring-mobile
D:\Projects\image-scoring-model
D:\Projects\image-scoring-skills
D:\Projects\image-scoring-ui
D:\Projects\image-scoring-pipeline
```

Canonical paths are also in [`repos.manifest.json`](../repos.manifest.json) (`path` per repo). On another machine, update those paths or rely on sibling `dir` + `layout.parentDir`.

## Why siblings matter

- **Gallery** discovers backend API port via sibling `webui.lock` unless `api.url` / `api.port` is set.
- **Mobile** leases batches and flushes annotations to the labeling hub / backend.
- **Skills** MCP launchers assume `../image-scoring-pipeline`.
- **UI package** local dev uses `file:../image-scoring-ui` from backend and gallery `package.json`.
- **Model** integration docs use `pip install -e /path/to/image-scoring-model`.

## Workspace vs single-folder open

| Open mode | Best for |
|-----------|----------|
| `image-scoring.code-workspace` | Cross-repo refactors, paired MCP, agent tasks spanning backend + gallery |
| Single repo root | Focused PRs, repo-native slash commands and CI |

The hub repo is safe to open alone for manifest/script edits; it is not sufficient for running the full stack.
