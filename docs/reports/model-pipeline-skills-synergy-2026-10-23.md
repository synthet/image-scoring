---
type: Report
title: Model, pipeline, and skills synergy — 2026-10-23
description: Research summary and pointer to the shared evidence-bound knowledge consolidation.
resource: reports/model-pipeline-skills-synergy-2026-10-23.md
tags: [image-scoring, research, integration, llm-wiki]
timestamp: 2026-10-23T00:00:00Z
okf_version: 0.1
---

# Model, pipeline, and skills synergy

The strongest opportunity is a shared subject-evidence workflow: model localization feeds pipeline regions and measurements, which feed skills explanations and editorial decisions; independent human labels evaluate each layer.

The detailed, source-linked report belongs to the shared knowledge bundle at `synthet-llm-wiki/docs/ecosystems/image-scoring/model-pipeline-skills-synergy-2026-10-23.md`. The [LLM Wiki guide](../llm-wiki/README.md) explains how that bundle relates to this hub. This page is the offline summary, not a second living contract.

## Inspected snapshots

These are the nested checkouts requested by the user, not similarly named siblings:

| Checkout under this hub | HEAD | Date |
|---|---|---|
| `image-scoring-model` | `20bae89a25d923c56466fb1a0421572ad291e4a0` | 2026-09-29 |
| `image-scoring-pipeline` | `2269ef1c22481567153254988a9da11f698f5174` | 2026-10-09 |
| `image-scoring-skills` | `0b1c6d323c5c7677576fe079bbcf10d971f3b831` | 2026-10-10 |

## Useful connections

1. **Shared evidence contract:** explicit box format, orientation, selected-region identity, source/rendition hashes, model version, and separate quality/confidence/applicability. Model boxes use `[x,y,w,h]`; pipeline region helpers use corners.
2. **Independent evaluation:** reuse the #415 human-label protocol across model features, crop scoring and skills judgments. Score-derived picks and judge-derived labels are not human ground truth. Blind labels must remain separate from informed judgments.
3. **Pixel preparation reuse:** pipeline crop/rendition helpers can serve detection, pose, species and review exports. Freeze crop pixels and decode routes before attributing a result to a model change.
4. **Read-only explanations and species suggestions:** skills can consume named evidence and limitations while preserving model scores, editorial scores, Jev carousel suitability and manual overrides separately.
5. **Selection-to-edit evidence:** the skills color exporter already supplies ordered-file manifests, XMP/ICC, histograms, source hashes and partial-result checks for reproducible edit advice.

## Findings that constrain the next work

- Eye-teacher training is on hold: the model pilot did not establish approved eye pseudo-labels or human-verified negatives. High-confidence pipeline eye points are not certified precise eye locations.
- Pipeline selected-region keypoints cover 4,401 regions, but Stage 6 crop fusion remains gated. The completed species comparison used 360 names / threshold 0.1; it does not validate the later 369-name / 0.5 policy.
- The October 9 capture-date boundary defect was subsequently fixed in the inspected code using `images.registered_at`; an older rollout table still lists it as open.
- Later wiki sessions extend beyond these checkout dates. Their plans and reported historical outcomes must not silently become current runtime facts. Quantitative benchmark summaries without a traceable evaluation remain unverified.

Primary entry points: [model eye evidence](https://github.com/synthet/image-scoring-model/blob/20bae89a25d923c56466fb1a0421572ad291e4a0/docs/architecture/eye-evidence-spec.md), [pipeline handoff](https://github.com/synthet/image-scoring-pipeline/blob/2269ef1c22481567153254988a9da11f698f5174/NEXT_STEPS.md), [skills decision layer](https://github.com/synthet/image-scoring-skills/blob/0b1c6d323c5c7677576fe079bbcf10d971f3b831/docs/jev-decision-layer.md).

## Consolidation policy

Primary documents and this report are ingested through the wiki CLI, with exact revision-bound candidate claims. No claims are human-approved by an agent. Private-derived transcript details stay in local-only notes. Runtime code, training, jobs, photo files, rollout flags and Git history are outside this research's changes.

Completed consolidation: **15 sources added, 26 candidate claims compiled, zero canonical integrity errors**. Candidate-inclusive rendering completed for all 143 existing entity pages. The source-revision and compilation receipt is `synthet-llm-wiki/wiki/notes/model-pipeline-skills-consolidation-2026-10-23.md`. Targeted OKF lint passed for the hub and shared-bundle pages; sampled claims were fetched through MCP and retained exact quotes and candidate status.
