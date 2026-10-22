---
module_id: phy-005-sheet-thickness-and-scene-units
department: physics
course: Spessore del foglio dalle coordinate IX alle unità di scena proposte
level: intermediate
prerequisites: [basic-ratios, dimensional-analysis]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-21-005
version: "0.1.0"
---

# Spessore del foglio dalle coordinate IX alle unità di scena proposte

> **Dipartimento di fisica** | 40 minuti | Bozza italiana provvisoria; revisione disciplinare, revisione di una persona con piena padronanza dell'italiano e verifica con un discente ancora da svolgere.

## Obiettivi e problema del progetto

Un foglio IX può avere coordinate comprese tra zero e uno, mentre lo spessore del materiale si misura in millimetri. Un artefatto proposto per Blender o Godot richiede un'altra scala di lunghezza dichiarata. Riportare il solo numero `0.4` in tutte e tre le rappresentazioni trasformerebbe un normale cartoncino in un foglio 150 volte troppo spesso, oppure convertirebbe i millimetri in metri di scena con un errore di un fattore 1000.

Al termine della lezione saprai ricavare spessori e altezze delle pile in ogni rappresentazione, distinguere il numero di strati sovrapposti dai livelli di pannelli paralleli, individuare due errori di scala e preparare un passaggio di consegne circoscritto alle evidenze. Dedica circa 12 minuti alla lettura delle derivazioni, 18 minuti agli esercizi prima di consultarne le risposte e 10 minuti alla preparazione del compito di trasferimento. Questa lezione riguarda lunghezze geometriche e conversioni di unità. La velocità di eccitazione della chitarra è trattata in PHY-004; la ricostruzione di uno stato di piegatura appartiene alla sequenza di calcolo visuale.

