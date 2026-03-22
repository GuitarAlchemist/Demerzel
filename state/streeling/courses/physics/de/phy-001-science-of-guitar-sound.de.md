---
module_id: phy-001-science-of-guitar-sound
department: physics
course: "Akustik und Wellenphysik"
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: physics
version: "1.0.0"
---

# Die Physik des Gitarrenklangs

> **Fachbereich Physik** | Stufe: Nigredo (Einführung) | Dauer: 25 Minuten

## Lernziele

Nach dieser Lektion werden Sie in der Lage sein:
- Zu erklären, wie eine Gitarrensaite schwingt und Klang erzeugt (stehende Wellen)
- Die Obertonreihe zu beschreiben und warum sie jedem Instrument seine einzigartige Klangfarbe verleiht
- Zu verstehen, wie der Gitarrenkorpus den Klang durch Resonanz verstärkt
- Die Bundplatzierung mit Frequenzverhältnissen mithilfe einfacher Physik in Verbindung zu bringen

---

## 1. Saitenschwingung — Stehende Wellen

Wenn Sie eine Gitarrensaite anschlagen, schwingt sie nicht einfach zufällig. Sie schwingt in einem sehr bestimmten Muster, einer sogenannten **stehenden Welle**.

Eine stehende Welle entsteht, wenn eine Welle zwischen zwei festen Endpunkten hin und her reflektiert wird — in diesem Fall dem Sattel und dem Steg (oder einem Bund und dem Steg). Die reflektierten Wellen interferieren miteinander, und nur bestimmte Schwingungsmuster überleben. Diese überlebenden Muster sind diejenigen, bei denen die Saitenlänge einer exakten Anzahl halber Wellenlängen entspricht.

Die **Grundfrequenz** ist das einfachste Muster: Die gesamte Saite schwingt als ein Bogen hin und her, mit maximaler Auslenkung in der Mitte und null Auslenkung an den Endpunkten (den sogenannten **Knoten**).

Die Grundfrequenz hängt von drei Dingen ab:

```
f = (1 / 2L) * sqrt(T / mu)
```

Wobei:
- **L** = schwingende Länge der Saite
- **T** = Spannung (wie straff die Saite gespannt ist)
- **mu** = Längenbezogene Masse (Masse pro Längeneinheit — dickere Saiten haben mehr)

Diese Formel erklärt alles über das Verhalten von Gitarrensaiten:
- **Kürzere Saite** (Bund drücken) → höherer Ton
- **Straffere Saite** (höher stimmen) → höherer Ton
- **Dickere Saite** (tiefes E vs. hohes E) → tieferer Ton

### Übung

Probieren Sie dies auf Ihrer Gitarre: Schlagen Sie eine Leersaite an, dann drücken Sie die gleiche Saite am 12. Bund und schlagen Sie erneut an. Der 12. Bund halbiert die Saitenlänge (L wird L/2), was die Frequenz verdoppelt — Sie hören genau eine Oktave höher. Vergleichen Sie nun die leere tiefe E-Saite (dick) mit der leeren hohen E-Saite (dünn). Gleicher Notenname, zwei Oktaven Unterschied — der Unterschied liegt in der Massendichte (mu).

---

## 2. Die Obertonreihe — Warum eine Gitarre wie eine Gitarre klingt

Wenn Sie eine Saite anschlagen, schwingt sie nicht nur bei der Grundfrequenz. Sie schwingt gleichzeitig bei **allen ganzzahligen Vielfachen** der Grundfrequenz. Diese sind die **Obertöne** (auch **Harmonische** oder **Teiltöne** genannt).

| Oberton | Frequenz | Musikalisches Intervall | Knoten auf der Saite |
|---------|----------|------------------------|---------------------|
| 1. (Grundton) | f | Grundton | 2 (nur Endpunkte) |
| 2. | 2f | Oktave | 3 |
| 3. | 3f | Oktave + reine Quinte | 4 |
| 4. | 4f | Zwei Oktaven | 5 |
| 5. | 5f | Zwei Oktaven + große Terz | 6 |
| 6. | 6f | Zwei Oktaven + reine Quinte | 7 |

