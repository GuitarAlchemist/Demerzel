---
module_id: phy-003-sampling-aliasing-guitar-engine
department: physics
course: Abtastung und Aliasing an der Grenze der GA-Gitarrenengine
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-003
version: "0.1.0"
---

# Abtastung und Aliasing an der Grenze der GA-Gitarrenengine

> **Fachbereich Physik** | Mittelstufe | 35 Minuten | Deutscher Entwurf; Prüfung und Veröffentlichung ausstehend

## Lernziele

Du berechnest eine Nyquist-Grenze und eine Aliasfrequenz, bestimmst die Abtastrate, die die Rust-Engine von GA tatsächlich erhält, und entwirfst einen Offline-Test für Aliasing, ohne ein berechnetes Risiko als gemessenen Fehler auszugeben. [PHY-001](../de/phy-001-science-of-guitar-sound.de.md) führt Gitarrenharmonische ein. [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) behandelt Analysefenster für zeitlich veränderliche Noten. Hier setzt die Frage früher in der Signalkette an: **Welche kontinuierlichen Frequenzen kann ein abgetastetes Gitarrensignal darstellen, und was muss vor Aufnahme, Synthese oder Ratenumwandlung geschehen?**

## 1. Die Rate an das Artefakt binden, nicht an den Notennamen

Die [festgelegte GAS-001-Fixture](../../../fixtures/guitar-acoustics/gas-001/README.md) enthält vier Sekunden einer aufgenommenen leeren tiefen E2-Saite und einen vier Sekunden langen nativen Render der GA-Rust-Engine. Beide Dateien sind mono mit **44.100 Samples pro Sekunde**. Der Render ruft `engine_note_on(82.4069 Hz, 0.1)` auf; die E2-Bezeichnung der Aufnahme ist ein Datensatzlabel, keine Frequenzmessung. Der Render entstand mit einem nativen Build, **nicht** durch Aufnahme des Browser-AudioWorklets. Diese Herkunft ist bei der Untersuchung eines Audioartefakts wichtig.

Am GA-Commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) sendet die [Browser-Audiobrücke](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) `audioContext.sampleRate` an das [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js). Dieses ruft `engine_init(srToUse)` auf und kopiert die berechneten Mono-Samples in die Browser-Ausgabekanäle. Die [Rust-Engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) speichert die Rate und nutzt sie für Resonatorkoeffizienten und Verzögerungsleitungslängen. Die festgelegte 44,1-kHz-WAV belegt deshalb **nicht**, dass jede Browser-Sitzung mit 44,1 kHz läuft. Protokolliere die tatsächliche Kontextrate und den Aufnahmeweg, bevor du eine Browseraufnahme mit GAS-001 vergleichst.

Für die Dauer `T` gilt die Samplezahl `N = f_s T`. Vier Sekunden bei 44.100 Hz ergeben **176.400 Samples** je Monokanal, bei 48.000 Hz wären es **192.000**. Keine dieser Zahlen belegt eine korrekte Filterung des Analogeingangs oder aliasfreie Synthese.

### Übung 1

Jemand sieht den GAS-001-Render mit 44,1 kHz und behauptet: „Die GA-Browserengine läuft immer mit 44,1 kHz.“ Was stützen die Quellen tatsächlich, und was sollte ein Browsertest erfassen?

> **Antwort:** GAS-001 legt **seine nativ gerenderte WAV** auf 44.100 Hz fest. Die Browserbrücke übergibt `audioContext.sampleRate` an Worklet und Rust-Engine; ihr tatsächlicher Wert muss in der jeweiligen Sitzung beobachtet werden. Notiere Kontextrate, Ausgabe- oder Aufnahmerate und Codec, Engine-Revision und Aufnahmeweg. Eine native WAV ist keine Browseraufnahme.

## 2. Den darstellbaren Bereich vor den Harmonischen berechnen

Für ein gleichmäßig mit `f_s` abgetastetes reelles Signal ist die Nyquistfrequenz `f_N = f_s/2`: **22.050 Hz** bei 44.100 Hz und **24.000 Hz** bei 48.000 Hz. Ein ideales kontinuierliches, bandbegrenztes Eingangssignal mit Frequenzanteilen strikt unter `f_N` lässt sich grundsätzlich aus seinen Samples rekonstruieren. Bei realer Aufnahme muss ein Anti-Aliasing-Filter **vor** der Abtastung liegen und unter Nyquist einen Übergangsbereich haben. `f_N` ist eine mathematische Grenze, kein Versprechen eines perfekten Filters in Mikrofon, Wandler, Engine oder Export.

