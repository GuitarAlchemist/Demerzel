---
module_id: mat-012-iterative-optimisation
department: mathematics
course: Optimización iterativa
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-011-gradients-reverse-mode-autodiff]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Optimización iterativa — Tamaños de paso, curvatura y qué significa converger

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Reconocer las funciones convexas, L-suaves y fuertemente convexas, y leer L, μ y el número de condición κ en una hessiana
- Mostrar por qué el descenso de gradiente sobre una cuadrática converge exactamente cuando 0 < η < 2/L, y elegir el paso que minimiza su tasa
- Enunciar las garantías de convergencia del descenso de gradiente para funciones no convexas, convexas y fuertemente convexas, y qué prueba y qué no prueba un gradiente pequeño
- Explicar cómo la inercia de la bola pesada mejora la tasa asintótica de (κ − 1)/(κ + 1) a (√κ − 1)/(√κ + 1) sobre una cuadrática
- Explicar las estimaciones de momentos de Adam y su corrección del sesgo, y por qué su paso es del orden de η sea cual sea el tamaño del gradiente
- Rastrear qué informan los optimizadores de IX, su gradiente numérico y su herramienta MCP, y cuándo «convergido» no significa convergido

---

## 1. Convexidad, suavidad y número de condición

Para minimizar una función diferenciable f: Rⁿ → R, los métodos iterativos buscan un punto donde se anule el gradiente de MAT-011. Tal **punto estacionario** puede ser un mínimo, un máximo o un punto de silla. La función es **convexa** si f(y) ≥ f(x) + ∇f(x) · (y − x) para todos x e y: queda por encima de cada uno de sus planos tangentes, de modo que todo punto estacionario es un mínimo global. Para una f dos veces diferenciable, esto ocurre exactamente cuando la hessiana ∇²f(x), la matriz simétrica de las derivadas parciales segundas, es semidefinida positiva en todas partes.

Dos constantes gobiernan la rapidez de los métodos de descenso. f es **L-suave** si su gradiente es L-lipschitziano, ‖∇f(x) − ∇f(y)‖ ≤ L‖x − y‖; para una f dos veces diferenciable, significa que todo valor propio de toda hessiana está en [−L, L]. f es **μ-fuertemente convexa**, con μ > 0, si todo valor propio de toda hessiana es al menos μ. Su cociente κ = L/μ ≥ 1 es el **número de condición** del problema. El caso modelo es la cuadrática f(x) = ½xᵀAx − bᵀx con A simétrica definida positiva: su hessiana es A en todas partes, así que μ y L son el menor y el mayor valor propio de A, como en MAT-005, y κ es el número de condición κ₂(A) de MAT-003.

### Ejercicio práctico

Sea f(x, y) = x² + 10y². Halla su hessiana, μ, L y κ.

> *Solución:* ∂²f/∂x² = 2, ∂²f/∂y² = 20 y la derivada cruzada es 0, así que la hessiana es la matriz diagonal diag(2, 20) en todo punto. Por tanto μ = 2, L = 20 y κ = 10. Las curvas de nivel son elipses cuyos ejes están en la razón √10 ≈ 3.16, más largas según x; en un punto como (1, 1), el gradiente (2, 20) apunta sobre todo según y, a través del valle, en lugar de hacia el mínimo.

---

## 2. El descenso de gradiente sobre una cuadrática

El **descenso de gradiente** da el paso x_{k+1} = x_k − η∇f(x_k), con un **tamaño de paso** o tasa de aprendizaje η > 0. Sobre la cuadrática del §1, ∇f(x) = Ax − b y el minimizador es x* = A⁻¹b, así que el error e_k = x_k − x* cumple e_{k+1} = (I − ηA)e_k. En la base de vectores propios de A, cada componente se multiplica en cada paso por su propio factor 1 − ηλ, donde λ es el valor propio correspondiente. La iteración converge desde todo punto de partida exactamente cuando |1 − ηλ| < 1 para todo valor propio, es decir, cuando **0 < η < 2/L**.

