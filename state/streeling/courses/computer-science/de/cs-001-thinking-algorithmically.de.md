---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: "Grundlagen der Informatik"
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Algorithmisches Denken

> **Fachbereich Informatik** | Stufe: Nigredo (Einführung) | Dauer: 25 Minuten

## Lernziele

Nach dieser Lektion werden Sie in der Lage sein:
- Zu definieren, was ein Algorithmus ist, und Algorithmen im Alltag zu erkennen
- Vier zentrale Problemlösungstechniken anzuwenden: Zerlegung, Mustererkennung, Abstraktion und Teile-und-Herrsche
- Gierige und erschöpfende Ansätze voneinander zu unterscheiden
- Ein Gefühl für die O-Notation zu entwickeln und zu verstehen, warum Effizienz wichtig ist

---

## 1. Was ist ein Algorithmus?

Ein **Algorithmus** ist eine endliche Folge wohldefinierter Schritte, die eine Eingabe entgegennimmt und eine Ausgabe erzeugt. Das ist alles. Kein Computer erforderlich.

Sie folgen täglich Algorithmen:
- Ein Kochrezept ist ein Algorithmus (Eingabe: Zutaten, Ausgabe: ein Gericht)
- Eine Wegbeschreibung ist ein Algorithmus (Eingabe: aktueller Standort, Ausgabe: Ziel)
- Das Herausgeben von Wechselgeld an der Kasse ist ein Algorithmus (Eingabe: geschuldeter Betrag, Ausgabe: möglichst wenige Münzen)

Was einen Algorithmus von vagen Anweisungen unterscheidet, ist **Präzision**. „Kochen, bis es fertig ist" ist kein Algorithmus — das ist mehrdeutig. „Bei 180°C für 25 Minuten erhitzen, dann Kerntemperatur prüfen; falls unter 74°C, in 5-Minuten-Schritten fortfahren" ist ein Algorithmus. Jeder Schritt ist eindeutig und der Prozess terminiert.

Drei Eigenschaften eines gültigen Algorithmus:
1. **Endlichkeit** — er muss irgendwann anhalten
2. **Bestimmtheit** — jeder Schritt muss präzise definiert sein
3. **Ausführbarkeit** — jeder Schritt muss tatsächlich durchführbar sein

### Übung

Schreiben Sie einen Algorithmus (in einfachem Deutsch, nummerierte Schritte) für das Nachschlagen eines Wortes in einem gedruckten Wörterbuch. Seien Sie präzise genug, dass jemand, der noch nie ein Wörterbuch benutzt hat, Ihren Schritten folgen könnte. Vergleichen Sie Ihren Ansatz mit der Methode aus Abschnitt 5 (Teile und Herrsche) — sind sie gleich?

---

## 2. Zerlegung — Probleme aufbrechen

Die mächtigste Fähigkeit des algorithmischen Denkens ist die **Zerlegung** (Dekomposition): ein komplexes Problem in kleinere, handhabbare Teilprobleme aufteilen.

**Beispiel:** Sie möchten ein Konzert organisieren.

Als einzelne Aufgabe ist das überwältigend. Aber zerlegen Sie es:
1. Einen Veranstaltungsort finden
2. Künstler buchen
3. Einen Termin festlegen
4. Karten verkaufen
5. Tontechnik organisieren
6. Die Veranstaltung bewerben

Jedes Teilproblem ist noch komplex, aber nun können Sie sie einzeln angehen. Und manche Teilprobleme lassen sich weiter zerlegen: „Karten verkaufen" wird zu: Plattform wählen, Preise festlegen, Karten gestalten, Verkauf eröffnen.

Zerlegung ist rekursiv — man bricht die Dinge weiter herunter, bis jedes Stück einfach genug ist, um es direkt zu lösen. So wird jedes große Softwaresystem gebaut: nicht als ein riesiges Programm, sondern als Tausende kleiner, kombinierbarer Teile.

**Zentrale Erkenntnis:** Wenn Sie ein Problem nicht lösen können, haben Sie es wahrscheinlich nicht genug zerlegt.

### Übung

Zerlegen Sie das folgende Problem in Teilprobleme: „Eine Website bauen, auf der Nutzer Gitarrenakkorde suchen können." Zerlegen Sie weiter, bis jedes Teilproblem etwas ist, das eine Person an einem Tag oder weniger erledigen könnte. Wie viele Zerlegungsebenen brauchten Sie?

---

## 3. Mustererkennung

**Mustererkennung** ist die Fähigkeit, Ähnlichkeiten zwischen bereits gelösten Problemen und neuen Problemen zu bemerken.

**Beispiel:** Das Sortieren einer Hand Spielkarten und das Sortieren einer Namensliste von Schülern sind dasselbe Problem — Elemente nach einer Vergleichsregel in eine Reihenfolge bringen. Sobald Sie einen Sortieralgorithmus kennen, können Sie ihn auf alles anwenden, was verglichen werden kann.

