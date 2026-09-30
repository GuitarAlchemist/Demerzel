---
module_id: mat-017-nonnegative-matrix-factorisation
department: mathematics
course: Factorización de matrices no negativas
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-006-svd-low-rank-approximation, mat-012-iterative-optimisation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Factorización de matrices no negativas — Partes, actualizaciones multiplicativas y factores que no son únicos

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Enunciar el problema de la NMF, y acotar su error por debajo con la SVD
- Deducir las actualizaciones multiplicativas de Lee y Seung como pasos de gradiente escalados, y decir qué prueba su monotonía y qué no prueba
- Mostrar que los factores de la NMF están definidos, en el mejor de los casos, salvo escala y orden, y construir factorizaciones exactas que difieren en algo más
- Explicar por qué una tolerancia absoluta sobre el error de reconstrucción hace que una regla de parada dependa de las unidades de los datos
- Distinguir partes identificadas de una elección arbitraria entre soluciones igual de buenas, con varias semillas y un control separable
- Rastrear lo que garantiza `NonNegativeMatrixFactorization` de IX, y dónde su documentación, sus pruebas y su regla de parada prometen más de lo que el código entrega

---

## 1. El problema

Sea V una matriz n × p con entradas no negativas: n muestras, p características. La **factorización de matrices no negativas** (NMF) busca una matriz W de tamaño n × k y una matriz H de tamaño k × p, ambas con entradas no negativas, que minimicen ‖V − WH‖_F². Paatero y Tapper (1994) la introdujeron como factorización matricial positiva, y Lee y Seung (1999) la popularizaron. La fila i de V se aproxima por Σ_c W_ic h_c, una combinación de las k filas h_c de H con pesos no negativos: las filas de H son las **partes**, y W dice cuánto de cada parte contiene cada muestra. Nada puede restarse, así que ninguna parte puede anular a otra. Por eso la NMF de imágenes de caras da rasgos localizados, como la nariz o los ojos, y la NMF de recuentos de palabras da temas, mientras que la SVD del MAT-006 da componentes con signos mezclados.

El producto WH tiene rango a lo sumo k, así que el teorema de Eckart–Young–Mirsky del MAT-006 acota por debajo el error de toda factorización, no negativa o no: ‖V − WH‖_F ≥ √(σₖ₊₁² + σₖ₊₂² + …). La NMF solo puede alcanzar esta cota cuando alguna de las mejores aproximaciones de rango k es un producto de factores no negativos de dimensión interior k; cuando σₖ > σₖ₊₁ solo hay una, la SVD truncada V_k. Para k ≤ 2 esto ocurre exactamente cuando alguna de ellas no tiene ninguna entrada negativa, porque una matriz no negativa de rango a lo sumo 2 siempre tiene factores no negativos de la misma dimensión interior (Cohen y Rothblum 1993). Para k mayor puede fallar incluso para una mejor aproximación no negativa: el **rango no negativo** puede superar al rango. Además, el problema es difícil en general: Vavasis (2009) demostró que decidir si V tiene una NMF exacta de dimensión interior rango(V) es NP-difícil.

Con W fija, el objetivo es convexo en H: es un problema de mínimos cuadrados no negativos, como los del MAT-007. Lo mismo vale en W con H fija, pero no en ambas a la vez, ya que (W, H) y (WD, D⁻¹H) dan el mismo producto (§3), así que los minimizadores nunca son puntos aislados. Los algoritmos prácticos alternan entre los dos subproblemas convexos, y lo que encuentran depende de dónde empiezan.

### Ejercicio práctico

IX acepta cualquier k de 1 a min(n, p). Muestra que k = min(n, p) es trivial.

> *Solución:* Si k = p ≤ n, se toman W = V y H = I_p: ambas son no negativas y WH = V, con error 0. Si k = n ≤ p, se toman W = I_n y H = V. La cota de esta sección concuerda, ya que σₖ₊₁ = 0 cuando k ≥ rango(V). La NMF solo dice algo de los datos para k < min(n, p), donde las muestras deben compartir partes.

---

## 2. Actualizaciones multiplicativas

