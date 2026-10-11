---
module_id: aud-003-transient-preservation-gate
department: audio-engineering
course: "Preservar el ataque de una cuerda de guitarra durante el análisis espectral sin conexión"
level: intermediate
prerequisites: [aud-002-level-matched-guitar-comparison, phy-002-time-frequency-guitar-transients]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-003
version: "0.1.0"
---

# Preservar el ataque de una cuerda de guitarra durante el análisis espectral sin conexión

> **Departamento de Ingeniería de Audio** | Nivel: intermedio | Duración estimada: 35 minutos | Estado: borrador en español; revisión y publicación pendientes

## Objetivos

Al terminar esta lección, podrás:

- elegir entre una FFT del intervalo completo y una STFT según la decisión que debas tomar sobre el audio;
- configurar tamaños de ventana y salto válidos para el espectrograma de IX sin perder el ataque en todas las tramas;
- distinguir el eliminador de ruido Haar de IX de los análisis con wavelets centrados en frecuencias de la fixture GAS-001;
- rechazar una reducción de ruido que cambie un transitorio de guitarra más allá de un límite declarado; y
- definir una evaluación sin conexión que otro ingeniero pueda refutar usando los mismos WAV.

## La decisión del proyecto

La [fixture GAS-001 de la cuerda mi grave al aire](../../../fixtures/guitar-acoustics/gas-001/README.md), fijada en el commit de Demerzel [`5c496745`](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), contiene una grabación con licencia de E2 al aire y un render del motor nativo de GA. Ambos son WAV mono de cuatro segundos a 44 100 Hz. El primer ataque de la grabación ocurre aproximadamente 1,1 segundos después del comienzo del archivo; el render empieza en cero. La fixture registra otro ataque cerca de 2,75 segundos en la grabación. Es un par didáctico, no una prueba de referencia validada del realismo ni una captura del AudioWorklet del navegador.

[PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md) explica el compromiso entre tiempo y frecuencia e interpreta las mediciones FFT y con wavelets de tipo Morlet guardadas en la fixture. [AUD-002](../en/aud-002-level-matched-guitar-comparison.md) controla la alineación de los ataques y el nivel de reproducción antes de escuchar. Esta lección aborda otra decisión de ingeniería: **¿conviene quitar ruido a la referencia grabada antes de usar su ataque para evaluar un render de GA?** Una reducción aparente del ruido no basta. El procesado también puede atenuar, extender o desplazar el transitorio que el analista quería conservar.

