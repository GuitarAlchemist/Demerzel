---
module_id: mus-002-beyond-tonality
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

# Más allá de la tonalidad: teoría postonal para guitarristas

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración: 45 minutos

## Objetivos

Al terminar esta lección serás capaz de:
- Explicar la disolución histórica de la tonalidad clásica y la aparición del atonalismo
- Traducir alturas a notación entera de clases de altura y calcular la forma normal y la forma prima
- Construir vectores de intervalos e identificar clases de conjuntos por su número de Forte
- Derivar las cuatro formas de una serie dodecafónica y comprender la matriz de 12 × 12
- Analizar música atonal libre mediante la centricidad de altura, las células motívicas y la distribución registral
- Aplicar el pensamiento postonal al repertorio de guitarra moderno, así como a tu composición e improvisación
- Reconocer cómo la teoría de conjuntos tiende un puente con el análisis de los voicings de jazz

---

## 1. El final de la práctica común

Durante unos 300 años, de Bach a Brahms, la música culta occidental funcionó dentro de un sistema compartido llamado **tonalidad de la práctica común**. Ese sistema tenía una gramática clara: un centro tónico, armonía funcional (tónica — subdominante — dominante) y organización melódica en torno a las escalas diatónicas. Cada acorde tenía una función; cada nota tenía un destino.

A finales del siglo XIX, los compositores estiraron esa gramática hasta romperla. La ópera *Tristán e Isolda* de Wagner (1859) se abre con un acorde —el célebre «acorde de Tristán» (fa, si, re♯, sol♯)— que se niega a resolver de manera tradicional. Durante horas, Wagner aplaza la resolución esperada sobre la tónica y mantiene al oyente suspendido en la ambigüedad cromática. La ópera acaba resolviendo, pero el mensaje quedó claro: la función tonal podía retrasarse, debilitarse y finalmente disolverse.

Debussy, Mahler, Strauss y Scriabin continuaron esa expansión cromática. Los acordes acumularon tantas notas ajenas, extensiones alteradas y movimientos paralelos que el esqueleto tonal desapareció. A comienzos del siglo XX la pregunta se volvió inevitable: si los acordes ya no tienen que resolver, y si las tonalidades ya no obligan a nada, ¿qué queda?

**La emancipación de la disonancia de Schoenberg:**

Arnold Schoenberg respondió con una afirmación radical en 1908: **la disonancia no necesita resolver**. En la teoría tradicional, la consonancia era «natural» y la disonancia una desviación que debía corregirse. Schoenberg sostuvo que se trataba de una convención histórica, no de una ley acústica. Disonancia y consonancia no son opuestos: son puntos de un continuo, y los compositores deberían ser libres de emplear cualquier sonoridad como suceso estable.

Esta emancipación de la disonancia rompió la última restricción de la tonalidad. Las *Tres piezas para piano, op. 11* de Schoenberg (1909) suelen citarse como la primera obra «atonal». Sin armadura. Sin resolución sobre una tónica. Alturas organizadas por una lógica motívica y registral en lugar de por la armonía funcional.

**Dos caminos: atonalismo libre y serialismo:**

Tras la emancipación, los compositores se dividieron en dos caminos:

- **Atonalismo libre:** intuitivo, motívico, no sistematizado. Las alturas se eligen de oído y por lógica estructural. Schoenberg (1908-1920), Berg, el primer Webern, Varèse, Ives. El oído del compositor es la única autoridad.
- **Serialismo (técnica dodecafónica):** un método sistemático, desarrollado por Schoenberg en 1921, para organizar el material atonal. Cada composición se basa en una serie ordenada de las 12 clases de altura, manipulada mediante operaciones precisas. El sistema sustituyó la gramática tonal por una nueva.

Ambos caminos comparten el mismo fundamento: las 12 clases de altura del temperamento igual se tratan como un conjunto democrático, sin que ninguna nota tenga privilegio. Ese es el punto de partida de la teoría postonal.

---

## 2. La notación entera de clases de altura

La teoría postonal necesita una notación que trate las 12 clases de altura como equivalentes y abstractas. Los nombres tradicionales de las notas (do, re, mi…) son cómodos, pero arrastran el legado tonal: las grafías enarmónicas (do♯ frente a re♭) sugieren significados tonales distintos, irrelevantes en el análisis postonal.

La solución: la **notación entera**. Se asigna un entero a cada clase de altura:

| Altura | Entero |
|-------|---------|
| do     | 0       |
| do♯/re♭ | 1       |
| re     | 2       |
| re♯/mi♭ | 3       |
| mi     | 4       |
| fa     | 5       |
| fa♯/sol♭ | 6       |
| sol     | 7       |
| sol♯/la♭ | 8       |
| la     | 9       |
| la♯/si♭ | 10 (t)  |
| si     | 11 (e)  |

**Equivalencia de octava:** en el espacio de clases de altura, todos los do son «el mismo»: no hay un do central frente a un do grave. El entero 0 representa la clase de todos los do, en cualquier octava. Un conjunto de alturas se convierte en un conjunto de enteros módulo 12.

**Equivalencia enarmónica:** do♯ y re♭ son la misma clase de altura (1). El análisis postonal abandona la distinción tonal, pues no hay contexto tonal que la justifique.

**Forma normal:**

Dado un conjunto de alturas, la **forma normal** es su ordenación más compacta. Para hallarla:

1. Ordenar las clases de altura de manera ascendente alrededor del círculo cromático.
2. Considerar cada rotación del conjunto.
3. Elegir la rotación cuya extensión, del primer al último elemento, sea menor.
4. En caso de empate, elegir la que esté más comprimida hacia la izquierda (segundo elemento menor, luego tercero, etc.).

**Ejemplo:** el conjunto {mi, sol♯, do} = {4, 8, 0}. Rotaciones (con su extensión del primero al último alrededor del círculo):
- 0, 4, 8: extensión = 8
- 4, 8, 0: extensión = 8 (pues 0 vale «0 + 12 = 12», es decir 12 − 4 = 8)
- 8, 0, 4: extensión = 8

Todas las rotaciones son simétricas: se trata de un acorde aumentado. Por convención se retiene {0, 4, 8}.

**Forma prima:**

La **forma prima** es la representación más abstracta de una clase de conjuntos: borra a la vez las distinciones de transposición Y de inversión. Para hallarla:

1. Calcular la forma normal.
2. Calcular la forma normal de la inversión (invertir el conjunto en torno a 0 tomando el opuesto de cada elemento módulo 12, y luego normalizar).
3. Retener la más comprimida hacia la izquierda de las dos.
4. Transponer para que el primer elemento sea 0.

Las formas primas se escriben entre corchetes: [0,3,7] para el acorde menor, [0,4,7] para el mayor.

**Un momento: ¿son los acordes mayor y menor clases de conjuntos distintas?** Sí, pero sus formas primas están relacionadas por inversión: [0,3,7] (menor) se invierte en [0,4,7] (mayor). En la clasificación de Forte, ambos pertenecen a la clase de conjuntos **3-11**, ya que el sistema considera una sola clase a los conjuntos equivalentes por inversión. En la práctica, [0,3,7] es la forma prima canónica de la clase 3-11.

### Ejercicio práctico

Las cuerdas al aire de una guitarra en afinación estándar son mi, la, re, sol, si, mi. En enteros de clases de altura:
- mi = 4
- la = 9
- re = 2
- sol = 7
- si = 11

Tratando las cuerdas al aire como un conjunto (ignorando la duplicación de octava del mi): {2, 4, 7, 9, 11}.

Tu tarea:
1. Ordenar estos elementos de manera ascendente.
2. Determinar la forma normal.
3. Calcular la forma prima.

**Solución detallada:**
- Orden ascendente: {2, 4, 7, 9, 11}
- Rotaciones y extensiones:
  - (2, 4, 7, 9, 11): extensión = 11 − 2 = 9
  - (4, 7, 9, 11, 2+12=14): extensión = 14 − 4 = 10
  - (7, 9, 11, 14, 16): extensión = 9
  - (9, 11, 14, 16, 19): extensión = 10
  - (11, 14, 16, 19, 21): extensión = 10
- Rotaciones empatadas: (2,4,7,9,11) y (7,9,11,2,4). Se comparan los segundos elementos: 4 frente a 9. Se retiene 4. Forma normal: {2, 4, 7, 9, 11}.
- Transposición para empezar en 0: restar 2 a cada elemento → {0, 2, 5, 7, 9}.
- Comprobación de la inversión: invertir {0,2,5,7,9} → {0,−2,−5,−7,−9} módulo 12 = {0, 10, 7, 5, 3}. Reordenar: {0, 3, 5, 7, 10}. ¿Está más comprimida hacia la izquierda que {0,2,5,7,9}? Comparemos los segundos elementos, 2 frente a 3: gana {0,2,5,7,9} (2 < 3).
- **Forma prima: [0,2,5,7,9]** — es la clase de conjuntos 5-35, el **subconjunto pentatónico/diatónico** (la escala pentatónica anhemitónica). Las cuerdas al aire de la guitarra forman una clase de conjuntos pentatónica.

