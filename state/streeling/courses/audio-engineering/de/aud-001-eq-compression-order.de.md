---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "EQ- und Kompressionsreihenfolge an einem Gitarrensignal prüfen"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-004
version: "1.1.0"
---

# EQ- und Kompressionsreihenfolge an einem Gitarrensignal prüfen

> **Fachbereich Audiotechnik** | Mittelstufe | 35 Minuten | Überarbeiteter deutscher Entwurf; fachliche, didaktische und sprachliche Prüfung sowie Veröffentlichung ausstehend

## Lernziele und Projektfrage

Du unterscheidest einen Filter von einem pegelabhängigen Prozessor, zeigst die Bedeutung ihrer Reihenfolge durch eine kleine Rechnung und entwirfst einen Offline-Vergleich, den eine künftige Kompressorimplementierung widerlegen könnte. **Projektfrage:** Wenn GA eine Aufnahme der offenen E2-Saite oder den Render seiner Gitarrenengine bearbeiten möchte, ändert eine gewählte EQ *vor* der Kompression Attack und Pegelverlauf gegenüber derselben EQ *nach* der Kompression? Für eine Entscheidung braucht es Messungen am selben Eingangssignal statt einer allgemeinen Regel darüber, welche Reihenfolge natürlicher klingt.

Die [GAS-001-Fixture](../../../fixtures/guitar-acoustics/gas-001/README.md) enthält ein konkretes Paar: eine aufgenommene offene E2 und ein nativ von GA erzeugtes E2, jeweils als vier Sekunden lange Mono-WAV-Datei mit 44.100 Hz. Der erste Anschlag der Aufnahme beginnt **ungefähr bei 1.1 s**, ein weiterer liegt bei **2.75 s**; der Render beginnt bei Dateizeit null. Die [Fixture-Messungen](../../../fixtures/guitar-acoustics/gas-001/measurements.json) zeigen Unterschiede in Teiltonverhältnissen und Abklingen in ausgewählten Fenstern. Sie bewerten weder Realismus noch belegen sie, dass eine Datei Kompression benötigt. Bewahre die Original-WAVs unverändert auf. Für diese Lektion dient die *Aufnahme* als vorgeschlagener erster Eingang; der Render kann später separat gekennzeichnet wiederholt werden. Ein Unterschied zwischen bearbeiteter und unbearbeiteter Datei darf nicht der Prozessorreihenfolge zugeschrieben werden.

Die [GA-Browser-Audioengine am festgelegten Commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) lädt die WASM-Engine in einen [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), verbindet ihn mit dem Ausgang und bietet einen MediaRecorder-Pfad. Der GAS-001-Render stammt aus einem **nativen Build desselben Rust-Quellcodes**, nicht aus einer Worklet-Aufnahme. Dieser Code belegt den Gitarrensignalweg, keine EQ/Kompressor-Kette im Demo. Bei [IX-Commit `bd1336b`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) stellt `FirFilter` Tiefpass- und Hochpassentwurf sowie ein `apply` für Abtastwerte bereit. Das kann ein Baustein für Offline-Filterung sein. Die festgelegten Artefakte belegen keine Kompressorimplementierung; diese müsste vor einem echten A/B-Vergleich spezifiziert und geprüft werden.

## 1. Beide Operationen genau angeben

Ein FIR-Filter ist linear: Bei Koeffizienten `h` lautet seine Ausgabe `E(x)[n] = Σ_k h[k] x[n-k]`, mit ausdrücklich festgelegtem Randverhalten. IXs `FirFilter::apply` beginnt mit einer auf null gesetzten Ausgabe und berücksichtigt nur Eingangswerte mit nicht negativem Index. Ein Tief- oder Hochpass kann den Pegel am nachfolgenden Detektor ändern. Das genaue Verhalten hängt von den Koeffizienten ab; ein Filter kann auch einen Anschlag verschieben oder verwischen. Jede Filtereinstellung „korrigierende EQ“ zu nennen belegt keine Verbesserung des Gitarrensignals.

