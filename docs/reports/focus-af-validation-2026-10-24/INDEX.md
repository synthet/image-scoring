---
type: Verification Report
title: Nikon AF validation and container verification
description: Historical AF validation receipts and the completed Docker and Z8 integration checks.
resource: reports/focus-af-validation-2026-10-24/INDEX.md
tags: [verification, nikon, autofocus, docker, tests]
timestamp: 2026-10-26T00:00:00Z
okf_version: 0.1
---

# Nikon AF validation

The pending container build and decoder checks completed on 2026-10-26. The standard pipeline Dockerfile built successfully, and the resulting image reported ExifTool **13.52**.

| Check | Result |
|---|---|
| Standard Docker build | Exit 0; cached dependency and pinned decoder layers reused |
| Decoder version in the built image | Exit 0; ExifTool 13.52 |
| Focused AF/EXIF unit tests | 97 passed, 3 sample-data tests deselected |
| Z8 indexing and metadata integration | 5 passed, 2 ML tests deselected |
| Test-resource cleanup | No remaining task containers or networks |

The [sanitized verification receipt](evidence/verification-2026-10-26.json) records commands, counts, image identity and hashes of the retained local evidence. Raw build logs, JUnit files and session history remain local.

## Verified source and isolation

The image was built from pipeline revision `e787a0392b81038a93b6289b6e16458019c14e88` on `release/v9.2.1-localization`, including pre-existing uncommitted changes to `CHANGELOG.md` and `modules/version.py`. This verifies that working tree, rather than a pristine commit snapshot. The release edits were preserved.

The focused tests ran offline with a read-only container root. Integration tests used five Z8 samples copied by the fixture into temporary storage, and a new `image_scoring_test` database in a disposable PostgreSQL 17 container. Its internal Docker network published no host port. The database and network were removed after the run; the verification image was retained. No existing library database or source photograph was modified.

## Historical validation evidence

- [Focused-test receipt](evidence/green-final.json) — October 24 run: 94 passed, 3 deselected.
- [Frozen Z8 metadata replay](evidence/replay.json) — eleven matching records; not rerun during the October 26 verification.
- [As-built documentation receipt](evidence/documentation-writes.json) — source-document hashes from the earlier increment.

## Remaining research and limits

The [pipeline AF focus evidence plan](https://github.com/synthet/image-scoring-pipeline/blob/e787a0392b81038a93b6289b6e16458019c14e88/docs/planning/af-focus-evidence.md) still requires fixture-backed calibration of all eight EXIF orientations, camera active-area offsets and rendition transforms. Derived AF-state observations belong in research output before schema or ranking changes. The existing eleven-frame robustness experiment already demonstrates sensitivity to added noise, so further evaluation should address high-ISO robustness and retain decoder, keypoint-run and rendition identities.

This verification covers the standard Dockerfile, focused unit tests and five Z8 samples through non-ML integration paths. It does not establish all-camera geometry, calibrated eye-quality ranking, another image recipe, GPU inference, deployment or release readiness.
