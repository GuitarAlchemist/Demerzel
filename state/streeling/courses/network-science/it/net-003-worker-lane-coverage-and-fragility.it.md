---
module_id: net-003-worker-lane-coverage-and-fragility
department: network-science
course: "Misurare la copertura delle assegnazioni dopo un cambio di modalità"
level: intermediate
prerequisites: [net-002-capability-graphs-and-projections]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-003
version: "0.1.0"
---

# Misurare la copertura delle assegnazioni dopo un cambio di modalità

> **Dipartimento di scienza delle reti** | Livello intermedio | 35 minuti | Bozza italiana; revisione e pubblicazione in sospeso

## Obiettivi e domanda del progetto

Costruirai un grafo tra lavoratori e classi di lavoro a partire da una policy Demerzel delle assegnazioni fissata a un commit. Misurerai la copertura, l'effetto della rimozione di un lavoratore e le informazioni che il grafo perde su ruoli e decisioni. **Domanda del progetto:** se cambia la modalità consultiva di distribuzione o una corsia diventa indisponibile, quali *classi di lavoro dichiarate* conservano un percorso nominato? Il calcolo può orientare la scelta di una corsia o una domanda di revisione. Non prova che un agente sia online, autorizzato ad agire o abbia concluso un compito.

[NET-002](../en/net-002-capability-graphs-and-projections.md) collega *repository* a famiglie di capacità. Questa lezione collega invece *lavoratori* ai ruoli assegnati e alle loro classi. Gli archi provengono dalla [policy Demerzel al commit `ecdc6c2`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) e sono filtrati secondo la modalità richiesta. Il grafo non incorpora percorsi MCP né lo stato attuale degli agenti.

## 1. Definire il grafo prima di misurarlo

La policy fissata dichiara cinque lavoratori: `jules`, `claude`, `gemini`, `codex` e `augment`. Ognuno ha un ruolo `primary`, una lista di ruoli `secondary` e una lista separata `forbidden` ([definizioni dei lavoratori](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L54-L79)). Ogni ruolo nominato corrisponde a una `work_class` ([definizioni dei ruoli](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L19-L51)). La policy si descrive come **consultiva e in sola simulazione**. Propone un instradamento, non certifica lavoro svolto.

Costruisci il grafo diretto a tre livelli `lavoratore → ruolo assegnato → classe di lavoro`. Traccia il primo arco solo per un ruolo primario o secondario; un ruolo vietato non crea un percorso. Il secondo arco segue `work_class`. Per la modalità richiesta, nascondi i percorsi la cui classe compare in [`mode_blocks`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L81-L86). Nella proiezione a due livelli, un arco lavoratore-classe esiste se sopravvive almeno un percorso attraverso un ruolo assegnato. Più ruoli della stessa classe contano come **un solo** arco lavoratore-classe. Contiamo scelte di lavoratori distinti, non capacità o compiti completati.

Il dizionario completo `work_classes` contiene 13 nomi, comprese azioni vietate. Solo cinque classi compaiono nelle assegnazioni primarie o secondarie: `fix`, `groom`, `navigate`, `net_new_feature` e `review`. Chiamiamo questo insieme `A`. Definiamo **copertura** `C(m) = |{c in A: degree_m(c) > 0}| / |A|` e **numero di classi ridondanti** `R(m) = |{c in A: degree_m(c) >= 2}|`. Sono metriche descrittive: due lavoratori connessi alla stessa classe non sono necessariamente intercambiabili per lo stesso ruolo.

### Esercizio pratico 1: non contare più volte i ruoli

In NORMAL, `claude` ha `draft_to_ready_helper`, `test_author` e `review_feedback_applier`, tutti nella classe `fix`, oltre a `builder_fixer` in `net_new_feature` e `lightweight_groomer` in `groom`. Qual è il suo grado nella proiezione lavoratore-classe e quanti percorsi verso ruoli assegnati ha? Perché i numeri differiscono?

> **Risposta:** Il grado proiettato è **3**: `fix`, `net_new_feature`, `groom`. Ha **5** percorsi verso ruoli assegnati, uno primario e quattro secondari. I tre ruoli `fix` diventano un solo arco lavoratore-classe. Considerare cinque ruoli come cinque lavoratori alternativi gonfierebbe falsamente la ridondanza.

## 2. Misurare il taglio prodotto da una modalità

Le assegnazioni primarie e secondarie producono la seguente proiezione in NORMAL. Un `1` indica che almeno un percorso tramite ruolo assegnato sopravvive al filtro della classe:

| Lavoratore | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 1 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

