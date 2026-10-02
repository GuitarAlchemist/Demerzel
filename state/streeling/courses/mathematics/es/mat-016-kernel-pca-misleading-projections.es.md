---
module_id: mat-016-kernel-pca-misleading-projections
department: mathematics
course: ACP con núcleo y proyecciones engañosas
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-013-distances-kernels-psd, mat-014-pca-variance-preservation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# ACP con núcleo y proyecciones engañosas — Componentes principales en el espacio de características, y estructuras que el núcleo inventa

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Deducir el ACP con núcleo de la forma del ACP mediante la matriz de Gram, y decir qué debe cumplir el núcleo
- Centrar una matriz de núcleo en el espacio de características, y explicar por qué existen como mucho n − 1 componentes
- Normalizar los vectores propios, proyectar los puntos de entrenamiento y puntos nuevos, y comprobar que las dos proyecciones coinciden
- Describir cómo el ancho de banda RBF lleva el ACP con núcleo del ACP lineal a una proyección que no dice nada de los datos
- Distinguir una separación fabricada por la proyección de una estructura de los datos, con un barrido del ancho de banda y un control negativo
- Rastrear lo que garantiza `KernelPca` de IX, y dónde su prueba, su documentación y un umbral numérico prometen más de lo que el código entrega

---

## 1. Del ACP al ACP con núcleo

El MAT-014 calcula el ACP a partir de la matriz de covarianza p × p. Las mismas componentes se obtienen de la matriz n × n de productos escalares. Si X_c es la matriz de datos centrada, con la SVD X_c = UΣVᵀ del MAT-006, la matriz de Gram X_cX_cᵀ = UΣ²Uᵀ tiene los valores propios λᵢ = σᵢ² y los vectores propios unitarios vᵢ, las columnas de U, y las puntuaciones son X_cV_k = U_kΣ_k: la puntuación del punto j en la componente i es √λᵢ (vᵢ)ⱼ. Esta forma usa los datos solo a través de los productos escalares xᵢ · xⱼ.

El **ACP con núcleo** (Schölkopf, Smola y Müller 1998) sustituye cada producto escalar por un valor de núcleo k(xᵢ, xⱼ) = φ(xᵢ) · φ(xⱼ), en el sentido del MAT-013: es el ACP de las imágenes φ(xᵢ) en el espacio de características, calculado sin formar nunca φ. El espacio de características del núcleo polinómico (γ x · y + c)^d tiene una coordenada por monomio de grado como mucho d, o exactamente d cuando c = 0; el del núcleo RBF es de dimensión infinita, así que el ACP allí solo es posible a través de la matriz de núcleo K. El núcleo debe ser semidefinido positivo: si no, no existe ningún φ, y K puede tener valores propios negativos, que no son varianzas. Una componente del ACP con núcleo es una dirección del espacio de características. Sus puntuaciones son una función no lineal de la entrada, mientras que el método mismo sigue siendo lineal, en el espacio de características.

### Ejercicio práctico

Para el núcleo k(x, y) = (x · y)² en ℝ², encontrar una aplicación de características φ, y calcular k((1, 2), (3, 1)) de las dos maneras.

> *Solución:* (x · y)² = (x₁y₁ + x₂y₂)² = x₁²y₁² + 2x₁x₂y₁y₂ + x₂²y₂², así que φ(x) = (x₁², √2 x₁x₂, x₂²). Directamente, (1 · 3 + 2 · 1)² = 5² = 25. A través de φ, φ(1, 2) = (1, 2√2, 4) y φ(3, 1) = (9, 3√2, 1), cuyo producto escalar es 9 + 12 + 4 = 25. El ACP de las φ(xᵢ) busca direcciones entre los tres monomios cuadráticos: una elipse centrada en el origen de la entrada se convierte en un plano del espacio de características.

---

## 2. Centrar en el espacio de características

El ACP necesita datos centrados, y la media φ̄ de las imágenes no se puede formar. No hace falta: los productos escalares de las imágenes centradas son (φ(xᵢ) − φ̄) · (φ(xⱼ) − φ̄) = kᵢⱼ − rᵢ − rⱼ + g, donde rᵢ es la media de la fila i de K y g la media de todas sus entradas. En forma matricial, K_c = JKJ con la matriz de centrado J = I − (1/n) 11ᵀ: el doble centrado del MDS clásico, aplicado a K en lugar de −½ D⁽²⁾. Para el núcleo RBF el vínculo es exacto, ya que ‖φ(x) − φ(y)‖² = k(x, x) + k(y, y) − 2k(x, y) = 2 − 2k(x, y): el ACP con núcleo RBF es el MDS clásico sobre las distancias del espacio de características √(2 − 2kᵢⱼ), un vínculo que estudia Williams (2002).