El gradiente de f(W, H) = ½‖V − WH‖_F² respecto de H es WᵀWH − WᵀV. Lee y Seung (2001) dan un paso de gradiente con un tamaño de paso distinto para cada entrada, η_ij = H_ij/(WᵀWH)_ij, y el paso se convierte en una multiplicación: H_ij − η_ij(WᵀWH − WᵀV)_ij = H_ij (WᵀV)_ij/(WᵀWH)_ij. Del mismo modo, W_ij pasa a ser W_ij (VHᵀ)_ij/(WHHᵀ)_ij. Cada factor es un cociente de números no negativos, así que W y H siguen siendo no negativas sin ninguna proyección, y no hay tamaño de paso que ajustar, cuando en el MAT-012 el tamaño de paso lo decide todo.

Lee y Seung demuestran que ninguna de las dos actualizaciones aumenta ‖V − WH‖_F. En la H actual construyen una cota superior cuadrática de f con hessiana diagonal, de entradas (WᵀWH)_a/H_a. La cota toca a f en el punto actual, y su minimizador es exactamente la actualización: una **función auxiliar**, o paso de mayorización–minimización. La prueba da una sucesión de errores no creciente, acotada por debajo por 0, así que los errores convergen. No muestra que los iterados converjan, ni que su límite sea un punto estacionario. Lin (2007) señaló que no existía ninguna prueba de convergencia a un punto estacionario para estas actualizaciones, y propuso actualizaciones modificadas para las que la demostró. Incluso un punto estacionario es solo una condición necesaria de mínimo local.

La actualización multiplica cada entrada, así que una entrada igual a 0 sigue en 0 diga lo que diga el gradiente. Los valores de partida deben ser, por tanto, positivos. Si V no tiene ninguna fila nula ni ninguna columna nula, unos factores positivos mantienen positivos los numeradores (WᵀV)_ij y (VHᵀ)_ij, así que toda entrada sigue siendo positiva, y una entrada cuyo valor óptimo es 0 se acerca a él poco a poco sin alcanzarlo nunca. Una columna nula de V, en cambio, anula la columna correspondiente de WᵀV, y la primera actualización pone exactamente a 0 esa columna de H. Como ejemplo resuelto, toma V = [[2, 1], [1, 2]], k = 1, W₀ = (1, 1)ᵀ y H₀ = (1, 1). Entonces W₀ᵀV = (3, 3) y W₀ᵀW₀H₀ = (2, 2), así que H₁ = (3/2, 3/2); luego VH₁ᵀ = (9/2, 9/2)ᵀ y W₀H₁H₁ᵀ = (9/2, 9/2)ᵀ, así que W₁ = W₀. El error baja de ‖V − W₀H₀‖_F = √2 ≈ 1.414 a ‖V − W₁H₁‖_F = 1. Los valores singulares de V son 3 y 1, así que 1 es la cota del §1: un solo paso alcanzó el óptimo.

### Ejercicio práctico

Sea V = uvᵀ con u y v vectores positivos, y k = 1. Muestra que un par de actualizaciones, desde cualesquiera w y h positivos, da exactamente W₁H₁ = V.

> *Solución:* wᵀV = (w · u)vᵀ y wᵀwh = ‖w‖²h, así que H₁ = ((w · u)/‖w‖²) v: las entradas de h se cancelan, y H₁ = αv con α > 0. Entonces VH₁ᵀ = α‖v‖²u y wH₁H₁ᵀ = α²‖v‖²w, así que W₁ = u/α, y W₁H₁ = uvᵀ. El error es 0 tras el primer par de actualizaciones, sea cual sea el punto de partida; la prueba de rango uno de IX usa una matriz así (§6).

---

## 3. Factores que no son únicos

Si WH = V, entonces (WD)(D⁻¹H) = V para toda matriz invertible D de tamaño k × k; la única cuestión es si WD y D⁻¹H siguen siendo no negativas. Para una D diagonal positiva, una permutación, o un producto de ambas, siempre lo son: la NMF no puede distinguir el tamaño de una parte del peso que se le da, ni el orden de las partes. Estas matrices monomiales son las únicas matrices no negativas cuya inversa también es no negativa. Antes de comparar ejecuciones, se escala por tanto cada parte, por ejemplo para que sume 1, y se emparejan las partes.

Para factores particulares, otras matrices mantienen no negativos ambos factores, y entonces la factorización no es única ni siquiera tras escalar. Toma X = [[2, 1], [1, 2]], W = I y H = X, y D = [[1, a], [0, 1]], cuya inversa es [[1, −a], [0, 1]]. Entonces W_a = [[1, a], [0, 1]] y H_a = [[2 − a, 1 − 2a], [1, 2]] cumplen W_aH_a = X, y ambas son no negativas exactamente cuando 0 ≤ a ≤ 1/2: un continuo de factorizaciones exactas que ningún escalado ni reordenamiento relaciona. Para a = 1/2, W = [[1, 1/2], [0, 1]] y H = [[3/2, 0], [1, 2]].

