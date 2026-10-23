---
module_id: mus-011-modes-modal-families
department: music
course: Modos y familias modales
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-010-scales-pattern-set-interval-vector, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Modos y familias modales — La rotación frente al vector interválico compartido

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Construir los modos de una escala rotando su fórmula de intervalos, y nombrar los siete modos de la escala mayor
- Distinguir los modos relativos, que conservan las notas y cambian de tónica, de los modos paralelos, que conservan la tónica y cambian las notas, y tocar unos y otros en la guitarra
- Contar los modos distintos de una escala, incluidas las escalas de transposición limitada
- Explicar por qué dos escalas con el mismo vector de clases de intervalo no son necesariamente modos una de otra: imágenes especulares y relación Z
- Seguir cómo construye GA sus familias modales, y leer lo que el laboratorio de Learn ya ha medido

---

## 1. Los modos como rotaciones

MUS-010 describió una escala por su fórmula de intervalos. Leer la misma fórmula desde otro paso da un **modo**. El artículo «Mode (music)» de Wikipedia lo dice así: «Modern Western modes use the same set of notes as the major scale, in the same order, but starting from one of its seven degrees in turn as a tonic, and so present a different sequence of whole and half steps.» (Los modos occidentales modernos usan las mismas notas que la escala mayor, en el mismo orden, pero tomando por turno cada uno de sus siete grados como tónica, y presentan así una sucesión distinta de tonos y semitonos.)

| Modo | Fórmula de intervalos | Sobre su grado de do mayor |
|------|------|------|
| Jónico | 2 2 1 2 2 2 1 | do re mi fa sol la si |
| Dórico | 2 1 2 2 2 1 2 | re mi fa sol la si do |
| Frigio | 1 2 2 2 1 2 2 | mi fa sol la si do re |
| Lidio | 2 2 2 1 2 2 1 | fa sol la si do re mi |
| Mixolidio | 2 2 1 2 2 1 2 | sol la si do re mi fa |
| Eólico | 2 1 2 2 1 2 2 | la si do re mi fa sol |
| Locrio | 1 2 2 1 2 2 2 | si do re mi fa sol la |

Cada fórmula es la de la fila de arriba con su primer paso movido al final: una **rotación**. Un modo queda fijado por su fórmula, no por sus notas: «transposition preserves mode» (la transposición conserva el modo), así que re dórico, do dórico y fa♯ dórico son todos dóricos. El jónico es la escala mayor, y el eólico la menor natural.

Toda escala tiene modos en el mismo sentido. «Other heptatonic scales also have seven modes each» (las demás escalas heptatónicas también tienen siete modos cada una), y Wikipedia da el ejemplo de la armonía de la menor melódica, «based on the seven rotations of the ascending melodic minor scale» (basada en las siete rotaciones de la escala menor melódica ascendente).

### Ejercicio práctico

Escribe la fórmula del cuarto modo de la pentatónica mayor, 2 2 3 2 3, y da sus notas sobre do.

> *Solución:* El cuarto modo empieza por el cuarto paso de la fórmula: 2 3 2 2 3. Sobre do, los pasos 2, 3, 2 y 2 llevan a re, fa, sol y la, y el último paso, 3, vuelve a do: do re fa sol la. Es la pentatónica mayor do re mi sol la leída desde sol, su cuarta nota, y llevada a do.

---

## 2. Modos relativos y modos paralelos

Dos modos pueden compararse de dos maneras.

**Los modos relativos conservan las notas.** Re dórico y sol mixolidio se tocan ambos en las teclas blancas: re dórico es do mayor leído desde re, sol mixolidio es do mayor leído desde sol. El artículo «Relative key» de Wikipedia dice lo mismo de una tonalidad mayor y su relativa menor: «share all of the same notes but are arranged in a different order of whole steps and half steps» (comparten todas las mismas notas, pero ordenadas en una sucesión distinta de tonos y semitonos).

