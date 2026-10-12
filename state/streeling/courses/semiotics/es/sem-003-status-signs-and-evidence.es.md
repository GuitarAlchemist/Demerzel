---
module_id: sem-003-status-signs-and-evidence
department: semiotics
course: "Signos de estado y pruebas en el trabajo agéntico"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-12-003
version: "0.1.0"
---

# Signos de estado y pruebas en el trabajo agéntico

> **Departamento de Semiótica** | Nivel: intermedio | Etapa: Albedo | Duración: 35 minutos | Borrador español pendiente de revisión

## Objetivos

Aprenderás a distinguir una palabra de estado del hecho que pretende describir, a leer un registro de producción de Streeling sin convertir una comprobación limitada en un veredicto final y a redactar un traspaso entre agentes verificable frente a un artefacto fijado. También distinguirás qué demuestra un esquema, una compilación local y una lectura pública.

## La decisión del proyecto

Un agente redacta una lección de Streeling y otro informa «sin hallazgos» tras leer la fuente y las respuestas. ¿Qué debe comunicar el coordinador al siguiente agente: **borrador**, **listo**, **revisado** o **publicado**? Esa palabra determina si se dirige a un alumno al curso público, se pide una inspección al revisor o se solicita una corrección al autor. Un término demasiado fuerte puede hacer que se omita un paso pendiente.

Esta lección utiliza el [registro de producción real de SEM-002](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/course-productions/cp-semiotics-2026-10-11-002.json), su [acta de revisión IA limitada](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/sem-002-subject-review-2026-10-11.md), el [esquema de producción](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/schemas/course-production.schema.json) y el [informador de progreso](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py). Todos los enlaces a fuentes de Demerzel fijan el commit `c453a91d1c4d913af72c28779eff826659c1d654`. Analizamos esa instantánea, sin afirmar que el estado actual de producción o del sitio siga siendo igual.

## 1. ¿A qué se refiere un signo de estado?

[SEM-001](sem-001-signs-in-governance.es.md) introdujo el signo, su objeto y la interpretación del lector. En un traspaso, `reviewed` es un **símbolo** cuyo significado depende de una convención compartida. Un enlace al acta puede actuar como **índice** hacia un artefacto concreto. Una marca de verificación verde es otro signo compacto, pero necesita una interpretación acordada, un predicado nombrado y procedencia. Ninguno de estos signos realiza por sí mismo una revisión.

Las palabras de la pregunta inicial designan posibles afirmaciones, **no** una nueva máquina de estados de Streeling:

| Palabra del mensaje | Posible afirmación comprobable | Prueba necesaria antes de usarla sin matices |
| --- | --- | --- |
| `draft` | Existe un archivo fuente | Ruta y revisión exacta |
| `ready` | Se superó una puerta de entrada definida | Nombre del control, entradas, resultado y fecha; ¿listo *para qué*? |
| `reviewed` | Un revisor examinó un alcance definido | Acta, revisor, alcance, resultado y revisiones pendientes |
| `published` | Un alumno puede recuperar la versión prevista | Ruta desplegada, lectura anónima y procedencia de la fuente coincidente |

Son **pruebas de comunicación**, no cuatro valores implementados. El esquema fijado permite `in_progress`, `review_pending`, `published`, `rejected` y `failed`; no define `draft`, `ready` ni `reviewed`. Es preferible decir «existe el borrador inglés» o «listo para revisión limitada de la fuente» cuando eso es lo probado, sin insinuar una transición inexistente del esquema.

### Ejercicio 1 — Identificar el objeto

Un traspaso solo dice «SEM-002 está listo». Da dos significados sustancialmente distintos de `ready` y reescribe la frase para que uno pueda comprobarse. ¿Incluye el esquema el valor `ready`?

> **Respuesta:** Puede estar listo para revisar la fuente o listo para desplegar tras todas las revisiones. Por ejemplo: «La fuente inglesa de SEM-002 en el commit `c453a91d1c4d913af72c28779eff826659c1d654` está lista **para una revisión limitada de la fuente y sus respuestas**; la revisión final de producción y la publicación siguen incompletas». El esquema no contiene `ready`.

## 2. Leer el registro y después el acta

