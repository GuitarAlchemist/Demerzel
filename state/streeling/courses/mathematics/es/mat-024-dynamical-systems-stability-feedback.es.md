---
module_id: mat-024-dynamical-systems-stability-feedback
department: mathematics
course: Sistemas dinámicos, estabilidad y realimentación
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-006-svd-low-rank-approximation]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Sistemas dinámicos, estabilidad y realimentación — Lo que pueden decir una derivada, un exponente y un rango

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Encontrar los puntos fijos y los ciclos de una aplicación, decidir su estabilidad a partir de un multiplicador, y decir cuándo la linealización no decide nada
- Calcular un exponente de Lyapunov como el promedio de log|f′| a lo largo de una órbita, y decir qué dice y qué no dice su signo sobre el atractor
- Localizar las bifurcaciones de duplicación de periodo, estimar a partir de ellas la δ de Feigenbaum, y explicar por qué un barrido con una tolerancia fija las sitúa mal
- Estabilizar un punto fijo inestable mediante el control OGY, y decir cuándo el controlador actúa linealmente, se satura o no hace falta en absoluto
- Deducir el filtro de Kalman escalar y su régimen estacionario, y explicar por qué la forma de Joseph mantiene honesta una covarianza donde la forma corta no lo hace
- Decidir la controlabilidad y la observabilidad mediante el criterio del rango de Kalman, y leer el margen y la tolerancia de los que depende un rango numérico
- Seguir lo que calculan los crates `ix-chaos` e `ix-signal` de IX, cuáles de sus salidas fija un test, y qué dejan fuera

---

## 1. Puntos fijos y linealización

Un sistema dinámico discreto itera una aplicación: x_(k+1) = f(x_k). Un **punto fijo** x* cumple f(x*) = x*. Escribamos x_k = x* + e_k; un desarrollo de Taylor da e_(k+1) = f′(x*) e_k + O(e_k²), así que cerca de x* el error se multiplica en cada paso por el **multiplicador** f′(x*). Si |f′(x*)| < 1, el punto fijo es asintóticamente estable: los errores pequeños se reducen aproximadamente en ese factor por paso, y cuando el multiplicador es negativo alternan de signo. Si |f′(x*)| > 1, es inestable. Si |f′(x*)| = 1, la linealización no decide nada, y son los términos de orden superior los que zanjan la cuestión. Si f′(x*) = 0, el punto fijo es **superestable**: el error se eleva al cuadrado en cada paso.

La **aplicación logística** f(x) = r x (1 − x), con 0 ≤ r ≤ 4, lleva [0, 1] en sí mismo. Para r > 1 tiene un punto fijo x* = 1 − 1/r además de 0, y como f′(x) = r(1 − 2x), el multiplicador allí es f′(x*) = 2 − r. En r = 2.5, x* = 0.6 y el multiplicador es −0.5: los errores se reducen a la mitad y alternan. En r = 2, x* = 1/2 es superestable. En r = 3.2 el multiplicador es −1.2, y x* repele.

Un **ciclo** de periodo p es un punto fijo de la p-ésima iterada f^p, y por la regla de la cadena su multiplicador es el producto de f′ a lo largo del ciclo. Para la aplicación logística, el ciclo de periodo 2 existe para r > 3, y su multiplicador resulta ser 4 + 2r − r². Es estable mientras |4 + 2r − r²| < 1, es decir, para 3 < r < 1 + √6 ≈ 3.449490. Es superestable en r = 1 + √5 ≈ 3.236068, donde el ciclo pasa por x = 1/2. Nace en r = 3, donde el multiplicador del punto fijo pasa por −1, y pierde la estabilidad donde su propio multiplicador alcanza −1.

En n dimensiones, x_(k+1) = F(x_k) se linealiza con la jacobiana J de F en el punto fijo, y el punto fijo es estable cuando todos los valores propios de J tienen módulo menor que 1, es decir, cuando el **radio espectral** ρ(J) es menor que 1 (MAT-005). Para un sistema lineal x_(k+1) = A x_k, ρ(A) < 1 es necesario y suficiente para que x_k → 0 desde cualquier punto de partida. No impide un crecimiento transitorio. A = [[0.5, 10], [0, 0.5]] tiene ρ(A) = 0.5, pero desde x_0 = (0, 1) la primera componente de x_k es 10k · 0.5^(k−1): 10 en el primer y el segundo paso, 7.5 en el tercero, y menor que 1 solo a partir del octavo. Los valores propios fijan el largo plazo; para una A no normal, la norma, aquí de alrededor de 10.02, acota el corto plazo. CYB-002 describe con palabras la amortiguación de las oscilaciones entre repositorios; el multiplicador es su forma cuantitativa.

### Ejercicio práctico

¿En qué r pierde la estabilidad el punto fijo x* = 1 − 1/r de la aplicación logística?

> *Solución:* El multiplicador es f′(x*) = 2 − r, y |2 − r| < 1 se cumple para 1 < r < 3. En r = 3 el multiplicador alcanza −1 y nace el ciclo de periodo 2. En r = 3 mismo la linealización no decide nada: la órbita sigue acercándose a x*, pero tan despacio que el exponente del §2, promediado sobre 10,000 pasos, sale −0.000359.

---

## 2. Exponentes de Lyapunov

Dos órbitas de una aplicación unidimensional que empiezan a una distancia δ_0 están, tras n pasos, separadas por aproximadamente |δ_0| veces el producto de los |f′(x_i)| a lo largo de la órbita. El **exponente de Lyapunov** es la tasa media de crecimiento por paso:

```
λ = lim (1/n) Σ_{i<n} ln|f′(x_i)|
```

Si λ < 0, las órbitas cercanas convergen: la órbita es atraída por un punto fijo o un ciclo estable. Si λ > 0, las órbitas cercanas se separan exponencialmente sin dejar de estar acotadas, lo que es la firma del caos. λ = 0 marca un comportamiento marginal, como un punto de bifurcación o un movimiento cuasiperiódico. En un punto fijo estable, los términos ln|f′(x_i)| tienden a ln|f′(x*)|, y su promedio también, así que λ = ln|f′(x*)|. En un ciclo estable de periodo p, λ es ln|multiplicador| dividido por p. Si la órbita pasa exactamente por un punto donde f′ = 0, el logaritmo es −∞, y λ también.

Para la aplicación logística, partiendo de x_0 = 0.1, descartando 1,000 pasos y promediando los 10,000 siguientes:

| r | 2.5 | 2.9 | 3.0 | 3.2 | 3.5 | 3.7 | 3.8 | 3.83 | 4.0 |
|---|---|---|---|---|---|---|---|---|---|
| λ | −0.693147 | −0.105361 | −0.000359 | −0.916291 | −0.872507 | 0.350235 | 0.428314 | −0.369511 | 0.693135 |
| Atractor | punto fijo | punto fijo | punto fijo, marginal | ciclo de periodo 2 | ciclo de periodo 4 | caótico | caótico | ciclo de periodo 3 | caótico |

La teoría se confirma. En r = 2.5, λ = ln 0.5 = −0.693147, y en r = 2.9, λ = ln 0.9 = −0.105361. En el ciclo de periodo 2 en r = 3.2, el multiplicador es 4 + 6.4 − 10.24 = 0.16, y λ = (1/2) ln 0.16 = ln 0.4 = −0.916291. En r = 4 el valor exacto es ln 2 = 0.693147, y la ejecución queda a 0.000012 de él. El valor r = 3.83 está en la ventana de periodo 3 que se abre en 1 + √8 ≈ 3.828427, dentro del rango caótico: un exponente negativo allí no es un error. En r = 2 y r = 1 + √5 la órbita cae en x = 1/2 y λ = −∞.

El signo dice si las órbitas cercanas convergen, no hacia qué convergen: un punto fijo, un ciclo de periodo 2 y un ciclo de periodo 3 dan todos λ < 0. Para distinguirlos, se cuenta el periodo (§3).

Para un sistema en n dimensiones hay n exponentes. Benettin y sus colegas los calculan haciendo evolucionar n vectores tangentes con la jacobiana a lo largo de la órbita, reortonormalizándolos mediante una descomposición QR en cada paso, y promediando los logaritmos de la diagonal de R. Para un flujo, que hay que integrar en el tiempo, el esquema de integración de los vectores tangentes entra en el resultado (§7).

### Ejercicio práctico

Calcula λ en r = 2.9 sin iterar, y explica por qué el mismo razonamiento da λ = (1/2) ln|4 + 2r − r²| en el ciclo de periodo 2.

> *Solución:* La órbita converge a x* = 1 − 1/2.9, donde f′(x*) = 2 − 2.9 = −0.9, así que los términos del promedio tienden a ln 0.9 y λ = ln 0.9 = −0.105361. En el ciclo de periodo 2, los términos alternan entre ln|f′(p)| y ln|f′(q)|, cuya suma es el logaritmo del multiplicador |f′(p) f′(q)| = |4 + 2r − r²|, así que cada paso aporta en promedio la mitad.

---

## 3. Duplicación de periodo y constante de Feigenbaum

Cuando r supera r_1 = 3, el punto fijo cede el paso a un ciclo estable de periodo 2, que cede el paso en r_2 = 1 + √6 a un ciclo estable de periodo 4, luego de periodo 8, y así sucesivamente: en r_k el multiplicador del ciclo de periodo 2^(k−1) pasa por −1. Resolver esa condición por el método de Newton, con 40 cifras significativas, da:

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| r_k | 3 | 3.449489743 | 3.54409036 | 3.564407266 | 3.56875942 | 3.56969161 |

Las distancias se reducen geométricamente. Los cocientes δ_k = (r_(k+1) − r_k) / (r_(k+2) − r_(k+1)) son 4.7514, 4.6563, 4.6682 y 4.6687, y convergen a la **constante de Feigenbaum** δ = 4.669201…, la misma para toda aplicación suave de una sola joroba con un máximo cuadrático (Feigenbaum, 1978). La cascada se acumula en r_∞ ≈ 3.569946, valor que da la extrapolación de las distancias con δ. Más allá de r_∞ el caos alterna con ventanas periódicas, como la ventana de periodo 3 del §2.

Encontrar estos puntos a partir de órbitas es más difícil de lo que parece. Un test numérico de periodo itera más allá de un transitorio y devuelve el primer p para el que x_(k+p) vuelve a quedar dentro de una tolerancia de x_k. Cerca de r_k, el multiplicador del ciclo es cercano a −1, así que la órbita se acerca al ciclo despacio, y tras un transitorio fijo sigue demasiado lejos para una tolerancia fija. Un barrido sobre r ve por tanto una duplicación donde la convergencia resulta pasar el test, lo que puede ocurrir antes o después del verdadero r_k (§7).

### Ejercicio práctico

