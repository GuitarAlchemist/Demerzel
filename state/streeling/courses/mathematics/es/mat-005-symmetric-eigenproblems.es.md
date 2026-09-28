---
module_id: mat-005-symmetric-eigenproblems
department: mathematics
course: Problemas de valores propios simétricos
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Problemas de valores propios simétricos — Las direcciones que una matriz solo estira

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Hallar a mano los valores propios y los vectores propios de una matriz 2 × 2
- Enunciar el teorema espectral para matrices simétricas reales, demostrar sus pasos clave y mostrar con contraejemplos lo que falla sin simetría
- Usar el cociente de Rayleigh para acotar los valores propios y para estimar uno a partir de un vector propio aproximado
- Aplicar una rotación de Jacobi y explicar por qué converge el método de Jacobi cíclico
- Explicar por qué un valor propio múltiple determina su subespacio propio pero no sus vectores propios, y comprobar correctamente un resultado así
- Explicar cuándo falla el método de la potencia, y decir qué garantizan y qué no los solucionadores de valores propios de IX

---

## 1. Valores propios y vectores propios

Un vector no nulo v es un **vector propio** de una matriz cuadrada A, con **valor propio** λ, si

A v = λ v.

En la dirección de v, A solo estira, por el factor λ, e invierte el sentido si λ < 0. Como A v = λ v significa (A − λI) v = 0 con v ≠ 0, la matriz A − λI no es invertible, así que λ es una raíz del **polinomio característico** det(A − λI) (MAT-004). Para una matriz 2 × 2, este polinomio es

λ² − (tr A) λ + det A,

donde la traza tr A es la suma de las entradas diagonales. Para A = [[2, 1], [1, 2]], vale λ² − 4λ + 3 = (λ − 3)(λ − 1): los valores propios son 3, para v = (1, 1), y 1, para v = (1, −1).

Dos contraejemplos muestran que una matriz real no siempre da una imagen tan limpia:
- **Ningún valor propio real.** La rotación de 90° de MAT-004, R = [[0, −1], [1, 0]], tiene el polinomio característico λ² + 1, que no tiene raíces reales: ninguna dirección del plano queda simplemente estirada por un cuarto de vuelta.
- **Demasiado pocos vectores propios.** El cizallamiento [[1, 1], [0, 1]] tiene el valor propio doble 1, pero solo los múltiplos de (1, 0) son vectores propios, así que ninguna base de R² está formada por sus vectores propios.

### Ejercicio práctico

Halla los valores propios y los vectores propios de A = [[5, 2], [2, 2]], y comprueba que los vectores propios son ortogonales.

> *Solución:* tr A = 7 y det A = 10 − 4 = 6, así que el polinomio característico es λ² − 7λ + 6 = (λ − 6)(λ − 1). Para λ = 6, A − 6I = [[−1, 2], [2, −4]], cuyas dos filas dicen x = 2y: v = (2, 1), y en efecto A (2, 1) = (12, 6) = 6 · (2, 1). Para λ = 1, A − I = [[4, 2], [2, 1]], cuyas dos filas dicen y = −2x: w = (1, −2), y A (1, −2) = (1, −2). Por último, v · w = 2 − 2 = 0.

---

## 2. El teorema espectral

Una matriz es **simétrica** si Aᵀ = A, es decir, si su entrada en la fila i y la columna j es igual a la de la fila j y la columna i. Los dos contraejemplos del §1 no son simétricos, y no es casualidad:

**Teorema espectral.** Una matriz simétrica real A de tamaño n × n tiene n valores propios reales, contados con multiplicidad, y una base ortonormal de vectores propios. De forma equivalente, A = Q Λ Qᵀ, donde Q es **ortogonal** (QᵀQ = I; sus columnas son los vectores propios) y Λ es la matriz diagonal de los valores propios.

En la base de sus vectores propios, una matriz simétrica es solo un escalado a lo largo de ejes perpendiculares. Dos pasos de la demostración son cortos:
- **Los vectores propios de valores propios distintos son ortogonales.** Si A u = λ u y A v = μ v con λ ≠ μ, entonces λ (u · v) = (A u) · v = u · (A v) = μ (u · v), donde la igualdad del medio usa Aᵀ = A. Así, (λ − μ)(u · v) = 0, y u · v = 0.
- **Los valores propios son reales.** Si A x = λ x para un vector complejo x ≠ 0, entonces λ ‖x‖² = x̄ᵀ A x, y x̄ᵀ A x es igual a su propio conjugado porque A es real y simétrica. Así que λ es real.

