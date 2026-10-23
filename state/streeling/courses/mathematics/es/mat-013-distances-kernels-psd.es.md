---
module_id: mat-013-distances-kernels-psd
department: mathematics
course: Distancias, núcleos y matrices semidefinidas positivas
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Distancias, núcleos y matrices semidefinidas positivas — Cuándo una similitud es de verdad un producto escalar

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Enunciar los axiomas de una métrica, y decidir si una distancia dada los cumple
- Reconocer las matrices semidefinidas positivas, comprobarlas con sus valores propios, y exhibir un testigo cuando una matriz falla
- Explicar qué hace válido a un núcleo, y construir o rechazar núcleos con matrices de Gram
- Describir cómo el ancho de banda del núcleo gaussiano lleva su matriz de Gram de la identidad a una matriz de rango uno
- Usar la distancia de Mahalanobis, y decir qué matrices la convierten en una métrica
- Rastrear qué garantizan las distancias, los núcleos y la prueba por valores propios de IX, y dónde un redondeo o un recorte silencioso viola un axioma

---

## 1. Las métricas y lo que prometen

Una **métrica** sobre un conjunto es una función d(x, y) con cuatro propiedades: d(x, y) ≥ 0; d(x, y) = 0 exactamente cuando x = y; d(x, y) = d(y, x); y la **desigualdad triangular** d(x, z) ≤ d(x, y) + d(y, z). Una **pseudométrica** abandona una mitad del segundo axioma: puntos distintos pueden estar a distancia 0. Los algoritmos se apoyan en estos axiomas: un índice de vecinos más cercanos poda toda una región gracias a la desigualdad triangular, y un método de agrupamiento que fusiona puntos a distancia 0 supone que son el mismo punto.

Las distancias de Minkowski (Σ|xᵢ − yᵢ|^p)^(1/p) del MAT-004 son métricas para p ≥ 1. Para p = 1/2 la desigualdad triangular falla: de (0, 0) a (1, 1) la fórmula da (1 + 1)² = 4, mientras que el rodeo por (1, 0) cuesta 1 + 1 = 2. La distancia euclidiana al cuadrado también falla, sobre los puntos 0, 1 y 2 de la recta: 4 > 1 + 1. Sirve para comparar distancias, ya que elevar al cuadrado conserva su orden, pero no es en sí misma una métrica.

### Ejercicio práctico

La distancia coseno es 1 − cos θ, donde θ es el ángulo entre dos vectores no nulos. ¿Es una métrica? ¿Y el propio ángulo θ?

> *Solución:* No. Toma vectores unitarios a 0°, 45° y 90°. Las distancias entre vecinos valen 1 − √2/2 ≈ 0.2929 cada una, su suma 0.5858, mientras que la distancia de 0° a 90° es 1: la desigualdad triangular falla, así que ni siquiera es una pseudométrica. El ángulo θ = arccos(cos θ) es una métrica sobre la esfera unidad: es la longitud del arco más corto, y aquí π/4 + π/4 = π/2, con igualdad. Sobre vectores no normalizados, el ángulo es solo una pseudométrica, ya que x y 2x forman un ángulo nulo.

---

## 2. Matrices semidefinidas positivas

Una matriz simétrica A es **semidefinida positiva** (SDP) si xᵀAx ≥ 0 para todo vector x, y **definida positiva** si xᵀAx > 0 para todo x ≠ 0. Por el teorema espectral del MAT-005, A = QΛQᵀ con Q ortogonal, así que xᵀAx = Σλᵢ(qᵢ · x)²: A es SDP exactamente cuando todos sus valores propios son ≥ 0, y definida positiva cuando todos son > 0. Toda **matriz de Gram** G = BBᵀ, cuya entrada (i, j) es el producto escalar de las filas i y j de B, es SDP, ya que xᵀGx = ‖Bᵀx‖² ≥ 0. Recíprocamente, toda matriz SDP es una matriz de Gram: A = (QΛ^(1/2))(QΛ^(1/2))ᵀ.

