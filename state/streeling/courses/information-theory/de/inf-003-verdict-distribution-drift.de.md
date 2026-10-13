---
module_id: inf-003-verdict-distribution-drift
department: information-theory
course: "Veränderungen von Urteilsverteilungen mit Jensen-Shannon-Divergenz messen"
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-003
version: "0.1.0"
---

# Veränderungen von Urteilsverteilungen mit Jensen-Shannon-Divergenz messen

> **Fachbereich Informationstheorie** | Niveau: Mittelstufe | Geschätzte Dauer: 35 Minuten | Status: deutscher KI-Entwurf; fachliche, didaktische und sprachliche Prüfung sowie Veröffentlichung ausstehend

## Lernziele

Nach dieser Lektion kannst du:

- vergleichbare Häufigkeiten der IX-Analyseurteile in gleich geordnete Wahrscheinlichkeitsvektoren umwandeln;
- die gerichtete Kullback–Leibler-Divergenz (KL) und die symmetrische Jensen–Shannon-Divergenz (JS) in den von IX zurückgegebenen Einheiten berechnen;
- erklären, warum eine neue Kategorie in einer KL-Richtung einen Fehler auslösen kann, während JS endlich bleibt;
- einen Divergenzwert als Anlass zur Untersuchung von Belegen nutzen und dabei Analysegrenzen und Zusammensetzung der Gruppen kontrollieren.

## Die Projektfrage

Der [Petri-Netz-Analysator von IX in der festgehaltenen Revision](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L105) serialisiert das Ergebnis einer Eigenschaft als `holds`, `fails` oder `unknown`. Zu `fails` kann ein Gegenbeispiel gehören; `unknown` bedeutet, dass der Analysator innerhalb der Suchgrenzen keine Entscheidung getroffen hat. Eine veränderte Häufigkeit dieser Ergebnisse zwischen zwei Läufen kann eine Untersuchung rechtfertigen. Wie lässt sich die Veränderung beziffern, ohne eine Zahl als Beweis für eine Regression misszuverstehen?

