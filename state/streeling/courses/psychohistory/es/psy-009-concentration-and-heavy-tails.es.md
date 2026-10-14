---
module_id: psy-009-concentration-and-heavy-tails
department: psychohistory
course: "Concentración: cuando cuatro días tienen la mitad de los eventos"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-009
version: "0.1.0"
---

# Concentración: cuando cuatro días tienen la mitad de los eventos

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

Ordenará los días de un registro de eventos, medirá con cuánta desigualdad se reparten los eventos (proporciones de los k primeros, curva de Lorenz, coeficiente de Gini), comparará una media con una mediana y pondrá a prueba un plan de capacidad dimensionado sobre la media frente a otro dimensionado sobre un cuantil. **Pregunta de proyecto:** ¿cuánta de la actividad de disparo se concentra en los pocos días más cargados, y qué le hace eso a un plan de capacidad basado en una media?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lee una tasa de señales duplicada, un recuento dividido por una ventana de tiempo, como indicio de una transición próxima. Una tasa es una media, y este módulo mide cuánto de una media pueden llevar unos pocos días. [PSY-008](psy-008-bursts-are-not-rates.es.md) contrasta esos mismos recuentos diarios con una referencia de Poisson; [PSY-007](psy-007-power-law-or-not.es.md) y PSY-022 ajustan distribuciones.

## 1. Ordenar los días y sumar desde arriba

**Observado.** Hasta su retirada el 2026-07-18, un [flujo de trabajo](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) escribía un *archivo de disparador* por cada evento del repositorio. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) contiene 594, de tres tipos: envíos, incidencias abiertas y discusiones creadas. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/extract.py) toma una instantánea de la carpeta en [`observed-input.json`](../../../fixtures/psychohistory/psy-009/observed-input.json). El día de un evento es la fecha UTC de su marca de tiempo. El registro va del 2026-03-20 al 2026-07-16: **119** días naturales, **100** con al menos un evento y **19** sin ninguno.

**Calculado** por [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/analyze.py) en [`results.json`](../../../fixtures/psychohistory/psy-009/results.json), con los porcentajes redondeados a dos decimales. Ordenemos los días del más cargado al más tranquilo y sumemos desde arriba: una *proporción de los k primeros* es la parte de todos los eventos que cae en los k días más cargados.

Los cuatro días más cargados tienen 286 de los 594 eventos, el 48.15%: casi la mitad, no la mitad del título de este módulo; para pasar de la mitad hace falta un quinto día. Los cuatro días son dos pares de vecinos, el 21 y el 22 de marzo (169 eventos) y el 27 y el 28 de junio (117), a 97 días de distancia (del 22 de marzo al 27 de junio), cada par dentro de uno de los dos *episodios* de PSY-008 (días de ráfaga separados por 7 días como máximo). La proporción depende de dónde empiece un día: en los 24 relojes de UTC−11 a UTC+12 queda entre el 48.15% (UTC, el más bajo) y el 55.05%, y alcanza o supera la mitad en 15 de ellos.

### Ejercicio práctico 1

Los diez días más cargados tienen 109, 72, 60, 45, 26, 24, 20, 20, 20 y 19 eventos, de un total de 594. Calcule la proporción del día más cargado, la de los cuatro más cargados y la de los diez más cargados, y el número de días necesarios para pasar de la mitad.

> **Respuesta:** `109 / 594 = 18.35%`. `109 + 72 + 60 + 45 = 286` y `286 / 594 = 48.15%`. Los diez suman 415: `415 / 594 = 69.87%`. La mitad de 594 es 297; cuatro días dan 286 y cinco dan `286 + 26 = 312`, así que cinco días (el 52.53%).

## 2. La curva de Lorenz y el coeficiente de Gini

