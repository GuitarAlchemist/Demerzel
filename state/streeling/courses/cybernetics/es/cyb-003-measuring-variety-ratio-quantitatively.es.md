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

La ley de la variedad requerida de Ashby establece que un regulador debe tener al menos tanta variedad como las perturbaciones a las que se enfrenta. Este curso define un marco cuantitativo para medir la variedad de Demerzel, en bits, en tres dimensiones: conductual (personas), estructural (gramáticas) y regulatoria (las decisiones y las etiquetas que llevan). La fórmula clave es V = log2(N), donde N cuenta los resultados distinguibles. Tres reglas de recuento mantienen honestas las cifras. Un producto de recuentos de componentes solo es un espacio de estados conjunto si los componentes varían de forma independiente; si no, es solo una cota superior. Un recuento de reglas no es un recuento de estados: la atenuación que aportan las restricciones, las políticas y las puertas es la variedad que eliminan, V_in - V_out. Y un inventario no es un conjunto de resultados: las definiciones de reglas, las etiquetas de decisión y los pares de políticas son lo que el repositorio define, no las estructuras, las respuestas y las perturbaciones que se producen. El inventario se cuenta en un commit; las variedades que compara la ley de Ashby hay que medirlas. El cociente de variedad que restringe la ley compara la variedad de las respuestas con la de las perturbaciones; su logaritmo, log2 R = V_response - V_disturbance en bits, se seguirá a lo largo del tiempo para detectar una deriva, una vez medidos ambos lados.

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

En un marco de gobernanza, la variedad no es un único número. Este curso mide la de Demerzel en tres dimensiones. Los recuentos del inventario (personas, restricciones, gramáticas, reglas, políticas, artículos) se leen en el repositorio en el commit `74cf7c5`, que añadió este módulo. Los valores lógicos y los escalones de confianza siguen las definiciones canónicas actuales, en `CONTEXT.md` y `logic/confidence-thresholds.yaml`, leídas en el commit `91e41ac`.

### Tres reglas de recuento

**Estados conjuntos.** Si un componente tiene a estados y otro tiene b, el par tiene como mucho a × b estados conjuntos, y exactamente a × b solo si puede darse cada combinación. Si el segundo queda fijado por el primero, el par solo tiene a estados. Así, log2(a) + log2(b) es una cota superior de la variedad del par, y el mayor de log2(a) y log2(b) es una cota inferior.

**Las reglas no son estados.** Una regla, como una política, una restricción de persona o una puerta de evolución, es un predicado que permite unos estados y prohíbe otros. Varias reglas pueden aplicarse a la vez y solaparse, y dividir una regla en dos cambia su número sin cambiar ningún comportamiento. Por tanto, el log2 de un número de reglas no es una variedad. Un atenuador se mide por la variedad que elimina: A = V_in - V_out, donde V_in es la variedad de lo que le llega y V_out la de lo que deja pasar.

**Un inventario no es un conjunto de resultados.** Un recuento de lo que el repositorio define solo acota los resultados si cada elemento puede darse solo, como un resultado. Una derivación de gramática usa varias definiciones de reglas a la vez, una misma etiqueta de decisión puede cubrir varias acciones distintas, y un par de políticas solo es una interacción si ambas interactúan de verdad, mientras que un mismo par que interactúa puede entrar en conflicto de varias formas distinguibles. La variedad se cuenta sobre los resultados: las estructuras distintas generadas, las respuestas dadas y las perturbaciones encontradas.

### Dimensión 1: variedad conductual (V_B)

**Qué mide:** La gama de comportamientos de agente distintos que el sistema puede producir.

**Amplificadores:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveles de orientación a objetivos (enumeración del esquema; 3 en uso) | 4 | 2.00 bits |
| Voces (tono, verbosidad, estilo), una por persona | 14 | 3.81 bits |

Cada archivo de persona fija exactamente un nivel de orientación a objetivos y una voz: `schemas/persona.schema.json` exige ambos, y cada uno contiene un único valor. Elegir una persona es, por tanto, elegir ambos, y las 14 voces son las de las 14 personas. Los perfiles conductuales que Demerzel puede instanciar son las propias personas.

