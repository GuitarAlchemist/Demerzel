---
module_id: phi-001-how-to-argue-well
department: philosophy
course: "Grundlagen der Philosophie"
level: beginner
prerequisites: []
estimated_duration: "25 minutes"
produced_by: philosophy
version: "1.0.0"
---

# Gut argumentieren — Logik und kritisches Denken

> **Fachbereich Philosophie** | Stufe: Einführung | Dauer: 25 Minuten

## Lernziele

Nach dieser Lektion werden Sie in der Lage sein:
- Die Struktur eines Arguments zu erkennen (Prämissen und Schlussfolgerung)
- Zwischen Gültigkeit und Stichhaltigkeit zu unterscheiden
- Häufige logische Fehlschlüsse zu erkennen
- Schlechte Argumente im Alltag zu entlarven
- Ein wohlstrukturiertes Argument selbst zu formulieren

---

## 1. Was ist ein Argument?

In der Philosophie ist ein „Argument" kein Streitgespräch. Es ist eine strukturierte Menge von Behauptungen:

- **Prämissen** — Aussagen, die als Belege oder Gründe angeboten werden
- **Schlussfolgerung** — die Aussage, die durch die Prämissen gestützt werden soll

**Beispiel:**
- Prämisse 1: Alle Gitarren haben Saiten.
- Prämisse 2: Dieses Instrument ist eine Gitarre.
- Schlussfolgerung: Also hat dieses Instrument Saiten.

Das ist alles. Ein Argument besteht nur aus Prämissen, die zu einer Schlussfolgerung führen. Alles andere — Rhetorik, Emotionen, Lautstärke, Überzeugung — ist Dekoration.

### Wie man das Argument findet

Im Alltag werden Argumente selten sauber aufgelistet. Achten Sie auf Signalwörter:

| Prämissen-Indikatoren | Schlussfolgerungs-Indikatoren |
|---|---|
| Weil, da, denn, angesichts der Tatsache, dass | Daher, also, folglich, demnach |
| Der Grund ist, es folgt aus | Das bedeutet, woraus sich ergibt |
| In Anbetracht dessen, aufgrund von | Wir können schlussfolgern, dass, somit |

**Beispiel aus dem Alltag:** „Wir sollten auf ein neues Framework umsteigen, weil das aktuelle keine Community-Unterstützung hat und drei ungepatchte Sicherheitslücken aufweist."

- Prämisse 1: Das aktuelle Framework hat keine Community-Unterstützung.
- Prämisse 2: Es hat drei ungepatchte Sicherheitslücken.
- Schlussfolgerung: Wir sollten auf ein neues Framework umsteigen.

Nun können Sie jedes Element einzeln bewerten. Sind die Prämissen wahr? Folgt die Schlussfolgerung daraus?

### Übung

Finden Sie einen Meinungsbeitrag, einen Tweet oder eine Slack-Nachricht, die eine Behauptung aufstellt. Identifizieren Sie die Prämissen und die Schlussfolgerung. Schreiben Sie sie im obigen Format auf.

---

## 2. Gültigkeit vs. Stichhaltigkeit

Diese beiden Begriffe bilden die wichtigste Unterscheidung in der Logik:

### Gültigkeit

Ein Argument ist **gültig** (valide), wenn die Schlussfolgerung *notwendigerweise* wahr sein muss, wann immer die Prämissen wahr sind. Es geht um die *Struktur*, nicht den Inhalt.

**Gültig (aber absurd):**
- Prämisse 1: Alle Katzen bestehen aus Käse.
- Prämisse 2: Minka ist eine Katze.
- Schlussfolgerung: Minka besteht aus Käse.

Die Struktur ist einwandfrei. Wenn Katzen *tatsächlich* aus Käse bestünden, würde Minka tatsächlich käsig sein. Das Argument ist gültig, obwohl Prämisse 1 offensichtlich falsch ist.

### Stichhaltigkeit

Ein Argument ist **stichhaltig** (sound), wenn es gültig ist UND alle Prämissen tatsächlich wahr sind.

