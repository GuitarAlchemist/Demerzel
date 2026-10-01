---
module_id: mus-007-pitch-spelling-enharmonic-identity
department: music
course: Altura, grafía e identidad enarmónica
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-001-what-is-a-chord]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Altura, grafía e identidad enarmónica — Un sonido, varios nombres

> **Departamento de Música** | Etapa: Nigredo (Principiante) | Duración estimada: 45 minutos

## Objetivos

Al terminar esta lección, podrás:
- Distinguir una altura, una clase de altura y un nombre de nota, y dar la octava y el número MIDI de una altura escrita, como do♭4 o si♯3
- Enumerar los 35 nombres de nota con a lo sumo una doble alteración, situarlos en la línea de quintas, y explicar por qué sol♯/la♭ es la única clase de altura que tiene solo dos
- Escribir las siete notas de cualquiera de las 30 tonalidades mayores y menores con un nombre por grado, y explicar por qué los sostenidos y los bemoles de dos tonalidades enarmónicas suman 12
- Escribir las tríadas de re♭ mayor y de do♯ mayor, que un guitarrista toca en los mismos trastes
- Localizar dónde GA conserva la grafía de una nota, y dónde reduce una nota a su clase de altura y vuelve a nombrarla a partir de una lista

---

## 1. Altura, clase de altura y nombre de nota

Una nota se describe en tres niveles, y cada uno olvida algo que el anterior conserva.

Una **altura** es un sonido de altura definida. El MIDI numera las alturas por semitono: en notación científica, el do central es do4 (algunas tradiciones lo llaman do3), vale 60, y do♯4 vale 61. Una **clase de altura** olvida la octava: todo do es la clase de altura 0, numeradas de do = 0 a si = 11, como hace MUS-002. Un **nombre de nota** combina uno de los siete nombres do, re, mi, fa, sol, la, si (C a B en notación anglosajona) con una alteración: ninguna (♮), ♯ o ♭ para moverlo un semitono hacia arriba o hacia abajo, 𝄪 o 𝄫 para moverlo dos.

En un instrumento de temperamento igual, dos nombres para la misma altura, como do♯ y re♭, son **enarmónicos**: son la misma tecla en un piano y el mismo traste en una guitarra. El nombre no es una propiedad del sonido. Indica qué nombre, y por tanto qué grado de una escala, ocupa la nota.

El número de octava pertenece al nombre, no al sonido. La notación científica empieza cada octava en do, así que el do♭ escrito en la octava 4 es do♭4, y suena como si3, MIDI 59; si♯3 suena como do4, MIDI 60. En general, MIDI = 12 × (octava + 1) + la clase de altura del nombre + el valor de la alteración, de −2 para 𝄫 a +2 para 𝄪: do♯4 y re♭4 valen ambos 61, mi♯4 vale 65 y fa♭4 vale 64.

### Ejercicio práctico

Da el número MIDI de si♯4 y de do♭5, y la nota natural que suena en cada caso.

> *Solución:* si♯4 vale 12 × 5 + 11 + 1 = 72, el sonido de do5. Do♭5 vale 12 × 6 + 0 − 1 = 71, el sonido de si4. Ambos nombres cruzan el límite entre si y do, así que cada uno lleva el número de octava de su nombre, no el de su sonido.

---

## 2. Los 35 nombres y la línea de quintas

Siete nombres y cinco alteraciones, 𝄫, ♭, ♮, ♯ y 𝄪, dan 35 nombres de nota. Cubren de forma desigual las 12 clases de altura:

| Clase de altura | Nombres |
|---|---|
| 0 | re𝄫, do, si♯ |
| 1 | re♭, do♯, si𝄪 |
| 2 | mi𝄫, re, do𝄪 |
| 3 | fa𝄫, mi♭, re♯ |
| 4 | fa♭, mi, re𝄪 |
| 5 | sol𝄫, fa, mi♯ |
| 6 | sol♭, fa♯, mi𝄪 |
| 7 | la𝄫, sol, fa𝄪 |
| 8 | la♭, sol♯ |
| 9 | si𝄫, la, sol𝄪 |
| 10 | do𝄫, si♭, la♯ |
| 11 | do♭, si, la𝄪 |

