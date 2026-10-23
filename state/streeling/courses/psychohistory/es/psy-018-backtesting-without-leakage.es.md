---
module_id: psy-018-backtesting-without-leakage
department: psychohistory
course: "Pruebas retrospectivas sin fuga de datos"
level: intermediate
prerequisites: ["psy-005-persistence-baseline"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-018
version: "0.1.0"
---

# Pruebas retrospectivas sin fuga de datos

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

Una *prueba retrospectiva* (*backtesting*) puntúa un método de pronóstico con datos que ya existen, como si cada valor no hubiera llegado todavía. En este módulo decidirá qué es un pronóstico en un registro irregular, desplazará el origen a lo largo de él, puntuará tres métodos sencillos y reconocerá tres maneras en que un valor posterior entra en un pronóstico anterior. **Pregunta de proyecto:** ¿cómo se pone a prueba un pronóstico del recuento de citas de un artefacto sin dejar que el futuro se filtre en la prueba?

[PSY-005](psy-005-persistence-baseline.es.md) puntuó «nada cambia» sobre etiquetas. Una serie numérica añade errores que tienen un tamaño, y estadísticos que hay que ajustar, que es por donde entran las fugas. [PSY-011](psy-011-measurement-change-or-system-change.es.md) estudia el cambio de instrumento que aquí se deja de lado; [PSY-004](psy-004-how-large-is-large.es.md) explica por qué unas observaciones que comparten una causa cuentan como menos observaciones.

## 1. Qué hay que pronosticar

**Observado.** En cada *ejecución*, el *feeder* (el «alimentador») [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py) añade una fila por cada *artefacto* de gobernanza (una política, una habilidad) a [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend). `citation_count` está pensado como [el número de archivos rastreados que mencionan el artefacto](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15); las lecciones también cuentan, de ahí las barras espaciadas de más abajo. `delta_citations` es, según la [línea 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), el recuento menos el de la fila anterior, o 0 en una fila marcada `rebaseline`.

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-018/extract.py) toma una instantánea de estos archivos en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-018/observed-input.json): **1,548** filas, **88** ejecuciones, **18** artefactos. Las 11 filas de la primera ejecución son filas semilla sin recuento, lo que deja 1,537 filas con recuento y 1,537 − 18 = 1,519 *pares de filas consecutivas* de un mismo artefacto.

El recuento difiere en **20** pares: 16 terminan el 2026-09-13 y 4 el 2026-10-03. Hasta la primera fecha, los recuentos se [introducían a mano y nunca se actualizaban](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8); en la ejecución del 2026-09-13T17:52:14Z, un recuento de `git grep` los sustituyó en 16 artefactos (`policies / alignment-policy.yaml` pasó de 3 a 42) y el feeder marcó esas filas con `rebaseline: true`. El *instrumento*, el procedimiento que produce el número, había cambiado. Este módulo reinicia cada serie en una fila de *rebaseline*: una *serie* es un artefacto bajo un mismo instrumento. Eso da **34** series (16 anteriores a una fila de rebaseline, 16 que empiezan en una, 2 artefactos que nunca se volvieron a medir) y 1,519 − 16 = 1,503 pares dentro de una serie.

Dentro de las series cambian **4** pares, en 4 artefactos: todos en la ejecución del 2026-10-03T15:31:16Z, todos en +2 (de 42 a 44, de 43 a 45, y de 27 a 29 dos veces). Las otras 30 series no varían nunca.

- **Dos conjuntos de veinte.** 20 filas llevan un `delta_citations` distinto de cero y 20 filas difieren del recuento de la fila anterior, pero solo 4 filas están en los dos conjuntos: dieciséis deltas distintos de cero están en la primera fila con recuento de un artefacto, donde el feeder resta 0, y las 16 filas de rebaseline cambiaron mientras su delta se escribía como 0. Este módulo cuenta cambios de valor.
- **Una ejecución no es un día.** Entre ejecuciones consecutivas del feeder pasan de 0.001 a 6.453 días: «un paso adelante» significa una ejecución adelante.

### Ejercicio práctico 1

Un pronóstico necesita dos filas anteriores de su serie. Partiendo de 1,548 filas, deduzca el número de pronósticos que ofrecen las 34 series. ¿Qué filas tienen un delta distinto de cero aunque su recuento no cambió?

