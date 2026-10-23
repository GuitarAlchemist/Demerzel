---
module_id: psy-025-capstone-preregistered-forecast
department: psychohistory
course: "Proyecto final: un pronóstico prerregistrado que se puede puntuar"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "psy-016-brier-score", "psy-017-calibration-with-six-observations"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-025
version: "0.1.0"
---

# Proyecto final: un pronóstico prerregistrado que se puede puntuar

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo escribirá un pronóstico en forma de registro que un desconocido pueda resolver, lo contrastará con reglas sobre sus campos, tomará su tasa base de datos fijados y lo puntuará para cada resultado posible antes de que exista ninguno. **Pregunta de proyecto:** ¿podemos escribir sobre Streeling un pronóstico que un desconocido pueda puntuar más adelante sin preguntarnos qué quisimos decir?

Este proyecto final recurre a [PSY-005](psy-005-persistence-baseline.es.md) para la referencia que un pronóstico debe superar, a [PSY-016](psy-016-brier-score.es.md) para la puntuación de Brier y a [PSY-017](psy-017-calibration-with-six-observations.es.md) para los intervalos exactos sobre recuentos pequeños.

## 1. Un registro, no una conjetura

Para Nosek y sus colegas (2018), el *prerregistro* es «committing to analytic steps without advance knowledge of the research outcomes» (comprometerse con los pasos del análisis sin conocer de antemano los resultados de la investigación), depositado por lo general en una plataforma de registro independiente que «preserves the preregistration and makes it discoverable» (conserva el prerregistro y permite encontrarlo). El prerregistro «does not favor prediction over postdiction; its purpose is to make clear which is which» (no favorece la predicción frente a la posdicción; su propósito es dejar claro cuál es cuál). Un registro de pronóstico fija, antes del resultado, todo lo necesario para puntuar un pronóstico.

[`scenarios.json`](../../../fixtures/psychohistory/psy-025/scenarios.json) contiene cuatro registros. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-025/analyze.py) contrasta cada uno con 22 reglas sobre sus campos, enumeradas con sus mensajes de error en el [README](../../../fixtures/psychohistory/psy-025/README.md) del *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección). Las reglas responden a las preguntas de un desconocido:

| Un desconocido pregunta | Campos (reglas) |
|---|---|
| ¿Qué se pronostica exactamente? | `question` (R02), `kind` (R03), `forecast` (R15) |
| ¿Dónde y cuándo debo mirar? | `resolution_source` (R04–R06), `resolution_time` (R07, R08) |
| ¿Qué cuenta? | `resolution_rule`: qué, cuántas veces, qué no (R09); qué hacer si la fuente se trasladó (R10); cuándo es nulo (R11) |
| ¿Comparado con qué? | `reference_class`, `base_rate` con un comando y un commit (R12–R14), `reference_forecast` (R16) |
| ¿Qué cuenta en su contra? | `adjustment` (R17), `falsifier` (R18, R19) |
| ¿Quién lo escribió, quién más decide, y cuándo? | `author_can_influence_outcome` (R20) y su nota, `written_at` y su evidencia (R21, R22) |

**Sintético.** El borrador `library-growth-draft` dice «Streeling will keep growing fast next quarter» (Streeling seguirá creciendo deprisa el próximo trimestre), con la fuente «the repo» (el repositorio) y el pronóstico «likely» (probable). **Calculado:** el validador lo rechaza en 16 de las 22 reglas (R02, R04–R07, R09–R16, R18, R20, R22) y no puede juzgar R08, R17 ni R19, cuyos campos son inutilizables. Uno de los fallos es de otra naturaleza: este lote de módulos amplía la biblioteca, de modo que el autor del borrador podría hacer que se cumpliera, y un resultado que su autor puede dirigir es un plan que vigilar, no un pronóstico que puntuar. R20 solo juzga al autor del registro; los mantenedores que integrarían los registros integran también los módulos de todos los departamentos, cosa que declara `author_influence_note`. La versión reparada, `library-growth-repaired`, pregunta por la biblioteca fuera de Psicohistoria y pasa, al igual que los dos registros de ejemplo de la sección 3.

El validador comprueba la forma y la concordancia entre campos, no la claridad. Seis copias modificadas de los registros de ejemplo fallan cada una exactamente en la regla que se rompió; una séptima, cuyo pronóstico es igual a su referencia, pasa ([`results.json`](../../../fixtures/psychohistory/psy-025/results.json), `validation.controls`).

### Ejercicio práctico 1

Dos lectores traducen el «likely» del borrador por 0.6 y por 0.8. Dé la puntuación de Brier de cada lectura si el suceso ocurre y si no ocurre. ¿Qué dice eso sobre puntuar una palabra?

