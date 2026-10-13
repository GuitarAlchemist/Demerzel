---
module_id: gas-003-decay-calibration-open-e
department: guitar-acoustics
course: "Calibrar una prueba de decaimiento del mi al aire para el motor de guitarra de GA"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-12-003
version: "0.1.0"
---

# Calibrar una prueba de decaimiento del mi al aire para el motor de guitarra de GA

> **Departamento de acústica y síntesis de guitarra** | Intermedio | 40 minutos | Borrador traducido por IA; revisión pendiente

## Objetivos

Distinguirás una *medición* del decaimiento de un *parámetro* de Rust, calcularás la diferencia del par de mi al aire fijado, seguirás el coeficiente de realimentación del motor y definirás un experimento nativo de un solo parámetro con criterio de refutación y salvaguardas. [GAS-001](../en/gas-001-open-string-audio-evidence.md) establece el par grabado y sintetizado. [GAS-002](../en/gas-002-brightness-control-and-evaluation-gate.md) prueba una hipótesis de brillo para una proporción armónica local. La pregunta aquí es: **¿puede un cambio controlado del ajuste de decaimiento de GA acercar la caída de nivel de su mi al aire a la de la grabación sin perjudicar el ataque, la altura ni otras notas?** Todavía no se ha renderizado ningún candidato de decaimiento para esta lección.

## 1. Empezar por la envolvente medida, no por el control

El [fixture GAS-001](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) fijado contiene dos WAV mono de cuatro segundos a 44 100 Hz: una grabación acústica independiente, etiquetada como mi2 al aire por su conjunto de datos, y un render **nativo** del motor Rust de GA en el commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. El render emplea el perfil de guitarra 0 predeterminado y `engine_note_on(82.4069 Hz, velocity 0.1)`. No es una captura del AudioWorklet del navegador. El [README del fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md) documenta los hashes, los límites de procedencia, el crédito y la atribución CC BY-SA 4.0 de la grabación.

El [JSON de mediciones](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) indica un cambio RMS tardío menos temprano de **−3.9 dB** en la grabación y **−1.1 dB** en el render. El [script de medición](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) toma las ventanas 0.2–0.4 s y 1.0–1.2 s **después del primer ataque de cada archivo**. El primer ataque grabado ocurre aproximadamente a 1.1 s y hay otro cerca de 2.75 s; el render comienza en cero. Las ventanas de la grabación caen así cerca de **1.3–1.5** y **2.1–2.3 s** del archivo, antes del segundo ataque. No son constantes de decaimiento de todo el archivo.

La caída seleccionada del render es **2.8 dB menos negativa**: `−1.1 − (−3.9) = +2.8 dB`. El error absoluto frente al cambio grabado es `|−1.1 − (−3.9)| = 2.8 dB`. Son valores ya redondeados a una décima. Los WAV tienen distintos niveles iniciales, instrumentos, micrófonos, salas y pulsaciones; aquí conviene más comparar *cambios* dentro de cada archivo que comparar sus RMS absolutos en dBFS. Incluso esta diferencia no identifica el parámetro causante ni la preferencia de quienes escuchan.

### Ejercicio 1 — Leer la diferencia

Con los valores guardados, calcula la diferencia con signo entre render y grabación para el cambio tardío menos temprano, y el error absoluto. ¿Significa un error de 2.8 dB que todo el render suena 2.8 dB más fuerte?

> **Respuesta:** `−1.1 − (−3.9) = +2.8 dB`; el error absoluto es `2.8 dB`. El nivel del render cae menos entre las dos ventanas RMS relativas al ataque. No es una comparación de sonoridad de archivos completos ni demuestra una preferencia auditiva.

### Ejercicio 2 — Excluir el segundo ataque

¿En qué tiempos del archivo caen ambas ventanas de la grabación si el primer ataque está aproximadamente en 1.1 s? ¿Por qué no sirve una ventana tardía que empieza en 2.8 s para estudiar la primera nota?

> **Respuesta:** La temprana es aproximadamente `1.1 + [0.2, 0.4] = 1.3–1.5 s`; la tardía, `1.1 + [1.0, 1.2] = 2.1–2.3 s`. Una ventana desde 2.8 s queda después del ataque adicional, cerca de 2.75 s, y mezclaría otro evento con el supuesto decaimiento. Como el inicio es aproximado, repite el análisis variándolo ligeramente antes de hacer afirmaciones firmes.

## 2. Seguir el parámetro Rust y su coeficiente efectivo

