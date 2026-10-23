---
module_id: mat-001-proof-strategies
department: mathematics
course: Fundamentos de razonamiento matemático
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "30 minutes"
produced_by: mathematics
version: "1.0.0"
---

# Estrategias de demostración — Cómo probar cosas

> **Departamento de Matemáticas** | Etapa: Nigredo (Principiante) | Duración: 30 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Explicar qué es una demostración matemática y por qué importa
- Aplicar la demostración directa para establecer un enunciado a partir de hechos conocidos
- Aplicar la demostración por contradicción para mostrar que un enunciado debe ser verdadero
- Aplicar la demostración por inducción para probar enunciados sobre todos los números naturales
- Reconocer qué estrategia de demostración se ajusta a un problema dado

---

## 1. ¿Qué es una demostración?

Una demostración es un argumento lógico que establece, sin lugar a dudas, que un enunciado matemático es verdadero. No probablemente verdadero, no verdadero en la mayoría de los casos — **siempre** verdadero, en cada situación posible que el enunciado describe.

Esto es lo que hace única a la matemática entre las disciplinas. En ciencia, recopilas evidencia y formas teorías que podrían ser refutadas por nuevos datos. En matemática, una vez que algo se demuestra, permanece demostrado para siempre. Las demostraciones de Euclides del 300 a.C. son tan válidas hoy como lo fueron entonces.

Una demostración parte de **axiomas** (enunciados aceptados como verdaderos) y **resultados previamente demostrados**, luego usa reglas lógicas para llegar a la conclusión. Cada paso debe seguirse inevitablemente de los pasos anteriores.

Tres concepciones erróneas comunes:
- **"Los ejemplos demuestran cosas."** No. Mostrar que un enunciado funciona para 10, 100 o un millón de casos no prueba que funcione para todos los casos. Un solo contraejemplo puede destruir una conjetura que pasó miles de millones de pruebas.
- **"Las demostraciones deben ser largas y complicadas."** Algunas de las demostraciones más hermosas son cortas. La elegancia es valorada.
- **"Solo hay una forma de demostrar algo."** La mayoría de los teoremas pueden demostrarse de múltiples maneras. Elegir la estrategia correcta es parte del arte.

---

## 2. Demostración directa

Una **demostración directa** parte de lo que sabes y razona hacia adelante, paso a paso, hasta lo que quieres mostrar.

**Estructura:**
1. Asume la hipótesis (la parte "si" del enunciado)
2. Aplica definiciones, resultados conocidos y pasos lógicos
3. Llega a la conclusión (la parte "entonces")

**Ejemplo: Demuestra que la suma de dos números pares es par.**

*Enunciado:* Si *a* y *b* son pares, entonces *a + b* es par.

*Demostración:*
- Como *a* es par, por definición *a = 2m* para algún entero *m*.
- Como *b* es par, por definición *b = 2n* para algún entero *n*.
- Entonces *a + b = 2m + 2n = 2(m + n)*.
- Como *m + n* es un entero, *a + b* es 2 veces un entero, lo cual es par por definición.

Esa es una demostración completa. Cada paso sigue lógicamente. Sin huecos, sin ambigüedades.

**Cuándo usar demostración directa:** Cuando puedes ver claramente un camino de la hipótesis a la conclusión. Cuando las definiciones te dan formas algebraicas para manipular. Esta es tu estrategia por defecto — inténtala primero.

### Ejercicio práctico

Demuestra que el producto de dos números impares es impar. (Pista: un número impar se puede escribir como *2k + 1* para algún entero *k*.)

> *Solución:* Sean *a = 2m + 1* y *b = 2n + 1*. Entonces *ab = (2m+1)(2n+1) = 4mn + 2m + 2n + 1 = 2(2mn + m + n) + 1*. Como *2mn + m + n* es un entero, *ab* tiene la forma *2k + 1*, así que es impar.

---

## 3. Demostración por contradicción

A veces el camino directo no es obvio. La **demostración por contradicción** toma un enfoque diferente: asume lo opuesto de lo que quieres demostrar, luego muestra que esa suposición lleva a algo imposible.

**Estructura:**
1. Asume la negación del enunciado que quieres demostrar
2. Razona lógicamente a partir de esa suposición
3. Llega a una contradicción (algo que es claramente falso, o que contradice un hecho conocido)
4. Concluye que la suposición debe ser incorrecta, así que el enunciado original es verdadero

**Ejemplo: Demuestra que la raíz cuadrada de 2 es irracional.**

