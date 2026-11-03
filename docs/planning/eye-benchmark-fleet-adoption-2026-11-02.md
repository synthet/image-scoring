---
type: Plan
title: Eye benchmark fleet adoption plan
description: How each image-scoring repository can use the 2026-11 eye-model benchmark and the two-stage localizer, with review findings and cross-project synergies.
resource: docs/planning/eye-benchmark-fleet-adoption-2026-11-02.md
tags: [planning, eye-pose, keypoints, detection, evaluation, synergy]
timestamp: 2026-11-02T00:00:00Z
okf_version: 0.1
---

# Eye benchmark fleet adoption plan

**Sources:**
- model PR #23: `docs/reports/eye-model-benchmark-2026-11-03.md` in `image-scoring-model`;
- model PR #24: opt-in two-stage localizer, branch `feat/two-stage-eye-localizer`;
- the skills keep-one operations plan (local, not committed).

All of these were read on 2026-11-02 together with the pipeline, gallery, mobile, UI, skills and
Kestrel repositories. Every file reference below was checked in that survey.

**Scope.** This plan only proposes work: each item needs a backlog entry in its owning repository. No production policy, stored keypoint, threshold or library metadata changes as part of it.

## 1. The key fact: production eyes already come from a crop path

The benchmark's "production path" (`A_pipe`: within 5% = 0.49 on library birds) is the model
repository's full-frame `PoseLocalizer.localize_eyes()`. **No production consumer reads that path.**

The eyes the fleet actually stores and shows come from the pipeline:
- `modules/keypoints.py` takes the selected `bird_detect_v1` box, pads it by 25%, runs `eye_pose_v0` on the crop and matches the result back to the box by IoU.
- It runs only through `scripts/backfill_region_keypoints.py`, behind `localization.keypoints.bird_head.enabled`, which is false by default.
- Its output goes to `image_keypoint_runs` and `image_region_keypoints`.
- Consumers keep eyes at confidence ≥ `EYE_CONSUMER_MIN_CONF = 0.8`. That value is copied in three places:

| Copy | Where |
|---|---|
| pipeline | `modules/keypoints.py:53` (API `eye_keypoints`, visual evidence) |
| gallery | `electron/db.ts:2631` (eye overlay, direct SQL) |
| skills | `scripts/neardupe_study/proposals.py:40` (keep-one anchor eyes and the `eye_set_change` veto) |

That path is structurally close to the benchmark's `A_td` (two-stage `eye_pose_v0`: 0.69 within 5%). But its IoU matching and 0.8 floor were **not benchmarked**.

The 0.8 floor itself came from an AI-judged spot check of 110 items (pipeline
`docs/reports/eye-keypoint-spot-check-2026-09-27.md`). The code says it should be re-fitted against owner-checked points. The benchmark's owner labels are the first such points.

This also corrects the owner column in the [vision stack comparison](cross-project-vision-stack-2026-11-01.md): detection and keypoint **models** come from the model repository, but keypoint **inference in production** belongs to the pipeline.

## 2. Review findings on the model PRs

Both PRs merged on 2026-11-03 (UTC). Every finding below still holds on model `main` (`99f50b9`), so each one becomes a follow-up issue.

