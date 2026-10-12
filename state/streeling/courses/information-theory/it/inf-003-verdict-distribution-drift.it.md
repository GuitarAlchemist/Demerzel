---
module_id: inf-003-verdict-distribution-drift
department: information-theory
course: "Misurare la deriva delle distribuzioni dei verdetti con la divergenza di Jensen-Shannon"
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-003
version: "0.1.0"
---

# Misurare la deriva delle distribuzioni dei verdetti con la divergenza di Jensen-Shannon

> **Dipartimento di Teoria dell'Informazione** | Livello: intermedio | Durata stimata: 35 minuti | Stato: bozza italiana; revisioni della materia, didattica e linguistica e pubblicazione in sospeso

## Obiettivi

Al termine della lezione saprai:

- trasformare conteggi comparabili dei verdetti dell'analizzatore IX in vettori di probabilità allineati;
- calcolare la divergenza direzionale di Kullback–Leibler (KL) e la divergenza simmetrica di Jensen–Shannon (JS) nelle unità restituite da IX;
- spiegare perché una categoria nuova può causare un errore in una direzione di KL mentre JS rimane finita;
- usare una divergenza per decidere quali prove esaminare, controllando i limiti dell'analisi e la composizione dei lotti.

## La domanda del progetto

L'[analizzatore di reti di Petri IX alla revisione indicata](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L105) serializza il risultato di una proprietà come `holds`, `fails` oppure `unknown`. `Fails` può contenere un controesempio; `unknown` indica che l'analizzatore non ha deciso la proprietà entro i limiti di esplorazione. Una variazione della frequenza di questi risultati fra due esecuzioni può richiedere un'indagine. Come quantificarla senza scambiare un singolo numero per la prova di una regressione?

La domanda falsificabile è: **per una proprietà, gli stessi ID delle reti, la stessa revisione dell'analizzatore e gli stessi limiti, di quanto è cambiata la distribuzione delle categorie dopo una modifica delle reti?** IX offre già le [funzioni KL e JS](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L222), esposte anche come [funzioni scalari DuckDB](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-duck/src/inference.rs#L186-L210). Qui otteniamo una risposta riproducibile da conteggi **sintetici**. Non abbiamo misurato alcun lotto IX di produzione né un cambiamento di qualità percepito dagli utenti.

INF-001 usava l'entropia per descrivere una distribuzione di token di policy. INF-002 mostrava le distinzioni perse dalla mappatura compatta OPTIC-K di GA fra singoli vettori. Qui confrontiamo **due distribuzioni sulle medesime categorie di verdetti**. Il punteggio riassume frequenze aggregate; non rivela quale rete sia cambiata, perché o se il cambiamento sia utile.

## 1. Scegliere un'osservazione dal significato stabile

L'[enum `Verdict<T>`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L95) ha tre etichette. Il metodo `holds()` restituisce true soltanto per `Holds`: `Unknown` non diventa un successo implicito. Il report `Analysis` contiene proprietà **diverse**, fra cui `deadlock_free`, `bounded`, `quasi_live`, `live` e `reversible`. Unirle in un solo conteggio mescolerebbe domande con condizioni di prova differenti. Scegliamo soltanto `deadlock_free`, un verdetto per rete e l'ordine `[holds, fails, unknown]`.

