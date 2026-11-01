---
type: Report
title: Architecture review run contract
description: Scope, evidence requirements, budgets and stopping conditions for the review campaign.
resource: reports/architecture-review-2026-10-23/run-contract.md
tags: [architecture, review, experiments]
timestamp: 2026-10-23T00:00:00Z
okf_version: 0.1
---

# Run contract

Objective: map each requested product subsystem to code-derived specifications or an explicit gap;
retain correctness fixes only after reproducing failures; compare each redesign track reproducibly.
The user's supplied campaign plan is the task authority. No commits or remote issue changes are requested.

Execution uses one coding agent and sequential evidence/fix/verification steps. Independent read-only
commands may run concurrently. No external CLI reviews or delegation. Jev routing is advisory and cannot
authorize export; the current coding model remains in use. The first two Jev calls classified/routed the
task (server-reported model `jev-1.14.0`); eight calls remain. All further judgments use sanitized summaries.

Mutable: product code and regression tests in the three owning repositories; canonical product docs,
as-built specs, indexes and logs; review receipts and local experiment tools. Protected: existing edits,
source photographs, original historical research, splits/labels, production databases/catalogs, consumer
activation settings, agent setup, credentials and Git configuration. Sibling writes need sandbox approval.

Baseline: `evidence/baseline.json` (kept local) records full HEADs, dirty paths and relevant
working-file SHA-256 values before review. Symbol CSVs are navigational inventories, **not** semantic
coverage claims. Exclusions: credentials, transcripts, vendored code, agent infrastructure, weights/data.
Untracked cleanup code and modified library workflow must be described as working-tree behavior.

Success signals: failing-then-passing targeted tests per fix; fresh relevant broader tests; docs integrity;
source-linked coverage matrix; frozen input/code/weight/parameter/metric identities per experiment.
Natural-image accuracy requires capture-group-separated evidence; synthetic checks establish conformance
only. No redesign is adopted without an attributable comparison and explicit adoption/rejection/inconclusive
decision. No training without established permissions, annotations and frozen splits.

GPU ceilings (including failures): baseline 2h, eye/localization 6h, region/scoring 6h, dedupe 8h,
final held-out replay 2h; total 24h. One GPU workload at a time; each run at most 2h. Check existing
workloads before launch; never interrupt them. No allocation is spent without a useful frozen hypothesis.
Record GPU usage, elapsed time, denominators, coverage, failures, memory and latency. CPU tests count as
zero campaign GPU-hours; existing unrelated GPU jobs do not become campaign evidence.

Retain only scoped fixes supported by red/green evidence. If a trial fails, undo only the trial's own edit,
preserving the original dirty baseline; no reset/clean. Mechanical environment errors get at most two
focused retries before recording the limitation. Do not weaken checks. Stop an experiment on timeout,
memory failure, interference with another GPU job, invalid provenance, or absent valid evaluation data.
Record the best artifact and unresolved acceptance criteria honestly; an inconclusive experiment is not
evidence of equivalence or accuracy. Production rollout, soft-culls, metadata edits, deployment, publication,
paid services other than the bounded Jev allowance, and new external exports are excluded.