**Los modos paralelos conservan la tónica.** Do dórico y do mixolidio empiezan ambos en do, pero sus notas difieren. El artículo «Parallel key» de Wikipedia llama tonalidades paralelas (en español, homónimas) a una escala mayor y una menor con «the same starting note (tonic)» (la misma nota de partida, la tónica). Los siete modos paralelos sobre do toman las notas de siete escalas mayores distintas:

| Modo sobre do | Notas | Notas de | Bajados respecto al lidio |
|------|------|------|------|
| do lidio | do re mi fa♯ sol la si | sol mayor | ninguno |
| do jónico | do re mi fa sol la si | do mayor | 4 |
| do mixolidio | do re mi fa sol la si♭ | fa mayor | 4, 7 |
| do dórico | do re mi♭ fa sol la si♭ | si♭ mayor | 4, 7, 3 |
| do eólico | do re mi♭ fa sol la♭ si♭ | mi♭ mayor | 4, 7, 3, 6 |
| do frigio | do re♭ mi♭ fa sol la♭ si♭ | la♭ mayor | 4, 7, 3, 6, 2 |
| do locrio | do re♭ mi♭ fa sol♭ la♭ si♭ | re♭ mayor | 4, 7, 3, 6, 2, 5 |

Leídas en este orden, las tonalidades de origen bajan por el círculo de quintas, de un sostenido a cinco bemoles. El artículo «Mode (music)» de Wikipedia describe la misma sucesión: «each mode has one more lowered interval relative to the tonic than the mode preceding it» (cada modo tiene un intervalo bajado más, respecto a la tónica, que el modo que lo precede).

**En la guitarra.** En primera posición, con la afinación estándar, las notas de do mayor están en los trastes 0 a 3. Re dórico parte de la cuerda de re al aire y sube hasta el re de la segunda cuerda, traste 3: re mi fa sol la si do re. Sol mixolidio parte de la sexta cuerda, traste 3, y sube hasta la cuerda de sol al aire: sol la si do re mi fa sol. Los dos salen de la misma forma de do mayor en primera posición, en los trastes 0 a 3: son modos relativos, el mismo conjunto leído desde dos tónicas. Lo que los hace sonar distinto es la nota en la que se empieza y se termina, y los acordes que se tocan debajo.

### Ejercicio práctico

¿Qué escala mayor contiene las notas de mi frigio, y cuál contiene las notas de do frigio?

> *Solución:* Mi frigio es do mayor leído desde mi, su tercer grado. Do frigio empieza en do con la misma fórmula, 1 2 2 2 1 2 2: do re♭ mi♭ fa sol la♭ si♭, las notas de la♭ mayor, cuyo tercer grado es do.

---

## 3. ¿Cuántos modos?

Una escala de n notas tiene n rotaciones, pero dos rotaciones pueden dar la misma fórmula. Wikipedia: «The number of possible modes for any intervallic set is dictated by the pattern of intervals in the scale.» (El número de modos posibles de un conjunto de intervalos lo dicta la fórmula de intervalos de la escala.) La escala disminuida «has only two distinct modes» (solo tiene dos modos distintos), y el artículo sigue: «The chromatic and whole-tone scales, each containing only steps of uniform size, have only a single mode each, as any rotation of the sequence results in the same sequence.» (Las escalas cromática y de tonos enteros, que solo contienen pasos de un único tamaño, tienen un solo modo cada una, ya que toda rotación de la sucesión da la misma sucesión.)

Las escalas de tonos enteros y disminuida son dos de los **modos de transposición limitada** de Messiaen: escalas que «may be transposed to all twelve notes of the chromatic scale, but at least two of these transpositions must result in the same pitch classes» (pueden transportarse a las doce notas de la escala cromática, pero al menos dos de esas transposiciones deben dar las mismas clases de altura; Wikipedia, «Modes of limited transposition»). La escala de tonos enteros «has two transpositions and one mode» (tiene dos transposiciones y un modo); la escala octatónica, o escala disminuida, «has three transpositions, like the diminished 7th chord, and two modes» (tiene tres transposiciones, como el acorde de séptima disminuida, y dos modos). La escala aumentada de la tabla de abajo cumple la misma definición, pero Messiaen no la incluyó: el mismo artículo la ve como una forma truncada del tercer modo de Messiaen.