> **Respuesta:** `1,548 − 11 = 1,537` filas con recuento; `1,537 − 18 = 1,519` pares; `1,519 − 16 = 1,503` pares dentro de una serie; el primer par de cada serie solo tiene una fila anterior, así que `1,503 − 34 = 1,469` pronósticos. Las `20 − 4 = 16` filas son primeras filas con recuento, 12 el 2026-07-18 y 4 el 2026-07-29: su delta es el propio recuento.

## 2. Desplazar el origen

Un pronóstico tiene un *origen*, la última fila que puede usar, y un *objetivo*, la fila que predice. Una *partición temporal* sitúa todas las filas de entrenamiento antes de todas las filas de prueba. Un *origen móvil* repite la partición: cada fila, por turno, es el objetivo, y se pronostica solo a partir de las filas anteriores a ella ([Hyndman y Athanasopoulos, sección 5.10](https://otexts.com/fpp3/toolbox.html#sec-tscv); Tashman 2000). Tres métodos, para una serie y_1 … y_t conocida en el origen t:

```text
persistencia (ingenua)    pronóstico = y_t
media acumulada           pronóstico = (y_1 + ... + y_t) / t
deriva                    pronóstico = y_t + (y_t - y_1) / (t - 1)

error = real - pronóstico          MAE (error absoluto medio) = media de |error|
MAE relativo = MAE / MAE de la persistencia, sobre los mismos pronósticos
```

**Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-018/analyze.py) y guardado en [`results.json`](../../../fixtures/psychohistory/psy-018/results.json), redondeado a 6 decimales:

| Método | Error absoluto total (1,469 pronósticos) | MAE, una serie que varía (30 pronósticos) | MAE relativo |
|---|---|---|---|
| persistencia | 8 | 0.066667 | 1 |
| deriva | 11.177980 | 0.093150 | 1.397247 |
| media acumulada | 72.156930 | 0.601308 | 9.019616 |

La persistencia yerra por 2 en cada uno de los cuatro escalones. Los otros dos métodos cometen esos mismos errores y siguen pagando: la media va por detrás del nuevo nivel durante diez filas más, y la deriva extrapola una subida que ocurrió una sola vez. Todos estos errores están entre los 480 pronósticos sobre recuentos de `git grep`; los 819 sobre recuentos introducidos a mano y los 170 sobre los dos artefactos que nunca se volvieron a medir releen un número que nadie actualizó. Ahí todos los métodos son exactos, y el MAE relativo de las 30 series planas es 0/0.

Un *error escalado* (Hyndman y Koehler 2006) divide cada error por el MAE del pronóstico ingenuo dentro de las filas de entrenamiento:

```text
escala en el origen t = (|y_2 - y_1| + ... + |y_t - y_(t-1)|) / (t - 1)
error escalado        = |error| / escala
```

Aquí la escala vale 0 hasta que una serie ha cambiado: solo 40 de los 1,469 pronósticos tienen una escala positiva, ninguno en una serie plana, y los cuatro errores de la persistencia caen en orígenes donde todavía vale 0. Sobre esos 40, la persistencia obtiene 0 y la deriva 1: una vez que cada serie se reinicia en su fila de rebaseline, la puntuación solo existe donde ya no queda nada que medir.

### Ejercicio práctico 2

`policies / alignment-policy.yaml` marca 42 durante 21 filas y después 44 durante 11 filas. Calcule los tres pronósticos de la fila 23 (origen: fila 22) y sus errores y, después, el MAE de la persistencia sobre los 30 pronósticos de esta serie.

> **Respuesta:** Persistencia: 44, error 0. Media acumulada: `(21 × 42 + 44) / 22 = 42.090909`, error 1.909091. Deriva: `44 + (44 − 42) / 21 = 44.095238`, error −0.095238. La persistencia yerra una sola vez, por 2, en la fila 22: MAE `2 / 30 = 0.066667`.

### Ejercicio práctico 3

La misma serie. Dé la escala en los orígenes 21 y 22 y, después, el error escalado de cada método para la fila 23. ¿Cuál es el error escalado de los pronósticos de la fila 22?

> **Respuesta:** En el origen 21 todas las filas marcan 42: escala 0. En el origen 22, un cambio de 2 en 21 pares: `2 / 21 = 0.095238`. Fila 23: persistencia 0, media acumulada `(42 / 22) / (2 / 21) = 20.045455`, deriva `(2 / 21) / (2 / 21) = 1`. En la fila 22, la del escalón, todos los métodos yerran por 2 sobre una escala de 0: indefinido.

## 3. Tres maneras en que entra el futuro

Una prueba retrospectiva **tiene una fuga** cuando un pronóstico usa una entrada que aún no estaba registrada en su origen: el objetivo, una fila posterior o un número derivado de ellos (una media, una escala, un parámetro ajustado), incluidas las filas posteriores que una partición aleatoria coloca entre las filas de entrenamiento (siguiendo a Kaufman et al. 2012). Una sola pregunta pone a prueba cualquier número de una cadena de procesamiento: *¿podría haberse anotado en el origen?* Un error emparentado no cambia ningún pronóstico, pero sesga la puntuación: elegir los objetivos con información posterior, una *selección a posteriori*. Elegir un método a partir de las filas de prueba es la reutilización del conjunto de prueba que trata [PSY-013](psy-013-four-scores-and-a-trend.es.md).

La persistencia no ajusta nada, así que dos de las tres fugas no pueden alcanzarla; alcanzan a cualquier método que ajuste un estadístico. El más sencillo es un *nivel*: la media de las filas de entrenamiento, usada como pronóstico de todas las filas de prueba. **Calculado:** tome una serie que varía (32 filas; las cuatro dan cifras idénticas) y haga la prueba sobre su último cuarto, una elección guardada en [`scenarios.json`](../../../fixtures/psychohistory/psy-018/scenarios.json).

| Prueba del nivel ajustado | MAE en las 8 filas de prueba | Cambio |
|---|---|---|
| Partición temporal: nivel a partir de las filas 1 a 24 | 1.75 | referencia |
| Fuga 1: nivel calculado sobre las 32 filas, incluidas las de prueba | 1.3125 | −25% |
| Fuga 3: 8 filas de prueba extraídas al azar, nivel a partir de las otras 24, con filas posteriores entre ellas | 0.931452 | −46.77% |

La tercera cifra es la media exacta sobre las 10,518,300 maneras de extraer las filas de prueba; solo 165 dan un error tan grande como el de la partición temporal.

**La fuga 2** es una variable predictora que codifica el objetivo: pronosticar «recuento anterior + `delta_citations` de la fila objetivo». Con el origen móvil no comete ningún error en 1,469 pronósticos, donde la persistencia yerra cuatro veces: −100%.

Las fugas 1 y 3 no siempre hacen parecer mejor el resultado. En los 30 cortes que dejan al menos dos filas de entrenamiento, la fuga 1 reduce el error en 21 cortes (hasta un 34.38%), lo deja igual en 1 y lo aumenta en 8 (hasta un 25%); la fuga 3 lo reduce en 23 y lo aumenta en 7. Con el origen móvil, la media de toda la serie obtiene 0.916667, frente a 0.601308 de la media acumulada, un 52.45% peor, porque la media honesta es exacta mientras la serie es plana. Una fuga hace que la puntuación sea errónea, en un sentido que depende de dónde cae el cambio entre las filas de prueba.

### Ejercicio práctico 4

Con la pregunta «¿podría haberse anotado en el origen?», clasifique como fuga, selección a posteriori o ninguna de las dos: (a) una escala calculada sobre toda la serie; (b) una prueba solo sobre «los artefactos que varían»; (c) el `delta_citations` de la fila de origen. Calcule después el pronóstico de la fuga 2 para `constitutions / asimov.constitution.md` en su fila de rebaseline: recuento anterior 5, `delta_citations` 0, valor real 65.

> **Respuesta:** (a) Fuga: la escala contiene filas posteriores; haría que todos los errores escalados de una serie que varía estuvieran definidos (persistencia 1.033333). (b) Selección a posteriori: no cambia ningún pronóstico, pero qué artefactos varían solo se sabe al final del registro; los 1,469 pronósticos agrupados evitan esa elección. (c) Ninguna de las dos: ese delta se registró en el origen. Pronóstico `5 + 0 = 5`, error 60. La variable con fuga falla donde el feeder escribió 0: sobre los 1,519 pares, yerra en las 16 filas de rebaseline, con un error absoluto total de 306.

## 4. Lo que esta prueba retrospectiva puede mostrar

**Cuatro series, un suceso.** Los cuatro cambios comparten una ejecución y un tamaño; las cuatro series comparten un mismo perfil de errores, así que los cocientes de la sección 2 se repiten por construcción. De 85 ejecuciones objetivo, una concentra todos los errores de la persistencia. Leído fuera del *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección), el historial es compatible con una sola causa: entre las dos ejecuciones, el commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642) añadió 26 lecciones traducidas, seis de las cuales escriben las rutas de estos artefactos, dos por artefacto. Pronosticar este recuento es pronosticar lo que se escribe en el repositorio, lecciones incluidas. «La persistencia superó a la deriva en 4 de 4 series» suena a cuatro lanzamientos de moneda (una analogía), con una probabilidad de 1/16; con un solo suceso es un solo lanzamiento, 1/2.

