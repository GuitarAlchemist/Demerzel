---
module_id: psy-021-conservation-claims
department: psychohistory
course: "Enunciados de conservación que se pueden comprobar"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-021
version: "0.1.0"
---

# Enunciados de conservación que se pueden comprobar

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo clasificará en cuatro tipos los enunciados a los que se llama «de conservación», auditará una identidad de existencias y flujos sobre un registro de eventos real y nombrará el registro que necesita una afirmación para poder fallar. **Pregunta de proyecto:** PSY-001 toma prestado el teorema de Noether para el «impulso de aprendizaje». ¿Qué enunciados de conservación sobre este proyecto pueden comprobarse realmente?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) anuncia una ley de conservación para la gobernanza. Este módulo se pregunta qué exige una ley así y audita después lo más parecido que ofrece el repositorio: la contabilidad de su registro de disparadores. [PSY-008](psy-008-bursts-are-not-rates.es.md) y [PSY-009](psy-009-concentration-and-heavy-tails.es.md) leen ese registro como llegadas, [PSY-024](psy-024-the-single-actor.es.md) se pregunta quién las envió, y [PSY-003](psy-003-review-throughput-and-compounding.es.md) aplica identidades parecidas a las colas de revisión.

## 1. Cuatro cosas a las que se llama conservación

En física, una ley de conservación dice que un número calculado a partir del estado de un sistema aislado conserva su valor mientras el estado cambia: la energía, la cantidad de movimiento, la carga eléctrica. El teorema de Noether (1918) es una de las fuentes de esas leyes. Se refiere a un sistema cuyos movimientos hacen estacionaria una *acción*, un único número calculado a partir de toda la historia del sistema. Si una familia continua de transformaciones (desplazar cada instante en la misma cantidad, sea cual sea esa cantidad) deja la acción sin cambios, el teorema construye una magnitud que permanece constante a lo largo de todo movimiento: la energía para los desplazamientos en el tiempo, la cantidad de movimiento para los desplazamientos en el espacio. Nadie elige la magnitud: se deduce.

**Observado.** [La sección 5 de PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md#L112) enuncia el teorema como «every continuous symmetry of a system has a corresponding conserved quantity» (toda simetría continua de un sistema tiene una magnitud conservada correspondiente) y lo aplica: «In fractal compounding, the symmetry is **scale invariance** — the compound operation has the same shape at every level. The conserved quantity is **learning momentum (p_L)**» (en el compuesto fractal, la simetría es la invariancia de escala, y la magnitud conservada, el impulso de aprendizaje), con

```text
p_L = (beliefs_gained_T - beliefs_lost_T) / cycles_elapsed
```

y «If your compounding process is consistent (symmetric across scales), p_L stays constant or grows. If you break the symmetry — by skipping compounding at some level, or by compounding differently at different scales — p_L decays.» (si el proceso de compuesto es consistente, p_L se mantiene constante o crece; si se rompe la simetría, p_L decae).

**Esto es una analogía.** Su intuición es razonable: un proceso que se ejecuta de la misma manera en cada nivel debería seguir produciendo creencias validadas. Pero no se cumplen las condiciones del teorema (es la lectura del autor, registrada en [`scenarios.json`](../../../fixtures/psychohistory/psy-021/scenarios.json)). No se ha escrito ninguna acción para los ciclos de gobernanza. La simetría une cinco niveles con nombre (paso, pipeline, ciclo, sesión, evolución): una correspondencia discreta, no una familia continua. Y p_L se define mediante una fórmula y puede crecer, cosa que una magnitud conservada no puede hacer.

Un proyecto sí tiene enunciados de conservación que puede comprobar: las identidades contables de unas *existencias* (*stock*), la cantidad de algo presente en un momento dado (Meadows 2008).

```text
existencias ahora = todo lo que entró - todo lo que salió
```

Lo que vale un enunciado así depende de si los registros habrían podido hacerlo falso. Este módulo usa cuatro etiquetas:

- **por construcción**: verdadero digan lo que digan los registros, por aritmética o por la manera en que se obtienen sus lados (a menudo los dos proceden de los mismos registros); no dice nada sobre el sistema;
- **auditable**: los registros habrían podido hacerlo falso, a menudo porque sus lados se escribieron por separado;
- **no registrado**: una de las magnitudes nunca se anotó;
- **analogía**: el vocabulario de una ley sin sus condiciones.

## 2. Lo que pueden cuadrar los archivos del commit fijado

**Observado.** Un *disparador* (*trigger*) es un pequeño archivo JSON que un [flujo de trabajo de GitHub](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) escribía en `state/triggers/` por cada *push*, incidencia abierta o discusión creada, para que lo consumiera un agente autónomo, el *driver*. Ambos se retiraron el 2026-07-18; el archivo enlazado es una versión posterior. Las incidencias reabiertas y las ejecuciones de CI fallidas que también contempla no aparecen nunca en el historial. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-021/extract.py) toma una instantánea de [la carpeta](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers) en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-021/observed-input.json): 603 archivos de eventos.

