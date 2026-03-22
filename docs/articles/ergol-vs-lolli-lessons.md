# ERGOL vs LOLLI — Lessons from Session 2026-03-24

## The Numbers

- 80+ artifacts created in one session
- 24 tasks completed by autonomous agent teams
- 8 repos in the ecosystem
- 42 skills, 26 grammars, 21 departments

**ERGOL score: ~15%.** Only the Discord chatbot was validated by a real user.

## The Five Lessons

### 1. One user interaction > 50 specs

"Can you reharmonize Let It Be in minor mode?" → "Cool!"

That exchange validated more than all 8 design specs combined. Specs are promises. User interactions are proof.

### 2. LOLLI feels productive, ERGOL feels slow

Writing a grammar: 10 minutes, feels amazing. Running a research cycle: 2 hours, produces one finding. The finding is ERGOL. The grammar alone is LOLLI.

### 3. Factory-of-factories amplifies LOLLI

MetaBuild produces a department in 60 seconds. We made 6. Zero have generated a single insight. The factory makes creation trivially easy — which makes the discipline to NOT create even more critical.

### 4. Agent teams optimize for completion, not value

24 tasks "completed" sounds impressive. But agents optimized for task completion (LOLLI), not value delivery (ERGOL). 5 specs produced — all perfect, none executed. The system rewards production over validation.

### 5. The only reliable ERGOL detector is a real user

No automated metric captures "Cool!" — the moment a real guitarist found the chatbot useful. User interactions should be the highest-weighted ERGOL signal.

## The Fix

### D_c Formula Revision

```
Old:   value = citations × 0.35 + PDCA × 0.25 + U→T × 0.25 + transfers × 0.15
Risk:  All metrics gameable by agents citing each other

New:   value = user_interactions × 0.40 + executed_pipelines × 0.25 +
              validated_findings × 0.20 + external_citations × 0.15
```

### The Anti-LOLLI Checklist

Before creating ANY artifact, answer:
1. **Who will use this today?** (not "eventually")
2. **Can I validate it right now?** (run it, test it, show it to a user)
3. **Does something similar already exist?** (extend, don't duplicate)
4. **What's the ERGOL metric?** (how will I know it delivered value?)
5. **Would deleting this hurt anyone?** (if no → it's LOLLI)

### The Session Rule

Every session should end with: **"What did a real human find useful today?"**

If the answer is "nothing" — the session was LOLLI, regardless of artifact count.

## Reference

- Jean-Pierre Petit, *Economicon* (1984) — ERGOL (productive capacity) vs LOLLI (inflated metrics)
- [Anti-LOLLI inflation policy](../policies/anti-lolli-inflation-policy.yaml)
- [Compounding metrics policy](../policies/compounding-metrics-policy.yaml)
- [Fractal compounding theory](../logic/fractal-compounding.md)
