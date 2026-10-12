---
module_id: gas-003-decay-calibration-open-e
department: guitar-acoustics
course: "Einen Abklingtest für die leere E-Saite der GA-Gitarrenengine kalibrieren"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-12-003
version: "0.1.0"
---

# Einen Abklingtest für die leere E-Saite der GA-Gitarrenengine kalibrieren

> **Fachbereich Gitarrenakustik und Klangsynthese** | Mittelstufe | 40 Minuten | KI-Übersetzungsentwurf; Prüfung ausstehend

## Lernziele

Du unterscheidest eine *gemessene* Pegelabnahme von einem *Rust-Parameter*, berechnest die Differenz des fixierten Paars für die leere E-Saite, verfolgst den Rückkopplungskoeffizienten der Engine und entwirfst einen nativen Versuch mit genau einem veränderten Parameter, Widerlegungskriterium und Schutzprüfungen. [GAS-001](../en/gas-001-open-string-audio-evidence.md) dokumentiert das aufgenommene und das gerenderte Signal. [GAS-002](../en/gas-002-brightness-control-and-evaluation-gate.md) prüft eine Brightness-Hypothese anhand eines lokalen Obertonverhältnisses. Hier lautet die Frage: **Kann eine kontrollierte Änderung des GA-Decay-Werts die Pegelabnahme der leeren E-Saite an die Aufnahme annähern, ohne Anschlag, Tonhöhe oder andere Töne zu verschlechtern?** Für diese Lektion wurde noch kein Decay-Kandidat gerendert.

## 1. Mit der gemessenen Hüllkurve beginnen, nicht mit dem Regler

Das fixierte [GAS-001-Fixture](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) enthält zwei vier Sekunden lange Mono-WAVs bei 44.100 Hz: eine separat zugeschriebene akustische Aufnahme, die ihr Datensatz als leeres E2 bezeichnet, und einen **nativen** Render der GA-Rust-Engine beim Commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. Der Render nutzt das standardmäßige Gitarrenprofil 0 und `engine_note_on(82.4069 Hz, velocity 0.1)`. Er ist keine Aufnahme des Browser-AudioWorklets. Das [Fixture-README](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md) nennt WAV-Hashes, Provenienzgrenzen, Quelle und CC-BY-SA-4.0-Zuschreibung der Aufnahme.

Das gespeicherte [Mess-JSON](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) gibt für die Differenz spätes minus frühes RMS **−3.9 dB** für die Aufnahme und **−1.1 dB** für den Render an. Das [Messskript](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) verwendet Fenster bei 0.2–0.4 s und 1.0–1.2 s **nach dem ersten Anschlag jeder Datei**. Der erste Anschlag der Aufnahme liegt ungefähr bei 1.1 s, ein weiterer bei 2.75 s; der Render beginnt bei null. Die Aufnahmefenster liegen daher ungefähr bei **1.3–1.5** und **2.1–2.3 s** Dateizeit, vor dem zweiten Anschlag. Das sind keine Abklingkonstanten der gesamten Datei.

Die ausgewählte Pegelabnahme des Renders ist **um 2.8 dB weniger negativ**: `−1.1 − (−3.9) = +2.8 dB`. Der absolute Fehler gegenüber der aufgenommenen Änderung beträgt `|−1.1 − (−3.9)| = 2.8 dB`. Beide Werte sind bereits auf Zehntel gerundet. Die WAVs unterscheiden sich im Anfangspegel sowie bei Instrument, Mikrofon, Raum und Anschlag. Daher sind *Änderungen innerhalb* jeder Datei hier sinnvoller als ein direkter Vergleich absoluter RMS-dBFS-Werte. Auch diese Differenz verrät weder den verursachenden Engine-Parameter noch die Hörpräferenz.

### Übung 1 — Die Differenz lesen

Berechne anhand der gespeicherten Werte die vorzeichenbehaftete Differenz Render minus Aufnahme für spätes minus frühes RMS und den absoluten Fehler. Bedeutet ein Fehler von 2.8 dB, dass der ganze Render 2.8 dB lauter ist?

