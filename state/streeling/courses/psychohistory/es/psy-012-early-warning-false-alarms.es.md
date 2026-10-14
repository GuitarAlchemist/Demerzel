---
module_id: psy-012-early-warning-false-alarms
department: psychohistory
course: "Las señales de alerta temprana y sus falsas alarmas"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "mat-008-probability-conditional-reasoning", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-012
version: "0.1.0"
---

# Las señales de alerta temprana y sus falsas alarmas

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo calculará dos indicadores móviles, la varianza y la autocorrelación de orden 1, resumirá cada tendencia con un único estadístico de rangos y medirá una regla de alarma por sus dos lados: con qué frecuencia se dispara cuando un sistema se acerca a un punto de vuelco (*tipping point*), y con qué frecuencia cuando no se acerca a ninguno. **Pregunta de proyecto:** PSY-002 propone señales de un cambio de régimen que se avecina; ¿con qué frecuencia aparecen una varianza creciente y una autocorrelación creciente en un sistema que no se acerca a ninguna transición?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md), que se apoya en [PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md), enumera seis señales y pide que converjan tres o más. Este módulo toma los dos indicadores de alerta temprana mejor estudiados en la literatura y mide, para esos dos, lo que PSY-002 no da para sus seis: una tasa de falsas alarmas. Las secciones 1 a 3 son **sintéticas**: entradas supuestas en [scenarios.json](../../../fixtures/psychohistory/psy-012/scenarios.json), cálculo con [analyze.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-012/analyze.py), resultados guardados en [results.json](../../../fixtures/psychohistory/psy-012/results.json). Solo la sección 4 usa datos **observados** del proyecto. Los cambios de instrumento corresponden a PSY-011; el caos, a PSY-014.

## 1. Por qué un sistema se ralentiza antes del vuelco

Una *bifurcación de pliegue* es el punto de vuelco más simple: al variar un *parámetro de control* q, un estado de reposo estable y un umbral inestable se acercan, se encuentran y desaparecen, y el sistema salta a otra parte. El *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección) usa la forma de los manuales, dx/dt = r + x², escrita con r = −q² y con ruido añadido:

```text
x[t+1] = x[t] + h * (x[t]^2 - q[t]^2) + e[t]      h = 0.005, e ~ Normal(0, 1)
estado de reposo x = -q     umbral inestable x = +q     pliegue en q = 0
```

Cerca del estado de reposo, una pequeña perturbación d se reduce en un factor fijo en cada paso:

```text
d[t+1] ≈ phi * d[t]       phi = 1 - 2 * h * q
varianza = 1 / (1 - phi^2)       autocorrelación de orden 1 = phi
```

La segunda línea es el resultado clásico para un *proceso AR(1)*, en el que cada valor es phi veces el anterior más un ruido nuevo; la *autocorrelación de orden 1* es la correlación entre la serie y ella misma un paso más tarde. Cuando q baja hacia 0, phi sube hacia 1: la recuperación se hace más lenta, de modo que las fluctuaciones duran más (sube la autocorrelación) y se acumulan (sube la varianza). Esta *ralentización crítica* es el mecanismo que hay detrás de las señales de alerta temprana que revisan Scheffer et al. (2009).

En el fixture, q baja en línea recta de 50 a 10 y nunca llega al pliegue: al final, el umbral inestable sigue a 8.72 desviaciones estándar de las fluctuaciones, y ninguna simulación de aproximación lo cruzó.

El estimador (sección 2) se prueba primero con respuestas conocidas. Con 200,000 puntos de un AR(1) estacionario con phi = 0.9 devuelve una varianza de 5.2742 (teoría: 5.2632) y una autocorrelación de 0.9002; el simulador del pliegue, mantenido en q = 25, devuelve 0.7513 frente a un 0.75 previsto. Las ventanas cortas dan lecturas bajas: en 1,000 simulaciones **sintéticas** con phi = 0.9, la autocorrelación estimada media es 0.555 en una ventana de 25 puntos, 0.7279 con 50, 0.8641 con 200 y 0.8913 con 800, y la varianza media con 25 puntos es 1.7243 frente a un valor verdadero de 5.2632. El sesgo es máximo en un sistema lento, justo donde se supone que debe aparecer la señal.

### Ejercicio práctico 1

Calcule phi, la varianza y la desviación estándar de las fluctuaciones al inicio (q = 50) y al final (q = 10) de la aproximación. ¿En qué factor crece la varianza? ¿Cuántos pasos hacen falta para perder la mitad de una perturbación en cada extremo (resuelva phi^k = 0.5)?

