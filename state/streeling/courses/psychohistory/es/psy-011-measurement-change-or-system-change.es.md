---
module_id: psy-011-measurement-change-or-system-change
department: psychohistory
course: "¿Cambio de medición o cambio de sistema? Los rebaselines en la tendencia de calidad"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-005-persistence-baseline"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-011
version: "0.1.0"
---

# ¿Cambio de medición o cambio de sistema? Los rebaselines en la tendencia de calidad

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

Leerá cómo se produce un número antes de leer su serie, encontrará un cambio de instrumento en un registro, clasificará cada salto en «empieza la medición», «cambia el instrumento» o «mismo instrumento», y mostrará qué hace una regla de alarma cuando los tres están mezclados. **Pregunta de proyecto:** la tendencia de calidad tiene filas marcadas con `rebaseline` y un campo `citation_source` que aparece a mitad de camino; ¿cuáles de los saltos de la serie son el instrumento cambiando y no el sistema?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lee un cambio rápido en un indicador de gobernanza como indicio de un cambio de régimen próximo. Esa lectura supone que el indicador se producía de la misma manera antes y después; este módulo pone a prueba el supuesto sobre la columna de citas del registro que presentó [PSY-005](psy-005-persistence-baseline.es.md). [PSY-012](psy-012-early-warning-false-alarms.es.md) trata los indicadores de alerta temprana.

## 1. Leer el instrumento antes que la serie

Un *instrumento* es todo el procedimiento que convierte el mundo en un número registrado: quién o qué cuenta, qué se cuenta y dónde. Un *cambio de sistema* es un cambio en la cosa contada.

**Observado, en el código fijado.** Una [tarea diaria](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) ejecuta el *feeder* (el «alimentador»), [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), que añade una fila por cada *artefacto* de gobernanza (una política, un esquema, una habilidad) a `state/quality-trend/`; un lanzamiento es una *ejecución*. El `citation_count` de una fila se [copia del registro de evolución del artefacto](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L75-L76), un archivo JSON de `state/evolution/`. Desde septiembre de 2026 un segundo script, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), calcula ese número como los ["tracked files that mention any of the artifact's citation paths (`git grep -lF`)"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) y [marca el registro](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L104-L107) con `citation_source: "git-grep-v1"`. Antes de eso, dice su docstring, cada métrica ["was typed by hand"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8) y «nothing updated it afterwards».

El feeder reacciona a la marca en las [líneas 90 a 92](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L90-L92) y en la [línea 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), donde `prev` es la fila anterior del artefacto:

```text
prev = previous.get(artifact, {})
source = metrics.get("citation_source")
rebaseline = bool(prev) and prev.get("citation_source") != source
"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),
```

De ahí se siguen tres cosas:

1. Se declara un *rebaseline* (un reanclaje de la base) cuando existe una fila anterior y su etiqueta de origen difiere de la actual; una clave ausente se lee como nula.
2. El cambio registrado, `delta_citations`, vale entonces 0, mientras que [`citation_count` se escribe tal como se leyó](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L96): el salto se queda en `citation_count`.
3. Sin fila anterior, o con una sin recuento, el feeder resta 0: el «cambio» es el recuento entero.

La docstring del feeder da la intención: ["the jump is a change of measurement, not a change in citations"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L14-L18).

**Calculado.** [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/analyze.py) reimplementa esta regla sobre la instantánea que toma [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/extract.py). Reproduce `delta_citations` en las 1,537 filas que tienen recuento y en las 576 marcas registradas, con 0 discrepancias.

### Ejercicio práctico 1

Filas **sintéticas** de [`scenarios.json`](../../../fixtures/psychohistory/psy-011/scenarios.json). Dé la marca y el `delta_citations` que escribe la regla: (a) la primera fila de un artefacto, recuento 9; (b) fila anterior 12 sin origen, ahora 27 desde `git-grep-v1`; (c) fila anterior 6 y ahora 19, ambas `git-grep-v1`, después de que alguien añadiera una ruta a los `citation_paths` del registro. ¿Cuál de los casos es un cambio de instrumento que la regla no puede ver?

