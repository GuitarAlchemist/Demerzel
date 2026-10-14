---
module_id: psy-010-growth-curves-short-series
department: psychohistory
course: "¿Exponencial, logística o escalera? Ajustar un crecimiento a una historia corta"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-010
version: "0.1.0"
---

# ¿Exponencial, logística o escalera? Ajustar un crecimiento a una historia corta

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

Convertirá un historial de commits en una serie diaria, le ajustará tres curvas de crecimiento por mínimos cuadrados, leerá en cada una la fecha de un objetivo y pondrá a prueba si los datos permiten distinguirlas. **Pregunta de proyecto:** los módulos de curso en inglés se añadieron en ráfagas. ¿Qué predicen para llegar a 525 los ajustes exponencial, logístico y lineal del recuento acumulado, y permite el historial distinguirlos?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) retrata el crecimiento sano como un interés compuesto. Si la biblioteca capitalizara, su recuento sería exponencial; aquí eso es un candidato entre tres. PSY-022 compara modelos con criterios de verosimilitud, PSY-018 pone a prueba pronósticos sobre datos reservados y PSY-023 vigila un plan en cuanto existe un calendario.

## 1. Convertir el historial en una serie

**Observado.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/extract.py) pregunta a git cuáles de los 1,599 commits alcanzables desde el commit `4b03838` modificaron la carpeta [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses): 73 commits, del 2026-03-21 al 2026-10-13. Escribe [`observed-input.json`](../../../fixtures/psychohistory/psy-010/observed-input.json) solo a partir de las fechas de commit y de los nombres de archivo. Un *módulo* es una ruta `DEPARTMENT/en/NAME.md`. No se cuentan las traducciones (181 archivos en la fijación), los archivos README (4, y 2 más dentro de carpetas `en/`) ni los 10 nombres de archivo de una organización antigua sin carpetas de idioma. En conjunto, los commits añaden 73 rutas de módulo y quitan 5 (un cambio de nombre cuenta como una baja y un alta): **68** módulos en la fijación, en 18 de las 21 carpetas de departamento.

**Supuesto.** El plan de estudios prevé 21 departamentos con 25 cursos cada uno, 21 × 25 = **525**, la cifra de una especificación en borrador, tomada tal cual aunque el repositorio registre 23 departamentos, dos de ellos sin carpeta de cursos. 68 es el 13.0% de 525.

Cada commit se fecha por su fecha de committer en UTC; los commits que comparten un segundo conservan su orden de ascendencia. La serie es el recuento al final de cada día UTC, siendo el día 0 el 2026-03-21: 207 días. **Calculado:** el recuento cambia en 12 de ellos.

```text
día      0   1   2   3  15  190  191  195  196  197  200  206
número 13  17  19  23  31   32   37   60   63   66   67   68
```

Llamemos *activos* a esos 12 días, y llamemos *ráfaga* a una serie de días activos separados por 7 días como máximo (una convención, guardada en [`scenarios.json`](../../../fixtures/psychohistory/psy-010/scenarios.json); [PSY-008](psy-008-bursts-are-not-rates.es.md) llama *episodio* a un grupo así):

| Ráfaga | Días | Módulos añadidos | Proporción de los 68 |
|---|---|---|---|
| Del 21 al 24 de marzo | 4 | 23 | 33.8% |
| 5 de abril | 1 | 8 | 11.8% |
| Del 27 de septiembre al 13 de octubre, aún abierta | 17 | 37 | 54.4% |

La tercera ráfaga sigue abierta: la fijación misma añadió un módulo, de modo que, bajo la regla de los 7 días, sus 37 módulos y sus 17 días son cotas inferiores, y los módulos del lote de esta lección la prolongan si se fusionan antes del 2026-10-20. Durante 174 días, del 6 de abril al 26 de septiembre, el recuento se mantuvo en 31. Una regla de 3 días da 5 ráfagas y una de 12 días da 2: «ráfaga» es una elección. También lo es el reloj: cinco husos horarios distintos dan de 10 a 13 días activos, siempre en tres ráfagas.

