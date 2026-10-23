---
module_id: mat-011-gradients-reverse-mode-autodiff
department: mathematics
course: Gradientes y diferenciación automática en modo inverso
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Gradientes y diferenciación automática en modo inverso — La regla de la cadena, recorrida hacia atrás sobre una cinta

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Calcular gradientes y jacobianas, y aplicar la regla de la cadena a una composición como un producto de matrices
- Escribir un cálculo como una traza de evaluación y propagar derivadas a través de ella en modo directo
- Ejecutar el modo inverso sobre una cinta, y explicar por qué un solo barrido inverso da un gradiente entero
- Tratar los productos de matrices, la difusión y los valores reutilizados en una pasada hacia atrás
- Usar las diferencias finitas como oráculo, y elegir el paso que equilibra el error de truncamiento y el de redondeo
- Rastrear qué garantizan, y qué no, la cinta de diferenciación automática de IX, sus pruebas por diferencias finitas y su herramienta MCP

---

## 1. Derivadas, gradientes y regla de la cadena

Para una función f: Rⁿ → R, la **derivada parcial** ∂f/∂xᵢ es la tasa de cambio de f cuando solo se mueve xᵢ, y el **gradiente** ∇f(x) = (∂f/∂x₁, …, ∂f/∂xₙ) las reúne. Da la mejor aproximación lineal f(x + d) ≈ f(x) + ∇f(x) · d para d pequeño, y apunta en la dirección en la que f crece más rápido. Para una función F: Rⁿ → Rᵐ, la **jacobiana** J_F(x) es la matriz m × n cuya fila i es el gradiente de la i-ésima salida: es la matriz, en el sentido de MAT-004, de la aplicación lineal que mejor aproxima F cerca de x.

La **regla de la cadena** dice que la aproximación lineal de una composición es la composición de las aproximaciones lineales: J_{G∘F}(x) = J_G(F(x)) J_F(x), un producto de matrices, como en MAT-004. Para una función escalar g de y = F(x), se escribe ∇(g∘F)(x) = J_F(x)ᵀ ∇g(y): el gradiente respecto de x es el gradiente respecto de y multiplicado por la jacobiana traspuesta. Cada método de esta lección es una manera de organizar ese producto.

### Ejercicio práctico

Sea f(x, y) = (xy + x)². Calcula ∂f/∂x y ∂f/∂y en (1, 2).

> *Solución:* Escribe u = xy + x, de modo que f = u², con u = 3 y f = 9 en (1, 2). Por la regla de la cadena, ∂f/∂x = 2u · ∂u/∂x = 2u(y + 1) = 18, y ∂f/∂y = 2u · ∂u/∂y = 2u · x = 6.

---

## 2. Trazas de evaluación y modo directo

Un programa calcula f mediante una sucesión de operaciones elementales, cada una con una derivada conocida. Escrita con un nombre por valor intermedio, esa sucesión es una **traza de evaluación**, o lista de Wengert. Para la función del §1:

v₁ = x, v₂ = y, v₃ = v₁v₂, v₄ = v₃ + v₁, v₅ = v₄², f = v₅.

El **modo directo** lleva, junto a cada valor vᵢ, su **tangente** v̇ᵢ, la derivada de vᵢ en una dirección de entrada elegida, y la actualiza con la derivada local de cada operación: v̇₃ = v̇₁v₂ + v₁v̇₂, v̇₄ = v̇₃ + v̇₁, v̇₅ = 2v₄v̇₄. Sembrar las entradas con una dirección d da en la salida la derivada direccional J d, un **producto jacobiana–vector**, por un pequeño múltiplo constante del coste de evaluar f. Un gradiente completo de f: Rⁿ → R requiere por tanto n barridos directos, uno por entrada.

La diferenciación automática no es ni diferenciación simbólica ni diferenciación numérica. Nunca construye una fórmula para la derivada, así que las expresiones no se hinchan, y los bucles y las ramas se tratan a medida que se ejecutan; y no usa ningún paso, así que su resultado es exacto salvo por el redondeo de las propias operaciones.

### Ejercicio práctico

Ejecuta el modo directo sobre la traza anterior en (x, y) = (1, 2) con la semilla (ẋ, ẏ) = (1, 0). ¿Cuánto valen v̇₃, v̇₄ y v̇₅? ¿Qué da la semilla (0, 1)?

