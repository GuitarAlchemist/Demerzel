---
module_id: sem-004-face-identity-under-reindexing
department: semiotics
course: "Identidad de las caras tras la reindexación"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-21-004
version: "0.1.0"
---

# Identidad de las caras tras la reindexación

> **Departamento de Semiótica** | Nivel intermedio | 40 minutos | Traducción provisional, sin revisión lingüística

## Objetivos y decisión del proyecto

Un futuro visor de escenas selecciona la cara 1 de un modelo de origami. Otro agente renumera el modelo y comunica que la cara 1 ha cambiado de nivel. ¿Se ha movido el material, ha cambiado el orden o el mismo número designa ahora otra cara? Para responder hay que interpretar el número antes de interpretar la geometría.

Al terminar esta lección podrás trasladar una selección mediante una permutación explícita, invertir la correspondencia, distinguir identidad, nivel y orientación, y redactar un informe verificable entre agentes. Dedica ocho minutos al problema y los signos, doce a la tabla, diez a las transformaciones y diez a los ejercicios y la transferencia. El producto es una tabla de correspondencias y un informe justificado, sin desarrollar un nuevo servicio de identidad.

Las fuentes del proyecto están fijadas al commit de IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), [pruebas de espesor](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) y [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). Los enlaces describen esa versión inspeccionada, sin garantizar el estado actual de la rama. IX aporta verificaciones y transformaciones de control. Esta lección no demuestra exportación a Blender, importación en Godot, renderizado ni un mecanismo persistente de selección.

## 1. El número de una cara es un signo contextual

En semiótica, un signo representa un objeto bajo una interpretación. Aquí `1` es el signo; una cara material concreta es el objeto deseado; y «consultar la posición 1 de esta revisión del modelo» es la interpretación. Un **índice de matriz** es una dirección dentro de una colección ordenada. Debe distinguirse del término semiótico *índice*, un signo conectado con aquello que indica. Ninguno de los dos sentidos otorga identidad permanente al número.

Un informe necesita la revisión del modelo o el contexto de transformación. La cara 1 de entrada y la cara 1 de salida pueden ser referencias distintas. La forma, el color y el nivel actual ayudan a reconocer una cara, pero varias caras pueden compartir esas propiedades o cambiarlas durante una transformación. Por sí solas no establecen procedencia.

En esta lección, **identidad material** significa correspondencia con la misma cara de entrada a través de la transformación controlada que estamos estudiando. No resuelve remallados arbitrarios, divisiones, fusiones ni reconstrucciones a partir de imágenes. Una etiqueta didáctica como A conserva la correspondencia que proporcionamos. Estas etiquetas son explícitamente sintéticas: `Permutation` de IX describe una transformación, sin constituir un registro universal de identificadores persistentes.

### Ejercicio 1 — Reparar una referencia

Un agente escribe: «La cara 1 está mal después de renumerar». ¿Qué información falta? Reformula la frase como una pregunta verificable.

> **Respuesta:** Faltan el contexto de los modelos de entrada y salida, la correspondencia y la propiedad comparada. Una pregunta útil sería: «Para la cara sintética de entrada 1 (B), utilizando el mapa antiguo-a-nuevo `[2,0,3,1]`, ¿conserva la cara de salida 0 el nivel de entrada 2?». Esto identifica el material y la comparación sin afirmar que existe un defecto de IX.

## 2. Respetar la dirección declarada del mapa

`Permutation` documenta adónde fue cada índice **antiguo**. La función `place` escribe el elemento antiguo en `out[perm[old]]`. Por tanto, `perm.faces[f]` recibe un índice de cara de entrada y devuelve su índice de salida. Para saber qué cara de entrada ocupa una posición de salida determinada hace falta la inversa.

Este ejemplo de cuatro caras es explícitamente **sintético** y también está en la [fixture](../../../fixtures/semiotics/sem-004/scenarios.json). Sus números no son resultados de la grulla, una semilla muestreada de IX ni un experimento físico de espesor.

| Índice de entrada | Etiqueta didáctica de procedencia | Nivel de entrada | Índice de salida `p[old]` |
|---:|---|---:|---:|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 0 |
| 2 | C | 1 | 3 |
| 3 | D | 3 | 1 |

El mapa directo es `p = [2,0,3,1]`. Al recorrer las posiciones de salida 0 a 3 obtenemos las etiquetas `[B,D,A,C]` y los niveles `[2,3,0,1]`. La inversa es `q = [1,3,0,2]`: la salida 0 procede de la entrada 1 y la salida 1 procede de la entrada 3. Se comprueban ambas direcciones: `q[p[f]] = f` y `p[q[j]] = j`.

La comparación correcta es `new[p[f]] == old[f]`. Para B es `new[0] == old[1]`, por lo que `2 == 2`. La comparación directa de las matrices devuelve desigualdad aunque cada material conserva su valor. Reutilizar el entero seleccionado 1 señalaría D, cuyo nivel es 3. Puede haber un error de selección sin corrupción del cálculo de niveles.

La inversa también interpreta un clic en la salida 3: identifica C, situada en la entrada 2. Escribir `new[q[f]]` en la comparación directa mezcla dominios. Con nuestro mapa, deliberadamente distinto de su inversa, la entrada 0 compararía `new[1] = 3` con `old[0] = 0`. Un ejemplo basado solo en un intercambio puede ocultar este fallo porque un intercambio es su propia inversa.

### Ejercicio 2 — Trasladar la selección

Traslada la selección C desde la entrada. Después averigua el origen de un clic en la salida 1. ¿Conservar el entero 2 mantendría la selección C?

