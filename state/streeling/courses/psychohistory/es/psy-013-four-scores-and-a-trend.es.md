---
module_id: psy-013-four-scores-and-a-trend
department: psychohistory
course: "Cuatro puntuaciones y una tendencia: leer el historial de resiliencia"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-013
version: "0.1.0"
---

# Cuatro puntuaciones y una tendencia: leer el historial de resiliencia

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo dará un intervalo exacto para una puntuación obtenida en once ensayos, pondrá a prueba un salto entre dos puntuaciones, tendrá en cuenta que se hacen varias pruebas sobre los mismos cuatro números y dirá qué mide un conjunto de prueba reutilizado. **Pregunta de proyecto:** el historial de resiliencia muestra 0.00, 0.64, 0.73, 0.82 a lo largo de cuatro ciclos; ¿cuáles de estos saltos se distinguen del azar, y qué mide un conjunto de inyecciones repetido?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lee esta puntuación como un indicador de régimen y su variación como una velocidad. Este módulo se pregunta cuánto cambio pueden mostrar once ensayos. [PSY-004](psy-004-how-large-is-large.es.md) construye el intervalo exacto que se usa aquí, [PSY-011](psy-011-measurement-change-or-system-change.es.md) trata los cambios de instrumento y [PSY-023](psy-023-monitoring-a-plan.es.md) diseña reglas de alarma.

## 1. Leer el registro antes de calcular

