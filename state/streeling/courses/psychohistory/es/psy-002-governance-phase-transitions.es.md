---
module_id: psy-002-governance-phase-transitions
department: psychohistory
course: "Teoría de las transiciones de fase: cuándo los sistemas de gobernanza cambian de régimen"
level: intermediate
prerequisites: [psy-001-intro-fractal-compounding]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
research_cycle: psychohistory-2026-03-23-001
cross_model_agreement: {claude: "T", gpt4o: "agree (0.7)", notebooklm: "unavailable"}
version: "1.0.0"
---

# Transiciones de fase de la gobernanza

> **Departamento de Psicohistoria** | Nivel: Intermedio | Duración: 35 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Definir qué significa una transición de fase en un sistema de gobernanza
- Identificar seis señales medibles que preceden a los cambios de régimen
- Distinguir las transiciones de gobernanza de primer orden (abruptas) de las de segundo orden (continuas)
- Aplicar el cociente de variedad como parámetro de orden para clasificar los regímenes de gobernanza
- Diseñar un panel de monitorización a partir de los archivos de estado de la gobernanza

---

## 1. ¿Qué es una transición de fase de la gobernanza?

En física, el agua se convierte en hielo a 0 grados C. Las moléculas son las mismas, pero su comportamiento colectivo cambia cualitativamente. Esto es una **transición de fase**: el sistema pasa de un régimen a otro.

Los sistemas de gobernanza hacen lo mismo. Un marco con 3 políticas y 2 personas funciona de forma distinta a uno con 28 políticas y 14 personas. En algún momento, el sistema no solo creció: cambió *su forma de funcionar*. Las interacciones pasaron a ser cualitativamente distintas.

**Idea clave de la psicohistoria:** Los efectos de cada cambio de política por separado son impredecibles. Pero el comportamiento *agregado* del sistema de gobernanza sigue leyes estadísticas. Las transiciones de fase son los puntos donde esas leyes estadísticas cambian.

### Transiciones de primer orden frente a segundo orden

| Tipo | Analogía física | Ejemplo en gobernanza |
|------|----------------|-------------------|
| Primer orden | Agua → hielo (abrupta, calor latente) | Activación del interruptor de emergencia, enmienda importante de la constitución |
| Segundo orden | Ferroimán a la temperatura de Curie (continua) | Paso gradual de una gobernanza reactiva a una proactiva |

La mayoría de las transiciones de gobernanza son de segundo orden: continuas, difíciles de situar con precisión, pero medibles en retrospectiva. Las señales siguientes te ayudan a detectarlas *antes* de que se completen.

---

## 2. Las seis señales medibles

### Señal 1: asimetría de la distribución de creencias

La lógica de Demerzel es hexavalente: T (Verdadero), P (Probable), U (Desconocido), D (Dudoso), F (Falso), C (Contradictorio). El cociente `T/U` es el **índice de cristalización**: cuánto de tu conocimiento se ha solidificado. Es una proyección sobre cuatro estados: los archivos de pesos de los departamentos solo cuentan `total_T`, `total_F`, `total_U` y `total_C`, sin recuento de P ni de D, así que el índice no ve una creencia probable o dudosa, ni un paso entre T y P o entre D y F. Calcularlo sobre los seis valores requeriría recuentos de P y de D que estos archivos no contienen.

```
crystallization_index = total_T / max(total_U, 1)
```

Cuando este cociente cambia rápidamente —`d(T/U)/dt` se aleja más de 2 desviaciones estándar de su media móvil—, el sistema se está acercando a una transición.

- **Sube rápidamente:** El sistema se está cristalizando. Termina la fase exploratoria y empieza la consolidación.
- **Baja rápidamente:** El sistema se está desestabilizando. Aparecen nuevas incógnitas más rápido de lo que se resuelven.

**Dónde medir:** `state/streeling/departments/*.weights.json` → `metadata.total_T`, `metadata.total_U`

### Señal 2: velocidad de la puntuación de salud