Cuando rango(V) = k, toda factorización exacta tiene la forma (WQ, Q⁻¹H) para una Q invertible, porque las columnas de cualquier otra W deben generar el espacio de columnas de V. Supón que W contiene un múltiplo positivo de cada fila unitaria, de modo que cada parte aparece pura en alguna muestra, y que H contiene un múltiplo positivo de cada columna unitaria, de modo que cada parte tiene una característica que ninguna otra parte usa. Las filas de WQ incluyen entonces múltiplos de las filas de Q, así que Q ≥ 0, y las columnas de Q⁻¹H múltiplos de las columnas de Q⁻¹, así que Q⁻¹ ≥ 0: Q es monomial, y la factorización es única salvo escala y orden. En el ejemplo anterior, W = I cumple la primera condición, pero H = X no tiene ninguna columna unitaria, lo que deja sitio a la cizalla. Donoho y Stodden (2004) dieron condiciones de este tipo para que la NMF recupere las partes verdaderas. Arora, Ge, Kannan y Moitra (2012) demostraron que la segunda condición sola, que llaman separabilidad, hace que la NMF sea calculable en tiempo polinómico.

### Ejercicio práctico

Muestra que (WD)(D⁻¹H) = WH para toda D invertible. ¿Por qué una D diagonal positiva mantiene no negativos ambos factores, mientras que una D diagonal con una entrada negativa no lo hace?

> *Solución:* Por asociatividad, (WD)(D⁻¹H) = W(DD⁻¹)H = WH. Una D diagonal = diag(d_1, …, d_k) multiplica la columna c de W por d_c y la fila c de H por 1/d_c. Cuando todos los d_c son positivos, ningún signo cambia. Cuando d_c < 0, la columna c de W cambia de signo; es no negativa y no nula, así que adquiere una entrada negativa. La factorización está definida, por tanto, en el mejor de los casos, salvo escalados positivos y reordenamientos de las partes.

---

## 4. Reglas de parada y unidades

Multiplica V por c > 0 y parte de √c W₀ y √c H₀. En la actualización de H, (√cW)ᵀ(cV) = c^(3/2) WᵀV y (√cW)ᵀ(√cW)(√cH) = c^(3/2) WᵀWH, así que el cociente no cambia y la nueva H es √c veces la anterior; la actualización de W se comporta del mismo modo. Por inducción, cada iterado sobre cV es √c veces el iterado correspondiente sobre V, y cada error es c veces mayor. Las actualizaciones no dependen de las unidades de los datos.

Una regla de parada puede reintroducir las unidades. Una regla que se detiene cuando el error cambia menos de τ, en términos absolutos, se convierte sobre cV en la regla de tolerancia τ/c sobre V: multiplicar los datos por 1000, como cuando los metros pasan a milímetros, hace la regla 1000 veces más estricta, y dividirlos por 1000 la hace 1000 veces más laxa. Una regla relativa, como |e_t − e_(t+1)| ≤ τ e_t, da el mismo número de iteraciones en cualquier unidad, y también una tolerancia sobre una medida de estacionariedad relativa a su primer valor, el tipo de regla que usa Lin (2007). Como en el MAT-012, un cambio pequeño certifica poco: no prueba ningún mínimo y, tras el §3, nada sobre los factores, ya que el error es constante a lo largo de familias enteras de factorizaciones.

Las constantes aditivas rompen la equivariancia del mismo modo. Un suelo sobre un valor de partida, o un ε sumado a un denominador, es una longitud en las unidades de los datos, y cuenta cuando los datos son pequeños frente a él. IX tiene ambos (§6).

### Ejercicio práctico

Completa el argumento para la actualización de W: si W_t y H_(t+1) sobre cV son √c veces los iterados sobre V, muestra que la actualización de W sobre cV da √c W_(t+1). ¿Qué cambia cuando se suma ε a los denominadores?

> *Solución:* (cV)(√cH)ᵀ = c^(3/2) VHᵀ y (√cW)(√cH)(√cH)ᵀ = c^(3/2) WHHᵀ, así que el cociente no cambia, y √cW por ese cociente es √c W_(t+1). Con ε, el denominador pasa a ser c^(3/2)(WHHᵀ)_ij + ε, y el cociente cambia en una cantidad relativa del orden de ε/(c^(3/2)(WHHᵀ)_ij): despreciable para datos ordinarios, pero no cuando c^(3/2)(WHHᵀ)_ij se acerca a ε.

