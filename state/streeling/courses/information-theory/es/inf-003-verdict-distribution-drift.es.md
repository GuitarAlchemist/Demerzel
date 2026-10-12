---
module_id: inf-003-verdict-distribution-drift
department: information-theory
course: "Medir la deriva de las distribuciones de veredictos con la divergencia de Jensen-Shannon"
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-003
version: "0.1.0"
---

# Medir la deriva de las distribuciones de veredictos con la divergencia de Jensen-Shannon

> **Departamento de Teoría de la Información** | Nivel: intermedio | Duración estimada: 35 minutos | Estado: borrador en español; pendientes las revisiones de la materia, del alumnado y lingüística, así como la publicación

## Objetivos

Al terminar la lección podrás:

- convertir recuentos comparables de veredictos del analizador IX en vectores de probabilidad alineados;
- calcular la divergencia direccional de Kullback–Leibler (KL) y la divergencia simétrica de Jensen–Shannon (JS) en las unidades que devuelve IX;
- explicar por qué una categoría nueva puede provocar un error en una dirección de KL mientras JS sigue siendo finita;
- usar una divergencia para decidir qué evidencias examinar, controlando los límites del análisis y la composición de los lotes.

## La pregunta del proyecto

El [analizador de redes de Petri de IX fijado en esta revisión](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L105) serializa el resultado de una propiedad como `holds`, `fails` o `unknown`. `Fails` puede incluir un contraejemplo; `unknown` significa que el analizador no decidió la propiedad dentro de sus límites de exploración. Un cambio en la mezcla de esos resultados entre dos ejecuciones puede justificar una investigación. ¿Cómo cuantificarlo sin confundir una cifra con la prueba de una regresión?