> **Respuesta:** 0.6: `(0.6 − 1)² = 0.16` si ocurre, `0.6² = 0.36` si no. 0.8: `0.04` y `0.64`. Un mismo resultado recibe dos puntuaciones según el lector, así que la puntuación mediría al lector, no al pronosticador: R15 exige un número.

## 2. Una tasa base a partir del historial fijado

**Observado.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-025/extract.py) lee los 73 commits que modificaron [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses) hasta el commit `4b03838`, y los 255 archivos de la carpeta en ese commit, cada uno contrastado con su blob fijado ([`observed-input.json`](../../../fixtures/psychohistory/psy-025/observed-input.json)). Un *módulo* en inglés es un archivo `<department>/en/<name>.md` que no sea un README: 68 en el commit fijado, en 18 departamentos. Música tiene 19, y Psicohistoria, 2.

Los pronósticos de ejemplo tratan sobre Música, que este lote no toca: uno sobre Psicohistoria mediría el propio plan del lote.

Una *clase de referencia* es el conjunto de casos pasados con el que se compara un pronóstico; su *tasa base* es la proporción de casos en los que ocurrió el suceso. Aquí un caso es un departamento durante una ventana de 92 días, el horizonte de los pronósticos, y el suceso es «su número de módulos aumentó». Dos ventanas consecutivas terminan en el commit fijado y caben después del primer commit de módulos, del 2026-03-21. **Calculado:**

| Clase de referencia | Subidas / casos | Tasa base | Intervalo exacto al 95% (PSY-017) |
|---|---|---|---|
| Departamentos que tienen un módulo al inicio de la ventana | 2 / 36 | 0.055556 | 0.0068 a 0.1866 |
| Solo Música | 1 / 2 | 0.5 | 0.0126 a 0.9874 |

Las dos subidas son las de Matemáticas (de 1 a 25 módulos) y Música (de 6 a 19), ambas en la ventana que termina en el commit fijado.

Se aplica la advertencia de [PSY-010](psy-010-growth-curves-short-series.es.md): el recuento avanza a ráfagas, así que la tasa base depende de dónde caen las ventanas. Retrasar las dos ventanas de un día en un día (`base_rate.alignment`) da a la clase amplia de 0.055556 a 0.151515 (5 de 33, 21 días atrás), y a Música de 0 a 2 subidas. Declarar la alineación hace que el número sea reproducible, no preciso.

### Ejercicio práctico 2

La tabla no muestra la clase amplia sin Música. Calcule su tasa. Diga después qué valor cae dentro del intervalo exacto de la otra clase, y qué se sigue de ello para elegir una clase.

> **Respuesta:** Sin la 1 subida de Música en 2 ventanas, `(2 − 1) / (36 − 2) = 1 / 34 = 0.029412`: quitar un solo departamento casi reduce la tasa a la mitad. La tasa amplia, 0.055556, cae dentro del intervalo de Música (de 0.0126 a 0.9874); 0.5 queda fuera del de la clase amplia (de 0.0068 a 0.1866), pero solo porque esa clase trata a Música como a los departamentos sin actividad. Los datos no pueden elegir la clase: el registro debe nombrar una y justificar cualquier desviación respecto a su tasa.

## 3. El pronóstico de ejemplo y su regla de resolución

**Sintético: un ejercicio de redacción de un pronóstico, no un compromiso del departamento ni una predicción que este respalde.** Dos registros comparten una fuente, una regla y una fecha:

- `music-rise-2027-01-13`: «Will the Streeling course library hold more than 19 distinct Music modules at 2027-01-13T23:59:59Z?» (¿contendrá la biblioteca de cursos de Streeling, en ese instante, más módulos distintos de Música que esa cifra?). Pronóstico de referencia: 0.055556, la tasa base amplia; pronóstico: **0.7**.
- `music-count-2027-01-13`: el mismo recuento, en forma de intervalo **[19, 25]** con α = 0.2, frente al [19, 19] de la persistencia (PSY-005): en 34 de los 36 casos el recuento no se movió. Con 0.3 en 19 (el cuantil 0.1 del autor) y, tras una subida, seis posibilidades sobre siete o más de quedarse en 25 o menos (de modo que 25 está en el cuantil 0.9 o por encima de él), la probabilidad de cobertura según el autor es al menos `0.3 + 0.7 × 6/7 = 0.9`: es un intervalo del 80% solo por su nivel declarado.

El campo `adjustment` dice por qué 0.7 se aparta de 0.055556: Música subió en la última ventana, su módulo más reciente lleva la fecha del día del commit fijado, y la tasa de Música sola es demasiado incierta para fijar un número, así que 0.7 es un juicio. Un desconocido puede discutir esa frase; el resto es mecánico.

