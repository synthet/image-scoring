"""Frozen CPU comparisons; no model loading, service calls, test-label access or production writes."""

import argparse
import gzip
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def paths(siblings):
    pipeline = siblings / "image-scoring-pipeline"
    skills = siblings / "image-scoring-skills"
    model = siblings / "image-scoring-model"
    study = pipeline / "reports/model-selection-2026-10-01"
    measurements = skills / "work/disk/library-dedupe-2026-10-21/score/cleanup-dryrun-2026-10-23/shoots"
    files = [study / name for name in ("snapshot.json.gz", "sample.json", "reviews.jsonl")]
    files += sorted(measurements.glob("*/measurements.json"))
    files += [pipeline / "modules/score_normalization.py", pipeline / "modules/score_analytics/study.py",
              pipeline / "modules/score_analytics/study_report.py", model / "src/eye_quality/scoring/aggregate.py",
              skills / "scripts/neardupe_study/cleanup/physical.py", skills / "scripts/neardupe_study/cleanup/represent.py"]
    return files


def freeze(siblings, output):
    target = output / "experiment-freeze.json"
    if target.exists():
        raise ValueError("Experiment freeze already exists")
    files = paths(siblings)
    if len([p for p in files if p.name == "measurements.json"]) != 3:
        raise ValueError("Expected exactly three historical development-shoot measurement tables")
    receipt = {"runner_sha256": sha(__file__), "inputs": {p.relative_to(siblings).as_posix(): sha(p) for p in files},
               "gpu_hours_max": 0, "timeout_seconds": 600, "weights": "none loaded; frozen scores/measurements only",
               "parameters": {"bootstrap_resamples": 1000, "bootstrap_seed": 20261001,
                              "variants": ["current", "continuous-v2-candidate", "without-arniqa"],
                              "eye": "focus [.2,.5,.7,.9] x confidence [.1,.3,.45,.9], two visible 48px crops",
                              "dedupe": "unchanged physical POLICY vs uncertainty_margin=true; no threshold search"},
               "metrics": {"eye": "selection disagreement/grade, synthetic conformance only",
                           "scoring": "fixed train/validation human_blind weighted rho/top1, block bootstrap; no test labels",
                           "dedupe": "per-shoot coverage/edges/suppressions/representatives, no accuracy claim"},
               "stopping": "fail on identity drift, leakage, invalid labels or timeout; no retries for metric shopping",
               "decisions": "No production adoption from conformance alone. Natural-image adoption needs independent held-out evidence."}
    output.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("Frozen", len(files), "inputs and runner", receipt["runner_sha256"])


