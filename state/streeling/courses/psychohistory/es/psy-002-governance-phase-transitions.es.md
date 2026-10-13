---
module_id: psy-002-governance-phase-transitions
department: psychohistory
course: "Poner a prueba la analogía de las transiciones de fase en la gobernanza"
level: intermediate
prerequisites: [psy-001-intro-fractal-compounding]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
research_cycle: psychohistory-2026-03-23-001
version: "1.1.0"
---

# Poner a prueba los cambios de régimen en la gobernanza

> **Departamento de Psicohistoria** | Nivel: Intermedio | Duración: 35 minutos | Estado: borrador revisado; revisión temática y prueba con alumnado pendientes

## Objetivos

Al terminar esta lección, serás capaz de:
- Distinguir una transición de fase física de una analogía propuesta para la gobernanza
- Identificar cinco indicadores propuestos y una hipótesis no medida sobre la variedad para investigar cambios de régimen
- Indicar qué pruebas harían falta para llamar abrupto, continuo o predecible a un cambio de gobernanza
- Explicar qué pruebas harían falta antes de probar la variedad requerida como señal de transición de gobernanza
- Diseñar un panel de monitorización a partir de los archivos de estado de la gobernanza

---

## 1. La analogía y sus límites

En física, el agua se convierte en hielo a 0 grados C. Las moléculas son las mismas, pero su comportamiento colectivo cambia cualitativamente. Esto es una **transición de fase**: el sistema pasa de un régimen a otro.

Para Demerzel, «transición de fase» es una analogía que debe ponerse a prueba, no una ley observada. Un inventario mayor puede cambiar el trabajo, pero el número de archivos no demuestra un cambio cualitativo ni predice cuándo ocurrirá. Una prueba definiría el comportamiento estudiado, fijaría observaciones antes y después de un cambio y compararía otras explicaciones.

### Transiciones de primer orden frente a segundo orden

| Tipo | Analogía física | Ejemplo en gobernanza |
|------|----------------|-------------------|
| Primer orden | Agua → hielo (abrupta, calor latente) | Activación del interruptor de emergencia como **analogía** de un cambio brusco |
| Segundo orden | Ferroimán a la temperatura de Curie (continua) | Cambio gradual del trabajo como **analogía**; no se ha medido ningún punto crítico |

Aquí no se ha demostrado que un cambio de gobernanza tenga la estructura de una transición de fase física. Los indicadores siguientes sirven para investigar; su capacidad predictiva no se ha validado con transiciones anteriores.

---

## 2. Cinco indicadores propuestos y una medición pendiente

### Señal 1: asimetría de la distribución de creencias

La lógica de Demerzel es hexavalente: T (Verdadero), P (Probable), U (Desconocido), D (Dudoso), F (Falso), C (Contradictorio). El cociente `T/U` es el **índice de cristalización**: cuánto de tu conocimiento se ha solidificado. Es una proyección sobre cuatro estados: los archivos de pesos de los departamentos solo cuentan `total_T`, `total_F`, `total_U` y `total_C`, sin recuento de P ni de D, así que el índice no ve una creencia probable o dudosa, ni un paso entre T y P o entre D y F. Calcularlo sobre los seis valores requeriría recuentos de P y de D que estos archivos no contienen.

```
crystallization_index = total_T / max(total_U, 1)
```

Si este cociente se aleja más de dos desviaciones estándar históricas, examina los recuentos y cómo se registraron. El umbral ilustra una razón para investigar, no un predictor validado; con pocos ciclos, la desviación estándar puede ser inestable.

- **Sube rápidamente:** Se registran más T respecto de U; comprueba cambios de clasificación y cobertura.
- **Baja rápidamente:** Se registran más U respecto de T; comprueba si entraron temas nuevos.

**Dónde medir:** `state/streeling/departments/*.weights.json` → `metadata.total_T`, `metadata.total_U`

### Señal 2: velocidad de la puntuación de salud

La puntuación R de Demerzel se define en `CONTEXT.md` como `R = injections_caught / injections_total`: la proporción de fallos inyectados que detecta el sistema. `state/resilience/history.json` registra `overall_score` por ciclo de caos, y `governance-health.json` guarda el último valor. Una variación de R describe esas pruebas; no es un potencial termodinámico ni mide la cercanía a una frontera de régimen:

```
velocity = dR/dt (variación de la puntuación de salud por ciclo)
```

| Patrón | Significado |
|---------|---------|
| Velocidad positiva, acelerando | La puntuación declarada subió más rápido; examinar cambios en las pruebas |
| Velocidad positiva, desacelerando | La puntuación declarada siguió subiendo, más despacio |
| Velocidad cercana a cero | La puntuación declarada apenas cambió; no demuestra equilibrio |
| Velocidad negativa | La puntuación declarada bajó; examinar casos y detección |