Los dos números están ligados. Un modo sobre do es una transposición de la escala, elegida para que contenga do, leída desde do. Una escala de n notas con t transposiciones distintas coloca n × t notas sobre las 12 clases de altura, el mismo número sobre cada una, así que n × t / 12 de sus transposiciones contienen do:

| Escala | Notas n | Transposiciones t | Modos n × t / 12 |
|------|------|------|------|
| Mayor | 7 | 12 | 7 |
| Menor armónica | 7 | 12 | 7 |
| Pentatónica mayor | 5 | 12 | 5 |
| Tonos enteros | 6 | 2 | 1 |
| Aumentada, do mi♭ mi sol sol♯ si | 6 | 4 | 2 |
| Octatónica | 8 | 3 | 2 |
| Cromática | 12 | 1 | 1 |

MUS-006 cuenta las mismas rotaciones, y la lección 12 del curso music-theory-ga de Learn estudia estas escalas en GA.

### Ejercicio práctico

La fórmula de la escala aumentada es 3 1 3 1 3 1. ¿Cuántos modos distintos tiene, y cuáles son sus fórmulas?

> *Solución:* Dos: 3 1 3 1 3 1 y 1 3 1 3 1 3. Toda rotación de dos pasos devuelve la misma fórmula. Tiene cuatro transposiciones, y 6 × 4 / 12 = 2.

---

## 4. Mismo vector, familia distinta

Las rotaciones conservan el conjunto de una escala, salvo transposición, así que los modos de una escala comparten todos su vector de clases de intervalo (MUS-010, MUS-020). La recíproca es falsa: dos escalas pueden compartir un vector sin ser modos una de otra.

**Las imágenes especulares.** Do menor armónica, do re mi♭ fa sol la♭ si, tiene la fórmula 2 1 2 2 1 3 1. Do mayor armónica, do re mi fa sol la♭ si, tiene 2 2 1 2 1 3 1. El artículo «Harmonic major scale» de Wikipedia la describe como una escala mayor con la sexta bajada, y añade: «Its upper tetrachord is the same as that of the harmonic minor scale.» (Su tetracordio superior es el mismo que el de la escala menor armónica.) Las dos tienen el vector <3 3 5 4 4 2>. Las siete rotaciones de la fórmula de la menor armónica son:

2 1 2 2 1 3 1, 1 2 2 1 3 1 2, 2 2 1 3 1 2 1, 2 1 3 1 2 1 2, 1 3 1 2 1 2 2, 3 1 2 1 2 2 1, 1 2 1 2 2 1 3

Ninguna es 2 2 1 2 1 3 1, así que la mayor armónica no es un modo de la menor armónica. Es su **imagen especular**: toca los pasos de la menor armónica bajando desde sol, 2 1 2 2 1 3 1, y obtienes sol fa mi re do si la♭, las notas de do mayor armónica; sol es la nota de partida que cae en do y no en una transposición. Una imagen especular tiene los mismos intervalos en orden inverso, y por tanto el mismo vector (MUS-020 la llama una inversión). La escala mayor, la menor melódica, la pentatónica y las escalas de tonos enteros, aumentada, octatónica y cromática del §3 son sus propias imágenes especulares; la menor armónica, la mayor armónica y la escala de blues no lo son.

**La relación Z.** Algunos conjuntos comparten un vector sin ser una transposición ni una imagen especular uno del otro. El artículo «Interval vector» de Wikipedia da un ejemplo, el más pequeño posible: «the two sets 4-z15A {0,1,4,6} and 4-z29A {0,1,3,7} have the same interval vector ⟨111111⟩ but one can not transpose and/or invert the one set onto the other.» (Los dos conjuntos 4-z15A {0,1,4,6} y 4-z29A {0,1,3,7} tienen el mismo vector interválico ⟨111111⟩, pero no se puede transportar ni invertir uno sobre el otro.) Sobre do, son do do♯ mi fa♯ y do do♯ mi♭ sol.

