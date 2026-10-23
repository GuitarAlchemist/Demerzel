---
category: harness
date: 2026-07-30
topic: A derived artifact nobody regenerated was platform-dependent in two ways, one of which git cannot normalise — wiring the dormant guard to CI is what proved it
source: Issue #919, PR #924, ADR-0005 §Decision.4, scripts/check_baml_drift.ps1
---

# The guard that finally ran, and what it found underneath

## Symptom

`scripts/verify.ps1` had regenerated `baml_client/` and diffed it against
`baml_src/` since ADR-0005. Its own comment said *"that only stays honest if CI
diffs them."* No workflow invoked `verify.ps1`. 23 generated files reached master
stale behind that gap.

Adding the CI caller was expected to be a five-line job. It was not: the first
Linux run failed against a client that was, by every local check, perfectly in
step with its source.

## The house pattern, one turn further in

The prior lesson —
[a guard is only as good as its subject](2026-07-29-a-guard-is-only-as-good-as-its-subject.md)
— says to ask what a guard is bound to, not whether it runs. This was the
complement: **binding correct, subject correct, invocation path never executed.**
Both questions are load-bearing, and neither implies the other.

## What the guard found once it ran

`baml_client/` was never reproducible. Two independent causes, and the second is
the one worth remembering.

**1. Content embedded as an escaped literal.** `inlinedbaml.py` embeds the
*content* of every `.baml` file as a Python string literal. A CRLF checkout
changes the characters *inside* that literal, `\n` becoming `\r\n`. git's
autocrlf normalisation operates on a file's line endings, not on escape sequences
within a literal, so `git diff` cannot see past it. The committed artifact held
152 escaped `\r\n` for one source file and plain `\n` for another sitting beside
it. There was no `.gitattributes` at all, so `core.autocrlf` decided this
per-machine.

**2. A bare trailing CR, which `.gitattributes` cannot fix.** Pinning both trees
to `text eol=lf` was necessary and insufficient. Seven files still differed, each
by one line whose two sides rendered identically:

| | last bytes of `baml_client/__init__.py` |
|---|---|
| committed (Windows) | `b'...\n]\r'` — 1 CR, 0 CRLF |
| Linux runner | `b'...\n]'` |

The generator terminates several files with a **lone `\r` and no `\n`**. git's
CRLF→LF clean filter rewrites `\r\n` *pairs*; a bare CR is not a line ending, so
no attribute setting touches it and the byte is committed verbatim. Whoever ran
the generator last set the trailing byte, and the other platform's CI would
report drift forever.

## Lessons

**A dormant guard hides the state of its subject, not just its own health.** The
cost of never running `verify.ps1` was not "we might have drift" — it was that
`baml_client/` had been non-reproducible for its entire existence and nothing
could reveal that except a regeneration on a second platform.

**`eol=lf` is not a guarantee of byte-identical codegen.** It normalises line
endings. It does not normalise a bare CR, a trailing-newline difference, or any
platform-dependent byte a generator embeds *inside* string content. If a
generated artifact is committed and diffed, prove reproducibility by regenerating
on a second OS — not by reading `.gitattributes`.

**A drift report must print the drift.** The first CI failure named seven files
and stopped, which cannot distinguish real codegen drift from a whitespace
artifact — and the reader is looking at a log they cannot reproduce locally.
Naming the file is the beginning of the report, not the end.

**A guard that cries wolf every run is worse than no guard.** Shipping the job
before finding these two causes would have failed every PR against a correct
client, and taught everyone to click past it. When a brand-new check fails on its
first real run, the check is the more likely suspect than the codebase — but only
until you have measured. Here the bytes said the codebase was genuinely wrong.

**Measure the bytes.** Both `git diff` renderings looked identical. `\ No newline
at end of file` on both sides of a one-line diff means an invisible byte, and the
only way through is to read the blob and the working copy as `bytes` and compare
lengths and counts.

## Also relevant

`npx --yes @boundaryml/baml generate` floated on **latest**. A drift check whose
own generator version can move underneath it manufactures the drift it exists to
detect: the next release that alters codegen fails every PR against a correct
artifact. Pin the generator, and single-source the pin from the file that already
declares it — see
[a constraint is worth its enforcement path](2026-07-28-a-constraint-is-worth-its-enforcement-path.md).
