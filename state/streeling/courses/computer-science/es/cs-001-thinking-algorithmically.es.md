---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: Fundamentos de Ciencias de la Computación
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Pensar algorítmicamente

> **Departamento de Ciencias de la Computación** | Etapa: Nigredo (Principiante) | Duración: 25 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Definir qué es un algoritmo e identificar algoritmos en la vida cotidiana
- Aplicar cuatro técnicas clave de resolución de problemas: descomposición, reconocimiento de patrones, abstracción y divide y vencerás
- Distinguir entre enfoques voraces y exhaustivos
- Desarrollar intuición para la notación Big-O y por qué la eficiencia importa

---

## 1. ¿Qué es un algoritmo?

Un **algoritmo** es una secuencia finita de pasos bien definidos que toma una entrada y produce una salida. Eso es todo. No se necesitan computadoras.

Sigues algoritmos todos los días:
- Una receta de cocina es un algoritmo (entrada: ingredientes, salida: una comida)
- Las indicaciones para llegar a un lugar son un algoritmo (entrada: ubicación actual, salida: destino)
- El proceso de dar cambio en una caja registradora es un algoritmo (entrada: monto adeudado, salida: menor cantidad de monedas)

Lo que separa un algoritmo de instrucciones vagas es la **precisión**. "Cocinar hasta que esté listo" no es un algoritmo — es ambiguo. "Calentar a 180C durante 25 minutos, luego verificar la temperatura interna; si está por debajo de 74C, continuar en incrementos de 5 minutos" es un algoritmo. Cada paso es inequívoco y el proceso termina.

Tres propiedades de un algoritmo válido:
1. **Finitud** — debe terminar eventualmente
2. **Definición** — cada paso debe estar definido con precisión
3. **Efectividad** — cada paso debe ser algo que realmente se pueda llevar a cabo

### Ejercicio práctico

Escribe un algoritmo (en español sencillo, pasos numerados) para buscar una palabra en un diccionario físico. Sé lo suficientemente preciso para que alguien que nunca ha usado un diccionario pueda seguir tus pasos. Compara el tuyo con el enfoque descrito en la Sección 5 (divide y vencerás) — ¿son iguales?

---

## 2. Descomposición — Dividir problemas en partes

La habilidad de pensamiento algorítmico más poderosa es la **descomposición**: dividir un problema complejo en subproblemas más pequeños y manejables.

**Ejemplo:** Quieres organizar un concierto.

Esto es abrumador como una sola tarea. Pero descomponlo:
1. Encontrar un lugar
2. Contratar artistas
3. Fijar una fecha
4. Vender boletos
5. Conseguir equipo de sonido
6. Promover el evento

Cada subproblema sigue siendo complejo, pero ahora puedes abordarlos individualmente. Y algunos subproblemas se descomponen aún más: "Vender boletos" se convierte en elegir una plataforma, fijar precios, diseñar el boleto, abrir ventas.

La descomposición es recursiva — sigues dividiendo hasta que cada pieza es lo suficientemente simple para resolverla directamente. Así es como se construye todo sistema de software grande: no como un programa gigante, sino como miles de piezas pequeñas y componibles.

**Idea clave:** Si no puedes resolver un problema, probablemente no lo has descompuesto lo suficiente.

### Ejercicio práctico

Descompone el siguiente problema en subproblemas: "Construir un sitio web que permita a los usuarios buscar acordes de guitarra." Sigue descomponiendo hasta que cada subproblema sea algo que una persona pueda completar en un día o menos. ¿Cuántos niveles de descomposición necesitaste?

---

## 3. Reconocimiento de patrones

El **reconocimiento de patrones** es la habilidad de notar similitudes entre problemas que ya has resuelto y nuevos problemas que enfrentas.

**Ejemplo:** Ordenar una mano de cartas y ordenar una lista de nombres de estudiantes son el mismo problema — organizar elementos en orden según alguna regla de comparación. Una vez que aprendes un algoritmo de ordenamiento, puedes aplicarlo a cualquier cosa que se pueda comparar.

