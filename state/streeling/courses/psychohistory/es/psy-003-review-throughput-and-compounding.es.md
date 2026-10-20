---
module_id: psy-003-review-throughput-and-compounding
department: psychohistory
course: "Medir la mejora recursiva a lo largo de la revisión y la publicación"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "psy-002-governance-phase-transitions"]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: psychohistory-2026-10-12-003
version: "0.1.0"
---

# Medir la mejora recursiva a lo largo de la revisión y la publicación

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo distinguirá el trabajo medido de una hipótesis sobre el caudal de salida, calculará dos colas a lo largo de cuatro ciclos semanales y definirá un criterio de refutación para una mejora recursiva propuesta. **Pregunta de proyecto:** si los agentes de Streeling redactan cursos más deprisa, ¿llegará realmente antes el proyecto a tener 25 cursos útiles, revisados y públicos en cada uno de 21 departamentos? La respuesta depende de cada etapa del recorrido, incluidos los veredictos humanos y la relectura pública (volver a leer, de forma anónima, la página publicada para comprobar que muestra la versión prevista de la fuente). Más borradores, por sí solos, no pueden establecerlo.

[PSY-001](psy-001-intro-fractal-compounding.es.md) introduce una analogía de «compuesto fractal». [PSY-002](psy-002-governance-phase-transitions.es.md) interpreta el cambio de gobernanza como una transición de fase, pero califica sus fronteras de régimen de elegidas y no medidas, y advierte de que un cociente de variedad que cruza 1.0 no es por sí mismo una transición de fase. Aquí esa misma disciplina se lleva a la práctica: un bucle de mejora repetido es una *explicación candidata* del aumento del caudal de salida, no una prueba de progreso exponencial. Ni una etiqueta de ley de potencia ni una analogía con un teorema de conservación de la física establecen una tasa de entrega medida.

## 1. Partir de un límite observado

La [instantánea de candidatos a revisión](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/state/streeling/reviews/review-candidates-793e92b.json) fijada registra **21** carpetas de cursos, un objetivo provisional de **525** cursos troncales, **113** códigos troncales distintos, **114** módulos redactados en inglés, porque un curso optativo queda más allá de los 25 primeros códigos de su departamento, **nueve** fuentes con los seis idiomas activos y al menos cinco pares de ejercicio y respuesta detectables, y **cuatro** dossiers de revisión incluidos en commits. El script de informe de progreso registró, en esta misma versión de las fuentes, **cero marcas de revisión de producción aprobadas**. Son observaciones de las fuentes y del triaje, no un recuento de aprendizaje humano ni de páginas publicadas. El [generador](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/scripts/streeling_review_candidates.py) fija cada archivo fuente de la lista a un blob de Git y dice explícitamente que un archivo, una señal de respuesta o un dossier no es una revisión autenticada.