> **Respuesta:** Inicio: phi = 1 − 2 × 0.005 × 50 = 0.5, varianza 1 / (1 − 0.25) = 1.3333, desviación estándar 1.1547. Final: phi = 0.9, varianza 1 / (1 − 0.81) = 5.2632, desviación estándar 2.2942. La varianza crece en un factor de 3.9474. Con k = ln 0.5 / ln phi, la mitad de una perturbación se pierde en 1 paso al inicio y en 6.58 pasos al final.

## 2. Dos indicadores móviles y un número de tendencia

Un analista dispone de una sola serie y no puede ver q. La receta habitual (Dakos et al. 2012) desliza una *ventana* de W puntos consecutivos a lo largo de la serie y calcula los dos indicadores en cada posición. El fixture resta primero, dentro de cada ventana, la recta que mejor se ajusta: el propio nivel de reposo deriva, aquí en 34.64 desviaciones estándar iniciales, y un nivel que deriva se contaría como varianza.

```text
e[u] = y[u] - (a + b * u)        u = 0 .. W-1
varianza        = suma(e[u]^2) / (W - 2)
autocorrelación = suma(e[u] * e[u+1]) / suma(e[u]^2)
```

Una serie de n puntos da m = n − W + 1 valores móviles de cada indicador. La *tau de Kendall*, una correlación de rangos con el tiempo, dice en un solo número si suben: entre los P = m(m − 1)/2 pares de posiciones, C son concordantes (el valor posterior es mayor), D discordantes (es menor) y t empatados (iguales). El programa calcula la forma corregida por empates, tau-b.

```text
tau = (C - D) / sqrt(P * (P - t))       +1 siempre creciente, -1 siempre decreciente
    = (C - D) / P                       cuando no hay dos valores iguales (t = 0)
M   = min(tau de la varianza, tau de la autocorrelación)       alarma cuando M >= T
```

M exige que suban los dos indicadores, como lo hace la convergencia de PSY-002. Se comparan tres umbrales T:

- **prueba de manual**: cada tau debe ser «significativa al 5%» según la fórmula unilateral estándar, que trata los m valores como independientes: T = 1.645 × sqrt(2(2m + 5) / (9m(m − 1)));
- **umbral fijo**: T = 0.5;
- **umbral calibrado**: T es el valor que alcanza el 5% de 1,000 simulaciones estacionarias hechas aparte (AR(1), phi = 0.7, mismos n y W), la idea de las series subrogadas (*surrogate series*) de Dakos et al. (2012).

### Ejercicio práctico 2

Seis valores móviles consecutivos son 0.8, 0.5, 1.1, 1.4, 1.2, 1.9 (inventados). Cuente los pares concordantes y discordantes y calcule tau. ¿Alcanza este indicador por sí solo T = 0.5?

> **Respuesta:** 6 × 5 / 2 = 15 pares. Dos son discordantes, (0.8, 0.5) y (1.4, 1.2), así que C = 13, D = 2 y tau = (13 − 2) / 15 = 0.7333, por encima de 0.5.

## 3. Detección y falsas alarmas, medidas

Para cada longitud de registro n y cada ventana (un cuarto y la mitad de n), el fixture ejecutó 1,000 simulaciones de aproximación y 1,000 simulaciones de cada control estacionario: AR(1) con phi = 0.5, 0.7 y 0.9. La *tasa de detección* es la proporción de simulaciones de aproximación en las que se dispara la alarma; la *tasa de falsas alarmas* es esa misma proporción entre las simulaciones de control. Cada tasa, para un umbral dado, tiene un error estándar de 1.58 puntos porcentuales como máximo; los umbrales calibrados, estimados a partir de 1,000 simulaciones y mostrados con dos decimales, añaden su propio error. Todos los valores son porcentajes **sintéticos**; las falsas alarmas se dan para phi = 0.5/0.7/0.9.

| n/W | Prueba de manual: falsas alarmas | Umbral fijo: detección | Umbral fijo: falsas alarmas | T calibrado | Umbral calibrado: detección | Umbral calibrado: falsas alarmas |
|---|---|---|---|---|---|---|
| 100/25 | 21.6/21.4/26.7 | 6.0 | 0.9/2.0/2.2 | 0.40 | 12.4 | 4.4/4.8/5.0 |
| 100/50 | 26.5/29.2/32.8 | 29.7 | 8.7/11.3/10.7 | 0.63 | 18.9 | 3.4/5.2/4.7 |
| 400/100 | 28.6/30.7/36.9 | 49.8 | 2.6/4.5/4.1 | 0.46 | 55.8 | 3.7/5.6/5.1 |
| 400/200 | 30.8/32.9/41.5 | 78.2 | 9.6/11.3/15.1 | 0.64 | 65.3 | 4.6/4.5/6.1 |
| 1,600/400 | 31.2/35.8/40.7 | 97.6 | 3.1/3.9/5.5 | 0.50 | 97.6 | 3.1/3.9/5.5 |
| 1,600/800 | 33.2/38.2/43.7 | 99.6 | 11.0/14.0/17.2 | 0.66 | 99.0 | 4.4/6.4/8.0 |

