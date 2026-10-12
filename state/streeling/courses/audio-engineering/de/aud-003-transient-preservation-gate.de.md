---
module_id: aud-003-transient-preservation-gate
department: audio-engineering
course: "Den Anschlag einer Gitarrensaite bei der Offline-Spektralanalyse bewahren"
level: intermediate
prerequisites: [aud-002-level-matched-guitar-comparison, phy-002-time-frequency-guitar-transients]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-003
version: "0.1.0"
---

# Den Anschlag einer Gitarrensaite bei der Offline-Spektralanalyse bewahren

> **Fachbereich Audiotechnik** | Niveau: Mittelstufe | Geschätzte Dauer: 35 Minuten | Status: deutscher Entwurf; Prüfung und Veröffentlichung ausstehend

## Lernziele

Nach dieser Lektion können Sie:

- je nach Fragestellung zwischen einer FFT des gesamten Intervalls und einer STFT wählen;
- gültige Fenster- und Hop-Größen für das IX-Spektrogramm festlegen, sodass der Anschlag in mindestens einem Frame sichtbar bleibt;
- den Haar-Wavelet-Denoiser von IX von den frequenzgerichteten Wavelet-Analysen des GAS-001-Fixtures unterscheiden;
- eine Rauschminderung ablehnen, die einen Gitarrentransienten jenseits einer zuvor festgelegten Grenze verändert; und
- eine Offline-Auswertung festlegen, die andere mit denselben WAV-Dateien widerlegen könnten.

## Die Projektentscheidung

Das [GAS-001-Fixture der leeren tiefen E-Saite](../../../fixtures/guitar-acoustics/gas-001/README.md), festgehalten im Demerzel-Commit [`5c496745`](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), enthält eine lizenzierte Aufnahme des leeren E2 und ein Rendering der nativen GA-Engine. Beide sind vier Sekunden lange Mono-WAV-Dateien mit 44.100 Hz. Der erste aufgenommene Anschlag liegt ungefähr 1,1 Sekunden nach Dateibeginn; das Rendering beginnt bei null. Das Fixture dokumentiert in der Aufnahme einen weiteren Anschlag um 2,75 Sekunden. Das Paar dient der Lehre; es ist weder ein validierter Realismus-Benchmark noch eine Aufnahme des Browser-AudioWorklets.

[PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md) erläutert den Zeit-Frequenz-Kompromiss und deutet die gespeicherten FFT- und Morlet-artigen Wavelet-Messungen des Fixtures. [AUD-002](../en/aud-002-level-matched-guitar-comparison.md) kontrolliert vor dem Anhören die Ausrichtung der Anschläge und den Wiedergabepegel. Hier geht es um eine andere technische Entscheidung: **Sollte man die aufgenommene Referenz offline entrauschen, bevor man anhand ihres Anschlags ein GA-Rendering beurteilt?** Eine scheinbare Rauschminderung reicht nicht. Der Denoiser kann den zu bewahrenden Transienten auch abschwächen, verbreitern oder zeitlich verschieben.