Ein Kompressor ist **pegelabhängig**. Seine Verstärkung hängt vom Eingang und bei üblichen Bauformen von einer Detektorhüllkurve mit Attack- und Release-Zustand ab. Die Wellenform kann durch Schwelle, Verhältnis, Detektortyp, Zeitkonstanten, Kanalkopplung, Makeup-Gain und Initialisierung verändert werden. Diese Angaben müssen festgehalten werden. Ein Kompressor ist nicht automatisch frequenzselektiv: Ein Vollbanddetektor reagiert auf den Pegel der Eingangswellenform, zu dem mehrere Teiltöne beitragen können. „Er hört 200 Hz“ ist eine vereinfachte Aussage und kein Nachweis dafür, welcher Anteil die Pegelreduktion auslöste. Sidechain-Filter, Multibandkompression und dynamische EQ wären andere Versuche.

Sei `E` die gewählte EQ und `C` der Kompressor. Die vorgeschlagenen Ketten sind `A = E(C(x))` (**Comp→EQ**) und `B = C(E(x))` (**EQ→Comp**). Beide müssen dasselbe `x`, dieselben EQ-Koeffizienten und Kompressorparameter sowie dieselbe Abtastrate und Kanalform verwenden. In A erhält `C` das rohe `x`, in B das gefilterte `E(x)`. Die nachgeschaltete EQ in A kann eine bereits getroffene Detektorentscheidung nicht rückgängig machen. In B kann der Kompressor auf durch EQ erzeugte oder entfernte Spitzen reagieren. Keine Reihenfolge ist universeller Standard; Klangabsicht und gemessene Vor- und Nachteile entscheiden.

### Übung 1: Detektoreingang bestimmen

Was erreicht `C` in A und B? Falls die EQ einen ausgewählten Gitarrenteilton verstärkt: In welcher Kette *könnte* sich dadurch die Gain-Reduction ändern?

> **Antwort:** In A erhält `C` das ungefilterte `x`, in B `E(x)`. Die Teiltonverstärkung kann den Vollbanddetektor in B direkt beeinflussen. In A folgt die EQ erst nach dem Kompressor und kann dessen frühere Gain-Entscheidung nicht ändern. Das beschreibt einen Kausalweg, weder Hörbarkeit noch Größe der Pegelreduktion.

## 2. Reihenfolgenabhängigkeit mit einer synthetischen Fixture zeigen

Verwende das bewusst einfache **synthetische** Vier-Sample-Signal `x=[0,2,0,0]` mit Nullvorgeschichte. Definiere den FIR-Filter `E` durch `h=[0.5,0.5]`, sodass `E(x)[n]=0.5x[n]+0.5x[n-1]` für verfügbare Samples gilt. Dieser Mittelwert aus zwei Taps ist ein mathematisches Tiefpassbeispiel, **keine** empfohlene Gitarren-EQ und nicht die Ausgabe von IXs `lowpass`-Entwurf. Definiere einen gedächtnislosen Lehr-Kompressor mit Schwelle `T=1`, Verhältnis `R=2:1`, ohne Makeup-Gain und ohne Attack/Release: `C(v)=sign(v) × (|v| if |v|<=1 else 1+(|v|-1)/2)`. Er bildet die positive Probe `2` auf `1.5` ab. Ein echter Hüllkurvenkompressor hätte weiteren Zustand und könnte andere Werte liefern.

Für A gilt `C(x)=[0,1.5,0,0]`, danach `E(C(x))=[0,0.75,0.75,0]`. Für B gilt `E(x)=[0,1,1,0]`, danach `C(E(x))=[0,1,1,0]`, denn kein gefilterter Nichtnullwert übersteigt die Schwelle. Die Ausgaben unterscheiden sich an den Positionen 1 und 2 um `0.25`. Das ist ein exaktes Gegenbeispiel zu `E∘C = C∘E` für die definierten Operatoren. Es ist **keine** Messung der GAS-001-Aufnahme, keine Vorhersage für ein unbestimmtes Plugin und kein Nachweis, dass B besser klingt.

Auch die verschiedenen Spitzen, `0.75` für A und `1` für B, warnen vor einem Hörvergleich bei unkontrollierter Lautstärke. Lege einen Wiedergabepegelabgleich **nach** jeder vollständigen Kette fest und protokolliere seine Verstärkung. Verändere nicht die Schwellen getrennt, um ähnliche Gain-Reduction zu erzwingen: Das wäre eine andere Versuchsfrage. Wenn beide Ketten in einer echten Passage unter der Schwelle bleiben, können sie trotz des synthetischen Gegenbeispiels gleich oder nahezu gleich sein.

