---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Probar el orden de ecualización y compresión en una guitarra"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-004
version: "1.1.0"
---

# Probar el orden de ecualización y compresión en una guitarra

> **Departamento de ingeniería de audio** | Nivel intermedio | 35 minutos | Borrador revisado en español; revisión técnica, intentos de alumnos y publicación pendientes

## Objetivos y pregunta del proyecto

Distinguirás un filtro de un procesador dependiente del nivel, demostrarás con un cálculo pequeño que su orden importa y diseñarás una comparación sin conexión que una futura implementación de compresor pueda refutar. **Pregunta del proyecto:** si GA estudia procesar un Mi2 al aire grabado o su versión renderizada por el motor de guitarra, ¿colocar una ecualización elegida antes de comprimir cambia el ataque y el nivel respecto a colocar esa *misma* ecualización después? Una decisión de procesamiento necesita resultados medidos con la misma entrada, no una regla genérica sobre qué orden suena más natural.

La [fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) ofrece un par concreto de guitarra: un WAV mono de Mi2 al aire grabado y otro generado por el motor nativo de GA, ambos de cuatro segundos a 44.100 Hz. El primer ataque grabado comienza **aproximadamente a 1,1 s** del inicio del archivo; hay otro hacia **2,75 s**. El render comienza en el tiempo cero. Las [mediciones de la fixture](../../../fixtures/guitar-acoustics/gas-001/measurements.json) muestran diferencias de balance de parciales y decaimiento en determinadas ventanas, pero no clasifican el realismo ni demuestran que algún archivo necesite compresión. Conserva ambos WAV originales. Usa primero el archivo *grabado* como entrada propuesta; reserva el render para una réplica posterior identificada por separado. No compares audio procesado con un archivo sin procesar como si solo hubiera cambiado el orden.

El [motor de audio del navegador GA en el commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) carga un motor WASM en un [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), lo conecta a los altavoces y ofrece una ruta MediaRecorder. El render GAS-001 procede de una **compilación nativa del mismo código Rust**, no de una captura de ese worklet. Las fuentes inspeccionadas documentan la procedencia de la señal de guitarra, no una cadena de ecualizador y compresor en la demo. En el [commit IX `bd1336b`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs), `FirFilter` ofrece diseño de filtros paso bajo y paso alto y un método `apply` para muestras. Es una posible pieza de filtro sin conexión. Estos artefactos no prueban que exista un compresor; antes de un ensayo A/B real habría que especificarlo y revisarlo.

## 1. Definir con precisión las dos operaciones

Un filtro FIR es lineal. Con coeficientes `h`, su salida es `E(x)[n] = Σ_k h[k] x[n-k]`, con una regla de límites explícita. `FirFilter::apply` de IX empieza con una salida de ceros e incluye solo términos cuyo índice de entrada no es negativo. Un paso bajo o paso alto puede cambiar el nivel que recibe después un detector. La respuesta exacta depende de los coeficientes y el filtro también puede desplazar o extender un ataque. Llamar a cualquier ajuste «ecualización correctiva» no demuestra que mejore la señal de guitarra.

Un compresor depende del **nivel**. Su ganancia depende de la entrada y, en un diseño convencional, de la envolvente de un detector con estado de ataque y liberación. La forma de onda puede variar con el umbral, la relación, el tipo de detector, las constantes de tiempo, la vinculación de canales, la ganancia de compensación y la inicialización. Hay que registrar esos detalles. Un compresor de banda completa no selecciona frecuencias automáticamente: su detector responde al nivel de la forma de onda, influido por varios parciales. Decir que «el compresor oye 200 Hz» es una simplificación, no una garantía sobre el componente que provocó la reducción de ganancia. El filtrado de cadena lateral, la compresión multibanda y la ecualización dinámica serían experimentos diferentes.

Sean `E` la ecualización elegida y `C` el compresor. Las cadenas propuestas son `A = E(C(x))` (**Comp→EQ**) y `B = C(E(x))` (**EQ→Comp**). Las dos deben usar el mismo `x`, coeficientes EQ, parámetros del compresor, frecuencia de muestreo y formato de canales. `C` recibe `x` sin filtrar en A y `E(x)` filtrado en B. La EQ final de A no puede deshacer una decisión anterior del detector. El compresor de B sí puede reaccionar a picos creados o eliminados por la EQ. Ningún orden es universal: la intención sonora y los compromisos medidos deben guiar la elección.

### Ejercicio práctico 1: identificar la entrada del detector

En A y B, ¿qué entra exactamente en `C`? Si la EQ realza un parcial elegido de la guitarra, ¿en qué cadena *podría* cambiar la reducción de ganancia por ese realce?