---

## 3. Vectores de intervalos y clases de conjuntos

Más allá del contenido de alturas, al análisis postonal le interesa el **contenido interválico**: qué intervalos hay en un conjunto y cuántos de cada uno. Eso es lo que captura el **vector de intervalos**.

**Clase de intervalo (ci):**

En teoría postonal, los intervalos se clasifican de 0 a 6 (solo existen 7 clases de intervalo, pues son simétricas en torno al tritono):

| ci | Semitonos | Ejemplo |
|----|-----------|---------|
| 0  | unísono/octava | do-do |
| 1  | segunda menor / séptima mayor | do-re♭ / do-si |
| 2  | segunda mayor / séptima menor | do-re / do-si♭ |
| 3  | tercera menor / sexta mayor | do-mi♭ / do-la |
| 4  | tercera mayor / sexta menor | do-mi / do-la♭ |
| 5  | cuarta justa / quinta justa | do-fa / do-sol |
| 6  | tritono | do-fa♯ |

Una segunda menor (1 semitono) y una séptima mayor (11 semitonos) pertenecen a la misma clase de intervalo, porque son inversión una de la otra.

**Construir el vector de intervalos:**

El vector de intervalos es una lista de 6 elementos que cuenta las apariciones de cada clase de intervalo (ci1 a ci6) entre todos los pares de notas de un conjunto.

**Ejemplo — el acorde perfecto de do mayor {0, 4, 7}:**
- Pares: (0,4), (0,7), (4,7)
- Intervalos: 4−0=4 (ci4), 7−0=7 (ci5), 7−4=3 (ci3)
- Recuento: ci1=0, ci2=0, ci3=1, ci4=1, ci5=1, ci6=0
- **Vector de intervalos: [001110]**

Fíjate en que el acorde mayor y el menor comparten el mismo vector [001110], porque están relacionados por inversión. Por eso pertenecen a la misma clase de conjuntos: **3-11**.

**Números de Forte:**

Allen Forte (1973) catalogó todas las clases de conjuntos de 3 a 9 notas y asignó un número a cada una. El formato es **cardinalidad-rango**:

- **3-11:** la 11.ª clase de conjuntos de cardinalidad 3 — el acorde perfecto mayor/menor.
- **3-12:** el acorde aumentado [0,4,8], vector de intervalos [000300].
- **4-20:** el acorde de séptima mayor [0,1,5,8], vector de intervalos [101220].
- **3-1:** el tricordio cromático [0,1,2], vector de intervalos [210000].
- **6-Z28 / 6-Z49:** hexacordios en relación Z (véase más abajo).

Los rangos reflejan un orden elegido por Forte según el contenido interválico, que va aproximadamente de lo más compacto (rangos más bajos) a lo más disperso.

**Relaciones Z:**

Algunas clases de conjuntos distintas comparten el mismo vector de intervalos, aunque su contenido de alturas difiera y no estén relacionadas ni por transposición ni por inversión. Se dice que están en **relación Z**, y Forte las marcó con el prefijo Z. El ejemplo más célebre: las clases 4-Z15 y 4-Z29 tienen ambas el vector [111111] (el «tetracordio de todos los intervalos»), y sin embargo son realmente distintas. Las relaciones Z fascinaron a Elliott Carter y Milton Babbitt, porque revelan una simetría profunda en el espacio de los intervalos.

### Ejercicio práctico

Calcula el vector de intervalos de **Misus4** en la guitarra. Misus4 se compone de mi, la, si, es decir las clases de altura {4, 9, 11}.

**Solución detallada:**
- Pares e intervalos:
  - (4, 9): 9 − 4 = 5 → ci5
  - (4, 11): 11 − 4 = 7 → ci5 (pues ci = mín(7, 12−7) = 5)
  - (9, 11): 11 − 9 = 2 → ci2
- Recuento: ci1=0, ci2=1, ci3=0, ci4=0, ci5=2, ci6=0
- **Vector de intervalos: [010020]**

