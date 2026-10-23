---
module_id: psy-005-persistence-baseline
department: psychohistory
course: "Primero, la persistencia: la referencia que un pronóstico de gobernanza debe superar"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-005
version: "0.1.0"
---

# Primero, la persistencia: la referencia que un pronóstico de gobernanza debe superar

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo decidirá qué cuenta como un pronóstico en un historial, puntuará el pronóstico «nada cambia», expresará cualquier otro pronóstico como un índice de pericia (*skill score*) respecto a él y dirá cuándo ese índice no puede calcularse. **Pregunta de proyecto:** si un modelo predice la etiqueta de eficacia de mañana para cada artefacto de gobernanza, ¿qué exactitud alcanza ya «nada cambia» en la tendencia de calidad registrada?

[PSY-002](psy-002-governance-phase-transitions.es.md) considera que un cambio rápido en el equilibrio entre las etiquetas de valor de verdad es señal de que se avecina un cambio de régimen. Todo modelo que pronostique esas etiquetas debe compararse primero con el pronóstico más barato disponible; este módulo construye esa comparación para etiquetas categóricas. [PSY-016](psy-016-brier-score.es.md) puntúa pronósticos probabilísticos sobre los mismos pares, [PSY-006](psy-006-transition-matrix-from-counts.es.md) los convierte en una matriz de transición y [PSY-018](psy-018-backtesting-without-leakage.es.md) somete series numéricas a pruebas retrospectivas (*backtesting*).

## 1. Decidir qué es un pronóstico

**Observado.** Una [tarea programada diaria](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) ejecuta [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), al que el repositorio llama *feeder* (el «alimentador»). Lee un registro de evolución (un archivo JSON en `state/evolution/`) por cada *artefacto* de gobernanza (una política, una constitución, un esquema, una habilidad) y añade una fila por artefacto a `state/quality-trend/`. Todas las filas escritas en un mismo lanzamiento comparten un `timestamp`: eso es aquí una *ejecución*. El campo `effectiveness_to` de una fila es el valor de verdad que el registro atribuye en ese momento a una proposición escrita sobre el artefacto: T (verdadero), P (probable), U (desconocido), D (dudoso), F (falso) o C (contradictorio). Su `effectiveness_from` se [copia de la fila anterior del artefacto](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L104).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-005/extract.py) toma una instantánea de estos archivos en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-005/observed-input.json): **1,548** filas, **88** ejecuciones en **83** fechas UTC, **18** artefactos. La primera ejecución es de otra naturaleza. Sus 11 filas, con fecha 2026-05-01, llevan la marca `baseline: true`: son *filas semilla*, que registran un estado inicial. Las otras 87 son *ejecuciones del feeder*, del 2026-07-18 al 2026-10-13.