> **Antwort:** `−1.1 − (−3.9) = +2.8 dB`; der absolute Fehler beträgt `2.8 dB`. Der Renderpegel fällt zwischen den beiden anschlagsbezogenen RMS-Fenstern weniger stark. Das ist weder ein Lautheitsvergleich der ganzen Dateien noch ein Beleg für Hörpräferenz.

### Übung 2 — Den zweiten Anschlag ausschließen

Wo liegen die beiden Fenster in der Aufnahmedatei, wenn ihr erster Anschlag ungefähr bei 1.1 s liegt? Weshalb eignet sich ein spätes Fenster ab 2.8 s nicht zur Untersuchung des ersten Tons?

> **Antwort:** Das frühe Fenster liegt ungefähr bei `1.1 + [0.2, 0.4] = 1.3–1.5 s`, das späte bei `1.1 + [1.0, 1.2] = 2.1–2.3 s`. Ein Fenster ab 2.8 s folgt auf den weiteren Anschlag bei etwa 2.75 s und mischt ein neues Ereignis in die vermeintliche Abklingmessung. Weil der erste Anschlag nur näherungsweise bestimmt wurde, sollte man die Analyse vor einer starken Aussage mit leicht verschobener Anschlagszeit wiederholen.

## 2. Rust-Parameter und wirksamen Koeffizienten verfolgen

In der fixierten [GA-Rust-Engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) beginnt `Engine::new` mit `decay = 0.9968`, wählt danach aber das Standardprofil 0, das den **Basis-Decay auf 0.9978** setzt. Das exportierte `engine_set_decay` begrenzt einen angeforderten Wert auf `[0.95, 0.9999]`. Wähle das Profil **vor** dem Setzen des Kandidaten: Eine spätere Profilwahl überschreibt Decay und weitere Regler. Der [Fixture-Renderer](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py) ruft `engine_init` und `engine_note_on`, aber nicht `engine_set_decay` auf. Für einen Kandidaten braucht es eine dokumentierte Erweiterung oder einen separaten Testaufbau. Hier wird kein Kandidatenlauf behauptet.

Im Renderzyklus sind diese Ausdrücke maßgeblich:

```text
f_norm = clamp((voice_frequency_hz - 82) / (330 - 82), 0, 1)
voice.sustain = min(0.995 + 0.006 * (1 - f_norm), 0.9998)  # assigned at note excitation
feedback_decay = (base_decay + 0.0025 * (1 - f_norm)) * voice.sustain
```

Für die nominellen `82.4069 Hz` des Fixtures gilt `f_norm ≈ 0.00164073`. Der unbegrenzte Sustain-Ausdruck ergibt etwa `1.00099016`; deshalb ist `voice.sustain = 0.9998`. Mit Basis `0.9978` ergibt sich `(0.9978 + 0.0025 × (1 − 0.00164073)) × 0.9998 ≈ 1.00009584`. Ein **vorgeschlagener** Basiswert von `0.9976` ergibt etwa **0.99989588**. Beide Basiswerte liegen innerhalb der Setter-Grenzen.

Dies sind **aus dem Quellcode berechnete Rückkopplungskoeffizienten**, keine gemessenen Abklingraten der Hüllkurve. Die Schleife kombiniert außerdem Verzögerungsleitungssamples, Allpass-Dispersion, einen zustandsbehafteten Tiefpass mit Brightness-Mischung, Anschlagsrauschen, Resonatoren und Hall. Ein Koeffizient knapp über eins in einem Ausdruck beweist **weder** instabilen Ausgang **noch** einen hörbaren Fehler. Ein kleinerer Koeffizient sagt auch keine bestimmte dB-Änderung im WAV voraus. Die Ausgabe muss nach fester Methode gemessen werden.

Das gesonderte `attack_decay` steuert das Anschlagsrauschen, `reverb_mix` den Nachhall und Brightness die Rückkopplungsmischung. Ändere diese nicht zugleich mit dem Decay-Kandidaten, sonst wird die Ursache jeder beobachteten Wirkung mehrdeutig. GAS-002 behandelt Brightness; hier bleibt sie konstant.