### Ejercicio práctico 1

¿Qué proporción de los 68 módulos llegó en la última ráfaga, y en qué proporción de los 207 días? ¿En cuántos días no cambió el recuento?

> **Respuesta:** `37 / 68 = 54.4%` de los módulos en `17 / 207 = 8.2%` de los días. `207 − 12 = 195` días sin cambio, el 94.2%. Más de la mitad del crecimiento está en los últimos 17 días: cualquier curva que se ajuste aquí depende en gran medida de un único suceso reciente.

## 2. Ajustar tres leyes de crecimiento

Tres leyes candidatas para el recuento N en el día t:

```text
recta        N = a + b t                      el mismo número de módulos cada día
exponencial  N = a exp(b t)                   altas proporcionales al recuento: capitalización
logística    N = K / (1 + exp(-r (t - m)))    capitalización que frena cuando N se acerca a un techo K

ajuste recta b = (n ΣtN - Σt ΣN) / (n Σt² - (Σt)²)      sumas sobre los n días
             a = (ΣN - b Σt) / n
```

Los *mínimos cuadrados* eligen los parámetros que minimizan la SSE, la suma sobre los 207 días de (observado − ajustado)². La RMSE, la raíz cuadrada de SSE / 207, es el error típico, en módulos. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/analyze.py) resuelve la recta exactamente a partir de esas sumas y halla las dos curvas con una búsqueda determinista (una rejilla y luego pasos de Newton). El techo logístico se fija en K = 525, y m es el día en que la curva pasa K / 2. Una curva logística solo se acerca a su techo, así que «llega a 525» significa, para cada curva, el primer día en que su valor es de al menos 524.5.

**Calculado** ([`results.json`](../../../fixtures/psychohistory/psy-010/results.json), `fits.pinned_date`):

| Curva | Parámetros (t en días) | SSE | RMSE | Valor el día 206 | Llega a 525 | Años tras la fijación |
|---|---|---|---|---|---|---|
| Recta | a = 24.5641, b = 0.0767431 | 11,462.4 | 7.441 | 40.37 | 2044-01-21 | 17.3 |
| Exponencial | a = 24.6004, b = 0.00257104 | 11,100.5 | 7.323 | 41.78 | 2029-06-24 | 2.7 |
| Logística | r = 0.00272281, m = 1,106.31 | 11,130.8 | 7.333 | 41.65 | 2036-03-29 | 9.5 |

Las tres fechas abarcan 14.6 años. Cada curva pone entre 40 y 42 módulos en un día en que el repositorio tenía 68.

### Ejercicio práctico 2

A partir de los parámetros, calcule el día en que la recta y la exponencial llegan a 524.5, y luego los años tras la fijación (día 206, 365.25 días por año).

> **Respuesta:** Recta: `(524.5 − 24.5641) / 0.0767431 = 6,514.4`, es decir, el día 6,515, que son `6,515 − 206 = 6,309` días, o 17.3 años tras la fijación. Exponencial: `ln(524.5 / 24.6004) / 0.00257104 = 1,190.1`, es decir, el día 1,191: 985 días, 2.7 años.

### Ejercicio práctico 3

¿Cuánto tarda la logística en llegar a 524.5 después de su punto medio m? ¿Qué dice el resultado sobre la pregunta «cuándo llegamos a 525»?

> **Respuesta:** N = 524.5 cuando `exp(−r (t − m)) = 0.5 / 524.5`, así que `t − m = ln(1,049) / r = 6.95559 / 0.00272281 = 2,554.6` días, 7.0 años. La curva pasa 262.5 el día 1,107, 2.5 años tras la fijación, y necesita 7.0 años más para la segunda mitad. Nunca es igual a 525: bajo esta ley la pregunta solo tiene respuesta con una convención como el margen de medio módulo.

## 3. ¿Permite el historial distinguirlas?

Cuatro comprobaciones **calculadas**.

*Las sumas de residuos son casi iguales.* La mayor SSE es 1.033 veces la menor.

