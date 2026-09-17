# CYB-002: Mecanismos de amortiguación activa para controlar la oscilación entre repositorios

**Departamento:** Cibernética
**ID del módulo:** CYB-002
**Producido por:** ciclo del plan Seldon cybernetics-2026-03-23-002
**Creencia:** T (probable), confianza 0.83
**Fecha:** 2026-03-23
**Requisito previo:** CYB-001 (Correspondencia entre el VSM y la gobernanza de la IA)

## Pregunta de investigación

¿Qué mecanismos de amortiguación activa de la cibernética y la teoría de control pueden evitar la oscilación entre repositorios en un sistema de gobernanza de la IA basado en archivos?

## Resumen

El Galactic Protocol de Demerzel define actualmente formatos y flujos de mensajes (directivas, informes de cumplimiento, paquetes de conocimiento), pero funciona como un sistema de coordinación **en lazo abierto**. Especifica *cómo* son los mensajes, no *cómo* evitar una retroalimentación oscilatoria entre los repositorios consumidores (ix, tars, ga). Cinco mecanismos clásicos de la teoría de control —retroalimentación negativa, histéresis, bandas muertas, limitación de frecuencia y espera exponencial— pueden transformar el Galactic Protocol de una especificación de interfaz pasiva en un Sistema 2 activo (coordinador antioscilación) según el VSM de Beer.

## El problema de la oscilación

### Cómo se ve la oscilación en la gobernanza

La oscilación entre repositorios ocurre cuando los cambios de estado en un repositorio desencadenan reacciones en otros, que a su vez desencadenan nuevas reacciones, creando bucles de retroalimentación que se amplifican:

```
ix detects gap → Demerzel issues directive → tars adjusts →
Demerzel detects tars drift → issues counter-directive →
ix re-adjusts → Demerzel detects ix drift → ...
```

Es el mismo problema de inestabilidad que el Sistema 2 del VSM de Beer se diseñó para evitar. En el modelo de sistema viable, las unidades operativas del Sistema 1 (ix, tars, ga) son semiautónomas, pero no deben desestabilizarse entre sí mediante reacciones no coordinadas.

### Por qué los contratos estáticos no bastan

Los seis tipos de mensaje del Galactic Protocol (directive, knowledge-package, compliance-report, belief-snapshot, learning-outcome, external-sync-envelope) definen *interfaces*: la forma de los mensajes. Pero las interfaces por sí solas no pueden evitar la oscilación. Un termostato con un sensor de temperatura (interfaz) pero sin banda muerta (amortiguación) se encenderá y apagará continuamente. Del mismo modo, los contratos de gobernanza sin amortiguación producirán bucles directiva-cumplimiento-directiva.

## Cinco mecanismos de amortiguación

### 1. Retroalimentación negativa (corrección en lazo cerrado)

**Teoría de control:** La salida de un sistema se realimenta y se resta de la entrada, lo que produce un comportamiento autocorrector que converge hacia un valor de consigna.

**Aplicación a la gobernanza:** Cada directiva del Galactic Protocol debería incluir un *estado objetivo* y cada informe de cumplimiento un *estado medido*. La diferencia (señal de error) determina si hacen falta más directivas. Si el error disminuye, no se emite ninguna directiva nueva: el sistema está convergiendo.

**Implementación:**
- Las directivas incluyen un campo `target_state` (lo que Demerzel quiere)
- Los informes de cumplimiento incluyen un campo `measured_state` (lo que logró el repositorio)
- Error = `target_state - measured_state`
- Solo se emiten directivas nuevas cuando el error *crece* o está *estancado*, no cuando *disminuye*

**Correspondencia con el VSM:** Esto transforma el Galactic Protocol de lazo abierto (directivas de «disparar y olvidar») a lazo cerrado (directivas corregidas por la retroalimentación de cumplimiento).

### 2. Histéresis (propagación de estado condicionada por umbrales)

**Teoría de control:** Un sistema tiene umbrales distintos para la activación y la desactivación, lo que crea una brecha de conmutación que evita los cambios rápidos. Un termostato ajustado a 20C podría encender la calefacción a 19C y apagarla a 21C: la brecha de 2 grados es la histéresis.

**Aplicación a la gobernanza:** Los cambios de estado en un repositorio solo deberían propagarse a los demás cuando crucen un *umbral de relevancia*, y el umbral de «problema resuelto» debería ser distinto del umbral de «problema detectado».

**Implementación:**
- Umbral de detección: la confianza de una creencia baja de 0.5 (desencadena una investigación)
- Umbral de resolución: la confianza de una creencia sube por encima de 0.7 (retira la señal)
- La brecha de 0.2 evita: detectar en 0.49 → corregir a 0.51 → volver a detectar en 0.49 → corregir...
- Se aplica a: cambios de estado de creencia, puntuaciones de cumplimiento, hallazgos de auditoría de gobernanza

