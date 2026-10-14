---
module_id: psy-010-growth-curves-short-series
department: psychohistory
course: "¿Exponencial, logístico o escalonado? Ajustar el crecimiento a un historial corto"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-010
version: "0.1.0"
---

# ¿Exponencial, logístico o escalonado? Ajustar el crecimiento a un historial corto

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo convertirá un historial de commits en una serie diaria, le ajustará tres curvas de crecimiento por mínimos cuadrados, leerá en cada una la fecha en que se alcanza un objetivo y comprobará si los datos permiten distinguirlas. **Pregunta de proyecto:** los módulos de curso en inglés se añadieron en ráfagas. ¿Qué predicen los ajustes exponencial, logístico y lineal del recuento acumulado sobre la fecha en que se llegará a 525, y permite el historial distinguirlos?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) representa el crecimiento sano como un interés compuesto. Si la biblioteca creciera de forma compuesta, su recuento sería exponencial; aquí es solo una de las tres curvas candidatas. [PSY-022](../en/psy-022-competing-explanations.md) compara modelos con criterios de verosimilitud, [PSY-018](../en/psy-018-backtesting-without-leakage.md) pone a prueba pronósticos sobre datos reservados y [PSY-023](../en/psy-023-monitoring-a-plan.md) vigila un plan una vez que existe un calendario.

## 1. Convertir el historial en una serie

**Observado.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/extract.py) pregunta a git cuáles de los 1,599 commits alcanzables desde el commit `4b03838` modificaron la carpeta [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses): 73 commits, del 2026-03-21 al 2026-10-13. Escribe [`observed-input.json`](../../../fixtures/psychohistory/psy-010/observed-input.json) solo a partir de las fechas de los commits y de los nombres de archivo. Un *módulo* es una ruta `DEPARTMENT/en/NAME.md`. No se cuentan las traducciones (181 archivos en el commit fijado), los archivos README (4, y 2 más dentro de carpetas `en/`) ni los 10 nombres de archivo de una primera organización del repositorio, sin carpetas de idioma. En conjunto, los commits añaden 73 rutas de módulo y eliminan 5 (un cambio de nombre cuenta como una eliminación más una adición): **68** módulos en el commit fijado, en 18 de las 21 carpetas de departamento.

**Supuesto.** El plan de estudios prevé 21 departamentos con 25 cursos cada uno, 21 × 25 = **525**, una cifra tomada de un borrador de especificación y usada tal cual, aunque el repositorio registra 23 departamentos, dos de ellos sin carpeta de cursos. 68 equivale al 13.0% de 525.

Cada commit se fecha con su fecha de confirmación (*committer date*) en UTC; los commits que comparten el mismo segundo se ordenan según su ascendencia. La serie es el recuento al final de cada día UTC, siendo el día 0 el 2026-03-21: 207 días. **Calculado:** el recuento cambia en 12 de ellos.

```text
día        0   1   2   3  15  190  191  195  196  197  200  206
recuento  13  17  19  23  31   32   37   60   63   66   67   68
```

Llamaremos *activos* a esos 12 días, y *ráfaga* a una sucesión de días activos separados entre sí por 7 días como máximo (una convención, guardada en [`scenarios.json`](../../../fixtures/psychohistory/psy-010/scenarios.json); [PSY-008](psy-008-bursts-are-not-rates.es.md) llama *episodio* a un grupo así):

| Ráfaga | Días | Módulos añadidos | Proporción de los 68 |
|---|---|---|---|
| Del 21 al 24 de marzo | 4 | 23 | 33.8% |
| 5 de abril | 1 | 8 | 11.8% |
| Del 27 de septiembre al 13 de octubre, todavía abierta | 17 | 37 | 54.4% |

La tercera ráfaga sigue abierta: el propio commit fijado añadió un módulo, de modo que, con la regla de 7 días, sus 37 módulos y sus 17 días son cotas inferiores, y los módulos del lote de esta lección la prolongan si se fusionan a más tardar el 2026-10-20. Durante 174 días, del 6 de abril al 26 de septiembre, el recuento se mantuvo en 31. Una regla de 3 días da 5 ráfagas, y una de 12 días, 2: «ráfaga» es una elección. También lo es el reloj: otras cinco zonas horarias dan de 10 a 13 días activos, que siguen formando tres ráfagas.