El umbral es nítido. En η = 2/L, la componente según la dirección más empinada cambia de signo sin disminuir; por encima, esa componente crece como |1 − ηL|^k mientras las demás pueden seguir disminuyendo. La tasa es max(|1 − ημ|, |1 − ηL|). El paso η = 1/L da 1 − μ/L = 1 − 1/κ, y el mejor paso fijo, η = 2/(L + μ), equilibra los dos extremos y da **(κ − 1)/(κ + 1)**. Para κ cercano a 1 el método es rápido; para κ grande, la tasa se acerca a 1 y el método se arrastra a lo largo de las direcciones planas, mientras el paso queda limitado por la empinada.

### Ejercicio práctico

Para f(x) = (L/2)x², ¿para qué tamaños de paso converge el descenso de gradiente? Toma L = 20 y describe qué ocurre para η = 1/20, 3/40, 1/10 y 3/20.

> *Solución:* ∇f(x) = Lx, así que x ← (1 − ηL)x, y la iteración converge exactamente cuando |1 − ηL| < 1, es decir, 0 < η < 2/L = 1/10. Con L = 20: η = 1/20 da el factor 0 y alcanza el mínimo en un paso; η = 3/40 da −1/2, una oscilación que se reduce a la mitad en cada paso; η = 1/10 da −1, una oscilación entre x₀ y −x₀ que nunca disminuye; η = 3/20 da −2, una oscilación que se duplica en cada paso.

---

## 3. El lema de descenso y las velocidades de convergencia

Más allá de las cuadráticas, la L-suavidad sigue acotando f por encima con una parábola: f(y) ≤ f(x) + ∇f(x) · (y − x) + (L/2)‖y − x‖². Es el **lema de descenso**. Con y = x − η∇f(x), da f(y) ≤ f(x) − η(1 − Lη/2)‖∇f(x)‖², un descenso garantizado siempre que 0 < η < 2/L, máximo en η = 1/L, donde vale ‖∇f(x)‖²/(2L). Sumar estos descensos a lo largo de K pasos con η = 1/L da tres garantías, donde f* es el valor mínimo, o el ínfimo:

- para toda f L-suave acotada inferiormente, el mínimo para k < K de ‖∇f(x_k)‖² es ≤ 2L(f(x₀) − f*)/K: algún iterado es casi estacionario, lo que no es lo mismo que casi mínimo;
- para una f convexa con un minimizador x*, f(x_K) − f* ≤ L‖x₀ − x*‖²/(2K);
- para una f μ-fuertemente convexa, f(x_K) − f* ≤ (1 − μ/L)^K (f(x₀) − f*), una tasa lineal.

De ello se siguen dos advertencias. Primero, L acota la curvatura en todos los lugares por donde pasan los iterados. Sobre una función no cuadrática, un paso seguro cerca del mínimo puede ser demasiado grande en otra parte, y es la curvatura local en el punto actual la que decide el paso siguiente (§6). Segundo, un criterio de parada de la forma ‖∇f(x)‖ < tol solo certifica la casi estacionariedad. Solo la convexidad fuerte lo convierte en una cota de la distancia al minimizador, ‖x − x*‖ ≤ ‖∇f(x)‖/μ, y ningún criterio puede certificar un gradiente mal calculado.

### Ejercicio práctico

Para f(x, y) = x² + 10y² del §1, ¿cuántas iteraciones reducen la componente de error más lenta en un factor 10^6, con η = 1/L y con η = 2/(L + μ)?

> *Solución:* Con η = 1/L = 1/20, los factores son 1 − 2/20 = 0.9 según x y 0 según y, así que la tasa es 0.9 y 0.9^k < 10^-6 exige k ≥ 132. Con η = 2/(L + μ) = 1/11, los factores son 1 − 2/11 = 9/11 y 1 − 20/11 = −9/11, la tasa es (κ − 1)/(κ + 1) = 9/11, y (9/11)^k < 10^-6 exige k ≥ 69, aproximadamente la mitad.

