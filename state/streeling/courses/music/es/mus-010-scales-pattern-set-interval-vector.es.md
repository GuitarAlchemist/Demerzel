---
module_id: mus-010-scales-pattern-set-interval-vector
department: music
course: Fórmulas de escalas, conjuntos y vector interválico diatónico
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-008-intervals-inversion-compound, mat-022-symmetry-groups-invariants]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Fórmulas de escalas, conjuntos y vector interválico diatónico — Lo que la escala mayor tiene de raro

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Construir cualquier escala sobre cualquier tónica a partir de su fórmula de intervalos, y escribir una escala de siete notas con una letra por grado
- Distinguir la fórmula de una escala, su conjunto de clases de altura y su vector de clases de intervalo, y decir qué olvida cada uno
- Calcular los vectores de las escalas mayor, pentatónica y de tonos enteros, y usar el teorema de las notas comunes para decir cuántas notas comparten dos tonalidades
- Reconocer la propiedad de escala profunda, la propiedad de Myhill, la regularidad máxima y la generación por quintas, y decir cuáles tienen la escala mayor, la pentatónica y la escala de tonos enteros
- Rastrear cómo calcula GA estas propiedades, y dónde sus resultados dependen de la transposición o se apartan de las definiciones

---

## 1. Una escala como fórmula de intervalos

Una escala enumera notas en orden dentro de una octava. Su **fórmula de intervalos** da los semitonos de cada nota a la siguiente, terminando con el paso que vuelve a la octava, de modo que los pasos suman 12.

| Escala | Fórmula | Sobre do |
|------|------|------|
| Mayor | 2 2 1 2 2 2 1 | do re mi fa sol la si |
| Menor natural | 2 1 2 2 1 2 2 | do re mi♭ fa sol la♭ si♭ |
| Pentatónica mayor | 2 2 3 2 3 | do re mi sol la |
| Tonos enteros | 2 2 2 2 2 2 | do re mi fa♯ sol♯ la♯ |

Escrita en tonos (T) y semitonos (S), la fórmula mayor es T T S T T T S. El artículo «Major scale» de Wikipedia señala que «a major scale may be seen as two identical tetrachords separated by a whole tone» (una escala mayor puede verse como dos tetracordios idénticos separados por un tono): T T S, luego T, luego T T S.

Para construir una escala sobre otra tónica, se aplican los mismos pasos desde esa tónica. Una escala de siete notas toma entonces una letra por grado, y cada alteración se deduce de la letra (MUS-007). Mi mayor se escribe mi fa♯ sol♯ la si do♯ re♯. Fa mayor se escribe fa sol la si♭ do re mi: el cuarto grado está un semitono por encima de la, y se escribe si♭, no la♯, porque la ya es el tercer grado.

En la guitarra, una fórmula tocada en una sola cuerda es una lista de distancias entre trastes. En la cuerda de la, la fórmula mayor desde la cuerda al aire da los trastes 0 2 4 5 7 9 11 12: la si do♯ re mi fa♯ sol♯ la. Las mismas distancias desde el traste 3 dan do mayor: trastes 3 5 7 8 10 12 14 15.

### Ejercicio práctico

Construye si♭ mayor y re menor natural a partir de sus fórmulas, con una letra por grado.

> *Solución:* Si♭ mayor: si♭ do re mi♭ fa sol la, pasos 2 2 1 2 2 2 1. Re menor natural: re mi fa sol la si♭ do, pasos 2 1 2 2 1 2 2. En las dos, cada letra aparece una vez.

---

## 2. Fórmula, conjunto y tónica

Una fórmula no dice dónde empezar; una tónica fija las notas. El **conjunto de clases de altura** conserva las notas y olvida la tónica, el orden y las octavas (MUS-020): do mayor es {0, 2, 4, 5, 7, 9, 11} con do = 0.

Dos escalas pueden compartir un conjunto y diferir en su fórmula. La menor natural, la si do re mi fa sol, contiene las notas de do mayor. Su fórmula, 2 1 2 2 1 2 2, es la fórmula mayor leída desde su sexto paso: los pasos la–si, si–do, y luego de do–re a sol–la. Leer una fórmula desde otro paso da un **modo**; MUS-006 cuenta los modos como rotaciones.