### Übung 3 — Rechnen und die Schlussfolgerung begrenzen

Welche Sustain-Obergrenze gilt bei `82.4069 Hz`, und welche näherungsweisen wirksamen Rückkopplungskoeffizienten ergeben die Basiswerte `0.9978` und `0.9976`? Beweist der erste Wert über eins, dass das gespeicherte GA-WAV mit der Zeit lauter wird?

> **Antwort:** `f_norm ≈ 0.00164073`; der unbegrenzte Sustain-Ausdruck übersteigt `0.9998`, also greift die Grenze `0.9998`. Die Formel ergibt ungefähr `1.00009584` bei `0.9978` und `0.99989588` bei `0.9976`. Nein: Das ist ein Koeffizient in einem gefilterten, zustandsbehafteten, resonierenden und verhallten System. Das gespeicherte WAV hat in den ausgewählten Fenstern tatsächlich `−1.1 dB`; der Koeffizient allein sagt seine Hüllkurve nicht voraus.

## 3. Einen Versuch mit einem Parameter vorab festlegen

Ein kontrollierter nativer Versuch würde **dieselbe fixierte Rust-Revision** kompilieren und für jeden Arm bei 44.100 Hz eine frische Engine initialisieren. Profil 0, E2-Frequenz `82.4069 Hz`, Velocity `0.1`, vier Sekunden, Compiler, WAV-Kodierung und alle anderen Einstellungen bleiben gleich. Der Basisarm verwendet `0.9978`. Im Kandidatenarm erfolgt `engine_set_decay(0.9976)` **nach** Initialisierung und Profilwahl, **vor** `engine_note_on`. Halte Reihenfolge und Wert, beide WAV-Hashes und die gewählte Anschlagszeit fest. Der Quellcode setzt beim Erzeugen einen festen Rauschseed; frische Engines und identische Builds verhindern dennoch Zustandsübernahme. Der aktuelle Renderer besitzt keine Decay-Option: Passe ihn an oder ersetze ihn und prüfe das Skript vor jeder empirischen Behauptung. Ein nativer Vergleich zertifiziert nicht das Browser-AudioWorklet; wenn dieses ausgeliefert wird, muss es separat geprüft werden.

Verwende für beide Arme dasselbe Messverfahren. Eine **vorgeschlagene Unterrichtsschwelle** verlangt gegenüber dem gerundeten Basisfehler von `2.8 dB` einen um mindestens **1.0 dB geringeren** absoluten Fehler: Ziel `≤ 1.8 dB` bezogen auf die aufgenommenen `−3.9 dB`. Mit gerundeten Werten entspricht das einem Kandidatenbereich von **−5.7 bis −2.1 dB**. Eine tatsächliche Annahmeentscheidung muss ungerundete WAV-Messwerte und eine dokumentierte Toleranz verwenden, statt am Zehntel-dB-Rand anhand des gerundeten JSON zu entscheiden. Diese vorab gewählte Schwelle ist eine Lehrregel, **kein** GA-Produktstandard und keine Vorhersage, dass `0.9976` besteht.

Sichere den Vergleich ab: kein Clipping oder Beinahe-Clipping (vorgeschlagene absolute Spitzenamplitude **unter 0.95**), E2-Grundton nahe dem Basiswert mit derselben Ein-Sekunden-Peaksuche, Prüfung des ersten Anschlags und der Verläufe des zweiten und vierten Teiltons. Ein besseres aggregiertes RMS kann einen geschädigten Transienten oder Spektralausklang verbergen. Wiederhole den Versuch auf anderen Saiten, Tönen und Velocities, bevor du verallgemeinerst. Prüfe pegelangepasste, verblindete Hörurteile: Numerische Übereinstimmung mit einer fremden Gitarre belegt keinen wahrgenommenen Realismus. Verfehlt der Kandidat `≤1.8 dB` oder eine Schutzprüfung, verwerfe **diesen Kandidaten für diesen Test** und berichte das Messergebnis. Das beweist nicht, dass keine Decay-Änderung helfen könnte.

### Übung 4 — Die vorgeschlagene Schwelle anwenden

