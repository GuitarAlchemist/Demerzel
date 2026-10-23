---
module_id: mat-020-markov-chains-hmm
department: mathematics
course: Cadenas de Markov y modelos de Markov ocultos
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning, mat-019-graphs-centrality-spectral]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Cadenas de Markov y modelos de Markov ocultos — Dónde se asienta una cadena, y qué deja ver una cadena oculta

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Escribir una cadena de Markov como una matriz estocástica, hacer avanzar una distribución con ella, y encontrar su distribución estacionaria
- Decir cuándo una cadena finita tiene una única distribución estacionaria y cuándo la distribución converge a ella, y reconocer una cadena periódica en la que no converge
- Calcular exactamente los tiempos de alcance, los tiempos de retorno y las probabilidades de absorción, y decir qué estima en su lugar una simulación truncada
- Evaluar y decodificar un modelo de Markov oculto con los algoritmos hacia delante–hacia atrás y de Viterbi, y explicar cuándo discrepan las dos decodificaciones
- Obtener Baum–Welch como un caso del algoritmo EM, y decir qué garantiza y qué no
- Rastrear lo que garantizan `MarkovChain`, `HiddenMarkovModel`, sus manejadores y `model_code_evolution` de IX, y dónde sus guías, contratos y pruebas prometen más de lo que el código entrega

---

## 1. Las cadenas de Markov como matrices

Una cadena de Markov sobre los estados 0 a n − 1 pasa en cada paso del estado i al estado j con una probabilidad P_ij que solo depende de i: el estado siguiente solo depende del pasado a través del presente, que es la **propiedad de Markov**. La matriz P es **estocástica**: sus entradas son no negativas y cada fila suma 1. Una distribución sobre los estados es un vector fila μ, y un paso la lleva a μP, así que tras t pasos μ_t = μ_0 Pᵗ; la entrada (Pᵏ)_ij es la probabilidad de estar en j k pasos después de estar en i, y Pᵏ⁺ˡ = Pᵏ Pˡ (la ecuación de Chapman–Kolmogorov).

Una **distribución estacionaria** es una distribución π con πP = π: un vector propio por la izquierda de P para el valor propio 1. El valor propio 1 existe siempre, ya que P𝟙 = 𝟙, y ningún valor propio es mayor en módulo: para un vector fila x, Σ_j |Σ_i x_i P_ij| ≤ Σ_i |x_i| Σ_j P_ij, así que ‖xP‖₁ ≤ ‖x‖₁. Que π sea única, y que μ_t se le acerque, depende de la cadena (§2).

La cadena con dos estados, P = [[1 − a, a], [b, 1 − b]] con a + b > 0, lo muestra todo a la vez. Su distribución estacionaria es π = (b, a)/(a + b), su otro valor propio es 1 − a − b, y μ_t − π = (μ_0 − π)(1 − a − b)ᵗ: una diferencia (δ, −δ) se lleva a (1 − a − b)(δ, −δ). La propia prueba de IX usa la cadena del tiempo con a = 0.3 y b = 0.4, cuya distribución estacionaria es (4/7, 3/7), y la distancia a ella se multiplica por 0.3 en cada paso.

### Ejercicio práctico

Comprueba que π = (b, a)/(a + b) es estacionaria para la cadena con dos estados, y que es la única distribución estacionaria cuando a + b > 0.

> *Solución:* La primera entrada de πP es (b(1 − a) + ab)/(a + b) = b/(a + b), y la segunda es (ba + a(1 − b))/(a + b) = a/(a + b). Una distribución estacionaria (x, 1 − x) debe enviar en cada paso tanta probabilidad de 0 a 1 como de 1 a 0: x a = (1 − x) b, así que x = b/(a + b), la única solución. Cuando a = b = 0 nada se mueve, y toda distribución es estacionaria.

---

## 2. Distribuciones estacionarias y convergencia

Una cadena es **irreducible** cuando cada estado puede alcanzar todos los demás: el grafo dirigido con una arista i → j siempre que P_ij > 0 es fuertemente conexo. El **período** de un estado i es el máximo común divisor de los k ≥ 1 con (Pᵏ)_ii > 0; todos los estados de una cadena irreducible lo comparten, y la cadena es **aperiódica** cuando vale 1. Dos teoremas resuelven entonces las preguntas del §1 para una cadena finita (Norris 1997):

- Una cadena irreducible tiene exactamente una distribución estacionaria, y todas sus entradas son positivas. Es el teorema de Perron–Frobenius del MAT-019 §1, en su forma para matrices no negativas irreducibles, aplicado a P.
- Si además la cadena es aperiódica, μ_0 Pᵗ → π desde cualquier inicio. P es entonces **primitiva**: alguna potencia Pᵏ tiene todas sus entradas positivas. Wielandt (1950) demostró que k = (n − 1)² + 1 basta siempre, y que su matriz lo necesita: i → i + 1 para i < n − 1, y n − 1 → 0 o 1 con probabilidad ½ cada uno, cuyos ciclos tienen longitudes n y n − 1.