Il perimetro delle nostre fonti è il commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [`thickness.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), i suoi [test esistenti](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) e [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs). Abbiamo esaminato quelle definizioni e asserzioni. L'agente coordinatore ha eseguito il target specifico dei test sullo spessore mantenendo invariato HEAD di IX alla revisione fissata: 11 superati, 0 falliti; questo risultato non riguarda l'intera suite. La [fixture aritmetica](../../../fixtures/physics/phy-005/scenarios.json) fornisce esempi modellati, con istruzioni per riprodurli nel relativo [README](../../../fixtures/physics/phy-005/README.md).

## 1. Dichiara una scala di misura prima di convertire una coordinata

Siano `C` la larghezza del foglio espressa nelle unità di coordinate del diagramma delle pieghe, `W` la sua larghezza fisica ipotizzata in mm e `h` lo spessore completo del materiale in mm. Definisci `a=W/C`, in mm per unità di coordinata. Allora:

```text
x_mm = x_cp × a
t_cp = h/a = h × C/W
H_mm = H_cp × a
```

Il pedice identifica una rappresentazione; non afferma che IX memorizzi metadati fisici. La larghezza `W` è un'ipotesi esterna fornita per questo esempio svolto. Un file che descrive un quadrato unitario, da solo, non dice se il foglio reale sia largo 150 mm o 300 mm. Lo spessore è quello completo, non un semispessore né un conteggio di facce.

Il test della gru descrive esplicitamente un cartoncino di 0.4 mm su un foglio di 150 mm il cui diagramma delle pieghe è il quadrato unitario. Quindi `C=1`, `W=150`, `a=150` e `t_cp=0.4/150=0.0026666667`. La verifica della conversione inversa dà `0.0026666667 × 150 ≈ 0.4 mm`. Mantieni la frazione fino alla visualizzazione finale per evitare errori cumulativi di arrotondamento.

`lib.rs` descrive il ridimensionamento delle coordinate mediante potenze di due prima dei controlli con tolleranza assoluta: l'estensione del diagramma delle pieghe diventa compresa tra uno e due. Si tratta di condizionamento numerico. Non è né una dichiarazione di metri né una misura del foglio. `stack(ctx,t)` usa il valore `t` fornito dal chiamante senza modificarlo nelle moltiplicazioni riportate; non può dedurre `W` né convertire implicitamente un valore fornito come `0.4 mm`. Conserva una corrispondenza esterna esplicita per la rappresentazione delle coordinate che intendi usare nelle fasi successive.

### Esercizio pratico 1: correggere lo spessore in ingresso

Un passaggio di consegne per la gru del test, rappresentata nel quadrato unitario, etichetta `t=0.4` come «0.4 mm». Calcola il valore `t_cp` necessario, lo spessore fisico rappresentato dal valore errato e il fattore di errore.

> **Risposta:** `t_cp=0.4/150=0.0026666667`. Con `a=150 mm/cp`, il valore errato `0.4 cp` significa `60 mm`. Il rapporto rispetto allo spessore desiderato è `60/0.4=150`. Sostituisci il numero e dichiara la corrispondenza; cambiare l'etichetta del numero esistente non esegue una conversione.

## 2. Tieni distinte le due letture della pila

L'implementazione calcola `ply` come il numero massimo di facce in una cella di sovrapposizione. La sua altezza è `ply_height=ply × t`. Questa lettura consente a una faccia di occupare altezze diverse in celle diverse, come potrebbe fare un foglio flessibile che si adatta alle superfici. È un limite inferiore per pile che mantengono le posizioni planari dichiarate.

Per pannelli rigidi paralleli, le facce collegate da giunti piatti appartengono allo stesso pannello. Un arco diretto collega un pannello inferiore a uno superiore per una coppia sovrapposta con ordine dichiarato. Con un ordine aciclico e tutte le coppie di pannelli sovrapposti determinate, `levels` è la lunghezza della catena più lunga e `height=levels × t` è l'altezza minima secondo questa interpretazione ristretta. Se mancano ordini, il conteggio dei livelli riportato è un limite inferiore; `levels_exact=false` e `face_levels` è assente. Un conteggio è adimensionale, mentre un'altezza ha le stesse unità di `t`.

Il test esistente della gru verifica `ply=28`, un numero esatto di livelli rigidi `levels=36`, nessuna coppia indeterminata e 59 valori di livello delle facce che rispettano l'ordine dichiarato. Fornisce una catena di 36 facce. Queste sono asserzioni relative a quella fixture e a quell'interpretazione, non una specifica universale della gru. Applica entrambe le formule:

```text
altezza per strati:  28 × (0.4/150) = 0.0746666667 cp = 11.2 mm
altezza rigida:      36 × (0.4/150) = 0.096 cp        = 14.4 mm
```

In una disposizione illustrativa che usa le superfici inferiori `z_k=k×t`, la superficie inferiore più alta si trova a `35t` per 36 livelli occupati. La sommità di quell'ultima lastra è a `36t`. Questo spiega la differenza tra la quota di una superficie e l'estensione completa della pila; è una convenzione di disegno proposta, non geometria esportata da IX.

### Esercizio pratico 2: distinguere quota ed estensione

Le indicazioni per la scena dicono: «Lo spessore della gru è di 28 strati, quindi la pila rigida è alta 11.2 mm; il livello rigido più alto è 35, quindi la sua altezza è 35t». Correggi entrambe le affermazioni usando le ipotesi del test.

> **Risposta:** La lettura a 28 strati dà 11.2 mm. La lettura a pannelli rigidi paralleli ha 36 livelli esatti e un'estensione completa di `36×0.4=14.4 mm`. Secondo la convenzione proposta per la superficie inferiore, il livello 35 inizia a `35×0.4=14.0 mm` e termina a 14.4 mm. Un indice intero di livello non è il conteggio dei livelli occupati.

## 3. Ricava esplicitamente una futura scala di scena

Supponiamo che un futuro artefatto scelga `u=1 scene unit per metre`. È una scelta didattica, non una configurazione verificata di Blender o Godot. La conversione è `b=u/1000` unità di scena per mm, quindi `x_scene=x_cp×a×b`. Applica lo stesso moltiplicatore a tutte le lunghezze appartenenti alla stessa geometria, compresi lo spessore e le altezze calcolate.

Per il foglio di riferimento, un'unità di coordinata corrisponde a `150/1000=0.15` unità di scena. Quindi `t_scene=(0.4/150)×0.15=0.0004`, l'altezza per strati è `0.0112` e l'altezza rigida è `0.0144`. Il percorso fisico indipendente dà `14.4 mm × (1/1000)=0.0144 scene units`. La concordanza tra i due percorsi verifica l'aritmetica, non una pipeline di importazione.

Se un'anteprima didattica separata sceglie invece `u=100 scene units per metre`, ogni lunghezza di scena diventa 100 volte maggiore. La larghezza del foglio diventa 15 unità di scena e l'altezza rigida diventa 1.44. Lo spessore fisico resta 0.4 mm. La scelta della scala cambia la rappresentazione, non il materiale.

### Esercizio pratico 3: trovare un errore di un fattore 1000

Una scena proposta con scala in metri usa una larghezza del foglio di `0.15`, uno spessore di `0.4` e un'altezza rigida di `14.4`. Calcola i valori corretti delle due lunghezze minori e mostra un rapporto che rilevi l'incoerenza senza dipendere dalla scala della scena.

> **Risposta:** Lo spessore dovrebbe essere `0.0004` e l'altezza rigida `0.0144` unità di scena. Entrambi i valori forniti sono 1000 volte troppo grandi. I rapporti corretti sono `thickness/width=0.4/150≈0.0026666667` e `rigid height/width=14.4/150=0.096`. La scena errata ha rapporti di circa 2.6667 e 96. Una scala uniforme coerente conserva questi rapporti adimensionali.

## 4. Cambia un'ipotesi alla volta

Cambiare materiale e ridimensionare la geometria rispondono a domande diverse. Sullo stesso foglio di 150 mm, raddoppiare lo spessore a 0.8 mm raddoppia `t_cp`, entrambe le altezze e le rispettive lunghezze di scena. Non cambia l'ordine delle facce in ingresso. Il test esistente `heights_scale_with_the_thickness` confronta `t=0.25` e `0.5`, verifica il raddoppio delle altezze e verifica che i livelli delle facce restino invariati. Quei numeri verificano l'algebra; non sono misure del cartoncino.

Mantenere materiale di 0.4 mm ma usare un foglio di 300 mm dimezza `t_cp` per una rappresentazione nel quadrato unitario. Le altezze fisiche restano 11.2 e 14.4 mm per la stessa configurazione combinatoria dichiarata. Al contrario, raddoppiare tutte le lunghezze fisiche, compreso lo spessore del materiale, conserva `t_cp` e raddoppia le altezze fisiche. Dichiara quale di queste trasformazioni intendi quando dici «ingrandire».

Ricodificare lo stesso foglio di 150 mm con `C=2` dà `a=75 mm/cp` e `t_cp=0.0053333333`; l'altezza rigida diventa `0.192 cp`. Moltiplicare per 75 restituisce 14.4 mm. Questa è una derivazione dimensionale per una rappresentazione ricodificata in modo coerente, non una nuova esecuzione osservata di IX.

### Esercizio pratico 4: confrontare tre modifiche

Partendo dal riferimento, calcola `t_cp` e l'altezza rigida in mm per: A, spessore 0.8 mm con larghezza 150 mm e `C=1`; B, spessore 0.4 mm con larghezza 300 mm e `C=1`; C, il foglio fisico originale rappresentato con `C=2`. Assumi lo stesso ordine esatto di 36 livelli.

> **Risposta:** A: `t_cp=0.8/150≈0.0053333333`, altezza `36×0.8=28.8 mm`. B: `t_cp=0.4/300≈0.0013333333`, altezza 14.4 mm. C: `t_cp=0.4×2/150≈0.0053333333`, altezza 14.4 mm. A e C condividono uno spessore in coordinate ma descrivono ipotesi fisiche diverse. I valori delle coordinate richiedono la relativa scala di misura.

## 5. Dichiara che cosa dimostra un'altezza convertita

Il verificatore legge un singolo stato dichiarato di piegatura piatta. `lib.rs` precisa che i controlli locali non dimostrano la piegabilità piatta globale e non calcolano un ordine degli strati. `thickness.rs` limita l'interpretazione rigida a pannelli paralleli, ciascuno a un'unica altezza. Un ciclo fa rifiutare questa interpretazione per `t` positivo; a spessore zero viene segnalato senza rifiuto. L'assenza di un'altezza rigida in presenza di un ciclo non è uno zero misurato.

Anche un'altezza esatta aciclica non dimostra che una piegatura con spessore sia fisicamente realizzabile: cerniere reali, contatto, flessione e percorso del movimento sono esclusi da questo calcolo. La fonte osserva esplicitamente che pannelli inclinati possono evitare un rifiuto del modello a pannelli paralleli e che il contatto esatto in corrispondenza di pieghe con spessore pone un'ulteriore limitazione. Questo corso non produce alcun esportatore, mesh, collider, simulazione dinamica della piegatura, test sui materiali o integrazione operativa Blender/Godot/DLSS.

### Esercizio pratico 5: scrivere l'affermazione per il passaggio di consegne

Scrivi tre frasi per chi realizzerà un futuro artefatto visuale usando il risultato di riferimento: una sulle evidenze, una sulla corrispondenza con la scena e una su un'affermazione fisica o d'integrazione ancora da verificare.

> **Risposta:** «Al commit IX fissato `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, le asserzioni esaminate nel test della gru specificano 28 strati e 36 livelli esatti di pannelli paralleli per `t=0.4/150`; il coordinatore riporta inoltre 11 test specifici sullo spessore superati a quella revisione invariata. Assumendo un foglio di 150 mm e un'unità di scena per metro, le estensioni derivate per strati e per pannelli rigidi sono 0.0112 e 0.0144 unità di scena. Queste conversioni non dimostrano né la piegabilità fisica né un'importazione Blender/Godot funzionante.» Includi il collegamento alla fixture quando trasferisci questa affermazione.

## Trasferimento e revisione

Completa il [compito separato per il discente senza risposte](../../../reviews/phy-005-learner-task.md) con una nuova larghezza fisica e una nuova scala di scena. Chi revisiona dovrebbe esaminare la fonte alla revisione fissata, ricalcolare le conversioni e controllare la corrispondenza linguistica tramite le [indicazioni per la revisione](../../../reviews/phy-005-review-brief.md). Non sono registrati tentativi di discenti, approvazioni linguistiche da parte di persone con piena padronanza della lingua o verifiche della pubblicazione mediante rilettura. L'artefatto completato qui è una lezione in bozza con un pacchetto aritmetico; il beneficio proposto resta da verificare mediante un trasferimento svolto senza assistenza da un discente reale.
