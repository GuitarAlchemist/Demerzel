---
module_id: mat-025-allocation-games-bandits-penalties
department: mathematics
course: Asignación con restricciones, juegos, bandidos y penalizaciones
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-009-estimation-uncertainty-sampling, mat-012-iterative-optimisation]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Asignación con restricciones, juegos, bandidos y penalizaciones — Lo que pueden prometer un multiplicador, un equilibrio y una cota de arrepentimiento

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Escribir las condiciones KKT de una asignación con restricciones, resolver una pequeña y leer cada multiplicador como un precio sombra
- Enunciar la dualidad de la programación lineal y la holgura complementaria, y resolver a mano un programa de dos variables y su dual
- Encontrar los equilibrios de Nash de un juego bimatricial pequeño por enumeración de soportes, y decir lo que el juego ficticio garantiza y lo que no
- Calcular el valor de Shapley de un juego cooperativo, comprobar un reparto frente al núcleo y explicar por qué los dos pueden discrepar
- Definir el arrepentimiento (regret), comparar ε-voraz con UCB1 y decir lo que la cota de UCB1 supone sobre la escala de las recompensas
- Convertir una restricción en una penalización para una búsqueda que solo conoce cotas de caja, y decir cuándo la penalización es exacta
- Seguir lo que calculan los crates `ix-game`, `ix-rl` e `ix-evolution` de IX, cuáles de sus salidas fija un test y qué dejan fuera

---

## 1. Multiplicadores de Lagrange y condiciones KKT

Una asignación elige x para maximizar un rendimiento f(x) sujeto a restricciones g_i(x) ≤ c_i. Cuando f es cóncava, cada g_i es convexa y algún punto cumple estrictamente todas las restricciones (**condición de Slater**), x* es óptimo exactamente cuando existen multiplicadores λ_i tales que:

```
∇f(x*) = Σ_i λ_i ∇g_i(x*)
g_i(x*) ≤ c_i
λ_i ≥ 0
λ_i (c_i − g_i(x*)) = 0
```

Estas son las **condiciones de Karush–Kuhn–Tucker** (Karush, 1939; Kuhn y Tucker, 1951): estacionariedad, factibilidad primal, factibilidad dual y holgura complementaria. La holgura complementaria dice que una restricción con holgura tiene multiplicador cero. Un multiplicador es también un precio: si V(c) es el valor óptimo en función de los límites, entonces, bajo los mismos supuestos, ∂V/∂c_i = λ_i allí donde V es derivable. λ_i es el **precio sombra** del recurso i, lo que vale en el margen una unidad más de ese recurso.

Repartamos un presupuesto de 10 entre dos actividades que rinden ln(1 + x) y 2 ln(1 + y): maximizar ln(1 + x) + 2 ln(1 + y) sujeto a x + y ≤ 10, con x, y ≥ 0. La estacionariedad da 1/(1 + x) = λ y 2/(1 + y) = λ, así que 1 + y = 2(1 + x). Con el presupuesto gastado, x = 3, y = 7 y λ = 1/4, y el valor es ln 4 + 2 ln 8 = 8 ln 2 ≈ 5.545177. Un presupuesto de 11 da x = 10/3 e y = 23/3, y un valor mayor en unos 0.240128, cerca de λ = 0.25: el multiplicador predice la ganancia de primer orden, y la concavidad hace que la ganancia real sea algo menor.

Pongamos ahora un tope a la segunda actividad, y ≤ 5. La solución anterior viola el tope, así que el tope está activo: y = 5 y x = 5. La estacionariedad se lee 1/6 = λ para x y 2/6 = λ + μ para y, donde μ es el multiplicador del tope, así que λ = μ = 1/6. Ambos son no negativos, así que es un punto KKT, y como el problema es cóncavo, es el óptimo. El valor baja a 3 ln 6 ≈ 5.375278.

### Ejercicio práctico

Con el tope y ≤ 5 en vigor, súbelo a 6 y mantén el presupuesto en 10. ¿Qué predice μ, y cuál es la ganancia real?

> *Solución:* μ = 1/6 predice una ganancia de unos 0.166667. El nuevo óptimo es x = 4, y = 6, todavía sobre ambas restricciones, ya que 1/5 = λ y 2/7 = λ + μ dan λ = 1/5 y μ = 3/35, ambos positivos. Su valor es ln 5 + 2 ln 7 ≈ 5.501258, una ganancia de 0.125980: la estimación de primer orden se pasa, como debe hacerlo con un rendimiento cóncavo.

---

## 2. Programación lineal y dualidad

Cuando el rendimiento y las restricciones son lineales, el problema es un **programa lineal** (P), y tiene un **dual** (D):

```
(P)  max { cᵀx : A x ≤ b, x ≥ 0 }
(D)  min { bᵀu : Aᵀu ≥ c, u ≥ 0 }
```

