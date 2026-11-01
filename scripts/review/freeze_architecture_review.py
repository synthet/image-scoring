"""Freeze local product sources without copying code, credentials, weights, or datasets."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPOS = ("image-scoring-model", "image-scoring-pipeline", "image-scoring-skills")
PRODUCT_ROOTS = {
    REPOS[0]: ("src/", "training/", "tools/", "tests/", "docs/", "scripts/"),
    REPOS[1]: ("modules/", "scripts/", "tests/", "docs/", "migrations/", "models/"),
    REPOS[2]: ("scripts/", "prompts/", "docs/", ".cursor/scripts/"),
}
EXCLUDED = ("/vendor/", "/skill_harness/", "/agent_memory/", "/agent-memory/", "/agent_harness/")


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, encoding="utf-8")


def freeze(root: Path, output: Path) -> dict:
    files = sorted(set(git(root, "ls-files", "--cached", "--others", "--exclude-standard").splitlines()))
    committed = set(git(root, "ls-files").splitlines())
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    hashes, symbols, errors = [], [], []
    for rel in files:
        path = root / rel
        if not path.is_file() or not rel.startswith(PRODUCT_ROOTS[root.name]):
            continue
        if any(part in "/" + rel for part in EXCLUDED):
            continue
        if path.suffix.lower() not in (".py", ".md", ".yaml", ".yml", ".toml", ".ps1"):
            continue
        if any(part in rel.lower() for part in ("secret", "credential", "transcript", "session-dump")):
            continue
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        hashes.append({"path": rel, "sha256": sha, "bytes": len(data), "tracked": rel in committed})
        if path.suffix != ".py":
            continue
        try:
            tree = ast.parse(data.decode("utf-8-sig"), filename=rel)
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"path": rel, "error": str(exc)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                symbols.append((rel, node.lineno, type(node).__name__, node.name, sha))
    output.mkdir(parents=True, exist_ok=True)
    with (output / f"{root.name}-symbols.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("path", "line", "kind", "symbol", "working_sha256"))
        writer.writerows(sorted(symbols))
    return {
        "head": git(root, "rev-parse", "HEAD").strip(),
        "branch": git(root, "branch", "--show-current").strip(),
        "status": status,
        "working_files": hashes,
        "parse_errors": errors,
        "symbol_count": len(symbols),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--siblings", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target = args.output / "baseline.json"
    if target.exists():
        parser.error("Baseline already exists; choose a new output directory rather than replacing evidence")
    result = {"frozen_at": datetime.now(timezone.utc).isoformat(), "repositories": {}}
    for name in REPOS:
        result["repositories"][name] = freeze(args.siblings / name, args.output)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for name, receipt in result["repositories"].items():
        print(name, receipt["head"], "files", len(receipt["working_files"]), "symbols", receipt["symbol_count"], "dirty paths", len(receipt["status"]))


if __name__ == "__main__":
    main()
