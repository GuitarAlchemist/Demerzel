---
module_id: mat-022-symmetry-groups-invariants
department: mathematics
course: Simetría, grupos e invariantes
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-002-counterexamples-and-exhaustive-checks]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Simetría, grupos e invariantes — Contar las clases de conjuntos, y lo que olvida un invariante

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Describir la transposición y la inversión de clases de altura como el grupo diédrico D12 actuando sobre los 4096 subconjuntos de Z/12, y comprobar las leyes de grupo y de acción
- Calcular órbitas y estabilizadores, y predecir el tamaño de una clase de conjuntos con el teorema de la órbita y el estabilizador
- Contar órbitas con el lema de Burnside: 352 clases de transposición, 224 clases de conjuntos, y los recuentos para cada cardinal
- Distinguir un invariante completo de uno incompleto, y leer la relación Z como el fallo del vector de clases de intervalos al separar órbitas
- Tratar las operaciones neorriemannianas P, L y R como involuciones sobre las 24 tríadas consonantes, y explicar por qué conmutan con la transposición y la inversión
- Seguir lo que calcula la crate `ix-bracelet` de IX: qué representante llama forma prima, y qué conjuntos puede alcanzar su búsqueda de caminos armónicos

---

## 1. Grupos y acciones

Numera las clases de altura Do = 0, Do♯ = 1, …, Si = 11, de modo que formen Z/12, los enteros módulo 12. La transposición por n es T_n: x ↦ x + n, y la inversión seguida de una transposición es T_nI: x ↦ n − x. Estas 24 aplicaciones forman un **grupo**: componer dos de ellas da una tercera, T_0 es la identidad, y cada una tiene inversa, puesto que T_n deshace T_(−n) y cada T_nI se deshace a sí misma, porque n − (n − x) = x. En la esfera del reloj, T_n es una rotación y T_nI una reflexión, y el grupo es el **grupo diédrico** D12 del dodecágono regular. Lee las composiciones de derecha a izquierda, como con las funciones: T_mI T_n envía x a m − (x + n), así que es T_(m−n)I. El grupo no es conmutativo: T_1 T_0I envía x a 1 − x, mientras que T_0I T_1 lo envía a −(x + 1) = 11 − x.

Un grupo **actúa** sobre un conjunto cuando cada elemento g mueve los puntos del conjunto, de modo que la identidad no mueve nada y (gh)·x = g·(h·x). D12 actúa sobre los conjuntos de clases de altura punto por punto: T_n{0, 4, 7} = {n, n + 4, n + 7}. Permuta los 2^12 = 4096 subconjuntos de Z/12 y nunca cambia su cardinal.

### Ejercicio práctico

Calcula T_3I de la tríada de Do mayor {0, 4, 7}, y vuelve a aplicar T_3I.

> *Solución:* 3 − 0 = 3, 3 − 4 = 11 y 3 − 7 = 8, así que T_3I{0, 4, 7} = {3, 8, 11}, la tríada de Sol♯ menor. Volver a aplicar T_3I da 3 − 3 = 0, 3 − 8 = 7 y 3 − 11 = 4, la tríada de Do mayor: T_3I es su propia inversa.

---

## 2. Órbitas y estabilizadores

La **órbita** de un conjunto X es la colección de sus imágenes g·X, y su **estabilizador** es el conjunto de los elementos g con g·X = X. Las órbitas forman una partición de los 4096 subconjuntos. Bajo D12 son las **clases de conjuntos**; bajo el subgrupo C12 de las doce transposiciones son las clases de transposición. El **teorema de la órbita y el estabilizador** dice que |órbita| · |estabilizador| = |G|, aquí 24. La demostración: g·X = h·X exactamente cuando h⁻¹g pertenece al estabilizador, así que los elementos que envían X a una imagen dada forman una clase lateral del estabilizador, y todas las clases laterales tienen su tamaño.

