---
module_id: mus-014-inversions-bass-line
department: music
course: Inversiones y línea de bajo
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-013-root-bass-pitch-class-set]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Inversiones y línea de bajo — Las mismas notas, otro bajo

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, podrás:
- Nombrar la posición de un acorde solo por su bajo: estado fundamental, primera, segunda o tercera inversión
- Escribir la cifra de bajo cifrado de cada posición de una tríada y de un acorde de séptima, y distinguir la cifra 6 del C6 del jazz
- Reconocer los cuatro tipos de acorde de cuarta y sexta y tocar cada uno en la guitarra
- Decir dónde la posición no se lee solo en las notas que suenan, y rastrear cómo trata GA las inversiones en su tipo `Chord`, en sus documentos de voicing y en su catálogo de modos

---

## 1. Las mismas notas, otro bajo

MUS-013 separó la fundamental de un acorde de su bajo. La **posición** de un acorde dice cuál de sus notas está en el bajo. El artículo «Inversion (music)» de Wikipedia: «A chord's inversion describes the relationship of its lowest notes to the other notes in the chord.» (La inversión de un acorde describe la relación entre sus notas más graves y las demás notas del acorde.) Con la fundamental en el bajo, el acorde está en estado fundamental; con otra nota, está en inversión. «The inversions are numbered in the order their lowest notes appear in a close root-position chord (from bottom to top)» (las inversiones se numeran en el orden en que sus notas más graves aparecen en el acorde cerrado en estado fundamental, de abajo arriba): la tercera da la primera inversión, la quinta la segunda, y en un acorde de séptima, la séptima da la tercera. Un acorde de tres notas tiene dos inversiones; «Chords with four notes (such as seventh chords) work in a similar way, except that they have three inversions» (los acordes de cuatro notas, como los de séptima, funcionan de modo parecido, salvo que tienen tres inversiones). El mismo artículo señala que algunos textos reservan el término «inversion» (inversión) para un bajo distinto de la fundamental y usan **posición** para todos los casos; esta lección hace lo mismo.

| Posición | Bajo | Posición cerrada | Sobre el bajo (semitonos) |
|------|------|------|------|
| Estado fundamental | do, la fundamental | do mi sol | tercera mayor (4), quinta justa (7) |
| Primera inversión | mi, la tercera | mi sol do | tercera menor (3), sexta menor (8) |
| Segunda inversión | sol, la quinta | sol do mi | cuarta justa (5), sexta mayor (9) |

Los intervalos sobre el bajo cambian con la posición, y por eso cada una suena distinta: Wikipedia da a la primera inversión «the intervals of a minor third and a minor sixth above the inverted bass of E» (los intervalos de tercera menor y sexta menor sobre el bajo invertido, mi). La fundamental no cambia. En su *Tratado de armonía* (1722), Rameau consideraba las posiciones de un acorde «functionally equivalent» (equivalentes en su función; «Inversion (music)»).

Solo cuenta el bajo. El orden de las notas que tiene encima, sus octavas y sus duplicaciones no cambian la posición. En las tres cuerdas agudas, las posiciones cerradas de do son rotaciones unas de otras:

| Forma | Notas, cuerda 6 primero | Bajo | Posición |
|------|------|------|------|
| xxx553 | do4 mi4 sol4 | do | estado fundamental |
| xxx988 | mi4 sol4 do5 | mi | primera inversión |
| xxx010 | sol3 do4 mi4 | sol | segunda inversión |

Las formas abiertas x32010, 032010 y 332010 de MUS-013 contienen las mismas tres posiciones en cinco o seis cuerdas. Las inversiones también permiten que una línea de bajo avance por grados conjuntos mientras cambian los acordes: C – G/B – Am, tocado x32010 – x20003 – x02210, hace bajar el bajo por do3, si2, la2, con G en primera inversión.

### Ejercicio práctico

Da la posición de 2x0232 y de x00232.

> *Solución:* 2x0232 hace sonar fa♯2 re3 la3 re4 fa♯4. El acorde es re mayor, y fa♯, su tercera, está en el bajo: primera inversión. x00232 hace sonar la2 re3 la3 re4 fa♯4: la, la quinta, está en el bajo, así que es la segunda inversión, D/A.

---

