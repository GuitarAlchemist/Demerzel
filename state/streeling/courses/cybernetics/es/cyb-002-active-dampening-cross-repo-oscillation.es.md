# CYB-002: Mecanismos de amortiguación activa para controlar la oscilación entre repositorios

**Departamento:** Cibernética
**Identificador del módulo:** CYB-002
**Producido por:** Ciclo del Plan Seldon cybernetics-2026-03-23-002
**Creencia:** T (probable), confianza 0,83
**Fecha:** 2026-03-23
**Requisito previo:** CYB-001 (correspondencia MSV — gobernanza de la IA)

## Pregunta de investigación

¿Qué mecanismos de amortiguación activa, procedentes de la cibernética y la teoría de control, pueden evitar la oscilación entre repositorios en un sistema de gobernanza de la IA basado en ficheros?

## Resumen

El protocolo galáctico de Demerzel define hoy formatos y flujos de mensajes (directivas, informes de cumplimiento, paquetes de conocimiento), pero funciona como un sistema de coordinación **en lazo abierto**. Especifica *cómo son* los mensajes, no *cómo* evitar una realimentación oscilante entre los repositorios consumidores (ix, tars, ga). Cinco mecanismos clásicos de la teoría de control —realimentación negativa, histéresis, bandas muertas, limitación de tasa y retroceso exponencial— pueden transformar el protocolo galáctico de una especificación de interfaz pasiva en un coordinador anti-oscilación activo, es decir, el sistema 2 del MSV de Beer.

## El problema de la oscilación

### Qué aspecto tiene una oscilación en gobernanza

La oscilación entre repositorios ocurre cuando los cambios de estado de un repositorio provocan reacciones en otros, que a su vez provocan nuevas reacciones, creando bucles de realimentación amplificadores:

```
ix detecta una carencia → Demerzel emite una directiva → tars se ajusta →
Demerzel detecta una deriva en tars → emite una contradirectiva →
ix se reajusta → Demerzel detecta una deriva en ix → ...
```

Es exactamente el problema de inestabilidad que el sistema 2 del MSV de Beer fue diseñado para prevenir. En el modelo de sistema viable, las unidades operativas del sistema 1 (ix, tars, ga) son semiautónomas, pero no deben desestabilizarse entre sí mediante reacciones descoordinadas.

### Por qué los contratos estáticos no bastan

Los seis tipos de mensaje del protocolo galáctico (directiva, paquete de conocimiento, informe de cumplimiento, instantánea de creencias, resultado de aprendizaje, sobre de sincronización externa) definen *interfaces*, es decir, la forma de los mensajes. Pero una interfaz por sí sola no puede evitar la oscilación. Un termostato con sensor de temperatura (la interfaz) pero sin banda muerta (la amortiguación) se encenderá y apagará sin parar. Del mismo modo, unos contratos de gobernanza sin amortiguación producirán bucles de directiva — cumplimiento — directiva.

## Cinco mecanismos de amortiguación

### 1. Realimentación negativa (corrección en lazo cerrado)

**Teoría de control:** la salida del sistema se devuelve y se resta de la entrada, lo que produce un comportamiento autocorrector que converge hacia una consigna.

**Aplicación a la gobernanza:** toda directiva del protocolo galáctico debería incluir un *estado objetivo*, y todo informe de cumplimiento un *estado medido*. La diferencia (la señal de error) determina si hacen falta más directivas. Si el error disminuye, no se emite ninguna directiva nueva: el sistema está convergiendo.

**Implementación:**
- Las directivas incluyen el campo `target_state` (lo que Demerzel quiere)
- Los informes de cumplimiento incluyen el campo `measured_state` (lo que el repositorio logró)
- Error = `target_state - measured_state`
- Solo se emite una directiva nueva cuando el error *crece* o *se estanca*, nunca cuando *disminuye*

**Correspondencia con el MSV:** esto lleva al protocolo galáctico del lazo abierto (directivas lanzadas sin seguimiento) al lazo cerrado (directivas corregidas por la realimentación de cumplimiento).

### 2. Histéresis (propagación de estado con umbrales distintos)

**Teoría de control:** el sistema tiene umbrales distintos para activarse y desactivarse, lo que crea una holgura de conmutación que impide los cambios rápidos. Un termostato fijado en 20 °C puede encender la calefacción a 19 °C y apagarla a 21 °C: esa holgura de 2 grados es la histéresis.

**Aplicación a la gobernanza:** un cambio de estado en un repositorio solo debería propagarse a los demás al superar un *umbral de significación*, y el umbral de «problema resuelto» debe diferir del de «problema detectado».

**Implementación:**
- Umbral de detección: la confianza en una creencia cae por debajo de 0,5 (dispara una investigación)
- Umbral de resolución: la confianza sube por encima de 0,7 (retira el aviso)
- La holgura de 0,2 evita esto: detectar en 0,49 → corregir a 0,51 → volver a detectar en 0,49 → corregir…
- Se aplica a los cambios del estado de creencias, a las puntuaciones de cumplimiento y a los hallazgos de las auditorías de gobernanza

