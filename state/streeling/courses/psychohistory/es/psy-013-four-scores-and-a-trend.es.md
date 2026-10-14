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

Pondrá un intervalo exacto a una puntuación obtenida en once ensayos, pondrá a prueba un escalón entre dos puntuaciones, tendrá en cuenta varias pruebas sobre los mismos cuatro números y dirá qué mide un conjunto de prueba reutilizado. **Pregunta de proyecto:** el historial de resiliencia muestra 0.00, 0.64, 0.73 y 0.82 a lo largo de cuatro ciclos; ¿cuál de estos escalones se distingue del azar, y qué mide un conjunto de inyecciones repetido?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lee esta puntuación como un indicador de régimen y su cambio como una velocidad. Este módulo pregunta cuánto cambio pueden mostrar once ensayos. [PSY-004](psy-004-how-large-is-large.es.md) construye el intervalo exacto que se usa aquí, [PSY-011](psy-011-measurement-change-or-system-change.es.md) trata los cambios de instrumento y PSY-023 diseña reglas de alarma.

## 1. Leer el registro antes de calcular

**Observado** en el commit `4b03838`. El proyecto define la puntuación de resiliencia como `R = injections_caught / injections_total` ([glosario](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/CONTEXT.md#L48), [política de la métrica](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/resilience-metric-policy.yaml)). Una *inyección* es un defecto plantado a propósito. El [informe de la prueba de caos](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/chaos-test-report.md) enumera once en tres archivos, por ejemplo un enlace que nada lee en [`chaos-test.ixql`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/chaos-test.ixql), una política cuya descripción carece de sentido a propósito, un esquema al que nada hace referencia. Cada una tiene uno de siete *niveles* (L0, un archivo entero, hasta L4, una sola expresión, y luego política y esquema) y un detector esperado.

[`history.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json) tiene cuatro registros, de `chaos-001` a `chaos-004`, fechados en menos de 20 horas los días 2026-03-22 y 2026-03-23; el commit fijado está fechado 204 días después. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/extract.py) lo guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-013/observed-input.json), y [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/analyze.py) confirma que los once nombres de inyección son idénticos en los cuatro registros: el conjunto se reutiliza, no se vuelve a sortear. El README enuncia la afirmación que se examina aquí: «Trend: 0.0 → 0.64 → 0.73 → 0.82 across 4 chaos cycles» ([línea 132](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L132)).

| Ciclo | Detectadas (registrado) | Etiquetas de estado de las 11 inyecciones |
|---|---|---|
| chaos-001 | 0 | 11 no detectadas |
| chaos-002 | 7 | 6 automated, 2 spec-only, 2 manual, 1 delayed-14d |
| chaos-003 | 8 | 6 automated, 2 policy-enforceable, 2 spec-only, 1 delayed-14d |
| chaos-004 | 9 | 6 automated, 3 policy-enforceable, 2 spec-only |

Tres hechos vienen antes de cualquier estadística:

- **Qué significa «detectada».** El [informe de `chaos-003`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/shake-metafix-cycle-001.md) marca una inyección como detectada cuando su estado es `automated` o `policy-enforceable`, y llama al segundo reglas ejecutables por una persona, «NOT yet automated tooling».
- **El ciclo 2 no cuadra.** Esa regla da 6, las puntuaciones de nivel del registro implican 5, y lo registrado es 7.
- **La referencia depende de quien puntúa.** El informe de la prueba de caos, fechado el mismo día que `chaos-001`, puntúa esas mismas once inyecciones con 5/11 «immediate» y 9/11 «including spec-level». El historial registra 0.

Los otros tres archivos de la carpeta, `2026-03-23-red-team-cycle-00N.json`, son otra serie (14 escenarios de ataque calificados PASS, PARTIAL o FAIL), no el detalle de estos ciclos.

### Ejercicio práctico 1

Aplique la regla «detectada = automated o policy-enforceable» a las cuatro filas de la tabla. ¿Dónde discrepa del recuento registrado? Puntúe después el ciclo 2 a partir de sus puntuaciones de nivel: 1.0 para L2 (tres inyecciones) y para L3 (una), 0.5 para L4 (dos), 0 en el resto.

> **Respuesta:** La regla da 0, 6, 8, 9 frente a los 0, 7, 8, 9 registrados: solo el ciclo 2 discrepa. Puntuaciones de nivel: `3 × 1 + 1 × 1 + 2 × 0.5 = 5`. El registro respalda 7, 6 o 5 para un mismo ciclo, y ningún conjunto de etiquetas de estado reproduce los cuatro recuentos registrados (`status_rules` en [`results.json`](../../../fixtures/psychohistory/psy-013/results.json)). Las secciones siguientes usan 7 y dicen qué cambia con 6 o con 5.

## 2. Poner un intervalo a cada puntuación

Tratemos un ciclo como 11 ensayos independientes con una sola tasa de detección p, como si las inyecciones fueran una muestra al azar de los defectos que importan (un supuesto que la sección 4 cuestiona). El *intervalo exacto al 95% (de Clopper–Pearson)* es el conjunto de tasas que el recuento no rechaza: su cota inferior es el p al que «esta cantidad o más» tiene probabilidad 0.025, y su cota superior el p al que «esta cantidad o menos» tiene probabilidad 0.025.

**Calculado** (cotas redondeadas a tres decimales):

| Ciclo (detectadas) | Intervalo al 95% | Bandas de la política tocadas |
|---|---|---|
| chaos-001 (0/11) | 0–0.285 | critical |
| chaos-002 (7/11) | 0.308–0.891 | critical, warning, watch |
| chaos-003 (8/11) | 0.390–0.940 | las cuatro |
| chaos-004 (9/11) | 0.482–0.977 | las cuatro |

La política de la métrica corta R en 0.5, 0.7 y 0.9 en critical, warning, watch y healthy. La última puntuación, 0.82, se lee «watch» («proactive» en PSY-002), pero su intervalo tiene una anchura de 0.49 y toca todas las bandas. El primer intervalo no se solapa con ninguno de los otros; los tres últimos se solapan entre sí.

### Ejercicio práctico 2

Para 0 de n la cota superior tiene una forma cerrada, `1 − 0.025^(1/n)`; para n de n la cota inferior es `0.025^(1/n)`. Estas pertenecen al intervalo bilateral; una cota unilateral al 95%, como en [PSY-006](psy-006-transition-matrix-from-counts.es.md), usa 0.05. (a) Calcule ambas para n = 11. (b) Un conjunto nuevo se detecta por completo. ¿De qué tamaño tiene que ser para que la cota inferior llegue al corte «healthy», 0.9?

> **Respuesta:** (a) `0.025^(1/11) = 0.715`: 0 de 11 da una cota superior de `1 − 0.715 = 0.285`, y 11 de 11 una cota inferior de 0.715, todavía en «watch». (b) La cota llega a 0.9 cuando `0.9^n ≤ 0.025`. `0.9^35 = 0.02503` es demasiado grande y `0.9^36 = 0.02253` es lo bastante pequeño: 36 inyecciones, todas detectadas.

## 3. Poner a prueba cada escalón y luego contar las pruebas

**Calculado.** La *prueba exacta de Fisher* compara dos recuentos como dos muestras independientes. Fijemos los márgenes: 11 ensayos por ciclo, y el total detectado en los dos. Si los ciclos comparten una sola tasa, todas las formas de colocar esas detecciones entre los 22 ensayos son igual de probables. El *valor p* que se usa aquí es bilateral: la probabilidad total de todas las tablas no más probables que la observada. El valor unilateral (el ciclo posterior es el más alto) es la mitad en el primer escalón.

| Ciclos comparados (recuentos) | p bilateral |
|---|---|
| 1 contra 2 (0/11, 7/11) | 0.0039 |
| 2 contra 3 (7/11, 8/11) | 1 |
| 3 contra 4 (8/11, 9/11) | 1 |
| 1 contra 4 (0/11, 9/11) | 0.0002 |

**Cuatro pruebas sobre cuatro números.** Cuatro pruebas independientes al nivel del 5% dan al menos un falso positivo (un p por debajo de 0.05 cuando nada difiere) el 18.5% de las veces (`1 − 0.95^4`). La *corrección de Bonferroni* compara cada p con `0.05 / 4 = 0.0125` y se cumple sea cual sea la dependencia entre pruebas. Aquí las pruebas comparten recuentos, y una prueba exacta sobre 11 ensayos es conservadora: sobre todas las formas de colocar las 24 detecciones registradas entre los 44 ensayos, una prueba sola cae por debajo de 0.05 en el 1.78% de las disposiciones y al menos una de las cuatro en el 6.2%. La corrección no cambia ningún veredicto de la tabla, pero decide otras dos lecturas:

- **El diseño es emparejado.** Se vuelven a puntuar las mismas inyecciones, así que la prueba que corresponde es la *prueba exacta de los signos* (la prueba de McNemar en forma exacta): si nada cambió, una inyección cuyo resultado difiere tiene la misma probabilidad de haberse movido en un sentido que en el otro. Del ciclo 1 al ciclo 2, siete ganancias y ninguna pérdida dan un p bilateral de `2 × (1/2)^7 = 0.0156`, por encima de 0.0125 (seis ganancias, según las etiquetas de estado: 0.031).
- **El recuento del ciclo 2.** Con 6 en lugar de 7, el p de Fisher es 0.0124; con 5 es 0.035.

**¿Un escalón o tres?** Para los tres últimos ciclos, una prueba exacta de «una sola tasa común» (Freeman–Halton) da p = 0.88 y una prueba exacta de tendencia unilateral (Cochran–Armitage, puntuaciones 0, 1, 2) da p = 0.24. Tres ciclos independientes de 11 ensayos a su tasa agrupada, 8/11, crecen estrictamente en el 8.5% de los casos. La política etiqueta un ciclo como «improving» cuando su R supera la media de los dos anteriores; en ciclos así esa regla dice «improving» el 45% de las veces, y dos veces seguidas el 18%.

Con los recuentos registrados y la prueba de Fisher, el primer escalón es el único que se distingue del azar (en la prueba emparejada pasa con tres comparaciones y falla con cuatro); los dos escalones posteriores no, bajo ninguna de las lecturas anteriores.

### Ejercicio práctico 3

Calcule a mano el valor p unilateral de Fisher del ciclo 1 al ciclo 2, y luego el bilateral.

> **Respuesta:** Con 7 detecciones entre 22 ensayos y ninguna en el ciclo 1, los 11 ensayos del ciclo 1 vienen todos de las 15 no detectadas: `C(15,11) / C(22,11) = 1,365 / 705,432 = 0.0019`. La tabla espejo (7 y luego 0) es igual de probable y ninguna otra tabla es tan improbable, así que el valor bilateral es el doble: 0.0039.

### Ejercicio práctico 4

Del ciclo 2 al ciclo 3 las etiquetas de estado muestran dos inyecciones que pasan de no detectadas a detectadas, y ninguna en sentido contrario. Dé el valor p bilateral de la prueba de los signos. Decida después si el valor p emparejado del primer escalón sobrevive a una corrección de Bonferroni para tres pruebas (los escalones consecutivos) y para cuatro (añadiendo el primero contra el último).

> **Respuesta:** `2 × (1/2)^2 = 0.5`: ninguna evidencia de cambio. Primer escalón: `2 × (1/2)^7 = 1/64 = 0.0156`. Con tres pruebas el umbral es `0.05 / 3 = 0.0167` y el escalón pasa; con cuatro es 0.0125 y el escalón falla. El veredicto depende de cuántas comparaciones admita haber hecho.

## 4. Qué mide un conjunto de inyecciones reutilizado

**Observado.** Cada registro posterior dice qué se construyó antes de puntuarlo. `chaos-002`: tres detecciones implementadas en un analizador sintáctico, tras lo cual seis inyecciones nombran una sola función, `analyzeLolli()`, como su detector. `chaos-003`: dos correcciones en el nivel de la política, y las dos inyecciones de política cambian de estado. `chaos-004`: dos correcciones en el nivel del esquema, una de ellas un archivo de prueba «including injection #10 regression test», y la inyección 10, el esquema sin referencias, es la que cambia. Ninguna inyección vuelve de detectada a no detectada.

A partir del ciclo 2, R sobre este conjunto cuenta por tanto cuántos de los once defectos conocidos tienen ya un detector o una regla escrita: una medida de avance sólida para una lista de reparaciones, pero no la tasa de detección sobre defectos que nadie ha plantado todavía, que es lo que sugiere el nombre «resiliencia». **Analogía:** un modelo ajustado contra su propio conjunto de prueba mantiene una puntuación que sube y que ya no estima su rendimiento sobre datos nuevos (Dwork et al. 2015).

**Sintético** (no existe ningún conjunto así). Un *conjunto reservado*, escrito por alguien que no ha leído las correcciones y puntuado una sola vez antes de cualquier reparación, estimaría esa tasa. Con 11 inyecciones reservadas, una prueba bilateral de Fisher contra 9/11 solo cae por debajo de 0.05 con 3 detectadas o menos (p = 0.030; 4 detectadas dan 0.080).

**La objeción más fuerte a esta lección** es que su modelo de azar no se ajusta ni al conjunto ni a la puntuación. Las inyecciones no se muestrearon; un estado registra si existe un detector, no una ejecución con ruido; y las inyecciones se mueven juntas: las puntuaciones de nivel valen 0 o 1 en todos los ciclos menos uno. Con los 7 niveles como unidades (0, 2, 4, 5 puntuados por completo), el primer escalón tiene p = 0.46 y el primero contra el último 0.021, por encima de 0.0125. La referencia también se mueve: con el 5/11 del informe en lugar de 0, el ciclo 2 da p = 0.67 y el ciclo 4 da 0.18. **Este registro no permite distinguir un salto en la detección de un cambio en lo que se contaba como detectado.** La siguiente comprobación lo zanjaría.

### Ejercicio práctico 5

Sintético. Un quinto ciclo registra 11 detectadas de 11 sobre el mismo conjunto, y la línea de estado dice R = 1.00, «healthy». Un colega escribe después 11 inyecciones nuevas sin leer las correcciones; 4 se detectan. (a) ¿Qué establece el 1.00? (b) ¿Difiere el 4/11 del último 9/11 registrado? Enuncie su criterio.

> **Respuesta:** (a) Que los once defectos conocidos tienen ya todos un detector o una regla, no qué les ocurre a los defectos nuevos; incluso leído como una muestra nueva, 11 de 11 deja tasas de hasta 0.715. (b) Criterio: un p bilateral de Fisher por debajo de 0.05. 4/11 contra 9/11 da 0.080, así que los dos no se distinguen; 3/11 daría 0.030.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cuatro archivos de [`state/resilience/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience), los dos informes, la política de la métrica, el glosario, la línea del README y los tres archivos de inyección. `extract.py` se niega a ejecutarse si alguno difiere de su blob fijado o si la carpeta gana un archivo.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py` y luego `analyze.py` en la misma carpeta. El [README](../../../fixtures/psychohistory/psy-013/README.md) enumera las autocomprobaciones y los controles negativos, y [`scenarios.json`](../../../fixtures/psychohistory/psy-013/scenarios.json) las decisiones de análisis.

**Referencias de método.** Clopper, C. J., y Pearson, E. S. (1934), «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial», *Biometrika* 26(4), 404–413. Dunn, O. J. (1961), «Multiple Comparisons Among Means», *Journal of the American Statistical Association* 56, 52–64 (la corrección de Bonferroni). Agresti, A. (2013), *Categorical Data Analysis*, tercera edición, Wiley (las pruebas exactas, la prueba de McNemar). Dwork, C., y cinco coautores (2015), «The Reusable Holdout: Preserving Validity in Adaptive Data Analysis», *Science* 349, 636–638.

**No realizado.** No se volvió a ejecutar ninguna inyección, y el analizador sintáctico que nombran los registros ([`Parser.fs`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/tools/ixql-parser/IxqlParser/Parser.fs), en este repositorio) no se compiló ni se ejecutó: el fixture solo lee los registros. No existe ningún conjunto reservado. Las cuatro comparaciones se eligieron después de conocer las cuatro puntuaciones. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Escribir la regla de puntuación, aplicarla a los once veredictos del primer informe y a cada ciclo, y puntuar una sola vez un conjunto reservado. Si la regla sitúa la referencia cerca de 5/11, la conclusión pasa de «un escalón grande y luego una meseta» a «ningún escalón distinguible». Por separado, compilar el analizador sintáctico y aplicar `analyzeLolli` a `pipelines/chaos-test.ixql`: los registros le acreditan seis inyecciones.
