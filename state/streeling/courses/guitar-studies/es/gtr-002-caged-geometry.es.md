---
module_id: gtr-002-caged-geometry
department: guitar-studies
course: "Disposición del diapasón y sistema CAGED"
level: intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "45 minutes"
produced_by: seldon-research-cycle
research_cycle: guitar-studies-2026-03-23-001
version: "1.0.0"
---

# Geometría CAGED: por qué cinco formas gobiernan el diapasón

> **Departamento de Estudios de Guitarra** | Nivel: Intermedio | Duración: 45 minutos

## Objetivos
- Entender por qué exactamente 5 formas de acordes abiertos cubren todo el diapasón
- Derivar el sistema CAGED a partir de la observación de la estructura interválica de los acordes abiertos
- Demostrar que CAGED es una consecuencia matemática de la afinación estándar, no un sistema arbitrario
- Aplicar formas de acordes con cejilla movibles para navegar cualquier acorde mayor a lo largo del mástil

---

## 1. Las cinco formas abiertas

Todo guitarrista aprende estos cinco acordes mayores abiertos al principio. Cada uno tiene una huella geométrica distinta:

Los diagramas se leen de la cuerda 6 (Mi grave) a la cuerda 1 (Mi agudo); `x` marca una cuerda que no se toca.

### Forma C (Do)
```
x 3 2 0 1 0    Cuerdas: 6-5-4-3-2-1
  T 3 5 T 3    Intervalos: Tónica-3M-5J-Tónica-3M
```

### Forma A (La)
```
x 0 2 2 2 0    Cuerdas: 6-5-4-3-2-1
  T 5 T 3 5    Intervalos: Tónica-5J-Tónica-3M-5J
```

### Forma G (Sol)
```
3 2 0 0 0 3    Cuerdas: 6-5-4-3-2-1
T 3 5 T 3 T    Intervalos: Tónica-3M-5J-Tónica-3M-Tónica
```

### Forma E (Mi)
```
0 2 2 1 0 0    Cuerdas: 6-5-4-3-2-1
T 5 T 3 5 T    Intervalos: Tónica-5J-Tónica-3M-5J-Tónica
```

### Forma D (Re)
```
x x 0 2 3 2    Cuerdas: 6-5-4-3-2-1
    T 5 T 3    Intervalos: Tónica-5J-Tónica-3M
```

**Observación clave:** Cada forma contiene solo tres clases de notas: Tónica, Tercera mayor y Quinta justa. Las diferencias están en la *disposición* -- en qué octava aparece cada nota y qué cuerdas las llevan.

---

## 2. La prueba del deslizamiento

Aquí está la idea central: si mantienes la *geometría de los dedos* de cualquier acorde abierto pero lo deslizas por el mástil, las relaciones interválicas se preservan. El dedo de la cejilla reemplaza a la cejuela.

**Forma E en el traste 0:** Mi mayor (abierto)
**Forma E en el traste 1:** Fa mayor (acorde con cejilla de Fa)
**Forma E en el traste 3:** Sol mayor
**Forma E en el traste 5:** La mayor

Esto funciona porque el intervalo entre cada par de cuerdas adyacentes está fijado por la afinación. Mover todos los dedos el mismo número de trastes transpone cada nota por el mismo intervalo.

Esto no es un truco pedagógico -- es un *teorema geométrico* sobre el diapasón.

---

## 3. ¿Por qué exactamente cinco formas?

La afinación estándar (Mi-La-Re-Sol-Si-Mi) crea un patrón de intervalos específico entre las cuerdas:

```
Cuerda:    6    5    4    3    2    1
Nota:      Mi   La   Re   Sol  Si   Mi
Intervalo:   4J   4J   4J   3M   4J
```

El patrón 4ta-4ta-4ta-3ra-4ta crea exactamente **cinco regiones distintas** donde se pueden formar acordes abiertos. Cada forma ocupa una extensión diferente de trastes y cuerdas.

