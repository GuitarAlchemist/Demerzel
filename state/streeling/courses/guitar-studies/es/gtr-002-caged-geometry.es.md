---
module_id: gtr-002-caged-geometry
department: guitar-studies
course: "Disposicion del diapason y sistema CAGED"
level: intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "45 minutes"
produced_by: seldon-research-cycle
research_cycle: guitar-studies-2026-03-23-001
version: "1.0.0"
---

# Geometria CAGED: por que cinco formas gobiernan el diapason

> **Departamento de Estudios de Guitarra** | Nivel: Intermedio | Duracion: 45 minutos

## Objetivos
- Entender por que exactamente 5 formas de acordes abiertos cubren todo el diapason
- Derivar el sistema CAGED a partir de la observacion de la estructura intervalica de los acordes abiertos
- Demostrar que CAGED es una consecuencia matematica de la afinacion estandar, no un sistema arbitrario
- Aplicar formas de acordes con cejilla movibles para navegar cualquier acorde mayor a lo largo del mastil

---

## 1. Las cinco formas abiertas

Todo guitarrista aprende estos cinco acordes mayores abiertos al principio. Cada uno tiene una huella geometrica distinta:

### Forma C (Do)
```
x 3 2 0 1 0    Cuerdas: 5-4-3-2-1
  T 3 5 T 3    Intervalos: Tonica-3M-5J-Tonica-3M
```

### Forma A (La)
```
x 0 2 2 2 0    Cuerdas: 5-4-3-2-1
  T 5 T 3 5    Intervalos: Tonica-5J-Tonica-3M-5J
```

### Forma G (Sol)
```
3 2 0 0 0 3    Cuerdas: 6-5-4-3-2-1
T 3 5 T 3 T    Intervalos: Tonica-3M-5J-Tonica-3M-Tonica
```

### Forma E (Mi)
```
0 2 2 1 0 0    Cuerdas: 6-5-4-3-2-1
T 5 T 3 5 T    Intervalos: Tonica-5J-Tonica-3M-5J-Tonica
```

### Forma D (Re)
```
x x 0 2 3 2    Cuerdas: 4-3-2-1
  T 5 T 3      Intervalos: Tonica-5J-Tonica-3M
```

**Observacion clave:** Cada forma contiene solo tres clases de notas: Tonica, Tercera mayor y Quinta justa. Las diferencias estan en la *disposicion* -- en que octava aparece cada nota y que cuerdas las llevan.

---

## 2. La prueba del deslizamiento

Aqui esta la idea central: si mantienes la *geometria de los dedos* de cualquier acorde abierto pero lo deslizas por el mastil, las relaciones intervalicas se preservan. El dedo de la cejilla reemplaza a la cejuela.

**Forma E en el traste 0:** Mi mayor (abierto)
**Forma E en el traste 1:** Fa mayor (acorde con cejilla de Fa)
**Forma E en el traste 3:** Sol mayor
**Forma E en el traste 5:** La mayor

Esto funciona porque el intervalo entre cada par de cuerdas adyacentes esta fijado por la afinacion. Mover todos los dedos el mismo numero de trastes transpone cada nota por el mismo intervalo.

Esto no es un truco pedagogico -- es un *teorema geometrico* sobre el diapason.

---

## 3. Por que exactamente cinco formas?

La afinacion estandar (Mi-La-Re-Sol-Si-Mi) crea un patron de intervalos especifico entre las cuerdas:

```
Cuerda:    6    5    4    3    2    1
Nota:      Mi   La   Re   Sol  Si   Mi
Intervalo:   4J   4J   4J   3M   4J
```

El patron 4ta-4ta-4ta-3ra-4ta crea exactamente **cinco regiones distintas** donde se pueden formar acordes abiertos. Cada forma ocupa una extension diferente de trastes y cuerdas.

Las cinco formas se entrelazan como piezas de rompecabezas:

```
Traste: 0    3    5    7    8    10   12
        |--E--|--D--|--C--|--A--|--G--|--E--|
        (formas mostradas para la tonalidad de Mi mayor)
```

Recorrer el orden C-A-G-E-D te lleva a lo largo del mastil, con la tonica de cada forma conectando con la nota mas alta de la siguiente. Esta es la **secuencia CAGED** -- un camino ciclico a traves de las cinco regiones de disposicion.

---

## 4. Es CAGED el unico orden?

Las cinco formas forman un **ciclo**, asi que cualquier punto de partida da una secuencia valida:

- **CAGED** (la mas comun)
- **AGEDC** (empezando desde A)
- **GEDCA** (empezando desde G)
- **EDCAG** (empezando desde E)
- **DCAGE** (empezando desde D)

El nombre "CAGED" es una conveniencia mnemonica. El ciclo subyacente de 5 formas esta determinado estructuralmente. Todos los ordenes describen la misma cobertura del diapason.

---

## 5. Dependencia de la afinacion

CAGED es especifico de la afinacion estandar. Cambia la afinacion y las formas cambian:

- **Afinacion en todas cuartas** (Mi-La-Re-Sol-Do-Fa): La irregularidad de la 3M entre las cuerdas 3-2 desaparece. Las formas de acordes se vuelven mas uniformes pero diferentes de CAGED.
- **Afinacion abierta en Sol** (Re-Sol-Re-Sol-Si-Re): Las cuerdas al aire ya forman un acorde, creando un sistema de formas completamente diferente.
- **Drop D** (Re-La-Re-Sol-Si-Mi): Solo cambia la cuerda mas grave, preservando la mayoria de las formas CAGED pero alterando las formas E y G en las cuerdas graves.

Esto demuestra que CAGED se *deriva de* la geometria de la afinacion estandar, no se le impone.

---

## Ejercicio practico

### Ejercicio 1: Identificacion de formas
Toca un acorde de Do mayor usando las cinco formas CAGED. Comienza con la forma abierta de Do, luego encuentra la forma A (traste 3), forma G (traste 5), forma E (traste 8) y forma D (traste 10).

### Ejercicio 2: Conexion de formas
Elige dos formas CAGED adyacentes cualesquiera. Encuentra las notas que comparten en las mismas cuerdas. Estas notas compartidas son tus "puntos de pivote" para moverte entre formas.

### Ejercicio 3: Una cuerda, cinco formas
En la cuerda 2 solamente, toca la nota Do en cada una de las cinco posiciones CAGED. Observa como cada forma coloca Do en un traste diferente de esa cuerda.

---

## Puntos clave
- El sistema CAGED es **descubierto, no inventado** -- es una consecuencia estructural de la geometria de la afinacion estandar
- Exactamente **5 formas** cubren el diapason debido al patron de afinacion 4ta-4ta-4ta-3ra-4ta
- Cada forma preserva su estructura intervalica cuando se pone cejilla y se mueve -- esto es un teorema geometrico, no un atajo pedagogico
- El nombre "CAGED" es uno de 5 ordenes ciclicos equivalentes
- Diferentes afinaciones producen diferentes sistemas de formas, confirmando que CAGED se deriva de la afinacion

## Lecturas complementarias
- [GTR-001: El mapa del diapason](gtr-001-the-fretboard-map.es.md) -- prerrequisito
- Departamento de Musica: Sistemas de afinacion y temperamento
- Departamento de Fisica: Acustica de la vibracion de cuerdas y armonicos
- Departamento de Matematicas: Teoria de grupos y simetria del diapason

---
*Producido por el Ciclo de Investigacion Seldon guitar-studies-2026-03-23-001 el 2026-03-23.*
*Pregunta de investigacion: Las voicings comunes de acordes abiertos comparten patrones estructurales que predicen sus formas movibles con cejilla?*
*Creencia: T (confianza: 0.85)*