La periodicidad no es un tecnicismo. El paseo aleatorio sobre el camino 0–1–2, P = [[0, 1, 0], [½, 0, ½], [0, 1, 0]], es irreducible con período 2, y su distribución estacionaria es (1/4, 1/2, 1/4), el d_i/(2m) del MAT-019 §2 con grados 1, 2, 1 y m = 2. Desde el inicio uniforme, un paso da (1/6, 2/3, 1/6) y el siguiente da de nuevo (1/3, 1/3, 1/3): la distribución alterna para siempre, y π es la media de las dos. Para toda cadena irreducible, las medias (1/T) Σ_(t<T) μ_0 Pᵗ convergen a π, y el teorema ergódico dice más: a lo largo de una sola trayectoria, la fracción de los T primeros pasos pasada en el estado j tiende a π_j con probabilidad 1, sea cual sea el período.

Una cadena cumple el **equilibrio detallado** cuando π_i P_ij = π_j P_ji para todos i y j; sumando sobre i se obtiene entonces πP = π, así que el equilibrio detallado es una forma rápida de encontrar π, y tal cadena se llama reversible. El paseo aleatorio sobre un grafo no dirigido es reversible con π_i = d_i/(2m), ya que los dos lados valen 1/(2m) en cada arista.

### Ejercicio práctico

Encuentra la distribución estacionaria de P = [[0, 1], [1, 0]], y di si μ_0 Pᵗ converge.

> *Solución:* Por el §1 con a = b = 1, π = (½, ½) es la única distribución estacionaria. Desde μ_0 = (x, 1 − x), μ_t alterna entre (x, 1 − x) y (1 − x, x), así que solo converge si x = ½, donde es constante desde el inicio. La cadena tiene período 2, y el valor propio −1 de P mantiene viva la diferencia μ_0 − π, con el signo cambiado en cada paso.

---

## 3. Tiempos de alcance y cadenas absorbentes

El **tiempo de alcance** de un estado j es T_j = min{t ≥ 1 : X_t = j}. Condicionar sobre el primer paso da, para todo i ≠ j, h_i = 1 + Σ_(k≠j) P_ik h_k, donde h_i es el tiempo de alcance esperado desde i: un sistema lineal con una incógnita por estado distinto de j, cuya solución es única y finita cuando j es alcanzable desde todo estado. Desde el propio j, el mismo paso da el **tiempo de retorno** esperado m_jj = 1 + Σ_(k≠j) P_jk h_k, y la fórmula de Kac afirma que m_jj = 1/π_j para una cadena irreducible (Kac 1947). Reuniendo todos los pares en una matriz M, con J la matriz de unos y M_dg la diagonal de M, el sistema se escribe M = J + P(M − M_dg) (Kemeny y Snell 1960). La resta importa: el sistema M = J + PM no tiene solución (§6).

Un estado j con P_jj = 1 es **absorbente**. Cuando todo estado puede alcanzar uno absorbente, ordena primero los estados transitorios, de modo que P = [[Q, R], [0, I]]. La **matriz fundamental** N = (I − Q)^-1 = I + Q + Q² + … cuenta visitas: N_ik es el número esperado de visitas al estado transitorio k desde i. El número esperado de pasos antes de la absorción es t = N𝟙, y la matriz de las probabilidades de absorción es B = NR. Para una ruina del jugador equitativa sobre 0 a 4, con los estados transitorios 1, 2, 3 y pasos de ±1 con probabilidad ½,

N = [[3/2, 1, 1/2], [1, 2, 1], [1/2, 1, 3/2]], t = (3, 4, 3),

así que la partida dura en promedio k(4 − k) pasos desde k, y la columna de B para el estado 4 es (1/4, 1/2, 3/4) = k/4.

Estas respuestas exactas cuestan una resolución lineal. Una simulación que lanza paseos desde i y detiene cada uno tras L pasos solo puede promediar los paseos que llegaron, así que estima E[T | T ≤ L], no E[T]. Para un estado que sale en cada paso con probabilidad p hacia un estado absorbente, T es geométrica, y con q = 1 − p,

E[T | T ≤ L] = 1/p − L qᴸ/(1 − qᴸ).

Con p = 0.1 y L = 10 esto vale 4.6466, frente a E[T] = 10, y solo llegan 1 − 0.9^10 ≈ 65% de los paseos. Lanzar más paseos reduce el ruido pero no este sesgo; una simulación debe informar de cuántos paseos llegaron, y cuando la cadena es conocida, el sistema lineal da el valor exacto.

### Ejercicio práctico

Encuentra el tiempo de retorno esperado al estado 0 de la cadena del tiempo del §1 condicionando sobre el primer paso, y comprueba la fórmula de Kac.

