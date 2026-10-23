---
module_id: psy-023-monitoring-a-plan
department: psychohistory
course: "Vigilar un plan: bandas de tolerancia y reglas de alarma"
level: intermediate
prerequisites: ["psy-012-early-warning-false-alarms", "psy-004-how-large-is-large"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-023
version: "0.1.0"
---

# Vigilar un plan: bandas de tolerancia y reglas de alarma

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo contará con qué frecuencia una sola mirada a un plan da una falsa alarma, verá por qué mirarlo cada semana multiplica ese riesgo, comparará una tolerancia fija con la suma acumulada de Page y elegirá un umbral a partir de los costos antes de que lleguen los datos. **Pregunta de proyecto:** un plan largo (25 cursos en cada uno de 21 departamentos) necesita una regla para decir «nos hemos desviado del plan»; ¿con qué frecuencia da una regla sencilla la alarma sin motivo, y con cuánto retraso detecta una ralentización real?

El plan es la cifra de un borrador de especificación del plan de estudios, que se usa tal cual y solo para dar una escala: el repositorio fijado no la recoge. Contiene [23 registros de departamento](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments), 21 de ellos con una carpeta de cursos, y la línea 57 de su [README](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L57) dice «Streeling University — 23 departments, 21 course tracks» (departamentos e itinerarios de cursos), sin indicar cuántos cursos tiene cada itinerario. No se midió ninguna producción semanal del proyecto, así que nada de lo que sigue dice si el proyecto cumple su plan o se ha desviado de él.

[PSY-012](psy-012-early-warning-false-alarms.es.md) calibró una alarma para una sola mirada a un registro terminado; aquí la mirada se repite cada semana, y eso es lo que infla las falsas alarmas. [PSY-010](psy-010-growth-curves-short-series.es.md) ajusta el historial de crecimiento; este módulo supone que existe un calendario. Todo lo que sigue es **sintético**: supuestos en [scenarios.json](../../../fixtures/psychohistory/psy-023/scenarios.json), cálculo con [analyze.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-023/analyze.py), resultados guardados en [results.json](../../../fixtures/psychohistory/psy-023/results.json).

## 1. Una sola mirada al plan

El plan: 21 × 25 = 525 cursos a razón de 5 por semana, es decir, 105 semanas. Suponga que cada semana hay 10 borradores en curso y que cada uno se termina dentro de la semana con probabilidad 1/2, de forma independiente. La producción de una semana es entonces el número de caras al lanzar 10 monedas equilibradas: media 5, varianza 5/2, desviación estándar 1.5811. El *déficit* tras t semanas es el total previsto menos el total real. Al ritmo previsto, tiene media 0 y desviación estándar `sqrt(5t/2)`: 8.0623 en la semana 26 y 16.2019 en la semana 105.

Usar monedas en lugar de ruido normal convierte cada probabilidad en un recuento exacto sobre historias de lanzamientos igual de probables (2^10 = 1,024 por semana); una simulación con semilla fija de 20,000 trayectorias comprueba después cada cifra exacta, y no al revés.

Dos reglas pueden comprobarse en una semana elegida de antemano:

- Un *límite semanal*: alarma cuando la producción de la semana es 1 como máximo. Eso ocurre en 1 + 10 = 11 de las 1,024 historias, 0.010742. Primeras semanas simuladas: 215 de 20,000, 0.01075 (error estándar 0.000729; intervalo exacto al 95% de 0.009367 a 0.012278, como en [PSY-004](psy-004-how-large-is-large.es.md)).
- Una *banda de predicción*: alarma cuando el déficit supera 2 desviaciones estándar, `2 sqrt(5t/2)`.

### Ejercicio práctico 1

Compruebe la banda una sola vez, en la semana 26. Indique el total previsto, la anchura de la banda, el menor déficit entero que dispara la alarma y el mayor total real con el que se dispara. El *fixture* (los datos y scripts que acompañan a la lección) cuenta una probabilidad de 0.020247 para esa mirada; ¿por qué no es la cola normal, 0.02275?

> **Respuesta:** Total previsto: `26 × 5 = 130`. Desviación estándar: `sqrt(26 × 5/2) = sqrt(65) = 8.0623`; dos de ellas suman 16.1245. El menor déficit entero por encima de ese valor es 17, así que la alarma se dispara con un total de `130 − 17 = 113` o menos. La producción se cuenta en cursos enteros, así que el recuento (0.020247) no es la cola de una variable normal continua (0.02275).

## 2. Mirar cada semana

Comprobado cada semana, un límite semanal da miradas independientes, con formas cerradas. Para una probabilidad de alarma a por semana al ritmo previsto:

```text
P(al menos una alarma en T semanas) = 1 - (1 - a)^T
longitud media de corrida           = 1 / a
```

La *longitud media de corrida* (ARL, *average run length*) es el número medio de semanas hasta la primera alarma; la sección 6.3.2.3.1 del manual de NIST/SEMATECH la define como «the average number of samples (subgroups) taken before an action signal is given» (el número medio de muestras, o subgrupos, que se toman antes de que se dé una señal de actuación). Para el límite 1, a = 11/1024 y la ARL es de 93.09 semanas, menos que la duración del plan: la regla se dispara al menos una vez en una fracción 0.678266 de los planes al ritmo previsto. La recursión del fixture reproduce exactamente la fórmula; la simulación da 13,552 de 20,000, 0.6776 (error estándar 0.003305).

La banda comprobada cada semana da miradas dependientes (el déficit de la semana 27 es el de la semana 26 más una semana), así que la fórmula del producto deja de valer, y la probabilidad de que el déficit cruce la banda al menos una vez en un horizonte dado no tiene una forma cerrada sencilla. La recursión la calcula exactamente, semana a semana, a partir de las historias que todavía no la han cruzado. Para la banda de 2 desviaciones estándar, ninguna mirada aislada supera 0.028332 y, sin embargo, la banda se dispara al menos una vez hasta la semana 105 en una fracción 0.170761 de los planes al ritmo previsto, 6.03 veces la mayor mirada aislada. La simulación: 3,380 de 20,000, 0.169 (error estándar 0.00265). La suma de las 105 miradas aisladas, 2.359684, es una cota superior válida, e inútil.

### Ejercicio práctico 2

Para el límite semanal «producción de 1 como máximo»: (a) dé la ARL y la probabilidad de al menos una alarma hasta la semana 52; (b) con la cota `P(at least one alarm) ≤ T × a`, halle la probabilidad por semana que limitaría al 5% la probabilidad de alarma en todo el plan. ¿Puede algún límite semanal lograrlo?

> **Respuesta:** (a) `1024 / 11 = 93.09` semanas; `1 − (1 − 11/1024)^52 = 0.429713`. (b) `0.05 / 105 = 0.000476` (resolver exactamente `1 − (1 − a)^105 = 0.05` da 0.000488). El límite más estricto, una semana vacía, tiene `1/1024 = 0.000977`, alrededor del doble de lo admisible: ningún límite semanal es lo bastante silencioso. Ese límite sigue disparándose en una fracción 0.097502 de los planes al ritmo previsto.

## 3. Una tolerancia y la suma acumulada de Page

Dos reglas vigilan el déficit acumulado. La *tolerancia* se dispara cuando el déficit alcanza c cursos. La *suma acumulada* de Page (Page, 1954) puntúa cada semana como su déficit menos un *valor de referencia* k, y se dispara cuando la suma de las puntuaciones queda al menos el *intervalo de decisión* h por encima de su valor más bajo anterior, contando el valor inicial 0. El enunciado del manual: «If the distance between a plotted point and the lowest previous point is equal to or greater than h, one concludes that the process mean has shifted (increased)» (si la distancia entre un punto representado y el punto anterior más bajo es igual o mayor que h, se concluye que la media del proceso se ha desplazado al alza). La recursión siguiente es equivalente; las dos formas coinciden en todas las trayectorias simuladas.

```text
tolerancia:      S(t) = S(t-1) + 5 - producción(t);              alarma si S(t) >= c
suma acumulada:  C(t) = max(0, C(t-1) + 5 - producción(t) - k);  alarma si C(t) >= h
```

Aquí k = 1, la mitad de los 2 cursos por semana que se pierden con la ralentización supuesta: a partir de la semana 53, 6 borradores en curso, una media de 3 cursos, el 60% del plan. Una regla está *calibrada* en el menor umbral entero cuya probabilidad exacta de alarma en 105 semanas al ritmo previsto es del 5% como máximo: c = 32 (31 da 0.052439) y h = 8 (7 da 0.084257). El *retraso* es el número de semanas lentas transcurridas cuando llega la alarma, entre los planes que no han dado ninguna alarma hasta la semana 52 (las trayectorias continúan más allá de la semana 105).

| Regla | Alarma al ritmo previsto, exacta | Simulada ± EE [intervalo exacto al 95%] | Retraso medio, exacto (simulado ± EE) | 90% de los retrasos, como máximo |
|---|---|---|---|---|
| Tolerancia 32, calibrada | 0.045372 | 0.0458 ± 0.001478 [0.042944, 0.048789] | 16.5 (16.56 ± 0.04) | 25 |
| Tolerancia 40 | 0.012603 | 0.01185 ± 0.000765 [0.010397, 0.013448] | 20.44 (20.5 ± 0.04) | 29 |
| Suma acumulada 6 | 0.185318 | 0.18365 ± 0.002738 [0.178305, 0.189087] | 5.88 (5.87 ± 0.02) | 10 |
| Suma acumulada 8, calibrada | 0.037333 | 0.03655 ± 0.001327 [0.033992, 0.039244] | 7.85 (7.85 ± 0.02) | 12 |
| Suma acumulada 10 | 0.007136 | 0.0064 ± 0.000564 [0.005342, 0.007605] | 9.83 (9.82 ± 0.03) | 15 |

Dentro de cada regla, un umbral más silencioso significa una alarma más tardía: ningún umbral sale gratis. Con niveles de falsas alarmas comparables, la suma acumulada señala la ralentización tras 7.85 semanas de media, frente a 16.5, un cociente de 0.4754; su ARL es de 2,623.4 semanas al ritmo previsto y de 8.3 tras una ralentización, partiendo de cero. La tolerancia es más lenta porque acumula todo excedente: un plan que va adelantado tiene que perder primero su ventaja. Una semana al ritmo previsto puntúa −1 en la suma acumulada, así que C vuelve a derivar hacia cero y olvida el pasado. Uno de los 28 intervalos simulados al 95% no contiene su valor exacto (intervalo de decisión 9, 2.97 errores estándar por debajo), más o menos uno de cada veinte, como cabía esperar.

### Ejercicio práctico 3

Un registro inventado de 12 semanas: 7, 6, 6, 5, 3, 4, 2, 3, 4, 2, 3, 3; la ralentización empezó en la semana 5. Calcule S y C (k = 1) cada semana. ¿Qué regla calibrada se dispara, y cuándo?

> **Respuesta:** Déficits semanales: −2, −1, −1, 0, 2, 1, 3, 2, 1, 3, 2, 2. S: −2, −3, −4, −4, −2, −1, 2, 4, 5, 8, 10, 12: la tolerancia (32) sigue en silencio, a 20 cursos de dispararse, unas `20 / 2 = 10` semanas lentas más. Puntuaciones: −3, −2, −2, −1, 1, 0, 2, 1, 0, 2, 1, 1, así que C: 0, 0, 0, 0, 1, 1, 3, 4, 4, 6, 7, 8. La suma acumulada se dispara en la semana 12, la 8.ª semana lenta. La tolerancia sigue arrastrando la ventaja de 4 cursos de las semanas 1 a 4; la suma acumulada la descartó.

## 4. Elegir el umbral a partir de los costos, y fijarlo antes de mirar

Un umbral elegido después de leer el registro no tiene una tasa de falsas alarmas conocida: lo eligió el registro.

### Ejercicio práctico 4

Un colega que lee el registro cada semana ve en la semana 61 un déficit de 25 cursos, y la banda de 2 desviaciones estándar se dispara a partir de 25. Su informe: «al ritmo previsto, un déficit así de grande en la semana 61 tiene una probabilidad de 0.023586; el plan se ha desviado». Clasifique la afirmación e indique la regla que usaría usted en su lugar.

> **Respuesta:** No respaldada. 0.023586 es la probabilidad de una sola mirada en una semana elegida de antemano. El colega habría informado de cualquier semana en la que se cruzara la banda, y ese procedimiento se dispara en una fracción 0.170761 de los planes al ritmo previsto en 105 semanas. Fije una regla antes de mirar, calibrada sobre el plan completo: la tolerancia 32 o la suma acumulada 8, cada una con un 5% como máximo.

El objetivo del 5% es en sí mismo una convención, no un costo. Con costos supuestos (una ralentización a partir de la semana 53 con probabilidad q = 1/2, un costo de 2 cursos por cada semana lenta antes de la alarma y de F cursos de revisión por cada falsa alarma):

```text
costo esperado = (1 - q) × P(falsa alarma) × F + q × retraso medio × 2
```

Con F = 20, el intervalo de decisión más barato es 7 (7.7 cursos); con F = 100, es 9 (9.66). El 8 calibrado no es el más barato en ninguno de los dos casos.

### Ejercicio práctico 5

Con q = 1/2, 2 cursos por semana lenta y F = 20, calcule a partir de la tabla el costo esperado de los intervalos de decisión 6 y 8, y el costo de una falsa alarma con el que empatan.

> **Respuesta:** h = 6: `0.5 × 0.185318 × 20 + 0.5 × 5.88 × 2 = 1.85 + 5.88 = 7.73`. h = 8: `0.5 × 0.037333 × 20 + 0.5 × 7.85 × 2 = 0.37 + 7.85 = 8.22`. Empatan cuando `0.5 × F × (0.185318 − 0.037333) = 7.85 − 5.88`, así que `F = 1.97 / 0.0739925 = 26.62` con las cifras redondeadas de la tabla (26.55 con las exactas). Por debajo del empate, h = 6 es más barato; por encima, h = 8.

**La objeción más fuerte** es que cada umbral pertenece a su modelo de producción. PSY-010 encontró que los módulos se añaden en ráfagas, y [PSY-008](psy-008-bursts-are-not-rates.es.md) muestra cómo engaña una tasa media cuando las llegadas se producen en ráfagas. Mantenga la media de 5 por semana, pero entréguela por lotes: 40 borradores en curso una semana de cada cuatro, ninguno las demás. La varianza semanal pasa a ser 155/2, 31 veces la de la producción regular. La tolerancia calibrada 32 se dispara entonces en una fracción 0.704574 de los planes al ritmo previsto (simulada: 0.7046 ± 0.003226), y la suma acumulada 8, en una fracción 1.000000 de ellos con seis decimales (20,000 de 20,000 simulados, intervalo de 0.999816 a 1). La elección de k también tiene su contrapartida: para una ralentización más suave (8 borradores, el 80% del plan), una semana lenta puntúa 0 de media, y el retraso medio de la suma acumulada, 41.45 semanas, supera al de la tolerancia, 32.78; de los planes que no han dado ninguna alarma hasta la semana 52, una fracción 0.261752 y otra 0.076485, respectivamente, siguen sin alarma cuando termina el plan. **Este modelo no puede decir qué regla conviene al proyecto**: para eso hacen falta la producción semanal del proyecto y una decisión sobre qué ralentización merece detectarse.

## Fuentes, límites y próxima comprobación

**Fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** la línea del README y los registros de departamento citados más arriba, para dar una escala; no se leyó ningún archivo de datos.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py`, y después el mismo comando con `--check`, que compara una ejecución nueva con los resultados guardados. El [README](../../../fixtures/psychohistory/psy-023/README.md) enumera las 24 autocomprobaciones, entre ellas un caso resuelto a mano y un control negativo.

**Referencias de método.** Page, E. S. (1954), «Continuous Inspection Schemes», *Biometrika* 41(1–2), 100–115, doi:10.1093/biomet/41.1-2.100. NIST/SEMATECH *e-Handbook of Statistical Methods*, sección [6.3.2.3.1](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc3231.htm), fuente de las dos citas, y sección [6.3.2.3](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm), sobre los gráficos de suma acumulada. Brook, D., y Evans, D. A. (1972), «An approach to the probability distribution of cusum run length», *Biometrika* 59(3), 539–549, doi:10.1093/biomet/59.3.539 (la idea de la cadena de Markov en la que se basa la recursión del fixture). Armitage, P., McPherson, C. K., y Rowe, B. C. (1969), «Repeated Significance Tests on Accumulating Data», *Journal of the Royal Statistical Society, Series A* 132(2), 235–244, doi:10.2307/2343787 (por qué las miradas repetidas inflan una tasa de error).

**No realizado.** No se leyó ninguna producción semanal del proyecto. No se consultó el artículo de Page de 1954; su regla se enuncia tal como la da el manual. Solo se estudiaron reglas unilaterales y una única ralentización brusca y permanente; no reglas bilaterales, derivas graduales ni la estimación del tamaño de una ralentización. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Cuando exista un calendario, extraer la producción semanal del proyecto (las adiciones de módulos fechadas de PSY-010 son un punto de partida), estimar su varianza y su proporción de semanas vacías, y recalibrar las dos reglas con esa dispersión. Si la producción llega en ráfagas, los umbrales anteriores se dispararían en la mayoría de los planes al ritmo previsto.
