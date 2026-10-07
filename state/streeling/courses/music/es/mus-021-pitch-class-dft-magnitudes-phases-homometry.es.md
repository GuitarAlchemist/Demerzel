---
module_id: mus-021-pitch-class-dft-magnitudes-phases-homometry
department: music
course: La TDF de las clases de altura — módulos, fases y homometría
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites: [mus-020-set-classes-interval-vectors-prime-forms, mat-021-fourier-analysis-signals]
estimated_duration: "75 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# La TDF de las clases de altura — Lo que conservan los módulos y lo que añaden las fases

> **Departamento de Música** | Etapa: Citrinitas (Intermedio a avanzado) | Duración estimada: 75 minutos

## Objetivos

Al terminar esta lección, podrás:
- Calcular los coeficientes de Fourier de un conjunto de clases de altura y leerlos como sumas de puntos sobre un círculo
- Demostrar que la transposición y la inversión conservan los módulos, decir qué hacen con las fases y decir qué hace M5 con los módulos
- Deducir el lema de Lewin y usarlo para explicar por qué los conjuntos en relación Z comparten todos sus módulos
- Nombrar los conjuntos que maximizan cada uno de los seis módulos, y predecir a partir de la simetría de un conjunto qué coeficientes se anulan
- Comparar dos conjuntos por sus fases, y decir exactamente qué muestra y qué no muestra una similitud de fase igual a 1
- Seguir lo que GA calcula para cada uno de estos puntos, y dónde sus nombres, su documentación y sus pruebas dicen otra cosa

---

## 1. Un conjunto como señal

Numera las clases de altura de do = 0 a si = 11, como hace MUS-020, y escribe un conjunto de clases de altura A como una señal de 12 muestras: 1 en cada clase de altura de A, 0 en las demás. MAT-021 define la transformada discreta de Fourier de una señal así. Para un conjunto, la suma recorre sus notas:

X_k(A) = Σ_(x ∈ A) e^(−2πikx/12), para k = 0, 1, …, 11.

Cada nota aporta un punto del círculo unidad, con un ángulo de −30k·x grados, y X_k suma esos puntos. Para k = 1, las notas conservan su lugar en el círculo cromático. Para k = 5, la nota x pasa al lugar de 5x, y el círculo se convierte en el ciclo de cuartas: do, fa, si♭, mi♭ y así sucesivamente. X_0 es el número de notas, n. La señal es real, así que X_(12−k) es el conjugado de X_k (MAT-021 §1), y los coeficientes para k = 0 a 6 llevan toda la información. Esta lección usa solo esos.

Un coeficiente es grande cuando sus puntos se agrupan y pequeño cuando se reparten alrededor del círculo. Su **módulo** |X_k| mide cuánto se agrupan, y su **fase**, el ángulo φ_k de X_k, dice dónde. Para do mayor {0, 4, 7} y k = 5, los tres puntos quedan en 0°, 120° y 30° (do, mi y sol, ya que −600° y −1050° equivalen a 120° y 30° en el círculo), y su suma es X_5 = 1.366 + 1.366i, de módulo 1.932 y fase 45°.

### Ejercicio práctico

Calcula todos los coeficientes del tritono do fa♯, {0, 6}.

> *Solución:* X_k = 1 + e^(−2πi·6k/12) = 1 + e^(−πik) = 1 + (−1)^k. Los coeficientes valen 2 para k par y 0 para k impar.

---

## 2. Transposición, inversión y M5

Transponer A en t lleva cada nota x a x + t, y su término se convierte en e^(−2πik(x+t)/12) = e^(−2πikt/12) e^(−2πikx/12). Todos los términos se multiplican por el mismo factor, así que

X_k(T_t A) = e^(−2πikt/12) X_k(A).

Es el **teorema del desplazamiento**. El módulo no cambia, y la fase gira −30kt grados: cada coeficiente gira a su propia velocidad, k veces más rápido que el primero. La inversión I0 lleva x a −x, lo que sustituye cada término por su conjugado, así que X_k(I0 A) es el conjugado de X_k(A): el módulo se mantiene y la fase cambia de signo. Estas operaciones llevan de cualquier conjunto de una clase de conjuntos a cualquier otro, así que los seis módulos |X_1| a |X_6| son los mismos para todos los conjuntos de una clase.

