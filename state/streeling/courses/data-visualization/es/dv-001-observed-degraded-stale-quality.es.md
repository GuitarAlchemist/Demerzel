---
module_id: dv-001-observed-degraded-stale-quality
department: data-visualization
course: Ejecuciones observadas, degradadas y datos obsoletos
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-04-001
version: "0.1.0"
---

# Ejecuciones observadas, degradadas y datos obsoletos

> **Departamento de Visualización de Datos** | Nivel: principiante | Duración estimada: 35 minutos | Estado: pendiente de revisión

## Objetivos

Al terminar esta lección, usted podrá:

- distinguir una tasa de aprobación medida de una ejecución no disponible y de un valor histórico trasladado;
- dibujar una serie temporal sin convertir la falta de medición en un fallo ni unir silenciosamente puntos a través de una interrupción;
- comprobar el denominador, la antigüedad y el entorno antes de comparar dos mediciones;
- ofrecer una descripción textual y una tabla como alternativas accesibles al gráfico.

## La pregunta del proyecto

GA guarda los resultados de control de calidad de su chatbot en `state/quality/chatbot-qa/`. Una persona que consulta el panel pregunta: «¿Empeoró el chatbot?». La visualización solo debe responder hasta donde lo permitan los registros. Usaremos cuatro **resultados históricos** fijados al commit de GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). Sirven para el ejercicio; no describen el estado actual del chatbot.

| Fecha del resultado | `total_prompts` | `pass_pct` | `degraded` | Qué permite afirmar el registro |
|---|---:|---:|---|---|
| [2026-06-08](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-08.json) | 52 | `null` | `true` | El backend no estaba disponible; no se publicó una tasa de aprobación. |
| [2026-06-15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) | 52 | 75,00 | `false` | Se publicó una tasa para esta ejecución. |
| [2026-06-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-19.json) | 52 | 7,69 | `false` | Se publicó una tasa baja; este archivo no explica la causa. |
| [2026-07-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) | 52 | 98,08 | `false` | Se publicó una tasa más alta para una ejecución posterior. |

### Ejercicio práctico

Clasifique cada fila como tasa observada o ejecución no disponible. ¿Cuál puede colocarse en el 0 % del eje de tasas?

> **Respuesta:** El 15 de junio, el 19 de junio y el 19 de julio tienen tasas publicadas. La ejecución del 8 de junio no estuvo disponible. Ninguna fila publica una tasa del 0 %; colocar allí el 8 de junio inventaría una medición.

## 1. Tres estados distintos

Una **observación** es un valor realmente publicado por una ejecución. Una **ejecución no disponible** indica que no se pudo obtener o confiar en la medición bajo las condiciones descritas. Un **valor trasladado** es una observación anterior mostrada como contexto; no es una medición nueva en la fecha del panel.

El archivo del 8 de junio contiene `pass_pct: null`, `degraded: true` y `degraded_reason: "backend_unavailable"`. También contiene `last_known_good_pass_pct: 94.0`, una fecha anterior y `last_known_good_source: "carryforward"`. Ese 94 % corresponde a la observación anterior. Dibujarlo como punto del 8 de junio haría parecer que el rendimiento siguió estable durante la interrupción. Dibujar `null` como cero haría parecer que el chatbot falló. Ambas transformaciones cambian la afirmación.

Conserve dos campos en el modelo visual: `quality_value` para la tasa medida y `run_status` para el estado observado, degradado o desconocido. Conserve la fecha original de toda referencia histórica por separado de la fecha en que se muestra. No deduzca una tasa de `total_prompts`: la nota del 8 de junio informa de errores del backend, no de respuestas del chatbot evaluadas.

### Ejercicio práctico

Una tarjeta dice «94 % de aprobación el 8 de junio» porque el archivo contiene `last_known_good_pass_pct: 94.0`. Reescríbala en una oración.

> **Respuesta:** «Control de calidad no disponible el 8 de junio: backend inaccesible; última buena medición conocida, 94 % el 16 de mayo». La fecha histórica debe ser visible y la tasa del 8 de junio debe quedar como desconocida.

## 2. Separar calidad y disponibilidad

Reserve el eje de tasas para los valores medidos. Deje un hueco cuando `pass_pct` sea `null`, en vez de unir puntos a través de él. Una segunda banda, alineada por fecha, puede marcar la ejecución del 8 de junio como degradada con un icono **y una etiqueta**. Así se responden dos preguntas diferentes: qué calidad se midió y si hubo una medición disponible.

Para los cuatro registros basta este boceto textual:

```text
Fecha         Calidad              Disponibilidad
2026-06-08    sin punto            DEGRADADA: backend no disponible
2026-06-15    75,00 %              observada
2026-06-19     7,69 %              observada; investigar
2026-07-19    98,08 %              observada
```