### Übung 2: Beide Ketten berechnen

Schreibe mit den festgelegten `x`, `h` und `C` die Ausgaben A und B auf. Wie groß ist `B[1]-A[1]`, und was folgt daraus?

> **Antwort:** `A=[0,0.75,0.75,0]`; `B=[0,1,1,0]`; `B[1]-A[1]=0.25`. Die angegebenen Operatoren kommutieren auf diesem synthetischen Eingang nicht. Daraus folgt weder ein Hörurteil noch ein Ergebnis für einen echten Hüllkurvenkompressor oder die Gitarren-WAV.

### Übung 3: Den Rand behandeln

Wie lauten bei Nullvorgeschichte und `h=[0.5,0.5]` die Werte `E([2,0])[0]` und `E([2,0])[1]`? Weshalb müssen Randbehandlung und Latenz dokumentiert sein?

> **Antwort:** Beide sind `1`. An Index 0 trägt der fehlende Vorgänger null bei; an Index 1 ist der vorherige Eingangswert `2`. Anderes Padding oder Warmlaufen würde die Attack-Samples ändern. Längere praktische FIR-Filter können Gruppenlaufzeit verursachen. Richte Ausgaben aus und dokumentiere die Randregel, bevor du eine Verschiebung des Spitzenzeitpunkts deutest.

## 3. Einen widerlegbaren Gitarren-A/B-Versuch entwerfen

Dies ist ein **vorgeschlagener Offline-Versuch, kein ausgeführter Lauf**. Beginne mit der Aufnahme `deb-low-e-open.wav` im [Fixture-Verzeichnis](../../../fixtures/guitar-acoustics/gas-001/README.md), deren SHA-256 `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248` lautet. Dekodiere ihre Mono-float32-WAV-Samples einmal und bewahre die ursprünglichen Bytes. Erfasse Decoder, Abtastrate, Eingangshash und ungefähren ersten Anschlag; prüfe die Wellenform, bevor du ein Vergleichsfenster festlegst, das den zweiten Anschlag ausschließt. Später kann `ga-engine-e2-open-4s.wav` getrennt getestet werden, denn dieser native Render hat einen anderen Beginn und andere Herkunft.

Bevor der künftige Kompressor implementiert wird, lege seine Parameter fest: Schwelle in dBFS, Verhältnis, Einheiten für Attack und Release, Peak- oder RMS-Detektor, Lookahead, Knee, Makeup-Gain, Zustandsreset und Verhalten bei der ersten Probe. Pinne Code-Revision und Tests. Verwende eine deterministische EQ: Entweder veröffentliche wörtliche FIR-Koeffizienten oder pinne den [IX-Filtercode](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) und protokolliere Grenzfrequenz, Ordnung, Koeffizienten und Randverhalten. Verwende in beiden Ketten *dieselben* Einstellungen und setze den Kompressorzustand vor jedem Render getrennt zurück. Exportiere verlustfreie A- und B-WAVs mit derselben Abtastrate und speichere Gain-Reduction-Verlauf, Sample-Anzahl und Verarbeitungsmanifest. Behaupte nicht, GA oder IX stelle diese kombinierte Kette bereits bereit.

Lege das Fenster für den ersten Anschlag relativ zum **ungefähr bei 1.1 s** liegenden Beginn der Aufnahme fest und schreibe den gewählten Sample-Index ins Manifest. Berichte für jede Kette Spitzensample und -zeit, Kurzzeit-RMS oder Hüllkurve am Anschlag, späteres RMS und Gain-Reduction-Verlauf. Gleiche für das Hören den Ausgangspegel ab und protokolliere die Verstärkung, damit Rohmessungen und abgeglichene Messungen getrennt bleiben. Vermeide Clipping nach Makeup-Gain oder Pegelabgleich. Wenn FIR-Latenz und Bypass-Pfad unterschiedlich sind, richte die Signale vor einem Vergleich der Spitzenzeit mit dokumentierter Verzögerung oder Kreuzkorrelation aus. Ein später genehmigter Hörtest sollte Kennzeichnungen verbergen, Reihenfolge zufällig wählen und „kein wahrnehmbarer Unterschied“ zulassen; er ist von der numerischen Prüfung getrennt.

