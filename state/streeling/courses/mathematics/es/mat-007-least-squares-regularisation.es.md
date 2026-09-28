---
module_id: mat-007-least-squares-regularisation
department: mathematics
course: Mínimos cuadrados, regularización e identificabilidad
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-003-floating-point-conditioning, mat-006-svd-low-rank-approximation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Mínimos cuadrados, regularización e identificabilidad — Cuando los datos no bastan para fijar los parámetros

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Deducir las ecuaciones normales de la ortogonalidad del residuo, y resolver a mano un pequeño ajuste por mínimos cuadrados
- Decir cuándo los parámetros de un modelo lineal son identificables, y encontrar la solución de norma mínima cuando no lo son
- Explicar por qué resolver las ecuaciones normales pierde el doble de cifras que una resolución por la SVD, y por qué centrar una variable ayuda
- Escribir la solución ridge (Tikhonov) con la SVD, y explicar por qué es única para todo λ positivo
- Decir qué calcula la regresión lineal de IX, dónde falla, y qué hace su fallo a los procesos que la llaman

---

## 1. El problema de mínimos cuadrados

Un modelo lineal predice y a partir de variables: y ≈ X w, donde la **matriz de diseño** X, de tamaño n × p, tiene una fila por observación y una columna por parámetro. Con más observaciones que parámetros, las ecuaciones X w = y en general no tienen solución. Los **mínimos cuadrados** eligen el w que minimiza la longitud del **residuo** r = y − X w, es decir ‖X w − y‖₂.

Los vectores X w llenan el espacio de columnas de X, y el más cercano a y es su proyección ortogonal: el residuo del mejor w es ortogonal a cada columna de X. Es decir, Xᵀ(y − X w) = 0, las **ecuaciones normales**

XᵀX w = Xᵀy.

Recíprocamente, todo w que las cumple minimiza el residuo: para cualquier otro w′, X(w′ − w) está en el espacio de columnas, así que ‖X w′ − y‖² = ‖X (w′ − w)‖² + ‖X w − y‖² por Pitágoras.

### Ejercicio práctico

Ajusta la recta y = a + b x a los puntos (0, 0), (1, 1) y (2, 3).

> *Solución:* Las filas de X son (1, 0), (1, 1) y (1, 2), e y = (0, 1, 3). Entonces XᵀX = [[3, 3], [3, 5]] y Xᵀy = (4, 7). El determinante es 15 − 9 = 6, así que (a, b) = (1/6) · (5 · 4 − 3 · 7, −3 · 4 + 3 · 7) = (−1/6, 3/2). Los valores ajustados son −1/6, 4/3 y 17/6, y el residuo es (1/6, −1/3, 1/6): su suma es 0 y 0 · 1/6 + 1 · (−1/3) + 2 · 1/6 = 0, así que es ortogonal a ambas columnas.

---

## 2. Identificabilidad

Los parámetros son **identificables** cuando los datos los determinan: cuando la solución de mínimos cuadrados es única. Eso ocurre exactamente cuando X tiene **rango de columnas completo**. Si X v = 0 para algún v ≠ 0, entonces w + t v se ajusta exactamente igual de bien que w para todo t, y los datos no pueden distinguir esos vectores de parámetros. Si en cambio X v = 0 solo para v = 0, entonces vᵀXᵀX v = ‖X v‖² > 0 para todo v ≠ 0, así que XᵀX es invertible y las ecuaciones normales tienen una sola solución.

Las causas típicas de un rango deficiente son una variable que duplica otra, una variable que es combinación de otras, una variable constante junto al sesgo, y menos observaciones que parámetros. Cuando el rango es deficiente, todavía se puede elegir una respuesta: la **solución de norma mínima** w⁺ = X⁺y, con la pseudoinversa de MAT-006 §4, es la solución de mínimos cuadrados de menor longitud. No tiene ninguna componente en las direcciones que los datos no ven.

### Ejercicio práctico

