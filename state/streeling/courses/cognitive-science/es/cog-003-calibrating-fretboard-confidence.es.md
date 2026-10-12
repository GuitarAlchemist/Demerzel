---
module_id: cog-003-calibrating-fretboard-confidence
department: cognitive-science
course: "Calibrar la confianza al identificar notas en el diapasón"
level: intermediate
prerequisites: [cog-002-feedback-integrity-fretboard-recall]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-12-003
version: "0.1.0"
---

# Calibrar la confianza al identificar notas en el diapasón

> **Departamento de Ciencias Cognitivas** | Nivel intermedio | 40 minutos | Borrador español; revisión y publicación pendientes

## Objetivos

Convertirás «estoy seguro» en una probabilidad registrada **antes** de recibir respuesta, calcularás una puntuación binaria de Brier con una clave de GA verificada, distinguirás seis ejemplos inventados de resultados medidos en alumnos y diseñarás una prueba que pudiera refutar una hipótesis de calibración. [COG-002 (en inglés)](../en/cog-002-feedback-integrity-fretboard-recall.md) comprueba la clave mostrada. Aquí preguntamos: **¿coincide la confianza declarada con la frecuencia de respuestas correctas?**

## La decisión del proyecto

Imagina un ejercicio de GA «nombra esta nota» en su diapasón SVG. Dos guitarristas aciertan cuatro de seis posiciones. Uno tiene poca confianza en las dos respuestas erróneas; el otro está convencido. La exactitud bruta los iguala, pero quizá necesiten indicaciones distintas. Para decidirlo hacen falta un suceso definido, una clave fiable y una prueba con alumnos reales del efecto de las indicaciones.

En el commit GA [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), la [página de demostración](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) declara seis posiciones. El [componente SVG](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) numera la cuerda aguda E como `string: 0`, define el traste 0 como cuerda al aire y afina por defecto `E, B, G, D, A, E` de agudo a grave. La página no cambia esa afinación. Su sexta posición muestra **C** en cuerda 5, traste 3, aunque tres semitonos sobre el E grave dan **G**. Es una discrepancia del código, no una observación de usuarios. La secuencia correcta en el orden de la página es `E, C, G, E, C, G`.

La página se denomina prueba de un componente SVG antiguo. El [manejador de clic](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) pasa solo cuerda y traste. Estas fuentes no muestran entrada de confianza, sesión puntuada, panel de calibración ni curso desplegado. **Todas las respuestas de alumnos que aparecen abajo son datos sintéticos de enseñanza.**

## 1. Define la predicción antes de revelar la respuesta

En cada intento, pide una nota `a_i` para cierta cuerda y traste. Luego solicita `p_i`, entre 0 y 1: «¿Qué probabilidad hay de que **la nota que elegí** coincida con la clave comprobada independientemente?». Se predice la corrección de esa respuesta, no si la guitarra sonará ni si la etiqueta de la demostración es fiable. Registra `a_i` y `p_i` antes de mostrar la nota. Después asigna `y_i=1` si coinciden y `y_i=0` si no.

Para construir la clave, conserva orden de cuerdas, afinación, traste y revisión de fuente. El E grave es la cuerda 5; E corresponde a clase de altura 4. En el traste 3, `(4+3) mod 12=7`, o G. El C mostrado no puede usarse como clave sin la corrección documentada en COG-002.

La interfaz necesitaría entradas **nuevas** para nota y confianza; el clic actual envía una coordenada. Un registro propuesto es `{source_sha, tuning, string, fret, chosen_note, confidence_before_feedback, verified_note, answer_time, feedback_time}`: es un diseño de estudio, **no** una API de GA. También hay que ocultar la respuesta antes de recoger `p_i`, pues los marcadores de la página ya muestran etiquetas.

### Ejercicio 1 — Define el suceso

Un alumno elige C en cuerda 5, traste 3, con `p=0.9`. ¿Cuál es la nota verificada, cuánto vale `y` y registra `p` el clic actual?

> **Respuesta:** La cuerda 5 es E grave. `(4+3) mod 12=7` da G, así que para C `y=0`. El clic solo pasa `{string, fret}`; no recoge nota elegida ni confianza. La respuesta con `p=0.9` es hipotética.

