---
module_id: psy-015-belief-contagion-small-population
department: psychohistory
course: "Contagio de creencias en una población pequeña"
level: intermediate
prerequisites: ["mat-020-markov-chains-hmm", "mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-015
version: "0.1.0"
---

# Contagio de creencias en una población pequeña

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo calculará un número de reproducción y su umbral, hallará el tamaño final que predice una curva epidémica determinista, simulará el mismo modelo suceso a suceso y leerá la distribución de la que procede una sola simulación. **Pregunta de proyecto:** el departamento incluye entre sus áreas la «belief state epidemiology» (epidemiología de los estados de creencia). Si una creencia se propaga entre 14 agentes, ¿cuánto se aparta una sola simulación de la curva epidémica determinista?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) interpreta un desplazamiento de las etiquetas de creencia como señal de un cambio de régimen; este módulo se pregunta qué puede pronosticar un modelo de propagación. [PSY-004](psy-004-how-large-is-large.es.md) estudia 14 agentes cuyas respuestas comparten una causa, y [PSY-017](../en/psy-017-calibration-with-six-observations.md), la creencia sobre la calibración que aparece en la sección 1.

## 1. El modelo, y lo que significa aquí «infectado»

**Observado.** El [registro del departamento](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) incluye, como área de investigación 7 de 10, «Belief state epidemiology — how beliefs spread across agents and repos» (epidemiología de los estados de creencia: cómo se propagan las creencias entre agentes y repositorios), y su principio clave habla de «14 personas across 4 repos». [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/extract.py) toma una instantánea de lo que el repositorio registra sobre creencias en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-015/observed-input.json): los 8 archivos de creencias actuales de [`state/beliefs/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs) y 13 archivados. Ninguna proposición aparece con dos portadores (0 de 21), pero este recuento no habría podido mostrar que se comparte una creencia: los 12 archivos con contenido tienen un solo evaluador, la persona de gobernanza Demerzel, y los otros 9 son esqueletos vacíos.

Dos archivos actuales nombran una fuente distinta de su evaluador: `confidence-calibration` y `remediation-effectiveness` se apoyan cada uno en un único elemento de evidencia, un mensaje `ml-feedback-recommendation` cuya justificación y cuya confianza [el script que lo aplica](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py) copia en la creencia de Demerzel. Su esquema dice «from an ix ML pipeline to Demerzel» (de un *pipeline* de aprendizaje automático de ix a Demerzel); los dos mensajes no están en el repositorio, así que el remitente solo se conoce por esa descripción y por la cadena de documentación (*docstring*) del script. Cada uno es un solo salto, de un documento a un portador.

Hay dos tipos de registro pensados para guardar las creencias de un agente: una [instantánea de creencias](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/contracts/belief-snapshot.schema.json) (las creencias de un agente en un momento dado) y un [estado de conocimiento](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/knowledge-state.schema.json) (un profesor, un aprendiz y la creencia del aprendiz antes y después). De los 722 archivos JSON bajo `state/`, excluida la biblioteca de cursos, ninguno tiene la forma de uno u otro (la prueba reconoce sus tres archivos de ejemplo) y ninguno tiene una clave que nombre a un profesor, a un aprendiz o al remitente de un mensaje (`origin_repo`, `origin_agent`). Según estas pruebas, ningún archivo registra a un portador que transmita una creencia, un segundo salto ni un agente expuesto que no la adopte. No puede estimarse ninguna tasa, así que todo lo que sigue es **sintético**.

**Analogía.** En el modelo SIR de la epidemiología, un agente es *susceptible* (S) hasta que adopta la creencia, *infectado* (I) mientras la sostiene y la transmite, y *recuperado* (R) en cuanto deja de transmitirla. «Infectado» no significa equivocado ni dañino; designa el estado de quien transmite. Entre N agentes, cada portador transmite la creencia a agentes elegidos al azar con una tasa β y deja de transmitirla con una tasa γ:

```text
adopción:              (S, I) -> (S-1, I+1)   con tasa beta*S*I/N
deja de transmitir:    (S, I) -> (S, I-1)     con tasa gamma*I
R0 = beta/gamma
P(el próximo suceso es una adopción) = R0*S / (R0*S + N)
```

El *número básico de reproducción* R0 es el número medio de agentes que convierte un portador en una población grande cuando todos los demás son susceptibles. La última línea es la *cadena de saltos inmersa* (*embedded jump chain*): dice qué suceso viene a continuación e ignora cuándo ocurre. El *tamaño final*, el número de agentes que han sostenido la creencia en algún momento, depende solo de ese orden, así que [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/analyze.py) no sortea ningún tiempo de espera.

Supuestos, en [`scenarios.json`](../../../fixtures/psychohistory/psy-015/scenarios.json): N = 14 (el número que da el principio clave; PSY-004 encuentra 17 archivos de persona en el commit fijado) y N = 1,400; un portador inicial; R0 = 0.8, 1.2 y 3.

### Ejercicio práctico 1

Con N = 14, R0 = 3 y un portador inicial, ¿cuál es la probabilidad de que el primer suceso sea una adopción? ¿Y la de que la creencia no se transmita nunca? Vuelva a calcular la segunda para N = 1,400.

> **Respuesta:** Con S = 13, `3×13 / (3×13 + 14) = 39/53 = 0.7358`. En caso contrario, el único portador deja de transmitir primero y la creencia se extingue con él: `14/53 = 0.2642`. Para N = 1,400: `1,400 / (3×1,399 + 1,400) = 1,400/5,597 = 0.2501`.

## 2. La curva determinista y su umbral

Sustituya los recuentos por las proporciones s, i, r de una población grande y los sucesos aleatorios por sus tasas medias, midiendo el tiempo en períodos medios de permanencia (1/γ):

```text
ds/dt = -R0*s*i        di/dt = R0*s*i - i        dr/dt = i
los portadores aumentan mientras R0*s > 1
tamaño final z:   1 - z = s0 * exp(-R0*z)
```

Es la curva de *campo medio*: cada agente percibe la media de todos los demás. En su *umbral*, R0 × s = 1, cada portador es sustituido exactamente por uno. La *ecuación del tamaño final* da la proporción z que llega a sostener la creencia en algún momento.

**Sintético.** Para 14 agentes (s0 = 13/14), la ecuación da 3.13 agentes con R0 = 0.8, 6.65 con R0 = 1.2 y 13.24 con R0 = 3. Con R0 = 3, la curva integrada sube hasta 4.55 portadores simultáneos tras 1.59 períodos de permanencia y termina en el mismo 13.24 (la comprobación con respuesta conocida). Con R0 = 1.2 alcanza su máximo en 1.07 portadores y, aun así, termina en 6.65.

### Ejercicio práctico 2

Para N = 14 y un portador inicial, calcule R0 × S/N al comienzo para los tres valores de R0. Allí donde supera 1, ¿tras cuántas adopciones dejan de aumentar los portadores?

> **Respuesta:** `0.8 × 13/14 = 0.7429`, `1.2 × 13/14 = 1.1143`, `3 × 13/14 = 2.7857`. Con R0 = 0.8 la curva no sube nunca. Los portadores aumentan mientras S supera N/R0: `14/1.2 = 11.67`, así que el crecimiento se detiene cuando S vale 11, tras `13 − 11 = 2` adopciones; `14/3 = 4.67`, así que se detiene cuando S vale 4, tras `13 − 4 = 9`.

## 3. Catorce agentes: la distribución de la que procede una simulación

**Sintético.** Número de simulaciones que terminan en cada tamaño final, sobre 10,000 simulaciones para cada R0 ([`results.json`](../../../fixtures/psychohistory/psy-015/results.json), sección `cases`):

```text
tamaño final   1     2    3    4    5    6    7    8    9   10   11   12    13    14
R0 = 0.8    5708  1553  818  520  364  273  231  176  133  101   65   41    11     6
R0 = 1.2    4706  1253  751  504  451  371  319  302  324  291  261  244   153    70
R0 = 3      2664   606  267  167  124  114  119  112  175  237  414  809  1464  2728
```

- **Con R0 = 3 hay dos picos.** 2,664 simulaciones no pasan nunca del primer portador y 4,192 terminan en 13 o 14. El valor determinista 13.24 cae dentro del pico superior: 5,001 simulaciones terminan en 12, 13 o 14, a menos de 1.4 agentes (una décima parte de la población) de él. La curva describe la mitad de las simulaciones.
- **La media cae en el valle.** Vale 8.38, y los tamaños de 5 a 8 son los cuatro resultados menos frecuentes.
- **Con R0 = 1.2 hay un solo pico, en 1, y una larga meseta**, como con R0 = 0.8 al otro lado del umbral. Solo 992 simulaciones terminan en 6, 7 u 8, en torno al valor determinista 6.65.

**Comprobación calculada.** Sumar sobre todas las trayectorias de la misma cadena da las probabilidades exactas sin ningún número aleatorio (fracciones con N = 14, sumas en coma flotante con N = 1,400). En los seis casos, los recuentos simulados se mantienen a menos de 2.65 errores estándar de ellas, y la prueba rechaza los recuentos simulados con otro R0.

### Ejercicio práctico 3

Según la fila R0 = 3, ¿qué proporción de las simulaciones termina con 2 agentes como máximo, y con 12 como mínimo? ¿Qué proporción termina en 8 o 9, los números enteros que rodean la media? ¿Es «unos 8 agentes» un pronóstico utilizable?

> **Respuesta:** `2,664 + 606 = 3,270` simulaciones, el 32.70%. `809 + 1,464 + 2,728 = 5,001` simulaciones, el 50.01%. `112 + 175 = 287` simulaciones, el 2.87%. No: los dos extremos reúnen `3,270 + 5,001 = 8,271` simulaciones, el 82.71%. Ante un resultado con dos picos, indique los dos picos y sus proporciones, no la media.

## 4. Cien veces más agentes, y la objeción más fuerte

**Sintético.** El mismo modelo con N = 1,400. «Cerca» significa a menos de una décima parte de la población del tamaño final determinista; una «extinción temprana» termina en una décima parte de la población o por debajo (1 agente de 14, 140 de 1,400).

| R0 | Tamaño final determinista | Simulaciones cerca de él | Extinciones tempranas |
|---|---|---|---|
| 0.8 | 4.96 | 9,995 | 9,995 |
| 1.2 | 443.03 | 1,097 | 8,455 |
| 3 | 1,316.74 | 6,634 | 3,366 |

**El tamaño no elimina la extinción.** Con N = 1,400 y R0 = 3, 3,366 simulaciones se extinguen pronto; la probabilidad exacta es 0.3339. Mientras casi todos son susceptibles, cada portador convierte, de forma independiente, a un número aleatorio de otros agentes, que sigue una distribución geométrica de media R0 porque el tiempo de permanencia es exponencial. Ese *proceso de ramificación* se extingue con probabilidad 1/R0 cuando R0 supera 1: aquí, 0.3333. Con un tiempo de permanencia fijo, el valor sería 0.0595: la proporción de extinciones descansa también sobre ese supuesto. Con R0 = 1.2, el número de extinciones depende del corte.

**Lo que compra el tamaño es la separación.** Con N = 1,400 y R0 = 3, ninguna simulación terminó entre 16 y 1,256 agentes, y el 90% de las 6,634 simulaciones por encima del corte terminó entre 1,293 y 1,337: una vez que una simulación ha despegado, 1,316.74 es un pronóstico preciso. Con N = 14, ningún hueco separa los dos picos.

El riesgo de extinción disminuye con el número m de portadores iniciales: el valor del proceso de ramificación es 1/R0 elevado a m, y las probabilidades exactas con N = 1,400 y R0 = 3 son 0.3339, 0.1117, 0.0374 y 0.0042 para m = 1, 2, 3 y 5.

### Ejercicio práctico 4

Calcule el valor del proceso de ramificación para R0 = 3 y m = 1, 2, 3 y 5, y compárelo con las probabilidades exactas anteriores. ¿Cuál es el menor m que lleva el riesgo de extinción temprana por debajo del 5%?

> **Respuesta:** `1/3 = 0.3333`, `1/9 = 0.1111`, `1/27 = 0.0370` y `1/243 = 0.0041`, cerca de los valores exactos. Tres portadores: 0.0374 está por debajo de 0.05, mientras que con dos queda 0.1117. El tamaño por sí solo no basta; varios portadores iniciales, sí.

**La objeción más fuerte a esta lectura** es que SIR podría ser la familia de modelos equivocada. Necesita portadores que conviertan a otros agentes uno a uno. Las personas que leen los mismos archivos de gobernanza pueden, en cambio, adquirir una creencia todas a la vez, de una fuente común: una difusión (*broadcast*), sin cadena, sin número de reproducción y sin extinción. Lo registrado apunta en ese sentido: los dos estados de conocimiento de ejemplo nombran a un solo profesor, la persona que encabeza el departamento, y las dos adopciones registradas proceden ambas de un documento. **Este *fixture* (los datos y scripts que acompañan a la lección) no permite distinguir el contagio de la difusión: dos adopciones a partir de un documento y ninguna cadena no bastan para decidirlo.** Un registro de transmisión lo zanjaría, con seis elementos por agente y proposición: quién la sostiene, qué dice, de quién procede, cuándo se adoptó, cuándo dejó el agente de transmitirla y quién más estuvo expuesto sin adoptarla. El esquema del estado de conocimiento tiene claves para cuatro y, mediante su evaluación de un aprendiz cada vez, para parte del sexto; la instantánea de creencias tiene claves para tres; ninguno registra cuándo deja de transmitir un portador.

### Ejercicio práctico 5

Clasifique cada afirmación como observada, sintética, analogía o no respaldada, y dé la razón: (a) dos archivos de creencias actuales se apoyan en un mensaje de otro *pipeline*; (b) con R0 = 3, alrededor de una cuarta parte de las simulaciones entre 14 agentes no transmiten nunca la creencia; (c) un agente que sostiene una creencia está infectado; (d) las creencias se propagan entre las personas del proyecto con un R0 superior a 1.

> **Respuesta:** (a) Observada en los dos archivos y en el script que los escribe; el remitente se deduce de la descripción del esquema, no de los mensajes. (b) Sintética: 2,664 de 10,000 simulaciones (probabilidad exacta 14/53), con tasas supuestas. (c) Analogía: una palabra tomada de la epidemiología para «la sostiene y la transmite». (d) No respaldada: ningún archivo leído aquí registra a un portador que transmita una creencia a otro agente, así que R0 no puede estimarse; el registro de seis elementos lo haría observable.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** `extract.py` se niega a ejecutarse si alguno de sus 32 archivos, o cualquiera de las dos carpetas que enumera (722 archivos JSON bajo `state/`, 11 esquemas de contrato), difiere del commit fijado. `results.json` enumera las 42 autocomprobaciones; el [README](../../../fixtures/psychohistory/psy-015/README.md) da los comandos y los controles.

**Referencias de método.** Kermack, W. O., y McKendrick, A. G. (1927), «A Contribution to the Mathematical Theory of Epidemics», *Proceedings of the Royal Society of London, Series A* 115, 700–721 (modelo determinista, umbral, tamaño final). Bailey, N. T. J. (1975), *The Mathematical Theory of Infectious Diseases and its Applications*, segunda edición, Griffin. Whittle, P. (1955), «The Outcome of a Stochastic Epidemic: A Note on Bailey's Paper», *Biometrika* 42, 116–122 (brotes menores y 1/R0).

**No realizado.** No se estimó ninguna tasa a partir de datos del proyecto: los tres valores de R0 son supuestos. Solo se simuló el tamaño final, y solo con mezcla homogénea: sin red, sin agentes desiguales, sin segunda adopción. Las pruebas de forma y de claves cubren los archivos JSON bajo `state/`; aparte de un archivo de creencias YAML (sin evaluador; 10 de sus 49 elementos de evidencia citan `GPT-4o`), no se leyó ningún YAML, ningún Markdown ni ningún otro repositorio. Ningún humano ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Llevar el registro de seis elementos para un puñado de proposiciones. Si la mayoría de las adopciones nombran como fuente un documento o un único profesor, sustituir este modelo por un modelo de difusión. Si nombran a otros agentes, estimar R0 a partir de las adopciones por portador y comparar los tamaños finales observados con la sección 3.
