---
module_id: net-003-worker-lane-coverage-and-fragility
department: network-science
course: "Medir la cobertura de las vías de trabajo tras un cambio de modo"
level: intermediate
prerequisites: [net-002-capability-graphs-and-projections]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-003
version: "0.1.0"
---

# Medir la cobertura de las vías de trabajo tras un cambio de modo

> **Departamento de ciencia de redes** | Nivel intermedio | 35 minutos | Borrador en español; revisión y publicación pendientes

## Objetivos y pregunta del proyecto

Construirás un grafo entre trabajadores y clases de trabajo a partir de una política de vías de Demerzel fijada a un commit. Medirás la cobertura y el efecto de retirar un trabajador, y comprobarás qué información pierde el grafo sobre los roles y las decisiones. **Pregunta del proyecto:** si cambia el modo consultivo de distribución o una vía deja de estar disponible, ¿qué *clases de trabajo declaradas* siguen teniendo una ruta nominal? El cálculo puede orientar la elección de una vía o una pregunta de revisión. No demuestra que un agente esté conectado, tenga autorización para actuar o haya terminado una tarea.

[NET-002](../en/net-002-capability-graphs-and-projections.md) conecta *repositorios* con familias de capacidades. Esta lección conecta *trabajadores* con roles asignados y clases de trabajo. Sus aristas proceden de la [política de vías de Demerzel en el commit `ecdc6c2`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) y se filtran según el modo solicitado. El grafo no contiene rutas MCP ni datos actuales de personal.

## 1. Definir el grafo antes de medirlo

La política fijada declara cinco trabajadores: `jules`, `claude`, `gemini`, `codex` y `augment`. Cada uno tiene un rol `primary`, una lista de roles `secondary` y otra lista `forbidden` ([definiciones de trabajadores](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L54-L79)). Cada rol nombrado se asocia a una `work_class` ([definiciones de roles](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L19-L51)). La propia política se declara **consultiva y de simulación**. Propone una ruta, pero no acredita trabajo realizado.

Construye un grafo dirigido de tres capas `trabajador → rol asignado → clase de trabajo`. Dibuja la primera arista solo para un rol primario o secundario; un rol prohibido nunca crea una ruta. La segunda arista sigue `work_class`. Para un modo, oculta las rutas cuya clase figure en [`mode_blocks`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L81-L86). En la proyección de dos capas existe una arista trabajador-clase si sobrevive al menos una ruta de rol asignado. Varios roles de la misma clase cuentan como **una** arista trabajador-clase. Contamos opciones de trabajadores distintos para una clase, no capacidad ni tareas completadas.

El diccionario completo `work_classes` tiene 13 nombres, incluidas acciones prohibidas. Solo cinco clases aparecen en asignaciones primarias o secundarias: `fix`, `groom`, `navigate`, `net_new_feature` y `review`. Llama `A` a ese conjunto. Define la **cobertura** `C(m) = |{c in A: degree_m(c) > 0}| / |A|` y el **número de clases redundantes** `R(m) = |{c in A: degree_m(c) >= 2}|`. Son medidas descriptivas: dos trabajadores vecinos de una clase no son necesariamente intercambiables para un rol concreto.

### Ejercicio práctico 1: evitar contar roles dos veces

En NORMAL, `claude` tiene `draft_to_ready_helper`, `test_author` y `review_feedback_applier`, todos de clase `fix`; además, `builder_fixer` pertenece a `net_new_feature` y `lightweight_groomer` a `groom`. ¿Cuál es el grado de `claude` en la proyección trabajador-clase y cuántas rutas hacia roles asignados tiene? ¿Por qué difieren?

> **Respuesta:** Su grado proyectado es **3**: `fix`, `net_new_feature` y `groom`. Tiene **5** rutas hacia roles asignados, una primaria y cuatro secundarias. Los tres roles `fix` se reducen a una sola arista trabajador-clase. Contar cinco roles como cinco trabajadores alternativos inflaría falsamente la redundancia.

## 2. Medir el corte causado por un modo

Las asignaciones primarias y secundarias producen la siguiente proyección en NORMAL. Un `1` indica que sobrevive al menos una ruta de rol asignado tras filtrar por clase:

| Trabajador | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 1 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

