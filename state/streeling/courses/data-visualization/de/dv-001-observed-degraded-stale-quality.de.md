---
module_id: dv-001-observed-degraded-stale-quality
department: data-visualization
course: Messwerte, beeinträchtigte Läufe und veraltete Daten
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-04-001
version: "0.1.0"
---

# Messwerte, beeinträchtigte Läufe und veraltete Daten

> **Fachbereich Datenvisualisierung** | Niveau: Einstieg | Geschätzte Dauer: 35 Minuten | Status: Prüfung ausstehend

## Lernziele

Nach dieser Lektion kannst du:

- eine gemessene Bestehensquote von einem nicht verfügbaren Lauf und einem übernommenen historischen Wert unterscheiden;
- eine Zeitreihe zeichnen, ohne fehlende Messungen als Fehlschläge darzustellen oder Punkte über einen Ausfall hinweg stillschweigend zu verbinden;
- vor dem Vergleich zweier Messungen Nenner, Beobachtungsdatum und Umgebung prüfen;
- eine zugängliche Textbeschreibung und Tabelle als Ergänzung zum Diagramm anbieten.

## Die Frage aus dem Projekt

GA speichert die Qualitätssicherungsdaten seines Chatbots unter `state/quality/chatbot-qa/`. Wer das Dashboard liest, fragt: „Ist der Chatbot schlechter geworden?“ Die Darstellung darf nur so weit antworten, wie es die Aufzeichnungen erlauben. Diese Lektion verwendet vier **historische Datensätze** aus dem GA-Commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). Sie bilden einen Übungsdatensatz und beschreiben nicht den heutigen Zustand des Chatbots.

| Datum des Datensatzes | `total_prompts` | `pass_pct` | `degraded` | Was der Datensatz belegt |
|---|---:|---:|---|---|
| [2026-06-08](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-08.json) | 52 | `null` | `true` | Das Backend war nicht verfügbar; es wurde keine Bestehensquote gemeldet. |
| [2026-06-15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) | 52 | 75,00 | `false` | Für diesen Lauf wurde eine Bestehensquote gemeldet. |
| [2026-06-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-19.json) | 52 | 7,69 | `false` | Es wurde eine niedrige Quote gemeldet; der Datensatz allein erklärt die Ursache nicht. |
| [2026-07-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) | 52 | 98,08 | `false` | Ein späterer Lauf meldete eine höhere Quote. |

### Übung

Ordne jede Zeile als beobachtete Quote oder nicht verfügbaren Lauf ein. Welche Zeile darf bei 0% auf der Quotenachse stehen?

> **Antwort:** Für den 15. Juni, den 19. Juni und den 19. Juli liegen gemeldete Quoten vor. Der Lauf vom 8. Juni war nicht verfügbar. Keine Zeile meldet eine Quote von 0%; ein Nullpunkt für den 8. Juni wäre eine erfundene Messung.

## 1. Drei verschiedene Datenzustände

Eine **Beobachtung** ist ein Wert, den ein Lauf tatsächlich gemeldet hat. Ein **nicht verfügbarer Lauf** bedeutet, dass unter den dokumentierten Bedingungen keine verlässliche Messung möglich war. Ein **übernommener historischer Wert** ist eine frühere Beobachtung, die zur Einordnung erneut angezeigt wird; er ist keine neue Messung am Anzeigedatum.

Die Datei vom 8. Juni enthält `pass_pct: null`, `degraded: true` und `degraded_reason: "backend_unavailable"`. Sie enthält außerdem `last_known_good_pass_pct: 94.0`, ein früheres Datum und `last_known_good_source: "carryforward"`. Die 94% gehören zur früheren Beobachtung. Als Punkt am 8. Juni würden sie während des Ausfalls eine stabile Leistung vortäuschen. `null` als Nullwert würde dagegen einen Fehlschlag des Chatbots vortäuschen. Beide Darstellungen verändern die Aussage.