## 2. Puntúa seis intentos explícitamente inventados

La **puntuación binaria de Brier** es `BS=(1/n) Σ_i (p_i-y_i)^2`. Va de 0 a 1 y **menor es mejor**. A diferencia de un recuento de aciertos, distingue un error cometido con confianza 0.9 de uno con 0.6. Aplica siempre la misma definición del resultado. Las seis elecciones y probabilidades siguientes son **inventadas**; solo las coordenadas, la afinación y la clave corregida proceden de GA.

| Intento | Cuerda, traste | Nota verificada | Elección ficticia | `p_i` | `y_i` | `(p_i-y_i)^2` |
|---:|---|---|---|---:|---:|---:|
| 1 | 0, 0 | E | E | 0.9 | 1 | 0.01 |
| 2 | 1, 1 | C | C | 0.8 | 1 | 0.04 |
| 3 | 2, 0 | G | A | 0.7 | 0 | 0.49 |
| 4 | 3, 2 | E | E | 0.6 | 1 | 0.16 |
| 5 | 4, 3 | C | C | 0.9 | 1 | 0.01 |
| 6 | 5, 3 | G | C | 0.9 | 0 | 0.81 |

El personaje ficticio acierta `4/6≈0.6667`. Las pérdidas suman `0.01+0.04+0.49+0.16+0.01+0.81=1.52`; por tanto, `BS=1.52/6≈0.2533`. Estas cifras **no** estiman la capacidad de un alumno real. Si por error se puntuara el intento 6 contra el C mostrado, su pérdida sería 0.01 en lugar de 0.81, y la puntuación aparente bajaría a `(1.52-0.81+0.01)/6=0.12`. Una buena regla de puntuación no corrige una clave equivocada.

### Ejercicio 2 — Calcula la puntuación

Calcula la exactitud, la suma de pérdidas cuadráticas y la media Brier. ¿Qué intento incorrecto cuesta más?

> **Respuesta:** Cuatro de seis dan `4/6≈0.6667`; la suma es `1.52` y la media `1.52/6≈0.2533`. El intento 6 cuesta `0.81`, frente a `0.49` del intento 3, pues su respuesta errónea tenía confianza 0.9 en vez de 0.7.

### Ejercicio 3 — Examina un grupo de confianza

Entre los intentos con `p_i=0.9`, ¿qué fracción es correcta y cuánto queda por debajo de 0.9? ¿Bastan estos tres intentos para demostrar una calibración individual estable?

> **Respuesta:** Son los intentos 1, 5 y 6; dos aciertan, así que `2/3≈0.6667`. La diferencia es `0.9-2/3≈0.2333`. Tres ejemplos inventados y relacionados son insuficientes para establecer una curva estable.

### Ejercicio 4 — Detecta una clave contaminada

Si el intento 6 se puntuara contra el C mostrado en lugar del G verificado, ¿qué ocurriría con su resultado, pérdida y media? ¿Sería prueba de mejora del alumno?

> **Respuesta:** La elección C pasaría a `y_6=1`; su pérdida bajaría de `(0.9-0)^2=0.81` a `(0.9-1)^2=0.01`. La suma sería `0.72` y la media `0.72/6=0.12`. El alumno no cambió su predicción: la mejora aparente proviene de una clave errónea.

## 3. Por qué conviene minimizar el error cuadrático

Sea `q` la probabilidad real de acertar una respuesta elegida en una clase dada de futuros intentos, y `p` la probabilidad comunicada. La pérdida Brier esperada es `q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q)`. El segundo término no depende de `p`, por lo que la pérdida esperada tiene su mínimo único en `p=q`. Así se recompensan probabilidades honestas **en promedio esperado**, no necesariamente en cada muestra de seis. Tampoco se descubre si el error se debió a invertir cuerdas, olvidar una nota o recibir información engañosa.