Once clases de altura tienen tres nombres. La clase 8 tiene solo dos: solo sol y la están a dos semitonos de ella o menos, y los nombres siguientes, fa y si, están a tres semitonos, uno más de lo que alcanza una doble alteración.

La **línea de quintas** explica este recuento. Escribe los nombres a una quinta justa de distancia: … si♭ fa do sol re la mi si fa♯ do♯ sol♯ … A diferencia del círculo de quintas, la línea nunca se cierra: después de si viene fa♯, no fa. Numera las posiciones desde do = 0, de modo que sol sea 1, fa −1 y fa♯ 6. Cada siete posiciones se añade un sostenido, y la clase de altura de un nombre es 7 veces su posición, módulo 12, es decir, el resto de dividir entre 12: sol♯, en la posición 8, da 56, es decir, 8. Los 35 nombres ocupan las 35 posiciones consecutivas de fa𝄫 a si𝄪. Doce quintas hacen siete octavas, así que dos nombres separados por doce posiciones comparten clase de altura: do en 0, si♯ en 12, re𝄫 en −12. Un segmento de 35 posiciones, 2 × 12 + 11, contiene tres nombres para 11 clases de altura y dos para la última, la♭ y sol♯.

### Ejercicio práctico

Nombra todas las grafías de la clase de altura 6, y da la posición de cada una en la línea de quintas.

> *Solución:* sol♭ en −6, fa♯ en 6 y mi𝄪 en 18. Cada una está a doce posiciones de la siguiente, y 7 × −6 = −42, 7 × 6 = 42 y 7 × 18 = 126 valen todos 6 módulo 12: por ejemplo, −42 + 48 = 6.

---

## 3. Escribir una tonalidad: un nombre por grado

Una escala mayor o menor natural usa cada uno de los siete nombres exactamente una vez; la menor natural es la escala menor sin ningún grado elevado, como en las teclas blancas de la a la. Una **armadura** indica los nombres que llevan una alteración: los sostenidos se añaden en el orden fa do sol re la mi si, los bemoles en el orden si mi la re sol do fa. Con 0 a 7 sostenidos o bemoles, hay 15 tonalidades mayores, de do♭ a do♯, y 15 tonalidades menores, de la♭ menor a la♯ menor. Una tonalidad mayor y una menor con la misma armadura son **relativas**: si♭ mayor y sol menor tienen ambas dos bemoles.

Escribir una tonalidad se vuelve entonces mecánico: empieza en la tónica, toma los seis nombres siguientes, y añade la alteración de la armadura donde corresponda. Fa♯ mayor tiene seis sostenidos, fa do sol re la mi, y se escribe fa♯ sol♯ la♯ si do♯ re♯ mi♯. Su séptimo grado suena como fa, pero el nombre fa ya es el de la tónica y faltaría el nombre mi, así que el grado es mi♯. Do♭ mayor, con siete bemoles, se escribe do♭ re♭ mi♭ fa♭ sol♭ la♭ si♭.

En las 30 tonalidades, las 210 notas escritas usan 21 nombres: los 7 naturales, los 7 sostenidos y los 7 bemoles. Ninguna armadura necesita una doble alteración. En la grafía de las tonalidades, mi♯, si♯, do♭ y fa♭ solo aparecen en las 8 tonalidades con seis o siete alteraciones: fa♯ y do♯ mayor, re♯ y la♯ menor, sol♭ y do♭ mayor, y mi♭ y la♭ menor.

Tres pares de tonalidades mayores tienen las mismas clases de altura: si y do♭, fa♯ y sol♭, do♯ y re♭. Lo mismo ocurre con tres pares de tonalidades menores: sol♯ y la♭, re♯ y mi♭, la♯ y si♭. En cada par, los sostenidos y los bemoles suman 12: si mayor tiene 5 sostenidos y do♭ mayor 7 bemoles. Las dos tónicas están a doce posiciones de distancia en la línea de quintas (§2), y cada posición hacia la derecha añade un sostenido a la armadura o quita un bemol.