Il [ramo relativo all'assenza di deadlock](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L465-L491) chiarisce le etichette. Una marcatura morta individuata produce `Fails`, anche se l'enumerazione viene successivamente troncata; `max_reported_deadlocks` limita i testimoni riportati e può valere zero. Se non emerge una marcatura morta, `Holds` richiede esplorazione completa; altrimenti si ottiene `Unknown`. È un'osservazione specifica di questa proprietà, non una generalizzazione a ogni ramo dell'analizzatore.

Il lotto di dieci reti seguente è **inventato** per l'esercizio numerico:

| Esecuzione | Holds | Fails | Unknown | Totale |
|---|---:|---:|---:|---:|
| Riferimento | 8 | 0 | 2 | 10 |
| Candidata | 6 | 2 | 2 | 10 |

Dividendo ogni riga per il totale si ricavano `p = [0.8, 0, 0.2]` e `q = [0.6, 0.2, 0.2]`. L'ordine delle etichette deve coincidere. La funzione accetterebbe array con etichette scambiate ma confronterebbe eventi diversi. Conserva le etichette insieme ai conteggi e convalida l'ordine.

### Esercizio 1: formare vettori comparabili

Scrivi i due vettori normalizzati nell'ordine `[holds, fails, unknown]`. Quali metadati servono per un confronto reale?

> **Risposta:** `p=[8/10,0/10,2/10]=[0.8,0,0.2]`; `q=[6/10,2/10,2/10]=[0.6,0.2,0.2]`. Conserva la proprietà, gli ID delle reti, l'ordine delle categorie, il commit dell'analizzatore, i limiti di esplorazione e il totale di ogni esecuzione. La divergenza non verifica da sola queste condizioni.

## 2. Leggere il calcolo effettivo di IX

L'implementazione di [`normalize`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L173) divide un vettore non negativo per la sua somma. Rifiuta vettori vuoti, valori negativi o NaN e somme nulle. Il nostro protocollo richiede inoltre conteggi finiti prima della chiamata: il codice non rifiuta esplicitamente l'infinito positivo. Entrambe le divergenze richiedono vettori di pari lunghezza e usano logaritmi naturali; il risultato è in **nat**. Dividi per `ln(2)` per convertirlo in bit. Il wrapper DuckDB espone `ix_kl(p,q)` e `ix_js(p,q)` per valori `DOUBLE[]`: una lista SQL `NULL` propaga `NULL`, mentre un errore matematico diventa un errore SQL. Il wrapper non dimostra l'esistenza di un confronto pianificato.

KL è direzionale:

`D_KL(p || q) = Σ_i p_i ln(p_i / q_i)`.

Contribuiscono solo le categorie con `p_i > 0`. Qui `D_KL(p || q)=0.8 ln(0.8/0.6)+0.2 ln(0.2/0.2)=0.23014565796142483` nat. Nell'altra direzione, `fails` richiede `0.2 ln(0.2/0)`: matematicamente diverge e [IX restituisce un errore](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L185-L209), non un valore infinito. Invertire gli argomenti cambia la domanda. Non nascondere la categoria nuova registrando zero al posto dell'errore.

### Esercizio 2: spiegare la direzione di KL

Calcola `D_KL(p || q)`. `D_KL(q || p)` restituisce lo stesso numero in IX?

> **Risposta:** `D_KL(p || q)=0.8 ln(4/3)=0.23014565796142483` nat. Per `D_KL(q || p)`, `q_fails=0.2` incontra `p_fails=0`; dopo aver invertito gli argomenti, IX restituisce l'errore di parametro « q is zero where p is positive ». KL è asimmetrica: qui solo la direzione riferimento-verso-candidata ha supporto finito.

## 3. Usare JS come indicatore finito e simmetrico

JS forma il punto medio `m=(p+q)/2` e fa la media di due KL: `D_JS(p,q)=0.5 D_KL(p||m)+0.5 D_KL(q||m)`. Qui `m=[0.7,0.1,0.2]`. Il punto medio ha massa positiva ovunque uno dei vettori ne abbia: JS rimane finita per questa coppia. Il [codice e il commento](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L210-L222) specificano che JS è simmetrica e limitata da `ln(2)` nat. Zero indica distribuzioni **normalizzate** identiche, non esecuzioni o dimensioni dei lotti identiche.

Un calcolo indipendente della formula dà `D_KL(p||m)=0.10682511409961822` e `D_KL(q||m)=0.04613902821563412`; la semisomma è `D_JS=0.07648207115762617` nat, cioè `0.1103403047760241` bit. Questi risultati appartengono all'esempio sintetico, non a un'installazione IX. I [test unitari fissati](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L568-L580) coprono il massimo per vettori one-hot disgiunti e zero per valori uguali; non abbiamo eseguito la suite qui.

### Esercizio 3: calcolare e limitare JS

Calcola il punto medio e JS. Scambiare le esecuzioni cambia il risultato? Qual è il massimo teorico in nat?

> **Risposta:** `m=[0.7,0.1,0.2]`; `D_JS=0.5(0.10682511409961822+0.04613902821563412)=0.07648207115762617` nat. Lo scambio conserva il punto medio e inverte i due termini di pari peso; JS non cambia. Il massimo è `ln(2)=0.6931471805599453` nat per supporti disgiunti.

### Esercizio 4: cosa nasconde la normalizzazione

Confronta `[80,0,20]` e `[8,0,2]` con `ix_js`. Che cosa dimostra il risultato?

> **Risposta:** Entrambi diventano `[0.8,0,0.2]` dopo la normalizzazione, perciò `ix_js` restituisce `0`, salvo gli effetti della rappresentazione in virgola mobile. Dimostra solo l'uguaglianza delle proporzioni. Un lotto contiene 100 osservazioni, l'altro 10: JS perde tale differenza e non dice se le stesse reti hanno ricevuto gli stessi verdetti. Conserva totali e ID appaiati fuori dal punteggio.

## 4. Decidere cosa deve attivare il segnale

Immagina una futura regola QA approvata separatamente che segnali `JS > 0.05` nat per un'indagine. Il valore **illustrativo** supera questa soglia inventata. È un motivo per esaminare i dati, non la prova di una regola già distribuita né una ragione automatica per respingere una modifica. Controlla prima che siano state analizzate le stesse dieci reti e la proprietà `deadlock_free`. Verifica poi revisione e `Limits`: il [report espone troncamento e motivo](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L161-L175). Aumentare `max_states` può far passare `unknown` a `holds` o `fails` senza modificare alcuna rete. Appaia i verdetti per ID e consulta i testimoni di fallimento e i motivi di incertezza disponibili. Se serve un testimone mancante, riesegui con `max_reported_deadlocks` maggiore di zero. L'istogramma non identifica le reti cambiate né convalida i controesempi per la proprietà voluta.

Per un lotto piccolo e stabile, la tabella a tre colonne e i cambiamenti individuali possono essere più chiari di un numero. Il punteggio può aiutare a ordinare molti lotti comparabili, purché la tabella e le prove per rete restino accessibili. È un'ipotesi di progetto, non un sostituto della revisione dei testimoni. Se gli avvisi ripetuti dipendono soprattutto da composizioni o budget di esplorazione diversi, l'utilità del segnale è falsificata: occorre rivedere il protocollo, non regolare la soglia finché gli avvisi spariscono.

### Esercizio 5: interpretare un avviso

La soglia ipotetica è `0.05` nat e JS vale `0.07648207115762617`. Un collega dice: « La candidata è regredita; ci sono due nuovi fallimenti ». Quale parte è un risultato aritmetico verificabile e cosa va controllato prima di accettare la regressione?

> **Risposta:** `0.07648207115762617 > 0.05`: l'esempio sintetico attiverebbe la regola d'indagine inventata. La tabella mostra due `fails` nella candidata e nessuno nel riferimento, ma non identifica le reti cambiate. Verifica ID, proprietà, revisione e limiti identici; appaia gli esiti; leggi i testimoni di fallimento disponibili e i motivi di `unknown`. Richiedi `max_reported_deadlocks > 0` e riesegui se manca un testimone necessario. Un limite o un lotto diverso potrebbe spiegare la deriva senza una regressione del codice. Il punteggio non dimostra causalità o significatività statistica.

## Limiti e passo successivo

Abbiamo verificato la formula su una tabella sintetica con un piccolo calcolo indipendente e letto il codice IX al commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Non abbiamo eseguito l'analizzatore su dieci reti, interrogato una vera tabella DuckDB, eseguito la suite IX, stimato l'incertezza campionaria o convalidato una soglia di produzione. Lotti ripetuti ma non identici richiederebbero un piano di campionamento e appaiamento. Un prossimo esperimento circoscritto registrerebbe una proprietà per ID stabile a due revisioni fissate e con limiti uguali, calcolerebbe JS e ispezionerebbe manualmente ogni verdetto cambiato. Conserva tabella, risultati per rete e testimoni accanto al punteggio. Questa traduzione è una bozza IA: revisione umana, sincronizzazione e build di Learn e lettura pubblica sono ancora in sospeso.