Las dos etiquetas están presentes en 1,540 filas. A siete filas les falta `effectiveness_from` porque no había ninguna etiqueta anterior que copiar. A una fila, la primera de `contracts / galactic-protocol.md`, le faltan las dos: el feeder escribe un `effectiveness_to` nulo cuando la evaluación de un registro es texto libre, que es lo que [contenía ese registro en aquel momento](https://github.com/GuitarAlchemist/Demerzel/blob/d9ddbaf9203a12b14c31b580070599efb8498031/state/evolution/2026-07-23-galactic-v1.3-ratification.evolution.json) (leído una sola vez en el commit `d9ddbaf`, fuera del *fixture*, es decir, de la carpeta de datos y scripts que reproduce las cifras de esta lección).

Un pronóstico necesita un momento de emisión y un momento posterior de verificación. Los datos admiten dos lecturas:

- **Dentro de la fila:** `effectiveness_from` frente a `effectiveness_to` en una misma fila, 1,540 pares.
- **Filas consecutivas:** el `effectiveness_to` de un artefacto en una fila frente al de su fila siguiente. Hay 1,548 − 18 = 1,530 pares de filas; 1 de ellos empieza en la fila sin etiqueta, lo que deja **1,529**.

Esta lección usa las filas consecutivas: cada par une dos etiquetas registradas en dos momentos distintos. El recuento dentro de la fila incluye además las 11 filas semilla, cuyos dos campos se escribieron a la vez y sin ninguna fila anterior detrás: no hubo un momento previo en el que se hubiera podido emitir un pronóstico, y las 11 coinciden por construcción. **Comprobación cruzada calculada:** fuera de las filas semilla, las dos lecturas dan los mismos 1,529 pares, y en ninguna fila `effectiveness_from` difiere del `effectiveness_to` de la fila anterior (0 discrepancias; `negative_controls` en [`results.json`](../../../fixtures/psychohistory/psy-005/results.json) muestra que una discrepancia introducida a propósito sí se cuenta).

### Ejercicio práctico 1

Partiendo de 1,548 filas y 18 artefactos, deduzca el número de pronósticos. Dedúzcalo de nuevo a partir de las 1,540 filas que llevan las dos etiquetas, y explique por qué 1,540 no es el recuento correcto.

> **Respuesta:** La primera fila de cada artefacto no tiene predecesora: `1,548 − 18 = 1,530` pares de filas. Uno empieza en la fila sin etiqueta: `1,530 − 1 = 1,529` pronósticos. Por el otro camino, `1,540 − 11 = 1,529` una vez retiradas las filas semilla. Contar 1,540 añadiría 11 pares sin ninguna ejecución anterior detrás, cada uno «correcto» solo porque sus dos campos se escribieron a la vez.

## 2. Puntuar el pronóstico que no predice nada nuevo

El *pronóstico de persistencia* dice que la próxima etiqueta será igual a la actual; no necesita ni modelo ni datos de entrenamiento. La *exactitud* es la proporción de pronósticos que coinciden con el resultado. La *tasa base de cambio* es la proporción de pares cuya etiqueta cambió.

```text
exactitud                    = pronósticos correctos / pronósticos
tasa base de cambio          = pares que cambiaron / pares
exactitud de la persistencia = 1 - tasa base de cambio
```

**Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-005/analyze.py) a partir de la instantánea (porcentajes redondeados a dos decimales):

| Pares | Recuento | Cambiaron | Exactitud de la persistencia |
|---|---|---|---|
| Todos los pares utilizables | 1,529 | 1 | 1,528/1,529 = 99.93% |
| De una fila semilla a la primera ejecución del feeder, 78.5 días | 11 | 1 | 10/11 = 90.91% |
| Entre ejecuciones del feeder separadas por menos de medio día | 72 | 0 | 100% |
| Entre ejecuciones del feeder separadas de 0.565 a 1.372 días | 1,433 | 0 | 100% |
| Entre ejecuciones del feeder separadas por 6.453 días | 13 | 0 | 100% |

La respuesta a la pregunta de proyecto es el 99.93% sobre todo lo registrado, y el 100% sobre los 1,433 pares cuyas dos filas distan alrededor de un día. La tasa base de cambio es 1/1,529 = 0.000654. El único cambio es de U a F, para `skills/demerzel-drive + policies/autonomous-loop-policy v1.1.0`; las etiquetas de los otros diecisiete artefactos no cambiaron nunca en lo registrado.

Importan tanto la unidad como la referencia. Puntuada por ejecución («ninguna etiqueta cambia en esta ejecución»), la persistencia acierta en 86 de las 87 ejecuciones objetivo, el 98.85%. Otro pronóstico barato, «siempre T» (el resultado más frecuente, elegido a posteriori), acierta en 775 de los 1,529 pares, el 50.69%. Un modelo tiene que superar al mejor pronóstico barato, no a cero ni al más débil.

### Ejercicio práctico 2

A partir de la tabla y del párrafo anterior, calcule la exactitud de la persistencia y la tasa base de cambio (a) sobre todos los pares utilizables y (b) sobre todos los pares entre ejecuciones del feeder. Calcule después la exactitud de «siempre T».

> **Respuesta:** (a) `1,528 / 1,529 = 0.999346`, es decir, el 99.93%; tasa base `1 / 1,529 = 0.000654`. (b) `72 + 1,433 + 13 = 1,518` pares y ningún cambio: exactitud del 100%, tasa base 0. «Siempre T»: `775 / 1,529 = 0.506867`, es decir, el 50.69%. Son recuentos sobre la instantánea fijada, no pronósticos de ejecuciones futuras.

## 3. Medir la pericia a partir de la referencia

Un *índice de pericia* sitúa una exactitud A en una escala en la que un pronóstico de referencia vale 0 y un pronóstico sin errores vale 1:

```text
pericia = (A - A_ref) / (1 - A_ref) = 1 - E / E_ref
```

E y E_ref cuentan los errores del pronóstico y de la referencia sobre los mismos pares. Una pericia negativa significa que el pronóstico lo hizo peor que la referencia.

