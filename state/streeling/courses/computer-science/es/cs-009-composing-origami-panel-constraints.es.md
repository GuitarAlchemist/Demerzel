---
module_id: cs-009-composing-origami-panel-constraints
department: computer-science
course: "Componer las restricciones de origami antes de aceptar un apilamiento rígido"
level: intermediate
prerequisites: [cs-001-thinking-algorithmically, cs-006-ixql-pipeline-composition]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-21-009
version: "0.1.0"
---

# Componer las restricciones de origami antes de aceptar un apilamiento rígido

> **Departamento de Informática** | Nivel intermedio | 40 minutos | Borrador en español; revisión de contenido y evaluación con un estudiante pendientes

## Objetivos y pregunta para el proyecto

Convertirás las uniones planas en clases de equivalencia, conservarás las restricciones dirigidas entre esas clases, distinguirás las pruebas locales de solapamiento de una restricción global de apilamiento e interpretarás un resultado incompleto sin inventar una colocación. La pregunta práctica es: **¿qué resultado puede transmitir un agente a un futuro adaptador de Blender o Godot después de que IX haya comprobado un estado de origami?** Una representación visual de un objeto artesanal exige una interpretación explícita del análisis, porque superar una comprobación puede coexistir con un rechazo bajo otro modelo.

El caso de estudio es el [módulo de espesor de IX](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) y sus [pruebas de integración](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), ambos fijados a `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. El módulo lee un espesor de material expresado en las unidades de coordenadas del patrón de pliegues. Examina un estado dado plegado en plano; no planifica el movimiento de plegado ni exporta una escena. El [conjunto de datos del curso](../../../fixtures/computer-science/cs-009/README.md) contiene pequeñas derivaciones con grafos, claramente separadas de los resultados reales de las pruebas de Rust.

## 1. Agrupar primero las caras en paneles

Una cara es un polígono de la descripción del estado plegado. En este modelo, un panel es un conjunto de caras conectadas por uniones planas que deben mantener una misma altura. La función `panels` de la implementación une sus conjuntos y asigna a cada cara la cara de menor índice de su componente conexa. Ese representante es una etiqueta algorítmica. No es un identificador permanente de objeto: renumerar la entrada puede cambiarlo sin alterar el panel representado.

Considera las caras 0, 1 y 2. Las caras 0 y 1 comparten una unión plana. Las relaciones dadas sitúan 2 encima de 0 y 1 encima de 2. En el grafo de caras, los arcos de abajo hacia arriba son `0 → 2 → 1`, sin ningún ciclo. Si asignamos a cada cara su propia altura, la respuesta aparente es los niveles 0, 1 y 2. Esto incumple el modelo: las caras 0 y 1 pertenecen al mismo panel rígido y no pueden tener alturas diferentes.

Tras unir las caras conectadas en plano, la correspondencia de paneles es `[0, 0, 2]`. Las dos restricciones se convierten en `panel 0 → panel 2` y `panel 2 → panel 0`. El ciclo se hace visible. Esta es una construcción por cociente: primero se agrupan los objetos que deben moverse juntos y después se aplican las restricciones de orden a esos grupos. Comprobar cada parte antes de componerlas pasa por alto el requisito que introduce su identidad compartida.

### Ejercicio 1: corregir el grafo engañoso

Utiliza el caso `pierced-flat-joint` del conjunto de datos. Indica los representantes de los paneles y los dos arcos entre paneles. Explica por qué el orden topológico del grafo de caras no puede justificar una colocación rígida. ¿Qué decisión adicional de implementación sería necesaria si un adaptador quisiera un identificador permanente de panel?

> **Respuesta:** Los representantes son `[0, 0, 2]`; los arcos son `0 → 2` y `2 → 0`. El orden de las caras permite dos alturas distintas para el mismo panel conectado en plano, por lo que resuelve el sistema de restricciones equivocado. Un identificador permanente de panel necesitaría una correspondencia declarada con la identidad del material o de la fuente que se mantuviera entre ediciones o permutaciones. El representante de menor índice, por sí solo, no ofrece esa garantía.

## 2. Un éxito local puede coexistir con un rechazo global

La prueba fijada `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` construye cuatro tiras. Cada una se solapa con la siguiente en una esquina diferente. Todas las celdas locales de la superposición pueden tener un orden coherente; sin embargo, las afirmaciones combinadas dicen que la tira 0 está encima de 1, 1 encima de 2, 2 encima de 3 y 3 encima de 0. Los arcos de abajo hacia arriba dan `0 → 3 → 2 → 1 → 0`. Ninguna altura única por tira satisface las cuatro desigualdades para un espesor positivo del material.

Esto es distinto de [VC-007](../../visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), cuyo verificador sintético detecta un reinicio de la paridad en los bordes de teselas repetidas. Aquí el problema es un ciclo que atraviesa distintas regiones de solapamiento en la implementación existente de IX. Una textura, una vista previa de un cruce local o un análisis básico de origami satisfactorio no resuelven la cuestión global de los paneles paralelos.

La prueba comprueba que `analyse(&weave()).unwrap().ok` es verdadero. También comprueba la lectura opcional del espesor para `t = 0`, un `t` positivo muy pequeño y `t = 0.5`. El grafo sigue siendo cíclico, pero `rigid.refused` solo es verdadero para un `t` positivo. En cero, la implementación sigue devolviendo `levels`, `height` y `face_levels` como ausentes para esta lectura cíclica. No sustituyas una altura rígida ausente por cero solo porque el valor separado `ply_height` sea cero.

### Ejercicio 2: interpretar el caso cero

El entrelazado tiene `ply = 2` y un orden cíclico de paneles. ¿Cuáles son los valores de `ply_height` y `rigid.refused` para `t = 0` y `t = 0.5`? ¿Alguno de los resultados proporciona una asignación de niveles a las caras rígidas?

> **Respuesta:** En cero, `ply_height = 0` y `rigid.refused = false`; en 0.5, `ply_height = 1` y el rechazo es verdadero. Ambos informes cíclicos carecen de niveles rígidos, altura rígida y asignación de niveles a las caras. La ausencia de rechazo con espesor cero no proporciona el testigo que falta, y el rechazo con espesor positivo corresponde a este modelo de paneles paralelos.

## 3. Las restricciones acíclicas permiten calcular el camino más largo

Cuando el grafo de paneles admite un orden topológico, la implementación inicializa todos los niveles en cero. Para cada arista dirigida de un panel inferior `u` a un panel superior `v`, actualiza `level[v] = max(level[v], level[u] + 1)`. Procesar en orden topológico garantiza que el nivel de cada predecesor esté disponible. El nivel más alto, cuya numeración empieza en cero, más uno da la longitud de la cadena en paneles. Multiplicar por el espesor total `t` da la altura del apilamiento para un orden completamente determinado.

El valor `face_levels` indicado es un testigo producido por esta recurrencia. Pueden existir otros apilamientos válidos; los valores por cara no constituyen un etiquetado canónico de todos los apilamientos admisibles.

El DAG sintético del conjunto de datos tiene los arcos `P → R`, `Q → R` y `R → S`. P y Q pueden compartir el nivel cero porque el ejemplo no aporta ninguna relación que exija separarlos; R debe estar por encima de ambos y S por encima de R. Son datos abstractos de un grafo, no una geometría FOLD exportada ni una afirmación sobre el solapamiento espacial. Su propósito es practicar la recurrencia antes de leer la prueba, más extensa, de la grulla.

### Ejercicio 3: calcular la cadena

Asigna los cuatro niveles del DAG sintético, cuenta los paneles de la cadena más larga y calcula la altura para `t = 0.2`. ¿Por qué informar solo del nivel más alto produciría un error de desfase de uno? Como comparación, ¿qué dos cantidades distingue la prueba real de la grulla?

> **Respuesta:** P y Q están en 0, R en 1 y S en 2. La cadena tiene tres paneles, por lo que la altura es `3 × 0.2 = 0.6` en unidades del patrón de pliegues. El índice máximo 2 omite un nivel ocupado. La prueba real de la grulla distingue un máximo local de 28 capas de hoja de los 36 niveles de paneles paralelos necesarios; la ocupación local y una cadena que atraviesa regiones responden a preguntas diferentes.

## 4. El orden que falta forma parte del resultado

La implementación cuenta los pares de caras solapadas de distintos paneles cuyo orden no se ha indicado. Si existe algún par así, `levels_exact` es falso. Informa de `max(chain, ply)` como cota inferior y no proporciona `face_levels`. Unas restricciones dadas acíclicas no bastan para certificar que una colocación propuesta respete una relación que la entrada nunca especificó.

La prueba fijada `an_unstated_overlap_gives_a_lower_bound` utiliza dos hojas solapadas sin un orden indicado. Espera un par indeterminado, dos niveles como cota inferior y ninguna asignación de niveles a las caras. Quien invoque el módulo debe conservar el indicador de exactitud junto con el número. Si el resumen de un agente lo omite, una etapa posterior puede convertir una cota inferior en una disposición supuestamente completa sin que nadie tome esa decisión de forma explícita.

### Ejercicio 4: conservar la incertidumbre en una transferencia

La ficha sintética de orden incompleto tiene una cadena de 2, un `ply` de 3, un par indeterminado y `t = 0.2`. ¿Qué altura numérica puede indicar el algoritmo y cómo debe describirse? ¿Puede un adaptador de escenas usarla para colocar todas las caras?

> **Respuesta:** Indica `max(2, 3) = 3` niveles y una cota inferior de altura de 0.6, con `levels_exact = false` y `face_levels = null`. No puede proporcionar una colocación completa. Una transferencia debe conservar la etiqueta de cota inferior, el número de pares sin orden, la identidad de la fuente y la ausencia de testigo, sin prometer coordenadas derivadas de un orden no observado.

## 5. Convertir el resultado en una decisión verificable

Una composición agéntica puede transportar juntos el análisis básico y la lectura rígida. La [decisión de diseño fijada](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/docs/adr/0007-origami-thickness-as-parallel-rigid-panels.md) mantiene explícitamente la lectura del espesor junto al veredicto básico. Un rechazo significa que no existe un apilamiento bajo los supuestos de paneles rígidos paralelos. No demuestra que un objeto material sea imposible con paneles inclinados, pliegues modificados u otros métodos de construcción. A la inversa, la ausencia de rechazo no demuestra la viabilidad de fabricación.

Para una prueba propuesta en Godot, conserva la revisión del FOLD de origen, la conversión del espesor total y de las unidades, los dos resultados del análisis, cualquier testigo de ciclo, la exactitud y la correspondencia entre caras y objetos. Asigna al observador una tarea concreta, como encontrar la relación responsable de un rechazo. Compara su respuesta con la obtenida mediante un diagrama sencillo del grafo para la misma tarea. Se trata de un experimento de transferencia propuesto; el curso no registra ningún renderizador, exportación, prueba con estudiantes ni mejora de rendimiento. Un nuevo DSL solo justificaría su coste si mejorara esa tarea frente a un informe tipado más sencillo y al verificador existente.

### Ejercicio 5: decidir qué enviar a las etapas posteriores

Un futuro agente informa: «análisis básico superado; rechazo rígido con espesor positivo; caras del ciclo `[0,3], [3,2], [2,1], [1,0]`». Propone etiquetar el objeto como «físicamente imposible» y omitir el ciclo porque la escena parece plausible. Escribe una formulación corregida dirigida al usuario e identifica las pruebas necesarias para una demostración en una escena.

> **Respuesta:** «El estado dado superó las comprobaciones básicas, pero el orden indicado contiene un ciclo que impide un apilamiento de paneles rígidos paralelos con este espesor positivo». Conserva el ciclo y los supuestos. Una demostración en una escena necesita una importación vinculada a la fuente, una correspondencia entre caras y objetos, una visualización del ciclo verificable de forma independiente y una tarea de observación registrada. Una captura de pantalla por sí sola no puede demostrar el resultado del grafo, la imposibilidad física ni un beneficio para el aprendizaje.

## Repetición de las pruebas y límites

Ejecuta `cargo test -p ix-origami --test thickness` en IX en la revisión fijada. El coordinador volvió a ejecutar las 11 pruebas de integración de espesor el 2026-10-21: 11 superadas, 0 fallidas. El README del conjunto de datos registra los blobs de la fuente y de las pruebas. Las fichas de grafos son datos didácticos derivados a mano; no se introduce ningún analizador adicional ni runtime consumidor. Superar esas pruebas respalda los casos descritos de la implementación; la exactitud del contenido, la calidad idiomática de las traducciones, el éxito de los estudiantes, la importación de escenas y la verificación anónima de la publicación en Learn siguen siendo trabajos distintos.
