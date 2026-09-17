---
module_id: mus-006-the-scale-universe
department: music
course: "Fundamentos de teoría musical"
level: intermediate
alchemical_stage: albedo
prerequisites:
  - mus-001-what-is-a-chord
estimated_duration: "45 minutos"
produced_by: music
version: "1.0.0"
---

# El universo de las escalas: 4096 posibilidades a partir de 12 notas

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración: 45 minutos

## Objetivos

Al terminar esta lección serás capaz de:

- Representar cualquier escala como un número binario de 12 bits y convertirlo en un entero decimal
- Explicar por qué existen exactamente 4096 escalas matemáticamente posibles en el temperamento igual de 12 sonidos
- Calcular los modos de cualquier escala mediante desplazamientos circulares a la izquierda (rotaciones de bits)
- Distinguir el recuento total (4096) de los recuentos obtenidos bajo distintas equivalencias (formas primas, clases de Forte)
- Aplicar los criterios de Zeitler para filtrar el universo y quedarte solo con las escalas «musicalmente reales»
- Calcular vectores de intervalos, brillo y propiedades de simetría a partir del entero de una escala
- Trasladar cualquier entero de escala a las posiciones del mástil de la guitarra
- Relacionar el espacio de escalas con las relaciones de equivalencia OPTIC-K empleadas en la teoría de conjuntos musicales

---

## 1. El alfabeto cromático

La música occidental emplea doce clases de altura por octava. Una **clase de altura** es una nota con independencia de la octava en que aparezca: todos los do de un piano pertenecen a la misma clase de altura.

Las doce clases de altura, numeradas de 0 a 11:

| Clase de altura | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-------------|---|---|---|---|---|---|---|---|---|---|----|----|
| Nombre de nota | do | do♯/re♭ | re | re♯/mi♭ | mi | fa | fa♯/sol♭ | sol | sol♯/la♭ | la | la♯/si♭ | si |

Piensa ahora en una escala como una **elección**: para cada una de las doce clases de altura, o bien está **dentro** de la escala (1), o bien está **fuera** (0). Eso nos da un número binario de 12 bits: doce decisiones sí/no independientes.

**¿Cuántas elecciones posibles hay?** Dos opciones para cada una de las doce posiciones:

$$ 2^{12} = 4096 $$

Existen exactamente 4096 escalas matemáticamente posibles en el temperamento igual de 12 sonidos. Eso incluye la escala vacía (todo ceros), la escala cromática (todo unos), todas las «escalas» de una sola nota, todas las escalas tradicionales y cualquier colección extraña que haya entre medias.

Ese es el **universo de las escalas**. Su tamaño es finito, conocible y sorprendentemente pequeño: un número que un ordenador enumera en microsegundos.

---

## 2. Una escala ES un número

He aquí el replanteamiento decisivo: **toda escala es un entero entre 0 y 4095**.

### La asignación de bits

Se asigna a cada clase de altura una posición binaria:

| Bit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| Clase de altura | do | do♯ | re | re♯ | mi | fa | fa♯ | sol | sol♯ | la | la♯ | si |
| Valor posicional | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |

Para convertir una escala en un entero, se marca cada nota con un 1 y se suman los valores posicionales.

### Ejemplo: la escala mayor

La **escala de do mayor** contiene las notas do, re, mi, fa, sol, la, si — clases de altura 0, 2, 4, 5, 7, 9, 11.

En binario (leído del bit 11 al bit 0):

```
Bit:        11 10  9  8  7  6  5  4  3  2  1  0
Nota:        si si♭ la la♭ sol sol♭ fa mi mi♭ re re♭ do
En la escala: 1  0  1  0  1  0  1  1  0  1  0  1
```

En decimal:

$$ 1 + 4 + 16 + 32 + 128 + 512 + 2048 = 2741 $$

**do mayor = 2741.**

Toda escala mayor tiene la misma **estructura interválica**, de modo que, sea cual sea la fundamental, es el patrón (pasos de 2-2-1-2-2-2-1 semitonos) lo que define el modo mayor. El entero 2741 es su representación con raíz en do. Con raíz en otras notas, el patrón rota.

### Ejemplo: la escala pentatónica menor

La escala **pentatónica menor de do** contiene do, mi♭, fa, sol, si♭ — clases de altura 0, 3, 5, 7, 10.

