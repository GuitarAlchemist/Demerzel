---
module_id: mat-002-counterexamples-and-exhaustive-checks
department: mathematics
course: Contraejemplos, testigos y comprobaciones exhaustivas
level: beginner
alchemical_stage: nigredo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "35 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Contraejemplos, testigos y comprobaciones exhaustivas — Cuando comprobar casos es una demostración

> **Departamento de Matemáticas** | Etapa: Nigredo (Principiante) | Duración estimada: 35 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Distinguir un enunciado universal de uno existencial, y decir qué refuta o establece cada uno
- Refutar un enunciado universal con un solo contraejemplo, y comprobar un testigo de un enunciado existencial
- Explicar cuándo comprobar casos es una demostración: en un dominio finito, o en uno infinito reducido a un número finito de casos
- Explicar por qué las pruebas aleatorias y las búsquedas inacabadas pueden encontrar contraejemplos pero no pueden demostrar un enunciado universal
- Leer lo que establecen de verdad las pruebas de IX sobre el grupo diédrico y su analizador de redes de Petri

---

## 1. Enunciados universales y contraejemplos

Un **enunciado universal** afirma que una propiedad P se cumple para todo elemento de un dominio D: «para todo x en D, P(x)». MAT-001 mostró que ningún número de ejemplos demuestra un enunciado así. La otra dirección es mucho más barata: **un solo** x para el que P(x) es falso lo refuta. Ese x es un **contraejemplo**. En lógica, un contraejemplo es un testigo de la negación: «no (para todo x, P(x))» dice lo mismo que «existe un x tal que no P(x)».

Dos ejemplos clásicos:
- **El polinomio de Euler.** n² + n + 41 es primo para n = 0, 1, 2, …, 39: cuarenta aciertos seguidos. En n = 40 da 40² + 40 + 41 = 40 · 41 + 41 = 41 · 41 = 1681, que no es primo. Cuarenta confirmaciones no demostraron el enunciado; un solo contraejemplo lo refutó.
- **La conjetura de Euler sobre sumas de potencias.** Euler conjeturó que, para k ≥ 3, hacen falta al menos k potencias k-ésimas positivas para que su suma sea una potencia k-ésima. El enunciado resistió casi dos siglos, hasta que Lander y Parkin encontraron, mediante una búsqueda por computadora, cuatro potencias quintas cuya suma es una potencia quinta: 27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵ = 61,917,364,224. Encontrar este contraejemplo exigió una búsqueda con máquina; comprobarlo exige cinco potencias y una suma.

### Ejercicio práctico

Muestra, sin calculadora, que n² + n + 41 no es primo para n = 41.

> *Solución:* Para n = 41, cada término es múltiplo de 41: 41² + 41 + 41 = 41 · (41 + 1 + 1) = 41 · 43. El número tiene los factores 41 y 43, así que no es primo.

---

## 2. Enunciados existenciales y testigos

Un **enunciado existencial** afirma que al menos un elemento tiene la propiedad: «existe x en D tal que P(x)». Se demuestra con un **testigo**: un x explícito, junto con una comprobación de que P(x) se cumple. Un testigo vale lo que vale su comprobación, así que esta debe estar al alcance del lector.

- **Los números de Fermat.** Fermat creía que todo número 2^(2^n) + 1 es primo. Euler lo refutó con el testigo n = 5: 2^32 + 1 = 4,294,967,297 = 641 × 6,700,417. Cualquiera puede comprobar el producto sin rehacer la búsqueda que encontró 641. El mismo testigo demuestra el enunciado existencial «algún número 2^(2^n) + 1 es compuesto» y refuta el enunciado universal «todo número 2^(2^n) + 1 es primo».
- **Las comprobaciones necesarias.** Una comprobación necesaria es una prueba rápida que toda respuesta correcta debe pasar. Fallarla refuta la respuesta de inmediato; pasarla no demuestra nada. Comparar las últimas cifras es una de ellas: dos enteros iguales terminan en la misma cifra, pero también muchos enteros distintos.

Algunas demostraciones de existencia, como ciertas demostraciones por contradicción, nunca construyen un testigo. Esta lección solo trata de las que sí lo construyen.

### Ejercicio práctico

Sin calcular las potencias por completo, comprueba que 27⁵ + 84⁵ + 110⁵ + 133⁵ y 144⁵ terminan en la misma cifra. ¿Demuestra esto la identidad de Lander y Parkin?

