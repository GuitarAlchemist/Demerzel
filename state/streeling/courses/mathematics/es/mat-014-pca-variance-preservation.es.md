---
module_id: mat-014-pca-variance-preservation
department: mathematics
course: El ACP como preservación de la varianza
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-006-svd-low-rank-approximation, mat-009-estimation-uncertainty-sampling]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# El ACP como preservación de la varianza — Qué conservan las componentes principales, y qué no prometen

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Obtener las componentes principales como las direcciones de mayor varianza, y mostrar que son vectores propios de la matriz de covarianza
- Mostrar que las mismas componentes minimizan el error de reconstrucción cuadrático, y calcular ese error a partir de los valores propios descartados
- Calcular el ACP a partir de la SVD de los datos centrados, y explicar por qué esa vía es más precisa que formar la matriz de covarianza
- Leer correctamente una razón de varianza explicada, y explicar cómo las unidades cambian las componentes
- Decir cuándo las componentes principales no son únicas ni estables, y distinguir el ACP del blanqueo
- Rastrear qué calcula el ACP de IX, y dónde su razón, su prueba de parada y su estado guardado se apartan de estas definiciones

---

## 1. La varianza a lo largo de una dirección

Sean x₁, …, xₙ observaciones en dimensión p con media x̄, y X_c la matriz n × p cuyas filas son los xᵢ − x̄. La **matriz de covarianza muestral** es S = X_cᵀX_c/(n − 1), con el n − 1 del MAT-009. Para un vector unitario w, las **puntuaciones** zᵢ = wᵀ(xᵢ − x̄) tienen media 0 y varianza muestral wᵀSw. La primera **componente principal** es el vector unitario que maximiza esta varianza.

S es simétrica y semidefinida positiva, así que por el MAT-005 el máximo del cociente de Rayleigh wᵀSw sobre los vectores unitarios es su mayor valor propio λ₁, alcanzado en un vector propio q₁. La segunda componente maximiza wᵀSw sobre los vectores unitarios ortogonales a q₁, lo que da λ₂ y q₂, y así sucesivamente. Las componentes son ortonormales, las puntuaciones según componentes distintas están incorreladas, y sus varianzas son λ₁ ≥ λ₂ ≥ … ≥ λ_p ≥ 0. La varianza total, la traza de S, vale λ₁ + … + λ_p: el ACP gira los datos sin cambiar su dispersión total.

### Ejercicio práctico

Unos datos tienen covarianza S = [[2, 1], [1, 2]]. ¿Cuál es la primera componente principal, y qué fracción de la varianza total lleva? Compárala con la varianza a lo largo de (1, 0).

> *Solución:* S (1, 1) = (3, 3) y S (1, −1) = (1, −1), así que los valores propios son 3 y 1, para (1, 1)/√2 y (1, −1)/√2. La primera componente es (1, 1)/√2, con varianza 3 sobre un total de 4, una fracción 3/4. A lo largo de (1, 0) la varianza es solo S₁₁ = 2: la correlación entre las dos coordenadas inclina la dirección de mayor dispersión hacia la diagonal.

---

## 2. La mejor aproximación de baja dimensión

Conservar k componentes sustituye cada observación por x̂ᵢ = x̄ + Σⱼ≤ₖ zᵢⱼ qⱼ, su proyección ortogonal sobre el subespacio afín que pasa por x̄ y está generado por q₁, …, qₖ. Por Pitágoras, ‖xᵢ − x̄‖² = ‖x̂ᵢ − x̄‖² + ‖xᵢ − x̂ᵢ‖². Sumado sobre las observaciones, el lado izquierdo vale (n − 1) veces la traza de S, fijada por los datos, así que maximizar la varianza conservada equivale a minimizar el **error de reconstrucción** cuadrático Σ‖xᵢ − x̂ᵢ‖². El mínimo es (n − 1)(λₖ₊₁ + … + λ_p), los valores propios descartados. Es el teorema de Eckart–Young del MAT-006, aplicado a X_c: ningún otro subespacio de dimensión k lo hace mejor.

### Ejercicio práctico

Toma los cuatro puntos B: (2, 0), (−2, 0), (0, 1) y (0, −1). Calcula S, la suma de los cuadrados de las distancias a la media, y el error de reconstrucción con una componente.