**Observado** en el commit `4b03838`. El proyecto define la puntuación de resiliencia como `R = injections_caught / injections_total` ([glosario](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/CONTEXT.md#L48), [política de la métrica](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/resilience-metric-policy.yaml)). Una *inyección* es un defecto introducido a propósito. El [informe de la prueba de caos](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/chaos-test-report.md) enumera once, repartidas en tres archivos: por ejemplo, una asignación (*binding*) que nada lee en [`chaos-test.ixql`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/chaos-test.ixql), una política cuya descripción carece de sentido de forma deliberada, un esquema al que nada hace referencia. Cada una tiene uno de siete *niveles* (de L0, un archivo entero, a L4, una expresión, más los niveles de política y de esquema) y un detector esperado.

[`history.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json) contiene cuatro registros, de `chaos-001` a `chaos-004`, fechados en un lapso de 20 horas el 2026-03-22 y el 2026-03-23; el commit fijado es 204 días posterior. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/extract.py) guarda una instantánea en [`observed-input.json`](../../../fixtures/psychohistory/psy-013/observed-input.json), y [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/analyze.py) confirma que los nombres de las once inyecciones son idénticos en los cuatro registros: el conjunto se reutiliza, no se vuelve a extraer. El README enuncia la afirmación que se examina aquí: «Trend: 0.0 → 0.64 → 0.73 → 0.82 across 4 chaos cycles» (una tendencia a lo largo de cuatro ciclos de caos; [línea 132](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L132)).

| Ciclo | Interceptadas (registradas) | Etiquetas de estado de las 11 inyecciones |
|---|---|---|
| chaos-001 | 0 | 11 *missed* |
| chaos-002 | 7 | 6 *automated*, 2 *spec-only*, 2 *manual*, 1 *delayed-14d* |
| chaos-003 | 8 | 6 *automated*, 2 *policy-enforceable*, 2 *spec-only*, 1 *delayed-14d* |
| chaos-004 | 9 | 6 *automated*, 3 *policy-enforceable*, 2 *spec-only* |

Tres hechos van antes de cualquier estadística:

- **Qué significa «interceptada».** El [informe de `chaos-003`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/shake-metafix-cycle-001.md) da una inyección por interceptada cuando su estado es `automated` o `policy-enforceable`, y describe el segundo como reglas que debe ejecutar una persona, «NOT yet automated tooling» (todavía no son herramientas automatizadas).
- **Las cuentas del ciclo 2 no cuadran.** Esa regla da 6, las puntuaciones por nivel del registro implican 5, y el valor registrado es 7.
- **El punto de partida depende de quién puntúa.** El informe de la prueba de caos, con la misma fecha que `chaos-001`, puntúa las mismas once inyecciones con 5/11 «immediate» (inmediatas) y 9/11 «including spec-level» (contando el nivel de especificación). El historial registra 0.

Los otros tres archivos de la carpeta, `2026-03-23-red-team-cycle-00N.json`, son otra serie (14 escenarios de ataque calificados PASS, PARTIAL o FAIL), no el detalle de estos ciclos.

### Ejercicio práctico 1

Aplique la regla «interceptada = automated o policy-enforceable» a las cuatro filas de la tabla. ¿Dónde discrepa del recuento registrado? Puntúe después el ciclo 2 a partir de sus puntuaciones por nivel: 1.0 para L2 (tres inyecciones) y para L3 (una), 0.5 para L4 (dos), 0 en los demás niveles.

> **Respuesta:** La regla da 0, 6, 8, 9 frente a los 0, 7, 8, 9 registrados: solo discrepa el ciclo 2. Puntuaciones por nivel: `3 × 1 + 1 × 1 + 2 × 0.5 = 5`. El registro respalda 7, 6 o 5 para un mismo ciclo, y ningún conjunto de etiquetas de estado reproduce los cuatro recuentos registrados (`status_rules` en [`results.json`](../../../fixtures/psychohistory/psy-013/results.json)). Las secciones siguientes usan 7 e indican qué cambia con 6 o con 5.

## 2. Un intervalo para cada puntuación

Trate un ciclo como 11 ensayos independientes con una única tasa de detección p, como si las inyecciones fueran una muestra aleatoria de los defectos que importan (un supuesto que la sección 4 pone en duda). El *intervalo exacto al 95% (de Clopper–Pearson)* es el conjunto de tasas que el recuento no rechaza: su cota inferior es el p para el que «este número o más» tiene probabilidad 0.025, y su cota superior, el p para el que «este número o menos» tiene probabilidad 0.025.

**Calculado** (cotas redondeadas a tres decimales):

| Ciclo (interceptadas) | Intervalo al 95% | Bandas de la política que toca |
|---|---|---|
| chaos-001 (0/11) | 0–0.285 | critical |
| chaos-002 (7/11) | 0.308–0.891 | critical, warning, watch |
| chaos-003 (8/11) | 0.390–0.940 | las cuatro |
| chaos-004 (9/11) | 0.482–0.977 | las cuatro |

La política de la métrica corta R en 0.5, 0.7 y 0.9 y obtiene así las bandas critical, warning, watch y healthy (crítica, advertencia, vigilancia y saludable). La última puntuación, 0.82, cae en «watch» («régimen proactivo» en PSY-002), pero su intervalo tiene una anchura de 0.49 y toca todas las bandas. El primer intervalo no se solapa con ninguno de los otros; los tres últimos se solapan entre sí.

### Ejercicio práctico 2

Para 0 de n, la cota superior tiene una forma cerrada, `1 − 0.025^(1/n)`; para n de n, la cota inferior es `0.025^(1/n)`. Ambas corresponden al intervalo bilateral; una cota unilateral al 95%, como en [PSY-006](psy-006-transition-matrix-from-counts.es.md), usa 0.05. (a) Calcule las dos para n = 11. (b) Un conjunto nuevo se intercepta por completo. ¿Qué tamaño debe tener para que la cota inferior alcance el umbral de «healthy», 0.9?

> **Respuesta:** (a) `0.025^(1/11) = 0.715`: 0 de 11 da una cota superior de `1 − 0.715 = 0.285`, y 11 de 11, una cota inferior de 0.715, todavía en «watch». (b) La cota alcanza 0.9 cuando `0.9^n ≤ 0.025`. `0.9^35 = 0.02503` es demasiado grande y `0.9^36 = 0.02253` es lo bastante pequeño: 36 inyecciones, todas interceptadas.

## 3. Probar cada salto y después contar las pruebas

**Calculado.** La *prueba exacta de Fisher* compara dos recuentos como dos muestras independientes. Se fijan los márgenes: 11 ensayos por ciclo y el total de inyecciones interceptadas en ambos. Si los ciclos comparten una misma tasa, todas las maneras de repartir esas inyecciones interceptadas entre los 22 ensayos son igual de probables. El *valor p* que se usa aquí es bilateral: la probabilidad total de todas las tablas que no son más probables que la observada. El valor unilateral (el ciclo posterior es más alto) es la mitad para el primer salto.

| Ciclos comparados (recuentos) | p bilateral |
|---|---|
| Del 1 al 2 (0/11, 7/11) | 0.0039 |
| Del 2 al 3 (7/11, 8/11) | 1 |
| Del 3 al 4 (8/11, 9/11) | 1 |
| Del 1 al 4 (0/11, 9/11) | 0.0002 |

**Cuatro pruebas sobre cuatro números.** Cuatro pruebas independientes al nivel del 5% dan al menos un falso positivo (un p inferior a 0.05 cuando nada difiere) el 18.5% de las veces (`1 − 0.95^4`). La *corrección de Bonferroni* compara cada p con `0.05 / 4 = 0.0125` y es válida sea cual sea la dependencia entre las pruebas. Aquí las pruebas comparten recuentos, y una prueba exacta sobre 11 ensayos es conservadora: sobre todas las maneras de repartir las 24 inyecciones interceptadas registradas entre los 44 ensayos, una prueba aislada cae por debajo de 0.05 en el 1.78% de las configuraciones, y al menos una de las cuatro, en el 6.2%. La corrección no cambia ningún veredicto de la tabla, pero decide otras dos lecturas:

- **El diseño es pareado.** Se vuelven a puntuar las mismas inyecciones, así que la prueba adecuada es la *prueba exacta del signo* (la prueba de McNemar en su forma exacta): si nada hubiera cambiado, una inyección cuyo resultado difiere tendría la misma probabilidad de haberse movido en un sentido que en el otro. Del ciclo 1 al ciclo 2, siete ganancias y ninguna pérdida dan un p bilateral de `2 × (1/2)^7 = 0.0156`, por encima de 0.0125 (con seis ganancias, según las etiquetas de estado: 0.031).
- **El recuento del ciclo 2.** Con 6 en lugar de 7, el p de Fisher es 0.0124; con 5, es 0.035.

**¿Un salto o tres?** Para los tres ciclos posteriores, una prueba exacta de «una tasa común» (Freeman–Halton) da p = 0.88, y una prueba exacta de tendencia unilateral (Cochran–Armitage, puntuaciones 0, 1, 2), p = 0.24. Tres ciclos independientes de 11 ensayos con su tasa combinada, 8/11, suben de forma estricta en el 8.5% de los casos. La política etiqueta un ciclo como «improving» (en mejora) cuando su R supera la media de los dos anteriores; en ciclos así, esa regla dice «improving» el 45% de las veces, y dos veces seguidas, el 18%.

Con los recuentos registrados y la prueba de Fisher, el primer salto es el único que se distingue del azar (con la prueba pareada, resiste la corrección con tres comparaciones y no con cuatro); los dos saltos posteriores no se distinguen con ninguna de las lecturas anteriores.

### Ejercicio práctico 3

Calcule a mano el valor p unilateral de Fisher del ciclo 1 al ciclo 2 y, después, el bilateral.

> **Respuesta:** Con 7 inyecciones interceptadas entre 22 ensayos y ninguna en el ciclo 1, los 11 ensayos del ciclo 1 salen todos de los 15 no interceptados: `C(15,11) / C(22,11) = 1,365 / 705,432 = 0.0019`. La tabla simétrica (7 y después 0) es igual de probable y ninguna otra tabla es tan improbable, así que el valor bilateral es el doble: 0.0039.

### Ejercicio práctico 4

Del ciclo 2 al ciclo 3, las etiquetas de estado muestran dos inyecciones que pasan de no interceptadas a interceptadas, y ninguna en sentido contrario. Dé el valor p bilateral de la prueba del signo. Decida después si el valor p pareado del primer salto resiste una corrección de Bonferroni para tres pruebas (los saltos consecutivos) y para cuatro (añadiendo el primer ciclo frente al último).

> **Respuesta:** `2 × (1/2)^2 = 0.5`: ningún indicio de cambio. Primer salto: `2 × (1/2)^7 = 1/64 = 0.0156`. Con tres pruebas, el umbral es `0.05 / 3 = 0.0167` y el salto lo supera; con cuatro, es 0.0125 y no lo supera. El veredicto depende de cuántas comparaciones reconozca usted haber hecho.

## 4. Lo que mide un conjunto de inyecciones reutilizado

**Observado.** Cada registro posterior dice qué se construyó antes de puntuarlo. `chaos-002`: tres detecciones implementadas en un analizador sintáctico (*parser*), tras lo cual seis inyecciones citan una misma función, `analyzeLolli()`, como su detector. `chaos-003`: dos correcciones en el nivel de política, y las dos inyecciones de política cambian de estado. `chaos-004`: dos correcciones en el nivel de esquema, una de ellas un archivo de prueba «including injection #10 regression test», y la inyección 10, el esquema al que nada hace referencia, es la que cambia. Ninguna inyección vuelve de interceptada a no interceptada.

A partir del ciclo 2, R sobre este conjunto cuenta, por tanto, cuántos de once defectos conocidos tienen ya un detector o una regla escrita: una medida de progreso válida para una lista de reparaciones, pero no la tasa de detección de defectos que nadie ha introducido todavía, que es lo que sugiere el nombre «resiliencia». **Analogía:** un modelo ajustado contra su propio conjunto de prueba mantiene una puntuación creciente que ya no estima su rendimiento sobre datos nuevos (Dwork et al. 2015).

**Sintético** (no existe tal conjunto). Un *conjunto reservado* (*held-out set*), escrito por alguien que no ha leído las correcciones y puntuado una sola vez antes de cualquier reparación, estimaría esa tasa. Con 11 inyecciones reservadas, una prueba de Fisher bilateral frente a 9/11 cae por debajo de 0.05 solo con 3 interceptadas o menos (p = 0.030; con 4 interceptadas da 0.080).

**La objeción más fuerte a esta lección** es que su modelo de azar no se ajusta ni al conjunto ni a la puntuación. Las inyecciones no se extrajeron por muestreo; un estado registra si existe un detector, no una ejecución con ruido; y las inyecciones se mueven juntas: las puntuaciones por nivel valen 0 o 1 en todos los ciclos menos uno. Con los 7 niveles como unidades (0, 2, 4, 5 puntuados por completo), el primer salto tiene p = 0.46, y el primer ciclo frente al último, 0.021, por encima de 0.0125. El punto de partida también se mueve: con el 5/11 del informe en lugar de 0, el ciclo 2 da p = 0.67 y el ciclo 4 da 0.18. **Este registro no permite distinguir un salto en la detección de un cambio en lo que se contó como interceptado.** La próxima comprobación, más abajo, lo zanjaría.

### Ejercicio práctico 5

Sintético. Un quinto ciclo registra 11 de 11 sobre el mismo conjunto, y la línea de estado indica R = 1.00, «healthy». Después, un colega escribe 11 inyecciones nuevas sin leer las correcciones; se interceptan 4. (a) ¿Qué establece ese 1.00? (b) ¿Difiere 4/11 del último valor registrado, 9/11? Enuncie su criterio.

> **Respuesta:** (a) Que los once defectos conocidos tienen ya un detector o una regla, no cómo les va a defectos nuevos; incluso leído como una muestra nueva, 11 de 11 sigue siendo compatible con tasas tan bajas como 0.715. (b) Criterio: un p bilateral de Fisher inferior a 0.05. 4/11 frente a 9/11 da 0.080, así que los dos no se distinguen; 3/11 daría 0.030.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cuatro archivos de [`state/resilience/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience), los dos informes, la política de la métrica, el glosario, la línea del README y los tres archivos de inyecciones. `extract.py` se niega a ejecutarse si alguno difiere de su blob fijado o si la carpeta gana un archivo.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py`, y después `analyze.py` en la misma carpeta. El [README](../../../fixtures/psychohistory/psy-013/README.md) enumera las autocomprobaciones y los controles negativos, y [`scenarios.json`](../../../fixtures/psychohistory/psy-013/scenarios.json), las elecciones del análisis.

**Referencias de método.** Clopper, C. J., y Pearson, E. S. (1934), «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial», *Biometrika* 26(4), 404–413. Dunn, O. J. (1961), «Multiple Comparisons Among Means», *Journal of the American Statistical Association* 56, 52–64 (la corrección de Bonferroni). Agresti, A. (2013), *Categorical Data Analysis*, tercera edición, Wiley (pruebas exactas, prueba de McNemar). Dwork, C., y cinco coautores (2015), «The Reusable Holdout: Preserving Validity in Adaptive Data Analysis», *Science* 349, 636–638.

**No realizado.** No se volvió a ejecutar ninguna inyección, y el analizador sintáctico que citan los registros ([`Parser.fs`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/tools/ixql-parser/IxqlParser/Parser.fs), en este repositorio) no se compiló ni se ejecutó: el fixture solo lee los registros. No existe ningún conjunto reservado. Las cuatro comparaciones se eligieron después de conocer las cuatro puntuaciones. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Poner por escrito la regla de puntuación, aplicarla a los once veredictos del primer informe y a cada ciclo, y después puntuar una sola vez un conjunto reservado. Si la regla sitúa el punto de partida cerca de 5/11, la conclusión pasa de «un gran salto y después una meseta» a «ningún salto distinguible». Por separado, compilar el analizador sintáctico y aplicar `analyzeLolli` a `pipelines/chaos-test.ixql`: los registros le atribuyen seis inyecciones.