**Benchmark report (PR #23):**
1. **Framing.** It calls `A_pipe` "what scoring uses". Add the pipeline crop path and its 0.8 floor (section 1) as unmeasured.
2. **Numbers that disagree:**
   - The text says CUB within 2% is "0.74–0.80 for ours"; the table gives 0.699–0.738.
   - The text gives library AUROC as 0.58–0.81; check this against the table.
3. **Latency.** The per-image timings (two-stage 82 ms vs `A_pipe` 215 ms) disagree with the production table's "about 2×". Explain both.
4. **"The design, not the model."** Two-stage scores 0.69 [0.57–0.82] and the external model 0.55 [0.43–0.69]; the intervals overlap. Add a paired bootstrap on the difference, or soften the claim. The no-subject false-eye rates rest on 21 frames, so give frame counts.
5. **Older cameras.** "D300 and DJI gave no flagged frames" is probably partly the decoding failure in finding 13, so say so. The pipeline decodes D300 NEFs through exiftool `JpgFromRaw` and then rawpy (`modules/localization.py:274-302`). Reuse that route for improvement #7.
6. **Size bands** come from the largest detector box, and the report shows many detector boxes are false. Note this.
7. **Date.** The report is dated 2026-11-03; the work is from 2026-11-02.
8. **Teacher identity.** The committed report gives the external teacher's architecture, point count, heads and file sizes. Generalise them so the private identity stays under `docs/private/`.

**Two-stage localizer (PR #24):**
1. **Bug, add a test.** `localize_eyes` takes `detections[0]`, ordered by detector confidence, even when the pose step on that crop returned no keypoints. Two-stage appends such detections, so a more confident false box (a cat, a deer, a figurine: common, per the report) hides a real bird.
   - Prefer the best detection that has eye keypoints.
   - Add a test with a stub detector that returns two boxes, the top one with no keypoints.
2. **Thresholds.** The detector gate reuses the pose model's `min_bbox_conf`. Give the detector its own threshold so it can be calibrated separately (report improvement #2).
3. **Neighbouring birds.** `max_det=1` on a crop padded by 25% can return a neighbouring bird's keypoints; 9 labelled frames hold more than one bird. Keep the pose result that best overlaps the detector box, as the pipeline does by IoU (`modules/keypoints.py:112`).
4. **Duplicate implementations.** The PR and the pipeline's `keypoints.py` now implement the same idea with different details. See synergy 1.

## 3. Adoption by repository

| Repo | Adopt | Size | Depends on |
|---|---|---|---|
| **model** | Fix the PR #24 items. Add a `pipeline` adapter to `training/eval_eye_benchmark.py` that replays `keypoints.py`, or reads its stored keypoints for the sampled files, and report it with and without the 0.8 floor. Map `bird_pose_15_v0` parts 6 and 10 into the 6-point schema (owner decision). Fix older-NEF preview decoding. | M | — |
| **pipeline** | (a) Re-fit `EYE_CONSUMER_MIN_CONF` on the calibration sample `field_eye_calib_v1`, never on the 147-frame test set. (b) A YOLO + RTMDet agreement rule: `modules/localization_cascade.py` already stores both detectors' boxes, and `iou()` (`:47`) can be reused. In the benchmark, frames where only `bird_detect_v1` fired held no bird in 48 of 54 cases. (c) An optional `bird_head.model_file` swap to `bird_pose_15_v0` with an eye-index map and a `provider_version` bump. (d) Correct the backend-integration guidance: the model repo's guide still describes an `EYE_QUALITY` phase that was never built. | M | model adapter (for a and c) |
| **skills** | Keep-one depends on 0.8-floor eyes (`refcull_eye`, anchor eyes, the `eye_set_change` veto), so re-check it after any floor or model change. The benchmark's 21% false-eye rate on hidden sides is measured at the model's own gates, not at 0.8. See section 5 for the keep-one plan. `/carousel` already treats eye scores as supporting evidence only: no change. | S | pipeline (a)–(c) |
| **gallery** | Stop hardcoding the 0.8 floor in `electron/db.ts`. Take eyes or the floor from the pipeline API (`GET /api/images/{id}` already returns filtered `eye_keypoints`). Show an "unreliable eye" state instead of dropping the eye silently. | S | hub contract |
| **ui** | Add codes to `src/constants/evidenceDisplay.ts` for a low-confidence eye and a non-bird subject. `small_subject_second_pass` and `head_unverified` already exist. Reuse the `keypointOccluded` / `experimental` tokens for the style. | XS | — |
| **mobile** | The cheapest source of eye ground truth at scale: a `presence` or `box_quality` task with `secondaryAsset: 'eye_crop'` ("is this a real, visible eye?") measures false eyes on hidden sides with no schema change. Point labels would need a new `geometry.points` answer field. | S / M | — |
| **Kestrel** | Read-only behaviour evidence only (its AGENTS.md and ADR-0056): ONNX-only runtime, open checkpoints, and no naming of other applications' private weights. Useful to it: the detector-agreement result; the gap between CUB and the library; the benchmark method (PCK by box diagonal, thresholds frozen on a public set, bootstrap intervals) for its Spec 04; and scoring its mammal pose stage on the owner's 70 labelled non-bird subjects. | S | — |
| **hub** | Add the eye-confidence floor and keypoint provider identity to the [vision terms contract](../specs/vision-terms-contract.md). Ingest the **committed** report into the LLM wiki; never `docs/private/`. | XS | — |

## 4. Synergies

1. **One eye path.** Converge the model repository's two-stage localizer and the pipeline's `keypoints.py`. Either the pipeline builds `PoseLocalizer` with a crop detector, or the model repository declares the pipeline path canonical and benchmarks it. Either way, the benchmark then measures what every consumer reads.
2. **One floor, published once.** Re-fit the 0.8 floor once on the calibration sample and expose it through the API and the contract. The gallery overlay, visual evidence and keep-one then improve together, and no copy drifts.
3. **Detector agreement fixes three problems:**
   - false boxes (cats, deer) carried into two-stage;
   - keep-one's 1,479 frames with no detection: the cascade already runs RTMDet only on YOLO `no_detection` frames, and 966 of those frames sit within 1 s of a localized neighbour, which gives a gate;
   - moving the pipeline cascade from shadow to active.
4. **Shared labelling.** These collect overlapping ground truth: boxes, eye presence and verified negatives.
   - the model repository's `training/label_eyes/` page;
   - mobile `eye_crop` presence tasks;
   - the pipeline's `scripts/research/detector_benchmark/` label page.

   Keep one negatives set (`verified_negatives_v1` and the pipeline's frames with no bird keyword) and one exclusion manifest, so a test frame never enters calibration.
5. **Non-bird coverage as one thread:**
   - keep-one Phase 6.1 (non-bird shoots currently yield 0 removals);
   - the benchmark's 70 labelled non-bird subjects (cats, deer, squirrels and others);
   - Kestrel's mammal pose stage.

   The 70 subjects serve as an evaluation set only.
6. **Change control.** Any keypoint model, detector or floor change in the pipeline bumps `provider_version` / `provider_config_hash`. Keep-one's input identity check (section 5, item 2) then catches it.

## 5. Keep-one operations plan: amendments

1. **Hold-out gate feasibility.** The retrospective's own analysis says a tied pair cannot pass `judged_correct`.
   - Decide before the sealed set is pinned whether Jev-resolved ties are excluded from the sealed 100.
   - Run the gate as soon as 100 sealed removals exist, before the full-library run finishes.
2. **Input identity.** The frozen engine hash does not cover the pipeline's detector and keypoint runs. Record their `provider_version` / `provider_config_hash` distribution and the detector hash in every receipt and in the drift guard.
3. **New imports.** Keypoints are a backfill script, not a pipeline phase. A nightly run on new shoots must run localization and the keypoint backfill first, or keep-one sees no eyes.
4. **Second detector.** The pipeline cascade already provides the "second detector on `no_detection` frames": run it, shadow only, before building anything new.
5. **Runner.** The runner is a hardcoded Docker path. Move it into configuration.
6. **External export.** The judge pages send photo crops to external CLI providers. Record that approval in the gate receipt.
7. **Owner labels.** State whether the benchmark's owner labels may serve as read-only evaluation for non-bird coverage. The plan's calibration rule forbids using them to calibrate.

## 6. Order, low-hanging first

| Order | Item | Repo | Size |
|---|---|---|---|
| 1 | PR #24 shadowed-bird fix, its test and a separate detector threshold | model | S |
| 2 | Fix the PR #23 report (section 2) | model | XS |
| 3 | `pipeline` adapter in the benchmark: measure the production eye path | model | S–M |
| 4 | Keep-one plan amendments (section 5) | skills | XS |
| 5 | Run the cascade on keep-one `no_detection` frames, shadow only (scope of pipeline#627) | pipeline + skills | S |
| 6 | Floor and provider identity in the vision terms contract | hub | XS |
| 7 | Re-fit the floor on `field_eye_calib_v1`; publish it through the API; gallery and skills read it | pipeline, gallery, skills | M |
| 8 | YOLO + RTMDet agreement rule, calibrated on the calibration sample | pipeline | M |
| 9 | Mobile `eye_crop` presence tasks for false-eye ground truth | mobile | S |
| 10 | `bird_pose_15_v0` as the keypoint model (owner decision) | model + pipeline | M |
| 11 | UI codes and the gallery "unreliable eye" state | ui, gallery | S |
| 12 | Non-bird eyes: Kestrel mammal stage on the 70 labelled subjects | Kestrel (read-only use of the model repository's local labels) | S |

These rules apply to every item:
- the 147-frame sample stays a test set;
- calibration uses `field_eye_calib_v1` with its exclusion manifest;
- new behaviour starts opt-in or shadow-only;
- consumers see a changed model or threshold through a version bump.
