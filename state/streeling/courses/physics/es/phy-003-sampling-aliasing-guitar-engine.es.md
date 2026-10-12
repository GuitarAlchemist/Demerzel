---
module_id: phy-003-sampling-aliasing-guitar-engine
department: physics
course: Muestreo y aliasing en el límite del motor de guitarra de GA
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-003
version: "0.1.0"
---

# Muestreo y aliasing en el límite del motor de guitarra de GA

> **Departamento de Física** | Nivel intermedio | 35 minutos | Borrador en español; revisión y publicación pendientes

## Objetivos

Calcularás un límite de Nyquist y una frecuencia alias, identificarás la frecuencia de muestreo que realmente recibe el motor Rust de GA y diseñarás una prueba sin conexión que pueda revelar aliasing sin confundir un riesgo calculado con un defecto medido. [PHY-001](../es/phy-001-science-of-guitar-sound.es.md) presenta los armónicos de guitarra. [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) elige ventanas de análisis para notas cambiantes. Aquí la pregunta aparece antes en la cadena: **¿qué frecuencias continuas puede representar una señal muestreada y qué debe ocurrir antes de la captura, síntesis o conversión de frecuencia?**

## 1. Vincular la frecuencia al artefacto, no al nombre de la nota

La [fixture GAS-001 fijada](../../../fixtures/guitar-acoustics/gas-001/README.md) contiene un mi grave al aire grabado durante cuatro segundos y un render nativo de cuatro segundos del motor Rust de GA. Ambos archivos son mono a **44 100 muestras por segundo**. El render llama a `engine_note_on(82.4069 Hz, 0.1)`; la identidad E2 de la grabación es una etiqueta del conjunto de datos, no una medición de frecuencia. El render procede de una compilación nativa, **no** de capturar el AudioWorklet del navegador. Estas diferencias importan al investigar un artefacto de audio.

En el commit de GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), el [puente de audio del navegador](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) envía `audioContext.sampleRate` al [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js). Este llama a `engine_init(srToUse)` y copia muestras mono generadas a los canales de salida del navegador. El [motor Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) guarda esa frecuencia y la usa para los coeficientes de resonadores y la longitud de la línea de retardo. Por tanto, el WAV fijado a 44,1 kHz **no** demuestra que todas las sesiones del navegador usen 44,1 kHz. Registra la frecuencia real del contexto y la ruta de captura antes de compararla con GAS-001.

Para una duración `T`, el número de muestras es `N = f_s T`. Cuatro segundos a 44 100 Hz producen **176 400 muestras** por canal mono; a 48 000 Hz serían **192 000**. Ningún recuento revela si se filtró bien la entrada analógica o si el sintetizador evitó alias.

### Ejercicio práctico 1

Al ver el render GAS-001 a 44,1 kHz, alguien escribe: «El motor de GA en el navegador siempre funciona a 44,1 kHz». ¿Qué respaldan realmente las fuentes y qué debe registrar una prueba en el navegador?

> **Respuesta:** GAS-001 fija **su WAV renderizado de forma nativa** a 44 100 Hz. El puente del navegador transmite `audioContext.sampleRate` al AudioWorklet y al motor Rust; el valor real debe observarse en esa sesión. Registra la frecuencia del contexto, la frecuencia y el códec de salida o grabación, la revisión del motor y la ruta de captura. Un WAV nativo no es una captura del navegador.

## 2. Calcular la banda representable antes de hablar de armónicos

Para una señal real muestreada uniformemente a `f_s`, la frecuencia de Nyquist es `f_N = f_s/2`: **22 050 Hz** a 44 100 Hz y **24 000 Hz** a 48 000 Hz. En principio, se puede reconstruir una entrada continua ideal, limitada en banda y con contenido estrictamente inferior a `f_N`, a partir de sus muestras. Una captura real necesita un filtro antialias **antes** del muestreo, con banda de transición por debajo de Nyquist. `f_N` es un límite matemático, no la promesa de un filtro perfecto en el micrófono, convertidor, motor o exportación.