**Elección de la persona:** V_B_persona = log2(14) = **3.81 bits**, la variedad de elegir qué persona actúa. Las acciones que una persona puede emprender después no se cuentan aquí; son lo que registra la medición de la atenuación (métrica 3).

Multiplicar las tres filas, 14 × 4 × 14 = 784 perfiles (9.61 bits), contaría combinaciones que solo existen si cualquier nivel y cualquier voz pudieran recombinarse con cualquier persona en tiempo de ejecución, algo que los archivos de persona no permiten. Ese producto es una cota superior, no la variedad.

**Atenuadores:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Restricciones de persona | 60 | Reglas, unas 4.3 por persona; no estados |
| Emparejamiento de estimador | 1 | skeptical-auditor evalúa a las otras 13 personas |

**Atenuación conductual:** sin medir. Las 60 restricciones son predicados que se aplican juntos y pueden solaparse; log2(60) = 5.91 bits las trataría como 60 resultados distinguibles. Su atenuación es la reducción de variedad entre las acciones que propone cada persona y las que permiten sus restricciones, A_B = V_in - V_out, y medirla requiere un registro de ambas, con los rechazos registrados aparte.

Interpretación: Demerzel tiene 14 perfiles conductuales, 3.81 bits de elección de persona, cada uno acotado por sus propias restricciones. Cuánto eliminan las restricciones es la medición pendiente de esta dimensión.

### Dimensión 2: variedad estructural (V_S)

**Qué mide:** La gama de estructuras distintas (formas de pregunta, patrones de investigación, formatos de salida) que el sistema puede generar.

**Inventario:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Gramáticas | 27 | Archivos de gramática |
| Definiciones de reglas de gramática (unas 42 por gramática) | 1,129 | Definiciones de no terminales; no estructuras |

Una gramática deriva una estructura componiendo definiciones de reglas: `grammars/sci-cybernetics.ebnf`, por ejemplo, construye una investigación a partir de varios no terminales a la vez, y una gramática recursiva deriva una cantidad ilimitada de estructuras. Así que las 1,129 definiciones no son 1,129 estructuras mutuamente excluyentes, y log2(1,129) = 10.14 bits es el tamaño del inventario, no una variedad estructural.

**Variedad estructural:** sin medir. Es el número de estructuras distintas que las gramáticas generan de hecho en un ciclo, y medirla requiere un registro de las derivaciones producidas. Los departamentos de Streeling no son estructuras, y el inventario los deja fuera.

**Atenuadores:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Puertas de evolución de gramáticas (T >= 0.7; T >= 0.7 y C < 0.1) | 2 | Reglas sobre los cambios propuestos; no estados |
| Alerta de obsolescencia (más de 30 días) | 1 | Una regla sobre la antigüedad de una gramática; no un estado |

**Atenuación estructural:** sin medir. Es la reducción de variedad entre los cambios de gramática propuestos y los que aceptan las puertas, A_S = V_in - V_out, y medirla requiere el registro de propuestas y veredictos.

Interpretación: tres reglas controlan 27 gramáticas que contienen 1,129 definiciones de reglas. El inventario por sí solo no dice cuánto eliminan, pero muestra qué pocos mecanismos separan una propuesta de las gramáticas, lo que justifica más puertas estructurales (véase Valoración actual).

### Dimensión 3: variedad regulatoria (V_R)

**Qué mide:** La gama de decisiones de gobernanza distintas que el sistema puede tomar.

En el commit `74cf7c5`, la lógica de Demerzel tenía cuatro valores, T/F/U/C. Su lógica canónica es ahora hexavalente, T/P/U/D/F/C (`CONTEXT.md`), de la que T/F/U/C es el subconjunto de cuatro valores, y este curso cuenta los seis valores.

**Etiquetas de decisión:**
| Componente | Cantidad (N) | Variedad V = log2(N) |
|-----------|-----------|---------------------|
| Valores de la lógica hexavalente | 6 | 2.58 bits |
| Escalones de confianza | 5 | 2.32 bits |
| Estados PDCA | 4 | 2.00 bits |

