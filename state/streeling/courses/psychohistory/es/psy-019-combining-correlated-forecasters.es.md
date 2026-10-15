---
module_id: psy-019-combining-correlated-forecasters
department: psychohistory
course: "Combinar pronosticadores que comparten una fuente"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-019
version: "0.1.0"
---

# Combinar pronosticadores que comparten una fuente

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo escribirá el error cuadrático medio de un promedio de k pronósticos con errores correlacionados, hallará el suelo por debajo del cual no baja ningún número de pronosticadores, comparará un pronosticador más del mismo tipo con uno de otra fuente y dirá qué muestra el acuerdo. **Pregunta de proyecto:** ¿sirve de algo promediar los juicios de varios agentes cuando leen el mismo contexto?

[PSY-016](psy-016-brier-score.es.md) puntúa un pronóstico; este módulo puntúa un *promedio de pronósticos* con la aritmética de [PSY-004](psy-004-how-large-is-large.es.md).

## 1. Lo que comparten los jueces

**Observado** en el commit fijado; [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-019/extract.py) guarda una instantánea en [`observed-input.json`](../../../fixtures/psychohistory/psy-019/observed-input.json):

- La [política de orquestación multimodelo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/multi-model-orchestration-policy.yaml#L198-L203) fija `single_model: max 0.8`, `two_model_agreement: 0.9` y `two_model_disagreement: 0.5`. Su regla `cross-validation` exige el acuerdo de al menos dos modelos y nombra a claude y a chatgpt, que su registro de modelos asigna a dos proveedores.
- El [script del panel del tribunal](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) enviaría una *pull request* (solicitud de integración) a 5 *personas* (los perfiles de agente que define el proyecto). Todos los mensajes llevan el mismo título, la misma descripción, la misma lista de archivos y el mismo extracto del diff; solo cambian la *persona* y la preocupación que declara, y el flujo de trabajo pasa un único `--model`. Cada *persona* devuelve `block`, `merge_with_followups` o `pass`, y puede devolver un `score`, «0..1 confidence in this PR for my concern (1 = clean)» (la confianza en esta PR desde la preocupación propia, con el máximo para una PR limpia); el veredicto se queda con la respuesta más estricta, no con un promedio.
- El [script del consejo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py#L12-L35) empareja la comprobación de un analizador estático con la revisión de un modelo, dos revisores que llama «deliberately heterogeneous» (deliberadamente heterogéneos), y conserva la menor de sus dos puntuaciones; un veredicto con dos revisiones, dice, «lifts the single-model confidence cap honestly» (levanta honestamente el tope de confianza de un solo modelo), un supuesto que ningún archivo mide.

Ninguno de ellos contiene la respuesta de una *persona* ni un resultado; los cinco veredictos registrados del consejo contienen nueve puntuaciones (la de reviewer_a es 0.75 todas las veces) y ningún resultado. **No se ha medido ninguna correlación entre los agentes del proyecto: no la ha medido este módulo, ni consta en ninguno de los archivos que ha leído.** Todo lo que sigue es **sintético**.

Un *pronóstico* es un número enunciado antes de que se conozca el resultado; su *error* es el pronóstico menos el resultado. El modelo da al pronosticador i el error

```text
error_i = bias + sigma × ( sqrt(rho) × C + sqrt(1 − rho) × I_i )
```

C, la *parte común*, se sortea una vez por ocasión y la comparten todos; I_i, la *parte individual*, se sortea para cada pronosticador; las dos tienen media 0 y varianza 1. Cada error tiene entonces varianza sigma², y dos errores tienen correlación rho, la proporción común de esa varianza. Los agentes pueden compartir el *contexto* (lo que omite el extracto se le escapa a todo lector) y el *modelo* (los hábitos de un mismo conjunto de pesos); un escenario reparte rho = 0.6 en 0.3 para cada uno, un reparto inventado. Todos los que pronostican un mismo suceso comparten además lo que nadie podía prever en su resultado: ningún número de pronosticadores ni ninguna otra fuente lo elimina, e infla la correlación de los errores puntuados frente a los resultados. Hasta el último párrafo de la sección 4, los errores se miden respecto al mejor pronóstico posible, sin esa parte.

### Ejercicio práctico 1

Con ese reparto, dé la correlación de los errores entre una *persona* del panel y (a) otra *persona* del panel; (b) un revisor que usa otro modelo y lee el mismo extracto; (c) una segunda ejecución del modelo del panel a la que se da otro material; (d) un revisor que usa otro modelo y recibe otro material. ¿Qué caso es una sexta *persona*?

> **Respuesta:** (a) Las dos partes son comunes: `0.3 + 0.3 = 0.6`. (b) Solo el contexto: 0.3. (c) Solo el modelo: 0.3. (d) Nada: 0. Una sexta *persona* es el caso (a): un pronosticador más, el mismo rho. Estos valores clasifican fuentes; no miden nada.

## 2. La varianza de un promedio

Tome bias = 0. El *error cuadrático medio* (MSE, por sus siglas en inglés), el promedio del error al cuadrado sobre muchas ocasiones, es entonces la varianza del error. Un promedio de k pronósticos deja intacta la parte común, mientras que la media de k partes individuales tiene varianza 1/k:

```text
MSE del promedio de k pronósticos = sigma² × ( rho + (1 − rho) / k )
suelo, por grande que sea k       = rho × sigma²
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-019/analyze.py) lo comprueba sin muestreo: con partes de +1 o −1, los 32,768 patrones de signos para k = 14 dan como promedios de C², C × media(I) y media(I)² exactamente 1, 0 y 1/k.

**Calculado a partir de la forma cerrada**, en unidades del MSE de un pronosticador (sigma² = 1), con cuatro decimales:

| Pronosticadores k | rho = 0 | rho = 0.3 | rho = 0.6 | rho = 0.9 |
|---|---|---|---|---|
| 5 | 0.2 | 0.44 | 0.68 | 0.92 |
| 14 | 0.0714 | 0.35 | 0.6286 | 0.9071 |
| suelo | 0 | 0.3 | 0.6 | 0.9 |
| 14, simulado | 0.0716 | 0.3504 | 0.6284 | 0.9061 |

**Comprobación sintética.** La última fila procede de 200,000 ocasiones simuladas con semilla fija y partes uniformes. En las 56 celdas (k = 1 a 14), la simulación queda a menos de 1.02 errores estándar de la forma cerrada, y, en las 39 celdas con rho > 0 y k ≥ 2, se aparta al menos 82.26 de sigma²/k.

### Ejercicio práctico 2

Cinco pronosticadores tienen rho = 0.3. Calcule el MSE de su promedio y el de cinco pronosticadores independientes. De lo que el promedio puede llegar a eliminar, ¿cuánto han eliminado los cinco?

> **Respuesta:** `0.3 + 0.7 / 5 = 0.44`, frente a `1 / 5 = 0.2`. El suelo es 0.3, así que promediar puede eliminar como mucho `1 − 0.3 = 0.7`; los cinco han eliminado `1 − 0.44 = 0.56`, y `0.56 / 0.7 = 80%`. Esa proporción es `1 − 1/k` con cualquier rho: la correlación no hace más lento el promedio, sino que encoge lo que el promedio puede eliminar.

## 3. Más pronosticadores frente a otra fuente

Llamemos *valor equivalente* de un grupo al número de pronosticadores independientes cuyo promedio tiene el mismo MSE: `k / (1 + (k − 1) rho)`, que nunca supera `1 / rho` (Clemen y Winkler 1985). Es el tamaño muestral efectivo de PSY-004, aplicado a los errores: catorce pronosticadores valen 2.857 con rho = 0.3, 1.591 con 0.6 y 1.102 con 0.9.

Un pronosticador más del mismo tipo reduce el MSE en `sigma² (1 − rho) / (k (k − 1))`: de 13 a 14 con rho = 0.6, en 0.002198, es decir, un 0.35% (un 7.14% con pronosticadores independientes).

**Sintético.** Trece pronosticadores con rho = 0.6 (MSE 0.6308) y, después, un decimocuarto de la misma precisión:

| Lo que comparte el decimocuarto | Correlación con un miembro del panel | MSE, pesos iguales | MSE, pesos óptimos |
|---|---|---|---|
| contexto y modelo | 0.6 | 0.6286 | 0.6286 |
| uno de los dos | 0.3 | 0.5888 | 0.5246 |
| ninguno | 0 | 0.5490 | 0.3868 |

Los *pesos óptimos* minimizan el MSE del promedio ponderado (Bates y Granger 1969). Con v el MSE del promedio del panel, c la correlación del recién llegado con un miembro del panel y sigma² = 1:

```text
peso del recién llegado = (v − c) / (v + 1 − 2c)        MSE = (v − c²) / (v + 1 − 2c)
```

Un decimocuarto sin nada en común reduce el MSE en un 12.97% con un voto de catorce, y en un 38.68% con su peso óptimo, 0.3868 (con c = 0, el peso, el MSE y la reducción coinciden): los trece valen 1.585 pronosticadores y él añade uno.

### Ejercicio práctico 3

Un panel de 5 tiene rho = 0.6. Opción A: ampliarlo a 14 del mismo tipo. Opción B: mantener 5 y añadir un pronosticador independiente de la misma precisión. Calcule el MSE de A, el de B con pesos iguales y el de B con el peso óptimo.

> **Respuesta:** A: `0.6 + 0.4 / 14 = 0.6286`. B con pesos iguales: los cinco aportan `5 + 5 × 4 × 0.6 = 17` entre varianzas y covarianzas, y el externo, 1 y ninguna covarianza, así que `18 / 6² = 0.5`. B con el peso óptimo: `v = 0.6 + 0.4 / 5 = 0.68` y `c = 0`, así que el peso es `0.68 / 1.68 = 0.4048` y el MSE, 0.4048. Un externo con un voto de seis supera a nueve internos más, y baja de su suelo de 0.6.

## 4. Lo que un promedio no puede eliminar, y lo que muestra el acuerdo

**Un sesgo compartido.** Si todos los pronosticadores se inclinan hacia el mismo lado, el MSE del promedio es `bias² + sigma² (rho + (1 − rho) / k)`. **Sintético**, con bias = 0.5 y rho = 0.3: 1.25 para un pronosticador, 0.6 para catorce, por encima de un suelo de 0.55. Un sesgo puede estimarse a partir de pronósticos puntuados y restarse; la parte común cambia en cada ocasión y no puede restarse.

### Ejercicio práctico 4

Con bias = 0.5 y rho = 0.3, un equipo de 14 puede duplicarse hasta 28, o bien puntuar sus pronósticos pasados y restar el sesgo que encuentre. ¿Qué reduce más el MSE?

> **Respuesta:** Ahora: `0.25 + 0.3 + 0.7 / 14 = 0.6`, del cual el sesgo es `0.25 / 0.6 = 41.67%`. Duplicar: `0.25 + 0.3 + 0.7 / 28 = 0.575`, un 4.17% menos. Restar el sesgo: `0.3 + 0.7 / 14 = 0.35`, un 41.67% menos. Gana restar el sesgo, si es estable y conocido.

**Acuerdo.** La *dispersión* (*spread*) de un panel, la distancia cuadrática media de sus pronósticos a su propio promedio, no necesita ningún resultado. Pero la parte común desaparece de ella: su valor esperado es `sigma² (1 − rho) (k − 1) / k`. Con k = 14 y rho = 0.9, los pronósticos están a 0.30 de su promedio, mientras que ese promedio está a 0.95 del mejor pronóstico (medias cuadráticas); con rho = 0, las cifras son 0.96 y 0.27. **De dos paneles de pronosticadores igual de precisos, el que concuerda más estrechamente tiene, en valor esperado, el promedio menos preciso.**

**Una lectura que la política no enuncia.** Tome 0.8 como la probabilidad p de que un modelo acierte en una pregunta de sí o no, y rho como la correlación entre «el modelo 1 acierta» y «el modelo 2 acierta». Dos respuestas erróneas a una pregunta de sí o no coinciden, así que, con q = 1 − p,

```text
P(acierto | los dos coinciden) = (p² + rho p q) / (p² + q² + 2 rho p q)
```

Eso da 0.941 con rho = 0, 0.844 con 0.6 y 0.8 con 1, y exactamente el 0.9 de la política con rho = 7/32 = 0.21875. Cuando los dos discrepan, cada uno acierta la mitad de las veces, con cualquier rho: el 0.5 de la política.

### Ejercicio práctico 5

Dos *personas* del panel, con un mismo extracto y un mismo `--model`, coinciden en si hay que bloquear (una lectura de sí o no de sus tres veredictos), y un colega aplica el 0.9 de la política. Según la lectura anterior, calcule lo que vale su acuerdo con rho = 0 y con rho = 0.6, y después decida.

> **Respuesta:** Con rho = 0: `0.64 / 0.68 = 0.941`. Con rho = 0.6: `(0.64 + 0.6 × 0.16) / (0.68 + 2 × 0.6 × 0.16) = 0.736 / 0.872 = 0.844`. Decisión: no respaldada. El 0.9 necesita un rho de 0.21875 como máximo; la regla de la política empareja modelos de dos proveedores, y estas *personas* no lo son; y nadie ha medido rho para ninguno de los dos pares.

**La objeción más fuerte a esta lectura** es que todos los rho de este módulo son inventados. Las *personas* juzgan preocupaciones distintas; si eso hace que sus errores sean casi independientes, cinco de ellas eliminan el 80% del MSE de una *persona* (sección 2). Un extracto compartido aboga por un rho alto, y unas instrucciones distintas, por uno bajo: **este módulo no permite distinguir un rho de 0.1 de un rho de 0.9.** Los resultados por sí solos no lo zanjan. **Sintético**: en una pregunta de sí o no cuya probabilidad verdadera está entre 0.3 y 0.7, cinco *personas* se desvían de ella en 0.21 (desviación estándar); el 84% del MSE de una *persona* es la parte imprevisible, y `1 − (k / (k − 1)) × spread / error variance` tiende a 0.843 para *personas* que no comparten nada, y a 0.937 con rho = 0.6 (el 90% de 1,000 registros de 20 pull requests: de 0.79 a 0.87, y de 0.91 a 0.95).

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los archivos enlazados en la sección 1, el [flujo de trabajo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) que ejecuta el panel y los cinco registros del consejo. `extract.py` se detiene si alguno de ellos difiere de su blob de Git fijado.

**Fixture.** Desde la raíz del repositorio, `python -I -B scripts/streeling_fixtures/psychohistory/psy-019/extract.py`, y después `analyze.py` y `analyze.py --check` en la misma carpeta. Supuestos: [`scenarios.json`](../../../fixtures/psychohistory/psy-019/scenarios.json). Todas las cifras anteriores: [`results.json`](../../../fixtures/psychohistory/psy-019/results.json). Autocomprobaciones y límites: [README](../../../fixtures/psychohistory/psy-019/README.md).

**Referencias de método.** Bates, J. M., y Granger, C. W. J. (1969), «The Combination of Forecasts», *Operational Research Quarterly* 20(4), 451–468, doi:10.1057/jors.1969.103. Clemen, R. T., y Winkler, R. L. (1985), «Limits for the Precision and Value of Information from Dependent Sources», *Operations Research* 33(2), 427–442, doi:10.1287/opre.33.2.427.

**No realizado.** No se ejecutó ningún agente ni se leyó ningún resultado: la correlación entre los agentes del proyecto es desconocida. El modelo da a todos los pronosticadores la misma precisión y a todos los pares la misma correlación, y sortea errores de colas ligeras, lo que hace que el dimensionamiento anterior parezca más favorable de lo que es. No se modelizan ni la regla del panel, en la que se impone la respuesta más estricta, ni el mínimo del consejo. Ningún humano ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** En cada pull request, pedir a cada *persona* y a un *externo* (*outsider*), un agente con otro modelo al que se da otro material, la probabilidad de un suceso de sí o no (que se revierta en el plazo de un mes) y registrar el resultado. La parte imprevisible se cancela en `(persona–persona covariance − persona–outsider covariance) / (persona variance − persona–outsider covariance)`, que tiende a rho si el externo no comparte nada más con el panel (a un valor menor si comparte contexto o modelo, a uno mayor si sus errores van en sentido contrario a los del panel; el registro no permite saberlo). En el entorno sintético, 500 pull requests separan rho = 0 de 0.6 (el 90% de los registros: de −0.22 a 0.15, y de 0.49 a 0.67); 100 no lo consiguen. A diferencia del registro de PSY-004, este necesita resultados. Una estimación cercana a 0 haría que cinco *personas* valieran cinco pronosticadores; una cercana a 0.6, que valieran 1.471, y el siguiente agente debería leer otra cosa.