Predice r_6 a partir de r_3, r_4 y r_5 con δ ≈ 4.669, y compáralo con la tabla.

> *Solución:* r_6 ≈ r_5 + (r_5 − r_4)/4.669 = 3.56875942 + 0.00435215/4.669 ≈ 3.569692. La tabla da 3.56969161: la ley geométrica ya se cumple con una precisión de alrededor de una parte en diez millones de r.

---

## 4. Controlar el caos: OGY y Pyragas

Un atractor caótico contiene infinitas órbitas periódicas inestables, entre ellas el punto fijo x*. Ott, Grebogi y Yorke (1990) propusieron estabilizar una de ellas con pequeños cambios de un parámetro. Linealicemos a la vez en el estado y en el parámetro: x_(k+1) − x* ≈ f_x (x_k − x*) + f_r (r_k − r_0), donde f_x y f_r son las derivadas parciales en (x*, r_0). La perturbación

```
δr_k = −(f_x / f_r) (x_k − x*)
```

cancela el término lineal, así que la siguiente desviación es de segundo orden. Como la perturbación debe seguir siendo pequeña, se recorta a |δr| ≤ δr_max, y el controlador solo actúa linealmente dentro de la ventana |x − x*| ≤ δr_max |f_r| / |f_x|. Fuera de la ventana se satura, y es la propia órbita caótica la que acaba llevando el estado a la ventana.

Para la aplicación logística en r_0 = 3.8: x* = 0.736842, f_x = 2 − r_0 = −1.8, f_r = x*(1 − x*) = 0.193906, y con δr_max = 0.1 la ventana tiene una semianchura de 0.010773. Partiendo de x_0 = 0.5 con control desde el paso 50, la perturbación se satura en los pasos 50 a 55. En el paso 56 la desviación es 1.0407e-2, dentro de la ventana, y las siguientes son 8.7741e-4, 6.3042e-6, 3.2578e-10 y 2.2204e-16. Cada una es aproximadamente 8.2 veces el cuadrado de la anterior, y el cociente tiende a 8.1971: una vez cancelado el término lineal, lo que queda son los términos cuadráticos −r_0 e² + (1 − 2x*) e δr.

Pyragas (1992) propuso para los flujos un control que no necesita modelo: añadir K (x(t − τ) − x(t)) a la dinámica, donde τ es el periodo de la órbita que se quiere estabilizar. Sobre esa órbita el término se anula, así que el control no cuesta nada una vez que ha tenido éxito; τ debe coincidir con el periodo.

### Ejercicio práctico

Con δr_max = 0.05 en lugar de 0.1, ¿cuál es la semianchura de la ventana, y qué cambia?

> *Solución:* 0.05 × 0.193906 / 1.8 ≈ 0.005386, la mitad de ancha. La órbita caótica entra con menos frecuencia en una ventana más estrecha, así que la espera antes de la captura es en promedio más larga. Una vez que la órbita está dentro, la convergencia es la misma, ya que el término lineal se cancela sea cual sea δr_max.

---

## 5. El filtro de Kalman como estimación lineal óptima

Un modelo lineal tiene un estado oculto x_k = F x_(k−1) + w_k, observado como z_k = H x_k + v_k, con ruidos independientes w ~ N(0, Q) y v ~ N(0, R). El **filtro de Kalman** alterna dos pasos:

```
predict:  x⁻ = F x            P⁻ = F P Fᵀ + Q
update:   S = H P⁻ Hᵀ + R     K = P⁻ Hᵀ S⁻¹
          x = x⁻ + K (z − H x⁻)
          P = (I − K H) P⁻
```

La ganancia K minimiza la varianza del error a posteriori entre todas las actualizaciones lineales, y con ruido gaussiano la estimación es la media condicional del estado dadas las mediciones (Kalman, 1960).

En el caso escalar F = H = 1, una constante medida con ruido, tomemos Q = 0.01 y R = 1. En régimen estacionario P⁻ = P + Q y P = P⁻ R / (P⁻ + R), así que P⁻² − Q P⁻ − Q R = 0 y P⁻ = (Q + √(Q² + 4QR)) / 2 = 0.105125. La ganancia estacionaria es K = P⁻ / (P⁻ + R) = 0.095125, y la varianza a posteriori es P = K R = 0.095125. Cada nueva medición recibe entonces un peso de 0.095, un olvido exponencial sobre unas 1/K ≈ 10.5 mediciones. Partiendo de x = 0 con P = 1, las mediciones 5.2, 4.8, 5.1, 4.9, 5.0, 5.3, 4.7, 5.1, 4.9 y 5.0, cuya media es 5.0, dan las estimaciones 2.6129, 3.3540, 3.8055, 4.0373, 4.2120, 4.3869, 4.4325, 4.5225, 4.5703 y 4.6219, mientras la ganancia baja de 0.5025 a 0.1201. Tras diez mediciones, la estimación sigue a 0.3781 de 5: la previa x = 0 todavía pesa.

La actualización P = (I − KH) P⁻ solo es correcta para la ganancia óptima. La **forma de Joseph** P = (I − KH) P⁻ (I − KH)ᵀ + K R Kᵀ vale para cualquier ganancia y se mantiene simétrica y semidefinida positiva en coma flotante. Con P⁻ = 1 y R = 1, la ganancia óptima 0.5 da P = 0.5 de ambas maneras. Con una ganancia de 0.8, impuesta o degradada por el redondeo, la verdadera varianza a posteriori es 0.2² × 1 + 0.8² × 1 = 0.68, pero la forma corta da 0.2: subestima la incertidumbre más de tres veces.

