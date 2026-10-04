---
module_id: vc-001-accessible-fretboard-paths
department: visual-computing
course: Un diapasón, tres vías de acceso
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-04-001
version: "0.1.0"
---

# Un diapasón, tres vías de acceso

> **Departamento de Computación Visual** | Nivel: principiante | Duración estimada: 35 minutos | Estado: pendiente de revisión

## Objetivos

Al terminar esta lección, usted podrá:

- describir una posición de guitarra sin depender del marcador dibujado;
- distinguir un diagrama informativo de un control interactivo;
- ofrecer la misma información y, cuando exista, la misma acción con puntero, teclado y lector de pantalla;
- definir comprobaciones comparables para los modos SVG, Canvas y 3D.

## La pregunta del proyecto y el ejemplo fijo

¿Puede una persona localizar una posición en el diapasón de GA y, si se permite seleccionarla, activarla con puntero, teclado o lector de pantalla? En el commit GA [`dc2e74c`, el componente compartido `GuitarFretboard`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx) dibuja marcadores SVG. Cada círculo maneja entrada y salida del ratón y clic. El marcador inspeccionado no tiene activación por teclado ni nombre, rol o destino de foco explícitos. El [renderizador Canvas](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/RealisticFretboard.tsx) registra eventos de puntero en gráficos Pixi. El [componente que elige el modo](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/StringedInstrumentFretboard.tsx) transmite callbacks de posición a sus ramas SVG, Canvas y 3D.

Se trata de una inspección del código, no de una auditoría terminada en navegador o con tecnología de asistencia. La [tarjeta de voicing de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-client/src/components/SmartVoicingDisplay.tsx) usa el diagrama sin callback de clic: en ese contexto informa, pero no permite seleccionar. No se debe anunciar una acción inexistente.

Usaremos estas dos posiciones con afinación estándar. En GA, los índices de cuerda empiezan en cero, primero la cuerda mi aguda. Para el guitarrista son las cuerdas 1 y 2.

| Posición GA | Descripción para el guitarrista | Nota esperada |
|---|---|---|
| `{ string: 0, fret: 3, label: "G" }` | Cuerda 1 (mi agudo), traste 3, sol | Sol |
| `{ string: 1, fret: 1, label: "C" }` | Cuerda 2 (si), traste 1, do | Do |

### Ejercicio

El SVG muestra solo `G` dentro del primer marcador. ¿Qué falta y por qué no conviene decir «cuerda 0»?

> **Respuesta:** `G` no identifica cuerda ni traste. `0` es un índice del código; para el músico corresponde a «cuerda 1, traste 3, sol».

## 1. Separar la posición del dibujo

Una posición necesita una única fuente de datos: instrumento y afinación, cuerda, traste, nombre de la nota cuando se conoce y disponibilidad de la selección. El círculo SVG, el gráfico Pixi y el objeto 3D son representaciones. El texto debe proceder de los mismos datos, no de coordenadas de pantalla ni de una leyenda escrita aparte. De otro modo, una cejilla, un modo zurdo o un cambio de afinación pueden hacer que el texto contradiga la imagen.

Para el ejemplo, un resumen sería: «Afinación estándar. Dos posiciones marcadas: cuerda 1, traste 3, sol; cuerda 2, traste 1, do». Una lista cercana puede detallar cada posición. Si un clic selecciona, la lista necesita un control que invoque esa misma acción. Si el diagrama solo ilustra un voicing, basta con texto. La [guía del W3C sobre contenido no textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) pide transmitir el significado del gráfico; su nombre por sí solo no describe todas las posiciones.

### Ejercicio

Una persona añade `aria-label="Diapasón de guitarra"` al SVG. ¿Puede el lector identificar las dos posiciones solo con ese nombre?

> **Respuesta:** No. El nombre no incluye las cuerdas, los trastes ni las notas. Hace falta una descripción o lista estructurada y, si existen, los controles de selección.

## 2. Igualar la acción según la finalidad del diagrama

Cuando un marcador llama a `onPositionClick`, también debe ser posible hacer esa selección mediante una interfaz de teclado. El criterio [Keyboard de WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) se refiere a la función: una lista de botones HTML nativos junto al SVG puede ofrecer la vía de teclado. «Seleccionar cuerda 1, traste 3, sol» puede invocar el mismo callback que el clic con puntero. Hay que comprobar el indicador visible de foco y el estado de selección comunicado. Los botones nativos ya responden a Tab, Intro y Espacio. Una cuadrícula ARIA solo conviene si se implementan y prueban sus reglas de foco y flechas según el [patrón de cuadrícula WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/patterns/grid/).