Der Klang, den Sie hören, ist **all diese Frequenzen zusammen**. Ihr Ohr nimmt den Grundton als „die Tonhöhe" wahr, aber die relative Lautstärke jedes Obertons formt die **Klangfarbe** (Timbre) — die Tonqualität, die eine Gitarre anders klingen lässt als ein Klavier, selbst wenn sie den gleichen Ton spielen.

Deshalb klingt eine Gitarre wie eine Gitarre: Ihr Saitenmaterial, ihre Korpusform und die Anschlagposition erzeugen ein bestimmtes Obertonrezept. Schlagen Sie nahe am Steg an und betonen Sie höhere Obertöne (hell, metallisch). Schlagen Sie nahe am Hals an und unterdrücken Sie diese (warm, weich).

### Übung

Sie können einzelne Obertöne auf der Gitarre isolieren. Berühren Sie die Saite leicht direkt über dem 12. Bund (nicht herunterdrücken — nur berühren) und schlagen Sie an. Sie hören den 2. Oberton: einen klaren, glockenartigen Ton eine Oktave über der Leersaite. Versuchen Sie dasselbe am 7. Bund (3. Oberton — eine Oktave plus eine Quinte darüber) und am 5. Bund (4. Oberton — zwei Oktaven darüber). Sie zwingen die Saite, in bestimmten Mustern zu schwingen, indem Sie mit Ihrer Fingerspitze einen Knoten erzeugen.

---

## 3. Resonanz — Wie der Korpus den Klang verstärkt

Eine schwingende Saite allein ist nahezu unhörbar. Halten Sie eine unverstärkte E-Gitarre und schlagen Sie an — Sie können sie kaum quer durch einen Raum hören. Die Saite braucht Hilfe, um genügend Luft zu bewegen, damit der Klang Ihre Ohren erreicht.

Diese Hilfe kommt durch **Resonanz**. Wenn Sie eine Saite auf einer akustischen Gitarre anschlagen:

1. Die Saite schwingt bei ihrem Grundton und den Obertönen
2. Die Schwingung wandert durch den Steg in die **Brücke**
3. Die Brücke ist auf die **Decke** (Resonanzboden) des Gitarrenkorpus geleimt
4. Die Decke ist eine große, dünne, flexible Fläche, die mitschwingt — sie ist der Lautsprecher der akustischen Gitarre
5. Die schwingende Decke bewegt Luft innerhalb des Korpushohlraums, der durch das **Schallloch** resoniert

Der Korpus wirkt als **Resonanzhohlraum**. Er hat seine eigenen Eigenfrequenzen, bestimmt durch Form, Größe und Material. Wenn die Frequenzen der Saite mit den Resonanzfrequenzen des Korpus übereinstimmen, werden diese Frequenzen stärker verstärkt.

Deshalb klingen verschiedene Gitarren unterschiedlich, selbst mit den gleichen Saiten. Ein Dreadnought-Korpus (groß, breit) betont tiefe Frequenzen. Eine Parlor-Gitarre (kleiner Korpus) klingt heller. Holzart, Beleistung und Korpustiefe stimmen alle das Resonanzprofil ab.

**Zentrales Konzept:** Resonanz bedeutet nicht „alles gleichmäßig lauter machen." Es ist **selektive Verstärkung** — bestimmte Frequenzen werden stärker angehoben als andere, was die einzigartige Stimme der Gitarre formt.

### Übung

Falls Sie eine akustische Gitarre haben, versuchen Sie dies: Drücken Sie Ihr Ohr an die Rückseite des Korpus, während jemand anderes eine einzelne Saite anschlägt. Sie werden spüren, wie der gesamte Korpus schwingt. Klopfen Sie nun sanft an verschiedenen Stellen auf die Decke — Sie werden verschiedene Tonhöhen hören. Das sind die Eigenresonanzfrequenzen des Korpus. Jede Gitarre ist eine Zusammenarbeit zwischen Saite und Korpus.