En binario:

```
Bit:        11 10  9  8  7  6  5  4  3  2  1  0
En la escala: 0  1  0  0  1  0  1  0  1  0  0  1
```

En decimal:

$$ 1 + 8 + 32 + 128 + 1024 = 1193 $$

**pentatónica menor de do = 1193.**

### Por qué esto importa

Una vez aceptas que una escala es un número, todo se sigue de ahí:
- Puedes **enumerar** todas las escalas (contar de 0 a 4095)
- Puedes **comparar** escalas (comparación de enteros)
- Puedes **transformar** escalas (operaciones de bits: desplazamiento, Y, O, O exclusivo, POPCOUNT)
- Puedes **buscar** escalas (por vector de intervalos, cardinalidad o simetría concretos)
- Puedes **almacenar** escalas (12 bits en lugar de una lista de notas)

Una escala no es algo místico. Es un número.

### Ejercicio práctico

Convierte las tres escalas siguientes en enteros mediante la asignación de bits:

1. **do menor natural** (do, re, mi♭, fa, sol, la♭, si♭) — clases de altura 0, 2, 3, 5, 7, 8, 10
2. **do pentatónico mayor** (do, re, mi, sol, la) — clases de altura 0, 2, 4, 7, 9
3. **do por tonos** (do, re, mi, fa♯, sol♯, la♯) — clases de altura 0, 2, 4, 6, 8, 10

Calcula cada una sumando los valores posicionales (potencias de 2). Comprueba tus respuestas abajo.

Respuestas:
1. do menor natural = 1 + 4 + 8 + 32 + 128 + 256 + 1024 = **1453**
2. do pentatónico mayor = 1 + 4 + 16 + 128 + 512 = **661**
3. do por tonos = 1 + 4 + 16 + 64 + 256 + 1024 = **1365**

---

## 3. Los modos como rotaciones

Un **modo** es una escala comenzada en otro grado. Do dórico contiene las mismas notas que si♭ mayor, pero empieza en do. En la representación entera esto no es una suma ni una multiplicación: es una **rotación**.

### La operación de desplazamiento circular

Para hallar el siguiente modo de una escala:
1. Localizar el bit a 1 más bajo (la fundamental)
2. Quitarlo y desplazar hacia abajo el patrón restante
3. Llevar la antigua fundamental a lo alto

Con más precisión, la rotación modal es un **desplazamiento circular a la izquierda** por la distancia que separa la fundamental de la siguiente nota de la escala. En un sistema de 12 bits, «dar la vuelta» significa que los bits que salen por el borde izquierdo reaparecen por la derecha.

### Ejemplo: los modos de la escala mayor

El patrón de la escala mayor tiene los intervalos 2-2-1-2-2-2-1 (siete notas). Sus siete modos se generan rotando a cada uno de los siete grados:

| Nombre del modo | Grado de partida | Patrón de intervalos |
|-----------|----------------|------------------|
| Jónico (mayor) | 1 | 2-2-1-2-2-2-1 |
| Dórico | 2 | 2-1-2-2-2-1-2 |
| Frigio | 3 | 1-2-2-2-1-2-2 |
| Lidio | 4 | 2-2-2-1-2-2-1 |
| Mixolidio | 5 | 2-2-1-2-2-1-2 |
| Eólico (menor natural) | 6 | 2-1-2-2-1-2-2 |
| Locrio | 7 | 1-2-2-1-2-2-2 |

**No son siete escalas distintas.** Son siete rotaciones del mismo patrón subyacente. Cuando tocas do dórico en un piano, estás tocando las teclas blancas empezando en re.

### Calcular las rotaciones como operaciones binarias

En pseudocódigo, para rotar `n` posiciones a la izquierda un entero de escala de 12 bits:

```
rotacion_izquierda(escala, n):
    desplazado = (escala << n) & 0xFFF    # desplazar a la izquierda, enmascarar a 12 bits
    arrastrado = escala >> (12 - n)       # bits que se salieron
    return desplazado | arrastrado        # combinación
```

Aplicada a la escala mayor (2741), una rotación del número correcto de posiciones produce la representación entera de cada modo.

### Ejercicio práctico

Calcula los tres primeros modos de la **escala menor armónica** (do re mi♭ fa sol la♭ si — intervalos 2-1-2-2-1-3-1).

