---
module_id: mat-003-floating-point-conditioning
department: mathematics
course: Aritmética de punto flotante y condicionamiento
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Aritmética de punto flotante y condicionamiento — Cuando una computadora pierde dígitos

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Explicar por qué la mayoría de los números reales, incluido 0.1, no pueden almacenarse exactamente en una computadora
- Enunciar el modelo estándar del redondeo de punto flotante y el significado del épsilon de máquina
- Distinguir el error hacia adelante del error hacia atrás, y un problema mal condicionado de un algoritmo inestable
- Demostrar la cota que define el número de condición de un sistema lineal
- Estimar a partir de κ(A) cuántos dígitos puede perder un cálculo, y encontrar dónde traza IX ese límite en su código

---

## 1. Los números que una computadora puede almacenar

Una computadora no almacena números reales. Almacena un conjunto **finito** de ellos. El formato habitual, **binary64** de la norma IEEE 754 (`f64` en Rust, `double` en C), codifica un número en 64 bits: 1 bit de signo, 11 bits de exponente y 52 bits de fracción. Con el 1 inicial implícito, cada número almacenado **normal** lleva **53 bits significativos**, unos 16 dígitos decimales. Los diminutos números **subnormales** cercanos a cero renuncian a ese 1 inicial y tienen menos.

Los números almacenados no están espaciados de manera uniforme. Entre 1 y 2 están separados por 2^-52; entre 2 y 4, el doble; y así sucesivamente. Dos cantidades describen esta cuadrícula:
- El **épsilon de máquina** ε = 2^-52 ≈ 2.2 × 10^-16 es la distancia entre 1 y el siguiente número almacenado.
- La **unidad de redondeo** u = ε/2 = 2^-53 ≈ 1.1 × 10^-16 es el mayor error relativo que se comete al redondear un real del **rango normal** al número almacenado más cercano. Por debajo, entre los subnormales, el error relativo puede ser mucho mayor: 2^-1075 se redondea a 0, un error relativo de 1.

Un número se almacena exactamente solo si es una fracción cuyo denominador es una potencia de dos (y cabe en el rango y en los 53 bits). **0.1 = 1/10 no lo es**: su denominador contiene el factor 5, así que su desarrollo binario nunca termina, igual que 1/3 = 0.333… nunca termina en decimal. La computadora almacena en su lugar el número binary64 más cercano. Por eso `0.1 + 0.2 == 0.3` no es una prueba segura: cada literal se redondea, la suma se redondea de nuevo, y nada garantiza que el resultado caiga en el mismo número almacenado que 0.3.

### Ejercicio práctico

¿Cuáles de estos números se almacenan exactamente en binary64: 0.5, 0.75, 0.1, 1/3, 2^60?

> *Solución:* 0.5 = 2^-1, 0.75 = 2^-1 + 2^-2 y 2^60 son exactos: cada uno es una suma de unas pocas potencias de dos, dentro del rango. 0.1 y 1/3 no lo son: sus denominadores (10 y 3) no son potencias de dos, así que sus desarrollos binarios son infinitos y deben redondearse.

---

## 2. El modelo estándar del redondeo

IEEE 754 exige que cada operación básica esté **correctamente redondeada**: la computadora devuelve el resultado exacto, redondeado a un número almacenado. Con redondeo al más cercano, y mientras nada desborde por arriba ni por abajo, se obtiene el **modelo estándar**:

fl(x ∘ y) = (x ∘ y)(1 + δ), con |δ| ≤ u, para ∘ una de las operaciones +, −, ×, ÷.

Así, una operación *aislada* es casi exacta. Los problemas vienen de dos lugares:
- **La acumulación.** Un cálculo largo comete muchos errores pequeños, y pueden sumarse.
- **La cancelación.** Restar dos números casi iguales es exacto o casi exacto, pero deja al descubierto los errores de redondeo que los operandos *ya* llevaban. Los primeros dígitos se cancelan; lo que queda es sobre todo ruido.

### Ejercicio práctico

El número a = 1 + 10^-8 se almacena con un error relativo de a lo sumo u, y b = 1 se almacena exactamente. Acota el error relativo de la diferencia calculada â − b, ignorando el error (mínimo) de la propia resta.