M5, que multiplica cada clase de altura por 5, no es una de esas operaciones, pero su efecto es sencillo. Lleva el término de la nota x a e^(−2πik·5x/12), que es el término de x en X_5k. Así, X_k(M5 A) = X_(5k mod 12)(A). Para k = 1 a 6, 5k mod 12 vale 5, 10, 3, 8, 1 y 6, y |X_10| = |X_2|, |X_8| = |X_4|. M5 intercambia |X_1| y |X_5| y conserva los demás módulos. Es la cara espectral del §2 de MUS-020, donde M5 intercambia los recuentos de las clases de intervalo 1 y 5. El pentacordio cromático do do♯ re mi♭ mi tiene |X_1| = 3.732 y |X_5| = 0.268. Su imagen por M5, la escala pentatónica, tiene lo contrario.

Una comprobación en Python sobre los 4,096 conjuntos y las 12 transposiciones halla el teorema del desplazamiento, la conjugación y la regla de M5 exactos salvo redondeo, con diferencias menores que 10⁻¹³.

### Ejercicio práctico

Para do mayor, X_5 tiene fase 45°. Sin sumar ningún término, halla la fase de X_5 para re mayor y para do menor.

> *Solución:* Re mayor es T2 de do mayor, así que la fase gira −30 × 5 × 2 = −300°, es decir, +60°: 105°. Do menor {0, 3, 7} es I7 de do mayor, ya que 7 − {0, 4, 7} = {7, 3, 0}, e I7 es I0 seguida de T7. I0 convierte 45° en −45°, y T7 la hace girar −30 × 5 × 7 = −1050°, es decir, +30°: −15°. El módulo sigue siendo 1.932 en ambos casos.

---

## 3. El lema de Lewin y la homometría

Multiplica X_k por su conjugado:

|X_k|² = Σ_(x ∈ A) Σ_(y ∈ A) e^(−2πik(x−y)/12).

Los n términos con x = y dan n. Cada par de notas distintas aparece dos veces, como x − y y como y − x, y los dos términos suman 2 cos(2πk(x − y)/12). Ese coseno depende solo de la clase de intervalo d del par, en la forma cos(πkd/6). Agrupando los pares por clase de intervalo:

|X_k|² = n + 2 Σ_(d=1..6) ICV_d cos(πkd/6),

donde ICV_d es el recuento de la clase de intervalo d en el vector de clases de intervalo del §2 de MUS-020. Es el **lema de Lewin**, llamado así por Lewin (1959). Para do mayor, n = 3 y el vector es <001110>. Para k = 3, los cosenos para d = 3, 4 y 5 son cos 270° = 0, cos 360° = 1 y cos 450° = 0, así que |X_3|² = 3 + 2 = 5 y |X_3| = 2.236.

La fórmula también se lee al revés. Sus siete ecuaciones, para k = 0 a 6, forman una transformada de cosenos, y se pueden resolver para obtener n y los seis recuentos. Así, los siete módulos |X_0| a |X_6| y el par (n, vector) llevan la misma información: los 4,096 conjuntos tienen 201 perfiles distintos de siete módulos y 201 pares distintos, en correspondencia uno a uno. n importa en los dos lados: el conjunto vacío y una nota sola comparten el vector <000000> pero no n, y sin |X_0| los seis módulos |X_1| a |X_6| solo dan 118 perfiles, y ni siquiera distinguen un conjunto de su complemento, cuyos coeficientes son −X_k para todo k distinto de 0, ya que los del agregado valen 0.

Dos conjuntos son **homométricos** cuando tienen los mismos siete módulos |X_0| a |X_6|, es decir, el mismo tamaño y los mismos |X_1| a |X_6|. Las clases de conjuntos en relación Z (§5 de MUS-020) tienen el mismo tamaño y el mismo vector, así que por el lema de Lewin comparten los siete. Los tetracordios de todos los intervalos 4-Z15 (0146) y 4-Z29 (0137) no se pueden distinguir con ninguna función de los módulos, y lo mismo vale para los 23 pares en relación Z.

### Ejercicio práctico

Calcula |X_5| de do mayor a partir de su vector, y compáralo con el §1.

> *Solución:* Para k = 5, los cosenos para d = 3, 4 y 5 son cos 450° = 0, cos 600° = −0.5 y cos 750° = 0.866. Así, |X_5|² = 3 + 2(−0.5 + 0.866) = 3.732, y |X_5| = 1.932, como en el §1.

---

## 4. Seis cualidades

Cada módulo mide un tipo de regularidad. Quinn (2006–07) leyó los seis módulos como seis cualidades armónicas, cada una juzgada por lo cerca que queda un conjunto de los conjuntos que la maximizan. Una búsqueda en Python entre todos los conjuntos de cada tamaño encuentra esos conjuntos:

- **k = 1**, los clusters cromáticos: do do♯ re entre los conjuntos de tres notas, con 2.732, y el hexacordio cromático entre los de seis, con 3.864.
- **k = 2**, dos clusters a un tritono uno del otro: do fa♯ con 2, el único conjunto de dos notas que lo alcanza salvo transposición, do do♯ fa♯ sol con 3.464, y do do♯ re fa♯ sol la♭ con 4.
- **k = 3**, el ciclo de terceras mayores: la tríada aumentada con 3, y la escala hexatónica do do♯ mi fa sol♯ la con 4.243.
- **k = 4**, el ciclo de terceras menores: el acorde de séptima disminuida y la escala octatónica, ambos con 4.
- **k = 5**, las cadenas de quintas: do re sol con 2.732, la escala pentatónica con 3.732, do re mi fa sol la entre los de seis, con 3.864, y entre los conjuntos de siete notas la colección diatónica, también con 3.732.
- **k = 6**, la escala de tonos enteros, con 6. Las clases de altura pares y las impares forman las dos escalas de tonos enteros, y X_6 = Σ_(x ∈ A) (−1)^x cuenta las notas pares de un conjunto menos sus notas impares.

Los módulos de algunos conjuntos conocidos muestran las cualidades lado a lado:

| Conjunto | n | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 | k = 6 |
|---|---|---|---|---|---|---|---|
| Tríada mayor do mi sol | 3 | 0.518 | 1 | 2.236 | 1.732 | 1.932 | 1 |
| Tríada aumentada do mi sol♯ | 3 | 0 | 0 | 3 | 0 | 0 | 3 |
| Cluster cromático do do♯ re | 3 | 2.732 | 2 | 1 | 0 | 0.732 | 1 |
| Tritono do fa♯ | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| Séptima de dominante do mi sol si♭ | 4 | 0.518 | 1 | 1.414 | 2.646 | 1.932 | 2 |
| Séptima mayor do mi sol si | 4 | 0.518 | 1.732 | 2.828 | 1 | 1.932 | 0 |
| Séptima disminuida do mi♭ sol♭ la | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| Pentatónica do re mi sol la | 5 | 0.268 | 1 | 1 | 1 | 3.732 | 1 |
| Escala de tonos enteros | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| Hexatónica do do♯ mi fa sol♯ la | 6 | 0 | 0 | 4.243 | 0 | 0 | 0 |
| Escala diatónica de do mayor | 7 | 0.268 | 1 | 1 | 1 | 3.732 | 1 |
| Octatónica do do♯ mi♭ mi fa♯ sol la si♭ | 8 | 0 | 0 | 0 | 4 | 0 | 0 |

Así que ningún número solo dice si un acorde suena *a tonos enteros* o *a quintas*, pero un número por cualidad sí. C7 y Cmaj7 están igual de cerca de las quintas, con 1.932 en k = 5, pero C7 se inclina hacia la escala de tonos enteros, con 2 en k = 6, frente a 0 para Cmaj7, que se inclina hacia la tríada aumentada, con 2.828 en k = 3.

Los ceros se deducen de la simetría. Si T_p lleva A sobre sí mismo, el teorema del desplazamiento da X_k(A) = e^(−2πikp/12) X_k(A), así que X_k = 0 salvo que kp sea múltiplo de 12. Entre k = 1 y 6, la tríada aumentada y la escala hexatónica, fijadas por T4, solo pueden ser distintas de cero en k = 3 y 6. La séptima disminuida y la escala octatónica, fijadas por T3, solo en k = 4. La escala de tonos enteros, fijada por T2, solo en k = 6, y el tritono, fijado por T6, solo en los k pares. La comprobación en Python no encuentra ninguna excepción entre los 4,096 conjuntos. El recíproco falla: ninguna transposición fija Cmaj7, y sin embargo X_6 = 0, ya que tiene dos notas pares y dos impares.

### Ejercicio práctico

¿Por qué |X_6| de la escala de tonos enteros do re mi fa♯ sol♯ si♭ es el mayor valor que puede alcanzar un conjunto?

> *Solución:* Sus notas son las clases de altura pares, así que cada término e^(−2πi·6x/12) = (−1)^x vale +1. Los seis términos se suman en fase, y |X_6| = 6. Ningún conjunto lo supera: X_6 es el número de notas pares menos el de notas impares, como mucho 6 en valor absoluto.

---

## 5. Lo que añaden las fases

Los módulos no distinguen un conjunto de sus transposiciones e inversiones, ni una clase de un par en relación Z de la otra. Las fases sí. Por el §2, transponer en t hace girar la fase de X_k −30kt grados, todos los coeficientes a la vez, cada uno a su propia velocidad. Para comparar B con A salvo transposición, gira las fases de B para cada t y mide cuánto se alinean con las de A, ponderando cada coeficiente por los dos módulos:

S(A, B) = max sobre t de Σ_(k=1..6) |X_k(A)| |X_k(B)| cos(φ_k(A) − φ_k(B) + 30°·kt) / Σ_(k=1..6) |X_k(A)| |X_k(B)|.

Los valores de t que alcanzan el máximo se escriben t*. Si B = T_u A, cada coseno vale 1 en t = −u, así que S = 1. Do mayor frente a re mayor da S = 1 en t = 10, la transposición que devuelve re mayor a do mayor. S no cambia cuando se transpone cualquiera de los dos conjuntos. Do mayor frente a do menor da S = 0.5714, porque una inversión cambia el signo de las fases en lugar de hacerlas girar. Comparar A también con la inversión de B, cuyos coeficientes son los conjugados de los de B, da S_TnI(A, B), el mayor de los dos valores. Vale 1 para do mayor y do menor. En los 23 pares en relación Z, S_TnI queda por debajo de 1, como mucho 0.6667: las fases separan los conjuntos que los módulos no separan.

**S = 1 no significa una transposición.** Cada término de S, en la suma y en el denominador, es cero salvo que ambos conjuntos tengan un coeficiente distinto de cero en ese k, y los módulos solo ponderan los cosenos. S llega a 1 en cuanto, para un t, se anulan todas las diferencias de fase en los coeficientes compartidos. Toma do re mi y la tríada aumentada do mi sol♯. Para k = 1 a 6, los coeficientes de la tríada aumentada son 0, 0, 3, 0, 0 y 3, y los de do re mi son 1 − 1.732i, 0, 1, 0, 1 + 1.732i y 3. Solo cuentan k = 3 y k = 6, y ahí ambos conjuntos tienen fase 0. En t = 0 los dos cosenos valen 1, y S = (1 × 3 + 3 × 3) / (1 × 3 + 3 × 3) = 1, también en t = 4 y t = 8, ya que T4 y T8 fijan la tríada aumentada. Sin embargo, do re mi, (024), y do mi sol♯, (048), son clases de conjuntos distintas. Cuando ningún k tiene sus dos coeficientes distintos de cero, como en la tríada aumentada frente a la séptima disminuida, S vale 0/0. GA fija entonces S en 0, y en 1 solo cuando cada uno de los dos conjuntos es el conjunto vacío o el agregado. Los recuentos del párrafo siguiente siguen esa convención: entre los pares que recorren, 268 son de este tipo y reciben S = 0.

Ni siquiera hacen falta ceros. El pentacordio cromático do do♯ re mi♭ mi y la escala pentatónica do re mi sol la no tienen ningún coeficiente nulo, y sus módulos difieren (§2), pero sus fases coinciden en t = 0, y S = 1. Sobre todos los pares de tipos Tn distintos, dejando aparte el conjunto vacío y el agregado, 270 pares del mismo tamaño y 1,230 pares de tamaños distintos alcanzan S = 1. Entre acordes: Csus2 y C9 en t = 0, y Cmaj7 y Cdim7 en t = 1, 4, 7 y 10.

S = 1 sí da una transposición cuando los dos conjuntos tienen además el mismo tamaño y los mismos módulos. Entonces las fases coinciden en cada coeficiente distinto de cero, así que los coeficientes de A igualan los de una transposición de B para k = 0 a 6, y por conjugación para todo k. La TDF inversa convierte coeficientes iguales en conjuntos iguales.

### Ejercicio práctico

Muestra que S = 1 entre la nota sola do y el tritono do fa♯, y halla todos los t que lo alcanzan.

> *Solución:* {0} tiene X_k = 1 para todo k, con fase 0. Por el §1, {0, 6} tiene X_k = 2 para k par y 0 para k impar. Solo cuentan k = 2, 4 y 6, todos con fase 0 en ambos lados, así que en t = 0, S = (2 + 2 + 2) / (2 + 2 + 2) = 1. En t = 6, cada coeficiente gira 180k grados, un número entero de vueltas para k par, así que S = 1 también ahí. Un conjunto de una nota y uno de dos alcanzan S = 1, en t = 0 y t = 6.

---

## 6. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`40d3374`](https://github.com/GuitarAlchemist/ga/tree/40d337479af36d987df3f06c8c638ffd35f13458), la rama `main` de GA el 2026-10-06; esta lección documenta ese código sin modificarlo, y no ha ejecutado GA ni sus pruebas. Los números de abajo vienen de una transcripción en Python, línea por línea, del código de GA nombrado.

