---
type: Report
title: Architecture review and enhancement campaign
description: Source-derived specifications, regression fixes, development comparisons, coverage gaps and the focus evidence plan.
resource: reports/architecture-review-2026-10-23/INDEX.md
tags: [image-scoring, architecture, review, experiments, integration]
timestamp: 2026-10-24T03:00:00Z
okf_version: 0.1
---

# Architecture review and enhancement campaign

The reviewed core workflows now have seven code-derived specifications, two regression-tested correctness
fixes and reproducible CPU comparisons. The next integration opportunity is independently localized
subject evidence augmented by camera metadata and shown in Kestrel. The
[focus evidence synergy plan](../../planning/focus-evidence-synergy-2026-10-23.md) specifies staged work,
ownership, contracts and acceptance criteria. It does not activate a scoring or culling policy.

**Campaign status: partial architecture coverage; redesign accuracy inconclusive.** This report does not
claim that every module was reviewed or that the requested natural-image/GPU campaign is complete.
The module inventory makes remaining gaps explicit. No GPU budget was consumed, training run, weights
published, production gates changed, photo metadata rewritten, or soft-culls applied.

## Frozen sources and working changes

| Sibling | HEAD | Interpretation |
|---|---|---|
| Model | `b80aa536c3597d9986ca3121fc0e6376741df57d` | Committed runtime plus existing dataset/training/agent edits; targeted fallback fix added |
| Pipeline | `321d3a15f5ebf5f2de62cc212eb087eccf548f2e` | Existing working changes preserved; product code unchanged by this campaign |
| Skills | `98e8246250af3e06a344e351f2f00f3f6d6c33df` | Cleanup package was already untracked working code; finite-evidence fix applies to that package |
| Kestrel | `373330f37425c7ff19359f6765188f0697dbe7a3` | Later read-only extension; existing measurement/session/app edits preserved |

Baseline hashes/status (`evidence/baseline.json`, kept local) freeze the first three before review edits;
The Kestrel snapshot (`evidence/kestrel-snapshot.json`, kept local) was captured after initial read-only exploration.
Symbol inventories list classes/functions with working-file hashes. The
[documentation write receipt](evidence/documentation-writes.json) records before/after hashes for the initial
canonical backfill. Historical research remains in place, including the
[earlier nested-checkout synergy report](../model-pipeline-skills-synergy-2026-10-23.md).

## Architecture and code-to-spec matrix

Source-derived specs live in each owning repository's `docs/specs/as-built/`; proposed changes live in
the hub plan. These are reviewed workflow contracts, not a claim of line-by-line verification of every
source file. Public API/schema contracts retain authority where intended requirements conflict with code.

| Project and subsystem | As-built specification | Observed flow and remaining gap |
|---|---|---|
| Model detection, pose, eye crops, heuristics, confidence/visibility, aggregation | `image-scoring-model/docs/specs/as-built/eye-evidence.md` | Image → localization → eye crops → per-eye metrics → aggregation; confidence affects grade after candidate selection. Full EXIF/real-weight conformance and tiny-crop boundaries remain gaps |
| Model datasets, teachers, checkpoints and field evaluation | `image-scoring-model/docs/specs/as-built/training-and-evaluation.md` | Annotation validity/masks → training recipes → candidate checkpoints → frozen grouped field evaluation. Unknown labels are not negatives; partial-label helper is not evidence it is wired into stock training |
| Pipeline phase lifecycle, local/remote registry, normalization/fusion | `image-scoring-pipeline/docs/specs/as-built/execution-and-scoring.md` | Metadata → config-gated localization and consumer phases; registered/enabled/shadow/fusion membership differ. Actual cross-host inference parity remains unverified |
| Pipeline rendition identity, region ownership, species and repair | `image-scoring-pipeline/docs/specs/as-built/localization-and-consumers.md` | Decode/cache → versioned detections → explicit selection → consumer crop/fallback → persistence/repair. Isolated selection locks tested; full repair/decode matrices remain gaps |
| Pipeline model catalog, embeddings, clustering/culling | `image-scoring-pipeline/docs/specs/as-built/model-catalog.md` | Named model recipes and native ranges; typed embedding spaces → visual grouping → allocation/ranking. No clustering edge establishes physical equivalence; actual runtime/weight coverage incomplete |
| Skills candidate retrieval, physical comparison, dominance, representatives, guarded application | `image-scoring-skills/docs/specs/as-built/dedupe-physical-and-application.md` | Candidate pairs → measurements → finite physical gate → local dominance → direct keeper edges → protection/coverage → separate guarded dry-run/application. Natural-image false-cull accuracy unresolved |
| Skills reviewers, Jev, carousel, evidence/color exports | `image-scoring-skills/docs/specs/as-built/editorial-and-color-evidence.md` | Reviewer evidence → finite fit/constraints → ordered relaxation → incomplete-result reporting; separate color/ICC/histogram evidence. Historical judge labels are not human ground truth |
| Kestrel local scorer, model adapters, burst/session/reweigh, diagnostics | [Kestrel review](kestrel-as-built.md) | Overview evidence → criteria → body/time bursts → ranked review; explicit user flags remain separate. Bird eye fallback and absent AF ingest limit focus interpretation |