**Contar los conjuntos de un vector.** Toma todos los conjuntos que contienen do y tienen un vector dado. Incluyen los modos sobre do de todas las escalas con ese vector:
- el vector de la escala mayor: los siete modos sobre do del §2, ya que la escala mayor es su propia imagen especular y no tiene pareja Z;
- el vector de la menor armónica: 14 conjuntos, los siete modos sobre do de la menor armónica y los siete de la mayor armónica;
- el vector de la escala de blues: 24 conjuntos, seis modos de la escala de blues, seis de su imagen especular, y doce conjuntos de una clase en relación Z con ella.

El recuento del §3 se extiende a una clase entera. Si una clase de n notas tiene f conjuntos distintos entre sus transposiciones y sus imágenes especulares, n × f / 12 de ellos contienen do. Para la clase de la menor armónica, f = 24 y 7 × 24 / 12 = 14.

### Ejercicio práctico

¿Son do menor armónica y do mayor armónica modos una de otra?

> *Solución:* No. La fórmula de la mayor armónica, 2 2 1 2 1 3 1, no está entre las siete rotaciones de la fórmula de la menor armónica. Las dos escalas son imágenes especulares una de otra: comparten el vector <3 3 5 4 4 2>, pero ninguna rotación lleva de una a otra.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos de abajo se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Esta lección documenta ese código y no lo modifica. No ha ejecutado GA ni sus pruebas: los recuentos de abajo vienen de una reimplementación en Python de los métodos citados. Los archivos que cita no han cambiado en la rama `main` de GA, en `0843879`.

El curso music-theory-ga de Learn compila una versión anterior de GA, `a826864`, y sus lecciones ya han medido las familias modales de GA. `ModalFamily.cs` es el mismo archivo en los dos commits, y también las líneas de los miembros de `PitchClassSet` usados abajo. El código al que llaman sí cambió entretanto: se añadieron cachés y tablas de consulta, el vector de doce notas <12 12 12 12 12 6> recibió una decodificación especial, y cambió código de lectura de texto, de formas normales y de tonalidades que la construcción de las familias no usa. La reimplementación también encuentra todos los recuentos que midió Learn. Así que esas mediciones siguen describiendo el código de GA. Esta sección las resume, enlaza con ellas y añade un censo de todas las familias.