Las fechas están separadas; no son cuatro mediciones diarias consecutivas. Una línea entre el 19 de junio y el 19 de julio sugeriría que se midieron los días omitidos y que la trayectoria fue uniforme. En la serie completa, corte la línea en los intervalos sin datos. Sitúe los puntos según el tiempo transcurrido, no como categorías igualmente espaciadas. El [informe histórico de calidad de GA en el commit fijado](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) también marca fuentes obsoletas: un valor llamado «último» necesita su fecha de observación.

### Ejercicio práctico

Esboce dos bandas para el 8 y el 15 de junio, con fechas y etiquetas. ¿Debe unirse el 94 % trasladado con el 75 % del 15 de junio?

> **Respuesta:** El 8 de junio no tiene punto de calidad y muestra «backend no disponible». El 15 de junio tiene un punto de 75 % y la etiqueta «observada». El 94 % se anota con su fecha original, el 16 de mayo; no es un punto del 8 de junio ni inicia un segmento hacia el 15.

## 3. Una cifra baja exige investigación

El 19 de junio se informó un 7,69 % y `degraded: false`. El gráfico debe mostrar ese resultado, pero el archivo por sí solo no permite concluir si el código de GA sufrió una regresión, si cambió el modelo, si cambió el corpus o si se comportó de otra manera alguna dependencia. `degraded: false` es la clasificación del productor para esa ejecución, no un certificado completo de salud. Investigue la configuración, la identidad de las preguntas, los registros del backend, las reglas de puntuación y las ejecuciones cercanas antes de atribuir una causa.

Las tres filas observadas indican 52 preguntas cada una. Eso aporta contexto, pero un número igual no demuestra que fueran las mismas preguntas ni que se puntuaran igual. Una comparación debería fijar las revisiones del corpus y del evaluador. Si no figuran, indique que la comparación es provisional. Un porcentaje aislado puede ocultar la fragilidad de una muestra pequeña.

### Ejercicio práctico

Evalúe esta frase: «GA se recuperó de una regresión de software confirmada entre el 19 de junio y el 19 de julio». ¿Qué se observó y qué falta demostrar?

> **Respuesta:** Los archivos informan 7,69 % el 19 de junio y 98,08 % el 19 de julio. «Se recuperó» y «regresión de software» atribuyen una causa y una continuidad que estos cuatro registros no establecen. Hay que comparar el mismo corpus, evaluador y entorno e investigar los fallos.

## 4. Hacer legible el gráfico sin colores

El color ayuda, pero un marcador de interrupción también necesita una etiqueta o una forma. La [orientación del W3C sobre el uso del color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) pide otra señal visual cuando el color transmite información. La [orientación sobre contenido no textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content) explica que un gráfico necesita una alternativa textual que conserve su propósito; una tabla puede ofrecer los valores exactos.

Una descripción breve de este ejercicio sería: «Control de calidad histórico del chatbot GA: medición no disponible el 8 de junio; tasas publicadas del 75 % el 15 de junio, 7,69 % el 19 de junio y 98,08 % el 19 de julio. Aquí no se ha establecido la causa del resultado bajo del 19 de junio». Mantenga la tabla junto al gráfico. Quien use un lector de pantalla debe poder consultar fechas, valores y estados sin interpretar colores ni ventanas emergentes.

### Ejercicio práctico

Un punto rojo sin texto marca el 8 de junio. ¿Qué información debe añadirse?

> **Respuesta:** Añada texto visible, como «backend no disponible», y una etiqueta accesible para tecnologías de asistencia. Deje ausente la tasa del 8 de junio. Ofrezca una tabla o descripción equivalente con la fecha y el estado.

## Ideas clave

- Un dato de calidad ausente no es una tasa cero ni una tasa satisfactoria.
- Un valor histórico trasladado conserva su fecha original.
- La disponibilidad de la medición debe mostrarse junto a la calidad medida.
- Una tasa observada baja puede motivar una investigación sin demostrar su causa.
- Las fechas, los denominadores, las revisiones de las fuentes y el texto accesible forman parte de la afirmación.

## Lecturas y pruebas del proyecto

- GA: [resultados históricos del chatbot](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa) e [informe histórico de tendencias](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). El informe tiene fecha y no representa el estado actual.
- W3C: [Comprender el criterio 1.4.1: uso del color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color).
- W3C: [Comprender el criterio 1.1.1: contenido no textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content).

*Investigación: `data-visualization-2026-10-04-001`. Quedan pendientes la revisión temática y la revisión lingüística; este borrador no debe presentarse como un curso verificado.*