Transportar una escala suma el mismo número a cada clase de altura. Conserva la fórmula y cambia el conjunto: las doce escalas mayores son doce conjuntos distintos. Una escala que se transforma en sí misma por una transposición tiene menos: solo hay dos escalas de tonos enteros, {0, 2, 4, 6, 8, 10} y {1, 3, 5, 7, 9, 11} (MUS-006, MAT-022).

El resto de esta lección estudia propiedades del conjunto, que la tónica no cambia: su vector interválico, los tamaños que toman sus intervalos, y lo regularmente que se reparte por la octava.

### Ejercicio práctico

¿Qué escala mayor contiene las notas de mi menor natural, y desde qué grado de esa escala empieza mi menor?

> *Solución:* Mi menor natural se escribe mi fa♯ sol la si do re, las notas de sol mayor. Mi es el sexto grado de sol mayor, y la fórmula de mi menor, 2 1 2 2 1 2 2, es la de sol mayor leída desde ese grado.

---

## 3. El vector interválico de una escala

El **vector de clases de intervalo** cuenta, para cada par de notas de un conjunto, la clase de intervalo que las separa, de 1 (un semitono o una séptima mayor) a 6 (un tritono) (MUS-020). Un conjunto de n notas tiene n(n − 1)/2 pares: 21 para siete notas, 15 para seis, 10 para cinco.

Para la escala mayor, cuenta cada clase sobre do re mi fa sol la si:
- **Clase 1**, semitonos: mi–fa y si–do. **2.**
- **Clase 2**, tonos: do–re, re–mi, fa–sol, sol–la y la–si. **5.**
- **Clase 3**, terceras menores: re–fa, mi–sol, la–do y si–re. **4.**
- **Clase 4**, terceras mayores: do–mi, fa–la y sol–si. **3.**
- **Clase 5**, quintas justas: fa–do, do–sol, sol–re, re–la, la–mi y mi–si. **6.**
- **Clase 6**, el tritono: si–fa. **1.**

El total es 21, y el vector es <2 5 4 3 6 1>.

| Escala | Notas | Pares | Vector |
|------|------|------|------|
| Mayor | do re mi fa sol la si | 21 | <2 5 4 3 6 1> |
| Menor armónica | la si do re mi fa sol♯ | 21 | <3 3 5 4 4 2> |
| Pentatónica mayor | do re mi sol la | 10 | <0 3 2 1 4 0> |
| Tonos enteros | do re mi fa♯ sol♯ la♯ | 15 | <0 6 0 6 0 3> |

La pentatónica no tiene semitono ni tritono; MUS-006 calcula el mismo vector para la pentatónica menor. En la escala de tonos enteros, cada nota tiene un tono a cada lado y una tercera mayor a cada lado, lo que da seis pares de clase 2 y seis de clase 4. Sus tres tritonos son do–fa♯, re–sol♯ y mi–la♯, y no tiene ninguna clase de intervalo impar.

### Ejercicio práctico

Calcula el vector de la escala de seis notas do re mi fa sol la.

> *Solución:* Quince pares. Clase 1: mi–fa. Clase 2: do–re, re–mi, fa–sol y sol–la. Clase 3: re–fa, mi–sol y la–do. Clase 4: do–mi y fa–la. Clase 5: do–fa, do–sol, re–sol, re–la y mi–la. Ningún tritono, ya que falta si. El vector es <1 4 3 2 5 0>, y sus componentes suman 15.

---

## 4. Escalas profundas y notas comunes

Las seis componentes de <2 5 4 3 6 1> son seis números distintos. El artículo «Common tone (scale)» de Wikipedia llama a esto la **propiedad de escala profunda** (deep scale property): «containing each interval class a unique number of times» (contener cada clase de intervalo un número de veces que solo le pertenece a ella). El vector de la pentatónica repite 0, el de la menor armónica repite 3 y 4, y el de la escala de tonos enteros repite 0 y 6: ninguna de ellas es profunda.

**El teorema de las notas comunes.** Transporta un conjunto n semitonos. Una nota b del conjunto transportado vale a + n para alguna nota a del conjunto, y b pertenece también al conjunto de partida exactamente cuando el conjunto contiene el intervalo que sube n semitonos desde a. El número de notas comunes es, pues, el número de tales pares:
- para n de 1 a 5, cada par es un intervalo de clase n, y el número es la componente del vector para la clase n;
- para n de 7 a 11, cada par es un intervalo de clase 12 − n;
- para el tritono, n = 6, cada tritono cuenta desde sus dos extremos, ya que a + 6 + 6 = a: si sube a fa y fa sube a si. El número es el doble de la componente del vector.