### Ejercicio práctico

Con Q = 0.04 y R = 1, halla P⁻ y K en régimen estacionario. ¿Sigue ahora el filtro los cambios más rápido o más despacio?

> *Solución:* P⁻ = (0.04 + √(0.0016 + 0.16)) / 2 ≈ 0.220998, y K = 0.220998 / 1.220998 ≈ 0.180998. La ganancia es casi el doble: el filtro confía menos en el modelo, sigue los cambios más rápido, y deja pasar más ruido de medición a su estimación.

---

## 6. Controlabilidad y observabilidad

Un sistema lineal invariante en el tiempo x_(k+1) = A x_k + B u_k, y_k = C x_k, con n estados, es **controlable** cuando la entrada puede llevar cualquier estado a cualquier otro en un número finito de pasos, y **observable** cuando las salidas determinan el estado inicial. Tras n pasos desde x_0 = 0, los estados alcanzables son el espacio columna de la **matriz de controlabilidad** [B, AB, …, A^(n−1) B]. Por el teorema de Cayley–Hamilton, A^n es una combinación de I, A, …, A^(n−1), así que las potencias siguientes no añaden nada, y el sistema es controlable exactamente cuando esta matriz tiene rango n (Kalman). Del mismo modo, es observable exactamente cuando la **matriz de observabilidad** [C; CA; …; C A^(n−1)] tiene rango n. Las dos nociones son duales: (A, C) es observable exactamente cuando (Aᵀ, Cᵀ) es controlable. El criterio de Hautus señala al culpable: (A, B) es controlable exactamente cuando [A − λI, B] tiene rango n para todo valor propio λ de A. Para una A diagonal con valores propios distintos, el modo i es controlable exactamente cuando la fila i de B no es nula, y observable exactamente cuando la columna i de C no es nula.

El doble integrador discreto A = [[1, 1], [0, 1]], B = [0; 1], C = [1, 0] tiene [B, AB] = [[0, 1], [1, 1]] y [C; CA] = [[1, 0], [1, 1]], ambas de rango 2, con valores singulares φ = 1.618034 y 1/φ = 0.618034. El sistema modal A = diag(1, 2, 3), B = [1; 1; 0], C = [1, 1, 0] tiene [B, AB, A²B] = [[1, 1, 1], [1, 2, 4], [0, 0, 0]], de rango 2, con valores singulares 4.838, 0.7735 y 0: su tercer modo no es ni alcanzable ni visible, y [A − 3I, B] tiene rango 2.

Un ordenador decide el rango contando los valores singulares que superan una tolerancia. La convención de LAPACK y NumPy toma max(filas, columnas) × σ_max × ε, con ε = 2^(−52): 3.22e-15 para el sistema modal. Un cambio de base x → Tx, con T = [[1, 2, 0], [0, 1, 1], [1, 0, 2]] (det T = 4), convierte (A, B, C) en (TAT⁻¹, TB, CT⁻¹), sin ningún cero que leer. Los rangos no cambian: la matriz de controlabilidad transformada tiene valores singulares 11.76 y 0.7791, y un tercero que es 0 en aritmética exacta y un residuo de redondeo del orden de 1e-16 en coma flotante, frente a una tolerancia de 7.84e-15.

El valor singular más pequeño, el **margen**, es la distancia en norma 2 a la matriz de rango inferior más cercana (Eckart–Young, MAT-006). Con A = diag(1, 1 + 1e-10) y C = [1, 1], la matriz de observabilidad tiene valores singulares de alrededor de 2 y 5e-11: el sistema es observable, pero con dos modos que la salida no puede distinguir en la práctica. Con A = diag(1, 3) son 3.414214 y 0.585786.

Las potencias de A también degradan el cálculo. Para A = diag(1, 2, …, n) y B una columna de unos, la matriz de controlabilidad es una matriz de Vandermonde, y las matrices de Vandermonde están notoriamente mal condicionadas (Gautschi, 1975). Con valores singulares calculados a 60 dígitos y la tolerancia anterior, n = 12 da σ_max = 8.057e11, σ_min = 1.139e-4 y una tolerancia de 2.147e-3, de ahí el rango 11, para un sistema que es controlable: sus valores propios son distintos y B toca todos los modos. Escalar A por 1/12 baja σ_max a 5.143 y la tolerancia a 1.37e-14, y devuelve el rango a 12. Escalar ayuda sin curar: con la misma escala, n = 20 tiene σ_min = 1.541e-16 frente a una tolerancia de 3.009e-14, y rango 18. Los algoritmos de escalera de Paige y de Van Dooren (1981) reducen (A, B) mediante transformaciones ortogonales y nunca forman las potencias.

### Ejercicio práctico

En el sistema modal, sustituye B por [1; 1; 1]. ¿Es controlable ahora? ¿Y observable?

> *Solución:* Controlable: B toca todos los modos y los valores propios son distintos, y [B, AB, A²B] = [[1, 1, 1], [1, 2, 4], [1, 3, 9]] es una matriz de Vandermonde con determinante (2 − 1)(3 − 1)(3 − 2) = 2. Sigue sin ser observable: C = [1, 1, 0] no ve el tercer modo, y la matriz de observabilidad mantiene el rango 2.

---

