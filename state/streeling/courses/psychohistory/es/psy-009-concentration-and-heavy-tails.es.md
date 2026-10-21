---
module_id: psy-009-concentration-and-heavy-tails
department: psychohistory
course: "Concentración: cuando cuatro días reúnen la mitad de los eventos"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-009
version: "0.1.0"
---

# Concentración: cuando cuatro días reúnen la mitad de los eventos

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo ordenará los días de un registro de eventos, medirá lo desigual que es el reparto de los eventos entre ellos (proporciones de los k primeros, curva de Lorenz, coeficiente de Gini), comparará una media con una mediana y pondrá a prueba un plan de capacidad dimensionado con la media frente a otro dimensionado con un cuantil. **Pregunta de proyecto:** ¿qué parte de la actividad de los disparadores se concentra en los pocos días más cargados, y qué efecto tiene eso sobre un plan de capacidad basado en la media?

[PSY-002](psy-002-governance-phase-transitions.es.md) interpreta la duplicación de una tasa de señales, un recuento dividido por una ventana de tiempo, como indicio de una transición próxima. Una tasa es una media, y este módulo mide qué parte de una media pueden sostener unos pocos días. [PSY-008](psy-008-bursts-are-not-rates.es.md) compara los mismos recuentos diarios con una referencia de Poisson; [PSY-007](psy-007-power-law-or-not.es.md) y [PSY-022](psy-022-competing-explanations.es.md) ajustan distribuciones.

## 1. Ordenar los días y sumar desde arriba

**Observado.** Hasta su retirada el 2026-07-18, un [flujo de trabajo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) escribía un *archivo de disparador* (*trigger file*) por cada evento del repositorio. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) contiene 594, de tres tipos: *push*, incidencias (*issues*) abiertas y discusiones creadas. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/extract.py) guarda una instantánea de la carpeta en [`observed-input.json`](../../../fixtures/psychohistory/psy-009/observed-input.json). El día de un evento es la fecha UTC de su marca de tiempo. El registro va del 2026-03-20 al 2026-07-16: **119** días de calendario, **100** con al menos un evento y **19** sin ninguno.

**Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/analyze.py), con resultados en [`results.json`](../../../fixtures/psychohistory/psy-009/results.json) y porcentajes redondeados a dos decimales. Ordene los días del más cargado al más tranquilo y sume desde arriba: la *proporción de los k primeros* (*top-k share*) es la parte del total de eventos que cae en los k días más cargados.

Los cuatro días más cargados reúnen 286 de los 594 eventos, el 48.15%: casi la mitad, no la mitad del título de este módulo; para superar la mitad hace falta un quinto día. Los cuatro días forman dos pares de días contiguos, los días 21 y 22 de marzo (169 eventos) y 27 y 28 de junio (117), separados por 97 días (del 22 de marzo al 27 de junio), cada uno dentro de uno de los dos *episodios* de PSY-008 (días de ráfaga separados por 7 días como máximo). La proporción depende de dónde empieza un día: en los 24 husos horarios de UTC−11 a UTC+12 se sitúa entre el 48.15% (UTC, el valor más bajo) y el 55.05%, y alcanza o supera la mitad en 15 de ellos.

### Ejercicio práctico 1

Los diez días más cargados contienen 109, 72, 60, 45, 26, 24, 20, 20, 20 y 19 eventos, de un total de 594. Calcule la proporción del día más cargado, la de los cuatro más cargados y la de los diez más cargados, y el número de días necesario para superar la mitad.

> **Respuesta:** `109 / 594 = 18.35%`. `109 + 72 + 60 + 45 = 286` y `286 / 594 = 48.15%`. Los diez suman 415: `415 / 594 = 69.87%`. La mitad de 594 es 297; cuatro días dan 286 y cinco dan `286 + 26 = 312`, así que hacen falta cinco días (52.53%).

## 2. La curva de Lorenz y el coeficiente de Gini