Las imágenes centradas suman 0, así que K_c 1 = 0: el vector de unos es siempre vector propio con valor propio 0, y como mucho n − 1 valores propios son no nulos. Por grande que sea el espacio de características, n puntos centrados generan como mucho n − 1 de sus dimensiones, así que el ACP con núcleo ofrece como mucho n − 1 componentes, cada una combinación de las imágenes de entrenamiento.

### Ejercicio práctico

Aplicar el ACP con núcleo con el núcleo lineal a los puntos 0, 1 y 3 de la recta real. Calcular K, K_c y las puntuaciones.

> *Solución:* K = xxᵀ = [[0, 0, 0], [0, 1, 3], [0, 3, 9]], con medias de fila 0, 4/3 y 4 y media global 16/9. Entonces (K_c)₁₁ = 0 − 0 − 0 + 16/9 = 16/9, y del mismo modo K_c = x̃x̃ᵀ con x̃ = (−4/3, −1/3, 5/3), los puntos centrados. K_c tiene rango 1, el único valor propio no nulo ‖x̃‖² = 14/3 y el vector propio unitario x̃/‖x̃‖, así que las puntuaciones √(14/3) · x̃/‖x̃‖ = x̃ son los puntos centrados, salvo el signo: con el núcleo lineal, el ACP con núcleo es el ACP.

---

## 3. Normalización y proyección fuera de la muestra

Sea v un vector propio unitario de K_c con valor propio λ > 0. La dirección del espacio de características w = Σⱼ αⱼ (φ(xⱼ) − φ̄) con α = v/√λ tiene longitud 1, ya que ‖w‖² = αᵀK_cα = vᵀK_cv/λ = 1; esta es la normalización de Schölkopf, Smola y Müller. La puntuación del punto de entrenamiento i es el producto escalar de su imagen centrada con w, (K_cα)ᵢ = λvᵢ/√λ = √λ vᵢ, la fórmula del §1.

Un punto nuevo x se proyecta del mismo modo, con las estadísticas de entrenamiento. Su vector de núcleo centrado tiene las entradas k̃ⱼ(x) = k(x, xⱼ) − m(x) − rⱼ + g, donde m(x) es la media de los k(x, xⱼ) sobre los puntos de entrenamiento, y su puntuación es Σⱼ αⱼ k̃ⱼ(x). Para un punto de entrenamiento, k̃(xᵢ) es la fila i de K_c y la puntuación vuelve a ser √λ vᵢ, así que las dos vías deben coincidir en el conjunto de entrenamiento: es la primera comprobación que hay que hacer en cualquier implementación. Cuando λ = 0, v está en el núcleo de K_c, no se puede construir con él ninguna dirección unitaria w, y la salida correcta es una columna de ceros, o ninguna columna.

Volver de una puntuación al espacio de entrada es más difícil, porque un punto del espacio de características no tiene por qué ser la imagen de ninguna entrada. Este **problema de la preimagen** solo se resuelve de forma aproximada: por iteración para el núcleo RBF (Mika et al. 1999), o a partir de las distancias (Kwok y Tsang 2004).

### Ejercicio práctico

Continuar el ejercicio del §2: proyectar el punto nuevo x = 2 con el núcleo lineal, a través de k̃(x) y α.

> *Solución:* k(2, xⱼ) = (0, 2, 6), con media m = 8/3. Con las medias de fila 0, 4/3 y 4 y g = 16/9, k̃ = (0 − 8/3 − 0 + 16/9, 2 − 8/3 − 4/3 + 16/9, 6 − 8/3 − 4 + 16/9) = (−8/9, −2/9, 10/9). Con v = x̃/‖x̃‖ y λ = 14/3, α = x̃/λ = (−2/7, −1/14, 5/14), y la puntuación es (−8/9)(−2/7) + (−2/9)(−1/14) + (10/9)(5/14) = 16/63 + 1/63 + 25/63 = 2/3: el punto 2 menos la media de entrenamiento 4/3, como daría el ACP.

