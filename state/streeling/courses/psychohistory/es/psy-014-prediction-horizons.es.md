---
module_id: psy-014-prediction-horizons
department: psychohistory
course: "Horizontes de predicción: con qué rapidez crecen los errores pequeños"
level: intermediate
prerequisites: ["mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-014
version: "0.1.0"
---

# Horizontes de predicción: con qué rapidez crecen los errores pequeños

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo ejecutará un modelo dos veces desde casi el mismo punto de partida, medirá cómo cambia la diferencia entre las dos ejecuciones, resumirá ese cambio en un exponente de Lyapunov y lo convertirá en un *horizonte de predicción*: el número de pasos durante los cuales un pronóstico se mantiene dentro de una tolerancia fijada de antemano. **Pregunta de proyecto:** ¿hasta dónde se puede confiar en un modelo determinista cuando su estado inicial solo se conoce de forma aproximada?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) afirma que la psicohistoria puede «predict the broad strokes» (predecir las grandes líneas), pero no los sucesos individuales, y [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md), que los cambios individuales son impredecibles mientras que el comportamiento agregado sigue leyes estadísticas. Ninguno de los dos dice hasta dónde se sostiene un pronóstico ni qué aporta conocer mejor el presente: este módulo responde a ambas cosas para un modelo pequeño, con el exponente de la sección 2 de [MAT-024](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-024-dynamical-systems-stability-feedback.md). Las señales de alerta temprana corresponden a [PSY-012](psy-012-early-warning-false-alarms.es.md), y las reglas de alarma, a [PSY-023](psy-023-monitoring-a-plan.es.md). Todos los resultados que siguen son **sintéticos**: describen el modelo, no el proyecto.

## 1. Ejecutar el modelo dos veces

Un modelo *determinista* no contiene ningún azar: el mismo punto de partida da siempre la misma ejecución. El ejemplo pequeño clásico es el *mapa logístico* (May 1976), que actualiza un estado x comprendido entre 0 y 1 mediante

```text
x_next = r * x * (1 - x)
```

donde r es un parámetro fijo. Tras un régimen transitorio, el estado permanece en un *atractor*: un punto fijo con r = 2.9, un ciclo de dos puntos con r = 3.2 y una banda irregular con r = 3.7 y con r = 4. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-014/analyze.py) sortea 1,000 puntos de partida con una semilla fija ([`scenarios.json`](../../../fixtures/psychohistory/psy-014/scenarios.json)), deja que cada uno se estabilice durante 1,000 pasos y después lo ejecuta dos veces: una tal cual y otra desplazado por un *error inicial* de 1e-9. La *separación* es la diferencia absoluta entre las dos ejecuciones en un mismo paso.

**Sintético.** Separación mediana de los 1,000 pares, tomada de `gap_table` en [`results.json`](../../../fixtures/psychohistory/psy-014/results.json):

| Paso | r = 2.9 | r = 3.2 | r = 3.7 | r = 4 |
|---|---|---|---|---|
| 0 | 1e-9 | 1e-9 | 1e-9 | 1e-9 |
| 10 | 3.49e-10 | 1.05e-13 | 4.85e-8 | 1.04e-6 |
| 20 | 1.22e-10 | 0 | 1.72e-6 | 0.00107 |
| 30 | 4.24e-11 | 0 | 6.14e-5 | 0.537 |
| 60 | 1.8e-12 | 0 | 0.173 | 0.36 |

Un `0` indica una separación demasiado pequeña para los números de coma flotante de 64 bits del programa (sección 3), no una separación nula: recalculada con números de 1,024 bits, la mediana con r = 3.2 es de 1.1e-17 en el paso 20.

En las dos primeras columnas el error disminuye. Estos *regímenes estables* olvidan su punto de partida: los 1,000 puntos de partida estabilizados se han concentrado en el atractor, es decir, en los dos puntos del ciclo con r = 3.2 y, con r = 2.9, en el punto fijo, que el redondeo representa como dos números separados por 6.66e-16. Así, estos 1,000 pares repiten dos experimentos. En los *regímenes caóticos* de las dos últimas columnas, la separación crece en un factor aproximadamente constante por paso: es la *dependencia sensible de las condiciones iniciales*. Después deja de crecer: una separación no puede superar el tamaño del atractor.

