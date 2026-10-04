---
module_id: cs-003-chord-parser-uncertainty
department: computer-science
course: Expresar la incertidumbre al interpretar símbolos de acordes
level: intermediate
prerequisites: ["símbolos de acordes básicos", "tipos de resultado"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: cs-2026-10-04-003
version: "0.1.0"
---

# Expresar la incertidumbre al interpretar símbolos de acordes

> **Departamento de Informática** | Nivel intermedio | 45 minutos | Borrador: faltan la prueba de ejecución y la revisión musical

## Objetivos

Seguirás la entrada de un músico desde el intérprete de acordes de GA hasta una respuesta de digitaciones. Distinguirás un acorde reconocido de una interpretación parcial, representarás una notación desconocida mediante un resultado explícito y prepararás pruebas que comprueben el significado musical, no solo la existencia de un objeto `Chord`.

## 1. El problema: una respuesta equivocada que parece correcta

Un guitarrista pide digitaciones para `C7b5`. La etiqueta `C7b5` solo sirve si la fórmula conserva tanto la séptima dominante como la quinta rebajada. Mostrar diagramas atractivos de otro conjunto de notas es peor que indicar que esa forma aún no está disponible: el error puede pasar por una respuesta fiable.

GA tiene varios intérpretes de símbolos. Aquí seguimos el utilizado por `VoicingFilterService`: `Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs`. Su expresión regular toma una raíz seguida de **cualquier** sufijo (líneas 11–12). `ParseChordSuffix` reconoce formas exactas; después `ParseComplexSuffix` busca alteraciones como subcadenas (líneas 103–133). Si no encuentra ninguna, devuelve la fórmula mayor (líneas 138–139). `TryParse` captura todas las excepciones y devuelve solo `true` o `false` (líneas 42–53). El consumidor no recibe ninguna señal de que se haya ignorado parte de la entrada.

El recorrido hasta la persona usuaria también importa. `VoicingFilterService.cs:28` llama a `TryParse` y genera digitaciones a partir de `chord.PitchClassSet`. `ContextualChordsController.cs:56–63` devuelve `200 OK` cuando recibe resultados y un `400` genérico ante un error de argumento. Por lo tanto, un acorde mal interpretado pero construido sin error puede llegar a la API. Es una deducción del código; todavía no es una observación de una solicitud HTTP real.

### Ejercicio 1

Para `Cnope`, sigue la raíz, el sufijo, la fórmula, el servicio y la posible respuesta. ¿Cuál debería ser el resultado?

> **Respuesta:** La raíz es C. `nope` no coincide con ninguna forma admitida y el camino de reserva devuelve una fórmula mayor. `TryParse` tiene éxito y el servicio puede entregar digitaciones de C mayor con el texto original y `200 OK`. El comportamiento deseable es un resultado tipado «sufijo desconocido», traducido a un mensaje útil. No hay motivo para suponer que `nope` significa «mayor».

## 2. Comprobar el significado, no el número de análisis exitosos

El [corpus CS-003](../../../fixtures/computer-science/cs-003/README.md) contiene ocho entradas. `C`, `Am` y `G7` son controles admitidos; `Hmaj7` comprueba una raíz inválida. Las otras cuatro entradas revelan problemas diferentes:

| Entrada | Interpretación deducida del código actual | Contrato esperado |
|---|---|---|
| `Cnope` | un sufijo desconocido se convierte en mayor | rechazar el sufijo |
| `Galtxyz` | la subcadena `alt` gana aunque sobre `xyz` | consumir toda la entrada o rechazar |
| `C7b5` | la rama `b5` crea los semitonos 4 y 6; se pierde la séptima | conservar ambos intervalos o rechazar |
| `C/E` | el sufijo se convierte en mayor; queda la etiqueta `C/E`, pero `Chord.Bass` vale la primera nota, C | representar E como bajo o rechazar |

`ChordSymbolParserTests.cs` comprueba que los casos válidos producen un objeto, una raíz y un símbolo. Incluye `C/E`, pero no comprueba su bajo. Eso verifica la construcción, no la interpretación. Una prueba de regresión debe verificar clases de altura, calidad, extensión y bajo cuando la función los promete. Para una forma no admitida debe comprobar un rechazo explícito.

También existe `Chord.TryFromSymbol` en `Common/GA.Domain.Core/Theory/Harmony/Chord.cs`. Devuelve `false` ante un sufijo desconocido (líneas 161–166), pero su vocabulario exacto es más reducido. Sustituir el intérprete del servicio sin un corpus de compatibilidad podría rechazar formas que hoy se aceptan. Primero se fija el contrato y luego se mide la compatibilidad.

### Ejercicio 2

¿Por qué una prueba que solo comprueba que `C7b5` produce un objeto `Chord` no protege al guitarrista? Añade dos comprobaciones.

> **Respuesta:** Un objeto puede conservar el símbolo correcto y tener los intervalos equivocados. Hay que comprobar la séptima dominante y la quinta rebajada en la fórmula o en las clases de altura, y verificar que no queda ningún fragmento del sufijo sin interpretar.

### Ejercicio 3

`C/E` es una notación común, pero este recorrido de GA no representa su bajo. ¿Es una entrada inválida?

> **Respuesta:** La notación puede ser válida; su **significado no está implementado en este recorrido**. Hay que representar y probar E como bajo, o devolver «forma no admitida». Mantener `C/E` como etiqueta de un C mayor en posición fundamental oculta la pérdida de información.

## 3. Componer una frontera capaz de decir «no lo sé»

Una posible separación de responsabilidades es:

```text
tokenize(input)                    -> Result<Tokens, SyntaxError>
consumeAll(tokens)                 -> Result<ChordSyntax, TrailingInput>
interpret(syntax, vocabulary)      -> Result<ChordMeaning, UnsupportedForm>
construct(meaning)                 -> Result<Chord, DomainError>
mapForUser(error)                  -> respuesta documentada al cliente
```

Los cuatro primeros pasos pueden ser funciones puras si el vocabulario se pasa como dato. La API y el registro son efectos. Conserva el texto original para diagnosticar errores, pero nunca lo coloques como etiqueta sobre otra fórmula. `UnsupportedForm` distingue una notación musical posiblemente válida de una raíz mal escrita. Cambiar el código HTTP o la estructura pública de respuesta requiere revisar la compatibilidad; este curso no prescribe tal cambio.

### Ejercicio 4

Un agente propone cambiar solo la rama `b5` para «arreglar» `C7b5`. ¿Qué deben demostrar sus pruebas?

> **Respuesta:** Deben comprobar los intervalos previstos, incluidos la séptima dominante y la quinta rebajada; conservar el significado de `C`, `Am`, `G7` y otras formas admitidas; rechazar una cola como `Galtxyz`; y comprobar que el servicio no genera digitaciones plausibles para una forma no admitida.

## 4. Usar el producto para probar la ruta de error

Ejecuta primero el corpus sobre una revisión fija de GA. Después pide a un guitarrista que introduzca en la interfaz de digitaciones un acorde admitido, un error tipográfico y un acorde con bajo aún no implementado. Guarda el texto mostrado, si la corrección resulta evidente y si un diagrama erróneo parece creíble. Las pruebas de código demuestran el contrato; el uso real muestra si el mensaje ayuda a recuperarse. Compara el comportamiento anterior y el nuevo con las mismas entradas, incluidas las formas que un intérprete más estricto podría rechazar por accidente.

Fija la condición de aceptación antes de editar: ningún sufijo desconocido debe crear un acorde exitoso; ninguna entrada admitida debe cambiar silenciosamente sus clases de altura; y el mensaje debe distinguir un error tipográfico de una forma no implementada. Un fallo de prueba o un mensaje confuso exige revisar la solución, no inventar un acorde. Las predicciones del corpus siguen siendo deducciones del código hasta que se ejecuten como prueba.

### Ejercicio 5

Un intérprete más estricto rechaza `C/E` y evita un diagrama incorrecto de C mayor, pero los músicos todavía no pueden pedir acordes con bajo. ¿Terminó el trabajo?

> **Respuesta:** Se contuvo el riesgo de una respuesta falsa, pero la necesidad del producto continúa. Registra esta mejora parcial, conserva el soporte de bajos en el backlog y comprueba si el mensaje ayuda al guitarrista. Solo declara soporte completo después de implementar y verificar la semántica de E en el recorrido del usuario.

## Evidencia y límites

Se inspeccionaron los caminos de código, las pruebas y el [corpus](../../../fixtures/computer-science/cs-003/chord-symbol-corpus.json) en una copia local de GA el 4 de octubre de 2026. Los comportamientos descritos son deducciones del código. Antes de publicar faltan una prueba ejecutable, una revisión fija de GA, observaciones de la API y comentarios de músicos.
