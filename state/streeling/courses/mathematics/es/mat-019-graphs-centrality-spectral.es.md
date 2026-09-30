---
module_id: mat-019-graphs-centrality-spectral
department: mathematics
course: Grafos, centralidad y estructura espectral
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-018-clustering-density-validity]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Grafos, centralidad y estructura espectral — Qué vértice importa y qué cuenta el laplaciano

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Describir un grafo por sus matrices de adyacencia, de grados y laplaciana, y leer en ellas los paseos y las componentes
- Definir PageRank como la distribución estacionaria de un navegante aleatorio, acotar el error de su iteración de potencias, y decir qué pasa con el rango de un vértice sin enlaces salientes
- Calcular las centralidades de grado, de cercanía, de intermediación y de vector propio, y construir un grafo en el que discrepan
- Demostrar que el laplaciano es semidefinido positivo y que la multiplicidad de su valor propio 0 es el número de componentes conexas
- Partir un grafo con el vector de Fiedler, y decir cuándo ese vector no está determinado
- Rastrear lo que garantizan el `Graph` de IX, sus manejadores y `compute_laplacian_spectrum`, y dónde sus comentarios, su catálogo y sus pruebas prometen más de lo que el código entrega

---

## 1. Los grafos como matrices

Un grafo tiene n vértices, numerados de 0 a n − 1, y un conjunto de aristas. En un grafo dirigido, una arista i → j tiene un sentido; en un grafo no dirigido, una arista {i, j} es un par no ordenado. La **matriz de adyacencia** A tiene A_ij = 1 cuando hay una arista de i a j y 0 en otro caso, o un peso w_ij > 0 en un grafo ponderado; para un grafo no dirigido, A es simétrica. El **grado** de un vértice es d_i = Σ_j A_ij, y D = diag(d_1, …, d_n). En un grafo no ponderado, la entrada (Aᵏ)_ij cuenta los paseos de longitud k de i a j, ya que un paseo i → l → j aporta A_il A_lj a (A²)_ij, y así sucesivamente. Dos vértices de un grafo no dirigido están en la misma **componente conexa** cuando un paseo los une; un grafo dirigido es débilmente conexo cuando sus aristas, sin tener en cuenta su sentido, lo conectan.

Para un grafo no dirigido, A es simétrica, así que el teorema espectral del MAT-005 da valores propios reales λ_1 ≥ … ≥ λ_n y una base ortonormal de vectores propios. Como A tiene entradas no negativas, el teorema de Perron–Frobenius añade más (Horn y Johnson 2013, cap. 8): λ_1 ≥ |λ_i| para todo i, y cuando el grafo es conexo, λ_1 es simple y tiene un vector propio de entradas positivas, el **vector de Perron**. La cota |λ_n| ≤ λ_1 puede ser una igualdad: un grafo conexo tiene λ_n = −λ_1 exactamente cuando es **bipartito**, cuando sus vértices se reparten en dos lados con cada arista entre ambos (Brouwer y Haemers 2012). Una estrella, un camino y un ciclo par son bipartitos; un triángulo no lo es. Esto importa para la iteración de potencias (§3), que necesita un valor propio estrictamente mayor en módulo que todos los demás.

### Ejercicio práctico

Muestra que el espectro de un grafo bipartito es simétrico respecto de 0: si λ es un valor propio, también lo es −λ, con la misma multiplicidad.

> *Solución:* Numera primero los vértices de un lado, de modo que A = [[0, B], [Bᵀ, 0]]. Si (u, v) es un vector propio para λ, entonces B v = λ u y Bᵀ u = λ v. Entonces A (u, −v) = (−B v, Bᵀ u) = (−λ u, λ v) = −λ (u, −v), así que −λ es un valor propio. La aplicación (u, v) ↦ (u, −v) es invertible y lleva el subespacio propio de λ al de −λ, así que las multiplicidades son iguales. Para la estrella de centro 0 y hojas 1, 2 y 3, los valores propios son √3, 0, 0 y −√3.

---

## 2. PageRank

PageRank (Brin y Page 1998; Page, Brin, Motwani y Winograd 1999) ordena los vértices de un grafo dirigido según el comportamiento a largo plazo de un navegante aleatorio. Desde el vértice i, con probabilidad α, el **factor de amortiguamiento**, el navegante sigue uno de los enlaces salientes de i, cada uno con probabilidad 1/out(i); con probabilidad 1 − α, salta a un vértice elegido uniformemente. Un vértice sin enlaces salientes, un **nodo colgante**, necesita una regla propia, y la habitual envía al navegante desde él a un vértice uniforme. Llamemos P a la matriz de los enlaces salientes, con P_ij = 1/out(i) para una arista i → j, cuyas filas de los nodos colgantes son nulas; S a P con esas filas sustituidas por u = (1/n, …, 1/n); y 𝟙 a la columna de unos. La **matriz de Google** es M = α S + (1 − α) 𝟙u, y el vector PageRank es su distribución estacionaria: el vector fila π ≥ 0 con Σ_i π_i = 1 y π M = π.

Para 0 ≤ α < 1 todas las entradas de M son positivas, así que por Perron–Frobenius π existe, es única y es positiva. La iteración de potencias la encuentra, y su error se acota con facilidad. Para dos vectores de probabilidad x e y, x M − y M = α (x − y) S, porque (x − y) 𝟙 = 0; S tiene entradas no negativas y filas que suman 1, así que ‖(x − y) S‖₁ ≤ ‖x − y‖₁, y ‖x M − y M‖₁ ≤ α ‖x − y‖₁. Tras k pasos desde cualquier arranque, el error en la norma ℓ1 es como mucho 2αᵏ. Con el habitual α = 0.85, 100 pasos dejan como mucho 2 · 0.85^100 ≈ 1.7 × 10^-7; con α = 0.99 la misma cota es 2 · 0.99^100 ≈ 0.73, y puede alcanzarse casi (§6). El segundo valor propio de M es como mucho α en módulo (Haveliwala y Kamvar 2003): α fija la velocidad.

