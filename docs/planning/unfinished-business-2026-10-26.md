---
type: Roadmap
title: Unfinished business and next steps
description: Consolidated remaining work, live issue and epic inventory, delivery gaps, dependencies and closeout criteria across the workspace.
resource: planning/unfinished-business-2026-10-26.md
tags: [planning, backlog, roadmap, ecosystem, handoff]
timestamp: 2026-10-26T00:00:00Z
okf_version: 0.1
---

# Unfinished business — 2026-10-26

This is a dated reconciliation of the eight product/hub repositories, their current working trees, public plans and GitHub backlog. It documents the remaining work; GitHub issues and the [project board](https://github.com/users/synthet/projects/1) remain the canonical execution queue. No issue, assignee, stage, PR, production setting or source photograph was changed by this documentation task.

The complete records are in the [issue and epic register](../reports/unfinished-business-2026-10-26/INDEX.md), [source-marker appendix](../reports/unfinished-business-2026-10-26/source-markers.md) and [machine-readable snapshot](../reports/unfinished-business-2026-10-26/inventory.json). The snapshot retains all open issue links, priorities, assignees, board stages, stage labels, formal parent/child relationships, open PRs, branch identities and plan-file hashes. Counts below describe that collection, not an enduring live dashboard.

**Post-collection update, 2026-10-27:** pipeline PR #679 merged at `2026-10-27T03:15:05Z` after the owner-requested conflict resolution `092f39a623a372bd8d95aed3513e41748b2bfa74`; all five CI checks passed. Of the three PRs originally collected, two remain open: pipeline #591 is conflicting and skills #4 is a draft with an UNSTABLE check state. The snapshot preserves the original retrieval state and records later delivery updates separately.

## Status and scope

| Record | Count | Meaning |
|---|---:|---|
| Open GitHub issues | 225 | 181 pipeline, 42 gallery, 1 model, 1 skills; hub/mobile/UI/Kestrel returned zero |
| Epics or issues with formal sub-issues | 22 | Existing tracker records; theme groups below are not newly created epics |
| Open PRs | 3 | Pipeline #679 and #591; skills draft #4 |
| Explicit source/documentation markers | 315 | 311 unchecked documentation items, 2 potential implementation comments and 2 explanatory template comments |
| Public working files scanned | 2,457 | 1,956 source files and 501 documentation files; exclusions are listed in the marker appendix |
| Open issues absent from the board | 50 | Intake/queue reconciliation needed; absence does not make an issue Ready |
| Board-linked open issues with no Stage | 16 | Generic Status=Todo does not establish Stage |
| Board/label stage disagreements | 2 | Pipeline #568 and #570: board In Progress, label stage:backlog |

**Verified** means there is a specific current check or state observation. **Reported open** means an issue or plan still lists the work; reproduce or reconcile it before implementing. **Proposed** means an existing research/specification idea without a confirmed delivery task. **Gated** means its prerequisite is not satisfied. A source marker is not automatically a defect or a new task.

The issue queries were paginated with a 2,000-item limit per repository; no repository reached it. All 319 project-board items were received. Formal hierarchy coverage was checked against the complete pipeline/gallery open-issue sets. Infrastructure repositories were consulted only as dependencies; their entire independent backlogs and private notes are outside this inventory. Collection spans several reads rather than one atomic transaction.

## Completed work to keep out of the unfinished queue

| Work | Evidence and remaining boundary |
|---|---|
| Nikon AF numeric/cache correction and container decoder fix | Pipeline [#672](https://github.com/synthet/image-scoring-pipeline/issues/672) is closed; [plan PR #670](https://github.com/synthet/image-scoring-pipeline/pull/670) is merged. This does not establish coordinate calibration or a ranking policy. |
| Pending AF build and decoder verification | [Verification report](../reports/focus-af-validation-2026-10-24/INDEX.md): Docker build passed, ExifTool 13.52, 97 focused tests passed / 3 deselected, five Z8 integration tests passed / two ML tests deselected. Scope is the recorded working tree at `e787a039`, not every later release commit. |
| Publish the verification record | Hub commit `0007f8c7f7fd9552374527e3cc6d653143edb528` was pushed and remote identity verified. Raw logs and transcripts remain local. |
| Structured CLIP output compatibility and release preparation | [#695](https://github.com/synthet/image-scoring-pipeline/issues/695) closed and [PR #696](https://github.com/synthet/image-scoring-pipeline/pull/696) merged during collection. They are removed from the open snapshot; no deployment or release-observation claim follows. |
| AF plan PR conflict resolution and merge | [PR #679](https://github.com/synthet/image-scoring-pipeline/pull/679) merged after both documentation conflicts were resolved and five CI checks passed. Only the intended plan and activity-log changes differed from master. |
| Localization consumer/writer work already delivered | The current rollout record says the gallery consumer, rollback drill, disagreement review and writer reroute (#664) are done. Stage 8 still has coverage and compatibility-observation gates; do not reopen the delivered subparts simply because #638's older checklist remains broad. |
| Mobile core review modes | The working adoption plan records box-quality, presence, pairwise comparison, best-in-burst/loupe, geometry annotation and demo/hub seeds as implemented. Remaining work concerns delivery, real batches, export mapping and verification; implementation claims were not retested by this inventory. |
| Evidence design package version/pin | UI package version is 1.3.0 and gallery already depends on `github:synthet/image-scoring-ui#v1.3.0`. The older unchecked instruction to publish/pin 1.3.x needs reconciliation, not automatic repetition. |
| Recent library evidence completion | The latest skills working status reports current bird-cohort localization/keypoints apart from three terminal corrupt originals, complete CLIP-quality coverage and a refreshed exact-copy audit. These are source-document claims, not checks rerun here; later development-frame gaps and policy gates remain below. |

## Immediate sequence

These recommendations respect existing Stage and ownership; they do not promote or claim issues.

| Order | Next action | Owner and existing record | Observable completion |
|---|---|---|---|
| 1 | Reconcile active delivery before starting overlapping work: resolve conflicting PR #591 and investigate draft skills #4's non-green checks. Preserve the active #694 tooling while reconciling the local checkout with merged #679/#696. | Pipeline/skills; PR list below | Each PR has a documented disposition and relevant current checks; no unrelated local edits are bundled. |
| 2 | Continue the source-current duplicate-study closeout already reported in progress: verify v2, repair the held eleven April rows, then perform the separately bound April v3 replay. | Skills [#5](https://github.com/synthet/image-scoring-skills/issues/5), pipeline [#601](https://github.com/synthet/image-scoring-pipeline/issues/601) | All 10,077 development-frame identities are source-current; reused January/February snapshots verify; preservation and replay receipts exist. This is not permission to launch or interrupt another run. |
| 3 | Resolve the localization promotion prerequisite before judging the frozen fresh sample. | Pipeline [#694](https://github.com/synthet/image-scoring-pipeline/issues/694), [#638](https://github.com/synthet/image-scoring-pipeline/issues/638) | Three judges meet the unchanged 18/20 calibration rule; otherwise retain HOLD. Current record has only one qualified judge. |
| 4 | Reproduce and address the highest-priority Ready work without duplicating in-flight changes. Security #218, missing phase-state #166 and grouping bug #278 are concrete candidates. | Pipeline Ready queue; existing assignees and claim rules apply | A bounded reproduction, scoped fix and targeted regression check for the selected issue. [#253](https://github.com/synthet/image-scoring-pipeline/issues/253) and [#143](https://github.com/synthet/image-scoring-pipeline/issues/143) are also P1 Ready epics, not single small fixes. |
| 5 | Define the next AF geometry conformance increment, preserving the distinction between camera target and anatomical eye. | Pipeline [#322](https://github.com/synthet/image-scoring-pipeline/issues/322), [#325](https://github.com/synthet/image-scoring-pipeline/issues/325), [#423](https://github.com/synthet/image-scoring-pipeline/issues/423) | Tests for all eight EXIF orientations, centre semantics, active-area/rendition transforms and unavailable evidence; independent real-image landmarks before alignment assertions. |
| 6 | Establish independent labels and the consumer contract before crop/fusion or ranking comparisons. | [#415](https://github.com/synthet/image-scoring-pipeline/issues/415), [#645](https://github.com/synthet/image-scoring-pipeline/issues/645), gallery [#176](https://github.com/synthet/image-scoring-gallery/issues/176) | Versioned human-label provenance and grouped splits, explicit input_mode handling, predeclared metrics and adoption thresholds. |

## Remaining work by program

### Localization promotion and Stage 8 retirement

The [current rollout record](https://github.com/synthet/image-scoring-pipeline/blob/master/docs/architecture/pipeline/localization-rollout.md) supersedes older checklist wording where delivery evidence exists.

| Task | State / dependency | Closeout evidence |
|---|---|---|
| #694 judge calibration | **Gated.** R2 is frozen; Antigravity 19/20, Codex and Claude 17/20. Only one meets 18/20; three are required. | Two additional qualifying judges under the unchanged rubric, or a recorded hold/failure. A repaired image-read hook alone does not satisfy judge calibration. |
| Frozen promotion-sample validation | Wait for calibration. The recorded freeze has 390 frames, 130 per size band, excluding 1,467 prior sample/control IDs. | Reproducible rule/sample hashes and unchanged per-stratum thresholds; preserved outcomes and abstentions. No sample replacement after seeing labels. |
| Source-current promotion-cohort reconciliation | Historical issue count 28,475, frozen cohort 30,046 and later skills source-current candidates 30,006 are different dated observations. | Reconcile IDs and source hashes against each bound receipt before reuse; do not silently replace the frozen sample or mix denominators. |
| Promotion tranches | Conditional on passing the fresh gate. | Verified backup, supported selection API, tranche receipts, preserved review state, coverage recount and tested rollback. |
| #638 compatibility-release observation and detector retirement | **Still gated.** A live start or version bump is not a complete compatibility release. | Full observation interval, normalized-read rollback telemetry, sufficient active-selection coverage, then a separately reviewed retirement change. |
| Retry/cascade recovery policy and small-crop species | Reported remaining rollout work. Small-crop precision previously failed: Wilson lower bound 0.8123 below 0.85. | Registered recovery behavior and new predeclared evidence for [#610](https://github.com/synthet/image-scoring-pipeline/issues/610); small stratum remains geometry-only until then. |

### AF evidence, eye quality and inspection

Use the [pipeline AF plan](https://github.com/synthet/image-scoring-pipeline/blob/master/docs/planning/af-focus-evidence.md) and the hub working plan `focus-evidence-synergy-2026-10-23.md`. That separate working-plan document is not included in this inventory publication.

| Task | Owner / prerequisites | Acceptance |
|---|---|---|
| Research AF helper geometry | Pipeline `scripts/research/bird_crop/af_metadata.py`; #322/#325 | Camera-grid centre semantics, eight orientations, crop/active-area offsets and rendition identity are fixture-backed; invalid geometry abstains. |
| Preserve missing-coordinate state and focus-result provenance | Pipeline plan step 3; coordinate contract first | Research JSONL distinguishes point/area/none/unavailable, missing focus result and parse failure. Audit gallery consumers before any stored-contract change. |
| AF/head/eye overlays and matched native crops | Pipeline/gallery/Kestrel, each through its own contracts | Independent landmarks align within predeclared tolerance; missing evidence is explicit; stale source/transform caches invalidate; review flags and selections remain intact. |
| Eye/head versus AF-target measurements | Model/pipeline | Separate anatomical and camera-target identities; pinned provider/run, weight and rendition identities, same-scale noise estimates and sufficient pixels. |
| High-ISO robustness and shadow ranking | #325/#423/#645; independent labels and calibrated geometry | Compare pixels-only, metadata-only diagnostic and combined variants on grouped holdout data; report coverage, false rejects, uncertainty, noise strata and abstentions. |
| Current Kestrel contract reconciliation | Kestrel; dated architecture report is an older baseline | Reconcile current code/spec authority before adding adapters; verify actual bird-eye applicability and natural-image/GPU behavior instead of inferring it from mammal/fallback fixtures. No new Kestrel issue was filed. |

The eleven-frame blur/noise experiment already exists. Repeat it only to answer a new frozen question; neither a constant camera focus result nor AF proximity establishes eye sharpness or redundancy.

### Independent labels, mobile and crop/fusion scoring

Existing epic [#645](https://github.com/synthet/image-scoring-pipeline/issues/645) contains the Stage 6 research program; human-label synchronization is epic [#454](https://github.com/synthet/image-scoring-pipeline/issues/454).

| Task | Existing records / owner | Completion condition |
|---|---|---|
| Count and collect independent burst labels | #415; pipeline/gallery/mobile | Verify actual human provenance, then obtain the approximately 300 stratified bursts needed by the registered study. Auto-cull picks and mirrored metadata are not independent labels. |
| Human labeling sync M1–M6 | Pipeline #455–#460; mobile counterpart | Schema ownership, blind task generation, import/quarantine, hub CLI/contract, end-to-end culling and operational hardening, with milestones verified individually. |
| Production mobile review batches and exports | Mobile working adoption plan | Real review JPEGs and prior-choice metadata; machine export mapping to the model/backend format; offline lease/cache/outbox and type/lint checks. Core screens need reconciliation rather than rebuilding. |
| Shared rendition and representative input evaluation | #406, #568, #570, epic #260 | Current upright pixel/decode provenance, representative aspect/size study and gallery impact gate; reconcile delivered orientation fixes before proposing another fix. |
| Gallery input-mode compatibility | Gallery #176, before pipeline #409 | Consumer filters/adapters handle per-model input modes and baked thumbnail behavior under a documented contract. |
| Crop IQA and interpretable evidence | #409, #423 | Region/input-mode score storage, versioned fusion, crop-only backfill and research JSONL with per-criterion keep/drop decisions. Full-frame production defaults remain until promotion evidence passes. |
| Final experiment campaign | Architecture/focus plan | Natural-image/GPU runtime, local/remote real-model parity, remaining database/repair paths and final held-out replay. Earlier synthetic/CPU comparisons were inconclusive, not production wins. |

### Duplicate research, coverage and guarded application

Use the latest working [skills closeout record](https://github.com/synthet/image-scoring-skills/blob/main/docs/library-dedupe-status.md), skills [#5](https://github.com/synthet/image-scoring-skills/issues/5) and pipeline epic [#601](https://github.com/synthet/image-scoring-pipeline/issues/601). Working status text may be ahead of the linked committed page; its hash is retained in the snapshot.

| Task | Latest reported state | Exit / remaining decision |
|---|---|---|
| Finish development v2 verification | April/February 6,654-file remeasurement reported in progress; January 3,423-file reuse requires unchanged source identity | Verify checksums, measured coverage, exact decision replay and unchanged catalog/source state. |
| Repair eleven held April rows and remeasure April v3 | Eleven stale rows outside the bird-tagged census are explicitly held | Supported exact-ID repair, then separately bound April-only replay; final source-current coverage of all 10,077 development inputs. |
| Missing local score sessions | CLIP-quality reported complete; 494 images still lack matching local-score source sessions | Recover or reconstruct authoritative sessions where possible; otherwise retain unavailable status. Never substitute global IQA or invented local scores. |
| Physical-policy integration and calibration | `paired-physical-v1` is separate from the executor's `local-bird-v1`; historical replay is 24 proposals / 3 strict-margin proposals | Integrate only with version binding, larger labelled positives/negatives, uncertainty/change-control checks and a new run directory. Earlier 26-proposal figures include two invalid prior-removal keepers. |
| Crop, temporal and feature research | Pipeline #603, #605, #606, #607, #627 | Reconcile already completed evidence backfills; evaluate usable eye/head coverage, temporal/linkage alternatives, DINO/SSCD and per-variant keeper coverage on pinned cohorts. |
| Unseen-shoot audit | 523-shoot / 70,218-file queue is advisory and unanalyzed | A separately scoped run and required unseen-proposal audit; no automatic library-wide execution from the existence of the queue. |
| Audited application / deletion requests | Pipeline #602, #628, #637, #644 remain open | Fresh matching evidence, direct retained-keeper proof, protections, supported executor and the task's explicit authorization/backup/rollback requirements. Documentation does not execute them. |

Three terminal corrupt originals remain retained exceptions, not an endlessly retried missing-work queue. The matched test-folder exact copy is also retained because it is outside the qualifying canonical inventory. Historical culling proposals are not applied decisions.

### Remaining tracker programs

The [full register](../reports/unfinished-business-2026-10-26/INDEX.md) contains every open task, including smaller children not repeated here.

| Program | Existing epic/issues | Remaining business and gate |
|---|---|---|
| Remote inference and host separation | Pipeline #435 (M1–M6), #548 (#549–#557), open PR #591 | Resolve the current decoupling PR, distinguish the two architectural tracks, then complete per-request balancing, bounded phase windows, backpressure, culling embeddings, dashboard/MCP, parity, resource and failover evidence. Avoid implementing both tracks as if their storage/execution models were identical. |
| API/DB contracts and security | Pipeline #198, #171, #172, #174, #218; gallery #109, #88, #89, #91 | Reproduce open write-token/transaction findings; explicit atomic or read-only semantics; generated API types, stable DB reads and drift checks. Token values/configuration are not included in this report. |
| Lifecycle, repair and culling correctness | Pipeline #202, #166, #170, #163, #165, #677, #678, #681, #682, #684 | Reproduce current failures, preserve queue/cancel/report contracts, correct pure-function pick-cap coverage and pending-cover recomputation; update stale test expectations without weakening production checks. |
| Eye-model research and retraining review | Model #1; proposed SSL, eye-density and retraining-judge plans; pipeline #323 | Corpus/split provenance, SSL milestones S0–S5, point-versus-density experiment, field calibration, qualified blind review and export/provider compatibility. Student E2 remains behind its recorded human review checkpoint. No training was performed here. |
| Scoring-stack modernization | Pipeline #180/#214 and gallery #94; input-size epic #260 | Reconcile wrappers already landed against live inference gaps, calibration, disagreement diagnostics, old/new evaluation, staged migration, legacy retirement and paired gallery SQL/UI/type tests. |
| Codebase decomposition | Pipeline #289 and gallery #147 | Verify which historical size/refactor children are already implemented, then split remaining hotspots with behavior checks and CI size guards. Original line counts are historical, not current measurements. |
| Evidence viewer delivery | Gallery remaining overlay phases; UI evidence design spec | Mask worker, refresh action, synchronized compare layers, score-breakdown coupling and orientation/parity fixtures; visual regression for chips/legend. Package 1.3.0/pin is already present. |
| Technical failure evidence | Pipeline #143, #144/#146–#149; gallery #83 | Subject-conditioned metrics, labelled classifier decision, optional metrics and UI evidence with explicit unavailable states and human validation. |
| Embeddings and Atlas UX | Pipeline #199, gallery #108, #75/#77–#80 | Scope/filter wiring, color/size/lasso/inspector behavior, projection map, outliers, tag suggestions, smart covers and contract tests. Gallery #73 is marked obsolete: triage rather than implement it literally. |
| Caption/species/domain expansion | Pipeline #118/#150–#155, #413, #420–#422, #449 | Benchmark/freeze additional VL providers, per-tag calibration, species abstention/list gaps, crop applicability and macro routing before activation. |
| Schema and compatibility operations | Pipeline #103/#111/#119, #227, #489/#491; gallery #158 and pipeline #300 | Reconcile migration ownership/version drift, expand-contract retirement, normalized embedding constraints and per-drive sessions. #489 and #491 overlap and need explicit scope consolidation. |
| Manual compatibility QA and branch triage | Pipeline #200/#201/#203, #104–#110, branch-triage children | Complete RAW-preview and Lightroom/XMP checks on intended applications; compare old branches to current master before merging, closing or deleting anything. |
| Framework and pending delivery | Pipeline #574/#301, gallery #159, hub working tree | Inventory existing hook/backup/rename/framework/model-report edits, review coherent groups, validate canonical/generated parity and deliver separately. Setup changes require their existing inventory/review process. |

## Local changes awaiting reconciliation or delivery

These are porcelain-status entry counts at collection start; an untracked directory can represent many files. They are not task counts, and no remote fetch was used to certify all branch ancestry.

| Repository | Branch / HEAD prefix | Local status entries | Remaining action |
|---|---|---:|---|
| Hub | `main` / `0007f8c` | 189 | Separate existing assistant-tree/config/manifest/rename changes, architecture/spec reports and transcript exports. Keep private transcripts out of commits; deliver reviewed groups under #574 where applicable. |
| Pipeline | `release/v9.2.1-localization` / `a5fc3106` | 1 | Release and compatibility work is committed; #696 merged after this branch snapshot. Reconcile the local branch and observation gate; remaining entry is workspace material, not an uncommitted version bump. |
| Gallery | `chore/contract-sync-pipeline-575` / `7e2aa245` | 20 | Review/test the existing DB, IPC, viewer/grid, bridge, file-picker and EXIF-export changes; determine their owning issues and delivery PR. |
| Mobile | `main` / `69f17b77` | 24 | Reconcile task-framework, hub, label engine, settings, fixtures and preview/export changes; run the documented checks before delivery. |
| Model | `docs/dinov3-cookbook` / `95036b33` | 202 | Separate agent/scaffold and documentation edits from heuristic behavior and new evaluation/training-safety tests; targeted tests and model/data provenance are required for the relevant group. |
| UI | `main` / `cf4c1c59` | 9 | Review design/constitution/workflow and shared-helper changes independently of the already-present package version/pin. |
| Skills | `feat/dedupe-keeper-guard` / `bea51636` | 1 | Deliver the updated library closeout document only after the currently reported data/replay results are reconciled. |
| Kestrel | `slice-2-app` / `34aaade5` | 1 | Remaining entry is a transcript export, not proof of unfinished runtime code. The actual remote is `synthet/krestel`; correct the manifest description in a separately scoped metadata change. |

The pipeline and model branch snapshots have no configured upstream. That fact alone does not prove their commits are unpushed. The other snapshots matched their locally recorded upstream refs; this is not a guarantee that remote state cannot have advanced.

## Open PR disposition

| PR | Observed status | Required next action |
|---|---|---|
| Pipeline [#679](https://github.com/synthet/image-scoring-pipeline/pull/679) | Merged; five CI checks passed | No further conflict resolution or merge task. Reconcile local checkouts without overwriting active work. |
| Pipeline [#591](https://github.com/synthet/image-scoring-pipeline/pull/591) | Open, merge state DIRTY/CONFLICTING | Resolve against current master in an isolated checkout, then verify the remote-inference tests and remaining #549 acceptance criteria. |
| Skills [#4](https://github.com/synthet/image-scoring-skills/pull/4) | Draft, merge state UNSTABLE | Inspect the failed/pending checks before deciding design readiness; complete review/validation or retain it as a draft. |

## Documentation, knowledge and queue hygiene

| Task | Required result |
|---|---|
| Reconcile 50 off-board issues and 16 missing stages | Add or classify them through the configured provider when authorized; do not infer Ready from issue age or an empty Stage. Preserve assignments. |
| Resolve #568/#570 stage-label drift | Record the authoritative board stage and align secondary labels through the owner workflow. Current board has both In Progress while labels say backlog. |
| Reconcile historical checklist items with delivery | In particular #638 delivered subparts, mobile shipped milestones, UI 1.3.0/pin, completed evidence backfills and #695/#696. Closing an issue still requires its own acceptance evidence. |
| Triage source markers | The appendix records 311 unchecked documentation items and two potential implementation comments (`modules/metadata_runner.py:481`, `modules/clustering.py:1081`). The two TODO(KEY) comments explain template syntax and are not implementation work. File real gaps only after deduplicating against existing issues. |
| Finish the architecture campaign | Reconcile source drift after frozen baselines, complete the module-level semantic coverage matrix and retain explicit unknown/failed checks. Symbol inventories and passing narrow tests do not certify all modules. |
| Address the broader skills test limitation | The dated campaign recorded Linux path-fixture discovery errors; current skills status reports 163 passed / 17 skipped in a later suite. Reconcile environment and suite scope before declaring the historical failure fixed or rerunning it as an unchanged blocker. |
| Review wiki knowledge | Reviewed-only lookup found no supporting claims. Store stats: 519 candidate, 10 stale, 71 superseded revisions. Existing campaign consolidation is candidate knowledge, not approved requirements. Preserve immutable source/evidence IDs during any later authorized review. |
| Source-root and documentation authority | Earlier direct sibling-spec ingestion was refused by the allowed-root boundary. Use accepted hub summaries or an explicitly reviewed source-policy change; do not treat this as server failure. Reconcile draft/implemented spec authority in the owning repository. |
| Index and activity maintenance | Keep this roadmap, dated register, plan-source hashes and completed-work exclusions consistent when refreshing. Raw session stores, private library membership and unsanitized logs stay out of the public records. |

## Execution and refresh handoff

For an existing issue, first read its current body, assignee and project stage, then compare its proposed behavior with the current source. Claim one Ready item through the provider before implementing. Preserve other branches and working edits. A new unfiled plan item needs owner triage into the existing program rather than an ad hoc TODO queue.

Useful read-only refresh commands, run from the hub or owning repository:

```powershell
gh project item-list 1 --owner synthet --limit 2000 --format json
gh issue list --repo synthet/image-scoring-pipeline --state open --limit 2000 --json number,title,state,url,labels,assignees,projectItems,updatedAt
gh pr list --repo synthet/image-scoring-pipeline --state open --json number,title,url,isDraft,mergeStateStatus
git -C ../image-scoring-gallery status --short --branch
```

Repeat issue/PR queries for every repository listed in the snapshot, including the verified `synthet/krestel` remote. Confirm result limits, closed-state changes, formal hierarchy and board coverage before replacing the inventory. Source markers require the same documented scan exclusions and working-file identity bindings.

Suggested next execution handoff:

> Read this roadmap and the live canonical issue/board state. Select one ready or already-owned task, reconcile it against the current checkout, and state its exact acceptance criteria. Preserve unrelated work. For localization promotion, retain the failed calibration hold until three judges meet the frozen rule. For duplicate research, verify the existing v2/held-row/v3 state before any new run. For AF geometry, begin with conformance fixtures and research observations; production ranking remains a separate evidence-gated decision. Report the actual test results, source identities and unresolved prerequisites.
