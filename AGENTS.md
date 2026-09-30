# AI agents — image-scoring umbrella

<!-- BEGIN SYNTHET-CODE-FRAMEWORK -->
## Authoring & skill source of truth

- **Canonical** assets are authored under `.claude/` (+ `.agent/`).
- The **`.cursor/`** tree and Codex-native **`.agents/skills/`** + **`.codex/agents/`**
  trees are **generated** by `python scripts/sync_assistant_trees.py` — do not hand-edit
  generated files.
- Install shared common-skills **globally** (`~/.agents/skills`). An in-repo common-skills
  install into `.agents/skills` is wiped the next time assistant trees are synced.

## Commands

```bash
python scripts/sync_assistant_trees.py --check
python scripts/okf_lint.py --profile project docs
python scripts/ci/check_agent_frontmatter.py
python scripts/ci/check_secrets.py
python scripts/ci/check_private_docs_not_tracked.py
.\scripts\layout-doctor.ps1
```

See [`.agent/SAFETY.md`](.agent/SAFETY.md), [`docs/ai-workflow/README.md`](docs/ai-workflow/README.md), and [`docs/FRAMEWORK_AND_WIKI.md`](docs/FRAMEWORK_AND_WIKI.md).

## Upstream + evidence wiki

| System | Path | Use |
|--------|------|-----|
| [synthet-code-framework](https://github.com/synthet/synthet-code-framework) | `D:\Projects\synthet-code-framework` | Refresh hub scaffold: `.\scripts\framework-adopt.ps1` |
| [synthet-llm-wiki](https://github.com/synthet/synthet-llm-wiki) | `D:\Projects\synthet-llm-wiki` | `llmwiki-ro-core` MCP; OKF bundle `docs/ecosystems/image-scoring/`; sync `.\scripts\llmwiki-sync-ecosystem.ps1` |
| Jev Engineering note + harness | PDF in hub `docs/raw/`; harness in `image-scoring-pipeline` | [`JEV_ENGINEERING_ADOPTION.md`](docs/guides/JEV_ENGINEERING_ADOPTION.md), [`JEV_MCP_INTEGRATION.md`](docs/guides/JEV_MCP_INTEGRATION.md); `.\scripts\jev-mcp-integrate.ps1`; MCP `jev-rw-systemone` |

App siblings remain **Cursor-first** forks; see `image-scoring-pipeline/docs/raw/framework-adoption-port-manifest.md`.

<!-- END SYNTHET-CODE-FRAMEWORK -->


You are in the **meta hub** (`image-scoring`). Application code, tests, and MCP servers live in **sibling repositories**, not in this folder.

## Layout contract

- **Sibling layout:** `image-scoring`, `image-scoring-pipeline`, `image-scoring-gallery`, `image-scoring-mobile`, `image-scoring-model`, `image-scoring-ui`, and `image-scoring-skills` share the same parent directory (see [`repos.manifest.json`](repos.manifest.json)).
- **Open workspace:** [`image-scoring.code-workspace`](image-scoring.code-workspace) — folder names must match `${workspaceFolder:…}` keys in [`.cursor/mcp.example.json`](.cursor/mcp.example.json).
- **Verify:** `.\scripts\layout-doctor.ps1` from the hub root.

## Where to work

| Task | Repo | Entry docs |
|------|------|------------|
| Pipeline, scoring, Postgres, Gradio, doctor | `image-scoring-pipeline` | `README.md`, `AGENTS.md`, `docs/DIAGNOSTICS.md` |
| Electron gallery, `npm run doctor` | `image-scoring-gallery` | `README.md`, `docs/DEVELOPMENT.md` |
| Mobile labeler (Expo / React Native) | `image-scoring-mobile` | `README.md`, `AGENTS.md` |
| Eye-quality model, training, API contract | `image-scoring-model` | `README.md`, `docs/guides/BACKEND_INTEGRATION.md` |
| Design tokens, `npm run build` before consumers | `image-scoring-ui` | `README.md` |
| Editorial `/review`, `/carousel`, imgscore MCP | `image-scoring-skills` | `AGENTS.md`, `docs/image-scoring-db.md` |
| Cross-repo workspace only | `image-scoring` (here) | This file, `docs/ECOSYSTEM.md` |

**Rule:** Implement features in the owning repo. Update this hub only for manifest, workspace, shared scripts, or ecosystem docs — not for backend/gallery logic.

## MCP (multi-root)

- Backend template: `image-scoring-pipeline/.cursor/mcp.pair.example.json`
- Hub copy (same semantics): [`.cursor/mcp.example.json`](.cursor/mcp.example.json) → copy to `.cursor/mcp.json` (gitignored) after building both `mcp-server` packages.
- **User** `~/.cursor/mcp.json`: cross-repo tools only — not `is-be-*` / `is-ui-*` (see backend `AGENTS.md`).

## PR / hygiene

- Backend: ruff + pytest subsets per `image-scoring-pipeline/AGENTS.md`
- Gallery: lint, `test:run`, tsc per `image-scoring-gallery/AGENTS.md`
- Mobile: expo lint + tsc per `image-scoring-mobile/AGENTS.md`
- Hub: no runtime tests; keep manifest and scripts in sync when adding a repo

## Infrastructure siblings

In the default workspace: **`synthet-llm-wiki`** (`llmwiki-ro-core`). Upstream scaffold: **`synthet-code-framework`** (not in workspace; adopt via script). Optional: `subagent-orchestrator` — see `optionalSiblings` in [`repos.manifest.json`](repos.manifest.json).
