---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: Fondamenti di Informatica
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Pensare Algoritmicamente

> **Dipartimento di Informatica** | Stadio: Nigredo (Principiante) | Durata: 25 minuti

## Obiettivi

Al termine di questa lezione, sarai in grado di:
- Definire cos'è un algoritmo e identificare algoritmi nella vita quotidiana
- Applicare quattro tecniche chiave di risoluzione dei problemi: decomposizione, riconoscimento di pattern, astrazione e dividi e conquista
- Distinguere tra approcci greedy ed esaustivi
- Sviluppare un'intuizione per la notazione Big-O e perché l'efficienza conta

---

## 1. Cos'è un Algoritmo?

Un **algoritmo** è una sequenza finita di passi ben definiti che prende un input e produce un output. Tutto qui. Non servono computer.

Segui algoritmi ogni giorno:
- Una ricetta di cucina è un algoritmo (input: ingredienti, output: un piatto)
- Le indicazioni stradali sono un algoritmo (input: posizione attuale, output: destinazione)
- Il processo di dare il resto alla cassa è un algoritmo (input: importo dovuto, output: minimo numero di monete)

Ciò che separa un algoritmo da istruzioni vaghe è la **precisione**. "Cuoci fino a cottura" non è un algoritmo — è ambiguo. "Scaldare a 180°C per 25 minuti, poi controllare la temperatura interna; se inferiore a 74°C, continuare a intervalli di 5 minuti" è un algoritmo. Ogni passo è inequivocabile e il processo termina.

Tre proprietà di un algoritmo valido:
1. **Finitezza** — deve eventualmente fermarsi
2. **Definitezza** — ogni passo deve essere definito con precisione
3. **Efficacia** — ogni passo deve essere qualcosa che può effettivamente essere eseguito

### Esercizio Pratico

Scrivi un algoritmo (in italiano semplice, passi numerati) per cercare una parola in un dizionario cartaceo. Sii abbastanza preciso da consentire a qualcuno che non ha mai usato un dizionario di seguire i tuoi passi. Confronta il tuo con l'approccio descritto nella Sezione 5 (dividi e conquista) — sono uguali?

---

## 2. Decomposizione — Scomporre i Problemi

La competenza più potente del pensiero algoritmico è la **decomposizione**: scomporre un problema complesso in sotto-problemi più piccoli e gestibili.

**Esempio:** Vuoi organizzare un concerto.

Questo è opprimente come compito unico. Ma scomponilo:
1. Trovare una sede
2. Ingaggiare gli artisti
3. Fissare una data
4. Vendere i biglietti
5. Organizzare l'attrezzatura audio
6. Promuovere l'evento

Ogni sotto-problema è ancora complesso, ma ora puoi affrontarli individualmente. E alcuni sotto-problemi si scompongono ulteriormente: "Vendere i biglietti" diventa scegliere una piattaforma, fissare i prezzi, progettare il biglietto, aprire le vendite.

La decomposizione è ricorsiva — si continua a scomporre finché ogni pezzo è abbastanza semplice da risolvere direttamente. È così che viene costruito ogni grande sistema software: non come un unico programma gigante, ma come migliaia di piccoli pezzi componibili.

**Intuizione chiave:** Se non riesci a risolvere un problema, probabilmente non lo hai scomposto abbastanza.

### Esercizio Pratico

Scomponi il seguente problema in sotto-problemi: "Costruire un sito web che permetta agli utenti di cercare accordi per chitarra." Continua a scomporre finché ogni sotto-problema è qualcosa che una persona potrebbe completare in un giorno o meno. Quanti livelli di decomposizione ti sono serviti?

---

## 3. Riconoscimento di Pattern

Il **riconoscimento di pattern** è la capacità di notare somiglianze tra problemi già risolti e nuovi problemi che si affrontano.

**Esempio:** Ordinare una mano di carte da gioco e ordinare un elenco di nomi di studenti sono lo stesso problema — disporre elementi in ordine secondo una regola di confronto. Una volta imparato un algoritmo di ordinamento, lo puoi applicare a qualsiasi cosa possa essere confrontata.