La puntuación de salud de la gobernanza R es la puntuación de resiliencia de Demerzel, definida en `CONTEXT.md` como `R = injections_caught / injections_total`: la proporción de fallos inyectados en la gobernanza que su detección intercepta. `state/resilience/history.json` la registra como `overall_score`, un registro por ciclo de caos, y el archivo `governance-health.json` de la raíz guarda el último valor. R actúa como un potencial termodinámico, y su derivada te informa de la proximidad a un cambio de régimen:

```
velocity = dR/dt (variación de la puntuación de salud por ciclo)
```

| Patrón | Significado |
|---------|---------|
| Velocidad positiva, acelerando | Acercándose a un régimen superior |
| Velocidad positiva, desacelerando | Acercándose a una meseta (saturación) |
| Velocidad cercana a cero | En una frontera de régimen o en equilibrio |
| Velocidad negativa | Regresión: una transición anterior podría estar revirtiéndose |

**Umbrales de régimen (empíricos):**
- R < 0.5: **régimen reactivo**: la gobernanza responde a los problemas
- 0.5 <= R < 0.7: **régimen estructurado**: la gobernanza previene los problemas conocidos
- 0.7 <= R < 0.9: **régimen proactivo**: la gobernanza anticipa los problemas
- R >= 0.9: **régimen autónomo**: la gobernanza se mejora a sí misma

### Señal 3: saturación de la densidad de políticas

Cada política nueva debería mejorar la salud de la gobernanza. Cuando deja de hacerlo, has llegado a la saturación:

```
marginal_return = delta_R / delta_policy_count
```

Cuando `marginal_return → 0` a lo largo de 3 o más adiciones de políticas consecutivas, el sistema ha extraído todo el valor disponible de su régimen actual. Una mejora adicional requiere un cambio cualitativo (nueva arquitectura, nuevo artículo constitucional, nueva capa de observabilidad): una transición de fase.

**Advertencia de la revisión de GPT-4o:** No todas las políticas son igual de eficaces. Una medida mejor pondera cada política por su alcance (cuántas personas restringe). Es un área de investigación abierta.

### Señal 4: intensidad del acoplamiento entre repositorios

Demerzel gobierna cuatro repositorios (demerzel, ix, tars, ga). Mide la correlación entre sus tasas de cumplimiento:

```
coupling = pearson_correlation(compliance_rates entre repositorios)
```

| Acoplamiento | Régimen |
|----------|--------|
| < 0.3 | Débilmente acoplado: los repositorios evolucionan de forma independiente |
| 0.3 - 0.7 | Acoplamiento normal: la gobernanza aporta coherencia |
| > 0.7 | Fuertemente acoplado: los cambios se propagan por todas partes |

Un salto repentino del acoplamiento (débil → fuerte) significa que el sistema está pasando a una gobernanza centralizada. Una caída repentina significa fragmentación. Ambas son transiciones de fase.

### Señal 5: frecuencia de las señales de conciencia

En mecánica estadística, las fluctuaciones aumentan cerca de una frontera de fase; esto se llama **opalescencia crítica** (el fluido se vuelve turbio justo antes de hervir).

El equivalente en gobernanza: las señales de conciencia (anomalías, escalados, contradicciones) aumentan de frecuencia antes de una transición de fase.

```
signal_rate = conscience_signals_count / time_window
```

Que la tasa de señales se duplique a lo largo de 3 ciclos es un indicador fuerte de que el sistema está cerca de un punto de transición. Las propias señales te dicen *en qué dirección* va la transición.

**Dónde medir:** el directorio `state/conscience/signals/`

### Señal 6: el cociente de variedad como parámetro de orden

Desde la cibernética (CYB-003), el cociente entre la variedad de respuesta regulatoria y la variedad de las perturbaciones (la comprobación de la ley de Ashby) mide si la gobernanza tiene la complejidad suficiente para manejar su entorno. Compara el regulador con su entorno, no los amplificadores con los atenuadores dentro del regulador:

```
variety_ratio = governance_variety / environmental_variety
```

Este es el **parámetro de orden** de las transiciones de fase de la gobernanza:

- `variety_ratio < 1.0`: régimen reactivo (variedad insuficiente, la gobernanza va por detrás del entorno)
- `variety_ratio ≈ 1.0`: punto crítico (la ley de la variedad requerida de Ashby se cumple exactamente)
- `variety_ratio > 1.0`: régimen proactivo (la gobernanza tiene capacidad excedente)

