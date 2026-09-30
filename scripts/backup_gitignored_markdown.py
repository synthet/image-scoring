#!/usr/bin/env python3
"""Copy untracked, git-ignored *.md files from ecosystem repos under a parent dir."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PARENT = Path(r"C:\Projects")
SKIP_PREFIXES = (
    ".agent/scratch/",
    "node_modules/",
    ".venv/",
    "venv/",
    "dist/",
    "build/",
    "graphify-out/",
)
PRIVATE_PREFIXES = ("docs/private/", ".docs/private/")


def hub_manifest_repos(hub: Path) -> list[Path]:
    manifest = hub / "repos.manifest.json"
    if not manifest.is_file():
        return []
    data = json.loads(manifest.read_text(encoding="utf-8"))
    roots: list[Path] = [hub]
    for key in ("repositories", "infrastructure"):
        for entry in data.get(key, []):
            path = entry.get("path")
            if path:
                roots.append(Path(path))
    seen: set[str] = set()
    out: list[Path] = []
    for root in roots:
        key = str(root.resolve()).lower()
        if key in seen:
            continue
        seen.add(key)
        if root.is_dir() and (root / ".git").is_dir():
            out.append(root.resolve())
    return out


def discover_repos(parent: Path) -> list[Path]:
    repos = hub_manifest_repos(parent / "image-scoring")
    if repos:
        return repos
    found: list[Path] = []
    if (parent / "image-scoring").is_dir():
        found.append((parent / "image-scoring").resolve())
    for path in sorted(parent.glob("image-scoring-*")):
        if (path / ".git").is_dir():
            found.append(path.resolve())
    return found


def ignored_untracked_md(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--others", "-i", "--exclude-standard"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        rel = line.strip()
        if not rel.endswith(".md"):
            continue
        if any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        paths.append(rel)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, default=DEFAULT_PARENT)
    parser.add_argument(
        "--only-private-dirs",
        action="store_true",
        help="Only docs/private/ and .docs/private/ markdown",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Backup root (default: <parent>/_backup/gitignored-markdown-<timestamp>)",
    )
    args = parser.parse_args()
    parent = args.parent.resolve()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    dest_root = args.dest or (parent / "_backup" / f"gitignored-markdown-{stamp}")
    dest_root.mkdir(parents=True, exist_ok=True)

    manifest_lines: list[str] = []
    copied = 0
    for repo in discover_repos(parent):
        for rel in ignored_untracked_md(repo):
            if args.only_private_dirs and not any(rel.startswith(p) for p in PRIVATE_PREFIXES):
                continue
            src = repo / rel
            if not src.is_file():
                continue
            try:
                repo_key = src.relative_to(parent)
                out = dest_root / repo_key
            except ValueError:
                out = dest_root / repo.name / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)
            manifest_lines.append(f"{repo}|{rel}")
            copied += 1

    (dest_root / "BACKUP_MANIFEST.txt").write_text(
        "\n".join(manifest_lines) + ("\n" if manifest_lines else ""),
        encoding="utf-8",
    )
    print(f"Backup root: {dest_root}")
    print(f"Files copied: {copied}")
    return 0 if copied >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