> *Solución:* La última cifra de una potencia solo depende de la última cifra de la base. Las últimas cifras de 7, 7², …, 7⁵ son 7, 9, 3, 1, 7; las de 4, 4², …, 4⁵ son 4, 6, 4, 6, 4; las de 3, 3², …, 3⁵ son 3, 9, 7, 1, 3; y 0⁵ termina en 0. El lado izquierdo termina entonces en la última cifra de 7 + 4 + 0 + 3 = 14, es decir 4, y 144⁵ también termina en 4. La comprobación pasa, pero solo es necesaria: también pasaría una identidad falsa cuyos dos lados terminaran por casualidad en la misma cifra. La identidad se demuestra calculando los dos lados, que valen ambos 61,917,364,224.

---

## 3. Comprobaciones exhaustivas en dominios finitos

Cuando el dominio es **finito**, la regla de MAT-001 tiene una excepción: comprobar P(x) para **cada** x de D es una demostración, llamada **demostración por agotamiento**. Un enunciado universal sobre un dominio finito es una lista finita de enunciados unidos por «y», y cada uno de ellos se ha comprobado.

El tamaño de la comprobación depende de cuántas variables cuantifica el enunciado. Tomemos el **grupo diédrico D12**: las 24 rotaciones y reflexiones de un dodecágono regular, que la teoría musical usa para las transposiciones e inversiones de las 12 clases de altura.
- Un enunciado sobre un elemento, como «todo elemento tiene inverso», necesita 24 comprobaciones.
- Un enunciado sobre dos elementos, como «g · h = h · g», necesita 24² = 576.
- Un enunciado sobre tres elementos, como la **asociatividad**, (g · h) · f = g · (h · f), necesita 24³ = 13,824.

Un enunciado sobre un dominio **infinito** a veces puede reducirse a un número finito de casos. La reducción es un paso de la demostración; las comprobaciones hacen el resto.

### Ejercicio práctico

Demuestra que, para todo entero n, el resto de dividir n² entre 4 es 0 o 1.

> *Solución:* Escribamos n = 4q + r con r ∈ {0, 1, 2, 3}. Entonces n² = 16q² + 8qr + r², así que n² y r² dejan el mismo resto al dividir entre 4. Esto reduce el dominio infinito a cuatro casos: r² = 0, 1, 4, 9 dejan los restos 0, 1, 0, 1. El enunciado se cumple en cada caso, así que se cumple para todo entero. Como consecuencia, una suma de dos cuadrados deja resto 0, 1 o 2 al dividir entre 4, nunca 3.

---

## 4. ¿Demostración o comprobación?

Escribamos cada elemento de D12 como un par (i, a), donde i cuenta los pasos de rotación (de 0 a 11) y a = 1 marca una reflexión. Con σ(a) = (−1)^a, el producto es

(i, a) · (k, b) = (i + σ(a) · k mod 12, a ⊕ b),

donde ⊕ es la suma módulo 2. El cambio de signo expresa la regla de que una reflexión invierte el sentido de una rotación. Es la regla que implementa IX (§6).

**Teorema.** Este producto es asociativo, y la demostración vale para todo módulo, no solo para 12.

*Demostración (directa, como en MAT-001):* tomemos g₁ = (i, a), g₂ = (k, b) y g₃ = (m, c), con todas las partes de rotación tomadas módulo 12.
- (g₁ · g₂) · g₃ = (i + σ(a)k, a ⊕ b) · (m, c) = (i + σ(a)k + σ(a ⊕ b)m, a ⊕ b ⊕ c).
- g₁ · (g₂ · g₃) = (i, a) · (k + σ(b)m, b ⊕ c) = (i + σ(a)k + σ(a)σ(b)m, a ⊕ b ⊕ c).
- Ambos coinciden porque σ(a ⊕ b) = σ(a)σ(b): el signo de dos marcas de reflexión combinadas es el producto de sus signos. ∎

La demostración y una comprobación exhaustiva hacen trabajos distintos:
- La **demostración** cubre la fórmula, para todo módulo. No dice nada sobre si un programa dado implementa la fórmula.
- Una **comprobación exhaustiva** del producto de un programa sobre las 13,824 ternas cubre ese programa, solo para D12.

