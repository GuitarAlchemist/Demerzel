---
module_id: psy-007-power-law-or-not
department: psychohistory
course: "¿Es una ley de potencia? Dieciocho recuentos de citas"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-007
version: "0.1.0"
---

# ¿Es una ley de potencia? Dieciocho recuentos de citas

> **Departamento de Psicohistoria** | Intermedio | 45 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo leerá una lista rango-tamaño, verá por qué una recta en un gráfico log-log no prueba una ley de potencia, estimará un exponente por máxima verosimilitud a partir de un corte explícito, comparará la ley de potencia con dos familias más simples y dirá qué puede distinguir una muestra tan pequeña. **Pregunta de proyecto:** entre sus temas, el departamento incluye «power law dynamics» (dinámica de leyes de potencia) en la eficacia de los artefactos; ¿respaldan los últimos recuentos de citas una ley de potencia frente a alternativas más simples?

[PSY-001](psy-001-intro-fractal-compounding.es.md) define una dimensión de compuesto, `D_c = log(value_ratio) / log(scale_ratio)` (su línea 66): el exponente de una relación de ley de potencia entre dos magnitudes, mientras que esta lección se pregunta cuántos elementos tienen cada tamaño. Ni PSY-001 ni [PSY-002](psy-002-governance-phase-transitions.es.md) emplean el término «ley de potencia». [PSY-009](psy-009-concentration-and-heavy-tails.es.md) mide la concentración sin suponer ninguna familia.

## 1. Lo que dice el registro y qué son los dieciocho números