> *Solución:* El valor almacenado es â = a(1 + δ) con |δ| ≤ u. Entonces â − b = (a − b) + aδ, así que el error relativo es |aδ| / |a − b| ≤ u(1 + 10^-8) / 10^-8 ≈ 10^8 · u ≈ 1.1 × 10^-8. El resultado tiene unos 8 dígitos correctos, no 16: la resta perdió la mitad.

---

## 3. Error hacia adelante, error hacia atrás y condicionamiento

Supongamos que queremos y = f(x) y la computadora devuelve ŷ.
- El **error hacia adelante** (forward error) pregunta: ¿a qué distancia está la respuesta de la verdad? Vale |ŷ − y| / |y|.
- El **error hacia atrás** (backward error) pregunta: ¿para qué entrada cercana es ŷ la respuesta *exacta*? Es la menor perturbación relativa |Δx| / |x| tal que ŷ = f(x + Δx).

Un algoritmo es **estable hacia atrás** (backward stable) si su error hacia atrás es siempre del orden de u: da la respuesta exacta a una pregunta ligeramente distinta. Que esa respuesta esté *cerca de la verdad* depende del problema, no del algoritmo. El **número de condición** mide cuánto amplifica el problema un cambio relativo en su entrada. Ambos se combinan en la regla más útil del análisis numérico:

error hacia adelante ≲ número de condición × error hacia atrás.

Esta regla separa dos fallos distintos: un **problema mal condicionado** (ningún algoritmo puede hacerlo mucho mejor) y un **algoritmo inestable** (un algoritmo mejor sí podría).

### Ejercicio práctico

Para una función derivable, el número de condición relativo es |x · f′(x) / f(x)|. Calcúlalo para f(x) = x − 1 y evalúalo en x = 1 + 10^-8.

> *Solución:* f′(x) = 1, así que el número de condición es |x / (x − 1)|. En x = 1 + 10^-8 vale (1 + 10^-8) / 10^-8 ≈ 10^8. Es la cancelación del §2 vista desde el lado del problema: cualquier error relativo en x se amplifica unas 10^8 veces, sea cual sea el algoritmo que calcule x − 1.

---

## 4. El número de condición de una matriz

Resolvamos ahora un sistema lineal A x = b, con A cuadrada e invertible. Supongamos que el lado derecho se perturba: A(x + Δx) = b + Δb. ¿Cuánto puede cambiar x en términos relativos?

**Teorema.** Para toda norma vectorial y su norma matricial inducida,

‖Δx‖ / ‖x‖ ≤ κ(A) · ‖Δb‖ / ‖b‖, donde κ(A) = ‖A‖ · ‖A⁻¹‖.

*Demostración (directa, como en MAT-001):*
- Restando A x = b de A(x + Δx) = b + Δb se obtiene A Δx = Δb, así que Δx = A⁻¹ Δb y ‖Δx‖ ≤ ‖A⁻¹‖ · ‖Δb‖.
- De b = A x se obtiene ‖b‖ ≤ ‖A‖ · ‖x‖, así que 1 / ‖x‖ ≤ ‖A‖ / ‖b‖ (para b ≠ 0).
- Multiplicando las dos desigualdades se obtiene ‖Δx‖ / ‖x‖ ≤ ‖A‖ · ‖A⁻¹‖ · ‖Δb‖ / ‖b‖. ∎

En la norma euclidiana, κ₂(A) = σ_max / σ_min, el cociente entre el mayor y el menor **valor singular** de A. Geométricamente, A transforma la esfera unidad en un elipsoide; los valores singulares son las longitudes de sus semiejes, así que κ₂ mide cuán aplastado está ese elipsoide. Esta lección usa los valores singulares como una caja negra; cómo se calculan (la SVD) es el tema de un módulo posterior.

**Regla práctica.** Un solucionador estable hacia atrás en binary64 da un error relativo hacia adelante de aproximadamente κ(A) · u. Con u ≈ 10^-16, cabe esperar perder unos **log₁₀ κ(A)** de los aproximadamente 16 dígitos significativos. Cuando κ(A) se acerca a 1/u ≈ 10^16, ningún dígito de la respuesta es fiable. Es una estimación a partir de una cota superior, no un teorema sobre cada caso.

### Ejercicio práctico

