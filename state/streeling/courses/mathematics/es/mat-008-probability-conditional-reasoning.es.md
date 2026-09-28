---
module_id: mat-008-probability-conditional-reasoning
department: mathematics
course: Probabilidad y razonamiento condicional
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies, mat-003-floating-point-conditioning]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Probabilidad y razonamiento condicional — Revisar una creencia a la luz de la evidencia

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Enunciar los axiomas de Kolmogórov, y deducir de ellos la regla del complemento y la inclusión–exclusión
- Calcular probabilidades condicionales, y distinguir la independencia de la independencia condicional
- Aplicar el teorema de Bayes, en forma de probabilidades y en forma de momios, y explicar por qué importa la tasa base
- Actualizar una distribución a priori Beta con datos binomiales, y decir qué oculta la media a posteriori
- Decir qué calculan los pesos bayesianos de las reglas de IX y su clasificador bayesiano ingenuo, y dónde fallan

---

## 1. Los axiomas

Un modelo de probabilidad tiene un **espacio muestral** Ω, el conjunto de resultados posibles; **sucesos**, que son subconjuntos de Ω; y una probabilidad P que cumple los **axiomas de Kolmogórov**:
1. P(A) ≥ 0 para todo suceso A.
2. P(Ω) = 1.
3. Para sucesos disjuntos dos a dos A₁, A₂, …, P(A₁ ∪ A₂ ∪ …) = P(A₁) + P(A₂) + ….

Todo lo demás se deduce. Como A y su complemento son disjuntos y llenan Ω, P(no A) = 1 − P(A), y P(∅) = 0. Si A ⊆ B, entonces P(A) ≤ P(B). Partir A ∪ B en trozos disjuntos da la **inclusión–exclusión**: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). Cuando Ω es finito y sus resultados son equiprobables, P(A) = |A|/|Ω|, y calcular una probabilidad es contar.

### Ejercicio práctico

Lanza dos dados equilibrados. Calcula P(la suma es 7) y P(al menos un seis), la segunda de dos maneras.

> *Solución:* Los 36 pares ordenados son equiprobables. La suma es 7 para (1, 6), (2, 5), (3, 4), (4, 3), (5, 2) y (6, 1), así que P = 6/36 = 1/6. Para al menos un seis, el complemento «ningún seis» tiene 5 · 5 = 25 pares, así que P = 1 − 25/36 = 11/36. Por inclusión–exclusión, P(el primero es 6) + P(el segundo es 6) − P(ambos son 6) = 1/6 + 1/6 − 1/36 = 11/36.

---

## 2. Probabilidad condicional e independencia

La **probabilidad condicional** de A dado B, para P(B) > 0, es P(A | B) = P(A ∩ B)/P(B): se restringen los resultados a B y se renormaliza. Da la **regla del producto** P(A ∩ B) = P(A | B) P(B) y, cuando los sucesos B₁, …, B_k parten Ω en trozos disjuntos, la **ley de la probabilidad total** P(A) = P(A | B₁) P(B₁) + … + P(A | B_k) P(B_k).

A y B son **independientes** cuando P(A ∩ B) = P(A) P(B), lo que, para P(B) > 0, significa P(A | B) = P(A): saber B no cambia la probabilidad de A. La independencia no es la disjunción. Dos sucesos disjuntos de probabilidad positiva nunca son independientes, ya que saber uno descarta el otro. A y B son **condicionalmente independientes** dado C cuando P(A ∩ B | C) = P(A | C) P(B | C). Ninguna de las dos independencias implica la otra: dos pruebas al mismo paciente pueden ser condicionalmente independientes dado su estado, y sin embargo dependientes en conjunto, ya que un primer resultado positivo hace más probable la enfermedad, y por tanto un segundo resultado positivo.

### Ejercicio práctico

Con dos dados, sea A el suceso «el primer dado muestra 6». Calcula P(A | la suma es 7), P(A | la suma es 11) y P(A | la suma es 12), y di qué condición deja A independiente.

