"""Index product modules/config reads and distinguish mapped contracts from unaudited gaps."""

import ast
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

HUB = Path(__file__).resolve().parents[2]
OUT = HUB / "docs/reports/architecture-review-2026-10-23/evidence"
BASELINE = json.loads((OUT / "baseline.json").read_text())


def mapped(repo, rel):
    if repo.endswith("model"):
        if rel.startswith("src/eye_quality/"):
            return "eye-evidence.md"
        if rel.startswith("training/"):
            return "training-and-evaluation.md"
    if repo.endswith("skills"):
        if rel.startswith("scripts/neardupe_study/"):
            return "dedupe-physical-and-application.md"
        if rel.startswith(".cursor/scripts/"):
            return "editorial-and-color-evidence.md"
    if repo.endswith("pipeline"):
        if rel.startswith(("modules/engines/", "modules/remote_gpu/")) or rel in (
            "modules/phases.py", "modules/phase_executors.py", "modules/pipeline.py", "modules/job_dispatcher.py",
            "modules/score_normalization.py", "modules/scoring_inputs.py", "scripts/python/run_all_musiq_models.py"):
            return "execution-and-scoring.md"
        if rel.startswith("modules/localization") or rel.startswith("modules/detectors/") or rel in (
            "modules/rendition.py", "modules/rendition_cache.py", "modules/bird_species.py",
            "modules/bird_species_eligibility.py", "modules/bird_detection.py"):
            return "localization-and-consumers.md"
        if rel in ("modules/embedding_spaces.py", "modules/embedding_extractors.py", "modules/culling_embeddings.py",
                   "modules/clustering.py", "modules/sub_clustering.py", "modules/two_level_culling.py",
                   "modules/liqe.py", "modules/topiq.py", "modules/arniqa.py", "modules/student_scoring.py"):
            return "model-catalog.md"
    return ""


def main():
    modules, config_reads, supplements = [], [], []
    for repo, baseline in BASELINE["repositories"].items():
        root = HUB.parent / repo
        known = {f["path"]: f for f in baseline["working_files"]}
        # Teacher sources can be ignored locally; record their hashes too rather than pretending absent code.
        if repo.endswith("model"):
            for path in (root / "training").rglob("*.py"):
                rel = path.relative_to(root).as_posix()
                if rel not in known:
                    item = {"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "tracked": False, "baseline_status": "supplemental ignored source; captured during review"}
                    known[rel] = item
                    supplements.append({"repository": repo, **item})
        for rel, item in sorted(known.items()):
            if not rel.endswith(".py") or rel.startswith("tests/") or "/test_" in rel:
                continue
            if any(s in rel for s in ("/ci/", "assistant", "/skill_harness/", "/agent_harness/", "/agent_skills/",
                                      "/agent_memory/", "/agent-memory/", "okf_", "wiki_")):
                continue
            path = root / rel
            try:
                tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            except (SyntaxError, UnicodeError):
                continue
            page = mapped(repo, rel)
            committed = subprocess.run(["git", "-C", str(root), "show", "HEAD:" + rel], capture_output=True)
            committed_sha = hashlib.sha256(committed.stdout).hexdigest() if committed.returncode == 0 else ""
            dirty = any(s[:2] != "??" and s[3:] == rel for s in baseline["status"])
            relation = "modified" if dirty else "committed" if item["tracked"] else "untracked_or_ignored"
            modules.append({"repository": repo, "path": rel, "baseline_working_sha256": item["sha256"],
                            "head_blob_sha256": committed_sha, "baseline_relation": relation,
                            "symbols": sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for n in ast.walk(tree)),
                            "specification": "docs/specs/as-built/" + page if page else "",
                            "coverage": "partial_contract_mapping" if page else "explicit_gap",
                            "gap": "No line-by-line correctness or natural-image validation claimed; see subsystem matrix" if page
                            else "Inventory only; detailed behavior has not been reconstructed in this campaign"})
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or not node.args:
                    continue
                if node.func.attr not in ("get_config_value", "get_config_section"):
                    continue
                value = node.args[0]
                key = value.value if isinstance(value, ast.Constant) and isinstance(value.value, str) else "<dynamic>"
                config_reads.append({"repository": repo, "path": rel, "line": node.lineno,
                                     "reader": node.func.attr, "key": key})
    for name, rows in (("source-coverage.csv", modules), ("config-reads.csv", config_reads)):
        with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    (OUT / "supplemental-sources.json").write_text(json.dumps(supplements, indent=2) + "\n", encoding="utf-8")
    print("modules", len(modules), "coverage", dict(Counter(r["coverage"] for r in modules)),
          "config reads", len(config_reads), "supplemental ignored sources", len(supplements))


if __name__ == "__main__":
    main()