Wikipedia enuncia el teorema para la escala diatónica: «However many times an interval class occurs in a diatonic scale is the number of tones common both to the original scale and a scale transposed by that particular interval class.» (El número de veces que aparece una clase de intervalo en una escala diatónica es el número de notas comunes a la escala de partida y a la escala transportada por esa clase de intervalo.) Para do mayor:

| Transposición (semitonos) | Tonalidades | Notas comunes |
|------|------|------|
| 0 | do | 7 |
| 1 o 11 | re♭, si | 2 |
| 2 o 10 | re, si♭ | 5 |
| 3 o 9 | mi♭, la | 4 |
| 4 o 8 | mi, la♭ | 3 |
| 5 o 7 | fa, sol | 6 |
| 6 | fa♯ | 2: si, y fa, escrito mi♯ en fa♯ mayor |

Las dos vecinas de do en el círculo de quintas, fa y sol, conservan seis notas: pasar de do mayor a sol mayor solo cambia fa por fa♯, un dedo movido un traste. Wikipedia: «Six of seven possible common tones are shared by closely related keys» (las tonalidades vecinas comparten seis de las siete notas comunes posibles). Como la escala es profunda, las transposiciones de 1 a 5 semitonos conservan cinco números de notas distintos, los mismos hacia arriba o hacia abajo.

La fila del tritono pide cuidado. Wikipedia da al tritono 1 nota común, «as there is only one tritone in a diatonic scale» (ya que solo hay un tritono en una escala diatónica), y su tabla pone si para fa♯ mayor y fa para sol♭ mayor en filas separadas. Contadas como clases de altura, do mayor y fa♯ mayor comparten a la vez si y fa; fa♯ mayor escribe fa como mi♯. Cada tritono cuenta desde sus dos extremos. Eso da dos notas, tantas como una transposición de un semitono; el 1 de Wikipedia solo vale para las notas escritas igual. El número doblado del tritono puede repetir otro: la propiedad de escala profunda solo garantiza números distintos para las clases de intervalo 1 a 5.

La escala de tonos enteros muestra el caso opuesto: «every even transposition of the whole tone scale is identical with the original and every odd transposition has no common tones whatsoever» (toda transposición par de la escala de tonos enteros es idéntica a la original, y toda transposición impar no tiene ninguna nota común) (Wikipedia, «Common tone (scale)»).

**¿Qué conjuntos son profundos?** Seis números enteros distintos suman al menos 0 + 1 + 2 + 3 + 4 + 5 = 15, así que un conjunto profundo tiene al menos 15 pares, y por tanto al menos seis notas. Un recuento sobre los 4096 conjuntos de clases de altura encuentra 48 conjuntos profundos, doce transposiciones en cada una de cuatro clases de conjuntos:

| Clase de Forte | Ejemplo | Vector | Una cadena de |
|------|------|------|------|
| 6-1 | do do♯ re mi♭ mi fa | <5 4 3 2 1 0> | semitonos |
| 6-32 | do re mi fa sol la | <1 4 3 2 5 0> | quintas, de fa a mi |
| 7-1 | do do♯ re mi♭ mi fa fa♯ | <6 5 4 3 2 1> | semitonos |
| 7-35 | do re mi fa sol la si | <2 5 4 3 6 1> | quintas, de fa a si |

Entre los conjuntos de siete notas, solo la escala diatónica y el segmento cromático de siete notas son, pues, profundos. El artículo «Common tone (scale)» de Wikipedia enuncia la regla así: «In twelve-tone equal temperament, all scales with the deep scale property can be generated with any interval coprime with twelve» (en el temperamento igual de doce sonidos, todas las escalas con la propiedad de escala profunda pueden generarse con cualquier intervalo coprimo con doce). Leída junto con la tabla, cada escala profunda es una cadena de uno solo de esos intervalos, no de cada uno: el semitono o la quinta, los dos únicos salvo inversión. Multiplicar cada clase de altura por 5, la operación que MUS-020 llama M5, intercambia los números de las clases 1 y 5: envía cada fila cromática de la tabla a la fila de quintas del mismo tamaño.