El objetivo de mi grave al aire es `f_0 = 82.4069 Hz`. Su parcial entero ideal `k` estaría en `k f_0`, pero una guitarra física o sintetizada no tiene necesariamente todos los parciales ni los mantiene en múltiplos exactos. A 44,1 kHz, `267 f_0 = 22,002.6423 Hz` queda por debajo de Nyquist y `268 f_0 = 22,085.0492 Hz` por encima. A 48 kHz, el límite está entre el parcial **291** (`23,980.4079 Hz`) y el **292** (`24,062.8148 Hz`). Son *límites teóricos de índice* para esa fundamental, no un recuento de parciales audibles o medidos. Conviene dejar un margen operativo por debajo del límite exacto, porque los filtros necesitan una banda de transición y la implementación importa.

### Ejercicio práctico 2

Para el mismo E2 ideal, calcula el armónico entero más alto estrictamente por debajo de Nyquist a 44,1 y 48 kHz. ¿Demuestra eso que la fixture contiene esos armónicos?

> **Respuesta:** `floor(22,050 / 82.4069) = 267` y `floor(24,000 / 82.4069) = 291`. Los parciales siguientes, 268 y 292, superan sus respectivos límites de Nyquist. La aritmética no demuestra que alguna forma de onda tenga un parcial 267 o 291 detectable. Para medir niveles se necesitan los WAV, una ventana apropiada, un suelo de ruido y límites de análisis explícitos.

## 3. Calcular a mano una frecuencia alias

Muestrear un seno continuo de `f` Hz da `sin(2π f n / f_s)` en índices enteros `n`. Sumar o restar un múltiplo entero de `f_s` produce las mismas muestras, salvo un cambio de signo o fase. Una regla práctica para la magnitud de la frecuencia alias es plegar `f` por múltiplos de `f_s` al intervalo `[0, f_s/2]`; de forma equivalente, elegir un entero `m` tal que `|f - m f_s|` caiga en ese intervalo. Es un cálculo **sintético de un solo tono**, no una observación de GAS-001.

Considera un seno continuo de **23 000 Hz**. A 44,1 kHz está 950 Hz por encima de Nyquist y se pliega a `|23,000 - 44,100| = 21,100 Hz`. La secuencia muestreada equivale a un seno de 21 100 Hz con un cambio de signo o fase. A 48 kHz, 23 000 Hz está por debajo del límite de 24 000 Hz y no se pliega. Convertir después la captura de 44,1 kHz a 48 kHz no recupera la entrada original de 23 000 Hz: las muestras no distinguen esos dos orígenes continuos.

En un motor de guitarra, la excitación de banda ancha del punteo, el procesamiento no lineal y los parciales agudos justifican **comprobar** ese límite. La [excitación Rust fijada](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) usa ruido filtrado en una línea de retardo y procesamiento por muestras. Inspeccionarla no demuestra un alias audible o medible en su salida. Una frecuencia mayor puede desplazar el límite de aliasing, pero también cambia tamaños de búfer y coste de cálculo; no sustituye a limitar la banda de forma controlada y medir.

### Ejercicio práctico 3

Una excitación propuesta tiene una componente continua de 30 000 Hz. ¿Dónde situaría un muestreador ideal su alias a 44,1 y 48 kHz?

> **Respuesta:** A 44,1 kHz, `|30,000 - 44,100| = 14,100 Hz`. A 48 kHz, `|30,000 - 48,000| = 18,000 Hz`. Son pliegues de un seno ideal, no picos espectrales predichos para el motor GA. Un filtro antialias anterior puede atenuar la componente antes de capturarla; un generador digital debe evitar crear contenido fuera de banda o controlar su plegado.

### Ejercicio práctico 4

Alguien remuestrea a 48 kHz una grabación de 44,1 kHz con un pico a 21,1 kHz y afirma: «Ahora que Nyquist está a 24 kHz, se ha recuperado el tono original de 23 kHz». Explica el error.

