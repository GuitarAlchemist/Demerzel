---
module_id: gas-003-decay-calibration-open-e
department: guitar-acoustics
course: "Calibrare un test del decadimento del Mi a vuoto per il motore di chitarra GA"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-12-003
version: "0.1.0"
---

# Calibrare un test del decadimento del Mi a vuoto per il motore di chitarra GA

> **Dipartimento di acustica e sintesi della chitarra** | Intermedio | 40 minuti | Bozza tradotta dall'IA; revisione in attesa

## Obiettivi

Imparerai a distinguere una *misura* di decadimento da un *parametro* Rust, a calcolare lo scarto della coppia fissata di Mi a vuoto, a seguire il coefficiente di retroazione del motore e a definire un esperimento nativo con un solo parametro, una condizione di falsificazione e controlli di sicurezza. [GAS-001](../en/gas-001-open-string-audio-evidence.md) stabilisce la coppia registrata e sintetizzata. [GAS-002](../en/gas-002-brightness-control-and-evaluation-gate.md) verifica un'ipotesi sulla brillantezza per un rapporto armonico locale. Qui chiediamo: **una modifica controllata al decay di GA può avvicinare il calo di livello del Mi a vuoto a quello registrato senza danneggiare attacco, altezza o altre note?** Nessun candidato di decay è stato ancora renderizzato per questa lezione.

## 1. Parti dall'inviluppo misurato, non dalla manopola

Il [fixture GAS-001](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) fissato contiene due WAV mono di quattro secondi a 44.100 Hz: una registrazione acustica separata, etichettata come Mi2 a vuoto dal suo dataset, e un render **nativo** del motore Rust GA al commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. Il render usa il profilo chitarra 0 predefinito e `engine_note_on(82.4069 Hz, velocity 0.1)`. Non è una cattura dell'AudioWorklet nel browser. Il [README del fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md) documenta hash, limiti di provenienza, credito e attribuzione CC BY-SA 4.0 della registrazione.

Il [JSON delle misure](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) riporta una variazione RMS tardiva meno iniziale di **−3.9 dB** per la registrazione e **−1.1 dB** per il render. Lo [script di misura](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) usa le finestre 0.2–0.4 s e 1.0–1.2 s **dopo il primo attacco di ciascun file**. Il primo attacco registrato è circa a 1.1 s e ce n'è un altro vicino a 2.75 s; il render parte da zero. Nel file registrato le finestre cadono quindi circa a **1.3–1.5** e **2.1–2.3 s**, prima del secondo attacco. Non sono costanti di decadimento dell'intero file.

Il calo scelto del render è **meno negativo di 2.8 dB**: `−1.1 − (−3.9) = +2.8 dB`. L'errore assoluto rispetto alla variazione registrata è `|−1.1 − (−3.9)| = 2.8 dB`. Entrambi i valori sono già arrotondati al decimo. I WAV differiscono per livello iniziale, strumento, microfono, stanza e pizzicata; qui confrontare le *variazioni* interne a ciascun file è più utile che confrontare gli RMS assoluti in dBFS. Neppure questa differenza rivela quale parametro l'abbia causata o quale suono preferiscano gli ascoltatori.

### Esercizio 1 — Leggi lo scarto

Con i valori salvati, calcola la differenza con segno render meno registrazione nella variazione tardiva meno iniziale e l'errore assoluto. Un errore di 2.8 dB significa che l'intero render è più forte di 2.8 dB?

> **Risposta:** `−1.1 − (−3.9) = +2.8 dB`; l'errore assoluto è `2.8 dB`. Il render cala meno fra le due finestre RMS riferite all'attacco. Non è un confronto di sonorità dell'intero file né una prova di preferenza d'ascolto.

### Esercizio 2 — Escludi il secondo attacco

In quali istanti del file cadono le due finestre della registrazione se il primo attacco è circa a 1.1 s? Perché una finestra tardiva che comincia a 2.8 s non è adatta alla prima nota?

> **Risposta:** La finestra iniziale è circa `1.1 + [0.2, 0.4] = 1.3–1.5 s`; quella tardiva è `1.1 + [1.0, 1.2] = 2.1–2.3 s`. Da 2.8 s si è già oltre l'altro attacco vicino a 2.75 s: si mescolerebbe un nuovo evento al presunto decadimento. L'istante d'attacco è approssimato; ripeti l'analisi variandolo leggermente prima di formulare conclusioni forti.

## 2. Segui il parametro Rust e il coefficiente effettivo