*Enunciado:* No existe una fracción *p/q* (con *p, q* enteros, *q* distinto de cero, en términos reducidos) tal que *(p/q)^2 = 2*.

*Demostración:*
- **Asume lo opuesto:** Supongamos que raíz de 2 es racional. Entonces raíz de 2 = *p/q* donde *p* y *q* son enteros sin factores comunes (términos reducidos).
- Elevando al cuadrado ambos lados: *2 = p^2 / q^2*, entonces *p^2 = 2q^2*.
- Esto significa que *p^2* es par, lo que implica que *p* mismo debe ser par (ya que el cuadrado de un impar es impar). Entonces *p = 2k* para algún entero *k*.
- Sustituyendo: *(2k)^2 = 2q^2*, entonces *4k^2 = 2q^2*, entonces *q^2 = 2k^2*.
- Esto significa que *q^2* es par, entonces *q* es par.
- Pero ahora tanto *p* como *q* son pares, lo que significa que comparten un factor de 2. **Esto contradice nuestra suposición** de que *p/q* estaba en términos reducidos.
- Por lo tanto, nuestra suposición era incorrecta. La raíz cuadrada de 2 es irracional.

**Cuándo usar contradicción:** Cuando quieres demostrar que algo no existe, o cuando el enunciado involucra palabras como "no," "no puede" o "imposible." También es útil cuando el enfoque directo se enreda.

### Ejercicio práctico

Demuestra por contradicción que no existe un entero más grande. (Pista: asume que existe un entero más grande *N*, luego considera *N + 1*.)

> *Solución:* Supongamos que existe un entero más grande *N*. Entonces *N + 1* también es un entero (los enteros son cerrados bajo la adición). Pero *N + 1 > N*, lo que contradice la suposición de que *N* era el más grande. Por lo tanto, no existe un entero más grande.

---

## 4. Demostración por inducción

La **inducción** es tu herramienta para demostrar enunciados sobre todos los números naturales (o cualquier secuencia infinita). Funciona como una cadena de dominós.

**Estructura:**
1. **Caso base:** Demuestra que el enunciado es verdadero para el primer valor (usualmente *n = 0* o *n = 1*)
2. **Paso inductivo:** Asume que el enunciado es verdadero para algún valor arbitrario *n = k* (la **hipótesis inductiva**). Luego demuestra que también debe ser verdadero para *n = k + 1*.
3. **Conclusión:** Como el caso base es verdadero y cada caso implica el siguiente, el enunciado es verdadero para todos los números naturales.

¿Por qué funciona? Si el dominó 1 cae (caso base), y cada dominó que cae derriba al siguiente (paso inductivo), entonces todos los dominós caen.

**Ejemplo: Demuestra que la suma 1 + 2 + 3 + ... + n = n(n+1)/2 para todos los enteros positivos n.**

*Caso base (n = 1):*
- Lado izquierdo: 1
- Lado derecho: 1(1+1)/2 = 1
- Coinciden. El caso base se cumple.

*Paso inductivo:*
- **Hipótesis inductiva:** Asume que 1 + 2 + ... + k = k(k+1)/2 para algún entero positivo *k*.
- **Muestra que se cumple para k + 1:** Necesitamos que 1 + 2 + ... + k + (k+1) = (k+1)(k+2)/2.
- Partiendo del lado izquierdo: 1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1) (usando la hipótesis inductiva)
- = (k+1)(k/2 + 1) = (k+1)(k+2)/2
- Esto coincide con la fórmula para *n = k + 1*. El paso inductivo se cumple.

*Conclusión:* Por inducción, la fórmula se cumple para todos los enteros positivos *n*.

**Cuándo usar inducción:** Cuando el enunciado es sobre todos los números naturales (o todos los valores a partir de algún punto de inicio). Busca fórmulas que involucren *n*, enunciados como "para todo *n* >= 1," o definiciones recursivas.

### Ejercicio práctico

Demuestra por inducción que *2^n > n* para todos los enteros positivos *n*.

> *Solución:*
> *Caso base (n = 1):* 2^1 = 2 > 1. Verdadero.
> *Paso inductivo:* Asume 2^k > k. Entonces 2^(k+1) = 2 * 2^k > 2k (por la hipótesis). Como 2k = k + k >= k + 1 para todo k >= 1, tenemos 2^(k+1) > k + 1.
> Por inducción, 2^n > n para todos los enteros positivos n.

---

## 5. Elegir tu estrategia

