---
module_id: mat-009-estimation-uncertainty-sampling
department: mathematics
course: Estimación, incertidumbre y muestreo reproducible
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Estimación, incertidumbre y muestreo reproducible — Lo que un número sacado de los datos puede afirmar

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Definir el sesgo, la varianza y el error cuadrático medio de un estimador, y mostrar por qué la varianza muestral divide entre n − 1
- Decir qué afirman un intervalo de confianza y un valor p, y qué no afirman
- Elegir entre la prueba t de Welch, la prueba de Mann–Whitney y la prueba de Kolmogórov–Smirnov, y calcular un valor p exacto con muestras pequeñas contando
- Estimar el error con datos nuevos mediante validación cruzada de k pliegues, y decir por qué la dispersión de las puntuaciones de los pliegues subestima su incertidumbre
- Tratar la semilla, el generador y su versión como parte de la especificación de un experimento, y decir qué garantizan las funciones de muestreo, de validación cruzada y de prueba de IX

---

## 1. Estimadores, sesgo y varianza

Un **estimador** es una regla que convierte una muestra X₁, …, Xₙ en una estimación θ̂ de una cantidad desconocida θ. La muestra es aleatoria, así que θ̂ es una variable aleatoria, y dos números dicen lo bueno que es: su **sesgo** E[θ̂] − θ y su **varianza** Var(θ̂). Juntos dan el **error cuadrático medio**, E[(θ̂ − θ)²] = sesgo² + varianza; desarrollar (θ̂ − E[θ̂] + E[θ̂] − θ)² lo muestra, ya que el término cruzado tiene esperanza 0.

Para extracciones independientes con media μ y varianza σ², la **media muestral** X̄ = (X₁ + … + Xₙ)/n es insesgada, y Var(X̄) = σ²/n, ya que las varianzas de términos independientes se suman. Su desviación típica σ/√n es el **error estándar**: reducirlo a la mitad exige cuatro veces más datos.

La varianza es más sutil. Las desviaciones Xᵢ − X̄ se miden desde X̄, que se ajusta a los mismos datos, así que en promedio son más pequeñas que las desviaciones respecto de μ: Σ(Xᵢ − X̄)² = Σ(Xᵢ − μ)² − n (X̄ − μ)², cuya esperanza es n σ² − n · σ²/n = (n − 1) σ². Dividir entre n subestima por tanto σ² en el factor (n − 1)/n, y dividir entre n − 1, la **corrección de Bessel**, elimina el sesgo. Insesgado no significa mejor: con datos normales, dividir entre n da el menor error cuadrático medio. Lo importante es decir cuál usa un número.

### Ejercicio práctico

La prueba unitaria de IX para la prueba de Welch usa las muestras (1, 2, 3, 4, 5) y (2, 3, 4, 5, 6). Calcula la varianza de cada muestra con n − 1 y con n, luego el estadístico t = (X̄₁ − X̄₂)/√(s₁²/n₁ + s₂²/n₂) y los grados de libertad de Welch–Satterthwaite (s₁²/n₁ + s₂²/n₂)²/((s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)).

> *Solución:* Ambas muestras tienen la suma de desviaciones al cuadrado 4 + 1 + 0 + 1 + 4 = 10, así que la varianza es 10/4 = 5/2 con n − 1 y 10/5 = 2 con n. Con 5/2, cada media tiene el error estándar al cuadrado (5/2)/5 = 1/2, el denominador es √(1/2 + 1/2) = 1, y t = (3 − 4)/1 = −1. Los grados de libertad son 1/((1/2)²/4 + (1/2)²/4) = 1/(1/8) = 8. Son los valores del comentario de la prueba de IX (§6).

---

## 2. Intervalos de confianza y valores p

Por el teorema central del límite, X̄ es aproximadamente normal para n grande, sea cual sea la distribución de las Xᵢ, siempre que σ sea finita. Entonces X̄ ± 1.96 σ/√n es un **intervalo de confianza del 95%** aproximado: antes de extraer los datos, la probabilidad de que este intervalo aleatorio contenga μ es 0.95. Cuando s sustituye a σ, el multiplicador sale de la distribución t de Student con n − 1 grados de libertad, y es mayor para n pequeño.

