#Requires -Version 5.1
<#
.SYNOPSIS
  Ingest Image Scoring OKF bundle into synthet-llm-wiki and re-render pages.
#>
param(
    [string]$LlmWikiRoot = "D:\Projects\synthet-llm-wiki"
)

$ErrorActionPreference = "Stop"
$LlmWikiRoot = (Resolve-Path -LiteralPath $LlmWikiRoot).Path

Push-Location $LlmWikiRoot
Write-Host "==> OKF lint (image-scoring bundle)"
python scripts/okf_lint.py --profile project docs/ecosystems/image-scoring
Write-Host "==> ingest"
python scripts/ingest_image_scoring_ecosystem.py
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run llmwiki validate
    uv run llmwiki render
} else {
    llmwiki validate
    llmwiki render
}
Pop-Location
Write-Host "Done. Use llmwiki-ro-core search/ask (reviewed claims)."
