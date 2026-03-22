---
module_id: mat-001-proof-strategies
department: mathematics
course: "Grundlagen des mathematischen Denkens"
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "30 minutes"
produced_by: mathematics
version: "1.0.0"
---

# Beweisstrategien — Wie man Dinge beweist

> **Fachbereich Mathematik** | Stufe: Nigredo (Einführung) | Dauer: 30 Minuten

## Lernziele

Nach dieser Lektion werden Sie in der Lage sein:
- Zu erklären, was ein mathematischer Beweis ist und warum er wichtig ist
- Den direkten Beweis anzuwenden, um eine Aussage aus bekannten Fakten herzuleiten
- Den Widerspruchsbeweis anzuwenden, um zu zeigen, dass eine Aussage wahr sein muss
- Die vollständige Induktion anzuwenden, um Aussagen über alle natürlichen Zahlen zu beweisen
- Zu erkennen, welche Beweisstrategie zu einem gegebenen Problem passt

---

## 1. Was ist ein Beweis?

Ein Beweis ist eine logische Argumentation, die über jeden Zweifel hinaus feststellt, dass eine mathematische Aussage wahr ist. Nicht wahrscheinlich wahr, nicht in den meisten Fällen wahr — **immer** wahr, in jeder möglichen Situation, die die Aussage beschreibt.

Das macht die Mathematik einzigartig unter den Wissenschaften. In den Naturwissenschaften sammelt man Belege und bildet Theorien, die durch neue Daten widerlegt werden könnten. In der Mathematik bleibt etwas, das einmal bewiesen ist, für immer bewiesen. Euklids Beweise aus dem Jahr 300 v. Chr. sind heute genauso gültig wie damals.

Ein Beweis beginnt mit **Axiomen** (als wahr akzeptierte Aussagen) und **zuvor bewiesenen Ergebnissen** und verwendet dann logische Regeln, um zur Schlussfolgerung zu gelangen. Jeder Schritt muss zwingend aus den vorhergehenden folgen.

Drei verbreitete Missverständnisse:
- **„Beispiele beweisen etwas."** Nein. Zu zeigen, dass eine Aussage für 10, 100 oder eine Million Fälle gilt, beweist nicht, dass sie für alle Fälle gilt. Ein einziges Gegenbeispiel kann eine Vermutung zerstören, die Milliarden von Tests bestanden hat.
- **„Beweise müssen lang und kompliziert sein."** Einige der schönsten Beweise sind kurz. Eleganz wird geschätzt.
- **„Es gibt nur einen Weg, etwas zu beweisen."** Die meisten Sätze können auf mehrere Arten bewiesen werden. Die richtige Strategie zu wählen, ist Teil der Kunst.

---

## 2. Direkter Beweis

Ein **direkter Beweis** beginnt bei dem, was man weiß, und schließt Schritt für Schritt vorwärts auf das, was man zeigen möchte.

