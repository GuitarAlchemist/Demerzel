---
module_id: phy-005-sheet-thickness-and-scene-units
department: physics
course: Grosor de láminas de las coordenadas IX a las unidades de escena propuestas
level: intermediate
prerequisites: [basic-ratios, dimensional-analysis]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-21-005
version: "0.1.0"
---

# Grosor de láminas: de las coordenadas IX a las unidades de escena propuestas

> **Departamento de Física** | 40 minutos | Borrador ES; revisión especializada y prueba con un estudiante pendientes. EN/FR/ES son borradores; faltan PT/IT/DE.

## Objetivos y problema del proyecto

Una lámina de IX puede tener coordenadas entre cero y uno, aunque el grosor del material se mida en milímetros. Un futuro artefacto de Blender o Godot necesita otra escala de longitud declarada. Pasar el número `0.4` sin conversión entre las tres representaciones convertiría una cartulina normal en una lámina 150 veces más gruesa, o introduciría un error de factor 1000 entre milímetros y metros de escena.

Al terminar podrás deducir el grosor y las alturas de apilamiento en cada representación, distinguir capas locales de niveles de paneles paralelos, diagnosticar dos errores de escala y preparar una entrega limitada por sus pruebas. Dedica 12 minutos a las derivaciones, 18 a los ejercicios antes de leer las respuestas y 10 a la tarea de transferencia. Esta lección trata longitudes geométricas y conversiones. La velocidad de excitación de la guitarra corresponde a PHY-004; la reconstrucción de un estado plegado pertenece a la secuencia de visual computing.

