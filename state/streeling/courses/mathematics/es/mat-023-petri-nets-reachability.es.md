---
module_id: mat-023-petri-nets-reachability
department: mathematics
course: Redes de Petri y alcanzabilidad
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-002-counterexamples-and-exhaustive-checks]
estimated_duration: "55 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Redes de Petri y alcanzabilidad — Lo que prueba la enumeración, y cuándo debe responder Unknown

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 55 minutos

## Objetivos

Al terminar esta lección, podrás:
- Definir una red de lugares y transiciones y su regla de disparo, y disparar secuencias a mano
- Construir un grafo de alcanzabilidad en anchura, y leer en él los bloqueos y sus testigos más cortos
- Contar los marcados alcanzables con una matriz de transferencia, y explicar por qué los espacios de estados crecen exponencialmente
- Probar que una red no está acotada con un testigo de bombeo, y decir lo que no prueba el hecho de no encontrar ninguno
- Leer la vivacidad y la reversibilidad en las componentes fuertemente conexas de un grafo de alcanzabilidad finito
- Usar la matriz de incidencia y los P-invariantes para probar la acotación y la exclusión mutua sin enumerar, y explicar por qué la ecuación de estado es solo una condición necesaria
- Seguir lo que decide el crate `ix-petri` de IX, cuáles de sus veredictos sobreviven a una búsqueda truncada, y dónde debe responder `Unknown`

---

## 1. Lugares, transiciones y regla de disparo

Una **red de lugares y transiciones** tiene un conjunto finito de lugares, un conjunto finito de transiciones, y arcos ponderados que van de un lugar a una transición o de una transición a un lugar, nunca entre dos lugares ni entre dos transiciones. Escribimos Pre(p, t) para el peso del arco del lugar p a la transición t, y Post(p, t) para el peso del arco de t a p, con 0 donde no hay arco. Un **marcado** m da a cada lugar un número de marcas m(p) ≥ 0, y la red parte de un marcado inicial m0. Una transición t está **habilitada** en m cuando m(p) ≥ Pre(p, t) para todo lugar p. **Dispararla** da el marcado m′ = m − Pre(·, t) + Post(·, t): consume Pre(p, t) marcas de cada lugar de entrada y produce Post(p, t) en cada lugar de salida. Se dispara una sola transición a la vez, y un disparo es indivisible.

Un búfer de una casilla tiene dos lugares, `empty` con una marca y `full` sin ninguna, y dos transiciones: `produce` mueve la marca de `empty` a `full`, y `consume` la devuelve. En m0 solo `produce` está habilitada; dispararla da full = 1, donde solo `consume` está habilitada, y dispararla devuelve m0. Un lugar puede ser a la vez entrada y salida de una misma transición, un **bucle**: la transición necesita la marca para dispararse y la vuelve a poner.

De la regla se siguen dos hechos, y las secciones siguientes descansan en ellos. **Monotonía**: si una secuencia σ puede dispararse desde m, y m′ ≥ m lugar por lugar, entonces σ puede dispararse desde m′, porque las marcas adicionales nunca deshabilitan una transición. **Linealidad**: el cambio que produce σ es la suma de los cambios de sus transiciones, sea cual sea su orden, de modo que σ cambia m′ exactamente en el mismo vector que m.

### Ejercicio práctico

El lugar p contiene 2 marcas y tiene un arco de peso 3 hacia la transición t, que tiene un arco de salida hacia un lugar vacío q. ¿Está habilitada t? ¿Y si p contuviera 5 marcas?

> *Solución:* No: t necesita 3 marcas de p, y p tiene 2. Con 5 marcas t está habilitada, y dispararla deja 2 marcas en p y 1 en q. Después t vuelve a estar deshabilitada, así que se dispara exactamente una vez.

---

## 2. El grafo de alcanzabilidad

Un marcado es **alcanzable** cuando alguna secuencia de disparos lleva a él desde m0. El **grafo de alcanzabilidad** tiene como vértices los marcados alcanzables, y un arco de m a m′ etiquetado t siempre que disparar t en m da m′. Se construye en anchura: se parte de m0, se toman los marcados en el orden en que se encontraron, se dispara cada transición habilitada en cada uno, y se añade cada marcado nuevo al final de la cola. Un marcado está **muerto** cuando ninguna transición está habilitada en él, y una red está **libre de bloqueo** cuando ningún marcado alcanzable está muerto. La búsqueda en anchura encuentra cada marcado primero a lo largo de una secuencia de disparos más corta, así que seguir el padre de cada marcado hasta m0 da un **testigo** más corto: una secuencia que cualquiera puede reproducir con la regla de disparo.

En la cena de los filósofos de Dijkstra, n filósofos se sientan alrededor de una mesa, con un tenedor entre cada par de vecinos. El filósofo i piensa, toma el tenedor izquierdo i, luego el tenedor derecho i + 1 (mod n), come, y devuelve los dos tenedores. Como red hay lugares THINK_i, WAIT_i (con el tenedor izquierdo en la mano), EAT_i y FORK_i, con una marca en cada THINK_i y cada FORK_i, y transiciones TAKE_LEFT_i, TAKE_RIGHT_i y RELEASE_i. Para n = 3 el grafo de alcanzabilidad tiene 14 marcados y 27 arcos. Exactamente un marcado está muerto: cada filósofo tiene un tenedor izquierdo y espera un tenedor derecho que tiene un vecino. Su testigo es TAKE_LEFT_0, TAKE_LEFT_1, TAKE_LEFT_2. Si en cambio cada filósofo toma los dos tenedores en una sola transición, hay 4 marcados alcanzables, en los que nadie come o come exactamente uno de los tres, y ninguno está muerto.

