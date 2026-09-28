---
module_id: mat-006-svd-low-rank-approximation
department: mathematics
course: Descomposición en valores singulares y aproximación de bajo rango
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms, mat-005-symmetric-eigenproblems]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Descomposición en valores singulares y aproximación de bajo rango — La mejor simplificación de una matriz

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Enunciar la descomposición en valores singulares y deducirla del teorema espectral de MAT-005
- Calcular a mano la SVD de una matriz 2 × 2
- Leer la norma, el rango, el número de condición y el determinante de una matriz en sus valores singulares
- Enunciar el teorema de Eckart–Young–Mirsky y calcular el error de una mejor aproximación de rango k
- Elegir una tolerancia de rango relativa al mayor valor singular, y explicar por qué falla una absoluta
- Explicar cómo calcula la SVD el método de Jacobi unilateral, y decir qué garantiza y qué no la implementación de IX

---

## 1. Toda matriz es una rotación, un estiramiento y una rotación

**Descomposición en valores singulares.** Toda matriz real A de tamaño m × n se escribe

A = U Σ Vᵀ,

donde U (m × m) y V (n × n) son ortogonales, y Σ (m × n) es nula salvo en su diagonal, cuyas entradas σ₁ ≥ σ₂ ≥ … ≥ 0 son los **valores singulares**. Las columnas de V son los **vectores singulares derechos**, las de U los **vectores singulares izquierdos**, y A vᵢ = σᵢ uᵢ.

Leída de derecha a izquierda: Vᵀ gira la entrada, Σ la estira a lo largo de los ejes de coordenadas, y U gira el resultado. La esfera unidad se convierte en un elipsoide cuyos semiejes miden σᵢ y apuntan en la dirección de los uᵢ. Con k = min(m, n), la **SVD reducida** conserva solo las k primeras columnas de U y de V; es la forma que devuelve IX.

La SVD se deduce del teorema espectral de MAT-005. La matriz AᵀA es simétrica, y xᵀAᵀAx = ‖Ax‖² ≥ 0, así que sus valores propios λᵢ son reales y no negativos. Tomemos una base ortonormal v₁, …, vₙ de vectores propios, ordenados de modo que λ₁ ≥ λ₂ ≥ … ≥ λₙ, y pongamos σᵢ = √λᵢ. Para i ≠ j, (A vᵢ) · (A vⱼ) = vᵢᵀAᵀA vⱼ = λⱼ (vᵢ · vⱼ) = 0, y ‖A vᵢ‖² = λᵢ = σᵢ². Así, los vectores uᵢ = A vᵢ / σᵢ, para σᵢ > 0, son ortonormales, y A vᵢ = σᵢ uᵢ; completar los uᵢ hasta una base ortonormal da A V = U Σ, es decir, A = U Σ Vᵀ.

A diferencia de los valores propios (MAT-005 §1), los valores singulares existen siempre y son reales y no negativos, para toda matriz: cuadrada o no, simétrica o no.

### Ejercicio práctico

Calcula la SVD de B = [[3, 0], [4, 5]].

> *Solución:* BᵀB = [[3 · 3 + 4 · 4, 3 · 0 + 4 · 5], [0 · 3 + 5 · 4, 0 · 0 + 5 · 5]] = [[25, 20], [20, 25]]. Su traza es 50 y su determinante 625 − 400 = 225, así que sus valores propios son 45, para v₁ = (1, 1)/√2, y 5, para v₂ = (1, −1)/√2. Por tanto σ₁ = √45 = 3√5 y σ₂ = √5. Luego u₁ = B v₁/σ₁ = (3, 9)/(√2 · 3√5) = (1, 3)/√10 y u₂ = B v₂/σ₂ = (3, −1)/(√2 · √5) = (3, −1)/√10, que son ortogonales: 3 − 3 = 0.

---

## 2. Lo que dicen los valores singulares