Todo u factible acota el primal por arriba, ya que cᵀx ≤ (Aᵀu)ᵀx = uᵀAx ≤ uᵀb: es la **dualidad débil**. Si uno de los dos problemas tiene óptimo, ambos lo tienen, con el mismo valor: es la **dualidad fuerte**. En el óptimo, cada restricción primal y su variable dual cumplen la holgura complementaria, y las variables duales son los precios sombra del §1. El método símplex (Dantzig) va de vértice en vértice del polígono factible, ya que un objetivo lineal que tiene un máximo en él lo alcanza en un vértice.

Dos productos rinden 2 y 3 por unidad. La máquina A tiene 4 horas (x + y ≤ 4) y la máquina B tiene 6 horas (x + 3y ≤ 6). Los vértices (0, 0), (4, 0), (0, 2) y (3, 1) rinden 0, 8, 6 y 9, así que el óptimo es (3, 1) con 9. El dual minimiza 4u + 6v sujeto a u + v ≥ 2 y u + 3v ≥ 3. Las dos variables primales son positivas, así que las dos restricciones duales están activas: u = 3/2 y v = 1/2, con valor 4 × 3/2 + 6 × 1/2 = 9. Una hora más en la máquina A mueve el óptimo a (4.5, 0.5), que rinde 10.5 = 9 + u.

Los juegos de suma cero son programas lineales. Si A paga al jugador fila, el teorema minimax de von Neumann (1928) dice que max_p min_q pᵀAq = min_q max_p pᵀAq. Este **valor** común es lo que el jugador fila puede garantizarse, y un p óptimo resuelve: maximizar v sujeto a Aᵀp ≥ v·1, Σ p_i = 1, p ≥ 0. En piedra, papel o tijera el valor es 0, y la única estrategia óptima es (1/3, 1/3, 1/3) para cada jugador.

### Ejercicio práctico

La capacidad de la máquina B sube de 6 a 7. Predice el nuevo óptimo a partir del dual, y luego compruébalo.

> *Solución:* v = 1/2 predice 9.5. Las restricciones activas son ahora x + y = 4 y x + 3y = 7, así que y = 1.5 y x = 2.5, que rinden 2 × 2.5 + 3 × 1.5 = 9.5. Los otros vértices, (4, 0) y (0, 7/3), rinden 8 y 7, así que la predicción se cumple. El óptimo se ha movido, pero siguen activas las mismas dos restricciones; la predicción solo fallaría cuando pasara a estar activo otro par, aquí cuando la capacidad de B saliera del intervalo de 4 a 12.

---

## 3. Equilibrios de Nash y enumeración de soportes

En un juego bimatricial, el jugador A elige una fila i y el jugador B una columna j; A recibe a_ij y B recibe b_ij. Las estrategias mixtas p y q son vectores de probabilidad, y el pago esperado de A es pᵀAq. Un par (p, q) es un **equilibrio de Nash** cuando ningún jugador gana desviándose por su cuenta. Como un pago es lineal en la propia estrategia, basta con comprobar las desviaciones hacia estrategias puras. Nash (1950) demostró que todo juego finito tiene un equilibrio, posiblemente mixto.

En equilibrio, cada estrategia pura que un jugador usa rinde el mismo pago esperado contra la mezcla del otro, y ninguna estrategia no usada rinde más: es el **principio de indiferencia**. La **enumeración de soportes** adivina qué estrategias usa cada jugador (los soportes), resuelve las ecuaciones lineales de indiferencia y se queda con las soluciones que son vectores de probabilidad y que ninguna estrategia no usada supera. Un juego m × n tiene (2^m − 1)(2^n − 1) pares de soportes. En un juego no degenerado solo soportes del mismo tamaño pueden sostener un equilibrio, y el número de equilibrios es impar, como muestra el algoritmo de Lemke–Howson (1964).

- **Dilema del prisionero**, A = [[3, 0], [5, 1]] y B = Aᵀ. Traicionar domina estrictamente a cooperar para ambos jugadores. Así que (traicionar, traicionar), que vale 1 a cada uno, es el único equilibrio, aunque cooperar daría 3 a cada jugador.
- **Pares o nones**, A = [[1, −1], [−1, 1]] y B = −A. No hay equilibrio puro; la indiferencia da p = q = (1/2, 1/2).
- **La batalla de los sexos**, A = [[3, 0], [0, 2]] y B = [[2, 0], [0, 3]]. Hay dos equilibrios puros, que pagan (3, 2) y (2, 3), y uno mixto. B debe hacer indiferente a A, 3q = 2(1 − q), así que q = 2/5. A debe hacer indiferente a B, 2p = 3(1 − p), así que p = 3/5. Cada jugador espera entonces 6/5, menos que en cualquiera de los equilibrios puros.
- **Piedra, papel o tijera.** El único equilibrio usa las tres estrategias, en (1/3, 1/3, 1/3); ningún soporte de tamaño 1 o 2 sostiene uno.

El **juego ficticio** (Brown, 1951) es una regla de aprendizaje: en cada ronda, cada jugador juega una mejor respuesta a las frecuencias empíricas del juego pasado del otro. Robinson (1951) demostró que en los juegos de suma cero todo punto límite de estas frecuencias es una estrategia de equilibrio, así que convergen cuando el equilibrio es único. Shapley (1964) mostró que en general no tienen por qué hacerlo. En un juego 3 × 3 del tipo que él usó, con A la matriz identidad y B = [[0, 1, 0], [0, 0, 1], [1, 0, 0]], el único equilibrio es uniforme. Aun así, el juego recorre en ciclo seis perfiles puros, en rachas cuyas longitudes crecen geométricamente (§7), y las frecuencias nunca se estabilizan.

