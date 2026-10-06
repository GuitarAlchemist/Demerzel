---
module_id: gtr-003-audit-voicing-playability
department: guitar-studies
course: Examinar una afirmación sobre la facilidad de tocar una disposición
level: intermediate
prerequisites: ["gtr-001-the-fretboard-map", "gtr-002-caged-geometry", "gaa-004-choose-a-useful-voicing"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-studies-2026-10-05-003
version: "0.1.0"
---

# Examinar una afirmación sobre la facilidad de tocar una disposición

> **Departamento de Estudios de Guitarra** | Intermedio | 45 minutos | Borrador: pendientes la revisión musical y lingüística

## Objetivos

Calculará una medida sencilla de extensión, distinguirá las dos reglas de
cejilla de GA, encontrará un contraejemplo a una afirmación de comodidad
universal y diseñará una prueba con guitarristas que aporte los datos humanos
que faltan.

## 1. Un número depende de su definición

Use las tres [posiciones didácticas de do mayor](../../../fixtures/guitar-studies/gtr-003/voicing-comparison.json)
de GAA-004: do abierto `x 3 2 0 1 0`, forma de la `x 3 5 5 5 3` y forma
de mi `8 10 10 9 8 8`. Son ejemplos comprobados por sus notas, **no**
salidas capturadas de GA. Las tres tienen una **extensión de dos trastes
positivos**: ignore las cuerdas silenciadas (`-1`) y al aire (`0`), y reste
el menor traste positivo del mayor. Son iguales según esta medida, aunque
ocupan zonas distintas del diapasón y exigen gestos diferentes.

En el [commit GA `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-server/GaApi/Services/VoicingComfortService.cs),
`VoicingComfortService.ComputeStretch` utiliza esa diferencia entre números
de traste para ordenar los candidatos. Es un indicador geométrico útil,
pero no mide milímetros, tamaño de mano, presión necesaria ni dolor. El
[`VoicingPhysicalAnalyzer`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs)
emplea la distancia física entre trastes como una parte de la puntuación
de dificultad. Por eso los dos órdenes pueden diferir.

### Ejercicio 1

Calcule la extensión de trastes positivos de las formas de la y de mi.
¿Demuestra el mismo resultado una distancia igual en milímetros o el mismo
esfuerzo?

> **Respuesta:** Forma de la: `5 - 3 = 2`; forma de mi: `10 - 8 = 2`.
> La igualdad no demuestra la misma distancia física ni la misma disposición
> de los dedos o esfuerzo.

## 2. Leer las dos reglas de cejilla

El indicador `BarreRequired` del analizador busca **tres cuerdas adyacentes
en el mismo traste positivo**. En la forma de la, las cuerdas 4, 3 y 2
están en el traste 5; el indicador es verdadero. En la forma de mi, el
traste 8 aparece en las cuerdas 6, 2 y 1, pero nunca en tres adyacentes;
es falso. Eso describe un patrón detectado, no la digitación obligatoria.

El servicio de comodidad usa otra regla, `IsFullBarre`, cuando se activa
`excludeFullBarre`: cuatro o más cuerdas pisadas deben compartir el menor
traste positivo. En la forma de la, el traste mínimo 3 aparece dos veces;
en la forma de mi, el mínimo 8 aparece tres veces. Ninguna cumple la
regla. Sin embargo, es habitual tocar la forma de mi con una cejilla
completa: es un contraejemplo a interpretar `excludeFullBarre` como «se
eliminan todas las digitaciones con cejilla». Ambas reglas aparecen en el
[registro del material](../../../fixtures/guitar-studies/gtr-003/README.md).

### Ejercicio 2

Para ambas formas, prediga `BarreRequired` y si `excludeFullBarre: true`
las eliminaría **si GA devolviera exactamente esos arreglos de trastes**.
¿Por qué es necesaria esa condición?

> **Respuesta:** Forma de la: `BarreRequired = true`, pero `IsFullBarre =
> false`. Forma de mi: ambos son `false`. Las dos pasarían el filtro. La
> condición importa porque el material didáctico no prueba que el generador
> de GA produzca esos arreglos.

## 3. Contrastar el modelo con quien toca

La puntuación de dificultad de GA combina distancia física entre trastes,
un indicador de cejilla, presencia de cuerdas al aire y número de
posiciones pisadas distintas. Tiene un máximo de 10; las etiquetas se
derivan de umbrales relacionados. Estos datos ayudan a examinar
candidatos, pero el código estudiado no mide el alcance de una mano
concreta, dolor, técnica, ajuste del instrumento ni claridad de las notas.
Incluso «Principiante» es una categoría calculada, no una garantía médica
o pedagógica.

Si tiene una guitarra, pruebe cada forma lentamente. Pulse cada cuerda
prevista y luego rasguee. Anote `notas claras / notas intentadas`, la
digitación, si puede soltar y recuperar la forma y cualquier molestia.
Deténgase si duele. Otra persona, con distinta mano o experiencia, puede
obtener otro resultado. La prueba de una persona puede cuestionar una
afirmación universal, pero no establece la facilidad para toda una población.

### Ejercicio 3

El servicio da una puntuación baja a una forma, pero su tercera cuerda
trastea y usted no llega a tiempo para el cambio. ¿Qué puede concluir?

> **Respuesta:** La puntuación es un indicador calculado. En esta prueba
> no predijo una ejecución clara ni la transición requerida para esta
> persona y este tempo. Registre el contexto y pruebe otra forma; no
> convierta el número en un juicio universal.

## 4. Hacer comprobable el ciclo de mejora

Si un agente propone cambiar un peso de la puntuación, fije primero una
revisión de GA y un pequeño corpus de acordes. Mantenga la misma afinación
y filtros, registre los órdenes anteriores y nuevos, y pida a guitarristas
que prueben algunas formas dentro de una tarea musical definida. Busque
mejoras y regresiones: ¿se tocan claramente más formas de las primeras
posiciones y se ocultan alternativas útiles? Una mejor correlación en una
sola persona no resuelve el modelo. La revisión debe conservar los ensayos
y los contraejemplos.

### Ejercicio 4

Un agente propone fusionar `BarreRequired` e `IsFullBarre` en un único
booleano. ¿Qué pruebas faltan antes de hacerlo?

> **Respuesta:** Defina qué pregunta debe responder y contraste ambas
> reglas con digitaciones reales, observaciones de intérpretes y contratos
> de los servicios. Los ejemplos de la y de mi ya muestran desacuerdos;
> sustituir las reglas sin medir a sus consumidores podría cambiar filtros
> y ocultar posiciones útiles.

## Ideas clave

- Una extensión en números de traste, una puntuación de distancia física y
  la experiencia de una persona responden preguntas diferentes.
- Las dos reglas de cejilla de GA no son intercambiables: indique cuál
  produjo cada resultado.
- Un indicador calculado es una propuesta para probar en contexto musical,
  no una prueba de comodidad universal.

## Pruebas y límites

El [registro del material](../../../fixtures/guitar-studies/gtr-003/README.md)
fija el código GA y las pruebas focalizadas. La ejecución usó un binario
existente: todavía faltan una compilación nueva de GA, una captura del
generador para estas tres formas y pruebas con músicos. También siguen
pendientes las revisiones técnica y lingüística.