---

## 4. El ancho de banda: del ACP lineal a la proyección de nada

El MAT-013 siguió la matriz de Gram RBF K al variar γ. El centrado cambia los dos límites. Para γ pequeño, exp(−γd²) = 1 − γd² + O(γ²d⁴); el centrado elimina la constante, y K_c ≈ −γ J D⁽²⁾ J = 2γB, donde B es la matriz doblemente centrada del MDS clásico, la matriz de Gram de las entradas centradas. El ACP con núcleo se acerca entonces al ACP lineal, con valores propios de unas 2γ veces los de B y puntuaciones de unas √(2γ) veces las del ACP. Sobre los puntos 0, 1 y 3 con γ = 0.001, el mayor valor propio es de unos 9.29 · 10^-3, frente a 2γ · 14/3 ≈ 9.33 · 10^-3, y las puntuaciones divididas por √(2γ) son −1.330, −0.334 y 1.663, frente a −4/3, −1/3 y 5/3.

Para γ grande, cada kᵢⱼ fuera de la diagonal tiende a 0, K tiende a I y K_c a J, cuyos valores propios son 1, n − 1 veces, y 0. Todo vector unitario ortogonal a 1 es entonces vector propio, así que las componentes son la base que devuelva el resolvedor, sea cual sea. En el espacio de características, las imágenes de puntos distintos se vuelven ortogonales, todas a distancia √2 unas de otras: un símplex regular, que se ve igual desde todas las direcciones.

Entre estos límites, lo que muestra el ACP con núcleo depende de γ, y ningún valor es correcto en general. El MAT-013 menciona un valor inicial habitual, σ igual a la distancia mediana entre los puntos, con γ = 1/(2σ²): un punto de partida, no una garantía de que la estructura buscada vaya a aparecer.

### Ejercicio práctico

Para n puntos distintos y γ → ∞, ¿qué devuelve el ACP con núcleo con k componentes, y qué dice de los datos?

> *Solución:* K_c tiende a J, así que los n − 1 valores propios no nulos tienden todos a 1, y cualquier base ortonormal de los vectores ortogonales a 1 es un conjunto válido de vectores propios. Las k columnas devueltas son los vectores que produzca el resolvedor, sean cuales sean, multiplicados por √1 = 1: una proyección de un símplex regular, que no dice nada de los datos. Cualquier patrón en un gráfico así, grupos incluidos, viene del resolvedor.

---

## 5. Proyecciones engañosas: dos anillos y un control negativo

Dos anillos concéntricos son el escaparate clásico del ACP con núcleo. Ninguna proyección lineal los separa (véase el ejercicio), pero el núcleo RBF puede, a través de una componente concreta. Tomemos m puntos en cada anillo, en los mismos ángulos. La configuración no cambia con las rotaciones y reflexiones de un m-ágono regular, y K_c conmuta con las permutaciones de los puntos que estas inducen. Los vectores que fijan esas permutaciones son los constantes en cada anillo; forman un plano que contiene 1 y que K_c envía en sí mismo, así que la otra dirección de ese plano, s = (1, …, 1, −1, …, −1)/√(2m), es un vector propio exacto, con el valor propio λ_rad = sᵀKs. Sus puntuaciones son +√(λ_rad/(2m)) en un anillo y −√(λ_rad/(2m)) en el otro: cada anillo se reduce a un solo valor, una separación perfecta. Cualquier otro vector propio puede elegirse ortogonal a ese plano, así que sus puntuaciones tienen media 0 en cada anillo. Sin s, toda función afín de las puntuaciones conservadas tiene la misma media en los dos anillos, así que no puede ser positiva en un anillo y negativa en el otro: que las componentes conservadas separen los anillos por una recta o un hiperplano depende solo de que s esté entre ellas, es decir, del rango de λ_rad, y ese rango depende de γ y de la geometría. Los anillos pueden seguir difiriendo en el radio en un gráfico así, como se ve abajo, pero solo una regla no lineal puede aprovecharlo.

