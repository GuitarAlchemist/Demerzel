---
module_id: mus-018-key-finding-roman-numerals-cadences
department: music
course: Identificación de la tonalidad, números romanos y cadencias
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-003-functional-harmony]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Identificación de la tonalidad, números romanos y cadencias — Lo que un recuento de acordes puede decidir y lo que no

> **Departamento de Música** | Etapa: Albedo (Intermedio) | Duración estimada: 60 minutos

## Objetivos

Al terminar esta lección, podrás:
- Enumerar las tríadas de una tonalidad mayor y de su relativa menor, y explicar por qué los acordes por sí solos no permiten distinguir esas dos tonalidades
- Puntuar una progresión frente a las 30 tonalidades mayores y menores contando sus tríadas diatónicas, y deshacer los empates con la cadencia, el acorde inicial y el modo
- Explicar por qué el V mayor de una tonalidad menor no pertenece a su escala menor natural, y qué cambia eso en un recuento
- Etiquetar una progresión con números romanos una vez elegida su tonalidad, incluidas las dominantes secundarias y los acordes semidisminuidos
- Distinguir tonalidades enarmónicas por su grafía, y nombrar la tonalidad relativa de cada una de las 30 tonalidades
- Decir en qué se diferencian los algoritmos de perfiles tonales del recuento de acordes, y qué puede y qué no puede oír cada uno
- Seguir lo que calcula la identificación de tonalidad de GA, qué muestra cada una de sus herramientas, y dónde sus respuestas y su documentación no coinciden

---

## 1. Tonalidades, tríadas diatónicas y par relativo

Una tonalidad mayor construye una tríada sobre cada grado de su escala: I, ii, iii, IV, V, vi y vii°. En do mayor son C, Dm, Em, F, G, Am y B°. La escala **menor natural** construida sobre la nota la usa las mismas siete notas, así que sus tríadas son los mismos siete acordes en otro orden: i, ii°, III, iv, v, VI y VII, es decir, Am, B°, C, Dm, Em, F y G. Una tonalidad mayor y la tonalidad menor construida sobre su sexto grado forman un **par relativo**: comparten armadura, cada nota y cada tríada diatónica. En sentido inverso, la relativa mayor está en el tercer grado de la tonalidad menor.

La armonía en menor no se queda en la escala menor natural. Para volver a su tónica, eleva el séptimo grado, sol a sol♯ en la menor. Es la escala **menor armónica**. La tríada del quinto grado pasa a ser mayor, mi sol♯ si, y la séptima de dominante E7 (mi sol♯ si re) contiene el tritono sol♯–re cuya resolución describió MUS-003 §3. La tríada del séptimo grado pasa a ser vii°, sol♯ si re. Una tonalidad menor tiene así dos dominantes sobre su quinto grado, v de la escala menor natural y V de la escala menor armónica, y sus cadencias usan V.

Con siete sostenidos o bemoles como máximo hay 15 tonalidades mayores y 15 tonalidades menores, 30 nombres en total. Sus escalas forman solo 12 conjuntos de notas distintos, uno por cada transposición de la escala diatónica. Nueve de esos conjuntos llevan dos nombres, una tonalidad mayor y su relativa menor. Los otros tres llevan cuatro, porque cada una de sus tonalidades puede escribirse de dos maneras: si y do♭ mayor con sol♯ y la♭ menor, fa♯ y sol♭ mayor con re♯ y mi♭ menor, y do♯ y re♭ mayor con la♯ y si♭ menor. Eso da 9 × 2 + 3 × 4 = 30.

### Ejercicio práctico

¿Por qué los acordes por sí solos no pueden separar do mayor de la menor en Am F C G?

> *Solución:* Las dos tonalidades comparten todas sus tríadas diatónicas, así que los cuatro acordes pertenecen a ambas, igual que cada nota. Solo el énfasis puede decidir: qué acorde abre y cuál cierra, cuál dura más o cae en los tiempos fuertes, y sobre todo una cadencia, G a C o E a Am. Aquí Am abre la progresión, lo que inclina hacia la menor, pero nada en la lista de acordes lo prueba.

---

## 2. Contar tríadas diatónicas

El detector de tonalidad más simple reduce cada acorde a su fundamental y a la calidad de su tríada: mayor, menor o disminuida. Un acorde de séptima cuenta como su tríada, así que Dm7 vale Dm y G7 vale G. Para cada una de las 30 tonalidades, cuenta cuántos de los acordes distintos de la progresión están entre las siete tríadas de la tonalidad, y se queda con las tonalidades de recuento más alto.