> **Respuesta:** C está en la entrada 2, por lo que su salida es `p[2] = 3`, conservando el nivel 1. La salida 1 procede de `q[1] = 3`, etiqueta D. Conservar el entero 2 seleccionaría A en la salida. Cambia la dirección mientras se conserva la correspondencia material estipulada.

### Ejercicio 3 — Comparar los objetos correctos

Encuentra la primera diferencia directa entre `[0,2,1,3]` y `[2,3,0,1]`. Indica las cuatro comparaciones con correspondencia y comprueba una ecuación de la inversa.

> **Respuesta:** La posición directa 0 difiere: `0 != 2`. Las comparaciones correctas son `new[2]=0`, `new[0]=2`, `new[3]=1` y `new[1]=3`, que coinciden respectivamente con las entradas 0–3. Por ejemplo, `q[p[2]] = q[3] = 2`. La desigualdad directa no refuta la correspondencia afirmada.

## 3. Conservar las relaciones e interpretar sus signos

La renumeración también cambia las referencias a vértices y aristas. Rota cíclicamente la lista de vértices de cada cara conservando el sentido de recorrido; puede intercambiar los extremos de una arista; y mezcla la secuencia de entradas de `faceOrders`. Son operaciones distintas. Rotar un contorno triangular de `[0,1,2]` a `[1,2,0]` cambia el punto inicial. Invertirlo a `[0,2,1]` cambia el sentido de recorrido. Estas pequeñas listas ilustran convenciones de orden; no son geometría extraída de IX.

En cada triple `[f,g,s]` de `faceOrders`, `renumber` sustituye `[p[f],p[g],s]` y mantiene el signo. Nuestro triple sintético `[1,3,1]` pasa a `[0,1,1]`. El signo se interpreta respecto a las normales de las caras; no basta para asignar una etiqueta global «encima» sin considerar la orientación. Cambiar la secuencia de la colección de relaciones tampoco invierte cada relación. Posición en una lista, posición de un extremo, dirección del contorno y signo de orden expresan cosas diferentes.

La prueba fijada `controls_leave_the_stack_unchanged` renumera la grulla con las semillas 1–5. Comprueba `ply` 28, 36 niveles rígidos y, para cada cara de entrada, `new[perm.faces[f]] == old[f]`. Es evidencia concreta para esos controles sobre esa fixture, sin demostrar un teorema exhaustivo para todo pliegue o transformación.

`face_levels` es un testigo de apilamiento que respeta los pares declarados, comenzando en cero abajo. La implementación puede no devolver niveles por cara cuando existe un ciclo o falta información de orden. Un nivel no es un identificador material único ni una descripción canónica de todos los apilamientos admisibles. Varias caras pueden compartirlo. La coincidencia de totales no prueba que una selección siga señalando la cara deseada.

### Ejercicio 4 — Distinguir tres operaciones de orden

Un revisor llama «reordenar matrices» a rotar el contorno de una cara, mezclar las entradas de `faceOrders` y dar la vuelta al modelo. ¿Qué distinciones pierde? Transforma `[1,3,1]`.

> **Respuesta:** La rotación del contorno conserva el sentido cíclico; mezclar las relaciones conserva cada una y cambia su enumeración; dar la vuelta cambia las orientaciones y la interpretación de arriba. Requieren comprobaciones distintas. El triple pasa a `[0,1,1]`: sus referencias siguen p y su signo relativo se conserva. Esto por sí solo no establece una relación global «encima».

## 4. Precisar la transformación y los límites de la evidencia

`move_folded` rota el marco plegado en su plano y después lo traslada, conservando las orientaciones. La prueba usa 0,7 radianes y el desplazamiento `[3,-2]`, y afirma igualdad de toda la estructura de apilamiento devuelta respecto al resultado inicial. La observación respalda ese movimiento rígido probado, sin abarcar escalado, deformación ni remallado arbitrarios.

`turn_over` refleja las coordenadas plegadas mediante `y -> -y`. Su documentación indica que las orientaciones y arriba se invierten conjuntamente, por lo que `faceOrders`, relativo a las normales, permanece igual. La prueba compara `ply`, su altura, el número de niveles rígidos y su altura. Explícitamente **no** comprueba qué cara ocupa cada nivel. Informar de niveles individuales sin cambios al dar la vuelta excedería la evidencia. Correspondencia material y orden vertical son cuestiones separadas.

Un informe útil nombra revisión fuente, transformación, dirección del mapa, índices seleccionados antes y después, propiedad comparada y resultado. Si una regeneración arbitraria no aporta correspondencia, la identidad queda sin resolver. Un espesor total idéntico o una silueta conocida no reemplazan el mapa. Este requisito de comunicación se propone para un flujo futuro; no describe un protocolo de selección ya implementado en IX.

### Ejercicio 5 — Diseñar una prueba falsable de selección

Propón un ensayo futuro en Godot que pueda refutar la conservación correcta de la selección tras esta renumeración sintética. Incluye una afirmación sobre dar la vuelta que las fuentes actuales no justifican.

> **Respuesta:** Antes de transformar, seleccionar B en la entrada 1 y registrar la etiqueta didáctica, la revisión del modelo y el mapa. Tras aplicar p, el resaltado y el informe deben señalar la salida 0, B, nivel 2. Resaltar la salida 1/D refuta la conservación aunque coincidan los totales. Guardar eventos sin modificar y capturas antes y después; aquí no se ha ejecutado el ensayo. «B conserva su nivel al dar la vuelta» no está respaldado por las afirmaciones agregadas de la prueba fijada.

El ensayo propuesto necesita un adaptador real de escenas y observación independiente. Los entregables actuales son análisis de fuentes, una tabla sintética y tareas preparadas para un estudiante. Siguen pendientes la revisión humana de la materia, una respuesta real del estudiante, la revisión lingüística y la publicación.
