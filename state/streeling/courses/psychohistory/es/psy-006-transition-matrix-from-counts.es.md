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

Convertirá un registro de etiquetas en una matriz de recuentos, estimará a partir de ella probabilidades de transición, acotará una transición que nunca se observó y dirá qué añaden a los datos el suavizado y una matriz uniforme. **Pregunta de proyecto:** el repositorio guarda una matriz de transición de gobernanza uniforme de 4 estados, sin ninguna observación; ¿qué aspecto tiene una matriz estimada a partir de las transiciones de etiquetas de las que sí disponemos, y qué no puede decir?

[PSY-005](psy-005-persistence-baseline.es.md) puntuó el pronóstico «nada cambia» sobre estas etiquetas; este módulo acota la probabilidad de cambio que aquel dejaba abierta. Las distribuciones estacionarias y los tiempos de llegada vienen de [MAT-020](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-020-markov-chains-hmm.md).

## 1. Contar las transiciones y luego dividir

**Observado.** Una tarea diaria ejecuta [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), al que el repositorio llama *feeder* (el «alimentador»): añade una fila por cada *artefacto* de gobernanza (una política, un esquema, una habilidad) a [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), y las filas de un mismo lanzamiento forman una *ejecución*. Cada fila lleva un `effectiveness_to`, el valor de verdad atribuido a una proposición escrita sobre el artefacto: T (verdadero), P (probable), U (desconocido), D (dudoso), F (falso) o C (contradictorio). [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/extract.py) toma una instantánea de los cinco archivos en el commit `4b03838` y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-006/observed-input.json): 1,548 filas, 88 ejecuciones, 18 artefactos.

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

**Calculado.** Tratemos las etiquetas como una *cadena de Markov*: la etiqueta siguiente depende solo de la actual, a través de una matriz de probabilidades fija, la misma para todos los artefactos. La *estimación de máxima verosimilitud*, la matriz que hace más probables los pares observados, es cada fila de recuentos dividida por su total (Anderson y Goodman 1957):