Para Am F C G, do mayor y la menor cuentan ambas 4 de 4. Cuatro tonalidades cuentan 3 de 4. Fa mayor contiene F, C y Am, pero su ii es Gm, no G. Sol mayor contiene C, G y Am, pero no F. Re menor contiene F, C y Am, y mi menor contiene G, Am y C. Cualquier otra tonalidad cuenta como mucho 1.

Un recuento sobre la escala menor natural pasa por alto la cadencia propia de la tonalidad menor. En Am Dm E7 Am, la tríada de E7 es mi mayor, que no está en la menor natural, donde el quinto grado lleva Em. La menor cuenta 2 de los 3 acordes distintos, no más que do mayor, fa mayor y re menor. Contar también el V armónico da a la menor 3 de 3, sola en cabeza. Esa corrección tiene un precio en las tonalidades mayores. Una **dominante secundaria** (MUS-003 §5) toma prestado el V de la forma armónica de una tonalidad menor: en C E7 Am F, E7 es el V7/vi de do mayor. Si se cuenta el V armónico, la menor obtiene los 4 acordes y do mayor 3, así que el recuento nombra la relativa menor de una progresión que se queda en do mayor. Sin él, do mayor, la menor, fa mayor y re menor cuentan 3 cada una. Ninguna de las dos maneras de contar acierta con las dos progresiones: el recuento necesita la ayuda del orden de los acordes.

### Ejercicio práctico

Puntúa Dm G C frente a do mayor, la menor, re menor y sol mayor.

> *Solución:* Do mayor cuenta 3 de 3 (ii, V, I), y la menor también (iv, VII, III). Re menor cuenta 2: Dm y C, sus i y VII, pero G es una tríada mayor, no su iv natural. Sol mayor cuenta 2: G y C, sus I y IV, pero su V es re mayor, no Dm.

---

## 3. Deshacer el empate: cadencia, acorde inicial y modo

Un recuento deja empatadas una tonalidad y su relativa menor siempre que todos los acordes son diatónicos, y también puede dejar empatadas otras tonalidades. Tres tipos de indicio deshacen el empate, de más fuerte a más débil.

- **La cadencia.** Una progresión que termina en V–I, o V7–I, confirma la tonalidad de ese I. En una tonalidad menor, el V de la cadencia es el V mayor de la escala menor armónica. Una semicadencia termina en V, y una cadencia plagal termina en IV–I. Ninguna de las dos confirma una tonalidad del mismo modo, y una cadencia rota, V–vi, evita por completo la tónica.
- **El acorde inicial.** Una progresión que empieza en la tríada de tónica de una de las tonalidades empatadas se inclina hacia esa tonalidad.
- **La convención.** Cuando nada más decide, un detector tiene que elegir, por ejemplo la tonalidad mayor.

Estas reglas resuelven los ejemplos anteriores. Am F C G empieza en Am y va a la menor, mientras que C G Am F va a do mayor. Dm G C termina en G–C, V–I de do mayor, así que do mayor va primero, aunque la menor tenga el mismo recuento. En Am Dm E7 Am, E7–Am es el V7–i de la menor, lo que decide entre las cuatro tonalidades que cuentan 2. C D G C muestra que una cadencia puede pesar más que el recuento. Sol mayor y mi menor contienen los tres acordes distintos y do mayor solo dos, ya que D es V/V, una dominante secundaria. Aun así la progresión termina en G–C y está en do mayor. Un detector que da a la cadencia el peso de dos acordes, como hace GA (§7), pone do mayor primero.

Hay música sin tonalidad mayor o menor que encontrar. G F C G está en sol mixolidio, el modo de la escala mayor con la séptima rebajada, así que su acorde de F es ♭VII. Su recuento da a do mayor y a la menor 3 de 3 y a sol mayor 2, y su final C–G es plagal, así que ninguna cadencia habla por sol. C B♭ F C está en do mayor con un ♭VII prestado de do menor; el recuento prefiere fa mayor y re menor, que contienen los tres acordes distintos, a do mayor, que contiene dos. Un vamp dórico, Dm7 Em7 repetido, cuenta 2 de 2 para do mayor y la menor. Un detector cuyas respuestas son las 30 tonalidades mayores y menores solo puede nombrar la tonalidad cuyas notas usan estas progresiones.

### Ejercicio práctico

D C♯7 F♯m empieza en D. ¿En qué tonalidad está?