> *Solución:* v̇₁ = 1 y v̇₂ = 0. Entonces v₃ = 2 y v̇₃ = 1 · 2 + 1 · 0 = 2; v₄ = 3 y v̇₄ = 2 + 1 = 3; v₅ = 9 y v̇₅ = 2 · 3 · 3 = 18, que es ∂f/∂x. La semilla (0, 1) da v̇₃ = 1, v̇₄ = 1 y v̇₅ = 6, que es ∂f/∂y: dos barridos para dos derivadas parciales.

---

## 3. El modo inverso y la cinta

El **modo inverso** ejecuta la traza una vez hacia delante, registrando en una **cinta** cada operación y los valores que necesitará, y luego recorre la cinta hacia atrás. Lleva para cada valor su **adjunto** v̄ᵢ = ∂f/∂vᵢ, la sensibilidad de la salida a ese valor. La salida empieza con el adjunto 1. Cada operación pasa a cada una de sus entradas su propio adjunto multiplicado por la derivada parcial local, y un valor usado por varias operaciones recibe la suma de las contribuciones: la regla de la cadena suma sobre todos los caminos que van del valor a la salida.

Un solo barrido inverso da el adjunto de cada entrada, así que el gradiente entero de una función escalar cuesta un pequeño múltiplo constante de una evaluación de f, sea cual sea el número de entradas. En términos de matrices, un barrido inverso calcula un **producto vector–jacobiana** v̄ᵀ J, donde el modo directo calcula J d. El precio es la memoria: cada valor que necesita una derivada local debe permanecer en la cinta hasta que el recorrido hacia atrás llegue a él. El modo directo conviene a funciones con pocas entradas y muchas salidas, el modo inverso al caso contrario, como una pérdida que depende de millones de parámetros. El modo inverso aplicado a una red neuronal es la **retropropagación**.

### Ejercicio práctico

Ejecuta el modo inverso sobre la traza del §2 en (1, 2). Da los adjuntos de v₄, v₃, x e y.

> *Solución:* v̄₅ = 1. Como v₅ = v₄², v̄₄ = 2v₄ · v̄₅ = 6. La suma v₄ = v₃ + v₁ pasa 6 a v₃ y 6 a v₁. El producto v₃ = v₁v₂ pasa v̄₃ · v₂ = 12 a v₁ y v̄₃ · v₁ = 6 a v₂. Así x̄ = 6 + 12 = 18 e ȳ = 6: las dos derivadas parciales en un solo barrido. x se usa dos veces, y su adjunto es la suma de las dos contribuciones.

---

## 4. Arreglos: productos de matrices, difusión y reutilización

El código de aprendizaje automático aplica las mismas reglas a arreglos enteros. Para Z = AB, con A de tamaño m × k y B de tamaño k × n, y una pérdida escalar L cuyo adjunto respecto de Z es el arreglo m × n Z̄, la regla de la cadena da Ā = Z̄ Bᵀ y B̄ = Aᵀ Z̄. Las formas se comprueban solas: Z̄ Bᵀ es un m × n por un n × k, la forma de A.

La **difusión** (broadcasting) permite a una operación combinar arreglos de formas distintas repitiendo el más pequeño: sumar una fila b de 1 × 3 a cada fila de una matriz 2 × 3 usa b dos veces. Cada uso devuelve un adjunto, así que b̄ es la suma de Z̄ sobre las filas. La regla general, a menudo llamada **desdifusión** (unbroadcasting), suma el adjunto entrante sobre cada eje que la difusión creó o estiró, hasta recuperar la forma del operando. La **reutilización** es la misma regla en otra forma: en x · x el mismo arreglo es los dos operandos, cada operando recibe Z̄ multiplicado por el otro, x, y el adjunto de x es su suma, 2x por Z̄ elemento a elemento.

### Ejercicio práctico

Sea L = sum(AB) con A = [[0.1, −0.5, 1.2], [0.3, −0.8, 0.7]] y B = [[0.5, −0.2], [0.8, 1.1], [−0.4, 0.3]], escritas fila por fila. Calcula Ā y B̄.