### Ejercicio práctico

¿Cuántas notas comparten do mayor y mi♭ mayor, y cuáles?

> *Solución:* Mi♭ está 3 semitonos por encima de do, y la escala mayor tiene cuatro intervalos de clase 3, así que comparten cuatro notas: do, re, fa y sol. Mi♭ mayor sustituye mi, la y si por mi♭, la♭ y si♭.

---

## 5. Dos tamaños por paso, y reparto regular

Un **intervalo genérico** «is the number of scale steps between notes of a collection or scale» (es el número de pasos de la escala entre dos notas de una colección o de una escala); un **intervalo específico** es el número de semitonos (Wikipedia, «Generic and specific intervals»). En la escala mayor, una tercera, dos pasos, es una tercera menor o una tercera mayor: 3 o 4 semitonos.

| Intervalo genérico (pasos) | 1 | 2 | 3 | 4 | 5 | 6 |
|------|------|------|------|------|------|------|
| Mayor | 1, 2 | 3, 4 | 5, 6 | 6, 7 | 8, 9 | 10, 11 |
| Pentatónica mayor | 2, 3 | 4, 5 | 7, 8 | 9, 10 | | |
| Tonos enteros | 2 | 4 | 6 | 8 | 10 | |

- La **propiedad de Myhill** consiste en tener «exactly two specific intervals for every generic interval» (exactamente dos intervalos específicos para cada intervalo genérico) (Wikipedia, «Generic and specific intervals»). Las escalas mayor y pentatónica la tienen; la escala de tonos enteros, con un solo tamaño por paso, no.
- La **regularidad máxima** (maximal evenness, Clough y Douthett, 1991) es otra condición: cada intervalo genérico toma un solo tamaño o dos tamaños consecutivos, de modo que las notas estén «spread out as much as possible» (repartidas tanto como sea posible) (Wikipedia, «Maximal evenness»). Las escalas mayor, pentatónica y de tonos enteros son máximamente regulares; la menor armónica no lo es, ya que sus segundas miden 1, 2 y 3 semitonos. Ninguna de las dos propiedades implica la otra. La escala de tonos enteros es máximamente regular sin tener la propiedad de Myhill, y el segmento cromático de siete notas de do a fa♯ del §4 tiene la propiedad de Myhill sin ser máximamente regular: sus segundas miden 1 o 6 semitonos, dos tamaños pero no consecutivos.
- Una **colección generada** es «formed by repeatedly adding a constant interval in integer notation, the generator» (formada añadiendo repetidamente un intervalo constante en notación entera, el generador) (Wikipedia, «Generated collection»). La escala mayor es una cadena de siete notas unidas por seis quintas: «F-C-G-D-A-E-B» (fa-do-sol-re-la-mi-si). Una cadena está **bien formada** cuando el generador abarca siempre el mismo número de pasos: en la escala mayor, cada quinta de la cadena abarca 4 pasos. «The major and minor pentatonic scales are also well formed.» (Las escalas pentatónicas mayor y menor también están bien formadas.) Las seis notas fa do sol re la mi dan do re mi fa sol la, cuyos pasos son 2 2 1 2 2 3: una quinta abarca 4 pasos de do a sol pero 3 de fa a do, así que esta cadena es generada y no está bien formada. El artículo «Maximal evenness» de Wikipedia une la buena formación a la propiedad de Myhill, «a scale with Myhill's property is said to be a well-formed scale» (de una escala con la propiedad de Myhill se dice que está bien formada), y dice que la escala de tonos enteros «is not well-formed since each generic interval comes in only one size» (no está bien formada, ya que cada intervalo genérico tiene un solo tamaño). Su artículo «Generated collection» llama a la misma escala una «degenerate well-formed collection» (colección bien formada degenerada), en la que cada paso es el generador. Para los conjuntos de dos notas o más, dejando aparte las cadenas degeneradas, buena formación y propiedad de Myhill quieren decir lo mismo.

| Escala | Profunda | Propiedad de Myhill | Máximamente regular | Generada |
|------|------|------|------|------|
| Mayor | sí | sí | sí | sí, siete notas en quintas |
| Pentatónica mayor | no | sí | sí | sí, cinco notas en quintas |
| Tonos enteros | no | no | sí | degenerada, por tonos |
| Menor armónica | no | no | no | no |
| do re mi fa sol la | sí | no | no | sí, seis notas en quintas |