The named catalog reconciles YOLO/RTMDet, MUSIQ variants, LIQE, TOPIQ, ARNIQA, CLIP/BioCLIP,
conditional student models, SSCD and DINOv2/DINOv3, distinguishing recipes from enabled inference,
shadow evidence, experiments and available weights. It explicitly records unresolved runtime/checkpoint
identity rather than treating a file or registry entry as proof of execution.

[Source coverage](evidence/source-coverage.csv): **788 Python modules indexed**, 159 mapped to partial
workflow contracts and **629 inventory-only gaps**. This is 41 model, 672 pipeline and 75 skills modules;
the count excludes tests and selected agent/infrastructure surfaces, and includes supplemental locally
ignored training sources recorded in [their receipt](evidence/supplemental-sources.json).
[Configuration reads](evidence/config-reads.csv) record AST-located config accesses; dynamic keys,
environment variables, CLI flags and transitive consumers are not a complete gate inventory.
Kestrel is a focused extension, not included in that three-repository denominator.

Canonical pages were backfilled first: model pipeline/API semantics, pipeline model ranges/defaults and
phase graph, skills physical-gate and editorial contracts. Each sibling gained as-built/spec indexes,
authority pointers and activity entries. Documentation discrepancies still requiring wider work include
actual weight/runtime provenance, undocumented module behavior, Kestrel's draft/implemented peaking
authority and historical explanatory examples that may outlive their policy revision.

## Prioritized findings and retained fixes

| Priority | Concrete trigger and cause | Result and regression evidence |
|---|---|---|
| Data/decision integrity | Replay/direct physical-decision inputs contain NaN, infinities, strings or booleans. None-only checks allowed NaN comparisons to fall through or malformed values to crash; invalid quality could influence dominance | Skills validates required metrics/local evidence and policy numbers. Invalid evidence retains; invalid thresholds refuse the decision. [Red](evidence/red-cleanup.json) then [46-test green](evidence/targeted-tests.json); no thresholds or policy activation changed |
| Incorrect measurement | NumPy-only eye-noise fallback receives a flat bright crop. Its 3×3 uint8 sum wraps before averaging, producing noise where none exists | Model promotes padded pixels to float before summing. [Five failing regressions](evidence/red-model-tests.json) then [88-test green](evidence/green-model-tests.json), with two GPU cases deselected |
| Contract/reproducibility | Normalization exactly at LIQE p02=.311 returns .15, while a value 1e-6 above returns about .000001456 | Confirmed discontinuity; versioned candidate comparison only. Do not silently migrate stored scores or assume sampled rank equivalence proves all-input equivalence |
| Incorrect interpretation | Bird subject p98 gradients are presented as estimated eye evidence in Kestrel; Nikon AF success does not establish optical eye focus | Preserve source/applicability labels; add verified anatomy and AF-target measurements separately. No AF ranking policy implemented |
| Reproducibility | AF grid, RAW grid, active crop and preview may differ; tag namespaces and subsecond strings carry information | Frozen eleven-file extraction; geometry/decoder conformance is the first enhancement stage, before overlays or alignment decisions |

The non-finite trigger is traced through measurement sanitizers, artifact loading and selection. Standard
measurement builders already sanitize numbers and normal artifact writers disallow NaN, but Python JSON
loading can accept non-standard non-finite constants. The independent decision boundary still needs
validation; this is not evidence that ordinary production rows routinely carried the malformed values.

## Measured redesign decisions

