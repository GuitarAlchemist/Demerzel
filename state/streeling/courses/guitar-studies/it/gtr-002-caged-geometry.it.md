---
module_id: gtr-002-caged-geometry
department: guitar-studies
course: "Layout della tastiera e sistema CAGED"
level: intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "45 minutes"
produced_by: seldon-research-cycle
research_cycle: guitar-studies-2026-03-23-001
version: "1.0.0"
---

# Geometria CAGED: Perché Cinque Forme Governano la Tastiera

> **Dipartimento di Studi Chitarristici** | Livello: Intermedio | Durata: 45 minuti

## Obiettivi
- Comprendere perché esattamente 5 forme di accordi aperti tassellano l'intera tastiera
- Derivare il sistema CAGED dall'osservazione della struttura intervallare degli accordi aperti
- Dimostrare che il CAGED è una conseguenza matematica dell'accordatura standard, non un sistema arbitrario
- Applicare le forme di barré mobili per navigare qualsiasi accordo maggiore lungo il manico

---

## 1. Le Cinque Forme Aperte

Ogni chitarrista impara questi cinque accordi maggiori aperti fin dall'inizio. Ciascuno ha un'impronta geometrica distinta:

### Forma C (Do)
```
x 3 2 0 1 0    Corde: 5-4-3-2-1
  F 3 5 F 3    Intervalli: Fondamentale-3M-5G-Fondamentale-3M
```

### Forma A (La)
```
x 0 2 2 2 0    Corde: 5-4-3-2-1
  F 5 F 3 5    Intervalli: Fondamentale-5G-Fondamentale-3M-5G
```

### Forma G (Sol)
```
3 2 0 0 0 3    Corde: 6-5-4-3-2-1
F 3 5 F 3 F    Intervalli: Fondamentale-3M-5G-Fondamentale-3M-Fondamentale
```

### Forma E (Mi)
```
0 2 2 1 0 0    Corde: 6-5-4-3-2-1
F 5 F 3 5 F    Intervalli: Fondamentale-5G-Fondamentale-3M-5G-Fondamentale
```

### Forma D (Re)
```
x x 0 2 3 2    Corde: 4-3-2-1
  F 5 F 3      Intervalli: Fondamentale-5G-Fondamentale-3M
```

**Osservazione chiave:** Ogni forma contiene solo tre classi di altezza: Fondamentale, Terza Maggiore e Quinta Giusta. Le differenze sono nel *voicing* — in quale ottava appare ogni nota e quali corde le portano.

---

## 2. Il Test dello Scorrimento

Ecco l'intuizione centrale: se si mantiene la *geometria delle dita* di qualsiasi accordo aperto ma la si scorre lungo il manico, le relazioni intervallari si preservano. Il dito del barré sostituisce il capotasto.

**Forma E al tasto 0:** Mi maggiore (aperto)
**Forma E al tasto 1:** Fa maggiore (barré di Fa)
**Forma E al tasto 3:** Sol maggiore
**Forma E al tasto 5:** La maggiore

Questo funziona perché l'intervallo tra ogni coppia di corde adiacenti è fissato dall'accordatura. Spostare tutte le dita dello stesso numero di tasti traspone ogni nota dello stesso intervallo.

Non è un trucco didattico — è un *teorema geometrico* sulla tastiera.

---

## 3. Perché Esattamente Cinque Forme?

L'accordatura standard (Mi-La-Re-Sol-Si-Mi) crea un pattern intervallare specifico tra le corde:

```
Corda:     6    5    4    3    2    1
Nota:      Mi   La   Re   Sol  Si   Mi
Intervallo:  4G   4G   4G   3M   4G
```

Il pattern 4a-4a-4a-3a-4a crea esattamente **cinque regioni distinte** dove le forme degli accordi aperti possono essere formate. Ogni forma occupa un diverso intervallo di tasti e corde.

Le cinque forme si incastrano come pezzi di un puzzle:

```
Tasto: 0    3    5    7    8    10   12
       |--E--|--D--|--C--|--A--|--G--|--E--|
       (forme mostrate per la tonalità di Mi maggiore)
```

Muovendosi nell'ordine C-A-G-E-D si risale il manico, con la fondamentale di ogni forma che si collega alla nota più alta della forma successiva. Questa è la **sequenza CAGED** — un percorso ciclico attraverso tutte e cinque le regioni di voicing.

---

## 4. Il CAGED è l'Unico Ordinamento?

Le cinque forme formano un **ciclo**, quindi qualsiasi punto di partenza dà una sequenza valida:

- **CAGED** (il più comune)
- **AGEDC** (partendo da La)
- **GEDCA** (partendo da Sol)
- **EDCAG** (partendo da Mi)
- **DCAGE** (partendo da Re)

Il nome "CAGED" è una convenzione mnemonica. Il ciclo sottostante a 5 forme è determinato strutturalmente. Tutti gli ordinamenti descrivono la stessa tassellatura della tastiera.

---

## 5. Dipendenza dall'Accordatura

Il CAGED è specifico dell'accordatura standard. Cambia l'accordatura e cambiano le forme:

- **Accordatura per quarte** (Mi-La-Re-Sol-Do-Fa): L'irregolarità della terza maggiore tra le corde 3-2 scompare. Le forme degli accordi diventano più uniformi ma diverse dal CAGED.
- **Accordatura aperta di Sol** (Re-Sol-Re-Sol-Si-Re): Le corde a vuoto formano già un accordo, creando un sistema di forme completamente diverso.
- **Drop D** (Re-La-Re-Sol-Si-Mi): Solo la corda più grave cambia, preservando la maggior parte delle forme CAGED ma alterando le forme E e G sulle corde basse.

Questo dimostra che il CAGED è *derivato dalla* geometria dell'accordatura standard, non imposto su di essa.

---

## Esercizio Pratico

### Esercizio 1: Identificazione delle Forme
Suona un accordo di Do maggiore usando tutte e cinque le forme CAGED. Parti dalla forma C aperta, poi trova la forma A (tasto 3), la forma G (tasto 5), la forma E (tasto 8) e la forma D (tasto 10).

### Esercizio 2: Connessione tra Forme
Scegli due forme CAGED adiacenti. Trova le note che condividono sulle stesse corde. Queste note condivise sono i tuoi "punti di snodo" per muoverti tra le forme.

### Esercizio 3: Una Corda, Cinque Forme
Sulla corda 2 soltanto, suona la nota Do in ciascuna delle cinque posizioni CAGED. Nota come ogni forma posiziona il Do su un tasto diverso di quella corda.

---

## Punti Chiave
- Il sistema CAGED è **scoperto, non inventato** — è una conseguenza strutturale della geometria dell'accordatura standard
- Esattamente **5 forme** tassellano la tastiera a causa del pattern di accordatura 4a-4a-4a-3a-4a
- Ogni forma preserva la sua struttura intervallare quando barrata e spostata — questo è un teorema geometrico, non una scorciatoia didattica
- Il nome "CAGED" è uno dei 5 ordinamenti ciclici equivalenti
- Accordature diverse producono sistemi di forme diversi, confermando che il CAGED è derivato dall'accordatura

## Approfondimenti
- [GTR-001: La Mappa della Tastiera](gtr-001-the-fretboard-map.it.md) — prerequisito
- Dipartimento di Musica: Sistemi di accordatura e temperamento
- Dipartimento di Fisica: Acustica della vibrazione delle corde e armoniche
- Dipartimento di Matematica: Teoria dei gruppi e simmetria della tastiera

---
*Prodotto dal Ciclo di Ricerca Seldon guitar-studies-2026-03-23-001 il 2026-03-23.*
*Domanda di ricerca: I voicing comuni degli accordi aperti condividono pattern strutturali che predicono le loro forme barré mobili?*
*Credenza: V (confidenza: 0.85)*
