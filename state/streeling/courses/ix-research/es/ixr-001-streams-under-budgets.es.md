---
module_id: ixr-001-streams-under-budgets
department: ix-research
course: "Pipelines de IX en flujo, con presupuestos"
level: intermediate
prerequisites: []
estimated_duration: "40 minutes"
produced_by: claude-ix-research
research_cycle: null
version: "0.1.0"
---

# Flujos con presupuesto: contrapresión, una compuerta que aprende y una verificación de Petri

> **Departamento de Investigación sobre IX** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión humana pendiente. No existe ningún registro de ciclo de investigación para este módulo (véase «Procedencia»).

## Objetivos y pregunta del proyecto

Al terminar este módulo sabrás:

- explicar cómo los canales acotados convierten un nodo lento en contrapresión, hasta el motor SQL que alimenta el flujo, y cómo una parada viaja en sentido contrario;
- enviar cada elemento a un solo experto con un presupuesto en dinero, y nombrar los tres recursos que gasta un enrutador así: la calidad, el dinero y la capacidad;
- devolver la opinión de un juez a un enrutador sin un ciclo de canales;
- decir, antes de ejecutar, si un grafo de enlaces que esperan puede quedar en interbloqueo, y qué cambia un solo enlace con pérdida.

**Pregunta del proyecto:** ¿se puede enrutar un flujo de preguntas de guitarra entre un enrutador local gratuito y un experto de pago, con un presupuesto fijo, de modo que supere a una regla fija con el mismo gasto, sin colas que crezcan ni interbloqueos?