Cuando te enfrentas a un enunciado para demostrar, hazte estas preguntas:

| Pregunta | Si la respuesta es sí, intenta... |
|----------|----------------------------------|
| ¿Puedo ir de la hipótesis a la conclusión usando definiciones y álgebra? | Demostración directa |
| ¿El enunciado dice que algo es imposible, o que algo no existe? | Contradicción |
| ¿El enunciado es sobre todos los números naturales, o tiene estructura recursiva? | Inducción |
| ¿Estoy atascado con la demostración directa? | Intenta contradicción como alternativa |

En la práctica, los matemáticos a menudo intentan la demostración directa primero. Si se estanca, cambian a contradicción. Si el enunciado es sobre números naturales, la inducción suele ser la opción correcta.

Algunos enunciados pueden demostrarse por cualquiera de los tres métodos. Conforme ganas experiencia, desarrollas intuición para cuál enfoque será el más limpio.

---

## 6. Errores comunes

- **Asumir lo que intentas demostrar.** Esto se llama "petición de principio" o razonamiento circular. En la demostración directa, tu punto de partida debe ser la hipótesis, no la conclusión.
- **Olvidar el caso base en la inducción.** Sin el caso base, no tienes dominó inicial. El paso inductivo solo no demuestra nada.
- **No enunciar claramente la hipótesis inductiva.** Sé explícito: "Asumamos que el enunciado se cumple para *n = k*." Luego usa esta suposición para demostrar el caso *k + 1*.
- **En contradicción, no llegar realmente a una contradicción.** Debes llegar a algo que sea definitivamente falso — no solo extraño o inesperado.

---

## Términos clave

| Término | Definición |
|---------|-----------|
| **Demostración** | Un argumento lógico que establece que un enunciado matemático es verdadero en todos los casos |
| **Axioma** | Un enunciado aceptado como verdadero sin demostración, que sirve como punto de partida |
| **Demostración directa** | Razonar hacia adelante desde la hipótesis hasta la conclusión usando definiciones y lógica |
| **Demostración por contradicción** | Asumir la negación de la conclusión deseada y derivar una contradicción |
| **Demostración por inducción** | Demostrar un caso base y un paso inductivo para establecer un enunciado para todos los números naturales |
| **Hipótesis inductiva** | La suposición de que el enunciado se cumple para *n = k*, usada en el paso inductivo |
| **Contraejemplo** | Un solo caso que muestra que un enunciado es falso — un contraejemplo refuta una afirmación universal |

---

## Autoevaluación

**1. ¿Cuál es la diferencia fundamental entre una demostración y una gran colección de ejemplos?**
> Una demostración establece la verdad para todos los casos mediante deducción lógica. Los ejemplos solo muestran que casos específicos funcionan y no pueden descartar un contraejemplo no examinado.

**2. En la demostración por contradicción, ¿cuáles son los tres pasos después de asumir la negación?**
> Razonar lógicamente desde la suposición, llegar a un enunciado que contradice un hecho conocido, y luego concluir que la suposición era falsa.

**3. ¿Cuáles son los dos componentes de una demostración por inducción?**
> El caso base (demostrar el enunciado para el primer valor) y el paso inductivo (demostrar que si el enunciado se cumple para *k*, también se cumple para *k + 1*).

**4. Quieres demostrar que ningún número par mayor que 2 es primo. ¿Qué estrategia usarías?**
> Demostración directa: por definición, un número par mayor que 2 se puede escribir como *2k* donde *k > 1*, así que tiene factores 1, 2, k y 2k — lo que significa que tiene un factor distinto de 1 y de sí mismo, por lo tanto no es primo.

**Criterio de aprobación:** Aplicar exitosamente la demostración directa, por contradicción y por inducción a ejemplos sencillos, y explicar cuándo cada estrategia es apropiada.

---

## Base de investigación

- La demostración es la metodología definitoria de las matemáticas, desde la antigua Grecia
- La demostración directa, por contradicción y por inducción cubren la gran mayoría de las técnicas de demostración a nivel universitario
- Los errores comunes en demostración (razonamiento circular, caso base faltante) están bien documentados en la investigación en educación matemática
- Pedagógicamente, aprender estrategias de demostración antes del contenido matemático específico mejora la habilidad de razonamiento a largo plazo
- Fuentes: Consenso en educación matemática, currículo del Departamento de Matemáticas de Streeling
- Estado de creencia: T(0.92) F(0.01) U(0.05) C(0.02)
