# CYB-003: Medir cuantitativamente el cociente de variedad

**Departamento:** Cibernética
**ID del módulo:** CYB-003
**Producido por:** ciclo del plan Seldon cybernetics-2026-03-23-003
**Creencia:** T (verificada), confianza 0.85; **traducción al español:** U (sin revisión de un hablante nativo)
**Fecha:** 2026-03-23
**Requisitos previos:** CYB-001 (Correspondencia con el VSM), CYB-002 (Amortiguación activa)

## Pregunta de investigación

¿Cómo puede Demerzel medir cuantitativamente su cociente de variedad? (Heredada de las preguntas de seguimiento del ciclo 001)

## Resumen

La ley de la variedad requerida de Ashby establece que un regulador debe tener al menos tanta variedad como las perturbaciones a las que se enfrenta. Este curso define un marco cuantitativo para medir el cociente de variedad de Demerzel en tres dimensiones: variedad conductual (personas), variedad estructural (gramáticas) y variedad regulatoria (políticas, constituciones, umbrales). La fórmula clave es V = log2(N) aplicada a cada dimensión. El cociente de variedad R = N_amplifiers / N_attenuators compara los dos espacios de estados; como V = log2(N), R = 2^(V_amplifiers - V_attenuators), y su logaritmo log2 R = V_amplifiers - V_attenuators, en bits, se sigue a lo largo del tiempo para detectar una deriva de la gobernanza hacia la sobrerrestricción o la infrarregulación.

## La variedad de Ashby: la definición formal

### ¿Qué es la variedad?

La variedad es el número de estados distinguibles que puede presentar un sistema. Ashby la definió en *An Introduction to Cybernetics* (1956, capítulo 7) así:

> La variedad de un conjunto de elementos es el logaritmo (en base 2) del número de elementos distintos.

**Fórmula:**

```
V = log2(N)
```

donde N es el número de estados distinguibles. Se mide en bits, la misma unidad que la entropía de Shannon. Un sistema con 8 estados posibles tiene variedad 3 (bits). Un sistema con 1024 estados posibles tiene variedad 10 (bits).

### ¿Por qué logarítmica?

La escala logarítmica importa porque la variedad se combina de forma multiplicativa, no aditiva. Si el sistema A tiene 4 estados y el sistema B tiene 8, el sistema combinado tiene 4 x 8 = 32 estados, y log2(32) = log2(4) + log2(8) = 2 + 3 = 5 bits. Por eso podemos sumar las log-variedades de dimensiones independientes.

### La ley de Ashby

```
V(regulador) >= V(perturbación)
```

«Solo la variedad puede absorber la variedad». Un sistema de gobernanza que puede producir menos respuestas distintas que las perturbaciones distintas a las que se enfrenta fracasará necesariamente al regular algunas de esas perturbaciones.

## Tres dimensiones de la variedad en Demerzel

En un marco de gobernanza, la variedad no es un único número. La variedad de Demerzel opera en tres dimensiones independientes:

### Dimensión 1: variedad conductual (V_B)

**Qué mide:** La gama de comportamientos de agente distintos que el sistema puede producir.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveles de orientación a objetivos | 4 | 2.00 bits |
| Configuraciones de voz (tono x verbosidad x estilo) | ~27 | 4.75 bits |

**Amplificación conductual total:** V_B_amp = 3.81 + 2.00 + 4.75 = **10.56 bits**

Esto significa que Demerzel puede producir aproximadamente 14 × 4 × 27 = 1,512 configuraciones conductuales distinguibles (2^10.56 ≈ 1,510).

**Atenuadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Restricciones de persona (4 de media por persona) | 56 | 5.81 bits |
| Emparejamientos de estimador (fijados a skeptical-auditor) | 1 | 0 bits |

**Atenuación conductual total:** V_B_att = 5.81 bits

**Cociente de variedad conductual:** log2 R_B = V_B_amp - V_B_att = 10.56 - 5.81 = **4.75 bits**, así que R_B = 2^4.75 ≈ **27**

Interpretación: los amplificadores abarcan unas 27 veces más estados que los atenuadores (1,512 configuraciones frente a 56 restricciones). Esto es saludable: el sistema tiene más capacidad de respuesta que restricción. Dividir en cambio las dos variedades, 10.56 / 5.81 ≈ 1.82, no mediría esto: un cociente de logaritmos no es un cociente de espacios de estados.

