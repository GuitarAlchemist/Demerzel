---
module_id: psy-016-brier-score
department: psychohistory
course: "Pronósticos probabilísticos y la puntuación de Brier"
level: intermediate
prerequisites: ["psy-005-persistence-baseline"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-016
version: "0.1.0"
---

# Pronósticos probabilísticos y la puntuación de Brier

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo convertirá un historial de etiquetas en un suceso de sí o no, puntuará probabilidades declaradas con la puntuación de Brier y la puntuación logarítmica, medirá la pericia frente a un pronóstico de tasa base y comprobará si una regla de puntuación es *propia*. **Pregunta de proyecto:** ¿cómo debe puntuarse un pronóstico probabilístico sobre las etiquetas de gobernanza, y qué premia la puntuación?

[PSY-005](psy-005-persistence-baseline.es.md) puntuó el pronóstico «la etiqueta no cambia» contando aciertos y errores. Un pronosticador que dice «un cambio tiene una probabilidad del 2%» no acierta ni se equivoca en un par concreto: el número declarado necesita una puntuación específica, que aquí se construye sobre los pares de PSY-005. [PSY-017](psy-017-calibration-with-six-observations.es.md) trata la calibración (¿coinciden las probabilidades declaradas con las frecuencias observadas?) sobre un puñado de resultados; [PSY-025](psy-025-capstone-preregistered-forecast.es.md) aplica la puntuación a un pronóstico escrito de antemano.

## 1. Un suceso, una probabilidad declarada, una puntuación

**Observado.** En cada ejecución de un [script alimentador](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py) (el *feeder*), la [tendencia de calidad](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) del repositorio recibe una fila nueva por artefacto de gobernanza (una política, una habilidad), con una etiqueta de eficacia (`effectiveness_to`): un valor de verdad, como T (verdadero) o U (desconocido), atribuido a una proposición escrita sobre el artefacto. Como en PSY-005, un *par* lo forman dos filas consecutivas de un mismo artefacto, ambas con etiqueta. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-016/extract.py) toma una instantánea de los cinco archivos en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-016/observed-input.json): 1,548 filas, 18 artefactos, **1,529 pares**. La etiqueta difiere entre las dos filas en **1** par. Once pares empiezan en una *fila semilla* (un estado inicial registrado) y terminan 78.5 días después, en la primera ejecución del feeder; el único cambio está entre ellos. Los otros **1,518** pares unen dos ejecuciones del feeder, separadas por entre 0.001 y 6.453 días, y ninguno cambió.

El *suceso* es «la etiqueta difiere en la fila siguiente del artefacto»; el resultado `o` vale 1 si ocurrió y 0 si no. Un *pronóstico probabilístico* declara un número `p` entre 0 y 1 para el suceso antes de que se conozca el resultado. «La fila siguiente» no es un intervalo de tiempo fijo: un pronosticador que declara un mismo `p` para todos los pares trata un paso de 78.5 días como si fuera un paso de minutos.

La *puntuación de Brier* es la media de las diferencias al cuadrado entre la probabilidad declarada y el resultado:

```text
BS = (1/N) × suma de (p_i - o_i)²
```

Cuanto más baja, mejor: 0 significa estar siempre seguro y acertar; 1, estar siempre seguro y equivocarse. Brier (1950) añade el mismo término para «sin cambio», lo que duplica todos los valores (rango de 0 a 2); esta lección usa la forma habitual, de un solo término.

**Pronosticadores sintéticos, puntuaciones calculadas.** Nadie emitió pronósticos para estos pares. [`scenarios.json`](../../../fixtures/psychohistory/psy-016/scenarios.json) define pronosticadores imaginarios por la probabilidad que declara cada uno, y [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-016/analyze.py) los puntúa sobre los resultados observados ([`results.json`](../../../fixtures/psychohistory/psy-016/results.json)). Las puntuaciones se redondean a seis decimales, o a nueve donde hace falta.

| Pronosticador | Declara | Suma de errores al cuadrado | Puntuación de Brier, 1,529 pares | Puntuación de Brier, 1,518 pares |
|---|---|---|---|---|
| `never` | 0 | 1 | 0.000654022 | 0 |
| `base_rate` | 1/1,529 | 0.999346 | 0.000653594 | 0.000000428 |
| `one_percent` | 0.01 | 1.1329 | 0.000741 | 0.0001 |
| `five_percent` | 0.05 | 4.7225 | 0.003089 | 0.0025 |
| `coin` | 0.5 | 382.25 | 0.25 | 0.25 |

