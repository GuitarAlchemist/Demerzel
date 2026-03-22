---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: Fundamentos de Ciencias de la Computacion
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Pensar algoritmicamente

> **Departamento de Ciencias de la Computacion** | Etapa: Nigredo (Principiante) | Duracion: 25 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Definir que es un algoritmo e identificar algoritmos en la vida cotidiana
- Aplicar cuatro tecnicas clave de resolucion de problemas: descomposicion, reconocimiento de patrones, abstraccion y divide y venceras
- Distinguir entre enfoques voraces y exhaustivos
- Desarrollar intuicion para la notacion Big-O y por que la eficiencia importa

---

## 1. Que es un algoritmo?

Un **algoritmo** es una secuencia finita de pasos bien definidos que toma una entrada y produce una salida. Eso es todo. No se necesitan computadoras.

Sigues algoritmos todos los dias:
- Una receta de cocina es un algoritmo (entrada: ingredientes, salida: una comida)
- Las indicaciones para llegar a un lugar son un algoritmo (entrada: ubicacion actual, salida: destino)
- El proceso de dar cambio en una caja registradora es un algoritmo (entrada: monto adeudado, salida: menor cantidad de monedas)

Lo que separa un algoritmo de instrucciones vagas es la **precision**. "Cocinar hasta que este listo" no es un algoritmo — es ambiguo. "Calentar a 180C durante 25 minutos, luego verificar la temperatura interna; si esta por debajo de 74C, continuar en incrementos de 5 minutos" es un algoritmo. Cada paso es inequivoco y el proceso termina.

Tres propiedades de un algoritmo valido:
1. **Finitud** — debe terminar eventualmente
2. **Definicion** — cada paso debe estar definido con precision
3. **Efectividad** — cada paso debe ser algo que realmente se pueda llevar a cabo

### Ejercicio practico

Escribe un algoritmo (en espanol sencillo, pasos numerados) para buscar una palabra en un diccionario fisico. Se lo suficientemente preciso para que alguien que nunca ha usado un diccionario pueda seguir tus pasos. Compara el tuyo con el enfoque descrito en la Seccion 5 (divide y venceras) — son iguales?

---

## 2. Descomposicion — Dividir problemas en partes

La habilidad de pensamiento algoritmico mas poderosa es la **descomposicion**: dividir un problema complejo en subproblemas mas pequenos y manejables.

**Ejemplo:** Quieres organizar un concierto.

Esto es abrumador como una sola tarea. Pero descomponlo:
1. Encontrar un lugar
2. Contratar artistas
3. Fijar una fecha
4. Vender boletos
5. Conseguir equipo de sonido
6. Promover el evento

Cada subproblema sigue siendo complejo, pero ahora puedes abordarlos individualmente. Y algunos subproblemas se descomponen aun mas: "Vender boletos" se convierte en elegir una plataforma, fijar precios, disenar el boleto, abrir ventas.

La descomposicion es recursiva — sigues dividiendo hasta que cada pieza es lo suficientemente simple para resolverla directamente. Asi es como se construye todo sistema de software grande: no como un programa gigante, sino como miles de piezas pequenas y componibles.

**Idea clave:** Si no puedes resolver un problema, probablemente no lo has descompuesto lo suficiente.

### Ejercicio practico

Descompone el siguiente problema en subproblemas: "Construir un sitio web que permita a los usuarios buscar acordes de guitarra." Sigue descomponiendo hasta que cada subproblema sea algo que una persona pueda completar en un dia o menos. Cuantos niveles de descomposicion necesitaste?

---

## 3. Reconocimiento de patrones

El **reconocimiento de patrones** es la habilidad de notar similitudes entre problemas que ya has resuelto y nuevos problemas que enfrentas.

**Ejemplo:** Ordenar una mano de cartas y ordenar una lista de nombres de estudiantes son el mismo problema — organizar elementos en orden segun alguna regla de comparacion. Una vez que aprendes un algoritmo de ordenamiento, puedes aplicarlo a cualquier cosa que se pueda comparar.

