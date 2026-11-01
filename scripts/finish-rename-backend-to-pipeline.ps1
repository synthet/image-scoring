#Requires -Version 5.1
<#
.SYNOPSIS
  Completes renaming D:\Projects\image-scoring-backend to D:\Projects\image-scoring-pipeline.
.DESCRIPTION
  Safely unlinks the interim junction, renames the directory, re-creates a backward-compatibility
  fallback junction (image-scoring-backend -> image-scoring-pipeline), repairs any linked git
  worktrees, and runs layout-doctor.ps1.
#>
param(
    [string]$OldPath = 'D:\Projects\image-scoring-backend',
    [string]$NewPath = 'D:\Projects\image-scoring-pipeline',
    [switch]$KeepFallbackJunction = $true
)

$ErrorActionPreference = 'Stop'

Write-Host "==> Checking prerequisites..."
if (-not (Test-Path -LiteralPath $OldPath)) {
    throw "Target folder $OldPath does not exist!"
}

$oldItem = Get-Item -LiteralPath $OldPath -Force
if ($oldItem.LinkType -eq 'Junction') {
    Write-Host "[OK] $OldPath is already a junction. Renaming is already complete."
    exit 0
}

if (Test-Path -LiteralPath $NewPath) {
    $newItem = Get-Item -LiteralPath $NewPath -Force
    if ($newItem.LinkType -ne 'Junction') {
        throw "$NewPath already exists and is a regular directory (not a junction)! Aborting."
    }
    Write-Host "==> Removing interim junction $NewPath..."
    cmd /c rmdir $NewPath
    if (Test-Path -LiteralPath $NewPath) {
        throw "Failed to remove junction $NewPath"
    }
}

# Record linked worktrees before the rename; paths inside the repo move with it.
$oldFull = [IO.Path]::GetFullPath($OldPath).TrimEnd('\')
$worktrees = @(git -C $OldPath worktree list --porcelain |
    Where-Object { $_ -like 'worktree *' } |
    ForEach-Object { [IO.Path]::GetFullPath($_.Substring(9)).TrimEnd('\') } |
    Where-Object { $_ -ne $oldFull } |
    ForEach-Object {
        if ($_.StartsWith($oldFull + '\', [StringComparison]::OrdinalIgnoreCase)) { $NewPath + $_.Substring($oldFull.Length) } else { $_ }
    })
Write-Host "==> Linked worktrees to repair after rename: $($worktrees.Count)"

try {
    Write-Host "==> Renaming directory $OldPath to $(Split-Path $NewPath -Leaf)..."
    Rename-Item -LiteralPath $OldPath -NewName (Split-Path $NewPath -Leaf)
    Write-Host "[OK] Successfully renamed to $NewPath"

    if ($KeepFallbackJunction) {
        Write-Host "==> Creating backward-compatibility junction $OldPath -> $NewPath..."
        New-Item -ItemType Junction -Path $OldPath -Target $NewPath | Out-Null
        Write-Host "[OK] Fallback junction created: $OldPath -> $NewPath"
    }

    # Repair every linked worktree recorded before the rename (both link directions).
    $existing = @($worktrees | Where-Object { Test-Path -LiteralPath $_ })
    if ($existing.Count -gt 0) {
        git -C $NewPath worktree repair @existing
        if ($LASTEXITCODE -ne 0) { Write-Warning "git worktree repair exited $LASTEXITCODE" }
        Write-Host "[OK] Repaired $($existing.Count) worktree(s)"
    }

    Write-Host ""
    Write-Host "==> Running layout doctor..."
    $doctorScript = Join-Path $PSScriptRoot "layout-doctor.ps1"
    if (Test-Path -LiteralPath $doctorScript) {
        & $doctorScript
    }

    Write-Host ""
    Write-Host "[DONE] Renaming completed successfully."
}
catch {
    Write-Warning "Rename failed: $_"
    # Rollback if needed
    if ((Test-Path -LiteralPath $OldPath) -and (-not (Test-Path -LiteralPath $NewPath))) {
        New-Item -ItemType Junction -Path $NewPath -Target $OldPath | Out-Null
        Write-Warning "Rollback: Restored junction $NewPath -> $OldPath"
    }
    throw
}
