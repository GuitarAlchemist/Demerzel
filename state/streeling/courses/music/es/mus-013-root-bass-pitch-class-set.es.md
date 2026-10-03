---
module_id: mus-013-root-bass-pitch-class-set
department: music
course: Fundamental, bajo y conjunto de clases de altura
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-012-chord-formulas-essential-tones-doubling, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Fundamental, bajo y conjunto de clases de altura — Un conjunto, varios nombres

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, podrás:
- Distinguir la fundamental de un acorde, su bajo y su conjunto de clases de altura, y decir qué fija cada uno de estos: un símbolo de acorde, una barra y un voicing
- Encontrar todas las fundamentales que leen un conjunto como un acorde con nombre, y reconocer los conjuntos que tienen más de una: acordes de sexta y de séptima, sus2 y sus4, la tríada aumentada, la séptima disminuida
- Elegir entre las lecturas por el bajo, la armonía y la resolución, y escribir la elección como acorde con barra cuando el bajo no es la fundamental
- Rastrear cómo GA da un solo nombre a cada conjunto de clases de altura sin mirar el bajo, y dónde ese nombre pierde una nota o una grafía

---

## 1. Tres cosas en un nombre de acorde

Un acorde tocado en una guitarra tiene tres propiedades, y un nombre de acorde las mezcla.

- **El conjunto de clases de altura** es el conjunto de las notas del acorde sin las octavas ni las duplicaciones (MUS-020). La forma x32010 hace sonar do3 mi3 sol3 do4 mi4, y su conjunto es {do, mi, sol}, o {0, 4, 7} con do = 0.
- **El bajo** es la nota más grave que suena: do3 en x32010. Pertenece al voicing, no al conjunto.
- **La fundamental** es la nota que da nombre al acorde. Para un acorde construido por terceras, el artículo «Root (chord)» de Wikipedia da el método: «reorganize the pitches as a stack of thirds and then identify the lowest note in the stack» (reorganizar las alturas como un apilamiento de terceras y luego identificar la nota más grave del apilamiento). Las notas do, mi y sol forman un apilamiento de terceras sobre do, así que la fundamental es do, dondequiera que suene do.

La fundamental no tiene por qué ser el bajo. Con la fundamental en el bajo, el acorde está en estado fundamental; con otra nota del acorde en el bajo, está en inversión, una inversión del acorde y no de un intervalo como en MUS-008. Un **acorde con barra** (slash chord) escribe el bajo después de una barra: C/E es una tríada de do mayor con mi en el bajo. El artículo «Slash chord» de Wikipedia añade que la barra «does not indicate 'or'» (no indica «o»). Tres voicings de do mayor comparten un mismo conjunto:

| Forma | Notas, cuerda 6 primero | Conjunto | Bajo | Fundamental | Símbolo |
|------|------|------|------|------|------|
| x32010 | do3 mi3 sol3 do4 mi4 | {0, 4, 7} | do | do | C |
| 032010 | mi2 do3 mi3 sol3 do4 mi4 | {0, 4, 7} | mi | do | C/E |
| 332010 | sol2 do3 mi3 sol3 do4 mi4 | {0, 4, 7} | sol | do | C/G |

Un símbolo de acorde fija una fundamental y un conjunto. Una barra añade el bajo. Un voicing añade octavas y duplicaciones, y puede omitir notas (MUS-012).

### Ejercicio práctico

Da el conjunto, el bajo, la fundamental y el símbolo de 2x0232.

> *Solución:* 2x0232 hace sonar fa♯2 re3 la3 re4 fa♯4. El conjunto es {re, fa♯, la}, o {2, 6, 9}, y el bajo es fa♯. La fundamental es re, ya que re fa♯ la es un apilamiento de terceras sobre re. El símbolo es D/F♯, el acorde central del descenso G – D/F♯ – Em que el artículo «Slash chord» de Wikipedia da como ejemplo.

---

## 2. Un conjunto, varias fundamentales

