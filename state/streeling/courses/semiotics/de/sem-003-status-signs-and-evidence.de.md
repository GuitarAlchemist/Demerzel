---
module_id: sem-003-status-signs-and-evidence
department: semiotics
course: "Statuszeichen und Belege in der Agentenarbeit"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-12-003
version: "0.1.0"
---

# Statuszeichen und Belege in der Agentenarbeit

> **Fachbereich Semiotik** | Niveau: Mittelstufe | Phase: Albedo | Dauer: 35 Minuten | Deutscher Entwurf, Prüfung ausstehend

## Lernziele

Du lernst, ein Statuswort von dem Ereignis zu unterscheiden, das es angeblich bezeichnet, einen Streeling-Produktionsdatensatz zu lesen, ohne eine begrenzte Prüfung als abschließendes Urteil auszugeben, und eine überprüfbare Übergabe zwischen Agenten mit einem festen Quellartefakt zu verfassen. Außerdem unterscheidest du, was ein Schema, ein lokaler Build und ein öffentlicher Abruf jeweils belegen.

## Die Projektentscheidung

Ein Agent hat eine Streeling-Lektion entworfen. Ein anderer meldet nach Lektüre von Quelltext und Antworten „keine Befunde“. Was soll die koordinierende Person dem nächsten Agenten mitteilen: **Entwurf**, **bereit**, **geprüft** oder **veröffentlicht**? Davon hängt ab, ob Lernende zu einem öffentlichen Kurs geleitet, Prüfende um Durchsicht gebeten oder Autorinnen und Autoren zur Überarbeitung aufgefordert werden. Ein zu starkes Wort kann eine noch offene Hürde überspringen.

Diese Lektion nutzt den echten [SEM-002-Produktionsdatensatz](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/course-productions/cp-semiotics-2026-10-11-002.json), den [Bericht zur begrenzten KI-Prüfung](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/sem-002-subject-review-2026-10-11.md), das [Produktionsschema](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/schemas/course-production.schema.json) und den [Fortschrittsbericht-Generator](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py). Alle Demerzel-Quelllinks zeigen auf Commit `c453a91d1c4d913af72c28779eff826659c1d654`. Wir untersuchen diesen Stand und behaupten nicht, dass Produktion oder Website heute noch denselben Stand haben.

## 1. Worauf verweist ein Statuszeichen?

[SEM-001 (Englisch)](../en/sem-001-signs-in-governance.md) führt Zeichen, Gegenstand und Deutung ein. In einer Agentenübergabe ist `reviewed` ein **Symbol**: Seine Bedeutung beruht auf einer gemeinsamen Konvention. Ein Link zum Prüfbericht kann als **Index** auf ein bestimmtes Artefakt zeigen. Ein grünes Häkchen ist ebenfalls ein kompaktes Zeichen, benötigt aber eine vereinbarte Bedeutung, ein benanntes Prüfkriterium und Herkunftsangaben. Keines dieser Zeichen führt selbst eine Prüfung durch.

Die eingangs genannten Wörter bezeichnen mögliche Aussagen, **keine** neue Streeling-Zustandsmaschine:

| Wort in der Nachricht | Mögliche überprüfbare Aussage | Erforderlicher Beleg für eine unqualifizierte Verwendung |
| --- | --- | --- |
| `draft` | Eine Quelldatei existiert | Pfad und genaue Revision |
| `ready` | Eine definierte Eingangshürde wurde erfüllt | Hürde, Eingaben, Ergebnis und Datum; bereit *wofür*? |
| `reviewed` | Eine prüfende Person hat einen festgelegten Umfang untersucht | Prüfbericht, Person, Umfang, Ergebnis und offene Prüfungen |
| `published` | Lernende können die beabsichtigte Version abrufen | Bereitgestellte Route, anonymer Abruf und passende Quellherkunft |

