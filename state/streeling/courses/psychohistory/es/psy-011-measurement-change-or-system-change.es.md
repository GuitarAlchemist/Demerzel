---
module_id: psy-011-measurement-change-or-system-change
department: psychohistory
course: "¿Cambio de medición o cambio del sistema? Las nuevas líneas de base de la tendencia de calidad"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-005-persistence-baseline"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-011
version: "0.1.0"
---

# ¿Cambio de medición o cambio del sistema? Las nuevas líneas de base de la tendencia de calidad

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo leerá cómo se produce un número antes de leer su serie, localizará un cambio de instrumento en un registro, clasificará cada salto como «empieza la medición», «cambia el instrumento» o «mismo instrumento» y mostrará qué hace una regla de alarma cuando se mezclan los tres. **Pregunta de proyecto:** la tendencia de calidad tiene filas marcadas con `rebaseline` y un campo `citation_source` que solo aparece a partir de cierto momento; ¿qué saltos de la serie se deben a que cambia el instrumento, y no el sistema?

[PSY-002](psy-002-governance-phase-transitions.es.md) interpreta un cambio rápido en un indicador de gobernanza como señal de que se avecina un cambio de régimen. Esa lectura supone que el indicador se produjo de la misma manera antes y después; este módulo pone a prueba ese supuesto en la columna de citas del registro que presentó [PSY-005](psy-005-persistence-baseline.es.md). [PSY-012](psy-012-early-warning-false-alarms.es.md) trata los indicadores de alerta temprana.

## 1. Leer el instrumento antes que la serie

Un *instrumento* es todo el procedimiento que convierte el mundo en un número registrado: quién o qué cuenta, qué se cuenta y dónde. Un *cambio del sistema* es un cambio en lo que se cuenta.

