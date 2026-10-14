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

Calculará un número de reproducción y su umbral, hallará el tamaño final que predice una curva epidémica determinista, simulará el mismo modelo suceso a suceso y leerá la distribución de la que se extrae una sola trayectoria. **Pregunta de proyecto:** el departamento inscribe una «belief state epidemiology». Si una creencia se propaga entre 14 agentes, ¿cuánto se aparta una sola trayectoria de la curva epidémica determinista?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lee un desplazamiento de las etiquetas de creencia como indicio de un cambio de régimen; este módulo pregunta qué puede pronosticar un modelo de propagación. [PSY-004](psy-004-how-large-is-large.es.md) estudia 14 agentes cuyas respuestas comparten una causa, y PSY-017 la creencia de calibración que aparece en la sección 1.

## 1. El modelo y qué significa aquí «infectado»

**Observado.** El [registro del departamento](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) inscribe, como séptima de diez líneas de investigación, «Belief state epidemiology — how beliefs spread across agents and repos», y su principio clave habla de «14 personas across 4 repos». [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/extract.py) guarda lo que el repositorio registra sobre creencias en el commit `4b03838` en [`observed-input.json`](../../../fixtures/psychohistory/psy-015/observed-input.json): los 8 archivos de creencia actuales de [`state/beliefs/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs) y 13 archivados. Ninguna proposición aparece bajo dos poseedores (0 de 21), pero este recuento no podría haber mostrado que se comparta: los 12 archivos con contenido tienen un solo evaluador, la persona de gobernanza Demerzel, y los otros 9 son armazones vacíos.

Dos archivos actuales nombran un origen externo a su evaluador: `confidence-calibration` y `remediation-effectiveness` descansan cada uno en un único elemento de evidencia, un mensaje `ml-feedback-recommendation` cuya justificación y confianza [el script que lo aplica](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py) copia en la creencia de Demerzel. Su esquema dice «from an ix ML pipeline to Demerzel»; los dos mensajes no están en el repositorio, así que el remitente se conoce solo por esa descripción y por la docstring del script. Cada uno es un solo salto, de un documento a un único poseedor.

Dos tipos de registro están diseñados para contener las creencias de un agente: una [instantánea de creencias](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/contracts/belief-snapshot.schema.json) (las creencias de un agente en un momento dado) y un [estado de conocimiento](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/knowledge-state.schema.json) (un docente, un aprendiz, la creencia del aprendiz antes y después). De los 722 archivos JSON de `state/`, excluida la biblioteca de cursos, ninguno tiene la forma de uno ni de otro (la prueba sí reconoce sus tres archivos de ejemplo) y ninguno tiene una clave que nombre a un docente, a un aprendiz o al remitente de un mensaje (`origin_repo`, `origin_agent`). Bajo estas pruebas, ningún archivo registra a un poseedor transmitiendo una creencia, un segundo salto, ni a un agente expuesto sin adoptarla. No se puede estimar ninguna tasa, así que todo lo que sigue es **sintético**.

**Analogía.** En el modelo SIR de la epidemiología, un agente es *susceptible* (S) hasta que adopta la creencia, *infectado* (I) mientras la sostiene y la transmite, y *recuperado* (R) en cuanto deja de transmitirla. «Infectado» no significa equivocado ni dañino; nombra el estado de transmitir. Entre N agentes, cada poseedor transmite la creencia a agentes escogidos al azar a una tasa β y deja de transmitir a una tasa γ:

```text
adopción:                (S, I) -> (S-1, I+1)   a la tasa beta*S*I/N
deja de transmitir:      (S, I) -> (S, I-1)     a la tasa gamma*I
R0 = beta/gamma
P(el próximo suceso es una adopción) = R0*S / (R0*S + N)
```

El *número básico de reproducción* R0 es el número medio de agentes que un poseedor convierte en una población grande cuando todos los demás son susceptibles. La última línea es la *cadena de saltos incorporada*: dice qué suceso viene después y pasa por alto el cuándo. El *tamaño final*, el número de agentes que alguna vez sostuvieron la creencia, depende solo de ese orden, así que [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/analyze.py) no extrae ningún tiempo de espera.

Supuestos, en [`scenarios.json`](../../../fixtures/psychohistory/psy-015/scenarios.json): N = 14 (el recuento del principio clave; PSY-004 encuentra 17 archivos de persona en la fijación) y N = 1,400; un poseedor inicial; R0 = 0.8, 1.2 y 3.

### Ejercicio práctico 1

Con N = 14, R0 = 3 y un poseedor inicial, ¿cuál es la probabilidad de que el primer suceso sea una adopción? ¿Y de que la creencia nunca se transmita? Vuelva a calcular la segunda para N = 1,400.

> **Respuesta:** Con S = 13, `3×13 / (3×13 + 14) = 39/53 = 0.7358`. En caso contrario, el único poseedor se detiene primero y la creencia se extingue con él: `14/53 = 0.2642`. Para N = 1,400: `1,400 / (3×1,399 + 1,400) = 1,400/5,597 = 0.2501`.

## 2. La curva determinista y su umbral

Sustituyamos los recuentos por proporciones s, i, r de una población grande y los sucesos aleatorios por sus tasas medias, con el tiempo medido en periodos medios de tenencia (1/γ):

```text
ds/dt = -R0*s*i        di/dt = R0*s*i - i        dr/dt = i
los poseedores aumentan mientras R0*s > 1
tamaño final z:   1 - z = s0 * exp(-R0*z)
```

Esta es la curva de *campo medio*: cada agente siente el promedio de todos los demás. En su *umbral*, R0 × s = 1, cada poseedor es reemplazado por exactamente uno. La *ecuación del tamaño final* da la proporción z que sostiene la creencia en algún momento.

**Sintético.** Para 14 agentes (s0 = 13/14) la ecuación da 3.13 agentes con R0 = 0.8, 6.65 con R0 = 1.2 y 13.24 con R0 = 3. Con R0 = 3 la curva integrada sube a 4.55 poseedores simultáneos tras 1.59 periodos de tenencia y termina en esos mismos 13.24 (la comprobación de respuesta conocida). Con R0 = 1.2 alcanza un máximo de 1.07 poseedores y, aun así, termina en 6.65.

### Ejercicio práctico 2

Para N = 14 y un poseedor inicial, calcule R0 × S/N al principio para los tres valores de R0. Donde pase de 1, ¿tras cuántas adopciones dejan de aumentar los poseedores?

> **Respuesta:** `0.8 × 13/14 = 0.7429`, `1.2 × 13/14 = 1.1143`, `3 × 13/14 = 2.7857`. Con R0 = 0.8 la curva no sube nunca. Los poseedores aumentan mientras S supere N/R0: `14/1.2 = 11.67`, así que el crecimiento se detiene en cuanto S vale 11, tras `13 − 11 = 2` adopciones; `14/3 = 4.67`, así que en cuanto S vale 4, tras `13 − 4 = 9`.

## 3. Catorce agentes: la distribución de la que viene una trayectoria

**Sintético.** Trayectorias por tamaño final, sobre 10,000 trayectorias para cada R0 ([`results.json`](../../../fixtures/psychohistory/psy-015/results.json), sección `cases`):

```text
tamaño final   1     2    3    4    5    6    7    8    9   10   11   12    13    14
R0 = 0.8    5708  1553  818  520  364  273  231  176  133  101   65   41    11     6
R0 = 1.2    4706  1253  751  504  451  371  319  302  324  291  261  244   153    70
R0 = 3      2664   606  267  167  124  114  119  112  175  237  414  809  1464  2728
```

- **R0 = 3 tiene dos jorobas.** 2,664 trayectorias no pasan nunca del primer poseedor y 4,192 terminan en 13 o 14. El 13.24 determinista cae dentro de la joroba alta: 5,001 trayectorias terminan en 12, 13 o 14, a menos de 1.4 agentes (una décima parte de la población) de él. La curva describe la mitad de las trayectorias.
- **La media cae en el valle.** Vale 8.38, y los tamaños de 5 a 8 son los cuatro resultados más raros.
- **R0 = 1.2 tiene una sola joroba, en 1, y una larga repisa**, igual que R0 = 0.8 al otro lado del umbral. Solo 992 trayectorias terminan en 6, 7 u 8, en torno al 6.65 determinista.

**Comprobación calculada.** Sumar sobre todos los caminos de la misma cadena da probabilidades exactas sin ningún número aleatorio (fracciones con N = 14, sumas en coma flotante con N = 1,400). En los seis casos los recuentos simulados se mantienen a menos de 2.65 errores estándar de ellas, y la prueba rechaza recuentos simulados con otro R0.

### Ejercicio práctico 3

A partir de la fila R0 = 3: ¿qué proporción de las trayectorias termina con 2 agentes como máximo, y con al menos 12? ¿Qué proporción termina en 8 o 9, los enteros que rodean la media? ¿Es «unos 8 agentes» un pronóstico utilizable?

> **Respuesta:** `2,664 + 606 = 3,270` trayectorias, el 32.70%. `809 + 1,464 + 2,728 = 5,001` trayectorias, el 50.01%. `112 + 175 = 287` trayectorias, el 2.87%. No: los dos extremos tienen `3,270 + 5,001 = 8,271` trayectorias, el 82.71%. Para un resultado de dos jorobas, enuncie las dos jorobas y sus proporciones, no el promedio.

## 4. Cien veces más agentes y la objeción más fuerte

**Sintético.** El mismo modelo con N = 1,400. «Cerca» significa a menos de una décima parte de la población del tamaño final determinista; una «extinción temprana» termina en una décima parte de la población o por debajo (1 agente de 14, 140 de 1,400).

| R0 | Tamaño final determinista | Trayectorias cerca de él | Extinciones tempranas |
|---|---|---|---|
| 0.8 | 4.96 | 9,995 | 9,995 |
| 1.2 | 443.03 | 1,097 | 8,455 |
| 3 | 1,316.74 | 6,634 | 3,366 |

**El tamaño no elimina la extinción.** Con N = 1,400 y R0 = 3, 3,366 trayectorias se extinguen pronto; la probabilidad exacta es 0.3339. Mientras casi todo el mundo es susceptible, cada poseedor convierte de forma independiente a un número aleatorio de otros, geométrico con media R0 porque el tiempo de tenencia es exponencial. Ese *proceso de ramificación* se extingue con probabilidad 1/R0 cuando R0 pasa de 1: aquí 0.3333. Con un tiempo de tenencia fijo el valor sería 0.0595: la proporción de extinciones descansa también en ese supuesto. Con R0 = 1.2 el recuento de extinciones depende del corte.

**Lo que el tamaño compra es separación.** Con N = 1,400 y R0 = 3 ninguna trayectoria terminó entre 16 y 1,256 agentes, y el 90% de las 6,634 trayectorias por encima del corte terminó entre 1,293 y 1,337: una vez que una trayectoria ha despegado, 1,316.74 es un pronóstico afilado. Con N = 14 ningún hueco separa las jorobas.

El riesgo de extinción baja con el número m de poseedores iniciales: el valor de ramificación es 1/R0 elevado a m, y las probabilidades exactas con N = 1,400 y R0 = 3 son 0.3339, 0.1117, 0.0374 y 0.0042 para m = 1, 2, 3 y 5.

### Ejercicio práctico 4

Calcule el valor de ramificación para R0 = 3 y m = 1, 2, 3 y 5, y compárelo con las probabilidades exactas de arriba. ¿Cuál es el menor m que baja el riesgo de una extinción temprana por debajo del 5%?

> **Respuesta:** `1/3 = 0.3333`, `1/9 = 0.1111`, `1/27 = 0.0370` y `1/243 = 0.0041`, cercanos a los valores exactos. Tres poseedores: 0.0374 está por debajo de 0.05, mientras que dos dejan 0.1117. El tamaño por sí solo no basta; varios poseedores iniciales sí.

**La objeción más fuerte a esta lectura** es que SIR quizá no sea la familia de modelos adecuada. Necesita poseedores que conviertan a otros agentes uno por uno. Unas personas que leen los mismos archivos de gobernanza pueden, en cambio, adquirir una creencia a la vez, de una fuente común: una difusión, sin cadena, sin número de reproducción y sin extinción. Lo registrado apunta en esa dirección: los dos estados de conocimiento de ejemplo nombran a un solo docente, la persona que encabeza el departamento, y las dos adopciones registradas vienen ambas de un documento. **Este fixture no permite distinguir el contagio de la difusión: dos adopciones a partir de un documento y ninguna cadena son demasiado poco para decidirlo.** Un registro de transmisión lo zanjaría, con seis elementos por agente y proposición: quién la sostiene, qué dice, de quién vino, cuándo se adoptó, cuándo el agente dejó de transmitirla y quién más estuvo expuesto sin adoptarla. El esquema de estado de conocimiento tiene claves para cuatro y, mediante su evaluación de un aprendiz a la vez, para parte del sexto; la instantánea de creencias tiene claves para tres; ninguno registra cuándo un poseedor se detiene.

### Ejercicio práctico 5

Clasifique cada afirmación como observada, sintética, analogía o sin respaldo, con el motivo: (a) dos archivos de creencia actuales descansan en un mensaje de otra canalización; (b) con R0 = 3, cerca de una cuarta parte de las trayectorias entre 14 agentes no transmite nunca la creencia; (c) un agente que sostiene una creencia está infectado; (d) las creencias se propagan entre las personas del proyecto con un R0 mayor que 1.

> **Respuesta:** (a) Observada en los dos archivos y en el script que los escribe; el remitente se lee en la descripción del esquema, no en los mensajes. (b) Sintética: 2,664 de 10,000 trayectorias (probabilidad exacta 14/53), bajo tasas supuestas. (c) Analogía: una palabra tomada de la epidemiología para «la sostiene y la transmite». (d) Sin respaldo: ningún archivo leído aquí registra a un poseedor transmitiendo una creencia a otro agente, así que R0 no puede estimarse; el registro de seis elementos lo haría observable.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** `extract.py` se niega a ejecutarse si alguno de sus 32 archivos, o cualquiera de las dos carpetas que enumera (722 archivos JSON bajo `state/`, 11 esquemas de contrato), difiere de la fijación. `results.json` enumera las 42 autocomprobaciones; el [README](../../../fixtures/psychohistory/psy-015/README.md) da los comandos y los controles.

**Referencias de método.** Kermack, W. O., y McKendrick, A. G. (1927), «A Contribution to the Mathematical Theory of Epidemics», *Proceedings of the Royal Society of London, Series A* 115, 700–721 (modelo determinista, umbral, tamaño final). Bailey, N. T. J. (1975), *The Mathematical Theory of Infectious Diseases and its Applications*, segunda edición, Griffin. Whittle, P. (1955), «The Outcome of a Stochastic Epidemic: A Note on Bailey's Paper», *Biometrika* 42, 116–122 (los brotes menores y 1/R0).

**No realizado.** No se estimó ninguna tasa a partir de datos del proyecto: los tres valores de R0 son supuestos. Solo se simuló el tamaño final, y solo con mezcla uniforme: sin red, sin agentes desiguales, sin una segunda adopción. Las pruebas de forma y de claves cubren los archivos JSON bajo `state/`; más allá de un archivo de creencia en YAML (sin evaluador; 10 de sus 49 elementos de evidencia citan `GPT-4o`), no se leyó ningún YAML, ningún Markdown ni ningún otro repositorio. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Llevar el registro de seis elementos para un puñado de proposiciones. Si la mayoría de las adopciones nombran un documento o un único docente como su origen, sustituir este modelo por un modelo de difusión. Si nombran a otros agentes, estimar R0 a partir de las adopciones por poseedor y comparar los tamaños finales observados con la sección 3.
