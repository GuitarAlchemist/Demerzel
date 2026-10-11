# DV-001 simulated AI learner probe — 2026-10-11

## Protocol and boundary

An independent Codex subagent started with no conversation history. It was told to read only `dv-001-learner-task.md` and raw records explicitly requested there, and not to read the lesson, answers, scorecard, or review brief. It made no edits and consulted no source records beyond the handout. This was an **AI simulation**, not a human learner test. Duration was not measured.

## First response, before the handout correction

1. June 8 has no measured pass rate because `pass_pct` is `null`; the run is degraded due to backend unavailability. June 15, June 19, and July 19 report 75.00%, 7.69%, and 98.08% with `degraded: false`. No date belongs at 0%.
2. The proposed two-lane table left June 8's pass rate empty and marked the backend unavailable, placed the three later rates on their actual dates, and left unrecorded days blank without connecting points or inferring status.
3. Caption: “June 8: backend unavailable, so no pass rate was measured; 94% is a carried-forward May 16 reference.”
4. The response reported the measured June 15→June 19 drop and later July 19 rise without attributing a software cause. It requested prompt-level failures and run conditions, plus incident/code/deployment evidence for a claimed fix.
5. Its text alternative included all four dates, the absent June 8 value and degraded reason, the three later values, and the absence of data between snapshots.

The subagent called the three later runs “available,” then raised its own uncertainty: the handout had no explicit availability field, and `degraded: false` plus a reported rate might not establish full service availability. It also noted that “recovered” could describe a QA metric without proving operational or software recovery.

## Assessment and correction

The first response met all five criteria in the **original** scorecard. The availability wording exposed a real ambiguity: the lesson already says `degraded: false` records the producer's classification and is not a complete health certificate, but the answer-free handout had asked for “availability status” without that boundary. The handout now defines the status lane as the QA snapshot's report, and the scorecard now rejects an unsupported whole-service health claim. This correction does not turn the simulated attempt into a human learner result. Human subject, fluent-language, learner, and publication gates remain open.

## Blind retest after correction

A second independent Codex subagent started without conversation history and read the revised handout only. It answered all five tasks within the revised scorecard: it left June 8's quality value missing, used “not flagged degraded” for the later rows, left unrecorded days blank, dated the 94% carryforward to May 16, rejected the causal recovery claim, and wrote a status-complete text alternative. It explicitly stated that `degraded: false` reports only the QA snapshot's classification, not whole-service health or an explanation of a rate change. It still could not infer the producer's exact criteria for setting `degraded`; the exercise does not require that inference. No source records beyond the handout were consulted and duration was not measured. This remains a simulated AI probe, not a human learner result.
