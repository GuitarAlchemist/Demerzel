---
module_id: psy-022-competing-explanations
department: psychohistory
course: "Explicaciones rivales: comparar modelos con pocos datos"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-022
version: "0.1.0"
---

# Explicaciones rivales: comparar modelos con pocos datos

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo ajustará tres distribuciones de recuento por máxima verosimilitud, las ordenará con AIC y BIC, medirá con qué frecuencia estos criterios eligen el modelo verdadero con este tamaño de muestra y nombrará el supuesto que comparten los tres modelos. **Pregunta de proyecto:** los recuentos diarios de disparadores pueden «explicarse» con una distribución de Poisson, una geométrica o una binomial negativa; ¿qué explicación favorecen los datos, con qué contundencia, y qué sigue sin describir la ganadora?

[PSY-008](psy-008-bursts-are-not-rates.es.md) mostró que estos recuentos están mucho más dispersos que los de un proceso de Poisson y que los días cargados llegan en rachas; [PSY-007](psy-007-power-law-or-not.es.md) y [PSY-010](psy-010-growth-curves-short-series.es.md) ajustan otras familias a otros datos.

## 1. Tres candidatos y sus verosimilitudes

**Observado.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-022/extract.py) lee los 594 archivos de [`state/triggers/archived`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) en el commit `4b03838` y escribe [`observed-input.json`](../../../fixtures/psychohistory/psy-022/observed-input.json): un recuento por día de calendario UTC, n = 119 días del 2026-03-20 al 2026-07-16, S = 594 eventos. Hay 19 días sin ningún evento, 63 con exactamente uno, y el más cargado tiene 109; la varianza, 196.848669 (con divisor n), supera con creces a la media, 4.991597.

Cada candidato asigna una probabilidad a k eventos en un día y trata los días como extracciones independientes, así que la log-verosimilitud (log L) es una suma sobre los días:

```text
Poisson            P(k) = exp(-λ) λ^k / k!                 log L = S ln λ - n λ - Σ ln(x!)
geométrica         P(k) = (1 - q) q^k                      log L = n ln(1 - q) + S ln q
binomial negativa  P(k) = [r (r+1) ... (r+k-1) / k!] (r/(r+μ))^r (μ/(r+μ))^k
```

Igualar la derivada a cero da formas cerradas: λ = S/n y q = S/(n + S). Para la binomial negativa, μ = S/n, y r es el cero de la función de puntuación (*score*) d(log L)/dr, que se halla con una búsqueda sobre un solo parámetro; su varianza es μ + μ²/r (la de la geométrica es μ + μ², con r = 1). **Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-022/analyze.py):

| Modelo | Estimaciones | log L |
|---|---|---|
| Poisson | λ = 4.991597 | −1007.841 |
| geométrica | q = 594/713 = 0.8331 | −321.518 |
| binomial negativa | r = 0.430337, μ = 4.991597 | −298.913 |

**Comprobación de la búsqueda.** La bisección de la función de puntuación (tolerancia relativa de 1e-10 sobre r) devuelve 0.430337 desde tres intervalos iniciales, [1e-6, 1e6], [0.01, 100] y [0.2, 3]. Una búsqueda por sección áurea sobre log L coincide con ella con una diferencia inferior a 1e-6 y recupera las formas cerradas de la Poisson y de la geométrica. La función de puntuación cambia de signo una sola vez en una malla de 1e-4 a 1e4: hay un único máximo. Con r = 1, la log L de la binomial negativa es igual a la de la geométrica; con r = 10^6 se acerca a la de la Poisson, como predice la teoría.

### Ejercicio práctico 1

A partir de n = 119 y S = 594, calcule λ y q. Con ln(1 − q) = −1.790358 y ln q = −0.182602, reconstruya la log-verosimilitud de la geométrica. ¿Por qué tiene que alcanzar la binomial negativa al menos ese valor, sean cuales sean los datos?

> **Respuesta:** `λ = 594 / 119 = 4.991597`; `q = 594 / (119 + 594) = 594/713 = 0.8331`. Después, `log L = 119 × (−1.790358) + 594 × (−0.182602) = −213.0526 − 108.4656 = −321.5182`, es decir, −321.518. Con r = 1, la binomial negativa es la geométrica, así que su máximo sobre r no puede ser menor: la ganancia del modelo mayor está garantizada; solo su magnitud aporta información.

## 2. Poner precio al parámetro adicional: AIC y BIC