Nel [motore Rust GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) fissato, `Engine::new` parte con `decay = 0.9968`, ma poi seleziona il profilo predefinito 0, che imposta il **decay di base a 0.9978**. La funzione esportata `engine_set_decay` limita la richiesta a `[0.95, 0.9999]`. Scegli il profilo **prima** di applicare il candidato: una scelta successiva riscrive decay e altri controlli. Il [renderizzatore del fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py) chiama `engine_init` ed `engine_note_on`, ma non `engine_set_decay`; serve un'estensione documentata o un harness separato. Qui non è riportata alcuna esecuzione candidata.

Le espressioni pertinenti nel ciclo di rendering sono:

```text
f_norm = clamp((voice_frequency_hz - 82) / (330 - 82), 0, 1)
voice.sustain = min(0.995 + 0.006 * (1 - f_norm), 0.9998)  # assigned at note excitation
feedback_decay = (base_decay + 0.0025 * (1 - f_norm)) * voice.sustain
```

Per gli `82.4069 Hz` nominali del fixture, `f_norm ≈ 0.00164073`. L'espressione sustain senza limite vale circa `1.00099016`, quindi `voice.sustain = 0.9998`. Con base `0.9978`, si ottiene `(0.9978 + 0.0025 × (1 − 0.00164073)) × 0.9998 ≈ 1.00009584`. Una base **proposta** di `0.9976` dà circa **0.99989588**. Entrambe le basi rientrano nei limiti del setter.

Questi sono **coefficienti di retroazione calcolati dal sorgente**, non tassi misurati di decadimento dell'inviluppo. Il ciclo combina inoltre campioni della linea di ritardo, dispersione passa-tutto, un passa-basso con stato miscelato secondo la brillantezza, rumore d'attacco, risonatori e riverbero. Un coefficiente leggermente superiore a uno in una sola espressione **non dimostra** di per sé un'uscita instabile o un difetto udibile. Un coefficiente minore non predice neppure una specifica variazione in dB del WAV. Occorre misurare l'uscita con un metodo fisso.

`attack_decay` controlla separatamente l'evoluzione del rumore d'attacco; `reverb_mix` influisce sulla coda; la brillantezza modifica la miscela nella retroazione. Non cambiarli insieme al candidato di decay, altrimenti la causa di un eventuale effetto diventa ambigua. GAS-002 tratta già la brillantezza; qui resta fissa.

### Esercizio 3 — Calcola, poi limita l'inferenza

A `82.4069 Hz`, quale limite di sustain si applica e quali coefficienti effettivi approssimativi risultano dalle basi `0.9978` e `0.9976`? Il primo valore sopra uno dimostra che il WAV GA salvato aumenta di livello nel tempo?

> **Risposta:** `f_norm ≈ 0.00164073`; il sustain senza limite supera `0.9998`, dunque il limite è `0.9998`. L'espressione dà circa `1.00009584` per `0.9978` e `0.99989588` per `0.9976`. No: è un coefficiente in un sistema filtrato, con stato, risonanze e riverbero. Nelle finestre selezionate il WAV salvato mostra invece `−1.1 dB`; il coefficiente da solo non ne predice l'inviluppo.

## 3. Predichiara un esperimento a un parametro

Una prova nativa controllata compilerebbe **la stessa revisione Rust fissata** e inizializzerebbe un motore nuovo per ciascun braccio a 44.100 Hz. Mantieni profilo 0, Mi2 `82.4069 Hz`, velocità `0.1`, durata di quattro secondi, compilatore, codifica WAV e ogni altro controllo. Il braccio di riferimento usa `0.9978`. In quello candidato chiama `engine_set_decay(0.9976)` **dopo** inizializzazione e scelta del profilo, **prima** di `engine_note_on`. Registra ordine delle chiamate, valore richiesto, hash di entrambi i WAV e attacco scelto. Il codice imposta un seme casuale fisso alla creazione, ma motori nuovi e identica compilazione evitano il trascinamento dello stato. Il renderizzatore attuale non offre un'opzione decay: adattalo o sostituiscilo e revisiona lo script prima di affermare un risultato empirico. Il confronto nativo non certifica l'AudioWorklet nel browser: verifica separatamente quella via se sarà il prodotto distribuito.

Applica la stessa procedura di misura ai due bracci. Una **soglia didattica proposta** richiede un errore assoluto almeno **1.0 dB inferiore** all'errore di riferimento arrotondato di `2.8 dB`: obiettivo `≤ 1.8 dB` rispetto ai `−3.9 dB` registrati. Sui numeri arrotondati corrisponde a un calo candidato fra **−5.7 e −2.1 dB**. Per decidere davvero, usa le misure WAV non arrotondate e registra una tolleranza, senza giudicare al confine del decimo usando il JSON arrotondato. È una soglia didattica scelta in anticipo, **non** uno standard di prodotto GA né una previsione che `0.9976` passerà.