En la revisión fijada, el registro de SEM-002 dice `status: in_progress`. Investigación, esquema del curso y contenido están completos; traducción está incompleta con `languages: ["en"]`; revisión y publicación tienen `completed: false`. El acta IA separada informa **sin hallazgos en el alcance limitado de la fuente y sus respuestas**. Deja expresamente pendientes las comprobaciones humanas de la materia, alumnos, idiomas y Learn público. Una inspección acotada puede haber ocurrido mientras la fase de revisión final sigue incompleta.

El error semiótico sería hacer que `reviewed` abarcara cualquier clase de revisión. «La revisión previa IA de la fuente y las respuestas no encontró problemas» es concreto. «Curso revisado» podría interpretarse como aprobación editorial o humana final y encaminar mal al siguiente agente. Tampoco basta con identificar al revisor: el acta debe indicar qué se examinó y qué quedó fuera. Una marca del registro es una afirmación de un archivo; necesita una prueba trazable para ser un hecho fiable en el traspaso.

El [informador de progreso](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py#L89-L107) cuenta una aprobación solo cuando `phases.review.completed` es verdadero **y** `phases.review.verdict` es `approved`. SEM-002 no satisface ese predicado en la instantánea. El contador consulta registros: no evalúa por sí solo la exactitud de la materia. Si alguien escribiera ambos valores manualmente sin una revisión fiable, el contador tampoco demostraría que esta ocurrió.

### Ejercicio 2 — Delimitar una afirmación de revisión

Para SEM-002 fijado, elige: (A) «No hubo ninguna revisión»; (B) «El curso superó todas las revisiones»; (C) «Una comprobación IA limitada de fuente y respuestas no encontró problemas; la fase de revisión de producción sigue incompleta». Explica por qué fallan las otras.

> **Respuesta:** C. A contradice el acta de la inspección limitada. B supera su alcance: quedan abiertas las revisiones humanas de materia, alumnos, idiomas y sitio público; `phases.review.completed` es falso. «Sin hallazgos» se refiere al alcance declarado, no a todo posible defecto.

## 3. Una forma válida no es una transición verificada

El esquema limita tipos de campos y valores `status`. Exige estado, investigación, esquema del curso, contenido y marca de tiempo. Cuando aparecen las fases de revisión y publicación, sus campos `completed` son booleanos. **No** establece una regla cruzada como «`status: published` implica `publish.completed: true`». Por eso un registro puede cumplir la sintaxis del esquema y a la vez formular una afirmación operativa contradictoria. Esto describe los límites del esquema, no afirma que exista tal registro defectuoso en producción.

La [comprobación previa de cursos](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_preflight.py) valida esquemas, nombres de archivo, frontmatter, archivos de idioma declarados, número de palabras inglesas y señales de ejercicios respondidos. Su única regla explícita de coherencia de estado exige que `in_progress` tenga falsas las marcas de revisión y publicación. No consulta el sitio público ni califica la materia. Pasarla significa que se cumplieron esos predicados, no «aprobado por alumnos» ni «en línea en Learn».

Imagina un cambio **sintético** del registro SEM-002: solo `status` pasa a `published` y `phases.publish.completed: false` permanece. El esquema admite ambos valores individuales y no los vincula. Como la única regla de coherencia de la comprobación previa se aplica a `in_progress`, ese caso ficticio la eludiría. No lo introduzcas en el repositorio. La lección es examinar el registro, un comprobante de despliegue y una ruta anónima antes de confiar en `published`.

### Ejercicio 3 — Distinguir forma y verdad

¿Violaría el esquema JSON fijado el caso sintético `status: published` con `phases.publish.completed: false`? ¿Demostraría la validez del esquema que SEM-002 está disponible públicamente?

> **Respuesta:** No hay ninguna regla que relacione ambos campos. Validar el esquema solo acredita la estructura que examina; no prueba despliegue ni disponibilidad pública anónima. Hay que investigar la contradicción, no anunciar una publicación.

## 4. Separar el referente local del público

El [acta pública de referencia](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/public-baseline-2026-10-11.md) registra una lectura anónima del índice Streeling el 11 de octubre de 2026, cita un commit fuente y advierte que estar en público no equivale a una revisión del autor. También informa que la comprobación local de Learn generó páginas DV-001 mientras las peticiones GET anónimas a sus nuevas rutas públicas respondieron 404. «Existe página local generada» señala un artefacto de compilación; «publicado» señala una versión recuperable en una ruta pública. Lo primero no implica lo segundo.

Esa acta es prueba **histórica sobre las rutas DV-001**, no una prueba actual de SEM-002 ni del sitio de hoy. Para una publicación de SEM-003, el coordinador necesitaría definir la ruta, desplegar el sitio, consultarla anónimamente e inspeccionar una marca de versión o SHA de la fuente y el contenido servido. HTTP 200 podría corresponder a una versión anterior. El SHA apunta a la versión escrita; la lectura de la ruta la conecta con lo que ve el alumno. El acta del revisor apunta a otro evento. Ninguna sustituye a la otra.

### Ejercicio 4 — Precisar qué se observó

En el ejemplo DV-001 fechado, existe una página local y la ruta anónima dio 404. ¿Qué frase está respaldada: «se publicó la lección», «la compilación local produjo la página, pero esa ruta pública no la sirvió aquel día», o «no existía fuente»? ¿Qué habría que comprobar tras un despliegue posterior?

> **Respuesta:** La frase del medio. La página local y el 404 pertenecen a superficies distintas en aquella observación. Tras desplegar, consulta la ruta pública prevista de forma anónima y compara el contenido o SHA de procedencia con la revisión deseada. Una compilación local o la orden de despliegue no bastan.

## 5. Redactar un traspaso accionable

Un mensaje útil forma una cadena pequeña de pruebas: **artefacto y revisión → control identificado → resultado observado → paso pendiente → siguiente acción**. Es una pauta de redacción para este ejercicio, **no un nuevo DSL normativo**. Permite al receptor seguir los enlaces y rechazar interpretaciones obsoletas o excesivas. Ejemplo basado en la instantánea SEM-002:

> «La fuente inglesa de SEM-002 existe en Demerzel en el commit `c453a91d1c4d913af72c28779eff826659c1d654`. Una comprobación IA limitada de fuente y cinco respuestas no encontró problemas. El registro sigue `in_progress`, con revisión y publicación incompletas. Después: obtener la revisión humana de materia y alumnos y comprobar el despliegue Learn previsto mediante lectura anónima».

El mensaje no inventa un valor `ready`. Si una futura revisión aprueba solo la exactitud factual, hay que indicar ese alcance, sin extenderlo al idioma. Una nueva revisión de la fuente no queda cubierta automáticamente por un acta anterior. Los enlaces a revisiones inmutables conectan revisor, fuente y lectura pública con el mismo objeto o hacen visible una ruptura.

### Ejercicio 5 — Reparar un mensaje de agente

Reescribe «SEM-002 está revisado y publicado; las pruebas están verdes» usando solo el registro fijado y su acta. Indica una siguiente acción exacta y una incógnita sin inventar pruebas ni despliegue.

> **Respuesta:** «En el commit Demerzel `c453a91d1c4d913af72c28779eff826659c1d654`, SEM-002 tiene un borrador inglés y un acta de inspección IA limitada de la fuente y respuestas sin hallazgos. Su registro sigue `in_progress`, con `review.completed=false` y `publish.completed=false`. Estos artefactos no acreditan una ejecución nueva de pruebas ni una lectura pública de la ruta SEM-002. Después: solicitar revisión humana de materia y alumnos sobre esta revisión». El mensaje inicial convierte un control limitado en revisión final y afirma sin pruebas la publicación y las pruebas.

## Límites y transferencia

Esta lección analiza archivos Demerzel fijados y un acta pública fechada. No realiza un traspaso real entre agentes, ensayo con alumnos, validación humana por un especialista en semiótica ni publicación. Los cinco ejercicios examinan si el lector relaciona cada palabra de estado con su referente y su prueba. Para saber si el enfoque mejora la coordinación, compara en un experimento controlado un grupo que reciba un estado sin matices con otro que reciba la cadena de pruebas; mide si eligen el paso correcto y citan la revisión correcta. **Hasta entonces, el beneficio para los traspasos sigue siendo una hipótesis.**
