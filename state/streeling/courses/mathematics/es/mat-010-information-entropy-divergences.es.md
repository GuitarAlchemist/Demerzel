---
module_id: mat-010-information-entropy-divergences
department: mathematics
course: Entropía, divergencias e información mutua
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Entropía, divergencias e información mutua — Medir la incertidumbre y el coste de un modelo equivocado

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Calcular la entropía de una distribución discreta en bits y en nats, y mostrar que la distribución uniforme la maximiza
- Relacionar la entropía conjunta y la condicional mediante la regla de la cadena, y calcular la información mutua de dos variables
- Calcular la divergencia de Kullback–Leibler, demostrar que no es negativa y explicar por qué no es una distancia
- Usar la divergencia de Jensen–Shannon cuando hace falta una comparación simétrica y acotada
- Decir cómo están sesgadas las estimaciones de entropía y de información mutua obtenidas de muestras, y rastrear qué garantizan las funciones de entropía, divergencia y retardo de IX

---

## 1. Sorpresa y entropía

Un resultado de probabilidad p lleva la **sorpresa** −log p: un resultado seguro no lleva ninguna, y cada vez que la probabilidad se divide entre dos se le añade log 2, exactamente un bit cuando el logaritmo es en base 2. La **entropía** de una variable aleatoria discreta X con distribución p₁, …, p_K es su sorpresa media, H(X) = −Σ pᵢ log pᵢ, con 0 log 0 = 0, el límite de p log p cuando p → 0. La base del logaritmo fija la unidad: la base 2 da **bits**, el logaritmo natural da **nats**, y 1 bit = ln 2 ≈ 0.693 nats.

La entropía vale 0 exactamente cuando un resultado es seguro, y vale como mucho log K, con igualdad exactamente para la distribución uniforme; el §3 demuestra esta cota. El teorema de codificación de fuente de Shannon le da un sentido operativo: ningún código binario unívocamente decodificable puede usar en promedio menos de H(X) bits por símbolo, y existen códigos que se quedan a menos de un bit de ella.

### Ejercicio práctico

¿Cuál es la entropía de la distribución uniforme sobre 8 resultados, en bits y en nats? ¿Cuál es la entropía de (1/2, 1/4, 1/8, 1/8), y cómo se compara con la de la distribución uniforme sobre 4 resultados?

> *Solución:* Cada resultado tiene la sorpresa log₂ 8 = 3 bits, así que H = 3 bits, es decir 3 ln 2 ≈ 2.079 nats. Para (1/2, 1/4, 1/8, 1/8), H = 1/2 · 1 + 1/4 · 2 + 1/8 · 3 + 1/8 · 3 = 1/2 + 1/2 + 3/8 + 3/8 = 7/4 bits, por debajo de log₂ 4 = 2 bits. El código 0, 10, 110, 111 tiene exactamente esta longitud media, 1.75 bits.

---

## 2. Entropía conjunta, entropía condicional e información mutua

Para dos variables, la **entropía conjunta** H(X, Y) es la entropía del par, y la **entropía condicional** H(Y | X) = Σₓ p(x) H(Y | X = x) es la incertidumbre que queda sobre Y una vez conocida X. Cumplen la **regla de la cadena** H(X, Y) = H(X) + H(Y | X), y condicionar nunca aumenta la entropía en promedio: H(Y | X) ≤ H(Y).

La **información mutua** es la reducción de incertidumbre sobre una variable que aporta la otra: I(X; Y) = H(Y) − H(Y | X) = H(X) + H(Y) − H(X, Y). Es simétrica, nunca es negativa, y vale 0 exactamente cuando X e Y son independientes en el sentido de MAT-008. A diferencia de un coeficiente de correlación, detecta cualquier dependencia, no solo una lineal, y ningún reetiquetado biyectivo de una u otra variable la cambia.

### Ejercicio práctico

X es un bit equilibrado, e Y es igual a X salvo que se invierte con probabilidad 1/4. Calcula I(X; Y) en bits.

> *Solución:* Y también es un bit equilibrado, así que H(Y) = 1. Dado X, Y solo es incierto por la inversión, así que H(Y | X) = h(1/4), donde h(q) = −q log₂ q − (1 − q) log₂(1 − q). h(1/4) = 1/4 · 2 + 3/4 · log₂(4/3) = 2 − (3/4) log₂ 3 ≈ 0.811, así que I(X; Y) = 1 − h(1/4) = (3/4) log₂ 3 − 1 ≈ 0.189 bits. La tabla conjunta (3/8, 1/8; 1/8, 3/8) da el mismo valor mediante H(X) + H(Y) − H(X, Y).