Además, una comprobación solo detecta los errores a los que es sensible. Quita el cambio de signo, (i, a) · (k, b) = (i + k, a ⊕ b), y el producto sigue siendo asociativo: es otro grupo, Z12 × Z2. Una comprobación de asociatividad no puede ver el signo que falta. Una comprobación de la relación «reflexión, luego rotación, luego reflexión da la rotación inversa» sí puede.

Hay un segundo camino de los pares a las ternas. Hagamos que cada elemento g = (i, a) actúe sobre las 12 clases de altura mediante la función π_g(p) = i + σ(a)p mod 12. Si π_{g·h} = π_g ∘ π_h para todo par, y elementos distintos dan funciones distintas, la asociatividad se hereda de la composición de funciones, que siempre es asociativa: π_{(g·h)·f} = π_g ∘ π_h ∘ π_f = π_{g·(h·f)}, de donde (g · h) · f = g · (h · f). Una comprobación sobre los pares, junto con este argumento, demuestra un enunciado sobre ternas. El §6 muestra que IX tiene una prueba exactamente de esta forma.

### Ejercicio práctico

Una implementación defectuosa toma el signo del segundo factor: (i, a) · (k, b) = (i + σ(b) · k mod 12, a ⊕ b). Muestra que no es asociativa, con g₁ = (0, 0), g₂ = (1, 0) y g₃ = (0, 1).

> *Solución:* A la izquierda, g₁ · g₂ = (0 + 1, 0) = (1, 0), y luego (1, 0) · (0, 1) = (1 − 0, 1) = (1, 1). A la derecha, g₂ · g₃ = (1 − 0, 1) = (1, 1), y luego g₁ · (1, 1) = (0 − 1, 1) = (11, 1). Como (1, 1) ≠ (11, 1), esta sola terna refuta la asociatividad: un contraejemplo entre las 13,824 ternas basta.

---

## 5. Cuando la búsqueda es incompleta

Las búsquedas son asimétricas:
- Un contraejemplo encontrado por una búsqueda **parcial** es concluyente. Refuta el enunciado universal, por pequeña que sea la parte del dominio explorada.
- Una búsqueda parcial que no encuentra **ningún** contraejemplo no demuestra nada sobre la parte que no exploró.

Las **pruebas aleatorias** son una búsqueda parcial. QuickCheck (Claessen y Hughes, 2000) las convirtió en una herramienta habitual: se enuncia una propiedad, y la herramienta la comprueba en muchas entradas generadas al azar, informando de cualquier entrada en la que falle. Un fallo informado es un contraejemplo. Mil aciertos son un indicio, no una demostración: en un dominio infinito, la parte sin explorar sigue siendo infinita. En un dominio finito pequeño, una comprobación exhaustiva es mejor, porque es una demostración; para la asociatividad en D12 solo tiene 13,824 casos.