Muster tauchen überall in der Informatik auf:
- Durchsuchen einer Sammlung (ein Buch in der Bibliothek finden, eine Datei auf der Festplatte finden, eine Note auf dem Griffbrett finden)
- Elemente filtern, die Kriterien entsprechen (Spam-Filter, Bildsuche, Akkordsuche)
- Daten von einem Format in ein anderes umwandeln (Übersetzung, Dateikonvertierung, Transposition)

Erfahrene Programmierer lösen Probleme nicht schneller, weil sie klüger sind, sondern weil sie Muster erkennen. Sie sehen ein neues Problem und denken: „Das ist im Grunde ein Suchproblem" oder „Das ist eine Graphentraversierung" — und greifen auf eine bekannte Lösung zurück.

### Übung

Betrachten Sie diese drei Probleme. Welches Muster verbindet sie?
1. Die kürzeste Route zwischen zwei Städten finden
2. Die wenigsten Akkordwechsel finden, um von einem Akkord zu einem anderen zu gelangen
3. Die minimale Anzahl von Zügen finden, um ein Rätsel zu lösen

> Sie sind alle **Kürzeste-Weg-Probleme** — das Finden der kostenminimalen Schrittfolge zwischen einem Startzustand und einem Zielzustand.

---

## 4. Abstraktion — Ignorieren, was nicht zählt

**Abstraktion** ist die Kunst, irrelevante Details abzustreifen, um sich auf das zu konzentrieren, was für das jeweilige Problem wichtig ist.

Wenn Sie eine Karte zeichnen, fügen Sie nicht jeden Baum, jeden Riss im Pflaster, jeden Grashalm ein. Sie fügen Straßen, Orientierungspunkte und Entfernungen ein — die für die Navigation relevanten Details. Alles andere wird abstrahiert.

In algorithmischem Denken bedeutet Abstraktion:
- Ein reales Problem durch ein vereinfachtes Modell darstellen
- Details ignorieren, die die Lösung nicht beeinflussen
- Klare Ein- und Ausgaben definieren

**Beispiel:** Wenn Sie den kürzesten Weg zwischen zwei Städten finden möchten, müssen Sie nicht die Farbe der Straßenschilder oder die Geschwindigkeitsbegrenzung modellieren (es sei denn, Geschwindigkeit ist relevant für Ihr Problem). Sie abstrahieren die Karte zu einem **Graphen**: Städte sind Knoten, Straßen sind Kanten, Entfernungen sind Gewichte. Nun können Sie einen Graphenalgorithmus anwenden, ohne an Asphalt zu denken.

Abstraktion ermöglicht es, dass Algorithmen **universell einsetzbar** sind. Ein Sortieralgorithmus kümmert sich nicht darum, ob er Zahlen, Namen oder Gitarrenakkorde sortiert. Er muss nur wissen, wie man zwei Elemente vergleicht. Alles andere wird abstrahiert.

### Übung

Sie bauen ein System zur Empfehlung von Übungsprogrammen für Gitarrenschüler. Welche Details über jeden Schüler sind für den Algorithmus relevant? Welche können abstrahiert werden? Erstellen Sie zwei Listen: „einbeziehen" und „ignorieren."

---

## 5. Teile und Herrsche

**Teile und Herrsche** (Divide and Conquer) ist eine spezifische algorithmische Strategie:

1. **Teile** das Problem in kleinere Teilprobleme gleichen Typs
2. **Löse** jedes Teilproblem (rekursiv, falls nötig)
3. **Kombiniere** die Ergebnisse

Dies unterscheidet sich von allgemeiner Zerlegung. Bei Teile und Herrsche haben die Teilprobleme die **gleiche Struktur** wie das Original — nur kleiner.

**Beispiel — Binäre Suche (ein Wort im Wörterbuch nachschlagen):**
1. Öffnen Sie das Wörterbuch in der Mitte
2. Steht das Wort auf dieser Seite? Wenn ja, fertig.
3. Wenn das Wort alphabetisch vor dieser Seite kommt, wiederholen Sie mit der ersten Hälfte
4. Wenn es danach kommt, wiederholen Sie mit der zweiten Hälfte
5. Halbieren Sie weiter, bis Sie das Wort finden

Jeder Schritt halbiert den verbleibenden Suchraum. Ein Wörterbuch mit 100.000 Wörtern erfordert höchstens 17 Schritte (da 2^17 = 131.072 > 100.000). Vergleichen Sie das mit dem Starten bei Seite 1 und dem Lesen jedes Eintrags — bis zu 100.000 Schritte.