---

## 5. Semillas, partes y un control separable

La prueba `test_nmf_error_decreases` de IX (§6) factoriza V = [[1, 0, 2], [0, 3, 1], [2, 1, 0], [1, 2, 1]] con k = 2 y 300 iteraciones. Por el §1, ninguna factorización de dimensión interior 2 tiene un error inferior a σ₃ ≈ 1.699561. La SVD truncada V₂ tiene como menor entrada aproximadamente 0.158, así que, por Cohen y Rothblum, tiene factores no negativos de dimensión interior 2, que alcanzan la cota. Toda factorización que alcanza la cota cumple WH = V₂, ya que la mejor aproximación de rango 2 es única cuando σ₂ > σ₃. Y como V₂ no tiene ninguna entrada nula, queda sitio para inclinar sus partes como en la cizalla del §3: V₂ tiene toda una familia de factorizaciones óptimas.

La transcripción del código de IX (§6) predice, para las semillas 42, 0 y 100, los errores 1.6996, 1.6997 y 1.6997 tras 51, 46 y 56 iteraciones, todos a menos de 0.0002 de la cota. Escala cada parte para que sume 1, y llama parte B a la que tiene más peso en la segunda característica. Es (0.035, 0.793, 0.173), (0.031, 0.789, 0.180) y (0.000, 0.832, 0.167), y el peso de la muestra 1, la fila (1, 0, 2), en la parte B es 0.174, 0.011 y 0.000. Las tres ejecuciones coinciden en el error, y discrepan sobre si la muestra 1 contiene la parte B.

Una parada prematura no lo explica. Con la tolerancia en 0 y 20,000 iteraciones, las tres ejecuciones deberían llegar a 1.699561, la cota misma, con los pesos 0.185, 0.007 y 0.000 para la muestra 1: convergen a tres factorizaciones óptimas distintas.

Un **control separable** es un conjunto de datos cuya factorización se sabe única. Toma V = [[1, 0, 2], [0, 1, 1], [1, 1, 3], [2, 1, 5]], que es WH para W = [[1, 0], [0, 1], [1, 1], [2, 1]] y H = [[1, 0, 2], [0, 1, 1]]. W contiene las dos filas unitarias y H las dos columnas unitarias, así que, por el §3, la factorización es única salvo escala y orden, con las partes (1/3, 0, 2/3) y (0, 1/2, 1/2) una vez escaladas para sumar 1. Con las 200 iteraciones por defecto de IX, las semillas 42, 0 y 100 deberían devolver ambas partes con un margen de 0.01, con errores de 0.018, 0.027 y 0.018. Ninguna de las tres ejecuciones se detiene antes del tope: las entradas que deberían valer 0 se acercan a 0 despacio (§2), y el cambio en las cinco últimas iteraciones sigue por encima de 10^-4, en 0.00044, 0.00096 y 0.00040.

Los dos casos separan dos cosas que uno querría que significara una parada. En la matriz de la prueba, la regla de IX se detiene mientras las partes son arbitrarias; en el control, nunca se detiene mientras las partes son correctas. Dar sentido a las partes exige indicios de que están identificadas, como el acuerdo entre semillas tras escalar y emparejar, no una parada ni un error pequeño.

### Ejercicio práctico

En el segundo párrafo, ¿por qué pueden las tres ejecuciones discrepar sobre el peso de la muestra 1 y coincidir en el error?

> *Solución:* Los tres productos están todos cerca de V₂, la única mejor aproximación de rango 2, así que los tres errores están cerca de σ₃. El producto no determina los factores: V₂ no tiene ninguna entrada nula, así que, como con la cizalla del §3, sus partes pueden inclinarse dentro del plano que generan mientras ambos factores siguen siendo no negativos. A lo largo de una familia así, el producto, y por tanto el error, no cambia, mientras que el peso de cada muestra en cada parte sí; el peso de la muestra 1 en la parte B es una de las cantidades que cambian.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de `fit_transform` y `transform` a Python, con una réplica del `StdRng` de rand 0.9 (ChaCha12, sembrado mediante PCG32) que reproduce las extracciones del propio crate. Los flotantes de Python son binary64 IEEE como el `f64` de Rust; las sumas pueden diferir de las de ndarray en los últimos bits, muy por debajo de los márgenes de los valores enunciados. Estos números son predicciones, y el §7 propone comprobarlas.