**Correspondencia con el VSM:** La histéresis da «memoria» al Sistema 2: recuerda si el sistema estuvo estable o inestable recientemente y ajusta su sensibilidad en consecuencia.

### 3. Bandas muertas (zonas de tolerancia)

**Teoría de control:** Una región alrededor del valor de consigna en la que no se toma ninguna acción de control. Las desviaciones pequeñas se ignoran, lo que reduce el desgaste de los actuadores y evita correcciones innecesarias.

**Aplicación a la gobernanza:** Los cambios de estado menores en los repositorios consumidores no deberían desencadenar mensajes del Galactic Protocol. Un cambio de versión de una persona de 1.0.0 a 1.0.1 (parche) no debería desencadenar una directiva de gobernanza, mientras que de 1.0.0 a 2.0.0 (mayor) sí.

**Implementación:**
- Cambios de confianza de una creencia < 0.05: sin propagación entre repositorios
- Puntuaciones de cumplimiento de políticas dentro de +/-5% del objetivo: sin directiva
- Versiones de parche de personas: sin reacción de gobernanza
- Actualizaciones del estado de conocimiento con < 3 entradas nuevas: agrupar, no propagar individualmente

**Correspondencia con el VSM:** Las bandas muertas reducen la *variedad* de señales que fluyen por el Sistema 2 y evitan la sobrecarga de coordinación. Es un atenuador de variedad: filtra el ruido del canal de S1 a S2.

### 4. Limitación de frecuencia (frecuencia de actualización acotada)

**Teoría de control:** La frecuencia máxima a la que un controlador puede emitir correcciones está acotada, lo que impide que el controlador reaccione más rápido de lo que el sistema puede responder.

**Aplicación a la gobernanza:** Demerzel no debería emitir más de N directivas por repositorio por ciclo. Los repositorios consumidores no deberían enviar más de M informes de cumplimiento por periodo. Esto evita bucles directiva-respuesta en ráfaga.

**Implementación:**
- Máximo de directivas por repositorio por ciclo PDCA: 3
- Intervalo mínimo entre directivas al mismo repositorio: 1 ciclo
- Agrupación de informes de cumplimiento: agregar en un único informe por ciclo
- Entrega de paquetes de conocimiento: máximo 2 por repositorio por ciclo

**Correspondencia con el VSM:** La limitación de frecuencia ajusta la cadencia de coordinación del Sistema 2 a la cadencia operativa del Sistema 1. Si el bucle de gobernanza va más rápido de lo que las operaciones pueden responder, las directivas se acumulan y la oscilación se amplifica.

### 5. Espera exponencial (enfriamiento adaptativo)

**Teoría de control:** Tras correcciones fallidas repetidas, el controlador aumenta exponencialmente el tiempo de espera antes de reintentar, lo que evita agotar los recursos y da tiempo al sistema para estabilizarse.

**Aplicación a la gobernanza:** Si se emite una directiva y no se logra el cumplimiento tras un ciclo, volver a emitirla en el ciclo siguiente. Si sigue sin cumplirse, esperar 2 ciclos, y luego 4. Esto evita que Demerzel machaque a un repositorio que quizá necesite cambios estructurales (no solo arreglos rápidos).

**Implementación:**
- Primer incumplimiento: volver a emitir la directiva en el ciclo siguiente
- Segundo incumplimiento: esperar 2 ciclos, aumentar la gravedad
- Tercer incumplimiento: esperar 4 ciclos, escalar a un humano
- Cuarto incumplimiento: detener las directivas automatizadas, exigir intervención humana
- Restablecer la espera a 0 cuando se logre el cumplimiento

**Correspondencia con el VSM:** La espera exponencial es un atenuador de variedad en el canal de S3 a S1. Evita que el sistema de control abrume a las operaciones con correcciones repetidas que no funcionan.

## Marco de transparencia de la coordinación

El artículo de Springer de 2026 «Coordination transparency: governing distributed agency in AI systems» aporta una validación académica a este enfoque mediante cuatro componentes:

### Componente 1: registro de interacciones
Registrar cada mensaje del Galactic Protocol con emisor, receptor, marca de tiempo y hash del contenido. Demerzel ya lo admite en parte mediante el artículo 7 (Auditabilidad), pero los registros deben capturar *patrones de interacción*, no solo mensajes individuales.

### Componente 2: monitorización de la coordinación en vivo
Seguir métricas cuantitativas que detecten la oscilación:
- **Índice de convergencia:** ¿Las puntuaciones de cumplimiento tienden hacia los objetivos u oscilan?
- **Índice de oscilación:** Frecuencia de pares directiva-contradirectiva dentro de una ventana
- **Deriva de similitud de políticas:** ¿Divergen los repositorios en sus perfiles de cumplimiento de la gobernanza?
- **Recuento de cascadas interrumpidas:** ¿Con qué frecuencia los mecanismos de amortiguación evitan acciones innecesarias?