## 2. El bajo cifrado

El bajo cifrado escribe un acorde con números junto a su bajo. El artículo «Figured bass» de Wikipedia los sitúa «above or below (or next to) a bass note» (encima o debajo de una nota del bajo, o a su lado): «The numbers indicate the number of scale steps above the given bass-line that a note should be played.» (Los números indican a cuántos grados por encima de la línea de bajo dada debe tocarse una nota.) Los grados se cuentan por nombres de notas, como los números de los intervalos (MUS-008): sobre sol, do es una cuarta (sol la si do) y mi una sexta. Las cifras «do not express notes in upper voices that double, or are unison with, the bass note» (no expresan las notas de las voces superiores que duplican el bajo o están al unísono con él; «Inversion (music)»), y por lo general ignoran las octavas: una cifra nombra una posición, no un voicing.

Cada posición tiene una cifra completa y una abreviatura habitual. Las tríadas en estado fundamental «appear without symbols (the 53 is understood)» (aparecen sin símbolo, pues el 53 se sobrentiende), y «first-inversion triads are customarily abbreviated as just 6» (las tríadas en primera inversión suelen abreviarse con un simple 6; «Inversion (music)»):

| Posición de la tríada | Cifra completa | Se escribe |
|------|------|------|
| Estado fundamental | 5/3 | nada |
| Primera inversión | 6/3 | 6 |
| Segunda inversión | 6/4 | 6/4 |

Para los acordes de séptima, «Seventh chord» da las cuatro posiciones de G7, sol si re fa, con V7, V6/5, V4/3 y V4/2 o V2:

| Posición | Bajo | Posición cerrada | Cifra completa | Se escribe |
|------|------|------|------|------|
| Estado fundamental | sol | sol si re fa | 7/5/3 | 7 |
| Primera inversión | si | si re fa sol | 6/5/3 | 6/5 |
| Segunda inversión | re | re fa sol si | 6/4/3 | 4/3 |
| Tercera inversión | fa | fa sol si re | 6/4/2 | 4/2 o 2 |

«Figured bass» confirma la última fila: un 2 solo o un 4/2 equivale a 6/4/2. En el análisis, la cifra sigue a un número romano: «the term I6 refers to a tonic triad in first inversion» (el término I6 designa una tríada de tónica en primera inversión; «Inversion (music)»). También puede seguir a una nota del bajo: una tríada de do mayor sobre sol «would be written G64» (se escribiría G64), y sobre mi «E63 or E6 (this is different from the jazz notation, where a C6 means the added sixth chord C–E–G–A, i.e., a C major with an added 6th degree)» (E63 o E6, lo que difiere de la notación del jazz, donde C6 designa el acorde de sexta añadida do–mi–sol–la, es decir, un do mayor con un sexto grado añadido; «Figured bass»). Citadas como texto plano, las cifras superpuestas quedan juntas: G64 es sol con 6/4, E63 es mi con 6/3, y 53 es 5/3. El C6 del cifrado americano es un acorde de cuatro notas con do en el bajo; la cifra E6 es una tríada de do con mi en el bajo.

### Ejercicio práctico

Escribe la cifra de cada acorde sobre su bajo: D/A, Am/C, G7/D, G7/F.

> *Solución:* D/A: sobre la, re es una cuarta y fa♯ una sexta, así que 6/4: la tríada tiene su quinta en el bajo. Am/C: sobre do, mi es una tercera y la una sexta, así que 6. G7/D: sobre re, fa es una tercera, sol una cuarta y si una sexta, así que 6/4/3, escrito 4/3. G7/F: sobre fa, sol es una segunda, si una cuarta y re una sexta, así que 6/4/2, escrito 4/2 o 2.

---

## 3. El acorde de cuarta y sexta

De las posiciones de una tríada, solo la segunda inversión pone una cuarta sobre el bajo. El artículo «Six-four chord» de Wikipedia: «the bass note and the root of the chord are a fourth apart (or a corresponding compound interval) which traditionally qualifies as a dissonance. There is therefore a tendency for movement and resolution.» (el bajo y la fundamental del acorde están a distancia de cuarta, o del intervalo compuesto correspondiente, lo que tradicionalmente cuenta como disonancia. De ahí una tendencia al movimiento y a la resolución.) El voicing sobre el bajo es libre: «Note that any voicing above the bass is allowed.» (Nótese que se permite cualquier voicing sobre el bajo.) Un acorde de cuarta y sexta rara vez es un punto de reposo, y el mismo artículo clasifica sus usos: «There are four types of second-inversion chords: cadential, passing, auxiliary, and bass arpeggiation.» (Hay cuatro tipos de acordes en segunda inversión: cadencial, de paso, de bordadura y de arpegio del bajo.)