### Dimensión 2: variedad estructural (V_S)

**Qué mide:** La gama de estructuras distintas (formas de pregunta, patrones de investigación, formatos de salida) que el sistema puede generar.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Gramáticas | 27 | 4.75 bits |
| Producciones de gramática (12 de media por gramática) | ~324 | 8.34 bits |
| Departamentos de Streeling | 15 | 3.91 bits |

**Amplificación estructural total:** V_S_amp = 4.75 + 8.34 + 3.91 = **17.00 bits**

**Atenuadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Puertas de evolución de gramáticas (T >= 0.7, C < 0.1) | 2 | 1.00 bit |
| Detección de obsolescencia (ventana de 30 días) | 1 | 0 bits |

**Atenuación estructural total:** V_S_att = 1.00 bit

**Cociente de variedad estructural:** log2 R_S = V_S_amp - V_S_att = 17.00 - 1.00 = **16.00 bits**, así que R_S = 2^16.00 ≈ **66,000**

Interpretación: las gramáticas abarcan unas 66,000 veces más estructuras de las que distinguen las puertas de evolución. Esto refleja la naturaleza generativa de las gramáticas: son amplificadores de variedad por diseño. Sin embargo, este cociente alto también señala un posible problema: una restricción estructural insuficiente podría llevar a una proliferación de gramáticas sin control de calidad.

### Dimensión 3: variedad regulatoria (V_R)

**Qué mide:** La gama de decisiones de gobernanza distintas que el sistema puede tomar.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Estados de la lógica tetravalente | 4 | 2.00 bits |
| Umbrales de confianza | 5 | 2.32 bits |
| Estados PDCA | 4 | 2.00 bits |

**Amplificación regulatoria total:** V_R_amp = 2.00 + 2.32 + 2.00 = **6.32 bits**

**Atenuadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Políticas | 37 | 5.21 bits |
| Artículos constitucionales (Asimov + Default) | 17 | 4.09 bits |
| Categorías de la taxonomía de daños | 4 | 2.00 bits |

**Atenuación regulatoria total:** V_R_att = 5.21 + 4.09 + 2.00 = **11.30 bits**

**Cociente de variedad regulatoria:** log2 R_R = V_R_amp - V_R_att = 6.32 - 11.30 = **-4.98 bits**, así que R_R = 2^-4.98 ≈ **0.032**

Interpretación: la atenuación regulatoria supera con claridad a la amplificación: los atenuadores abarcan unas 31 veces más estados que los amplificadores (37 × 17 × 4 = 2,516 combinaciones frente a 4 × 5 × 4 = 80). Esto es **intencionado**: la gobernanza debe restringir más de lo que amplifica. Un cociente regulatorio inferior a 1, es decir, un log2 R_R negativo, significa que el sistema es conservador, lo que concuerda con las leyes de Asimov (preferir la seguridad a la capacidad).

## El panel compuesto de variedad

### Tabla resumen

| Dimensión | V_amplifiers | V_attenuators | log2 R | Cociente R | Valoración |
|-----------|-------------|---------------|--------|---------|------------|
| Conductual (V_B) | 10.56 bits | 5.81 bits | 4.75 bits | ≈ 27 | Saludable: más capacidad de respuesta que restricción |
| Estructural (V_S) | 17.00 bits | 1.00 bit | 16.00 bits | ≈ 66,000 | Precaución: alta generatividad, poca restricción |
| Regulatoria (V_R) | 6.32 bits | 11.30 bits | -4.98 bits | ≈ 0.032 | Intencionado: la gobernanza es conservadora |

### Sentidos saludables

La ley de Ashby y los principios del VSM (CYB-001) fijan el sentido que debe tomar cada cociente, todavía no su tamaño:

| Dimensión | Sentido saludable | Justificación |
|-----------|---------------|-----------|
| Conductual | R > 1 (log2 R > 0 bits) | El sistema necesita más opciones conductuales que restricciones, pero no sin límite |
| Estructural | R > 1 (log2 R > 0 bits), con puertas de calidad | Las gramáticas deben ser generativas, pero filtradas por controles de calidad |
| Regulatoria | R < 1 (log2 R < 0 bits) | La gobernanza DEBE estar sobreatenuada: es el principio conservador |