La sensible de una tonalidad menor puede salirse de la armadura. La menor armónica sube el séptimo grado un semitono sin cambiar su nombre, así que la sensible de fa♯ menor es mi♯ y la de do♯ menor si♯, y la de sol♯ menor es fa𝄪, la de re♯ menor do𝄪 y la de la♯ menor sol𝄪.

### Ejercicio práctico

¿En qué tonalidades mayores es mi♯ un grado de la escala?

> *Solución:* fa♯ mayor (fa♯ sol♯ la♯ si do♯ re♯ mi♯) y do♯ mayor (do♯ re♯ mi♯ fa♯ sol♯ la♯ si♯). Mi♯ es el sexto sostenido del orden fa do sol re la mi si, así que solo las armaduras con seis o siete sostenidos lo contienen.

---

## 4. Mismos trastes, dos grafías

Un guitarrista que lee una partitura en re♭ mayor y luego otra en do♯ mayor toca los mismos trastes: las dos tonalidades tienen las mismas siete clases de altura. Cada nota cambia de nombre:

| Grado | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| re♭ mayor | re♭ | mi♭ | fa | sol♭ | la♭ | si♭ | do |
| do♯ mayor | do♯ | re♯ | mi♯ | fa♯ | sol♯ | la♯ | si♯ |

Cada nombre de la segunda fila es el nombre inmediatamente inferior al de la primera. Re♭ mayor necesita 5 bemoles y do♯ mayor 7 sostenidos.

Los acordes siguen la misma regla. Una tríada apila dos terceras, y una tercera abarca tres nombres, así que una tríada toma un nombre sí y otro no: la fundamental, el nombre dos pasos por encima y el nombre cuatro pasos por encima. La tríada de tónica de re♭ mayor es re♭ fa la♭; la de do♯ mayor es do♯ mi♯ sol♯, no do♯ fa sol♯, que haría parecer la tercera una cuarta. Contar semitonos, como en MUS-001, encuentra los trastes; la sucesión de los nombres fija la grafía. Las siete tríadas construidas sobre los grados de una tonalidad son sus tríadas **diatónicas**, numeradas con números romanos: en mayúsculas para una tríada mayor, en minúsculas para una menor, y con ° para una disminuida, que GA escribe dim:

| Grado | I | ii | iii | IV | V | vi | vii° |
|---|---|---|---|---|---|---|---|
| re♭ mayor | re♭ fa la♭ | mi♭ sol♭ si♭ | fa la♭ do | sol♭ si♭ re♭ | la♭ do mi♭ | si♭ re♭ fa | do mi♭ sol♭ |
| do♯ mayor | do♯ mi♯ sol♯ | re♯ fa♯ la♯ | mi♯ sol♯ si♯ | fa♯ la♯ do♯ | sol♯ si♯ re♯ | la♯ do♯ mi♯ | si♯ re♯ fa♯ |

El número de un intervalo viene de sus nombres, como muestra la [lección 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) de Learn: de re♭ a fa se recorren tres nombres, una tercera; de do♯ a fa, cuatro, una cuarta, aunque ambos abarcan cuatro semitonos. Las cualidades de los intervalos quedan para un módulo posterior, MUS-008.

### Ejercicio práctico

Una partitura en re♭ mayor dice D♭ – B♭m – G♭ – A♭ – Fm – E♭m – A♭ – D♭. Reescríbela en do♯ mayor, en los mismos trastes.

> *Solución:* La progresión es I – vi – IV – V – iii – ii – V – I. En do♯ mayor dice C♯ – A♯m – F♯ – G♯ – E♯m – D♯m – G♯ – C♯. Cada fundamental pasa al nombre inmediatamente inferior, así que Fm se convierte en E♯m: fa no es un grado de do♯ mayor, cuyo tercer grado es mi♯.

---

