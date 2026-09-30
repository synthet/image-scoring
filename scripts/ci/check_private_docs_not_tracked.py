#!/usr/bin/env python3
"""Fail if git tracks files under docs/private/ or .docs/private/ in ecosystem repos."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = HUB_ROOT / "repos.manifest.json"
PRIVATE_PREFIXES = ("docs/private/", ".docs/private/")


def repo_roots() -> list[Path]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    roots: list[Path] = [HUB_ROOT]
    for entry in data.get("repositories", []):
        path = entry.get("path")
        if path:
            roots.append(Path(path))
    seen: set[str] = set()
    unique: list[Path] = []
    for root in roots:
        key = str(root.resolve()).lower()
        if key in seen or not root.is_dir():
            continue
        seen.add(key)
        unique.append(root)
    return unique


def tracked_private_paths(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "docs/private", ".docs/private"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def gitignore_covers_private(repo: Path) -> list[str]:
    gi = repo / ".gitignore"
    if not gi.is_file():
        return ["missing .gitignore"]
    text = gi.read_text(encoding="utf-8", errors="replace")
    missing: list[str] = []
    for prefix in PRIVATE_PREFIXES:
        if prefix not in text and prefix.rstrip("/") not in text:
            missing.append(f".gitignore must list {prefix}")
    return missing


def main() -> int:
    errors: list[str] = []
    for repo in repo_roots():
        rel = repo.name
        errors.extend(f"{rel}: {msg}" for msg in gitignore_covers_private(repo))
        for path in tracked_private_paths(repo):
            errors.append(f"{rel}: tracked private doc {path}")
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    print("Private doc paths OK (ignored and not tracked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
