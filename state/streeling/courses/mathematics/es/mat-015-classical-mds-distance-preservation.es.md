---
module_id: mat-015-classical-mds-distance-preservation
department: mathematics
course: MDS clásico y preservación de distancias
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-013-distances-kernels-psd, mat-014-pca-variance-preservation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# MDS clásico y preservación de distancias — Recuperar puntos a partir de sus distancias, y saber cuándo no se puede

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Convertir una matriz de distancias en una matriz de productos escalares por doble centrado, y explicar por qué el resultado solo queda fijado salvo un movimiento rígido
- Enunciar el criterio de Schoenberg, Young y Householder: una matriz de distancias es euclídea exactamente cuando su matriz doblemente centrada es semidefinida positiva
- Calcular una configuración de MDS clásico, y mostrar que sobre distancias euclídeas devuelve las puntuaciones del ACP
- Reconocer disimilitudes no euclídeas por los valores propios negativos de la matriz doblemente centrada, y medir cuánto deforman la configuración
- Distinguir el MDS clásico del MDS métrico por stress, del MDS no métrico y de Isomap
- Rastrear qué garantiza `classical_mds` de IX, y dónde un recorte silencioso o una tolerancia absoluta cambia la respuesta

---

## 1. De las distancias a los productos escalares

Supongamos que solo se conocen las distancias dᵢⱼ entre n puntos, y no los puntos mismos. La ley de los cosenos relaciona distancias y productos escalares: ‖xᵢ − xⱼ‖² = ‖xᵢ‖² + ‖xⱼ‖² − 2 xᵢ · xⱼ. Los productos escalares dependen del origen y las distancias no, así que las distancias determinan los productos escalares una vez elegido un origen. El escalamiento clásico elige el centroide x̄. Escribamos D⁽²⁾ para la matriz de distancias al cuadrado d²ᵢⱼ, y J = I − (1/n) 11ᵀ para la **matriz de centrado**. La **matriz doblemente centrada** B = −½ J D⁽²⁾ J tiene las entradas bᵢⱼ = −½ (d²ᵢⱼ − rᵢ − rⱼ + g), donde rᵢ es la media de la fila i de D⁽²⁾ y g la media de todas sus entradas, y es igual a la matriz de Gram de los puntos centrados: bᵢⱼ = (xᵢ − x̄) · (xⱼ − x̄). Cada fila de B suma 0, porque los puntos centrados suman 0. El centrado debe aplicarse a las distancias al cuadrado; aplicado a las distancias mismas, no tiene ningún sentido geométrico.

Las distancias no cambian cuando los puntos se trasladan, se giran o se reflejan, así que ningún método puede recuperar la configuración más allá de tal **movimiento rígido**. El doble centrado elimina la traslación al llevar el centroide al origen; la rotación y la reflexión quedan, y el §4 vuelve sobre ellas.

### Ejercicio práctico

Tres puntos de una recta están a distancias mutuas d₁₂ = 1, d₂₃ = 2 y d₁₃ = 3. Calcula B y recupera los puntos.

> *Solución:* D⁽²⁾ = [[0, 1, 9], [1, 0, 4], [9, 4, 0]], con medias de fila 10/3, 5/3 y 13/3 y media global 28/9. Entonces b₁₁ = −½(0 − 20/3 + 28/9) = 16/9, y del mismo modo B = xxᵀ con x = (−4/3, −1/3, 5/3). B tiene rango 1 y el único valor propio no nulo ‖x‖² = 14/3, así que los puntos están en una recta, en −4/3, −1/3 y 5/3: los puntos 0, 1 y 3 desplazados por su media 4/3. La respuesta reflejada (4/3, 1/3, −5/3) respeta las distancias igual de bien.

---

## 2. ¿Cuándo es euclídea una matriz de distancias?

Una matriz simétrica D con diagonal nula es una **matriz de distancias euclídea** si hay puntos x₁, …, xₙ de algún ℝᵐ con dᵢⱼ = ‖xᵢ − xⱼ‖. El criterio de Schoenberg (1935) y de Young y Householder (1938) afirma que D es euclídea exactamente cuando B es semidefinida positiva, y que la menor dimensión m que sirve es el rango de B. Una dirección es el §1: una matriz de Gram es SDP (MAT-013). Para la otra, una matriz B SDP se factoriza como B = YYᵀ con Y = QΛ^(1/2) (MAT-005), y las filas de Y son puntos con las distancias correctas, ya que bᵢᵢ + bⱼⱼ − 2bᵢⱼ = d²ᵢⱼ para toda D simétrica con diagonal nula.

