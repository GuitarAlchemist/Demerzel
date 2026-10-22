---
module_id: sem-004-face-identity-under-reindexing
department: semiotics
course: "Flächenidentität bei Neuindizierung"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-21-004
version: "0.1.0"
---

# Flächenidentität bei Neuindizierung

> **Fachbereich Semiotik** | Mittelstufe | 40 Minuten | Vorläufiger deutscher Übersetzungsentwurf; fachliche Prüfung, Prüfung durch eine Person mit fließenden Deutschkenntnissen und Lernversuch stehen aus.

## Lernziele und Projektentscheidung

Ein künftiger Szenenbetrachter wählt Fläche 1 eines Origami-Modells aus. Ein zweiter Agent nummeriert das Modell neu und meldet, dass Fläche 1 nun auf einer anderen Ebene liegt. Hat sich das Material bewegt, hat sich die Ordnung geändert, oder bezeichnet dieselbe Zahl jetzt eine andere Fläche? Um diese Frage zu beantworten, muss man zunächst die Zahl deuten, bevor man die Geometrie deutet.

Nach dieser Lektion können Sie eine Auswahl durch eine ausdrücklich angegebene Permutation verfolgen, diese Zuordnung umkehren, Flächenidentität von Ebene und Orientierung unterscheiden und einen Bericht für die Zusammenarbeit zwischen Agenten mit klar begrenzten Aussagen verfassen. Planen Sie acht Minuten für Problem und Zeichen, zwölf für die Tabelle, zehn für Transformationen und zehn für Übungen und Transfer ein. Das Artefakt ist eine kleine Zuordnungstabelle mit einer begründbaren Übergabe, kein neuer Identitätsdienst.

Die Projektevidenz stammt aus IX-Commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), [Thickness-Tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) und [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). Diese Links legen den untersuchten Quellstand fest, nicht den aktuellen Branch. IX stellt hier Prüfungen und kontrollierte Transformationen bereit; diese Lektion demonstriert weder einen Blender-Export oder Godot-Import noch einen Renderer oder eine Implementierung dauerhaft erhaltener Auswahlzustände.

## 1. Eine Flächennummer ist ein kontextabhängiges Zeichen

In der Semiotik steht ein Zeichen unter einer bestimmten Interpretation für ein Objekt. Hier ist `1` das Zeichen, eine bestimmte materielle Fläche das gemeinte Objekt und „Eintrag 1 in dieser Modellrevision nachschlagen“ die Interpretation. Ein Array-**Index** ist eine Adresse innerhalb einer geordneten Sammlung im Programm. Er darf nicht mit dem allgemeineren semiotischen Begriff *Index* verwechselt werden, einem Zeichen, das mit dem verbunden ist, worauf es verweist. Keine der beiden Wortbedeutungen verleiht der Zahl eine dauerhafte Identität.

Ein Bericht benötigt seine Modellrevision oder den Kontext der Transformation. „Fläche 1“ in der Eingabe und „Fläche 1“ in der Ausgabe sind zwei möglicherweise unterschiedliche Verweise. Form, Farbe und aktuelle Stapelebene können einem Menschen helfen, eine Fläche wiederzuerkennen; diese Eigenschaften können aber bei mehreren Flächen gleich sein oder sich unter einer Transformation ändern. Für sich genommen belegen sie keine Herkunft.

In dieser Lektion bedeutet **materielle Identität** die Zuordnung zur selben Eingabefläche durch die jeweilige kontrollierte Transformation. Sie löst nicht das allgemeine Problem beliebiger Neuvernetzung, Teilung, Zusammenführung oder Rekonstruktion eines Modells aus einem Bild. Eine Herkunftskennzeichnung wie das Unterrichtslabel A hält die von uns vorgegebene Zuordnung fest. Solche Kennzeichnungen sind ausdrücklich synthetisch; die untersuchte IX-`Permutation` ist eine Zuordnung für eine Transformation, kein universelles Register dauerhafter IDs.

### Übung 1 — einen Verweis berichtigen

Ein Agent sagt: „Fläche 1 stimmt nach der Neunummerierung nicht.“ Welche Angaben fehlen? Formulieren Sie daraus eine überprüfbare Frage.

