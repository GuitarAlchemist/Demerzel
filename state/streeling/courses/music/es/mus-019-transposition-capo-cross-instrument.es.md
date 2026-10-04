---
module_id: mus-019-transposition-capo-cross-instrument
department: music
course: Transposición, capotraste y equivalencia entre instrumentos
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-009-tuning-fretboard-geometry, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Transposición, capotraste y equivalencia entre instrumentos — Tres clases de identidad

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, podrás:
- Transportar una altura, un acorde, una progresión o una tonalidad n semitonos, y escribir el resultado en su nueva tonalidad
- Hallar la tonalidad que suena con un capotraste y sus formas de acorde, y las formas y el traste del capotraste para una tonalidad que suena
- Decir en qué se convierte una forma de acorde en otro instrumento o en otro grupo de cuerdas
- Escribir la tonalidad de la parte de un instrumento en si♭, en mi♭ o en fa para una tonalidad real, y mantener separados el sonido real y la altura escrita
- Rastrear lo que GA calcula para la transposición y el capotraste, dónde se equivocan sus nombres o su lectura de una pregunta, y qué le falta

---

## 1. Transposición

El artículo «Transposition (music)» de Wikipedia: «transposition refers to the process or operation of moving a collection of notes (pitches or pitch classes) up or down in pitch by a constant interval.» (la transposición designa el proceso u operación de mover un conjunto de notas, alturas o clases de altura, hacia arriba o hacia abajo un intervalo constante.) Para alturas, el intervalo es un número de semitonos: la4, MIDI 69, subido una tercera mayor, 4 semitonos, da MIDI 73, do♯5. Los números de octava son los de la notación científica, como en MUS-007: el do central es do4, MIDI 60 (algunas tradiciones lo llaman do3). Para clases de altura, la suma se toma módulo 12: 9 + 4 = 13 ≡ 1. MUS-020 escribió esta operación Tn: Tn suma n a cada clase de altura, módulo 12.

Una transposición conserva cada intervalo, así que conserva la calidad de cada acorde y su lugar en la tonalidad. T3 lleva la tríada de do mayor {0, 4, 7} a {3, 7, 10}, mi♭ mayor, y lleva la progresión C – Am – F – G, I – vi – IV – V en do mayor, a E♭ – Cm – A♭ – B♭, I – vi – IV – V en mi♭ mayor. Cada acorde de la nueva progresión es la imagen por T3 del anterior.

Solo un desplazamiento de un número fijo de semitonos es un Tn. Wikipedia distingue dos clases de desplazamiento:
- **Transposición cromática.** En ella, «every pitch in a collection of notes is shifted by the same number of semitones. For instance, transposing the pitches C4–E4–G4 upward by four semitones, one obtains the pitches E4–G♯4–B4.» (cada altura de un conjunto de notas se desplaza el mismo número de semitonos. Por ejemplo, al transportar las alturas do4–mi4–sol4 cuatro semitonos hacia arriba, se obtienen mi4–sol♯4–si4.)
- **Transposición diatónica.** Cada altura se mueve el mismo número de grados de una escala: «transposing the pitches C4–E4–G4 up two steps in the familiar C major scale gives the pitches E4–G4–B4» (transportar las alturas do4–mi4–sol4 dos grados hacia arriba en la conocida escala de do mayor da mi4–sol4–si4). La tríada mayor se ha convertido en mi menor. Los grados de una escala no tienen todos el mismo tamaño, así que esto no es un Tn.

Pasar una canción a otra tonalidad es una transposición cromática.

**Los semitonos no fijan el nombre de las notas.** Como mostró MUS-007, una misma clase de altura tiene varios nombres. Una transposición de n semitonos se escribe nombrando su intervalo, con un número y una calidad, y moviendo la tónica ese intervalo. Tres semitonos por encima de do es una tercera menor, do re mi, hasta mi♭; o una segunda aumentada, do re, hasta re♯. Mi♭ mayor tiene tres bemoles; re♯ mayor necesitaría nueve sostenidos, contando cada 𝄪 como dos. Cuando solo se dan los semitonos, la tonalidad con menos alteraciones es el nombre habitual.

La línea de quintas de MUS-007 hace la cuenta. Cada quinta justa ascendente añade un sostenido a la armadura o quita un bemol, así que un intervalo vale un número fijo de quintas:

| Intervalo ascendente | quinta justa | segunda mayor | sexta mayor | tercera mayor | cuarta justa | séptima menor | tercera menor | sexta menor |
|------|------|------|------|------|------|------|------|------|
| Quintas | +1 | +2 | +3 | +4 | −1 | −2 | −3 | −4 |

Transportar do mayor una tercera menor hacia arriba desplaza su armadura −3 lugares: pasa de ninguna alteración a tres bemoles, mi♭ mayor. Sol mayor, un sostenido, subido una segunda mayor, recibe tres sostenidos, la mayor.

### Ejercicio práctico

Transporta G – Em – C – D7 tres semitonos hacia arriba. Nombra la tonalidad y escribe los acordes.

> *Solución:* Tres semitonos hacia arriba es una tercera menor, −3 quintas. Sol mayor tiene un sostenido; un sostenido y tres bemoles dejan dos bemoles: si♭ mayor. Los acordes son B♭ – Gm – E♭ – F7. Escrita como la♯ mayor, la tonalidad necesitaría diez sostenidos.