**Klassische Teile-und-Herrsche-Algorithmen:**
- **Binäre Suche** — ein Element in einer sortierten Sammlung finden
- **Mergesort** — Sortieren durch Teilen, Sortieren der Hälften, dann Zusammenführen
- **Quicksort** — Sortieren durch Wahl eines Pivots und Partitionierung

### Übung

Sie haben eine sortierte Liste von 1.000 Liedern. Wie viele Vergleiche braucht die binäre Suche maximal, um ein bestimmtes Lied zu finden? (Hinweis: Wie oft können Sie 1.000 halbieren, bevor Sie bei 1 ankommen?)

> log2(1000) ~ 10. Maximal 10 Vergleiche — verglichen mit 1.000 bei einer linearen Suche.

---

## 6. Gierige vs. erschöpfende Ansätze

Zwei große Algorithmenfamilien vertreten unterschiedliche Philosophien:

**Gierige Algorithmen** treffen bei jedem Schritt die lokal optimale Wahl in der Hoffnung, dass dies zu einer global optimalen Lösung führt.

*Beispiel — Wechselgeld mit möglichst wenigen Münzen:*
- Betrag: 67 Cent
- Gieriger Ansatz: Die größte passende Münze nehmen. 50 (zwei 20+10 bzw. 50er) → dann weiter mit den Resten. Ergebnis variiert je nach Münzsystem.
- Für Euro-Münzen funktioniert gierig oft. Aber für ein Münzsystem mit 1, 3 und 4 Cent scheitert der gierige Ansatz: Für 6 Cent liefert gierig 4+1+1 (3 Münzen), aber optimal ist 3+3 (2 Münzen).

**Erschöpfende Algorithmen** prüfen jede mögliche Lösung und wählen die beste. Sie finden immer die optimale Antwort, können aber langsam sein.

*Beispiel — Das Handlungsreisenden-Problem:*
- 10 Städte besuchen und auf kürzestem Weg nach Hause zurückkehren
- Erschöpfend: Alle möglichen Reihenfolgen ausprobieren (10! = 3.628.800 Routen), jede messen, die kürzeste wählen
- Das garantiert die optimale Route, ist aber rechenintensiv

| Ansatz | Vorteil | Nachteil | Einsatz wenn |
|--------|---------|----------|-------------|
| Gierig | Schnell, einfach | Kann die optimale Lösung verfehlen | Gut genug reicht aus |
| Erschöpfend | Garantiert optimal | Langsam bei großen Problemen | Korrektheit ist kritisch und die Eingabe ist klein |

Viele reale Algorithmen mischen beide Ansätze: gierige Heuristiken zum Beschneiden des Suchraums, dann erschöpfende Prüfung der verbleibenden Kandidaten.

### Übung

Sie packen einen Koffer mit Gegenständen unterschiedlicher Gewichte und Werte, und der Koffer hat ein Gewichtslimit. Beschreiben Sie einen gierigen und einen erschöpfenden Ansatz. Welchen würden Sie bei 5 Gegenständen verwenden? Bei 500?

> *Gierig:* Gegenstände nach Wert-zu-Gewicht-Verhältnis sortieren, Gegenstände vom höchsten Verhältnis hinzufügen, bis der Koffer voll ist. *Erschöpfend:* Jede mögliche Kombination ausprobieren, den Gesamtwert für jene innerhalb des Gewichtslimits berechnen, die beste wählen. Bei 5 Gegenständen (32 Kombinationen) ist erschöpfend machbar. Bei 500 Gegenständen (2^500 Kombinationen) ist erschöpfend unmöglich — verwenden Sie gierig oder einen intelligenteren Algorithmus.

---

## 7. O-Notation — Wie schnell ist schnell genug?

Nicht alle Algorithmen sind gleich geschaffen. Die **O-Notation** (Big-O) beschreibt, wie die Laufzeit eines Algorithmus mit zunehmender Eingabegröße wächst.

Sie müssen die O-Notation jetzt nicht exakt berechnen können. Sie brauchen ein **Gefühl** dafür, was die Kategorien bedeuten:

| O-Notation | Name | Beispiel | 1.000 Elemente | 1.000.000 Elemente |
|------------|------|----------|----------------|-------------------|
| O(1) | Konstant | Zugriff auf ein Array-Element per Index | 1 Schritt | 1 Schritt |
| O(log n) | Logarithmisch | Binäre Suche | ~10 Schritte | ~20 Schritte |
| O(n) | Linear | Jedes Element einmal durchlaufen | 1.000 Schritte | 1.000.000 Schritte |
| O(n log n) | Linearithmisch | Mergesort, Quicksort | ~10.000 Schritte | ~20.000.000 Schritte |
| O(n^2) | Quadratisch | Jedes Paar vergleichen | 1.000.000 Schritte | 1.000.000.000.000 Schritte |
| O(2^n) | Exponentiell | Erschöpfende Teilmengensuche | ~10^301 Schritte | Vergessen Sie es |

