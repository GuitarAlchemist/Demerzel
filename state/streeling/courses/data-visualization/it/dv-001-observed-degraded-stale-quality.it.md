---
module_id: dv-001-observed-degraded-stale-quality
department: data-visualization
course: Misure, esecuzioni degradate e dati non aggiornati
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-04-001
version: "0.1.0"
---

# Misure, esecuzioni degradate e dati non aggiornati

> **Dipartimento di visualizzazione dei dati** | Livello: principiante | Durata stimata: 35 minuti | Stato: revisione in attesa

## Obiettivi

Al termine della lezione saprai:

- distinguere un tasso di successo misurato da un'esecuzione non disponibile e da un valore storico riportato;
- disegnare una cronologia senza trasformare una misura assente in un insuccesso né collegare tacitamente i punti attraverso un'interruzione;
- verificare denominatore, data della misura e ambiente prima di confrontare due risultati;
- affiancare al grafico una descrizione testuale e una tabella accessibili.

## La domanda del progetto

GA conserva le rilevazioni di controllo qualità del chatbot in `state/quality/chatbot-qa/`. Chi consulta il pannello chiede: «Il chatbot è peggiorato?». La visualizzazione deve rispondere solo nella misura consentita dai dati. Questa lezione usa quattro **rilevazioni storiche** fissate al commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). Servono per l'esercizio e non descrivono lo stato attuale del chatbot.

| Data della rilevazione | `total_prompts` | `pass_pct` | `degraded` | Cosa permette di affermare il file |
|---|---:|---:|---|---|
| [2026-06-08](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-08.json) | 52 | `null` | `true` | Il backend non era disponibile; non è stato riportato alcun tasso di successo. |
| [2026-06-15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) | 52 | 75,00 | `false` | Per questa esecuzione è stato riportato un tasso di successo. |
| [2026-06-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-19.json) | 52 | 7,69 | `false` | È stato riportato un tasso basso; il file da solo non ne spiega la causa. |
| [2026-07-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) | 52 | 98,08 | `false` | Un'esecuzione successiva ha riportato un tasso più alto. |

### Esercizio pratico

Classifica ogni riga come tasso osservato o esecuzione non disponibile. Quale riga può essere collocata allo 0% sull'asse dei tassi?

> **Risposta:** Il 15 giugno, il 19 giugno e il 19 luglio hanno tassi riportati. L'esecuzione dell'8 giugno non era disponibile. Nessuna riga riporta lo 0%; collocare l'8 giugno a zero inventerebbe una misura.

## 1. Tre stati diversi dei dati

Un'**osservazione** è un valore effettivamente riportato da un'esecuzione. Un'**esecuzione non disponibile** indica che la misura non poteva essere effettuata o considerata affidabile nelle condizioni registrate. Un **valore storico riportato** è un'osservazione precedente mostrata per dare contesto; non è una nuova misura alla data in cui compare sul pannello.

Il file dell'8 giugno contiene `pass_pct: null`, `degraded: true` e `degraded_reason: "backend_unavailable"`. Contiene anche `last_known_good_pass_pct: 94.0`, una data precedente e `last_known_good_source: "carryforward"`. Quel 94% appartiene all'osservazione precedente. Disegnarlo come punto dell'8 giugno farebbe sembrare stabile la prestazione durante l'interruzione. Disegnare `null` come zero la farebbe sembrare un insuccesso del chatbot. Entrambe le scelte cambiano il significato dei dati.

Mantieni due campi nel modello della visualizzazione: `quality_value` per il tasso misurato e `run_status` per lo stato osservato, degradato o sconosciuto. Conserva la data originale di ogni riferimento storico separatamente dalla data in cui lo mostri. Non ricavare un tasso da `total_prompts`: la nota dell'8 giugno segnala errori del backend, non risposte del chatbot valutate.

### Esercizio pratico

Una scheda mostra «94% di successo l'8 giugno» perché il file contiene `last_known_good_pass_pct: 94.0`. Riscrivila in una frase.

> **Risposta:** «Controllo qualità non disponibile l'8 giugno: backend non disponibile; ultimo valore valido noto, 94% il 16 maggio». La data storica deve essere visibile e il tasso dell'8 giugno deve restare sconosciuto.

## 2. Disegna qualità e disponibilità separatamente

Usa l'asse dei tassi solo per i valori misurati. Lascia una lacuna quando `pass_pct` è `null`, invece di collegare i punti attraverso di essa. Una seconda fascia, allineata alle date, può segnalare l'esecuzione dell'8 giugno come degradata con un'icona **e un'etichetta testuale**. Così chi legge riceve due risposte distinte: quale qualità è stata misurata e se era disponibile una misura.

Per le quattro rilevazioni basta questo schema testuale:

```text
Data          Fascia qualità         Fascia disponibilità
2026-06-08    nessun punto           DEGRADATO: backend non disponibile
2026-06-15    75,00%                 osservato
2026-06-19     7,69%                 osservato; da indagare
2026-07-19    98,08%                 osservato
```