Otro tratamiento de los nodos colgantes descarta su rango: itera x ← α x P + (1 − α) u. El mismo argumento, con P en lugar de S, muestra que converge, a x* = (1 − α) u (I − α P)^-1, cuyas entradas suman menos de 1 en cuanto un nodo colgante tiene rango positivo. Toma dos artículos, 0 y 1, que citan a un tercero, 2, que no cita nada, con α = 0.85. Tras dos pasos, los rangos de 0 y 1 valen 0.15/3 = 0.05, el de 2 vale 0.05 + 0.85 · (0.05 + 0.05) = 0.135, y después nada cambia: los tres suman 0.235. Dividido por esa suma, x* se convierte en (10/47, 10/47, 27/47) ≈ (0.2128, 0.2128, 0.5745), que es exactamente π con saltos uniformes desde el nodo colgante (ejercicio abajo; Langville y Meyer 2006).

En un grafo no dirigido con m aristas y sin vértices aislados, donde cada arista cuenta en ambos sentidos, el paseo sin saltos, α = 1, tiene la matriz de transición D^-1 A, y π_i = d_i/(2m) es estacionaria: Σ_i (d_i/(2m)) (A_ij/d_i) = d_j/(2m). En un grafo no dirigido, el navegante aleatorio tiende hacia los vértices de grado alto.

### Ejercicio práctico

Muestra que, cuando se descarta el rango de los nodos colgantes, el punto fijo x*, dividido por la suma de sus entradas, es el PageRank π con saltos uniformes desde los nodos colgantes.

> *Solución:* Sea a la columna que vale 1 en los nodos colgantes y 0 en el resto, de modo que S = P + a u. Como π 𝟙 = 1, π M = α π P + α (π a) u + (1 − α) u, así que π = α π P + γ u con γ = α (π a) + 1 − α > 0. La matriz I − α P es invertible, porque α P tiene entradas no negativas y filas que suman como mucho α < 1, así que π = γ u (I − α P)^-1 = (γ/(1 − α)) x*. Por tanto π es un múltiplo positivo de x*, y como las entradas de π suman 1, π = x*/Σ_i x*_i. En el grafo de citas, γ = 0.85 · 27/47 + 0.15 = 30/47, y γ/(1 − α) = 200/47 = 1/0.235.

---

## 3. La familia de las centralidades

Las medidas de centralidad responden a preguntas distintas sobre un vértice i de un grafo no dirigido conexo con n vértices:
- La **centralidad de grado**, d_i/(n − 1): cuántos vecinos, como fracción de los posibles.
- La **centralidad de cercanía**, (n − 1)/Σ_j dist(i, j), con distancias contadas en aristas: cuán cerca está i de todos los demás. En un grafo no conexo esa suma es infinita; la forma r²/((n − 1) Σ_j dist(i, j)), con r el número de vértices alcanzables desde i y la suma sobre ellos, se reduce a la primera cuando todos los vértices son alcanzables (Wasserman y Faust 1994).
- La **centralidad de intermediación**, Σ σ_st(i)/σ_st sobre los pares no ordenados {s, t} de otros vértices, donde σ_st cuenta los caminos más cortos entre s y t y σ_st(i) los que pasan por i (Freeman 1977): con qué frecuencia i está en el camino. Dividir por (n − 1)(n − 2)/2, el número de pares, la lleva a [0, 1]. Brandes (2001) la calcula para todos los vértices en tiempo O(nm) para m aristas, con una búsqueda en anchura desde cada vértice.
- La **centralidad de vector propio** (Bonacich 1972): el vector de Perron de A, de modo que cada vértice puntúa en proporción a la suma de las puntuaciones de sus vecinos, x_i = (1/λ_1) Σ_j A_ij x_j.

La cometa de Krackhardt (Krackhardt 1990) es el grafo clásico en el que discrepan. Sus diez vértices, Andre, Beverly, Carol, Diane, Ed, Fernando, Garth, Heather, Ike y Jane, se numeran de 0 a 9, con las aristas 0–1, 0–2, 0–3, 0–5, 1–3, 1–4, 1–6, 2–3, 2–5, 3–4, 3–5, 3–6, 4–6, 5–6, 5–7, 6–7, 7–8 y 8–9. Diane tiene el grado más alto, 6 de 9, y la mayor centralidad de vector propio. Fernando y Garth son los más cercanos, con 9/14 ≈ 0.643 frente a 3/5 de Diane. Heather, el único enlace entre la parte densa y la cola Ike–Jane, tiene la mayor intermediación, 14 de los 36 pares de otros vértices, frente a 25/3 de Fernando y Garth y 11/3 de Diane. Ninguna de las cuatro respuestas es incorrecta: cada una mide otra cosa, y «el vértice más central» no significa nada hasta que se dice qué medida.

La centralidad de vector propio suele calcularse por iteración de potencias (MAT-005 §6), que falla en los grafos bipartitos: por el §1, su espectro contiene −λ_1 además de λ_1, los dos términos de mayor módulo nunca se separan, y el iterado oscila. En la estrella de centro 0 y hojas 1, 2 y 3, desde x = (1, 1, 1, 1), A x = (3, 1, 1, 1) y A² x = (3, 3, 3, 3): tras cada número par de pasos el iterado normalizado es uniforme, y el centro parece una hoja. El remedio habitual itera con A + I, cuyos valores propios son λ_i + 1, con los mismos vectores propios. Como λ_n ≥ −λ_1, |λ_n + 1| < λ_1 + 1 siempre que λ_1 > 0, así que el vector de Perron domina ahora estrictamente. Los valores propios desplazados no tienen por qué ser positivos: en la estrella son 1 + √3, 1, 1 y 1 − √3 ≈ −0.732. En un grafo no conexo, la iteración desde un arranque positivo converge a un vector soportado en las componentes cuyo λ_1 es el mayor, y todo otro vértice puntúa 0 en el límite.

