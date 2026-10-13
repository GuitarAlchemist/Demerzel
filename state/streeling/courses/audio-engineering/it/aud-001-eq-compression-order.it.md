---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Verificare l'ordine di EQ e compressione su un segnale di chitarra"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-004
version: "1.1.0"
---

# Verificare l'ordine di EQ e compressione su un segnale di chitarra

> **Dipartimento di Ingegneria Audio** | Livello: intermedio | Durata: 35 minuti | Bozza italiana rivista; revisioni disciplinare, didattica e linguistica e pubblicazione in sospeso

## Obiettivi e domanda del progetto

Distinguere un filtro da un processore dipendente dal livello, dimostrare con un piccolo calcolo che l'ordine conta e progettare un confronto offline falsificabile da una futura implementazione di compressore: questi sono gli obiettivi. **Domanda del progetto:** se GA valutasse l'elaborazione di una registrazione della corda E2 a vuoto o del render del suo motore di chitarra, mettere una EQ scelta prima della compressione cambierebbe attacco e andamento del livello rispetto a mettere la *stessa* EQ dopo? Una decisione richiede uscite misurate sulla stessa sorgente, non una regola generica su quale ordine suoni più naturale.

La [fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) contiene una coppia concreta: un WAV mono registrato di E2 a vuoto e un WAV mono E2 renderizzato nativamente da GA, entrambi di quattro secondi a 44.100 Hz. Il primo attacco registrato inizia **intorno a 1.1 s**; ne compare un altro verso **2.75 s**. Il render inizia al tempo zero del file. Le [misure della fixture](../../../fixtures/guitar-acoustics/gas-001/measurements.json) mostrano differenze di parziali e decadimento in finestre selezionate, senza classificare il realismo o dimostrare che un file richieda compressione. Conserva intatti entrambi i WAV originali. Qui la registrazione è il primo input proposto; il render servirebbe solo per una replica successiva e identificata separatamente. Non attribuire all'ordine differenze tra un file elaborato e uno non elaborato.