I pattern compaiono ovunque nell'informatica:
- Cercare in una collezione (trovare un libro in biblioteca, trovare un file su disco, trovare una nota sulla tastiera della chitarra)
- Filtrare elementi che corrispondono a criteri (filtro antispam, ricerca di foto, ricerca di accordi)
- Trasformare dati da un formato a un altro (traduzione, conversione di file, trasposizione)

I programmatori esperti risolvono i problemi più velocemente non perché sono più intelligenti, ma perché riconoscono i pattern. Vedono un nuovo problema e pensano: "Questo è essenzialmente un problema di ricerca" o "Questo è un attraversamento di grafi" — e si rivolgono a una soluzione nota.

### Esercizio Pratico

Considera questi tre problemi. Quale pattern condividono?
1. Trovare il percorso più breve tra due città
2. Trovare il minor numero di cambi di accordo per passare da un accordo all'altro
3. Trovare il numero minimo di mosse per risolvere un puzzle

> Sono tutti problemi di **cammino minimo** — trovare la sequenza di passi a costo minimo tra uno stato iniziale e uno stato obiettivo.

---

## 4. Astrazione — Ignorare Ciò Che Non Conta

L'**astrazione** è l'arte di eliminare i dettagli irrilevanti per concentrarsi su ciò che conta per il problema in questione.

Quando disegni una mappa, non includi ogni albero, ogni crepa nel marciapiede, ogni filo d'erba. Includi strade, punti di riferimento e distanze — i dettagli rilevanti per la navigazione. Tutto il resto è astratto.

Nel pensiero algoritmico, l'astrazione significa:
- Rappresentare un problema del mondo reale con un modello semplificato
- Ignorare dettagli che non influenzano la soluzione
- Definire input e output chiari

**Esempio:** Se vuoi trovare il percorso più breve tra due città, non hai bisogno di modellare il colore dei cartelli stradali o il limite di velocità su ogni strada (a meno che la velocità conti per il tuo problema). Astrai la mappa in un **grafo**: le città sono nodi, le strade sono archi, le distanze sono pesi. Ora puoi applicare un algoritmo su grafi senza pensare all'asfalto.

L'astrazione è ciò che permette agli algoritmi di essere **generici**. Un algoritmo di ordinamento non si preoccupa se sta ordinando numeri, nomi o accordi per chitarra. Ha solo bisogno di sapere come confrontare due elementi. Tutto il resto è astratto.

### Esercizio Pratico

Stai costruendo un sistema per raccomandare routine di pratica per studenti di chitarra. Quali dettagli su ogni studente sono rilevanti per l'algoritmo? Quali dettagli possono essere astratti? Scrivi due liste: "includere" e "ignorare."

---

## 5. Dividi e Conquista

**Dividi e conquista** è una strategia algoritmica specifica:

1. **Dividi** il problema in sotto-problemi più piccoli dello stesso tipo
2. **Conquista** ogni sotto-problema (ricorsivamente, se necessario)
3. **Combina** i risultati

Questo è diverso dalla decomposizione generale. In dividi e conquista, i sotto-problemi hanno la **stessa struttura** dell'originale — solo più piccoli.

**Esempio — Ricerca Binaria (trovare una parola nel dizionario):**
1. Apri il dizionario a metà
2. La parola è su questa pagina? Se sì, fatto.
3. Se la parola viene prima di questa pagina in ordine alfabetico, ripeti con la prima metà
4. Se la parola viene dopo, ripeti con la seconda metà
5. Continua a dimezzare finché trovi la parola

Ogni passo dimezza lo spazio di ricerca rimanente. Un dizionario con 100.000 parole richiede al massimo 17 passi (poiché 2^17 = 131.072 > 100.000). Confrontalo con partire dalla pagina 1 e leggere ogni voce — fino a 100.000 passi.

**Algoritmi classici dividi e conquista:**
- **Ricerca binaria** — trovare un elemento in una collezione ordinata
- **Merge sort** — ordinare dividendo, ordinando le metà, poi unendo
- **Quicksort** — ordinare scegliendo un pivot e partizionando

### Esercizio Pratico