El paso restante, que hay suficientes vectores propios incluso cuando los valores propios se repiten, es una inducción sobre n (MAT-001); el libro de Axler, en la Base de investigación, la da.

### Ejercicio práctico

Con los vectores propios del ejercicio del §1, toma Q = (1/√5) [[2, 1], [1, −2]] y Λ = diag(6, 1), y comprueba que Q Λ Qᵀ = [[5, 2], [2, 2]].

> *Solución:* Las columnas (2, 1)/√5 y (1, −2)/√5 tienen longitud 1 y son ortogonales, así que Q es ortogonal, y aquí Qᵀ = Q. Luego [[2, 1], [1, −2]] · diag(6, 1) = [[12, 1], [6, −2]], y [[12, 1], [6, −2]] · [[2, 1], [1, −2]] = [[25, 10], [10, 10]]. Los dos factores 1/√5 dan 1/5, y (1/5) · [[25, 10], [10, 10]] = [[5, 2], [2, 2]].

---

## 3. El cociente de Rayleigh

Para una matriz simétrica A y un vector x ≠ 0, el **cociente de Rayleigh** es

R(x) = (xᵀ A x) / (xᵀ x).

Si x es un vector propio con valor propio λ, entonces R(x) = λ. En general, escribamos x = c₁q₁ + … + cₙqₙ en una base ortonormal de vectores propios, con valores propios λ₁ ≥ … ≥ λₙ. Entonces

R(x) = (λ₁c₁² + … + λₙcₙ²) / (c₁² + … + cₙ²),

un promedio ponderado de los valores propios. De ahí salen dos consecuencias:
- **Cotas.** λₙ ≤ R(x) ≤ λ₁ para todo x ≠ 0, con igualdad en los vectores propios: el mayor valor propio es el máximo de R, y el menor es su mínimo. Para una matriz simétrica, la norma 2 inducida de MAT-004 es el mayor |λᵢ|.
- **Precisión.** Si x está cerca de un vector propio, R(x) está mucho más cerca de su valor propio: un error de orden ε en la dirección de x da un error de orden ε² en R(x).

### Ejercicio práctico

Para A = diag(3, 1) y x = (1, 1/10), calcula R(x) y su distancia al valor propio 3.

> *Solución:* xᵀ A x = 3 · 1 + 1 · 1/100 = 301/100 y xᵀ x = 101/100, así que R(x) = 301/101. Su distancia a 3 es 3 − 301/101 = 2/101, unos 0.02, mientras que la dirección de x se aparta del vector propio (1, 0) un ángulo de unos 1/10. El error en el valor propio es aproximadamente el doble del cuadrado del error en la dirección, como dice la segunda consecuencia.

---

## 4. Las rotaciones de Jacobi

En 1846, Jacobi propuso diagonalizar una matriz simétrica mediante una sucesión de rotaciones planas. Cada paso elige un par de índices p < q y reemplaza A por JᵀAJ, donde J gira el plano de las coordenadas p y q un ángulo elegido para anular la nueva entrada a_pq. Como J es ortogonal, JᵀAJ tiene los mismos valores propios que A.

Para el bloque 2 × 2 [[a_pp, a_pq], [a_pq, a_qq]] con a_pq ≠ 0, tomemos θ = (a_qq − a_pp) / (2a_pq). La tangente t del ángulo de rotación es una raíz de t² + 2θt − 1 = 0, y la raíz de menor valor absoluto, t = sign(θ) / (|θ| + √(1 + θ²)), mantiene pequeña la rotación. Con c = 1/√(1 + t²) y s = t c, la rotación da las nuevas entradas diagonales

a_pp − t a_pq y a_qq + t a_pq,

y un cero en la posición (p, q).

Por qué converge el método: una semejanza ortogonal conserva la suma de los cuadrados de todas las entradas. La rotación convierte las dos entradas fuera de la diagonal a_pq en ceros y pasa su peso a la diagonal, así que la suma de los cuadrados fuera de la diagonal baja exactamente 2a_pq². Una rotación posterior puede volver a hacer no nula una entrada ya anulada; por eso el **método de Jacobi cíclico** recorre todos los pares una y otra vez. La suma fuera de la diagonal sigue disminuyendo, y el método converge, al final de forma cuadrática (Golub y Van Loan, cap. 8). El producto V = J₁J₂J₃… de las rotaciones contiene los vectores propios en sus columnas.