## 7. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus tests. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea a Python de `lyapunov.rs`, `bifurcation.rs` y `control.rs` en `crates/ix-chaos`, y de `kalman.rs` y `state_space.rs` en `crates/ix-signal`. La transcripción reproduce las aserciones de los tests que cita esta sección. No cubre `bifurcation_diagram`, `drive_response_sync`, el filtro de velocidad constante, ni los tests de construcción y simulación del modelo de espacio de estados. Estos números son predicciones, y el §8 propone comprobarlos.

**El exponente de una aplicación, y el nombre que se le da.** [`mle_1d`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L8) promedia ln|f′| a lo largo de la órbita tras un transitorio, y [devuelve −∞](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L23) en el primer |f′| menor que 1e-15. La herramienta MCP `ix_chaos_lyapunov` es el manejador [`chaos_lyapunov`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1436), que la ejecuta sobre la aplicación logística [desde x_0 = 0.1 con un transitorio de 1,000](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1449) y nombra el resultado con [un umbral de 0.01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1450), mediante [`classify_dynamics`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L160):

```rust
pub fn classify_dynamics(mle: f64, threshold: f64) -> DynamicsType {
    if mle > threshold {
        if mle > 10.0 {
            DynamicsType::Divergent
        } else {
            DynamicsType::Chaotic
        }
    } else if mle > -threshold {
        DynamicsType::Periodic
    } else {
        DynamicsType::FixedPoint
    }
}
```

