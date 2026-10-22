---
module_id: sem-004-face-identity-under-reindexing
department: semiotics
course: "Identità delle facce durante la reindicizzazione"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-21-004
version: "0.1.0"
---

# Identità delle facce durante la reindicizzazione

> **Dipartimento di semiotica** | Livello intermedio | 40 minuti | Bozza italiana provvisoria; revisione disciplinare, revisione di una persona con piena padronanza dell'italiano e verifica con un discente ancora da svolgere.

## Obiettivi e decisione di progetto

Un futuro visualizzatore di scene seleziona la faccia 1 di un modello origami. Un secondo agente rinumera il modello e segnala che la faccia 1 ha cambiato livello. Il materiale si è spostato, l'ordine è cambiato oppure lo stesso numero ha iniziato a indicare una faccia diversa? Per rispondere occorre interpretare il numero prima di interpretare la geometria.

Al termine della lezione saprai trasferire una selezione attraverso una permutazione esplicita, invertire tale corrispondenza, distinguere l'identità di una faccia dal suo livello e dal suo orientamento e scrivere un rapporto tra agenti con limiti dichiarati. Dedica otto minuti al problema e ai segni, dodici alla tabella, dieci alle trasformazioni e dieci agli esercizi e al trasferimento. L'artefatto è una piccola tabella di corrispondenza e un passaggio di consegne sostenibile sulla base delle evidenze, anziché un nuovo servizio d'identità.

Le evidenze del progetto provengono dal commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), i [test sullo spessore](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) e [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). Questi collegamenti fissano la fonte esaminata, non il branch corrente. IX fornisce qui controlli di verifica e trasformazione; questa lezione non dimostra un'esportazione Blender, un'importazione Godot, un renderer o un'implementazione della selezione persistente.

## 1. Il numero di una faccia è un segno contestuale

In semiotica, un segno sta per un oggetto secondo un'interpretazione. Qui `1` è il segno, una particolare faccia materiale è l'oggetto inteso e «cerca la posizione 1 in questa revisione del modello» è l'interpretazione. Un **indice** di array è un indirizzo informatico all'interno di una raccolta ordinata. Non va confuso con il termine semiotico più ampio *indice*, cioè un segno connesso a ciò che indica. Nessuno dei due usi della parola conferisce al numero un'identità permanente.

Un rapporto deve specificare la revisione del modello o il contesto della trasformazione. «Faccia 1» nell'ingresso e «faccia 1» nell'uscita sono due riferimenti potenzialmente diversi. Forma, colore e livello corrente nella pila possono aiutare una persona a riconoscere una faccia, ma queste proprietà possono coincidere tra facce diverse o cambiare con una trasformazione. Da sole non ne stabiliscono la provenienza.

In questa lezione, per **identità materiale** si intende la corrispondenza con la stessa faccia in ingresso attraverso la particolare trasformazione controllata. Non risolve i problemi di ricostruzione arbitraria della mesh, divisione, fusione o ricostruzione di un modello da un'immagine. Un'etichetta di provenienza, come l'etichetta didattica A, registra la corrispondenza che abbiamo fornito. Queste etichette sono esplicitamente sintetiche; la `Permutation` esaminata in IX è una mappa relativa a una trasformazione, non un registro universale di identificatori persistenti.

### Esercizio 1 — Correggere un riferimento

Un agente dice: «La faccia 1 è sbagliata dopo la rinumerazione». Quali informazioni mancano? Riformula la frase come domanda verificabile.

> **Risposta:** Mancano il contesto del modello in ingresso e in uscita, la mappa di corrispondenza e la proprietà confrontata. Una domanda utile è: «Per la faccia sintetica 1 in ingresso (B), usando la mappa da vecchi a nuovi indici `[2,0,3,1]`, la faccia 0 in uscita mantiene il livello 2 dell'ingresso?» Questo identifica il materiale inteso e il confronto preciso; non sostiene che IX abbia un difetto.

## 2. Applica la mappa nella direzione dichiarata

`Permutation` documenta dove è finito ciascun **vecchio** indice. La funzione ausiliaria `place` scrive un vecchio elemento in `out[perm[old]]`. Quindi `perm.faces[f]` prende l'indice di una faccia in ingresso e restituisce l'indice della stessa faccia in uscita. Non dice quale faccia in ingresso occupi ora una posizione arbitraria in uscita; per questo serve l'inversa.

Usa questo esempio di quattro facce esplicitamente **sintetico**, registrato anche nella [fixture](../../../fixtures/semiotics/sem-004/scenarios.json). I suoi numeri non sono risultati della gru, un seed campionato o un esperimento sullo spessore fisico.