---

## 2. El capotraste

El artículo «Capo (musical device)» de Wikipedia define el capotraste como «a device a musician uses on the neck of a stringed (typically fretted) instrument to transpose and shorten the playable length of the strings—hence raising the pitch» (un dispositivo que un músico coloca en el mástil de un instrumento de cuerda, normalmente con trastes, para transportar y acortar la longitud útil de las cuerdas, y así subir la altura). Los músicos lo usan «so they can play in a different key using the same fingerings as playing open (i.e., without a capo). In effect, a capo uses a fret of an instrument to create a new nut at a higher note than the instrument's actual nut.» (para tocar en otra tonalidad con las mismas digitaciones que al aire, es decir, sin capotraste. En la práctica, un capotraste usa un traste del instrumento para crear una nueva cejuela, en una nota más alta que la cejuela real del instrumento.)

En el lenguaje de MUS-009, la afinación es un vector t, y una cuerda s en el traste f suena t_s + f. Un capotraste en el traste c hace sonar cada cuerda al aire c semitonos más alto. La nueva afinación es t + (c, c, c, c, c, c), y la diferencia Δ vale c en cada cuerda. Una forma tocada con los trastes f contados desde el capotraste suena t + c + f: cada nota que toca sube c semitonos. El capotraste es T_c aplicado a todo lo que toca el guitarrista. Wikipedia: «Playing with a capo creates the same musical effect as retuning all strings up the same number of steps. However, using a capo only affects the open note of each string.» (tocar con capotraste produce el mismo efecto musical que reafinar todas las cuerdas hacia arriba una misma distancia. Sin embargo, el capotraste solo afecta a la nota al aire de cada cuerda.) Las notas pisadas no cambian: con el capotraste en el traste 3, el traste 7 de la cuerda 6, contando desde la cejuela, sigue sonando si2.

**Dos nombres para un acorde.** Un acorde puede nombrarse por la forma que hacen los dedos o por lo que hace sonar. Wikipedia: «a D-shaped chord can be referred to as "D" (based on the shape relative to the capo), or E (based on the absolute audible chord produced). Neither method strongly prevails over the other.» (un acorde con forma de re puede llamarse D, según la forma respecto al capotraste, o E, según el acorde que realmente se oye. Ninguno de los dos métodos se impone claramente al otro.) Por eso los guitarristas dicen «forma de acorde» cuando hablan de la digitación. Con el capotraste en el traste c:

- sonido = forma + c;
- forma = sonido − c.

La pregunta de esta lección es la de un guitarrista: con un capotraste en el tercer traste y formas de do, ¿en qué tonalidad oye el público la canción, y qué lee un trompetista en si♭ para la misma canción? Con el capotraste en el traste 3, la forma de do x32010 se toca en x65343, contando desde la cejuela. Hace sonar mi♭3 sol3 si♭3 mi♭4 sol4: mi♭ mayor, tres semitonos por encima de do. La progresión C – Am – F – G, tocada en formas, suena E♭ – Cm – A♭ – B♭. Los nombres que suenan se escriben en la tonalidad que suena, por la regla del §1: do subido una tercera menor da mi♭, no re♯.

**Elegir el traste del capotraste.** Para sonar en una tonalidad K con formas abiertas, toma una tonalidad S que tenga acordes abiertos fáciles, do, la, sol, mi o re, y pon el capotraste en el traste K − S, módulo 12. Para mi♭ mayor:

| Formas | re | do | la | sol | mi |
|------|------|------|------|------|------|
| Traste del capotraste | 1 | 3 | 6 | 8 | 11 |

Wikipedia da dos de estas elecciones. En «Guitar», para una canción en si mayor, un guitarrista puede «put a capo on the second fret of the instrument, and then play the song as if it were in the key of A Major» (poner un capotraste en el segundo traste del instrumento y luego tocar la canción como si estuviera en la mayor). En «Capo (musical device)», dos guitarristas tocan I IV V en mi: «the first guitarist plays E A B7 while the second plays the same progression capoed at the fourth fret using C F G7 chord-shapes» (el primer guitarrista toca E A B7 mientras el segundo toca la misma progresión con capotraste en el cuarto traste, en formas C F G7). La segunda guitarra hace sonar los mismos acordes en otros voicings.

La tonalidad que suena toma el nombre con menos alteraciones. Las formas de sol con un capotraste en el traste 4 suenan si mayor, cinco sostenidos, en lugar de do♭ mayor, siete bemoles. Las formas de re en el traste 4 suenan fa♯ mayor o sol♭ mayor, seis alteraciones en ambos casos: un empate, y los dos nombres se usan.

**El capotraste parcial.** Un capotraste parcial cubre solo algunas cuerdas. El ejemplo de Wikipedia cubre «the top five strings of a guitar» (las cinco cuerdas agudas de una guitarra) y deja libre el mi grave: «When played at the second fret, this appears to create a drop D tuning (in which the bass E string is detuned to a D) raised one full tone in pitch.» (colocado en el segundo traste, parece crear una afinación en drop D, en la que la cuerda grave de mi se baja a re, subida un tono entero.) Enumerada desde la cuerda 1, Δ = (2, 2, 2, 2, 2, 0), es decir, un capotraste de un tono, (2, 2, 2, 2, 2, 2), más el (0, 0, 0, 0, 0, −2) del drop D. Las cuerdas al aire suenan mi2 si2 mi3 la3 do♯4 fa♯4 desde la cuerda 6: el drop D, re2 la2 re3 sol3 si3 mi4, dos semitonos más alto.