---

## 3. La divergencia de Kullback–Leibler

La **divergencia de Kullback–Leibler** de p respecto de q es KL(p ‖ q) = Σ pᵢ log(pᵢ/qᵢ), sumada sobre los resultados con pᵢ > 0. Vale +∞ en cuanto q da probabilidad 0 a un resultado que p permite. La **desigualdad de Gibbs** afirma que KL(p ‖ q) ≥ 0, con igualdad exactamente cuando p = q. Como ln x ≤ x − 1, −KL(p ‖ q) = Σ pᵢ ln(qᵢ/pᵢ) ≤ Σ pᵢ (qᵢ/pᵢ − 1) = Σ qᵢ − 1 ≤ 0, donde las sumas recorren pᵢ > 0. Con q uniforme, KL(p ‖ q) = log K − H(p), lo que demuestra la cota del §1.

KL mide el coste de un modelo equivocado. La **entropía cruzada** H(p, q) = −Σ pᵢ log qᵢ es igual a H(p) + KL(p ‖ q): codificar datos que siguen p con las longitudes de código ideales −log₂ qᵢ de q cuesta en promedio KL(p ‖ q) bits de más por símbolo, y minimizar la pérdida logarítmica de un clasificador minimiza la divergencia de su modelo respecto de los datos. KL no es una distancia: no es simétrica y no cumple la desigualdad triangular. La información mutua es ella misma una divergencia, I(X; Y) = KL(p(x, y) ‖ p(x) p(y)), el coste de suponer independencia.

### Ejercicio práctico

Sean p = (3/4, 1/4) y q = (1/2, 1/2). Calcula KL(p ‖ q) y KL(q ‖ p) en nats.

> *Solución:* KL(p ‖ q) = 3/4 · ln(3/2) + 1/4 · ln(1/2) = (3/4) ln 3 − ln 2 ≈ 0.131, que también es ln 2 − H(p). KL(q ‖ p) = 1/2 · ln(2/3) + 1/2 · ln 2 = (1/2) ln(4/3) ≈ 0.144. Los dos sentidos difieren, e intercambiar los argumentos puede incluso convertir un valor finito en +∞: KL((1, 0) ‖ (1/2, 1/2)) = ln 2, mientras que KL((1/2, 1/2) ‖ (1, 0)) es infinita.

---

## 4. La divergencia de Jensen–Shannon

La **divergencia de Jensen–Shannon** compara p y q con su mezcla m = (p + q)/2: JS(p, q) = ½ KL(p ‖ m) + ½ KL(q ‖ m) = H(m) − (H(p) + H(q))/2. Es simétrica y siempre finita, ya que m es positiva donde lo sea p o q. Está acotada por ln 2: m ≥ p/2, así que cada pᵢ/mᵢ ≤ 2 y KL(p ‖ m) ≤ ln 2, y lo mismo vale para q. La cota se alcanza exactamente cuando p y q tienen soportes disjuntos. JS es la información mutua entre una moneda equilibrada que elige p o q y el resultado extraído después, y su raíz cuadrada es una métrica.

### Ejercicio práctico

Calcula JS((1, 0), (1/2, 1/2)) en nats y en bits, y compárala con la cota.

> *Solución:* m = (3/4, 1/4). KL((1, 0) ‖ m) = ln(4/3), y KL((1/2, 1/2) ‖ m) = 1/2 · ln(2/3) + 1/2 · ln 2 = (1/2) ln(4/3). Así que JS = (1/2) ln(4/3) + (1/4) ln(4/3) = (3/4) ln(4/3) ≈ 0.216 nats, es decir (3/4) log₂(4/3) ≈ 0.311 bits, muy por debajo de ln 2 ≈ 0.693 nats, un bit. Es finita aunque una de las dos divergencias KL entre estas distribuciones no lo es.

---

## 5. Estimar la información a partir de muestras

En la práctica p es desconocida, y el **estimador por sustitución** la reemplaza por las frecuencias observadas. La entropía por sustitución está sesgada hacia abajo: las frecuencias se ajustan a la muestra, y los resultados no observados no contribuyen. Para N observaciones de K resultados, el desarrollo de primer orden de Miller da E[Ĥ] ≈ H − (K − 1)/(2N) nats. La información mutua por sustitución está sesgada hacia arriba: para variables independientes con B_X y B_Y clases de probabilidad positiva, y suficientes observaciones en cada celda, 2N Î es el estadístico G de una prueba de independencia, aproximadamente χ² con (B_X − 1)(B_Y − 1) grados de libertad, así que E[Î] ≈ (B_X − 1)(B_Y − 1)/(2N) nats aunque el valor verdadero es 0.

