---
module_id: sem-003-status-signs-and-evidence
department: semiotics
course: "Status Signs and Evidence in Agentic Work"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-12-003
version: "0.1.0"
---

# Status Signs and Evidence in Agentic Work

> **Department of Semiotics** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to separate a status word from the event it claims to represent, read a Streeling course-production record without promoting a bounded check into a final verdict, and write an agent handoff whose claims can be checked against a pinned artifact. You will also identify what a schema, a local build, and a public readback each establish.

## The project decision

An agent has drafted a Streeling lesson and another agent reports “no findings” after reading its source and answer key. What should a coordinator tell the next agent: **draft**, **ready**, **reviewed**, or **published**? The choice controls whether a learner is directed to a public course, a reviewer is asked to inspect it, or an author is asked to revise it. An overstrong word can cause the next agent to skip a missing gate.

This course uses the real [SEM-002 production record](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/course-productions/cp-semiotics-2026-10-11-002.json), its [bounded AI review receipt](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/sem-002-subject-review-2026-10-11.md), the [production schema](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/schemas/course-production.schema.json), and the [source-progress reporter](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py). Every Demerzel source link in this lesson pins commit `c453a91d1c4d913af72c28779eff826659c1d654`. This is an analysis of that snapshot. It does not claim the current production or public state is identical.

## 1. What does a status sign stand for?

[SEM-001](sem-001-signs-in-governance.md) introduced the sign, its object, and the interpretation a reader makes. In an agent handoff, `reviewed` is a **symbol**: its meaning depends on a shared convention. A link to a review receipt can act as an **index**, pointing to a particular artifact. A green check badge is another compact sign, but its color and mark need an agreed meaning, a named predicate, and provenance. None of these marks, by itself, performs a review.

The words in the opening question name different possible claims, not a new Streeling state machine:

| Word in a message | Checkable claim it might mean | Evidence needed before using it without qualification |
| --- | --- | --- |
| `draft` | A source file exists | Path and exact revision of that file |
| `ready` | A defined intake gate has passed | Named gate, its inputs, result, and date; `ready` alone does not say ready *for what* |
| `reviewed` | A stated reviewer examined a stated scope | Review receipt, reviewer, scope, result, and any remaining review gates |
| `published` | A learner can retrieve the intended version | Deployed route, anonymous readback, and matching source provenance |

These are **communication tests**, not claims that the repository implements four corresponding enum values. The pinned production schema actually permits `in_progress`, `review_pending`, `published`, `rejected`, and `failed`. It does not define a `draft`, `ready`, or `reviewed` status value. An agent should say “English source draft exists” or “ready for bounded source review” when that is the evidence, instead of implying a nonexistent schema transition.

### Exercise 1 — Name the object

A handoff says only “SEM-002 is ready.” Identify two materially different objects that `ready` could represent, and rewrite the sentence so one of them can be checked. Do the pinned schema values include `ready`?

> **Answer:** It could mean ready for source review, or ready for deployment after all reviews. One checkable rewrite is “SEM-002 English source at commit `c453a91d1c4d913af72c28779eff826659c1d654` is ready **for a bounded source and answer-key review**; production review and publication are incomplete.” The schema has no `ready` enum value.

## 2. Read the record, then the receipt

At the pinned revision, the SEM-002 production record says `status: in_progress`. Its research, outline, and content phases are complete; translation is incomplete with `languages: ["en"]`; review and publish each have `completed: false`. The separate AI receipt says an independent reader found **no findings within a bounded source and answer-key scope**. It explicitly leaves human subject, learner, fluent-language, and public Learn checks open. Those statements can both be true: a scoped inspection happened, while the final review phase remains incomplete.

The semiotic failure would be to let the word `reviewed` absorb every possible review scope. “AI source and answer-key preflight completed with no findings” is a precise statement. “Course reviewed” can be read as a final editorial or human subject verdict and would misdirect the next agent. A reviewer identity alone is also weak evidence: the receipt must tell us what was examined and which checks were excluded. A production flag is a claim made by a file; its basis needs a traceable receipt before it becomes a trusted handoff fact.

