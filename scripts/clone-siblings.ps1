#Requires -Version 5.1
<#
.SYNOPSIS
  Clone sibling repositories from repos.manifest.json (skips hub and existing dirs).
#>
param(
    [ValidateSet("https", "ssh")]
    [string]$Protocol = "https",
    [string]$ManifestPath = (Join-Path $PSScriptRoot "..\repos.manifest.json")
)

$ErrorActionPreference = "Stop"
$hubRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$manifest = Get-Content -Raw -Path $ManifestPath | ConvertFrom-Json
$parent = $manifest.layout.parentDir

if (-not (Test-Path -LiteralPath $parent)) {
    $parent = (Resolve-Path (Join-Path $hubRoot "..")).Path
    Write-Host "Using parent: $parent"
}

New-Item -ItemType Directory -Force -Path $parent | Out-Null

function Clone-RepoEntry($repo, $parentDir, $Protocol) {
    if (-not $repo.clone) {
        Write-Host "[skip] $($repo.dir) (no clone URLs in manifest)"
        return
    }
    $dest = if ($repo.path) { $repo.path } else { Join-Path $parentDir $repo.dir }
    if (Test-Path -LiteralPath $dest) {
        Write-Host "[exists] $($repo.dir)"
        return
    }
    $url = if ($Protocol -eq "ssh") { $repo.clone.ssh } else { $repo.clone.https }
    Write-Host "[clone] $url -> $dest"
    git clone $url $dest
}

foreach ($repo in $manifest.repositories) {
    if ($repo.id -eq "hub") { continue }
    Clone-RepoEntry $repo $parent $Protocol
}

if ($manifest.infrastructure) {
    Write-Host ""
    Write-Host "Infrastructure:"
    foreach ($infra in $manifest.infrastructure) {
        Clone-RepoEntry $infra $parent $Protocol
    }
}

Write-Host "Done. Run .\scripts\layout-doctor.ps1 to verify."