Como B1 = 0, y Jx = x siempre que las entradas de x suman 0, xᵀBx = −½ xᵀD⁽²⁾x para tales x: D es euclídea exactamente cuando xᵀD⁽²⁾x ≤ 0 para todo x cuyas entradas suman 0. Un solo vector x con xᵀBx < 0 es un **testigo** de que ninguna configuración, en ninguna dimensión, tiene esas distancias.

La desigualdad triangular es necesaria pero no suficiente. En un espacio euclídeo, la igualdad d(a, c) = d(a, b) + d(b, c) obliga a b a estar en el segmento de a a c, a las distancias prescritas de ambos. Las distancias de camino más corto en un grafo alcanzan a menudo esta igualdad, y entonces las restricciones pueden contradecirse.

### Ejercicio práctico

El grafo estrella K₁,₃ tiene un centro unido a tres hojas. Sus distancias de camino más corto valen 1 del centro a cada hoja y 2 entre hojas, y cumplen la desigualdad triangular. ¿Son euclídeas?

> *Solución:* No. Cada par de hojas está a distancia 2 = 1 + 1 pasando por el centro, así que en un espacio euclídeo el centro sería el punto medio de cada par de hojas. El punto medio de las hojas 1 y 2 y el de las hojas 1 y 3 solo coinciden si las hojas 2 y 3 coinciden, y sin embargo están a distancia 2. En números: D⁽²⁾ tiene medias de fila 3/4 para el centro y 9/4 para las hojas, y media global 15/8, así que la entrada diagonal del centro en B es b₀₀ = −½(0 − 3/2 + 15/8) = −3/16 < 0. El vector unitario e₀ es un testigo, y los valores propios de B son 2, 2, 0 y −1/4.

---

## 3. MDS clásico y ACP

El **escalamiento multidimensional clásico** (Torgerson 1952), que Gower (1966) llama análisis de coordenadas principales, calcula la descomposición propia B = QΛQᵀ con λ₁ ≥ λ₂ ≥ …, conserva los k mayores valores propios, y devuelve la configuración n × k Y = Q_kΛ_k^(1/2): la fila i contiene las coordenadas del punto i. Cuando D es euclídea, YYᵀ es la mejor aproximación de rango k de B en la norma de Frobenius (Eckart–Young, MAT-006); en general, es la mejor aproximación semidefinida positiva. Este criterio sobre B, a menudo llamado **strain**, es lo que optimiza el MDS clásico, y no las distancias mismas.

Cuando D procede de puntos con una matriz de datos centrada X_c de tamaño n × p, B = X_cX_cᵀ. Con la SVD X_c = UΣVᵀ del MAT-006, B = UΣ²Uᵀ, así que los valores propios no nulos de B son los σᵢ², que valen n − 1 veces las varianzas del MAT-014, e Y = U_kΣ_k = X_cV_k: el MDS clásico devuelve exactamente las puntuaciones del ACP, salvo el signo de cada columna. Gower describió esta dualidad entre los problemas propios n × n y p × p. El MDS es la elección natural cuando solo se conocen distancias, o cuando p es mucho mayor que n. El ACP es más barato cuando n es grande y p pequeño: su problema propio es p × p, y nunca forma las n² distancias.

### Ejercicio práctico

El MAT-014 encontró las varianzas 8/3 y 2/3 para los cuatro puntos (±2, 0) y (0, ±1). ¿Cuáles son los valores propios de B para estos puntos, y qué configuración devuelve el MDS clásico con k = 2?

> *Solución:* Los puntos ya están centrados, así que B = X_cX_cᵀ, cuyos valores propios no nulos son los de X_cᵀX_c = diag(8, 2): n − 1 = 3 veces 8/3 y 2/3. Los otros dos valores propios son 0, ya que B tiene rango 2. Los vectores propios son (1, −1, 0, 0)/√2 para 8 y (0, 0, 1, −1)/√2 para 2, y multiplicarlos por √8 y √2 devuelve los puntos (±2, 0) y (0, ±1), salvo el signo de cada coordenada.

---

## 4. Lo que las distancias no dicen: movimientos rígidos y empates