Los valores singulares resumen una matriz:
- **Norma.** ‖A‖₂ = σ₁: la norma 2 inducida de MAT-004 es el mayor estiramiento.
- **Tamaño.** ‖A‖_F² = σ₁² + σ₂² + …, donde la norma de Frobenius ‖A‖_F es la raíz cuadrada de la suma de los cuadrados de todas las entradas; multiplicar por matrices ortogonales no la cambia.
- **Rango.** El rango de A es el número de valores singulares no nulos.
- **Condicionamiento.** Para A cuadrada invertible, el número de condición de MAT-003 es κ₂(A) = σ₁/σₙ.
- **Volumen.** Para A cuadrada, |det A| = σ₁σ₂…σₙ: U y V conservan longitudes y ángulos, así que conservan los volúmenes, y por la regla del producto de MAT-004 solo Σ los cambia, por el producto de su diagonal.

### Ejercicio práctico

Para la matriz B del §1, da ‖B‖₂, ‖B‖_F, κ₂(B) y |det B| a partir de sus valores singulares, y comprueba dos de ellos directamente.

> *Solución:* ‖B‖₂ = 3√5, ‖B‖_F = √(45 + 5) = √50, κ₂(B) = 3√5/√5 = 3 y |det B| = 3√5 · √5 = 15. Directamente, los cuadrados de las entradas suman 9 + 0 + 16 + 25 = 50, y det B = 3 · 5 − 0 · 4 = 15.

---

## 3. Aproximación de bajo rango

Escrita columna por columna, la SVD es una suma de matrices de rango 1 en orden decreciente de importancia:

A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + … .

Conservar los k primeros términos da el **truncamiento de rango k** A_k.

**Teorema de Eckart–Young–Mirsky.** Para toda matriz X de rango como mucho k, ‖A − X‖₂ ≥ σₖ₊₁ y ‖A − X‖_F ≥ √(σₖ₊₁² + σₖ₊₂² + …), con igualdad para X = A_k.

El error del propio truncamiento se lee fácilmente: A − A_k = σₖ₊₁uₖ₊₁vₖ₊₁ᵀ + … vuelve a estar escrita como una SVD, así que su norma 2 es su mayor valor singular σₖ₊₁, y su norma de Frobenius la raíz cuadrada de la suma de los cuadrados de sus valores singulares. La parte difícil del teorema es que ninguna otra matriz de rango k lo hace mejor; la Base de investigación da las demostraciones. Se siguen dos consecuencias: el error disminuye al crecer k y llega a 0 en k = rango A, y una matriz es «casi de rango k» exactamente cuando σₖ₊₁ es pequeño frente a σ₁. Es lo que usan la compresión, la eliminación de ruido y el análisis semántico latente.

### Ejercicio práctico

Da la mejor aproximación de rango 1 de A = diag(3, 2, 1) y su error en ambas normas. Luego haz lo mismo con la matriz B del §1.

> *Solución:* La SVD de diag(3, 2, 1) es la propia matriz, con U = V = I, así que A₁ = diag(3, 0, 0), con ‖A − A₁‖₂ = 2 y ‖A − A₁‖_F = √(4 + 1) = √5. Para B, B₁ = 3√5 · u₁v₁ᵀ = 3√5 · [[1, 1], [3, 3]]/(√10 · √2) = (3/2) [[1, 1], [3, 3]]. Solo queda σ₂ = √5, así que ambos errores valen √5. Comprobación: B − B₁ = [[3/2, −3/2], [−1/2, 1/2]], cuyas entradas al cuadrado suman 9/4 + 9/4 + 1/4 + 1/4 = 5.

---

## 4. Rango numérico

En aritmética de punto flotante, un valor singular que es cero en aritmética exacta sale en general como un número diminuto no nulo. «El rango es el número de σ no nulos» debe convertirse entonces en «el número de σ por encima de una tolerancia», y la tolerancia debe ser **relativa** a σ₁: multiplicar A por 10^6 multiplica cada valor singular por 10^6 y no cambia el rango. Una convención habitual, la de `matrix_rank` de NumPy, es max(m, n) · σ₁ · ε, donde ε = 2^-52 es el épsilon de máquina de MAT-003. Una tolerancia absoluta mide la escala de la matriz, no su rango.

La misma tolerancia gobierna la **pseudoinversa** A⁺ = V Σ⁺ Uᵀ, donde Σ⁺ invierte los valores singulares por encima de la tolerancia y pone los demás a 0; A⁺b es la solución de mínimos cuadrados de norma mínima. Ahí la elección cuenta doblemente: un valor singular conservado justo por encima de la tolerancia aporta el término enorme 1/σ.

