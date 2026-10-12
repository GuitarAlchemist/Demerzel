---
module_id: phy-003-sampling-aliasing-guitar-engine
department: physics
course: Campionamento e aliasing al confine del motore per chitarra GA
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-003
version: "0.1.0"
---

# Campionamento e aliasing al confine del motore per chitarra GA

> **Dipartimento di Fisica** | Livello intermedio | 35 minuti | Bozza italiana; revisione e pubblicazione in sospeso

## Obiettivi

Calcolerai il limite di Nyquist e una frequenza di alias, individuerai la frequenza di campionamento realmente ricevuta dal motore Rust di GA e progetterai una prova offline che possa rilevare l'aliasing senza scambiare un rischio calcolato per un difetto misurato. [PHY-001](../it/phy-001-science-of-guitar-sound.it.md) introduce gli armonici della chitarra. [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) sceglie le finestre di analisi per note variabili. Qui la domanda è più a monte: **quali frequenze continue può rappresentare un segnale campionato, e cosa occorre fare prima di acquisizione, sintesi o conversione della frequenza?**

## 1. Collegare la frequenza all'artefatto, non al nome della nota

La [fixture GAS-001 fissata](../../../fixtures/guitar-acoustics/gas-001/README.md) contiene un Mi2 a vuoto registrato per quattro secondi e un render nativo di quattro secondi del motore Rust di GA. Entrambi i file sono mono a **44 100 campioni al secondo**. Il render chiama `engine_note_on(82.4069 Hz, 0.1)`; l'identità E2 del file registrato è un'etichetta del dataset, non una misura della frequenza. Il render proviene da una build nativa, **non** da una cattura dell'AudioWorklet nel browser. La distinzione conta quando si indaga un artefatto audio.

Al commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), il [collegamento audio del browser](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) invia `audioContext.sampleRate` all'[AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js). Quest'ultimo chiama `engine_init(srToUse)` e copia i campioni mono generati nei canali di uscita del browser. Il [motore Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) conserva la frequenza e la usa per i coefficienti dei risonatori e la lunghezza della linea di ritardo. Il WAV fissato a 44,1 kHz **non** prova quindi che ogni sessione browser usi 44,1 kHz. Registra la frequenza effettiva del contesto e il percorso di acquisizione prima di confrontare una registrazione browser con GAS-001.

Per una durata `T`, il numero di campioni è `N = f_s T`. Quattro secondi a 44 100 Hz danno **176 400 campioni** per canale mono; a 48 000 Hz sarebbero **192 000**. Nessun conteggio indica se l'ingresso analogico sia stato filtrato correttamente o se il sintetizzatore abbia evitato alias.

### Esercizio pratico 1

Una persona vede il render GAS-001 a 44,1 kHz e scrive: «Nel browser il motore GA funziona sempre a 44,1 kHz». Che cosa sostengono davvero le fonti e che cosa deve registrare una prova nel browser?

> **Risposta:** GAS-001 fissa **il proprio WAV renderizzato nativamente** a 44 100 Hz. Il collegamento browser passa `audioContext.sampleRate` al worklet e al motore Rust; il valore effettivo deve essere osservato in quella sessione. Registra frequenza del contesto, frequenza e codec dell'uscita o registrazione, revisione del motore e percorso di cattura. Un WAV nativo non è una cattura browser.

## 2. Calcolare la banda rappresentabile prima degli armonici

Per un segnale reale campionato uniformemente a `f_s`, la frequenza di Nyquist è `f_N = f_s/2`: **22 050 Hz** a 44 100 Hz e **24 000 Hz** a 48 000 Hz. In linea di principio, dalle sue misure si può ricostruire un ingresso continuo ideale limitato in banda, con contenuto strettamente inferiore a `f_N`. Un'acquisizione reale richiede un filtro anti-alias **prima** del campionamento, con banda di transizione sotto Nyquist. `f_N` è un confine matematico, non una promessa di filtro perfetto in microfono, convertitore, motore o esportazione.

