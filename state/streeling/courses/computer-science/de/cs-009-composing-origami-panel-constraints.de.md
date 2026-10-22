---
module_id: cs-009-composing-origami-panel-constraints
department: computer-science
course: "Origami-Bedingungen zusammenführen, bevor ein starrer Stapel akzeptiert wird"
level: intermediate
prerequisites: [cs-001-thinking-algorithmically, cs-006-ixql-pipeline-composition]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-21-009
version: "0.1.0"
---

# Origami-Bedingungen zusammenführen, bevor ein starrer Stapel akzeptiert wird

> **Fachbereich Informatik** | Mittelstufe | 40 Minuten | Vorläufiger deutscher Übersetzungsentwurf; fachliche Prüfung, Prüfung durch eine Person mit fließenden Deutschkenntnissen und Lernversuch stehen aus.

## Lernziele und Projektfrage

Sie werden flache Gelenke in Äquivalenzklassen überführen, gerichtete Bedingungen zwischen diesen Klassen erhalten, lokale Überlappungsprüfungen von einer globalen Stapelbedingung unterscheiden und ein unvollständiges Ergebnis lesen, ohne eine Platzierung zu erfinden. Die praktische Frage lautet: **Welches Ergebnis darf ein Agent an einen künftigen Blender- oder Godot-Adapter weitergeben, nachdem IX einen Origami-Zustand geprüft hat?** Ein sichtbares Bastelobjekt benötigt eine ausdrücklich benannte Interpretation der Analyse, weil eine erfolgreiche Prüfung mit einer Zurückweisung unter einem anderen Modell vereinbar sein kann.

