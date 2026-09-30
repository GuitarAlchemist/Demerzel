---
module_id: mat-018-clustering-density-validity
department: mathematics
course: Agrupamiento, densidad y validez de los clústeres
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-009-estimation-uncertainty-sampling, mat-013-distances-kernels-psd]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Agrupamiento, densidad y validez de los clústeres — Qué minimiza k-means, qué garantiza EM y cuándo engañan las puntuaciones

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Enunciar el objetivo que minimiza k-means, y mostrar por qué el algoritmo de Lloyd se detiene en un punto fijo que depende del arranque
- Definir los clústeres basados en densidad, con puntos núcleo, puntos frontera y ruido, y decir qué controlan ε y minPts
- Deducir EM para una mezcla gaussiana, probar que la log-verosimilitud nunca disminuye, y explicar por qué la verosimilitud misma no tiene máximo
- Calcular la puntuación de silueta, y decir qué recompensa
- Construir casos en los que la inercia, la verosimilitud y la silueta prefieren todas la partición equivocada
- Rastrear qué garantizan `KMeans`, `DBSCAN`, `GMM` y `silhouette_score` de IX, y dónde sus comentarios, sus manejadores y sus pruebas prometen más de lo que el código entrega

---

## 1. Qué minimiza k-means

Dados puntos x_1, …, x_n en ℝ^p y un número k, k-means busca una partición C_1, …, C_k y centros μ_1, …, μ_k que minimicen la **inercia**, la suma de cuadrados dentro de los clústeres W = Σ_c Σ_(i∈C_c) ‖x_i − μ_c‖². Para una partición fija, el mejor centro de cada clúster es su media, y entonces W = Σ_c (1/(2|C_c|)) Σ_(i,j∈C_c) ‖x_i − x_j‖²: k-means recompensa los clústeres cuyos puntos están cerca unos de otros en la distancia euclídea del MAT-013, sea cual sea su forma. Para centros fijos, la mejor partición envía cada punto a su centro más cercano, así que los clústeres son las celdas de un diagrama de Voronoi, y dos clústeres están separados por la mediatriz de sus centros, un hiperplano.

**El algoritmo de Lloyd** (Lloyd 1982) alterna estos dos pasos. Ninguno puede aumentar W, y hay un número finito de particiones, así que, con una regla fija para los empates, la iteración llega a una partición que el paso siguiente deja sin cambios. Ese punto fijo no tiene por qué ser el mínimo global, ni siquiera un mínimo local para el traslado de un solo punto a otro clúster (el rectángulo siguiente muestra ambas cosas): minimizar W es NP-difícil, ya para k = 2 cuando la dimensión forma parte de la entrada (Aloise et al. 2009).

Como ejemplo resuelto, toma las cuatro esquinas de un rectángulo de 4 × 1, (0, 0), (0, 1), (4, 0) y (4, 1), con k = 2. La división en un par izquierdo y un par derecho tiene centros (0, 1/2) y (4, 1/2), y W = 4 · (1/2)² = 1. La división en un par inferior y un par superior tiene centros (2, 0) y (2, 1), y W = 4 · 2² = 16; también es un punto fijo, ya que cada esquina está a distancia al cuadrado 4 de su propio centro y 5 del otro. Sin embargo, mover solo la esquina (0, 0) al par superior baja W a 34/3 ≈ 11.3: la media del par superior se acerca al punto nuevo, algo que el paso de asignación de Lloyd, que compara distancias a los centros actuales, no tiene en cuenta. A qué punto fijo llega Lloyd depende del arranque. **k-means++** (Arthur y Vassilvitskii 2007) extrae el primer centro de forma uniforme, y cada uno de los siguientes con probabilidad proporcional a D(x)², el cuadrado de la distancia de x al centro más cercano ya elegido. Desde (0, 0), las otras esquinas tienen D² = 1, 16 y 17, así que el mal segundo centro (0, 1) tiene probabilidad 1/34, frente a 1/3 con una extracción uniforme; por simetría, lo mismo vale desde cada esquina. En esperanza, el arranque k-means++ por sí solo, antes de cualquier paso de Lloyd, queda a un factor 8(ln k + 2) de la inercia óptima, y reiniciar desde varias semillas, como en el muestreo reproducible del MAT-009, quedándose con la inercia más baja, reduce aún más el riesgo.

### Ejercicio práctico

¿Por qué k-means con k = n puede alcanzar inercia cero y aun así carecer de sentido?

> *Solución:* Cada punto se convierte en su propio centroide, así que W = 0. La inercia óptima solo puede bajar al crecer k: partir un clúster en dos y dar a cada mitad su propia media no puede aumentar W, ya que la media anterior sigue disponible para ambas mitades. La inercia sola no puede, por tanto, elegir k, y su mínimo sobre todos los k es la partición en unitarios, que no dice nada de los datos.

---