**Variedad de las etiquetas:** según las reglas de recuento, la variedad de la terna de etiquetas está entre el mayor componente, 2.58 bits, y la suma de los tres, log2(6 × 5 × 4) = log2(120) = **6.91 bits**, que solo se alcanza si puede darse cualquier combinación de valor lógico, escalón de confianza y estado PDCA. No está establecido que varíen de forma independiente, así que se conservan ambas cotas.

Estas etiquetas clasifican una decisión; no cuentan respuestas. Un valor de verdad enuncia una creencia, un escalón de confianza encamina la ejecución y un estado PDCA es una etapa del flujo de trabajo, así que varias acciones distintas, un escalado entre ellas, pueden llevar la misma terna. La variedad de las etiquetas no acota, por tanto, la variedad de respuestas V_R_amp, que **no está medida**: medirla requiere un registro de las acciones distintas que toma la gobernanza, escalados incluidos.

**Atenuadores:**
| Componente | Cantidad | Qué cuenta el número |
|-----------|-------|-------------------|
| Políticas | 37 | Reglas; no estados |
| Artículos constitucionales (Asimov 6, Default 11) | 17 | Reglas; no estados |
| Niveles de gravedad del daño (Critical, High, Medium, Low) | 4 | Clases que encaminan una respuesta; no estados eliminados |

**Atenuación regulatoria:** sin medir. Es la reducción de variedad entre las decisiones candidatas y las que permiten las políticas y los artículos, A_R = V_in - V_out.

Interpretación: la gobernanza debe restringir más de lo que amplifica, en línea con las leyes de Asimov (preferir la seguridad a la capacidad), pero no están medidas ni su variedad de respuestas ni cuánto restringe.

## El panel compuesto de variedad

### Tabla resumen

| Dimensión | Inventario en `74cf7c5` | Variedad establecida | Atenuación | Valoración |
|-----------|------------------------|---------------------|-------------|------------|
| Conductual (V_B) | 14 personas, 60 restricciones, 1 estimador | Elección de la persona: 3.81 bits | Sin medir | Perfiles fijados por persona |
| Estructural (V_S) | 27 gramáticas, 1,129 definiciones de reglas, 2 puertas, 1 alerta de obsolescencia | Sin medir | Sin medir | Pocos controles sobre muchas gramáticas |
| Regulatoria (V_R) | 4 valores (6 en `91e41ac`), 5 escalones en `91e41ac`, 4 estados PDCA; 37 políticas, 17 artículos, 4 niveles de gravedad | Etiquetas: 2.58 a 6.91 bits; respuestas sin medir | Sin medir | Conservadora por diseño, alcance sin medir |

### Por qué el panel no tiene un cociente de amplificadores entre atenuadores

Un atajo tentador divide, en cada dimensión, los estados de los amplificadores entre el número de atenuadores, por ejemplo los 784 perfiles del producto anterior entre las 60 restricciones. Ese cociente no tiene sentido en términos de Ashby. Su numerador cuenta perfiles que los archivos de persona no pueden producir, y su denominador cuenta reglas, no estados, así que dividir una restricción en dos lo cambiaría sin cambiar ningún comportamiento. Un cociente de espacios de estados necesita estados en ambos lados: la variedad V_in que llega a un atenuador y la variedad V_out que deja pasar. La columna Atenuación pasará a ser un número cuando se midan, y la comprobación de la ley de Ashby más abajo compara la variedad de las respuestas con la de las perturbaciones.

### Sentidos saludables

La ley de Ashby y los principios del VSM (CYB-001) fijan el sentido que debe tomar cada magnitud, todavía no su tamaño:

| Dimensión | Sentido saludable | Justificación |
|-----------|---------------|-----------|
| Conductual | A_B > 0 sobre las acciones dañinas, mientras cada persona conserva las acciones permitidas para su rol | Las restricciones deben eliminar el daño, no roles enteros |
| Estructural | Las puertas rechazan los cambios propuestos que no las superan, fallos inyectados incluidos | Una puerta se prueba con los cambios que debe rechazar; un lote de cambios válidos da con razón A_S = 0 |
| Regulatoria | V_response >= V_disturbance, contando la variedad que el escalado toma prestada de los humanos | La ley de Ashby |