```text
estimación p(a→b) = n_ab / n_a      n_ab = pares de a a b, n_a = pares que parten de a
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/analyze.py) la escribe en [`results.json`](../../../fixtures/psychohistory/psy-006/results.json): 1 en la diagonal para T, P, F y C, 174/175 = 0.994286 para U→U y 1/175 = 0.005714 para U→F. Leída literalmente, la matriz dice que cuatro etiquetas nunca cambian y que una etiqueta desconocida espera 175 pares en promedio y luego siempre se vuelve falsa. Todo ello descansa sobre un solo par.

Además, una matriz pertenece a un paso temporal determinado, y estos pares mezclan al menos dos. 1,518 pares unen dos ejecuciones consecutivas del feeder (intervalos de 0.001 a 6.453 días, mediana 0.999). Los otros 11 parten de una *fila semilla* (con la marca `baseline: true`, fechada el 2026-05-01) y llegan a la primera ejecución del feeder, 78.5 días después; el único cambio, de U a F, es uno de ellos. Entre ejecuciones del feeder la estimación es la matriz identidad sobre cinco etiquetas.

### Ejercicio práctico 1

A partir de la matriz de recuentos, estime la fila U. ¿Cuál es la estimación para la fila D? ¿En qué se convierte la fila U sobre los 1,518 pares entre ejecuciones del feeder, donde tiene 172 pares y ninguna salida?

> **Respuesta:** `174 / 175 = 0.994286` para U→U, `1 / 175 = 0.005714` para U→F, 0 en el resto. La fila D vale `0 / 0`, indefinida: los datos callan, lo que no es una estimación de cero. Entre ejecuciones del feeder la fila vale `172 / 172 = 1` para U→U: la única estimación fuera de la diagonal de la matriz proviene de un par de 78.5 días.

## 2. Acotar lo que nunca se observó

Un recuento de cero no hace que una probabilidad sea cero. Una transición con probabilidad p en cada uno de n ensayos independientes queda sin verse —un registro *limpio*— con probabilidad (1 − p)^n. La *cota superior* es el mayor p que un registro limpio no rechaza al nivel del 5%:

```text
(1 − p)^n = 0.05   →   cota superior exacta al 95% = 1 − 0.05^(1/n)
regla de tres: en torno a 3 / n, ya que −ln 0.05 = 2.9957
```

La *regla de tres* es el atajo descrito por Hanley y Lippman-Hand (1983). **Calculado** para la salida de cada etiqueta, contando un par como un ensayo:

| Etiqueta abandonada | Pares limpios | Cota exacta | 3/n |
|---|---|---|---|
| T | 775 | 0.386% | 0.387% |
| P | 406 | 0.735% | 0.739% |
| C | 87 | 3.385% | 3.448% |
| F | 86 | 3.423% | 3.488% |
| cualquier etiqueta, entre ejecuciones del feeder | 1,518 | 0.197% | 0.198% |

La fila U tiene una salida en 175 pares; su cota, 2.682%, es el p al que «como máximo una salida en 175 pares» tiene probabilidad 0.05 (Clopper y Pearson 1934). La fila D no tiene ningún ensayo, de modo que no tiene ninguna cota por debajo del 100%. La regla de tres supera la cota exacta en un 1.9% de esa cota con 86 pares y en un 15.9% con 10 ensayos.

Las cotas son unilaterales ([PSY-004](psy-004-how-large-is-large.es.md) y [PSY-013](../en/psy-013-four-scores-and-a-trend.md) usan el intervalo bilateral, 0.025 en cada cola) y se toman de fila en fila; juntas se cumplen a menos del 95%. **La objeción más fuerte** recae sobre la palabra «independientes». Una etiqueta es una evaluación escrita que cambia solo cuando se edita su registro, y una misma sesión puede abarcar varios artefactos. En un extremo de la dependencia entre artefactos, donde las etiquetas de una ejecución cambian todas juntas o ninguna, una ejecución es un ensayo: los 86 pasos entre ejecuciones del feeder acotan entonces la probabilidad de cambio en un 3.423% por par, no en un 0.197%. Si, en cambio, la etiqueta de cada artefacto es una evaluación, los ensayos son los artefactos: la fila T tiene nueve y las filas F y C una cada una; 0 de 9 abandonaron T, una cota del 28.313% sobre todo el registro, y un solo artefacto no da ninguna cota por debajo del 95%. Esta muestra no permite situar la verdad; el historial de ediciones de `state/evolution/`, donde se escriben las evaluaciones, mostraría cómo se revisan las etiquetas.

### Ejercicio práctico 2

Calcule la cota exacta y la regla de tres para la salida de F (86 pares, ninguna salida). Un colega concluye que «F es definitivo». ¿Qué respaldan los datos?

> **Respuesta:** `1 − 0.05^(1/86) = 0.034234` y `3 / 86 = 0.034884`. Los datos respaldan «la probabilidad de abandonar F en un par está por debajo del 3.423%, al nivel del 95%, si los 86 pares son ensayos independientes», no «F es definitivo». Los 86 pares son un solo artefacto leído en 87 ejecuciones consecutivas: contados como una sola evaluación, no dan ninguna cota por debajo del 95%.

## 3. El suavizado es un previo, y un previo es una afirmación

El *suavizado por suma de uno* añade un pseudorrecuento de 1 a cada celda antes de dividir, de modo que ninguna estimación sea cero:

```text
p suavizada (a→b) = (n_ab + 1) / (n_a + k)      k = número de etiquetas, aquí 6
```

Es el promedio de las matrices que siguen siendo plausibles después de los datos cuando, antes de ellos, todo conjunto de probabilidades de fila se tenía por igualmente plausible: un *previo uniforme*. **Calculado:**

- Fila D, sin pares: cada destino recibe 1/6. Sin datos, la suma de uno devuelve la fila uniforme.
- Fila U entre los 11 pares de filas semilla (2 permanecen, 1 pasa a F): permanecer cae de 2/3 a (2 + 1)/(3 + 6) = 1/3, y 4/9 de la probabilidad recae sobre cuatro destinos nunca observados.
- Fila T, 775 pares: la salida recibe 5/781 = 0.64%, por encima de la cota del 0.386%.

Para toda fila limpia de 5 a 2,000 pares, la suma de uno sobre seis etiquetas afirma más salidas de las que la fila permite al nivel del 95%; un pseudorrecuento de 0.5 nunca lo hace en ese rango. Lo deciden los pseudorrecuentos puestos sobre las cinco salidas, 5 o 2.5 frente al 3 de la regla, no los datos.

**Observado.** El repositorio contiene una tabla semilla sobre estas seis letras: la máquina `belief_hexavalent` de [`state/driver/transition-weights.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L22). Mantiene T con un peso de 0.9 y [declara U→F como prohibida](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L49). **Calculado bajo un supuesto que el archivo no enuncia**, que un paso de la tabla equivale a un par: la tabla espera 492.4 etiquetas cambiadas entre los 1,518 pares que hay entre ejecuciones del feeder, donde no ocurrió ninguno. El único cambio registrado, U→F, es un salto que la tabla prohíbe en un paso (0.0825 en dos, pasando por D o C); un par de 78.5 días no puede mostrar cuántos pasos abarcó. Así, una matriz de recuentos casi vacía puede aun así descartar un candidato a un paso temporal enunciado. Leído como un previo, un cero es lo contrario del exceso de la suma de uno: ninguna cantidad de datos puede elevarlo.

