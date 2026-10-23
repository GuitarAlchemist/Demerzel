---
module_id: mus-009-tuning-fretboard-geometry
department: music
course: Afinación y geometría del mástil
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-007-pitch-spelling-enharmonic-identity, mat-004-vectors-matrices-norms, phy-001-science-of-guitar-sound]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Afinación y geometría del mástil — Una altura, muchos lugares

> **Departamento de Música** | Etapa: Nigredo (Principiante) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, podrás:
- Escribir una afinación como un vector de seis alturas y dar la altura de cualquier cuerda en cualquier traste
- Encontrar todos los lugares donde se puede tocar una altura dada, y contar los lugares de cada altura del mástil
- Describir lo que una afinación alternativa cambia y lo que deja intacto, como la diferencia de dos vectores de afinación
- Deducir dónde van los trastes a partir del semitono temperado, y calcular la posición de los trastes para cualquier longitud de escala
- Localizar lo que GA calcula para las afinaciones, las posiciones y las distancias entre trastes, y dónde su catálogo y sus pruebas se apartan de la teoría

---

## 1. La afinación como vector

Los guitarristas numeran las cuerdas desde el agudo: la cuerda 1 es la más fina, la que suena más alto, y la cuerda 6 la más gruesa. En afinación estándar suenan, de la cuerda 1 a la cuerda 6, mi4, si3, sol3, re3, la2 y mi2, MIDI 64, 59, 55, 50, 45 y 40. Los números de octava son los de la notación científica, como en MUS-007: el do central es do4, MIDI 60 (algunas tradiciones lo llaman do3).

En el lenguaje de MAT-004, la afinación es un vector con una componente por cuerda, t = (t₁, …, t₆) = (64, 59, 55, 50, 45, 40). Cada traste añade un semitono, así que la cuerda s en el traste f da t_s + f. Una forma de acorde es un vector de trastes, uno por cuerda. Los guitarristas la escriben a partir de la cuerda 6: en la forma abierta de mi 022100, las cuerdas 6 a 1 están en los trastes 0, 2, 2, 1, 0 y 0. Ordenada con la cuerda 1 primero, como t, la forma vale (0, 0, 1, 2, 2, 0), y las alturas que suena son la suma de los dos vectores: (64, 59, 56, 52, 47, 40). Leído desde la cuerda 6, eso da 40, 47, 52, 56, 59 y 64, es decir mi2, si2, mi3, sol♯3, si3 y mi4.

Las diferencias entre componentes vecinas son los intervalos entre las cuerdas. Subiendo desde la cuerda 6, valen 5, 5, 5, 4 y 5 semitonos: cuartas justas, salvo la tercera mayor de la cuerda 3 a la cuerda 2. Así, el traste 5 de una cuerda da la siguiente cuerda al aire hacia el agudo, salvo en la cuerda 3, donde lo da el traste 4.

### Ejercicio práctico

En la forma con cejilla de fa 133211, escrita a partir de la cuerda 6, ¿qué alturas dan las cuerdas 6 y 3?

> *Solución:* La cuerda 6 está en el traste 1: 40 + 1 = 41, fa2. La cuerda 3 está en el traste 2: 55 + 2 = 57, la3, la tercera mayor del acorde.

---

## 2. Una altura, muchos lugares

Una altura p se puede tocar en la cuerda s cuando el traste que necesita, p − t_s, está entre 0 y el número de trastes. La guitarra por defecto de GA tiene 24 trastes. En ella, la4, MIDI 69, tiene cinco lugares: cuerda 1 en el traste 5, cuerda 2 en el traste 10, cuerda 3 en el traste 14, cuerda 4 en el traste 19 y cuerda 5 en el traste 24. La cuerda 6 necesitaría el traste 29. En una guitarra de 22 trastes, la cuerda 5 desaparece y la4 tiene cuatro lugares.