Calcula κ₂ de A = diag(1, 10^-8). ¿Cuántos de los 16 dígitos puede perder una solución de A x = b?

> *Solución:* Los valores singulares de una matriz diagonal son los valores absolutos de sus entradas diagonales: 1 y 10^-8. Así que κ₂(A) = 1 / 10^-8 = 10^8, y una resolución puede perder unos 8 de los 16 dígitos significativos.

---

## 5. Dónde traza IX el límite

IX es la biblioteca Rust de aprendizaje automático del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese comportamiento y no lo modifica.

- [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L83) usa eliminación de Gauss–Jordan con pivoteo parcial. Devuelve `MathError::Singular` cuando el mayor pivote disponible tiene un valor absoluto menor que 10^-12 ([línea 110](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L110)). Ese umbral es **absoluto**: depende de la escala de A, no de κ(A).
- [`SvdResult::rank(tol)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L67) y [`pseudo_inverse(tol)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73) conservan solo los valores singulares estrictamente mayores que `tol`, una tolerancia absoluta elegida por quien llama. La herramienta de agente `ix_svd` elige una **relativa**, σ₁ · 10^-10 ([`handlers.rs` línea 639](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L639)).
- IX **no tiene función de número de condición**. κ₂ debe calcularse como σ_max / σ_min a partir de [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L100).
- [`LinearRegression::fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L68) resuelve las ecuaciones normales XᵀX w = Xᵀy con `inverse(...).expect("X^T X is singular")`, de modo que cualquier veredicto `Singular` se convierte en un pánico en lugar de un error. Formar XᵀX además eleva al cuadrado el número de condición: para X de rango columna completo, κ₂(XᵀX) = κ₂(X)², porque los valores singulares de XᵀX son los cuadrados de los de X.

La prueba de pivote, literal de `linalg.rs`, líneas 110–112:

```rust
        if max_val < 1e-12 {
            return Err(MathError::Singular);
        }
```

### Ejercicio práctico

Usando solo el código anterior, predice qué devuelve `inverse` para A = 10^-13 · I₂ (la identidad 2 × 2 multiplicada por 10^-13) y para A = [[1, 2], [2, 4]]. ¿Qué veredicto dice algo de la matriz, y cuál solo de su escala?

> *Solución:* Ambos devuelven `Singular`. Para 10^-13 · I₂, el primer pivote tiene valor absoluto 10^-13 < 10^-12, así que `inverse` se detiene, aunque κ₂ = 1 (condicionamiento perfecto) y la inversa, 10^13 · I₂, es fácil de calcular. Para [[1, 2], [2, 4]], la segunda fila es el doble de la primera, así que la matriz es exactamente singular; la prueba de IX [`test_singular_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L219) comprueba este caso. Solo el segundo veredicto describe la matriz. El primero describe su escala y, a la inversa, una matriz con un κ enorme pero con pivotes mayores que 10^-12 se invierte sin ningún aviso.

---

## 6. Experimento: matrices de Hilbert en IX

La matriz de Hilbert H_n es la matriz n × n con entradas 1 / (i + j − 1). Es la prueba clásica del mal condicionamiento:
- H_n es simétrica definida positiva, así que es **invertible para todo n** en aritmética exacta.
- Su inversa exacta tiene **entradas enteras** (Choi 1983), lo que da una referencia exacta para medir los errores.
- κ₂(H_n) crece como (1 + √2)^(4n) / √n, aproximadamente e^(3.5n) (Todd 1954): cada fila y columna adicional lo multiplica por unos (1 + √2)^4 ≈ 34.
- La H_n *almacenada* ya no es H_n, porque entradas como 1/3 se redondean: fl(H_n) = H_n + ΔH con ‖ΔH‖ ≤ u‖H_n‖ en la norma ∞. El §4 acota perturbaciones de b, no de A. Para A, el resultado clásico es: si κ(A) · δ < 1 con δ = ‖ΔA‖ / ‖A‖, entonces ‖(A + ΔA)⁻¹ − A⁻¹‖ / ‖A⁻¹‖ ≤ κ(A)δ / (1 − κ(A)δ) (Higham 2002). Así, incluso una inversión perfecta de fl(H_n) tiene un error relativo de hasta aproximadamente κ · u mientras κ · u sea pequeño, y no acotado en cuanto κ · u ≥ 1, cuando la matriz redondeada puede incluso ser singular.
- Para una matriz simétrica A, κ∞(A) / n ≤ κ₂(A) ≤ κ∞(A), donde κ∞ usa la norma del máximo de las sumas por filas. Esta **banda** es un teorema sobre las normas de **una misma** matriz.

