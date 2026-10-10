---
type: Guide
title: Submodule Deduplication & Junction Options
description: Architectural evaluation of deduplicating sibling workspaces and nested submodules using NTFS directory junctions on Windows.
resource: guides/SUBMODULE_DEDUPLICATION_OPTIONS.md
tags: [git, submodules, windows, junctions, symlinks, deduplication]
timestamp: 2026-10-10T16:55:00Z
okf_version: 0.1
---

# Submodule Deduplication & NTFS Junction Strategy

## Context & Problem Statement

The `image-scoring` repository serves as the umbrella/meta workspace on GitHub with registered Git submodules for all components (`image-scoring-pipeline`, `image-scoring-gallery`, `image-scoring-mobile`, `image-scoring-model`, `image-scoring-ui`, `image-scoring-skills`).

On the local Windows development machine (`ZEPHYR`), repositories have historically resided as **siblings** in `D:\Projects\<repo>` to support relative path discovery (e.g. `../image-scoring-pipeline` by MCP servers, gallery lock files, and local packages).

When Git submodules were added to `D:\Projects\image-scoring`, Git created nested working copies under `D:\Projects\image-scoring\<repo>`.

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

Because `--reference` was used during submodule creation, Git object stores are shared. Heavy development assets (`node_modules`, `.venv`, Docker caches, model weights) are **not duplicated**. The total overhead of maintaining both is only **~110 MB**.

---

## Future Deduplication Option: NTFS Directory Junctions

If full physical deduplication (0 bytes duplicate) becomes desired in the future, the recommended method on Windows is **NTFS Directory Junctions** (`mklink /J`).

### Why Junctions instead of Symlinks (`mklink /D`)?
* **No Administrator Required:** Junctions do not require Windows Developer Mode or Administrator privileges.
* **Transparent Resolution:** Python, Node.js, Vite, and Electron resolve junctions transparently as native directories.
* **No Git Mode Confusion:** Unlike symlinks (which Git tracks as `120000` text pointers), junctions operate purely at the NTFS filesystem level outside Git tracking.

---

### Step-by-Step Migration Plan (Future Execution)

#### Phase 1: Preparation
1. Stop running processes (Docker daemon, Electron gallery, Python MCP servers, active VS Code/Cursor windows).
2. Ensure working trees in both sibling and submodule checkouts are clean (`git status`).

#### Phase 2: Consolidate Canonical Checkouts Inside `image-scoring`
Move the full working directories (with their `.venv`, `node_modules`, and local configs) into the `image-scoring` tree:
```powershell
# Example for each subproject:
Move-Item "D:\Projects\image-scoring-pipeline\*" "D:\Projects\image-scoring\image-scoring-pipeline\" -Force
# Remove the empty sibling folder
Remove-Item "D:\Projects\image-scoring-pipeline" -Recurse -Force
```

#### Phase 3: Create NTFS Junctions at `D:\Projects`
Recreate the sibling paths as junctions pointing into the submodule directories:
```cmd
mklink /J "D:\Projects\image-scoring-pipeline" "D:\Projects\image-scoring\image-scoring-pipeline"
mklink /J "D:\Projects\image-scoring-gallery"  "D:\Projects\image-scoring\image-scoring-gallery"
mklink /J "D:\Projects\image-scoring-mobile"   "D:\Projects\image-scoring\image-scoring-mobile"
mklink /J "D:\Projects\image-scoring-model"    "D:\Projects\image-scoring\image-scoring-model"
mklink /J "D:\Projects\image-scoring-skills"   "D:\Projects\image-scoring\image-scoring-skills"
mklink /J "D:\Projects\image-scoring-ui"       "D:\Projects\image-scoring\image-scoring-ui"
```

### Result & Benefits
1. **Zero Duplicate Bytes:** The source code, node_modules, and virtualenvs exist in exactly one location on disk.
2. **Backward Compatibility:** All existing tools, Docker host paths (`IMAGE_SCORING_HOST_PROJECT_WIN=D:\Projects\image-scoring-pipeline`), scripts (`.\scripts\layout-doctor.ps1`), and relative imports (`../image-scoring-pipeline`) continue to work transparently.
3. **Native Git Submodule Status:** Inside `image-scoring`, Git natively tracks the submodules and allows `git submodule update --remote` to bump pointers.

---

### Rollback Procedure
If junctions cause unexpected path resolution issues:
```cmd
# Removing an NTFS junction does NOT delete target files:
rmdir "D:\Projects\image-scoring-pipeline"
# Then move the folder back:
move "D:\Projects\image-scoring\image-scoring-pipeline" "D:\Projects\image-scoring-pipeline"
```