**Observado, en el código fijado.** Una [tarea programada diaria](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) ejecuta el *feeder* (el «alimentador»), [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), que añade a `state/quality-trend/` una fila por cada *artefacto* de gobernanza (una política, un esquema, una habilidad); cada lanzamiento es una *ejecución*. El `citation_count` de una fila se [copia del registro de evolución del artefacto](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L75-L76), un archivo JSON de `state/evolution/`. Desde septiembre de 2026, un segundo script, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), calcula ese número como los [«tracked files that mention any of the artifact's citation paths (`git grep -lF`)»](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) (los archivos rastreados que mencionan alguna de las rutas de citación del artefacto) y [sella el registro](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L104-L107) con `citation_source: "git-grep-v1"`. Antes, dice su docstring, cada métrica [«was typed by hand»](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8) (se introducía a mano) y «nothing updated it afterwards» (nada la actualizaba después).

El feeder reacciona a ese sello en las [líneas 90 a 92](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L90-L92) y en la [línea 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), donde `prev` es la fila anterior del artefacto:

```text
prev = previous.get(artifact, {})
source = metrics.get("citation_source")
rebaseline = bool(prev) and prev.get("citation_source") != source
"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),
```

De ahí se siguen tres cosas:

1. Se declara un *rebaseline*, una nueva línea de base, cuando existe una fila anterior y su etiqueta de fuente difiere de la actual; una clave ausente se lee como nula.
2. El cambio registrado, `delta_citations`, vale entonces 0, mientras que [`citation_count` se escribe tal como se lee](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L96): el salto queda en `citation_count`.
3. Sin fila anterior, o con una fila anterior sin recuento, el feeder resta 0: el «cambio» es el recuento entero.

El docstring del feeder expone la intención: [«the jump is a change of measurement, not a change in citations»](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L14-L18) (el salto es un cambio de medición, no un cambio en las citas).

**Calculado.** [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/analyze.py) reimplementa esta regla sobre la instantánea que toma [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/extract.py). Reproduce `delta_citations` en las 1,537 filas que tienen recuento y las 576 marcas registradas, con 0 discrepancias.

### Ejercicio práctico 1

Filas **sintéticas** de [`scenarios.json`](../../../fixtures/psychohistory/psy-011/scenarios.json). Indique la marca y el `delta_citations` que escribe la regla: (a) la primera fila de un artefacto, con recuento 9; (b) fila anterior con 12 y sin fuente, ahora 27 con `git-grep-v1`; (c) fila anterior con 6 y ahora 19, ambas con `git-grep-v1`, después de que alguien añadiera una ruta a la lista `citation_paths` del registro. ¿Qué caso es un cambio de instrumento que la regla no puede ver?

> **Respuesta:** (a) Sin fila anterior: sin marca, delta 9, un inicio de medición registrado como una subida. (b) Marca, delta 0; el escalón de 15 solo sobrevive en `citation_count`. (c) Sin marca, delta 13: es el caso que la regla no puede ver. La lista de rutas forma parte del instrumento, pero la etiqueta no cambió, así que la edición queda registrada como 13 citas nuevas.

## 2. Localizar el cambio en el registro

**Observado** en [`observed-input.json`](../../../fixtures/psychohistory/psy-011/observed-input.json): 1,548 filas en 88 ejecuciones para 18 artefactos. La primera ejecución, con fecha 2026-05-01, contiene 11 *filas semilla* sin recuento; le siguen 87 ejecuciones del feeder. La clave `citation_source` falta en las 56 primeras ejecuciones (972 filas) y está presente en las 32 últimas. Aparece por primera vez el 2026-09-13T17:52:14Z, cuando 16 filas llevan `git-grep-v1` y `rebaseline: true`. Las otras 2 filas tienen una fuente nula y ninguna marca: sus artefactos tienen una lista `citation_paths` vacía, que [señala un artefacto externo al repositorio](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23), y conservan sus valores introducidos a mano, 55 y 0. Ninguna otra fila está marcada.

**Calculado.** Cada uno de los 16 artefactos tuvo un mismo valor introducido a mano en todas las filas anteriores. Esa ejecución lo sustituyó:

| Artefacto (barras espaciadas) | Introducido a mano | `git grep` |
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

Los escalones van de −7 a +60, y el cociente entre el valor nuevo y el antiguo, de 0 a 27 (indefinido cuando el valor antiguo es 0): ningún factor de conversión único une los dos instrumentos.

### Ejercicio práctico 2

A partir de la tabla, calcule la suma de los 16 recuentos antes y después, y el escalón. Añada los dos artefactos sin marca para obtener el total de los 18 y su cociente. ¿Cuántos recuentos bajaron? ¿Cuánto sumó `delta_citations` en esa ejecución?

> **Respuesta:** Antes `61`, después `351`, escalón `351 − 61 = 290`. Sobre los 18 artefactos: `61 + 55 + 0 = 116` antes y `351 + 55 + 0 = 406` después, un cociente de `406 / 116 = 3.5`. Bajaron dos recuentos (de 8 a 1 y de 1 a 0). Las filas marcadas tienen delta 0 y las otras dos no se movieron, así que `delta_citations` suma 0 en la ejecución en la que el total creció en 290.

## 3. Clasificar cada salto

«Filas con un `delta_citations` distinto de cero» y «filas cuyo recuento difiere del de la fila anterior» parecen el mismo conjunto. Cada uno contiene 20 filas; solo 4 están en ambos. Clasificar cada fila respecto a la fila anterior del artefacto muestra por qué (**calculado**, [`results.json`](../../../fixtures/psychohistory/psy-011/results.json)):

| Clase de fila | Filas | Recuento cambiado | Delta distinto de cero |
|---|---|---|---|
| Primer recuento: no hay recuento anterior con el que comparar | 18 | indefinido | 16 |
| Cambio de instrumento: la fila anterior tiene otra fuente | 16 | 16 | 0 |
| Mismo instrumento: la fila anterior tiene la misma fuente | 1,503 | 4 | 4 |

Los 16 deltas distintos de cero de la primera clase son niveles, no cambios: 10 siguen a una fila semilla, 6 son la primera fila de un artefacto, y suman 116. Quedan 4 filas, todas en la ejecución del 2026-10-03T15:31:16Z, cada una con un escalón de +2.

De los 1,503 pares de filas consecutivas de un mismo artefacto con el mismo instrumento, 1,007 no tienen fuente en ninguna de las dos filas (el periodo de introducción manual y los dos artefactos externos) y registran 0 cambios. Un número que nadie vuelve a introducir no puede moverse, así que este cero dice que el instrumento estaba mudo, no que el sistema estuviera quieto. Con `git-grep-v1`: 496 pares, y los 4 cambios.

La misma división se aplica a la suma sobre los artefactos, que creció de 106 en la primera ejecución del feeder a 414 en la última: `308 = 10 + 290 + 8`, es decir, los primeros recuentos de artefactos añadidos más tarde, el cambio de instrumento y los escalones con el mismo instrumento. Solo el último término es *homogéneo*: mismo instrumento, mismo conjunto de artefactos.

### Ejercicio práctico 3

Partiendo de 1,548 filas y 18 artefactos, deduzca el número de pares con el mismo instrumento y la proporción que cambió. Indique después qué proporción del crecimiento del total se midió en términos homogéneos.

> **Respuesta:** `1,548 − 18 = 1,530` pares de filas. Se retiran los 11 que empiezan en una fila semilla y los 16 que atraviesan el cambio de fuente: `1,530 − 11 − 16 = 1,503`. Cambiaron: `4 / 1,503 = 0.27%`. Crecimiento: `8 / 308 = 2.60%`; el resto es un instrumento nuevo (290) o artefactos nuevos (10).

## 4. Mantener fija la medición antes de leer un cambio

La primera señal de PSY-002 es una tasa de cambio «exceeding 2 standard deviations from its running mean», enunciada para su índice de cristalización, no para las citas. Como **elección de análisis** guardada en `scenarios.json`, aplique una regla de esa forma al escalón entre ejecuciones consecutivas del recuento de citas sumado sobre los artefactos: señale un escalón que se aparte de la media de todos los escalones anteriores (al menos 3) en más de 2 de sus desviaciones estándar poblacionales. Entre una ejecución del feeder y la siguiente pasan de 122 segundos a 6.45 días; la misma regla aplicada a escalones por día señala las mismas ejecuciones. **Calculado** sobre tres versiones de la serie:

| Serie | Escalones señalados | El +8 del 2026-10-03 |
|---|---|---|
| `citation_count` sumado | +2 y +8 el 2026-07-29, +290 el 2026-09-13 | no señalado |
| `delta_citations` sumado | +2 y +8 el 2026-07-29 | señalado |
| Solo escalones con el mismo instrumento | ninguno antes | señalado |

Sobre la suma bruta, la regla da tres alarmas y ninguna es un cambio homogéneo: dos son artefactos que entran en la suma, una es el nuevo instrumento. Esta última infla además la desviación estándar acumulada, de modo que el único escalón homogéneo pasa inadvertido. Si se conservan todos los escalones anteriores, un cambio de instrumento se paga dos veces: una falsa alarma cuando ocurre y ceguera después. Precaución con la última fila: tras un historial de ceros, cualquier escalón distinto de cero queda señalado.

### Ejercicio práctico 4

En la ejecución del 2026-10-03, los 75 escalones anteriores tienen media 4 y desviación estándar 33.2602 en la suma bruta, y media 0.1333 y desviación estándar 0.9428 en el `delta_citations` sumado. Para cada serie, calcule el borde superior de la banda (la media más 2 desviaciones estándar) y el menor escalón entero que quedaría señalado.

> **Respuesta:** Suma bruta: `4 + 2 × 33.2602 = 70.5204`, así que +8 queda dentro de la banda y el menor escalón señalado es 71. Deltas sumados: `0.1333 + 2 × 0.9428 = 2.0189`, así que +8 queda señalado y el menor escalón señalado es 3. Un solo cambio de instrumento llevó el umbral de detección de 3 a 71.

**La objeción más fuerte a esta lectura** es que «mismo instrumento» descansa sobre una etiqueta, y el ejercicio 1(c) muestra un cambio de instrumento que conserva su etiqueta: los cuatro escalones restantes podrían ser un cambio así. El *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección) indica que los cuatro registros de evolución comparten un mismo instante `last_cited`, 2026-10-02T20:05:16Z, situado entre la ejecución anterior y la del escalón, y que dos de los cuatro artefactos miden la misma ruta: cuatro filas, como mucho tres recuentos independientes. Fuera del fixture, en el historial de Git hasta el commit fijado, se lee lo siguiente: el script productor tiene un único commit, y entre las dos ejecuciones solo el commit de la propia tarea diaria tocó `state/evolution/`, así que nadie editó el código ni una lista de rutas; el commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642), hecho en ese mismo instante, añadió traducciones al francés y al español de 13 módulos de cursos; y cada ruta de citación de los cuatro artefactos está citada, en el commit fijado, por exactamente dos archivos añadidos entre las dos ejecuciones: las dos traducciones de una misma lección. Esto es compatible con un cambio en lo que se cuenta, y pequeño: tres de los 13 módulos traducidos citan estas rutas.

