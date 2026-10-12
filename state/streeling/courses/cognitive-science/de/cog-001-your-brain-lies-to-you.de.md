---
module_id: cog-001-your-brain-lies-to-you
department: cognitive-science
course: "Grundlagen der Kognitionswissenschaft"
level: beginner
prerequisites: []
estimated_duration: "40 minutes"
produced_by: cognitive-science
version: "1.0.0"
---

# Dein Gehirn belügt dich — Kognitive Verzerrungen, die jeder kennen sollte

> **Fachbereich Kognitionswissenschaft** | Stufe: Einführung | Dauer: 40 Minuten

## Lernziele

Nach dieser Lektion werden Sie in der Lage sein:
- Sieben wesentliche kognitive Verzerrungen zu benennen und zu erklären
- Jede Verzerrung in einem Beispiel aus der Praxis wiederzuerkennen
- Mindestens eine Gegenstrategie pro Verzerrung anzuwenden
- Zu erklären, warum kognitive Verzerrungen für KI-Governance relevant sind

---

## 1. Warum Ihr Gehirn lügt

Ihr Gehirn ist keine Logikmaschine. Es ist eine Überlebensmaschine. Über Hunderttausende von Jahren hat die Evolution es auf Geschwindigkeit optimiert, nicht auf Genauigkeit. Das Ergebnis: eine Reihe mentaler Abkürzungen (Heuristiken), die meistens gut genug funktionieren, aber auf vorhersehbare Weise systematisch versagen.

Diese vorhersehbaren Fehler nennt man **kognitive Verzerrungen** (engl. *cognitive biases*). Sie sind kein Zeichen von Dummheit — sie betreffen jeden, auch Experten. Der Unterschied zwischen einem naiven und einem sorgfältigen Denker ist nicht die Abwesenheit von Verzerrungen. Es ist das Bewusstsein dafür.

Dieser Kurs behandelt sieben Verzerrungen, die bei der Entscheidungsfindung den größten Schaden anrichten — insbesondere in Technologie- und Governance-Kontexten.

---

## 2. Bestätigungsfehler (Confirmation Bias)

### Was es ist

Die Tendenz, nach Informationen zu suchen, diese zu interpretieren und sich an solche zu erinnern, die bestätigen, was man bereits glaubt — während Informationen, die dem widersprechen, ignoriert oder abgetan werden.

### Anschauliches Beispiel

Ein Entwickler ist überzeugt, dass Framework X die beste Wahl ist. Er liest fünf Artikel, die es loben, und einen, der es kritisiert. Später erinnert er sich lebhaft an die fünf positiven Artikel, hat aber nur eine vage Erinnerung an die Kritik. Auf Nachfrage sagt er: „Alles, was ich gelesen habe, sagt, es ist großartig." Das ist keine Lüge. Das Gehirn hat die Informationen tatsächlich asymmetrisch gefiltert.

### Gegenmaßnahmen

- **Aktiv nach widerlegenden Belegen suchen.** Fragen Sie sich vor einer Entscheidung: „Was würde meine Meinung ändern?" Und dann suchen Sie genau danach.
- **Eigene Ideen angreifen.** Bestimmen Sie jemanden (oder sich selbst) mit der Aufgabe, jeden Grund zu finden, warum die Idee falsch ist.
- **Prä-Mortem-Analyse.** Stellen Sie sich vor, die Entscheidung ist gescheitert. Was ging schief? Das zwingt Sie, den negativen Fall zu betrachten.

### Governance-Relevanz

Demerzels aktuelle hexavalente Logik enthält **C (Widersprüchlich)** für einander widersprechende Belege. Das Festhalten eines Widerspruchs kann übersehene Belege sichtbar machen; der Zustand allein beseitigt keinen Bestätigungsfehler.

---

## 3. Ankereffekt (Anchoring)

### Was es ist