Das sind **Kommunikationstests**, keine vier implementierten Enum-Werte. Das fixierte Schema erlaubt `in_progress`, `review_pending`, `published`, `rejected` und `failed`, aber nicht `draft`, `ready` oder `reviewed`. Je nach Beleg sollte man sagen „englischer Entwurf vorhanden“ oder „bereit für begrenzte Quellenprüfung“, statt einen nicht vorhandenen Schemaübergang anzudeuten.

### Übung 1 — Benenne den Gegenstand

Eine Übergabe lautet nur „SEM-002 ist bereit“. Nenne zwei wesentlich verschiedene Bedeutungen von `ready` und formuliere die Aussage für eine davon überprüfbar um. Enthält das Schema `ready`?

> **Antwort:** Gemeint sein kann bereit zur Quellenprüfung oder bereit zur Bereitstellung nach allen Prüfungen. Überprüfbar wäre: „Der englische SEM-002-Quelltext bei Commit `c453a91d1c4d913af72c28779eff826659c1d654` ist **für eine begrenzte Prüfung von Text und Antworten** bereit; abschließende Produktionsprüfung und Veröffentlichung sind noch offen.“ `ready` ist kein Enum-Wert des Schemas.

## 2. Lies zuerst den Datensatz, dann den Bericht

Bei der fixierten Revision steht im SEM-002-Datensatz `status: in_progress`. Forschung, Gliederung und Inhalt sind abgeschlossen; die Übersetzung ist mit `languages: ["en"]` unvollständig; Prüfung und Veröffentlichung haben jeweils `completed: false`. Der gesonderte KI-Bericht meldet **keine Befunde innerhalb der begrenzten Prüfung von Quelltext und Antworten**. Er lässt menschliche Fachprüfung, Lerntest, Sprachprüfung und öffentliche Learn-Prüfung ausdrücklich offen. Die begrenzte Sichtung hat stattgefunden, während die abschließende Prüfphase unvollständig bleibt.

Der semiotische Fehler wäre, `reviewed` auf jeden denkbaren Prüfumfang auszudehnen. „KI-Vorprüfung von Quelle und Antworten ohne Befund“ ist präzise. „Kurs geprüft“ könnte als abschließendes redaktionelles oder menschliches Urteil gelesen werden. Auch der Name einer prüfenden Person reicht nicht: Der Bericht muss geprüfte und ausgeschlossene Bereiche nennen. Ein Produktions-Flag ist zunächst die Behauptung einer Datei; erst ein nachvollziehbarer Beleg macht sie zu einer belastbaren Übergabeinformation.