*Las tres curvas se equivocan de la misma manera.* Un *residuo* es lo observado menos lo ajustado. A lo largo de los 207 días, los residuos de cada curva cambian de signo 3 veces, y la serie más larga de un mismo lado dura de 105 a 111 días. Los mínimos cuadrados dan lo mejor de sí cuando los errores son ruido independiente: una recta **sintética** más un ruido así, ajustada con una recta, cambia de signo 107 veces. Estos residuos no son ruido: son la escalera.

*Dentro de la muestra, una escalera sin ninguna ley de crecimiento ajusta mucho mejor.* Dos niveles planos, 30.41 antes del 2 de octubre y 65.92 a partir de ese día, dejan una SSE de 1,564.1: 7.1 veces menos que la mejor curva, con 3 parámetros frente a 2. Con 11 puntos de cambio la SSE es 0. Una escalera no dice nada del siguiente escalón. Cómo pesar el ajuste frente al número de parámetros es el asunto de PSY-022.

*No se puede estimar ningún techo.* Con K fijado en 12 valores de 69 a 100,000, la SSE de la logística baja en cada paso, de 11,469.8 a 11,100.7, hacia los 11,100.5 de la exponencial. Un techo situado un módulo por encima del recuento actual y un techo de 100,000 difieren en un 3.3%: K no es *identificable* a partir de estos datos. El método no es el culpable: en una logística sintética vista pasado su codo, el mismo procedimiento recupera el techo plantado de 525 (SSE 8,751.7, frente a 29,596.0 con 550); vista antes de su codo, es plana con un margen del 0.4%. Este historial no ha alcanzado ningún codo, si es que hay uno.

### Ejercicio práctico 4

Un colega escribe: «La exponencial tiene la SSE más baja, así que la biblioteca capitaliza y llegamos a 525 en 2029.» Acepte o rechace, y enuncie su criterio.

> **Respuesta:** Rechazar por falta de respaldo. Una clasificación cuenta solo cuando la diferencia entre los candidatos es grande al lado de lo que todos ellos se equivocan. Aquí `11,462.4 / 11,100.5 = 1.033`, mientras que una escalera de dos niveles lo hace `11,100.5 / 1,564.1 = 7.1` veces mejor y las tres curvas dejan los mismos 3 cambios de signo. Esta muestra no permite distinguir las tres leyes; la capitalización sigue siendo un candidato, no un hallazgo.

## 4. Mover la fecha de corte y luego contar ráfagas

Un ajuste que hubiera captado la ley daría fechas que dejan de moverse a medida que el historial crece. **Calculado:** los mismos ajustes sobre el historial al final de la segunda ráfaga, en la víspera de la tercera y en la fijación.

| Historial hasta | Días | Recuento | Recta | Exponencial | Logística |
|---|---|---|---|---|---|
| 5 de abril | 16 | 31 | 2028-08-16 | 2026-08-02 | 2027-04-16 |
| 26 de septiembre | 190 | 31 | 2088-12-21 | 2037-10-26 | 2062-12-02 |
| 13 de octubre | 207 | 68 | 2044-01-21 | 2029-06-24 | 2036-03-29 |

Entre las dos primeras filas, 174 días tranquilos retrasaron las fechas en 60.3, 11.2 y 35.6 años. La última ráfaga las adelantó luego en 44.9, 8.3 y 26.7 años. Para el 13 de octubre, los ajustes de abril predecían 136.68, 3,267.78 y 467.68 módulos, y los de septiembre 32.68, 32.66 y 32.66; el recuento era 68. Aquí una curva ajustada a una escalera extrapola lo último que vio, una contrahuella o una huella.

Otras elecciones defendibles mueven otra vez las fechas: ajustar solo los 12 días activos da 2033-07-08, 2027-11-09 y 2030-12-15; una recta ajustada al logaritmo de los recuentos (la línea de tendencia exponencial de una hoja de cálculo) da 2030-04-27; fechar un commit por su fecha de autor, 1.3 días antes, mueve la fecha de la recta 81 días.