**Correspondencia con el MSV:** la histéresis da «memoria» al sistema 2: recuerda si el sistema estuvo estable o inestable hace poco y ajusta su sensibilidad en consecuencia.

### 3. Bandas muertas (zonas de tolerancia)

**Teoría de control:** una región alrededor de la consigna donde no se emprende ninguna acción de control. Las desviaciones pequeñas se ignoran, lo que reduce el desgaste de los actuadores y evita correcciones innecesarias.

**Aplicación a la gobernanza:** los cambios de estado menores en los repositorios consumidores no deberían disparar mensajes del protocolo galáctico. Subir una persona de la versión 1.0.0 a la 1.0.1 (parche) no debe provocar una directiva de gobernanza; pasar de 1.0.0 a 2.0.0 (mayor), sí.

**Implementación:**
- Variación de confianza de una creencia < 0,05: sin propagación entre repositorios
- Puntuación de cumplimiento dentro de un margen de ±5 % del objetivo: sin directiva
- Versiones de parche de las personas: sin reacción de gobernanza
- Actualizaciones del estado de conocimiento con menos de 3 entradas nuevas: agrupar en lugar de propagar una a una

**Correspondencia con el MSV:** las bandas muertas reducen la *variedad* de señales que atraviesan el sistema 2 y previenen la sobrecarga de coordinación. Son un atenuador de variedad: filtran el ruido del canal S1 → S2.

### 4. Limitación de tasa (frecuencia de actualización acotada)

**Teoría de control:** el ritmo máximo al que un controlador puede emitir correcciones está acotado, para impedir que reaccione más rápido de lo que el sistema puede responder.

**Aplicación a la gobernanza:** Demerzel no debería emitir más de N directivas por repositorio y ciclo. Los repositorios consumidores no deberían enviar más de M informes de cumplimiento por periodo. Así se evitan los bucles directiva — respuesta a ritmo acelerado.

**Implementación:**
- Número máximo de directivas por repositorio y ciclo PDCA: 3
- Intervalo mínimo entre dos directivas al mismo repositorio: 1 ciclo
- Agrupación de informes de cumplimiento: un único informe agregado por ciclo
- Entrega de paquetes de conocimiento: como máximo 2 por repositorio y ciclo

**Correspondencia con el MSV:** la limitación de tasa acompasa la cadencia de coordinación del sistema 2 con la cadencia operativa del sistema 1. Si el bucle de gobernanza va más rápido de lo que las operaciones pueden responder, las directivas se acumulan y la oscilación se amplifica.

### 5. Retroceso exponencial (enfriamiento adaptativo)

**Teoría de control:** tras varias correcciones fallidas, el controlador aumenta exponencialmente el tiempo de espera antes de reintentar, lo que evita agotar los recursos y da tiempo al sistema para estabilizarse.

**Aplicación a la gobernanza:** si se emite una directiva y no se alcanza el cumplimiento tras un ciclo, esperar 2 ciclos antes de reemitirla. Si el incumplimiento persiste, esperar 4 ciclos. Así se evita que Demerzel hostigue a un repositorio que quizá necesite cambios estructurales, no arreglos rápidos.

**Implementación:**
- Primer incumplimiento: reemitir la directiva en el ciclo siguiente
- Segundo incumplimiento: esperar 2 ciclos y elevar la gravedad
- Tercer incumplimiento: esperar 4 ciclos y escalar a una persona
- Cuarto incumplimiento: detener las directivas automáticas y exigir intervención humana
- Reiniciar el retroceso a cero en cuanto se logre el cumplimiento

**Correspondencia con el MSV:** el retroceso exponencial es un atenuador de variedad en el canal S3 → S1. Impide que el sistema de control abrume a las operaciones con correcciones repetidas que no funcionan.

## Marco de transparencia de la coordinación

El artículo de Springer de 2026 «Coordination transparency: governing distributed agency in AI systems» aporta validación académica a este enfoque mediante cuatro componentes.

### Componente 1: registro de interacciones
Registrar cada mensaje del protocolo galáctico con emisor, receptor, marca de tiempo y huella del contenido. Demerzel ya lo permite en parte mediante el artículo 7 (auditabilidad), pero los registros deben capturar los *patrones de interacción*, no solo los mensajes sueltos.

### Componente 2: supervisión de la coordinación en vivo
Seguir métricas cuantitativas que detecten la oscilación:
- **Índice de convergencia:** ¿las puntuaciones de cumplimiento tienden hacia sus objetivos u oscilan?
- **Índice de oscilación:** frecuencia de pares directiva — contradirectiva dentro de una ventana
- **Deriva de similitud entre políticas:** ¿divergen los repositorios en sus perfiles de cumplimiento?
- **Recuento de cascadas interceptadas:** ¿con qué frecuencia los mecanismos de amortiguación evitan acciones innecesarias?