Los datos de prueba de IX tienen cuatro puntos en cada uno de los anillos de radios 1 y 2. Con γ = 0.5, los valores propios de K_c son de unos 1.531 dos veces, 1.216, 0.672 = λ_rad, 0.333 dos veces, 0.148 y 0: la componente radial es la cuarta, y es la cuarta para cada γ del barrido del §7, de 0.001 a 10. Las dos primeras componentes forman un par empatado que registra el ángulo de cada punto: cada punto interior cae en el mismo ángulo que su vecino exterior, a un radio de unos 0.583 frente a 0.653 para el anillo exterior. La razón 2 entre los radios se reduce a unos 1.12, y ninguna recta separa los dos cuadrados.

Con el radio interior cambiado a 0.3 y el exterior a 1, la componente radial es la cuarta hasta γ = 0.5, la tercera con γ = 1, y la primera por encima de γ ≈ 1.597. Su ventaja sobre el valor propio siguiente llega a unos 0.357 con γ = 5 y cae a unos 1.2 · 10^-4 con γ = 50. Los mismos datos no muestran, pues, ninguna separación con γ = 1 y una perfecta con γ = 5. Una separación que se mantiene en una ventana de γ es una propiedad de los datos y de γ juntos, y comunicarla exige dar la ventana.

Un **control negativo** es un conjunto de datos sin la estructura buscada. Tomemos los ocho puntos equiespaciados 0, 1, …, 7 de una recta: no tienen ningún grupo. Con γ = 0.001 la primera componente es prácticamente la recta, y su mayor hueco entre puntuaciones consecutivas es 0.145 del rango, frente a 1/7 ≈ 0.143 para un espaciado exactamente regular. Con γ = 0.1 y con cada γ mayor del barrido, la primera componente deja de ser monótona: los dos extremos se pliegan mientras el centro se estira, y para γ = 2, 5 y 10 el hueco entre los puntos 3 y 4 llega a 0.347 del rango, más del doble del hueco regular. Un histograma de esa componente muestra dos grupos de cuatro puntos. Es el efecto **herradura** de los núcleos locales (Diaconis, Goel y Holmes 2008): el núcleo solo ve a los vecinos cercanos, y los primeros vectores propios de tales matrices curvan una recta en arco, a menudo con los extremos vueltos hacia dentro. Todo criterio que declare separados los anillos debería probarse sobre un control así, y debe fallar en él.

### Ejercicio práctico

¿Por qué ninguna proyección lineal puede separar dos anillos concéntricos centrados en el origen?

> *Solución:* Una proyección lineal lleva x a u · x para algún vector unitario u; la primera componente del ACP es una aplicación de ese tipo. Un anillo completo de radio r se proyecta sobre todo el intervalo [−r, r], así que el intervalo del anillo interior está dentro del del anillo exterior, y todo umbral estrictamente entre −r₁ y r₁ tiene puntos de los dos anillos a cada lado. Para los cuatro puntos por anillo de IX, cada punto exterior es el doble del punto interior del mismo ángulo, así que cada puntuación exterior es el doble de una puntuación interior; las puntuaciones interiores toman los dos signos, así que las exteriores las rebasan por ambos extremos, y ningún umbral separa los anillos. Conservar más componentes lineales no ayuda: una aplicación lineal lleva los dos anillos a dos elipses anidadas, una copia reducida de la otra.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de `fit_transform`, `transform`, `compute_kernel` y `symmetric_eigen` a Python, cuyos flotantes son binary64 IEEE como el `f64` de Rust: son predicciones, y el §7 propone comprobarlas.

