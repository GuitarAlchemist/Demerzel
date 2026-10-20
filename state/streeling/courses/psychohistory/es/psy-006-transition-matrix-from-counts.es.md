---
module_id: psy-006-transition-matrix-from-counts
department: psychohistory
course: "Estimar una matriz de transición a partir de recuentos observados"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "mat-020-markov-chains-hmm"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-006
version: "0.1.0"
---

# Estimar una matriz de transición a partir de recuentos observados

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo convertirá un registro de etiquetas en una matriz de recuentos, estimará a partir de ella probabilidades de transición, acotará una transición que nunca se observó y dirá qué añaden a los datos el suavizado y una matriz uniforme. **Pregunta de proyecto:** el repositorio guarda una matriz de transición de gobernanza uniforme, de 4 estados y sin ninguna observación; ¿qué aspecto tiene una matriz estimada a partir de las transiciones de etiquetas de las que sí disponemos, y qué es lo que no puede decir?

[PSY-005](psy-005-persistence-baseline.es.md) puntuó el pronóstico «nada cambia» sobre estas etiquetas; este módulo acota la probabilidad de cambio que aquel dejó abierta. Las distribuciones estacionarias y los tiempos de primera llegada (*hitting times*) proceden de [MAT-020](../../mathematics/es/mat-020-markov-chains-hmm.es.md).

## 1. Contar las transiciones y después dividir

**Observado.** Una tarea diaria ejecuta [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), el *feeder* (el «alimentador»): añade a [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) una fila por *artefacto* de gobernanza (una política, un esquema, una habilidad), y las filas de un mismo lanzamiento forman una *ejecución*. Cada fila lleva `effectiveness_to`, el valor de verdad atribuido a una proposición escrita sobre el artefacto: T (verdadero), P (probable), U (desconocido), D (dudoso), F (falso) o C (contradictorio). [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/extract.py) toma una instantánea de los cinco archivos en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-006/observed-input.json): 1,548 filas, 88 ejecuciones, 18 artefactos.

Una *transición* es un par de filas consecutivas, como en PSY-005: la etiqueta de un artefacto en una fila y en su fila siguiente. Eso da 1,548 − 18 = 1,530 pares de filas; uno empieza en una fila sin etiqueta, lo que deja **1,529**. La *matriz de recuentos* contiene el número de pares que van de cada etiqueta (fila) a cada etiqueta (columna):

```text
de \ a        T     P     U     D     F     C    pares
T           775     0     0     0     0     0      775
P             0   406     0     0     0     0      406
U             0     0   174     0     1     0      175
D             0     0     0     0     0     0        0
F             0     0     0     0    86     0       86
C             0     0     0     0     0    87       87
```

**Calculado.** Trate las etiquetas como una *cadena de Markov*: la etiqueta siguiente depende solo de la actual, a través de una matriz de probabilidades fija, la misma para todos los artefactos. La *estimación de máxima verosimilitud*, la matriz que hace más probables los pares observados, es cada fila de recuentos dividida por su total (Anderson y Goodman 1957):

