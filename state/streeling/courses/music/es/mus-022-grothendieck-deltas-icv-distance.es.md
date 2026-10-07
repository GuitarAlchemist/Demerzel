---
module_id: mus-022-grothendieck-deltas-icv-distance
department: music
course: Los deltas de Grothendieck — lo que mide la distancia de contenido interválico
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites: [mus-020-set-classes-interval-vectors-prime-forms, mat-022-symmetry-groups-invariants]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Los deltas de Grothendieck — Lo que mide la distancia de contenido interválico, y lo que no puede ver

> **Departamento de Música** | Etapa: Citrinitas (Intermedio a avanzado) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Tratar los vectores de clases de intervalo como elementos de un monoide conmutativo, y construir el grupo en el que se pueden restar
- Calcular el delta y la distancia L1 entre dos conjuntos, y acotar la distancia a partir de los tamaños de los conjuntos y nada más
- Demostrar qué conjuntos están a distancia 0, y por qué dos conjuntos del mismo tamaño están a una distancia par
- Decir lo que la distancia no puede ver: la conducción de voces, el mayor y el menor, las tonalidades, las notas que contiene un acorde y la relación Z
- Seguir lo que GA calcula para cada uno de estos puntos, y dónde una heurística, un comentario o una prueba dicen otra cosa

---

## 1. El contenido interválico como recuento

Un guitarrista pide «un acorde cercano a este». Una respuesta posible compara el contenido interválico. El vector de clases de intervalo del §2 de MUS-020 cuenta, para cada clase de intervalo de 1 a 6, los pares de notas del conjunto separados por esa distancia. Do mayor tiene <001110>: una tercera menor, una tercera mayor y una quinta.

Un vector es una lista de seis números naturales, un elemento de N^6, y dos listas así se suman componente a componente. Con <000000> como elemento neutro, N^6 es un **monoide conmutativo**: su suma es asociativa y conmutativa y tiene elemento neutro. Ningún elemento salvo <000000> tiene opuesto: ninguna lista de números naturales sumada a <001110> da <000000>.

La suma de dos vectores cuenta pares; no combina acordes. Añade la nota si a do mi sol. El nuevo conjunto, Cmaj7, conserva los tres pares de do mayor y gana los tres pares que forma si con do, mi y sol, a 11, 7 y 4 semitonos: las clases de intervalo 1, 5 y 4. Así, ICV(Cmaj7) = <001110> + <100110> = <101220>. En general, cuando dos conjuntos A y B no comparten ninguna nota, ICV(A ∪ B) = ICV(A) + ICV(B) + X(A, B), donde X(A, B) cuenta los pares formados por una nota de cada conjunto, clase por clase: la función de intervalos de Lewin (1987), plegada sobre las clases de intervalo. La nota si, por sí sola, tiene el vector <000000>; todo lo que añade viene de X.

No toda lista es el vector de un conjunto. Los seis recuentos de un conjunto de n notas suman n(n − 1)/2, su número de pares. Los 4,096 conjuntos tienen 200 vectores distintos: <000000> para el conjunto vacío y las notas solas, y luego 6, 12, 28, 35, 35, 35, 28, 12, 6, 1 y 1 vectores para los tamaños 2 a 12. Son las 224 clases de conjuntos del §4 de MUS-020, menos 23 porque cada par en relación Z comparte un vector, menos 1 porque el conjunto vacío y una nota sola comparten <000000>.

### Ejercicio práctico

Halla el vector de C7, do mi sol si♭, a partir del de do mayor.

> *Solución:* Si♭ está 10, 6 y 3 semitonos por encima de do, mi y sol: las clases de intervalo 2, 6 y 3. Así, X = <011001>, y <001110> + <011001> = <012111>, el vector que el §2 de MUS-020 da para C7.

---

## 2. Restar recuentos: el grupo de Grothendieck

Para comparar dos conjuntos queremos una diferencia: cuántos pares de cada clase tiene el segundo conjunto más que el primero. N^6 no tiene elementos negativos, así que lo ampliamos hasta el grupo más pequeño en el que se pueden restar dos cualesquiera de sus elementos.

