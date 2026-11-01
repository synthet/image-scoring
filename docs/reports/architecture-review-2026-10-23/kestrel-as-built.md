---
type: Report
title: Kestrel architecture and focus integration review
description: Read-only code-derived review of current Kestrel and its focus evidence integration seams.
resource: reports/architecture-review-2026-10-23/kestrel-as-built.md
tags: [kestrel, architecture, focus, as-built]
timestamp: 2026-10-24T03:00:00Z
okf_version: 0.1
---

# Kestrel architecture and focus integration review

Kestrel is a local Python scorer and Electron/React review application. This review observed HEAD
`373330f37425c7ff19359f6765188f0697dbe7a3` plus existing working edits, including `measure.py` and
`session.py`. The snapshot (`evidence/kestrel-snapshot.json`, kept local) records selected file hashes and status after
initial read-only exploration. It is not a pristine commit-only baseline. No Kestrel source or approved spec was changed.

The [integration plan](../../planning/focus-evidence-synergy-2026-10-23.md) proposes future functionality. No Kestrel implementation or scoring policy has changed.

## Existing data flow

`discovery.py` pairs source files; `metadata.py` obtains capture metadata and extracts a RAW preview;
`imaging.py` prepares an upright RGB analysis rendition; `measure.py` records evidence; `scoring.py`
maps that evidence to six criteria and a composite. `pipeline.py` builds the persisted session;
`bursts.py` groups and ranks within bursts. `session.py` preserves review state and supports recomputing
scores from stored evidence. The application exposes inspection, comparison and reweighing through its Python service.

| Surface and source symbol | Observed behavior | Focus integration implication |
|---|---|---|
| `metadata.py:TAGS`, `CaptureMeta`, `_from_exiftool` | Standard timing, ISO, focal lengths, body identity, orientation, keywords; no Nikon AF rectangle, result or distance in this contract | A metadata adapter and explicit compatibility contract are missing |
| `imaging.py:load_rendition`, image preparation | Analysis long edge 1024; EXIF orientation applied to the rendition | Tiny eye detail can disappear; retain source-to-rendition geometry for native crops |
| `models.py:MODELS`, `load_stages` | RTMDet-tiny COCO detector; RTMPose-m AP-10K mammal eyes; U2-Net-p saliency; ONNX providers prefer available GPU then CPU; missing/unloadable stages degrade explicitly | These are registered recipes; this review did not establish local weight identity or field accuracy |
| `measure.py:analyse` | Chooses a subject using detection/detail/area/cut information; falls back to detail estimate; masking is conditional | A user-selected subject and an AF target must remain separate identities |
| `measure.py:analyse` eye branch | Pose called only for `kind == mammal`; highest-confidence eye gets a local gradient window; otherwise subject gradient p98 becomes `source=estimate` | Bird fallback is not anatomically localized eye sharpness; feathers/beak can dominate |
| `measure.py:_keypoints`, working edit | Existing edit persists left/right-eye and nose points with local measurements | Useful inspection detail; it does not add a bird pose provider |
| `scoring.py:Settings`, `evaluate` | Sharpness, eye, exposure, framing, cleanliness and setting; detail curves, confidence/visibility handling, goal settings and display curve | Add separate evidence first; sharing a scalar with pipeline fusion would hide different semantics |
| `bursts.py` grouping and ranking | Default adjacent time gap 500 ms per camera body; locks/pins respected; manual override precedes composite ranking; close leads marked contested | Temporal groups are not physical-equivalence classes; a lead does not authorize rejecting the rest |
| `session.py:rescore`, review setters | Stored-evidence recomputation; scoring revision checks; flags/overrides/pins/locks preserved through their own paths | Strong seam for reproducible policy comparisons without rescanning every source |
| `kestrel_app/peaking.py` | On-demand gradient/texture visualization; measurement resolution capped at 1600 long edge; visual overlays | Useful focus inspection aid, not a calibrated optical focus-plane detector |
| `kestrel_app/diagnostics.py` | On-demand subject/landmark/mask diagnostics using stored evidence and optional models | Natural place for camera-AF and anatomy overlays with independent unavailable states |
| `kestrel_app/reweigh.py` | Preview settings without writing the session; saved settings and named presets handled separately | Shadow comparisons can preserve the user's saved policy and manual decisions |

Source paths above are relative to `kestrel-py/src/kestrel/` unless prefixed `kestrel_app/`, which is
under `kestrel-app/src/`. File-level hashes bind observations to the working files. These sources include
independent Kestrel constants recorded in its ADRs; this report does not propose importing other products' tuning.

## Exact behavior that matters for synergy

The scorer's default criterion weights are sharpness .30, eye .22, exposure .15, framing .15,
cleanliness .10 and setting .08. Its detail curve is `100*m/(m+12)`. These are existing Kestrel values,
not coefficients for a cross-project Nikon policy. Eye localization confidence modifies its keypoint
criterion; an estimated eye has a different evidence source. Missing subject evidence is not a measured eye failure.

Kestrel's mammal pose path uses AP-10K semantics. The model sibling's bird-eye semantics and crop
aggregation differ. An adapter must state species applicability, landmark definition, coordinate frame,
visibility, quality direction/range and fallback. An identically named field or matching vector dimension
does not establish interchangeability. AF-target crop detail should remain a separately named measurement.

Burst ranking and explicit review flags are separate. A contested score gap is a heuristic, not a calibrated
probability of uncertainty. Any proposed suppression needs independent physical comparison, direct keeper
evidence and protections; temporal proximity and similar quality scores cannot establish redundancy.

## Verification and limits

[Focused native CPU tests](evidence/kestrel-tests-native.json): **86 passed, 1 skipped** across scoring,
model adapters, bursts and sessions. Existing synthetic fixtures/fake ONNX sessions exercise contracts;
they do not establish natural-image accuracy or actual GPU inference. The first sandbox attempt had
85 passes, one skip and one Git-ownership failure in the tracked-weight integrity test; rerunning under
the repository owner's Windows identity passed. No Git configuration was changed.

Not exercised: Electron interaction, actual model weights, bird-eye inference, native-NEF optical
sharpness, AF overlay calibration, persistence migration, or any AF-based score/culling policy.
The approved focus-peaking document still labels itself draft while implementation and an ADR exist;
resolve authority through the owner, without rewriting approved text as part of this review.