### Ejercicio práctico

Dos carriles de trabajo comparten un árbol de trabajo y una pila de stash. El carril 0 toma el árbol y luego el stash; el carril 1 toma el stash y luego el árbol. Cada carril libera ambos al final de su trabajo y vuelve a estar listo. Encuentra un marcado muerto y un testigo más corto. ¿Cuántos marcados son alcanzables?

> *Solución:* El carril 0 toma el árbol y el carril 1 toma el stash. Cada carril tiene ahora su primer recurso y espera el que tiene el otro carril, y nada está habilitado. El testigo tiene dos disparos, una toma por carril. Los marcados alcanzables son: los dos carriles listos; el carril 0 con el árbol; el carril 0 con ambos; el carril 1 con el stash; el carril 1 con ambos; y el marcado muerto. Son seis.

---

## 3. Contar los marcados alcanzables

El espacio de estados de una red crece mucho más deprisa que la red. Cuando los filósofos toman los dos tenedores a la vez, un marcado alcanzable es un conjunto de filósofos que comen, ninguno de ellos vecino de otro, ya que los vecinos comparten un tenedor, y cada uno de esos conjuntos se alcanza dejando que sus miembros tomen sus tenedores uno tras otro. Contar esos conjuntos es un cálculo de **matriz de transferencia**. Se da la vuelta a la mesa anotando si cada filósofo come, con la regla de que a uno que come le sigue uno que no come. La matriz A = [[1, 1], [1, 0]] enumera los pasos permitidos, y el número de recorridos permitidos que se cierran tras n pasos es la traza de A^n. Esa traza vale φ^n + ψ^n, donde φ = (1 + √5)/2 y ψ = (1 − √5)/2 son los valores propios de A: son los números de Lucas.

Cuando los filósofos toman primero el tenedor izquierdo, cada uno piensa (T), espera con el tenedor izquierdo (W) o come (E). El tenedor i lo tiene el filósofo i en W o en E, y el filósofo i − 1 en E. Así que el único patrón prohibido es una E seguida de una W o de una E. En el orden T, W, E la matriz de transferencia es M = [[1, 1, 1], [1, 1, 1], [1, 0, 0]]. Su polinomio característico es λ(λ² − 2λ − 1), con valores propios 0 y 1 ± √2, de modo que el número de configuraciones permitidas es Q(n) = (1 + √2)^n + (1 − √2)^n, los números de Pell-Lucas, que cumplen Q(n) = 2Q(n − 1) + Q(n − 2). Toda configuración permitida es alcanzable: que los que comen tomen primero sus dos tenedores, y luego los que esperan tomen su tenedor izquierdo. El §6 muestra que ningún otro marcado lo es. La enumeración en anchura coincide:

| n | 2 | 3 | 4 | 5 | 6 | 12 | 13 |
|---|---|---|---|---|---|---|---|
| Tenedor izquierdo primero: marcados alcanzables | 6 | 14 | 34 | 82 | 198 | 39,202 | 94,642 |
| Ambos tenedores a la vez: marcados alcanzables | 3 | 4 | 7 | 11 | 18 | 322 | 521 |

Cada filósofo más multiplica la primera fila por aproximadamente 1 + √2, y la segunda por aproximadamente φ. Trece filósofos tienen ya 94,642 marcados alcanzables, más que los 50,000 que el analizador de IX explora por defecto (§7).

### Ejercicio práctico

Calcula Q(6) a partir de Q(4) = 34 y Q(5) = 82, y comprueba el resultado con (1 + √2)^6 + (1 − √2)^6.

> *Solución:* Q(6) = 2 × 82 + 34 = 198. Como (1 + √2)² = 3 + 2√2, el cubo da (1 + √2)^6 = (3 + 2√2)³ = 27 + 54√2 + 72 + 16√2 = 99 + 70√2. Del mismo modo (1 − √2)^6 = 99 − 70√2, y la suma es 198.

---

## 4. Acotación y testigo de bombeo

Un lugar está **k-acotado** cuando ningún marcado alcanzable pone en él más de k marcas, y una red está **acotada** cuando algún k sirve para todos los lugares. Una red 1-acotada se llama **segura**. Una red acotada tiene un número finito de marcados alcanzables, así que la búsqueda en anchura termina. Una red no acotada tiene infinitos, y ninguna enumeración de ellos termina.

Supongamos que m es alcanzable, que m′ es alcanzable desde m por una secuencia σ, y que m′ **cubre estrictamente** a m: m′ ≥ m lugar por lugar, y m′ ≠ m. Entonces la red no está acotada. Por monotonía, σ puede dispararse de nuevo desde m′, y por linealidad añade el mismo vector d = m′ − m, que es no negativo y no nulo. Repetir σ alcanza m + kd para todo k, así que algún lugar crece sin límite. El par (m, m′), con la secuencia que los une, es un **testigo de bombeo**.