## 5. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); esta lección documenta ese código sin modificarlo, y no ha ejecutado GA ni sus pruebas. Los archivos que cita no han cambiado en la rama `main` de GA en `8fe33f8`. Las lecciones [1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) y [5](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/05-keys-and-the-circle-of-fifths.mdx) de music-theory-ga, en Learn, compilan una versión anterior de GA, `a826864`, y comprueban sus nombres de nota y la grafía de sus tonalidades. Los demás números de abajo vienen de una transcripción en Python, línea por línea, del código de GA nombrado.

**Las notas conservan su grafía.** La unión [`Note`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L17) de GA comprende notas de tonalidad, que contienen un nombre y una alteración, y un caso [`Note.Chromatic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L82) que solo guarda la clase de altura. Como notas de tonalidad, do♯ y re♭ son valores distintos: las notas enarmónicas [«share a pitch class but are not equal»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L27). [`Note.Accidented.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L330) lee los 35 nombres del §2, escritos con ♯, ♭, 𝄪 y 𝄫 o con #, b, ## y bb, pero su analizador de alteraciones [no contempla ♯♯](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Accidental.cs#L147) ni ♭♭, que `Note.Sharp` y `Note.Flat` aceptan mediante sus propios [patrones de alteración](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/SharpAccidental.cs#L64). La lección 1 de Learn comprueba [ocho grafías](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L16), de do♯ a fa𝄪, frente a sus clases de altura. Los registros `Pitch` siguen el §1: contados desde el do que empieza la octava, [«Cb4 is -1 (B3) and B#3 is 12 (C4)»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Pitch.cs#L46).