**NMF** (`crates/ix-unsupervised`). [`fit_transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L105) rechaza [k = 0 y k > min(n, p)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L112) y las [entradas negativas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L119). Extrae W y luego H de [`StdRng::seed_from_u64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L129), aplica las actualizaciones del §2 con ε en los denominadores, y mide el error con [`frobenius_distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L241), la norma misma y no su cuadrado, cada cinco iteraciones. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L183) conserva H, extrae una W nueva [con la misma semilla](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L202) y hace [50 actualizaciones de W](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L213). Los valores por defecto son [200 iteraciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L74) y la [semilla 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L77). El módulo es solo una biblioteca: [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/lib.rs#L11) lo exporta y ningún otro archivo Rust del repositorio se refiere a él, así que ninguna herramienta MCP ni etapa de pipeline ofrece la NMF. La inicialización y la prueba de parada dicen:

```rust
        let mean = v.mean().unwrap_or(1.0).abs().max(1e-3);
        let scale = (mean / self.n_components as f64).sqrt();
        let mut rng = StdRng::seed_from_u64(self.seed);
        let mut w = Array2::<f64>::zeros((n_samples, self.n_components));
        for e in w.iter_mut() {
            *e = rng.random::<f64>() * scale + self.eps;
        }
        let mut h = Array2::<f64>::zeros((self.n_components, n_features));
        for e in h.iter_mut() {
            *e = rng.random::<f64>() * scale + self.eps;
        }
```

```rust
            if iter % 5 == 0 || iter == self.max_iterations - 1 {
                let err = frobenius_distance(v, &w.dot(&h));
                final_err = err;
                if convergence.converged((prev_err - err).abs()) {
                    break;
                }
                prev_err = err;
            }
```

- **La regla de parada depende de las unidades de los datos.** La [tolerancia de 10^-4](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L75), documentada como una [«Convergence tolerance on the Frobenius reconstruction error»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L55), se compara mediante [`converged`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/convergence.rs#L46), con un `<` estricto, con el cambio del error entre dos comprobaciones. Las comprobaciones llegan tras las iteraciones 1, 6, 11 y así sucesivamente, así que el primer cambio abarca una iteración y los siguientes cinco. La escala de partida s = √(media/k) crece como √c, así que mientras la media se mantenga por encima del suelo de 10^-3 y ε siga siendo despreciable, toda la ejecución es equivariante (§4), y la tolerancia es absoluta. En la matriz del §5 con la semilla 42, multiplicada por 0.001, 1 y 1000, la transcripción predice 16, 51 y 86 iteraciones, con errores de 1.7360, 1.6996 y 1.69956 veces el factor, frente a la cota 1.699561.
- **La documentación promete más de lo que se sabe de las actualizaciones.** La documentación del módulo dice que la convergencia está [«guaranteed (not necessarily to a global optimum, but to a local one).»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L24) Lee y Seung demuestran que las actualizaciones exactas nunca aumentan el error. Que los iterados converjan a un punto estacionario, y menos aún a un mínimo local, no está demostrado para estas actualizaciones (§2), y la regla de parada de IX no comprueba ninguna de las dos cosas (§4, §5). La transcripción concuerda con la monotonía: con 30 semillas en cada una de las tres matrices de prueba de tamaños 3 × 3, 4 × 3 y 4 × 4 con k = 2, 300 iteraciones cada una, la mayor subida de una iteración a la siguiente es de aproximadamente 6.7 · 10^-16, un error de redondeo.
- **La prueba del error no pone a prueba las actualizaciones.** [`test_nmf_error_decreases`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L320) nunca compara el error final con el inicial. Afirma que el error es [menor](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L332) que la [suma de las entradas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L330), Σvᵢⱼ = 14. La factorización nula ya tiene el error ‖V‖_F = √26 ≈ 5.10, y ‖V‖_F ≤ Σvᵢⱼ para toda V no negativa. Antes de cualquier actualización, el error es menor que 5.49 para cualquier semilla (véase el ejercicio siguiente), así que la prueba seguiría pasando si se borrara el bucle de actualización. La monotonía de Lee y Seung se refiere a las actualizaciones exactas, no a las de IX, que añaden ε a los denominadores y pueden aumentar el error en cantidades del orden de ε: partiendo de V = W = H = 1, una factorización exacta, una actualización de H da el error ε/(1 + ε). Que la aserción siga cumpliéndose tras las actualizaciones con cualquier semilla no queda, por tanto, demostrado aquí; la transcripción lo predice para las 200 semillas probadas, sin ningún error mayor que 4.9 en ninguna comprobación y con todos los errores finales menores que 1.7. Con la semilla 42, la transcripción predice un error inicial de 4.545 y uno final de 1.6996, tras 51 iteraciones.
- **La prueba de rango uno se resuelve con la primera actualización.** [`test_nmf_rank_one_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L258) y el ejemplo del módulo usan V = uuᵀ con u = (1, 2, 3). Por el ejercicio del §2, el primer par de actualizaciones la reproduce desde cualquier punto de partida positivo, salvo el efecto de ε. La primera comprobación ve un cambio igual a todo el error inicial, aproximadamente 12.363 con la semilla 42, y no puede detenerse; la segunda sí puede. La transcripción predice 6 iteraciones para cualquier semilla, y un error de aproximadamente 4 · 10^-11 con la semilla 42, muy por debajo del [umbral de 0.1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L267). La prueba comprueba una propiedad real, pero no la iteración: cualquier método que dé un paso exacto de rango uno la pasa. El ejemplo solo afirma [el número de columnas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L39).
- **Nada advierte de que las partes no son únicas.** La documentación recomienda la NMF porque [«produces a parts-based»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L7) [«decomposition that is often more interpretable»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L8). La semilla tiene un [constructor](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L97), pero ninguna prueba la varía y ningún documento menciona el §3. El §5 da la consecuencia prevista en la propia matriz de la prueba del error: pesos de 0.174, 0.011 y 0.000 para la muestra 1 en la misma parte, con las semillas 42, 0 y 100.
- **Se aceptan entradas NaN y +∞.** La [comprobación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L119) `x < 0.0` es falsa para NaN y para +∞, así que una matriz con una entrada así la supera; −∞ se rechaza. Su media es NaN, y el [suelo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L127) la convierte en 10^-3, porque `f64::max` de Rust devuelve el otro operando cuando uno es NaN. Tras la primera actualización, todas las entradas de W y H son NaN; el cambio es NaN, `converged` nunca se cumple, y la transcripción predice las 200 iteraciones, y luego `Ok`, con W, H y el error enteramente NaN. Una entrada igual a +∞ da el mismo resultado, y [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L196) tiene la misma comprobación.
- **Otras lagunas.** [`test_nmf_transform_matches_shape`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L302) solo comprueba [formas y signos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L316), y ninguna prueba compara `transform` sobre los datos de entrenamiento con la W que devuelve `fit_transform`. No hay inicialización estructurada como NNDSVD, ni reinicio con varias semillas, ni tolerancia relativa, ni regularización, ni otro objetivo que la norma de Frobenius, ni indicador de una ejecución que llegó al tope: [`n_iter`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L66) igual a `max_iterations` es la única señal.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

