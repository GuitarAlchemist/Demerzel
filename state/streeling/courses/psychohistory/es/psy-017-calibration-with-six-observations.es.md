---
module_id: psy-017-calibration-with-six-observations
department: psychohistory
course: "Calibración con seis observaciones"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-017
version: "0.1.0"
---

# Calibración con seis observaciones

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo rastreará un registro de calibración hasta los archivos que hay detrás de sus recuentos, pondrá un intervalo exacto a una proporción sobre seis, calculará con qué frecuencia un pronosticador calibrado muestra el mismo recuento, hallará el tamaño muestral que separa dos tasas y seguirá una regla de corrección alimentada con seis observaciones cada vez. **Pregunta de proyecto:** un archivo de creencias registra que 2 de 6 creencias de alta confianza se revisaron más tarde, y desplaza un umbral en −0.1. ¿Qué pueden decir seis observaciones sobre la calibración?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) incluye la asimetría de las creencias entre seis señales de un cambio de régimen que se avecina; este módulo se pregunta cuánto puede sostener un único recuento pequeño sobre creencias. [PSY-004](psy-004-how-large-is-large.es.md) construye el intervalo exacto que se reutiliza aquí, [PSY-016](psy-016-brier-score.es.md) puntúa pronósticos probabilísticos con la puntuación de Brier y [PSY-025](psy-025-capstone-preregistered-forecast.es.md) usa ambos.

## 1. Leer el registro y después volver a contarlo

**Observado.** Un *archivo de creencias* de `state/beliefs/` contiene una proposición, un valor de verdad (T verdadero, P probable, U desconocido, D dudoso, F falso, C contradictorio) y una `confidence` (confianza) entre 0 y 1. En el commit `4b03838`, la carpeta contiene ocho archivos `*.belief.json` (más una lista YAML de 19 creencias, 9 de ellas con 0.85 o más, que el patrón *glob* del productor pasa por alto) y [`archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/archived), trece más. Esta lección se apoya en uno, [`confidence-calibration.belief.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/confidence-calibration.belief.json). Su proposición dice del agente de gobernanza: «confidence-assignment threshold is calibrated against the observed overconfidence-then-revision rate in her belief states.» (su umbral de asignación de confianza está calibrado frente a la tasa observada de exceso de confianza seguido de revisión en sus estados de creencia). Valor de verdad P, confianza 0.92, un elemento a favor, ninguno en contra. La afirmación (*claim*) de ese elemento, íntegra:

```text
2 of 6 high-confidence beliefs (>= 0.85) were later revised (overconfidence_rate=0.3333). Revisions evidenced by archived prior versions: 2026-03-17-consumer-repo-integration-status.belief.json, 2026-03-17-ga-governance-integration.belief.json. Nudge magnitude capped at +/-0.1/cycle per ml-governance-feedback-policy.
```

Un bloque `calibration` guarda `threshold_nudge` −0.1, `applied_delta` 0.0, `prior_nudge` −0.1 y `cap` 0.1. El archivo no dice qué seis creencias se contaron, qué umbral mueve el ajuste (*nudge*) ni si una creencia revisada era errónea.