> *Solución:* Desde el estado 1, la cadena pasa a 0 con probabilidad 0.4 en cada paso, así que h_1 = 1 + 0.6 h_1 y h_1 = 2.5. Desde 0, el paso siguiente se queda en 0 con probabilidad 0.7, lo que es un retorno tras un paso, o pasa a 1 con probabilidad 0.3: m_00 = 1 + 0.3 · 2.5 = 1.75 = 7/4. La distribución estacionaria da π_0 = 4/7, y 1/π_0 = 7/4.

---

## 4. Modelos de Markov ocultos: evaluación y decodificación

En un **modelo de Markov oculto**, una cadena de estados q_1, …, q_T no se observa; cada estado emite un símbolo o_t, que sí se observa. El modelo tiene una distribución inicial ν, una matriz de transición A y una matriz de emisión B, con B_ik la probabilidad de que el estado i emita el símbolo k. La probabilidad de las observaciones y de un camino q es ν_(q_1) B_(q_1, o_1) Π_(t≥2) A_(q_(t−1), q_t) B_(q_t, o_t), y Rabiner (1989) enumera tres problemas: la probabilidad P(O) de las observaciones, los estados ocultos más probables, y los parámetros que hacen probables las observaciones.

El **algoritmo hacia delante** calcula P(O) sin enumerar los nᵀ caminos. Con α_1(i) = ν_i B_i(o_1) y α_(t+1)(j) = (Σ_i α_t(i) A_ij) B_j(o_(t+1)), α_t(i) es la probabilidad de las t primeras observaciones con q_t = i, y P(O) = Σ_i α_T(i), en O(T n²) operaciones. Las variables hacia atrás β_T(i) = 1 y β_t(i) = Σ_j A_ij B_j(o_(t+1)) β_(t+1)(j) dan la probabilidad de las observaciones posteriores desde q_t = i, y γ_t(i) = α_t(i) β_t(i)/P(O) es la probabilidad a posteriori del estado i en el instante t. Como α_t decrece más o menos geométricamente con t, sufre desbordamiento por abajo en las secuencias largas; las implementaciones reescalan cada α_t para que sume 1 con un factor c_t y suman los logaritmos: log P(O) = Σ_t log c_t.

El **algoritmo de Viterbi** sustituye la suma por un máximo. En logaritmos, δ_1(i) = log(ν_i B_i(o_1)) y δ_t(j) = max_i (δ_(t−1)(i) + log A_ij) + log B_j(o_t), con un puntero al i que alcanza el máximo; seguir los punteros hacia atrás desde el mejor estado final da el camino más probable en su conjunto (Viterbi 1967; Forney 1973). La **decodificación a posteriori** toma en cambio, en cada t, el estado con mayor γ_t(i). Maximiza el número esperado de estados correctos, pero la secuencia que devuelve no tiene por qué ser un camino posible.

El modelo del tiempo de IX tiene los estados ocultos Lluvioso (0) y Soleado (1), los símbolos Caminar, Comprar y Limpiar, ν = (0.6, 0.4), A = [[0.7, 0.3], [0.4, 0.6]] y B = [[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]]. Para Caminar, Comprar, Limpiar, P(O) = 8403/250000 = 0.033612; el camino más probable es Soleado, Lluvioso, Lluvioso, con probabilidad 42/3125 = 0.01344, y la probabilidad a posteriori de Soleado es 0.7683, 0.3759 y 0.1360 en los tres pasos. Aquí las dos decodificaciones coinciden. Discrepan en un modelo con tres estados y un solo símbolo, de modo que las observaciones no aportan información: ν = (0.4, 0.3, 0.3), el estado 0 se queda en 0, el estado 1 pasa a 2, y el estado 2 se queda en 2. Tras dos pasos, γ_1 = (0.4, 0.3, 0.3) y γ_2 = (0.4, 0, 0.6), así que la decodificación a posteriori devuelve (0, 2), un camino de probabilidad 0, ya que 0 nunca pasa a 2; Viterbi devuelve (0, 0), con probabilidad 0.4.

### Ejercicio práctico

Demuestra que Σ_i α_t(i) β_t(i) = P(O) para todo t.

> *Solución:* α_t(i) es la probabilidad de o_1, …, o_t y q_t = i, y β_t(i) es la probabilidad de o_(t+1), …, o_T dado q_t = i. Dado el estado presente, las observaciones posteriores no dependen de las anteriores (la propiedad de Markov de la cadena oculta, con cada símbolo dependiendo solo de su estado), así que el producto es la probabilidad de todas las observaciones y de q_t = i. Sumar sobre i da P(O).

---

## 5. Aprendizaje: Baum–Welch como EM