> *Solución:* Fa♯ menor. D y F♯m están ambos en re mayor, la mayor, si menor y fa♯ menor, que cuentan 2 de 3 cada una, mientras que la tríada de C♯7 no está en ninguna de sus formas naturales. C♯7–F♯m es el V7–i de fa♯ menor, la cadencia de la escala menor armónica, y pesa más que el inicio en D.

---

## 4. Números romanos

Una vez elegida la tonalidad, cada acorde recibe un **número romano**: el grado de su fundamental en la escala de la tonalidad, en mayúsculas para una tríada mayor, en minúsculas para una menor, con ° para una tríada disminuida, ø para una séptima semidisminuida, + para una tríada aumentada, y la cifra de la séptima cuando la hay. En do mayor, Dm7 G7 Cmaj7 es ii7 V7 Imaj7. En la menor, Bø7 E7 Am es iiø7 V7 i. La tríada de Bø7, si re fa, es disminuida: Bø7 es el mismo acorde que Bm7♭5, una séptima menor con la quinta rebajada, y no una tríada menor. E7 es V7, de la escala menor armónica, y Am es i.

Los números llevan la función además del grado. En C E7 Am F G7 C, E7 es **V7/vi**, la dominante de Am, y no un acorde «III7» de do mayor: el número nombra el acorde al que conduce (MUS-003 §5). Un acorde cuya fundamental está fuera de la escala recibe una alteración: B♭ en do mayor es ♭VII.

Un etiquetador que solo lee el grado de la fundamental y la calidad del acorde escribirá III para E7 en do mayor. Eso describe el acorde, pero oculta su función, y no hay que confundir las dos convenciones.

### Ejercicio práctico

Etiqueta C E7 Am F G7 C en do mayor.

> *Solución:* I, V7/vi, vi, IV, V7, I. La progresión tonicaliza vi durante un acorde y luego vuelve a I por IV y V7.

---

## 5. Tonalidades enarmónicas y tonalidad relativa

Re♭ mayor y do♯ mayor suenan igual en una guitarra y contienen las mismas clases de altura, pero son tonalidades distintas sobre el papel. Re♭ mayor tiene cinco bemoles; do♯ mayor tiene siete sostenidos, y sus acordes se escriben C♯, F♯ y G♯. Una hoja guía que dice D♭ G♭ A♭ D♭ está en re♭ mayor, y la grafía es la prueba. Un detector de tonalidad que convierte cada acorde en una clase de altura antes de puntuar da a las dos tonalidades la misma puntuación, así que no puede usar esa prueba.

La relativa también es una cuestión de grafía. La relativa menor de si mayor es sol♯ menor, sobre el sexto grado de si mayor, y ambas tienen cinco sostenidos. La♭ menor contiene las mismas clases de altura, pero tiene siete bemoles y es la relativa menor de do♭ mayor. Los 12 nombres de tonalidad de los tres conjuntos que llevan cuatro nombres forman seis pares enarmónicos del mismo modo: si y do♭ mayor, fa♯ y sol♭ mayor, do♯ y re♭ mayor, y sol♯ y la♭, re♯ y mi♭, la♯ y si♭ menor.

### Ejercicio práctico

Nombra las tonalidades relativas de fa♯ mayor y de re♯ menor.

> *Solución:* Re♯ menor y fa♯ mayor, cada una con seis sostenidos. Mi♭ menor y sol♭ mayor tienen las mismas notas, pero con seis bemoles.

---

## 6. Perfiles tonales: pesar las notas en lugar de contar los acordes

El recuento de acordes es una familia de detectores de tonalidad. Otra pesa las notas mismas. Longuet-Higgins y Steedman (1971) hallaron la tonalidad de los 48 sujetos de fuga de *El clave bien temperado* de Bach eliminando, nota a nota, las tonalidades cuya escala no contiene la nota oída, con una regla que favorece la tonalidad cuya tónica, o si no la dominante, es la primera nota cuando la eliminación no decide. Krumhansl y Kessler (1982) preguntaron a oyentes hasta qué punto cada una de las 12 clases de altura encajaba en un contexto tonal. Las respuestas dieron un **perfil tonal** para las tonalidades mayores y otro para las menores, el más alto para la tónica y el más bajo para las notas fuera de la escala. En el **algoritmo de Krumhansl–Schmuckler** (Krumhansl, 1990, cap. 4), la duración total de cada clase de altura en un pasaje se correlaciona con las 24 rotaciones de los dos perfiles, y gana la tonalidad de correlación más alta. Temperley (1999) reconsideró ese algoritmo y propuso revisiones. Su libro (Temperley, 2001) trata la identificación de la tonalidad con reglas de preferencia, junto con el metro, la armonía y la grafía de las alturas, y deja que la tonalidad cambie a lo largo de una pieza.

