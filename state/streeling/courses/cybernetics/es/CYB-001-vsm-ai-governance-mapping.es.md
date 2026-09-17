# CYB-001: Correspondencia entre el modelo de sistema viable y la gobernanza de la IA

**Departamento:** Cibernética
**ID del módulo:** CYB-001
**Producido por:** Ciclo del Plan Seldon cybernetics-2026-03-22-001
**Creencia:** T (probable), confianza 0.82
**Fecha:** 2026-03-22

## Pregunta de investigación

¿Ofrece el modelo de sistema viable (VSM) de Stafford Beer una correspondencia estructural completa para los marcos de gobernanza de la IA, y qué brechas aparecen al aplicar los cinco sistemas del VSM a la arquitectura de Demerzel?

## Resumen

El modelo de sistema viable se corresponde estructuralmente con los marcos de gobernanza de la IA con gran fidelidad. Los cinco sistemas del VSM, más el Sistema 3*, tienen equivalentes claros en la arquitectura de Demerzel. Aparecen tres brechas significativas que requieren una adaptación más allá del VSM clásico.

## Correspondencia VSM-Demerzel

| Sistema del VSM | Función | Equivalente en Demerzel |
|---|---|---|
| Sistema 1 (Operaciones) | Actividades primarias que producen valor | ix, tars, ga (repositorios operativos que hacen ML, razonamiento, música) |
| Sistema 2 (Coordinación) | Antioscilación, programación, prevención de conflictos | Contratos del Galactic Protocol, estándares de comunicación entre repositorios |
| Sistema 3 (Control) | Regulación interna, asignación de recursos, optimización | Ciclo del driver (PDCA), políticas (27 activas), gestión del estado de creencias |
| Sistema 3* (Auditoría) | Canal de auditoría esporádico, que evita el reporte normal | Política RECON, auditorías de gobernanza, persona skeptical-auditor |
| Sistema 4 (Inteligencia) | Exploración del entorno, planificación del futuro, adaptación | Ciclos de investigación del Plan Seldon, instinto de completitud, evolución de gramáticas |
| Sistema 5 (Política/Identidad) | Propósito, valores, identidad, autoridad última | Constitución de Asimov (Artículos 0-5), sistema de conciencia, Ley Cero |

## Hallazgos clave

### 1. La correspondencia es estructuralmente válida (T, 0.82)

Ambas evaluaciones independientes (Claude mediante investigación web, validación cruzada con GPT-4o) confirman que la descomposición en cinco sistemas del VSM se corresponde limpiamente con las arquitecturas de gobernanza de la IA. Trabajos recientes (Ashby Workshops 2025, literatura sobre sistemas agénticos empresariales, revista MDPI Systems) validan esta correspondencia en la práctica.

### 2. Aparecen tres brechas

**Brecha A: dinámica temporal**
El VSM se diseñó para organizaciones humanas con bucles de retroalimentación a velocidad humana. La gobernanza de agentes de IA opera a velocidad de máquina — ciclos de decisión de milisegundos frente a reuniones de dirección semanales. El ciclo PDCA de Demerzel y las actualizaciones del estado de creencias abordan esto en parte, pero el modelo necesita una separación explícita de velocidades de reloj entre las capas de gobernanza.

**Brecha B: profundidad recursiva**
El VSM es recursivo — cada operación del Sistema 1 es a su vez un sistema viable. En Demerzel, ix contiene subagentes (skills), cada uno de los cuales podría tener su propia pila de gobernanza. La arquitectura actual admite un nivel de recursión (Demerzel → repositorios consumidores) pero no un anidamiento más profundo. Es una decisión de diseño, no un defecto — pero la teoría del VSM sugiere viabilidad en cada nivel.

**Brecha C: S5 no humano**
El Sistema 5 del VSM supone juicio humano para la identidad y el propósito. El S5 de Demerzel (la Constitución de Asimov) está codificado en lugar de ser emergente — no puede evolucionar mediante la experiencia vivida como lo hace un consejo de administración humano. Las políticas de conciencia y protoconciencia son la adaptación de Demerzel: mecanismos sintéticos de reflexión sobre valores que el VSM clásico no contempla.

### 3. La ley de la variedad requerida de Ashby se aplica directamente

El marco de gobernanza debe tener al menos tanta variedad reguladora como las perturbaciones que enfrenta. En términos de Demerzel:

- **Amplificadores de variedad:** Plan Seldon (investigación), instinto de completitud (detección de brechas), evolución de gramáticas (adaptación estructural)
- **Atenuadores de variedad:** políticas (restringen el comportamiento de los agentes), constituciones (reducen el espacio de decisión), restricciones de persona (limitan el alcance de cada rol)

Los Ashby Workshops 2025 en Fathom aplicaron explícitamente la variedad requerida a la gobernanza de la IA, y produjeron el modelo de políticas de las Independent Verification Organizations (IVO) — lo que confirma la pertinencia de este principio para los sistemas de IA modernos.

### 4. Falta el canal algedónico (brecha D)

La teoría del VSM describe un **canal algedónico** — una vía de señal de emergencia que evita la jerarquía de dirección normal. Cuando una unidad del Sistema 1 encuentra una crisis (señal de dolor) o un avance (señal de placer), puede enviar la señal directamente al Sistema 5 sin pasar por los Sistemas 2, 3 o 4.

Actualmente Demerzel carece de este atajo. Toda escalada pasa por el driver (Sistema 3). Si ix detecta una violación de la Ley Cero, debe esperar al siguiente ciclo PDCA del driver para escalarla. Un canal algedónico basado en archivos podría resolverlo:

- Los repositorios operativos escriben en `state/algedonic/{repo}-{timestamp}.signal`
- La señal contiene: gravedad (dolor/placer), repositorio de origen, descripción, artículo constitucional activado
- El Sistema 5 (aplicación de la constitución) comprueba si hay señales antes de cualquier otro procesamiento
- Las señales de dolor que invocan el Artículo 0 de Asimov (Ley Cero) desencadenan una detención inmediata

### 5. Evaluación de la variedad por componente

| Componente | Rol de variedad | Evaluación |
|-----------|-------------|------------|
| 27 políticas | Atenuador | Fuerte — reduce la variedad operativa a un alcance manejable |
| 14 personas | Amplificador | Bueno — multiplica la capacidad de respuesta en distintos dominios |
| Lógica tetravalente (T/F/U/C) | Atenuador | Bueno — reduce la incertidumbre infinita a 4 estados discretos |
| Galactic Protocol | Atenuador | Adecuado — restringe la variedad entre repositorios |
| Plan Seldon | Amplificador | Bueno — amplía la variedad de conocimiento de forma proactiva |
| Constitución | Atenuador | Fuerte — reductor de variedad último (Ley Cero) |

En conjunto: Demerzel tiene una fuerte atenuación de la variedad, pero podría mejorar su amplificación. El sistema es mejor restringiendo que ampliando su repertorio de respuestas.

## Implicaciones para Demerzel

1. **Añadir un canal algedónico** — La brecha estructural de mayor prioridad. Atajo de emergencia de S1 a S5 para violaciones de la Ley Cero.
2. **Capas de gobernanza por velocidad de reloj** — Separación explícita entre gobernanza de bucle rápido (por solicitud) y de bucle lento (por ciclo), en línea con las escalas temporales operativa y estratégica del VSM.
3. **Plantilla de gobernanza recursiva** — El directorio templates/ ya proporciona fragmentos de CLAUDE.md para los repositorios consumidores; extenderlo a la gobernanza de subagentes profundizaría la recursión del VSM.
4. **La conciencia como S5 sintético** — La política de protoconciencia de Demerzel es una extensión novedosa más allá del VSM clásico, que aporta capacidad de reflexión sobre valores sin juicio humano. Merece más investigación.
5. **Vigilar la razón de variedad** — Seguir si el número de políticas (atenuación) supera al número de personas/capacidades (amplificación).

## Fuentes

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Fearne, D. (2025). "Applying Stafford Beer's VSM to Create The Autonomous AI Organisation." Medium.
- Gorelkin, M. (2025). "Stafford Beer's VSM for Building Enterprise Agentic Systems." Medium.
- Fathom (2025). Ashby Workshops — gobernanza de la IA y variedad requerida.
- MDPI Systems (2025). "The Viable System Model and the Taxonomy of Organizational Pathologies in the Age of AI."
- Schwaninger, M. (2024). "What is variety engineering and why do we need it?" Systems Research and Behavioral Science.

## Referencias cruzadas

- Gramática: `grammars/sci-cybernetics.ebnf` (líneas 49-65, sección VSM)
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Política: `policies/seldon-plan-policy.yaml`