De estas cinco escalas, solo la escala mayor tiene las cuatro propiedades. La **propiedad de Rothenberg** (Rothenberg propriety) añade una prueba: un intervalo que abarca más pasos nunca debería ser más pequeño que uno que abarca menos. La escala mayor la pasa, pero el tritono es a la vez una cuarta, fa–si, y una quinta, si–fa, así que el artículo «Rothenberg propriety» de Wikipedia la llama propia pero «not strictly proper because the three step intervals and the four step intervals share an interval size (the tritone)» (no estrictamente propia, porque los intervalos de tres pasos y los de cuatro pasos comparten un tamaño, el tritono); «the major pentatonic scale is strictly proper» (la pentatónica mayor es estrictamente propia).

Son hechos de estructura. No prueban que la escala mayor suene equilibrada; muestran lo que tiene de raro entre los 4096 conjuntos.

### Ejercicio práctico

¿Tiene la menor armónica de la la propiedad de Myhill? ¿Es máximamente regular?

> *Solución:* Ninguna de las dos cosas. Sus segundas la–si, 2 semitonos, si–do, 1, y fa–sol♯, 3: un mismo intervalo genérico en tres tamaños. El artículo «Maximal evenness» de Wikipedia da este ejemplo.

---

## 6. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos de abajo se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Esta lección documenta ese código y no lo modifica. No ha ejecutado GA ni sus pruebas: los recuentos de abajo vienen de una transcripción en Python, línea por línea, de los métodos citados. Los archivos que cita no han cambiado en la rama `main` de GA, en `0843879`. El curso music-theory-ga de Learn compila una versión anterior de GA, `a826864`, que tiene `IsDeepScale` pero no `ScaleStructuralProperties`. Su lección 4 [ya cita `IsDeepScale`](https://github.com/spareilleux/learn/blob/0c918c8206dc9dda0241d097e6b0c65e897c92ec/src/content/docs/music-theory-ga/04-set-classes.mdx#L77-L81) y la definición de escala profunda de Wikipedia; esta sección sigue adelante, hasta las notas comunes y las demás propiedades.

**Una escala se construye a partir de notas.** [`Scale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L37-L45) toma una lista de notas y [calcula su conjunto de clases de altura y su vector](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L42-L43). Sus escalas con nombre se escriben nota por nota: [`Major`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L53) vale «C D E F G A B», [`MajorPentatonic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L57) «C D E G A», [`WholeTone`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L60) «C D E F# G# A#» y [`Minor.Natural`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L125) «A B C D E F G», con nombres de notas en inglés. Una prueba comprueba que [el vector de la escala mayor es <2 5 4 3 6 1>](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleTests.cs#L19-L21), y otra que [la menor y do mayor comparten un conjunto](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleTests.cs#L24-L27), como en el §2. La escala expone también [seis propiedades estructurales](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L85-L90), y el servidor MCP de GA las muestra para un identificador de escala de 12 bits en su [herramienta `GaScaleProperties`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/ScaleTool.cs#L168-L194).

