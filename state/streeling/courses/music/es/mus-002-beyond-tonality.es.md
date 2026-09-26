---
module_id: mus-002-beyond-tonality
department: music
course: "Fundamentos de teoría musical"
level: intermediate
alchemical_stage: albedo
prerequisites:
  - mus-001-what-is-a-chord
estimated_duration: "45 minutes"
produced_by: music
version: "1.0.0"
---

# Más allá de la tonalidad: teoría postonal para guitarristas

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración: 45 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Explicar la disolución histórica de la tonalidad de la práctica común y el surgimiento de la atonalidad
- Traducir alturas a notación entera de clases de altura y calcular formas normales y formas primas
- Construir vectores interválicos e identificar clases de conjuntos mediante los números de Forte
- Derivar las cuatro formas de una serie dodecafónica y comprender la matriz 12x12
- Analizar la música atonal libre a través de la centralidad de altura, las células motívicas y la distribución de registros
- Aplicar el pensamiento postonal al repertorio moderno de guitarra y a tu propia composición/improvisación
- Reconocer cómo la teoría de conjuntos tiende un puente de vuelta al análisis de voicings de jazz

---

## 1. El fin de la práctica común

Durante unos 300 años — de Bach a Brahms — la música académica occidental funcionó dentro de un sistema compartido llamado **tonalidad de la práctica común**. Este sistema tenía una gramática clara: un centro tonal, una armonía funcional (tónica-subdominante-dominante) y una organización melódica en torno a las escalas diatónicas. Cada acorde tenía un papel; cada nota tenía un destino.