> **Antwort:** Es fehlen der Kontext von Eingabe- und Ausgabemodell, die Zuordnungstabelle und die verglichene Eigenschaft. Eine brauchbare Frage lautet: „Behält bei der synthetischen Eingabefläche 1 (B) und der Alt-zu-neu-Zuordnung `[2,0,3,1]` die Ausgabefläche 0 die Eingabeebene 2 bei?“ Damit werden das gemeinte Material und der genaue Vergleich benannt; ein IX-Fehler wird damit nicht behauptet.

## 2. Die Zuordnung in ihrer angegebenen Richtung anwenden

`Permutation` dokumentiert, wohin jeder **alte** Index verschoben wurde. Die Hilfsfunktion `place` schreibt ein altes Element nach `out[perm[old]]`. Daher nimmt `perm.faces[f]` einen Eingabeflächenindex an und gibt den zugehörigen Ausgabeflächenindex zurück. Daraus geht nicht hervor, welche Eingabefläche jetzt einen beliebigen Ausgabeeintrag belegt; dafür braucht man die inverse Zuordnung.

Verwenden Sie dieses ausdrücklich **synthetische** Beispiel mit vier Flächen, das auch im [Fixture](../../../fixtures/semiotics/sem-004/scenarios.json) festgehalten ist. Seine Zahlen sind weder Kranich-Ergebnisse noch eine gezogene Seed-Stichprobe oder ein physisches Experiment zur Materialdicke.

| Eingabeindex | Herkunftslabel im Unterricht | Eingabeebene | Ausgabeindex `p[old]` |
|---:|---|---:|---:|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 0 |
| 2 | C | 1 | 3 |
| 3 | D | 3 | 1 |

Die Vorwärtszuordnung lautet `p = [2,0,3,1]`. Liest man die Ausgabeeinträge von 0 bis 3, erhält man die Labels `[B,D,A,C]` und die Ebenen `[2,3,0,1]`. Die inverse Zuordnung lautet `q = [1,3,0,2]`: Ausgabeeintrag 0 stammt von Eingabeeintrag 1, Ausgabeeintrag 1 von Eingabeeintrag 3. Prüfen Sie beide Richtungen: `q[p[f]] = f` und `p[q[j]] = j`.

Der korrekte Eigenschaftsvergleich lautet `new[p[f]] == old[f]`. Für Eingabe B ist das `new[0] == old[1]`, also `2 == 2`. Ein direkter Vergleich der Arrays ergibt Ungleichheit, obwohl jedes materielle Element seinen Wert behält. Wird die ausgewählte Ganzzahl 1 einfach wiederverwendet, wird stattdessen D hervorgehoben, dessen Ebene 3 ist. Das ist ein Auswahlfehler, ohne dass die Ebenenberechnung beschädigt wäre.

Die inverse Zuordnung ist ebenso nützlich, wenn jemand auf Ausgabeeintrag 3 klickt: Sie identifiziert die Eingabe C an Eintrag 2. `new[q[f]]` im Vorwärtsvergleich zu schreiben, vermischt die Definitionsbereiche. Bei unserer absichtlich nicht selbstinversen Zuordnung würde Eingabe 0 dann `new[1] = 3` mit `old[0] = 0` vergleichen. Ein Beispiel, das nur aus einer Vertauschung besteht, kann diesen Fehler verdecken, weil eine Vertauschung ihrer eigenen inversen Abbildung entspricht.

### Übung 2 — die Auswahl mitführen

Übertragen Sie die Eingabeauswahl C durch die Zuordnung. Verfolgen Sie anschließend einen Klick auf Ausgabeeintrag 1 zur Eingabe zurück. Würde das Beibehalten der Ganzzahl 2 die ursprüngliche Auswahl C erhalten?

> **Antwort:** C ist Eingabe 2, daher ist sein Ausgabeindex `p[2] = 3`; Ebene 1 bleibt erhalten. Ausgabe 1 stammt von `q[1] = 3`, dem Label D. Das Beibehalten der Ganzzahl 2 würde in der Ausgabe A auswählen. Die Zuordnung ändert die Adresse und erhält dabei die von uns festgelegte materielle Entsprechung.