> *Solución:* La suma da el adjunto 1 a cada entrada de Z = AB, así que Z̄ es la matriz 2 × 2 de unos. Ā = Z̄ Bᵀ: las dos filas de Ā contienen las sumas de las filas de B, (0.5 − 0.2, 0.8 + 1.1, −0.4 + 0.3) = (0.3, 1.9, −0.1). B̄ = Aᵀ Z̄: las dos columnas de B̄ contienen las sumas de las columnas de A, (0.1 + 0.3, −0.5 − 0.8, 1.2 + 0.7) = (0.4, −1.3, 1.9). Son los arreglos de `verify_matmul_backward` de IX (§6).

---

## 5. Las diferencias finitas como oráculo

Antes de confiar en una pasada hacia atrás escrita a mano, compárala con un cociente de diferencias. La fórmula de Taylor da f(x ± h) = f(x) ± h f′(x) + (h²/2) f″(x) ± (h³/6) f‴(x) + …, así que la **diferencia hacia delante** (f(x + h) − f(x))/h = f′(x) + (h/2) f″(x) + … tiene un **error de truncamiento** de orden h, mientras que en la **diferencia centrada** (f(x + h) − f(x − h))/(2h) los términos de orden par se cancelan y el error es (h²/6) f‴(x) + …, de orden h². Para f(x) = x³ en 1, la diferencia centrada vale exactamente 3 + h², y la diferencia hacia delante 3 + 3h + h².

El redondeo tira en sentido contrario. Cada valor calculado de f lleva un error de alrededor de u|f|, o mayor si el propio cálculo de f pierde precisión, donde u = 2^-53 ≈ 1.1 · 10^-16 es la unidad de redondeo de MAT-003, y el cociente lo divide por h. El error de la diferencia centrada es por tanto de alrededor de E(h) = h²|f‴|/6 + u|f|/h: baja como h² al reducir h, y luego crece como 1/h, una curva en U cuyo mínimo está cerca de h = (3u|f|/|f‴|)^(1/3), del orden de u^(1/3) ≈ 5 · 10^-6 para magnitudes de orden 1, con un error del orden de u^(2/3) ≈ 10^-11. Para la diferencia hacia delante, el mejor paso y el mejor error son ambos del orden de √u ≈ 10^-8. Una comprobación por diferencia centrada puede confirmar así unas diez cifras de un gradiente, no más, y necesita dos evaluaciones por entrada: un oráculo para las pruebas, no una manera de entrenar.

Dos casos escapan a este modelo. Si f es un polinomio de grado a lo sumo 2 en la variable perturbada, entonces f‴ = 0 y la diferencia centrada no tiene ningún error de truncamiento: la comprobación solo ve el redondeo. Y en un punto anguloso, donde f no tiene derivada, los dos métodos pueden discrepar legítimamente.

### Ejercicio práctico

Calcula las diferencias hacia delante y centrada de f(x) = x³ en x = 1 con h = 0.1, y explica por qué sus errores tienen órdenes distintos. ¿Qué da la diferencia centrada para |x| en 0?