Apilar terceras da una sola fundamental para una tríada o un acorde de séptima sin huecos en su apilamiento, salvo si el apilamiento cierra la octava: la tríada aumentada y la séptima disminuida son apilamientos de terceras desde cualquiera de sus notas, como muestra el tercer punto de abajo. Algunos conjuntos se leen desde más de una de sus notas, y cada lectura es correcta. Las notas la, do, mi y sol forman un apilamiento de terceras sobre la: es el acorde de séptima menor Am7. También es una tríada de do mayor con un la añadido, una sexta por encima de do: es C6. El artículo «Sixth chord» de Wikipedia dice de C6: «Because it is also an A minor seventh chord in first inversion, it is tonally ambiguous. Identifying the root depends on context.» (Como también es un acorde de la menor séptima en primera inversión, es tonalmente ambiguo. Identificar su fundamental depende del contexto).

| Notas | Conjunto | Lecturas |
|------|------|------|
| do mi sol la | {0, 4, 7, 9} | C6, Am7 |
| do mi♭ sol la | {0, 3, 7, 9} | Cm6, Am7♭5 |
| do re sol | {0, 2, 7} | Csus2, Gsus4 |
| do mi sol♯ | {0, 4, 8} | Caug, Eaug, A♭aug |
| do mi♭ sol♭ la | {0, 3, 6, 9} | Cdim7, E♭dim7, G♭dim7, Adim7 |

Cada lectura escribe las notas a su manera. Como Eaug, el do de la cuarta fila es si♯; como A♭aug, el sol♯ es la♭, lo que da el ejemplo de tríada aumentada de Wikipedia, la♭–do–mi («Augmented triad»).

- **Acordes de sexta y de séptima.** C6 y Am7 comparten un conjunto, y también Cm6 y Am7♭5. El artículo «Sixth chord» de Wikipedia da más nombres para do mi♭ sol la: «might be written as Cm6, F9, F9 (no root), Am7♭5, B7♭9, A♭Maj7♭9, or Balt» (puede escribirse Cm6, F9, F9 sin fundamental, Am7♭5, B7♭9, A♭Maj7♭9 o Balt). Uno de ellos es un error: B7♭9 es si re♯ fa♯ la do, con fa♯ y sin sol, así que no contiene el conjunto.
- **Acordes suspendidos.** Csus2 es do re sol y Gsus4 es sol do re: las mismas tres notas. Para un acorde suspendido, «Root (chord)» dice que hay que «identify the triad that has been modified and then find its root» (identificar la tríada que se ha modificado y luego encontrar su fundamental). Las notas do, re y sol forman una tríada de do con re en lugar de mi, o una tríada de sol con do en lugar de si; el conjunto no dice cuál.
- **Acordes simétricos.** La tríada aumentada divide la octava en tres terceras mayores, 4 + 4 + 4 = 12 semitonos, y la séptima disminuida en cuatro terceras menores, 3 + 3 + 3 + 3 = 12. Transportar cualquiera de las dos por uno de sus propios intervalos devuelve el mismo conjunto (MUS-020), así que cada una de sus notas lo lee como el mismo tipo de acorde. Como conjuntos, solo hay cuatro tríadas aumentadas y tres acordes de séptima disminuida; Wikipedia: «there are only three distinct diminished seventh chords (as opposed to twelve)» (solo hay tres acordes de séptima disminuida distintos, y no doce; «Diminished seventh chord»).

Para un acorde de séptima disminuida, el mismo artículo remite a las notas escritas: «Understanding what inversion a given diminished seventh chord is written in (and thus finding its root) depends on its enharmonic spelling.» (Entender en qué inversión está escrito un acorde de séptima disminuida, y por tanto encontrar su fundamental, depende de su grafía enarmónica). Un conjunto de clases de altura no tiene grafía (MUS-007): {0, 3, 6, 9} es do mi♭ sol♭ si𝄫 como Cdim7, y la do mi♭ sol♭ como Adim7.

### Ejercicio práctico

¿Qué notas de mi sol si♭ do♯ pueden ser la fundamental de un acorde de séptima disminuida? ¿A qué fundamental apunta la grafía mi sol si♭ re♭?

> *Solución:* Las cuatro: el conjunto {1, 4, 7, 10} es un apilamiento de terceras menores desde cualquiera de sus notas. Escrito mi sol si♭ re♭, el apilamiento empieza en mi: mi–sol, sol–si♭ y si♭–re♭ son terceras menores, y re♭ es una séptima disminuida por encima de mi, así que el acorde es Edim7. Escrito con do♯, el apilamiento empieza en do♯: do♯ mi sol si♭, C♯dim7.

---

## 3. Elegir entre lecturas

El conjunto da los candidatos. El bajo, la armonía y la resolución eligen entre ellos.