El recíproco es lo que hace decidible la acotación. Si la red no está acotada, el árbol en anchura de los marcados alcanzables distintos es infinito, y cada marcado tiene un número finito de hijos, así que por el lema de Kőnig el árbol tiene una rama infinita m0, m1, m2, …. Por el **lema de Dickson**, toda sucesión infinita de vectores de números naturales tiene índices i < j con m_i ≤ m_j, y en una rama de marcados distintos m_i ≠ m_j: la rama contiene un testigo de bombeo. Karp y Miller convirtieron este argumento en el árbol de cobertura, que decide la acotación para toda red. Ninguno de los dos lemas acota la distancia entre i y j, así que una búsqueda que solo busca el par un número fijo de pasos atrás puede perderlo (§7).

### Ejercicio práctico

Una red tiene un lugar `queue` y una transición `grow`, sin arco de entrada y con un arco de salida hacia `queue`. Da un testigo de bombeo. Añade después un lugar `ticket` con una marca, con un arco de `ticket` a `grow` y un arco de `grow` de vuelta a `ticket`. ¿Sigue sin estar acotada la red?

> *Solución:* En m0 la cola está vacía, y disparar `grow` da queue = 1, que cubre estrictamente a m0: el testigo es m0, queue = 1, y la secuencia `grow`. Con el ticket, `grow` toma el ticket y lo devuelve, así que puede seguir disparándose para siempre. El testigo pasa a ser ticket = 1, luego ticket = 1 y queue = 1, de nuevo con `grow`. Un bucle no limita cuántas veces se dispara una transición.

---

## 5. Vivacidad, reversibilidad y componentes fuertemente conexas

Una transición está **muerta** cuando ningún marcado alcanzable la habilita, y una red sin transiciones muertas es **cuasi-viva** (nivel L1 en la clasificación de Murata). Una red es **viva** (nivel L4) cuando, desde todo marcado alcanzable, toda transición puede aún dispararse tras alguna secuencia. Una red es **reversible** cuando m0 puede alcanzarse de nuevo desde todo marcado alcanzable. Estas propiedades difieren. Toma un lugar `q` con una marca, una transición `loop` que toma la marca y la devuelve, y una transición `never` cuyo lugar de entrada está vacío. Esa red está libre de bloqueo, ya que `loop` está siempre habilitada, pero no es ni cuasi-viva ni viva.

En un grafo de alcanzabilidad finito, estas propiedades se leen en las **componentes fuertemente conexas**, los conjuntos maximales de marcados que pueden alcanzarse todos entre sí. Las componentes forman un grafo acíclico, y una componente es **terminal** cuando ningún arco sale de ella.

**Teorema.** Una red cuyo grafo de alcanzabilidad es finito es viva exactamente cuando cada transición etiqueta un arco dentro de cada componente terminal. *Demostración.* Desde todo marcado alcanzable se puede alcanzar alguna componente terminal: seguir arcos de componente en componente tiene que detenerse, ya que el grafo de componentes es finito y acíclico. Si t se dispara dentro de cada componente terminal, entonces desde cualquier marcado se alcanza una componente terminal, y dentro de ella cada marcado alcanza a cada otro, incluido uno donde t está habilitada. Así que t puede aún dispararse. Recíprocamente, supongamos que t no etiqueta ningún arco dentro de una componente terminal K. Entonces t no está habilitada en ningún marcado de K, porque dispararla añadiría un arco, y ningún arco sale de K. Desde un marcado de K la red nunca sale de K, así que t no vuelve a dispararse.

La red es reversible exactamente cuando todo el grafo es una sola componente, ya que todo marcado es alcanzable desde m0 por construcción. Un marcado muerto es por sí solo una componente terminal, sin arcos, así que una red con un bloqueo y al menos una transición no es viva. Para tres filósofos que toman primero el tenedor izquierdo, los 14 marcados forman dos componentes: el marcado muerto, que es terminal, y los otros 13, desde los que se alcanza. La vivacidad falla por tanto para las nueve transiciones, y la reversibilidad falla también, ya que m0 no se alcanza desde el marcado muerto.

### Ejercicio práctico

Muestra que una red viva con al menos una transición está libre de bloqueo, y da una red libre de bloqueo que no sea reversible.

> *Solución:* Sea m alcanzable y t una transición. La vivacidad dice que alguna secuencia desde m termina con t. Si m estuviera muerto, solo la secuencia vacía podría dispararse desde él, y no contiene t. Para la segunda parte, toma un lugar p con una marca, un lugar vacío q, una transición `go` de p a q, y una transición `stay` que toma la marca de q y la devuelve. `stay` sigue disparándose, así que ningún marcado está muerto, pero una vez disparada `go` la marca nunca vuelve a p: la red no es reversible, y tampoco es viva.

---

## 6. La matriz de incidencia y los invariantes

