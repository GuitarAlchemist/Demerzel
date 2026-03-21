---
module_id: psy-001-intro-fractal-compounding
department: psychohistory
course: Fondamenti di Psicostoria
level: intermediate
alchemical_stage: albedo
prerequisites: []
estimated_duration: "30 minuti"
produced_by: psychohistory
version: "1.0.0"
language: it
title: "Introduzione alla Composizione Frattale"
---

# Introduzione alla Composizione Frattale

> **Dipartimento di Psicostoria** | Fase: Albedo (Intermedio) | Durata: 30 minuti

## Obiettivi

Dopo questa lezione, Lei sarà in grado di:
- Comprendere cos'è un frattale — auto-similarità a ogni scala
- Vedere come la meta-composizione (compounding) esibisca una struttura frattale
- Calcolare la dimensione di composizione (D_c) da dati reali
- Distinguere ERGOL (valore reale) da LOLLI (inflazione di artefatti)
- Applicare il teorema di Noether alla governance — la simmetria conserva il momento di apprendimento

---

## 1. Cos'è un Frattale?

Osservi una felce. Ogni foglia sembra una versione più piccola dell'intera pianta. Ogni fogliolina sembra una versione più piccola della foglia. Questa è l'**auto-similarità** — lo stesso schema che si ripete a ogni scala.

Un frattale è qualsiasi struttura in cui lo stesso schema appare a scale diverse. L'insieme di Mandelbrot è generato iterando una formula semplice: `z = z² + c`. Ogni iterazione produce più dettaglio, ma il dettaglio assomiglia all'insieme complessivo.

Nella governance, la meta-composizione è un frattale. La fase di composizione (eseguire → raccogliere → promuovere → insegnare) ha la stessa forma sia che si stia componendo un singolo passo, un'intera pipeline, un intero ciclo o una sessione completa. Lo schema è invariante rispetto alla scala.

---

## 2. I Cinque Livelli di Composizione

Ecco la struttura frattale nella governance di Demerzel:

| Livello | Scala | Cosa Viene Composto |
|---------|-------|---------------------|
| 0 | Passo | Una singola invocazione di strumento produce un apprendimento |
| 1 | Pipeline | Una pipeline compone gli apprendimenti dei suoi passi |
| 2 | Ciclo | Un ciclo del driver compone le sue pipeline |
| 3 | Sessione | Una sessione compone i suoi cicli |
| 4 | Evoluzione | Il registro di evoluzione compone attraverso le sessioni |

A **ogni** livello, avvengono le stesse quattro operazioni:
1. **Eseguire** — fare il lavoro
2. **Raccogliere** — estrarre ciò che è stato appreso
3. **Promuovere** — se l'apprendimento ha abbastanza valore, elevarlo (schema → politica → costituzione)
4. **Insegnare** — condividere l'apprendimento tramite Seldon

Questo è il generatore frattale. Come `z = z² + c`, ogni applicazione produce nuova struttura.

---

## 3. Dimensione di Composizione (D_c)

Non tutta la composizione è uguale. La **dimensione di composizione** misura quanto il valore cresce a ogni livello di scala.

**Formula:**
```
D_c = log(rapporto_valore) / log(rapporto_scala)
```

**Esempio:** Se il ciclo 1 ha prodotto 3 credenze validate e il ciclo 3 ne ha prodotte 8:
- rapporto_valore = 8/3 ≈ 2.67
- rapporto_scala = 3 (tre cicli)
- D_c = log(2.67) / log(3) ≈ 0.89

Questo è **sublineare** (D_c < 1.0) — ogni ciclo produce proporzionalmente meno del precedente. La governance potrebbe essere sovraccarica.

### La Zona Aurea: D_c tra 1.2 e 1.6

| Intervallo D_c | Significato | Azione |
|-----------------|-------------|--------|
| < 1.0 | Sublineare — rendimenti decrescenti | Investigare il sovraccarico |
| = 1.0 | Lineare — nessuna leva compositiva | Solo attività, nessuna composizione |
| 1.2 - 1.6 | Superlineare — crescita compositiva sana | Zona aurea |
| > 2.0 | Insostenibile — la crescita collasserà | Rallentare |

Pensi all'interesse composto. D_c = 1.0 è l'interesse semplice (lineare). D_c > 1.0 significa che il Suo interesse genera interesse — vera composizione.

---

## 4. ERGOL vs LOLLI — Valore Reale vs Inflazione