De ahí salen tres pruebas prácticas. La prueba por valores propios calcula el valor propio más pequeño y lo compara con una tolerancia, ya que el redondeo desplaza los valores propios en torno a u‖A‖ (MAT-003). La **factorización de Cholesky** A = LLᵀ, con L triangular inferior, tiene éxito exactamente para las matrices definidas positivas y cuesta unas n³/3 operaciones, mucho menos que una descomposición espectral. Y un solo vector x con xᵀAx < 0 es un **testigo** de que A no es SDP, fácil de comprobar a mano. El criterio de Sylvester, según el cual los menores principales dominantes son positivos, caracteriza solo las matrices definidas positivas; para SDP, todos los menores principales deben ser ≥ 0, no solo los dominantes.

### Ejercicio práctico

Una «similitud» da 1 a los puntos separados como mucho por un paso en la recta: T = [[1, 1, 0], [1, 1, 1], [0, 1, 1]] para los puntos 0, 1 y 2, escrita fila por fila. ¿Es T SDP?

> *Solución:* No. Para x = (1, −1, 1), Tx = (0, 1, 0), así que xᵀTx = −1 < 0: x es un testigo. Los valores propios son 1 − √2 ≈ −0.414, 1 y 1 + √2 ≈ 2.414; suman la traza 3, y su producto es el determinante −1. Todas las entradas diagonales son positivas y cada fila parece una similitud, y sin embargo T no es la matriz de Gram de ningún conjunto de vectores.

---

## 3. Núcleos

Un **núcleo** k(x, y) es una similitud que es un producto escalar en algún espacio de características: k(x, y) = φ(x) · φ(y) para una aplicación φ. Una función k es un **núcleo definido positivo** cuando toda matriz de Gram Kᵢⱼ = k(xᵢ, xⱼ), para todo conjunto finito de puntos, es SDP; por el teorema de Moore–Aronszajn, esa es exactamente la condición para que exista tal φ, posiblemente con valores en un espacio de dimensión infinita. El teorema de Mercer enuncia la misma condición para los núcleos continuos mediante su operador integral. Las sumas, los productos y los múltiplos positivos de núcleos son núcleos, y así se construyen la mayoría de ellos.

Los tres núcleos clásicos son el núcleo **lineal** x · y; el núcleo **polinómico** (γ x · y + c)^d, que es un núcleo cuando d es un entero positivo, γ > 0 y c ≥ 0; y el núcleo **gaussiano** o **RBF** exp(−γ‖x − y‖²), que es un núcleo para todo γ > 0. Todo núcleo define una distancia en el espacio de características, d_k(x, y)² = k(x, x) + k(y, y) − 2k(x, y), una pseudométrica en general y una métrica cuando φ es inyectiva. La similitud coseno es el núcleo lineal de los vectores normalizados x/‖x‖, y su distancia de núcleo es √(2 − 2 cos θ), la cuerda que los une: la raíz cuadrada del doble de la distancia coseno del §1 es una métrica sobre la esfera unidad, mientras que la distancia coseno misma no lo es.

### Ejercicio práctico

¿Es k(x, y) = (xy − 1)² un núcleo sobre la recta real? Usa los puntos 0, 1 y 2.

> *Solución:* No. Su matriz de Gram sobre 0, 1 y 2 es [[1, 1, 1], [1, 0, 1], [1, 1, 9]]. El menor principal sobre los puntos 0 y 1, [[1, 1], [1, 0]], tiene determinante −1 < 0, así que la matriz no es SDP. Aquí c = −1 < 0: al desarrollar se obtiene (xy)² − 2xy + 1, y el término −2xy resta un núcleo. Con c = +1, (xy + 1)² = φ(x) · φ(y) para φ(x) = (x², √2 x, 1).

---

## 4. El ancho de banda del núcleo gaussiano

El parámetro γ del núcleo RBF fija la escala a la que los puntos cuentan como similares, y a menudo se escribe γ = 1/(2σ²) con un ancho de banda σ. Cuando γ crece, cada entrada fuera de la diagonal tiende a 0 y K tiende a la identidad: cada punto solo se parece a sí mismo, y un método construido sobre K memoriza su conjunto de entrenamiento. Cuando γ decrece, cada entrada tiende a 1 y K tiende a la matriz de unos, cuyos valores propios son n, 0, …, 0: cada punto se parece a todos los demás.