> *Solución:* P(A) = 1/6. De los 6 pares con suma 7, solo (6, 1) tiene un primer 6, así que P(A | suma 7) = 1/6 = P(A): estos dos sucesos son independientes. La suma es 11 para (5, 6) y (6, 5), así que P(A | suma 11) = 1/2. La suma es 12 solo para (6, 6), así que P(A | suma 12) = 1. Solo la suma 7 deja A independiente.

---

## 3. El teorema de Bayes y las tasas base

Escribir P(H ∩ E) de dos maneras con la regla del producto da el **teorema de Bayes**:

P(H | E) = P(E | H) P(H)/P(E), con P(E) = P(E | H) P(H) + P(E | no H) P(no H).

P(H) es la **probabilidad a priori**, P(E | H) la **verosimilitud** y P(H | E) la **probabilidad a posteriori**. Dividir el teorema para H entre el teorema para «no H» da la **forma de momios**: los momios a posteriori son los momios a priori multiplicados por la **razón de verosimilitud** P(E | H)/P(E | no H). Cuando varias evidencias son condicionalmente independientes dado H y dado «no H», sus razones de verosimilitud se multiplican, y el orden en que llegan no importa.

Una prueba para una afección que afecta al 1% de las personas tiene una sensibilidad P(+ | enfermo) del 99% y una tasa de falsos positivos P(+ | sano) del 5%. Entonces P(+) = 0.99 · 0.01 + 0.05 · 0.99 = 0.0099 + 0.0495 = 0.0594, y P(enfermo | +) = 0.0099/0.0594 = 1/6. Tras un resultado positivo en una prueba sensible al 99%, quedan cinco posibilidades de seis de que la persona esté sana, porque las personas sanas son 99 veces más numerosas. Ignorar así la probabilidad a priori es la **falacia de la tasa base**.

### Ejercicio práctico

La misma persona se hace una segunda prueba, condicionalmente independiente de la primera dado su estado, y también da positivo. Usa la forma de momios para actualizar.

> *Solución:* Tras la primera prueba, P(enfermo) = 1/6, es decir, momios de 1 a 5. La razón de verosimilitud de un resultado positivo es 0.99/0.05 = 19.8. Los momios a posteriori son 19.8/5 = 3.96, así que P(enfermo | dos positivos) = 3.96/4.96 = 99/124, unos 0.80. El teorema de Bayes con la probabilidad a priori 1/6 da el mismo número.

---

## 4. La conjugación: el modelo Beta–binomial

Sea θ una probabilidad de éxito desconocida. La distribución **Beta(α, β)**, para α, β > 0, tiene una densidad proporcional a θ^(α−1) (1 − θ)^(β−1) en [0, 1]; Beta(1, 1) es la distribución uniforme. Tras s éxitos y f fracasos, la verosimilitud es proporcional a θ^s (1 − θ)^f, así que la distribución a posteriori es proporcional a θ^(α+s−1) (1 − θ)^(β+f−1): es Beta(α + s, β + f). Una distribución a priori cuya distribución a posteriori se queda en la misma familia es **conjugada**, y aquí α y β actúan como pseudoconteos de éxitos y fracasos. La media a posteriori es (α + s)/(α + β + s + f), y Beta(a, b) tiene la varianza ab/((a + b)² (a + b + 1)).

Como la actualización solo suma conteos, la distribución a posteriori depende de los datos solo a través de s y f: las actualizaciones **conmutan**, y una observación cada vez da la misma distribución a posteriori que todas a la vez. La media sola oculta cuánto se sabe. Beta(2, 2) y Beta(501, 501) tienen ambas la media 1/2, pero sus varianzas son 1/20 y unos 2.5 · 10^-4. Una regla que debe seguir explorando las opciones inciertas, como el **muestreo de Thompson**, que extrae θ de cada distribución a posteriori y elige la mayor extracción, necesita toda la distribución, no solo su media.