- **El bajo.** Un cifrado suele nombrar la lectura cuya fundamental está en el bajo: las notas la do mi sol con la en el bajo son Am7, y con do en el bajo, C6. Sobre cualquier otra nota del bajo hace falta una barra. Am7/C no es incorrecto: nombra las mismas notas con fundamental la y bajo do. Cuál de los dos escribe un cifrado dice qué fundamental usa la armonía.
- **La armonía.** Después de G7 en do mayor, las notas la do mi sol con do en el bajo son la tónica, C6. En sol mayor, entre Em y D7, las mismas notas son el acorde ii7: Am7, escrito Am7/C si do está en el bajo. Para do mi♭ sol la, el artículo «Sixth chord» de Wikipedia elige entre Cm6 y F9 por el «analysis of the movement of the root, in the presence of dominant-functioning harmonies» (análisis del movimiento de la fundamental, en presencia de armonías con función de dominante).
- **La resolución.** «A common suspension is a fourth above the root resolving to the third of the chord» (una suspensión habitual es una cuarta por encima de la fundamental que resuelve en la tercera del acorde; Wikipedia, «Suspended chord»). El conjunto re sol la, cuando resuelve en re fa♯ la, es Dsus4, no Gsus2 sobre re. Para un acorde de séptima disminuida, «resolution is a better indicator of function than spelling» (la resolución indica la función mejor que la grafía; Wikipedia, «Diminished seventh chord»): el acorde sobre la sensible de do, si re fa la♭, resuelve en la tónica.

Los acordes con barra también sirven a los arreglistas. El artículo «Slash chord» de Wikipedia escribe F/D para un Dm7, para que un principiante pueda tocar una tríada de fa sobre re, y B°7/G para G7♭9. Ambos escriben un conjunto como un acorde conocido sobre un bajo: F/D es re fa la do, y B°7/G es sol si re fa la♭.

### Ejercicio práctico

Un cifrado en do mayor termina Dm7 – G7 – ?, y el último acorde se toca x35555. Nómbralo.

> *Solución:* x35555 hace sonar do3 sol3 do4 mi4 la4: el conjunto {do, mi, sol, la} con do en el bajo. Después de G7, la cadencia llega a la tónica do, así que el acorde es C6. Am7/C nombra las mismas notas, pero con fundamental la.

---

## 4. Formas de guitarra con dos nombres

Muchas formas habituales contienen uno de los conjuntos del §2 o una de sus transposiciones. El nombre del cifrado sigue al bajo y a la resolución habitual; las demás lecturas necesitan una barra.

| Forma | Notas, cuerda 6 primero | Nombre del cifrado | Conjunto | Otras lecturas |
|------|------|------|------|------|
| x02010 | la2 mi3 sol3 do4 mi4 | Am7 | {la, do, mi, sol} | C6/A |
| x35555 | do3 sol3 do4 mi4 la4 | C6 | {la, do, mi, sol} | Am7/C |
| xx0233 | re3 la3 re4 sol4 | Dsus4 | {re, sol, la} | Gsus2/D |
| x02230 | la2 mi3 la3 re4 mi4 | Asus4 | {la, re, mi} | Dsus2/A |
| xx0230 | re3 la3 re4 mi4 | Dsus2 | {la, re, mi} | Asus4/D |
| 022200 | mi2 si2 mi3 la3 si3 mi4 | Esus4 | {mi, la, si} | Asus2/E |
| xx0101 | re3 sol♯3 si3 fa4 | Ddim7 | {re, fa, sol♯, si} | Fdim7/D, G♯dim7/D, Bdim7/D |
| 032110 | mi2 do3 mi3 sol♯3 do4 mi4 | Eaug | {mi, sol♯, do} | Caug/E, A♭aug/E |

La columna de notas nombra cada traste con sostenidos; no es la grafía del acorde. Como Ddim7, xx0101 se escribe re fa la♭ do♭, y como Eaug, 032110 se escribe mi sol♯ si♯.

Dos formas, x02230 y xx0230, contienen el mismo conjunto {la, re, mi}: solo el bajo y la resolución separan Asus4 de Dsus2. Cada forma sus4 se resuelve un traste más abajo: xx0233 a D xx0232 (sol4 baja a fa♯4), x02230 a A x02220 (re4 a do♯4), y 022200 a E 022100 (la3 a sol♯3). Las dos últimas filas contienen conjuntos simétricos que Wikipedia usa como ejemplos. El conjunto de xx0101 es el de G♯dim7, «G♯–B–D–F» (sol♯–si–re–fa), del que «Diminished seventh chord» dice que es «enharmonically equivalent to three other inverted diminished chords» (enarmónicamente equivalente a otros tres acordes disminuidos invertidos); el conjunto de 032110 es el de A♭+, la♭–do–mi, el ejemplo con el que empieza «Augmented triad».