Ninguna transposición fija la tríada de Do mayor, y cada inversión la convierte en una tríada menor, así que su estabilizador es {T_0} y su órbita tiene 24 miembros, las 12 tríadas mayores y las 12 menores. La tríada aumentada {0, 4, 8} queda fija por T_0, T_4 y T_8 y por T_0I, T_4I y T_8I: un estabilizador de 6 y una órbita de 4, las cuatro tríadas aumentadas. La séptima disminuida {0, 3, 6, 9} tiene un estabilizador de 8, los T_n y T_nI con n = 0, 3, 6 o 9, y una órbita de 3. Como un estabilizador es un subgrupo, su orden divide a 24, y también lo divide el tamaño de toda clase de conjuntos.

### Ejercicio práctico

Halla el estabilizador y la órbita de la escala de tonos enteros {0, 2, 4, 6, 8, 10}.

> *Solución:* T_n envía las clases de altura pares a sí mismas para todo n par, y T_nI también, puesto que n menos un número par es par; para n impar, ambas las envían a las impares. El estabilizador tiene 12 elementos, y la órbita 24/12 = 2: las dos escalas de tonos enteros.

---

## 3. Contar órbitas con el lema de Burnside

Dividir 4096 entre 24 no cuenta las clases de conjuntos; ni siquiera es un entero, porque los conjuntos simétricos tienen órbitas más pequeñas. El **lema de Burnside** las cuenta exactamente: el número de órbitas es el número medio de puntos fijos, (1/|G|) Σ_g |Fix(g)|. Cuenta de dos maneras los pares (g, X) con g·X = X. Por g, suman Σ_g |Fix(g)|; por X, suman Σ_X |Stab(X)| = Σ_X 24/|Orb(X)|, y los miembros de cada órbita aportan juntos exactamente 24.

**Rotaciones.** T_n divide Z/12 en mcd(n, 12) ciclos, y un conjunto queda fijo cuando es una unión de ciclos, así que T_n fija 2^mcd(n, 12) conjuntos. Para n = 0, …, 11 esto da 4096 + 2 + 4 + 8 + 16 + 2 + 64 + 2 + 16 + 8 + 4 + 2 = 4224, y 4224/12 = 352 clases de transposición.

**Reflexiones.** T_nI fija las clases de altura x con 2x = n. Para n par hay dos, n/2 y n/2 + 6, y las otras diez forman cinco pares intercambiados, así que quedan fijos 2^7 = 128 conjuntos; para n impar no hay ninguna, hay seis pares y 2^6 = 64 conjuntos fijos. Las seis reflexiones pares y las seis impares fijan 6 × 128 + 6 × 64 = 1152 conjuntos, y (4224 + 1152)/24 = 5376/24 = 224 clases de conjuntos.

**Un cardinal cada vez.** Para los tricordios, solo T_4 y T_8 fijan algo además de la identidad, cada una las cuatro tríadas aumentadas: (220 + 4 + 4)/12 = 228/12 = 19 clases de transposición. Una reflexión par fija un tricordio formado por una clase de altura fija y un par intercambiado, 2 × 5 = 10 tricordios, y una reflexión impar no fija ninguno: (228 + 60)/24 = 288/24 = 12 clases de conjuntos. Cinco de las doce son simétricas, 3-1, 3-6, 3-9, 3-10 y 3-12, y las otras siete se dividen cada una en dos clases de transposición, lo que da de nuevo 12 + 7 = 19.

| Cardinal | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Clases de transposición (C12) | 1 | 1 | 6 | 19 | 43 | 66 | 80 | 66 | 43 | 19 | 6 | 1 | 1 | 352 |
| Clases de conjuntos (D12) | 1 | 1 | 6 | 12 | 29 | 38 | 50 | 38 | 29 | 12 | 6 | 1 | 1 | 224 |

### Ejercicio práctico

Cuenta las clases de tetracordios con el lema de Burnside, primero bajo la transposición sola y después bajo D12.

