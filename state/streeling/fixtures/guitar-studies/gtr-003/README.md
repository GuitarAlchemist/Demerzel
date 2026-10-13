# C-major voicing comparison for GAA-004 and GTR-003

`voicing-comparison.json` contains three hand-checked **teaching shapes** in
standard tuning, written from low E to high E. They are not captured output
from GA's generator. `-1` mutes a string, `0` plays an open string, and positive
integers are fret numbers. Notes and positive-fret spans can be checked with a
guitar or a fretboard map. Each shape sounds C, E, and G; none proves the
position is comfortable for a particular hand.

The project behavior is anchored to GA commit
`dc2e74cbd992a298f67efb928b5b3754615e1924`:

- `Apps/ga-server/GaApi/Services/VoicingFilterService.cs` parses a chord,
  generates candidates, records frets/difficulty/barre information, and sorts
  results by ascending `DifficultyScore`. It does not promise that these exact
  three teaching shapes appear in every query result.
- `Apps/ga-server/GaApi/Services/VoicingComfortService.cs` ranks by the span of
  positive frets and optionally excludes its own definition of a full barre.
- `Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs`
  computes difficulty from physical fret distance, open strings, distinct
  frets, and a three-adjacent-strings barre heuristic. The comfort service's
  full-barre predicate instead needs four fretted strings at the lowest fret.
- `Tests/Apps/GaApi.Tests/Services/VoicingFilterServiceTests.cs` verifies known
  chord queries, difficulty ordering, and filter behavior;
  `VoicingComfortServiceTests.cs` verifies stretch and barre filtering.

On 2026-10-05, the two test classes passed 18/18 in the local GA checkout with
`dotnet test Tests/Apps/GaApi.Tests/GaApi.Tests.csproj --no-build --filter
"FullyQualifiedName~VoicingFilterServiceTests|FullyQualifiedName~VoicingComfortServiceTests"`.
That run used an existing test binary; it did not rebuild GA from source.

To reproduce the learner comparison, first inspect the three fixed shapes,
then query GA for `C` in a build of the pinned revision and record two returned
fret arrays, score, and barre fields. Check the service's string ordering before
translating an array into a low-to-high diagram. A guitar-playing check and
musician feedback remain necessary before calling either shape comfortable.