### Ejercicio práctico 1

Con r = 2.9, un error pequeño se multiplica por 0.9 en cada paso. Compruébelo con la tabla a lo largo de diez pasos y calcule después cuántos pasos hacen falta para que un error de 1e-3 baje de 1e-6.

> **Respuesta:** `0.9^10 = 0.3487`, y la tabla da `3.49e-10 / 1e-9 = 0.349`. Un error disminuye en un factor de 1,000 en `ln(1e-6 / 1e-3) / ln(0.9) = −6.9078 / −0.105361 = 65.56` pasos, es decir, en 66 pasos; el *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección) cuenta 66 en los dos experimentos. Aquí un pronóstico mejora con el tiempo, siempre que el error de partida sea pequeño.

## 2. La tasa: un exponente de Lyapunov

Mientras una separación es pequeña, cada paso la multiplica por el valor absoluto de la pendiente del mapa en el estado actual, |r (1 − 2x)|. El *exponente de Lyapunov* λ es la media del logaritmo de ese factor a lo largo de una ejecución larga:

```text
λ = media de ln|r * (1 - 2 * x)| a lo largo de la ejecución
separación tras n pasos ≈ error inicial * e^(λ * n)      mientras la separación siga siendo pequeña
```

Un λ negativo significa que los errores disminuyen; uno positivo, que crecen en promedio en un factor e^λ por paso. **Sintético**, a partir de 1,000,000 de pasos por valor de r:

| r | λ estimado | λ conocido | e^λ |
|---|---|---|---|
| 2.9 | −0.105361 | ln 0.9 = −0.105361 | 0.9 |
| 3.2 | −0.916291 | ln 0.4 = −0.916291 | 0.4 |
| 3.7 | 0.3547 ± 0.0003 | sin forma cerrada | 1.426 |
| 4 | 0.693144 | ln 2 = 0.693147 | 2 |

Con r = 3.7 solo se dispone de la estimación; su error estándar procede de 100 bloques de 10,000 pasos. MAT-024 da 0.350235 a partir de 10,000 pasos: es el primer bloque de esta ejecución, reproducido con seis decimales.

El exponente es una media: con r = 3.2, la pendiente vale en valor absoluto 1.9165 en un punto del ciclo y 0.0835 en el otro, y su producto es 0.16 = 0.4².

### Ejercicio práctico 2

Estime λ a partir de dos entradas de la tabla de separaciones: para r = 4, a partir de los pasos 0 y 20; para r = 3.2, a partir de los pasos 0 y 10. ¿Por qué no sirve el paso 30 para r = 4?

> **Respuesta:** r = 4: `ln(0.00107 / 1e-9) / 20 = 13.8832 / 20 = 0.6942`, frente a ln 2 = 0.6931. r = 3.2: `ln(1.05e-13 / 1e-9) / 10 = −9.1616 / 10 = −0.9162`, frente a −0.9163. En el paso 30 la separación mediana es de 0.537: el crecimiento se ha detenido en el tamaño del atractor.

## 3. El horizonte y el precio de un dígito

Se llama *tolerancia* a la mayor separación que acepta quien usa un pronóstico, y *horizonte*, al primer paso en el que la separación la alcanza. Si se iguala la separación a la tolerancia en la ley de crecimiento, se obtiene

```text
horizonte ≈ ln(tolerancia / error inicial) / λ
pasos ganados por cada dígito decimal de precisión adicional = ln(10) / λ
```

**Sintético.** Horizonte medio de los 1,000 pares para una tolerancia de 0.1, junto al valor de la fórmula:

| Error inicial | r = 3.7: media | fórmula | r = 4: media | fórmula |
|---|---|---|---|---|
| 1e-3 | 12.93 | 12.98 | 6.79 | 6.64 |
| 1e-6 | 32.56 | 32.46 | 16.78 | 16.61 |
| 1e-9 | 51.54 | 51.93 | 26.78 | 26.58 |
| 1e-12 | 71.05 | 71.41 | 36.69 | 36.54 |