**ACP con núcleo** (`crates/ix-unsupervised`). [`fit_transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L96) construye K, la centra con la [fórmula del §2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L129), entrega K_c a [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L135), el método de Jacobi del MAT-005, y conserva los `n_components` primeros pares. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L169) centra los vectores de núcleo de los puntos nuevos con las [estadísticas de entrenamiento](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L205) y [los multiplica por los alphas almacenados](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L210). El módulo es solo una biblioteca: [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/lib.rs#L7) lo exporta y ningún otro archivo Rust del repositorio lo menciona, así que ninguna herramienta MCP, función DuckDB ni etapa de pipeline ofrece el ACP con núcleo. La normalización y la proyección de entrenamiento dicen:

```rust
        // Take top-k alphas and lambdas.
        let mut alphas = Array2::<f64>::zeros((n, self.n_components));
        let mut lambdas = Array1::<f64>::zeros(self.n_components);
        for r in 0..self.n_components {
            let lambda = eigenvalues[r].max(0.0);
            lambdas[r] = lambda;
            // Normalize alphas so that lambda * alpha.alpha = 1 (standard Kernel PCA convention)
            let norm = if lambda > 1e-12 { lambda.sqrt() } else { 1.0 };
            for i in 0..n {
                alphas[[i, r]] = eigenvectors[[i, r]] / norm;
            }
        }
```

```rust
        // Project training data. The closed form is
        // X_projected[i, r] = sqrt(lambda_r) * eigenvector[i, r]
        let mut projected = Array2::<f64>::zeros((n, self.n_components));
        for r in 0..self.n_components {
            let scale = lambdas[r].sqrt();
            for i in 0..n {
                projected[[i, r]] = eigenvectors[[i, r]] * scale;
            }
        }
```

- **La prueba de los anillos no prueba una separación.** [`test_rbf_kernel_separates_rings`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L264) ajusta [dos componentes con γ = 0.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L276) sobre los anillos del §5 y solo comprueba que la [media de los cuadrados de la primera componente](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L283) está [por encima de 10^-4](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L285). La transcripción predice la imagen del §5: dos cuadrados concéntricos de radios de unos 0.583 y 0.653, que ninguna recta separa, y una media de los cuadrados de unos 0.191, que pasa. El ejemplo del módulo ejecuta los mismos datos y ajustes bajo el comentario [«Two rings of points — impossible to separate with linear PCA»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L29), y solo comprueba [el número de columnas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L42).
- **La nota de IX sobre esta prueba da el veredicto correcto por una razón equivocada.** La nota [`kernel-pca-symmetric-centroid-trap.md`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L7) explica por qué fallaba una versión anterior de la prueba, que comparaba los centros de los anillos en la primera componente: toda [«component of the projection has zero mean within each symmetric ring»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L45). Su veredicto, [«This is not a Kernel PCA bug.»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L47), se sostiene, pero no su razón: el §5 muestra que la afirmación vale para todas las componentes menos una: la componente radial, cuarta con γ = 0.5, tiene medias ±0.290 en los anillos y ninguna dispersión dentro de un anillo. La prueba anterior fallaba porque esa componente no estaba entre las dos conservadas, y no porque la simetría impida una separación. La alternativa de la nota, la [separación por pares](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L65), habría fallado con las dos componentes conservadas: un punto interior está a unos 0.070 de su vecino exterior y a 0.824 del siguiente punto interior. La nota recomienda también preguntarse [«what would this assertion look like on completely random data?»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L77) La aserción de reemplazo no supera esa comprobación: la media de los cuadrados de la primera componente es λ₁/n para cualesquiera datos, y sobre la recta equiespaciada del §5 con γ = 0.5 es de unos 0.250, más que en los anillos.
- **Una componente con un valor propio diminuto se proyecta de dos maneras.** El [umbral](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L144) conserva α = v en lugar de v/√λ cuando 0 < λ ≤ 10^-12, así que en los puntos de entrenamiento `transform` devuelve λv donde `fit_transform` devuelve √λ v, a un factor √λ de distancia. Para los puntos (±1, 0) y (0, ±5 · 10^-7) con el núcleo lineal y dos componentes, λ₂ = 5 · 10^-13: `fit_transform` da las segundas coordenadas ±5 · 10^-7, las proyecciones verdaderas, y `transform` da unos ±3.54 · 10^-13. Ninguna prueba compara las dos vías: [`test_transform_out_of_sample`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L308) solo comprueba [la forma](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L314) de su salida.
- **La documentación describe unos alphas que el código no almacena.** La documentación del módulo da la proyección como [`alpha_r[i] * sqrt(lambda_r)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L17) y llama a los alphas almacenados los [vectores propios de la matriz de núcleo centrada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L71), pero el código almacena los [vectores propios divididos por √λ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L146), como pretende su propio [comentario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L143). Con los alphas almacenados, la fórmula documentada devuelve vᵢ en lugar de √λ vᵢ. La [proyección de entrenamiento](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L156) del código multiplica los vectores propios por √λ y es correcta.
- **Un núcleo NaN devuelve igualmente `Ok`.** El MAT-013 señaló que el núcleo polinómico, con un [grado de tipo `f64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L57) elevado con [`powf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L225), da NaN cuando una base negativa se encuentra con un grado fraccionario. El ajuste no se detiene ahí. La media global propaga el NaN a todas las entradas de K_c, `symmetric_eigen` recorre sus [100 barridos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47) sobre NaN, y el [recorte](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L141) convierte cada valor propio NaN en 0, porque `f64::max` de Rust devuelve el otro operando cuando uno es NaN. Sobre el cuadrado (±1, 0), (0, ±1) con grado 1.5, γ = 1 y c = 0, donde k((1, 0), (−1, 0)) = (−1)^1.5, la transcripción predice 600 rotaciones, y luego `Ok`, con todas las proyecciones NaN y todos los λ iguales a 0.
- **Las pruebas comprueban formas más que propiedades.** De las seis pruebas, la [prueba lineal](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L243) comprueba una propiedad real, puntuaciones monótonas a lo largo de una recta. La prueba de los anillos comprueba una media de los cuadrados que casi cualesquiera datos superan, la [prueba polinómica](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L292) y la prueba de `transform` comprueban formas, y las dos últimas comprueban que se rechazan `n_components` = 0 y `n_components` ≥ n. Ninguna varía γ, compara `transform` con `fit_transform`, ni usa un control negativo.
- **Sin preimagen ni selección del ancho de banda.** `KernelPca` no tiene preimagen, ni regla ni búsqueda para γ, ni comprobación de que la matriz de núcleo sea semidefinida positiva.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