Die widerlegbare Frage lautet: **Wie stark änderte sich für eine Eigenschaft, dieselben Netz-IDs, dieselbe Analysatorrevision und dieselben Grenzen die Kategorienverteilung nach Änderung der Netze?** IX stellt bereits [KL- und JS-Funktionen](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L222) bereit, auch als [DuckDB-Skalarfunktionen](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-duck/src/inference.rs#L186-L210). Wir rechnen ein kleines **synthetisches** Beispiel nach. Weder eine produktive IX-Gruppe noch eine von Nutzern wahrgenommene Qualitätsänderung wurde gemessen.

INF-001 verwendete Entropie für eine einzelne Verteilung von Richtlinientokens. INF-002 zeigte, welche Unterschiede zwischen Vektoren GAs kompakte OPTIC-K-Abbildung verliert. Hier vergleichen wir **zwei Verteilungen über dieselben benannten Urteilskategorien**. Der Wert beschreibt aggregierte Häufigkeiten; er zeigt weder welches Netz sich änderte, noch warum oder ob die Änderung gut ist.

## 1. Eine Beobachtung mit gleichbleibender Bedeutung wählen

Das [`Verdict<T>`-Enum](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L95) besitzt drei Kennzeichnungen. `holds()` liefert nur für `Holds` true; `Unknown` wird nicht stillschweigend als Erfolg gewertet. Der Bericht `Analysis` enthält **verschiedene Eigenschaften**, darunter `deadlock_free`, `bounded`, `quasi_live`, `live` und `reversible`. Ihre Häufigkeiten zusammenzufassen würde Fragen mit verschiedenen Beweisbedingungen vermischen. Wir wählen nur `deadlock_free`, ein Urteil pro Netz und die Reihenfolge `[holds, fails, unknown]`.

Der [Zweig für Deadlockfreiheit](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L465-L491) verdeutlicht die Bedeutung der Kennzeichnungen. Eine gefundene tote Markierung ergibt `Fails`, selbst wenn die Enumeration danach abbricht; `max_reported_deadlocks` begrenzt die ausgegebenen Zeugen und darf null sein. Wird keine tote Markierung gefunden, erfordert `Holds` eine vollständige Suche; andernfalls ergibt sich `Unknown`. Das gilt für diesen Eigenschaftszweig, nicht automatisch für alle Eigenschaften des Analysators.

Die folgende Gruppe aus zehn Netzen ist ein **erfundenes** Rechenbeispiel:

| Lauf | Holds | Fails | Unknown | Gesamt |
|---|---:|---:|---:|---:|
| Ausgangswert | 8 | 0 | 2 | 10 |
| Kandidat | 6 | 2 | 2 | 10 |

Durch Division jeder Zeile durch ihre Summe erhalten wir `p = [0.8, 0, 0.2]` und `q = [0.6, 0.2, 0.2]`. Beide Vektoren müssen dieselbe Reihenfolge verwenden. Die Funktion nähme auch unterschiedlich sortierte Arrays an, vergliche dann aber die falschen Ereignisse. Speichere die Kennzeichnungen mit den Zahlen und prüfe ihre Reihenfolge.

### Übung 1: Vergleichbare Vektoren bilden

Schreibe die normierten Vektoren in der Reihenfolge `[holds, fails, unknown]`. Welche Metadaten braucht ein realer Vergleich?

> **Antwort:** `p=[8/10,0/10,2/10]=[0.8,0,0.2]`; `q=[6/10,2/10,2/10]=[0.6,0.2,0.2]`. Bewahre Eigenschaft, Netz-IDs, Kategorienreihenfolge, Analysator-Commit, Suchgrenzen und die Gesamtzahl jedes Laufs auf. Die Divergenzrechnung prüft diese Voraussetzungen nicht selbst.

## 2. Nachlesen, was IX tatsächlich berechnet

Die Funktion [`normalize`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L173) teilt einen nicht negativen Vektor durch seine Summe. Sie weist leere Vektoren, negative oder NaN-Einträge sowie eine Nullsumme zurück. Unser Protokoll verlangt zusätzlich endliche Zahlen vor dem Aufruf: positiven unendlichen Wert weist der Quellcode nicht ausdrücklich zurück. Beide Divergenzen verlangen gleich lange Vektoren und verwenden natürliche Logarithmen; das Ergebnis hat die Einheit **Nat**. Für Bit teile durch `ln(2)`. Der DuckDB-Wrapper bietet `ix_kl(p,q)` und `ix_js(p,q)` für `DOUBLE[]`: Eine SQL-`NULL`-Liste führt zu `NULL`, ein mathematischer Fehler zu einem SQL-Fehler. Der Wrapper belegt keinen geplanten Vergleichsjob.

KL ist gerichtet:

`D_KL(p || q) = Σ_i p_i ln(p_i / q_i)`.

Nur Kategorien mit `p_i > 0` tragen bei. Hier gilt `D_KL(p || q)=0.8 ln(0.8/0.6)+0.2 ln(0.2/0.2)=0.23014565796142483` Nat. In Gegenrichtung verlangt `fails` den Term `0.2 ln(0.2/0)`: Mathematisch divergiert er; [IX gibt einen Fehler zurück](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L185-L209), keinen Unendlichkeitswert. Vertauschte Argumente beantworten eine andere Frage. Wandle einen Fehler durch eine neu beobachtete Kategorie nicht in null um.

### Übung 2: Die KL-Richtung erklären

Berechne `D_KL(p || q)`. Gibt `D_KL(q || p)` in IX dieselbe Zahl zurück?

> **Antwort:** `D_KL(p || q)=0.8 ln(4/3)=0.23014565796142483` Nat. Bei `D_KL(q || p)` trifft `q_fails=0.2` auf `p_fails=0`; nach Vertauschen der Argumente gibt IX den Parameterfehler „q is zero where p is positive“ zurück. KL ist asymmetrisch: Nur die Richtung Ausgangswert-zu-Kandidat hat hier endlichen Support.

## 3. JS als endliche, symmetrische Kennzahl

JS bildet den Mittelpunkt `m=(p+q)/2` und mittelt zwei KL-Werte: `D_JS(p,q)=0.5 D_KL(p||m)+0.5 D_KL(q||m)`. Hier ist `m=[0.7,0.1,0.2]`. Der Mittelpunkt hat überall dort positive Masse, wo einer der Eingangsvektoren welche hat. JS bleibt daher für dieses Paar endlich. [Code und Kommentar](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L210-L222) bezeichnen JS als symmetrisch und durch `ln(2)` Nat beschränkt. Null bedeutet identische **normierte** Verteilungen, nicht identische Läufe oder Gruppengrößen.

Eine unabhängige Rechnung ergibt `D_KL(p||m)=0.10682511409961822` und `D_KL(q||m)=0.04613902821563412`; ihre halbe Summe beträgt `D_JS=0.07648207115762617` Nat oder `0.1103403047760241` Bit. Diese Zahlen stammen aus dem synthetischen Beispiel, nicht aus einem IX-Produktionslauf. Die [festgelegten Unit-Tests](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L568-L580) prüfen das Maximum für disjunkte One-Hot-Vektoren und null für gleiche Eingaben; wir haben diese Tests hier nicht ausgeführt.

### Übung 3: JS berechnen und begrenzen

Berechne Mittelpunkt und JS. Ändert ein Tausch der Läufe den Wert? Was ist das theoretische Maximum in Nat?

> **Antwort:** `m=[0.7,0.1,0.2]`; `D_JS=0.5(0.10682511409961822+0.04613902821563412)=0.07648207115762617` Nat. Ein Tausch lässt den Mittelpunkt gleich und vertauscht die gleich gewichteten Terme; JS bleibt unverändert. Das Maximum beträgt `ln(2)=0.6931471805599453` Nat für disjunkte Supports.

### Übung 4: Was die Normierung verbirgt

Vergleiche `[80,0,20]` und `[8,0,2]` mit `ix_js`. Was beweist das Ergebnis?

> **Antwort:** Beide werden zu `[0.8,0,0.2]` normiert; `ix_js` ergibt `0`, vorbehaltlich der Gleitkommadarstellung. Bewiesen ist nur dieselbe Kategorienmischung. Eine Gruppe umfasst 100 Beobachtungen, die andere 10; JS lässt den Größenunterschied verschwinden und sagt auch nicht, ob dieselben Netze dieselben Urteile erhielten. Bewahre Summen und zugeordnete Netz-IDs außerhalb des Werts auf.

## 4. Entscheiden, was das Signal auslösen soll

Angenommen, eine künftig gesondert genehmigte QA-Regel fordert bei `JS > 0.05` Nat eine Untersuchung. Unser **illustrativer** Wert übersteigt diesen erfundenen Grenzwert. Das ist ein Anlass, Daten zu prüfen, kein Beleg für eine bereits eingesetzte Schranke und kein automatischer Ablehnungsgrund. Prüfe zuerst dieselben zehn Netz-IDs und `deadlock_free`, danach Analysatorrevision und `Limits`: Der [Bericht zeigt Abbruch und Grund](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L161-L175). Ein höheres `max_states` kann `unknown` in `holds` oder `fails` verwandeln, ohne ein Netz zu ändern. Ordne Urteile nach Netz-ID zu und prüfe vorhandene Fehlerzeugen und Gründe für Unentschiedenheit. Falls ein benötigter Zeuge fehlt, wiederhole den Lauf mit `max_reported_deadlocks` größer als null. Ein Histogramm zeigt weder die betroffenen Netze noch die Gültigkeit der Gegenbeispiele für die beabsichtigte Eigenschaft.

Bei einer kleinen stabilen Gruppe sind die Tabelle mit drei Spalten und die einzelnen Änderungen unter Umständen verständlicher als eine Zahl. Für viele konsistente Gruppen kann der Wert Untersuchungen priorisieren, sofern Tabelle und Belege pro Netz verfügbar bleiben. Das ist ein Gestaltungsvorschlag, kein Ersatz für Zeugenprüfung. Werden wiederholte Alarme überwiegend durch verschiedene Netzgruppen oder Suchbudgets verursacht, ist der Nutzen dieses Signals für den Zweck widerlegt: Das Vergleichsprotokoll muss überarbeitet werden, statt den Grenzwert bis zum Verschwinden der Alarme zu ändern.

### Übung 5: Einen Alarm einordnen

Der hypothetische Grenzwert ist `0.05` Nat; JS beträgt `0.07648207115762617`. Eine Person behauptet: „Der Kandidat ist schlechter; es gibt zwei neue Fehlschläge.“ Welcher Teil ist rechnerisch überprüfbar, und was muss vor der Annahme einer Regression geprüft werden?

> **Antwort:** `0.07648207115762617 > 0.05`: Das synthetische Beispiel würde die erfundene Untersuchungsregel auslösen. Die Tabelle enthält zwei `fails` beim Kandidaten und keine beim Ausgangswert, benennt aber keine geänderten Netze. Prüfe gleiche IDs, Eigenschaft, Revision und Grenzen; ordne die Ergebnisse zu; lies vorhandene Fehlerzeugen und `unknown`-Gründe. Verlange `max_reported_deadlocks > 0` und wiederhole den Lauf, wenn ein erforderlicher Zeuge fehlt. Andere Grenzen oder andere Netze könnten die Verschiebung ohne Coderegression erklären. Der Wert beweist weder Kausalität noch statistische Signifikanz.

## Grenzen und nächster Schritt

Wir haben die Formel anhand einer synthetischen Tabelle unabhängig nachgerechnet und IX-Quellcode beim Commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1` gelesen. Wir haben den Analysator nicht auf zehn Netzen ausgeführt, keine echte DuckDB-Tabelle abgefragt, keine IX-Tests ausgeführt, keine Stichprobenunsicherheit geschätzt und keinen produktiven Grenzwert validiert. Wiederholte, aber unterschiedliche Gruppen bräuchten einen Stichproben- und Zuordnungsplan. Ein begrenztes Folgeexperiment würde eine Eigenschaft je stabiler Netz-ID an zwei festgehaltenen Revisionen mit gleichen Grenzen erfassen, JS berechnen und jedes geänderte Urteil manuell prüfen. Bewahre Tabelle, Netzdatensätze und Zeugen zusammen mit dem Wert auf. Diese Übersetzung ist ein KI-Entwurf: menschliche Prüfung, Learn-Synchronisierung und Build sowie öffentliche Lesekontrolle stehen noch aus.