```text
estimación p(a→b) = n_ab / n_a      n_ab = pares que salen de a y llegan a b, n_a = pares que salen de a
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/analyze.py) la escribe en [`results.json`](../../../fixtures/psychohistory/psy-006/results.json): 1 en la diagonal para T, P, F y C, 174/175 = 0.994286 para U→U y 1/175 = 0.005714 para U→F. Leída al pie de la letra, la matriz dice que cuatro etiquetas no cambian nunca y que una etiqueta desconocida espera de media 175 pares y después pasa siempre a falsa. Todo ello descansa sobre un único par.

Una matriz corresponde además a una sola longitud de paso, y estos pares mezclan al menos dos. De ellos, 1,518 unen dos ejecuciones consecutivas del feeder (con separaciones de 0.001 a 6.453 días y una mediana de 0.999). Los otros 11 empiezan en una *fila semilla* (marcada `baseline: true`, con fecha 2026-05-01) y terminan en la primera ejecución del feeder, 78.5 días después; el único cambio, de U a F, es uno de ellos. Entre ejecuciones del feeder, la estimación es la matriz identidad sobre cinco etiquetas.

### Ejercicio práctico 1

A partir de la matriz de recuentos, estime la fila U. ¿Cuál es la estimación para la fila D? ¿En qué se convierte la fila U sobre los 1,518 pares entre ejecuciones del feeder, donde tiene 172 pares y ninguna salida?

> **Respuesta:** `174 / 175 = 0.994286` para U→U, `1 / 175 = 0.005714` para U→F, 0 en las demás celdas. La fila D es `0 / 0`, indefinida: los datos callan, y eso no es una estimación de cero. Entre ejecuciones del feeder, la fila es `172 / 172 = 1` para U→U: la única estimación de la matriz fuera de la diagonal procede de un par de 78.5 días.

## 2. Acotar lo que nunca se observó

Un recuento nulo no hace nula una probabilidad. Una transición con probabilidad p en cada uno de n ensayos independientes no se observa nunca, lo que da un historial *limpio*, con probabilidad (1 − p)^n. La *cota superior* es el mayor p que un historial limpio no rechaza al nivel del 5%:

```text
(1 − p)^n = 0.05   →   cota superior exacta al 95% = 1 − 0.05^(1/n)
regla del tres: unos 3 / n, ya que −ln 0.05 = 2.9957
```

La *regla del tres* (*rule of three*) es el atajo descrito por Hanley y Lippman-Hand (1983). **Calculado** para la salida de cada etiqueta, contando cada par como un ensayo:

| Etiqueta que se abandona | Pares limpios | Cota exacta | 3/n |
|---|---|---|---|
| T | 775 | 0.386% | 0.387% |
| P | 406 | 0.735% | 0.739% |
| C | 87 | 3.385% | 3.448% |
| F | 86 | 3.423% | 3.488% |
| cualquier etiqueta, entre ejecuciones del feeder | 1,518 | 0.197% | 0.198% |

La fila U tiene una salida en 175 pares; su cota, el 2.682%, es el p para el que «como mucho una salida en 175 pares» tiene probabilidad 0.05 (Clopper y Pearson 1934). La fila D no tiene ningún ensayo y, por tanto, ninguna cota por debajo del 100%. La regla del tres supera la cota exacta en un 1.9% de esa cota con 86 pares y en un 15.9% con 10 ensayos.

Las cotas son unilaterales ([PSY-004](psy-004-how-large-is-large.es.md) y [PSY-013](psy-013-four-scores-and-a-trend.es.md) usan el intervalo bilateral, 0.025 en cada cola) y se calculan fila por fila; en conjunto se cumplen a un nivel inferior al 95%. **La objeción más fuerte** es la palabra «independientes». Una etiqueta es una evaluación escrita que solo cambia cuando se edita su registro, y una misma sesión de trabajo puede abarcar muchos artefactos. En un extremo de la dependencia entre artefactos, cuando las etiquetas de una ejecución cambian todas a la vez o ninguna, una ejecución es un solo ensayo: los 86 pasos entre ejecuciones del feeder sitúan entonces la cota de la probabilidad de cambio en el 3.423% por par, no en el 0.197%. Si, en cambio, la etiqueta de cada artefacto es una sola evaluación, los ensayos son los artefactos: la fila T tiene nueve, y las filas F y C, uno cada una; 0 de 9 abandonaron T, lo que da una cota del 28.313% para todo el historial, y un solo artefacto no da ninguna cota por debajo del 95%. Esta muestra no permite situar la verdad; el historial de ediciones de `state/evolution/`, donde se escriben las evaluaciones, mostraría cómo se revisan las etiquetas.

### Ejercicio práctico 2

Calcule la cota exacta y la regla del tres para la salida de F (86 pares, ninguna salida). Un colega concluye que «F es definitivo». ¿Qué respaldan los datos?

> **Respuesta:** `1 − 0.05^(1/86) = 0.034234` y `3 / 86 = 0.034884`. Los datos respaldan «la probabilidad de salir de F en un par es inferior al 3.423%, al nivel del 95%, si los 86 pares son ensayos independientes», no «F es definitivo». Los 86 pares son un solo artefacto leído en 87 ejecuciones consecutivas: contados como una sola evaluación, no dan ninguna cota por debajo del 95%.

## 3. El suavizado es una distribución a priori, y una distribución a priori es una afirmación

El *suavizado de Laplace* (*add-one smoothing*) suma un pseudorrecuento de 1 a cada celda antes de dividir, de modo que ninguna estimación sea nula:

```text
p(a→b) suavizada = (n_ab + 1) / (n_a + k)      k = número de etiquetas, aquí 6
```

Es la media de las matrices que siguen siendo plausibles después de ver los datos cuando, antes de verlos, todos los conjuntos de probabilidades de una fila se consideraban igual de plausibles: una *distribución a priori uniforme*. **Calculado:**

- Fila D, sin pares: cada destino recibe 1/6. Sin datos, el suavizado de Laplace devuelve la fila uniforme.
- Fila U entre los 11 pares que empiezan en una fila semilla (2 se quedan, 1 pasa a F): la permanencia cae de 2/3 a (2 + 1)/(3 + 6) = 1/3, y 4/9 de la probabilidad recaen en cuatro destinos nunca observados.
- Fila T, 775 pares: la salida recibe 5/781 = 0.64%, por encima de la cota del 0.386%.

Para toda fila limpia de 5 a 2,000 pares, el suavizado de Laplace sobre seis etiquetas atribuye más salidas de las que la fila permite al nivel del 95%; un pseudorrecuento de 0.5 nunca lo hace en ese rango. Lo deciden los pseudorrecuentos de las cinco salidas, 5 o 2.5 frente al 3 de la regla, no los datos.

**Observado.** El repositorio contiene una tabla de pesos iniciales sobre estas seis letras: la máquina `belief_hexavalent` de [`state/driver/transition-weights.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L22). Mantiene T con un peso de 0.9 y [declara prohibida la transición U→F](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L49). **Calculado bajo un supuesto que el archivo no enuncia**, que un paso de la tabla equivale a un par: la tabla prevé 492.4 etiquetas cambiadas en los 1,518 pares entre ejecuciones del feeder, donde no se produjo ningún cambio. El único cambio registrado, U→F, es un salto que la tabla prohíbe en un paso (0.0825 en dos, pasando por D o por C); un par de 78.5 días no puede mostrar cuántos pasos abarcó. Una matriz de recuentos casi vacía puede, por tanto, descartar aun así una matriz candidata para una longitud de paso dada. Leído como distribución a priori, un cero es lo contrario del exceso del suavizado de Laplace: ninguna cantidad de datos puede elevarlo.