Las cinco formas se entrelazan como piezas de rompecabezas:

```
Traste: 0    3    5    7    8    10   12
        |--E--|--D--|--C--|--A--|--G--|--E--|
        (formas mostradas para la tonalidad de Mi mayor)
```

Recorrer el orden C-A-G-E-D te lleva a lo largo del mástil, con la tónica de cada forma conectando con la nota más alta de la siguiente. Esta es la **secuencia CAGED** -- un camino cíclico a través de las cinco regiones de disposición.

---

## 4. ¿Es CAGED el único orden?

Las cinco formas forman un **ciclo**, así que cualquier punto de partida da una secuencia válida:

- **CAGED** (la más común)
- **AGEDC** (empezando desde A)
- **GEDCA** (empezando desde G)
- **EDCAG** (empezando desde E)
- **DCAGE** (empezando desde D)

El nombre "CAGED" es una conveniencia mnemónica. El ciclo subyacente de 5 formas está determinado estructuralmente. Todos los órdenes describen la misma cobertura del diapasón.

---

## 5. Dependencia de la afinación

CAGED es específico de la afinación estándar. Cambia la afinación y las formas cambian:

- **Afinación en todas cuartas** (Mi-La-Re-Sol-Do-Fa): La irregularidad de la 3M entre las cuerdas 3-2 desaparece. Las formas de acordes se vuelven más uniformes pero diferentes de CAGED.
- **Afinación abierta en Sol** (Re-Sol-Re-Sol-Si-Re): Las cuerdas al aire ya forman un acorde, creando un sistema de formas completamente diferente.
- **Drop D** (Re-La-Re-Sol-Si-Mi): Solo cambia la cuerda más grave, preservando la mayoría de las formas CAGED pero alterando las formas E y G en las cuerdas graves.

Esto demuestra que CAGED se *deriva de* la geometría de la afinación estándar, no se le impone.

---

## Ejercicio práctico

### Ejercicio 1: Identificación de formas
Toca un acorde de Do mayor usando las cinco formas CAGED. Comienza con la forma abierta de Do, luego encuentra la forma A (traste 3), forma G (traste 5), forma E (traste 8) y forma D (traste 10).

### Ejercicio 2: Conexión de formas
Elige dos formas CAGED adyacentes cualesquiera. Encuentra las notas que comparten en las mismas cuerdas. Estas notas compartidas son tus "puntos de pivote" para moverte entre formas.

### Ejercicio 3: Una cuerda, cinco formas
En la cuerda 2 solamente, toca la nota Do en cada una de las cinco posiciones CAGED. Observa cómo cada forma coloca Do en un traste diferente de esa cuerda.

---

## Puntos clave
- El sistema CAGED es **descubierto, no inventado** -- es una consecuencia estructural de la geometría de la afinación estándar
- Exactamente **5 formas** cubren el diapasón debido al patrón de afinación 4ta-4ta-4ta-3ra-4ta
- Cada forma preserva su estructura interválica cuando se pone cejilla y se mueve -- esto es un teorema geométrico, no un atajo pedagógico
- El nombre "CAGED" es uno de 5 órdenes cíclicos equivalentes
- Diferentes afinaciones producen diferentes sistemas de formas, confirmando que CAGED se deriva de la afinación

## Lecturas complementarias
- [GTR-001: El mapa del diapasón](gtr-001-the-fretboard-map.es.md) -- prerrequisito
- Departamento de Música: Sistemas de afinación y temperamento
- Departamento de Física: Acústica de la vibración de cuerdas y armónicos
- Departamento de Matemáticas: Teoría de grupos y simetría del diapasón

---
*Producido por el Ciclo de Investigación Seldon guitar-studies-2026-03-23-001 el 2026-03-23.*
*Pregunta de investigación: ¿Las voicings comunes de acordes abiertos comparten patrones estructurales que predicen sus formas movibles con cejilla?*
*Creencia: T (confianza: 0.85)*
