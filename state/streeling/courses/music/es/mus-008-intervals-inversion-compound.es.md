---
module_id: mus-008-intervals-inversion-compound
department: music
course: Intervalos, inversión e intervalos compuestos
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-007-pitch-spelling-enharmonic-identity]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Intervalos, inversión e intervalos compuestos — Contar más allá de la octava

> **Departamento de Música** | Etapa: Nigredo (Principiante) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, podrás:
- Nombrar un intervalo por su número, contado sobre los nombres de nota, y por su calidad, medida en semitonos: justa, mayor, menor, aumentada o disminuida
- Invertir un intervalo simple, y explicar por qué los números de un intervalo y de su inversión suman 9 y sus semitonos 12
- Nombrar un intervalo compuesto como una novena mayor o una undécima justa, dar sus semitonos, y reducirlo a su forma simple
- Nombrar el intervalo entre dos notas pisadas en el mástil a más de una octava de distancia, a partir de sus nombres y de sus números de octava
- Localizar dónde GA calcula correctamente los intervalos simples, y dónde sus intervalos compuestos mezclan dos numeraciones

---

## 1. Número y calidad

Un intervalo tiene dos partes. Su **número** cuenta los nombres de nota, incluidos los dos extremos: de do a mi se pasa por do, re y mi, así que es una tercera, sean cuales sean las alteraciones de las dos notas. Su **calidad** viene de los semitonos que abarca.

La referencia es la escala mayor construida sobre la nota inferior. Por encima de do, da:

| Número | Nombre | Nota por encima de do | Semitonos | Calidad en la escala mayor |
|---|---|---|---|---|
| 1 | Unísono | do | 0 | Justa |
| 2 | Segunda | re | 2 | Mayor |
| 3 | Tercera | mi | 4 | Mayor |
| 4 | Cuarta | fa | 5 | Justa |
| 5 | Quinta | sol | 7 | Justa |
| 6 | Sexta | la | 9 | Mayor |
| 7 | Séptima | si | 11 | Mayor |
| 8 | Octava | do | 12 | Justa |

El unísono, la cuarta, la quinta y la octava son números **justos**; la segunda, la tercera, la sexta y la séptima son números **imperfectos**. Para un número justo, el intervalo es justo en el tamaño de referencia, aumentado (A) un semitono por encima y disminuido (d) un semitono por debajo. Para un número imperfecto, es mayor (M) en el tamaño de referencia y menor (m) un semitono por debajo; es aumentado un semitono por encima del mayor, y disminuido un semitono por debajo del menor. Doblemente aumentado y doblemente disminuido van un semitono más allá. No hay quinta mayor ni tercera justa: cada número solo tiene su propia familia de calidades. Contados con todas las calidades, de doblemente disminuido a doblemente aumentado, el rango que usa GA, los ocho números dan 44 intervalos simples, 5 por cada número justo y 6 por cada número imperfecto. Algunos son solo teóricos, como el unísono disminuido, cuya nota superior sonaría por debajo de la inferior. Las abreviaturas son las del inglés, que imprime GA: P (perfect) para justo, M para mayor, m para menor, A para aumentado y d para disminuido.

Dos intervalos con los mismos semitonos pueden tener nombres distintos. De do a fa♯ y de do a sol♭ hay 6 semitonos: el primero abarca cuatro nombres y es una cuarta aumentada, A4; el segundo abarca cinco y es una quinta disminuida, d5. MUS-007 dejó abierta una pareja de este tipo: de re♭ a fa y de do♯ a fa hay cuatro semitonos. De re♭ a fa se abarcan tres nombres, y cuatro semitonos es el tamaño de referencia de una tercera: es una tercera mayor. De do♯ a fa se abarcan cuatro nombres, y cuatro semitonos es uno menos que una cuarta justa: es una cuarta disminuida.

### Ejercicio práctico

Nombra los intervalos mi–si♭ y la–do♯.