**La objeción más fuerte a esta lección** es que su propia prueba depende de un valor posterior. La marca `rebaseline` está en la fila objetivo: en el origen del 2026-09-13T15:24:53Z nadie podía saber que la ejecución siguiente, 0.102 días más tarde, cambiaría el instrumento. Reiniciar ahí las series es una selección a posteriori: elimina 16 objetivos usando información posterior. Sin el reinicio, el error absoluto total de la persistencia es 314 en lugar de 8, y 306 de ellos (el 97.45%) están en las filas de rebaseline. Las dos cifras responden a preguntas distintas, «¿qué dirá el archivo?» y «¿qué marcará este instrumento?»; un informe debe decir cuál de las dos da.

**Esta muestra no permite distinguir** un proceso por escalones de una tendencia lenta, ni ordenar los métodos más allá de un paso: con un instrumento fijo contiene un suceso en 31 pasos de una ejecución a la siguiente. Muestra algo más acotado: la contabilidad de una prueba movió el error informado, de −100% a +52.45% a través de las tres fugas, y de 8 a 314 a través de la elección de los objetivos. Solo un registro más largo permitiría zanjar algo más.

### Ejercicio práctico 5

(a) ¿Por qué 1/16 es la probabilidad equivocada para «4 de 4»? (b) Suponga, solo para fijar una escala, que las ejecuciones con un cambio siguen llegando a razón de una cada 31 pasos de una ejecución a la siguiente. ¿Al cabo de cuántas ejecuciones se esperan 10 ejecuciones así, frente a las 32 registradas desde el rebaseline?