The [freeze](evidence/cpu-comparison-v2/experiment-freeze.json) pins inputs and runner before the
[CPU replay](evidence/cpu-comparison-v2/experiment-results.json). An earlier path-format failure is retained
in the [attempt receipt](evidence/experiment-attempts.json). Both consumed zero GPU time.
Successful replay took 5.380 s, peak process RSS 369060 KiB in that container; this is not inference latency.

| Track | Comparison and denominators | Decision |
|---|---|---|
| Eye evidence | Current post-selection confidence handling vs confidence-filtered candidates; 16 synthetic scalar cases, 4 best-eye changes | **Inconclusive** for natural-image quality. Demonstrates a semantic difference only; no learned/localization improvement established |
| Scoring | Historical human-blind development labels, 77,331-image snapshot; fixed current vs continuous normalization vs no ARNIQA; validation general/technical/aesthetic n=22 in 11 blocks | **Inconclusive**. Current general weighted rho .340, 95% interval [-.194,.736]; no-ARNIQA .352 [-.176,.686]. Continuous candidate leaves sampled rankings unchanged. No test split accessed for evaluation |
| Keeper ranking | Same historical study, validation culling n=8 in 5 blocks; weighted expected top-1 .589 with interval [0,1] for all three policies | **Inconclusive**; denominator and uncertainty do not support replacing production fusion |
| Dedupe uncertainty | Three development shoots, 1,898 candidate pairs, 693 fully measured and 1,205 missing; default uncertainty vs strict margin | Proposed suppressions 26 → 3; direct retained keeper, protection and reverse-order checks passed. **Inconclusive** for false-cull accuracy; no human labels used here |
| Nikon/Kestrel | Eleven Z8 NEFs, four temporal groups; metadata/geometry only; 86 existing focused tests pass | Adopt a **specification-first inspection pilot** as the next work item; no score/culling adoption |

No experiment establishes a production redesign winner. Full-frame vs selected-region natural-image
quality, registration/local dominance alternatives, representation choice, grouped held-out replay and
actual inference latency/memory remain open work under the staged plan. Synthetic conformance cannot
replace natural-image accuracy. Preserve the original historical study's test-access gate.

## Verification and acceptance

| Check | Result | Scope/limit |
|---|---|---|
| Model targeted documented fast subset | 88 passed, 2 GPU deselected; 2 subtests passed | Includes fallback regressions; no real-weight GPU replay |
| Skills cleanup/library/workflow subset | 46 passed | Includes finite-value regressions and guarded workflow tests |
| Pipeline registry, prerequisites, normalization, rendition/selection/species tests | 72 passed | CPU contract checks; no local/remote real-model parity |
| Isolated PostgreSQL concurrency | 3 passed | Disposable pg17 tmpfs, no production mounts or exposed ports; [isolation receipt](evidence/postgres-isolation.json) |
| Kestrel scoring/model-adapter/burst/session subset | 86 passed, 1 skipped | Native CPU, synthetic/fake-model fixtures; no Electron review |
| Broader skills discovery | 177 run, 5 errors, 4 skipped | Existing removal-manifest fixtures assume Windows disk identity; failed under Linux tmp paths. Not reported as a green suite |
| Documentation | Final focused checks: zero errors/warnings in hub and all three siblings | Fixed the pre-existing pipeline archive link; native host lacked YAML, so the hub check used the existing offline container |
| Full natural-image, GPU, remote and complete DB/repair campaign | Unknown/not run | No claim of coverage based on unit tests |

Every retained product fix has failing-then-passing evidence. Every executed redesign comparison has an
explicit inconclusive decision. The complete module-level review and natural-image validation remain
unfinished; that limitation is part of the handoff, not an acceptance pass. Production rollout remains
behind the existing consumer gates and is outside this campaign.

The shared LLM Wiki lookup supplied candidate/stale Nikon context, with exact identifiers preserved in
the focus plan. New campaign claims must remain evidence-bound candidates; an agent does not grant
human review status. Current consolidation receipt, when generated, is linked from this directory rather
than inferred from the older report's historical ingestion.

The wiki accepted the hub reports but refused direct sibling-spec ingestion because those paths are
outside its configured allowed roots. The refusal is retained in `evidence/wiki-ingest.json`; roots and
permissions were not changed. Consolidation therefore uses the hub's source-linked summaries, with
the complete as-built pages remaining authoritative in their owning repositories.