Los patrones aparecen en todas partes en la computacion:
- Buscar en una coleccion (encontrar un libro en una biblioteca, encontrar un archivo en disco, encontrar una nota en el diapason)
- Filtrar elementos que coinciden con criterios (filtro de spam, busqueda de fotos, consulta de acordes)
- Transformar datos de un formato a otro (traduccion, conversion de archivos, transposicion)

Los programadores experimentados resuelven problemas mas rapido no porque sean mas inteligentes, sino porque reconocen patrones. Ven un nuevo problema y piensan: "Esto es esencialmente un problema de busqueda" o "Esto es un recorrido de grafos" — y recurren a una solucion conocida.

### Ejercicio practico

Considera estos tres problemas. Que patron comparten?
1. Encontrar la ruta mas corta entre dos ciudades
2. Encontrar el menor numero de cambios de acorde para ir de un acorde a otro
3. Encontrar el numero minimo de movimientos para resolver un rompecabezas

> Todos son problemas de **camino mas corto** — encontrar la secuencia de pasos de costo minimo entre un estado inicial y un estado objetivo.

---

## 4. Abstraccion — Ignorar lo que no importa

La **abstraccion** es el arte de eliminar detalles irrelevantes para enfocarse en lo que importa para el problema en cuestion.

Cuando dibujas un mapa, no incluyes cada arbol, cada grieta en el pavimento, cada brizna de pasto. Incluyes calles, puntos de referencia y distancias — los detalles relevantes para la navegacion. Todo lo demas se abstrae.

En el pensamiento algoritmico, abstraccion significa:
- Representar un problema del mundo real con un modelo simplificado
- Ignorar detalles que no afectan la solucion
- Definir entradas y salidas claras

**Ejemplo:** Si quieres encontrar el camino mas corto entre dos ciudades, no necesitas modelar el color de las senales de transito o el limite de velocidad en cada carretera (a menos que la velocidad importe para tu problema). Abstraes el mapa en un **grafo**: las ciudades son nodos, las carreteras son aristas, las distancias son pesos. Ahora puedes aplicar un algoritmo de grafos sin pensar en asfalto.

La abstraccion es lo que permite que los algoritmos sean de **proposito general**. Un algoritmo de ordenamiento no le importa si esta ordenando numeros, nombres o acordes de guitarra. Solo necesita saber como comparar dos elementos. Todo lo demas se abstrae.

### Ejercicio practico

Estas construyendo un sistema para recomendar rutinas de practica a estudiantes de guitarra. Que detalles de cada estudiante son relevantes para el algoritmo? Que detalles se pueden abstraer? Escribe dos listas: "incluir" e "ignorar."

---

## 5. Divide y venceras

**Divide y venceras** es una estrategia algoritmica especifica:

1. **Divide** el problema en subproblemas mas pequenos del mismo tipo
2. **Vence** cada subproblema (recursivamente, si es necesario)
3. **Combina** los resultados

Esto es diferente de la descomposicion general. En divide y venceras, los subproblemas tienen la **misma estructura** que el original — solo mas pequenos.

**Ejemplo — Busqueda binaria (buscar una palabra en un diccionario):**
1. Abre el diccionario en la pagina del medio
2. Esta la palabra en esta pagina? Si si, listo.
3. Si la palabra viene antes de esta pagina alfabeticamente, repite con la primera mitad
4. Si la palabra viene despues, repite con la segunda mitad
5. Sigue dividiendo a la mitad hasta encontrar la palabra

Cada paso reduce el espacio de busqueda restante a la mitad. Un diccionario con 100,000 palabras requiere a lo sumo 17 pasos (ya que 2^17 = 131,072 > 100,000). Compara eso con empezar en la pagina 1 y leer cada entrada — hasta 100,000 pasos.

**Algoritmos clasicos de divide y venceras:**
- **Busqueda binaria** — encontrar un elemento en una coleccion ordenada
- **Merge sort** — ordenar dividiendo, ordenando mitades, luego fusionando
- **Quicksort** — ordenar eligiendo un pivote y particionando

### Ejercicio practico

