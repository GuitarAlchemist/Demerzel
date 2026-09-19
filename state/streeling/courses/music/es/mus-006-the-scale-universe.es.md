---
module_id: mus-006-the-scale-universe
department: music
course: Fundamentos de teoría musical
level: intermediate
alchemical_stage: albedo
prerequisites:
  - mus-001-what-is-a-chord
estimated_duration: "45 minutes"
produced_by: music
version: "1.0.0"
---

# El universo de las escalas: 4096 posibilidades a partir de 12 notas

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración: 45 minutos

## Objetivos de aprendizaje

Al terminar este curso, serás capaz de:

- Representar cualquier escala como un número binario de 12 bits y convertirlo en un entero decimal
- Explicar por qué existen exactamente 4096 escalas matemáticamente posibles en el temperamento igual de 12 tonos
- Calcular los modos de cualquier escala mediante desplazamientos circulares (rotaciones de bits)
- Distinguir entre el recuento total (4096) y el recuento bajo distintas equivalencias (formas primas, clases de Forte)
- Aplicar los criterios de Zeitler para reducir el universo a las escalas «musicalmente reales»
- Calcular vectores interválicos, brillo y propiedades de simetría a partir del entero de una escala
- Llevar cualquier entero de escala a posiciones en el diapasón de la guitarra
- Relacionar el espacio de escalas con las relaciones de equivalencia OPTIC-K que se usan en la teoría de conjuntos musical

---

## 1. El alfabeto cromático

La música occidental usa doce clases de altura por octava. Una **clase de altura** es una nota sin importar en qué octava aparezca — todos los Do de un piano pertenecen a la misma clase de altura.

Las doce clases de altura, numeradas del 0 al 11:

| Clase de altura | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-------------|---|---|---|---|---|---|---|---|---|---|----|----|
| Nombre de nota | C | C#/Db | D | D#/Eb | E | F | F#/Gb | G | G#/Ab | A | A#/Bb | B |

Ahora piensa en una escala como una **elección**: para cada una de las doce clases de altura, o bien está **dentro** de la escala (1) o bien **fuera** (0). Eso nos da un número binario de 12 bits — doce decisiones independientes de sí/no.

**¿Cuántas elecciones posibles hay?** Dos opciones para cada una de las doce posiciones:

$$ 2^{12} = 4096 $$

Existen exactamente 4096 escalas matemáticamente posibles en el temperamento igual de 12 tonos. Esto incluye la escala vacía (todo ceros), la escala cromática (todo unos), todas las «escalas» de una sola nota, todas las escalas tradicionales y cualquier colección extraña que haya entre medias.

Este es el **universo de las escalas**. Su tamaño es finito, cognoscible y sorprendentemente pequeño — un número que una computadora puede enumerar en microsegundos.

---

## 2. Una escala ES un número

Este es el cambio de enfoque clave: **toda escala es un entero entre 0 y 4095**.

### La asignación de bits

Asigna a cada clase de altura una posición de bit:

| Bit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| Clase de altura | C | C# | D | D# | E | F | F# | G | G# | A | A# | B |
| Valor posicional | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |

Para convertir una escala en un entero, marca cada nota con un 1 y suma los valores posicionales.

### Ejemplo: la escala mayor

La **escala de Do mayor** contiene las notas Do, Re, Mi, Fa, Sol, La, Si — clases de altura 0, 2, 4, 5, 7, 9, 11.

En binario (leyendo del bit 11 al bit 0):

```
Bit:     11 10  9  8  7  6  5  4  3  2  1  0
Note:     B  Bb  A  Ab G  Gb F  E  Eb D  Db C
In scale:  1  0  1  0  1  0  1  1  0  1  0  1
```

En decimal:

$$ 1 + 4 + 16 + 32 + 128 + 512 + 2048 = 2741 $$

**Do mayor = 2741.**

Todas las escalas mayores tienen la misma **estructura interválica**, así que, sea cual sea la tónica, el patrón (pasos de 2-2-1-2-2-2-1 semitonos) define lo mayor. El entero 2741 es la representación con raíz en Do. Con raíz en otras notas, el patrón rota.

### Ejemplo: la escala pentatónica menor

La escala **pentatónica menor de Do** contiene Do, Mib, Fa, Sol, Sib — clases de altura 0, 3, 5, 7, 10.

En binario:

```
Bit:     11 10  9  8  7  6  5  4  3  2  1  0
In scale:  0  1  0  0  1  0  1  0  1  0  0  1
```

En decimal:

$$ 1 + 8 + 32 + 128 + 1024 = 1193 $$

**Pentatónica menor de Do = 1193.**

### Por qué importa