*Fuente:* `GuitarAlchemist/Demerzel`, consultado después del momento de resolución, en el último commit de la cadena de primeros padres (*first-parent*) de `master` (o de la rama predeterminada, si se renombra) cuya fecha de confirmación (*committer date*) sea igual o anterior a ese momento; el registro da los comandos. *Qué cuenta:* los identificadores distintos de módulos de Música en archivos `.md`. El identificador de un archivo es el `module_id` de su cabecera (*front matter*) o, si no lo tiene, su nombre de archivo sin `.md` ni sufijo de idioma; su departamento, el de la cabecera o, si no, el de su carpeta (sin contar las carpetas de idioma); se excluyen los README, las páginas de índice y las copias publicadas. *Si se traslada:* si `master` nombra otro lugar como fuente de la biblioteca o como parte de ella (un README, un archivo puntero, un mensaje de commit), la regla se aplica también allí, exista o no esta carpeta; un identificador repartido entre varios lugares cuenta una sola vez. *Nulo:* no se encuentra ninguna biblioteca; `4b03838` no es un ancestro del commit de resolución; no hay sello de tiempo antes del momento de resolución; o el recuento de Música es distinto de 19 en algún commit de primer padre de `master` posterior a `4b03838` cuya fecha de confirmación preceda a ese sello de tiempo. Un pronóstico nulo se declara nulo, nunca se puntúa como 0.

**Calculado:** la cabecera por sí sola encuentra 67 módulos, no 68: `cyb-003-measuring-variety-ratio-quantitatively.md` no tiene. Con el nombre de archivo como alternativa, la regla da 68 y coincide con el recuento de rutas en los 18 departamentos; los 181 archivos traducidos llevan el identificador de su módulo en inglés y no añaden nada. Contar identificadores, y no rutas `en/`, permite que la regla sobreviva a una organización sin carpetas `en/`.

*Momento de redacción.* `written_at` (2026-10-14T13:39:06Z) es la palabra del autor: el archivo no está en ningún commit. Su sello de tiempo será el `mergedAt` que GitHub registre para la primera *pull request* (solicitud de integración) que integre su texto definitivo en `master`, o la constancia de su hash en un servicio de sellado de tiempo, si es anterior; no la hora de apertura de la solicitud (puede preceder al texto definitivo), ni las horas de los *push* (la API de eventos de GitHub las conserva 30 días), ni las fechas de los commits (las fija la máquina de quien hace el commit). Hasta entonces, el registro tiene la forma de un prerregistro, pero todavía no está registrado.

### Ejercicio práctico 3

Aplique la regla a esta lista inventada de archivos (ruta, `module_id` y `department` de la cabecera; `-` significa ausente) tras un traslado. ¿Cuántos módulos de Música contiene? ¿Y si en la fecha de puntuación la biblioteca ha desaparecido y nada nombra un nuevo lugar?

```text
music/index.md - -
music/mus-001-what-is-a-chord.md mus-001-what-is-a-chord music
music/mus-023-voice-leading.md - -
music/fr/mus-001-what-is-a-chord.fr.md mus-001-what-is-a-chord music
music/fr/mus-023-voice-leading.fr.md mus-023-voice-leading music
musicology/mcl-003-performance-practice.md mcl-003-performance-practice musicology
```

> **Respuesta:** 2. `index.md` queda excluido; `mus-023-voice-leading` toma su identificador del nombre de archivo y su departamento, de su carpeta; los archivos en francés repiten identificadores ya contados; `mcl-003` es de Musicología. Sin biblioteca y sin nada que apunte a un nuevo lugar, el pronóstico es nulo: no es 0, ni tampoco «no».

## 4. Puntuarlo antes de que exista el resultado

Un registro está terminado cuando se conoce su puntuación para cada resultado posible. **Calculado, sobre resultados INVENTADOS**, con la pericia de PSY-016, `1 − BS / BS_ref` (BS_ref: la puntuación de Brier de la referencia, exactamente 0.055556 tal como se declara, a partir de puntuaciones sin redondear):

| `music-rise` | Brier, pronóstico 0.7 | Brier, referencia 0.055556 | Pericia |
|---|---|---|---|
| Resultado 1 (más de 19) | 0.09 | 0.891974 | 0.8991 |
| Resultado 0 (19 o menos) | 0.49 | 0.003086 | −157.75746 |

El resultado 0, único caso en el que 0.7 lo hace peor que la tasa base, es el resultado refutador.

