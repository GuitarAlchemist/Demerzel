# CYB-003: Medir cuantitativamente la razón de variedad

**Departamento:** Cibernética
**Identificador del módulo:** CYB-003
**Producido por:** Ciclo del Plan Seldon cybernetics-2026-03-23-003
**Creencia:** T (verificada), confianza 0,85
**Fecha:** 2026-03-23
**Requisitos previos:** CYB-001 (correspondencia MSV), CYB-002 (amortiguación activa)

## Pregunta de investigación

¿Cómo puede Demerzel medir cuantitativamente su razón de variedad? (Pregunta heredada del seguimiento del ciclo 001.)

## Resumen

La ley de la variedad requerida de Ashby establece que un regulador debe tener al menos tanta variedad como las perturbaciones que enfrenta. Este curso define un marco cuantitativo para medir la razón de variedad de Demerzel en tres dimensiones: variedad conductual (las personas), variedad estructural (las gramáticas) y variedad reguladora (las políticas, las constituciones, los umbrales). La fórmula central es V = log2(N), aplicada dimensión por dimensión, y la razón de variedad R = V_amplificadores / V_atenuadores se sigue a lo largo del tiempo para detectar una deriva de la gobernanza hacia el exceso de restricción o la falta de regulación.

## La variedad de Ashby: definición formal

### ¿Qué es la variedad?

La variedad es el número de estados distinguibles que un sistema puede presentar. Ashby la definió así en *An Introduction to Cybernetics* (1956, capítulo 7):

> La variedad de un conjunto de elementos es el logaritmo (en base 2) del número de elementos distintos.

**Fórmula:**

```
V = log2(N)
```

donde N es el número de estados distinguibles. Se mide en bits, la misma unidad que la entropía de Shannon. Un sistema con 8 estados posibles tiene una variedad de 3 bits. Uno con 1024 estados posibles tiene una variedad de 10 bits.

### ¿Por qué logarítmica?

La escala logarítmica importa porque la variedad se combina de forma multiplicativa, no aditiva. Si el sistema A tiene 4 estados y el sistema B tiene 8, el sistema combinado tiene 4 × 8 = 32, y log2(32) = log2(4) + log2(8) = 2 + 3 = 5 bits. Por eso podemos sumar variedades logarítmicas de dimensiones independientes.

### La ley de Ashby

```
V(regulador) >= V(perturbación)
```

«Solo la variedad absorbe la variedad.» Un sistema de gobernanza capaz de producir menos respuestas distintas que las perturbaciones distintas que enfrenta fracasará necesariamente al regular algunas de ellas.

## Tres dimensiones de la variedad en Demerzel

En un marco de gobernanza, la variedad no es un único número. La de Demerzel opera en tres dimensiones independientes.

### Dimensión 1: la variedad conductual (V_B)

**Qué mide:** el abanico de conductas de agente distintas que el sistema puede producir.