La diferencia con un recuento de acordes está en el peso. Un método de perfiles oye que un acorde dura cuatro compases y que la nota de tónica vuelve una y otra vez, así que puede separar una tonalidad de su relativa menor donde un recuento de acordes distintos no puede. Una lista de acordes sin duraciones no le da nada que pesar, y ninguna de las dos familias oye la línea del bajo, el metro o la frase a menos que se añadan a su entrada. Además, ambas eligen solo entre tonalidades mayores y menores, así que un pasaje dórico o mixolidio recibe la tonalidad mayor o menor cuyas notas usa.

### Ejercicio práctico

C dura cuatro compases, y luego Am, F y G un compás cada uno. ¿Por qué un perfil ponderado por las duraciones puede separar aquí do mayor de la menor, cuando un recuento de acordes distintos no puede?

> *Solución:* Las dos tonalidades contienen los cuatro acordes, así que el recuento empata. En las duraciones, do, mi y sol pesan mucho más que la, y do es la que más pesa. El perfil de do mayor es el más alto en do, así que su correlación con el pasaje supera la de la menor, cuyo perfil es el más alto en la.

---

## 7. Dónde está GA

GA es la biblioteca de teoría musical y el chatbot del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); esta lección documenta ese código sin cambiarlo, y no ha ejecutado GA ni sus pruebas. El servicio y sus llamadores no han cambiado hoy en la rama `main` de GA. Los números vienen de dos fuentes. La [lección 11 de ga-ai](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/ga-ai/11-the-chords-the-key-skill-reads.md) de Learn compila el servicio de GA e imprime sus respuestas, con la etiqueta `6baf32e`, el último commit que cambió el servicio. Los demás números vienen de una transcripción en Python, línea a línea, del servicio, de la herramienta del chatbot y de la herramienta de lista, que reproduce cada respuesta que Learn imprime para esta versión del servicio, en 53 líneas.

**Un servicio, seis llamadores.** [`KeyIdentificationService.Identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L175) puntúa las 30 tonalidades del §1 con el patrón mayor y el [patrón de la escala menor natural](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L40), y cuenta [acordes distintos](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L182). Las habilidades [`KeyIdentificationSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L47) y [`ProgressionCompletionSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ProgressionCompletionSkill.cs#L51) del chatbot, y la herramienta MCP [`ga_key_identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L62), lo llaman con acordes leídos en una frase. La herramienta MCP [`ga_key_from_progression`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L177) y las clausuras DSL [`domain.analyzeProgression`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L405) y [`domain.progressionCompletion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L739) lo llaman con una lista de acordes.

**El V del modo menor: en el orden, no en el recuento.** El patrón de la escala menor natural pone una tríada menor en el quinto grado, y una séptima de dominante solo cuenta en una tonalidad menor sobre el [séptimo grado](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L207), como VII7, así que ni E ni E7 cuentan en la menor. GA eligió el recuento natural del §2, con el que C E7 Am F empata cuatro tonalidades y do mayor va primero por su acorde inicial. La cadencia vuelve en el orden de los candidatos:

```csharp
            .Where(s => s.Candidate.MatchCount > 0)
            .OrderByDescending(s => s.Candidate.MatchCount + s.Cadence)
            .ThenByDescending(s => s.OpensOnTonic)
            .ThenByDescending(s => s.Candidate.Key.EndsWith("major", StringComparison.OrdinalIgnoreCase))
            .ThenBy(s => s.Candidate.Key)
            .Select(s => s.Candidate)];
