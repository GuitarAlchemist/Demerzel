---
module_id: cs-002-governing-agentic-loops
department: computer-science
course: "IA agéntica — Sistemas multiagente, uso de herramientas, bucles de razonamiento"
level: intermediate
prerequisites: ["Patrones de orquestación multiagente"]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
revised_by: codex-project-pilot
research_cycle: computer-science-2026-10-12-002
original_research_cycle: cs-2026-03-22-001
coverage_ratio_at_selection: 0.0
version: "1.1.0"
---

# Gobernar los bucles agénticos: evitar la iteración ilimitada en sistemas impulsados por LLM

> **Departamento de Ciencias de la Computación** | Nivel: Intermedio | Duración: 35 minutos | Borrador revisado; pendientes la revisión humana del contenido y la prueba con un alumno

## Objetivos

- Distinguir la iteración productiva (convergente) de los bucles patológicos (divergentes) en agentes impulsados por LLM
- Entender por qué las condiciones de terminación deben imponerse desde fuera en lugar de autodeclararse
- Aplicar las seis propiedades requeridas de un bucle gobernado a diseños de sistemas reales
- Relacionar la gobernanza de bucles con el artículo Default 9 (Autonomía acotada) de la constitución de Demerzel

---

## 1. El problema del bucle

Un agente LLM al que se le da un objetivo iterará hacia él. Esto es útil: el refinamiento iterativo es
la forma en que se resuelven las tareas complejas. Pero crea un riesgo estructural: **el mismo razonamiento que produjo
el bucle puede producir la valoración «he convergido».**

No es un error de ningún modelo concreto. Es una propiedad intrínseca de la generación autorregresiva:
el modelo no puede observar su propio comportamiento desde fuera. Puede describir la convergencia, pero no puede
garantizarla. La garantía debe venir del framework.

### El paralelo con la parada

Alan Turing demostró (1936) que ningún algoritmo puede decidir, para todos los programas, si se detendrán.
Tampoco hay un procedimiento general que pueda decidirlo para un bucle de agente arbitrario. Por eso la terminación se impone
en lugar de detectarse: un límite impuesto por el framework acota el número de iteraciones, y un plazo máximo impuesto por el framework a cada iteración completa la detiene cuando vence, si hace falta matando el proceso que la ejecuta. Solo los dos juntos hacen que el bucle se detenga por construcción: una iteración que nunca termina nunca llega al contador, y un plazo en cada llamada no basta, porque una iteración puede encadenar cualquier número de llamadas o calcular entre ellas.

El teorema de la parada **no** demuestra que todos los agentes se equivoquen cuando declaran haber terminado. Descarta un procedimiento de decisión universal para programas arbitrarios. Para los cursos y las releases de este proyecto, la regla práctica es más concreta: comprobar los artefactos externos en vez de aceptar la declaración del agente.

**Implicación:** Cualquier framework agéntico que dependa de que el modelo declare su propia finalización
es defectuoso por construcción.

---

## 2. Taxonomía: bucles productivos frente a patológicos

| Propiedad | Productivo | Patológico |
|---|---|---|
| Cada iteración produce un estado distinto | Sí | No: las salidas se repiten o derivan |
| El criterio de terminación puede definirse antes del bucle | Sí | No: el criterio se genera dentro del bucle |
| El progreso es medible desde fuera | Sí | No: solo autodeclarado |
| Un humano puede inspeccionar el estado intermedio | Sí | No: solo interno |
| El bucle puede pausarse y reanudarse | Sí | No: el estado no es serializable |

Un bucle es **productivo** cuando cada iteración acerca el sistema, de forma medible, a un estado
terminal definible. Es **patológico** cuando genera tokens sin generar transiciones de estado.

---

## 3. Seis propiedades requeridas de un bucle gobernado

Estas seis propiedades hacen que una iteración sea acotada y auditable. Un bucle que deba poder pausarse y reanudarse necesita además un estado serializable (secciones 2 y 6):

### Propiedad 1: límite estricto de iteraciones
Un número máximo de iteraciones impuesto por el framework, no por el modelo. Al alcanzarlo: detenerse,
registrar el límite y escalar a revisión humana. El contador solo avanza cuando termina una iteración, así que el límite también exige un plazo máximo alrededor de cada iteración completa, impuesto por el framework, que detiene la iteración cuando vence, si hace falta matando el proceso que la ejecuta. Los plazos en las llamadas al modelo, las llamadas a herramientas y las peticiones de red son útiles, pero no acotan por sí solos una iteración. La configuración de abajo solo fija el límite.