**Protocolo.** El laboratorio de Learn [`code/streeling-mathematics`](https://github.com/spareilleux/learn/tree/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics) fija IX en `e35138b9`. Sus predicciones se escribieron y se registraron con hash antes de cualquier compilación ([`preregistration.md`](https://github.com/spareilleux/learn/blob/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics/preregistration.md), SHA-256 `a70179d8a698f835aec724181066823368f0b38f76fe8dcb994494495e412f20`). Para n = 2 a 16 construye fl(H_n) y las mismas matrices multiplicadas por 2^-20 y 2^20. Multiplicar por una potencia de dos es exacto en punto flotante binario, así que cambia la escala y no el condicionamiento. Para cada matriz registra:
- `kappa_inf`: κ∞ de la H_n exacta, a partir de la inversa entera exacta; `kappa_2`: σ₁ / σ_n según la `svd` de IX aplicada a la fl(H_n) almacenada; `band`: si `kappa_2` está entre `kappa_inf` / n y `kappa_inf`. **Corrección:** estas dos columnas describen dos matrices distintas, así que `band` es una comparación mixta, no el teorema anterior;
- `inverse`: la respuesta de IX, `ok` o `Singular`; `fwd_err`: su error hacia adelante ‖X − H_n⁻¹‖∞ / ‖H_n⁻¹‖∞ respecto de la inversa exacta; `residual`: ‖H_n X − I‖∞;
- `rank`: el rango con la tolerancia de `ix_svd`, σ₁ · 10^-10; `pinv_res`: el residuo de ese `pseudo_inverse` truncado; `pinv0_fwd`: el error hacia adelante de `pseudo_inverse(0.0)`.

**Medido** en Windows 11 x86-64 (rustc 1.94.0), copiado de [`expected/mat003_conditioning.txt`](https://github.com/spareilleux/learn/blob/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics/expected/mat003_conditioning.txt) (SHA-256 `6d2a9590b9a37577dd1c4b670d23dbfca55a8fef529e590a246ffa33c675bedb`):

```text
 n  kappa_inf  kappa_2    band  inverse   fwd_err   residual  rank  pinv_res  pinv0_fwd
 2  2.70e1     1.93e1     ok    ok        2.96e-16  0.00e0       2  4.44e-16  4.44e-16
 3  7.48e2     5.24e2     ok    ok        5.97e-15  1.51e-14     3  3.02e-14  5.64e-15
 4  2.84e4     1.55e4     ok    ok        5.55e-14  5.19e-13     4  1.28e-12  1.59e-13
 5  9.44e5     4.77e5     ok    ok        7.26e-13  1.14e-11     5  3.84e-11  4.79e-12
 6  2.91e7     1.50e7     ok    ok        8.89e-11  9.57e-10     6  7.61e-10  1.62e-10
 7  9.85e8     4.75e8     ok    ok        3.02e-9   5.51e-8      7  1.01e-8   2.22e-9
 8  3.39e10    1.53e10    ok    ok        4.82e-9   1.04e-6      7  1.39e0    5.78e-8
 9  1.10e12    4.93e11    ok    ok        3.05e-6   2.54e-4      8  1.36e0    2.55e-4
10  3.54e13    2.10e12    out   ok        1.10e-4   9.91e-3      8  1.47e0    1.00e0
11  1.23e15    2.72e12    out   Singular  -         -            8  1.66e0    1.00e0
12  4.12e16    1.51e12    out   Singular  -         -            9  1.52e0    1.00e0
13  1.32e18    4.31e12    out   Singular  -         -            9  1.83e0    1.00e0
14  4.54e19    7.66e13    out   Singular  -         -           11  3.62e0    1.00e0
15  1.54e21    1.26e14    out   Singular  -         -            9  1.90e0    1.00e0
16  5.06e22    9.71e14    out   Singular  -         -            9  1.98e0    1.00e0
```

```text
Refusal boundary, by scale (the true kappa does not change with scale)
  scale 1      first Singular: 11             worst accepted fwd_err: 1.10e-4 at n = 10
  scale 2^-20  first Singular: 6              worst accepted fwd_err: 7.26e-13 at n = 5
  scale 2^20   first Singular: none up to 16  worst accepted fwd_err: 1.04e0 at n = 14
  scale 1 verdicts: 2:ok 3:ok 4:ok 5:ok 6:ok 7:ok 8:ok 9:ok 10:ok 11:S 12:S 13:S 14:S 15:S 16:S

Scaling by 2^k is exact in binary floating point; is the answer?
  inverse(2^k H) == inverse(H) / 2^k bit for bit: 13 of 13 accepted pairs
  IX kappa_2 bit-identical at the three scales: 5 of 15

Controls
  I * 2^-40: kappa = 1, inverse Singular
  I * 2^-39: kappa = 1, inverse ok, inverse == I * 2^39: true
  [[1,2],[2,4]]: inverse Singular, rank(sigma_1 * 1e-10) = 1
  exact H_3^-1 = [[9, -36, 30], [-36, 192, -180], [30, -180, 180]], H_3 * H_3^-1 == I exactly: Some(true)
  checker on a wrong inverse (I for H_3^-1): residual 1.42e0
```

**Predicciones prerregistradas y veredictos:**

| Predicción | Medido | Veredicto |
|---|---|---|
| `inverse(H_n)` devuelve `Singular` por primera vez en n = 11 | primer `Singular` en n = 11, y luego para todo n hasta 16 | confirmada |
| El rechazo sigue a la escala, no al condicionamiento | I · 2^-40 (κ = 1) rechazada, I · 2^-39 aceptada; 2^-20 · H_n rechazada desde n = 6; 2^20 · H_n nunca rechazada hasta n = 16, con un error hacia adelante de 1.04e0 en n = 14 | confirmada |
| Toda inversa aceptada tiene un error hacia adelante ≤ n · κ∞ · u | se cumple; el peor es 1.10e-4, en n = 10 | confirmada |
| `inverse(2^k H_n)` = `inverse(H_n)` / 2^k, bit a bit | 13 de 13 pares aceptados | confirmada |
| `rank(σ₁ · 10^-10)` baja de n por primera vez en n = 8 | rango 7 en n = 8; el residuo truncado es al menos 1.36 desde ahí | confirmada |
| El κ₂ de IX se mantiene dentro de la banda hasta n = 11 | dentro solo para n = 2 a 9; por debajo de κ∞ / n desde n = 10 | **refutada** tal como se prerregistró, pero la banda mezcla H_n y fl(H_n): ver la corrección más abajo |
| El κ₂ de IX es idéntico bit a bit en las tres escalas | 5 de 15 tamaños | **refutada** |

**Lo que muestra la ejecución:**
- La frontera `Singular` la fija el umbral de pivote absoluto, no la matriz. Las mismas matrices, solo reescaladas, se rechazan desde n = 6 o nunca. En la escala 2^20, `inverse` responde en n = 14 con un error hacia adelante de 1.04e0 — ningún dígito correcto — sin señalar ningún error.
- **Corrección.** Una versión anterior de esta lección interpretaba las salidas de la banda como prueba de que la `svd` de IX devuelve un κ₂ erróneo. Una revisión señaló que la banda compara κ∞ de la H_n exacta con el κ₂ que IX calcula para la fl(H_n) almacenada, mientras que el teorema solo relaciona normas de una misma matriz. Para una H_n mal condicionada, redondear las entradas puede cambiar notablemente el número de condición. Por eso, que `kappa_2` quede por debajo de `kappa_inf` / n desde n = 10 es una **observación**: el valor reportado no es κ₂(H_n), pero la ejecución no permite saber qué parte de la diferencia viene del redondeo de la entrada y qué parte de la SVD. Decidirlo requeriría una referencia para la misma matriz almacenada, como el κ de fl(H_n) calculado con mayor precisión, que este laboratorio no tiene. La columna `rank` tampoco es monótona (11 en n = 14, luego 9 en n = 15), lo que también es solo una observación.
- El κ₂ de IX cambia con un reescalado exacto en todos los tamaños salvo 5 de 15. La causa **no está identificada**; queda como una reproducción abierta para IX, sin explicarla ni corregirla aquí.
- `pseudo_inverse(0.0)`, que conserva todos los valores singulares, tiene un error hacia adelante de 1.00e0 desde n = 10: tampoco tiene ningún dígito correcto.
- La regla práctica del §4 sigue siendo teoría, no una ley medida: los errores medidos quedan por debajo de n · κ∞ · u, y en n = 10 (κ∞ = 3.54e13) el error es 1.10e-4.

**Plataformas.** Los números se midieron en una sola máquina. Después, la CI alojada volvió a ejecutar el laboratorio en Linux x86-64, Windows x86-64 y macOS arm64 (rustc 1.98.1; [PR n.º 24 de Learn](https://github.com/spareilleux/learn/pull/24), [ejecución 36335008098](https://github.com/spareilleux/learn/actions/runs/36335008098)) y reprodujo esta salida byte a byte, incluido un resumen (digest) de los bits en bruto de cada valor calculado (`0ffcce71a1dffe45`). Una salida idéntica muestra que el cálculo es **reproducible** en esas plataformas. No muestra que sea **correcto**: la corrección requiere una referencia independiente para el mismo problema, como la inversa exacta detrás de `fwd_err`, y una salida idéntica solo significa que todas las plataformas cometen exactamente los mismos errores.

### Ejercicio práctico

Usando κ₂(H_n) ≈ e^(3.5n) y la regla práctica del §4, estima el tamaño n a partir del cual una inversa calculada de H_n ya no tiene ningún dígito fiable.

> *Solución:* Ningún dígito sobrevive cuando κ₂ llega a aproximadamente 1/u ≈ 10^16. Resolver e^(3.5n) = 10^16 da n = 16 · ln 10 / 3.5 ≈ 36.8 / 3.5 ≈ 10.5. La ley de crecimiento oculta un factor constante y el término 1 / √n, así que es solo un orden de magnitud. En la tabla medida, κ∞ supera 10^16 por primera vez en n = 12 (4.12e16), con el κ₂ verdadero entre κ∞ / n y κ∞; `inverse` todavía responde en n = 10 con un error hacia adelante de 1.10e-4 y rechaza desde n = 11.

---

## 7. Errores comunes

- **Comparar flotantes calculados con `==`.** Compara con una tolerancia derivada del problema, y hazla relativa cuando la escala varía.
- **Confiar en un residuo pequeño.** Un residuo pequeño r = b − A x̂ no significa un error pequeño: por el teorema del §4 con Δb = −r, el error relativo puede llegar a κ(A) · ‖r‖ / ‖b‖.
- **Confiar en un número de condición calculado cercano a 1/u.** κ también se calcula en punto flotante, a partir de una entrada redondeada: en el §6, el κ₂ que IX reporta para la fl(H_n) almacenada queda por debajo de la cota inferior de la H_n exacta desde n = 10. Por tanto, no es el número de condición del problema que se quería resolver, sea cual sea el peso del redondeo y de la SVD en la diferencia.
- **Leer «no singular» como «bien condicionada».** Un umbral de pivote absoluto, como el de `inverse`, mide la escala, no el condicionamiento.
- **Invertir para resolver.** Calcular A⁻¹ y luego A⁻¹ b cuesta más trabajo que resolver A x = b directamente y suele ser menos preciso; formar XᵀX eleva κ al cuadrado.
- **Creer los dígitos impresos.** Imprimir 17 dígitos no los hace correctos; log₁₀ κ de ellos pueden ser ruido.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **binary64** | El formato de punto flotante de 64 bits de IEEE 754: 53 bits significativos para los números normales, unos 16 dígitos decimales |
| **Épsilon de máquina (ε)** | La distancia entre 1 y el siguiente número almacenado: 2^-52 en binary64 |
| **Unidad de redondeo (u)** | El mayor error relativo del redondeo al más cercano en el rango normal: u = ε/2 = 2^-53 |
| **Cancelación** | Pérdida de dígitos correctos al restar números casi iguales que ya llevan errores |
| **Error hacia adelante** | La distancia entre la respuesta calculada y la respuesta verdadera |
| **Error hacia atrás** | La menor perturbación de la entrada para la que la respuesta calculada es exacta |
| **Estable hacia atrás** | Se dice de un algoritmo cuyo error hacia atrás es siempre del orden de u |
| **Número de condición** | Cuánto amplifica un problema los cambios relativos de su entrada; para una matriz, κ(A) = ‖A‖ · ‖A⁻¹‖ |
| **Valor singular** | La longitud de un semieje de la imagen de la esfera unidad bajo A; κ₂(A) = σ_max / σ_min |
| **Matriz de Hilbert** | La matriz con entradas 1 / (i + j − 1): invertible pero extremadamente mal condicionada |

---

## Autoevaluación

**1. ¿Por qué 0.1 no se almacena exactamente en binary64, mientras que 0.75 sí?**
> 0.75 = 3/4 tiene un denominador potencia de dos, así que su desarrollo binario es finito. 0.1 = 1/10 tiene el factor 5 en su denominador, así que su desarrollo binario es infinito y debe redondearse.

**2. Un algoritmo es estable hacia atrás, pero su respuesta solo tiene 4 dígitos correctos. ¿Es culpa del algoritmo?**
> No necesariamente. Error hacia adelante ≲ número de condición × error hacia atrás. Con un error hacia atrás cercano a 10^-16, 4 dígitos correctos apuntan a un número de condición cercano a 10^12: es el problema, no el algoritmo, el que pierde los dígitos.

**3. Enuncia y demuestra la cota que define κ(A) para A x = b.**
> ‖Δx‖ / ‖x‖ ≤ ‖A‖ · ‖A⁻¹‖ · ‖Δb‖ / ‖b‖. Demostración: Δx = A⁻¹ Δb da ‖Δx‖ ≤ ‖A⁻¹‖ ‖Δb‖, y b = A x da 1 / ‖x‖ ≤ ‖A‖ / ‖b‖; se multiplican ambas.

**4. La función `inverse` de IX devuelve una matriz sin error. ¿Significa eso que el resultado es preciso?**
> No. `inverse` solo se niega cuando un pivote cae por debajo del umbral absoluto 10^-12. Una matriz con un κ grande y pivotes mayores se invierte en silencio, y el resultado puede perder unos log₁₀ κ dígitos. Un κ₂ calculado con la `svd` de IX es solo un diagnóstico, no una prueba de precisión: cerca de 1/u esa estimación puede ser poco fiable en sí misma (§6). Contrasta con una referencia independiente, como una inversa exacta conocida o una estimación del número de condición validada de forma independiente, antes de fiarte de los dígitos.

**Criterio de aprobación:** Explicar la cuadrícula binary64 y el modelo estándar, distinguir el error hacia adelante del error hacia atrás, demostrar la cota de κ(A), y usar κ para predecir y explicar la pérdida de dígitos, incluso en la función `inverse` de IX.

---

## Base de investigación

- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019: el formato binary64 y las operaciones correctamente redondeadas
- D. Goldberg, «What Every Computer Scientist Should Know About Floating-Point Arithmetic», *ACM Computing Surveys* 23(1), 5–48, 1991, doi:10.1145/103162.103163
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2.ª ed., SIAM, 2002: el modelo estándar, los errores hacia adelante y hacia atrás, y el número de condición de los sistemas lineales
- J. Todd, 1954, National Bureau of Standards Applied Mathematics Series 39: el crecimiento del número de condición de las matrices de Hilbert
- M.-D. Choi, «Tricks or Treats with the Hilbert Matrix», *American Mathematical Monthly* 90(5), 1983: las entradas enteras de la inversa
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §5 enlaza a su línea
- Mediciones: laboratorio de Learn `code/streeling-mathematics/` en el commit `c8135fa508fcb9d35593e8dedbb925c44282b3a2` (PR n.º 24 de Learn), que fija IX en el mismo commit; SHA-256 de la salida esperada `6d2a9590b9a37577dd1c4b670d23dbfca55a8fef529e590a246ffa33c675bedb`, SHA-256 del prerregistro `a70179d8a698f835aec724181066823368f0b38f76fe8dcb994494495e412f20`; medido en Windows 11 x86-64 (rustc 1.94.0), salida reproducida por la CI alojada en Linux, Windows y macOS (ejecución 36335008098)
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