### Ejercicio práctico

Parte de Beta(1, 1) y observa 3 éxitos y 1 fracaso. Da la distribución a posteriori, su media y su varianza.

> *Solución:* Beta(1 + 3, 1 + 1) = Beta(4, 2), con media 4/6 = 2/3 y varianza 4 · 2/(6² · 7) = 8/252 = 2/63.

---

## 5. Bayes ingenuo y cálculo en escala logarítmica

El teorema de Bayes clasifica: P(clase c | x) es proporcional a P(c) p(x | c). El **bayesiano ingenuo** supone que las variables x₁, …, x_p son condicionalmente independientes dada la clase, de modo que p(x | c) = p(x₁ | c) · … · p(x_p | c). El **bayesiano ingenuo gaussiano** modela cada p(x_j | c) con una densidad normal, con una media y una varianza por clase estimadas con los datos de entrenamiento.

Dos puntos numéricos deciden si esto funciona. Primero, un producto de muchas densidades pequeñas sufre subdesbordamiento, así que el cálculo suma log-probabilidades en su lugar, y normaliza con el truco **log-sum-exp**: restar la mayor puntuación logarítmica antes de exponenciar, lo que no cambia los cocientes y hace que el mayor término sea exp(0) = 1. Segundo, la fórmula de varianza E[x²] − E[x]² resta dos números casi iguales cuando la media es grande frente a la dispersión, y la cancelación de MAT-003 destruye la diferencia. Restar primero la media, la fórmula **de dos pasadas** media((x − x̄)²), o la actualización de una pasada de Welford lo evitan.

### Ejercicio práctico

Dos clases tienen las puntuaciones logarítmicas −1000 y −1002. ¿Qué falla si las exponencias directamente, y qué probabilidades da log-sum-exp?

> *Solución:* e^-1000 está por debajo del menor número binary64 positivo, unos 4.9 · 10^-324, así que ambas exponenciales se redondean a 0 y la normalización es 0/0. Restar el máximo da exp(0) = 1 y e^-2, así que las probabilidades son 1/(1 + e^-2) ≈ 0.881 y 0.119.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**Los pesos bayesianos de las reglas** (`crates/ix-grammar/src/weighted.rs`). Una `WeightedRule` parte de la [distribución a priori uniforme Beta(1, 1)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L31) y guarda como peso la [media de la distribución Beta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L13). [`bayesian_update`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L57) es la actualización conjugada del §4, literal en las líneas 57 a 66:

```rust
pub fn bayesian_update(rule: &WeightedRule, success: bool) -> WeightedRule {
    let mut updated = rule.clone();
    if success {
        updated.alpha += 1.0;
    } else {
        updated.beta += 1.0;
    }
    updated.weight = updated.alpha / (updated.alpha + updated.beta);
    updated
}
```

- **La actualización es correcta y conmuta exactamente.** Los conteos son números enteros, exactos en binary64 hasta 2^53, así que cualquier orden de las mismas observaciones da los mismos α, β y peso, bit a bit. [`test_bayesian_update_success`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L145) comprueba un éxito a partir de Beta(1, 1).
- **La selección solo ve la media, a través de un softmax plano.** [`softmax`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L83) da a cada regla una probabilidad proporcional a exp(peso/T), y [`select_weighted`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L111) muestrea con T = 1. Los pesos están entre 0 y 1, así que con T = 1 ninguna regla es más de e ≈ 2.72 veces más probable que otra: una regla de peso 0.99 frente a una regla de peso 0.01 se elige con la probabilidad 1/(1 + e^-0.98) ≈ 0.727. Beta(2, 2) y Beta(501, 501) dan el mismo peso, así que una regla probada dos veces y una regla probada mil veces se tratan igual; esto no es muestreo de Thompson.
- **La herramienta MCP se fía de su entrada.** El manejador de `ix_grammar_weights` lee [`alpha`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1559) y `beta` sin comprobar que sean positivos, como exige una distribución Beta, y acepta un [`weight`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1561) que puede contradecirlos; el softmax usa ese peso para toda regla que la petición no actualiza. Su temperatura [vale 1 por defecto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1601).