Die Fallstudie behandelt das implementierte [IX-Modul zur Materialdicke](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) und seine [Integrationstests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), beide festgelegt auf `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. Das Modul liest eine Materialdicke in den Koordinateneinheiten des Faltmusters ein. Es untersucht einen einzelnen angegebenen flach gefalteten Zustand; es plant weder eine Faltbewegung noch exportiert es eine Szene. Das [Kurs-Fixture](../../../fixtures/computer-science/cs-009/README.md) enthält kleine Herleitungen an Graphen, die klar von den tatsächlichen Rust-Testergebnissen getrennt sind.

## 1. Zuerst Flächen zu Paneelen zusammenfassen

Eine Fläche ist ein Polygon in der Beschreibung des gefalteten Zustands. Ein Paneel ist in diesem Modell eine Menge von Flächen, die durch flache Gelenke verbunden sind und dieselbe Höhe beibehalten müssen. Die Funktion `panels` der Implementierung vereinigt ihre Mengen und bildet jede Fläche auf die Fläche mit dem kleinsten Index in ihrer Zusammenhangskomponente ab. Dieser Repräsentant ist eine algorithmische Kennzeichnung. Er ist keine dauerhafte Objektkennung; eine Neunummerierung der Eingabe kann ihn ändern, obwohl das dargestellte Paneel erhalten bleibt.

Betrachten Sie die Flächen 0, 1 und 2. Die Flächen 0 und 1 haben ein gemeinsames flaches Gelenk. Die angegebenen Beziehungen setzen 2 über 0 und 1 über 2. Im Flächengraphen lauten die gerichteten Kanten von unten nach oben `0 → 2 → 1`; er enthält keinen Zyklus. Weist man jeder Fläche eine eigene Höhe zu, scheinen die Ebenen 0, 1 und 2 die Antwort zu sein. Das verletzt das Modell: Die Flächen 0 und 1 gehören zu einem starren Paneel und dürfen keine unterschiedlichen Höhen einnehmen.

Nach der Vereinigung der durch flache Gelenke verbundenen Flächen lautet die Paneelzuordnung `[0, 0, 2]`. Aus den beiden Bedingungen werden `panel 0 → panel 2` und `panel 2 → panel 0`, also eine Kante von Paneel 0 zu Paneel 2 und eine in Gegenrichtung. Jetzt ist der Zyklus sichtbar. Das ist eine Quotientenkonstruktion: Zuerst werden Objekte gruppiert, die sich gemeinsam bewegen müssen, dann werden die Ordnungsbedingungen auf diese Gruppen angewandt. Wer die Teile vor ihrer Zusammenführung einzeln prüft, übersieht die Anforderung, die durch ihre gemeinsame Identität entsteht.

### Übung 1: den irreführenden Graphen korrigieren

Verwenden Sie das Fixture `pierced-flat-joint`. Geben Sie die Paneelrepräsentanten und die beiden gerichteten Paneelkanten an. Erklären Sie, warum die topologische Ordnung des Flächengraphen keine starre Platzierung rechtfertigen kann. Welche zusätzliche Implementierungsentscheidung wäre nötig, wenn ein Adapter eine dauerhafte Paneel-ID verwenden wollte?

> **Antwort:** Die Repräsentanten sind `[0, 0, 2]`; die gerichteten Kanten lauten `0 → 2` und `2 → 0`. Die Flächenordnung erlaubt zwei unterschiedliche Höhen für dasselbe durch flache Gelenke verbundene Paneel und löst damit das falsche Bedingungssystem. Eine dauerhafte Paneel-ID benötigte eine festgelegte Rückzuordnung zur Material- oder Quellidentität über Bearbeitungen oder Permutationen hinweg. Der Repräsentant mit dem kleinsten Index allein bietet diese Garantie nicht.

## 2. Lokaler Erfolg ist mit globaler Zurückweisung vereinbar

Der festgelegte Test `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` konstruiert vier Streifen. Jeder überlappt den nächsten an einer anderen Ecke. Jede lokale Überlagerungszelle kann eine konsistente Ordnung haben; gemeinsam besagen die Angaben jedoch, dass Streifen 0 über 1, 1 über 2, 2 über 3 und 3 über 0 liegt. Mit gerichteten Kanten von unten nach oben ergibt sich `0 → 3 → 2 → 1 → 0`. Bei positiver Materialdicke erfüllt keine einzelne Höhe pro Streifen alle vier Ungleichungen.

Das unterscheidet sich von [VC-007](../../visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), dessen synthetischer Prüfer eine an wiederholten Kachelgrenzen neu beginnende Parität erkennt. Hier geht es um einen Zyklus über verschiedene Überlappungsbereiche hinweg in der vorhandenen IX-Implementierung. Eine Textur, eine Vorschau einer lokalen Kreuzung oder eine erfolgreiche Origami-Basisanalyse kann die globale Frage nach parallelen Paneelen nicht entscheiden.

Der Test sichert zu, dass `analyse(&weave()).unwrap().ok` wahr ist. Er prüft außerdem die optionale Auswertung der Materialdicke bei `t = 0`, einem winzigen positiven `t` und `t = 0.5`. Der Graph bleibt zyklisch, aber `rigid.refused` ist nur bei positivem `t` wahr. Bei null gibt die Implementierung für diese zyklische Auswertung weiterhin `levels`, `height` und `face_levels` als fehlend zurück. Ersetzen Sie eine fehlende Höhe starrer Paneele nicht durch null, nur weil das getrennte `ply_height` null ist.

### Übung 2: den Nullfall interpretieren

Das Geflecht hat `ply = 2` und eine zyklische Paneelordnung. Welche Werte haben `ply_height` und `rigid.refused` bei `t = 0` und bei `t = 0.5`? Liefert eines der Ergebnisse eine Zuordnung starrer Flächen zu Ebenen?

> **Antwort:** Bei null sind `ply_height = 0` und `rigid.refused = false`; bei 0.5 sind `ply_height = 1` und die Zurückweisung wahr. In beiden zyklischen Berichten fehlen Ebenen starrer Paneele, deren Höhe und die Ebenenzuordnung pro Fläche. Eine ausbleibende Zurückweisung bei Dicke null liefert die fehlende konkrete Zuordnung nicht nach; die Zurückweisung bei positiver Dicke betrifft dieses Modell paralleler Paneele.

## 3. Azyklische Bedingungen ermöglichen eine Berechnung des längsten Pfads

Wenn der Paneelgraph eine topologische Ordnung besitzt, initialisiert die Implementierung jede Ebene mit null. Für jede gerichtete Kante von einem unteren Paneel `u` zu einem oberen Paneel `v` aktualisiert sie `level[v] = max(level[v], level[u] + 1)`. Die Verarbeitung in topologischer Reihenfolge stellt sicher, dass die Ebene jedes Vorgängers bereits verfügbar ist. Die höchste nullbasierte Ebene plus eins ist die in Paneelen gezählte Kettenlänge. Multipliziert mit der vollen Materialdicke `t` ergibt das die Stapelhöhe für eine vollständig bestimmte Ordnung.

Das gemeldete `face_levels` ist eine konkrete mögliche Zuordnung, die durch diese Rekurrenz entsteht. Es kann andere gültige Stapel geben; die Werte pro Fläche sind keine kanonische Kennzeichnung jedes zulässigen Stapels.

Der synthetische DAG im Fixture hat die gerichteten Kanten `P → R`, `Q → R` und `R → S`. P und Q dürfen Ebene null teilen, weil das Beispiel keine Beziehung vorgibt, die sie trennen müsste; R muss über beiden liegen, anschließend S über R. Das sind abstrakte Graphdaten, keine exportierte FOLD-Geometrie und keine Aussage über räumliche Überlappung. Sie dienen dazu, die Rekurrenz zu üben, bevor der größere Kranich-Test gelesen wird.

### Übung 3: die Kette berechnen

Weisen Sie den vier Knoten des synthetischen DAGs Ebenen zu, zählen Sie die Paneele in der längsten Kette und berechnen Sie die Höhe für `t = 0.2`. Warum wäre es ein Fehler um eins, nur die höchste Ebene zu melden? Welche beiden Anzahlen unterscheidet zum Vergleich der tatsächliche Kranich-Test?

> **Antwort:** P und Q haben Ebene 0, R Ebene 1 und S Ebene 2. Die Kette umfasst drei Paneele, also beträgt die Höhe `3 × 0.2 = 0.6` in Faltmuster-Koordinateneinheiten. Der höchste Index 2 lässt eine belegte Ebene unberücksichtigt. Der tatsächliche Kranich-Test unterscheidet die maximale lokale Lagenzahl 28 von 36 erforderlichen Ebenen paralleler Paneele; lokale Belegung und eine Kette über mehrere Bereiche hinweg beantworten unterschiedliche Fragen.

## 4. Fehlende Ordnung ist Teil des Ergebnisses

Die Implementierung zählt überlappende Flächenpaare auf unterschiedlichen Paneelen, deren Reihenfolge nicht angegeben ist. Sobald es ein solches Paar gibt, ist `levels_exact` falsch. Sie meldet `max(chain, ply)` als untere Schranke und gibt `face_levels` nicht aus. Azyklische angegebene Bedingungen allein können nicht bestätigen, dass eine vorgeschlagene Platzierung eine Beziehung einhält, die in der Eingabe nie angegeben wurde.

Der festgelegte Test `an_unstated_overlap_gives_a_lower_bound` verwendet zwei überlappende Bögen ohne angegebene Reihenfolge. Er erwartet ein unbestimmtes Paar, zwei Ebenen als untere Schranke und keine Ebenenzuordnung pro Fläche. Ein Aufrufer muss die Exaktheitskennzeichnung zusammen mit der Zahl erhalten. Verwirft die Zusammenfassung eines Agenten diese Kennzeichnung, kann eine spätere Stufe eine untere Schranke in eine angeblich vollständige Anordnung umdeuten, ohne dass jemand diese Entscheidung ausdrücklich trifft.

### Übung 4: Unsicherheit bei einer Übergabe erhalten

Die synthetische Karte mit unvollständiger Ordnung hat Kettenlänge 2, lokale Lagenzahl 3, ein unbestimmtes Paar und `t = 0.2`. Welche numerische Höhe kann der Algorithmus melden, und wie muss sie beschrieben werden? Kann ein Szenenadapter damit jede Fläche platzieren?

> **Antwort:** Er meldet `max(2, 3) = 3` Ebenen und eine untere Höhenschranke von 0.6, mit `levels_exact = false` und `face_levels = null`. Er kann keine vollständige Platzierung liefern. Eine Übergabe sollte die Kennzeichnung als untere Schranke, die Anzahl der Paare mit fehlender Ordnungsangabe, die Quellidentität und die fehlende konkrete Zuordnung erhalten, statt Koordinaten zu versprechen, die aus einer nicht beobachteten Ordnung abgeleitet wären.

## 5. Das Ergebnis in eine überprüfbare Entscheidung überführen

Eine Komposition von Agentenschritten kann die Basisanalyse und die Auswertung starrer Paneele gemeinsam weiterführen. Die [festgelegte Entwurfsentscheidung](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/docs/adr/0007-origami-thickness-as-parallel-rigid-panels.md) belässt die Auswertung der Materialdicke ausdrücklich neben dem Basisurteil. Eine Zurückweisung bedeutet, dass unter den Annahmen paralleler starrer Paneele kein Stapel möglich ist. Sie beweist nicht, dass ein materielles Objekt mit geneigten Paneelen, veränderten Falten oder anderen Konstruktionsmethoden unmöglich ist. Umgekehrt beweist eine ausbleibende Zurückweisung keine Herstellbarkeit.

Erhalten Sie für einen vorgeschlagenen Godot-Versuch die Revision der FOLD-Quelle, die volle Materialdicke samt Einheitenumrechnung, beide Analyseergebnisse, gegebenenfalls einen Zyklusnachweis, die Exaktheit und die Zuordnung von Flächen zu Objekten. Geben Sie einer betrachtenden Person eine konkrete Aufgabe, etwa die Beziehung zu finden, die für eine Zurückweisung verantwortlich ist. Vergleichen Sie ihre Antwort mit der Antwort bei Verwendung eines einfachen Graphdiagramms für dieselbe Aufgabe. Das ist ein vorgeschlagenes Transferexperiment; der Kurs dokumentiert weder Renderer oder Export noch Lernversuch oder Leistungsgewinn. Eine neue DSL wäre ihren Aufwand nur dann wert, wenn sie diese Aufgabe gegenüber einem einfacheren typisierten Bericht und dem vorhandenen Prüfer verbessert.

### Übung 5: entscheiden, was weitergegeben wird

Ein künftiger Agent meldet: „Basisanalyse bestanden; Zurückweisung starrer Paneele bei positiver Materialdicke; Zyklusflächen `[0,3], [3,2], [2,1], [1,0]`.“ Er schlägt vor, das Asset als „physisch unmöglich“ zu kennzeichnen und den Zyklus wegzulassen, weil die Szene plausibel aussieht. Schreiben Sie eine korrigierte Aussage für die Nutzenden und nennen Sie die nächsten erforderlichen Belege für eine Szenendemonstration.

> **Antwort:** „Der angegebene Zustand hat die Basisprüfungen bestanden, aber seine angegebene Ordnung enthält einen Zyklus, der bei dieser positiven Materialdicke einen Stapel paralleler starrer Paneele verhindert.“ Erhalten Sie den Zyklus und die Annahmen. Eine Szenendemonstration benötigt einen an die Quelle gebundenen Import samt Zuordnung von Flächen zu Objekten, eine unabhängig überprüfbare Darstellung des Zyklus und eine dokumentierte Aufgabe für die betrachtende Person. Ein Screenshot allein kann weder das Graphenergebnis noch physische Unmöglichkeit oder einen Lernnutzen belegen.

## Reproduktion und Grenzen

Führen Sie in IX am festgelegten Commit `cargo test -p ix-origami --test thickness` aus. Der Koordinator hat am 2026-10-21 alle 11 Thickness-Integrationstests erneut ausgeführt: 11 bestanden, 0 fehlgeschlagen. Die Fixture-README hält die Quell- und Test-Blobs fest. Die Graphkarten sind von Hand hergeleitete Lehrdaten; es wird weder ein zusätzlicher Analysator noch eine Laufzeitkomponente für ein konsumierendes Projekt eingeführt. Das Bestehen dieser Tests stützt die beschriebenen Implementierungsfälle; fachliche Richtigkeit, flüssige Übersetzung, Lernerfolg, Szenenimport und anonymer Abruf der Veröffentlichung auf Learn bleiben eigenständige offene Aufgaben.
