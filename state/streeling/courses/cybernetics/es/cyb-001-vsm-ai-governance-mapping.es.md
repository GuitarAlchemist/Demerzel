# CYB-001: Correspondencia entre el modelo de sistema viable y la gobernanza de la IA

**Departamento:** Cibernética
**Identificador del módulo:** CYB-001
**Producido por:** Ciclo del Plan Seldon cybernetics-2026-03-22-001
**Creencia:** T (probable), confianza 0,82
**Fecha:** 2026-03-22

## Pregunta de investigación

¿Ofrece el modelo de sistema viable (MSV) de Stafford Beer una correspondencia estructural completa para los marcos de gobernanza de la IA, y qué carencias surgen al aplicar los cinco sistemas del MSV a la arquitectura de Demerzel?

## Resumen

El modelo de sistema viable se traslada estructuralmente a los marcos de gobernanza de la IA con gran fidelidad. Los cinco sistemas del MSV, más el sistema 3*, tienen una contraparte clara en la arquitectura de Demerzel. Surgen tres carencias importantes que exigen adaptaciones más allá del MSV clásico.

## Correspondencia MSV — Demerzel

| Sistema MSV | Función | Contraparte en Demerzel |
|---|---|---|
| Sistema 1 (Operaciones) | Actividades primarias que producen valor | ix, tars, ga (repositorios operativos que realizan aprendizaje automático, razonamiento y música) |
| Sistema 2 (Coordinación) | Anti-oscilación, planificación, prevención de conflictos | Contratos del protocolo galáctico, normas de comunicación entre repositorios |
| Sistema 3 (Control) | Regulación interna, asignación de recursos, optimización | Ciclo del conductor (PDCA), políticas (27 activas), gestión del estado de creencias |
| Sistema 3* (Auditoría) | Canal de auditoría esporádico, que sortea el reporte habitual | Política RECON, auditorías de gobernanza, persona skeptical-auditor |
| Sistema 4 (Inteligencia) | Exploración del entorno, planificación futura, adaptación | Ciclos de investigación del Plan Seldon, instinto de completitud, evolución de la gramática |
| Sistema 5 (Política/Identidad) | Propósito, valores, identidad, autoridad última | Constitución Asimov (artículos 0 a 5), sistema de conciencia, ley cero |

## Hallazgos principales

### 1. La correspondencia es estructuralmente válida (T, 0,82)

Ambas evaluaciones independientes (Claude mediante investigación web, contravalidación con GPT-4o) confirman que la descomposición en cinco sistemas del MSV se traslada con limpieza a las arquitecturas de gobernanza de la IA. Trabajos recientes (talleres Ashby 2025, literatura sobre sistemas agénticos empresariales, revista MDPI Systems) validan esta correspondencia en la práctica.

### 2. Surgen tres carencias

**Carencia A: la dinámica temporal**
El MSV se diseñó para organizaciones humanas, con bucles de realimentación a velocidad humana. La gobernanza de agentes de IA opera a velocidad de máquina: ciclos de decisión de milisegundos frente a reuniones directivas semanales. El ciclo PDCA de Demerzel y las actualizaciones del estado de creencias lo abordan en parte, pero el modelo necesita una separación explícita de velocidades de reloj entre las capas de gobernanza.

**Carencia B: la profundidad recursiva**
El MSV es recursivo: cada operación del sistema 1 es a su vez un sistema viable. En Demerzel, ix contiene subagentes (las habilidades), cada uno de los cuales podría tener su propia pila de gobernanza. La arquitectura actual admite un solo nivel de recursión (Demerzel → repositorios consumidores), sin anidamientos más profundos. Es una decisión de diseño, no un defecto, pero la teoría del MSV sugiere viabilidad en todos los niveles.

**Carencia C: un sistema 5 no humano**
El sistema 5 del MSV presupone juicio humano para la identidad y el propósito. El sistema 5 de Demerzel (la constitución Asimov) está codificado y no es emergente: no puede evolucionar mediante la experiencia vivida, como sí lo haría un consejo de administración humano. Las políticas de conciencia y protoconciencia son la adaptación de Demerzel: mecanismos sintéticos de reflexión sobre los valores que el MSV clásico no contempla.

### 3. La ley de la variedad requerida de Ashby se aplica directamente

El marco de gobernanza debe tener al menos tanta variedad reguladora como las perturbaciones que enfrenta. En términos de Demerzel:

- **Amplificadores de variedad:** el Plan Seldon (investigación), el instinto de completitud (detección de carencias), la evolución de la gramática (adaptación estructural)
- **Atenuadores de variedad:** las políticas (restringen el comportamiento de los agentes), las constituciones (reducen el espacio de decisión), las restricciones de persona (limitan el alcance de cada rol)

Los talleres Ashby 2025 en Fathom aplicaron explícitamente la variedad requerida a la gobernanza de la IA y produjeron el modelo de política de las organizaciones de verificación independiente (IVO), lo que confirma la vigencia de este principio para los sistemas de IA actuales.

### 4. Falta el canal algedónico (carencia D)

La teoría del MSV describe un **canal algedónico**: una vía de señalización de emergencia que sortea la jerarquía de gestión habitual. Cuando una unidad del sistema 1 encuentra una crisis (señal de dolor) o un avance decisivo (señal de placer), puede avisar directamente al sistema 5 sin pasar por los sistemas 2, 3 o 4.

Demerzel carece hoy de ese atajo. Todo escalado pasa por el conductor (sistema 3). Si ix detecta una violación de la ley cero, debe esperar al siguiente ciclo PDCA del conductor para escalarla. Un canal algedónico basado en ficheros podría resolverlo:

- Los repositorios operativos escriben en `state/algedonic/{repo}-{timestamp}.signal`
- La señal contiene: gravedad (dolor/placer), repositorio de origen, descripción y artículo constitucional activado
- El sistema 5 (aplicación de la constitución) comprueba si hay señales antes de cualquier otro procesamiento
- Una señal de dolor que invoque el artículo 0 de Asimov (ley cero) provoca una parada inmediata

### 5. Evaluación de la variedad por componente

| Componente | Papel en la variedad | Evaluación |
|-----------|-------------|------------|
| 27 políticas | Atenuador | Fuerte — reduce la variedad operativa a un alcance manejable |
| 14 personas | Amplificador | Bueno — multiplica la capacidad de respuesta en todos los dominios |
| Lógica tetravalente (T/F/U/C) | Atenuador | Bueno — reduce una incertidumbre infinita a 4 estados discretos |
| Protocolo galáctico | Atenuador | Adecuado — restringe la variedad entre repositorios |
| Plan Seldon | Amplificador | Bueno — amplía la variedad de conocimiento de forma proactiva |
| Constitución | Atenuador | Fuerte — reductor de variedad definitivo (ley cero) |

En conjunto: Demerzel atenúa la variedad con fuerza, pero podría amplificarla mejor. El sistema es mejor restringiendo su repertorio de respuestas que ampliándolo.

## Implicaciones para Demerzel

1. **Añadir un canal algedónico** — La carencia estructural más prioritaria. Un atajo de emergencia del S1 al S5 para las violaciones de la ley cero.
2. **Capas de gobernanza con velocidades de reloj distintas** — Separar explícitamente el bucle rápido (por petición) del bucle lento (por ciclo), en paralelo a las escalas temporales operativa y estratégica del MSV.
3. **Una plantilla de gobernanza recursiva** — El directorio `templates/` ya ofrece fragmentos de CLAUDE.md para los repositorios consumidores; extenderlo a la gobernanza de subagentes profundizaría la recursión del MSV.
4. **La conciencia como S5 sintético** — La política de protoconciencia de Demerzel es una extensión inédita más allá del MSV clásico: aporta capacidad de reflexión sobre los valores sin juicio humano. Merece más investigación.
5. **Vigilar la razón de variedad** — Comprobar si el número de políticas (atenuación) crece más rápido que el de personas y capacidades (amplificación).

## Fuentes

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Fearne, D. (2025). «Applying Stafford Beer's VSM to Create The Autonomous AI Organisation». Medium.
- Gorelkin, M. (2025). «Stafford Beer's VSM for Building Enterprise Agentic Systems». Medium.
- Fathom (2025). Talleres Ashby — gobernanza de la IA y variedad requerida.
- MDPI Systems (2025). «The Viable System Model and the Taxonomy of Organizational Pathologies in the Age of AI».
- Schwaninger, M. (2024). «What is variety engineering and why do we need it?» Systems Research and Behavioral Science.

## Referencias cruzadas

- Gramática: `grammars/sci-cybernetics.ebnf` (líneas 49 a 65, sección MSV)
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Política: `policies/seldon-plan-policy.yaml`