El **algoritmo de Baum–Welch** ajusta ν, A y B a una secuencia observada (Baum et al. 1970). Su paso E calcula las probabilidades a posteriori γ_t(i) y ξ_t(i, j) = α_t(i) A_ij B_j(o_(t+1)) β_(t+1)(j)/P(O), la probabilidad del paso de i a j entre t y t + 1. Su paso M fija ν̂_i = γ_1(i), Â_ij = Σ_(t<T) ξ_t(i, j)/Σ_(t<T) γ_t(i) y B̂_ik = Σ_(t : o_t = k) γ_t(i)/Σ_t γ_t(i): recuentos esperados divididos por totales esperados. Es el algoritmo EM del MAT-018 §3 con el camino oculto como dato faltante (Dempster, Laird y Rubin 1977), y hereda la misma garantía y los mismos límites: la verosimilitud nunca disminuye, pero los iterados pueden asentarse en un máximo local o en un punto de silla en lugar del máximo global.

De las fórmulas se siguen cuatro consecuencias:
- **Los ceros siguen siendo cero.** Un cero en A, B o ν anula cada término del recuento esperado correspondiente (ver el ejercicio).
- **La simetría se conserva.** Si intercambiar dos estados deja el modelo sin cambios, sus probabilidades a posteriori son iguales, y también sus parámetros reestimados, como para las componentes idénticas del MAT-018 §3.
- **Una secuencia da un solo inicio.** ν̂ = γ_1 viene del primer instante de la única secuencia, así que a medida que el modelo se afina suele acabar poniendo probabilidad 1 en un solo estado.
- **Los estados no tienen nombre.** Cualquier reetiquetado de los estados da la misma verosimilitud; los estados solo son identificables salvo permutación.

Toma la secuencia 0, 1, 0, 1, … de longitud 100, dos estados y dos símbolos. El modelo que alterna sin fallar, con A = [[0, 1], [1, 0]], B la identidad y ν = (1, 0), le da probabilidad 1, el máximo. Desde el inicio completamente simétrico, ν = (½, ½), todas las entradas de A iguales a ½ y las dos filas de emisión (0.6, 0.4), un paso M da a las dos filas de emisión las frecuencias (½, ½) de los datos y deja todo lo demás en ½. Bajo ese modelo, toda secuencia de longitud 100 tiene probabilidad 2^-100, así que la log-verosimilitud es 100 ln ½ ≈ −69.3147, y el paso M siguiente no cambia nada: un punto fijo que no es un máximo. La prueba de IX parte en cambio de un modelo ligeramente asimétrico (§6).

### Ejercicio práctico

Demuestra que un paso M nunca convierte un cero de A, B o ν en un valor positivo, siempre que el estado en cuestión tenga masa a posteriori positiva, para que el cociente esté definido.

> *Solución:* Si A_ij = 0, cada ξ_t(i, j) contiene el factor A_ij, así que cada uno es 0, su suma es 0, y Â_ij = 0. Si B_ik = 0, entonces α_t(i) = 0 en cada t con o_t = k, así que γ_t(i) = 0 allí y el numerador de B̂_ik es 0. Si ν_i = 0, entonces α_1(i) = 0 y ν̂_i = γ_1(i) = 0. Un cero introducido por error es por tanto permanente, y un cero estructural, un paso que el modelo debe prohibir, se conserva.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea a Python de `crates/ix-graph/src/markov.rs`, de `crates/ix-graph/src/hmm.rs`, de los dos manejadores de abajo y de `model_code_evolution`, con una réplica del `StdRng` de rand 0.9 para las simulaciones, comprobada frente a extracciones del propio rand. Estos números son predicciones, y el §7 propone comprobarlos.

**La cadena y su manejador.** [`MarkovChain::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L20) comprueba que la matriz es cuadrada y que cada fila suma 1 [con una tolerancia de 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L27); como [dicen](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L8) los contratos de IX, no rechaza las entradas negativas. [`stationary_distribution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L56) parte de la [distribución uniforme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L58) y ejecuta:

```rust
        for _ in 0..max_iter {
            let new_dist = dist.dot(&self.transition);
            let diff = (&new_dist - &dist).mapv(f64::abs).sum();
            dist = new_dist;
            if diff < tol {
                break;
            }
        }
```

