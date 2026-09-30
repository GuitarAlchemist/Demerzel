---
module_id: mat-004-vectors-matrices-norms
department: mathematics
course: Vectores, matrices, normas y aplicaciones lineales
level: beginner
alchemical_stage: nigredo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Vectores, matrices, normas y aplicaciones lineales — Lo que una matriz le hace al espacio

> **Departamento de Matemáticas** | Etapa: Nigredo (Principiante) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Describir un espacio vectorial y escribir un vector en coordenadas respecto de una base
- Reconocer una aplicación lineal y construir su matriz a partir de las imágenes de los vectores de la base
- Explicar por qué el producto de matrices es la composición de aplicaciones lineales, y por qué es asociativo pero no conmutativo
- Leer el determinante como un volumen con signo y estimar el costo de calcularlo por desarrollo en cofactores
- Enunciar los axiomas de norma, usar las normas p, y mostrar por qué la «norma» p = 1/2 no lo es
- Decir qué garantizan y qué no garantizan las funciones de álgebra lineal y de distancia de IX

---

## 1. Vectores y espacios vectoriales

Un **vector** de Rⁿ es una lista de n números reales, x = (x₁, …, xₙ). Los vectores se suman y se multiplican por números (**escalares**) componente a componente: (1, 2) + (3, 4) = (4, 6) y 3 · (1, 2) = (3, 6).

Un **espacio vectorial** es cualquier conjunto con una suma y una multiplicación por escalares de este tipo que cumplen las reglas conocidas: la suma es asociativa y conmutativa, hay un vector cero y cada vector tiene un opuesto, y la multiplicación por escalares es distributiva respecto de ambas sumas. Rⁿ es el ejemplo principal, pero no el único: los polinomios a₀ + a₁t + a₂t² de grado a lo sumo 2 también forman un espacio vectorial, y se comportan exactamente como las ternas (a₀, a₁, a₂).

Una **combinación lineal** de los vectores v₁, …, vₖ es una suma c₁v₁ + … + cₖvₖ. Una **base** es una lista de vectores tal que todo vector del espacio es combinación lineal de ellos de una única manera; los números cᵢ son entonces las **coordenadas** del vector en esa base. La **base canónica** de R² es e₁ = (1, 0), e₂ = (0, 1), y en ella las coordenadas de (3, 4) son simplemente 3 y 4. En otra base, el mismo vector tiene otras coordenadas.

### Ejercicio práctico

Encuentra las coordenadas de (3, 4) en la base u = (1, 1), w = (1, −1).

> *Solución:* Buscamos a y b con a · (1, 1) + b · (1, −1) = (3, 4), es decir, a + b = 3 y a − b = 4. Sumando las ecuaciones, 2a = 7, así que a = 7/2; restándolas, 2b = −1, así que b = −1/2. Comprobación: 7/2 · (1, 1) − 1/2 · (1, −1) = (7/2 − 1/2, 7/2 + 1/2) = (3, 4).

---

## 2. Aplicaciones lineales y sus matrices

Una aplicación L de un espacio vectorial en otro es **lineal** si respeta las dos operaciones:

L(u + v) = L(u) + L(v) y L(c · v) = c · L(v), para todos los vectores u, v y todo escalar c.

Las rotaciones alrededor del origen, las reflexiones respecto de una recta que pasa por el origen y los escalamientos son lineales. Una traslación x ↦ x + b con b ≠ 0 no lo es: toda aplicación lineal envía 0 a 0, porque L(0) = L(0 · 0) = 0 · L(0) = 0.

Una aplicación lineal queda determinada por lo que hace con una base. Si x = x₁e₁ + … + xₙeₙ, entonces L(x) = x₁L(e₁) + … + xₙL(eₙ). Por eso escribimos las imágenes L(e₁), …, L(eₙ) como las **columnas** de una matriz A, y calcular L(x) se convierte en el producto matriz–vector A x: x₁ veces la primera columna, más x₂ veces la segunda, y así sucesivamente. Por ejemplo, la rotación de 90° envía e₁ = (1, 0) a (0, 1) y e₂ = (0, 1) a (−1, 0), así que su matriz es