De 1e-3 a 1e-12, nueve dígitos más, el horizonte medio gana 58.12 pasos con r = 3.7 y 29.9 con r = 4: 6.46 y 3.32 pasos por dígito, frente a 6.49 y 3.32 según la fórmula. **En un régimen caótico, cada dígito de precisión compra el mismo número reducido de pasos.** Los umbrales escritos en la hipótesis del ciclo de investigación antes de la primera ejecución se cumplieron todos: pendiente a menos del 10% de la de la fórmula, desfase de 5 pasos como máximo y variación del desfase inferior a 2 (medido: de −0.39 a 0.22 pasos).

Donde λ es negativo no hay horizonte: con r = 2.9 y con r = 3.2, ninguna de las 20,000 combinaciones de par, error y tolerancia (1,000 pares, diez errores, tolerancias 0.1 y 0.01) alcanzó una tolerancia (40 combinaciones distintas en cada caso: los puntos de partida estabilizados son 2 números). Un detector que no se disparara nunca daría el mismo cero: como control, una ejecución iniciada en el otro punto del ciclo de dos puntos, a 0.286 de distancia, queda detectada en el paso 1 y se mantiene a 0.286. «Sin horizonte» solo vale para errores pequeños.

La aritmética fija su propio horizonte. Un *double*, el formato de coma flotante de 64 bits que usa Python, ofrece 15.95 dígitos decimales: entre 0.5 y 1, dos valores vecinos distan 2^-53 ≈ 1.11e-16. El redondeo actúa como un error inicial: frente a una ejecución desde el mismo punto de partida con números de 1,024 bits, una ejecución en doubles queda a 0.1 de distancia tras 53.27 pasos en promedio con r = 4 y tras 99.55 con r = 3.7; a partir de ahí ya no es la órbita del mapa desde su punto de partida. Los horizontes anteriores siguen siendo los del mapa: con esos números, 3 de cada 10,000 horizontes (diez errores iniciales) cambian con r = 3.7 y 1 de cada 10,000 con r = 4, en 2 pasos como máximo.

### Ejercicio práctico 3

Con r = 3.7, tome λ = 0.355 y una tolerancia de 0.1. Calcule el horizonte para un error inicial de 1e-6 y, después, lo que se gana al reducir el error a 1e-9.

> **Respuesta:** `ln(0.1 / 1e-6) / 0.355 = 11.5129 / 0.355 = 32.43` pasos (media medida: 32.56). Cada dígito vale `ln(10) / 0.355 = 6.49` pasos, así que tres dígitos compran 19.46 pasos y el horizonte pasa a 51.89. Una medición 1,000 veces más precisa alarga el horizonte en `19.46 / 32.43 = 0.60`, es decir, un 60%.

### Ejercicio práctico 4

Con r = 4, ¿qué error inicial mantendría un pronóstico dentro de 0.1 durante 100 pasos? ¿Puede proporcionarlo un double?

> **Respuesta:** `0.1 × e^(−0.693147 × 100) = 0.1 × 2^−100 = 7.89e-32`, lo que exige 31.1 dígitos decimales. Un double tiene 15.95, así que no. Si el error inicial es el espaciado entre dos doubles vecinos, la fórmula da `ln(0.1 / 1.11e-16) / 0.693147 = 49.68` pasos, cerca de los 53.27 medidos.

## 4. Más allá del horizonte, y lo que un plan puede aprovechar

Pasado el horizonte, el estado se pierde, pero no todo se pierde. **Sintético:** dos ejecuciones con r = 4 desde 0.3 y desde 0.3 + 1e-12 están a 0.1 de distancia en el paso 37, tanto en doubles como con números de 1,024 bits. En el paso 100, las dos ejecuciones calculadas valen 0.673899 y 0.002785, números que ya dependen del redondeo: desde los mismos puntos de partida, las ejecuciones con 1,024 bits dan 0.991939 y 0.735222. Sin embargo, a lo largo de 100,000 pasos, la primera ejecución calculada pasa 33,353 pasos por debajo de 0.25 y la segunda 33,525, frente a una proporción conocida de 1/3. La estadística del atractor sigue siendo predecible cuando el estado ya no lo es: es la versión, a escala de modelo, de lo que PSY-002 afirma sobre los agregados.

### Ejercicio práctico 5