> *Solución:* (1.331 − 1)/0.1 = 3.31, un error de 0.31 = 3h + h², de orden h; (1.331 − 0.729)/0.2 = 3.01, un error de 0.01 = h², de orden h². En los desarrollos de f(x + h) y f(x − h), los términos de orden par tienen el mismo signo y se cancelan en la diferencia, lo que deja 2h f′(x) más términos en h³. Para |x| en 0, la diferencia centrada vale (h − h)/(2h) = 0 para todo h, mientras que las diferencias laterales dan 1 y −1: |x| no tiene derivada en 0, y 0 es solo una elección admisible entre otras, una convención que IX también usa para el módulo de un espectro (§6).

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**La cinta** (`crates/ix-autograd`). Cada operación apila un [`TapeNode`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L22), que guarda su nombre, los identificadores de sus entradas y su valor, sobre una [`Tape`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L41) de solo anexión, que lleva un [`DiffContext`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L90). Las [operaciones documentadas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/lib.rs#L6) son `add`, `sub`, `mul`, `sum`, `matmul`, `div_scalar`, `mean` y `variance`, las dos últimas compuestas de las otras; no hay `exp`, ni `log`, ni función de activación, así que, salvo una operación de FFT detrás de un indicador de funcionalidad, toda función construida con ellas es un polinomio de las entradas, ya que `div_scalar` solo divide por una constante. [`backward`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L382) recorre la cinta [en orden inverso de índices](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L391), un orden topológico inverso válido porque las entradas de una operación siempre se apilan antes que ella, y [suma](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L438) cada contribución al adjunto de su entrada, la regla del §3. La pasada hacia atrás de `matmul` calcula [Z̄ Bᵀ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L249) y [Aᵀ Z̄](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L251), y `unbroadcast`, abajo, es la regla del §4. `variance` [eleva su residuo al cuadrado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L365) con `mul(ctx, residual, residual)`, el mismo identificador dos veces, y depende de esa acumulación.

```rust
fn unbroadcast(mut grad: ArrayD<f64>, target_shape: &[usize]) -> ArrayD<f64> {
    while grad.ndim() > target_shape.len() {
        grad = grad.sum_axis(Axis(0));
    }
    for (i, &t) in target_shape.iter().enumerate() {
        if t == 1 && grad.shape()[i] != 1 {
            let summed = grad.sum_axis(Axis(i));
            grad = summed.insert_axis(Axis(i));
        }
    }
    grad
}
```

- **Los errores de forma entran en pánico en lugar de devolver un error.** El comentario de `add` dice [`// ndarray broadcasts automatically; errors if incompatible`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L78), pero `&av + &bv` devuelve un arreglo, no un `Result`, así que no puede informar de un error: en la versión que declara IX, la 0.17, ndarray entra en pánico cuando dos formas no se pueden difundir, y `sub` y `mul` usan los mismos operadores. `matmul` [comprueba que sus dos entradas tengan rango 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L193) pero no que las dimensiones interiores coincidan, y [`dot`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L215) entra en pánico cuando difieren. El crate define un error [`ShapeMismatch`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/lib.rs#L83) para esos casos, y solo la operación de FFT [lo devuelve](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops_fft.rs#L139). Una matriz 5 × 3 por una matriz 2 × 1 termina por tanto en un pánico, no en un `Err`.
- **Un objetivo aplanado cambia la pérdida sin ningún error.** El [esquema de `ix_autograd_run`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/tools.rs#L1366) acepta cada entrada como «1-D, 2-D, or scalar», y [`parse_array_d`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4359) convierte una lista plana en un [arreglo de una dimensión](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4376). [`build_graph`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L56) [resta luego el objetivo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L73) de la predicción sin comprobar las formas. Con y como columna 5 × 1, el residuo es 5 × 1; con los mismos cinco números como un y plano de forma 5, la difusión lo convierte en 5 × 5 y compara cada predicción con cada objetivo. Con las entradas de la prueba MCP, la pérdida pasa a ser 0.16316 en lugar de 0.15116, y el gradiente de w cambia con ella, sin ningún error. La [prueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/autograd_run.rs#L47) pasa y como columna y [de la pérdida solo comprueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/autograd_run.rs#L75) que sea finita y no negativa, como lo son ambos valores. Estos números vienen de una transcripción, no de una ejecución; el §7 los comprueba.
- **El modo de ejecución no cambia nada.** Un `DiffContext` [guarda un `ExecutionMode`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L94), y [`VerifyFiniteDiff`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L41) está documentado como el modo que [ejecuta el verificador por diferencias finitas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L38) sobre cada herramienta. Ningún código actúa según el modo, que solo imprime la salida `Debug`: cada operación apila en la cinta en todos los modos, incluido `Eager`, documentado como [«plain values, no tape»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L25), cuya pasada hacia delante, según el trait de las herramientas, [se ejecuta en «pure numeric»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tool.rs#L37). El verificador, [`verify_gradient`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L43), es una función del archivo de pruebas, no de la biblioteca, y fuera de su propia definición, el único código que nombra `VerifyFiniteDiff` es una prueba que [comprueba sus predicados](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L108). `ix_autograd_run` [siempre se ejecuta en `Train`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4314).
- **Las pruebas por diferencias finitas no pueden ver el error de truncamiento.** Las 17 comprobaciones que se ejecutan por defecto usan ε = 10^-6, cerca del mejor paso centrado del §5, y una tolerancia absoluta de 10^-5, relajada a 10^-4 en cinco de ellas; los comentarios de las pruebas de la [varianza](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L628) y del [error cuadrático medio](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L718) dan como motivo la profundidad de la cadena. Pero cada función que comprueban, restringida al único elemento perturbado, es un polinomio de grado a lo sumo 2: sumas, productos de dos factores, un producto de matrices, una media, una varianza, un error cuadrático. Para una función así, la diferencia centrada es exacta salvo por el redondeo, sea cual sea la profundidad de la cadena, así que las pruebas solo miden el redondeo, alrededor de u|f|/ε ≈ 10^-10 para valores de orden 1, muy por debajo de ambas tolerancias. La única comprobación no polinómica, [`verify_rfft_magnitude_backward`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L887), está detrás de la funcionalidad [`fft-autograd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L885), que solo un job de CI [activa](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/.github/workflows/ci.yml#L111).
- **Un punto anguloso recibe una convención.** La pasada hacia atrás de `rfft_magnitude` [pone el gradiente a 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops_fft.rs#L152) allí donde un módulo es menor que 10^-15, la elección del §5 para |x| en 0. Su comentario habla de módulos exactamente nulos; el umbral anula también el gradiente de un módulo de 10^-16, que no lo es.
- **Cada herramienta ignora el adjunto de arriba.** Las cuatro herramientas diferenciables, para la [regresión lineal](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L139), la [varianza](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/stats_variance.rs#L64), la [media](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/stats_mean.rs#L60) y el [error cuadrático](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/mse_loss.rs#L109), reciben los gradientes de arriba en un `_out_grads` sin usar y [siembran su propia salida con 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L144). Dentro de un barrido inverso más largo, la regla del §3 multiplica por el adjunto entrante; estas herramientas siempre devuelven el gradiente de su propia salida, como si fuera la pérdida final. `ix_autograd_run` ejecuta una herramienta cada vez, así que hoy no se ve afectado; un pipeline que encadenara herramientas sí lo estaría.

El verificador compara cada gradiente analítico con una diferencia centrada y una tolerancia absoluta:

```rust
        for (flat_idx, &analytical) in grad_values.iter().enumerate().take(input.len()) {
            let f_plus = perturbed_loss(&forward, &inputs, name, flat_idx, epsilon);
            let f_minus = perturbed_loss(&forward, &inputs, name, flat_idx, -epsilon);
            let numerical = (f_plus - f_minus) / (2.0 * epsilon);
            let diff = (numerical - analytical).abs();
            if diff > tolerance {
```

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

¿Por qué un y plano de longitud 5 da un residuo 5 × 5 en `build_graph`, y qué calcula entonces la pérdida?

> *Solución:* La predicción tiene forma 5 × 1 y un y plano tiene forma 5. La difusión trata primero y como una fila 1 × 5, y luego estira ambos a 5 × 5, así que la entrada (i, j) del residuo es ŷᵢ − yⱼ. La media de sus 25 cuadrados compara cada predicción con cada objetivo, y no cada una con el suyo: con ŷ = (0.16, 0.58, −0.31, 0.09, 0.66) y el y de la prueba, vale 0.16316 en lugar de 0.15116. Nada falla, porque las formas son compatibles; solo una comprobación de formas allí donde entran los datos, o una prueba sobre el valor, lo detecta.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio, nunca contra un servidor MCP en funcionamiento.

1. **El ejemplo resuelto.** Construye f(x, y) = (xy + x)² con `input`, `mul`, `add`, `mul` y `sum` sobre los tensores de un elemento x = [1] e y = [2], y llama a `backward` con la semilla 1. Predicción: los adjuntos de x y de y valen exactamente 18 y 6.
2. **La curva en U.** Construye f(x) = sum(x · x · x) con dos operaciones `mul` en x = [1]; su gradiente en modo inverso vale exactamente 3. Compáralo con las diferencias centradas y hacia delante del valor calculado por la cinta para h = 10^-1, 10^-2, …, 10^-12. Predicción: el error centrado es igual a h² con una precisión del 1% para h de 10^-1 a 10^-3, alcanza su mínimo, por debajo de 10^-9, entre h = 10^-7 y 10^-5, y supera 10^-6 en h = 10^-12; el error hacia delante es cercano a 3h para h grande y es mínimo entre h = 10^-9 y 10^-7, en un valor mayor que el mínimo centrado.
3. **El punto ciego cuadrático.** Repite el paso 2 con sum(x · x), cuyo gradiente vale 2. Predicción: no hay rama en h²; para h de 10^-1 a 10^-6, el error centrado se mantiene por debajo de 10^-10.
4. **El producto de matrices.** Con los arreglos de `verify_matmul_backward`, calcula el gradiente de sum(AB). Predicción: las dos filas de Ā valen (0.3, 1.9, −0.1) y las dos columnas de B̄ valen (0.4, −1.3, 1.9), con una precisión de 10^-15.
5. **Un objetivo aplanado.** Llama al manejador `autograd_run` con las entradas de la prueba MCP, una vez con y como columna y otra vez plano. Predicción: las pérdidas 0.15116 y 0.16316, con una precisión de 10^-12, la segunda sin error y con un gradiente de w distinto.
6. **Formas incompatibles.** Bajo `std::panic::catch_unwind`, llama a `matmul` sobre una matriz 5 × 3 y una matriz 2 × 1, y a `add` sobre una matriz 2 × 3 y una matriz 2 × 2. Predicción: ambas llamadas entran en pánico, y ninguna devuelve un `Err`.
7. **Los modos.** Construye el grafo de regresión lineal en cada uno de los cuatro modos. Predicción: la cinta contiene 10 nodos en cada modo, y no se ejecuta ninguna comprobación por diferencias finitas.

### Ejercicio práctico

En el paso 2, con f(x) = x³ en 1, el modelo de error del §5 se escribe E(h) = h² + u/h. ¿Qué h lo minimiza, y qué error predice en el fondo de la curva?

> *Solución:* E′(h) = 2h − u/h² se anula cuando h³ = u/2 = 2^-54, así que h = 2^-18 ≈ 3.8 · 10^-6. Allí, E = 2^-36 + 2^-35 = 3 · 2^-36 ≈ 4.4 · 10^-11. La rejilla del paso 2 encierra ese punto entre h = 10^-6 y 10^-5, y por eso la predicción sitúa el mínimo entre 10^-7 y 10^-5, por debajo de 10^-9: el modelo da el tamaño del error de redondeo, no su valor exacto.

---

## 8. Errores comunes

- **Sobrescribir en lugar de acumular.** Un valor usado dos veces debe recibir la suma de sus adjuntos; sobrescribir conserva un solo camino y reduce a la mitad, sin avisar, la derivada de x · x.
- **Olvidar la desdifusión.** El adjunto de un operando difundido debe sumarse hasta recuperar la forma de ese operando.
- **Elegir a ciegas el paso de las diferencias finitas.** Demasiado grande y domina el truncamiento, demasiado pequeño y domina el redondeo; toma alrededor de u^(1/3) para las diferencias centradas y √u para las diferencias hacia delante, a la escala de x.
- **Comprobar solo funciones cuadráticas.** Sus diferencias centradas son exactas salvo por el redondeo, así que la comprobación nunca encuentra el error de truncamiento; incluye una función cúbica o trascendente.
- **Comprobar en un punto anguloso.** En la esquina de |x|, de un máximo o de un módulo, la derivada no existe, y las diferencias finitas y la diferenciación automática pueden diferir legítimamente.
- **Confiar en la difusión silenciosa.** Formas compatibles pero no deseadas dan un número erróneo en lugar de un error; comprueba las formas allí donde entran los datos.
- **Perder el adjunto de arriba.** Una pasada hacia atrás dentro de una cadena más larga debe multiplicar por el adjunto que recibe; sembrar 1 solo es correcto para la pérdida final.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Gradiente** | El vector de las derivadas parciales de una función escalar, que apunta hacia donde crece más rápido |
| **Jacobiana** | La matriz de las derivadas parciales de una función vectorial, la matriz de su mejor aproximación lineal |
| **Regla de la cadena** | La jacobiana de una composición es el producto de las jacobianas |
| **Traza de evaluación** | La sucesión de operaciones elementales que ejecuta un programa, también llamada lista de Wengert |
| **Tangente** | En modo directo, la derivada de un valor intermedio en una dirección de entrada elegida |
| **Adjunto** | En modo inverso, la derivada de la salida respecto de un valor intermedio |
| **Modo directo** | Propaga las tangentes junto con la evaluación; un barrido da un producto jacobiana–vector |
| **Modo inverso** | Recorre la traza hacia atrás; un barrido da un producto vector–jacobiana, el gradiente entero de un escalar |
| **Cinta** | El registro de la traza y de los valores que necesita el barrido inverso |
| **Desdifusión** | La suma de un adjunto sobre los ejes que la difusión amplió, hasta la forma del operando |
| **Diferencia centrada** | (f(x + h) − f(x − h))/(2h), con un error de truncamiento de orden h² y un error de redondeo de orden u/h |

---

## Autoevaluación

**1. Una pérdida depende de 10^6 parámetros. ¿Por qué se prefiere el modo inverso al modo directo y a las diferencias finitas para calcular su gradiente?**
> Un solo barrido inverso da las 10^6 derivadas parciales por un pequeño múltiplo constante del coste de una evaluación. El modo directo necesita un barrido por parámetro, y las diferencias centradas necesitan 2 · 10^6 evaluaciones y solo confirman unas diez cifras. El precio del modo inverso es la memoria: la cinta conserva los valores intermedios.

**2. En una cinta, ¿por qué x · x recibe el adjunto 2x, y qué devolvería un recorrido que sobrescribiera los adjuntos en lugar de sumarlos?**
> Las dos entradas de la operación son el mismo nodo, y cada una recibe el adjunto entrante multiplicado por el otro factor, x; su suma es 2x. Un recorrido que sobrescribiera conservaría una sola contribución y devolvería x, la mitad de la derivada.

**3. Las pruebas por diferencias finitas de IX pasan. ¿Qué establecen?**
> Que las pasadas hacia atrás concuerdan con diferencias centradas, en los puntos elegidos y dentro de la tolerancia, para sumas, productos, un producto de matrices, medias, varianzas y errores cuadráticos. Estas funciones tienen grado a lo sumo 2 en cada elemento, así que la diferencia centrada es exacta salvo por el redondeo: las pruebas detectan una fórmula de derivada errónea, pero nunca ejercitan el error de truncamiento, las funciones no polinómicas fuera de la prueba de FFT sujeta a una funcionalidad, ni los errores de forma.

**4. `ix_autograd_run` devuelve una pérdida finita y no negativa para tus datos. ¿Puedes confiar en ella?**
> No sin comprobar las formas. Un y plano se difunde contra la predicción 5 × 1 en un residuo 5 × 5 y da otra pérdida finita y no negativa, 0.16316 en lugar de 0.15116 con los datos de la prueba. Envía y como una columna n × 1, y compara la forma de la predicción devuelta con la de y.

**Criterio de aprobación:** Calcular gradientes y jacobianas y aplicar la regla de la cadena, ejecutar a mano los modos directo e inverso sobre una traza de evaluación, deducir las reglas de la pasada hacia atrás para los productos de matrices, la difusión y la reutilización, elegir un paso de diferencias finitas a partir del equilibrio entre truncamiento y redondeo, y rastrear qué garantizan la cinta, las pruebas y la herramienta MCP de IX.

---

## Base de investigación

- R. E. Wengert, «A simple automatic derivative evaluation program», *Communications of the ACM* 7, 1964: la traza de evaluación y el modo directo
- S. Linnainmaa, «Taylor expansion of the accumulated rounding error», *BIT Numerical Mathematics* 16, 1976: la acumulación inversa de derivadas
- D. E. Rumelhart, G. E. Hinton y R. J. Williams, «Learning representations by back-propagating errors», *Nature* 323, 1986: la retropropagación
- A. Griewank y A. Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, 2.ª ed., SIAM, 2008: las cintas, los adjuntos y el coste de un barrido inverso
- A. G. Baydin, B. A. Pearlmutter, A. A. Radul y J. M. Siskind, «Automatic differentiation in machine learning: a survey», *Journal of Machine Learning Research* 18, 2018: los modos directo e inverso, y en qué se distinguen de la diferenciación simbólica y la numérica
- P. E. Gill, W. Murray y M. H. Wright, *Practical Optimization*, Academic Press, 1981: la elección de los pasos de diferencias finitas
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