```yaml
# Ejemplo: configuración de un bucle (valor por defecto de la política 10, máximo absoluto 25)
max_iterations: 12
cap_behavior: halt_and_escalate
```

El valor `12` es un ejemplo de configuración, no el valor por defecto actual de Demerzel. La [política de bucles fijada](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/policies/autonomous-loop-policy.yaml) indica `default_max: 10`, `absolute_max: 25` y `stall_limit: 3`. El registro de investigación de marzo hablaba de un «límite de 12 ciclos»; esta comprobación corrige esa afirmación histórica sin convertirla en una regla vigente.

### Propiedad 2: prueba de progreso
Cada iteración debe producir un cambio de estado medible. El framework compara los hashes del estado
antes y después de cada paso. Si `hash(state_n) == hash(state_n-1)`, el bucle está estancado. Calcula el hash
de los campos que llevan el resultado, no del contador de iteraciones: ese cambia en cada paso, así que la
prueba de estancamiento nunca se activaría. Y una prueba de estancamiento detecta la repetición, no la deriva: un
bucle que sigue cambiando sin converger nunca cumple el criterio externo, y lo detiene el límite, no esta prueba.

```python
def stall_test(state_before, state_after):
    return hash(state_before) == hash(state_after)

if stall_test(prev_state, curr_state):
    raise StallDetected("Ningún cambio de estado — posible bucle infinito")
```

### Propiedad 3: criterio de terminación externo
La condición de salida se especifica antes de que empiece el bucle, no se genera durante la ejecución.
El modelo no puede redefinir la convergencia a mitad del bucle. El límite de iteraciones no forma parte del criterio: un bucle que alcanza el límite no ha convergido, y se detiene y escala como exige la propiedad 1, en lugar de dar su trabajo por terminado.

```python
# Bien: el criterio es externo
def is_complete(state) -> bool:
    return state.belief_confidence >= 0.85

# Alcanzar el límite no es un éxito: detenerse y escalar (propiedad 1)
def cap_reached(state) -> bool:
    return state.iteration >= MAX

# Mal: el modelo declara él mismo que ha terminado
result = model.run("sigue hasta que creas que has terminado")
```

### Propiedad 4: punto de control legible por humanos
Cada N iteraciones, el framework emite un punto de control: una entrada de registro estructurada que un humano
puede leer sin ejecutar el bucle. Sirve a la vez como observabilidad y como pista de auditoría.

### Propiedad 5: deduplicación de salidas
El framework lleva la cuenta del conjunto de salidas emitidas hasta el momento. Si una salida candidata es
funcionalmente idéntica a una salida anterior, se marca como indicio de bucle.

### Propiedad 6: decisión de salida externa
El modelo propone la terminación; el framework decide. El «he terminado» del modelo se
trata como un voto, no como una orden.

---

## 4. El patrón de bucle gobernado de Demerzel

El framework Demerzel especifica este patrón en `autonomous-loop-policy.yaml`, con límites de iteraciones y de estancamiento pero sin plazo por iteración:

```
BUCLE GOBERNADO
├── Precondiciones (comprobadas antes de la primera iteración)
│   ├── Comprobación del kill switch
│   ├── Comprobación del límite diario/de sesión
│   └── Criterio de terminación definido
│
├── Cuerpo de la iteración
│   ├── Ejecutar el paso
│   ├── Prueba de progreso (comparación de hashes)
│   ├── Emisión de un punto de control (cada N pasos)
│   └── Comprobación de deduplicación de salidas
│
└── Postcondiciones (cualquiera puede detener el bucle)
    ├── Criterio de terminación cumplido → completado
    ├── Límite de iteraciones alcanzado → escalar
    ├── Estancamiento detectado → escalar
    ├── Kill switch activado → detención inmediata
    └── Anomalía detectada → señal de conciencia + detención
```