Die Zielgrundfrequenz der leeren tiefen E2-Saite beträgt `f_0 = 82.4069 Hz`. Ihr idealer ganzzahliger Teilton `k` läge bei `k f_0`; eine reale oder synthetisierte Gitarre muss weder alle Teiltöne besitzen noch sie exakt bei ganzzahligen Vielfachen halten. Bei 44,1 kHz liegt `267 f_0 = 22,002.6423 Hz` unter Nyquist und `268 f_0 = 22,085.0492 Hz` darüber. Bei 48 kHz verläuft die Grenze zwischen Teilton **291** (`23,980.4079 Hz`) und **292** (`24,062.8148 Hz`). Das sind *theoretische Indexgrenzen* für diese Grundfrequenz, keine Zählung hörbarer oder gemessener Teiltöne. In der Praxis braucht man Abstand von der exakten Grenze, weil Filter einen Übergangsbereich benötigen und die Implementierung zählt.

### Übung 2

Berechne für dasselbe ideale E2 die höchste ganzzahlige Harmonische strikt unter Nyquist bei 44,1 und 48 kHz. Beweist das, dass die Fixture diese Harmonischen enthält?

> **Antwort:** `floor(22,050 / 82.4069) = 267` und `floor(24,000 / 82.4069) = 291`. Die benachbarten Teiltöne 268 und 292 liegen über den jeweiligen Nyquistgrenzen. Die Rechnung beweist keinen erkennbaren 267. oder 291. Teilton in einer der WAV-Dateien. Für Pegelmessungen braucht man die Dateien, ein geeignetes Fenster, eine Rauschgrenze und ausdrücklich festgelegte Analysegrenzen.

## 3. Eine Aliasfrequenz von Hand berechnen

Die Abtastung einer kontinuierlichen Sinusschwingung mit `f` Hz liefert an ganzzahligen Indizes `n` die Werte `sin(2π f n / f_s)`. Addition oder Subtraktion ganzzahliger Vielfacher von `f_s` ergibt bis auf Vorzeichen oder Phase dieselben Samples. Für den Frequenzbetrag falte `f` anhand von Vielfachen von `f_s` in `[0, f_s/2]`; wähle also eine ganze Zahl `m`, für die `|f - m f_s|` in diesem Intervall liegt. Dies ist eine **synthetische Einzeltonrechnung**, keine Beobachtung aus GAS-001.

Betrachte einen kontinuierlichen Sinus bei **23.000 Hz**. Bei 44,1 kHz liegt er 950 Hz über Nyquist und faltet sich zu `|23,000 - 44,100| = 21,100 Hz`. Die abgetastete Folge entspricht einem 21.100-Hz-Sinus mit geändertem Vorzeichen oder geänderter Phase. Bei 48 kHz liegt 23.000 Hz unter der 24.000-Hz-Grenze und faltet sich nicht. Eine nachträgliche Umwandlung der 44,1-kHz-Aufnahme auf 48 kHz stellt das ursprüngliche 23.000-Hz-Signal nicht wieder her: Die Samples unterscheiden die beiden kontinuierlichen Ursprünge nicht.

Bei einer Gitarrenengine sind breitbandige Anregung durch Anschlag, nichtlineare Verarbeitung und hohe Teiltöne Gründe, die Grenze zu **prüfen**. Die [festgelegte Rust-Anregung](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) nutzt gefiltertes Rauschen in einer Verzögerungsleitung und verarbeitet Samples. Die Quellinspektion beweist kein hörbares oder messbares Alias in der Ausgabe. Eine höhere Rate kann die Aliasgrenze verschieben, verändert aber auch Puffergrößen und Rechenaufwand; sie ersetzt weder kontrollierte Bandbegrenzung noch Messungen.

### Übung 3

Eine vorgeschlagene Anregung enthält eine kontinuierliche Komponente bei 30.000 Hz. Wohin würde ein idealer Abtaster deren Alias bei 44,1 beziehungsweise 48 kHz abbilden?

> **Antwort:** Bei 44,1 kHz gilt `|30,000 - 44,100| = 14,100 Hz`; bei 48 kHz `|30,000 - 48,000| = 18,000 Hz`. Das sind Faltungen eines idealen Sinus, keine vorhergesagten Spektralspitzen der GA-Engine. Ein vorgeschalteter Anti-Aliasing-Filter kann die Komponente vor der Aufnahme dämpfen; ein digitaler Generator muss außerbandige Anteile vermeiden oder deren Faltung beherrschen.

### Übung 4

Jemand wandelt eine 44,1-kHz-Aufnahme mit einer 21,1-kHz-Spitze auf 48 kHz um und sagt: „Nun liegt Nyquist bei 24 kHz; der ursprüngliche 23-kHz-Ton ist wiederhergestellt.“ Erkläre den Fehler.

> **Antwort:** Die 44,1-kHz-Samplefolge ist sowohl mit einem 21,1-kHz- als auch einem 23-kHz-Ton vereinbar, bis auf Phasen- oder Vorzeichenwechsel. Ratenumwandlung kann die vorhandenen Daten interpolieren oder filtern, aber ihren kontinuierlichen Ursprung nicht erschließen. Verhindere die Faltung **vor** der ursprünglichen Abtastung durch analoge Anti-Aliasing-Filterung oder erzeuge bandbegrenzte digitale Inhalte mit der Zielrate.

