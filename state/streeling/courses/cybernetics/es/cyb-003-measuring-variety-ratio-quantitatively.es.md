---
module_id: cyb-003-measuring-variety-ratio-quantitatively
department: cybernetics
course: Medir la variedad requerida sin inventar capacidad
level: intermediate
prerequisites: [cyb-001-vsm-ai-governance-mapping, cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: cybernetics-2026-10-21-003
version: "0.2.0"
---

# Medir la variedad requerida sin inventar capacidad

> **Departamento de cibernética** | Nivel: intermedio | Duración: 35 minutos | Estado: pendientes las revisiones temática, de aprendizaje y lingüística

## Objetivos

Después de esta lección podrás:

- distinguir las etiquetas posibles de un esquema, los estados observados en una muestra y las respuestas reguladoras eficaces;
- calcular la variedad máxima de un alfabeto finito y la entropía empírica de una muestra sin confundirlas con la calidad de la gobernanza;
- explicar por qué los números de políticas, personas y producciones gramaticales no forman un «cociente de variedad» significativo;
- diseñar para Demerzel un experimento que empareje perturbación, respuesta y resultado.

## La pregunta del proyecto

La primera versión de CYB-003 comunicó cocientes conductuales y regulatorios «saludables» y una «brecha regulatoria de 3 bits» sumando logaritmos de cantidades de archivos, umbrales e interacciones supuestas entre políticas. Esos números no contaban perturbaciones distinguibles ni respuestas eficaces bajo una tarea definida. Las franjas consideradas saludables carecían de base en resultados medidos. **Se retiran esas conclusiones.** Los cálculos siguientes usan registros reales del proyecto, pero no afirman medir su capacidad operativa.

El ejemplo está fijado en la revisión de Demerzel [66083fc](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f). Consulta el [esquema de producción de cursos](https://github.com/GuitarAlchemist/Demerzel/blob/66083fc684b57a12ef307c19c3819d91c551295f/schemas/course-production.schema.json) y los [ocho registros](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f/state/streeling/course-productions). El [script de reproducción](../../../fixtures/cybernetics/cyb-003/README.md) comprueba las cifras en una copia de trabajo que contiene esa revisión. Esta instantánea histórica no describe el estado actual del proceso.

## 1. Definir el conjunto antes de contar

La variedad de Ashby trata los estados distinguibles de un **conjunto especificado**. Si sus N estados son posibles, su variedad máxima es log2(N) bits. Importan tanto el conjunto elegido como las distinciones que pueden observarse. Un esquema enumera *símbolos permitidos*; no dice con qué frecuencia aparecen, si todas las combinaciones son posibles ni si un controlador puede manejar una perturbación. El [texto original de Ashby](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf) distingue estados posibles, estados observados y regulación.

En la revisión fijada, el esquema permite cinco valores de status: in_progress, review_pending, published, rejected y failed. También permite tres valores de review.verdict: approved, revise y reject. El veredicto es opcional en el esquema y no aparece en ninguno de los ocho registros examinados. Siete registros tienen el estado in_progress y uno tiene review_pending.

| Pregunta | Respuesta de la fuente fijada | Lo que **no** demuestra |
|---|---:|---|
| ¿Cuántas etiquetas de estado están configuradas? | 5 | Cinco conductas ejercidas |
| ¿Cuántas etiquetas de estado aparecen en la muestra? | 2 | Todo el rango operativo |
| ¿Cuántos registros se examinaron? | 8 | Una serie temporal representativa |
| ¿Cuántos contienen un veredicto de revisión? | 0 | La capacidad o calidad de los revisores |

### Ejercicio práctico 1

Calcula la variedad máxima del alfabeto de estados configurado y la de las dos etiquetas de estado observadas. ¿Puede llamarse capacidad reguladora de Demerzel a alguno de los dos números?

> **Respuesta:** log2(5) ≈ 2,322 bits para el alfabeto configurado; log2(2) = 1 bit para las dos etiquetas observadas. Ninguno mide la capacidad reguladora: cuentan etiquetas, no respuestas distintas y eficaces ante perturbaciones especificadas.

## 2. La distribución de una muestra responde a otra pregunta

La entropía de Shannon de la distribución de símbolos de una muestra es H = -Σ p(x) log2 p(x). En los ocho registros fijados, las frecuencias de estado son 7/8 y 1/8, así que H ≈ 0,544 bits por estado muestreado. Es una estadística descriptiva de este conjunto pequeño y seleccionado de registros de producción, no una estimación de la conducta futura de los agentes. La fórmula procede del [artículo original de Shannon](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).

El alfabeto configurado, el alfabeto observado y la entropía empírica son mediciones diferentes. No sumes la variedad de «cinco estados» y la de «tres veredictos»: puede faltar el veredicto, las fases restringen las combinaciones plausibles y no se ha demostrado independencia. El cálculo log2(5 × 3) ≈ 3,907 describe solo un conjunto hipotético de **15 pares de etiquetas sin valores ausentes**. Si se cuenta «veredicto ausente» como cuarto símbolo, el producto cartesiano sin restricciones contiene 20 pares. Ninguna cifra establece qué combinaciones son alcanzables o útiles.

### Ejercicio práctico 2

Vuelve a calcular la entropía empírica a partir de la tabla y explica por qué log2(8) = 3 bits no responde a la pregunta.

> **Respuesta:** -(7/8)log2(7/8) -(1/8)log2(1/8) ≈ 0,544 bits. Ocho es el número de registros, no el número de estados distintos. log2(8) mediría la capacidad de identificar uno de ocho registros si su identidad fuera la variable definida: esa es otra pregunta.

### Ejercicio práctico 3

Un panel multiplica cinco estados por tres veredictos de revisión, llama al resultado «15 respuestas del regulador» y presenta 3,907 bits como prueba de gobernanza adecuada. Identifica dos pasos sin fundamento.

> **Respuesta:** Supone que todas las combinaciones estado/veredicto son válidas y alcanzables, aunque el veredicto sea opcional y las fases impongan restricciones. También sustituye las respuestas comprobadas ante perturbaciones por símbolos del esquema: no se midió ninguna perturbación, acción elegida o resultado.

## 3. Medir una tarea real de regulación

Para probar la variedad requerida hay que definir la **perturbación** (qué salió mal), la **respuesta** (qué hizo el controlador) y un **resultado esencial** (qué debe mantenerse dentro de límites). Para la producción de cursos, una prueba propuesta podría presentar tres fallos distintos: una fixture ausente, una fuente de pruebas ilegible y una respuesta de ejercicio incompatible con su fixture. El sistema podría reparar la fixture, solicitar acceso o corregir la respuesta, y después emitir un recibo. Son **casos de prueba propuestos**, no observaciones del comportamiento actual de Demerzel.

Antes de ejecutar la prueba, registra la fixture de entrada, la distinción esperada, la acción permitida, el límite de tiempo y la regla de aprobación. Ejecuta cada caso y conserva la decisión y el resultado. Una respuesta genérica de «reintentar» para los tres casos revela que falta una distinción, aunque el controlador tenga muchos archivos de políticas. A la inversa, tres etiquetas diferentes no ayudan si todas producen el mismo artefacto defectuoso. Cuenta las *distinciones eficaces para la tarea*, no los sustantivos del repositorio.

| Perturbación propuesta | Prueba que la distingue | Respuesta posible | Resultado comprobable |
|---|---|---|---|
| Fixture ausente | La ruta declarada no existe | Reparar o bloquear indicando la ruta exacta | El recibo identifica la fixture ausente; ningún resultado inventado |
| Fuente ilegible | Falla el intento de lectura | Pedir acceso o usar una fuente expresamente permitida | El recibo indica la lectura fallida y su alcance |
| Respuesta incoherente | El cálculo reproducido difiere | Corregir la respuesta y repetir el ejercicio | La nueva respuesta concuerda con la fixture fijada |

Esta tabla es un diseño experimental. No puede establecer un cociente respuestas/perturbaciones sin ejecuciones emparejadas con resultados. Incluso entonces, un cociente de entropías ignoraría qué respuesta funciona para cada perturbación. Presenta la matriz de confusión y el éxito de la tarea junto con cualquier medida de información.

**Una cota condicional de Ashby.** La gramática revisada del proyecto expresa una cota sobre los *resultados*, no sobre cantidades de archivos de políticas. En un ciclo donde cada perturbación recibe una respuesta y ninguna respuesta lleva dos perturbaciones distintas al mismo resultado, el grupo de respuesta más grande contiene al menos N_D/N_R perturbaciones con resultados distintos. Por tanto, N_O ≥ N_D/N_R, o V_O ≥ V_D - V_R para recuentos positivos. Si una misma respuesta lleva varias perturbaciones a un mismo resultado aceptable, esta deducción no se aplica: cuatro perturbaciones pueden compartir una respuesta y un resultado. Ninguno de los dos casos demuestra que los resultados observados sean aceptables. Registra cada perturbación, respuesta y resultado esencial antes de aplicar la cota; la fixture de etiquetas del esquema anterior no contiene esas observaciones.

### Ejercicio práctico 4

Un agente encuentra una fuente ilegible, pero escribe «revisión aprobada» tras omitirla sin avisar. ¿Qué campos debe mostrar el recibo de reproducción? ¿Es una regulación exitosa?

> **Respuesta:** Registra la fuente declarada y su revisión, el intento de lectura, el error, la alternativa si está autorizada, la acción elegida y el resultado final. Sin la prueba, la aprobación carece de fundamento; el resultado seguro es un bloqueo o una revisión pendiente, no el éxito.

### Ejercicio práctico 5

Diseña una forma de refutar la afirmación «añadir una cuarta política de gobernanza mejoró la regulación de la revisión de cursos».

> **Respuesta:** Mantén fijas las fixtures de perturbación y la regla de aprobación; compara las decisiones de revisión y los resultados comprobados independientemente antes y después de la política. Si la nueva política no reduce las aprobaciones sin fundamento o los casos sin resolver, o los aumenta, esta prueba no respalda la mejora. Mide también el tiempo de preparación y revisión: más texto de política puede añadir coste sin mejorar las decisiones.

## 4. Qué informar después

Un panel útil mostraría por separado el alfabeto de estados configurado, las frecuencias de estados observados, los veredictos ausentes y los resultados de perturbaciones emparejadas. Mostraría también la revisión del repositorio y la selección de la muestra. No afirmaría intervalos «saludables» para un cociente que no se haya validado contra resultados de gobernanza o de usuarios. Para probar una mejora recurrente, repite el mismo conjunto de perturbaciones entre revisiones y sigue el éxito comprobado independientemente, los casos sin resolver y el esfuerzo total. Un ciclo más corto solo es mejor si produce más decisiones correctas sin trasladar trabajo a una cola de revisión invisible.

Esto se relaciona también con [el ciclo controlado de audio agentico de CS-004](../../../fixtures/computer-science/cs-004/recursive-improvement-evidence.json): fallos de lectura de fuentes y un comparador insensible se convirtieron en cambios explícitos del harness y de la evaluación. Esos pocos ciclos observados respaldan un aprendizaje local, no una afirmación de progreso exponencial.

## Fuentes y límites

- [Esquema de producción de cursos de Demerzel](https://github.com/GuitarAlchemist/Demerzel/blob/66083fc684b57a12ef307c19c3819d91c551295f/schemas/course-production.schema.json) y [registros fijados](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f/state/streeling/course-productions); las cifras se comprueban mediante la [fixture local de reproducción](../../../fixtures/cybernetics/cyb-003/README.md).
- W. Ross Ashby, [*An Introduction to Cybernetics*](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf), capítulos 7 y 11; C. E. Shannon, [*A Mathematical Theory of Communication*](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).
- Los ocho registros forman una muestra histórica seleccionada. No había un registro que emparejara perturbaciones, respuestas y resultados, ni un intento de los ejercicios por parte de un estudiante. Siguen pendientes las revisiones temática y lingüística.