### Ejercicio práctico

Nombra 3x0013 como lo haría un cifrado, y da la otra lectura de su conjunto.

> *Solución:* 3x0013 hace sonar sol2 re3 sol3 do4 sol4: el conjunto {sol, do, re} con sol en el bajo. Un cifrado lo nombra Gsus4, ya que el do suele bajar a si y da G. El mismo conjunto es Csus2, escrito sobre este bajo Csus2/G.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos de abajo se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Esta lección documenta ese código y no lo modifica. No ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA, en `ba3b9ac`. Learn, el sitio de cursos del ecosistema, tiene un curso music-theory-ga cuyas lecciones compilan una versión anterior de GA, `a826864`; los archivos del reconocedor han cambiado desde entonces. Su lección 3 [nombra una forma](https://github.com/spareilleux/learn/blob/89dc3e64d392cdc36844b03719880484d823b4d7/src/content/docs/music-theory-ga/03-chords-and-voicings.mdx#L240) probando primero el bajo, como hace un cifrado, y pide al catálogo de GA los intervalos medidos desde el bajo. Esta lección sigue al reconocedor de acordes de GA, que elige la fundamental por sí mismo.

**GA nombra un conjunto de clases de altura sin su bajo.** [`CanonicalChordRecognizer.Identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L26-L39) recibe un conjunto y un bajo opcional. Su comentario dice que [«Everything except the slash suffix is a function of the pitch-class set alone»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L30-L31) (todo, salvo el sufijo con barra, depende solo del conjunto de clases de altura), y el método guarda [una respuesta por conjunto](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L34). Para tres clases de altura o más:
- cada nota del conjunto se prueba como fundamental contra cada patrón del catálogo, y un patrón puede [carecer de un intervalo y añadir uno](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L153-L166);
- los candidatos se [ordenan](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L178-L183) por distancia (intervalos que faltan más intervalos que sobran), luego por no faltar nada, luego por la prioridad del patrón (primero el número más bajo), luego por una [puntuación de frecuencia de la fundamental](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L362-L377): do vale 0, sol y fa 1, re y si♭ 2, la y mi♭ 3, y así sucesivamente;
- [«the bass note must NOT influence which pattern wins»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L171-L173) (el bajo NO debe influir en qué patrón gana);
- un bajo distinto de la fundamental se añade después como [sufijo con barra](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L35-L38).

Una prueba recorre [los 4096 conjuntos con cada uno de los 12 bajos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Chords/CanonicalChordRecognizerCacheTests.cs#L24-L46) y comprueba que el bajo solo cambia el sufijo. El analizador de voicings de GA pasa la [nota más grave del voicing como bajo](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L12-L17) y guarda [el nombre con su sufijo](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L72-L80) como nombre de acorde del voicing.

**El conjunto la do mi sol siempre es Am7.** Minor-7 tiene [prioridad 5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L63) y major-6 [prioridad 10](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L55). Las dos lecturas son exactas, así que Am7 gana sea cual sea el bajo, y la forma de C6 x35555 se nombra `Am7/C`. La lista de exclusiones de la prueba de ida y vuelta lo dice: [«major-6 [0,4,7,9] ≡ minor-7 at root 9 (priority 5 beats 10)»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L39) (major-6 equivale a minor-7 sobre la fundamental 9; la prioridad 5 gana a 10). Su corpus de referencia espera [Am7 para x02010](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L424-L426). El reconocedor no puede dar el C6 de la cadencia del §3.

**Los empates van a la fundamental más frecuente.** sus2 y sus4 tienen ambos [prioridad 8](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L51-L52), así que entre dos lecturas de un conjunto sus decide la puntuación de frecuencia de la fundamental. Sol vale 1 y re 2, así que el Dsus4 xx0233 se nombra `Gsus2/D`. El corpus de referencia [espera Gsus2](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L451-L456), y su comentario explica la elección como sus4 sobre re «(prio 8)» frente a sus2 sobre sol «(prio 7)». El catálogo da 8 a ambos: desempata la puntuación de la fundamental, no la prioridad. El mismo comentario dice que el «Dsus4» del guitarrista es «recovered» (recuperado) como `Gsus2/D`; esa es la otra lectura de la tabla del §4, no el nombre del cifrado. Csus4 y Dsus2 [salen como en el cifrado](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L443-L449), porque do tiene una puntuación más baja que fa, y re más baja que la. La séptima disminuida tiene [prioridad 7](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L66) en cada una de sus cuatro fundamentales, y la tríada aumentada [prioridad 3](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L50) en cada una de sus tres, así que la puntuación de la fundamental basta para nombrarlas.

**Los nombres se escriben con bemoles.** Las fundamentales y los sufijos vienen de una misma [lista de doce nombres](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L379-L383), C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B, que también construye los [sufijos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L51-L52). Un acorde de fa♯ menor es `Gbm`, y el D/F♯ del descenso es `D/Gb`. El reconocedor trabaja con clases de altura, que no llevan grafía (MUS-007), así que la pista que Wikipedia da para la fundamental de una séptima disminuida no está a su alcance.

**Un nombre oculta la novena.** El catálogo lista dos veces el conjunto do re mi sol la: como [major-6-add-9, prioridad 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L57), y como [6-9, prioridad 54](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L111). Sus observaciones llaman a los dos nombres [sinónimos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L166-L168). El constructor de sufijos tiene un caso para [«6-9»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L281) pero ninguno para major-6-add-9. Ese patrón recibe su [calidad, su extensión y sus alteraciones](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L293) seguidas: nada para mayor, «6» para la sexta, y nada para «add9», una [alteración que no se imprime](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L307). Leído, no ejecutado: do re mi sol la tiene cinco lecturas exactas, major-6-add-9 sobre do, 9-sus4 sobre re, dominant-11 sobre re, 6-9 sobre do y quartal-5 sobre mi. La primera tiene el número de prioridad más bajo, así que el reconocedor nombra el conjunto `C6`. Minor-6-add-9 convierte del mismo modo do re mi♭ sol la en `Cm6`. Como la do mi sol es Am7, un `C6` del reconocedor nunca es el C6 del §2: contiene una novena. La prueba de ida y vuelta comprueba el nombre del patrón, la distancia, la fundamental y el indicador de exactitud, [pero no el nombre que imprime](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L134-L142), así que pasa.

**El ejemplo simétrico de la prueba no es simétrico.** La lista de exclusiones dice que [«dominant-7-sharp-5 [0,4,8,10] is T4-symmetric — multiple roots, same set»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L43) (dominant-7-sharp-5 es simétrico por T4: varias fundamentales, el mismo conjunto). Transportado 4 semitonos, do mi sol♯ si♭ se convierte en mi sol♯ do re, otro conjunto. Sus únicas lecturas exactas están sobre do, con dos nombres para los mismos intervalos, [augmented-7](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L68) y [dominant-7-sharp-5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L95). La ida y vuelta devuelve augmented-7, prioridad 8 antes que 30, y la exclusión se sostiene por eso. Los acordes de cuatro notas del catálogo sí contienen dos conjuntos simétricos: la séptima disminuida del §2, y [dominant-7-b5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L94), do mi sol♭ si♭, que una transposición de un tritono lleva sobre sí mismo: C7♭5 es también G♭7♭5.

**Los conjuntos sin coincidencia reciben un nombre de Forte y ninguna fundamental.** Un conjunto al que ningún patrón se ajusta con un intervalo que falte y uno que sobre como mucho se nombra por su [número de Forte](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L320-L356), sin fundamental, y [solo una coincidencia con un patrón](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L43-L44) puede llevar un sufijo con barra. Para un conjunto así, el analizador de voicings de GA [guarda el bajo como fundamental del voicing](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L84), escrito por [`PitchClass.ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L83-L88) como un número, con T para 10 y E para 11, donde un conjunto reconocido guarda un nombre de nota. El nombre del acorde no se ve afectado. MUS-020 trata el catálogo de Forte.

Corregir todo esto corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

Según la ordenación de GA, ¿qué devuelve `Identify` para do re sol con sol en el bajo, y para mi sol♯ do con mi en el bajo?

> *Solución:* Para do re sol, Csus2 y Gsus4 son ambos exactos con prioridad 8, y do vale 0 frente al 1 de sol, así que la fundamental es do. Sol no es la fundamental, así que el nombre es `Csus2/G`. Para mi sol♯ do, Caug, Eaug y Abaug son exactos con prioridad 3; do vale 0, mi y la♭ 4, así que el nombre es `Caug/E`.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA. La versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`. Nada en esta sección es una medición:
- las predicciones vienen de los §2 a §5 y se escriben antes de cualquier ejecución;
- los nombres y los recuentos vienen de una transcripción en Python, línea por línea, del reconocedor y de su catálogo de patrones;
- una versión posterior de esta lección informará de los resultados.

Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **El bajo solo cambia el sufijo.** Para las ocho formas del §4 y cuatro más, llamar a `Identify` con el conjunto solo, y luego con el bajo de la forma. Predicción:

   | Forma | Sin el bajo | Con el bajo |
   |------|------|------|
   | x02010 | Am7 | Am7 |
   | x35555 | Am7 | Am7/C |
   | xx0233 | Gsus2 | Gsus2/D |
   | x02230 | Dsus2 | Dsus2/A |
   | xx0230 | Dsus2 | Dsus2 |
   | 022200 | Asus2 | Asus2/E |
   | xx0101 | Fdim7 | Fdim7/D |
   | 032110 | Caug | Caug/E |
   | 3x0013 | Csus2 | Csus2/G |
   | x03221 | Faug | Faug/A |
   | 244222 | Gbm | Gbm |
   | 2x0232 | D | D/Gb |

2. **El censo.** Para cada uno de los 4096 conjuntos, llamar a `Identify` y anotar `MatchDistance`. Para cada conjunto de tres clases de altura o más, contar las fundamentales en las que algún patrón del catálogo coincide exactamente. Predicción:
   - de los 4017 conjuntos de tres clases de altura o más, 484 coinciden exactamente, 1644 a distancia 1 y 648 a distancia 2, y 1241 recurren a un nombre de Forte;
   - los únicos conjuntos de cuatro notas que recurren a él son las seis transposiciones de do re♭ sol♭ sol;
   - 124 conjuntos tienen lecturas exactas sobre dos fundamentales o más. Salvo transposición, son 15: el conjunto sus2, el conjunto 7sus4, el conjunto 7sus2, m7♭5, m7, 7♭5, la tríada aumentada, la séptima disminuida, 7♭9♯9, el conjunto 6/9, m11, 7♭9♯11, y las escalas aumentada, de tonos enteros y octatónica.
3. **Los acordes de sexta.** Contar los conjuntos cuyo nombre termina en `6` pero no en `m6`, y los que terminan en `m6`, y comprobar en cada uno la novena sobre su fundamental; contar los nombres que terminan en `6/9`. Predicción: 48 y 60 conjuntos, todos con su novena, y ningún conjunto llamado 6/9 o m6/9. El conjunto la do mi sol se llama Am7, y do mi♭ sol la, Am7b5.
4. **El ejemplo simétrico.** Identificar do mi sol♯ si♭ y su transposición de 4 semitonos, y luego do mi sol♭ si♭ y su transposición de 6. Predicción: `Caug7` y `Eaug7`, dos conjuntos distintos; `C7b5` las dos veces, un solo conjunto.

### Ejercicio práctico

El paso 2 predice 124 conjuntos con lecturas exactas sobre dos fundamentales o más, que salen de 15 conjuntos salvo transposición. ¿Por qué la tríada aumentada y la séptima disminuida solo aportan 4 y 3 conjuntos, cuando la do mi sol y sus transposiciones aportan 12?

> *Solución:* Un conjunto que una transposición lleva sobre sí mismo tiene menos transposiciones distintas. La tríada aumentada se lleva sobre sí misma con 4 semitonos, así que tiene 12 / 3 = 4 transposiciones; la séptima disminuida se lleva sobre sí misma con 3 semitonos, así que tiene 12 / 4 = 3. El conjunto la do mi sol no se lleva sobre sí mismo con ninguna transposición salvo T0, así que tiene 12.

---

## 7. Errores comunes

- **Tomar el bajo por la fundamental.** C/E tiene fundamental do; el bajo es una propiedad del voicing.
- **Leer la barra como «o».** C/E significa un acorde de do sobre mi.
- **Llamar incorrecta a una lectura.** C6 y Am7/C son las mismas notas; la armonía decide qué fundamental nombrar.
- **Nombrar una séptima disminuida por su conjunto.** Cada una de sus notas puede ser la fundamental; la grafía y la resolución deciden.
- **Fiarse del `C6` de GA.** Si viene del reconocedor, contiene una novena: es un acorde 6/9.
- **Tomar el nombre con barra de GA por el nombre del cifrado.** `Gsus2/D` es la otra lectura de Dsus4, elegida por la puntuación de frecuencia de la fundamental de GA.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Conjunto de clases de altura** | Las notas de un acorde sin las octavas ni las duplicaciones, como {0, 4, 7} |
| **Bajo** | La nota más grave que suena; una propiedad del voicing |
| **Fundamental** | La nota que da nombre a un acorde; para un acorde por terceras, la nota más grave del apilamiento de terceras |
| **Inversión** | Un voicing de un acorde con una nota del acorde distinta de la fundamental en el bajo |
| **Acorde con barra** | Un símbolo de acorde seguido de su bajo, como C/E |
| **Lectura** | Una fundamental y un tipo de acorde que juntos dan exactamente un conjunto: C6 y Am7 son dos lecturas de la do mi sol |
| **Acorde simétrico** | Un acorde cuyo conjunto se lleva sobre sí mismo con una transposición distinta de T0, como la tríada aumentada y la séptima disminuida |
| **Frecuencia de la fundamental** | El desempate de GA entre lecturas igual de buenas: primero do, luego sol y fa, luego re y si♭, y así sucesivamente |

---

## Autoevaluación

**1. Da el conjunto, el bajo y las dos lecturas de 8x798x, y el nombre que escribiría un cifrado después de G7 en do mayor.**
> 8x798x hace sonar do3 la3 mi4 sol4: el conjunto {do, mi, sol, la}, con do en el bajo. Las lecturas son C6 y Am7, escritas sobre este bajo C6 y Am7/C. Después de G7 en do mayor, el cifrado escribe C6.

**2. ¿Por qué cualquier nota de un acorde de séptima disminuida puede ser su fundamental, y qué indica la fundamental en la música escrita?**
> Sus cuatro notas dividen la octava en cuatro terceras menores, así que el conjunto es el mismo apilamiento de terceras menores desde cada una de ellas. La grafía indica la fundamental, donde empieza el apilamiento de terceras escrito, y la resolución indica la función.

**3. ¿Por qué GA nombra el Asus4 x02230 `Dsus2/A`?**
> Su conjunto {la, re, mi} es exactamente Asus4 y exactamente Dsus2. Los dos patrones tienen prioridad 8, y la puntuación de frecuencia de la fundamental prefiere re (2) a la (3). El bajo, la, no es esa fundamental, así que GA añade `/A`.

**4. En GA en `5c3a52a`, ¿qué contiene un `C6` del reconocedor, y por qué?**
> Do, re, mi, sol y la, novena incluida. GA nombra el conjunto 6/9 por su patrón major-6-add-9, cuyo «add9» no se imprime. El C6 simple, la do mi sol, siempre es Am7.

**Criterio de aprobación:** Distinguir la fundamental, el bajo y el conjunto en cualquier voicing. Enumerar las lecturas de un conjunto, incluidas las simétricas. Elegir una lectura por el bajo, la armonía y la resolución, y escribirla como acorde con barra cuando haga falta. Decir cómo nombra GA un conjunto, y dónde su nombre difiere del de un cifrado.

---

## Base de investigación

- Wikipedia, «Root (chord)»: el método del apilamiento de terceras y la fundamental de un acorde suspendido.
- Wikipedia, «Slash chord»: la barra, que «does not indicate 'or'», el descenso, y los acordes con barra de los arreglistas.
- Wikipedia, «Sixth chord»: C6 como Am7 en primera inversión, y los nombres de do mi♭ sol la.
- Wikipedia, «Suspended chord»: la cuarta que resuelve en la tercera.
- Wikipedia, «Diminished seventh chord»: los tres acordes distintos, la fundamental por la grafía, y la resolución antes que la grafía.
- Wikipedia, «Augmented triad»: A♭+ escrito la♭–do–mi.
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §5 enlaza a su línea.
- Learn, lección 3 de music-theory-ga en el commit `89dc3e64d392cdc36844b03719880484d823b4d7`: cómo nombra una forma su laboratorio.
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia.
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión.
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