Hai una lista ordinata di 1.000 canzoni. Usando la ricerca binaria, qual è il numero massimo di confronti necessari per trovare una canzone specifica? (Suggerimento: quante volte puoi dimezzare 1.000 prima di arrivare a 1?)

> log2(1000) ≈ 10. Al massimo 10 confronti — rispetto a 1.000 per una ricerca lineare.

---

## 6. Approcci Greedy vs Esaustivi

Due grandi famiglie di algoritmi rappresentano filosofie diverse:

**Gli algoritmi greedy** fanno la scelta localmente ottimale ad ogni passo, sperando che porti a una soluzione globalmente ottimale.

*Esempio — Dare il resto con il minor numero di monete:*
- Importo: 67 centesimi
- Approccio greedy: prendi la moneta più grande che entra. 50 → 10 → 5 → 2. Risultato: 50+10+5+2 = 4 monete.
- Questo funziona per le monete dell'euro. Ma per una valuta con monete da 1, 3 e 4 centesimi, il greedy fallisce: per 6 centesimi, il greedy dà 4+1+1 (3 monete) ma l'ottimo è 3+3 (2 monete).

**Gli algoritmi esaustivi** controllano ogni possibile soluzione e scelgono la migliore. Trovano sempre la risposta ottimale, ma possono essere lenti.

*Esempio — Il commesso viaggiatore:*
- Visitare 10 città e tornare a casa per il percorso più breve
- Esaustivo: provare tutti i possibili ordinamenti (10! = 3.628.800 percorsi), misurare ciascuno, scegliere il più breve
- Questo garantisce il percorso ottimale, ma è computazionalmente costoso

| Approccio | Vantaggio | Svantaggio | Quando Usarlo |
|-----------|-----------|------------|---------------|
| Greedy | Veloce, semplice | Può non trovare la soluzione ottimale | Quando una soluzione buona è sufficiente |
| Esaustivo | Ottimale garantito | Lento per problemi grandi | Quando la correttezza è critica e l'input è piccolo |

Molti algoritmi reali combinano entrambi: usare euristiche greedy per potare lo spazio di ricerca, poi controllare esaustivamente i candidati rimanenti.

### Esercizio Pratico

Stai preparando una valigia con oggetti di pesi e valori diversi, e la valigia ha un limite di peso. Descrivi un approccio greedy e uno esaustivo. Quale useresti con 5 oggetti? 500 oggetti?

> *Greedy:* Ordinare gli oggetti per rapporto valore/peso, aggiungere oggetti dal rapporto più alto finché la valigia è piena. *Esaustivo:* Provare ogni combinazione possibile, calcolare il valore totale per quelle entro il limite di peso, scegliere la migliore. Per 5 oggetti (32 combinazioni), l'esaustivo va bene. Per 500 oggetti (2^500 combinazioni), l'esaustivo è impossibile — usare greedy o un algoritmo più intelligente.

---

## 7. Intuizione Big-O — Quanto Veloce è Abbastanza Veloce?

Non tutti gli algoritmi sono uguali. La **notazione Big-O** descrive come il tempo di esecuzione di un algoritmo cresce al crescere della dimensione dell'input.

Non è necessario calcolare il Big-O con precisione adesso. Serve l'**intuizione** per cosa significano le categorie:

| Big-O | Nome | Esempio | 1.000 elementi | 1.000.000 elementi |
|-------|------|---------|----------------|-------------------|
| O(1) | Costante | Accedere a un elemento di array per indice | 1 passo | 1 passo |
| O(log n) | Logaritmico | Ricerca binaria | ~10 passi | ~20 passi |
| O(n) | Lineare | Scansionare ogni elemento una volta | 1.000 passi | 1.000.000 passi |
| O(n log n) | Linearitmico | Merge sort, quicksort | ~10.000 passi | ~20.000.000 passi |
| O(n^2) | Quadratico | Confrontare ogni coppia | 1.000.000 passi | 1.000.000.000.000 passi |
| O(2^n) | Esponenziale | Ricerca esaustiva di sottoinsiemi | ~10^301 passi | Lascia perdere |