La *curva de Lorenz* muestra todos los k a la vez: se ordenan los días del más tranquilo al más cargado y se representa la proporción acumulada de días frente a la proporción acumulada de eventos. Unos días iguales darían la diagonal. **Calculado:** la mitad más tranquila de los días (60 de 119) tiene 41 eventos, el 6.90%; el 90% más tranquilo (108 días) tiene el 27.10%.

El *coeficiente de Gini* G condensa la curva en un solo número, el doble del área entre la diagonal y la curva. Con los n recuentos diarios ordenados de forma creciente y T su total:

```text
G = suma sobre i de (2i - n - 1) * x_i / (n * T)      x_1 <= x_2 <= ... <= x_n
todos los días iguales          -> G = 0
un día los tiene todos          -> G = (n - 1) / n    118/119 = 0.9916 en este registro
```

El fixture verifica ambos límites. **Calculado:** G = 0.7789 sobre los 119 días naturales y 0.7369 sobre los 100 días activos solos: no son los días vacíos los que lo hacen alto.

Cero es la vara de medir equivocada para esa cifra: el azar por sí solo hace desiguales los días. **Sintético.** [`scenarios.json`](../../../fixtures/psychohistory/psy-009/scenarios.json) define 2,000 registros de control de 594 eventos, cada evento colocado en uno de los 119 días extraído uniformemente al azar.

| Medida | Registro observado | 2,000 registros sintéticos: mediana (del más bajo al más alto) |
|---|---|---|
| Eventos en los cuatro días más cargados | 286 | 41 (34 a 52) |
| Días necesarios para pasar de la mitad | 5 | 40 (36 a 44) |
| Coeficiente de Gini | 0.7789 | 0.2468 (0.1958 a 0.2995) |

Ningún registro sintético alcanza el valor observado en ninguna fila: una colocación al azar da un coeficiente de Gini cercano a 0.25, no a 0.

### Ejercicio práctico 2

Un registro de cinco días tiene como recuentos diarios 0, 1, 1, 2, 6. Calcule su coeficiente de Gini y luego de nuevo sobre sus cuatro días activos solos.

> **Respuesta:** n = 5 y T = 10; los pesos `2i − n − 1` son −4, −2, 0, 2, 4, la suma es `0 − 2 + 0 + 4 + 24 = 26` y `G = 26 / 50 = 0.52`. Sobre 1, 1, 2, 6 los pesos son −3, −1, 1, 3: `−3 − 1 + 2 + 18 = 16` y `G = 16 / 40 = 0.40`. Quitar un día vacío baja G aunque no se haya movido ningún evento: diga qué días se contaron.

### Ejercicio práctico 3

Dos registros imaginarios tienen cada uno 594 eventos en 119 días. En el registro A los cuatro días más cargados tienen 42 eventos y G = 0.25; en el registro B, 89 eventos y G = 0.45. Clasifique cada uno frente a los registros sintéticos y frente al registro observado.

> **Respuesta:** A queda dentro del rango sintético en las dos medidas (34 a 52 eventos; 0.1958 a 0.2995): es compatible con una colocación al azar. B queda por encima de todos los registros sintéticos en ambas y, sin embargo, muy por debajo del observado: `89 / 286 = 31.12%` de sus eventos de cabeza, y 0.45 frente a 0.7789. El rango viene de un lote finito, no de una cota.

## 3. Media, mediana y una media que no se asienta

**Calculado.** La media es `594 / 119 = 4.99` eventos por día natural. La mediana, el valor central de los recuentos ordenados (la media de los dos valores centrales cuando su número es par), es 1: 63 días tienen exactamente un evento, y 100 de los 119 días están en la media o por debajo, lo que no describe un día habitual.

En un registro concentrado unos pocos días llevan la media, y esta se mueve con ellos. Sin el día más cargado baja de 4.99 a 4.11 (−17.66%); sin los cuatro más cargados, a 2.68 (−46.34%). La mediana se mantiene en 1. En los registros sintéticos la misma eliminación mueve la media como máximo un 2.21%.

