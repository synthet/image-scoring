# Wiki activity log

Append-only. One line per wiki restructure, newest under the current month.
Format: `- YYYY-MM-DD: <verb> — <details and paths>` (verbs: `created`, `updated`, `ingested`,
`lint-fixed`, `reorganized`).

## 2026-11

- 2026-11-03: updated — specs/vision-terms-contract.md: added the eye consumer floor and keypoint provider identity (hub #7).

- 2026-11-03: updated — planning/eye-benchmark-fleet-adoption-2026-11-02.md: added the measured fleet eye path and the agreement-rule calibration costs; corrected the claim that the cascade stores both detectors' boxes.

- 2026-11-02: created — planning/eye-benchmark-fleet-adoption-2026-11-02.md: review of model PRs #23 and #24, the finding that production eyes come from the pipeline's unbenchmarked crop path with a 0.8 floor copied in three repos, per-repo adoption, synergies and keep-one plan amendments.

## 2026-10

- 2026-10-29: reorganized — decommissioned nested Git submodules in image-scoring (gallery, mobile, model, pipeline, skills, ui); codified flat sibling checkout layout under D:\Projects; superseded SUBMODULE_DEDUPLICATION_OPTIONS.md, updated LAYOUT.md, added root ignore for image-scoring-*/, and verified clean multi-root workspace passing layout-doctor.

- 2026-10-27: updated — completed the four-step plan: published inventory `d487010`, resolved PR #591 as `6809cc08` with 126 local regression tests and eight CI checks passing, verified existing #694 tooling with 26 tests unchanged, and diagnosed inherited inventory drift in draft skills PR #4 with 30 other tests passing; receipts in reports/execution-2026-10-27/.

- 2026-10-27: updated — prepared the unfinished-business inventory for publication; recorded merged pipeline PR #679, conflicting pipeline PR #591 and draft skills PR #4's non-green check state while preserving the October 26 collection snapshot.

- 2026-10-26: created — consolidated unfinished business across eight repositories: 225 open issues, 22 epic/hierarchy records, three open PRs and 315 explicit documentation/source markers; recorded current gate failures, delivery gaps, completed-work exclusions and sanitized snapshot bindings in planning/unfinished-business-2026-10-26.md and reports/unfinished-business-2026-10-26/. Recorded the later owner-requested PR #679 conflict resolution (`092f39a6`, CLEAN/MERGEABLE, five CI checks passed); review and merge remain open.

- 2026-10-26: updated — completed Nikon AF container verification: Docker build and ExifTool 13.52 checks passed, 97 focused tests and 5 isolated Z8 integration tests passed; published reports/focus-af-validation-2026-10-24/INDEX.md and its sanitized receipt.

- 2026-10-24: updated — completed the focus synergy plan and resumed-checkout verification; model 88, skills 46 and pipeline 72 focused tests passed; recorded 14 wiki candidate claims from three accepted sources, zero canonical errors and completed rendering. Later checkout changes and remaining field-evaluation gaps are explicit in the handoff.

- 2026-10-23: created — model/pipeline/skills synergy research summary and reports index; detailed source-linked consolidation belongs to the shared LLM Wiki Image Scoring bundle.
- 2026-10-23: ingested — shared wiki consolidation added 15 sources and 26 candidate claims with immutable revision locators; canonical validation reported zero errors and candidate-inclusive rendering completed for 143 pages.
- 2026-10-23: updated — recorded the newer sibling architecture campaign, seven source-derived specs, two regression fixes and inconclusive CPU redesign comparisons; added read-only Kestrel review and a Nikon focus evidence enhancement plan with eleven-file metadata evidence and explicit coverage gaps.

## 2026-07

- 2026-07-14: updated — regenerated agent-asset-inventory after skill consolidation (removed diagnosing-bugs/tdd duplicates; added karpathy-guidelines).

## 2026-06

- 2026-06-16: created — initial framework docs (README, INDEX, CANONICAL_SOURCES, OKF_ADOPTION, WIKI_SCHEMA, ai-workflow, security, project).
