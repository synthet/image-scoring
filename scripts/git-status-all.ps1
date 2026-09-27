#Requires -Version 5.1
param(
    [string]$ManifestPath = (Join-Path $PSScriptRoot "..\repos.manifest.json")
)

$ErrorActionPreference = "Stop"
$hubRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$manifest = Get-Content -Raw -Path $ManifestPath | ConvertFrom-Json
$parent = $manifest.layout.parentDir
if (-not (Test-Path -LiteralPath $parent)) {
    $parent = (Resolve-Path (Join-Path $hubRoot "..")).Path
}

foreach ($repo in $manifest.repositories) {
    if ($repo.path) {
        $dir = $repo.path
    } elseif ($repo.id -eq "hub") {
        $dir = $hubRoot.Path
    } else {
        $dir = Join-Path $parent $repo.dir
    }
    Write-Host ""
    Write-Host "=== $($repo.dir) ===" -ForegroundColor Cyan
    if (-not (Test-Path -LiteralPath (Join-Path $dir ".git"))) {
        Write-Host "(not a git repo or missing)"
        continue
    }
    Push-Location $dir
    $branch = git branch --show-current 2>$null
    if ($branch) { Write-Host "branch: $branch" }
    git status -sb
    Pop-Location
}
