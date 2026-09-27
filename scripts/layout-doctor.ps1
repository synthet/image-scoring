#Requires -Version 5.1
<#
.SYNOPSIS
  Verify sibling repos listed in repos.manifest.json exist next to the hub.
#>
param(
    [string]$ManifestPath = (Join-Path $PSScriptRoot "..\repos.manifest.json")
)

$ErrorActionPreference = "Stop"
$hubRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$manifest = Get-Content -Raw -Path $ManifestPath | ConvertFrom-Json
$parent = $manifest.layout.parentDir

if (-not (Test-Path -LiteralPath $parent)) {
    Write-Warning "manifest.layout.parentDir not found: $parent (checking relative to hub only)"
    $parent = (Resolve-Path (Join-Path $hubRoot "..")).Path
}

$missing = @()
$present = @()

foreach ($repo in $manifest.repositories) {
    if ($repo.id -eq "hub") { continue }
    $target = if ($repo.path) { $repo.path } else { Join-Path $parent $repo.dir }
    if (Test-Path -LiteralPath $target) {
        $present += $repo.dir
    } else {
        $missing += $repo.dir
    }
}

Write-Host "Hub:    $hubRoot"
Write-Host "Parent: $parent"
Write-Host ""

foreach ($name in $present) {
    Write-Host "[ok]   $name"
}
foreach ($name in $missing) {
    Write-Host "[MISS] $name"
}

if ($manifest.infrastructure) {
    Write-Host ""
    Write-Host "Infrastructure:"
    foreach ($infra in $manifest.infrastructure) {
        $target = if ($infra.path) { $infra.path } else { Join-Path $parent $infra.dir }
        if (Test-Path -LiteralPath $target) {
            Write-Host "[ok]   $($infra.dir)"
        } else {
            Write-Host "[MISS] $($infra.dir)"
            $missing += $infra.dir
        }
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Clone missing repos: .\scripts\clone-siblings.ps1"
    exit 1
}

Write-Host ""
Write-Host "Layout OK."
exit 0
