# C# 15 Discriminated Unions — Implementation Guide for ga

**Status:** Implementation ready (requires .NET 11 Preview 3+)
**Related issues:** #133, #131 (tars IxQL), #53 (AI probes)
**Related specs:** `logic/`, `docs/superpowers/specs/2026-03-22-fuzzy-enum-du-design.md`

---

## Overview

C# 15 / .NET 11 Preview 3 introduces the `union` keyword — native discriminated unions with exhaustive pattern matching. This eliminates the need for `OneOf<>` wrapper libraries and brings ga's type system into alignment with tars F# discriminated unions, enabling shared domain semantics across the Galactic Protocol.

---

## Tetravalent Logic

Demerzel's tetravalent logic (T/F/U/C) maps directly to a C# 15 union. The `confidence` double on `True` reflects the belief-currency model; `reason` on `False`/`Unknown` satisfies Article 2 (Transparency); dual `evidence` strings on `Contradictory` support tetravalent escalation.

```csharp
union Conclusion
{
    True(double confidence);
    False(string reason);
    Unknown(string gap);
    Contradictory(string evidenceA, string evidenceB);
}
```

Exhaustive pattern matching — the compiler rejects incomplete switches:

```csharp
string Summarize(Conclusion c) => c switch
{
    Conclusion.True(var conf)          => $"Verified (confidence={conf:F2})",
    Conclusion.False(var reason)       => $"Refuted: {reason}",
    Conclusion.Unknown(var gap)        => $"Insufficient evidence: {gap}",
    Conclusion.Contradictory(var a, var b) => $"Conflict — A: {a} / B: {b}",
};
```

**Confidence thresholds** (from `constitutions/default.constitution.md`):

| Value | Action |
|-------|--------|
| >= 0.9 | Proceed autonomously |
| >= 0.7 | Proceed with note |
| >= 0.5 | Ask for confirmation |
| >= 0.3 | Escalate to human |
| < 0.3  | Do not act |

---

## IxQL Pipeline Results

IxQL query results from ga's music-analysis pipeline replace `OneOf<Validated, Rejected, Inconclusive, Unstable>` with a native union. The `Explanation` type carries human-readable reasoning for Article 2 compliance; `Contradiction[]` enables multi-source conflict reporting for the Contradictory branch.

```csharp
union PipelineResult
{
    Validated(double score, Explanation reasoning);
    Rejected(string violation);
    Inconclusive(string[] missingInputs);
    Unstable(Contradiction[] conflicts);
}

record Explanation(string Summary, string[] Steps);
record Contradiction(string SourceA, string SourceB, string Detail);
```

Pipeline composition with LINQ mirrors the F# computation expression pattern in tars IxQL:

```csharp
IEnumerable<PipelineResult> RunPipeline(IEnumerable<ChordInput> inputs) =>
    inputs
        .Select(Validate)
        .Select(ApplyHarmonicRules)
        .Select(CheckGovernanceGate);
```

---

## Governance Gates

Each governance gate corresponds to a constitutional article. `GateResult` encodes the Article 7 (Auditability) requirement — every rejection carries an article reference and explanation. `NeedsReview` maps to the >= 0.5 confidence threshold requiring confirmation.

```csharp
union GateResult
{
    Passed;
    Failed(Article article, string explanation);
    NeedsReview(double confidence, string reason);
}

enum Article
{
    Truthfulness = 1, Transparency, Reversibility, Proportionality,
    NonDeception, Escalation, Auditability, Observability,
    BoundedAutonomy, StakeholderPluralism, EthicalStewardship
}
```

Gate evaluation chains cleanly:

```csharp
GateResult EvaluateAll(MusicAction action) =>
    CheckTruthfulness(action) is GateResult.Failed f ? f :
    CheckProportionality(action) is GateResult.Failed f2 ? f2 :
    CheckBoundedAutonomy(action) is GateResult.NeedsReview nr ? nr :
    GateResult.Passed;
```

---

## Music Domain

### HarmonicFunction

Models Roman-numeral harmonic analysis with recursive secondary and borrowed chords. The recursive `Secondary` case (e.g., V/V) and `Borrowed` case (modal interchange) require discriminated unions — class hierarchies become unwieldy at this depth.

```csharp
union HarmonicFunction
{
    Tonic(ChordQuality quality);
    Subdominant(ChordQuality quality);
    Dominant(ChordQuality quality, bool hasSeventh);
    Secondary(HarmonicFunction applied, HarmonicFunction target);
    Borrowed(Mode sourceMode, HarmonicFunction function);
}
```