```text
AIC = 2k - 2 log L
BIC = k ln(n) - 2 log L        k = parámetros libres, ln(119) = 4.779123
```

Cuanto más bajo, mejor; k vale 1, 1 y 2; cada parámetro cuesta 2 puntos de AIC y 4.779 puntos de BIC. **Calculado** a partir de log L redondeada a tres decimales:

| Modelo | AIC | ΔAIC | BIC | ΔBIC |
|---|---|---|---|---|
| Poisson | 2017.682 | 1415.856 | 2020.461 | 1413.077 |
| geométrica | 645.036 | 43.21 | 647.815 | 40.431 |
| binomial negativa | 601.826 | 0 | 607.384 | 0 |

Los dos criterios dan el mismo orden: binomial negativa, geométrica, Poisson. El doble de la ganancia de log-verosimilitud que se obtiene al liberar r es 45.21.

**Con qué contundencia, según las escalas de las fuentes.** Burnham y Anderson (2004, p. 271) dan unas «simple rules of thumb» (reglas prácticas sencillas) para ΔAIC: hasta 2, «substantial support» (apoyo sustancial); de 4 a 7, «considerably less support» (bastante menos apoyo); por encima de 10, «essentially no support» (prácticamente ningún apoyo); los tramos de 2 a 4 y de 7 a 10 no tienen nombre. Kass y Raftery (1995, p. 777) gradúan el doble del logaritmo del factor de Bayes, que una diferencia de BIC aproxima a grandes rasgos (p. 778): de 0 a 2, «not worth more than a bare mention» (apenas digna de mención); de 2 a 6, evidencia positiva; de 6 a 10, fuerte; por encima de 10, muy fuerte; una escala que, según ellos, es «not a calibration» (no una calibración), sino «a rough descriptive statement» (una descripción aproximada). En ambas escalas, la geométrica y la Poisson quedan muy por detrás.

**Lo que no son estas cifras.** Un ΔAIC de 43.21 no es una probabilidad de que la geométrica sea falsa o de que la binomial negativa sea verdadera. Para Burnham y Anderson, un ΔAIC grande hace menos plausible que el modelo sea «the best approximating model in the candidate set» (el modelo que mejor aproxima dentro del conjunto de candidatos); al tratar el BIC (p. 279), añaden que una probabilidad a posteriori del modelo cercana a 1 «does not justify an inference» (no justifica inferir) que el modelo sea la verdad, lo que «requires an a priori certainty that the true model is in the model set» (exige tener la certeza a priori de que el modelo verdadero está en el conjunto de modelos).

### Ejercicio práctico 2

A partir de log L = −321.518 (geométrica) y −298.913 (binomial negativa), con ln 119 = 4.779123, calcule el AIC y el BIC de los dos modelos y las dos diferencias. Lea cada diferencia en la escala citada que le corresponde.

> **Respuesta:** AIC: `2 + 643.036 = 645.036` y `4 + 597.826 = 601.826`, diferencia de 43.21: «essentially no support» (prácticamente ningún apoyo) para la geométrica. BIC: `4.779123 + 643.036 = 647.815` y `9.558246 + 597.826 = 607.384`, diferencia de 40.431: «very strong» (muy fuerte) en la escala de Kass y Raftery. Son reglas prácticas sobre una clasificación, no probabilidades.

## 3. ¿Con qué frecuencia eligen los criterios el modelo verdadero?

**Sintético.** Cada modelo ajustado generó 5,000 muestras con semilla fija de días independientes, con cuatro longitudes (se muestran dos), y a cada muestra se le volvieron a ajustar los tres modelos. Proporción de muestras en las que cada criterio eligió el generador verdadero (AIC / BIC):

| Generador verdadero | 15 días | 119 días |
|---|---|---|
| Poisson | 95.62% / 97.54% | 93.62% / 98.62% |
| geométrica | 82.06% / 88.32% | 84.30% / 97.08% |
| binomial negativa | 57.28% / 49.84% | 100% / 99.94% |

Con 119 días, los errores van en un solo sentido: cuando la verdadera es la geométrica, AIC elige la binomial negativa en 785 de 5,000 muestras (15.70%), y BIC en 146 (2.92%). La teoría lo predice: la geométrica es la binomial negativa con r = 1, así que el doble de la ganancia obtenida al liberar r se comporta, en muestras grandes, como una chi cuadrado con 1 grado de libertad (Wilks 1938), y supera 2 con probabilidad 0.1573 y ln 119 con probabilidad 0.0288. Las dos proporciones simuladas quedan a menos de dos errores estándar de estos valores. Ninguna muestra generada por la geométrica se acercó a la ganancia observada de 45.21 (la mayor fue 12.934); 622 muestras generadas por la binomial negativa la alcanzaron.