### Componente 3: puntos de intervención
Ofrecer capacidades de detener, pausar y redirigir en la capa de coordinación:
- **Cortacircuitos:** Si el índice de oscilación supera un umbral, detener las directivas entre repositorios hasta una revisión humana
- **Limitadores de frecuencia:** Imponer una frecuencia máxima de directivas (ver el mecanismo 4)
- **Puertas de aprobación:** Las directivas de alto impacto requieren confirmación humana

### Componente 4: condiciones de contorno
Restringir las topologías de interacción:
- Los repositorios no pueden desencadenar directivas directamente entre sí (toda la coordinación pasa por Demerzel)
- Profundidad máxima de las cadenas de directivas (evita bucles A→B→C→A)
- Entorno aislado: los cambios de gobernanza experimentales se aplican a un solo repositorio antes de propagarse

## Comparación entre lazo abierto y lazo cerrado

| Aspecto | Actual (lazo abierto) | Con amortiguación (lazo cerrado) |
|--------|---------------------|-------------------------------|
| Directivas | Disparar y olvidar | Estado objetivo + corrección del error |
| Cambios de estado | Todos propagados | Filtrados por banda muerta + histéresis |
| Frecuencia de actualización | Ilimitada | Limitada por ciclo |
| Fallos repetidos | Misma directiva reemitida | Espera exponencial + escalado |
| Detección de oscilación | Ninguna | Índices de convergencia/oscilación |
| Intervención | Solo manual | Cortacircuitos + puertas de aprobación |

## Implicaciones para Demerzel

1. **Mejorar el Galactic Protocol**: añadir `target_state` a las directivas y `measured_state` a los informes de cumplimiento, para permitir la corrección en lazo cerrado (retroalimentación negativa).
2. **Definir los parámetros de amortiguación**: especificar anchos de banda muerta, brechas de histéresis, límites de frecuencia y calendarios de espera como parámetros de gobernanza configurables, no como valores fijos en el código.
3. **Añadir monitorización de la oscilación**: seguir los índices de convergencia y oscilación a lo largo de los ciclos PDCA. Guardarlos en `state/coordination/oscillation-metrics.json`.
4. **Implementar cortacircuitos**: si el índice de oscilación supera un umbral, detener las directivas automatizadas y escalar a un humano. Es el equivalente en gobernanza de un fusible.
5. **Preservar el bypass algedónico**: los mecanismos de amortiguación NO deben aplicarse a las señales del canal algedónico (brecha D de CYB-001, ya resuelta mediante `policies/algedonic-channel-policy.yaml`). El bypass de emergencia siempre prevalece sobre la amortiguación de la coordinación.

## Relación con CYB-001

Este curso aborda directamente la **brecha B** de CYB-001: «Los contratos del Sistema 2 son estáticos, no amortiguan activamente». Los cinco mecanismos transforman el Galactic Protocol de una especificación de interfaz pasiva (lazo abierto) en un coordinador antioscilación activo (lazo cerrado), cumpliendo la función central del Sistema 2 en el VSM de Beer.

El canal algedónico (brecha D de CYB-001) se resolvió por separado mediante `policies/algedonic-channel-policy.yaml`. La amortiguación y el bypass algedónico son complementarios: la amortiguación ralentiza la coordinación normal para evitar la oscilación; el canal algedónico sortea toda amortiguación en las emergencias reales.

## Fuentes

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Coordination transparency: governing distributed agency in AI systems. (2026). *AI & Society*, Springer. https://link.springer.com/article/10.1007/s00146-026-02853-w
- Gorelkin, M. (2025). "Stafford Beer's VSM for Building Enterprise Agentic Systems." Medium. https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0
- Fearne, D. (2025). "Applying Stafford Beer's VSM to Create The Autonomous AI Organisation." Medium. https://medium.com/@fearney/applying-stafford-beers-viable-system-model-to-create-the-autonomous-ai-organisation-aaaed39b37e2
- IBM Research. (2025). "Agentic AI Needs a Systems Theory."
- NI. (2025). "PID Theory Explained." https://www.ni.com/en/shop/labview/pid-theory-explained.html
- GeeksforGeeks. (2025). "Feedback Loops in Distributed Systems." https://www.geeksforgeeks.org/system-design/feedback-loops-in-distributed-systems/

## Referencias cruzadas

- Requisito previo: `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
- Protocolo: `contracts/galactic-protocol.md`
- Política algedónica: `policies/algedonic-channel-policy.yaml`
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Gramática: `grammars/sci-cybernetics.ebnf`
- Política: `policies/seldon-plan-policy.yaml`
