---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Fondamenti di compressione — rapporto, soglia, attacco, rilascio"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ e Compressione: Perché l'Ordine della Catena del Segnale Conta

> **Dipartimento di Ingegneria Audio** | Livello: Intermedio | Durata: 35 minuti

## Obiettivi
- Comprendere le differenze tecniche tra le catene di segnale Comp→EQ ed EQ→Comp
- Identificare quando ciascun ordine produce risultati migliori sulle voci
- Applicare la tecnica a sandwich EQ→Comp→EQ per il massimo controllo
- Riconoscere gli artefatti di compressione dipendenti dalla frequenza e come prevenirli

---

## 1. La Domanda Fondamentale

Importa se si comprime prima o dopo l'EQ? **Sì** — in modo misurabile. L'ordine cambia il modo in cui il compressore reagisce al contenuto in frequenza, influenzando la naturalezza della dinamica e la chiarezza del timbro.

La ragione è semplice: un compressore risponde al *livello*. Se certe frequenze sono più forti (ad es. l'effetto di prossimità che amplifica i 100-200 Hz, o le sibilanti con picchi a 4-10 kHz), il compressore reagisce a *quelle frequenze*, non solo alla performance vocale complessiva.

---

## 2. Compressione Prima dell'EQ (Comp→EQ)

```
Voce → [Compressore] → [EQ] → Bus di Missaggio
```

**Cosa succede:**
- Il compressore vede il segnale grezzo — comprese le frequenze problematiche
- Se le sibilanti sono forti (picchi a 4-10 kHz), possono attivare la compressione su quei transienti
- Il compressore "pompa" sulle frequenze problematiche anziché controllare la dinamica complessiva
- L'EQ successivo modella il segnale già compresso

**Quando usarlo:**
- Quando la voce è ben registrata con problemi di frequenza minimi
- Quando si vuole che il compressore reagisca al segnale completo e naturale
- Quando si usa una compressione leggera (rapporto 2:1, attacco lento) per "incollare"

**Rischio:** Pompaggio dipendente dalla frequenza. Il compressore non sa che non volete che reagisca alla gobba di prossimità a 200 Hz — vede solo il livello.

---

## 3. EQ Prima della Compressione (EQ→Comp)

```
Voce → [EQ] → [Compressore] → Bus di Missaggio
```

**Cosa succede:**
- L'EQ correttivo rimuove prima i problemi: taglio della prossimità a 200 Hz, controllo delle sibilanti a 6 kHz
- Il compressore riceve un segnale più pulito e bilanciato
- La compressione risponde alla *performance musicale*, non agli artefatti di frequenza
- Risultato: compressione più naturale e trasparente

**Quando usarlo:**
- Quando la voce presenta problemi di frequenza evidenti (prossimità, risonanze ambientali, asprezza)
- Quando si vuole che il compressore risponda alla dinamica, non ai picchi di frequenza
- Quando la qualità della registrazione è variabile

**Questa è generalmente l'opzione più sicura** — correggere i problemi di frequenza prima di chiedere al compressore di gestire la dinamica.

---

## 4. Il Sandwich: EQ→Comp→EQ

```
Voce → [EQ Correttivo] → [Compressore] → [EQ Timbrico] → Bus di Missaggio
```

Questo è lo standard professionale per un buon motivo:

1. **Primo EQ (correttivo):** Filtro passa-alto a 80-100 Hz, taglio del fango a 200-300 Hz, notch sulle risonanze ambientali. Questo è chirurgico — si stanno rimuovendo problemi, non modellando il timbro.

2. **Compressore:** Ora reagisce a un segnale pulito. Impostare il rapporto (3:1-4:1 tipico per le voci), la soglia per ottenere circa 6 dB di riduzione del guadagno, attacco medio (10-30ms) per preservare i transienti, rilascio medio (50-100ms).

3. **Secondo EQ (timbrico):** Ora modellare il suono creativamente. Aumentare l'aria a 10-12 kHz, aggiungere presenza a 3-5 kHz, scaldare le basse-medie. Questo EQ è dopo la compressione, quindi i boost non attiveranno il compressore.

**Perché funziona:** Separazione delle responsabilità. L'EQ correttivo previene gli artefatti del compressore. Il compressore gestisce la dinamica su un segnale pulito. L'EQ timbrico modella il carattere finale senza influire sulla dinamica.

---

## 5. Artefatti Dipendenti dalla Frequenza da Tenere d'Occhio

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| Pompaggio sulle plosive | Picchi di bassa frequenza che attivano il compressore | Filtro passa-alto prima del compressore (EQ→Comp) |
| Sibilanti amplificate | Il compressore riduce il corpo, le sibilanti restano | De-esser prima del compressore, o taglio EQ a 6 kHz prima |
| Suono opaco dopo la compressione | Attacco veloce che schiaccia i transienti | Attacco lento (15-30ms), o compressione parallela |
| Timbro inconsistente | Il compressore reagisce diversamente a sezioni piano e forte | Usare 2 stadi di compressione leggera invece di 1 stadio pesante |

---

## 6. EQ Dinamico: L'Alternativa Moderna

L'EQ dinamico combina EQ e compressione in un unico processore. Ogni banda EQ si attiva solo quando la frequenza supera una soglia — come un compressore che opera solo su frequenze specifiche.

**Caso d'uso:** Sibilanti che variano durante la performance. Un taglio statico a 6 kHz renderebbe opaca l'intera voce, ma un taglio di EQ dinamico si attiva solo quando le sibilanti superano la soglia.

Questo non sostituisce la questione Comp→EQ — è uno strumento specializzato per problemi di dinamica dipendenti dalla frequenza.

---

## Esercizio Pratico

### Esercizio 1: Confronto A/B dell'Ordine
Prendete una registrazione vocale. Impostate due catene parallele:
- Catena A: Compressore (4:1, -6 dB GR) → EQ (boost 3 kHz +3 dB, taglio 250 Hz -4 dB)
- Catena B: Stesso EQ → Stesso Compressore

Ascoltate entrambe. Dove sentite la differenza? Concentratevi su:
- Consistenza delle basse frequenze (gestione dell'effetto di prossimità)
- Livello delle sibilanti
- "Naturalezza" complessiva della compressione

### Esercizio 2: Costruire un Sandwich
Impostare: Filtro passa-alto a 100 Hz + taglio a 250 Hz → Compressore (3:1) → Boost di presenza a 4 kHz + Aria a 12 kHz. Confrontare con una catena singola EQ-poi-comprimi.

---

## Punti Chiave
- **L'ordine conta** — il compressore risponde a qualsiasi frequenza sia più forte nell'ingresso
- **EQ→Comp è l'opzione più sicura** — correggere i problemi prima della compressione per risultati più naturali
- **Il sandwich EQ→Comp→EQ è lo standard professionale** — correttivo prima, timbrico dopo
- **Non esiste un ordine universalmente "corretto"** — dipende dalla registrazione, dal genere e dall'intenzione
- **L'EQ dinamico** è uno strumento moderno per problemi di dinamica dipendenti dalla frequenza
- L'obiettivo è sempre: controllare la dinamica senza distruggere il carattere naturale dell'esecuzione

## Approfondimenti
- Dipartimento di Fisica: Acustica — frequenza, ampiezza e rapporti armonici
- Dipartimento di Musica: Come la percezione timbrica influenza le decisioni di missaggio
- Dipartimento di Informatica: Algoritmi DSP alla base di EQ e compressione
- AES (Audio Engineering Society): Standard per la misura del loudness (ITU-R BS.1770)

---
*Prodotto dal Ciclo di Ricerca Seldon audio-engineering-2026-03-23-001 il 2026-03-23.*
*Domanda di ricerca: L'ordine della compressione prima dell'EQ rispetto all'EQ prima della compressione produce risultati misurabimente diversi sulle voci?*
*Credenza: T (confidenza: 0.80)*