El 95% pertenece al procedimiento, no a un intervalo concreto. Una vez obtenidos los datos, un intervalo dado contiene μ o no la contiene. «μ está en [a, b] con probabilidad 0.95» es el enunciado de un intervalo de credibilidad bayesiano, leído en una distribución a posteriori como en MAT-008, y necesita una distribución a priori.

Una **prueba de hipótesis** fija una hipótesis nula H₀ y un estadístico T. El **valor p** es la probabilidad, calculada bajo H₀, de un estadístico al menos tan extremo como el observado. No es P(H₀ | datos): como con las tasas base de MAT-008, pasar de uno a otro exige la probabilidad a priori de H₀. Cuando T es continuo y H₀ es cierta, el valor p es uniforme en [0, 1], así que una prueba al nivel α = 0.05 rechaza una hipótesis nula cierta el 5% de las veces. Esa es toda su garantía, y vale para una prueba elegida de antemano. Hacer varias pruebas y comunicar el menor p, o probar análisis hasta que uno funcione, multiplica las posibilidades de un falso positivo: es el **jardín de senderos que se bifurcan**. La **corrección de Bonferroni** prueba cada una de m hipótesis al nivel α/m, lo que mantiene la probabilidad de algún rechazo erróneo en α como mucho, por la cota de la unión.

### Ejercicio práctico

Se hacen veinte pruebas independientes al nivel α = 0.05, y todas las hipótesis nulas son ciertas. ¿Cuál es la probabilidad de que al menos un valor p quede por debajo de 0.05? ¿Qué umbral usa la corrección de Bonferroni?

> *Solución:* Cada valor p es uniforme, así que cada prueba no da la alarma con probabilidad 19/20, y las veinte callan con probabilidad (19/20)^20 ≈ 0.358. Al menos un falso positivo tiene por tanto la probabilidad 1 − (19/20)^20 ≈ 0.64. Bonferroni prueba cada hipótesis al nivel 0.05/20 = 0.0025, y la probabilidad de algún rechazo erróneo es entonces como mucho 20 · 0.0025 = 0.05.

---

## 3. Pruebas de dos muestras

Tres pruebas de IX comparan dos muestras, y responden a preguntas distintas:
- **La prueba t de Welch** pregunta si las medias difieren. Su estadístico divide la diferencia de las medias entre su error estándar estimado, √(s₁²/n₁ + s₂²/n₂), sin suponer varianzas iguales, y su distribución bajo la hipótesis nula se aproxima por la t de Student con los grados de libertad de Welch–Satterthwaite. Supone que las medias muestrales son casi normales.
- **La prueba de Mann–Whitney** usa solo rangos. Su estadístico U cuenta los pares (X₁ᵢ, X₂ⱼ) con X₁ᵢ > X₂ⱼ, y un empate cuenta como un medio. Bajo la hipótesis nula de que las n₁ + n₂ observaciones son intercambiables, cada elección de los rangos que corresponden a la primera muestra es equiprobable, lo que da a U una distribución exacta por conteo. Con muestras grandes se parece a una normal de media n₁ n₂/2.
- **La prueba de Kolmogórov–Smirnov de dos muestras** toma la mayor separación vertical D entre las dos funciones de distribución empíricas. Reacciona a cualquier diferencia de distribución: de posición, de dispersión o de forma.

Una prueba **exacta** calcula el valor p a partir de la distribución nula finita. Una prueba **asintótica** usa su límite para muestras grandes, que puede estar muy lejos con muestras pequeñas. Con tres observaciones por muestra hay C(6, 3) = 20 maneras equiprobables de colocar los rangos, y el resultado más extremo en cada sentido, todos los valores de una muestra por debajo de todos los de la otra, es una sola disposición.

### Ejercicio práctico

Con tres observaciones por muestra, ¿puede una prueba de rangos exacta bilateral dar p < 0.05? ¿Cuál es su valor p para una separación completa?

> *Solución:* No. Bajo H₀, cada uno de los C(6, 3) = 20 conjuntos de rangos de la primera muestra tiene la probabilidad 1/20. La separación completa da U = 0 o U = 9, una disposición cada uno, así que su valor p bilateral es 2/20 = 0.1, y cualquier otro resultado da uno mayor. La separación completa es también la única manera de obtener D = 1 en la prueba de Kolmogórov–Smirnov, cuyo valor p exacto es entonces también 2/20 = 0.1. Una comparación de tres contra tres no puede llegar a 0.05, sean cuales sean los datos.

---

## 4. La validación cruzada