Wie groß ist mit den gerundeten Basiswerten der höchste zulässige absolute Fehler für eine Verbesserung von 1.0 dB? Welcher Kandidatenbereich folgt um `−3.9 dB`? Würde ein Kandidat innerhalb des Bereichs mit einer Spitze von `0.98` alle Schutzprüfungen bestehen?

> **Antwort:** `2.8 − 1.0 = 1.8 dB`; aus `|candidate − (−3.9)| ≤ 1.8` folgt `−5.7 ≤ candidate ≤ −2.1 dB`. Eine Spitze von `0.98` verletzt die vorgeschlagene Grenze `<0.95`, auch wenn der Abklingwert besteht. Das ist Rechnung an einer vorgeschlagenen Schwelle, kein gemessenes Kandidatenergebnis.

### Übung 5 — Eine Widerlegung formulieren

Ein Agent behauptet, Basis-Decay `0.9976` verbessere die E2-Dämpfung von GA. Welche kontrollierten Mindestartefakte und welches Ergebnis würden diese Behauptung nach der Lehrregel widerlegen? Was bliebe selbst nach einem erfolgreichen E2-Einzeltest unbekannt?

> **Antwort:** Sichere exakte Engine-Revision und Build, Reihenfolge der Parameteraufrufe, native Basis- und Kandidaten-WAVs aus frischen Engines samt Hashes, anschlagsbezogene Messung sowie Spitzen-, Teilton- und Anschlagsprüfungen. Sinkt der ungerundete absolute Fehler nicht um mindestens 1.0 dB, oder scheitert eine Schutzprüfung, fällt dieser Kandidat durch. Auch nach Erfolg sind Browserausgabe, weitere Töne und Velocities, unterschiedliche Aufnahmebedingungen und Hörpräferenzen nicht verifiziert.

## 4. Verbesserung und Kalibrierung auseinanderhalten

Die Aufnahme ist eine **Kalibrierprobe**, kein genaues physikalisches Ziel für jede Gitarre. Der Datensatz nennt sie leeres E2, aber Raum, Instrument, Mikrofon und Spieler unterscheiden sich vom Render. Eine globale `decay`-Änderung kann viele Töne betreffen; die frequenzabhängige Formel macht Verallgemeinerungen vom E2 besonders riskant. Nähert ein Kandidat die Hüllkurve dieser Referenz an, sage nur, dass er **das festgelegte Maß spätes minus frühes RMS** des geprüften Renders annähert. Falls nicht, bewahre den Fehlversuch für eine spätere Hypothese zu Anschlagsrauschen, Hall, frequenzabhängiger Rückkopplung oder Fensterempfindlichkeit auf, ohne die Vergangenheit umzudeuten.

GAs vorhandener [Offline-Iterationsablauf](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) und spektraler Critic unterstützen wiederholte Versuche, geben aber kein automatisches Hörurteil. Ein später mit ComfyUI bearbeiteter Kandidat wäre **ein separater Offline-Arm**, kein Beleg für den Erfolg des Rust-Setters. Trenne Agentenvorschläge, Engine-Render, Referenzen, Hashes, Messungen, Review und Veröffentlichungsstand.

## Quellen und Grenzen

- [GAS-001-Provenienz](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md), [Messwerte](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json), [Messmethode](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) und [nativer Renderer](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py), jeweils bei Demerzel `5c4967454ddc740ed937c87719ca4d71a3522e4b`.
- [GA-Rust-Engine-Quellcode](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) und [Offline-Iterationsskript](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), jeweils bei GA `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Vor dieser Lektion wurde nur das gespeicherte GAS-001-Paar gemessen. Koeffizienten und Annahmeintervall sind berechnet. Eine unabhängige Prüfung des Inhalts und der Bedeutungsgleichheit der KI-Übersetzungsentwürfe ergab keine konkreten Befunde. Kandidatenrender `0.9976`, Erweiterung des nativen Testaufbaus, Browser-Capture, Mehrtonprüfung, Hörpanel, menschliche Fachprüfung, Lernendentest, sprachliche Prüfung und Veröffentlichung stehen aus.