Queste date sono distanziate: non rappresentano quattro letture giornaliere consecutive. Una linea tra il 19 giugno e il 19 luglio suggerirebbe che i giorni non mostrati siano stati misurati e abbiano seguito un andamento regolare. Se la serie completa presenta lacune, interrompi la linea in corrispondenza di esse. Usa le date effettive, non posizioni equidistanti che cancellano il tempo trascorso. Anche il [rapporto storico sulle tendenze di qualità GA al commit fissato](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) segnala fonti non aggiornate; un valore indicato come «più recente» deve mostrare la data dell'osservazione.

### Esercizio pratico

Disegna due fasce per l'8 e il 15 giugno, indicando data e stato testuale. Il 94% storico va collegato con una linea al 75% del 15 giugno?

> **Risposta:** L'8 giugno non ha alcun punto nella fascia qualità e riporta «backend non disponibile» nella fascia disponibilità. Il 15 giugno ha un punto al 75% e lo stato «osservato». Il 94% viene annotato con la sua data originale, il 16 maggio; non è un punto dell'8 giugno né l'inizio di una linea verso il 15 giugno.

## 3. Un numero basso è una domanda, non una diagnosi

Il 19 giugno riporta 7,69% e `degraded: false`. Il grafico deve mostrare il numero, ma questo file da solo non permette di concludere se il codice GA sia regredito, il modello sia cambiato, il corpus sia cambiato o una dipendenza si sia comportata diversamente. `degraded: false` è soltanto la classificazione del produttore per quell'esecuzione; non è un certificato completo di buona salute. Esamina configurazione, identità delle domande, log del backend, regole di valutazione ed esecuzioni vicine prima di attribuire una causa.

Le tre righe osservate indicano 52 domande ciascuna. È un contesto utile, ma quantità uguali non dimostrano che le domande o le regole di valutazione fossero identiche. Un confronto dovrebbe fissare la revisione del corpus e quella del valutatore, oltre al conteggio. Se questi dati mancano, segnala il confronto come provvisorio. Un asse percentuale senza denominatore né fonte può nascondere la fragilità di un campione piccolo.

### Esercizio pratico

Valuta la frase: «GA si è ripreso da una regressione software confermata tra il 19 giugno e il 19 luglio». Cosa è stato osservato e cosa richiede ancora prove?

> **Risposta:** I file riportano 7,69% il 19 giugno e 98,08% il 19 luglio. «Si è ripreso» e «regressione software» attribuiscono una causa e una continuità che queste quattro rilevazioni non dimostrano. Occorre confrontare lo stesso corpus, valutatore e ambiente, quindi esaminare gli insuccessi.

## 4. Rendi il grafico comprensibile senza affidarti al colore

Il colore può aiutare, ma un indicatore di indisponibilità deve avere anche un'etichetta o una forma. La [guida del W3C sull'uso del colore](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) richiede un altro segnale visivo quando il colore trasmette informazioni. La [guida del W3C sui contenuti non testuali](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content) spiega che un grafico necessita di un'alternativa testuale che ne comunichi lo scopo; una tabella può riportare i valori esatti.

Per questi dati, una breve descrizione utile è: «Controllo qualità storico del chatbot GA: 8 giugno non disponibile; i tassi riportati sono 75% il 15 giugno, 7,69% il 19 giugno e 98,08% il 19 luglio. Qui non è stata accertata la causa del risultato basso del 19 giugno». Tieni la tabella sopra accanto al grafico. Chi usa un lettore di schermo deve poter raggiungere date, valori e stati senza interpretare colori o suggerimenti visibili solo al passaggio del mouse.

### Esercizio pratico

Esamina un punto rosso senza testo sull'8 giugno. Quali informazioni vanno aggiunte?

> **Risposta:** Aggiungi testo visibile, per esempio «backend non disponibile», e un'etichetta accessibile alle tecnologie assistive. Lascia assente il tasso dell'8 giugno. Fornisci una tabella o una descrizione equivalente con data e stato.

## Punti chiave

- L'assenza di dati sulla qualità non equivale né a un tasso zero né a un tasso di successo.
- Un riferimento storico conserva la propria data originale di osservazione.
- Il grafico deve mostrare la disponibilità della misura insieme alla qualità misurata.
- Una percentuale bassa osservata può avviare un'indagine senza dimostrarne la causa.
- Date, denominatori, revisioni delle fonti e testo accessibile fanno parte dell'affermazione.

## Letture e prove del progetto

- GA: [rilevazioni storiche di controllo qualità del chatbot](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa) e [rapporto sulle tendenze di qualità](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). Il rapporto è datato, non indica lo stato in tempo reale.
- W3C, [Understanding Success Criterion 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color).
- W3C, [Understanding Success Criterion 1.1.1: Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content).

*Ricerca: `data-visualization-2026-10-04-001`. Le revisioni disciplinare e linguistica sono in attesa; non presentare questa bozza come corso verificato.*