### Ejercicio práctico

Una biblioteca declara nulo todo valor singular inferior a 10^-10. ¿Qué rango informa para 10^-12 · I₃, y cuál informa la convención relativa?

> *Solución:* Los tres valores singulares de 10^-12 · I₃ valen 10^-12, por debajo de 10^-10, así que la biblioteca informa el rango 0 para una matriz de rango 3. La tolerancia relativa es 3 · 10^-12 · ε, unos 6.7 · 10^-28, muy por debajo de 10^-12, así que la convención relativa informa el rango 3. Solo la respuesta relativa sigue igual cuando se cambia la escala de la matriz.

---

## 5. Calcular la SVD con Jacobi unilateral

El **método de Jacobi unilateral** (Hestenes, 1958) nunca forma AᵀA, cuyo número de condición es el cuadrado del de A (MAT-003). Gira pares de columnas de la propia A, lo que multiplica A por la derecha por rotaciones planas, hasta que todas las columnas son ortogonales. En ese momento A V = W, donde V es el producto de las rotaciones y las columnas de W son ortogonales: sus normas son los valores singulares, y las columnas normalizadas forman U.

Para dos columnas a_p y a_q, la rotación es la rotación de Jacobi de MAT-005 §4 aplicada a la matriz 2 × 2 [[a_p · a_p, a_p · a_q], [a_p · a_q, a_q · a_q]], un bloque de AᵀA calculado solo a partir de las dos columnas. Tras la rotación, las dos columnas son ortogonales. Como en MAT-005, una rotación posterior puede estropear una anterior, así que el método barre todos los pares repetidamente.

### Ejercicio práctico

Aplica una rotación a las columnas a_p = (3, 4) y a_q = (0, 5) de la matriz B del §1, con la actualización a_p ← c a_p − s a_q y a_q ← s a_p + c a_q.

> *Solución:* a_p · a_p = 25, a_q · a_q = 25 y a_p · a_q = 20, así que θ = (25 − 25)/(2 · 20) = 0, lo que da t = 1 y c = s = 1/√2. Las nuevas columnas son ((3, 4) − (0, 5))/√2 = (3, −1)/√2 y ((3, 4) + (0, 5))/√2 = (3, 9)/√2. Son ortogonales, ya que 9 − 9 = 0, con normas √10/√2 = √5 y √90/√2 = 3√5: los valores singulares del §1. Normalizarlas da u₂ = (3, −1)/√10 y u₁ = (1, 3)/√10.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**El solucionador** (`crates/ix-math/src/svd.rs`). [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L100) es el método de Jacobi unilateral del §5, con 50 barridos como máximo y una tolerancia de 10^-12. Devuelve la SVD reducida, con los valores singulares en orden decreciente. La prueba que salta un par ya ortogonal es [relativa](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L136) al tamaño de las dos columnas, así que las rotaciones no dependen de la escala de A. El comentario del criterio de parada reivindica la misma propiedad, literal en las líneas 168 a 176:

```rust
        // Scale-invariant stopping criterion: the off-diagonal Frobenius
        // mass should be a small fraction of the matrix's total Frobenius
        // mass. Using an absolute threshold (the old behavior) meant that
        // well-scaled matrices converged in 1-2 sweeps while any matrix
        // with entries much larger than `tol` stayed above the threshold
        // indefinitely.
        if off_diag_sum_sq < tol * tol * a_frob_sq {
            break;
        }
```