Los límites numéricos de log2 R quedan por calibrar con ciclos observados. No pueden fijarse sobre el cociente V_amplifiers / V_attenuators, que no tiene un sentido fijo en términos de espacios de estados: 10 / 5 y 2 / 1 valen ambos 2, mientras que los espacios de estados que comparan difieren en factores de 2^5 = 32 y 2^1 = 2. Un log2 R negativo no es una variedad negativa: es el logaritmo de un cociente menor que 1.

### Valoración actual

- **Conductual (R_B ≈ 27, 4.75 bits):** En el sentido saludable. No se requiere ninguna acción.
- **Estructural (R_S ≈ 66,000, 16.00 bits):** En el sentido saludable, pero con mucho el mayor cociente de los tres: 2 puertas de evolución frente a las estructuras de 27 gramáticas con ~324 producciones, que están débilmente restringidas. Recomendación: añadir puertas de calidad estructurales (por ejemplo, requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones).
- **Regulatoria (R_R ≈ 0.032, -4.98 bits):** En el sentido saludable. El sistema es conservador; saber si lo es demasiado requiere un límite inferior calibrado.

## El lado de las perturbaciones: ¿qué hay que regular?

El cociente de variedad solo cuenta la mitad de la historia. También debemos medir la variedad de las perturbaciones a las que se enfrenta el sistema:

### Perturbaciones externas (V_D_ext)
| Fuente | Estimación (N) | Variedad V |
|--------|-------------|-----------|
| Repositorios consumidores (ix, tars, ga) | 3 | 1.58 bits |
| Combinaciones de estados de los repositorios (3 repositorios x ~10 estados cada uno) | 10 a 10^3 = 1000 | 3.32 a 9.97 bits |
| Cambios del entorno externo (bibliotecas, API, modelos) | ~100 | 6.64 bits |

**Variedad total de perturbaciones externas:** las combinaciones de estados de los repositorios ya cubren los tres repositorios, así que la primera fila no añade nada. Esa fila es a su vez un intervalo: con unos 10 estados cada uno, los tres repositorios tienen entre 10 estados conjuntos (3.32 bits), si el estado de uno determina el de los demás, y 10^3 = 1000 (9.97 bits), si varían de forma independiente. La fila del entorno es entonces el mayor término aislado: V_D_ext vale al menos **6.64 bits**, y como mucho log2(1000 × 100) = 9.97 + 6.64 = **16.61 bits** si un cambio del entorno puede llegar en cualquiera de los 1000 estados de los repositorios

### Perturbaciones internas (V_D_int)
| Fuente | Estimación (N) | Variedad V |
|--------|-------------|-----------|
| Cambios de estado de creencia por ciclo | ~20 | 4.32 bits |
| Interacciones entre políticas (37 políticas, por pares) | 666 | 9.38 bits |
| Propuestas de evolución de gramáticas | ~5 por ciclo | 2.32 bits |

**Variedad total de perturbaciones internas:** con las mismas cotas, V_D_int vale al menos **9.38 bits** (solo las interacciones entre políticas), y como mucho log2(20 × 666 × 5) = 4.32 + 9.38 + 2.32 = **16.02 bits** si las tres fuentes son independientes

### Comprobación de la ley de Ashby

Para que la gobernanza sea viable:

```
V(respuesta reguladora) >= V(perturbación)
```

- V_R_amp está entre su mayor componente aislado, los umbrales de confianza con 2.32 bits, y la suma de los tres, 6.32 bits, que solo se alcanza si puede producirse cualquier combinación de estado lógico, umbral de confianza y estado PDCA
- V_D está entre la mayor fuente aislada, las interacciones entre políticas con 9.38 bits, y la suma de todas las fuentes, 16.61 + 16.02 = 32.63 bits
- **Brecha: al menos 9.38 - 6.32 = 3.06 bits, como mucho 32.63 - 2.32 = 30.31 bits**