---

## 4. Bünde und Frequenzverhältnisse

Hier trifft Physik am direktesten auf Musiktheorie. Die Bünde auf einer Gitarre sind nicht in gleichen Abständen gesetzt — sie rücken näher zusammen, je weiter man zum Korpus kommt. Warum?

Jeder Bund erhöht die Tonhöhe um einen Halbton. In der **gleichstufigen Temperatur** (dem Standard-Stimmsystem) multipliziert jeder Halbton die Frequenz mit dem gleichen Verhältnis:

```
r = 2^(1/12) ≈ 1,05946
```

Das bedeutet, jeder Bund verkürzt die schwingende Saite um den Faktor *r*. Da die Bünde auf einer geometrischen (nicht arithmetischen) Progression basieren, nimmt der Abstand ab, je höher man geht.

Einige musikalisch wichtige Bundpositionen und ihre Frequenzverhältnisse:

| Bund | Frequenzverhältnis | Musikalisches Intervall | Saitenlängenanteil |
|------|-------------------|------------------------|-------------------|
| 0 (offen) | 1:1 | Prime | 1 |
| 5 | 2^(5/12) ≈ 1,335 | Reine Quarte | ~3/4 |
| 7 | 2^(7/12) ≈ 1,498 | Reine Quinte | ~2/3 |
| 12 | 2^(12/12) = 2 | Oktave | 1/2 |

Beachten Sie die reine Quinte bei Bund 7: Das Frequenzverhältnis ist sehr nah an 3/2 (1,5). Die reine Quarte bei Bund 5 liegt nah an 4/3 (1,333). Diese einfachen Verhältnisse sind der Grund, warum diese Intervalle konsonant klingen — die gleiche Physik, die die Obertonreihe bestimmt, bestimmt auch die Intervalle, die wir als angenehm empfinden.

Die gleichstufige Temperatur passt diese Verhältnisse leicht an, damit alle Tonarten gleich gut klingen — ein Kompromiss. In reiner (natürlicher) Stimmung wäre eine reine Quinte exakt 3/2, aber dann würden manche Tonarten schrecklich klingen. Die festen Bünde der Gitarre legen sie auf die gleichstufige Temperatur fest.

*Historische Anmerkung: Die mathematischen Grundlagen der gleichstufigen Temperatur wurden unter anderem von dem deutschen Organisten und Musiktheoretiker Andreas Werckmeister im 17. Jahrhundert weiterentwickelt. Das Wohltemperierte Klavier von J. S. Bach demonstrierte die praktische Anwendung dieser Stimmungskompromisse.*

### Übung

Messen Sie den Abstand vom Sattel zum 12. Bund auf Ihrer Gitarre, dann messen Sie vom 12. Bund zum Steg. Sie sollten fast exakt gleich sein — was bestätigt, dass der 12. Bund die Saitenlänge halbiert und die Frequenz verdoppelt (eine Oktave). Messen Sie nun Sattel bis Bund 7: Es sollte ungefähr 2/3 der Gesamtsaitenlänge sein, passend zum 3:2-Verhältnis einer reinen Quinte.

---

## 5. Alles zusammen

Jeder Klang, den Sie von einer Gitarre hören, ist das Ergebnis dieser vier physikalischen Konzepte im Zusammenspiel:

1. **Stehende Wellen** bestimmen, welche Frequenzen die Saite erzeugen kann
2. **Die Obertonreihe** formt die Klangfarbe durch Mischung mehrerer gleichzeitiger Frequenzen
3. **Resonanz** im Korpus verstärkt diese Frequenzen selektiv auf hörbare Lautstärke
4. **Frequenzverhältnisse** aus der gleichstufigen Temperatur bestimmen die musikalischen Intervalle zwischen gegriffenen Tönen

