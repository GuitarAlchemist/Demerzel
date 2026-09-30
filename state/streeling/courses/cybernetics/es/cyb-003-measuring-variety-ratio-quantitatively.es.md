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

La ley de la variedad requerida de Ashby establece que un regulador debe tener al menos tanta variedad como las perturbaciones a las que se enfrenta. Este curso define un marco cuantitativo para medir la variedad de Demerzel, en bits, en tres dimensiones: conductual (personas), estructural (gramáticas) y regulatoria (valores lógicos, escalones de confianza, estados PDCA). La fórmula clave es V = log2(N), donde N cuenta los estados distinguibles. Dos reglas de recuento mantienen honestas las cifras. Un producto de recuentos de componentes solo es un espacio de estados conjunto si los componentes varían de forma independiente; si no, es solo una cota superior. Y un recuento de reglas no es un recuento de estados: la atenuación que aportan las restricciones, las políticas y las puertas es la variedad que eliminan, V_in - V_out, que hay que medir en lugar de leerla en el número de reglas. El cociente de variedad que restringe la ley de Ashby compara la variedad de las respuestas con la de las perturbaciones; su logaritmo, log2 R = V_response - V_disturbance en bits, se sigue a lo largo del tiempo para detectar una deriva.

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

En un marco de gobernanza, la variedad no es un único número. Este curso mide la de Demerzel en tres dimensiones. Los recuentos del inventario (personas, restricciones, gramáticas, reglas, políticas, artículos) se leen en el repositorio en el commit `74cf7c5`, que añadió este módulo. Los valores lógicos y los escalones de confianza siguen las definiciones canónicas actuales, en `CONTEXT.md` y `logic/confidence-thresholds.yaml`.

### Dos reglas de recuento

**Estados conjuntos.** Si un componente tiene a estados y otro tiene b, el par tiene como mucho a × b estados conjuntos, y exactamente a × b solo si puede darse cada combinación. Si el segundo queda fijado por el primero, el par solo tiene a estados. Así, log2(a) + log2(b) es una cota superior de la variedad del par, y el mayor de log2(a) y log2(b) es una cota inferior.

**Las reglas no son estados.** Una regla, como una política, una restricción de persona o una puerta de evolución, es un predicado que permite unos estados y prohíbe otros. Varias reglas pueden aplicarse a la vez y solaparse, y dividir una regla en dos cambia su número sin cambiar ningún comportamiento. Por tanto, el log2 de un número de reglas no es una variedad. Un atenuador se mide por la variedad que elimina: A = V_in - V_out, donde V_in es la variedad de lo que le llega y V_out la de lo que deja pasar.

### Dimensión 1: variedad conductual (V_B)

**Qué mide:** La gama de comportamientos de agente distintos que el sistema puede producir.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveles de orientación a objetivos (enumeración del esquema; 3 en uso) | 4 | 2.00 bits |
| Voces (tono, verbosidad, estilo), una por persona | 14 | 3.81 bits |

Cada archivo de persona fija exactamente un nivel de orientación a objetivos y una voz: `schemas/persona.schema.json` exige ambos, y cada uno contiene un único valor. Elegir una persona es, por tanto, elegir ambos, y las 14 voces son las de las 14 personas. Los perfiles conductuales que Demerzel puede instanciar son las propias personas.

**Amplificación conductual:** V_B_amp = log2(14) = **3.81 bits**

Multiplicar las tres filas, 14 × 4 × 14 = 784 perfiles (9.61 bits), contaría combinaciones que solo existen si cualquier nivel y cualquier voz pudieran recombinarse con cualquier persona en tiempo de ejecución, algo que los archivos de persona no permiten. Ese producto es una cota superior, no la variedad.

**Atenuadores:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Restricciones de persona | 60 | Reglas, unas 4.3 por persona; no estados |
| Emparejamiento de estimador | 1 | skeptical-auditor evalúa a las otras 13 personas |

**Atenuación conductual:** sin medir. Las 60 restricciones son predicados que se aplican juntos y pueden solaparse; log2(60) = 5.91 bits las trataría como 60 resultados distinguibles. Su atenuación es la variedad de acciones que eliminan a cada persona, A_B = V_in - V_out, y medirla requiere un registro de las acciones que propone cada persona y de las que rechazan sus restricciones.

Interpretación: Demerzel tiene 14 perfiles conductuales, 3.81 bits, cada uno acotado por sus propias restricciones. Cuánto eliminan las restricciones es la medición pendiente de esta dimensión.

### Dimensión 2: variedad estructural (V_S)

