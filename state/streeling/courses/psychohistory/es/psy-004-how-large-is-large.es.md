---
module_id: psy-004-how-large-is-large
department: psychohistory
course: "¿Cuántos son muchos? Previsibilidad agregada con catorce agentes"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-002-governance-phase-transitions"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-004
version: "0.1.0"
---

# ¿Cuántos son muchos? Previsibilidad agregada con catorce agentes

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo pondrá un intervalo exacto a una proporción observada entre unos pocos agentes que responden sí o no, dirá cómo se reduce su amplitud a medida que crece el grupo y sustituirá el número de agentes por un tamaño muestral efectivo cuando los agentes comparten una causa. **Pregunta de proyecto:** el departamento afirma que el comportamiento agregado de 14 *personas* (los perfiles de agente que define el proyecto) repartidas en 4 repositorios sigue leyes matemáticas. ¿Qué amplitud tiene la incertidumbre sobre un agregado de 14, y qué efecto tiene sobre ella un contexto compartido?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) afirma que el agregado sigue leyes estadísticas e interpreta la correlación entre repositorios como una señal de acoplamiento. [PSY-019](psy-019-combining-correlated-forecasters.es.md) aplica la misma aritmética a los errores de pronóstico; [PSY-024](psy-024-the-single-actor.es.md) se pregunta quién actuó en los sucesos registrados.

## 1. Lo que afirma el registro y lo que contiene el repositorio

**Observado.** El [registro del departamento](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) cierra su principio clave con esta frase: «One agent's decision is unpredictable, but the aggregate behavior of 14 personas across 4 repos follows mathematical laws.» [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/extract.py) guarda una instantánea de ese registro, y de los archivos a los que la frase podría referirse, en [`observed-input.json`](../../../fixtures/psychohistory/psy-004/observed-input.json).

- El registro enumera 4 repositorios consumidores, como dice la frase. [`personas/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/personas) contiene **17** archivos de *persona*, 3 más de los indicados; contenía 14 en el [commit `e9fe8b7`](https://github.com/GuitarAlchemist/Demerzel/tree/e9fe8b7d711ede390b602896e4a5c571d0ad1f67/personas), que añadió el registro el 2026-03-21 (leído con `git ls-tree`, fuera del *fixture*, es decir, de la carpeta de datos y scripts que reproduce las cifras de esta lección).
- Un archivo de *persona* describe un rol y no registra ninguna decisión.
- Un [flujo de trabajo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) enviaría una *pull request* (solicitud de integración) a un panel de **5** *personas*, cada una de las cuales la examinaría desde un aspecto distinto y respondería `block`, `merge_with_followups` o `pass`. Las cinco reciben el mismo título, la misma descripción, la misma lista de archivos y el mismo diff truncado, y la [ejecución](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) fija un único `--model`. Allí, unos comentarios dicen que el flujo de trabajo fue «observed failing on every sibling-pr-opened dispatch» (visto fallar en cada envío sibling-pr-opened) y que «silently never produced a verdict» (nunca produjo un veredicto, sin avisar) mientras le faltó un permiso que el archivo concede; en el commit fijado no hay ningún veredicto guardado, y su carpeta, `state/quality/verdicts/`, no existe.
- Entre los archivos leídos, las únicas respuestas registradas de varios revisores a una misma pregunta están en [`state/council/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/council): 5 veredictos sobre una sola pull request, fechados el 2026-06-24, con 9 revisiones `pass` o `fail`, como máximo 2 por veredicto (el límite del [esquema](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/council-verdict.schema.json)). Los revisores son dos roles, una comprobación automática (`reviewer_a`) y un revisor basado en un modelo de lenguaje (`reviewer_b`), según el [script que los escribe](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py), nunca una *persona* (0 de 9). En los 4 veredictos con dos revisiones, las respuestas coinciden una vez y difieren tres.

**Calculado.** El mayor grupo que la instantánea muestra respondiendo a una misma pregunta tiene 2 miembros; el panel del flujo de trabajo tiene 5, no 14, y ningún veredicto. Este fixture no puede, por tanto, poner a prueba la afirmación. Todo lo que sigue es **sintético**: «agentes» que responden sí o no con probabilidades supuestas.

### Ejercicio práctico 1

