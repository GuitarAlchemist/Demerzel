# Streeling: 25 project-useful courses per department

Status: first curriculum slice, 2026-10-04. Source of record: `state/streeling/courses` in Demerzel. The Learn site is a synced publication, not the editing surface.

## Outcome and counting rule

Each of the 21 departments should eventually have 25 distinct modules that help a learner understand, test, build, or make a decision in the GuitarAlchemist ecosystem. A title, outline, translation, or generated page alone does not satisfy the outcome. Count a module as **ready** only when it has a specific project question, a checked project artifact or reproducible fixture, at least one exercise with an answer, source and limitation notes, a review record, and the required localizations. Keep published count and reviewed count separate.

The inventory below is from Demerzel `origin/master` at `fcaecf9` on 2026-10-04, counting English module files and excluding `README.md`. It has 65 files; the target is 525, leaving 460. The public Learn page was synced from an earlier commit and lists 64. These are inventory counts, not quality verdicts.

| Department | English modules | Remaining to 25 | Project-specific course spine |
|---|---:|---:|---|
| Audio Engineering | 1 | 24 | Recording, signal chains, measurable sound quality, and GA audio output |
| Cognitive Science | 1 | 24 | Ear learning, feedback, cognitive load, and evaluation bias |
| Computer Science | 2 | 23 | GA parsers and services, IX algorithms, TARS grammars, and agent boundaries |
| Cybernetics | 3 | 22 | Gaia/Demerzel feedback, lane transitions, stability, and control evidence |
| Data Visualization | 0 | 25 | Honest quality trends, embeddings, graphs, and accessible dashboards |
| Futurology | 1 | 24 | Bounded scenarios for technical decisions, with explicit falsifiers |
| Guitar Acoustics & Sound Synthesis | 0 | 25 | String models, spectral measurement, synthesis, and realism tests |
| Guitar Alchemist Academy | 3 | 22 | Learner journeys using actual GA tasks and musical assessments |
| Guitar Studies | 2 | 23 | Fretboard skills, voicing playability, technique, and practice |
| Information Theory | 1 | 24 | Representation loss, index retrieval, compression, and information flow |
| Mathematics | 25 | 0 | Review and apply the existing sequence before expanding it |
| Music | 16 | 9 | Chord identity, harmony, rhythm, and GA's theory behavior |
| Musicology | 2 | 23 | Corpus provenance, style, form, and historical context |
| Network Science | 1 | 24 | Tool dependencies, agent coordination graphs, and chord relations |
| Philosophy | 1 | 24 | Evidence, inference, disagreement, and normative decisions |
| Physics | 1 | 24 | Vibrating strings, waves, sampling, and measurable acoustics |
| Product and Project Management | 1 | 24 | Vertical slices, queues, acceptance gates, and delivery evidence |
| Psychohistory | 2 | 23 | Observed ecosystem trends, model limits, and competing explanations |
| Semiotics | 1 | 24 | Chord symbols, notation, UI meaning, and governance labels |
| Visual Computing | 0 | 25 | Fretboard rendering, interaction, performance, and accessibility |
| World Music & Languages | 1 | 24 | Tunings, notation traditions, terminology, and localization checks |

## Six pilot questions

The pilots span learner, domain, interface, and system boundaries. Their codes are provisional until a branch and collision check immediately before authoring. Do not duplicate MUS-013 (root/bass/set), MUS-014 (inversions), or CS-002 (agent loops).

| Code | Course question | Project artifact or reproducible fixture | Acceptance exercise |
|---|---|---|---|
| DV-001 | When does a GA quality chart show an observation, an outage, or an old value? | GA `state/quality/chatbot-qa` snapshots and `docs/quality/README.md` | Classify four dated snapshots; draw a timeline with a gap and a separate availability lane; explain which trend claim remains unknown. |
| VC-001 | Can a guitarist use the same fretboard diagram with pointer, keyboard, and screen reader? | GA fretboard UI and a fixed chord/voicing fixture | Navigate, name, and compare a voicing by all three paths; record any missing information. |
| GAS-001 | What can an open-string recording establish about GA's guitar WASM engine? | A pinned recorded E2, a render of GA's existing Rust engine, and onset-aligned FFT/wavelet measurements | Compare pitch, partials, and time courses; name two audible properties the measurements do not settle; specify an offline ComfyUI candidate gate. |
| CS-003 | Where should a chord-name parser return uncertainty instead of inventing a chord? | GA chord parsing boundary and a small positive/negative input corpus | Trace each input through parsing, domain result, and user-visible error; verify no unsupported name is silently accepted. |
| GAA-004 | Can a novice select and play a useful voicing from a GA answer? | A fixed GA chord query and fretboard output | Play two candidate voicings, compare their physical demands, and explain a choice in musical context. |
| GTR-003 | Which playability claim can a voicing model actually support? | GA voicing generation and playability criteria | Compare three shapes and record the criteria that require a human hand test. |