### Ejercicio práctico

Calcula la intermediación del centro de una estrella con k hojas, y del vértice central del camino 0–1–2, antes y después de dividir por el número de pares.

> *Solución:* En una estrella, cada par de hojas tiene exactamente un camino más corto, por el centro, así que la intermediación del centro es k(k − 1)/2, el número de pares de hojas, y cada hoja puntúa 0. Con n = k + 1 vértices hay (n − 1)(n − 2)/2 = k(k − 1)/2 pares de otros vértices, así que el valor normalizado es 1. Para el camino 0–1–2, el único par que no contiene a 1 es {0, 2}, cuyo único camino más corto pasa por 1: intermediación 1, normalizada 1. Sin normalizar, el centro de una estrella puntúa 3 con tres hojas y 10 con cinco, aunque ambos están en todos los caminos más cortos en que podrían estar.

---

## 4. El laplaciano

El **laplaciano** de un grafo no dirigido con pesos w_ij ≥ 0 es L = D − A, donde d_i = Σ_j w_ij. Su forma cuadrática es

xᵀ L x = Σ sobre las aristas {i, j} de w_ij (x_i − x_j)²,

así que L es semidefinido positivo (ejercicio), y L 𝟙 = 0 porque cada fila suma 0. Sus valores propios, en orden creciente, son 0 = μ_1 ≤ μ_2 ≤ … ≤ μ_n.

**El valor propio cero cuenta las componentes.** Para una matriz semidefinida positiva, xᵀ L x = 0 se cumple exactamente cuando L x = 0. Con pesos positivos, xᵀ L x = 0 significa x_i = x_j a lo largo de cada arista, es decir, x constante en cada componente conexa. Así que el núcleo de L está generado por los vectores indicadores de las componentes, y la multiplicidad del valor propio 0 es el número c de componentes. En particular μ_2 > 0 exactamente cuando el grafo es conexo; Fiedler (1973) llamó a μ_2 la **conectividad algebraica**.

**El vector de Fiedler.** Por el cociente de Rayleigh del MAT-005, tomado sobre los vectores ortogonales a 𝟙, el vector propio de μ_1,

μ_2 = mín sobre los x ≠ 0 con Σ_i x_i = 0 de Σ sobre las aristas de (x_i − x_j)² / Σ_i x_i²,

para un grafo no ponderado, y un minimizador es un **vector de Fiedler**. Poner x_i = 1 en una mitad de los vértices y −1 en la otra, cuando n es par, convierte el numerador en 4 veces el número de aristas cortadas y el denominador en n, así que μ_2 ≤ 4 · corte/n para toda partición en dos mitades. El vector de Fiedler es la mejor relajación con valores reales de ese corte equilibrado, y partir los vértices según su signo es la más sencilla de las particiones espectrales. Fiedler (1975) demostró que, en un grafo conexo, los vértices donde el vector es ≥ 0 inducen un subgrafo conexo, y también los vértices donde es ≤ 0. El vector solo está determinado, salvo signo y escala, cuando μ_2 es simple. En un grafo no conexo, μ_2 = 0 se repite; en el grafo completo K_n, cuyos valores propios del laplaciano son 0 y n, repetido n − 1 veces, todo vector ortogonal a 𝟙 es un vector de Fiedler (MAT-005 §5).

Algunos espectros que conviene recordar: el camino con n vértices tiene los valores propios 2 − 2 cos(πk/n) para k = 0, …, n − 1, así que μ_2 = 4 sin²(π/(2n)) ≈ π²/n²; la estrella con n vértices tiene 0, 1 repetido n − 2 veces, y n. Chung (1997) y el agrupamiento espectral (Shi y Malik 2000; Ng, Jordan y Weiss 2002; von Luxburg 2007) usan los **laplacianos normalizados** L_sym = I − D^(-1/2) A D^(-1/2) y L_rw = I − D^-1 A, donde D^-1 A es el paseo del §2. La desigualdad de Cheeger liga el segundo valor propio de L_sym con la conductancia h del mejor corte: h²/2 ≤ μ_2(L_sym) ≤ 2h. El agrupamiento espectral sumerge cada vértice mediante sus entradas en los k primeros vectores propios de un laplaciano así, y ejecuta el k-means del MAT-018 sobre esa inmersión.

### Ejercicio práctico

Demuestra que xᵀ L x = Σ sobre las aristas {i, j} de w_ij (x_i − x_j)², y deduce que L es semidefinido positivo.

> *Solución:* xᵀ L x = Σ_i d_i x_i² − Σ_(i,j) w_ij x_i x_j, donde la segunda suma recorre los pares ordenados, así que cada arista {i, j} aparece en ella dos veces y aporta −2 w_ij x_i x_j. El grado d_i = Σ_j w_ij reparte el peso de cada arista entre sus dos extremos, así que la primera suma aporta w_ij (x_i² + x_j²) por cada arista. Juntas, cada arista da w_ij (x_i² − 2 x_i x_j + x_j²) = w_ij (x_i − x_j)². Una suma de términos no negativos es no negativa, así que xᵀ L x ≥ 0 para todo x, y cada valor propio de L, el cociente de Rayleigh de su vector propio, es ≥ 0.

---

## 5. La haltera