> *Solución:* La identidad fija los C(12, 4) = 495 tetracordios. T_3 y T_9 tienen tres ciclos de longitud 4 y fijan 3 cada una; T_6 tiene seis ciclos de longitud 2 y fija C(6, 2) = 15; las demás rotaciones no fijan ninguno. Así que (495 + 3 + 3 + 15)/12 = 516/12 = 43. Una reflexión par fija los dos puntos fijos con un par, o dos de sus cinco pares: 5 + 10 = 15; una reflexión impar fija dos de sus seis pares, otra vez 15. Así que (516 + 12 × 15)/24 = 696/24 = 29.

---

## 4. Invariantes y formas normales

Un **invariante** es una función que toma el mismo valor en todos los miembros de una órbita. El cardinal es uno. El vector de clases de intervalos es otro: T_n conserva cada diferencia entre dos clases de altura, T_nI le cambia el signo, y la clase de intervalo min(d, 12 − d) ignora el signo. Un invariante es **completo** cuando además separa las órbitas, de modo que valores iguales implican la misma órbita. El vector de clases de intervalos no es completo: {0, 1, 4, 6} y {0, 1, 3, 7} tienen ambos un intervalo de cada clase, el vector ⟨111111⟩, y sin embargo están en órbitas distintas, 4-Z15 y 4-Z29. Esta es la **relación Z**. Una comprobación exhaustiva de las 224 clases, al modo de MAT-002, encuentra 23 pares así, 46 clases en total: 1 par de tetracordios, 3 de pentacordios, 15 de hexacordios, 3 de heptacordios y 1 de octacordios.

Una **forma normal** es un invariante completo de un tipo particular: una regla que elige un miembro de cada órbita, el mismo sea cual sea el miembro del que parta. La forma prima de una clase de conjuntos es una regla así, y las dos reglas publicadas deshacen los empates de forma distinta: las de Forte y de Rahn dan formas primas distintas para 6 de las 224 clases, 5-20, 6-Z29, 6-31, 7-Z18, 7-20 y 8-26. Cualquier regla que devuelva el menor miembro de la órbita en un orden total fijo es también una forma normal, pero no tiene por qué imprimir lo que imprime una tabla publicada. Los módulos de la transformada discreta de Fourier de un conjunto de clases de altura son otros invariantes, y tampoco separan las clases en relación Z: los dos miembros de cada uno de los 23 pares los comparten.

### Ejercicio práctico

Muestra que {0, 1, 4, 6} y {0, 1, 3, 7} tienen el mismo vector de clases de intervalos, y encuentra un invariante que los separe.

> *Solución:* Las seis diferencias en {0, 1, 4, 6} son 1, 4, 6, 3, 5 y 2, y en {0, 1, 3, 7} son 1, 3, 7, 2, 6 y 4, donde 7 es la clase de intervalo 5: una de cada clase en ambos. Recorriendo el círculo, los pasos entre notas sucesivas son 1, 3, 2, 6 para el primer conjunto y 1, 2, 4, 5 para el segundo. T_n conserva este ciclo de pasos y T_nI lo invierte, así que el multiconjunto de pasos es un invariante, y {1, 2, 3, 6} ≠ {1, 2, 4, 5}.

---

## 5. Transformaciones neorriemannianas

Tres operaciones actúan sobre las 24 tríadas mayores y menores. **P** (paralela) conserva la fundamental y la quinta y mueve la tercera un semitono: Do mayor ↔ Do menor. **L** (intercambio de sensible, *leading-tone exchange*) conserva la tercera y la quinta de una tríada mayor y baja su fundamental un semitono: Do mayor {0, 4, 7} ↔ Mi menor {4, 7, 11}. **R** (relativa) conserva la fundamental y la tercera de una tríada mayor y sube su quinta un tono: Do mayor ↔ La menor {9, 0, 4}. Cada una conserva dos notas de la tríada y refleja la tercera nota respecto de ellas, así que cada una es una inversión elegida por la propia tríada, y cada una es una **involución**: aplicada dos veces, devuelve la tríada de partida.