**Calculado: qué sostiene la clasificación.** Nuevo ajuste tras dejar fuera los días más cargados:

| Días más cargados excluidos | r | ΔAIC (G − BN) | ΔBIC (G − BN) |
|---|---|---|---|
| 0 | 0.430337 | 43.21 | 40.431 |
| 1 (109 eventos) | 0.493112 | 25.996 | 23.226 |
| 2 (109, 72) | 0.556301 | 15.182 | 12.42 |
| 4 (45 o más) | 0.736965 | 1.578 | −1.167 |
| 11 (18 o más) | 2.702526 | 10.178 | 7.496 |

Los cuatro días más cargados, dos pares de días contiguos (21–22 de marzo, 27–28 de junio), sostienen la diferencia decisiva. Con once días excluidos, la binomial negativa vuelve a ganar, con r = 2.7, menos dispersa que la geométrica: un mismo nombre, dos formas. Si se añaden de nuevo los doce archivos de disparadores borrados sin archivarse (un recuento tomado de PSY-009), se obtienen 44.566 y 41.787: nada cambia.

### Ejercicio práctico 3

Sintético. Un registro imaginario de 15 días da a la geométrica un BIC 1.1 más bajo. Con esa longitud y los parámetros ajustados más arriba, BIC elige la geométrica en 4,416 de 5,000 muestras con semilla fija cuando la verdadera es la geométrica, y en 2,502 de 5,000 cuando la verdadera es la binomial negativa. ¿Qué conclusión comunica usted?

> **Respuesta:** 1.1 cae en la banda de 0 a 2, «not worth more than a bare mention» (apenas digna de mención). La comprobación coincide: elegir la geométrica es `4,416 / 2,502 = 1.76` veces más frecuente cuando la verdadera es la geométrica que cuando lo es la binomial negativa. Informe de que ambas son compatibles con el registro; 1.76 no es una probabilidad de que la geométrica sea la verdadera.

### Ejercicio práctico 4

Deje fuera los cuatro días más cargados: 115 días, log L −247.501 (geométrica) y −245.712 (binomial negativa), ln 115 = 4.744932. ¿Qué modelo elige cada criterio, y por qué margen?

> **Respuesta:** AIC: `2 + 495.002 = 497.002` frente a `4 + 491.424 = 495.424`: la binomial negativa, por 1.578. BIC: `4.744932 + 495.002 = 499.747` frente a `9.489864 + 491.424 = 500.914`: la geométrica, por 1.167. Los criterios discrepan, y los dos por menos de 2: el veredicto de 43.21 puntos descansa sobre 4 de 119 días.

## 4. El supuesto que comparten los tres

**Calculado: una comprobación absoluta.** Los criterios solo ordenan; los días esperados por banda muestran lo que describe cada ajuste:

| Eventos en el día | Observados | Poisson | geométrica | binomial negativa |
|---|---|---|---|---|
| 0 | 19 | 0.81 | 19.86 | 40.00 |
| 1 | 63 | 4.04 | 16.55 | 15.85 |
| 2 | 13 | 10.07 | 13.78 | 10.43 |
| 3 a 11 | 13 | 103.44 | 55.51 | 36.50 |
| 12 a 44 | 7 | 0.64 | 13.27 | 15.62 |
| 45 o más | 4 | 0.00 | 0.03 | 0.60 |

El modelo ganador mejora en la cola (0.60 días esperados con 45 eventos o más, frente a 0.03) y lo paga en el cuerpo de la distribución (ejercicio 5).

**Orden.** Barajar los días deja intactas las tres log-verosimilitudes (una autocomprobación), pero el orden de los datos importa: la autocorrelación de orden 1 de los recuentos es 0.4587, un valor que alcanzan 3 de 10,000 permutaciones al azar (percentil 95: 0.1454); sobre los rangos (cada recuento sustituido por su rango, con los empates repartiéndose su rango medio) es 0.3861, y ninguna permutación lo alcanza. Controles: un orden barajado da −0.0057, y los días ordenados de menor a mayor, 0.7209. A los días cargados les siguen días cargados: el supuesto compartido de días independientes e idénticamente distribuidos es falso aquí.