### Ejercicio práctico 5

Un panel presenta «citas multiplicadas por unos 3.9 desde julio (de 106 a 414)» como prueba de un cambio de régimen. Acepte o rechace la afirmación, enuncie su criterio y nombre dos registros que harían legible un cambio futuro.

> **Respuesta:** Rechazar. Criterio: dos recuentos solo pueden compararse si los produjo el mismo instrumento, para el mismo conjunto de artefactos. De los 308, 290 vienen de un instrumento nuevo y 10 de artefactos añadidos a la suma; 8 cumplen el criterio, todos en una misma ejecución. Dos registros útiles: una etiqueta de fuente que cambie cada vez que cambien el script, su lista de exclusiones o una lista `citation_paths`; y, en cada cambio, los dos instrumentos ejecutados en paralelo durante varias ejecuciones, para que el solapamiento mida la diferencia.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cinco archivos JSONL de [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), los dos scripts enlazados más arriba y los 18 registros `*.evolution.json` de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution). El [README](../../../fixtures/psychohistory/psy-011/README.md) del fixture da los comandos, las autocomprobaciones y los controles negativos.

**Referencias de método.** Shadish, W. R., Cook, T. D., y Campbell, D. T. (2002), *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Houghton Mifflin (la *instrumentación* como amenaza a la validez).

**No realizado.** El recuento de `git grep` no se recalculó para las ejecuciones anteriores al 2026-09-13, así que nada de lo dicho aquí indica si las citas se movieron entonces. No se leyeron las versiones anteriores del feeder. Las afirmaciones sobre el historial de Git se basan en comandos enumerados en el dossier de revisión, no en el fixture. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Recalcular el recuento `git-grep-v1` en el commit de cada ejecución anterior. Un único instrumento bajo las 87 ejecuciones del feeder mostraría si algo se movió antes de septiembre; si fue así, la conclusión pasa de «casi nada se movió» a «el movimiento no se midió».

**Huella propia.** Este módulo escribe los nombres de los artefactos como etiquetas con barras espaciadas, de modo que ninguno de sus archivos contiene la ruta de citación de ningún artefacto: ejecutada sobre ellos con cada ruta, la búsqueda literal de la sección 1 (`git grep -lF`) no encuentra nada. [PSY-020](psy-020-goodhart-and-reflexivity.es.md) retoma la cuestión general.
