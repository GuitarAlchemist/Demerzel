---
module_id: cog-003-calibrating-fretboard-confidence
department: cognitive-science
course: "Sicherheit bei der Notenerkennung auf dem Griffbrett kalibrieren"
level: intermediate
prerequisites: [cog-002-feedback-integrity-fretboard-recall]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-12-003
version: "0.1.0"
---

# Sicherheit bei der Notenerkennung auf dem Griffbrett kalibrieren

> **Fachbereich Kognitionswissenschaft** | Mittelstufe | 40 Minuten | Deutscher Entwurf; Prüfung und Veröffentlichung ausstehend

## Lernziele

Du wandelst „Ich bin sicher“ in eine **vor** der Rückmeldung aufgezeichnete Wahrscheinlichkeit um, berechnest einen binären Brier-Wert anhand eines geprüften GA-Antwortschlüssels, trennst sechs erfundene Beispiele von Messungen an Lernenden und entwirfst einen Test, der eine Kalibrierungshypothese widerlegen könnte. [COG-002 (Englisch)](../en/cog-002-feedback-integrity-fretboard-recall.md) prüft den angezeigten Schlüssel. Hier fragen wir: **Entspricht die angegebene Sicherheit der Häufigkeit richtiger Notenantworten?**

## Die Projektentscheidung

Stell dir eine GA-Aufgabe „Nenne diese Note“ auf dem SVG-Griffbrett vor. Zwei Gitarristen erkennen jeweils vier von sechs Positionen. Der eine ist sich bei seinen zwei Fehlern unsicher, der andere sehr sicher. Die reine Trefferquote behandelt beide gleich, aber möglicherweise brauchen sie unterschiedliche Rückmeldungen. Dafür brauchen wir ein klar definiertes Ereignis, einen verlässlichen Schlüssel und einen Test mit echten Lernenden.

Bei GA-Commit [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924) enthält die [Demoseite](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) sechs Positionen. Die [SVG-Komponente](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) verwendet `string: 0` für die hohe E-Saite, Bund 0 für die leere Saite und standardmäßig `E, B, G, D, A, E` von hoch nach tief. Die Demoseite überschreibt diese Stimmung nicht. An der sechsten Position, Saite 5 und Bund 3, steht **C**, obwohl drei Halbtöne über dem tiefen E **G** ergeben. Das ist ein Widerspruch im Quelltext, keine Beobachtung an Nutzern. Die korrigierte Folge lautet `E, C, G, E, C, G`.

Die Seite nennt sich Test einer älteren SVG-Komponente. Ihr [Klick-Handler](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) übermittelt nur Saite und Bund. Diese Quellen zeigen weder eine Sicherheitseingabe noch bewertete Lernsitzungen, ein Kalibrierungs-Dashboard oder einen bereitgestellten Kurs. **Alle folgenden Lernendenantworten sind erfundene Übungsdaten.**

## 1. Definiere die Vorhersage vor der Antwort

Für jeden Versuch wählt die lernende Person eine Note `a_i` für Saite und Bund. Danach gibt sie `p_i` zwischen 0 und 1 an: „Wie wahrscheinlich ist es, dass **meine gewählte Note** mit dem unabhängig geprüften Schlüssel übereinstimmt?“ Gefragt ist die Richtigkeit dieser Antwort, nicht die Wahrscheinlichkeit, dass die Gitarre klingt oder dass das Demo-Label stimmt. Zeichne `a_i` und `p_i` vor dem Anzeigen einer Note auf. Anschließend gilt `y_i=1` bei Übereinstimmung, sonst `y_i=0`.

Bewahre für den Schlüssel Saitenreihenfolge, Stimmung, Bund und Quellrevision auf. Die tiefe E-Saite hat Index 5; E ist Tonklasse 4. Am dritten Bund gilt `(4+3) mod 12=7`, also G. Das angezeigte C kann ohne die in COG-002 erläuterte Korrektur nicht als Lösung dienen.

Die Oberfläche bräuchte **neue** Eingaben für Note und Sicherheit. Der vorhandene Klick liefert eine Koordinate, keine Notenvorhersage. Ein vorgeschlagener Versuchseintrag ist `{source_sha, tuning, string, fret, chosen_note, confidence_before_feedback, verified_note, answer_time, feedback_time}`: Studienentwurf, **keine** bestehende GA-API. Vor `p_i` muss die Lösung verborgen werden, denn die Marker der Demo tragen sichtbare Beschriftungen.

### Übung 1 — Bestimme das Ereignis

Jemand wählt C auf Saite 5, Bund 3 mit `p=0.9`. Welche Note ist richtig, welchen Wert hat `y`, und speichert der jetzige Klick `p`?

> **Antwort:** Saite 5 ist das tiefe E. `(4+3) mod 12=7` ergibt G; für C gilt `y=0`. Der Klick sendet nur `{string, fret}`, weder die gewählte Note noch Sicherheit. Die Angabe `p=0.9` ist hypothetisch.

## 2. Werte sechs ausdrücklich erfundene Versuche aus