> **Respuesta:** La secuencia de 44,1 kHz es compatible tanto con un tono de 21,1 kHz como con uno de 23 kHz, salvo un cambio de fase o signo. La conversión puede interpolar o filtrar los datos disponibles, pero no inferir su origen continuo. Hay que impedir el plegado **antes** del muestreo original mediante filtrado antialias analógico, o generar contenido digital limitado en banda a la frecuencia objetivo.

## 4. Convertir el riesgo en una prueba refutable de GA

Las [mediciones GAS-001](../../../fixtures/guitar-acoustics/gas-001/measurements.json) incluyen picos próximos a E2 y algunos parciales graves, no un estudio de alias agudos. Un gráfico de los dos WAV a 44,1 kHz no puede identificar por sí solo la frecuencia original de un alias: un pico bajo Nyquist puede tener varias causas. Además, la grabación tiene un primer ataque aproximado a 1,1 s y otro cerca de 2,75 s; el render empieza en cero. Conserva intervalos alineados por ataque antes de comparar espectros; [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) explica este problema temporal.

Un experimento sin conexión debería comenzar con una **referencia sintética conocida**: generar un seno de 23 kHz a una frecuencia de referencia más alta, muestrearlo a 44,1 y 48 kHz registrando el filtro elegido y comprobar el pliegue esperado de 21,1 kHz solo en la rama de 44,1 kHz deliberadamente sin filtrar. Después, genera con la misma fuente GA fijada, nota, velocidad, perfil y duración a ambas frecuencias mediante llamadas **nativas**, o captura ambas por el **navegador** registrando su frecuencia; no mezcles rutas sin indicarlo. Guarda ajustes de entrada, compilación exacta, hashes WAV, frecuencia, nivel pico y ventanas espectrales. Compara con una referencia controlada a frecuencia equivalente a lo largo de varias notas y velocidades. Si un tono inesperado se desplaza según la predicción de alias al cambiar la frecuencia de render, investiga la etapa que lo genera; si permanece en la misma frecuencia física, la hipótesis de alias simple se debilita. Confirma con un cambio de código dirigido a la etapa sospechosa y repite la escucha a nivel igualado. El protocolo es **propuesto**: esos renders, capturas y escuchas adicionales **no** se han realizado para esta lección.

Para una futura conversión de frecuencia, documenta las frecuencias de origen y destino, banda pasante y de rechazo del filtro, retardo, comprobaciones de saturación y si la referencia se capturó antes o después de codificación con pérdidas. El puente del navegador tiene una [ruta MediaRecorder opcional](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js); no supongas que su blob es un WAV bruto a 44,1 kHz. Mantén esa ruta separada del render nativo de la fixture.

### Ejercicio práctico 5

Aparece un pico a 21,1 kHz en un render del motor a 44,1 kHz. ¿Basta para afirmar que es un alias de síntesis de 23 kHz? Indica la siguiente comparación decisiva y un control.

> **Respuesta:** No. El pico puede ser una componente dentro de banda, un alias de otra componente fuera de banda o un artefacto de captura. Genera la misma configuración fijada del motor a 48 kHz y compara espectros agudos alineados por ataque: una fuente cercana a 23 kHz debería aparecer allí cerca de 23 kHz, mientras que su alias a 44,1 kHz estaría cerca de 21,1 kHz. Controla revisión del motor, nota, velocidad, perfil y ruta de captura; inspecciona la etapa de señal o añade un cambio dirigido de limitación de banda antes de atribuir una causa. El movimiento predicho es una **prueba**, no un resultado observado.

## Fuentes y límites actuales

- [Fixture GAS-001 fijada, procedencia y frecuencias](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), con su [README local](../../../fixtures/guitar-acoustics/gas-001/README.md). La grabación se atribuye allí a **collegefishiesd** bajo licencia CC BY-SA 4.0; esta lección no reproduce el audio.
- Commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo): [puente del navegador](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) y [motor Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs).
- Los recuentos de muestras, límites de índice armónico y pliegues de senos anteriores se calculan directamente a partir de las frecuencias indicadas. No se han completado para PHY-003 nuevas mediciones de alias agudos en GAS-001, captura del navegador, revisión independiente de la materia, prueba con estudiantes, revisión lingüística ni lectura pública.
