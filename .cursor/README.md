# Cursor — umbrella workspace

1. Open **[`image-scoring.code-workspace`](../image-scoring.code-workspace)** (hub + product siblings + **synthet-llm-wiki**).
2. Copy **`mcp.example.json`** → **`mcp.json`** (gitignored). Reload MCP after edits.
3. **LLM Wiki:** `llmwiki-ro-core` uses `${workspaceFolder:synthet-llm-wiki}` — run `uv sync --extra dev` in that repo once.
4. **Jev:** run `..\scripts\jev-mcp-integrate.ps1` once; `jev-rw-systemone` → `JEV_ENV_FILE` in `jev-mcp/.env` (paid API). Guide: `docs/guides/JEV_MCP_INTEGRATION.md`.
5. **Product MCP:** build before enabling `is-be-mcp` / `is-ui-mcp`:
   - `image-scoring-pipeline/mcp-server`: `npm install && npm run build`
   - `image-scoring-gallery/mcp-server`: `npm install && npm run build`

Workspace folder names must match `${workspaceFolder:…}` keys in `mcp.example.json`.

See [docs/FRAMEWORK_AND_WIKI.md](../docs/FRAMEWORK_AND_WIKI.md). Backend pair template: [mcp.pair.example.json](https://github.com/synthet/image-scoring-pipeline/blob/main/.cursor/mcp.pair.example.json).