The [CS-003 draft](../../state/streeling/courses/computer-science/en/cs-003-chord-parser-uncertainty.md) follows the `ChordSymbolParser` used by GA's voicing endpoint. Its [eight-case corpus](../../state/streeling/fixtures/computer-science/cs-003/README.md) separates supported inputs, invalid roots, unknown suffixes, partially interpreted alterations, and slash-bass notation. Its current behaviors are source-traced predictions; runtime tests, a pinned GA commit, musician feedback, and subject/localization reviews remain open. A parser that returns a plausible but different chord fails the course's acceptance rule even if it returns `200 OK` and a non-null object.

Produce these as six separate reviewable modules, starting with DV-001. A pilot is not published on the strength of its outline. The first pilot is a tracer for the research, course, localization, review, and Learn synchronization path. Later modules should use what that tracer reveals rather than copying its format blindly.

### Audio project direction, clarified during GAS-001

GA already has a Rust/WASM guitar prototype running through an AudioWorklet and an offline recording/critic loop. ComfyUI audio is a proposed offline refinement input, not a currently wired GA audio stage or a real-time dependency. A useful course should teach the evidence path from a licensed recording and a pinned engine render through onset-aligned FFT/wavelet measurements and level-matched listening, then to a controlled engine parameter experiment. Treat the candidate workflow, its provenance, and the parameter change as hypotheses until the measurements and listening checks support them.

This is also agentic dogfooding: an agent may propose a bounded change using GA's own rendered output, while a fixed external recording, repeatable signal measurements, and independent listening decide whether the change helped. Preserve rejected iterations as evidence. Cybernetics can teach feedback stability, Computer Science can teach the agent's proposal/evaluation boundary, and Product and Project Management can teach the acceptance gate; GAS-001 supplies the concrete audio case.

### Agentic experience and functional composition: tested candidate

CS-004 now drafts the next Computer Science slice against GA's local, unmerged ComfyUI bridge. It composes pure signal transformations and decision functions around explicit capture, network, decode, listening, and receipt effects. Its first dogfood run is a negative control: candidate and baseline are the same pinned GA E2 WAV, so every reported baseline/candidate error is equal and the improvement claim must be rejected. The [control evidence](../../state/streeling/fixtures/computer-science/cs-004/README.md) is reproducible. A [bounded wmux review attempt](../../state/streeling/fixtures/computer-science/cs-004/wmux-dogfood-observation.md) exposed denied sibling-repository reads and receipt writing. A user-authorized narrow retry then produced a marker-verified [advisory review and known-perturbation follow-up](../../state/streeling/fixtures/computer-science/cs-004/review-followup-20261004.md). These are observed agent-experience and comparator limits, not evidence of a generally reliable audio-refinement loop.

For preparation under increasing agent capability, the next proposed acceptance gate is practical: a lane must prove it can read its declared evidence and write its declared receipt before it counts as active; a generated audio candidate must retain baseline/workflow/model/seed provenance; pure comparisons must be reproducible; a listening protocol and human observations must be recorded before an engine change. The strongest counterargument is that this could add ceremony without improving a guitarist's experience. Revisit the approach if a smaller workflow yields the same verified decisions with less setup time. Do not expand the 25-course quota around this idea until the course exercise and the actual agent/audio workflow are tested by users.

## Data Visualization: 25-course path

This first complete department syllabus is organized as five progressions. Each entry has a different decision or skill; related Mathematics modules provide mathematical prerequisites, while these modules teach what a viewer may infer from a display.

| Range | Courses |
|---|---|
| DV-001–005: claims and data | 001 Observed, degraded, and stale quality runs; 002 Denominators and changing test populations; 003 Compare instrument cohorts without hiding their sizes; 004 Uncertainty in small QA suites; 005 Baselines, thresholds, and historical targets |
| DV-006–010: visual encoding | 006 Position, length, area, and the comparison task; 007 Small multiples for embedding partitions; 008 Scales for pass rate and latency; 009 Encode multi-state status without color alone; 010 Gaps and irregular time intervals |
| DV-011–015: interaction | 011 Drill from a headline to a failing case; 012 Cross-filter without losing the denominator; 013 Provenance and freshness in the tooltip; 014 Repository dependencies as graph or matrix; 015 Focus and context for a large chord universe |
| DV-016–020: high-dimensional data | 016 What a two-dimensional embedding projection cannot prove; 017 Neighborhood preservation checks; 018 Density and overplotting in a voicing corpus; 019 Distinguish clusters from label artifacts; 020 Compare projections across schema versions |
| DV-021–025: delivery and review | 021 A chart description that preserves the claim; 022 Keyboard and screen-reader access to underlying data; 023 Animation that preserves object identity; 024 Red-team a misleading quality chart; 025 Capstone: a reviewable GA/IX quality dashboard |