---

## 4. La inercia

El **método de la bola pesada** de Polyak añade al paso de gradiente una fracción β del paso anterior: v_{k+1} = βv_k − η∇f(x_k) y x_{k+1} = x_k + v_{k+1}, o de forma equivalente x_{k+1} = x_k − η∇f(x_k) + β(x_k − x_{k−1}). La velocidad v se acumula según las direcciones donde el gradiente mantiene su signo y se cancela según las direcciones donde alterna, que es exactamente el valle del §1: un avance constante según el eje plano, una oscilación amortiguada a través del empinado.

Sobre una cuadrática, la elección η = 4/(√L + √μ)² y β = ((√κ − 1)/(√κ + 1))² da la tasa asintótica **(√κ − 1)/(√κ + 1)**. Toma x² + 100y² desde (1, 1), así que κ = 100. El descenso de gradiente con su mejor paso multiplica ambas coordenadas por ±99/101 ≈ ±0.980 en cada paso y necesita 691 pasos para llevarlas por debajo de 10^-6. Para la bola pesada, (9/11)^k ≈ 0.818^k sugiere 69 pasos, pero esa tasa solo es asintótica: con estos parámetros la recurrencia tiene una raíz doble, y con velocidad inicial nula las coordenadas valen exactamente (1 + 2k/11)(9/11)^k y (1 + 20k/11)(−9/11)^k. El factor lineal retrasa la ganancia, y ambas coordenadas solo caen por debajo de 10^-6 tras 95 pasos, aun así unas siete veces menos que 691. La ganancia crece con κ, ya que el número de iteraciones crece como κ para uno y como √κ para la otra. Esta tasa solo está garantizada sobre cuadráticas: Lessard, Recht y Packard dan una función suave y fuertemente convexa sobre la que la bola pesada con estos parámetros no converge. El gradiente acelerado de Nesterov alcanza una tasa del mismo orden, 1 − 1/√κ, con una garantía para toda función suave y fuertemente convexa.

### Ejercicio práctico

Con β = 0.9, ¿hacia qué tiende la velocidad cuando el gradiente es una constante g, como en una pendiente larga y recta?

> *Solución:* v_k = −ηg(1 + β + … + β^(k−1)), que tiende a −ηg/(1 − β) = −10ηg. Sobre una pendiente constante, la inercia multiplica el paso efectivo por 1/(1 − β) = 10; es su ventaja en las direcciones planas y su peligro cuando la pendiente cambia, ya que la velocidad tarda unos 1/(1 − β) pasos en girar.

---

## 5. Pasos adaptativos: Adam

**Adam**, de Kingma y Ba, mantiene dos medias móviles exponenciales por coordenada: la del gradiente, m_k = β₁m_{k−1} + (1 − β₁)g_k, y la de su cuadrado, v_k = β₂v_{k−1} + (1 − β₂)g_k², con los valores por defecto β₁ = 0.9 y β₂ = 0.999. Divide la primera por la raíz cuadrada de la segunda: x_{k+1} = x_k − η m̂_k/(√v̂_k + ε), coordenada a coordenada, con ε = 10^-8.

Ambas medias empiezan en 0, así que al principio están sesgadas hacia 0: si el gradiente fuera constante, m_k valdría (1 − β₁^k) veces ese gradiente. La **corrección del sesgo** divide por ese factor, m̂_k = m_k/(1 − β₁^k) y v̂_k = v_k/(1 − β₂^k). En el primer paso, m̂₁ = g₁ y v̂₁ = g₁², así que el paso vale η g₁/(|g₁| + ε), aproximadamente η en tamaño, en la dirección opuesta al signo del gradiente. Más en general, Kingma y Ba muestran que el paso está aproximadamente acotado por η, sea cual sea la escala del gradiente. Es lo contrario del descenso de gradiente, cuyo paso es proporcional al gradiente. Significa que Adam no puede explotar como lo hace el descenso de gradiente por encima de 2/L; significa también que no tiene un umbral como 2/L ni una garantía general. Cerca de un mínimo donde el gradiente cambia de signo, m̂ promedia los signos hasta anularlos mientras que v̂ no, y los pasos disminuyen. Reddi, Kale y Kumar dan un problema convexo sencillo sobre el que Adam no converge, y proponen una variante corregida, AMSGrad.

