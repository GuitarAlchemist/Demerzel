# Streeling course-bearing departments

The `departments` array in `university.json` is the course-bearing set for the current 25-courses-per-department objective. It contains 21 departments, so the target is 525 distinct numbered core courses (`001` through `025` within each department). The 21 course directories under `state/streeling/courses/` match that set. A draft, a translation file, or a department record by itself does not count as a reviewed or published course.

The records `departments/metaqa.department.json` and `departments/systems-engineering.department.json` remain in Demerzel. They have no course directories and are outside this 21-department catalog. Their presence does not raise the current target to 575. Adding either to the course-bearing set requires an explicit scope change and a matching course directory; no empty directory or synthetic approval is created merely to make counts agree.

The progress report (`python scripts/streeling_course_progress.py`) separately reports authored English drafts, distinct core codes, active-language source presence, pipeline review approvals, and discrepancies among registry, records, and directories. Local Learn sync discovers course directories; it is a generated preview, not public publication. Human review and anonymous readback remain separate gates.
