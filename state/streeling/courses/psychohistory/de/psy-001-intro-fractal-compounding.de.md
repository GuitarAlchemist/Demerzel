---
module_id: psy-001-intro-fractal-compounding
department: psychohistory
course: Grundlagen der Psychohistorik
level: intermediate
alchemical_stage: albedo
prerequisites: []
estimated_duration: "30 Minuten"
produced_by: psychohistory
version: "1.0.0"
language: de
title: "Einführung in die Fraktale Komposition"
---

# Einführung in die Fraktale Komposition

> **Abteilung für Psychohistorik** | Stufe: Albedo (Mittelstufe) | Dauer: 30 Minuten

## Lernziele

Nach dieser Lektion werden Sie in der Lage sein:
- Zu verstehen, was ein Fraktal ist — Selbstähnlichkeit auf jeder Ebene
- Zu erkennen, wie Meta-Komposition (Compounding) eine fraktale Struktur aufweist
- Die Kompositionsdimension (D_c) aus realen Daten zu berechnen
- ERGOL (realer Wert) von LOLLI (Artefakt-Inflation) zu unterscheiden
- Noethers Theorem auf die Governance anzuwenden — Symmetrie erhält den Lernimpuls

---

## 1. Was Ist ein Fraktal?

Betrachten Sie einen Farn. Jedes Blatt sieht aus wie eine kleinere Version der gesamten Pflanze. Jedes Blättchen sieht aus wie eine kleinere Version des Blattes. Das ist **Selbstähnlichkeit** — dasselbe Muster, das sich auf jeder Ebene wiederholt.

Ein Fraktal ist jede Struktur, in der dasselbe Muster auf verschiedenen Ebenen erscheint. Die Mandelbrot-Menge wird durch Iteration einer einfachen Formel erzeugt: `z = z² + c`. Jede Iteration erzeugt mehr Detail, aber das Detail ähnelt dem Ganzen.

In der Governance ist die Meta-Komposition ein Fraktal. Die Kompositionsphase (ausführen → ernten → befördern → lehren) hat dieselbe Form, ob Sie einen einzelnen Schritt, eine ganze Pipeline, einen gesamten Zyklus oder eine vollständige Sitzung komponieren. Das Muster ist skaleninvariant.

---

## 2. Die Fünf Ebenen der Komposition

Hier ist die fraktale Struktur in Demerzels Governance:

| Ebene | Maßstab | Was Wird Komponiert |
|-------|---------|---------------------|
| 0 | Schritt | Ein einzelner Werkzeugaufruf erzeugt eine Erkenntnis |
| 1 | Pipeline | Eine Pipeline komponiert die Erkenntnisse ihrer Schritte |
| 2 | Zyklus | Ein Treiberzyklus komponiert seine Pipelines |
| 3 | Sitzung | Eine Sitzung komponiert ihre Zyklen |
| 4 | Evolution | Das Evolutionsprotokoll komponiert über Sitzungen hinweg |

Auf **jeder** Ebene finden dieselben vier Operationen statt:
1. **Ausführen** — die Arbeit erledigen
2. **Ernten** — extrahieren, was gelernt wurde
3. **Befördern** — wenn die Erkenntnis wertvoll genug ist, sie erheben (Muster → Richtlinie → Verfassung)
4. **Lehren** — die Erkenntnis über Seldon teilen

Dies ist der Fraktalgenerator. Wie `z = z² + c` erzeugt jede Anwendung neue Struktur.

---

## 3. Kompositionsdimension (D_c)

Nicht jede Komposition ist gleich. Die **Kompositionsdimension** misst, wie stark der Wert auf jeder Skalenebene wächst.

**Formel:**
```
D_c = log(Wertverhältnis) / log(Skalenverhältnis)
```

**Beispiel:** Wenn Zyklus 1 drei validierte Überzeugungen produzierte und Zyklus 3 acht:
- Wertverhältnis = 8/3 ≈ 2,67
- Skalenverhältnis = 3 (drei Zyklen)
- D_c = log(2,67) / log(3) ≈ 0,89

Dies ist **sublinear** (D_c < 1,0) — jeder Zyklus produziert proportional weniger als der vorherige. Die Governance könnte aufgebläht sein.