`never` es el pronóstico de persistencia de PSY-005 declarado con certeza. Para un pronóstico de 0 o 1, la puntuación de Brier es la tasa de error, aquí 1/1,529, la tasa base de cambio de PSY-005; `base_rate` declara esa proporción en cada par.

### Ejercicio práctico 1

Un pronosticador declara 0.02 en cada par. Calcule su suma de errores al cuadrado y su puntuación de Brier sobre los 1,529 pares, y después su puntuación de Brier sobre los 1,518 pares entre ejecuciones del feeder.

> **Respuesta:** El par que cambió aporta `(0.02 − 1)² = 0.9604`; los 1,528 pares sin cambio aportan `1,528 × 0.02² = 0.6112`. Suma: `1.5716`; puntuación de Brier: `1.5716 / 1,529 = 0.001028`. Entre ejecuciones del feeder nada cambió, así que cada par aporta `0.02² = 0.0004`, y esa es la puntuación.

## 2. Un solo par sostiene la puntuación

El *índice de pericia de Brier* (*Brier skill score*) compara un pronóstico con una referencia sobre los mismos pares, como hizo PSY-005 con la exactitud, pero esta lección sustituye la referencia de PSY-005, la persistencia, por la tasa base `b`, la proporción de pares en los que ocurrió el suceso, declarada en cada par:

```text
pericia = 1 - BS / BS_ref        BS_ref: puntuación de Brier de la referencia sobre los mismos pares
```

Para el pronóstico de tasa base, `BS_ref = b × (1 − b)`. Cuando la referencia no comete ningún error, la pericia queda indefinida, como ocurría con la persistencia en PSY-005: sobre los 1,518 pares, la referencia declara su tasa base, 0, mientras que el pronosticador `base_rate` mantiene 1/1,529.

**Calculado.** Cada suma de errores al cuadrado se divide en la parte del par que cambió y el resto:

| Pronosticador | Parte del par que cambió | Pericia |
|---|---|---|
| `never` | 100% | −0.000654 |
| `base_rate` | 99.93% | 0 |
| `one_percent` | 86.51% | −0.133641 |
| `five_percent` | 19.11% | −3.725591 |
| `coin` | 0.07% | −381.500164 |
| `long_step_hedge` | 88.86% | 0.087885 |

Para un pronosticador que declara un mismo `p` en todas partes, la puntuación es `(p - b)² + b × (1 - b)`, el caso de un solo valor de la partición de Murphy (1973), fiabilidad menos resolución más incertidumbre, en el que la resolución vale 0. El segundo término, la incertidumbre, aquí 0.000654, es el mismo para todos. El primero, la fiabilidad, es lo único que controla un pronosticador constante: `(0.01 − 0.000654)² = 0.000087` para `one_percent`. Así que ningún pronóstico constante puede superar a la tasa base de los pares sobre los que se puntúa: es una identidad, no un hallazgo. Una pericia positiva exige probabilidades distintas en pares distintos, más altas donde ocurren los cambios.

`long_step_hedge` (sintético) lo hace con una sola regla: 0.1 cuando la fila anterior es una fila semilla y 0.001 en los demás casos. Queda en primer lugar, por delante de `base_rate` y de `never`, con una pericia de 0.087885. Pero sus probabilidades las eligió el autor de esta lección después de ver dónde estaba el cambio, y toda su ventaja procede de un solo par: si se retira cualquiera de los 1,528 pares sin cambio, la clasificación no varía; si se retira el par que cambió, esos tres puestos se invierten.

**Conocimiento a posteriori.** `base_rate` también conoce la respuesta: 1/1,529 solo podía declararse una vez conocidos todos los resultados. Su ventaja sobre `never` es 0.000000428, el cuadrado de 1/1,529. Cuando se resolvió el par que cambió, en la primera ejecución del feeder, ningún par se había resuelto antes que él, así que el historial no ofrecía ninguna tasa base que declarar.

En este historial, los cuatro primeros pronosticadores puntúan entre 0.000596 y 0.000741, y el orden de los tres primeros descansa sobre un solo par. La puntuación sí los separa de `five_percent` y de `coin`.

### Ejercicio práctico 2

Vuelva a calcular la suma de errores al cuadrado de `long_step_hedge` a partir de sus dos probabilidades y de los recuentos de la sección 1, y después su puntuación de Brier y su pericia. ¿Qué queda de la suma sin el par que cambió?

