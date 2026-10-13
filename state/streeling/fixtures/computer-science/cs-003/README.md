# CS-003 chord-symbol boundary corpus

`chord-symbol-corpus.json` is a small teaching oracle, not a claim that the current GA parser has been fixed. Its current-behavior column is a source trace from `Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs` and `Common/GA.Domain.Core/Theory/Harmony/Chord.cs` in the local GA checkout on 2026-10-04. Pin a GA commit and execute the corpus before publication.

The path into the user interface is `Apps/ga-server/GaApi/Services/VoicingFilterService.cs` to `Apps/ga-server/GaApi/Controllers/ContextualChordsController.cs`. The service returns voicings after `TryParse`; the controller returns `400 Bad Request` only for an `ArgumentException`. Thus a symbol silently interpreted as a major triad can reach `200 OK` with the requested text retained even when its musical meaning was lost.

The fixture distinguishes malformed syntax, unknown suffix, valid but unimplemented notation, and a supported chord. The desired result for `C7b5` and `C/E` is deliberately two-valued: implement their complete semantics or reject them explicitly. It is never acceptable to preserve the original symbol while inventing a different chord. A proposed regression test should assert the formula or bass as well as the presence of a `Chord` object.

This fixture does not prescribe a public API change. A future code slice should choose one canonical parser, preserve `Result` or a similarly explicit error at the domain boundary, and map only documented invalid-input cases to the endpoint's user-facing response. Check both `ChordSymbolParser` and `Chord.TryFromSymbol`: the latter already returns `false` for unknown suffixes, but supports a narrower vocabulary. Do not silently replace one parser with the other without a compatibility corpus.