Pattern matching for display:

```csharp
string RomanNumeral(HarmonicFunction f, Key key) => f switch
{
    HarmonicFunction.Tonic(var q)         => q == ChordQuality.Major ? "I" : "i",
    HarmonicFunction.Subdominant(var q)   => q == ChordQuality.Major ? "IV" : "iv",
    HarmonicFunction.Dominant(_, true)    => "V7",
    HarmonicFunction.Dominant(_, false)   => "V",
    HarmonicFunction.Secondary(var a, var t) =>
        $"{RomanNumeral(a, key)}/{RomanNumeral(t, key)}",
    HarmonicFunction.Borrowed(var m, var fn) =>
        $"({m}) {RomanNumeral(fn, key)}",
};
```

### VoicingResult

Guitar voicing calculations have three distinct outcomes: an optimal voicing, a playable-but-stretched voicing, or an impossible arrangement (no fingering exists within human reach). The `Stretch` value on `Playable` encodes fret-span in semitones; `Impossible` carries a diagnostic string for the UI.

```csharp
union VoicingResult
{
    Optimal(Voicing voicing);
    Playable(Voicing voicing, Stretch fretSpan);
    Impossible(string diagnostic);
}

record Voicing(int[] Frets, Finger[] Fingering);
record Stretch(int SemitoneSpan, bool RequiresBarre);
```

---

## Relationship to tars F# Discriminated Unions

F# has had DUs since its inception. C# 15 unions are semantically equivalent, enabling:

- Shared domain types between tars (F#) and ga (C#) across the Galactic Protocol
- Tetravalent `Conclusion` union mirrors `type Conclusion = True of float | False of string | Unknown of string | Contradictory of string * string`
- IxQL results are type-safe in both languages — JSON serialization shape is identical
- Galactic Protocol messages can embed union-typed tetravalent conclusions without polymorphic workarounds

---

## Migration Path

### Prerequisites

1. Upgrade ga to **.NET 11 Preview 3+** (first release with `union` keyword)
2. Verify C# 15 LangVersion in all `.csproj` files: `<LangVersion>preview</LangVersion>`
3. Pin the SDK version in `global.json`:

```json
{
  "sdk": { "version": "11.0.100-preview.3", "rollForward": "latestPatch" }
}
```

### Step-by-Step

| Step | Action |
|------|--------|
| 1 | Upgrade all ga projects to `net11.0` TFM |
| 2 | Set `<LangVersion>preview</LangVersion>` |
| 3 | Replace `OneOf<T1, T2, ...>` usages with `union` declarations |
| 4 | Replace F#-style result types (`Result<T, E>`) with domain-specific unions |
| 5 | Port tetravalent class hierarchy to `union Conclusion` |
| 6 | Add exhaustive `switch` expressions — compiler enforces completeness |
| 7 | Remove `OneOf` NuGet package references |
| 8 | Update Galactic Protocol contract schemas to reflect union shapes |

### OneOf Replacement Pattern

Before (OneOf library):

```csharp
OneOf<Validated, Rejected, Inconclusive> result = pipeline.Run(input);
result.Switch(
    v => Console.WriteLine($"OK: {v.Score}"),
    r => Console.WriteLine($"Rejected: {r.Violation}"),
    i => Console.WriteLine($"Inconclusive: {string.Join(", ", i.Missing)}")
);
```

After (C# 15 union):

```csharp
PipelineResult result = pipeline.Run(input);
Console.WriteLine(result switch
{
    PipelineResult.Validated(var score, var exp) => $"OK: {score} — {exp.Summary}",
    PipelineResult.Rejected(var v)               => $"Rejected: {v}",
    PipelineResult.Inconclusive(var missing)     => $"Inconclusive: {string.Join(", ", missing)}",
    PipelineResult.Unstable(var conflicts)        => $"Unstable: {conflicts.Length} conflicts",
});
```

---

## References

- .NET 11 Preview 3 release notes (C# 15 discriminated unions)
- `logic/tetravalent-logic.md` — T/F/U/C specification
- `constitutions/default.constitution.md` — Articles 1-11 (confidence thresholds, transparency requirements)
- `docs/superpowers/specs/2026-03-22-fuzzy-enum-du-design.md` — FuzzyDU design
- Issue #131 — tars IxQL computation expressions (F# DU counterpart)
- Issue #103 — ix CLI readiness (dependency for Hyperlight phase 1)
