---
type: Guide
title: Backend to Pipeline Directory Rename Migration Guide
description: Migration status, locking diagnostics, and execution steps for renaming image-scoring-backend to image-scoring-pipeline.
resource: docs/guides/RENAME_BACKEND_TO_PIPELINE.md
tags: [backend, pipeline, migration, layout]
timestamp: 2026-10-10T16:08:00Z
okf_version: 0.1
---

# Migration Guide: Renaming `image-scoring-backend` to `image-scoring-pipeline`

## 1. Executive Summary

The transition of the primary backend repository from `image-scoring-backend` to `image-scoring-pipeline` is **fully configured and functional**:
- All git remotes, manifests, workspaces, design packages, and environment configurations point to `image-scoring-pipeline`.
- `D:\Projects\image-scoring-pipeline` currently exists as an NTFS **directory junction** pointing to `D:\Projects\image-scoring-backend`.
- All tools, IDEs, and ecosystem scripts resolve paths and pass layout audits (`layout-doctor.ps1` returns `Layout OK`).

Completing the final physical directory rename on disk requires releasing open handles in Windows before executing the rename script.

---

## 2. Configuration & Ecosystem Status

| Component | Status | Details |
|---|---|---|
| **Git Remote** | Configured | `git@github.com:synthet/image-scoring-pipeline.git` |
| **Workspace Manifest** | Configured | `repos.manifest.json` specifies `dir: image-scoring-pipeline` and `path: D:\Projects\image-scoring-pipeline` |
| **VS Code / Cursor Workspace** | Configured | `image-scoring.code-workspace` uses `image-scoring-pipeline` |
| **Docker Compose / Environment** | Configured | `.env` sets `IMAGE_SCORING_HOST_PROJECT_WIN=D:\Projects\image-scoring-pipeline` while preserving legacy volume prefix `image-scoring-backend` |
| **Layout Doctor** | Passing | `.\scripts\layout-doctor.ps1` confirms `[ok] image-scoring-pipeline` |
| **Interim Filesystem Link** | Active | `D:\Projects\image-scoring-pipeline -> D:\Projects\image-scoring-backend` (Junction) |

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

---

## 4. Completion Script & Procedure

A standalone automation script has been created at:
[`scripts/finish-rename-backend-to-pipeline.ps1`](../../scripts/finish-rename-backend-to-pipeline.ps1)

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