## 4. Aus dem Risiko einen widerlegbaren GA-Test machen

Die [GAS-001-Messungen](../../../fixtures/guitar-acoustics/gas-001/measurements.json) enthalten Spitzen nahe E2 und einige niedrige Teiltöne, aber keine Untersuchung hochfrequenter Aliase. Eine Darstellung der beiden 44,1-kHz-WAV-Dateien allein verrät die ursprüngliche Frequenz eines Alias nicht: Eine Spitze unter Nyquist kann mehrere Ursachen haben. Die Aufnahme hat ihren ersten ungefähren Anschlag bei 1,1 s und einen weiteren bei 2,75 s, während der Render bei null beginnt. Erhalte am Anschlag ausgerichtete Intervalle vor einem Spektralvergleich; [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) erklärt dieses Zeitfensterproblem.

Ein Offline-Versuch sollte zunächst einen **bekannten synthetischen Referenzton** nutzen: Erzeuge einen 23-kHz-Sinus mit höherer Referenzrate, taste ihn mit 44,1 und 48 kHz bei dokumentierter Filterwahl ab und prüfe die vorhergesagte Faltung auf 21,1 kHz nur im absichtlich ungefilterten 44,1-kHz-Arm. Rendere anschließend dieselbe festgelegte GA-Enginequelle mit gleicher Note, Anschlagstärke, Profil und Dauer bei beiden Raten durch **native** Aufrufe oder erfasse beide Fälle im **Browser** mit protokollierter Rate; mische die Wege nicht stillschweigend. Speichere Eingabeeinstellungen, genauen Build, WAV-Hashes, Rate, Spitzenpegel und Spektralfenster. Vergleiche mit einer kontrollierten Referenz bei passender Rate über mehrere Noten und Anschlagstärken. Bewegt sich ein unerwarteter Ton beim Ratenwechsel wie vorhergesagt, untersuche seine Erzeugungsstufe; bleibt er bei derselben physikalischen Frequenz, wird die einfache Aliasannahme schwächer. Bestätige sie mit einer gezielten Codeänderung an der verdächtigen Stufe und wiederhole das Hören bei gleichem Pegel. Dieses Verfahren ist **vorgeschlagen**: Weitere Render, Aufnahmen und Hörtests wurden für diese Lektion **nicht** durchgeführt.

Für künftige Ratenumwandlungen dokumentiere Quell- und Zielrate, Durchlass- und Sperrbereich des Filters, Verzögerung, Clippingprüfungen und ob die Referenz vor oder nach verlustbehafteter Kodierung erfasst wurde. Die Browserbrücke besitzt einen optionalen [MediaRecorder-Weg](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js); setze dessen Blob nicht mit einer rohen 44,1-kHz-WAV gleich. Halte den Weg vom nativen Fixture-Render getrennt.

### Übung 5

In einem Engine-Render mit 44,1 kHz erscheint eine Spitze bei 21,1 kHz. Reicht das als Beweis für ein Synthesealias von 23 kHz? Nenne den nächsten entscheidenden Vergleich und eine Kontrolle.

> **Antwort:** Nein. Es könnte eine Komponente innerhalb des Bandes, ein Alias einer anderen außerbandigen Komponente oder ein Aufnahmefehler sein. Rendere dieselbe festgelegte Enginekonfiguration mit 48 kHz und vergleiche am Anschlag ausgerichtete Hochfrequenzspektren: Eine Quelle nahe 23 kHz sollte dort nahe 23 kHz erscheinen, während ihr 44,1-kHz-Alias nahe 21,1 kHz läge. Halte Engine-Revision, Note, Anschlagstärke, Profil und Aufnahmeweg konstant; untersuche die Signalstufe oder ergänze gezielte Bandbegrenzung, bevor du die Ursache zuschreibst. Die vorhergesagte Verschiebung ist ein **Test**, kein beobachtetes Ergebnis.

## Quellen und aktuelle Grenzen

- [Festgelegte GAS-001-Fixture, Herkunft und Raten](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) mit [lokalem README](../../../fixtures/guitar-acoustics/gas-001/README.md). Die Aufnahme wird dort **collegefishiesd** unter CC BY-SA 4.0 zugeschrieben; diese Lektion vervielfältigt das Audio nicht.
- GA-Commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo): [Browserbrücke](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) und [Rust-Engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs).
- Samplezahlen, Harmonischenindexgrenzen und die Einzeltonfaltungen oben sind direkte Berechnungen aus den genannten Raten und Frequenzen. Für PHY-003 wurden keine neuen Hochfrequenzalias-Messungen an GAS-001, Browseraufnahmen, unabhängige fachliche Prüfung, Lerntests, sprachliche Prüfung oder öffentliche Rücklesung durchgeführt.