```

[`CadenceWeight`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L233) suma 2 cuando los dos últimos acordes son el V de la tonalidad, como tríada mayor o como séptima de dominante, y su tríada de tónica. Luego vienen el acorde inicial y la tonalidad mayor, como en el §3, y al final el nombre de la tonalidad. Am Dm E7 Am pone por tanto la menor primero, con 2 de 3. El comentario del servicio sobre C E7 Am F G7 C dice que la menor [coincide con más acordes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L165). Eso era cierto del recuento armónico, no de este código: do mayor y la menor cuentan ambas 4 de 5, y la cadencia G7–C pone do mayor primero, como exige [la prueba](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L104).

**Dos recuentos para una progresión.** [`IsChordDiatonic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L251) sí [acepta el V armónico](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L265) en una tonalidad menor, y la confianza de la herramienta de lista cuenta cada acorde de la lista, repeticiones incluidas, [con él](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L187). El chatbot muestra en cambio el recuento de `Identify`, como [«N/M chords diatonic»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L105). Para Am Dm E7 Am la herramienta de lista da la menor con 4/4 (100%), como afirma la [prueba de la clausura](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L97) para su confianza, mientras que `Identify` cuenta 2 de 3. La herramienta de lista mantiene el orden de `Identify` pero [calcula su propia puntuación](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L204), así que su primera tonalidad puede mostrar la confianza más baja. Para C E7 Am F G7 C, su mejor apuesta es do mayor con 5/6 (83%), seguida de la menor con 6/6 (100%). Para C D G C, es do mayor con 3/4 (75%), seguida de sol mayor y mi menor con 4/4 (100%).

**Lo que lee el chatbot.** Los acordes de una frase se leen con [una expresión regular](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L325) cuyo `\b` final pierde un sostenido delante de un espacio. En «What key is F# B C# F# in?», F♯ se lee como F y C♯ como C. Los signos ♭ y ♯ no se leen, C° se lee como un acorde de do mayor, y CM7, CΔ7 y Cø7 se omiten. Los acordes repetidos se [eliminan](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L299) antes de que `Identify` los vea. «What key is C D G C in?» se lee como C D G, cuyos dos últimos acordes son el V–I de sol mayor, y la respuesta es [sol mayor](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L92). El analizador de acordes cambia min por m y luego conserva la tríada borrando [todo a partir de la primera cifra](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L319), junto con un maj, aug, sus o add justo delante. Bm7♭5, escrito Bm7b5, se convierte en Bm, una tríada menor, así que un iiø7 nunca coincide con ii°. AM7 se convierte en un acorde de la menor, y una [prueba](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L149) afirma que AM7, leído como acorde menor, es diatónico a do mayor. En los cifrados habituales, CM7 es Cmaj7, una séptima mayor. Learn planteó las seis progresiones de manual de su lección en las 15 tonalidades de su modo, 90 preguntas. En [esta versión](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L84), 50 ponen primero la tonalidad del manual, 13 la empatan en cabeza sin ponerla primero, 11 la dejan fuera del grupo de cabeza, y 16 pierden o leen mal un acorde.

**El grupo de cabeza que ve el modelo.** La herramienta entrega al modelo las tonalidades empatadas en cabeza, y luego hasta tres más tomadas de la lista ordenada:

```csharp
        var topScore = candidates[0].MatchCount;
        var topTied  = candidates
            .Where(c => c.MatchCount == topScore)
            .Select(ToCandidate)
            .ToArray();
        var partial  = candidates
            .Skip(topTied.Length)
            .Take(MaxPartialCandidates)
            .Select(ToCandidate)
            .ToArray();
```