Tienes una lista ordenada de 1,000 canciones. Usando busqueda binaria, cual es el numero maximo de comparaciones necesarias para encontrar una cancion especifica? (Pista: cuantas veces puedes dividir 1,000 a la mitad antes de llegar a 1?)

> log2(1000) ≈ 10. A lo sumo 10 comparaciones — comparado con 1,000 para una busqueda lineal.

---

## 6. Enfoques voraces vs exhaustivos

Dos grandes familias de algoritmos representan diferentes filosofias:

**Los algoritmos voraces** toman la decision localmente optima en cada paso, esperando que esto lleve a una solucion globalmente optima.

*Ejemplo — Dar cambio con la menor cantidad de monedas:*
- Monto: 67 centavos
- Enfoque voraz: toma la moneda mas grande que quepa. 50 (25+25) → 15 (10) → 5 (5) → 2 (1+1). Resultado: 25+25+10+5+1+1 = 6 monedas.
- Esto funciona para la moneda estadounidense. Pero para una moneda con piezas de 1, 3 y 4 centavos, el voraz falla: para 6 centavos, el voraz da 4+1+1 (3 monedas) pero el optimo es 3+3 (2 monedas).

**Los algoritmos exhaustivos** verifican cada solucion posible y eligen la mejor. Siempre encuentran la respuesta optima, pero pueden ser lentos.

*Ejemplo — El viajante:*
- Visitar 10 ciudades y regresar a casa por la ruta mas corta
- Exhaustivo: probar todas las ordenaciones posibles (10! = 3,628,800 rutas), medir cada una, elegir la mas corta
- Esto garantiza la ruta optima, pero es computacionalmente costoso

| Enfoque | Ventaja | Desventaja | Usar cuando |
|---------|---------|------------|-------------|
| Voraz | Rapido, simple | Puede perder la solucion optima | Lo suficientemente bueno es suficiente |
| Exhaustivo | Optimo garantizado | Lento para problemas grandes | La correccion es critica y la entrada es pequena |

Muchos algoritmos del mundo real combinan ambos: usan heuristicas voraces para podar el espacio de busqueda, luego verifican exhaustivamente los candidatos restantes.

### Ejercicio practico

Estas empacando una maleta con objetos de diferentes pesos y valores, y la maleta tiene un limite de peso. Describe un enfoque voraz y un enfoque exhaustivo. Cual usarias si tuvieras 5 objetos? 500 objetos?

> *Voraz:* Ordena objetos por relacion valor-peso, agrega objetos desde la mayor relacion hasta que la maleta este llena. *Exhaustivo:* Prueba cada combinacion posible, calcula el valor total para las que estan dentro del limite de peso, elige la mejor. Para 5 objetos (32 combinaciones), el exhaustivo esta bien. Para 500 objetos (2^500 combinaciones), el exhaustivo es imposible — usa voraz o un algoritmo mas inteligente.

---

## 7. Intuicion Big-O — Que tan rapido es suficientemente rapido?

No todos los algoritmos son iguales. La **notacion Big-O** describe como crece el tiempo de ejecucion de un algoritmo a medida que aumenta el tamano de la entrada.

No necesitas calcular Big-O con precision ahora mismo. Necesitas **intuicion** para lo que significan las categorias:

| Big-O | Nombre | Ejemplo | 1,000 elementos | 1,000,000 elementos |
|-------|--------|---------|-----------------|---------------------|
| O(1) | Constante | Buscar un elemento de un arreglo por indice | 1 paso | 1 paso |
| O(log n) | Logaritmico | Busqueda binaria | ~10 pasos | ~20 pasos |
| O(n) | Lineal | Recorrer cada elemento una vez | 1,000 pasos | 1,000,000 pasos |
| O(n log n) | Linearitmico | Merge sort, quicksort | ~10,000 pasos | ~20,000,000 pasos |
| O(n^2) | Cuadratico | Comparar cada par | 1,000,000 pasos | 1,000,000,000,000 pasos |
| O(2^n) | Exponencial | Busqueda exhaustiva de subconjuntos | ~10^301 pasos | Olvidalo |

