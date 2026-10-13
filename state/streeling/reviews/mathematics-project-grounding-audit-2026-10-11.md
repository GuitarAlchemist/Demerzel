# Mathematics project-grounding audit — 2026-10-11

## Scope

Three independent read-only Codex agents inspected the 25 English Mathematics lessons at Demerzel commit `4b9d3101c5fb33e9372f66098db4a07a40cfa23c`, in ranges MAT-001–008, MAT-009–016, and MAT-017–025. They checked for a concrete GA/IX/Demerzel question, a pinned project artifact, at least one answered exercise, and an explicit evidence limit. This was a **grounding audit**, not a line-by-line mathematical proof check, learner test, fluent-language review, or pipeline approval.

## Findings

- **MAT-001 was the clear gap.** It taught general proof methods with answered general exercises but no pinned project problem or project-evidence limit. Its six active-language files exist, so an English correction needs corresponding localized drafts and review.
- **MAT-002–025 met the bounded project-grounding baseline.** Each cited IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`, contained at least one answered IX-specific exercise, and distinguished a proposed experiment from a run. The MAT-009–016 reviewer verified all 54 distinct linked IX source paths in that range; the other ranges checked their cited paths. This does not verify every mathematical answer or runtime behavior.
- **MAT-013** could state its `ix_distance` caller decision more plainly; its existing negative cosine self-distance exercise supports that question.
- **MAT-021** covers IX FFT, decimation, Welch, and wavelet behavior, but does not contain a GA audio render or measurement. Its proposed audio-rate exercise must not be reported as a measured GA result.
- **MAT-023** pins a GA PNML fixture only in a proposed experiment. Its IX reachability exercise does not establish live Demerzel agent-lane behavior. A future exercise could test the pinned PNML and keep those models separate.

## Follow-up in this branch

MAT-001 now has a small GA embedding-similarity case, an answered direct-proof exercise, and pinned source and test links in all six active-language drafts. The proof states its exact-arithmetic and nonzero-input assumptions; the finite GA contract test is identified as evidence for one vector pair, not a universal proof. Research cycle `mathematics-2026-10-11-001` and production record `cp-mathematics-2026-10-11-001` document the change. This follow-up does not change the count of approved reviews or publicly published courses.