Esta clase de conjuntos contiene una segunda mayor y dos cuartas/quintas justas. Su forma prima es [0,2,7], clase de conjuntos **3-9**. Es el tricordio cuartal, una sonoridad central en los voicings de jazz (el acompañamiento de la mano izquierda de McCoy Tyner, por ejemplo) y en la escritura orquestal del siglo XX (Copland, Hindemith).

---

## 4. Series dodecafónicas y operaciones seriales

El método dodecafónico de Schoenberg (1921) organiza el material atonal mediante una **serie ordenada**: una sucesión precisa que contiene las 12 clases de altura, cada una exactamente una vez. La serie es el código genético de la obra; toda melodía, toda armonía y todo contrapunto derivan de ella.

**Las cuatro formas de la serie:**

A partir de una **serie original (P0)**, el orden de partida, tres transformaciones generan tres formas emparentadas:

1. **Original (P):** la serie de partida.
2. **Retrógrado (R):** la serie tocada al revés (la última nota primero).
3. **Inversión (I):** cada intervalo de la serie original cambia de dirección. Si P asciende una tercera menor, I desciende una tercera menor.
4. **Retrógrado de la inversión (RI):** la inversión tocada al revés.

Cada forma puede **transponerse** a cualquiera de las 12 clases de altura, lo que da **48 formas en total** (4 operaciones × 12 transposiciones).

**Ejemplo — una serie sencilla:**

Sea P0 = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10] (serie inventada para el ejemplo).