def scoring(siblings):
    import numpy as np
    from modules import score_normalization as normal
    from modules.score_analytics import study, study_report

    root = siblings / "image-scoring-pipeline/reports/model-selection-2026-10-01"
    sample = json.loads((root / "sample.json").read_text())
    assert sha(root / "snapshot.json.gz") == sample["snapshot_sha256"]
    snapshot = json.loads(gzip.decompress((root / "snapshot.json.gz").read_bytes()))
    units = {u["id"]: u for u in sample["units"]}
    reviews = {}
    for line in (root / "reviews.jsonl").read_text().splitlines():
        row = json.loads(line)
        unit = units[row["unit_id"]]
        if unit["split"] == "test":
            continue  # Never inspect test-label content for this development comparison.
        assert row.get("study_id") == sample["study_id"]
        study.validate_review(unit, row)
        if row["reviewer"] == "owner":
            reviews[row["unit_id"]] = row
    images = {r["id"]: r for r in snapshot["images"]}
    anchors, fusion = snapshot["percentile_anchors"], snapshot["fusion"]
    models = sorted(set().union(*(set(w) for w in fusion.values())))
    normal._config_cache = {"percentile_anchors": anchors, "scoring": {"fusion": fusion}}

    def score(frame, category, variant):
        values = frame["scores"]
        weighted = []
        for key, weight in fusion[category].items():
            if variant == "without-arniqa" and key == "arniqa":
                continue
            value = values.get(key)
            if value is None or not math.isfinite(value):
                continue
            anchor = anchors.get(key)
            if anchor:
                low, high = anchor["p02"], anchor["p98"]
                if variant == "continuous-v2-candidate" and value > low and high > low:
                    value = min(1.0, .15 + .85 * (value - low) / (high - low))
                else:
                    value = normal.rescale_percentile(value, low, high)
            weighted.append((weight, value))
        return round(sum(w * s for w, s in weighted) / sum(w for w, _ in weighted), 4) if weighted else None

    report = []
    for split in ("train", "validation"):
        for category in ("general", "technical", "aesthetic", "culling"):
            eligible = [u for u in sample["units"] if u["split"] == split and not u.get("repeat_of")
                        and reviews.get(u["id"], {}).get("status") == "done"
                        and (u["kind"] != "single") == (category == "culling")]
            common = [u for u in eligible if all(isinstance(images[i]["scores"].get(m), (int, float))
                      and math.isfinite(images[i]["scores"][m]) for i in u["image_ids"] for m in models)]
            for variant in ("current", "continuous-v2-candidate", "without-arniqa"):
                rows = []
                for unit in common:
                    label = reviews[unit["id"]]
                    predicted = [score(images[i], "general" if category == "culling" else category, variant)
                                 for i in unit["image_ids"]]
                    if category == "culling":
                        labels = {f["image_id"]: f for f in label["frames"]}
                        metric = study.group_metrics(predicted, [labels[i]["grade"] for i in unit["image_ids"]],
                                                     [labels[i]["best"] for i in unit["image_ids"]])
                        if not metric or metric["top1"] is None:
                            continue
                        rows.append({**unit, "value": metric["top1"]})
                    else:
                        rows.append({**unit, "value": predicted[0], "label": label["ratings"][category]})
                def primary(rr, weights):
                    if category == "culling":
                        return float(np.average([r["value"] for r in rr], weights=weights))
                    return study.weighted_rho([r["value"] for r in rr], [r["label"] for r in rr], weights)
                metric = study.bootstrap_metric(rows, primary, resamples=1000, seed=20261001)
                report.append({"split": split, "category": category, "variant": variant,
                               "eligible": len(eligible), "common_complete": len(common), "measured": len(rows),
                               "subgroups": dict(Counter(u["stratum"] for u in common)), "metric": metric})
    low, high = anchors["liqe"]["p02"], anchors["liqe"]["p98"]
    boundary = {"p02": low, "at_p02": normal.rescale_percentile(low, low, high),
                "above_p02": normal.rescale_percentile(low + 1e-6, low, high)}
    return {"labels": "historical human_blind; development only; latest per owner/unit; repeats excluded",
            "snapshot_images": len(images), "groups": "frozen folder/session/overlap blocks from sample",
            "test_split": "not evaluated; no production adoption; preserve original study's test-access gate",
            "boundary": boundary, "comparisons": report,
            "decision": "inconclusive for production; development comparison cannot certify held-out quality"}


