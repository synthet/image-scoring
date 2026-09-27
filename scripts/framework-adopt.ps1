#Requires -Version 5.1
<#
.SYNOPSIS
  Re-merge synthet-code-framework agent scaffolding into the hub (--adopt).
#>
param(
    [string]$FrameworkRoot = "D:\Projects\synthet-code-framework"
)

$ErrorActionPreference = "Stop"
$hub = Resolve-Path (Join-Path $PSScriptRoot "..")

if (-not (Test-Path (Join-Path $FrameworkRoot "bootstrap.py"))) {
    Write-Error "Framework not found: $FrameworkRoot"
}

python (Join-Path $FrameworkRoot "bootstrap.py") `
    --target $hub `
    --name "Image Scoring" `
    --slug image-scoring `
    --desc "Meta workspace hub for the Vexlum Scoring ecosystem (sibling repos, MCP, agents)." `
    --stack generic `
    --mcp-prefix is-hub `
    --repo-url "https://github.com/synthet/image-scoring" `
    --adopt `
    --no-include-ci

Write-Host ""
Write-Host "Re-apply hub-only files if needed: docs/FRAMEWORK_AND_WIKI.md, repos.manifest.json, image-scoring.code-workspace, .cursor/mcp.example.json (multi-root MCP)."
Write-Host "Run: python scripts/sync_assistant_trees.py"
