---
type: Plan
title: CV library report adoption plan
description: What to adopt from the 2026-11-01 Kornia/OpenCV/FAISS culling and dedupe report, what is already built, and what is rejected.
resource: docs/planning/cv-library-report-adoption-2026-11-01.md
tags: [planning, deduplication, culling, kornia, evaluation]
timestamp: 2026-11-01T00:00:00Z
okf_version: 0.1
---

# CV library report adoption plan

Source: a downloaded deep-research report, "Image Culling, Burst Clustering and Deduplication
with Kornia and Related CV Libraries" (2026-11-01, 274 lines; not committed). It is a generic
survey. Most of it is already implemented in the ecosystem, often more rigorously, so this plan
adopts **one study and one measurement**, and records the rest so later reports in the same
series need not be re-assessed from scratch.

## 1. Goal

Done means:

- Every report recommendation has a recorded disposition: already built, adopt, or reject, with
  the reason (section 3).
- The pairwise-wins keeper study (work item B) has a reproducible offline comparison against
  the current keeper rule and a recorded **adopt / reject / inconclusive** decision.
- The focus-measure profiling (work item C1) has a receipt and a go/no-go for a GPU port.
- No production policy, library metadata or stored ranking changes as part of this plan.

## 2. Files and areas

| Repo | Path | Change |
|---|---|---|
| hub | `docs/planning/cv-library-report-adoption-2026-11-01.md` | This plan |
| skills | `scripts/neardupe_study/experiments/keeper_borda.py` | New offline experiment (B) |
| skills | `scripts/neardupe_study/test_keeper_borda.py` | New tests (B) |
| skills | `scripts/neardupe_study/proposals.py` | Read only: `keeper_rank`, `pick_keeper` and `SHARP_TIE` are the baseline |
| pipeline | `scripts/benchmarks/focus_quality_profile.py` | New profiling script (C1) |
| pipeline | `modules/focus_quality.py` | Read only in C1; changed only if C2 is approved |
| pipeline | `tests/test_focus_quality_kornia_parity.py` | New, only for C2 |

## 3. Disposition of the report's recommendations

| Report recommendation | Status | Evidence | Disposition |
|---|---|---|---|
| pHash/dHash, then embeddings, then geometric check | Built | skills `scripts/neardupe_study/signals.py` (`phash_dhash`, SSCD, DINOv2, aligned SSIM, `stage_gate`) | Already built |
| LightGlue/LoFTR + RANSAC verification | Built | `signals.py` `matcher()`: DISK + LightGlue, `cv2.USAC_MAGSAC` homography, returns `1 - inliers/n`; gate floor 0.5954 evaluated (`gate-lightglue.txt`) | Already built and measured |
| ResNet-50 embeddings | Weaker than in use | SSCD for copies, DINOv2/DINOv3 for visual similarity | Reject |
| FAISS index | Covered | pipeline pgvector + HNSW | Reject: a second index adds nothing at library scale |
| ImageHash library | Covered | own pHash/dHash in `signals.py` | Reject |
| Laplacian-variance blur score | Weaker than in use | pipeline `modules/focus_quality.py`: noise-corrected Laplacian variance with Immerkaer noise estimation (plain variance moved 0.019 to 4435 under noise) | Reject the naive metric |
| Weighted composite `w1*blur + w2*faces + ...` | Contradicts audit findings | 2026-10-23 architecture review: normalization discontinuity, model redundancy; ranking, suppression and editorial fit kept separate | Reject |
| YuNet faces, Detectron2 | Not applicable | wildlife: RTMDet/YOLO, bird/head/eye localization, BioCLIP | Reject |
| SSIM "most central frame" tie-break | Weaker than in use | physical gate, keeper policy, judge panels, Jev | Reject |
| Time-based burst grouping | Built | Kestrel 500 ms gap; pipeline stacks | Already built |
| Burst alignment and merge (HDR+, denoise) | Out of scope | the ecosystem selects frames, it does not synthesize them | Reject |
| DALI, PyTorchVideo | Not needed | no video; decode reuse tracked separately | Reject |
| AVA, Deep1B, Copydays benchmarks | Mostly mismatched | evaluation uses frozen capture-group splits and human-blind labels | Reject; Copydays optional (D) |
| **Pairwise wins / Borda ranking for ties** | **Not built** | `pick_keeper` breaks sharpness ties by score order only | **Adopt as study B** |
| **Batched GPU (Kornia) filters** | **Not measured** | `focus_quality.py` runs NumPy convolutions per crop | **Adopt as measurement C1** |

