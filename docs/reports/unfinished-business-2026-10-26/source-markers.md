---
type: Inventory
title: Unreconciled source and documentation markers
description: Comment TODO markers and unchecked documentation items requiring owner triage.
resource: reports/unfinished-business-2026-10-26/source-markers.md
tags: [backlog, inventory, unfinished, audit]
timestamp: 2026-10-26T00:00:00Z
okf_version: 0.1
---


# Source and documentation markers

[Roadmap](../../planning/unfinished-business-2026-10-26.md) · [Issue register](INDEX.md)

These are **unreconciled markers**, not a second task queue and not a claim that every line is unfinished implementation. Acceptance checklists, examples outside code fences, test scaffolding and stale plans can all produce hits. Map real work to an existing issue before opening a new one; close or update stale documentation through its owning repository.

Scope: comment TODO/FIXME/HACK/XXX markers in product, scripts and tests; unchecked Markdown items outside code fences. Archives, historical reports, private/local notes, generated/runtime trees, dependency folders and fixture trees are excluded. Only UTF-8 text files smaller than 1 MB are scanned. This is explicit-marker coverage, not a semantic audit of every unfinished sentence.

Paths and line numbers identify the current working files; uncommitted files may differ from their repository HEAD.

Two TODO(KEY) comments in the secret-detection helpers describe placeholder syntax; they are examples, not implementation tasks.

| Repository | Source files scanned | Documentation files scanned | Markers |
|---|---|---|---|
| hub | 53 | 29 | 6 |
| pipeline | 1288 | 272 | 227 |
| gallery | 277 | 79 | 77 |
| mobile | 64 | 5 | 0 |
| model | 65 | 39 | 0 |
| ui | 30 | 11 | 4 |
| skills | 121 | 41 | 1 |
| kestrel | 58 | 25 | 0 |

## hub — 6 markers

| Kind | Working-tree location | Marker requiring triage |
|---|---|---|
| unchecked documentation item | `docs/security.md:37` | No secrets, tokens, or credentials in the diff. |
| unchecked documentation item | `docs/security.md:38` | New inputs validated; injection/path-traversal considered. |
| unchecked documentation item | `docs/security.md:39` | No new undocumented network calls or secret-storage locations. |
| unchecked documentation item | `docs/security.md:40` | Side-effecting actions gated behind confirmation/approval. |
| unchecked documentation item | `docs/security.md:41` | Logs/outputs redact sensitive values. |
| TODO | `scripts/ci/secret_detection.py:49` | TODO(KEY) markers |

## pipeline — 227 markers