El [código SVG de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx) muestra un cursor de puntero incluso si falta el callback. En una tarjeta de voicing solo informativa, un botón «Seleccionar» inventaría una función. El criterio exige equivalencia de las funciones *disponibles*.

### Ejercicio

Escriba los nombres de dos botones para la variante interactiva y explique qué haría Intro. ¿Qué cambia en la tarjeta informativa?

> **Respuesta:** «Seleccionar cuerda 1, traste 3, sol» y «Seleccionar cuerda 2, traste 1, do». Intro activa la misma selección que el puntero. La tarjeta informativa describe las posiciones sin botones ni estados de selección ficticios.

## 3. Exponer el nombre y el estado de los controles

Para un control personalizado, [Name, Role, Value de WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html) requiere nombre y rol determinables mediante programación, además del estado pertinente. Un círculo con `onClick` sigue siendo un nodo dibujado con un evento; la `G` visible no indica necesariamente a la tecnología de asistencia que es accionable ni a qué traste corresponde. Una pequeña lista de botones HTML al lado del renderizador es una opción sencilla. Si la selección persiste, muestre la posición elegida en texto y exponga su estado. No anuncie un efecto de hover como selección.

Use las mismas palabras en SVG, Canvas y 3D. Los píxeles Canvas y las mallas 3D no crean por sí solos un inventario textual navegable. La lista compartida permanece disponible al cambiar de modo. Es una propuesta de diseño para GA, no una función ya comprobada.

### Ejercicio

Un lector de pantalla anuncia solo «G», mientras quien usa el puntero ve la cuerda mi aguda, traste 3. ¿Qué falta?

> **Respuesta:** Faltan como mínimo cuerda y traste, además de la nota en contexto. Si el marcador selecciona, hacen falta rol de control, acceso por teclado y estado de selección. Si solo informa, no debe tener un rol de acción.

## 4. Probar las tres vías con los mismos datos

Cargue las dos posiciones en cada modo de renderizado. En la variante interactiva, pulse el primer marcador con el puntero y active el botón correspondiente con Intro y Espacio; la posición seleccionada debe coincidir. Compruebe que el lector de pantalla expone los dos nombres completos y cualquier estado de selección. En la variante informativa, ambas posiciones deben seguir siendo legibles y no aparecer como falsos controles. Cambie de modo y verifique que el foco conserva una ruta previsible. Las aserciones sobre el árbol de accesibilidad del navegador ayudan, pero no sustituyen una prueba manual con tecnología de asistencia.

El [archivo Playwright inspeccionado](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/tests/fretboard.spec.ts) comprueba el renderizado y los errores de consola; no demuestra estas tres vías. Registre navegador, lector de pantalla, modo y resultado antes de afirmar que funcionan.

### Ejercicio

La prueba encuentra el SVG y no ve errores de consola. ¿Se cumple el criterio VC-001? ¿Qué observaciones faltan?

> **Respuesta:** No. Hay que verificar las descripciones, la selección por puntero cuando exista, la selección por teclado, los nombres y estados anunciados, y la coherencia al pasar a Canvas o 3D. Anote los modos y combinaciones de asistencia sin probar.

## Ideas clave

- El significado musical de una posición debe seguir disponible sin los píxeles.
- Un diagrama informativo aporta datos; uno interactivo aporta además una acción equivalente por teclado.
- Un modelo compartido puede mantener coherentes las vistas SVG, Canvas, 3D y textual.
- Leer el código descubre un riesgo; las pruebas con navegador y lector de pantalla establecen el comportamiento.

## Fuentes y evidencias del proyecto

- GA: [diapasón SVG compartido](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx), [Canvas](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/RealisticFretboard.tsx), [selector de modo](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/StringedInstrumentFretboard.tsx), [tarjeta de voicing](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-client/src/components/SmartVoicingDisplay.tsx) y [pruebas Playwright](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/tests/fretboard.spec.ts), commit `dc2e74c`.
- W3C: [Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html), [Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) y [Grid Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/).

*Investigación: `visual-computing-2026-10-04-001`. Siguen pendientes la revisión temática y lingüística y las pruebas reales con tecnología de asistencia. Este borrador no es un curso validado.*