Report errors to note when citing it: SIFT's patent expired in 2020; LightGlue is trained on
SuperPoint/DISK/ALIKED features, not SIFT/HardNet; the blur sketch negates the variance and then
calls larger values sharper; the YuNet snippet does not run as written; `pretrained=True` is
deprecated in torchvision; Deep1B is an ANN benchmark, not a duplicate benchmark; the "10–100x"
GPU speedups are unsourced; the Mermaid labels contain unquoted parentheses and do not render.

## 4. Approach

### B. Pairwise-wins keeper study (skills, offline only)

1. Freeze the inputs: the labelled same-moment clusters used by the keep-one experiments, the
   per-frame signals (sharpness, `score_general`, `score_technical`, eye-quality where present),
   `SHARP_TIE`, and the code revision. Record the label provenance (human-blind, judge-derived or
   historical approval) and keep the classes separate in every result.
2. Implement `keeper_borda.decide(cluster, signals)`:
   - Protected frames win, exactly as `pick_keeper` does.
   - Outside the `SHARP_TIE` margin, the sharpest measured frame wins, as today.
   - Inside the tie set only, each ordered pair (i, j) is compared on each signal with a
     per-signal margin; the larger value wins that signal; a missing value or a difference
     inside the margin casts no vote. A frame's points are its pairwise wins. Most points wins.
   - A points tie, or a cycle, falls back to the current `keeper_rank` order.
3. Compare against `pick_keeper` on the frozen clusters: agreement with labelled keepers,
   number of flipped keepers, flips by label class, and the denominator of tie clusters.
4. Decide: **adopt** only if agreement improves on held-out shoots with no flip on protected or
   direct-keeper invariants; **inconclusive** if fewer than 30 labelled tie clusters exist;
   otherwise **reject**. Use Jev only for disputed individual flips, over sanitized summaries.
5. Record the decision in `image-scoring-skills/docs/` and, if adopted, propose a versioned
   keeper policy (e.g. `keeper-v2-borda`) behind the existing consumer gates. Activation is a
   separate, owner-approved change.

### C. Focus-measure profiling (pipeline)

- **C1 (measurement):** profile `focus_quality.analyze` on a frozen sample of 200 crops on the
  GPU host, reporting median and p95 per crop and its share of the metadata/scoring phase wall
  time. **Go** for C2 only if the focus step is at least 15% of that phase or above 20 ms per
  crop; otherwise record no-go and stop.
- **C2 (only on go, separate approval):** add a Kornia batched implementation behind a config key
  that defaults to the NumPy path, with numerical parity tests. No change to stored values.

### D. Copydays SSCD sanity check (optional, deferred)

Needs an external dataset download and a license check. It says nothing about wildlife accuracy.
Do not start without owner approval.

## 5. Constitution check

- **Owning repos:** the study belongs to `image-scoring-skills`, the profiling to
  `image-scoring-pipeline`; the hub holds only this plan.
- **Backlog:** create one issue per work item (skills: B; pipeline: C1) and claim it before
  starting. Creating issues is a remote write and needs approval.
- **Coordination:** the skills checkout is on `feat/neardupe-keep-one` with another session's
  work. Use a separate branch or worktree from the default branch and check with that session
  before touching `scripts/neardupe_study/`.