## Review gates and next slice

For every proposed module: check existing and in-flight IDs; record the repo revision and source evidence; require an exercise with an answer; run the repository verifier; review subject accuracy separately from prose and localization; verify the EN/FR/ES public readback after Learn synchronization. The public Streeling index currently warns that generated modules have not been reviewed. Preserve that disclosure until a real review process supports a stronger claim.

The source progress report now exposes conservative content signals for an exercise paired with an answer, a pinned Git revision link, and a resolvable local fixture link. On 2026-10-11 it found 48, 45, and 6 English modules respectively out of 77. These are review-queue signals only; absence can reflect a different course format, and presence cannot prove subject accuracy or project usefulness. The [CYB-003 correction receipt](../../state/streeling/reviews/cyb-003-correction-2026-10-11.md) shows why a quantitative-looking lesson must be checked against a real project task before it counts toward the 25-course outcome.

After DV-001, assess whether its exercise can be completed using only the pinned fixtures. Then author VC-001 and GAS-001 against fixed UI/audio fixtures, followed by CS-003, GAA-004, and GTR-003. Expand the other 20 department syllabi only after checking their current courses and consumers, so the 25-course quota does not generate duplicate or decorative lessons.

### Pilot authoring status, 2026-10-05

All six planned pilot questions now have EN/FR/ES **drafts**: DV-001, VC-001,
GAS-001, CS-003, GAA-004, and GTR-003. CS-004 is an additional agentic audio
dogfooding draft. GAA-004 and GTR-003 share a hand-checked C-major teaching
fixture and source-traced GA voicing rules; the shapes are not claimed to be
captured GA generator output. Focused GA voicing tests passed 18/18 with an
existing test binary, without a fresh build. Demerzel's `scripts/verify.ps1`
passed after these drafts were added; it ran 783 Python tests (one skipped),
the IXQL grammar tests, and the BAML drift check. An independent read-only
review found no substantive issue in the two new lessons or translations.

This is authoring progress, not seven reviewed or published courses. The next
gate is a fresh GA build and captured result for the two voicing lessons,
musician exercises, independent subject and native-language reviews, the
remaining policy localizations, then Learn sync and
anonymous EN/FR/ES readback. Record failures and changes to the lessons before
expanding the remaining department quotas.

### Reproducible source progress, 2026-10-11

Run `python scripts/streeling_course_progress.py` from Demerzel to measure the
source tree without counting a draft as a reviewed or public course. At pilot
commit `7fca60e`, the report finds 21 course directories, 72 English modules
(excluding `README.md`), and 453 remaining English modules to reach 25 in each
directory. Only 15 modules have files for all six active languages in the
multilingual policy. No course-production record on this branch records an
approved pipeline review. Four course directories (cybernetics,
information-theory, network-science, semiotics) are absent from
`state/streeling/university.json`; resolve that registry discrepancy before
using it as an authoritative department list. These are source-tree counts;
the public Learn index, native-language review, subject review, and learner
validation remain separate evidence.

The next Data Visualization draft, DV-002, teaches denominators and test
populations using two pinned GA QA snapshots and an explicitly labeled
counterfactual. It raises the pilot branch source count to 73 English modules
and lowers the source gap to 452, while remaining English-only and unreviewed.
DV-003 adds a separate unit-of-analysis exercise against the pinned GA voicing
audit: instrument corpus shares count voicings, while the 793/793 consistency
result counts shared pitch-class sets and retained representatives. It also
distinguishes inferred zero null/unknown counts from unmeasured musical naming
correctness. The branch now has 74 English source modules, 451 short of 25 in
each of its 21 department directories. DV-003 is English-only and unreviewed.
DV-001 now has EN/FR/ES/PT/IT/DE drafts. Each has eight level-two sections,
five exercises, five answers, and the pinned GA source links. Its production
record is `review_pending` because the research confidence is 0.65 and human subject,
native-language, and learner reviews have not happened. A bounded independent AI
subject check on 2026-10-11 approved the English facts and five answers, with its
scope and remaining gates recorded in `state/streeling/reviews/`. This adds one module to
the six-language source-coverage count, but changes neither the reviewed nor
the published count.

DV-004 is an English-only draft against the same pinned 52-prompt GA QA
snapshots. It teaches the exact percentage-point effect of one changed verdict
and keeps that calculation separate from a statistical confidence interval.
Its exercise asks the learner to repair a misleading “98.08% ± 1.92%
confidence” label. At the pre-rebase pilot tip, the source inventory was 75
English modules, 450 short of 25 in each department directory. After rebasing
onto Demerzel `origin/master` at `260226f`, upstream MUS-019 and MUS-021 bring
the source inventory to 77 English modules, 448 short. DV-004 is neither
reviewed nor published.