El estudio trata del crate [`ix-stream`](https://github.com/GuitarAlchemist/ix/tree/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream), commit [`14dccd0`](https://github.com/GuitarAlchemist/ix/commit/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab) de la rama `exp/loop-nodes` de GuitarAlchemist/ix. Todos los enlaces al código que siguen están fijados en ese commit.

## 1. El punto de partida: un pipeline que ni fluye ni corre en paralelo

IX ya ejecuta pipelines: `ix-pipeline` traduce un `ix.yaml` a un DAG y lo ejecuta. Su ejecutor avanza nivel por nivel, con una barrera tras cada nivel, y cada nodo recibe un valor JSON entero. La rama que trata un nivel de varios nodos anuncia «en paralelo», pero ejecuta cada nodo en el hilo actual, como dice el comentario que contiene, porque la función de cálculo de un nodo no es `Send` ([`executor.rs`, líneas 164 a 211](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-pipeline/src/executor.rs#L164-L211)).

Así, un pipeline sobre una consulta grande espera el resultado entero y luego ejecuta sus nodos uno tras otro. Nada frena cuando un nodo es lento, porque nada fluye. `ix-stream` es una rebanada trazadora del otro modelo: los valores fluyen de uno en uno por un grafo de hilos unidos por canales acotados.

## 2. Contrapresión y cancelación

Cada nodo de un grafo `ix-stream` es uno o varios hilos, sus trabajadores, que comparten un canal de entrada con un máximo de `cap` valores ([`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/lib.rs#L1-L16)). Un envío a un canal lleno espera. Esa espera es la contrapresión: un nodo lento retiene todo lo que está aguas arriba, hasta la fuente, en lugar de dejar crecer una cola. Es el `request(n)` de Reactive Streams en su forma más simple, donde `n` es el número de huecos libres.

La fuente puede ser una consulta de DuckDB. [`source::duckdb`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/source.rs#L28) ejecuta la CLI `duckdb` con `-jsonlines` y envía cada fila en cuanto la lee. Cuando el grafo está lleno, la fuente deja de leer, la tubería se llena y DuckDB espera en su escritura: la contrapresión llega al motor SQL.

La cancelación va en sentido contrario. Cuando un nodo se detiene, o todos sus trabajadores terminan, su entrada se descarta y todo envío hacia él falla. Un nodo cuyos enlaces llevan todos a nodos terminados se detiene también, así que la parada sube hasta la fuente, y la fuente DuckDB mata entonces su proceso: una consulta que ya nadie lee deja de calcular.

**Probado.** [`a_full_channel_holds_the_source_back`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L13-L61) construye la cadena fuente → `a` (cap 2, 1 trabajador) → `b` (cap 3, 2 trabajadores) → `sink` (cap 4, 1 trabajador), retiene el sumidero en su primer valor y cuenta, a los 400 ms, los valores que han salido de la fuente frente a esta cota:

```rust
// Values in channels, plus one in each worker's hand, plus the source's next one.
let bound = (2 + 1) + (3 + 2) + (4 + 1) + 1;
```

(El comentario dice: los valores en los canales, más uno en la mano de cada trabajador, más el siguiente de la fuente.) Así, como mucho 14 de los 10 000 valores salen de la fuente mientras el sumidero retiene. [`a_stopped_graph_stops_the_duckdb_query`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L374-L401) comprueba que detener el grafo detiene la consulta. Las 18 pruebas de `tests/stream.rs` pasaron en el commit fijado el 2026-10-16, incluidas las 3 que necesitan la CLI de DuckDB (Windows 11, DuckDB v1.5.3, compilación debug); estas son la primera y la última línea de su salida:

```text
running 18 tests
test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.41s
```

### Ejercicio práctico 1

Una cadena fuente → `parse` (cap 8, 4 trabajadores) → `score` (cap 2, 1 trabajador) → `sink` (cap 16, 1 trabajador). El sumidero se bloquea en su primer valor. ¿Cuántos valores, como mucho, pueden haber salido de la fuente?

> **Respuesta:** cada nodo retiene su canal más un valor por trabajador: (8 + 4) + (2 + 1) + (16 + 1) = 32, más el valor que la fuente sostiene mientras espera para enviarlo: 33. La cota no depende de la longitud del flujo, y en eso consiste la contrapresión.

## 3. Retroalimentación sin ciclo: el bus algedónico

Un enrutador que aprende tiene que saber cómo salieron sus elecciones, y el juez está aguas abajo de él. Un canal del juez al enrutador cerraría un ciclo de enlaces que esperan, y la sección 6 muestra que un ciclo así puede atascarse.

Por eso `ix-stream` envía la retroalimentación por un [`Bus`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/bus.rs) aparte. Quien publica nunca espera: cada suscriptor tiene su propia cola acotada, y un evento que la encuentra llena se pierde para ese suscriptor y se cuenta. Por él viajan señales de placer (valencia +1) y de dolor (−1): el juez dice acierto o error para cada elemento, una vía de pago informa de la parte de su presupuesto que gastó cada llamada, y el enrutador señala dolor cuando una vía que quería estaba llena. Antes de enrutar el elemento siguiente, el enrutador lee las señales que han llegado, y nunca espera ninguna.

El nombre viene del modelo de sistema viable de Stafford Beer, donde una señal algedónica salta la jerarquía normal. [CYB-001](../../cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md) nombra la falta de canal algedónico como la brecha D de la gobernanza de Demerzel. Este bus aplica la misma idea dentro de un pipeline, y pierde eventos en lugar de bloquear, porque aquí una señal es una pista para aprender, no una alarma.

## 4. Una compuerta que enruta como la de una mezcla de expertos, con presupuestos

La [compuerta](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs) envía cada elemento a un solo experto, un *brazo*. Para cada contexto, una casilla que calcula quien la llama, mantiene un bandido UCB1 de `ix-rl` que estima lo buenas que resultaron las respuestas de cada brazo. Ordena los brazos según

```text
score(arm) = q(arm) + 0.3 * sqrt(2 * ln(N) / n(arm)) - price(arm)
```

donde `q` es la calidad media juzgada del brazo en ese contexto, `n` cuántas veces se juzgó allí y `N` el total del contexto. Un brazo nunca probado en un contexto puntúa +∞, así que cada brazo se prueba una vez. El 0.3 es el peso de exploración por defecto de la compuerta.

Un brazo con presupuesto tiene un precio sombra que sigue su ritmo ([`price`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs#L178)):

```text
price(arm) = max(0, base_price + 4 * (spent / cap - share of the stream seen))
```

(`spent / cap` es la parte del presupuesto gastada y `share of the stream seen` la parte del flujo ya vista.) El precio es infinito cuando el presupuesto no puede pagar una llamada más, y 4 es la ganancia por defecto. Gastar por delante del ritmo sube el precio, lo que reserva el brazo para los contextos donde más gana; quedarse atrás lo baja. El precio solo orienta. El tope firme es el [`Ledger`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs#L58), el libro mayor: una vía gasta de él, y el libro rechaza una llamada que no puede pagar.

### Ejercicio práctico 2

El brazo Jev tiene un precio base de 0.02. A mitad del flujo, Jev ha gastado el 60 % de su presupuesto. ¿Cuál es su precio? ¿Y si hubiera gastado el 40 %?

> **Respuesta:** 0.02 + 4 × (0.6 − 0.5) = 0.42: Jev solo gana un contexto donde su calidad estimada, con su bonificación de exploración, supera en más de 0.42 a la del enrutador local gratuito. Al 40 %: 0.02 + 4 × (0.4 − 0.5) = −0.38, que se queda en 0: Jev no cuesta nada hasta que alcanza su ritmo.

## 5. El experimento: 663 preguntas de guitarra, dos expertos, un presupuesto

[`examples/route.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/examples/route.rs) hace fluir las 221 preguntas etiquetadas del estudio del enrutador Jev: 190 piden uno de los 32 skills de GA y 31 están fuera de alcance, etiquetadas `__none__` ([`RESULTS.md`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/RESULTS.md), etapa 3). Las hace fluir tres veces, en un orden que DuckDB baraja con un hash con semilla: 663 elementos. Cada elemento pasa por:

1. `local`: la respuesta que le dio el enrutador local por embeddings (`c2-merge`), grabada, con su confianza;
2. `kw`: un experto por palabras clave escrito en Zig, compilado para WASI y ejecutado en el entorno aislado de `ix-wasm`;
3. `gate`: aceptar `local` o consultar a Jev, en uno de seis contextos ([`context`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/examples/route.rs#L279)): el enrutador local declinó, quedó por debajo de 0.7 o llegó al menos a 0.7, cruzado con si `kw` coincide con él;
4. `jev`: la respuesta grabada de Jev, tras una pausa que hace las veces de la latencia de una llamada real, cobrada al coste medio por llamada del estudio. Jev es el clasificador alojado zero-shot `jev-1.13.0` de TypeSafe. **No se envía nada a Jev**: las respuestas se reproducen a partir de los recibos del estudio;
5. `judge`: compara la respuesta con la etiqueta y señala acierto o error en el bus.

El ejemplo también puede añadir una vía de Claude Haiku en directo, con el plan de la persona, limitada en llamadas. Por defecto no se usa ninguna, y ningún resultado de abajo la incluye (véase la sección 8).

**El presupuesto.** Las 221 llamadas a Jev grabadas en el estudio costaron 0.026733 USD según la tarifa publicada, calculado a partir de los tokens de entrada declarados, no facturado ([`full/jev-eval.json`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/jev/full/jev-eval.json)): 0.000120962 USD por llamada. El ejemplo concede a Jev el 40 % del flujo: 0.4 × 663 × 0.000120962 = **0.0320792472 USD, el precio de 265.2 llamadas**.

**Las políticas.** `local` se queda siempre con la respuesta local. `jev` consulta a Jev hasta agotar su presupuesto y después se queda con la respuesta local: «Jev hasta agotarlo». `learned` es la compuerta de la sección 4.

**Esperar o no.** Con `--wait`, la compuerta espera su primera elección cuando esa vía está llena. Sin esa opción, una vía llena se salta en favor de la elección siguiente, como una mezcla de expertos descarta lo que desborda la capacidad de un experto.

**Observado.** Cada ejecución escribe `results.jsonl`, una línea por elemento. Esta consulta cuenta, para cada ejecución, los aciertos y las llamadas a Jev realizadas:

```sql
SELECT regexp_extract(filename, 'route-[a-z]+(-wait)?-seed[0-9]+') AS run,
       count(*) AS n,
       sum(correct::INT) AS right_n,
       count(*) FILTER (WHERE arm = 'jev' AND fallback IS NULL) AS jev_calls
FROM read_json('route-*/results.jsonl', filename = true, union_by_name = true)
GROUP BY ALL ORDER BY run;
```

```text
┌───────────────────────────┬───────┬─────────┬───────────┐
│            run            │   n   │ right_n │ jev_calls │
│          varchar          │ int64 │ int128  │   int64   │
├───────────────────────────┼───────┼─────────┼───────────┤
│ route-jev-seed7           │   663 │     483 │        84 │
│ route-jev-wait-seed1      │   663 │     523 │       265 │
│ route-jev-wait-seed2      │   663 │     527 │       265 │
│ route-jev-wait-seed3      │   663 │     522 │       265 │
│ route-jev-wait-seed4      │   663 │     525 │       265 │
│ route-jev-wait-seed5      │   663 │     526 │       265 │
│ route-jev-wait-seed7      │   663 │     524 │       265 │
│ route-learned-seed7       │   663 │     471 │        84 │
│ route-learned-wait-seed1  │   663 │     555 │       265 │
│ route-learned-wait-seed11 │   663 │     557 │       265 │
│ route-learned-wait-seed2  │   663 │     554 │       265 │
│ route-learned-wait-seed3  │   663 │     550 │       265 │
│ route-learned-wait-seed4  │   663 │     551 │       265 │
│ route-learned-wait-seed5  │   663 │     550 │       265 │
│ route-learned-wait-seed7  │   663 │     546 │       265 │
│ route-local-seed7         │   663 │     456 │         0 │
└───────────────────────────┴───────┴─────────┴───────────┘
  16 rows                                       4 columns
```

Las ejecuciones con cinco semillas reprodujeron a Jev con una pausa de 40 ms (`--jev-ms 40`); las de la semilla 7 usaron los 400 ms por defecto. Todas daban 4 trabajadores a Jev.

| Política | Espera | Pausa de Jev | Semillas | Aciertos de 663 | Exactitud | Llamadas a Jev |
|---|---|---|---|---|---|---|
| local | — | — | 7 | 456 | 0.688 | 0 |
| Jev hasta agotarlo | sí | 40 ms | 1 a 5 | 523, 527, 522, 525, 526 | media 0.791 (0.787 a 0.795) | 265 |
| compuerta aprendida | sí | 40 ms | 1 a 5 | 555, 554, 550, 551, 550 | media 0.833 (0.830 a 0.837) | 265 |
| Jev hasta agotarlo | sí | 400 ms | 7 | 524 | 0.790 | 265 |
| compuerta aprendida | sí | 400 ms | 7 | 546 | 0.824 | 265 |
| Jev hasta agotarlo | no | 400 ms | 7 | 483 | 0.729 | 84 |
| compuerta aprendida | no | 400 ms | 7 | 471 | 0.710 | 84 |

El enrutador local solo obtiene 456 de 663, que son los 152 de 221 grabados por el estudio, tres veces: sus respuestas están grabadas y cada pasada las repite.

**Calculado.** Esperando a su vía elegida, con el mismo gasto (265 llamadas a Jev, 0.03206 USD), la compuerta aprendida supera a «Jev hasta agotarlo» en cada semilla, por 32, 27, 28, 26 y 24 preguntas: **4.1 puntos** de media (27.4 de 663). En la semilla 7, con una vía de 400 ms, gana por 22.

**De dónde sale la ganancia.** Los mismos archivos, agrupados por contexto sobre las semillas 1 a 5 (`to_jev`: parte de los elementos enviados a Jev; `acc_local` y `acc_jev`: exactitud en los elementos que respondió cada brazo):

```sql
SELECT ctx,
       regexp_extract(filename, 'route-([a-z]+)-wait', 1) AS policy,
       count(*) / 5 AS per_run,
       round(avg((arm = 'jev')::INT), 2) AS to_jev,
       round(avg(correct::INT), 3) AS acc,
       round(avg(correct::INT) FILTER (WHERE arm = 'local'), 2) AS acc_local,
       round(avg(correct::INT) FILTER (WHERE arm = 'jev'), 2) AS acc_jev
FROM read_json('route-*-wait-seed[1-5]/results.jsonl', filename = true, union_by_name = true)
GROUP BY ALL ORDER BY ctx, policy;
```

```text
┌───────┬─────────┬─────────┬────────┬────────┬───────────┬─────────┐
│  ctx  │ policy  │ per_run │ to_jev │  acc   │ acc_local │ acc_jev │
│ int64 │ varchar │ double  │ double │ double │  double   │ double  │
├───────┼─────────┼─────────┼────────┼────────┼───────────┼─────────┤
│     0 │ jev     │   114.0 │   0.41 │  0.602 │      0.35 │    0.97 │
│     0 │ learned │   114.0 │   0.88 │  0.896 │      0.34 │    0.97 │
│     1 │ jev     │    66.0 │    0.4 │  0.894 │      0.82 │     1.0 │
│     1 │ learned │    66.0 │   0.56 │  0.912 │       0.8 │     1.0 │
│     2 │ jev     │    63.0 │   0.38 │  0.584 │      0.47 │    0.77 │
│     2 │ learned │    63.0 │    0.5 │  0.619 │      0.48 │    0.75 │
│     3 │ jev     │    15.0 │    0.4 │    1.0 │       1.0 │     1.0 │
│     3 │ learned │    15.0 │   0.19 │    1.0 │       1.0 │     1.0 │
│     4 │ jev     │   273.0 │   0.41 │  0.805 │      0.71 │    0.94 │
│     4 │ learned │   273.0 │    0.3 │  0.779 │      0.71 │    0.94 │
│     5 │ jev     │   132.0 │   0.41 │   0.95 │      0.93 │    0.97 │
│     5 │ learned │   132.0 │   0.09 │  0.932 │      0.93 │    0.95 │
└───────┴─────────┴─────────┴────────┴────────┴───────────┴─────────┘
  12 rows                                                 7 columns
```

«Jev hasta agotarlo» envía a Jev el primer 40 % del flujo, sea cual sea el contexto. La compuerta aprende que en el contexto 0, donde el enrutador local declinó y el experto por palabras clave propone un skill, el enrutador local acierta en cerca de un tercio de los elementos y Jev en el 97 %: le envía el 88 %. Lo paga en el contexto 5, donde el enrutador local está seguro y el experto por palabras clave coincide, enviando allí solo el 9 %. Pierde un poco en los contextos 4 y 5 y gana mucho más en el contexto 0.

**Una nota sobre los recibos.** El mensaje del commit `14dccd0` da la compuerta aprendida en 0.832 (0.828 a 0.837). Los archivos dan 0.833 (0.830 a 0.837), porque la carpeta de la semilla 3 se reescribió unos cinco minutos después del commit con una versión posterior del ejemplo, y esa nueva ejecución acertó una pregunta más (550 en lugar de 549, el único total que se redondea a 0.828). La diferencia de 4.1 puntos es la misma en ambos casos. La sección 8 explica por qué dos ejecuciones con la misma semilla pueden diferir.

## 6. La capacidad, un tercer recurso

Sin esperar, el mismo presupuesto compra mucho menos. La vía de Jev admite 4 elementos y tiene 4 trabajadores, cada uno ocupado 400 ms por llamada: como mucho 10 llamadas por segundo, mientras que una ejecución entera de 663 elementos duró unos 8.6 segundos. Una compuerta que encuentra la vía llena la salta y se queda con la respuesta local. En la semilla 7 solo hubo **84 de las 265 llamadas pagables** (0.01016 USD de 0.03208), con las dos políticas, y ambas acabaron entre 0.71 y 0.73. En esa ejecución la regla fija lo hizo mejor que la compuerta, 483 frente a 471: cuando la capacidad rechaza la mayoría de las elecciones de la compuerta, lo que aprendió sobre la calidad ya no decide.

Es el factor de capacidad de las capas de mezcla de expertos. En el Switch Transformer (Fedus, Zoph y Shazeer, 2021), cada experto toma como mucho un número fijo de tokens por lote, y los tokens que lo desbordan se saltan el experto y pasan sin cambios por la conexión residual. Un enrutador gasta calidad y dinero, y también el rendimiento de cada experto. Los precios de la compuerta solo cubren el dinero. Convertir «esperar o desbordar» en una elección que la compuerta aprenda, con la latencia contada como un coste, es trabajo pendiente.

## 7. Una verificación de Petri antes de ejecutar

¿Pueden los hilos quedar en interbloqueo? [`petri.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/petri.rs#L1-L23) traduce el grafo a una red de Petri con `ix-petri`. `ix-petri` no tiene capacidades de lugar, así que cada canal se convierte en dos lugares: los valores que contiene y sus huecos libres, que empiezan en su capacidad. Cada envío toma un hueco libre y cada recepción devuelve uno, de modo que el par siempre tiene `cap` marcas y la red está acotada por construcción. Los trabajadores de un nodo son marcas de su lugar `idle`. Un trabajador toma un valor y lo sostiene; puede no enviar nada, como hace un filtro, o comprometerse con un puerto y esperar allí un hueco libre; en un puerto con pérdida puede además soltar lo que sostiene.

La red puede comprometerse con un puerto en cualquier momento, que es más de lo que hacen los hilos, así que tiene todos los comportamientos de los hilos: una red sin interbloqueo garantiza hilos sin interbloqueo. Lo contrario no se cumple: un interbloqueo señalado puede ser uno al que los hilos nunca llegan.

**Acíclico significa sin interbloqueo, sin explorar.** Supongamos que los enlaces que esperan, todos salvo los que pierden, no forman ningún ciclo. Una marca muerta exigiría un trabajador esperando ante un nodo lleno cuyos trabajadores esperan todos más abajo. Siguiendo los enlaces que esperan aguas abajo en un grafo acíclico se termina en un sumidero, que siempre toma, así que tal marca no existe. Por eso [`check`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/petri.rs#L243) responde de inmediato para un grafo acíclico, aunque sea una cadena de cientos de nodos, y solo explora las marcas alcanzables cuando hay un ciclo. Si los enlaces que esperan son acíclicos lo dice el `Dag` de `ix-pipeline`, que rechaza una arista que cerraría un ciclo. El grafo de enrutamiento de la sección 5 es acíclico: su `petri.json` indica `method: acyclic`, 26 lugares, 22 transiciones, 0 estados explorados.

**Un bucle de reintento se atasca; un enlace con pérdida lo libera.** La forma de prueba [`retry_loop`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L254-L269) es fuente → compuerta → experto → juez → fin, más un enlace del juez a la compuerta para lo que rechaza; cada canal contiene un valor y cada nodo tiene un trabajador. Un programa desechable que llama a `check` y a `explore` sobre esa forma imprimió, en el commit fijado:

```text
waiting retry, check: method=Reachability deadlock_free=Some(false) states=1728 places=21 transitions=18
dead marking: done free=1 rows waiting on gate=1 gate waiting on expert=1 expert waiting on judge=1 judge waiting on gate=1 gate queued=1 expert queued=1 judge queued=1
witness: 44 firings, the last four: rows picks gate, gate picks expert, expert picks judge, judge picks gate
lossy retry, check: method=Acyclic deadlock_free=Some(true) states=0 places=21 transitions=19
lossy retry, explore: method=Reachability deadlock_free=Some(true) states=1728 places=21 transitions=19
```

En la marca muerta, cada canal del bucle está lleno y cada trabajador sostiene un valor que no puede colocar: el juez espera a la compuerta, que espera al experto, que espera al juez. El testigo es la secuencia de 44 disparos que lleva hasta allí. Si el enlace de reintento pierde, los enlaces que esperan vuelven a ser acíclicos: `check` responde sin explorar, y una exploración completa de las mismas 1728 marcas lo confirma. Un reintento perdido cuenta como `refused` en las estadísticas del nodo, así que la pérdida sigue siendo visible. Por eso, también, el juez de la sección 3 habla con la compuerta por el bus y no por un canal.

### Ejercicio práctico 3

¿Por qué falla el argumento acíclico en el bucle de reintento?

> **Respuesta:** sigue los enlaces que esperan aguas abajo hasta llegar a un sumidero, que siempre toma. En el bucle, juez → compuerta es un enlace que espera, así que los enlaces que salen de la compuerta vuelven a ella y nunca llegan a un sumidero: cada nodo del ciclo puede estar lleno y esperando al siguiente.

### Ejercicio práctico 4

Tienes que conservar los reintentos. Da dos maneras de mantener el bucle sin interbloqueo, y lo que cuesta cada una.

> **Respuesta:** hacer que el enlace de reintento pierda, y un reintento se pierde cada vez que la compuerta está llena (la pérdida se cuenta); o sacar el reintento de los canales, como hace el bus con la retroalimentación, y entonces un reintento llega cuando llega, sin garantía de que llegue. En ambos casos se renuncia a una garantía sobre los reintentos para obtener una garantía contra el interbloqueo.

## 8. Tres lecciones sobre los recibos

**Declinar es una respuesta.** El primer borrador de este experimento fue una simulación en Python fuera de línea. Contaba como errores los rechazos del enrutador local y le daba un 55 %; el flujo, que puntúa las respuestas grabadas frente a las etiquetas, encontró un 68.8 %. Recalculado a partir de los archivos grabados: el enrutador local declina 60 de las 221 preguntas, y 31 de ellas son las 31 preguntas fuera de alcance, todas. Cuenta un rechazo como la respuesta `__none__` y el enrutador acierta 152 de 221 (0.688); cuéntalo como error y acierta 121 (0.548). El código de la simulación no se conservó; su 55 % es lo que da ese error de puntuación.

**Una semilla fija el orden del flujo, no la ejecución.** La semilla fija el orden en que DuckDB envía los elementos. La compuerta aprende de señales que llegan mientras otros trabajadores corren, así que dos ejecuciones con la misma semilla pueden elegir distinto: la nueva ejecución de la semilla 3, en la sección 5, se movió una pregunta.

**Un recibo puede sobrescribirse.** La sesión que construyó el crate informó de una ejecución con una vía de Claude Haiku en directo (12 llamadas con el plan de la persona) en 0.840, semilla 11. La carpeta de la semilla 11 contiene hoy una ejecución sin esa vía, con 557 de 663 (0.840), y no existe ninguna carpeta de trabajo de Claude. El nombre de la carpeta codificaba la política, el modo de espera y la semilla, pero no el límite de Claude, así que una ejecución escribió encima de la otra, y ya no se puede saber de cuál viene el 0.840. Sin recibo, este módulo no da ninguna cifra para la vía de Claude. Cada opción que cambia el grafo tiene su sitio en el nombre de la carpeta donde escribe una ejecución.

## 9. Lo que esto muestra y lo que no

**Mostrado:**

- la contrapresión de un nodo lento hasta el proceso de DuckDB, y la cancelación en sentido contrario, con pruebas que pasan;
- con el mismo gasto, si la compuerta espera su elección, un bandido por contexto con un precio sombra ajustado al ritmo supera a «Jev hasta agotarlo» en cada una de las cinco semillas, por 4.1 puntos de media;
- sin esperar, lo que limita es la capacidad de un experto, no su presupuesto;
- los enlaces que esperan, si son acíclicos, no pueden quedar en interbloqueo, y un bucle de reintento de enlaces que esperan sí puede.

**No mostrado:**

- Jev en directo: cada respuesta de Jev se reproduce a partir de los recibos del estudio, y su latencia es una pausa;
- la generalidad: un solo corpus de 221 preguntas escritas por un modelo, vistas tres veces, así que la compuerta se puntúa sobre las preguntas de las que aprende. Una pasada reservada es la próxima comprobación. Con títulos de preguntas escritos por personas (la etapa 4 del estudio), el mismo enrutador local envió a un skill 32 de las 86 que debía declinar;
- la significación: cinco semillas de un solo diseño, emparejadas por semilla, sin prueba estadística;
- el rendimiento en una compilación release: estas ejecuciones son compilaciones debug;
- la vía de Claude (sección 8).

## Ideas clave

- Un canal acotado es todo el mecanismo de contrapresión: un nodo lento bloquea a quienes le envían, hasta el motor SQL, y los valores en vuelo tienen una cota que se puede calcular.
- La retroalimentación viaja por un bus con pérdida, nunca de vuelta por un canal: un enrutador que espera su propia retroalimentación puede atascarse.
- Una compuerta con presupuesto gasta donde más gana solo si su precio sigue el ritmo del presupuesto; el tope firme es el libro mayor, no el precio.
- La calidad y el dinero no bastan: la capacidad de un experto decide cuando el enrutador no puede esperar.
- Verifica el grafo antes de ejecutar: los enlaces que esperan, si son acíclicos, no se interbloquean por un argumento, y un ciclo necesita una exploración o un enlace con pérdida.

## Procedencia

- **Código:** GuitarAlchemist/ix, rama `exp/loop-nodes`, commit `14dccd0ef1fb0f4395d38f5beed9ad42fa458eab` (2026-10-16), crate `crates/ix-stream`. Desde entonces la rama recibió nodos SQL (commit `944f42c`), que este módulo no cubre.
- **Datos:** el estudio del enrutador Jev en el commit `7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da`, en `state/router-spike/`: el corpus `jev/corpora/full-sol.json`, las respuestas locales `jev/full/local-c2-merge.json`, las respuestas y el consumo de Jev `jev/full/jev-eval.json`, y `RESULTS.md`.
- **Resultados:** las 16 carpetas `route-*` que `examples/route.rs` escribió el 2026-10-16 en la máquina del autor, leídas para este módulo el mismo día. No están publicadas. Dos de ellas, local y «Jev hasta agotarlo» sin espera en la semilla 7, son anteriores al commit en un cuarto de hora aproximadamente: a su primer evento le faltan los campos `wait` y `jev_workers` que escribe el ejemplo del commit.
- **Pruebas:** `cargo test -p ix-stream --test stream -- --include-ignored` en el commit fijado: 18 pasadas.
- **Ciclo de investigación:** ninguno. Este módulo se escribió a partir de una rebanada trazadora hecha en una sesión de Claude Code, no con `/seldon research-cycle`, y no existe ningún registro suyo en `state/streeling/research-cycles/`. Necesita una revisión humana antes de contar como publicado.

Se pueden repetir ejecuciones como estas con la CLI de DuckDB y Zig en el path (o `IX_DUCKDB` e `IX_ZIG`). El ejemplo del commit nombra sus carpetas de salida como la tabla de arriba:

```text
cargo run -p ix-stream --example route -- --policy learned --wait --seed 1 --jev-ms 40
cargo run -p ix-stream --example route -- --policy jev --wait --seed 1 --jev-ms 40
cargo run -p ix-stream --example route -- --policy learned --seed 7
```

## Para saber más

- [CYB-001](../../cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md): el canal algedónico en la gobernanza de Demerzel.
- [CS-002](../../computer-science/es/cs-002-governing-agentic-loops.es.md): límites que impone el marco, no el modelo.
- [PSY-025](../../psychohistory/es/psy-025-capstone-preregistered-forecast.es.md): el prerregistro, que el estudio de Jev aplicó a cada una de sus etapas.

## Referencias

- Reactive Streams, versión 1.0, `Subscription.request(n)`.
- Stafford Beer, *Brain of the Firm*, 1972: la señal algedónica del modelo de sistema viable.
- Peter Auer, Nicolò Cesa-Bianchi y Paul Fischer, «Finite-time Analysis of the Multiarmed Bandit Problem», *Machine Learning* 47, 2002: UCB1.
- William Fedus, Barret Zoph y Noam Shazeer, «Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity», arXiv:2101.03961, 2021: la capacidad de los expertos y el factor de capacidad.
- Tadao Murata, «Petri Nets: Properties, Analysis and Applications», *Proceedings of the IEEE* 77(4), 1989: lugares acotados mediante lugares complementarios.

---
*Producido para el Departamento de Investigación sobre IX el 2026-10-16 a partir de los recibos enumerados en «Procedencia». Sin ciclo de investigación; revisión humana pendiente.*