- **Evaluation discipline:** frozen splits, capture-group separation, label classes kept
  distinct, denominators and uncertainty reported; synthetic results never stand for natural
  images.
- **Safety:** no production policy activation, no library metadata writes, no soft-culls, no
  external data export (D needs approval), no secrets in receipts, no prohibited terms anywhere.
- **GPU:** one workload at a time; C1 is short and read-only.

## 6. Tests (write first, see them fail)

`image-scoring-skills/scripts/neardupe_study/test_keeper_borda.py`:

| Test | AC |
|---|---|
| `test_protected_frame_always_wins` | AC-3 |
| `test_clear_sharpness_lead_matches_pick_keeper` | AC-3 |
| `test_tie_set_resolved_by_pairwise_wins_across_signals` | AC-2 |
| `test_points_tie_falls_back_to_keeper_rank` | AC-4 |
| `test_cycle_falls_back_to_keeper_rank` | AC-4 |
| `test_missing_or_within_margin_signal_casts_no_vote` | AC-4 |
| `test_result_is_independent_of_member_order` | AC-4 |

`image-scoring-pipeline/tests/test_focus_quality_kornia_parity.py` (C2 only):
`test_sharpness_matches_numpy_within_tolerance`, `test_noise_sigma_matches_numpy`,
`test_batched_equals_per_crop`, `test_default_config_uses_numpy_path`.

Acceptance criteria:

- **AC-1:** this plan passes `okf_lint` and the prohibited-term scan.
- **AC-2:** inside a sharpness tie, the frame winning most pairwise signal comparisons is chosen.
- **AC-3:** protected frames and clear sharpness leads give the same keeper as `pick_keeper`.
- **AC-4:** ties, cycles, missing signals and member order never produce an arbitrary keeper.
- **AC-5:** the comparison report lists denominators, flips by label class and the decision.
- **AC-6:** the C1 receipt records sample, hardware, per-crop timings, phase share and go/no-go.

Commands: skills `python -m pytest -q scripts/neardupe_study/test_keeper.py scripts/neardupe_study/test_keeper_borda.py`
and `ruff check scripts/neardupe_study`; pipeline per its `AGENTS.md` (ruff + the focused pytest subset).

## 7. Task breakdown

Run `/tasks` before implementation: the work spans two repos, two backlog items and a gated
second phase (C2).

## 8. Rollback and flags

- B is offline; nothing to roll back. Any adopted policy ships as a new versioned policy behind
  existing consumer gates, with the current rule remaining the default.
- C2, if built, sits behind a config key defaulting to the NumPy path; reverting is flipping the
  key or reverting the commit. Stored focus values are never rewritten.

## 9. Task breakdown

Discovery during `/tasks`: keep-one (`scripts/neardupe_study/experiments/keepone.py`) is label-free
and already accepts `decide(rows, signals, frames, tie_choices=None, policy=None)`, and
`e0.load_rows` refuses shoots whose engine hash differs from the frozen run. B is therefore built
as a keep-one policy variant replayed on the frozen shoots, not as a separate keeper module.
Keeper labels live elsewhere (owner-applied soft-cull manifests read by `decided_state`, judge
panels, Jev tie answers), so the first task counts them by class.

### Traceability

| AC | Tasks | Verification |
|---|---|---|
| AC-1 | T-1 | `python scripts/okf_lint.py --profile project docs`; prohibited-term scan |
| AC-2 | T-5, T-7 | `test_tie_set_resolved_by_pairwise_wins_across_signals` |
| AC-3 | T-5, T-7 | `test_protected_frame_always_wins`, `test_clear_sharpness_lead_matches_pick_keeper` |
| AC-4 | T-5, T-7 | the three fallback/no-vote/order tests |
| AC-5 | T-4, T-8, T-9 | comparison report with denominators, flips by label class, decision |
| AC-6 | T-10, T-11 | C1 receipt JSON and go/no-go note |