Ambos intervalos se cumplen sean cuales sean las dependencias: un espacio de estados conjunto tiene al menos tantos estados como su mayor parte y como mucho el producto de sus tamaños. La brecha es mínima cuando las fuentes de perturbación son lo más dependientes posible, y los componentes de la respuesta lo más independientes posible; es máxima en el caso contrario. Los vínculos causales entre fuentes de perturbación (un cambio en un repositorio que desencadena un cambio de creencia, una interacción entre políticas que motiva una propuesta de gramática) reducen V_D, y las combinaciones de valores de respuesta que la gobernanza nunca produce reducen V_R_amp. Medir ambas variedades conjuntas, contando las combinaciones distintas observadas de hecho en cada ciclo, situaría la brecha dentro de ese intervalo.

Esto significa que el sistema regulatorio se enfrenta a una variedad de perturbaciones entre 2^3.06 ≈ 8.3 y 2^30.31 ≈ 1.3 × 10^9 veces mayor que la variedad de respuestas que puede producir. La brecha se absorbe mediante:

1. **Escalado a humanos**: el sistema de umbrales de confianza deriva las decisiones difíciles a humanos, tomando prestada su variedad
2. **Prevalencia constitucional**: las leyes de Asimov reducen las decisiones complejas a una elección binaria (seguro/inseguro), lo que disminuye la variedad requerida
3. **Ciclo PDCA**: el procesamiento secuencial convierte perturbaciones paralelas en colas manejables

Son mecanismos legítimos de absorción de variedad, pero incluso la cota inferior de 3.06 bits sugiere que Demerzel debería vigilar si la complejidad de las interacciones entre políticas crece más rápido que la capacidad regulatoria.

## Protocolo de medición

Para seguir el cociente de variedad a lo largo del tiempo, Demerzel debería calcular las siguientes métricas en cada ciclo de gobernanza:

### Métrica 1: recuento de componentes

```json
{
  "variety_snapshot": {
    "timestamp": "2026-03-23T00:00:00Z",
    "amplifiers": {
      "personas": 14,
      "grammars": 27,
      "grammar_productions": 324,
      "departments": 15,
      "tetravalent_states": 4,
      "confidence_levels": 5,
      "pdca_states": 4
    },
    "attenuators": {
      "policies": 37,
      "constitutional_articles": 17,
      "harm_categories": 4,
      "persona_constraints": 56,
      "evolution_gates": 2
    }
  }
}
```

### Métrica 2: cocientes por dimensión

```json
{
  "variety_ratios_log2_bits": {
    "behavioral": 4.75,
    "structural": 16.00,
    "regulatory": -4.98,
    "timestamp": "2026-03-23T00:00:00Z"
  }
}
```

### Métrica 3: detección de tendencias

Sigue log2 R a lo largo de ciclos consecutivos. Alerta cuando:
- Cualquier cociente salga de su sentido saludable (su log2 R cambie de signo)
- El log2 R_R regulatorio baje 1 bit o más en un ciclo (riesgo de parálisis: en relación con los amplificadores, el espacio de estados de los atenuadores se ha duplicado)
- El log2 R_S estructural suba 1 bit o más en un ciclo (riesgo de proliferación de gramáticas)
- El log2 R_B conductual baje 1 bit o más en un ciclo (el sistema responde menos)

Un paso de 1 bit, es decir, un cociente que se duplica o se reduce a la mitad, es un umbral de partida, no un umbral calibrado.

### Métrica 4: tasa de crecimiento de las perturbaciones

Sigue V_disturbance a lo largo del tiempo. Si la variedad de las perturbaciones crece más rápido que la variedad de respuesta, la ley de Ashby acabará violándose. Es el equivalente en gobernanza de la deuda técnica.

## Validación cruzada con GPT-4o

La validación cruzada con GPT-4o confirmó:

1. **V = log2(N) es la fórmula correcta** para la variedad de Ashby. Ambos modelos coinciden.
2. **El modelo aditivo (sumar log-variedades) es válido** para dimensiones independientes, pero demasiado simplista cuando los componentes interactúan. La separación en dimensiones (conductual, estructural, regulatoria) lo resuelve tratando cada dimensión de forma independiente.
3. **GPT-4o calculó un cociente compuesto ingenuo de -2.8**, tratando amplificadores y atenuadores como una única suma aditiva. Esto es incorrecto: una variedad negativa carece de sentido (no se pueden tener menos de cero estados distinguibles). El modelo por dimensiones evita este error.
4. **Ambos modelos coinciden en que R_regulatory < 1.0 es lo esperado** para un sistema de gobernanza. La gobernanza es intrínsecamente atenuadora.
5. **La brecha regulatoria** es un hallazgo nuevo que no aparece en el análisis de GPT-4o. Surge de calcular por separado la variedad de las perturbaciones, algo que GPT-4o no hizo.