La misma inestabilidad aparece en el tiempo: leída a finales de marzo (12 días), de abril, de mayo y de junio, y luego el último día, la media acumulada era 17.67, 5.88, 3.97, 5.14 y 4.99; la mediana era 4.5 y luego 1 cuatro veces.

De manera informal, unos recuentos tienen *cola pesada* cuando los valores muy por encima del habitual son lo bastante frecuentes para llevar una gran parte del total; una media de muestra depende entonces de si la muestra atrapó uno. Esa descripción encaja con estos recuentos. La definición formal se refiere a lo lentamente que decae la cola, y 119 días no permiten ponerla a prueba: dos episodios pueden producir cifras así sin ninguna cola pesada.

### Ejercicio práctico 4

Vuelva a calcular la media sin el día más cargado y luego sin los cuatro más cargados. ¿Qué número informaría para «un día habitual» y para qué sigue sirviendo la media?

> **Respuesta:** `(594 − 109) / 118 = 485 / 118 = 4.11` y `(594 − 286) / 115 = 308 / 115 = 2.68`. Informe la mediana, 1, para un día habitual; no se mueve en ninguno de los dos casos. La media sigue siendo el número correcto para totales: `4.99 × 119` devuelve los 594 eventos, salvo redondeo.

## 4. Dimensionar un plan sobre la media y luego sobre un cuantil

**Observado.** Los disparadores se escribían para un conductor autónomo cuyo [archivo de habilidad](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md) dice que «ran 3 manual cycles in March 2026 and was never scheduled». Ese mismo archivo fija dos límites: como máximo 50 disparadores en la cola, y los disparadores de más de 72 horas descartados. Los disparadores archivados nunca se consumieron, así que nada de lo que sigue es una medición.

**Sintético.** Supongamos un consumidor que atiende como máximo c eventos al día, los más antiguos primero; el resto espera, y la capacidad no usada se pierde. Un evento está *tardío* cuando no se atiende dentro de los 3 días siguientes a su día de llegada (el límite de 72 horas con resolución de un día). El *percentil* p es el valor en la posición `ceil(p × n / 100)` de los recuentos ordenados (rango más próximo, la regla de los cuantiles de PSY-008).

| Plan | c por día | Eventos tardíos | Espera más larga |
|---|---|---|---|
| Media, redondeada hacia arriba | 5 | 489 | 33 días |
| Percentil 90 | 8 | 393 | 20 días |
| Percentil 95 | 24 | 49 | 6 días |
| Menor c suficiente | 34 | 0 | 3 días |
| Percentil 99 | 72 | 0 | 1 día |

El plan de la media ofrece `5 × 119 = 595` huecos para 594 eventos y parece suficiente. Atiende 440 y deja 154 esperando al final, porque la capacidad que queda ociosa en las semanas tranquilas no puede trasladarse a una semana cargada; su acumulación alcanza un máximo de 205 eventos, más de cuatro veces el límite de cola de 50 del diseño.

Parte de ese fracaso corresponde a un plan sin margen, no a la concentración: en 1,919 de los 2,000 registros sintéticos una capacidad de 5 también deja eventos tardíos (81 en el registro mediano). Pero allí la menor capacidad suficiente es de 5 a 7 al día, y el percentil 95 (de 8 a 11) nunca deja un evento tardío. La concentración cambia el precio del remedio: 34 al día, 6.81 veces la media.

Todos los planes de la tabla están dimensionados a posteriori, sobre los 119 días en los que se ejecutan, y un percentil alto no se asienta mejor que la media: leído a finales de mayo, el 95 era 8, no 24, y una capacidad de 8 a partir del 1 de junio deja 199 eventos tardíos en los 46 días restantes. Con menos de 100 días leídos, el percentil 99 es el día más cargado hasta la fecha.

### Ejercicio práctico 5

Su criterio es el del diseño: ningún evento tardío. ¿Qué plan de percentil de la tabla lo cumple? Calcule la capacidad que ofrece el menor plan suficiente a lo largo del registro y la proporción que se usa.