Halte im Darstellungsmodell zwei Felder getrennt: `quality_value` für die gemessene Quote und `run_status` für den Zustand „beobachtet“, „beeinträchtigt“ oder „unbekannt“. Bewahre das Quelldatum eines historischen Werts getrennt vom Anzeigedatum auf. Leite aus `total_prompts` keine Quote ab: Die Notiz vom 8. Juni beschreibt Backendfehler, keine bewerteten Chatbotantworten.

### Übung

Eine Dashboard-Kachel zeigt „94% Bestehensquote am 8. Juni“, weil die Datei `last_known_good_pass_pct: 94.0` enthält. Formuliere die Kachel in einem Satz neu.

> **Antwort:** „Chatbot-QA am 8. Juni nicht verfügbar: Backend ausgefallen; letzter bekannter guter Wert 94% vom 16. Mai.“ Das historische Datum muss sichtbar bleiben, und die Quote für den 8. Juni ist unbekannt.

## 2. Qualität und Verfügbarkeit getrennt darstellen

Verwende die Quotenachse nur für gemessene Werte. Lasse bei `pass_pct: null` eine Lücke, statt Punkte darüber hinweg zu verbinden. Eine zweite, an denselben Daten ausgerichtete Spur kann den Lauf vom 8. Juni mit Symbol **und Text** als beeinträchtigt markieren. So beantwortet die Darstellung zwei getrennte Fragen: Welcher Qualitätswert wurde gemessen, und war eine Messung verfügbar?

Für die vier Datensätze genügt eine Textskizze:

```text
Datum         Qualitätsspur          Verfügbarkeitsspur
2026-06-08    kein Punkt             BEEINTRÄCHTIGT: Backend nicht verfügbar
2026-06-15    75,00%                 beobachtet
2026-06-19     7,69%                 beobachtet; untersuchen
2026-07-19    98,08%                 beobachtet
```

Die Daten liegen auseinander; sie sind keine vier aufeinanderfolgenden Tagesmessungen. Eine Linie zwischen dem 19. Juni und dem 19. Juli könnte suggerieren, dass auch die nicht gezeigten Tage gemessen wurden und einem gleichmäßigen Verlauf folgten. Hat die vollständige Reihe Lücken, unterbrich die Linie dort. Verwende die tatsächlichen Daten statt gleich weit auseinanderliegender Kategorien, die den Zeitabstand verdecken. Der [historische GA-Qualitätsbericht aus dem fixierten Commit](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) kennzeichnet zudem veraltete Datenquellen; ein als „aktuellster Wert“ angezeigter Messwert braucht sein Beobachtungsdatum.

### Übung

Skizziere zwei Spuren für den 8. und 15. Juni, jeweils mit Datum und Textstatus. Soll der übernommene Wert von 94% durch eine Linie mit den 75% vom 15. Juni verbunden werden?

> **Antwort:** Am 8. Juni steht kein Punkt in der Qualitätsspur; die Verfügbarkeitsspur meldet „Backend nicht verfügbar“. Am 15. Juni stehen ein Punkt bei 75% und der Status „beobachtet“. Die 94% werden mit ihrem ursprünglichen Datum, dem 16. Mai, beschriftet. Sie sind weder ein Punkt vom 8. Juni noch der Anfang einer Linie zum 15. Juni.

## 3. Eine niedrige Zahl ist eine Frage, keine Diagnose

Der Datensatz vom 19. Juni meldet 7,69% und `degraded: false`. Das Diagramm soll den Wert zeigen. Aus dieser Datei allein lässt sich jedoch nicht schließen, ob GA-Code schlechter wurde, das Modell wechselte, der Fragenkorpus verändert wurde oder eine Abhängigkeit anders reagierte. `degraded: false` ist nur die Einstufung des Erzeugers für diesen Lauf und kein vollständiger Gesundheitsnachweis. Prüfe Konfiguration, Identität der Fragen, Backendprotokolle, Bewertungsregeln und benachbarte Läufe, bevor du eine Ursache benennst.