> *Solución:* De mi a si♭ se abarcan cinco nombres, mi fa sol la si, y 6 semitonos, uno menos que una quinta justa: una quinta disminuida, d5. De la a do♯ se abarcan tres nombres y 4 semitonos, el tamaño de referencia de una tercera: una tercera mayor, M3.

---

## 2. Inversión

Para **invertir** un intervalo, se sube su nota inferior una octava, o se baja su nota superior una octava. De do a mi por encima, una tercera mayor, pasa a ser de mi a do por encima, una sexta menor.

Dos sumas se mantienen fijas. Los números suman 9, no 8, porque la nota que se queda en su sitio se cuenta en los dos intervalos: una tercera y una sexta, 3 + 6 = 9. Los semitonos suman 12, una octava: 4 + 8 = 12. La calidad cambia dentro de su familia: mayor pasa a menor y menor a mayor, aumentado pasa a disminuido y disminuido a aumentado, las calidades doblemente alteradas se intercambian de la misma manera, y justo sigue siendo justo. Los números justos se invierten entre sí, 1 y 8, 4 y 5, y lo mismo los imperfectos, 2 y 7, 3 y 6. En los 44 intervalos simples, las dos sumas valen siempre 9 y 12.

| Intervalo | Semitonos | Inversión | Semitonos |
|---|---|---|---|
| M3 | 4 | m6 | 8 |
| m2 | 1 | M7 | 11 |
| P4 | 5 | P5 | 7 |
| A4 | 6 | d5 | 6 |

La cuarta aumentada y la quinta disminuida son la inversión la una de la otra, y ambas abarcan 6 semitonos, media octava: el **tritono**.

### Ejercicio práctico

Invierte una séptima menor y una segunda aumentada.

> *Solución:* Una séptima menor, 10 semitonos, se invierte en una segunda mayor, 2 semitonos: 7 + 2 = 9 y 10 + 2 = 12. Una segunda aumentada, 3 semitonos, se invierte en una séptima disminuida, 9 semitonos.

---

## 3. Intervalos compuestos

Un intervalo cuyo número es mayor que 8 es **compuesto**: abarca más de una octava de nombres. Si añades una octava a un intervalo simple, su número crece en 7, no en 8, por la misma razón que en el §2: la nota superior de la octava se cuenta dos veces, como último nombre de la octava y como primero del intervalo de encima. Una segunda por encima de una octava es una novena, 8 + 2 − 1, y una tercera por encima de una octava una décima. Los semitonos crecen en 12, y la calidad no cambia. Para hallar la **forma simple** de un intervalo compuesto, resta 7 al número y 12 a los semitonos.

| Número compuesto | Forma simple | Semitonos, mayor o justo |
|---|---|---|
| 9 | 2 | 14 |
| 10 | 3 | 16 |
| 11 | 4 | 17 |
| 12 | 5 | 19 |
| 13 | 6 | 21 |
| 14 | 7 | 23 |
| 15 | 8 | 24 |

La undécima, la duodécima y la decimoquinta son justas, como la cuarta, la quinta y la octava de las que vienen; las demás son mayores o menores. La decimoquinta abarca dos octavas, 15 = 8 + 8 − 1, y también se llama **doble octava**.

Los cifrados de acordes nombran las notas apiladas por encima de la séptima con números compuestos: el 9 de C9 es re, el segundo grado de do mayor una octava más arriba, y el 11 y el 13 de C11 y C13 son fa y la. En un voicing la nota puede sonar en cualquier octava; el número nombra su grado por encima de la fundamental.

### Ejercicio práctico

Da la forma simple de una décima mayor y de una duodécima justa, y los semitonos de una novena menor.

> *Solución:* Una décima mayor, 16 semitonos, se reduce a una tercera mayor, 4 semitonos; una duodécima justa, 19, a una quinta justa, 7. Una novena menor abarca 13 semitonos: una segunda menor, 1, más una octava.

