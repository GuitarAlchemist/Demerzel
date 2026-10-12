---
module_id: net-003-worker-lane-coverage-and-fragility
department: network-science
course: "Abdeckung von Worker-Lanes nach einem Moduswechsel messen"
level: intermediate
prerequisites: [net-002-capability-graphs-and-projections]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-003
version: "0.1.0"
---

# Abdeckung von Worker-Lanes nach einem Moduswechsel messen

> **Fachbereich Netzwerkwissenschaft** | Mittelstufe | 35 Minuten | Deutscher Entwurf; Prüfung und Veröffentlichung ausstehend

## Lernziele und Projektfrage

Sie erstellen aus einer auf einen Commit festgelegten Demerzel-Lane-Policy einen Graphen zwischen Workern und Arbeitsklassen. Sie messen die Abdeckung, die Folgen des Entfernens eines Workers und den Informationsverlust der Projektion bezüglich Rollen und Entscheidungen. **Projektfrage:** Wenn der beratende Fan-out-Modus wechselt oder eine Lane nicht verfügbar ist, welche *deklarierten Arbeitsklassen* haben noch einen benannten Weg? Die Rechnung kann eine Lane-Auswahl oder Prüffrage unterstützen. Sie belegt weder, dass ein Agent online ist, noch dass er handeln darf oder Arbeit abgeschlossen hat.

[NET-002](../en/net-002-capability-graphs-and-projections.md) verbindet *Repositorys* mit Fähigkeitsfamilien. Hier verbinden wir *Worker* mit zugewiesenen Rollen und deren Arbeitsklassen. Die Kanten stammen aus der [Demerzel-Policy im Commit `ecdc6c2`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) und werden nach dem angefragten Modus gefiltert. Der Graph enthält weder MCP-Routen noch Angaben zum aktuellen Agentenstatus.

## 1. Den Graphen vor der Messung definieren

Die festgelegte Policy nennt fünf Worker: `jules`, `claude`, `gemini`, `codex` und `augment`. Jeder hat eine `primary`-Rolle, eine Liste `secondary`-Rollen und eine getrennte Liste `forbidden` ([Worker-Definitionen](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L54-L79)). Jede benannte Rolle verweist auf eine `work_class` ([Rollendefinitionen](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L19-L51)). Die Policy bezeichnet sich als **beratend und als Trockenlauf**. Sie schlägt eine Zuordnung vor, liefert aber keinen Beleg für erledigte Arbeit.

Erstellen Sie einen gerichteten Graphen mit drei Ebenen `Worker → zugewiesene Rolle → Arbeitsklasse`. Zeichnen Sie die erste Kante nur für eine primäre oder sekundäre Rolle; eine verbotene Rolle erzeugt keinen Weg. Die zweite Kante folgt `work_class`. Für einen Modus blenden Sie Wege aus, deren Klasse in [`mode_blocks`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L81-L86) steht. In der Projektion auf zwei Ebenen besteht eine Worker-Klasse-Kante, wenn mindestens ein zugewiesener Rollenpfad bestehen bleibt. Mehrere Rollen derselben Klasse zählen als **eine** Worker-Klasse-Kante. Gezählt werden verschiedene benannte Worker je Klasse, weder ihre Kapazität noch erledigte Aufgaben.

Das vollständige Verzeichnis `work_classes` enthält 13 Namen, darunter verbotene Handlungen. Nur fünf Klassen kommen in primären oder sekundären Zuweisungen vor: `fix`, `groom`, `navigate`, `net_new_feature` und `review`. Nennen wir diese Menge `A`. Definieren wir die **Abdeckung** `C(m) = |{c in A: degree_m(c) > 0}| / |A|` und die **Anzahl redundanter Klassen** `R(m) = |{c in A: degree_m(c) >= 2}|`. Diese Graphenwerte sind beschreibend. Zwei Worker derselben Klasse sind für eine bestimmte Rolle nicht zwangsläufig austauschbar.

### Übung 1: Rollen nicht doppelt zählen