La *curva de Lorenz* muestra todos los k a la vez: ordene los días del más tranquilo al más cargado y represente la proporción acumulada de eventos frente a la proporción acumulada de días. Con días iguales se obtendría la diagonal. **Calculado:** la mitad más tranquila de los días (60 de 119) contiene 41 eventos, el 6.90%; el 90% más tranquilo (108 días), el 27.10%.

El *coeficiente de Gini* G resume la curva en un solo número: el doble del área entre la diagonal y la curva. Con los n recuentos diarios ordenados de menor a mayor y T su total:

```text
G = suma sobre i de (2i - n - 1) * x_i / (n * T)        x_1 <= x_2 <= ... <= x_n
todos los días iguales  -> G = 0
un día los reúne todos  -> G = (n - 1) / n            118/119 = 0.9916 en este registro
```

El *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección) comprueba ambos límites. **Calculado:** G = 0.7789 sobre los 119 días de calendario y 0.7369 sobre los 100 días activos únicamente: no son los días vacíos lo que lo eleva.

Cero no es la vara de medir adecuada para esa cifra: el azar por sí solo hace que los días sean desiguales. **Sintético.** [`scenarios.json`](../../../fixtures/psychohistory/psy-009/scenarios.json) define 2,000 registros de control de 594 eventos, en los que cada evento se coloca en uno de los 119 días, sorteado al azar con probabilidad uniforme.

| Medida | Registro observado | 2,000 registros sintéticos: mediana (del más bajo al más alto) |
|---|---|---|
| Eventos en los cuatro días más cargados | 286 | 41 (34 a 52) |
| Días necesarios para superar la mitad | 5 | 40 (36 a 44) |
| Coeficiente de Gini | 0.7789 | 0.2468 (0.1958 a 0.2995) |

Ningún registro sintético alcanza el valor observado en ninguna fila: la colocación al azar da un coeficiente de Gini cercano a 0.25, no a 0.

### Ejercicio práctico 2

Un registro de cinco días tiene los recuentos diarios 0, 1, 1, 2, 6. Calcule su coeficiente de Gini, y después otra vez solo sobre sus cuatro días activos.

> **Respuesta:** n = 5 y T = 10; los pesos `2i − n − 1` son −4, −2, 0, 2, 4, la suma es `0 − 2 + 0 + 4 + 24 = 26`, y `G = 26 / 50 = 0.52`. Sobre 1, 1, 2, 6 los pesos son −3, −1, 1, 3: `−3 − 1 + 2 + 18 = 16` y `G = 16 / 40 = 0.40`. Quitar un día vacío reduce G aunque ningún evento se haya movido: indique qué días se contaron.

### Ejercicio práctico 3

Dos registros imaginarios contienen cada uno 594 eventos en 119 días. En el registro A, los cuatro días más cargados reúnen 42 eventos y G = 0.25; en el registro B, 89 eventos y G = 0.45. Clasifique cada uno respecto a los registros sintéticos y respecto al registro observado.

> **Respuesta:** A queda dentro del rango sintético en las dos medidas (de 34 a 52 eventos; de 0.1958 a 0.2995): es compatible con una colocación al azar. B queda por encima de todos los registros sintéticos en las dos, pero muy por debajo del observado: sus cuatro primeros días reúnen el `89 / 286 = 31.12%` de lo que reúnen los del registro observado, y 0.45 frente a 0.7789. El rango procede de un lote finito, no de una cota.

## 3. Media, mediana y una media que no se estabiliza

**Calculado.** La media es `594 / 119 = 4.99` eventos por día de calendario. La mediana, el valor central de los recuentos ordenados (la media de los dos valores centrales cuando su número es par), es 1: 63 días tienen exactamente un evento, y 100 de los 119 días quedan en la media o por debajo de ella, de modo que la media no describe un día habitual.

En un registro concentrado, unos pocos días sostienen la media, y esta se mueve con ellos. Sin el día más cargado cae de 4.99 a 4.11 (−17.66%); sin los cuatro más cargados, a 2.68 (−46.34%). La mediana se mantiene en 1. En los registros sintéticos, la misma eliminación mueve la media un 2.21% como máximo.