Estos sentidos pasarán a ser umbrales cuando A_B, A_S, A_R y las variedades conjuntas se hayan medido durante varios ciclos.

### Valoración actual

- **Conductual (3.81 bits de elección de persona, 14 personas):** cada persona fija su nivel y su voz. Cuánto eliminan sus restricciones está sin medir; registrar las acciones que propone cada persona y las que permiten sus restricciones lo mediría.
- **Estructural (27 gramáticas, 1,129 definiciones de reglas):** tres reglas las controlan, y no se mide ninguna variedad estructural. Recomendación: añadir puertas de calidad estructurales (por ejemplo, requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones), cuyos veredictos medirían también A_S, y registrar las derivaciones producidas, lo que mediría V_S.
- **Regulatoria (etiquetas de 2.58 a 6.91 bits):** conservadora por diseño; saber si lo es demasiado, o si tiene suficiente variedad de respuesta, requiere A_R y V_R_amp.

## El lado de las perturbaciones: ¿qué hay que regular?

El lado de los amplificadores solo cuenta la mitad de la historia. También debemos estimar la variedad de las perturbaciones a las que se enfrenta el sistema. Los valores de las tablas siguientes son estimaciones, no mediciones, y una fuente no está estimada en absoluto:

### Perturbaciones externas (V_D_ext)
| Fuente | Estimación (N) | Variedad V |
|--------|-------------|-----------|
| Repositorios consumidores (ix, tars, ga) | 3 | 1.58 bits |
| Combinaciones de estados de los repositorios (3 repositorios x ~10 estados cada uno) | 10 a 10^3 = 1000 | 3.32 a 9.97 bits |
| Cambios del entorno externo (bibliotecas, API, modelos) | ~100 | 6.64 bits |

**Variedad total de perturbaciones externas:** las combinaciones de estados de los repositorios ya cubren los tres repositorios, así que la primera fila no añade nada. Esa fila es a su vez un intervalo: con unos 10 estados cada uno, los tres repositorios tienen entre 10 estados conjuntos (3.32 bits), si el estado de uno determina el de los demás, y 10^3 = 1000 (9.97 bits), si varían de forma independiente. Si las estimaciones se cumplen, la fila del entorno es entonces el mayor término aislado: V_D_ext vale al menos **6.64 bits**, y como mucho log2(1000 × 100) = 9.97 + 6.64 = **16.61 bits** si los cambios del entorno llegan de uno en uno, cada uno en cualquiera de los 1000 estados de los repositorios.

### Perturbaciones internas (V_D_int)
| Fuente | Estimación (N) | Variedad V |
|--------|-------------|-----------|
| Cambios de estado de creencia por ciclo | ~20 | 4.32 bits |
| Interacciones entre políticas (37 políticas, 666 pares) | sin estimar | sin estimar |
| Propuestas de evolución de gramáticas | ~5 por ciclo | 2.32 bits |

666 es el número de pares de políticas. Cuenta los pares que podrían interactuar, no los resultados de sus interacciones: solo contribuyen los pares que interactúan de verdad, un mismo par puede entrar en conflicto de varias formas distinguibles, y nada aquí mide ni lo uno ni lo otro. Así que la fila de las políticas no da ni cota inferior ni cota superior.

**Variedad total de perturbaciones internas:** si las estimaciones se cumplen, V_D_int vale al menos **4.32 bits** (solo los cambios de creencia, si se producen unos 20 cambios distintos en un ciclo). El inventario no le da ninguna cota superior: la fila de las políticas no está estimada, y las otras dos filas cuentan eventos por ciclo, no las formas distintas que puede tomar cada evento.

### Comprobación de la ley de Ashby

Para que la gobernanza sea viable:

```
V(respuesta reguladora) >= V(perturbación)
```