| Tipo | En do mayor | Formas | Qué se mueve |
|------|------|------|------|
| Cadencial | C/G – G – C, I6/4 – V – I | 332010 – 320003 – x32010 | Sobre sol2, do3 baja a si2 y mi3 a re3: la cuarta y la sexta bajan a la tercera y la quinta |
| De paso | C – G/D – C/E, I – V6/4 – I6 | x32010 – xx0003 – xx2010 | El bajo avanza por grados do3, re3, mi3; el sol3 al aire se mantiene |
| De bordadura (pedal, auxiliar) | C – F/C – C, I – IV6/4 – I | x32010 – x33211 – x32010 | Sobre do3, mi3 sube a fa3 y sol3 a la3, y luego las dos vuelven |
| Arpegio del bajo | C – C/E – C/G | x32010 – 032010 – 332010 | El bajo toca do3, mi2, sol2 bajo un solo acorde |

- **Cadencial.** «Six-four chord» da dos lecturas. Una, la de la mayoría de los manuales de armonía antiguos, ve en el acorde una tónica en segunda inversión, I6/4 – V – I. La otra, que prefieren varios manuales modernos, oye la dominante con «a double appoggiatura on the V that resolves down by step» (una doble apoyatura sobre el V que resuelve bajando por grado conjunto), escrita V6/4 – 5/3: el bajo sol ya es la dominante, y do y mi son disonancias que resuelven en si y re.
- **De paso.** En un acorde de cuarta y sexta de paso, «the bass passes between two tones a third apart» (el bajo pasa entre dos notas a distancia de tercera), y el acorde, situado entre dos acordes más estables, cae «on the weaker beat between these two chords» (en el tiempo más débil, entre esos dos acordes).
- **De bordadura.** El IV6/4 armoniza una nota de bordadura: «the third and fifth rise a step each and then fall back» (la tercera y la quinta suben un grado cada una y luego vuelven a bajar).
- **Arpegio del bajo.** El bajo recorre la fundamental, la tercera y la quinta de un mismo acorde; la quinta en el bajo forma un acorde de cuarta y sexta, pero nada necesita resolver.

### Ejercicio práctico

Una progresión en do mayor encadena Am – C/G – G7 – C. ¿Qué tipo de acorde de cuarta y sexta es C/G, y cómo puede leerse?

> *Solución:* Es un acorde de cuarta y sexta cadencial: cae antes de la dominante de una cadencia. Una lectura lo llama I6/4, la tónica en segunda inversión. La otra oye la dominante ya en el bajo, sol, con do y mi como doble apoyatura que baja a si y re: V6/4 – 5/3, y G7 añade su séptima, fa, en la resolución.

---

## 4. Cuando las notas no deciden

Una posición se mide desde una fundamental, y las notas que suenan no siempre fijan la fundamental.

- **Dos lecturas, dos posiciones.** MUS-013 mostró que do mi sol la es a la vez C6 y Am7. Sobre do, es C6 en estado fundamental, o Am7/C en primera inversión. El bajo cifrado no nombra ninguna fundamental y escribe la misma cifra para los dos: sobre do, mi es una tercera, sol una quinta y la una sexta, así que 6/5, la cifra de un acorde de séptima en primera inversión.
- **La grafía decide la cifra.** Las cifras cuentan nombres de notas, y un acorde simétrico puede escribirse a partir de cualquiera de sus notas. Mi sol♯ do sobre mi es la tríada aumentada Caug en primera inversión: de mi a do hay una sexta, así que la cifra es 6. Escrito mi sol♯ si♯, es Eaug en estado fundamental: de mi a si♯ hay una quinta, así que la cifra es 5/3. Los dos miden 8 semitonos.
- **La séptima disminuida.** En cada posición de si re fa la♭, las notas sobre el bajo están 3, 6 y 9 semitonos más arriba, así que el sonido no muestra la posición. Los nombres de las notas sí la muestran: si re fa la♭ da 7/5/3, re fa la♭ si 6/5/3, fa la♭ si re 6/4/3, y la♭ si re fa 6/4/2. Como MUS-013 citó de «Diminished seventh chord»: «Understanding what inversion a given diminished seventh chord is written in (and thus finding its root) depends on its enharmonic spelling.» (Entender en qué inversión está escrito un acorde de séptima disminuida, y por tanto encontrar su fundamental, depende de su grafía enarmónica.)