Die Tendenz, sich bei Entscheidungen zu stark auf die erste Information zu stützen, der man begegnet (dem „Anker"), selbst wenn diese Information irrelevant ist.

### Anschauliches Beispiel

In einem klassischen Experiment drehten Forscher vor den Teilnehmern ein Glücksrad. Das Rad landete „zufällig" auf 10 oder 65. Dann wurden die Teilnehmer gefragt: „Wie viel Prozent der afrikanischen Länder sind Mitglied der Vereinten Nationen?" Personen, die 65 auf dem Rad sahen, schätzten deutlich höher als jene, die 10 sahen — obwohl ein Glücksrad absolut nichts mit der Frage zu tun hat.

In der Praxis: Wenn jemand zu Beginn eines Meetings sagt „dieses Projekt wird sechs Monate dauern", kreisen alle folgenden Schätzungen um sechs Monate, unabhängig von der Evidenz.

### Gegenmaßnahmen

- **Eigene Schätzung erstellen, bevor man andere hört.** Schreiben Sie sie privat auf und vergleichen Sie dann.
- **Die Spanne betrachten, nicht nur den Einzelwert.** Fragen Sie: „Was ist der beste Fall? Der schlimmste? Der wahrscheinlichste?" Das durchbricht das Einzel-Anker-Muster.
- **Runde Zahlen misstrauisch betrachten.** „Etwa eine Million Nutzer" oder „sechs Monate" sind fast sicher Anker, keine Analysen.

### Governance-Relevanz

Die Konfidenzschwellen in Demerzels Framework (0.9 / 0.7 / 0.5 / 0.3) erzwingen eine explizite Kalibrierung, anstatt einem einzelnen Anker die Dominanz zu überlassen. Man kann nicht einfach sagen „Ich bin ziemlich sicher" — man muss eine Zahl vergeben, die einer bestimmten Aktion zugeordnet ist.

---

## 4. Verfügbarkeitsheuristik (Availability Heuristic)

### Was es ist

Die Tendenz, die Wahrscheinlichkeit eines Ereignisses danach zu beurteilen, wie leicht Beispiele in den Sinn kommen, anstatt nach der tatsächlichen Häufigkeit.

### Anschauliches Beispiel

Nach der Berichterstattung über einen Flugzeugabsturz überschätzen Menschen das Flugrisiko dramatisch — obwohl Fliegen statistisch weit sicherer ist als Autofahren. Der Absturz ist lebendig, emotional und aktuell, also kommt er leicht in den Sinn. Die Tausenden reibungslosen Flüge an diesem Tag sind unsichtbar.

In der Technik: Ein Team erlebt einen katastrophalen Deployment-Fehler. Für das nächste Jahr überdimensionieren sie jedes Deployment und fügen Wochen an Prozessen hinzu, um eine Wiederholung zu verhindern — obwohl die tatsächliche Fehlerrate bei 0,1% liegt.

### Gegenmaßnahmen

- **Nach der Basisrate fragen.** Bevor Sie beurteilen, wie wahrscheinlich etwas ist, schauen Sie nach, wie oft es tatsächlich vorkommt. „Wie viele Deployments sind letztes Jahr von wie vielen insgesamt gescheitert?"
- **Lebhafte Anekdoten misstrauisch betrachten.** Eine fesselnde Geschichte ist keine Datenerhebung. Ein einziges anschauliches Beispiel kann hundert stille Erfolge überwiegen.
- **Tatsächliche Häufigkeit verfolgen.** Protokolle, Metriken und Aufzeichnungen schlagen das Gedächtnis jedes Mal.

### Governance-Relevanz

Deshalb verlangt Demerzels Politik evidenzbasierte Überzeugungszustände (T/F/U/C mit Wahrscheinlichkeitsgewichtung) statt Bauchgefühl. Eine Governance-Entscheidung auf Basis von „Ich erinnere mich, dass etwas schiefging" ist nicht akzeptabel — die Überzeugung muss in Evidenz mit expliziten Konfidenzniveaus verankert sein.

---

## 5. Dunning-Kruger-Effekt

### Was es ist

Menschen mit geringer Kompetenz in einem Bereich neigen dazu, ihre Fähigkeiten zu überschätzen, während hochkompetente Menschen ihre Fähigkeiten eher unterschätzen. Je weniger man weiß, desto weniger weiß man darüber, wie viel man nicht weiß.

### Anschauliches Beispiel

Ein Berufseinsteiger, der gerade ein Online-Tutorial abgeschlossen hat, verkündet, er könne „definitiv ein produktionsreifes verteiltes System bauen." Ein erfahrener Ingenieur mit 20 Jahren Berufserfahrung sagt: „Ich denke, wir können es wahrscheinlich bauen, aber es gibt mehrere Unbekannte, die mich beunruhigen." Der Anfänger ist übermäßig zuversichtlich, weil er die Komplexität nicht sehen kann. Der Erfahrene ist vorsichtig, weil er sie sieht.

### Gegenmaßnahmen

- **Mit Experten abgleichen.** Wenn Sie sich bei etwas außerhalb Ihres Fachgebiets sicher fühlen, fragen Sie jemanden, der tatsächlich in diesem Bereich arbeitet.
- **Eigene Vorhersagen verfolgen.** Schreiben Sie auf, was Ihrer Meinung nach passieren wird, und überprüfen Sie es später. Wenn Sie regelmäßig falsch liegen, ist Ihre Zuversicht falsch kalibriert.
- **„Ich weiß es nicht" akzeptieren.** Die gefährlichsten Worte bei der Entscheidungsfindung sind nicht „Ich weiß es nicht" — sondern „Ich bin mir sicher."

### Governance-Relevanz

Der Zustand **U (Unbekannt)** in der aktuellen hexavalenten Logik hält unzureichende Belege fest. „Unbekannt“ statt einer Vermutung kann übermäßige Sicherheit begrenzen und eine Untersuchung auslösen; es diagnostiziert keine Fähigkeit einer Person.

---

## 6. Versunkene-Kosten-Irrtum (Sunk Cost Fallacy)

### Was es ist

Die Tendenz, weiter in etwas zu investieren, weil man bereits investiert hat (Zeit, Geld, Aufwand), obwohl die Evidenz nahelegt, dass man aufhören sollte.

### Anschauliches Beispiel

Sie haben 8 Monate mit der Entwicklung einer Funktion verbracht. Nutzertests zeigen, dass niemand sie will. Die rationale Entscheidung wäre, sie einzustellen. Aber das Team sagt: „Wir haben schon so viel investiert — wir können jetzt nicht aufhören." Die 8 Monate sind so oder so vergangen. Sie können nicht zurückgeholt werden. Die einzige Frage ist: „Ist das angesichts unserer aktuellen Lage die beste Verwendung unseres nächsten Monats?" Vergangene Investitionen sind für diese Frage irrelevant.

### Gegenmaßnahmen

- **Den Neustart-Test anwenden.** Fragen Sie: „Wenn wir heute bei Null anfangen würden, ohne bisherige Investition, würden wir uns für dieses Projekt entscheiden?" Wenn die Antwort nein ist, sollte die bestehende Investition diese Antwort nicht ändern.
- **Entscheider und Investor trennen.** Die Person, die die ursprüngliche Investition genehmigt hat, kann oft nicht objektiv beurteilen, ob weitergemacht werden soll. Holen Sie eine frische Perspektive ein.
- **Das Beenden schlechter Projekte feiern.** Machen Sie das Stoppen zu einem Zeichen guter Urteilskraft, nicht zu einem Scheitern.

### Governance-Relevanz

Demerzels Rollback-Politik unterstützt ausdrücklich die Rücknahme von Entscheidungen unabhängig von früheren Investitionen. Artikel 3 der Verfassung (Reversibilität) besagt: Bevorzuge umkehrbare Handlungen. Die Fähigkeit, zu stoppen und umzukehren, ist eine Stärke, kein Versagen.

---

## 7. Status-quo-Verzerrung

### Was es ist

Die Tendenz, den aktuellen Zustand zu bevorzugen, einfach weil er der aktuelle ist, selbst wenn Alternativen besser wären.

### Anschauliches Beispiel

Ein Team nutzt seit drei Jahren ein bestimmtes Werkzeug. Eine eindeutig bessere Alternative existiert — sie ist schneller, günstiger und besser unterstützt. Aber der Wechsel würde bedeuten, etwas Neues zu lernen, also bleibt das Team beim Alten. Der Standard gewinnt nicht, weil er der beste ist, sondern weil er bereits da ist.

### Gegenmaßnahmen

- **Die Frage umkehren.** Statt „Sollten wir wechseln?" fragen Sie: „Wenn wir heute die Alternative nutzen würden, würden wir zu dem wechseln, was wir derzeit haben?" Wenn die Antwort nein ist, unterliegen Sie der Status-quo-Verzerrung.
- **Die Kosten des Nichtstuns beziffern.** Nichts zu tun ist nicht kostenlos. Berechnen Sie, was die aktuelle Wahl Sie an Zeit, Geld oder Chancen kostet.
- **Regelmäßige Überprüfungspunkte setzen.** Planen Sie vierteljährliche Überprüfungen wichtiger Werkzeug- und Prozessentscheidungen, damit der Standard periodisch hinterfragt wird.

### Governance-Relevanz

Die Kaizen-Politik verlangt kontinuierliche Verbesserung — aktiv nach besseren Ansätzen suchen, anstatt den Status quo zu akzeptieren. PDCA-Zyklen (Plan-Do-Check-Act) bauen Neubewertung in den Prozess ein.

---

## 8. Überlebensverzerrung (Survivorship Bias)

### Was es ist

Die Tendenz, sich auf Erfolge (die „Überlebenden") zu konzentrieren, während die Misserfolge, die nicht mehr sichtbar sind, ignoriert werden, was zu falschen Schlussfolgerungen über Erfolgsursachen führt.

### Anschauliches Beispiel

Startup-Ratgeber-Artikel zeigen Gründer, die das Studium abgebrochen und Milliardäre geworden sind. Schlussfolgerung: Studienabbruch führt zum Erfolg! Aber für jeden Studienabbrecher-Milliardär gibt es Tausende von Abbrechern in gewöhnlichen Berufen. Ihre Geschichten hört man nie. Die erfolgreichen Abbrecher sind sichtbar; die erfolglosen sind unsichtbar.

In der Musik: „Übe einfach 8 Stunden am Tag wie die Großen!" Aber für jeden Musiker, der 8 Stunden geübt hat und Erfolg hatte, gab es viele andere, die dasselbe taten und nicht erfolgreich wurden. Übung ist notwendig, aber nicht hinreichend — und die Überlebensverzerrung lässt es aussehen, als wäre es die einzige Variable.

### Gegenmaßnahmen

- **Fragen Sie: „Wo sind die, die es nicht geschafft haben?"** Suchen Sie für jede Erfolgsgeschichte nach den unsichtbaren Misserfolgen, die denselben Weg gingen.
- **Die vollständige Stichprobe betrachten, nicht nur die Überlebenden.** Nur erfolgreiche Unternehmen zu studieren zeigt, was Gewinner tun, nicht was das Gewinnen verursacht.
- **Vorsicht bei „Mach einfach, was sie gemacht haben"-Ratschlägen.** Das Gesamtbild umfasst alle, die dasselbe getan haben und gescheitert sind.

### Governance-Relevanz

Demerzels Belief-Currency-Politik verlangt die Verfolgung widerlegender Evidenz, nicht nur bestätigender Evidenz. Governance-Entscheidungen müssen berücksichtigen, was gescheitert und verschwunden ist, nicht nur was erfolgreich war und sichtbar blieb.

---

## 9. Das große Ganze — Warum das für KI-Governance wichtig ist

KI-Agenten erben menschliche Verzerrungen durch ihre Trainingsdaten, die Annahmen ihrer Entwickler und ihre Optimierungsziele. Ein KI-Governance-Framework, das kognitive Verzerrungen ignoriert, baut auf Sand.

Demerzels Architektur begegnet Verzerrungen systematisch:

| Verzerrung | Governance-Gegenmaßnahme |
|------------|--------------------------|
| Bestätigungsfehler | C (Widersprüchlich)-Zustand erzwingt Aufmerksamkeit für widersprüchliche Belege |
| Ankereffekt | Explizite Konfidenzschwellen verhindern Verankerung an einer einzelnen Schätzung |
| Verfügbarkeitsheuristik | Evidenzbasierte Überzeugungszustände überschreiben lebhafte Anekdoten |
| Dunning-Kruger | U (Unbekannt)-Zustand verhindert falsche Gewissheit |
| Versunkene-Kosten-Irrtum | Rollback-Politik + Reversibilitätsartikel unterstützen das Beenden schlechter Investitionen |
| Status-quo-Verzerrung | Kaizen-Politik verpflichtet zu kontinuierlicher Verbesserung |
| Überlebensverzerrung | Belief-Currency verfolgt widerlegende Evidenz |

Das Wissen um die eigenen Verzerrungen beseitigt sie nicht. Aber es ermöglicht den Bau von Systemen — menschlichen oder KI-basierten — die sie kompensieren.

---

## Schlüsselbegriffe

| Begriff | Definition |
|---------|-----------|
| Kognitive Verzerrung | Ein systematisches Muster der Abweichung von rationalem Urteilen |
| Heuristik | Eine mentale Abkürzung, die schnelle Entscheidungen ermöglicht, aber Fehler produzieren kann |
| Bestätigungsfehler | Bevorzugung von Informationen, die bestehende Überzeugungen bestätigen |
| Ankereffekt | Übermäßiges Vertrauen auf die erste Information, der man begegnet |
| Verfügbarkeitsheuristik | Beurteilung der Wahrscheinlichkeit nach Leichtigkeit des Erinnerns statt nach tatsächlicher Häufigkeit |
| Dunning-Kruger-Effekt | Geringqualifizierte überschätzen ihre Fähigkeiten; Hochqualifizierte unterschätzen sie |
| Versunkene-Kosten-Irrtum | Fortsetzung einer Investition wegen vergangener Kosten statt zukünftigem Nutzen |
| Status-quo-Verzerrung | Bevorzugung des aktuellen Zustands, einfach weil er der aktuelle ist |
| Überlebensverzerrung | Schlussfolgerungen aus Erfolgen ziehen, während unsichtbare Misserfolge ignoriert werden |

---

## Selbstüberprüfung

**1. Ein Team sagt: „Wir haben zu viel investiert, um jetzt aufzuhören." Welche Verzerrung liegt vor, und welche Frage sollten sie stattdessen stellen?**
> Versunkene-Kosten-Irrtum. Sie sollten fragen: „Wenn wir heute bei Null anfangen würden, würden wir dieses Projekt wählen?" Vergangene Investitionen sind für zukünftige Entscheidungen irrelevant.

**2. Nach einem schweren Sicherheitsvorfall will das Team fünf Sicherheitsüberprüfungsebenen für jedes Deployment einführen. Welche Verzerrung könnte hier wirken?**
> Verfügbarkeitsheuristik. Der lebhafte jüngste Vorfall lässt das Risiko größer erscheinen, als es ist. Sie sollten die Basisrate betrachten — wie viele Deployments hatten tatsächlich Sicherheitsprobleme? — und Kontrollen proportional zum tatsächlichen Risiko gestalten.

**3. Sie fühlen sich sehr sicher bei einem Thema, das Sie erst letzte Woche gelernt haben. Was sollte Sie beunruhigen?**
> Dunning-Kruger-Effekt. Am Anfang des Lernens weiß man noch nicht, was man nicht weiß. Suchen Sie Expertenfeedback, verfolgen Sie Ihre Vorhersagen und seien Sie offen für die Möglichkeit, dass Ihre Zuversicht Ihre Kompetenz übersteigt.

**4. Warum verwendet Demerzel U (Unbekannt) anstatt eine Wahr/Falsch-Antwort zu erzwingen?**
> Um dem Dunning-Kruger-Effekt entgegenzuwirken und falsche Gewissheit zu verhindern. Wenn die Evidenz unzureichend ist, löst „Unbekannt" eine Untersuchung aus anstelle einer Vermutung. Das ist ehrlicher und führt zu besseren Entscheidungen.

**Bestanden-Kriterien:** Alle sieben Verzerrungen benennen und definieren können, für mindestens fünf ein Praxisbeispiel geben können und erklären können, wie mindestens drei mit KI-Governance-Konzepten zusammenhängen.

---

## Projektübung: Eine Streeling-Veröffentlichung prüfen

Der [COG‑001-Fall](../../../fixtures/cognitive-science/cog-001/bias-release-case.json) ist **erfunden**; seine Zahlen sind keine Messung von GA oder Learn. Er bildet eine echte Projektgrenze ab: Die [Demerzel-Vorprüfung](https://github.com/GuitarAlchemist/Demerzel/blob/af4e9a3a6f242745730f2d0d28e2535fe7477666/scripts/streeling_course_preflight.py) prüft Quelldateien und Datensätze, aber weder fachliche Qualität noch menschliche Prüfung oder Veröffentlichung. Der [Kandidatenbericht](https://github.com/GuitarAlchemist/Demerzel/blob/af4e9a3a6f242745730f2d0d28e2535fe7477666/scripts/streeling_review_candidates.py) dient der Sichtung, nicht der Freigabe. Die aktuelle kanonische Logik ist **hexavalent** (T/P/U/D/F/C); T/F/U/C oben ist nur ihre didaktische Teilmenge.

Beantworten Sie die Fragen anhand der Falldatei, bevor Sie die Lösungen lesen. Nennen Sie jeweils eine Beobachtung, die Ihre Schlussfolgerung ändern würde. Die Aufgaben prüfen Entscheidungen und diagnostizieren keine Person.

### Exercise 1 — Bestätigung und fehlender Nachweis

Vier lokale Vorschauen waren erfolgreich. Ein Kollege behauptet, alle zwölf Kurse seien veröffentlicht. Was widerspricht dem, und welche Prüfung fehlt?

> **Answer:** Die einzige öffentliche Prüfung ergab 404 unter der angegebenen URL zum angegebenen Zeitpunkt; elf weitere öffentliche Ergebnisse sind unbekannt. Jede URL und die ausgelieferte Revision prüfen sowie menschliche Prüfbelege einholen. Vier lokale Vorschauen beweisen keine zwölf Veröffentlichungen.

### Exercise 2 — Überlebensverzerrung und Nenner

Welcher Anteil der geplanten Kurse hat eine geprüfte, erfolgreiche lokale Vorschau? Ist das die öffentliche Veröffentlichungsrate?

> **Answer:** 4/12 = 1/3 = 33,3 %. Die acht ungeprüften Kurse bleiben im Nenner der geplanten Kurse. Für keinen der zwölf ist hier eine Veröffentlichung bestätigt: Eine URL ergab 404, elf wurden nicht geprüft. Weder 4/4 noch 4/12 ist eine gemessene Veröffentlichungsrate.

### Exercise 3 — Anker bei 80 %

Die erste Schätzung lautete 80 % Bereitschaft. Tragen die Daten diese Zahl?

> **Answer:** Nein. Nur 4/12 lokale Vorschauen bestanden; 1/12 öffentliche URLs wurde geprüft und ergab 404. Diese Werte definieren und belegen keine 80 %. Zuerst eine Regel für Quellprüfungen, Prüfbelege und öffentliche Abrufe jeder erforderlichen Sprache festlegen; dann Zähler und Nenner messen.

### Exercise 4 — Verfügbarkeit nach einem 404

Jemand erinnert sich lebhaft an den 404 und will alle künftigen Releases dauerhaft stoppen. Was vermeidet diese Verallgemeinerung?

> **Answer:** URL, Zeitpunkt und ausgelieferte Revision festhalten; die elf anderen URLs prüfen und nach der Korrektur erneut testen. Ein Abruf schätzt keine systemweite Fehlerrate. Die betroffene Veröffentlichung bis zum erfolgreichen Abruf sperren; künftige Kontrollen anhand gemessener Grundrate und Ursachen wählen.

### Exercise 5 — Versunkene Kosten und künftiger Nutzen

Nach acht Monaten Arbeit prognostiziert der Fall zwei Stunden Nutzen und fünf Stunden Wartung pro Woche. Welche Entscheidung folgt aus diesen Annahmen?

> **Answer:** Die *prognostizierte* Bilanz beträgt 2 − 5 = −3 Stunden pro Woche. Die vergangenen acht Monate verbessern diese künftige Bilanz nicht. Den breiten Rollout pausieren, Prognose und Nutzwert in einem kleinen reversiblen Pilotversuch prüfen und nur bei neuer positiver Evidenz fortfahren. Das sind keine beobachteten GA-Kosten.

**Transferkriterium:** Vorschau, Prüfung und öffentlichen Abruf unterscheiden; 4/12 berechnen; eine Beobachtung nennen, die die Veröffentlichungsbehauptung widerlegt. Die separate Lernaufgabe enthält keine Antworten.

---

## Forschungsgrundlage

- Taxonomie kognitiver Verzerrungen nach Daniel Kahneman, *Schnelles Denken, langsames Denken* (2011)
- Dunning-Kruger-Effekt nach Kruger & Dunning, „Unskilled and Unaware of It" (1999)
- Versunkene-Kosten-Forschung nach Arkes & Blumer, „The Psychology of Sunk Cost" (1985)
- Überlebensverzerrung nach Abraham Walds Analyse der Flugzeugpanzerung im Zweiten Weltkrieg
- Ankerexperimente nach Tversky & Kahneman, „Judgment Under Uncertainty" (1974)
- Die Governance-Beispiele beziehen sich auf Demerzels hexavalente Logik sowie Rollback-, Kaizen- und Belief-Currency-Politiken; eine Wirkung auf menschliche Verzerrungen wurde hier nicht gemessen
- Überzeugungszustand: T(0.85) F(0.02) U(0.10) C(0.03)
