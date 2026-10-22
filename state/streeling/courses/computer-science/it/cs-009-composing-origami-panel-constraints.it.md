---
module_id: cs-009-composing-origami-panel-constraints
department: computer-science
course: "Comporre i vincoli origami prima di accettare una pila rigida"
level: intermediate
prerequisites: [cs-001-thinking-algorithmically, cs-006-ixql-pipeline-composition]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-21-009
version: "0.1.0"
---

# Comporre i vincoli origami prima di accettare una pila rigida

> **Dipartimento di informatica** | Livello intermedio | 40 minuti | Bozza italiana provvisoria; revisione disciplinare, revisione di una persona con piena padronanza dell'italiano e verifica con un discente ancora da svolgere.

## Obiettivi e domanda del progetto

Trasformerai i giunti piatti in classi di equivalenza, conserverai i vincoli diretti tra quelle classi, distinguerai i controlli locali di sovrapposizione da un vincolo globale sulla pila e leggerai un risultato incompleto senza inventare una disposizione. La domanda pratica è: **quale risultato può trasmettere un agente a un futuro adattatore Blender o Godot quando IX ha verificato uno stato origami?** Un manufatto visibile richiede un'interpretazione dichiarata dell'analisi, perché un controllo superato può coesistere con un rifiuto secondo un altro modello.