1. Escribe la representación binaria de 12 bits de do menor armónico
2. Determina cuántos bits hay que rotar para obtener el 2.º modo (locrio 6.ª natural)
3. Determina cuántos bits hay que rotar para obtener el 3.er modo (jónico ♯5)

Pista: la cantidad de rotación es igual al número de semitonos entre la antigua y la nueva fundamental.

Esbozo de respuesta:
- do menor armónico = 2477 (binario: 100110101101)
- Rotar a la izquierda 2 semitonos (re está 2 semitonos por encima de do) → 2.º modo
- Rotar a la izquierda 3 semitonos (mi♭ está 3 semitonos por encima de do) → 3.er modo

Los siete modos de la menor armónica son todos rotaciones del entero 2477.

---

## 4. ¿Cuántas son realmente únicas?

Partimos de **4096** escalas. Pero muchas de ellas son «la misma» bajo distintas equivalencias. ¿Cuántas estructuras son realmente distintas?

### Formas primas: ignorando la rotación

Dos escalas son **modalmente equivalentes** si una es rotación de la otra. La **forma prima** de una escala es su representante canónico: por convención, la rotación con el menor valor entero (o la que comprime las notas hacia el comienzo).

Bajo la equivalencia modal:
- La familia de la escala mayor de 7 notas tiene 7 rotaciones (7 modos) → 1 forma prima
- La escala por tonos de 6 notas tiene una sola rotación única (se transforma en sí misma) → 1 forma prima
- La escala cromática de 12 notas es su propia forma prima

**Recuento de formas primas:** de las 4096 escalas, aproximadamente **352** son estructuralmente únicas bajo rotación. El recuento exacto depende de las convenciones (si se incluye o no la escala vacía, las escalas de una sola nota, etc.).

### Clases de Forte: ignorando la rotación Y la inversión

En los años setenta, Allen Forte formalizó una equivalencia adicional: tratar una escala y su **inversión** (imagen especular) como la misma estructura. La inversión de una escala invierte su patrón de intervalos.

- La **escala mayor** (2-2-1-2-2-2-1) se invierte en **frigio** (1-2-2-2-1-2-2), que es precisamente un modo del mayor.
- Pero la mayoría de las escalas tienen inversiones que NO pertenecen a la misma familia modal.

Bajo la **equivalencia T/I** (transposición + inversión), Forte identificó **224 clases de conjuntos distintas** para las cardinalidades de 3 a 9. Incluyendo todas las cardinalidades de 0 a 12, el recuento total es algo mayor.

El **número de Forte** (por ejemplo, «7-35» para la escala diatónica/mayor) es un sistema de denominación normalizado en el que:
- El primer número es la cardinalidad (el número de notas)
- El segundo es la posición ordinal dentro de esa cardinalidad (según un orden canónico)

### El caso especial de la escala por tonos

La escala por tonos (do re mi fa♯ sol♯ la♯) tiene un patrón de intervalos 2-2-2-2-2-2. Cada rotación produce una escala idéntica: tiene **un solo modo**.

Su entero: 1365 (binario 010101010101).

Rótala un número par de posiciones: vuelves a obtener 1365. Rótala un número impar: obtienes la otra escala por tonos (2730, binario 101010101010).

Por tanto, solo existen **dos escalas por tonos** en todo el universo, y son transposición una de la otra por un semitono. Bajo la equivalencia de Forte, ambas pertenecen a la misma clase de conjuntos.

### La jerarquía de recuentos

| Equivalencia | Recuento | Qué se identifica |
|-------------|-------|-----------------|
| Ninguna (en bruto) | 4096 | Todos los subconjuntos de las 12 clases de altura |
| Transposición (T) | ~352 formas primas | Rotaciones de un mismo patrón |
| Transposición + inversión (T/I) | 224 clases de Forte | Lo anterior, más las imágenes especulares |
| T/I + complementación | ~158 | Lo anterior, más los pares escala+complemento |

### Ejercicio práctico

Convéncete de que la escala por tonos es «modalmente invariante»:

1. Escribe do por tonos en binario de 12 bits: 010101010101
2. Rota 2 bits a la izquierda: ¿qué obtienes?
3. Rota 1 bit a la izquierda: ¿qué obtienes?
4. Explica por qué una escala de estructura interválica uniforme (todos los pasos del mismo tamaño) tiene menos modos únicos