**Qué mide:** La gama de estructuras distintas (formas de pregunta, patrones de investigación, formatos de salida) que el sistema puede generar.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Gramáticas | 27 | 4.75 bits |
| Reglas de gramática (unas 42 por gramática) | 1,129 | 10.14 bits |

Cada regla pertenece a una gramática y nombra un patrón: una forma de pregunta, un paso de investigación, un formato de salida. Las reglas ya enumeran el contenido de las gramáticas, así que multiplicar 1,129 por 27 contaría cada regla 27 veces. Elegir un patrón del catálogo tiene 1,129 resultados.

**Amplificación estructural:** V_S_amp = log2(1,129) = **10.14 bits** por la elección de un patrón

Esto cuenta patrones con nombre, no las cadenas que una gramática puede derivar: una gramática recursiva deriva una cantidad ilimitada, y una derivación encadena muchas elecciones. Los departamentos de Streeling no son estructuras, y el recuento los deja fuera.

**Atenuadores:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Puertas de evolución de gramáticas (T >= 0.7; T >= 0.7 y C < 0.1) | 2 | Reglas sobre los cambios propuestos; no estados |
| Alerta de obsolescencia (más de 30 días) | 1 | Una regla sobre la antigüedad de una gramática; no un estado |

**Atenuación estructural:** sin medir. Es la variedad de los cambios de gramática propuestos que las puertas rechazan, A_S = V_in - V_out, y medirla requiere el registro de propuestas y veredictos.

Interpretación: tres reglas controlan un catálogo de 1,129 patrones. El recuento por sí solo no dice cuánto eliminan, pero muestra qué pocos mecanismos separan una propuesta del catálogo, lo que justifica más puertas estructurales (véase Valoración actual).

### Dimensión 3: variedad regulatoria (V_R)

**Qué mide:** La gama de decisiones de gobernanza distintas que el sistema puede tomar.

En el commit `74cf7c5`, la lógica de Demerzel tenía cuatro valores, T/F/U/C. Su lógica canónica es ahora hexavalente, T/P/U/D/F/C (`CONTEXT.md`), de la que T/F/U/C es el subconjunto de cuatro valores, y este curso cuenta los seis valores.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Valores de la lógica hexavalente | 6 | 2.58 bits |
| Escalones de confianza | 5 | 2.32 bits |
| Estados PDCA | 4 | 2.00 bits |

**Amplificación regulatoria:** según las reglas de recuento, V_R_amp está entre el mayor componente, 2.58 bits, y la suma de los tres, log2(6 × 5 × 4) = log2(120) = **6.91 bits**, que solo se alcanza si puede darse cualquier combinación de valor lógico, escalón de confianza y estado PDCA. No está establecido que varíen de forma independiente, así que se conservan ambas cotas.

**Atenuadores:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Políticas | 37 | Reglas; no estados |
| Artículos constitucionales (Asimov 6, Default 11) | 17 | Reglas; no estados |
| Niveles de gravedad del daño (Critical, High, Medium, Low) | 4 | Clases que encaminan una respuesta; no estados eliminados |

**Atenuación regulatoria:** sin medir. Es la variedad de decisiones candidatas que las políticas y los artículos descartan, A_R = V_in - V_out.

Interpretación: la gobernanza debe restringir más de lo que amplifica, en línea con las leyes de Asimov (preferir la seguridad a la capacidad), pero cuánto restringe está sin medir.

## El panel compuesto de variedad

### Tabla resumen

| Dimensión | Variedad de los amplificadores | Reglas contadas | Atenuación | Valoración |
|-----------|-------------------|---------------|-------------|------------|
| Conductual (V_B) | 3.81 bits (14 personas) | 60 restricciones, 1 estimador | Sin medir | Perfiles fijados por persona |
| Estructural (V_S) | 10.14 bits (1,129 reglas, una elección) | 2 puertas, 1 alerta de obsolescencia | Sin medir | Pocos controles sobre un gran catálogo |
| Regulatoria (V_R) | 2.58 a 6.91 bits | 37 políticas, 17 artículos, 4 niveles de gravedad | Sin medir | Conservadora por diseño, alcance sin medir |

### Por qué el panel no tiene un cociente de amplificadores entre atenuadores