### Ejercicio práctico 3

Aplique el suavizado de Laplace sobre seis etiquetas a la fila F (86 pares, todos F→F): dé las probabilidades suavizadas de quedarse y de salir, y compare la segunda con la cota del ejercicio 2.

> **Respuesta:** Quedarse: `(86 + 1) / (86 + 6) = 87/92 = 0.945652`. Cada una de las demás etiquetas recibe `1/92`, así que salir recibe `5/92 = 0.054348`, es decir, el 5.435%, por encima de la cota del 3.423%: la fila suavizada afirma más cambio del que sus propios 86 pares permiten al nivel del 95%.

## 4. Lo que afirma la matriz uniforme guardada

**Observado.** [`state/markov/transition-matrix.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/transition-matrix.json) tiene cuatro estados, Healthy, Watch, Warning y Freeze (sano, vigilancia, alerta y congelación), y 0.25 en cada celda; su nota empieza por «Uniform prior — no observations yet.» (a priori uniforme; todavía sin observaciones). [`predictions.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/predictions.json) contiene una lista vacía, y el `engine-state.json` que menciona la nota no está en la carpeta. La [especificación](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L29) asigna uno de los cuatro estados a cada ciclo de gobernanza en su conjunto, solo a partir de una puntuación de resiliencia y de un cociente de inflación de artefactos (LOLLI/ERGOL).

**Calculado.** Es de nuevo la fila D: el suavizado de Laplace sin datos, con k = 4. Como todas las filas son iguales, el estado siguiente no depende del actual. Desde Healthy, un Freeze tiene probabilidad 0.25 en el ciclo siguiente, 0.578125 en un plazo de 3 ciclos y 0.943686 en un plazo de 10; la espera media hasta el primer Freeze es de 4 ciclos, y a largo plazo una cuarta parte de todos los ciclos están en Freeze. La fórmula de la especificación, [`cycles_to_freeze = log(0.5) / log(P(not_freeze))`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L151), da 2.409 ciclos para P(not_freeze) = 0.75 (el plazo en el que la probabilidad de un Freeze llega a la mitad, no la espera media), mientras que su [alerta](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L168), que salta «When P(Freeze) > 0.3», permanece en silencio.