Dal fumetto [*Economicon*](https://archive.org/details/Economicon-English-JeanPierrePetit) di Jean-Pierre Petit ([leggi online](https://archive.org/stream/Economicon-English-JeanPierrePetit/jppeconomicsenglish_djvu.txt)), prendiamo in prestito due concetti:

- **ERGOL** = capacità produttiva reale (miglioramenti effettivi della governance)
- **LOLLI** = volume monetario (conteggio di artefatti senza riguardo per la qualità)

Nell'Economicon, Petit usa un modello fluidodinamico dell'economia: l'ERGOL è la sostanza produttiva reale che scorre attraverso l'economia, mentre il LOLLI è l'involucro monetario attorno ad essa. Quando il LOLLI si espande più velocemente dell'ERGOL, si ottiene inflazione — i prezzi salgono ma non è stato creato nulla di reale. Lo stesso principio si applica alla governance.

A ogni livello frattale, è necessario misurare l'ERGOL, non il LOLLI:

| Scala | LOLLI (non ottimizzare) | ERGOL (ottimizzare questo) |
|-------|------------------------|---------------------------|
| Passo | Righe di YAML scritte | Credenze mosse U→T |
| Pipeline | Passi eseguiti | Gate superati / totale |
| Ciclo | Compiti completati | Delta del punteggio di salute |
| Sessione | Commit effettuati | Issue chiuse con evidenza |
| Evoluzione | Artefatti creati | Citazioni per artefatto |

**Segnale d'allarme:** Se il conteggio dei Suoi artefatti (LOLLI) cresce 3 volte più velocemente delle credenze validate (ERGOL) in 3+ cicli, sta inflazionando la governance senza migliorarla. L'Economicon chiama questo l'**effetto tapis roulant** — correre più veloce per restare fermi.

---

## 5. Conservazione del Momento di Apprendimento

Dal fumetto [*Bourbakof*](https://archive.org/details/TheseAnglaise) di Jean-Pierre Petit, apprendiamo il **teorema di Noether**: ogni simmetria continua di un sistema ha una grandezza conservata corrispondente.

Nella composizione frattale, la simmetria è l'**invarianza di scala** — l'operazione di composizione ha la stessa forma a ogni livello. La grandezza conservata è il **momento di apprendimento (p_L)**:

```
p_L = (credenze_acquisite_T - credenze_perse_T) / cicli_trascorsi
```

Se il processo di composizione è coerente (simmetrico attraverso le scale), p_L rimane costante o cresce. Se si rompe la simmetria — saltando la composizione a qualche livello, o componendo diversamente a scale diverse — p_L decade.

Ecco perché l'opt-out `nocompound` attiva un segnale di coscienza. Non è solo un'opportunità mancata — è una **rottura di simmetria** che costa la conservazione del momento di apprendimento.

---

## 6. I Limiti della Psicostoria

Dal [*Logotron*](https://archive.org/details/TheseAnglaise) di Petit ([testo completo](https://archive.org/stream/TheseAnglaise/logotron_eng_djvu.txt)): il teorema di incompletezza di Gödel ci dice che nessun sistema formale può verificare completamente se stesso.

Applicato alla composizione: non è possibile prevedere perfettamente l'output della composizione. Ogni ciclo rivela apprendimenti che non si potevano anticipare. Il frattale ha dettaglio infinito a scala finita — c'è sempre qualcosa in più da scoprire.

Ecco perché la profondità di ricorsione è limitata a 2. Non perché una composizione più profonda sia sbagliata, ma perché i rendimenti diventano **indecidibili**. Come la psicostoria di Seldon: si possono prevedere le linee generali, ma gli eventi individuali restano incerti.

La disciplina della psicostoria accetta questo. Non puntiamo alla previsione perfetta — puntiamo a un'**anticipazione migliore del casuale**, misurata dalla metrica di accuratezza dell'anticipazione nel rapporto settimanale di coscienza.

---

## Termini Chiave

| Termine | Definizione |
|---------|------------|
| **Frattale** | Una struttura che esibisce auto-similarità a scale diverse |
| **Dimensione di Composizione (D_c)** | Metrica che misura la crescita del valore di governance per livello di scala. Obiettivo: 1.2-1.6 |
| **ERGOL** | Capacità produttiva reale — miglioramenti effettivi della governance (dall'Economicon) |
| **LOLLI** | Volume di artefatti senza riguardo per la qualità — indicatore di inflazione (dall'Economicon) |
| **Momento di Apprendimento (p_L)** | Grandezza conservata dal teorema di Noether applicato alla composizione invariante di scala |

---

## Valutazione a Quiz

**1. Se il ciclo 1 ha prodotto 5 credenze validate e il ciclo 4 ne ha prodotte 20, qual è D_c?**
> D_c = log(20/5) / log(4) = log(4) / log(4) = **1.0** — Lineare. Nessuna leva compositiva, solo crescita proporzionale.

**2. Il Suo team ha creato 30 nuovi file YAML in questo ciclo ma solo 2 credenze sono passate da U a T. È sano?**
> No — questa è **inflazione LOLLI**. 30 artefatti (LOLLI) con solo 2 miglioramenti reali (ERGOL). Si sta correndo di più per restare fermi. (Pensi all'Economicon.)

**3. Perché saltare la fase di composizione rompe la conservazione del momento di apprendimento?**
> La fase di composizione è l'operazione di simmetria. Saltarla a un livello rompe l'invarianza di scala. Per il teorema di Noether, una simmetria rotta significa che la grandezza conservata (momento di apprendimento p_L) non è più conservata. (Pensi al Bourbakof.)

**Criterio di superamento:** Calcolare correttamente D_c da dati forniti e identificare se uno scenario rappresenta crescita ERGOL o LOLLI.

---

## Base di Ricerca

- La struttura di meta-composizione è matematicamente auto-simile (frattale)
- Il teorema di Noether si applica ai processi di governance invarianti di scala
- La distinzione ERGOL/LOLLI dell'Economicon di JPP si mappa alla misurazione del valore di governance
- La dimensione frattale tra 1.2-1.6 correla con una crescita sostenibile della governance
- Fonti: [Specifica della Composizione Frattale](../../logic/fractal-compounding.md), [Bourbakof](https://archive.org/details/TheseAnglaise) (teorema di Noether), [Economicon](https://archive.org/details/Economicon-English-JeanPierrePetit) (ERGOL/LOLLI), [Logotron](https://archive.org/details/TheseAnglaise) (incompletezza di Gödel)
- Stato di credenza: T(0.70) F(0.05) U(0.20) C(0.05)