> **Respuesta:** En A, `C` recibe `x` sin filtrar; en B recibe `E(x)`. El aumento del parcial puede influir directamente en el detector de banda completa de B. En A, la EQ va después del compresor y no puede cambiar su decisión previa de ganancia. Es una afirmación de causalidad, no una predicción sobre audibilidad o cantidad de reducción.

## 2. Demostrar la dependencia del orden con una fixture sintética

Usa una señal de cuatro muestras deliberadamente **sintética**, `x=[0,2,0,0]`, con historial previo cero. Define el FIR `E` con `h=[0.5,0.5]`, de modo que `E(x)[n]=0.5x[n]+0.5x[n-1]` para muestras disponibles. Este promedio de dos coeficientes es un ejemplo matemático de paso bajo, **no** un ajuste EQ recomendado para guitarra ni los coeficientes generados por el diseñador `lowpass` de IX. Define un compresor didáctico sin memoria, umbral `T=1`, relación `R=2:1`, sin ganancia de compensación, ataque ni liberación: `C(v)=sign(v) × (|v| if |v|<=1 else 1+(|v|-1)/2)`. Convierte una muestra positiva `2` en `1.5`. Un compresor real de envolvente requiere estado adicional y puede producir otros números.

Calcula A: `C(x)=[0,1.5,0,0]` y después `E(C(x))=[0,0.75,0.75,0]`. Calcula B: `E(x)=[0,1,1,0]` y después `C(E(x))=[0,1,1,0]`, porque ninguna muestra filtrada no nula supera el umbral. Las salidas difieren en `0.25` en las muestras 1 y 2. Es un contraejemplo exacto a `E∘C = C∘E` para los operadores declarados. El cálculo **no** mide la grabación GAS-001, **no** predice la salida de un plugin no especificado y **no** demuestra que B suene mejor.

Los picos distintos, `0.75` para A y `1` para B, advierten contra juzgar el orden con volumen no controlado. La comparación auditiva exige igualar el nivel de reproducción **después** de cada cadena completa y registrar la ganancia aplicada. No cambies por separado los umbrales para forzar reducciones similares: eso alteraría la pregunta experimental. En un pasaje real donde ambas cadenas permanezcan bajo el umbral, las salidas pueden ser idénticas o casi idénticas pese al contraejemplo sintético.

### Ejercicio práctico 2: calcular ambas cadenas

Con los `x`, `h` y `C` declarados, escribe A y B. ¿Cuánto vale `B[1]-A[1]` y qué conclusión permite el cálculo?

> **Respuesta:** `A=[0,0.75,0.75,0]`; `B=[0,1,1,0]`; `B[1]-A[1]=0.25`. Los operadores especificados no conmutan para esta entrada sintética. El cálculo no da un veredicto auditivo ni resultados para un compresor real de envolvente o un WAV de guitarra.

### Ejercicio práctico 3: tratar el borde

Con historial previo cero y `h=[0.5,0.5]`, ¿cuánto valen `E([2,0])[0]` y `E([2,0])[1]`? ¿Por qué debe un proceso sin conexión registrar el tratamiento del borde y la latencia?

> **Respuesta:** Ambos valen `1`. En el índice 0, la muestra anterior inexistente aporta cero; en el índice 1, la muestra anterior de entrada es `2`. Otro criterio de relleno o calentamiento cambiaría las primeras muestras. Los FIR prácticos más largos pueden introducir retardo de grupo: hay que alinear salidas y registrar la regla del borde antes de interpretar diferencias temporales entre picos.

## 3. Diseñar una comparación A/B refutable para guitarra

Lo siguiente es un **experimento sin conexión propuesto, no ejecutado**. Empieza con `deb-low-e-open.wav` del [directorio de la fixture](../../../fixtures/guitar-acoustics/gas-001/README.md), cuyo SHA-256 es `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`. Decodifica una sola vez sus muestras WAV mono float32 y conserva los bytes originales. Registra decodificador, frecuencia de muestreo, hash de entrada y primer ataque aproximado; inspecciona la forma de onda antes de fijar una ventana que excluya el segundo ataque. Una segunda ejecución podría usar `ga-engine-e2-open-4s.wav`, pero debe informarse aparte: es un render nativo con otro inicio y distinta procedencia.