---

## 4. En el mástil

En una guitarra con afinación estándar, las cuerdas al aire son mi2, la2, re3, sol3, si3 y mi4, MIDI 40, 45, 50, 55, 59 y 64, y cada traste añade un semitono, como comprueba la [lección 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) de Learn. Los números de octava son los de la notación científica, como en MUS-007: el do central es do4 (algunas tradiciones lo llaman do3). Una forma de acorde abarca a menudo más de una octava. En x32033, un acorde de do con novena añadida, Cadd9, la quinta cuerda en el traste 3 da do3, MIDI 48, y la segunda cuerda en el traste 3 da re4, MIDI 62.

Dos restas nombran el intervalo. Los semitonos son la diferencia de los números MIDI: 62 − 48 = 14. El número cuenta los nombres de una octava a otra: con los nombres numerados de do = 0 a si = 6, vale 7 × (diferencia de los números de octava) + (diferencia de los nombres) + 1. De do3 a re4 da 7 × 1 + 1 + 1 = 9. Una novena es mayor con 14 semitonos, una segunda mayor más una octava, así que de do3 a re4 hay una novena mayor: la novena añadida que da nombre al acorde.

| Forma | Nota inferior | Nota superior | Semitonos | Intervalo |
|---|---|---|---|---|
| Cadd9, x32033 | do3, cuerda 5, traste 3 | re4, cuerda 2, traste 3 | 14 | M9 |
| Cadd9, x32033 | do3, cuerda 5, traste 3 | sol4, cuerda 1, traste 3 | 19 | P12 |
| E, 022100 | mi2, cuerda 6, al aire | sol♯3, cuerda 3, traste 1 | 16 | M10 |
| Asus4, x02230 | la2, cuerda 5, al aire | re4, cuerda 2, traste 3 | 17 | P11 |

La forma abierta de mi pone su tercera, sol♯3, una décima por encima del bajo, y la cuarta suspendida de Asus4, re4, suena una undécima por encima de su bajo. Reducir cada uno de estos intervalos a su forma simple da el nombre de la nota en el acorde: la tercera, la cuarta, y para Cadd9 la segunda y la quinta.

### Ejercicio práctico

En la forma abierta de sol 320003, nombra los intervalos desde el sol grave, cuerda 6 traste 3, hasta la cuerda de si al aire y hasta el sol agudo, cuerda 1 traste 3.

> *Solución:* El sol grave es sol2, MIDI 43. La cuerda de si al aire es si3, MIDI 59: 16 semitonos, y 7 × 1 + (6 − 4) + 1 = 10, una décima mayor. El sol agudo es sol4, MIDI 67: 24 semitonos, y 7 × 2 + 0 + 1 = 15, una decimoquinta justa, una doble octava.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); esta lección documenta ese código sin modificarlo, y no ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA en `8fe33f8`. La [lección 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) de music-theory-ga, en Learn, compila una versión anterior de GA, `a826864`, y comprueba sus intervalos simples. Los demás números de abajo vienen de una transcripción en Python, línea por línea, del código de GA nombrado.

**`Interval.Simple` es correcto.** [`Interval.Simple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L28) calcula sus semitonos como el [tamaño de referencia](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L85) de su número más la [alteración de su calidad](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L127), con una tabla para los números justos y otra para los imperfectos, como en el §1. [`ToInverse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L43) toma [9 menos el número](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L136) y [cambia el signo de la calidad](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L115), cuyos valores van de −3 para doblemente disminuido a 3 para doblemente aumentado: mayor y menor se intercambian, y lo mismo aumentado y disminuido. Según la transcripción, los 44 intervalos simples reciben los semitonos del §1, y cada uno se invierte como en el §2, con sumas de 9 y 12. La lección 1 de Learn comprueba [ocho intervalos](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L27) nombrados por [`GetInterval`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L104) a partir de dos nombres de nota, de do–mi a mi–do, y la inversión de [M3 en m6](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L37). `NoteExtensions.cs` e `IntervalQuality.cs` no han cambiado desde `a826864`, ni tampoco la tabla de semitonos y `ToInverse` de `SimpleIntervalSize`, así que esas comprobaciones siguen valiendo en `5c3a52a`. `GetInterval` recibe notas sin octava, así que siempre devuelve un intervalo simple: de do3 y re4 solo ve do y re, una segunda mayor. Además [reduce los semitonos módulo 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L110) y recurre a [justo](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L42) o [mayor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L55) cuando la diferencia sale de su tabla: de do a si♯, una séptima aumentada de 12 semitonos, devuelve M7.