Il Mi2 a vuoto scelto ha `f_0 = 82.4069 Hz`. Il suo parziale intero ideale `k` sarebbe a `k f_0`, ma una chitarra fisica o sintetizzata non possiede necessariamente tutti i parziali né li mantiene a multipli esatti. A 44,1 kHz, `267 f_0 = 22,002.6423 Hz` è sotto Nyquist e `268 f_0 = 22,085.0492 Hz` sopra. A 48 kHz il confine passa tra il parziale **291** (`23,980.4079 Hz`) e il **292** (`24,062.8148 Hz`). Sono *limiti teorici di indice* per la fondamentale scelta, non un conteggio di parziali udibili o misurati. Un margine pratico va posto sotto il confine esatto: i filtri hanno bisogno di una banda di transizione e conta l'implementazione.

### Esercizio pratico 2

Per lo stesso E2 ideale, calcola l'armonico intero più alto strettamente sotto Nyquist a 44,1 e 48 kHz. Questo dimostra che tali armonici esistono nella fixture?

> **Risposta:** `floor(22,050 / 82.4069) = 267` e `floor(24,000 / 82.4069) = 291`. I parziali successivi 268 e 292 superano i rispettivi limiti. L'aritmetica non dimostra che nei WAV ci sia un 267° o 291° parziale rilevabile. Per misurarne i livelli servono i file, una finestra adatta, un rumore di fondo e limiti di analisi espliciti.

## 3. Calcolare a mano un alias

Campionare una sinusoide continua di `f` Hz produce `sin(2π f n / f_s)` agli indici interi `n`. Aggiungere o sottrarre un multiplo intero di `f_s` dà gli stessi campioni, salvo un cambiamento di segno o fase. Per la frequenza di alias in modulo, ripiega `f` tramite multipli di `f_s` dentro `[0, f_s/2]`; equivalentemente, scegli un intero `m` affinché `|f - m f_s|` cada nell'intervallo. È un calcolo **sintetico di tono singolo**, non un'osservazione su GAS-001.

Considera una sinusoide continua a **23 000 Hz**. A 44,1 kHz supera Nyquist di 950 Hz e si ripiega a `|23,000 - 44,100| = 21,100 Hz`. La sequenza campionata equivale a una sinusoide a 21 100 Hz con segno o fase diversi. A 48 kHz, 23 000 Hz resta sotto il limite di 24 000 Hz e non si ripiega. Ricampionare successivamente la cattura da 44,1 a 48 kHz non ripristina l'ingresso originale a 23 000 Hz: i campioni non distinguono le due origini continue.

In un motore per chitarra, eccitazione a banda larga del pizzico, elaborazioni non lineari e parziali alti sono motivi per **verificare** il confine. L'[eccitazione Rust fissata](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) usa rumore filtrato in una linea di ritardo e tratta i campioni. L'ispezione non prova alias udibili o misurabili in uscita. Una frequenza maggiore può spostare la soglia di ripiegamento ma cambia dimensioni dei buffer e costo di calcolo; non sostituisce limitazione di banda controllata e misure.

### Esercizio pratico 3

Un'eccitazione proposta ha una componente continua a 30 000 Hz. Dove collocherebbe il suo alias un campionatore ideale a 44,1 e 48 kHz?

> **Risposta:** A 44,1 kHz, `|30,000 - 44,100| = 14,100 Hz`; a 48 kHz, `|30,000 - 48,000| = 18,000 Hz`. Sono ripiegamenti di una sinusoide ideale, non picchi spettrali previsti del motore GA. Un filtro anti-alias a monte può attenuare la componente prima dell'acquisizione; un generatore digitale deve evitare contenuto fuori banda o controllarne il ripiegamento.

### Esercizio pratico 4

Una persona ricampiona a 48 kHz una registrazione a 44,1 kHz con un picco a 21,1 kHz e dice: «Ora che Nyquist è 24 kHz, la sinusoide originale a 23 kHz è stata recuperata». Spiega l'errore.

> **Risposta:** La sequenza a 44,1 kHz è compatibile sia con un tono a 21,1 kHz sia con uno a 23 kHz, salvo una differenza di fase o segno. La conversione può interpolare o filtrare i dati disponibili, non dedurne l'origine continua. Evita il ripiegamento **prima** del campionamento originale con un filtro analogico anti-alias, oppure genera contenuto digitale limitato in banda alla frequenza desiderata.