Cuatro lecturas:

1. **La pregunta de proyecto.** En los controles estacionarios, las dos taus son positivas en 334 a 461 de cada 1,000 simulaciones, y la prueba de manual, que nominalmente no pasa del 5%, se dispara en un 21.4% a 43.7%. Las ventanas vecinas comparten todos los puntos menos uno, así que m valores móviles distan mucho de ser m observaciones independientes.
2. **El umbral depende de la ventana.** T = 0.5 da de un 0.9% a un 5.5% de falsas alarmas con ventanas de un cuarto, y de un 8.7% a un 17.2% con ventanas de la mitad.
3. **Cerca del 5% de falsas alarmas, la detección depende de la longitud del registro.** La regla calibrada detecta esta aproximación en un 12.4% a 18.9% de las simulaciones con 100 puntos, en un 55.8% a 65.3% con 400 y en un 97.6% a 99.0% con 1,600 (un registro más largo es aquí el mismo cambio de q repartido en más pasos: una aproximación más lenta).
4. **El umbral calibrado es una estimación.** En simulaciones nuevas con phi = 0.7 se dispara en un 3.9% a 6.4%, y en el conjunto de los tres controles, en un 3.1% a 8.0%; 1,000 simulaciones no separan su error de muestreo de una dependencia respecto a phi.

Dos comprobaciones. Un gemelo lineal (un AR(1) cuyo coeficiente sigue la misma trayectoria de 0.5 a 0.9, sin nivel móvil y sin pliegue) se dispara con una frecuencia a menos de 3.7 puntos porcentuales de la del pliegue en todas las filas y con todas las reglas, así que las detecciones provienen de la ralentización. Sin la resta de la recta, la detección de la regla fija con n = 400, W = 200 cae del 78.2% al 3.3%.

### Ejercicio práctico 3

Con n = 100, W = 50, la regla fija se disparó en 297 de 1,000 simulaciones de aproximación y en 113 de 1,000 simulaciones estacionarias (phi = 0.7). Suponga que 1 de cada 10 sistemas vigilados se acerca realmente a un pliegue. ¿Qué proporción de las alarmas es verdadera?

> **Respuesta:** P(alarma) = 0.1 × 0.297 + 0.9 × 0.113 = 0.1314; la proporción verdadera es 0.0297 / 0.1314 = 0.226, unas 23 alarmas de cada 100.

### Ejercicio práctico 4

Un colega aplica la prueba de manual a un registro de 400 puntos con W = 200, encuentra los dos indicadores «significativos al 5%» y concluye que el azar queda excluido. Clasifique la afirmación, e indique el umbral que usted exigiría y su costo.

> **Respuesta:** No respaldada. En series estacionarias con phi = 0.7 esta prueba se dispara en el 32.9% de las simulaciones, no en el 5%: supone valores independientes, mientras que las ventanas móviles se solapan. Exija un umbral calibrado sobre un modelo estacionario ajustado a ese registro. En la configuración del propio fixture es M ≥ 0.64, que se disparó en el 4.5% de las simulaciones de control independientes y detectó el 65.3% de las aproximaciones: se omite más o menos una aproximación real de cada tres.

## 4. Lo que la tendencia de calidad registrada puede mostrar y lo que no

**Observado.** La [tendencia de calidad](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) fijada del repositorio contiene 1,548 filas: 18 artefactos de gobernanza registrados en 88 ejecuciones repartidas en 83 días. [extract.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-012/extract.py) comprueba cada archivo fuente contra su blob de Git y escribe [observed-input.json](../../../fixtures/psychohistory/psy-012/observed-input.json). Cada artefacto tiene de 81 a 87 ejecuciones que llevan los tres números; las filas de la primera ejecución, en mayo, no llevan ninguno. **Calculado** a partir de ese extracto:

- `compliance_rate` y `violation_count`: las 18 series mantienen un único valor; 0 cambios en 1,519 pares de filas consecutivas de un mismo artefacto ([PSY-005](psy-005-persistence-baseline.es.md) cuenta 1,518: uno de esos pares empieza en una fila sin etiqueta).
- `citation_count`: 2 series son constantes; las otras 16 cambian, 20 veces en 1,519 pares, y los 20 cambios caen en dos ejecuciones (16 series el 2026-09-13, 4 el 2026-10-03).

Este registro puede mostrar la persistencia, que es el tema de [PSY-005](psy-005-persistence-baseline.es.md), y dos escalones fechados; si esos escalones se deben al instrumento o al sistema es la pregunta de PSY-011.