> **Respuesta:** (a) `(1/2)^4 = 1/16` exige cuatro comparaciones independientes; los cuatro escalones comparten una ejecución y un tamaño: un suceso, probabilidad `1/2`. (b) `10 × 31 = 310` pasos, es decir, 311 ejecuciones, unas diez veces las 32 registradas. La tasa descansa sobre una sola ejecución con cambio: un orden de magnitud, no un calendario.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cinco archivos JSONL de `state/quality-trend/` y los dos scripts enlazados más arriba.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-018/extract.py`, después `analyze.py` y después `analyze.py --check`; el [README](../../../fixtures/psychohistory/psy-018/README.md) enumera las 35 autocomprobaciones, las formas cerradas y los controles negativos.

**Referencias de método.** Hyndman, R. J., y Koehler, A. B. (2006), «Another look at measures of forecast accuracy», *International Journal of Forecasting* 22(4), 679–688. Tashman, L. J. (2000), «Out-of-sample tests of forecasting accuracy: an analysis and review», *International Journal of Forecasting* 16(4), 437–450. Kaufman, S., Rosset, S., Perlich, C., y Stitelman, O. (2012), «Leakage in data mining: Formulation, detection, and avoidance», *ACM Transactions on Knowledge Discovery from Data* 6(4), 1–21. Hyndman, R. J., y Athanasopoulos, G. (2021), *Forecasting: Principles and Practice*, tercera edición, OTexts, secciones 5.2, [5.8](https://otexts.com/fpp3/toolbox.html#sec-accuracy), 5.10.

**No realizado.** No se ajustó ningún modelo aparte de los tres métodos de referencia. No se modelizó el tiempo irregular entre un origen y su objetivo (de 0.001 a 6.453 días). El historial se leyó a mano, fuera del fixture. Ningún humano ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Volver a ejecutar el fixture cuando el registro contenga varias ejecuciones con cambio, de causas distintas, bajo un mismo instrumento: un método que entonces superase a la persistencia convertiría «no permite ordenar» en una clasificación con una incertidumbre declarada.