> **Respuesta:** (a) Ninguna fila anterior: sin marca, delta 9, un inicio de medición registrado como una subida. (b) Marca, delta 0; el escalón de 15 solo sobrevive en `citation_count`. (c) Sin marca, delta 13, el caso que la regla no puede ver: la lista de rutas forma parte del instrumento, pero la etiqueta no cambió, así que la edición queda registrada como 13 citas nuevas.

## 2. Localizar el cambio en el registro

**Observado** en [`observed-input.json`](../../../fixtures/psychohistory/psy-011/observed-input.json): 1,548 filas en 88 ejecuciones para 18 artefactos. La primera ejecución, fechada el 2026-05-01, tiene 11 *filas semilla* sin recuento; siguen 87 ejecuciones del feeder. La clave `citation_source` está ausente de las 56 primeras ejecuciones (972 filas) y presente en las 32 últimas. Aparece por primera vez el 2026-09-13T17:52:14Z, donde 16 filas llevan `git-grep-v1` y `rebaseline: true`. Las otras 2 filas tienen origen nulo y ninguna marca: sus artefactos tienen una lista `citation_paths` vacía, que [señala un artefacto fuera del repositorio](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23), y conservan sus 55 y 0 escritos a mano. Ninguna otra fila está marcada.

**Calculado.** Cada uno de los 16 artefactos tenía un valor escrito a mano en todas sus filas anteriores. Esa ejecución lo reemplazó:

| Artefacto (barras separadas) | Escrito a mano | `git grep` |
|---|---|---|
| `constitutions / asimov.constitution.md` | 5 | 65 |
| `contracts / galactic-protocol.md` | 2 | 43 |
| `policies / alignment-policy.yaml` | 3 | 42 |
| `constitutions / default.constitution.md` | 11 | 47 |
| `skills / demerzel-drive + policies / autonomous-loop-policy v1.1.0` | 1 | 27 |
| `logic / tetravalent-state.schema.json` | 4 | 23 |
| `logic / governance-evolution.schema.json` | 2 | 17 |
| `policies / autonomous-loop-policy.yaml` | 12 | 27 |
| `afk-graduated-self-merge` | 1 | 14 |
| `schemas / loop-state.schema.json` | 3 | 15 |
| `logic / kaizen-pdca-state.schema.json` | 3 | 13 |
| `scripts / afk_backends /` | 0 | 6 |
| `ml-feedback-loop` | 1 | 6 |
| `meta / compounding-cycle` | 4 | 5 |
| `docs / governance / the-sentinel-spec.md` | 1 | 0 |
| `docs / governance / harness-engineering-direction.md` | 8 | 1 |

Los escalones van de −7 a +60 y la razón entre el valor nuevo y el antiguo de 0 a 27 (indefinida para un valor antiguo de 0): ningún factor de conversión único une los dos instrumentos.

### Ejercicio práctico 2

A partir de la tabla, calcule la suma de los 16 recuentos antes y después, y el escalón. Añada los dos artefactos sin marca para obtener el total de los 18 y su razón. ¿Cuántos recuentos bajaron? ¿Cuánto sumó `delta_citations` en esa ejecución?

> **Respuesta:** Antes `61`, después `351`, escalón `351 − 61 = 290`. Sobre los 18 artefactos: `61 + 55 + 0 = 116` antes y `351 + 55 + 0 = 406` después, una razón de `406 / 116 = 3.5`. Dos recuentos bajaron (de 8 a 1 y de 1 a 0). Las filas marcadas tienen delta 0 y las otras dos no se movieron, así que `delta_citations` suma 0 en la ejecución en la que el total creció en 290.

## 3. Clasificar cada salto

«Filas con un `delta_citations` distinto de cero» y «filas cuyo recuento difiere del de la fila anterior» suenan como un mismo conjunto. Cada uno tiene 20 filas; solo 4 están en los dos. Clasificar cada fila frente a la fila anterior del artefacto muestra por qué (**calculado**, [`results.json`](../../../fixtures/psychohistory/psy-011/results.json)):

