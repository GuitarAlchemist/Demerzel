---
module_id: psy-008-bursts-are-not-rates
department: psychohistory
course: "Las ráfagas no son tasas: llegadas de eventos en el registro de disparadores"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-008
version: "0.1.0"
---

# Las ráfagas no son tasas: llegadas de eventos en el registro de disparadores

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

Convertirá un registro de eventos en recuentos por día natural, los comparará con lo que produciría una tasa constante, medirá la diferencia con el índice de dispersión y sustituirá una media engañosa por cifras que un plan pueda usar. **Pregunta de proyecto:** el registro archivado de disparadores contiene 594 eventos a lo largo de 119 días naturales, 100 de ellos activos. ¿Es una media de «unos cinco eventos al día» una descripción utilizable para planificar?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lee una duplicación de la tasa de señales de conciencia a lo largo de tres ciclos como indicio de que una transición está cerca (su quinta señal). Una tasa es una media; este módulo pregunta qué dice una media de un registro cuyos eventos llegan en ráfagas. [PSY-009](psy-009-concentration-and-heavy-tails.es.md) mide la concentración de ese mismo registro, PSY-022 compara modelos de recuento sobre él y PSY-024 pregunta quién envió los eventos.

## 1. Contar por día natural, días vacíos incluidos

**Observado.** Hasta su retirada el 2026-07-18, el flujo de trabajo [`demerzel-driver-triggers.yml`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) escribía un archivo JSON, un *disparador*, por cada envío a la rama principal, por cada incidencia abierta o reabierta, por cada discusión creada y por cada ejecución fallida de otros cuatro flujos de trabajo. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) contiene 594, fechados del 2026-03-20 al 2026-07-16, de solo tres tipos: 252 `discussion_created`, 207 `push` y 135 `issue_opened`. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-008/extract.py) lee los 594 en el commit `4b03838`, rechaza una carpeta que difiera de su resumen fijado y escribe una fila por evento en [`observed-input.json`](../../../fixtures/psychohistory/psy-008/observed-input.json). Los pocos archivos de disparador que están [fuera del archivo histórico](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers) quedan excluidos.

Un *día* es la fecha UTC de la marca de tiempo de un disparador. Del primer día al último hay **119** días naturales: **100** días *activos*, con al menos un evento, y **19** vacíos. Una tasa cuenta eventos sobre tiempo transcurrido, así que los días vacíos permanecen en la serie.

```text
media por día natural = 594 / 119 = 4.99
media por día activo  = 594 / 100 = 5.94
```

**Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-008/analyze.py) en [`results.json`](../../../fixtures/psychohistory/psy-008/results.json):

| Eventos en el día | Días | Eventos |
|---|---|---|
| 0 | 19 | 0 |
| 1 a 2 | 76 | 89 |
| 3 a 11 | 13 | 72 |
| 12 o más | 11 | 433 |

El día más frecuente tiene exactamente 1 evento: 63 días, el 52.94%. Exactamente 5 eventos ocurrieron en 2 días, y 4, 5 o 6 eventos en 4 días, el 3.36% de los días. «Unos cinco al día» no describe casi ningún día.

### Ejercicio práctico 1

Calcule las dos medias. Un colega presupuesta los próximos 30 días naturales multiplicando por 30 la media por día activo. ¿Qué da eso, qué da la media por día natural y dónde está el error?

> **Respuesta:** `594 / 119 = 4.99` y `594 / 100 = 5.94`. Con la media natural, `30 × 594 / 119 = 149.75` eventos; con la media por día activo, `30 × 5.94 = 178.2`, que es `119 / 100 = 1.19` veces la cifra natural: la media por día activo quita los 19 días vacíos del denominador, pero los próximos 30 días también contendrán días vacíos.

## 2. La referencia de Poisson y el índice de dispersión

Si los eventos llegan con independencia unos de otros a una tasa constante (un *proceso de Poisson*), el recuento de un día sigue una distribución de Poisson, cuya varianza es igual a su media. El *índice de dispersión* D compara ambas:

```text
probabilidad de Poisson  P(k eventos) = mean^k × exp(−mean) / k!
varianza de la muestra   s² = (Σx² − (Σx)² / n) / (n − 1)
índice de dispersión     D  = s² / mean
```

Este módulo usa en todas partes la varianza de la muestra, con divisor n − 1. Un D cercano a 1 es lo que da una tasa constante; un D por debajo de 1 significa recuentos más regulares que el azar (un reloj diario da 0); un D por encima de 1 es *sobredispersión*: tramos tranquilos y ráfagas. Bajo un proceso de Poisson, `(n − 1) × D` es aproximadamente una chi cuadrado con n − 1 grados de libertad, de modo que D tiene una desviación típica de alrededor de `sqrt(2 / (n − 1))`, aquí 0.13 (Cox y Lewis 1966).

**Calculado.** Los recuentos diarios dan s² = 198.52 y D = 39.77, unas 298 de esas desviaciones típicas por encima de 1. La referencia es la distribución de Poisson con la media observada, 594/119:

| Clase de día | Probabilidad de referencia | Esperado en 119 días | Observado |
|---|---|---|---|
| ningún evento | 0.68% | 0.81 | 19 |
| exactamente 1 evento | 3.39% | 4.04 | 63 |
| 4, 5 o 6 eventos | 49.72% | 59.17 | 4 |
| 12 o más (cuantil del 99% de la referencia: 11) | 0.54% | 0.64 | 11 |

El cuantil del 99% es el menor k con P(0) + … + P(k) ≥ 0.99. Llamemos *días de ráfaga* a los 11 días por encima de él. El más cargado, el 2026-03-22, tiene 109 eventos; la referencia da a un día al menos tan cargado una probabilidad de 6.32 × 10⁻¹⁰³. Una cifra así significa que la referencia es la descripción equivocada, no que haya ocurrido algo casi imposible.

**Controles sintéticos.** El mismo código devuelve D = 0.0017 para 594 eventos repartidos por igual en 119 días, y D = 1.23, dentro del azar de 1, para un registro con semilla fija en el que cada evento cae en un día extraído uniformemente. Los tres registros comparten la media 4.99: la media no permite distinguirlos.

### Ejercicio práctico 2

Con n = 119, Σx = 594 y Σx² = 26,390, calcule s² y D, y diga después a cuántas desviaciones típicas por encima de 1 queda D.

> **Respuesta:** `(Σx)² / n = 352,836 / 119 = 2,965.01`, así que `s² = (26,390 − 2,965.01) / 118 = 23,424.99 / 118 = 198.52` y `D = 198.517 / 4.9916 = 39.77`. Con `sqrt(2 / 118) = 0.1302`, `(39.77 − 1) / 0.1302 = 297.8` desviaciones típicas: una tasa constante no es candidata.

### Ejercicio práctico 3

Calcule P(0) y P(1) de la referencia, los números de días así esperados en 119 y compárelos con el registro.

> **Respuesta:** `exp(−4.9916) = 0.006795` y `119 × 0.006795 = 0.81` días vacíos esperados frente a 19 observados, 23.5 veces más. `4.9916 × 0.006795 = 0.03392` y `119 × 0.03392 = 4.04` días de un evento esperados frente a 63 observados, 15.6 veces más. El registro tiene demasiados días vacíos, de un evento y de ráfaga, y le falta el medio: los días que se parecen a la media.

## 3. De qué están hechos los días

**Calculado a partir de los tipos de evento.**

*Un reloj.* De los 63 días de un solo evento, 58 tienen un único `discussion_created`, fechado entre las 13:51 y las 16:09 UTC, 56 de ellos en días laborables. De los 85 días laborables, 81 tienen al menos un `discussion_created`. Eso es compatible con una tarea programada; un candidato, [`streeling-daily.yml`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/streeling-daily.yml), se ejecuta de lunes a viernes a las 13:17 UTC y publica discusiones. Un disparador no registra qué discusión vio, así que la atribución es una inferencia.