**Bandas ilustrativas para el panel, no umbrales empíricos de régimen:** `<0,5`, `0,5–<0,7`, `0,7–<0,9` y `≥0,9` permiten agrupar valores mostrados de R. No demuestran comportamientos reactivos, estructurados, proactivos ni autónomos. Esas interpretaciones necesitan resultados medidos por separado y casos de inyección estables.

### Señal 3: saturación de la densidad de políticas

Una política nueva puede ayudar, no cambiar nada o añadir trabajo. Un cálculo descriptivo de cambio por archivo es:

```
marginal_return = delta_R / delta_policy_count
```

Tres valores cercanos a cero no demuestran saturación. Las políticas pueden cambiar junto con las pruebas, su aplicación, las personas u otras políticas, así que `delta_R / delta_policy_count` no aísla el efecto causal de una política. Compara casos de inyección emparejados y registra los cambios simultáneos antes de decidir si hace falta otro diseño.

Ponderar por el número de personas restringidas seguiría midiendo el alcance declarado, no la eficacia. Podría ser un campo descriptivo, no una medida validada del rendimiento.

### Señal 4: intensidad del acoplamiento entre repositorios

Demerzel gobierna cuatro repositorios (demerzel, ix, tars, ga). Registra la tasa de cumplimiento de cada repositorio en cada ciclo y, sobre una ventana de los últimos W ciclos, promedia los valores absolutos de las correlaciones de Pearson de los seis pares de repositorios (un solo ciclo da una tasa por repositorio, de la que no puede calcularse ninguna correlación). Toma W de al menos 30 ciclos, el mismo en todas las ventanas que compares: con W = 2 toda correlación vale exactamente ±1, y en ventanas cortas el azar por sí solo da valores grandes, ya que para dos repositorios independientes la esperanza de |r| es de unos 0.8/√(W − 1), 0.27 con W = 10 y 0.15 con W = 30, frente al umbral de 0.3 de abajo. Toma valores absolutos porque dos repositorios que evolucionan en sentidos opuestos, con una correlación cercana a −1, están tan acoplados como dos que evolucionan juntos, y las correlaciones de signo opuesto se anularían en una media con signo. Una serie constante, como la de un repositorio que se mantiene al 100 %, no tiene correlación con nada: deja fuera sus pares y compara dos ventanas solo sobre los pares definidos en ambas. Una media sobre otro conjunto de pares mide otra cosa, y descartar pares débiles basta para elevarla hasta el régimen fuertemente acoplado. Si no queda ningún par, el acoplamiento está indefinido para la ventana:

```
coupling = mean_{i<j} |pearson_correlation(rates_i[W], rates_j[W])|
```

| Acoplamiento | Régimen |
|----------|--------|
| < 0,3 | Baja correlación absoluta observada en esta ventana |
| 0,3 - 0,7 | Banda intermedia ilustrativa; buscar causas comunes |
| > 0,7 | Alta correlación absoluta observada; no demuestra propagación |

Un salto significa que las series registradas se correlacionaron más en la ventana elegida; no demuestra acoplamiento causal. La media descarta los signos: dos repositorios que mejoran mientras otros dos empeoran pueden dar `|r| = 1` en cada par. Examina las correlaciones con signo y los cambios comunes antes de proponer una explicación. Un cambio de correlación no demuestra por sí solo una transición de fase.

### Señal 5: frecuencia de las señales de conciencia

En mecánica estadística, las fluctuaciones crecen sin límite al acercarse un sistema a un punto crítico, donde la transición es continua (de segundo orden). Cerca del punto crítico líquido–gas esto se manifiesta como **opalescencia crítica**: las fluctuaciones de densidad alcanzan la escala de la longitud de onda de la luz y el fluido se vuelve lechoso. La ebullición ordinaria, una transición de primer orden, no tiene tal señal previa.

La idea de que cambie la tasa de anomalías o escalados antes de ciertos cambios de gobernanza es una hipótesis. Esta lección no cuenta con una serie temporal que la pruebe. Un interruptor de emergencia es un evento administrativo; llamarlo «de primer orden» es una metáfora, no una clasificación física medida.

```
signal_rate = conscience_signals_count / time_window
```

Que la tasa se duplique en 3 ciclos invita a examinar los eventos y su denominador. No se ha validado ningún umbral ni dirección de transición para este indicador.

**Dónde medir:** el directorio `state/conscience/signals/`

### Señal 6: la variedad requerida, una propuesta sin validar

La revisión de [CYB-003](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) retira su antiguo cociente basado en el número de políticas y personas. Contar las categorías de respuestas y perturbaciones de un ciclo sería reproducible, pero su cociente no diría qué respuesta funciona para cada perturbación. Aquí no se ha medido ninguna serie que empareje perturbación → respuesta → resultado. Por tanto, **aún no hay señal operativa de variedad ni frontera de régimen en 1,0** que se pueda trazar.

