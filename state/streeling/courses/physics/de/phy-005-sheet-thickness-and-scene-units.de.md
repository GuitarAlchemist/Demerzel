---
module_id: phy-005-sheet-thickness-and-scene-units
department: physics
course: Materialdicke von IX-Koordinaten in vorgeschlagene Szeneneinheiten umrechnen
level: intermediate
prerequisites: [basic-ratios, dimensional-analysis]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-21-005
version: "0.1.0"
---

# Materialdicke von IX-Koordinaten in vorgeschlagene Szeneneinheiten umrechnen

> **Fachbereich Physik** | 40 Minuten | Vorläufiger deutscher Übersetzungsentwurf; fachliche Prüfung, Prüfung durch eine Person mit fließenden Deutschkenntnissen und Lernversuch stehen aus.

## Lernziele und Projektproblem

Ein Bogen in IX kann Koordinaten zwischen null und eins haben, während seine Materialdicke in Millimetern gemessen wird. Ein vorgeschlagenes Blender- oder Godot-Artefakt benötigt einen weiteren ausdrücklich festgelegten Längenmaßstab. Würde man die bloße Zahl `0.4` durch alle drei Darstellungen übernehmen, würde aus gewöhnlichem Karton ein 150-mal zu dicker Bogen, oder Millimeter würden mit einem Fehler um den Faktor 1000 zu Metern in der Szene.

Nach dieser Lektion können Sie Materialdicke und Stapelhöhen in jeder Darstellung herleiten, die lokale Lagenzahl von den Ebenen paralleler Paneele unterscheiden, zwei Skalierungsfehler erkennen und eine Übergabe formulieren, deren Aussagen durch die vorhandene Evidenz begrenzt sind. Planen Sie ungefähr 12 Minuten für die Herleitungen, 18 Minuten für die Übungen vor dem Aufdecken der Antworten und 10 Minuten für die Transferaufgabe ein. Diese Lektion behandelt geometrische Längen und die Umrechnung von Einheiten. Die Anregungsgeschwindigkeit einer Gitarrensaite gehört zu PHY-004; die Rekonstruktion eines Faltzustands gehört zur Kursfolge im Bereich Visual Computing.