Las variables continuas añaden una elección de clases. Con clases de anchura Δ, la entropía por clases es cercana a h(X) − log Δ, donde h es la entropía diferencial, así que crece sin límite cuando las clases se estrechan; dos entropías por clases solo son comparables con las mismas clases y el mismo intervalo. Una divergencia KL por sustitución es infinita en cuanto una clase está vacía en la muestra de q y no en la de p, y suavizar los recuentos la hace finita, pero su valor depende entonces del suavizado.

### Ejercicio práctico

Se lanza dos veces una moneda equilibrada, y se estima la entropía a partir de los dos resultados. ¿Cuál es la estimación por sustitución esperada en nats, y cómo se compara con la entropía verdadera?

> *Solución:* Con probabilidad 1/2 los lanzamientos coinciden, las frecuencias son (1, 0) y Ĥ = 0; con probabilidad 1/2 difieren, las frecuencias son (1/2, 1/2) y Ĥ = ln 2. Así que E[Ĥ] = (ln 2)/2 ≈ 0.347, la mitad del valor verdadero ln 2 ≈ 0.693. La corrección de primer orden (K − 1)/(2N) = 1/4 solo la llevaría a unos 0.60: el desarrollo supone N grande frente a K.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado las pruebas de IX.

**Divergencias** (`crates/ix-math/src/inference.rs`). [`shannon_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L176), [`kl_divergence`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L187) y [`js_divergence`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L212) trabajan en nats, y primero pasan sus entradas por `normalize`, así que aceptan cualquier peso no negativo y multiplicarlos por una constante no cambia nada. `kl_divergence` [devuelve un error](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L199) cuando q es 0 donde p es positiva, en lugar de +∞, y el comentario de documentación de `js_divergence` [enuncia la cota](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L211) [0, ln 2]. La prueba [`entropy_and_divergences`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L569) comprueba la distribución uniforme sobre 4 resultados, una masa puntual, KL((1, 0) ‖ (1/2, 1/2)) = ln 2, JS de soportes disjuntos y el caso de error. La extensión de DuckDB expone las tres funciones en SQL como [`ix_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L143), [`ix_kl`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L192) e [`ix_js`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L205).

```rust
fn normalize(p: &[f64]) -> Result<Vec<f64>, MathError> {
    if p.is_empty() {
        return Err(MathError::EmptyInput);
    }
    if p.iter().any(|&v| v < 0.0 || v.is_nan()) {
        return Err(MathError::InvalidParameter(
            "probability vector must be non-negative".into(),
        ));
    }
    let total: f64 = p.iter().sum();
    if total <= 0.0 {
        return Err(MathError::InvalidParameter(
            "probability vector sums to zero".into(),
        ));
    }
    Ok(p.iter().map(|v| v / total).collect())
}
```