El mismo recuento vale para cada altura. Una guitarra de 24 trastes en afinación estándar va de mi2, MIDI 40, a mi6, MIDI 64 + 24 = 88: 49 alturas. De ellas, 10 tienen un lugar, 9 tienen dos, 10 tienen tres, 9 tienen cuatro y 10 tienen cinco. Una sola altura se puede tocar en las seis cuerdas: mi4, la primera cuerda al aire, que la cuerda 6 alcanza en el traste 24. Las alturas con un solo lugar son las cinco más graves, de mi2 a sol♯2, que solo tiene la cuerda 6, y las cinco más agudas, de do6 a mi6, que solo alcanza la cuerda 1.

Una altura no es una clase de altura. La clase de altura la, en cualquier octava, tiene 13 lugares en el mismo mástil: la2 tiene 2, la3 tiene 4, la4 tiene 5 y la5 tiene 2. Un diagrama de digitación que marca «todos los la» muestra los 13; un guitarrista al que se le pide la4 necesita los 5.

### Ejercicio práctico

¿Cuántos lugares tiene mi4 en una guitarra de 22 trastes, y en qué trastes?

> *Solución:* Cinco: cuerda 1 al aire, cuerda 2 en el traste 5, cuerda 3 en el traste 9, cuerda 4 en el traste 14 y cuerda 5 en el traste 19. La cuerda 6 necesitaría el traste 24, que una guitarra de 22 trastes no tiene.

---

## 3. Cambiar la afinación

Una afinación alternativa es un nuevo vector t′, y la diferencia Δ = t′ − t dice, cuerda por cuerda, cuántos semitonos se giró cada cuerda. En drop D, escrita re2 la2 re3 sol3 si3 mi4 a partir de la cuerda 6, solo cambia la cuerda 6, de mi2 a re2: Δ = (0, 0, 0, 0, 0, −2), ordenado con la cuerda 1 primero, como t. DADGAD, re2 la2 re3 sol3 la3 re4, da Δ = (−2, −2, 0, 0, 0, −2), y open G, re2 sol2 re3 sol3 si3 re4, da Δ = (−2, 0, 0, 0, −2, −2).

Lo que cambia se limita a las cuerdas donde Δ no es cero. Cada nota de una de esas cuerdas se desplaza: para conservar una altura, su traste pasa a ser f − Δ_s. En drop D, mi2 necesita la cuerda 6 en el traste 2, y la guitarra baja ahora hasta re2, MIDI 38. Una forma que conserva los mismos trastes da t′ más los trastes: la forma abierta de mi 022100 tiene ahora re2 en el bajo. El intervalo de la cuerda 6 a la cuerda 5 pasa a 7 semitonos, una quinta, así que las cuerdas 6, 5 y 4 en un mismo traste dan una fundamental, una quinta y una octava: al aire, suenan re2, la2 y re3.

Lo que queda es todo lo demás. Las otras cuerdas, la regla t_s + f y los propios trastes no cambian, como tampoco el número de lugares de cualquier altura que las cuerdas cambiadas no alcanzan en ninguna de las dos afinaciones: en drop D, la4 conserva sus cinco lugares.

Las normas de MAT-004 miden una reafinación. La norma 1, ‖Δ‖₁, suma los semitonos girados: 2 para drop D y 6 para DADGAD y open G. La norma ∞, ‖Δ‖∞, es el mayor giro en una sola cuerda: 2 para las tres. Esa es la que importa a la cuerda: según la fórmula de PHY-001, a longitud fija, la tensión de una cuerda va con el cuadrado de su frecuencia, así que bajar una cuerda k semitonos multiplica su tensión por 2^(−2k/12). Dos semitonos más abajo, le queda alrededor de 0.79 de su tensión.

### Ejercicio práctico

Open D es re2 la2 re3 fa♯3 la3 re4, a partir de la cuerda 6. Da su Δ, sus dos normas y las cuerdas que conservan su altura.