La enumeración visita los marcados de uno en uno; el álgebra lineal razona sobre todos a la vez. La **matriz de incidencia** C = Post − Pre tiene una fila por lugar y una columna por transición, y la columna t es el cambio que produce disparar t. Si σ lleva de m0 a m y el vector x cuenta cuántas veces aparece cada transición en σ, la linealidad da la **ecuación de estado** m = m0 + C x.

Un **P-invariante** es un vector no nulo y con yᵀ C = 0. Multiplicar la ecuación de estado por yᵀ da yᵀ m = yᵀ m0 para todo marcado alcanzable: una suma ponderada de marcas se conserva. Si y ≥ 0 e y(p) > 0, entonces y(p) m(p) ≤ yᵀ m = yᵀ m0, así que el lugar p nunca contiene más de yᵀ m0 / y(p) marcas. Una red cuyos lugares están todos cubiertos por P-invariantes no negativos está por tanto acotada, desde cualquier marcado inicial, sin enumerar nada.

Para los filósofos que toman primero el tenedor izquierdo, dos familias de P-invariantes valen para todo n:
- THINK_i + WAIT_i + EAT_i = 1: cada filósofo está en exactamente un estado;
- FORK_i + WAIT_i + EAT_i + EAT_(i−1) = 1: el tenedor i está en la mesa, lo tiene el filósofo i, o lo tiene el filósofo i − 1 como tenedor derecho.

Cada lugar aparece en al menos una de ellas con peso 1, así que la red es segura para todo n, incluido 13, donde la enumeración no puede terminar dentro del presupuesto por defecto. La segunda familia prueba también la exclusión mutua: EAT_i + EAT_(i−1) ≤ 1, así que dos vecinos nunca comen a la vez, y por eso el §3 no encontró marcados fuera de las configuraciones permitidas. Para n = 3, los 12 lugares y las 9 transiciones dan una matriz de rango 6, y estos seis invariantes generan todos los P-invariantes.

Un **T-invariante** es un vector no nulo x ≥ 0 con C x = 0: una secuencia cuyos recuentos son x vuelve al marcado del que partió, si es que puede dispararse. TAKE_LEFT_i, TAKE_RIGHT_i, RELEASE_i es uno.

La ecuación de estado es necesaria para la alcanzabilidad, no suficiente. Toma los lugares `gate` y `out`, ambos vacíos, y una transición t con arcos de `gate` a t, de t a `gate` y de t a `out`. La columna t de C es (0, 1), ya que el bucle se cancela. El marcado out = 1 satisface la ecuación de estado con x = (1), y sin embargo t nunca está habilitada, y m0 es el único marcado alcanzable. La matriz de incidencia no ve un bucle. Decidir la alcanzabilidad exactamente es posible (Mayr, 1981), pero ningún algoritmo puede hacerlo en tiempo primitivo recursivo: el problema es Ackermann-completo, con la cota superior de Leroux y Schmitz (2019) y la cota inferior de Czerwiński y Orlikowski, y de Leroux (2021).

### Ejercicio práctico

En la bomba de dos carriles del §2, encuentra un P-invariante que contenga el lugar de los árboles libres, y otro que contenga el stash. Comprueba que el marcado muerto satisface ambos. ¿Podrían estos invariantes por sí solos haber predicho el bloqueo?

> *Solución:* El árbol está libre, lo tiene el carril 0 mientras espera el stash o trabaja, o lo tiene el carril 1 mientras trabaja: árboles libres + carril 0 con su primer recurso + carril 0 con ambos + carril 1 con ambos = 1. Del mismo modo, stash + carril 0 con ambos + carril 1 con su primer recurso + carril 1 con ambos = 1. En el marcado muerto los dos carriles tienen su primer recurso, lo que da 0 + 1 + 0 + 0 = 1 y 0 + 0 + 1 + 0 = 1. Los invariantes dicen qué marcados son posibles, no cuáles son alcanzables o están muertos: el bloqueo lo muestra su testigo, y los invariantes no pueden descartarlo.

---

## 7. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus tests. Los números atribuidos al comportamiento de IX proceden de una transcripción a Python de `net.rs`, `analysis.rs` y `models.rs` en `crates/ix-petri`, y de la red construida en `tests/worktree_pump.rs`. La transcripción reproduce las aserciones de los tests de esos archivos, con dos excepciones: omite el test que compara dos serializaciones JSON, y para las redes mal formadas comprueba que se rechazan, no qué error se produce. Estos números son predicciones, y el §8 propone comprobarlos.

**La regla de disparo y su orden.** [`is_enabled`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L216) comprueba m(p) ≥ Pre(p, t) lugar por lugar, y [`fire`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L239) [consume las entradas antes de producir las salidas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L237), de modo que un bucle se comporta como dice el §1:

```rust
        let mut next = marking.0.clone();
        for &(p, w) in &tr.pre {
            next[p] -= w;
        }
        for &(p, w) in &tr.post {
            next[p] = next[p].checked_add(w).ok_or_else(|| PetriError::Overflow {
                transition: tr.id.clone(),
                place: self.places[p].id.clone(),
            })?;
        }
        Ok(Marking(next))
```

[`build`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L389) [ordena los lugares](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L402) y las transiciones por identificador y rechaza los identificadores duplicados, y [`enabled`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L229) devuelve las transiciones en ese orden. La numeración en anchura y cada testigo son por tanto los mismos en cada ejecución.