La prueba de los anillos de IX conserva dos componentes con γ = 0.5. Calcular λ_rad = sᵀKs para sus datos, con s = (1, 1, 1, 1, −1, −1, −1, −1)/√8, y explicar por qué las medias en los anillos de la primera componente son iguales mientras que las de la cuarta no lo son.

> *Solución:* Dentro del anillo interior los cuadrados de las distancias son 2 entre vecinos y 4 entre opuestos; dentro del anillo exterior, 8 y 16; entre los anillos, 1 en el mismo ángulo, 5 en ángulo recto y 9 en oposición. Sumando K sobre los pares ordenados con γ = 0.5, el bloque interior da 4 + 8e^−1 + 4e^−2 ≈ 7.484, el bloque exterior 4 + 8e^−4 + 4e^−8 ≈ 4.148 y cada bloque entre los anillos 4e^−0.5 + 8e^−2.5 + 4e^−4.5 ≈ 3.127, así que λ_rad ≈ (7.484 + 4.148 − 2 × 3.127)/8 ≈ 0.672. Eso está por debajo de 1.531, 1.531 y 1.216, así que s es el cuarto vector propio, y un ajuste con dos componentes no lo conserva. La primera componente pertenece al par empatado, ortogonal al plano de los vectores constantes en cada anillo, así que su media en cada anillo es 0; la cuarta es el propio s, con las puntuaciones ±√(0.672/8) ≈ ±0.290.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Núcleo lineal.** Llamar a `fit_transform` con el núcleo lineal y una componente sobre los puntos 0, 1 y 3, y luego a `transform` sobre el punto 2. Predicción: ±(−4/3, −1/3, 5/3) y ±2/3, con el mismo signo, con un margen de 10^-12.
2. **Los anillos.** Llamar a `fit_transform` sobre los datos de `test_rbf_kernel_separates_rings` con siete componentes, para cada γ del barrido 0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5 y 10, y encontrar la componente cuyas puntuaciones son constantes en cada anillo. Predicción: es la cuarta para cada γ; con γ = 0.5 los valores propios son los del §5, la cuarta componente tiene medias ±0.290 en los anillos, y las dos primeras colocan los anillos a radios de unos 0.583 y 0.653.
3. **Anillos con radio interior 0.3.** Repetir el paso 2 con el anillo interior de radio 0.3 y el exterior de radio 1, añadiendo γ = 1.5, 1.6 y 50. Predicción: la componente radial es la cuarta hasta γ = 0.5, la tercera con 1 y 1.5, y la primera a partir de 1.6, con una ventaja de unos 0.357 con γ = 5 y 1.2 · 10^-4 con γ = 50.
4. **Control negativo.** Llamar a `fit_transform` con dos componentes sobre los puntos 0, 1, …, 7 de una recta, sobre el mismo barrido. Predicción: la primera componente es monótona hasta γ = 0.05 y se pliega por ambos extremos a partir de 0.1; su mayor hueco está entre los puntos 3 y 4 y es 0.145 del rango con γ = 0.001 y 0.347 con γ = 2, 5 y 10; con γ = 0.5, la media de los cuadrados de la primera componente es de unos 0.250, por encima del 0.191 de los anillos.
5. **Transformación frente a ajuste.** Sobre los puntos (±1, 0) y (0, ±ε) con el núcleo lineal y dos componentes, comparar `transform` sobre los puntos de entrenamiento con `fit_transform`, para ε = 10^-6 y 5 · 10^-7. Predicción: coincidencia con un margen de 10^-15 para ε = 10^-6; para ε = 5 · 10^-7, segundas coordenadas de unos ±5 · 10^-7 y ±3.54 · 10^-13.
6. **Un grado fraccionario.** Llamar a `fit_transform` con dos componentes y el núcleo polinómico de grado 1.5, γ = 1 y c = 0 sobre los puntos (±1, 0) y (0, ±1). Predicción: `Ok`, con todas las proyecciones NaN y los dos λ iguales a 0.