> *Solución:* t′ = (62, 57, 54, 50, 45, 38), así que Δ = (−2, −2, −1, 0, 0, −2): ‖Δ‖₁ = 7 y ‖Δ‖∞ = 2. Las cuerdas 4 y 5 conservan su altura.

---

## 4. Dónde van los trastes

Con la misma tensión y la misma cuerda, la frecuencia de una cuerda vibrante es inversamente proporcional a su longitud, como muestra PHY-001. Un semitono multiplica la frecuencia por 2^(1/12), así que la longitud de la cuerda debe multiplicarse por 2^(−1/12). Llamemos L a la **longitud de escala**, la longitud vibrante de la cuerda al aire, de la cejuela a la selleta. En el traste n, la cuerda sigue vibrando sobre L · 2^(−n/12), así que el traste está a una distancia de la cejuela de

d(n) = L · (1 − 2^(−n/12)).

El traste 12 divide la cuerda en dos: d(12) = L/2. El traste 24 deja una cuarta parte: d(24) = 3L/4. En una longitud de escala de 648 mm, los trastes 1, 5, 7, 12 y 24 están a 36.4, 162.5, 215.5, 324 y 486 mm de la cejuela. Los trastes no están igualmente espaciados. Cada espacio vale 2^(−1/12), alrededor de 0.944, veces el anterior, así que el espacio del traste 12 al traste 13, 18.2 mm, es la mitad del primero. Dicho de otro modo, el espacio que sigue a cada traste vale 1/17.817 de la longitud que sigue vibrando desde ese traste hasta la selleta, ya que 1/(1 − 2^(−1/12)) vale alrededor de 17.817.

La longitud de escala cambia las distancias, no las proporciones: en cualquier escala, el traste 12 está en la mitad de la cuerda, a 314 mm en una escala de 628 mm y a 432 mm en un bajo de 864 mm. Algunos trastes caen cerca de fracciones simples de la cuerda. En una escala de 648 mm, el traste 7 está 0.5 mm antes del tercio, 216 mm, y el traste 5 0.5 mm después del cuarto, 162 mm. El tercio y el cuarto de la cuerda son los puntos donde se tocan el tercer y el cuarto armónico, como PHY-001 toca el segundo en el traste 12.

### Ejercicio práctico

En una escala de 628 mm, ¿dónde está el traste 12, y a qué distancia de la cejuela está el primer traste?

> *Solución:* El traste 12 está a 628/2 = 314 mm. El primer traste está a 628 · (1 − 2^(−1/12)), alrededor de 35.2 mm.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos de abajo se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); esta lección documenta ese código sin cambiarlo, y no ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA en `8fe33f8`. Learn, el sitio de cursos del ecosistema, ofrece un curso music-theory-ga cuyas lecciones [1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) y [8](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx) compilan una versión anterior de GA, `a826864`. Los demás números de abajo provienen de una transcripción a Python, línea por línea, del código de GA nombrado.