### Componente 3: puntos de intervención
Ofrecer capacidades de parada, pausa y redirección en la capa de coordinación:
- **Cortacircuitos:** si el índice de oscilación supera un umbral, detener las directivas entre repositorios hasta una revisión humana
- **Limitadores de tasa:** imponer una frecuencia máxima de directivas (véase el mecanismo 4)
- **Puertas de aprobación:** las directivas de alto impacto exigen confirmación humana

### Componente 4: condiciones de contorno
Restringir las topologías de interacción:
- Los repositorios no pueden dirigirse directivas entre sí: toda coordinación pasa por Demerzel
- Profundidad máxima de las cadenas de directivas (impide bucles A → B → C → A)
- Entorno aislado: los cambios de gobernanza experimentales se aplican a un solo repositorio antes de propagarse

## Lazo abierto frente a lazo cerrado

| Aspecto | Hoy (lazo abierto) | Con amortiguación (lazo cerrado) |
|--------|---------------------|-------------------------------|
| Directivas | Lanzadas sin seguimiento | Estado objetivo y corrección del error |
| Cambios de estado | Todos se propagan | Filtrados por banda muerta e histéresis |
| Frecuencia de actualización | Ilimitada | Limitada por ciclo |
| Fallos repetidos | Se reemite la misma directiva | Retroceso exponencial y escalado |
| Detección de oscilación | Ninguna | Índices de convergencia y oscilación |
| Intervención | Solo manual | Cortacircuitos y puertas de aprobación |

## Implicaciones para Demerzel

1. **Enriquecer el protocolo galáctico** — Añadir `target_state` a las directivas y `measured_state` a los informes de cumplimiento, lo que habilita la corrección en lazo cerrado (realimentación negativa).
2. **Definir los parámetros de amortiguación** — Expresar las anchuras de banda muerta, las holguras de histéresis, los límites de tasa y los calendarios de retroceso como parámetros de gobernanza configurables, no como valores fijados en el código.
3. **Añadir supervisión de la oscilación** — Seguir los índices de convergencia y oscilación a lo largo de los ciclos PDCA y almacenarlos en `state/coordination/oscillation-metrics.json`.
4. **Implantar cortacircuitos** — Si el índice de oscilación supera un umbral, detener las directivas automáticas y escalar a una persona. Es el equivalente de un fusible para la gobernanza.
5. **Preservar el atajo algedónico** — Los mecanismos de amortiguación NO deben aplicarse a las señales del canal algedónico (carencia D de CYB-001, ya resuelta mediante `policies/algedonic-channel-policy.yaml`). El atajo de emergencia siempre prevalece sobre la amortiguación de la coordinación.

## Relación con CYB-001

Este curso responde directamente a la **carencia B** de CYB-001: «los contratos del sistema 2 son estáticos, no amortiguan activamente». Los cinco mecanismos transforman el protocolo galáctico de una especificación de interfaz pasiva (lazo abierto) en un coordinador anti-oscilación activo (lazo cerrado), cumpliendo así la función central del sistema 2 en el MSV de Beer.

El canal algedónico (carencia D de CYB-001) se resolvió por separado mediante `policies/algedonic-channel-policy.yaml`. Amortiguación y atajo algedónico son complementarios: la amortiguación ralentiza la coordinación ordinaria para prevenir la oscilación; el canal algedónico sortea toda amortiguación ante emergencias reales.

## Fuentes

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Coordination transparency: governing distributed agency in AI systems. (2026). *AI & Society*, Springer. https://link.springer.com/article/10.1007/s00146-026-02853-w
- Gorelkin, M. (2025). «Stafford Beer's VSM for Building Enterprise Agentic Systems». Medium. https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0
- Fearne, D. (2025). «Applying Stafford Beer's VSM to Create The Autonomous AI Organisation». Medium. https://medium.com/@fearney/applying-stafford-beers-viable-system-model-to-create-the-autonomous-ai-organisation-aaaed39b37e2
- IBM Research. (2025). «Agentic AI Needs a Systems Theory».
- NI. (2025). «PID Theory Explained». https://www.ni.com/en/shop/labview/pid-theory-explained.html
- GeeksforGeeks. (2025). «Feedback Loops in Distributed Systems». https://www.geeksforgeeks.org/system-design/feedback-loops-in-distributed-systems/

## Referencias cruzadas

- Requisito previo: `state/streeling/courses/cybernetics/en/cyb-001-vsm-ai-governance-mapping.md`
- Protocolo: `contracts/galactic-protocol.md`
- Política algedónica: `policies/algedonic-channel-policy.yaml`
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Gramática: `grammars/sci-cybernetics.ebnf`
- Política: `policies/seldon-plan-policy.yaml`