**De dónde procede el registro.** El agente de gobernanza no calculó estos números: su *script de aplicación*, [`scripts/apply_ml_feedback.py`, líneas 130–154](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py#L130-L154), escribe la creencia con una proposición fija y una etiqueta fija, P (con el comentario «Probable: evidence leans true, magnitude still small-N», es decir, la evidencia se inclina hacia lo verdadero, pero la magnitud aún descansa sobre una N pequeña), y copia la confianza, la afirmación y la fiabilidad de la afirmación de un documento de recomendación, que un productor de otro repositorio (`ix/scripts/confidence_calibrator.py`, nombrado en la cabecera del script) calcula a partir de estos mismos archivos de creencias.

Tres archivos fijados enuncian la regla. La [política](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/ml-governance-feedback-policy.yaml#L57) define la tasa como «Proportion of high-confidence beliefs that were later revised» (proporción de creencias de alta confianza que se revisaron más tarde). La [especificación del *pipeline*](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/ml-feedback-loop.ixql#L41) recomienda un cambio cuando la tasa supera 0.15, de tamaño `max(-0.1, -1 * overconfidence_rate * 0.5)`. El script de aplicación (línea 128) suma ese ajuste al total almacenado y limita el total a ±0.10.

**Calculado.** Ese productor ([`confidence_calibrator.py`](https://github.com/GuitarAlchemist/ix/blob/6418fcc69012108af266544ec4cf5a931a8f78e8/scripts/confidence_calibrator.py), leído en el commit `6418fcc` de ix, fuera del *fixture*) cuenta según esta regla: todo archivo de creencias, actual o archivado, con una confianza de al menos 0.85 es «de alta confianza» (*high-confidence*), y los archivados entre ellos son «revisados» (*revised*). [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-017/extract.py) toma una instantánea de los 21 archivos de creencias fijados y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-017/observed-input.json), y [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-017/analyze.py) les aplica esa regla:

| Archivo de creencias | Valor de verdad | Confianza | Grupo |
|---|---|---|---|
| `2026-03-18-consumer-repo-integration-status` | P | 0.85 | actual |
| `2026-07-25-schema-conformance` | T | 0.95 | actual |
| `confidence-calibration` | P | 0.92 | actual |
| `remediation-effectiveness` | P | 0.90 | actual |
| `2026-03-17-consumer-repo-integration-status` | F | 0.90 | archivado: revisado |
| `2026-03-17-ga-governance-integration` | F | 0.85 | archivado: revisado |

Cuatro archivos actuales y dos archivados suman seis, los dos archivados son los que nombra la afirmación, y la frase reconstruida a partir del recuento es idéntica a la registrada ([`results.json`](../../../fixtures/psychohistory/psy-017/results.json), `recount`): un cálculo reproducido, no una segunda fuente. Los otros cuatro archivos actuales tienen 0.80 o 0.82; los otros once archivados, 0.5 o 0; y las nueve creencias del archivo YAML no se cuentan nunca.

El registro se cuenta a sí mismo: su propio 0.92 lo sitúa entre los seis. Tanto él como `remediation-effectiveness` los escribe el script de aplicación, con confianzas copiadas de recomendaciones; sin esos dos, la misma regla da 2 de 4. Tampoco se actualizaron los seis por última vez en momentos comparables: los dos archivados, 209.7 y 209.6 días antes del registro; los cuatro actuales, 31.5, 30.5, 0 y 0 días antes.

### Ejercicio práctico 1

A partir de la tasa registrada y de `prior_nudge`, reproduzca `threshold_nudge` y `applied_delta` con las dos fórmulas fijadas.

> **Respuesta:** `−0.5 × 2/6 = −0.1667`, que la fórmula limita a −0.1. Total almacenado: `−0.1 + (−0.1) = −0.2`, recortado a −0.1, así que `threshold_nudge = −0.1` y `applied_delta = −0.1 − (−0.1) = 0.0`. El total ya estaba en su límite: esta ejecución no cambió nada.

## 2. Lo que permite un recuento de seis

Un pronosticador está *calibrado* cuando, entre las afirmaciones hechas con confianza c, resulta verdadera una proporción c. Esta lección añade una lectura propia, que el repositorio no enuncia: toda revisión es un error. Las creencias sostenidas con 0.85 o más deberían entonces revisarse como mucho el 15% de las veces; el disparador del *pipeline* es ese mismo 0.15.

Trate las seis como ensayos independientes con una única tasa de revisión desconocida. El *intervalo exacto al 95%* (bilateral; de Clopper y Pearson; PSY-004 muestra su construcción) conserva todas las tasas bajo las cuales el recuento observado no cae en ninguna de las dos colas del 2.5%. **Calculado:** para 2 de 6 va de **0.0433 a 0.7772**, y contiene el 15%, el 10% y el 5%.

¿Con qué frecuencia muestra dos o más revisiones entre seis un pronosticador cuya tasa se conoce? **Calculado con tasas supuestas** ([`scenarios.json`](../../../fixtures/psychohistory/psy-017/scenarios.json)), porcentajes redondeados a dos decimales:

| Pronosticador supuesto | Tasa de revisión verdadera | P(2 o más de 6) |
|---|---|---|
| Calibrado en 0.95 | 5% | 3.28% |
| Calibrado en 0.90 | 10% | 11.43% |
| Calibrado en 0.85 | 15% | 22.35% |
| Según lo registrado | un tercio | 64.88% |

Un pronosticador calibrado exactamente en el umbral muestra el recuento registrado, o uno peor, más de una vez de cada cinco. El *cociente de verosimilitudes* compara la probabilidad de exactamente 2 de 6 bajo dos tasas: 0.329218 con un tercio frente a 0.176177 con el 15%, un cociente de 1.87. **Esta muestra no permite distinguir un pronosticador calibrado de uno con exceso de confianza.**

### Ejercicio práctico 2

Calcule la probabilidad de dos o más revisiones entre seis para una tasa verdadera del 15%.

> **Respuesta:** `P(0) = 0.85^6 = 0.377150` y `P(1) = 6 × 0.15 × 0.85^5 = 0.399335`, así que `P(2 or more) = 1 − 0.377150 − 0.399335 = 0.2235` con cuatro decimales.

### Ejercicio práctico 3

Un colega dice: «Un tercio es más del doble del 15%, así que el pronosticador tiene claramente un exceso de confianza». ¿El registro respalda esa afirmación, la refuta o la deja sin decidir? Dé dos números.

> **Respuesta:** Sin decidir. El intervalo exacto, de 0.0433 a 0.7772, contiene el 15% e incluso el 5%, y la probabilidad de exactamente 2 de 6 con un tercio es solo 1.87 veces la que tiene con el 15%.

## 3. Cuántas observaciones separarían el 15% del 33%

Tome una regla: «declarar que el pronosticador tiene exceso de confianza cuando se revisan c o más de n creencias». Su tasa de *falsas alarmas* es la probabilidad de que un pronosticador calibrado (15%) la dispare; su tasa de *detección*, la probabilidad de que la dispare uno con exceso de confianza (un tercio). **Calculado** para n = 6:

| Regla | Falsa alarma | Detección |
|---|---|---|
| 1 o más de 6 | 62.29% | 91.22% |
| 2 o más de 6 | 22.35% | 64.88% |
| 3 o más de 6 | 4.73% | 31.96% |

Mantener las falsas alarmas por debajo del 5% obliga a esperar tres revisiones, y esa regla deja escapar a un pronosticador con exceso de confianza el 68.04% de las veces. El recuento registrado, 2, no la alcanza. La regla fijada se dispara desde la primera fila de la tabla: una revisión entre seis, una tasa de 0.1667, está por encima del disparador.

`analyze.py` explora todos los n hasta 400 con sumas binomiales exactas. La muestra más pequeña con una tasa de falsas alarmas del 5% como máximo y una detección de al menos el 80% es **33** («9 o más de 33»: 4.95% y 82.12%), 5.5 veces las seis. Si la tasa verdadera fuera del 25% en lugar de un tercio, el mismo diseño necesitaría 101.

### Ejercicio práctico 4

Suponga, solo para fijar una escala, que las creencias de alta confianza siguen registrándose al ritmo de las seis: seis en los 209.7 días que median entre la más antigua de ellas y el registro. ¿Cuántos días después de la más antigua de las seis llegaría la 33.ª, y cuántos después del registro?

> **Respuesta:** `33 × 209.7 / 6 ≈ 1,153` días después de la más antigua y, por tanto, `27 × 209.7 / 6 ≈ 944` días, unos 2.6 años, después del registro. El ritmo es un supuesto: las fechas son de última actualización, no de creación.

## 4. Una regla de corrección alimentada con seis observaciones

**Calculado a partir de la regla fijada.** Con seis creencias por ciclo, sin ninguna revisión el total almacenado no cambia; una revisión lo mueve en −0.0833, y dos o más, en −0.1. Un pronosticador calibrado con una tasa del 15% recibe un ajuste a la baja en el 62.29% de los ciclos; uno con una tasa del 5%, en el 26.49%; uno con exceso de confianza, en el 91.22%. Nada de lo registrado lo mueve hacia arriba: la rama ascendente de la especificación necesita una «underconfidence rate» (tasa de falta de confianza), y el archivo de creencias no contiene ninguna.

**Sintético.** Conceda a la regla su caso más favorable, seis creencias nuevas e independientes en cada ciclo, y siga exactamente el total almacenado (una simulación con semilla fija de 20,000 ejecuciones coincide con un margen de 0.0073):

| Después de | Calibrado (15%): total en −0.1 | Con exceso de confianza (un tercio): total en −0.1 |
|---|---|---|
| 1 ciclo | 22.35% | 64.88% |
| 4 ciclos | 89.41% | 99.92% |
| 13 ciclos | 99.9954% | 100.00% |

La política programa esta calibración cada semana, así que 13 ciclos son un trimestre. Para entonces, los dos pronosticadores están en −0.1: el valor almacenado es donde termina la regla para cualquiera de ellos, y no es ningún indicio de cuál de los dos está presente.

**Observado.** La ejecución registrada no es ese caso más favorable. `prior_nudge` vale −0.1 y `applied_delta` vale 0.0, y las dos revisiones que cita se actualizaron por última vez el 2026-03-17: esta ejecución volvió a leer evidencia antigua.

**Lo que mide una «revisión».** Las dos creencias archivadas llevan F: el 2026-03-17 juzgaron, con 0.90 y 0.85, que un paso de integración no se había producido. La [creencia actual sobre ese tema](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/2026-03-18-consumer-repo-integration-status.belief.json) cita trabajo fechado el 2026-03-18. Los archivos fijados muestran veredictos superados por los acontecimientos, y el [`SUPERSEDED.md`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/archived/SUPERSEDED.md) de la carpeta dice que las creencias archivadas «are retired, not deleted» (se retiran, no se borran); nada registra que alguno de los dos veredictos fuera erróneo cuando se escribió. En sentido contrario, el `refresh_note` de esa creencia actual registra «T -> F» el 2026-09-12 y «F -> P» el 2026-09-13, cambios editados en el propio archivo, que un recuento de creencias archivadas no puede ver. Si se cuenta también esa creencia, resultan 3 de 6.

**La confianza del propio registro.** El productor (citado, fuera del commit fijado) la fija con `min(0.92, 0.70 + 0.02 × belief files read)`, donde *belief files read* es el número de archivos de creencias leídos. Con 21 archivos se llega al tope, 0.92: la fórmula no usa ni el 2 ni el 6, y a partir de ocho archivos alcanza 0.85, el umbral (`CONF_AUTO_APPLY`) por debajo del cual el script de aplicación escala una recomendación en lugar de aplicarla. Así que el 0.92 no es un juicio sobre lo bien respaldada que está la afirmación, y la sección 2 dice lo que no puede significar: seis observaciones no respaldan ninguna afirmación sobre la tasa de revisión más estrecha que «entre el 4% y el 78%» con una confianza del 95%.

**La objeción más fuerte a esta lectura** es bayesiana. Con una distribución a priori uniforme para la tasa, la probabilidad de que supere el 15% es 0.926235 tras 2 de 6. Pero esa distribución a priori ya da 0.85 antes de cualquier dato, así que las seis observaciones añaden 0.076; y la objeción hereda los defectos del recuento. Lo que lo zanjaría: un resultado, acierto o error comprobado tras un plazo fijo, para al menos 33 creencias de alta confianza que no escriba el script de aplicación.

### Ejercicio práctico 5

(a) Para el pronosticador calibrado de la tabla, calcule la probabilidad de que el total almacenado siga en 0 después de 4 ciclos. (b) ¿Debe leerse un −0.1 almacenado como un indicio de exceso de confianza? Enuncie su criterio.

> **Respuesta:** (a) Ninguna revisión en cuatro muestras de seis: `0.377150^4 = 0.020233`, alrededor del 2%. (b) No. Una observación es un indicio a favor de una hipótesis frente a otra solo si es claramente más probable bajo la primera. Después de 4 ciclos, un total de −0.1 tiene una probabilidad del 99.92% para el pronosticador con exceso de confianza y del 89.41% para el calibrado, un cociente de `0.9992 / 0.8941 = 1.12`; después de 13 ciclos, el cociente es 1.00. Los dos pronosticadores son sintéticos.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** la creencia de calibración, los otros veinte archivos de creencias, la lista de creencias YAML, el `SUPERSEDED.md` de las creencias archivadas, la política, la especificación del *pipeline* y el script de aplicación enlazados más arriba.

**Fixture.** El [README](../../../fixtures/psychohistory/psy-017/README.md) da los comandos, las 32 autocomprobaciones y los controles negativos.

**Referencias de método.** Clopper, C. J., y Pearson, E. S. (1934), «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial», *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404). Lichtenstein, S., Fischhoff, B., y Phillips, L. D. (1982), «Calibration of probabilities: The state of the art to 1980», en Kahneman, D., Slovic, P., y Tversky, A. (eds.), *Judgment under Uncertainty: Heuristics and Biases*, Cambridge University Press, 306–334.

**No realizado.** No se leyó el historial de Git de la creencia de calibración, así que se desconoce el número de ciclos ya aplicados. No se rastreó si algún proceso lee el ajuste almacenado y mueve un umbral. El documento de recomendación que cita la creencia es un archivo generado en tiempo de ejecución que el repositorio no conserva, y no consta qué versión del productor de ix lo escribió. Toda probabilidad supone creencias independientes con una única tasa, y las seis no lo son; las cifras son el caso más favorable para los datos. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Leer el historial de `state/beliefs/` para contar los ciclos y ver si las seis cambiaron alguna vez. Si cada ciclo volvió a leer las mismas dos creencias archivadas, la conclusión se precisa: pasa de «seis observaciones no permiten decidir» a «un único recuento de seis, aplicado muchas veces».