La matrice contiene **9** archi lavoratore-classe. I gradi delle classi sono `fix:2`, `groom:2`, `navigate:1`, `net_new_feature:1`, `review:3`. Quindi `C(NORMAL)=5/5` e `R(NORMAL)=3`. CONSTRAINED blocca `net_new_feature` e `broad_architecture`; DRAINING blocca anche `workflow_policy_change`. Tra queste classi, solo `net_new_feature` ha un percorso assegnato: **entrambe** le modalità conservano 8 archi e quattro classi coperte, con `C=4/5` e `R=3`. HALTED blocca anche `fix`, `groom` e `navigate`, ma non `review`. Restano tre archi, tutti verso `review`: `C(HALTED)=1/5`, `R(HALTED)=1`. Quel rapporto non autorizza operazioni in un sistema fermo; descrive soltanto le dichiarazioni sopravvissute al filtro.

### Esercizio pratico 2: calcolare un taglio, non un'interruzione reale

In DRAINING, quale arco di NORMAL scompare, quanto valgono `C` e `R`, e il calcolo prova che un agente Claude abbia davvero smesso di lavorare?

> **Risposta:** Scompare soltanto `claude → net_new_feature`, l'unico arco assegnato della classe bloccata. Rimangono otto dei nove archi; quattro delle cinque classi sono coperte, quindi `C=4/5`. `fix`, `groom` e `review` hanno ancora grado almeno due, quindi `R=3`. È un taglio del grafo di policy, non una prova di un agente in esecuzione o di una distribuzione reale.

## 3. Provare la fragilità rispetto alla perdita di un lavoratore

Per la modalità `m` e il lavoratore rimosso `w`, definiamo `L_m(w)` come il numero di classi coperte prima della rimozione e scoperte dopo. Elimina `w` e i suoi percorsi, poi ricalcola i gradi. In DRAINING, solo `augment` ha un arco verso `navigate`. Rimuoverlo porta il grado di `navigate` da 1 a 0: `L_DRAINING(augment)=1` e la copertura scende da `4/5` a `3/5`. Rimuovere uno qualsiasi degli altri quattro non fa perdere **nessuna classe intera**, perché resta un altro lavoratore nominato. È una prova di sensibilità tramite rimozione di un vertice, non una stima della probabilità di guasto. Il JSON non registra ogni causa di indisponibilità e condividere una classe non garantisce il ruolo esatto richiesto.

Ridondanza delle classi e ridondanza dei ruoli sono diverse. `review` ha tre lavoratori vicini in DRAINING, ma il ruolo primario `read_only_critic` di `gemini`, il secondario `architecture_summarizer` di `jules` e i ruoli secondari di revisione di `codex` sono assegnazioni differenti. Il grafo mantiene un percorso verso la classe ampia `review` dopo la perdita di un lavoratore. Non garantisce tre sostituti per ogni ruolo richiesto; può servire riassegnazione o escalation.

### Esercizio pratico 3: rimuovere un vertice

Confronta la rimozione di `augment` con quella di `codex` dal grafo DRAINING. Indica classi perse e copertura residua in ciascun caso. Il grafo basta per giudicare se le note di revisione sostitutive avrebbero uguale qualità?

> **Risposta:** Rimuovere `augment` fa perdere `navigate`; restano `fix`, `groom` e `review`, quindi `C=3/5`. Rimuovere `codex` non fa perdere alcuna classe: `claude` conserva `fix`, mentre `jules` e `gemini` conservano `review`; `C=4/5`. Nessun risultato misura qualità, permessi, equivalenza esatta dei ruoli, disponibilità o conclusione di compiti.

## 4. Tenere la semantica del selettore accanto al grafo

Il [selettore consultivo fissato](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L1-L19) consuma la policy. Controlla nell'ordine lavoratore sconosciuto, modalità sconosciuta, ruoli vietati, appartenenza del ruolo richiesto alla corsia e blocco della sua classe ([ordine delle decisioni](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L77-L154)). Un ruolo primario assegnato e non bloccato dà `allow`; un secondario dà `recommend`, non `allow`. Un ruolo vietato dà `block` **prima** del controllo di appartenenza. Un ruolo estraneo alla corsia dà `warn`. Una classe bloccata dà `block` con un codice di backpressure. Sono risposte costruite dal codice, non permessi di modificare lo stato. Il codice di uscita 0 significa **valutato**; la decisione è nel JSON. Un errore di input o policy può dare 2.

In DRAINING, `builder_fixer`, ruolo primario di `claude`, appartiene a `net_new_feature`, bloccata; `test_author`, secondario, appartiene a `fix`, non bloccata. La sorgente prevede `block` per la prima richiesta e `recommend` per la seconda. Ciò **non** vuol dire che `test_author` possa svolgere un compito di costruzione di funzionalità: ruolo richiesto e risultato atteso devono corrispondere al lavoro. `autonomous_merge_actor` è espressamente vietato a `codex`, quindi la sua richiesta prevede `block` anche cambiando modalità. Nessun arco del grafo autorizza un merge.

