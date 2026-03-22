---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Kompression Grundlagen — Ratio, Threshold, Attack, Release"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ und Kompression: Warum die Reihenfolge in der Signalkette entscheidend ist

> **Fachbereich Tontechnik** | Stufe: Mittelstufe | Dauer: 35 Minuten

## Lernziele
- Die technischen Unterschiede zwischen Komp→EQ und EQ→Komp Signalketten verstehen
- Erkennen, wann welche Reihenfolge bei Gesangsaufnahmen bessere Ergebnisse liefert
- Die EQ→Komp→EQ Sandwich-Technik für maximale Kontrolle anwenden
- Frequenzabhängige Kompressionsartefakte erkennen und vermeiden

---

## 1. Die Kernfrage

Spielt es eine Rolle, ob man vor oder nach dem EQ komprimiert? **Ja** — und zwar messbar. Die Reihenfolge verändert, wie der Kompressor auf den Frequenzinhalt reagiert, was die Natürlichkeit der Dynamik und die Klarheit des Klangs beeinflusst.

Der Grund ist einfach: Ein Kompressor reagiert auf *Pegel*. Wenn bestimmte Frequenzen lauter sind (z.B. Nahbesprechungseffekt bei 100-200 Hz oder Zischlaute bei 4-10 kHz), reagiert der Kompressor auf *diese Frequenzen*, nicht nur auf die gesamte Gesangsperformance.

---

## 2. Kompression vor EQ (Komp→EQ)

```
Gesang → [Kompressor] → [EQ] → Summenbus
```

**Was passiert:**
- Der Kompressor sieht das Rohsignal — einschließlich problematischer Frequenzen
- Wenn Zischlaute laut sind (4-10 kHz Spitzen), kann dies die Kompression auf diesen Transienten auslösen
- Der Kompressor „pumpt" auf problematischen Frequenzen, anstatt die Gesamtdynamik zu kontrollieren
- Der nachfolgende EQ formt das bereits komprimierte Signal

**Wann einsetzen:**
- Wenn die Gesangsaufnahme gut ist und minimale Frequenzprobleme aufweist
- Wenn der Kompressor auf das volle, natürliche Signal reagieren soll
- Bei sanfter Kompression (2:1 Ratio, langsames Attack) als „Kleber"

**Risiko:** Frequenzabhängiges Pumpen. Der Kompressor weiß nicht, dass er nicht auf den 200 Hz Nahbesprechungseffekt reagieren soll — er sieht nur den Pegel.

---

## 3. EQ vor Kompression (EQ→Komp)

```
Gesang → [EQ] → [Kompressor] → Summenbus
```

**Was passiert:**
- Der korrigierende EQ beseitigt zuerst Probleme: Nahbesprechungseffekt bei 200 Hz beschneiden, Zischlaute bei 6 kHz zähmen
- Der Kompressor erhält ein saubereres, ausgewogeneres Signal
- Die Kompression reagiert auf die *musikalische Darbietung*, nicht auf Frequenzartefakte
- Ergebnis: natürlichere, transparentere Kompression

**Wann einsetzen:**
- Wenn die Aufnahme merkliche Frequenzprobleme hat (Nahbesprechung, Raumresonanzen, Härte)
- Wenn der Kompressor auf die Dynamik reagieren soll, nicht auf Frequenzspitzen
- Bei schwankender Aufnahmequalität

**Dies ist generell die sicherere Standardwahl** — Frequenzprobleme beheben, bevor der Kompressor die Dynamik verwaltet.

---

## 4. Das Sandwich: EQ→Komp→EQ

```
Gesang → [Korrektur-EQ] → [Kompressor] → [Klang-EQ] → Summenbus
```

Dies ist aus gutem Grund der professionelle Standard:

1. **Erster EQ (korrektiv):** Hochpassfilter bei 80-100 Hz, Mulm bei 200-300 Hz beschneiden, Raumresonanzen auskerben. Dies ist chirurgisch — man entfernt Probleme, formt nicht den Klang.

2. **Kompressor:** Reagiert nun auf ein sauberes Signal. Ratio einstellen (3:1-4:1 typisch für Gesang), Threshold auf ca. 6 dB Pegelreduktion, mittleres Attack (10-30ms) um Transienten zu erhalten, mittleres Release (50-100ms).

3. **Zweiter EQ (klangformend):** Nun den Sound kreativ gestalten. Luft bei 10-12 kHz anheben, Präsenz bei 3-5 kHz hinzufügen, die unteren Mitten aufwärmen. Dieser EQ sitzt nach der Kompression, sodass Anhebungen den Kompressor nicht triggern.