Con X = [[1, 2], [1, 2]] e y = (3, 3), describe todas las soluciones de mínimos cuadrados, y da la de norma mínima.

> *Solución:* Ambas filas dicen w₁ + 2 w₂ = 3, así que cada punto de esa recta se ajusta exactamente, con residuo 0; la dirección (2, −1) cumple X (2, −1) = 0 y no se puede ver. La solución más corta es ortogonal a (2, −1), así que es múltiplo de (1, 2): t (1, 2) con t + 4 t = 3, es decir w⁺ = (3/5, 6/5), de longitud al cuadrado 9/25 + 36/25 = 9/5.

---

## 3. Condicionamiento: por qué no las ecuaciones normales

Los valores singulares de XᵀX son los cuadrados de los de X (MAT-006), así que κ₂(XᵀX) = κ₂(X)² cuando X tiene rango de columnas completo. Según la regla práctica de MAT-003, una resolución por las ecuaciones normales puede perder unas 2 log₁₀ κ₂(X) cifras. Una resolución por la SVD, w = V Σ⁻¹ Uᵀ y para rango de columnas completo, o por una factorización QR, trabaja sobre la propia X y pierde unas log₁₀ κ₂(X) cuando el residuo es pequeño. Cuando el residuo es grande, el propio problema de mínimos cuadrados contiene un término en κ², y ningún algoritmo lo evita.

Formar XᵀX puede incluso destruir la información por completo. La **matriz de Läuchli** X = [[1, 1], [δ, 0], [0, δ]] tiene los valores singulares √(2 + δ²) y δ, así que tiene rango completo para todo δ ≠ 0. Pero XᵀX = [[1 + δ², 1], [1, 1 + δ²]], y para δ = 10^-8, δ² = 10^-16 está por debajo de la mitad del épsilon de máquina de MAT-003: fl(1 + δ²) = 1, y la XᵀX almacenada es [[1, 1], [1, 1]], exactamente singular. La SVD de X sigue encontrando δ.

El condicionamiento también depende de cómo se escribe el modelo. Toma la variable x = c + (0, 1, 2) con un sesgo. Para c = 0 el problema es dócil; para c grande, la columna x es casi paralela a la columna de unos, y el segundo pivote de XᵀX cae como 2/c². Restar la media de la variable, el **centrado**, elimina el problema: con x − x̄ = (−1, 0, 1), XᵀX = diag(2, 3). La recta ajustada es la misma, escrita alrededor de x̄ en lugar de 0.

### Ejercicio práctico

Para x = c + (0, 1, 2) con una columna de sesgo, demuestra que eliminar la primera columna de XᵀX deja el segundo pivote 6/(3c² + 6c + 5).

> *Solución:* XᵀX = [[Σx², Σx], [Σx, 3]] con Σx = 3c + 3 y Σx² = c² + (c + 1)² + (c + 2)² = 3c² + 6c + 5. El segundo pivote es 3 − (Σx)²/Σx² = (3 (3c² + 6c + 5) − (3c + 3)²)/Σx² = (9c² + 18c + 15 − 9c² − 18c − 9)/Σx² = 6/(3c² + 6c + 5), unos 2/c² para c grande.

---

## 4. Regresión ridge

La **regresión ridge**, o **regularización de Tikhonov**, minimiza ‖X w − y‖² + λ ‖w‖² para un λ > 0 elegido. Anular el gradiente da (XᵀX + λI) w = Xᵀy. XᵀX es semidefinida positiva, ya que vᵀXᵀX v = ‖X v‖² ≥ 0 (§2), así que cada valor propio de XᵀX + λI es al menos λ > 0, y la solución es única para todo λ > 0, incluso cuando X tiene rango deficiente. Con la SVD de MAT-006,

w_λ = Σᵢ σᵢ/(σᵢ² + λ) (uᵢ · y) vᵢ.