Entre ambos extremos, K es SDP pero puede estar mal condicionada. Sobre los puntos 0, 1 y 2 de la recta, el valor propio más pequeño de K es de unos 0.489 para γ = 1, 0.0124 para γ = 0.1, 1.3 · 10^-4 para γ = 0.01 y 1.3 · 10^-6 para γ = 10^-3, donde el número de condición llega a unos 2.2 · 10^6: por la regla del MAT-003, una resolución con K puede perder seis cifras. Con más puntos o un γ más pequeño, una matriz exactamente SDP puede tener un valor propio calculado ligeramente por debajo de 0, así que una prueba por valores propios debe aceptar valores hasta una tolerancia proporcional a n u ‖K‖, y no tratar cada número negativo como un veredicto. Un valor inicial habitual toma como σ la distancia mediana entre los puntos.

### Ejercicio práctico

Para n puntos distintos, ¿a qué tienden la matriz de Gram RBF y sus valores propios cuando γ → ∞ y cuando γ → 0?

> *Solución:* Cuando γ → ∞, exp(−γ‖xᵢ − xⱼ‖²) → 0 para i ≠ j, así que K → I, con todos sus valores propios iguales a 1: perfectamente condicionada, y ningún par de puntos similares. Cuando γ → 0, cada entrada tiende a 1, así que K → 11ᵀ, con valores propios n y 0 repetido n − 1 veces: los valores propios más pequeños tienden a 0 y el número de condición crece sin cota.

---

## 5. La distancia de Mahalanobis

Para un vector aleatorio con matriz de covarianza S, la **distancia de Mahalanobis** es d_M(x, y) = √((x − y)ᵀ M (x − y)) con M = S⁻¹. Mide las diferencias en unidades de la dispersión en cada dirección: con S = diag(4, 1), los puntos (2, 0) y (0, 0) están a distancia 1, tan lejos como (0, 1) y (0, 0). Si S = LLᵀ es una factorización de Cholesky, d_M(x, y) = ‖L⁻¹(x − y)‖: la distancia de Mahalanobis es la distancia euclidiana tras el **blanqueo** de los datos.

La matriz M decide si d_M es una métrica. Si M es simétrica definida positiva, lo es. Si M es solo SDP, las direcciones de su núcleo son invisibles, y d_M es una pseudométrica. Si M tiene un valor propio negativo, la cantidad bajo la raíz puede ser negativa, y d_M no es en absoluto una distancia. Solo la parte simétrica (M + Mᵀ)/2 entra en la forma cuadrática, de modo que una M no simétrica oculta lo que realmente mide.

### Ejercicio práctico

Sea M = [[1, 2], [0, 1]]. Su determinante es 1, así que es invertible. ¿Es √((x − y)ᵀ M (x − y)) una métrica?

> *Solución:* No. Con d = x − y, dᵀMd = d₁² + 2d₁d₂ + d₂² = (d₁ + d₂)². Nunca es negativa, pero se anula siempre que d₂ = −d₁: los puntos (1, −1) y (0, 0) son distintos y están a distancia 0. La parte simétrica [[1, 1], [1, 1]] tiene valores propios 2 y 0, así que la «distancia» es una pseudométrica que solo ve d₁ + d₂. La invertibilidad de M no es la condición; lo es que su parte simétrica sea definida positiva.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de las funciones siguientes a Python, cuyos flotantes son binary64 IEEE como el `f64` de Rust: son predicciones, y el §7 propone comprobarlas.