**El bayesiano ingenuo** (`crates/ix-supervised/src/naive_bayes.rs`). `GaussianNaiveBayes` trabaja en escala logarítmica y resta la [mayor puntuación logarítmica](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L101) antes de exponenciar, como recomienda el §5. Su varianza es la otra fórmula del §5, literal en las líneas 52 a 59:

```rust
            let mean = class_data.mean_axis(ndarray::Axis(0)).unwrap();
            let var = class_data
                .mapv(|v| v * v)
                .mean_axis(ndarray::Axis(0))
                .unwrap()
                - &mean.mapv(|v| v * v);
            // Add small epsilon to avoid division by zero
            let var = var.mapv(|v| v.max(1e-9));
```

- **La varianza se cancela con variables desplazadas.** Para los datos de clase c + (0, 1, 2), de varianza 2/3, una transcripción de estas líneas, con las sumas secuenciales que `ndarray` usa para menos de 8 filas, predice la varianza calculada 0.671875 en c = 10^7, 2 en c = 10^8, y exactamente 0 en c = 10^9. La función `var_axis` del crate `ndarray` usa la actualización de Welford.
- **El piso es absoluto.** Una varianza calculada de 0 o menos pasa a ser 10^-9, sea cual sea la escala de la variable, como los umbrales absolutos de MAT-003. En c = 10^9, convierte el 0 calculado en 10^-9 donde la varianza verdadera es 2/3, y el clasificador se vuelve seguro.
- **Una clase ausente entra en pánico.** `fit` fija el número de clases en [la mayor etiqueta más uno](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L37). Si una etiqueta menor no tiene ningún ejemplo, esa clase no tiene filas, `mean_axis` devuelve `None` para un eje vacío, y el [`unwrap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L52) entra en pánico.
- **La prueba se queda en el caso fácil.** [`test_gaussian_nb`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L127) ajusta seis puntos bien separados cerca del origen y comprueba una exactitud de entrenamiento superior a 0.8. No comprueba ninguna probabilidad, ningún desplazamiento y ninguna etiqueta ausente.

**A través del servidor MCP.** La operación `naive_bayes` de `ix_supervised` convierte las etiquetas con [`as usize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2615), que trunca 1.5 a 1 y satura −1 a 0, y llama a `fit` sin protección. La herramienta se declara como el skill [`supervised`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L665), y [cada skill del registro](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L320) se convierte en una herramienta MCP respaldada por el registro, cuyas llamadas se ejecutan mientras `dispatch_action` mantiene un `Mutex` global. La lectura de este código predice que un pánico en `fit` deja la llamada sin respuesta y envenena ese mutex, tras lo cual cada llamada respaldada por el registro entra en pánico en el [`expect`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L238) del cerrojo, hasta que el servidor se reinicia. Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Para las clases c + (0, 1, 2) y c + (4, 5, 6) y el punto c + 2.5, la probabilidad a posteriori exacta de la primera clase es 1/(1 + e^-3) ≈ 0.953. Con las varianzas calculadas arriba, predice qué devuelve `predict_proba` en c = 10^8 y en c = 10^9.