Su contrato tiene cuatro límites que conviene conocer:
- **El criterio de parada no es invariante de escala.** `off_diag_sum_sq` suma los cuadrados de los productos a_p · a_q, que son entradas de AᵀA: multiplicar A por s lo multiplica por s⁴. `a_frob_sq` es ‖A‖_F², multiplicado por s². Los dos lados no tienen el mismo grado: el criterio pide √`off_diag_sum_sq` < (10^-12/‖A‖_F) · ‖A‖_F², una tolerancia de 10^-12/‖A‖_F relativa al tamaño de AᵀA, en lugar de 10^-12. Cuando ‖A‖_F es grande, esa tolerancia cae por debajo de lo que suele quedar una vez que el método ha convergido: los pares que la prueba de salto deja sin tocar, cuyo producto está por debajo de 10^-12 en relación con el tamaño de las columnas pero no es cero, y el redondeo (MAT-003). Para una matriz así el criterio no se cumple nunca, y la llamada ejecuta los 50 barridos: el resultado sigue siendo exacto, ya que nada gira más, pero cuesta muchas veces más. Solo unos productos exactamente nulos la detienen aún pronto, como en un múltiplo de la identidad, cuyo primer barrido encuentra `off_diag_sum_sq` = 0. Cuando ‖A‖_F es del orden de 10^-12 o menos, el criterio se cumple al final del primer barrido, lo que, con más de dos columnas, puede dejarlas lejos de ser ortogonales. Comparar `off_diag_sum_sq` con `tol * tol * a_frob_sq * a_frob_sq` daría a ambos lados el grado 4.
- **La promesa no se comprueba.** El comentario de documentación dice [«Guaranteed to converge for any real matrix»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L97). La teoría lo garantiza, pero el [bucle de barridos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L123) se detiene tras 50 barridos, y la función devuelve entonces [`Ok`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L209) se haya cumplido o no el criterio de parada.
- **Queda un umbral absoluto.** Los vectores singulares izquierdos se extraen con el bucle siguiente, literal en las líneas 195 a 207. Una columna de U solo se rellena cuando su valor singular supera `tol`, el 10^-12 absoluto; si no, queda en cero, y `reconstruct` omite entonces ese término. Los valores singulares siguen la escala de A, pero esta prueba no, como el umbral de pivote de `inverse` en MAT-003. El ejercicio de abajo muestra la consecuencia.

```rust
    // Take top-k columns.
    let mut v_sorted = Array2::<f64>::zeros((n, k));
    for (rank, (sig, orig)) in sigma_col.into_iter().take(k).enumerate() {
        singular_values[rank] = sig;
        if sig > tol {
            for i in 0..m {
                u[[i, rank]] = work[[i, orig]] / sig;
            }
        }
        for i in 0..n {
            v_sorted[[i, rank]] = v[[i, orig]];
        }
    }
```

- **Quien llama elige la tolerancia de rango.** [`rank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L67) y [`pseudo_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73) comparan los valores singulares con una tolerancia absoluta `tol` que pasa quien llama, y hacerla relativa le corresponde a quien llama. Dos llamadores lo hacen, de forma distinta. El manejador de la herramienta MCP `ix_svd`, [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L627), usa [σ₁ · 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L639). La prueba de rango del espacio de estados usa [max(m, n) · σ₁ · ε](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L397), la convención del §4, con una [nota](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L395) según la cual la SVD de Jacobi deja un valor singular que es cero en aritmética exacta cerca de 10^-16 · σ₁ en lugar de en 0.

[`truncated_svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L223) calcula la SVD completa y conserva sus k primeras componentes: la A_k del §3. La herramienta MCP `ix_svd` no la ofrece: su [esquema de entrada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L435) recibe una matriz y nada más.

Dos pruebas merecen una mirada más atenta. [`test_svd_scale_invariance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L327) comprueba que multiplicar A [por 10^6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L333) multiplica los valores singulares y mantiene exacta la reconstrucción. Su comentario dice que el criterio relativo corrigió el antiguo, que «would have required many more sweeps to converge (or failed to converge within the default 50)». Las aserciones comprueban la exactitud, no los barridos: ‖10^6 · A‖_F es de unos 10^7, así que según el primer límite de arriba el criterio de parada pide una tolerancia relativa de unos 10^-19, por debajo del nivel de redondeo de MAT-003, y se predice que la llamada ejecuta los 50 barridos, el caso que el comentario presenta como corregido. Además, la prueba solo cambia la escala hacia arriba, mientras que el umbral absoluto de arriba actúa hacia abajo. [`test_truncated_svd_rank_1_approx`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L305) comprueba que el truncamiento de rango 1 de A = [[1, 2], [3, 4], [5, 6]] tiene un error relativo de Frobenius [inferior a 0.10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L315). Eckart–Young da el valor exacto: AᵀA = [[35, 44], [44, 56]] tiene el polinomio característico λ² − 91λ + 24, de raíces (91 ± √8185)/2, así que σ₁ ≈ 9.53, σ₂ ≈ 0.514, ‖A‖_F = √91 y el mejor error relativo es σ₂/√91 ≈ 0.054. La prueba aceptaría también una aproximación hasta 1.8 veces peor que la mejor.