## 2. Clústeres basados en densidad

DBSCAN (Ester, Kriegel, Sander y Xu 1996) define los clústeres por la densidad en lugar de por centros. El ε-entorno N_ε(x) es el conjunto de puntos de los datos a distancia como mucho ε de x, incluido x. Un punto es un **punto núcleo** cuando N_ε(x) tiene al menos minPts puntos. Un punto y es directamente alcanzable por densidad desde un punto núcleo x cuando y ∈ N_ε(x), y alcanzable por densidad cuando una cadena de tales pasos lleva de x a y. Un **clúster** es un conjunto maximal de puntos conectados de este modo a través de puntos núcleo; sus puntos que no son puntos núcleo son **puntos frontera**, y los puntos que no pertenecen a ningún clúster son **ruido**.

Qué puntos son puntos núcleo, cómo se agrupan los puntos núcleo en clústeres y qué puntos son ruido no depende del orden de los datos. Un punto frontera, en cambio, puede estar a distancia como mucho ε de puntos núcleo de dos clústeres distintos; la definición lo admite en ambos, y una implementación lo asigna al clúster que lo alcanza primero (Schubert et al. 2017). Un clúster puede tener cualquier forma, siempre que esté conectado a través de regiones densas, pero un único ε fija un único umbral de densidad, así que clústeres de densidades muy distintas no pueden encontrarse todos a la vez. Ester et al. sugieren minPts = 4 para datos en 2 dimensiones, y leer ε en las distancias ordenadas de cada punto a su cuarto vecino más cercano.

k-means no puede separar dos medias lunas entrelazadas, ya que sus dos clústeres siempre están separados por una recta (§5). DBSCAN sí puede, cuando ε está entre la separación de los puntos dentro de una luna y el hueco entre las lunas.

### Ejercicio práctico

Muestra que con minPts = 2 los clústeres de DBSCAN son las componentes conexas, con al menos dos puntos, del grafo que une los puntos a distancia como mucho ε, y que los demás puntos son ruido.

> *Solución:* Con minPts = 2, un punto es un punto núcleo exactamente cuando algún otro punto está a distancia como mucho ε. Un punto frontera tendría que estar a distancia como mucho ε de un punto núcleo sin tener ningún otro punto a distancia como mucho ε, lo cual es imposible, así que no hay puntos frontera. La alcanzabilidad por densidad a través de puntos núcleo es entonces un camino en el grafo, así que los clústeres son sus componentes conexas con al menos dos puntos, y los puntos aislados son ruido. Son los clústeres del agrupamiento jerárquico de enlace simple cortado a la altura ε, con los unitarios llamados ruido.

---

## 3. Mezclas gaussianas y EM

Una mezcla gaussiana modela la densidad como p(x) = Σ_c π_c N(x; μ_c, Σ_c), con pesos π_c ≥ 0 que suman 1. Maximizar la log-verosimilitud ℓ(θ) = Σ_i ln p(x_i) no tiene forma cerrada, pero la tendría si supiéramos qué componente produjo cada punto. **EM** (Dempster, Laird y Rubin 1977) alterna dos pasos. El paso E calcula las **responsabilidades** r_ic = π_c N(x_i; μ_c, Σ_c)/p(x_i), la probabilidad a posteriori de que la componente c haya producido x_i. El paso M ajusta cada componente a los puntos ponderados por sus responsabilidades: con N_c = Σ_i r_ic, toma π_c = N_c/n, μ_c = Σ_i r_ic x_i/N_c, y Σ_c igual a la covarianza ponderada; para una covarianza diagonal, cada varianza es Σ_i r_ic (x_ij − μ_cj)²/N_c.

La log-verosimilitud nunca disminuye. Para cualesquiera pesos q_ic ≥ 0 que sumen 1 sobre c, la desigualdad de Jensen da ln p(x_i) = ln Σ_c q_ic π_c N(x_i; μ_c, Σ_c)/q_ic ≥ Σ_c q_ic ln(π_c N(x_i; μ_c, Σ_c)/q_ic), con igualdad cuando q_ic = r_ic. El paso E hace que esta cota inferior toque ℓ en el θ actual, y el paso M maximiza la cota en θ, así que ℓ(θ_new) ≥ cota(θ_new) ≥ cota(θ_old) = ℓ(θ_old), un paso de minorización–maximización. El argumento solo prueba la monotonía. La convergencia de los iterados a un punto estacionario requiere más condiciones (Wu 1983), y un punto estacionario puede ser un punto de silla o un mal máximo local.