Una herramienta honesta mantiene visible la diferencia. Una **red de Petri** modela un sistema mediante fichas que se mueven entre lugares; un *marcado* es un estado del sistema, y un marcado está *muerto* cuando ya no puede ocurrir nada a partir de él. El analizador de redes de Petri de IX, tema de MAT-023, explora los marcados que una red puede alcanzar y devuelve uno de tres veredictos para cada propiedad ([`Verdict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L89)):
- `Holds`: la propiedad se cumple, y esto es lo que se midió;
- `Fails`: la propiedad no se cumple, y este es el contraejemplo;
- `Unknown`: la propiedad no se decidió dentro de los límites de la exploración, y esta es la razón.

`Unknown` nunca cuenta como un acierto: el método [`holds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L100) solo es verdadero para `Holds`.

### Ejercicio práctico

Un analizador se detiene en su límite de estados tras explorar un millón de marcados, ninguno muerto, y da para la ausencia de bloqueos el veredicto `Unknown`. Un colega concluye que la red está libre de bloqueos. ¿Qué falla? Y si el analizador hubiera encontrado un marcado muerto entre sus diez primeros estados, ¿debilitaría ese resultado la parada temprana?

> *Solución:* «Ningún marcado alcanzable está muerto» es un enunciado universal sobre todos los marcados alcanzables, y el analizador solo exploró algunos. Entre los demás puede haber un marcado muerto, así que `Unknown` es la respuesta honesta y la conclusión del colega no se sigue. Un marcado muerto encontrado es un contraejemplo: la secuencia de disparos que lo alcanza puede reproducirse desde el marcado inicial, quede lo que quede sin explorar. La parada temprana no lo debilita.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica. No ha ejecutado las pruebas de IX: si pasan en ese commit es una cuestión para el experimento del §7.

**El grupo diédrico.** [`DihedralElement`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L16) guarda una rotación de 0 a 11 y una marca de reflexión, e implementa el trait [`Group`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L6). Su producto, copiado literalmente de las líneas 66 a 77 de `dihedral.rs`, es la regla del §4:

```rust
    fn compose(&self, other: &Self) -> Self {
        // (r^i s^j)(r^k s^l) = r^(i + (-1)^j · k) s^(j+l).
        // The sign flip encodes sr = r^(-1)s: rotation "conjugates" through reflection.
        let i = self.rotation as i16;
        let k = other.rotation as i16;
        let sign: i16 = if self.reflected { -1 } else { 1 };
        let new_rot = (i + sign * k).rem_euclid(12) as u8;
        Self {
            rotation: new_rot,
            reflected: self.reflected ^ other.reflected,
        }
    }
```

La prueba [`group_law_exhaustive_closure_and_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L137) es exhaustiva sobre los elementos y los pares, no sobre las ternas:
- para cada uno de los 24 elementos, afirma g · g⁻¹ = e, g⁻¹ · g = e, e · g = g y g · e = g;
- para cada uno de los 576 pares, afirma que la rotación de g · h es menor que 12 ([línea 148](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L148));
- afirma que los 576 productos incluyen los 24 elementos ([línea 158](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L158)).

Ninguna prueba de `dihedral.rs` enuncia la asociatividad. La prueba [`action_composition_matches_group_composition`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L135) hace más de lo que parece. Para cada uno de los 576 pares y cada uno de nueve conjuntos de clases de altura x tomados como muestra, afirma (g · h) · x = g · (h · x), donde la acción [`apply`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L40) está escrita aparte de `compose`: envía cada clase de altura p a −p si el elemento es una reflexión, y luego rota. Es la función π_g del §4. Uno de los conjuntos de la muestra, el acorde de do mayor {0, 4, 7}, es enviado por los 24 elementos a 24 conjuntos distintos: los 12 acordes mayores y los 12 acordes menores. Así, para cada par, un solo elemento envía {0, 4, 7} a g · (h · {0, 4, 7}), a saber, el verdadero producto de D12, y la prueba obliga a `compose` a devolverlo. Si esta prueba pasa, los 576 productos son todos correctos, y la asociatividad se sigue de la demostración del §4 sin ningún bucle sobre ternas.

**El analizador de redes de Petri.** [`analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L436) explora los marcados alcanzables hasta sus límites. Su veredicto sobre bloqueos, copiado literalmente de las líneas 483 a 491 de `analysis.rs`, es la asimetría del §5 escrita en código:

```rust
    let deadlock_free = if deadlock_count > 0 {
        Verdict::Fails(deadlocks)
    } else if complete {
        Verdict::Holds(Vec::new())
    } else {
        Verdict::Unknown {
            reason: unknown("deadlock freedom"),
        }
    };
```

Un marcado muerto encontrado da `Fails` tanto si la exploración terminó como si no: como dice el comentario situado encima de este código ([línea 460](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L460)), su secuencia testigo lo alcanza desde el marcado inicial y el disparo es determinista. La ausencia de marcados muertos da `Holds` solo si la exploración terminó (`complete`), y `Unknown` en caso contrario. La prueba [`witness_sequences_are_shortest_and_replayable`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L809) construye una red pequeña con un camino corto y otro largo hacia el mismo marcado muerto, afirma que el testigo informado es el corto, `a_short`, y lo reproduce con `fire` para comprobar que alcanza el marcado informado.

**Las pruebas basadas en propiedades.** IX declara la biblioteca `proptest`, una herramienta de Rust de la familia QuickCheck, en el manifiesto de su espacio de trabajo ([`Cargo.toml` línea 211](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L211)) y en cinco crates, pero en ese commit ningún archivo Rust la usa. En IX, las pruebas basadas en propiedades son teoría, no práctica.

### Ejercicio práctico

¿Qué aserción de `group_law_exhaustive_closure_and_inverse` no puede fallar nunca, y por qué? Considera luego un producto defectuoso que solo difiere del de IX en una entrada: (1, 1) · (2, 1) devuelve (5, 0) en lugar de (11, 0). ¿Cuál de las dos pruebas de D12 anteriores lo detectaría?

> *Solución:* «La rotación de g · h es menor que 12» no puede fallar nunca: `compose` reduce la rotación con `rem_euclid(12)`, que siempre devuelve un valor de 0 a 11, y una aserción que no puede fallar no comprueba nada. El producto defectuoso pasa todas las aserciones de `dihedral.rs`: las aserciones de identidad e inverso solo usan pares que contienen e, o un elemento y su inverso, y (2, 1) no es el inverso de (1, 1), ya que cada reflexión es su propio inverso; los 576 productos siguen incluyendo los 24 elementos; y las demás pruebas del archivo usan otros productos. Sin embargo, la regla defectuosa no es asociativa: con g₁ = (1, 0), g₂ = (0, 1) y g₃ = (2, 1), (g₁ · g₂) · g₃ = (1, 1) · (2, 1) = (5, 0), mientras que g₂ · g₃ = (0 − 2, 0) = (10, 0) y g₁ · (10, 0) = (11, 0). La prueba de la acción lo detecta: π_(1,1) ∘ π_(2,1) envía p a 1 − (2 − p) = p − 1, que es π_(11,0), así que solo (11, 0) envía {0, 4, 7} al conjunto correcto.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados.

1. **La asociatividad, exhaustivamente.** Comprobar (g · h) · f = g · (h · f) con la función `compose` de IX para las 13,824 ternas y contar los fallos. Predicción: ninguno, por la demostración del §4.
2. **Controles negativos.** Pasar el mismo comprobador por la regla defectuosa del ejercicio del §4 y por el producto defectuoso de una entrada del ejercicio del §6. Predicción: al menos una terna que falla para cada uno, entre ellas las dos ternas encontradas a mano más arriba. Un comprobador que no informa aquí de ningún fallo está roto, y su veredicto del paso 1 no significaría nada.
3. **Qué detectan las pruebas de IX.** Reescribir las aserciones de `group_law_exhaustive_closure_and_inverse` y de `action_composition_matches_group_composition` como comprobaciones de una regla de producto cualquiera, y aplicarlas a la función `compose` de IX y a las dos reglas defectuosas. Predicción: la función `compose` de IX pasa las dos; el producto defectuoso de una entrada pasa la primera y falla la segunda; la regla del ejercicio del §4 falla las dos, la primera ya en e · g = g, puesto que e · (1, 1) = (0 − 1, 1) = (11, 1).
4. **Reproducir un testigo.** Construir la red de `witness_sequences_are_shortest_and_replayable`, ejecutar `analyze` con los límites por defecto, y reproducir el testigo informado con `fire`. Predicción: la ausencia de bloqueos es `Fails`, el testigo es `a_short`, y la reproducción alcanza el marcado muerto informado.

### Ejercicio práctico

¿Por qué el paso 2 debe salir bien antes de que alguien confíe en el paso 1?

> *Solución:* Un comprobador que anuncia «ningún fallo» puede tener razón, o ser incapaz de fallar, como la aserción «rotación menor que 12» del §6. Pasarlo por reglas que se sabe que son falsas muestra que sabe detectar un fallo. Solo entonces su silencio sobre la función `compose` de IX significa algo: junto con la demostración del §4, dice que ese código implementa un producto asociativo.

---

## 8. Errores comunes

- **Tomar muchas confirmaciones por una demostración.** El polinomio de Euler pasó cuarenta casos y falló en el cuadragésimo primero.
- **Comprobar sobre el número equivocado de variables.** Un enunciado sobre ternas no se comprueba con un bucle sobre pares, salvo que un argumento como el del §4 los relacione.
- **Escribir aserciones que no pueden fallar.** Asegúrate de que cada aserción fallaría para alguna implementación incorrecta; si no, no prueba nada.
- **Contar `Unknown` como un acierto.** «Ningún contraejemplo encontrado dentro de los límites» no es «ningún contraejemplo».
- **Confiar en un comprobador que nunca ha fallado.** Pásalo primero por un fallo conocido: un control negativo.
- **Confundir una comprobación necesaria con una verificación.** Que coincidan las últimas cifras hace plausible una identidad, no verdadera.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Enunciado universal** | Un enunciado según el cual una propiedad se cumple para todo elemento de un dominio: «para todo x, P(x)» |
| **Enunciado existencial** | Un enunciado según el cual al menos un elemento tiene una propiedad: «existe x tal que P(x)» |
| **Contraejemplo** | Un elemento para el que un enunciado universal es falso; uno solo basta para refutarlo |
| **Testigo** | Un elemento explícito, con una comprobación, que demuestra un enunciado existencial |
| **Demostración por agotamiento** | Una demostración que comprueba cada caso de un dominio finito, o los casos en número finito a los que se reduce uno infinito |
| **Comprobación necesaria** | Una prueba que toda respuesta correcta pasa: fallarla refuta, pasarla no demuestra nada |
| **Pruebas aleatorias** | Comprobar una propiedad enunciada en muchas entradas generadas al azar: encuentran contraejemplos pero no demuestran nada sobre las entradas que omiten |
| **Control negativo** | Pasar un comprobador por un caso que se sabe incorrecto, para mostrar que puede fallar |
| **Asociatividad** | (g · h) · f = g · (h · f) para todos g, h, f: un enunciado sobre ternas |
| **Grupo diédrico D12** | Las 24 rotaciones y reflexiones de un dodecágono regular, usadas para las transposiciones e inversiones de las clases de altura |

---

## Autoevaluación

**1. Una propiedad se ha cumplido para el primer millón de enteros positivos. ¿Está demostrada?**
> No. Es un enunciado universal sobre un dominio infinito, y un millón de casos deja infinitos sin comprobar; n² + n + 41 fue primo cuarenta veces antes de fallar. Hace falta una demostración, quizá una que reduzca el enunciado a un número finito de casos.

**2. ¿Por qué 13,824 comprobaciones demuestran que un producto de D12 es asociativo, mientras que 10,000 ternas de enteros al azar no demuestran nada sobre una operación definida en todos los enteros?**
> D12 tiene 24 elementos, así que sus 13,824 ternas son todos los casos: la comprobación es una demostración por agotamiento. 10,000 ternas de enteros al azar dejan infinitas sin probar, y cualquiera de ellas podría ser un contraejemplo.

**3. ¿Puede una comprobación sobre los 576 pares de D12 establecer la asociatividad?**
> No por sí sola: la asociatividad es un enunciado sobre ternas, y una comprobación sobre pares ni siquiera lo enuncia. Sí puede junto con un argumento que relacione los pares con las ternas, como una acción: si π_{g·h} = π_g ∘ π_h para todo par y elementos distintos actúan de forma distinta, la asociatividad se sigue de la de la composición de funciones. La prueba de la acción de IX tiene esta forma.

**4. El analizador de Petri de IX da para la ausencia de bloqueos el veredicto `Unknown`. ¿Qué puedes concluir?**
> Solo que no se encontró ningún marcado muerto en la parte explorada antes del límite. No se sigue nada sobre el resto, así que no es un acierto. Si se hubiera encontrado un marcado muerto, el veredicto sería `Fails`, con un testigo reproducible, incluso tras una parada temprana.

**Criterio de aprobación:** Refutar un enunciado universal con un contraejemplo, comprobar un testigo, reconocer cuándo una comprobación finita es una demostración, y explicar por qué las pruebas aleatorias y las búsquedas inacabadas no demuestran enunciados universales, incluso en las pruebas de IX y en su analizador de Petri.

---

## Base de investigación

- I. Lakatos, *Proofs and Refutations: The Logic of Mathematical Discovery*, Cambridge University Press, 1976: el papel de los contraejemplos en el desarrollo de las matemáticas
- L. J. Lander y T. R. Parkin, «Counterexample to Euler's conjecture on sums of like powers», *Bulletin of the American Mathematical Society* 72, 1079, 1966
- K. Claessen y J. Hughes, «QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs», *Proceedings of the Fifth ACM SIGPLAN International Conference on Functional Programming (ICFP 2000)*, 268–279, doi:10.1145/351240.351266
- El polinomio de Euler n² + n + 41 y su factorización de 2^32 + 1 son clásicos; cada número de esta lección puede comprobarse a mano o por cálculo directo
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código de los §5 y §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