Alle drei beobachteten Zeilen nennen jeweils 52 Fragen. Das ist hilfreicher Kontext, beweist aber weder identische Fragen noch identische Bewertung. Ein Vergleich sollte neben der Anzahl auch die Revision des Fragenkorpus und des Bewertungsverfahrens festhalten. Fehlen diese Angaben, kennzeichne den Vergleich als vorläufig. Eine Prozentachse ohne Nenner und Quelle kann verbergen, wie empfindlich eine kleine Stichprobe ist.

### Übung

Beurteile die Aussage: „GA hat sich zwischen dem 19. Juni und dem 19. Juli von einer bestätigten Softwareregression erholt.“ Was ist beobachtet, und wofür fehlen noch Belege?

> **Antwort:** Die Dateien melden 7,69% am 19. Juni und 98,08% am 19. Juli. „Erholt“ und „Softwareregression“ unterstellen Ursache und Verlauf, die diese vier Datensätze nicht belegen. Vergleiche denselben Fragenkorpus, dasselbe Bewertungsverfahren und dieselbe Umgebung und untersuche die Fehlschläge.

## 4. Das Diagramm ohne Farbcodierung verständlich machen

Farbe kann helfen, doch ein Ausfallmarker braucht zusätzlich Text oder eine unterscheidbare Form. Die [W3C-Erläuterung zur Verwendung von Farbe](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) verlangt ein weiteres visuelles Merkmal, wenn Farbe Informationen vermittelt. Die [W3C-Erläuterung zu nichttextuellen Inhalten](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content) beschreibt eine Textalternative, die den Zweck eines Diagramms wiedergibt; eine Datentabelle kann die genauen Werte liefern.

Für diese Daten eignet sich etwa die Kurzbeschreibung: „Historische Chatbot-QA von GA: 8. Juni nicht verfügbar; gemeldete Bestehensquoten waren 75% am 15. Juni, 7,69% am 19. Juni und 98,08% am 19. Juli. Die Ursache des niedrigen Ergebnisses vom 19. Juni ist hier nicht geklärt.“ Stelle die Tabelle oben direkt neben das Diagramm. Menschen mit Screenreader müssen Daten, Werte und Zustände erreichen können, ohne Farben oder nur beim Überfahren sichtbare Hinweise deuten zu müssen.

### Übung

Am 8. Juni steht nur ein roter Punkt ohne Text. Was muss ergänzt werden?

> **Antwort:** Ergänze sichtbaren Text wie „Backend nicht verfügbar“ und eine programmatisch verfügbare Beschriftung. Für den 8. Juni darf keine Bestehensquote erscheinen. Biete eine Tabelle oder gleichwertige Beschreibung mit Datum und Status an.

## Wichtigste Erkenntnisse

- Fehlende Qualitätsdaten sind weder ein Nullwert noch ein Erfolgswert.
- Ein übernommener historischer Wert behält sein ursprüngliches Beobachtungsdatum.
- Ein Diagramm sollte Messverfügbarkeit und gemessene Qualität getrennt zeigen.
- Eine niedrige beobachtete Quote kann eine Untersuchung auslösen, ohne eine Ursache zu beweisen.
- Daten, Nenner, Quellrevisionen und zugänglicher Text gehören zur Aussage.

## Weiterführende Quellen und Projektbelege

- GA: [historische Chatbot-QA-Datensätze](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa) und [Qualitätstrendbericht](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). Der Bericht ist datiert und kein Live-Status.
- W3C, [Understanding Success Criterion 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color).
- W3C, [Understanding Success Criterion 1.1.1: Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content).

*Forschung: `data-visualization-2026-10-04-001`. Fachliche und sprachliche Prüfung stehen aus; dieser Entwurf ist kein verifizierter Kurs.*