### Tasks

| ID | Role | Repo / files | Depends | AC | Verification / evidence |
|---|---|---|---|---|---|
| T-1 | hub agent | hub `docs/planning/cv-library-report-adoption-2026-11-01.md` | — | AC-1 | lint exit 0, term scan 0 |
| T-2 | owner | GitHub: one issue in `image-scoring-skills` (B), one in `image-scoring-pipeline` (C1), each linking this plan | T-1 | — | done: [skills #24](https://github.com/synthet/image-scoring-skills/issues/24), [pipeline #738](https://github.com/synthet/image-scoring-pipeline/issues/738) |
| T-3 | skills agent | coordinate with the session on `feat/neardupe-keep-one`; create a worktree from the default branch, or from that branch once merged | T-2 | — | `git worktree list`; peer reply recorded |
| T-4 | skills agent | read-only inventory: labelled tie clusters per frozen shoot, split by label class (owner-applied, judge, Jev); `scripts/neardupe_study/experiments/keeper_borda_inventory.py` | T-3 | AC-5 | JSON counts; stop with **inconclusive** if fewer than 30 labelled tie clusters |
| T-5 | skills agent | write failing tests `scripts/neardupe_study/test_keeper_borda.py` (7 tests, section 6) | T-3 | AC-2..4 | `pytest -q scripts/neardupe_study/test_keeper_borda.py` fails for the missing policy |
| T-6 | skills agent | add a `pairwise-wins` policy to `experiments/keepone.py` (or `experiments/keeper_borda.py` called through `policy=`); current policy stays the default | T-5 | AC-2..4 | — |
| T-7 | skills agent | make T-5 pass; run the existing keeper/keep-one tests unchanged | T-6 | AC-2..4 | `pytest -q scripts/neardupe_study/test_keeper.py scripts/neardupe_study/test_keeper_borda.py scripts/neardupe_study/test_experiments.py -k "keeper or KeepOne"`; `ruff check scripts/neardupe_study` |
| T-8 | skills agent | replay both policies on the frozen shoots via `e0.load_rows` (engine hash must match); report agreement, flips, flips by label class, denominators | T-4, T-7 | AC-5 | report JSON + markdown under `work/` (not committed) and a summary in `docs/` |
| T-9 | skills agent + owner | decision adopt / reject / inconclusive per section 4; Jev only for disputed flips over sanitized numbers | T-8 | AC-5 | decision recorded in `image-scoring-skills/docs/` |
| T-10 | pipeline agent | `scripts/benchmarks/focus_quality_profile.py`: frozen 200-crop sample, `focus_quality.analyze` median/p95, phase share | T-2 | AC-6 | receipt JSON with sample hash, hardware, timings |
| T-11 | pipeline agent + owner | go/no-go for C2 (>= 15% of the phase or > 20 ms per crop) | T-10 | AC-6 | note on the C1 issue |

### Execution order

1. Setup: T-1, T-2, T-3.
2. Discovery and tests first: T-4 and T-5.
3. Implementation: T-6, T-7.
4. Validation: T-8, T-9.
5. In parallel with 2–5: T-10, then T-11.

### Parallelization

- B (T-3..T-9) and C1 (T-10, T-11) touch different repos and can run concurrently.
- T-10 uses the GPU host: run it only when no other GPU workload is active, one workload at a time.
- T-4 can end B early (inconclusive) before any implementation.

### Definition of done

- AC-1..AC-6 have evidence as listed.
- Skills: the T-7 test and ruff commands are green, and the existing keep-one tests pass unchanged.
- Pipeline: its `AGENTS.md` ruff and focused pytest subset are green for any touched file.
- No production policy, library metadata or stored value changed.

### Out-of-scope follow-ups

- C2 Kornia port (only after a T-11 go and separate approval).
- D Copydays check (needs a dataset download and approval).
- Activating any adopted keeper policy (separate owner-approved change).