Une dos grafos completos K_5, sobre los vértices 0–4 y 5–9, con la única arista 4–5. Aquí las centralidades coinciden. Los dos extremos del puente tienen grado 5 frente a 4, e intermediación 20 cada uno, ya que cada uno de los 4 × 5 pares formados por otro vértice de su propia clique y un vértice de la otra clique pasa por ellos. Su cercanía es 9/13 ≈ 0.692 frente a 1/2, su centralidad de vector propio es la mayor, y la distribución estacionaria del paseo sin saltos da a cada uno 5/42, frente a 4/42 (§2).

El laplaciano tiene los valores propios 0, (7 − √41)/2 ≈ 0.2984, luego 5 repetido siete veces, y (7 + √41)/2 ≈ 6.7016 (ejercicio). Un vector de Fiedler toma un valor a en los cuatro vértices interiores de la primera clique, (1 − μ_2) a ≈ 0.7016 a en el extremo del puente, y los valores opuestos en la segunda clique, así que su signo parte la haltera en sus dos pesas, cortando una arista. La conectividad algebraica es pequeña, 0.2984 frente a 5 dentro de cada clique sola: una arista mantiene unidas las dos mitades, y μ_2 lo dice. Quita el puente, y 0 pasa a ser un valor propio doble. Los vectores iguales a 1 en una clique y a 0 en la otra generan el núcleo, toda combinación de ellos es un vector de Fiedler, y la regla del signo ya no significa nada.

### Ejercicio práctico

Deduce los valores propios (7 ± √41)/2 del laplaciano de la haltera a partir del vector que vale a en los cuatro vértices interiores de la primera clique, b en el vértice 4, −b en el vértice 5 y −a en los cuatro vértices interiores de la segunda clique.

> *Solución:* En un vértice interior de la primera clique, de grado 4, (L x)_i = 4a − 3a − b = a − b; en el vértice 4, de grado 5, (L x)_4 = 5b − 4a − (−b) = 6b − 4a. En la segunda clique las ecuaciones son las mismas con los signos opuestos. Así que x es un vector propio para μ cuando a − b = μ a y 6b − 4a = μ b. La primera da b = (1 − μ) a, y la segunda entonces 6(1 − μ) − 4 = μ(1 − μ), es decir μ² − 7μ + 2 = 0, cuyas raíces son (7 ± √41)/2 ≈ 0.2984 y 6.7016. El valor propio 5 tiene los vectores que se anulan fuera de los vértices interiores de una clique y suman 0 en ellos, tres por cada clique, y el vector igual a a en los ocho vértices interiores y a −4a en los dos extremos del puente; con 𝟙 para el valor propio 0, eso da los diez.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea a Python del `Graph` de `crates/ix-graph`, de `compute_laplacian_spectrum` con el resolvedor de Jacobi al que llama (MAT-005 §4), y de los manejadores de abajo. `Graph` guarda sus listas de adyacencia en un `HashMap` y sus conjuntos de vecinos en `HashSet`, que Rust recorre en un orden sorteado en cada proceso; ese orden solo cambia el orden de algunas sumas en coma flotante, lo que puede mover los últimos bits de una puntuación pero ninguno de los decimales que aquí se dan. Estos números son predicciones, y el §7 propone comprobarlas.

**El grafo y sus manejadores.** [`Graph`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L8) guarda, para cada vértice, una lista de pares (vecino, peso), y [`add_undirected_edge`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L37) añade los dos sentidos. La herramienta MCP `ix_graph` llama a [`graph_ops`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2815), que construye un grafo con `n_nodes` vértices, rechaza una arista con un extremo fuera de rango, trata las aristas como [dirigidas salvo que se indique lo contrario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2832), toma un peso ausente como [1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2860), y ofrece el algoritmo de Dijkstra, caminos más cortos, PageRank, búsqueda en anchura y en profundidad y una ordenación topológica, con un [amortiguamiento de 0.85](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2889) y [100 iteraciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2890) por defecto para PageRank. Las cuatro centralidades del §3 están disponibles en SQL mediante una función de tabla de `crates/ix-duck`, que calcula, por ejemplo, [la centralidad de vector propio con 100 iteraciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L482), y cuyo analizador de aristas [rechaza los pesos negativos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L141); la intermediación también está detrás de `ix_mesh_correlate`. El bucle interior de [`pagerank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L185) es:

```rust
            for (&node, edges) in &self.adjacency {
                let out = out_degree[&node] as f64;
                if out > 0.0 {
                    let share = damping * rank[&node] / out;
                    for &(neighbor, _) in edges {
                        *new_rank.get_mut(&neighbor).unwrap() += share;
                    }
                }
            }
```

**El laplaciano.** [`compute_laplacian_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L420) construye L a partir de una lista de aristas no ponderadas, llama al [resolvedor de Jacobi completo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L449) del MAT-005, [recorta en 0 los valores propios negativos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L454), devuelve los tres más pequeños con μ_2, μ_2 − μ_1 y un [vector de Fiedler](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L477), y cuenta las componentes así:

```rust
    let zero_tol = 1e-6;
    let n_components = eigenvalues_all
        .iter()
        .filter(|&&e| e < zero_tol)
        .count()
        .max(1);
```