### Ejercicio práctico

Con η = 0.01 y los valores por defecto de β₁, β₂ y ε, ¿cuál es el primer paso de Adam para un gradiente g = 10^-6? ¿Cuál sería para un g mayor sin corrección del sesgo?

> *Solución:* El primer paso corregido vale η g/(|g| + ε) = 0.01 · 10^-6/(10^-6 + 10^-8) = 0.01/1.01 ≈ 0.0099: casi η entero, aunque el gradiente sea diminuto. Sin corrección del sesgo, m₁ = 0.1g y v₁ = 0.001g², y el paso vale η · 0.1|g|/(√0.001 |g|) ≈ 3.16η cuando |g| es mucho mayor que ε: más del triple del tamaño buscado, porque √v₁ ≈ 0.0316|g| subestima |g| más de lo que m₁ = 0.1g subestima g.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea de su bucle a Python, cuyos flotantes son binary64 IEEE como el `f64` de Rust: son predicciones, y el §7 propone comprobarlas.

**Los optimizadores** (`crates/ix-optimize`). [`SGD`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L21) da el paso del §2; [`Momentum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L49) es la bola pesada del §4, con una velocidad inicializada en −η∇f; y [`Adam`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L111) es el §5, con las [constantes por defecto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L77) y la [corrección del sesgo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L107). Salvo que un objetivo aporte su propio gradiente, el [valor por defecto del trait](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/traits.rs#L12) es [`numerical_gradient`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/calculus.rs#L7) con ε = 10^-7, y el envoltorio de clausuras [`ClosureObjective`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/traits.rs#L43) no aporta ninguno. [`minimize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L124) ejecuta el bucle siguiente: guarda el mejor valor visto, y declara la convergencia en cuanto la norma del gradiente que acaba de usar cae por debajo de la tolerancia.

```rust
    for i in 0..criteria.max_iterations {
        let grad = objective.gradient(&params);
        let new_params = optimizer.step(&params, &grad);
        let value = objective.evaluate(&new_params);

        if value < best_value {
            best_value = value;
            best_params = new_params.clone();
        }

        // Check gradient norm convergence
        let grad_norm: f64 = grad.dot(&grad).sqrt();
        if grad_norm < criteria.tolerance {
            return OptimizeResult {
                best_params,
                best_value,
                iterations: i + 1,
                converged: true,
            };
        }
```