**Confianza de la validación cruzada: 0.85** (T: ambos modelos coinciden en los fundamentos; el refinamiento por dimensiones aporta valor más allá del análisis de GPT-4o)

## Implicaciones para Demerzel

1. **Seguir los cocientes de variedad en cada ciclo**: añadir una instantánea de variedad a `state/governance/variety-metrics.json` (o a un archivo de estado equivalente). Vigilar la deriva de los cocientes por dimensión.
2. **Añadir puertas de calidad estructurales**: el cociente estructural, 2^16.00 ≈ 66,000, es con mucho el mayor de los tres. Introducir requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones para aumentar la atenuación sin reducir la generatividad.
3. **Vigilar la brecha regulatoria (de 3.06 a 30.31 bits)**: la complejidad de las interacciones entre políticas (666 combinaciones por pares a partir de 37 políticas) es la mayor fuente aislada de perturbación. A medida que crezcan las políticas, el número de pares crecerá de forma cuadrática, pero su variedad log2(n(n-1)/2) solo crecerá de forma logarítmica, unos 2 bits cada vez que se duplique el número de políticas. Como es la mayor fuente aislada, esos bits elevan de inmediato las dos cotas. Considerar agrupar las políticas u organizarlas jerárquicamente.
4. **El escalado a humanos es un puente de variedad**: el sistema de umbrales de confianza (Artículo 6: Escalado) es el mecanismo principal de Demerzel para absorber la variedad que supera su capacidad regulatoria. Es una característica, no una limitación.
5. **Hacer evolucionar la sección 6 de la gramática**: la sección de variedad requerida de la gramática `sci-cybernetics.ebnf` (líneas 78-82) debería ampliarse con producciones de medición cuantitativa.

## Relación con CYB-001 y CYB-002

- **CYB-001** estableció que la ley de Ashby se aplica a Demerzel y enumeró cualitativamente los amplificadores y atenuadores de variedad. CYB-003 lo hace cuantitativo.
- **La recomendación 5 de CYB-001** («Vigilar el cociente de variedad») queda ahora operacionalizada con fórmulas concretas, sentidos saludables y un protocolo de medición.
- **CYB-002** abordó la amortiguación del Sistema 2. Los mecanismos de banda muerta e histéresis de CYB-002 son en sí mismos atenuadores de variedad: reducen la variedad de las señales que circulan por los canales de coordinación. La métrica de atenuación estructural de CYB-003 debería incluirlos cuando se implementen.

## Fuentes

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Capítulo 7: Quantity of Variety; capítulo 11: Requisite Variety)
- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley. (Capítulo 6: Variety Engineering)
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal, 27(3), 379-423.
- Schwaninger, M. (2024). "What is variety engineering and why do we need it?" Systems Research and Behavioral Science.
- Fathom (2025). Ashby Workshops: gobernanza de la IA y variedad requerida, modelo de las Independent Verification Organizations (IVO).

## Preguntas de seguimiento para el ciclo 004

1. ¿Qué parte de la brecha regulatoria puede cerrar una agrupación jerárquica de políticas (reduciendo las interacciones por pares de O(n^2) a O(n log n))?
2. ¿Cómo debería seguirse el uso de las producciones de gramática para detectar producciones muertas y orientar la atenuación estructural?
3. ¿Cuál es la relación, desde la teoría de la información, entre la lógica tetravalente de Demerzel (T/F/U/C) y la entropía de Shannon? ¿Lleva U (Unknown) más bits que T (True)?

## Referencias cruzadas

- Requisito previo: `state/streeling/courses/cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md`
- Requisito previo: `state/streeling/courses/cybernetics/es/cyb-002-active-dampening-cross-repo-oscillation.es.md`
- Gramática: `grammars/sci-cybernetics.ebnf` (sección 6, variedad requerida)
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Política: `policies/seldon-plan-policy.yaml`