Die enge Hypothese „Die EQ-Position ändert diese Gitarrenpassage bei diesen festgelegten Einstellungen“ wäre **widerlegt**, wenn A und B innerhalb einer zuvor festgelegten numerischen Toleranz Sample für Sample gleich bleiben oder ein scheinbarer Unterschied nach Korrektur von Ausrichtung, Reset oder Pegelbehandlung verschwindet. Falls sie sich unterscheiden, untersuche Detektoreingang und Gain-Reduction-Verläufe, um den Mechanismus zu bestimmen. Ein Unterschied beweist keine größere Natürlichkeit einer Reihenfolge. Bei neutraler EQ oder nicht ausgelöster Kompression ist ein Nullbefund plausibel und nützlich. Eine Aussage über bessere Bewahrung des Anschlags bräuchte eine festgelegte Attack-Metrik, Richtung, Toleranz und einen Hörtest, falls Wahrnehmung Teil der Aussage ist.

### Übung 4: Die Fixture gültig halten

Ein vorgeschlagener Versuch bearbeitet die Aufnahme bei Dateizeit `0.0–1.0 s`, vergleicht sie mit dem Render im selben Intervall und folgert, EQ→Comp erhalte den Anschlag besser. Nenne zwei unabhängige Probleme.

> **Antwort:** Der erste aufgenommene Anschlag liegt erst ungefähr bei `1.1 s`; `0.0–1.0 s` enthält überwiegend Vorlauf, während der Render bei null beginnt. Die Fenster sind nicht am Anschlag ausgerichtet. Außerdem isoliert der Vergleich zweier verschiedener Quelldateien die Reihenfolge nicht: A und B müssen **dieselbe Quell-WAV** nutzen. Keine der beiden Dateien ist eine validierte Realismus-Benchmark.

### Übung 5: Die nächste Prüfung wählen

Ein künftiger Lauf findet `0.2 dB` Unterschied im RMS-Fenster des ersten Anschlags. Die Ausgaben sind aber nicht ausgerichtet und das Manifest mit den Kompressoreinstellungen fehlt. Begründet das eine bevorzugte Reihenfolge? Welche Nachweise sind nötig?

> **Antwort:** Nein. Sichere Eingangshash und Fenster, veröffentliche Kompressorversion und Einstellungen, prüfe getrennte Zustandsresets, richte Latenz und Anschlag aus und bestätige gleiche EQ-Koeffizienten ohne Clipping. Wiederhole dann den Versuch und vergleiche Rohmessungen und Gain-Reduction-Verläufe. Bei einer Klangqualitätsaussage gleiche den Wiedergabepegel nach der Bearbeitung für einen separaten Blindtest ab. `0.2 dB` allein benennt weder die Ursache noch begründet es eine Präferenz.

## Evidenz und Grenzen

- Das [GAS-001-Fixture-README](../../../fixtures/guitar-acoustics/gas-001/README.md) dokumentiert aufgenommene und nativ gerenderte E2-Dateien, Hashes, Herkunft, ungefähre Anschläge und Messgrenzen. Die [GAS-001-Lektion](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) und ihre Messungen betreffen den *rohen* Vergleich, keinen EQ/Kompressionsversuch.
- Der festgelegte [GA-Browser-Pfad](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) mit [Worklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) belegt den Demo-Signalweg, der [IX-FIR-Code](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) eine verfügbare Filteroperation. Sie belegen weder einen implementierten Kompressor noch einen Reihenfolgentest oder eine bearbeitete WAV.
- Die Vier-Sample-Rechnung ist synthetisch. A/B-Versuch, Parameter und Metriken sind Vorschläge. Für diese Lektion wurde kein Kompressor gebaut oder ausgeführt; es gibt hier keine bearbeitete Gitarren-WAV, kein Blindhörurteil und keine produktive Routingentscheidung. Fachliche, didaktische und sprachliche Prüfung, Learn-Synchronisierung und Build sowie anonymer öffentlicher Abruf stehen aus. Der Forschungseintrag vom 2026-03-23 bleibt ein historisches vokalbezogenes Artefakt; diese Fassung verwendet den neuen Zyklus.