### Ejercicio práctico

En el paso 5, ¿para qué ε hace el umbral de IX que `transform` discrepe de `fit_transform`, y en qué factor?

> *Solución:* Los puntos ya están centrados, y los valores propios no nulos de K_c = XXᵀ son 2 y 2ε², con el vector propio unitario v₂ = (0, 0, 1, −1)/√2 para 2ε². El umbral conserva α = v₂ cuando 2ε² ≤ 10^-12, es decir, cuando ε ≤ (5 · 10^-13)^(1/2) ≈ 7.07 · 10^-7. `fit_transform` devuelve entonces √(2ε²) v₂, las coordenadas verdaderas ±ε, mientras que `transform` devuelve K_c v₂ = 2ε² v₂, las coordenadas ±√2 ε²: un factor √2 ε, de unos 7.07 · 10^-7 con ε = 5 · 10^-7, donde las coordenadas son ±5 · 10^-7 y unos ±3.54 · 10^-13. Devolver una columna de ceros para tales componentes, en las dos vías, las haría coincidir.

---

## 8. Errores comunes

- **Leer una separación en un solo valor de γ.** Comunicar el intervalo de γ en el que se mantiene, y el rango de la componente que la lleva.
- **Saltarse el control negativo.** Pasar datos sin la estructura por la misma cadena; un criterio que los supera no mide nada.
- **Comprobar una propiedad que toda entrada tiene.** Una varianza no nula, una forma correcta o un valor finito valen para casi cualesquiera datos; una prueba debe poder fallar cuando falta la propiedad.
- **Suponer que las primeras componentes llevan la estructura.** La componente que separa puede ser la tercera o la cuarta; mirar más componentes, y los valores propios, antes de concluir que un núcleo ha fallado.
- **Centrar un punto nuevo con sus propias estadísticas.** Un punto nuevo debe centrarse con las medias de fila y la media global de entrenamiento, o su puntuación no es comparable con las de entrenamiento.
- **Fiarse de una proyección con γ grande.** Cuando K está cerca de la identidad, los valores propios no nulos están todos cerca de 1 y las componentes son arbitrarias.
- **Comparar dos ejecuciones del ACP con núcleo coordenada a coordenada.** Unos valores propios empatados, como en los anillos, hacen de cualquier rotación del par empatado una respuesta igual de válida.
- **Usar un núcleo que no es semidefinido positivo.** Sus valores propios negativos no tienen varianza que explicar, y recortarlos a 0 oculta el problema.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **ACP con núcleo** | El ACP de las imágenes φ(xᵢ) en el espacio de características, calculado a partir de la matriz de núcleo |
| **Truco del núcleo** | Sustituir los productos escalares por valores de núcleo, de modo que φ nunca se forma |
| **Matriz de núcleo centrada** | K_c = JKJ, los productos escalares de las imágenes centradas |
| **Coeficientes duales** | Los pesos α = v/√λ que expresan una dirección unitaria del espacio de características a través de las imágenes de entrenamiento |
| **Proyección fuera de la muestra** | La puntuación Σⱼ αⱼ k̃ⱼ(x) de un punto nuevo, centrada con las estadísticas de entrenamiento |
| **Ancho de banda** | La escala que fija γ en el núcleo RBF exp(−γ‖x − y‖²) |
| **Componente radial** | Para anillos con los mismos ángulos, el vector propio constante en cada anillo y ortogonal a 1, que los separa |
| **Control negativo** | Datos sin la estructura buscada, sobre los que un criterio de detección debe fallar |
| **Efecto herradura** | La curvatura de una recta en arco por los primeros vectores propios de un núcleo local |
| **Problema de la preimagen** | Encontrar una entrada cuya imagen sea la más cercana a un punto dado del espacio de características |