**La herramienta MCP.** `ix_optimize` llama al manejador [`optimize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L181). Quien la llama elige una función entre esfera, Rosenbrock y Rastrigin, una dimensión, un método y un tope de iteraciones, según su [esquema](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L20). Para los métodos con gradiente, el manejador fija el resto: [η = 0.01 para `SGD`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L221) y [para `Adam`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L230), una [tolerancia de 10^-8](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L224) sobre la norma del gradiente, y un [inicio en 5 en cada coordenada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L226). Devuelve el mejor punto, el mejor valor, el número de iteraciones y el [indicador `converged`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L259). Los métodos `pso` y `annealing` no usan gradiente y se dejan aquí de lado.

- **Una divergencia se informa como convergencia.** La función de Rosenbrock f(x, y) = 100(y − x²)² + (1 − x)² vale f(5, 5) = 40,016 en el inicio, con el gradiente (40,008, −4000). Su hessiana tiene allí ∂²f/∂x² = 28,002 y un valor propio máximo cercano a 28,145, así que el umbral 2/L de la curvatura local es de unos 7.1 · 10^-5 y η = 0.01 es unas 140 veces demasiado grande. `SGD` lleva x a −395.08, luego a unos 2.5 · 10^8, luego a unos −5.5 · 10^25. Allí la separación entre dobles vecinos es 2^33 ≈ 8.6 · 10^9, así que x + 10^-7 y x − 10^-7 se redondean ambos a x; e y, todavía de unos 3.1 · 10^5, se pierde junto a x² ≈ 3 · 10^51 cuando se redondea y − x², con o sin 10^-7. Cada cociente de diferencias del gradiente numérico vale entonces exactamente 0. El bucle ve un gradiente nulo y devuelve `converged` verdadero tras 4 iteraciones, con el mejor punto (5, 5), el inicio, y el mejor valor 40,016. En dimensión 3, ocurre lo mismo con el valor 80,032.
- **El tamaño de paso es el mismo para las tres funciones.** Sobre la [esfera](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L195), la suma de cuadrados, L = 2, así que η = 0.01 es cincuenta veces menor que el paso 1/L = 1/2 que alcanza el mínimo de una vez. Cada iteración multiplica el error por 1 − 2η = 0.98, y la transcripción se detiene tras 1027, 1044 y 1054 iteraciones en dimensiones 1, 2 y 3. Sobre Rosenbrock, el mismo η es demasiado grande en el inicio.
- **Los mínimos de Rastrigin repelen a SGD.** La función de Rastrigin suma, por coordenada, x² − 10 cos(2πx) + 10, cuyo [término](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L211) tiene curvatura 2 + 40π² cos(2πx), hasta 2 + 40π² ≈ 396.8. En cada uno de sus 55 mínimos locales entre −27 y 27, incluido el global en 0, η por esta curvatura supera 2, con un valor mínimo de unos 2.07, de modo que, por el §2, cada uno de estos mínimos repele la iteración. Los primeros mínimos estables, hacia ±27.8, quedan lejos de la región que visitan los iterados: desde 5, la transcripción se mantiene en |x| < 5.5 y devuelve `converged` falso tras 5000 iteraciones. `Adam`, cuyo paso no es proporcional al gradiente, se asienta en el mínimo local cercano a 4.975, con un valor de unos 24.87 por coordenada: convergido, hacia un punto estacionario que no es el mínimo global 0.
- **Rosenbrock en dimensión 1 es idénticamente nula.** El objetivo suma sobre [`0..x.len() - 1`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L200), vacío para una sola coordenada, y el esquema [admite la dimensión 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L24). Ambos métodos informan entonces de convergencia tras 1 iteración, en 5, con el valor 0.
- **El gradiente numérico tiene un paso absoluto.** ε = 10^-7 está unas cincuenta veces por debajo del mejor paso centrado u^(1/3) ≈ 5 · 10^-6 de MAT-011, así que su error es sobre todo de redondeo, del orden de u|f|/ε ≈ 1.1 · 10^-9 |f| por componente, frente a una tolerancia de 10^-8. Y ε no se escala con |x|: en cuanto una coordenada supera 2^30 ≈ 1.07 · 10^9 en valor absoluto, x ± 10^-7 se redondea a x y esa componente vale exactamente 0, que es el mecanismo del primer hallazgo.
- **«SGD» es determinista.** El tipo está [documentado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L8) como «Stochastic Gradient Descent», pero avanza según el gradiente completo que recibe, y nada en el bucle muestrea: es el descenso de gradiente del §2.
- **Las pruebas solo comprueban el valor.** [`test_adam_rosenbrock`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L193) ejecuta `Adam` con η = 0.01 desde (0, 0) y [afirma un mejor valor inferior a 0.1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L205), con el comentario «Adam may not converge perfectly on Rosenbrock»; la transcripción predice una convergencia a menos de 10^-7 de (1, 1), con un mejor valor inferior a 10^-15. La prueba cuadrática, `test_sgd_quadratic`, también [afirma solo un valor](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L189). Ninguna de las dos comprueba `converged` ni `iterations`, los dos campos que, según muestra el primer hallazgo, pueden inducir a error.

El gradiente numérico perturba una coordenada cada vez con el mismo ε absoluto:

```rust
    let n = x.len();
    let mut grad = Array1::zeros(n);
    for i in 0..n {
        let mut x_plus = x.clone();
        let mut x_minus = x.clone();
        x_plus[i] += epsilon;
        x_minus[i] -= epsilon;
        grad[i] = (f(&x_plus) - f(&x_minus)) / (2.0 * epsilon);
    }
    grad
```

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

En el primer hallazgo, ¿por qué el gradiente numérico vale exactamente 0 en x ≈ −5.5 · 10^25, cuando el verdadero gradiente allí es enorme?

> *Solución:* Hacia 5.5 · 10^25, dos dobles consecutivos distan 2^33 ≈ 8.6 · 10^9, así que `x_plus[i] += epsilon` y `x_minus[i] -= epsilon` dejan ambos x sin cambios. Las dos evaluaciones de f ocurren entonces en el mismo punto, su diferencia vale exactamente 0, y también el cociente. Para la componente en y, los dos puntos sí difieren, pero hacia x² ≈ 3 · 10^51 dos dobles consecutivos distan 2^119 ≈ 6.6 · 10^35, así que y + 10^-7 − x² e y − 10^-7 − x² se redondean al mismo número, y f toma dos veces el mismo valor. La verdadera derivada respecto de x, del orden de 400|x|³, nunca interviene: el cociente de diferencias solo ve los valores que devuelve f. Un paso escalado con |x|, o un gradiente calculado por el modo inverso de MAT-011, no se anularía.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **El umbral 2/L.** Minimiza f(x) = 10x², escrita `10.0 * x[0] * x[0]` en un `ClosureObjective`, así que L = 20 y 2/L = 0.1, con `SGD` desde x = 1, una tolerancia de 10^-8 y un tope de 400 iteraciones. Predicción: η = 0.05 converge tras 2 iteraciones; η = 0.09 converge tras 97; η = 0.1 no converge, y |x| se mantiene a menos de 10^-6 de 1; η = 0.2 devuelve `converged` verdadero tras 20 iteraciones con el mejor punto 1 y el mejor valor 10, aunque x haya crecido como 3^k.
2. **El manejador MCP, llamado dentro del proceso.** Llama a `optimize` con Rosenbrock en dimensiones 2 y 3, con `sgd` y un tope de 5000. Predicción: `converged` verdadero tras 4 iteraciones, mejor punto 5 en cada coordenada, mejores valores 40,016 y 80,032. Rosenbrock en dimensión 1, con `sgd` y con `adam`: convergencia tras 1 iteración con el valor 0. Rastrigin en dimensiones 1 a 3: `sgd` no convergido tras 5000 iteraciones; `adam` convergido, cada coordenada cerca de 4.975 y el valor cerca de 24.87 veces la dimensión. La esfera con `sgd`: 1027, 1044 y 1054 iteraciones.
3. **La inercia.** Minimiza x² + 10y² desde (1, 1), con una tolerancia de 10^-8 y un tope de 2000. Predicción: `SGD` con η = 1/20 converge tras 183 iteraciones y con η = 1/11 tras 108; `Momentum` con η = 4/(√20 + √2)² y β = ((√10 − 1)/(√10 + 1))² tras 40.
4. **La prueba de Adam, registrando el resultado.** Repite la configuración de `test_adam_rosenbrock` y registra `converged`, `iterations` y el mejor punto. Predicción: convergencia tras unas 1300 iteraciones, entre 1200 y 1400, en un punto a menos de 10^-7 de (1, 1), con un mejor valor inferior a 10^-15.
5. **El primer paso de Adam.** Llama a `step` una vez sobre un `Adam::new(0.01)` nuevo en el punto 0 con el gradiente 10^-6, y una vez sobre otro con el gradiente 10^6. Predicción: pasos de −0.01/1.01 y de −0.01, cada uno con un error menor que 10^-12.

### Ejercicio práctico

Predice el número de iteraciones para η = 0.09 en el paso 1, tomando el gradiente numérico como exacto.

> *Solución:* El factor es 1 − 0.09 · 20 = −0.8, así que tras i pasos |x| = 0.8^i y el gradiente que comprueba el bucle vale 20 · 0.8^i. Cae por debajo de 10^-8 cuando 0.8^i < 5 · 10^-10, es decir, i > ln(2 · 10^9)/ln(1.25) ≈ 95.98, así que por primera vez en i = 96; el bucle cuenta desde 0 e informa de i + 1 = 97 iteraciones. El margen en i = 96 es inferior al 1%, mucho mayor que el error de redondeo relativo del gradiente numérico.

---

## 8. Errores comunes

- **Una sola tasa de aprendizaje para todos los problemas.** El paso seguro lo fija la curvatura, 2/L; un η fijo puede ser más de cien veces demasiado grande para una función y cincuenta veces demasiado pequeño para otra.
- **Leer «convergido» como «minimizado».** Una norma pequeña del gradiente solo certifica la casi estacionariedad: un punto de silla, un mínimo local o un gradiente calculado como nulo pasan todos la prueba.
- **Un paso de diferencias finitas absoluto.** Un paso de 10^-7 desaparece en el redondeo en cuanto |x| supera 2^30; escálalo con el tamaño de x, o usa diferenciación automática.
- **Ignorar la dirección empinada.** En un problema mal condicionado, la dirección más empinada limita el paso y la más plana marca el ritmo; el número de iteraciones crece como κ.
- **Inercia sin garantía.** La tasa de la bola pesada está demostrada para cuadráticas; sobre otras funciones, puede oscilar o no converger donde el método de Nesterov sí convergería.
- **Tratar el paso de Adam como un paso de gradiente.** Su tamaño es de unos η sea cual sea el gradiente, así que η fija una distancia por paso, no una fracción de la pendiente.
- **Probar solo el valor.** Una prueba que acota el mejor valor pero no `converged` ni `iterations` pasa incluso cuando el bucle informa de una falsa convergencia.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Punto estacionario** | Un punto donde el gradiente se anula: un mínimo, un máximo o un punto de silla |
| **Función convexa** | Una función por encima de cada uno de sus planos tangentes; todo punto estacionario es un mínimo global |
| **L-suave** | Que tiene un gradiente L-lipschitziano; los valores propios de la hessiana están en [−L, L] |
| **Fuertemente convexa** | Cuyos valores propios de la hessiana valen todos al menos μ > 0 |
| **Número de condición** | κ = L/μ, el cociente entre la curvatura más empinada y la más plana |
| **Tamaño de paso** | El factor η que multiplica el gradiente en un paso de descenso, también llamado tasa de aprendizaje |
| **Lema de descenso** | f(y) ≤ f(x) + ∇f(x) · (y − x) + (L/2)‖y − x‖² para una f L-suave |
| **Inercia de la bola pesada** | El descenso de gradiente más una fracción β del paso anterior |
| **Corrección del sesgo** | La división de las medias móviles de Adam por 1 − β^k para deshacer su inicio en 0 |
| **Adam** | Un método que divide una media de los gradientes por la raíz de una media de sus cuadrados, coordenada a coordenada |
| **Criterio de parada por la norma del gradiente** | Detenerse cuando ‖∇f‖ cae por debajo de una tolerancia, una prueba de casi estacionariedad solamente |

---

## Autoevaluación

**1. Una cuadrática tiene μ = 2 y L = 50. ¿Para qué tamaños de paso converge el descenso de gradiente, y qué paso fijo minimiza su tasa?**
> Converge exactamente para 0 < η < 2/L = 0.04; la cota misma falla, ya que en η = 0.04 la componente más empinada solo cambia de signo. El mejor paso fijo es 2/(L + μ) = 2/52 ≈ 0.038, con la tasa (κ − 1)/(κ + 1) = 24/26 ≈ 0.92 para κ = 25.

**2. Una ejecución se detiene con ‖∇f‖ < 10^-8. ¿Qué sabes del punto que devuelve?**
> Que el último gradiente calculado por el bucle era pequeño. Si f es μ-fuertemente convexa y ese gradiente era exacto, el punto está a menos de 10^-8/μ del minimizador; si no, puede ser un punto de silla, un mínimo local o, como en el caso Rosenbrock de IX, un punto donde el gradiente numérico se redondeó a cero. En IX, el punto devuelto es además el mejor visto, que puede no ser el punto donde el gradiente era pequeño.

**3. ¿Por qué ayuda la inercia de la bola pesada en x² + 100y², y dónde termina su garantía?**
> Con κ = 100, la bola pesada bien ajustada tiene la tasa asintótica 9/11 en lugar de 99/101, porque la velocidad se acumula según la dirección plana y se cancela a través de la empinada. Desde (1, 1) con velocidad inicial nula, lleva ambas coordenadas por debajo de 10^-6 en 95 pasos en lugar de 691; la estimación asintótica, 69, ignora un factor transitorio que crece linealmente con k. La tasa solo está demostrada para cuadráticas; Lessard, Recht y Packard dan una función fuertemente convexa sobre la que falla, mientras que el método de Nesterov mantiene una tasa de orden 1 − 1/√κ sobre toda función suave y fuertemente convexa.

**4. `ix_optimize` devuelve `converged` verdadero tras 4 iteraciones para Rosenbrock. ¿Puedes fiarte?**
> No solo por ese indicador. Compara el mejor punto con el inicio y mira el mejor valor: aquí son (5, 5) y 40,016, los valores de partida, lo que significa que ninguna iteración mejoró el inicio. El gradiente se anuló porque los iterados crecieron tanto que el paso numérico se perdió en el redondeo, no porque alcanzaran el mínimo en (1, 1).

**Criterio de aprobación:** Leer μ, L y κ en una hessiana, deducir el umbral 2/L y el mejor paso fijo sobre una cuadrática, enunciar las garantías del descenso de gradiente y qué prueba un gradiente pequeño, explicar las tasas de la inercia de la bola pesada y el paso de Adam, y rastrear cuándo el bucle de IX informa de una convergencia que no ocurrió.

---

## Base de investigación

- H. H. Rosenbrock, «An automatic method for finding the greatest or least value of a function», *The Computer Journal* 3, 1960: el valle en forma de plátano usado como función de prueba
- B. T. Polyak, «Some methods of speeding up the convergence of iteration methods», *USSR Computational Mathematics and Mathematical Physics* 4, 1964: el método de la bola pesada y su tasa sobre cuadráticas
- Y. Nesterov, «A method of solving a convex programming problem with convergence rate O(1/k²)», *Soviet Mathematics Doklady* 27, 1983: los métodos de gradiente acelerado
- S. Boyd y L. Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004: convexidad, convexidad fuerte y convergencia del descenso de gradiente
- J. Nocedal y S. J. Wright, *Numerical Optimization*, 2.ª ed., Springer, 2006: tamaños de paso, búsquedas lineales y gradientes por diferencias finitas
- D. P. Kingma y J. Ba, «Adam: A method for stochastic optimization», *International Conference on Learning Representations*, 2015: Adam, su corrección del sesgo y la cota de su paso
- L. Lessard, B. Recht y A. Packard, «Analysis and design of optimization algorithms via integral quadratic constraints», *SIAM Journal on Optimization* 26, 2016: una función fuertemente convexa sobre la que la bola pesada no converge
- S. J. Reddi, S. Kale y S. Kumar, «On the convergence of Adam and beyond», *International Conference on Learning Representations*, 2018: un problema convexo sobre el que Adam falla, y AMSGrad
- Y. Nesterov, *Lectures on Convex Optimization*, 2.ª ed., Springer, 2018: el lema de descenso y las velocidades de convergencia del §3
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
