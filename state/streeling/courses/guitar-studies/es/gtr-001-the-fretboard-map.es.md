---
module_id: gtr-001-the-fretboard-map
department: guitar-studies
course: Fundamentos de guitarra
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "30 minutes"
produced_by: guitar-studies
version: "1.0.0"
---

# El mapa del diapason

> **Departamento de Estudios de Guitarra** | Etapa: Nigredo (Principiante) | Duracion: 30 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Nombrar las seis cuerdas al aire y recordarlas con un mnemonico
- Encontrar cualquier nota natural en cualquier cuerda usando el mapeo de traste a nota
- Identificar el patron de octavas que se repite a lo largo del diapason
- Describir las cinco formas del sistema CAGED y por que importan
- Navegar el diapason con confianza en lugar de memorizar posiciones a ciegas

---

## 1. Las seis cuerdas al aire

La guitarra tiene seis cuerdas, afinadas desde el tono mas grave (cuerda mas gruesa) hasta el mas agudo (cuerda mas delgada):

| Numero de cuerda | Nota | Descripcion |
|-----------------|------|-------------|
| 6 | Mi | Mi grave — cuerda mas gruesa |
| 5 | La | |
| 4 | Re | |
| 3 | Sol | |
| 2 | Si | |
| 1 | Mi | Mi agudo — cuerda mas delgada |

**Mnemonico:** **Mi** **La**do **Re**sulta **Sol**o **Si** **Mi**ras

Nota que las cuerdas 6 y 1 son ambas Mi, con dos octavas de diferencia. Esta simetria es una de las caracteristicas mas utiles de la guitarra — los patrones que funcionan en la cuerda Mi grave tambien funcionan en la cuerda Mi agudo.

### Ejercicio practico

Sin mirar una referencia, di los nombres de las cuerdas en voz alta de la 6 a la 1, luego de la 1 a la 6. Repite hasta que puedas hacerlo en menos de 3 segundos en cada direccion. Luego pulsa cada cuerda al aire en tu guitarra, diciendo su nombre mientras suena.

---

## 2. Trastes y semitonos

Cada traste en la guitarra eleva el tono exactamente **un semitono** (medio tono). Esto significa:

- Traste 0 (cuerda al aire) a traste 1 = un semitono
- Traste 1 a traste 2 = un semitono
- Traste 12 = exactamente una octava por encima de la cuerda al aire (12 semitonos = 1 octava)

La escala cromatica (las 12 notas) en orden:

```
La → La#/Sib → Si → Do → Do#/Reb → Re → Re#/Mib → Mi → Fa → Fa#/Solb → Sol → Sol#/Lab → (vuelve a La)
```

Dos excepciones importantes donde **no hay sostenido/bemol entre notas naturales adyacentes**:
- **Si a Do** — un semitono, no hay Si#
- **Mi a Fa** — un semitono, no hay Mi#