Este patrón aparece en tres lugares del ecosistema Demerzel, y solo los dos primeros acotan la duración de una iteración:
- **Seldon Plan:** límite de 6 ciclos al día, registro de novedad como prueba de progreso, límite flexible de 30 minutos por ciclo (`policies/seldon-plan-policy.yaml`) y parada forzosa a los 35 minutos (`timeout-minutes` en `.github/workflows/seldon-plan.yml`)
- **Demerzel Driver:** una pausa para revisión humana tras 5 ciclos consecutivos sin intervención, señales de conciencia como detección de anomalías, plazo de ciclo (2 horas flexible, luego parada forzosa a las 2h15)
- **Ralph Loop:** límite de iteraciones + métrica de convergencia (tasa de pruebas superadas) como criterio externo, pero sin plazo por iteración: ni `policies/autonomous-loop-policy.yaml` ni `.claude/skills/demerzel-loop/SKILL.md` lo definen, así que una iteración que se bloquea nunca llega al contador

---

## 5. Fundamento constitucional

**Artículo Default 9 — Autonomía acotada:**
> Los agentes operan dentro de límites predefinidos. La autonomía es un recurso, no un derecho.
> Cuando se alcanzan los límites, escala; no te autorices a ti mismo a ampliarlos.

Las seis propiedades anteriores hacen operativo el artículo 9 para los procesos iterativos. En concreto:
- Límite estricto = límite predefinido
- Terminación externa = «predefinido» (no decidido sobre la marcha)
- Escalado al llegar al límite = «escala, no te autorices a ti mismo»

**Artículo Default 7 — Auditabilidad:**
> Cada ciclo debe registrarse con una traza completa.

Los puntos de control y los registros de deduplicación de salidas lo cumplen: el bucle es auditable incluso a mitad de la ejecución.

---

## 6. Antipatrones

| Antipatrón | Por qué falla | Solución |
|---|---|---|
| `while not model.done()` | El modelo declara su propia finalización | Sustituir por un criterio externo |
| Número de iteraciones en el prompt («inténtalo 5 veces») | El modelo puede ignorarlo al generar | Imponerlo en el framework, no en el prompt |
| «Sigue mejorando hasta quedar satisfecho» | Sin límite, la satisfacción es autodeclarada | Definir una métrica de satisfacción medible |
| Sin registro de puntos de control | Bucle no auditable sobre la marcha | Emitir un punto de control cada N iteraciones |
| Estado no serializado | El bucle no puede pausarse/reanudarse | Usar una máquina de estados, serializar cada paso |

---

## Práctica: decidir a partir de trazas

Lee la [política de bucles fijada](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/policies/autonomous-loop-policy.yaml) y el [workflow de Seldon](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/.github/workflows/seldon-plan.yml) antes de responder. Los casos siguientes son **ejemplos ficticios**, salvo donde se cita una fuente. Una política escrita, una configuración de workflow y una ejecución observada son pruebas distintas.

### Ejercicio práctico 1

Un bucle tiene `max_iterations: 10`. Termina dos iteraciones y se bloquea para siempre dentro de la tercera llamada a una herramienta. ¿Lo acota el límite de iteraciones? Nombra el límite que falta y el archivo del proyecto que configura un plazo para un job completo.

> **Respuesta:** No. El contador llega a tres solo cuando termina la tercera iteración, así que el límite de diez no detiene esa llamada. Hace falta un plazo impuesto a la iteración completa, o un plazo estricto que abarque el job y pueda terminar su proceso. El workflow de Seldon declara `timeout-minutes: 35` para su job; la política general declara recuento y límite de estancamiento, pero no un plazo por iteración. Una configuración de timeout no demuestra que una ejecución local arbitraria haya sido detenida.

### Ejercicio práctico 2

Un estado cambia de `{payload: "A", iteration: 4}` a `{payload: "A", iteration: 5}`. Otro cambia de `{payload: "A", iteration: 5}` a `{payload: "B", iteration: 6}`, pero sigue faltando el artefacto objetivo. ¿Qué cambio es un estancamiento exacto si se excluye el contador? ¿El segundo demuestra convergencia?

> **Respuesta:** El primero es un estancamiento exacto si el hash incluye `payload` y excluye el contador. En el segundo cambia el valor, por lo que no se activa la prueba de igualdad, pero tampoco se demuestra un avance hacia el artefacto. Un criterio de éxito independiente debe comprobar ese artefacto y las demás pruebas exigidas. Por eso la política distingue convergencia, regresión y deriva: un hash distinto no equivale a éxito.

### Ejercicio práctico 3

Un agente de cursos llega a su décima iteración completada, declara una confianza de `0.90` y ha redactado el curso prometido. Faltan el veredicto humano sobre el contenido y la comprobación de la página pública. Clasifica el resultado como `complete`, `halt_and_escalate` o `continue`, y explica por qué el ejemplo `is_complete` de la sección 3 no basta para publicar.