### Ejercicio práctico

Aplica una rotación de Jacobi a A = [[5, 2], [2, 2]].

> *Solución:* θ = (2 − 5)/(2 · 2) = −3/4, así que √(1 + θ²) = √(25/16) = 5/4 y t = −1/(3/4 + 5/4) = −1/2. Las nuevas entradas diagonales son 5 − (−1/2) · 2 = 6 y 2 + (−1/2) · 2 = 1, y la entrada fuera de la diagonal es 0. Una sola rotación diagonaliza cualquier matriz simétrica 2 × 2: aquí encuentra los valores propios 6 y 1 del §1, y la suma de cuadrados fuera de la diagonal pasa de 2 · 2² = 8 a 0.

---

## 5. Valores propios múltiples

Cuando un valor propio se repite, su **subespacio propio**, el conjunto de todos los v con A v = λ v, tiene dimensión mayor que 1; para una matriz simétrica, esa dimensión es igual a la multiplicidad. Toda base ortonormal del subespacio propio es entonces un conjunto de vectores propios igual de correcto.

Tomemos B = I + J, donde J es la matriz 3 × 3 de unos. Como J (1, 1, 1) = 3 · (1, 1, 1), y J v = 0 siempre que las componentes de v sumen 0, B tiene el valor propio 4 para (1, 1, 1) y el valor propio doble 1 en todo el plano de los vectores cuyas componentes suman 0. Dos vectores ortonormales cualesquiera de ese plano son una respuesta correcta.

Lo que es único es el subespacio propio, y con él el **proyector ortogonal** sobre ese subespacio, P = uuᵀ + wwᵀ, que no depende de la base ortonormal u, w elegida. Por eso una prueba de un solucionador de valores propios debe comprobar **invariantes**, A v = λ v, VᵀV = I y A = V Λ Vᵀ, o comparar proyectores, y nunca comparar los vectores propios con una lista esperada fija: incluso un vector propio simple solo está determinado salvo el signo.

Los valores propios están bien condicionados (MAT-003): sumar una matriz simétrica E a una matriz simétrica mueve cada valor propio como mucho ‖E‖₂, que es la desigualdad de Weyl. Los vectores propios no: cuando dos valores propios están cerca, un cambio pequeño de la matriz puede girar mucho sus vectores propios dentro del plano que generan.

### Ejercicio práctico

Comprueba que u = (1, −1, 0)/√2 y w = (1, 1, −2)/√6 son vectores propios ortonormales de B = I + J para el valor propio 1, y que uuᵀ + wwᵀ = I − J/3.

> *Solución:* Las componentes de u, y las de w, suman 0, así que J u = J w = 0, de donde B u = u y B w = w. Además u · w = (1 − 1 + 0)/√12 = 0, ‖u‖² = 2/2 = 1 y ‖w‖² = 6/6 = 1. Luego uuᵀ = (1/2) [[1, −1, 0], [−1, 1, 0], [0, 0, 0]] y wwᵀ = (1/6) [[1, 1, −2], [1, 1, −2], [−2, −2, 4]]. Su suma tiene 1/2 + 1/6 = 2/3 o 0 + 4/6 = 2/3 en la diagonal, y −1/2 + 1/6 = −1/3 o 0 − 2/6 = −1/3 fuera de ella: es I − J/3, cuyas entradas diagonales valen 1 − 1/3 = 2/3 y las demás −1/3. Otra base ortonormal del plano da la misma matriz.

---

## 6. El método de la potencia y su punto ciego

El **método de la potencia** es el más sencillo de los solucionadores de valores propios: se parte de un vector unitario v₀, se repite v ← A v / ‖A v‖, y se estima el valor propio con el cociente de Rayleigh de v. Si v₀ = c₁q₁ + … + cₙqₙ y |λ₁| > |λ₂| ≥ …, entonces

Aᵏ v₀ = c₁λ₁ᵏ q₁ + … + cₙλₙᵏ qₙ,