El error de un modelo sobre los datos con los que se ajustó es optimista, porque el ajuste ya se ha adaptado a su ruido. La **validación cruzada de k pliegues** estima el error con datos nuevos: reparte las n observaciones en k pliegues, ajusta el modelo k veces, cada vez con k − 1 pliegues, y lo puntúa en el pliegue apartado, de modo que cada observación se puntúa una vez, por un modelo que no la ha visto. Los pliegues **estratificados** mantienen en cada pliegue las proporciones de clases de la muestra entera.

De la construcción se siguen dos precauciones. Las k puntuaciones no son independientes, ya que dos conjuntos de entrenamiento cualesquiera comparten k − 2 pliegues, así que la desviación típica de las puntuaciones de los pliegues dividida entre √k subestima la incertidumbre de su media; Bengio y Grandvalet mostraron que ningún estimador de esa varianza es insesgado para toda distribución. Y la validación cruzada estima el error de un solo procedimiento: elegir el mejor de muchos modelos con los mismos pliegues y comunicar su puntuación la vuelve a hacer optimista, cosa que evita la validación cruzada anidada.

También importa cómo se combinan las puntuaciones de los pliegues. La media de las exactitudes de los pliegues pesa igual cada pliegue, y la exactitud de las predicciones reunidas pesa igual cada observación. Coinciden cuando los pliegues tienen el mismo tamaño.

### Ejercicio práctico

Cuatro pliegues de prueba contienen 6, 3, 3 y 3 observaciones, y un clasificador acierta 6, 1, 1 y 1 de ellas. Compara la media de las exactitudes de los pliegues con la exactitud global.

> *Solución:* Las exactitudes de los pliegues son 1, 1/3, 1/3 y 1/3, con media (1 + 1)/4 = 1/2. La exactitud global es (6 + 1 + 1 + 1)/15 = 9/15 = 3/5. El pliegue grande cuenta como un pliegue de cuatro en el primer número y como 6 observaciones de 15 en el segundo; el §6 muestra cómo IX puede producir esos pliegues.

---

## 5. Remuestreo y semilla

El **bootstrap** estima la distribución muestral de un estadístico a partir de la propia muestra: extraer n observaciones con reemplazo, recalcular el estadístico, repetir muchas veces, y leer la dispersión o los cuantiles de los resultados. Una remuestra omite una observación dada con la probabilidad (1 − 1/n)^n, que tiende a 1/e ≈ 0.368, así que contiene alrededor del 63% de las observaciones distintas. El **intervalo de percentiles**, entre los cuantiles del 2.5% y del 97.5% de los estadísticos bootstrap, es el intervalo de confianza bootstrap más sencillo. No necesita ninguna fórmula del error estándar, pero hereda el sesgo del estadístico y puede ser pobre para n pequeño.

Remuestrear, barajar pliegues e inicializar modelos consumen números aleatorios, así que sus resultados dependen del generador. Un **generador pseudoaleatorio** es una función determinista: el mismo algoritmo, arrancado desde la misma **semilla**, produce la misma secuencia. La semilla sola no especifica esa secuencia. Lo que extrae una ejecución lo especifican la semilla, el algoritmo, la versión de la biblioteca que lo implementa y el orden en que el programa consume los números; cambia cualquiera de ellos y las extracciones pueden cambiar. Un resultado que vale para una semilla es un resultado sobre esa semilla. Comunicarlo tras probar varias semillas es otro sendero del jardín que se bifurca, así que una ejecución debe fijar su semilla antes de ver los datos, o comunicar la dispersión sobre muchas semillas.

### Ejercicio práctico

Para una muestra de n = 10 observaciones, ¿cuál es la probabilidad de que una observación dada falte en una remuestra bootstrap, y cuántas observaciones distintas contiene una remuestra en promedio?

> *Solución:* Cada una de las 10 extracciones la omite con la probabilidad 9/10, así que falta con la probabilidad (9/10)^10 ≈ 0.349, algo menos que 1/e ≈ 0.368. Por la linealidad de la esperanza, el número de observaciones distintas es en promedio 10 · (1 − (9/10)^10) ≈ 6.51.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**El muestreo** (`crates/ix-math/src/random.rs`). [`seeded_rng`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L10) construye un `StdRng` a partir de una semilla `u64`, y [`shuffle_indices`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L35) y [`sample_indices`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L43) reciben un generador así como argumento. Las cuatro funciones definidas entre ellas no reciben ninguno. Las líneas 9 a 17, literales, muestran el constructor con semilla y la primera de esas funciones; las otras tres tienen la misma forma:

```rust
/// Create a seeded RNG for reproducibility.
pub fn seeded_rng(seed: u64) -> StdRng {
    StdRng::seed_from_u64(seed)
}

/// Random matrix from uniform distribution [low, high).
pub fn uniform_matrix(rows: usize, cols: usize, low: f64, high: f64) -> Array2<f64> {
    Array2::random((rows, cols), Uniform::new(low, high).unwrap())
}
```

- **Las funciones aleatorias públicas no se pueden reproducir.** `uniform_matrix`, [`normal_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L20), `uniform_vector` y `normal_vector` llaman a [`random`](https://docs.rs/ndarray-rand/0.16.0/ndarray_rand/trait.RandomExt.html) de `ndarray-rand`, que en cada llamada inicializa un generador nuevo a partir del generador local al hilo de `rand`, inicializado a su vez por el sistema operativo. Ningún argumento puede hacer coincidir dos llamadas, y las pruebas de `random.rs` solo comprueban sus dimensiones. `Uniform::new` falla cuando low ≥ high, así que el [`unwrap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L16) entra en pánico con un intervalo vacío, como `uniform_matrix(2, 2, 1.0, 1.0)`.
- **Una semilla todavía no es una especificación portable.** La documentación de `rand` 0.9 describe [`StdRng`](https://docs.rs/rand/0.9.2/rand/rngs/struct.StdRng.html) como no portable: «any future library version may replace the algorithm and results may be platform-dependent». Remite a [`rand_chacha`](https://docs.rs/rand_chacha/0.9.0/rand_chacha/), cuyos generadores llama portables. El espacio de trabajo de IX pide [`rand = "0.9"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L102), un rango de versiones, y su [`.gitignore`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/.gitignore#L3) excluye `Cargo.lock`, el archivo que registraría la versión usada por una compilación. Así, `seeded_rng(42)` repite su secuencia dentro de una misma compilación, pero fijar IX en `e35138b9` no basta por sí solo para fijar esa secuencia. El espacio de trabajo ya depende de [`rand_chacha`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L103).
- **`sample_indices` acorta su respuesta sin avisar.** [Extrae `k.min(n)` índices](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L45), así que pedir 10 índices de 5 devuelve 5, sin error.
- **La validación cruzada tiene semilla, con un valor por defecto oculto.** [`KFold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L64) y `StratifiedKFold` barajan por defecto con la [semilla 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L76), y [`cross_val_score`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L245) pasa su argumento `seed` a un [`StratifiedKFold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L312). Esa partición [reparte cada clase por turnos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L193) empezando cada vez por el primer pliegue, así que tres clases de 5 observaciones con k = 4 dan pliegues de prueba de 6, 3, 3 y 3, el caso del ejercicio del §4. Con las etiquetas (0, 0, 1, 1) y k = 3, el tercer pliegue queda vacío aunque n ≥ k, y si el modelo acepta una entrada vacía, [`accuracy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/metrics.rs#L98) divide entonces 0 entre 0, lo que da NaN en binary64.
- **Ningún intervalo de confianza.** Los crates de IX no tienen ninguna función de bootstrap ni de intervalo de confianza. El único remuestreo está dentro del bosque aleatorio, que [extrae n índices con reemplazo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-ensemble/src/random_forest.rs#L66) para cada árbol a partir de un generador con semilla, y no comunica el error fuera de bolsa que permitirían las observaciones que quedan fuera de cada remuestra, alrededor del 37%.

**Las pruebas de dos muestras** (`crates/ix-math/src/inference.rs`). El archivo dice seguir las convenciones de SciPy y fija sus pruebas en valores de SciPy. [`welch_t_test`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L340) usa la [varianza con n − 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L349) del §1, y [`welch_t_test_matches_scipy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L624) comprueba el t = −1 del ejercicio del §1, y un valor p a menos de 2 · 10^-3 del 0.3466 de SciPy. Las dos pruebas de rangos solo calculan valores p asintóticos. El valor p de Mann–Whitney pasa por esta función de cola, literal en las líneas 386 a 389:

```rust
/// Upper tail of the standard normal: `P(Z > z)`.
fn normal_sf(z: f64) -> f64 {
    0.5 * (1.0 - erf(z / std::f64::consts::SQRT_2))
}
```

- **Los valores p pequeños se vuelven exactamente 0.** [`erf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L373) es la aproximación 7.1.26 de Abramowitz y Stegun, a menos de 1.5 · 10^-7 del valor verdadero. Para z grande, la erf calculada se redondea a 1 y 1 − erf es exactamente 0: una transcripción de estas líneas predice que [`mann_whitney_u`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L283) devuelve p = 0 en cuanto z supera unos 8.38, donde la verdadera cola normal vale todavía unos 5 · 10^-17. Para 50 observaciones contra 50, la separación completa da z ≈ 8.61 y p = 0, mientras que su valor p exacto es 2/C(100, 50), minúsculo pero positivo. Un valor p de 0 devuelto por esta función significa «por debajo de unos 10^-16», no «imposible»; calcular directamente la función de error complementaria evita la cancelación.
- **El valor p de Kolmogórov–Smirnov no es el de SciPy.** El [comentario de documentación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L242) cita `method='asymp'` de SciPy, pero el código [aplica la corrección de Stephens](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L273) dentro de la serie de Kolmogórov, como hace Numerical Recipes. En SciPy 1.17.1, esa opción evalúa en cambio la distribución de D para un tamaño de muestra N = n₁ n₂/(n₁ + n₂), redondeado, así que los dos valores p difieren. Con muestras diminutas, el de IX puede ser demasiado pequeño: para (0, 1, 2) contra (10, 11, 12), las muestras de la [prueba de IX](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L590), la fórmula da unos 0.033, mientras que el valor p exacto es 0.1 (§3). La prueba solo [afirma p < 0.2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L592), cosa que cumplen ambos valores.

**Una prueba que no puede fallar.** [`test_hurst_random_walk`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L208) extrae sus pasos ±1 de [`rand::rng()`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L211), un generador inicializado por el sistema operativo, así que cada ejecución prueba datos distintos. Su comentario espera H ≈ 0.5 para un paseo aleatorio. Pero [`hurst_exponent`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L97) [acumula él mismo las desviaciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L116), así que espera los pasos, y la prueba le pasa el paseo, su suma acumulada. Para una serie integrada así, el rango reescalado crece como el propio tamaño de la ventana, lo que predice H cerca de 1, no de 0.5. La aserción [0.1 < H < 1.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L221) acepta ambos valores, así que la prueba no puede detectar la confusión. Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Para (0, 1, 2) contra (10, 11, 12), D = 1 y N = 3 · 3/6 = 3/2. Calcula el valor p de la fórmula de IX, 2 e^(−2t²) con t = (√N + 0.12 + 0.11/√N) · D, ya que los términos siguientes de la serie son aquí despreciables, y compáralo con el valor p exacto del §3.

> *Solución:* √(3/2) ≈ 1.225, así que t ≈ 1.225 + 0.12 + 0.090 ≈ 1.435, 2t² ≈ 4.12, y 2 e^(−4.12) ≈ 0.033. El término siguiente, 2 e^(−8t²), vale unos 10^-7. El valor p exacto es 2/20 = 0.1: la fórmula declara significación al 0.05 para una comparación que, como mostró el §3, nunca puede alcanzarla. Esto es aritmética sobre el código, no una ejecución; el §7 lo comprueba.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **Misma semilla, misma secuencia.** Para s = 0, …, 999, llamar dos veces a `shuffle_indices(10, &mut seeded_rng(s))`. Predicción: las dos permutaciones son idénticas para cada s. Anotar la versión de `rand` leída en el `Cargo.lock` de la compilación junto a los resultados.
2. **Semillas distintas, estadístico estable.** Para las mismas 1000 semillas, contar los puntos fijos de cada permutación. Predicción: los conteos varían con la semilla, y su media está a menos de 0.1 de 1, el número esperado de puntos fijos de una permutación aleatoria uniforme.
3. **Las funciones sin semilla.** Llamar dos veces a `uniform_vector(5, 0.0, 1.0)`. Predicción: los dos vectores difieren. Luego llamar a `uniform_matrix(2, 2, 1.0, 1.0)`. Predicción: un pánico del `unwrap` de `Uniform::new`.
4. **Muestreo truncado.** Llamar a `sample_indices(5, 10, &mut seeded_rng(0))`. Predicción: 5 índices distintos y ningún error.
5. **Colas de las pruebas.** Llamar a `mann_whitney_u` con 0, …, 49 contra 100, …, 149, y luego con 0, …, 39 contra 100, …, 139. Predicción: U₁ = 0 las dos veces, con p = 0 exactamente para 50 contra 50 y un p positivo del orden de 10^-14 para 40 contra 40. Llamar a `ks_two_sample` con (0, 1, 2) contra (10, 11, 12). Predicción: D = 1 y p ≈ 0.033.
6. **Pliegues.** Partir las etiquetas (0, 0, 1, 1) con `StratifiedKFold::new(3)`, y cinco etiquetas de cada una de tres clases con `StratifiedKFold::new(4)`. Predicción: pliegues de prueba de tamaños 2, 2 y 0, y luego 6, 3, 3 y 3. Después ejecutar `cross_val_score` con `KNN::new(1)` sobre cuatro puntos con las primeras etiquetas, e informar de si la tercera puntuación es NaN o si la llamada entra en pánico.
7. **La prueba de Hurst.** Construir los paseos de `test_hurst_random_walk` a partir de 100 generadores con semilla en lugar de `rand::rng()`, y aplicar `hurst_exponent` a los paseos y a sus pasos. Predicción: H cerca de 1 para los paseos y cerca de 0.5 para los pasos, todos dentro de (0.1, 1.5).

### Ejercicio práctico

El paso 2 predice una media a menos de 0.1 de 1 sobre 1000 semillas. ¿De dónde sale ese margen?

> *Solución:* Sea Iᵢ el indicador de que la posición i es fija. Cada Iᵢ tiene la esperanza 1/10, así que el número de puntos fijos tiene la esperanza 10 · 1/10 = 1. Cada Iᵢ tiene la varianza (1/10)(9/10), y para i ≠ j, P(ambos fijos) = 1/90, así que la covarianza es 1/90 − 1/100 = 1/900. La varianza es 10 · 9/100 + 90 · 1/900 = 9/10 + 1/10 = 1. La media sobre 1000 semillas independientes tiene la desviación típica 1/√1000 ≈ 0.032, y tres de ellas, unos 0.095, caben dentro de 0.1. Esto supone que las semillas dan permutaciones uniformes independientes, que es lo que un buen generador aproxima; la semilla hace la ejecución repetible, no más aleatoria.

---

## 8. Errores comunes

- **Comunicar una estimación sin su incertidumbre.** Una media sin error estándar ni intervalo no se puede comparar con nada.
- **Leer un valor p como la probabilidad de que la hipótesis nula sea cierta.** Se calcula suponiendo esa hipótesis.
- **Leer «no significativo» como «sin efecto».** Una muestra pequeña puede carecer de potencia para detectar nada: tres contra tres nunca llega a 0.05.
- **Elegir la prueba después de ver los datos.** Fijar antes la prueba, la métrica y el umbral, o corregir por el número de pruebas.
- **Fiarse de valores p asintóticos con muestras diminutas.** Contar la distribución nula exacta cuando las muestras son pequeñas.
- **Tratar las puntuaciones de los pliegues como independientes.** Su dispersión subestima la incertidumbre de la media de validación cruzada.
- **Tratar una semilla como toda la especificación.** Anotar también el generador, la versión de la biblioteca y el orden de las extracciones, y comunicar los resultados sobre varias semillas.
- **Escribir una prueba que su alternativa también supera.** Una cota lo bastante amplia para aceptar a la vez H ≈ 0.5 y H ≈ 1 no comprueba ninguno de los dos.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Estimador** | Una regla que convierte una muestra en una estimación de una cantidad desconocida |
| **Sesgo** | E[θ̂] − θ, el error medio de un estimador |
| **Error estándar** | La desviación típica de un estimador, σ/√n para la media muestral |
| **Corrección de Bessel** | Dividir la suma de desviaciones al cuadrado entre n − 1, lo que hace insesgado el estimador de la varianza |
| **Intervalo de confianza** | Un intervalo aleatorio que contiene el valor verdadero con una probabilidad dada, antes de extraer los datos |
| **Valor p** | La probabilidad bajo la hipótesis nula de un estadístico al menos tan extremo como el observado |
| **Prueba exacta** | Una prueba cuyo valor p sale de la distribución nula finita, a menudo por conteo |
| **Validación cruzada** | Estimar el error con datos nuevos ajustando con una parte de los datos y puntuando con el resto, por turnos |
| **Bootstrap** | Estimar una distribución muestral remuestreando los datos con reemplazo |
| **Semilla** | El estado inicial de un generador pseudoaleatorio; con el algoritmo y su versión, fija la secuencia |
| **Jardín de senderos que se bifurcan** | La inflación de falsos positivos cuando el análisis se elige después de ver los datos |

---

## Autoevaluación

**1. ¿Por qué dividir entre n subestima la varianza?**
> Las desviaciones se miden desde X̄, que se ajusta a los mismos datos y está más cerca de ellos que μ: E[Σ(Xᵢ − X̄)²] = (n − 1) σ², así que dividir entre n da (n − 1) σ²/n en promedio.

**2. Un estudio comunica p = 0.03. ¿Por qué la probabilidad de que la hipótesis nula sea cierta no es 0.03?**
> El valor p es la probabilidad de datos al menos tan extremos dada H₀, no la probabilidad de H₀ dados los datos. Pasar de uno a otro exige la probabilidad a priori de H₀ y el comportamiento de los datos bajo la alternativa, como con el teorema de Bayes de MAT-008.

**3. Dos ejecuciones del mismo programa con la misma semilla dan resultados distintos. Nombra tres causas posibles.**
> Otra versión de la biblioteca del generador, otro algoritmo bajo el mismo nombre, otro orden o número de extracciones, o un azar que no procede en absoluto del generador con semilla, como `uniform_matrix` de IX.

**4. La prueba `test_hurst_random_walk` de IX pasa. ¿Qué te dice sobre `hurst_exponent`?**
> Poco: la cota 0.1 < H < 1.5 acepta a la vez el valor 0.5 que espera su comentario y el valor cercano a 1 que debería dar el paseo que construye, y sus datos cambian en cada ejecución.

**Criterio de aprobación:** Calcular el sesgo y el error estándar de estimadores sencillos, interpretar un intervalo de confianza y un valor p, contar una distribución nula exacta con muestras pequeñas, explicar qué estima la validación cruzada de k pliegues y qué se le escapa a la dispersión de sus pliegues, decir qué fija y qué no fija una semilla, y seguir lo que garantizan el muestreo, la validación cruzada y las pruebas de dos muestras de IX.

---

## Base de investigación

- L. Wasserman, *All of Statistics*, Springer, 2004: estimadores, intervalos de confianza, pruebas y bootstrap
- B. Efron y R. J. Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall, 1993: el bootstrap y los intervalos de percentiles
- B. L. Welch, «The generalization of 'Student's' problem when several different population variances are involved», *Biometrika* 34, 1947: la prueba de Welch
- H. B. Mann y D. R. Whitney, «On a test of whether one of two random variables is stochastically larger than the other», *Annals of Mathematical Statistics* 18, 1947: la prueba U
- N. Smirnov, «Table for estimating the goodness of fit of empirical distributions», *Annals of Mathematical Statistics* 19, 1948: el estadístico de dos muestras
- M. A. Stephens, «Use of the Kolmogorov–Smirnov, Cramér–von Mises and related statistics without extensive tables», *Journal of the Royal Statistical Society B* 32, 1970: la corrección para muestras pequeñas
- M. Abramowitz e I. A. Stegun, *Handbook of Mathematical Functions*, National Bureau of Standards, 1964, fórmula 7.1.26: la aproximación de erf
- W. H. Press, S. A. Teukolsky, W. T. Vetterling y B. P. Flannery, *Numerical Recipes*, 3.ª ed., Cambridge University Press, 2007: la rutina de Kolmogórov–Smirnov que sigue IX
- Y. Bengio e Y. Grandvalet, «No unbiased estimator of the variance of K-fold cross-validation», *Journal of Machine Learning Research* 5, 2004: por qué la dispersión de las puntuaciones de los pliegues subestima la incertidumbre
- A. Gelman y E. Loken, «The garden of forking paths», 2013: el análisis que depende de los datos
- A. A. Anis y E. H. Lloyd, «The expected value of the adjusted rescaled Hurst range of independent normal summands», *Biometrika* 63, 1976: el comportamiento del rango reescalado con muestras pequeñas
- La documentación de `rand` 0.9 y de `rand_chacha` 0.9, citada en el §6: la portabilidad de los generadores con semilla
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
