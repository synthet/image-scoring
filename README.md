# Image Scoring — meta workspace

Umbrella hub for the **Vexlum Scoring** ecosystem: sibling git repos under one parent folder (`D:\Projects` on this machine). This repo does not ship application runtime code; it holds the **multi-root Cursor/VS Code workspace**, a **repo manifest**, and **cross-repo scripts**.

## Repositories

| Folder | GitHub | Role |
|--------|--------|------|
| **image-scoring** (here) | [synthet/image-scoring](https://github.com/synthet/image-scoring) | Meta hub |
| **image-scoring-pipeline** | [synthet/image-scoring-pipeline](https://github.com/synthet/image-scoring-pipeline) | Vexlum Scoring — pipeline, WebUI, Postgres, MCP `is-be-*` |
| **image-scoring-gallery** | [synthet/image-scoring-gallery](https://github.com/synthet/image-scoring-gallery) | Driftara Gallery — Electron app, MCP `is-ui-*` |
| **image-scoring-mobile** | [synthet/image-scoring-mobile](https://github.com/synthet/image-scoring-mobile) | Mobile Labeler — Expo / React Native offline-first human labeling app |
| **image-scoring-model** | [synthet/image-scoring-model](https://github.com/synthet/image-scoring-model) | `eye-quality` — eye pose / focus scoring |
| **image-scoring-ui** | [synthet/image-scoring-ui](https://github.com/synthet/image-scoring-ui) | `@synthet/image-scoring-design` tokens |
| **image-scoring-skills** | [synthet/image-scoring-skills](https://github.com/synthet/image-scoring-skills) | Editorial / carousel prompts + optional DB MCP |

Machine-readable list: [`repos.manifest.json`](repos.manifest.json). Architecture notes: [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md).

## Clone (hub only)

```bash
git clone https://github.com/synthet/image-scoring.git
# or
git clone git@github.com:synthet/image-scoring.git image-scoring
```

Sibling app repos: `.\scripts\clone-siblings.ps1` (see [`repos.manifest.json`](repos.manifest.json)).

## Quick start

1. **Open the workspace** (recommended): double-click or `cursor image-scoring.code-workspace` from this folder.
2. **Verify layout**:
   ```powershell
   .\scripts\layout-doctor.ps1
   ```
3. **Clone missing siblings** (HTTPS by default):
   ```powershell
   .\scripts\clone-siblings.ps1
   ```
4. **Per-repo setup** — follow each repo’s README (backend Docker/WSL, gallery `npm install`, model `pip install -e ".[dev]"`, etc.).

Gallery API port discovery and skills MCP expect **backend as a sibling** unless you override `config.json` / `environment.json`.

## Scripts

| Script | Purpose |
|--------|---------|
| [`scripts/layout-doctor.ps1`](scripts/layout-doctor.ps1) | Check that expected sibling folders exist |
| [`scripts/clone-siblings.ps1`](scripts/clone-siblings.ps1) | Clone repos from the manifest |
| [`scripts/git-status-all.ps1`](scripts/git-status-all.ps1) | Short `git status` across siblings |
| [`scripts/jev-mcp-integrate.ps1`](scripts/jev-mcp-integrate.ps1) | Wire `jev-mcp` (MCP, skill sync, doctor) |
| [`scripts/llmwiki-sync-ecosystem.ps1`](scripts/llmwiki-sync-ecosystem.ps1) | Ingest OKF bundle → LLM Wiki + render |

## Cursor / agents

Agent scaffold from **[synthet-code-framework](https://github.com/synthet/synthet-code-framework)** (`.\scripts\framework-adopt.ps1`). Evidence wiki: **[synthet-llm-wiki](https://github.com/synthet/synthet-llm-wiki)** in the workspace.

- **[AGENTS.md](AGENTS.md)** — umbrella scope vs sibling repos.
- **[docs/FRAMEWORK_AND_WIKI.md](docs/FRAMEWORK_AND_WIKI.md)** — framework fork policy + `llmwiki-ro-core`.
- **[docs/guides/JEV_ENGINEERING_ADOPTION.md](docs/guides/JEV_ENGINEERING_ADOPTION.md)** — *Jev Engineering for Coding Agents* PDF → backend harness + `jev-mcp`.
- **LLM Wiki OKF bundle** — `synthet-llm-wiki/docs/ecosystems/image-scoring/`; sync: `.\scripts\llmwiki-sync-ecosystem.ps1` ([`docs/llm-wiki/README.md`](docs/llm-wiki/README.md)).
- **[`.cursor/README.md`](.cursor/README.md)** — multi-root MCP (`mcp.example.json`).

Canonical product docs stay in **image-scoring-pipeline** and **image-scoring-gallery**; do not duplicate long setup guides here.