No puede mostrar ninguna de las dos señales de alerta temprana. En una ventana cuyos valores son todos iguales, la varianza es 0 y la autocorrelación es 0 / 0: indefinida, no baja. Es el caso de todas las ventanas de dos de los campos y de 689 de las 1,105 ventanas de 25 ejecuciones de los recuentos de citas; en las demás, la única variación es un escalón. La ralentización crítica se refiere a la recuperación tras muchas sacudidas pequeñas, y un contador que no registra ninguna sacudida pequeña no informa de ninguna velocidad de recuperación. Por eso el fixture no calcula ningún indicador sobre los datos del proyecto, y la ausencia de tendencia no es un indicio ni de que el sistema de gobernanza esté lejos de un cambio ni de que esté cerca de uno. Incluso una serie fluctuante de esta longitud (de 81 a 87 puntos) sería corta para lo que exige la simulación, y las tasas simuladas descansan sobre una aproximación y una escala de tiempo supuestas, sin equivalente en el proyecto.

### Ejercicio práctico 5

En observed-input.json, los recuentos de citas de `policies / alignment-policy.yaml` valen 3 durante 55 ejecuciones, después 42 durante 21 ejecuciones y después 44 durante 11 ejecuciones. ¿Cuántas ventanas de 25 ejecuciones tiene esta serie, y cuántas son constantes? ¿Cuánto valen los dos indicadores en una ventana constante? ¿Debería aplicar la prueba de tendencia? Enuncie su criterio.

> **Respuesta:** 87 − 25 + 1 = 63 ventanas. Una ventana solo es constante dentro de un único tramo; los tramos de 21 y de 11 ejecuciones son más cortos que 25, así que solo sirven las 55 primeras ejecuciones: 55 − 25 + 1 = 31 ventanas. Las otras 32 abarcan un escalón. En una ventana constante, la varianza es 0 y la autocorrelación es 0 / 0, indefinida. No aplique la prueba: los indicadores necesitan fluctuación dentro de cada ventana, y aquí toda la variación son dos escalones.

## Fuentes, límites y próxima comprobación

**Fuentes.** Observado: la carpeta fijada de la tendencia de calidad; el [README](../../../fixtures/psychohistory/psy-012/README.md) del fixture da los comandos. Referencias de método: Scheffer et al. (2009), «Early-warning signals for critical transitions», *Nature* 461, 53–59, [doi:10.1038/nature08227](https://doi.org/10.1038/nature08227); Dakos et al. (2012), «Methods for detecting early warnings of critical transitions in time series illustrated using simulated ecological data», *PLoS ONE* 7(7), e41010, [doi:10.1371/journal.pone.0041010](https://doi.org/10.1371/journal.pone.0041010); Boettiger y Hastings (2012), «Quantifying limits to detection of early warning for critical transitions», *Journal of the Royal Society Interface* 9, 2527–2539, [doi:10.1098/rsif.2012.0125](https://doi.org/10.1098/rsif.2012.0125); Boettiger y Hastings (2012), «Early warning signals and the prosecutor's fallacy», *Proceedings of the Royal Society B* 279, 4734–4739, [doi:10.1098/rspb.2012.2085](https://doi.org/10.1098/rspb.2012.2085).

**Límites.** Una sola aproximación (phi de 0.5 a 0.9), un solo nivel de ruido, un nivel que deriva en línea recta por diseño. Los controles son únicamente AR(1) estacionarios: un ruido cambiante, la estacionalidad, un cambio de instrumento o la elección de los casos una vez ocurrido un cambio (la falacia del fiscal) pueden, cada uno por su cuenta, elevar los indicadores sin que haya transición, de modo que estas tasas describen la variedad más benigna de «no se acerca nada». La regla M y la eliminación de la tendencia dentro de cada ventana son simplificaciones de este fixture, no el procedimiento de un artículo citado. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Objeción más fuerte.** La escasa detección con 100 puntos puede deberse a esta receta y no a la alerta temprana como tal: una prueba de verosimilitud basada en un modelo, del tipo que defienden Boettiger y Hastings, aprovecha los datos con más eficiencia, y un registro que termine más cerca del pliegue lleva una señal más fuerte. Lo zanjaría aplicar una prueba así, y una aproximación más cercana, a las mismas series con semilla fija y con tasas de falsas alarmas iguales; eso no se hizo.

**Próxima comprobación.** Una magnitud por ejecución que cambie en la mayoría de los pares consecutivos, registrada con un instrumento sin cambios durante varios cientos de ejecuciones, permitiría calibrar una regla de este tipo para el proyecto. Aun así, una regla silenciosa no excluiría una transición: con 400 puntos captó del 55.8% al 65.3% de las aproximaciones simuladas.
