---
module_id: aud-003-transient-preservation-gate
department: audio-engineering
course: "Preservare l'attacco di una corda di chitarra nell'analisi spettrale offline"
level: intermediate
prerequisites: [aud-002-level-matched-guitar-comparison, phy-002-time-frequency-guitar-transients]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-003
version: "0.1.0"
---

# Preservare l'attacco di una corda di chitarra nell'analisi spettrale offline

> **Dipartimento di Ingegneria Audio** | Livello: Intermedio | Durata stimata: 35 minuti | Stato: bozza in italiano; revisione e pubblicazione in sospeso

## Obiettivi

Al termine di questa lezione saprai:

- scegliere una FFT sull'intero intervallo oppure una STFT in base alla decisione da prendere sull'audio;
- impostare dimensioni valide di finestra e passo per lo spettrogramma di IX, mantenendo l'attacco visibile in almeno un frame;
- distinguere il denoiser a wavelet di Haar di IX dalle analisi wavelet mirate a frequenze del fixture GAS-001;
- respingere una riduzione del rumore che modifichi il transiente della chitarra oltre una soglia dichiarata; e
- specificare una valutazione offline falsificabile da un'altra persona con gli stessi WAV.

## La decisione del progetto

Il [fixture GAS-001 del Mi grave a vuoto](../../../fixtures/guitar-acoustics/gas-001/README.md), fissato al commit [`5c496745` di Demerzel](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), contiene una registrazione autorizzata del Mi2 a vuoto e un rendering del motore nativo di GA. Entrambi sono WAV mono di quattro secondi a 44.100 Hz. Il primo attacco registrato arriva circa 1,1 secondi dopo l'inizio del file; il rendering inizia a zero. Il fixture documenta un altro attacco nella registrazione intorno a 2,75 secondi. È una coppia didattica, non un benchmark convalidato di realismo né una cattura dell'AudioWorklet del browser.

[PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md) spiega il compromesso tempo-frequenza e interpreta le misure FFT e wavelet di tipo Morlet salvate nel fixture. [AUD-002](../en/aud-002-level-matched-guitar-comparison.md) controlla l'allineamento degli attacchi e il livello di riproduzione prima dell'ascolto. Questa lezione affronta un'altra scelta tecnica: **chi analizza l'audio offline dovrebbe ridurre il rumore della registrazione di riferimento prima di usarne l'attacco per valutare un rendering di GA?** Una riduzione apparente del rumore non basta. Il denoiser può anche attenuare, allargare o spostare il transiente che si intende preservare.

