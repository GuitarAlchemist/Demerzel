---
module_id: psy-014-prediction-horizons
department: psychohistory
course: "Horizontes de predicción: a qué velocidad crecen los errores pequeños"
level: intermediate
prerequisites: ["mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-014
version: "0.1.0"
---

# Horizontes de predicción: a qué velocidad crecen los errores pequeños

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

Ejecutará un modelo dos veces desde puntos de partida casi iguales, medirá cómo cambia la diferencia entre las dos trayectorias, la resumirá en un exponente de Lyapunov y la convertirá en un *horizonte de predicción*: el número de pasos durante los cuales un pronóstico se mantiene dentro de una tolerancia enunciada. **Pregunta de proyecto:** ¿hasta dónde se puede confiar en un modelo determinista cuando su estado de partida solo se conoce de forma aproximada?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) dice que la psicohistoria puede «predict the broad strokes» pero no los sucesos individuales, y [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) que los cambios individuales son impredecibles mientras que el comportamiento agregado sigue leyes estadísticas. Ninguno dice hasta dónde se sostiene un pronóstico, ni qué compra un mejor conocimiento del presente: este módulo responde a las dos cosas para un modelo pequeño, con el exponente de la sección 2 de [MAT-024](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-024-dynamical-systems-stability-feedback.md). Las señales de alerta temprana corresponden a [PSY-012](psy-012-early-warning-false-alarms.es.md), y las reglas de alarma a PSY-023. Todos los resultados de más abajo son **sintéticos**: describen el modelo, no el proyecto.

## 1. Ejecutar el modelo dos veces

Un modelo *determinista* no contiene azar: el mismo punto de partida da siempre la misma trayectoria. El ejemplo pequeño de referencia es el *mapa logístico* (May 1976), que hace evolucionar un estado x entre 0 y 1 mediante

```text
x_next = r * x * (1 - x)
```

donde r es un ajuste fijo. Tras un transitorio, el estado se queda sobre un *atractor*: un punto fijo con r = 2.9, un ciclo de dos puntos con r = 3.2, una banda irregular con r = 3.7 y con r = 4. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-014/analyze.py) extrae 1,000 puntos de partida con semilla fija ([`scenarios.json`](../../../fixtures/psychohistory/psy-014/scenarios.json)), deja que cada uno se asiente durante 1,000 pasos y luego lo ejecuta dos veces: una tal cual y otra desplazado un *error inicial* de 1e-9. La *separación* es la diferencia absoluta entre las dos trayectorias en el mismo paso.

**Sintético.** Separación mediana de los 1,000 pares, según `gap_table` en [`results.json`](../../../fixtures/psychohistory/psy-014/results.json):

| Paso | r = 2.9 | r = 3.2 | r = 3.7 | r = 4 |
|---|---|---|---|---|
| 0 | 1e-9 | 1e-9 | 1e-9 | 1e-9 |
| 10 | 3.49e-10 | 1.05e-13 | 4.85e-8 | 1.04e-6 |
| 20 | 1.22e-10 | 0 | 1.72e-6 | 0.00107 |
| 30 | 4.24e-11 | 0 | 6.14e-5 | 0.537 |
| 60 | 1.8e-12 | 0 | 0.173 | 0.36 |

Un `0` significa una separación demasiado pequeña para los números de 64 bits del programa (sección 3), no una separación nula: recalculada con números de 1,024 bits, la mediana con r = 3.2 vale 1.1e-17 en el paso 20.

En las dos primeras columnas el error se encoge. Estos *regímenes estables* olvidan su punto de partida: los 1,000 puntos ya asentados se han derrumbado sobre el atractor, los dos puntos del ciclo con r = 3.2 y, con r = 2.9, el punto fijo, que el redondeo mantiene como dos números separados por 6.66e-16. Así que estos 1,000 pares repiten dos experimentos. En los *regímenes caóticos* de las dos últimas columnas la separación crece por un factor aproximadamente constante en cada paso: es la *dependencia sensible de las condiciones iniciales*. Luego se detiene: una separación no puede superar el tamaño del atractor.

### Ejercicio práctico 1