**Stichhaltig:**
- Prämisse 1: Alle Menschen sind sterblich.
- Prämisse 2: Sokrates ist ein Mensch.
- Schlussfolgerung: Sokrates ist sterblich.

Gültige Struktur + wahre Prämissen = stichhaltiges Argument. Das ist der Goldstandard.

### Warum das wichtig ist

Wenn jemand ein Argument vorbringt, haben Sie zwei separate Fragen:
1. **Ist die Struktur gültig?** Folgt die Schlussfolgerung aus den Prämissen?
2. **Sind die Prämissen wahr?** Stimmen die Belege tatsächlich?

Ein schlechtes Argument kann auf beiden Ebenen scheitern. Viele Meinungsverschiedenheiten in der realen Welt drehen sich eigentlich um die Prämissen (die Fakten), nicht um die Logik (das Schlussfolgern).

---

## 3. Häufige Fehlschlüsse — Die Schurkengalerie

Ein **Fehlschluss** (Trugschluss, lat. *fallacia*) ist ein Argumentationsmuster, das überzeugend aussieht, aber logisch fehlerhaft ist. Hier sind die häufigsten:

### Ad Hominem (Angriff auf die Person)

**Wie es aussieht:** „Man kann ihrer Codebase-Analyse nicht trauen — sie ist erst seit sechs Monaten im Team."

**Warum es falsch ist:** Die Qualität eines Arguments hängt nicht davon ab, wer es vorbringt. Eine Neueinsteigerin kann recht haben; ein Veteran kann irren. Bewerten Sie das Argument, nicht die Person.

**Achten Sie auf:** „Du sagst das ja nur, weil...", „Was wissen *die* schon davon?"

### Strohmann-Argument (Verzerrung des Arguments)

**Wie es aussieht:** Person A sagt: „Wir sollten Eingabevalidierung zur API hinzufügen." Person B antwortet: „Du willst also alle Benutzereingaben blockieren? Das würde das Produkt unbenutzbar machen."

**Warum es falsch ist:** Person B greift eine verzerrte Version von Person As Argument an. Niemand hat „alle Eingaben blockieren" gesagt. Das macht es leicht, gegen eine Position zu „gewinnen", die niemand tatsächlich vertritt.

**Achten Sie auf:** „Also, was du *eigentlich* sagst, ist..."

### Falsches Dilemma (Nur zwei Möglichkeiten)

**Wie es aussieht:** „Entweder wir liefern diese Funktion bis Freitag, oder wir verlieren den Kunden für immer."

**Warum es falsch ist:** Es gibt fast immer mehr als zwei Optionen. Man könnte eine Teilversion liefern, eine neue Frist verhandeln oder das zugrundeliegende Anliegen des Kunden auf andere Weise adressieren.

**Achten Sie auf:** „Entweder... oder...", wenn die Optionen nicht tatsächlich erschöpfend sind.

### Autoritätsargument (Vertrauen wegen Status)

**Wie es aussieht:** „Der Geschäftsführer denkt, wir sollten diese Datenbank verwenden, also muss es die richtige Wahl sein."

**Warum es falsch ist:** Autorität ist kein Beweis. Der Geschäftsführer versteht vielleicht nichts von Datenbanken. Was zählt, ist die *Begründung und Evidenz*, nicht wer es gesagt hat.

**Nuance:** Expertenmeinungen *sind* Belege, wenn der Experte innerhalb seines Fachgebiets spricht. Ein Datenbankingenieur, der eine Datenbank empfiehlt, hat mehr Gewicht als ein Geschäftsführer, der dasselbe tut. Der Fehlschluss besteht darin, Autorität als *Ersatz* für Evidenz zu behandeln statt als *Quelle* davon.

### Argumentum ad Populum (Alle denken das)

**Wie es aussieht:** „Dieses JavaScript-Framework hat 80.000 GitHub-Sterne, also muss es gut sein."