Antes de implementar el futuro compresor, escribe un contrato de parámetros: umbral en dBFS, relación, unidades de ataque y liberación, detector de pico o RMS, anticipación, codo, ganancia de compensación, reinicio del estado y comportamiento en la primera muestra. Fija la revisión del código y las pruebas. Usa una sola EQ determinista: publica coeficientes FIR literales o fija el [código de filtro IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) y registra corte, orden, coeficientes y tratamiento de límites. Usa los *mismos* ajustes de EQ y compresor en ambas cadenas; reinicia por separado el estado del compresor antes de cada render. Exporta WAV A y B sin pérdidas a igual frecuencia y guarda la traza de reducción de ganancia, el número de muestras y el manifiesto. No afirmes que GA o IX ya ofrece esta cadena completa.

Elige la ventana del primer ataque relativa al inicio grabado **aproximado de 1,1 s**, anotando el índice de muestra elegido en el manifiesto. Para cada cadena, informa muestra y tiempo del pico, RMS de ventana corta o envolvente cerca del ataque, RMS posterior y traza de reducción de ganancia. Igualar el nivel de salida para escuchar exige registrar el ajuste y distinguir medidas brutas de medidas igualadas. Evita clipping después de compensar o igualar nivel. Si la latencia FIR difiere de una ruta sin tratamiento, alinea con una regla documentada de retardo o correlación cruzada antes de comparar tiempos de pico. Una prueba de escucha, si se aprueba después, debería ocultar las etiquetas, aleatorizar el orden y permitir «sin diferencia perceptible»; es distinta de la verificación numérica.

El **falsador** de la hipótesis estrecha «la posición de la EQ cambia este pasaje de guitarra con estos ajustes fijados» sería que A y B sigan siendo idénticas muestra por muestra dentro de una tolerancia numérica predefinida, o que una diferencia aparente desaparezca tras corregir un error de alineación, reinicio o nivel. Si difieren, examina la entrada del detector y las trazas de reducción de ganancia para atribuir el mecanismo. Una diferencia no prueba que un orden sea más natural. Una EQ neutra o un compresor que nunca cruza su umbral puede dar un resultado nulo útil. Afirmar que un orden conserva mejor el ataque requeriría una métrica de ataque declarada, una dirección, una tolerancia aceptable y una escucha si la percepción forma parte de la afirmación.

### Ejercicio práctico 4: conservar la validez de la fixture

Un proceso propuesto trata el WAV grabado entre `0.0–1.0 s`, lo compara con el render en el mismo intervalo temporal de archivo y concluye que EQ→Comp conservó mejor el ataque. Nombra dos problemas independientes.

> **Respuesta:** El primer ataque grabado no llega hasta cerca de `1.1 s`, así que la ventana `0.0–1.0 s` es principalmente tiempo previo, mientras el render empieza en cero. Las ventanas no están alineadas por ataque. Además, comparar dos archivos fuente distintos no aísla el orden de procesamiento: A y B deben usar el **mismo WAV de origen**. Ningún archivo es una referencia de realismo validada.

### Ejercicio práctico 5: elegir la siguiente comprobación

Una futura ejecución encuentra una diferencia de `0.2 dB` en el RMS de la ventana del primer ataque entre A y B, pero las salidas no están alineadas y falta el manifiesto de ajustes del compresor. ¿Respalda esto un orden preferido? ¿Qué pruebas hay que pedir?

> **Respuesta:** No. Conserva primero el hash de entrada y la ventana; publica versión y ajustes del compresor; verifica reinicios independientes, alinea latencia y ataque, confirma los mismos coeficientes EQ y ausencia de clipping. Ejecuta de nuevo y compara medidas brutas y trazas de reducción de ganancia. Si la afirmación trata de calidad sonora, iguala el volumen después de procesar para una escucha ciega independiente. `0.2 dB` por sí solo no identifica la etapa responsable ni establece una preferencia.

## Evidencia y límites

- El [README de la fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) documenta los archivos E2 grabado y renderizado nativamente, hashes, atribución, ataques aproximados y límites de las mediciones. La [lección GAS-001](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) y sus medidas guardadas se refieren a la comparación *sin procesar*, no a un ensayo de EQ y compresión.
- El [enrutamiento del navegador GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), su [worklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) y el [FIR IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) documentan la ruta de guitarra y una operación de filtrado disponible. No prueban un compresor implementado, una prueba del orden EQ-compresor ni un resultado de WAV procesado.
- El cálculo de cuatro muestras es sintético. La comparación A/B, sus umbrales y métricas se proponen. No se construyó ni ejecutó un compresor para esta lección; no hay aquí WAV de guitarra procesado, veredicto de escucha ciega ni decisión de enrutamiento de producción. Siguen pendientes las revisiones técnica y pedagógica, la traducción, la sincronización y compilación de Learn y la lectura pública anónima. El ciclo de investigación de 2026-03-23 sigue siendo un artefacto histórico sobre voz; esta revisión usa el nuevo ciclo indicado en el frontmatter.