### Ejercicio práctico

Encuentra todos los equilibrios de A = [[2, 0], [0, 1]], B = [[1, 0], [0, 2]], y el pago esperado de cada jugador en el mixto.

> *Solución:* Los dos equilibrios puros son (fila 1, columna 1) y (fila 2, columna 2). Para el mixto, la mezcla de B hace indiferente a A: 2q = 1 − q, así que q = 1/3. La mezcla de A hace indiferente a B: p = 2(1 − p), así que p = 2/3. A espera 2q = 2/3 y B espera p = 2/3. Tres equilibrios, un número impar, como en todo juego no degenerado.

---

## 4. El valor de Shapley y el núcleo

Un juego cooperativo da a cada coalición S de los n jugadores un valor v(S), con v(∅) = 0, y un reparto x divide v(N), el valor de la gran coalición. Shapley (1953) mostró que una sola regla cumple cuatro axiomas. Eficiencia: las partes suman v(N). Simetría: jugadores intercambiables reciben lo mismo. Jugador nulo: un jugador que no aporta nada no recibe nada. Aditividad: las partes de una suma de juegos son las sumas de las partes. Esa regla es el **valor de Shapley**:

```
φ_i = Σ_{S ⊆ N∖{i}}  |S|! (n − |S| − 1)! / n!  ·  [v(S ∪ {i}) − v(S)]
```

es decir, la contribución marginal de i promediada sobre los n! órdenes en que pueden llegar los jugadores. El **núcleo** pide estabilidad en lugar de equidad (Gillies, 1959): x está en el núcleo si es eficiente y ninguna coalición puede hacerlo mejor por su cuenta, Σ_{i∈S} x_i ≥ v(S) para todo S. El núcleo puede estar vacío. Cuando no lo está, no tiene por qué contener el valor de Shapley; en un juego convexo lo contiene (Shapley, 1971).

En el **juego de los guantes**, los jugadores 1 y 2 tienen cada uno un guante izquierdo, el jugador 3 un guante derecho, y un par vale 1. El jugador 3 aporta 1 en todos los órdenes salvo los dos en que llega primero, así que φ_3 = 4/6 = 2/3. El jugador 1 solo aporta 1 en el orden (3, 1, 2), así que φ_1 = φ_2 = 1/6. El núcleo exige x_1 + x_3 ≥ 1, x_2 + x_3 ≥ 1 y x_i ≥ 0 para todo i, con x_1 + x_2 + x_3 = 1, lo que fuerza x_1 = x_2 = 0: el núcleo es el único punto (0, 0, 1). El valor de Shapley paga 1/6 a cada guante izquierdo; el núcleo no les paga nada, porque dos guantes izquierdos compiten por un solo guante derecho. En el **juego de mayoría**, donde dos cualesquiera de tres jugadores pueden repartirse 1, el núcleo está vacío: las tres restricciones de pares suman 2(x_1 + x_2 + x_3) ≥ 3, mientras que las partes deben sumar 1. El valor de Shapley es 1/3 para cada uno.

El **índice de Banzhaf** (Banzhaf, 1965) cuenta, para cada jugador, las coaliciones que convierte de perdedoras en ganadoras, en lugar de promediar sobre órdenes. En una votación ponderada con pesos 3, 3, 3, 1 y 1 y una cuota de 10, una coalición ganadora necesita a los tres miembros grandes y a uno pequeño. El valor de Shapley es (0.3, 0.3, 0.3, 0.05, 0.05), y el índice de Banzhaf normalizado es (3/11, 3/11, 3/11, 1/11, 1/11).

### Ejercicio práctico

Dos jugadores, con v({1}) = v({2}) = 0 y v({1, 2}) = 1. Da el valor de Shapley y el núcleo.

> *Solución:* El valor de Shapley es 1/2 para cada uno, por simetría y eficiencia. El núcleo es el conjunto de los (x, 1 − x) con 0 ≤ x ≤ 1, ya que cada jugador solo puede garantizarse 0. El valor de Shapley es su punto medio.

---

## 5. Bandidos y arrepentimiento

Un bandido de K brazos tiene K distribuciones de recompensa con medias desconocidas μ_1, …, μ_K. En cada ronda, el aprendiz tira de un brazo y solo observa la recompensa de ese brazo. El **arrepentimiento** (regret) tras T rondas es el déficit esperado frente a tirar siempre del mejor brazo: R_T = T μ* − E[Σ_t r_t] = Σ_i Δ_i E[N_i(T)], donde Δ_i = μ* − μ_i y N_i(T) cuenta las tiradas del brazo i. Lai y Robbins (1985) mostraron que un aprendiz que funciona bien en todo bandido debe tirar de cada brazo peor del orden de ln T veces, así que el arrepentimiento crece al menos logarítmicamente.