Respuestas:
1. 010101010101 = 1365
2. Rotación a la izquierda de 2: sigue siendo 010101010101 = 1365 (la misma escala)
3. Rotación a la izquierda de 1: 101010101010 = 2730 (la otra escala por tonos)
4. Una escala de N notas tiene como mucho N modos, pero si posee simetría de rotación (se transforma en sí misma al rotar k semitonos con k < 12), tiene menos. La escala por tonos tiene un periodo de simetría de rotación de 12/6 = 2, de modo que todas las rotaciones producen uno de dos estados.

---

## 5. ¿Qué hace que una escala sea «real»?

De las 4096 posibilidades matemáticas, la mayoría no son útiles para la música. Una escala como `101100000001` (do, re♭, mi♭, si) es una colección de notas, pero nadie la llamaría escala en sentido práctico. ¿Cómo filtrar el universo para quedarnos con las escalas legítimas?

### Los criterios de Zeitler

William Zeitler, en su trabajo de catalogación exhaustiva, propuso cuatro criterios para que una escala sea «real»:

1. **La fundamental está presente**: el bit 0 debe estar a 1. Una escala debe contener su propia tónica. Esto elimina 2048 escalas (la mitad del universo).

2. **Ningún hueco mayor de 4 semitonos**: dos notas consecutivas de la escala no pueden distar más de una tercera mayor. Un hueco de 5 semitonos o más crea un vacío audible que rompe la continuidad escalar.

3. **Entre 5 y 8 notas**: las escalas fuera de ese rango suenan demasiado dispersas (para oírse como escalas) o demasiado densas (para distinguirse del cromatismo). Es una restricción pragmática, no matemática.

4. **Ningún racimo de más de 3 semitonos consecutivos**: cuatro o más notas cromáticas seguidas crean un racimo cromático que pierde su carácter escalar.

Aplicar los cuatro criterios reduce las 4096 escalas a unas **1490 escalas «legítimas»**. Siguen siendo muchísimas más que el repertorio familiar de escalas con nombre.

### Por qué estos criterios son pautas y no leyes

Los criterios de Zeitler son **heurísticas**, no definiciones. Abundan los contraejemplos:

- La **escala cromática** tiene 12 semitonos consecutivos (viola el criterio 4) y es claramente una escala real
- Los **bordones** de una sola nota violan el mínimo de 5 notas y son claramente una estructura musical real
- Las **escalas de blues** aprovechan a veces con habilidad huecos de 3 semitonos (la pentatónica menor presenta un hueco de si♭ a do)
- Las **escalas del gagaku**, las escalas microtonales y otros sistemas no occidentales no encajan en absoluto en el temperamento igual de 12 sonidos

Los criterios son **propios de una cultura**: describen escalas que encajan en la práctica tonal y modal europea. Son un filtro útil, no una verdad universal.

### Ejercicio práctico

Para cada una de las escalas siguientes, determina qué criterios de Zeitler viola, si es que viola alguno:

1. **do mayor** (0, 2, 4, 5, 7, 9, 11)
2. **do cromático** (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
3. **una escala con hueco** (0, 5, 11) — do, fa, si
4. **una escala en racimo** (0, 1, 2, 3, 4) — do, do♯, re, re♯, mi

Respuestas:
1. do mayor: no viola ninguno — cumple todos los criterios
2. do cromático: viola el criterio 3 (12 notas, por encima del máximo de 8) y el criterio 4 (12 semitonos consecutivos)
3. Escala con hueco: viola el criterio 2 (el hueco de fa a si es de 6 semitonos) y el criterio 3 (solo 3 notas)
4. Escala en racimo: viola el criterio 4 (5 semitonos consecutivos) y el criterio 3 (solo 5 notas, en el límite)

---

## 6. Propiedades de escala que puedes calcular

En cuanto una escala es un entero, todas sus propiedades musicales se vuelven calculables. No necesitas escuchar: puedes analizar el número.

### Vector de intervalos

Un **vector de intervalos** cuenta cuántas veces aparece cada clase de intervalo en la escala. Hay seis clases de intervalo (de 1 a 6 semitonos; el tritono es su propio inverso, y los intervalos de 7 a 11 son los complementos de los de 1 a 5).

Para la **escala de do mayor** (do re mi fa sol la si):

```
Clase de intervalo: 1   2   3   4   5   6
Recuento:           2   5   4   3   6   1
```

Vector de intervalos: `[2, 5, 4, 3, 6, 1]`

El vector se calcula examinando todos los pares de notas de la escala y contando la distancia entre ellas (reducida al rango 1-6).

**Por qué importa:** el vector de intervalos codifica el potencial armónico. Las escalas ricas en terceras y quintas (clases de intervalo 3, 4, 5) suenan consonantes y tonales. Las escalas cargadas de clases 1 y 6 suenan disonantes e inestables.

### Brillo

El **brillo** es la suma de las clases de altura (las posiciones binarias a 1). Una suma mayor significa que las notas de la escala están más arriba en el círculo cromático (más sostenidos); una suma menor significa más bemoles.

- do mayor (0, 2, 4, 5, 7, 9, 11): suma = 38
- do lidio (0, 2, 4, 6, 7, 9, 11): suma = 39 — más brillante en una unidad
- do frigio (0, 1, 3, 5, 7, 8, 10): suma = 34 — más oscuro

El **espectro locrio-lidio** (del más oscuro al más brillante de los modos del mayor) se corresponde con valores de brillo crecientes de manera monótona. Es una propiedad calculada: no hace falta oído.

### Simetría

Una escala tiene **simetría de rotación** si al rotarla k semitonos se obtiene la misma escala. El orden de simetría de la escala indica cuántas transposiciones distintas admite.

- **Escala por tonos:** simetría cada 2 semitonos → solo 2 transposiciones distintas
- **Escala disminuida (octatónica):** simetría cada 3 semitonos → solo 3 transposiciones distintas
- **Escala aumentada:** simetría cada 4 semitonos → solo 4 transposiciones distintas
- **Escala mayor:** sin simetría de rotación → las 12 transposiciones son distintas

### Quiralidad

Una escala es **quiral** si su inversión (imagen especular en torno a la clase de altura 0) NO coincide con ninguna de sus rotaciones. La mayoría de las escalas son quirales. Son excepción la escala mayor (cuya inversión es el modo frigio, que SÍ es una rotación) y las escalas simétricas.

### Relación Z

Dos escalas están **en relación Z** si tienen el mismo vector de intervalos pero NO están relacionadas por transposición ni por inversión. Suenan armónicamente parecidas pero son estructuralmente distintas. Los pares en relación Z son raros y musicalmente fascinantes.

El par Z más célebre: la relación Z del **tetracordio de todos los intervalos** entre `{0,1,4,6}` y `{0,1,3,7}`, ambos con vector de intervalos `[1,1,1,1,1,1]`.

### Ejercicio práctico

Calcula el vector de intervalos de la **escala pentatónica menor de do** (do mi♭ fa sol si♭ = clases de altura 0, 3, 5, 7, 10).

Paso 1: enumerar todos los pares y sus distancias.
Paso 2: reducir las distancias a clases de intervalo (las distancias de 7 a 11 pasan a ser 12 − distancia: por ejemplo, 8 semitonos → clase 4).
Paso 3: contar las apariciones de cada clase.

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

Recuento de clases de intervalo:
- Clase 1: 0
- Clase 2: 3
- Clase 3: 2
- Clase 4: 1
- Clase 5: 4
- Clase 6: 0

Vector de intervalos: **[0, 3, 2, 1, 4, 0]**

Nota: fuerte presencia de la clase 5 (cuartas y quintas justas) y ausencia de la clase 6 (tritono) y de la clase 1 (semitono); por eso las escalas pentatónicas suenan estables y «nunca fallan».

---

## 7. Explorar escalas sin nombre en la guitarra

Los manuales de teoría musical cubren quizá **200 escalas con nombre**: mayor, menor, modos, pentatónicas, menores armónica y melódica y sus modos, disminuida, por tonos, blues, escalas bebop, un puñado de escalas «exóticas» (húngara, bizantina, etc.) y los modos de Messiaen.

Quedan, pues, **unas 3800 escalas sin nombre** que cumplen los criterios básicos de Zeitler. La inmensa mayoría del universo de las escalas es territorio inexplorado.

### Cómo explorar

1. **Elige un número** entre 1 y 4095 (o usa un generador aleatorio)
2. **Decodifica los bits** para averiguar qué clases de altura hay en la escala
3. **Comprueba los criterios de Zeitler**: ¿es «razonable» esta escala?
4. **Tócala** en tu instrumento y escucha
5. **Anota el vector de intervalos** y compáralo con el de escalas que conozcas

### Fórmula de traslado al mástil

Para tocar un entero de escala en la guitarra hay que trasladar las clases de altura a las posiciones de traste de cada cuerda.

Dados:
- El entero de escala S
- Las clases de altura de las cuerdas al aire en afinación estándar: mi(4), la(9), re(2), sol(7), si(11), mi(4)
- Para cada cuerda, calcular qué trastes (0-12) contienen una nota de la escala

**Fórmula:** para cada traste f (de 0 a 12) de una cuerda cuya clase de altura al aire es p:

```
clase_de_altura_en_el_traste = (p + f) mod 12
esta_en_la_escala = (S >> clase_de_altura_en_el_traste) & 1
```

Si el resultado es 1, marca ese traste. Repite para las seis cuerdas.

### Ejemplo: una escala al azar

Elijamos el entero de escala **1749**. Decodificación:

```
1749 en binario: 011011010101
Clases de altura (bits 0 a 11): 0, 2, 4, 6, 7, 9, 10
Notas a partir de do:           do, re, mi, fa♯, sol, la, si♭
```

Esta escala tiene 7 notas, contiene do (la fundamental está presente), su hueco máximo es de 2 semitonos y no tiene racimos largos: cumple los criterios de Zeitler.

Patrón de intervalos: 2-2-2-1-2-1-2 (suma 12).

**Es el mixolidio ♯11** (o lidio dominante, el 4.º modo de la menor melódica): ¡una escala con nombre! Acabas de redescubrirla eligiendo un número.

Prueba un número menos transitado: **2391**. Decodificación:

```
2391 en binario: 100101010111
Clases de altura: 0, 1, 2, 4, 6, 8, 11
Notas a partir de do: do, do♯, re, mi, fa♯, sol♯, si
```

Esta cumple los criterios de Zeitler (fundamental presente, huecos pequeños, 7 notas, racimos cortos) pero no corresponde a ninguna escala de nombre habitual. Tócala en la guitarra. Escucha. Ponle nombre.

### El protocolo de exploración

1. Genera de 5 a 10 números de escala aleatorios que cumplan los criterios de Zeitler
2. Toca cada uno durante 30 segundos, atento a su carácter emocional
3. Anota tus favoritos
4. Construye melodías sencillas aprovechando el sabor interválico propio de cada escala
5. Compara con escalas con nombre de vectores de intervalos parecidos

Así es como se descubre música nueva. El universo está ahí; el traslado es mecánico; el juicio musical es tuyo.

### Ejercicio práctico

Toma el entero de escala **1709** (de sonoridad húngara).

1. Conviértelo a binario e identifica las clases de altura
2. Escribe la escala empezando en do
3. Calcula el patrón de intervalos (los pasos entre notas consecutivas)
4. Traslada la escala a las dos cuerdas agudas de una guitarra en afinación estándar (1.ª cuerda = mi, 2.ª cuerda = si) para los trastes 0 a 12

Pista: 1709 = 1024 + 512 + 128 + 32 + 8 + 4 + 1 → bits 0, 2, 3, 5, 7, 9, 10.

---

## 8. Conexión con OPTIC-K

La teoría de conjuntos musicales emplea una taxonomía de **relaciones de equivalencia** para describir en qué sentido dos colecciones de notas pueden considerarse «la misma». La regla mnemotécnica OPTIC-K las reúne todas. El marco del entero de escala hace calculables esas equivalencias.

### Las seis equivalencias

| Letra | Nombre | Significado | Operación |
|--------|------|---------|-----------|
| **O** | Octava | Las notas en octavas distintas son equivalentes | Reducción a clase de altura (mod 12) |
| **P** | Permutación | El orden de las notas es indiferente | Tratamiento como conjunto |
| **T** | Transposición | Mismo patrón a partir de otra fundamental | Rotación modular |
| **I** | Inversión | Imagen especular en torno a un pivote | Inversión del orden de los intervalos |
| **C** | Cardinalidad | Número de clases de altura distintas | POPCOUNT del entero |
| **K** | (Forma alternativa) | — | Calculada a partir de una K-net o estructura análoga |

(La «K» de OPTIC-K remite, según las fuentes, o bien a la equivalencia de cardinalidad, o bien a una estructura concreta de Kuusisto/Lewin.)

### Dónde vive cada equivalencia en el marco

- **Equivalencia O:** integrada en el modelo. Al reducir las notas a clases de altura de 0 a 11, se descarta la información de octava.
- **Equivalencia P:** integrada en el modelo. Un entero de 12 bits es un conjunto (independiente del orden) por construcción.
- **Equivalencia T:** se calcula como rotación (desplazamiento circular) del entero.
- **Equivalencia I:** se calcula como **inversión de los bits** del entero de 12 bits. Invertir los bits de una escala S da su escala invertida (queda rotar para devolver la fundamental al bit 0).
- **Equivalencia C:** se calcula mediante POPCOUNT, el número de bits a 1.

### Las 224 clases de Forte

Bajo la equivalencia combinada T e I (la taxonomía estándar de Forte), las 4096 escalas se reducen a **224 clases distintas**. Esas clases constituyen el fundamento de la teoría de conjuntos musicales del siglo XX.

Cada clase de Forte tiene una forma prima canónica (el representante lexicográficamente menor tras la normalización). El libro de Forte de 1973, **«The Structure of Atonal Music»**, tabula las 224 clases con sus vectores de intervalos, simetrías y relaciones Z.

### El espacio vectorial de 216 dimensiones de GA

Guitar Alchemist representa las escalas como vectores de características en un espacio de 216 dimensiones. Esas dimensiones codifican:

- La cardinalidad (1 dimensión)
- El vector de intervalos (6 dimensiones)
- El brillo (1 dimensión)
- Las posiciones modales (número variable)
- El contenido de acordes (número variable)
- Las métricas de ejecutabilidad propias de la guitarra (número variable)
- Las pertenencias a las clases de equivalencia OPTIC-K (número variable)

Dos escalas próximas en ese espacio de 216 dimensiones comparten carácter musical. El espacio es navegable: puedes ir del mayor hacia el lidio caminando en una dirección concreta; puedes encontrar la escala «sin nombre» más próxima a una con nombre; puedes calcular distancias armónicas entre escalas cualesquiera.

El entero de escala es el **índice** de ese espacio vectorial. Dado el entero S, GA calcula de forma determinista el vector completo de 216 características.

### El beneficio

El universo de las escalas es:
- **Finito** (4096 escalas)
- **Enumerable** (los enteros de 0 a 4095)
- **Transformable** (operaciones de bits para modos, inversiones y complementos)
- **Calculable** (toda propiedad se deduce del entero)
- **Navegable** (distancias y vecindades en el espacio de características)
- **En su mayor parte inexplorado** (solo unas 200 de las ~1500 escalas legítimas tienen nombre)

La teoría musical no tenía por qué ser difusa. La teoría de conjuntos de clases de altura, unida al cálculo moderno, convierte las escalas de folclore en datos.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Clase de altura** | La identidad de una nota con independencia de la octava (do, do♯, re, … si) |
| **Temperamento igual de 12 sonidos** | El temperamento igual de doce grados: el sistema de afinación occidental estándar |
| **Entero de escala** | Un número de 12 bits en el que cada bit indica la presencia o ausencia de una clase de altura |
| **Modo** | Una rotación de una escala, en la que un grado distinto de la fundamental pasa a ser la nueva fundamental |
| **Forma prima** | El representante canónico de una familia de escalas bajo una equivalencia |
| **Número de Forte** | Una etiqueta normalizada (por ejemplo, 7-35) para una clase de conjuntos de clases de altura |
| **Vector de intervalos** | Una séxtupla que cuenta las apariciones de cada clase de intervalo en una escala |
| **Clase de intervalo** | Un intervalo reducido módulo la octava Y la inversión: los intervalos de 1 a 6 y sus complementos de 11 a 6 se reducen a las clases 1 a 6 |
| **Brillo** | La suma de las clases de altura de una escala (indicador del carácter sostenido/bemol) |
| **Simetría (de rotación)** | La propiedad de una escala de transformarse en sí misma al rotar |
| **Quiralidad** | La asimetría de una escala bajo la inversión |
| **Relación Z** | Dos escalas con el mismo vector de intervalos no relacionadas por T ni por I |
| **Criterios de Zeitler** | Heurísticas que filtran las escalas matemáticas para quedarse con las «musicalmente reales» |
| **POPCOUNT** | El número de bits a 1 de un número binario (= la cardinalidad de la escala) |
| **OPTIC-K** | Regla mnemotécnica de las relaciones de equivalencia en la teoría de conjuntos musicales |

---

## Autoevaluación

**1. Convierte la escala de do dórico (do re mi♭ fa sol la si♭) en su entero de clases de altura según la convención de asignación de bits.**
> Clases de altura: 0, 2, 3, 5, 7, 9, 10. Entero = 1 + 4 + 8 + 32 + 128 + 512 + 1024 = **1709**.

**2. Calcula el vector de intervalos de la escala por tonos de do (do re mi fa♯ sol♯ la♯).**
> Los pares solo dan intervalos de 2, 4 y 6 semitonos. Recuentos: clase 1 = 0, clase 2 = 6, clase 3 = 0, clase 4 = 6, clase 5 = 0, clase 6 = 3. Vector de intervalos: **[0, 6, 0, 6, 0, 3]**.

**3. ¿Cuál es el número de Forte de la escala mayor (colección diatónica) y cuántas notas tiene?**
> Número de Forte **7-35**. La primera cifra (7) indica una cardinalidad de 7 notas.

**4. Explica por qué los siete modos de la escala mayor NO son siete escalas distintas bajo la equivalencia de transposición.**
> Los siete modos contienen las mismas siete clases de altura dispuestas según el mismo patrón cíclico de intervalos (2-2-1-2-2-2-1). Cada modo es una rotación de los demás: comparten una sola forma prima. Empezar el patrón en otro grado no cambia la estructura subyacente de la escala, solo la elección de la tónica.

**5. Aplica el filtrado de Zeitler a la escala de clases de altura {0, 1, 7}. ¿Qué criterios cumple y cuáles incumple?**
> Fundamental presente (bit 0 a 1): CUMPLE. Hueco máximo de 1 a 7: 6 semitonos: INCUMPLE (supera 4). Cardinalidad = 3 notas: INCUMPLE (por debajo del mínimo de 5). Sin racimos de 4 semitonos o más: CUMPLE. Balance: no supera el filtro de Zeitler como escala «legítima» (es un tricordio, no una escala).

**Criterios de logro:** convertir cualquier escala (dada en clases de altura o en nombres de nota) hacia y desde su representación entera, calcular su vector de intervalos a mano, identificar su cardinalidad de Forte y explicar qué equivalencias OPTIC-K están integradas en el modelo entero y cuáles exigen un cálculo adicional.

---

## Bases de la investigación

- El temperamento igual de 12 sonidos como estándar de afinación occidental está documentado empíricamente en la afinación de pianos y en la práctica orquestal desde el siglo XIX
- La teoría de conjuntos de clases de altura y la enumeración de las 4096 escalas tienen su origen en los trabajos combinatorios de Milton Babbitt (años cincuenta) y fueron formalizadas por Allen Forte en *The Structure of Atonal Music* (1973)
- Las 224 clases de conjuntos bajo la equivalencia T/I están enumeradas y tabuladas en Forte (1973) y siguen siendo la taxonomía de referencia
- Los criterios de escala de Zeitler proceden del proyecto de catalogación exhaustiva de William Zeitler (*All The Scales*, 2011, y el sitio complementario), y constituyen un filtro práctico sobre el universo
- La geometría de las escalas y las relaciones de vecindad se exploran en *A Geometry of Music* de Dmitri Tymoczko (2011), que formaliza las distancias de conducción de voces entre acordes y escalas
- La representación en un espacio de características de 216 dimensiones es una decisión de implementación de Guitar Alchemist, que amplía la teoría clásica de conjuntos de clases de altura con metadatos de interpretación y de función armónica
- Las relaciones de equivalencia OPTIC-K se remontan a *Generalized Musical Intervals and Transformations* de David Lewin (1987) y a su sistematización posterior en la enseñanza de la teoría musical
- Fuentes: Forte (1973); Tymoczko (2011); Lewin (1987); Rahn, *Basic Atonal Theory* (1980); catálogo de escalas de Zeitler (2011)
- Estado de creencia: T(0.85) F(0.03) U(0.08) C(0.04)