*Los fines de semana están vacíos o cargados.* De los 19 días vacíos, 15 son sábados o domingos; también lo son los cuatro días más cargados, cuyas ráfagas son de más de una clase:

| Día | Eventos | `push` | `issue_opened` | `discussion_created` |
|---|---|---|---|---|
| 2026-03-22, domingo | 109 | 32 | 38 | 39 |
| 2026-06-28, domingo | 72 | 4 | 34 | 34 |
| 2026-03-21, sábado | 60 | 41 | 6 | 13 |
| 2026-06-27, sábado | 45 | 0 | 21 | 24 |

**Observado.** El registro del proyecto [`anti-pattern-003-push-triggered-spam`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/patterns/anti-pattern-003-push-triggered-spam.pattern.json) describe flujos de trabajo que «trigger on every push to master, causing duplicate runs when a session has many commits». Fecha el patrón el 2026-03-21 y el 03-22 (2 apariciones), lo detecta con «Workflow runs > 3 in a single day for the same workflow» e informa de una corrección en un flujo de trabajo el 03-22.

**Calculado.** El registro concuerda con ese registro en esos dos días: 41 y 32 eventos `push`. Pero los envíos son 77 de los 286 eventos de los cuatro días más cargados, el 26.92%, por debajo de su proporción en todo el registro (207 de 594, el 34.85%).

Cada archivo archivado es una ejecución del productor, que debe ejecutarse una vez por evento. Aplicado literalmente a él, el umbral del registro se supera en 21 días, 18 de ellos después del 03-22. Fíjese en la forma de la regla: un umbral sobre un recuento diario, no sobre una media.

### Ejercicio práctico 4

Clasifique tres días: (a) el 2026-03-21, 60 eventos de los cuales 41 `push`; (b) el 2026-06-27, 45 eventos, ningún `push`; (c) el 2026-04-07, un martes con un `discussion_created` a las 13:54 UTC. ¿Cuál describe el registro de push-triggered-spam, y cuál marcaría su regla?

> **Respuesta:** (a) Descrito y marcado: una ráfaga de envíos en una fecha que el registro nombra, y 60 > 3. (b) Marcado, ya que 45 > 3, pero no descrito: ningún envío en absoluto, la ráfaga son 21 incidencias y 24 discusiones. (c) Ninguno de los dos: una ejecución, a la hora de una programación de días laborables. Tras una sola media hay tres patrones; una corrección dirigida a los envíos no habría tocado (b).

## 4. Las ventanas más largas no rescatan la media

Una reparación natural es planificar por semanas y dejar que las ráfagas se promedien. Cortemos los 119 días en 17 bloques de 7 días a partir del primer día:

```text
176 38 8 13 7 5 14 6 15 6 6 6 8 63 204 11 8
```

**Calculado.** El bloque medio tiene 34.94 eventos y el bloque mediano 8 (el cuantil del 50%; por *rango más próximo*, el cuantil de nivel p es el k-ésimo menor de n valores, con k = p × n redondeado hacia arriba). El D de los bloques es 104.41, mayor que el de los días; un proceso de Poisson daría alrededor de 1 en cualquier longitud de ventana. Un índice que crece con la ventana significa que los días cargados llegan en series: los 11 días de ráfaga forman dos *episodios* (los días de ráfaga separados por 7 días como máximo cuentan como un episodio, una decisión de análisis), tres días entre el 03-21 y el 03-27 y ocho entre el 06-21 y el 07-02, a 86 días de distancia.

El total del bloque al menos se duplicó en 4 de los 16 pasos entre bloques vecinos, así que una regla de duplicación del tipo de PSY-002 necesita una referencia que tenga en cuenta las ráfagas. La media misma se conoce mal: su error estándar, `sqrt(variance / n)`, sería 0.20 con la varianza de la referencia (la media), y es 1.29 con s² y 2.09 a partir de los bloques, `sqrt(s²_blocks / 17) / 7`. El resultado tampoco depende de la medianoche UTC: moviendo la frontera del día 6, 12 o 18 horas, D queda entre 47.58 y 64.09 y la mediana se mantiene en 1.