En un ejemplo hipotético con `q=0.7`, declarar `p=0.7` da `0.7(0.3)^2+0.3(0.7)^2=0.21` de pérdida esperada. Declarar `p=0.9` da `0.7(0.1)^2+0.3(0.9)^2=0.25`; los 0.04 extra equivalen a `(0.9-0.7)^2`. Los seis intentos inventados **no** establecen que `q=0.7` para guitarristas reales.

Una puntuación Brier menor no implica por sí sola más conocimiento musical. Acercarse a 0.5 en todo podría abaratar errores muy seguros sin acertar más notas. Comunica también exactitud, resultados por cuerda y traste y las probabilidades originales recogidas **antes** de la devolución. Cambiarlas después invalidaría la medida del pronóstico inicial.

### Ejercicio 5 — Comprueba la dirección de la regla

Con `q=0.7` hipotético, compara las pérdidas esperadas para `p=0.7` y `p=0.9`. ¿Cuál es menor y por cuánto?

> **Respuesta:** Para `p=0.7`, `0.7(1-0.7)^2+0.3(0.7)^2=0.21`. Para `p=0.9`, `0.7(1-0.9)^2+0.3(0.9)^2=0.25`. La primera es menor por 0.04. Los seis datos de enseñanza no midieron `q`.

## 4. Diseña una prueba capaz de fracasar

Hipótesis de proyecto: **mostrar información explícita sobre calibración de confianza después de cada respuesta verificada reducirá el Brier del día siguiente en posiciones reservadas, sin bajar la exactitud de notas**, respecto a mostrar solo la nota correcta. Ambos grupos han de elegir nota e introducir confianza antes de recibir respuesta. El grupo de calibración podría ver su confianza, corrección y puntuación acumulada; el grupo de comparación, la misma nota y corrección sin resumen de confianza. Es una propuesta, no una función actual de GA.

Primero corrige la etiqueta errónea o usa otra clave auditada. Construye dos estados de pregunta sin etiquetas visibles con la misma afinación declarada; verifica que nadie vea la nota antes de contestar. Recluta alumnos reales, registra consentimiento y experiencia previa, y asígnalos a las condiciones antes de practicar. Contrabalancea posiciones y reserva otras para el día siguiente. Registra revisión de fuente, ítem, respuesta, confianza, momento de respuesta, devolución y demora exacta. Reconocer un punto en un dibujo no demuestra saber tocar u oír esa nota.

Declara de antemano la medida principal: Brier medio del día siguiente en posiciones reservadas, con exactitud como barrera de seguridad. La hipótesis **no recibe apoyo** si la calibración no reduce ese Brier frente al grupo de comparación o si un aparente beneficio viene acompañado de menor exactitud según la barrera declarada. Informa incertidumbre y número de alumnos e ítems. Un piloto puede revelar confusión de interfaz o efecto techo y justificar otro diseño, no un éxito proclamado después. **No se han realizado** alumnos, asignaciones, variantes de interfaz ni mediciones al día siguiente para esta lección.

### Ejercicio 6 — Especifica un resultado refutador

Un agente dice «El Brier inventado de `0.2533` demuestra que nuestra devolución de confianza mejora el recuerdo». Indica dos razones por las que es injustificado y un resultado del estudio que haría fracasar la hipótesis.

> **Respuesta:** Las seis probabilidades y respuestas se inventaron y la página GA no ofrece esa intervención ni mediciones posteriores. Fracasaría si el grupo de calibración no lograra un Brier inferior en posiciones reservadas al día siguiente, o si la menor puntuación viniera con una disminución de exactitud bajo la barrera prevista. Se necesita una clave corregida y recoger probabilidades antes de dar la respuesta.

## Límite de las pruebas

Las fuentes GA fijadas muestran seis coordenadas, orden de cuerdas, etiquetas visibles y datos enviados al pulsar. La clave corregida y las cuentas de Brier pueden comprobarse. Los seis pronósticos, `q=0.7`, las variantes de interfaz y el estudio son construcciones didácticas. Aquí no constan confianza de usuarios reales, cambio de calibración, beneficio de intervención, ejecución en navegador, revisión temática o lingüística, compilación Learn ni lectura pública. Harán falta pruebas y revisores independientes para llamar a este borrador curso revisado o publicado.
