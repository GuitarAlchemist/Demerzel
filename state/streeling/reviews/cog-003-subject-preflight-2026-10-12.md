# COG-003 independent AI subject preflight — 2026-10-12

An independent read-only Codex agent checked the English COG-003 draft, research and production JSON, and pinned GA fretboard demo/component at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. **No actionable findings within the static source and arithmetic scope.** The demo has six positions and displays `C` at string 5 fret 3; the component's high-to-low default tuning makes that position G. The corrected teaching key `E,C,G,E,C,G` is consistent with the pinned source. The click callback records a string/fret coordinate only; no confidence input or learner intervention was established.

The reviewer recomputed the six explicitly synthetic outcomes `[1,1,0,1,1,0]`, squared losses `[0.01,0.04,0.49,0.16,0.01,0.81]`, total `1.52`, mean Brier `1.52/6≈0.2533`, and contaminated-key mean `0.12`. For hypothetical `q=0.7`, expected losses `0.21` at `p=0.7` and `0.25` at `p=0.9` differ by `0.04`. All six exercise answers align. The proposed held-out next-day Brier/accuracy test has an explicit falsifier and is not presented as a real learner result. Targeted package preflight passed; review and publish flags remain false.

Five AI-drafted localizations (FR, ES, PT, IT, DE) received a separate read-only semantic-parity check by an agent that had not authored those translations. It found no actionable difference in the six synthetic rows, corrected `E,C,G,E,C,G` key, Brier and expected-loss math, six answers, or proposed study limits. Pinned URL sets match and local links resolve. This is not fluent-language approval.

This review did not run a browser UI, test a learner, establish an intervention benefit, approve fluent translations, or perform public readback. Human subject and learner review remain open.