**Warum es falsch ist:** Popularität ist kein verlässlicher Indikator für Qualität. Viele beliebte Dinge sind mittelmäßig; viele ausgezeichnete Dinge sind unbekannt.

### Dammbruch-Argument (Wenn A, dann Z)

**Wie es aussieht:** „Wenn wir freitags Homeoffice erlauben, wird bald niemand mehr ins Büro kommen, und die Unternehmenskultur wird zusammenbrechen."

**Warum es falsch ist:** Jeder Schritt in der Kette braucht seine eigene Begründung. A führt nur dann zu B, wenn man zeigen kann, *warum* es zu B führt. Einfach eine Kette von Konsequenzen zu behaupten, ist kein Argument.

### Übung

Achten Sie in den nächsten 24 Stunden auf Fehlschlüsse in Gesprächen, Meetings, Nachrichten oder sozialen Medien. Versuchen Sie, mindestens ein Beispiel für jeden der obigen Typen zu finden. Schreiben Sie auf, was gesagt wurde und welchen Fehlschluss es darstellt.

---

## 4. Wie man schlechte Argumente erkennt

Hier ist eine schnelle Checkliste, die Sie mental auf jedes Argument anwenden können:

1. **Die Schlussfolgerung finden.** Was genau wird behauptet?
2. **Die Prämissen finden.** Welche Gründe werden angeführt?
3. **Die Struktur prüfen.** Folgt die Schlussfolgerung aus den Prämissen? (Gültigkeit)
4. **Die Prämissen prüfen.** Sind sie tatsächlich wahr? Welche Belege stützen sie? (Stichhaltigkeit)
5. **Auf Fehlschlüsse prüfen.** Stützt sich das Argument auf einen logischen Trick statt auf echte Begründung?
6. **Auf fehlende Informationen prüfen.** Was wird *nicht* gesagt? Welche Annahmen sind versteckt?