- **R0:** invertir el orden de P0 → [10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 1, 0]
- **I0:** inversión en torno a 0. Para cada elemento x de P0, calcular (0 − x) módulo 12:
  - P0: [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10]
  - I0: [0, 11, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
- **RI0:** invertir el orden de I0 → [2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 11, 0]

**Transposición:** para crear P3 (forma original que empieza en la clase de altura 3), sumar 3 a cada elemento de P0 (módulo 12): [3, 4, 6, 5, 8, 7, 10, 9, 0, 11, 2, 1].

**La matriz de 12 × 12:**

La matriz dodecafónica muestra de forma compacta las 48 formas de la serie:

- **Las filas** (de izquierda a derecha) son las 12 transposiciones de P, denominadas P0 a P11 según su primera clase de altura.
- **Las filas leídas de derecha a izquierda** son los retrógrados (R0 a R11).
- **Las columnas** (de arriba abajo) son las 12 transposiciones de I, denominadas según su primera clase de altura.
- **Las columnas leídas de abajo arriba** son los retrógrados de la inversión.

Para construir la matriz:
1. Escribir P0 en la fila superior.
2. Escribir I0 en la columna izquierda (la inversión de P0, que empieza en la misma primera nota).
3. Cada fila siguiente es P0 transpuesta para que su primera nota coincida con la de la columna izquierda.

**Combinatorialidad:**

Algunas series tienen una propiedad especial, la **combinatorialidad**: al dividir la serie en dos hexacordios (las 6 primeras notas y las 6 últimas), una transposición dada de I produce hexacordios que, unidos a los de P, forman dos agregados completos (las 12 clases de altura en cada mitad). Schoenberg explotó ampliamente la combinatorialidad, porque permite enunciar P e I simultáneamente sin repetición de clase de altura: una especie de contrapunto dodecafónico que preserva el ideal atonal de no privilegiar ninguna nota.

### Ejercicio práctico

Sea **P0 = [7, 10, 8, 0, 5, 2, 4, 9, 11, 1, 3, 6]** (la apertura del *Concierto op. 24* de Webern, reordenada para el ejercicio):

1. Deriva **R0** invirtiendo el orden de P0.
2. Deriva **I0** calculando (7 − x + 7) módulo 12 para cada elemento, es decir, invirtiendo en torno a la primera nota. Método más sencillo: calcular (2 × 7 − x) módulo 12 para cada x de P0, lo que refleja cada nota en torno a la clase de altura 7.
3. Deriva **RI0** invirtiendo el orden de I0.

**Solución detallada:**

- **R0:** [6, 3, 1, 11, 9, 4, 2, 5, 0, 8, 10, 7]

- **I0** (inversión en torno a 7, fórmula (14 − x) módulo 12):
  - 7 → (14−7) mód 12 = 7
  - 10 → (14−10) mód 12 = 4
  - 8 → (14−8) mód 12 = 6
  - 0 → (14−0) mód 12 = 2
  - 5 → (14−5) mód 12 = 9
  - 2 → (14−2) mód 12 = 0
  - 4 → (14−4) mód 12 = 10
  - 9 → (14−9) mód 12 = 5
  - 11 → (14−11) mód 12 = 3
  - 1 → (14−1) mód 12 = 1
  - 3 → (14−3) mód 12 = 11
  - 6 → (14−6) mód 12 = 8
  - **I0: [7, 4, 6, 2, 9, 0, 10, 5, 3, 1, 11, 8]**

- **RI0:** invertir el orden de I0 → [8, 11, 1, 3, 5, 10, 0, 9, 2, 6, 4, 7]

Comprueba que cada serie contiene una sola vez cada clase de altura de 0 a 11.

---

## 5. El atonalismo libre

No toda la música atonal es serial. El **atonalismo libre** —la música de Schoenberg (1908-1920), del primer Berg, del primer Webern y de muchos compositores posteriores— organiza las alturas sin las restricciones sistemáticas de las series dodecafónicas. Se apoya, en cambio, en principios intuitivos.

**Centricidad de altura (sin tonalidad):**

Incluso sin tónica, ciertas alturas pueden adquirir importancia estructural mediante:
- **La repetición:** una altura que reaparece a lo largo de una pieza se convierte en punto de referencia.
- **El registro:** una altura situada sistemáticamente en un registro extremo (muy agudo o muy grave) gana relieve.
- **El ritmo:** una altura colocada en tiempos fuertes o en duraciones largas destaca.
- **El timbre:** una altura confiada constantemente a un instrumento característico se vuelve memorable.

Eso es la **centricidad de altura**: la emergencia de alturas focales sin el aparato funcional de la tonalidad. La altura es central no porque sea «la tónica», sino porque el compositor la ha destacado estructuralmente.

**Células motívicas:**

La música atonal libre suele apoyarse en pequeños conjuntos de clases de altura —las **células motívicas**— que constituyen su ADN estructural. Una célula es una clase de conjuntos de 3 a 5 notas que reaparece a lo largo de la pieza bajo diversas transposiciones, inversiones y disposiciones. Las *Cinco piezas para orquesta, op. 10* de Webern emplean apenas un puñado de clases de conjuntos en toda su duración: su economía resulta asombrosa.

La célula funciona como un leitmotiv wagneriano, pero en el plano de las clases de altura y no en el de la melodía. El oyente percibe una coherencia que no sabría explicar.

**Progresiones de clases de conjuntos:**

Una sucesión de clases de conjuntos a escala de una pieza puede crear un movimiento estructural de gran amplitud. Una pieza puede, por ejemplo, empezar con clases cromáticas pequeñas (3-1 [0,1,2]) y ampliarse progresivamente hacia clases más amplias y diatónicas (5-35 [0,2,4,7,9]). O al revés: un trayecto de la consonancia a la disonancia, o de la tensión a la distensión, sin recurrir a la cadencia tonal.

**Distribución registral:**

En la música atonal, el registro suele portar sentido estructural. Webern era célebre por distribuir las notas de un mismo acorde o de una misma línea melódica en registros extremos, fenómeno llamado **Klangfarbenmelodie** (melodía de timbres). El resultado: el oyente percibe la pieza tanto por el espacio y el timbre como por las alturas. Por tanto, el análisis postonal debe considerar dónde se sitúan las notas, y no solo qué clases de altura aparecen.

**Los ecos tonales de Berg:**

Alban Berg ocupa una posición intermedia apasionante. Sus obras (el *Concierto para violín*, por ejemplo) emplean series dodecafónicas que contienen subconjuntos tonales: acordes perfectos, séptimas de dominante, fragmentos diatónicos. De ahí resulta una música atonal que evoca sin cesar la memoria tonal sin comprometerse nunca con una tonalidad. La música de Berg enseña que «atonal» no significa «antitonal»: puede querer decir «tonal por fragmentos, pero no por gramática».

---

## 6. Aplicaciones a la guitarra y repertorio

Las técnicas postonales no son ejercicios abstractos: están ampliamente presentes en el repertorio de guitarra moderno y en la práctica de la improvisación.

**Henze — *Royal Winter Music* (1976):**

Las dos sonatas de Hans Werner Henze sobre personajes de Shakespeare figuran entre las obras atonales más importantes del repertorio de guitarra. *Royal Winter Music I* consta de seis movimientos (Gloucester, Romeo y Julieta, Ariel, Ofelia, Touchstone, Oberón). Cada personaje se retrata mediante un vocabulario de clases de altura propio: un pequeño conjunto de células motívicas desarrolladas a lo largo del movimiento. La sonata es atonal pero gestual, y sigue siendo reconocible como galería de retratos incluso sin centro tonal.

**Britten — *Nocturnal after John Dowland, op. 70* (1963):**

Esta obra maestra para guitarra sola toma un tema del compositor renacentista John Dowland y lo somete a ocho variaciones cada vez más alejadas de la tonalidad. Las primeras parecen inestables pero reconocibles; las centrales se disuelven en texturas atonales libres; la última, una pasacalle, recupera la claridad tonal. La obra es un recorrido por las técnicas postonales que se resuelve en la armonía clásica: una reconciliación más que un rechazo.

**Componer un estudio atonal — método práctico:**

He aquí un procedimiento para componer un breve estudio atonal para guitarra a partir de una célula de tres notas:

1. **Elegir una célula tricordal.** Ejemplo: la clase de conjuntos 3-3 [0,1,4], un agregado cromático más una tercera. En alturas: do, do♯, mi.
2. **Trasladarla a las posiciones CAGED.** Encontrar las transposiciones de [0,1,4] que caen de forma natural bajo cada una de las cinco formas CAGED. En la posición V (traste 5): la, si♭, do♯. En la posición III: sol, la♭, si. Y así sucesivamente.
3. **Componer frases que recorran las posiciones.** Cada frase enuncia la célula en una posición y luego se desliza hacia la siguiente. La identidad de la célula se conserva mientras su localización en el mástil se desplaza.
4. **Variar el registro, la dinámica, la articulación.** Aplicar la distribución registral del atonalismo libre: tocar unas células muy cerradas y otras extendidas a lo largo de dos octavas.
5. **Emplear la inversión y el retrógrado.** Enunciar [0,1,4], después su inversión [0,3,4], después su retrógrado, después el retrógrado de la inversión. El desarrollo motívico se hace mediante operaciones seriales.

Este método produce una música atonal, coherente y específicamente guitarrística: la geometría del mástil moldea la forma musical.

**Aplicaciones a la improvisación:**

Los guitarristas de jazz —Ben Monder, Kurt Rosenwinkel, Mary Halvorson— emplean con frecuencia técnicas atonales en sus improvisaciones: células tricordales, vectores de intervalos como guías de sonoridad, voicings cuartales y cromáticos. Comprender la teoría de conjuntos permite al improvisador moverse conscientemente entre los lenguajes tonal y postonal, tratándolos como un espectro unificado y no como sistemas opuestos.

---

## 7. El puente de vuelta

La teoría postonal no es un rechazo de la teoría tonal: es una generalización suya. Las herramientas forjadas para el análisis atonal iluminan la música tonal bajo una luz nueva y tienden un puente entre tradiciones que podrían parecer incompatibles.

**La teoría de conjuntos como herramienta de análisis de los voicings de jazz:**

La armonía de jazz es notoriamente compleja: extensiones, alteraciones, poliacordes, tríadas superiores. El análisis tonal tradicional tiene dificultades para describir un acorde como **Sol7alt(♭9,♯9,♭13)**. El análisis por clases de conjuntos, en cambio, lo reduce a un conjunto de clases de altura e identifica su clase directamente. El acorde anterior tiene como clases de altura {7, 11, 5, 9, 10, 3}; su forma prima es un hexacordio preciso, cuyo vector de intervalos caracteriza la sonoridad.

Los teóricos del jazz disponen así de un lenguaje que atraviesa las convenciones de cifrado. Dos acordes con cifrados distintos pueden pertenecer a la misma clase de conjuntos y, por tanto, compartir el mismo contenido interválico. Dos acordes con cifrados parecidos pueden pertenecer a clases distintas. La teoría de conjuntos revela la sonoridad real que hay bajo la notación.

**Los vectores de intervalos como medidas de sonoridad:**

El vector de intervalos cuantifica el «color» de un acorde. Un acorde rico en ci3 y ci4 (terceras) suena terciano. Un acorde dominado por los ci5 suena cuartal. Un acorde cargado de ci2 y ci6 suena denso y disonante. Al leer el vector de intervalos de un acorde puedes predecir su carácter sonoro sin siquiera oírlo.

Esto resulta inmediatamente útil para el guitarrista: para elegir el voicing de un acorde ambiguo, puedes quedarte con aquel cuyo vector de intervalos corresponda a la sonoridad buscada — abierta y cuartal, densa y cromática, o algo intermedio.

**OPTIC/K y la equivalencia de clases de altura:**

En la teoría neorriemanniana y transformacional, las equivalencias de conducción de voces se describen mediante las relaciones **OPTIC**:
- **O**ctava: dos alturas separadas por una octava son idénticas.
- **P**ermutación: reordenar dentro de una octava no cambia la identidad.
- **T**ransposición: dos acordes separados por un mismo intervalo son equivalentes.
- **I**nversión: dos acordes en espejo son equivalentes.
- **C**ardinalidad: las duplicaciones no cuentan.

Estos son exactamente los principios de la teoría de conjuntos de clases de altura, formulados de otro modo. OPTIC hace explícito que esa teoría no tiene nada de exótico: formaliza el modo en que los músicos siempre han oído las equivalencias (un acorde de do mayor es «el mismo» tanto si se dispone do-mi-sol, sol-do-mi o do-mi-sol-do).

La relación **K** añade una capa suplementaria, la equivalencia hasta la pertenencia a una clase de conjuntos. Juntas, OPTIC y K forman un marco matemático que unifica el análisis tonal de la conducción de voces y la teoría postonal de conjuntos. Ambas tradiciones no se oponen: son dos dialectos de una misma lengua.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Tonalidad de la práctica común** | El sistema armónico de la música culta occidental, de aproximadamente 1600 a 1900, basado en la armonía funcional y los centros tonales |
| **Emancipación de la disonancia** | La afirmación de Schoenberg, en 1908, de que las sonoridades disonantes no tienen que resolver sobre una consonancia |
| **Atonalismo** | Música organizada sin centro tonal ni tonalidad |
| **Atonalismo libre** | Música atonal organizada intuitivamente mediante células motívicas, distribución registral y centricidad de altura |
| **Serialismo (dodecafonismo)** | Organización sistemática de la música atonal a partir de una serie ordenada de 12 clases de altura |
| **Clase de altura** | Clase de equivalencia de las alturas relacionadas por la octava (todos los do pertenecen a la clase 0) |
| **Notación entera** | Representación de las clases de altura mediante los enteros de 0 a 11 |
| **Forma normal** | La ordenación más compacta de un conjunto de clases de altura |
| **Forma prima** | El representante canónico de una clase de conjuntos, incluida la equivalencia por inversión, transpuesto para empezar en 0 |
| **Clase de intervalo (ci)** | Clase de equivalencia de los intervalos (0 a 6) que agrupa los relacionados por inversión |
| **Vector de intervalos** | Lista de 6 elementos que cuenta las apariciones de cada clase de intervalo en un conjunto |
| **Clase de conjuntos** | Grupo de conjuntos de clases de altura relacionados por transposición e inversión, designado por un número de Forte |
| **Número de Forte** | La etiqueta del catálogo de Allen Forte para una clase de conjuntos, en formato cardinalidad-rango (por ejemplo 3-11) |
| **Relación Z** | Relación entre clases de conjuntos distintas que comparten el mismo vector de intervalos |
| **Original/Retrógrado/Inversión/Retrógrado de la inversión (P/R/I/RI)** | Las cuatro operaciones seriales aplicadas a una serie dodecafónica |
| **Combinatorialidad** | Propiedad de ciertas series cuyos hexacordios, combinados con formas transpuestas, producen agregados |
| **Centricidad de altura** | Realce estructural de ciertas alturas en música atonal, sin función tonal |
| **Célula motívica** | Pequeño conjunto de clases de altura que sirve de ADN estructural a una composición atonal |

---

## Autoevaluación

**1. ¿Qué entendía Schoenberg por «emancipación de la disonancia» y por qué fue un punto de inflexión histórico?**
> Schoenberg afirmó en 1908 que las sonoridades disonantes no necesitan resolver sobre consonancias, y que la distinción entre consonancia y disonancia es una convención histórica, no una ley acústica. Fue un punto de inflexión porque levantaba la última restricción de la tonalidad clásica —la obligación de resolver la tensión— y abría la vía a una composición atonal en la que cualquier sonoridad podía valer como suceso estructural estable.

**2. Calcula la forma prima del conjunto {re, fa, la, do} (un acorde de re menor séptima). Muestra la forma normal y una comprobación de inversión.**
> Clases de altura: {2, 5, 9, 0} → orden ascendente {0, 2, 5, 9}. Rotaciones y extensiones:
> - (0, 2, 5, 9): extensión = 9
> - (2, 5, 9, 0+12=12): extensión = 10
> - (5, 9, 12, 14): extensión = 9
> - (9, 12, 14, 17): extensión = 8 — ¡la menor!
> Forma normal: {9, 0, 2, 5}. Transposición para empezar en 0: restar 9 → {0, 3, 5, 8}. Inversión: {0, −3, −5, −8} módulo 12 = {0, 9, 7, 4} → reordenar {0, 4, 7, 9}. Comparación de {0,3,5,8} y {0,4,7,9}: el segundo elemento 3 < 4, luego {0,3,5,8} está más comprimido hacia la izquierda.
> **Forma prima: [0,3,5,8]** — clase de conjuntos 4-26, la sonoridad de séptima menor (acorde menor más séptima).

**3. Sea P0 = [0, 1, 4, 9, 5, 11, 2, 7, 6, 10, 3, 8]. Deriva I0 (inversión que empieza en 0). Indica la fórmula empleada.**
> Fórmula: I0[k] = (0 − P0[k]) módulo 12 = (−P0[k]) módulo 12.
> - 0 → 0
> - 1 → 11
> - 4 → 8
> - 9 → 3
> - 5 → 7
> - 11 → 1
> - 2 → 10
> - 7 → 5
> - 6 → 6
> - 10 → 2
> - 3 → 9
> - 8 → 4
> **I0: [0, 11, 8, 3, 7, 1, 10, 5, 6, 2, 9, 4]**

**4. ¿Qué es una relación Z y por qué importa en la teoría postonal?**
> Una relación Z es la propiedad que comparten dos clases de conjuntos distintas con vectores de intervalos idénticos, sin estar relacionadas por transposición ni por inversión. Importa porque revela que el contenido interválico —qué intervalos hay— no determina por sí solo la identidad de la clase de conjuntos, es decir, qué configuraciones de alturas producen esos intervalos. Los conjuntos en relación Z suenan de forma muy parecida pero son estructuralmente distintos: una simetría profunda, explotada por compositores como Elliott Carter y Milton Babbitt.

**5. ¿En qué sentido el análisis por teoría de conjuntos tiende un puente entre la música postonal y la armonía de jazz?**
> La teoría de conjuntos abstrae los acordes en conjuntos y clases de clases de altura, liberándose de las convenciones de cifrado. Un acorde de dominante alterada complejo puede identificarse por su clase de conjuntos y caracterizarse por su vector de intervalos, lo que saca a la luz su sonoridad subyacente allí donde el cifrado la enmascara. Los analistas del jazz pueden así comparar voicings de cualidades aparentemente distintas, detectar sonoridades comunes y entender los lenguajes atonal y jazzístico como dos dialectos de un mismo marco de clases de altura, y no como sistemas opuestos.

**Criterios de logro:** calcular la forma prima de un acorde dado de 4 a 5 notas, derivar I0 y R0 a partir de una P0 dada, y explicar la función estructural de una célula motívica en un contexto atonal libre.

---

## Bases de la investigación

- La teoría de conjuntos de clases de altura fue formalizada por Allen Forte en *The Structure of Atonal Music* (1973); los números de Forte siguen siendo el sistema de catalogación de referencia
- *Introduction to Post-Tonal Theory* de Joseph N. Straus (4.ª ed., 2016) es el manual pedagógico de referencia y la fuente de los algoritmos de forma normal y forma prima
- *Serial Composition and Atonality* de George Perle (6.ª ed., 1991) aporta las bases históricas y analíticas de la técnica dodecafónica
- La teoría neorriemanniana y las relaciones OPTIC prolongan la teoría de conjuntos hacia el análisis de la conducción de voces (Cohn, 2012; Tymoczko, *A Geometry of Music*, 2011)
- Repertorio de guitarra citado: Henze, *Royal Winter Music I & II*; Britten, *Nocturnal op. 70*; Takemitsu, *All in Twilight*; Ginastera, *Sonata op. 47*
- Los escritos del propio Schoenberg (*Style and Idea*, 1950) documentan la emancipación de la disonancia en sus propias palabras
- Fuentes: Forte 1973, Straus 2016, Perle 1991, Tymoczko 2011, Cohn 2012, Schoenberg 1950
- Estado de creencia: T(0.85) F(0.03) U(0.08) C(0.04)