| Tipo | Pendientes | Archivados | Total |
|---|---|---|---|
| discussion_created | 5 | 252 | 257 |
| issue_opened | 3 | 135 | 138 |
| push | 0 | 207 | 207 |
| research_followup | 1 | 0 | 1 |
| Total | 9 | 594 | 603 |

«Pendientes» significa que siguen en el propio `state/triggers/`; «archivados», que están en su subcarpeta `archived/`; la tercera carpeta, `processing/`, está vacía. De los 603 archivos, 602 comparten una misma forma: seis claves (`type`, `repo`, `ref`, `priority`, `details`, `timestamp`), con `event`, `sender` y `run_id` (el identificador único de la ejecución del flujo de trabajo) dentro de `details`. Ninguna clave registra un momento de archivado, un paso de procesamiento ni un resultado: un disparador que se procesó y otro que se abandonó tienen el mismo aspecto.

**Calculado** solo a partir de estos archivos por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-021/analyze.py), con resultados en [`results.json`](../../../fixtures/psychohistory/psy-021/results.json):

- *Por construcción:* los totales por tipo suman 603: un mismo recuento, repartido y vuelto a sumar.
- *Auditable, y se cumple:* 603 nombres de archivo, todos distintos, así que ningún archivo está en dos carpetas; 602 identificadores de ejecución, todos distintos; y el archivo del flujo de trabajo y el archivo de habilidad del driver declaran los dos 594 disparadores huérfanos, que es lo que contiene la carpeta de archivados.
- *No registrado:* las carpetas sugieren un circuito cerrado, `created = archived + pending + in processing`, pero nada en el commit fijado cuenta lo que se creó: la identidad no tiene lado izquierdo. La [propia regla](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md#L331) del driver explica por qué: «On WAKE: move triggers to `state/triggers/processing/` before reading, delete after processing.» (al despertar, mover los disparadores a la carpeta de procesamiento antes de leerlos, y borrarlos después de procesarlos). La salida prevista no deja ningún archivo.

### Ejercicio práctico 1

A partir de la tabla, calcule el número de archivos de eventos por carpeta y por tipo. Después, encuentre la suma de esta sección que habría podido discrepar de un número escrito con independencia de los archivos.

> **Respuesta:** Por carpeta, `9 + 0 + 594 = 603`; por tipo, `257 + 138 + 207 + 1 = 603`. Estas no pueden discrepar: las dos vuelven a sumar un mismo recuento. La columna de archivados sí puede: `252 + 135 + 207 = 594` se cuenta a partir de los archivos, y 594 se declara además en dos documentos. Coinciden.

### Ejercicio práctico 2

Asigne a cada enunciado una de las cuatro etiquetas: (a) «ningún identificador de ejecución aparece en dos archivos»; (b) «todo disparador archivado se procesó»; (c) «los recuentos por tipo suman el número de archivos»; (d) «el impulso de aprendizaje se conserva».

> **Respuesta:** (a) Auditable: un archivo copiado habría repetido un identificador; se cumple, 602 distintos de 602. (b) No registrado: ninguna clave registra el procesamiento. (c) Por construcción. (d) Analogía: faltan las condiciones del teorema.

## 3. El historial aporta el lado que faltaba, y la identidad falla

**Observado, a partir del historial.** `extract.py` lee también el historial de Git del commit fijado: a lo largo de la *cadena de primeros padres* (la *first-parent chain*, es decir, los sucesivos estados de la rama principal: 1,528 commits, 623 de los cuales tocan la carpeta) enumera cada adición y cada borrado de un archivo de disparador.

| Carpeta | Añadidos | Borrados | Añadidos − borrados | En disco |
|---|---|---|---|---|
| pendientes | 615 | 606 | 9 | 9 |
| en procesamiento | 5 | 5 | 0 | 0 |
| archivados | 594 | 0 | 594 | 594 |

Así que se crearon 615 archivos de disparadores, y la identidad cerrada tiene un lado izquierdo. **Falla:** 615 frente a 594 + 9 + 0 = 603. Doce archivos, el 1.95% de los creados, no están en ninguna carpeta:

- 2 borrados de los pendientes por `c5cca0c` y `49a573c`, cada uno de los cuales elimina un «trigger file with invalid Windows filename» (archivo de disparador con un nombre no válido en Windows);
- 5 borrados de `processing/` por `2b752a7`, «Driver cycle 002 complete — 9 tasks, all repos healthy»;
- 5 borrados de los pendientes por `a2c1ef0`, «docs(seldon): Markov + state-space model architecture and schemas (#605)».

Los cinco borrados de `processing/` tomaron la salida prevista: el commit que los trasladó allí dice «consume 5 triggers», y ningún otro disparador se trasladó nunca allí; los otros siete salieron por otras puertas. Y «594 orphans» (huérfanos) es el tamaño de la carpeta de archivados, no el número de disparadores que nadie consumió: 615 − 5 = 610 no se consumieron nunca (609 escritos por el productor): 594 archivados, 9 pendientes y 7 eliminados.

Con un término de *eliminados*, las cuentas cuadran: 615 = 603 + 12, cada carpeta queda equilibrada y, nombre por nombre, los 603 archivos están donde los deja el historial. **Ese cierre es por construcción.** Git guarda instantáneas y calcula las adiciones y los borrados comparando instantáneas consecutivas; sumar las diferencias devuelve la última instantánea, que son los archivos. El cierre muestra que el historial se leyó por completo (un control negativo que suprime un registro de borrado descuadra las cuentas en uno), y nada sobre los disparadores. Dos resultados habrían podido salir de otra manera: los 12, y la correspondencia entre los 613 asuntos de commit que anuncian un disparador y los archivos que añadieron sus commits, uno del tipo anunciado en cada caso. El asunto y el tipo de archivo proceden los dos de una misma variable de un mismo paso del flujo de trabajo, así que esto solo muestra que cada ejecución hizo commit de su propio archivo. Los otros dos archivos llegaron con un commit que informaba del primer ciclo autónomo del driver y con un commit de investigación.

### Ejercicio práctico 3

Desglose los 606 borrados de la carpeta de pendientes. Calcule después la discrepancia del sistema cerrado y la proporción de los archivos creados que contiene la carpeta de archivados.

> **Respuesta:** `5` trasladados a `processing/`, `594` trasladados a `archived/` y `2 + 5 = 7` borrados sin más: `5 + 594 + 7 = 606`. Discrepancia: `615 − 603 = 12`. Proporción archivada: `594 / 615 = 96.59%`.

**Sintético.** Donde un registro y una estantería se cuentan por separado, como en un almacén, el propio cuadre de cuentas puede fallar. `scenarios.json` contiene cinco casos escritos a mano, de ocho eventos imaginarios cada uno, con las respuestas fijadas de antemano:

| Caso | Creados − listados | Lo mismo, menos las eliminaciones registradas | Carpetas descuadradas | Elementos fuera de lugar |
|---|---|---|---|---|
| limpio | 0 | 0 | 0 | 0 |
| eliminación registrada | 1 | 0 | 0 | 0 |
| pérdida sin registrar | 1 | 1 | 1 | 1 |
| copia sin registrar | −1 | −1 | 1 | 1 |
| pérdida y copia a la vez | 0 | 0 | 0 | 2 |

### Ejercicio práctico 4

Un panel muestra solo las tres primeras columnas, y todas marcan 0. ¿Qué casos deja abiertos, y qué comprobación los separa?

> **Respuesta:** Dos: el caso limpio, y una pérdida y una copia que se compensan. Solo la comparación nombre por nombre los separa: en el último caso, un evento se espera en la carpeta de archivados y falta, y otro aparece en dos carpetas. Unos recuentos que cuadran muestran el error neto, no el número de errores.

## 4. Convertir la analogía en una afirmación que pueda fallar

**Observado.** La [política que define p_L](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/compounding-metrics-policy.yaml#L124-L131) dice dónde se sigue: «state/driver/health-scores.json trend fields» (los campos de tendencia de ese archivo). En el commit fijado, [ese archivo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/health-scores.json) contiene, para cada uno de cuatro repositorios, una puntuación compuesta, una fecha y una tendencia de una sola palabra: 0 valores de p_L, y ningún recuento de creencias. La misma política lee p_L de tres maneras: constante, «symmetry preserved» (simetría preservada); creciente, «healthy compounding» (compuesto saludable); decreciente, «symmetry broken; investigate root cause» (simetría rota; investigar la causa raíz).

Una afirmación solo dice algo a través de los resultados que prohíbe (Popper 1959). Entre dos ciclos, p_L puede bajar, mantenerse o subir. La conservación estricta prohíbe dos de los tres. La primera frase de PSY-001 prohíbe uno, una bajada mientras el proceso es consistente, siempre que la consistencia se registre sin mirar p_L; la segunda prohíbe otro, la ausencia de decaimiento tras una ruptura registrada. La lectura en tres casos no prohíbe ninguno: la propia bajada se toma como señal de que la simetría se rompió.

### Ejercicio práctico 5

Sintético. Seis ciclos imaginarios ganaron 6, 7, 5, 4, 6, 6 creencias validadas y perdieron 1, 2, 2, 3, 1, 1. Un registro aparte dice que la fase de compuesto se ejecutó en los cinco niveles en todos los ciclos salvo el cuarto. Calcule p_L por ciclo (cycles_elapsed = 1) y ponga a prueba las tres versiones.

> **Respuesta:** p_L = 5, 5, 3, 1, 5, 5. *Conservación:* p_L cambia en 3 de los 5 pasos: refutada. *Primera frase de PSY-001:* 3 pasos unen dos ciclos consistentes (de 1 a 2, de 2 a 3, de 5 a 6) y p_L baja en uno, de 2 a 3: refutada. *Lectura en tres casos:* los pasos se etiquetan estable, en descenso, en descenso, en aumento, estable; nada la contradice, y ninguna serie podría hacerlo. La serie es inventada; el registro que hace comprobable la afirmación es un registro de consistencia llevado aparte de p_L.

**La objeción más fuerte a la lectura de esta lección** es que su lado izquierdo tampoco es la producción. «Creado» significa «incluido en un commit»: el flujo de trabajo del commit fijado [escribe un archivo y después hace *pull* y *push*](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L82-L90), y una ejecución cuyo *push* falló no dejó nada en el repositorio. El 615 y el 12 son cotas inferiores. **Este historial no permite distinguir un flujo de trabajo que nunca perdió un evento de otro que perdió eventos antes de que llegaran a un commit.** La lista de ejecuciones del flujo de trabajo en GitHub lo zanjaría.

## Fuentes, límites y próxima comprobación

**Observado** en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`: `state/triggers/` (comprobada por su identificador de árbol de Git), su historial de Git y los cinco archivos enlazados más arriba.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-021/extract.py`, y después `analyze.py` en la misma carpeta; `analyze.py --check` compara una ejecución nueva con los resultados guardados. El [README](../../../fixtures/psychohistory/psy-021/README.md) da un recuento sin los scripts.

**Referencias de método.** Noether, E. (1918), «Invariante Variationsprobleme», *Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 235–257 ([EuDML](https://eudml.org/doc/59024)); traducción al inglés de M. A. Tavel, *Transport Theory and Statistical Physics* 1(3), 1971, doi:10.1080/00411457108231446. Meadows, D. H. (2008), *Thinking in Systems: A Primer*, Chelsea Green. Popper, K. (1959), *The Logic of Scientific Discovery*, Hutchinson. Chacon, S., y Straub, B. (2014), *Pro Git*, segunda edición, Apress, [«What is Git?»](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F).

**No realizado.** No se leyó el contenido de los doce archivos borrados: sus tipos y fechas proceden de sus nombres, y los motivos de su borrado, de los asuntos de los commits. No se leyeron ni la lista de ejecuciones del flujo de trabajo ni sus versiones anteriores. No se calculó ningún valor de p_L a partir de datos del proyecto: el archivo designado para ello no contiene ninguno, y no se buscó en ninguna otra fuente. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** En GitHub, contar las ejecuciones del flujo de trabajo que escribieron un disparador y compararlas con los 613 commits del productor. Más ejecuciones que commits significa que se perdieron eventos antes de contarse; la igualdad significa que los 12 borrados son toda la pérdida.
