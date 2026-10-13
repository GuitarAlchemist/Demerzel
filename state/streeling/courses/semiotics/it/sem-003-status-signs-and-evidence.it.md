---
module_id: sem-003-status-signs-and-evidence
department: semiotics
course: "Segni di stato e prove nel lavoro degli agenti"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-12-003
version: "0.1.0"
---

# Segni di stato e prove nel lavoro degli agenti

> **Dipartimento di Semiotica** | Livello: intermedio | Fase: Albedo | Durata: 35 minuti | Bozza italiana in attesa di revisione

## Obiettivi

Imparerai a distinguere una parola di stato dall'evento che pretende di rappresentare, a leggere una scheda di produzione Streeling senza trasformare un controllo circoscritto in un verdetto finale e a scrivere un passaggio di consegne fra agenti verificabile rispetto a un artefatto fissato. Distinguerai inoltre ciò che dimostrano uno schema, una compilazione locale e una lettura pubblica.

## La decisione del progetto

Un agente ha preparato una lezione Streeling; un altro, dopo aver letto sorgente e risposte, riferisce «nessun rilievo». Che cosa dovrebbe comunicare il coordinatore all'agente successivo: **bozza**, **pronto**, **revisionato** o **pubblicato**? La parola può indirizzare uno studente verso una pagina pubblica, un revisore verso il testo o l'autore verso una correzione. Una formulazione troppo forte può far saltare una verifica ancora aperta.

Questa lezione usa la vera [scheda di produzione SEM-002](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/course-productions/cp-semiotics-2026-10-11-002.json), il relativo [resoconto di revisione IA circoscritta](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/sem-002-subject-review-2026-10-11.md), lo [schema di produzione](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/schemas/course-production.schema.json) e il [reporter di avanzamento](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py). Tutti i link alle fonti Demerzel fissano il commit `c453a91d1c4d913af72c28779eff826659c1d654`. Analizziamo quell'istantanea senza sostenere che lo stato odierno della produzione o del sito sia identico.

## 1. Che cosa rappresenta un segno di stato?

[SEM-001 (in inglese)](../en/sem-001-signs-in-governance.md) introduce segno, oggetto e interpretazione. In un passaggio di consegne `reviewed` è un **simbolo**, il cui senso dipende da una convenzione condivisa. Un link al resoconto può fungere da **indice** verso un preciso artefatto. Una spunta verde è un altro segno compatto, ma richiede un significato concordato, un predicato nominato e una provenienza. Nessuno di questi segni, da solo, svolge una revisione.

Le parole iniziali indicano possibili affermazioni, **non** una nuova macchina a stati Streeling:

| Parola nel messaggio | Possibile affermazione verificabile | Prova richiesta per usarla senza precisazioni |
| --- | --- | --- |
| `draft` | Esiste un file sorgente | Percorso e revisione esatta |
| `ready` | È stato superato un controllo d'ingresso definito | Controllo, input, risultato e data; pronto *per cosa*? |
| `reviewed` | Un revisore ha esaminato un ambito dichiarato | Resoconto, revisore, ambito, esito e revisioni mancanti |
| `published` | Lo studente può recuperare la versione prevista | Percorso distribuito, lettura anonima e provenienza della fonte corrispondente |

Questi sono **test di comunicazione**, non quattro valori implementati nel repository. Lo schema fissato ammette `in_progress`, `review_pending`, `published`, `rejected` e `failed`, non `draft`, `ready` o `reviewed`. È più esatto dire «esiste una bozza inglese» o «pronto per una revisione limitata della fonte», secondo le prove, senza suggerire una transizione dello schema inesistente.

### Esercizio 1 — Indica l'oggetto

Un passaggio di consegne dice solo «SEM-002 è pronto». Indica due significati sostanzialmente diversi di `ready` e riscrivi la frase rendendone verificabile uno. `ready` è fra i valori dello schema?

> **Risposta:** Può significare pronto per la revisione del sorgente oppure pronto per la distribuzione dopo tutte le revisioni. Per esempio: «La fonte inglese SEM-002 al commit `c453a91d1c4d913af72c28779eff826659c1d654` è pronta **per una revisione circoscritta del testo e delle risposte**; revisione finale di produzione e pubblicazione restano incomplete». Lo schema non comprende `ready`.

## 2. Leggi prima la scheda, poi il resoconto

