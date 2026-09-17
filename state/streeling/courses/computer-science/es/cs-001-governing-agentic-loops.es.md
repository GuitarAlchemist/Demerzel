---
module_id: cs-001-governing-agentic-loops
department: computer-science
course: "IA agéntica — Sistemas multiagente, uso de herramientas, bucles de razonamiento"
level: intermediate
prerequisites: ["Multi-agent orchestration patterns"]
estimated_duration: "25 minutes"
produced_by: seldon-auto-research
research_cycle: cs-2026-03-22-001
coverage_ratio_at_selection: 0.0
version: "1.0.0"
---

# Gobernar los bucles agénticos: evitar la iteración ilimitada en sistemas impulsados por LLM

> **Departamento de Ciencias de la Computación** | Nivel: Intermedio | Duración: 25 minutos

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
Un LLM dentro de un bucle se enfrenta al mismo problema: el sistema que ejecuta el bucle no puede determinar de forma fiable
si ese bucle terminará. La comprobación debe ser externa.

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

Estas propiedades son necesarias y suficientes para una iteración acotada y auditable:

### Propiedad 1: límite estricto de iteraciones
Un número máximo de iteraciones impuesto por el framework, no por el modelo. Al alcanzarlo: detenerse,
registrar el límite y escalar a revisión humana.

```yaml
# Example: Demerzel autonomous-loop configuration
max_iterations: 12
cap_behavior: halt_and_escalate
```

### Propiedad 2: prueba de progreso
Cada iteración debe producir un cambio de estado medible. El framework compara los hashes del estado
antes y después de cada paso. Si `hash(state_n) == hash(state_n-1)`, el bucle está estancado.

```python
def progress_test(state_before, state_after):
    return hash(state_before) != hash(state_after)

if not progress_test(prev_state, curr_state):
    raise StallDetected("No state change — possible infinite loop")
```

### Propiedad 3: criterio de terminación externo
La condición de salida se especifica antes de que empiece el bucle, no se genera durante la ejecución.
El modelo no puede redefinir la convergencia a mitad del bucle.

```python
# Good: criterion is external
def is_complete(state) -> bool:
    return state.belief_confidence >= 0.85 or state.iteration >= MAX

# Bad: model declares its own completion
result = model.run("keep going until you think you're done")
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

El framework Demerzel lo implementa mediante `autonomous-loop-policy.yaml`:

```
GOVERNED LOOP
├── Pre-conditions (checked before first iteration)
│   ├── Kill switch check
│   ├── Daily/session cap check
│   └── Termination criterion defined
│
├── Iteration body
│   ├── Execute step
│   ├── Progress test (hash compare)
│   ├── Checkpoint emit (every N steps)
│   └── Output dedup check
│
└── Post-conditions (any can halt the loop)
    ├── Termination criterion met → complete
    ├── Iteration cap hit → escalate
    ├── Stall detected → escalate
    ├── Kill switch set → halt immediately
    └── Anomaly detected → conscience signal + halt
```

Este patrón aparece en tres lugares del ecosistema Demerzel:
- **Seldon Plan:** límite de 6 ciclos al día, registro de novedad como prueba de progreso
- **Demerzel Driver:** límite de 12 ciclos consecutivos, señales de conciencia como detección de anomalías
- **Ralph Loop:** límite de iteraciones + métrica de convergencia (tasa de pruebas superadas) como criterio externo

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

## Conclusiones clave

- Un LLM no puede detectar de forma fiable sus propios bucles infinitos: la terminación debe ser externa
- Un bucle gobernado tiene exactamente seis propiedades: límite estricto, prueba de progreso, criterio externo, punto de control, deduplicación, decisión de salida externa
- El framework Demerzel las implementa en seldon-plan, demerzel-drive y Ralph Loop
- El artículo 9 (Autonomía acotada) es la base constitucional: los límites están predefinidos y ampliarlos requiere escalado

## Lecturas adicionales

- `policies/autonomous-loop-policy.yaml`: especificación del bucle gobernado de Demerzel
- `policies/seldon-plan-policy.yaml`: fase 1 (WAKE), interruptor de emergencia y lógica de límites
- `policies/continuous-learning-policy.yaml`: límites de iteración en los pipelines de aprendizaje
- `.claude/skills/demerzel-drive/SKILL.md`: ciclo del Driver (patrón de límite de 12 ciclos)
- `.claude/skills/seldon-plan/SKILL.md`: ciclo de investigación (límite de 6 al día + registro de novedad como prueba de progreso)

---
*Producido por Seldon Auto-Research cs-2026-03-22-001 el 2026-03-22.*
*Pregunta de investigación: ¿Qué propiedades de gobernanza debe cumplir un framework de orquestación multiagente para evitar bucles de razonamiento ilimitados sin renunciar a la resolución iterativa legítima de problemas?*
*Creencia: T (confianza: 0.82): coherente internamente con la teoría del problema de la parada y la arquitectura de gobernanza de Demerzel*