**Distancias** (`crates/ix-math`). [`distance.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L60) ofrece las funciones euclidiana, de Manhattan, de Minkowski, de Chebyshev y coseno; la distancia de Minkowski [rechaza p < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L48), la condición del §1. La herramienta MCP `ix_distance`, a través del manejador [`distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L148), ofrece las métricas euclidiana, de Manhattan y [coseno](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L163). [`GeometricSpace`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L38) reúne once distancias tras una sola función [`distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L87), entre ellas la [distancia de Mahalanobis](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L61), que recibe del llamador una covarianza inversa; el módulo está [exportado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/lib.rs#L14), y ningún código fuera de sus propias pruebas lo llama. Las funciones coseno dicen:

```rust
/// Cosine similarity (not distance). Returns value in [-1, 1].
pub fn cosine_similarity(a: &Array1<f64>, b: &Array1<f64>) -> Result<f64, MathError> {
    check_same_len(a, b)?;
    let dot: f64 = a.dot(b);
    let norm_a = a.dot(a).sqrt();
    let norm_b = b.dot(b).sqrt();
    if norm_a < 1e-12 || norm_b < 1e-12 {
        return Ok(0.0);
    }
    Ok(dot / (norm_a * norm_b))
}

/// Cosine distance = 1 - cosine_similarity.
pub fn cosine_distance(a: &Array1<f64>, b: &Array1<f64>) -> Result<f64, MathError> {
    cosine_similarity(a, b).map(|s| 1.0 - s)
}
```

- **Una distancia coseno puede ser negativa.** Para x = (1, 1, 1), el producto escalar es 3 y cada norma √3, pero el producto de las dos normas redondeadas es 2.9999999999999996, así que la similitud de x consigo mismo es 1 + 2^-52 y su [distancia](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L73) a sí mismo es −2^-52 ≈ −2.2 · 10^-16. Nada recorta el valor, así que el intervalo documentado [−1, 1] y el axioma d ≥ 0 fallan ambos; para x = (1, 1), la distancia a sí mismo es en cambio +2^-52. La distancia esférica de `GeometricSpace` sí [recorta su coseno](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L113). La extensión de DuckDB enuncia el [invariante](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/udf.rs#L224) «identical vectors -> 0.0», y su prueba usa [(1, 2, 3)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/lib.rs#L311), para el que el redondeo resulta ser exacto.
- **Un vector nulo está a distancia 1 de sí mismo.** Cuando una norma es menor que 10^-12, la similitud [devuelve 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L66), así que la distancia coseno de 0 a 0 es 1. La distancia esférica toma la [decisión contraria](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L111): el vector nulo está a distancia 0 de todo vector, incluidos (1, 0) y (0, 1), que están a π/2 uno de otro, así que la desigualdad triangular falla al pasar por él.
- **Una forma de Mahalanobis negativa se recorta a 0.** La rama de Mahalanobis de más abajo comprueba [solo la forma](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L136) de la matriz, no su simetría ni su carácter definido, y [toma el máximo con 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L145) antes de la raíz cuadrada. Con la «covarianza inversa» diag(1, −1), los puntos (1, 1) y (0, 0) están a distancia 0, y también (0, 1) y (0, 0), cuya forma cuadrática vale −1: no se produce ningún error, y cada par de puntos distintos recibe la distancia 0. Con [[1, 2], [0, 1]], la matriz del §5, el par (1, −1) y (0, 0) también recibe 0.
- **La tolerancia de Hamming viola la desigualdad triangular.** La distancia de Hamming cuenta las coordenadas que [difieren en más de 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L168). La igualdad salvo una tolerancia no es transitiva: para los puntos de una coordenada 0, 6 · 10^-13 y 1.2 · 10^-12, las distancias son 0, 0 y 1.
- **Chebyshev ignora NaN.** La distancia de Chebyshev toma un [máximo acumulado con `f64::max`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L82), que devuelve el otro operando cuando uno es NaN: (NaN, 0) y (0, 0) están a distancia de Chebyshev 0, mientras que su distancia euclidiana es NaN.
- **Los núcleos no se validan, y los valores propios negativos se recortan.** El ACP con núcleo ofrece las variantes de [`Kernel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L53) del §3, con un [grado polinómico de tipo `f64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L57) aplicado con [`powf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L225), y un [RBF](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L232) que acepta γ de cualquier signo. Nada rechaza c < 0, un grado fraccionario o γ < 0, que pueden dar matrices de Gram que no son SDP, o entradas NaN cuando una base negativa se eleva a una potencia fraccionaria, y el ajuste [sustituye cada valor propio negativo por 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L141) sin informar de ello. La documentación del módulo dice que se pueden añadir núcleos propios [implementando el trait `Kernel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L20), pero `Kernel` es una enumeración, no un trait.
- **La prueba por valores propios depende de la escala.** IX no tiene prueba SDP ni factorización de Cholesky, así que la prueba por valores propios del §2 debe pasar por [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L46), el método de Jacobi del MAT-005, cuya tolerancia de [10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47) es absoluta. Su [prueba de parada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L82) se cumple antes de la primera rotación para 10^-13 T, la matriz del §2 reducida de escala, así que la función devuelve la diagonal, tres veces 10^-13, y una matriz indefinida pasa por SDP. Con 8 · 10^-13 T se detiene tras un barrido de tres rotaciones con unos −2.9 · 10^-13 en lugar del valor exacto 8 · 10^-13 (1 − √2) ≈ −3.3 · 10^-13.

La rama de Mahalanobis de `distance`:

```rust
        GeometricSpace::Mahalanobis { inv_cov } => {
            let n = a.len();
            if inv_cov.shape() != [n, n] {
                return Err(MathError::DimensionMismatch {
                    expected: n,
                    got: inv_cov.shape()[0],
                });
            }
            let diff = a - b;
            let sx = inv_cov.dot(&diff);
            let acc = diff.dot(&sx);
            Ok(acc.max(0.0).sqrt())
        }
```

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

¿Por qué la distancia coseno de (1, 1, 1) a sí mismo es negativa, mientras que la de (1, 2, 3) a sí mismo es exactamente 0?

> *Solución:* El código divide el producto escalar por el producto de dos raíces cuadradas redondeadas por separado. Para (1, 1, 1), √3 se redondea a un double cuyo cuadrado, 2.9999999999999996, queda justo por debajo de 3, así que 3 dividido por él da 1 + 2^-52, y 1 menos eso da −2^-52. Para (1, 2, 3), el producto escalar es 14, y el cuadrado de √14 redondeado resulta redondearse exactamente a 14, así que la similitud es exactamente 1. Que la distancia a sí mismo sea 0, ligeramente positiva o ligeramente negativa depende de cómo caiga un redondeo; por eso una distancia construida a partir de una similitud debe recortarse a 0, o calcularse como ‖x/‖x‖ − y/‖y‖‖²/2, que nunca es negativa.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Matrices de Gram.** Sobre los puntos (0, 0), (1, 0), (0, 1), (1, 1) y (2, 1), construir las matrices de Gram del núcleo lineal, del núcleo RBF con γ = 0.5 y del núcleo polinómico (x · y + 1)², y pasar cada una a `symmetric_eigen`. Predicción: la matriz lineal tiene rango 2, con sus tres valores propios más pequeños a menos de 10^-12 de 0; los valores propios más pequeños de las otras dos son de unos 0.133 y 0.298. Con c = −1 en el núcleo polinómico, y con γ = −0.5 en el núcleo RBF, los valores propios más pequeños son de unos −1.08 y −12.6.
2. **La similitud con umbral y su escala.** Pasar la T del §2 a `symmetric_eigen`. Predicción: su valor propio más pequeño es 1 − √2 con un error menor que 10^-12. Pasar después 10^-13 T y 8 · 10^-13 T. Predicción: la primera devuelve tres veces 10^-13; la segunda devuelve un valor propio más pequeño cercano a −2.9 · 10^-13.
3. **Mahalanobis.** Llamar a `distance` con `Mahalanobis` e `inv_cov` igual a diag(1, −1), sobre (1, 1) y (0, 0), luego sobre (0, 1) y (0, 0); después con [[1, 2], [0, 1]] sobre (1, −1) y (0, 0). Predicción: las tres devuelven `Ok(0.0)`.
4. **Coseno.** Llamar al manejador `distance` con `metric` igual a `cosine` para a = b = (1, 1, 1), luego para a = b = (1, 1), luego para dos vectores nulos. Predicción: −2^-52, +2^-52 y 1.
5. **Hamming y Chebyshev.** Calcular las distancias de Hamming entre los puntos de una coordenada 0, 6 · 10^-13 y 1.2 · 10^-12, y la distancia de Chebyshev entre (NaN, 0) y (0, 0). Predicción: 0, 0 y 1, y 0.
6. **El ancho de banda.** Sobre los puntos 0, 1 y 2, pasar a `symmetric_eigen` las matrices de Gram RBF para γ = 1, 0.1, 0.01 y 10^-3. Predicción: valores propios más pequeños de unos 0.489, 0.0124, 1.3 · 10^-4 y 1.3 · 10^-6, cada uno a menos de 10^-12 de un solucionador de referencia, y todos positivos.

### Ejercicio práctico

En el paso 2, ¿para qué factores de escala c devuelve `symmetric_eigen` la diagonal de cT sin una sola rotación?

> *Solución:* El bucle suma los cuadrados por encima de la diagonal, aquí 2c², y se detiene cuando la raíz cuadrada es menor que 10^-12, es decir, cuando √2 c < 10^-12, o sea c < 10^-12/√2 ≈ 7.07 · 10^-13. Para todos esos c, la función devuelve tres veces c y la matriz parece definida positiva. El umbral es absoluto, así que no tiene nada que ver con que la matriz sea SDP; una prueba relativa, que comparara la norma fuera de la diagonal con la norma de la matriz, no dependería de c.

---

## 8. Errores comunes

- **Llamar distancia a cualquier disimilitud.** 1 − cos θ, la distancia euclidiana al cuadrado y la fórmula de Minkowski con p < 1 violan todas la desigualdad triangular; comprueba los axiomas antes de usar un índice o un método que dependa de ellos.
- **Confiar en una matriz de similitud porque parece correcta.** Una diagonal positiva y entradas razonables no hacen SDP a una matriz; busca su valor propio más pequeño o un testigo x con xᵀAx < 0.
- **Comprobar el carácter SDP con los menores dominantes.** El criterio de Sylvester caracteriza las matrices definidas positivas; para SDP, todos los menores principales deben ser ≥ 0.
- **Tomar un valor propio negativo diminuto por un veredicto.** El redondeo desplaza los valores propios en torno a u‖A‖; compara con una tolerancia proporcional a la matriz, no con 0 ni con una constante absoluta.
- **Usar un núcleo fuera de su dominio.** Un núcleo polinómico con c < 0 o un grado fraccionario, o un RBF con γ < 0, puede dar matrices de Gram que no son SDP; recortar después los valores propios negativos oculta el error.
- **Invertir una covarianza y esperar lo mejor.** La distancia de Mahalanobis necesita una matriz simétrica definida positiva; la invertibilidad no basta, y un recorte a 0 convierte un error en una distancia nula.
- **Construir una distancia a partir de una similitud sin recorte.** 1 − s puede ser negativo por redondeo cuando s debería valer 1; recorta a 0 o usa una fórmula que no pueda volverse negativa.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Métrica** | Una función no negativa, nula solo entre puntos iguales, simétrica, y que cumple la desigualdad triangular |
| **Pseudométrica** | Una métrica que puede dar distancia 0 a puntos distintos |
| **Desigualdad triangular** | d(x, z) ≤ d(x, y) + d(y, z) |
| **Matriz semidefinida positiva** | Una matriz simétrica con xᵀAx ≥ 0 para todo x, es decir, sin valores propios negativos |
| **Matriz de Gram** | La matriz de productos escalares de un conjunto de vectores, siempre SDP |
| **Testigo** | Un vector x con xᵀAx < 0, que prueba que A no es SDP |
| **Factorización de Cholesky** | A = LLᵀ con L triangular inferior, que existe exactamente para las matrices definidas positivas |
| **Núcleo definido positivo** | Una función cuyas matrices de Gram son todas SDP, es decir, un producto escalar de vectores de características |
| **Núcleo RBF** | exp(−γ‖x − y‖²), un núcleo para todo γ > 0, con ancho de banda σ dado por γ = 1/(2σ²) |
| **Distancia de Mahalanobis** | √((x − y)ᵀ S⁻¹ (x − y)), la distancia euclidiana tras el blanqueo por la covarianza S |
| **Blanqueo** | Un cambio de coordenadas lineal que convierte una matriz de covarianza en la identidad |

---

## Autoevaluación

**1. Una biblioteca de agrupamiento acepta cualquier «distancia». ¿En qué axiomas se apoya, y cuáles de 1 − cos θ, el ángulo θ y la distancia euclidiana al cuadrado los cumplen?**
> No negatividad, identidad de los indiscernibles, simetría y desigualdad triangular; esta última es la que permite a un índice podar una búsqueda. El ángulo es una métrica sobre la esfera unidad. 1 − cos θ viola la desigualdad triangular, como muestran 0°, 45° y 90°, y la distancia euclidiana al cuadrado la viola sobre 0, 1 y 2.

**2. Una matriz de núcleo de 500 × 500 tiene un valor propio calculado más pequeño de −3 · 10^-14, y el más grande es 400. ¿Es inválido el núcleo?**
> No con esa evidencia. Un solucionador espectral estable hacia atrás desplaza los valores propios en un pequeño múltiplo de u‖K‖, aquí u‖K‖ ≈ 400 · 1.1 · 10^-16 ≈ 4.4 · 10^-14, y el múltiplo crece con n, así que −3 · 10^-14 es 0 salvo redondeo. Un núcleo válido con puntos casi dependientes produce exactamente esto. Un valor propio claramente negativo, o un testigo x que siga siendo negativo en aritmética exacta, lo zanjaría.

**3. ¿Por qué la distancia de Mahalanobis necesita una matriz definida positiva, y qué devuelve IX cuando no lo es?**
> Con una M definida positiva, (x − y)ᵀM(x − y) > 0 para x ≠ y y d_M es la distancia euclidiana tras el blanqueo. Una M SDP pero singular aplasta las direcciones de su núcleo, y una M indefinida hace negativa la forma para algunos pares. IX solo comprueba la forma y recorta las formas negativas a 0, así que ambos fallos vuelven como una distancia nula, sin error.

**4. `ix_distance` devuelve una distancia coseno de −2.2 · 10^-16 para dos vectores idénticos. ¿Es un fallo de tus datos?**
> No. Es un redondeo en la fórmula de IX: el producto de las dos normas redondeadas puede quedar justo por debajo del producto escalar, lo que hace que la similitud supere 1. Recorta el resultado a 0 antes de usarlo como distancia, y no cuentes con ceros exactos para entradas idénticas.

**Criterio de aprobación:** Enunciar y comprobar los axiomas de una métrica, probar si una matriz es semidefinida positiva y dar un testigo cuando no lo es, decidir a partir de sus matrices de Gram si una función es un núcleo, explicar el efecto del ancho de banda RBF sobre el condicionamiento, dar la condición para que la distancia de Mahalanobis sea una métrica, y rastrear dónde las distancias y la prueba por valores propios de IX violan un axioma.

---

## Base de investigación

- M. Fréchet, «Sur quelques points du calcul fonctionnel», *Rendiconti del Circolo Matematico di Palermo* 22, 1906: los espacios métricos
- J. Mercer, «Functions of positive and negative type, and their connection with the theory of integral equations», *Philosophical Transactions of the Royal Society A* 209, 1909: los núcleos definidos positivos y los operadores integrales
- P. C. Mahalanobis, «On the generalised distance in statistics», *Proceedings of the National Institute of Sciences of India* 2, 1936: la distancia de Mahalanobis
- I. J. Schoenberg, «Metric spaces and positive definite functions», *Transactions of the American Mathematical Society* 44, 1938: cuándo una distancia procede de un producto escalar, y el núcleo gaussiano
- N. Aronszajn, «Theory of reproducing kernels», *Transactions of the American Mathematical Society* 68, 1950: el espacio de características de un núcleo definido positivo
- B. Schölkopf y A. J. Smola, *Learning with Kernels*, MIT Press, 2002: los núcleos, las matrices de Gram y su construcción
- R. A. Horn y C. R. Johnson, *Matrix Analysis*, 2.ª ed., Cambridge University Press, 2013: las matrices semidefinidas positivas, Cholesky y el criterio de Sylvester
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
