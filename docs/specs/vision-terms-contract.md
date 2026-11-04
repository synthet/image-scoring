---
type: Specification
title: Vision terms contract
description: Shared meaning of burst, stack, same moment, sharpness, box format and eye evidence across the image-scoring repositories.
resource: docs/specs/vision-terms-contract.md
tags: [specs, contract, vocabulary, culling, deduplication]
timestamp: 2026-11-03T00:00:00Z
okf_version: 0.1
---

# Vision terms contract

The same words meant different things in different repositories (hub issue #1). This page fixes
their meaning. Each repository keeps its own implementation; when a document, issue or review uses
one of these terms, it means the definition here. Where a repository differs, the table records how.

## Terms

| Term | Meaning | Owner | Current values |
|---|---|---|---|
| **Burst** | Frames separated only by small capture-time gaps; a time grouping, independent of content | Kestrel (`kestrel-py/src/kestrel/bursts.py`) | `DEFAULT_GAP_MS = 500`, allowed 250–3000 ms |
| **Stack** | A pipeline grouping by visual similarity, optionally bounded by a time window; may span several bursts | pipeline (`modules/clustering.py`, `modules/sub_clustering.py`) | `clustering.default_time_gap` defaults to 120 s; distance threshold `clustering.default_threshold` |
| **Same moment** | A measured pair showing the same pose and scene within pose tolerances; a pair relation, not a time window | skills keep-one (`scripts/neardupe_study/experiments/keepone.py`, `docs/keep-one.md`) | tolerances as defined in keep-one; no time gap |
| **Keeper** | The frame retained for a same-moment cluster; every removal has a direct replacement edge to a retained keeper | skills keep-one | protected frames always stay |
| **Soft-cull** | A reversible removal flag; a hard delete is a separate step with the owner's explicit go-ahead | skills `docs/neardupe-softcull-flag.md`; executor in pipeline `scripts/neardupe_maintenance/` | review window per the flag spec |

Do not use "burst" for a stack or for a same-moment cluster. If a statement depends on the grouping,
name it: "Kestrel burst", "pipeline stack" or "keep-one cluster".

## Sharpness

The **canonical sharpness statistic** is the pipeline's noise-corrected Laplacian variance
(`image-scoring-pipeline/modules/focus_quality.py`): Immerkaer noise estimate per 32 px block at
the 10th percentile, with the `20 * sigma^2` white-noise term removed, measured at native
resolution on the subject box with a context ring.

| Repository | Statistic | Status |
|---|---|---|
| pipeline | canonical (above) | owner |
| skills | vendored, pinned copy (`scripts/neardupe_study/library/sharpness.py`) | aligned; drift check in skills#30 |
| model | plain Laplacian variance / 500 on eye crops | **differs**; model#8 |
| Kestrel | gradient detail score; noise scored as a separate penalty | **differs**: noise is not subtracted from detail |

Plain Laplacian variance must not be used as a quality signal: sensor noise can raise it by
orders of magnitude on a defocused region.

## Box format

**Canonical storage** is normalised corners `[x1, y1, x2, y2]` in `0..1`, in the oriented (display)
image, as stored in pipeline `image_regions`.

| Repository | Format | Convert to canonical |
|---|---|---|
| pipeline `image_regions` / `images.bird_bbox` (normalised reads) | normalised `[x1, y1, x2, y2]` | — |
| pipeline `focus_quality.analyze(box=...)` | pixel `(x1, y1, x2, y2)` in the analysed image | divide by that image's width and height |
| model detector (`bird_detector.py`) | normalised `[x, y, w, h]`, oriented image space | `x2 = x + w`, `y2 = y + h` |
| Kestrel | normalised `(x0, y0, x1, y1)` | same as canonical |
| gallery | reads pipeline normalised boxes | — |

Pixel boxes are only valid for the exact image they were measured on. A pixel box from a downscaled
model input does not apply to the original (see pipeline#746).

## Eye evidence

| Term | Meaning | Owner | Current value |
|---|---|---|---|
| **Eye consumer floor** | Minimum keypoint confidence for a consumer to treat an eye as found | pipeline (`EYE_CONSUMER_MIN_CONF`, `modules/keypoints.py`) | 0.8 |
| **Keypoint provider identity** | Which model, detector and settings produced the stored eyes | pipeline (`image_keypoint_runs.provider_version`, `provider_config_hash`) | per run |

The gallery (`EYE_MIN_CONFIDENCE`, `electron/db.ts`) and skills (`EYE_MIN_CONF`,
`scripts/neardupe_study/proposals.py`) hold copies of the floor, so a change must update both.
The owner-labelled review that kept 0.8 is in the model repository's
`docs/reports/eye-model-benchmark-2026-11-03.md`.

A change of model, detector or floor bumps the provider identity, and downstream receipts such as
keep-one record it.

## Change rule

Changing any definition or canonical value here needs a hub issue and a link from the owning
repository's `CANONICAL_SOURCES.md`. Implementation changes stay in the owning repository.