R = [[0, −1], [1, 0]],

escrita fila por fila.

### Ejercicio práctico

Encuentra la matriz S de la reflexión respecto de la recta y = x, y comprueba que envía (1, 2) a (2, 1).

> *Solución:* La reflexión intercambia las dos coordenadas, así que envía e₁ = (1, 0) a (0, 1) y e₂ = (0, 1) a (1, 0). Estas imágenes son las columnas: S = [[0, 1], [1, 0]]. Entonces S (1, 2) = 1 · (0, 1) + 2 · (1, 0) = (2, 1).

---

## 3. La composición es el producto de matrices

Si B es la matriz de una aplicación lineal M y A la de L, aplicar primero M y luego L sigue siendo lineal, y su matriz es el **producto** AB: por definición, (AB) x = A (B x). Calculando las columnas se obtiene la regla habitual

(AB)ᵢⱼ = Σₖ Aᵢₖ Bₖⱼ,

que exige que el número de columnas de A sea igual al número de filas de B. Fíjate en el orden: en (AB) x, la aplicación B actúa **primero**.

De esta definición se siguen dos propiedades:
- **El producto es asociativo**: (AB)C = A(BC). Ambos lados son la composición «C, luego B, luego A», y la composición de funciones siempre es asociativa. No hace falta ningún cálculo con las entradas.
- **El producto no es conmutativo**: en general AB ≠ BA, porque hacer dos cosas en el orden inverso suele ser hacer otra cosa.

### Ejercicio práctico

Con R = [[0, −1], [1, 0]] (rotación de 90°) y F = [[1, 0], [0, −1]] (reflexión respecto del eje x), calcula RF y FR y describe cada una como una transformación geométrica.

> *Solución:* RF = [[0 · 1 + (−1) · 0, 0 · 0 + (−1) · (−1)], [1 · 1 + 0 · 0, 1 · 0 + 0 · (−1)]] = [[0, 1], [1, 0]], la reflexión respecto de la recta y = x. FR = [[1 · 0 + 0 · 1, 1 · (−1) + 0 · 0], [0 · 0 + (−1) · 1, 0 · (−1) + (−1) · 0]] = [[0, −1], [−1, 0]], la reflexión respecto de la recta y = −x. Como RF ≠ FR, el orden importa: «reflejar y luego rotar» no es «rotar y luego reflejar».

---

## 4. El determinante como volumen

Para una matriz 2 × 2, det [[a, b], [c, d]] = ad − bc. Su valor absoluto es el **área** del paralelogramo generado por las dos columnas (a, c) y (b, d), y su signo dice si la aplicación conserva la orientación del plano (+) o la invierte (−). En n dimensiones, |det A| es el factor por el que A multiplica los volúmenes. De esta imagen se siguen tres hechos:
- det(AB) = det A · det B: aplicar B y luego A multiplica los volúmenes por ambos factores.
- det A = 0 exactamente cuando A aplasta el espacio sobre una dimensión menor, es decir, cuando sus columnas son linealmente dependientes y A no tiene inversa.
- Una rotación tiene determinante 1 y una reflexión −1: ambas conservan las áreas, y solo la reflexión invierte la orientación.

Para matrices más grandes, el **desarrollo en cofactores** por la primera fila reduce un determinante n × n a n determinantes de tamaño n − 1:

det A = Σⱼ (−1)ʲ⁺¹ a₁ⱼ det A₁ⱼ,