La documentación del enum describe [`FixedPoint`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L150) como la convergencia a un punto fijo y [`Periodic`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L152) como una órbita cuasiperiódica o un ciclo límite, que es como se leen los exponentes de un flujo. Para una aplicación, el §2 muestra que todo ciclo estable tiene λ < 0. Por eso la herramienta llama `FixedPoint` al ciclo de periodo 2 en r = 3.2, al ciclo de periodo 4 en r = 3.5 y al ciclo de periodo 3 en r = 3.83. Llama `Periodic` al valor r = 3, donde el punto fijo está a punto de perder la estabilidad y todavía no existe ningún ciclo. Los propios tests de métricas de bucle de IX fijan dos consecuencias más: un exponente NaN falla todas las comparaciones y [cae en `FixedPoint`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/tests/loop_metrics.rs#L279), y un [bucle estancado es `Periodic`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/tests/loop_metrics.rs#L256). Los tests de `mle_1d` comprueban que [r = 4 da ln 2 con un margen de 0.05](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L179), donde la transcripción queda a 0.000012, y que [r = 3.2 da un valor negativo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L195).

**El espectro: RK4 para el estado, Euler para las tangentes.** [`lyapunov_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L43) integra el estado con [un paso de Runge–Kutta de cuarto orden](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L65), pero mueve los vectores tangentes con [un paso de Euler, con la jacobiana tomada en el estado ya actualizado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L92), y luego los reortonormaliza mediante [Gram–Schmidt modificado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L106). Para el flujo lineal ẋ = a x el exponente exacto es a, pero un paso de Euler multiplica un vector tangente por 1 + a dt, así que la función devuelve ln|1 + a dt| / dt. Con dt = 0.01 eso da −1.005034 para a = −1 y 0.995033 para a = +1: un sesgo de alrededor de a² dt / 2 que más pasos no eliminan. La función no tiene test, y nada en el espacio de trabajo la llama; solo las guías de teoría del caos de IX la muestran en ejemplos.

**Detección de periodo con una tolerancia fija.** [`detect_period`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L61) compara los iterados tras el transitorio con [el primero de ellos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L77). Su test comprueba [los periodos 1 y 2 en r = 2.5 y 3.2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L159); con los ajustes del test, la transcripción encuentra también 4 en r = 3.5, 8 en 3.55, 16 en 3.566, 3 en 3.83, y ningún periodo en 3.8. [`find_period_doublings`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L92) barre r uniformemente, detecta el periodo [con una tolerancia de 1e-8 y como máximo 64](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L108), y registra r allí donde el periodo es el doble del del punto anterior; [un punto sin periodo reinicia la comparación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L110). Sobre [2.9, 3.57] desde x_0 = 0.5, la transcripción da:

| Puntos del barrido | Transitorio | Duplicaciones registradas | Cocientes resultantes |
|---|---|---|---|
| 68 | 1,000 | 3.55 | ninguno |
| 68 | 10,000 | 3.45, 3.55 | ninguno |
| 671 | 1,000 | 2.985, 3.444, 3.542, 3.569 | 4.684, 3.63 |
| 671 | 10,000 | 2.999, 3.449, 3.565, 3.569 | 3.879, 29.0 |

La primera duplicación está en r = 3, y sin embargo la tercera fila registra 2.985, donde el punto fijo sigue siendo estable. Allí el multiplicador es −0.985, y tras 1,000 pasos la órbita sigue a alrededor de 1e-8 de x*. Un paso después queda al otro lado, a alrededor de 1.99e-8 del iterado inicial, lo que no pasa la tolerancia; dos pasos después está a 2.99e-10, lo que sí la pasa, así que el barrido ve periodo 2. Ninguna de las filas se acerca a δ. [`feigenbaum_delta`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L124) solo toma los cocientes. Su [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L170) le da cuatro puntos fijados en el código, de los que obtiene 4.7515 y 4.6578, y solo afirma que el primer cociente está entre 3 y 6. `find_period_doublings` no tiene test.

**OGY: el test pasa sin control.** [`ogy_control`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L17) calcula la perturbación del §4 y [la recorta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L42). Su [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L154) es la ejecución del §4, y afirma que el último estado está [a menos de 0.1 de x*](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L176). La transcripción queda fijada a 2.2e-16 a partir del paso 60. Sin ningún control, el estado en el paso 199 está a 0.0892 de x*, lo que también pasa. Desde x_0 = 0.3, 0.6 y 0.9, las distancias sin control son 0.0876, 0.1653 y 0.1481. Sobre 10,000 puntos de partida tomados uniformemente (`random` de Python, semilla 0), el 28.28% termina a menos de 0.1 sin ningún control, y todos quedan fijados a 1e-12 con él. La tolerancia del test no distingue el control del azar.

**Pyragas: un retardo un paso más corto.** [`pyragas_control`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L57) guarda los estados retardados en un búfer circular que empieza como [`delay_steps` copias de x_0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L68):

```rust
    for step in 0..steps {
        trajectory.push(x.clone());

        let mut dx = dynamics(&x);

        // Apply Pyragas control after startup
        if step >= control_start && step >= delay_steps {
            let delayed = &history[step % delay_steps];
            for i in 0..n {
                dx[i] += gain * (delayed[i] - x[i]);
            }
        }

        // Euler integration (simple for demonstration)
        for i in 0..n {
            x[i] += dt * dx[i];
        }

        history[step % delay_steps] = x.clone();
    }
```

En el paso k lee la casilla k mod d, que el paso k − d escribió tras su actualización, con el estado x_(k−d+1). El término de control usa por tanto x(t − (d − 1) dt), no x(t − d dt). Con `delay_steps` = 1 lee el estado actual y el término de control es cero, sea cual sea la ganancia. Con 0, el primer resto que calcula provoca un pánico: en la línea 78 si el control empieza en el paso 0, en la línea 89 en caso contrario. El ejemplo de la guía de IX pasa [628 pasos para un periodo de 2π con dt = 0.01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/chaos-theory/chaos-control.md#L112), así que el retardo efectivo es de 627 pasos. La función no tiene test.

**Kalman: la forma corta, y una protección construida alrededor de su pánico.** [`KalmanFilter::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L36) fija [H = 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L39), Q = 0.01 I, R = I y P = I, y los contratos del crate dicen que estos [valores por defecto no son un filtro utilizable](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L12). [`update`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L65) invierte S [con `expect("Innovation covariance singular")`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L76) y actualiza P con [la forma corta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L82). El [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L134) es la ejecución escalar del §5, y afirma que la última estimación está [a menos de 0.5 de 5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L161); la transcripción termina en 4.6219, a 0.3781. Los manejadores MCP rechazan un ruido de medición menor que [1e-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L956). Su documentación explica que ese mínimo evita el pánico, señala que la actualización [«usa `P = (I − KH)P`, no la forma de Joseph»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L937), y registra [una tabla medida](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L940) en la que q = r = 1e-13 provoca un pánico a partir de cuatro muestras.

**Tests de rango con un margen y una tolerancia.** [`StateSpaceModel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L121) construye las matrices de [controlabilidad](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L265) y de [observabilidad](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L282) con n bloques, lo que sus comentarios justifican por Cayley–Hamilton. [`rank_report`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L372) usa [la tolerancia del §6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L396) e informa del [valor singular más pequeño como margen](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L400). Los tests fijan los ejemplos del §6: el [doble integrador](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L232), el [tercer modo oscuro](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L241), el [mismo sistema tras el cambio de base](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L257), y los [dos márgenes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L391). Un filtro cuya matriz de control nunca se fijó [da rango 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L475). El comentario sobre el cambio de base del test dice [det = −3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L53); el determinante es 4, lo que no hace daño, ya que cualquier matriz invertible sirve. La documentación del módulo advierte de que, con un radio espectral grande, [el rango puede salir por debajo del real](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L66) y de que no hay implementado ningún algoritmo de escalera. El §6 muestra el efecto desde n = 12, con valores propios de 1 a 12. El modelo de espacio de estados no está expuesto por MCP.

**Lo que falta.** Nada en `ix-signal` ni en `ix-chaos` comprueba la estabilidad mediante el radio espectral. El único campo llamado `spectral_radius` en el espacio de trabajo, en una [red de reservorio](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/memristive-markov/src/reservoir.rs#L12), [reescala los pesos por su mayor elemento en valor absoluto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/memristive-markov/src/reservoir.rs#L34), lo que no es el radio espectral. No hay ecuación de Lyapunov, ni LQR, ni controlador PID. La matriz de brechas de IX distingue los [dos Lyapunov](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/research/tars-v1-advanced-math-ix-gap-matrix.md#L171): el exponente, que IX tiene, y la función de Lyapunov, un certificado de estabilidad que se obtiene resolviendo AᵀPA − P = −Q, y que [planea](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/research/tars-v1-advanced-math-ix-gap-matrix.md#L314).

Corregir cualquiera de estas cosas corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

La herramienta `ix_chaos_lyapunov` responde `FixedPoint` para la aplicación logística en r = 3.5. ¿Cuál es el atractor, y cómo lo averiguarías con IX?

> *Solución:* Un ciclo estable de periodo 4. Su exponente, −0.872507, es menor que −0.01, de ahí el nombre, que solo dice que las órbitas cercanas convergen. `detect_period` con los ajustes del test devuelve 4.

---

## 8. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Un barrido de λ(r).** Ejecutar `mle_1d` sobre la aplicación logística para r de 2.5 a 4.0 en pasos de 0.001, desde x_0 = 0.1 con 10,000 iteraciones tras un transitorio de 1,000, y nombrar cada valor con `classify_dynamics` a 0.01. Predicción: en los r de la tabla del §2, sus valores con seis decimales; `Chaotic` en 3.7, 3.8 y 4.0; `FixedPoint` en 3.2, 3.5 y 3.83; `Periodic` en 3.0.
2. **El barrido de duplicaciones.** Ejecutar `find_period_doublings` sobre [2.9, 3.57] desde x_0 = 0.5 con los cuatro ajustes del §7. Predicción: las cuatro filas de su tabla, incluida la duplicación en 2.985.
3. **OGY con y sin control.** Ejecutar el test de IX tal como está escrito, y luego con `control_start` = 200, de modo que el control nunca empiece. Predicción: una distancia final de 2.2e-16 con control y de 0.0892 sin él; ambas pasan la tolerancia de 0.1 del test.
4. **El retardo de Pyragas.** Ejecutar `pyragas_control` sobre un oscilador bidimensional con `delay_steps` = 1, una vez con ganancia 0 y otra con ganancia 5. Luego ejecutarlo con `delay_steps` = 0. Predicción: las dos ejecuciones con un retardo de 1 dan la misma trayectoria bit a bit; un retardo de 0 provoca un pánico.
5. **El filtro escalar.** Ejecutar el filtro del test, y luego el mismo filtro sobre 200 mediciones de 0. Predicción: las diez estimaciones del §5 con cuatro decimales; tras 200 pasos, una ganancia y una covarianza de 0.095125.
6. **El rango bajo las potencias.** Construir A = diag(1, …, n) con B una columna de unos, y ejecutar `controllability` para n = 12, luego con A escalada por 1/12, y para n = 14 escalada por 1/14. Predicción: rangos 11, 12 y 14. Los valores singulares más cercanos a la tolerancia están a un factor de 3 o más de ella, así que una SVD en coma flotante no debería cambiar estos rangos. El n = 20 del §6 queda fuera: uno de sus valores singulares está a menos de un factor de 2.5 por debajo de la tolerancia.

### Ejercicio práctico

El paso 3 predice que el test pasa con y sin control. ¿Qué test separaría los dos casos?

> *Solución:* Uno que afirme lo que solo el control consigue. Por ejemplo: una distancia final menor que 1e-12, que la ejecución controlada alcanza en el paso 60 y la no controlada no; o la captura desde muchos puntos de partida. Con control, los 10,000 puntos de partida aleatorios quedan todos fijados a 1e-12, mientras que sin él, el 28.28% termina a menos de 0.1 por azar.

---

## 9. Errores comunes

- **Leer un exponente negativo como un punto fijo.** Todo ciclo estable de una aplicación tiene λ < 0; el periodo debe contarse aparte.
- **Leer «Periodic» como «un ciclo».** Para una aplicación, un exponente cercano a cero marca un comportamiento marginal, como un punto de bifurcación, no un ciclo estable.
- **Fiarse de la linealización en |f′(x*)| = 1.** Allí deciden los términos de orden superior, y la convergencia, si la hay, es lenta.
- **Tomar ρ(A) < 1 como «nunca crece».** Una A no normal puede amplificar un estado muchas veces antes de que decaiga.
- **Localizar bifurcaciones con una sola tolerancia y un solo transitorio.** Cerca de una bifurcación la convergencia es más lenta, así que es ahí donde un test fijo se equivoca.
- **Aceptar un test de control que pasa sin control.** Una tolerancia más holgada que la dispersión sin control no prueba nada.
- **Usar la actualización corta de la covarianza con una ganancia que no es óptima.** Solo la forma de Joseph sigue siendo correcta para cualquier ganancia.
- **Leer el rango completo como «bien controlable» o «bien observable».** El margen dice a qué distancia está el sistema de perder la propiedad; escala el sistema antes de comparar márgenes.
- **Formar potencias altas de A.** Las matrices de Kalman heredan el condicionamiento de las potencias de A; las reducciones ortogonales de escalera las evitan.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Punto fijo** | Un estado x* con f(x*) = x* |
| **Multiplicador** | f′(x*) en un punto fijo, o el producto de f′ a lo largo de un ciclo; la estabilidad exige un módulo menor que 1 |
| **Superestable** | Un punto fijo o un ciclo con multiplicador 0, donde los errores se elevan al cuadrado en cada paso |
| **Radio espectral** | El mayor módulo de un valor propio; ρ(A) < 1 hace que x_(k+1) = A x_k converja a 0 |
| **Exponente de Lyapunov** | El promedio de ln\|f′\| a lo largo de una órbita: la tasa exponencial a la que se separan las órbitas cercanas |
| **Bifurcación de duplicación de periodo** | Un valor del parámetro en el que el multiplicador de un ciclo pasa por −1 y nace un ciclo de periodo doble |
| **Constante de Feigenbaum** | δ = 4.669201…, el límite de los cocientes de las distancias sucesivas entre duplicaciones |
| **Control OGY** | Pequeños cambios de un parámetro que cancelan la desviación lineal respecto de un punto fijo inestable |
| **Filtro de Kalman** | El estimador lineal recursivo que minimiza la varianza del error a posteriori |
| **Forma de Joseph** | La actualización de la covarianza (I − KH) P⁻ (I − KH)ᵀ + K R Kᵀ, válida para cualquier ganancia |
| **Controlabilidad, observabilidad** | La entrada puede llevar cualquier estado a cualquier otro; las salidas determinan el estado inicial |
| **Criterio del rango de Kalman** | La controlabilidad y la observabilidad se cumplen exactamente cuando las matrices [B, …, A^(n−1) B] y [C; …; C A^(n−1)] tienen rango n |
| **Margen** | El valor singular más pequeño de una matriz de prueba: su distancia a una matriz de rango inferior |

---

## Autoevaluación

**1. Una herramienta informa de λ = −0.37 y «FixedPoint» para una aplicación unidimensional. ¿Qué sabes del atractor?**
> Que las órbitas cercanas convergen, así que el atractor es estable: un punto fijo o un ciclo estable de cualquier periodo. En r = 3.83 la aplicación logística da exactamente esta respuesta para un ciclo de periodo 3. El periodo debe contarse aparte.

**2. ¿Por qué OGY converge cuadráticamente una vez que ha capturado la órbita, y por qué necesita una ventana?**
> La perturbación cancela el término lineal de la desviación, así que lo que queda es de segundo orden. La ventana viene del recorte de la perturbación: solo dentro de |x − x*| ≤ δr_max |f_r| / |f_x| puede el controlador cancelar exactamente el término lineal, y fuera de ella espera a que la órbita caótica lleve el estado dentro.

**3. Un filtro usa la actualización P = (I − KH) P⁻ con una ganancia que el redondeo ha alejado del óptimo. ¿Qué falla?**
> La forma corta solo vale para la ganancia óptima. Con cualquier otra ganancia da una covarianza errónea; con P⁻ = 1, R = 1 y K = 0.8 da 0.2 en lugar del verdadero 0.68, así que el filtro se vuelve demasiado confiado. La forma de Joseph da 0.68 para cualquier ganancia.

**4. El sistema A = diag(1, …, 12), con B una columna de unos, es controlable, y sin embargo un test de rango informa de 11. ¿Está mal el test?**
> En aritmética exacta el rango es 12, ya que los valores propios son distintos y B toca todos los modos. Pero la matriz de controlabilidad es una matriz de Vandermonde con σ_max ≈ 8.1e11 y σ_min ≈ 1.1e-4. El valor singular más pequeño está por debajo de la tolerancia relativa de 2.1e-3, así que numéricamente la matriz no se puede distinguir de una de rango 11. Escalar A por 1/12 restablece el rango 12; un algoritmo de escalera evita por completo las potencias.

**Criterio de aprobación:** Decidir la estabilidad de un punto fijo o de un ciclo a partir de su multiplicador; calcular un exponente de Lyapunov y decir lo que su signo no dice; estimar la δ de Feigenbaum a partir de puntos de bifurcación y explicar por qué un barrido los sitúa mal; calcular la ventana de OGY y explicar la convergencia cuadrática; deducir el régimen estacionario del filtro de Kalman escalar y explicar la forma de Joseph; decidir la controlabilidad y la observabilidad mediante el criterio del rango y leer el margen y la tolerancia; y decir qué salidas de IX fijan sus tests.

---

## Base de investigación

- S. H. Strogatz, *Nonlinear Dynamics and Chaos*, 2.ª edición, Westview Press, 2015: puntos fijos, linealización, la aplicación logística y las bifurcaciones
- R. M. May, «Simple mathematical models with very complicated dynamics», *Nature* 261, 1976: la aplicación logística
- M. J. Feigenbaum, «Quantitative universality for a class of nonlinear transformations», *Journal of Statistical Physics* 19, 1978: la constante δ
- G. Benettin, L. Galgani, A. Giorgilli y J.-M. Strelcyn, «Lyapunov characteristic exponents for smooth dynamical systems and for Hamiltonian systems», *Meccanica* 15, 1980: el espectro por ortonormalización repetida
- E. Ott, C. Grebogi y J. A. Yorke, «Controlling chaos», *Physical Review Letters* 64, 1990: el control OGY
- K. Pyragas, «Continuous control of chaos by self-controlling feedback», *Physics Letters A* 170, 1992: el control por realimentación retardada
- R. E. Kalman, «A new approach to linear filtering and prediction problems», *Journal of Basic Engineering* 82, 1960: el filtro de Kalman
- R. E. Kalman, «On the general theory of control systems», *Proceedings of the First IFAC Congress*, 1960: controlabilidad, observabilidad y dualidad
- R. S. Bucy y P. D. Joseph, *Filtering for Stochastic Processes with Applications to Guidance*, Interscience, 1968: la forma de Joseph
- M. L. J. Hautus, «Controllability and observability conditions of linear autonomous systems», *Indagationes Mathematicae* 31, 1969: el criterio de los valores propios
- C. C. Paige, «Properties of numerical algorithms related to computing controllability», *IEEE Transactions on Automatic Control* 26, 1981, y P. Van Dooren, «The generalized eigenstructure problem in linear system theory», mismo volumen: por qué no deben formarse las potencias de A, y la reducción de escalera
- W. Gautschi, «Norm estimates for inverses of Vandermonde matrices», *Numerische Mathematik* 23, 1975: el condicionamiento de las matrices de Vandermonde
- C. Eckart y G. Young, «The approximation of one matrix by another of lower rank», *Psychometrika* 1, 1936: el margen como distancia
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §7 enlaza a su línea
- Experimento: propuesto en el §8, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