La verosimilitud misma no tiene máximo cuando las varianzas son libres y k ≥ 2. Centra una componente en un punto de los datos x_1 y deja que sus varianzas se encojan: su densidad en x_1 crece sin cota, mientras que una segunda componente con peso positivo, media y varianzas fijos mantiene la densidad de cada punto por encima de una cota positiva, así que ℓ → ∞ (McLachlan y Peel 2000). Por eso las implementaciones ponen un suelo a las varianzas o añaden una distribución a priori, y el suelo decide entonces cuánto puede crecer ℓ. Los datos con valores repetidos lo hacen concreto: una componente situada sobre un valor repetido puede conservar un peso positivo mientras el paso M lleva su varianza hacia 0.

EM también trata las componentes de forma simétrica. Permutarlas no cambia nada, y dos componentes que empiezan con parámetros idénticos los conservan para siempre (ejercicio siguiente). k-means es un límite de EM: con todas las covarianzas iguales a σ²I y pesos iguales y fijos, las responsabilidades tienden a asignaciones duras al centro más cercano cuando σ → 0, y el paso M para las medias se convierte en la actualización de Lloyd (Bishop 2006).

### Ejercicio práctico

Muestra que si dos componentes empiezan con el mismo peso, la misma media y la misma covarianza, EM las mantiene idénticas en cada iteración.

> *Solución:* Si las componentes a y b tienen los mismos π, μ y Σ, entonces π_a N(x_i; μ_a, Σ_a) = π_b N(x_i; μ_b, Σ_b) para todo i, así que r_ia = r_ib. El paso M calcula N_c, la media y la covarianza de cada componente a partir de sus propias responsabilidades con las mismas fórmulas, así que devuelve de nuevo parámetros idénticos. Por inducción, las dos componentes siguen idénticas, y el ajuste tiene en la práctica k − 1 componentes; solo algo externo a EM, como otro arranque, puede separarlas.

---

## 4. Puntuaciones de validez de los clústeres

Sin etiquetas, la calidad de un agrupamiento debe juzgarse solo a partir de los datos, mediante un **índice interno**. La **silueta** (Rousseeuw 1987) compara, para cada punto i, la distancia media a(i) a los demás puntos de su clúster con la menor distancia media b(i) a los puntos de otro clúster: s(i) = (b(i) − a(i))/max(a(i), b(i)), que está en [−1, 1], y un punto solo en su clúster recibe s(i) = 0 por convención. La puntuación de silueta es la media de los s(i). Es alta cuando los clústeres son compactos y están alejados en distancia euclídea, que es también lo que recompensa la inercia: prefiere clústeres redondos y bien separados, y penaliza un clúster largo y curvo cuyos extremos están lejos uno del otro, aunque ese clúster sea el correcto.

Otros índices internos codifican otras preferencias. El índice de Davies–Bouldin (Davies y Bouldin 1979) y el índice de Calinski–Harabasz (Caliński y Harabasz 1974) comparan la dispersión dentro de los clústeres con las distancias entre sus centros, y para las mezclas el BIC (Schwarz 1978) resta de ℓ una penalización que crece con el número de parámetros. Ninguno es neutral: cada uno define qué es un clúster, y una partición puede puntuar bien sin captar la estructura que importa. Cuando existe una verdad de referencia, un **índice externo** como el índice de Rand ajustado (Hubert y Arabie 1985) compara directamente la partición con ella.

Elegir k por una puntuación interna tiene sus propias trampas: la inercia siempre baja al crecer k (§1), la log-verosimilitud de una mezcla puede crecer sin cota (§3), y una silueta que cuenta el ruido de DBSCAN como un clúster lo puntúa como si lo fuera (§6).

### Ejercicio práctico

Para los puntos 0, 1 y 5 en una recta, calcula la puntuación de silueta de las particiones {0, 1}{5}, {0}{1, 5} y {0, 5}{1}. ¿Cuál prefiere, y qué da para tres unitarios?

> *Solución:* Para {0, 1}{5}: s(0) = (5 − 1)/5 = 4/5, s(1) = (4 − 1)/4 = 3/4 y s(5) = 0, así que la puntuación es 31/60 ≈ 0.517. Para {0}{1, 5}: s(0) = 0, s(1) = (1 − 4)/4 = −3/4 y s(5) = (5 − 4)/5 = 1/5, así que la puntuación es −11/60 ≈ −0.183. Para {0, 5}{1}: s(0) = (1 − 5)/5 = −4/5, s(5) = (4 − 5)/5 = −1/5 y s(1) = 0, así que la puntuación es −1/3 ≈ −0.333. La silueta prefiere {0, 1}{5}. Para tres unitarios, cada s(i) vale 0 por convención, así que la puntuación es 0; a diferencia de la inercia, la silueta no recompensa la partición en unitarios.

---

## 5. Dos lunas

Toma 20 puntos en cada una de dos medias lunas entrelazadas: la luna A en (cos t_i, sin t_i) y la luna B en (1 − cos t_i, 1/2 − sin t_i), con t_i = πi/19 para i = 0, …, 19. Dentro de una luna, dos puntos consecutivos están a 2 sin(π/38) ≈ 0.165 uno del otro, y el par más cercano entre las lunas está a unos 0.503. Los extremos de una luna, en cambio, están a 2 uno del otro.