La *puntuación de intervalo* (*interval score*) de un intervalo central [l, u] de nivel (1 − α), ante el resultado x, es su anchura `u − l`, más `(2/α)(l − x)` si x < l, o más `(2/α)(x − u)` si x > u; cuanto más baja, mejor. Es la forma de Gneiting y Raftery (2007, ec. 43), que ellos remontan a trabajos anteriores, entre ellos Winkler (1972). Un *fallo* es un resultado fuera del intervalo. Aquí α = 0.2, así que cada módulo fuera del intervalo cuesta 10, más la anchura, 6.

| Recuento inventado | 18 | 19 | 21 | 25 | 28 |
|---|---|---|---|---|---|
| Cubierto por [19, 25] | no | sí | sí | sí | no |
| Puntuación de intervalo | 16 | 6 | 6 | 6 | 36 |
| Persistencia [19, 19] | 10 | 0 | 20 | 60 | 90 |

El intervalo puntúa peor que la persistencia exactamente en los recuentos de 0 a 19: los mismos resultados refutadores. La cobertura exige muchos intervalos: diez intervalos así, cada uno con una probabilidad de cobertura de 0.9, cubren siete veces o menos con probabilidad 0.070191.

### Ejercicio práctico 4

Vuelva a calcular la puntuación de intervalo de [19, 25] con α = 0.2, y la de la persistencia, para los recuentos inventados 28 y 18. ¿Cuáles son fallos, y dónde gana la persistencia?

> **Respuesta:** 28: `6 + 10 × (28 − 25) = 36`; persistencia, `10 × 9 = 90`. 18: `6 + 10 × (19 − 18) = 16`; persistencia, `10 × 1 = 10`. Los dos son fallos. En 18 gana la persistencia, 10 frente a 16: el intervalo pagó además su anchura.

**La objeción más fuerte**: el registro es puntuable, pero su pronóstico es débil. La tasa base descansa sobre dos ventanas y pasa de 0.055556 a 0.151515 según su alineación; su intervalo exacto trata los 36 pares departamento-ventana como independientes, cuando las dos subidas caen en una misma ventana y en una misma ráfaga, así que subestima la incertidumbre; el 0.7 es un juicio; y el recuento de Música depende de las decisiones de integración de los mantenedores, en las que un pronóstico publicado podría influir por sí mismo. Una sola puntuación no dice casi nada sobre la pericia: 0.8991 o −157.8 (redondeado). Lo zanjaría una serie de registros así, cada uno con un sello de tiempo anterior a su resultado y puntuado frente a su referencia declarada.

### Ejercicio práctico 5

`library-growth-repaired` declara 0.75 frente a su tasa base, 1 subida en 2 ventanas. Calcule las dos puntuaciones de Brier y la pericia para cada resultado, y nombre el resultado refutador. Si el recuento supera 66 el 2027-01-13, ¿ha demostrado pericia el pronosticador?

> **Respuesta:** Resultado 1: `(0.75 − 1)² = 0.0625` frente a `(0.5 − 1)² = 0.25`, pericia `1 − 0.0625 / 0.25 = 0.75`. Resultado 0: `0.75² = 0.5625` frente a `0.25`, pericia `1 − 0.5625 / 0.25 = −1.25`. Resultado refutador: 0. No: una sola resolución favorable no permite distinguir a un buen pronosticador de uno con suerte.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** el historial de commits y los 255 archivos de la biblioteca de cursos enlazada más arriba.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-025/extract.py`, y después `analyze.py` y `analyze.py --check`. El README enumera las reglas, las 22 autocomprobaciones y los controles negativos.

**Referencias de método.** Nosek, B. A., Ebersole, C. R., DeHaven, A. C., y Mellor, D. T. (2018), «The preregistration revolution», *PNAS* 115(11), 2600–2606, [doi:10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114). Gneiting, T., y Raftery, A. E. (2007), «Strictly Proper Scoring Rules, Prediction, and Estimation», *Journal of the American Statistical Association* 102(477), 359–378, sección 6.2. Winkler, R. L. (1972), «A Decision-Theoretic Approach to Interval Estimation», *Journal of the American Statistical Association* 67(337), 187–191. Los intervalos exactos son los de Clopper y Pearson (1934), citados en PSY-017.

**No realizado.** Ningún registro se ha resuelto ni ha recibido un sello de tiempo, y todos los resultados puntuados son inventados. La regla de recuento solo se probó sobre la biblioteca fijada, no sobre contenidos anteriores de los archivos ni sobre copias publicadas. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Después de 2027-01-13T23:59:59Z, resolver los dos registros de ejemplo según su propia regla o declararlos nulos, y puntuarlos frente a sus referencias. Antes: un cambio en el recuento de Música anterior a su sello de tiempo los anula, lo que mostraría con qué rapidez puede anularse un pronóstico sobre una carpeta activa antes de que nadie lo registre.