**ε-voraz** tira de un brazo uniformemente al azar con probabilidad ε y, si no, del brazo con la mejor media. Su exploración nunca se detiene. Una vez que sus medias ordenan bien los brazos, cada ronda cuesta ε veces la brecha media de una tirada uniforme. Con medias 1, 2 y 3 y ε = 0.1, eso es 0.1 × (2 + 1 + 0)/3 = 0.1 por ronda, un arrepentimiento que crece linealmente en T. **UCB1** (Auer, Cesa-Bianchi y Fischer, 2002) tira una vez de cada brazo y luego del brazo con el mayor q_i + √(2 ln t / n_i), donde q_i es la media del brazo, n_i su número de tiradas y t el total. Para recompensas en [0, 1] tira de un brazo peor como mucho 8 ln T / Δ_i² + 1 + π²/3 veces en esperanza, un arrepentimiento logarítmico. El **muestreo de Thompson** (Thompson, 1933) saca una media para cada brazo de su distribución a posteriori y tira del brazo con la mejor muestra.

La cota supone recompensas en [0, 1]. El bono √(2 ln t / n_i) no tiene unidad, mientras que q_i tiene la unidad de la recompensa, así que multiplicar todas las recompensas por c cambia las elecciones de UCB1, salvo que el bono también se multiplique por c. Dos brazos que siempre pagan 0.5 y 0.4 lo muestran sin ningún azar. Tras 10,000 rondas, UCB1 ha tirado del brazo peor 877 veces. Si pagan 50 y 40, tira del brazo peor una vez, durante el arranque, y nunca más. Si pagan 0.005 y 0.004, tira del brazo peor 4,918 veces, cerca de la mitad. Una escala grande tampoco es segura. Que el primer pago del mejor brazo sea desafortunado, 30 en lugar de 50, y todos los siguientes 50. UCB1 ya no vuelve a él: una tirada, y luego 9,999 del brazo peor, un arrepentimiento de 10 por ronda. Para salvar una brecha de 10, el bono √(2 ln t) necesita ln t cerca de 50.

### Ejercicio práctico

Para dos brazos con recompensas en [0, 1] y Δ = 0.1, ¿cuántas tiradas del brazo peor permite la cota de UCB1 tras T = 10,000 rondas? Compáralo con las 877 de los brazos deterministas.

> *Solución:* 8 ln(10,000)/0.01 + 1 + π²/3 ≈ 7,372.6. La cota vale para toda distribución en [0, 1], incluidas las peores, así que en este par fácil y sin ruido es holgada por un factor de alrededor de 8.

---

## 6. Penalizaciones: restricciones para una búsqueda que solo conoce cajas

Una búsqueda que solo conoce cotas de caja l ≤ x ≤ u, como muchos algoritmos evolutivos, puede respetar otras restricciones si se trasladan al objetivo. Para una restricción de igualdad h(x) = 0, la **penalización cuadrática** minimiza f(x) + (ρ/2) h(x)²; para g(x) ≤ 0 usa max(0, g(x))². Cuando ρ crece, sus minimizadores se acercan al minimizador con restricciones, y ρ h(x_ρ) se acerca al multiplicador salvo el signo. Para todo ρ finito, sin embargo, violan la restricción siempre que su multiplicador no sea nulo. La **penalización ℓ1** f(x) + ρ |h(x)| es **exacta**: en cuanto ρ supera el módulo del multiplicador, el minimizador con restricciones es un minimizador local de la función penalizada y, para un problema convexo como los de aquí, su minimizador global (Nocedal y Wright, cap. 17). El precio es una esquina en la solución, donde los métodos de gradiente tienen dificultades.

Minimicemos x² + y² sujeto a x + y = 2. La solución es x = y = 1, con multiplicador λ* = 2, ya que la estacionariedad se lee 2x = λ. Con la penalización cuadrática, la simetría da x = y = t con 2t + ρ(2t − 2) = 0, así que t = ρ/(1 + ρ). ρ = 10 da t ≈ 0.909091 y una violación de 2/11 ≈ 0.181818. ρ = 100 da 0.990099 y 0.019802. La estimación ρ(2 − 2t) = 2ρ/(1 + ρ), es decir 1.818182 y luego 1.980198, se acerca a λ* = 2. Con la penalización ℓ1, minimicemos 2t² + ρ|2t − 2|. Por debajo de t = 1 la derivada es 4t − 2ρ, así que el minimizador es t = min(ρ/2, 1). Es exacto a partir de ρ = 2 = λ*, e infactible por debajo.

Recortar cada coordenada a su intervalo, como hace una búsqueda acotada por una caja, no es una penalización sino una proyección. Trata una caja exactamente, y nada más.

### Ejercicio práctico

El problema de presupuesto del §1, escrito para un minimizador que solo conoce la caja [0, 10]², pasa a ser: minimizar −ln(1 + x) − 2 ln(1 + y) + ρ max(0, x + y − 10). ¿Qué pesos ρ hacen exacta esta penalización ℓ1?