Los patrones aparecen en todas partes en la computación:
- Buscar en una colección (encontrar un libro en una biblioteca, encontrar un archivo en disco, encontrar una nota en el diapasón)
- Filtrar elementos que coinciden con criterios (filtro de spam, búsqueda de fotos, consulta de acordes)
- Transformar datos de un formato a otro (traducción, conversión de archivos, transposición)

Los programadores experimentados resuelven problemas más rápido no porque sean más inteligentes, sino porque reconocen patrones. Ven un nuevo problema y piensan: "Esto es esencialmente un problema de búsqueda" o "Esto es un recorrido de grafos" — y recurren a una solución conocida.

### Ejercicio práctico

Considera estos tres problemas. ¿Qué patrón comparten?
1. Encontrar la ruta más corta entre dos ciudades
2. Encontrar el menor número de cambios de acorde para ir de un acorde a otro
3. Encontrar el número mínimo de movimientos para resolver un rompecabezas

> Todos son problemas de **camino más corto** — encontrar la secuencia de pasos de costo mínimo entre un estado inicial y un estado objetivo.

---

## 4. Abstracción — Ignorar lo que no importa

La **abstracción** es el arte de eliminar detalles irrelevantes para enfocarse en lo que importa para el problema en cuestión.

Cuando dibujas un mapa, no incluyes cada árbol, cada grieta en el pavimento, cada brizna de pasto. Incluyes calles, puntos de referencia y distancias — los detalles relevantes para la navegación. Todo lo demás se abstrae.

En el pensamiento algorítmico, abstracción significa:
- Representar un problema del mundo real con un modelo simplificado
- Ignorar detalles que no afectan la solución
- Definir entradas y salidas claras

**Ejemplo:** Si quieres encontrar el camino más corto entre dos ciudades, no necesitas modelar el color de las señales de tránsito o el límite de velocidad en cada carretera (a menos que la velocidad importe para tu problema). Abstraes el mapa en un **grafo**: las ciudades son nodos, las carreteras son aristas, las distancias son pesos. Ahora puedes aplicar un algoritmo de grafos sin pensar en asfalto.

La abstracción es lo que permite que los algoritmos sean de **propósito general**. Un algoritmo de ordenamiento no le importa si está ordenando números, nombres o acordes de guitarra. Solo necesita saber cómo comparar dos elementos. Todo lo demás se abstrae.

### Ejercicio práctico

Estás construyendo un sistema para recomendar rutinas de práctica a estudiantes de guitarra. ¿Qué detalles de cada estudiante son relevantes para el algoritmo? ¿Qué detalles se pueden abstraer? Escribe dos listas: "incluir" e "ignorar."

---

## 5. Divide y vencerás

**Divide y vencerás** es una estrategia algorítmica específica:

1. **Divide** el problema en subproblemas más pequeños del mismo tipo
2. **Vence** cada subproblema (recursivamente, si es necesario)
3. **Combina** los resultados

Esto es diferente de la descomposición general. En divide y vencerás, los subproblemas tienen la **misma estructura** que el original — solo más pequeños.

**Ejemplo — Búsqueda binaria (buscar una palabra en un diccionario):**
1. Abre el diccionario en la página del medio
2. ¿Está la palabra en esta página? Si sí, listo.
3. Si la palabra viene antes de esta página alfabéticamente, repite con la primera mitad
4. Si la palabra viene después, repite con la segunda mitad
5. Sigue dividiendo a la mitad hasta encontrar la palabra

Cada paso reduce el espacio de búsqueda restante a la mitad. Un diccionario con 100,000 palabras requiere a lo sumo 17 pasos (ya que 2^17 = 131,072 > 100,000). Compara eso con empezar en la página 1 y leer cada entrada — hasta 100,000 pasos.

**Algoritmos clásicos de divide y vencerás:**
- **Búsqueda binaria** — encontrar un elemento en una colección ordenada
- **Merge sort** — ordenar dividiendo, ordenando mitades, luego fusionando
- **Quicksort** — ordenar eligiendo un pivote y particionando

### Ejercicio práctico