- **PageRank descarta el rango de los nodos colgantes.** En el bucle de arriba, un vértice con `out` = 0 no transmite nada: es la iteración del §2 que descarta su rango, con n [el número de vértices del mapa](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L186). En el grafo de citas del §2, `ix_graph` devuelve 0.05, 0.05 y 0.135, que suman 0.235. La función de DuckDB `ix_pagerank` divide por la suma, como dice su comentario, [«so dangling-node mass leakage doesn't break the probability-distribution contract»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L161). Por el ejercicio del §2, esto es más que cosmético: una vez convergida, devuelve exactamente PageRank con saltos uniformes desde los nodos colgantes, aquí 10/47, 10/47 y 27/47. La herramienta MCP devuelve el vector bruto. La propia prueba de humo de IX [pasa el grafo de dependencias](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/cargo_deps_smoke.rs#L183) de `ix_cargo_deps` a `ix_graph`, con una arista de cada crate a cada crate de IX de la que depende, de modo que todo crate sin dependencia de IX es un nodo colgante; la prueba solo [cuenta las entradas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/cargo_deps_smoke.rs#L200).
- **PageRank ignora los pesos.** El bucle lee cada arista como [`(neighbor, _)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L207): cada enlace saliente recibe la misma parte, sea cual sea su peso, así que una lista de aristas ponderadas da los mismos rangos que la lista sin pesos. El recorrido guiado de IX sobre la malla ejecutable [se encontró con esto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/walkthroughs/executable-pipeline-mesh.md#L57): un PageRank sobre las distancias por pares de un grafo completo salió uniforme, y el recorrido lo explica como una propiedad de los grafos completos. La uniformidad viene de este código, para el que un grafo completo es regular sean cuales sean sus pesos; un paseo ponderado, con probabilidades w_ij/Σ_k w_ik, tiende hacia los vértices de mayor peso total, como por el §2 tiende hacia el grado alto.
- **El número de iteraciones es fijo.** `pagerank` hace exactamente `iterations` pasadas y no comprueba nada. Por el §2, el error es como mucho 2αᵏ: despreciable para α = 0.85 y 100 pasadas, no para α = 0.99. En la estrella con tres hojas, con cada arista en ambos sentidos, α = 0.99 y 100 pasadas, la transcripción predice 0.4077 para el centro y 0.1974 para cada hoja, frente a los valores exactos 0.4987 y 0.1671, un error de 0.1821 en la norma ℓ1. La estrella es bipartita, así que el error cambia de signo en cada pasada y solo se reduce por el factor 0.99. El catálogo que `ix_explain_algorithm` envía al cliente da como hiperparámetros de PageRank [«damping» y «tol»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5861); no hay ninguna tolerancia.
- **El manejador no comprueba ni α ni el número de iteraciones.** Lee ambos con un valor por defecto de respaldo, así que un amortiguamiento no numérico se convierte en 0.85, y acepta cualquier número, mientras que `ix_pagerank` rechaza [α fuera de [0, 1]](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L165) y [menos de 1 iteración](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L169). Con α = 1.5 en el grafo de citas, `ix_graph` devuelve −1/6, −1/6 y −2/3; con 0 iteraciones devuelve el arranque uniforme.
- **El comentario del vector propio da una razón equivocada para un método correcto.** [`eigenvector_centrality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L333) itera con A + I, como en el §3, y su comentario dice que A + I [«has strictly positive eigenvalues»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L330). En la estrella de la propia prueba de IX uno de ellos es 1 − √3 ≈ −0.732. El método converge de todos modos, por la razón dada en el §3: desde el arranque uniforme, el error del cociente centro sobre hoja se reduce por el factor (√3 − 1)/(√3 + 1) = 2 − √3 ≈ 0.268 por pasada, y la transcripción predice √3 ≈ 1.7321 con precisión doble tras 30 de las 100 pasadas. La prueba exige [un cociente mayor que 1.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L498), que la iteración sin desplazar, uniforme tras 100 pasadas, no cumple. En el triángulo 0–1–2 con la arista separada 3–4, las puntuaciones de 3 y 4 se reducen por el factor 2/3 por pasada, y la transcripción predice unos 1.4 × 10^-18 tras 100 pasadas.
- **La intermediación es un recuento, no una fracción.** El comentario de [`betweenness_centrality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L363) habla de [«the fraction of shortest paths through each node»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L361), pero el código suma las fracciones sobre todos los pares y [divide el total entre dos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L400), por los pares vistos desde sus dos extremos, sin dividir por el número de pares: 3 para el centro de la estrella de la prueba, 10 con cinco hojas, 20 para los extremos del puente de la haltera. Las puntuaciones de grafos de tamaños distintos no se pueden comparar. La prueba de la estrella solo exige que la puntuación del centro sea [positiva](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L508).
- **`ix_mesh_correlate` nombra un centro cuando no lo hay.** [`mesh_correlate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1214) une las series cuya correlación de Pearson alcanza el umbral en valor absoluto, calcula su [intermediación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1239), y devuelve como `hub` el vértice elegido por [`max_by`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1244), que devuelve el último de varios máximos iguales. Cuando ningún par alcanza el umbral, o cuando todos lo alcanzan, todas las puntuaciones valen 0 y `hub` es la última serie: para las tres series (1, −1, 1, −1), (1, 1, −1, −1) y (1, −1, −1, 1), incorreladas dos a dos, la transcripción predice `hub` = 2. En un camino 0–1–2–3, donde 1 y 2 empatan, también devuelve 2.
- **Dijkstra acepta pesos negativos.** [`dijkstra`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L92) es la variante perezosa: [salta una entrada obsoleta del montículo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L108) y vuelve a expandir un vértice cada vez que su distancia baja. Con pesos negativos y sin ciclo negativo, sigue devolviendo las distancias correctas, quizá tras un número exponencial de pasos (Johnson 1973). El catálogo de IX recomienda Dijkstra para [«non-negative weights»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5853), pero el manejador toma cualquier número como peso. El analizador de DuckDB rechaza los pesos negativos, y su comentario dice que un peso negativo [«gives wrong paths and a negative cycle never settles»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L140): la segunda mitad es cierta, pero esta variante perezosa sigue dando los caminos correctos, en el peor caso despacio, y el PageRank que nombra el mismo comentario ignora los pesos. Con `directed` a false, una sola arista negativa es un ciclo negativo de dos aristas, y el bucle baja las dos distancias por turnos: en la única arista 0–1 de peso −1, la transcripción llega a −12 y −11 tras doce pasos, y el bucle solo se detendría cerca de −2^53, donde restar 1 ya no cambia un double, tras unos 9 × 10^15 pasos. Esto se predice a partir del código, no se ha ejecutado; el §7 lo ejecuta con un tiempo límite.
- **El manejador comprueba las aristas pero no el origen.** Un extremo de arista fuera del grafo es un error, pero [`source`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2870) no se comprueba: desde el origen 7 en un grafo con tres vértices, Dijkstra devuelve la distancia 0 para un vértice 7 que no existe e ∞ para los otros tres, que la salida JSON escribe como `null`, igual que para todo vértice inalcanzable.
- **Los comentarios del laplaciano describen otro algoritmo.** Anuncian una iteración [«inverse power»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L400), y después una iteración de potencias sobre una matriz desplazada [con deflación de Gram–Schmidt](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L417), mientras que el código ejecuta el método de Jacobi completo, con O(n³) operaciones por barrido. Los lazos y las aristas fuera de rango se [omiten sin aviso](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L436). Como los valores propios se recortan en 0, `spectral_gap`, μ_2 − μ_1, es μ_2 salvo redondeo y repite `algebraic_connectivity`. Nada fuera de `physics.rs` llama a la función, y ninguna herramienta MCP la expone.
- **Las componentes se cuentan con un umbral absoluto.** Un valor propio cuenta como cero por debajo de [10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L462). Un grafo conexo de diámetro D tiene μ_2 ≥ 4/(n · D) (Mohar 1991), y n · D ≤ n(n − 1) < 4 × 10^6 cuando n ≤ 2000, así que ningún grafo conexo con como mucho 2000 vértices baja tanto. Los mayores pueden: el camino con n vértices tiene μ_2 = 4 sin²(π/(2n)), por debajo de 10^-6 desde n = 3142, donde vale 0.99974 × 10^-6, así que la función contaría un camino conexo de 3142 vértices como 2 componentes. Una búsqueda en anchura, como en [`connected_components`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L224), las cuenta exactamente.
- **El vector de Fiedler se devuelve incluso cuando no está determinado.** Cuando μ_2 se repite, el vector devuelto es un vector del subespacio propio, elegido por las rotaciones. En K_4 la transcripción predice (−0.2887, −0.2887, −0.2887, 0.866), es decir (−1, −1, −1, 3)/√12. En la haltera sin su puente predice 1/√5 ≈ 0.4472 en la primera clique y 0 en la segunda: un vector del núcleo, que separa las cliques por entradas nulas y no nulas, no por el signo. Nada señala ninguno de los dos casos.
- **Algunas pruebas pasarían con un código incorrecto.** [`test_pagerank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L574) usa un 3-ciclo dirigido, en el que el vector uniforme es un punto fijo para todo α, y exige rangos iguales [con margen 0.01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L585): la transcripción devuelve exactamente 1/3 para α = 0.85, 0 y 1, y tras 0 iteraciones. Un PageRank que ignorara α, descartara los saltos o nunca iterara pasaría. [`test_laplacian_disconnected`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L617) exige [al menos 2 componentes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L621) para las aristas 0–1 y 2–3, cuyos valores propios son 0, 0, 2 y 2: un umbral de 3 daría 4 componentes y seguiría pasando. [`test_laplacian_connected`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L606) exige μ_2 [mayor que 0.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L610) en K_4, donde vale 4.
- **Otras lagunas.** No hay laplaciano normalizado, ni agrupamiento espectral, ni constante de Cheeger, ni PageRank ponderado o personalizado, ni prueba de convergencia en PageRank o en la centralidad de vector propio, ni intermediación normalizada, ni caminos más cortos con pesos negativos, ni operación MCP para las centralidades, las componentes o el laplaciano.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Muestra que en el punto fijo del PageRank de IX la suma s de los rangos cumple s = (1 − α) + α (s − x_D), donde x_D es el rango total de los nodos colgantes, y compruébalo en el grafo de citas.

> *Solución:* Cada pasada fija cada vértice en (1 − α)/n más las partes que recibe. Sumados sobre los n vértices, los primeros términos dan 1 − α, y las partes dan α veces el rango de los vértices con enlaces salientes, ya que un vértice así transmite α veces todo su rango, mientras que un nodo colgante no transmite nada: α (s − x_D). En el punto fijo, s = (1 − α) + α (s − x_D), así que s = 1 − α x_D/(1 − α): con α = 0.85, a la suma le faltan para llegar a 1 unas 17/3 ≈ 5.67 veces el rango de los nodos colgantes. En el grafo de citas x_D = 0.135, y s = 1 − (17/3) · 0.135 = 1 − 0.765 = 0.235.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **La fuga.** Llama a `graph_ops` con la operación `pagerank` en el grafo de citas del §2, y después a `ix_pagerank` en una conexión de DuckDB dentro del mismo proceso sobre las mismas aristas. Predicción: 0.05, 0.05 y 0.135, que suman 0.235; después 10/47, 10/47 y 27/47, unos 0.2128, 0.2128 y 0.5745.
2. **La convergencia lenta.** Llama a `graph_ops` con `pagerank` en la estrella con tres hojas, `directed` a false, amortiguamiento 0.99, y 100 y luego 2000 iteraciones. Predicción: 0.4077 para el centro, y luego 0.4987.
3. **La cometa.** Construye la cometa de Krackhardt y llama a las cuatro centralidades y a `pagerank`. Predicción: centralidades de grado y de vector propio máximas en Diane (3), cercanía máxima en Fernando y Garth (5 y 6), con 9/14, intermediación máxima en Heather (7), con 14, y PageRank máximo en Diane, con 0.1471.
4. **El desplazamiento.** Llama a `eigenvector_centrality` en la estrella con 30 y con 100 iteraciones, y después en el triángulo con la arista separada del §6. Predicción: un cociente centro sobre hoja de √3 ≈ 1.7321 las dos veces, y después puntuaciones de unos 1.4 × 10^-18 en la arista.
5. **Espectros.** Llama a `compute_laplacian_spectrum` en la haltera del §5, en la haltera sin su puente, en el triángulo 0–1–2 con la arista 3–4 y el vértice aislado 5, y en K_4. Predicción: 1 componente, μ_2 = 0.2984 y un vector de Fiedler de unos ±0.3336 en los vértices interiores y ±0.2341 en los extremos del puente, con un signo por pesa; 2 componentes y el vector del §6; 3 componentes; 1 componente, μ_2 = 4 y el vector del §6.
6. **El centro de la malla.** Llama a `mesh_correlate` sobre las tres series incorreladas del §6 con el umbral por defecto de 0.5. Predicción: ninguna arista, todas las intermediaciones a 0, y `hub` = 2.
7. **Pesos negativos.** Llama a `graph_ops` con `dijkstra` desde el vértice 0 sobre las aristas 0 → 1 de peso 2, 0 → 2 de peso 5 y 2 → 1 de peso −4, y después, en un proceso hijo con un tiempo límite de 10 segundos, sobre la única arista 0–1 de peso −1 con `directed` a false. Predicción: las distancias 0, 1 y 5; después salta el tiempo límite.

### Ejercicio práctico

¿Por qué el paso 1 no depende del número de iteraciones, siempre que haya al menos 2, mientras que el paso 2 necesita miles?

> *Solución:* El grafo de citas no tiene ciclos. Tras una pasada, los rangos de 0 y 1 valen 0.05 para siempre, ya que nada enlaza con ellos, y tras la segunda, el rango de 2 solo depende de los suyos: cada pasada posterior repite los mismos valores. La estrella es bipartita, así que el error cambia de signo en cada pasada y su tamaño se reduce por el factor α = 0.99 por pasada. Tras 100 pasadas queda 0.99^100 ≈ 0.366 del error inicial, y tras 2000, unos 2 × 10^-9.

---

## 8. Errores comunes

- **Leer un vector PageRank bruto como una distribución.** Con nodos colgantes suma menos de 1; divide por la suma, lo que da PageRank con saltos uniformes desde ellos, e informa de cuánto rango tenían.
- **Esperar que los pesos cambien el PageRank de IX.** No lo cambian; construye tú las probabilidades de transición ponderadas, o di que la ordenación no es ponderada.
- **Nombrar el vértice más central sin nombrar la medida.** Las centralidades de grado, de cercanía, de intermediación y de vector propio responden a preguntas distintas, y en la cometa eligen tres vértices distintos.
- **Comparar intermediaciones brutas entre grafos.** Divide primero por el número de pares, (n − 1)(n − 2)/2 para un grafo no dirigido.
- **Ejecutar la iteración de potencias con A en un grafo bipartito.** Desplaza por la identidad, o detecta una oscilación de periodo 2, antes de fiarte del resultado.
- **Fiarse de un número fijo de iteraciones con α cerca de 1.** La cota del error es 2αᵏ; con α = 0.99, 100 pasadas distan mucho de bastar.
- **Contar las componentes a partir de los valores propios.** Un umbral absoluto confunde grafos grandes débilmente conexos con grafos no conexos; una búsqueda en anchura las cuenta exactamente.
- **Leer un vector de Fiedler cuando μ_2 es 0 o se repite.** Es entonces un vector de un subespacio propio, y sus signos no significan nada; comprueba antes la multiplicidad.
- **Pasar una lista de aristas no dirigidas a `ix_graph` sin poner `directed` a false.** El manejador trata entonces cada arista como de sentido único.
- **Dar pesos negativos al algoritmo de Dijkstra.** Usa Bellman–Ford en su lugar; una arista negativa no dirigida ya es un ciclo negativo.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Matriz de adyacencia** | La matriz A con A_ij = 1, o un peso, para una arista de i a j, y 0 en otro caso |
| **Grado** | El número de vecinos de un vértice, o la suma de los pesos de sus aristas |
| **Vector de Perron** | El vector propio de entradas positivas del mayor valor propio de la matriz de adyacencia de un grafo conexo |
| **Grafo bipartito** | Un grafo cuyos vértices se reparten en dos lados con cada arista entre ambos; su espectro es simétrico respecto de 0 |
| **Factor de amortiguamiento** | La probabilidad α de que el navegante aleatorio siga un enlace en lugar de saltar |
| **Nodo colgante** | Un vértice sin enlaces salientes |
| **PageRank** | La distribución estacionaria de la matriz de Google |
| **Centralidad de intermediación** | La suma, sobre los pares de otros vértices, de la fracción de sus caminos más cortos que pasan por un vértice |
| **Centralidad de vector propio** | La entrada de un vértice en el vector de Perron |
| **Laplaciano** | L = D − A, cuya forma cuadrática suma (x_i − x_j)² sobre las aristas |
| **Conectividad algebraica** | El segundo valor propio más pequeño μ_2 del laplaciano, positivo exactamente cuando el grafo es conexo |
| **Vector de Fiedler** | Un vector propio de μ_2, cuyos signos dan una partición espectral del grafo |

---

## Autoevaluación

**1. Un colega ordena los crates de un espacio de trabajo con el PageRank de `ix_graph` sobre el grafo de `ix_cargo_deps`, y ve que los rangos no suman 1. ¿Hay algo roto?**
> No necesariamente. IX descarta el rango de los nodos colgantes, y todo crate sin dependencia de IX es uno, así que el vector bruto suma 1 − α x_D/(1 − α), donde x_D es su rango total (§6). Dividir por la suma da PageRank con saltos uniformes desde esos crates (§2), que es lo que devuelve `ix_pagerank`. Señala también que los pesos se ignoran, y que las aristas van de un crate a sus dependencias, así que el rango fluye hacia los crates de los que dependen los demás.

**2. ¿Por qué la iteración de potencias con A no encuentra la centralidad de vector propio de una estrella, y por qué funciona la iteración de IX con A + I aunque su comentario da la razón equivocada?**
> Una estrella es bipartita, así que −λ_1 es un valor propio además de λ_1, y el iterado alterna: desde (1, 1, 1, 1) vuelve a ser uniforme tras cada número par de pasos. Con A + I los valores propios pasan a ser λ_i + 1, y como λ_n ≥ −λ_1, |λ_n + 1| < λ_1 + 1: el vector de Perron domina estrictamente. Los valores propios desplazados no son todos positivos, como afirma el comentario, ya que uno de los de la estrella es 1 − √3; lo que la iteración necesita es la dominancia estricta en módulo.

**3. `compute_laplacian_spectrum` informa de 2 componentes y devuelve un vector de Fiedler. ¿Qué compruebas antes de usarlos?**
> Si el grafo es realmente no conexo: un valor propio cuenta como cero por debajo de un umbral absoluto de 10^-6, que también alcanza un camino conexo de 3142 vértices o más, así que cuenta las componentes con una búsqueda en anchura. Si el grafo es no conexo, μ_2 = 0 se repite y el vector es uno de los muchos del núcleo, cuyos signos no significan nada: parte primero por componentes, y toma el vector de Fiedler de cada componente.

**4. En la cometa de Krackhardt, ¿qué vértice es el más central?**
> Depende de la pregunta. Diane tiene más vínculos y la mayor centralidad de vector propio, Fernando y Garth son los más cercanos a todos, con 9/14, y Heather controla el único paso hacia Ike y Jane, con intermediación 14. Un informe debe nombrar la medida y decir por qué encaja con la pregunta.

**Criterio de aprobación:** Describir un grafo por A, D y L; definir PageRank, su tratamiento de los nodos colgantes y la cota de su error; calcular y comparar las cuatro centralidades; demostrar que L es semidefinido positivo y que sus valores propios nulos cuentan las componentes; partir un grafo con el vector de Fiedler y decir cuándo no está determinado; y rastrear dónde los comentarios, el catálogo, los manejadores y las pruebas de IX prometen más de lo que el código entrega.

---

## Base de investigación

- E. W. Dijkstra, «A note on two problems in connexion with graphs», *Numerische Mathematik* 1, 1959: el algoritmo del camino más corto
- P. Bonacich, «Factoring and weighting approaches to status scores and clique identification», *Journal of Mathematical Sociology* 2, 1972: la centralidad de vector propio
- D. B. Johnson, «A note on Dijkstra's shortest path algorithm», *Journal of the ACM* 20, 1973: trabajo exponencial con pesos negativos
- M. Fiedler, «Algebraic connectivity of graphs», *Czechoslovak Mathematical Journal* 23, 1973: la conectividad algebraica
- M. Fiedler, «A property of eigenvectors of nonnegative symmetric matrices and its application to graph theory», *Czechoslovak Mathematical Journal* 25, 1975: los lados conexos del vector de Fiedler
- L. C. Freeman, «A set of measures of centrality based on betweenness», *Sociometry* 40, 1977: la intermediación
- D. Krackhardt, «Assessing the political landscape: structure, cognition, and power in organizations», *Administrative Science Quarterly* 35, 1990: la cometa
- B. Mohar, «Eigenvalues, diameter, and mean distance in graphs», *Graphs and Combinatorics* 7, 1991: la cota inferior de μ_2
- S. Wasserman y K. Faust, *Social Network Analysis: Methods and Applications*, Cambridge University Press, 1994: las centralidades, y la cercanía en grafos no conexos
- F. R. K. Chung, *Spectral Graph Theory*, American Mathematical Society, 1997: el laplaciano normalizado y la desigualdad de Cheeger
- S. Brin y L. Page, «The anatomy of a large-scale hypertextual Web search engine», *Computer Networks and ISDN Systems* 30, 1998: PageRank
- L. Page, S. Brin, R. Motwani y T. Winograd, «The PageRank citation ranking: bringing order to the Web», informe técnico del Stanford InfoLab, 1999: el navegante aleatorio y el factor de amortiguamiento
- J. Shi y J. Malik, «Normalized cuts and image segmentation», *IEEE Transactions on Pattern Analysis and Machine Intelligence* 22, 2000: los cortes normalizados
- U. Brandes, «A faster algorithm for betweenness centrality», *Journal of Mathematical Sociology* 25, 2001: el algoritmo de Brandes
- A. Y. Ng, M. I. Jordan y Y. Weiss, «On spectral clustering: analysis and an algorithm», *Advances in Neural Information Processing Systems* 14, 2002: el agrupamiento espectral
- T. H. Haveliwala y S. D. Kamvar, «The second eigenvalue of the Google matrix», informe técnico de la Universidad de Stanford, 2003: el segundo valor propio es como mucho α en módulo
- A. N. Langville y C. D. Meyer, *Google's PageRank and Beyond: The Science of Search Engine Rankings*, Princeton University Press, 2006: los nodos colgantes y la forma de sistema lineal
- U. von Luxburg, «A tutorial on spectral clustering», *Statistics and Computing* 17, 2007: el agrupamiento espectral y los laplacianos de grafo
- A. E. Brouwer y W. H. Haemers, *Spectra of Graphs*, Springer, 2012: los espectros de las matrices de adyacencia y de los laplacianos
- R. A. Horn y C. R. Johnson, *Matrix Analysis*, 2.ª ed., Cambridge University Press, 2013: el teorema de Perron–Frobenius
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