**Los modos tonales de GA son rotaciones.** [`MajorScaleMode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/Diatonic/MajorScaleMode.cs#L16) pasa `Scale.Major` a su clase base, que la guarda como [`ParentScale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L27-L34) y construye las notas de cada modo [rotando las notas de la escala madre](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L127-L135). Son los modos relativos del §2: una prueba comprueba que [los siete modos empiezan en do, re, mi, fa, sol, la y si](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleModeTests.cs#L21-L40). Otra prueba, [`AllModes_ShareParentScaleIntervalClassVector`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleModeTests.cs#L62-L71), afirma que «every rotation of the diatonic scale has the same interval-class vector» (toda rotación de la escala diatónica tiene el mismo vector de clases de intervalo), pero lee `mode.ParentScale.IntervalClassVector`, que es el vector de `Scale.Major` para los siete modos, y lo compara con la constante `IntervalClassVector.Major`: la misma comprobación, siete veces. Leer las notas propias de los modos solo haría trivial la comprobación, ya que los modos relativos comparten un solo conjunto. La afirmación tiene contenido para los modos llevados a do, como en la tabla del §2: siete conjuntos distintos con un solo vector; esta prueba no los construye.

**Las familias modales de GA agrupan los conjuntos por vector.** Una [`ModalFamily`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L9-L13) es un [«Group of pitch class sets representing a scale that share the same interval vector»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L10) (grupo de conjuntos de clases de altura que representan una escala y comparten el mismo vector interválico). GA [construye las familias](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L114-L129) a partir de todos los conjuntos que contienen 0, agrupados por número de notas y luego por vector: el recuento del §4. Sus miembros son, por tanto, modos paralelos sobre do, y la familia mayor está formada por los siete conjuntos de la tabla del §2. GA ordena sus conjuntos [por identificador creciente](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L19-L20), siendo el identificador de un conjunto su número de 12 bits (MUS-020), y el [agrupamiento](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L119-L120) conserva ese orden. Así, el primer miembro y el [`PrimeMode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L51) de la familia mayor son do locrio, identificador 1387. [`ModeIndex`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L106-L117) es el lugar de un conjunto en esa lista, y `FamilySize` la longitud de la lista; `ModeIndex` vale 5 para do jónico y 6 para do lidio, no es un grado. La lección 13 de Learn muestra que vale −1 para un conjunto sin do ([lección 13](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/13-extended-and-altered-chords.mdx#L355)).

**Lo que Learn ha medido.** Con GA compilado en `a826864`:
- la familia de la menor armónica tiene 14 miembros en GA, y la familia de blues 24 ([lección 2](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/02-scales-and-modes.mdx#L236-L256)), los recuentos del §4;
- la familia de la tríada mayor tiene 6 miembros, la de la séptima de dominante 8 y la del tetracordio de todos los intervalos 16 ([lección 4](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/04-set-classes.mdx#L184-L196));
- `UnifiedModeService.RankByBrightness` ordena 14 escalas para la familia de la menor armónica ([lección 11](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/11-modes-in-depth.mdx#L211-L229));
- `IsMonomodal`, cuyo comentario de documentación pone como ejemplos «Whole Tone, Diminished» (tonos enteros, disminuida), es falso para la escala octatónica, la escala disminuida, ya que su familia tiene dos miembros, y verdadero para el acorde de séptima disminuida ([lección 12](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/12-symmetry-and-limited-transposition.mdx#L254)).

El catálogo de GA generado a partir de estas familias, `AtonalModalFamilies.yaml`, archiva el vector <3 3 5 4 4 2> con el nombre [«Harmonic Major Family»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L6446-L6452) (familia mayor armónica), con un `DistinctModeCount` de 14, es decir, según el §4, los modos sobre do de dos escalas, y dos subfamilias tonales, la mayor armónica y la menor armónica. La lección 12 de Learn lee el campo `IsSymmetric` del archivo ([lección 12](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/12-symmetry-and-limited-transposition.mdx#L260)).

**Todas las familias, por transcripción.** Sobre las 200 familias de GA, la transcripción encuentra:

| Tipo de familia | Familias | Conjuntos |
|------|------|------|
| Solo rotaciones del primer miembro | 75 | 398 |
| También imágenes especulares, sin pareja Z | 102 | 1218 |
| Una clase en relación Z | 23 | 432 |

Así, 125 de las 200 familias, que contienen 1650 de los 2048 conjuntos que contienen do, no son familias de modos. El comentario de documentación de [`IsMultimodal`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L181-L184) habla de «a family with multiple distinct rotations (e.g. Diatonic, Harmonic Minor)» (una familia con varias rotaciones distintas, por ejemplo diatónica, menor armónica), pero siete de los catorce miembros de la familia de la menor armónica no son sus rotaciones. [`IsZRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L196-L211) busca un miembro que no esté entre las 24 transposiciones e inversiones del primer miembro, así que señala las 23 familias Z y acepta las 102 familias con imágenes especulares.

**Lo que comprueban las pruebas.** Unas pruebas compiladas comprueban que el conjunto propio de una escala está en su familia ([`ScaleModalMetadataTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ScaleModalMetadataTests.cs#L8-L32)), que `IsZRelated` coincide con las marcas Z del catálogo de Forte hasta seis notas ([`CanonicalForteCatalogTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L81-L90)), y que la familia mayor tiene siete miembros, mediante `UnifiedModeService.EnumerateRotations` ([`UnifiedModeEdgeCaseTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Unified/UnifiedModeEdgeCaseTests.cs#L227-L240)). Ninguna enumera los conjuntos que una familia debería contener. La prueba que lo hacía está retirada de su proyecto, junto con otras dos ([`ModalFamilyScaleModeFactoryTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L50), [`ModalFamilyTests` y `ModalFamilyScaleModeTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L69-L70)). Esa prueba, `ModalFamilyTests`, [espera siete miembros](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L90-L92), y luego [busca](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L103-L109) los siete modos relativos que enumera, [de C D E F G A B a B C D E F G A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L59-L69), con nombres de notas en inglés. Como conjuntos, son uno solo, el de do mayor, así que la prueba nunca busca do dórico ni los demás miembros de la tabla del §2.

Corregir cualquiera de estas cosas corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

El `FamilySize` de GA para do menor armónica vale 14. ¿Cuántos de esos 14 conjuntos son modos de la escala menor armónica, y qué son los demás?

> *Solución:* Siete: las transposiciones de la menor armónica que contienen do, leídas desde do. Los otros siete son los modos sobre do de la mayor armónica, su imagen especular, que comparte el vector <3 3 5 4 4 2>.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA en `a826864`. La versión de GA fijada en el laboratorio no tiene que cambiar: como explica el §5, el código que construye las familias es el mismo en `5c3a52a`, salvo cachés y un caso especial de decodificación. Nada en esta sección es una medición:
- las predicciones vienen de los §3 a §5 y se escriben antes de cualquier ejecución;
- los recuentos y los identificadores, incluidos los recuentos por número de notas del paso 1, vienen de la reimplementación en Python del §5;
- una versión posterior de esta lección informará de los resultados.

Cada paso llama a los tipos de GA dentro del propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **El censo.** Contar las `ModalFamily.Items` y sus miembros por número de notas. Predicción: 200 familias que contienen 2048 conjuntos; por número de notas de 1 a 12, 1, 6, 12, 28, 35, 35, 35, 28, 12, 6, 1 y 1 familias.
2. **Rotaciones o no.** Para cada familia, probar cada miembro contra las doce transposiciones del primer miembro, y luego contra sus imágenes especulares. Predicción: 75 familias solo de rotaciones, 102 con imágenes especulares y sin pareja Z, 23 con una clase en relación Z; 1650 de los 2048 conjuntos están en las 125 familias mixtas.
3. **`IsZRelated`.** Leerlo para cada conjunto que contiene do. Predicción: verdadero para los 432 conjuntos de las 23 familias Z, falso para los otros 1616.
4. **Los controles.** Mostrar la familia mayor y la familia de la menor armónica. Predicción: la familia mayor contiene los identificadores 1387, 1451, 1453, 1709, 1717, 2741 y 2773, con `PrimeMode` 1387, do locrio; la familia de la menor armónica contiene 14 conjuntos, siete transposiciones de do menor armónica y siete de do mayor armónica.

### Ejercicio práctico

El paso 1 predice 35 familias de siete notas y 35 de cinco. ¿Por qué son iguales los dos números?

> *Solución:* Una familia de n notas es un vector compartido por conjuntos de n notas. El paso al complemento empareja uno a uno los conjuntos de 7 notas con los de 5, y dos conjuntos de 7 notas comparten un vector exactamente cuando sus complementos comparten uno (el teorema del complemento de MUS-020). Las dos cardinalidades tienen, por tanto, el mismo número de vectores, y el mismo número de familias.

---

## 7. Errores comunes

- **Confundir modos relativos y modos paralelos.** Re dórico tiene las notas de do mayor; do dórico tiene las notas de si♭ mayor.
- **Contar los modos de una escala simétrica por sus notas.** La escala octatónica tiene ocho notas y dos modos.
- **Tomar un vector compartido por una familia compartida.** La mayor armónica tiene el vector de la menor armónica y no es uno de sus modos.
- **Tomar una imagen especular por una rotación.** Una imagen especular invierte la fórmula; una rotación solo mueve su comienzo.
- **Leer la `ModalFamily` de GA como los modos de una sola escala.** Contiene todos los conjuntos que contienen do con ese vector, imágenes especulares y parejas Z incluidas.
- **Leer el `ModeIndex` de GA como un grado.** Es un lugar en una lista ordenada por identificador: do locrio vale 0, do jónico 5.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Modo** | La fórmula de intervalos de una escala leída desde otro de sus pasos: una rotación |
| **Modos relativos** | Modos que comparten las mismas notas y difieren en la tónica, como re dórico y sol mixolidio |
| **Modos paralelos** | Modos que comparten la misma tónica y difieren en las notas, como do dórico y do mixolidio |
| **Modo de transposición limitada** | Una escala con menos de doce transposiciones distintas, y por tanto con menos modos que notas |
| **Imagen especular** | Una escala con los mismos pasos en orden inverso; comparte el vector, y solo es un modo si la escala es su propia imagen especular |
| **Relación Z** | Dos conjuntos con el mismo vector que no son ni transposiciones ni imágenes especulares uno del otro |
| **Familia modal** | Los modos de una escala: sus rotaciones |
| **La `ModalFamily` de GA** | Todos los conjuntos que contienen do con un vector dado: los modos de varias escalas cuando imágenes especulares o parejas Z lo comparten |

---

## Autoevaluación

**1. Escribe la fórmula del modo lidio y da las notas de fa lidio y de do lidio.**
> 2 2 2 1 2 2 1. Fa lidio se escribe fa sol la si do re mi, las notas de do mayor. Do lidio se escribe do re mi fa♯ sol la si, las notas de sol mayor.

**2. Toca re dórico y sol mixolidio en primera posición. ¿Por qué caben los dos en la misma forma?**
> Los dos son do mayor leído desde otra tónica: son modos relativos, con el mismo conjunto. Solo cambian la nota de partida y los acordes que se tocan debajo.

**3. ¿Cuántos modos distintos tienen la escala de tonos enteros y la escala octatónica, y por qué?**
> Uno y dos. La fórmula de tonos enteros repite un solo paso, así que cada rotación la devuelve; la fórmula octatónica alterna dos pasos, así que tiene dos rotaciones distintas. Con n notas y t transposiciones, n × t / 12 da 6 × 2 / 12 = 1 y 8 × 3 / 12 = 2.

**4. En GA en `5c3a52a`, ¿por qué la familia modal de do menor armónica tiene 14 miembros, y qué tipo de familia del §5 es?**
> GA agrupa por vector todos los conjuntos que contienen do, y la mayor armónica, imagen especular de la menor armónica, tiene el mismo vector. La familia contiene los siete modos sobre do de cada una de las dos escalas: es una de las 102 familias con imágenes especulares y sin pareja Z.

**Criterio de aprobación:** Construir y nombrar los modos de una escala a partir de su fórmula. Distinguir modos relativos y paralelos, y tocar unos y otros. Contar los modos de una escala, escalas simétricas incluidas. Explicar por qué un vector compartido no hace de dos escalas modos una de otra. Decir qué contiene la `ModalFamily` de GA, y en qué se diferencia de una familia de modos.

---

## Base de investigación

- Wikipedia, «Mode (music)»: los modos diatónicos modernos, la transposición y el modo, la sucesión a lo largo del círculo de quintas, los siete modos de las demás escalas de siete notas, y el número de modos distintos.
- Wikipedia, «Modes of limited transposition»: la definición de Messiaen, las transposiciones y los modos de las escalas de tonos enteros y octatónica, y la escala aumentada como truncamiento del tercer modo de Messiaen.
- Wikipedia, «Relative key» y «Parallel key»: las dos relaciones, para tonalidades mayores y menores.
- Wikipedia, «Harmonic major scale»: la sexta bajada, y el tetracordio superior compartido con la menor armónica.
- Wikipedia, «Interval vector»: la relación Z y los conjuntos 4-z15A y 4-z29A.
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §5 enlaza con su línea.
- Learn, lecciones 2, 4, 11, 12 y 13 de music-theory-ga en el commit `9e03205191de8602d1833e171aecff832ea9cb14`: sus mediciones de las familias modales de GA en `a826864`.
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia.
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión.
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
