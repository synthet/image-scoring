---
type: Guide
title: Submodule Deduplication & Junction Options (Superseded)
description: Historical evaluation of deduplicating sibling workspaces and nested submodules. Superseded by adopting pure sibling checkouts in D:\Projects without nested submodules.
resource: guides/SUBMODULE_DEDUPLICATION_OPTIONS.md
tags: [git, submodules, windows, junctions, symlinks, deduplication, historical]
timestamp: 2026-10-10T16:55:00Z
okf_version: 0.1
---

# Submodule Deduplication & NTFS Junction Strategy (Historical / Superseded)

> [!NOTE]
> **Status: Superseded.** Nested Git submodules within `image-scoring` have been decommissioned.
> All repositories reside directly as sibling checkouts under `D:\Projects\<repo>` and are managed via [`image-scoring.code-workspace`](../../image-scoring.code-workspace), [`repos.manifest.json`](../../repos.manifest.json), and [`AGENTS.md`](../../AGENTS.md).

## Context & Problem Statement

The `image-scoring` repository previously registered Git submodules for all components (`image-scoring-pipeline`, `image-scoring-gallery`, `image-scoring-mobile`, `image-scoring-model`, `image-scoring-ui`, `image-scoring-skills`).

On the local Windows development machine, repositories have historically resided as **siblings** in `D:\Projects\<repo>` to support relative path discovery (e.g. `../image-scoring-pipeline` by MCP servers, gallery lock files, and local packages).

When Git submodules were added to `D:\Projects\image-scoring`, Git created nested working copies under `D:\Projects\image-scoring\<repo>`, creating duplicate, stale checkouts.

---

## Current Measured Overhead (Baseline)

An analysis was performed across all six component checkouts to measure disk usage:

| Subproject | Sibling Folder (`D:\Projects\...`) | Nested Submodule (`image-scoring\...`) |
|---|---|---|
| **`image-scoring-pipeline`** | **21.86 GB** (Docker, `.venv`, test DB, data) | **98.6 MB** (Source only) |
| **`image-scoring-gallery`** | **1.09 GB** (`node_modules`, builds) | **9.0 MB** (Source only) |
| **`image-scoring-mobile`** | **458 MB** (`node_modules`, cache) | **1.1 MB** (Source only) |
| **`image-scoring-model`** | **1.39 GB** (`.venv`, cached weights) | **0.6 MB** (Source only) |
| **`image-scoring-skills`** | **255 MB** | **1.1 MB** (Source only) |
| **`image-scoring-ui`** | **25.6 MB** | **0.1 MB** (Source only) |
| **TOTAL** | **~25.1 GB** | **~110.5 MB** |

---

## Resolution: Adoption of Flat Sibling Layout

Rather than consolidating into nested submodules with reverse junctions, the ecosystem decommissioned the nested submodules completely. Sibling repositories under `D:\Projects` remain the single source of truth for active development.