La **construcción de Grothendieck** hace esto para cualquier monoide conmutativo M. Toma pares (a, b) de elementos de M, que se leen como «a − b». Llama equivalentes a (a, b) y (c, d) cuando a + d + k = b + c + k para algún k de M. Las clases forman un grupo abeliano K(M): (a, b) + (c, d) = (a + c, b + d), el elemento neutro es la clase de (0, 0), y el opuesto de (a, b) es la clase de (b, a). La aplicación a ↦ (a, 0) lleva M a K(M), y todo homomorfismo de M en un grupo se extiende a K(M) de una única manera: ese es el sentido de «más pequeño». Cuando M es **cancelativo**, es decir, cuando a + k = b + k implica a = b, el k se puede omitir y la aplicación es inyectiva. N^6 es cancelativo, y K(N^6) es Z^6: la clase de (a, b) es la lista de enteros a − b.

El **delta de Grothendieck** de un conjunto A a un conjunto B es δ(A, B) = ICV(B) − ICV(A), un elemento de Z^6. De do mayor a Cmaj7 vale <+1, 0, 0, +1, +1, 0>: un semitono más, una tercera mayor más y una quinta más. Tres leyes lo convierten en una diferencia, y se cumplen porque la resta en un grupo las cumple:
- δ(A, A) = 0;
- δ(B, A) = −δ(A, B);
- δ(A, B) + δ(B, C) = δ(A, C).

El delta depende solo de los dos vectores, no de las notas. Ir de do mayor a Fmaj7, fa la do mi, conserva do y mi, quita sol y añade fa y la, y sin embargo da el mismo delta que ir a Cmaj7, porque Fmaj7 y Cmaj7 comparten el vector <101220>.

La **norma L1** de un delta suma los valores absolutos de sus seis componentes, y la **distancia** d(A, B) es la norma L1 de δ(A, B). Sobre los vectores, es una métrica. Sobre los conjuntos, es solo una pseudométrica: d(A, B) = 0 no obliga a que A = B (§3).

### Ejercicio práctico

Da los vectores de una tríada mayor y de una tríada menor, y su distancia.

> *Solución:* Ambos son <001110>. Una tríada menor es una inversión de una tríada mayor, y una inversión conserva cada clase de intervalo (§2 de MUS-020). El delta es 0, y la distancia también. GA da 1 (§5).

---

## 3. Lo que mide la distancia

Sea T(n) = n(n − 1)/2 el número de pares de un conjunto de n notas. Los seis componentes de δ(A, B) suman T(|B|) − T(|A|).

**Teorema 1 (cota de tamaño y paridad).** d(A, B) ≥ |T(|B|) − T(|A|)|, y d(A, B) − (T(|B|) − T(|A|)) es par.

*Demostración.* La suma de los valores absolutos de los componentes es al menos el valor absoluto de su suma. Y para todo entero x, |x| − x vale 0 o 2|x|, un número par, así que la norma y la suma difieren en un número par. ∎

De ahí se siguen tres consecuencias:
- Dos conjuntos del mismo tamaño están a una distancia par, así que dos conjuntos del mismo tamaño con vectores distintos están al menos a 2.
- Un conjunto de tres notas y uno de cuatro notas están al menos a T(4) − T(3) = 3.
- Una distancia de exactamente 1 requiere T(|B|) − T(|A|) = ±1, lo que solo ocurre entre un conjunto de dos notas y uno de como mucho una nota. Desde un conjunto de tres notas o más, todo conjunto está a distancia 0 o al menos a 2.

**Teorema 2 (una nota añadida).** Si A tiene n notas y x no es una de ellas, añadir x añade los n pares entre x y las notas de A y no cambia ningún otro par. Así, δ(A, A ∪ {x}) tiene componentes no negativos que suman n, y d(A, A ∪ {x}) = n, sea cual sea la nota añadida.

Así, Cmaj7, C7, C6 y Cadd9 están todos a distancia 3 de do mayor, la menor distancia que un conjunto de cuatro notas puede tener respecto de uno de tres. De las 29 clases de tetracordios, 13 están a distancia 3 de do mayor. Cuatro de ellas no contienen ninguna tríada mayor ni menor: (0125), (0135), (0145) y (0146).