Wenn Sie einen Akkord spielen, erzeugt jede Saite ihren eigenen Grundton und ihre Obertöne. Der Korpus resoniert mit allen gleichzeitig. Ihr Ohr empfängt eine komplexe Welle mit Dutzenden von Frequenzen und nimmt sie irgendwie als „einen C-Dur-Akkord" wahr. Die Physik ist außergewöhnlich. Dass Menschen sie als Musik wahrnehmen, ist noch erstaunlicher.

---

## Schlüsselbegriffe

| Begriff | Definition |
|---------|-----------|
| **Stehende Welle** | Ein Schwingungsmuster, das stationär bleibt, mit festen Knoten und Schwingungsbäuchen |
| **Grundfrequenz** | Die niedrigste Frequenz, bei der eine Saite schwingt — wird als Tonhöhe wahrgenommen |
| **Oberton (Harmonische)** | Ein ganzzahliges Vielfaches der Grundfrequenz |
| **Klangfarbe (Timbre)** | Die Tonqualität, die ein Instrument von einem anderen unterscheidet, wenn sie den gleichen Ton spielen |
| **Knoten** | Ein Punkt auf einer stehenden Welle, der stationär bleibt (null Auslenkung) |
| **Resonanz** | Die Verstärkung von Klang, wenn ein schwingender Körper einen anderen Körper bei dessen Eigenfrequenz anregt |
| **Gleichstufige Temperatur** | Stimmsystem, bei dem jeder Halbton ein gleiches Frequenzverhältnis von 2^(1/12) hat |

---

## Selbstüberprüfung

**1. Welche drei physikalischen Eigenschaften einer Saite bestimmen ihre Grundfrequenz?**
> Länge (L), Spannung (T) und längenbezogene Masse (mu). Die Formel lautet f = (1/2L) * sqrt(T/mu).

**2. Warum klingt eine Gitarre anders als ein Klavier, das den gleichen Ton in gleicher Lautstärke spielt?**
> Sie haben unterschiedliche Obertonprofile — die relative Lautstärke jedes Obertons unterscheidet sich, was eine andere Klangfarbe erzeugt. Der Gitarrenkorpus, das Saitenmaterial und die Anschlagmethode erzeugen ein einzigartiges Obertonrezept.

**3. Was passiert, wenn Sie eine Saite am 12. Bund leicht berühren und anschlagen?**
> Sie erzeugen einen Knoten am Mittelpunkt und zwingen die Saite, in ihrem 2. Oberton zu schwingen. Der Grundton wird unterdrückt, und Sie hören einen reinen Ton eine Oktave höher.

**4. Warum rücken die Bünde näher zusammen, je weiter man den Hals hinaufgeht?**
> Die Bundabstände folgen einer geometrischen Progression (jeder Bund multipliziert die Frequenz mit 2^(1/12)). Da jeder Bund einen konstanten Bruchteil der verbleibenden Saitenlänge entfernt statt einer konstanten Strecke, nimmt der Abstand ab.

**Bestanden-Kriterien:** Erklären, wie stehende Wellen Gitarrenklang erzeugen, mindestens drei Obertöne der Reihe identifizieren und die Bundposition mit dem Frequenzverhältnis in Verbindung bringen.

---

## Forschungsgrundlage

- Saitenschwingung folgt der Wellengleichung; stehende Wellen sind deren Randwert-Lösungen
- Die Obertonreihe ist eine direkte Konsequenz der Physik schwingender Saiten
- Gitarrenkorpus-Resonanz ist umfassend mittels Modalanalyse untersucht worden
- Die gleichstufige Temperatur verwendet 2^(1/12)-Abstufung, ein mathematischer Kompromiss, der vom 16. bis 18. Jahrhundert formalisiert wurde
- Quellen: Konsens in Akustik und Wellenphysik, Lehrplan des Fachbereichs Physik der Streeling-Universität
- Überzeugungszustand: T(0.93) F(0.01) U(0.04) C(0.02)