### Ejercicio práctico 1

¿Qué proporción de los 68 módulos llegó en la última ráfaga, y en qué proporción de los 207 días? ¿En cuántos días no cambió el recuento?

> **Respuesta:** `37 / 68 = 54.4%` de los módulos, en `17 / 207 = 8.2%` de los días. `207 − 12 = 195` días sin cambios, el 94.2%. Más de la mitad del crecimiento se concentra en los 17 últimos días: cualquier curva ajustada aquí depende en gran medida de un único suceso reciente.

## 2. Ajustar tres leyes de crecimiento

Tres leyes candidatas para el recuento N el día t:

```text
recta        N = a + b t                      el mismo número de módulos cada día
exponencial  N = a exp(b t)                   adiciones proporcionales al recuento: crecimiento compuesto
logística    N = K / (1 + exp(-r (t - m)))    crecimiento compuesto que se frena cuando N se acerca a un techo K

ajuste de    b = (n ΣtN - Σt ΣN) / (n Σt² - (Σt)²)      sumas sobre los n días
la recta     a = (ΣN - b Σt) / n
```

El método de los *mínimos cuadrados* elige los parámetros que minimizan la SSE, la suma sobre los 207 días de (observado − ajustado)². La RMSE, raíz cuadrada de SSE / 207, es el error típico, expresado en módulos. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/analyze.py) resuelve la recta de forma exacta a partir de esas sumas y encuentra las dos curvas mediante una búsqueda determinista (una rejilla y después pasos de Newton). El techo de la logística, su capacidad de carga, se fija en K = 525, y m es el día en que la curva pasa por K / 2. Una curva logística solo se acerca a su techo, así que «llega a 525» significa, para todas las curvas, el primer día en que su valor es al menos 524.5.

**Calculado** ([`results.json`](../../../fixtures/psychohistory/psy-010/results.json), `fits.pinned_date`):

| Curva | Parámetros (t en días) | SSE | RMSE | Valor el día 206 | Llega a 525 | Años después del commit fijado |
|---|---|---|---|---|---|---|
| Recta | a = 24.5641, b = 0.0767431 | 11,462.4 | 7.441 | 40.37 | 2044-01-21 | 17.3 |
| Exponencial | a = 24.6004, b = 0.00257104 | 11,100.5 | 7.323 | 41.78 | 2029-06-24 | 2.7 |
| Logística | r = 0.00272281, m = 1,106.31 | 11,130.8 | 7.333 | 41.65 | 2036-03-29 | 9.5 |

Las tres fechas abarcan 14.6 años. Cada curva sitúa entre 40 y 42 módulos en un día en que el repositorio contenía 68.

### Ejercicio práctico 2

A partir de los parámetros, calcule el día en que la recta y la exponencial llegan a 524.5 y, después, los años transcurridos desde el commit fijado (día 206, 365.25 días por año).

> **Respuesta:** Recta: `(524.5 − 24.5641) / 0.0767431 = 6,514.4`, luego el día 6,515, que cae `6,515 − 206 = 6,309` días o 17.3 años después del commit fijado. Exponencial: `ln(524.5 / 24.6004) / 0.00257104 = 1,190.1`, luego el día 1,191: 985 días, 2.7 años.

### Ejercicio práctico 3

¿Cuánto tiempo después de su punto medio m llega la logística a 524.5? ¿Qué dice el resultado sobre la pregunta «cuándo llegaremos a 525»?

> **Respuesta:** N = 524.5 cuando `exp(−r (t − m)) = 0.5 / 524.5`, así que `t − m = ln(1,049) / r = 6.95559 / 0.00272281 = 2,554.6` días, 7.0 años. La curva pasa por 262.5 el día 1,107, 2.5 años después del commit fijado, y necesita 7.0 años más para la segunda mitad. Nunca llega a valer 525: con esta ley, la pregunta solo tiene respuesta mediante una convención como el margen de medio módulo.

## 3. ¿Puede el historial distinguirlas?

Cuatro comprobaciones **calculadas**.