## 4. Rendere falsificabile il rischio per GA

Le [misure GAS-001](../../../fixtures/guitar-acoustics/gas-001/measurements.json) riportano picchi vicino a E2 e pochi parziali bassi, non un'indagine sugli alias ad alta frequenza. Un grafico dei due WAV a 44,1 kHz da solo non rivela la frequenza d'origine di un alias: un picco sotto Nyquist può avere varie cause. La registrazione ha inoltre un primo attacco approssimativo a 1,1 s e un secondo verso 2,75 s, mentre il render parte da zero. Conserva intervalli allineati agli attacchi prima di confrontare spettri; [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) spiega il problema della scelta temporale.

Una prova offline inizierebbe da un **riferimento sintetico noto**: genera una sinusoide a 23 kHz con frequenza di riferimento superiore, campionala a 44,1 e 48 kHz registrando la scelta del filtro e verifica il ripiegamento previsto a 21,1 kHz solo nel ramo a 44,1 kHz volutamente non filtrato. Poi renderizza la stessa sorgente GA fissata, con nota, velocità, profilo e durata uguali, a entrambe le frequenze tramite chiamate **native**, oppure cattura entrambi i casi nel **browser** registrandone la frequenza; non mescolare i percorsi senza dichiararlo. Salva impostazioni di ingresso, build esatta, hash WAV, frequenza, livello di picco e finestre spettrali. Confronta con un riferimento controllato a frequenza corrispondente su più note e velocità. Se un tono inatteso si sposta secondo la previsione di alias cambiando la frequenza di render, indaga lo stadio che lo produce; se resta alla stessa frequenza fisica, l'ipotesi semplice di alias si indebolisce. Conferma con una modifica del codice mirata allo stadio sospetto e ripeti l'ascolto a livello abbinato. Il protocollo è **proposto**: questi render, catture e ascolti aggiuntivi **non** sono stati eseguiti per la lezione.

Per future conversioni di frequenza, documenta frequenze d'origine e destinazione, bande passante e di arresto del filtro, ritardo, controlli di clipping e se il riferimento fu catturato prima o dopo codifica con perdita. Il collegamento browser offre un [percorso MediaRecorder opzionale](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js); non presupporre che il suo blob sia un WAV grezzo a 44,1 kHz. Tieni tale percorso distinto dal render nativo della fixture.

### Esercizio pratico 5

In un render del motore a 44,1 kHz compare un picco a 21,1 kHz. Basta per attribuirlo a un alias di sintesi da 23 kHz? Indica la prossima comparazione decisiva e un controllo.

> **Risposta:** No. Potrebbe essere una componente in banda, un alias di un'altra componente fuori banda o un artefatto di cattura. Renderizza la stessa configurazione fissata del motore a 48 kHz e confronta spettri alti allineati agli attacchi: una sorgente vicina a 23 kHz dovrebbe apparire lì verso 23 kHz, mentre il suo alias a 44,1 kHz sarebbe verso 21,1 kHz. Controlla revisione del motore, nota, velocità, profilo e percorso di acquisizione; ispeziona lo stadio del segnale o aggiungi una modifica mirata di limitazione di banda prima di attribuire la causa. Lo spostamento previsto è una **prova**, non un risultato osservato.

## Fonti e limiti attuali

- [Fixture GAS-001 fissata, provenienza e frequenze](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), con il [README locale](../../../fixtures/guitar-acoustics/gas-001/README.md). La registrazione è attribuita a **collegefishiesd** sotto CC BY-SA 4.0; la lezione non ne riproduce l'audio.
- Commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo): [collegamento browser](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) e [motore Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs).
- Conteggi di campioni, limiti degli indici armonici e ripiegamenti di sinusoidi sono calcoli diretti dalle frequenze dichiarate. Per PHY-003 non sono stati completati nuove misure di alias alti su GAS-001, catture browser, revisione indipendente della materia, prove di studenti, revisione linguistica o lettura pubblica.