**Las afinaciones y las posiciones siguen los §1 y §2.** [`Tuning.Default`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Tuning.cs#L23) analiza «E2 A2 D3 G3 B3 E4» y guarda primero la cuerda 1. Para saber qué extremo de una afinación escrita es la cuerda 1, [cuenta los pasos ascendentes y descendentes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Tuning.cs#L121) entre cuerdas vecinas, de modo que una afinación reentrante, cuyas cuerdas, contando desde la cuerda 1, no están en orden descendente de altura, se lea en el sentido en que está escrita. La lección 8 de Learn registró el [banjo de 5 cuerdas](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l8.txt#L29) como una diferencia: GA `a826864` tomaba el bordón, la cuerda corta en sol4 que los intérpretes numeran 5, por la cuerda 1. El commit `4e23984` cambió la regla, y las pruebas de GA esperan ahora [re4 como cuerda 1](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Instruments/TuningTests.cs#L47). [`Fretboard.GetNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L48) suma el traste a la [nota MIDI de la cuerda al aire](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L62), como en el §1, y luego [devuelve solo la nota](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L67), sin su octava: la cuerda 1 y la cuerda 6, al aire, dan ambas mi. Toma un índice de cuerda desde 0, y el índice 0 es la cuerda 1, el mi agudo, como dicen las [pruebas](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Instruments/FretboardTests.cs#L11) de GA. Su propio comentario dice lo contrario: [«0 = lowest string»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L45). El mástil por defecto tiene [24 trastes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L109).

[`GetPositionsForNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L76) toma una nota sin octava y [compara clases de altura](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L82). Responde a la pregunta del §2 sobre clases de altura, no a la pregunta sobre alturas: para la en el mástil por defecto devuelve 13 posiciones, por transcripción. Cada una [lleva su nota MIDI](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L87), y quedarse con las que valen 69 deja los cinco lugares de la4. En la lección 1 de Learn, GA `a826864` todavía comparaba notas enteras y no encontraba [ninguna posición](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L61) para `Note.Sharp.C`, que nunca es igual a la nota cromática que devuelve `GetNote`; el commit `3a7c242` pasó a clases de altura. Un mástil en drop D se construye a partir de sus alturas, como hace la lección 1 de Learn para su [ejercicio en drop D](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L78).

**Las distancias entre trastes siguen el §4.** [`CalculateFretPositionMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L35) calcula [L · (1 − 2^(−n/12))](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L42), con una [longitud de escala por defecto](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L334) de [648 mm](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L331). Por transcripción, da las distancias del §4, 324 mm en el traste 12 y 486 en el traste 24. Dos límites lo rodean:

- [`CalculateStringSpacingMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L78) ensancha el mástil en línea recta de 43 mm en la cejuela a 52 mm en la selleta, y luego [divide entre 5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L87), el número de huecos entre seis cuerdas, sea cual sea el instrumento: 8.6 mm en la cejuela, 9.5 en el traste 12.
- El analizador de voicings mide la extensión de un voicing con [`CalculateFretDistanceMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs#L103) sin pasarle longitud de escala, así que toda extensión se mide a 648 mm.

El archivo de pruebas de la calculadora está [excluido de la compilación](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L47), y ninguna prueba compilada llama directamente a sus métodos de distancia: las pruebas del analizador de voicings llegan a `CalculateFretDistanceMm` a través de `CalculatePlayability` y comprueban la dificultad y la forma de acorde que devuelve. El archivo tampoco compilaría tal como está: llama a [`CalculateStringSpacingMM`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/PhysicalFretboardCalculatorTests.cs#L169), un nombre que la clase no tiene. También escribe a mano la nota MIDI de cada una de sus 41 posiciones, y según t_s + f, 8 de ellas están mal. En su acorde de mi abierto, la cuerda 3 en el traste 1 está [escrita 55](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/PhysicalFretboardCalculatorTests.cs#L62), sol3, cuando suena sol♯3, 56. El análisis de tocabilidad solo lee las cuerdas y los trastes, así que esos números no cambiarían ningún resultado.

**El catálogo de afinaciones contiene dos errores de octava.** Desde el commit `49bd286`, GA lee todo [`Instruments.yaml`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/InstrumentsConfig.fs#L34), y `InstrumentTool.GetTuning`, una herramienta del servidor MCP de GA, a través del cual los asistentes de IA llaman a GA, [devuelve la línea de una afinación](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/InstrumentTool.cs#L27) tal como está escrita. De las 11 afinaciones de seis cuerdas que agrupa bajo `Guitar`, 9 tienen una ‖Δ‖∞ de 2 o menos respecto a la estándar. Las otras dos ponen la cuerda 2 una octava demasiado baja:

- [`OpenCMajor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Instruments.yaml#L536) vale «C2 G2 C3 G3 C3 E4». Open C, do2 sol2 do3 sol3 do4 mi4, da Δ = (0, 1, 0, −2, −2, −4), con ‖Δ‖∞ = 4: sube la cuerda 2 un semitono, de si3 a do4. La línea del catálogo da Δ = (0, −11, 0, −2, −2, −4): su C3 bajaría la cuerda 2 en 11 semitonos, a 2^(−22/12), alrededor de 0.28 de su tensión.
- [`OpenAMajor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Instruments.yaml#L560) vale «E2 A2 E3 A3 C#3 E4», cuyo C♯3 baja la cuerda 2 en 10 semitonos.

Un código que compara afinaciones por clases de altura no puede ver un error así. La habilidad de afinaciones alternativas de GA, para sus propias nueve afinaciones, [reduce cada diferencia módulo 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs#L257) y [la pliega](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs#L258) entre −5 y +6: de si a do indicaría +1, con o sin el error de octava.

Corregir todo esto corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

El catálogo de GA escribe open A como mi2 la2 mi3 la3 do♯3 mi4. Open A sube las cuerdas 4, 3 y 2 un tono respecto a la estándar. Da Δ para ambas, y di qué componente delata el error.

> *Solución:* Open A es mi2 la2 mi3 la3 do♯4 mi4: Δ = (0, 2, 2, 2, 0, 0), con ‖Δ‖∞ = 2. La línea del catálogo da Δ = (0, −10, 2, 2, 0, 0), con ‖Δ‖∞ = 10. La segunda componente, la cuerda 2 bajada 10 semitonos, delata el error.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA; la versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`. Nada en ella es una medición. Las predicciones provienen de los §2 a §5 y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso llama a los tipos de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Los lugares de cada altura.** En el mástil por defecto, para cada nota MIDI de 40 a 88, quédate con las posiciones que `GetPositionsForNote` devuelve para su clase de altura y que llevan esa nota MIDI. Predicción: 10 alturas tienen un lugar, 9 dos, 10 tres, 9 cuatro, 10 cinco, y solo mi4 seis.
2. **La4 en dos afinaciones.** Pide la en el mástil por defecto y en un mástil en drop D de 24 trastes. Predicción: 13 posiciones en cada uno, y las mismas 5 con la nota MIDI 69.
3. **El índice de cuerda y la octava.** Llama a `GetNote(0, 0)` y a `GetNote(5, 0)`, y luego quédate con las posiciones al aire que `GetPositionsForNote` devuelve para mi. Predicción: mi las dos veces, sin octava; las posiciones son la cuerda 1 con la nota MIDI 64 y la cuerda 6 con 40, así que el índice 0 es la cuerda aguda.
4. **Las distancias entre trastes.** Compara `CalculateFretPositionMm(n)` con L · (1 − 2^(−n/12)) para n de 0 a 24 a 648 mm. Predicción: iguales salvo redondeo, con 324 en el traste 12 y 486 en el traste 24.
5. **El catálogo.** Lee las afinaciones de seis cuerdas agrupadas bajo `Guitar` en `Instruments.yaml` mediante `InstrumentsConfig`, analiza cada una y calcula su Δ respecto a la estándar. Predicción: 11 afinaciones; 9 con una ‖Δ‖∞ de 2 o menos, `OpenCMajor` con 11 y `OpenAMajor` con 10.

### Ejercicio práctico

El paso 5 señala las afinaciones por ‖Δ‖∞. ¿Por qué no por ‖Δ‖₁?

> *Solución:* ‖Δ‖₁ suma los giros de las seis cuerdas, así que muchos giros pequeños y corrientes se acumulan. Afinar todas las cuerdas un tono más abajo, re2 sol2 do3 fa3 la3 re4, da ‖Δ‖₁ = 12, cerca de los 14 de la línea de open A del catálogo. ‖Δ‖∞ las separa, 2 frente a 10: mira el mayor giro en una sola cuerda, el que un error de octava hace grande y del que depende la tensión de una cuerda.

---

## 7. Errores comunes

- **Numerar las cuerdas desde el grave.** La cuerda 1 es la más fina, la que suena más alto.
- **Contar los lugares de una clase de altura.** En una guitarra de 24 trastes, la tiene 13 lugares; la4 tiene 5.
- **Mover todas las formas para una nueva afinación.** Solo cambian las cuerdas donde Δ no es cero.
- **Espaciar los trastes por igual.** Cada espacio vale alrededor de 0.944 veces el anterior; el traste 12 está en la mitad de la cuerda.
- **Cambiar las proporciones con la longitud de escala.** Una escala más larga mueve cada traste, pero el traste 12 sigue en la mitad.
- **Leer una afinación como clases de altura.** Un error de octava en una cuerda es invisible módulo 12.
- **Fiarse del comentario de `GetNote`.** En GA, el índice de cuerda 0 es el mi agudo, no la cuerda más grave.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Número de cuerda** | El rango de una cuerda contado desde el agudo: la cuerda 1 es la más fina |
| **Vector de afinación** | Los números MIDI de las cuerdas al aire, t = (t₁, …, t₆); la cuerda s en el traste f da t_s + f |
| **Lugar** | Una cuerda y un traste que tocan una altura dada; una clase de altura tiene los lugares de todas sus octavas |
| **Vector de reafinación** | Δ = t′ − t, los semitonos que se gira cada cuerda; ‖Δ‖₁ los suma, ‖Δ‖∞ toma el mayor |
| **Longitud de escala** | La longitud vibrante de una cuerda al aire, de la cejuela a la selleta |
| **Posición de un traste** | La distancia del traste n a la cejuela, d(n) = L · (1 − 2^(−n/12)) |
| **Afinación reentrante** | Una afinación cuyas cuerdas, contando desde la cuerda 1, no están en orden descendente de altura: alguna cuerda suena más aguda que la anterior |

---

## Autoevaluación

**1. ¿Dónde está el traste 12 en una escala de 648 mm?**
> A 324 mm de la cejuela: d(12) = 648 · (1 − 1/2).

**2. En una guitarra de 24 trastes en afinación estándar, ¿dónde se puede tocar la4?**
> En cinco lugares: cuerda 1 en el traste 5, cuerda 2 en el traste 10, cuerda 3 en el traste 14, cuerda 4 en el traste 19 y cuerda 5 en el traste 24.

**3. Da el vector de reafinación de drop D y sus dos normas.**
> Δ = (0, 0, 0, 0, 0, −2), primero la cuerda 1: ‖Δ‖₁ = 2 y ‖Δ‖∞ = 2.

**4. Por transcripción, [`GetPositionsForNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L76) de GA devuelve 13 posiciones para la en su mástil por defecto. ¿Por qué más de cinco?**
> Compara clases de altura, así que devuelve todos los la de la2 a la5: 2, 4, 5 y 2 lugares. Solo los 5 cuya nota MIDI vale 69 tocan la4.

**Criterio de aprobación:** Dar la altura de cualquier cuerda y traste a partir del vector de afinación; encontrar y contar los lugares de una altura; describir una reafinación por su Δ y sus normas; calcular la posición de los trastes para cualquier longitud de escala; y distinguir las posiciones por clase de altura de GA de los lugares de alturas del §2.

---

## Base de investigación

- T. D. Rossing, F. R. Moore y P. A. Wheeler, *The Science of Sound*, 3.ª ed., Addison-Wesley, 2002: las cuerdas vibrantes y los instrumentos de cuerda
- N. H. Fletcher y T. D. Rossing, *The Physics of Musical Instruments*, 2.ª ed., Springer, 1998: la guitarra
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §5 enlaza a su línea
- Learn, lecciones 1 y 8 de music-theory-ga y su salida esperada en el commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: las comprobaciones compiladas de GA `a826864` citadas en el §5
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