*Las sumas de cuadrados de los residuos son casi iguales.* La SSE más grande es 1.033 veces la más pequeña.

*Las tres curvas fallan de la misma manera.* Un *residuo* es lo observado menos lo ajustado. A lo largo de los 207 días, los residuos de cada curva cambian de signo 3 veces, y la racha más larga de un mismo lado dura de 105 a 111 días. Los mínimos cuadrados rinden mejor cuando los errores son ruido independiente: en una recta **sintética** con un ruido así, ajustada por una recta, los residuos cambian de signo 107 veces. Estos residuos no son ruido: son la escalera.

*Dentro de la muestra, una escalera sin ninguna ley de crecimiento se ajusta mucho mejor.* Dos niveles planos, 30.41 antes del 2 de octubre y 65.92 a partir de ese día, dejan una SSE de 1,564.1: 7.1 veces menos que la mejor curva, con 3 parámetros frente a 2. Con 11 puntos de cambio, la SSE es 0. Una escalera no dice nada del próximo escalón. Cómo sopesar el ajuste frente al número de parámetros es el tema de PSY-022.

*No puede estimarse ningún techo.* Con K fijado en 12 valores, de 69 a 100,000, la SSE de la logística baja en cada paso, de 11,469.8 a 11,100.7, hacia los 11,100.5 de la exponencial. Un techo situado un módulo por encima del recuento actual y un techo de 100,000 dan SSE que difieren en un 3.3%: K no es *identificable* con estos datos. El método no tiene la culpa: en una logística sintética observada más allá de su punto de inflexión, el mismo perfil recupera el techo de 525 con el que se generó (SSE 8,751.7, frente a 29,596.0 con 550); observada antes de su punto de inflexión, el perfil es plano, con variaciones de menos del 0.4%. Este historial no ha llegado a ningún punto de inflexión, si es que lo hay.

### Ejercicio práctico 4

Un colega escribe: «La exponencial tiene la SSE más baja, así que la biblioteca crece de forma compuesta y llegaremos a 525 en 2029». Acepte o rechace la afirmación y enuncie su criterio.

> **Respuesta:** Se rechaza por falta de respaldo. Una clasificación solo cuenta cuando la distancia entre las candidatas es grande en comparación con lo que todas dejan sin explicar. Aquí `11,462.4 / 11,100.5 = 1.033`, mientras que una escalera de dos niveles lo hace `11,100.5 / 1,564.1 = 7.1` veces mejor y las tres curvas dejan los mismos 3 cambios de signo. Esta muestra no permite distinguir las tres leyes; el crecimiento compuesto sigue siendo una hipótesis candidata, no un hallazgo.

## 4. Mover la fecha de corte y después contar ráfagas

Un ajuste que hubiera captado la ley daría fechas que dejarían de moverse a medida que crece el historial. **Calculado:** los mismos ajustes sobre el historial al final de la segunda ráfaga, en la víspera de la tercera y en el commit fijado.

| Historial hasta | Días | Recuento | Recta | Exponencial | Logística |
|---|---|---|---|---|---|
| 5 de abril | 16 | 31 | 2028-08-16 | 2026-08-02 | 2027-04-16 |
| 26 de septiembre | 190 | 31 | 2088-12-21 | 2037-10-26 | 2062-12-02 |
| 13 de octubre | 207 | 68 | 2044-01-21 | 2029-06-24 | 2036-03-29 |

Entre las dos primeras filas, 174 días sin cambios retrasaron las fechas 60.3, 11.2 y 35.6 años. La última ráfaga las adelantó después 44.9, 8.3 y 26.7 años. Para el 13 de octubre, los ajustes de abril predecían 136.68, 3,267.78 y 467.68 módulos, y los de septiembre, 32.68, 32.66 y 32.66; el recuento fue de 68. Aquí, una curva ajustada a una escalera extrapola lo último que vio: un salto o un rellano.

Otras elecciones defendibles vuelven a mover las fechas: ajustar solo los 12 días activos da 2033-07-08, 2027-11-09 y 2030-12-15; una recta ajustada al logaritmo de los recuentos (la línea de tendencia exponencial de una hoja de cálculo) da 2030-04-27; fechar un commit por su fecha de autor (*author date*), 1.3 días anterior, desplaza 81 días la fecha de la recta.