Der **binäre Brier-Wert** ist `BS=(1/n) Σ_i (p_i-y_i)^2`. Er liegt zwischen 0 und 1; **niedriger ist besser**. Anders als die reine Trefferzahl unterscheidet er einen Fehler mit Sicherheit 0.9 von einem mit 0.6. Die Ereignisdefinition muss für alle Aufgaben gleich bleiben. Die sechs Antworten und Wahrscheinlichkeiten sind **erfunden**; nur Koordinaten, Stimmung und korrigierter Schlüssel stammen aus GA.

| Versuch | Saite, Bund | Geprüfte Note | Erfundenes Urteil | `p_i` | `y_i` | `(p_i-y_i)^2` |
|---:|---|---|---|---:|---:|---:|
| 1 | 0, 0 | E | E | 0.9 | 1 | 0.01 |
| 2 | 1, 1 | C | C | 0.8 | 1 | 0.04 |
| 3 | 2, 0 | G | A | 0.7 | 0 | 0.49 |
| 4 | 3, 2 | E | E | 0.6 | 1 | 0.16 |
| 5 | 4, 3 | C | C | 0.9 | 1 | 0.01 |
| 6 | 5, 3 | G | C | 0.9 | 0 | 0.81 |

Die erfundene Person löst `4/6≈0.6667` richtig. Die quadratischen Verluste ergeben `0.01+0.04+0.49+0.16+0.01+0.81=1.52`; folglich `BS=1.52/6≈0.2533`. Das schätzt **keine** Fähigkeit einer realen Person. Würde das falsche Demo-C in Versuch 6 als Schlüssel verwendet, sänke sein Verlust von 0.81 auf 0.01 und der scheinbare Mittelwert auf `(1.52-0.81+0.01)/6=0.12`. Eine gute Bewertungsregel repariert keinen falschen Antwortschlüssel.

### Übung 2 — Berechne den Wert

Berechne Trefferquote, Summe der Verluste und mittleren Brier-Wert. Welcher falsche Versuch trägt mehr Verlust bei?

> **Antwort:** Vier von sechs sind richtig: `4/6≈0.6667`. Die Summe beträgt `1.52`, der Mittelwert `1.52/6≈0.2533`. Versuch 6 trägt `0.81` bei, mehr als Versuch 3 mit `0.49`, weil die falsche Antwort mit Sicherheit 0.9 statt 0.7 gegeben wurde.

### Übung 3 — Untersuche eine Sicherheitsgruppe

Welcher Anteil der Versuche mit `p_i=0.9` ist richtig, und wie weit liegt er unter 0.9? Reichen diese drei Versuche für eine stabile individuelle Kalibrierung?

> **Antwort:** Versuche 1, 5 und 6 haben 0.9; zwei sind richtig, also `2/3≈0.6667`. Der Abstand beträgt `0.9-2/3≈0.2333`. Drei erfundene, zusammenhängende Versuche reichen nicht für eine stabile Kalibrierungskurve.

### Übung 4 — Erkenne einen verfälschten Schlüssel

Wie änderten sich Ergebnis, Verlust und Mittelwert von Versuch 6, wenn gegen das angezeigte C statt gegen das geprüfte G gewertet würde? Wäre ein niedrigerer Wert ein Lernfortschritt?

> **Antwort:** Die Wahl C würde als `y_6=1` gewertet. Der Verlust sänke von `(0.9-0)^2=0.81` auf `(0.9-1)^2=0.01`. Summe und Mittelwert wären `0.72` und `0.72/6=0.12`. Die Vorhersage ist unverändert; der scheinbare Fortschritt entsteht durch den falschen Schlüssel.

## 3. Warum ist der quadratische Fehler nützlich?

Sei `q` die tatsächliche Wahrscheinlichkeit, dass eine gewählte Antwort in einer bestimmten Klasse künftiger Aufgaben stimmt, und `p` die gemeldete Wahrscheinlichkeit. Der erwartete Brier-Verlust lautet `q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q)`. Der zweite Summand hängt nicht von `p` ab; der eindeutige Mindestwert entsteht bei `p=q`. Die Regel belohnt ehrliche Wahrscheinlichkeiten **im Erwartungswert**, garantiert aber kein besseres Ergebnis in jeder Sechsergruppe. Sie zeigt auch nicht, ob ein Fehler von Saitenverwechslung, Gedächtnis oder irreführendem Feedback herrührt.

Im hypothetischen Beispiel `q=0.7` ergibt `p=0.7` den erwarteten Verlust `0.7(0.3)^2+0.3(0.7)^2=0.21`. Bei `p=0.9` sind es `0.7(0.1)^2+0.3(0.9)^2=0.25`; der Mehrverlust 0.04 entspricht `(0.9-0.7)^2`. Die sechs erfundenen Versuche belegen **nicht** `q=0.7` für echte Gitarristen.