La configuración que devuelve el MDS clásico está centrada, pero los datos no determinan su orientación. Cada vector propio puede sustituirse por su opuesto, lo que refleja la configuración. Cuando dos valores propios son iguales, cualquier base ortonormal de su espacio propio vale tanto como otra, así que la configuración puede girar libremente en ese plano. El cuadrado unidad es el caso más simple: su matriz B tiene valores propios 1, 1, 0 y 0, y cualquier rotación del cuadrado alrededor de su centro es una respuesta igual de válida. Dos mapas MDS de los mismos datos, de dos bibliotecas o de dos ejecuciones, pueden por tanto diferir en una rotación o una reflexión sin que ninguno sea erróneo.

Para comparar dos configuraciones Y₁ e Y₂, compara sus distancias, o alinéalas primero: la matriz ortogonal R que minimiza ‖Y₁ − Y₂R‖_F es R = WZᵀ, donde Y₂ᵀY₁ = WΣZᵀ es una SVD (Schönemann 1966). Este alineamiento de **Procrustes ortogonal** elimina exactamente la ambigüedad que dejan las distancias.

### Ejercicio práctico

¿Por qué el MDS clásico solo puede recuperar una configuración salvo un movimiento rígido, y qué parte de ese movimiento fija?

> *Solución:* Las traslaciones, rotaciones y reflexiones conservan todas las distancias, así que dos configuraciones relacionadas por una de ellas tienen la misma matriz de distancias, y nada calculado a partir de las distancias puede distinguirlas. El doble centrado fija la traslación al llevar el centroide al origen. El resto queda en manos del solucionador propio: el signo de cada vector propio y, cuando hay valores propios empatados como en el cuadrado, la elección de base en su espacio propio.

---

## 5. Disimilitudes no euclídeas, stress e Isomap

Cuando B tiene valores propios negativos, ninguna configuración en ninguna dimensión reproduce D, y el MDS clásico solo conserva valores propios positivos. Descartar los negativos cambia las distancias, y su tamaño mide cuán lejos está D de ser euclídea. Mardia (1978) propuso la fracción Σᵢ≤ₖ λᵢ / Σᵢ |λᵢ|, que se queda por debajo de 1 siempre que hay valores propios negativos. Un gráfico de todos los valores propios, negativos incluidos, es la mejor guía para elegir k.

El ciclo C₄, cuatro puntos en anillo con distancias de camino más corto 1 entre vecinos y 2 en diagonal, es el ejemplo más pequeño. Como en la estrella, d(0, 2) = d(0, 1) + d(1, 2) y d(0, 2) = d(0, 3) + d(3, 2) harían de los puntos 1 y 3 el punto medio de 0 y 2, y sin embargo están a distancia 2. B tiene los valores propios 2, 2, 0 y −1, y la fracción de Mardia para k = 2 es 4/5.

El MDS clásico es un miembro de una familia. El **MDS métrico** minimiza un **stress**, como Σ (dᵢⱼ − ‖yᵢ − yⱼ‖)², directamente sobre las distancias y por iteración; SMACOF, que funciona por mayorización, es el algoritmo de referencia, y la solución clásica es un punto de partida habitual (Borg y Groenen 2005). El **MDS no métrico** (Kruskal 1964) solo usa el orden de las disimilitudes: ajusta una transformación monótona de ellas junto con la configuración, lo que conviene a valoraciones y clasificaciones cuyos valores numéricos significan poco. **Isomap** (Tenenbaum, de Silva y Langford 2000) aplica el MDS clásico a las distancias de camino más corto de un grafo de vecindad, para desplegar datos que están sobre una superficie curva; esas distancias son distancias de grafo y, como las de C₄, no tienen por qué ser euclídeas.

### Ejercicio práctico

Para C₄, calcula B, sus valores propios y las distancias de la configuración de MDS clásico con k = 2.