**Aufbau:**
1. Die Voraussetzung annehmen (den „wenn"-Teil der Aussage)
2. Definitionen, bekannte Ergebnisse und logische Schritte anwenden
3. Bei der Schlussfolgerung ankommen (dem „dann"-Teil)

**Beispiel: Beweise, dass die Summe zweier gerader Zahlen gerade ist.**

*Aussage:* Wenn *a* und *b* gerade sind, dann ist *a + b* gerade.

*Beweis:*
- Da *a* gerade ist, gilt per Definition *a = 2m* für eine ganze Zahl *m*.
- Da *b* gerade ist, gilt per Definition *b = 2n* für eine ganze Zahl *n*.
- Dann ist *a + b = 2m + 2n = 2(m + n)*.
- Da *m + n* eine ganze Zahl ist, ist *a + b* das Zweifache einer ganzen Zahl, also per Definition gerade.

Das ist ein vollständiger Beweis. Jeder Schritt folgt logisch. Keine Lücken, kein Handwedeln.

**Wann den direkten Beweis verwenden:** Wenn man einen klaren Weg von der Voraussetzung zur Schlussfolgerung sieht. Wenn Definitionen algebraische Formen liefern, die man umformen kann. Das ist Ihre Standardstrategie — versuchen Sie es zuerst.

### Übung

Beweisen Sie, dass das Produkt zweier ungerader Zahlen ungerade ist. (Hinweis: Eine ungerade Zahl lässt sich als *2k + 1* für eine ganze Zahl *k* schreiben.)

> *Lösung:* Sei *a = 2m + 1* und *b = 2n + 1*. Dann ist *ab = (2m+1)(2n+1) = 4mn + 2m + 2n + 1 = 2(2mn + m + n) + 1*. Da *2mn + m + n* eine ganze Zahl ist, hat *ab* die Form *2k + 1*, ist also ungerade.

---

## 3. Widerspruchsbeweis (Beweis durch Widerspruch)

Manchmal ist der direkte Weg nicht offensichtlich. Der **Widerspruchsbeweis** geht einen anderen Weg: Man nimmt das Gegenteil dessen an, was man beweisen möchte, und zeigt dann, dass diese Annahme zu etwas Unmöglichem führt.

**Aufbau:**
1. Die Negation der zu beweisenden Aussage annehmen
2. Logisch aus dieser Annahme schließen
3. Zu einem Widerspruch gelangen (etwas, das offensichtlich falsch ist oder einer bekannten Tatsache widerspricht)
4. Schlussfolgern, dass die Annahme falsch sein muss, also die ursprüngliche Aussage wahr ist

**Beispiel: Beweise, dass die Quadratwurzel von 2 irrational ist.**

*Aussage:* Es gibt keinen Bruch *p/q* (mit ganzen Zahlen *p, q*, *q* ungleich Null, vollständig gekürzt), sodass *(p/q)^2 = 2*.

*Beweis:*
- **Annahme des Gegenteils:** Angenommen, sqrt(2) ist rational. Dann ist sqrt(2) = *p/q*, wobei *p* und *q* ganze Zahlen ohne gemeinsame Teiler sind (vollständig gekürzt).
- Quadrieren beider Seiten: *2 = p^2 / q^2*, also *p^2 = 2q^2*.
- Das bedeutet, *p^2* ist gerade, was bedeutet, dass *p* selbst gerade sein muss (da das Quadrat einer ungeraden Zahl ungerade ist). Also *p = 2k* für eine ganze Zahl *k*.
- Einsetzen: *(2k)^2 = 2q^2*, also *4k^2 = 2q^2*, also *q^2 = 2k^2*.
- Das bedeutet, *q^2* ist gerade, also ist *q* gerade.
- Aber nun sind sowohl *p* als auch *q* gerade, das heißt, sie teilen den Faktor 2. **Das widerspricht unserer Annahme**, dass *p/q* vollständig gekürzt war.
- Daher war unsere Annahme falsch. Die Quadratwurzel von 2 ist irrational.

**Wann den Widerspruchsbeweis verwenden:** Wenn man beweisen möchte, dass etwas nicht existiert, oder wenn die Aussage Wörter wie „kein", „kann nicht" oder „unmöglich" enthält. Auch nützlich, wenn der direkte Ansatz sich verheddert.

### Übung

Beweisen Sie durch Widerspruch, dass es keine größte ganze Zahl gibt. (Hinweis: Nehmen Sie an, es gäbe eine größte ganze Zahl *N*, und betrachten Sie *N + 1*.)

> *Lösung:* Angenommen, es existiert eine größte ganze Zahl *N*. Dann ist *N + 1* ebenfalls eine ganze Zahl (ganze Zahlen sind abgeschlossen unter Addition). Aber *N + 1 > N*, was der Annahme widerspricht, dass *N* die größte war. Folglich existiert keine größte ganze Zahl.

---

## 4. Vollständige Induktion

**Induktion** ist Ihr Werkzeug zum Beweisen von Aussagen über alle natürlichen Zahlen (oder jede unendliche Folge). Sie funktioniert wie eine Kette von Dominosteinen.

**Aufbau:**
1. **Induktionsanfang:** Beweisen, dass die Aussage für den ersten Wert gilt (üblicherweise *n = 0* oder *n = 1*)
2. **Induktionsschritt:** Annehmen, die Aussage gelte für einen beliebigen Wert *n = k* (die **Induktionsvoraussetzung**). Dann beweisen, dass sie auch für *n = k + 1* gelten muss.
3. **Schlussfolgerung:** Da der Induktionsanfang wahr ist und jeder Fall den nächsten impliziert, gilt die Aussage für alle natürlichen Zahlen.

Warum funktioniert das? Wenn der erste Dominostein fällt (Induktionsanfang) und jeder fallende Dominostein den nächsten umwirft (Induktionsschritt), dann fallen alle Dominosteine.

**Beispiel: Beweise, dass die Summe 1 + 2 + 3 + ... + n = n(n+1)/2 für alle positiven ganzen Zahlen n.**

*Induktionsanfang (n = 1):*
- Linke Seite: 1
- Rechte Seite: 1(1+1)/2 = 1
- Sie stimmen überein. Induktionsanfang gilt.

*Induktionsschritt:*
- **Induktionsvoraussetzung:** Angenommen, 1 + 2 + ... + k = k(k+1)/2 für eine positive ganze Zahl *k*.
- **Zeige, dass es für k + 1 gilt:** Wir brauchen 1 + 2 + ... + k + (k+1) = (k+1)(k+2)/2.
- Von der linken Seite ausgehend: 1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1) (unter Verwendung der Induktionsvoraussetzung)
- = (k+1)(k/2 + 1) = (k+1)(k+2)/2
- Das entspricht der Formel für *n = k + 1*. Der Induktionsschritt gilt.

*Schlussfolgerung:* Durch Induktion gilt die Formel für alle positiven ganzen Zahlen *n*.

**Wann Induktion verwenden:** Wenn die Aussage alle natürlichen Zahlen betrifft (oder alle Werte ab einem Startwert). Achten Sie auf Formeln mit *n*, Aussagen wie „für alle *n* >= 1" oder rekursive Definitionen.

### Übung

Beweisen Sie durch Induktion, dass *2^n > n* für alle positiven ganzen Zahlen *n*.

> *Lösung:*
> *Induktionsanfang (n = 1):* 2^1 = 2 > 1. Wahr.
> *Induktionsschritt:* Angenommen, 2^k > k. Dann ist 2^(k+1) = 2 * 2^k > 2k (nach Voraussetzung). Da 2k = k + k >= k + 1 für alle k >= 1, gilt 2^(k+1) > k + 1.
> Durch Induktion gilt 2^n > n für alle positiven ganzen Zahlen n.

---

## 5. Die richtige Strategie wählen

Wenn Sie eine Aussage beweisen sollen, stellen Sie sich diese Fragen:

| Frage | Wenn ja, versuchen Sie... |
|-------|--------------------------|
| Kann ich mit Definitionen und Algebra von der Voraussetzung zur Schlussfolgerung gelangen? | Direkter Beweis |
| Sagt die Aussage, dass etwas unmöglich ist oder nicht existiert? | Widerspruchsbeweis |
| Bezieht sich die Aussage auf alle natürlichen Zahlen oder hat eine rekursive Struktur? | Induktion |
| Komme ich mit dem direkten Beweis nicht weiter? | Widerspruchsbeweis als Alternative versuchen |

In der Praxis versuchen Mathematiker oft zuerst den direkten Beweis. Wenn das stockt, wechseln sie zum Widerspruchsbeweis. Wenn die Aussage natürliche Zahlen betrifft, ist Induktion meist die richtige Wahl.

Manche Aussagen können mit jeder der drei Methoden bewiesen werden. Mit zunehmender Erfahrung entwickeln Sie ein Gespür dafür, welcher Ansatz am elegantesten sein wird.

---

## 6. Häufige Fehler

- **Das annehmen, was man beweisen möchte.** Das nennt man Zirkelschluss. Beim direkten Beweis muss Ihr Ausgangspunkt die Voraussetzung sein, nicht die Schlussfolgerung.
- **Den Induktionsanfang vergessen.** Ohne den Induktionsanfang gibt es keinen ersten Dominostein. Der Induktionsschritt allein beweist nichts.
- **Die Induktionsvoraussetzung nicht klar formulieren.** Seien Sie explizit: „Angenommen, die Aussage gilt für *n = k*." Verwenden Sie dann diese Annahme, um den Fall *k + 1* zu beweisen.
- **Beim Widerspruchsbeweis keinen tatsächlichen Widerspruch erreichen.** Sie müssen bei etwas ankommen, das definitiv falsch ist — nicht nur seltsam oder unerwartet.

---

## Schlüsselbegriffe

| Begriff | Definition |
|---------|-----------|
| **Beweis** | Eine logische Argumentation, die feststellt, dass eine mathematische Aussage in allen Fällen wahr ist |
| **Axiom** | Eine Aussage, die ohne Beweis als wahr akzeptiert wird und als Ausgangspunkt dient |
| **Direkter Beweis** | Vorwärtsschließen von der Voraussetzung zur Schlussfolgerung unter Verwendung von Definitionen und Logik |
| **Widerspruchsbeweis** | Annehmen der Negation der gewünschten Schlussfolgerung und Herleiten eines Widerspruchs |
| **Vollständige Induktion** | Beweis eines Induktionsanfangs und eines Induktionsschritts, um eine Aussage für alle natürlichen Zahlen festzustellen |
| **Induktionsvoraussetzung** | Die Annahme, dass die Aussage für *n = k* gilt, verwendet im Induktionsschritt |
| **Gegenbeispiel** | Ein einzelner Fall, der eine Aussage widerlegt — ein Gegenbeispiel widerlegt eine universelle Behauptung |

---

## Selbstüberprüfung

**1. Was ist der grundlegende Unterschied zwischen einem Beweis und einer großen Sammlung von Beispielen?**
> Ein Beweis stellt die Wahrheit für alle Fälle durch logische Deduktion fest. Beispiele zeigen nur, dass bestimmte Fälle funktionieren, und können ein unentdecktes Gegenbeispiel nicht ausschließen.

**2. Welches sind beim Widerspruchsbeweis die drei Schritte nach dem Annehmen der Negation?**
> Logisch aus der Annahme schließen, bei einer Aussage ankommen, die einer bekannten Tatsache widerspricht, dann schlussfolgern, dass die Annahme falsch war.

**3. Was sind die zwei Bestandteile eines Induktionsbeweises?**
> Der Induktionsanfang (Beweis der Aussage für den ersten Wert) und der Induktionsschritt (Beweis, dass wenn die Aussage für *k* gilt, sie auch für *k + 1* gilt).

**4. Sie möchten beweisen, dass keine gerade Zahl größer als 2 eine Primzahl ist. Welche Strategie würden Sie verwenden?**
> Direkter Beweis: Per Definition kann eine gerade Zahl größer als 2 als *2k* geschrieben werden, wobei *k > 1*, also hat sie die Teiler 1, 2, k und 2k — das heißt, sie hat einen Teiler ungleich 1 und sich selbst, ist also keine Primzahl.

**Bestanden-Kriterien:** Den direkten Beweis, Widerspruchsbeweis und die Induktion erfolgreich auf einfache Beispiele anwenden und erklären, wann welche Strategie angemessen ist.

---

## Forschungsgrundlage

- Der Beweis ist die definierende Methodik der Mathematik seit der antiken griechischen Mathematik
- Direkter Beweis, Widerspruchsbeweis und Induktion decken die große Mehrheit der Beweistechniken im Grundstudium ab
- Häufige Beweisfehler (Zirkelschluss, fehlender Induktionsanfang) sind in der mathematikdidaktischen Forschung gut dokumentiert
- Pädagogisch verbessert das Erlernen von Beweisstrategien vor spezifischen mathematischen Inhalten die langfristige Denkfähigkeit
- Quellen: Konsens der Mathematikdidaktik, Lehrplan des Fachbereichs Mathematik der Streeling-Universität
- Überzeugungszustand: T(0.92) F(0.01) U(0.05) C(0.02)