L'intuizione chiave: **la differenza tra le categorie di algoritmi cresce enormemente con la dimensione dell'input.** Un algoritmo O(n) e un algoritmo O(n^2) potrebbero entrambi sembrare istantanei su 10 elementi. Su un milione di elementi, uno finisce in un secondo e l'altro impiega giorni.

Ecco perché il pensiero algoritmico conta. Scegliere l'algoritmo giusto può fare la differenza tra un programma che funziona e uno che non termina mai.

### Esercizio Pratico

Hai due algoritmi per cercare in una libreria musicale:
- Algoritmo A: controlla ogni canzone una per una (O(n))
- Algoritmo B: usa un indice ordinato e la ricerca binaria (O(log n))

Per una libreria di 10 milioni di canzoni, approssimativamente quanti passi richiede ciascuno?
> A: 10.000.000 passi. B: log2(10.000.000) ≈ 23 passi. L'algoritmo B è oltre 400.000 volte più veloce.

---

## Termini Chiave

| Termine | Definizione |
|---------|-----------|
| **Algoritmo** | Una sequenza finita di passi ben definiti che trasforma un input in un output |
| **Decomposizione** | Scomporre un problema complesso in sotto-problemi più piccoli e gestibili |
| **Riconoscimento di pattern** | Identificare somiglianze tra un nuovo problema e problemi risolti in precedenza |
| **Astrazione** | Eliminare i dettagli irrilevanti per concentrarsi su ciò che conta per la soluzione |
| **Dividi e conquista** | Dividere un problema in istanze più piccole dello stesso problema, risolvendo ricorsivamente |
| **Algoritmo greedy** | Fare la scelta localmente ottimale ad ogni passo |
| **Algoritmo esaustivo** | Controllare ogni possibile soluzione per garantire di trovare la migliore |
| **Notazione Big-O** | Una classificazione dell'efficienza degli algoritmi basata su come il tempo di esecuzione cresce con la dimensione dell'input |

---

## Autovalutazione

**1. Quali tre proprietà deve avere un algoritmo valido?**
> Finitezza (termina), definitezza (ogni passo è inequivocabile) ed efficacia (ogni passo può essere effettivamente eseguito).

**2. Devi cercare un nome in una lista non ordinata di 1.000 nomi. Qual è il miglior Big-O che puoi raggiungere?**
> O(n) — ricerca lineare. Senza ordinamento o indicizzazione, devi potenzialmente controllare ogni elemento. Se la lista fosse ordinata, potresti usare la ricerca binaria per O(log n).

**3. Un algoritmo greedy per dare il resto dà la risposta sbagliata per monete da 1, 3 e 4 centesimi quando si devono dare 6 centesimi. Perché?**
> L'approccio greedy sceglie prima la moneta più grande (4), poi servono 1+1 per il resto (3 monete totali). Ma 3+3 usa solo 2 monete. Il greedy fallisce perché la scelta localmente ottimale (moneta più grande) non porta alla soluzione globalmente ottimale.

**4. Perché O(n log n) è considerato efficiente per l'ordinamento?**
> È stato dimostrato matematicamente che nessun algoritmo di ordinamento basato su confronti può fare meglio di O(n log n) nel caso peggiore. Merge sort e quicksort raggiungono questo limite, rendendoli ottimali tra gli ordinamenti per confronto.

**Criteri di superamento:** Scomporre un dato problema in sotto-problemi, identificare quale approccio algoritmico (greedy, esaustivo, dividi e conquista) si adatta a uno scenario dato, e spiegare le differenze Big-O con esempi concreti.

---

## Base di Ricerca

- Il pensiero algoritmico (decomposizione, riconoscimento di pattern, astrazione) è riconosciuto come competenza fondamentale del pensiero computazionale
- Dividi e conquista, greedy e ricerca esaustiva sono i tre paradigmi algoritmici fondamentali
- La notazione Big-O fornisce una misura dell'efficienza degli algoritmi indipendente dall'hardware
- Insegnare l'intuizione algoritmica prima dell'analisi formale migliora il trasferimento nella risoluzione dei problemi
- Fonti: consenso nella formazione in informatica, curriculum del Dipartimento di Informatica di Streeling
- Stato di credenza: V(0.91) F(0.02) I(0.05) C(0.02)
