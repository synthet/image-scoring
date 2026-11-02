---
type: Guide
title: Backend to Pipeline Directory Rename Migration Guide
description: Migration status, locking diagnostics, and execution steps for renaming image-scoring-backend to image-scoring-pipeline.
resource: docs/guides/RENAME_BACKEND_TO_PIPELINE.md
tags: [backend, pipeline, migration, layout]
timestamp: 2026-11-02T14:32:00Z
okf_version: 0.1
---

# Migration Guide: Renaming `image-scoring-backend` to `image-scoring-pipeline`

## 1. Executive Summary

The rename of the primary backend repository from `image-scoring-backend` to `image-scoring-pipeline` is **complete** (2026-11-02):
- All git remotes, manifests, workspaces, design packages, and environment configurations point to `image-scoring-pipeline`.
- `D:\Projects\image-scoring-pipeline` is the real directory. `D:\Projects\image-scoring-backend` is a backward-compatibility NTFS **directory junction** pointing to it.
- All tools, IDEs, and ecosystem scripts resolve paths and pass layout audits (`layout-doctor.ps1` returns `Layout OK`).

Sections 3 and 4 record how the rename was blocked and how it was finished.

---

## 2. Configuration & Ecosystem Status

| Component | Status | Details |
|---|---|---|
| **Git Remote** | Configured | `git@github.com:synthet/image-scoring-pipeline.git` |
| **Workspace Manifest** | Configured | `repos.manifest.json` specifies `dir: image-scoring-pipeline` and `path: D:\Projects\image-scoring-pipeline` |
| **VS Code / Cursor Workspace** | Configured | `image-scoring.code-workspace` uses `image-scoring-pipeline` |
| **Docker Compose / Environment** | Configured | `.env` sets `IMAGE_SCORING_HOST_PROJECT_WIN=D:\Projects\image-scoring-pipeline` while preserving legacy volume prefix `image-scoring-backend` |
| **Layout Doctor** | Passing | `.\scripts\layout-doctor.ps1` confirms `[ok] image-scoring-pipeline` |
| **Physical Directory** | Renamed | `D:\Projects\image-scoring-pipeline` is the real directory (2026-11-02) |
| **Fallback Filesystem Link** | Active | `D:\Projects\image-scoring-backend -> D:\Projects\image-scoring-pipeline` (Junction) |
| **Interim Filesystem Link** | Removed | The earlier `D:\Projects\image-scoring-pipeline -> D:\Projects\image-scoring-backend` junction was replaced by the rename |

---

## 3. Directory Rename Attempt & Diagnostic Findings

### What Occurred
1. The interim junction `D:\Projects\image-scoring-pipeline` was safely unlinked (`cmd /c rmdir`).
2. An atomic directory rename was attempted:
   ```powershell
   Rename-Item -LiteralPath "D:\Projects\image-scoring-backend" -NewName "image-scoring-pipeline"
   ```
3. Windows denied the rename with:
   ```text
   The process cannot access the file because it is being used by another process.
   ```
4. The automated safety rollback immediately restored the junction `D:\Projects\image-scoring-pipeline -> D:\Projects\image-scoring-backend`.

### Root Cause of the Windows File Lock
On Windows, NTFS does not permit renaming or deleting a directory if any running process has:
- Its **Current Working Directory (CWD)** set to that folder or any subfolder.
- An open file/directory handle with non-delete-sharing permissions (e.g. file watchers via `ReadDirectoryChangesW`).

Active processes identified pinning `D:\Projects\image-scoring-backend`:
1. **Terminal Sessions**: Multiple `pwsh.exe` processes running under Warp terminal tabs.
2. **Agent / IDE Workspace**: The active Antigravity CLI / IDE session holding workspace watcher handles.
3. **MCP Servers**: Background `is-be-mcp` (Node `compactIndex.js`) processes.

### Resolution (2026-11-02)
Windows also refuses the rename while any process has its working directory inside the folder, including through the junction. Closing terminals was not enough: five Warp prompt-helper `pwsh.exe` processes were stuck mid-termination and could not be ended. A reboot cleared them. The script then ran successfully, before Docker Desktop, Warp, or any agent session opened the folder.

For any future directory rename on Windows, check process working directories as well as open files, and run the rename right after a reboot.

---

## 4. Completion Script & Procedure

A standalone automation script has been created at:
[`scripts/finish-rename-backend-to-pipeline.ps1`](../../scripts/finish-rename-backend-to-pipeline.ps1)

This script completed the rename on 2026-11-02 and repaired all 5 linked worktrees. Running it again reports that the rename is already done.

### Execution Steps

1. **Close active terminal tabs** in Warp (or any command prompt) whose working directory is in `image-scoring-backend`.
2. **Close IDE / editor windows** or exit agent sessions having `image-scoring-backend` open as a root workspace.
3. Open a clean PowerShell window (outside of `image-scoring-backend`, e.g. at `D:\Projects\image-scoring`) and run:
   ```powershell
   powershell -File D:\Projects\image-scoring\scripts\finish-rename-backend-to-pipeline.ps1
   ```

### Script Actions:
- Verifies directory integrity and unlinks the interim junction without touching target files.
- Renames `D:\Projects\image-scoring-backend` to `D:\Projects\image-scoring-pipeline`.
- Re-creates a backward-compatibility fallback junction (`D:\Projects\image-scoring-backend -> D:\Projects\image-scoring-pipeline`) so any legacy references or bookmarks never break.
- Updates git worktree pointers (e.g. `isb-wt-549`) and runs `git worktree repair`.
- Runs `layout-doctor.ps1` to verify workspace consistency.