Aquí la referencia es la persistencia, con E_ref = 1. La escala avanza, por tanto, en pasos enteros de 1: ningún error da 1, un error da 0, dos errores dan −1. No puede darse ningún valor entre 0 y 1.

**Sintético.** Los modelos siguientes no existen. [`scenarios.json`](../../../fixtures/psychohistory/psy-005/scenarios.json) define cada uno por cómo se habría comportado sobre los pares observados:

| Modelo imaginario | Comportamiento | Exactitud | Pericia |
|---|---|---|---|
| `echo` | devuelve la etiqueta anterior, sea cual sea su funcionamiento interno | 99.93% | 0 |
| `one_false_alarm` | como `echo`, más un cambio anunciado que no ocurrió | 99.87% | −1 |
| `one_right_call` | anuncia el único cambio y nada más | 100% | 1 |
| `cautious_alarm` | anuncia el único cambio y tres que no ocurrieron | 99.80% | −2 |

La primera fila es la clave de este módulo. Un modelo alcanza el 99.93% sin aprender nada más que «copiar la última etiqueta», de modo que una exactitud declarada cercana al 99.9% no informa en absoluto de si es capaz de anticipar un cambio. Solo la comparación con la persistencia lo hace, y aquí esa comparación descansa sobre un único par: `one_right_call` obtiene la puntuación máxima con un solo anuncio, que esta muestra no permite distinguir de un acierto por azar.

### Ejercicio práctico 3

Un proveedor informa de que su modelo acertó en 1,527 de los 1,529 pares. Indique su exactitud y su pericia frente a la persistencia. ¿Qué es lo que el informe sigue sin decir?

> **Respuesta:** Exactitud `1,527 / 1,529 = 0.998692`, es decir, el 99.87%. Cometió 2 errores donde la persistencia cometió 1: pericia `= 1 − 2/1 = −1`, peor que copiar la última etiqueta. El informe no dice qué errores fueron: el cambio omitido más una falsa alarma, el cambio anunciado correctamente más dos falsas alarmas, o el cambio anunciado con una etiqueta nueva equivocada más una falsa alarma.

## 4. Omisiones, falsas alarmas y la objeción más fuerte

La exactitud, y todo índice de pericia construido sobre ella, cuentan todos los errores por igual. Cuando los cambios son raros hay dos tipos de error: una *omisión* (un cambio que nadie anunció) y una *falsa alarma* (un cambio anunciado que no ocurrió). Un cambio anunciado con una etiqueta nueva equivocada también es un error. La persistencia nunca da una falsa alarma y omite todos los cambios. Si una omisión cuesta c veces lo que una falsa alarma, compare `c × misses + false alarms` (c × omisiones + falsas alarmas).