Con r = 2.9 un error pequeño se multiplica por 0.9 en cada paso. Compruébelo en la tabla a lo largo de diez pasos y calcule después cuántos pasos llevan un error de 1e-3 por debajo de 1e-6.

> **Respuesta:** `0.9^10 = 0.3487`, y la tabla da `3.49e-10 / 1e-9 = 0.349`. Un error cae por un factor de 1,000 en `ln(1e-6 / 1e-3) / ln(0.9) = −6.9078 / −0.105361 = 65.56` pasos, así que 66 pasos; el fixture cuenta 66 en los dos experimentos. Aquí un pronóstico mejora con el tiempo, siempre que el error de partida sea pequeño.

## 2. La velocidad: un exponente de Lyapunov

Mientras una separación es pequeña, un paso la multiplica por el tamaño de la pendiente del mapa en el estado actual, |r (1 − 2x)|. El *exponente de Lyapunov* λ es el promedio del logaritmo de ese factor a lo largo de una trayectoria larga:

```text
λ = promedio de ln|r * (1 - 2 * x)| a lo largo de la trayectoria
separación tras n pasos ≈ error inicial * e^(λ * n)      mientras la separación siga pequeña
```

Un λ negativo significa que los errores se encogen; uno positivo, que crecen en promedio por un factor e^λ en cada paso. **Sintético**, a partir de 1,000,000 de pasos por ajuste:

| r | λ estimado | λ conocido | e^λ |
|---|---|---|---|
| 2.9 | −0.105361 | ln 0.9 = −0.105361 | 0.9 |
| 3.2 | −0.916291 | ln 0.4 = −0.916291 | 0.4 |
| 3.7 | 0.3547 ± 0.0003 | sin forma cerrada | 1.426 |
| 4 | 0.693144 | ln 2 = 0.693147 | 2 |

Con r = 3.7 solo hay la estimación; su error estándar viene de 100 bloques de 10,000 pasos. MAT-024 imprime 0.350235 a partir de 10,000 pasos: el primer bloque de esta trayectoria, reproducido con seis decimales.

El exponente es un promedio: con r = 3.2 la pendiente tiene tamaño 1.9165 en un punto del ciclo y 0.0835 en el otro, y su producto es 0.16 = 0.4².

### Ejercicio práctico 2

Estime λ a partir de dos entradas de la tabla de separaciones: para r = 4 con los pasos 0 y 20, y para r = 3.2 con los pasos 0 y 10. ¿Por qué el paso 30 es inservible para r = 4?

> **Respuesta:** r = 4: `ln(0.00107 / 1e-9) / 20 = 13.8832 / 20 = 0.6942`, frente a ln 2 = 0.6931. r = 3.2: `ln(1.05e-13 / 1e-9) / 10 = −9.1616 / 10 = −0.9162`, frente a −0.9163. En el paso 30 la separación mediana es 0.537: el crecimiento se ha detenido en el tamaño del atractor.

## 3. El horizonte y el precio de un dígito

Llamemos *tolerancia* a la mayor separación que acepta quien usa un pronóstico, y *horizonte* al primer paso en que la separación la alcanza. Igualando la separación a la tolerancia en la ley de crecimiento se obtiene

```text
horizonte ≈ ln(tolerancia / error inicial) / λ
pasos ganados por cada dígito decimal extra de precisión = ln(10) / λ
```

**Sintético.** Horizonte medio de los 1,000 pares para una tolerancia de 0.1, junto a la fórmula:

| Error inicial | r = 3.7: media | fórmula | r = 4: media | fórmula |
|---|---|---|---|---|
| 1e-3 | 12.93 | 12.98 | 6.79 | 6.64 |
| 1e-6 | 32.56 | 32.46 | 16.78 | 16.61 |
| 1e-9 | 51.54 | 51.93 | 26.78 | 26.58 |
| 1e-12 | 71.05 | 71.41 | 36.69 | 36.54 |