A finales del siglo XIX, los compositores empezaron a estirar esta gramática hasta que se rompió. La ópera de Wagner *Tristan und Isolde* (1859) comienza con un acorde — el famoso «acorde de Tristán» (Fa-Si-Re#-Sol#) — que se niega a resolver de cualquier manera tradicional. Durante varias horas de música, Wagner aplaza la resolución esperada en la tónica y mantiene al oyente suspendido en la ambigüedad cromática. La ópera termina con una resolución, pero el mensaje estaba claro: la función tonal podía retrasarse, debilitarse y finalmente disolverse.

Debussy, Mahler, Strauss y Scriabin continuaron esta expansión cromática. Los acordes se cargaron tanto de notas ajenas, extensiones alteradas y movimiento paralelo que el esqueleto tonal subyacente desapareció. A principios del siglo XX, la pregunta se volvió inevitable: si los acordes ya no necesitan resolver y las tonalidades ya no son vinculantes, ¿qué queda?

**La emancipación de la disonancia de Schoenberg:**

Arnold Schoenberg respondió a la pregunta en su música desde 1908, y más tarde llamó a este principio «emancipación de la disonancia» (ensayo «Opinion or Insight?», 1926, recogido en *Style and Idea*): **la disonancia no necesita resolver**. En la teoría tradicional, la consonancia era «natural» y la disonancia una desviación que debía corregirse. Schoenberg sostuvo que eso era una convención histórica, no una ley acústica. Disonancia y consonancia no son opuestos — son puntos de un continuo, y los compositores deberían ser libres de usar cualquier sonoridad como un evento estable.

Esta emancipación de la disonancia rompió la última restricción de la tonalidad. Las *Tres piezas para piano, op. 11* (1909) de Schoenberg se citan a menudo como la primera obra «atonal». Sin armadura. Sin resolución en una tónica. Alturas organizadas por una lógica motívica y de registro en lugar de por la armonía funcional.

**Dos caminos: atonalidad libre frente a serialismo:**

Tras la emancipación, los compositores siguieron dos caminos distintos:

- **Atonalidad libre:** intuitiva, motívica, no sistematizada. Alturas elegidas de oído y por lógica estructural. Schoenberg (1908-1920), Berg, el primer Webern, Varese, Ives. El oído del compositor es la única autoridad.
- **Serialismo (técnica dodecafónica):** un método sistemático que Schoenberg desarrolló en 1921 para organizar el material de alturas atonal. Cada composición se basa en una serie ordenada de las 12 clases de altura, manipulada mediante operaciones concretas. El sistema sustituyó la gramática tonal por una nueva.

Ambos caminos comparten el mismo fundamento: las 12 clases de altura del temperamento igual se tratan como un conjunto democrático, sin que ninguna nota tenga privilegio sobre otra. Este es el punto de partida de la teoría postonal.

---

## 2. Notación entera de clases de altura

La teoría postonal necesita una notación que trate las 12 clases de altura como equivalentes y abstractas. Los nombres tradicionales de las notas (Do, Re, Mi...) son prácticos, pero arrastran un bagaje tonal — las grafías enarmónicas (Do# frente a Reb) sugieren significados tonales distintos que son irrelevantes en el análisis postonal.

La solución: la **notación entera**. Asigna un entero a cada clase de altura:

| Altura | Entero |
|-------|---------|
| Do    | 0       |
| Do#/Reb | 1     |
| Re    | 2       |
| Re#/Mib | 3     |
| Mi    | 4       |
| Fa    | 5       |
| Fa#/Solb | 6    |
| Sol   | 7       |
| Sol#/Lab | 8    |
| La    | 9       |
| La#/Sib | 10 (t) |
| Si    | 11 (e)  |

**Equivalencia de octava:** en el espacio de clases de altura, todos los Do son «el mismo» — no hay Do central frente a Do grave. El entero 0 representa la clase de todos los Do en todas las octavas. Un conjunto de alturas se convierte en un conjunto de enteros módulo 12.

**Equivalencia enarmónica:** Do# y Reb son la misma clase de altura (1). El análisis postonal descarta la distinción tonal porque no hay un contexto de tonalidad que la justifique.

**Forma normal:**

Dado un conjunto de alturas, la **forma normal** es la ordenación más compacta del conjunto. Para encontrarla:

1. Ordena las clases de altura de forma ascendente alrededor del círculo cromático.
2. Considera cada rotación del conjunto.
3. Elige la rotación con la menor extensión del primer al último elemento.
4. Si varias rotaciones empatan, compara sus **intervalos medidos desde el primer elemento** (transporta cada rotación para que empiece en 0), no los números de las clases de altura. La regla de Forte elige la rotación más apretada hacia la izquierda: el menor intervalo del primer al segundo elemento, luego del primero al tercero, etc. La regla de Rahn, que usa la mayoría de las tablas actuales (p. ej., Open Music Theory), compara desde la derecha: el menor intervalo del primer al penúltimo elemento, luego del primero al anterior a ese, etc. Las dos reglas coinciden en todos los conjuntos de este módulo; dan formas primas distintas solo en 6 de las 224 clases de conjuntos (p. ej., 5-20: Rahn (01568), Forte (01378)).

**Ejemplo:** el conjunto {Mi, Sol#, Do} = {4, 8, 0}. Rotaciones (como intervalos del primero al último alrededor del círculo):
- 0, 4, 8: extensión = 8
- 4, 8, 0: extensión = 8 (pero 0 significa «0 + 12 = 12», así que extensión = 12 - 4 = 8)
- 8, 0, 4: extensión = 8

Todas las rotaciones son simétricas (es una tríada aumentada). Por convención, elegimos {0, 4, 8}.

**Forma prima:**

La **forma prima** es la representación más abstracta de una clase de conjuntos — elimina las distinciones de transposición E inversión. Para encontrar la forma prima:

1. Calcula la forma normal y transpórtala para que el primer elemento sea 0.
2. Calcula la forma normal de la inversión (invierte el conjunto alrededor de 0 cambiando el signo de cada elemento mod 12 y luego normaliza) y transpórtala para que el primer elemento sea 0.
3. Elige la más apretada de las dos, con la misma regla de desempate que para la forma normal.

Los conjuntos de clases de altura en forma normal se escriben entre corchetes, p. ej. [0,4,7]; las formas primas, que nombran toda una clase de conjuntos, se escriben entre paréntesis y sin comas: (037) es la forma prima tanto de la tríada mayor como de la menor.

**Un momento — ¿las tríadas mayor y menor son clases de conjuntos distintas?** Solo con transposición, sí: ninguna transposición convierte Do mayor [0,4,7] en una tríada menor. Pero las clases de conjuntos de la teoría postonal (las de Forte) se definen salvo transposición **e** inversión, e invertir Do mayor [0,4,7] alrededor de 0 da Fa menor [5,8,0]. Así, las tríadas mayor y menor pertenecen a la **misma clase de conjuntos, 3-11**, con la única forma prima (037). Los catálogos que separan las formas relacionadas por inversión (los «tipos Tn», solo con transposición) etiquetan la forma menor [0,3,7] como 3-11A y la forma mayor [0,4,7] como 3-11B.

### Ejercicio práctico

Las cuerdas al aire de una guitarra (afinación estándar) son Mi-La-Re-Sol-Si-Mi. Convertidas a enteros de clases de altura:
- Mi = 4
- La = 9
- Re = 2
- Sol = 7
- Si = 11

Tratando las cuerdas al aire como un conjunto (ignorando la duplicación a la octava de Mi): {2, 4, 7, 9, 11}.

Tu tarea:
1. Ordénalas de forma ascendente.
2. Determina la forma normal.
3. Calcula la forma prima.

**Solución paso a paso:**
- Ascendente: {2, 4, 7, 9, 11}
- Rotaciones y extensiones:
  - (2, 4, 7, 9, 11): extensión = 11 - 2 = 9
  - (4, 7, 9, 11, 2+12=14): extensión = 14 - 4 = 10
  - (7, 9, 11, 14, 16): extensión = 9
  - (9, 11, 14, 16, 19): extensión = 10
  - (11, 14, 16, 19, 21): extensión = 10
- Rotaciones empatadas: (2,4,7,9,11) y (7,9,11,2,4). Compara sus intervalos desde el primer elemento, no las clases de altura: (2,4,7,9,11) → 0, 2, 5, 7, 9 y (7,9,11,14,16) → 0, 2, 4, 7, 9. Desde la izquierda, los segundos elementos empatan (2 frente a 2) y los terceros deciden (4 < 5); desde la derecha, los penúltimos empatan (7 frente a 7) y los anteriores deciden (4 < 5). Ambas reglas eligen (7,9,11,2,4). Forma normal: [7, 9, 11, 2, 4] (Sol, La, Si, Re, Mi).
- Transporta para empezar en 0: resta 7 a cada elemento → [0, 2, 4, 7, 9].
- Comprueba la inversión: invierte {2,4,7,9,11} → {10, 8, 5, 3, 1}. Ascendente: {1, 3, 5, 8, 10}. Sus rotaciones empatadas (extensión 9) son (1,3,5,8,10) → 0, 2, 4, 7, 9 y (8,10,1,3,5) → 0, 2, 5, 7, 9; la más apretada vuelve a dar [0, 2, 4, 7, 9], igual que el original: esta clase de conjuntos es simétrica por inversión.
- **Forma prima: (02479)** — es la clase de conjuntos 5-35, el **subconjunto pentatónico/diatónico** (la escala pentatónica anhemitónica). Las cuerdas al aire de la guitarra forman una clase de conjuntos pentatónica: pentatónica mayor de Sol, Sol La Si Re Mi.

---

## 3. Vectores interválicos y clases de conjuntos

Más allá del contenido de alturas, al análisis postonal le importa el **contenido interválico** — qué intervalos están presentes en un conjunto y cuántos de cada uno. Esto lo recoge el **vector interválico**.

**Clase interválica (ic):**

En teoría postonal, los intervalos se clasifican del 0 al 6 (solo hay 7 clases interválicas porque las clases interválicas son simétricas alrededor del tritono):

| ic | Semitonos | Ejemplo |
|----|-----------|---------|
| 0  | unísono/octava | Do-Do |
| 1  | segunda menor / séptima mayor | Do-Reb / Do-Si |
| 2  | segunda mayor / séptima menor | Do-Re / Do-Sib |
| 3  | tercera menor / sexta mayor | Do-Mib / Do-La |
| 4  | tercera mayor / sexta menor | Do-Mi / Do-Lab |
| 5  | cuarta justa / quinta justa | Do-Fa / Do-Sol |
| 6  | tritono | Do-Fa# |

Una segunda menor (1 semitono) y una séptima mayor (11 semitonos) son la misma clase interválica porque son inversiones una de la otra.

**Construir el vector interválico:**

El vector interválico es una lista de 6 elementos que cuenta cuántas veces aparece cada clase interválica (ic1 a ic6) entre todos los pares de notas de un conjunto.

**Ejemplo — tríada de Do mayor {0, 4, 7}:**
- Pares: (0,4), (0,7), (4,7)
- Intervalos: 4-0=4 (ic4), 7-0=7 (ic5), 7-4=3 (ic3)
- Recuento: ic1=0, ic2=0, ic3=1, ic4=1, ic5=1, ic6=0
- **Vector interválico: [001110]**

Fíjate: la tríada mayor y la tríada menor comparten el mismo vector interválico [001110] porque están relacionadas por inversión, y la inversión conserva las clases interválicas. Estar relacionadas por inversión es también la razón de que pertenezcan a la misma clase de conjuntos, **3-11**. Lo contrario no se cumple: dos conjuntos con el mismo vector interválico no tienen por qué pertenecer a la misma clase de conjuntos (ver las relaciones Z más abajo).

**Números de Forte:**

Allen Forte (1973) catalogó todas las clases de conjuntos posibles de 3 a 9 notas y asignó a cada una un número. El formato es **cardinalidad-ordinal**:

- **3-11:** la 11.ª clase de conjuntos de cardinalidad 3 — la tríada mayor/menor.
- **3-12:** la tríada aumentada (048), vector interválico [000300].
- **4-20:** el acorde de séptima mayor (0158), vector interválico [101220].
- **3-1:** el tricordio cromático (012), vector interválico [210000].
- **6-Z28 / 6-Z49:** hexacordios en relación Z (ver más abajo).

Los ordinales reflejan un orden que Forte eligió según el contenido interválico, aproximadamente del más compacto (ordinales más bajos) al más disperso.

**Relaciones Z:**

Algunas clases de conjuntos distintas comparten el mismo vector interválico pese a tener contenidos de alturas diferentes y no estar relacionadas por transposición ni por inversión. Se llaman conjuntos **en relación Z**. Forte los marcó con un prefijo Z. El ejemplo más famoso: las clases de conjuntos 4-Z15 y 4-Z29 tienen ambas el vector interválico [111111] (el «tetracordio de todos los intervalos»), pero son conjuntos realmente diferentes. Las relaciones Z fascinaron a Elliott Carter y a Milton Babbitt porque representan una simetría profunda del espacio interválico.

### Ejercicio práctico

Calcula el vector interválico de **Esus4** en la guitarra. Esus4 consta de Mi, La, Si — clases de altura {4, 9, 11}.

**Solución paso a paso:**
- Pares e intervalos:
  - (4, 9): 9 - 4 = 5 → ic5
  - (4, 11): 11 - 4 = 7 → ic5 (porque ic = min(7, 12-7) = 5)
  - (9, 11): 11 - 9 = 2 → ic2
- Recuento: ic1=0, ic2=1, ic3=0, ic4=0, ic5=2, ic6=0
- **Vector interválico: [010020]**

Esta clase de conjuntos contiene un intervalo de segunda mayor y dos intervalos de cuarta/quinta justa. Su forma prima es (027), clase de conjuntos **3-9**. Es el tricordio cuartal — una sonoridad central en los voicings de jazz (p. ej., el acompañamiento de mano izquierda de McCoy Tyner) y en la escritura orquestal del siglo XX (Copland, Hindemith).

---

## 4. Series dodecafónicas y operaciones seriales

El método dodecafónico de Schoenberg (1921) organizaba el material de alturas atonal mediante una **serie ordenada** — una secuencia concreta que contiene las 12 clases de altura, cada una exactamente una vez. La serie funciona como el código genético de la composición; cada melodía, armonía y contrapunto deriva de ella.

**Las cuatro formas de la serie:**

Dada una **serie original (P0)** — el orden de partida —, tres transformaciones generan tres formas relacionadas:

1. **Original (P):** la serie de partida.
2. **Retrógrada (R):** la serie tocada al revés (la última nota primero).
3. **Inversión (I):** cada intervalo de la serie original cambia de dirección. Si P sube una tercera menor, I baja una tercera menor.
4. **Retrógrada de la inversión (RI):** la inversión tocada al revés.

Cada forma puede **transportarse** para empezar en cualquiera de las 12 clases de altura, lo que da **48 formas de serie en total** (4 operaciones × 12 transposiciones).

**Ejemplo — una serie sencilla:**

Sea P0 = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10] (una serie inventada).

- **R0:** P0 al revés → [10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 1, 0]
- **I0:** inversión alrededor de 0. Para cada elemento x de P0, calcula (0 - x) mod 12:
  - P0: [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10]
  - I0: [0, 11, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
- **RI0:** I0 al revés → [2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 11, 0]

**Transposición:** para crear P3 (forma original que empieza en la clase de altura 3), suma 3 a cada elemento de P0 (mod 12): [3, 4, 6, 5, 8, 7, 10, 9, 0, 11, 2, 1].

**La matriz 12x12:**

Una matriz dodecafónica es una forma compacta de mostrar las 48 formas de la serie:

- Las **filas** (de izquierda a derecha) son las 12 transposiciones de P, etiquetadas de P0 a P11 según su nivel de transposición respecto de P0 (su primera clase de altura cuando P0 empieza en 0).
- Las **filas leídas de derecha a izquierda** son las retrógradas (R0 a R11).
- Las **columnas** (de arriba abajo) son las 12 transposiciones de I, etiquetadas según su primera clase de altura.
- Las **columnas leídas de abajo arriba** son las retrógradas de las inversiones.

Para construir la matriz:
1. Escribe P0 en la fila superior.
2. Escribe I0 en la columna izquierda (la inversión de P0, empezando en la misma primera nota).
3. Cada fila siguiente es P0 transportada de modo que su primera nota coincida con la columna de más a la izquierda.

**Combinatoriedad:**

Algunas series tienen una propiedad especial llamada **combinatoriedad**: si divides la serie en dos hexacordios (las 6 primeras notas y las 6 últimas), una transposición concreta de I produce hexacordios que, junto con los de P, forman dos agregados completos (las 12 clases de altura en cada mitad). Schoenberg explotó mucho la combinatoriedad porque permite enunciar P e I simultáneamente sin repetir clases de altura — una especie de contrapunto dodecafónico que preserva el ideal atonal de no privilegio.

### Ejercicio práctico

Dada **P0 = [7, 10, 8, 0, 5, 2, 4, 9, 11, 1, 3, 6]** (el comienzo del *Concierto, op. 24* de Webern, reordenado para este ejercicio):

1. Deriva **R0** invirtiendo el orden de P0.
2. Deriva **I0** calculando (7 - x + 7) mod 12 para cada elemento — es decir, invirtiendo alrededor de la primera nota. Un método más sencillo: calcula (2 × 7 - x) mod 12 para cada x de P0, lo que refleja cada nota alrededor de la clase de altura 7.
3. Deriva **RI0** invirtiendo el orden de I0.

**Solución paso a paso:**

- **R0:** [6, 3, 1, 11, 9, 4, 2, 5, 0, 8, 10, 7]

- **I0** (inversión alrededor de 7, fórmula (14 - x) mod 12):
  - 7 → (14-7) mod 12 = 7
  - 10 → (14-10) mod 12 = 4
  - 8 → (14-8) mod 12 = 6
  - 0 → (14-0) mod 12 = 2
  - 5 → (14-5) mod 12 = 9
  - 2 → (14-2) mod 12 = 0
  - 4 → (14-4) mod 12 = 10
  - 9 → (14-9) mod 12 = 5
  - 11 → (14-11) mod 12 = 3
  - 1 → (14-1) mod 12 = 1
  - 3 → (14-3) mod 12 = 11
  - 6 → (14-6) mod 12 = 8
  - **I0: [7, 4, 6, 2, 9, 0, 10, 5, 3, 1, 11, 8]**

- **RI0:** I0 al revés → [8, 11, 1, 3, 5, 10, 0, 9, 2, 6, 4, 7]

Comprueba que cada serie contiene cada clase de altura de 0 a 11 exactamente una vez.

---

## 5. La atonalidad libre

No toda la música atonal es serial. La **atonalidad libre** — la música de Schoenberg (1908-1920), del primer Berg, del primer Webern y de muchos compositores posteriores — organiza las alturas sin las restricciones sistemáticas de las series dodecafónicas. En su lugar, se apoya en principios intuitivos:

**Centralidad de altura (sin tonalidad):**

Incluso sin tónica, ciertas alturas pueden ganar protagonismo estructural mediante:
- **La repetición:** una altura que reaparece a lo largo de una pieza se convierte en un punto de referencia.
- **El registro:** una altura situada sistemáticamente en un registro extremo (muy agudo o muy grave) adquiere énfasis.
- **El ritmo:** una altura asignada a tiempos fuertes o a duraciones largas destaca.
- **El timbre:** una altura presentada sistemáticamente por un instrumento característico se vuelve memorable.

Esta es la **centralidad de altura**: la aparición de alturas focales sin el aparato funcional de la tonalidad. La altura es central no porque sea «la tónica», sino porque el compositor la ha enfatizado estructuralmente.

**Células motívicas:**

La música atonal libre suele apoyarse en pequeños conjuntos de clases de altura — **células motívicas** — como su ADN estructural. Una célula es una clase de conjuntos de 3 a 5 notas que aparece a lo largo de una pieza en diversas transposiciones, inversiones y disposiciones. Las *Cinco piezas para orquesta, op. 10* de Webern usan solo un puñado de clases de conjuntos en toda su duración; la economía es asombrosa.

La célula funciona como un leitmotiv wagneriano, pero en el nivel de las clases de altura en lugar del nivel melódico. El oyente percibe coherencia sin poder explicar por qué.

**Progresiones de clases de conjuntos:**

Una sucesión de clases de conjuntos a lo largo de una pieza puede crear un movimiento estructural a gran escala. Por ejemplo, una pieza podría empezar con clases de conjuntos pequeñas y cromáticas (3-1, (012)) y expandirse poco a poco hacia clases más grandes y diatónicas (5-35, (02479)). O al revés: un viaje de la consonancia a la disonancia, o de la tensión a la distensión, sin depender de la cadencia tonal.

**Distribución de registros:**

En la música atonal, el registro suele tener un significado estructural. Webern era famoso por repartir las notas de un mismo acorde o de una misma línea melódica entre registros extremos, y por hacer pasar una línea de un instrumento a otro — este segundo procedimiento se llama **Klangfarbenmelodie** (melodía de timbres, término de Schoenberg en la última página de su *Harmonielehre*, 1911). El resultado: el oyente percibe la pieza tanto a través del espacio y el timbre como a través de la altura. El análisis postonal debe tener en cuenta dónde se colocan las notas, no solo qué clases de altura aparecen.

**Los ecos tonales de Berg:**

Alban Berg ocupa un fascinante término medio. Sus obras (p. ej., el *Concierto para violín*) usan series dodecafónicas que contienen subconjuntos tonales — tríadas, séptimas de dominante, fragmentos diatónicos. El resultado es una música atonal que evoca una y otra vez la memoria tonal sin comprometerse nunca con una tonalidad. La música de Berg enseña que «atonal» no significa «antitonal» — puede significar «tonal a fragmentos, pero no en su gramática».

---

## 6. Aplicaciones a la guitarra y repertorio

Las técnicas postonales no son ejercicios abstractos — tienen una presencia rica en el repertorio moderno de guitarra y en la práctica de la improvisación.

**Henze — *Royal Winter Music* (1976):**

Las dos sonatas de Hans Werner Henze sobre personajes de Shakespeare están entre las obras atonales más importantes del repertorio de guitarra. *Royal Winter Music I* tiene seis movimientos (Gloucester, Romeo and Juliet, Ariel, Ophelia, Touchstone, Oberon). Cada personaje se retrata con un vocabulario de clases de altura propio — un pequeño conjunto de células motívicas que se desarrollan a lo largo del movimiento. La sonata es atonal pero gestual: se reconocen retratos de personajes incluso sin centros tonales.

**Britten — *Nocturnal after John Dowland, op. 70* (1963):**

La obra maestra de Britten para guitarra sola toma un tema del compositor renacentista John Dowland y lo somete a ocho variaciones cada vez más alejadas de la tonalidad. Las primeras variaciones suenan inestables pero reconocibles; las variaciones centrales se disuelven en texturas atonales libres; la octava y última de ellas es una passacaglia, y solo después de ella llega entera la canción de Dowland *Come, Heavy Sleep*, con plena claridad tonal. La pieza es un viaje por las técnicas postonales que se resuelve de nuevo en la armonía de la práctica común — una reconciliación más que un rechazo.

**Construir un estudio atonal — método práctico:**

Este es un proceso para componer un breve estudio atonal para guitarra a partir de una célula de tricordio:

1. **Elige una célula de tricordio.** Ejemplo: la clase de conjuntos 3-3 (014) — un clúster cromático más una tercera. En alturas: Do, Do#, Mi.
2. **Llévala a las posiciones CAGED.** Busca transposiciones de [0,1,4] que caigan de forma natural bajo cada una de las cinco formas CAGED. En la posición V (traste 5): La, Sib, Do#. En la posición III: Sol, Lab, Si. Y así sucesivamente.
3. **Compón frases que recorran las posiciones.** Cada frase enuncia la célula en una posición y luego pasa a la siguiente. La identidad de la célula se conserva mientras cambia su ubicación en el diapasón.
4. **Varía el registro, la dinámica y la articulación.** Aplica la distribución de registros de la atonalidad libre: toca algunas células comprimidas y otras repartidas en dos octavas.
5. **Usa la inversión y la retrogradación.** Enuncia [0,1,4], luego su inversión [0,3,4], luego su retrógrada y luego la retrógrada de la inversión. Desarrollo motívico mediante operaciones seriales.

Este método produce música atonal, coherente y específicamente guitarrística — la geometría del diapasón da forma a la estructura musical.

**Aplicaciones a la improvisación:**

Los guitarristas de jazz (p. ej., Ben Monder, Kurt Rosenwinkel, Mary Halvorson) usan con frecuencia técnicas atonales en sus improvisaciones: células de tricordios, vectores interválicos como guías de sonoridad, voicings cuartales y cromáticos. Entender la teoría de conjuntos prepara al improvisador para moverse conscientemente entre los lenguajes tonal y postonal, tratándolos como un espectro unificado y no como sistemas opuestos.

---

## 7. El camino de vuelta

La teoría postonal no es un rechazo de la teoría tonal — es una generalización. Las herramientas desarrolladas para el análisis atonal iluminan la música tonal de nuevas maneras y tienden un puente entre tradiciones que, de otro modo, podrían parecer incompatibles.

**La teoría de conjuntos como herramienta de análisis de voicings de jazz:**

La armonía del jazz es notoriamente compleja: extensiones, alteraciones, poliacordes, tríadas de estructura superior. El análisis tonal tradicional tiene dificultades para describir un acorde como **G7alt(b9,#9,b13)**. En cambio, el análisis por clases de conjuntos lo reduce a un conjunto de clases de altura e identifica directamente su clase de conjuntos. El acorde anterior tiene las clases de altura {7, 11, 5, 8, 10, 3}; su forma prima es un hexacordio concreto cuyo vector interválico caracteriza su sonoridad.

Esto da a los teóricos del jazz un lenguaje que atraviesa las convenciones de los cifrados. Dos acordes con cifrados distintos pueden pertenecer a la misma clase de conjuntos y, por tanto, compartir el mismo contenido interválico. Dos acordes con cifrados parecidos pueden pertenecer a clases de conjuntos distintas. La teoría de conjuntos revela la sonoridad real que hay bajo la notación.

**Los vectores interválicos como medidas de sonoridad:**

El vector interválico cuantifica el «color» de un acorde. Un acorde con muchas ic3 e ic4 (terceras) suena terciario. Un acorde dominado por ic5 suena cuartal. Un acorde con muchas ic2 e ic6 suena denso y disonante. Leyendo el vector interválico de un acorde, puedes predecir su carácter sonoro sin siquiera oírlo.

Esto es útil de inmediato para los guitarristas: al elegir un voicing para un acorde ambiguo, puedes seleccionar el voicing cuyo vector interválico corresponda a la sonoridad que buscas — abierta y cuartal, densa y cromática, o algo intermedio.

**OPTIC/K y la equivalencia de clases de altura:**

En la teoría musical geométrica (Callender, Quinn y Tymoczko, *Science*, 2008), las equivalencias de conducción de voces se describen mediante las relaciones **OPTIC**:
- Equivalencia de **O**ctava: dos alturas separadas por una octava son la misma.
- **P**ermutación: reordenar dentro de una octava no cambia la identidad.
- **T**ransposición: dos acordes relacionados por un mismo intervalo son equivalentes.
- **I**nversión: los acordes especulares son equivalentes.
- **C**ardinalidad: las duplicaciones no cuentan.

Son exactamente los principios de la teoría de conjuntos de clases de altura, expresados de forma algo distinta. OPTIC deja explícito que la teoría de conjuntos no es exótica — es la formalización de cómo los músicos siempre han oído las equivalencias (un acorde de Do mayor es «el mismo» tanto si se dispone Do-Mi-Sol como Sol-Do-Mi o Do-Mi-Sol-Do).

La relación **K** añade una capa más (la equivalencia salvo pertenencia a una clase de conjuntos). Juntas, OPTIC y K proporcionan un marco matemático que unifica el análisis tonal de la conducción de voces con la teoría postonal de conjuntos. Las dos tradiciones no se oponen — son dos dialectos del mismo lenguaje subyacente.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Tonalidad de la práctica común** | El sistema armónico de la música académica occidental de aproximadamente 1600-1900, basado en la armonía funcional y los centros tonales |
| **Emancipación de la disonancia** | La afirmación de Schoenberg de 1908 de que las sonoridades disonantes no necesitan resolver en una consonancia |
| **Atonalidad** | Música organizada sin centro tonal ni tonalidad |
| **Atonalidad libre** | Música atonal organizada intuitivamente mediante células motívicas, distribución de registros y centralidad de altura |
| **Serialismo (dodecafónico)** | Organización sistemática de la música atonal basada en una serie ordenada de las 12 clases de altura |
| **Clase de altura** | Una clase de equivalencia de alturas relacionadas por la octava (p. ej., todos los Do pertenecen a la clase de altura 0) |
| **Notación entera** | Representación de las clases de altura mediante los enteros 0-11 |
| **Forma normal** | La ordenación más compacta de un conjunto de clases de altura |
| **Forma prima** | El representante canónico de una clase de conjuntos, incluida la equivalencia por inversión, transportado para empezar en 0 |
| **Clase interválica (ic)** | Una clase de equivalencia de intervalos (0-6) que agrupa los intervalos relacionados por inversión |
| **Vector interválico** | Una lista de 6 elementos que cuenta las apariciones de cada clase interválica en un conjunto |
| **Clase de conjuntos** | Un grupo de conjuntos de clases de altura relacionados por transposición e inversión, etiquetado con un número de Forte |
| **Número de Forte** | La etiqueta de catálogo de Allen Forte para una clase de conjuntos, con formato cardinalidad-ordinal (p. ej., 3-11) |
| **Relación Z** | La relación entre clases de conjuntos distintas que comparten el mismo vector interválico |
| **Original/Retrógrada/Inversión/Retrógrada de la inversión (P/R/I/RI)** | Las cuatro operaciones seriales aplicadas a una serie dodecafónica |
| **Combinatoriedad** | Propiedad de ciertas series cuyos hexacordios se combinan con formas transportadas para producir agregados |
| **Centralidad de altura** | Énfasis estructural de ciertas alturas en la música atonal sin función tonal |
| **Célula motívica** | Un pequeño conjunto de clases de altura usado como ADN estructural a lo largo de una composición atonal |

---

## Autoevaluación

**1. ¿Qué quería decir Schoenberg con «la emancipación de la disonancia» y por qué fue un punto de inflexión histórico?**
> Schoenberg sostuvo — en su música desde 1908 y, con ese nombre, en su ensayo «Opinion or Insight?» de 1926 — que las sonoridades disonantes no necesitan resolver en consonancias — que la distinción entre consonancia y disonancia es una convención histórica, no una ley acústica. Fue un punto de inflexión porque eliminó la última restricción de la tonalidad de la práctica común (la obligación de resolver la tensión) y abrió la puerta a una composición atonal en la que cualquier sonoridad podía funcionar como un evento estructural estable.

**2. Calcula la forma prima del conjunto {Re, Fa, La, Do} (un acorde de Re menor séptima). Muestra la forma normal y una comprobación de la inversión.**
> Clases de altura: {2, 5, 9, 0} → ascendente {0, 2, 5, 9}. Rotaciones y extensiones:
> - (0, 2, 5, 9): extensión = 9
> - (2, 5, 9, 0+12=12): extensión = 10
> - (5, 9, 12, 14): extensión = 9
> - (9, 12, 14, 17): extensión = 8 — ¡la menor!
> Forma normal: [9, 0, 2, 5]. Transporta para empezar en 0: resta 9 → [0, 3, 5, 8]. Inversión: invierte {0, 2, 5, 9} → {0, 10, 7, 3}, ascendente {0, 3, 7, 10}. Normalízala también (no te limites a reordenarla): la rotación (7, 10, 12, 15) tiene la menor extensión (8), así que su forma normal es [7, 10, 0, 3], transportada para empezar en 0 → [0, 3, 5, 8]. La inversión da el mismo resultado: esta clase de conjuntos es simétrica por inversión.
> **Forma prima: (0358)** — clase de conjuntos 4-26, la sonoridad de séptima menor / tríada menor más 7.

**3. Dada P0 = [0, 1, 4, 9, 5, 11, 2, 7, 6, 10, 3, 8], deriva I0 (inversión que empieza en 0). Muestra la fórmula utilizada.**
> Fórmula: I0[k] = (0 - P0[k]) mod 12 = (-P0[k]) mod 12.
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

**4. ¿Qué es una relación Z y por qué es importante en la teoría postonal?**
> Una relación Z es la propiedad que comparten dos clases de conjuntos distintas con vectores interválicos idénticos pero no relacionadas por transposición ni por inversión. Es importante porque revela que el contenido interválico (qué intervalos están presentes) no determina de forma única la identidad de la clase de conjuntos (qué configuraciones de alturas producen esos intervalos). Los conjuntos en relación Z suenan muy parecidos pero son estructuralmente distintos, una simetría profunda que explotaron compositores como Elliott Carter y Milton Babbitt.

**5. ¿Cómo tiende el análisis mediante teoría de conjuntos un puente entre la música postonal y la armonía del jazz?**
> La teoría de conjuntos abstrae los acordes en conjuntos de clases de altura y clases de conjuntos, atravesando las convenciones de los cifrados. Un complejo acorde de dominante alterado del jazz puede identificarse por su clase de conjuntos y caracterizarse por su vector interválico, lo que revela su sonoridad subyacente de una forma que los cifrados ocultan. Esto permite a los analistas de jazz comparar voicings de calidades de acorde aparentemente distintas, reconocer sonoridades compartidas y entender los lenguajes atonal y jazzístico como dialectos del mismo marco de clases de altura y no como sistemas opuestos.

**Criterios de aprobación:** calcular la forma prima de un acorde dado de 4 o 5 notas, derivar I0 y R0 a partir de una P0 dada y explicar la función estructural de una célula motívica en un contexto de atonalidad libre.

---

## Base de investigación

- Teoría de conjuntos de clases de altura formalizada por Allen Forte en *The Structure of Atonal Music* (1973); los números de Forte siguen siendo el sistema de catalogación estándar
- *Introduction to Post-Tonal Theory* de Joseph N. Straus (4.ª ed., 2016) es el texto pedagógico de referencia y la fuente de los algoritmos de forma normal y forma prima
- *Serial Composition and Atonality* de George Perle (6.ª ed., 1991) aporta una base histórica y analítica a la técnica dodecafónica
- La teoría neorriemanniana y las relaciones OPTIC extienden la teoría de conjuntos hacia el análisis de la conducción de voces (Cohn, 2012; Tymoczko, *A Geometry of Music*, 2011)
- Referencias del repertorio de guitarra: Henze *Royal Winter Music I & II*; Britten *Nocturnal Op. 70*; Takemitsu *All in Twilight*; Ginastera *Sonata Op. 47*
- Los propios escritos de Schoenberg (*Style and Idea*, 1950) documentan la emancipación de la disonancia en sus propias palabras
- Fuentes: Forte 1973, Straus 2016, Perle 1991, Tymoczko 2011, Cohn 2012, Schoenberg 1950
- Estado de creencia: T(0.85) F(0.03) U(0.08) C(0.04)