> *Solución:* Ambas clases reciben la misma varianza calculada v, así que los términos de normalización se cancelan y solo cuentan las distancias al cuadrado: 1.5² = 2.25 hasta la primera media y 2.5² = 6.25 hasta la segunda, ya que las medias c + 1 y c + 5 se calculan exactamente aquí. La diferencia entre las puntuaciones logarítmicas es (6.25 − 2.25)/(2v) = 2/v, que vale 3 para la v verdadera, 2/3. En c = 10^8, v = 2 da la diferencia 1 y la probabilidad 1/(1 + e^-1) ≈ 0.731. En c = 10^9, v = 10^-9 da la diferencia 2 · 10^9, e^(−2 · 10^9) sufre subdesbordamiento a 0, y la probabilidad es exactamente 1. La primera respuesta es demasiado dudosa y la segunda segura; ambas vienen de la varianza, no de los datos. Es una predicción obtenida leyendo el código, no una ejecución; el §7 la comprueba.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **La conmutación.** Aplica `bayesian_update` desde Beta(1, 1) a las mismas 10^3 observaciones en tres órdenes: tal como se registraron, al revés, y todos los éxitos primero. Predicción: α, β y peso idénticos, bit a bit.
2. **El softmax plano.** Construye dos reglas con α, β = 99, 1 y 1, 99, de pesos 0.99 y 0.01, y llama a `select_weighted` 10^5 veces con un generador de semilla fija. Predicción: la frecuencia de la primera regla es 0.727 con un margen de 0.005.
3. **El barrido de desplazamientos.** Para c = 10^0, …, 10^9, ajusta `GaussianNaiveBayes` sobre las clases c + (0, 1, 2) y c + (4, 5, 6), y llama a `predict_proba` en c + 2.5. Predicción: a menos de 10^-4 de 0.9526 para c ≤ 10^6, unos 0.9515 en c = 10^7, unos 0.7311 en c = 10^8, y exactamente 1 en c = 10^9. Restar primero a cada valor la media de la variable de entrenamiento, c + 3, da 0.9526 para todo c.
4. **La clase ausente.** Llama a `fit` con las etiquetas (0, 0, 2, 2). Predicción: el pánico «called `Option::unwrap()` on a `None` value». Luego, en un proceso `ix-mcp` desechable, nunca en uno compartido, envía a `ix_supervised` la operación `naive_bayes` con esas etiquetas, seguida de una llamada `ix_stats` bien planteada. Predicción: ninguna de las dos llamadas recibe respuesta, y la salida de error del servidor muestra ese pánico, y luego «middleware chain mutex poisoned».

### Ejercicio práctico

El paso 2 predice 0.727 con un margen de 0.005 para 10^5 extracciones. ¿De dónde sale ese margen?

> *Solución:* Cada extracción elige la primera regla con la probabilidad p ≈ 0.727, independientemente de las demás, así que el conteo es binomial y la frecuencia tiene la desviación típica √(p (1 − p)/n) = √(0.727 · 0.273/10^5) ≈ 0.0014. Tres desviaciones típicas, unos 0.0042, caben en 0.005. Esto supone que el generador se comporta como extracciones uniformes independientes; la semilla hace la ejecución reproducible, no más aleatoria.

---

## 8. Errores comunes