**Sintético.** [`scenarios.json`](../../../fixtures/psychohistory/psy-006/scenarios.json) define una matriz imaginaria «pegajosa» (*sticky*), que mantiene cada estado con probabilidad 0.97 y reparte el resto a partes iguales. Su distribución estacionaria es la misma y, sin embargo, un Freeze en un plazo de 10 ciclos tiene probabilidad 0.095618 y la espera media es de 100 ciclos. Las proporciones a largo plazo no identifican una matriz; la uniforme es el miembro sin memoria de esa familia, una afirmación concreta y no una neutra.

**Dos espacios de estados.** Las etiquetas describen 18 artefactos; los estados de gobernanza describen el sistema entero, uno por ciclo. Ninguna etiqueta interviene en esa clasificación, de modo que los recuentos de etiquetas no dicen nada sobre Healthy→Freeze. Un estado registrado por ciclo sí lo diría: 59 transiciones desde Healthy, ninguna hacia Freeze, bajarían la cota de esa transición al 5%. No hay ninguno registrado: el registro de predicciones está vacío.

### Ejercicio práctico 4

Partiendo de Healthy, calcule la probabilidad de un Freeze en un plazo de 3 ciclos y la espera media hasta el primer Freeze, con la matriz guardada y con la pegajosa (cada uno de los demás estados: 0.01).

> **Respuesta:** Guardada: cada ciclo es un Freeze con probabilidad 0.25, así que `1 − 0.75^3 = 37/64 = 0.578125` y la espera es de `1 / 0.25 = 4` ciclos. Pegajosa: desde cualquier otro estado, un Freeze tiene probabilidad 0.01, así que `1 − 0.99^3 = 0.029701` y `1 / 0.01 = 100` ciclos.

### Ejercicio práctico 5

Un compañero de equipo quiere rellenar la matriz de gobernanza a partir de la matriz de etiquetas: «las etiquetas casi nunca cambian, así que Healthy se queda en Healthy». Acepte o rechace la propuesta, e indique su criterio. ¿Cuántos ciclos consecutivos sin Freeze rechazarían el 0.25 guardado al nivel del 5%?

> **Respuesta:** Se rechaza. Un recuento solo es prueba para el espacio de estados y el paso en los que se contó: las etiquetas son valores de verdad de 18 artefactos, los estados de gobernanza clasifican el sistema entero una vez por ciclo, y la especificación clasifica un ciclo sin recurrir a ninguna etiqueta. `0.75^10 = 0.056314` está por encima de 0.05 y `0.75^11 = 0.042235` por debajo: 11 ciclos consecutivos sin Freeze.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cinco archivos de la tendencia de calidad, dos de los tres archivos de `state/markov/`, la especificación y la tabla de pesos iniciales enlazadas más arriba. El [README](../../../fixtures/psychohistory/psy-006/README.md) del *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección) da los comandos y las comprobaciones.

**Referencias de método.** Anderson, T. W., y Goodman, L. A. (1957), «Statistical Inference about Markov Chains», *Annals of Mathematical Statistics* 28(1), 89–110, [doi:10.1214/aoms/1177707039](https://doi.org/10.1214/aoms/1177707039). Hanley, J. A., y Lippman-Hand, A. (1983), «If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators», *JAMA* 249(13), 1743–1745, [doi:10.1001/jama.1983.03330370053031](https://doi.org/10.1001/jama.1983.03330370053031). Clopper, C. J., y Pearson, E. S. (1934), «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial», *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).

**No realizado.** No se clasificó ningún estado de gobernanza, así que no se puso a prueba nada de la matriz de 4 estados, aunque las entradas del clasificador se registraron unas pocas veces: [cuatro puntuaciones de resiliencia](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json), que lee PSY-013, y [un cociente](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json). No se pusieron a prueba ni el supuesto de Markov ni la constancia de la matriz en el tiempo: con un solo cambio no hay nada sobre lo que ponerlos a prueba. Puntuar pronósticos probabilísticos sobre estas etiquetas corresponde a [PSY-016](psy-016-brier-score.es.md). Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Comparar los bloques `assessment` a lo largo del historial de Git de `state/evolution/` para contar con qué frecuencia se reexaminó cada valor de verdad. Si fueron un puñado de veces, las cotas por par dejan paso a cotas por evaluación mucho más amplias, y la matriz identidad de la sección 1 registra archivos sin revisar, no artefactos estables.