> *Solución:* La media es 0, y X_cᵀX_c = [[8, 0], [0, 2]], así que S = diag(8/3, 2/3). La suma de los cuadrados de las distancias es 4 + 4 + 1 + 1 = 10 = 3 (8/3 + 2/3). La primera componente es el primer eje, y proyectar sobre él deja los residuos de (0, 1) y (0, −1), con error cuadrático 1 + 1 = 2 = 3 · 2/3, el valor propio descartado por n − 1. La componente conserva 8/(8 + 2) = 0.8 de la varianza.

---

## 3. El ACP mediante la SVD

Escribamos la SVD del MAT-006 como X_c = UΣVᵀ. Entonces S = VΣ²Vᵀ/(n − 1): las direcciones principales son los vectores singulares por la derecha, las varianzas son λᵢ = σᵢ²/(n − 1), y las puntuaciones son X_cV = UΣ. Calcular el ACP así nunca forma X_cᵀX_c, cuyo número de condición es el cuadrado del de X_c: formarla puede perder el doble de cifras, y las componentes pequeñas las pierden primero (MAT-003, MAT-007). Cada vector singular, y por tanto cada componente, solo está definido salvo el signo: dos programas correctos pueden devolver q y −q, y sus resultados deben compararse salvo el signo.

### Ejercicio práctico

Calcula los valores singulares de la matriz centrada de B, las varianzas que dan, y los números de condición de X_c y de S.

> *Solución:* Las columnas de X_c son (2, −2, 0, 0) y (0, 0, 1, −1). Son ortogonales, con normas √8 y √2, así que σ₁ = √8 y σ₂ = √2, y λ = 8/3 y 2/3 como en el §2. κ(X_c) = √8/√2 = 2, mientras que κ(S) = (8/3)/(2/3) = 4 = κ(X_c)².

---

## 4. Varianza explicada y unidades

La **razón de varianza explicada** de la componente i es λᵢ/(λ₁ + … + λ_p) = λᵢ/traza(S). Su denominador es la varianza total, la suma de los p valores propios, no solo de los que se conservan; se puede calcular a partir de la diagonal de S, sin ningún valor propio. La razón dice qué parte de la dispersión lleva una componente, no si importa: una dirección de varianza pequeña puede ser la que separa dos clases.

El ACP sobre la covarianza depende de las unidades de cada variable. Multiplicar una variable por 100 multiplica su varianza por 10^4 y atrae hacia ella la primera componente. El **ACP estandarizado** divide antes cada variable por su desviación típica, lo que equivale a tomar los vectores propios de la matriz de correlación: elimina las unidades, y da a cada variable el mismo peso por decisión. Multiplicar todas las variables por el mismo factor, en cambio, debe dejar las componentes sin cambios y multiplicar cada varianza por el cuadrado del factor.

### Ejercicio práctico

La estatura tiene desviación típica 0.1 m y el peso 10 kg, y no están correlacionados. ¿Cuál es la primera componente principal, y su razón? ¿Qué cambia si la estatura se mide en centímetros?

> *Solución:* S = diag(0.01, 100), así que la primera componente es el eje del peso, con razón 100/100.01 ≈ 0.9999. En centímetros, la estatura tiene desviación típica 10 y varianza 100, así que S = diag(100, 100): las dos varianzas son iguales, la primera componente no es única, y cada eje lleva 1/2. Ninguna de las dos respuestas dice qué variable importa más; decidieron las unidades.

---

## 5. Unicidad, estabilidad y blanqueo

Si λ₁ = λ₂, todo vector unitario de su espacio propio de dimensión dos es una primera componente válida, y programas correctos distintos devuelven componentes distintas. Si λ₁ y λ₂ están cerca, la componente existe pero es frágil: por el teorema de Davis–Kahan, una perturbación E de S, por ruido o por redondeo, puede girar q₁ un ángulo θ cuyo seno llega a ‖E‖ dividido por la **brecha espectral** λ₁ − λ₂. La iteración de la potencia del MAT-005 nota la misma brecha: la tangente de su ángulo con q₁ se multiplica por λ₂/λ₁ en cada paso, y la **deflación**, que resta λ v vᵀ para hallar la componente siguiente, transmite el error restante.

El ACP no **blanquea**. Sus puntuaciones conservan las varianzas λᵢ; el blanqueo divide la puntuación según qᵢ por √λᵢ, de modo que los datos blanqueados tienen la identidad como covarianza. El blanqueo pone las direcciones de menor varianza, a menudo casi solo ruido, al mismo nivel que las mayores.

