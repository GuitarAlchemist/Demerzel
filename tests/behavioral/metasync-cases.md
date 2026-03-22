# MetaSync Behavioral Test Cases

Tests for the `/demerzel metasync` skill — drift detection and auto-fix between documentation and disk reality.

## TC-MSYNC-001: Detect count drift in README artifact table

**Given:** README.md artifact table states `| Grammars | 21 |`
**And:** `grammars/*.ebnf` on disk contains 26 files

**When:** `/demerzel metasync --scan` is invoked

**Then:**
- Drift type: TRIVIAL_DRIFT
- Report line: `✗ Grammars: README says 21, actual: 26`
- Severity: auto-fixable
- No structural flag raised

---

## TC-MSYNC-002: Auto-fix count drift updates README table

**Given:** README.md states `| Behavioral tests | 44 |`
**And:** `tests/behavioral/*.md` contains 53 files

**When:** `/demerzel metasync --fix counts` is invoked

**Then:**
- README.md line updated to `| Behavioral tests | 53 |`
- Change committed with message `fix: MetaSync — update artifact counts`
- Log entry written to `state/evolution/metasync-log.json` with `was: 44, now: 53`
- No STRUCTURAL_DRIFT flagged

---

## TC-MSYNC-003: Detect stale prose description in README

**Given:** README.md prose contains "a 16-department knowledge framework"
**And:** `state/streeling/departments/*.department.json` contains 21 files

**When:** `/demerzel metasync --scan` is invoked

**Then:**
- Drift type: STRUCTURAL_DRIFT (prose mismatch, not just table count)
- Report line: `! README Streeling prose says "16-department", actual: 21`
- Auto-fix updates the prose to "21-department"
- Flag also notes CLAUDE.md should be checked for matching description

---

## TC-MSYNC-004: Detect cross-repo reference drift — IxQL renaming

**Given:** A consumer CLAUDE.md snippet (e.g., in `templates/CLAUDE.md.snippet`) still references "MOG" (Multi-Objective Grammar)
**And:** The canonical term is now "IxQL" throughout Demerzel artifacts

**When:** `/demerzel metasync --fix cross-repo` is invoked

**Then:**
- Drift type: STRUCTURAL_DRIFT
- Report line: `! templates/CLAUDE.md.snippet — references deprecated "MOG", should use "IxQL"`
- No auto-fix (structural — requires human review)
- Flag escalated for human decision on terminology migration

---

## TC-MSYNC-005: Detect missing cross-repo reference file

**Given:** README.md contains `[IxQL Guide](docs/ixql-guide.md)` link
**And:** `docs/ixql-guide.md` does NOT exist on disk

**When:** `/demerzel metasync --scan` is invoked

**Then:**
- Drift type: STRUCTURAL_DRIFT
- Report line: `! docs/ixql-guide.md — referenced in README, file missing`
- No auto-fix attempted
- Escalated for human review

---

## TC-MSYNC-006: Detect grammar section count mismatch

**Given:** README.md IxQL section states "**11 sections**"
**And:** `grammars/sci-ml-pipelines.ebnf` contains a different number of top-level section headers (lines matching `^\(\* [0-9]+\.`)

**When:** `/demerzel metasync --fix grammars` is invoked

**Then:**
- Drift type: TRIVIAL_DRIFT if count-only, STRUCTURAL_DRIFT if sections renamed
- If count-only: README updated and committed
- If sections renamed: report lists changed section names, no auto-fix
- Log updated with check result

---

## TC-MSYNC-007: Clean state — no drift detected

**Given:** All README artifact table counts match actual file counts on disk
**And:** All referenced cross-repo files exist
**And:** CLAUDE.md prose counts match actual counts

**When:** `/demerzel metasync --scan` is invoked

**Then:**
- Report shows all entries as MATCH
- No files modified
- Log entry written with `trivial_drifts_fixed: 0, structural_flags: 0`
- Exit with success

---

## TC-MSYNC-008: CLAUDE.md policy count drift

**Given:** CLAUDE.md states `24 policies: alignment, rollback, ...`
**And:** `policies/*.yaml` on disk contains 27 files

**When:** `/demerzel metasync --fix counts` is invoked

**Then:**
- CLAUDE.md policy line updated to `27 policies:`
- Policy list in CLAUDE.md updated to include new policy names
- Committed with standard MetaSync commit message
- Log entry records the fix with `file: CLAUDE.md`

---

## TC-MSYNC-009: MetaSync log is append-only

**Given:** `state/evolution/metasync-log.json` already contains prior run entries
**And:** A new MetaSync run fixes 3 trivial drifts

**When:** MetaSync auto-fix completes

**Then:**
- New entry APPENDED to log (array entry, not overwrite)
- Existing entries preserved
- New entry includes `timestamp`, `trivial_drifts_fixed: 3`, `structural_flags: N`, `artifacts_checked: 9`, and `fixes` array
- Article 7 (Auditability) satisfied

---

## TC-MSYNC-010: Scan-only mode makes no changes

**Given:** Multiple trivial drifts exist (counts wrong)

**When:** `/demerzel metasync --scan` is invoked (scan-only mode)

**Then:**
- Drift report printed to stdout
- No files modified (README.md, CLAUDE.md unchanged)
- No git commit made
- No log entry written
- Exit with non-zero status indicating drifts found