Como cada una se define por los intervalos propios de la tríada, y T_n y T_nI transportan los intervalos, P, L y R conmutan con toda transposición e inversión: transponer y luego aplicar P da la misma tríada que aplicar P y luego transponer. Las tres generan un grupo de orden 24 que actúa sobre las mismas 24 tríadas, el dual del grupo T/I en el sentido de Lewin. Alternar P y L desde Do mayor visita seis tríadas, Do mayor, Do menor, La♭ mayor, La♭ menor, Mi mayor y Mi menor: es el ciclo hexatónico, cuyas notas {0, 3, 4, 7, 8, 11} forman la colección hexatónica. Alternar P y R visita ocho, el ciclo octatónico que pasa por Do, Mi♭, Fa♯ y La. Alternar R y L visita las 24.

### Ejercicio práctico

Partiendo de Do mayor, aplica L, luego P, luego R. ¿Dónde llegas, y qué comparten las dos tríadas?

> *Solución:* L da Mi menor {4, 7, 11}; P da Mi mayor {4, 8, 11}; R conserva Mi y Sol♯ y sube Si un tono hasta Do♯, lo que da Do♯ menor {1, 4, 8}. Do mayor y Do♯ menor comparten su tercera, Mi: es el deslizamiento S (*slide*). Aplicar R, luego P, luego L también da Do♯ menor, puesto que S es una involución.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea a Python de `dihedral.rs`, `action.rs`, `orbit.rs`, `prime_form.rs`, `forte.rs`, `neo_riemannian.rs` y `grothendieck.rs` en `crates/ix-bracelet`, y del manejador `ix_grothendieck_path`. Estos números son predicciones, y el §7 propone comprobarlos.

**El grupo y la acción.** La crate presenta [D12 mediante generadores y relaciones](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L1), compone los elementos según la [regla para r^i s^j](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L67), y [refleja antes de girar](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L41), de modo que un elemento con reflexión envía x a n − x, el T_nI del §1. La ley de acción está, en palabras del trait, [«verified in tests, not by this trait»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L10); la transcripción la comprueba para los 576 pares de elementos, sobre cuatro conjuntos. [`orbit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L13) enumera las 24 imágenes de un conjunto, y sus pruebas fijan la órbita de la [tríada aumentada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L118) en 4 y la de la [séptima disminuida](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L125) en 3, como deduce el §2. `all_prime_forms` encuentra sus 224 clases reduciendo [cada máscara](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L43) a su representante, y su comentario nombra el [total de Burnside/Pólya](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L36) que calcula el §3.

**Lo que IX llama forma prima no es ni la de Forte ni la de Rahn.** La función detrás de cada representante es:

```rust
/// Minimum (under [`lex_less`]) over all 24 dihedral images of `x`.
pub fn bracelet_prime_form(x: PcSet) -> PcSet {
    let mut best = x;
    for reflected in [false, true] {
        for rotation in 0u8..12 {
            let g = DihedralElement {
                rotation,
                reflected,
            };
            let cand = g.apply(x);
            if lex_less(cand.raw(), best.raw()) {
                best = cand;
            }
        }
    }
    best
}
```

- **El orden es lexicográfico sobre listas ordenadas.** `lex_less` implementa el [orden lexicográfico sobre las listas ordenadas de clases de altura](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/prime_form.rs#L12), así que el representante es el miembro de la órbita cuya lista ordenada es la menor, no la forma normal más compacta del §4. El comentario del módulo dice que esto coincide con la [convención de Forte para las clases de conjuntos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/prime_form.rs#L5). Lo hace para las clases, no para su escritura: el representante es la forma prima de Forte para 189 clases y la de Rahn para 183. Para 4-10 devuelve [0, 1, 3, 10], donde ambas reglas publicadas dan (0235).
- **Los números de Forte son correctos.** [`forte_number`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L360) busca [este representante](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L363) en una tabla de 224 máscaras, y cada máscara lleva el número que la lista publicada da a su órbita. La cabecera de la tabla dice que las máscaras [coinciden exactamente con las órbitas canónicas de Forte](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L19), lo que es cierto de las órbitas. La prueba de invariancia comprueba [ocho conjuntos de muestra](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L427) bajo los 24 elementos.
- **La escritura llega a los usuarios.** La función DuckDB `ix_prime_form` devuelve este representante con el nombre de [«bracelet prime form»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/bracelet.rs#L9), así que una consulta que compare su salida con una tabla publicada discrepa en 35 clases con una tabla en la escritura de Forte y en 41 con una en la de Rahn.

**Los operadores neorriemannianos.** [`p`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L36), [`l`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L48) y [`r`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L59) implementan el §5 sobre las 24 tríadas consonantes, y una [prueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L134) comprueba que los tres son involuciones. La transcripción añade que generan un grupo de orden 24 y conmutan con T_1 y con T_0I. El comentario del deslizamiento dice [«L ∘ P ∘ R applied left-to-right»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L67), mientras que el código [`l(p(r(x)?)?)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L70) aplica R primero. Como S es una involución, ambos órdenes dan la misma tríada.