In NORMAL hat `claude` die Rollen `draft_to_ready_helper`, `test_author` und `review_feedback_applier`, alle in `fix`, sowie `builder_fixer` in `net_new_feature` und `lightweight_groomer` in `groom`. Welchen Grad hat `claude` in der Worker-Klasse-Projektion und wie viele Wege zu zugewiesenen Rollen gibt es? Warum unterscheiden sich die Zahlen?

> **Antwort:** Der projizierte Grad ist **3**: `fix`, `net_new_feature`, `groom`. Es gibt **5** zugewiesene Rollenpfade, einen primären und vier sekundäre. Die drei `fix`-Rollen werden zu einer Worker-Klasse-Kante zusammengefasst. Fünf Rollen als fünf alternative Worker zu zählen würde die Redundanz künstlich erhöhen.

## 2. Die Modussperre messen

Aus den primären und sekundären Zuweisungen folgt diese Projektion für NORMAL. Eine `1` bedeutet, dass mindestens ein zugewiesener Rollenpfad die Klassensperre des Modus übersteht:

| Worker | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 1 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

Die Matrix enthält **9** Worker-Klasse-Kanten. Die Klassengrade sind `fix:2`, `groom:2`, `navigate:1`, `net_new_feature:1`, `review:3`. Damit gelten `C(NORMAL)=5/5` und `R(NORMAL)=3`. CONSTRAINED sperrt `net_new_feature` und `broad_architecture`; DRAINING sperrt zusätzlich `workflow_policy_change`. Von diesen Klassen hat nur `net_new_feature` einen zugewiesenen Pfad. **Beide** Modi behalten daher 8 Kanten und vier abgedeckte Klassen: `C=4/5`, `R=3`. HALTED sperrt außerdem `fix`, `groom` und `navigate`, aber nicht `review`. Es bleiben drei Kanten zu `review`: `C(HALTED)=1/5`, `R(HALTED)=1`. Dieses Verhältnis erlaubt keinen Betrieb eines angehaltenen Systems; es beschreibt nur die Deklarationen, die den Filter überstehen.

### Übung 2: Eine Graphensperre statt eines Ausfalls berechnen

Welche NORMAL-Kante entfällt in DRAINING, wie lauten `C` und `R`, und beweist die Rechnung, dass ein Claude-Agent tatsächlich aufgehört hat zu arbeiten?

> **Antwort:** Nur `claude → net_new_feature` entfällt, denn das ist die einzige zugewiesene Kante dieser gesperrten Klasse. Acht der neun Kanten bleiben; vier von fünf Klassen sind abgedeckt, also `C=4/5`. `fix`, `groom` und `review` haben weiterhin mindestens zwei Worker-Nachbarn, also `R=3`. Das ist eine Sperre im Policy-Graphen, kein Nachweis für einen laufenden Agenten oder eine tatsächliche Zuweisung.

## 3. Anfälligkeit beim Wegfall eines Workers testen

Für Modus `m` und entfernten Worker `w` sei `L_m(w)` die Zahl der vorher abgedeckten, danach aber nicht mehr abgedeckten Klassen. Entfernen Sie `w` und seine Rollenpfade und berechnen Sie die Grade erneut. In DRAINING ist `augment` der einzige Worker mit einer `navigate`-Kante. Ohne ihn sinkt deren Grad von 1 auf 0; somit `L_DRAINING(augment)=1` und die Abdeckung fällt von `4/5` auf `3/5`. Entfernt man einen der anderen vier Worker, geht **keine ganze Klasse** verloren, da ein weiterer benannter Worker bleibt. Diese Knotenentfernung prüft die Empfindlichkeit des Graphen und sagt keine Ausfallwahrscheinlichkeit voraus. Die JSON-Policy erfasst nicht alle Ursachen mangelnder Verfügbarkeit; eine gemeinsame Klasse garantiert auch nicht die genau benötigte Rolle.