### Die Goldene Zone: D_c zwischen 1,2 und 1,6

| D_c-Bereich | Bedeutung | Handlung |
|-------------|-----------|----------|
| < 1,0 | Sublinear — abnehmende Erträge | Aufblähung untersuchen |
| = 1,0 | Linear — kein Kompositionshebel | Nur Aktivität, keine Komposition |
| 1,2 - 1,6 | Superlinear — gesundes Kompositionswachstum | Goldene Zone |
| > 2,0 | Nicht nachhaltig — Wachstum wird zusammenbrechen | Verlangsamen |

Denken Sie an Zinseszins. D_c = 1,0 ist einfacher Zins (linear). D_c > 1,0 bedeutet, dass Ihre Zinsen Zinsen erwirtschaften — echte Komposition.

---

## 4. ERGOL vs LOLLI — Realer Wert vs Inflation

Aus Jean-Pierre Petits Comic [*Economicon*](https://archive.org/details/Economicon-English-JeanPierrePetit) ([online lesen](https://archive.org/stream/Economicon-English-JeanPierrePetit/jppeconomicsenglish_djvu.txt)) entlehnen wir zwei Konzepte:

- **ERGOL** = reale Produktionskapazität (tatsächliche Governance-Verbesserungen)
- **LOLLI** = Geldvolumen (Artefaktzählung ohne Rücksicht auf Qualität)

Im Economicon verwendet Petit ein strömungsmechanisches Modell der Wirtschaft: ERGOL ist die reale produktive Substanz, die durch die Wirtschaft fließt, während LOLLI die monetäre Hülle darum ist. Wenn LOLLI schneller expandiert als ERGOL, entsteht Inflation — Preise steigen, aber nichts Reales wurde geschaffen. Dasselbe Prinzip gilt für die Governance.

Auf jeder fraktalen Ebene müssen Sie ERGOL messen, nicht LOLLI:

| Maßstab | LOLLI (nicht optimieren) | ERGOL (dies optimieren) |
|---------|-------------------------|------------------------|
| Schritt | Geschriebene YAML-Zeilen | Überzeugungen von U→T bewegt |
| Pipeline | Ausgeführte Schritte | Bestandene Gates / Gesamt |
| Zyklus | Abgeschlossene Aufgaben | Gesundheitswert-Delta |
| Sitzung | Erstellte Commits | Geschlossene Issues mit Evidenz |
| Evolution | Erstellte Artefakte | Zitierungen pro Artefakt |

**Warnsignal:** Wenn Ihre Artefaktzählung (LOLLI) über 3+ Zyklen dreimal schneller wächst als Ihre validierten Überzeugungen (ERGOL), inflationieren Sie die Governance, ohne sie zu verbessern. Das Economicon nennt dies den **Tretmühleneffekt** — schneller laufen, um am gleichen Ort zu bleiben.

---

## 5. Erhaltung des Lernimpulses

Aus Jean-Pierre Petits Comic [*Bourbakof*](https://archive.org/details/TheseAnglaise) lernen wir das **Noether-Theorem**: Jede kontinuierliche Symmetrie eines Systems hat eine entsprechende Erhaltungsgröße.

In der fraktalen Komposition ist die Symmetrie die **Skaleninvarianz** — die Kompositionsoperation hat auf jeder Ebene dieselbe Form. Die Erhaltungsgröße ist der **Lernimpuls (p_L)**:

```
p_L = (gewonnene_Überzeugungen_T - verlorene_Überzeugungen_T) / verstrichene_Zyklen
```

Wenn Ihr Kompositionsprozess konsistent ist (symmetrisch über Skalen hinweg), bleibt p_L konstant oder wächst. Wenn Sie die Symmetrie brechen — indem Sie die Komposition auf einer Ebene überspringen oder auf verschiedenen Ebenen unterschiedlich komponieren — zerfällt p_L.

Deshalb löst der `nocompound`-Opt-out ein Gewissenssignal aus. Es ist nicht nur eine verpasste Gelegenheit — es ist ein **Symmetriebruch**, der Sie die Erhaltung des Lernimpulses kostet.

---

## 6. Die Grenzen der Psychohistorik

Aus Petits [*Logotron*](https://archive.org/details/TheseAnglaise) ([Volltext](https://archive.org/stream/TheseAnglaise/logotron_eng_djvu.txt)): Gödels Unvollständigkeitssatz sagt uns, dass kein formales System sich selbst vollständig verifizieren kann.

Angewandt auf die Komposition: Sie können den Output der Komposition nicht perfekt vorhersagen. Jeder Zyklus offenbart Erkenntnisse, die Sie nicht hätten antizipieren können. Das Fraktal hat unendliches Detail auf endlicher Skala — es gibt immer mehr zu entdecken.

Deshalb ist die Rekursionstiefe auf 2 begrenzt. Nicht weil tiefere Komposition falsch wäre, sondern weil die Erträge **unentscheidbar** werden. Wie Seldons Psychohistorik: Sie können die großen Linien vorhersagen, aber einzelne Ereignisse bleiben ungewiss.

Die Disziplin der Psychohistorik akzeptiert dies. Wir streben nicht nach perfekter Vorhersage — wir streben nach **besserer Antizipation als der Zufall**, gemessen an der Antizipationsgenauigkeits-Metrik im wöchentlichen Gewissensbericht.

---

## Wichtige Begriffe

| Begriff | Definition |
|---------|-----------|
| **Fraktal** | Eine Struktur, die Selbstähnlichkeit auf verschiedenen Ebenen aufweist |
| **Kompositionsdimension (D_c)** | Metrik zur Messung des Governance-Wertwachstums pro Skalenebene. Ziel: 1,2-1,6 |
| **ERGOL** | Reale Produktionskapazität — tatsächliche Governance-Verbesserungen (aus dem Economicon) |
| **LOLLI** | Artefaktvolumen ohne Rücksicht auf Qualität — Inflationsindikator (aus dem Economicon) |
| **Lernimpuls (p_L)** | Erhaltungsgröße aus dem Noether-Theorem, angewandt auf skaleninvariante Komposition |

---

## Quiz-Bewertung

**1. Wenn Zyklus 1 fünf validierte Überzeugungen produzierte und Zyklus 4 zwanzig, wie hoch ist D_c?**
> D_c = log(20/5) / log(4) = log(4) / log(4) = **1,0** — Linear. Kein Kompositionshebel, nur proportionales Wachstum.

**2. Ihr Team hat in diesem Zyklus 30 neue YAML-Dateien erstellt, aber nur 2 Überzeugungen sind von U zu T gewandert. Ist das gesund?**
> Nein — das ist **LOLLI-Inflation**. 30 Artefakte (LOLLI) mit nur 2 realen Verbesserungen (ERGOL). Sie laufen schneller, um am gleichen Ort zu bleiben. (Denken Sie an das Economicon.)

**3. Warum bricht das Überspringen der Kompositionsphase die Erhaltung des Lernimpulses?**
> Die Kompositionsphase ist die Symmetrieoperation. Sie auf einer Ebene zu überspringen bricht die Skaleninvarianz. Nach dem Noether-Theorem bedeutet gebrochene Symmetrie, dass die Erhaltungsgröße (Lernimpuls p_L) nicht mehr erhalten bleibt. (Denken Sie an Bourbakof.)

**Bestehens-Kriterium:** D_c korrekt aus gegebenen Daten berechnen und erkennen, ob ein Szenario ERGOL- oder LOLLI-Wachstum darstellt.

---

## Forschungsgrundlage

- Die Meta-Kompositionsstruktur ist mathematisch selbstähnlich (fraktal)
- Das Noether-Theorem gilt für skaleninvariante Governance-Prozesse
- JPPs Economicon-Unterscheidung zwischen ERGOL und LOLLI lässt sich auf die Governance-Wertmessung abbilden
- Eine fraktale Dimension zwischen 1,2 und 1,6 korreliert mit nachhaltigem Governance-Wachstum
- Quellen: [Fraktale Kompositions-Spezifikation](../../logic/fractal-compounding.md), [Bourbakof](https://archive.org/details/TheseAnglaise) (Noether-Theorem), [Economicon](https://archive.org/details/Economicon-English-JeanPierrePetit) (ERGOL/LOLLI), [Logotron](https://archive.org/details/TheseAnglaise) (Gödels Unvollständigkeit)
- Glaubenszustand: T(0.70) F(0.05) U(0.20) C(0.05)