donde A₁ⱼ es A sin su primera fila ni su columna j. Es una definición correcta pero un algoritmo costoso. La **eliminación gaussiana** necesita un número de operaciones del orden de n³. Suma a una fila un múltiplo de otra, lo que no cambia el determinante, e intercambia filas, lo que cambia su signo. Así, det A es el producto de los pivotes, multiplicado por −1 por cada intercambio de filas: para [[0, 1], [1, 0]], un intercambio da los pivotes 1 y 1, y det = −1.

### Ejercicio práctico

Una implementación aplica el desarrollo en cofactores de forma recursiva y se detiene en las matrices 2 × 2, que calcula directamente. ¿Cuántos determinantes 2 × 2 evalúa para una matriz n × n? Compara la cuenta para n = 10 con 10³.

> *Solución:* Sea D(n) la cuenta. D(2) = 1, y una matriz n × n hace n llamadas de tamaño n − 1, así que D(n) = n · D(n − 1). Por inducción (MAT-001), D(n) = n!/2: se cumple para n = 2, ya que 2!/2 = 1, y si D(n − 1) = (n − 1)!/2, entonces D(n) = n · (n − 1)!/2 = n!/2. Para n = 10, son 10!/2 = 1,814,400 determinantes de tamaño 2, frente a un número de pasos de eliminación del orden de 10³ = 1000. Para n = 20, 20!/2 es aproximadamente 1.2 × 10^18.

---

## 5. Normas: medir longitudes

Una **norma** asigna una longitud ‖x‖ a cada vector y cumple tres axiomas:
- **Positividad:** ‖x‖ ≥ 0, y ‖x‖ = 0 solo para x = 0.
- **Homogeneidad:** ‖c · x‖ = |c| · ‖x‖ para todo escalar c.
- **Desigualdad triangular:** ‖x + y‖ ≤ ‖x‖ + ‖y‖.

Toda norma da una **distancia** d(x, y) = ‖x − y‖, y la desigualdad triangular de la norma se convierte en la de las distancias: d(x, z) ≤ d(x, y) + d(y, z). Dar un rodeo por y nunca es más corto que ir directamente.

Las **normas p** en Rⁿ son ‖x‖ₚ = (|x₁|ᵖ + … + |xₙ|ᵖ)^(1/p), para p ≥ 1, y ‖x‖∞ = maxᵢ |xᵢ|, que es su límite cuando p crece. Para x = (3, 4):
- ‖x‖₁ = 3 + 4 = 7, la longitud de Manhattan;
- ‖x‖₂ = √(9 + 16) = 5, la longitud euclidiana;
- ‖x‖∞ = 4, la mayor componente.

Para p ≥ 1 se cumple la desigualdad triangular: es la **desigualdad de Minkowski**. Para 0 < p < 1 la misma fórmula sigue dando un número, pero no una norma.

Una matriz también tiene normas. La **inducida** por una norma vectorial es ‖A‖ = max ‖A x‖ / ‖x‖ sobre los x ≠ 0, el mayor factor por el que A estira un vector. Es la norma que está detrás del número de condición de MAT-003.

### Ejercicio práctico

Para p = 1/2, definamos d(x, y) = (|x₁ − y₁|^(1/2) + |x₂ − y₂|^(1/2))². Muestra que viola la desigualdad triangular para x = (0, 0), y = (1, 0) y z = (1, 1).

> *Solución:* d(x, y) = (1 + 0)² = 1 y d(y, z) = (0 + 1)² = 1, mientras que d(x, z) = (1 + 1)² = 4. Así que d(x, z) = 4 > 2 = d(x, y) + d(y, z): dar un rodeo por y es más corto que ir directamente. Este único contraejemplo muestra que la fórmula con p = 1/2 no es una norma.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**Álgebra lineal** (`crates/ix-math/src/linalg.rs`):
- [`matmul`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L8) y [`matvec`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L19) calculan AB y A x, y devuelven `DimensionMismatch` cuando el número de columnas de A no coincide con el otro operando.
- [`trace`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L151) suma la diagonal de una matriz cuadrada.
- [`determinant`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L35) está documentada como «desarrollo en cofactores, adecuado para matrices pequeñas». Su recursión, copiada literalmente de las líneas 43 a 59 de `linalg.rs`, es el algoritmo del ejercicio del §4:

```rust
fn det_recursive(a: &Array2<f64>) -> f64 {
    let n = a.nrows();
    if n == 1 {
        return a[[0, 0]];
    }
    if n == 2 {
        return a[[0, 0]] * a[[1, 1]] - a[[0, 1]] * a[[1, 0]];
    }

    let mut det = 0.0;
    for j in 0..n {
        let minor = minor_matrix(a, 0, j);
        let sign = if j % 2 == 0 { 1.0 } else { -1.0 };
        det += sign * a[[0, j]] * det_recursive(&minor);
    }
    det
}
```

- `linalg.rs` no tiene ninguna función que devuelva una norma matricial. En `ix-math`, la norma de Frobenius solo aparece dentro de algoritmos, como criterio de parada, y como [función auxiliar de prueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L237) en `svd.rs`.

**Distancias** (`crates/ix-math/src/distance.rs`): [`euclidean`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L18), [`manhattan`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L37) y [`chebyshev`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L77) son las distancias de las normas 2, 1 e ∞. [`minkowski`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L46) calcula la distancia p y rechaza p < 1, como muestran las líneas 46 a 57, copiadas literalmente:

```rust
pub fn minkowski(a: &Array1<f64>, b: &Array1<f64>, p: f64) -> Result<f64, MathError> {
    check_same_len(a, b)?;
    if p < 1.0 {
        return Err(MathError::InvalidParameter("p must be >= 1".into()));
    }
    let sum: f64 = a
        .iter()
        .zip(b.iter())
        .map(|(x, y)| (x - y).abs().powf(p))
        .sum();
    Ok(sum.powf(1.0 / p))
}
```

Esta guarda traduce el §5: rechaza todo p menor que 1, donde la fórmula no es una norma. Sin embargo, deja pasar dos valores no finitos: `f64::NAN`, porque toda comparación con NaN es falsa, tras lo cual las potencias devuelven NaN en general, que no es una distancia; y p = ∞, como muestra el ejercicio siguiente. Por eso el contraejemplo con p = 1/2 no puede calcularse con la función `minkowski` de IX, que devuelve un error; es un cálculo a mano, como en el ejercicio del §5.

Las pruebas comprueban ejemplos, no propiedades. [`test_minkowski_equals_euclidean`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L116) compara `minkowski` con p = 2 y `euclidean` en un solo par de puntos, (0, 0) y (3, 4); las demás pruebas de distancia también usan uno o dos pares fijos cada una. Ninguna prueba de `distance.rs` enuncia la desigualdad triangular ni otro axioma de norma. En otra parte de IX, [`test_cpu_triangle_inequality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-gpu/src/distance.rs#L193) la enuncia para la matriz de distancias euclidianas propia del crate de GPU, pero solo comprueba una terna de puntos. Como explica MAT-001, esos ejemplos pueden refutar una propiedad, pero no demostrarla.

**No toda «distancia» es una métrica.** [`cosine_distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L72) devuelve 1 − cos θ, donde θ es el ángulo entre los vectores. No cumple la desigualdad triangular: para x = (1, 0), y = (1, 1) y z = (0, 1), da d(x, z) = 1, pero d(x, y) + d(y, z) = 2 − √2 ≈ 0.59.

### Ejercicio práctico

La guarda de `minkowski` rechaza p < 1, pero deja pasar p = ∞ (`f64::INFINITY`). Usando las reglas habituales de las potencias en punto flotante —x^0 = 1 para todo x y, para p = ∞, t^p vale 0 cuando 0 ≤ t < 1, 1 cuando t = 1 e ∞ cuando t > 1—, predice qué devuelve `minkowski` para p = ∞, y compáralo con `chebyshev`.