DV-005 adds an English draft on historical baselines, moving averages,
regression alerts, drift, and release targets using GA's pinned July 23 quality
report. Its five exercises require the learner to keep comparison scope,
metric-series denominators, and degraded observations visible. Source inventory
is now 78 English modules across 21 directories, 447 short of 25 each; 49 have
a detectable exercise/answer pair and 46 a pinned revision link. The new
course received a bounded AI subject check: the first pass found a report-date
versus observation-date error, and a focused recheck approved the correction.
Human subject and learner review, localization, and public Learn readback remain
pending. Its pipeline record remains `in_progress`.

The department denominator needs a decision before treating 525 as the final
quota. `university.json` registers 17 names, 21 names have course directories,
and 23 have `*.department.json` records marked as departments. Six records are
absent from the university list: cybernetics, information-theory, metaqa,
network-science, semiotics, and systems-engineering. MetaQA and Systems
Engineering have no course directories yet. The progress script now reports
all three counts and the missing sets; its 447-course gap still uses the 21
existing course directories. Do not silently choose 21 or 23 as the final
department scope while the curriculum decision in [Demerzel #1209](https://github.com/GuitarAlchemist/Demerzel/issues/1209) is pending.

The next bounded authoring batch adds DV-006 (quantitative encoding choices),
PM-002 (release evidence gates), and CS-005 (agent handoff evidence contracts).
All three use pinned project artifacts, five answered exercises, and an English
source draft. The source inventory is 81 English modules across 21 directories,
444 short of the provisional 525 target. DV-006's bounded AI subject review
found and corrected a description of three historical snapshots. PM-002's
bounded AI subject and evidence check found no factual or answer-key errors.
CS-005's bounded AI review found and corrected a synthetic fixture's revision
comparison; its focused recheck approved that correction.
These checks do not satisfy the human subject, fluent-language, learner, or
public readback gates; all three pipeline records keep review and publish open.

The following bounded batch adds DV-007 (OPTIC-K partition small multiples),
PM-003 (review queue flow metrics), and CS-006 (IXQL stage composition). Each
has a pinned project source or an explicitly synthetic teaching fixture and
five answered exercises. The source count is now 84 English modules across 21
course directories, leaving 441 to the provisional 525 target. Cross-checks
corrected a five-feed versus ROOT attribution in DV-007 and repeated-module
wording in PM-003; CS-006 had no finding in its bounded source and answer-key
review. DV-007's caption sentence count was corrected and rechecked. The six
production records from both batches keep human subject, learner, language,
and public readback gates open.

The next three English drafts are AUD-002 (level-matched GA guitar comparison),
PHY-002 (global FFT, STFT, and wavelet interpretation for guitar transients),
and VC-002 (evidence for the React-to-Godot message bridge). Each has a pinned
project source or reproducible fixture and five answered exercises. The source
inventory is 87 English modules across the provisional 21 course directories,
438 short of 525. Independent bounded AI checks found and corrected two
PHY-002 interpretation errors and a VC-002 test-host assumption; AUD-002 had
no finding in its source, arithmetic, and answer-key check. The PHY-002 STFT,
AUD-002 listening comparison, and VC-002 browser/Godot checks remain proposed
experiments, not measured outcomes. All three remain English drafts with
human subject, learner, localization, and public readback gates open.

INF-002, NET-002, and MCL-003 extend three departments with only one or two
previous modules. INF-002 demonstrates the information lost by GA's 124-slot
compact OPTIC-K vector with an executed synthetic calculation, while keeping
full retrieval behavior unclaimed. NET-002 computes a graph from Demerzel's
static capability registry and contrasts it with an intended but undelivered
BAML seam; it does not infer live tool connectivity. MCL-003 separates a GA
progression catalog's style labels from claims about unheard performances.
Each English draft has five answered exercises and a bounded independent AI
source and answer-key check with no finding. The source inventory is now 90
English modules across 21 provisional course directories, 435 short of the
525 target. Human subject, learner, fluent-language, pipeline review, and
public Learn publication remain open.

COG-002, PHI-002, and SEM-002 add project-grounded English drafts in three
more one-module departments. COG-002 uses a pinned GA fretboard demo to show
that one of six displayed note labels disagrees with its string and fret; it
does not claim a learner encountered the error. PHI-002 checks the gap between
a schema-valid advisory decision with empty evidence and Demerzel's stated
evidence and human-merge requirements. SEM-002 traces chord-symbol input,
canonical rendering, and projected pitch class through GA's F# DSL. Each has
five answered exercises and a bounded independent AI source/answer-key check
with no finding. The source inventory is 93 English modules across 21
provisional course directories, 432 short of 525. Human subject, learner,
language, pipeline review, and public readback remain open.