Die zentrale Erkenntnis: **Der Unterschied zwischen Algorithmenkategorien wächst enorm mit der Eingabegröße.** Ein O(n)-Algorithmus und ein O(n^2)-Algorithmus fühlen sich bei 10 Elementen beide sofort an. Bei einer Million Elementen endet der eine in einer Sekunde und der andere braucht Tage.

Deshalb ist algorithmisches Denken wichtig. Die Wahl des richtigen Algorithmus kann den Unterschied zwischen einem Programm, das funktioniert, und einem, das nie fertig wird, ausmachen.

### Übung

Sie haben zwei Algorithmen zum Durchsuchen einer Musikbibliothek:
- Algorithmus A: prüft jedes Lied einzeln (O(n))
- Algorithmus B: nutzt einen sortierten Index und binäre Suche (O(log n))

Wie viele Schritte braucht jeder bei einer Bibliothek mit 10 Millionen Liedern ungefähr?
> A: 10.000.000 Schritte. B: log2(10.000.000) ~ 23 Schritte. Algorithmus B ist über 400.000-mal schneller.

---

## Schlüsselbegriffe

| Begriff | Definition |
|---------|-----------|
| **Algorithmus** | Eine endliche Folge wohldefinierter Schritte, die eine Eingabe in eine Ausgabe transformiert |
| **Zerlegung** | Aufteilen eines komplexen Problems in kleinere, handhabbare Teilprobleme |
| **Mustererkennung** | Erkennen von Ähnlichkeiten zwischen einem neuen Problem und zuvor gelösten Problemen |
| **Abstraktion** | Abstreifen irrelevanter Details, um sich auf das für die Lösung Wesentliche zu konzentrieren |
| **Teile und Herrsche** | Aufspalten eines Problems in kleinere Instanzen desselben Problems, rekursives Lösen |
| **Gieriger Algorithmus** | Treffen der lokal optimalen Wahl bei jedem Schritt |
| **Erschöpfender Algorithmus** | Prüfen jeder möglichen Lösung, um garantiert die beste zu finden |
| **O-Notation** | Klassifizierung der Algorithmus-Effizienz danach, wie die Laufzeit mit der Eingabegröße wächst |

---

## Selbstüberprüfung

**1. Welche drei Eigenschaften muss ein gültiger Algorithmus haben?**
> Endlichkeit (er terminiert), Bestimmtheit (jeder Schritt ist eindeutig) und Ausführbarkeit (jeder Schritt kann tatsächlich durchgeführt werden).

**2. Sie müssen in einer unsortierten Liste von 1.000 Namen nach einem Namen suchen. Was ist die beste erreichbare O-Notation?**
> O(n) — lineare Suche. Ohne Sortierung oder Indizierung muss man potenziell jedes Element prüfen. Wäre die Liste sortiert, könnte man binäre Suche mit O(log n) nutzen.

**3. Ein gieriger Algorithmus für Wechselgeld liefert für Münzen von 1, 3 und 4 Cent bei 6 Cent die falsche Antwort. Warum?**
> Der gierige Ansatz wählt die größte Münze zuerst (4), braucht dann 1+1 für den Rest (3 Münzen insgesamt). Aber 3+3 benötigt nur 2 Münzen. Gierig scheitert, weil die lokal optimale Wahl (größte Münze) nicht zur global optimalen Lösung führt.

**4. Warum gilt O(n log n) als effizient für das Sortieren?**
> Es ist mathematisch bewiesen, dass kein vergleichsbasierter Sortieralgorithmus im schlimmsten Fall besser als O(n log n) sein kann. Mergesort und Quicksort erreichen diese Schranke und sind damit unter vergleichsbasierten Sortierungen optimal.

**Bestanden-Kriterien:** Ein gegebenes Problem in Teilprobleme zerlegen, identifizieren, welcher algorithmische Ansatz (gierig, erschöpfend, Teile-und-Herrsche) zu einem gegebenen Szenario passt, und O-Notation-Unterschiede anhand konkreter Beispiele erklären.

---

## Forschungsgrundlage

- Algorithmisches Denken (Zerlegung, Mustererkennung, Abstraktion) wird als zentrale Kompetenz des informatischen Denkens anerkannt
- Teile und Herrsche, gierig und erschöpfende Suche sind die drei fundamentalen algorithmischen Paradigmen
- Die O-Notation bietet ein hardwareunabhängiges Maß für Algorithmus-Effizienz
- Das Vermitteln algorithmischer Intuition vor formaler Analyse verbessert den Problemlösungstransfer
- Quellen: Konsens der Informatik-Didaktik, Lehrplan des Fachbereichs Informatik der Streeling-Universität
- Überzeugungszustand: T(0.91) F(0.02) U(0.05) C(0.02)
