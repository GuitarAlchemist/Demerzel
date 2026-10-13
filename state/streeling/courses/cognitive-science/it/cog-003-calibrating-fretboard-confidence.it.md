---
module_id: cog-003-calibrating-fretboard-confidence
department: cognitive-science
course: "Calibrare la sicurezza nel riconoscere le note sulla tastiera"
level: intermediate
prerequisites: [cog-002-feedback-integrity-fretboard-recall]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-12-003
version: "0.1.0"
---

# Calibrare la sicurezza nel riconoscere le note sulla tastiera

> **Dipartimento di Scienze Cognitive** | Livello intermedio | 40 minuti | Bozza italiana; revisione e pubblicazione in attesa

## Obiettivi

Trasformerai «ne sono sicuro» in una probabilità registrata **prima** del feedback, calcolerai il punteggio di Brier binario su una chiave di risposta GA verificata, distinguerai sei esempi inventati da risultati misurati su studenti e progetterai un test che potrebbe confutare un'ipotesi di calibrazione. [COG-002 (in inglese)](../en/cog-002-feedback-integrity-fretboard-recall.md) controlla la chiave visualizzata. Qui chiediamo: **la sicurezza dichiarata corrisponde alla frequenza delle risposte corrette?**

## La decisione del progetto

Immagina un esercizio GA «nomina questa nota» sulla tastiera SVG. Due chitarristi identificano correttamente quattro posizioni su sei. Uno dichiara poca sicurezza sulle due risposte errate, l'altro ne è convinto. La precisione grezza li mette alla pari, ma potrebbero aver bisogno di suggerimenti diversi. Per scegliere occorrono un evento definito, una chiave affidabile e una prova dell'effetto del feedback su veri studenti.

Al commit GA [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), la [pagina dimostrativa](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) elenca sei posizioni. Il [componente SVG](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) usa `string: 0` per il Mi cantino, tasto 0 per la corda a vuoto e accordatura predefinita `E, B, G, D, A, E` dall'acuto al grave. La pagina non cambia tale accordatura. La sesta posizione mostra **C** alla corda 5, tasto 3, mentre il Mi grave al terzo tasto è **G**. È una discrepanza del codice, non un'osservazione sugli utenti. La sequenza corretta, nell'ordine della pagina, è `E, C, G, E, C, G`.

La pagina si definisce test di un vecchio componente SVG. Il [gestore del clic](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) invia solo corda e tasto. Le fonti non mostrano inserimento di sicurezza, sessione valutata, pannello di calibrazione o corso pubblicato. **Tutte le risposte degli studenti qui sotto sono dati sintetici per esercitarsi.**

## 1. Definisci la previsione prima di rivelare la risposta

Per ogni prova, chiedi una nota `a_i` a una corda e a un tasto specifici, poi `p_i`, da 0 a 1: «Quanto è probabile che **la nota che ho scelto** coincida con la chiave verificata indipendentemente?». Si valuta la correttezza della scelta, non la probabilità che la chitarra suoni o che l'etichetta della demo sia affidabile. Registra `a_i` e `p_i` prima di svelare il nome della nota; poi poni `y_i=1` se la scelta coincide con la chiave e `y_i=0` altrimenti.

Per ottenere una chiave utilizzabile, conserva ordine delle corde, accordatura, tasto e revisione della fonte. Il Mi grave è la corda 5; E ha classe d'altezza 4. Al terzo tasto `(4+3) mod 12=7`, cioè G. Il C mostrato non può diventare la risposta corretta senza la rettifica documentata in COG-002.

L'interfaccia avrebbe bisogno di input **nuovi** per nota e sicurezza; il clic attuale porta solo una coordinata. Un registro proposto è `{source_sha, tuning, string, fret, chosen_note, confidence_before_feedback, verified_note, answer_time, feedback_time}`: progetto di studio, **non** API GA esistente. Occorre anche nascondere la risposta fino a dopo `p_i`, perché i marcatori attuali mostrano etichette visibili.

### Esercizio 1 — Definisci l'evento

Uno studente sceglie C alla corda 5, tasto 3, con `p=0.9`. Qual è la nota verificata, quanto vale `y` e il clic attuale registra `p`?