### Esercizio pratico 4: distinguere percorsi e decisioni

In DRAINING, prevedi le decisioni per `(claude, builder_fixer)`, `(claude, test_author)` e `(codex, autonomous_merge_actor)`. Quale informazione necessaria all'ultima richiesta viene persa salvando solo la proiezione lavoratore-classe?

> **Risposta:** La prima dà `block` perché `net_new_feature` è bloccata; la seconda dà `recommend` perché `test_author` è un ruolo `fix` *secondario* non bloccato; la terza dà `block` perché `autonomous_merge_actor` è nella lista vietata di `codex`. La proiezione non codifica ruoli vietati né ordine dei controlli. L'assenza di un arco per il merge non è un semplice avviso per ruolo sconosciuto né un permesso.

## 5. Rendere falsificabile la misura

I numeri sopra sono stati calcolati dal **JSON fissato**: espansione dei ruoli primari e secondari, associazione a `work_class`, filtro con `mode_blocks` e deduplicazione delle coppie `(lavoratore, classe)`. Uno [script di riproduzione offline](../../../../../scripts/streeling_net003_replay.py) controlla ora separatamente l'interpretazione del selettore. Confronta gli identificatori dei blob Git del selettore e della policy presenti nel checkout con quelli del commit fissato ed enumera le 22 coppie `(lavoratore, ruolo)` assegnate in ciascuna delle quattro modalità. `allow` e `recommend` contano come percorsi assegnati non bloccati; `block` indica un percorso tagliato dalla modalità. La [ricevuta della riproduzione del 12 ottobre 2026](../../../reviews/net-003-selector-replay-2026-10-12.json) registra **22, 21, 21, 8** percorsi di ruolo non bloccati per NORMAL, CONSTRAINED, DRAINING e HALTED, **9, 8, 8, 3** archi lavoratore-classe proiettati e **5, 4, 4, 1** percorsi primari non bloccati. Tutti i risultati corrispondono alle previsioni della policy e del selettore fissati.

La riproduzione confronta la decisione nel JSON, non il codice di uscita del processo. I controlli separati hanno restituito `block` per il ruolo di merge vietato a `codex`, `warn` per un ruolo sconosciuto e `escalate` per una modalità sconosciuta; nessuno appartiene alle 22 coppie assegnate. Una divergenza nei conteggi o nelle decisioni falsificherebbe la regola ipotizzata o rivelerebbe una modifica delle fonti. La concordanza convalida questo modello limitato per la revisione fissata, senza dimostrare pianificazione reale, salute dei lavoratori o correttezza della governance umana. Per riprodurre la ricevuta JSON, esegui `python scripts/streeling_net003_replay.py` dalla radice del repository Demerzel.

### Esercizio pratico 5: progettare l'oracolo della ripetizione

Supponi che `(claude, builder_fixer, DRAINING)` restituisca codice di uscita 0 e decisione JSON `block`. Un collega conta un percorso attivo perché il processo è riuscito. Qual è la classificazione corretta? Indica un numero che, se diverso dalle previsioni, falsificherebbe l'estrazione del grafo.

> **Risposta:** È un **percorso verso un ruolo assegnato ma bloccato**. Il codice 0 indica che la richiesta consultiva è stata valutata, non autorizzata. La ripetizione dovrebbe trovare 21 percorsi assegnati non bloccati in DRAINING e 8 archi lavoratore-classe dopo la proiezione. Trovare, per esempio, 22 percorsi o 9 archi con policy e script fissati falsificherebbe l'estrazione. Da solo non dimostrerebbe un incidente di produzione.

## Evidenze e limiti

- La [policy delle corsie](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) e il [selettore](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) sono fissati al commit Demerzel `ecdc6c27559bb1a11343cfad33687465893e9891`. La riproduzione locale della sezione 5 ha verificato gli identificatori dei blob Git prima di usare i file del checkout. È un calcolo riproducibile e un'invocazione di prova del selettore, non una misura di agenti attivi.
- Il grafo raggruppa ruoli assegnati differenti in classi. Esclude i ruoli vietati e non conserva tutti gli input, l'ordine delle decisioni o l'autorità del selettore. `allow` e `recommend` sono valori consultivi, non ricevute di completamento.
- Rimuovere lavoratori o tagliare modalità sono esperimenti di sensibilità su un grafo statico dichiarato. Prima di affermare qualcosa sull'instradamento operativo, controlla la revisione corrente della policy, richiesta e decisione effettive, presenza e permessi del lavoratore, e artefatto o ricevuta del compito. Revisione disciplinare, tentativi degli studenti, revisione della traduzione, sincronizzazione e build di Learn e lettura pubblica anonima restano in sospeso.