- V_R_amp, la variedad de respuestas, no está medida. El inventario solo da la variedad de las etiquetas, entre 2.58 y 6.91 bits, que no la acota (véase la dimensión 3)
- Si las estimaciones se cumplen, V_D vale al menos 6.64 bits, los cambios del entorno, la mayor fuente estimada aislada. El inventario no da ninguna cota superior, ya que las interacciones entre políticas no están estimadas (véase Perturbaciones internas)
- **Brecha: sin calcular.** Ninguno de los dos lados está medido, y los inventarios son compatibles tanto con un superávit como con un déficit de cualquier tamaño

La cota inferior se cumple sean cuales sean las dependencias, dadas las estimaciones: un espacio de estados conjunto tiene al menos tantos estados como su mayor parte. Muestra también lo poco que deciden los inventarios. Unos 100 cambios del entorno distintos (6.64 bits) son menos que las 120 ternas de etiquetas (6.91 bits), así que incluso las etiquetas podrían en principio distinguirlos, mientras que nada en los inventarios pone techo a las perturbaciones. Medir ambas variedades conjuntas, contando las perturbaciones distintas encontradas y las respuestas distintas dadas en cada ciclo, situaría la brecha, si la hay.

Si las perturbaciones superan a las respuestas, la diferencia debe absorberse mediante:

1. **Escalado a humanos**: el sistema de umbrales de confianza deriva las decisiones difíciles a humanos, tomando prestada su variedad
2. **Prevalencia constitucional**: las leyes de Asimov reducen las decisiones complejas a una elección binaria (seguro/inseguro), lo que disminuye la variedad requerida
3. **Ciclo PDCA**: el procesamiento secuencial convierte perturbaciones paralelas en colas manejables

Son mecanismos legítimos de absorción de variedad. Si bastan es lo que mostraría la medición de ambos lados, y Demerzel debería vigilar si la complejidad de las interacciones entre políticas crece más rápido que la capacidad regulatoria.

## Protocolo de medición

Para seguir la variedad a lo largo del tiempo, Demerzel debería calcular las siguientes métricas en cada ciclo de gobernanza:

### Métrica 1: recuentos del inventario

```json
{
  "variety_snapshot": {
    "commit": "74cf7c5",
    "inventory": {
      "personas": 14,
      "grammars": 27,
      "grammar_rule_definitions": 1129,
      "logic_values": 4,
      "pdca_states": 4,
      "policies": 37,
      "constitutional_articles": 17,
      "harm_severity_levels": 4,
      "persona_constraints": 60,
      "evolution_gates": 2
    },
    "definitions": {
      "commit": "91e41ac",
      "logic_values": 6,
      "confidence_rungs": 5
    }
  }
}
```

`commit` fecha los recuentos del inventario, todos leídos en `74cf7c5`, donde la lógica tenía cuatro valores. `definitions` contiene lo que usa la variedad de las etiquetas: los seis valores lógicos de `CONTEXT.md` y los cinco escalones de `logic/confidence-thresholds.yaml`, leídos en `91e41ac`. El archivo de la escala no existía en `74cf7c5`, así que el inventario no cuenta escalones.

### Métrica 2: variedades por dimensión

```json
{
  "variety_bits": {
    "persona_selection": 3.81,
    "decision_labels": [2.58, 6.91],
    "structures_generated": null,
    "responses": null,
    "disturbances": null,
    "attenuation": {"behavioral": null, "structural": null, "regulatory": null},
    "inventory_commit": "74cf7c5",
    "definitions_commit": "91e41ac"
  }
}
```

Un `null` marca una magnitud aún sin medir, no un cero. `persona_selection` viene del inventario y `decision_labels` de las definiciones, de ahí los dos commits.

### Métrica 3: medición de los resultados y de la atenuación

Para cada atenuador, registra en cada ciclo lo que le llega y lo que deja pasar: las acciones que propone cada persona y las que permiten sus restricciones, los cambios de gramática propuestos y los que aceptan las puertas, las decisiones candidatas y las que permiten las políticas y los artículos. Registra aparte las acciones rechazadas, los cambios rechazados y las decisiones excluidas: muestran lo que se eliminó, no lo que pasó. Con N_in resultados distintos que llegan a un atenuador y N_out resultados distintos que lo atraviesan, V_in = log2(N_in), V_out = log2(N_out), y A = V_in - V_out = log2(N_in / N_out) bits: un atenuador que deja pasar 4 de 8 propuestas distintas elimina 1 bit. Si no llega nada al atenuador (N_in = 0), el ciclo no es una observación: regístralo como inactivo, no como un bloqueo. Si le llegan entradas y ninguna pasa (N_in > 0, N_out = 0), V_out no está definido; registra ese ciclo como un bloqueo total, no como un número. Registra del mismo modo, como log2 de cada recuento, las estructuras distintas que generan las gramáticas (V_S), las respuestas distintas que da la gobernanza, escalados incluidos (V_R_amp), y las perturbaciones distintas que encuentra (V_D).