### Ejercicio práctico

Da la cifra y la posición de la♭ si re fa sobre la♭, y del mismo sonido escrito sol♯ si re fa sobre sol♯.

> *Solución:* Sobre la♭, si es una segunda (la si), re una cuarta y fa una sexta: 6/4/2, la tercera inversión de B°7, si re fa la♭. Sobre sol♯, si es una tercera, re una quinta y fa una séptima (de sol a fa): 7/5/3, G♯°7 en estado fundamental.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos de abajo se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Esta lección documenta ese código y no lo modifica. No ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA, en `e610b77`, salvo dos: en `Modes.yaml` las líneas citadas no han cambiado, y en `ModesSkill.cs` el código citado no ha cambiado, pero está en otros números de línea. Esta lección sigue las inversiones a través de tres lugares de GA.

**`Chord` cuenta por rotación.** [`Bass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L260-L263) es `Notes[0]`, documentada como la «lowest note in the voicing» (nota más grave del voicing). [`GetInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L281-L298) devuelve 0 cuando el bajo es la fundamental; si no, busca la fundamental en la lista de notas y devuelve cuántas notas van desde la fundamental hasta el final de la lista. [`ToInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L300-L320) hace girar la lista. Un acorde construido a partir de un símbolo ordena sus notas según el [orden de su fórmula](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L25-L43), do mi sol para C, así que las rotaciones mi sol do y sol do mi cuentan 1 y 2. Las pruebas [`Inversions_ShouldWorkCorrectly`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Harmony/ChordTests.cs#L123-L143) y [`ToInversion_PreservesFormulaAndSymbol`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L134-L154) lo comprueban para C, Cm, Cmaj7, C9 y C13.

Learn, el sitio de cursos del ecosistema, tiene un curso music-theory-ga cuyo laboratorio compila una versión anterior de GA, `a826864`. Su [lección 3](https://github.com/spareilleux/learn/blob/aaf6d3e52490d159ab962c75928e88c0dae28c28/src/content/docs/music-theory-ga/03-chords-and-voicings.mdx#L174-L195) halló que `ToInversion` volvía a analizar las notas giradas y perdía la tercera de una primera inversión, con lo que imprimía la cualidad `Other` para C/E. En `5c3a52a`, `ToInversion` pasa por un [constructor privado](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L64-L71) que copia la fundamental, la fórmula, el símbolo y el conjunto, y solo sustituye las notas. Dos hechos importan para las inversiones:
- **El símbolo no lleva barra.** La primera inversión de C tiene el bajo mi e imprime `C`, ya que el constructor copia el símbolo: [`ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L367) devuelve el símbolo, y la prueba [comprueba que no cambia](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L149).
- **La igualdad ignora el bajo.** [`Equals`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L277) y [`GetHashCode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L365) solo comparan el conjunto y la fundamental, así que C es igual a sus inversiones, como habría querido Rameau.

**Las notas en otro orden se cuentan mal.** El [constructor a partir de notas](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L48-L62) mantiene las notas en el orden dado. Leído, no ejecutado, con la fundamental do:

| Notas | Bajo | Posición | `GetInversion` |
|------|------|------|------|
| mi sol do | mi, la tercera | primera inversión | 1 |
| mi do sol | mi, la tercera | primera inversión | 2 |
| sol do mi | sol, la quinta | segunda inversión | 2 |
| sol mi do | sol, la quinta | segunda inversión | 1 |

`GetInversion` solo mira dónde aparece por primera vez la fundamental en la lista, y cuenta las notas desde ahí hasta el final. En posición cerrada, esa cuenta da la inversión; otros órdenes y duplicaciones pueden alterarla: mi sol do mi, en orden cerrado con mi duplicado arriba, cuenta 2. Un acorde en estado fundamental cuenta 0 en cualquier orden, ya que el bajo es la fundamental. `ToInversion` hereda el error: a partir de mi do sol, `ToInversion(1)` devuelve sol mi do, con la quinta en el bajo, y `GetInversion` dice entonces 1. La [prueba de este constructor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L156-L162) pasa mi sol do, un orden que cuenta bien, y comprueba la cualidad y la fórmula, no la inversión. La lección 3 de Learn da por correcto `GetInversion`; lo es, para las rotaciones que esa lección prueba.

**El documento de voicing cuenta semitonos.** GA describe un voicing con un documento para su búsqueda. [`VoicingDocumentFactory`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L22-L28) toma la nota más grave como bajo y, como fundamental, la del reconocedor de acordes de MUS-013, mediante [`TryGetRootPitchClass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Analysis/ChordIdentificationExtensions.cs#L19-L29). [`CalculateInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L88-L96) convierte luego los semitonos que van de la fundamental al bajo, hacia arriba: 0 da el estado fundamental; 3 o 4 dan 1; 6 o 7 dan 2; 10 u 11 dan 3; cualquier otra distancia da −1. Leído, no ejecutado, con los nombres del reconocedor transcritos de su código; como en MUS-013, la columna de notas nombra cada traste con sostenidos:

| Forma | Nombre en una hoja de acordes | Notas, cuerda 6 primero | Nombre del reconocedor | Bajo sobre la fundamental de GA | Inversión |
|------|------|------|------|------|------|
| 032010 | C/E | mi2 do3 mi3 sol3 do4 mi4 | `C/E` | 4 | 1 |
| 332010 | C/G | sol2 do3 mi3 sol3 do4 mi4 | `C/G` | 7 | 2 |
| 1x0003 | G7/F | fa2 re3 sol3 si3 sol4 | `G7/F` | 10 | 3 |
| x35555 | C6 | do3 sol3 do4 mi4 la4 | `Am7/C` | 3 | 1 |
| xx0233 | Dsus4 | re3 la3 re4 sol4 | `Gsus2/D` | 7 | 2 |
| 032110 | Eaug | mi2 do3 mi3 sol♯3 do4 mi4 | `Caug/E` | 4 | 1 |
| 4x2110 | A♭aug | sol♯2 mi3 sol♯3 do4 mi4 | `Caug/Ab` | 8 | −1 |
| xx0101 | Ddim7 | re3 sol♯3 si3 fa4 | `Fdim7/D` | 9 | −1 |

- **El número sigue a la fundamental de GA.** El C6 y el Dsus4 de las hojas de acordes están en estado fundamental; GA los lee como Am7 y Gsus2, así que da 1 y 2. Eaug, A♭aug y Ddim7 también están en estado fundamental en una hoja de acordes, pero GA los mide desde do, do y fa.
- **El documento quita la barra.** Su `ChordName` [prefiere el nombre canónico del reconocedor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L43-L46), que el nombre con barra [solo prolonga](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L417-L419): el documento de 032010 se llama `C`, y el de 4x2110 `Caug`.
- **Faltan dos distancias de las tríadas y las séptimas.** Una tríada aumentada con su quinta en el bajo tiene ese bajo 8 semitonos por encima de la fundamental, y una séptima disminuida con su séptima en el bajo lo tiene 9 por encima: las dos reciben −1, donde las lecturas que eligió GA las hacen segunda y tercera inversión. Lo mismo ocurre con cualquier bajo 1, 2 o 5 semitonos por encima de la fundamental.
- **Los consumidores lo leen tal cual.** Cuando el servicio de búsqueda de GA indexa documentos, [copia cada inversión](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Search/EnhancedVoicingSearchService.cs#L120) en la entrada, y [`VoicingFilterEngine`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Search/VoicingFilterEngine.cs#L105) solo conserva una entrada si su inversión es igual a la del filtro, así que una búsqueda de segundas inversiones descarta 4x2110. [`AutoTaggingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Enrichment/AutoTaggingService.cs#L164-L168) solo añade una etiqueta `Inversion:n` cuando n es mayor que 0, así que un −1 no recibe etiqueta, como un estado fundamental.
- **Las pruebas se quedan en C/E.** La prueba de la fábrica [espera 1 para C/E y 0 para cuatro formas en estado fundamental](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/VoicingDocumentFactoryTests.cs#L21-L25). Una prueba de búsqueda filtra por 2, con un [documento de fixture](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/Search/SemanticSearchTestFixture.cs#L243-L246) cuya inversión se fija a mano. Una prueba de indexación [pasa 100 voicings generados al indexador](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/Search/VoicingIndexingServiceTests.cs#L18-L34), que construye documentos mediante la fábrica, pero no comprueba ninguna inversión. Ninguna prueba comprueba lo que da `CalculateInversion` para una segunda o tercera inversión, ni para una distancia que convierta en −1.

**Las inversiones de tríadas del catálogo están mal etiquetadas.** El archivo `Modes.yaml` de GA enumera las tríadas como [familias modales](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L424-L492), cada una con entradas nombradas como inversiones, todas con do en el bajo:

| Entrada | Notas | Alias | Qué son las notas | Cifra |
|------|------|------|------|------|
| [Minor Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L432-L436) | do mi♭ la♭ | Minor 6/4 | la♭ mayor, primera inversión | 6 |
| [Minor Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L437-L441) | do fa la | Minor 6/4 | fa mayor, segunda inversión | 6/4 |
| [Major Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L442-L446) | do fa la♭ | Major 6/4 | fa menor, segunda inversión | 6/4 |
| [Major Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L447-L451) | do mi la | Major 6/4 | la menor, primera inversión | 6 |
| [Diminished Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L465-L469) | do mi la | Diminished 6/4 | la menor, primera inversión | 6 |
| [Diminished Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L470-L474) | do fa♯ si♭ | Diminished 6/4 | ninguna tríada: clase de conjuntos 3-8 | — |
| [Augmented Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L483-L487) | do fa la | Augmented 6/4 | fa mayor, segunda inversión | 6/4 |
| [Augmented Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L488-L492) | do mi♭ fa♯ | Augmented 6/4 | do disminuido, estado fundamental, escrito do mi♭ sol♭ | 5/3 |

Ninguna entrada nombra sus notas. La familia mayor contiene los cuatro conjuntos correctos, las inversiones de la♭ y fa mayores y de la y fa menores sobre do, con los nombres intercambiados. Las otras dos familias contienen otras tríadas, y un conjunto que no es una tríada. Cada alias dice 6/4, pero solo tres de las ocho entradas son acordes de cuarta y sexta. Sobre do, las inversiones de la tríada disminuida son do mi♭ la y do fa♯ la, y la tríada aumentada es do mi sol♯ en todas las posiciones, con otra grafía (§4). La cifra de la última fila también requiere esa otra grafía: tal como está escrito, fa♯ es una cuarta sobre do. El vector de intervalos de la familia aumentada, [<0 1 0 0 2 0>](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L476), tampoco es el de la tríada aumentada, <0 0 0 3 0 0>.

`AtonalModalFamilies.yaml` [importa estos nombres por conjunto](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L9-L10). La familia de la tríada mayor recibe [los cuatro nombres](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L185-L204). Las verdaderas inversiones de la tríada disminuida, {0, 3, 9} y {0, 6, 9}, [no reciben ninguno](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L220-L229). {0, 6, 10} [lleva «Diminished Triad Second Inversion»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L290-L294), lo que también da a su familia [el nombre «Diminished Triad Family»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L256-L259), el nombre de [la verdadera](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L206-L207). El archivo también numera estas dos familias [3-5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L258) y [3-3](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L208), donde la lista de Forte da 3-8 y 3-10. Cuando el `ModesSkill` de GA encuentra un vector de intervalos en una pregunta, [responde a partir de este archivo](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L560-L568) [antes que nada](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L156-L164), y [enumera cada modo de la familia](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L628-L656) con este nombre y sus clases de altura, con una confianza de 1.0.

Corregir cualquiera de estas cosas corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

En GA en `5c3a52a`, ¿qué bajo, qué número de inversión y qué nombre impreso tiene la tercera inversión de `Chord.FromSymbol("G7")`? ¿Qué inversión da el documento de voicing a G7/F, 1x0003?

> *Solución:* Las notas sol si re fa giran a fa sol si re: bajo fa, `GetInversion` 3, y el acorde imprime `G7`, ya que el símbolo se conserva. Para 1x0003, el reconocedor da `G7/F`; fa está 10 semitonos por encima de sol, así que `CalculateInversion` da 3. Los dos dicen tercera inversión, y ningún nombre muestra el bajo: el documento también se llama `G7`.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA. La versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`. Nada en esta sección es una medición:
- las predicciones vienen del §5 y se escriben antes de cualquier ejecución;
- vienen de una transcripción en Python, línea por línea, de `Chord`, de `CalculateInversion` y del reconocedor de acordes, y de la lectura de los dos archivos de catálogo de GA;
- una versión posterior de esta lección informará de los resultados.

Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Rotaciones a partir de símbolos.** Para C, Cmaj7, G7 y C6 construidos con `Chord.FromSymbol`, llamar a `ToInversion(k)` para cada k, y anotar `Bass`, `GetInversion`, `Symbol` y `Equals` con el original. Predicción: el bajo es la nota de índice k, contando desde 0, en do mi sol, do mi sol si, sol si re fa y do mi sol la; `GetInversion` devuelve k; el símbolo no cambia; `Equals` es verdadero.
2. **Órdenes.** Construir `new Chord(AccidentedNoteCollection.Parse(...), C)` a partir de mi sol do, mi do sol, sol do mi y sol mi do, y llamar a `GetInversion`; luego llamar a `ToInversion(1)` sobre el acorde mi do sol. Predicción: 1, 2, 2 y 1; luego las notas sol mi do, con `GetInversion` 1.
3. **Documentos de voicing.** Para las ocho formas de la tabla del §5, construir el documento de voicing como lo hace `VoicingDocumentFactoryTests`, con cada diagrama escrito desde la cuerda 1 (032010 pasa a ser `0-1-0-2-3-0`), y anotar `RootPitchClass`, `MidiBassNote` e `Inversion`. Predicción, en el orden de la tabla: las fundamentales 0, 0, 7, 9, 7, 0, 0 y 5; los bajos 40, 43, 41, 48, 50, 40, 44 y 50; las inversiones 1, 2, 3, 1, 2, 1, −1 y −1.
4. **El catálogo.** Cargar la configuración de modos de GA y sus familias modales atonales, y, para cada modo cuyo nombre contenga «Inversion», identificar la tríada que forman sus notas sobre do. Predicción: la tabla del §5, sin que ninguna entrada nombre sus notas; en el archivo atonal, {0, 3, 9} y {0, 6, 9} no tienen nombre tonal.

### Ejercicio práctico

El paso 3 predice −1 para 4x2110. ¿Cómo lo nombra una hoja de acordes, qué posición le da la lectura de GA, y qué distancia le falta a `CalculateInversion`?

> *Solución:* Una hoja de acordes suele nombrar la lectura cuya fundamental está en el bajo: A♭aug, en estado fundamental. El reconocedor toma do como fundamental, `Caug/Ab`; para do, el bajo es la quinta aumentada sol♯, así que la forma es una segunda inversión, con el bajo 8 semitonos por encima de do. `CalculateInversion` solo reconoce una quinta en el bajo a 6 o 7 semitonos, la quinta disminuida y la justa.

---

## 7. Errores comunes

- **Leer la posición en la nota más aguda o en la forma.** Solo cuenta el bajo: xxx988 y 032010 son ambos primeras inversiones.
- **Leer el C6 del jazz como la cifra 6.** C6 añade la a una tríada de do sobre do; la cifra E6 es una tríada de do sobre mi.
- **Tratar un acorde de cuarta y sexta como un acorde de reposo.** La cuarta sobre el bajo es una disonancia; el acorde pasa, borda, arpegia o resuelve en una dominante.
- **Dar una posición sin fundamental.** Sobre do, do mi sol la está en estado fundamental como C6 y en primera inversión como Am7/C.
- **Leer una posición en semitonos.** La séptima disminuida tiene 3, 6 y 9 semitonos sobre su bajo en todas sus posiciones; solo la grafía las distingue.
- **Fiarse de los nombres de GA para las inversiones de tríadas.** Ninguna de las ocho entradas de `Modes.yaml` nombra sus notas.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Posición** | La nota del acorde que está en el bajo: estado fundamental, o una inversión |
| **Estado fundamental** | La fundamental en el bajo |
| **Primera, segunda, tercera inversión** | La tercera, la quinta o la séptima en el bajo |
| **Bajo cifrado** | Números junto a una nota del bajo para los intervalos que tiene encima, contados por nombres de notas |
| **Cifra** | Esos números, por lo general abreviados: 6, 6/4, 7, 6/5, 4/3, 4/2 |
| **Acorde de cuarta y sexta** | Una tríada en segunda inversión, con una cuarta y una sexta sobre el bajo |
| **Cuarta y sexta cadencial** | I6/4 antes de V, o la dominante con una doble apoyatura, V6/4 – 5/3 |
| **Cuarta y sexta de paso, de bordadura, de arpegio** | Un acorde de cuarta y sexta sobre un bajo que pasa por grados entre dos notas a distancia de tercera; sobre un bajo mantenido, con dos voces que suben un grado y vuelven; con un bajo que recorre un solo acorde |

---

## Autoevaluación

**1. Da la posición y la cifra de Em/G, 3x2000, y de Am/E, 002210.**
> 3x2000 hace sonar sol2 mi3 sol3 si3 mi4: sol, la tercera de mi menor, está en el bajo, así que primera inversión, cifra 6 (si es una tercera y mi una sexta sobre sol). 002210 hace sonar mi2 la2 mi3 la3 do4 mi4: mi, la quinta de la menor, está en el bajo, así que segunda inversión, cifra 6/4 (la es una cuarta y do una sexta sobre mi).

**2. Sobre do, ¿por qué do mi sol la está en estado fundamental como C6 y en primera inversión como Am7/C, y qué cifra escribe el bajo cifrado?**
> Una posición se mide desde la fundamental, y las dos lecturas tienen fundamentales distintas, do y la. El bajo cifrado no nombra ninguna fundamental: sobre do, mi es una tercera, sol una quinta y la una sexta, así que escribe 6/5 para las dos.

**3. En C – F/C – C, ¿qué tipo de acorde de cuarta y sexta es F/C, y qué se mueve?**
> Un acorde de cuarta y sexta de bordadura (pedal o auxiliar), IV6/4. Sobre el do mantenido, mi y sol suben un grado a fa y la, y luego vuelven a bajar.

**4. ¿Qué inversión da el documento de voicing de GA a Ddim7, xx0101, y por qué?**
> −1. El reconocedor nombra la forma `Fdim7/D`, así que la fundamental es fa, y re está 9 semitonos por encima de fa, una distancia que `CalculateInversion` no convierte.

**Criterio de aprobación:** Nombrar la posición de cualquier voicing por su bajo. Escribir las cifras de las tríadas y de los acordes de séptima en todas las posiciones, y distinguirlas de los símbolos de acorde. Nombrar los cuatro tipos de acorde de cuarta y sexta y tocar cada uno. Decir dónde el sonido solo no fija la posición, y dónde se equivocan el `Chord`, los documentos de voicing y el catálogo de GA.

---

## Base de investigación

- Wikipedia, «Inversion (music)»: la definición y la numeración de las inversiones, los intervalos de la primera inversión, las cifras 53 y 6, I6, «position» (posición), y Rameau.
- Wikipedia, «Figured bass»: los grados sobre el bajo, 2 por 6/4/2, G64 y E6 frente al C6 del jazz.
- Wikipedia, «Six-four chord»: la cuarta como disonancia, el voicing libre sobre el bajo, y los cuatro tipos.
- Wikipedia, «Seventh chord»: las cuatro posiciones de G7 en notación de bajo cifrado.
- Wikipedia, «Diminished seventh chord»: la posición que solo indica la grafía, como se citó en MUS-013.
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §5 enlaza a su línea.
- Learn, lección 3 de music-theory-ga en el commit `aaf6d3e52490d159ab962c75928e88c0dae28c28`: su comprobación de las inversiones sobre GA `a826864`.
- Citado por el plan de currículo de Streeling y no consultado para esta versión: Aldwell y Schachter, *Harmony and Voice Leading*, capítulos 5 y 9.
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia.
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión.
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