Un atajo tentador divide, en cada dimensión, los estados de los amplificadores entre el número de atenuadores, por ejemplo los 784 perfiles del producto anterior entre las 60 restricciones. Ese cociente no tiene sentido en términos de Ashby. Su numerador cuenta perfiles que los archivos de persona no pueden producir, y su denominador cuenta reglas, no estados, así que dividir una restricción en dos lo cambiaría sin cambiar ningún comportamiento. Un cociente de espacios de estados necesita estados en ambos lados: la variedad V_in que llega a un atenuador y la variedad V_out que deja pasar. La columna Atenuación pasará a ser un número cuando se midan, y la comprobación de la ley de Ashby más abajo compara la variedad de las respuestas con la de las perturbaciones.

### Sentidos saludables

La ley de Ashby y los principios del VSM (CYB-001) fijan el sentido que debe tomar cada magnitud, todavía no su tamaño:

| Dimensión | Sentido saludable | Justificación |
|-----------|---------------|-----------|
| Conductual | A_B > 0 sobre las acciones dañinas, mientras cada persona conserva las acciones permitidas para su rol | Las restricciones deben eliminar el daño, no roles enteros |
| Estructural | A_S > 0: las puertas rechazan algunos cambios propuestos | Una puerta que nunca rechaza nada no atenúa |
| Regulatoria | V_response >= V_disturbance, contando la variedad que el escalado toma prestada de los humanos | La ley de Ashby |

Estos sentidos pasarán a ser umbrales cuando A_B, A_S, A_R y las variedades conjuntas se hayan medido durante varios ciclos.

### Valoración actual

- **Conductual (3.81 bits, 14 personas):** cada persona fija su nivel y su voz. Cuánto eliminan sus restricciones está sin medir; registrar las acciones que se rechazan a cada persona lo mediría.
- **Estructural (10.14 bits, 1,129 reglas):** tres reglas controlan un catálogo de 1,129 patrones. Recomendación: añadir puertas de calidad estructurales (por ejemplo, requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones), cuyos veredictos medirían también A_S.
- **Regulatoria (2.58 a 6.91 bits):** conservadora por diseño; saber si lo es demasiado requiere A_R.

## El lado de las perturbaciones: ¿qué hay que regular?

Las variedades de los amplificadores solo cuentan la mitad de la historia. También debemos medir la variedad de las perturbaciones a las que se enfrenta el sistema:

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

- V_R_amp está entre su mayor componente aislado, los seis valores lógicos con 2.58 bits, y la suma de los tres, 6.91 bits, que solo se alcanza si puede producirse cualquier combinación de valor lógico, escalón de confianza y estado PDCA
- V_D está entre la mayor fuente aislada, las interacciones entre políticas con 9.38 bits, y la suma de todas las fuentes, 16.61 + 16.02 = 32.63 bits
- **Brecha: al menos 9.38 - 6.91 = 2.47 bits, como mucho 32.63 - 2.58 = 30.05 bits**

Ambos intervalos se cumplen sean cuales sean las dependencias: un espacio de estados conjunto tiene al menos tantos estados como su mayor parte y como mucho el producto de sus tamaños. La brecha es mínima cuando las fuentes de perturbación son lo más dependientes posible, y los componentes de la respuesta lo más independientes posible; es máxima en el caso contrario. Los vínculos causales entre fuentes de perturbación (un cambio en un repositorio que desencadena un cambio de creencia, una interacción entre políticas que motiva una propuesta de gramática) reducen V_D, y las combinaciones de valores de respuesta que la gobernanza nunca produce reducen V_R_amp. Medir ambas variedades conjuntas, contando las combinaciones distintas observadas de hecho en cada ciclo, situaría la brecha dentro de ese intervalo.

Esto significa que el sistema regulatorio se enfrenta a una variedad de perturbaciones entre 2^2.47 ≈ 5.5 y 2^30.05 ≈ 1.1 × 10^9 veces mayor que la variedad de respuestas que puede producir. La brecha se absorbe mediante:

1. **Escalado a humanos**: el sistema de umbrales de confianza deriva las decisiones difíciles a humanos, tomando prestada su variedad
2. **Prevalencia constitucional**: las leyes de Asimov reducen las decisiones complejas a una elección binaria (seguro/inseguro), lo que disminuye la variedad requerida
3. **Ciclo PDCA**: el procesamiento secuencial convierte perturbaciones paralelas en colas manejables

Son mecanismos legítimos de absorción de variedad, pero incluso la cota inferior de 2.47 bits sugiere que Demerzel debería vigilar si la complejidad de las interacciones entre políticas crece más rápido que la capacidad regulatoria.

## Protocolo de medición

Para seguir la variedad a lo largo del tiempo, Demerzel debería calcular las siguientes métricas en cada ciclo de gobernanza:

### Métrica 1: recuento de componentes