Todo lo demas tiene un sostenido/bemol entre las notas naturales (por ejemplo, La a Si tiene La#/Sib en medio — son dos semitonos).

---

## 3. Notas naturales en cada cuerda

Usando la secuencia cromatica y la afinacion de las cuerdas al aire, aqui estan todas las notas naturales en cada cuerda hasta el traste 12:

**Cuerda Mi grave (6ta):**
```
Traste: 0  1  2  3  4  5  6  7  8  9  10 11 12
Nota:   Mi Fa .  Sol .  La .  Si Do .  Re .  Mi
```

**Cuerda La (5ta):**
```
Traste: 0  1  2  3  4  5  6  7  8  9  10 11 12
Nota:   La .  Si Do .  Re .  Mi Fa .  Sol .  La
```

**Cuerda Re (4ta):**
```
Traste: 0  1  2  3  4  5  6  7  8  9  10 11 12
Nota:   Re .  Mi Fa .  Sol .  La .  Si Do .  Re
```

**Cuerda Sol (3ra):**
```
Traste: 0  1  2  3  4  5  6  7  8  9  10 11 12
Nota:   Sol .  La .  Si Do .  Re .  Mi Fa .  Sol
```

**Cuerda Si (2da):**
```
Traste: 0  1  2  3  4  5  6  7  8  9  10 11 12
Nota:   Si Do .  Re .  Mi Fa .  Sol .  La .  Si
```

**Cuerda Mi agudo (1ra):**
```
Traste: 0  1  2  3  4  5  6  7  8  9  10 11 12
Nota:   Mi Fa .  Sol .  La .  Si Do .  Re .  Mi
```

Los puntos (`.`) representan sostenidos/bemoles. Nota que las cuerdas 6 y 1 son identicas — las mismas notas en los mismos trastes.

### Ejercicio practico

Elige una cuerda. Comienza en la nota al aire y di cada nota natural en voz alta mientras tocas subiendo traste por traste hasta el traste 12. Salta los sostenidos/bemoles por ahora — solo encuentra las notas naturales. Haz esto para las seis cuerdas durante una semana, una cuerda por dia (dos cuerdas comparten el mismo patron).

---

## 4. El patron de octavas

La misma nota se repite en ubicaciones predecibles a lo largo del diapason. Conocer el **patron de octavas** significa que una vez que encuentras una nota en un lugar, puedes encontrarla instantaneamente en todas partes.

Relaciones clave de octavas:

| Desde cuerda | Movimiento | Hacia cuerda | Cambio de traste |
|-------------|------------|-------------|-----------------|
| 6ta (Mi) | +2 cuerdas, +2 trastes | 4ta (Re) | +2 |
| 5ta (La) | +2 cuerdas, +2 trastes | 3ra (Sol) | +2 |
| 4ta (Re) | +2 cuerdas, +3 trastes | 2da (Si) | +3 |
| 3ra (Sol) | +2 cuerdas, +3 trastes | 1ra (Mi) | +3 |
| 6ta (Mi) | mismo traste | 1ra (Mi) | 0 |

El cambio de +2 a +3 trastes ocurre por la cuerda Si. La guitarra esta afinada en cuartas justas (5 semitonos de diferencia) entre todas las cuerdas adyacentes **excepto** Sol a Si, que es una tercera mayor (4 semitonos). Esa diferencia de un traste se propaga por cada patron en el diapason.

**Ejemplo:** Encuentra todas las notas Do.
- 6ta cuerda, traste 8
- 4ta cuerda, traste 10 (8 + 2)
- 2da cuerda, traste 13 (10 + 3) — o traste 1
- 5ta cuerda, traste 3
- 3ra cuerda, traste 5 (3 + 2)
- 1ra cuerda, traste 8 (5 + 3) — mismo traste que la 6ta cuerda

### Ejercicio practico

Elige cualquier nota — digamos, Sol. Encuentrala en la 6ta cuerda (traste 3). Luego usa el patron de octavas para encontrar Sol en cada otra cuerda sin contar trastes desde la cuerda al aire. Verifica tu respuesta contando desde la nota al aire. Repite con tres notas diferentes.

---

## 5. El sistema CAGED — Cinco ventanas al diapason

El sistema CAGED es un marco que divide el diapason en cinco zonas superpuestas, cada una nombrada por una forma de acorde abierto: **C, A, G, E, D** (Do, La, Sol, Mi, Re).

La idea central: **cada acorde y escala se puede tocar en cinco posiciones diferentes del mastil, y cada posicion corresponde a una de estas cinco formas de acorde abierto.**

Asi es como las cinco formas se conectan, usando Do mayor como ejemplo:

| Forma | Posicion (traste de la tonica) | Basada en |
|-------|-------------------------------|-----------|
| Forma C | Posicion abierta (traste 0-3) | Acorde abierto de Do |
| Forma A | Area del traste 3 | Forma del acorde abierto de La, con cejilla |
| Forma G | Area del traste 5 | Forma del acorde abierto de Sol, desplazada |
| Forma E | Area del traste 8 | Forma del acorde abierto de Mi, con cejilla |
| Forma D | Area del traste 10 | Forma del acorde abierto de Re, desplazada |

Las formas se repiten infinitamente a lo largo del mastil: C-A-G-E-D-C-A-G-E-D...

**Por que importa:** En lugar de ver el diapason como 6 cuerdas por 20+ trastes de caos, ves cinco formas familiares que cubren todo el mastil. Cada acorde que ya conoces en posicion abierta es una plantilla para tocar ese acorde en cualquier lugar.

En esta etapa, solo conoce que el concepto existe. Aprenderas cada forma en detalle en lecciones posteriores. Por ahora, la conclusion es: **el diapason no es aleatorio. Son cinco patrones superpuestos.**

### Ejercicio practico

Toca un acorde abierto de Mi mayor (dedos en los trastes 1 y 2). Ahora toca un acorde con cejilla en el traste 5 usando la misma forma de Mi — eso es un acorde de La mayor. Muevete al traste 7 — Si mayor. Estas usando la forma E del CAGED para tocar acordes mayores en cualquier parte del mastil. Intenta lo mismo con la forma del acorde abierto de La mayor, poniendo la cejilla en diferentes trastes.

---

## 6. Integrando todo — Una estrategia para el diapason

No intentes memorizar todas las notas de una vez. En su lugar, usa esta estrategia por capas:

1. **Conoce tus cuerdas al aire** de memoria (Mi-La-Re-Sol-Si-Mi)
2. **Aprende las notas naturales en las cuerdas 6 y 5** primero — estas son tus autopistas de notas fundamentales para acordes y escalas
3. **Usa el patron de octavas** para encontrar las mismas notas en otras cuerdas
4. **Piensa en formas CAGED** — cuando aprendas un acorde o escala en una posicion, preguntate inmediatamente "en que forma estoy?" y encuentra las formas adyacentes

Con semanas y meses, el diapason deja de ser una cuadricula misteriosa y se convierte en un mapa que puedes leer con fluidez.

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| **Cuerda al aire** | Una cuerda tocada sin presionar ningun traste |
| **Semitono** | El intervalo mas pequeno en la musica occidental — un traste en la guitarra |
| **Escala cromatica** | Las 12 notas en secuencia, cada una separada por un semitono |
| **Octava** | La misma nota en un tono mas agudo o mas grave, a 12 semitonos de distancia |
| **Patron de octavas** | Las ubicaciones predecibles del diapason donde la misma nota se repite |
| **Sistema CAGED** | Marco que divide el diapason en cinco zonas superpuestas basadas en formas de acordes abiertos |
| **Acorde con cejilla** | Un acorde donde un dedo presiona a lo largo de multiples cuerdas, reemplazando la cejuela |

---

## Autoevaluacion

**1. Cuales son las seis notas de las cuerdas al aire de la mas grave a la mas aguda?**
> Mi - La - Re - Sol - Si - Mi

**2. Por que el cambio de traste es +3 en lugar de +2 cuando cruzas de la cuerda Sol a la cuerda Si?**
> El intervalo entre Sol y Si es una tercera mayor (4 semitonos) en lugar de una cuarta justa (5 semitonos) como todos los demas pares de cuerdas adyacentes. El semitono faltante agrega un traste extra al desplazamiento de octava.

**3. Encuentra la nota en el traste 5 de la cuerda La. Luego encuentra su octava usando el patron.**
> Cuerda La traste 5 = Re. Octava: cuerda Sol traste 7 (5 + 2). Otra octava: cuerda Si traste 10 (7 + 3).

**4. Que significa CAGED y para que se usa?**
> C-A-G-E-D son cinco formas de acordes abiertos que cubren todo el diapason. Proporcionan cinco posiciones superpuestas para tocar cualquier acorde o escala en cualquier parte del mastil.

**Criterio de aprobacion:** Nombrar las seis cuerdas al aire de memoria, localizar cualquier nota natural dada en al menos dos cuerdas diferentes usando el patron de octavas, y explicar el proposito del sistema CAGED.

---

## Base de investigacion

- Los nombres de las cuerdas y la afinacion estandar (EADGBE / Mi-La-Re-Sol-Si-Mi) son universales en la pedagogia moderna de guitarra
- El sistema CAGED es el marco de navegacion del diapason mas ampliamente ensenado
- Los patrones de octava aprovechan la afinacion consistente basada en cuartas de la guitarra con la excepcion de la cuerda Si
- Aprender las notas fundamentales en las cuerdas 5 y 6 primero acelera la adquisicion del vocabulario de acordes
- Fuentes: Consenso en pedagogia de guitarra, curriculo del Departamento de Estudios de Guitarra de Streeling
- Estado de creencia: T(0.92) F(0.01) U(0.05) C(0.02)