### Ejercicio práctico 3

Aplique la suma de uno sobre seis etiquetas a la fila F (86 pares, todos F→F): dé las probabilidades suavizadas de permanecer y de salir, y compare la segunda con la cota del ejercicio 2.

> **Respuesta:** Permanecer: `(86 + 1) / (86 + 6) = 87/92 = 0.945652`. Cada una de las demás etiquetas recibe `1/92`, así que salir recibe `5/92 = 0.054348`, es decir, el 5.435%, por encima de la cota del 3.423%: la fila suavizada afirma más cambio del que permiten sus propios 86 pares al nivel del 95%.

## 4. Qué afirma la matriz uniforme almacenada

**Observado.** [`state/markov/transition-matrix.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/transition-matrix.json) tiene cuatro estados, Healthy, Watch, Warning y Freeze, y 0.25 en cada celda; su nota empieza por «Uniform prior — no observations yet.» [`predictions.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/predictions.json) contiene una lista vacía, y el archivo `engine-state.json` que la nota nombra no está en la carpeta. La [especificación](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L29) asigna uno de los cuatro estados a cada ciclo de gobernanza tomado en su conjunto, a partir únicamente de una puntuación de resiliencia y de una razón de inflación de artefactos (LOLLI/ERGOL).

**Calculado.** Esta es de nuevo la fila D: la suma de uno sin datos, con k = 4. Siendo todas las filas iguales, el estado siguiente no depende del actual. Desde Healthy, un Freeze tiene probabilidad 0.25 en el ciclo siguiente, 0.578125 en 3 ciclos y 0.943686 en 10; la espera media del primer Freeze es de 4 ciclos y, a la larga, una cuarta parte de los ciclos están congelados. La fórmula de la especificación, [`cycles_to_freeze = log(0.5) / log(P(not_freeze))`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L151), da 2.409 ciclos para P(not_freeze) = 0.75 (el punto en que la probabilidad de un Freeze alcanza la mitad, no la espera media), mientras que su [alerta](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L168), que se lanza «When P(Freeze) > 0.3», permanece muda.

**Sintético.** [`scenarios.json`](../../../fixtures/psychohistory/psy-006/scenarios.json) define una matriz «pegajosa» imaginaria que mantiene cada estado con probabilidad 0.97 y reparte el resto por igual. Su distribución estacionaria es la misma y, sin embargo, un Freeze en 10 ciclos tiene probabilidad 0.095618 y la espera media es de 100 ciclos. Las proporciones a largo plazo no identifican una matriz; la uniforme es el miembro sin memoria de esa familia, una afirmación concreta y no una afirmación neutra.