**Con qué planificar en su lugar** (calculado): días vacíos, el 15.97%; días con 2 eventos como máximo, el 79.83%; mediana 1, cuantil del 90% 8, cuantil del 95% 24, máximo 109; días de ráfaga, 11 de 119, en dos episodios. PSY-009 dimensiona un plan sobre un cuantil así.

**La objeción más fuerte a esta lectura**: para un total a largo horizonte la tasa media es la magnitud correcta sea cual sea la dispersión, ya que total esperado = tasa × tiempo. Eso solo se cumple si los meses venideros se parecen a estas 17 semanas y, aun entonces, la tasa es 4.99 con un error estándar cercano a 2.09, porque 11 días de ráfaga llevan 433 de los 594 eventos. **Esta muestra no permite distinguir un proceso que produce ráfagas cada pocos meses de uno que las produjo dos veces por razones sin relación.** La siguiente comprobación lo zanjaría.

### Ejercicio práctico 5

Un compañero propone «unos 35 eventos por semana, con un margen del 20%». ¿Cuántos de los 17 bloques caen dentro de esa banda? Enuncie un criterio para aceptar una media como descripción de planificación y aplíquelo.

> **Respuesta:** El 20% alrededor de 34.94 va de 27.95 a 41.93; un bloque de 17 (38 eventos) queda dentro, y el bloque mediano tiene 8. Criterio: aceptar la media cuando los recuentos se dispersen a su alrededor como lo haría una tasa constante, con un D a menos de dos desviaciones típicas de 1 en la ventana sobre la que se planifica. Para 17 bloques, `sqrt(2 / 16) = 0.35`, así que D debería quedar entre 0.29 y 1.71; es 104.41. Rechace la media; planifique con la proporción de días vacíos, la mediana y los episodios de ráfaga.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los 594 archivos de disparador archivados (árbol de Git `2da37c16496d39c0c9137897c8be2b0c6d6b7978`; resumen del manifiesto en `observed-input.json`), el registro del patrón y los dos archivos de flujo de trabajo enlazados más arriba.

**Fixture.** [`scenarios.json`](../../../fixtures/psychohistory/psy-008/scenarios.json) contiene las decisiones de análisis; el [README](../../../fixtures/psychohistory/psy-008/README.md) da los comandos, las autocomprobaciones y los controles.

**Referencias de método.** Cox, D. R., y Lewis, P. A. W. (1966), *The Statistical Analysis of Series of Events*, Methuen (el índice de dispersión y su prueba). Barabási, A.-L. (2005), «The origin of bursts and heavy tails in human dynamics», *Nature* 435, 207–211 (los tiempos entre eventos, no analizados aquí).

**Límites y lo que no se hizo.** Un repositorio y 119 días, la vida activa de un solo flujo de trabajo productor; dos episodios no pueden decir con qué frecuencia ocurren las ráfagas. Una marca de tiempo es el momento en que el productor escribió el archivo. Doce archivos de disparador se borraron del repositorio sin archivarlos (siete fechados el 2026-03-20, cinco el 2026-06-30, ninguno en los cuatro días más cargados); PSY-009 los cuenta, y con ellos la media sería 5.09 y D 39.40. No se comprobó si ejecuciones solapadas perdieron otros. No se ajustó ningún modelo de recuento (PSY-022), no se calculó ninguna medida de concentración (PSY-009) ni se estableció la causa de ninguna ráfaga. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Contar envíos, incidencias y discusiones por día a partir del propio historial de eventos de GitHub durante un periodo más largo, con la causa de cada día de ráfaga. Si las ráfagas se repiten con un espaciado y un tamaño estables, un reloj de días laborables más episodios se convierte en un plan utilizable; si no, el plan honesto es una alarma de umbral, no un pronóstico.