| Clase de fila | Filas | Recuento cambiado | Delta no nulo |
|---|---|---|---|
| Primer recuento: ningún recuento anterior con el que comparar | 18 | indefinido | 16 |
| Cambio de instrumento: la fila anterior tiene otro origen | 16 | 16 | 0 |
| Mismo instrumento: la fila anterior tiene el mismo origen | 1,503 | 4 | 4 |

Los 16 deltas no nulos de la primera clase son niveles, no cambios: 10 siguen a una fila semilla, 6 son la primera fila de un artefacto, y suman 116. Quedan 4 filas, todas en la ejecución del 2026-10-03T15:31:16Z, cada una con un escalón de +2.

De los 1,503 pares de filas consecutivas de un mismo artefacto con el mismo instrumento, 1,007 no tienen origen en ninguna de las dos filas (el periodo de escritura a mano y los dos artefactos externos) y tienen 0 cambios. Un número que nadie vuelve a teclear no puede moverse, así que este cero dice que el instrumento estaba callado, no que el sistema estuviera quieto. Bajo `git-grep-v1`: 496 pares, y los 4 cambios.

La misma división se aplica a la suma sobre los artefactos, que creció de 106 en la primera ejecución del feeder a 414 en la última: `308 = 10 + 290 + 8`, es decir, primeros recuentos de artefactos añadidos más tarde, el cambio de instrumento y los escalones con el mismo instrumento. Solo el último es *comparable de igual a igual*: mismo instrumento, mismo conjunto de artefactos.

### Ejercicio práctico 3

Partiendo de 1,548 filas y 18 artefactos, deduzca el número de pares con el mismo instrumento y la proporción de los que cambiaron. Dé después la proporción del crecimiento del total que se midió de igual a igual.

> **Respuesta:** `1,548 − 18 = 1,530` pares de filas. Quite los 11 que empiezan en una fila semilla y los 16 que cruzan el cambio de origen: `1,530 − 11 − 16 = 1,503`. Cambiados: `4 / 1,503 = 0.27%`. Crecimiento: `8 / 308 = 2.60%`; el resto es un instrumento nuevo (290) o artefactos nuevos (10).

## 4. Fijar la medición antes de leer un cambio de régimen

La primera señal de PSY-002 es una tasa de cambio «exceeding 2 standard deviations from its running mean», enunciada para su índice de cristalización, no para las citas. Como **decisión de análisis** guardada en `scenarios.json`, apliquemos una regla de esa forma al escalón de una ejecución a la siguiente del recuento de citas sumado sobre los artefactos: marcar un escalón que se aparte de la media de todos los escalones anteriores (al menos 3) en más de 2 de sus desviaciones típicas poblacionales. Las ejecuciones del feeder están separadas de 122 segundos a 6.45 días; la misma regla sobre los escalones por día marca las mismas ejecuciones. **Calculado** sobre tres versiones de la serie:

| Serie | Escalones marcados | El +8 del 2026-10-03 |
|---|---|---|
| `citation_count` sumado | +2 y +8 el 2026-07-29, +290 el 2026-09-13 | sin marcar |
| `delta_citations` sumado | +2 y +8 el 2026-07-29 | marcado |
| Solo escalones con el mismo instrumento | ninguno anterior | marcado |

Sobre la suma bruta la regla levanta tres alarmas y ninguna es un cambio de igual a igual: dos son artefactos que entran en la suma y una es el instrumento nuevo. Esa última también infla la desviación típica móvil, así que el único escalón comparable de igual a igual pasa sin verse. Conservando todos los escalones anteriores, un cambio de instrumento cuesta dos veces: una falsa alarma cuando ocurre y ceguera después. Cuidado con la última fila: tras un historial todo a cero, cualquier escalón no nulo queda marcado.

### Ejercicio práctico 4