**Warnsignale:**
- Emotionale Sprache, die die Arbeit leistet, die Evidenz leisten sollte
- Vage Behauptungen, die nicht überprüfbar sind (siehe PM-001 zum BS-Test)
- Argumente, die Menschen angreifen statt Ideen
- „Jeder weiß" oder „Es ist offensichtlich" als Prämissen
- Falsche Dringlichkeit („Wir müssen JETZT entscheiden") unterbindet die Analyse

---

## 5. Wie man gute Argumente formuliert

Ein gutes Argument zu formulieren ist das Gegenstück zum Erkennen eines schlechten:

### Schritt 1: Formulieren Sie Ihre Schlussfolgerung klar

Sagen Sie, wofür Sie argumentieren. Ohne Absicherung, ohne es am Ende zu verstecken.

„Ich denke, wir sollten das Authentifizierungsmodul neu schreiben."

### Schritt 2: Liefern Sie Prämissen, die sie tatsächlich stützen

Jede Prämisse sollte unabhängig überprüfbar und direkt relevant sein.

- „Das aktuelle Modul hatte 12 Sicherheitsvorfälle im letzten Jahr."
- „Der Code wurde für ein Framework geschrieben, das wir nicht mehr verwenden."
- „Ein Neubau würde geschätzt 3 Wochen dauern; Flicken würde über die nächsten 6 Monate länger dauern."

### Schritt 3: Gegenargumente adressieren

Die stärksten Argumente nehmen den besten Einwand dagegen vorweg.

„Der offensichtliche Einwand ist, dass Neuschreiben riskant ist und oft länger dauert als geschätzt. Dem habe ich begegnet, indem ich den Umfang auf Authentifizierung beschränkt und einen 50%-Zeitpuffer eingeplant habe."

### Schritt 4: Ehrlich mit Unsicherheit umgehen

Wenn Sie sich bei einer Prämisse nicht sicher sind, sagen Sie es. Das ist keine Schwäche — es ist intellektuelle Integrität.

„Bei der Anzahl der Sicherheitsvorfälle bin ich sicher (sie steht in unseren Protokollen). Die Neubau-Schätzung ist weniger sicher — sie geht davon aus, dass es keine Überraschungen gibt, was optimistisch ist."

### Übung

Wählen Sie eine Entscheidung, vor der Sie gerade stehen (bei der Arbeit, in einem Projekt, im Leben). Schreiben Sie ein strukturiertes Argument für Ihre bevorzugte Option nach den vier Schritten oben. Schreiben Sie dann das beste Gegenargument, das Sie finden können. Übersteht Ihr ursprüngliches Argument die Prüfung?

---

## Schlüsselbegriffe

| Begriff | Definition |
|---------|-----------|
| Argument | Eine Menge von Prämissen, die zur Stützung einer Schlussfolgerung angeboten werden |
| Prämisse | Eine Aussage, die als Beleg oder Grund angeboten wird |
| Schlussfolgerung | Die Behauptung, die durch die Prämissen gestützt werden soll |
| Gültigkeit | Die Schlussfolgerung eines Arguments folgt notwendig aus seinen Prämissen |
| Stichhaltigkeit | Ein Argument ist gültig und alle seine Prämissen sind wahr |
| Fehlschluss | Ein Argumentationsmuster, das überzeugend erscheint, aber logisch fehlerhaft ist |
| Ad Hominem | Angriff auf die Person statt auf das Argument |
| Strohmann | Verzerrung eines Arguments, um es leichter angreifbar zu machen |
| Falsches Dilemma | Darstellung von nur zwei Optionen, wenn mehr existieren |

---

## Selbstüberprüfung

**1. Ist dieses Argument gültig? „Alle Vögel können fliegen. Pinguine sind Vögel. Also können Pinguine fliegen."**
> Ja, es ist gültig — die Schlussfolgerung folgt aus den Prämissen. Aber es ist nicht stichhaltig, weil die erste Prämisse falsch ist (nicht alle Vögel können fliegen). Das zeigt, warum Gültigkeit allein nicht ausreicht.

**2. Jemand sagt: „Du kannst diese Politik nicht kritisieren — du hast nie im öffentlichen Dienst gearbeitet." Welcher Fehlschluss ist das?**
> Ad Hominem. Die Qualität der Kritik hängt nicht vom Hintergrund des Kritikers ab. Das Argument sollte nach seinen eigenen Verdiensten bewertet werden.

**3. Was ist der Unterschied zwischen einem gültigen und einem stichhaltigen Argument?**
> Ein gültiges Argument hat eine korrekte logische Struktur — wenn die Prämissen wahr wären, müsste die Schlussfolgerung wahr sein. Ein stichhaltiges Argument ist gültig UND hat Prämissen, die tatsächlich wahr sind. Stichhaltigkeit ist der höhere Standard.

**4. „Entweder führen wir KI-Governance ein oder wir haben gar keine Governance." Was ist daran falsch?**
> Falsches Dilemma. Es gibt viele Formen von Governance zwischen „KI-Governance" und „keine Governance." Das Argument verengt die Optionen künstlich.

**Bestanden-Kriterien:** Prämissen und Schlussfolgerungen in einem Argument aus der Praxis identifizieren, mindestens vier Fehlschlüsse korrekt klassifizieren und ein strukturiertes Argument mit Gegenargument-Berücksichtigung formulieren können.

---

## Forschungsgrundlage

- Argumentstruktur und Gültigkeit/Stichhaltigkeit nach Irving Copi & Carl Cohen, *Introduction to Logic* (Standardwerk)
- Fehlschluss-Taxonomie basierend auf Aristoteles' *Sophistischen Widerlegungen* und aktualisiert durch Douglas Walton, *Informal Logic* (1989)
- Pädagogik des kritischen Denkens nach Richard Paul & Linda Elder, *Critical Thinking* (2001)
- Relevanz für KI-Governance: Die tetravalente Logik (T/F/U/C) erweitert das klassische Wahr/Falsch um Unsicherheit und Widerspruch — siehe Verzeichnis logic/
- Überzeugungszustand: T(0.88) F(0.02) U(0.07) C(0.03)