### Übung 3 — die richtigen Objekte vergleichen

Finden Sie die erste Abweichung bei einem direkten Vergleich von `[0,2,1,3]` und `[2,3,0,1]`. Geben Sie die vier Vergleiche mit Zuordnung an und prüfen Sie eine Gleichung der inversen Abbildung.

> **Antwort:** Der direkte Vergleich weicht schon bei Eintrag 0 ab: `0 != 2`. Die Prüfungen mit Zuordnung lauten `new[2]=0`, `new[0]=2`, `new[3]=1` und `new[1]=3`; sie stimmen jeweils mit den Eingabeeinträgen 0–3 überein. Zum Beispiel gilt `q[p[2]] = q[3] = 2`. Die direkte Ungleichheit widerlegt die behauptete Entsprechung nicht.

## 3. Beziehungen erhalten, ohne ihre Zeichen zu verwechseln

Die Neunummerierung ordnet auch Eckpunkte und Kanten neu zu. Sie rotiert die Eckpunktliste jeder Fläche zyklisch und erhält dabei deren Umlaufrichtung; sie kann die Endpunkte einer Kante vertauschen und die Folge der `faceOrders`-Einträge durchmischen. Das sind unterschiedliche Operationen. Die Rotation eines Dreiecksrandes von `[0,1,2]` zu `[1,2,0]` ändert seinen Startpunkt. Die Umkehrung zu `[0,2,1]` ändert die Umlaufrichtung und ist nicht dieselbe Operation. Diese winzigen Randlisten veranschaulichen Ordnungskonventionen; sie sind keine aus IX extrahierte Geometrie.

In jedem `faceOrders`-Tripel `[f,g,s]` setzt `renumber` die Werte `[p[f],p[g],s]` ein und behält das Vorzeichen bei. Unser synthetisches Tripel `[1,3,1]` wird zu `[0,1,1]`. Das Vorzeichen wird relativ zu den Flächennormalen interpretiert; ohne Orientierung darf es nicht zu einer uneingeschränkten globalen Kennzeichnung „oben“ erhoben werden. Auch das Durchmischen der Beziehungssammlung kehrt nicht jede Beziehung um. Eine Listenposition, eine Endpunktposition, eine Randrichtung und ein Vorzeichen der Lagenordnung haben unterschiedliche Bedeutungen.

Im festgelegten Thickness-Test führt `controls_leave_the_stack_unchanged` die Neunummerierung mit den Seeds 1–5 am Kranich aus. Der Test prüft die lokale Lagenzahl 28, die Zahl der Ebenen starrer Paneele 36 und für jede Eingabefläche `new[perm.faces[f]] == old[f]`. Das ist konkrete Evidenz für diese Transformationen an diesem Fixture. Es ist kein umfassender Satz für jede Faltung oder Transformation.

`face_levels` ist eine mögliche Stapelzuordnung, die die angegebenen Paare einhält und bei Ebene null beginnt. Die Implementierung kann bei einem Zyklus oder unzureichenden Ordnungsinformationen keine Ebenen pro Fläche zurückgeben. Eine Ebene ist daher weder eine eindeutige Kennung materieller Identität noch eine kanonische Beschreibung jedes zulässigen Stapels. Zwei Flächen können dieselbe Ebene teilen. Übereinstimmende Gesamtzahlen allein sagen einem Koordinator nicht, ob eine Auswahl weiterhin auf die beabsichtigte Fläche verweist.

### Übung 4 — drei Ordnungsoperationen unterscheiden

Eine prüfende Person bezeichnet einen rotierten Flächenrand, durchmischte `faceOrders`-Einträge und ein umgedrehtes Modell gleichermaßen als „Umordnung von Arrays“. Erklären Sie, warum diese Beschreibung relevante Bedeutung verliert. Bilden Sie das synthetische Tripel `[1,3,1]` ab.

