# Source Ingest Protocol

> Inspired by [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — compile knowledge once, query against compiled form.

## Three-Layer Model

```
Layer 1: sources/          Immutable raw material — never modified by LLM
Layer 2: state/streeling/  LLM-maintained knowledge wiki — courses, departments, research
Layer 3: CLAUDE.md + policies  Schema that governs how Layers 1→2 work
```

**Principle:** Don't re-derive answers from raw sources on every query. Compile sources into Streeling pages once, then query the compiled wiki. Each new source should touch 5-15 wiki pages.

## Source Categories

| Category | Path | Examples |
|----------|------|---------|
| **Conversations** | `sources/chats/` | TARS v1 chats, ChatGPT exports, Claude session transcripts |
| **Articles** | `sources/articles/` | Blog posts, papers, technical references (markdown or PDF) |
| **Explorations** | `sources/explorations/` | Brainstorm outputs, research notes, external repo analyses |
| **Extractions** | `sources/extractions/` | Structured takeaways from sessions (already partially processed) |

## Ingest Workflow

```
1. DROP    — Place raw source in sources/<category>/
2. INDEX   — Add entry to sources/index.md with status: pending
3. DISCUSS — Review source with user; identify key takeaways
4. COMPILE — For each takeaway:
             a. Find relevant Streeling department
             b. Update or create department knowledge page
             c. Update course material if applicable
             d. Add cross-references to related pages
             e. Update department weights if coverage changed
5. LOG     — Append to sources/index.md: status: ingested, pages_touched, date
6. LINT    — Run knowledge-topology lint (staleness-detection policy)
```

**Consumer skills:**
- `/seldon-research` — executes steps 3-4 for investigation sources
- `/seldon-course-pipeline` — executes step 4 for course-worthy material
- `/demerzel-harvest` — batch-processes pending sources daily
- `/demerzel-compound` — identifies session insights that should become sources

## Rules

1. **Sources are immutable.** Never edit a file in `sources/`. If a source needs correction, add a new source that supersedes it.
2. **Every source must be indexed.** An unindexed source is invisible to the knowledge pipeline.
3. **Ingestion is not summarization.** Don't just summarize — cross-reference, contradict, synthesize, and connect to existing knowledge.
4. **One source, many pages.** A single article might update a department overview, create a concept page, add a course module, and flag a contradiction in an existing belief.
5. **Pending sources are a backlog.** Track them. Stale pending sources (>7 days) trigger staleness alerts.

## Quality Signal

A healthy source pipeline shows:
- `sources/index.md` has zero pending entries older than 7 days
- Each ingested source touched ≥3 Streeling pages
- Department weights reflect recent source ingestion dates
- Cross-references grow monotonically (never shrink without explicit archival)