Klassenredundanz ist nicht Rollenredundanz. `review` hat in DRAINING drei Worker-Nachbarn. Doch `gemini` mit der primären Rolle `read_only_critic`, `jules` mit der sekundären Rolle `architecture_summarizer` und die sekundären Review-Rollen von `codex` haben verschiedene Aufgaben. Der Graph zeigt einen verbliebenen Weg zur allgemeinen Klasse `review`, aber nicht drei Ersatzkräfte für jede konkrete Review-Rolle. Eine Eskalation oder Neuzuordnung kann weiterhin nötig sein.

### Übung 3: Einen Knoten entfernen

Vergleichen Sie das Entfernen von `augment` mit dem Entfernen von `codex` im DRAINING-Graphen. Welche Klassen gehen verloren, und welche Abdeckung ergibt sich? Kann der Graph allein die Qualität ersetzender Review-Notizen beurteilen?

> **Antwort:** Ohne `augment` entfällt `navigate`; `fix`, `groom` und `review` bleiben, also `C=3/5`. Ohne `codex` entfällt keine ganze Klasse: `claude` behält `fix`, `jules` und `gemini` behalten `review`; `C=4/5`. Keines der Ergebnisse misst Qualität, Berechtigungen, genaue Rollengleichwertigkeit, Verfügbarkeit oder Aufgabenerfüllung.

## 4. Selektorsemantik neben dem Graphen bewahren

Der [festgelegte beratende Lane-Selektor](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L1-L19) nutzt die Policy. Er prüft der Reihe nach unbekannten Worker, unbekannten Modus, verbotene Rollen, Zugehörigkeit der angefragten Rolle zur Lane und die Klassensperre ([Entscheidungsreihenfolge](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L77-L154)). Eine zugewiesene primäre Rolle in einer ungesperrten Klasse ergibt `allow`; eine sekundäre ergibt `recommend`, nicht `allow`. Eine verbotene Rolle ergibt `block`, **bevor** die Rollenzugehörigkeit geprüft wird. Eine nicht zugewiesene Rolle ergibt `warn`. Eine gesperrte Klasse ergibt `block` mit Backpressure-Code. Dies sind vom Code erzeugte Antworten, keine Erlaubnisse zur Zustandsänderung. Exitcode 0 bedeutet **ausgewertet**; die Entscheidung steht im JSON. Eingabe- oder Policy-Fehler können Exitcode 2 ergeben.

In DRAINING gehört die primäre Rolle `builder_fixer` von `claude` zur gesperrten Klasse `net_new_feature`, seine sekundäre Rolle `test_author` hingegen zur ungesperrten Klasse `fix`. Der Code lässt für die erste Anfrage `block`, für die zweite `recommend` erwarten. Daraus folgt **nicht**, dass `test_author` eine neue Funktion bauen kann: angefragte Rolle und erwartetes Ergebnis müssen zur Aufgabe passen. Für `codex` ist `autonomous_merge_actor` ausdrücklich verboten; die Anfrage ergibt daher auch nach einem Moduswechsel voraussichtlich `block`. Keine Graphenkante erlaubt einen Merge.

### Übung 4: Pfade und Entscheidungen unterscheiden

Welche Entscheidungen erwarten Sie in DRAINING für `(claude, builder_fixer)`, `(claude, test_author)` und `(codex, autonomous_merge_actor)`? Welche Information zur letzten Anfrage verliert die Worker-Klasse-Projektion?

> **Antwort:** Die erste ergibt `block`, da `net_new_feature` gesperrt ist; die zweite `recommend`, da `test_author` eine ungesperrte *sekundäre* `fix`-Rolle ist; die dritte `block`, da `autonomous_merge_actor` in der Verbotsliste von `codex` steht. Die Projektion enthält weder diese Liste noch die Prüfungsreihenfolge. Eine fehlende Merge-Kante ist weder bloß eine Warnung wegen unbekannter Rolle noch eine Erlaubnis.

## 5. Die Messung widerlegbar machen