El caso de implementación se fija en el commit de IX [`bd1336b7`](https://github.com/GuitarAlchemist/ix/tree/bd1336b7c4045e427dcdbe80b102790e45da5ce1). IX ofrece un [handler de FFT](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1297-L1315), un [handler de espectrograma](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189) y un [handler de eliminación de ruido con wavelets Haar](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797). Reciben arreglos numéricos de muestras, no rutas de archivos WAV. Harían falta un decodificador WAV y un banco de pruebas sin conexión reproducible para aplicarlos al par de audio fijado; esta lección no ha realizado esa ejecución.

## 1. Elegir la vista según la afirmación

La función [`rfft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/fft.rs#L84-L115) de IX transforma un arreglo finito de muestras reales y rellena con ceros las longitudes que no son potencia de dos hasta la siguiente potencia de dos. Pese a su nombre, devuelve el arreglo FFT completo. El handler `ix_fft` devuelve magnitudes y frecuencias en **ciclos por muestra**, suponiendo una frecuencia de muestreo de 1,0. A 44 100 muestras por segundo, multiplica una frecuencia normalizada **hasta Nyquist** por 44 100 para expresarla en hercios; la mitad superior refleja las frecuencias negativas. El espectro de magnitud de un archivo completo es válido para una señal cambiante, pero no indica qué ataque produjo un pico. Una FFT limitada a la primera nota sirve para un resumen armónico local, aunque todavía promedia el intervalo elegido.

La función [`stft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L30) de IX repite FFT con ventanas en posiciones sucesivas. [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L32-L54) usa una ventana de Hann y conserva magnitudes de un solo lado del espectro. Puede mostrar si la energía asociada al ataque aparece en una trama temprana y cómo cambia. Su opción `db=true` calcula `20 log10(max(magnitude, 1e-10))`; no es una medida dBFS calibrada. No compares directamente esos valores brutos en dB con los valores RMS en dBFS de GAS-001.

### Ejercicio práctico 1: elegir una salida capaz de responder

Un analista calcula `ix_fft` sobre los cuatro segundos completos del WAV grabado y afirma que un pico brillante pertenece al *primer* punteo y no al ataque posterior. ¿Qué parte del resultado es útil y qué debe calcularse antes de atribuir el pico a un evento?

> **Respuesta:** La FFT del archivo completo puede mostrar que el archivo contiene energía cerca de esa frecuencia, tras convertir ciclos por muestra a hercios. Sus magnitudes no tienen etiquetas temporales, así que no pueden atribuir el pico al primer punteo. Decodifica el WAV, marca el primer inicio aproximado, calcula por separado un intervalo declarado de la primera nota e inspecciona una STFT alineada con ambos ataques si importa su posición temporal. Conserva el archivo bruto y los intervalos de análisis en el registro.

## 2. Ajustar la STFT de IX a una pregunta sobre el ataque

El **handler del agente** IX exige que `window_size` sea una potencia de dos, al menos dos y no mayor que la señal. Esto importa porque, en otro caso, la FFT subyacente rellenaría una trama con ceros y el número de bins y la correspondencia de frecuencias anunciados por el handler serían incorrectos. El handler usa por defecto un `hop_size` de media ventana, convierte un salto indicado de cero en uno y comunica `n_frames` y `n_bins`. La función central `stft` no proporciona esas validaciones de entrada; un banco de pruebas que la llame directamente debe validar sus argumentos. Solo procesa tramas completas, sin extender de forma implícita una cola corta.

Para una vista **propuesta** del primer ataque a 44,1 kHz, elige una ventana de 2 048 muestras y un salto de 512 muestras. La ventana abarca unos **46,44 ms**, el salto unos **11,61 ms**, y la cuadrícula FFT tiene `44,100 / 2,048 ≈ 21.53 Hz` por bin; la magnitud unilateral contiene **1 025 bins**. Esa cuadrícula es demasiado gruesa para resolver con una sola trama una discrepancia de un hercio en la altura. Una ventana mayor, de 8 192 muestras, abarca unos 185,76 ms y tiene bins separados por 5,38 Hz, pero mezcla más el ataque con el decaimiento. Un salto menor produce más tramas solapadas; no mejora la discriminación en frecuencia de cada trama. Estos son cálculos a partir de la configuración, **no** salidas de IX medidas sobre los WAV.

### Ejercicio práctico 2: especificar una petición válida a IX

A 44 100 Hz, calcula la duración de la ventana, el intervalo de salto y la separación nominal entre bins para `window_size=2048` y `hop_size=512`. ¿Cuántos bins debería indicar el handler de espectrograma de IX? ¿Por qué rechazaría `window_size=2205`, que representa exactamente 50 ms?

> **Respuesta:** La duración es `2048/44100 ≈ 46.44 ms`, el salto `512/44100 ≈ 11.61 ms` y la separación `44100/2048 ≈ 21.53 Hz`. El handler indica `2048/2 + 1 = 1025` bins. Rechaza 2 205 porque no es potencia de dos; una llamada directa a la función central podría rellenarlo con ceros, pero sería incorrecto interpretar sus bins como si la longitud de FFT fuera 2 205.

Una ventana de Hann llega a cero en los extremos. Esto ayuda con las discontinuidades del borde, pero un transitorio justo en un extremo puede desaparecer de esa trama. Con el solapamiento, la misma muestra ocupa otra posición en una trama diferente. Es una cuestión de **colocación del análisis**, no una afirmación de que el solapamiento cree información nueva. La [función de ventana](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/window.rs#L10-L15) y el [bucle de tramas](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L14-L29) de IX permiten comprobar el efecto del borde sin grabar una guitarra.

### Ejercicio práctico 3: mantener visible un impulso en el borde

Toma un arreglo sintético de 64 muestras, todo a cero excepto el índice 16, que vale 1. IX usa una ventana de Hann de 16 muestras. Con salto 16, ¿qué trama completa contiene el impulso y qué le ocurre? ¿Qué cambia con salto 8?

> **Respuesta:** Con salto 16, las tramas empiezan en 0, 16, 32 y 48. Solo la trama que empieza en 16 contiene el índice 16; este queda en el desplazamiento 0 de la ventana, donde el peso Hann es cero. Por tanto, todos los espectros devueltos pueden omitir ese impulso aislado. Con salto 8, la trama que empieza en 8 también lo contiene, en el desplazamiento 8, cuyo peso Hann es aproximadamente 0,989; esa trama sí muestra energía. Es un cálculo sintético derivado del código fuente, no una medición de IX sobre un WAV. Muestra por qué conviene verificar el salto propuesto de 512 muestras cerca de los límites de ataques reales.

## 3. Un eliminador de ruido Haar puede cambiar la evidencia

La función [`haar_forward`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L18) de IX forma promedios y diferencias por pares. [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L60-L82) aplica umbral suave a los coeficientes de detalle y reconstruye la señal. Es un tratamiento discreto Haar, **no** el análisis con wavelets complejas de tipo Morlet centradas en frecuencias y guardado en GAS-001. Ambos métodos producen resultados distintos y responden a preguntas diferentes. Un coeficiente de detalle Haar puede señalar un cambio rápido, pero al aplicar el umbral también puede eliminar parte de un punteo real junto con el ruido.

El handler de IX exige `levels >= 1`, un umbral finito no negativo y una longitud de entrada divisible por `2^levels`. En otro caso rechaza la petición porque la transformada Haar central puede perder las muestras impares finales. Su [prueba de ruido](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1387-L1411) incluida en el código usa una rampa suave con ruido alternante añadido y comprueba una menor media de errores cuadráticos. No comprueba si se conserva un ataque de guitarra aislado. Las [pruebas de validación](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1525-L1543) separadas cubren un tamaño de espectrograma inválido y una longitud de entrada indivisible para wavelets.

### Ejercicio práctico 4: predecir el cambio del transitorio

Para la señal sintética de ocho muestras `[0, 1, 0, 0, 0, 0, 0, 0]`, aplica las ecuaciones Haar de IX de un nivel con umbral suave 1. ¿Cuáles son las dos primeras muestras reconstruidas? ¿Respalda el resultado la afirmación de que eliminar ruido mediante wavelets siempre conserva el pico de un punteo?

> **Respuesta:** El primer par tiene aproximación `1/sqrt(2)` y detalle `-1/sqrt(2)`. Como la magnitud del detalle es inferior al umbral 1, el umbral suave lo convierte en cero. La inversa da `[0.5, 0.5]` para el primer par y deja los demás a cero. El pico aislado baja de 1 a 0,5 y se extiende una muestra hacia antes. El cálculo refuta una conservación incondicional; no predice qué umbral conviene para un WAV de guitarra grabado.

## 4. Declarar de antemano una condición de preservación sin conexión

La siguiente es una **receta de evaluación propuesta**, no una ejecución ni un estándar de aceptación de GA. Conserva ambos WAV de la fixture y sus hashes completos. Decodifica cada uno como muestras mono `f64` normalizadas sin sobrescribir el original. Registra el decodificador, la frecuencia de muestreo, el número de muestras y cualquier remuestreo; rechaza los cambios silenciosos de frecuencia. Usa los marcadores de inicio aproximados de la fixture (grabación 1,1 s; render 0,0 s) e inspecciona por separado los fragmentos del primer ataque y el ataque posterior grabado. Conserva una rama bruta y una rama de copia procesada en las mismas posiciones y con la misma ganancia. Ejecuta la vista STFT de IX sobre ambas ramas con los ajustes declarados 2 048/512; etiqueta las tramas por **muestra inicial y duración de ventana**, no solo por el centro visual de una columna. Registra si la conclusión sobre un inicio en el borde se mantiene al usar otro salto o desplazar un poco el marcador de inicio.

Antes de cualquier ejecución Haar, declara `levels` y el umbral, comprueba que la longitud exacta de entrada sea divisible por `2^levels` y guarda la política de relleno o recorte si hace falta. Por ejemplo, un fragmento de un segundo con 44 100 muestras **no** es divisible por ocho para tres niveles: deja resto cuatro. Rellenar con cuatro ceros hasta 44 104 es una opción que debe declararse; añade un borde que puede afectar a los coeficientes cercanos. Otra opción es cambiar el límite del fragmento o usar menos niveles. No llames directamente a la función central con una entrada de longitud impar suponiendo que la salida conservará la alineación.

Para la referencia grabada, mide un intervalo de ruido previo al ataque y un intervalo fijo del primer ataque, ambos declarados, en las copias bruta y procesada. Una **condición didáctica**, elegida antes de conocer el resultado, podría exigir al menos **3 dB** menos de RMS previo al ataque y conservar el valor absoluto del pico del primer ataque dentro del **10 %** del original y el instante de ese pico dentro de **1 ms**. Exige que no haya saturación y que el número de muestras sea el mismo después de cualquier recorte documentado. Vuelve a comprobar con marcadores de inicio desplazados ±5 ms y comunica todos los umbrales candidatos, incluidos los que fallen. El render de GA comienza en el instante cero del archivo y, por tanto, no tiene un intervalo equivalente de ruido previo al ataque; no le apliques esa parte de la condición. Conserva la grabación sin procesar como referencia principal. Superar estas aproximaciones basadas en la forma de onda permitiría una comparación auditiva aparte, documentada y con niveles igualados; **no** demostraría que el archivo procesado sea perceptualmente idéntico ni que GA suene realista.

### Ejercicio práctico 5: aplicar la condición e indicar su límite

Un ingeniero propone una ejecución Haar de tres niveles sobre un fragmento grabado de 44 100 muestras sin relleno. También presenta un candidato *hipotético* con 4 dB menos de RMS previo al ataque, un pico de ataque de 0,82 veces el pico original y un desplazamiento del instante del pico de 0,2 ms. ¿Qué debe cambiar para que el handler de IX acepte el fragmento? ¿Superaría el candidato la condición didáctica?

> **Respuesta:** `44,100 mod 8 = 4`, así que el handler rechaza tres niveles para esa longitud. Declara cuatro muestras añadidas para llegar a 44 104 y una política de recorte, elige otro fragmento o reduce los niveles. El candidato hipotético falla aunque el ruido baje más de 3 dB y el cambio temporal quede dentro de 1 ms: `1 - 0.82 = 0.18`, una pérdida del pico del 18 %, supera el límite declarado del 10 %. Ese rechazo trata de preservar el transitorio según esta condición indirecta; no es un resultado medido en ninguno de los WAV de la fixture ni un veredicto de escucha.

## Fuentes y límites

- El audio del proyecto y su procedencia vienen de la [fixture GAS-001 en el commit de Demerzel `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). La grabación y el render nativo de GA proceden de fuentes diferentes, con cadenas de interpretación y producción distintas. Sus resultados FFT y Morlet guardados son observaciones de esa fixture, no resultados de IX.
- La STFT, la FFT, las ecuaciones Haar, las validaciones de los handlers y las pruebas citadas arriba son observaciones del código fuente de IX en `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Las dimensiones 2 048/512, el ejemplo del impulso en el borde de Hann, el resultado Haar de ocho muestras y la aritmética de divisibilidad son **ejemplos derivados**. Para AUD-003 no se produjo ni midió ningún espectrograma de IX ni ningún WAV procesado.
- Una magnitud de análisis no es una puntuación calibrada de sonoridad o realismo. Los marcadores de inicio son aproximados; las ventanas espectrales, el relleno, los umbrales, el decodificador y la ganancia de entrada pueden cambiar el resultado. Un impulso sintético revela un posible modo de fallo, pero no predice el comportamiento de todos los punteos.
- Quedan pendientes la revisión del contenido, los intentos de estudiantes, la revisión por hablantes nativos, la sincronización y compilación de Learn y la lectura pública. Este texto en español es un borrador, no un curso publicado.