Clasifique cada afirmación como observada, calculada a partir de datos observados o no respaldada por la instantánea, y dé el motivo: (a) `personas/` contiene 17 archivos de *persona*; (b) tres de los cuatro veredictos con dos revisiones están divididos; (c) los cinco veredictos del consejo son cinco observaciones independientes del acuerdo entre revisores; (d) el comportamiento agregado de 14 *personas* sigue una ley estadística.

> **Respuesta:** (a) Observada: un recuento de archivos en el commit fijado. (b) Calculada a partir de las revisiones observadas: en 3 de los 4 veredictos con dos revisiones, las respuestas difieren. (c) No respaldada: los 5 se refieren a una sola pull request en el plazo de una hora, y `reviewer_a` responde `pass` en 5 de 5; eso se parece más a una ocasión repetida que a cinco. (d) No respaldada: el mayor grupo registrado tiene 2 miembros, ninguna revisión nombra a una *persona* y el panel de 5 no ha dejado ningún veredicto.

## 2. Catorce agentes independientes

Tome n agentes que dicen sí, cada uno de forma independiente, con la misma probabilidad desconocida p. La *proporción* de síes, k/n, estima p. La ley de los grandes números dice que la proporción se acerca a p a medida que n crece; su desviación estándar (DE), `sqrt(p (1 - p) / n)`, dice a qué velocidad. Un *intervalo exacto al 95%* (de Clopper y Pearson) conserva todos los valores de p bajo los cuales el recuento observado k no cae en ninguna de las dos colas del 2.5% (es bilateral; la cota unilateral de [PSY-006](psy-006-transition-matrix-from-counts.es.md) pone todo el 5% en una sola cola):

