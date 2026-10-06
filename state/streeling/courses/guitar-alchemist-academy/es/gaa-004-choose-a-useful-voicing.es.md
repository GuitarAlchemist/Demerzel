---
module_id: gaa-004-choose-a-useful-voicing
department: guitar-alchemist-academy
course: Elegir y tocar una disposición útil a partir de una respuesta de GA
level: beginner
alchemical_stage: nigredo
prerequisites: ["gaa-001-your-first-chord", "gtr-001-the-fretboard-map"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-alchemist-academy-2026-10-05-004
version: "0.1.0"
---

# Elegir y tocar una disposición útil a partir de una respuesta de GA

> **Guitar Alchemist Academy** | Principiante | 35 minutos | Borrador: pendientes la revisión musical y lingüística

## Objetivos

Aprenderá a leer una posición sin tocar una cuerda silenciada, comparar dos
formas de tocar el mismo acorde, usar el orden de dificultad de GA como punto
de partida y comprobar el resultado con las manos y el oído.

## 1. Descifrar una posición antes de juzgarla

Pida **do mayor**. El [material fijo](../../../fixtures/guitar-studies/gtr-003/README.md)
contiene tres posiciones cuyas notas se comprobaron. **No son resultados
capturados de GA**. Los diagramas van de la cuerda 6 (mi grave) a la 1 (mi
agudo). `x` indica que no se toca esa cuerda; `0`, que suena al aire.

```text
Cuerda:          6  5  4  3  2  1
Do abierto:      x  3  2  0  1  0
Do forma de la:  x  3  5  5  5  3
Do forma de mi:  8 10 10  9  8  8
```

Para el do abierto, toque solo las cuerdas 5 a 1. Sus notas son do, mi,
sol, do, mi. Las tres *clases de altura* do, mi y sol definen do mayor.
Repetir do o mi en otra octava cambia la disposición, pero no la identidad
básica del acorde. Antes de convertir un arreglo `Frets` de GA a este
diagrama, compruebe qué extremo corresponde al mi grave. El material
declara su propio orden, de grave a agudo; no demuestra el orden del servicio.

### Ejercicio 1

En `x 3 2 0 1 0`, ¿qué cuerda queda muda, cuáles suenan al aire y cuáles
son las tres notas distintas del acorde?

> **Respuesta:** No toque la cuerda 6. Las cuerdas 3 y 1 suenan al aire.
> Las notas son do, mi, sol, do, mi; las distintas son do, mi y sol.

## 2. Tomar el orden de GA como propuesta

En el [commit GA `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-server/GaApi/Services/VoicingFilterService.cs),
`GetVoicingsForChordAsync("C")` genera posiciones con arreglos de trastes,
etiquetas y puntuaciones de dificultad e información sobre cejillas. Después
las ordena por `DifficultyScore` ascendente. Las [pruebas del servicio](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Apps/GaApi.Tests/Services/VoicingFilterServiceTests.cs)
comprueban que C devuelve candidatos y que sus puntuaciones están ordenadas.
No garantizan que el primero sea cómodo para todas las personas ni que sea
una de las tres posiciones didácticas anteriores.

En una compilación de esa revisión de GA, anote los dos primeros resultados
de una consulta `C`: trastes, puntuación, cuerdas al aire e indicador de
cejilla. Si la interfaz no muestra un dato, escriba «no se muestra» en vez
de deducirlo del dibujo. `-1` significa cuerda silenciada; `0`, cuerda al
aire. Guarde la consulta, la revisión y la afinación para poder repetir la
comparación.

Si GA no está disponible, compare las posiciones fijas y anote « consulta
al servicio no ejecutada ». Las puntuaciones 3 y 5 del ejercicio siguiente
son hipotéticas: no las atribuya a esas posiciones ni las presente como
resultados de GA.

### Ejercicio 2

Con `noOpenStrings: true`, ¿puede esperar todavía la posición de do abierto?
Si dos resultados de GA tienen puntuaciones 3 y 5, ¿cuál probaría primero y
qué **no demuestra** esa puntuación?

> **Respuesta:** No. El servicio elimina posiciones que contienen el traste
> `0` cuando se activa `noOpenStrings`. Pruebe primero la de puntuación 3
> como propuesta inicial. El número no mide el tamaño de su mano, su
> técnica, el dolor ni el sonido de su instrumento.

## 3. Comprobar en la guitarra

Empiece con el do abierto. Ponga un dedo en la cuerda 5, traste 3; otro en
la cuerda 4, traste 2; y otro en la cuerda 2, traste 1. Pulse por separado
las cuerdas 5, 4, 3, 2 y 1. Si una nota trastea, acerque el dedo al traste
sin apretar más de lo necesario. Después rasguee solo esas cinco cuerdas.
No fuerce un estiramiento y deténgase si siente dolor.

Luego pruebe la forma de la: silencie la cuerda 6, toque las cuerdas 5 y
1 en el traste 3 y las cuerdas 4, 3 y 2 en el traste 5. Quizá necesite una
media cejilla u otra digitación. Compare la claridad de las notas y el
esfuerzo. Si hoy resulta demasiado difícil, anótelo y quédese con el do
abierto. Una disposición es útil si sirve a la música y al intérprete, no
solo porque la devuelva un algoritmo.

### Ejercicio 3

Ambas formas contienen do, mi y sol. Dé una razón musical y otra física
para elegir el do abierto en una canción lenta. ¿Cuándo elegiría la otra?

> **Ejemplo de respuesta:** Las cuerdas al aire del do abierto pueden
> resonar y esta forma requiere menos esfuerzo de mi mano hoy. Podría usar
> la otra si el acorde siguiente queda cerca del traste 3, cuando logre
> hacer sonar claramente todas sus notas. Otra persona puede decidir de
> otra manera después de probarlas.

## 4. Ajustar la conclusión a las pruebas

Separe lo que el servicio **calcula** de lo que usted **observa**. Una nota
de práctica puede seguir esta cadena: `consulta C + revisión GA → dos
posiciones y puntuaciones → posición tocada → notas claras o que trastean →
esfuerzo y contexto musical → elección`. El programa propone; la persona
comprueba. Si no ejecutó GA o no tocó la posición, indique qué falta probar.

### Ejercicio 4

Un agente afirma: «El primer do que propone GA es el más fácil para todo
el mundo». Reescriba la frase respetando las pruebas del servicio.

> **Respuesta:** «En esta consulta, el primer resultado tiene la puntuación
> de dificultad calculada más baja entre las posiciones devueltas. Una
> persona todavía debe comprobar la afinación, las notas, la digitación y
> la comodidad».

## Ideas clave

- Un arreglo de trastes indica qué hacer con cada cuerda; `-1` y `0` no
  significan lo mismo.
- Varias disposiciones pueden contener las mismas notas y, aun así, sentirse
  y sonar diferentes.
- El orden de GA ofrece una primera opción para probar. Quien toca decide
  después de escuchar y sentir el resultado.

## Pruebas y límites

El [material y el registro de pruebas](../../../fixtures/guitar-studies/gtr-003/README.md)
identifican la revisión GA y distinguen las posiciones didácticas de las
salidas del servicio. Pasaron las pruebas focalizadas de un binario ya
compilado, pero faltan una respuesta GA capturada, una prueba con principiantes
y revisión musical y lingüística. Este borrador aún no es un curso verificado.
