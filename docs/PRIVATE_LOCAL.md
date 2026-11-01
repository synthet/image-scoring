---
type: Guide
title: Local private documentation (hub)
description: Where private, operator-local documentation lives and how the hub checks it stays untracked.
resource: docs/PRIVATE_LOCAL.md
tags: [docs, privacy, policy]
timestamp: 2026-10-31T00:00:00Z
okf_version: 0.1
---

# Local private documentation (hub)

Proprietary names, third-party lineage, hashes, and reference inventories belong only under
**`docs/private/`** or **`.docs/private/`** in each ecosystem repo (including this hub). Both paths
are gitignored; never commit their contents.

Hub check: `python scripts/ci/check_private_docs_not_tracked.py`