De 1e-3 a 1e-12, nueve dígitos más, el horizonte medio gana 58.12 pasos con r = 3.7 y 29.9 con r = 4: 6.46 y 3.32 pasos por dígito, frente a 6.49 y 3.32 según la fórmula. **En un régimen caótico cada dígito de precisión compra el mismo número pequeño de pasos.** Todos los umbrales escritos en la hipótesis del ciclo de investigación antes de la primera ejecución se cumplieron: pendiente con un margen del 10% respecto a la de la fórmula, desplazamiento de 5 pasos como máximo y variando menos de 2 (medido: de −0.39 a 0.22 pasos).

Donde λ es negativo no hay horizonte: con r = 2.9 y r = 3.2, ninguna de las 20,000 combinaciones de par, error y tolerancia alcanzó una tolerancia (40 combinaciones distintas cada una: los puntos de partida asentados son 2 números). Un detector que nunca se dispara daría el mismo cero: como control, una trayectoria que arranca en el otro punto del ciclo de dos, a 0.286 de distancia, queda marcada en el paso 1 y se mantiene a 0.286. «Sin horizonte» solo vale para errores pequeños.

La aritmética fija su propio horizonte. Un *doble*, el formato numérico de 64 bits de Python, lleva 15.95 dígitos decimales: entre 0.5 y 1, los valores vecinos están separados por 2^-53 ≈ 1.11e-16. El redondeo actúa como un error inicial: frente a una trayectoria que arranca en el mismo punto con números de 1,024 bits, una trayectoria en dobles se aparta 0.1 tras 53.27 pasos de media con r = 4 y 99.55 con r = 3.7; más allá, ya no es la órbita del mapa desde su punto de partida. Los horizontes de arriba siguen perteneciendo al mapa: con esos números, 3 de 10,000 horizontes (diez errores iniciales) cambian con r = 3.7 y 1 de 10,000 con r = 4, y como máximo en 2 pasos.

### Ejercicio práctico 3

Con r = 3.7, tome λ = 0.355 y una tolerancia de 0.1. Calcule el horizonte para un error inicial de 1e-6 y después qué compra mejorar el error hasta 1e-9.

> **Respuesta:** `ln(0.1 / 1e-6) / 0.355 = 11.5129 / 0.355 = 32.43` pasos (media medida 32.56). Cada dígito vale `ln(10) / 0.355 = 6.49` pasos, así que tres dígitos compran 19.46 pasos y el horizonte pasa a 51.89. Una medición 1,000 veces más precisa alarga el horizonte en `19.46 / 32.43 = 0.60`, es decir, un 60%.

### Ejercicio práctico 4

Con r = 4, ¿qué error inicial mantendría un pronóstico dentro de 0.1 durante 100 pasos? ¿Puede proporcionarlo un doble?

> **Respuesta:** `0.1 × e^(−0.693147 × 100) = 0.1 × 2^−100 = 7.89e-32`, que necesita 31.1 dígitos decimales. Un doble tiene 15.95, así que no. Tomando una separación entre dobles como error inicial, la fórmula da `ln(0.1 / 1.11e-16) / 0.693147 = 49.68` pasos, cerca de los 53.27 medidos.

## 4. Más allá del horizonte y de qué puede servirse un plan

Pasado el horizonte el estado se pierde, pero no todo. **Sintético:** dos trayectorias con r = 4 que arrancan en 0.3 y en 0.3 + 1e-12 están a 0.1 de distancia en el paso 37, tanto en dobles como en números de 1,024 bits. En el paso 100 las dos trayectorias calculadas valen 0.673899 y 0.002785, números que ya dependen del redondeo: desde los mismos puntos de partida, las trayectorias de 1,024 bits dan 0.991939 y 0.735222. Y, sin embargo, a lo largo de 100,000 pasos la primera trayectoria calculada pasa 33,353 pasos por debajo de 0.25 y la segunda 33,525, frente a una proporción conocida de 1/3. La estadística del atractor sigue siendo predecible cuando el estado no lo es: la versión del tamaño de un modelo de la afirmación de PSY-002 sobre los agregados.

### Ejercicio práctico 5

Un pronóstico con r = 4 debe mantenerse dentro de 0.1 en cada uno de 60 pasos. Opción A: medir el punto de partida una sola vez, con 1e-12 en lugar de 1e-6. Opción B: quedarse con 1e-6 y volver a medir cada k pasos. De 1,000 pronósticos así, 972 se mantienen dentro de la tolerancia en los 60 pasos con k = 10, 960 con 11, 924 con 12 y 284 con 16. ¿Qué opción, y qué k más largo, mantiene al menos el 95% de los pronósticos de 60 pasos dentro de la tolerancia?