```text
límite inferior: el p para el que  P(X >= k) = 0.025
límite superior: el p para el que  P(X <= k) = 0.025      X ~ Binomial(n, p)
si los n dicen sí: límite inferior = 0.025^(1/n), límite superior = 1
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/analyze.py) suma los términos binomiales y despeja p por bisección. **Calculado a partir de entradas supuestas** (la mitad de los agentes dice sí; tres decimales):

| Agentes | Intervalo exacto al 95% | Amplitud | DE con p = 0.5 |
|---|---|---|---|
| 14 | 0.230 a 0.770 | 0.539 | 0.134 |
| 100 | 0.398 a 0.602 | 0.203 | 0.050 |
| 10,000 | 0.490 a 0.510 | 0.020 | 0.005 |

Catorce agentes divididos a partes iguales son compatibles con cualquier p entre 0.23 y 0.77, más de la mitad de la escala. La amplitud se reduce con la raíz cuadrada del tamaño del grupo: 100 agentes dan un intervalo 2.652 veces más estrecho (`sqrt(100 / 14) = 2.673`). La aproximación normal `n = z² p (1 - p) / h²`, con z = 1.959964 y p = 0.5, pide 384.146, es decir, 385 agentes, para una semiamplitud h de 5 puntos.

Con 14 agentes, este intervalo contiene p al menos el 95.5% de las veces para cada uno de los 99 valores de p entre 0.01 y 0.99 ([`results.json`](../../../fixtures/psychohistory/psy-004/results.json)). Un panel de 5 dice todavía menos: si los cinco dicen sí, el límite inferior es `0.025^(1/5) = 0.478`.

### Ejercicio práctico 2

Los 14 agentes dicen sí. (a) Calcule el límite inferior del intervalo exacto al 95%. (b) ¿Cuántos agentes independientes tienen que ser unánimes para que ese límite llegue a 0.95?

> **Respuesta:** (a) `0.025^(1/14) = 0.768`: la unanimidad de 14 agentes independientes admite una probabilidad de sí tan baja como 0.77. (b) `0.025^(1/n) >= 0.95` da `n >= ln 0.025 / ln 0.95 = 71.917`, es decir, 72 agentes.

## 3. Agentes que comparten una causa

El panel de la sección 1 da a sus cinco *personas* un mismo diff y un mismo ajuste de modelo: los agentes de un mismo proyecto pueden compartir causas. **Sintético, modelo supuesto:** en cada ocasión (una pregunta planteada a todos los agentes), una señal común dice sí con probabilidad p. Cada agente la copia con probabilidad c y, si no, decide por su cuenta, sí con probabilidad p. Cada agente sigue diciendo sí con probabilidad p, pero dos respuestas tienen ahora la correlación `rho = c²`. Entonces:

```text
varianza de la proporción = p (1 - p) / n × (1 + (n - 1) rho)
efecto de diseño          = 1 + (n - 1) rho
tamaño muestral efectivo  = n / (1 + (n - 1) rho)        tiende a 1 / rho cuando n crece
```

El *tamaño muestral efectivo* es el número de agentes independientes cuya proporción variaría tanto como la de este grupo; *efecto de diseño* es el término de Kish para el factor que separa ambas cantidades. Para 14 agentes y p = 0.5, a partir de la distribución exacta de los recuentos y de 50,000 ocasiones simuladas por fila:

| rho | Efecto de diseño | Tamaño muestral efectivo | DE de la proporción | Recuentos de síes que cubren al menos el 95% de las ocasiones | Varianza simulada ÷ varianza independiente |
|---|---|---|---|---|---|
| 0 | 1.0 | 14 | 0.134 | 3 a 11 | 0.990 |
| 0.1 | 2.3 | 6.087 | 0.203 | 2 a 12 | 2.291 |
| 0.3 | 4.9 | 2.857 | 0.296 | 1 a 13 | 4.926 |
| 0.6 | 8.8 | 1.591 | 0.396 | 0 a 14 | 8.792 |

La fila 1 es la comprobación con respuesta conocida: rho = 0 devuelve la varianza binomial.

Añadir agentes no lo remedia. Con rho = 0.1, el tamaño muestral efectivo es 6.087 para 14 agentes, 9.174 para 100 y 9.991 para 10,000, por debajo de un techo de `1 / rho = 10`, y la DE de la proporción no puede bajar de `sqrt(rho p (1 - p)) = 0.158`. La ley de los grandes números sigue promediando lo que cada agente decide por su cuenta, pero no la señal común: la proporción de 10,000 agentes se estabiliza cerca de 0.658 o de 0.342 (la probabilidad de sí dada la señal), no de 0.5. Con una causa común así, la discrepancia de la sección 1 importa poco: con rho = 0.3, 17 agentes valen tanto como 2.931 independientes, frente a 2.857 para 14.

### Ejercicio práctico 3

Un equipo tiene 100 agentes con rho = 0.3. Calcule el efecto de diseño y el tamaño muestral efectivo. ¿Cuántos agentes necesitaría para un tamaño muestral efectivo de 5?

> **Respuesta:** Efecto de diseño `1 + 99 × 0.3 = 30.7`; tamaño muestral efectivo `100 / 30.7 = 3.257`. Un tamaño muestral efectivo de 5 es inalcanzable: el techo es `1 / 0.3 = 3.333`. Solo un rho más bajo eleva el techo, y 5 exige un rho inferior a `1 / 5 = 0.2`.

## 4. Lo que cuesta ignorar la causa común, y la objeción más fuerte

**Sintético.** Aplique el intervalo de la sección 2 a agentes que comparten una causa, como si fueran independientes. Con p = 0.5 contiene p en el 98.7% de las ocasiones con rho = 0, en el 90.6% con 0.1, en el 64.5% con 0.3 y en el 20.4% con 0.6: con rho = 0.3, un intervalo «del 95%» contiene aquí p dos veces de cada tres.

Un tablero de indicadores imaginario informa de que 12 de 14 agentes aprueban y lo llama un consenso fuerte. Leído como un conjunto de respuestas independientes, el recuento lo respalda: el intervalo exacto, de 0.572 a 0.982, excluye un reparto a partes iguales. Pero cuando p vale 0.5, al menos 12 de los 14 agentes dan la misma respuesta en el 1.3% de las ocasiones si son independientes, en el 9.4% con rho = 0.1, en el 35.5% con 0.3 y en el 79.6% con 0.6.

### Ejercicio práctico 4

Decida si el tablero puede anunciar «consenso fuerte» según este criterio: 12 o más agentes de acuerdo deben darse en menos del 5% de las ocasiones bajo un reparto a partes iguales.

> **Respuesta:** Depende de un número que nadie ha medido. Con agentes independientes sale el 1.3%, por debajo del 5%: permitido. Un rho de 0.1 da el 9.4% y uno de 0.3 el 35.5%: no permitido. La decisión es «todavía no»: «12 de 14» es una prueba sólida solo si los agentes responden de forma casi independiente.

**La objeción más fuerte a esta lectura** es que las secciones 3 y 4 descansan sobre un único modelo inventado y sobre valores de rho inventados. Un segundo modelo con las mismas correlaciones (en cada ocasión se extrae un nivel común q de una distribución beta, y cada agente dice sí con probabilidad q) da exactamente la misma varianza y el mismo tamaño muestral efectivo, que dependen solo de rho. Las colas no: con rho = 0.3, los 14 agentes coinciden en el 10.7% de las ocasiones, frente al 2.8% en el primer modelo. Más importante aún, el rho de las *personas* es desconocido. Si está cerca de 0, la sección 2 es toda la respuesta. **Nada en este módulo permite distinguir ese caso de un rho de 0.6.**

Un registro de decisiones lo mediría: una respuesta sí/no por ocasión y por *persona*; a partir de él se estima rho como `(b - m²) / (m (1 - m))`, donde m es la proporción de síes y b la de pares de agentes que dicen sí los dos. **Dimensionamiento sintético:** un registro detecta una causa común cuando su estimación supera el percentil 95 de los registros simulados con rho = 0. Con 14 agentes, los registros de 20 ocasiones detectan rho = 0.1 en 2,312 de 2,500 (92%) y rho = 0.3 en los 2,500. Con los 5 agentes del panel, detectan rho = 0.3 en 9,447 de 10,000 (94%), pero rho = 0.1 en 3,608 (36%); los registros de 100 ocasiones detectan rho = 0.1 en 1,759 de 2,000 (88%).

### Ejercicio práctico 5

Un equipo quiere que la proporción de síes entre sus agentes quede a no más de 5 puntos de la tasa a largo plazo p = 0.5 en el 95% de las ocasiones. (a) ¿Qué DE de la proporción exige eso, y cuántos agentes independientes? (b) Resulta que los agentes tienen rho = 0.1. ¿Puede el equipo alcanzar el objetivo añadiendo agentes?

> **Respuesta:** (a) `0.05 / 1.959964 = 0.0255`, y `n = 1.959964² × 0.25 / 0.05² = 384.146`: unos 385 agentes independientes según la aproximación normal. Con el cálculo exacto, 385 agentes quedan a no más de 5 puntos en el 94.7% de las ocasiones; todos los grupos de 399 a 1,000 alcanzan el 95%. (b) No. Con rho = 0.1, la DE no puede bajar de `sqrt(0.1 × 0.25) = 0.158`, y el tamaño muestral efectivo no puede superar `1 / 0.1 = 10`, frente a los 385 necesarios. El equipo tiene que reducir rho o aceptar una banda más ancha.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los archivos enlazados en la sección 1.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-004/extract.py`, y después `analyze.py` en la misma carpeta. Supuestos y semillas: [`scenarios.json`](../../../fixtures/psychohistory/psy-004/scenarios.json). Autocomprobaciones y controles negativos: [README](../../../fixtures/psychohistory/psy-004/README.md).

**Referencias de método.** Clopper, C. J., y Pearson, E. S. (1934), «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial», *Biometrika* 26(4), 404–413. Kish, L. (1965), *Survey Sampling*, Wiley (el efecto de diseño).

**No realizado.** No se leyó ninguna decisión de ninguna *persona* ni se estimó ninguna correlación entre *personas*; este fixture leyó el panel del tribunal sin ejecutarlo. Los agentes son intercambiables (un mismo p y un mismo rho para todos) y solo responden sí o no; las *personas* del panel se ocupan de aspectos distintos y tienen tres respuestas posibles. Se probaron dos modelos generadores, ambos con p = 0.5. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Los veredictos del panel serían el registro de decisiones: su script guarda en cada uno un resultado por *persona*. Cuando las ejecuciones funcionen y existan 100 veredictos, estime rho. Una estimación cercana a 0 haría de la sección 2 la respuesta; una de 0.3 o más haría que las cinco voces del panel valieran como mucho lo que 2.273 independientes, y catorce voces así, como mucho lo que 2.857.