Der Implementierungsfall ist an IX-Commit [`bd1336b7`](https://github.com/GuitarAlchemist/ix/tree/bd1336b7c4045e427dcdbe80b102790e45da5ce1) gebunden. IX bietet einen [FFT-Handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1297-L1315), einen [Spektrogramm-Handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189) und einen [Handler zur Haar-Wavelet-Entrauschung](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797). Sie nehmen numerische Sample-Arrays an, keine WAV-Pfade. Um sie auf das referenzierte Audiopaar anzuwenden, wären ein WAV-Decoder und ein wiederholbarer Offline-Versuchsaufbau nötig; diese Lektion hat den Versuch nicht durchgeführt.

## 1. Wählen Sie die Ansicht passend zur Aussage

Die IX-Funktion [`rfft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/fft.rs#L84-L115) transformiert ein endliches Array reeller Samples. Eine Länge, die keine Zweierpotenz ist, wird bis zur nächsten Zweierpotenz mit Nullen aufgefüllt. Trotz ihres Namens gibt die Funktion das vollständige FFT-Array zurück. Der Handler `ix_fft` gibt Beträge und Frequenzen in **Zyklen pro Sample** zurück und nimmt dabei eine Abtastrate von 1,0 an. Bei 44.100 Samples pro Sekunde multiplizieren Sie die normierte Bin-Frequenz **bis zur Nyquist-Grenze** mit 44.100, um sie in Hertz auszudrücken; die obere Hälfte spiegelt negative Frequenzen. Ein Betragsspektrum der ganzen Datei ist auch für ein veränderliches Signal gültig, kennzeichnet aber nicht, von welchem Anschlag ein Peak stammt. Die FFT eines ausgewählten Intervalls der ersten Note eignet sich für eine lokale Zusammenfassung der Harmonischen, mittelt aber weiterhin über dieses Intervall.

Die IX-Funktion [`stft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L30) wiederholt gefensterte FFTs an aufeinanderfolgenden Sample-Positionen. [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L32-L54) verwendet ein Hann-Fenster und behält einseitige Beträge. So lässt sich sehen, ob Energie des Anschlags in einem frühen Frame erscheint und wie sie sich verändert. Bei `db=true` wird `20 log10(max(magnitude, 1e-10))` berechnet; das ist keine kalibrierte dBFS-Messung. Vergleichen Sie diese rohen dB-Werte nicht unmittelbar mit den RMS-Werten in dBFS von GAS-001.

### Übung 1: eine Ausgabe wählen, die die Frage beantworten kann

Jemand berechnet `ix_fft` für die gesamten vier Sekunden der aufgenommenen WAV-Datei und ordnet einen hellen Peak dem *ersten* Anschlag statt dem späteren zu. Welcher Teil des Ergebnisses ist brauchbar, und was muss vor der Zuordnung zu einem Ereignis berechnet werden?

> **Antwort:** Die FFT der ganzen Datei kann Energie in der Nähe dieser Frequenz zeigen, nachdem Zyklen pro Sample in Hertz umgerechnet wurden. Ihre Beträge tragen keine Zeitmarke und ordnen den Peak daher nicht dem ersten Anschlag zu. Dekodieren Sie die WAV-Datei, markieren Sie den ungefähren ersten Anschlag, berechnen Sie ein eigens festgelegtes Intervall der ersten Note und betrachten Sie eine an den Anschlägen ausgerichtete STFT, wenn deren Zeitlage wichtig ist. Halten Sie die unveränderte Datei und die Analyseintervalle fest.

## 2. Passen Sie die IX-STFT an die Anschlagsfrage an

Der **IX-Agent-Handler** verlangt ein `window_size`, das eine Zweierpotenz, mindestens zwei und nicht größer als das Signal ist. Andernfalls würde die darunterliegende FFT den Frame mit Nullen auffüllen, sodass die angegebene Bin-Zahl und Frequenzzuordnung des Handlers falsch wären. Standardmäßig ist `hop_size` ein halbes Fenster; einen angegebenen Hop von null setzt der Handler auf eins. Er meldet `n_frames` und `n_bins`. Die Kernfunktion `stft` enthält diese Eingabeprüfungen nicht: Ein Offline-Versuchsaufbau, der sie direkt aufruft, muss seine Argumente selbst prüfen. Die Funktion verarbeitet nur vollständige Frames und verlängert einen kurzen Rest nicht stillschweigend.

Für eine **vorgeschlagene** Ansicht des ersten Anschlags bei 44,1 kHz wählen Sie 2.048 Samples pro Fenster und einen Hop von 512 Samples. Das Fenster umfasst ungefähr **46,44 ms**, der Hop **11,61 ms** und das FFT-Raster `44,100 / 2,048 ≈ 21.53 Hz` pro Bin; der einseitige Betrag hat **1.025 Bins**. Dieses Raster ist zu grob, um mit einem einzelnen Frame einen Tonhöhenunterschied von einem Hertz zu entscheiden. Ein größeres Fenster mit 8.192 Samples umfasst ungefähr 185,76 ms und hat 5,38 Hz Bin-Abstand, mischt aber mehr vom Anschlag und Ausklang. Ein kleinerer Hop erzeugt mehr überlappende Frames; er verbessert nicht die Frequenzunterscheidung eines einzelnen Frames. Dies sind Berechnungen aus Einstellungen, **keine** an den WAV-Dateien gemessenen IX-Ausgaben.

### Übung 2: eine gültige IX-Anfrage angeben

Berechnen Sie bei 44.100 Hz Fensterdauer, Hop-Intervall und nominellen Bin-Abstand für `window_size=2048`, `hop_size=512`. Wie viele Bins sollte der IX-Spektrogramm-Handler melden? Warum würde dieser Handler `window_size=2205`, genau 50 ms, ablehnen?

> **Antwort:** Die Fensterdauer beträgt `2048/44100 ≈ 46.44 ms`, das Hop-Intervall `512/44100 ≈ 11.61 ms` und der Abstand `44100/2048 ≈ 21.53 Hz`. Der Handler meldet `2048/2 + 1 = 1025` Bins. Er lehnt 2.205 ab, weil es keine Zweierpotenz ist. Ein direkter Aufruf der Kernfunktion könnte mit Nullen auffüllen, aber die Bins so zu deuten, als sei die FFT 2.205 Samples lang, wäre falsch.

Ein Hann-Fenster fällt an den Endpunkten auf null ab. Das dämpft Diskontinuitäten am Rand, doch ein Transient genau am Endpunkt kann in diesem Frame verschwinden. Durch Überlappung liegt dasselbe Sample an einer anderen Position in einem weiteren Frame. Das ist ein Problem der **Platzierung der Analyse**, kein Zugewinn an Information. Die [IX-Fensterfunktion](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/window.rs#L10-L15) und die [Frame-Schleife](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L14-L29) machen diesen Randeffekt ohne Gitarrenaufnahme prüfbar.

### Übung 3: den Impuls am Fensterrand sichtbar halten

Nehmen Sie ein synthetisches Array mit 64 Samples, die alle null sind außer dem Wert 1 an Index 16. IX verwendet ein Hann-Fenster mit 16 Samples. Welcher vollständige Frame enthält bei Hop 16 den Impuls, und was geschieht mit ihm? Was ändert sich bei Hop 8?

> **Antwort:** Bei Hop 16 beginnen die Frames an 0, 16, 32 und 48. Nur der bei 16 beginnende Frame enthält Index 16; der Impuls liegt dort am Fenster-Offset 0 mit Hann-Gewicht null. Daher können sämtliche ausgegebenen Spektren diesen einzelnen Impuls verfehlen. Bei Hop 8 enthält ihn auch der bei 8 beginnende Frame, dort an Offset 8 mit einem Hann-Gewicht von etwa 0,989; dieser Frame zeigt Energie. Dies ist eine synthetische Berechnung aus dem Quellcode, keine IX-Messung an einer WAV-Datei. Sie zeigt, warum der vorgeschlagene Hop von 512 Samples an den Grenzen echter Anschläge überprüft werden sollte.

## 3. Ein Haar-Denoiser kann den Beleg verändern

Die IX-Funktion [`haar_forward`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L18) bildet paarweise Mittelwerte und Differenzen. [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L60-L82) unterzieht die Detailkoeffizienten einem Soft-Thresholding und rekonstruiert das Signal. Das ist ein diskreter Haar-Verarbeitungsschritt, **nicht** die frequenzzentrierte komplexe Morlet-artige Wavelet-Analyse, die in GAS-001 gespeichert ist. Beide Verfahren liefern andere Ergebnisse und beantworten andere Fragen. Ein Haar-Detailkoeffizient kann eine schnelle Änderung markieren; ihn zu schwellen kann jedoch zusammen mit Rauschen einen Teil eines echten Anschlags entfernen.

Der IX-Handler verlangt `levels >= 1`, einen endlichen, nichtnegativen Schwellenwert und eine durch `2^levels` teilbare Eingabelänge. Andernfalls weist er die Anfrage zurück, weil die Haar-Kerntransformation bei ungerader Restlänge Samples am Ende verlieren kann. Der eingecheckte [Rauschtest](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1387-L1411) verwendet eine glatte Rampe mit hinzugefügtem alternierendem Rauschen und prüft einen geringeren mittleren quadratischen Fehler. Er prüft nicht, ob ein isolierter Gitarrenanschlag erhalten bleibt. Gesonderte [Eingabeprüfungstests](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1525-L1543) decken eine ungültige Spektrogrammgröße und eine nicht teilbare Wavelet-Eingabelänge ab.

### Übung 4: die Änderung des Transienten vorhersagen

Wenden Sie auf das synthetische Signal aus acht Samples `[0, 1, 0, 0, 0, 0, 0, 0]` die einstufigen Haar-Gleichungen von IX mit Soft-Threshold 1 an. Wie lauten die ersten beiden rekonstruierten Samples? Stützt dies die Behauptung, dass Wavelet-Entrauschung einen Anschlags-Peak immer erhält?

> **Antwort:** Das erste Paar hat die Approximation `1/sqrt(2)` und das Detail `-1/sqrt(2)`. Dessen Betrag liegt unter der Schwelle 1, sodass Soft-Thresholding das Detail auf null setzt. Die inverse Transformation ergibt `[0.5, 0.5]` für das erste Paar; die anderen Paare bleiben null. Der isolierte Peak sinkt von 1 auf 0,5 und verteilt sich um ein Sample nach vorn. Die Rechnung widerlegt eine uneingeschränkte Erhaltungsbehauptung; sie sagt nicht voraus, welcher Schwellenwert für eine aufgenommene Gitarren-WAV angemessen wäre.

## 4. Eine Offline-Erhaltungsgrenze vorher festlegen

Die folgende Vorgehensweise ist ein **Auswertungsvorschlag**, kein ausgeführter Versuch und kein GA-Akzeptanzstandard. Bewahren Sie beide Fixture-WAVs und ihre vollständigen Hashes auf. Dekodieren Sie jede Datei in normierte Mono-`f64`-Samples, ohne die Originale zu überschreiben. Notieren Sie Decoder, Abtastrate, Sample-Zahl und jedes Resampling; lehnen Sie eine unbemerkte Änderung der Abtastrate ab. Verwenden Sie die ungefähren Anschlagsmarken des Fixtures (Aufnahme 1,1 s, Rendering 0,0 s) und untersuchen Sie Ausschnitte des ersten Anschlags getrennt vom späteren Anschlag in der Aufnahme. Behalten Sie einen unbearbeiteten Arm und eine bearbeitete Kopie an denselben Sample-Positionen mit demselben Gain. Führen Sie die IX-STFT-Ansicht für beide Arme mit den deklarierten Einstellungen 2.048/512 aus; beschriften Sie Frames mit **Startsample und Fensterspanne**, nicht nur mit dem optischen Mittelpunkt einer Spalte. Halten Sie fest, ob die Folgerung zum Anschlag am Rand einem anderen Hop oder einer kleinen Verschiebung der Anschlagsmarke standhält.

Legen Sie vor jedem Haar-Lauf `levels` und Schwellenwert fest, prüfen Sie die exakte Teilbarkeit der Eingabelänge durch `2^levels` und dokumentieren Sie bei Bedarf Auffüll- und Schnittregeln. Zum Beispiel ist ein einsekündiger Ausschnitt mit 44.100 Samples bei drei Stufen **nicht** durch acht teilbar: Der Rest beträgt vier. Vier Nullen bis 44.104 anzuhängen ist eine mögliche dokumentierte Wahl; sie erzeugt einen Rand, der benachbarte Koeffizienten beeinflussen kann. Sie können stattdessen die Ausschnittgrenze ändern oder weniger Stufen verwenden. Rufen Sie die Kernfunktion nicht direkt mit ungerader Eingabelänge auf und nehmen Sie dabei eine ausgerichtete Ausgabe an.

Messen Sie für die aufgenommene Referenz sowohl an der unbearbeiteten als auch an der bearbeiteten Kopie ein festgelegtes Rauschintervall vor dem Anschlag und ein festes Intervall des ersten Anschlags. Eine **didaktische Grenze**, vor Sichtung des Ergebnisses gewählt, könnte mindestens **3 dB** weniger RMS vor dem Anschlag verlangen, während der absolute Peak des ersten Anschlags innerhalb von **10%** des unbearbeiteten Werts und seine Zeitlage innerhalb von **1 ms** bleiben. Verlangen Sie keine Übersteuerung und nach einem dokumentierten Schnitt eine unveränderte Sample-Zahl. Wiederholen Sie die Prüfung mit um ±5 ms verschobenen Anschlagsmarken und melden Sie jeden Schwellenwertkandidaten, auch gescheiterte. Das GA-Rendering beginnt bei Dateizeit null; es hat daher kein entsprechendes Rauschintervall vor dem Anschlag. Wenden Sie gerade diese Rauschgrenze nicht darauf an. Bewahren Sie die unbearbeitete Aufnahme als primäre Vergleichsreferenz auf. Das Bestehen dieser Wellenform-Indikatoren würde einen getrennt dokumentierten Hörvergleich bei angeglichenem Pegel erlauben, **nicht** beweisen, dass die bearbeitete Datei wahrnehmbar unverändert ist oder GA realistisch klingt.

### Eine erste Prüfung der aufgenommenen WAV-Datei

Eine [begrenzte IX-Haar-Prüfung](../../../reviews/aud-003-ix-probe-2026-10-11.md) wurde auf 8.192 Samples der GAS-001-Aufnahme ab Sample 46.966 ausgeführt. Das Intervall von 35 ms vor dem im Fixture ungefähr bei 1,1 s vermerkten Anschlag ist nur ein **vorläufiger** Rauschindikator; das Anschlagsfenster reicht von 1,1 bis 1,25 s. Bei drei Haar-Stufen senkten die Schwellen 0.002, 0.004 und 0.008 den RMS-Wert in diesem vorläufigen Intervall um lediglich 0.0942, 0.0968 und 0.0968 dB. Die Anschlags-Peaks behielten 96.97%, 94.83% und 90.54% des unbearbeiteten Peaks; die gemessene Verschiebung des Peak-Samples betrug jeweils null. Jedes Ergebnis behielt die ursprüngliche Sample-Zahl bei und zeigte keine Übersteuerung. Keines erreichte das beispielhafte Ziel von 3 dB Rauschminderung; daher besteht keines diese Näherungsgrenze. Dieser einzelne kurze Ausschnitt validiert weder die Anschlagssegmentierung noch die Grenze für die ganze Datei, die Übereinstimmung des IX-Binärprogramms mit dem zitierten Quellcode-Commit oder die wahrnehmbare Gleichwertigkeit. Bewahren Sie die unbearbeitete Aufnahme als Referenz auf.

### Übung 5: Grenze anwenden und ihre Aussage beschränken

Jemand schlägt einen dreistufigen Haar-Lauf für einen aufgenommenen Ausschnitt mit 44.100 Samples ohne Auffüllung vor. Außerdem liegt ein *hypothetischer* Kandidat mit 4 dB weniger RMS vor dem Anschlag, einem Anschlags-Peak von 0,82 mal dem unbearbeiteten Peak und einer Verschiebung der Peak-Zeit um 0,2 ms vor. Was muss sich ändern, damit der IX-Handler den Ausschnitt akzeptiert? Besteht der Kandidat die didaktische Grenze?

> **Antwort:** `44,100 mod 8 = 4`; deshalb lehnt der Handler drei Stufen bei dieser Länge ab. Deklarieren Sie vier angehängte Samples bis 44.104 samt Schnittregel, wählen Sie einen anderen Ausschnitt oder reduzieren Sie die Stufenzahl. Der hypothetische Kandidat fällt durch, obwohl das Rauschen um mehr als 3 dB sinkt und die Zeitverschiebung innerhalb 1 ms liegt: `1 - 0.82 = 0.18`, also 18% Peak-Verlust, überschreitet die festgelegte Grenze von 10%. Diese Ablehnung betrifft den Erhalt des Transienten nach diesem Näherungskriterium; sie ist weder ein Messergebnis an einer der Fixture-WAVs noch ein Hörurteil.

## Evidenz und Grenzen

- Projektaudio und Provenienz stammen aus dem [GAS-001-Fixture bei Demerzel `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). Die Aufnahme und das native GA-Rendering sind getrennte Quellen mit unterschiedlichen Aufnahme- und Produktionsketten. Die gespeicherten FFT- und Morlet-Ergebnisse sind Beobachtungen dieses Fixtures, keine IX-Ausgaben.
- STFT-, FFT- und Haar-Gleichungen, Handler-Prüfungen und Tests oben stammen aus dem IX-Quellcode bei `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Die 2.048/512-Größen, das Hann-Randbeispiel, das Haar-Ergebnis mit acht Samples und die Teilbarkeitsrechnung sind **abgeleitete Beispiele**. Eine spätere lokale IX-MCP-Prüfung maß einen Sample-Ausschnitt der aufgenommenen WAV-Datei; weder ein IX-Spektrogramm noch eine bearbeitete WAV-Datei oder eine Auswertung der gesamten Aufnahme wurden erstellt. Für das laufende MCP-Binärprogramm wurde die Übereinstimmung mit dem zitierten Quellcode-Commit nicht unabhängig belegt.
- Ein Analysebetrag ist kein kalibriertes Maß für Lautheit oder Realismus. Die Anschlagsmarken sind ungefähr; Spektralfenster, Auffüllung, Schwellen, Decoder und Eingangsgain können ein Ergebnis ändern. Ein synthetischer Impuls macht eine mögliche Fehlerart sichtbar, sagt aber nicht das Verhalten jedes Anschlags voraus.
- Fachliche Prüfung, Lernversuche, muttersprachliche Prüfung, Learn-Synchronisierung und -Build sowie öffentlicher Abruf stehen noch aus. Dieser deutsche Text ist ein Übersetzungsentwurf, kein veröffentlichtes Kursmaterial.