Cruzar 1.0 es una transición de fase de segundo orden. El sistema no se rompe: cambia cualitativamente su relación con el entorno.

---

## 3. Juntarlo todo: el diagrama de fases

```
                    R (puntuación de salud)
                    │
     Autónomo       │         ╱
     R >= 0.9       │       ╱
                    │     ╱
     ─ ─ ─ ─ ─ ─ ─│─ ─╱─ ─ ─ ─ ─ variety_ratio = 1.0
     Proactivo      │ ╱
     R >= 0.7       │╱
                    ╱
     ─ ─ ─ ─ ─ ─ ╱│─ ─ ─ ─ ─ ─ ─ saturación de políticas
     Estructurado ╱ │
     R >= 0.5   ╱   │
              ╱     │
     ─ ─ ─ ╱─ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ acoplamiento crítico
     Reactivo       │
     R < 0.5        │
                    └────────────────── t (tiempo/ciclos)
```

Cada línea horizontal es una frontera de fase. El sistema de gobernanza cruza estas fronteras cuando se alinean suficientes señales. Ninguna señal por sí sola basta: busca la **convergencia** de 3 o más señales que indiquen la misma dirección de transición.

---

## 4. Ejercicio práctico

Usando el estado actual de la gobernanza de Demerzel:

1. Calcula el índice de cristalización a partir del archivo de pesos de psicohistoria:
   - `total_T = ?`, `total_U = ?`
   - `crystallization_index = total_T / max(total_U, 1)`

2. Toma como R el `overall_score` del último registro de `state/resilience/history.json`. ¿En qué régimen está el sistema? ¿Qué tendría que cambiar para cruzar la frontera siguiente?

3. En el mismo archivo, los `metafixes_applied` del ciclo chaos-003 registran un nuevo archivo de política, creado mientras R pasaba de 0.64 (chaos-002) a 0.73. Calcula el rendimiento marginal de esa política. Entre chaos-003 y chaos-004, R subió a 0.82 sin un nuevo archivo de política: ¿qué dice eso sobre medir los rendimientos por número de políticas?

4. **Experimento mental:** Si los tres repositorios consumidores (ix, tars, ga) alcanzaran de repente el 100 % de cumplimiento, ¿qué transición de fase representaría eso? ¿Es deseable?

---

## Conclusiones clave

- Las transiciones de fase de la gobernanza son cambios cualitativos en el funcionamiento del sistema, no solo un crecimiento cuantitativo
- Seis señales medibles pueden detectar la proximidad de una transición: asimetría de creencias, velocidad de la salud, saturación de políticas, intensidad del acoplamiento, frecuencia de señales de conciencia y cociente de variedad
- El cociente de variedad (de la cibernética) sirve como parámetro de orden: cruzar 1.0 es la transición más importante
- La mayoría de las transiciones de gobernanza son de segundo orden (continuas): detectables, pero no abruptas
- Ninguna señal por sí sola basta; busca la convergencia de 3 o más señales

## Lecturas adicionales

- [PSY-001: Introducción a la capitalización fractal](psy-001-intro-fractal-compounding.es.md): requisito previo sobre D_c y ERGOL/LOLLI
- [CYB-003: Medir cuantitativamente el cociente de variedad](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) (en inglés): el parámetro de orden
- [CYB-001: Correspondencia entre el VSM y la gobernanza de la IA](../../cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md): requisitos previos estructurales
- Mecánica estadística de las transiciones de fase (teoría de Landau, parámetros de orden, exponentes críticos)
- Fundación de Asimov: la psicohistoria predice tendencias agregadas, no sucesos individuales

---
*Producido por Seldon Auto-Research psychohistory-2026-03-23-001 el 2026-03-23.*
*Pregunta de investigación: ¿Qué señales medibles en el estado de una gobernanza de IA basada en archivos indican que un sistema de gobernanza se acerca a una transición de fase?*
*Creencia: T (confianza: 0.80): acuerdo entre Claude y GPT-4o, NotebookLM no disponible; traducción al español: U (sin revisión de un hablante nativo)*