Las fuentes se fijan en el commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [`thickness.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), sus [pruebas existentes](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) y [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs). Se inspeccionaron definiciones y aserciones. El agente coordinador ejecutó el objetivo específico de grosor en ese HEAD sin cambios: 11 pruebas aprobadas y ningún fallo. Eso no representa toda la suite. Los [casos aritméticos](../../../fixtures/physics/phy-005/scenarios.json) contienen ejemplos modelados; su [README](../../../fixtures/physics/phy-005/README.md) explica cómo reproducirlos.

## 1. Declarar una regla antes de convertir coordenadas

Sea `C` el ancho de la lámina en unidades de coordenadas del patrón de pliegues, `W` su ancho físico supuesto en mm y `h` el grosor completo del material en mm. Define `a=W/C`, en mm por unidad de coordenadas:

```text
x_mm = x_cp × a
t_cp = h/a = h × C/W
H_mm = H_cp × a
```

El subíndice identifica una representación; no afirma que IX almacene metadatos físicos. Aquí `W` es una suposición externa. Un archivo con un cuadrado unidad no revela si la lámina real tiene 150 o 300 mm de ancho. El grosor es completo: no es la mitad del grosor ni un recuento de caras.

La prueba de la grulla describe explícitamente cartulina de 0.4 mm sobre una lámina de 150 mm cuyo patrón es el cuadrado unidad. Por tanto `C=1`, `W=150`, `a=150` y `t_cp=0.4/150=0.0026666667`. La conversión inversa da `0.0026666667 × 150 ≈ 0.4 mm`. Conserva la fracción hasta mostrar el resultado final para reducir el error de redondeo.

`lib.rs` describe un reescalado por potencias de dos antes de las comprobaciones con tolerancias absolutas: el ancho del patrón queda entre uno y dos. Es acondicionamiento numérico, sin declarar metros ni medir físicamente la lámina. `stack(ctx,t)` utiliza el `t` proporcionado sin cambiarlo en sus multiplicaciones; no puede deducir `W` ni convertir implícitamente `0.4 mm`. Conserva una correspondencia externa explícita para la representación que transfieres.

### Ejercicio práctico 1: corregir el grosor de entrada

Una entrega de la grulla en cuadrado unidad etiqueta `t=0.4` como «0.4 mm». Calcula el `t_cp` correcto, el grosor físico representado por el valor erróneo y el factor de error.

> **Respuesta:** `t_cp=0.4/150=0.0026666667`. Con `a=150 mm/cp`, `0.4 cp` significa `60 mm`, es decir, `60/0.4=150` veces el grosor deseado. Sustituye el número y declara la correspondencia; cambiar únicamente la etiqueta no convierte el valor.

## 2. Separar las dos lecturas del apilamiento

La implementación calcula `ply` como el máximo número de caras en una celda de superposición. Su altura es `ply_height=ply × t`. Esta lectura permite que una cara ocupe alturas distintas en celdas distintas, como una lámina que se adapta o cae. Es una cota inferior para apilamientos que mantienen las posiciones planas declaradas.

Para paneles rígidos paralelos, las caras unidas por juntas planas comparten panel. Una arista dirigida conecta el panel inferior con el superior por cada par superpuesto cuyo orden está declarado. Si el orden es acíclico y todos los pares de paneles superpuestos están determinados, `levels` es la longitud de la cadena más larga y `height=levels × t` es la altura mínima de este modelo restringido. Si faltan órdenes, el número comunicado es una cota inferior; `levels_exact=false` y no existe `face_levels`. El recuento no tiene dimensión; una altura usa las mismas unidades que `t`.

La prueba existente de la grulla exige `ply=28`, exactamente 36 niveles rígidos, ningún par indeterminado y 59 entradas de niveles que respetan el orden declarado. Incluye una cadena de 36 caras. Son aserciones sobre ese caso y esa interpretación, no una especificación universal de grullas. Las fórmulas dan:

```text
altura ply:    28 × (0.4/150) = 0.0746666667 cp = 11.2 mm
altura rígida: 36 × (0.4/150) = 0.096 cp        = 14.4 mm
```

Una colocación ilustrativa con superficies inferiores `z_k=k×t` sitúa la superficie inferior más alta en `35t` para 36 niveles ocupados. La parte superior de la última placa llega a `36t`. Un desplazamiento de superficie difiere de la extensión total del apilamiento. Es una convención de dibujo propuesta, no geometría exportada por IX.

### Ejercicio práctico 2: desplazamiento o extensión

Una descripción dice: «La grulla tiene 28 capas, así que el apilamiento rígido mide 11.2 mm; el nivel rígido máximo es 35, por lo que su altura es 35t». Corrige ambas frases con las suposiciones de la prueba.

> **Respuesta:** La lectura de 28 capas locales da 11.2 mm. La lectura de paneles rígidos paralelos tiene exactamente 36 niveles y una extensión completa de `36×0.4=14.4 mm`. Según la convención propuesta, el nivel 35 empieza en `35×0.4=14.0 mm` y termina en 14.4 mm. El índice entero del nivel no equivale al número de niveles ocupados.

## 3. Deducir explícitamente una futura escala de escena

Supón que un futuro artefacto elige `u=1 unidad de escena por metro`. Es una elección didáctica, no una configuración verificada de Blender o Godot. El factor es `b=u/1000` unidades de escena por mm; por tanto `x_scene=x_cp×a×b`. Aplica el mismo multiplicador a todas las longitudes de la misma geometría, incluido el grosor y las alturas calculadas.

Para la lámina de referencia, una unidad de coordenadas corresponde a `150/1000=0.15` unidades de escena. Así, `t_scene=(0.4/150)×0.15=0.0004`, la altura ply es `0.0112` y la rígida `0.0144`. El camino físico independiente da `14.4 mm × (1/1000)=0.0144 unidades de escena`. La coincidencia verifica el cálculo, sin demostrar una cadena de importación.

Si otra vista didáctica elige `u=100 unidades de escena por metro`, todas las longitudes de escena se multiplican por 100. El ancho pasa a 15 y la altura rígida a 1.44. El grosor físico sigue siendo 0.4 mm. La elección de escala cambia la representación del material.

### Ejercicio práctico 3: detectar un factor 1000

Una escena propuesta a escala de metros usa ancho `0.15`, grosor `0.4` y altura rígida `14.4`. Calcula las dos longitudes menores correctas y un cociente que detecte el problema sin depender de la escala de escena.

> **Respuesta:** El grosor debe ser `0.0004` y la altura rígida `0.0144` unidades de escena. Los dos valores proporcionados son 1000 veces mayores. Los cocientes correctos son `grosor/ancho=0.4/150≈0.0026666667` y `altura rígida/ancho=14.4/150=0.096`. La escena errónea tiene aproximadamente 2.6667 y 96. Un reescalado uniforme coherente conserva estos cocientes adimensionales.

## 4. Cambiar una suposición cada vez

Cambiar el material y ampliar la geometría responden a preguntas diferentes. En la misma lámina de 150 mm, duplicar el grosor a 0.8 mm duplica `t_cp`, ambas alturas y sus longitudes de escena. No cambia el orden de caras de la entrada. La prueba existente `heights_scale_with_the_thickness` compara `t=0.25` con `0.5`, exige alturas dobles y los mismos niveles de caras. Esos valores prueban una relación algebraica; no miden cartulina.

Mantener material de 0.4 mm sobre una lámina de 300 mm reduce `t_cp` a la mitad en la representación de cuadrado unidad. Las alturas físicas siguen siendo 11.2 y 14.4 mm para la misma configuración combinatoria declarada. Si se duplican todas las longitudes físicas, incluido el grosor, `t_cp` se conserva y las alturas físicas se duplican. Explica a qué transformación te refieres con «ampliar».

Representar la misma lámina de 150 mm con `C=2` da `a=75 mm/cp`, `t_cp=0.0053333333` y altura rígida `0.192 cp`. Multiplicar por 75 devuelve 14.4 mm. Es una derivación dimensional para una representación modificada de manera coherente, no una nueva ejecución observada de IX.

### Ejercicio práctico 4: comparar tres cambios

Desde la referencia, calcula `t_cp` y la altura rígida en mm para A: grosor 0.8 mm, ancho 150 mm, `C=1`; B: grosor 0.4 mm, ancho 300 mm, `C=1`; C: lámina física original representada con `C=2`. Supón el mismo orden exacto de 36 niveles.

> **Respuesta:** A: `t_cp=0.8/150≈0.0053333333`, altura `36×0.8=28.8 mm`. B: `t_cp=0.4/300≈0.0013333333`, altura 14.4 mm. C: `t_cp=0.4×2/150≈0.0053333333`, altura 14.4 mm. A y C comparten grosor en coordenadas, pero describen suposiciones físicas distintas. Cada número necesita su regla.

## 5. Explicar qué establece una altura convertida

El comprobador lee un estado plano plegado declarado. `lib.rs` explica que sus comprobaciones locales no prueban la plegabilidad plana global ni calculan el orden de las capas. `thickness.rs` restringe su interpretación a paneles paralelos con una única altura por panel. Un ciclo impide esa interpretación si `t` es positivo; con grosor cero se informa sin rechazo. Una altura rígida ausente debido a un ciclo no es un cero medido.

Incluso una altura exacta y acíclica no prueba la realizabilidad física de un plegado grueso: bisagras, contacto, flexión y trayectoria quedan fuera del cálculo. La fuente señala que paneles inclinados pueden eludir un rechazo del modelo paralelo y que el contacto exacto en pliegues gruesos introduce otra limitación. Este curso no produce exportador, malla, collider, simulación dinámica, ensayo de material ni integración activa Blender/Godot/DLSS.

### Ejercicio práctico 5: redactar la entrega

Escribe tres frases para quien prepare un futuro artefacto visual: una sobre las pruebas, otra sobre la correspondencia de escena y otra sobre una afirmación física o de integración todavía no establecida.

> **Respuesta:** «En el commit IX fijado `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, las aserciones inspeccionadas de la grulla especifican 28 capas locales y 36 niveles paralelos exactos con `t=0.4/150`; el coordinador también informa de 11 pruebas de grosor aprobadas en esa revisión sin cambios. Suponiendo una lámina de 150 mm y una unidad de escena por metro, las extensiones ply y rígida deducidas son 0.0112 y 0.0144 unidades de escena. Estas conversiones no establecen ni la realizabilidad física del plegado ni una importación Blender/Godot operativa». Adjunta el enlace a los casos aritméticos.

## Transferencia y revisión

Completa la [tarea sin respuestas](../../../reviews/phy-005-learner-task.md) con otro ancho físico y otra escala. El revisor debe inspeccionar las fuentes fijadas, recalcular conversiones y comprobar la equivalencia entre idiomas según el [informe de revisión](../../../reviews/phy-005-review-brief.md). No hay prueba con estudiantes, aprobación de un revisor hispanohablante ni comprobación de publicación registrada. Los artefactos son una lección provisional y sus cálculos; su utilidad deberá comprobarse mediante una transferencia real sin ayuda.