---

## Autoevaluación

**1. Un colega muestra un gráfico de ACP con núcleo de datos de expresión génica con γ = 3, con dos grupos nítidos, y nada más. ¿Qué le pides?**
> El mismo gráfico sobre un rango de γ, con el rango en el que los grupos siguen separados; los valores propios, para ver qué componente lleva la separación y si empata con otras; y la misma cadena sobre un control negativo, como los datos con cada variable permutada de forma independiente, lo que conserva la distribución de cada variable y destruye la estructura conjunta. Los grupos no deben aparecer ahí. Como muestra el §5, puntos equiespaciados en una recta pueden mostrar un hueco de más del doble del espaciado regular con γ grande.

**2. ¿Por qué el ACP con núcleo con el núcleo lineal nunca puede separar dos anillos concéntricos, mientras que un núcleo RBF a veces sí?**
> Con el núcleo lineal, el ACP con núcleo es el ACP, una proyección lineal, y ninguna proyección lineal separa los anillos. El espacio de características RBF contiene, para anillos con los mismos ángulos, una dirección cuyas puntuaciones son constantes en cada anillo; los separa perfectamente, pero solo cuando su valor propio se sitúa entre las componentes conservadas, lo que depende de γ y de la geometría.

**3. `transform` y `fit_transform` de IX discrepan en los puntos de entrenamiento para una componente. ¿Qué compruebas?**
> El valor propio de esa componente. IX conserva α = v cuando 0 < λ ≤ 10^-12, así que `transform` devuelve λv donde `fit_transform` devuelve √λ v. Esa componente no lleva varianza utilizable: descartarla, o reducir `n_components`.

**4. Una prueba llamada `test_rbf_kernel_separates_rings` comprueba que la primera componente tiene una media de los cuadrados por encima de 10^-4. ¿Cómo sería una aserción con sentido?**
> Una que falle cuando los anillos no están separados: por ejemplo, que alguna componente conservada tenga todas las puntuaciones interiores a un lado de un umbral y todas las exteriores al otro, con un margen, junto con que la misma comprobación falle sobre un control negativo. Con los datos de IX y dos componentes con γ = 0.5, esa prueba fallaría, que es el resultado honesto; con cuatro componentes, pasaría en la cuarta.

**Criterio de aprobación:** Deducir el ACP con núcleo de la forma de Gram del ACP, centrar una matriz de núcleo y explicar la cota de n − 1 componentes, normalizar los coeficientes duales y proyectar puntos nuevos, describir los límites en γ, analizar los anillos por simetría, diseñar un barrido del ancho de banda con un control negativo, y rastrear dónde la prueba, la documentación y el umbral de `KernelPca` de IX prometen más de lo que el código entrega.

---

## Base de investigación

- J. Mercer, «Functions of positive and negative type, and their connection with the theory of integral equations», *Philosophical Transactions of the Royal Society A* 209, 1909: los núcleos positivos
- B. Schölkopf, A. Smola y K.-R. Müller, «Nonlinear component analysis as a kernel eigenvalue problem», *Neural Computation* 10, 1998: el ACP con núcleo, el centrado en el espacio de características y la normalización de los coeficientes duales
- S. Mika, B. Schölkopf, A. Smola, K.-R. Müller, M. Scholz y G. Rätsch, «Kernel PCA and de-noising in feature spaces», *Advances in Neural Information Processing Systems* 11, 1999: preimágenes por iteración
- C. K. I. Williams, «On a connection between kernel PCA and metric multidimensional scaling», *Machine Learning* 46, 2002: el ACP con núcleos isótropos y el MDS
- B. Schölkopf y A. J. Smola, *Learning with Kernels*, MIT Press, 2002: núcleos, centrado y proyección fuera de la muestra
- J. T. Kwok e I. W. Tsang, «The pre-image problem in kernel methods», *IEEE Transactions on Neural Networks* 15, 2004: preimágenes a partir de las distancias
- P. Diaconis, S. Goel y S. Holmes, «Horseshoes in multidimensional scaling and local kernel methods», *Annals of Applied Statistics* 2, 2008: el efecto herradura
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