Il caso di studio è il [modulo sullo spessore implementato in IX](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) e i suoi [test d'integrazione](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), entrambi fissati a `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. Il modulo legge uno spessore del materiale nelle unità di coordinate del diagramma delle pieghe. Esamina un singolo stato dichiarato di piegatura piatta; non pianifica il movimento della piegatura né esporta una scena. La [fixture del corso](../../../fixtures/computer-science/cs-009/README.md) contiene piccole derivazioni su grafi, chiaramente distinte dai risultati effettivi dei test Rust.

## 1. Componi prima le facce in pannelli

Una faccia è un poligono nella descrizione dello stato piegato. In questo modello, un pannello è un insieme di facce collegate da giunti piatti che devono mantenere un'unica altezza. La funzione `panels` dell'implementazione unisce i loro insiemi e associa ogni faccia alla faccia con indice minimo nella sua componente connessa. Quel rappresentante è un'etichetta algoritmica. Non è un identificatore permanente dell'oggetto e la rinumerazione dell'ingresso può cambiarlo pur conservando il pannello rappresentato.

Considera le facce 0, 1 e 2. Le facce 0 e 1 condividono un giunto piatto. Le relazioni dichiarate pongono 2 sopra 0 e 1 sopra 2. Nel grafo delle facce, gli archi dal basso verso l'alto sono `0 → 2 → 1`, senza cicli. Se assegniamo a ogni faccia un'altezza distinta, la risposta apparente è data dai livelli 0, 1 e 2. Questo viola il modello: le facce 0 e 1 appartengono a un unico pannello rigido e non possono assumere altezze diverse.

Dopo aver unito le facce collegate da giunti piatti, la mappa dei pannelli è `[0, 0, 2]`. I due vincoli diventano `panel 0 → panel 2` e `panel 2 → panel 0`. Ora il ciclo è visibile. È una costruzione per quoziente: prima si raggruppano gli oggetti che devono muoversi insieme, poi si applicano i vincoli d'ordine a quei gruppi. Verificare ogni parte prima della composizione non rileva il requisito introdotto dalla loro identità condivisa.

### Esercizio 1: correggere il grafo fuorviante

Usa la fixture `pierced-flat-joint`. Indica i rappresentanti dei pannelli e i due archi tra pannelli. Spiega perché l'ordine topologico del grafo delle facce non può giustificare una disposizione rigida. Quale ulteriore decisione implementativa servirebbe se un adattatore volesse un ID permanente del pannello?

> **Risposta:** I rappresentanti sono `[0, 0, 2]`; gli archi sono `0 → 2` e `2 → 0`. L'ordine delle facce consente due altezze diverse per lo stesso pannello collegato da giunti piatti, quindi risolve il sistema di vincoli sbagliato. Un ID permanente del pannello richiederebbe una corrispondenza dichiarata con l'identità del materiale o della fonte attraverso modifiche o permutazioni. Il solo rappresentante con indice minimo non offre tale garanzia.

## 2. Un esito locale positivo può coesistere con un rifiuto globale

Il test alla revisione fissata `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` costruisce quattro strisce. Ognuna si sovrappone alla successiva in un angolo diverso. Ogni cella locale di sovrapposizione può avere un ordine coerente, eppure le affermazioni combinate dicono che la striscia 0 è sopra 1, 1 sopra 2, 2 sopra 3 e 3 sopra 0. Usando archi dal basso verso l'alto si ottiene `0 → 3 → 2 → 1 → 0`. Nessuna assegnazione di un'unica altezza per striscia soddisfa tutte e quattro le disuguaglianze con spessore del materiale positivo.

È un problema distinto da [VC-007](../../visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), il cui verificatore sintetico rileva il riavvio della parità ai bordi di tasselli ripetuti. Qui il problema è un ciclo che attraversa regioni di sovrapposizione diverse nell'implementazione esistente di IX. Una texture, un'anteprima di un incrocio locale o un'analisi origami di base superata non possono risolvere la questione globale dei pannelli paralleli.

Il test verifica che `analyse(&weave()).unwrap().ok` sia vero. Controlla anche la lettura opzionale dello spessore con `t = 0`, un `t` positivo molto piccolo e `t = 0.5`. Il grafo resta ciclico, ma `rigid.refused` è vero solo per `t` positivo. A zero, l'implementazione restituisce comunque `levels`, `height` e `face_levels` come assenti per questa lettura ciclica. Non sostituire un'altezza rigida assente con zero solo perché il valore separato `ply_height` è zero.

### Esercizio 2: interpretare il caso zero

L'intreccio ha `ply = 2` e un ordine ciclico dei pannelli. Quali sono `ply_height` e `rigid.refused` con `t = 0` e con `t = 0.5`? Uno dei due risultati fornisce un'assegnazione rigida dei livelli alle facce?

> **Risposta:** A zero, `ply_height = 0` e `rigid.refused = false`; a 0.5, `ply_height = 1` e il rifiuto è vero. In entrambi i rapporti ciclici sono assenti i livelli rigidi, l'altezza e l'assegnazione dei livelli alle facce. L'assenza di rifiuto a spessore zero non fornisce la configurazione testimone mancante e il rifiuto a spessore positivo riguarda questo modello a pannelli paralleli.

## 3. I vincoli aciclici consentono il calcolo del cammino più lungo

Quando il grafo dei pannelli ammette un ordine topologico, l'implementazione inizializza ogni livello a zero. Per ogni arco diretto da un pannello inferiore `u` a un pannello superiore `v`, aggiorna `level[v] = max(level[v], level[u] + 1)`. L'elaborazione in ordine topologico assicura che il livello di ogni predecessore sia disponibile. Il livello più alto, con indicizzazione da zero, più uno dà la lunghezza della catena in pannelli. Moltiplicando per lo spessore completo `t` si ottiene l'altezza della pila per un ordine completamente determinato.

Il valore `face_levels` riportato è una configurazione testimone prodotta da questa ricorrenza. Possono esistere altre pile valide; i valori per faccia non costituiscono un'etichettatura canonica di ogni pila ammissibile.

Il DAG sintetico nella fixture ha archi `P → R`, `Q → R` e `R → S`. P e Q possono condividere il livello zero perché l'esempio non fornisce relazioni che ne richiedano la separazione; R deve stare sopra entrambi, poi S sopra R. Sono dati di un grafo astratto, non geometria FOLD esportata né un'affermazione sulla sovrapposizione spaziale. Servono a esercitarsi con la ricorrenza prima di leggere il test più ampio della gru.

### Esercizio 3: calcolare la catena

Assegna i livelli ai quattro pannelli del DAG sintetico, conta i pannelli nella catena più lunga e calcola l'altezza per `t = 0.2`. Perché riportare soltanto il livello più alto sarebbe un errore di uno nel conteggio? Per confronto, quali due conteggi distingue il test effettivo della gru?

> **Risposta:** P e Q sono a 0, R a 1 e S a 2. La catena ha tre pannelli, quindi l'altezza è `3 × 0.2 = 0.6` nelle unità del diagramma delle pieghe. L'indice massimo 2 omette un livello occupato. Il test effettivo della gru distingue il massimo locale di 28 strati dai 36 livelli richiesti per pannelli paralleli; l'occupazione locale e una catena attraverso regioni diverse rispondono a domande diverse.

## 4. L'ordine mancante fa parte del risultato

L'implementazione conta le coppie di facce sovrapposte su pannelli diversi il cui ordine non è dichiarato. In presenza di almeno una di queste coppie, `levels_exact` è falso. Riporta `max(chain, ply)` come limite inferiore e non fornisce `face_levels`. I soli vincoli dichiarati aciclici non possono certificare che una disposizione proposta rispetti una relazione mai specificata nell'ingresso.

Il test alla revisione fissata `an_unstated_overlap_gives_a_lower_bound` usa due fogli sovrapposti senza un ordine dichiarato. Si aspetta una coppia indeterminata, due livelli come limite inferiore e nessuna assegnazione di livelli alle facce. Il chiamante deve conservare il flag di esattezza insieme al numero. Se il riepilogo di un agente lo elimina, una fase successiva può trasformare un limite inferiore in una presunta disposizione completa senza che nessuno prenda esplicitamente quella decisione.

### Esercizio 4: conservare l'incertezza nel passaggio di consegne

La scheda sintetica con ordine incompleto ha catena 2, numero di strati 3, una coppia indeterminata e `t = 0.2`. Quale altezza numerica può riportare l'algoritmo e come va descritta? Un adattatore di scena può usarla per posizionare ogni faccia?

> **Risposta:** Riporta `max(2, 3) = 3` livelli e un limite inferiore dell'altezza di 0.6, con `levels_exact = false` e `face_levels = null`. Non può fornire una disposizione completa. Un passaggio di consegne dovrebbe conservare l'indicazione di limite inferiore, il conteggio delle coppie mancanti, l'identità della fonte e l'assenza della configurazione testimone, anziché promettere coordinate ricavate da un ordine non osservato.

## 5. Trasforma il risultato in una decisione verificabile

Una composizione agentica può trasportare insieme l'analisi di base e la lettura rigida. La [decisione di progetto alla revisione fissata](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/docs/adr/0007-origami-thickness-as-parallel-rigid-panels.md) mantiene esplicitamente la lettura dello spessore accanto al verdetto di base. Un rifiuto significa che non esiste una pila secondo le ipotesi dei pannelli rigidi paralleli. Non dimostra che un oggetto materiale sia impossibile con pannelli inclinati, pieghe modificate o altri metodi costruttivi. Viceversa, l'assenza di rifiuto non dimostra la fabbricabilità.

Per una prova proposta in Godot, conserva la revisione della fonte FOLD, la conversione dello spessore completo e delle unità, entrambi i risultati dell'analisi, l'eventuale ciclo testimone, l'esattezza e la mappa tra facce e oggetti. Assegna a chi usa il visualizzatore un compito specifico, per esempio trovare la relazione responsabile di un rifiuto. Confronta la sua risposta con quella ottenuta usando un semplice diagramma del grafo per lo stesso compito. È un esperimento di trasferimento proposto; il corso non registra alcun renderer, esportazione, prova con discenti o miglioramento delle prestazioni. Un nuovo DSL giustificherebbe il proprio costo solo se migliorasse quel compito rispetto a un rapporto tipizzato più semplice e al verificatore esistente.

### Esercizio 5: decidere che cosa trasmettere alle fasi successive

Un futuro agente riferisce: «Analisi di base superata; rifiuto rigido a spessore positivo; facce del ciclo `[0,3], [3,2], [2,1], [1,0]`». Propone di etichettare l'asset come «fisicamente impossibile» e di omettere il ciclo perché la scena appare plausibile. Scrivi una dichiarazione corretta rivolta all'utente e identifica le prossime evidenze necessarie per una dimostrazione in scena.

> **Risposta:** «Lo stato dichiarato ha superato i controlli di base, ma il suo ordine dichiarato presenta un ciclo che impedisce una pila di pannelli rigidi paralleli a questo spessore positivo.» Conserva il ciclo e le ipotesi. Una dimostrazione in scena richiede un'importazione legata alla fonte e una mappa tra facce e oggetti, una visualizzazione del ciclo verificabile in modo indipendente e un compito registrato per chi usa il visualizzatore. Una schermata da sola non può dimostrare il risultato del grafo, l'impossibilità fisica o il beneficio didattico.

## Riesecuzione e limiti

Esegui `cargo test -p ix-origami --test thickness` in IX al commit fissato. Il coordinatore ha rieseguito tutti gli 11 test d'integrazione sullo spessore il 2026-10-21: 11 superati, 0 falliti. Il README della fixture registra la fonte e i blob dei test. Le schede dei grafi sono dati didattici ricavati a mano; non viene introdotto alcun analizzatore aggiuntivo né runtime per i progetti consumatori. Il superamento di quei test sostiene i casi implementativi descritti, mentre accuratezza disciplinare, fluidità della traduzione, riuscita dell'apprendimento, importazione nella scena e pubblicazione Learn verificata senza autenticazione restano attività separate.