La misma inestabilidad aparece en el tiempo: leída a finales de marzo (12 días), de abril, de mayo y de junio, y después el último día, la media acumulada era 17.67, 5.88, 3.97, 5.14 y 4.99; la mediana fue 4.5 y después 1 cuatro veces.

De manera informal, unos recuentos son *de cola pesada* cuando los valores muy superiores al habitual son lo bastante frecuentes como para sostener una gran parte del total; una media muestral depende entonces de si la muestra ha recogido alguno. Esa descripción se ajusta a estos recuentos. La definición formal se refiere a la lentitud con la que decae la cola, y 119 días no permiten ponerla a prueba: dos episodios pueden producir cifras así sin que haya ninguna cola pesada.

### Ejercicio práctico 4

Vuelva a calcular la media sin el día más cargado y después sin los cuatro más cargados. ¿Qué número daría para «un día habitual», y para qué sigue sirviendo la media?

> **Respuesta:** `(594 − 109) / 118 = 485 / 118 = 4.11` y `(594 − 286) / 115 = 308 / 115 = 2.68`. Para un día habitual, dé la mediana, 1, que no se mueve en ninguno de los dos casos. La media sigue siendo el número adecuado para los totales: `4.99 × 119` devuelve los 594 eventos, salvo redondeo.

## 4. Dimensionar un plan con la media y después con un cuantil

**Observado.** Los disparadores se escribían para un *driver* autónomo (un agente que trabaja por ciclos) cuyo [archivo de habilidad](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md) dice que «ran 3 manual cycles in March 2026 and was never scheduled» (tres ciclos manuales en marzo, y nunca se programó). El mismo archivo fija dos límites: como máximo 50 disparadores en la cola de espera, y los disparadores con más de 72 horas de antigüedad se descartan. Los disparadores archivados nunca se consumieron, así que nada de lo que sigue es una medición.

**Sintético.** Supongamos un consumidor que atiende como máximo c eventos al día, empezando por los más antiguos; el resto espera, y la capacidad no utilizada se pierde. Un evento está *retrasado* cuando no se atiende en los 3 días siguientes a su día de llegada (el límite de 72 horas con una resolución de un día). El *percentil* p es el valor que ocupa la posición `ceil(p × n / 100)` en los recuentos ordenados (rango más cercano, la regla de los cuantiles de PSY-008).

| Plan | c por día | Eventos retrasados | Espera máxima |
|---|---|---|---|
| Media, redondeada hacia arriba | 5 | 489 | 33 días |
| Percentil 90 | 8 | 393 | 20 días |
| Percentil 95 | 24 | 49 | 6 días |
| Menor c suficiente | 34 | 0 | 3 días |
| Percentil 99 | 72 | 0 | 1 día |

El plan de la media ofrece `5 × 119 = 595` plazas para 594 eventos y parece suficiente. Atiende 440 y deja 154 esperando al final, porque la capacidad que queda ociosa en las semanas tranquilas no puede trasladarse a una semana cargada; sus eventos pendientes llegan a 205 en el punto máximo, más de cuatro veces el límite de 50 que el diseño fija para la cola de espera.

Parte de ese fracaso se debe a un plan sin margen, no a la concentración: en 1,919 de los 2,000 registros sintéticos, una capacidad de 5 también deja eventos retrasados (81 en el registro mediano). Pero allí la menor capacidad suficiente es de 5 a 7 al día, y el percentil 95 (de 8 a 11) nunca deja un evento retrasado. La concentración cambia el precio del remedio: 34 al día, 6.81 veces la media.

Todos los planes de la tabla están dimensionados a posteriori, sobre los mismos 119 días en los que se aplican, y un percentil alto no se estabiliza mejor que la media: leído a finales de mayo, el percentil 95 era 8, no 24, y una capacidad de 8 a partir del 1 de junio deja 199 eventos retrasados en los 46 días restantes. Con menos de 100 días leídos, el percentil 99 es el día más cargado hasta ese momento.

### Ejercicio práctico 5