**Dos espacios de estados.** Las etiquetas describen 18 artefactos; los estados de gobernanza describen el sistema entero, uno por ciclo. Ninguna etiqueta entra en esa clasificación, así que los recuentos de etiquetas no dicen nada sobre Healthy→Freeze. Un estado registrado por ciclo sí lo diría: 59 transiciones que salen de Healthy, ninguna hacia Freeze, rebajarían la cota de esa transición al 5%. No se registra ninguno: el registro de pronósticos está vacío.

### Ejercicio práctico 4

Partiendo de Healthy, calcule la probabilidad de un Freeze en 3 ciclos y la espera media del primer Freeze, bajo la matriz almacenada y bajo la pegajosa (cada uno de los demás estados: 0.01).

> **Respuesta:** Almacenada: cada ciclo es un Freeze con probabilidad 0.25, así que `1 − 0.75^3 = 37/64 = 0.578125` y la espera es de `1 / 0.25 = 4` ciclos. Pegajosa: desde cualquier otro estado un Freeze tiene probabilidad 0.01, así que `1 − 0.99^3 = 0.029701` y `1 / 0.01 = 100` ciclos.

### Ejercicio práctico 5

Un compañero quiere rellenar la matriz de gobernanza a partir de la matriz de etiquetas: «las etiquetas casi nunca cambian, así que Healthy sigue siendo Healthy». Acepte o rechace, indicando su criterio. ¿Cuántos ciclos consecutivos sin Freeze rechazarían el 0.25 almacenado al nivel del 5%?

> **Respuesta:** Rechazar. Un recuento es evidencia solo para el espacio de estados y el paso en los que se contó: las etiquetas son valores de verdad de 18 artefactos, los estados de gobernanza clasifican el sistema entero una vez por ciclo, y la especificación clasifica un ciclo sin ninguna etiqueta. `0.75^10 = 0.056314` está por encima de 0.05 y `0.75^11 = 0.042235` por debajo: 11 ciclos consecutivos sin Freeze.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los cinco archivos de la tendencia de calidad, dos de los tres archivos de `state/markov/`, la especificación y la tabla semilla enlazados más arriba. El [README](../../../fixtures/psychohistory/psy-006/README.md) del *fixture* —la carpeta de datos y scripts que reproduce las cifras— da los comandos y las comprobaciones.

**Referencias de método.** Anderson, T. W., y Goodman, L. A. (1957), «Statistical Inference about Markov Chains», *Annals of Mathematical Statistics* 28(1), 89–110, [doi:10.1214/aoms/1177707039](https://doi.org/10.1214/aoms/1177707039). Hanley, J. A., y Lippman-Hand, A. (1983), «If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators», *JAMA* 249(13), 1743–1745, [doi:10.1001/jama.1983.03330370053031](https://doi.org/10.1001/jama.1983.03330370053031). Clopper, C. J., y Pearson, E. S. (1934), «The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial», *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).

**No realizado.** No se clasificó ningún estado de gobernanza, así que no se puso a prueba nada de la matriz de 4 estados, aunque las entradas del clasificador se registraron unas pocas veces: [cuatro puntuaciones de resiliencia](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json), que PSY-013 lee, y [una razón](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json). No se pusieron a prueba el supuesto de Markov ni la constancia de la matriz en el tiempo: un solo cambio no da nada sobre lo que probarlos. Puntuar pronósticos probabilísticos sobre estas etiquetas corresponde a PSY-016. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Comparar los bloques `assessment` a lo largo del historial de Git de `state/evolution/` para contar cuántas veces se reexaminó cada valor de verdad. Si son un puñado de veces, las cotas por par dan paso a cotas por evaluación mucho más amplias, y la matriz identidad de la sección 1 registra archivos sin revisar, no artefactos estables.