Tienes una lista ordenada de 1,000 canciones. Usando búsqueda binaria, ¿cuál es el número máximo de comparaciones necesarias para encontrar una canción específica? (Pista: ¿cuántas veces puedes dividir 1,000 a la mitad antes de llegar a 1?)

> log2(1000) ≈ 10. A lo sumo 10 comparaciones — comparado con 1,000 para una búsqueda lineal.

---

## 6. Enfoques voraces vs exhaustivos

Dos grandes familias de algoritmos representan diferentes filosofías:

**Los algoritmos voraces** toman la decisión localmente óptima en cada paso, esperando que esto lleve a una solución globalmente óptima.

*Ejemplo — Dar cambio con la menor cantidad de monedas:*
- Monto: 67 centavos
- Enfoque voraz: toma la moneda más grande que quepa. 50 (25+25) → 15 (10) → 5 (5) → 2 (1+1). Resultado: 25+25+10+5+1+1 = 6 monedas.
- Esto funciona para la moneda estadounidense. Pero para una moneda con piezas de 1, 3 y 4 centavos, el voraz falla: para 6 centavos, el voraz da 4+1+1 (3 monedas) pero el óptimo es 3+3 (2 monedas).

**Los algoritmos exhaustivos** verifican cada solución posible y eligen la mejor. Siempre encuentran la respuesta óptima, pero pueden ser lentos.

*Ejemplo — El viajante:*
- Visitar 10 ciudades y regresar a casa por la ruta más corta
- Exhaustivo: probar todas las ordenaciones posibles (10! = 3,628,800 rutas), medir cada una, elegir la más corta
- Esto garantiza la ruta óptima, pero es computacionalmente costoso

| Enfoque | Ventaja | Desventaja | Usar cuando |
|---------|---------|------------|-------------|
| Voraz | Rápido, simple | Puede perder la solución óptima | Lo suficientemente bueno es suficiente |
| Exhaustivo | Óptimo garantizado | Lento para problemas grandes | La corrección es crítica y la entrada es pequeña |

Muchos algoritmos del mundo real combinan ambos: usan heurísticas voraces para podar el espacio de búsqueda, luego verifican exhaustivamente los candidatos restantes.

### Ejercicio práctico

Estás empacando una maleta con objetos de diferentes pesos y valores, y la maleta tiene un límite de peso. Describe un enfoque voraz y un enfoque exhaustivo. ¿Cuál usarías si tuvieras 5 objetos? 500 objetos?

> *Voraz:* Ordena objetos por relación valor-peso, agrega objetos desde la mayor relación hasta que la maleta esté llena. *Exhaustivo:* Prueba cada combinación posible, calcula el valor total para las que están dentro del límite de peso, elige la mejor. Para 5 objetos (32 combinaciones), el exhaustivo está bien. Para 500 objetos (2^500 combinaciones), el exhaustivo es imposible — usa voraz o un algoritmo más inteligente.

---

## 7. Intuición Big-O — ¿Qué tan rápido es suficientemente rápido?

No todos los algoritmos son iguales. La **notación Big-O** describe cómo crece el tiempo de ejecución de un algoritmo a medida que aumenta el tamaño de la entrada.

No necesitas calcular Big-O con precisión ahora mismo. Necesitas **intuición** para lo que significan las categorías:

| Big-O | Nombre | Ejemplo | 1,000 elementos | 1,000,000 elementos |
|-------|--------|---------|-----------------|---------------------|
| O(1) | Constante | Buscar un elemento de un arreglo por índice | 1 paso | 1 paso |
| O(log n) | Logarítmico | Búsqueda binaria | ~10 pasos | ~20 pasos |
| O(n) | Lineal | Recorrer cada elemento una vez | 1,000 pasos | 1,000,000 pasos |
| O(n log n) | Linearítmico | Merge sort, quicksort | ~10,000 pasos | ~20,000,000 pasos |
| O(n^2) | Cuadrático | Comparar cada par | 1,000,000 pasos | 1,000,000,000,000 pasos |
| O(2^n) | Exponencial | Búsqueda exhaustiva de subconjuntos | ~10^301 pasos | Olvídalo |