Queda un hueco en la lectura de nombres. [`Interval.Simple.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L77) acepta cualquier letra de calidad delante de cualquier número, de modo que «M5» se lee como una quinta mayor, que el §1 excluye. Al pedirle sus semitonos, ese intervalo lanza una `InvalidOperationException` desde la [tabla de alteraciones de los intervalos justos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L142).

**Los intervalos compuestos mezclan dos numeraciones.** [`CompoundIntervalSize`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L15) contiene los números del 9 al 16 y los llama Ninth a Fifteenth, y luego [DoubleOctave](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L188) para el 16. Sus partes no se ponen de acuerdo sobre lo que significa un número:

- Su [tabla de semitonos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L145) da 9 → 12, 10 → 14, 11 → 16, 12 → 17, 13 → 19, 14 → 21, 15 → 23 y 16 → 24. Es la tabla del §3 desplazada un número hacia arriba: cada número recibe los semitonos del número de debajo, 12, una octava, para una novena, y 24, una doble octava, para el 16.
- [`ToSimple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L47) resta 8, en la misma numeración desplazada: una novena se reduce a 1, un unísono, y no a una segunda.
- [`SimpleIntervalSize.ToCompound`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L125) suma 7, como el §3. Un viaje de ida y vuelta por `ToCompound` y `ToSimple` devuelve, por tanto, el número de debajo del de partida, de una segunda, pasando por 9, a 1, hasta una octava, pasando por 15, a 7. El `ToCompound` de un unísono valdría 8, fuera de rango, y lanza una `ArgumentOutOfRangeException`.
- Su [consonancia](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L129) declara justos el 11, el 12 y el 16: el 11 y el 12 como en el §3, y luego el 16 donde el §3 tiene el 15.
- Su resumen dice de los números que están [«Between 9 and 16 semitones»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L4) y da el ejemplo [«9 = Octave + Second (9 semitones)»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L12). Nueve cuenta nombres de nota; una novena menor o mayor abarca 13 o 14 semitonos.