La prueba del error de IX parte de W₀ y H₀ con entradas u · s + ε, donde u es uniforme en [0, 1) y s = √(media/k). Muestra que antes de cualquier actualización el error es menor que 5.49, sea cual sea la semilla.

> *Solución:* Las 12 entradas suman 14, así que la media es 7/6 y s² = 7/12 para k = 2. Cada entrada de W₀H₀ es una suma de dos productos de números de [ε, s + ε), así que está estrictamente entre 0 y 2(s + ε)² = 7/6 + δ, donde δ = 4sε + 2ε² es menor que 10^-9 para el ε de 10^-10 de IX. Una entrada v de V difiere, por tanto, de la entrada correspondiente de W₀H₀ en menos de 7/6 + δ para cada uno de los tres ceros, y en menos de v para los cinco unos, los tres doses y el tres. El error al cuadrado es menor que 3(7/6 + δ)² + 5 + 12 + 9 = 1083/36 + 7δ + 3δ², y 1083/36 ≈ 30.083 mientras que 5.49² ≈ 30.140, así que el error es menor que 5.49, menos de la mitad de 14.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **La matriz de la prueba del error.** Llamar a `fit_transform` con k = 2, 300 iteraciones y la semilla 42 sobre la matriz del §5. Predicción: `n_iter` igual a 51 y un error de 1.6996, con un margen de 10^-4.
2. **Un error monótono.** Para i = 1, …, 300, repetir el paso 1 con `with_tolerance(0.0)` y `with_max_iterations(i)`. Como `converged` es un `<` estricto, cada ejecución se detiene tras exactamente i iteraciones e informa del error tras i. Predicción: el error nunca sube más de 10^-15, y decrece hacia 1.699561.
3. **Semillas.** Repetir el paso 1 con las semillas 0 a 9, escalar cada parte para que sume 1, y hallar el peso de la muestra 1 en la parte B. Predicción: todos los errores a menos de 0.00024 de 1.699561, y pesos que van de 0.000 a 0.112.
4. **Unidades.** Repetir el paso 1 sobre 0.001 V y sobre 1000 V. Predicción: 16 y 86 iteraciones, frente a 51 para V, con errores de 1.7360 y 1.69956 veces el factor.
5. **Control separable.** Repetir el paso 3 sobre el control del §5 con las 200 iteraciones por defecto. Predicción: cada ejecución usa las 200 iteraciones, y ambas partes coinciden con (1/3, 0, 2/3) y (0, 1/2, 1/2) con un margen de 0.01.
6. **Una entrada NaN.** Sustituir una entrada de la matriz del §5 por NaN, y llamar a `fit_transform` con k = 2 y los ajustes por defecto. Predicción: `Ok`, `n_iter` igual a 200, y W, H y el error enteramente NaN.