The [progress reporter](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py#L89-L107) counts a pipeline review approval only when `phases.review.completed` is true **and** `phases.review.verdict` is `approved`. SEM-002 does not satisfy that predicate at the pinned revision. This reporter's count is a conservative flag over records, not an independent assessment of the course's subject accuracy. Conversely, if someone manually wrote those two values without a trustworthy review, the counter alone would not prove the review occurred.

### Exercise 2 — Scope a review claim

Choose the defensible handoff from these alternatives for pinned SEM-002: (A) “No review happened”; (B) “The course passed all review gates”; (C) “A bounded AI source and answer-key check found no findings; the production review phase remains incomplete.” Explain why the other two fail.

> **Answer:** C. A is false because the receipt documents a bounded AI check. B exceeds the receipt: human subject, learner, language, and public checks remain open, and `phases.review.completed` is false. The words “no findings” refer to the named inspection scope, not every possible defect.

## 3. A valid shape is not a verified transition

The production schema constrains field types and allowed `status` strings. It requires a `status`, research, outline, content, and timestamp. It gives `review.completed` and `publish.completed` boolean shapes when those phases are present. It does **not** encode a general cross-field rule such as “`status: published` implies `publish.completed: true`.” Therefore a record can be syntactically schema-valid while making a contradictory operational claim. This is a statement about the pinned schema's expressiveness, not evidence that such a bad record exists in production.

The pinned [course preflight](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_preflight.py) checks schemas, file names, frontmatter, declared language files, English word count, and answered exercise signals. It has one explicit status consistency rule: `in_progress` requires review and publish completion flags to be false. It does not fetch the public site or grade subject matter. A passing preflight means that its listed predicates held for the inspected package; it cannot be read as “learner approved” or “live on Learn.”

Here is a **synthetic** modification to the pinned SEM-002 record: change only `status` to `published`, leaving `phases.publish.completed: false`. The schema accepts both individual values and has no condition linking them. The preflight's only status consistency rule applies to `in_progress`, so this artificial contradiction would evade that particular rule. Do not create it in the repository; use it to learn which claim each checker can support. The appropriate response is to inspect the production record, a deployment receipt, and an anonymous route, not to trust the word `published`.

### Exercise 3 — Separate shape from truth

Would the synthetic `status: published` plus `phases.publish.completed: false` conflict with a rule in the pinned JSON schema? Would a valid schema result prove that SEM-002 is publicly available?

> **Answer:** No rule in that schema relates the two fields, so those values alone do not violate it. A schema-valid result establishes structural validity for the fields it checks; it does not prove deployment or anonymous public availability. The contradictory values should be investigated, not advertised as publication.

## 4. Keep local and public referents distinct

The [public baseline receipt](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/public-baseline-2026-10-11.md) records an anonymous Streeling index readback on 2026-10-11. It reports a source commit and notes that public presence alone is not an author review verdict. In the same dated receipt, local Learn preflight generated DV-001 pages while anonymous GET requests to those new routes returned 404. The lesson is a relation between signs and objects: “generated page exists locally” points to a build artifact; “published” points to a retrievable public route at a specific version. The former does not entail the latter.

The public baseline is historical evidence about DV-001 routes on that date, not a live test of SEM-002 or of today's site. For a new SEM-003 release, a coordinator would need to identify the intended route, deploy the generated site, fetch that route anonymously, inspect a version marker or source SHA, and check the returned content. HTTP 200 alone could serve an older version. The source SHA is an index into the authored revision; the route readback ties it to the learner's actual view. The reviewer receipt is a different index into the review event. Neither can substitute for the other.

### Exercise 4 — Identify what was observed

In the dated DV-001 example, a local generated page exists and the anonymous route returned 404. Which statement is supported: “the lesson was published,” “the local build produced a page, but that public route did not serve it on the readback date,” or “no source file existed”? What additional check would be needed after a later deploy?

> **Answer:** The middle statement is supported. The local page and the 404 describe different surfaces at the dated observation. After deployment, fetch the intended public route anonymously and compare its content or source-provenance SHA with the intended revision; a local build or deployment command alone is insufficient.

## 5. Write a handoff another agent can act on

A useful status message is a small evidence chain: **artifact and revision → named check → observed result → missing gate → next action**. This is a writing pattern for this exercise, not a proposal for a new normative DSL. It allows the receiving agent to follow the indices and reject a stale or broader interpretation. A compact example grounded in the pinned SEM-002 snapshot is:

> “SEM-002 English source exists in Demerzel at `c453a91d1c4d913af72c28779eff826659c1d654`. A bounded AI check of source and five answers reported no findings. The production record is `in_progress`, with review and publication incomplete. Next: obtain human subject and learner review, then verify the intended Learn deployment by anonymous readback.”

This message does not invent a `ready` enum value. It uses the operational word “next” to route work, and names which artifact would change the claim later. If a future review approves only factual accuracy, describe that scope; do not silently turn it into language approval. If the source revision changes, the old review receipt no longer automatically covers the new text. This is why immutable revision links matter: they tie the reviewer, source, and subsequent public readback to the same object or show where the chain has broken.

### Exercise 5 — Repair an agent message

Rewrite: “SEM-002 is reviewed and published; the tests are green.” Use the pinned production record and review receipt only. State one exact next action, and name an unknown rather than inventing a test or deployment result.

> **Answer:** “At Demerzel commit `c453a91d1c4d913af72c28779eff826659c1d654`, SEM-002 has an English draft and a bounded AI source and answer-key receipt with no findings. Its production record remains `in_progress` with `review.completed=false` and `publish.completed=false`. A fresh test run and public SEM-002 route readback are not established by these artifacts. Next: request human subject and learner review against this source revision.” The original message falsely expands a scoped check into final review and claims publication and tests without corresponding evidence.

## Limits and transfer

This lesson analyzes pinned Demerzel files and a dated public receipt; it does not execute a live agent handoff, test learners, validate SEM-003 with a human semiotician, or publish this draft. The five exercises test whether a reader can identify each status word's referent and supporting evidence. To see whether the approach improves agent coordination, run a controlled handoff: give one group an unqualified status message and another the evidence chain, then compare whether each group selects the correct next gate and cites the right source revision. Until such an experiment runs, the teaching benefit remains a hypothesis.