La matriz contiene **9** aristas trabajador-clase. Los grados son `fix:2`, `groom:2`, `navigate:1`, `net_new_feature:1` y `review:3`. Por tanto, `C(NORMAL)=5/5` y `R(NORMAL)=3`. CONSTRAINED bloquea `net_new_feature` y `broad_architecture`; DRAINING también bloquea `workflow_policy_change`. De ellas, solo `net_new_feature` tiene una ruta asignada: **ambos** modos conservan 8 aristas y cuatro clases cubiertas, con `C=4/5` y `R=3`. HALTED también bloquea `fix`, `groom` y `navigate`, pero no `review`. Quedan tres aristas, todas hacia `review`: `C(HALTED)=1/5` y `R(HALTED)=1`. Ese cociente no da luz verde para operar un sistema detenido; solo describe las declaraciones que sobreviven al filtro.

### Ejercicio práctico 2: calcular un corte, no una caída real

En DRAINING, ¿qué arista de NORMAL desaparece, cuánto valen `C` y `R`, y demuestra el cálculo que un agente Claude realmente dejó de trabajar?

> **Respuesta:** Solo desaparece `claude → net_new_feature`, la única arista asignada de esa clase bloqueada. Permanecen ocho de las nueve aristas; cuatro de cinco clases siguen cubiertas, luego `C=4/5`. `fix`, `groom` y `review` aún tienen grado al menos dos, luego `R=3`. Es un corte del grafo de políticas, no una observación de un agente activo ni de una asignación real.

## 3. Probar la fragilidad ante la pérdida de un trabajador

Para el modo `m` y el trabajador retirado `w`, define `L_m(w)` como el número de clases cubiertas antes de retirarlo y descubiertas después. Elimina `w` y sus rutas, y vuelve a calcular los grados. En DRAINING, solo `augment` tiene una arista hacia `navigate`. Retirarlo cambia el grado de `navigate` de 1 a 0; así, `L_DRAINING(augment)=1` y la cobertura baja de `4/5` a `3/5`. Retirar cualquiera de los otros cuatro trabajadores no pierde **ninguna clase completa**, porque queda otro trabajador vecino. Es una prueba de sensibilidad mediante eliminación de vértices, no una predicción de probabilidad de fallo. El JSON no registra toda causa de indisponibilidad y compartir una clase no garantiza el rol exacto exigido por una tarea.

La redundancia por clase no equivale a la redundancia por rol. `review` tiene tres trabajadores vecinos en DRAINING, pero el rol primario `read_only_critic` de `gemini`, el secundario `architecture_summarizer` de `jules` y los roles secundarios de revisión de `codex` son asignaciones distintas. El grafo conserva una ruta general de revisión tras perder a un trabajador. No ofrece tres sustitutos para cada rol solicitado; puede requerirse reasignación o escalado.

### Ejercicio práctico 3: eliminar un vértice

Compara retirar `augment` y retirar `codex` del grafo DRAINING. Indica clases perdidas y cobertura resultante. ¿Permite el grafo juzgar si las notas de revisión sustitutivas serían igual de buenas?

> **Respuesta:** Sin `augment` se pierde `navigate`; permanecen `fix`, `groom` y `review`, de modo que `C=3/5`. Sin `codex` no se pierde ninguna clase: `claude` conserva `fix`, mientras `jules` y `gemini` conservan `review`; `C=4/5`. Ningún resultado mide calidad, permisos, equivalencia exacta de roles, disponibilidad ni trabajo terminado.

## 4. Conservar la semántica del selector junto al grafo

El [selector consultivo fijado](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L1-L19) consume la política. Comprueba por orden trabajador desconocido, modo desconocido, roles prohibidos, pertenencia del rol solicitado a la vía y bloqueo de su clase ([orden de decisión](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L77-L154)). Un rol primario asignado y no bloqueado produce `allow`; uno secundario produce `recommend`, no `allow`. Un rol prohibido produce `block` **antes** de comprobar la pertenencia. Un rol ajeno a la vía produce `warn`. Una clase bloqueada produce `block` con un código de backpressure. Son respuestas del código, no permisos para modificar estado. El código de salida 0 significa **evaluado**; la decisión está en el JSON. Un error de entrada o política puede devolver 2.

En DRAINING, `builder_fixer`, rol primario de `claude`, corresponde a `net_new_feature`, bloqueada; `test_author`, secundario, corresponde a `fix`, no bloqueada. El código predice `block` para la primera solicitud y `recommend` para la segunda. Eso **no** significa que `test_author` pueda construir una función nueva: el rol solicitado y la salida esperada deben coincidir con el trabajo. `autonomous_merge_actor` está expresamente prohibido a `codex`, de modo que su solicitud predice `block` incluso tras cambiar de modo. Ninguna arista del grafo autoriza una fusión.