### Ejercicio práctico

En el paso 4, ¿por qué 0.001 V se detiene tras 16 iteraciones con un error mayor, si sus iterados son los de V escalados?

> *Solución:* Sobre 0.001 V, cada error es 0.001 veces el error sobre V (§4), así que la tolerancia de 10^-4 equivale a 0.1 en las unidades de V. En esas unidades, la transcripción predice cambios de 2.363, 0.208, 0.143 y 0.094 en las comprobaciones que siguen a las iteraciones 1, 6, 11 y 16. El cambio 0.094 es el primero por debajo de 0.1, así que la ejecución se detiene tras 16 iteraciones, en 1.7360 en las unidades de V, mientras que la ejecución sobre V sigue hasta que el cambio baja de 10^-4, tras 51 iteraciones. Una tolerancia relativa daría la misma respuesta en ambas unidades.

---

## 8. Errores comunes

- **Dar sentido a las partes de una sola ejecución.** Ejecuta varias semillas, escala y empareja las partes, e informa de lo que coincide.
- **Tomar una parada por una solución.** Un cambio por debajo de una tolerancia no prueba ningún mínimo ni identifica ningún factor; en la matriz de prueba del §5, la parada llega mientras las partes son arbitrarias.
- **Usar una tolerancia absoluta con datos en unidades arbitrarias.** Reescala los datos a una norma fija, o usa una regla relativa.
- **Elegir k solo por el error.** El mejor error solo puede bajar al crecer k, y llega a 0 en k = min(n, p), donde la factorización es trivial.
- **Empezar una entrada en 0.** Las actualizaciones multiplicativas nunca la mueven; parte de valores positivos.
- **Comparar factores columna a columna.** La escala y el orden son arbitrarios; escala cada parte y empareja las partes primero.
- **Escribir una prueba que la factorización nula supera.** Compara con el error inicial, o con la cota del §1.
- **Pasar NaN a un ajuste que solo rechaza entradas negativas.** Comprueba que cada entrada es finita antes de ajustar.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Factorización de matrices no negativas (NMF)** | Aproximar V ≥ 0 por WH con W ≥ 0 y H ≥ 0 de dimensión interior k |
| **Parte** | Una fila de H; cada muestra es una combinación no negativa de las partes |
| **Actualización multiplicativa** | Un paso de gradiente con tamaños de paso por entrada que se convierte en una multiplicación por un cociente de términos no negativos |
| **Función auxiliar** | Una cota superior del objetivo que lo toca en el punto actual, de modo que minimizarla no puede aumentar el objetivo |
| **Rango no negativo** | El menor k para el que V = WH exactamente con factores no negativos; es al menos rango(V) |
| **Ambigüedad de escala** | (WD)(D⁻¹H) = WH para toda D diagonal positiva |
| **Identificabilidad** | La propiedad de que V determina los factores, salvo escala y orden |
| **Separabilidad** | La condición de que cada parte tenga una característica que ninguna otra parte usa |
| **Tolerancia absoluta** | Un umbral de parada expresado en las unidades de los datos |
| **Control separable** | Datos cuya factorización se sabe única, sobre los que un método debe devolver las mismas partes con cualquier semilla |

---