> *Solución:* Con p = ∞, cada término |x − y|^p vale 0, 1 o ∞, así que `sum` vale 0, un entero positivo o ∞. El último paso lo eleva a la potencia 1/p = 1/∞ = 0, y x^0 = 1 para todo x, incluidos 0 e ∞. Así que `minkowski` devuelve 1 para cualquier par de vectores, incluso para a = b, donde una distancia debe valer 0. El límite de la distancia p cuando p crece es la distancia ∞, pero sustituir p por ∞ en la fórmula no calcula ese límite: `chebyshev` es la función correcta, y devuelve 0 para a = b y 4 para (0, 0) y (3, 4). Es una predicción deducida de las reglas anteriores, no una ejecución: el experimento del §7 la comprueba.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **La desigualdad triangular en una cuadrícula.** Para los 25 puntos de R² con coordenadas enteras de −2 a 2, comprobar d(x, z) ≤ d(x, y) + d(y, z) en las 15,625 ternas para `manhattan`, `euclidean`, `chebyshev` y `minkowski` con p = 3. Predicción: ninguna violación mayor que 10^-12. Donde los valores exactos son iguales, el redondeo aún puede hacer que los dos lados difieran en sus últimos bits, por lo que la comparación necesita una tolerancia (MAT-003).
2. **p menor que 1.** Llamar a `minkowski` con p = 1/2 sobre los puntos del ejercicio del §5. Predicción: `InvalidParameter("p must be >= 1")`.
3. **p = ∞.** Llamar a `minkowski` con p = `f64::INFINITY` sobre (0, 0) y (0, 0), y sobre (0, 0) y (3, 4). Predicción: 1 en ambos casos, frente a 0 y 4 con `chebyshev`.
4. **p grande.** Llamar a `minkowski` con p = 1000 sobre (0, 0) y (3, 4). Predicción: ∞, porque 3^1000 supera el mayor número binary64, aunque el resultado exacto es algo mayor que 4.
5. **El costo del desarrollo en cofactores.** Medir el tiempo de `determinant` para n = 2 a 11 sobre matrices fijas, y comprobar det(AB) = det A · det B en matrices 3 × 3 con entradas enteras pequeñas. Predicciones: desde n = 3, cada paso multiplica el tiempo por aproximadamente n, como sugiere la cuenta n!/2 del ejercicio del §4; y la regla del producto se cumple exactamente, porque cada valor intermedio es un entero lo bastante pequeño para almacenarse exactamente.

### Ejercicio práctico

El paso 1 comprueba cada terna de la cuadrícula. ¿Demuestra la desigualdad triangular para estas distancias en R²?

> *Solución:* No. La cuadrícula tiene 25 puntos, mientras que R² es infinito, así que la comprobación solo es exhaustiva sobre un subconjunto finito (MAT-001). Lo que demuestra la desigualdad es la desigualdad de Minkowski, para todo p ≥ 1. La comprobación prueba otra cosa: que el código de IX calcula estas distancias sin un error tan grande como para romper la desigualdad en esos puntos.

---

## 8. Errores comunes