Die Werte oben wurden aus dem **festgelegten JSON** berechnet: primäre und sekundäre Rollen erweitern, auf `work_class` abbilden, `mode_blocks` filtern und doppelte Paare `(Worker, Klasse)` entfernen. Für die getrennte Prüfung der Selektorinterpretation schlagen wir einen kleinen Offline-Durchlauf mit demselben Script und derselben Policy vor. Prüfen Sie die 22 zugewiesenen Paare `(Worker, Rolle)` in allen vier Modi; zählen Sie `allow` und `recommend` als ungesperrte zugewiesene Pfade, `block` als durch den Modus gesperrte Pfade. Aus dem Quellcode folgen 22 aktive Rollenpfade in NORMAL, 21 in CONSTRAINED und DRAINING sowie 8 in HALTED. Die projizierten Worker-Klasse-Kanten sollten 9, 8, 8 und 3 betragen, die überlebenden **primären** Pfade 5, 4, 4 und 1. Dies sind Vorhersagen des festgelegten Codes, **keine** Resultate eines für diese Lektion ausgeführten Durchlaufs.

Speichern Sie das Entscheidungs-JSON jeder Anfrage mit dem SHA und vergleichen Sie Entscheidungen statt Exitcodes. Ergänzen Sie als getrennte Kontrollfälle eine verbotene Anfrage, eine unbekannte Rolle und einen unbekannten Modus; keiner gehört zu den 22 zugewiesenen Paaren. Eine Abweichung würde die angenommene Pfadregel widerlegen oder eine Änderung des abgespielten Codes zeigen. Übereinstimmung würde dieses begrenzte Modell für die getestete Revision stützen, aber weder tatsächliche Planung, Worker-Gesundheit noch korrekte menschliche Governance nachweisen.

### Übung 5: Das Prüforakel entwerfen

Angenommen, `(claude, builder_fixer, DRAINING)` liefert Exitcode 0 und im JSON die Entscheidung `block`. Ein Kollege zählt wegen des erfolgreichen Prozesses einen aktiven Pfad. Wie ist er richtig einzuordnen? Nennen Sie einen Wert, dessen Abweichung die Graphenableitung widerlegen würde.

> **Antwort:** Es ist ein **zugewiesener, aber gesperrter Rollenpfad**. Exitcode 0 sagt nur, dass die beratende Anfrage ausgewertet, nicht erlaubt wurde. Der Durchlauf sollte in DRAINING 21 ungesperrte zugewiesene Rollenpfade und nach Projektion 8 Worker-Klasse-Kanten finden. Beispielsweise 22 Pfade oder 9 Kanten bei derselben festgelegten Policy und demselben Script würden die Ableitung widerlegen. Das allein bewiese keinen Produktionsvorfall.

## Evidenz und Grenzen

- Die [Lane-Policy](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) und der [Selektor](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) sind auf Demerzel-Commit `ecdc6c27559bb1a11343cfad33687465893e9891` festgelegt. Die Werte sind nachvollziehbare Rechnungen aus dem JSON, keine Messungen aktiver Agenten. Der Durchlauf in Abschnitt 5 wurde vorgeschlagen, aber für diese Lektion nicht ausgeführt.
- Der Graph fasst verschiedene zugewiesene Rollen zu Klassen zusammen. Verbotene Rollen sowie vollständige Eingaben, Entscheidungsreihenfolge und Autorität des Selektors fehlen. `allow` und `recommend` sind beratende Antwortwerte, keine Erledigungsbelege.
- Worker-Entfernung und Modussperren sind Empfindlichkeitsversuche auf einem statischen deklarierten Graphen. Vor Aussagen über tatsächliche Zuordnung prüfen Sie die aktuelle Policy-Revision, reale Anfrage und Entscheidung, Präsenz und Berechtigungen des Workers sowie Artefakt oder Beleg der Aufgabe. Fachliche Prüfung, Lernversuche, Übersetzungsprüfung, Learn-Synchronisierung und -Build sowie anonymer öffentlicher Abruf stehen aus.