En el [motor Rust de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) fijado, `Engine::new` empieza con `decay = 0.9968`, pero luego elige el perfil 0 predeterminado, que establece el **decaimiento base en 0.9978**. La función exportada `engine_set_decay` limita el valor solicitado a `[0.95, 0.9999]`. Elige el perfil **antes** de aplicar el valor candidato: cambiarlo después reescribe el decaimiento y otros controles. El [renderizador del fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py) llama a `engine_init` y `engine_note_on`, pero no a `engine_set_decay`; una prueba candidata necesita una extensión documentada u otro banco de pruebas. Aquí no se informa de ninguna ejecución candidata.

Las expresiones pertinentes del bucle de render son:

```text
f_norm = clamp((voice_frequency_hz - 82) / (330 - 82), 0, 1)
voice.sustain = min(0.995 + 0.006 * (1 - f_norm), 0.9998)  # assigned at note excitation
feedback_decay = (base_decay + 0.0025 * (1 - f_norm)) * voice.sustain
```

Para la frecuencia nominal `82.4069 Hz`, `f_norm ≈ 0.00164073`. La expresión de sustain sin tope vale aproximadamente `1.00099016`, así que `voice.sustain = 0.9998`. Con base `0.9978`, la expresión produce `(0.9978 + 0.0025 × (1 − 0.00164073)) × 0.9998 ≈ 1.00009584`. Una base **propuesta** de `0.9976` produce aproximadamente **0.99989588**. Los dos valores base están dentro del límite permitido por el setter.

Son **coeficientes de realimentación calculados a partir del código**, no tasas medidas de decaimiento de la envolvente. El bucle también combina muestras de la línea de retardo, dispersión mediante un filtro paso todo, un filtro paso bajo con estado mezclado según el brillo, ruido de ataque, resonadores y reverberación. Que una expresión produzca un coeficiente apenas mayor que uno **no demuestra** por sí solo una salida inestable ni un defecto audible. Reducirlo tampoco predice un cambio concreto en dB del WAV. Hay que medir la salida con un método fijo.

El `attack_decay` separado controla la evolución del ruido de ataque; `reverb_mix` afecta a la cola y el brillo altera la mezcla de realimentación. No los cambies a la vez que el candidato de decaimiento: el origen de cualquier efecto se volvería ambiguo. GAS-002 ya trata el brillo; aquí permanece fijo.

### Ejercicio 3 — Calcular y limitar la inferencia

Para `82.4069 Hz`, ¿qué tope de sustain se aplica y cuáles son los coeficientes efectivos aproximados para las bases `0.9978` y `0.9976`? ¿Demuestra el primero, mayor que uno, que el WAV de GA aumenta su nivel con el tiempo?

> **Respuesta:** `f_norm ≈ 0.00164073`; la expresión sin tope supera `0.9998`, por lo que se aplica el tope `0.9998`. La expresión produce aproximadamente `1.00009584` con `0.9978` y `0.99989588` con `0.9976`. No: es un coeficiente dentro de un sistema filtrado, con estado, resonancias y reverberación. En las ventanas elegidas, el WAV guardado muestra de hecho `−1.1 dB`; el coeficiente no predice por sí solo su envolvente.

## 3. Declarar antes de medir una prueba de un parámetro

Una prueba nativa controlada compilaría **la misma revisión Rust fijada** e inicializaría un motor nuevo para cada brazo a 44 100 Hz. Mantén el perfil 0, mi2 `82.4069 Hz`, velocidad `0.1`, cuatro segundos, compilador, codificación WAV y todos los demás ajustes. El brazo base usa `0.9978`. En el candidato, llama a `engine_set_decay(0.9976)` **después** de inicializar y elegir el perfil, y **antes** de `engine_note_on`. Registra el orden, el valor, los hashes de ambos WAV y el inicio elegido. La fuente inicializa una semilla de ruido fija, pero hacen falta motores nuevos y la misma compilación para evitar arrastrar estado. El renderizador actual carece de una opción de decaimiento; adáptalo o reemplázalo y revisa ese código antes de extraer conclusiones empíricas. Una comparación nativa no certifica el AudioWorklet del navegador: pruébalo por separado si ese será el producto distribuido.

Aplica el mismo procedimiento de medida a ambos brazos. Una **regla didáctica propuesta** exige reducir el error absoluto al menos **1.0 dB** respecto al error base redondeado de `2.8 dB`: objetivo `≤ 1.8 dB` respecto a `−3.9 dB`. Con cifras redondeadas equivale a una caída candidata entre **−5.7 y −2.1 dB**. Para una decisión real, calcula las mediciones WAV sin redondear y registra una tolerancia, en vez de decidir en un límite de décimas usando el JSON redondeado. Es un umbral didáctico elegido de antemano, **no** un estándar de producto GA ni una predicción de que `0.9976` pasará.