**Los módulos y las fases vienen de la forma prima.** [`SetClass.GetFourierCoefficients`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L157) calcula la TDF de [`GetSpectralPrimeForm()`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L120-L123), la forma prima, no del conjunto a partir del cual se construyó la clase. Los módulos son los mismos para todos los conjuntos de la clase (§2), así que [`GetMagnitudeSpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L190) es correcto como propiedad de la clase. Su prueba, [`GetMagnitudeSpectrum_IsInvariantUnderTransposition`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SetClassTests.cs#L105), construye una clase a partir de do mi sol y otra a partir de re fa♯ la. Ambas se reducen a la forma prima (037), así que los dos espectros salen de los mismos 12 números, y la prueba pasaría aunque la TDF no conservara los módulos bajo transposición. [`GetPhaseSpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L213) devuelve también las fases de la forma prima, las mismas para do mayor, re mayor y do menor, aunque [su resumen](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L211) diga «Phase encodes rotational alignment on the chromatic circle». El código de alineación más reciente de GA hace la elección contraria: sus coeficientes vienen del [«ACTUAL chroma (not the prime form — phases carry the transposition, which is the point)»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L75-L76) del conjunto. En el commit `40d3374`, ningún código de GA llama a `GetPhaseSpectrum`.

**El centroide y la distancia.** [`GetSpectralCentroid`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L230) promedia k sobre los 12 bins, ponderado por |X_k|. Como |X_(12−k)| = |X_k|, los bins se reflejan alrededor de 6, y el centroide se reduce a 6(1 − n / Σ|X_k|), una medida de cuánto del módulo total queda fuera del bin 0 (ver el ejercicio de abajo). La transcripción reproduce esa fórmula en las 223 clases no vacías con un error menor que 10⁻¹³. El centroide va de 0 para el agregado a 5.5 para una nota sola, el valor que comprueba [la prueba de GA](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SetClassTests.cs#L129-L139), y [`UnifiedModeService`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Unified/UnifiedModeService.cs#L133) lo lee. [`GetSpectralDistance`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L257) suma las diferencias absolutas de módulo sobre los 12 bins, así que k = 1 a 5 cuentan dos veces y k = 0 y 6 una vez. [`SetClassSpectralIndex.GetNearestBySpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/SetClassSpectralIndex.cs#L16) ordena las clases por la misma distancia, y por el §3 cada una de las 46 clases en relación Z encuentra primero a su pareja, sola a distancia 0 salvo redondeo. El método descarta la clase de partida [por referencia](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/SetClassSpectralIndex.cs#L26): una clase tomada de `SetClass.Items` queda fuera, pero una construida de nuevo con `new SetClass(...)` es igual a su copia del índice sin ser el mismo objeto, y vuelve la primera, a distancia exactamente 0, con su pareja en segundo lugar. En la transcripción, la distancia de la pareja es un residuo de redondeo de entre 9 × 10⁻¹⁵ y 3 × 10⁻¹⁴, nunca exactamente 0. En el commit `40d3374`, ningún código de GA llama a `GetSpectralDistance` ni a `GetNearestBySpectrum`.

**Las etiquetas del embedding.** El comentario de cabecera de la partición espectral del esquema de embedding de GA afirma [«Per Lewin's Lemma: ICV = |DFT|²»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L654). Por el §3, los módulos al cuadrado son una transformada de cosenos del tamaño y del vector, no el vector: do mayor tiene <001110>, y |X_1|² a |X_6|² valen 0.268, 1, 5, 3, 3.732 y 1. La propia [nota de investigación](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L24) de GA enuncia la relación casi correctamente: omite el tamaño. Leídas para un conjunto, donde cada clase de altura cuenta una vez (no para un croma ponderado de voicing), las etiquetas del esquema para los seis módulos nombran conjuntos equivocados en cuatro de ellas. Llama a k = 2 [«Whole-tone structure»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L683), pero la escala de tonos enteros tiene |X_2| = 0. Llama a k = 3 [«Diminished structure»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L690), con una «minor-third cycle affinity», pero el acorde de séptima disminuida tiene |X_3| = 0 y es la tríada aumentada la que lo maximiza. Llama a k = 4 [«Augmented structure»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L697), lo contrario. Y llama a k = 6 [«Tritone structure»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L712), pero es la escala de tonos enteros la que maximiza |X_6|; entre los conjuntos de dos notas, el tritono comparte el mayor |X_6| con la segunda mayor y la tercera mayor, mientras que solo él alcanza el mayor |X_2| (§4). Las etiquetas de k = 2 y 6 están intercambiadas, y también las de k = 3 y 4. Las etiquetas de k = 1, «Chromatic clumping», y de k = 5, «Diatonic structure», son correctas. El [§5](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L61) de la nota de investigación repite las etiquetas equivocadas y se las atribuye a Quinn, como «Quinn's quality semantics already documented in the schema».

**La alineación de fase.** [`SpectralPhaseAlignment.Similarity`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L49) y [`SimilarityTnI`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L57) calculan los S y S_TnI del §5 a partir de los coeficientes del propio conjunto, con pesos opcionales, y fijan S en 1 o en 0 por [convención](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L111-L119) cuando el denominador se anula. La transcripción reproduce los ejemplos de la nota de investigación: 1 en t = 10 para do mayor y re mayor; 0.5714, y 1 por la inversión, para do mayor y do menor; 0.3333 y 0.6667 para 4-Z15 y 4-Z29; 0.4000 para 6-Z17 y 6-Z43. Halla S_TnI por debajo de 1 en los 23 pares en relación Z, como mucho 0.6667, como afirma la prueba [`SimilarityTnI_SeparatesAll23ZRelatedPairs`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SpectralPhaseAlignmentTests.cs#L73). La documentación promete más: [S = 1 «iff the sets are transposition-aligned»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L27). El [teorema 3](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L26-L34) de la nota de investigación demuestra un sentido, S(A, T_t A) = 1, y la prueba [`Similarity_IsOne_OnEveryTransposition_Randomized`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SpectralPhaseAlignmentTests.cs#L108) comprueba ese sentido en 1,000 conjuntos aleatorios. El recíproco falla (§5). El [corolario de separación](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L43) de la nota sostiene que los conjuntos en relación Z quedan separados porque no son equivalentes por TnI. Por el §5 eso no se sigue: do re mi y do mi sol♯ tampoco son equivalentes, y alcanzan S = 1. La conclusión vale para los 23 pares porque se pueden comprobar uno a uno: la transcripción halla S_TnI como mucho 0.6667, y la prueba de GA afirma que queda por debajo de 1 − 10⁻⁶ en cada uno.

**Lo que dice la herramienta MCP.** La herramienta [`GaHomometricDistinguish`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L198) muestra, en cuanto S ≥ 1 − 10⁻⁶, [«Same shape up to transposition — one is a transposition of the other.»](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L231-L232) Según la transcripción, Csus2 frente a C9 y Cmaj7 frente a Cdim7 llegan a esa rama. La herramienta lee los dos acordes con el analizador de `GaChordToSet`, que pide a la closure `domain.chordIntervals` los intervalos de un acorde, y las pruebas de GA fijan las cuatro lecturas: `GaChordToSet` convierte [Cdim7 en `{C, Eb, F#, A}` y C9 en `{C, D, E, G, Bb}`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L17-L18), y la closure deletrea [Csus2 `P1 M2 P5`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/ClosureChordIntervalsTests.cs#L36) y [Cmaj7 `P1 M3 P5 M7`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/ClosureChordIntervalsTests.cs#L41). Las dos clases de pruebas llaman primero a [`GaClosureBootstrap.init()`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L14).

Mientras se escribe esta lección, ninguna issue de GA cubre estos puntos. Corregir cualquiera de ellos corresponde a los responsables de GA; esta lección solo los describe.

### Ejercicio práctico

Según la transcripción, `GetSpectralCentroid` de GA da 5.044 para la tríada mayor. Muestra que el centroide vale 6(1 − n / Σ|X_k|), y compruébalo con los módulos del §4.

> *Solución:* Sobre k = 0 a 11, empareja el bin k con el bin 12 − k para k = 1 a 5: como |X_(12−k)| = |X_k|, añaden k|X_k| + (12 − k)|X_k| = 12|X_k| a la suma ponderada. El bin 6 añade 6|X_6| y el bin 0 no añade nada. El módulo total es T = n + 2(|X_1| + … + |X_5|) + |X_6|, así que la suma ponderada vale 6(T − n), y el centroide 6(T − n)/T = 6(1 − n/T). Para la tríada mayor, T = 3 + 2(0.518 + 1 + 2.236 + 1.732 + 1.932) + 1, unos 18.84, y 6(1 − 3/18.84) vale unos 5.04: el 5.044 de GA, redondeado a dos decimales.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA; la versión de GA fijada en el laboratorio pasaría primero a `40d3374`. Nada en ella es una medición. Las predicciones vienen de la transcripción del §6 y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Los módulos bajo transposición.** Para los 4,096 conjuntos, comparar `new SetClass(A).GetMagnitudeSpectrum()` con los módulos de la TDF de A calculada por el propio laboratorio, y llamar a `GetPhaseSpectrum` sobre las clases de do mi sol, re fa♯ la y do mi♭ sol. Predicción: módulos iguales para cada conjunto, salvo redondeo; tres arreglos de fases idénticos.
2. **La homometría.** Para cada una de las 46 clases en relación Z, llamar a `SetClassSpectralIndex.GetNearestBySpectrum` sobre la clase tomada de `SetClass.Items`, y luego sobre la misma clase construida con `new SetClass(...)`, y comparar `GetMagnitudeSpectrum` con el de la pareja. Predicción: la pareja sale primera, sola a distancia 0 salvo redondeo, en 46 de 46; la clase construida de nuevo vuelve ella misma la primera, y su pareja la segunda; y los espectros son iguales salvo redondeo.
3. **El centroide.** Comparar `GetSpectralCentroid` con 6(1 − n / Σ|X_k|) en las 223 clases no vacías. Predicción: iguales salvo redondeo; 5.5 para una nota sola, 3.000 para la escala de tonos enteros, 3.515 para la escala hexatónica y 4.091 para la colección diatónica.
4. **La separación.** Llamar a `SimilarityTnI` sobre las formas primas de los 23 pares en relación Z. Predicción: todos los valores por debajo de 1, el mayor 0.6667, el menor 0.3333. Esto repite, a partir de una ejecución real, lo que afirma la prueba de GA.
5. **El recíproco.** Para cada par de tipos Tn distintos, dejando aparte el conjunto vacío y el agregado, llamar a `Similarity` sobre un representante de cada uno. Predicción: S ≥ 1 − 10⁻⁶ para 270 pares del mismo tamaño y 1,230 de tamaños distintos, entre ellos do re mi y do mi sol♯ con t* = 0, 4 y 8.
6. **El veredicto de la herramienta MCP.** Llamar a `GaClosureBootstrap.init()`, como hacen las pruebas de GA, y luego llamar directamente a `GaHomometricDistinguish("Csus2", "C9")` y a `GaHomometricDistinguish("Cmaj7", "Cdim7")`. Predicción: ambos terminan con «Same shape up to transposition — one is a transposition of the other.», con las cuatro lecturas que fijan las pruebas de GA (§6).

### Ejercicio práctico

El paso 5 predice 1,500 pares con S = 1 que no son transposiciones, y sin embargo la prueba aleatoria de GA seguiría pasando. ¿Qué prueba detectaría el «iff»?

> *Solución:* Una que tome pares que no sean transposiciones uno del otro y afirme S < 1 − 10⁻⁶, la tolerancia de la prueba de GA sobre los pares en relación Z. La prueba aleatoria de GA solo toma un conjunto y una de sus transposiciones, así que comprueba el sentido que demuestra el teorema 3. Según la transcripción del §6, esa afirmación fallaría en los 1,500 pares del paso 5, 270 de ellos del mismo tamaño.

---

## 8. Errores comunes

- **Tomar los módulos por una huella de un conjunto.** Junto con el número de notas, |X_0|, solo identifican un conjunto salvo transposición, inversión y, para 23 pares de clases, relación Z. |X_1| a |X_6| por sí solos ni siquiera distinguen un conjunto de su complemento.
- **Escribir «ICV = |DFT|²».** Los módulos al cuadrado son una transformada de cosenos del tamaño y del vector; llevan la misma información, no los mismos números.
- **Nombrar un coeficiente por el ciclo equivocado.** k = 3 mide la cercanía a la tríada aumentada, un ciclo de terceras mayores; k = 4, a la séptima disminuida, un ciclo de terceras menores. El coeficiente k es máximo para los conjuntos cuyas notas quedan cerca de k puntos espaciados por igual, a 12/k semitonos uno de otro: un cluster para k = 1, dos clusters a un tritono uno del otro para k = 2, la tríada aumentada para k = 3, la séptima disminuida para k = 4, la escala pentatónica para k = 5 y la escala de tonos enteros para k = 6.
- **Probar un invariante con entradas iguales por construcción.** Dos clases de conjuntos con una misma forma prima dan un solo espectro, haga lo que haga la TDF.
- **Leer S = 1 como «misma forma».** Dice que las fases coinciden, para un t, allí donde ambos conjuntos tienen un coeficiente distinto de cero, y que existe al menos un coeficiente así (la convención de GA da también 1 cuando cada uno de los dos conjuntos es el conjunto vacío o el agregado). Ni siquiera exige el mismo número de notas.
- **Tomar un argumento por una comprobación.** Una conclusión puede ser cierta aunque el argumento que se da para ella falle; para los pares en relación Z, la prueba exhaustiva es la evidencia.
- **Leer las fases de una forma prima.** Son las mismas para todos los conjuntos de la clase, y no dicen nada de dónde está el conjunto.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **TDF de las clases de altura** | Los coeficientes X_k = Σ_(x ∈ A) e^(−2πikx/12) de un conjunto de clases de altura A, para k = 0 a 11 |
| **Módulo** | El tamaño de un coeficiente X_k, que no cambia por transposición ni por inversión |
| **Fase** | El ángulo de un coeficiente, girado −30kt grados por una transposición en t y cambiado de signo por I0 |
| **Teorema del desplazamiento** | X_k(T_t A) = e^(−2πikt/12) X_k(A) |
| **Lema de Lewin** | El módulo de X_k al cuadrado vale n + 2 Σ_d ICV_d cos(πkd/6), así que los módulos de X_0 a X_6 y el par (tamaño, vector de clases de intervalo) se determinan mutuamente |
| **Homométrico** | Que tiene el mismo tamaño y los mismos módulos de X_1 a X_6, como todo par de conjuntos en relación Z |
| **Cualidad armónica** | Lo que mide un módulo: la cercanía a los conjuntos que lo maximizan, como la escala de tonos enteros para k = 6 |
| **Similitud por alineación de fase** | S, el mejor acuerdo de las fases de dos conjuntos sobre las 12 transposiciones, ponderado por sus módulos; S_TnI prueba también la inversión |

---

## Autoevaluación

**1. ¿Por qué do mayor y do menor tienen los mismos seis módulos?**
> Do menor es I7 de do mayor: I0 sustituye cada coeficiente por su conjugado y T7 lo multiplica por un número de módulo 1, así que ningún módulo cambia.

**2. ¿Cuáles de los coeficientes X_1 a X_6 de la escala octatónica pueden ser distintos de cero, y por qué?**
> Solo X_4. T3 lleva la escala sobre sí misma, así que X_k = 0 salvo que 3k sea múltiplo de 12, lo que, entre k = 1 y 6, deja k = 4. Su módulo vale 4.

**3. Dos conjuntos tienen S = 1. ¿Qué se puede concluir? ¿Y si además tienen los mismos módulos?**
> Por sí solo, únicamente que para un t sus fases coinciden en cada k donde ambos coeficientes son distintos de cero, y que existe al menos un k así (la convención de GA da también 1 cuando cada uno de los dos conjuntos es el conjunto vacío o el agregado). Con el mismo tamaño y los mismos módulos, sus coeficientes coinciden tras esa transposición, así que uno de los conjuntos es una transposición del otro.

**4. ¿Qué devuelve primero `GetNearestBySpectrum` de GA para 4-Z15?**
> 4-Z29, a distancia 0 salvo redondeo: las dos clases son homométricas, así que sus espectros de módulos son iguales. Eso vale cuando 4-Z15 se toma de `SetClass.Items`; una clase construida de nuevo vuelve ella misma la primera.

**Criterio de aprobación:** Calcular y leer los coeficientes de un conjunto; deducir el teorema del desplazamiento, el efecto de la inversión y de M5, y el lema de Lewin; explicar la homometría y los pares en relación Z; nombrar el prototipo de cada módulo y predecir los ceros a partir de la simetría; y decir qué muestra una similitud de fase igual a 1, con y sin módulos iguales.

---

## Base de investigación

- D. Lewin, «Re: Intervallic Relations between Two Collections of Notes», *Journal of Music Theory* 3/2, 1959: la función de intervalos de dos conjuntos y su transformada de Fourier
- I. Quinn, «General Equal-Tempered Harmony», *Perspectives of New Music* 44/2, 2006 (introducción y parte I), y 45/1, 2007 (partes II y III): los módulos de Fourier como cualidades armónicas
- E. Amiot, *Music Through Fourier Space: Discrete Fourier Transform in Music Theory*, Springer, 2016: la TDF de los conjuntos de clases de altura, el lema de Lewin, la homometría y las fases
- MAT-021 de Streeling para la TDF, y MUS-020 para las clases de conjuntos, los vectores de clases de intervalo y la relación Z
- Código fuente de GA en el commit `40d337479af36d987df3f06c8c638ffd35f13458`, incluida la nota de investigación `docs/research/2026-07-04-optick-spectral-phase-alignment.md`: cada hecho de código del §6 enlaza a su línea
- Comprobaciones en Python sobre los 4,096 conjuntos: cada número de los §§1–6 sale de ellas o de la transcripción del código de GA
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición del propio GA
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