**Sintético: lo que la dependencia hace a los criterios.** En un proceso *geométrico con inercia* (*sticky geometric*), cada día repite el recuento del día anterior con probabilidad 0.46 y, si no, extrae un valor nuevo de la geométrica ajustada, de modo que cada día sigue teniendo la distribución geométrica. Sobre 5,000 muestras de 119 días, AIC elige la binomial negativa en 2,008 (40.16%, frente a 15.70% con días independientes) y BIC en 961 (19.22%, frente a 2.92%): las rachas parecen dispersión adicional. Solo 1 muestra alcanzó una ganancia de 45.21: estas rachas, por sí solas, rara vez producen la diferencia observada. El modelo binomial negativo es el menos malo de tres modelos de días independientes, no una descripción de cómo llegan los disparadores.

**La objeción más fuerte a la lectura de esta lección:** los cuatro días son datos, no ruido; una ganancia de 45.21 no apareció en ninguna muestra geométrica independiente y sí en 1 de 5,000 muestras con inercia, así que la binomial negativa capta con razón una cola más pesada. La cola es más pesada. Lo que sigue abierto es si la produjo una única binomial negativa, de la que se extrae un valor nuevo cada día: los cuatro días son dos episodios, no cuatro extracciones independientes, y el mal ajuste en 0 y 1 eventos indica que el cuerpo de la distribución es incorrecto. **Esta muestra no permite distinguir una marginal binomial negativa (la distribución del recuento de un día) de una mezcla de días ordinarios y raros episodios de ráfaga.** Lo zanjaría un registro más largo, con muchos más episodios, o un modelo de dos regímenes comparado con la binomial negativa sobre datos con los que no se ajustó ninguno de los dos.

### Ejercicio práctico 5

La binomial negativa ajustada da P(0) = 0.336109 y P(1) = 0.13316. Calcule cuántos días vacíos y cuántos días de un solo evento se esperan en 119, compárelos con el registro y reescriba «los recuentos diarios de disparadores siguen una distribución binomial negativa» como una afirmación que estos resultados respalden.

> **Respuesta:** `119 × 0.336109 = 40.00` días vacíos frente a 19, y `119 × 0.13316 = 15.85` días de un solo evento frente a 63: el modelo ganador falla en los dos recuentos más frecuentes por factores de alrededor de 2 y 4. Una afirmación respaldada: «De tres modelos de días independientes, AIC y BIC prefieren la binomial negativa; la preferencia descansa sobre cuatro días agrupados en dos episodios, el ajuste falla en los recuentos frecuentes y los días no son independientes.»

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** la carpeta de disparadores archivados enlazada más arriba; `extract.py` rechaza una carpeta que difiera de la versión fijada.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-022/extract.py`, y después `analyze.py` en la misma carpeta; `analyze.py --check` compara una ejecución nueva con el [`results.json`](../../../fixtures/psychohistory/psy-022/results.json) guardado. Las semillas y la configuración están en [`scenarios.json`](../../../fixtures/psychohistory/psy-022/scenarios.json); el [README](../../../fixtures/psychohistory/psy-022/README.md) enumera las autocomprobaciones, un caso resuelto a mano y los controles negativos.

**Referencias de método.** Akaike, H. (1974), «A new look at the statistical model identification», *IEEE Transactions on Automatic Control* 19(6), 716–723. Schwarz, G. (1978), «Estimating the Dimension of a Model», *The Annals of Statistics* 6(2), 461–464. Kass, R. E., y Raftery, A. E. (1995), «Bayes Factors», *Journal of the American Statistical Association* 90(430), 773–795 ([copia de los autores](https://sites.stat.washington.edu/raftery/Research/PDF/kass1995.pdf)). Burnham, K. P., y Anderson, D. R. (2004), «Multimodel Inference: Understanding AIC and BIC in Model Selection», *Sociological Methods & Research* 33(2), 261–304. Wilks, S. S. (1938), «The Large-Sample Distribution of the Likelihood Ratio for Testing Composite Hypotheses», *The Annals of Mathematical Statistics* 9(1), 60–62.

**No realizado.** No se ajustó ningún modelo de dependencia entre días, no se aplicó ninguna corrección del AIC para muestras pequeñas ni se hizo ninguna comparación sobre datos reservados (de eso se ocupa PSY-018). Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Ajustar a los 119 recuentos un modelo de dos estados (días ordinarios y días de ráfaga, cada uno con una probabilidad de permanecer en él): si reproduce los 19 días vacíos, los 63 días de un solo evento y una autocorrelación de orden 1 cercana a 0.46, la lectura pasa de «el menos malo de tres» a «dos regímenes».