Protege la comparación: sin recorte ni casi recorte (amplitud pico absoluta **inferior a 0.95** como propuesta), fundamental mi2 próxima a la base bajo la misma búsqueda de picos de un segundo, y revisión del ataque inicial y las trazas del segundo y cuarto parcial. Una mejor cifra RMS agregada puede esconder daños en el transitorio o la cola espectral. Repite con otras cuerdas, notas y velocidades antes de generalizar. Examina juicios de escucha ciegos y con niveles igualados: coincidir numéricamente con una guitarra externa no establece realismo percibido. Si falla la regla `≤1.8 dB` o alguna salvaguarda, rechaza **esta configuración candidata para esta prueba** y comunica el resultado. El fallo no prueba que ningún cambio de decaimiento pudiera ayudar.

### Ejercicio 4 — Aplicar la regla propuesta

Con los valores base redondeados, ¿cuál es el error absoluto máximo permitido para mejorar 1.0 dB? ¿Qué intervalo de caídas candidatas resulta alrededor de `−3.9 dB`? ¿Pasaría todas las salvaguardas un candidato en ese intervalo con un pico de `0.98`?

> **Respuesta:** `2.8 − 1.0 = 1.8 dB`; `|candidate − (−3.9)| ≤ 1.8` da `−5.7 ≤ candidate ≤ −2.1 dB`. Un pico de `0.98` incumple la salvaguarda propuesta `<0.95`, aunque el decaimiento pase. Es aritmética de una regla propuesta, no una medición candidata.

### Ejercicio 5 — Formular una refutación

Un agente afirma que bajar la base a `0.9976` mejora la amortiguación de mi2 en GA. ¿Qué artefactos controlados mínimos y qué resultado refutarían esa afirmación bajo la regla de la lección? ¿Qué seguiría sin conocerse después de una prueba satisfactoria solo con mi2?

> **Respuesta:** Guarda la revisión y compilación exactas del motor, el orden de llamadas, los WAV nativos de base y candidato generados por motores nuevos y sus hashes, la medición alineada al inicio y las verificaciones de pico, parciales y ataque. Si el error absoluto sin redondear no disminuye al menos 1.0 dB, o falla una salvaguarda, el candidato no supera la regla. Aunque la supere, seguirían sin verificarse la salida del navegador, otras notas y velocidades, las diferencias de grabación y las preferencias de escucha.

## 4. Separar mejora y calibración

La grabación es una **sonda de calibración**, no una meta física exacta para todas las guitarras. El conjunto la etiqueta mi2 al aire, pero sala, instrumento, micrófono e intérprete difieren del render. Un cambio global de `decay` puede afectar a muchas notas; la fórmula dependiente de la frecuencia hace especialmente insegura la extrapolación desde mi2. Si el candidato acerca la envolvente a la referencia, di solo que acercó **la medida tardía menos temprana especificada** del render probado. Si no, conserva el artefacto fallido para examinar después ruido de ataque, reverberación, realimentación dependiente de la frecuencia o sensibilidad a las ventanas, sin reescribir la historia.

El [bucle de iteración sin conexión](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) existente y su crítico espectral permiten repetir experimentos, pero no emiten automáticamente un veredicto de escucha. Un candidato procesado más adelante con ComfyUI sería **otro brazo sin conexión**, no evidencia de éxito del setter Rust. Separa propuestas de agentes, renders, referencias, hashes, mediciones, revisión y publicación pública.

## Fuentes y límites

- [Procedencia GAS-001](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md), [mediciones guardadas](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json), [método](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) y [renderizador nativo](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py), en Demerzel `5c4967454ddc740ed937c87719ca4d71a3522e4b`.
- [Motor Rust de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) y [script de iteración sin conexión](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), en GA `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Antes de esta lección solo se había medido el par GAS-001 guardado. Los coeficientes y el intervalo de aceptación son cálculos. Una revisión independiente del tema y de la coherencia de los borradores traducidos por IA no encontró problemas aplicables. Siguen pendientes el render candidato `0.9976`, la extensión del banco nativo, la captura del navegador, las pruebas de otras notas, el panel de escucha, la revisión humana, la prueba con estudiantes, la revisión lingüística y la publicación.