> *Solución:* Todo ρ mayor que λ* = 1/4. Por debajo, una unidad más de presupuesto por encima de 10 rinde más, en el margen 1/(1 + x) = 1/4, de lo que cuesta la penalización, así que el minimizador gasta de más.

---

## 7. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus tests. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea a Python de `nash.rs` y `cooperative.rs` en `crates/ix-game`, y de `UCB1` y la elección voraz de `EpsilonGreedy` en `crates/ix-rl`. Ninguno de ellos saca un número aleatorio. La transcripción reproduce las aserciones de los tests deterministas que cita esta sección. No reproduce las ejecuciones que sacan números del `StdRng` con semilla de IX, cuyo flujo, como explica el §6 de MAT-009, no es una especificación portable; para ellas, el §8 solo enuncia predicciones cualitativas.

**Enumeración de soportes: dos tipos de soporte entre muchos.** [`support_enumeration`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L152) recorre todos los pares de soportes, pero [`solve_support`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L177) solo resuelve dos tipos: un par de estrategias puras, y el soporte completo de un juego 2 × 2.

```rust
        // For 2x2 mixed strategy: solve indifference conditions
        if m == 2 && n == 2 && support_a.len() == 2 && support_b.len() == 2 {
            return self.solve_2x2_mixed();
        }

        None // General case would need linear programming
```

La documentación del módulo anuncia [Lemke–Howson](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L3), que el archivo no contiene, y el espacio de trabajo no tiene ningún solucionador de programación lineal. En los juegos 2 × 2 del §3 la transcripción encuentra todos los equilibrios: 1 para pares o nones, cuyo [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L365) solo comprueba que un equilibrio cercano a (1/2, 1/2) está entre los encontrados, no cuántos hay, y 3 para la batalla de los sexos, cuyo test solo afirma [al menos 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L398). Piedra, papel o tijera y el juego de Shapley son 3 × 3 y solo tienen un equilibrio mixto, así que la función devuelve una lista vacía. La herramienta MCP [`ix_game_nash`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1406) responde entonces `count: 0` para juegos que, por el teorema de Nash, tienen un equilibrio, y nada en la respuesta dice que la búsqueda fue parcial. La guía de IX enuncia el límite con claridad en su [segundo error común](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L175), pero su [cuarto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L179) dice que la enumeración de soportes los encuentra todos.

**Juego ficticio: una primera jugada fantasma, y los empates a la última estrategia.** [`fictitious_play`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L247) empieza cada recuento [con una jugada de la estrategia 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L253). Entre mejores respuestas empatadas toma la última, porque `max_by` de Rust [devuelve el último de los máximos iguales](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L262). Su test juega el dilema del prisionero durante 1,000 rondas y afirma una frecuencia de traición [mayor que 0.9](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L413); la transcripción traiciona en todas las rondas, así que la única cooperación en 1,001 recuentos es la fantasma. En pares o nones, las frecuencias de los dos jugadores tras 100, 1,000, 10,000 y 100,000 rondas están a menos de 0.054455, 0.016484, 0.006649 y 0.001605 de 1/2, como predice el teorema de Robinson. En el juego de Shapley nunca se estabilizan. Las rachas de perfiles idénticos tienen longitudes 1, 2, 3, 6, 9, 13, 20, 30, 44, 65 y así sucesivamente, y el cociente de cada una entre la anterior tiende a unos 1.466. Tras 100,000 rondas, las frecuencias de A son (0.3822, 0.4399, 0.1779), lejos de (1/3, 1/3, 1/3). La función devuelve las frecuencias sin decir si convergieron, aunque su documentación advierte que [puede no converger en todos los juegos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L246). La guía de IX dice que el juego ficticio [converge con garantía](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L177) en los juegos de suma cero y en los juegos con un equilibrio único. El juego de Shapley, que el mismo error común cita a continuación, tiene un equilibrio único y cicla.