## Autoevaluación

**1. Un colega muestra los temas de una ejecución de NMF con la semilla 42, e interpreta el tema 3. ¿Qué le pides?**
> Ejecuciones con otras semillas, con los temas escalados y emparejados, para ver si el tema 3 reaparece; los errores de esas ejecuciones, y la cota del §1; el número de iteraciones frente al tope; y la misma cadena sobre un control separable, donde los temas deben coincidir entre semillas. Como muestra el §5, ejecuciones cuyos errores coinciden con un margen de 0.0002 pueden discrepar sobre qué muestras contienen una parte.

**2. ¿Por qué una actualización multiplicativa no puede mover una entrada que vale 0, y qué implica eso para el punto de partida?**
> La actualización multiplica la entrada por un cociente, así que 0 sigue en 0 diga lo que diga el gradiente. El punto de partida debe ser, por tanto, positivo, como asegura el pequeño desplazamiento ε de IX, y, salvo que V tenga una fila o una columna nula, una entrada que debería terminar en 0 solo se acerca a él poco a poco, lo que retrasa la parada, como en el control separable del §5.

**3. Las mismas mediciones necesitan 86 iteraciones en la NMF de IX cuando se expresan en gramos, 51 en kilogramos y 16 en toneladas. ¿Qué ejecución es la correcta?**
> Ninguna es privilegiada: las actualizaciones son las mismas salvo escala, y solo la regla de parada difiere, porque la tolerancia de 10^-4 de IX es absoluta. En toneladas equivale a una tolerancia 1000 veces más laxa que en kilogramos. Reescala los datos a una norma fija, o usa una regla relativa, e informa del error relativo a ‖V‖_F.

**4. `test_nmf_error_decreases` afirma que el error final es menor que la suma de las entradas. ¿Cómo sería una aserción útil?**
> Una que falle cuando las actualizaciones no funcionan: por ejemplo, que el error final sea menor que el inicial con un margen, o que esté a un factor pequeño de la cota σ₃ del §1, 1.699561 en la matriz de la prueba. La aserción actual se cumple incluso para la factorización nula, cuyo error es √26 ≈ 5.10, menor que 14.

**Criterio de aprobación:** Enunciar el problema de la NMF y su cota por la SVD, deducir las actualizaciones multiplicativas y decir qué prueba su monotonía, mostrar por qué los factores no son únicos y cuándo lo son, explicar por qué una tolerancia absoluta depende de las unidades, diseñar una comparación de semillas con un control separable, y rastrear dónde la documentación, las pruebas y la regla de parada de IX prometen más de lo que el código entrega.

---

## Base de investigación

- J. E. Cohen y U. G. Rothblum, «Nonnegative ranks, decompositions, and factorizations of nonnegative matrices», *Linear Algebra and its Applications* 190, 1993: el rango no negativo, y el caso de rango 2
- P. Paatero y U. Tapper, «Positive matrix factorization: a non-negative factor model with optimal utilization of error estimates of data values», *Environmetrics* 5, 1994: el problema
- D. D. Lee y H. S. Seung, «Learning the parts of objects by non-negative matrix factorization», *Nature* 401, 1999: las representaciones por partes
- D. D. Lee y H. S. Seung, «Algorithms for non-negative matrix factorization», *Advances in Neural Information Processing Systems* 13, 2001: las actualizaciones multiplicativas y su monotonía
- D. Donoho y V. Stodden, «When does non-negative matrix factorization give a correct decomposition into parts?», *Advances in Neural Information Processing Systems* 16, 2004: condiciones para partes únicas
- C.-J. Lin, «On the convergence of multiplicative update algorithms for nonnegative matrix factorization», *IEEE Transactions on Neural Networks* 18, 2007: la estacionariedad del límite, y actualizaciones modificadas
- C. Boutsidis y E. Gallopoulos, «SVD based initialization: a head start for nonnegative matrix factorization», *Pattern Recognition* 41, 2008: la inicialización NNDSVD
- S. A. Vavasis, «On the complexity of nonnegative matrix factorization», *SIAM Journal on Optimization* 20, 2009: la NP-dificultad
- S. Arora, R. Ge, R. Kannan y A. Moitra, «Computing a nonnegative matrix factorization — provably», *Proceedings of the ACM Symposium on Theory of Computing*, 2012: la separabilidad
- N. Gillis, *Nonnegative Matrix Factorization*, SIAM, 2020: algoritmos, identificabilidad y reglas de parada
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