> **Respuesta:** Par que cambió, desde una fila semilla: `(0.1 − 1)² = 0.81`. Diez pares sin cambio desde una fila semilla: `10 × 0.1² = 0.1`. Los 1,518 pares entre ejecuciones del feeder: `1,518 × 0.001² = 0.001518`. Suma: `0.911518`; puntuación de Brier: `0.911518 / 1,529 = 0.000596`. La suma de la tasa base es `0.999346`, así que pericia `= 1 − 0.911518 / 0.999346 = 0.087885`. Sin el par que cambió quedan `0.101518` sobre 1,528 pares, una puntuación de 0.000066: por detrás de `never` (0) y de `base_rate`, en el puesto 3.

### Ejercicio práctico 3

¿Cuántos de los 1,529 pares tendrían que cambiar para que declarar 0.01 en todas partes puntuara mejor que declarar 0? ¿Y para 0.05?

> **Respuesta:** Con `k` pares que cambian entre `N`, `never` puntúa `k/N` y un `p` constante puntúa `[k(1 − p)² + (N − k)p²]/N`. La segunda puntuación es menor cuando `Np² < 2kp`, es decir, `k > Np/2`. Para 0.01: `1,529 × 0.01 / 2 = 7.645`, así que 8 cambios. Para 0.05: `38.225`, así que 39.

## 3. Lo que significa «propia»

Una regla de puntuación es *propia* cuando un pronosticador obtiene la mejor puntuación esperada declarando la probabilidad en la que cree, y *estrictamente propia* cuando ninguna otra declaración lo hace igual de bien (Gneiting y Raftery 2007).

**Sintético.** Suponga que un suceso tiene una probabilidad verdadera `t = 0.3` y que un pronosticador declara `q` cada vez. La puntuación de Brier esperada es `t(1 − q)² + (1 − t)q² = (q − t)² + t(1 − t)`. Una alternativa tentadora, el error absoluto medio `|q − o|`, tiene como esperanza `t(1 − q) + (1 − t)q`.

| `q` declarado | Puntuación de Brier esperada | Error absoluto esperado | Puntuación de Brier media simulada |
|---|---|---|---|
| 0 | 0.3 | 0.3 | 0.30355 |
| 0.1 | 0.25 | 0.34 | 0.25284 |
| 0.3 | 0.21 | 0.42 | 0.21142 |
| 1 | 0.7 | 0.7 | 0.69645 |

La puntuación de Brier es mínima en `q = 0.3`, el valor verdadero. El error absoluto es mínimo en `q = 0`: premia a un pronosticador que cree en un 30% por decir «nunca». Una simulación con semilla fija (6,071 sucesos en 20,000 casos) coincide.

Con la puntuación de Brier, declarar un valor distinto del que se cree cuesta en esperanza `(q − t)²` por pronóstico. Para un suceso raro, eso es poco: con `t = 0.02`, declarar 0 cuesta 0.0004. De ahí que las primeras filas de la tabla de la sección 1 sean casi iguales: la puntuación de Brier es propia, pero paga poco por la diferencia entre «nunca» y «rara vez».

### Ejercicio práctico 4

Sintético. Usted cree que un suceso tiene probabilidad 0.2. Calcule la puntuación de Brier esperada y el error absoluto esperado si declara 0.2 y si declara 0. ¿Qué declaración premia cada regla?

> **Respuesta:** Brier: declarar 0.2 da `0.2 × 0.8² + 0.8 × 0.2² = 0.16`; declarar 0 da `0.2 × 1² + 0.8 × 0² = 0.2`. La declaración honesta gana por `0.04 = (0 − 0.2)²`. Error absoluto: declarar 0.2 da `0.2 × 0.8 + 0.8 × 0.2 = 0.32`; declarar 0 da `0.2`. Esa regla premia una certeza que el pronosticador no tiene, así que no es propia.

## 4. La puntuación logarítmica y la objeción más fuerte

La *puntuación logarítmica* (Good 1952) es la media de `−ln` de la probabilidad asignada a lo que ocurrió: `−ln p` cuando el suceso se produjo, `−ln(1 − p)` cuando no. También es estrictamente propia. **Calculado** (logaritmo natural):

| Pronosticador | Puntuación logarítmica, 1,529 pares | Puntuación logarítmica, 1,518 pares |
|---|---|---|
| `never` | infinita | 0 |
| `base_rate` | 0.005449 | 0.000654 |
| `one_percent` | 0.013056 | 0.01005 |
| `five_percent` | 0.053219 | 0.051293 |
| `coin` | 0.693147 | 0.693147 |
| `long_step_hedge` | 0.003188 | 0.001001 |