Comparada con la pseudoinversa, que multiplica uᵢ · y por 1/σᵢ, la ridge lo multiplica por el **factor de filtro** σᵢ²/(σᵢ² + λ): cercano a 1 cuando σᵢ² ≫ λ, cercano a 0 cuando σᵢ² ≪ λ. Por tanto, la ridge amortigua las direcciones que los datos apenas determinan en lugar de cortarlas en una tolerancia, y w_λ tiende a X⁺y cuando λ tiende a 0. El precio es una estimación sesgada hacia 0. El término de sesgo del modelo suele dejarse fuera de la penalización, y las variables se centran primero, para que la contracción no dependa de dónde está el origen.

### Ejercicio práctico

Para X = [[1, 2], [1, 2]] e y = (3, 3) del §2, calcula la solución ridge w_λ, y comprueba su límite cuando λ tiende a 0.

> *Solución:* XᵀX = [[2, 4], [4, 8]] y Xᵀy = (6, 12). Prueba w = α (1, 2): la primera ecuación da (2 + λ) α + 8 α = 6, así que α = 6/(10 + λ), y la segunda da 4 α + 2 (8 + λ) α = 12, el mismo α. Así que w_λ = (6/(10 + λ)) (1, 2), por ejemplo (1/2, 1) para λ = 2. Cuando λ tiende a 0, w_λ tiende a (3/5, 6/5), la solución de norma mínima del §2.

---

## 5. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**El ajuste** (`crates/ix-supervised/src/linear_regression.rs`). [`LinearRegression::fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L57) añade una columna de unos para el sesgo y resuelve las ecuaciones normales con una inversa explícita, literal en las líneas 57 a 74:

```rust
    fn fit(&mut self, x: &Array2<f64>, y: &Array1<f64>) {
        let n = x.nrows();
        // Add bias column (column of ones)
        let ones = Array2::ones((n, 1));
        let x_aug = ndarray::concatenate(Axis(1), &[x.view(), ones.view()]).unwrap();

        // Normal equation: w = (X^T X)^{-1} X^T y
        let xtx = x_aug.t().dot(&x_aug);
        let xty = x_aug.t().dot(y);

        // Solve via inverse (fine for small/medium datasets)
        let xtx_inv = ix_math::linalg::inverse(&xtx).expect("X^T X is singular");
        let w = xtx_inv.dot(&xty);

        let p = x.ncols();
        self.weights = Some(w.slice(ndarray::s![..p]).to_owned());
        self.bias = w[p];
    }
```

Tres consecuencias se siguen del §3 y de MAT-003:
- **Eleva al cuadrado el número de condición.** Cada ajuste paga κ₂(X)², y la columna de sesgo vuelve casi colineal con ella una variable desplazada.
- **Su veredicto depende de la escala y del desplazamiento.** [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L83) responde `Singular` cuando un pivote cae [por debajo de 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L110), un umbral absoluto (MAT-003). Para x = c + (0, 1, 2), el segundo pivote 6/(3c² + 6c + 5) cae por debajo en cuanto c supera unos 1.41 · 10^6, así que tres lecturas de una marca de tiempo Unix en segundos, del orden de 10^9, tomadas con un segundo de separación, hacen fallar el ajuste aunque el diseño tenga rango completo. Por debajo de ese punto, el ajuste termina sin error, por muchas cifras que se pierdan; el ejercicio al final de esta sección muestra cuántas.
- **Entra en pánico.** El `expect` de la línea 68 convierte `Singular` en un pánico, y los llamadores lo manejan de forma distinta.