[`Interval.Compound`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L31) suma la alteración de su calidad a esa tabla. Según la transcripción, su M9 abarca por tanto 12 semitonos, m9 11, M10 14, P11 16, P12 17 y M13 19: un semitono menos para la undécima, dos para los demás. De sus 11 intervalos con nombre, de m9 a [P15](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L132), solo P15 sale bien, con 24 semitonos, porque está construido sobre el tamaño 16, y por eso se imprime «P16». Leer «P15» da el tamaño 15, que la consonancia declara imperfecto, y ese intervalo lanza una `InvalidOperationException` cuando se le piden sus semitonos. Construidos por `ToCompound` a partir de los 44 intervalos simples del §1, ningún intervalo compuesto recibe los semitonos de los manuales: 38 se quedan cortos en uno o dos, los 5 unísonos lanzan una excepción en `ToCompound`, y el compuesto de P8 lanza una cuando se le piden sus semitonos. Los valores correctos también están en GA: su tipo [`Semitones`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Semitones.cs#L36) define MajorNinth como 14, PerfectEleventh como 17 y MajorThirteenth como 21.

**Quién lee estos valores.** [`ScaleModeCompoundInterval.ToSimple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/ScaleModeCompoundInterval.cs#L15) es el único llamador de `ToSimple`, y ningún código de GA lo llama. `ScaleMode` construye un [intervalo compuesto](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L207) para cada número par de un modo, 2, 4 y 6, en su propiedad `SimpleAndCompoundIntervals`, que ningún código de GA nombra. La [sincronización de intervalos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GA.Data.MongoDB/Services/DocumentServices/IntervalSyncService.cs#L34) de GA con MongoDB guarda cada tamaño compuesto con los semitonos de la tabla, 12 para el 9. Las pruebas de GA leen nombres compuestos, como «b9» en [m9](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/IntervalTests.cs#L181), comprueban que «13» [no se lee como una tercera](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Primitives/IntervalParsingTests.cs#L53), y comprueban que el `ToCompound` de una cuarta vale [11](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Core.Tests/Collections/ValueObjectMemoizationTests.cs#L175). Ninguna prueba le pide sus semitonos a un intervalo compuesto, y ninguna llama a `ToSimple`.

Corregir cualquiera de estas cosas corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

Según la transcripción, `Interval.Compound.P11` de GA abarca 16 semitonos. ¿Qué intervalo del §4 abarca 16 semitonos, y cuántos debería abarcar P11?

> *Solución:* La décima mayor de mi2 a sol♯3. Una undécima justa abarca 17: una cuarta justa, 5, más una octava. GA lee el tamaño 11 en una tabla desplazada un número hacia arriba, donde el 16 pertenece a la décima.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA; la versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`. Nada en ella es una medición. Las predicciones vienen de la transcripción del §5 y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Intervalos simples.** Construye los 44 intervalos simples del §1 y lee sus semitonos. Predicción: los 44 coinciden con el §1.
2. **Inversión.** Invierte cada uno de ellos con `ToInverse`. Predicción: en los 44 casos los números suman 9 y los semitonos 12.
3. **Ida y vuelta.** Para cada uno de los 8 tamaños simples, llama a `ToCompound` y luego a `ToSimple`. Predicción: el unísono lanza una `ArgumentOutOfRangeException`, y los 7 restantes vuelven un número más abajo, la octava como séptima.
4. **Intervalos compuestos con nombre.** Lee los semitonos de los 11 intervalos compuestos con nombre, de m9 a P15. Predicción: 10 difieren del §3; solo P15, impreso «P16», tiene sus 24.
5. **Compuestos a partir de simples.** Llama a `ToCompound` sobre los 44 intervalos simples y compara los semitonos de cada resultado con los del intervalo simple más 12. Predicción: ninguno coincide; 38 se quedan cortos en uno o dos, 5 lanzan una excepción en `ToCompound`, y el compuesto de P8 lanza una cuando se le piden sus semitonos.
6. **Lectura.** Lee «P15», «15» y «M5» con `Interval.Diatonic.Parse`, que prueba primero un intervalo simple y luego uno compuesto. Predicción: los tres se leen; «15» da M15, 23 semitonos, y los otros dos lanzan una `InvalidOperationException` cuando se les piden sus semitonos.

### Ejercicio práctico

El paso 3 predice que un viaje de ida y vuelta desde una tercera devuelve una segunda. ¿Qué cambio en `ToSimple` haría que los 7 viajes volvieran a su punto de partida, y qué otras partes de `CompoundIntervalSize` contradiría entonces?

> *Solución:* `ToSimple` restaría 7, la inversa de `ToCompound`. El resto del tipo seguiría la numeración desplazada. La tabla de semitonos tendría que bajar un número, a 9 → 14 hasta 15 → 24, y los tamaños justos tendrían que pasar a ser 11, 12 y 15. El tamaño 16, que `ToSimple` enviaría ahora al 9, fuera del rango simple, tendría que desaparecer, y `DoubleOctave` y el `P15` construido sobre él pasar al 15.

---

## 7. Errores comunes

- **Contar semitonos como número.** De do a mi hay cuatro semitonos, pero tres nombres: es una tercera.
- **Nombrar un intervalo solo por sus semitonos.** Do–fa♯ y do–sol♭ abarcan ambos 6 semitonos; el primero es A4, el segundo d5.
- **Quintas mayores y terceras justas.** Los 1, 4, 5 y 8 son justos, aumentados o disminuidos; los 2, 3, 6 y 7 son mayores, menores, aumentados o disminuidos.
- **Inversiones que suman 8.** Los números de un intervalo y de su inversión suman 9.
- **Sumar 8 por una octava.** Una segunda más una octava es una novena, y dos octavas forman una decimoquinta.
- **Olvidar la octava de un intervalo compuesto.** En Cadd9, re4 está 14 semitonos por encima de do3, no 2.
- **Leer un tamaño compuesto en la tabla de GA.** En `5c3a52a`, `CompoundIntervalSize` cuenta 12 semitonos para una novena, donde `Semitones.MajorNinth` cuenta 14.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Número de un intervalo** | La cantidad de nombres de nota que abarca un intervalo, incluidos los dos extremos: de do a mi es una tercera |
| **Calidad** | Justa, mayor, menor, aumentada o disminuida, fijada por los semitonos respecto de la escala mayor de la nota inferior |
| **Número justo** | El unísono, la cuarta, la quinta y la octava, y sus compuestos: justos, aumentados o disminuidos |
| **Número imperfecto** | La segunda, la tercera, la sexta y la séptima, y sus compuestos: mayores, menores, aumentados o disminuidos |
| **Inversión** | El intervalo que queda cuando la nota inferior sube una octava; los números suman 9 y los semitonos 12 |
| **Intervalo compuesto** | Un intervalo cuyo número es mayor que 8: 7 más en número y 12 más en semitonos que su forma simple |
| **Tritono** | Un intervalo de 6 semitonos: la cuarta aumentada o la quinta disminuida |

---

## Autoevaluación

**1. Da la inversión de una tercera mayor, con las dos sumas.**
> Una sexta menor: 3 + 6 = 9, y 4 + 8 = 12 semitonos.

**2. ¿Cuál es la forma simple de una décima mayor?**
> Una tercera mayor: 10 − 7 = 3, y 16 − 12 = 4 semitonos.

**3. En una guitarra con afinación estándar, ¿cuántos semitonos separan la quinta cuerda al aire de la segunda cuerda en el traste 3, y cuál es el intervalo?**
> La2 vale MIDI 45 y re4 62: 17 semitonos, una undécima justa, la cuarta de Asus4 por encima de su bajo.

**4. Según la transcripción, [`Interval.Compound.M9`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L123) de GA abarca 12 semitonos. ¿Cuántos debería abarcar, y de dónde sale 12?**
> 14: una segunda mayor, 2, más una octava. La tabla de [`CompoundIntervalSize`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L145) da a cada número los semitonos del número de debajo, y 12 es el de la octava.

**Criterio de aprobación:** Nombrar cualquier intervalo simple o compuesto a partir de sus nombres de nota y sus semitonos; invertir un intervalo simple, con sumas de 9 y 12; reducir un intervalo compuesto a su forma simple; nombrar el intervalo entre dos notas pisadas en el mástil a partir de sus números de octava; y distinguir los intervalos simples correctos de GA de su tabla compuesta desplazada.

---

## Base de investigación

- E. Aldwell, C. Schachter y A. Cadwallader, *Harmony and Voice Leading*, Cengage, 2019: los intervalos, sus calidades, la inversión y los intervalos compuestos
- W. Piston, *Harmony*, revisado por M. DeVoto, W. W. Norton, 1987: las escalas y los intervalos
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §5 enlaza a su línea
- Learn, lección 1 de music-theory-ga y su salida esperada en el commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: las comprobaciones compiladas de los intervalos simples de GA citadas en el §5
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