> **Respuesta:** A falla: el horizonte de la fórmula con 1e-12 es de 36.54 pasos y el más largo de los 1,000 horizontes medidos es 49. B funciona hasta k = 11, es decir, 6 mediciones: `960 / 1,000 = 96.0%`, frente al 92.4% con k = 12. Elegir k = 16, el horizonte 16.61 de la fórmula redondeado hacia abajo, solo mantiene el 28.4%: un horizonte es una distribución, aquí de 9 a 24 pasos en torno a una media de 16.78. El criterio es su extremo bajo, y el remedio es volver a medir, no medir mejor.

**Analogía, no medición.** Una hoja de ruta es un pronóstico largo desde un presente conocido de forma aproximada. Si el proceso que hay detrás amplifica las diferencias pequeñas, más detalle sobre el presente compra una prolongación fija y pequeña; volver a medir y pronosticar distribuciones son las cosas que ayudan. Si las amortigua, los pronósticos largos son baratos. Nadie ha medido un exponente de Lyapunov para este proyecto: esta lección no puede decir cuál de los dos casos se aplica.

**La objeción más fuerte** es que el mapa logístico es un solo número bajo una regla fija. Un proyecto tiene muchas variables, personas que reaccionan a los pronósticos y choques externos; con choques, los errores crecen incluso desde un punto de partida perfectamente conocido, y esta fórmula del horizonte no tiene por qué cumplirse. Una serie del proyecto puntuada en [PSY-005](psy-005-persistence-baseline.es.md) no lo zanja: «nada cambia» acertó en 1,528 de los 1,529 pares de filas consecutivas (desigualmente espaciadas), lo que muestra etiquetas que cambian rara vez, o un registro que nadie revisa, no cómo crecen los errores de pronóstico. **Este fixture no permite distinguir un proyecto caótico, uno ruidoso y uno estable.** Pronósticos fechados de una magnitud del proyecto, puntuados según el plazo de anticipación, podrían empezar a hacerlo: un error que crece exponencialmente y luego se estabiliza indica un exponente positivo; un error que se mantiene plano, un régimen estable; un error presente desde el primer paso que crece sin fase exponencial, uno ruidoso.

## Fuentes, límites y próxima comprobación

**Fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** PSY-001, PSY-002 y MAT-024. El fixture reproduce los cuatro exponentes que MAT-024 imprime para estos ajustes; el recuento de pares de filas de la sección 4 es el de PSY-005.

**Fixture.** Desde la raíz del repositorio, `python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py` y luego lo mismo con `--check`. Solo lee `scenarios.json` y ejecuta 41 autocomprobaciones; su [README](../../../fixtures/psychohistory/psy-014/README.md) explica por qué la salida es idéntica byte a byte entre plataformas y enumera los límites.

**Referencias de método.** May, R. M. (1976), «Simple mathematical models with very complicated dynamics», *Nature* 261, 459–467. Lorenz, E. N. (1963), «Deterministic nonperiodic flow», *Journal of the Atmospheric Sciences* 20, 130–141 (la dependencia sensible de las condiciones iniciales). Strogatz, S. H. (2015), *Nonlinear Dynamics and Chaos*, segunda edición, Westview Press (los exponentes de Lyapunov y el horizonte temporal de una predicción).

**No realizado.** No se analizó ningún dato del proyecto ni se estimó ningún exponente para ninguna magnitud del proyecto. Se estudió un solo mapa con una sola variable, sin ruido y con una sola semilla. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Archivar en cada ejecución un pronóstico fechado de una magnitud del proyecto, por ejemplo el recuento de módulos de [PSY-010](psy-010-growth-curves-short-series.es.md), y representar el error frente al plazo de anticipación en cuanto hayan vencido suficientes pronósticos. Un crecimiento exponencial seguido de una meseta sería una primera indicación de un exponente positivo, todavía no una estimación; una curva plana diría que no es el horizonte lo que limita el plan.