Proteggi il confronto: niente clipping o quasi clipping (ampiezza di picco assoluta proposta **sotto 0.95**), fondamentale Mi2 vicina al riferimento con la stessa ricerca del picco su un secondo, controllo dell'attacco iniziale e delle tracce del secondo e quarto parziale. Un RMS complessivo migliore può nascondere un transiente o una coda spettrale danneggiati. Ripeti su altre corde, note e velocità prima di generalizzare. Esamina giudizi d'ascolto in cieco e con livelli pareggiati: la somiglianza numerica con una chitarra esterna non stabilisce il realismo percepito. Se il candidato non supera `≤1.8 dB` o viola un controllo, respingi **questa impostazione candidata in questa prova** e riporta il risultato. Il fallimento non dimostra che ogni modifica del decay sia inutile.

### Esercizio 4 — Applica la soglia proposta

Con i valori arrotondati, qual è l'errore assoluto massimo per un miglioramento di 1.0 dB? Quale intervallo di cali candidati comporta attorno a `−3.9 dB`? Un candidato nell'intervallo ma con picco `0.98` supera tutti i controlli?

> **Risposta:** `2.8 − 1.0 = 1.8 dB`; `|candidate − (−3.9)| ≤ 1.8` implica `−5.7 ≤ candidate ≤ −2.1 dB`. Un picco di `0.98` fallisce il controllo proposto `<0.95`, anche se il decadimento passa. È aritmetica su una soglia proposta, non la misura di un candidato.

### Esercizio 5 — Formula un falsificatore

Un agente sostiene che abbassare la base a `0.9976` migliori lo smorzamento del Mi2 GA. Quali artefatti controllati minimi e quale risultato smentirebbero l'affermazione secondo questa soglia? Cosa rimarrebbe ignoto dopo una prova positiva su un solo Mi2?

> **Risposta:** Salva revisione e compilazione esatte del motore, ordine delle chiamate, WAV nativi di riferimento e candidato ottenuti da motori nuovi e relativi hash, misure allineate all'attacco e controlli su picco, parziali e attacco. Se l'errore assoluto non arrotondato non scende almeno di 1.0 dB, o fallisce un controllo, il candidato non supera la soglia. Anche in caso di successo restano non verificati browser, altre note e velocità, differenze di registrazione e preferenze degli ascoltatori.

## 4. Distingui miglioramento e calibrazione

La registrazione è una **sonda di calibrazione**, non un bersaglio fisico esatto per ogni chitarra. Il dataset la etichetta Mi2 a vuoto, ma stanza, strumento, microfono ed esecutore differiscono dal render. Una modifica globale di `decay` può toccare molte note; la formula dipendente dalla frequenza rende particolarmente insicuro estrapolare dal Mi2. Se il candidato avvicina l'inviluppo a quel riferimento, di' soltanto che ha avvicinato **la misura tardiva meno iniziale specificata** per il render provato. Se fallisce, conserva l'artefatto per un'ipotesi successiva su rumore d'attacco, riverbero, retroazione dipendente dalla frequenza o sensibilità alle finestre, senza riscrivere la cronologia.

Il [ciclo di iterazione offline](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) GA e il suo critico spettrale possono sostenere esperimenti ripetuti, ma non danno automaticamente un verdetto d'ascolto. Un eventuale candidato trattato con ComfyUI sarebbe **un braccio offline distinto**, non prova della riuscita del setter Rust. Tieni separati proposte degli agenti, render, riferimenti, hash, misure, revisione e stato di pubblicazione.

## Fonti e limiti

- [Provenienza GAS-001](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md), [misure](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json), [metodo](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) e [renderizzatore nativo](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py), alla revisione Demerzel `5c4967454ddc740ed937c87719ca4d71a3522e4b`.
- [Sorgente del motore Rust GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) e [script d'iterazione offline](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), alla revisione GA `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Prima di questa lezione è stata misurata soltanto la coppia GAS-001 salvata. Coefficienti e intervallo d'accettazione sono calcoli. Una verifica indipendente del contenuto e della coerenza delle bozze tradotte dall'IA non ha rilevato problemi concreti. Restano da completare il render candidato `0.9976`, l'estensione dell'harness nativo, la cattura browser, verifiche su più note, panel d'ascolto, revisione umana, prova con studenti, verifica linguistica e pubblicazione.