**Teorema 3 (distancia cero).** d(A, B) = 0 exactamente cuando A y B tienen el mismo vector. Como T(0) = T(1) = 0 y T crece a partir de n = 1, dos conjuntos de tamaños distintos solo comparten un vector cuando uno es vacío y el otro es una nota sola. Dos conjuntos del mismo tamaño comparten un vector exactamente cuando están en la misma clase de conjuntos o en dos clases en relación Z (§5 de MUS-020). Así, cada transposición y cada inversión de un conjunto está a distancia 0 de él, y lo mismo vale para cada conjunto de su clase compañera en relación Z.

La distancia cuenta cuántos pares de cada clase de intervalo aparecen o desaparecen, y nada más. El teorema 2 dice lo que cuesta una nota añadida; el teorema 3 dice lo que no cuesta nada.

### Ejercicio práctico

¿Qué distancias se dan entre dos clases de tricordios distintas?

> *Solución:* Dos tricordios tienen 3 pares cada uno, así que por el teorema 1 su distancia es par, y no es 0, porque ningún par de clases de tricordios está en relación Z. Los valores que se dan son 2, 4 y 6: (037) está a 2 de (025), a 4 de (048) y a 6 de (012).

---

## 4. Lo que no puede ver

Cada uno de los límites siguientes se deduce del §3: la distancia es una función de dos vectores, así que una operación que conserva el vector le resulta invisible.

**La conducción de voces.** Mueve una nota de do mi sol un semitono, hacia arriba o hacia abajo. Los seis resultados son mi sol si (mi menor) y do mi♭ sol (do menor) a distancia 0, y do♯ mi sol (do♯ disminuido), do fa sol (Csus4), do mi fa♯ y do mi sol♯ (do aumentado) a distancia 4. Las tres clases de tricordios más cercanas a do mayor por contenido interválico, a distancia 2, son (014), (015) y (025), y ninguna está a un semitono: sus representantes más cercanos, como mi♭ mi sol, do mi fa y re mi sol, necesitan tres, dos y dos semitonos de movimiento, sumando lo que se mueve cada voz. Una distancia sobre vectores no puede ordenar los acordes por cuánto se mueve la mano. El §6 de MAT-022 muestra que la búsqueda de caminos de IX no consigue, por esta razón, unir la tríada aumentada y do mayor, y la búsqueda de GA falla de la misma manera (§5).

**El mayor y el menor, las tonalidades y los modos.** Do mayor y do menor están a distancia 0, ya que una inversión conserva el vector. Lo mismo vale para las doce escalas mayores, incluidas do mayor y fa♯ mayor: una transposición conserva el vector, así que una distancia sobre vectores no puede contar alteraciones. Un modo de una escala es el mismo conjunto de clases de altura, y do menor natural contiene las notas de mi♭ mayor, así que ambas escalas están a distancia 0 de cada escala mayor.

**Las notas que contiene un acorde.** 4-Z15, do do♯ mi fa♯, y 4-Z29, do do♯ mi♭ sol, están ambos a distancia 3 de do mayor, con el mismo delta <+1, +1, 0, 0, 0, +1>. 4-Z29 contiene una tríada menor, do mi♭ sol; 4-Z15 no contiene ninguna tríada mayor ni menor. Estar a distancia 3 de do mayor no significa «do mayor más una nota»: otras tres clases de tetracordios están a distancia 3 sin ninguna tríada mayor ni menor, como 4-Z15 (§3).

**La relación Z.** Esos dos conjuntos comparten el vector <111111> y están a distancia 0 uno del otro, aunque ninguna transposición ni inversión lleva uno sobre el otro.

### Ejercicio práctico

Un usuario pide «un acorde de cuatro notas cercano a do mayor» y recibe las clases de tetracordios a distancia 3, la menor distancia posible para un conjunto de cuatro notas. ¿Cuáles contienen una tríada mayor o menor?