### Ejercicio práctico

¿Cuándo deja de ser única la primera componente principal? Para S = diag(2/3, 2r²/3) con r = 0.999, la iteración de la potencia parte de (1, 1)/√2. ¿Cuántos pasos hacen falta para que la tangente de su ángulo con el primer eje baje de 10^-6?

> *Solución:* Cuando λ₁ = λ₂: cualquier vector unitario de su espacio propio es entonces una primera componente válida. Aquí Sᵏ(1, 1) es proporcional a (1, r²ᵏ), así que la tangente tras k pasos es r²ᵏ, y el factor por paso es λ₂/λ₁ = r² = 0.998001. La condición r²ᵏ < 10^-6 exige k ≥ 6905 pasos. Tras 1000 pasos, la tangente todavía vale r^2000 ≈ 0.135, un ángulo de unos 7.7°.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de `fit`, `power_iteration`, `deflate` y `explained_variance_ratio` a Python, cuyos flotantes son binary64 IEEE como el `f64` de Rust: son predicciones, y el §7 propone comprobarlas.

**ACP** (`crates/ix-unsupervised`). `PCA` calcula la matriz de covarianza [con n − 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L168), luego extrae cada componente por [iteración de la potencia](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L103), con como mucho 1000 pasos y la tolerancia 10^-10 [fijada por `fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L176), y la retira por [deflación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L141). El MAT-005 mostró que el vector inicial fijo (1, …, 1)/√n puede perder por completo la dirección dominante; los hallazgos siguientes son de otro tipo. La herramienta MCP `ix_pca` llama a `PCA` a través del manejador [`pca`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L370), que [rechaza](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L382) más componentes que variables, y el pipeline de aprendizaje solo lo usa cuando su opción `pca_components` es [menor que el número de columnas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/ml_pipeline.rs#L539). La razón y el ajuste dicen:

```rust
    /// Get explained variance ratios (proportion of total variance per component).
    pub fn explained_variance_ratio(&self) -> Option<Array1<f64>> {
        self.explained_variance.as_ref().map(|ev| {
            let total = ev.sum();
            if total > 0.0 {
                ev / total
            } else {
                ev.clone()
            }
        })
    }
```

```rust
    fn fit(&mut self, x: &Array2<f64>) {
        let n = x.nrows();
        let p = x.ncols();
        let k = self.n_components.min(p);

        // Compute column means
        let mean = x.mean_axis(Axis(0)).unwrap();

        // Center the data
        let mut centered = x.clone();
        for mut row in centered.rows_mut() {
            row -= &mean;
        }

        // Compute covariance matrix: (1/(n-1)) X^T X
        let cov = centered.t().dot(&centered) / (n.max(2) - 1) as f64;

        // Extract top-k eigenvectors via repeated power iteration + deflation
        let mut components = Array2::zeros((k, p));
        let mut explained_variance = Array1::zeros(k);
        let mut current_cov = cov;

        for i in 0..k {
            let (eigenvalue, eigenvector) = power_iteration(&current_cov, 1000, 1e-10);
            components.row_mut(i).assign(&eigenvector);
            explained_variance[i] = eigenvalue.max(0.0);
            current_cov = deflate(&current_cov, eigenvalue, &eigenvector);
        }

        self.components = Some(components);
        self.explained_variance = Some(explained_variance);
        self.mean = Some(mean);
    }
```

- **La razón divide por la varianza conservada, no por el total.** `ev` solo contiene las k varianzas calculadas, así que con una componente la razón vale siempre 1, sean cuales sean los datos. Sobre los diez puntos del tutorial de Lindsay Smith, los datos de la prueba del skill de IX, la primera componente lleva una fracción 0.963 de la varianza, y la razón informa 1; sobre los puntos isótropos (±1, 0) y (0, ±1), donde la fracción verdadera es 1/2, también informa 1. Con k = p la suma es la traza y la razón es correcta: 0.9632 y 0.0368 sobre los mismos diez puntos. El esquema de salida promete la [«Fraction of total variance carried by each component»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L187). Dos pruebas comprueban la razón con una componente, [por encima de 0.99](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L237) y [por encima de 0.9](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L978): ambas pasan con cualquier conjunto de datos.
- **La prueba de parada depende de la escala de los datos.** La iteración de la potencia se detiene cuando la estimación de Rayleigh [cambia menos de 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L126), un umbral absoluto. Multiplicar los datos por una potencia de dos es exacto en binary64, así que cada paso del ajuste cambia de escala exactamente, salvo esa comparación. Sobre los cuatro puntos B del §2:
  - a escala 1, la primera llamada da 11 pasos y la primera componente está a menos de 2 · 10^-5 grados del primer eje;
  - a 2^-16, la primera componente se desvía 0.9°, las varianzas valen unos 2.66 s² y 0.30 s² en lugar de (8/3) s² y (2/3) s², y la razón es 0.90 en lugar de 0.8;
  - a 2^-17 ≈ 7.6 · 10^-6 y por debajo, la primera estimación de Rayleigh (5/3) s² ya está por debajo de 10^-10, así que cada llamada se detiene tras una sola multiplicación. Las dos componentes son (4, 1)/√17, a 14° del primer eje, con varianzas (5/3) s² y (15/34) s², y una razón de 34/43 ≈ 0.791.
- **La ortogonalidad solo vale lo que vale la prueba de parada.** Detenerse sobre el valor propio deja en el vector un error de un orden mayor, y la deflación lo transmite. Sobre B, el producto escalar de las dos componentes vale unos −7.2 · 10^-7 a escala 1, −1.1 · 10^-5 a 2^-4 y −7.3 · 10^-4 a 2^-10. [`test_pca_components_orthogonal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L288) exige [menos de 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L306) sobre datos cuyas dos primeras varianzas, 2.82 y 0.0133, están muy separadas; allí el producto escalar previsto es −1.9 · 10^-8. Ninguna de las siete pruebas de `pca.rs` compara las componentes con un solucionador espectral o con la SVD.
- **Los valores propios cercanos llegan al tope en silencio.** Sobre (±1, 0) y (0, ±r), las varianzas son 2/3 y 2r²/3, y los iterados son proporcionales a (1, r²ᵏ) como en el §5. La primera llamada da 50 pasos para r = 0.9 y unos 390 para r = 0.99. Para r = 0.999 se detiene en el tope de 1000 con la primera componente desviada unos 7.7°, y nada en el resultado indica que la iteración no convergió.
- **Un modelo guardado puede no cargarse.** `fit` conserva [min(n_components, p)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L156) componentes, pero `save_state` guarda el [número pedido](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L75), y `load_state` [redimensiona con él](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L89). Con tres componentes pedidas sobre dos variables, el estado contiene cuatro números para una forma 3 × 2, y la carga entra en pánico con [«PcaState components dimensions mismatch»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L90). El manejador y el pipeline nunca piden más componentes que variables, pero quien llama directamente a `PCA::new` no está protegido.
- **La transformación no blanquea.** [Proyecta los datos centrados](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L198) sobre las componentes, así que las puntuaciones conservan las varianzas λᵢ, como describe el §5.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