**El camino armónico no puede alcanzar la tríada aumentada.** `find_shortest_path` ejecuta el A* de IX sobre los conjuntos de un mismo cardinal, y un paso lleva a cualquier otro conjunto cuyo [vector de clases de intervalos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L129) esté a una distancia L1 de como mucho [2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L259):

```rust
    fn successors(&self) -> Vec<(PcSet, Self, f64)> {
        let card = self.current.cardinality();
        find_nearby(self.current, FIND_NEARBY_RADIUS_PER_STEP)
            .into_iter()
            .filter(|(s, _, _)| s.cardinality() == card && *s != self.current)
            .map(|(s, _, _)| {
                (
                    s,
                    PathNode {
                        current: s,
                        target: self.target,
                    },
                    1.0,
                )
            })
            .collect()
    }
```

- **Algunas clases forman islas.** Dos terceras mayores entre tres notas obligan a que el tercer intervalo sea también una tercera mayor, así que ningún tricordio tiene exactamente dos intervalos de clase 4. El vector ⟨000300⟩ de la tríada aumentada está por tanto a una distancia L1 de 4 o más del de cualquier otro tricordio, y las cuatro tríadas aumentadas forman una componente propia. Las 12 tríadas disminuidas forman otra, y entre los tetracordios, las tres séptimas disminuidas también. Los tricordios se reparten en componentes de 4, 12, 36 y 168 conjuntos, y los tetracordios en componentes de 3, 30 y 462.
- **«No encontrado» tiene dos significados.** [`find_shortest_path`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L275) devuelve un camino vacío cuando el [A* no encuentra ninguno](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-search/src/astar.rs#L169), y también cuando el más corto es más largo que `max_steps`. `ix_grothendieck_path` fija `max_steps` por defecto en [5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L7066) e informa de ambos casos como [`"found": false`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L7075). De {0, 4, 8} a {0, 4, 7} no informa de ningún camino, aunque mover una voz un semitono los une; la distancia está construida sobre un invariante, y no puede ver lo que ese invariante olvida.
- **La heurística es correcta; su comentario duda.** La heurística es [la mitad de la distancia L1 al objetivo](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L289). Es consistente, lo que el A* de IX necesita porque [los estados cerrados nunca se reabren](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-search/src/astar.rs#L75), así que los caminos que devuelve son los más cortos; todo tricordio de la componente de Do mayor está a 3 pasos o menos de Do mayor. El comentario de documentación llega a esa conclusión tras una corrección que se dejó tal cual, [«wait, actually»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L267).
- **Otras carencias.** Nada devuelve un estabilizador ni cuenta órbitas por el lema de Burnside; no hay forma prima en la escritura de Forte ni en la de Rahn; P, L y R solo están definidas sobre tríadas consonantes; y la búsqueda de caminos mide la distancia entre vectores de clases de intervalos, no la conducción de voces.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Muestra que la heurística h = L1/2 es consistente para pasos de coste 1 cuyos vectores de clases de intervalos difieren como mucho en 2 en distancia L1.

> *Solución:* Para un paso de u a v y un objetivo t, la desigualdad triangular da L1(u, t) ≤ L1(u, v) + L1(v, t) ≤ 2 + L1(v, t). Dividiendo entre 2, h(u) ≤ 1 + h(v): la estimación nunca baja más que el coste del paso, que es la consistencia, y h(t) = 0 en el objetivo.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Burnside frente a la enumeración.** Aplica `necklace_prime_form` y `bracelet_prime_form` a las 4096 máscaras y cuenta los resultados distintos para cada cardinal. Predicción: 352 y 224 en total, repartidos como en la tabla del §3.
2. **Estabilizadores.** Para cada máscara, cuenta los elementos que la fijan y los miembros de `orbit_unique`. Predicción: el producto es 24 para cada máscara; las rotaciones fijan 4224 conjuntos en total y las reflexiones 1152.
3. **Escrituras.** Compara `bracelet_prime_form` de cada clase con las formas primas de Forte y de Rahn. Predicción: 35 y 41 diferencias, con [0, 1, 3, 10] para 4-10.
4. **Ciclos neorriemannianos.** Aplica `p`, `l`, `r`, `s`, `n` y `h` dos veces a cada una de las 24 tríadas, y después alterna P y L, P y R, y R y L desde Do mayor. Predicción: seis involuciones, y ciclos de 6, 8 y 24 tríadas.
5. **Caminos.** Llama a `find_shortest_path` de {0, 4, 8} a {0, 4, 7} con `max_steps` 10, y de {0, 4, 7} a {0, 1, 2} con 3, y luego con 2. Predicción: un camino vacío; un camino de cuatro conjuntos; un camino vacío.

### Ejercicio práctico

En el paso 5, ¿cómo puede quien llama saber si un camino vacío significa que no existe ningún camino o que el límite era demasiado pequeño?

> *Solución:* Un camino más corto nunca visita dos veces el mismo conjunto, así que tiene menos pasos que conjuntos hay de ese cardinal. Con `max_steps` en C(12, k) − 1, 219 para los tricordios, un camino vacío significa que no existe ningún camino. Más barato aún: comparar las componentes del grafo de clases de intervalos, que solo dependen de los vectores.

---

## 8. Errores comunes

- **Componer en el orden equivocado.** T_mI T_n es T_(m−n)I, no T_(m+n)I; el grupo no es conmutativo, así que di qué aplicación actúa primero.
- **Dividir entre el orden del grupo para contar clases.** Los conjuntos simétricos tienen órbitas más pequeñas; usa el lema de Burnside, o cuenta las órbitas directamente.
- **Tomar un invariante por uno completo.** Vectores de clases de intervalos iguales no hacen equivalentes dos conjuntos bajo transposición e inversión: es la relación Z.
- **Mezclar convenciones de forma prima.** Las reglas de Forte y de Rahn difieren en seis clases, y un representante lexicográfico difiere de ambas en decenas; nombra la regla antes de comparar tablas.
- **Confundir una clase con su representante.** Dos herramientas pueden coincidir en todas las clases e imprimir aun así formas primas distintas.
- **Leer «ningún camino» como «sin relación».** Una distancia construida sobre un invariante no puede ver lo que el invariante olvida, como la conducción de voces.
- **Dejar sin precisar el orden de un producto neorriemanniano.** De izquierda a derecha y de derecha a izquierda solo coinciden cuando el producto es una involución, como en el caso de S.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Grupo** | Un conjunto con una composición asociativa, un elemento neutro y un inverso para cada elemento |
| **Grupo diédrico D12** | Las 24 simetrías del dodecágono regular: las transposiciones T_n y las inversiones T_nI |
| **Acción de grupo** | Una regla g·x bajo la cual la identidad no mueve nada y (gh)·x = g·(h·x) |
| **Órbita** | Las imágenes g·X de X; para D12 sobre conjuntos de clases de altura, una clase de conjuntos |
| **Estabilizador** | Los elementos g con g·X = X |
| **Teorema de la órbita y el estabilizador** | El tamaño de una órbita por el tamaño del estabilizador es igual al orden del grupo |
| **Lema de Burnside** | El número de órbitas es igual al número medio de puntos fijos |
| **Invariante** | Una función constante en las órbitas; completo cuando además las separa |
| **Relación Z** | Dos clases de conjuntos que comparten un vector de clases de intervalos |
| **Forma prima** | Un miembro canónico de una clase de conjuntos, elegido por una regla de desempate explícita |
| **P, L, R neorriemannianas** | Las inversiones de una tríada consonante que conservan dos de sus notas |
| **Involución** | Una aplicación que es su propia inversa |

---

## Autoevaluación

**1. Una tabla publicada da 4-10 como (0235), e IX imprime [0, 1, 3, 10]. ¿Se equivoca alguno de los dos?**
> Ninguno. T_10 envía {0, 2, 3, 5} a {10, 0, 1, 3}, así que ambos están en la misma órbita, y `forte_number` da 4-10 para ambos. Solo difieren en la regla que elige el representante: las reglas publicadas toman la forma más compacta, IX la lista ordenada lexicográficamente menor.

**2. Sin enumerar nada, ¿por qué una clase de conjuntos no puede tener 5 ni 7 miembros?**
> Por el teorema de la órbita y el estabilizador, el tamaño de una órbita es 24 dividido entre el orden de su estabilizador, que es un subgrupo de D12. Los tamaños posibles son los divisores de 24: 1, 2, 3, 4, 6, 8, 12 y 24.

**3. `ix_grothendieck_path` devuelve `"found": false` de la tríada aumentada a Do mayor. ¿Qué te dice eso?**
> Que en el grafo de IX, donde se unen los conjuntos cuyos vectores de clases de intervalos están a una distancia L1 de como mucho 2, las cuatro tríadas aumentadas forman una componente propia, puesto que ningún tricordio tiene exactamente dos intervalos de clase 4. No dice nada de la conducción de voces, donde un semitono las une. En general, el indicador también puede significar que el camino supera `max_steps`; aquí no puede ser, puesto que la componente tiene cuatro conjuntos.

**4. ¿Por qué P, L y R conmutan con todo T_n y todo T_nI?**
> Cada una conserva dos notas de la tríada y refleja la tercera nota respecto de ellas, una regla expresada en los intervalos propios de la tríada. T_n y T_nI transportan esos intervalos, así que aplicar P después de una transposición o una inversión da la imagen del resultado de P.

**Criterio de aprobación:** Describir la transposición y la inversión como el grupo D12 actuando sobre conjuntos de clases de altura; calcular órbitas y estabilizadores; contar clases con el lema de Burnside, en total y por cardinal; distinguir un invariante completo de uno incompleto y explicar la relación Z; trabajar con P, L y R y sus ciclos; y seguir qué representante llama IX forma prima y qué conjuntos puede alcanzar su búsqueda de caminos.

---

## Base de investigación

- W. Burnside, *Theory of Groups of Finite Order*, Cambridge University Press, 1897: el lema de recuento de órbitas, atribuido también a Cauchy y a Frobenius
- G. Pólya, «Kombinatorische Anzahlbestimmungen für Gruppen, Graphen und chemische Verbindungen», *Acta Mathematica* 68, 1937: el recuento bajo simetría
- A. Forte, *The Structure of Atonal Music*, Yale University Press, 1973: las clases de conjuntos y su numeración
- J. Rahn, *Basic Atonal Theory*, Longman, 1980: la regla de forma prima que usan la mayoría de las tablas actuales
- D. Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press, 1987: los grupos de transformaciones y la inversión contextual
- R. Cohn, «Maximally smooth cycles, hexatonic systems, and the analysis of late-Romantic triadic progressions», *Music Analysis* 15, 1996: los ciclos hexatónicos
- R. Cohn, «Neo-Riemannian operations, parsimonious trichords, and their Tonnetz representations», *Journal of Music Theory* 41, 1997: P, L, R y sus ciclos
- A. S. Crans, T. M. Fiore y R. Satyendra, «Musical actions of dihedral groups», *American Mathematical Monthly* 116, 2009: el grupo PLR como dual del grupo T/I
- D. Tymoczko, *A Geometry of Music*, Oxford University Press, 2011: la distancia de conducción de voces
- E. Amiot, *Music Through Fourier Space*, Springer, 2016: los módulos de Fourier como invariantes
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