### Ejercicio práctico

Con un capotraste en el traste 2, un guitarrista toca las formas G – C – D – Em. ¿Qué tonalidad oye el público? Para una canción en la♭ mayor, ¿dónde va el capotraste para formas de sol, y para formas de mi?

> *Solución:* La mayor, dos semitonos por encima de sol: los acordes suenan A – D – E – F♯m. Para la♭ mayor: formas de sol en el traste 1, ya que 7 + 1 = 8, y formas de mi en el traste 4, ya que 4 + 4 = 8.

---

## 3. La misma forma, otro instrumento

Un capotraste cambia cada cuerda en la misma cantidad, así que una forma conserva la calidad de su acorde y se mueve un solo Tn. Otro instrumento se compara con la guitarra del mismo modo, cuerda por cuerda, mediante la diferencia de las dos afinaciones. El curso music-theory-ga de Learn estudia estas comparaciones en su [lección 8](https://github.com/spareilleux/learn/blob/a0c78d95a4719fdc0df85052fe171c78cf204e2b/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx#L99-L161). El artículo «Ukulele» de Wikipedia da las afinaciones:
- **Sol grave.** La afinación lineal C6, «or "low G" tuning, which has the G in sequence an octave lower: G3–C4–E4–A4, which is equivalent to playing the top four strings (DGBE) of a guitar with a capo on the fifth fret.» (o afinación en sol grave, en la que el sol sigue el orden, una octava más abajo: sol3–do4–mi4–la4, lo que equivale a tocar las cuatro cuerdas agudas, re sol si mi, de una guitarra con un capotraste en el quinto traste.)
- **Sol agudo.** La afinación C6 habitual, sol4–do4–mi4–la4: «The G string is tuned an octave higher than might be expected, so this is often called "high G" tuning. This is known as a "reentrant tuning"» (la cuerda de sol se afina una octava más alta de lo que cabría esperar, de ahí el nombre habitual de afinación en sol agudo. Se la conoce como afinación reentrante.)
- **Barítono.** «The baritone ukulele usually uses linear G6 tuning: D3–G3–B3–E4, the same as the highest four strings of a standard 6-string guitar.» (el ukelele barítono suele usar la afinación lineal G6: re3–sol3–si3–mi4, la misma que las cuatro cuerdas más agudas de una guitarra estándar de 6 cuerdas.)

| Instrumento | Cuerdas 4 a 1 | Menos las cuerdas 4 a 1 de la guitarra | La forma de sol de la guitarra en las cuerdas 4 a 1, 0003 |
|------|------|------|------|
| Guitarra | re3 sol3 si3 mi4 | 0, 0, 0, 0 | re3 sol3 si3 sol4: sol mayor |
| Ukelele, sol grave | sol3 do4 mi4 la4 | 5, 5, 5, 5 | sol3 do4 mi4 do5: do mayor, sol en el bajo |
| Ukelele, sol agudo | sol4 do4 mi4 la4 | 17, 5, 5, 5 | sol4 do4 mi4 do5: do mayor, do en el bajo |
| Ukelele barítono | re3 sol3 si3 mi4 | 0, 0, 0, 0 | re3 sol3 si3 sol4: sol mayor |

- **El ukelele en sol grave.** Cada diferencia vale 5, así que el ukelele equivale a las cuatro cuerdas agudas de la guitarra con un capotraste en el traste 5. Cada forma hace sonar T5 de su acorde de guitarra: la forma de sol de la guitarra es el acorde de do del ukelele, y la forma de re de la guitarra, 0232, es su sol.
- **El ukelele en sol agudo.** La diferencia en la cuerda 4 vale 17, una octava y una cuarta. Módulo 12 sigue siendo 5, así que las clases de altura y los nombres de los acordes son los del sol grave. El bajo, no: el mismo acorde de do tiene su quinta en el bajo con sol grave y su fundamental con sol agudo, una segunda inversión frente a un estado fundamental, en los términos de MUS-014.
- **El ukelele barítono.** La diferencia vale 0, así que cada forma conserva su nombre de guitarra.
- **El bajo eléctrico.** El artículo «Bass guitar» de Wikipedia dice que se afina en «pitches one octave lower than the four lowest-pitched strings of a guitar, typically E, A, D, and G» (alturas una octava más bajas que las cuatro cuerdas más graves de una guitarra, normalmente mi, la, re y sol): mi1 la1 re2 sol2 frente a mi2 la2 re3 sol3, una diferencia de −12 en cada cuerda. Eso es T0 en las clases de altura, así que un traste en la cuerda 4 del bajo da la nota que da el mismo traste en la cuerda 6 de la guitarra, una octava más abajo.

**La misma forma en otras cuerdas de una guitarra.** Mover una forma a otro grupo de cuerdas solo conserva su sonido si las cuerdas conservan sus intervalos. Como mostró MUS-009, las cuerdas de la guitarra están a una cuarta entre sí, salvo las cuerdas 3 y 2, a una tercera mayor. La forma fundamental-quinta-octava x355xx hace sonar do3 sol3 do4. Un grupo de cuerdas más arriba, xx355x hace sonar fa3 do4 mi4: la octava se ha convertido en una séptima mayor, y la forma debe pasar a xx356x para dar fa3 do4 fa4.

### Ejercicio práctico

La forma 2210, en las cuerdas 4 a 1, es la parte alta del acorde de la menor de la guitarra. ¿Qué hace sonar en la guitarra, en un ukelele en sol grave y en un ukelele en sol agudo, y qué nota está en el bajo?

> *Solución:* En la guitarra, mi3 la3 do4 mi4: la menor con mi, su quinta, en el bajo. En un ukelele en sol grave, la3 re4 fa4 la4: re menor, cinco semitonos más arriba, con la, su quinta, en el bajo. En un ukelele en sol agudo, la4 re4 fa4 la4: re menor con re4 como la nota más grave, su fundamental.

---

## 4. Instrumentos transpositores

El artículo «Transposing instrument» de Wikipedia: «A transposing instrument is a musical instrument for which music notation is not written at concert pitch (concert pitch is the pitch on a non-transposing instrument such as the piano).» (un instrumento transpositor es un instrumento cuya música no se escribe en sonido real, siendo el sonido real la altura de un instrumento no transpositor como el piano.) Un instrumento se nombra por lo que hace sonar su do escrito: «Playing a written C on clarinet or soprano saxophone produces a concert B♭ (i.e. B♭ at concert pitch), so these are referred to as B♭ instruments.» (tocar un do escrito en un clarinete o un saxofón soprano produce un si♭ real, es decir, un si♭ en sonido real; por eso se les llama instrumentos en si♭.) El instrumento no cambia nada: «The instruments do not transpose the music; rather, their music is written at a transposed pitch. Where chords are indicated for improvisation they are also written in the appropriate transposed form.» (los instrumentos no transportan la música; más bien, su música se escribe a una altura transportada. Cuando se indican acordes para improvisar, también se escriben en la forma transportada que corresponde.)

| Instrumento | Un do escrito suena | Sonido real frente a lo escrito | Para escribir una tonalidad real, subirla una | Mi♭ mayor real se escribe en |
|------|------|------|------|------|
| Trompeta en si♭, clarinete en si♭ | si♭ | un tono más bajo | segunda mayor (+2 quintas) | fa mayor |
| Saxofón alto en mi♭ | mi♭ | una sexta mayor más bajo | sexta mayor (+3 quintas) | do mayor |
| Trompa en fa | fa | una quinta justa más bajo | quinta justa (+1 quinta) | si♭ mayor |
| Guitarra, bajo eléctrico | do, una octava más bajo | una octava más bajo | octava | mi♭ mayor |

Los intervalos del sonido real son los de Wikipedia. «Trumpet»: «The most common type of trumpet is a transposing instrument in B♭, with pitches sounding a whole step lower than written.» (el tipo de trompeta más común es un instrumento transpositor en si♭, cuyas alturas suenan un tono más bajas que lo escrito.) «Alto saxophone»: «The alto saxophone is a transposing instrument, with pitches sounding a major sixth lower than written.» (el saxofón alto es un instrumento transpositor, cuyas alturas suenan una sexta mayor más bajas que lo escrito.) «Transposing instrument» da la trompa «sounding a perfect fifth below written pitch in treble clef» (que suena una quinta justa por debajo de la altura escrita en clave de sol) y señala que «Double bass, bass guitar, guitar, and contrabassoon sound an octave lower than written.» (el contrabajo, el bajo eléctrico, la guitarra y el contrafagot suenan una octava más bajos que lo escrito.) La guitarra es ella misma un instrumento transpositor, a la octava.

Ahora, la segunda mitad de la pregunta. La canción suena en mi♭ mayor: capotraste en el traste 3, formas de do. Su hoja de acordes en sonido real dice E♭ – Cm – A♭ – B♭. Cada parte sube el intervalo de su instrumento, y la tabla de quintas del §1 da la armadura: mi♭ mayor tiene tres bemoles, así que +2 quintas dejan un bemol, fa mayor.

| Parte | Tonalidad escrita | Hoja de acordes |
|------|------|------|
| Sonido real | mi♭ mayor | E♭ – Cm – A♭ – B♭ |
| Trompeta en si♭ | fa mayor | F – Dm – B♭ – C |
| Saxofón alto en mi♭ | do mayor | C – Am – F – G |
| Trompa en fa | si♭ mayor | B♭ – Gm – E♭ – F |
| Guitarra, capotraste en el traste 3, en formas | do mayor | C – Am – F – G |

El saxofonista alto y el guitarrista leen los mismos nombres de acordes. La parte del saxofón se escribe una sexta mayor por encima del sonido, las formas del guitarrista una tercera menor por debajo, y 9 ≡ −3 módulo 12: los dos nombres caen en las mismas clases de altura, en octavas distintas.

Ahora pueden distinguirse las tres clases de identidad:

| Relación | Lo que sigue igual | Lo que cambia | Ejemplo |
|------|------|------|------|
| Transposición Tn | Los intervalos, las calidades de los acordes, los grados de la tonalidad | Cada clase de altura, desplazada n, y los nombres de las notas | C – Am – F – G y E♭ – Cm – A♭ – B♭ |
| Misma forma | La digitación | El sonido, según la diferencia de las afinaciones: un Tn solo cuando es la misma en cada cuerda | La forma de sol: sol en una guitarra, do en un ukelele |
| Misma nota escrita | La notación | El sonido, según la transposición del instrumento | Un do escrito: si♭ en una trompeta, mi♭ en un saxofón alto |

### Ejercicio práctico

Una canción está en si♭ mayor real. ¿En qué tonalidades la leen una trompeta en si♭, un saxofón alto en mi♭ y una trompa en fa? ¿Qué hace sonar un re escrito en la trompeta?

> *Solución:* Si♭ mayor tiene dos bemoles. La parte de la trompeta se desplaza +2 quintas: do mayor. La del saxofón alto se desplaza +3: un sostenido, sol mayor. La de la trompa se desplaza +1: un bemol, fa mayor. Un re escrito suena un tono más bajo en la trompeta: do.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos de abajo se leen en su código en el commit [`e610b77`](https://github.com/GuitarAlchemist/ga/tree/e610b7714b9d6a1fe625b17fe6ca004380ca6752). Esta lección documenta ese código y no lo modifica. No ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA, en `7595983`. Cuando un resultado necesita un cálculo, viene de una transcripción en Python, línea por línea, del código nombrado: leído, no ejecutado.

**Los conjuntos de clases de altura se transportan por rotación.** El `PitchClassSetId` de GA escribe un conjunto como un número de 12 bits, con el bit p activado para la clase de altura p, como en MUS-020. [`Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L82-L88) reduce n módulo 12 y hace girar los bits n lugares hacia arriba, y los bits de arriba vuelven abajo. Do mayor, 145, se convierte en 1160 por T3: {3, 7, 10}, mi♭ mayor. Eso es exactamente Tn. [`Rotate`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L90) llama a `Transpose`, con el comentario «Rotation of PC set is transposition» (la rotación de un conjunto de clases de altura es una transposición). Los dos archivos de prueba que llaman a `PitchClassSetId.Transpose` lo usan para comprobar otro código: que una [forma prima no cambia](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/GA.Domain.Core.Tests/Theory/Atonal/TranspositionClassTests.cs#L69-L82) con ninguna de las 12 transposiciones, y, mediante un [oráculo construido sobre él](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L16-L30), que las formas primas se calculan bien. Un segundo Tn, [`HarmonicTransformationService.Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Services/HarmonicTransformationService.fs#L15-L16), suma n a cada clase de altura de un conjunto, módulo 12. Ningún código fuera de las pruebas lo llama, y [su prueba](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.DSL.Tests/HarmonicTransformationTests.cs#L11-L22) comprueba el valor: {0, 4, 7} subido 2 da {2, 6, 9}.

**Símbolos de acorde: la fundamental se mueve, su grafía y el bajo no la siguen.** [`domain.transposeChord`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L227-L252) analiza un símbolo de acorde y suma n a la clase de altura de su fundamental. Nombra la nueva fundamental con una lista de sostenidos o una lista de bemoles, elegida por la fundamental anterior: según [`preferFlat`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L29-L37), bemoles para una fundamental con bemol o para fa, sostenidos en otro caso, como halló MUS-007. Luego [reemplaza la fundamental y nada más](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L250). Un acorde con bajo indicado conserva su [bajo](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Types/ChordAst.fs#L29), que el renderizador [vuelve a escribir tras la barra](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Generators/ChordRenderer.fs#L35-L38): C/E subido dos semitonos da `D/E`, no D/F♯, y G/B subido tres da `A#/B`, no B♭/D.

La herramienta de línea de comandos de GA transporta una progresión con `ga progression`, que llama a la closure [acorde por acorde](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Apps/GaCli/Program.fs#L239-L245). Leído, no ejecutado, para C Am F G:

| `--by` | GA imprime tras la flecha | Escrito en la tonalidad |
|------|------|------|
| 1 | C# A#m Gb G# | D♭ B♭m G♭ A♭ |
| 3 | D# Cm Ab A# | E♭ Cm A♭ B♭ |
| 8 | G# Fm Db D# | A♭ Fm D♭ E♭ |
| 10 | A# Gm Eb F | B♭ Gm E♭ F |

Los otros siete desplazamientos, de 1 a 11, dan una grafía de su tonalidad. Las clases de altura son correctas en cada fila: cada acorde es la imagen por Tn de aquel del que viene. Los nombres fallan en re♭, mi♭, la♭ y si♭ mayor, porque cada acorde toma el lado de su fundamental anterior: en `--by 1`, C# y G# conviven con Gb en una misma tonalidad.

La única prueba que transporta un acorde mediante la closure, [`EvalClosure_TransposeWithIntCoercion_Succeeds`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.ML.Tests/Unit/DslEvalMcpToolsTests.cs#L188-L205), pide C subido tres semitonos. Comprueba que vuelve un resultado, no cuál es; por transcripción, es `D#`. El `TransposeSkill` del chatbot hace que un modelo de lenguaje llame a [la misma closure](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/TransposeSkill.cs#L22).

El modelo de dominio de GA tiene una tercera transposición, [`ChordProgression.Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L189-L199). Mueve la fundamental de cada acorde, pero construye el nuevo acorde con [su símbolo anterior](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L25-L42), así que un C Am F G transportado sigue [imprimiéndose](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L201) como `C | Am | F | G`. Nada la llama, y ninguna prueba la cubre.

**El skill del capotraste: aritmética correcta, sostenidos por defecto, un lector estrecho.** El chatbot responde a las preguntas de capotraste con [`CapoSkill`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L6-L25): «Zero LLM calls — pure pitch-class arithmetic. Confidence = 1.0.» (cero llamadas a un LLM, aritmética pura de clases de altura; confianza = 1,0.) Su aritmética es la del §2, [sonido = forma + n](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L144) y [forma = sonido − n](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L116), módulo 12. [Nombra el resultado](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L178-L184) con una lista de sostenidos, «Default: sharps (guitarist convention)» (por defecto: sostenidos, convención de los guitarristas), y solo [toma bemoles](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L186-L191) cuando la tonalidad o la forma se escribe con «♭» o con una «b» minúscula, o cuando una pregunta sobre una forma contiene las letras «flat» (bemol) en cualquier parte, incluso dentro de una palabra más larga. Así, «Eb» toma bemoles y «EB» no, aunque las dos se leen como mi♭; un si natural escrito «b» también los toma. Su propio resumen promete [«Eb (C + 3st)»](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L13) para una forma de do con un capotraste en el traste 3; por transcripción, esa pregunta recibe `D#`.

El skill lee una pregunta con [dos expresiones regulares](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L52-L64), [primero la de las formas](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L88-L106). Por transcripción, en los [diez ejemplos de peticiones](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L33-L45) del propio skill:
- **Siete** reciben la respuesta del §2.
- **«I play a C shape with capo 3 — what does it sound like»** (toco una forma de do con capotraste en el traste 3: ¿cómo suena?) recibe la clase de altura correcta, nombrada `D#`.
- **«What's the sounding key if I play in G with capo on 5»** (¿cuál es la tonalidad que suena si toco en sol con capotraste en el traste 5?) se lee como una canción que suena en sol. El skill responde «play a D shape» (toca una forma de re); la pregunta pide do, sol + 5.
- **«What chord shape for B major with capo 4»** (¿qué forma de acorde para si mayor con capotraste en el traste 4?) no coincide con ninguna de las dos expresiones, así que el skill la rechaza. La respuesta es una forma de sol.

La propia pregunta de esta lección, planteada en inglés, «With a capo at the 3rd fret, playing C shapes, what key does the audience hear?», también se rechaza: las dos expresiones quieren «capo», luego como mucho «on», «at» o «fret», y luego un número, como en «capo 3» o «capo at 3», y la de las formas quiere la palabra «shape», no «shapes». Una tonalidad escrita con «#» o «♭» puede perder su signo: la expresión quiere un límite de palabra justo después de la tonalidad, o después de un «major» o un «minor» que la siga, y no lo hay entre «#» y una coma o un espacio. «Song is in F#, capo 2» (la canción está en fa♯, capotraste en el traste 2) se lee como una canción en fa, y el skill responde «play a D# shape» (toca una forma de re♯) cuando la respuesta es una forma de mi. «Song is in F# major, capo 2» (la canción está en fa♯ mayor, capotraste en el traste 2) recibe la forma de mi. Las pruebas del skill, en [`SkillDeclineTests`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.ML.Tests/Unit/SkillDeclineTests.cs#L17-L33), comprueban que un mensaje sin relación se rechaza y que capo 25 recibe un error en lugar de un rechazo. La transcripción coincide con ambas, y ninguna prueba comprueba una respuesta. El corpus de evaluación del chatbot [omite su única petición de capotraste](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Apps/GaChatbot.Api.Tests/Corpus/prompts.yaml#L534-L537), «Transpose this progression to capo 3» (transporta esta progresión con capotraste en el traste 3), hasta que exista una herramienta de progresiones. El backlog de GA [marca esa herramienta como no hecha](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/BACKLOG.md#L196).

**Voicings, otros instrumentos y lo que falta.**
- **Documentos de voicing.** La fábrica de documentos de voicing de GA recibe un [argumento `capo`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L16). Solo lo usa en el [identificador](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L29) del documento, y ningún llamador pasa uno.
- **El catálogo de instrumentos.** Escribe el bajo eléctrico como [E1 A1 D2 G2](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L157) y la afinación en do del ukelele como [G4 C4 E4 A4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1113), ambas como en el §3. La lección 8 de Learn compiló un GA anterior, `a826864`, y [leyó este catálogo](https://github.com/spareilleux/learn/blob/a0c78d95a4719fdc0df85052fe171c78cf204e2b/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx#L186-L225). Encontró la línea del ukelele precedida de un `C6` suelto, que ha desaparecido en `e610b77`. También encontró dos líneas de ukelele barítono, que no han cambiado: [D4 G3 B4 E4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1120) y [D4 G3 B3 E4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1434), donde el §3 tiene re3 sol3 si3 mi4. Las dos tienen las clases de altura de la guitarra, así que un código que compara clases de altura no puede ver la diferencia.
- **Instrumentos transpositores.** No están. En `e610b77`, nada en el repositorio de GA dice «transposing instrument» ni «written pitch», y «concert pitch» aparece una sola vez, en el [registro de una afinación de guitarra de 8 cuerdas](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/SpecializedTunings.yaml#L243). En los archivos C#, F#, TypeScript, JavaScript, Python y YAML de GA, las palabras «saxophone» y «clarinet» aparecen una sola vez, en una línea que pone un instrumento cuyo nombre las contiene, o contiene «flute», en la [familia «Wind»](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/GA.Data.MongoDB/Services/InstrumentService.cs#L120). El §4 se enseña como teoría.

Corregir todo esto corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

Por transcripción, ¿qué responde `CapoSkill` a «I play an F shape with capo 1, what does it sound like» (forma de fa, capotraste en el traste 1) y a «I play a D shape with capo 1, what does it sound like» (forma de re, capotraste en el traste 1)? ¿Son correctos los nombres?

> *Solución:* «F#» y «D#». El primero es correcto: fa♯ mayor y sol♭ mayor tienen seis alteraciones cada una. El segundo, no: la tonalidad es mi♭ mayor, tres bemoles, mientras que re♯ mayor necesitaría nueve sostenidos. Ninguna de las dos preguntas contiene un bemol, así que el skill usa su lista de sostenidos las dos veces.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA. La versión de GA fijada en el laboratorio pasaría primero a `e610b77`. Nada en esta sección es una medición:
- las predicciones vienen del §5 y se escriben antes de cualquier ejecución;
- vienen de una transcripción en Python, línea por línea, de `PitchClassSetId.Transpose`, de `domain.transposeChord` con el analizador y el renderizador de acordes, y de `CapoSkill`;
- una versión posterior de esta lección informará de los resultados.

Cada paso llama al código de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Cada conjunto, cada n.** Para cada `PitchClassSetId` de 0 a 4095 y cada n de 0 a 11, comparar `Transpose(n)` con el conjunto de las clases de altura p + n módulo 12, y comprobar que `Transpose(12 − n)` devuelve el conjunto. Predicción: los 49 152 pares pasan las dos comprobaciones; 145 da 1160 para n = 3.
2. **Una progresión, cada n.** Mediante el registro de closures de GA, invocar `domain.transposeChord` sobre C, Am, F y G para cada n de 1 a 11, y sobre C/E con n = 2 y G/B con n = 3. Analizar cada acorde transportado de la progresión con `Chord.FromSymbol` y comparar sus clases de altura con las del original desplazadas n. Predicción: los nombres de la tabla del §5, con re♭, mi♭, la♭ y si♭ mayor mal escritos y los otros siete desplazamientos correctos; cada conjunto de clases de altura una imagen por Tn; `D/E` y `A#/B`.
3. **El skill del capotraste.** Llamar a `CapoSkill.ExecuteAsync` sobre sus diez ejemplos de peticiones y sobre la pregunta de esta lección, y anotar `Declined` y la primera línea de `Result`. Predicción: como en el §5. Siete respuestas coinciden con el §2, la forma de do con un capotraste en el traste 3 suena `D#`, «play in G with capo on 5» recibe una forma de re, y la petición sobre si mayor y la pregunta de esta lección se rechazan.

### Ejercicio práctico

El paso 2 predice `Ab` para F subido tres semitonos y `D#` para C. ¿Por qué F recibe un bemol y C un sostenido, y qué deberían ser los dos?

> *Solución:* `preferFlat` da la lista de bemoles a una fundamental con bemol y a fa, la única fundamental natural cuya tonalidad mayor tiene un bemol, si♭; C recibe la lista de sostenidos. Los dos acordes llegan a mi♭ mayor, donde deberían ser A♭ y E♭: es la nueva tonalidad la que debería elegir el lado, no la fundamental anterior.

---

## 7. Errores comunes

- **Escribir una transposición solo por sus semitonos.** Tres semitonos por encima de do, en un cambio de tonalidad, es mi♭, una tercera menor, no re♯.
- **Tomar un desplazamiento diatónico por una transposición.** Do mi sol subido dos grados de do mayor da mi sol si, una tríada menor: no es un Tn.
- **Nombrar un acorde sin decir qué nombre.** Con un capotraste en el traste 2, un «re» puede ser la forma o el sonido: di «forma de re» o «suena mi».
- **Mover las notas pisadas con el capotraste.** El capotraste solo sube las cuerdas al aire; el traste 7 de la cuerda 6 es si2 con o sin capotraste en un traste inferior.
- **Esperar que una forma conserve su acorde en cada instrumento.** En un ukelele en sol grave suena una cuarta más alta; en una misma guitarra, una forma que pasa de un lado a otro de las cuerdas 3 y 2 cambia.
- **Leer la parte de un instrumento transpositor en sonido real.** Un do escrito en una trompeta en si♭ suena si♭.
- **Fiarse de los nombres de GA para un acorde transportado.** `domain.transposeChord` nombra la nueva fundamental con sostenidos salvo que la anterior tenga bemol o sea fa, y `CapoSkill` salvo que la pregunta cumpla una de las condiciones del §5 para los bemoles; `domain.transposeChord` también deja el bajo de un acorde con bajo indicado donde estaba.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Transposición, Tn** | Sumar n semitonos a cada altura, o n módulo 12 a cada clase de altura |
| **Transposición cromática y diatónica** | Un desplazamiento de un número fijo de semitonos, o de un número fijo de grados de una escala |
| **Capotraste** | Una pinza que se coloca a lo ancho de las cuerdas en un traste, una nueva cejuela: cada cuerda al aire sube el mismo número de semitonos |
| **Forma de acorde** | Un acorde nombrado por su digitación respecto al capotraste, no por lo que hace sonar |
| **Sonido real** | La altura que suena, que un instrumento no transpositor como el piano escribe tal cual |
| **Instrumento transpositor** | Un instrumento cuya parte se escribe a otra altura que la que suena: la trompeta en si♭, el saxofón alto en mi♭, la trompa en fa, y la guitarra y el bajo eléctrico a la octava |
| **Afinación reentrante** | Una afinación cuyas cuerdas no están en orden de altura, como el sol agudo del ukelele |

---

## Autoevaluación

**1. Un guitarrista toca las formas G – Em – C – D con un capotraste en el traste 3. ¿Qué oye el público, y en qué tonalidad?**
> B♭ – Gm – E♭ – F, en si♭ mayor. Cada acorde sube una tercera menor, y si♭ mayor tiene dos bemoles donde la♯ mayor necesitaría diez sostenidos.

**2. Una canción suena en la mayor. Da dos posiciones de capotraste con formas abiertas.**
> Formas de sol en el traste 2, ya que 7 + 2 = 9, o formas de mi en el traste 5, ya que 4 + 5 = 9. Las formas de re en el traste 7 y las de do en el traste 9 también sirven.

**3. La canción de la pregunta 2 tiene una trompeta en si♭ y un saxofón alto en mi♭. ¿En qué tonalidades leen?**
> La mayor tiene tres sostenidos. La parte de la trompeta se desplaza +2 quintas, hasta cinco sostenidos: si mayor. La del saxofón alto se desplaza +3, hasta seis sostenidos: fa♯ mayor.

**4. Por transcripción, ¿qué devuelve `domain.transposeChord` de GA para C/E subido dos semitonos, y qué debería devolver?**
> `D/E`: solo se mueve la fundamental. Debería devolver D/F♯.

**5. ¿Por qué una forma de guitarra suena una cuarta más alta en un ukelele en sol grave, e igual en un ukelele barítono?**
> Las cuerdas del ukelele en sol grave, sol3 do4 mi4 la4, son las cuatro cuerdas agudas de la guitarra, re3 sol3 si3 mi4, subidas cinco semitonos cada una: la misma diferencia en cada cuerda, como un capotraste en el traste 5. Las cuerdas del barítono son exactamente esas cuatro cuerdas, una diferencia de 0.

**Criterio de aprobación:** Transportar una altura, un acorde, una progresión o una tonalidad, y escribir el resultado en su tonalidad. Pasar del capotraste y las formas a la tonalidad que suena, y al revés. Decir en qué se convierte una forma en otro instrumento o en otro grupo de cuerdas. Escribir la tonalidad de una parte en si♭, en mi♭ o en fa para una tonalidad real. Decir dónde aciertan las respuestas de GA sobre la transposición y el capotraste, y dónde fallan sus nombres o su lectura de una pregunta.

---

## Base de investigación

- Wikipedia, «Transposition (music)»: la definición, Tn sobre las clases de altura, la transposición de alturas y de clases de altura, y la transposición cromática frente a la diatónica.
- Wikipedia, «Capo (musical device)»: la nueva cejuela, el mismo efecto que reafinar cada cuerda, el nombre de la forma frente al nombre que suena, el ejemplo E A B7 y C F G7, y el capotraste parcial.
- Wikipedia, «Guitar»: el capotraste en el segundo traste para si mayor con formas de la.
- Wikipedia, «Ukulele»: las afinaciones C6 con sol agudo y con sol grave, el sol grave como las cuatro cuerdas agudas de una guitarra con un capotraste en el quinto traste, y el re3–sol3–si3–mi4 del barítono.
- Wikipedia, «Bass guitar»: afinado una octava por debajo de las cuatro cuerdas más graves de la guitarra.
- Wikipedia, «Transposing instrument»: la definición, los instrumentos en si♭, los símbolos de acorde transportados, la trompa en fa, y la guitarra y el bajo eléctrico a la octava.
- Wikipedia, «Trumpet» y «Alto saxophone»: un tono y una sexta mayor por debajo de lo escrito.
- Código fuente de GA en el commit `e610b7714b9d6a1fe625b17fe6ca004380ca6752`: cada hecho de código del §5 enlaza a su línea.
- Learn, lección 8 de music-theory-ga en el commit `a0c78d95a4719fdc0df85052fe171c78cf204e2b`: las comparaciones del ukelele y del bajo, y su lectura del catálogo de GA en `a826864`.
- Citado por el plan de currículo de Streeling y no consultado para esta versión: Adler, *The Study of Orchestration* (cuarta edición), el capítulo sobre los instrumentos transpositores.
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia.
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión.
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