Sigue estas magnitudes a lo largo de ciclos consecutivos. Alerta cuando:
- Una sonda de control pase: una entrada que el atenuador debe rechazar, inyectada a propósito, lo atraviesa. A = 0 por sí solo no es una alerta, ya que un ciclo cuyas entradas son todas válidas da con razón A = 0
- La brecha V_D - V_R_amp suba 1 bit o más en un ciclo (la variedad de las perturbaciones se duplica en relación con la de las respuestas)
- Cambie el inventario (se ha añadido o retirado una persona, una regla de gramática o una política), para que se actualicen los recuentos

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

Este registro describe el curso tal como se escribió al principio. Los puntos 3 y 4 tratan de un cociente de amplificadores entre atenuadores, y el punto 5 de una brecha calculada a partir de los recuentos del inventario; el curso ya no calcula ninguno de los dos, por las razones dadas bajo el panel y en la comprobación de la ley de Ashby. La advertencia del punto 2 sobre los componentes que interactúan es lo que ahora tratan las reglas de recuento, con cotas inferiores y superiores.

## Implicaciones para Demerzel

1. **Seguir las variedades en cada ciclo**: añadir la instantánea del inventario a `state/governance/variety-metrics.json` (o a un archivo de estado equivalente). Registrar el inventario y, cuando se midan, las variedades de las estructuras, las respuestas y las perturbaciones, así como cada atenuación.
2. **Añadir puertas de calidad estructurales**: tres reglas controlan 1,129 definiciones de reglas de gramática. Introducir requisitos de cobertura de pruebas de las gramáticas y seguimiento del uso de las producciones; sus veredictos harían también medible A_S.
3. **Medir la brecha regulatoria**: los inventarios solo la acotan de lejos: perturbaciones de al menos 6.64 bits si las estimaciones se cumplen, sin cota superior, y ninguna cota sobre las respuestas. Las interacciones entre políticas son la fuente de perturbación menos conocida. El número de pares de políticas (666 a partir de 37 políticas) crece de forma cuadrática, unas cuatro veces cada vez que se duplica el número de políticas (2,701 pares para 74 políticas), y cada par que interactúa puede entrar en conflicto de varias formas. Agrupar las políticas u organizarlas jerárquicamente puede reducir las interacciones, pero si reduce las perturbaciones que estas producen es algo que debe mostrar la medición.
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

1. ¿Cómo registrar las perturbaciones distintas encontradas y las respuestas distintas dadas en cada ciclo, para que pueda medirse la brecha de Ashby? Una vez medida, ¿reduce una agrupación jerárquica de políticas las perturbaciones que producen las interacciones entre políticas, o solo el número de pares de políticas?
2. ¿Cómo debería seguirse el uso de las producciones de gramática para detectar producciones muertas y orientar la atenuación estructural?
3. ¿Cuál es la relación, desde la teoría de la información, entre la lógica hexavalente de Demerzel (T/P/U/D/F/C) y la entropía de Shannon? ¿Lleva U (Unknown) más bits que T (True)?

## Referencias cruzadas

- Requisito previo: `state/streeling/courses/cybernetics/es/cyb-001-vsm-ai-governance-mapping.es.md`
- Requisito previo: `state/streeling/courses/cybernetics/es/cyb-002-active-dampening-cross-repo-oscillation.es.md`
- Gramática: `grammars/sci-cybernetics.ebnf` (sección 6, variedad requerida)
- Departamento: `state/streeling/departments/cybernetics.department.json`
- Política: `policies/seldon-plan-policy.yaml`