> *Solución:* Cada fila de D⁽²⁾ es una rotación de (0, 1, 4, 1), con media 3/2, y la media global es 3/2, así que bᵢᵢ = 3/4, bᵢⱼ = 1/4 entre vecinos y −5/4 en diagonal. El vector (1, −1, 1, −1)/2 es un vector propio para −1, el vector de unos para 0, y el plano ortogonal a ambos lleva el valor propio doble 2. Descartar −1 suma ¼ vvᵀ a B, con v = (1, −1, 1, −1), lo que da entradas diagonales 1, entradas 0 entre vecinos y −1 en diagonal: la configuración es un cuadrado de lado √2 ≈ 1.414 y diagonal 2. Las distancias en diagonal son exactas, las de vecinos se estiran de 1 a 1.414, y la fracción de Mardia es 4/(2 + 2 + 0 + 1) = 4/5.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de `classical_mds`, `pairwise_euclidean` y `symmetric_eigen` a Python, cuyos flotantes son binary64 IEEE como el `f64` de Rust: son predicciones, y el §7 propone comprobarlas.

**MDS** (`crates/ix-unsupervised`). [`classical_mds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L49) rechaza [k = 0 y k ≥ n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L60), eleva la entrada al cuadrado tras promediarla con su traspuesta, la centra doblemente con la [fórmula del §1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L89), y pasa B a [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L95), el método de Jacobi del MAT-005. Su único llamador fuera de las pruebas es la función de tabla DuckDB `ix_mds_project`, que [limita k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/tablefn.rs#L344) al número de variables y a n − 1, y [construye las distancias](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/tablefn.rs#L345) a partir de los vectores de entrada con `pairwise_euclidean`; ninguna herramienta MCP expone el MDS. Por las interfaces de IX, el MDS clásico solo ve por tanto distancias euclídeas calculadas a partir de variables, donde el §3 muestra que devuelve las puntuaciones del ACP. La elevación al cuadrado y la configuración dicen:

```rust
    // Square and symmetrize the distance matrix.
    let mut sq = Array2::<f64>::zeros((n, n));
    for i in 0..n {
        for j in 0..n {
            let d = 0.5 * (distances[[i, j]] + distances[[j, i]]);
            sq[[i, j]] = d * d;
        }
    }
```

```rust
    // Full symmetric eigendecomposition via ix-math::eigen — returns pairs
    // already sorted in descending order, so we just take the top k.
    let (eigenvalues, eigenvectors) = symmetric_eigen(&b)?;

    let mut embedding = Array2::<f64>::zeros((n, k));
    for r in 0..k {
        let lambda = eigenvalues[r].max(0.0);
        let scale = lambda.sqrt();
        for i in 0..n {
            embedding[[i, r]] = eigenvectors[[i, r]] * scale;
        }
    }
```

- **Una entrada no euclídea se proyecta sin aviso.** La documentación del módulo dice que el MDS es [«a perfect fit»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L16) para los [«Non-metric similarity data»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L17) y para los [grafos a través de sus distancias de camino más corto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L18). La función nunca informa de un valor propio negativo: [sustituye cada uno por 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L99) antes de la raíz cuadrada. Sobre C₄ con k = 2, devuelve el cuadrado de lado √2 del §5, con un error medio de distancia de 2(√2 − 1)/3 ≈ 0.276; k = 3 da las mismas distancias, ya que el tercer valor propio es 0. Sobre la estrella, con k = 2 o 3, las hojas forman un triángulo equilátero de lado 2 y el centro cae en su centroide, a 2/√3 ≈ 1.155 de cada hoja en lugar de 1, con un error medio de unos 0.077. Sobre el ciclo de 6 vértices, cuya B tiene los valores propios 6, 6, 3/2, 0, −2 y −2, k = 5 devuelve una quinta columna de ceros. Los datos no métricos, en el sentido del método de Kruskal, piden un ajuste a rangos, que la función no hace; trata cada número como una distancia.
- **Las entradas negativas y asimétricas pasan en silencio.** La documentación dice que la función [«symmetrizes defensively»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L48). [Promedia dᵢⱼ y dⱼᵢ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L71) sea cual sea su diferencia, y [eleva el resultado al cuadrado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L72), así que una entrada negativa pierde su signo: [[0, −1], [−1, 0]] da la misma proyección ±0.5 que [[0, 1], [1, 0]], y un par de entradas 0 y 2 se convierte en una distancia de 1, sin error. No se comprueban ni el signo, ni la simetría, ni la diagonal nula.
- **Una tolerancia absoluta aplasta las configuraciones pequeñas.** `symmetric_eigen` se detiene cuando la norma fuera de la diagonal está [por debajo de 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47), una [prueba absoluta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L82), como mostró el MAT-013 para la prueba SDP. Para el cuadrado unidad escalado por s, las únicas entradas fuera de la diagonal de B son −s²/2 en (0, 2) y (1, 3), de norma s²/√2. Con s = 2^-19 ≈ 1.91 · 10^-6, dos rotaciones recuperan el cuadrado. Con 2^-20 ≈ 9.54 · 10^-7 y por debajo, no hay ninguna rotación: los valores propios son las entradas diagonales s²/2, los vectores propios son vectores de coordenadas, y con k = 2 dos esquinas vecinas quedan a s/√2 del origen, en ejes distintos, mientras las otras dos quedan en el origen. El error medio de distancia es entonces 0.5 s, la mitad del lado. `ix_mds_project` calcula las mismas distancias, bit a bit, a partir de las esquinas del cuadrado escalado, así que bastan puntos separados por un micrómetro, con coordenadas en metros, para provocarlo.
- **Las pruebas solo usan entradas euclídeas.** La [prueba del cuadrado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L150) exige un error medio [por debajo de 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L162) donde el error previsto es de unos 1.5 · 10^-16, y la [prueba coplanar](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L166) usa cinco puntos de un plano. Ninguna de las cinco pruebas de `mds.rs` proyecta una matriz no euclídea o una configuración pequeña, ni compara el resultado con el ACP.
- **Solo MDS clásico.** `crates/ix-unsupervised` no ofrece minimización del stress, SMACOF, MDS no métrico ni Isomap; la documentación solo menciona Isomap como usuario del MDS.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

IX proyecta la estrella con k = 2 y con k = 3 y devuelve las mismas distancias. ¿Por qué, y adónde va el centro?

> *Solución:* B tiene los valores propios 2, 2, 0 y −1/4. Con k = 3, la tercera columna procede del valor propio 0, salvo redondeo, y su vector propio (1, 1, 1, 1)/2 desplaza cada punto en la misma cantidad ínfima, lo que no cambia ninguna distancia. El valor propio −1/4 se descarta en los dos casos, y nada en el resultado lo dice. Descartarlo suma ¼ vvᵀ a B, con v = (3, −1, −1, −1)/√12, lo que anula la fila del centro y da a las hojas bᵢᵢ = 4/3 y bᵢⱼ = −2/3: las hojas forman un triángulo equilátero de lado 2 alrededor del origen, y el centro está en el origen, a 2/√3 ≈ 1.155 de cada hoja. La fracción de Mardia, 4/(4 + 1/4) = 16/17 ≈ 0.941, habría señalado la pérdida.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Entrada euclídea.** Llamar a `classical_mds` sobre las distancias de los puntos 0, 1 y 3 con k = 1, y sobre `pairwise_euclidean` de (±2, 0) y (0, ±1) con k = 2. Predicción: ±(−4/3, −1/3, 5/3) con un margen de 10^-12, y los cuatro puntos mismos, salvo el signo de cada columna, con un margen de 10^-12.
2. **Frente al ACP.** Llamar a `ix_mds_project` con k = 2 sobre los diez puntos del tutorial de Lindsay Smith, y calcular las puntuaciones del ACP por la SVD de los datos centrados. Predicción: las columnas coinciden salvo el signo con un margen de 10^-12.
3. **El cuadrado unidad.** Llamar a `classical_mds` con k = 2 sobre la matriz de distancias de `test_mds_recovers_2d_square`. Predicción: un error medio de distancia por debajo de 10^-15, de unos 1.5 · 10^-16.
4. **Distancias de grafo.** Llamar a `classical_mds` sobre C₄ y sobre la estrella con k = 2 y k = 3, calcular sus matrices B como en el §1, y pasarlas a `symmetric_eigen`. Predicción: los valores propios del §5 y del §2 con un margen de 10^-12, negativos incluidos; para C₄, un cuadrado de lado √2 y un error medio de unos 0.276 para los dos valores de k; para la estrella, hojas a distancia 2, un centro a unos 1.155 de cada una, y un error medio de unos 0.077. Sobre el ciclo de 6 vértices con k = 5, una quinta columna de ceros.
5. **Entrada inválida.** Llamar a `classical_mds` con k = 1 sobre [[0, −1], [−1, 0]], sobre [[0, 1], [1, 0]] y sobre [[0, 0], [2, 0]]. Predicción: las tres devuelven `Ok`, con la proyección ±0.5.
6. **La escala.** Llamar a `classical_mds` con k = 2 sobre el cuadrado unidad escalado por 2^-19, 2^-20 y 2^-21, y a `ix_mds_project` con k = 2 sobre las esquinas (0, 0), (s, 0), (s, s) y (0, s) para s = 2^-19 y 2^-20. Predicción: con 2^-19 se recupera el cuadrado; con 2^-20 y 2^-21, dos esquinas quedan en el origen y el error medio es 0.5 s.

### Ejercicio práctico

¿Para qué factores de escala s devuelve `symmetric_eigen` la diagonal de B sin cambios para el cuadrado unidad escalado por s, y por qué eso hace de 2^-20 la primera potencia de dos que falla?

> *Solución:* B escala como s², y sus entradas fuera de la diagonal valen −s²/2 en (0, 2) y (1, 3) y 0 en el resto, así que la norma que el bucle compara con 10^-12 es √(2 · s⁴/4) = s²/√2. Está por debajo de 10^-12 cuando s < (√2 · 10^-12)^(1/2) ≈ 1.19 · 10^-6. La potencia 2^-20 ≈ 9.54 · 10^-7 está por debajo, mientras que 2^-19 ≈ 1.91 · 10^-6 está por encima. Por debajo del umbral, los cuatro valores propios valen todos s²/2 salvo redondeo, y los dos vectores propios conservados son vectores de coordenadas, que dejan las otras dos esquinas en el origen. Una prueba relativa, que comparara la norma fuera de la diagonal con la norma de B, no dependería de s.

---

## 8. Errores comunes

- **Centrar las distancias en lugar de sus cuadrados.** El doble centrado convierte distancias al cuadrado en productos escalares; aplicado a las distancias sin más, da una matriz sin ningún sentido geométrico.
- **Fiarse de un mapa construido con disimilitudes no euclídeas.** Mira los valores propios negativos de B antes de leer distancias en la imagen; un valor propio negativo comparable a los conservados significa que el mapa deforma los datos.
- **Dar por suficiente la desigualdad triangular.** Las distancias de grafo, como las de una estrella o un ciclo, la cumplen y aun así no son euclídeas.
- **Comparar dos mapas coordenada a coordenada.** Los signos y, para valores propios empatados, rotaciones enteras son arbitrarios; alinea los mapas con Procrustes, o compara distancias.
- **Llamar al MDS clásico «MDS métrico» o «MDS no métrico».** Minimiza el strain sobre B; la minimización del stress y los ajustes a rangos son métodos distintos, con resultados distintos sobre datos no euclídeos.
- **Pedir más dimensiones que valores propios positivos.** Las columnas de más proceden de valores propios nulos o de valores propios negativos recortados; no aportan nada.
- **Usar una tolerancia absoluta.** Una prueba de parada que ignora el tamaño de B hace depender la respuesta de las unidades de las distancias.
- **Simetrizar sin mirar.** Una «distancia» negativa o muy asimétrica suele ser un error en los datos; promediar y elevar al cuadrado lo ocultan.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Matriz de centrado** | J = I − (1/n) 11ᵀ, que resta la media |
| **Matriz doblemente centrada** | B = −½ J D⁽²⁾ J, la matriz de Gram de los puntos centrados cuando D es euclídea |
| **Matriz de distancias euclídea** | Una matriz de las distancias entre puntos de algún ℝᵐ |
| **Criterio de Schoenberg** | D es euclídea exactamente cuando B es semidefinida positiva; la dimensión necesaria es el rango de B |
| **MDS clásico** | La configuración Q_kΛ_k^(1/2) construida con los k mayores valores propios de B, también llamada análisis de coordenadas principales |
| **Strain** | La discrepancia entre B y la matriz de Gram de la configuración, que el MDS clásico minimiza |
| **Stress** | La discrepancia entre las distancias dadas y las de la configuración, que el MDS métrico minimiza |
| **MDS no métrico** | Un MDS que solo ajusta el orden de las disimilitudes |
| **Criterio de Mardia** | La parte Σᵢ≤ₖ λᵢ / Σᵢ |λᵢ| de los valores propios de B que conserva una configuración de dimensión k |
| **Procrustes ortogonal** | La rotación o reflexión que mejor alinea una configuración con otra, calculada con una SVD |
| **Isomap** | El MDS clásico aplicado a las distancias de camino más corto de un grafo de vecindad |

---

## Autoevaluación

**1. Un mapa MDS de 50 productos parece convincente, y su matriz doblemente centrada tiene un valor propio mayor de 40 y uno menor de −25. ¿Qué concluyes?**
> Las disimilitudes están lejos de ser euclídeas: ninguna configuración las reproduce, y descartar un valor propio negativo de más de la mitad del mayor mueve muchas distancias. Como el segundo valor propio es a lo sumo 40, la fracción de Mardia para un mapa en dos dimensiones es a lo sumo 80/105 ≈ 0.76. Lee el mapa con cautela; un MDS métrico o no métrico por stress puede ajustar mejor los datos, o quizá haya que replantear la propia disimilitud.

**2. ¿Por qué el MDS clásico sobre las distancias euclídeas de un conjunto de datos da la misma imagen que el ACP, y cuándo usarías aun así el MDS?**
> Porque B = X_cX_cᵀ, cuyos vectores propios multiplicados por los valores singulares son las puntuaciones del ACP X_cV_k. Usa el MDS cuando solo hay distancias disponibles, o cuando las variables superan con mucho a las observaciones; usa el ACP cuando hay muchas observaciones y pocas variables.

**3. Dos ejecuciones del MDS sobre los mismos datos devuelven mapas que difieren en una rotación de 30°. ¿Es erróneo uno de ellos?**
> No necesariamente. Si los dos mayores valores propios de B son iguales, o casi, cualquier rotación en su plano respeta igual de bien las distancias, y el solucionador propio elige una. Compara las distancias de los dos mapas, o alinéalos con Procrustes ortogonal; si coinciden, los dos son correctos.

**4. `classical_mds` de IX devuelve una proyección para distancias de camino más corto sobre un ciclo, sin ningún aviso. ¿Qué compruebas antes de usarla?**
> Calcula B y sus valores propios con `symmetric_eigen`, ya que `classical_mds` recorta los valores propios negativos a 0 sin informar de ello. Para C₄, el valor propio −1 junto a dos valores propios 2 muestra que el mapa estira los lados de 1 a √2. Comprueba también la escala: con distancias en torno a 10^-6 o menores, la tolerancia absoluta del solucionador propio puede saltarse por completo las rotaciones.

**Criterio de aprobación:** Centrar doblemente una matriz de distancias y recuperar una configuración, decidir si una matriz de distancias es euclídea y dar un testigo cuando no lo es, relacionar el MDS clásico con el ACP, explicar las ambigüedades de reflexión y rotación, medir el efecto de los valores propios negativos, distinguir los MDS clásico, métrico y no métrico, y rastrear dónde `classical_mds` de IX oculta un valor propio negativo o aplasta una configuración pequeña.

---

## Base de investigación

- I. J. Schoenberg, «Remarks to Maurice Fréchet's article …», *Annals of Mathematics* 36, 1935: qué espacios de distancias se sumergen en el espacio de Hilbert
- G. Young y A. S. Householder, «Discussion of a set of points in terms of their mutual distances», *Psychometrika* 3, 1938: la matriz de Gram de las distancias y la dimensión necesaria
- W. S. Torgerson, «Multidimensional scaling: I. Theory and method», *Psychometrika* 17, 1952: el escalamiento clásico
- J. B. Kruskal, «Multidimensional scaling by optimizing goodness of fit to a nonmetric hypothesis», *Psychometrika* 29, 1964: el stress y el MDS no métrico
- J. C. Gower, «Some distance properties of latent root and vector methods used in multivariate analysis», *Biometrika* 53, 1966: las coordenadas principales y la dualidad con el ACP
- P. H. Schönemann, «A generalized solution of the orthogonal Procrustes problem», *Psychometrika* 31, 1966: el alineamiento de dos configuraciones
- K. V. Mardia, «Some properties of classical multi-dimensional scaling», *Communications in Statistics — Theory and Methods* 7, 1978: la bondad de ajuste en presencia de valores propios negativos
- J. B. Tenenbaum, V. de Silva y J. C. Langford, «A global geometric framework for nonlinear dimensionality reduction», *Science* 290, 2000: Isomap
- I. Borg y P. J. F. Groenen, *Modern Multidimensional Scaling*, 2.ª ed., Springer, 2005: el stress, SMACOF y el escalamiento clásico
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