**Lo que el pánico hace a los llamadores.** [`ix-duck`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L111) documenta el pánico y [lo captura](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L114), devolviendo un error SQL. El manejador de la herramienta MCP `ix_linear_regression` llama a [`fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L285) sin esa protección, igual que el [pipeline de ML](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/ml_pipeline.rs#L791). El servidor MCP ejecuta cada [`tools/call`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/main.rs#L175) en su propio hilo de trabajo, que escribe la respuesta solo [después de que el manejador retorna](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/main.rs#L184). `ix_linear_regression` pasa por el registro, como la mayoría de las herramientas básicas según un [comentario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/tools.rs#L1292) de `tools.rs`, y las llamadas que pasan por el registro atraviesan `dispatch_action`, que mantiene un cerrojo global mientras la herramienta se ejecuta, literal en las líneas 236 a 243 de `crates/ix-agent/src/registry_bridge.rs`:

```rust
    let chain_guard = middleware_chain()
        .lock()
        .expect("middleware chain mutex poisoned");

    let result = {
        let mut wc = WriteContext { read: cx, sink };
        chain_guard.dispatch(&mut wc, action, &RegistryLookupHandler)
    };
```

La lectura de este código predice tres efectos de una sola petición que hace entrar en pánico a `fit`:
1. El hilo de trabajo termina sin escribir una respuesta, así que el cliente espera una respuesta que nunca llega.
2. El pánico se propaga mientras `chain_guard` está tomado, y un `Mutex` de Rust queda **envenenado** cuando un hilo entra en pánico mientras lo tiene.
3. A partir de entonces, cada llamada que pasa por el registro entra en pánico en el `expect` de la [línea 238](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L238), y tampoco recibe respuesta, hasta que el servidor se reinicia.

Dos hechos más:
- **Su esquema nombra la clave equivocada.** El esquema de entrada publicado de `ix_linear_regression` exige [`"X"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L839), mientras que el manejador lee [`"x"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L270). Las claves JSON distinguen mayúsculas de minúsculas, así que se predice que un cliente que siga el esquema reciba el error «Missing or invalid field 'x'». La demo de IX envía `"x"`, y su [comentario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/demo/scenarios/sprint_oracle.rs#L71) lo dice.
- **Las pruebas se quedan en los casos fáciles.** [`test_linear_regression_multivariate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L152) ajusta datos exactos sobre los cuatro puntos de {1, 2}², un diseño bien condicionado, con una tolerancia de 10^-6. `ix-duck` [comprueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L283) que columnas exactamente colineales dan un error SQL en lugar de un pánico. Ninguna prueba cubre un desplazamiento o un diseño casi colineal, donde el ajuste termina sin error.