- **Confundir P(E | H) con P(H | E).** La sensibilidad de una prueba no es la probabilidad de la enfermedad tras un resultado positivo.
- **Ignorar la tasa base.** La misma evidencia mueve mucho menos una hipótesis rara que una común.
- **Tratar sucesos disjuntos como independientes.** Los sucesos disjuntos de probabilidad positiva siempre son dependientes.
- **Multiplicar razones de verosimilitud de evidencias dependientes.** Dos resultados solo se multiplican si son condicionalmente independientes dada cada hipótesis.
- **Dar una media a posteriori sin su dispersión.** Beta(2, 2) y Beta(501, 501) tienen la misma media; lo que se sabe no es lo mismo.
- **Calcular una varianza como E[x²] − E[x]².** Resta primero la media.
- **Multiplicar directamente muchas probabilidades pequeñas.** Suma sus logaritmos, y normaliza con log-sum-exp.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Espacio muestral** | El conjunto Ω de resultados posibles; los sucesos son sus subconjuntos |
| **Axiomas de Kolmogórov** | P(A) ≥ 0, P(Ω) = 1, y la aditividad sobre sucesos disjuntos |
| **Probabilidad condicional** | P(A \| B) = P(A ∩ B)/P(B), para P(B) > 0 |
| **Independencia** | P(A ∩ B) = P(A) P(B): saber uno de los sucesos no cambia la probabilidad del otro |
| **Independencia condicional** | P(A ∩ B \| C) = P(A \| C) P(B \| C) |
| **Teorema de Bayes** | P(H \| E) = P(E \| H) P(H)/P(E) |
| **Razón de verosimilitud** | P(E \| H)/P(E \| no H), el factor por el que una evidencia multiplica los momios de H |
| **Falacia de la tasa base** | Juzgar P(H \| E) a partir de P(E \| H) ignorando la probabilidad a priori P(H) |
| **Distribución a priori conjugada** | Una distribución a priori cuya distribución a posteriori se queda en la misma familia, como Beta para datos binomiales |
| **Bayesiano ingenuo** | Un clasificador que supone las variables condicionalmente independientes dada la clase |
| **Log-sum-exp** | Normalizar puntuaciones logarítmicas restando su máximo antes de exponenciar |

---

## Autoevaluación

**1. ¿Por qué dos sucesos disjuntos de probabilidad positiva no pueden ser independientes?**
> P(A ∩ B) = P(∅) = 0, mientras que P(A) P(B) > 0.

**2. Una prueba tiene una sensibilidad del 99%. ¿Por qué la probabilidad de la enfermedad tras un resultado positivo no es del 99%?**
> La probabilidad a posteriori depende también de la probabilidad a priori y de la tasa de falsos positivos. Con una prevalencia del 1% y una tasa de falsos positivos del 5%, es 1/6: la mayoría de los resultados positivos vienen de las muchas personas sanas.

**3. ¿Por qué conmutan las actualizaciones Beta–binomiales?**
> La distribución a posteriori Beta(α + s, β + f) depende de los datos solo a través de los números de éxitos s y de fracasos f, que no dependen del orden de las observaciones.

**4. La prueba `test_gaussian_nb` de IX pasa. ¿Qué te dice sobre variables desplazadas?**
> Nada: sus puntos están cerca del origen, donde E[x²] − E[x]² no pierde nada. La cancelación necesita una media grande frente a la dispersión de la clase.

**Criterio de aprobación:** Deducir consecuencias de los axiomas de Kolmogórov, calcular probabilidades condicionales y comprobar una independencia, aplicar el teorema de Bayes en sus dos formas con una tasa base, actualizar una distribución a priori Beta y dar su media y su varianza, normalizar puntuaciones logarítmicas con log-sum-exp, y seguir lo que calculan los pesos de las reglas y el bayesiano ingenuo de IX y dónde fallan.

---

## Base de investigación

- A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung*, Springer, 1933: los axiomas
- J. K. Blitzstein y J. Hwang, *Introduction to Probability*, 2.ª ed., CRC Press, 2019: la probabilidad condicional, el teorema de Bayes y el modelo Beta–binomial
- E. T. Jaynes, *Probability Theory: The Logic of Science*, Cambridge University Press, 2003: la probabilidad como lógica extendida, y la forma de momios del teorema de Bayes
- D. Kahneman y A. Tversky, «On the psychology of prediction», *Psychological Review* 80, 1973: el descuido de las tasas base
- W. R. Thompson, «On the likelihood that one unknown probability exceeds another in view of the evidence of two samples», *Biometrika* 25, 1933: el muestreo de Thompson
- B. P. Welford, «Note on a method for calculating corrected sums of squares and products», *Technometrics* 4, 1962: una varianza estable de una pasada
- T. F. Chan, G. H. Golub y R. J. LeVeque, «Algorithms for computing the sample variance: analysis and recommendations», *The American Statistician* 37, 1983: por qué falla E[x²] − E[x]²
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