La pregunta refutable es: **para una propiedad, el mismo conjunto de identificadores de redes, la misma revisión del analizador y los mismos límites, ¿cuánto cambió la distribución de categorías tras modificar las redes?** IX ya ofrece [funciones KL y JS](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L222), también expuestas como [funciones escalares de DuckDB](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-duck/src/inference.rs#L186-L210). Aquí calculamos una respuesta reproducible con recuentos **sintéticos**. No hemos medido ningún lote de producción de IX ni un cambio de calidad experimentado por usuarios.

INF-001 usaba entropía para describir una distribución de tokens de política. INF-002 mostraba distinciones que pierde la representación compacta OPTIC-K de GA. Aquí comparamos **dos distribuciones sobre las mismas categorías de veredictos**. La puntuación describe frecuencias agregadas: no revela qué red cambió, por qué cambió ni si el cambio es positivo.

## 1. Elegir una observación de significado estable

La [enumeración `Verdict<T>`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L95) tiene tres etiquetas. Su método `holds()` solo devuelve verdadero para `Holds`; `Unknown` no se convierte implícitamente en éxito. El informe `Analysis` contiene propiedades **distintas**, entre ellas `deadlock_free`, `bounded`, `quasi_live`, `live` y `reversible`. Sumarlas mezclaría preguntas con condiciones de prueba diferentes. Elegimos únicamente `deadlock_free`, un veredicto por red y el orden `[holds, fails, unknown]`.

La [rama de ausencia de interbloqueos](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L465-L491) explica el significado operativo de las etiquetas. Encontrar una marcación muerta produce `Fails` aunque luego se trunque la enumeración; `max_reported_deadlocks` limita los testigos publicados y puede ser cero. Si no se encuentra ninguna, `Holds` exige una exploración completa; en caso contrario se obtiene `Unknown`. Esta observación corresponde a esta propiedad concreta, no a todas las ramas del analizador.

El siguiente lote de diez redes es **inventado** y solo sirve de ejemplo numérico:

| Ejecución | Holds | Fails | Unknown | Total |
|---|---:|---:|---:|---:|
| Referencia | 8 | 0 | 2 | 10 |
| Candidata | 6 | 2 | 2 | 10 |

Al dividir cada fila por su total, `p = [0.8, 0, 0.2]` y `q = [0.6, 0.2, 0.2]`. Ambos vectores deben respetar el mismo orden. La función aceptaría arreglos con etiquetas permutadas, pero compararía sucesos equivocados. Guarda las etiquetas junto a los recuentos y verifica su orden.

### Ejercicio 1: formar vectores comparables

Escribe los vectores normalizados en el orden `[holds, fails, unknown]`. ¿Qué metadatos deben acompañar una comparación real?

> **Respuesta:** `p=[8/10,0/10,2/10]=[0.8,0,0.2]`; `q=[6/10,2/10,2/10]=[0.6,0.2,0.2]`. Conserva la propiedad, los identificadores de las redes, el orden de categorías, el commit del analizador, los límites de exploración y el total de cada ejecución. El cálculo de divergencia no comprueba esas condiciones por sí solo.

## 2. Leer lo que IX calcula realmente

La función [`normalize`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L173) divide un vector no negativo por su suma. Rechaza vectores vacíos, entradas negativas o NaN y sumas nulas. Nuestro protocolo exige además recuentos finitos antes de llamarla: el código no rechaza explícitamente el infinito positivo. Ambas divergencias requieren igual longitud y emplean logaritmos naturales; su resultado se expresa en **nats**. Divide por `ln(2)` para obtener bits. El envoltorio DuckDB permite llamar a `ix_kl(p,q)` o `ix_js(p,q)` sobre valores `DOUBLE[]`: una lista SQL `NULL` propaga `NULL`, mientras que un error matemático se convierte en error SQL. Este envoltorio no demuestra que exista una tarea programada de comparación.

KL es direccional:

`D_KL(p || q) = Σ_i p_i ln(p_i / q_i)`.

Solo contribuyen las categorías con `p_i > 0`. En el ejemplo, `D_KL(p || q)=0.8 ln(0.8/0.6)+0.2 ln(0.2/0.2)=0.23014565796142483` nats. En sentido inverso, `fails` exige el término `0.2 ln(0.2/0)`: matemáticamente diverge y [IX devuelve un error](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L185-L209), no infinito. Cambiar el orden de argumentos cambia la pregunta. No ocultes una categoría nueva convirtiendo ese error en cero.

### Ejercicio 2: explicar la dirección de KL

Calcula `D_KL(p || q)`. ¿Devuelve `D_KL(q || p)` el mismo número en IX?

> **Respuesta:** `D_KL(p || q)=0.8 ln(4/3)=0.23014565796142483` nats. Para `D_KL(q || p)`, `q_fails=0.2` se enfrenta a `p_fails=0`; al invertir los argumentos, IX devuelve el error de parámetros « q is zero where p is positive ». KL es asimétrica: aquí solo la dirección referencia-a-candidata tiene soporte finito.

## 3. JS como indicador finito y simétrico

JS forma el punto medio `m=(p+q)/2` y promedia dos KL: `D_JS(p,q)=0.5 D_KL(p||m)+0.5 D_KL(q||m)`. Aquí `m=[0.7,0.1,0.2]`. El punto medio tiene masa positiva donde cualquiera de los vectores la tiene, por lo que JS sigue siendo finita para este par. El [código y su comentario](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L210-L222) indican que JS es simétrica y está acotada por `ln(2)` nats. Cero significa distribuciones **normalizadas** idénticas, no ejecuciones ni tamaños de muestra idénticos.

Un cálculo independiente da `D_KL(p||m)=0.10682511409961822` y `D_KL(q||m)=0.04613902821563412`. Su semisuma es `D_JS=0.07648207115762617` nats, o `0.1103403047760241` bits. Son resultados del ejemplo sintético, no mediciones de IX desplegado. Los [tests unitarios fijados](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L568-L580) cubren el máximo para vectores unitarios disjuntos y cero para entradas iguales; aquí no ejecutamos esa suite.

### Ejercicio 3: calcular y acotar JS

Calcula el punto medio y JS. ¿Cambia el resultado si intercambias las ejecuciones? ¿Cuál es el máximo teórico en nats?

> **Respuesta:** `m=[0.7,0.1,0.2]`; `D_JS=0.5(0.10682511409961822+0.04613902821563412)=0.07648207115762617` nats. Intercambiar las ejecuciones conserva el punto medio e intercambia dos términos de igual peso; JS no cambia. El máximo es `ln(2)=0.6931471805599453` nats para soportes disjuntos.

### Ejercicio 4: lo que oculta la normalización

Compara `[80,0,20]` y `[8,0,2]` con `ix_js`. ¿Qué demuestra el resultado?

> **Respuesta:** Ambos se normalizan como `[0.8,0,0.2]`, así que `ix_js` devuelve `0`, sujeto a la representación de coma flotante. Esto solo demuestra igualdad de proporciones. Un lote tiene 100 observaciones y el otro 10; JS pierde esa diferencia y tampoco indica si las mismas redes recibieron los mismos veredictos. Conserva los totales y los identificadores emparejados fuera de la puntuación.

## 4. Decidir qué debe desencadenar la señal

Imagina una futura regla QA aprobada por separado que señale `JS > 0.05` nats para investigar. Nuestro valor **ilustrativo** supera ese umbral inventado. Es motivo para revisar datos, no prueba de que exista una puerta desplegada ni causa de rechazo automático. Comprueba primero que se analizaron las mismas diez redes y la propiedad `deadlock_free`. Comprueba luego la revisión del analizador y sus `Limits`: el [informe muestra el truncamiento y su causa](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L161-L175). Subir `max_states` puede convertir `unknown` en `holds` o `fails` sin cambiar ninguna red. Empareja los veredictos por ID y examina testigos de fallo y motivos de incertidumbre. Para revisar testigos, fija `max_reported_deadlocks` por encima de cero y repite la ejecución si falta uno. El histograma no dice qué redes cambiaron ni si los contraejemplos corresponden a la propiedad pretendida.

Para un lote pequeño y estable, la tabla de tres columnas y los cambios individuales pueden ser más claros que un único número. El indicador puede servir al comparar muchos lotes coherentes o priorizar una revisión, si se conservan los datos y pruebas por red. Es una propuesta de diseño, no un sustituto de revisar testigos. Una refutación sería que las alertas repetidas se debieran principalmente a composición o presupuestos de exploración distintos: habría que revisar el protocolo y no ajustar el umbral hasta ocultarlas.

### Ejercicio 5: interpretar una alerta

El umbral hipotético es `0.05` nats y JS vale `0.07648207115762617`. Alguien afirma: « La candidata ha empeorado; hay dos fallos nuevos ». ¿Cuál es el resultado aritmético comprobable y qué falta verificar antes de aceptar la regresión?

> **Respuesta:** `0.07648207115762617 > 0.05`; el ejemplo sintético activaría la regla inventada de investigación. La tabla contiene dos `fails` en la candidata y ninguno en la referencia, pero no identifica qué redes cambiaron. Comprueba IDs, propiedad, revisión y límites idénticos; empareja los resultados y lee los testigos de fallo disponibles y los motivos de `unknown`. Exige `max_reported_deadlocks > 0` y repite la ejecución si falta un testigo necesario. Un cambio de límites o de lote podría explicar la deriva sin regresión del código. La puntuación no demuestra causalidad ni significación estadística.

## Límites y siguiente paso

Verificamos la fórmula con una tabla sintética mediante un pequeño cálculo independiente y leímos el código IX en el commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. No ejecutamos el analizador sobre diez redes, no consultamos una tabla DuckDB real, no ejecutamos la suite IX, no estimamos incertidumbre de muestreo y no validamos un umbral de producción. Comparar lotes repetidos pero no idénticos requeriría un plan de muestreo y emparejamiento. Un experimento acotado registraría una propiedad por ID estable en dos revisiones fijadas con límites iguales, calcularía JS e inspeccionaría manualmente cada veredicto cambiado. Guarda la tabla, los registros por red y los testigos junto a la puntuación. Esta traducción es un borrador de IA: siguen pendientes la revisión humana, la sincronización y compilación de Learn y la lectura pública.