**Analogía (datos citados, no datos del proyecto).** En 1884, los pronósticos de tornados de J. P. Finley fueron correctos el 96.61% de las veces, sobre 2,803 pronósticos. No pronosticar nunca un tornado habría obtenido un 98.18%, y sin embargo Finley anunció 28 de los 51 tornados, y el 72% de sus alarmas fueron falsas ([tabla del JWGFVR](https://jwgfvr.github.io/forecastverification/); Murphy 1996). Cuál de los dos pronósticos era mejor depende de lo que cueste omitir un tornado.

### Ejercicio práctico 4

Sintético. `cautious_alarm` anuncia el único cambio y da tres falsas alarmas; la persistencia omite el cambio. ¿Para qué cociente de costos c es `cautious_alarm` el pronóstico más barato, y cuánto cuestan ambos con c = 10?

> **Respuesta:** La persistencia cuesta `c × 1 + 0 = c`; `cautious_alarm` cuesta `c × 0 + 3 = 3`. Empatan en `c = 3`; por encima de 3 la alarma es más barata, por debajo de 3 lo es la persistencia. Con `c = 10` los costos son 10 y 3. La alarma tiene la exactitud más baja (99.80% frente a 99.93%) y una pericia de −2, así que el criterio es el costo de cada tipo de error, no la exactitud. El modelo es imaginario: esto no dice nada sobre un pronosticador real.

**La objeción más fuerte a la lectura de esta lección** es que su único cambio no es un suceso a un día vista. Se sitúa en el paso de 78.5 días que va de una fila semilla a la primera ejecución del feeder, y el [registro de evolución](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution/2026-03-20-autonomous-driver.evolution.json) del artefacto fecha un evento `demoted` el 2026-07-18, el día de esa ejecución. Es una retirada que alguien decidió y dejó por escrito, no una deriva que el historial de etiquetas hubiera podido revelar. Entre ejecuciones del feeder nada cambió en 1,518 pares, de modo que ahí la persistencia no comete ningún error y la pericia queda indefinida (una división por cero): un modelo puede igualar los cero errores de la persistencia o cometer más, nunca menos. Además, las etiquetas son evaluaciones escritas que el feeder vuelve a leer; una etiqueta que no cambia puede significar tanto «nadie la reevaluó» como «sigue siendo eficaz». **Esta muestra no permite distinguir un sistema estable de un registro sin revisar, ni un modelo con pericia de la persistencia.** Dos cosas lo zanjarían: el historial de ediciones de los registros de evolución (con qué frecuencia se reexamina un valor de verdad, y con qué frecuencia cambia entonces) y un historial lo bastante largo como para contener varios cambios entre ejecuciones del feeder.

### Ejercicio práctico 5

Descarte los 11 pares que empiezan en una fila semilla. (a) ¿Cuál es la exactitud de la persistencia en el resto, y qué pericia puede demostrar ahí un modelo? (b) Suponga, solo para fijar una escala, que los cambios siguen produciéndose en 1 de cada 1,529 pares, sea cual sea el tiempo entre las dos filas, y que cada ejecución tiene 18 artefactos. ¿Al cabo de cuántas ejecuciones se esperan 10 cambios?

> **Respuesta:** (a) `1,529 − 11 = 1,518` pares, ninguno cambió: exactitud del 100%. E_ref vale 0, así que el índice de pericia queda indefinido; un modelo puede igualar a la persistencia sin cometer errores o quedar por debajo de ella. (b) `10 × 1,529 = 15,290` pares, y `15,290 / 18 = 849.4`, es decir, 850 ejecuciones, frente a las 87 ejecuciones del feeder registradas hasta ahora. El supuesto descansa sobre un único cambio observado, y ese cambio está en un par de 78.5 días, no en uno diario: 850 es un orden de magnitud, no un calendario.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los archivos de la tendencia de calidad de [mayo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-05.jsonl), [julio](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-07.jsonl), [agosto](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-08.jsonl), [septiembre](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-09.jsonl) y [octubre](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl) de 2026 (no hay archivo de junio), el script del feeder y el registro de evolución enlazados más arriba. `extract.py` se niega a ejecutarse si alguno de estos archivos difiere de su blob de Git fijado.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-005/extract.py`, y después `analyze.py` en la misma carpeta; `analyze.py --check` compara una ejecución nueva con los resultados guardados. El [README](../../../fixtures/psychohistory/psy-005/README.md) enumera todos los archivos, las autocomprobaciones y los controles negativos.

**Referencias de método.** Hyndman, R. J., y Athanasopoulos, G. (2021), *Forecasting: Principles and Practice*, tercera edición, OTexts, [sección 5.2](https://otexts.com/fpp3/simple-methods.html) (el pronóstico ingenuo, que es la persistencia para series numéricas). Jolliffe, I. T., y Stephenson, D. B., editores (2012), *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, segunda edición, Wiley (exactitud e índices de pericia). Murphy, A. H. (1996), «The Finley Affair: A Signal Event in the History of Forecast Verification», *Weather and Forecasting* 11, 3–20. Murphy, A. H. (1993), «What Is a Good Forecast? An Essay on the Nature of Goodness in Weather Forecasting», *Weather and Forecasting* 8, 281–293 (la calidad de un pronóstico frente a su valor para un usuario).

**No realizado.** No se entrenó ni se ejecutó ningún modelo de pronóstico; los cuatro modelos son imaginarios. No se dio ningún intervalo para la tasa base (PSY-006 trata las transiciones observadas rara vez o nunca) ni se puntuó ningún pronóstico probabilístico (PSY-016). No se leyó el historial de ediciones de los registros de evolución. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Contar, en el historial de Git de `state/evolution/`, con qué frecuencia se reexaminó cada valor de verdad y con qué frecuencia cambió. Si las etiquetas casi nunca se reexaminan, la conclusión pasa de «esta muestra no permite distinguir un modelo con pericia de la persistencia» a «esta etiqueta no es un observable diario», y la pregunta de pronóstico debería trasladarse a una magnitud medida en cada ejecución.