Ein niedrigerer Brier-Wert allein bedeutet nicht mehr musikalisches Wissen. Wer überall näher an 0.5 rückt, kann die Strafe für selbstsichere Fehler senken, ohne mehr Noten zu erkennen. Gib deshalb auch Trefferquote und Ergebnisse nach Saite/Bund an; behalte die ursprünglichen Wahrscheinlichkeiten **vor** dem Feedback. Eine nachträgliche Änderung von `p_i` macht die Bewertung der ursprünglichen Prognose ungültig.

### Übung 5 — Prüfe die Richtung der Regel

Vergleiche bei hypothetischem `q=0.7` die erwarteten Verluste für `p=0.7` und `p=0.9`. Welcher ist geringer, und um wie viel?

> **Antwort:** Für `p=0.7` gilt `0.7(1-0.7)^2+0.3(0.7)^2=0.21`; für `p=0.9` gilt `0.7(1-0.9)^2+0.3(0.9)^2=0.25`. Der erste liegt um 0.04 niedriger. Die sechs Übungsdaten haben `q` nicht gemessen.

## 4. Entwirf einen Test, der scheitern kann

Prüfbare Hypothese: **Explizites Feedback zur Kalibrierung der Sicherheit nach jeder geprüften Notenantwort senkt den Brier-Wert am Folgetag für zurückgehaltene Positionen, ohne die Notentrefferquote zu verschlechtern**, verglichen mit der alleinigen Anzeige der korrekten Note. Beide Gruppen müssen Note und Sicherheit vor dem Feedback angeben. Die Kalibrierungsgruppe könnte ihre Sicherheit, Richtigkeit und einen laufenden Wert sehen; die Vergleichsgruppe dieselbe geprüfte Note und Richtigkeit ohne Sicherheitsübersicht. Dies ist ein Vorschlag, keine vorhandene GA-Funktion.

Korrigiere zuerst das falsche Label oder nutze einen separat geprüften Schlüssel. Bereite zwei Aufgabenansichten ohne Notenbeschriftung bei gleicher Stimmung vor und stelle sicher, dass die Lösung vor der Prognose unsichtbar bleibt. Gewinne echte Lernende, erfasse Einwilligung und Griffbrettvorkenntnisse und ordne die Bedingungen vor dem Üben zu. Gleiche Aufgabensätze zwischen Bedingungen aus und halte Positionen für den Folgetag zurück. Protokolliere Quellrevision, Aufgabe, Antwort, Sicherheit, Antwortzeit, angezeigtes Feedback und genaue Verzögerung. Eine Koordinate im Bild zu erkennen beweist nicht, dass man die Note spielen oder hören kann.

Lege vorab als Hauptgröße den mittleren Brier-Wert am Folgetag für die zurückgehaltenen Positionen fest, mit Notentrefferquote als Schutzbedingung. Die Hypothese **wird nicht gestützt**, wenn die Kalibrierungsgruppe diesen Wert gegenüber der Vergleichsgruppe nicht senkt oder eine scheinbare Verbesserung mit geringerer Trefferquote nach der zuvor festgelegten Schutzbedingung einhergeht. Berichte Unsicherheit sowie Zahl der Lernenden und Aufgaben. Ein Pilot kann Bedienfehler oder Deckeneffekte zeigen; dann braucht es einen überarbeiteten Test statt nachträglich behaupteten Erfolgs. **Keine** solche Lerngruppe, Zuteilung, UI-Variante oder Messung am Folgetag wurde für diesen Kurs durchgeführt.

### Übung 6 — Nenne eine Widerlegung

Ein Agent behauptet: „Der erfundene Brier-Wert `0.2533` beweist, dass unser Sicherheitsfeedback das Erinnern verbessert.“ Nenne zwei Gegenargumente und ein Studienergebnis, das die Hypothese scheitern ließe.

> **Antwort:** Alle sechs Wahrscheinlichkeiten und Antworten wurden erfunden; die GA-Seite hat weder diese Feedback-Intervention noch Folgetagsmessungen. Die Hypothese scheitert, wenn die Kalibrierungsgruppe am Folgetag für zurückgehaltene Positionen keinen niedrigeren Brier-Wert erzielt oder eine niedrigere Zahl mit schlechterer Trefferquote gemäß der Schutzbedingung verbunden ist. Nötig sind ein korrigierter Schlüssel und vor dem Feedback festgehaltene Wahrscheinlichkeiten.

## Evidenzgrenze

Die fixierten GA-Quellen belegen sechs Demo-Koordinaten, Saitenreihenfolge, sichtbare Labels und Klickdaten. Korrigierter Schlüssel und Brier-Rechnungen sind überprüfbar. Die sechs Antworten/Wahrscheinlichkeiten, `q=0.7`, UI-Varianten und Studie sind Lehrkonstruktionen. Es gibt hier keine gemessene Sicherheit echter Lernender, keine nachgewiesene Kalibrierungsänderung, keinen Interventionsnutzen, keine Browserausführung, keine fachliche oder sprachliche Prüfung, keinen Learn-Build und keinen öffentlichen Abruf. Dafür sind eigene Artefakte und Prüfende nötig, bevor dieser Entwurf als geprüft oder veröffentlicht gelten kann.
