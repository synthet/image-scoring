# Changelog

All notable changes to the image-scoring hub are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the hub uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.3.0] — 2026-11-01

### Changed

- Sibling layout is now the only layout: the nested `image-scoring-*` submodules are removed, and
  sibling repositories live next to the hub under `D:\Projects` (`repos.manifest.json`,
  `docs/LAYOUT.md`).
- `okf_lint.py` skips the git-ignored `docs/_local/` folder by default, so the documented docs
  lint passes locally.
- The frontmatter checker skips the metadata and link checks for generated
  `framework-<command>` and `project-rule-<rule>` skill aliases.

### Added

- Kestrel registered as a local sibling in the manifest, README and workspace.
- `llmwiki-ro-core` MCP server for Codex; explicit transport types in `.mcp.json`.
- Shared library skills, a skill-local harness runtime, and the generated framework command
  aliases, with their Cursor and Codex copies; Antigravity agent and rule copies under `.agents/`.
- Pipeline rename guide and completion script (`scripts/finish-rename-backend-to-pipeline.ps1`),
  which repairs every linked worktree.
- Reports: the 2026-10-23 architecture review and focus-evidence plan, the model, pipeline and
  skills synergy report, Nikon AF validation and container verification receipts, the outstanding
  work inventory and the plan execution results.

### Fixed

- The assistant-tree sync no longer copies Python bytecode.
- Missing frontmatter on hub docs and rules, and index links to drafts that were never committed.

## [0.2.0] — 2026-09-27

- Initial meta workspace for the Vexlum Scoring ecosystem.