Unsere Quellengrundlage ist IX-Commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [`thickness.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), die zugehörigen [vorhandenen Tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) und [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs). Wir haben diese Definitionen und Zusicherungen im Testcode untersucht. Der koordinierende Agent hat das gezielte Thickness-Testziel am unveränderten, festgelegten IX-HEAD ausgeführt: 11 bestanden, 0 fehlgeschlagen; dies ist kein Ergebnis für die gesamte Testsuite. Das [Rechen-Fixture](../../../fixtures/physics/phy-005/scenarios.json) liefert modellierte Beispiele; Anweisungen zur Reproduktion stehen in seiner [README](../../../fixtures/physics/phy-005/README.md).

## 1. Vor der Umrechnung einer Koordinate einen Maßstab festlegen

Sei `C` die Breite des Bogens in Koordinateneinheiten des Faltmusters, `W` seine angenommene physische Breite in mm und `h` die volle Materialdicke in mm. Definieren Sie `a=W/C` in mm pro Koordinateneinheit. Dann gilt:

```text
x_mm = x_cp × a
t_cp = h/a = h × C/W
H_mm = H_cp × a
```

Der Index kennzeichnet eine Darstellung; er behauptet nicht, dass IX physische Metadaten speichert. Die Breite `W` ist eine externe Annahme für dieses Rechenbeispiel. Eine Datei mit einem Einheitsquadrat allein verrät nicht, ob der reale Bogen 150 mm oder 300 mm breit ist. Mit Dicke ist die volle Dicke gemeint, keine halbe Dicke und keine Anzahl von Flächen.

Der Kranich-Test beschreibt ausdrücklich Karton mit 0.4 mm Dicke auf einem 150 mm breiten Bogen, dessen Faltmuster das Einheitsquadrat ist. Daher gelten `C=1`, `W=150`, `a=150` und `t_cp=0.4/150=0.0026666667`. Die Rückrechnung ergibt `0.0026666667 × 150 ≈ 0.4 mm`. Behalten Sie den Bruch bis zur endgültigen Ausgabe bei, um Rundungsabweichungen zu vermeiden.

`lib.rs` beschreibt die Skalierung von Koordinaten mit Zweierpotenzen vor Prüfungen mit absoluter Toleranz: Das Faltmuster ist danach zwischen einer und zwei Einheiten breit. Das dient der numerischen Konditionierung. Es legt weder Meter als Einheit fest noch misst es den Bogen. `stack(ctx,t)` verwendet das vom Aufrufer gelieferte `t` in seinen ausgegebenen Multiplikationen unverändert; die Funktion kann weder `W` erschließen noch eine übergebene Angabe `0.4 mm` stillschweigend umrechnen. Halten Sie für die Koordinatendarstellung, die Sie weitergeben möchten, eine ausdrückliche externe Zuordnung fest.

### Übung 1: die Eingabe der Materialdicke korrigieren

Eine Übergabe für den Einheitsquadrat-Kranich des Tests beschriftet `t=0.4` mit „0.4 mm“. Berechnen Sie das erforderliche `t_cp`, die durch den falschen Wert dargestellte physische Dicke und den Fehlerfaktor.

> **Antwort:** `t_cp=0.4/150=0.0026666667`. Bei `a=150 mm/cp` bedeuten die irrtümlich eingesetzten `0.4 cp` eine Dicke von `60 mm`. Das Verhältnis zur beabsichtigten Dicke ist `60/0.4=150`. Ersetzen Sie die Zahl und nennen Sie die Zuordnung; eine andere Beschriftung der vorhandenen Zahl führt keine Umrechnung durch.

## 2. Die beiden Stapelauswertungen auseinanderhalten

Die Implementierung berechnet `ply` als die maximale Anzahl von Flächen in einer Überlagerungszelle. Die zugehörige Höhe ist `ply_height=ply × t`. Diese Auswertung erlaubt einer Fläche, in verschiedenen Zellen unterschiedliche Höhen einzunehmen, wie es bei einem sich anschmiegenden Bogen möglich wäre. Sie liefert eine untere Schranke für Stapel, die die angegebenen ebenen Positionen beibehalten.

Bei parallelen starren Paneelen gehören Flächen, die durch flache Gelenke verbunden sind, zu einem gemeinsamen Paneel. Für ein angegebenes überlappendes Paar verbindet eine gerichtete Kante ein unteres mit einem oberen Paneel. Bei azyklischer Ordnung und festgelegter Reihenfolge aller überlappenden Paneelpaare ist `levels` die Länge der längsten Kette und `height=levels × t` die geringstmögliche Höhe unter dieser eingeschränkten Interpretation. Fehlen Ordnungsangaben, ist die gemeldete Ebenenzahl eine untere Schranke; `levels_exact=false`, und `face_levels` fehlt. Eine Anzahl ist dimensionslos, während eine Höhe dieselbe Einheit wie `t` trägt.

Der vorhandene Kranich-Test sichert `ply=28`, exakt `levels=36` für starre Paneele, keine unbestimmten Paare sowie 59 Einträge für Flächenebenen zu, die die angegebene Ordnung einhalten. Er liefert eine Kette aus 36 Flächen. Das sind Zusicherungen über dieses Fixture und diese Interpretation, keine allgemeingültige Kranich-Spezifikation. Wenden Sie beide Formeln an:

```text
Höhe nach lokaler Lagenzahl: 28 × (0.4/150) = 0.0746666667 cp = 11.2 mm
Höhe starrer Paneele:       36 × (0.4/150) = 0.096 cp        = 14.4 mm
```

Bei einer beispielhaften Platzierung mit Unterseiten auf `z_k=k×t` liegt die höchste Unterseite bei 36 belegten Ebenen auf `35t`. Die Oberseite dieser letzten Platte liegt auf `36t`. Das erklärt den Unterschied zwischen einem Flächenversatz und der vollen Stapelausdehnung; es handelt sich um eine vorgeschlagene Zeichenkonvention, nicht um exportierte IX-Geometrie.

### Übung 2: Versatz und Ausdehnung unterscheiden

Die Szenenbeschreibung lautet: „Der Kranich ist 28 Lagen dick, also ist der starre Stapel 11.2 mm hoch; die höchste starre Ebene ist 35, also beträgt seine Höhe 35t.“ Korrigieren Sie beide Aussagen unter den Annahmen des Tests.

> **Antwort:** Die Auswertung mit 28 lokalen Lagen ergibt 11.2 mm. Die Auswertung paralleler starrer Paneele hat 36 exakte Ebenen und die volle Ausdehnung `36×0.4=14.4 mm`. Nach der vorgeschlagenen Unterseitenkonvention beginnt Ebene 35 bei `35×0.4=14.0 mm` und endet bei 14.4 mm. Ein ganzzahliger Ebenenindex ist nicht die Anzahl belegter Ebenen.

## 3. Einen künftigen Szenenmaßstab ausdrücklich herleiten

Angenommen, ein künftiges Artefakt wählt `u=1 scene unit per metre`, also eine Szeneneinheit pro Meter. Das ist eine didaktische Festlegung, keine überprüfte Blender- oder Godot-Konfiguration. Die Umrechnung lautet `b=u/1000` Szeneneinheiten pro mm, also `x_scene=x_cp×a×b`. Wenden Sie denselben Multiplikator auf jede Länge an, die zur selben Geometrie gehört, einschließlich Materialdicke und berechneter Höhen.

Für den Referenzbogen entspricht eine Koordinateneinheit `150/1000=0.15` Szeneneinheiten. Somit ist `t_scene=(0.4/150)×0.15=0.0004`, die Höhe nach lokaler Lagenzahl beträgt `0.0112` und die Höhe starrer Paneele `0.0144`. Der unabhängige Rechenweg über physische Einheiten ergibt `14.4 mm × (1/1000)=0.0144 scene units`, also 0.0144 Szeneneinheiten. Die Übereinstimmung der Rechenwege prüft die Arithmetik, keine Importpipeline.

Wählt eine getrennte didaktische Vorschau stattdessen `u=100 scene units per metre`, also 100 Szeneneinheiten pro Meter, wird jede Szenenlänge 100-mal größer. Die Bogenbreite beträgt dann 15 Szeneneinheiten und die Höhe starrer Paneele 1.44. Die physische Materialdicke bleibt 0.4 mm. Die Wahl des Maßstabs ändert die Darstellung, nicht das Material.

### Übung 3: einen Fehler um den Faktor 1000 finden

Eine vorgeschlagene Szene mit Metermaßstab verwendet die Bogenbreite `0.15`, die Materialdicke `0.4` und die Höhe starrer Paneele `14.4`. Berechnen Sie die beiden korrekten kleineren Längen und zeigen Sie ein Verhältnis, das die Unstimmigkeit unabhängig vom Szenenmaßstab aufdeckt.

> **Antwort:** Die Materialdicke sollte `0.0004` und die Höhe starrer Paneele `0.0144` Szeneneinheiten betragen. Beide angegebenen Werte sind 1000-mal zu groß. Die korrekten Verhältnisse sind `thickness/width=0.4/150≈0.0026666667` für Materialdicke zu Breite und `rigid height/width=14.4/150=0.096` für die Höhe starrer Paneele zu Breite. Die fehlerhafte Szene hat Verhältnisse von ungefähr 2.6667 und 96. Ein konsistenter einheitlicher Maßstab erhält diese dimensionslosen Verhältnisse.

## 4. Jeweils nur eine Annahme ändern

Eine Änderung des Materials und eine Größenänderung der Geometrie beantworten unterschiedliche Fragen. Auf demselben 150 mm breiten Bogen verdoppelt eine Materialdicke von 0.8 mm statt 0.4 mm das `t_cp`, beide Höhen und ihre Szenenlängen. Sie ändert nicht die Flächenordnung der Eingabe. Der vorhandene Test `heights_scale_with_the_thickness` vergleicht `t=0.25` und `0.5`, sichert verdoppelte Höhen zu und prüft unveränderte Flächenebenen. Diese Zahlen prüfen Algebra; sie sind keine Messungen an Karton.

Behält man Material mit 0.4 mm Dicke bei, verwendet aber einen 300 mm breiten Bogen, halbiert sich `t_cp` für eine Darstellung als Einheitsquadrat. Die physischen Höhen bleiben bei derselben angegebenen kombinatorischen Konfiguration 11.2 und 14.4 mm. Verdoppelt man dagegen jede physische Länge einschließlich der Materialdicke, bleibt `t_cp` erhalten, und die physischen Höhen verdoppeln sich. Geben Sie an, welche dieser Transformationen Sie mit „vergrößern“ meinen.

Wird derselbe 150 mm breite Bogen mit `C=2` neu kodiert, ergeben sich `a=75 mm/cp` und `t_cp=0.0053333333`; die Höhe starrer Paneele wird `0.192 cp`. Die Multiplikation mit 75 ergibt wieder 14.4 mm. Das ist eine Herleitung anhand der Einheiten für eine konsistent neu kodierte Darstellung, kein neu beobachteter IX-Lauf.

### Übung 4: drei Änderungen vergleichen

Berechnen Sie ausgehend von der Referenz `t_cp` und die Höhe starrer Paneele in mm für: A, Materialdicke 0.8 mm bei Breite 150 mm und `C=1`; B, Materialdicke 0.4 mm bei Breite 300 mm und `C=1`; C, den ursprünglichen physischen Bogen, dargestellt mit `C=2`. Nehmen Sie dieselbe exakte Ordnung mit 36 Ebenen an.

> **Antwort:** A: `t_cp=0.8/150≈0.0053333333`, Höhe `36×0.8=28.8 mm`. B: `t_cp=0.4/300≈0.0013333333`, Höhe 14.4 mm. C: `t_cp=0.4×2/150≈0.0053333333`, Höhe 14.4 mm. A und C haben dieselbe Koordinatendicke, beschreiben aber unterschiedliche physische Annahmen. Koordinatenwerte benötigen ihren Maßstab.

## 5. Festhalten, was eine umgerechnete Höhe belegt

Der Prüfer liest einen einzelnen angegebenen flach gefalteten Zustand. Laut `lib.rs` beweisen seine lokalen Prüfungen keine globale Flachfaltbarkeit und berechnen keine Lagenordnung. `thickness.rs` beschränkt seine Interpretation starrer Paneele auf parallele Paneele mit jeweils einer einzigen Höhe. Ein Zyklus führt bei positivem `t` zur Zurückweisung dieser Interpretation; bei Dicke null wird er ohne Zurückweisung gemeldet. Eine bei einem Zyklus fehlende Höhe starrer Paneele ist kein gemessener Nullwert.

Auch eine exakte azyklische Höhe beweist nicht, dass eine dicke Faltung physisch realisierbar ist: Reale Gelenke, Kontakt, Biegung und ein Bewegungsablauf liegen außerhalb dieser Berechnung. Der Quellcode weist ausdrücklich darauf hin, dass geneigte Platten einer Zurückweisung für parallele Paneele entgehen können und dass exakter Kontakt dicker Falten eine weitere Einschränkung mit sich bringt. Dieser Kurs erstellt weder Exporter, Mesh, Collider, dynamische Faltsimulation oder Materialprüfung noch eine laufende Blender-/Godot-/DLSS-Integration.

### Übung 5: die Aussage für die Übergabe formulieren

Schreiben Sie für eine Person, die künftig ein visuelles Artefakt erstellt, drei Sätze zum Referenzergebnis: einen über die Evidenz, einen über die Szenenzuordnung und einen über eine ungeklärte physische oder integrationsbezogene Aussage.

> **Antwort:** „Am festgelegten IX-Commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854` geben die untersuchten Zusicherungen des Kranich-Tests für `t=0.4/150` 28 lokale Lagen und 36 exakte Ebenen paralleler Paneele an; der Koordinator meldet außerdem 11 bestandene gezielte Thickness-Tests an dieser unveränderten Revision. Unter der Annahme eines 150 mm breiten Bogens und einer Szeneneinheit pro Meter betragen die hergeleiteten Ausdehnungen nach lokaler Lagenzahl und für starre Paneele 0.0112 und 0.0144 Szeneneinheiten. Diese Umrechnungen belegen weder physische Faltbarkeit noch einen funktionierenden Blender-/Godot-Import.“ Fügen Sie bei der Weitergabe dieser Aussage den Fixture-Link bei.

## Transfer und Prüfung

Bearbeiten Sie die separate [Lernaufgabe ohne Antworten](../../../reviews/phy-005-learner-task.md) mit einer neuen physischen Breite und einem neuen Szenenmaßstab. Eine prüfende Person sollte den festgelegten Quellcode untersuchen, die Umrechnungen nachrechnen und anhand des [Prüfauftrags](../../../reviews/phy-005-review-brief.md) die inhaltliche Übereinstimmung der Sprachfassungen prüfen. Es sind weder ein Lernversuch noch eine Freigabe durch eine Person mit fließenden Sprachkenntnissen oder ein öffentlicher Abruf nach Veröffentlichung dokumentiert. Das hier fertiggestellte Artefakt ist ein Lektionsentwurf mit Rechenmaterial; sein vorgeschlagener Nutzen muss noch durch den selbstständigen Transfer einer tatsächlich lernenden Person geprüft werden.