Los crates `ix-supervised` e `ix-math` de IX no tienen regresión ridge ni lasso, ni factorización QR. La vía SVD del §3 está disponible mediante [`pseudo_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73), con las salvedades de MAT-006, e IX ya tiene una prueba de rango relativa, [`RankReport.deficiency`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L356), en `ix-signal`, que un ajuste podría consultar antes de resolver. Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Predice qué devuelve `fit` para x = c + (0, 1, 2) e y = 2x + 1, cuya respuesta exacta es la pendiente 2 y el sesgo 1, para c = 10^6 y para c = 10^7.

> *Solución:* Para c = 10^7, el segundo pivote vale unos 2/c² = 2 · 10^-14, por debajo de 10^-12, así que `inverse` responde `Singular` y `fit` entra en pánico. Para c = 10^6 vale unos 2 · 10^-12, justo por encima del umbral, así que `fit` termina. Su respuesta la decide el redondeo en un pivote tan pequeño frente a entradas del orden de 3 · 10^12: κ₂(XᵀX) vale unos 1.5 · 10^24, mucho más de lo que binary64 puede resolver. Aquí las entradas de XᵀX y de Xᵀy son enteros menores que 2^53, así que son exactas, y una transcripción de `inverse` predice la pendiente 2 + 2^-11 = 2.00048828125 y el sesgo exactamente 0. Los valores ajustados en los datos quedan entonces desviados en unos 487, sin que se señale ningún error. Es una predicción obtenida leyendo el código, no una ejecución; el §6 la comprueba.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **El barrido de desplazamientos.** Para c = 10^0, 10^1, …, 10^7, ajusta x = c + (0, 1, 2), y = 2x + 1 con `LinearRegression`, capturando el pánico en el arnés del laboratorio. Predicción: la pendiente está a menos de 10^-9 de 2 para c ≤ 10^3; en c = 10^5, la pendiente es 2 − 2^-18 y el sesgo 1.5; en c = 10^6, la pendiente es 2 + 2^-11 y el sesgo 0; en c = 10^7, `fit` entra en pánico con «X^T X is singular». Sobre la variable centrada (−1, 0, 1), los mismos datos dan la pendiente exactamente 2 y el sesgo 2c + 3, el valor ajustado en x̄, con un error relativo de 10^-15 como máximo, para todo c.
2. **Ecuaciones normales frente a la SVD.** Toma x₁ = N · (1, 2, 3, 4), x₂ = x₁ + (1, −1, −1, 1) e y = x₁ + x₂ + 1, de modo que los pesos exactos son 1, 1 y 1, y κ₂ crece como 10 N. Para N = 10^0, …, 10^7, compara `fit` con la vía SVD: `pseudo_inverse` del diseño con su columna de unos, con la tolerancia max(m, n) · σ₁ · ε de MAT-006, aplicada a y. Predicción: el mayor error en los pesos de `fit` está por debajo de 10^-9 para N ≤ 10^3, es de unos 3 · 10^-5 en N = 10^5 y de unos 0.25 en N = 10^7, sin que se señale ningún error; la vía SVD se queda por debajo de 10^-7 para todo N.
3. **El servidor MCP tras un pánico.** En un proceso `ix-mcp` desechable, nunca en uno compartido, envía a `ix_linear_regression` los datos del paso 1 con c = 10^7, y luego una llamada `ix_stats` bien planteada. Predicción: ninguna de las dos llamadas recibe respuesta, y la salida de error del servidor muestra el pánico «X^T X is singular», y luego «middleware chain mutex poisoned».
4. **El esquema.** Envía a `ix_linear_regression` datos bien planteados bajo la clave `"X"`, como exige el esquema. Predicción: el error «Missing or invalid field 'x'».

### Ejercicio práctico

El paso 2 predice un error de unos 0.25 para las ecuaciones normales en N = 10^7, mientras que la vía SVD se queda por debajo de 10^-7. Estima ambos a partir del número de condición.

> *Solución:* κ₂ del diseño vale unos 10 N = 10^8. Las ecuaciones normales trabajan con κ₂² ≈ 10^16, y 10^16 por ε ≈ 2.2 · 10^-16 es de orden 1: ninguna cifra está garantizada, y un error de 0.25 está dentro de esa cota. La vía SVD trabaja con κ₂ ≈ 10^8, lo que predice un error de unos 10^8 · 2.2 · 10^-16 ≈ 2 · 10^-8, coherente con quedarse por debajo de 10^-7. Son órdenes de magnitud según la regla práctica de MAT-003, no cotas.

---

## 7. Errores comunes

- **Resolver mínimos cuadrados con una inversa explícita de XᵀX.** Eleva al cuadrado el número de condición; resuelve por QR o por la SVD.
- **Ajustar desplazamientos en bruto.** Marcas de tiempo, coordenadas y otras variables lejos de 0 en comparación con su dispersión vuelven la columna de sesgo casi colineal con ellas; céntralas primero.
- **Tomar «ningún error» por «un ajuste correcto».** En c = 10^6, se predice que `fit` devuelve una respuesta equivocada sin ningún aviso.
- **Dejar que un fallo numérico entre en pánico en un servidor.** Devuelve un error en su lugar, y nunca dejes que un pánico se propague mientras se tiene un cerrojo: el cerrojo queda envenenado para todos los llamadores siguientes.
- **Regularizar el sesgo.** La penalización debe contraer las pendientes, no el nivel de los datos.
- **Fiarse de un esquema sin una llamada que lo use.** Un esquema y un manejador pueden discrepar en una sola letra.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Matriz de diseño** | La matriz X de tamaño n × p, con una fila por observación y una columna por parámetro |
| **Residuo** | r = y − X w, lo que el modelo deja sin explicar |
| **Ecuaciones normales** | XᵀX w = Xᵀy: el residuo es ortogonal a cada columna de X |
| **Identificabilidad** | Los datos determinan los parámetros de forma única: X tiene rango de columnas completo |
| **Solución de norma mínima** | w⁺ = X⁺y, la solución de mínimos cuadrados más corta |
| **Matriz de Läuchli** | [[1, 1], [δ, 0], [0, δ]]: de rango completo, pero fl(XᵀX) es singular para δ pequeño |
| **Centrado** | Restar la media de una variable antes del ajuste, para que sea ortogonal a la columna de sesgo |
| **Regresión ridge (Tikhonov)** | Minimizar ‖X w − y‖² + λ ‖w‖², con la solución única (XᵀX + λI)⁻¹Xᵀy |
| **Factor de filtro** | σᵢ²/(σᵢ² + λ), el peso que la ridge da a la i-ésima dirección singular |
| **Envenenamiento de un mutex** | El estado de un cerrojo de Rust después de que un hilo entró en pánico mientras lo tenía; las llamadas posteriores a `lock` devuelven un error |

---

## Autoevaluación

**1. ¿Por qué formar XᵀX eleva al cuadrado el número de condición?**
> Los valores singulares de XᵀX son los σᵢ², así que para X de rango de columnas completo κ₂(XᵀX) = σ_max²/σ_min² = κ₂(X)².

**2. ¿Por qué la solución de mínimos cuadrados es única exactamente cuando X tiene rango de columnas completo?**
> Si X v = 0 con v ≠ 0, entonces w + t v se ajusta igual de bien que w para todo t. Si X v = 0 solo para v = 0, entonces vᵀXᵀX v = ‖X v‖² > 0, así que XᵀX es invertible y las ecuaciones normales tienen exactamente una solución.

**3. ¿Por qué la ridge tiene una solución única para todo λ > 0, incluso cuando X tiene rango deficiente?**
> XᵀX es semidefinida positiva, ya que vᵀXᵀX v = ‖X v‖² ≥ 0, así que cada valor propio de XᵀX + λI es al menos λ > 0, y la matriz es invertible.

**4. La prueba `test_linear_regression_multivariate` de IX pasa. ¿Qué te dice sobre datos desplazados o colineales?**
> Nada: ajusta datos exactos sobre los cuatro puntos de {1, 2}², un diseño pequeño y bien condicionado. Los fallos del §5 necesitan un gran desplazamiento o columnas casi colineales, que ninguna prueba cubre.

**Criterio de aprobación:** Deducir y resolver las ecuaciones normales de un pequeño ajuste, decidir la identificabilidad y dar la solución de norma mínima, explicar el κ² de las ecuaciones normales y el efecto del centrado, escribir la solución ridge con sus factores de filtro, y seguir lo que calcula la regresión de IX y lo que su pánico hace a sus llamadores.

---

## Base de investigación

- Å. Björck, *Numerical Methods for Least Squares Problems*, SIAM, 1996: las ecuaciones normales, las resoluciones por QR y por SVD, y su precisión
- L. N. Trefethen y D. Bau, *Numerical Linear Algebra*, SIAM, 1997, lecciones 11, 18 y 19: los mínimos cuadrados, su condicionamiento y la estabilidad de sus algoritmos
- P. Läuchli, «Jordan-Elimination und Ausgleichung nach kleinsten Quadraten», *Numerische Mathematik* 3, 1961: la matriz que sus ecuaciones normales pierden
- A. N. Tikhonov, «Solution of incorrectly formulated problems and the regularization method», *Soviet Mathematics Doklady* 4, 1963: la regularización
- A. E. Hoerl y R. W. Kennard, «Ridge regression: biased estimation for nonorthogonal problems», *Technometrics* 12, 1970: la regresión ridge
- T. Hastie, R. Tibshirani y J. Friedman, *The Elements of Statistical Learning*, 2.ª ed., Springer, 2009, §3.4: los métodos de contracción
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §5 enlaza a su línea
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