**La exploración, y lo que significa truncar.** [`explore`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L225) construye en anchura el grafo del §2. Un marcado nuevo más allá de [`max_states`, 50,000 por defecto](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L67), se [rechaza, y el grafo se marca como truncado](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L260); lo mismo ocurre con un disparo cuyo [número de marcas desbordaría](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L245) un entero de 64 bits. Un grafo truncado contiene marcados algunos de cuyos sucesores se rechazaron y nunca se registraron, e IX no los confunde con marcados muertos: pregunta [a la red, no al grafo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L464), si un marcado habilita algo.

**Qué veredictos sobreviven al truncamiento.** [`analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L436) devuelve `Holds`, `Fails` o `Unknown` para cada propiedad, con los argumentos de los §2 a §5. La tabla muestra qué veredictos da tras una ejecución truncada:

| Propiedad | IX decide tras una ejecución truncada | IX decide solo tras una ejecución completa |
|---|---|---|
| Ausencia de bloqueo | `Fails`, con el número de marcados muertos encontrados y, [por defecto, hasta 8](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L68) de ellos con sus testigos más cortos | `Holds` |
| Acotación | `Fails`, con un testigo de bombeo | `Holds`, con la cota de cada lugar |
| Cuasi-vivacidad | `Holds`, en cuanto cada transición se ha disparado | `Fails`, con las transiciones que nunca se dispararon |
| Vivacidad (L4) y reversibilidad | Nada | `Holds` o `Fails`, a partir de las componentes del §5 |

Es la asimetría de MAT-002. Una afirmación existencial se zanja con un ejemplo, encontrado en cualquier momento de la búsqueda: algún marcado alcanzable está muerto, alguna secuencia bombea, cada transición se dispara en algún sitio. Una afirmación universal solo se zanja con el grafo entero. Los veredictos de [bloqueo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L483), de [acotación](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L494), de [cuasi-vivacidad](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L527), y de [vivacidad y reversibilidad](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L538) siguen la tabla línea por línea. La última fila es una elección de IX, no una necesidad lógica, como explica *Otras carencias* más abajo. Una red no acotada nunca se explora por completo, así que solo la columna del medio puede aplicársele.

**La vivacidad y la reversibilidad, tal como las prueba el §5.** [`liveness_and_reversibility`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L604) marca una componente como terminal cuando ningún arco sale de ella, y hace fallar la vivacidad para cada transición que no etiqueta ningún arco dentro de alguna componente terminal. La reversibilidad se cumple cuando hay [una sola componente](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L640). Las componentes vienen de un [Tarjan iterativo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L367), así que un grafo profundo no puede desbordar la pila.

**El testigo de bombeo se busca en un solo camino, a lo sumo 512 pasos atrás.** Cuando se descubre un marcado, [`strictly_covered_ancestor`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L300) recorre hacia atrás sus padres en anchura, [a lo sumo 512 de ellos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L51), buscando uno al que cubra estrictamente:

```rust
    fn strictly_covered_ancestor(&self, state: usize) -> Option<usize> {
        let wide_total = |m: &Marking| -> u128 { m.tokens().iter().map(|&t| u128::from(t)).sum() };
        let total = wide_total(&self.markings[state]);
        let mut cursor = self.parent[state].map(|(p, _)| p);
        let mut walked = 0usize;
        while let Some(a) = cursor {
            if walked >= MAX_COVERING_WALK {
                return None;
            }
            walked += 1;
            if wide_total(&self.markings[a]) < total
                && self.markings[state].strictly_covers(&self.markings[a])
            {
                return Some(a);
            }
            cursor = self.parent[a].map(|(p, _)| p);
        }
        None
    }
```

Un par que señala es una prueba, por el §4. Un par que se le escapa deja la acotación en `Unknown`, como dice el comentario: acortar el recorrido [«can only *miss* a witness»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L292). Que se le escape no depende del presupuesto. Toma un anillo de L lugares alrededor del cual circula una marca, y deja que una transición del anillo añada también una marca a un lugar contador. El par más cercano en el que un marcado cubre estrictamente al otro, en cualquier camino, está entonces a L disparos de distancia. Con L = 512 la transcripción encuentra el testigo en el marcado 513; con L = 513 no encuentra ninguno con ningún presupuesto, y la red, aunque no está acotada, se declara `Unknown`.

**Respuestas conocidas.** [`dining_philosophers`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L32) construye los dos protocolos del §2. Un test comprueba, [para n = 2 a 5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L110), que tomar primero el tenedor izquierdo lleva a un bloqueo y tomar los dos a la vez no; otro fija [el marcado muerto para n = 3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L153). La bomba del §2 es [`opposite_acquisition_orders_wedge_the_pump`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L92). Otros tests del mismo archivo muestran que un [orden de adquisición canónico](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L138) elimina el bloqueo para 2 a 4 carriles, y que [un carril fuera de orden](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L162) lo trae de vuelta. El plan del crate registra una ejecución sobre el archivo de seis filósofos que publica pnml.org: [729 marcados y 3,402 arcos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/plans/2026-09-08-feat-ix-petri-place-transition-nets.md#L111), con dos marcados muertos. Leído con el analizador XML estándar de Python y pasado a la transcripción, el mismo archivo da los mismos números.

**Dónde se detiene el presupuesto por defecto.** Trece filósofos que toman primero el tenedor izquierdo tienen 94,642 marcados alcanzables (§3). El marcado muerto está a 13 disparos de m0, y el orden en anchura descubre 94,121 marcados antes que él. Con el presupuesto por defecto de 50,000 el análisis se detiene entre los marcados situados a nueve disparos de m0, y declara la ausencia de bloqueo como `Unknown`. Sin embargo el bloqueo está en el modelo, y su testigo, de TAKE_LEFT_00 a TAKE_LEFT_12, es fácil de escribir y de reproducir. La cuasi-vivacidad se cumple, ya que cada transición se dispara dentro del presupuesto; la acotación es `Unknown`, aunque los P-invariantes del §6 prueban en una línea que la red es segura. La guía de IX incluye [los P- y T-invariantes, los sifones y las trampas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/guides/petri-nets-in-ix.md#L201) entre lo no implementado, y dice que vale la pena añadirlos [«the day a net in this repository is too big for `max_states`»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/guides/petri-nets-in-ix.md#L203).

**Otras carencias.** El crate promete cada propiedad [«with a witness»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/lib.rs#L6), y los bloqueos y la no acotación tienen uno. Un `Holds` de cuasi-vivacidad [no lleva ninguno](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L528), ni siquiera un disparo de cada transición. Un veredicto de vivacidad fallido nombra transiciones, pero ningún marcado desde el que ya no puedan dispararse nunca. El veredicto de reversibilidad es un [`Verdict<()>`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L201), así que su fallo no lleva ningún marcado desde el que m0 sea inalcanzable. Para los filósofos que toman primero el tenedor izquierdo, el fallo de vivacidad enumera todas las transiciones, porque la componente terminal es el marcado muerto; el veredicto de bloqueo es el informativo. La vivacidad y la reversibilidad solo se calculan a partir de un grafo completo, así que una ejecución truncada que encuentra un marcado muerto declara ambas `Unknown`. Sin embargo, por el §5, ese marcado ya prueba que ambas fallan: nada se dispara desde él, y m0, desde el que una ejecución truncada ha disparado algo, no es alcanzable desde él. No hay árbol de cobertura, así que una red no acotada cuyo testigo se le escapa al recorrido sigue en `Unknown`. El mismo análisis se expone a SQL como [`ix_petri_analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/petri.rs#L10) y a los agentes como la herramienta MCP `ix_petri_analyze`, registrada como la habilidad [`petri.analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/petri.rs#L137). Ambos rechazan un presupuesto cuya memoria en el peor caso supere [512 MiB](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/json.rs#L123).

Corregir cualquier parte de esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Una ejecución sobre los trece filósofos con un presupuesto de 94,122 marcados queda truncada. ¿Qué veredictos puede decidir?

> *Solución:* El marcado muerto es el marcado 94,122 en ser descubierto, así que cabe en el presupuesto: la ausencia de bloqueo falla, con el testigo de los trece disparos TAKE_LEFT. La cuasi-vivacidad se cumple, ya que cada transición se dispara dentro del presupuesto. La acotación sigue en `Unknown`: probarla por enumeración exige el grafo entero, y le faltan 520 marcados. IX deja también la vivacidad y la reversibilidad en `Unknown`, aunque el marcado muerto ya prueba que ambas fallan (§5).

---

## 8. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Contar.** Ejecutar `analyze` con los límites por defecto sobre los dos protocolos para n = 2 a 12. Predicción: los recuentos del §3, ejecuciones completas, un marcado muerto cuando se toma primero el tenedor izquierdo y ninguno en otro caso.
2. **El borde del presupuesto.** Ejecutar los trece filósofos que toman primero el tenedor izquierdo con `max_states` fijado en 50,000, 94,121, 94,122 y 94,642. Predicción: ausencia de bloqueo `Unknown` para los dos primeros presupuestos; `Fails` con 94,122, truncada, con el marcado muerto en el estado 94,121; con 94,642 una ejecución completa, segura, ni viva ni reversible.
3. **El límite del recorrido.** Construir el anillo del §7 con L = 512 y L = 513, y ejecutarlo con `max_states` fijado en 5,000. Predicción: con L = 512, acotación `Fails` con un testigo de bombeo del estado 0 al estado 512 en 512 disparos; con L = 513, acotación `Unknown` y ningún testigo.
4. **Invariantes.** Construir la matriz de incidencia a partir de los campos `pre` y `post` de `transitions()` para n = 3 y n = 5, y comprobar los 2n invariantes del §6. Predicción: yᵀ C = 0 para cada uno de ellos, y C tiene rango 2n.
5. **Un archivo que IX no escribió.** Leer el archivo de seis filósofos de pnml.org con `read_pnml` y analizarlo. Predicción: 30 lugares, 30 transiciones, 729 marcados, 3,402 arcos, dos marcados muertos, segura, ni viva ni reversible.
6. **Dos redes de GA.** Leer los dos ejemplos PNML del componente IxqlViewer de GA, [`petri-producer-consumer.pnml`](https://github.com/GuitarAlchemist/ga/blob/b030c3f05e92189f9cb569d0fe0457ba6269e564/ReactComponents/ga-react-components/src/components/IxqlViewer/examples/petri-producer-consumer.pnml) y [`petri-pipeline-lifecycle.pnml`](https://github.com/GuitarAlchemist/ga/blob/b030c3f05e92189f9cb569d0fe0457ba6269e564/ReactComponents/ga-react-components/src/components/IxqlViewer/examples/petri-pipeline-lifecycle.pnml), y analizarlos. Predicción: la red productor-consumidor, con 6 lugares y 4 transiciones, tiene 12 marcados y 20 arcos, y es 2-acotada, libre de bloqueo, viva y reversible. La red del ciclo de vida del pipeline, con 12 lugares y 8 transiciones, tiene 8 marcados y 8 arcos; es segura y cuasi-viva, pero ni viva ni reversible, y la ausencia de bloqueo da `Fails` con tres marcados muertos, éxito, fallo y cancelación, alcanzados en cuatro disparos, dos disparos y un disparo.

### Ejercicio práctico

En el paso 2, un solo marcado de presupuesto separa `Unknown` de `Fails`. ¿Por qué no es una señal de inestabilidad?

> *Solución:* El orden de descubrimiento es fijo (§7), así que el marcado muerto es siempre el 94,122 en ser descubierto, y un presupuesto de 94,121 se detiene un marcado antes. `Unknown` es ahí una negativa a responder, no una conjetura, y no contradice ninguno de los dos veredictos. Un presupuesto mayor explora primero los mismos marcados y luego más, así que puede convertir `Unknown` en un veredicto, pero nunca invertir uno.

---

## 9. Errores comunes

- **Leer `Unknown` como `Holds`.** Una búsqueda detenida pronto no ha encontrado ningún bloqueo entre los marcados que vio, lo que no dice nada de los demás.
- **Tomar un recuento de estados truncado por el tamaño del espacio de estados.** Una ejecución detenida en 50,000 marcados ha visto 50,000 marcados, y el espacio completo puede ser mucho mayor.
- **Esperar que un recorrido de ancestros encuentre todo testigo de bombeo.** Un par más lejano de lo que alcanza el recorrido se pierde con cualquier presupuesto; solo un método completo, como el árbol de cobertura de Karp y Miller, decide la acotación.
- **Leer todo marcado muerto como un error.** Los estados finales de un flujo de trabajo son marcados muertos por diseño, como en el ciclo de vida del pipeline de GA (§8); un veredicto de bloqueo solo señala un defecto donde el modelo dice que el trabajo debe continuar.
- **Usar la ecuación de estado como prueba de alcanzabilidad.** Es necesaria, no suficiente, y no ve los bucles.
- **Leer «no viva» como «tiene un bloqueo».** Una red puede estar libre de bloqueo y tener aun así una transición que no vuelve a dispararse.
- **Leer un P-invariante como prueba de alcanzabilidad.** Un invariante descarta marcados; solo un testigo muestra que un marcado se alcanza.
- **Olvidar lo deprisa que crece el espacio.** Cada filósofo que toma primero el tenedor izquierdo multiplica los marcados alcanzables por unos 2.4, así que un modelo pequeño sobre el papel puede superar cualquier presupuesto.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Red de lugares y transiciones** | Lugares, transiciones, y arcos ponderados entre un lugar y una transición en cualquier sentido |
| **Marcado** | Un número de marcas para cada lugar; el estado de la red |
| **Regla de disparo** | Una transición está habilitada cuando cada lugar de entrada contiene al menos el peso del arco; dispararla consume y produce marcas en consecuencia |
| **Grafo de alcanzabilidad** | Los marcados alcanzables, con un arco por cada disparo |
| **Marcado muerto** | Un marcado en el que ninguna transición está habilitada |
| **Testigo** | Una secuencia de disparos desde m0 que cualquiera puede reproducir para comprobar una afirmación |
| **k-acotada, segura** | Ningún marcado alcanzable pone más de k marcas en un lugar; segura significa 1-acotada |
| **Testigo de bombeo** | Un marcado alcanzable m y un marcado m′ alcanzable desde m que lo cubre estrictamente, que prueban la no acotación |
| **Cuasi-viva (L1)** | Cada transición se dispara en algún marcado alcanzable |
| **Viva (L4)** | Desde todo marcado alcanzable, toda transición puede aún dispararse |
| **Reversible** | m0 puede alcanzarse de nuevo desde todo marcado alcanzable |
| **Componente terminal** | Una componente fuertemente conexa del grafo de alcanzabilidad de la que no sale ningún arco |
| **Matriz de incidencia** | C = Post − Pre; la columna t es el cambio que produce disparar t |
| **Ecuación de estado** | m = m0 + C x, una condición necesaria para alcanzar m |
| **P-invariante** | Un vector no nulo y con yᵀ C = 0; la suma ponderada de marcas yᵀ m se conserva |
| **T-invariante** | Un vector no nulo x ≥ 0 con C x = 0; una secuencia con esos recuentos vuelve a su marcado de partida |
| **Matriz de transferencia** | Una matriz de pasos permitidos, cuyas potencias cuentan las sucesiones permitidas |

---

## Autoevaluación

**1. Un analizador se detiene en 50,000 marcados, no encuentra ninguno muerto, y declara la ausencia de bloqueo como `Unknown`, pero cada transición se ha disparado. ¿Qué puedes concluir?**
> Que la red es cuasi-viva: cada transición se dispara en algún marcado alcanzable, y cada disparo es un testigo. Nada se sigue sobre la ausencia de bloqueo, ya que un marcado muerto puede estar entre los marcados no explorados; con trece filósofos, lo está.

**2. ¿Por qué un marcado alcanzable m, con un marcado m′ alcanzable desde m que lo cubre estrictamente, prueba la no acotación, mientras que no encontrar tal par no prueba nada?**
> La secuencia de m a m′ puede dispararse de nuevo desde m′, por monotonía, y añade cada vez el mismo vector no nulo, por linealidad. No encontrar un par no prueba nada, porque la búsqueda pudo detenerse antes de que el par apareciera, o, como en IX, mirar solo un número fijo de pasos atrás a lo largo de un único camino.

**3. ¿Cómo puede la cena de los filósofos ser segura para todo n cuando el analizador no puede terminar para n = 13?**
> Los P-invariantes THINK_i + WAIT_i + EAT_i = 1 y FORK_i + WAIT_i + EAT_i + EAT_(i−1) = 1 valen para todo n, y cubren cada lugar con peso 1. Acotan cada lugar por 1 sin enumerar un solo marcado.

**4. IX informa de que la vivacidad falla para las nueve transiciones de tres filósofos. ¿Qué añade esto al veredicto de bloqueo?**
> Nada. La única componente terminal es el marcado muerto, donde no se dispara ninguna transición, así que todas las transiciones faltan en ella. El veredicto de bloqueo dice más, ya que da el marcado y el testigo TAKE_LEFT_0, TAKE_LEFT_1, TAKE_LEFT_2.

**Criterio de aprobación:** Disparar a mano una red de lugares y transiciones; construir su grafo de alcanzabilidad y dar un testigo más corto de un bloqueo; contar marcados alcanzables con una matriz de transferencia; probar la no acotación con un testigo de bombeo y explicar lo que su ausencia no muestra; leer la vivacidad y la reversibilidad en las componentes terminales; probar la acotación y la exclusión mutua con P-invariantes y explicar por qué la ecuación de estado no basta; y decir qué veredictos de IX puede decidir una ejecución truncada.

---

## Base de investigación

- C. A. Petri, *Kommunikation mit Automaten*, tesis doctoral, 1962: el origen de las redes de Petri
- T. Murata, «Petri nets: Properties, analysis and applications», *Proceedings of the IEEE* 77, 1989: la regla de disparo, los niveles de vivacidad L0 a L4, la matriz de incidencia y los invariantes
- R. M. Karp y R. E. Miller, «Parallel program schemata», *Journal of Computer and System Sciences* 3, 1969: el árbol de cobertura y la decidibilidad de la acotación
- L. E. Dickson, «Finiteness of the odd perfect and primitive abundant numbers with n distinct prime factors», *American Journal of Mathematics* 35, 1913: el lema sobre vectores de números naturales
- D. Kőnig, «Über eine Schlussweise aus dem Endlichen ins Unendliche», *Acta Scientiarum Mathematicarum* 3, 1927: un árbol infinito con ramificación finita tiene una rama infinita
- E. W. Mayr, «An algorithm for the general Petri net reachability problem», *Proceedings of the 13th ACM Symposium on Theory of Computing*, 1981: la alcanzabilidad es decidible
- W. Czerwiński y Ł. Orlikowski, «Reachability in vector addition systems is Ackermann-complete», y J. Leroux, «The reachability problem for Petri nets is not primitive recursive», ambos en *Proceedings of the 62nd IEEE Symposium on Foundations of Computer Science*, 2021: la cota inferior
- J. Leroux y S. Schmitz, «Reachability in vector addition systems is primitive-recursive in fixed dimension», *Proceedings of the 34th Annual ACM/IEEE Symposium on Logic in Computer Science*, 2019: la cota superior de Ackermann
- R. E. Tarjan, «Depth-first search and linear graph algorithms», *SIAM Journal on Computing* 1, 1972: las componentes fuertemente conexas
- E. W. Dijkstra, «Hierarchical ordering of sequential processes», *Acta Informatica* 1, 1971: la cena de los filósofos
- E. G. Coffman, M. J. Elphick y A. Shoshani, «System deadlocks», *ACM Computing Surveys* 3, 1971: las condiciones del bloqueo, entre ellas la espera circular
- ISO/IEC 15909-2:2011, *High-level Petri nets — Part 2: Transfer format*: PNML, el formato de intercambio que lee IX
- OEIS A000032 (números de Lucas) y A002203 (números de Pell-Lucas): los recuentos del §3
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §7 enlaza a su línea
- Código fuente de GA en el commit `b030c3f05e92189f9cb569d0fe0457ba6269e564`: los dos ejemplos PNML del §8
- Experimento: propuesto en el §8, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