Su criterio es el del diseño: ningún evento retrasado. ¿Qué plan de la tabla basado en un percentil lo cumple? Calcule la capacidad que ofrece a lo largo del registro el menor plan suficiente, y la proporción que se utiliza.

> **Respuesta:** A posteriori, solo el percentil 99; el 95 deja 49 eventos retrasados y una espera máxima de 6 días. La menor capacidad suficiente es de 34 al día: `34 × 119 = 4,046` plazas, de las que se utiliza el `594 / 4,046 = 14.68%` y queda ociosa el `100 − 14.68 = 85.32%`. Decida según la tolerancia y el costo de la capacidad ociosa, no según la media. La regla es supuesta y los tamaños se leen a posteriori: describen un patrón de llegadas, no un consumidor, y no son una receta para los próximos 119 días.

**La objeción más fuerte a la lectura de esta lección** es que un archivo de disparador no es una unidad de trabajo. El mismo archivo de habilidad fusiona los disparadores que comparten tipo, repositorio y referencia (*ref*), y los 594 comparten un mismo repositorio y una misma referencia: un *driver* que se activara una vez al día (una cadencia supuesta) habría recibido 132 disparadores fusionados, como máximo 3 al día, con un coeficiente de Gini de 0.3287. Según esa lectura, la concentración describe con qué frecuencia se activaba el productor, no cuánto trabajo llegaba. En segundo lugar, la proporción de los cuatro primeros descansa sobre dos episodios: **esta muestra no permite distinguir un proceso con un episodio cada pocos meses de dos incidentes sin relación entre sí.** Un registro del trabajo realizado por cada disparador zanjaría el primer punto; una serie de eventos más larga, el segundo.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los 594 archivos de disparadores, el flujo de trabajo y el archivo de habilidad enlazados más arriba. `extract.py` se niega a ejecutarse si la carpeta o un archivo de diseño difiere de su versión fijada.

**Fixture.** El [README](../../../fixtures/psychohistory/psy-009/README.md) da los comandos, los casos resueltos a mano, las 41 autocomprobaciones y los controles negativos.

**Leído fuera del fixture.** `git log --diff-filter=D` en el commit fijado enumera 12 archivos de disparadores borrados sin haberse archivado: siete con fecha 2026-03-20, cinco de ellos retirados de `processing/` por el commit del [ciclo 002 del driver](https://github.com/GuitarAlchemist/Demerzel/commit/2b752a763e490aa090cf32ee992cb923a6d1bc24), y cinco con fecha 2026-06-30, eliminados por el commit [`a2c1ef0`](https://github.com/GuitarAlchemist/Demerzel/commit/a2c1ef01d2470ca737b89e005eddc8aa78fa7583). Uno de los doce es un disparador `self_initiated`, no un evento del repositorio. Ninguno cae en uno de los cuatro días más cargados, que, contando los doce, reunirían el `286 / (594 + 12) = 47.19%`.

**Referencias de método.** Lorenz, M. O. (1905), «Methods of Measuring the Concentration of Wealth», *Publications of the American Statistical Association* 9(70), 209–219, doi:10.2307/2276207. Ceriani, L., y Verme, P. (2012), «The origins of the Gini index: extracts from Variabilità e Mutabilità (1912) by Corrado Gini», *The Journal of Economic Inequality* 10(3), 421–443, doi:10.1007/s10888-011-9188-x. Hyndman, R. J., y Fan, Y. (1996), «Sample Quantiles in Statistical Packages», *The American Statistician* 50(4), 361–365.

**No realizado.** No se ajustó ninguna distribución ni se contrastó ninguna ley para la cola de la distribución. La regla de capacidad es supuesta y solo usa recuentos de llegadas: ni tiempo de atención, ni prioridades, ni eliminación de duplicados. Los planes están dimensionados a posteriori: cuatro lecturas anteriores no ponen a prueba una regla de dimensionamiento. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Aplicar las mismas medidas a una serie de eventos del proyecto que siga creciendo, como los commits por día. Si su coeficiente de Gini se acerca al de una colocación al azar con su propio total y su propio número de días, la concentración encontrada aquí es propia del productor retirado, no del proyecto.