| Indice in ingresso | Etichetta didattica di provenienza | Livello in ingresso | Indice in uscita `p[old]` |
|---:|---|---:|---:|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 0 |
| 2 | C | 1 | 3 |
| 3 | D | 3 | 1 |

La mappa diretta è `p = [2,0,3,1]`. Leggendo le posizioni in uscita da 0 a 3 si ottengono le etichette `[B,D,A,C]` e i livelli `[2,3,0,1]`. L'inversa è `q = [1,3,0,2]`: la posizione 0 in uscita proviene dalla posizione 1 in ingresso e la posizione 1 in uscita proviene dalla posizione 3 in ingresso. Verifica entrambe le direzioni: `q[p[f]] = f` e `p[q[j]] = j`.

Il confronto corretto delle proprietà è `new[p[f]] == old[f]`. Per B in ingresso è `new[0] == old[1]`, quindi `2 == 2`. Il confronto diretto degli array dà una disuguaglianza anche se ogni faccia materiale conserva il proprio valore. Riutilizzare invece l'intero selezionato 1 evidenzia D, il cui livello è 3. È un errore di selezione senza alcuna alterazione del calcolo dei livelli.

L'inversa è altrettanto utile quando un utente fa clic sulla posizione 3 in uscita: identifica C nella posizione 2 in ingresso. Scrivere `new[q[f]]` nel confronto diretto mescola i domini. Con la nostra mappa volutamente diversa dalla propria inversa, per l'ingresso 0 si confronterebbe `new[1] = 3` con `old[0] = 0`. Un esempio composto solo da uno scambio può nascondere questo errore, perché uno scambio coincide con la propria inversa.

### Esercizio 2 — Trasferire la selezione

Trasferisci la selezione C in ingresso attraverso la mappa. Poi risali all'ingresso da un clic sulla posizione 1 in uscita. Mantenere l'intero 2 conserverebbe la selezione originale di C?

> **Risposta:** C è l'ingresso 2, quindi il suo indice in uscita è `p[2] = 3`, mantenendo il livello 1. L'uscita 1 proviene da `q[1] = 3`, etichetta D. Mantenere l'intero 2 selezionerebbe A in uscita. La mappa cambia l'indirizzo preservando la corrispondenza materiale che abbiamo stabilito.

### Esercizio 3 — Confrontare gli oggetti giusti

Trova la prima discrepanza in un confronto diretto di `[0,2,1,3]` e `[2,3,0,1]`. Indica i quattro confronti effettuati tramite la mappa e verifica un'equazione dell'inversa.

> **Risposta:** La posizione 0 nel confronto diretto non coincide: `0 != 2`. I controlli tramite la mappa sono `new[2]=0`, `new[0]=2`, `new[3]=1` e `new[1]=3`, corrispondenti rispettivamente alle posizioni 0–3 in ingresso. Per esempio, `q[p[2]] = q[3] = 2`. La disuguaglianza diretta non confuta la corrispondenza dichiarata.

## 3. Conserva le relazioni senza confonderne i segni

La rinumerazione rimappa anche vertici e spigoli. Ruota ciclicamente l'elenco dei vertici di ogni faccia, mantenendone il verso di percorrenza; può scambiare gli estremi di uno spigolo; rimescola la sequenza delle voci di `faceOrders`. Sono operazioni distinte. Ruotare un contorno triangolare da `[0,1,2]` a `[1,2,0]` ne cambia il punto iniziale. Invertirlo in `[0,2,1]` cambia il verso di percorrenza e non è la stessa operazione. Questi piccoli elenchi di contorno illustrano convenzioni d'ordine, non geometria estratta da IX.

In ogni tripla `[f,g,s]` di `faceOrders`, `renumber` sostituisce gli indici ottenendo `[p[f],p[g],s]` e conserva il segno. La nostra tripla sintetica `[1,3,1]` diventa `[0,1,1]`. Il segno si interpreta rispetto alle normali delle facce; senza l'orientamento non deve essere trasformato in un'etichetta globale e incondizionata di «sopra». Anche rimescolare la raccolta delle relazioni non inverte tutte le relazioni. La posizione in un elenco, la posizione di un estremo, il verso di un contorno e il segno dell'ordine degli strati hanno significati diversi.