> **Respuesta:** A posteriori, solo el percentil 99; el 95 deja 49 eventos tardíos y una espera más larga de 6 días. La menor capacidad suficiente es de 34 al día: `34 × 119 = 4,046` huecos, de los cuales se usa el `594 / 4,046 = 14.68%` y queda ocioso el `100 − 14.68 = 85.32%`. Decida por la tolerancia y el costo de la capacidad ociosa, no por la media. La regla es un supuesto y los tamaños se leen a posteriori: un patrón de llegadas, no un consumidor, y ninguna receta para los próximos 119 días.

**La objeción más fuerte a la lectura de esta lección** es que un archivo de disparador no es una unidad de trabajo. Ese mismo archivo de habilidad fusiona los disparadores que comparten tipo, repositorio y referencia, y los 594 comparten un repositorio y una referencia: un conductor que despertara una vez al día (una cadencia supuesta) habría recibido 132 disparadores fusionados, como máximo 3 al día, con un coeficiente de Gini de 0.3287. Bajo esa lectura, la concentración describe con qué frecuencia disparó el productor, no cuánto trabajo llegó. Segundo, la proporción de los cuatro primeros descansa sobre dos episodios: **esta muestra no permite distinguir un proceso con un episodio cada pocos meses de dos incidentes sin relación.** Un registro del trabajo hecho por disparador zanjaría lo primero; un flujo de eventos más largo, lo segundo.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los 594 archivos de disparador, el flujo de trabajo y el archivo de habilidad enlazados más arriba. `extract.py` se niega a ejecutarse cuando la carpeta o un archivo de diseño difiere de su fijación.

**Fixture.** El [README](../../../fixtures/psychohistory/psy-009/README.md) da los comandos, los casos resueltos a mano, las 41 autocomprobaciones y los controles negativos.

**Leído fuera del fixture.** `git log --diff-filter=D` en la fijación enumera 12 archivos de disparador borrados sin archivar: siete fechados el 2026-03-20, cinco de ellos retirados de `processing/` por el commit del [ciclo de conducción 002](https://github.com/GuitarAlchemist/Demerzel/commit/2b752a763e490aa090cf32ee992cb923a6d1bc24), y cinco fechados el 2026-06-30, descartados por el commit [`a2c1ef0`](https://github.com/GuitarAlchemist/Demerzel/commit/a2c1ef01d2470ca737b89e005eddc8aa78fa7583). Uno de los doce es un disparador `self_initiated`, no un evento del repositorio. Ninguno cae en uno de los cuatro días más cargados, que, contando los doce, tendrían el `286 / (594 + 12) = 47.19%`.

**Referencias de método.** Lorenz, M. O. (1905), «Methods of Measuring the Concentration of Wealth», *Publications of the American Statistical Association* 9(70), 209–219, doi:10.2307/2276207. Ceriani, L., y Verme, P. (2012), «The origins of the Gini index: extracts from Variabilità e Mutabilità (1912) by Corrado Gini», *The Journal of Economic Inequality* 10(3), 421–443, doi:10.1007/s10888-011-9188-x. Hyndman, R. J., y Fan, Y. (1996), «Sample Quantiles in Statistical Packages», *The American Statistician* 50(4), 361–365.

**No realizado.** No se ajustó ninguna distribución ni se puso a prueba ninguna ley de cola. La regla de capacidad es un supuesto y usa solo los recuentos de llegada: ni tiempo de atención, ni prioridad, ni deduplicación. Los planes están dimensionados a posteriori: cuatro lecturas anteriores no ponen a prueba una regla de dimensionamiento. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** Aplicar las mismas medidas a un flujo de eventos del proyecto que siga creciendo, como los commits por día. Si su coeficiente de Gini está cerca del de una colocación al azar para su propio total y sus propios días, la concentración hallada aquí pertenece al productor retirado, no al proyecto.