Una vez que aceptas que una escala es un número, todo lo demás se deduce:
- Puedes **enumerar** todas las escalas (contar de 0 a 4095)
- Puedes **comparar** escalas (comparación de enteros)
- Puedes **transformar** escalas (operaciones de bits: desplazamiento, AND, OR, XOR, POPCOUNT)
- Puedes **buscar** escalas (por vectores interválicos, cardinalidades o simetrías concretas)
- Puedes **almacenar** escalas (12 bits en lugar de una lista de notas)

Una escala no es algo místico. Es un número.

### Ejercicio práctico

Convierte las tres escalas siguientes en enteros usando la asignación de bits:

1. **Do menor natural** (Do, Re, Mib, Fa, Sol, Lab, Sib) — clases de altura 0, 2, 3, 5, 7, 8, 10
2. **Pentatónica mayor de Do** (Do, Re, Mi, Sol, La) — clases de altura 0, 2, 4, 7, 9
3. **Escala de tonos enteros de Do** (Do, Re, Mi, Fa#, Sol#, La#) — clases de altura 0, 2, 4, 6, 8, 10

Calcula cada una sumando los valores posicionales (potencias de 2). Comprueba tus respuestas más abajo.

Respuestas:
1. Do menor natural = 1 + 4 + 8 + 32 + 128 + 256 + 1024 = **1453**
2. Pentatónica mayor de Do = 1 + 4 + 16 + 128 + 512 = **661**
3. Tonos enteros de Do = 1 + 4 + 16 + 64 + 256 + 1024 = **1365**

---

## 3. Los modos como rotaciones

Un **modo** es una escala que empieza en otro grado. Do dórico contiene las mismas notas que Sib mayor, pero empieza en Do. En la representación entera, esto no es una suma ni una multiplicación — es una **rotación**.

### La operación de desplazamiento circular

Para encontrar el siguiente modo de una escala:
1. Encuentra el bit activo más bajo (la tónica)
2. Quítalo y desplaza el resto del patrón hacia abajo
3. Coloca la antigua tónica arriba, dando la vuelta

Más exactamente, la rotación modal es un **desplazamiento circular a la derecha** igual a la distancia, en semitonos, entre la antigua tónica y la nueva: cada clase de altura p se convierte en (p − n) mod 12, de modo que la nueva tónica cae en el bit 0. En un sistema de 12 bits, «dar la vuelta» significa que los bits que salen por el borde derecho reaparecen por la izquierda. Un desplazamiento circular a la derecha de n equivale a un desplazamiento circular a la izquierda de 12 − n.

Cuidado con la dirección: un desplazamiento circular **a la izquierda** de n suma n a cada clase de altura, lo que **transporta** la escala hacia arriba en lugar de cambiar su modo. Desplazar Do mayor (2741) 2 posiciones a la izquierda da Re mayor (2774); desplazarlo 2 a la derecha da Re dórico llevado a Do, es decir, Do dórico (1709).

### Ejemplo: los modos de la escala mayor

El patrón de la escala mayor tiene los intervalos 2-2-1-2-2-2-1 (siete notas). Sus siete modos se generan rotando hacia cada uno de los siete grados de la escala:

| Nombre del modo | Grado inicial | Patrón interválico |
|-----------|----------------|------------------|
| Jónico (mayor) | 1 | 2-2-1-2-2-2-1 |
| Dórico | 2 | 2-1-2-2-2-1-2 |
| Frigio | 3 | 1-2-2-2-1-2-2 |
| Lidio | 4 | 2-2-2-1-2-2-1 |
| Mixolidio | 5 | 2-2-1-2-2-1-2 |
| Eólico (menor natural) | 6 | 2-1-2-2-1-2-2 |
| Locrio | 7 | 1-2-2-1-2-2-2 |

**No son siete escalas distintas.** Son siete rotaciones del mismo patrón subyacente. Cuando tocas Re dórico en un piano, estás tocando las teclas blancas empezando por Re.

### Calcular rotaciones con operaciones de bits

En pseudocódigo, para rotar `n` posiciones a la izquierda un entero de escala de 12 bits:

```
rotate_left(scale, n):
    shifted = (scale << n) & 0xFFF        # shift left, mask to 12 bits
    wrapped = scale >> (12 - n)           # bits that fell off
    return shifted | wrapped               # combine

mode(scale, n):                           # n = semitones from old root to new root
    return rotate_left(scale, (12 - n) % 12)   # = circular right shift by n
```

Aplicado a la escala mayor (2741), `mode(2741, n)` para n = 0, 2, 4, 5, 7, 9, 11 produce la representación entera de cada modo sobre Do: jónico 2741, dórico 1709, frigio 1451, lidio 2773, mixolidio 1717, eólico 1453, locrio 1387. (`rotate_left(2741, n)` daría en cambio las escalas mayores sobre Re, Mi, Fa...)

### Ejercicio práctico

Calcula los tres primeros modos de la **escala menor armónica** (Do Re Mib Fa Sol Lab Si — intervalos 2-1-2-2-1-3-1).

1. Escribe la representación binaria de 12 bits de Do menor armónica
2. Determina cuántos bits hay que rotar para obtener el 2.º modo (locrio natural 6)
3. Determina cuántos bits hay que rotar para obtener el 3.er modo (jónico #5)

Pista: la cantidad de rotación es igual al número de semitonos entre la antigua tónica y la nueva.

Esbozo de respuesta:
- Do menor armónica = 2477 (binario: 100110101101)
- Rotar a la derecha 2 semitonos (Re está 2 semitonos por encima de Do) → 2.º modo sobre Do: Do Reb Mib Fa Solb La Sib = 1643
- Rotar a la derecha 3 semitonos (Mib está 3 semitonos por encima de Do) → 3.er modo sobre Do: Do Re Mi Fa Sol# La Si = 2869

Los siete modos de la menor armónica son todos rotaciones del entero 2477.

---

## 4. ¿Cuántas son realmente únicas?

Empezamos con **4096** escalas. Pero muchas de ellas son «la misma» bajo distintas equivalencias. ¿Cuántas estructuras son de verdad distintas?

### Formas primas — ignorar la rotación

Dos escalas son **modalmente equivalentes** si una es una rotación de la otra. La **forma prima** de una escala es su representante canónico — por convención, la rotación con el menor valor entero (o la rotación que agrupa las notas hacia el principio).

Bajo la equivalencia modal:
- La familia de la escala mayor de 7 notas tiene 7 rotaciones (7 modos) → 1 forma prima
- La escala de tonos enteros de 6 notas solo tiene 1 rotación única (se transforma en sí misma) → 1 forma prima
- La escala cromática de 12 notas es su propia forma prima

**Contar formas primas:** de las 4096 escalas, exactamente **352** son estructuralmente únicas bajo rotación, contando todas las cardinalidades desde la escala vacía hasta la escala cromática (los 352 collares binarios de 12 cuentas, OEIS A000031).

### Clases de Forte — ignorar la rotación Y la inversión

En la década de 1970, Allen Forte formalizó una equivalencia adicional: tratar una escala y su **inversión** (imagen especular) como la misma estructura. La inversión de una escala invierte su patrón interválico.

- La **escala mayor** (2-2-1-2-2-2-1) se invierte en **frigio** (1-2-2-2-1-2-2) — un momento, eso SÍ es un modo de la mayor.
- Pero la mayoría de las escalas tienen inversiones que NO están en la misma familia modal.

Bajo la **equivalencia T/I** (transposición + inversión), la tabla de Forte recoge **208 clases de conjuntos distintas** para las cardinalidades 3 a 9. Si se añaden las 16 clases de 0, 1, 2, 10, 11 o 12 notas, se obtienen **224 clases de conjuntos** en todas las cardinalidades de 0 a 12.

El **número de Forte** (por ejemplo, «7-35» para la escala diatónica/mayor) es un sistema de nomenclatura normalizado donde:
- Primer número = cardinalidad (número de notas)
- Segundo número = posición ordinal dentro de esa cardinalidad (según un orden canónico)

### El caso especial de los tonos enteros

La escala de tonos enteros (Do Re Mi Fa# Sol# La#) tiene un patrón interválico 2-2-2-2-2-2. Cada rotación produce una escala idéntica — tiene **un solo modo**.

Su entero: 1365 (binario 010101010101).

Rótala un número par de posiciones: vuelves a obtener 1365. Rótala un número impar: obtienes la otra escala de tonos enteros (2730, binario 101010101010).

Así que solo hay **dos escalas de tonos enteros** en todo el universo, y cada una es la transposición de la otra un semitono. Bajo la equivalencia de Forte, ambas pertenecen a la misma clase de conjuntos.

### La jerarquía de recuentos

| Equivalencia | Recuento | Qué se identifica |
|-------------|-------|-----------------|
| Ninguna (en bruto) | 4,096 | Todos los subconjuntos de las 12 clases de altura |
| Transposición (T) | 352 formas primas | Rotaciones del mismo patrón |
| Transposición + inversión (T/I) | 224 clases de Forte | Lo anterior, más las imágenes especulares |
| T/I + complementación | 122 | Lo anterior, más los pares escala + complemento |

### Ejercicio práctico

Convéncete de que la escala de tonos enteros es «modalmente invariante»:

1. Escribe Do tonos enteros en binario de 12 bits: 010101010101
2. Rota 2 bits a la izquierda: ¿qué obtienes?
3. Rota 1 bit a la izquierda: ¿qué obtienes?
4. Explica por qué una escala con estructura interválica uniforme (todos los pasos del mismo tamaño) tiene menos modos únicos

Respuestas:
1. 010101010101 = 1365
2. Rotación de 2 a la izquierda: sigue siendo 010101010101 = 1365 (la misma escala)
3. Rotación de 1 a la izquierda: 101010101010 = 2730 (la otra escala de tonos enteros)
4. Una escala de N notas tiene como máximo N modos, pero si la escala tiene simetría rotacional (se transforma en sí misma al rotar k semitonos con k < 12), tiene menos modos únicos. La escala de tonos enteros se transforma en sí misma al rotar 2 semitonos, así que sus seis modos son la misma escala, y sus rotaciones de cualquier número de semitonos solo producen dos escalas distintas (1365 y 2730).

---

## 5. ¿Qué hace que una escala sea «real»?

De las 4096 posibilidades matemáticas, la mayoría no son útiles para la música. Una escala como `101100000001` (Do, Reb, Mib, Si) es una colección de notas, pero nadie la llamaría escala en sentido práctico. ¿Cómo reducimos el universo a escalas legítimas?

### Los criterios de Zeitler

El catálogo exhaustivo de William Zeitler (allthescales.org) define una escala mediante los criterios 1 y 2; este módulo añade los criterios 3 y 4 como filtros adicionales:

1. **La tónica está presente** — el bit 0 debe estar activo. Una escala debe contener su propia tónica. Esto elimina 2048 escalas (la mitad del universo).

2. **Ningún salto mayor de 4 semitonos** — dos notas consecutivas de la escala no pueden estar a más de una tercera mayor. Un salto de 5 o más semitonos crea un hueco audible que rompe la continuidad de la escala.

3. **Entre 5 y 8 notas** — las escalas fuera de este rango suenan o demasiado dispersas (para oírse como escala) o demasiado densas (para distinguirse del cromatismo). Es una restricción pragmática, no matemática.

4. **Ningún grupo de más de 3 semitonos consecutivos** — cuatro o más notas cromáticas seguidas forman un clúster cromático que pierde el carácter de escala.

Los criterios 1 y 2 reducen por sí solos las 4096 escalas a exactamente **1490**, el recuento de Zeitler. Aplicar los cuatro criterios tal como se enuncian aquí deja **716**. Siguen siendo muchísimas más que el repertorio conocido de escalas con nombre.

### Por qué estos criterios son pautas, no leyes

Los criterios de Zeitler son **heurísticas**, no definiciones. Abundan los contraejemplos:

- La **escala cromática** tiene 12 semitonos consecutivos (incumple el criterio 4) — y es claramente una escala real
- Los **«bordones» de una sola nota** incumplen el mínimo de 5 notas — y son claramente una estructura musical real
- Las **escalas tritónicas y tetratónicas**, habituales en repertorios africanos y en el folclore antiguo, dejan saltos que el criterio 2 prohíbe (Do–Mib–Sol avanza 3, luego 4 y luego 5 semitonos de Sol a Do) — son claramente escalas reales
- Las **escalas del gagaku**, las escalas microtonales y otros sistemas no occidentales no encajan en absoluto en el 12-TET

Los criterios son **específicos de una cultura** — describen escalas que encajan en la práctica tonal y modal europea. Son un filtro útil, no una verdad universal.

### Ejercicio práctico

Para cada una de las escalas siguientes, determina qué criterios de Zeitler incumple (si incumple alguno):

1. **Do mayor** (0, 2, 4, 5, 7, 9, 11)
2. **Do cromática** (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
3. **Una escala con hueco** (0, 5, 11) — Do, Fa, Si
4. **Una escala en clúster** (0, 1, 2, 3, 4) — Do, Do#, Re, Re#, Mi

Respuestas:
1. Do mayor: no incumple ninguno — cumple todos los criterios
2. Do cromática: incumple el criterio 3 (12 notas, supera el máximo de 8) y el criterio 4 (12 semitonos consecutivos)
3. Escala con hueco: incumple el criterio 2 (saltos de 5 semitonos de Do a Fa y de 6 de Fa a Si) y el criterio 3 (solo 3 notas)
4. Escala en clúster: incumple el criterio 4 (5 semitonos consecutivos) y el criterio 2 (salto de 8 semitonos de Mi hasta el Do siguiente); sus 5 notas cumplen el criterio 3

---

## 6. Propiedades de una escala que puedes calcular

Una vez que una escala es un entero, todas sus propiedades musicales se vuelven calculables. No necesitas escuchar — puedes analizar el número.

### Vector interválico

Un **vector interválico** cuenta cuántas veces aparece cada clase interválica en la escala. El vector tiene seis entradas, una por clase interválica de 1 a 6 semitonos (el tritono es su propia inversión, y los intervalos 7-11 son complementos de 1-5).

Para la **escala de Do mayor** (Do Re Mi Fa Sol La Si):

```
Interval class: 1   2   3   4   5   6
Count:          2   5   4   3   6   1
```

Vector interválico: `[2, 5, 4, 3, 6, 1]`

El vector se calcula examinando todos los pares de notas de la escala y contando la distancia entre ellas (reducida al rango 1-6).

**Por qué importa:** el vector interválico codifica el potencial armónico. Las escalas con muchas terceras y quintas (clases interválicas 3, 4, 5) suenan consonantes y tonales. Las escalas cargadas de clases interválicas 1 y 6 suenan disonantes e inestables.

### Brillo

El **brillo** es la suma de las clases de altura (posiciones de bits activos). Sumas más altas significan que las notas de la escala están más arriba en el círculo cromático (más sostenidos); sumas más bajas significan más bemoles.

- Do mayor (0, 2, 4, 5, 7, 9, 11): suma = 38
- Do lidio (0, 2, 4, 6, 7, 9, 11): suma = 39 — una unidad más brillante
- Do frigio (0, 1, 3, 5, 7, 8, 10): suma = 34 — más oscuro

El **espectro de locrio a lidio** (del modo más oscuro al más brillante de la escala mayor) corresponde a valores de brillo monótonamente crecientes. Es una propiedad calculada — no hace falta oído.

### Simetría

Una escala tiene **simetría rotacional** si al rotarla k semitonos se obtiene la misma escala. El orden de simetría de la escala te dice cuántas transposiciones distintas tiene.

- **Escala de tonos enteros:** simetría cada 2 semitonos → solo 2 transposiciones distintas
- **Escala disminuida (octatónica):** simetría cada 3 semitonos → solo 3 transposiciones distintas
- **Escala aumentada:** simetría cada 4 semitonos → solo 4 transposiciones distintas
- **Escala mayor:** sin simetría rotacional → las 12 transposiciones son distintas

### Quiralidad

Una escala es **quiral** si su inversión (imagen especular alrededor de la clase de altura 0) NO coincide con ninguna rotación de sí misma. La mayoría de las escalas son quirales. Entre las excepciones están la escala mayor (cuya inversión es el modo frigio, que SÍ es una rotación) y las escalas simétricas.

### Relación Z

Dos escalas están en **relación Z** si tienen el mismo vector interválico pero NO están relacionadas por transposición o inversión. Suenan parecidas armónicamente pero son estructuralmente distintas. Los pares en relación Z son raros y musicalmente fascinantes.

El par Z más famoso: la relación Z de los **tetracordios de todos los intervalos** `{0,1,4,6}` y `{0,1,3,7}`, ambos con vector interválico `[1,1,1,1,1,1]`.

### Ejercicio práctico

Calcula el vector interválico de la **escala pentatónica menor de Do** (Do Mib Fa Sol Sib = clases de altura 0, 3, 5, 7, 10).

Paso 1: enumera todos los pares y sus distancias.
Paso 2: reduce las distancias a clases interválicas (las distancias 7-11 pasan a ser 12 − distancia: p. ej., 8 semitonos → clase 4).
Paso 3: cuenta las apariciones de cada clase.

Respuesta:
Pares y distancias:
- 0-3: 3
- 0-5: 5
- 0-7: 5 (7 se reduce a 5)
- 0-10: 2 (10 se reduce a 2)
- 3-5: 2
- 3-7: 4
- 3-10: 5 (7 se reduce a 5)
- 5-7: 2
- 5-10: 5
- 7-10: 3

Recuento por clase interválica:
- Clase 1: 0
- Clase 2: 3
- Clase 3: 2
- Clase 4: 1
- Clase 5: 4
- Clase 6: 0

Vector interválico: **[0, 3, 2, 1, 4, 0]**

Nota: mucha clase 5 (cuartas/quintas justas) y ausencia de la clase 6 (tritono) y de la clase 1 (semitono) — por eso las escalas pentatónicas suenan estables y «nunca desafinan».

---

## 7. Explorar escalas sin nombre en la guitarra

Los libros de teoría musical cubren quizá **200 escalas con nombre**: mayor, menor, modos, pentatónicas, menor armónica y melódica y sus modos, disminuida, tonos enteros, blues, escalas bebop, un puñado de «exóticas» (húngara, bizantina, etc.) y los modos de Messiaen.

Eso deja **aproximadamente 1300 escalas sin nombre** entre las 1490 que cumplen los criterios básicos de Zeitler (unas 500 entre las 716 que superan los cuatro). La inmensa mayoría del universo de las escalas es territorio inexplorado.

### Cómo explorar

1. **Elige un número** entre 1 y 4095 (o usa un generador aleatorio)
2. **Decodifica los bits** para averiguar qué clases de altura están en la escala
3. **Comprueba los criterios de Zeitler** — ¿es «razonable» esta escala?
4. **Tócala** en tu instrumento y escucha
5. **Anota el vector interválico** y compáralo con escalas que conozcas

### Fórmula de asignación al diapasón

Para tocar un entero de escala en la guitarra, necesitas asignar las clases de altura a posiciones de traste en cada cuerda.

Datos:
- Entero de escala S
- Clases de altura de las cuerdas al aire en afinación estándar: Mi(4), La(9), Re(2), Sol(7), Si(11), Mi(4)
- Para cada cuerda, calcula qué trastes (0-12) contienen una nota de la escala

**Fórmula:** para cada traste f (de 0 a 12) en una cuerda cuya clase de altura al aire es p:

```
pitch_class_at_fret = (p + f) mod 12
is_in_scale = (S >> pitch_class_at_fret) & 1
```

Si el resultado es 1, marca ese traste. Repite para las seis cuerdas.

### Ejemplo: una escala al azar

Elige el entero de escala **1749**. Decodifica:

```
1749 in binary: 011011010101
Pitch classes (reading bits 0-11): 0, 2, 4, 6, 7, 9, 10
Notes from C:                     C, D, E, F#, G, A, Bb
```

Esta escala tiene 7 notas, contiene Do (la tónica está presente), su salto máximo es de 2 semitonos y no tiene clústeres largos — cumple los criterios de Zeitler.

Patrón interválico: 2-2-2-1-2-1-2 (suma 12).

**Es mixolidio #11** (o lidio dominante, el 4.º modo de la menor melódica) — ¡una escala con nombre! Acabas de redescubrirla eligiendo un número.

Prueba un número menos explorado: **2391**. Decodifica:

```
2391 in binary: 100101010111
Pitch classes: 0, 1, 2, 4, 6, 8, 11
Notes from C: C, C#, D, E, F#, G#, B
```

Cumple tres criterios de Zeitler (tónica presente, salto máximo de 3 semitonos, 7 notas) pero falla el criterio 4: Si, Do, Do#, Re son cuatro semitonos consecutivos, dando la vuelta de Si a Do. Tampoco es una escala que tenga un nombre común. Los criterios son heurísticas, así que tócala igualmente en la guitarra. Escucha. Ponle un nombre.

### El protocolo de exploración

1. Genera de 5 a 10 números de escala aleatorios que cumplan los criterios de Zeitler
2. Toca cada una durante 30 segundos, atento a su carácter emocional
3. Anota tus favoritas
4. Construye melodías sencillas usando el sabor interválico propio de cada escala
5. Compáralas con escalas con nombre que tengan vectores interválicos parecidos

Así es como se descubre música nueva. El universo está ahí; la asignación es mecánica; el juicio musical es tuyo.

### Ejercicio práctico

Toma el entero de escala **1709** (Do dórico).

1. Conviértelo a binario e identifica las clases de altura
2. Escribe la escala empezando en Do
3. Calcula el patrón interválico (los pasos entre notas consecutivas)
4. Lleva la escala a las dos cuerdas más agudas de una guitarra en afinación estándar (1.ª cuerda = Mi, 2.ª cuerda = Si) en los trastes 0-12

Pista: 1709 = 1024 + 512 + 128 + 32 + 8 + 4 + 1 → bits 0, 2, 3, 5, 7, 9, 10.

---

## 8. Conexión con OPTIC-K

La teoría de conjuntos musical usa una taxonomía de **relaciones de equivalencia** para describir cómo dos colecciones de notas pueden considerarse «la misma». La regla mnemotécnica OPTIC las reúne todas. El marco de los enteros de escala hace que estas equivalencias sean calculables.

### Las cinco equivalencias

| Letra | Nombre | Significado | Operación |
|--------|------|---------|-----------|
| **O** | Octava | Las notas en octavas distintas son equivalentes | Reducir a clase de altura (mod 12) |
| **P** | Permutación | El orden de las notas no importa | Tratar como conjunto |
| **T** | Transposición | El mismo patrón empezando en otra tónica | Rotación modular |
| **I** | Inversión | Imagen especular alrededor de un pivote | Invertir el orden de los intervalos |
| **C** | Cardinalidad | Número de clases de altura distintas | POPCOUNT del entero |

(OPTIC, sin K, designa las cinco equivalencias definidas por Callender, Quinn y Tymoczko, «Generalized Voice-Leading Spaces», *Science* 320, 2008. La «-K» pertenece al embedding OPTIC-K de Guitar Alchemist, no a ese artículo.)

### Dónde vive cada equivalencia en el marco

- **Equivalencia O:** integrada en el modelo. Al reducir las notas a las clases de altura 0-11, se descarta la información de octava.
- **Equivalencia P:** integrada en el modelo. Un entero de 12 bits es por construcción un conjunto (independiente del orden).
- **Equivalencia T:** se calcula como rotación (desplazamiento circular) del entero.
- **Equivalencia I:** se calcula como **inversión del orden de los bits** del entero de 12 bits. Invertir el orden de los bits de la escala S da su escala invertida (y luego se rota para devolver la tónica al bit 0).
- **Equivalencia C:** se calcula con POPCOUNT — el número de bits a 1.

### Las 224 clases de Forte

Bajo la equivalencia combinada T e I (la taxonomía estándar de Forte), las 4096 escalas se reducen a **224 clases distintas**. Estas clases forman la base de la teoría de conjuntos musical del siglo XX.

Cada clase de Forte tiene una forma prima canónica (el representante lexicográficamente menor tras la normalización). El libro de Forte de 1973, **«The Structure of Atonal Music»**, tabula las 208 clases de 3 a 9 notas con sus vectores interválicos, simetrías y relaciones Z; las 16 clases restantes (0, 1, 2, 10, 11 y 12 notas) completan las 224.

### El espacio vectorial de 216 dimensiones de GA

Guitar Alchemist representa las escalas como vectores de características en un espacio de 216 dimensiones. Las dimensiones codifican:

- Cardinalidad (1 dimensión)
- Vector interválico (6 dimensiones)
- Brillo (1 dimensión)
- Posiciones modales (variable)
- Contenido de acordes (variable)
- Métricas de tocabilidad específicas de la guitarra (variable)
- Pertenencia a clases de equivalencia OPTIC-K (variable)

Dos escalas cercanas en este espacio de 216 dimensiones comparten carácter musical. El espacio es navegable: puedes ir de la escala mayor hacia el lidio caminando en una dirección concreta; puedes encontrar la escala «sin nombre» más cercana a una con nombre; puedes calcular distancias armónicas entre escalas cualesquiera.

El entero de escala es el **índice** en este espacio vectorial. Dado el entero S, GA calcula de forma determinista el vector de características completo de 216 dimensiones.

### La recompensa

El universo de las escalas es:
- **Finito** (4096 escalas)
- **Enumerable** (enteros de 0 a 4095)
- **Transformable** (operaciones de bits para modos, inversiones, complementos)
- **Calculable** (toda propiedad se deriva del entero)
- **Navegable** (distancias y vecindarios en el espacio de características)
- **Mayormente inexplorado** (solo ~200 de ~1500 escalas legítimas tienen nombre)

La teoría musical no tenía por qué ser difusa. La teoría de conjuntos de clases de altura, combinada con la computación moderna, convierte las escalas de folclore en datos.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Clase de altura** | La identidad de una nota con independencia de la octava (Do, Do#, Re, ... Si) |
| **12-TET** | Temperamento igual de doce tonos — el sistema de afinación occidental estándar |
| **Entero de escala** | Un número de 12 bits en el que cada bit indica la presencia o ausencia de una clase de altura |
| **Modo** | Una rotación de una escala que toma un grado distinto de la tónica como nueva tónica |
| **Forma prima** | El representante canónico de una familia de escalas bajo una equivalencia |
| **Número de Forte** | Una etiqueta normalizada (p. ej., 7-35) para una clase de conjuntos de clases de altura |
| **Vector interválico** | Una 6-tupla que cuenta las apariciones de cada clase interválica en una escala |
| **Clase interválica** | Un intervalo reducido módulo la octava y la inversión: n y 12 − n semitonos son la misma clase (1 y 11 son ambos clase 1, 5 y 7 ambos clase 5). La clase 0 es el unísono, de modo que las clases que cuenta un vector interválico van de 1 a 6 |
| **Brillo** | La suma de las clases de altura de una escala (indicador de sostenidos/bemoles) |
| **Simetría (rotacional)** | Propiedad de una escala que se transforma en sí misma bajo rotación |
| **Quiralidad** | La asimetría de una escala bajo inversión |
| **Relación Z** | Dos escalas con el mismo vector interválico pero no relacionadas por T ni por I |
| **Criterios de Zeitler** | Heurísticas para filtrar las escalas matemáticas y quedarse con las «musicalmente reales» |
| **POPCOUNT** | El número de bits activos en un número binario (= cardinalidad de la escala) |
| **OPTIC-K** | Regla mnemotécnica de las relaciones de equivalencia en la teoría de conjuntos musical |

---

## Autoevaluación

**1. Convierte la escala de Do dórico (Do Re Mib Fa Sol La Sib) en su entero de clases de altura usando la convención de asignación de bits.**
> Clases de altura: 0, 2, 3, 5, 7, 9, 10. Entero = 1 + 4 + 8 + 32 + 128 + 512 + 1024 = **1709**.

**2. Calcula el vector interválico de la escala de tonos enteros de Do (Do Re Mi Fa# Sol# La#).**
> Los pares solo dan intervalos de 2, 4 y 6 semitonos. Recuento: clase 1 = 0, clase 2 = 6, clase 3 = 0, clase 4 = 6, clase 5 = 0, clase 6 = 3. Vector interválico: **[0, 6, 0, 6, 0, 3]**.

**3. ¿Cuál es el número de Forte de la escala mayor (colección diatónica) y cuántas notas tiene?**
> Número de Forte **7-35**. La primera cifra (7) indica la cardinalidad = 7 notas.

**4. Explica por qué los siete modos de la escala mayor NO son siete escalas distintas bajo la equivalencia por transposición.**
> Los siete modos contienen las mismas siete clases de altura dispuestas en el mismo patrón interválico cíclico (2-2-1-2-2-2-1). Cada modo es una rotación de los demás — comparten una forma prima. Empezar el patrón en otro grado no cambia la estructura subyacente de la escala, solo la elección de la tónica.

**5. Aplica el filtro de Zeitler a la escala con clases de altura {0, 1, 7}. ¿Qué criterios cumple o incumple?**
> Tónica presente (bit 0 activo): CUMPLE. Salto máximo de 1 a 7 de 6 semitonos: FALLA (supera 4). Cardinalidad = 3 notas: FALLA (por debajo del mínimo de 5). Ningún clúster de 4 o más semitonos: CUMPLE. Balance: no pasa el filtro de Zeitler como escala «legítima» (es un tricordio, no una escala).

**Criterios de aprobación:** convertir cualquier escala (dada como clases de altura o nombres de notas) a y desde su representación entera, calcular a mano su vector interválico, identificar su cardinalidad de Forte y explicar qué equivalencias OPTIC-K están integradas en el modelo entero y cuáles requieren un cálculo adicional.

---

## Base de investigación

- El temperamento igual de 12 tonos como estándar de afinación occidental está documentado empíricamente en la afinación de pianos y en la práctica orquestal desde el siglo XIX
- La teoría de conjuntos de clases de altura y la enumeración de las 4096 escalas se originan en el trabajo combinatorio de Milton Babbitt (década de 1950) y fueron formalizadas por Allen Forte en *The Structure of Atonal Music* (1973)
- Las 224 clases de conjuntos bajo la equivalencia T/I (todas las cardinalidades, de 0 a 12; OEIS A000029 las cuenta como los 224 brazaletes binarios de 12 cuentas) incluyen las 208 clases de 3 a 9 notas tabuladas en Forte (1973), que siguen siendo la taxonomía estándar
- Los criterios de escalas de Zeitler proceden del proyecto de catalogación exhaustiva de William Zeitler (*All The Scales*, 2011, y su sitio web complementario), y representan un filtro práctico sobre el universo
- La geometría de las escalas y las relaciones de vecindad se exploran en *A Geometry of Music* (2011) de Dmitri Tymoczko, que formaliza las distancias de conducción de voces entre acordes y escalas
- La representación de GA en un espacio de características de 216 dimensiones es una decisión de implementación de Guitar Alchemist, que amplía la teoría clásica de conjuntos de clases de altura con metadatos de interpretación y de función armónica
- Las relaciones de equivalencia OPTIC se definen en Clifton Callender, Ian Quinn y Dmitri Tymoczko, «Generalized Voice-Leading Spaces», *Science* 320 (2008): 346–348; *Generalized Musical Intervals and Transformations* (1987) de David Lewin pertenece a la tradición transformacional, distinta
- Fuentes: Forte (1973); Tymoczko (2011); Callender, Quinn y Tymoczko (2008); Lewin (1987); Rahn, *Basic Atonal Theory* (1980); catálogo de escalas de Zeitler (2011)
- Estado de creencia: T(0.85) F(0.03) U(0.08) C(0.04)