**La pregunta abierta de MAT-003.** En el laboratorio de Learn, MAT-003 midió que el κ₂ de IX de las matrices de Hilbert almacenadas fl(H_2) a fl(H_16) cambia, para 10 de los 15 tamaños, cuando la matriz se multiplica por 2^-20 o 2^20, y dejó abierta la causa. El criterio de parada la explica. Multiplicar por una potencia de dos es exacto, y mientras nada produzca desbordamiento por abajo o por arriba, como aquí, también lo es cada operación de `svd` sobre la matriz escalada: cada producto, cada rotación y cada decisión de salto es la de fl(H_n), multiplicada por una potencia de dos. Solo puede cambiar el número de barridos, y donde los barridos adicionales aún giran columnas, los bits cambian. Una transcripción de `svd` en Python que sigue el orden de suma de `ndarray` predice de 2 a 4 barridos a 2^-20, de 2 a 6 a escala 1, y los 50 a 2^20. Reproduce los 15 valores de κ₂ que imprimió el laboratorio, con las tres cifras impresas, y su recuento de 5 tamaños idénticos de 15. Es un análisis, no una ejecución de IX; el paso 4 del §7 permite al laboratorio comprobarlo con [`svd_with_opts`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L105), que limita el número de barridos.

### Ejercicio práctico

Con A = [[1, 2], [3, 4], [5, 6]], predice qué devuelven `svd(10^-13 · A).reconstruct()` y `svd(10^-12 · A).reconstruct()`.

> *Solución:* A tiene dos columnas, así que una sola rotación las vuelve ortogonales, decida lo que decida el criterio de parada, y esa rotación solo depende de cocientes entre los productos de las columnas: es la rotación usada para A. Los valores singulares salen, por tanto, como los de A multiplicados por la escala, salvo redondeo. Para 10^-13 · A valen unos 9.53 · 10^-13 y 5.14 · 10^-14, ambos por debajo de 10^-12: las dos columnas de U quedan en cero, y `reconstruct` devuelve la matriz nula, un error relativo de 1. Para 10^-12 · A valen unos 9.53 · 10^-12, conservado, y 5.14 · 10^-13, descartado: `reconstruct` devuelve en silencio el truncamiento de rango 1, con un error relativo de unos 0.054, que es exactamente el error de Eckart–Young de la prueba anterior y parece plausible. Es una predicción obtenida leyendo el código, no una ejecución; el §7 la comprueba.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **Eckart–Young para cada k.** Sobre A = [[1, 2], [3, 4], [5, 6]] y sobre M = [[1, 2, 3], [4, 5, 6], [7, 8, 10]], la matriz de la [prueba MCP](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L1311) de IX, calcula ‖A − A_k‖_F con `truncated_svd` para cada k, y compárala con √(σₖ₊₁² + …) calculada a partir de `svd`. Predicción: iguales salvo 10^-9 · ‖A‖_F, decrecientes en k, y nulas salvo redondeo en k = rango A.
2. **Un barrido de escalas.** Para s = 10^-14, 10^-13, …, 10^12, calcula los valores singulares de s · A y de s · M divididos entre s, y el error relativo de `reconstruct`. Predicción para A: los valores singulares coinciden con los de A salvo 10^-12 en relativo en todas las escalas; el error relativo es inferior a 10^-12 para s ≥ 10^-11, unos 0.054 para s = 10^-12, y exactamente 1 para s ≤ 10^-13. Predicción para M: los valores singulares coinciden salvo 10^-12 en relativo para s ≥ 10^-10; para s ≤ 10^-13, donde el bucle se detiene tras el primer barrido, al menos uno de ellos está equivocado en más de un 100 %.
3. **El coste de la escala.** Cronometra muchas llamadas de `svd` sobre A y sobre 10^6 · A, y sobre M y 10^6 · M. Predicción: las llamadas escaladas tardan varias veces más, ya que ejecutan los 50 barridos.
4. **El enigma de MAT-003.** Para n = 2 a 16, calcula `svd_with_opts(2^20 · fl(H_n), k, 10^-12)` para k = 1 a 6 y divide sus valores singulares entre 2^20. A esa escala el criterio de parada no se cumple nunca, así que se ejecutan exactamente k barridos. Predicción: el resultado reproduce bit a bit los valores singulares de `svd(fl(H_n))` para un primer valor de k, y los de `svd(2^-20 · fl(H_n))` divididos entre 2^-20 para un segundo: k = 2 y 2 para n = 2, 4 y 3 para n = 3 a 6, 5 y 4 para n = 7 a 14, y 6 y 4 para n = 15 y 16.
5. **Convenciones de rango.** Llama a `ix_svd` sobre [[1, 2], [2, 4]]. Predicción: rango 1. Llama a `rank` con la tolerancia 10^-10 sobre la SVD de 10^-12 · I₃. Predicción: 0, frente a 3 con la convención relativa del §4.
6. **La cota de la prueba.** Calcula el error relativo del truncamiento de rango 1 de la matriz de la prueba. Predicción: 0.054 con tres decimales, frente a la cota 0.10 que comprueba la prueba.