```json
{
  "variety_snapshot": {
    "commit": "74cf7c5",
    "amplifiers": {
      "personas": 14,
      "grammars": 27,
      "grammar_rules": 1129,
      "logic_values": 6,
      "confidence_rungs": 5,
      "pdca_states": 4
    },
    "rules": {
      "policies": 37,
      "constitutional_articles": 17,
      "harm_severity_levels": 4,
      "persona_constraints": 60,
      "evolution_gates": 2
    }
  }
}
```

`commit` fecha los recuentos del inventario. Como se indicó más arriba, `logic_values` y `confidence_rungs` siguen las definiciones actuales: en ese commit la lógica tenía cuatro valores.

### Métrica 2: variedades por dimensión

```json
{
  "variety_bits": {
    "behavioral_amplifiers": 3.81,
    "structural_amplifiers_one_choice": 10.14,
    "regulatory_amplifiers": [2.58, 6.91],
    "attenuation": {"behavioral": null, "structural": null, "regulatory": null},
    "commit": "74cf7c5"
  }
}
```

Un `null` marca una magnitud aún sin medir, no un cero.

### Métrica 3: medición de la atenuación

Para cada atenuador, registra en cada ciclo lo que le llega y lo que deja pasar: las acciones que propone cada persona y las que rechazan sus restricciones, los cambios de gramática propuestos y los que aceptan las puertas, las decisiones candidatas y las que permiten las políticas y los artículos. El número de resultados distintos en cada lado da V_in y V_out, y A = V_in - V_out.

Sigue estas magnitudes a lo largo de ciclos consecutivos. Alerta cuando:
- La A de un atenuador caiga a 0 bits (ha dejado de eliminar nada)
- La cota inferior de la brecha de Ashby suba 1 bit o más en un ciclo (la variedad de las perturbaciones se duplica en relación con la de las respuestas)
- V_B_amp o V_S_amp cambien (se ha añadido o retirado una persona o una regla de gramática), para que se actualicen los recuentos

Un paso de 1 bit, es decir, una duplicación o una reducción a la mitad, es un umbral de partida, no un umbral calibrado.

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

Este registro describe el curso tal como se escribió al principio. Los puntos 3 y 4 tratan de un cociente de amplificadores entre atenuadores, que el curso ya no calcula, por las razones dadas bajo el panel. La advertencia del punto 2 sobre los componentes que interactúan es lo que ahora tratan las reglas de recuento, con cotas inferiores y superiores.

## Implicaciones para Demerzel

1. **Seguir las variedades en cada ciclo**: añadir la instantánea de variedad a `state/governance/variety-metrics.json` (o a un archivo de estado equivalente). Vigilar las variedades de los amplificadores y, cuando se mida, cada atenuación.
2. **Añadir puertas de calidad estructurales**: tres reglas controlan 1,129 reglas de gramática. Introducir requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones; sus veredictos harían también medible A_S.
3. **Vigilar la brecha regulatoria (de 2.47 a 30.05 bits)**: la complejidad de las interacciones entre políticas (666 combinaciones por pares a partir de 37 políticas) es la mayor fuente aislada de perturbación. A medida que crezcan las políticas, el número de pares crecerá de forma cuadrática, pero su variedad log2(n(n-1)/2) solo crecerá de forma logarítmica, unos 2 bits cada vez que se duplique el número de políticas. Como es la mayor fuente aislada, eleva las dos cotas a la vez. Considerar agrupar las políticas u organizarlas jerárquicamente.
4. **El escalado a humanos es un puente de variedad**: el sistema de umbrales de confianza (Artículo 6: Escalado) es el mecanismo principal de Demerzel para absorber la variedad que supera su capacidad regulatoria. Es una característica, no una limitación.
5. **Hacer evolucionar la sección 6 de la gramática**: la sección de variedad requerida de la gramática `sci-cybernetics.ebnf` (líneas 76-82) debería ampliarse con producciones de medición cuantitativa.

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
3. ¿Cuál es la relación, desde la teoría de la información, entre la lógica hexavalente de Demerzel (T/P/U/D/F/C) y la entropía de Shannon? ¿Lleva U (Unknown) más bits que T (True)?

## Referencias cruzadas

- Requisito previo: `state/streeling/courses/cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md`
- Requisito previo: `state/streeling/courses/cybernetics/es/cyb-002-active-dampening-cross-repo-oscillation.es.md`
- Gramática: `grammars/sci-cybernetics.ebnf` (sección 6, variedad requerida)
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Política: `policies/seldon-plan-policy.yaml`