y el primer término se impone, con un error que disminuye como |λ₂/λ₁|ᵏ, **siempre que c₁ ≠ 0**. Dos cosas pueden salir mal:
- **Un arranque ciego.** Si v₀ es ortogonal a q₁, entonces c₁ = 0, y en aritmética exacta la iteración nunca encuentra q₁. El redondeo puede introducir una componente diminuta a lo largo de q₁, que luego necesita muchos pasos para crecer.
- **Un criterio de parada que no puede distinguir.** «Parar cuando la estimación deja de cambiar» se cumple tanto con una iteración atascada en el vector propio equivocado como con una que ha convergido al correcto.

Para hallar el siguiente par propio, la **deflación** reemplaza A por A − λ₁ v vᵀ, lo que lleva el valor propio encontrado a 0; cualquier error en el primer par se transmite al siguiente.

### Ejercicio práctico

Aplica el método de la potencia a A = [[2, −1], [−1, 2]] desde v₀ = (1, 1)/√2. ¿Qué valor propio anuncia, y cuál es el mayor?

> *Solución:* A (1, 1) = (1, 1), así que v₀ es un vector propio para el valor propio 1. Cada paso devuelve el propio v₀, el cociente de Rayleigh vale 1 en cada paso, y un criterio sobre su variación se detiene enseguida y anuncia 1. Pero A (1, −1) = (3, −3): el mayor valor propio es 3, para (1, −1)/√2, que es ortogonal a v₀. La iteración era ciega a él desde el principio.

---

## 7. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**El solucionador simétrico** (`crates/ix-math/src/eigen.rs`). [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L46) es el método de Jacobi cíclico del §4, con 100 barridos como máximo y una tolerancia de 10^-12. Devuelve los valores propios en orden decreciente y los vectores propios como columnas de una matriz. Su rotación, como muestran las líneas 92 a 109, copiadas literalmente, es la fórmula del §4:

```rust
                let app = m[[p, p]];
                let aqq = m[[q, q]];
                // Compute Jacobi rotation angle that zeros the (p, q) entry
                // of the 2x2 submatrix [[app, apq], [apq, aqq]].
                let theta = (aqq - app) / (2.0 * apq);
                let t = if theta >= 0.0 {
                    1.0 / (theta + (1.0 + theta * theta).sqrt())
                } else {
                    1.0 / (theta - (1.0 + theta * theta).sqrt())
                };
                let c = 1.0 / (1.0 + t * t).sqrt();
                let s = t * c;

                // Update diagonal entries and zero the off-diagonal.
                m[[p, p]] = app - t * apq;
                m[[q, q]] = aqq + t * apq;
                m[[p, q]] = 0.0;
                m[[q, p]] = 0.0;
```

Su contrato tiene tres límites que conviene conocer:
- **No comprueba la simetría.** Rechaza una entrada vacía o [no cuadrada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L64), pero lee las entradas por encima de la diagonal como si la matriz fuera simétrica. El ejercicio siguiente muestra qué devuelve entonces.
- **No informa de la convergencia.** El [bucle de barridos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L74) termina tras 100 barridos como máximo, y la función devuelve entonces [`Ok`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L151), se haya alcanzado o no la tolerancia.
- **Su criterio de parada no es el que anuncia su comentario.** El comentario habla de la norma de Frobenius de la parte fuera de la diagonal, pero el [bucle](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L78) solo suma los cuadrados por encima de la diagonal. Para una matriz simétrica, eso es la mitad de la suma de cuadrados fuera de la diagonal, así que el umbral real sobre esa norma es √2 · 10^-12: inofensivo aquí, y un recordatorio de que hay que leer el código y no el comentario.

Las pruebas comprueban el tipo correcto de propiedad. [`test_eigenvectors_are_orthonormal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L189) y [`test_reconstruction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L210) comprueban VᵀV = I y A = V Λ Vᵀ, los invariantes del §5, en una matriz 3 × 3. [`test_repeated_eigenvalues`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L231), en cambio, usa la identidad 4 × 4: su parte fuera de la diagonal ya es nula, así que el bucle se detiene antes de la primera rotación y devuelve la identidad de la que partió. La prueba pasa sin ejercitar ni una rotación sobre un valor propio múltiple; una matriz como la I + J del §5 forzaría rotaciones.