Un pronóstico con r = 4 debe mantenerse dentro de 0.1 en cada uno de los 60 pasos. Opción A: medir el punto de partida una sola vez, con 1e-12 en lugar de 1e-6. Opción B: mantener 1e-6 y volver a medir cada k pasos. De 1,000 pronósticos de este tipo, 972 se mantienen dentro de la tolerancia en los 60 pasos con k = 10, 960 con 11, 924 con 12 y 284 con 16. ¿Qué opción, y con qué k máximo, mantiene dentro de la tolerancia al menos el 95% de los pronósticos a 60 pasos?

> **Respuesta:** La opción A fracasa: el horizonte de la fórmula con 1e-12 es de 36.54 pasos, y el más largo de los 1,000 horizontes medidos es de 49. La opción B funciona hasta k = 11, es decir, con 6 mediciones: `960 / 1,000 = 96.0%`, frente al 92.4% con k = 12. Elegir k = 16, es decir, el horizonte de la fórmula (16.61) redondeado hacia abajo, conserva solo el 28.4%: un horizonte es una distribución, aquí de 9 a 24 pasos en torno a una media de 16.78. El criterio es su extremo inferior, y el remedio es volver a medir, no medir mejor.

**Analogía, no medición.** Una hoja de ruta es un pronóstico a largo plazo hecho desde un presente que solo se conoce de forma aproximada. Si el proceso que hay detrás amplifica las pequeñas diferencias, conocer el presente con más detalle solo compra una prolongación fija y pequeña; lo que ayuda es volver a medir y pronosticar distribuciones. Si las amortigua, los pronósticos a largo plazo salen baratos. Nadie ha medido un exponente de Lyapunov para este proyecto: esta lección no puede decir cuál de los dos casos se aplica.

**La objeción más fuerte** es que el mapa logístico es un solo número sometido a una regla fija. Un proyecto tiene muchas variables, personas que reaccionan a los pronósticos y perturbaciones externas; con perturbaciones, los errores crecen incluso desde un punto de partida conocido a la perfección, y esta fórmula del horizonte no tiene por qué cumplirse. Una serie del proyecto puntuada en [PSY-005](psy-005-persistence-baseline.es.md) no lo zanja: «nada cambia» acertó en 1,528 de 1,529 pares de filas consecutivas (espaciadas de forma irregular), lo que muestra etiquetas que rara vez cambian, o un registro que nadie revisa, no cómo crecen los errores de pronóstico. **Este fixture no permite distinguir un proyecto caótico, uno ruidoso y uno estable.** Pronósticos fechados de una magnitud del proyecto, puntuados según su antelación, podrían empezar a hacerlo: un error que crece de forma exponencial y luego se estabiliza indica un exponente positivo; un error que se mantiene plano, un régimen estable; un error presente desde el primer paso que crece sin fase exponencial, un régimen ruidoso.

## Fuentes, límites y próxima comprobación

**Fijados en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** PSY-001, PSY-002 y MAT-024. El fixture reproduce los cuatro exponentes que MAT-024 da para estos valores de r; el recuento de pares de filas de la sección 4 es el de PSY-005.

**Fixture.** Desde la raíz del repositorio, `python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py`, y después lo mismo con `--check`. Solo lee `scenarios.json` y ejecuta 41 autocomprobaciones; su [README](../../../fixtures/psychohistory/psy-014/README.md) explica por qué la salida es idéntica byte a byte en todas las plataformas y enumera los límites.

**Referencias de método.** May, R. M. (1976), «Simple mathematical models with very complicated dynamics», *Nature* 261, 459–467. Lorenz, E. N. (1963), «Deterministic nonperiodic flow», *Journal of the Atmospheric Sciences* 20, 130–141 (dependencia sensible de las condiciones iniciales). Strogatz, S. H. (2015), *Nonlinear Dynamics and Chaos*, segunda edición, Westview Press (exponentes de Lyapunov y horizonte temporal de una predicción).

**No realizado.** No se analizó ningún dato del proyecto ni se estimó ningún exponente para ninguna magnitud del proyecto. Se estudió un solo mapa, con una sola variable, sin ruido y con una sola semilla. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Archivar en cada ejecución un pronóstico fechado de una magnitud del proyecto, como el número de módulos de [PSY-010](psy-010-growth-curves-short-series.es.md), y representar el error frente a la antelación cuando se hayan resuelto suficientes pronósticos. Un crecimiento exponencial seguido de una meseta sería un primer indicio de un exponente positivo, todavía no una estimación; una curva plana indicaría que no es el horizonte lo que limita el plan.