def eye():
    from eye_quality.schemas import PerEyeMetrics, EyeVisibility
    from eye_quality.scoring.aggregate import aggregate_eye_quality

    cases, changes = [], 0
    for focus in (.2, .5, .7, .9):
        for confidence in (.1, .3, .45, .9):
            inputs = [PerEyeMetrics(eye_side="left", visibility=EyeVisibility.VISIBLE,
                                   detection_confidence=confidence, bbox_norm=[0, 0, .1, .1],
                                   focus_score=focus, sharpness_score=focus, crop_width_px=48),
                      PerEyeMetrics(eye_side="right", visibility=EyeVisibility.VISIBLE,
                                   detection_confidence=.9, bbox_norm=[.2, .2, .1, .1],
                                   focus_score=.6, sharpness_score=.6, crop_width_px=48)]
            current = aggregate_eye_quality(inputs).eye_quality
            # A research-only candidate: admit confident evidence before ranking; never multiply focus by confidence.
            candidate = aggregate_eye_quality([r for r in inputs if r.detection_confidence >= .45]).eye_quality
            changed = current.best_eye_side != candidate.best_eye_side
            changes += changed
            cases.append({"focus": focus, "confidence": confidence, "current": current.model_dump(mode="json"),
                          "candidate": candidate.model_dump(mode="json"), "changed": changed})
    return {"population": "synthetic scalar evidence; not natural-image accuracy", "n": len(cases),
            "selection_changes": changes, "cases": cases,
            "decision": "inconclusive: confidence filtering changes selection; no labels justify its adoption"}


def dedupe(siblings):
    from scripts.neardupe_study.cleanup import physical, represent

    root = siblings / "image-scoring-skills/work/disk/library-dedupe-2026-10-21/score/cleanup-dryrun-2026-10-23/shoots"
    result = []
    for path in sorted(root.glob("*/measurements.json")):
        doc = json.loads(path.read_text())
        rows = doc["rows"]
        signals = {k: f for row in rows for k, f in row["frames"].items()}
        for strict in (False, True):
            policy = {**physical.POLICY, "uncertainty_margin": strict}
            decided = physical.decide(rows, policy)
            selected = physical.select(decided["edges"], signals)
            assert selected == physical.select(list(reversed(decided["edges"])), signals)
            assert not any(signals[k]["protected"] for k in selected["suppressed"])
            assert all(k not in selected["suppressed"] for k in selected["suppressed"].values())
            result.append({"shoot": path.parent.name, "strict": strict, "pairs": len(rows),
                           "fully_measured": sum(not r["missing"] for r in rows), "frames_in_pairs": len(signals),
                           "edges": len(decided["edges"]), "suppressed": len(selected["suppressed"]),
                           "retained_direct_keepers": len(set(selected["suppressed"].values())),
                           "representatives_in_candidate_frames": sum(len(b["representatives"]) for b in
                               represent.representatives(sorted(signals), rows, decided["verdicts"], signals))})
    return {"labels": "none used; historical development measurements; no false-cull rate",
            "comparisons": result, "decision": "inconclusive: strict uncertainty changes coverage, no unseen-shoot accuracy proof"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage", choices=("freeze", "run"))
    ap.add_argument("--siblings", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.stage == "freeze":
        freeze(args.siblings, args.output)
        return
    receipt = json.loads((args.output / "experiment-freeze.json").read_text())
    assert receipt["runner_sha256"] == sha(__file__)
    for rel, expected in receipt["inputs"].items():
        assert sha(args.siblings / rel) == expected, "Frozen input drift: " + rel
    for repo in ("image-scoring-pipeline", "image-scoring-skills"):
        sys.path.insert(0, str(args.siblings / repo))
    sys.path.insert(0, str(args.siblings / "image-scoring-model/src"))
    output = args.output / "experiment-results.json"
    assert not output.exists(), "Do not overwrite or repeatedly inspect experiment results"
    start = time.perf_counter()
    results = {"scoring": scoring(args.siblings), "eye": eye(), "dedupe": dedupe(args.siblings),
               "gpu_hours": 0, "elapsed_seconds": time.perf_counter() - start}
    try:
        import resource
        results["peak_process_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except ImportError:
        results["peak_process_rss_kib"] = None
    output.write_text(json.dumps(results, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    print("CPU comparison complete; GPU hours 0; seconds", results["elapsed_seconds"])
    print("Eye synthetic selection changes", results["eye"]["selection_changes"], "/", results["eye"]["n"])
    print("Dedupe", [(r["shoot"][:8], r["strict"], r["suppressed"]) for r in results["dedupe"]["comparisons"]])


if __name__ == "__main__":
    main()