**Amplificadores:**
| Componente | Número (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3,81 bits |
| Niveles de orientación a objetivos | 4 | 2,00 bits |
| Configuraciones de voz (tono × extensión × estilo) | ~27 | 4,75 bits |

**Amplificación conductual total:** V_B_amp = 3,81 + 2,00 + 4,75 = **10,56 bits**

Es decir, Demerzel puede producir unas 2^10,56 = 1506 configuraciones conductuales distinguibles.

**Atenuadores:**
| Componente | Número (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Restricciones de persona (4 de media por persona) | 56 | 5,81 bits |
| Emparejamientos de estimador (fijados a skeptical-auditor) | 1 | 0 bits |

**Atenuación conductual total:** V_B_att = 5,81 bits

**Razón de variedad conductual:** R_B = V_B_amp / V_B_att = 10,56 / 5,81 = **1,82**

Lectura: la amplificación conductual supera a la atenuación por un factor de 1,82. Es saludable: el sistema tiene más capacidad de respuesta que restricciones.

### Dimensión 2: la variedad estructural (V_S)

**Qué mide:** el abanico de estructuras distintas (formas de pregunta, patrones de investigación, formatos de salida) que el sistema puede generar.

**Amplificadores:**
| Componente | Número (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Gramáticas | 27 | 4,75 bits |
| Producciones gramaticales (12 de media por gramática) | ~324 | 8,34 bits |
| Departamentos de Streeling | 15 | 3,91 bits |

**Amplificación estructural total:** V_S_amp = 4,75 + 8,34 + 3,91 = **17,00 bits**

**Atenuadores:**
| Componente | Número (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Umbrales de evolución de gramáticas (T >= 0,7; C < 0,1) | 2 | 1,00 bit |
| Detección de obsolescencia (ventana de 30 días) | 1 | 0 bits |

**Atenuación estructural total:** V_S_att = 1,00 bit

**Razón de variedad estructural:** R_S = V_S_amp / V_S_att = 17,00 / 1,00 = **17,00**

Lectura: la variedad estructural es muy alta frente a la atenuación. Refleja la naturaleza generativa de las gramáticas, amplificadoras de variedad por diseño. Pero esta razón elevada también señala un riesgo: una restricción estructural insuficiente puede derivar en una proliferación de gramáticas sin control de calidad.

### Dimensión 3: la variedad reguladora (V_R)

**Qué mide:** el abanico de decisiones de gobernanza distintas que el sistema puede tomar.

**Amplificadores:**
| Componente | Número (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Estados de la lógica tetravalente | 4 | 2,00 bits |
| Umbrales de confianza | 5 | 2,32 bits |
| Estados PDCA | 4 | 2,00 bits |

**Amplificación reguladora total:** V_R_amp = 2,00 + 2,32 + 2,00 = **6,32 bits**

**Atenuadores:**
| Componente | Número (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Políticas | 37 | 5,21 bits |
| Artículos constitucionales (Asimov y Predeterminada) | 17 | 4,09 bits |
| Categorías de la taxonomía de daños | 4 | 2,00 bits |

**Atenuación reguladora total:** V_R_att = 5,21 + 4,09 + 2,00 = **11,30 bits**

**Razón de variedad reguladora:** R_R = V_R_amp / V_R_att = 6,32 / 11,30 = **0,56**

Lectura: la atenuación reguladora supera con claridad a la amplificación. Es **deliberado**: la gobernanza debe restringir más de lo que amplifica. Una razón reguladora por debajo de 1,0 significa que el sistema es conservador, en línea con las leyes de Asimov (preferir la seguridad a la capacidad).

## El cuadro de mando compuesto de la variedad

### Síntesis

| Dimensión | V_amplificadores | V_atenuadores | Razón R | Evaluación |
|-----------|-------------|---------------|---------|------------|
| Conductual (V_B) | 10,56 bits | 5,81 bits | 1,82 | Saludable — más capacidad de respuesta que restricciones |
| Estructural (V_S) | 17,00 bits | 1,00 bit | 17,00 | Precaución — alta generatividad, poca restricción |
| Reguladora (V_R) | 6,32 bits | 11,30 bits | 0,56 | Deliberado — la gobernanza es conservadora |

### Rangos saludables

Según la ley de Ashby y los principios del MSV (CYB-001), los rangos saludables difieren por dimensión:

| Dimensión | Rango saludable | Justificación |
|-----------|---------------|-----------|
| Conductual | 1,2 a 3,0 | El sistema necesita más opciones conductuales que restricciones, pero no ilimitadas |
| Estructural | 2,0 a 10,0 | Las gramáticas deben ser generativas, pero acotadas por controles de calidad |
| Reguladora | 0,3 a 0,8 | La gobernanza DEBE estar sobreatenuada: es el principio de prudencia |

### Evaluación actual

- **Conductual (1,82):** dentro del rango saludable. No hace falta actuar.
- **Estructural (17,00):** por encima del rango saludable. Las 27 gramáticas y sus ~324 producciones están débilmente restringidas. Recomendación: añadir controles de calidad estructurales (requisitos de cobertura de pruebas de las gramáticas, seguimiento del uso de las producciones).
- **Reguladora (0,56):** dentro del rango saludable. El sistema es conservador sin estar paralizado.

## El lado de la perturbación: ¿qué hay que regular?

La razón de variedad solo cuenta la mitad de la historia. También hay que medir la variedad de las perturbaciones que el sistema enfrenta.

### Perturbaciones externas (V_D_ext)
| Fuente | Estimación (N) | Variedad V |
|--------|-------------|-----------|
| Repositorios consumidores (ix, tars, ga) | 3 | 1,58 bits |
| Combinaciones de estados de los repositorios (3 repositorios × ~10 estados cada uno) | 30 | 4,91 bits |
| Cambios del entorno externo (bibliotecas, API, modelos) | ~100 | 6,64 bits |

**Variedad total de perturbaciones externas:** V_D_ext = **6,64 bits** (dominada por los cambios del entorno)

### Perturbaciones internas (V_D_int)
| Fuente | Estimación (N) | Variedad V |
|--------|-------------|-----------|
| Cambios del estado de creencias por ciclo | ~20 | 4,32 bits |
| Interacciones entre políticas (37 políticas, por pares) | 666 | 9,38 bits |
| Propuestas de evolución de gramáticas | ~5 por ciclo | 2,32 bits |

**Variedad total de perturbaciones internas:** V_D_int = **9,38 bits** (dominada por las interacciones entre políticas)

### Comprobación de la ley de Ashby

Para que la gobernanza sea viable:

```
V(respuesta reguladora) >= V(perturbación)
```

- V_R_amp = 6,32 bits
- V_D = máx(V_D_ext, V_D_int) = 9,38 bits
- **Brecha: 9,38 − 6,32 = 3,06 bits**

Es decir, el sistema regulador enfrenta unas 2^3,06 = 8 veces más variedad de perturbaciones de la que puede producir en variedad de respuestas. Esa brecha se absorbe por tres vías:

1. **El escalado a una persona** — el sistema de umbrales de confianza deriva las decisiones difíciles a seres humanos, tomando prestada su variedad
2. **La anulación constitucional** — las leyes de Asimov reducen decisiones complejas a una elección binaria (seguro / no seguro), lo que rebaja la variedad requerida
3. **El ciclo PDCA** — el procesamiento secuencial convierte perturbaciones paralelas en colas manejables

Son mecanismos legítimos de absorción de variedad, pero la brecha de 3 bits sugiere que Demerzel debería vigilar si la complejidad de las interacciones entre políticas crece más rápido que su capacidad reguladora.

## Protocolo de medición

Para seguir la razón de variedad a lo largo del tiempo, Demerzel debería calcular estas métricas en cada ciclo de gobernanza.

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

### Métrica 2: razones por dimensión

```json
{
  "variety_ratios": {
    "behavioral": 1.82,
    "structural": 17.00,
    "regulatory": 0.56,
    "timestamp": "2026-03-23T00:00:00Z"
  }
}
```

### Métrica 3: detección de tendencias

Seguir las razones en ciclos consecutivos. Avisar cuando:
- una razón cruce el límite de su rango saludable;
- la razón reguladora caiga por debajo de 0,3 (riesgo de parálisis del sistema);
- la razón estructural supere 20,0 (riesgo de proliferación de gramáticas);
- la razón conductual caiga por debajo de 1,0 (sistema poco reactivo).

### Métrica 4: tasa de crecimiento de las perturbaciones

Seguir V_perturbación a lo largo del tiempo. Si la variedad de perturbaciones crece más rápido que la de respuestas, la ley de Ashby acabará por incumplirse. Es el equivalente en gobernanza de la deuda técnica.

## Contravalidación con GPT-4o

La contravalidación con GPT-4o confirmó cinco puntos:

1. **V = log2(N) es la fórmula correcta** para la variedad de Ashby. Ambos modelos coinciden.
2. **El modelo aditivo (sumar variedades logarítmicas) es válido** para dimensiones independientes, pero demasiado simplista en cuanto los componentes interactúan. La separación en dimensiones (conductual, estructural, reguladora) lo resuelve tratando cada una por separado.
3. **GPT-4o calculó una razón compuesta ingenua de −2,8**, tratando amplificadores y atenuadores como una única suma aditiva. Es incorrecto: una variedad negativa carece de sentido, porque no se puede tener menos de cero estados distinguibles. El modelo dimensional evita ese error.
4. **Ambos modelos coinciden en que una R_reguladora < 1,0 es lo esperable** en un sistema de gobernanza. La gobernanza atenúa por naturaleza.
5. **La brecha reguladora de 3 bits** es un hallazgo inédito, ausente del análisis de GPT-4o. Solo aparece al calcular por separado la variedad de las perturbaciones, algo que GPT-4o no hizo.

**Confianza de la contravalidación: 0,85** (T — ambos modelos coinciden en lo fundamental; el refinamiento por dimensiones aporta más que el análisis de GPT-4o.)

## Implicaciones para Demerzel

1. **Seguir las razones de variedad en cada ciclo** — Añadir una instantánea de variedad en `state/governance/variety-metrics.json` (o el fichero de estado equivalente) y vigilar la deriva de las razones por dimensión.
2. **Añadir controles de calidad estructurales** — La razón estructural (17,00) supera el rango saludable. Introducir requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones, para aumentar la atenuación sin reducir la generatividad.
3. **Vigilar la brecha reguladora de 3 bits** — La complejidad de las interacciones entre políticas (666 combinaciones por pares a partir de 37 políticas) es la mayor fuente de perturbación interna. A medida que crezcan las políticas, esta brecha se ensanchará de forma cuadrática. Conviene plantear una agrupación o una organización jerárquica de las políticas.
4. **El escalado a una persona es un puente de variedad** — El sistema de umbrales de confianza (artículo 6: escalado) es el mecanismo principal con el que Demerzel absorbe la variedad que excede su capacidad reguladora. Es una función deliberada, no una limitación.
5. **Hacer evolucionar la sección 6 de la gramática** — La sección sobre variedad requerida de `sci-cybernetics.ebnf` (líneas 78 a 82) debería ampliarse con producciones de medición cuantitativa.

## Relación con CYB-001 y CYB-002

- **CYB-001** estableció que la ley de Ashby se aplica a Demerzel y enumeró cualitativamente los amplificadores y atenuadores de variedad. CYB-003 lo vuelve cuantitativo.
- **La recomendación 5 de CYB-001** («vigilar la razón de variedad») queda ahora operativa: fórmulas concretas, rangos saludables y un protocolo de medición.
- **CYB-002** trataba la amortiguación del sistema 2. Sus bandas muertas e histéresis son a su vez atenuadores de variedad: reducen la variedad de señales que circulan por los canales de coordinación. Una vez implantadas, deberán entrar en la métrica de atenuación estructural de CYB-003.

## Fuentes

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Capítulo 7: Quantity of Variety; capítulo 11: Requisite Variety)
- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley. (Capítulo 6: Variety Engineering)
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Shannon, C. E. (1948). «A Mathematical Theory of Communication». Bell System Technical Journal, 27(3), 379-423.
- Schwaninger, M. (2024). «What is variety engineering and why do we need it?» Systems Research and Behavioral Science.
- Fathom (2025). Talleres Ashby — gobernanza de la IA y variedad requerida, modelo de las organizaciones de verificación independiente (IVO).

## Preguntas de seguimiento para el ciclo 004

1. ¿Puede cerrarse la brecha reguladora de 3 bits mediante una agrupación jerárquica de políticas, que reduciría las interacciones por pares de O(n²) a O(n log n)?
2. ¿Cómo debería seguirse el uso de las producciones gramaticales para detectar producciones muertas e informar la atenuación estructural?
3. ¿Cuál es la relación, desde la teoría de la información, entre la lógica tetravalente de Demerzel (T/F/U/C) y la entropía de Shannon: lleva el estado U (desconocido) más bits que el estado T (verdadero)?

## Referencias cruzadas

- Requisito previo: `state/streeling/courses/cybernetics/en/cyb-001-vsm-ai-governance-mapping.md`
- Requisito previo: `state/streeling/courses/cybernetics/en/cyb-002-active-dampening-cross-repo-oscillation.md`
- Gramática: `grammars/sci-cybernetics.ebnf` (sección 6, variedad requerida)
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Política: `policies/seldon-plan-policy.yaml`