La idea clave: **la diferencia entre categorias de algoritmos crece enormemente con el tamano de la entrada.** Un algoritmo O(n) y un algoritmo O(n^2) pueden sentirse instantaneos con 10 elementos. Con un millon de elementos, uno termina en un segundo y el otro tarda dias.

Por eso el pensamiento algoritmico importa. Elegir el algoritmo correcto puede ser la diferencia entre un programa que funciona y uno que nunca termina.

### Ejercicio practico

Tienes dos algoritmos para buscar en una biblioteca musical:
- Algoritmo A: verifica cada cancion una por una (O(n))
- Algoritmo B: usa un indice ordenado y busqueda binaria (O(log n))

Para una biblioteca de 10 millones de canciones, aproximadamente cuantos pasos toma cada uno?
> A: 10,000,000 pasos. B: log2(10,000,000) ≈ 23 pasos. El Algoritmo B es mas de 400,000 veces mas rapido.

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| **Algoritmo** | Una secuencia finita de pasos bien definidos que transforma entrada en salida |
| **Descomposicion** | Dividir un problema complejo en subproblemas mas pequenos y manejables |
| **Reconocimiento de patrones** | Identificar similitudes entre un problema nuevo y problemas resueltos previamente |
| **Abstraccion** | Eliminar detalles irrelevantes para enfocarse en lo que importa para la solucion |
| **Divide y venceras** | Dividir un problema en instancias mas pequenas del mismo problema, resolver recursivamente |
| **Algoritmo voraz** | Tomar la decision localmente optima en cada paso |
| **Algoritmo exhaustivo** | Verificar cada solucion posible para garantizar encontrar la mejor |
| **Notacion Big-O** | Una clasificacion de la eficiencia de algoritmos por como crece el tiempo de ejecucion con el tamano de la entrada |

---

## Autoevaluacion

**1. Que tres propiedades debe tener un algoritmo valido?**
> Finitud (termina), definicion (cada paso es inequivoco) y efectividad (cada paso puede realizarse de hecho).

**2. Necesitas buscar un nombre en una lista desordenada de 1,000 nombres. Cual es el mejor Big-O que puedes lograr?**
> O(n) — busqueda lineal. Sin ordenar o indexar, debes verificar potencialmente cada elemento. Si la lista estuviera ordenada, podrias usar busqueda binaria para O(log n).

**3. Un algoritmo voraz para dar cambio da la respuesta incorrecta para monedas de 1, 3 y 4 centavos al hacer 6 centavos. Por que?**
> El enfoque voraz elige la moneda mas grande primero (4), luego necesita 1+1 para el resto (3 monedas en total). Pero 3+3 usa solo 2 monedas. El voraz falla porque la decision localmente optima (la moneda mas grande) no lleva a la solucion globalmente optima.

**4. Por que O(n log n) se considera eficiente para ordenamiento?**
> Se ha demostrado matematicamente que ningun algoritmo de ordenamiento basado en comparaciones puede hacerlo mejor que O(n log n) en el peor caso. Merge sort y quicksort alcanzan este limite, haciendolos optimos entre los ordenamientos por comparacion.

**Criterio de aprobacion:** Descomponer un problema dado en subproblemas, identificar que enfoque algoritmico (voraz, exhaustivo, divide y venceras) se ajusta a un escenario dado, y explicar las diferencias de Big-O usando ejemplos concretos.

---

## Base de investigacion

- El pensamiento algoritmico (descomposicion, reconocimiento de patrones, abstraccion) es reconocido como una habilidad central del pensamiento computacional
- Divide y venceras, voraz y busqueda exhaustiva son los tres paradigmas algoritmicos fundamentales
- La notacion Big-O proporciona una medida de eficiencia independiente del hardware
- Ensenar intuicion algoritmica antes del analisis formal mejora la transferencia en resolucion de problemas
- Fuentes: Consenso en educacion en ciencias de la computacion, curriculo del Departamento de Ciencias de la Computacion de Streeling
- Estado de creencia: T(0.91) F(0.02) U(0.05) C(0.02)