### Ejercicio práctico 4: distinguir rutas de decisiones

En DRAINING, predice las decisiones para `(claude, builder_fixer)`, `(claude, test_author)` y `(codex, autonomous_merge_actor)`. ¿Qué información necesaria para la última solicitud se pierde al guardar solo la proyección trabajador-clase?

> **Respuesta:** La primera recibe `block` porque `net_new_feature` está bloqueada; la segunda recibe `recommend` porque `test_author` es un rol `fix` *secundario* no bloqueado; la tercera recibe `block` porque `autonomous_merge_actor` figura entre los roles prohibidos de `codex`. La proyección no guarda la lista prohibida ni el orden de comprobación del selector. Una arista de fusión ausente no equivale a un simple aviso por rol desconocido ni a permiso.

## 5. Hacer refutable la medida

Los recuentos anteriores se calcularon a partir del **JSON fijado**: expansión de roles primarios y secundarios, asignación de `work_class`, filtro por `mode_blocks` y deduplicación de pares `(trabajador, clase)`. Un [script de repetición sin conexión](../../../../../scripts/streeling_net003_replay.py) comprueba ahora por separado la interpretación del selector. Compara los identificadores de blob Git del selector y la política presentes en el checkout con los del commit fijado y enumera los 22 pares `(trabajador, rol)` asignados en cada uno de los cuatro modos. `allow` y `recommend` cuentan como rutas asignadas no bloqueadas; `block` indica una ruta cortada por el modo. El [comprobante de la repetición del 12 de octubre de 2026](../../../reviews/net-003-selector-replay-2026-10-12.json) registra **22, 21, 21, 8** rutas de rol no bloqueadas para NORMAL, CONSTRAINED, DRAINING y HALTED, **9, 8, 8, 3** aristas trabajador-clase proyectadas y **5, 4, 4, 1** rutas primarias no bloqueadas. Todos los resultados coinciden con las predicciones de la política y el selector fijados.

La repetición compara la decisión del JSON, no el código de salida del proceso. Sus controles separados devolvieron `block` para el rol de fusión prohibido a `codex`, `warn` para un rol desconocido y `escalate` para un modo desconocido; ninguno pertenece a los 22 pares asignados. Una discrepancia en los recuentos o decisiones refutaría la regla de rutas supuesta o revelaría deriva de las fuentes. La coincidencia valida este modelo limitado para la revisión fijada, sin demostrar planificación real, salud de trabajadores ni corrección de la gobernanza humana. Para reproducir el comprobante JSON, ejecuta `python scripts/streeling_net003_replay.py` desde la raíz del repositorio Demerzel.

### Ejercicio práctico 5: diseñar el oráculo de repetición

Supón que `(claude, builder_fixer, DRAINING)` devuelve código de salida 0 y decisión JSON `block`. Alguien cuenta una ruta activa porque el proceso terminó correctamente. ¿Cuál es la clasificación correcta? Da un recuento que, si difiere de las predicciones, refutaría la extracción del grafo.

> **Respuesta:** Es una **ruta hacia un rol asignado pero bloqueado**. El código 0 indica evaluación consultiva, no autorización. La repetición debería encontrar 21 rutas asignadas no bloqueadas en DRAINING y 8 aristas trabajador-clase tras la proyección. Hallar, por ejemplo, 22 rutas o 9 aristas con la política y el script fijados refutaría la extracción. Por sí solo no demostraría un incidente de producción.

## Evidencia y límites

- La [política de vías](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) y el [selector](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) están fijados al commit Demerzel `ecdc6c27559bb1a11343cfad33687465893e9891`. La repetición local de la sección 5 verificó sus identificadores de blob Git antes de usar los archivos del checkout. Es un cálculo reproducible y una invocación de prueba del selector, no una medida de agentes activos.
- El grafo agrupa roles asignados diferentes en clases. Excluye roles prohibidos y no conserva todas las entradas, el orden de decisión ni la autoridad del selector. `allow` y `recommend` son valores consultivos, no comprobantes de trabajo terminado.
- Retirar trabajadores y cortar modos son pruebas de sensibilidad sobre un grafo estático declarado. Antes de afirmar algo sobre rutas operativas, comprueba la revisión actual de la política, la solicitud y decisión reales, presencia y permisos del trabajador, y artefacto o comprobante de la tarea. Siguen pendientes la revisión técnica, los intentos de estudiantes, la revisión de traducción, la sincronización y compilación de Learn, y la lectura pública anónima.