**Observado.** El [registro del departamento](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) menciona las leyes de potencia tres veces, siempre como tema: las áreas de investigación «Fractal compounding analysis — measuring D_c, power laws, learning momentum» ([línea 10](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L10)) y «Power law dynamics — Pareto/Zipf distributions in artifact effectiveness» ([línea 17](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L17)), y la entrada del plan de estudios «Power Law Detection: identifying Pareto distributions in governance data» ([línea 26](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L26)). Ninguna nombra un conjunto de datos ni una prueba. La especificación que PSY-001 [cita en primer lugar](psy-001-intro-fractal-compounding.es.md#base-de-investigación) nombra ambos: la regla «If the top 20% of governance artifacts account for more than 60% of citations, a power law is present» ([línea 56](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56)), aplicada a los recuentos de citas de los registros de evolución ([línea 60](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L60)). Es un umbral sobre una proporción, no un ajuste.

Una *ley de potencia* asigna a un valor x una probabilidad proporcional a `x^-alpha`, con *exponente* alpha (las distribuciones de Pareto y de Zipf son de este tipo): los valores muy superiores al típico siguen siendo probables.

En la tendencia de calidad, la «eficacia» es una etiqueta categórica ([PSY-005](psy-005-persistence-baseline.es.md)); la regla de la especificación, y esta lección, usan `citation_count`: el número de archivos rastreados por Git que mencionan alguna de las *rutas de citación* del artefacto, contado con `git grep` ([`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15)).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/extract.py) toma una instantánea de la última ejecución en el commit `4b03838` (2026-10-13T18:43:54Z, [18 filas](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl#L217-L234)) y la guarda en [`observed-input.json`](../../../fixtures/psychohistory/psy-007/observed-input.json). Ordenados, y con un asterisco en los dos recuentos que no se midieron:

```text
65  55*  47  45  44  29  29  23  17  15  14  13  6  6  5  1  0  0*
```

La suma es 414. Tres hechos limitan lo que sigue:

- **Dieciséis mediciones, no dieciocho.** El 55 y el cero con asterisco no tienen `citation_source` ni ruta de citación, lo que el script interpreta como un artefacto externo: «[lives outside this repository (unmeasurable here)](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23)» (vive fuera de este repositorio y aquí no puede medirse); los dos conservaron un valor introducido a mano.
- **Recuentos dependientes.** Los dos 29 comparten casi todos sus archivos citantes: un artefacto incluye al otro entre sus rutas de citación; además, un mismo archivo puede citar varios artefactos.
- **Una coincidencia, no un uso.** La búsqueda es la de una cadena literal ([líneas 76–86](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L76-L86)): un archivo que solo enumera la ruta de un artefacto cuenta igual que uno que lo usa.

Una ley de potencia no asigna ninguna probabilidad a 0: se dejan aparte los dos ceros y quedan 16 recuentos positivos.

### Ejercicio práctico 1

¿Cuántos valores pueden entrar en un gráfico log-log, cuántos de ellos midió git grep y, como máximo, a cuántas mediciones distintas equivale eso?

> **Respuesta:** Entran en el gráfico `18 − 2 = 16` recuentos positivos. El 55 con asterisco se introdujo a mano: `16 − 1 = 15` mediciones de git grep. Los dos 29 cuentan casi los mismos archivos: como máximo, `15 − 1 = 14` mediciones distintas.

## 2. Una recta en papel log-log

En un *gráfico rango-tamaño* se representa `log10(count)` frente a `log10(rank)`, empezando por el recuento más alto. Bajo una ley de potencia de exponente alpha, los puntos quedan cerca de una recta de pendiente `−1 / (alpha − 1)`. La receta tentadora: ajustar una recta por mínimos cuadrados, leer `alpha = 1 + 1 / |slope|` e indicar el R², la proporción de la varianza que explica la recta. **Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/analyze.py) sobre los 16 recuentos positivos: pendiente −1.152, R² 0.669, exponente implícito 1.868.

**Sintético.** El script extrae 2,000 muestras de 16 valores de cada una de las tres familias ajustadas en la sección 4 ([`scenarios.json`](../../../fixtures/psychohistory/psy-007/scenarios.json) guarda sus parámetros como supuestos) y ajusta la misma recta:

| Familia generadora | R² mediano | Con R² de al menos 0.9 |
|---|---|---|
| Ley de potencia | 0.946 | 81.8% |
| Lognormal | 0.88 | 40.0% |
| Exponencial | 0.776 | 7.3% |

Clauset, Shalizi y Newman (2009, apéndice A) señalan que «in practice we rarely see a low r², regardless of the actual form of the distribution, so that the value of r² tells us little» (en la práctica rara vez se ve un r² bajo, sea cual sea la forma real de la distribución, de modo que el valor de r² dice poco). Aquí el valor bajo es el informativo: 1,989 de las 2,000 muestras de la ley de potencia alcanzan el 0.669 registrado.

### Ejercicio práctico 2

(a) La recta tiene pendiente −1.152: calcule el exponente que implica. (b) Los 16 recuentos de un colega dan un R² superior a 0.9. ¿Qué dice la tabla sobre su familia?

> **Respuesta:** (a) `1 + 1 / 1.152 = 1.868`. (b) Muy poco: un R² de 0.9 o más aparece en el 81.8% de las muestras de la ley de potencia, pero también en el 40.0% de las lognormales y en el 7.3% de las exponenciales. Solo un valor bajo discrimina: todas las muestras de la ley de potencia salvo `2,000 − 1,989 = 11` alcanzan 0.669.

## 3. El exponente por máxima verosimilitud, a partir de un corte explícito

La *máxima verosimilitud* elige el exponente con el que los valores observados son más probables. Una ley de potencia se ajusta a una *cola*, los valores iguales o superiores a un corte `x_min`, y todo ajuste debe indicar el corte y cuántos valores quedan.

```text
continua:    alpha = 1 + n / suma de ln(x / x_min)     error estándar = (alpha - 1) / sqrt(n)
discreta:    p(x) = x^-alpha / zeta(alpha, x_min)      alpha: media de ln x según el modelo = media muestral de ln x
```

`zeta(alpha, x_min)` es la suma de `k^-alpha` sobre los enteros `k >= x_min`. Estos recuentos son pocos y son enteros pequeños, así que esta lección ajusta la forma **discreta**; la fórmula continua trata los enteros como puntos de un continuo y puede calcularse a mano. Da un exponente 0.055 más alto con el corte 1 y 0.059 más alto con el corte 13; ninguna de las conclusiones que siguen depende de esta elección.

**Calculado** (KS, la *distancia de Kolmogorov–Smirnov*: la mayor diferencia entre las proporciones acumuladas de los datos y las de la ley ajustada):

| Corte `x_min` | Valores conservados | Exponente | Error estándar | KS |
|---|---|---|---|---|
| 1 | 16 | 1.297 | 0.075 | 0.395 |
| 13 | 12 | 2.21 | 0.349 | 0.214 |
| 44 | 5 | 7.602 | 2.955 | 0.174 |

En los diez cortes probados, el exponente va de 1.297 a 7.602: describe el corte tanto como los datos. La regla del artículo citado, la menor distancia KS, elige 44, una «cola» de cinco números. Esta lección presenta los cortes 1 (todos los recuentos positivos) y 13 (esa misma regla entre los cortes que conservan al menos 10 valores, un mínimo elegido después de ver los recuentos).

**Sintético.** En 2,000 colas de 12 valores extraídas de una ley de potencia de exponente 2.21, el 95% de los exponentes ajustados está entre 1.729 y 3.339.

### Ejercicio práctico 3

Con el corte 13 quedan 12 valores, y la suma de `ln(x / 13)` es 9.459. Calcule el exponente continuo y su error estándar; compárelos con el ajuste discreto.

> **Respuesta:** `alpha = 1 + 12 / 9.459 = 2.269`, y `(2.269 − 1) / sqrt(12) = 0.366`. El ajuste discreto da 2.21 con un error estándar de 0.349: las dos formas difieren en 0.059, alrededor de una sexta parte de cualquiera de los dos errores estándar.

## 4. Alternativas más simples, y lo que pueden decir dieciocho recuentos

Hay dos familias más simples definidas sobre los mismos enteros: una *exponencial* discreta (cada unidad adicional multiplica la probabilidad por una constante; sin cola pesada) y una *lognormal* (`ln x` sigue una distribución normal; aquí, redondeada al entero superior; dos parámetros). La *log-verosimilitud* de una familia ajustada es el logaritmo de la probabilidad que asigna a los datos; cuanto más alta, mejor. R es la log-verosimilitud de una familia menos la de otra (si es negativa, la segunda se ajusta mejor), y la prueba de Vuong (1989, tal como la aplica el artículo citado) da la probabilidad de obtener una razón tan alejada de cero si las dos se ajustan igual de bien; el artículo da el signo por fiable cuando p < 0.1, lo que esta lección llama decisivo.

Log-verosimilitudes **calculadas**, tomadas de [`results.json`](../../../fixtures/psychohistory/psy-007/results.json):

| Valores | Ley de potencia | Exponencial | Lognormal |
|---|---|---|---|
| Los 16 recuentos positivos | −80.97 | −67.74 | −69.93 |
| Los 12 recuentos de 13 o más | −49.96 | −48.24 | no ajustada |

Sobre todos los recuentos positivos, la ley de potencia es la peor de las tres, de forma decisiva: R = −13.23 frente a la exponencial (p < 0.0001) y −11.04 frente a la lognormal (p = 0.012). La exponencial y la lognormal no se separan (R = 2.19, p = 0.1779). Una prueba de bondad de ajuste coincide: la distancia KS registrada, 0.395, supera la de las 2,000 muestras sintéticas de la ley de potencia ajustada.

En la cola a partir de 13 no se decide nada: R = −1.71 frente a la exponencial (con valores sin redondear; p = 0.2557), y tampoco se descarta la ley de potencia (501 de 2,000 colas sintéticas quedan al menos igual de lejos de su ajuste, p = 0.2505, por encima del 0.1 del artículo). Sin embargo, con los cortes 15 y 17 la exponencial gana de forma decisiva (p = 0.0832 y 0.0364).

**Sintético: ¿qué pueden distinguir tan pocos valores?** En muestras de 16 valores, la familia generadora obtiene la mayor verosimilitud en 3,785 de 6,000, el 63.1%. Los recuentos registrados ponen en cabeza a la exponencial; eso ocurre en 2 de 2,000 muestras de la ley de potencia. En la cola, con una ley de potencia (alpha 2.21) y una exponencial (media 33) a partir de 13 como generadoras:

| Valores en la cola | Ley de potencia: signo correcto / y decisivo | Exponencial: signo correcto / y decisivo |
|---|---|---|
| 12 | 66.2% / 27.0% | 92.2% / 48.6% |
| 50 | 96.4% / 66.0% | 98.7% / 74.5% |
| 200 | 100.0% / 99.3% | 100.0% / 99.3% |

**Respuesta a la pregunta de proyecto:** no. Leídos como 16 extracciones independientes, los recuentos descartan una ley de potencia que empiece en 1; en los 12 recuentos de 13 o más, **esta muestra no permite distinguir una ley de potencia de una exponencial**.

### Ejercicio práctico 4

Clasifique las cuatro comparaciones de los cortes 1 y 13 con la regla del 0.1 y diga después qué frase respaldan los resultados: «los recuentos siguen una ley exponencial», «los recuentos no siguen una ley de potencia en todo su rango» o «la cola sigue una ley de potencia».

> **Respuesta:** Sobre todos los recuentos positivos, ley de potencia frente a exponencial (p < 0.0001) y frente a lognormal (p = 0.012): decisivas, en contra de la ley de potencia. Las otras dos (p = 0.1779 y p = 0.2557): sin decidir. Solo la segunda frase está respaldada. La primera falla porque la lognormal sigue en juego; la tercera, porque «no descartada» es más débil que «respaldada».

**La objeción más fuerte a esta lectura** es que describe el instrumento tanto como los artefactos ([PSY-011](psy-011-measurement-change-or-system-change.es.md)). Hasta el 2026-09-13, los recuentos se [introducían a mano](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8). En la última ejecución anterior a git grep, los mismos artefactos registraban 55, 12, 11, 8, 5, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1, 0, 0: el R² es 0.959, ninguna comparación de verosimilitudes es decisiva (frente a la exponencial: R = 1.27, p = 0.7688) y el valor p de la bondad de ajuste es 0.0805, ya por debajo de 0.1 (hoy: 0 de 2,000). La propia regla del proyecto se invierte con el instrumento: los tres o cuatro recuentos más altos (el 20% de 18 es 3.6) reunían el 67.2% o el 74.1% de las citas, una ley de potencia según su umbral del 60%, y hoy reúnen el 40.3% o el 51.2%. Retirar los dos recuentos introducidos a mano cambia poco (R = −12.08 frente a la exponencial, p = 0.0001).

### Ejercicio práctico 5

Puede medir más artefactos. A partir de la tabla de la cola, ¿cuántos valores de cola pediría y qué resultados le harían aceptar «ley de potencia» para la cola?

> **Respuesta:** Unos 200, una cifra calibrada solo frente a una exponencial: un veredicto decisivo y correcto llega en el 66.0% y el 74.5% de las muestras con 50 valores, y en el 99.3% con 200. Acepte la conclusión solo si se declaran el corte y el tamaño de la cola, el valor p de bondad de ajuste supera 0.1 y R favorece a la ley de potencia frente a las dos alternativas con p < 0.1.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** `extract.py` lee 27 archivos (cinco archivos de la tendencia de calidad, los 18 registros de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution), el registro del departamento, la especificación, PSY-001 y PSY-002) y se detiene si alguno difiere de su blob de Git fijado. El [README](../../../fixtures/psychohistory/psy-007/README.md) da los comandos, las 46 autocomprobaciones y los controles negativos.

**Referencias de método.** Clauset, A., Shalizi, C. R., y Newman, M. E. J. (2009), «Power-law distributions in empirical data», *SIAM Review* 51(4), 661–703, [arXiv:0706.1062](https://arxiv.org/abs/0706.1062): el método que se sigue aquí; advierte que los conjuntos de datos de menos de unos 50 valores «should be treated with caution» (deben tratarse con cautela). Vuong, Q. H. (1989), «Likelihood Ratio Tests for Model Selection and Non-Nested Hypotheses», *Econometrica* 57(2), 307–333.

**No realizado.** La prueba de bondad de ajuste mantiene fijo el corte, mientras que el artículo citado lo vuelve a estimar en cada muestra sintética: 0.2505 es probablemente demasiado indulgente. No se ajustaron una lognormal en la cola ni una ley de potencia truncada. Cada valor p trata los recuentos como extracciones independientes de una sola distribución; no son independientes, ni una muestra de los archivos gobernados: solo son los 18 que tienen registro de evolución. El valor p de Vuong es una aproximación para muestras grandes, usada aquí con 16 y 12 valores. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Aplicar la regla de git grep a todos los archivos rastreados y repetir el análisis. Una cola de unos 200 valores que supere la prueba de bondad de ajuste y gane de forma decisiva a las dos alternativas cambiaría la conclusión a «una ley de potencia es plausible en la cola».