Entre ejecuciones del feeder, `never` es perfecto con las dos puntuaciones. Al añadir el único suceso, queda tercero con la puntuación de Brier, cuya pérdida está acotada en 1 por par, y último con la puntuación logarítmica, porque `−ln 0` no tiene un valor finito. La puntuación de Brier perdona una certeza que falla una vez en 1,529 pares; la puntuación logarítmica no la perdona nunca.

### Ejercicio práctico 5

Las pérdidas `−ln(…)` de `one_percent` suman 19.962083 sobre los 1,529 pares; el par que cambió aporta `−ln 0.01 = 4.60517`. Compruebe su puntuación logarítmica e indique la parte que corresponde al par que cambió. Diga después qué puntuación debería elegir un equipo si nadie debe declarar 0 para algo posible, y qué lo muestra en las tablas.

> **Respuesta:** `19.962083 / 1,529 = 0.013056`; la parte es `4.60517 / 19.962083 = 23.07%`, frente al 86.51% del error cuadrático del mismo pronosticador. El equipo debería elegir la puntuación logarítmica: `never` pasa de 0 sobre los 1,518 pares a infinito en cuanto se incluye el par que cambió, mientras que su puntuación de Brier solo pasa de 0 a 0.000654.

**Respuesta a la pregunta de proyecto.** Puntúe una probabilidad declarada con una regla propia, frente a una referencia que hubiera podido declararse de antemano. La puntuación de Brier premia las probabilidades honestas que difieren donde difieren los resultados; en este historial, la regla a posteriori `long_step_hedge` aventaja a `base_rate` por solo 0.000057, y esa ventaja depende de un solo par.

**La objeción más fuerte a esta lectura** es que quizá el suceso no sea pronosticable. El único cambio está en el paso de 78.5 días que parte de una fila semilla, y PSY-005 lo lee como una retirada registrada, no como una deriva. Entre ejecuciones del feeder nada cambió, así que ahí las dos puntuaciones premian el número declarado más pequeño. Los 1,529 pares son 18 artefactos leídos repetidamente, no ensayos independientes, y aquí ninguna puntuación lleva barra de error. **Con la puntuación de Brier, esta muestra no permite ordenar `never`, `base_rate` y `long_step_hedge`: su orden depende de un solo par. Con la puntuación logarítmica, esos mismos tres intercambian sus puestos según ese par: con él, `never` es último e infinito; sin él, primero.**

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cinco archivos de la tendencia de calidad y el script del feeder enlazados más arriba. `extract.py` se niega a ejecutarse si un archivo difiere de su blob de Git fijado.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-016/extract.py`, y después `analyze.py` en la misma carpeta. El [README](../../../fixtures/psychohistory/psy-016/README.md) enumera las autocomprobaciones y el control negativo.

**Referencias de método.** Brier, G. W. (1950), «Verification of Forecasts Expressed in Terms of Probability», *Monthly Weather Review* 78(1), 1–3. Murphy, A. H. (1973), «A New Vector Partition of the Probability Score», *Journal of Applied Meteorology* 12(4), 595–600. Gneiting, T., y Raftery, A. E. (2007), «Strictly Proper Scoring Rules, Prediction, and Estimation», *Journal of the American Statistical Association* 102(477), 359–378, [doi:10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437) (allí se escribe como una recompensa: su puntuación cuadrática de un pronóstico de sí o no es la puntuación de dos términos de Brier cambiada de signo, `−2(p − o)²`). Good, I. J. (1952), «Rational Decisions», *Journal of the Royal Statistical Society, Series B* 14(1), 107–114, [doi:10.1111/j.2517-6161.1952.tb00104.x](https://doi.org/10.1111/j.2517-6161.1952.tb00104.x).

**No realizado.** No se emitió ningún pronóstico antes de conocer su resultado: todos los pronosticadores son imaginarios, y `base_rate` y `long_step_hedge` recurren a información a posteriori. No se examinó la calibración (PSY-017). Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Cuando el historial contenga varios cambios entre ejecuciones del feeder, puntuar probabilidades anotadas antes de cada ejecución frente a una referencia fijada de antemano. Si una regla cuya probabilidad crece con el tiempo transcurrido entre las dos filas mantiene ahí una pericia positiva, «un solo par decide la clasificación» deja paso a «la longitud del paso aporta información».