**Valor de Shapley: exacto, exponencial y fuera del núcleo.** [`shapley_value`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L53) suma la fórmula del §4 sobre las 2^(n−1) coaliciones sin cada jugador, con factoriales en [`u64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L168). El [test del juego de los guantes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L194) solo afirma que el guante derecho recibe [más que un guante izquierdo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L206) y que las partes suman 1. La transcripción da (1/6, 1/6, 2/3), que [`is_in_core`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L82) rechaza, mientras que acepta (0, 0, 1). Para el juego del test del núcleo, con 7, 5 y 3 para los pares y 10 para los tres, el valor de Shapley (13/3, 10/3, 7/3) está en el núcleo. La documentación del módulo menciona el [nucleolo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L1), que el archivo no implementa. Los contratos del crate dicen que no se llame a la función [más allá de unos 20 jugadores](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/CONTRACTS.md#L39), por una caché de valores de coaliciones que la función no reserva. El límite es real por otra razón: 21! vale unas 2.77 veces 2^64, así que a partir de 21 jugadores el factorial de n desborda `u64`. `product` de Rust entra entonces en pánico cuando las comprobaciones de desbordamiento están activas, como en una compilación de depuración, y da la vuelta módulo 2^64 en caso contrario.

**Bandidos: los empates al último brazo, y un bono sin unidad.** [`EpsilonGreedy::select_arm`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L26) elige la mejor media [con `max_by`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L33), así que su primera elección voraz, con todas las medias en 0, es el último brazo; los contratos del crate prometen [el primero](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L8). Lo mismo vale para la acción voraz del [Q-learning](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/q_learning.rs#L55), cuyo contrato también promete [el índice más bajo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L14). Vale también para [`first_price_auction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/auction.rs#L29), de la que su contrato dice que [desempata a favor del primer postor](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/CONTRACTS.md#L12). [`second_price_auction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/auction.rs#L46) ordena de forma estable y sí da un empate al primer postor. En el test de ε-voraz el mejor brazo es [el último](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L143), el que favorece el desempate. [`UCB1::select_arm`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L62) suma el bono del §5 sin parámetro de escala:

```rust
    pub fn select_arm(&self) -> usize {
        // Play each arm at least once
        for (i, &c) in self.counts.iter().enumerate() {
            if c == 0 {
                return i;
            }
        }

        let total = self.total_count as f64;
        self.q_values
            .iter()
            .enumerate()
            .map(|(i, &q)| {
                let bonus = (2.0 * total.ln() / self.counts[i] as f64).sqrt();
                (i, q + bonus)
            })
            .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
            .unwrap()
            .0
    }
```

Los brazos deterministas del §5 son ejecuciones de una transcripción de esta función. Su test solo comprueba que [cada uno de 5 brazos se juega una vez primero](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L164), y ningún test mide el arrepentimiento. El [muestreo de Thompson](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L91) fija la varianza de cada brazo en [1/n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L131). Es la varianza a posteriori de la media para recompensas de varianza 1 con una distribución a priori plana, y los contratos la llaman [una simplificación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L13). La herramienta MCP [`ix_bandit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2333) saca las recompensas con [desviación típica 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2355) de un generador [con semilla 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2342), e informa de las tiradas y la recompensa total, no del arrepentimiento.

**Evolución: solo cajas.** El algoritmo genético y la evolución diferencial toman un solo intervalo para todas las coordenadas ([`with_bounds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/genetic.rs#L57)) y [recortan](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/genetic.rs#L120) cada hijo a ese intervalo. No hay ninguna otra restricción ni ayuda para penalizaciones, así que las penalizaciones del §6 las tiene que escribir quien llama. El `mutation_rate` del algoritmo genético no es una tasa. Es la [desviación típica de un paso gaussiano](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/traits.rs#L56), y cada gen da ese paso [con probabilidad 0.3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/traits.rs#L58). El [`pick_three`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/differential.rs#L132) de la evolución diferencial saca tres índices distintos aparte del actual, y [reintenta hasta tenerlos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/differential.rs#L134). Con uno, dos o tres individuos no termina nunca. La herramienta MCP `ix_evolution` pasa el [`population_size`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2417) de quien llama sin comprobarlo.

Corregir cualquiera de estas cosas corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

`ix_game_nash` responde `count: 0` para piedra, papel o tijera. ¿Cuál es el equilibrio, y cómo podrías aproximarlo con IX tal como está?

> *Solución:* (1/3, 1/3, 1/3) para cada jugador, la estrategia minimax del §2. IX no sabe calcularlo, pero el juego es de suma cero, así que `fictitious_play` se acerca a él: tras 100,000 rondas cada frecuencia está a menos de 0.001077 de 1/3. `is_nash_equilibrium` confirma el propio perfil uniforme, ya que ninguna desviación gana nada.

---

## 8. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Enumeración de soportes.** Ejecutar `support_enumeration` en pares o nones, la batalla de los sexos, piedra, papel o tijera y el juego de Shapley. Predicción: 1, 3, 0 y 0 equilibrios; para la batalla de los sexos, el mixto en (0.6, 0.4) y (0.4, 0.6).
2. **Juego ficticio.** Ejecutar `fictitious_play` en pares o nones y en el juego de Shapley durante 100, 1,000, 10,000 y 100,000 rondas. Predicción: en pares o nones, la frecuencia de la primera estrategia de A 0.554455, 0.483516, 0.499550 y 0.500625; en el juego de Shapley, las frecuencias de A tras 100,000 rondas (0.3822, 0.4399, 0.1779).
3. **Valor de Shapley y núcleo.** Ejecutar `shapley_value` e `is_in_core` en el juego de los guantes y en el juego del test del núcleo, y `shapley_value` y `banzhaf_index` en la votación ponderada del §4. Predicción: los valores del §4 y del §7, (1/6, 1/6, 2/3) rechazado y (0, 0, 1) aceptado, (13/3, 10/3, 7/3) aceptado.
4. **Empates.** Llamar a `select_arm` en un `EpsilonGreedy` nuevo con tres brazos y ε = 0, y ejecutar las dos subastas con dos pujas iguales. Predicción: el brazo 2; la subasta de primer precio va al segundo postor, la de segundo precio al primero.
5. **UCB1 y la unidad de la recompensa.** Ejecutar `UCB1` durante 10,000 rondas en los brazos deterministas del §5, en las tres escalas y con el primer pago desafortunado. Predicción: 877, 1 y 4,918 tiradas del brazo peor; con el primer pago desafortunado en la escala 100, 1 tirada del mejor brazo.
6. **Arrepentimiento con brazos ruidosos.** Ejecutar `EpsilonGreedy` con ε = 0.1 y `UCB1` en tres brazos con medias 1, 2 y 3 y ruido gaussiano de desviación típica 1, como hace `ix_bandit`, durante 1,000, 10,000 y 100,000 rondas sobre 20 semillas, y calcular el arrepentimiento a partir de las tiradas. Predicción, solo cualitativa, ya que esta lección no reproduce el generador de IX: el arrepentimiento por ronda de ε-voraz se queda cerca de 0.1, mientras que el de UCB1 baja a medida que T crece.
7. **Evolución diferencial con tres individuos.** Ejecutar `DifferentialEvolution` con una población de 4, y luego de 3, en un hilo aparte, esperando su resultado como mucho 10 segundos. Predicción: la primera termina, la segunda no.

### Ejercicio práctico

El paso 6 compara el arrepentimiento con un único modelo de ruido fijo. ¿Cómo harías que la comparación fuera justa entre los dos algoritmos?

> *Solución:* Sacar las recompensas de antemano, un flujo por brazo, para que la k-ésima tirada de un brazo devuelva la misma recompensa sea cual sea el algoritmo que tire de él. Calcular el arrepentimiento a partir de las tiradas y las medias verdaderas, no de las recompensas recibidas, e informar de su dispersión sobre las semillas, no de una sola ejecución.

---

## 9. Errores comunes

- **Leer una lista de equilibrios vacía como «no hay equilibrio».** Todo juego finito tiene uno; una lista vacía salida de una enumeración parcial solo dice que la búsqueda no lo encontró.
- **Confiar en que el juego ficticio converja.** En los juegos de suma cero sus frecuencias se acercan a estrategias de equilibrio; en general no tienen por qué, ni siquiera con un equilibrio único. Comprueba las frecuencias frente a las mejores respuestas.
- **Tomar el valor de Shapley por un reparto estable.** La equidad y la estabilidad son axiomas distintos; comprueba el núcleo por separado.
- **Usar un multiplicador lejos del margen.** Es una derivada; un cambio grande en un recurso exige volver a resolver el problema.
- **Tomar la respuesta de una penalización cuadrática por factible.** Salvo que el multiplicador sea nulo, viola la restricción para todo peso finito; una penalización ℓ1 con un peso mayor que el multiplicador, no.
- **Llamar a un recorte tratamiento de restricciones.** Trata una caja, y nada más.
- **Comparar algoritmos de bandidos por la recompensa total con una sola semilla.** El arrepentimiento frente al mejor brazo es la medida, y una semilla es una sola muestra.
- **Dar a UCB1 recompensas fuera de [0, 1].** Reescala las recompensas, o el bono, al rango de la recompensa.
- **Suponer que un empate va al primer índice.** `max_by` de Rust devuelve el último de los máximos iguales y `min_by` el primero; una ordenación estable conserva el orden de entrada.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Condiciones KKT** | Estacionariedad, factibilidad, multiplicadores no negativos y holgura complementaria; necesarias y suficientes para un problema cóncavo bajo la condición de Slater |
| **Precio sombra** | El multiplicador de una restricción: el valor marginal de una unidad más de su recurso |
| **Dualidad de la programación lineal** | El dual acota el primal, y en un óptimo ambos tienen el mismo valor |
| **Equilibrio de Nash** | Un perfil de estrategias del que ningún jugador gana desviándose por su cuenta |
| **Enumeración de soportes** | Adivinar las estrategias que usa cada jugador y resolver las ecuaciones de indiferencia |
| **Juego ficticio** | Cada jugador juega una mejor respuesta a las frecuencias empíricas del juego pasado del otro |
| **Valor de Shapley** | La contribución marginal media sobre todos los órdenes de llegada; la única regla con eficiencia, simetría, jugador nulo y aditividad |
| **Núcleo** | Los repartos eficientes que ninguna coalición puede mejorar por su cuenta |
| **Arrepentimiento** | El déficit esperado frente a tirar siempre del mejor brazo |
| **UCB1** | Tirar del brazo con la mayor media más √(2 ln t / n_i), tras una tirada de cada uno |
| **Penalización cuadrática** | f + (ρ/2) h²: infactible para todo ρ finito cuando el multiplicador no es nulo, con ρ h acercándose al multiplicador |
| **Penalización exacta** | f + ρ \|h\|: exacta en cuanto ρ supera el módulo del multiplicador |

---

## Autoevaluación

**1. `support_enumeration` devuelve una lista vacía para un juego 3 × 3. ¿Qué sabes?**
> Nada sobre la existencia: por el teorema de Nash, el juego tiene un equilibrio. IX solo resuelve soportes puros y el soporte completo de un juego 2 × 2, así que un equilibrio que mezcla en un juego 3 × 3 queda fuera de su alcance. Piedra, papel o tijera es un ejemplo, con su único equilibrio en (1/3, 1/3, 1/3).

**2. En el juego de los guantes, ¿por qué el valor de Shapley no está en el núcleo?**
> Ambos son eficientes, pero el núcleo exige además que cada coalición reciba al menos su valor. El valor de Shapley da a los jugadores 1 y 3 juntos 1/6 + 2/3 = 5/6, menos que el 1 que pueden obtener solos. El único reparto que satisface a todas las coaliciones es (0, 0, 1).

**3. Un servicio da a UCB1 recompensas medidas en milisegundos ahorrados, del orden de cientos. ¿Qué falla?**
> El bono √(2 ln t / n_i) sigue siendo del orden de 1 mientras que las medias difieren en decenas. Tras el arranque UCB1 es voraz: un solo primer resultado desafortunado puede excluir al mejor brazo para siempre. Reescala las recompensas a [0, 1], o multiplica el bono por el rango.

**4. Un algoritmo genético con cotas de caja debe respetar x + y ≤ 10. ¿Qué puedes hacer?**
> Añadir una penalización al objetivo. La penalización ℓ1 ρ max(0, x + y − 10) es exacta en cuanto ρ supera el multiplicador de la restricción. Una penalización cuadrática solo es factible aproximadamente. El recorte trata la caja y no hace nada por la suma.

**Criterio de aprobación:** Escribir y resolver las condiciones KKT de una asignación pequeña y leer sus multiplicadores como precios; resolver un programa lineal de dos variables y su dual; encontrar los equilibrios de un juego bimatricial pequeño y decir cuándo converge el juego ficticio; calcular un valor de Shapley y comprobar el núcleo; definir el arrepentimiento y decir lo que supone la cota de UCB1; elegir un peso de penalización exacta; y decir cuáles de las salidas de IX fijan sus tests.

---

## Base de investigación

- W. Karush, *Minima of Functions of Several Variables with Inequalities as Side Constraints*, tesis de M.Sc., Universidad de Chicago, 1939, y H. W. Kuhn y A. W. Tucker, «Nonlinear programming», *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability*, 1951: las condiciones KKT
- S. Boyd y L. Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004, capítulo 5: dualidad, condición de Slater y precios sombra
- G. B. Dantzig, *Linear Programming and Extensions*, Princeton University Press, 1963: el método símplex y la dualidad de la programación lineal
- J. von Neumann, «Zur Theorie der Gesellschaftsspiele», *Mathematische Annalen* 100, 1928: el teorema minimax
- J. F. Nash, «Equilibrium points in n-person games», *Proceedings of the National Academy of Sciences* 36, 1950: todo juego finito tiene un equilibrio
- C. E. Lemke y J. T. Howson, «Equilibrium points of bimatrix games», *Journal of the Society for Industrial and Applied Mathematics* 12, 1964: el algoritmo de Lemke–Howson y el número impar de equilibrios
- G. W. Brown, «Iterative solution of games by fictitious play», en *Activity Analysis of Production and Allocation*, Wiley, 1951, y J. Robinson, «An iterative method of solving a game», *Annals of Mathematics* 54, 1951: el juego ficticio, y su convergencia en los juegos de suma cero
- L. S. Shapley, «Some topics in two-person games», en *Advances in Game Theory*, Annals of Mathematics Studies 52, 1964: un juego en el que el juego ficticio cicla
- L. S. Shapley, «A value for n-person games», en *Contributions to the Theory of Games II*, Annals of Mathematics Studies 28, 1953: el valor de Shapley
- D. B. Gillies, «Solutions to general non-zero-sum games», en *Contributions to the Theory of Games IV*, Annals of Mathematics Studies 40, 1959: el núcleo
- L. S. Shapley, «Cores of convex games», *International Journal of Game Theory* 1, 1971: el valor de Shapley de un juego convexo está en su núcleo
- J. F. Banzhaf III, «Weighted voting doesn't work: a mathematical analysis», *Rutgers Law Review* 19, 1965: el índice de Banzhaf
- T. L. Lai y H. Robbins, «Asymptotically efficient adaptive allocation rules», *Advances in Applied Mathematics* 6, 1985: la cota inferior logarítmica del arrepentimiento
- P. Auer, N. Cesa-Bianchi y P. Fischer, «Finite-time analysis of the multiarmed bandit problem», *Machine Learning* 47, 2002: UCB1 y su cota
- W. R. Thompson, «On the likelihood that one unknown probability exceeds another in view of the evidence of two samples», *Biometrika* 25, 1933: el muestreo de Thompson
- T. Lattimore y C. Szepesvári, *Bandit Algorithms*, Cambridge University Press, 2020: arrepentimiento, ε-voraz y UCB
- J. Nocedal y S. J. Wright, *Numerical Optimization*, 2.ª edición, Springer, 2006, capítulo 17: métodos de penalización cuadrática y exacta
- N. Nisan, T. Roughgarden, É. Tardos y V. V. Vazirani (eds.), *Algorithmic Game Theory*, Cambridge University Press, 2007: la enumeración de soportes y el cálculo de equilibrios
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §7 enlaza a su línea
- Experimento: propuesto en el §8, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
