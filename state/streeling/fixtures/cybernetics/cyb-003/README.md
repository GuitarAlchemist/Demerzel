# CYB-003 pinned pipeline-state replay

From a Demerzel checkout that contains commit `66083fc684b57a12ef307c19c3819d91c551295f`, run:

```powershell
python scripts/streeling_verify_cyb003_snapshot.py
```

The script reads the schema and all course-production JSON files **from that Git commit**, not from the working tree. It checks five configured status labels, three configured review verdict labels, eight records, the 7/1 observed status split, zero recorded verdicts, and the resulting 0.543564-bit empirical status entropy. These checks replay the course's arithmetic. They do not assess the course's subject accuracy, learner success, or regulatory capacity.