**Dos llamadores, dos maneras de cumplir la precondición.** El manejador de la herramienta MCP `ix_eigen`, [`eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L469), rechaza las [entradas no finitas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L483) y cualquier asimetría mayor que una [tolerancia relativa](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L491) de 10^-9, y [`eigen_rejects_non_symmetric`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L1173) prueba ese rechazo con [[1, 2], [3, 4]]. El optimizador CMA-ES, en cambio, [reemplaza su matriz de covarianza C por (C + Cᵀ)/2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-acoustic-tune/src/cmaes.rs#L181) antes de llamar al solucionador; la pregunta 3 de la autoevaluación muestra por qué es la reparación correcta.

**El PCA simple no usa este solucionador.** El comentario de módulo de `eigen.rs` pide al resto del espacio de trabajo que [lo llame](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L8) en vez de duplicarlo, pero `crates/ix-unsupervised/src/pca.rs` todavía extrae las componentes principales con el método de la potencia y [deflación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L141). Su método de la potencia, como muestran las líneas 103 a 137, copiadas literalmente:

```rust
fn power_iteration(matrix: &Array2<f64>, max_iter: usize, tol: f64) -> (f64, Array1<f64>) {
    let n = matrix.nrows();

    // Initialize with a non-zero vector
    let mut v = Array1::from_elem(n, 1.0 / (n as f64).sqrt());

    let mut eigenvalue = 0.0;

    for _ in 0..max_iter {
        // Multiply: v_new = M * v
        let v_new = matrix.dot(&v);

        // Compute eigenvalue (Rayleigh quotient)
        let new_eigenvalue = v.dot(&v_new);

        // Normalize
        let norm = v_new.dot(&v_new).sqrt();
        if norm < 1e-15 {
            break;
        }
        let v_normalized = &v_new / norm;

        // Check convergence
        if (new_eigenvalue - eigenvalue).abs() < tol {
            eigenvalue = new_eigenvalue;
            v = v_normalized;
            break;
        }

        eigenvalue = new_eigenvalue;
        v = v_normalized;
    }

    (eigenvalue, v)
}
```

El vector de partida es siempre (1, …, 1)/√n, y el bucle se detiene cuando la estimación de Rayleigh cambia menos de `tol`, que [`fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L176) fija en 10^-10: son los dos puntos ciegos del §6. Consideremos los seis puntos (1, −1), (−1, 1), (1, 0), (−1, 0), (0, 1) y (0, −1). Su media es 0 y su matriz de covarianza es [[4, −2], [−2, 4]]/5, con el valor propio 6/5 para (1, −1)/√2 y 2/5 para (1, 1)/√2. El vector de partida (1, 1)/√2 es el vector propio del menor, como en el ejercicio del §6. Tras la deflación, la matriz está cerca de [[3/5, −3/5], [−3/5, 3/5]], que lleva el vector de partida casi a cero, así que la segunda llamada debería detenerse en su primera prueba de norma, conservando el vector de partida y la estimación 0. Nuestra lectura del código predice, por tanto, que `PCA` con dos componentes devuelve (1, 1)/√2 como primera componente, con varianza 2/5, y de nuevo el mismo vector como segunda, con varianza 0. Un par así fallaría [`test_pca_components_orthogonal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L288), que comprueba la ortogonalidad con otro conjunto de datos. Los valores propios 6/5 y 2/5 están bien separados: el fallo viene del vector de partida fijo, no de valores propios cercanos. Es una predicción, no una ejecución (§8), y una limitación del código fijado que corresponde corregir a los responsables de IX, no un comportamiento que copiar.

### Ejercicio práctico

Recorre a mano `symmetric_eigen` sobre la matriz no simétrica A = [[1, 2], [3, 4]]. ¿Qué devuelve, y cómo detectaría el problema una comprobación de A v = λ v?

> *Solución:* El primer barrido tiene un solo par, (0, 1). El bucle lee a_pq = 2, la entrada por encima de la diagonal, con a_pp = 1 y a_qq = 4, así que θ = 3/(2 · 2) = 3/4, √(1 + θ²) = 5/4 y t = 1/(3/4 + 5/4) = 1/2. La nueva diagonal vale 1 − (1/2) · 2 = 0 y 4 + (1/2) · 2 = 5, las entradas fuera de la diagonal se ponen a 0, y el barrido siguiente se detiene. La función devuelve los valores propios (5, 0), sin error: son los valores propios de [[1, 2], [2, 4]], la matriz cuya entrada inferior copia la superior. Los verdaderos valores propios de A son (5 ± √33)/2, unos 5.37 y −0.37. Para λ = 5 el vector devuelto es v = (1, 2)/√5, y A v = (5, 11)/√5 ≠ 5 v = (5, 10)/√5: el residuo A v − λ v = (0, 1)/√5 está lejos de 0. Los valores de los que dependen los valores propios, θ, √(1 + θ²), t y la nueva diagonal, son todos exactos en binary64, así que esta lectura predice exactamente (5, 0); el §8 lo comprueba.

---

## 8. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **Los invariantes.** Llamar a `symmetric_eigen` con [[5, 2], [2, 2]], con la matriz 3 × 3 de las propias pruebas de IX y con I + J de tamaños 3 y 4. Comprobar A v = λ v, VᵀV = I y A = V Λ Vᵀ entrada por entrada con una tolerancia de 10^-9, la de las pruebas de IX. Predicción: todo se cumple, con los valores propios 6 y 1, luego 4, 1, 1, y luego 5, 1, 1, 1.
2. **El subespacio propio, no los vectores.** Para I + J de tamaño 3, construir uuᵀ + wwᵀ con los dos vectores propios devueltos para el valor propio 1, y compararlo con I − J/3. Predicción: iguales con una tolerancia de 10^-9, sean cuales sean los vectores que elija el solucionador.
3. **Una entrada no simétrica.** Llamar a `symmetric_eigen` con [[1, 2], [3, 4]]. Predicción: exactamente (5, 0), sin error. Llamar a `ix_eigen` con la misma matriz. Predicción: un error cuyo mensaje contiene «symmetric».
4. **El punto ciego del PCA.** Ajustar `PCA` con dos componentes sobre los seis puntos del §7. Predicción: las dos componentes valen (1, 1)/√2 salvo el signo y el redondeo, las varianzas son cercanas a 2/5 y 0, y `explained_variance_ratio` devuelve 1 y 0. Como comparación, `symmetric_eigen` sobre la misma matriz de covarianza devuelve 6/5 y 2/5.

### Ejercicio práctico

Si el paso 4 sale como se predice, la primera componente «explica» toda la varianza. ¿Por qué eso no prueba que sea el eje correcto, y qué comprobación sencilla revela el problema?

> *Solución:* El cociente divide cada varianza devuelta entre la suma de las varianzas devueltas, no entre la varianza total de los datos, así que un método que se salta el eje principal puede anunciar igualmente la totalidad. La varianza total es la traza de la matriz de covarianza, que es también la suma de sus valores propios (§1): 4/5 + 4/5 = 8/5. Las varianzas devueltas suman 2/5, así que 6/5 de la varianza, tres cuartas partes, quedan sin explicar.

---

## 9. Errores comunes

- **Dar una matriz no simétrica a un solucionador simétrico.** Responde a otra pregunta, sin error: comprueba la simetría, o repárala, antes.
- **Comparar los vectores propios con una lista esperada fija.** Su signo es libre, y con un valor propio múltiple también lo es toda la base: prueba invariantes o proyectores.
- **Fiarse de «la estimación dejó de cambiar».** Una iteración atascada en el vector propio equivocado también deja de cambiar.
- **Arrancar el método de la potencia desde un vector «neutro» fijo.** Sea cual sea ese vector, algunas matrices tienen su vector propio dominante ortogonal a él.
- **Escribir una prueba que nunca ejecuta el algoritmo.** Sobre la identidad, un solucionador de Jacobi no hace ninguna rotación.
- **Leer el comentario en lugar del código.** Los dos pueden discrepar, como en el criterio de parada de `symmetric_eigen`.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Vector propio, valor propio** | Un v no nulo con A v = λ v: una dirección que A solo estira, por el factor λ |
| **Polinomio característico** | det(A − λI), cuyas raíces son los valores propios |
| **Matriz simétrica** | Una matriz cuadrada con Aᵀ = A |
| **Matriz ortogonal** | Una matriz cuadrada Q con QᵀQ = I: sus columnas son ortonormales |
| **Teorema espectral** | Una matriz simétrica real se escribe A = Q Λ Qᵀ, con Q ortogonal y Λ real y diagonal |
| **Cociente de Rayleigh** | R(x) = xᵀAx / xᵀx, un promedio ponderado de los valores propios de una matriz simétrica A |
| **Rotación de Jacobi** | Una rotación plana J elegida para que JᵀAJ tenga un cero en una posición fuera de la diagonal elegida |
| **Subespacio propio** | Todos los v con A v = λ v para un λ dado; su dimensión puede ser mayor que 1 |
| **Proyector ortogonal** | uuᵀ + wwᵀ + … para una base ortonormal u, w, … de un subespacio; no depende de la base |
| **Método de la potencia** | La repetición de v ← A v / ‖A v‖, que encuentra el vector propio dominante si el arranque tiene una componente a lo largo de él |
| **Deflación** | El reemplazo de A por A − λ v vᵀ para quitar un par propio ya encontrado |

---

## Autoevaluación

**1. ¿Por qué los vectores propios de una matriz simétrica para los valores propios 3 y 1 tienen que ser ortogonales?**
> Si A u = 3u y A v = v, entonces 3 (u · v) = (A u) · v = u · (A v) = u · v, usando Aᵀ = A. Así, 2 (u · v) = 0, y u · v = 0.

**2. Para una matriz simétrica A con valores propios λ₁ ≥ … ≥ λₙ, ¿por qué el máximo del cociente de Rayleigh es λ₁, y dónde se alcanza?**
> R(x) es un promedio ponderado de los valores propios, con pesos cᵢ² ≥ 0 (§3), así que vale como mucho λ₁. Vale λ₁ en x = q₁, un vector propio para λ₁.

**3. CMA-ES reemplaza una matriz de covarianza C por S = (C + Cᵀ)/2 antes de llamar a `symmetric_eigen`. ¿Por qué S es la matriz simétrica más cercana a C?**
> Escribamos C = S + K con K = (C − Cᵀ)/2, de modo que Kᵀ = −K. Para toda matriz simétrica X, la matriz S − X es simétrica, y una matriz simétrica es ortogonal a K para el producto escalar Σ xᵢⱼyᵢⱼ que define la norma de Frobenius: los términos en (i, j) y (j, i) se cancelan, y K tiene ceros en su diagonal. Así, ‖C − X‖² = ‖S − X‖² + ‖K‖², que es mínimo exactamente para X = S. Para una matriz de covarianza que el redondeo ha alejado de la simetría, K es diminuta, y S es la reparación natural.

**4. La prueba `test_repeated_eigenvalues` de IX pasa. ¿Qué muestra sobre los valores propios múltiples?**
> Muy poco: sobre la identidad la parte fuera de la diagonal es nula, así que el solucionador se detiene antes de cualquier rotación y devuelve la identidad de la que partió. Una prueba con I + J forzaría rotaciones, y tendría que comprobar invariantes o el proyector, porque los vectores propios para el valor propio 1 no son únicos.

**Criterio de aprobación:** Hallar a mano los pares propios de una matriz 2 × 2, usar el teorema espectral y sus contraejemplos, acotar y estimar valores propios con el cociente de Rayleigh, aplicar una rotación de Jacobi, comprobar el resultado de un solucionador de valores propios mediante invariantes cuando los valores propios se repiten, y detectar las precondiciones y los puntos ciegos de los solucionadores de valores propios de IX.

---

## Base de investigación

- G. H. Golub y C. F. Van Loan, *Matrix Computations*, 4.ª ed., Johns Hopkins University Press, 2013, cap. 8: el problema de valores propios simétrico, el método de Jacobi, el método de la potencia y la desigualdad de Weyl
- B. N. Parlett, *The Symmetric Eigenvalue Problem*, SIAM Classics in Applied Mathematics, 1998: el cociente de Rayleigh y la sensibilidad de los vectores propios
- L. N. Trefethen y D. Bau, *Numerical Linear Algebra*, SIAM, 1997, lecciones 24 a 30: los algoritmos de valores propios, el método de la potencia y el método de Jacobi
- C. G. J. Jacobi, «Über ein leichtes Verfahren, die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen», *Journal für die reine und angewandte Mathematik* 30, 1846: el método de las rotaciones
- S. Axler, *Linear Algebra Done Right*, 4.ª ed., Springer, 2024: el teorema espectral y su demostración
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §7 enlaza a su línea
- Experimento: propuesto en el §8, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