- **Multiplicar en el orden equivocado.** En (AB) x la aplicación B actúa primero, y en general AB ≠ BA.
- **Llamar «lineal» a cualquier aplicación.** Una aplicación lineal envía 0 a 0; una traslación, no.
- **Calcular determinantes grandes por desarrollo en cofactores.** El costo crece como n!; la eliminación cuesta del orden de n³.
- **Leer un determinante pequeño como «casi singular».** det(10^-1 · I₂₀) = 10^-20, y sin embargo esta matriz solo multiplica por 10^-1 y tiene número de condición 1 (MAT-003).
- **Tomar cualquier fórmula de distancia por una métrica.** La fórmula p con 0 < p < 1 y la distancia coseno violan ambas la desigualdad triangular.
- **Sustituir p por ∞ en una fórmula.** Un límite no es un valor de la fórmula: usa la propia norma ∞.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Espacio vectorial** | Un conjunto con una suma y una multiplicación por escalares que cumplen las reglas habituales, como Rⁿ |
| **Base** | Una lista de vectores con la que todo vector se escribe como combinación lineal de una única manera |
| **Aplicación lineal** | Una aplicación con L(u + v) = L(u) + L(v) y L(c · v) = c · L(v) |
| **Matriz de una aplicación lineal** | La matriz cuyas columnas son las imágenes de los vectores de la base |
| **Producto de matrices** | La matriz de una composición: (AB) x = A (B x) |
| **Determinante** | El factor con signo por el que una matriz cuadrada multiplica los volúmenes; nulo exactamente cuando la matriz no es invertible |
| **Norma** | Una función longitud positiva, homogénea y que cumple la desigualdad triangular |
| **Norma p** | ‖x‖ₚ = (Σ |xᵢ|ᵖ)^(1/p) para p ≥ 1, y ‖x‖∞ = max |xᵢ| |
| **Desigualdad triangular** | ‖x + y‖ ≤ ‖x‖ + ‖y‖, o para distancias d(x, z) ≤ d(x, y) + d(y, z) |
| **Norma matricial inducida** | ‖A‖ = max ‖A x‖ / ‖x‖ sobre los x ≠ 0: el mayor factor de estiramiento de A |

---

## Autoevaluación

**1. ¿Por qué la aplicación x ↦ x + (1, 0) no es lineal?**
> Una aplicación lineal envía 0 a 0, ya que L(0) = L(0 · 0) = 0 · L(0) = 0. Esta aplicación envía 0 a (1, 0).

**2. ¿Por qué el producto de matrices es asociativo pero no conmutativo?**
> Es la composición de aplicaciones lineales. La composición de funciones siempre es asociativa, así que (AB)C = A(BC). El orden de dos aplicaciones suele importar: la rotación R y la reflexión F del §3 dan RF ≠ FR.

**3. Demuestra que ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ para todo x de Rⁿ.**
> Si la mayor componente en valor absoluto es xₖ, entonces ‖x‖∞² = xₖ² ≤ x₁² + … + xₙ² = ‖x‖₂². Y ‖x‖₁² = (|x₁| + … + |xₙ|)² es la suma de los cuadrados xᵢ² más los productos 2|xᵢ||xⱼ|, que son ≥ 0, así que ‖x‖₁² ≥ ‖x‖₂². Tomando raíces cuadradas de estos números no negativos se obtiene el enunciado.

**4. La función `minkowski` de IX rechaza p = 1/2. ¿Es una limitación o una garantía?**
> Una garantía: por debajo de p = 1 la fórmula no es una norma (§5), y rechazarla deja fuera esos resultados. La guarda no cubre los valores no finitos: deja pasar p = ∞, para el que la fórmula devuelve 1 sean cuales sean los puntos, y `f64::NAN`, para el que devuelve NaN en general (§6).

**Criterio de aprobación:** Escribir vectores en una base, construir la matriz de una aplicación lineal, multiplicar matrices y explicar por qué importa el orden, leer un determinante y contar su costo, y usar los axiomas de norma para distinguir una norma de una fórmula que no lo es, incluso en las funciones de distancia de IX.

---

## Base de investigación

- S. Axler, *Linear Algebra Done Right*, 4.ª ed., Springer, 2024: espacios vectoriales, aplicaciones lineales y sus matrices, determinantes
- G. Strang, *Introduction to Linear Algebra*, 6.ª ed., Wellesley-Cambridge Press, 2023: el producto de matrices como composición, la eliminación, los determinantes y las normas
- G. H. Hardy, J. E. Littlewood y G. Pólya, *Inequalities*, Cambridge University Press, 1934: la desigualdad de Minkowski
- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019: los valores especiales de la función potencia usados en el §6
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
