---
type: Report
title: Focus campaign knowledge consolidation
description: Canonical source revisions, candidate claims and validation receipts.
resource: reports/architecture-review-2026-10-23/knowledge-consolidation.md
tags: [image-scoring, llm-wiki, evidence]
timestamp: 2026-10-24T15:45:00Z
okf_version: 0.1
---

# Focus campaign knowledge consolidation

Three hub reports were ingested through the canonical local CLI in agent mode. Fourteen quote-bound claims were compiled into the existing `Photo burst eye-sharpness culling` entity. All remain **candidate**; no human review decision or supersession was made. No external provider call was used for this compilation.

| Hub source | Immutable source revision | SHA-256 |
|---|---|---|
| `image-scoring/docs/reports/architecture-review-2026-10-23/INDEX.md` | `f07cd241-dc7c-42fe-ad31-198a1e2107c3` | `216743c7c3fc2186649ae8b1a7c6394afe2de6054be857d2aded6eca871c921a` |
| `image-scoring/docs/reports/architecture-review-2026-10-23/kestrel-as-built.md` | `c5544833-d035-4d57-b7c5-c433890f4511` | `3cb168985486c4430dbae3b9cd573e1fcb7daf65e742f0b2655290120dabad7f` |
| `image-scoring/docs/planning/focus-evidence-synergy-2026-10-23.md` | `74dc45db-61a3-4442-9bf4-2ee44abb4d1e` | `7899afbe8a5e791284f70d4748b6d4c0b44b8ca88e51e0b84e9f688dd652996c` |

## Integrity and retrieval

Canonical validation reported **0 errors**. Candidate-inclusive rendering completed. The first render command encountered a Windows output-encoding error; the UTF-8 retry succeeded. Both receipts remain available.

Three sampled claims were fetched through MCP and retained candidate status, nonempty revision-bound quotes and no review records. Exact locator integrity was checked by the canonical compiler and validator.

Direct sibling-spec imports were refused by the configured source roots. Those roots were not changed and the files were not mirrored to bypass the restriction. The wiki contains source-linked review summaries; full as-built contracts remain in their owning repositories.

Compilation run: `da4d81b8-000d-48ff-8687-52e24ea3dc92`.

Candidate revision IDs:

- `17bfaca1-2d58-49c8-a428-0742ae585cf7`
- `47dbcdea-3a0c-4154-b3c0-943bfd69d2b5`
- `f0d0bbf4-eb00-45f5-9535-9e19fdda1e91`
- `7e21a9cb-f950-450b-85db-71cc22fa5a9d`
- `24dbbfb4-a208-4add-be78-d4ca223e2000`
- `ba99989f-da00-47cb-9694-210538c3c8d8`
- `bc1220f9-4f8f-4424-a913-3b5c369a0a7a`
- `d0eb0f49-0128-4c07-8904-2b050980d107`
- `2318143b-d3ba-4cf5-999e-ea0f7a6c70ea`
- `62b79ccd-0241-42bb-874c-cc7354cdc340`
- `87c5e041-1b97-40e1-aaa9-c262727083bb`
- `9636ae96-6752-456e-9eaf-5f207eb3e85f`
- `c4f1f972-7af9-4455-8cb3-9ca3249f3cfd`
- `f0b98525-533f-4068-bf34-1b44720b1529`

Receipts: `evidence/wiki-ingest-current.json`, `wiki-compilation.json`, `wiki-validation.json`, `wiki-render-utf8.json`, and `wiki-spotchecks.json`. Earlier attempts are retained separately.