### Ejercicio práctico

Supón que el paso 2 confirma que los valores singulares de s · A son proporcionales a s en todas las escalas. ¿Por qué no basta eso para fiarse de `svd` en todas las escalas?

> *Solución:* Primero, los valores singulares pueden ser correctos mientras U está mal: por debajo de 10^-12, las columnas de U quedan en cero aunque los valores singulares sean correctos. Segundo, A solo tiene dos columnas, así que una rotación lo resuelve todo, y una parada prematura tras el primer barrido no puede verse ahí; M, con tres columnas, debería mostrarla. Una comprobación fiable prueba los invariantes de la descomposición entera, A = U Σ Vᵀ y columnas de U ortonormales para cada valor singular no nulo, como en MAT-005 §5, sobre matrices de más de dos columnas, y en todas las escalas, no solo en la que usan las pruebas.

---

## 8. Errores comunes

- **Calcular los valores singulares como raíces cuadradas de los valores propios de AᵀA.** Formar AᵀA eleva al cuadrado el número de condición, y los valores singulares pequeños pierden precisión primero.
- **Usar un umbral de rango absoluto.** Mide la escala de la matriz, no su rango.
- **Fiarse solo de los valores singulares.** U y V pueden estar mal mientras los valores singulares son correctos: comprueba A = U Σ Vᵀ.
- **Probar una cantidad conocida con una cota holgada.** Cuando un teorema da el error exacto, una prueba con una cota casi el doble de grande deja pasar errores.
- **Confundir valores singulares y valores propios.** Para una matriz simétrica, los valores singulares son los valores absolutos de los valores propios, pero no en general: el cizallamiento de la autoevaluación 2 tiene los valores propios 1 y 1.
- **Comparar cantidades de grados distintos.** Una prueba solo es invariante de escala si sus dos lados escalan igual: una suma de cuadrados de entradas de AᵀA tiene grado 4 en A, ‖A‖_F² grado 2.
- **Tomar un comentario por una garantía.** «Guaranteed to converge» es un teorema sobre el método, y «scale-invariant» una afirmación sobre el código; el código aún tiene que informar de lo primero, y una prueba que comprobar lo segundo.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Descomposición en valores singulares** | A = U Σ Vᵀ, con U y V ortogonales y Σ diagonal con entradas σ₁ ≥ σ₂ ≥ … ≥ 0 |
| **Valores singulares** | Las entradas diagonales de Σ: las raíces cuadradas de los valores propios de AᵀA |
| **Vectores singulares izquierdos y derechos** | Las columnas uᵢ de U y vᵢ de V, con A vᵢ = σᵢ uᵢ |
| **SVD reducida** | La SVD que conserva solo las min(m, n) primeras columnas de U y de V |
| **Norma de Frobenius** | ‖A‖_F, la raíz cuadrada de la suma de los cuadrados de todas las entradas, igual a √(σ₁² + σ₂² + …) |
| **Truncamiento de rango k** | A_k = σ₁u₁v₁ᵀ + … + σₖuₖvₖᵀ |
| **Teorema de Eckart–Young–Mirsky** | A_k es una mejor aproximación de rango como mucho k, con errores σₖ₊₁ en norma 2 y √(σₖ₊₁² + …) en norma de Frobenius |
| **Rango numérico** | El número de valores singulares por encima de una tolerancia relativa a σ₁ |
| **Pseudoinversa** | A⁺ = V Σ⁺ Uᵀ, que invierte los valores singulares por encima de la tolerancia |
| **Jacobi unilateral** | Girar pares de columnas de A hasta que sean ortogonales; sus normas son los valores singulares |

