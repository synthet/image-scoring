---
type: Plan
title: Cross-project vision stack comparison and plan
description: GPU models, heuristics and algorithms used across the image-scoring repos, with conflicts, gaps, synergy and a low-hanging-first implementation plan.
resource: docs/planning/cross-project-vision-stack-2026-11-01.md
tags: [planning, models, heuristics, deduplication, culling, synergy]
timestamp: 2026-11-01T00:00:00Z
okf_version: 0.1
---

# Cross-project vision stack comparison and plan

Read-only survey of the model, pipeline, skills, Kestrel and gallery repositories on 2026-11-01.
The counts are files under production paths that mention each name (model `src/`, `scripts/` and
`training/`; pipeline `modules/`; skills `scripts/neardupe_study/` and `scripts/score_analytics/`;
Kestrel `kestrel-py/`; gallery `src/` and `electron/`), excluding tests, scratch and environments.
A count shows presence, not usage volume. Config values and the database were not read.

## 1. Models and algorithms by repository

| Model / algorithm | Model | Pipeline | Skills | Kestrel | Gallery | Owner today |
|---|---:|---:|---:|---:|---:|---|
| MUSIQ / LIQE / TOPIQ / ARNIQA (IQA) | 0 | 13 / 39 / 25 / 10 | 0 / 3 / 3 / 2 | 0 | 2 / 13 / 4 / 3 | pipeline (others read scores) |
| CLIP quality | 0 | 23 | 8 | 0 | 5 | pipeline |
| BioCLIP (species) | 1 | 20 | 5 | 0 | 3 | pipeline |
| SigLIP | 0 | 4 | 3 | 0 | 0 | — |
| DINOv2 | 0 | 3 | 9 | 0 | 0 | pipeline (`embedding_extractors.py`) and skills (study) |
| DINOv3 | 0 | 0 | 4 | 0 | 0 | skills study only; pipeline#741 proposes it |
| SSCD (copy detection) | 0 | 0 | 12 | 0 | 0 | skills study only; pipeline#606 pilot |
| YOLO / Ultralytics | 17 | 8 | 0 | 0 | 0 | model (`bird_detect_v1`) |
| RTMDet / RTMPose | 7 / 2 | 3 / 0 | 0 | 2 / 2 | 0 | model; Kestrel runs its own |
| SAM 2 | 1 | 1 | 0 | 0 | 0 | model |
| DISK + LightGlue (+ homography) | 0 | 0 | 3 | 0 | 0 | skills study |
| pHash / dHash | 0 | 0 | 16 | 0 | 0 | skills study |
| ECC alignment (`findTransformECC`) | 0 | 0 | 3 | 0 | 0 | skills study |
| HDBSCAN / agglomerative clustering | 0 | 3 | 4 | 0 | 0 | pipeline stacks; skills study |
| MMR (diversity) | 0 | 3 | 3 | 0 | 6 | three separate implementations |

## 2. Heuristics side by side

| Heuristic | Model | Pipeline | Skills | Kestrel |
|---|---|---|---|---|
| Sharpness | eye crops: plain Laplacian variance / 500, blended `0.45*sharpness + 0.35*clarity + 0.20*edge_energy` | `focus_quality.py`: Immerkaer noise estimate, Laplacian variance minus `20*sigma^2`, subject vs context ring at native resolution | vendored copy of the pipeline statistic at `bfafd1b5` (no drift as of 2026-11-01) | gradient statistic, `detail_score` half-saturation at 12 levels/px |
| Grouping | — | stacks by visual similarity; `clustering.default_time_gap` defaults to 120 s | keep-one "same moment": pose tolerances and measured pairs, no time gap | `DEFAULT_GAP_MS = 500` (250–3000) |
| Tie-break | — | `quality_ranking.py` canonical order, mirrored in the gallery's `electron/db.ts` | keep-one: protected, then 5% head-sharpness lead, then refcull focus gap 0.03, then Jev on measured ties | — |
| Box format | `[x,y,w,h]` | corner `[x1,y1,x2,y2]` | pipeline boxes | — |
| Deletion | — | `scripts/neardupe_maintenance/` (canonical, protects human labels) | older study copy without that protection | — |