¿Por qué `explained_variance_ratio` devuelve 1 para cualquier conjunto de datos cuando se pide una sola componente, y qué denominador lo convertiría en una fracción de la varianza total?

> *Solución:* Con una componente, `ev` tiene una sola entrada λ̂₁, y `ev / total` la divide por sí misma. La fracción de la varianza total necesita λ̂₁/traza(S), donde traza(S) es la suma de las p entradas diagonales de la matriz de covarianza, que `fit` calcula y luego descarta. Sobre los diez puntos del tutorial de Lindsay Smith eso da 1.284/(1.284 + 0.0491) ≈ 0.963. Una prueba capaz de detectar el fallo necesita datos cuya primera componente lleve una fracción conocida claramente por debajo de su umbral, como los puntos isótropos, cuya fracción es 1/2.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **La razón.** Llamar al manejador `pca` sobre los diez puntos del tutorial de Lindsay Smith con `n_components` igual a 1, luego 2, y sobre los puntos isótropos (±1, 0) y (0, ±1) con 1. Predicción: [1], luego unos [0.9632, 0.0368], luego [1]; la traza de la covarianza da las fracciones verdaderas 0.963 y 1/2 en los casos de una componente.
2. **Frente a la SVD.** Ajustar `PCA` con dos componentes sobre los diez puntos, y calcular `svd` de la matriz centrada. Predicción: las componentes coinciden con los vectores singulares por la derecha salvo el signo, la primera a menos de 10^-6 grados y la segunda a menos de 10^-5 grados, y las varianzas coinciden con σ²/9 con un error menor que 10^-12.
3. **La escala.** Ajustar `PCA` con dos componentes sobre B multiplicado por 1, 2^-4, 2^-10, 2^-16, 2^-17 y 2^-20. Predicción: los valores del §6, desde una primera componente a menos de 2 · 10^-5 grados del primer eje a escala 1 hasta la misma componente (4, 1)/√17 dos veces a partir de 2^-17.
4. **La ortogonalidad.** Sobre los datos de `test_pca_components_orthogonal` y sobre B a las escalas del paso 3, calcular el producto escalar de las dos componentes. Predicción: unos −1.9 · 10^-8 sobre los datos de la prueba, y −7.2 · 10^-7, −1.1 · 10^-5 y −7.3 · 10^-4 sobre B a 1, 2^-4 y 2^-10.
5. **Valores propios cercanos.** Ajustar sobre (±1, 0) y (0, ±r) para r = 0.9, 0.99 y 0.999. Predicción: la primera componente está a menos de 0.002° del primer eje para r = 0.9, desviada unos 0.024° para r = 0.99, y unos 7.7° para r = 0.999.
6. **Guardar y cargar.** Ajustar `PCA::new(3)` sobre los diez puntos, llamar a `save_state`, y luego a `load_state` dentro de `std::panic::catch_unwind`. Predicción: el ajuste y la transformación funcionan con dos componentes, y `load_state` entra en pánico con el mensaje del §6.

