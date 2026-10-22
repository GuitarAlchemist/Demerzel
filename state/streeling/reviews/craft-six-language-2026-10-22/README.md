# Craft courses: six-language source and Learn transfer evidence

Status: source candidates retained locally; subject, fluent-language and human learner reviews remain open. Nothing in this packet grants approval, declares a source freeze or claims public publication.

## Completed source work

Content commit: `cb0a738790db4ce6904a4972c414bc9aada44d3b`.

PHY-005 (physical/scene units), SEM-004 (face identity under reindexing) and CS-009 (composed panel constraints) now each have EN/FR/ES/PT/IT/DE drafts. Nine new localized files add 45 exercise/answer pairs. The three packages contain 18 language files and 90 pairs altogether. English content and fixtures are unchanged.

The three production records now declare all six source languages. Translation completion, review and publication remain false. Their feedback distinguishes the earlier AI dry-run from the human evidence still needed. Old frozen briefs continue to describe their original revisions; `source-manifest.json` binds the current 44 lesson, fixture, production/research and review artifacts for a new review or transfer.

## Verification and review

- All nine new files have five ordered exercise/answer pairs. Coordinator checks passed for retained frontmatter, the complete source URL sequence, inline code, numeric values and existing relative links. Two German files repeat supplied values outside their preserved code to explain units or panel direction; those repetitions were inspected rather than treated as a new mathematical claim. Details are in `locale-checks.json`.
- The three targeted `streeling_course_preflight.py` checks passed after updating the declared languages.
- `pwsh scripts/verify.ps1` exited 0: 804 Python tests with two skipped, the IXQL grammar checks and BAML parity. Generated BAML changes were confirmed to be line endings only and restored.
- A fresh independent AI reader compared all nine new translations with all three English sources and returned **no findings**. Its audit covered unit mappings, absent versus zero height, lower bounds and absent witnesses, forward/inverse maps, turnover limits and the scope of rigid-model refusal. This was same-family static review; it did not replay IX, assess a human learner or provide fluent-human approval.

The source inventory now has 26 modules with files in all six active languages, up from 23. It still has 147 core English course codes toward the original 525 target, with 378 remaining and zero pipeline review approvals. These are candidate-branch counts, not the deployed catalog.

## Rendered Learn evidence

An isolated snapshot used Learn migration prototype `1c8aefd9d273f6e09957067990b4780de9dd63f1` and the clean earlier Demerzel source `d89f9e91242c92205d900bf2baea0f55e3de0751`. The three EN/FR/ES lesson contents are unchanged at the new source commit.

The full Astro build exited 0 and built 1,711 pages. The nine course pages were hashed after rendering. The existing HTML link checker examined their article links: **nine pages, zero unresolved internal links**. Its self-test detected both an intentionally absent page and an absent anchor. All four FR/ES English-fallback routes for CS-006 and VC-007 exist as rendered HTML. This resolves the previous source-only routing uncertainty.

The first build invocation used `--root` from the GA working directory and failed resolving a package from a GA prerender path. Running from the actual isolated Learn directory succeeded. No product code was changed to address that environment failure. The build used existing dependencies (Node 24.12.0, Astro 7.3.2, Starlight 0.42.0), not a fresh lockfile install. `render-proof.json` records the exact scope, hashes and limits.

This is static rendering and article-link verification. No browser interaction, visual assessment, scene import, deployment or anonymous public readback was performed. External GitHub source and fixture links still need authoritative publication.

## Transfer requirements established by the rehearsal

Learn #197 is still an open draft whose owner explicitly says not to merge; #200 is still unmerged. No final Demerzel freeze/source-copy commit was established. Existing Learn worktrees and the migration owner's branch were preserved.

1. **Retain the complete source.** The prototype copies only EN/FR/ES and deliberately leaves PT/IT/DE in Demerzel. Preserve the nine new language files in any source move; the current prototype alone would not transfer them. The current site generates three locales, so retained source languages and rendered site languages must be reported separately.
2. **Carry the dependency closure.** Against #197's present source, the three roots need seven additional pilot modules: CS-005, CS-006, VC-001, VC-002, VC-004, VC-005 and VC-007. `dependency-closure.json` lists exact module names. The PHY prerequisite labels `basic-ratios` and `dimensional-analysis` are concepts, not missing course IDs. Recompute the closure against the final frozen source rather than blindly importing an old catalog.
3. **Move the verifiable exercises with the lessons.** `source-manifest.json` proposes fixture paths under `code/streeling/fixtures/`, consistent with the migration direction. Those are proposed paths; source links must be transformed when the approved move is applied. No existing Learn source was edited by hand.
4. **Keep review provenance.** Production/research records, frozen briefs, original learner tasks, the revised CS-009 task and raw AI responses remain part of the packet. Their final Learn location is outside #197's prototype and remains undecided. They must retain original blobs and distinguish old targets from a new review target.
5. **Recheck public evidence after integration.** Generate from the actual accepted source; verify links and rendering there, obtain the real review verdicts, then deploy and read back the public revision. A local render does not establish those outcomes.

The transfer inventory makes these requirements inspectable without overwriting the migration owner's work. The original 21-department/525-course objective remains active. AUD-001's human reviewer is still for the user to designate.