## 3. Conflicts

1. **Noise-blind eye sharpness in the model repo.** The model eye scorer uses exactly the
   `laplacian_variance / 500` formula the pipeline removed, because sensor noise moved the
   variance from 0.019 to 4435 on a defocused region. Filed as model#8. Skills#25 plans raw
   Laplacian/Tenengrad features and should reuse the noise-corrected statistic.
2. **"Burst" means three different things:** 500 ms (Kestrel), 120 s plus visual similarity
   (pipeline stacks) and pose equivalence (keep-one). Box formats also differ between model and
   pipeline. Filed as hub#1 (vision terms contract).
3. **Two deletion executors.** The skills study copy lacks the pipeline copy's human-label
   protection and cross-drive recovery. Deletions ran through the pipeline copy, but the study
   copy can still apply. Filed as skills#30.
4. **Stale roadmap.** The planned `paired-physical-v1` pipeline module was never built and keep-one
   replaced its rule. Filed as skills#31.
5. **Two culling models in waiting:** keep-one (skills) and replacement-graph set-cover
   (pipeline#511). Reconciliation is part of pipeline#743.

## 4. Gaps

- The pipeline has no SSCD and no production DINOv3 (pipeline#606, pipeline#741), so every skills
  study recomputes embeddings the pipeline could own.
- No closed-eye / nictitating-membrane / catchlight signal anywhere (model#7, skills#28).
- No pairwise (Bradley-Terry) aggregation of judge or owner verdicts (skills#24).
- No both-order judge presentation; `audit_panel.py` randomises A/B once with a fixed seed
  (follow-up G in the CV report adoption plan).
- No learned keeper ranking from owner picks (follow-up F; gated on the skills#24 label count).

## 5. Synergy

- **One owner per signal.** IQA and embeddings belong in the pipeline (pgvector spaces);
  detection and keypoints in the model repo; pair evidence and culling research in skills;
  presentation in the gallery. Studies read the owner's output instead of recomputing it.
- **Proven delivery routes.** Skills to pipeline through `export_delivery.py` (as for
  `neardupe_maintenance`); skills to gallery through versioned read-only JSON exports (as for
  `driftara-representative-preview/1`); skills judge harness reused by the model repo for QC.
- **Shared focus statistic.** The pipeline's noise-corrected sharpness is already vendored into
  skills; extending it to the model eye scorer and Kestrel removes the largest numerical conflict.

## 6. Implementation plan, low-hanging first

| Order | Item | Issue | Size | Why first |
|---|---|---|---|---|
| 1 | Mark the stale roadmap rows superseded | skills#31 | XS | Docs only; removes a misleading "Ready to Code" |
| 2 | Refuse apply mode in the study deletion copy; sharpness drift check | skills#30 | S | Closes a safety gap with one test |
| 3 | Vision terms contract (burst, stack, same moment, sharpness owner, box format) | hub#1 | S | Unblocks consistent specs and reviews in every repo |
| 4 | Noise-corrected eye sharpness, impact measured first | model#8 | S–M | Largest numerical conflict; versioned, default unchanged until reviewed |
| 5 | Keep-one review view in the gallery | gallery#210 | M | Reuses the representative-preview contract pattern |
| 6 | Pairwise-wins / Bradley-Terry keeper study | skills#24 | M | Offline; label count first |
| 7 | Focus-measure profiling go/no-go | pipeline#738 | S | Only matters if technical-failure detection is enabled |
| 8 | Keep-one as a pipeline culling policy, reconciled with #511 and #607 | pipeline#743 | M–L | Skills#21 is merged; needs a parity test |
| 9 | SSCD and DINOv3 embedding spaces | pipeline#606, pipeline#741 | M | Removes per-study recompute |
| 10 | Bird-masked GPU features, AF background check, E7, catchlight, MMR carousel | skills#25–#29, model#7 | M–L | Already filed by another session; align with items 3 and 4 |

Rules for every item: no production policy activation, no library metadata or stored-score
rewrite, frozen evaluation with label classes kept separate, soft-cull before any hard delete, and
a hard delete only with the owner's explicit go-ahead.