### Ejercicio práctico

¿Para qué factores de escala s se detiene la primera llamada de la iteración de la potencia tras una sola multiplicación sobre B · s, y por qué eso hace de 2^-17 la primera potencia de dos afectada?

> *Solución:* La primera estimación se compara con el valor inicial 0, así que el bucle se detiene de inmediato cuando v₀ᵀ(s² S)v₀ < 10^-10, con v₀ = (1, 1)/√2 y v₀ᵀSv₀ = (8/3 + 2/3)/2 = 5/3. Eso significa (5/3) s² < 10^-10, o s < √(6 · 10^-11) ≈ 7.75 · 10^-6. La potencia 2^-17 ≈ 7.63 · 10^-6 está por debajo, mientras que 2^-16 ≈ 1.53 · 10^-5 está por encima. Los datos son los mismos salvo las unidades; solo el umbral absoluto ve la diferencia.

---

## 8. Errores comunes

- **Dividir por la varianza conservada.** La razón de varianza explicada necesita la traza de la matriz de covarianza; la suma de los valores propios retenidos hace que una sola componente lo explique todo.
- **Mezclar unidades en el ACP sobre la covarianza.** Una variable con gran dispersión numérica domina la primera componente; estandariza cuando las unidades sean arbitrarias, y dilo.
- **Leer la varianza como importancia.** Una componente pequeña puede llevar la señal que importa; la razón mide dispersión, no relevancia.
- **Comparar componentes sin tener en cuenta el signo.** q y −q son la misma componente; compara |qᵀq′|, o fija una convención de signo.
- **Confiar en una componente con una brecha espectral pequeña.** Cuando λ₁ ≈ λ₂, interpreta el subespacio que generan, no cada dirección.
- **Formar XᵀX cuando la SVD está disponible.** Eleva al cuadrado el número de condición y pierde primero las componentes pequeñas.
- **Detenerse sobre un cambio absoluto.** Una tolerancia que ignora el tamaño de la matriz hace que la respuesta dependa de las unidades; compara los cambios con el tamaño del valor propio.
- **Confundir el ACP con el blanqueo.** El ACP gira; el blanqueo también cambia la escala, y amplifica las direcciones de menor varianza.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Matriz de covarianza muestral** | S = X_cᵀX_c/(n − 1), para la matriz de datos centrados X_c |
| **Componente principal** | Un vector propio unitario de S; la primera maximiza la varianza de los datos proyectados |
| **Puntuación** | La coordenada wᵀ(x − x̄) de una observación según una componente |
| **Varianza total** | La traza de S, igual a la suma de sus valores propios |
| **Razón de varianza explicada** | λᵢ dividido por la varianza total |
| **Error de reconstrucción** | La suma de los cuadrados de las distancias de las observaciones a sus proyecciones, (n − 1) veces los valores propios descartados |
| **Teorema de Eckart–Young** | La SVD truncada es la mejor aproximación de rango dado en la norma de Frobenius |
| **ACP estandarizado** | El ACP de la matriz de correlación, tras dividir cada variable por su desviación típica |
| **Brecha espectral** | λ₁ − λ₂, que controla la estabilidad de la primera componente |
| **Deflación** | Restar λ v vᵀ de una matriz para retirar un par propio ya hallado |
| **Blanqueo** | Dividir las puntuaciones por √λᵢ, de modo que la covarianza pase a ser la identidad |