**Sintético.** Proyectar la lectura escalonada exige suponer que el futuro repite el pasado: quedan 457 módulos, las ráfagas añadieron 23, 8 y al menos 37, y empezaron con 15 y 175 días de separación.

### Ejercicio práctico 5

Con ese supuesto, ¿cuántas ráfagas hacen falta y cuánto tiempo llevan (a) con el tamaño medio y el intervalo medio, (b) con el tamaño mayor, al menos 37, y el intervalo más corto, (c) con el tamaño menor y el intervalo más largo?

> **Respuesta:** (a) Tamaño medio `68 / 3 = 22.67`; `457 / 22.67 = 20.16`, luego 21 ráfagas; intervalo medio `(15 + 175) / 2 = 95` días; `21 × 95 = 1,995` días, 5.5 años. (b) `457 / 37 = 12.35`, luego 13 ráfagas; `13 × 15 = 195` días, 0.5 años. (c) `457 / 8 = 57.125`, luego 58 ráfagas; `58 × 175 = 10,150` días, 27.8 años. La ráfaga abierta convierte (a) y (b) en cotas superiores. Tres ráfagas dan un rango de 0.5 a 27.8 años: aritmética sobre un supuesto, no un pronóstico.

**La objeción más fuerte a esta lectura** es que la competición entre curvas no viene al caso. El 2 de octubre el recuento subió en 23 con 23 commits de un módulo cada uno, 14 de ellos en un lapso de dos minutos: el patrón de un lote de producción. Si los módulos llegan cuando alguien decide lanzar un lote, la serie registra decisiones, no una ley de crecimiento, y «no permite distinguir las curvas» es cierto pero no informa de nada. Dos cosas lo zanjarían: un calendario de producción por escrito, que convierte la fecha en un plan que vigilar (PSY-023), o varias ráfagas más con la misma regla de 7 días, las suficientes para ver si los módulos añadidos por unidad de tiempo crecen con el recuento (ráfagas mayores o más frecuentes: crecimiento compuesto), se mantienen estables (lineal) o disminuyen (un techo).

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** el historial de commits de `state/streeling/courses` y los registros de los departamentos en el commit fijado (solo commits y árboles). `extract.py` rechaza un clon superficial (*shallow clone*) o cualquier historial distinto del fijado. 525 es la cifra del plan.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py`, y después `analyze.py` en la misma carpeta; `analyze.py --check` compara una ejecución nueva con los resultados guardados. El [README](../../../fixtures/psychohistory/psy-010/README.md) documenta el método y sus comprobaciones.

**Referencias de método.** Bates, D. M., y Watts, D. G. (1988), *Nonlinear Regression Analysis and Its Applications*, Wiley (mínimos cuadrados para curvas; pasos de Gauss–Newton). Debecker, A., y Modis, T. (1994), «Determination of the uncertainties in S-curve logistic fits», *Technological Forecasting and Social Change* 46(2), 153–173 (cuán incierto es un techo ajustado antes de que la curva llegue a su punto de inflexión). Meade, N., e Islam, T. (1995), «Forecasting with growth curves: An empirical comparison», *International Journal of Forecasting* 11(2), 199–215.

**No realizado.** No se dio ningún intervalo para ninguna fecha, ni se calculó ninguna verosimilitud ni ningún criterio de información, AIC o BIC (PSY-022). No se leyeron el contenido, la calidad ni el estado de revisión de los módulos: aquí un módulo es un nombre de archivo. Todos los días pesan lo mismo; ninguna otra ponderación estaba justificada. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Volver a ejecutar `extract.py`, tras sustituir sus constantes fijadas por un commit posterior, cuando se hayan cerrado al menos cinco ráfagas nuevas, con la regla de 7 días y los ajustes en las tres fechas de corte definidos tal como están ahora. Si las nuevas ráfagas se mantienen dentro de los rangos observados (de 8 a al menos 37 módulos, con inicios separados de 15 a 175 días), la lectura escalonada no queda contradicha; si los módulos añadidos por unidad de tiempo aumentan con el recuento, el crecimiento compuesto obtiene su primer apoyo.