Il caso implementativo è fissato al commit [`bd1336b7` di IX](https://github.com/GuitarAlchemist/ix/tree/bd1336b7c4045e427dcdbe80b102790e45da5ce1). IX espone un [handler FFT](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1297-L1315), un [handler spettrogramma](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189) e un [handler per la riduzione del rumore con wavelet di Haar](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797). Ricevono array numerici di campioni, non percorsi di file WAV. Per applicarli alla coppia audio fissata servirebbero un decoder WAV e una procedura offline ripetibile; questa lezione non ha eseguito tale prova.

## 1. Scegli la rappresentazione in base alla tesi

La funzione [`rfft` di IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/fft.rs#L84-L115) trasforma un array finito di campioni reali e aggiunge zeri fino alla successiva potenza di due se la lunghezza non è già una potenza di due. Nonostante il nome, restituisce l'intero array FFT. L'handler `ix_fft` restituisce magnitudini e frequenze in **cicli per campione**, assumendo una frequenza di campionamento pari a 1,0. A 44.100 campioni al secondo, moltiplica per 44.100 la frequenza normalizzata di un bin **fino a Nyquist** per esprimerla in hertz; la metà superiore è lo specchio delle frequenze negative. Uno spettro di magnitudine dell'intero file è valido anche per un segnale che cambia, ma non identifica quale attacco ha prodotto un picco. La FFT di un intervallo scelto della prima nota è utile per riassumerne localmente le armoniche, ma fa comunque una media sull'intervallo selezionato.

La funzione [`stft` di IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L30) ripete FFT finestrate in posizioni successive. [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L32-L54) usa una finestra di Hann e conserva le magnitudini di un solo lato dello spettro. Può mostrare se l'energia legata all'attacco appare in un frame iniziale e come cambia. Il percorso `db=true` calcola `20 log10(max(magnitude, 1e-10))`; non è una misura calibrata in dBFS. Non confrontare direttamente i suoi numeri grezzi in dB con i valori RMS in dBFS di GAS-001.

### Esercizio pratico 1: scegli un risultato adatto alla domanda

Una persona calcola `ix_fft` sull'intero WAV registrato di quattro secondi e afferma che un picco brillante appartiene alla *prima* pizzicata, non all'attacco successivo. Quale parte del risultato è utile e che cosa va calcolato prima di attribuire il picco a un evento?

> **Risposta:** La FFT dell'intero file può mostrare energia vicino a quella frequenza, dopo aver convertito i cicli per campione in hertz. Le sue magnitudini non hanno etichette temporali e quindi non attribuiscono il picco alla prima pizzicata. Decodifica il WAV, marca approssimativamente il primo attacco, calcola separatamente un intervallo dichiarato della prima nota e osserva una STFT allineata agli attacchi se conta la loro collocazione nel tempo. Conserva nel resoconto il file originale e gli intervalli analizzati.

## 2. Adatta le impostazioni STFT di IX alla domanda sull'attacco

L'**handler dell'agente** IX richiede un `window_size` che sia una potenza di due, almeno pari a due e non superiore alla lunghezza del segnale. È importante perché la FFT sottostante altrimenti aggiungerebbe zeri al frame e il numero di bin e la mappatura delle frequenze dichiarati dall'handler sarebbero errati. L'handler usa come `hop_size` predefinito metà finestra, porta a uno un passo zero fornito dall'utente e restituisce `n_frames` e `n_bins`. La funzione di base `stft` non fornisce queste verifiche: una procedura offline che la chiama direttamente deve convalidare i propri argomenti. Elabora soltanto frame completi e non prolunga silenziosamente una coda corta.

Per una vista **proposta** del primo attacco a 44,1 kHz, scegli una finestra di 2.048 campioni e un passo di 512. La finestra dura circa **46,44 ms**, il passo circa **11,61 ms**, e la griglia FFT è `44,100 / 2,048 ≈ 21.53 Hz` per bin; la magnitudine di un solo lato contiene **1.025 bin**. Questa griglia è troppo grossolana per risolvere una disputa di un hertz con un singolo frame. Una finestra più grande, di 8.192 campioni, dura circa 185,76 ms e ha spaziatura di 5,38 Hz, ma mescola più attacco e decadimento. Un passo minore produce più frame sovrapposti; non migliora la discriminazione in frequenza di ciascun frame. Sono calcoli dai parametri, **non** risultati misurati di IX sui WAV.

### Esercizio pratico 2: specifica una richiesta valida a IX

A 44.100 Hz, calcola durata della finestra, intervallo tra i passi e spaziatura nominale dei bin per `window_size=2048`, `hop_size=512`. Quanti bin dovrebbe indicare l'handler dello spettrogramma di IX? Perché rifiuterebbe `window_size=2205`, pari a esattamente 50 ms?

> **Risposta:** La durata è `2048/44100 ≈ 46.44 ms`, l'intervallo è `512/44100 ≈ 11.61 ms`, e la spaziatura è `44100/2048 ≈ 21.53 Hz`. L'handler indica `2048/2 + 1 = 1025` bin. Rifiuta 2.205 perché non è una potenza di due; una chiamata diretta alla funzione di base potrebbe aggiungere zeri, ma interpretare i suoi bin come se la FFT fosse lunga 2.205 sarebbe errato.

La finestra di Hann scende a zero agli estremi. Questo attenua le discontinuità ai bordi, ma un transiente esattamente su un estremo può sparire da quel frame. La sovrapposizione porta lo stesso campione in una posizione diversa di un altro frame. È un problema di **posizionamento dell'analisi**, non una creazione di nuove informazioni. La [funzione finestra di IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/window.rs#L10-L15) e il [ciclo sui frame](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L14-L29) rendono verificabile l'effetto di bordo senza una registrazione di chitarra.

### Esercizio pratico 3: conserva l'impulso sul bordo

Prendi un array sintetico di 64 campioni, tutti zero tranne il valore 1 all'indice 16. IX usa una finestra di Hann di 16 campioni. Con passo 16, quale frame completo contiene l'impulso e che cosa gli succede? Che cosa cambia con passo 8?

> **Risposta:** Con passo 16, i frame iniziano a 0, 16, 32 e 48. Solo quello che inizia a 16 contiene l'indice 16; l'impulso è all'offset 0, dove il peso Hann è zero. Tutti gli spettri restituiti possono quindi perdere questo impulso isolato. Con passo 8, anche il frame che inizia a 8 lo contiene, all'offset 8, dove il peso Hann è circa 0,989; quel frame mostra energia. È un calcolo sintetico derivato dal sorgente, non una misurazione IX su un WAV. Mostra perché il passo proposto di 512 campioni va verificato vicino ai bordi degli attacchi reali.

## 3. Un denoiser di Haar può alterare la prova

La funzione [`haar_forward` di IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L18) forma medie e differenze a coppie. [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L60-L82) applica una soglia morbida ai coefficienti di dettaglio e ricostruisce il segnale. È un'elaborazione Haar discreta, **non** l'analisi con wavelet complesse di tipo Morlet centrate sulle frequenze salvata in GAS-001. I due metodi producono risultati diversi e rispondono a domande diverse. Un coefficiente di dettaglio Haar può indicare un cambiamento rapido, ma applicargli una soglia può eliminare parte di una vera pizzicata insieme al rumore.

L'handler di IX richiede `levels >= 1`, una soglia finita non negativa e una lunghezza dell'input divisibile per `2^levels`; altrimenti respinge la richiesta, poiché la trasformata Haar di base può perdere i campioni finali quando una lunghezza è dispari. Il [test sul rumore nel repository](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1387-L1411) usa una rampa regolare con rumore alternato aggiunto e verifica una riduzione dell'errore quadratico medio. Non controlla se viene conservato un attacco isolato di chitarra. I [test delle guardie](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1525-L1543) riguardano una dimensione di spettrogramma non valida e una lunghezza indivisibile per le wavelet.

### Esercizio pratico 4: prevedi il cambiamento del transiente

Per il segnale sintetico di otto campioni `[0, 1, 0, 0, 0, 0, 0, 0]`, applica le equazioni Haar a un livello di IX con soglia morbida pari a 1. Quali sono i primi due campioni ricostruiti? Il risultato sostiene che la riduzione del rumore con wavelet conservi sempre il picco di una pizzicata?

> **Risposta:** La prima coppia ha approssimazione `1/sqrt(2)` e dettaglio `-1/sqrt(2)`. Il modulo del dettaglio è inferiore alla soglia 1, quindi la soglia morbida lo azzera. L'inversa produce `[0.5, 0.5]` per la prima coppia, lasciando le altre a zero. Il picco isolato scende da 1 a 0,5 e si diffonde di un campione verso l'inizio. Il calcolo confuta una tesi incondizionata di preservazione; non prevede quale soglia sia appropriata per un WAV di chitarra registrata.

## 4. Dichiara in anticipo un criterio offline di preservazione

La procedura che segue è una **proposta di valutazione**, non una prova eseguita né uno standard di accettazione GA. Conserva entrambi i WAV del fixture e i loro hash completi. Decodifica ciascuno come campioni mono `f64` normalizzati senza sovrascriverlo. Registra decoder, frequenza di campionamento, numero di campioni ed eventuale ricampionamento; respingi un cambio silenzioso di frequenza di campionamento. Usa i marcatori approssimativi del fixture (registrazione a 1,1 s, rendering a 0,0 s) ed esamina separatamente estratti del primo attacco e dell'attacco successivo nella registrazione. Mantieni una versione originale e una copia elaborata nelle stesse posizioni dei campioni e con lo stesso guadagno. Esegui la vista STFT di IX su entrambe con le impostazioni dichiarate 2.048/512; etichetta i frame tramite **campione iniziale e durata della finestra**, non soltanto dal centro visivo di una colonna. Registra se la conclusione sull'attacco al bordo resiste a un passo alternativo o a un piccolo spostamento del marcatore d'attacco.

Prima di qualsiasi esecuzione Haar, dichiara `levels` e soglia, verifica che la lunghezza esatta dell'input sia divisibile per `2^levels` e salva la politica di riempimento/taglio, se necessaria. Per esempio, un estratto di un secondo con 44.100 campioni **non** è divisibile per otto a tre livelli: il resto è quattro. Aggiungere quattro zeri fino a 44.104 è una possibile scelta dichiarata; introduce un bordo che può influenzare i coefficienti vicini. Altre scelte sono cambiare il confine dell'estratto o ridurre i livelli. Non chiamare direttamente la funzione di base con un input di lunghezza dispari dando per scontato che l'output resti allineato.

Sulla registrazione di riferimento, misura un intervallo di rumore precedente all'attacco e un intervallo fisso del primo attacco tanto nella versione originale quanto in quella elaborata. Un **criterio didattico**, fissato prima di vedere il risultato, potrebbe richiedere un RMS pre-attacco ridotto di almeno **3 dB**, mantenendo il picco assoluto del primo attacco entro **10%** del valore originale e il suo istante entro **1 ms**. Richiedi assenza di clipping e numero di campioni invariato dopo ogni taglio documentato. Ripeti la verifica con i marcatori d'attacco spostati di ±5 ms e riporta ogni soglia candidata, comprese quelle che falliscono. Il rendering GA parte dal tempo zero del file, quindi non ha un intervallo di rumore pre-attacco equivalente; non applicargli questo specifico criterio sul rumore. Conserva la registrazione non elaborata come riferimento principale per il confronto. Superare questi indicatori della forma d'onda permetterebbe un confronto d'ascolto con livelli pareggiati e documentato separatamente, **non** proverebbe che il file elaborato è percettivamente invariato né che GA suona realistico.

### Esercizio pratico 5: applica il criterio e dichiarane il limite

Una persona propone un'elaborazione Haar a tre livelli su un estratto registrato di 44.100 campioni, senza riempimento. Presenta anche un candidato *ipotetico* con RMS pre-attacco più basso di 4 dB, picco d'attacco pari a 0,82 volte quello originale e spostamento del picco di 0,2 ms. Che cosa deve cambiare perché l'handler IX accetti l'estratto? Il candidato supera il criterio didattico?

> **Risposta:** `44,100 mod 8 = 4`, quindi l'handler rifiuta tre livelli per quella lunghezza. Dichiara quattro campioni aggiunti per arrivare a 44.104 e una politica di taglio, scegli un altro estratto oppure riduci i livelli. Il candidato ipotetico fallisce anche se il rumore cala di più di 3 dB e l'istante resta entro 1 ms: `1 - 0.82 = 0.18`, una perdita del 18% del picco, superiore al limite dichiarato del 10%. Questo rifiuto riguarda la preservazione del transiente secondo il criterio approssimativo; non è una misura su uno dei WAV del fixture né un giudizio di ascoltatori.

## Evidenze e limiti

- L'audio del progetto e la sua provenienza vengono dal [fixture GAS-001 a Demerzel `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). La registrazione e il rendering nativo GA sono fonti diverse, con diverse catene di esecuzione e produzione. Le misure FFT e Morlet salvate sono osservazioni di quel fixture, non output di IX.
- Le equazioni STFT, FFT e Haar, le guardie degli handler e i test citati sopra sono osservazioni del codice IX al commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Le dimensioni 2.048/512, l'esempio del bordo Hann, il risultato Haar su otto campioni e l'aritmetica della divisibilità sono **esempi derivati**. AUD-003 non ha prodotto o misurato uno spettrogramma IX né un WAV con rumore ridotto.
- Una magnitudine d'analisi non è una misura calibrata di volume percepito o realismo. I marcatori d'attacco sono approssimativi; finestre spettrali, riempimento, soglie, decoder e guadagno d'ingresso possono cambiare il risultato. Un impulso sintetico mostra una possibile modalità di errore ma non prevede il comportamento di ogni pizzicata.
- Revisione tecnica, prove degli studenti, revisione da parte di madrelingua, sincronizzazione/build di Learn e verifica pubblica restano in sospeso. Questa versione italiana è una bozza di traduzione, non un corso pubblicato.