La herramienta MCP `ix_markov` llama a [`markov`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1320), que pasa su parámetro `steps` como `max_iter` con una [tolerancia de 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1327) y añade [`is_ergodic(100)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1328) a su respuesta. [`mean_first_passage`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L94) simula paseos, detiene cada uno tras `max_steps`, y termina con:

```rust
        if reached == 0 {
            f64::INFINITY
        } else {
            total_steps as f64 / reached as f64
        }
```

- **En una cadena periódica, la respuesta depende de la paridad de `steps`.** En el camino 0–1–2 del §2, los iterados alternan entre el vector uniforme y (1/6, 2/3, 1/6), el cambio vale 2/3 en cada pasada, y el bucle llega hasta `max_iter`: `ix_markov` devuelve (1/6, 2/3, 1/6) para un `steps` impar y (1/3, 1/3, 1/3) para uno par, nunca (1/4, 1/2, 1/4), y nada en la respuesta dice que el bucle no convergió. Los contratos de IX sí advierten de que quien llama [no puede distinguir](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L11) la convergencia del corte; `is_ergodic` es false aquí, que es el único indicio. En [[0, 1], [1, 0]] la función devuelve (½, ½) tras una pasada, porque el inicio uniforme ya es estacionario: el éxito no dice nada de la convergencia. La guía de IX dice de esta cadena que [«never actually converges»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/markov-chains.md#L195), lo que es cierto de `state_distribution` desde otros inicios, no de esta función.
- **Las entradas negativas pasan.** Las filas de [[1.1, −0.1], [0.5, 0.5]] suman 1, y `ix_markov` devuelve aproximadamente (1.25, −0.25) como distribución estacionaria, una solución verdadera de πP = π con una entrada negativa, junto con `is_ergodic` false. `HiddenMarkovModel::new` [rechaza los valores negativos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L80).
- **`is_ergodic` comprueba si cada entrada de Pᵏ supera [10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L144)**, y el manejador toma siempre k = 100. Una cadena irreducible y aperiódica puede fallar de dos maneras. La matriz de Wielandt sobre 11 estados necesita (11 − 1)² + 1 = 101 pasos, así que P^100 todavía tiene una entrada nula y la respuesta es false; sobre 10 estados necesita 82, y la respuesta es true. La cadena [[1 − ε, ε], [ε, 1 − ε]] con ε = 10^-12 se mezcla tan despacio que las entradas fuera de la diagonal de P^100 quedan justo por debajo de 100ε = 10^-10, y la respuesta vuelve a ser false. Una respuesta positiva es correcta, ya que una potencia positiva prueba que la cadena es irreducible y aperiódica; no hay ninguna prueba de irreducibilidad ni del período.
- **`mean_first_passage` solo promedia los paseos que llegaron.** Un paseo que no ha alcanzado el objetivo tras `max_steps` se [descarta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L119) sin contarse, así que el resultado estima el E[T | T ≤ L] del §3, con L = `max_steps`. En [[0.9, 0.1], [0, 1]], de 0 a 1 con 10 000 paseos y la semilla 42, la transcripción predice 4.6178 con `max_steps` 10, donde llegan 6449 paseos, y 10.1787 con 1000, frente al valor exacto 10. La guía de IX pide [«at least 10,000 simulations»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/markov-chains.md#L189), lo que reduce el ruido y no este sesgo, y llama al sistema exacto «M = 1 + P * M», que no tiene solución (ver el ejercicio). No hay tiempo de alcance exacto, ni matriz fundamental, ni probabilidad de absorción; [`AbsorbingChain`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L149) se limita a listar los estados cuya [entrada diagonal vale exactamente 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L157).
- **`model_code_evolution` predice una caída que sus datos nunca mostraron.** En `crates/ix-code`, [`model_code_evolution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L303) reparte un historial de puntuaciones de calidad en clases, cuenta las transiciones, añade [10^-6 a cada casilla](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L356) antes de normalizar, y da como tiempo medio hasta la clase de calidad más baja el valor de [`mean_first_passage` con 200 paseos de como mucho 1000 pasos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L381). Una clase que nunca se abandonó no tiene recuentos, así que su fila es uniforme. Para el historial creciente 0, 1, 2, 3 con 4 estados, la clase superior nunca se abandonó, y el modelo predice una caída a la clase más baja en unos 7 pasos (6.99998 exactamente para esta matriz, 7.53 por la simulación), para una calidad que solo subió. Para 1, 2, …, 8, a la clase superior solo la siguió siempre ella misma: el tiempo medio exacto es de unos 1.0 × 10^6 pasos, pero solo uno de los 200 paseos alcanza la clase más baja en 1000 pasos, y la función devuelve 878. Su prueba, [`test_markov_evolution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L591), solo comprueba las sumas de las filas y las longitudes, y nada más llama a la función.
- **El manejador de Viterbi comprueba el modelo pero no los símbolos.** [`viterbi`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1339) construye el modelo con [`HiddenMarkovModel::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1353) pero nunca compara las observaciones con el número de columnas de emisión, así que un símbolo fuera de rango indexa más allá de la matriz de emisión, lo que provoca un pánico en `ndarray`. La función de DuckDB `ix_viterbi` lo [rechaza](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L531) con un error SQL, como promete su [invariante](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L517). Para una secuencia imposible, como 0 y luego 1 bajo un modelo cuyos estados nunca cambian y siempre emiten su propio índice, cada puntuación vale −∞, la [comparación estricta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L268) nunca se activa, el camino recae en el estado 0 en cada paso, y la salida JSON escribe la log-probabilidad −∞ como `null`.
- **NaN pasa los dos constructores.** Una suma NaN hace falso [`(row_sum - 1.0).abs() > 1e-6`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L57), y una entrada NaN hace falso [`v < 0.0`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L77), así que ninguna de las dos comprobaciones lo rechaza, en `HiddenMarkovModel::new` como en `MarkovChain::new`. JSON no puede transportar NaN, así que solo quien llama desde Rust puede llegar a esto.
- **El código, la guía y los contratos discrepan sobre Baum–Welch.** [`baum_welch`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L330) clona el modelo, devuelve la copia entrenada como `Result<Self, String>`, y se detiene cuando la log-verosimilitud cambia [menos de `tol`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L353). Los contratos de IX dicen que [«MUTATES the HMM in place and returns the final log-likelihood»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L14), sin garantía de mejora monótona «due to numerical underflow», y que [no devuelve un Result](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L24). Las recursiones reescaladas existen para evitar el desbordamiento por abajo, y por el §5 EM nunca baja la verosimilitud, como dice la propia [guía de los HMM](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/hidden-markov-models.md#L214) de IX; en la secuencia de la prueba de IX, la transcripción encuentra una subida en cada uno de los 50 pasos.
- **Algunas pruebas pasarían con código erróneo.** [`test_baum_welch_improves_likelihood`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L627) afirma que la log-verosimilitud tras el entrenamiento es al menos la de antes [menos 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L637), lo que cumpliría un `baum_welch` que devolviera su entrada sin cambios. La transcripción predice −14.6565 antes y −13.0797 tras 50 pasos, con una distribución inicial colapsada en (0, 1) salvo 10^-55, el efecto de secuencia única del §5. [`test_forward_backward_consistency`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L738) anuncia que la log-probabilidad hacia delante [«should match what we compute from alpha alone»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L739), y luego solo comprueba que γ está en [0, 1] y que la log-probabilidad es finita. [`test_baum_welch_recovers_parameters`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L687) entrena sobre la secuencia alternante del §5 desde un inicio ligeramente asimétrico; la transcripción predice que alcanza el modelo alternante del §5, con log-verosimilitud 0, tras 7 reestimaciones. Esa prueba solo [comprueba que las emisiones se especializan](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L709), que es la comprobación correcta, ya que ningún parámetro verdadero generó los datos.
- **El catálogo nombra el crate equivocado.** El catálogo que envía `ix_explain_algorithm` lista el HMM como [«ix_probabilistic::HMM (viterbi)»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5844); `ix-probabilistic` contiene filtros de Bloom, count-min y cuco y HyperLogLog, y el HMM está en `ix_graph::hmm`.
- **Otras lagunas.** No hay distribución estacionaria exacta por resolución lineal, ni prueba de irreducibilidad o del período, ni tiempo de alcance exacto o análisis de absorción, ni Baum–Welch sobre varias secuencias, ni muestreo desde un modelo de Markov oculto, ni operación MCP para el algoritmo hacia delante, la decodificación a posteriori o Baum–Welch: `ix_markov` e `ix_viterbi` son las dos únicas.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Demuestra que el sistema M = J + PM nombrado en la guía de IX no tiene solución, y que el sistema del §3 da la fórmula de Kac.

> *Solución:* Sea π una distribución estacionaria. Multiplicar M = J + PM por la izquierda por π da πM = πJ + πM, ya que πP = π; como las entradas de π suman 1, πJ es la fila de unos, así que 0 = (1, …, 1), lo que es imposible. El sistema del §3, M = J + P(M − M_dg), da en cambio πM = πJ + πM − πM_dg, así que πM_dg = (1, …, 1): π_j m_jj = 1 para todo j, que es la fórmula de Kac.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Paridad.** Llama a `markov` con la cadena del camino del §2 y `steps` 1, luego 100. Predicción: (1/6, 2/3, 1/6), luego (1/3, 1/3, 1/3), con `is_ergodic` false las dos veces; la media de las dos es (1/4, 1/2, 1/4).
2. **Ergodicidad.** Llama a `is_ergodic(100)` sobre la matriz de Wielandt con 10 y 11 estados, y sobre la cadena de dos estados con ε = 10^-12. Predicción: true, false, false; y true para 11 estados con `is_ergodic(101)`.
3. **Truncamiento.** Llama a `mean_first_passage` sobre [[0.9, 0.1], [0, 1]] de 0 a 1 con 10 000 paseos y la semilla 42, y `max_steps` 10, luego 1000; luego de 0 de vuelta a 0 sobre la cadena del tiempo del §1, con 10 000 paseos de como mucho 1000 pasos y la semilla 7. Predicción: 4.6178, 10.1787, y 1.7538 frente al 7/4 de Kac.
4. **Evolución del código.** Llama a `model_code_evolution` sobre 0, 1, 2, 3 y sobre 1, 2, …, 8, con 4 estados. Predicción: el estado actual 3 las dos veces, y un tiempo medio hasta el estado crítico de 7.53, luego 878.
5. **Tiempo.** Construye el modelo del tiempo de IX y llama a `forward`, `viterbi` y `forward_backward` sobre Caminar, Comprar, Limpiar. Predicción: la exponencial de la log-probabilidad vale 0.033612, el camino Soleado, Lluvioso, Lluvioso tiene log-probabilidad ln 0.01344, y la probabilidad a posteriori de Soleado vale 0.7683, 0.3759 y 0.1360.
6. **Decodificadores.** Llama a `map_estimate` y `viterbi` sobre el modelo de tres estados del §4 con dos observaciones; luego llama al manejador `viterbi` sobre las observaciones 0, 1 del modelo cuyos estados nunca cambian, luego con el símbolo 2, en un proceso hijo. Predicción: (0, 2), luego (0, 0) con probabilidad 0.4; el camino (0, 0) con una log-probabilidad `null`; luego un pánico.
7. **Baum–Welch.** Ejecuta `baum_welch` sobre la secuencia alternante de longitud 100 desde el inicio simétrico del §5 y desde el inicio de la prueba de IX, con 100 pasos y una tolerancia de 10^-10. Predicción: todos los parámetros a ½ y la log-verosimilitud −69.3147 tras 2 pasos; el modelo alternante y la log-verosimilitud 0 tras 7.

### Ejercicio práctico

¿Por qué la predicción para `max_steps` 1000 en el paso 3 no vale exactamente 10, y está sesgada?

> *Solución:* Un paseo no alcanza el objetivo en 1000 pasos con probabilidad 0.9^1000, alrededor de 1.7 × 10^-46, así que el sesgo de truncamiento es despreciable ahí. La diferencia es ruido de muestreo: T tiene desviación típica √0.9/0.1 ≈ 9.49, así que la media de 10 000 paseos tiene un error típico de alrededor de 0.095, y 10.1787 está alrededor de 1.9 errores típicos por encima de 10. Otra semilla caería en otro punto alrededor de 10, mientras que con `max_steps` 10 cualquier semilla cae cerca de 4.6466.

---

## 8. Errores comunes

- **Leer un resultado de iteración de potencias como estacionario sin comprobarlo.** Calcula ‖πP − π‖₁; en una cadena periódica los iterados oscilan, y promediar muchos iterados consecutivos, o resolver el sistema lineal, da π.
- **Confiar en una convergencia desde el inicio uniforme.** En una cadena cuya distribución estacionaria es uniforme, la primera pasada ya se detiene, sea cual sea el período.
- **Tomar «todas las entradas de P^100 por encima de 10^-10» por ergodicidad.** La irreducibilidad es una cuestión de conexión fuerte en el grafo de las entradas positivas, y el período es un máximo común divisor de longitudes de ciclos; responde a las dos directamente.
- **Promediar solo los paseos que llegaron.** Informa de cuántos llegaron, o resuelve el sistema lineal del §3.
- **Predecir a partir de filas que los datos nunca llenaron.** Un estado que nunca se abandonó no tiene datos para su fila, y el suavizado hace uniforme esa fila; informa de los recuentos detrás de cada fila.
- **Leer una decodificación a posteriori como un camino.** Cada estado es el más probable en su propio paso, y la secuencia puede ser imposible; usa Viterbi para un camino.
- **Arrancar Baum–Welch desde un modelo simétrico o con ceros que no querías.** La simetría es un punto fijo y los ceros son permanentes; parte de varios puntos aleatorios y quédate con la mejor verosimilitud.
- **Aprender la distribución inicial de una sola secuencia.** Colapsa en un solo estado; fíjala, o entrena con varias secuencias.
- **Enviar a `ix_viterbi` un símbolo mayor o igual que el número de columnas de emisión.** El manejador MCP entra en pánico; comprueba antes los símbolos, o usa la función de DuckDB, que devuelve un error.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Matriz estocástica** | Una matriz con entradas no negativas cuyas filas suman 1 cada una |
| **Distribución estacionaria** | Una distribución π con πP = π |
| **Cadena irreducible** | Una cadena en la que cada estado puede alcanzar todos los demás |
| **Período** | El máximo común divisor de las longitudes de los retornos de un estado a sí mismo |
| **Matriz primitiva** | Una matriz no negativa con una potencia cuyas entradas son todas positivas |
| **Equilibrio detallado** | π_i P_ij = π_j P_ji para todos i y j, lo que hace estacionaria a π |
| **Tiempo de alcance** | El primer instante t ≥ 1 en que la cadena está en un estado dado |
| **Matriz fundamental** | N = (I − Q)^-1 de una cadena absorbente, cuyas entradas cuentan las visitas esperadas |
| **Modelo de Markov oculto** | Una cadena de Markov de estados no observados, cada uno de los cuales emite un símbolo observado |
| **Algoritmo hacia delante** | La recursión que calcula la probabilidad de las observaciones en O(T n²) operaciones |
| **Camino de Viterbi** | La secuencia de estados ocultos más probable dadas las observaciones |
| **Algoritmo de Baum–Welch** | El algoritmo EM para los parámetros de un modelo de Markov oculto |

---

## Autoevaluación

**1. `ix_markov` devuelve (1/6, 2/3, 1/6) como distribución estacionaria de una cadena, con `is_ergodic` false. ¿Qué concluyes, y cómo obtienes π?**
> Comprueba primero πP = π: aquí el resultado se lleva a (1/3, 1/3, 1/3), así que no es estacionario. La cadena es el camino periódico del §2, el bucle llegó hasta `steps` sin converger, y con un `steps` par la respuesta habría sido uniforme. Promedia dos iterados consecutivos, o resuelve π(P − I) = 0 con las entradas de π sumando 1: (1/4, 1/2, 1/4).

**2. Un informe afirma, a partir de `model_code_evolution`, que un crate alcanzará una calidad crítica en 878 commits en promedio. ¿Qué preguntas antes de creerlo?**
> Cuántos de los 200 paseos alcanzaron la clase más baja: el valor solo promedia esos, y en el historial creciente del §6 solo uno llegó, mientras que la media exacta para esa matriz es de unos 10^6. Luego qué filas de la matriz se apoyan en datos: una clase que nunca se abandonó recibe una fila uniforme, que por sí sola puede crear un camino hacia la clase más baja. Por último, si una cadena con unas pocas clases se ajusta siquiera al historial.

**3. Viterbi y la decodificación a posteriori discrepan en una secuencia. ¿Cuál das?**
> Depende de la pregunta. Para la secuencia de estados más probable en su conjunto, por ejemplo para segmentar una señal, da el camino de Viterbi; para acertar el mayor número posible de estados, da la decodificación a posteriori, con sus probabilidades, y di que su secuencia puede ser imposible, como lo es (0, 2) en el modelo del §4.

**4. Baum–Welch se detiene tras dos pasos con todos los parámetros iguales a ½. ¿Está rota la implementación?**
> No necesariamente. Un inicio en el que intercambiar los estados deja el modelo sin cambios sigue siendo simétrico bajo EM (§5), y en la secuencia alternante alcanza un punto fijo con log-verosimilitud 100 ln ½, muy por debajo del máximo 0. Rompe la simetría, lanza varios inicios aleatorios y quédate con la mejor verosimilitud, y contrasta la respuesta con los datos.

**Criterio de aprobación:** Escribir una cadena como una matriz estocástica y encontrar su distribución estacionaria; decir cuándo es única y cuándo la distribución converge a ella; calcular los tiempos de alcance, los tiempos de retorno y las probabilidades de absorción, y decir qué estima una simulación truncada; evaluar y decodificar un modelo de Markov oculto y explicar cuándo discrepan las decodificaciones; obtener Baum–Welch como EM y enunciar su garantía y sus límites; y rastrear dónde las guías, contratos, manejadores y pruebas de IX prometen más de lo que el código entrega.

---

## Base de investigación

- A. A. Markov, «Extension of the law of large numbers to dependent quantities» (en ruso), *Izvestiya of the Physico-Mathematical Society at Kazan University* 15, 1906: las primeras cadenas
- M. Kac, «On the notion of recurrence in discrete stochastic processes», *Bulletin of the American Mathematical Society* 53, 1947: el tiempo medio de retorno
- H. Wielandt, «Unzerlegbare, nicht negative Matrizen», *Mathematische Zeitschrift* 52, 1950: el exponente de una matriz primitiva
- J. G. Kemeny y J. L. Snell, *Finite Markov Chains*, Van Nostrand, 1960: la matriz fundamental y los tiempos medios de primer paso
- A. J. Viterbi, «Error bounds for convolutional codes and an asymptotically optimum decoding algorithm», *IEEE Transactions on Information Theory* 13, 1967: el algoritmo de Viterbi
- L. E. Baum, T. Petrie, G. Soules y N. Weiss, «A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains», *Annals of Mathematical Statistics* 41, 1970: el algoritmo de Baum–Welch y su monotonía
- G. D. Forney, «The Viterbi algorithm», *Proceedings of the IEEE* 61, 1973: el algoritmo como camino más corto
- A. P. Dempster, N. M. Laird y D. B. Rubin, «Maximum likelihood from incomplete data via the EM algorithm», *Journal of the Royal Statistical Society, Series B* 39, 1977: EM
- L. R. Rabiner, «A tutorial on hidden Markov models and selected applications in speech recognition», *Proceedings of the IEEE* 77, 1989: los tres problemas, el reescalado y la decodificación a posteriori
- J. R. Norris, *Markov Chains*, Cambridge University Press, 1997: irreducibilidad, periodicidad, convergencia y el teorema ergódico
- O. Cappé, E. Moulines y T. Rydén, *Inference in Hidden Markov Models*, Springer, 2005: suavizado, decodificación e identificabilidad
- D. A. Levin, Y. Peres y E. L. Wilmer, *Markov Chains and Mixing Times*, American Mathematical Society, 2009: las velocidades de convergencia
- R. A. Horn y C. R. Johnson, *Matrix Analysis*, 2.ª ed., Cambridge University Press, 2013: las matrices primitivas y la cota de Wielandt
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