**Sintético.** Proyectar la lectura en escalones exige suponer que el futuro repite el pasado: quedan 457 módulos, las ráfagas añadieron 23, 8 y al menos 37, y empezaron con 15 y 175 días de separación.

### Ejercicio práctico 5

Bajo ese supuesto, ¿cuántas ráfagas hacen falta y cuánto tardan (a) con el tamaño medio y el intervalo medio, (b) con el tamaño mayor, al menos 37, y el intervalo más corto, (c) con el tamaño menor y el intervalo más largo?

> **Respuesta:** (a) Tamaño medio `68 / 3 = 22.67`; `457 / 22.67 = 20.16`, así que 21 ráfagas; intervalo medio `(15 + 175) / 2 = 95` días; `21 × 95 = 1,995` días, 5.5 años. (b) `457 / 37 = 12.35`, así que 13 ráfagas; `13 × 15 = 195` días, 0.5 años. (c) `457 / 8 = 57.125`, así que 58 ráfagas; `58 × 175 = 10,150` días, 27.8 años. La ráfaga abierta hace de (a) y (b) cotas superiores. Tres ráfagas dan un rango de 0.5 a 27.8 años: aritmética sobre un supuesto, no un pronóstico.

**La objeción más fuerte a esta lectura** es que la competición entre curvas no viene al caso. El 2 de octubre el recuento subió en 23 mediante 23 commits de un módulo cada uno, 14 de ellos en menos de dos minutos: el patrón de un lote de producción. Si los módulos llegan cuando alguien decide lanzar un lote, la serie registra decisiones, no una ley de crecimiento, y «no se pueden distinguir las curvas» es cierto y poco informativo. Dos cosas lo zanjarían: un calendario de producción escrito, que convierte la fecha en un plan que vigilar (PSY-023); o varias ráfagas más bajo la misma regla de los 7 días, suficientes para ver si los módulos añadidos por unidad de tiempo crecen con el recuento (ráfagas mayores o más frecuentes: capitalización), se mantienen (lineal) o bajan (un techo).

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** el historial de commits de `state/streeling/courses` y los registros de departamento en la fijación (solo commits y árboles). `extract.py` rechaza un clon superficial y cualquier historial que no sea el fijado. 525 es la cifra del plan.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py` y luego `analyze.py` en la misma carpeta; `analyze.py --check` compara una ejecución nueva con los resultados guardados. El [README](../../../fixtures/psychohistory/psy-010/README.md) documenta el método y sus comprobaciones.

**Referencias de método.** Bates, D. M., y Watts, D. G. (1988), *Nonlinear Regression Analysis and Its Applications*, Wiley (los mínimos cuadrados para curvas; los pasos de Gauss–Newton). Debecker, A., y Modis, T. (1994), «Determination of the uncertainties in S-curve logistic fits», *Technological Forecasting and Social Change* 46(2), 153–173 (cuán incierto es un techo ajustado antes de que la curva gire). Meade, N., y Islam, T. (1995), «Forecasting with growth curves: An empirical comparison», *International Journal of Forecasting* 11(2), 199–215.

**No realizado.** No se dio ningún intervalo para ninguna fecha, ni se calculó ninguna verosimilitud, AIC o BIC (PSY-022). No se leyó el contenido, la calidad ni el estado de revisión de los módulos: aquí un módulo es un nombre de archivo. Todos los días pesan igual; no se justificó ninguna otra ponderación. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Volver a ejecutar `extract.py` tras sustituir sus constantes fijadas por una fijación posterior, una vez cerradas al menos cinco ráfagas nuevas, con la regla de los 7 días y los tres ajustes por fecha de corte tal como están ahora. Si las ráfagas nuevas se mantienen dentro de los rangos observados (de 8 a al menos 37 módulos, inicios separados de 15 a 175 días), la lectura en escalones no queda contradicha; si los módulos añadidos por unidad de tiempo suben con el recuento, la capitalización gana su primer respaldo.
