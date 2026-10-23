# Streeling University — courses have moved to learn

Since 2026-10-21, Streeling courses are written and published in
[spareilleux/learn](https://github.com/spareilleux/learn), not here:

| What | Where in learn |
|---|---|
| Modules, English, French and Spanish | [`streeling/courses/<department>/{en,fr,es}/`](https://github.com/spareilleux/learn/tree/main/streeling/courses) |
| Department files (`*.department.json`), `university.json`, `curriculum-references.json` | [`streeling/`](https://github.com/spareilleux/learn/tree/main/streeling) |
| Fixtures: programs and data behind a module's evidence | [`code/streeling/<department>/<module>/`](https://github.com/spareilleux/learn/tree/main/code/streeling) |
| Production records and their schema, review packets | [`streeling/course-productions/`](https://github.com/spareilleux/learn/tree/main/streeling/course-productions), [`streeling/reviews/`](https://github.com/spareilleux/learn/tree/main/streeling/reviews) |
| The published pages | <https://spareilleux.github.io/learn/streeling/> |

learn copied them from this repository at commit
[`1beb089`](https://github.com/GuitarAlchemist/Demerzel/tree/1beb0890faec827e1a9e5532abfdc97908de441d/state/streeling),
which still holds the files as they were here. To write or fix a course, open a pull request in learn, from a clone
next to this one (`../learn/`); its `AGENTS.md` gives the conventions.

## What stays here

- The German, Italian and Portuguese translations in `<department>/{de,it,pt}/`, frozen: learn publishes English,
  French and Spanish only. Their English source is in learn, and it may have changed since they were translated.
- The department weights, `../departments/*.weights.json`, which `seldon-research-cycle` and tars read.
- The research cycles, `../research-cycles/`, and the rest of `state/streeling/`.