**Las tonalidades se escriben con un nombre por grado.** [`Key.GetNotes`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Key.cs#L82) toma la tónica, luego los seis nombres siguientes, cada uno con sostenido o bemol cuando la [armadura](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/KeySignature.cs#L76) lo nombra, con los sostenidos añadidos desde fa por quintas y los bemoles desde si por cuartas. Es la regla del §3. Las pruebas de GA comprueban la grafía de las 15 tonalidades mayores, hasta [do♯ mayor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/MajorKeyTests.cs#L22), y de las 15 tonalidades menores, hasta [la♯ menor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/MinorKeyTests.cs#L22). La lección 5 de Learn encontró la grafía de los manuales para las [15 armaduras](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l5.txt#L3) y para [ocho tonalidades](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l5.txt#L21), y ni `GetNotes` ni `KeySignature` han cambiado desde `a826864`.

**Las notas de los acordes a partir de los nombres.** [`ChordSpelling.Spell`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/ChordSpelling.cs#L52) primero avanza el nombre de la fundamental tantos pasos como fija el acorde, y luego añade la alteración que alcanza la clase de altura buscada, como en el §4. Sus pruebas comprueban, por ejemplo, que la [tercera menor de si♭ es re♭](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/ChordSpellingTests.cs#L30), no do♯. La herramienta MCP de acordes [la llama](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/ChordMcpTools.cs#L62), igual que la [habilidad de acordes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ChordInfoSkill.cs#L291) del chatbot. Según la transcripción, a partir de la fundamental escrita de cada tríada, escribe las 210 tríadas diatónicas de las 30 tonalidades con los nombres de los manuales, E♯m en do♯ mayor incluido.

**Dónde una clase de altura se nombra a partir de una lista.** Otras partes de GA reducen una nota a su clase de altura y vuelven a nombrarla a partir de una lista de 12 nombres, una lista con sostenidos y otra con bemoles. Ninguna de las dos contiene mi♯, si♯, do♭, fa♭ ni una doble alteración.

- [`EnharmonicNamingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L11) guarda una [lista con sostenidos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L120) y una [lista con bemoles](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L141). Su método `GetEnharmonicEquivalents`, documentado como [«Gets all enharmonic equivalents for a chord»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L48), devuelve a lo sumo dos nombres por clase de altura, 17 de los 35. Su método [`DetermineContextFromKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L225) toma la tónica de la tonalidad como una clase de altura y nunca lee su parámetro `isMajor`. Una tónica 0 o 9 cuenta como natural, así que la mayor y do menor también; 1, 6 y 11 se prueban como tonalidades con sostenidos antes que como tonalidades con bemoles, así que re♭, sol♭ y do♭ mayor pasan por tonalidades con sostenidos, igual que sol y re menor, tónicas 7 y 2; y 8, 3 y 10 cuentan como tonalidades con bemoles, así que sol♯, re♯ y la♯ menor también. Comparado con la armadura, se equivoca en estas 10 de las 30 tonalidades. Ningún código lo llama, y ninguna prueba de GA nombra el servicio.
- [`KeyAwareChordNamingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/KeyAwareChordNamingService.cs#L295) toma el lado de la armadura, lo cual es correcto, y luego [nombra una fundamental](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/KeyAwareChordNamingService.cs#L302) a partir de esas listas mediante `EnharmonicNamingService.AnalyzeEnharmonicChoices`. Según la transcripción, la clase de altura 5 en do♯ mayor sale como «F», y la clase 11 en sol♭ mayor como «B». De los 210 grados de las 30 tonalidades, 12 salen mal escritos, todos en las 8 tonalidades del §3 que usan mi♯, si♯, do♭ o fa♭.

**Las closures de F#.** La capa F# de GA elige entre sus dos listas según la alteración de la propia fundamental: la [lista con bemoles](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L31) cuando la fundamental lleva bemol o es fa, la lista con sostenidos en otro caso. [`domain.diatonicChords`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L274) aplica esa elección a la tónica de la tonalidad. Según la transcripción:

| Tonalidad | Acordes devueltos | Mal escritos |
|---|---|---|
| do♯ mayor | C#, D#m, Fm, F#, G#, A#m, Cdim | Fm por E♯m, Cdim por B♯° |
| sol♭ mayor | Gb, Abm, Bbm, B, Db, Ebm, Fdim | B por C♭ |
| re menor | Dm, Edim, F, Gm, Am, A#, C | A# por B♭ |
| do menor | Cm, Ddim, D#, Fm, Gm, G#, A# | D#, G#, A# por E♭, A♭, B♭ |

En las 30 tonalidades, 18 de los 210 acordes están mal escritos, en 11 tonalidades: las 8 del §3, y re, sol y do menor, cuyas tónicas no llevan bemol. [`domain.relativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L329) hace la misma elección y, según la transcripción, responde «A# major» para sol menor, «D# major» para do menor y «B major» para la♭ menor. [`domain.transposeChord`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L248) conserva el lado de la fundamental anterior: sol subido tres semitonos se convierte en «A#». Un número de semitonos no fija el nombre, pero la♯ mayor necesitaría diez sostenidos, contando cada 𝄪 como dos, mientras que si♭ mayor tiene dos bemoles.

Estas closures responden a las herramientas MCP [`GaDiatonicChords`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GaDslTool.cs#L179) y [`GaRelativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GaDslTool.cs#L188) de GA, y a la habilidad [`DiatonicChordsSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/DiatonicChordsSkill.cs#L22) del chatbot. La descripción de la habilidad dice que usa la closure para que la grafía enarmónica sea correcta: [«spelling is correct in less-common keys (Gb major, F# minor)»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/DiatonicChordsSkill.cs#L32). Fa♯ menor es correcto. Sol♭ mayor es una de las 11 tonalidades, y las [instrucciones](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/diatonic-chords/SKILL.md#L26) de la habilidad dicen «Gb major returns Cm, not B#m», aunque sol♭ mayor no contiene ni do ni si♯: su cuarto grado es do♭, que la closure nombra «B». La grafía correcta ya existe en GA, en `Key.Notes` y `ChordSpelling.Spell`; las closures no llaman a ninguno de los dos.

**Un nombre se lee según una convención.** En notación de conjuntos, T y E valen 10 y 11. [`PitchClass.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L258) lee T y E de ese modo antes de probar los nombres de nota, así que «E» es la clase de altura 11, no la nota mi, 4. Sus [observaciones](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L232) citan las dos lecturas, y [una prueba](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Atonal/PitchClassTests.cs#L130) fija «E» en 11. El método `TryGetRootPitchClass` de GA lee en cambio una fundamental reconocida con `Note.Accidented.TryParse`, y su [observación](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Analysis/ChordIdentificationExtensions.cs#L17) todavía dice que este método lee «A» como 10, cosa que ahora solo hace `TryParseSetNotation`; `TryParse` lee «A» como la nota la, 9.

Corregir cualquiera de estas cosas corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

Según la transcripción, `domain.diatonicChords` devuelve para do♭ mayor B, Dbm, Ebm, E, Gb, Abm, Bbdim. Corrige la grafía, y explica por qué cambia incluso la tónica.

> *Solución:* C♭, D♭m, E♭m, F♭, G♭, A♭m, B♭°. La closure lee «Cb» como la clase de altura 11, y luego nombra 11 a partir de su lista con bemoles, donde 11 es «B»: el nombre do se pierde antes de elegir ningún nombre. Fa♭, clase de altura 4, sale como «E» del mismo modo.

---

## 6. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio music-theory-ga de Learn, que compila GA; la versión de GA fijada en el laboratorio pasaría primero a `5c3a52a`. Nada en ella es una medición. Las predicciones vienen de la transcripción del §5 y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso llama a los tipos o a las closures de GA en el propio proceso del laboratorio, nunca a un servidor MCP en ejecución ni a un modelo de lenguaje.

1. **Los 35 nombres.** Analiza los 35 nombres del §2 con `Note.Accidented.TryParse` y tabula sus clases de altura. Predicción: se leen los 35; 11 clases de altura reciben tres nombres y la clase 8 dos.
2. **Las 30 tonalidades.** Escribe las 30 tonalidades con `Key.Notes`. Predicción: 7 nombres distintos en cada tonalidad, 21 nombres distintos en las 210 notas, y la grafía de los manuales en todas partes.
3. **Las octavas.** Calcula con `Pitch` los números MIDI de do♭4, si♯3, mi♯4 y fa♭4. Predicción: 59, 60, 65 y 64.
4. **La closure diatónica.** Invoca `domain.diatonicChords` para las 30 tonalidades y compara la fundamental de cada acorde con `Key.Notes`. Predicción: 18 de los 210 acordes difieren, en 11 tonalidades.
5. **La closure de los relativos.** Invoca `domain.relativeKey` para las 30 tonalidades. Predicción: 3 respuestas difieren, para sol menor, do menor y la♭ menor.
6. **El servicio de nombres.** Para cada una de las 210 notas, llama a `EnharmonicNamingService.AnalyzeEnharmonicChoices` con el contexto de la armadura de la tonalidad; luego llama a `DetermineContextFromKey` con la tónica de cada tonalidad. Predicción: 12 nombres difieren, en 8 tonalidades, y 10 de los 30 contextos contradicen la armadura.
7. **Las notas de los acordes.** Llama por reflexión a `ChordSpelling.Spell`, que es interno de GA.Business.ML, sobre las 210 tríadas diatónicas. Predicción: las 210 coinciden con `Key.Notes`.

### Ejercicio práctico

El paso 4 predice 18 diferencias. ¿Qué tendría que hacer la closure para que la predicción bajara a 0, y qué tipo de entrada seguiría sin poder escribirse?

> *Solución:* Tendría que escribir a partir de los nombres, como `Key.Notes` y `ChordSpelling.Spell`, en lugar de nombrar clases de altura a partir de una lista. Con una tónica escrita, nada es ambiguo: «Db» y «C#» designan tonalidades distintas. Una tónica dada solo como clase de altura, como 1, no puede decir si la tonalidad es re♭ o do♯ mayor.

---

## 7. Errores comunes

- **Decir que do♯ y re♭ son la misma nota.** Comparten una clase de altura, una tecla de piano y un traste, no un nombre ni un grado de la escala.
- **Escribir fa en fa♯ mayor.** Cada nombre aparece una vez en una tonalidad, así que el séptimo grado es mi♯.
- **Escribir un acorde a partir de los semitonos.** Una tríada toma un nombre sí y otro no: E♯m, y no Fm, es el acorde iii de do♯ mayor.
- **Leer la octava según el sonido.** Si♯3 suena como do4, pero su número de octava sigue al nombre si.
- **Olvidar la sensible de una tonalidad menor con sostenidos.** El séptimo grado elevado de sol♯ menor es fa𝄪.
- **Nombrar las notas a partir de una lista de 12.** Una lista con sostenidos y otra con bemoles contienen 17 de los 35 nombres, y ninguno de los cuatro que necesitan 8 tonalidades.
- **Tomar la tónica de una tonalidad por una clase de altura.** La clase de altura 1 es la tónica de re♭ mayor, con 5 bemoles, y de do♯ mayor, con 7 sostenidos.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Altura** | Un sonido de altura definida, como do4, MIDI 60 |
| **Clase de altura** | Una altura sin su octava, numerada de do = 0 a si = 11 |
| **Nombre de nota** | Un nombre de do a si con una alteración: 𝄫, ♭, ♮, ♯ o 𝄪 |
| **Enarmónico** | Se dice de dos nombres, o de dos tonalidades, con las mismas clases de altura, como do♯ y re♭ |
| **Línea de quintas** | Los nombres de nota a una quinta justa de distancia, en una línea que nunca se cierra: … fa do sol re la mi si fa♯ do♯ … |
| **Armadura** | Los nombres que llevan un sostenido (añadidos desde fa, por quintas) o un bemol (añadidos desde si, por cuartas) en una tonalidad |
| **Sensible** | El séptimo grado, un semitono por debajo de la tónica; en una tonalidad menor, el séptimo grado elevado de la menor armónica |

---

## Autoevaluación

**1. ¿Cuántos nombres con a lo sumo una doble alteración tiene la clase de altura 6? Nómbralos.**
> Tres: sol♭, fa♯ y mi𝄪. Están a doce posiciones de distancia en la línea de quintas.

**2. ¿Cuál es el número MIDI de do♭4, y qué nota natural suena?**
> 59, el sonido de si3. El número de octava sigue al nombre do, así que do♭4 está un semitono por debajo de do4.

**3. Escribe la escala menor natural de la♭ menor.**
> La♭ si♭ do♭ re♭ mi♭ fa♭ sol♭: siete bemoles, un nombre por grado.

**4. La closure [`domain.relativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L329) de GA responde «A# major» para sol menor. ¿Cuál es el relativo mayor, y por qué la closure lo escribe mal?**
> Si♭ mayor. La closure nombra la tónica relativa, la clase de altura 10, a partir de su lista con sostenidos, porque la tónica sol no lleva bemol y no es fa.

**Criterio de aprobación:** Distinguir una altura, una clase de altura y un nombre de nota; dar la octava y el número MIDI de una altura escrita; enumerar los nombres de una clase de altura a partir de la línea de quintas; escribir cualquiera de las 30 tonalidades, y las tríadas de dos tonalidades enarmónicas, con un nombre por grado; y distinguir la grafía de GA basada en los nombres de sus listas de clases de altura.

---

## Base de investigación

- D. Temperley, «The Line of Fifths», *Music Analysis* 19(3), 2000, 289–319: las alturas escritas situadas en una línea de quintas en lugar de un círculo
- E. Gould, *Behind Bars*, Faber Music, 2011: las alteraciones y la notación de la altura
- E. Aldwell, C. Schachter y A. Cadwallader, *Harmony and Voice Leading*, Cengage, 2019: las escalas, las armaduras y la grafía de las tríadas
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §5 enlaza a su línea
- Learn, lecciones 1 y 5 de music-theory-ga y su salida esperada en el commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: las comprobaciones compiladas de los nombres de nota y de la grafía de las tonalidades de GA citadas en el §5
- Experimento: propuesto en el §6, no ejecutado; esta lección no contiene ninguna medición propia
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