> **Risposta:** La corda 5 è il Mi grave. `(4+3) mod 12=7` dà G, dunque per C `y=0`. Il clic contiene soltanto `{string, fret}`, senza nota scelta o sicurezza. La risposta con `p=0.9` è ipotetica.

## 2. Valuta sei prove dichiaratamente inventate

Il **punteggio di Brier binario** è `BS=(1/n) Σ_i (p_i-y_i)^2`. Va da 0 a 1 e **più basso è meglio**. A differenza del conteggio di risposte corrette, distingue un errore con sicurezza 0.9 da uno con 0.6. Usa sempre la stessa definizione dell'esito. Le sei scelte e probabilità seguenti sono **inventate**; solo coordinate, accordatura e chiave corretta vengono da GA.

| Prova | Corda, tasto | Nota verificata | Scelta fittizia | `p_i` | `y_i` | `(p_i-y_i)^2` |
|---:|---|---|---|---:|---:|---:|
| 1 | 0, 0 | E | E | 0.9 | 1 | 0.01 |
| 2 | 1, 1 | C | C | 0.8 | 1 | 0.04 |
| 3 | 2, 0 | G | A | 0.7 | 0 | 0.49 |
| 4 | 3, 2 | E | E | 0.6 | 1 | 0.16 |
| 5 | 4, 3 | C | C | 0.9 | 1 | 0.01 |
| 6 | 5, 3 | G | C | 0.9 | 0 | 0.81 |

Lo studente fittizio indovina `4/6≈0.6667`. Le perdite sommano `0.01+0.04+0.49+0.16+0.01+0.81=1.52`, dunque `BS=1.52/6≈0.2533`. Questi numeri **non** stimano le capacità di una persona reale. Se per errore si valutasse la prova 6 usando il C mostrato, la perdita scenderebbe da 0.81 a 0.01 e il punteggio apparente diventerebbe `(1.52-0.81+0.01)/6=0.12`. Una buona regola di punteggio non ripara una chiave sbagliata.

### Esercizio 2 — Calcola il punteggio

Calcola precisione grezza, somma delle perdite quadratiche e media di Brier. Quale errore contribuisce di più?

> **Risposta:** Quattro su sei sono corretti: `4/6≈0.6667`. La somma è `1.52`, la media `1.52/6≈0.2533`. La prova 6 contribuisce `0.81`, più dello `0.49` della prova 3, perché l'errore aveva sicurezza 0.9 invece di 0.7.

### Esercizio 3 — Controlla una fascia di sicurezza

Fra le prove con `p_i=0.9`, quale quota è corretta e quanto dista da 0.9? Tre prove bastano a stabilire una calibrazione individuale stabile?

> **Risposta:** Prove 1, 5 e 6: due corrette, cioè `2/3≈0.6667`. La distanza è `0.9-2/3≈0.2333`. Tre prove inventate e correlate sono troppo poche per una curva individuale stabile.

### Esercizio 4 — Scopri la contaminazione della chiave

Se la prova 6 fosse valutata contro il C visualizzato invece del G verificato, come cambierebbero esito, perdita e media? Sarebbe prova di un apprendimento migliore?

> **Risposta:** La scelta C sarebbe segnata `y_6=1`; la perdita passerebbe da `(0.9-0)^2=0.81` a `(0.9-1)^2=0.01`. La somma diventerebbe `0.72` e la media `0.72/6=0.12`. La previsione non cambia: il miglioramento apparente deriva dalla chiave errata.

## 3. Perché usare l'errore quadratico?

Sia `q` la probabilità reale che una risposta scelta sia corretta in una data classe di prove future, e `p` quella dichiarata. La perdita attesa di Brier è `q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q)`. Il secondo termine non dipende da `p`: la perdita attesa ha minimo unico in `p=q`. La regola premia quindi probabilità oneste **in media attesa**, non garantisce il risultato migliore in ogni gruppo di sei prove. Non diagnostica neppure se un errore derivi da ordine delle corde, dimenticanza o feedback fuorviante.

Nell'esempio ipotetico `q=0.7`, dichiarare `p=0.7` dà `0.7(0.3)^2+0.3(0.7)^2=0.21` di perdita attesa; `p=0.9` dà `0.7(0.1)^2+0.3(0.9)^2=0.25`. L'eccesso di 0.04 equivale a `(0.9-0.7)^2`. Le sei prove inventate **non** misurano `q=0.7` fra i chitarristi reali.

