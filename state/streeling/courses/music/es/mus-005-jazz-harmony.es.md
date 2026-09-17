---
module_id: mus-005-jazz-harmony
department: music
course: Armonía de jazz para guitarra
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites:
  - mus-001-what-is-a-chord
  - mus-003-functional-harmony
  - gtr-002-caged-geometry
estimated_duration: "3 hours"
produced_by: music
version: "1.0.0"
---

# Armonía de jazz para guitarra: del ii-V-I a los Coltrane Changes

> **Departamento de Música** | Etapa: Citrinitas (Intermedio a avanzado) | Duración: 3 horas

## Objetivos de aprendizaje

Al completar este curso, serás capaz de:

- Leer e interpretar cualquier cifrado de acorde de jazz, incluidas las extensiones, las alteraciones y la notación con barra
- Identificar progresiones ii-V-I en tonalidades mayores y menores dentro del repertorio estándar de jazz
- Conducir las voces a través de los cambios de acordes con voicings shell, drop-2 y drop-3
- Aplicar la conducción de voces por notas guía para enlazar los acordes con suavidad
- Emplear la sustitución tritonal, la sustitución disminuida y la dominante "backdoor"
- Asociar las escalas adecuadas a cada calidad de acorde mediante la teoría acorde-escala
- Construir voicings por cuartas y tríadas de estructura superior para una sonoridad de jazz moderna
- Analizar y aplicar el ciclo de sustitución simétrico por terceras mayores de Coltrane

---

## 1. Leer con soltura los cifrados de jazz

Los cifrados de acordes de jazz son un lenguaje de notación comprimido. A diferencia del bajo cifrado clásico, codifican la calidad, las extensiones, las alteraciones y la nota del bajo en un único símbolo compacto. Leerlos con fluidez es un requisito previo para todo lo que sigue.

### Anatomía de un cifrado

Todo cifrado de jazz tiene hasta cuatro componentes:

```
Root  +  Quality  +  Extensions/Alterations  +  Slash Bass
 C        maj           9#11                      /E
```

**Fundamental:** cualquier letra de la A a la G, opcionalmente con # o b.

La **calidad** codifica la tríada y la séptima:

| Símbolo | Significado | Tercera | Séptima |
|--------|---------|-------|---------|
| (nada) o `maj` | Tríada mayor | Tercera mayor | — |
| `m` o `min` o `-` | Tríada menor | Tercera menor | — |
| `7` | Séptima de dominante | Tercera mayor | Séptima menor |
| `maj7` o `M7` o triángulo | Séptima mayor | Tercera mayor | Séptima mayor |
| `m7` o `min7` o `-7` | Séptima menor | Tercera menor | Séptima menor |
| `m7b5` o semidisminuido | Semidisminuido | Tercera menor | Séptima menor (b5) |
| `dim7` o `o7` | Séptima disminuida | Tercera menor | Séptima disminuida |

Las **extensiones** añaden notas superiores (9, 11, 13). El número más alto implica todas las notas impares por debajo:

- `Cmaj9` = C E G B D (implica que la 7.ª está presente)
- `Cmaj13` = C E G B D (F#) A (implica la 9 y la 7; la 11 suele ser #11 en un contexto mayor)

Las **alteraciones** modifican notas concretas:

- `#11` — 11.ª aumentada (evita el choque con la tercera mayor)
- `b9`, `#9` — 9.ª rebajada o aumentada
- `b13` — 13.ª rebajada (enarmónica de #5)
- `alt` — abreviatura de dominante con b9, #9, #11/b5, b13/#5

### La ambigüedad C7 / Cmaj7

Esto confunde a todos los principiantes:

- **C7** = C E G **Bb** (séptima de dominante — el "7" por defecto es un intervalo de séptima menor)
- **Cmaj7** = C E G **B** (séptima mayor — el calificativo "maj" eleva la séptima)

El "7" a secas siempre significa dominante. Tienes que escribir "maj7" para obtener una séptima mayor. Esta convención es un vestigio histórico del blues y del jazz temprano, donde las séptimas de dominante eran el sonido por defecto.

### Acordes con barra

`C/E` significa "acorde de Do mayor con E en el bajo". La nota después de la barra es la nota del bajo, no necesariamente una nota del acorde. Usos habituales:

- Inversiones: `C/E` (primera inversión), `C/G` (segunda inversión)
- Poliacordes implícitos: `Db/C` = tríada de Db sobre un bajo de C (crea un sonido de Cmaj7#11)
- Pedales: `Dm7/G` = crea un sonido de G11 sin enunciar G como fundamental

### Ejercicio práctico

Lee los siguientes cifrados y deletrea sus notas. No uses tu instrumento — trabaja solo a partir del símbolo:

1. `Fmaj9#11`
2. `Bb7alt`
3. `Ebm11`
4. `Ab13`
5. `Dm7b5`
6. `G7#9/Db` (¿qué sustitución implica?)

Respuestas:
1. F A C E G B (Fa mayor con 7.ª mayor, 9.ª, #11.ª)
2. Bb D Ab B/Cb Eb/D# Gb (dominante con todas las extensiones superiores alteradas)
3. Eb Gb Bb Db F Ab (séptima menor con 11.ª)
4. Ab C Eb Gb Bb Db F (séptima de dominante con 9.ª, 11.ª implícita, 13.ª)
5. D F Ab C (tríada menor con quinta disminuida y séptima menor)
6. G B D F A#/Bb sobre un bajo de Db — el bajo de Db implica la sustitución tritonal de G7

---

## 2. El universo del ii-V-I

La progresión ii-V-I es el centro de gravedad de la armonía de jazz. Entenderla es como entender las oraciones de un idioma — una vez que las oyes, las oyes en todas partes.

### ii-V-I mayor

En Do mayor:

```
  Dm7    →    G7    →    Cmaj7
  ii7         V7         Imaj7
```

¿Por qué funciona? Cada acorde se resuelve en el siguiente mediante el movimiento de fundamentales más fuerte de la música tonal — las quintas descendentes (D→G→C). La conducción de voces es igual de poderosa: la tercera de Dm7 (F) resuelve bajando a la tercera de G7 (B no es F, sino que la 7.ª de Dm7, C, se convierte en la relación de 7.ª). Más exactamente:

- La **7.ª del ii** (C) baja por grado conjunto a la **tercera del V** (B)
- La **tercera del V** (B) sube por grado conjunto a la **fundamental del I** (C)
- La **7.ª del V** (F) baja por grado conjunto a la **tercera del I** (E)

Esta atracción cromática por grados conjuntos crea una sensación de resolución irresistible.

### ii-V-i menor

En Do menor:

```
  Dm7b5  →    G7alt   →    Cm(maj7) or Cm7
  ii-half      V7alt        i
```

El ii semidisminuido aporta el color de la tonalidad menor. La dominante alterada (G7alt) contiene tanto la b9 (Ab) como la b13 (Eb), que son la b6 y la b3 de Do menor — justamente las notas que definen la tonalidad menor.

### Cadenas de ii-V extendidas

Las piezas de jazz a menudo encadenan ii-V por varias tonalidades sin resolver:

```
  Em7  A7  |  Dm7  G7  |  Cmaj7
  ii   V      ii   V      I
  (of D)      (of C)      (arrived)
```

El turnaround — los últimos compases de una forma que llevan de vuelta al principio — es la cadena extendida más habitual:

```
  Cmaj7  Am7  |  Dm7  G7  ||  (back to Cmaj7)
  I      vi      ii   V        I
```

### Ejercicio práctico

Esta es la progresión de acordes de **"All The Things You Are"** (Kern/Hammerstein). Rodea cada ii-V-I (mayor o menor). Marca si cada uno se resuelve o queda en el aire:

```
Fm7   | Bbm7   | Eb7    | Abmaj7 |
Dbmaj7| Dm7    | G7     | Cmaj7  |
Cm7   | Fm7    | Bb7    | Ebmaj7 |
Abmaj7| Am7    | D7     | Gmaj7  |
Am7   | D7     | Gmaj7  |        |
F#m7  | B7     | Emaj7  | C7alt  |
Fm7   | Bbm7   | Eb7    | Abmaj7 |
Dbmaj7| Dbm7   | Cm7    | Bdim7  |
Bbm7  | Eb7    | Abmaj7 |        |
```

Deberías encontrar al menos seis progresiones ii-V-I en tres tonalidades distintas, además de varios ii-V que resuelven de forma rota o se encadenan hacia la siguiente zona tonal.

---

## 3. Voicings de guitarra de jazz

Los pianistas pueden disponer los acordes con diez dedos a lo largo de cinco octavas. Los guitarristas tienen seis cuerdas y cuatro dedos para pisar. Esta limitación es en realidad un regalo — obliga a usar voicings económicos que atraviesan el conjunto y se prestan a una conducción de voces preciosa.

### Voicings shell (fundamental + tercera + séptima)

La fundamental, la tercera y la séptima son las **notas esenciales** que definen la calidad y la función de un acorde. La quinta casi siempre se omite (no aporta información armónica a menos que esté alterada).

**Fundamental en la 6.ª cuerda:**

```
Dm7:        G7:         Cmaj7:
e ----      e ----      e ----
B ----      B ----      B ----
G ----      G ----      G ----
D ----      D ----      D ----
A --5--     A ----      A --3--
E --x--     E --3--     E --x--
   1 b3 b7     1 3 b7      1 3 7
```

(Las posiciones reales de los trastes dependen de dónde esté la fundamental; el concepto es fundamental-tercera-séptima en cuerdas adyacentes.)

**Fundamental en la 5.ª cuerda:**

Los shells con la fundamental en la 5.ª cuerda mantienen el voicing en un registro medio cómodo. La tercera y la séptima caen en las cuerdas 4 y 3, lo que deja libres las cuerdas agudas para la melodía o las extensiones.

### Voicings drop-2

Toma un acorde de cuatro notas en posición cerrada y "deja caer" una octava la segunda nota más aguda. Esto reparte el voicing en cuatro cuerdas adyacentes — perfecto para la guitarra.

**Cmaj7 en posición cerrada:** B-E-G-C (de arriba abajo: C-G-E-B en orden ascendente, luego se reordena bajando la segunda desde arriba)

**Cmaj7 en drop-2 (grupo de cuerdas 5-4-3-2):**

```
e ----
B --0-- (B, the 7th)
G --0-- (G, the 5th)
D --2-- (E, the 3rd — dropped from close position)
A --3-- (C, the root)
E ----
```

Los voicings drop-2 existen en cuatro grupos de cuerdas:

| Grupo de cuerdas | Registro | Ideal para |
|-----------|-------|----------|
| 6-5-4-3 | Grave | Acompañamiento en dúo o con walking bass |
| 5-4-3-2 | Medio | Registro de acompañamiento estándar |
| 4-3-2-1 | Agudo | Acompañamiento melódico, chord melody |

Cada calidad de acorde (maj7, m7, 7, m7b5) tiene cuatro inversiones por grupo de cuerdas, lo que te da 48 voicings drop-2 que interiorizar (4 calidades x 4 inversiones x 3 grupos de cuerdas).

### Voicings drop-3

Deja caer una octava la tercera nota más aguda de un voicing cerrado. Esto crea una apertura más amplia, con un hueco entre la nota del bajo y el grupo superior. Los voicings drop-3 abarcan cinco cuerdas (saltándose una cuerda en el medio).

**Grupos de cuerdas para drop-3:** 6-4-3-2 y 5-3-2-1.

Los voicings drop-3 son más oscuros y orquestales. Joe Pass los usaba mucho en chord melody.

### Voicings a lo Freddie Green

El enfoque de la guitarra rítmica de Count Basie: cuatro negras por compás, un voicing por tiempo, casi siempre en las cuerdas 6-4-3 (o 5-4-3). Solo tres notas — fundamental (o nota grave del shell), tercera, séptima. Rasgueadas con un ataque rápido y percusivo que se apaga de inmediato. La guitarra se convierte en un tambor con altura definida.

### Técnica de octavas de Wes Montgomery / George Benson

No es una técnica de voicing en sentido armónico, pero sí vocabulario esencial de la guitarra de jazz. Líneas de una sola nota dobladas a la octava (cuerdas 6+4, 5+3 o 4+2), con la cuerda intermedia apagada por el dedo que pisa. Crea un sonido grueso, parecido al de un metal.

### Ejercicio práctico

Conduce las voces del siguiente ii-V-I en Do mayor con voicings drop-2 en el grupo de cuerdas 5-4-3-2. Tu objetivo: un movimiento mínimo de los dedos entre acordes. Escribe las posiciones de los trastes de cada acorde:

```
Dm7  →  G7  →  Cmaj7
```

Regla: la séptima de un acorde debe resolver por grado conjunto a la tercera (o a una nota cercana) del acorde siguiente. Encuentra dos inversiones distintas que logren este enlace suave.

---

## 4. Notas guía y conducción de voces

### El principio de las notas guía

La **tercera** y la **séptima** de cada acorde se llaman **notas guía** porque:

1. **Definen la calidad:** la tercera indica mayor o menor. La séptima indica dominante, mayor o menor.
2. **Crean movimiento:** cuando cambian los acordes, las notas guía se mueven por semitono o por tono — los intervalos más pequeños y suaves posibles.

El milagro central de la conducción de voces del ii-V-I:

```
Chord:    Dm7    G7     Cmaj7
3rd:       F  →   B  →   E
7th:       C  →   F  →   B
```

Observa:
- La **7.ª de Dm7 (C)** baja un semitono para convertirse en la **tercera de G7 (B)**
- La **tercera de Dm7 (F)** se queda quieta para convertirse en la **7.ª de G7 (F)**
- La **7.ª de G7 (F)** baja un semitono para convertirse en la **tercera de Cmaj7 (E)**
- La **tercera de G7 (B)** se queda quieta para convertirse en la **7.ª de Cmaj7 (B)**

Las notas guía **intercambian sus papeles**: la tercera de un acorde se convierte en la séptima del siguiente, y viceversa. Esto crea un contrapunto a dos voces que desciende cromáticamente: C-B, F-E.

### El acompañamiento a dos notas de Barry Harris

Barry Harris enseñaba que puedes acompañar un tema entero con **solo la tercera y la séptima** de cada acorde — dos notas en las cuerdas centrales. Esto reduce la armonía a su esencia y entrena tu oído para oír la función sin la muleta de los voicings completos.

### Construir una línea de notas guía

Una línea de notas guía es una única línea melódica que traza el camino más suave a través de una progresión de acordes siguiendo la tercera o la séptima de cada acorde. Cuando una resuelve hacia abajo, síguela. Cuando una se queda quieta, mantenla.

En un arreglo para guitarra sola, la línea de notas guía se convierte en la voz interior alrededor de la cual construyes voicings más completos por encima y por debajo.

### Ejercicio práctico

Escribe una línea de notas guía (solo terceras y séptimas, eligiendo las que se muevan con más suavidad) sobre la sección A de los **Rhythm Changes** en Sib:

```
Bbmaj7 | G7    | Cm7   | F7    |
Dm7    | G7    | Cm7   | F7    |
```

Empieza en la tercera de Bbmaj7 (D). En cada cambio de acorde, ve a la nota guía más cercana (tercera o séptima) del nuevo acorde. Tu línea debe moverse como mucho por semitono o por tono. Escribe la línea de ocho notas resultante.

---

## 5. Técnicas de sustitución

La sustitución es el arte de reemplazar un acorde por otro que cumple una función armónica similar pero crea un color diferente. El jazz se construye sobre capas de sustituciones aplicadas a progresiones subyacentes sencillas.

### La sustitución tritonal a fondo

La sustitución tritonal reemplaza un acorde de séptima de dominante por otro acorde de séptima de dominante cuya fundamental está a un tritono (b5) de distancia.

**G7 → Db7** (ambos resuelven a C)

¿Por qué funciona? Las **notas guía son compartidas:**

```
G7:   B (3rd)  F (7th)
Db7:  F (3rd)  Cb/B (7th)
```

La tercera y la séptima simplemente intercambian sus papeles. La resolución a Cmaj7 funciona igual porque F→E y B→C (o Cb→C) en ambos casos. Lo que cambia es el movimiento del bajo: en lugar de G→C (quinta descendente), obtienes Db→C (descenso cromático) — un sonido más estilizado y moderno.

**Aplicación en el ii-V-I:**

```
Original:    Dm7  | G7    | Cmaj7
Tritone sub: Dm7  | Db7   | Cmaj7
With ii:     Abm7 | Db7   | Cmaj7  (Abm7 is the related ii of Db7)
```

### Sustitución disminuida

Un acorde de séptima disminuida puede sustituir a un acorde de séptima de dominante situado un semitono por debajo de cualquiera de sus cuatro notas (porque el dim7 es simétrico — cada nota está a una tercera menor de la siguiente).

**Bdim7 puede sustituir a:** C7, Eb7, Gb7 o A7 (acordes de dominante cuya fundamental está un semitono por encima de cada nota del acorde disminuido: B, D, F, Ab).

### Acordes disminuidos de paso

Un acorde disminuido puede conectar dos acordes diatónicos cuyas fundamentales están a un tono de distancia:

```
Cmaj7 | C#dim7 | Dm7
I       #Idim7   ii
```

La línea del bajo (C-C#-D) crea un ascenso cromático. El C#dim7 funciona como un A7b9 sin fundamental (A-C#-E-G-Bb → sin A: C#-E-G-Bb).

### Dominante backdoor (bVII7 → I)

En lugar de la resolución estándar V7→I, el jazz usa **bVII7→I**:

```
Standard: G7  → Cmaj7  (V → I)
Backdoor: Bb7 → Cmaj7  (bVII → I)
```

El bVII7 se acerca a la tónica desde un tono por debajo. La resolución funciona porque Bb7 contiene D y Ab, que resuelven a C y G (o E) por grado conjunto. El sonido es cálido, inesperado y evita la atracción obvia de la dominante.

El **ii relacionado** de la dominante backdoor: Fm7 → Bb7 → Cmaj7.

### Ejercicio práctico

Rearmoniza el puente de los **Rhythm Changes** con técnicas de sustitución. El puente original es:

```
D7  | D7  | G7  | G7  |
C7  | C7  | F7  | F7  |
```

Aplica estas sustituciones:
1. Añade un ii relacionado antes de cada dominante
2. Aplica sustituciones tritonales a dominantes alternas
3. Prueba un acorde disminuido de paso entre D7 y G7

Escribe tu puente rearmonizado de 8 compases. No hay una única respuesta correcta — el objetivo es crear una conducción de voces suave mientras añades color armónico.

---

## 6. Teoría acorde-escala

La teoría acorde-escala asigna una escala a cada acorde, lo que proporciona un repertorio de notas melódicas consonantes con esa armonía. Es la pedagogía estándar del jazz para la improvisación, aunque tiene limitaciones importantes.

### Las asignaciones básicas

| Calidad de acorde | Escala | Origen | Notas a evitar |
|--------------|-------|--------|-------------|
| **Imaj7** | Jónico (mayor) | Escala mayor | 4 (F en Do) |
| **Imaj7#11** | Lidio | Menor melódica sobre el 4.º grado | Ninguna |
| **ii-7** | Dórico | Escala mayor desde el 2.º grado | Ninguna (la b6 añade color) |
| **V7** (que resuelve) | Mixolidio | Escala mayor desde el 5.º grado | 4 (pero utilizable como nota de paso) |
| **V7#11** | Lidio dominante | Menor melódica desde el 4.º grado | Ninguna |
| **V7alt** | Alterada | Menor melódica desde el 7.º grado | Ninguna |
| **ii-7b5** | Locrio | Escala mayor desde el 7.º grado | 2 (9.ª natural) — o usa el locrio #2 |
| **i-7** | Dórico | — | — |
| **bVII7** (backdoor) | Lidio dominante | — | — |
| **dim7** | Disminuida (semitono-tono) | Simétrica | — |

### La escala madre menor melódica

La escala **menor melódica** (forma ascendente: 1 2 b3 4 5 6 7) es la navaja suiza del músico de jazz. Sus modos generan las escalas para la mayoría de las situaciones de dominantes alteradas y extendidas:

| Modo | Grado | Nombre | Se usa para |
|------|--------|------|----------|
| 1.º | Fundamental | Menor melódica | Acordes menores con séptima mayor |
| 2.º | 2.º grado | Dórico b2 (frigio #6) | Acordes sus(b9) |
| 3.º | 3.er grado | Lidio aumentado | Acordes maj7#5 |
| 4.º | 4.º grado | Lidio dominante | Acordes 7#11, sustituciones tritonales |
| 5.º | 5.º grado | Mixolidio b6 | V7 que resuelve a menor |
| 6.º | 6.º grado | Locrio #2 (eólico b5) | Acordes semidisminuidos |
| 7.º | 7.º grado | Alterada (superlocria) | Acordes V7alt |

### Notas a evitar — qué son y qué no son

Una **nota a evitar** es un grado de la escala que crea una novena menor (intervalo de b9) contra una nota del acorde cuando se sostiene. No significa "no toques nunca esta nota" — significa no detenerse en ella ni enfatizarla. Como nota de paso o aproximación cromática, cualquier nota vale.

Ejemplo: sobre Cmaj7, la nota F (4.º grado) crea un semitono (novena menor) contra E (la tercera). Sostener F contra E produce disonancia. Pero F como nota de paso entre E y G es perfectamente natural.

### Limitaciones de la teoría acorde-escala

La teoría acorde-escala es un mapa, no el territorio:

- Funciona mejor con una armonía lenta, en la que cada acorde dura lo suficiente como para establecer una escala
- Sobre ii-V-I rápidos, los músicos experimentados piensan en términos de **conducción de voces** y **notas objetivo**, no de escalas
- Los grandes improvisadores de jazz (Parker, Coltrane, Shorter) trascienden el pensamiento basado en escalas mediante la **aproximación cromática**, los **enclosures** y el **desarrollo motívico**
- La teoría acorde-escala no dice nada sobre el ritmo, el fraseo o la narración — los elementos que realmente hacen que un solo sea cautivador

### Ejercicio práctico

Para cada acorde de la siguiente progresión, nombra la escala correspondiente y deletrea sus notas. Identifica las notas a evitar:

```
Cmaj7 | Dm7 | G7alt | Cm(maj7) |
```

Después toca la progresión en la guitarra improvisando una melodía sencilla que use solo las notas del acorde y una o dos notas de la escala por acorde. Fíjate en cómo las notas guía (terceras y séptimas) crean las conexiones melódicas más fuertes.

---

## 7. Armonía por cuartas y estructuras superiores

### Voicings por cuartas

La armonía tradicional apila **terceras**. La armonía por cuartas apila **cuartas**. El sonido es abierto, ambiguo y moderno — evita la fuerte atracción mayor/menor de la armonía por terceras.

**El enfoque de McCoy Tyner:** sobre un vamp en Re dórico, apila cuartas justas desde distintos grados de la escala:

```
From D: D - G - C - F     (stacked 4ths)
From E: E - A - D - G     (stacked 4ths)
From G: G - C - F - Bb    (stacked 4ths — includes b6, outside Dorian)
```

Estos voicings pueden moverse dentro del modo y crean un paisaje armónico resplandeciente y no funcional. Los voicings individuales no "resuelven" — flotan.

### El voicing "So What"

Procede de la grabación emblemática de Miles Davis (1959). El voicing para Re dórico:

```
E - A - D - G - B
```

Son tres cuartas apiladas (E-A-D-G) coronadas por una tercera mayor (G-B). Define el sonido del jazz modal. Transportado un semitono arriba para el puente (Mib dórico): F-Bb-Eb-Ab-C.

En la guitarra, el voicing So What se toca normalmente así:

```
e --7-- (B)
B --8-- (G)
G --7-- (D)
D --7-- (A)
A --7-- (E)
E ----
```

### Tríadas de estructura superior

Una tríada de estructura superior es una simple tríada mayor o menor superpuesta a un acorde de séptima de dominante, que crea extensiones y alteraciones ricas sin cifrados complejos.

Sobre **C7**, distintas tríadas de estructura superior producen:

| Tríada superior | Notas (sobre C-E-Bb) | Extensiones creadas |
|-------------|---------------------|-------------------|
| D mayor | D F# A | 9, #11, 13 — el sonido lidio dominante |
| Eb mayor | Eb G Bb | #9, 5, b7 — las extensiones del "acorde Hendrix" |
| Ab mayor | Ab C Eb | b13, fundamental, #9 — el sonido alterado |
| F# mayor | F# A# C# | #11, b7(enh), b9 — alterado extremo |
| Bb mayor | Bb D F | b7, 9, 11 — el sonido sus/11 |

La belleza de las estructuras superiores es que tocas una **tríada simple** — algo que tus manos ya conocen — mientras el bajista aporta la fundamental y la séptima. La combinación produce una armonía sofisticada a partir de ingredientes sencillos.

### Ejercicio práctico

Construye voicings por cuartas desde cada grado de Re dórico (D E F G A B C) en el grupo de cuerdas 4-3-2-1. Apila tres cuartas justas desde cada nota de partida. Escribe las cuatro notas de cada voicing e identifica la calidad de acorde resultante (algunos serán acordes por terceras conocidos, disfrazados).

Después: sobre un vamp de C7, toca formas de tríada de D mayor, Ab mayor y Eb mayor en el registro agudo mientras se sostiene una nota C en el bajo. Escucha cómo cada estructura superior cambia el color del acorde de dominante.

---

## 8. Coltrane Changes

### La división simétrica por terceras mayores

En 1959, John Coltrane introdujo un sistema de sustitución que divide la octava en tres partes iguales (terceras mayores): **B - G - Eb** (o, de forma equivalente, tres notas cualesquiera a una tercera mayor de distancia). Esto crea tres centros tonales equidistantes entre sí.

El ciclo: empezando desde cualquier tonalidad, baja una tercera mayor, luego otra tercera mayor, y vuelves al punto de partida:

```
C → Ab → E → C  (descending major thirds)
or equivalently:
C → E → Ab → C  (ascending major thirds)
```

### Análisis de Giant Steps

**"Giant Steps"** (Coltrane, 1960) es la aplicación definitiva. Toda la composición recorre en ciclo tres centros tonales a una tercera mayor de distancia:

```
Bmaj7 D7 | Gmaj7 Bb7 | Ebmaj7 | Am7 D7  |
Gmaj7 Bb7| Ebmaj7 F#7| Bmaj7  | Fm7 Bb7 |
Ebmaj7   | Am7 D7    | Gmaj7  | C#m7 F#7|
Bmaj7    | Fm7 Bb7   | Ebmaj7 | C#m7 F#7|
```

Los tres centros tonales son **B, G y Eb** — cada uno a una tercera mayor del anterior. Cada llegada a una nueva tonalidad está precedida por su V7 (y a veces por ii-V).

El ritmo armónico es vertiginoso: dos acordes por compás a un tempo rápido, con centros tonales que cambian cada uno o dos tiempos. Por eso "Giant Steps" se consideró casi imposible de tocar cuando se grabó por primera vez — los acompañantes tenían que recorrer tres tonalidades en el espacio en que normalmente bastaría una.

### Countdown como Tune Up rearmonizado

**"Countdown"** muestra cómo los Coltrane Changes funcionan como técnica de rearmonización. El tema original es "Tune Up" de Miles Davis:

```
Tune Up:   Em7  | A7   | Dmaj7 | Dmaj7 |
Countdown: Em7  | F7 Bbmaj7 | Db7 Gbmaj7 | A7 Dmaj7 |
```

Coltrane reemplaza el sencillo ii-V-I por una cadena de V-I que desciende por terceras mayores:

- Desde el objetivo (Dmaj7), retrocede por el ciclo de terceras mayores: Dmaj7 ← Gbmaj7 ← Bbmaj7
- Cada centro tonal está precedido por su V7: A7→D, Db7→Gb, F7→Bb
- El resultado: tres resoluciones ii-V-I comprimidas en cuatro compases

### La geometría

El ciclo de Coltrane es un **triángulo inscrito en el círculo de quintas** — tres puntos equidistantes en la esfera de reloj de doce sonidos. Donde la armonía de jazz tradicional se mueve por el círculo por quintas (pasos adyacentes), Coltrane lo atraviesa a saltos de terceras mayores (cada cuatro pasos).

```
       C
   F       G
 Bb           D
  Eb         A
    Ab     E
       B(Db)

Triangle 1: C - E - Ab
Triangle 2: D - F# - Bb
Triangle 3: Eb - G - B  ← Giant Steps triangle
Triangle 4: F - A - Db
```

Solo hay cuatro triángulos de terceras mayores distintos. Cada uno divide los doce sonidos en tres grupos de cuatro.

### Aplicar los Coltrane Changes a cualquier ii-V-I

Para rearmonizar un ii-V-I con el ciclo de Coltrane:

1. Identifica la tonalidad objetivo (el acorde de I)
2. Encuentra las otras dos tonalidades a una tercera mayor de distancia
3. Inserta un V7→I para cada centro tonal, empezando por el más lejano y volviendo hacia el objetivo

**Ejemplo — rearmonizar Dm7-G7-Cmaj7:**

```
Original:  Dm7     | G7      | Cmaj7   |
Coltrane:  Dm7 Eb7 | Abmaj7 B7 | Emaj7 G7 | Cmaj7 |
```

O, de forma más compacta:

```
Dm7 | Eb7 Abmaj7 | B7 Emaj7 | Cmaj7 |
```

### Ejercicio práctico

1. Escribe los tres centros tonales por terceras mayores para un ii-V-I en **Fa mayor** (objetivo: Fmaj7).
2. Rearmoniza `Gm7 | C7 | Fmaj7` con el ciclo de Coltrane, insertando pares V7→I para cada centro tonal.
3. Toca despacio tu rearmonización en la guitarra con voicings shell. Céntrate en el movimiento del bajo — debe seguir un patrón de terceras mayores descendentes conectadas por semitonos ascendentes (las fundamentales de los V7).

---

## Tabla de referencia de estándares

Los siguientes estándares de jazz se citan a lo largo de este curso como material de estudio:

| Estándar | Compositor | Conceptos clave | Por qué estudiarlo |
|----------|----------|-------------|--------------|
| **Autumn Leaves** | Kosma/Mercer | ii-V-I en mayor y en la relativa menor | El primer tema de jazz perfecto — dos ii-V-I en tonalidades relativas |
| **All The Things You Are** | Kern/Hammerstein | ii-V-I encadenados a través de cuatro centros tonales | El estándar armónicamente más rico del repertorio |
| **Rhythm Changes** | Gershwin (I Got Rhythm) | Turnarounds, dominantes del puente, campo de juego de la sustitución | La forma de jazz más habitual después del blues |
| **Stella by Starlight** | Young | Cadenas de ii-V, mezcla modal, resolución rota | Pone a prueba tu capacidad de seguir centros tonales que cambian rápidamente |
| **Giant Steps** | Coltrane | División simétrica por terceras mayores, Coltrane Changes | La carrera de obstáculos armónica definitiva |
| **So What** | Davis | Jazz modal, voicings por cuartas, vamp dórico | El nacimiento del jazz modal — dos acordes, posibilidades infinitas |

Estos temas forman un vocabulario básico. Un guitarrista de jazz que sepa conducir las voces, acompañar e improvisar sobre estos seis ha cubierto el paisaje armónico esencial de la tradición.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **ii-V-I** | La progresión de acordes fundamental del jazz: séptima sobre la supertónica, séptima de dominante, tónica — construida sobre un movimiento de fundamentales por quintas descendentes |
| **Voicing shell** | Un voicing mínimo que solo contiene la fundamental, la tercera y la séptima de un acorde |
| **Voicing drop-2** | Un voicing en posición cerrada reordenado bajando una octava la segunda nota más aguda |
| **Notas guía** | La tercera y la séptima de un acorde — las notas que definen su calidad e impulsan la conducción de voces |
| **Sustitución tritonal** | Reemplazar una séptima de dominante por otra séptima de dominante cuya fundamental está a un tritono (notas guía compartidas) |
| **Dominante backdoor** | Resolución a la tónica desde bVII7 en lugar de V7 |
| **Teoría acorde-escala** | La práctica de asignar una escala madre a cada calidad de acorde para improvisar |
| **Nota a evitar** | Un grado de la escala que crea una novena menor contra una nota del acorde cuando se sostiene |
| **Menor melódica** | La "escala madre" menor del jazz (1 2 b3 4 5 6 7) cuyos modos generan las escalas de dominantes alteradas y extendidas |
| **Voicing por cuartas** | Un acorde construido apilando cuartas justas en lugar de terceras |
| **Tríada de estructura superior** | Una tríada mayor o menor superpuesta a una séptima de dominante para crear extensiones |
| **Coltrane Changes** | Una técnica de rearmonización que divide la octava en tres centros tonales a una tercera mayor de distancia |
| **Conducción de voces** | El arte de enlazar acordes con un movimiento melódico mínimo en cada voz |
| **Extensiones** | Notas del acorde más allá de la séptima: 9.ª, 11.ª, 13.ª |
| **Alteraciones** | Extensiones elevadas o rebajadas cromáticamente: b9, #9, #11, b13 |

---

## Autoevaluación

**1. Deletrea las notas de un acorde Dm7b5 y nombra la escala que se le asocia con más frecuencia.**
> D F Ab C. La escala es el locrio (D Eb F G Ab Bb C) o el locrio #2 (D E F G Ab Bb C, el 6.º modo de la menor melódica).

**2. En un ii-V-I en Sib mayor, ¿cuáles son los tres acordes? Muestra cómo las notas guía del acorde de ii se conectan con las del acorde de V.**
> Cm7 - F7 - Bbmaj7. La 7.ª de Cm7 (Bb) desciende a la tercera de F7 (A). La tercera de Cm7 (Eb) se convierte en la 7.ª de F7 (Eb). Las notas guía intercambian sus papeles.

**3. ¿Cuál es la sustitución tritonal de G7 y por qué funciona?**
> Db7. Funciona porque G7 y Db7 comparten las mismas notas guía: B/Cb y F, con sus papeles de tercera y séptima intercambiados. Ambos resuelven a Cmaj7 con el mismo movimiento de conducción de voces.

**4. Nombra los tres centros tonales de Giant Steps y la relación geométrica entre ellos.**
> B, G y Eb. Son equidistantes en el círculo cromático, cada uno a una tercera mayor de distancia, y forman un triángulo equilátero en el círculo de quintas.

**5. Construye un voicing por cuartas empezando en A con cuartas justas apiladas (cuatro notas). ¿A qué acorde conocido se parece este voicing?**
> A - D - G - C. Es un Am7(11) o, de forma equivalente, un voicing C/A. La pila de cuartas contiene las notas de Am7 (A C G) más D (la 11.ª), pero sin el orden por terceras.

**Criterios de aprobación:** identificar todas las progresiones ii-V-I en una partitura guía desconocida, conducir las voces a través de ellas con al menos dos tipos de voicing, aplicar una técnica de sustitución y explicar la lógica de conducción de voces de cada enlace de acordes.

---

## Base de investigación

- El ii-V-I como progresión fundacional del jazz está documentado en todos los grandes textos de pedagogía del jazz y es la progresión estadísticamente más habitual del Great American Songbook
- La teoría acorde-escala procede principalmente de la tradición pedagógica de Berklee/NEC, formalizada por George Russell (Lydian Chromatic Concept, 1953) y sistematizada por Jamey Aebersold, Jerry Coker y Mark Levine
- El análisis de los Coltrane Changes se basa en la biografía de Lewis Porter y en la tesis doctoral de Demsey de 1991 sobre la armonía simétrica de Coltrane
- La conducción de voces por notas guía y la pedagogía armónica de Barry Harris representan la tradición de transmisión oral de la armonía del bebop
- Los sistemas de voicings drop-2 y drop-3 fueron codificados por Ted Greene, Mick Goodrick y el departamento de guitarra de Berklee
- Fuentes: Levine, *The Jazz Theory Book* (1995); Goodrick, *The Advancing Guitarist* y *Almanac of Guitar Voice Leading* (1987/2011); serie Aebersold Play-Along; Porter, *John Coltrane: His Life and Music* (1998)
- Estado de creencia: T(0.80) F(0.05) U(0.10) C(0.05)