---

## Autoevaluación

**1. ¿Por qué los valores singulares de toda matriz real son reales y no negativos, cuando sus valores propios pueden no serlo?**
> Son las raíces cuadradas de los valores propios de AᵀA, que es simétrica, así que sus valores propios son reales (MAT-005), y que cumple xᵀAᵀAx = ‖Ax‖² ≥ 0, así que son no negativos.

**2. El cizallamiento S = [[1, 1], [0, 1]] tiene el valor propio 1, dos veces. ¿Cuáles son sus valores singulares, y cuánto vale κ₂(S)?**
> SᵀS = [[1, 1], [1, 2]] tiene el polinomio característico λ² − 3λ + 1, de raíces (3 ± √5)/2. Sus raíces cuadradas son σ₁ = (1 + √5)/2, el número áureo, y σ₂ = (√5 − 1)/2, su inverso, ya que ((1 ± √5)/2)² = (3 ± √5)/2. Así κ₂(S) = σ₁/σ₂ = (3 + √5)/2, unos 2.62, aunque ambos valores propios valen 1: para una matriz no simétrica, los valores propios no muestran el condicionamiento.

**3. ¿Por qué el error en norma 2 de la mejor aproximación de rango k es σₖ₊₁ y no √(σₖ₊₁² + σₖ₊₂² + …)?**
> Los valores singulares de A − A_k son σₖ₊₁, σₖ₊₂, …, y la norma 2 de una matriz es su mayor valor singular, σₖ₊₁. La norma de Frobenius suma los cuadrados de todos ellos.

**4. La prueba `test_svd_scale_invariance` de IX pasa. ¿Qué garantiza sobre la escala, y qué se le escapa?**
> Comprueba que escalar hacia arriba por 10^6 mantiene exactos los valores singulares y la reconstrucción. Se le escapa el coste: a esa escala el criterio de parada no se cumple nunca, y se predice que la llamada ejecuta los 50 barridos. También se le escapa la reducción de escala, donde el umbral absoluto de 10^-12 sobre los valores singulares deja columnas de U en cero, y `reconstruct` omite términos en silencio (§6).

**Criterio de aprobación:** Deducir y calcular una SVD a mano, leer la norma, el rango, el condicionamiento y el determinante en los valores singulares, calcular las mejores aproximaciones de bajo rango y sus errores, elegir una tolerancia de rango relativa, aplicar una rotación de Jacobi unilateral, y detectar dónde la SVD de IX depende de la escala de su entrada.

---

## Base de investigación

- C. Eckart y G. Young, «The approximation of one matrix by another of lower rank», *Psychometrika* 1, 1936: la mejor aproximación de bajo rango en norma de Frobenius
- L. Mirsky, «Symmetric gauge functions and unitarily invariant norms», *Quarterly Journal of Mathematics* 11, 1960: el mismo resultado para toda norma unitariamente invariante, incluida la norma 2
- M. R. Hestenes, «Inversion of matrices by biorthogonalization and related results», *Journal of the Society for Industrial and Applied Mathematics* 6, 1958: el método de Jacobi unilateral
- J. Demmel y K. Veselić, «Jacobi's method is more accurate than QR», *SIAM Journal on Matrix Analysis and Applications* 13, 1992: la precisión de los métodos de Jacobi
- L. N. Trefethen y D. Bau, *Numerical Linear Algebra*, SIAM, 1997, lecciones 4 y 5: la SVD, su geometría y la aproximación de bajo rango
- G. H. Golub y C. F. Van Loan, *Matrix Computations*, 4.ª ed., Johns Hopkins University Press, 2013, caps. 2 y 8: la SVD, el rango numérico y los métodos de Jacobi para la SVD
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