Der [Fortschrittsbericht-Generator](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py#L89-L107) zählt eine Freigabe nur dann, wenn `phases.review.completed` wahr **und** `phases.review.verdict` gleich `approved` ist. SEM-002 erfüllt dies im fixierten Stand nicht. Der Zähler liest Datensätze; er beurteilt die fachliche Richtigkeit nicht unabhängig. Würde jemand beide Werte ohne vertrauenswürdige Prüfung von Hand eintragen, bewiese die Zahl allein ebenfalls keine Prüfung.

### Übung 2 — Begrenze die Prüfaussage

Welche Übergabe ist für das fixierte SEM-002 vertretbar? (A) „Es gab keine Prüfung“; (B) „Alle Prüfungen sind bestanden“; (C) „Eine begrenzte KI-Prüfung von Quelltext und Antworten fand keine Befunde; die Produktionsprüfphase bleibt unvollständig.“ Begründe, warum die anderen Aussagen scheitern.

> **Antwort:** C. A widerspricht dem Bericht über die begrenzte Prüfung. B überdehnt ihn: menschliche Fach-, Lernenden-, Sprach- und öffentliche Prüfungen stehen noch aus, `phases.review.completed` ist falsch. „Keine Befunde“ gilt nur für den genannten Umfang, nicht für alle möglichen Fehler.

## 3. Gültige Form ist kein nachgewiesener Übergang

Das Schema begrenzt Feldtypen und erlaubte `status`-Zeichenfolgen. Es verlangt Status, Forschung, Gliederung, Inhalt und Zeitstempel. Sind Prüf- und Veröffentlichungsphase vorhanden, müssen ihre `completed`-Felder boolesch sein. Es enthält **keine** allgemeine feldübergreifende Regel wie „`status: published` impliziert `publish.completed: true`“. Ein Datensatz kann damit formal schemagültig sein und dennoch eine widersprüchliche operative Aussage enthalten. Das beschreibt das Schema und beweist nicht, dass solch ein fehlerhafter Datensatz produktiv existiert.

Die fixierte [Kurs-Vorprüfung](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_preflight.py) prüft Schema, Dateinamen, Frontmatter, Dateien der erklärten Sprachen, englische Wortzahl und Signale für beantwortete Übungen. Ihre einzige ausdrückliche Statuskonsistenzregel verlangt bei `in_progress` falsche Abschluss-Flags für Prüfung und Veröffentlichung. Sie ruft weder die öffentliche Website ab noch beurteilt sie die Fachlichkeit. Ein Bestehen heißt weder „von Lernenden genehmigt“ noch „auf Learn verfügbar“.

Stell dir eine **synthetische** Änderung am SEM-002-Datensatz vor: Nur `status` wird auf `published` gesetzt, während `phases.publish.completed: false` bestehen bleibt. Das Schema erlaubt beide Einzelwerte und verknüpft sie nicht. Da die Konsistenzregel der Vorprüfung nur bei `in_progress` greift, würde dieser erfundene Widerspruch gerade dieser Regel entgehen. Trage ihn nicht ins Repository ein. Prüfe vielmehr Datensatz, Bereitstellungsbeleg und anonyme Route, statt dem Wort `published` zu vertrauen.

### Übung 3 — Trenne Form und Wahrheit

Verletzt der synthetische Fall `status: published` mit `phases.publish.completed: false` eine Regel des fixierten JSON-Schemas? Belegt ein gültiges Schemaergebnis die öffentliche Erreichbarkeit von SEM-002?

> **Antwort:** Nein, das Schema verbindet diese beiden Felder nicht. Seine Validierung bestätigt nur die geprüfte Struktur, weder Bereitstellung noch anonymen öffentlichen Zugriff. Der Widerspruch muss untersucht und darf nicht als Veröffentlichung ausgegeben werden.

## 4. Trenne lokale und öffentliche Bezugsobjekte

Der [öffentliche Basisbericht](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/public-baseline-2026-10-11.md) dokumentiert am 11. Oktober 2026 einen anonymen Abruf des Streeling-Indexes, nennt einen Quellcommit und hält fest, dass öffentliche Präsenz keine Autorenprüfung belegt. Damals erzeugte die lokale Learn-Vorprüfung DV-001-Seiten, während anonyme GET-Aufrufe der neuen öffentlichen DV-001-Routen 404 ergaben. „Lokal erzeugte Seite“ verweist auf ein Build-Artefakt; „veröffentlicht“ verweist auf eine abrufbare öffentliche Version. Aus Ersterem folgt Letzteres nicht.

Der Bericht ist ein **historischer DV-001-Befund**, keine aktuelle Prüfung von SEM-002 oder der heutigen Website. Für eine SEM-003-Veröffentlichung müsste man die geplante Route bestimmen, die erzeugte Site bereitstellen, die Route anonym abrufen und Inhalt oder Quell-SHA mit der beabsichtigten Revision vergleichen. HTTP 200 könnte eine ältere Version ausliefern. Der SHA verweist auf den verfassten Stand; der Routenabruf verbindet ihn mit der Ansicht der Lernenden. Der Prüfbericht verweist auf ein anderes Ereignis. Beides ist nicht austauschbar.

### Übung 4 — Was wurde beobachtet?

Im datierten DV-001-Beispiel existiert eine lokale Seite, während die anonyme Route 404 liefert. Welche Aussage trägt der Befund: „Die Lektion wurde veröffentlicht“, „Der lokale Build erzeugte eine Seite, aber diese öffentliche Route lieferte sie am Prüftag nicht aus“, oder „Es gab keine Quelldatei“? Was müsste man nach einer späteren Bereitstellung prüfen?

> **Antwort:** Die mittlere Aussage. Lokale Seite und 404 betreffen am Beobachtungstag verschiedene Oberflächen. Nach der Bereitstellung die vorgesehene Route anonym abrufen und Inhalt oder Herkunfts-SHA mit der gewünschten Revision vergleichen; lokaler Build oder Bereitstellungsbefehl reichen nicht.

## 5. Schreibe eine nutzbare Agentenübergabe

Eine brauchbare Statusmeldung bildet eine kurze Belegkette: **Artefakt und Revision → benannte Prüfung → beobachtetes Ergebnis → offene Hürde → nächste Handlung**. Das ist ein Schreibmuster für diese Übung, **kein neuer normativer DSL**. Empfangende Agenten können den Verweisen folgen und eine veraltete oder zu breite Auslegung zurückweisen. Beispiel aus dem fixierten SEM-002-Stand:

> „Der englische SEM-002-Quelltext existiert in Demerzel bei Commit `c453a91d1c4d913af72c28779eff826659c1d654`. Eine begrenzte KI-Prüfung von Quelle und fünf Antworten meldete keine Befunde. Der Produktionsdatensatz bleibt `in_progress`; Prüfung und Veröffentlichung sind nicht abgeschlossen. Als Nächstes menschliche Fach- und Lernendenprüfung einholen und anschließend die geplante Learn-Bereitstellung durch anonymen Abruf kontrollieren.“

Die Nachricht erfindet keinen `ready`-Enum-Wert. Wenn eine spätere Prüfung nur sachliche Richtigkeit freigibt, muss dieser Umfang genannt und darf nicht stillschweigend auf die Sprache ausgeweitet werden. Ändert sich die Quelle, deckt der alte Prüfbericht den neuen Text nicht automatisch ab. Unveränderliche Revisionslinks verbinden Prüfende, Quelle und öffentlichen Abruf mit demselben Objekt oder machen einen Bruch sichtbar.

### Übung 5 — Repariere eine Agentennachricht

Formuliere „SEM-002 ist geprüft und veröffentlicht; die Tests sind grün“ allein anhand des fixierten Datensatzes und Prüfberichts neu. Nenne eine konkrete nächste Handlung und ein Unbekanntes, ohne Test- oder Bereitstellungsergebnisse zu erfinden.

> **Antwort:** „Bei Demerzel-Commit `c453a91d1c4d913af72c28779eff826659c1d654` hat SEM-002 einen englischen Entwurf und einen Bericht über eine begrenzte KI-Prüfung von Quelltext und Antworten ohne Befunde. Der Datensatz bleibt `in_progress` mit `review.completed=false` und `publish.completed=false`. Diese Artefakte belegen weder einen neuen Testlauf noch einen öffentlichen Abruf der SEM-002-Route. Als Nächstes menschliche Fach- und Lernendenprüfung für diese Revision anfordern.“ Die ursprüngliche Aussage macht aus einer begrenzten Prüfung ein abschließendes Urteil und behauptet Veröffentlichung und Tests ohne Beleg.

## Grenzen und Übertragung

Diese Lektion analysiert fixierte Demerzel-Dateien und einen datierten öffentlichen Bericht. Sie führt keine wirkliche Agentenübergabe, keinen Test mit Lernenden und keine Begutachtung von SEM-003 durch eine menschliche Fachperson für Semiotik durch; sie veröffentlicht den Entwurf nicht. Die fünf Übungen prüfen, ob Lernende Statuswörter mit Bezugsobjekten und Belegen verbinden. Um eine bessere Agentenkoordination zu prüfen, gib in einem kontrollierten Versuch einer Gruppe ein unqualifiziertes Statuswort und einer anderen die Belegkette; vergleiche, ob beide die richtige nächste Hürde und Quellrevision nennen. **Bis ein solcher Versuch stattgefunden hat, bleibt der Nutzen für Übergaben eine Hypothese.**