- **Un total que desborda da tres respuestas distintas.** `normalize` rechaza [los pesos negativos y NaN](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L161) pero no +∞, y su [suma](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L166) puede desbordar. Para los pesos (10^308, 10^308), el total 2 · 10^308 supera el mayor `f64`, unos 1.8 · 10^308, así que se vuelve +∞ y cada peso normalizado se vuelve 0. `shannon_entropy` omite entonces todos los términos y devuelve −0.0 en lugar de ln 2, `kl_divergence` contra (1, 3) devuelve 0 en lugar de unos 0.144, y `js_divergence` devuelve el error «probability vector sums to zero», porque vuelve a normalizar el vector nulo. Un peso +∞ pasa la comprobación y se normaliza en NaN: para (+∞, 1), la entropía vuelve a ser −0.0, KL contra (1, 1) vale 0, y JS falla con «must be non-negative». Son predicciones sacadas de una transcripción línea a línea, no de una ejecución; MAT-003 trata el desbordamiento, y el §7 las comprueba.
- **Las cotas solo se cumplen salvo redondeo.** KL ≥ 0 y JS ≤ ln 2 son teoremas sobre sumas exactas, y las sumas calculadas se redondean. Para p y q casi iguales, los términos de la suma de KL casi se cancelan, así que el redondeo puede dejar un resultado ligeramente por debajo de 0; para p y q casi disjuntas, JS está en su cota, y el redondeo puede empujarla ligeramente por encima de ln 2. Cada error es del orden de la unidad de redondeo de `f64`, 2^-53 ≈ 1.1 · 10^-16, multiplicada por el tamaño de los términos. Esto se sigue de cómo funciona el redondeo, no de una ejecución; el paso 3 del §7 lo comprueba. La prueba de IX compara con una tolerancia, como debe; quien llame a la función y compruebe `kl >= 0.0` exactamente puede fallar.
- **El mismo nombre mide otra cosa en `ix-code`.** Su función [`shannon_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L145) toma valores brutos, los cuenta en clases de la misma anchura y [divide la entropía en bits entre log₂ del número de clases](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L176), lo que da un número en [0, 1]. Devuelve 0 cuando el rango vale como mucho [`f64::EPSILON`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L152) en valor absoluto, así que los valores 10^-20 y 2 · 10^-20, que difieren en un factor 2, reciben la entropía 0, mientras que 1 y 2 reciben 1/log₂ 10 ≈ 0.301 con 10 clases.
- **La perplejidad es coherente.** Las dos implementaciones de t-SNE comparan una entropía en nats con el logaritmo natural de la perplejidad objetivo, [en `ix-manifold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-manifold/src/lib.rs#L182), cuya [`entropy_of`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-manifold/src/lib.rs#L242) usa `ln`, y [en `ix-unsupervised`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/tsne.rs#L75). La perplejidad es por tanto e^H con H en nats, el mismo número que 2^H con H en bits.
- **La pérdida de entropía cruzada está acotada.** [`binary_cross_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-nn/src/loss.rs#L18) lleva las predicciones [a 10^-12 de 0 y de 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-nn/src/loss.rs#L19), así que una predicción errónea y segura de sí misma cuesta unos 27.63 nats por elemento en lugar de +∞.
- **La información mutua solo existe dentro de `optimal_delay`.** Ninguna función de IX calcula I(X; Y). [`optimal_delay`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L29) estima la información mutua entre una serie y su copia desplazada a partir de un [histograma bidimensional](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L71), y devuelve el último retardo antes de que la estimación [suba por primera vez](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L77), la regla de Fraser y Swinney. Su estimación es la de sustitución, con el sesgo hacia arriba del §5.
- **Su prueba acepta todos los resultados posibles.** [`test_optimal_delay_sine`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L188) pasa 2000 muestras de una sinusoide de periodo 100, con como mucho 50 retardos y 16 clases. Su [comentario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L194) espera unos 25, un cuarto de periodo, pero solo [afirma](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L197) un retardo entre 1 y 50, y con esta entrada la función no puede devolver otra cosa: su resultado está entre 1 y el menor del límite de retardo y n/2, aquí 50. Una transcripción predice 5. La estimación por clases baja a 1.584 nats en el retardo 5 y sube a 1.628 en el retardo 6, así que la regla de la primera subida se detiene ahí. Con 1 clase, cada estimación vale 0, la estimación nunca sube, y la función devuelve el límite de retardo, 50. Con 0 clases, [`num_bins - 1`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L43) pasa por debajo de cero y la llamada entra en pánico: en la resta cuando las comprobaciones de desbordamiento están activas, como en la compilación de depuración por defecto, y si no, en un índice fuera de rango.

```rust
        let delay = optimal_delay(&data, 50, 16);
        // Optimal delay for a sine wave should be around T/4 = 25
        // The mutual information method can vary; accept a wider range
        assert!(
            (1..=50).contains(&delay),
            "Optimal delay for sine: {}",
            delay
        );
```

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

¿Por qué `shannon_entropy` devuelve −0.0 para los pesos (10^308, 10^308), y qué devolvería si `normalize` dividiera primero cada peso entre el mayor?

> *Solución:* La suma 10^308 + 10^308 = 2 · 10^308 supera el mayor `f64`, unos 1.8 · 10^308, así que se redondea a +∞, y cada peso dividido entre +∞ vale 0. El filtro solo conserva los pesos positivos, la suma de ningún término vale 0, y su opuesto vale −0.0. Dividir primero entre el mayor peso da (1, 1), cuya suma 2 es exacta, y luego (1/2, 1/2), cuya entropía vale ln 2 ≈ 0.693. Esto es aritmética sobre el código, no una ejecución; el §7 lo comprueba.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **Valores nominales.** Llama a `shannon_entropy` con ocho pesos iguales, a `kl_divergence` con (3, 1) contra (1, 1) y en sentido inverso, y a `js_divergence` con (1, 0) y (1, 1). Predicción: 3 ln 2 ≈ 2.079, luego 0.131 y 0.144, luego (3/4) ln(4/3) ≈ 0.216, cada uno con un error menor que 10^-12.
2. **Desbordamiento e infinito.** Llama a las tres funciones con (10^308, 10^308), con (1, 3) como segundo argumento, y luego con (+∞, 1) y (1, 1). Predicción: −0.0, 0 y el error «sums to zero», luego −0.0, 0 y el error «must be non-negative».
3. **Cotas y redondeo.** Extrae 10^5 pares de vectores de pesos casi iguales y casi disjuntos con un generador con semilla. Predicción: algunos valores de KL por debajo de 0 y algunos valores de JS por encima de ln 2, todos a menos de 10^-15 de la cota.
4. **Sesgo por sustitución.** Para 100 semillas, extrae 1999 pares de valores uniformes independientes, reparte cada coordenada en 16 clases iguales y calcula Î = Ĥ(X) + Ĥ(Y) − Ĥ(X, Y) con `shannon_entropy` sobre los recuentos. Predicción: cada Î es positiva, y su media está cerca de 15²/(2 · 1999) ≈ 0.056 nats.
5. **El retardo.** Llama a `optimal_delay` con la sinusoide de `test_optimal_delay_sine` y 16 clases, 1 clase y 0 clases. Predicción: 5, luego 50, luego un pánico.
6. **La entropía por clases.** Llama a la función `shannon_entropy` de `ix-code` con (0, 1) y 2 clases, con (10^-20, 2 · 10^-20) y 10 clases, y con (1, 2) y 10 clases. Predicción: 1, luego 0, luego 1/log₂ 10 ≈ 0.301.
7. **El acotamiento.** Llama a `binary_cross_entropy` con la predicción 0 y el objetivo 1. Predicción: 12 ln 10 ≈ 27.63.

### Ejercicio práctico

En el paso 4, ¿por qué la media sigue siendo positiva aunque las variables son independientes, y qué media darían diez veces más pares?

> *Solución:* La estimación por sustitución es la divergencia de las frecuencias conjuntas observadas respecto del producto de las marginales observadas, y el ruido de muestreo basta para que difieran, así que Î > 0 en casi cualquier muestra. Su media es de unos (B_X − 1)(B_Y − 1)/(2N) = 225/3998 ≈ 0.056 nats. Con diez veces más pares, baja diez veces, a unos 0.0056: el sesgo decrece como 1/N, y una estimación positiva solo indica dependencia si supera claramente lo que dan datos independientes, por ejemplo después de barajar una de las variables.

---

## 8. Errores comunes

- **Mezclar bits y nats.** Un bit vale ln 2 ≈ 0.693 nats. `inference.rs` de IX trabaja en nats, e `ix-code` devuelve bits normalizados.
- **Tratar KL como una distancia.** No es simétrica y no tiene desigualdad triangular; usa JS, o su raíz cuadrada, cuando haga falta una comparación simétrica.
- **Dejar que q se anule donde p no se anula.** KL es entonces infinita, y el suavizado solo la hace finita a costa de un valor que depende del suavizado.
- **Fiarse de una estimación por sustitución obtenida de pocas muestras.** La entropía sale demasiado baja y la información mutua demasiado alta; compara con datos barajados.
- **Comparar entropías por clases calculadas con clases distintas.** La entropía por clases de una variable continua depende tanto de la anchura de las clases como de los datos.
- **Comprobar una cota exactamente en coma flotante.** Una KL calculada puede quedar ligeramente por debajo de 0; compara con una tolerancia.
- **Escribir una prueba cuyo intervalo aceptado contiene todos los resultados posibles.** Comprueba el valor que espera el comentario, con la tolerancia que permite el método.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Sorpresa** | −log p, la información que lleva un resultado de probabilidad p |
| **Entropía** | La sorpresa media de una variable aleatoria, −Σ pᵢ log pᵢ |
| **Bit y nat** | Las unidades de entropía para los logaritmos en base 2 y natural; 1 bit = ln 2 nats |
| **Entropía condicional** | H(Y \| X), la incertidumbre que queda sobre Y una vez conocida X |
| **Información mutua** | I(X; Y) = H(X) + H(Y) − H(X, Y), nula exactamente en caso de independencia |
| **Divergencia KL** | KL(p ‖ q) = Σ pᵢ log(pᵢ/qᵢ), el coste de usar q cuando los datos siguen p |
| **Entropía cruzada** | H(p, q) = H(p) + KL(p ‖ q), la pérdida logarítmica del modelo q sobre datos que siguen p |
| **Desigualdad de Gibbs** | KL(p ‖ q) ≥ 0, con igualdad exactamente cuando p = q |
| **Divergencia de Jensen–Shannon** | La divergencia KL media de p y q respecto de su mezcla; simétrica y como mucho ln 2 |
| **Estimador por sustitución** | Una estimación que reemplaza la distribución desconocida por las frecuencias observadas |
| **Perplejidad** | e^H con H en nats, el número efectivo de resultados equiprobables |

---

## Autoevaluación

**1. ¿Por qué la entropía de una distribución sobre K resultados vale como mucho log K, con igualdad solo para la distribución uniforme?**
> KL(p ‖ u) = log K − H(p) para la distribución uniforme u, y la desigualdad de Gibbs la hace no negativa, con igualdad exactamente cuando p = u.

**2. KL(p ‖ q) = 0.131 y KL(q ‖ p) = 0.144. ¿Cuál es la distancia entre p y q?**
> Ninguna. KL no es simétrica: cada sentido responde a su propia pregunta, el coste de suponer q para datos que siguen p o al revés. Una comparación simétrica necesita JS o su raíz cuadrada.

**3. Dos variables, repartidas cada una en 16 clases, dan una información mutua por sustitución de 0.05 nats con 2000 observaciones. ¿Es una señal de dependencia?**
> No por sí sola. Si las 16 clases de cada variable tienen una probabilidad apreciable, de modo que las 256 celdas están razonablemente llenas, variables independientes dan en promedio unos 15²/(2 · 2000) ≈ 0.056 nats, y 0.05 es el aspecto que tiene la ausencia total de dependencia. Si la masa solo ocupa unas pocas clases, el sesgo se acerca más a (b_X − 1)(b_Y − 1)/(2N), con b_X y b_Y las clases ocupadas, y 0.05 podría reflejar una dependencia real. Una comparación con pares barajados lo decide en ambos casos.

**4. La prueba `test_optimal_delay_sine` de IX pasa. ¿Qué te dice sobre `optimal_delay`?**
> Solo que la llamada no entra en pánico con esa entrada: la prueba acepta cualquier retardo de 1 a 50, es decir cualquier valor que la función puede devolver, y no el cuarto de periodo que espera su comentario.

**Criterio de aprobación:** Calcular la entropía, la entropía condicional y la información mutua en bits y en nats, calcular e interpretar las divergencias KL y de Jensen–Shannon, demostrar la desigualdad de Gibbs y la cota log K, explicar los sesgos de las estimaciones por sustitución, y rastrear qué garantizan las funciones de entropía, divergencia, pérdida y retardo de IX.

---

## Base de investigación

- C. E. Shannon, «A mathematical theory of communication», *Bell System Technical Journal* 27, 1948: la entropía, la información mutua y la codificación de fuente
- S. Kullback y R. A. Leibler, «On information and sufficiency», *Annals of Mathematical Statistics* 22, 1951: la divergencia
- T. M. Cover y J. A. Thomas, *Elements of Information Theory*, 2.ª ed., Wiley, 2006: las reglas de la cadena, la desigualdad de Gibbs, la codificación y la entropía diferencial
- J. Lin, «Divergence measures based on the Shannon entropy», *IEEE Transactions on Information Theory* 37, 1991: la divergencia de Jensen–Shannon y su cota
- D. M. Endres y J. E. Schindelin, «A new metric for probability distributions», *IEEE Transactions on Information Theory* 49, 2003: la raíz cuadrada de JS es una métrica
- G. A. Miller, «Note on the bias of information estimates», en *Information Theory in Psychology*, Free Press, 1955: el sesgo de la entropía por sustitución
- L. Paninski, «Estimation of entropy and mutual information», *Neural Computation* 15, 2003: el sesgo de los estimadores por sustitución
- A. M. Fraser y H. L. Swinney, «Independent coordinates for strange attractors from mutual information», *Physical Review A* 33, 1986: el retardo en el primer mínimo de la información mutua
- L. van der Maaten y G. Hinton, «Visualizing data using t-SNE», *Journal of Machine Learning Research* 9, 2008: la perplejidad
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