Sobre la base provisional de 21 carpetas, quedan `525 − 113 = 412` códigos troncales. Esa aritmética no significa que haya 113 cursos listos para enseñarse: la exactitud del contenido, la calidad verificable de los ejercicios, el sentido de la traducción, el resultado real de los aprendices, la integración, el despliegue y la relectura anónima son controles distintos. Tampoco explica por qué el repositorio tiene 23 registros de departamento; la [incidencia #1209](https://github.com/GuitarAlchemist/Demerzel/issues/1209) da seguimiento a esa cuestión de alcance, carpetas frente a registros. Use el denominador declarado para cada evaluación, y reconsidérelo si la institución cambia su definición de departamento.

### Ejercicio práctico 1

Calcule los códigos troncales restantes a partir de los recuentos fijados de las fuentes. ¿Por qué puede el inventario mostrar sin faltar a la verdad 114 módulos en inglés, pero solo 113 códigos troncales? ¿Por qué cero marcas de revisión de producción aprobadas no significa cero contenido redactado?

> **Respuesta:** `21 × 25 = 525`; quedan `525 − 113 = 412` códigos troncales. El recuento de módulos redactados incluye un curso optativo cuyo código queda fuera de la secuencia 001–025 de su departamento, así que no aumenta el objetivo de cursos troncales. Las marcas de revisión corresponden a una etapa posterior del pipeline: pueden existir 114 archivos fuente en inglés sin que ninguno tenga registrada una marca de revisión de producción aprobada. Incluso una marca positiva necesitaría una verificación humana del comprobante antes de afirmar públicamente nada sobre la calidad.

## 2. Modelar las colas antes de prometer una tasa

Los [escenarios de entrada](../../../fixtures/psychohistory/psy-003/scenarios.json), el [simulador](../../../../../scripts/streeling_fixtures/psychohistory/psy-003/analyze.py) y el [resultado guardado](../../../fixtures/psychohistory/psy-003/results.json) forman un **fixture didáctico sintético de cuatro semanas** (los datos y el script que acompañan a la lección). Ejecute `python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py --check` en la raíz de Demerzel para reproducirlo; el [README del fixture](../../../fixtures/psychohistory/psy-003/README.md) enumera sus autocomprobaciones. Supone **12 elementos nuevos listos para revisión por semana**, partiendo de colas de revisión y de publicación vacías. Ese supuesto está separado a propósito de los nueve *candidatos de triaje* observados más arriba: ser candidato no hace que un curso esté listo para revisión.

Cada semana, los nuevos elementos listos se añaden a la cola de revisión; se aceptan como máximo tantos como permitan la capacidad de revisión y los elementos disponibles; los elementos aceptados pasan a la cola de publicación; se publican como máximo tantos como permitan la capacidad de publicación y los elementos aceptados disponibles. El modelo supone que toda revisión terminada devuelve `approved` y que todo curso aprobado puede desplegarse. En la práctica, un revisor puede pedir cambios, una revisión lingüística puede quedar pendiente, una compilación puede fallar y una relectura pública puede no coincidir. Por eso, los «aceptados» y los «publicados» del modelo son **cotas superiores optimistas**, no mediciones actuales de Streeling.

```text
reviewed_t  = min(waiting_review_t + new_ready_t, review_capacity_t)
waiting_review_(t+1) = waiting_review_t + new_ready_t - reviewed_t
published_t = min(waiting_publication_t + reviewed_t, publication_capacity_t)
waiting_publication_(t+1) = waiting_publication_t + reviewed_t - published_t
```

Las comprobaciones de conservación son útiles: a lo largo de las cuatro semanas, el total de elementos nuevos listos es igual a los aceptados más la cola de revisión final, y el total de aceptados es igual a los publicados más la cola de publicación final. Si un panel incumple cualquiera de las dos identidades sin un recuento explícito de rechazos o retiradas, la contabilidad por etapas está mal. El modelo **no** codifica los cambios solicitados, el retrabajo ni los distintos tipos de revisión. Harían falta estados propios para ellos antes de que la herramienta pudiera estimar el caudal de salida real.

### Ejercicio práctico 2

En el escenario `flat`, las capacidades semanales de aceptación en revisión y de publicación son ambas de cuatro. Con 12 elementos nuevos listos cada semana y colas iniciales vacías, calcule la cola de revisión al final de cada una de las cuatro semanas, el total de aceptados, el total de publicados y la cola de publicación final.

> **Respuesta:** La cola de revisión crece en ocho por semana: `8, 16, 24, 32`. Cada semana se aceptan, con optimismo, cuatro elementos y se publican cuatro, lo que da 16 aceptados y 16 publicados en total. La cola de publicación final es cero. No es un desempeño observado: la tasa de llegada sintética supera la capacidad de revisión fija.

## 3. Una etapa intermedia más rápida puede desplazar el cuello de botella

El segundo escenario fija las capacidades de aceptación en revisión en `4, 8, 16, 32`, mientras la capacidad de publicación se mantiene en cuatro por semana. Esa duplicación es un **supuesto sobre la capacidad humana y operativa disponible**, no un beneficio gratuito de añadir agentes. Las aceptaciones efectivas son `4, 8, 16, 20`: en la cuarta semana solo hay 20 elementos disponibles, contando las nuevas llegadas, así que una capacidad de 32 queda en parte ociosa. Al cabo de cuatro semanas se han aceptado los 48 elementos nuevos listos, todos hipotéticos, y la cola de revisión está vacía. Solo se han publicado 16; **32 esperan su publicación**. Si la etapa de publicación real exige aprobar el despliegue, compilar el sitio y hacer la relectura, más automatización de la revisión no puede, por sí sola, eliminar esa cola.

Esto es lo esencial de la mejora recursiva, no una promesa sobre su forma. Un mejor verificador de terminología o un mejor paquete para la revisión podrían reducir el tiempo de los revisores. Hay que medir si aumentan los veredictos aceptados de igual calidad, si desplazan el retraso hacia la revisión lingüística o el despliegue, y si las páginas publicadas son realmente correctas. Una herramienta que hace que la etapa intermedia parezca rápida mientras aumenta las correcciones posteriores no ha compuesto una producción útil. El [borrador del comprobante de revisión](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/schemas/streeling-review-receipt.schema.json) distinguiría los veredictos de fondo, de idioma y de aprendices por blob exacto de la fuente, pero sigue en una *pull request* (solicitud de integración) en borrador, a la espera de que una persona revise el esquema.

### Ejercicio práctico 3

Use el escenario `growing_review_fixed_publication`. Indique las aceptaciones efectivas por semana, los totales finales de aceptados y de publicados, y las dos colas finales. ¿Por qué no se usa por completo la capacidad de 32 de la cuarta semana?

> **Respuesta:** Las aceptaciones efectivas son `4, 8, 16, 20`. Los totales son 48 aceptados y 16 publicados. La cola de revisión es cero y la cola de publicación contiene 32. En la cuarta semana esperaban ocho elementos y llegaron 12 nuevos, así que solo pudieron aceptarse 20; la capacidad restante de 12 no tuvo entrada. El escenario no demuestra que personas reales pudieran aprobar a estos ritmos, ni que fueran a hacerlo.

## 4. Poner a prueba una mejora recursiva en todo el recorrido

Para poner a prueba un cambio real, registre una ventana de referencia y la intervención: qué herramienta o práctica cambió, quién la usó, qué cursos y qué blobs exactos de la fuente entraron en cada cola, cuándo entraron y salieron, y por qué se rechazaron o devolvieron elementos. Siga al menos cuatro producciones semanales distintas: borradores nuevos con cinco ejercicios respondidos, veredictos **humanos** de fondo o de idioma completados, fusiones o despliegues aceptados, y páginas públicas releídas de forma anónima en la versión prevista de la fuente. Siga también la tasa de retrabajo y el tiempo de los revisores. Mantenga fijo el denominador o informe de un cambio de alcance. Compare cohortes de complejidad de curso y requisitos lingüísticos parecidos; si no, una cohorte fácil puede crear una mejora falsa.

Una regla propuesta de **contrapresión semántica** (*semantic backpressure*) puede dirigir el escaso esfuerzo de los agentes hacia la reparación de la evidencia cuando una etapa posterior está sobrecargada. Por ejemplo, una cola de revisión grande puede justificar mejorar los paquetes para los revisores, la paridad de las traducciones o la claridad de las respuestas. Una cola de publicación grande puede justificar comprobar el despliegue, la fijación de las fuentes y la relectura. Es una hipótesis de asignación, no un planificador implementado en Streeling ni un motivo para abandonar los 412 cursos troncales restantes. Si la regla aumenta el tiempo de espera sin aumentar los cursos aceptados, públicos y utilizables por los aprendices, recházela o modifíquela. Un control humano no puede autoaprobarlo un modelo más rápido.

Defina un criterio de refutación *antes* de la intervención. Un piloto razonable podría exigir un aumento sostenido de los cursos semanales con veredictos humanos autenticados **y** relectura pública, sin aumento de la tasa de correcciones ni de los fallos de aprendices sin resolver. Si solo aumentan los borradores redactados, o solo la confianza de un modelo, la intervención no ha demostrado un progreso de principio a fin. Si las páginas publicadas aumentan mientras la evidencia o la calidad bajan, la ganancia aparente no es el objetivo. Cuatro semanas de la tabla sintética no pueden sustituir a un piloto así.

### Ejercicio práctico 4

Un equipo informa de que su nuevo flujo de trabajo con agentes elevó los borradores de 12 a 24 por semana, mientras que las aprobaciones humanas verificadas siguen en cuatro y las relecturas públicas siguen en cuatro. Nombre un indicador adelantado que mejoró, un indicador de resultado que no mejoró y un criterio de refutación para la afirmación de que el flujo de trabajo aceleró la entrega.

> **Respuesta:** La creación de borradores mejoró de 12 a 24 por semana. Las relecturas públicas verificadas, un resultado más cercano al objetivo pedido, se quedaron en cuatro; las aprobaciones humanas también se quedaron en cuatro. Un criterio de refutación declarado de antemano: que cohortes comparables no muestren, tras el cambio, ningún aumento sostenido de las aprobaciones autenticadas y de las relecturas públicas correctas, o que aumenten el retrabajo o los fallos de aprendices. Una cola de borradores más grande no demuestra, por sí sola, una aceleración de la entrega.

### Ejercicio práctico 5

El escenario sintético de revisión creciente termina con 32 elementos a la espera de publicación. Un agente propone volver a duplicar la redacción de cursos y llamar al resultado «progreso exponencial de Streeling». ¿Qué trabajo debería inspeccionar primero el equipo, qué identidad de la fuente debe preservarse y qué contaría como una mejora real?

> **Respuesta:** Inspeccionar por qué esperan los elementos aceptados: la entrada de la generación del sitio, los controles de compilación y de lanzamiento, la capacidad de despliegue y la relectura anónima. Preservar el commit y el blob de Git exactos de la fuente de cada curso aceptado a lo largo de la página generada y de la verificación pública; no dejar que una edición posterior herede un veredicto antiguo. Una mejora real elevaría la tasa de cursos revisados correctamente y releídos públicamente sin ocultar problemas de calidad ni de retrabajo. Seguir redactando cursos de forma independiente puede seguir siendo útil, pero duplicar los borradores no resuelve esta cola de publicación.

## Fuentes, límites y próxima comprobación

La referencia observada consiste en la [instantánea de candidatos a revisión ligada a un commit](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/state/streeling/reviews/review-candidates-793e92b.json) y el [script de informe de progreso de las fuentes](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/scripts/streeling_course_progress.py). Los resultados numéricos de las cuatro semanas los calcula el [script del fixture](../../../../../scripts/streeling_fixtures/psychohistory/psy-003/analyze.py); no se midieron en una intervención. El modelo supone revisiones y publicaciones inmediatas y satisfactorias, y omite el retrabajo y la dificultad variable de los cursos. No se realizó ningún experimento operativo de cuatro semanas, ninguna revisión humana de esta lección ni de sus traducciones al francés y al español, ningún intento de un aprendiz ni ninguna relectura pública. La próxima comprobación es un piloto real acotado, con comprobantes de la fuente exacta, cohortes de cursos comparables y un recuento explícito de relecturas públicas.