**`IsDeepScale` es correcta, y ningún código hace referencia a ella.** [`IsDeepScale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVector.cs#L99) comprueba que los seis valores del vector son distintos, y el vector siempre contiene seis valores, [ceros incluidos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L45-L72), así que los dos ceros de la pentatónica cuentan como una repetición. Transcrita sobre los 4096 conjuntos, es verdadera exactamente para los 48 conjuntos del §4. Su documentación [remite al teorema de las notas comunes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVector.cs#L89-L98). Ningún otro archivo de código de GA la nombra, y ninguna prueba la comprueba.

**La propiedad de Myhill y la propiedad de Rothenberg siguen las definiciones.** [`HasMyhillProperty`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L40-L68) reúne los tamaños de cada intervalo genérico y exige exactamente dos; transcrita, es verdadera para las escalas mayor y pentatónica y falsa para la escala de tonos enteros. [`GetRothenbergPropriety`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L76-L123) compara el mayor tamaño de cada intervalo genérico con el menor tamaño de cada intervalo más grande; transcrita, devuelve `Proper` para la escala mayor y `StrictlyProper` para la pentatónica, como Wikipedia. La prueba de Myhill se llama [`Dorian_HasMyhillProperty_ReturnsTrue`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Atonal/ScaleStructuralPropertiesTests.cs#L10-L16) y construye `Scale.Major`; su comentario dice «Major / Dorian (1709)», pero 1709 es el identificador de do dórico, un conjunto distinto del 2741 de do mayor. Las cinco pruebas del archivo construyen `Scale.Major`, así que ninguna comprueba una escala para la que `HasMyhillProperty` o `IsWellFormed` sea falso.

**`IsWellFormed` prueba la generación, no la buena formación.** El resumen del método define una escala bien formada como una escala [«generated by repeatedly stacking a single generator interval mod 12»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L151-L154) (generada apilando repetidamente un solo intervalo generador módulo 12), y el [método](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L163-L187) acepta cualquier cadena de un solo intervalo. Es la colección generada del §5. Transcrita sobre los 4096 conjuntos, 89 conjuntos pasan `IsWellFormed` sin tener la propiedad de Myhill:
- 13 conjuntos de una nota como mucho: el conjunto vacío y las 12 notas sueltas;
- 16 divisiones iguales de la octava: el tritono, la tríada aumentada, la séptima disminuida, la escala de tonos enteros y el total cromático, que Wikipedia llama degeneradas;
- 60 cadenas de quintas de 4, 6, 8, 9 o 10 notas, como do re sol la y el do re mi fa sol la del §5, que tienen cada una un intervalo genérico en tres tamaños.

Ningún conjunto tiene la propiedad de Myhill y falla `IsWellFormed`. Para la escala mayor, el método devuelve el generador 5, el primero que funciona en el orden de 1 a 11: la cadena de cuartas si mi la re sol do fa, que es la cadena de quintas del §5 leída al revés.

**La puntuación de regularidad depende de la transposición.** [`GetMaximalEvennessDiscrepancy`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L129-L149) toma las clases de altura de un conjunto de n notas en orden ascendente desde do, las compara con los puntos 0, 12 / n, 2 × 12 / n y así sucesivamente, y devuelve la media cuadrática de las diferencias. Su resumen cita a Clough y Douthett y promete [«0.0 for perfectly even sets like Whole Tone or Augmented»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L125-L128) (0.0 para los conjuntos perfectamente regulares, como la escala de tonos enteros o la aumentada). Transcrita, redondeada a cuatro decimales:
- la escala de tonos enteros obtiene 0,0000 sobre do y 1,0000 sobre do♯, y la tríada aumentada 0,0000 sobre do y 1,0000 sobre do♯;
- el propio [`Scale.Augmented`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L61) de GA, do re♯ mi sol sol♯ si, es la escala aumentada de seis notas, no la tríada, y obtiene 0,7071;
- las doce escalas mayores obtienen de 0,2857, si♭ mayor, a 1,1780, fa♯ mayor; do mayor obtiene 0,4041.

Para Clough y Douthett, la regularidad máxima es una propiedad de sí o no, y las doce escalas mayores la tienen. Según la puntuación de GA, 472 conjuntos de siete notas que no son máximamente regulares salen más regulares que fa♯ mayor. La propia descripción de la herramienta sugiere [«1709 for Dorian or 2741 for Major»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/ScaleTool.cs#L174) (1709 para el dórico o 2741 para el mayor): los dos identificadores contienen las notas de si♭ mayor y de do mayor, una misma escala en dos transposiciones, y obtienen 0,2857 y 0,4041. Ninguna prueba comprueba la puntuación.

Corregir todo esto corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

¿Qué devuelven `IsWellFormed` y `HasMyhillProperty` de GA para do re sol la, y por qué no coinciden?

> *Solución:* `IsWellFormed` devuelve verdadero con el generador 5: desde la, sumar 5 semitonos tres veces da la re sol do. `HasMyhillProperty` devuelve falso: las segundas do–re, re–sol, sol–la y la–do miden 2, 5, 2 y 3 semitonos, tres tamaños. El conjunto es una cadena de un solo intervalo, que es todo lo que comprueba `IsWellFormed`, pero la cuarta abarca dos pasos de la a re y uno de re a sol, así que la cadena no está bien formada.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA. La versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`, ya que `ScaleStructuralProperties` no existe en `a826864`. Nada en esta sección es una medición:
- las predicciones vienen de los §3 a §6 y se escriben antes de cualquier ejecución;
- los recuentos y las puntuaciones vienen de la transcripción en Python del §6;
- una versión posterior de esta lección informará de los resultados.

Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Tres vectores.** Mostrar `IntervalClassVector` e `IsDeepScale` para `Scale.Major`, `Scale.MajorPentatonic` y `Scale.WholeTone`. Predicción: <2 5 4 3 6 1> y verdadero, <0 3 2 1 4 0> y falso, <0 6 0 6 0 3> y falso.
2. **El censo de escalas profundas.** Para cada conjunto de clases de altura, leer `IsDeepScale`, y para cada conjunto profundo, `IsWellFormed` y su generador. Predicción: 48 conjuntos profundos, 24 de seis notas en las clases 6-1 y 6-32 y 24 de siete notas en las clases 7-1 y 7-35; todos pasan `IsWellFormed`, con el generador 1 para las clases cromáticas y 5 para las demás.
3. **El teorema de las notas comunes.** Para cada conjunto no vacío y cada n de 1 a 11, contar las clases de altura comunes al conjunto y a su transposición de n, y comparar con el vector, doblado para n = 6. Predicción: ninguna excepción en los 4095 conjuntos; para do mayor, los números para n = 1 a 11 son 2 5 4 3 6 2 6 3 4 5 2.
4. **La puntuación de regularidad.** Llamar a `GetMaximalEvennessDiscrepancy` sobre las doce escalas mayores y las dos escalas de tonos enteros. Predicción, con cuatro decimales:

   | Escala mayor | Puntuación | Escala mayor | Puntuación |
   |------|------|------|------|
   | do | 0,4041 | fa♯ | 1,1780 |
   | do♯ | 0,5151 | sol | 0,5151 |
   | re | 0,6389 | la♭ | 0,4041 |
   | mi♭ | 0,3194 | la | 0,7693 |
   | mi | 0,9035 | si♭ | 0,2857 |
   | fa | 0,3194 | si | 1,0400 |

   Las escalas de tonos enteros obtienen 0,0000 sobre do y 1,0000 sobre do♯, y 472 conjuntos de siete notas que no son máximamente regulares obtienen menos de 1,1780.
5. **Generada o bien formada.** Sobre los 4096 conjuntos, el conjunto vacío incluido, contar los conjuntos para los que `IsWellFormed` es verdadero y `HasMyhillProperty` falso, y luego al revés. Predicción: 89 y 0.

### Ejercicio práctico

El paso 4 predice exactamente 1,0000 para la escala de tonos enteros sobre do♯. ¿Por qué?

> *Solución:* Sus notas en orden ascendente son 1, 3, 5, 7, 9 y 11, y los puntos con los que se comparan son 0, 2, 4, 6, 8 y 10. Cada nota está a un semitono de su punto, así que cada diferencia al cuadrado vale 1, y la media cuadrática de seis unos vale 1.

---

## 8. Errores comunes

- **Tomar la fórmula por el conjunto.** La menor natural y do mayor comparten un conjunto, no una fórmula.
- **Escribir con la letra equivocada.** Fa mayor tiene si♭, no la♯: una letra por grado.
- **Tomar profunda por regular.** La escala de tonos enteros es perfectamente regular y no es profunda; el conjunto profundo do re mi fa sol la no es máximamente regular.
- **Contar el tritono una sola vez.** En clases de altura, una transposición de un tritono conserva el doble de notas que tritonos tiene el conjunto: do mayor y fa♯ mayor comparten si y fa.
- **Leer el `IsWellFormed` de GA como la buena formación de Carey y Clampitt.** Solo comprueba que un conjunto es una cadena de un solo intervalo.
- **Comparar las puntuaciones de regularidad de GA entre transposiciones.** La puntuación se mide desde do: si♭ mayor y fa♯ mayor son igual de regulares y obtienen 0,2857 y 1,1780.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Fórmula de intervalos** | Los semitonos de cada nota de una escala a la siguiente, hasta la octava, como 2 2 1 2 2 2 1 |
| **Conjunto de clases de altura** | Las notas de una escala sin tónica, orden ni octava, como {0, 2, 4, 5, 7, 9, 11} |
| **Vector de clases de intervalo** | El número de pares de notas en cada clase de intervalo de 1 a 6, como <2 5 4 3 6 1> |
| **Escala profunda** | Un conjunto cuyo vector contiene seis números distintos: en doce sonidos, las clases 6-1, 6-32, 7-1 y 7-35 |
| **Teorema de las notas comunes** | Una transposición de n semitonos conserva tantas notas como el vector cuenta para la clase de intervalo de n, el doble para el tritono |
| **Intervalo genérico** | El número de pasos de la escala entre dos notas |
| **Propiedad de Myhill** | Cada intervalo genérico toma exactamente dos tamaños |
| **Máximamente regular** | Cada intervalo genérico toma un solo tamaño o dos tamaños consecutivos |
| **Colección generada** | Un conjunto formado apilando un solo intervalo, como la cadena de quintas fa do sol re la mi si |
| **Bien formada** | Generada, con un generador que abarca siempre el mismo número de pasos; para las cadenas de dos notas o más que no son degeneradas, equivale a la propiedad de Myhill |

---

## Autoevaluación

**1. Construye mi♭ mayor a partir de su fórmula y da su conjunto de clases de altura.**
> Se escribe mi♭ fa sol la♭ si♭ do re, con los pasos 2 2 1 2 2 2 1. Con do = 0, su conjunto es {0, 2, 3, 5, 7, 8, 10}.

**2. ¿Por qué una modulación de do mayor a sol mayor cambia una nota, mientras que do mayor y fa♯ mayor todavía comparten dos?**
> Sol es una transposición de 7 semitonos, clase de intervalo 5, y la escala mayor contiene seis intervalos de clase 5, así que seis notas se quedan y una cambia, fa por fa♯. Fa♯ es una transposición de un tritono; la escala tiene un tritono, si–fa, que cuenta desde sus dos extremos, así que si y fa se quedan. Escrito en fa♯ mayor, fa es mi♯.

**3. ¿Es profunda la pentatónica mayor? ¿Tiene la propiedad de Myhill? ¿Es máximamente regular?**
> No es profunda: su vector <0 3 2 1 4 0> contiene dos veces el 0. Tiene la propiedad de Myhill, ya que cada intervalo genérico toma dos tamaños: 2 o 3, 4 o 5, 7 u 8, 9 o 10. Es máximamente regular, ya que cada par de tamaños es consecutivo.

**4. En GA en `5c3a52a`, ¿qué devuelve `GetMaximalEvennessDiscrepancy` para do mayor y para si♭ mayor, y qué muestra la diferencia?**
> 0,4041 y 0,2857, con cuatro decimales. Las dos escalas tienen la misma fórmula y son igual de regulares; la puntuación difiere porque mide cada conjunto desde do.

**Criterio de aprobación:** Construir y escribir una escala a partir de su fórmula sobre cualquier tónica. Calcular el vector de una escala y usarlo para contar las notas comunes, tritono incluido. Decir cuáles de las propiedades profunda, de Myhill, máximamente regular y generada tiene una escala. Decir qué calcula GA para cada una, y dónde su resultado depende de la transposición o se aparta de la definición.

---

## Base de investigación

- Wikipedia, «Major scale»: los dos tetracordios, y la regularidad máxima.
- Wikipedia, «Interval vector»: la definición, y la propiedad de escala profunda de la escala mayor y sus modos.
- Wikipedia, «Common tone (scale)»: el teorema de las notas comunes y su tabla, las tonalidades vecinas, la propiedad de escala profunda, la generación por un intervalo coprimo con doce, y las transposiciones de la escala de tonos enteros; según Johnson, *Foundations of Diatonic Theory*, 2003, y Gamer, 1967.
- Wikipedia, «Generic and specific intervals»: intervalos genéricos y específicos, y la propiedad de Myhill.
- Wikipedia, «Maximal evenness»: la definición de Clough y Douthett, la menor armónica, la escala de tonos enteros, y la propiedad de Myhill como buena formación.
- Wikipedia, «Generated collection»: la cadena de quintas, las colecciones bien formadas y degeneradas, según Carey y Clampitt, 1989.
- Wikipedia, «Rothenberg propriety»: la escala mayor propia pero no estrictamente, la pentatónica estrictamente propia.
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §6 enlaza a su línea.
- Learn, lección 4 de music-theory-ga en el commit `0c918c8206dc9dda0241d097e6b0c65e897c92ec`: su exposición de `IsDeepScale`.
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición propia.
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión.
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