Un experimento útil definiría de antemano las clases de perturbación, las respuestas permitidas y los resultados aceptables, y conservaría cada evento emparejado durante varios ciclos. Habría que comparar los éxitos comprobados de forma independiente y los casos sin resolver antes de interpretar una medida de información. La idea de un parámetro de orden para transiciones de gobernanza sigue siendo una hipótesis, no un resultado de CYB-003.

---

## 3. Comparar las pruebas antes de nombrar un régimen

| Cantidad registrada | Comparación útil | Prueba pendiente |
|---|---|---|
| R por ciclo de caos | Comparar casos emparejados de inyección de fallos | Conjunto estable y resultados comprobados de forma independiente |
| Recuentos T y U | Examinar la distribución de creencias registradas | Cobertura estable y recuentos P/D |
| Tasas de cumplimiento de repositorios | Comparar ventanas alineadas y correlaciones con signo | Denominador común e investigación causal |
| Variedad requerida | Experimento propuesto perturbación → respuesta → resultado | Serie de eventos emparejados; aún no hay cociente |

Ningún número de indicadores alineados demuestra por ahora una transición de fase. Una afirmación útil indica el cambio de trabajo observado, la revisión, el período y la explicación alternativa examinada.

---

## 4. Ejercicio práctico

Usando el estado actual de la gobernanza de Demerzel:

1. Calcula el índice de cristalización a partir del archivo de pesos de psicohistoria:
   - `total_T = ?`, `total_U = ?`
   - `crystallization_index = total_T / max(total_U, 1)`

2. Toma como R el `overall_score` del último registro de `state/resilience/history.json`. ¿En qué banda ilustrativa cae? ¿Qué valor cruzaría la banda siguiente y qué otras pruebas harían falta para afirmar un cambio real en el trabajo?

3. En el mismo archivo, el ciclo chaos-003 registra, en `metafixes_applied`, un nuevo archivo de política y una sección añadida a una política existente, y en `level_deltas` una mejora en el nivel L4, mientras R pasaba de 0.64 (chaos-002) a 0.73. Calcula el rendimiento global de los cambios de ese ciclo. ¿Por qué no puede atribuirse la subida de 0.09 solo a la nueva política, y qué observación aislaría su rendimiento? Entre chaos-003 y chaos-004, R subió a 0.82 sin un nuevo archivo de política: ¿qué dice eso sobre medir los rendimientos por número de políticas?

4. **Experimento mental:** Si los tres repositorios consumidores (ix, tars, ga) declararan de repente un 100 % de cumplimiento, ¿demostraría eso una transición de fase o incluso una mejora real? ¿Qué pruebas pedirías?

> **Respuesta a 4:** No. Comprueba el denominador y las versiones de las políticas, si cambiaron las pruebas, si desaparecieron excepciones de los registros y si mejoraron resultados independientes. El salto declarado no clasifica ninguna transición física o de gobernanza.

---

## Conclusiones clave

- Un cambio cualitativo del trabajo no demuestra por sí solo una transición de fase física ni una ley predictiva
- Cinco señales propuestas se pueden examinar en los registros existentes; la variedad requerida sigue siendo una sexta propuesta sin medir
- Una medida de variedad necesita perturbaciones, respuestas y resultados emparejados antes de poder probarse como señal de transición
- Aquí no se ha establecido ningún orden de transición física ni umbral de aviso previo para cambios de gobernanza
- Examinar varios indicadores y resultados medidos de forma independiente; la regla de «3 o más señales» no está validada

## Lecturas adicionales

- [PSY-001: Introducción a la capitalización fractal](psy-001-intro-fractal-compounding.es.md): requisito previo sobre D_c y ERGOL/LOLLI
- [CYB-003: Medir la variedad requerida sin inventar capacidad](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) (en inglés): límites de medición y experimento propuesto
- [CYB-001: Correspondencia entre el VSM y la gobernanza de la IA](../../cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md): requisitos previos estructurales
- Mecánica estadística de las transiciones de fase (teoría de Landau, parámetros de orden, exponentes críticos)
- Fundación de Asimov: la psicohistoria predice tendencias agregadas, no sucesos individuales

---
*Producido por Seldon Auto-Research psychohistory-2026-03-23-001 el 2026-03-23.*
*Pregunta de investigación: ¿Qué señales medibles en el estado de una gobernanza de IA basada en archivos indican que un sistema de gobernanza se acerca a una transición de fase?*
*Creencia: T (confianza: 0.80): acuerdo entre Claude y GPT-4o, NotebookLM no disponible; traducción al español: U (sin revisión de un hablante nativo)*