Un Brier minore non significa necessariamente maggiore conoscenza musicale. Spostare ogni risposta verso 0.5 può ridurre la penalità di errori sicuri senza riconoscere più note. Riporta anche precisione, risultati per corda e tasto e probabilità originali **prima** del feedback. Riscrivere `p_i` dopo il feedback invalida la misura della previsione iniziale.

### Esercizio 5 — Verifica la direzione della regola

Con `q=0.7` ipotetico, confronta le perdite attese per `p=0.7` e `p=0.9`. Quale è minore e di quanto?

> **Risposta:** Con `p=0.7`, `0.7(1-0.7)^2+0.3(0.7)^2=0.21`; con `p=0.9`, `0.7(1-0.9)^2+0.3(0.9)^2=0.25`. La prima è minore di 0.04. Le sei prove didattiche non hanno misurato `q`.

## 4. Progetta uno studio che possa fallire

Ipotesi falsificabile: **mostrare feedback esplicito sulla calibrazione della sicurezza dopo ogni risposta verificata ridurrà il Brier del giorno seguente su posizioni tenute da parte senza peggiorare la precisione delle note**, rispetto a mostrare solo la nota corretta. Entrambi i gruppi devono scegliere una nota e dichiarare sicurezza prima del feedback. Il gruppo di calibrazione potrebbe vedere sicurezza, correttezza e punteggio cumulativo; quello di confronto la stessa nota e correttezza, ma nessun riepilogo della sicurezza. È un esperimento proposto, non una funzione GA attuale.

Prima correggi l'etichetta sbagliata o usa una chiave verificata a parte. Prepara due stati della domanda senza etichette di nota, con la stessa accordatura, e accertati che la risposta non appaia prima della previsione. Coinvolgi studenti reali, registra consenso ed esperienza, poi assegna i gruppi prima della pratica. Bilancia i set di posizioni e riservane altri al test del giorno seguente. Registra revisione della fonte, domanda, risposta, sicurezza, tempi di risposta e feedback mostrato, e intervallo esatto. Riconoscere una coordinata disegnata non dimostra saper suonare o sentire la nota.

Dichiara in anticipo l'esito principale: Brier medio il giorno seguente sulle posizioni riservate, con precisione delle note come vincolo. L'ipotesi **non è sostenuta** se il feedback di calibrazione non riduce tale Brier rispetto al confronto, oppure se un miglioramento del punteggio comporta meno risposte corrette secondo il vincolo prefissato. Riporta incertezza, numero di studenti e domande. Un test pilota può rivelare incomprensioni dell'interfaccia o un effetto soffitto e richiedere uno studio diverso, non un successo dichiarato dopo. **Nessuno** studente, assegnazione, variante o dato del giorno seguente è stato raccolto per la lezione.

### Esercizio 6 — Indica una confutazione

Un agente dice: «Il Brier fittizio `0.2533` prova che il nostro feedback migliora il ricordo». Perché non è giustificato? Dai due motivi e un risultato dello studio che smentirebbe l'ipotesi.

> **Risposta:** Le sei probabilità e risposte sono inventate; la pagina GA non offre l'intervento sulla sicurezza né misura il giorno dopo. L'ipotesi fallirebbe se il gruppo di calibrazione non ottenesse un Brier inferiore sulle posizioni riservate, oppure se il punteggio migliore si accompagnasse a minore precisione secondo il vincolo dichiarato. Servono chiave corretta e probabilità registrate prima del feedback.

## Limite delle prove

Le fonti GA fissate mostrano sei coordinate, ordine delle corde, etichette visibili e dati del clic. La chiave corretta e i conti di Brier sono verificabili. Le sei scelte e probabilità, `q=0.7`, le varianti UI e lo studio sono costruzioni didattiche. Non risultano sicurezza di utenti reali, miglioramento della calibrazione, beneficio dell'intervento, esecuzione nel browser, revisione della materia o linguistica, build Learn o lettura pubblica. Occorrono prove e revisori distinti prima di chiamare questa bozza corso revisionato o pubblicato.
