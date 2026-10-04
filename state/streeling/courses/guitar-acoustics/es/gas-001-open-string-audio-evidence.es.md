---
module_id: gas-001-open-string-audio-evidence
department: guitar-acoustics
course: Qué puede enseñar una cuerda al aire al motor de guitarra WASM
level: beginner
prerequisites: []
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-04-001
version: "0.1.0"
---

# Qué puede enseñar una cuerda al aire al motor de guitarra WASM

> **Departamento de Acústica de Guitarra y Síntesis Sonora** | Nivel: principiante | Duración estimada: 40 minutos | Estado: pendiente de revisión

## Objetivos

Al terminar esta lección, usted podrá:

- comparar una cuerda al aire grabada con una nota del motor Rust/WASM de guitarra que GA ya tiene;
- localizar el ataque antes de medir altura, parciales y decaimiento;
- usar una FFT con ventana para picos armónicos locales y wavelets para seguir el ataque y los parciales en el tiempo;
- separar una diferencia medible de un juicio sobre realismo percibido;
- evaluar fuera de línea una variante creada con ComfyUI antes de cambiar el motor WASM en tiempo real.

## La pregunta del proyecto y los archivos de trabajo

GA ya cuenta con un [motor de guitarra Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) cargado por un [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js). Incluye realimentación de cuerda pulsada, resonancias de caja, ruido de ataque y reverberación. También existe un [ciclo de grabación y análisis fuera de línea](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) con coloración DDSP opcional. **El código GA inspeccionado aún no conecta ComfyUI a ese ciclo.** La intención del proyecto es explorar variantes en ComfyUI fuera de línea, medirlas y escucharlas, y solo después decidir cambios en el motor WASM existente. No hace falta ejecutar un modelo generativo dentro del AudioWorklet.

La carpeta `state/streeling/fixtures/guitar-acoustics/gas-001/` contiene dos archivos:

| Archivo | Procedencia | Límite |
|---|---|---|
| `deb-low-e-open.wav` | Grabación acústica mono de cuatro segundos, identificada como `source=deb`, `low_E`, `fret=0`, `E2` en el [conjunto `collegefishiesd` de revisión `a33a262`](https://huggingface.co/datasets/collegefishiesd/guitar-fretboard-notes/tree/a33a26243e88e7ccd4893bee30eac3219ec8bef8). Licencia [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) y atribución en el [README de la fixture](../../../fixtures/guitar-acoustics/gas-001/README.md). | La identificación procede del conjunto; no presenciamos la sesión de grabación. |
| `ga-engine-e2-open-4s.wav` | Nota mono de cuatro segundos generada con el motor GA fijado, a 44.100 Hz, perfil predeterminado 0 y `engine_note_on(82.4069, 0.1)`, mediante el [script de renderizado](../../../fixtures/guitar-acoustics/gas-001/render-ga-e2.py). | Se compiló de forma nativa el mismo código Rust; no es una captura del AudioWorklet en el navegador. |

Ambos WAV y el [script de medición](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) se encuentran en el repositorio fuente. La publicación deberá copiar estos archivos o dar enlaces estables. El [README](../../../fixtures/guitar-acoustics/gas-001/README.md) documenta hashes SHA-256, método y licencia. Mi2 tiene una frecuencia nominal de 82,4069 Hz; un pico medido puede caer en otra frecuencia según la resolución.

### Ejercicio

El comparador espectral de GA también usa una grabación larga llamada `by-the-lake.wav`. ¿Por qué corresponde usar aquí la toma marcada `low_E`, `fret=0`?

> **Respuesta:** El conjunto identifica una sola nota mi2 de cuerda al aire. En `by-the-lake.wav` no se ha verificado un mi al aire aislado; tratar sus primeros segundos como tal invalidaría la comparación.

## 1. Localizar el evento antes de analizarlo

La grabación empieza con un tramo relativamente silencioso. El primer ataque aparece aproximadamente a **1,1 segundos** y otro cerca de **2,75 segundos**. La nota de GA comienza en cero. Una FFT de los cuatro segundos mezclaría silencio, ataques y decaimientos. Incluso una FFT local de 0,2 a 1,2 segundos desde el *inicio del archivo* estudiaría principalmente el tiempo anterior a la nota grabada. Alinee las ventanas con el primer ataque y termine antes del segundo.

La [medición de la fixture](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) usa una ventana Hann de un segundo desde **0,2 hasta 1,2 segundos después del primer ataque**. Compara también RMS en 0,2–0,4 y 1,0–1,2 segundos después del ataque. El instante de ataque es aproximado, elegido tras observar niveles por ventanas cortas. Conviene inspeccionar la forma de onda y repetir con un pequeño desplazamiento del marcador. El [manual de Audacity](https://manual.audacityteam.org/man/plot_spectrum.html) explica la relación entre duración de ventana y resolución de frecuencia.

### Ejercicio

Un programa toma de 0,2 a 1,2 segundos de ambos archivos y concluye que la grabación no tiene parciales de mi2. ¿Qué debe corregirse?

> **Respuesta:** Localizar el primer ataque grabado y desplazar la ventana respecto a él. La ventana elegida está principalmente antes de la nota. También hay que excluir el segundo ataque del cálculo de decaimiento e indicar que el instante inicial es aproximado.

## 2. Dar tareas distintas a FFT y wavelets

Una **FFT con ventana** muestra qué frecuencias destacaron durante un intervalo elegido. Permite comprobar el pico local de mi2 y el nivel relativo de sus armónicos, pero no cuándo apareció o disminuyó cada uno. Una **STFT** desplaza la ventana y permite estudiar audio cambiante, con resolución temporal y frecuencial determinada por su tamaño. [SciPy documenta ese uso temporal de la STFT](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html).

Una **wavelet compleja** adapta su escala temporal a la frecuencia. Nuestro script usa wavelets de tipo Morlet de seis ciclos centradas aproximadamente en 82, 165 y 330 Hz. Así sigue el ataque y la evolución del nivel de los parciales. El centro, número de ciclos e instante inicial influyen en el resultado; no representan una puntuación de realismo. [Una investigación sobre el timbre de la guitarra](https://www.iieta.org/journals/ts/paper/10.18280/ts.380218) también utiliza wavelets continuas para estudiar cómo cambia la energía de los parciales.

| Medición | Mi2 grabado | Mi2 generado por GA |
|---|---:|---:|
| Pico cercano a mi2, FFT local | 83 Hz | 82 Hz |
| Segundo parcial respecto al primero, FFT local | +7,0 dB | −16,9 dB |
| Cambio RMS, ventana tardía menos temprana | −3,9 dB | −1,1 dB |
| Cambio del segundo parcial con wavelet | −4,5 dB | −12,9 dB |

Los niveles absolutos de las tomas son distintos; compare primero **relaciones dentro de cada archivo**. La diferencia del segundo parcial es de 23,9 dB según esta FFT local. Eso no significa que una grabación sea 23,9 dB más fuerte en conjunto ni más realista. La wavelet sugiere que el segundo parcial cae más deprisa en el sonido de GA según este método. Observe la forma de onda y escuche antes de atribuirlo a un solo parámetro.

### Ejercicio

¿Qué técnica usaría para situar un ataque rápido? ¿Qué medición facilita comparar picos armónicos locales? ¿Qué no puede probar ninguna de las dos?

> **Respuesta:** Una vista temporal como wavelets o STFT ayuda a situar el ataque; una FFT con ventana declarada compara picos locales. Ninguna prueba el realismo percibido a partir de una sola nota.

## 3. Convertir la diferencia en un experimento WASM controlado

El [motor Rust de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) expone controles de decaimiento, brillo, dispersión, decaimiento de ataque, reverberación y perfil de guitarra. Un parcial agudo débil en esta pareja motiva **probar** un cambio de brillo o excitación, pero no lo justifica por sí solo. Cambie un parámetro o un conjunto pequeño documentado, renderice otra vez mi2 y conserve los WAV y la revisión del código antes y después. Compruebe altura, parciales, ataque, ausencia de recorte y latencia en otras cuerdas e intensidades. Después organice una comparación auditiva con niveles igualados. El [artículo original de Karplus y Strong](https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf) describe el decaimiento variable de los armónicos; un único espectro no lo resume.

ComfyUI puede aportar una **tercera variante fuera de línea**. Su núcleo tiene [nodos de carga, escucha y guardado de audio](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_audio.py) y existe un [workflow oficial de generación sonora](https://github.com/Comfy-Org/ComfyUI/blob/master/blueprints/Audio%20Generation%20%28Stable%20Audio%203%20Medium%20Base%29.json). Conserve hash de entrada, workflow JSON, modelo y versión, semilla, prompt, ajustes, hash de salida, formato y licencia. Confirme que la variante aún contiene un solo evento mi2 antes de compararla. Para medir, use una salida sin pérdida o una conversión documentada; la compresión con pérdida puede alterar el espectro. El ciclo GA actual utiliza DDSP o coloración espectral, no ComfyUI: la conexión aún es trabajo pendiente.

Esto permite una **iteración agentic de dogfooding**: grabar la salida actual de GA, pedir a un agente una sola modificación comprobable, explorar en ComfyUI una variante fuera de línea cuando aporte valor, renderizar el motor WASM modificado y comparar todos los archivos con la misma referencia externa. Cada ciclo registra el cambio de parámetros, hashes, medidas, resultado de escucha y decisión de aceptar o rechazar. La puntuación heurística del agente proponente es una pista, no el único juez de su resultado; un procedimiento de medición fijo y una escucha independiente evitan que la iteración premie sus propias preferencias. Un intento rechazado también informa el siguiente experimento.

### Ejercicio

Una salida de ComfyUI parece más brillante que GA, pero faltan prompt, semilla, entrada y versión de modelo. ¿Puede guiar el motor WASM? Cite dos controles para una nueva ejecución válida.

> **Respuesta:** Todavía no. Registre workflow, modelo, semilla y hashes de entrada y salida, y confirme que sigue siendo un mi2 aislado. Compare referencia, GA y variante a igual volumen; luego cambie un parámetro del motor y vuelva a medir. Una persona o evaluación independiente debe comprobar el resultado: el agente no puede validarlo solo con su propia puntuación. «Más brillante» no identifica un cambio seguro.

## 4. Declarar lo que aún no se sabe

Esta pareja muestra energía próxima a mi2 en ambos archivos y diferencias en los parciales y su evolución bajo las ventanas elegidas. No determina cuál convence más al oyente. Instrumento, micrófono, sala, fuerza al pulsar y procesamiento del conjunto grabado difieren del renderizado nativo de GA. Una nota no representa acordes, todo el diapasón ni varias dinámicas. Las wavelets añaden información temporal, pero no eliminan esas diferencias de origen.

Una FFT local no resuelve **la sensación del ataque inicial** ni **la respuesta del instrumento a distintas intensidades**. Tampoco bastan las wavelets de esta única nota. Una prueba de escucha debería ocultar la identidad de los archivos, igualar niveles, cubrir otras cuerdas e intensidades y registrar los juicios. El [comparador espectral de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/scripts/run-spectral-critic.js) ofrece indicios, no un veredicto validado de realismo.

### Ejercicio

Escriba la afirmación más fuerte que admite la tabla y dos observaciones necesarias antes de decir que «el nuevo motor WASM suena más a guitarra».

> **Respuesta:** Los dos mi2 difieren en nivel y evolución del segundo parcial según el método indicado. La afirmación sobre realismo necesita escucha con niveles igualados y medidas repetidas en otras notas o intensidades, con condiciones de grabación documentadas.

## Ideas clave

- Alinee los ataques antes de comparar una nota grabada con otra sintética.
- La FFT local mide picos en una ventana; STFT y wavelets muestran cómo cambian.
- Una diferencia numérica plantea una hipótesis de ajuste, no un juicio perceptivo.
- ComfyUI sirve para explorar y evaluar fuera de línea; el motor Rust/WASM existente sigue generando el sonido en tiempo real.
- El dogfooding ofrece al agente una salida GA que mejorar; medidas fijas y una escucha independiente deciden si el intento ayudó.
- Separe referencia grabada, variante generada, revisión del código, método y resultados de escucha.

## Fuentes y límites

- [Procedencia de archivos, hashes, scripts, medidas y atribución de licencia](../../../fixtures/guitar-acoustics/gas-001/README.md).
- GA: [motor Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs), [puente AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [ciclo fuera de línea](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), commit `dc2e74c`.
- [Karplus y Strong](https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf), [guía FFT de Audacity](https://manual.audacityteam.org/man/plot_spectrum.html), [STFT de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html), [investigación con wavelets](https://www.iieta.org/journals/ts/paper/10.18280/ts.380218).

*Investigación: `guitar-acoustics-2026-10-04-001`. Siguen pendientes las revisiones temática y lingüística. La fixture no incluye una captura del AudioWorklet en navegador, integración ComfyUI ni veredicto de un panel de oyentes.*