> *Solución:* 9 de las 13. (0125), (0135), (0145) y (0146) no contienen ninguna. La distancia ordena las 13 por igual.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`40d3374`](https://github.com/GuitarAlchemist/ga/tree/40d337479af36d987df3f06c8c638ffd35f13458), la rama `main` de GA el 2026-10-06; esta lección documenta ese código sin modificarlo, y no ha ejecutado GA ni sus pruebas. El curso ga-ai de Learn ejecutó parte del mismo código, compilado en dos commits anteriores de GA en los que el código implicado es el mismo que en `40d3374`, y sus salidas se citan donde corresponde. Los demás números vienen de una transcripción en Python, línea por línea, del código de GA citado.

**El delta.** [`GrothendieckDelta`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L8-L11) es «a signed delta in the Grothendieck group», con una suma y un opuesto que cumplen las leyes de grupo ([líneas 139-167](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L139-L167)). [`FromIcVs`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L113) resta los dos vectores componente a componente, y luego:

```csharp
        // Heuristic: When two distinct sets share the same ICV (e.g., diatonic modes/keys),
        // L1 difference is zero. To preserve musical differentiation expected by callers/tests,
        // emit a minimal non-zero delta focused on ic1. This keeps related keys close but not identical.
        if (delta.L1Norm == 0)
        {
            delta = delta with { Ic1 = 1 };
        }
```

El comentario habla de «two distinct sets», pero el método solo ve dos vectores, así que también da <+1, 0, 0, 0, 0, 0> para un conjunto comparado consigo mismo: para los 200 vectores, según la transcripción. Por tanto, la aplicación incumple las tres leyes del §2. δ(A, A) no es 0. De do menor de vuelta a do mayor, vuelve a dar <+1, 0, 0, 0, 0, 0>, no el opuesto del delta de ida. Y do mayor → do menor → do mayor suma <+2, 0, 0, 0, 0, 0>. Entre dos vectores distintos, la transcripción la encuentra igual al delta verdadero. El +1 cae en la clase de intervalo 1, donde no cambió ningún par de notas, y [`Explain`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L172) lo lee como «+1 ic1 (semitone)» y, como [una ganancia en ic1 o ic2](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L229-L232) se comprueba primero, como «more chromatic color». La issue [#776](https://github.com/GuitarAlchemist/ga/issues/776) de GA señala la heurística y pide que `ComputeDelta(v, v).L1Norm` sea 0. La [lección 14 del curso ga-ai](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/14-what-the-substitution-skill-answers.md) de Learn imprimió `ComputeDelta(...).L1Norm = 1` para C frente a C, frente a Am y frente a F♯, y para G7 frente a D♭7 ([salida](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l14.txt#L64-L67)), compilando GA en `a826864`, donde `GrothendieckDelta.cs` es el mismo que en `40d3374`.

GA tiene un segundo delta. [`IcvDelta`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.DSL/Generators/OptickGrothendieck.fs#L77-L93), en el archivo `OptickGrothendieck.fs` del DSL, representa «elements of the Grothendieck group Z^6» y resta sin heurística, así que los dos deltas de GA discrepan exactamente en los vectores iguales. Su prueba, [`Grothendieck_IcvDelta_IsAbelianGroupAndCancellative`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/OptickGrothendieckTests.cs#L143-L155), comprueba el elemento neutro y el opuesto sobre un solo delta; no comprueba ni la conmutatividad, ni la asociatividad, ni la propiedad cancelativa, y no toca `GrothendieckDelta`.

**Las escalas de las pruebas.** Las pruebas de GA escriben los conjuntos como cadenas de dígitos, leídas carácter a carácter ([`PitchClassSet.TryParse`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L728-L748)), mediante [`PitchClass.TryParseSetNotation`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L275-L294), que lee A y B como 10 y 11 y pasa todo lo demás a [`PitchClass.TryParse`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L244-L267): los dígitos, T para 10, E para 11, y los nombres de notas, que estas cadenas no usan. [`ShouldComputeDelta_FromCMajorToGMajor`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L73-L90) lee sol mayor como [«02479E1»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L77), con el comentario «G A B C D E F#», y `OptickGrothendieckTests` [lo repite](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/OptickGrothendieckTests.cs#L27). Los dígitos dan do do♯ re mi sol la si: un 1 donde sol mayor necesita un 6. Ese conjunto tiene el vector <354351>, no el diatónico <254361>, y su delta verdadero desde do mayor es <+1, 0, 0, 0, −1, 0>, a distancia 2. El «do menor» de [`ShouldComputeDelta_FromCMajorToCMinor`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L62-L70), «0235789», es do re mi♭ fa sol la♭ la, con el vector <344352>, a distancia 4; do menor natural sería «023578T». Según la transcripción:
- `FromCMajorToCMinor` afirma una L1 mayor que 0 y una explicación que contiene «ic», y [`ShouldComputeDelta_WithExplanation`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L93-L108), sobre el mismo «02479E1» que `FromCMajorToGMajor`, afirma que la explicación contiene «ic1». Ambas pasan con el delta verdadero. Con do menor natural en la primera prueba, el modo al que apunta su comentario («Moves between modes»), y el verdadero sol mayor en la segunda, los dos deltas verdaderos serían 0, y las dos pruebas solo pasarían gracias a la heurística: sin ella, `Explain` devolvería «No change». #776 lee la primera prueba como una comparación de do mayor con do menor natural, que comparten un vector, y concluye que pasa «only because of the rule above». En `40d3374`, como en el commit que cita #776, el conjunto de la prueba no es do menor natural, y la prueba pasa con el delta verdadero de 4.
- `FromCMajorToGMajor` afirma una L1 menor que 5: 2 para el conjunto que usa; 1, por la heurística, para el verdadero sol mayor.
- [`ShouldFindShortestPath_BetweenRelatedKeys`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L267-L279) solo comprueba los dos extremos del camino, que tiene un paso tanto si el destino es «02479E1» como si es el verdadero sol mayor.
- La prueba de `IcvDelta` de arriba usa el mismo «sol mayor»: su delta solo es distinto de cero por el dígito equivocado.

**Vecindades y caminos.** El coste es la norma L1 multiplicada por 0.6 ([líneas 39-42](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L39-L42)), que [`ShouldComputeHarmonicCost_AsL1Norm`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L115) comprueba con 5.4 para una norma de 9. [`FindNearby`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L45) recorre los 4,096 conjuntos, [pone el origen primero, con coste 0](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L58-L62), [descarta el origen por valor](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L72-L77) y se queda con cada conjunto cuyo delta heurístico cae dentro del radio, ordenados por coste. Cualquier otro conjunto con el vector del origen aparece a distancia 1, nunca 0. Según la transcripción, desde do mayor (la tríada), el radio 0 devuelve solo do mayor; el radio 1 devuelve do mayor y las otras 23 tríadas mayores y menores, y nada más; el radio 2 añade 108 díadas y tricordios a distancia verdadera 2, 132 conjuntos en total. Desde la escala de do mayor, el radio 1 devuelve sus 12 transposiciones, ella misma incluida, y el radio 2 devuelve 36 conjuntos.

[`FindShortestPath`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L118) busca en anchura mediante `FindNearby(current, 2)`, entre los conjuntos del tamaño actual ([líneas 148-151](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L148-L151)). Su comentario dice que el radio 2 [«connects closely related diatonic collections (e.g., C major → G major)»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L146-L147), que «typically differ by one accidental yet may exceed radius=1». Por el §4, dos escalas mayores cualesquiera están a distancia 0, y a 1 por la heurística: la métrica no ve la alteración, y cada tonalidad está a un paso de todas las demás. La transcripción va de la escala de do mayor a la de fa♯ mayor en un paso, como de do mayor a sol mayor; de la tríada de do mayor a do menor y a fa♯ mayor, en un paso cada uno; y no encuentra ningún camino de do mayor a do mi sol♯, ya que ninguna otra clase de tricordios está a 2 o menos de (048). El §6 de MAT-022 encuentra la misma laguna en IX, y la issue [#802](https://github.com/GuitarAlchemist/ga/issues/802) de GA la señala, con los caminos de un paso entre tríadas, en la `IcvShortestPathSkill` del chatbot.

**Las dos skills del chatbot.** La [lección 23 del curso ga-ai](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/23-harmonic-distance-and-path.md) de Learn llamó directamente a [`GrothendieckDeltaSkill`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L97-L131), compilando la rama `main` de GA en `f4f5b4a`, donde la skill, el delta y el servicio son los mismos que en `40d3374`. Cinco de los diez [prompts de ejemplo](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L46-L58) de la skill nombran dos acordes de una misma clase de conjuntos. La skill rechaza uno de ellos, «how different are C major and F major harmonically», porque «major» se interpone entre el primer acorde y «and», como señala la lección 23. Responde a los otros cuatro: C a G, Am y Em, Cmaj7 y Fmaj7, C a F. Para cada uno, en ambos sentidos, la ejecución imprimió el delta [+1, 0, 0, 0, 0, 0], L1 1, coste 0.60, y luego «+1 ic1 (semitone)» y «more chromatic color» ([salida, líneas 58-63](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l23-main.txt#L58-L63) y [66-67](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l23-main.txt#L66-L67)). La skill [explica](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L123-L128) después que cada componente «says how many more occurrences of that interval-class the target has than the source»: sol mayor tendría un semitono más que do mayor, cuando ninguno de los dos tiene ninguno. #802 lo señala, junto con la flecha mal codificada que `Explain` imprime entre las dos partes. La [lección 22 del curso ga-ai](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/22-similar-chords.md) de Learn ejecutó [`IcvNeighborsSkill`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L120-L140), que recalcula el delta verdadero a causa de la heurística ([su comentario](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L122-L129)). Por el teorema 1, todo conjunto a distancia 1 o 2 de un acorde de tres notas está a 2, así que la skill se queda con los ocho primeros en el orden de `FindNearby`, que es el orden de las máscaras de bits de los conjuntos. Para C: {0,3}, {0,4}, {1,4}, {0,1,4}, {0,3,4}, {0,5}, {1,5} y {0,1,5}, cinco clases de conjuntos, anunciados como el [«top 8 by harmonic cost»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L146) ([salida](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l22-main.txt#L90-L98)). La issue [#798](https://github.com/GuitarAlchemist/ga/issues/798) de GA lo señala. El filtro de la skill [descarta la distancia 0](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L136) como «exact ICV-identical (same set class)», lo que también descartaría una compañera Z; ninguno de los acordes que construye la skill tiene una.

**La herramienta MCP.** [`GaIcvNeighbors`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L325), de GaMcpServer, calcula bien la distancia. [Recalcula la L1 verdadera](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L337-L348), y su comentario nombra la heurística; descarta la propia clase de conjuntos del acorde y lista cada clase una sola vez. Según la transcripción, `GaIcvNeighbors("C", 2)` lista (03), (04), (014), (05), (015) y (025), todas a Δ=2. [Sus dos pruebas](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L72-L94) comprueban que la respuesta a distancia 1 para C no nombra Forte 3-11, y que a distancia 2 cada línea está a Δ=2, ninguna línea se repite ni nombra Forte 3-11, y Forte 3-7 aparece. Con la distancia por defecto, 1, no lista nada para C. Por el teorema 1, para un conjunto de tres notas o más, la distancia 1 solo puede añadir una compañera Z, a distancia 0, como dice la [descripción](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L327-L328) de la herramienta: «distance 0 is a Z-related set».

Las issues #776, #798 y #802 de GA cubren la heurística y las dos skills. Mientras se escribe esta lección, ninguna issue de GA cubre las escalas de las pruebas, el comentario sobre los caminos ni la prueba de `IcvDelta`. Corregir cualquiera de ellos corresponde a los responsables de GA; esta lección solo los describe.

### Ejercicio práctico

¿Pasaría `ShouldComputeDelta_WithExplanation` con la verdadera escala de sol mayor, «024679E», si `FromIcVs` devolviera el delta verdadero?

> *Solución:* No. La verdadera escala de sol mayor es una transposición de la de do mayor, así que el delta verdadero es 0, y `Explain` devuelve «No change», que no contiene «ic1». Con la heurística, pasa con <+1, 0, 0, 0, 0, 0>. Con el conjunto que usa la prueba, pasa en ambos casos, con <+1, 0, 0, 0, −1, 0>.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA; la versión de GA fijada en el laboratorio pasaría primero a `40d3374`. Nada en ella es una medición. Las predicciones vienen del §3 y de la transcripción del §5, y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje. Las skills del chatbot quedan fuera, ya que las lecciones 22 y 23 del curso ga-ai de Learn ya las ejecutaron.

1. **Los deltas.** Llamar a `GrothendieckService.ComputeDelta` y a `IcvDelta.Between` sobre los vectores de do mayor y do menor («047», «037»), de do mayor y re mayor («047», «269»), de 4-Z15 y 4-Z29 («0146», «0137»), de la escala de do mayor y la verdadera escala de sol mayor («024579E», «024679E»), y de la escala de do mayor y «02479E1». Predicción: para los cuatro primeros pares, `IcvDelta` es cero y `ComputeDelta` es <+1, 0, 0, 0, 0, 0>; para el último, ambos dan +1 en la clase de intervalo 1 y −1 en la clase de intervalo 5.
2. **Las leyes.** Sobre los 200 vectores distintos de los 4,096 conjuntos, probar las tres leyes del §2 en `ComputeDelta` y en `IcvDelta`. Predicción: `IcvDelta` cumple cada ley en cada par y cada terna. `ComputeDelta(v, v)` es <+1, 0, 0, 0, 0, 0> para los 200 vectores; la antisimetría falla solo en los 200 pares iguales; la aditividad falla en las 119,600 ternas cuyos tres vectores no son todos distintos, y solo ahí.
3. **Las vecindades.** Contar lo que devuelve `FindNearby` desde do mayor («047») con radio 0, 1 y 2, y desde la escala de do mayor con radio 1 y 2. Predicción: 1, 24 y 132; 12 y 36.
4. **Los caminos.** Llamar a `FindShortestPath` de la escala de do mayor a fa♯ mayor («13568TE») y a la verdadera escala de sol mayor, y de la tríada de do mayor («047») a la de do menor («037») y a do mi sol♯ («048»). Predicción: dos conjuntos cada uno para los tres primeros; un camino vacío para el último.
5. **Las escalas de las pruebas.** Imprimir los elementos y los vectores de «02479E1» y «0235789». Predicción: {0, 1, 2, 4, 7, 9, 11} con <354351>, y {0, 2, 3, 5, 7, 8, 9} con <344352>.
6. **La herramienta MCP.** Llamar a `GaClosureBootstrap.init()`, como hacen las pruebas de GA, y luego a `GaIcvNeighbors("C", 1)` y `GaIcvNeighbors("C", 2)`. Predicción: el mensaje «No other set class within distance 1 of C», y luego seis clases a Δ=2, entre ellas Forte 3-7.

### Ejercicio práctico

¿De dónde sale el 119,600 del paso 2?

> *Solución:* La heurística solo actúa con vectores iguales. Cuando a, b y c son todos distintos, cada término es una diferencia verdadera y la ley se cumple. Cuando a = b ≠ c, el lado izquierdo lleva el +1 del primer término; cuando b = c ≠ a, el del segundo. Cuando a = c ≠ b, el lado izquierdo es 0 y el derecho <+1, 0, 0, 0, 0, 0>. Cuando a = b = c, el lado izquierdo es <+2, 0, 0, 0, 0, 0> y el derecho <+1, 0, 0, 0, 0, 0>. Así, la ley falla exactamente en las 200³ − 200 × 199 × 198 = 8,000,000 − 7,880,400 = 119,600 ternas que no son todas distintas.

---

## 7. Errores comunes

- **Leer la distancia 0 como «el mismo acorde».** Significa el mismo vector: una transposición, una inversión o una compañera Z.
- **Leer una distancia pequeña como un movimiento pequeño.** Mover una nota de do mayor un semitono da distancia 0 o 4; las clases de tricordios a distancia 2 necesitan dos o tres semitonos de movimiento.
- **Esperar que la distancia cuente alteraciones.** Cada tonalidad mayor está a distancia 0 de todas las demás.
- **Leer un delta como una receta.** Un delta dice cuántos pares de cada clase aparecen o desaparecen, no qué notas cambian: de do mayor a Cmaj7 y de do mayor a Fmaj7 hay un mismo delta.
- **Parchear un cero.** Sustituir un delta nulo por uno «minimal non-zero» incumple δ(A, A) = 0, la antisimetría y la aditividad, y señala un cambio en una clase de intervalo en la que no cambió ningún par.
- **Fiarse del comentario de una prueba.** Una prueba comprueba el conjunto que construye su código, no el que nombra su comentario: «02479E1» no es sol mayor.
- **Comparar conjuntos de tamaños distintos.** La cota de tamaño vale sean cuales sean las notas: un acorde de tres notas y uno de cuatro nunca están a menos de 3.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Monoide conmutativo** | Un conjunto con una suma asociativa y conmutativa y un elemento neutro, como N^6 con la suma componente a componente |
| **Cancelativo** | Dicho de un monoide en el que a + k = b + k solo se cumple si a = b |
| **Grupo de Grothendieck** | K(M), las clases de pares (a, b) leídos como a − b: todo homomorfismo de M en un grupo se extiende a él de una única manera; K(N^6) = Z^6 |
| **Delta de Grothendieck** | δ(A, B) = ICV(B) − ICV(A), un elemento de Z^6 |
| **Norma L1** | La suma de los valores absolutos de los seis componentes de un delta |
| **Distancia de contenido interválico** | d(A, B), la norma L1 de δ(A, B): una métrica sobre los vectores, una pseudométrica sobre los conjuntos |
| **Cota de tamaño** | La distancia es al menos la diferencia absoluta entre los números de pares de los dos conjuntos, T(n) = n(n − 1)/2, y tiene la misma paridad |

---

## Autoevaluación

**1. ¿Cuál es el delta de do mayor a C7, y cuál es la distancia?**
> <0, +1, +1, 0, 0, +1>, a distancia 3. C7 añade si♭ a do mayor, y por el teorema 2 una nota añadida a un conjunto de tres notas cuesta siempre 3.

**2. ¿Por qué ningún acorde de cuatro notas puede estar a distancia 1 o 2 de un acorde de tres notas?**
> Los componentes del delta suman T(4) − T(3) = 3, así que su norma L1 es al menos 3 (teorema 1).

**3. `FindNearby` de GA devuelve 24 conjuntos dentro del radio 1 de la tríada de do mayor. ¿Cuáles son, y cuál es su distancia verdadera a do mayor?**
> Do mayor mismo y las otras 23 tríadas mayores y menores. Todas comparten el vector <001110>, así que su distancia verdadera es 0; la heurística pone las 23 a 1.

**4. ¿Puede `GaIcvNeighbors` con distancia 1 listar algo para un acorde de séptima de dominante?**
> Solo una compañera Z, a distancia 0: una distancia de exactamente 1 solo se da entre un conjunto de dos notas y uno de como mucho una. La clase del acorde de séptima de dominante, 4-27, no tiene compañera Z, así que la herramienta no lista nada.

**Criterio de aprobación:** Construir K(M) y explicar por qué K(N^6) = Z^6; calcular deltas y distancias; demostrar la cota de tamaño, la regla de la nota añadida y el teorema de la distancia cero; nombrar lo que la distancia no puede ver; y decir dónde la heurística, los comentarios y las pruebas de GA se apartan de las matemáticas.

---

## Base de investigación

- D. Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press, 1987: la función de intervalos de dos conjuntos
- S. Lang, *Algebra*, tercera edición revisada, Springer, 2002: el grupo de Grothendieck de un monoide conmutativo
- MUS-020 de Streeling para los vectores de clases de intervalo y la relación Z, y MAT-022 para los grupos, los invariantes y la búsqueda de caminos de IX
- Código fuente de GA en el commit `40d337479af36d987df3f06c8c638ffd35f13458`, y las issues #776, #798 y #802 de GA: cada hecho de código del §5 enlaza a su línea
- El curso ga-ai de Learn, lecciones 14, 22 y 23, en el commit `1190ee33650a5637414e73a455b69f3914f44fd6` de Learn: las salidas de ejecución citadas en el §5
- Comprobaciones en Python sobre los 4,096 conjuntos: cada uno de los demás números de los §§1–5 sale de ellas o de la transcripción del código de GA
- Experimento: propuesto en el §6, no ejecutado; esta lección no aporta ninguna medición nueva de GA
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