Alla revisione fissata la scheda SEM-002 dice `status: in_progress`. Ricerca, scaletta e contenuto sono completi; la traduzione è incompleta con `languages: ["en"]`; revisione e pubblicazione hanno `completed: false`. Il resoconto IA separato dice **nessun rilievo nel perimetro circoscritto di fonte e risposte**. Restano espressamente aperte le verifiche umane della materia, degli studenti, delle lingue e del Learn pubblico. Un'ispezione circoscritta può essere avvenuta mentre la fase finale di revisione resta incompleta.

L'errore semiotico sarebbe far includere a `reviewed` qualunque possibile revisione. «Il controllo preliminare IA di fonte e risposte non ha trovato rilievi» è preciso. «Corso revisionato» può essere interpretato come approvazione editoriale o umana finale. Il nome del revisore non basta: il resoconto deve dire cosa è stato controllato e cosa è stato escluso. Un flag nella scheda è una dichiarazione di un file; serve una prova rintracciabile perché diventi un fatto affidabile nel passaggio.

Il [reporter di avanzamento](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py#L89-L107) conta l'approvazione solo se `phases.review.completed` è vero **e** `phases.review.verdict` è `approved`. SEM-002 non soddisfa tale condizione nell'istantanea. Il conteggio legge le schede: non valuta autonomamente l'accuratezza della materia. Anche se qualcuno scrivesse a mano quei valori senza una revisione affidabile, il numero non dimostrerebbe che essa sia avvenuta.

### Esercizio 2 — Delimita l'affermazione

Per il SEM-002 fissato scegli: (A) «Non si è svolta alcuna revisione»; (B) «Il corso ha superato tutte le revisioni»; (C) «Un controllo IA circoscritto di fonte e risposte non ha trovato rilievi; la fase di revisione della produzione resta incompleta». Spiega gli errori delle altre due.

> **Risposta:** C. A contraddice il resoconto del controllo limitato. B va oltre il suo perimetro: verifiche umane di materia, studenti, lingue e sito pubblico restano aperte, e `phases.review.completed` è falso. «Nessun rilievo» riguarda solo l'ambito dichiarato, non ogni possibile difetto.

## 3. Una forma valida non equivale a una transizione verificata

Lo schema limita tipi dei campi e valori ammessi per `status`. Richiede stato, ricerca, scaletta, contenuto e data/ora. Se sono presenti le fasi di revisione e pubblicazione, i rispettivi campi `completed` sono booleani. **Non** codifica una regola fra campi come «`status: published` implica `publish.completed: true`». Quindi una scheda può essere valida per lo schema e contenere una dichiarazione operativa contraddittoria. È un limite dello schema, non la prova che esista una scheda difettosa in produzione.

Il [precontrollo dei corsi](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_preflight.py) verifica schemi, nomi dei file, frontmatter, file delle lingue dichiarate, numero di parole inglesi e segnali di esercizi con risposta. La sua unica regola esplicita di coerenza dello stato richiede che `in_progress` abbia falsi i flag di revisione e pubblicazione. Non interroga il sito pubblico né giudica il contenuto. Superarlo non significa «approvato dagli studenti» o «online su Learn».

Immagina una modifica **sintetica** della scheda SEM-002: cambia solo `status` in `published`, lasciando `phases.publish.completed: false`. Lo schema accetta entrambi i valori e non li collega. La regola del precontrollo vale solo per `in_progress`, perciò questo caso fittizio sfuggirebbe a quella regola. Non introdurlo nel repository. Controlla invece scheda, ricevuta di distribuzione e percorso pubblico anonimo prima di credere a `published`.

### Esercizio 3 — Distingui forma e verità

Il caso sintetico `status: published` e `phases.publish.completed: false` viola una regola dello schema JSON fissato? La validità secondo lo schema proverebbe che SEM-002 è pubblicamente disponibile?

> **Risposta:** Nessuna regola nello schema collega quei due campi. La convalida attesta solo la struttura controllata; non dimostra distribuzione o disponibilità pubblica anonima. La contraddizione va indagata, non annunciata come pubblicazione.

## 4. Separa i referenti locali e pubblici

Il [resoconto pubblico di riferimento](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/public-baseline-2026-10-11.md) registra una lettura anonima dell'indice Streeling l'11 ottobre 2026, segnala un commit sorgente e precisa che la presenza pubblica non equivale a revisione dell'autore. Registra anche pagine DV-001 generate dal precontrollo locale Learn, mentre richieste GET anonime ai nuovi percorsi pubblici DV-001 restituivano 404. «Pagina generata localmente» indica un artefatto di compilazione; «pubblicato» indica una versione raggiungibile su un percorso pubblico. La prima non implica la seconda.

Il resoconto è una prova **storica sui percorsi DV-001**, non una verifica attuale di SEM-002 o del sito odierno. Per una pubblicazione SEM-003 il coordinatore dovrebbe nominare il percorso, distribuire il sito, recuperarlo anonimamente e confrontare contenuto o SHA della fonte con la revisione desiderata. HTTP 200 potrebbe mostrare una versione precedente. Lo SHA punta al testo scritto; la lettura del percorso lo collega a ciò che riceve lo studente. Il resoconto del revisore punta a un altro evento; nessuno sostituisce l'altro.

### Esercizio 4 — Identifica l'osservazione

Nell'esempio DV-001 datato esiste una pagina locale e il percorso anonimo restituisce 404. Quale frase è sostenuta: «la lezione è stata pubblicata», «la compilazione locale ha prodotto una pagina, ma quel percorso pubblico non la serviva alla data della verifica», oppure «non esisteva il file sorgente»? Cosa controllare dopo una distribuzione futura?

> **Risposta:** La frase centrale. Pagina locale e 404 riguardano superfici diverse alla data osservata. Dopo la distribuzione, recupera anonimamente il percorso previsto e confronta contenuto o SHA di provenienza con la revisione desiderata; compilazione locale e comando di distribuzione non bastano.

## 5. Scrivi un passaggio di consegne utilizzabile

Un messaggio utile forma una piccola catena: **artefatto e revisione → controllo nominato → risultato osservato → passaggio mancante → azione successiva**. È un metodo di scrittura per l'esercizio, **non un nuovo DSL normativo**. Il destinatario può seguire i riferimenti e rifiutare interpretazioni obsolete o troppo ampie. Esempio basato sull'istantanea SEM-002:

> «La fonte inglese SEM-002 esiste in Demerzel al commit `c453a91d1c4d913af72c28779eff826659c1d654`. Un controllo IA circoscritto della fonte e delle cinque risposte non ha trovato rilievi. La scheda resta `in_progress`, con revisione e pubblicazione incomplete. Prossimo passo: ottenere revisione umana della materia e degli studenti e poi verificare la distribuzione Learn prevista con lettura anonima».

Il messaggio non inventa un valore `ready`. Se una revisione futura approva solo l'accuratezza fattuale, specificane l'ambito senza trasformarla in approvazione linguistica. Una modifica della fonte non è automaticamente coperta dal vecchio resoconto. I link a revisioni immutabili collegano revisore, fonte e lettura pubblica allo stesso oggetto oppure mostrano dove la catena si è interrotta.

### Esercizio 5 — Correggi il messaggio di un agente

Riscrivi «SEM-002 è revisionato e pubblicato; i test sono verdi» usando solo scheda e resoconto fissati. Indica un'azione successiva precisa e una cosa ignota senza inventare esiti di test o distribuzione.

> **Risposta:** «Al commit Demerzel `c453a91d1c4d913af72c28779eff826659c1d654`, SEM-002 ha una bozza inglese e un resoconto di controllo IA circoscritto della fonte e delle risposte senza rilievi. La scheda rimane `in_progress`, con `review.completed=false` e `publish.completed=false`. Questi artefatti non attestano una nuova esecuzione dei test né una lettura pubblica del percorso SEM-002. Prossimo passo: chiedere revisione umana della materia e degli studenti su questa revisione». La frase iniziale amplia un controllo limitato a revisione finale e dichiara senza prove pubblicazione e test.

## Limiti e applicazione

La lezione analizza file Demerzel fissati e un resoconto pubblico datato; non esegue un vero passaggio fra agenti, una prova con studenti, una validazione di SEM-003 da parte di un semiologo umano né la pubblicazione. I cinque esercizi valutano se il lettore collega ogni parola di stato al suo referente e alle prove. Per verificare se l'approccio migliori il coordinamento, confronta con un esperimento controllato un gruppo che riceve uno stato non qualificato e un altro che riceve la catena di prove; osserva se scelgono il prossimo controllo corretto e citano la revisione giusta. **Fino ad allora, il beneficio per i passaggi di consegne resta un'ipotesi.**