> **Respuesta:** `halt_and_escalate` para este bucle acotado: alcanzó el límite sin satisfacer el criterio externo completo. El borrador es un avance, pero ni la confianza ni el archivo por sí solos prueban la revisión humana o la publicación. La función `belief_confidence >= 0.85` ilustra dónde aplicar una comprobación externa; no es un criterio suficiente para Streeling. Una nueva unidad de trabajo autorizada puede seguir con otros cursos, pero el bucle agotado no debe llamar «completo» a su resultado parcial.

### Ejercicio práctico 4

La política indica `default_max: 10`, `absolute_max: 25` y `stall_limit: 3`; un registro de 2026 dice «límite de 12 ciclos»; el ejemplo del curso configura 12. ¿Cuál es el valor por defecto? ¿Cuál es un ejemplo permitido si se admiten ajustes por bucle? ¿Qué prueba mostraría que una ejecución concreta utilizó 12?

> **Respuesta:** Diez es el valor por defecto de la política fijada y 25 su máximo absoluto. Doce es un ejemplo de límite particular dentro de esas cotas, no el valor por defecto. La frase del registro antiguo contradice la política fijada y no debe repetirse como regla vigente. Para una ejecución concreta hay que inspeccionar su configuración efectiva y una traza que la vincule con esa ejecución; ni la política general ni este curso lo demuestran.

### Ejercicio práctico 5

Un revisor pregunta si `timeout-minutes: 35` demuestra que todos los bucles de Demerzel o Ralph tienen un plazo por iteración y siempre se detienen limpiamente. Responde en dos frases ajustadas a las pruebas y nombra una observación necesaria para verificar un timeout en una ejecución real de Seldon.

> **Respuesta:** El workflow fijado configura un límite de 35 minutos para ese job de Seldon, mientras que la política general no define ningún plazo por iteración; no se puede extender esa conclusión a todos los bucles de Demerzel o Ralph. Un timeout estricto puede terminar el trabajo sin un punto de control limpio, por lo que esa afirmación también requiere una traza. Para una ejecución real, inspecciona el resultado y los tiempos del job y el último punto de control o la salida del proceso; el YAML solo declara la configuración.

Estas respuestas comprueban razonamientos sobre fuentes fijadas y casos concretos. No acreditan que se haya observado un agente en ejecución ni que todo el framework aplique las seis propiedades. Siguen pendientes la revisión humana del contenido y una prueba con un alumno sin respuestas; esta traducción no ha sido revisada por un hablante designado.

## Conclusiones clave

- Un LLM no puede detectar de forma fiable sus propios bucles infinitos: la terminación debe ser externa
- Un bucle gobernado tiene seis propiedades: límite estricto con un plazo máximo en cada iteración, prueba de progreso, criterio externo, punto de control, deduplicación, decisión de salida externa, más un estado serializable si debe poder pausarse y reanudarse
- El framework Demerzel aplica el patrón en seldon-plan, demerzel-drive y Ralph Loop; solo los dos primeros fijan un plazo por iteración, así que Ralph Loop aún no se detiene por construcción
- El artículo 9 (Autonomía acotada) es la base constitucional: los límites están predefinidos y ampliarlos requiere escalado

## Lecturas adicionales

- `policies/autonomous-loop-policy.yaml`: especificación del bucle gobernado de Demerzel
- `policies/seldon-plan-policy.yaml`: fase 1 (WAKE), interruptor de emergencia y lógica de límites
- `policies/continuous-learning-policy.yaml`: límites de iteración en los pipelines de aprendizaje
- `.claude/skills/demerzel-drive/SKILL.md`: ciclo del Driver (pausa tras 5 ciclos sin intervención)
- `.claude/skills/seldon-plan/SKILL.md`: ciclo de investigación (límite de 6 al día + registro de novedad como prueba de progreso)

---
*Producido por Seldon Auto-Research cs-2026-03-22-001 el 2026-03-22.*
*Pregunta de investigación: ¿Qué propiedades de gobernanza debe cumplir un framework de orquestación multiagente para evitar bucles de razonamiento ilimitados sin renunciar a la resolución iterativa legítima de problemas?*
*Creencia: T (confianza: 0.82): coherente internamente con la teoría del problema de la parada y la arquitectura de gobernanza de Demerzel; traducción al español: U (sin revisión de un hablante nativo)*