Nel test sullo spessore alla revisione fissata, `controls_leave_the_stack_unchanged` esegue la rinumerazione della gru con i seed 1–5. Verifica 28 strati, 36 livelli rigidi e, per ogni faccia in ingresso, `new[perm.faces[f]] == old[f]`. Questa è un'evidenza concreta per quei controlli su quella fixture. Non è un teorema esaustivo per ogni piegatura o trasformazione.

`face_levels` è una configurazione testimone della pila che rispetta le coppie dichiarate, a partire dal livello zero. L'implementazione può non restituire alcun livello per faccia quando c'è un ciclo o l'informazione sull'ordine è insufficiente. Un livello non è quindi né un identificatore materiale univoco né una descrizione canonica di ogni pila ammissibile. Due facce possono condividere un livello. La sola corrispondenza dei conteggi aggregati non dice a un coordinatore se una selezione punti ancora alla faccia desiderata.

### Esercizio 4 — Distinguere tre operazioni sull'ordine

Chi revisiona tratta un contorno di faccia ruotato, voci di `faceOrders` rimescolate e un modello capovolto come «riordinamenti di array». Spiega perché questa descrizione perde significato rilevante. Rimappa la tripla sintetica `[1,3,1]`.

> **Risposta:** La rotazione del contorno conserva il verso ciclico di percorrenza; rimescolare l'elenco delle relazioni ne cambia l'enumerazione conservando ogni relazione; capovolgere cambia l'orientamento e l'interpretazione di ciò che è in alto. Richiedono controlli diversi. La tripla diventa `[0,1,1]`: i riferimenti alle facce vengono trasformati tramite p e il relativo segno è conservato. Questo, da solo, non stabilisce una relazione globale di «sopra».

## 4. Dichiara la trasformazione e il perimetro delle evidenze

`move_folded` ruota il sistema di riferimento piegato nel suo piano e poi lo trasla, conservando gli orientamenti. Il test alla revisione fissata usa un angolo di 0.7 radianti e uno spostamento `[3,-2]`, verificando l'uguaglianza dell'intera pila restituita con il riferimento. Questa osservazione sostiene il moto rigido testato, non ridimensionamenti, deformazioni o ricostruzioni arbitrarie della mesh.

`turn_over` riflette le coordinate y piegate con `y -> -y`. La documentazione dice che sia gli orientamenti sia il verso dell'alto si invertono, quindi `faceOrders`, definito rispetto alle normali delle facce, resta invariato. Il test sullo spessore verifica l'uguaglianza di numero di strati, altezza per strati, numero di livelli rigidi e altezza rigida. Esplicitamente **non** verifica quale faccia occupi quale livello. Affermare che i livelli delle singole facce restano invariati dopo il capovolgimento andrebbe oltre le evidenze. Corrispondenza materiale e ordine verticale sono questioni separate.

Un passaggio di consegne utile specifica revisione della fonte, trasformazione, direzione della mappa, indici selezionati in ingresso e in uscita, proprietà confrontata e risultato. Se la corrispondenza non è disponibile dopo una rigenerazione arbitraria, dichiara l'identità non risolta. Uno spessore aggregato identico o una sagoma familiare non possono fornire la mappa mancante. È un requisito di comunicazione per il flusso di lavoro proposto, non un protocollo di selezione implementato in IX.

### Esercizio 5 — Progettare una prova di selezione falsificabile

Proponi una futura prova in Godot che possa smentire il mantenimento corretto della selezione dopo questa rinumerazione sintetica. Includi un'affermazione sul capovolgimento che la fonte esistente non giustifica.

> **Risposta:** Prima della trasformazione, seleziona B all'indice 1 in ingresso e registra l'etichetta didattica di provenienza, la revisione del modello e la mappa. Dopo aver applicato p, richiedi che l'evidenziazione e il rapporto indichino l'uscita 0, B, livello 2. Un'evidenziazione dell'uscita 1/D smentisce il mantenimento della selezione anche se i livelli totali coincidono. Registra gli eventi grezzi di selezione e schermate prima e dopo; qui non è stata eseguita alcuna prova. «B mantiene lo stesso livello dopo il capovolgimento» non è sostenuto dalle asserzioni sul capovolgimento alla revisione fissata, che riguardano solo valori aggregati.

La prova proposta richiede un adattatore di scena reale e un'osservazione indipendente prima di poter dichiarare riuscita l'integrazione. Gli artefatti attuali sono l'analisi delle fonti, una tabella sintetica e compiti preparati per il discente. Restano da svolgere la revisione disciplinare umana, un tentativo di un discente, la revisione da parte di una persona con piena padronanza dell'italiano e la pubblicazione pubblica.