En la ejecución del 2026-10-03 los 75 escalones anteriores tienen media 4 y desviación típica 33.2602 en la suma bruta, y media 0.1333 y desviación típica 0.9428 en el `delta_citations` sumado. Para cada serie, calcule el borde superior de la banda (la media más 2 desviaciones típicas) y el menor escalón entero que quedaría marcado.

> **Respuesta:** Suma bruta: `4 + 2 × 33.2602 = 70.5204`, así que +8 queda dentro de la banda y el menor escalón marcado es 71. Deltas sumados: `0.1333 + 2 × 0.9428 = 2.0189`, así que +8 queda marcado y el menor escalón marcado es 3. Un solo cambio de instrumento movió el umbral de detección de 3 a 71.

**La objeción más fuerte a esta lectura** es que «mismo instrumento» descansa en una etiqueta, y el ejercicio 1(c) muestra un cambio de instrumento que conserva su etiqueta: los cuatro escalones restantes podrían ser un cambio así. El fixture responde: los cuatro registros de evolución comparten un mismo instante `last_cited`, 2026-10-02T20:05:16Z, situado entre la ejecución anterior y la del escalón, y dos de los cuatro artefactos miden la misma ruta: cuatro filas, como máximo tres recuentos independientes. Leído fuera del fixture, en el historial de Git hasta la fijación: el script productor tiene un solo commit y, entre las dos ejecuciones, solo el commit de la propia tarea diaria tocó `state/evolution/`, así que nadie editó el código ni una lista de rutas; el commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642), hecho en ese mismo instante, añadió las traducciones al francés y al español de 13 módulos de curso; y, para cada ruta de cita de los cuatro artefactos, exactamente dos archivos añadidos entre las dos ejecuciones la citan en la fijación, las dos traducciones de una misma lección. Eso es compatible con un cambio en la cosa contada, y pequeño: se tradujeron tres lecciones.

### Ejercicio práctico 5

Un panel informa de que «las citas se han multiplicado por unas 3.9 desde julio (de 106 a 414)» como prueba de un cambio de régimen. Acepte o rechace, enuncie su criterio y nombre dos registros que harían legible un cambio futuro.

> **Respuesta:** Rechazar. Criterio: dos recuentos solo pueden compararse si el mismo instrumento produjo ambos, para el mismo conjunto de artefactos. De los 308, 290 vienen de un instrumento nuevo y 10 de artefactos añadidos a la suma; 8 cumplen el criterio, todos en una sola ejecución. Dos registros útiles: una etiqueta de origen que cambie en cuanto cambie el script, su lista de exclusiones o una lista `citation_paths`; y, en cada cambio, los dos instrumentos ejecutados en paralelo durante varias ejecuciones, para que el solape mida la diferencia.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cinco archivos JSONL de [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), los dos scripts enlazados más arriba y los 18 registros `*.evolution.json` de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution). El [README](../../../fixtures/psychohistory/psy-011/README.md) del fixture da los comandos, las autocomprobaciones y los controles negativos.

**Referencias de método.** Shadish, W. R., Cook, T. D., y Campbell, D. T. (2002), *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Houghton Mifflin (la *instrumentación* como amenaza a la validez).

**No realizado.** El recuento de `git grep` no se volvió a calcular para las ejecuciones anteriores al 2026-09-13, así que nada de lo aquí dicho afirma si las citas se movieron entonces. No se leyeron las versiones anteriores del feeder. Las afirmaciones sacadas del historial de Git descansan en comandos enumerados en la nota de revisión, no en el fixture. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Volver a calcular el recuento `git-grep-v1` en el commit de cada ejecución anterior. Un solo instrumento bajo las 87 ejecuciones del feeder mostraría si algo se movió antes de septiembre; si se movió, la conclusión pasa de «casi nada se movió» a «el movimiento no se midió».

**Huella propia.** Este módulo escribe los nombres de artefacto como etiquetas con las barras separadas, de modo que ninguno de sus archivos contiene la ruta de cita de ningún artefacto: ejecutada sobre ellos con cada una de las rutas, la búsqueda literal de la sección 1 (`git grep -lF`) no encuentra nada. PSY-020 retoma la cuestión general.
