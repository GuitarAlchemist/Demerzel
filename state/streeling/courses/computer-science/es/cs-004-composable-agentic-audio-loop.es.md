---
module_id: cs-004-composable-agentic-audio-loop
department: computer-science
course: Componer y probar con uso propio un ciclo de mejora de audio con agentes
level: intermediate
prerequisites: ["cs-002-governing-agentic-loops", "gas-001-open-string-audio-evidence"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: cs-2026-10-04-004
version: "0.1.0"
---

# Componer y probar con uso propio un ciclo de mejora de audio con agentes

> **Departamento de Informática** | Nivel intermedio | 45 minutos | Borrador: pendiente de revisión técnica y lingüística

## Objetivos

Podrás separar las funciones que transforman pruebas de las operaciones que producen efectos, ejecutar un control sin mejora, describir una reanudación honesta después de un tiempo de espera y rechazar la declaración de éxito de un agente cuando no la respalden pruebas independientes.

## 1. Partir del problema del guitarrista y de un control

Un guitarrista quiere que el instrumento WASM en tiempo real de GA suene más convincente. GA ya cuenta con un motor de guitarra en Rust, un AudioWorklet y un ciclo de captura sin conexión. El prototipo GA local, aún sin integrar, en el commit `6fac5735f7ffbb4116ebee05cfc9d7911bb12ce9` añade `Rust/guitar-web-wasm-demo/scripts/run-comfy-audio.js` y `compare-audio.js`. El primero envía un WAV a un workflow ComfyUI local y guarda su procedencia. El segundo compara el audio inicial, un candidato y una referencia mediante resúmenes FFT y medidas RMS y Haar en intervalos de 250 ms. El workflow incluido solo carga y guarda audio: **no mejora el sonido**. No se ha verificado ningún candidato producido por una instancia real de ComfyUI ni una escucha a ciegas.

El [material GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) contiene un mi grave al aire grabado y atribuido, junto con una renderización nativa del motor Rust de GA. Esta usa el mismo código que el motor WASM, pero no es una captura del AudioWorklet. El primer ataque de la grabación aparece aproximadamente a los 1,1 segundos y hay otro cerca de los 2,75 segundos. Antes de interpretar una distancia, hay que seleccionar ventanas de la misma nota.

Primero fija **candidato = audio inicial**. Al utilizar `ga-engine-e2-open-4s.wav` dos veces, `deb-low-e-open.wav` como referencia, `--reference-offset 1.1` y `--seconds 1.5`, el comparador dio el mismo error absoluto medio RMS en intervalos de 250 ms para ambos: `0.124158746`. También coincidieron todos los errores FFT y Haar. Este control negativo es útil: si la cadena anuncia una mejora, la regla de decisión está mal, aunque todas las órdenes hayan terminado sin error.

Una revisión independiente en wmux señaló que este control también pasaría si el comparador siempre dijera «igual». Un [control con cambios conocidos](../../../fixtures/computer-science/cs-004/review-followup-20261004.md) reduce a la mitad la amplitud del audio nativo y, en otro ensayo, aplica un filtro estrecho cerca del segundo armónico de E2. Cambiaron las medidas RMS y espectrales, respectivamente. Esos controles muestran sensibilidad a los cambios, **no** una guitarra más realista: reducir la amplitud disminuyó el error RMS, el filtro lo aumentó y nadie escuchó estos archivos a ciegas.

### Ejercicio 1

¿Qué debes concluir si el candidato y el audio inicial comparten el SHA-256 `a78a70243a81aa79d806d9ef3db7baa1385c479505f7d5e97b8bf0c7866c3f98`?

> **Respuesta:** Rechazar toda afirmación de mejora. Los archivos son idénticos byte a byte: ni las medidas ni la escucha pueden atribuir un cambio a ComfyUI. Conservar la ejecución como control y comprobar si el workflow transformó el sonido.

## 2. Componer transformaciones y aislar efectos

Cada flecha tiene un contrato. Una función pura devuelve lo mismo con las mismas entradas y no lee el reloj ni archivos, no llama a servicios y no escribe. Las operaciones con efectos quedan en los bordes:

```text
capturarWasm(nota, perfil)              EFECTO -> WAV inicial
cargarYValidar(archivos, nota, ataques) EFECTO + validación PURA -> manifiesto fijo
enviarAComfy(workflow, inicial)         EFECTO -> ID de solicitud o error
recuperarCandidato(ID)                 EFECTO -> WAV y hashes
decodificarYAlinear(manifiesto)        EFECTO -> matrices de muestras
características(muestras)              PURO -> FFT, RMS, Haar
comparar(características, referencia)  PURO -> diferencias y alertas
proponerDecisión(pruebas, política)     PURO -> rechazar/aceptar/escuchar
escucharACiegas(A, B, pregunta)        OBSERVACIÓN HUMANA -> registro
registrarDecisión(todasLasPruebas)     EFECTO -> recibo duradero
```

Así se pueden probar `características` con muestras conocidas y `proponerDecisión` con registros fijos, sin iniciar ComfyUI ni confiar en la explicación del agente. El prototipo ya separa algunos cálculos (`timeFeatures`, `compareFeatures`) de la red y los archivos. Es un primer límite útil, no una garantía de pureza de todo el programa. Decodificar mediante FFmpeg y leer un WAV siguen siendo efectos. Cada límite debería devolver un resultado explícito como `Ok(candidato)` o `Err(tipo, prompt_id, pruebas)`; nunca se debe sustituir silenciosamente un candidato ausente por el audio inicial.

La política mínima es concreta: si el candidato es idéntico byte a byte, **rechazar la mejora**; si falta un archivo, la nota no coincide o los ataques no están alineados, **reparar el experimento**; si hay una diferencia espectral prometedora, **escuchar a ciegas**, no aceptar de inmediato. Una cifra de pérdida no representa por sí sola al guitarrista. El evaluador mantiene fija la referencia y comunica avances y regresiones en ataque, altura, caída, ruido y artefactos.

### Ejercicio 2

Clasifica `timeFeatures(samples)`, `fetch('/prompt')`, `hash(bytes)`, la decodificación con FFmpeg y la escritura del recibo. ¿Cuándo puede proponer otra seed el agente?

> **Respuesta:** `timeFeatures` y `hash` pueden ser puros si reciben todas sus entradas. La red, FFmpeg y la escritura son efectos. El agente propone la seed antes de `enviarAComfy`; la seed enviada y el hash del workflow deben quedar registrados.

### Ejercicio 3

El candidato reduce el error del centroide espectral, pero su ataque suena borroso en una prueba A/B a igual volumen. ¿Permite la cifra cambiar el motor?

> **Respuesta:** No. Esa medida solo sirve de diagnóstico. Registra tanto el cambio numérico como la observación del guitarrista, rechaza o revisa el candidato y conserva el motor inicial. No se sigue ningún cambio automático de parámetros Rust/WASM.

## 3. Reintentar sin inventar el resultado

Imagina que ComfyUI acepta `/prompt`, pero el cliente agota el tiempo antes de consultar `/history/{prompt_id}`. El servidor podría seguir trabajando. El resultado es **desconocido**, no necesariamente un fallo. Si se conoce el ID, consulta el historial antes de reenviar. Si se perdió, anota la incertidumbre y no cuentes el reintento como un experimento independiente. Define el experimento lógico mediante el hash del audio inicial, el del workflow, los campos del modelo y la seed; conserva por separado el ID de cada envío y de cada intento. Un nombre de carga basado en el hash identifica el mismo archivo, pero no hace idempotente la ejecución del modelo.

El primer prototipo todavía no persiste el ID antes de recuperar el candidato; reanudar después de una interrupción sigue siendo una carencia. Una corrección posterior distingue `comparison_pending`, `completed` y `comparison_failed`: una comparación fallida no debe dejar un veredicto de calidad satisfactorio. Solo se debe añadir recuperación después de reproducir ese fallo con una prueba y poder inspeccionar su recibo.

### Ejercicio 4

Ya existe el WAV candidato, pero falla la decodificación de la referencia. ¿Qué estado registras y qué vuelves a ejecutar?

> **Respuesta:** Conserva el candidato y sus hashes, marca `comparison_failed` e indica el error. Arregla la referencia o el decodificador y repite **la comparación del mismo candidato**. No hace falta volver a ejecutar ComfyUI.

## 4. Usar nuestra propia cadena de principio a fin

Desde un checkout que contenga GA y las fixtures Streeling, adapta la ruta. El prototipo GA sigue siendo un **commit local**: esta orden es un ejercicio para quien revise ese worktree, no una instalación pública.

```powershell
$fixture = '<ruta-del-checkout-Demerzel>\state\streeling\fixtures\guitar-acoustics\gas-001'
node scripts/compare-audio.js `
  --baseline "$fixture\ga-engine-e2-open-4s.wav" `
  --candidate "$fixture\ga-engine-e2-open-4s.wav" `
  --reference "$fixture\deb-low-e-open.wav" `
  --reference-offset 1.1 --seconds 1.5 --output control-comparison.json
```

Comprueba en el JSON la igualdad de los hashes y de los errores. Después, y solo si conoces un modelo de audio local y su licencia, prueba un workflow ComfyUI real. Mantén fijos el audio inicial y la referencia, cambia un único parámetro, registra modelo, seed y hashes, vuelve a medir y pide una escucha a ciegas con volúmenes igualados. El recibo debe contener la observación del usuario, las medidas, la decisión y el próximo experimento. Esto es dogfooding: usar nuestro motor y nuestras herramientas para descubrir problemas de preparación, errores, recuperación y revisión. Si un agente no puede leer la fixture o escribir el recibo, registra esa fricción como hallazgo del producto; enviar un prompt no demuestra progreso.

Antes de escuchar, registra quién evaluará, qué notas e intensidades oirá, cómo se igualarán los niveles y con qué tolerancia, cómo se aleatorizará el orden y cuál será la regla de decisión. Un grupo de tres guitarristas es una **propuesta por probar**, no un umbral validado. Conserva las elecciones y los comentarios individuales, incluso cuando discrepen. Si una comparación manual más sencilla llega a las mismas decisiones con menos preparación, descarta por ahora el flujo de agentes hasta que aporte un valor medible.

### Ejercicio 5

Propón una condición de éxito y un criterio de rechazo. ¿Quién decide si cambia el motor en tiempo real?

> **Respuesta:** Por ejemplo, exigir un candidato reproducible, archivos inicial y de referencia fijos, ningún deterioro del ataque o de la altura, y una preferencia documentada en escucha a ciegas. Una salida idéntica, procedencia ausente o rechazo repetido por los oyentes refutan la mejora. El agente propone; una evaluación independiente y una persona autorizada deciden si merece la pena probar un cambio Rust/WASM. El candidato sin conexión no se convierte por sí solo en el motor en tiempo real.

## 5. Mejorar el ciclo siguiente, no solo el resultado actual

El [registro de mejora recursiva](../../../fixtures/computer-science/cs-004/recursive-improvement-evidence.json) reúne dos pares de ensayos. La primera revisión en wmux leyó solo una de tres fuentes declaradas y no escribió un recibo. Tras añadir al lanzador reglas exactas de acceso a archivos autorizadas por el usuario, otra lane leyó cuatro de cuatro fuentes y escribió una revisión con marcador verificado. El primer control de audio mostró que un candidato idéntico no podía mejorar el punto de partida; las transformaciones conocidas posteriores mostraron que el comparador detectaba determinados cambios de nivel y espectro. Cada fallo cambió el **harness o la evaluación** y otro ensayo probó el cambio. Dos pares no demuestran crecimiento exponencial.

En los próximos tres experimentos de cursos y audio, asigna un único responsable de escritura a cada artefacto independiente, con entrada inmutable y recibo esperado. La preparación de fixtures, la localización y los candidatos pueden avanzar en colas separadas cuando sus entradas estén listas. Automatiza esquema, enlaces, cobertura de idiomas y controles; agrupa la revisión independiente de los recibos preparados. Reserva la escucha de músicos para juicios que las medidas no resuelven y la autorización humana para cambios difíciles de deshacer o publicación. Prueba cada evaluador nuevo con al menos un caso que no se usó para diseñarlo. Mide el tiempo desde la entrada lista hasta el curso revisado, la espera de revisión, los recibos fallidos, el éxito de los aprendices y los defectos posteriores. Cuenta **módulos útiles y revisados**, no palabras redactadas. Si la espera de coordinación crece más deprisa que la producción verificada, limita el trabajo en curso o simplifica el ciclo. Un método manual puede resultar mejor.

### Ejercicio 6

Tres agentes redactan 30 módulos en un día, pero solo dos tienen fixtures utilizables y ejercicios revisados. ¿Ha mejorado el sistema? Propón un cambio y un criterio de rechazo.

> **Respuesta:** No hay una mejora demostrada: la producción verificada es de dos módulos y la cola de revisión puede ser el cuello de botella. Localiza los recibos sin pruebas, automatiza las verificaciones repetibles de las fixtures y limita los nuevos borradores hasta vaciar la cola. Rechaza la supuesta aceleración si varios ciclos no reducen el tiempo por módulo útil y revisado sin aumentar defectos o rechazos.

## Fuentes y límites

El puente GA está en el commit local `6fac5735`. Pasaron las pruebas simuladas, pero ComfyUI no respondió en `127.0.0.1:8188` y no se volvió a capturar WASM en el navegador. Repetimos independientemente el control con los [WAV GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md). [CS-002](cs-002-governing-agentic-loops.es.md) explica los límites externos de un ciclo de agentes; aquí componemos un experimento observable. `docs/methodology/agentic-engineering.md` de GA aporta el contexto de colas y harness. Los [nodos de audio](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_audio.py) y las [rutas del servidor](https://github.com/Comfy-Org/ComfyUI/blob/master/server.py) describen la interfaz ComfyUI. Las distancias FFT/Haar no prueban realismo percibido y no presenciamos la sesión de grabación original.