> **Antwort:** Eine Randrotation erhält die zyklische Umlaufrichtung; das Durchmischen der Beziehungsliste ändert die Aufzählungsreihenfolge und erhält jede einzelne Beziehung; das Umdrehen ändert die Orientierung und die Bedeutung von „oben“. Dafür sind unterschiedliche Prüfungen nötig. Das Tripel wird zu `[0,1,1]`: Seine Flächenverweise werden durch p abgebildet, sein relatives Vorzeichen bleibt erhalten. Das allein belegt keine globale Oben-Beziehung.

## 4. Die Transformation und die Grenzen ihrer Evidenz benennen

`move_folded` rotiert das gefaltete Bezugssystem in seiner Ebene und verschiebt es anschließend; die Orientierungen bleiben erhalten. Der festgelegte Test verwendet den Winkel 0.7 Radiant und die Verschiebung `[3,-2]` und sichert zu, dass der gesamte zurückgegebene Stapel mit der Ausgangsbasis übereinstimmt. Diese Beobachtung stützt diese getestete starre Bewegung, keine beliebige Skalierung, Verformung oder Neuvernetzung.

`turn_over` spiegelt die gefalteten y-Koordinaten mit `y -> -y`. Laut Dokumentation kehren sich sowohl die Orientierungen als auch „oben“ um, sodass `faceOrders`, relativ zu den Flächennormalen, unverändert bleibt. Der Thickness-Test prüft gleiche lokale Lagenzahl, Höhe nach lokaler Lagenzahl, Ebenenzahl starrer Paneele und Höhe starrer Paneele. Er sichert ausdrücklich **nicht** zu, welche Fläche welche Ebene belegt. Nach dem Umdrehen unveränderte Ebenen pro Fläche zu melden, würde über die Evidenz hinausgehen. Materielle Entsprechung und vertikale Ordnung sind getrennte Fragen.

Eine brauchbare Übergabe nennt Quellrevision, Transformation, Zuordnungsrichtung, ausgewählte Eingabe- und Ausgabeindizes, verglichene Eigenschaft und Ergebnis. Ist die Entsprechung nach einer beliebigen Neugenerierung nicht verfügbar, melden Sie die Identität als ungeklärt. Identische Gesamtdicke oder eine vertraute Silhouette können die fehlende Zuordnung nicht ersetzen. Das ist eine Kommunikationsanforderung für den vorgeschlagenen Arbeitsablauf, kein implementiertes IX-Auswahlprotokoll.

### Übung 5 — einen widerlegbaren Auswahlversuch entwerfen

Schlagen Sie einen künftigen Godot-Versuch vor, der den korrekten Erhalt einer Auswahl nach dieser synthetischen Neunummerierung widerlegen könnte. Fügen Sie eine Aussage zum Umdrehen hinzu, die der vorhandene Quellcode nicht rechtfertigt.

> **Antwort:** Wählen Sie vor der Transformation B an Eingabe 1 aus und halten Sie Herkunftslabel aus dem Unterricht, Modellrevision und Zuordnung fest. Verlangen Sie nach der Anwendung von p, dass Hervorhebung und Bericht Ausgabe 0, B, Ebene 2 nennen. Eine Hervorhebung von Ausgabe 1/D widerlegt den Auswahlerhalt auch dann, wenn die Gesamtzahl der Ebenen stimmt. Zeichnen Sie die rohen Auswahlereignisse auf und erstellen Sie Screenshots vor und nach der Transformation; hier wurde noch kein Versuch durchgeführt. „B behält nach dem Umdrehen dieselbe Ebene“ wird durch die festgelegten Zusicherungen zum Umdrehen, die nur Gesamtwerte betreffen, nicht gestützt.

Der vorgeschlagene Versuch benötigt einen tatsächlichen Szenenadapter und eine unabhängige Beobachtung, bevor jemand eine erfolgreiche Integration behaupten kann. Die vorliegenden Ergebnisse sind Quellcodeanalyse, eine synthetische Tabelle und vorbereitete Lernaufgaben. Fachliche Prüfung durch einen Menschen, ein Lernversuch, Prüfung durch eine Person mit fließenden Sprachkenntnissen und öffentliche Veröffentlichung stehen weiterhin aus.
