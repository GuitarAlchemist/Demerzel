# Source Index

> Append-only ingest queue. See [INGEST_PROTOCOL.md](INGEST_PROTOCOL.md) for workflow.

## Format

```
| Source | Category | Status | Ingested | Pages Touched | Notes |
```

## Ingested Sources

| Source | Category | Status | Ingested | Pages Touched | Notes |
|--------|----------|--------|----------|:---:|-------|
| `tars-v1-chats/` (66 files) | conversations | ingested | 2026-03 | 14+ | Extracted personas, constitution articles, safety frameworks → Demerzel founding artifacts |

## Pending Sources

_None currently pending._

<!-- When adding a new source:
1. Place file in sources/<category>/
2. Add row here with status: pending
3. Run /seldon-research or /demerzel-harvest to ingest
4. Update status to ingested with date and pages_touched count
-->
