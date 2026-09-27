#Requires -Version 5.1
<#
.SYNOPSIS
  Wire D:\Projects\jev-mcp into the image-scoring hub (deps, skill sync, Cursor MCP, doctor).

.PARAMETER Workstation
  Also run jev-mcp/scripts/install_jev_mcp_workstation.py (user-level MCP + all TARGET_PROJECTS).
#>
param(
    [string]$JevMcpRoot = "D:\Projects\jev-mcp",
    [switch]$Workstation
)

$ErrorActionPreference = "Stop"
$HubRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$JevMcpRoot = (Resolve-Path -LiteralPath $JevMcpRoot).Path

if (-not (Test-Path (Join-Path $JevMcpRoot "scripts\run_jev_mcp.py"))) {
    Write-Error "jev-mcp checkout not found at $JevMcpRoot (run .\scripts\clone-siblings.ps1 or clone manually)."
}

$envFile = Join-Path $JevMcpRoot ".env"
$envExample = Join-Path $JevMcpRoot "env.example"
if (-not (Test-Path $envFile) -and (Test-Path $envExample)) {
    Copy-Item $envExample $envFile
    Write-Host "Created $envFile — add JEV_TOKEN before using MCP."
}

Write-Host "==> uv sync (jev-mcp)"
Push-Location $JevMcpRoot
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv sync --extra dev
} else {
    Write-Warning "uv not on PATH; skipping sync (install uv or pip install -e '.[dev]' in jev-mcp)."
}
Pop-Location

$canonicalSkill = Join-Path $JevMcpRoot ".claude\skills\jev-mcp\SKILL.md"
$hubClaudeSkill = Join-Path $HubRoot ".claude\skills\jev-mcp\SKILL.md"
if (Test-Path $canonicalSkill) {
    New-Item -ItemType Directory -Force -Path (Split-Path $hubClaudeSkill) | Out-Null
    Copy-Item -LiteralPath $canonicalSkill -Destination $hubClaudeSkill -Force
    Write-Host "Synced canonical skill -> $hubClaudeSkill"
}

Write-Host "==> merge jev-rw-systemone into .cursor/mcp.json"
$examplePath = Join-Path $HubRoot ".cursor\mcp.example.json"
$mcpPath = Join-Path $HubRoot ".cursor\mcp.json"
$example = Get-Content -Raw $examplePath | ConvertFrom-Json
$jevEntry = $example.mcpServers."jev-rw-systemone"
if (-not $jevEntry) {
    Write-Error "jev-rw-systemone missing from .cursor/mcp.example.json"
}
if (Test-Path $mcpPath) {
    $mcp = Get-Content -Raw $mcpPath | ConvertFrom-Json
} else {
    $mcp = [pscustomobject]@{ mcpServers = [pscustomobject]@{} }
}
if (-not $mcp.mcpServers) {
    $mcp | Add-Member -NotePropertyName mcpServers -NotePropertyValue ([pscustomobject]@{})
}
$mcp.mcpServers | Add-Member -NotePropertyName "jev-rw-systemone" -NotePropertyValue $jevEntry -Force
$mcp | ConvertTo-Json -Depth 10 | Set-Content -Path $mcpPath -Encoding utf8
Write-Host "Updated $mcpPath"

Push-Location $HubRoot
Write-Host "==> sync assistant trees (hub)"
python scripts/sync_assistant_trees.py
Pop-Location

if ($Workstation) {
    Write-Host "==> workstation installer (all clients + TARGET_PROJECTS)"
    python (Join-Path $JevMcpRoot "scripts\install_jev_mcp_workstation.py")
}

Write-Host "==> jev-mcp doctor"
Push-Location $JevMcpRoot
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run jev-mcp doctor
} elseif (Get-Command jev-mcp -ErrorAction SilentlyContinue) {
    jev-mcp doctor
} else {
    Write-Warning "Could not run doctor — install jev-mcp CLI first."
}
Pop-Location

Write-Host ""
Write-Host "Done. Reload Cursor MCP. Docs: docs/guides/JEV_MCP_INTEGRATION.md"