La transcripción del código de IX (§6) predice lo siguiente. El manejador de k-means de IX, con sus valores por defecto de semilla 42 y un solo arranque, corta las lunas con una recta y pone 11 de los 40 puntos en el clúster de la otra luna, con inercia 16.1871, frente a 25.4358 para las dos lunas mismas. Diez arranques (n_init = 10) encuentran una inercia menor, 16.1554 desde la semilla 43, y aún colocan mal 10 puntos. Un GMM de dos componentes con la semilla 42 coloca mal 6. DBSCAN con minPts = 3 devuelve exactamente las dos lunas, sin ruido, con ε = 0.3, y con cada ε de 0.166 a 0.503 en pasos de 0.001; con 0.165 todos los puntos son ruido, y con 0.504 las lunas se funden en un solo clúster.

La silueta ordena las particiones al revés: 0.2792 para las dos lunas, que es también la puntuación de DBSCAN, frente a 0.4694 para k-means con un arranque, 0.4728 con diez, y 0.4375 para el GMM. La inercia y la silueta coinciden entre sí, y ambas prefieren una partición equivocada. No están mal calculadas: una luna es larga y curva, sus extremos están más lejos que muchos pares de puntos de lunas distintas, y solo por la distancia es un mal clúster. Una puntuación mide el acuerdo con su propia idea de clúster, no con la estructura que produjo los datos.

### Ejercicio práctico

Muestra que ninguna recta separa las dos lunas, de modo que k-means con k = 2 no puede devolverlas, sea cual sea el arranque.

> *Solución:* Como t_(19−i) = π − t_i, los puntos B_i = (1 − cos t_i, 1/2 − sin t_i) y B_(19−i) = (1 + cos t_i, 1/2 − sin t_i) de la luna B tienen como punto medio (1, 1/2 − sin t_i), que está en la envolvente convexa de la luna B. Para i = 0 es (1, 1/2), y para i = 9 es (1, 1/2 − sin(9π/19)) ≈ (1, −0.497). El punto (1, 0) de la luna A, en i = 0, está en el segmento entre ambos, así que en la envolvente convexa de la luna B. Dos clústeres de k-means son los puntos a cada lado de la mediatriz de sus centros, un semiplano cerrado y el semiplano abierto opuesto, ambos convexos. Si la luna B estuviera en uno de ellos, también lo estarían su envolvente convexa y el punto (1, 0), que entonces no podría estar en el otro con el resto de la luna A.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de `KMeans`, `DBSCAN`, `GMM`, `silhouette_score` y sus manejadores MCP a Python, con una réplica del `StdRng` de rand 0.9 (ChaCha12, sembrado mediante PCG32) que reproduce las extracciones del propio crate, `random_range` incluido. IX calcula las distancias con sumas secuenciales, como la transcripción; algunas sumas de ndarray pueden diferir en los últimos bits. Las decisiones discretas detrás de cada predicción enunciada, como una extracción de k-means++, una asignación, una prueba de parada o una prueba sobre ε, tienen márgenes muy por encima de esos bits, salvo tres casi empates entre los diez arranques de k-means del §5, que llevan a la misma inercia en cualquier caso. Estos números son predicciones, y el §7 propone comprobarlas.

**k-means** (`crates/ix-unsupervised`). [`KMeans`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L25) ejecuta [un solo arranque k-means++](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L23) desde [la semilla 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L40), con como mucho [300 iteraciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L38). El primer centro sale de [`random_range`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L95), y un clúster vacío [conserva su centroide](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L159). El manejador MCP [`kmeans`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L303) usa por defecto [100 iteraciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L313), ejecuta `n_init` arranques desde las semillas seed, seed + 1, … y [se queda con la inercia más baja](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L351), como comprueba la prueba [`kmeans_n_init_keeps_the_lowest_inertia_start`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L937). Los centros siguientes salen de la extracción por D² del §1:

```rust
            // Weighted random selection
            let total: f64 = distances.sum();
            let mut r = rng.random::<f64>() * total;
            for i in 0..n {
                r -= distances[i];
                if r <= 0.0 {
                    centroids.row_mut(c).assign(&x.row(i));
                    break;
                }
            }
```

**GMM** (`crates/ix-unsupervised`). [`GMM`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L10) solo tiene [covarianzas diagonales](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L19), inicia cada varianza en la [varianza de los datos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L109) y cada peso en [1/k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L116), y se detiene cuando ℓ cambia menos de [10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L28). Sus medias parten de k filas de los datos:

```rust
        // Initialize with K-Means++ style: pick k random points as means
        use rand::Rng;
        let indices: Vec<usize> = {
            let mut idxs = Vec::with_capacity(self.k);
            for _ in 0..self.k {
                let mut idx = rng.random_range(0..n);
                while idxs.contains(&idx) {
                    idx = rng.random_range(0..n);
                }
                idxs.push(idx);
            }
            idxs
        };
```

**DBSCAN y la silueta.** [`DBSCAN`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L14) etiqueta los clústeres 1, 2, … y [el ruido 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L4), cuenta un punto en su propio entorno, y sigue el §2. Su manejador rechaza [ε ≤ 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L427) y [minPts < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L443). [`silhouette_score`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/eval/silhouette.rs#L26) calcula exactamente la definición de Rousseeuw, con s(i) = 0 para un unitario.

- **La tolerancia de k-means está en unidades de los datos al cuadrado.** La prueba de parada compara el [desplazamiento al cuadrado de los centroides](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L164) con [10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L39), con un `<` estricto. La iteración de Lloyd llega a un punto fijo exacto, donde el desplazamiento es exactamente 0, así que con datos de tamaño ordinario la tolerancia rara vez importa. Con números pequeños sí importa: un desplazamiento de δ cuenta como δ², así que con las lunas del §5 multiplicadas por 10^-6, la transcripción predice una parada tras la primera iteración, con una inercia de 20.1421 en las unidades de las lunas originales en lugar de 16.1871, y una silueta de 0.4248 en lugar de 0.4694. Con un factor 10^-3, la ejecución no cambia.
- **El manejador de k-means no comprueba k.** El esquema pide [k ≥ 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L104), pero `ix-agent` no tiene ningún validador de JSON Schema entre sus dependencias, y el manejador [lee k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L307) sin comprobarlo, a diferencia de `n_init` y a diferencia del manejador de GMM, que rechaza [k < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L662). Con k = 0, `init_centroids` [asigna la fila 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L96) de una matriz de centroides sin filas, y ndarray entra en pánico con ese índice.
- **El `predict` de DBSCAN no hace lo que dice su comentario.** El comentario dice que `predict` asigna un punto nuevo a [«the nearest core point's cluster,»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L112) pero la [condición](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L129) acepta cualquier punto de entrenamiento a distancia como mucho ε cuya etiqueta no sea ruido, puntos frontera incluidos. La [redefinición de `fit_predict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L149) devuelve en su lugar las etiquetas de `fit`, así que el manejador, que [la llama](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L450), no se ve afectado; `predict` sobre datos nuevos sí. Con los datos de la propia prueba de IX [`fit_predict_returns_canonical_fit_labels_not_predict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L290), con ε = 1 y minPts = 4, `fit` etiqueta el punto [(2.2, 0)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L297) como ruido, mientras que `predict` pone un punto nuevo en el mismo lugar en el clúster 1, porque está a distancia como mucho ε del punto frontera (1.3, 0).
- **El arranque del GMM no es k-means++, y filas distintas no son puntos distintos.** El comentario dice [«K-Means++ style»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L89), pero el código anterior extrae de forma uniforme k índices de fila distintos; cuando k > n el bucle no termina nunca, cosa que el manejador impide [rechazando k > n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L665) y la biblioteca no. Dos filas distintas con valores iguales hacen empezar dos componentes con la misma media, la misma varianza y el mismo peso, y por el §3 siguen idénticas. Con las diez valoraciones 1, 2, 2, 3, 3, 3, 4, 4, 5, 5 y k = 2, la transcripción lo predice para 15 de las semillas 0 a 99: dos componentes idénticas con media 3.2 y varianza 1.56, todos los puntos etiquetados 0, tras 2 iteraciones.
- **El suelo de varianza decide la verosimilitud.** El paso M [pone a cada varianza un suelo de 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L171), y unas salvaguardas mantienen finita la aritmética: el paso E [solo normaliza una fila si su suma supera 10^-300](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L138), N_c tiene un [suelo de 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L149), y ℓ pone un suelo de 10^-300 a [la densidad de cada punto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L63). Mientras esas salvaguardas sigan inactivas, el bucle es EM exacto para gaussianas diagonales cuyas varianzas se mantienen en 10^-6 o más, ya que llevar una varianza al suelo es el paso M con restricción, y ℓ no puede disminuir. La degeneración del §3 persiste. Con las diez valoraciones, se predice que 76 de las semillas 0 a 99, la semilla 42 incluida, ponen una componente sobre los dos 5, con varianza exactamente 10^-6, peso 0.19994 para la semilla 42, y ℓ = −4.1192, frente a −16.4128 para las componentes idénticas y −15.86 o −15.85 para los 9 ajustes con dos componentes propias. El ajuste colapsado gana porque su densidad en 5 es de unos 0.2/√(2π · 10^-6) ≈ 79.8; un suelo 100 veces menor añadiría unos ln 10 ≈ 2.30 por cada uno de los dos 5.
- **La prueba de la log-verosimilitud no pone a prueba EM.** [`test_gmm_log_likelihood_increases`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L249) ajusta los mismos datos con [una iteración](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L259) y con [como mucho 50](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L263), y afirma que la segunda log-verosimilitud [no es menor que la primera menos 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L267). La transcripción predice −19.5684 tras una iteración y −7.1398 tras tres, cuando el ajuste se detiene. Un paso M que devolviera su entrada sin cambios daría valores iguales y pasaría: la prueba no comprueba ni que EM mejore nada ni que ℓ nunca disminuya a lo largo de las iteraciones.
- **El manejador de GMM acepta en silencio valores mal formados.** Lee [`seed`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L671) y `max_iter` con una reserva al valor por defecto, así que un valor negativo o no entero se convierte en 42 o 100 sin error, donde el manejador de k-means [lo rechaza](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L322). Un `max_iter` de 0, por debajo del [mínimo de 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L499) del esquema, devuelve los parámetros de partida sin ningún paso de EM.
- **La silueta cuenta el ruido de DBSCAN como un clúster.** El esquema de la silueta sugiere darle las etiquetas de k-means o de DBSCAN: [«wire the `labels` output of kmeans/dbscan»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L325). La puntuación trata la etiqueta 0 como cualquier otra, y también el [recuento de clústeres](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L540) del manejador. Añade cuatro valores atípicos en (−1.5, 1.5), (2.5, 1.5), (−1.5, −1) y (2.5, −1) a las lunas del §5: DBSCAN con ε = 0.3 y minPts = 3 devuelve las dos lunas y etiqueta los atípicos como ruido, y el manejador de la silueta informa entonces de 3 clústeres y una puntuación de 0.2126, frente a 0.2792 una vez apartado el ruido. El `silhouette_score` de scikit-learn tiene la misma convención; el pipeline debe quitar primero el ruido, e informar de cuánto quitó.
- **Otras lagunas.** No hay índice de Davies–Bouldin ni de Calinski–Harabasz, ni BIC ni AIC, ni estimación de densidad por núcleos, ni OPTICS ni HDBSCAN, ni covarianza completa ni reinicios para el GMM, ni índice externo: los diagnósticos de embeddings de IX señalan que [no hay un índice de Rand ajustado nativo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-embedding-diagnostics/src/main.rs#L799). Para k = n, la silueta devuelve 0 donde scikit-learn lanza un error, como su documentación [indica](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/eval/silhouette.rs#L8).

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

En el rectángulo del §1, ¿por qué la extracción por D² da el mal arranque con probabilidad 1/34 sea cual sea la primera esquina, y qué hace el bucle anterior cuando todas las distancias restantes son 0?

> *Solución:* Las dos simetrías especulares del rectángulo y su producto conservan las distancias y llevan cualquier esquina a cualquier otra, así que desde cada primera esquina las otras tres tienen D² = 1, 16 y 17, y solo la esquina a distancia 1 lleva a la división inferior–superior: 1/(1 + 16 + 17) = 1/34. Cuando todas las distancias son 0, por ejemplo cuando k supera el número de puntos distintos, total es 0, así que r = 0, y la primera pasada por el bucle encuentra r ≤ 0 y elige la fila 0, que puede ser ya un centro. La prueba de IX del clúster vacío se apoya en esto: con los valores 10, 10, 14, 14 y k = 3, el tercer centro es la fila 0, en 10, y su clúster queda vacío.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **El rectángulo.** Llama al manejador de k-means sobre el rectángulo del §1 con k = 2 y las semillas 0 a 999. Predicción: 26 ejecuciones terminan en inercia 16, empezando por las semillas 3, 22 y 55, y las demás en 1; el número esperado es 1000/34 ≈ 29.4.
2. **Dos lunas, k-means.** Construye las lunas del §5 y llama al manejador de k-means con k = 2, y luego con n_init = 10. Predicción: inercia 16.1871 con 11 puntos mal colocados, y luego 16.1554 con 10.
3. **Dos lunas, DBSCAN.** Llama al manejador de DBSCAN sobre las lunas con min_points = 3 y ε = 0.165, 0.166, 0.3, 0.503 y 0.504. Predicción: todo ruido con 0.165; las dos lunas y nada de ruido con 0.166, 0.3 y 0.503; un solo clúster con 0.504.
4. **Puntuaciones.** Llama al manejador de la silueta sobre las lunas con las etiquetas verdaderas, las etiquetas del paso 2 con un arranque, y las del manejador de GMM con k = 2. Predicción: 0.2792, 0.4694 y 0.4375.
5. **Ruido.** Añade los cuatro atípicos del §6, llama al manejador de DBSCAN con ε = 0.3 y min_points = 3, y pasa sus etiquetas al manejador de la silueta tal cual, y luego sin las filas de ruido. Predicción: `n_noise` 4 y `n_clusters` 2; luego 3 clústeres y 0.2126, y 2 clústeres y 0.2792.
6. **Mezclas degeneradas.** Llama al manejador de GMM sobre las diez valoraciones del §6 con k = 2 y las semillas 0 a 99. Predicción: 76 ajustes con una varianza de exactamente 10^-6 en la media 5, 15 con dos componentes idénticas de media 3.2 y varianza 1.56, y 9 con dos componentes propias.
7. **El `predict` de DBSCAN.** Ajusta `DBSCAN` con ε = 1 y minPts = 4 sobre los seis puntos de su prueba, y llama a `predict` sobre el punto (2.2, 0). Predicción: `fit` lo etiqueta 0 y `predict` devuelve 1.

### Ejercicio práctico

En el paso 6, ¿por qué los ajustes colapsados tienen la log-verosimilitud más alta, y por qué eso no debería convertirlos en el modelo preferido?

> *Solución:* Una componente sobre los dos 5 tiene densidad π/√(2πσ²) en 5, que crece sin cota al encogerse σ² (§3). IX la detiene en σ² = 10^-6, donde la densidad es de unos 79.8 con π ≈ 0.2, así que cada 5 aporta unos ln 79.8 ≈ 4.38 a ℓ, mientras que una componente propia da a cada punto una contribución negativa. Esa ganancia viene del suelo, no de los datos: un suelo menor daría un ℓ mayor, sin límite. Las valoraciones son discretas, y un modelo de densidad puede darles una verosimilitud no acotada apilando masa sobre valores repetidos. Una comparación por ℓ, o por el BIC, cuya penalización es la misma para todo ajuste de dos componentes, elegiría el ajuste degenerado.

---

## 8. Errores comunes

- **Leer clústeres en la salida de k-means sobre datos curvos o alargados.** Sus clústeres son celdas de Voronoi; compruébalo con un método que admita otras formas, o con datos de estructura conocida.
- **Elegir k solo por la inercia.** Siempre baja al crecer k, hasta 0 en k = n.
- **Fiarse de un solo arranque.** Ejecuta varias semillas, quédate con la inercia más baja, y mira cuánto difieren las particiones.
- **Puntuar la salida de DBSCAN con el ruido como clúster.** Quita las filas de ruido antes de calcular un índice interno, e informa de cuántas había.
- **Comparar mezclas por su log-verosimilitud cuando una varianza puede colapsar.** Comprueba la varianza más pequeña y el peso de su componente, y pon un suelo a las varianzas o regularízalas en las unidades de los datos.
- **Tomar una silueta alta como prueba de estructura.** Recompensa los clústeres redondos y separados; en las lunas prefiere la partición equivocada.
- **Usar una tolerancia absoluta con datos en unidades arbitrarias.** Reescala primero los datos, o usa una regla relativa.
- **Ignorar el orden de las filas en DBSCAN.** Los puntos frontera van al primer clúster que los alcanza; infórmalos por separado cuando importen.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Inercia** | La suma, dentro de los clústeres, de las distancias al cuadrado a las medias de los clústeres, que minimiza k-means |
| **Algoritmo de Lloyd** | Alternar la asignación al centro más cercano y la actualización de las medias hasta que la partición deja de cambiar |
| **k-means++** | Un arranque que extrae cada centro nuevo con probabilidad proporcional al cuadrado de su distancia al centro más cercano ya elegido |
| **Punto núcleo** | Un punto con al menos minPts puntos, él incluido, a distancia como mucho ε |
| **Punto frontera** | Un punto de un clúster de DBSCAN que no es un punto núcleo |
| **Ruido** | Un punto que no pertenece a ningún clúster de DBSCAN |
| **Responsabilidad** | La probabilidad a posteriori de que una componente de la mezcla haya producido un punto |
| **EM** | Alternar responsabilidades y máxima verosimilitud ponderada, lo que nunca disminuye la log-verosimilitud |
| **Componente degenerada** | Una componente de la mezcla cuya varianza tiende a 0 sobre unos pocos puntos, con lo que la verosimilitud crece sin cota |
| **Silueta** | La media sobre los puntos de (b − a)/max(a, b), que compara distancias dentro de los clústeres y entre ellos |
| **Índice interno** | Una puntuación de un agrupamiento calculada solo a partir de los datos |
| **Índice externo** | Una puntuación que compara un agrupamiento con etiquetas conocidas, como el índice de Rand ajustado |

---

## Autoevaluación

**1. Un colega ejecuta k-means con k = 2 sobre dos arcos entrelazados e informa de una silueta de 0.47 como prueba de que hay dos clústeres. ¿Qué le respondes?**
> Que la silueta y la inercia comparten la idea de clúster de k-means, compacto y redondo, así que una puntuación alta dice que la partición encaja con esa idea, no que recupere los arcos. En las lunas del §5, k-means obtiene 0.4694 colocando mal 11 de 40 puntos, y las lunas verdaderas obtienen 0.2792. Pide un método que admita clústeres curvos, como DBSCAN con ε entre la separación y el hueco, y una comparación con una estructura conocida, mediante un índice externo, cuando la haya.

**2. ¿Por qué la log-verosimilitud de EM nunca puede disminuir, y por qué eso no hace bueno el ajuste?**
> Cada paso E construye una cota inferior que toca ℓ en los parámetros actuales, y cada paso M la maximiza, así que ℓ no puede bajar. Pero un ℓ no decreciente puede converger a un punto de silla o a un mal máximo local, y ℓ mismo no tiene máximo cuando una varianza puede encogerse sobre un punto: los ajustes de IX con las diez valoraciones del §6 alcanzan su ℓ más alto colapsando una componente sobre los dos 5.

**3. El manejador de DBSCAN de IX informa de 2 clústeres y 4 puntos de ruido, y el manejador de la silueta, con las mismas etiquetas, informa de 3 clústeres. ¿Por qué?**
> DBSCAN etiqueta el ruido con 0, y la silueta trata la etiqueta 0 como un clúster más, como hace scikit-learn. Los 4 puntos de ruido dispersos forman un tercer «clúster», muy disperso, que baja la puntuación de 0.2792 a 0.2126 en las lunas del §6. Quita primero las filas de ruido, e informa de su número.

**4. ¿Por qué los valores repetidos en los datos amenazan el ajuste de una mezcla gaussiana, y qué hace el suelo de IX al respecto?**
> Una componente puede situarse sobre un valor repetido con un peso positivo mientras su varianza tiende a 0, y su densidad allí, y por tanto ℓ, crece sin cota. El suelo de 10^-6 de IX detiene el colapso en un ℓ finito, pero entonces el suelo, expresado en unidades de los datos al cuadrado, decide cuánto crece ℓ, y el ajuste colapsado sigue teniendo el ℓ más alto.

**Criterio de aprobación:** Enunciar el objetivo de k-means y por qué Lloyd se detiene en un punto fijo que depende del arranque, definir los puntos núcleo, los puntos frontera y el ruido de DBSCAN, deducir EM y su monotonía y decir por qué la verosimilitud no tiene máximo, calcular una silueta a mano, mostrar con las dos lunas que las puntuaciones internas pueden preferir la partición equivocada, y rastrear dónde los comentarios, los manejadores y las pruebas de IX prometen más de lo que el código entrega.

---

## Base de investigación

- T. Caliński y J. Harabasz, «A dendrite method for cluster analysis», *Communications in Statistics* 3, 1974: el índice de Calinski–Harabasz
- A. P. Dempster, N. M. Laird y D. B. Rubin, «Maximum likelihood from incomplete data via the EM algorithm», *Journal of the Royal Statistical Society, Series B* 39, 1977: EM y su monotonía
- G. Schwarz, «Estimating the dimension of a model», *Annals of Statistics* 6, 1978: el BIC
- D. L. Davies y D. W. Bouldin, «A cluster separation measure», *IEEE Transactions on Pattern Analysis and Machine Intelligence* 1, 1979: el índice de Davies–Bouldin
- S. P. Lloyd, «Least squares quantization in PCM», *IEEE Transactions on Information Theory* 28, 1982: el algoritmo de Lloyd
- C. F. J. Wu, «On the convergence properties of the EM algorithm», *Annals of Statistics* 11, 1983: la convergencia de los iterados
- L. Hubert y P. Arabie, «Comparing partitions», *Journal of Classification* 2, 1985: el índice de Rand ajustado
- P. J. Rousseeuw, «Silhouettes: a graphical aid to the interpretation and validation of cluster analysis», *Journal of Computational and Applied Mathematics* 20, 1987: la silueta
- M. Ester, H.-P. Kriegel, J. Sander y X. Xu, «A density-based algorithm for discovering clusters in large spatial databases with noise», *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining*, 1996: DBSCAN
- G. McLachlan y D. Peel, *Finite Mixture Models*, Wiley, 2000: la verosimilitud no acotada y las componentes degeneradas
- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006: k-means como límite de EM
- D. Arthur y S. Vassilvitskii, «k-means++: the advantages of careful seeding», *Proceedings of the ACM-SIAM Symposium on Discrete Algorithms*, 2007: k-means++ y su garantía
- D. Aloise, A. Deshpande, P. Hansen y P. Popat, «NP-hardness of Euclidean sum-of-squares clustering», *Machine Learning* 75, 2009: la NP-dificultad para k = 2
- E. Schubert, J. Sander, M. Ester, H.-P. Kriegel y X. Xu, «DBSCAN revisited, revisited: why and how you should (still) use DBSCAN», *ACM Transactions on Database Systems* 42, 2017: los puntos frontera y la elección de los parámetros
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