La idea clave: **la diferencia entre categorías de algoritmos crece enormemente con el tamaño de la entrada.** Un algoritmo O(n) y un algoritmo O(n^2) pueden sentirse instantáneos con 10 elementos. Con un millón de elementos, uno termina en un segundo y el otro tarda días.

Por eso el pensamiento algorítmico importa. Elegir el algoritmo correcto puede ser la diferencia entre un programa que funciona y uno que nunca termina.

### Ejercicio práctico

Tienes dos algoritmos para buscar en una biblioteca musical:
- Algoritmo A: verifica cada canción una por una (O(n))
- Algoritmo B: usa un índice ordenado y búsqueda binaria (O(log n))

Para una biblioteca de 10 millones de canciones, ¿aproximadamente cuántos pasos toma cada uno?
> A: 10,000,000 pasos. B: log2(10,000,000) ≈ 23 pasos. El Algoritmo B es más de 400,000 veces más rápido.

---

## Términos clave

| Término | Definición |
|---------|-----------|
| **Algoritmo** | Una secuencia finita de pasos bien definidos que transforma entrada en salida |
| **Descomposición** | Dividir un problema complejo en subproblemas más pequeños y manejables |
| **Reconocimiento de patrones** | Identificar similitudes entre un problema nuevo y problemas resueltos previamente |
| **Abstracción** | Eliminar detalles irrelevantes para enfocarse en lo que importa para la solución |
| **Divide y vencerás** | Dividir un problema en instancias más pequeñas del mismo problema, resolver recursivamente |
| **Algoritmo voraz** | Tomar la decisión localmente óptima en cada paso |
| **Algoritmo exhaustivo** | Verificar cada solución posible para garantizar encontrar la mejor |
| **Notación Big-O** | Una clasificación de la eficiencia de algoritmos por cómo crece el tiempo de ejecución con el tamaño de la entrada |

---

## Autoevaluación

**1. ¿Qué tres propiedades debe tener un algoritmo válido?**
> Finitud (termina), definición (cada paso es inequívoco) y efectividad (cada paso puede realizarse de hecho).

**2. Necesitas buscar un nombre en una lista desordenada de 1,000 nombres. ¿Cuál es el mejor Big-O que puedes lograr?**
> O(n) — búsqueda lineal. Sin ordenar o indexar, debes verificar potencialmente cada elemento. Si la lista estuviera ordenada, podrías usar búsqueda binaria para O(log n).

**3. Un algoritmo voraz para dar cambio da la respuesta incorrecta para monedas de 1, 3 y 4 centavos al hacer 6 centavos. ¿Por qué?**
> El enfoque voraz elige la moneda más grande primero (4), luego necesita 1+1 para el resto (3 monedas en total). Pero 3+3 usa solo 2 monedas. El voraz falla porque la decisión localmente óptima (la moneda más grande) no lleva a la solución globalmente óptima.

**4. ¿Por qué O(n log n) se considera eficiente para ordenamiento?**
> Se ha demostrado matemáticamente que ningún algoritmo de ordenamiento basado en comparaciones puede hacerlo mejor que O(n log n) en el peor caso. Merge sort y quicksort alcanzan este límite, haciéndolos óptimos entre los ordenamientos por comparación.

**Criterio de aprobación:** Descomponer un problema dado en subproblemas, identificar qué enfoque algorítmico (voraz, exhaustivo, divide y vencerás) se ajusta a un escenario dado, y explicar las diferencias de Big-O usando ejemplos concretos.

---

## Base de investigación

- El pensamiento algorítmico (descomposición, reconocimiento de patrones, abstracción) es reconocido como una habilidad central del pensamiento computacional
- Divide y vencerás, voraz y búsqueda exhaustiva son los tres paradigmas algorítmicos fundamentales
- La notación Big-O proporciona una medida de eficiencia independiente del hardware
- Enseñar intuición algorítmica antes del análisis formal mejora la transferencia en resolución de problemas
- Fuentes: Consenso en educación en ciencias de la computación, currículo del Departamento de Ciencias de la Computación de Streeling
- Estado de creencia: T(0.91) F(0.02) U(0.05) C(0.02)