---

## Autoevaluación

**1. Una herramienta informa de que una componente principal explica el 100% de la varianza de un conjunto de datos. ¿Qué compruebas antes de creerlo?**
> Si la razón divide por la varianza total. Calcula la traza de la matriz de covarianza y compárala con el primer valor propio; el `explained_variance_ratio` de IX, por ejemplo, devuelve 1 para cualquier conjunto de datos cuando solo se conserva una componente. Un 100% genuino significa que los datos centrados están sobre una recta.

**2. Dos bibliotecas devuelven las primeras componentes (0.6, 0.8) y (−0.6, −0.8) sobre los mismos datos. ¿Se equivoca una de ellas?**
> No. Los vectores propios y los vectores singulares están definidos salvo el signo, así que ambas describen la misma componente; las puntuaciones solo difieren en el signo. Compara |qᵀq′|, que aquí vale 1.

**3. El ACP de IX da componentes distintas sobre las mismas medidas en centímetros y en kilómetros. ¿Es una propiedad del ACP?**
> No. Multiplicar todas las variables por el mismo factor multiplica S por su cuadrado y deja los vectores propios sin cambios. La diferencia viene de la tolerancia absoluta de 10^-10 de la iteración de la potencia de IX, por debajo de la cual caen las pequeñas varianzas en kilómetros. Cambiar la escala de una sola variable, en cambio, sí cambia las componentes.

**4. Una muestra da λ₁ = 1.00 y λ₂ = 0.99. ¿Hasta dónde confiarías en la dirección de la primera componente?**
> No mucho. La brecha espectral es 0.01, así que por Davis–Kahan una perturbación de S de tamaño 0.001 ya podría girar la componente un ángulo cuyo seno ronda 0.1. Informa del plano de las dos primeras componentes, y comprueba su estabilidad, por ejemplo por remuestreo.

**Criterio de aprobación:** Obtener las componentes principales a partir de la varianza, relacionarlas con el error de reconstrucción y con la SVD de los datos centrados, calcular una razón de varianza explicada con el denominador correcto, explicar el efecto de las unidades, del signo y de las brechas espectrales pequeñas, distinguir el ACP del blanqueo, y rastrear dónde la razón, la prueba de parada y el estado guardado de IX se apartan de las definiciones.

---

## Base de investigación

- K. Pearson, «On lines and planes of closest fit to systems of points in space», *Philosophical Magazine* 2, 1901: el subespacio mejor ajustado
- H. Hotelling, «Analysis of a complex of statistical variables into principal components», *Journal of Educational Psychology* 24, 1933: las componentes principales como direcciones de mayor varianza
- C. Eckart y G. Young, «The approximation of one matrix by another of lower rank», *Psychometrika* 1, 1936: la mejor aproximación de bajo rango
- C. Davis y W. M. Kahan, «The rotation of eigenvectors by a perturbation. III», *SIAM Journal on Numerical Analysis* 7, 1970: la estabilidad de los vectores propios y la brecha espectral
- I. T. Jolliffe, *Principal Component Analysis*, 2.ª ed., Springer, 2002: el ACP, la varianza explicada y la elección de escalas
- L. I. Smith, «A tutorial on principal components analysis», 2002: el ejemplo de diez puntos que usa la prueba del skill de IX
- G. H. Golub y C. F. Van Loan, *Matrix Computations*, 4.ª ed., Johns Hopkins University Press, 2013: la SVD, la iteración de la potencia y la deflación
- I. T. Jolliffe y J. Cadima, «Principal component analysis: a review and recent developments», *Philosophical Transactions of the Royal Society A* 374, 2016: el ACP estandarizado y la interpretación
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