Il [motore audio nel browser GA al commit fissato `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) carica il motore WASM in un [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), lo collega agli altoparlanti e offre un percorso MediaRecorder. Il render GAS-001 viene da una **build nativa della stessa sorgente Rust**, non da una cattura del worklet. La sorgente ispezionata prova il percorso del segnale di chitarra, non una catena EQ/compressore nel demo. Al [commit IX `bd1336b`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs), `FirFilter` fornisce la progettazione di filtri passa-basso e passa-alto e il metodo `apply` sui campioni. Può servire come componente per un filtro offline. Questi artefatti fissati non attestano un compressore implementato: prima di un vero A/B occorre specificarlo e revisionarlo.

## 1. Definire precisamente le due operazioni

Un filtro FIR è lineare: dati coefficienti `h`, la sua uscita è `E(x)[n] = Σ_k h[k] x[n-k]`, con una regola esplicita ai bordi. `FirFilter::apply` di IX parte da un'uscita inizializzata a zero e include solo termini con indice di input non negativo. Un passa-basso o passa-alto può cambiare il livello che raggiunge un rivelatore successivo. La risposta esatta dipende dai coefficienti; il filtro può anche spostare o allargare un attacco. Chiamare ogni impostazione “EQ correttiva” non dimostra che migliori il segnale di chitarra.

Un compressore è **dipendente dal livello**. Il guadagno dipende dall'ingresso e, in un progetto convenzionale, da un inviluppo del rivelatore con stato di attacco e rilascio. La forma d'onda può cambiare in base a soglia, rapporto, tipo di rivelatore, costanti di tempo, collegamento dei canali, guadagno di compensazione e inizializzazione. Registra tutti questi dettagli. Un compressore non è per forza selettivo in frequenza: un rivelatore a banda intera risponde al livello della forma d'onda, a cui possono contribuire più parziali. Dire che il compressore “sente 200 Hz” è informale, non identifica con certezza la componente che ha causato la riduzione. Filtro sidechain, compressione multibanda ed EQ dinamica sarebbero esperimenti diversi.

Siano `E` l'EQ scelta e `C` il compressore. Le due catene proposte sono `A = E(C(x))` (**Comp→EQ**) e `B = C(E(x))` (**EQ→Comp**). Usa gli stessi `x`, coefficienti EQ, parametri del compressore, frequenza di campionamento e formato dei canali in entrambe. In A, `C` vede `x` grezzo; in B vede `E(x)` filtrato. L'EQ finale di A non può annullare una decisione già presa dal rivelatore. In B, il compressore può reagire a picchi creati o rimossi dall'EQ. Nessun ordine è una scelta universale: contano obiettivo sonoro e compromessi misurati.

### Esercizio pratico 1: individuare l'ingresso del rivelatore

Che cosa entra esattamente in `C` nelle catene A e B? Se l'EQ aumenta una parziale di chitarra, quale catena *potrebbe* modificare per questo la riduzione di guadagno?

> **Risposta:** In A, `C` riceve `x` non filtrato; in B riceve `E(x)`. L'aumento della parziale può influire direttamente sul rivelatore a banda intera in B. In A, l'EQ arriva dopo e non cambia la decisione di guadagno precedente. È una descrizione del percorso causale, non una previsione dell'udibilità o della quantità di riduzione.

## 2. Dimostrare l'effetto dell'ordine con una fixture sintetica

Usa un segnale di quattro campioni volutamente **sintetico**, `x=[0,2,0,0]`, con storia iniziale nulla. Definisci il FIR `E` mediante `h=[0.5,0.5]`: `E(x)[n]=0.5x[n]+0.5x[n-1]` per i campioni disponibili. Questa media a due coefficienti è un esempio matematico di passa-basso, **non** un'EQ consigliata per chitarra né il risultato del progettista `lowpass` di IX. Definisci un compressore didattico senza memoria, con soglia `T=1`, rapporto `R=2:1`, senza guadagno di compensazione né attacco/rilascio: `C(v)=sign(v) × (|v| if |v|<=1 else 1+(|v|-1)/2)`. Trasforma il campione positivo `2` in `1.5`. Un vero compressore a inviluppo avrebbe altro stato e potrebbe produrre numeri diversi.

Per A, `C(x)=[0,1.5,0,0]` e quindi `E(C(x))=[0,0.75,0.75,0]`. Per B, `E(x)=[0,1,1,0]` e poi `C(E(x))=[0,1,1,0]`, poiché i due campioni filtrati non superano la soglia. Le uscite differiscono di `0.25` ai campioni 1 e 2. È un controesempio esatto a `E∘C = C∘E` per questi operatori. **Non** misura la registrazione GAS-001, non predice un plugin non specificato e non dimostra che B suoni meglio.

Anche i picchi diversi, `0.75` per A e `1` per B, sconsigliano di giudicare l'ordine a volumi non controllati. Un confronto d'ascolto richiede un livellamento dichiarato **dopo** ogni catena completa, con i guadagni registrati. Non usare soglie diverse per forzare una riduzione di guadagno simile: cambierebbe la domanda sperimentale. Se entrambe le catene restano sotto soglia in un brano reale, possono risultare uguali o quasi nonostante il controesempio sintetico.

### Esercizio pratico 2: calcolare le due catene

Con `x`, `h` e `C` dichiarati, scrivi A e B. Quanto vale `B[1]-A[1]` e che cosa giustifica questo calcolo?

> **Risposta:** `A=[0,0.75,0.75,0]`; `B=[0,1,1,0]`; `B[1]-A[1]=0.25`. Gli operatori specificati non commutano per questo ingresso sintetico. Il calcolo non fornisce un verdetto d'ascolto né il risultato per un compressore reale a inviluppo o per il WAV di chitarra.

### Esercizio pratico 3: gestire il bordo

Con storia iniziale nulla e `h=[0.5,0.5]`, quanto valgono `E([2,0])[0]` e `E([2,0])[1]`? Perché il test offline deve documentare bordi e latenza?

> **Risposta:** Entrambi valgono `1`. All'indice 0, il campione precedente mancante contribuisce zero; all'indice 1, il campione precedente è `2`. Un riempimento o un warm-up diverso cambierebbe l'attacco. FIR pratici più lunghi possono aggiungere ritardo di gruppo: prima di interpretare la differenza tra tempi di picco occorrono uscite allineate e una regola di bordo registrata.

## 3. Progettare un test A/B di chitarra falsificabile

Quanto segue è un **esperimento offline proposto, non eseguito**. Parti dalla registrazione `deb-low-e-open.wav` nel [direttorio della fixture](../../../fixtures/guitar-acoustics/gas-001/README.md), con SHA-256 `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`. Decodifica una volta i suoi campioni WAV mono float32 e conserva i byte originali. Registra decodificatore, frequenza di campionamento, hash e primo attacco approssimativo; guarda la forma d'onda prima di fissare una finestra che escluda il secondo attacco. Una seconda prova può usare `ga-engine-e2-open-4s.wav`, ma riportala separatamente: proviene da un render nativo, con attacco e origine diversi.

Prima di implementare il futuro compressore, definisci un contratto dei parametri: soglia in dBFS, rapporto, unità di attacco e rilascio, rivelatore di picco o RMS, lookahead, knee, makeup gain, reset dello stato e comportamento al primo campione. Fissa revisione e test del codice. Usa una sola EQ deterministica: pubblica coefficienti FIR letterali oppure fissa la [sorgente del filtro IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) e registra taglio, ordine, coefficienti e gestione dei bordi. In entrambe le catene usa le *stesse* impostazioni e reinizializza indipendentemente lo stato prima di ogni render. Esporta WAV A e B senza perdita alla stessa frequenza e conserva traccia di riduzione del guadagno, numero di campioni e manifesto di elaborazione. Non attribuire a GA o IX una catena combinata già disponibile.

Scegli la finestra del primo pizzico rispetto all'attacco registrato, **circa a 1.1 s**, annotando l'indice di campione nel manifesto. Per ogni catena riporta campione e istante del picco, RMS a finestra breve o inviluppo vicino all'attacco, RMS successivo e traccia della riduzione di guadagno. Livella l'uscita per l'ascolto e registra il guadagno applicato, distinguendo misure grezze e livellate. Evita clipping dopo compensazione o livellamento. Se la latenza FIR differisce da un percorso bypass, allinea con un ritardo documentato o una regola di correlazione incrociata prima di confrontare gli istanti dei picchi. Un eventuale test d'ascolto approvato in seguito dovrebbe nascondere le etichette, randomizzare l'ordine e consentire «nessuna differenza percepibile»; resta distinto dalla verifica numerica.

Il **falsificatore** dell'ipotesi ristretta «la posizione dell'EQ cambia questa sequenza con queste impostazioni fissate» sarebbe trovare A e B uguali campione per campione entro una tolleranza numerica predefinita, o vedere sparire la differenza apparente dopo la correzione di allineamento, reset o trattamento del livello. Se differiscono, esamina ingresso del rivelatore e tracce di guadagno per attribuire il meccanismo. Una differenza non prova che un ordine sia più naturale. Con EQ neutra o compressore che non supera mai la soglia, un risultato nullo è plausibile e utile. Affermare che un ordine preservi meglio l'attacco richiederebbe metrica dichiarata, direzione, tolleranza accettabile e ascolto se la percezione fa parte dell'affermazione.

### Esercizio pratico 4: mantenere valida la fixture

Un test proposto elabora la registrazione nell'intervallo del file `0.0–1.0 s`, la confronta con il render nello stesso intervallo e conclude che EQ→Comp preserva meglio l'attacco. Indica due problemi indipendenti.

> **Risposta:** Il primo attacco registrato arriva solo verso `1.1 s`, quindi `0.0–1.0 s` è soprattutto pre-attacco, mentre il render comincia a zero. Le finestre non sono allineate agli attacchi. Inoltre, due file sorgente diversi non isolano l'ordine: A e B devono usare lo **stesso WAV sorgente**. Nessuna fixture è un benchmark convalidato di realismo.

### Esercizio pratico 5: scegliere il prossimo controllo

Una prova futura trova una differenza di `0.2 dB` nel RMS della finestra del primo pizzico, ma le uscite non sono allineate e manca il manifesto delle impostazioni del compressore. Si può preferire un ordine? Quali prove chiedere?

> **Risposta:** No. Conserva hash e finestra d'ingresso, pubblica versione e impostazioni del compressore, verifica reset indipendenti, allinea latenza e attacco, conferma coefficienti EQ uguali e assenza di clipping; poi ripeti e confronta misure grezze e tracce della riduzione. Per un'eventuale affermazione sulla qualità sonora, livella dopo l'elaborazione per un ascolto cieco separato. `0.2 dB` da solo non identifica lo stadio responsabile né stabilisce una preferenza.

## Evidenze e limiti

- Il [README della fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) documenta WAV E2 registrato e renderizzato nativamente, hash, attribuzione, attacchi approssimativi e limiti delle misure. La [lezione GAS-001](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) e le misure salvate riguardano il confronto *grezzo*, non un test di EQ/compressione.
- Il [percorso browser GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) e il [worklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) fissati documentano il demo; il [codice FIR IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) documenta un'operazione filtro disponibile. Non dimostrano un compressore implementato, un test dell'ordine o un WAV elaborato.
- Il calcolo sui quattro campioni è sintetico. Test A/B, parametri e metriche sono proposti. Nessun compressore è stato costruito o eseguito per questa lezione; non esistono qui un WAV di chitarra elaborato, un giudizio cieco o una decisione di instradamento in produzione. Revisioni disciplinare, didattica e linguistica, distribuzione su Learn e lettura pubblica anonima restano in sospeso. Il ciclo del 2026-03-23 rimane un artefatto storico sulla voce; questa revisione usa il nuovo ciclo.