**Warum es funktioniert:** Trennung der Zuständigkeiten. Der korrigierende EQ verhindert Kompressorartefakte. Der Kompressor verwaltet die Dynamik eines sauberen Signals. Der klangformende EQ gestaltet den finalen Charakter, ohne die Dynamik zu beeinflussen.

---

## 5. Frequenzabhängige Artefakte im Blick

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Pumpen bei Plosiven | Tieffrequente Impulse triggern den Kompressor | Hochpassfilter vor dem Kompressor (EQ→Komp) |
| Verstärkte Zischlaute | Kompressor reduziert den Körper, Zischlaute bleiben | De-Esser vor dem Kompressor oder EQ-Absenkung bei 6 kHz vorschalten |
| Dumpfheit nach Kompression | Schnelles Attack unterdrückt Transienten | Langsameres Attack (15-30ms) oder Parallelkompression |
| Inkonsistenter Klang | Kompressor reagiert unterschiedlich auf leise vs. laute Passagen | Zwei Stufen sanfter Kompression statt einer starken Stufe |

---

## 6. Dynamischer EQ: Die moderne Alternative

Dynamischer EQ kombiniert EQ und Kompression in einem Prozessor. Jedes EQ-Band wird nur aktiv, wenn die Frequenz einen Schwellenwert überschreitet — wie ein Kompressor, der nur auf bestimmte Frequenzen wirkt.

**Anwendungsfall:** Zischlaute, die über die gesamte Performance variieren. Eine statische Absenkung bei 6 kHz würde den gesamten Gesang dumpfer machen, aber ein dynamischer EQ greift nur ein, wenn die Zischlaute den Schwellenwert überschreiten.

Dies ersetzt nicht die Komp→EQ-Frage — es ist ein spezialisiertes Werkzeug für frequenzabhängige Dynamikprobleme.

---

## Übung

### Übung 1: A/B-Vergleich der Reihenfolge
Nehmen Sie eine Gesangsaufnahme. Richten Sie zwei parallele Ketten ein:
- Kette A: Kompressor (4:1, -6 dB Pegelreduktion) → EQ (Anhebung 3 kHz +3 dB, Absenkung 250 Hz -4 dB)
- Kette B: Gleicher EQ → Gleicher Kompressor

Hören Sie beide an. Wo hören Sie den Unterschied? Achten Sie auf:
- Tieffrequente Konsistenz (Handhabung des Nahbesprechungseffekts)
- Zischlautpegel
- Gesamte „Natürlichkeit" der Kompression

### Übung 2: Bauen Sie ein Sandwich
Aufbau: Hochpassfilter bei 100 Hz + Absenkung bei 250 Hz → Kompressor (3:1) → Präsenzanhebung bei 4 kHz + Luft bei 12 kHz. Vergleichen Sie mit einer einzelnen EQ-dann-Komprimieren-Kette.

---

## Wichtigste Erkenntnisse
- **Die Reihenfolge ist entscheidend** — der Kompressor reagiert auf die lautesten Frequenzen im Eingangssignal
- **EQ→Komp ist die sicherere Standardwahl** — Probleme vor der Kompression beheben für natürlichere Ergebnisse
- **EQ→Komp→EQ Sandwich ist der professionelle Standard** — erst korrigieren, dann formen
- **Es gibt keine universell „richtige" Reihenfolge** — es hängt von der Aufnahme, dem Genre und der Absicht ab
- **Dynamischer EQ** ist ein modernes Werkzeug für frequenzabhängige Dynamikprobleme
- Das Ziel ist immer: Dynamik kontrollieren, ohne den natürlichen Charakter der Darbietung zu zerstören

## Weiterführende Lektüre
- Fachbereich Physik: Akustik — Frequenz, Amplitude und Obertonbeziehungen
- Fachbereich Musik: Wie die Klangfarbenwahrnehmung Mischentscheidungen beeinflusst
- Fachbereich Informatik: DSP-Algorithmen hinter EQ und Kompression
- AES (Audio Engineering Society): Standards für Lautheitsmessung (ITU-R BS.1770)

---
*Erstellt durch Seldon-Forschungszyklus audio-engineering-2026-03-23-001 am 23.03.2026.*
*Forschungsfrage: Führt die Reihenfolge von Kompression vor EQ gegenüber EQ vor Kompression zu messbar unterschiedlichen Ergebnissen bei Gesangsaufnahmen?*
*Überzeugungsgrad: T (Konfidenz: 0.80)*