| Kind | Working-tree location | Marker requiring triage |
|---|---|---|
| unchecked documentation item | `docs/features/planned/fix-thumbnail-generation-spec.md:152` | Submit a run for a folder with existing fully-processed images + new unprocessed files on disk |
| unchecked documentation item | `docs/features/planned/fix-thumbnail-generation-spec.md:153` | Verify metadata phase processes newly indexed images (check &#96;image_phase_status&#96; entries) |
| unchecked documentation item | `docs/features/planned/fix-thumbnail-generation-spec.md:154` | Verify thumbnails are generated (check &#96;thumbnail_path&#96; column and &#96;thumbnails/&#96; directory) |
| unchecked documentation item | `docs/features/planned/fix-thumbnail-generation-spec.md:155` | Verify &#96;/ui/runs/&lt;id&gt;&#96; shows work items for the metadata phase |
| unchecked documentation item | `docs/features/planned/fix-thumbnail-generation-spec.md:156` | Verify re-running a fully-processed folder with no new images completes quickly (skips efficiently) |
| unchecked documentation item | `docs/guides/setup/WINDOWS_WSL_DEPLOYMENT.md:162` | NVIDIA Drivers (Windows) |
| unchecked documentation item | `docs/guides/setup/WINDOWS_WSL_DEPLOYMENT.md:163` | WSL2 Installed |
| unchecked documentation item | `docs/guides/setup/WINDOWS_WSL_DEPLOYMENT.md:164` | Ubuntu User Created |
| unchecked documentation item | `docs/guides/setup/WINDOWS_WSL_DEPLOYMENT.md:165` | Virtual Environment Created &amp; Activated |
| unchecked documentation item | `docs/guides/setup/WINDOWS_WSL_DEPLOYMENT.md:166` | Requirements Installed |
| unchecked documentation item | `docs/guides/setup/WINDOWS_WSL_DEPLOYMENT.md:167` | GPU Verified |
| unchecked documentation item | `docs/planning/database/DB_SCHEMA_REFACTOR_IMPLEMENTATION.md:1198` | &#96;getImages()&#96; with no filters returns same count |
| unchecked documentation item | `docs/planning/database/DB_SCHEMA_REFACTOR_IMPLEMENTATION.md:1199` | &#96;getImages({ keyword: 'X' })&#96; returns same result set |
| unchecked documentation item | `docs/planning/database/DB_SCHEMA_REFACTOR_IMPLEMENTATION.md:1200` | &#96;getStacks()&#96; returns same stacks |
| unchecked documentation item | `docs/planning/database/DB_SCHEMA_REFACTOR_IMPLEMENTATION.md:1201` | &#96;getKeywords()&#96; includes all previous keywords |
| unchecked documentation item | `docs/planning/database/DB_SCHEMA_REFACTOR_IMPLEMENTATION.md:1202` | &#96;getFolders()&#96; lists same folders with matching image_counts |
| unchecked documentation item | `docs/planning/database/DB_SCHEMA_REFACTOR_IMPLEMENTATION.md:1203` | IPC handlers unchanged (no client-side code changes required) |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:112` | Run &#96;scripts/db/phase4_consistency_check.py&#96; against production snapshot |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:113` | Run &#96;scripts/db/phase4_performance_benchmark.py&#96; and document results |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:114` | Identify any remaining Firebird-only code paths for keywords |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:115` | Check Electron &#96;electron/db.ts&#96; for hardcoded column assumptions |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:119` | Audit keyword readers in &#96;modules/db.py&#96;: |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:120` | &#96;get_images_by_folder()&#96; — switch to normalized if not already |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:121` | &#96;get_images_by_folder_and_stack()&#96; — same |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:122` | Tag propagation queries — verify using &#96;IMAGE_KEYWORDS&#96; |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:123` | Gallery filter in &#96;modules/api.py&#96; — same |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:125` | Update &#96;CLAUDE.md&#96;: |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:133` | Test with Electron if applicable: |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:137` | Commit and tag as "feat: normalize keyword queries to PRIMARY source" |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:141` | Add deprecation logging to any remaining legacy reads |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:142` | Update CHANGELOG: "Deprecated: IMAGES.KEYWORDS legacy column; EOL in v7.0" |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:143` | Create GitHub issue: "Remove IMAGES.KEYWORDS in v7.0" with removal tasks |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:147` | Remove &#96;IMAGES.KEYWORDS&#96; column via Alembic migration |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:148` | Remove all Firebird keyword compatibility code |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:149` | Update docs; mark Firebird as unsupported |
| unchecked documentation item | `docs/planning/database/PHASE4_KEYWORDS_DEPRECATION.md:150` | Close deprecation issue |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:209` | Run integration tests with database available |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:210` | Manual WebUI smoke tests |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:211` | Tag and push v6.3.1 |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:212` | Update user-facing docs (README.md) if needed |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:215` | Implement deprecation logging in &#96;modules/db.py&#96; |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:216` | Update CHANGELOG.md |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:217` | Create GitHub issue for v7.0 removal |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:218` | Testing (verify warnings logged) |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:221` | Remove IMAGES.KEYWORDS column |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:222` | Remove legacy read paths |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:223` | Remove Firebird compatibility |
| unchecked documentation item | `docs/planning/database/PHASE4_STATUS_SUMMARY.md:224` | Update docs (mark Firebird unsupported) |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:600` | **Phase 1 (Weeks 1–2)** |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:601` | Create &#96;modules/db/&#96; package |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:602` | Extract &#96;connection.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:603` | Extract &#96;telemetry.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:604` | Update &#96;db.py&#96; re-exports |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:605` | Full test suite pass |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:606` | Zero import regressions |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:608` | **Phase 2 (Weeks 3–6)** |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:609` | Extract &#96;images.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:610` | Extract &#96;folders.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:611` | Extract &#96;stacks.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:612` | Extract &#96;keywords.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:613` | Test isolation for each module |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:614` | Update &#96;db.py&#96; re-exports |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:616` | **Phase 3 (Weeks 7–8)** |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:617` | Consolidate &#96;jobs.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:618` | Add recovery functions |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:619` | State machine tests |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:620` | Integration tests pass |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:622` | **Phase 4 (Weeks 9–10)** |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:623` | Extract &#96;embeddings.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:624` | Extract &#96;backup.py&#96; |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:625` | Final &#96;db.py&#96; → facade refactor |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:626` | Performance benchmarks pass |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:628` | **Phase 5 (Week 11)** |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:629` | Add deprecation warnings |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:630` | Write migration guide |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:631` | Update CLAUDE.md |
| unchecked documentation item | `docs/planning/db-refactor-decomposition.md:632` | Final validation |
| unchecked documentation item | `docs/planning/localization-stage4-slice1-status.md:145` | Run &#96;-m postgres --deselect&#96; for the #336 hang on both &#96;master&#96; and this branch, and |
| unchecked documentation item | `docs/planning/localization-stage4-slice1-status.md:151` | Open a PR with &#96;Closes #387&#96; and move the card to **Review**. |
| unchecked documentation item | `docs/planning/localization-stage4-slice1-status.md:152` | Separate issue: &#96;/task-claim&#96; / &#96;backlog_stage.py&#96; cannot find #387 on the board. The |
| unchecked documentation item | `docs/planning/localization-stage4-slice1-status.md:161` | Work left in &#96;.agent/scratch/localization-stage4&#96; (an older, broader draft on |
| unchecked documentation item | `docs/planning/mcp-search-dispatch.md:459` | &#96;search("why did scoring fail")&#96; returns &#96;diagnostics.get_error_summary&#96; in top 3 |
| unchecked documentation item | `docs/planning/mcp-search-dispatch.md:460` | &#96;dispatch("diagnostics.run_doctor", {"no_gpu": true})&#96; returns doctor JSON envelope |
| unchecked documentation item | `docs/planning/mcp-search-dispatch.md:461` | &#96;dispatch("maintenance.prune_missing_files", …)&#96; **not in registry** or rejected as unknown |
| unchecked documentation item | `docs/planning/mcp-search-dispatch.md:462` | CI validates &#96;action_registry.json&#96; in sync |
| unchecked documentation item | `docs/planning/mcp-search-dispatch.md:463` | Docs describe search → dispatch flow |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:134` | **Gate:** Issue + confirm facade pattern in &#96;modules/db/__init__.py&#96; is current |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:135` | Extract &#96;modules/db/connection.py&#96; — engine routing, pool, ping |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:136` | Extract &#96;modules/db/images.py&#96; — CRUD, queries; include &#96;_build_image_query_components&#96;, &#96;upsert_image&#96; |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:137` | Extract &#96;modules/db/folders.py&#96; — folder tree, &#96;delete_empty_folder_cache_subtree&#96;, &#96;get_folder_phase_summary&#96; |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:138` | Extract &#96;modules/db/stacks.py&#96; — stack membership, clustering helpers |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:139` | Extract &#96;modules/db/jobs.py&#96; — &#96;update_job_status&#96;, phase status (&#96;set_image_phase_status&#96;, &#96;_heal_stale_phase_flags&#96;) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:140` | Extract &#96;modules/db/keywords.py&#96; — normalized keyword sync/read helpers |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:141` | Extract &#96;modules/db/embeddings.py&#96; — embedding read/write batch APIs |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:142` | Extract &#96;modules/db/telemetry.py&#96; — pipeline events, metrics |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:143` | Extract &#96;modules/db/backup.py&#96; — backup/restore helpers |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:144` | Split &#96;_init_db_impl&#96; into per-domain DDL helpers (coordinate with Phase 3 Postgres init) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:145` | Keep &#96;modules.db&#96; import path stable via facade re-exports |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:146` | Run DB-marked tests + integration subset applicable to touched domains |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:147` | Re-run audit; target &#96;db_legacy.py&#96; **&lt;3000 LoC** (interim) then retire monolith — record: ___ |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:160` | **Gate:** Issue; read Alembic head vs inline DDL overlap |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:161` | Extract per-table or per-domain DDL functions (e.g. &#96;images&#96;, &#96;jobs&#96;, &#96;keywords&#96;, &#96;embeddings&#96;, &#96;stacks&#96;) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:162` | Keep &#96;_init_db_transaction&#96; as orchestrator calling domain inits in dependency order |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:163` | Run postgres-marked tests / fresh DB bootstrap smoke test |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:164` | Re-run audit; target &#96;_init_db_transaction&#96; **&lt;200 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:214` | **Gate:** Issue; identify planning vs enqueue vs loop boundaries |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:215` | Extract planning submodule (folder/run selection) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:216` | Extract enqueue submodule (job submission) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:217` | Extract main loop / polling submodule |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:218` | Keep public entrypoints stable (&#96;auto_drive_runs&#96; signature unchanged) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:219` | Run &#96;tests/test_runs_autodrive.py&#96; subset or full file |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:220` | Re-run audit; target file **&lt;1500 LoC**, &#96;auto_drive_runs&#96; **&lt;150 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:243` | Split &#96;_dispatch_to_runner&#96; by job type / phase (**Medium**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:244` | Split &#96;heal_phase_data&#96; by healing pass (**Medium**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:245` | Refactor agent_cull safety + schema validators (**Safe**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:246` | Split culling_analytics &#96;flags.py&#96; / &#96;hierarchy.py&#96; compute functions (**Safe**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:247` | Slim MCP &#96;get_embedding_stats&#96; query blocks (**Safe**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:248` | Move Gradio/status endpoints out of &#96;setup_server_endpoints&#96; (**Safe**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:249` | Chunk &#96;backfill_exif_camera_lens&#96; by EXIF field group (**Safe**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:250` | Continue &#96;webui.py&#96; modularization per &#91;REFACTORING_PLAN.md&#93;(REFACTORING_PLAN.md); shrink &#96;main&#96; (**Medium**) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:251` | Re-run audit; record cleared symbols: ___ |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:269` | _(Optional)_ Split &#96;run_all_musiq_models.py&#96; by model family |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:270` | _(Optional)_ Split gallery generator HTML/data builders |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:271` | _(Optional)_ Split &#96;analyze_phase_status.py&#96; report sections |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:272` | _(Optional)_ Extract shared backup script helpers |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:273` | Re-run audit if any optional phase completed |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:307` | Extract hooks from &#96;RunsBucketsPanel&#96; (filters, bucket state) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:308` | Split &#96;ImageInspectorPage&#96; into inspector panels + data hooks |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:309` | Decompose &#96;ScopeSelector&#96; into subcomponents |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:310` | Extract map layer / geo hooks from &#96;GeoMapPage&#96; |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:311` | Page-level extractions for Runs/Gallery/Db/Folder pages (one page per PR) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:312` | Run frontend unit tests + &#96;npm run design:check&#96; if tokens touched |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:313` | Re-run audit from backend root (includes &#96;frontend/&#96; paths) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:319` | All phases above either complete or explicitly deferred with issue links |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:320` | Full fast pytest: &#96;python -m pytest -m "not gpu and not db and not ml" --ignore=tests/test_probe.py&#96; |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:321` | Optional: &#96;ruff check&#96; on touched modules |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:322` | Re-run combined audit (backend + gallery); confirm no regressions above thresholds except grandfather list |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:323` | _(Optional)_ Add CI step: &#96;python scripts/audit/codebase_size_audit.py --file-min 1000 --fn-min 150 --format json&#96; with non-zero exit on new violations (grandfather list for exempt files/functions) |
| unchecked documentation item | `docs/planning/refactoring/CODEBASE_SIZE_REFACTOR_PLAN.md:324` | Update this document's **Last audit** date and line-count table |
| unchecked documentation item | `docs/planning/scoring-inputs/01-scoring-orientation.md:36` | OR-AC-5: A representative JPEG/RAW sample agrees with gallery display orientation. Include available HE/HE* samples and decoder fallbacks. Record score/ranking changes without claiming rotation-invariant model scores. |
| unchecked documentation item | `docs/planning/scoring-inputs/01-scoring-orientation.md:46` | OR-T-5: Coordinate the RAW-thumbnail double-rotation regression with #406/#418: rawpy may rotate pixels before &#96;generate_thumbnail&#96; copies source Orientation. Extend &#96;tests/test_thumbnail_orientation.py&#96; under that ownership (OR-AC-5). |
| unchecked documentation item | `docs/planning/scoring-inputs/01-scoring-orientation.md:47` | OR-T-6: Run focused pytest in gpu-shell, then sample model inference and gallery grid/viewer checks. Publish evidence and a targeted rerun/rollback procedure (OR-AC-5/6). |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:26` | EV-AC-1: Establish a versioned baseline after orientation/routing fixes, using our own representative portrait, landscape and square photos, JPEG/RAW decode routes, small subjects and extreme aspect ratios. Record sampling and exclusions. |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:27` | EV-AC-2: Verify each active checkpoint's supported input contract from its upstream documentation/code before selecting alternatives. Compare current square padding against valid aspect-preserving/model-native policies. Separate orientation, resize, crop and JPEG-encoding effects. |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:28` | EV-AC-3: Measure per-model score shifts, within-burst rank/pick agreement, latency, memory and decode time. Use human labels where available; do not treat agreement with legacy scores alone as quality evidence. |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:29` | EV-AC-4: Evaluate &#96;modules/rendition_cache.py&#96; specifically for scoring: resolution cap, decode route, JPEG round trip, hit/miss pixel equivalence and provenance. Report which models can consume it safely and which need higher-detail input. |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:31` | EV-AC-6: Any accepted change gets per-model configuration, cache/policy versioning, a limited rollout and targeted rerun/rollback guidance. No automatic removal of padding or full-library rescoring. |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:35` | EV-T-1: Resolve upstream input contracts, select sample strata and record acceptance thresholds before running the comparison (EV-AC-1/2/5). |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:37` | EV-T-3: Compare transformations one at a time, including cache hit/miss and full-source versus cached-source detail. Extend &#96;tests/test_rendition_cache.py&#96; only where a scoring adoption requirement is missing (EV-AC-2/4). |
| unchecked documentation item | `docs/planning/scoring-inputs/03-preprocessing-evaluation.md:38` | EV-T-4: Run real-model inference, report quality/ranking and resource measurements, and inspect the largest portrait/landscape discrepancies (EV-AC-3/4). |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:28` | GA-AC-1: EXIF 1-8, including reflection, display correctly for legacy tagged thumbnails and new upright thumbnails with absent/normal orientation; no double rotation. |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:30` | GA-AC-3: Grid/viewer preserve aspect ratio under contain sizing. Boxes and keypoints are mapped using their declared oriented rendition dimensions and provenance, excluding surrounding padding. Existing backend coordinate schema is retained; no blanket conversion to normalized coordinates is assumed. |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:31` | GA-AC-4: An asymmetric fixture and representative real portrait/landscape samples agree with the backend's corrected scoring orientation. Scene label "portrait" and head-facing direction never drive EXIF rotation. |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:35` | GA-T-1: Extend &#96;src/utils/exportImageBake.test.ts&#96;, &#96;src/utils/nefViewer.test.ts&#96; and &#96;electron/nefExtractor.test.ts&#96; for source-tag fallback, EXIF reflection and once-only rotation (GA-AC-1/2). |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:36` | GA-T-2: Add focused grid/viewer/overlay regression coverage with distinct corner and subject landmarks; compare tagged versus baked variants at identical display dimensions (GA-AC-1/3/4). |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:37` | GA-T-3: Make a minimal gallery fix only for a reproduced compatibility failure. Keep protocol/path loading and scoring backend ownership explicit (GA-AC-1..4). |
| unchecked documentation item | `docs/planning/scoring-inputs/04-gallery-orientation-verification.md:38` | GA-T-4: Run focused Vitest tests, renderer/Electron type checks and visual grid/full-view/overlay inspection alongside backend sample evidence. Attach results to gallery #176 without closing its unrelated score-reader work (GA-AC-1..4). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:300` | #399: fix the truncation bug (agent). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:301` | #414: decide S4-1 to S4-5 (you); run the dry-run legacy import (you). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:302` | #415: collect ~300 labelled bursts (you); the §4.4 count is 0 today, so re-run it as labels arrive (agent). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:303` | #416: timing baseline in gpu-shell (agent). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:304` | #418: measure the portrait-RAW share and its impact (agent). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:305` | B10: add &#96;BOARD_SYNC_TOKEN&#96; and dry-run the label sync (you). |
| unchecked documentation item | `docs/specs/pipeline-streamlining/07-blockers-and-decisions.md:306` | Decide §4.3: sibling table versus a primary-key change (you), before #409 starts. |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:54` | The gateway listens on its own port. The webui stays on &#96;127.0.0.1&#96; (&#96;webui.py:163&#96;). |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:55` | Each worker has its own token, stored hashed in &#96;secrets.json&#96;. Revoking one token blocks that worker only. |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:56` | Gateway endpoints accept &#96;image_id&#96; only. There is no path parameter anywhere, and paths are resolved and checked on the host. |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:57` | &#96;/worker/config&#96; never returns &#96;database.*&#96;, tokens or &#96;get_secret&#96; values. A test enforces it. |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:58` | Postgres role &#96;image_scoring_worker&#96;: no DDL and no &#96;TRUNCATE&#96;; &#96;DELETE&#96; only where the keyword-replace path needs it; &#96;pg_hba&#96; allows the worker's IP only. |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:59` | Optional &#96;sslmode=require&#96; and TLS on the gateway (M6). |
| unchecked documentation item | `docs/specs/remote-gpu-worker/05-rollout-and-testing.md:60` | The worker never uses &#96;/api/db/query&#96; or the &#96;X-DB-Write-Token&#96;. |
| unchecked documentation item | `docs/technical/AGENT_CULL_API_VOCABULARY.md:86` | **Add** &#96;pick_quality_advisory&#96; to &#96;AgentCullCandidateStatus&#96; (missing). |
| unchecked documentation item | `docs/technical/AGENT_CULL_API_VOCABULARY.md:87` | **Add** &#96;advisory&#96; to the **&#96;agent_decision&#96;** union **only** — not |
| unchecked documentation item | `docs/technical/AGENT_CULL_API_VOCABULARY.md:89` | **Remove** &#96;rolled_back&#96; from &#96;AgentCullCandidateStatus&#96; — the backend |
| unchecked documentation item | `docs/technical/AGENT_CULL_API_VOCABULARY.md:92` | **Remove** &#96;payload_built&#96; / &#96;agent_pending&#96; / &#96;agent_done&#96; from |
| unchecked documentation item | `docs/technical/AGENT_CULL_API_VOCABULARY.md:94` | Advisory cards: info styling, no Approve/Mark-safe; optional "View |
| unchecked documentation item | `docs/technical/CULLING_FEATURE.md:204` | Integration test with sample scored folder |
| unchecked documentation item | `docs/technical/CULLING_FEATURE.md:205` | Verify XMP creation for picks/rejects |
| unchecked documentation item | `docs/technical/CULLING_FEATURE.md:206` | Import into Lightroom Cloud and verify ratings |
| unchecked documentation item | `docs/technical/CULLING_REWORK_DESIGN_REVIEW.md:277` | Verify XMP files open correctly in Lightroom Classic |
| unchecked documentation item | `docs/technical/CULLING_REWORK_DESIGN_REVIEW.md:278` | Verify XMP files sync to Lightroom Cloud |
| unchecked documentation item | `docs/technical/CULLING_REWORK_DESIGN_REVIEW.md:279` | Test with various image formats (NEF, CR2, JPEG) |
| unchecked documentation item | `docs/technical/CULLING_REWORK_DESIGN_REVIEW.md:280` | Test with nested folder structures |
| unchecked documentation item | `docs/technical/CULLING_REWORK_DESIGN_REVIEW.md:281` | Test delete operation with locked files |
| unchecked documentation item | `docs/technical/CULLING_REWORK_DESIGN_REVIEW.md:282` | Test resume session after application restart |
| unchecked documentation item | `docs/technical/INBROWSER_RAW_PREVIEW.md:89` | Select NEF in Gallery → Extract Preview → Verify canvas renders |
| unchecked documentation item | `docs/technical/INBROWSER_RAW_PREVIEW.md:90` | Select JPG → Extract Preview → Verify warning message |
| unchecked documentation item | `docs/technical/INBROWSER_RAW_PREVIEW.md:91` | No image selected → Extract Preview → Verify error message |
| unchecked documentation item | `docs/technical/INBROWSER_RAW_PREVIEW.md:92` | Browser console: No JS errors on page load |
| unchecked documentation item | `docs/technical/INBROWSER_RAW_PREVIEW.md:93` | Check "NefViewer: Module loaded" appears in console |
| unchecked documentation item | `docs/technical/STACKS_MANUAL_MANAGEMENT.md:249` | Visual badge overlay on stack thumbnails |
| unchecked documentation item | `docs/technical/STACKS_MANUAL_MANAGEMENT.md:250` | Keyboard shortcuts (Ctrl+G, Ctrl+Shift+G) |
| unchecked documentation item | `docs/technical/STACKS_MANUAL_MANAGEMENT.md:251` | Set cover image manually |
| unchecked documentation item | `docs/technical/STACKS_MANUAL_MANAGEMENT.md:252` | Inline expand/collapse view |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:128` | Use &#96;FakeScoringRunner&#96;, &#96;FakeTaggingRunner&#96;, and &#96;FakeClusteringRunner&#96; |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:130` | Stub DB phase-gate helpers to model success, failure, and cancel states. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:131` | Use per-test callback/event fixtures so cancellation and failures can be |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:135` | Tagging never starts before scoring is marked complete. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:136` | Clustering never starts before tagging is marked complete. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:137` | A scoring failure prevents both tagging and clustering from starting. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:138` | A tagging failure prevents clustering from starting. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:139` | Cancellation propagates to all active runners (each fake runner records |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:141` | Job terminal state is persisted as &#96;failed&#96; or &#96;cancelled&#96; consistently |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:152` | Use &#96;tmp_path&#96; to write temporary &#96;config.json&#96; variants per test case. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:153` | Add factory fixtures that generate minimal-valid config dicts for focused |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:155` | Use parametrized invalid payload fixtures for boundary and type cases. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:158` | Missing required keys raise validation errors with key-specific messages. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:159` | Numeric boundaries reject out-of-range values (e.g., negatives where only |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:161` | Boolean/number/string coercion is explicit and deterministic (accepted |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:163` | Default values are applied only when keys are absent (not when invalid |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:165` | Unknown config keys are either rejected or ignored according to current |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:181` | Reuse Postgres/DB fixtures from &#96;tests/conftest.py&#96; for seeded datasets. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:182` | Add helper fixtures that create mixed folder/status/embedding rows for |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:184` | Use transaction or teardown fixtures to ensure isolation between query tests. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:187` | &#96;get_images_for_scoring()&#96; returns only rows matching each filter |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:189` | &#96;get_scoring_history()&#96; pagination returns non-overlapping pages with |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:191` | &#96;get_similar_images()&#96; orders results by ascending distance (or descending |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:193` | &#96;_sync_image_keywords&#96; and &#96;_backfill_keywords&#96; modify only targeted rows |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:201` | Use a mocked MCP tool registry or test client with deterministic tool outputs. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:202` | Patch DB-dependent helpers so response-shape tests do not require live DB/ML. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:203` | Add shared response-schema assertions (required keys, value types, error format). |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:206` | Tool success responses include required keys (&#96;ok&#96;/&#96;status&#96;/payload keys as |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:208` | Tool error responses use a consistent error envelope and message field. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:209` | DB-independent tools return valid shapes when DB is unavailable. |
| unchecked documentation item | `docs/testing/TEST_IMPROVEMENTS_PLAN.md:210` | DB-dependent tools return predictable error shapes when dependencies fail. |
| HACK | `modules/clustering.py:1081` | Hack: Just use a global trigger that the webui poller checks? |
| TODO | `modules/metadata_runner.py:481` | TODO: A better query would fetch images without metadata IPS done. |

## gallery — 77 markers

| Kind | Working-tree location | Marker requiring triage |
|---|---|---|
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:429` | SQLite database connection and query wrapper |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:430` | Path resolution: WSL → Windows conversion |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:431` | &#96;resolved_paths&#96; table creation and migration script |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:432` | Basic filter query builder |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:433` | Unit tests for path conversion and queries |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:436` | Win32 window creation with two-panel layout |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:437` | Left panel: Filter controls (rating, labels, sliders, dates, keywords) |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:438` | Right panel: Basic list view (details mode first) |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:439` | Filter state management and apply/reset logic |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:440` | Basic pagination controls |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:443` | Thumbnail loading using Windows Shell API |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:444` | Large Icons view mode with virtual scrolling |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:445` | Sorting controls and implementation |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:446` | Selection handling (single/double click) |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:447` | Context menu |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:450` | Double-click handler to open image |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:451` | Temporary navigation folder creation |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:452` | Launch Windows Photos with filtered set |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:453` | Cleanup logic for temp folders |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:456` | Background thread for path verification |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:457` | &#96;resolved_paths&#96; table updates |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:458` | Progress indicator for verification |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:459` | Handle missing/moved files (mark as unverified) |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:462` | Performance profiling and optimization |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:463` | Thumbnail caching (memory + disk) |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:464` | Settings persistence (registry/config file) |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:465` | Error handling and user feedback |
| unchecked documentation item | `docs/features/planned/01-windows-native-viewer.md:466` | Documentation and user guide |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:211` | Add menu event plumbing (&#96;open-processing&#96;) main ↔ preload ↔ renderer. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:212` | Add Processing view route/state in app shell. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:213` | Build Processing page with folder tree reuse. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:214` | Implement phase timeline + cards + global controls. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:215` | Implement worker log panel with buffering/virtualization. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:216` | Connect API/WS adapters and optimistic updates. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:217` | Add tests for state transitions and menu navigation. |
| unchecked documentation item | `docs/planning/04-gradio-to-electron-processing-migration.md:218` | Final parity validation against Gradio Pipeline. |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:100` | **Gate:** Issue; confirm &#96;electron/db/provider.ts&#96; boundaries unchanged |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:101` | Create &#96;electron/db/&#96; modules per table above |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:102` | Keep &#96;electron/db.ts&#96; as barrel re-export (no import churn in &#96;main.ts&#96; / IPC) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:103` | Run &#96;npx tsc -p electron/tsconfig.json --noEmit&#96; + IPC integration tests |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:104` | Re-run audit; target &#96;db.ts&#96; barrel **&lt;300 LoC**, largest domain file **&lt;800 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:116` | **Gate:** Issue; map hook groups (filters, viewer navigation, selection, stacks mode) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:117` | Extract &#96;useGalleryFilters&#96; (or equivalent) hook module |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:118` | Extract &#96;useViewerNavigation&#96; hook module |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:119` | Extract &#96;useSelectionState&#96; hook module |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:120` | Split JSX into subcomponents (toolbar, grid shell, viewer shell) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:121` | Coordinate with &#96;.cursor/skills/gallery-ui/SKILL.md&#96; |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:122` | Add/update Vitest for extracted hooks where behavior is non-obvious |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:123` | Re-run audit; target &#96;AppContent&#96; **&lt;300 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:135` | **Gate:** Issue + explicit regression checklist from EXIF/NEF docs |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:136` | Extract metadata panel subcomponent |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:137` | Extract controls / toolbar subcomponent |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:138` | Extract zoom-pan logic hook |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:139` | Extract export flow subcomponent/hook |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:140` | Run Vitest + manual NEF/EXIF regression pass documented in AGENTS.md |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:141` | Re-run audit; target file **&lt;1000 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:153` | Split route registration by concern (static, API proxy, health, …) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:154` | Keep exported &#96;createServerApp&#96; signature stable |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:155` | Run &#96;npm run test:run&#96; if server tests exist; &#96;npx tsc --noEmit&#96; |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:156` | Re-run audit; target &#96;createServerApp&#96; **&lt;150 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:168` | Split bridge handlers by domain (images, folders, stacks, …) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:169` | Keep &#96;createHttpBridge&#96; return shape stable for consumers |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:170` | Run renderer typecheck + relevant Vitest |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:171` | Re-run audit; target **&lt;150 LoC** — record: ___ |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:183` | Split action dispatch into per-action handler map/functions |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:184` | Rebuild MCP registry if needed (&#96;npm run build:registry&#96; in &#96;mcp-server/&#96;) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:185` | Re-run audit; target **&lt;80 LoC** dispatch shell — record: ___ |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:191` | All phases complete or deferred with issue links |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:192` | &#96;npm run test:run&#96; |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:193` | &#96;npx tsc --noEmit&#96; |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:194` | &#96;npx tsc -p electron/tsconfig.json --noEmit&#96; |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:195` | &#96;npm run lint&#96; (fix only regressions in touched files) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:196` | Re-run gallery audit; confirm no file ≥1000 LoC except grandfather list |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:197` | _(Optional)_ ESLint &#96;max-lines&#96; / &#96;max-lines-per-function&#96; scoped to &#96;electron/&#96;, &#96;src/&#96; with grandfather entries for deferred files |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:198` | Update **Last audit** date in this document |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:202` | Split &#96;registerSyncHandlers&#96; (587 LoC) into thematic register helpers (**Safe**) |
| unchecked documentation item | `docs/planning/CODEBASE_SIZE_REFACTOR_PLAN.md:203` | Split &#96;registerBackupHandlers&#96; (450 LoC) similarly (**Safe**) |

## mobile — 0 markers

No matching markers in the scanned scope.

## model — 0 markers

No matching markers in the scanned scope.

## ui — 4 markers

| Kind | Working-tree location | Marker requiring triage |
|---|---|---|
| unchecked documentation item | `docs/features/evidence-overlays-design-spec.md:44` | Storybook / visual regression for legend and chips |
| unchecked documentation item | `docs/features/evidence-overlays-design-spec.md:45` | Publish &#96;1.3.x&#96;; gallery pins released tag (not only &#96;file:&#96; sibling) |
| unchecked documentation item | `docs/scoring-evidence-tokens.md:22` | Phase 1 — Storybook: legend card, heatmap swatch, chip states |
| unchecked documentation item | `docs/scoring-evidence-tokens.md:23` | Phase 2 — publish &#96;1.3.x&#96;; gallery pins dependency; CHANGELOG |

## skills — 1 markers

| Kind | Working-tree location | Marker requiring triage |
|---|---|---|
| TODO | `scripts/ci/secret_detection.py:49` | TODO(KEY) markers |

## kestrel — 0 markers

No matching markers in the scanned scope.
