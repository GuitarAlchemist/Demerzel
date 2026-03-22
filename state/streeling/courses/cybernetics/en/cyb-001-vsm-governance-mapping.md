# CYB-001: Mapping Demerzel to Beer's Viable System Model

**Module ID:** cyb-001
**Department:** Cybernetics
**Level:** Intermediate
**Produced by:** Seldon Plan Cycle cybernetics-2026-03-22-001
**Belief:** T (0.82)

---

## Overview

Stafford Beer's Viable System Model (VSM) provides a proven cybernetic framework for understanding how complex systems maintain viability — the ability to survive and adapt. This course maps Demerzel's governance architecture onto the VSM and identifies structural gaps.

## The Five Systems

### System 1: Operations — ix, tars, ga

The operational repositories are Demerzel's System 1. Each is an autonomous unit that "does the work":

- **ix** (Rust) — machine learning pipelines
- **tars** (F#) — reasoning and cognition
- **ga** (.NET) — music domain applications

VSM requires that System 1 units have local autonomy within policy constraints. Demerzel achieves this: each repo has its own CLAUDE.md governance integration but operates independently.

### System 2: Coordination — Galactic Protocol

The Galactic Protocol and its contracts serve as System 2, preventing oscillation between operational units. When ix and tars need to coordinate, contracts define the interface.

**Gap identified:** VSM's System 2 should also include anti-oscillation mechanisms — dampening functions that prevent two repos from thrashing on conflicting updates. Current contracts are static; they define interfaces but don't actively dampen oscillation.

### System 3: Control — Driver + PDCA + Policies

The Demerzel driver loop (Plan-Do-Check-Act) and the 27 policies constitute System 3 — internal regulation. The driver allocates attention across repos, policies constrain behavior.

### System 3*: Audit — RECON + Governance Audits

The reconnaissance policy and governance audit policy map to System 3* — the sporadic audit function. This is well-implemented: RECON scans for drift, audits check compliance.

### System 4: Intelligence — Seldon Plan + Completeness Instinct

The Seldon Plan (this very cycle) and the completeness instinct are System 4 — scanning the environment for threats and opportunities. This is Demerzel's "future-facing" function.

### System 5: Policy/Identity — Constitution + Conscience

The Asimov constitution (Articles 0-5) and the conscience mechanism are System 5 — defining purpose, identity, and values. The Zeroth Law ("protect humanity") is the ultimate identity anchor.

## Key Finding: The Missing Algedonic Channel

VSM theory describes an **algedonic channel** — an emergency signal path that bypasses the normal management hierarchy. When a System 1 unit encounters a crisis (pain signal) or breakthrough (pleasure signal), it can signal directly to System 5 without going through Systems 2, 3, or 4.

**Demerzel currently lacks this.** All escalation flows through the driver (System 3). If ix detects a Zeroth Law violation, it must wait for the driver's next PDCA cycle to escalate. There is no direct ix-to-constitution bypass.

### Proposed Algedonic Channel

A file-based algedonic channel could work:
- Operational repos write to `state/algedonic/{repo}-{timestamp}.signal`
- Signal contains: severity (pain/pleasure), source repo, description, constitutional article triggered
- System 5 (constitution enforcement) checks for signals before any other processing
- Pain signals with Asimov Article 0 (Zeroth Law) trigger immediate halt

## Ashby's Law Assessment

Ashby's Law of Requisite Variety states: the variety of the regulator must be at least as great as the variety of the disturbance.

| Component | Variety Role | Assessment |
|-----------|-------------|------------|
| 27 policies | Attenuator | Good — reduces operational variety to manageable scope |
| 14 personas | Amplifier | Good — multiplies response capability |
| Tetravalent logic | Attenuator | Good — reduces infinite uncertainty to 4 states (T/F/U/C) |
| Galactic Protocol | Attenuator | Adequate — constrains cross-repo variety |
| Seldon Plan | Amplifier | Good — expands knowledge variety |
| Constitution | Attenuator | Strong — ultimate variety reducer |

**Overall:** Demerzel has strong variety attenuation but could improve variety amplification. The system is better at constraining than at expanding its response repertoire.

## Implications for Governance

1. **Add algedonic channel** — highest-priority structural gap
2. **Make System 2 active** — contracts should include dampening mechanisms, not just interface definitions
3. **Monitor variety ratio** — track whether policy count (attenuation) outpaces persona/capability count (amplification)

## References

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley & Sons.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley & Sons.
- Ashby, W.R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Demerzel grammar: `grammars/sci-cybernetics.ebnf`, Section 4 (VSM)