El grupo de cabeza se corta por el recuento de la primera tonalidad, mientras que el orden usa el recuento más la cadencia, así que los dos discrepan siempre que la cadencia sube una tonalidad de recuento más bajo. Para C♯m7b5 F♯7 Bm, iiø7 V7 i de si menor, si menor va primero con 1 de 3 gracias a su cadencia. El grupo de cabeza son entonces las [seis tonalidades con 1 de 3](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L103), y sol♯ menor, con 2 de 3, aparece entre las coincidencias parciales. Otras cinco tonalidades cuentan 2 de 3, la mayor, si mayor, do♭ mayor, la♭ menor y fa♯ menor, y no aparecen en ninguna de las dos listas. Para Bm7b5 E7 Am, el ii–V–i menor del [propio corpus de GA](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Corpus/Progressions/README.md#L37), el grupo de cabeza tiene seis tonalidades con 1 de 3. Las coincidencias parciales repiten tres de ellas, do mayor, re mayor y fa mayor, y las cuatro tonalidades con 2 de 3, la mayor, mi menor, fa♯ menor y sol mayor, quedan fuera. El prompt de la habilidad llama al grupo de cabeza [«all tied at the highest score»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L102), lo que aquí no es. La prueba del corpus usa una segunda definición, el [recuento más alto](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Corpus/ProgressionCorpusMatrixTests.cs#L440) entre todas las tonalidades, que deja la menor fuera del grupo de cabeza para Bm7b5 E7 Am.

**Tonalidades enarmónicas y tonalidades relativas.** Las fundamentales de los acordes se convierten en [clases de altura](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L106) antes de puntuar, así que las gemelas enarmónicas del §5 reciben siempre la misma puntuación, y es el [nombre de la tonalidad](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L227) el que decide entre ellas. D♭ G♭ A♭ D♭ pone [do♯ mayor primero](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L88), y las 13 preguntas de la tabla de Learn que empatan la tonalidad del manual en cabeza sin ponerla primero son todas empates de ese tipo. La relativa de cada tonalidad es la [primera tonalidad del otro modo](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L98) con las mismas clases de altura, así que [6 de las 30](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L107) se escriben a partir de la gemela: la relativa de si mayor se da como la♭ menor, y la de sol♯ menor como do♭ mayor.

**Números romanos.** [`romanFor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L355) toma el grado de la posición de la fundamental en la escala mayor o menor natural, y la caja y el signo del acorde. Am Dm E7 Am se etiqueta [i iv V i](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L99), y C Bdim Bm7b5 Caug en do mayor [I vii° viiø I+](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L110). Una fundamental fuera de la escala recibe [un signo de interrogación](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L374), así que B♭ en do mayor da «?», y no ♭VII. No hay notación de dominante secundaria: E7 en do mayor se etiqueta por su grado, como el acorde III del §4.

**Lo que dice la documentación.** Las instrucciones de la habilidad dan un [ejemplo con un solo candidato](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L60), Dm G C en do mayor con 3/3, pero la herramienta devuelve do mayor y la menor [empatadas](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L9), como lo están siempre las tonalidades relativas. Las instrucciones esperan [«almost always 2»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L64) tonalidades empatadas, y la documentación de la herramienta [«often 1 element»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L131); los conjuntos enarmónicos dan cuatro, y los ejemplos de arriba seis. Las instrucciones también remiten al servicio en [una ruta](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L88) donde ya no está. Un comentario de prueba dice que [si menor no tiene A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L86) como tríada mayor. En realidad, A es el VII de si menor natural, y la relativa de mi mayor es do♯ menor; la aserción en sí se cumple.

Las issues [#771](https://github.com/GuitarAlchemist/ga/issues/771) y [#772](https://github.com/GuitarAlchemist/ga/issues/772) de GA, ambas abiertas, señalan cómo lee el chatbot los acordes, cómo agrupa el grupo de cabeza, los empates enarmónicos, las tonalidades relativas y el ejemplo con un solo candidato. Corregir todo esto corresponde a los responsables de GA; esta lección solo lo describe.

### Ejercicio práctico

`ga_key_identify` responde sol mayor para «What key is C D G C in?», mientras que `ga_key_from_progression`, con ["C", "D", "G", "C"], responde do mayor. Explica las dos respuestas.

> *Solución:* La herramienta del chatbot lee C D G, porque elimina la C repetida. Sus dos últimos acordes, D y G, son el V–I de sol mayor, así que sol mayor recibe el peso de cadencia además de su recuento de 3. La herramienta de lista mantiene la lista tal cual, así que el final es G–C, V–I de do mayor. El recuento de 2 de do mayor más el peso de cadencia de 2 supera entonces los 3 de sol mayor. Do mayor es la respuesta de manual: D es V/V. La herramienta de lista aun así la pone primera con la confianza más baja, 3/4 (75%), frente al 4/4 (100%) de sol mayor.

---

## 8. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio ga-ai de Learn, que compila el servicio de GA. Nada en ella es una medición. Las predicciones vienen de la transcripción del §7 y se escriben antes de cualquier ejecución; una versión posterior de esta lección dará los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en marcha ni a un modelo de lenguaje.

1. **Identify sobre un corpus fijo.** Llamar a `Identify` con Am F C G, C G Am F, C E7 Am F G7 C, Am Dm E7 Am, D C♯7 F♯m, C D G C, Dm7 G7, G F C G, C B♭ F C (escrito C Bb F C) y Dm7 Em7 Dm7 Em7. Predicción, primera tonalidad y su recuento: la menor 4/4, do mayor 4/4, do mayor 4/5, la menor 2/3, fa♯ menor 2/3, do mayor 2/3, do mayor 2/2, do mayor 3/3, fa mayor 3/3 y do mayor 2/2.
2. **La herramienta del chatbot con las mismas progresiones.** Preguntar a `KeyIdentificationMcpTools.IdentifyKey` «What key is … in?» para cada una. Predicción: C D G C se lee como C D G y recibe la respuesta sol mayor, con mi menor empatada; Am Dm E7 Am se lee como Am Dm E7, con la menor, do mayor, fa mayor y re menor empatadas con 2/3, la menor primero.
3. **La herramienta de lista.** Llamar a `GaKeyFromProgression` con C E7 Am F G7 C y C D G C. Predicción: do mayor con 5/6 (83%) por delante de la menor con 6/6 (100%), y do mayor con 3/4 (75%) por delante de sol mayor y mi menor con 4/4 (100%).
4. **Dos definiciones del grupo de cabeza.** Para Bm7b5 E7 Am, calcular el grupo de cabeza de la herramienta y sus coincidencias parciales, y el grupo de cabeza de la prueba del corpus. Predicción: seis tonalidades con 1/3 con la menor primero; coincidencias parciales do mayor, re mayor y fa mayor, ya en el grupo de cabeza; el grupo de cabeza del corpus la mayor, mi menor, fa♯ menor y sol mayor, sin la menor.
5. **El V armónico contado.** En una copia del servicio dentro del laboratorio, nunca en GA mismo, contar una tríada mayor o una séptima de dominante sobre el quinto grado de una tonalidad menor. Predicción: Am Dm E7 Am da la menor 3/3, sola; C E7 Am F da la menor 4/4 por delante de do mayor 3/4; C E7 Am F G7 C sigue poniendo do mayor primero, con 4/5 más la cadencia, por delante de la menor con 5/5.
6. **Grafía enarmónica.** Llamar a `Identify` con D♭ G♭ A♭ D♭ y con C♯ F♯ G♯ C♯, ambas como listas. Predicción: la misma respuesta para las dos, do♯ mayor primero, luego re♭ mayor.

### Ejercicio práctico

El paso 5 cambia el recuento. ¿Qué resultado mostraría que el cambio merece la pena, y cuál que no?

> *Solución:* Merece la pena si cadencias en menor como Am Dm E7 Am se encuentran sin ayuda del orden, mientras las progresiones en mayor con una dominante secundaria conservan su tonalidad. C E7 Am F muestra que no: gana la relativa menor, ya que no hay cadencia final que corrija el recuento. Una prueba justa necesita un corpus con los dos tipos, con las tonalidades anotadas antes de la ejecución.

---

## 9. Errores comunes

- **Tomar un empate por una respuesta.** Una tonalidad y su relativa menor siempre empatan en sus acordes; el énfasis decide entre ellas.
- **Contar el V armónico en todas partes.** Encuentra las cadencias en menor, y arrastra las dominantes secundarias de las tonalidades mayores hacia la relativa menor.
- **Leer una lista de acordes sin su orden ni sus repeticiones.** La cadencia está en el orden, y una tónica repetida es énfasis.
- **Reducir los acordes a clases de altura antes de elegir entre tonalidades enarmónicas.** La grafía es la prueba.
- **Leer «N/M chords diatonic» como confianza.** Dos de las herramientas de GA calculan N distintos para los mismos acordes, y la primera tonalidad puede mostrar el más bajo.
- **Nombrar un modo con un detector de tonalidades mayores y menores.** Los vamps dóricos y mixolidios salen como la tonalidad cuyas notas usan.
- **Fiarse de un grupo de cabeza sin preguntar cómo se cortó.** Cortados por el recuento de la primera tonalidad o por el recuento más alto de todas las tonalidades, los mismos candidatos dan listas distintas, y ninguno de los dos cortes sigue el orden por recuento más cadencia.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Tríada diatónica** | Una tríada construida con las notas de la escala de una tonalidad sobre uno de sus siete grados |
| **Par relativo** | Una tonalidad mayor y la tonalidad menor construida sobre su sexto grado, con la misma armadura y las mismas tríadas |
| **Escala menor natural** | La escala menor con las notas de la armadura; su tríada del quinto grado es menor |
| **Escala menor armónica** | La escala menor con el séptimo grado elevado, que vuelve mayor la tríada del quinto grado |
| **Cadencia auténtica** | V o V7 a I (o i), el final que confirma una tonalidad |
| **Dominante secundaria** | El V o V7 de un acorde distinto de I, escrito V7/vi para la séptima de dominante de vi |
| **Número romano** | El grado de un acorde en la tonalidad, con caja y signos para su calidad |
| **Tonalidades enarmónicas** | Tonalidades del mismo modo cuyas tónicas son una misma altura escrita de dos maneras, como re♭ mayor y do♯ mayor |
| **Perfil tonal** | El peso de cada una de las 12 clases de altura en un contexto de tonalidad mayor o menor |
| **Algoritmo de Krumhansl–Schmuckler** | Correlacionar las duraciones de un pasaje por clase de altura con las 24 rotaciones de los perfiles tonales |

---

## Autoevaluación

**1. ¿Qué tonalidades empatan para Em C G D, y cuál decide el acorde inicial?**
> Sol mayor y mi menor cuentan 4 de 4. La progresión empieza en Em, la tríada de tónica de mi menor, así que un detector que pesa el acorde inicial elige mi menor, como exige la [prueba](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L122) de GA.

**2. ¿Por qué un recuento sobre la escala menor natural deja Am Dm E7 Am en 2 de 3 para la menor?**
> La tríada de E7 es mi mayor, el V de la escala menor armónica. El quinto grado de la escala menor natural lleva Em, así que E7 no se cuenta.

**3. Una hoja guía dice D♭ G♭ A♭ D♭, y un detector de tonalidad responde do♯ mayor. ¿Qué ha fallado?**
> El detector convirtió los acordes en clases de altura, que re♭ mayor y do♯ mayor comparten, y luego eligió por el nombre. La grafía, con cinco bemoles en lugar de siete sostenidos, dice re♭ mayor.

**4. Para C♯m7b5 F♯7 Bm, `ga_key_identify` devuelve seis tonalidades como candidatas de cabeza, [«tied at the highest match count»](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L140), con 1 de 3. ¿En qué tonalidad está, y qué falta?**
> Si menor: iiø7 V7 i. El grupo de cabeza se corta por el recuento de la primera tonalidad, mientras que el orden añade la cadencia. Faltan en el grupo de cabeza las tonalidades que cuentan 2 de 3: sol♯ menor aparece entre las coincidencias parciales, y otras cinco no aparecen en ningún sitio.

**Criterio de aprobación:** Nombrar las tríadas de una tonalidad y de su relativa; puntuar una progresión contando tríadas diatónicas y deshacer el empate con la cadencia y el acorde inicial; explicar el punto ciego del recuento sobre la escala menor natural y el precio de contar el V armónico; etiquetar una progresión con números romanos, dominantes secundarias incluidas; distinguir por la grafía tonalidades enarmónicas y tonalidades relativas; y decir qué herramienta de GA muestra qué recuento.

---

## Base de investigación

- M. Gotham, K. Gullings, C. Hamm, B. Hughes, B. Jarvis, M. Lavengood y J. Peterson, *Open Music Theory*, versión 2, VIVA Open Publishing, 2021 (CC BY-SA 4.0): las tríadas diatónicas, las escalas menores natural y armónica, y los números romanos
- S. Kostka, D. Payne y B. Almén, *Tonal Harmony*, 7.ª edición, McGraw-Hill, 2013: números romanos, cadencias y dominantes secundarias
- H. C. Longuet-Higgins y M. J. Steedman, «On interpreting Bach», *Machine Intelligence* 6, 1971, pp. 221–241: la identificación de la tonalidad por eliminación de tonalidades nota a nota
- C. L. Krumhansl y E. J. Kessler, «Tracing the dynamic changes in perceived tonal organization in a spatial representation of musical keys», *Psychological Review* 89(4), 1982, pp. 334–368: los perfiles tonales obtenidos con sonidos de sondeo
- C. L. Krumhansl, *Cognitive Foundations of Musical Pitch*, Oxford University Press, 1990, capítulo 4, «A key-finding algorithm based on tonal hierarchies»: el algoritmo de Krumhansl–Schmuckler
- D. Temperley, «What's key for key? The Krumhansl-Schmuckler key-finding algorithm reconsidered», *Music Perception* 17(1), 1999, pp. 65–100
- D. Temperley, *The Cognition of Basic Musical Structures*, MIT Press, 2001: la identificación de la tonalidad con reglas de preferencia
- Wikipedia, «Chord names and symbols (popular music)»: CM7, CΔ7 y Cmaj7 como nombres de la séptima mayor
- Código fuente de GA en el commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: cada hecho de código del §7 enlaza a su línea; issues #771 y #772 de GA
- Learn, lección 11 de ga-ai y su salida esperada en el commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: las respuestas compiladas del servicio de GA citadas en el §7
- Experimento: propuesto en el §8, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03); traducción al español: U (sin revisión de un hablante nativo)
