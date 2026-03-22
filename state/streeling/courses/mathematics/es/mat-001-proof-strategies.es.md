---
module_id: mat-001-proof-strategies
department: mathematics
course: Fundamentos de razonamiento matematico
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "30 minutes"
produced_by: mathematics
version: "1.0.0"
---

# Estrategias de demostracion — Como probar cosas

> **Departamento de Matematicas** | Etapa: Nigredo (Principiante) | Duracion: 30 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Explicar que es una demostracion matematica y por que importa
- Aplicar la demostracion directa para establecer un enunciado a partir de hechos conocidos
- Aplicar la demostracion por contradiccion para mostrar que un enunciado debe ser verdadero
- Aplicar la demostracion por induccion para probar enunciados sobre todos los numeros naturales
- Reconocer que estrategia de demostracion se ajusta a un problema dado

---

## 1. Que es una demostracion?

Una demostracion es un argumento logico que establece, sin lugar a dudas, que un enunciado matematico es verdadero. No probablemente verdadero, no verdadero en la mayoria de los casos — **siempre** verdadero, en cada situacion posible que el enunciado describe.

Esto es lo que hace unica a la matematica entre las disciplinas. En ciencia, recopilas evidencia y formas teorias que podrian ser refutadas por nuevos datos. En matematica, una vez que algo se demuestra, permanece demostrado para siempre. Las demostraciones de Euclides del 300 a.C. son tan validas hoy como lo fueron entonces.

Una demostracion parte de **axiomas** (enunciados aceptados como verdaderos) y **resultados previamente demostrados**, luego usa reglas logicas para llegar a la conclusion. Cada paso debe seguirse inevitablemente de los pasos anteriores.

Tres concepciones erroneas comunes:
- **"Los ejemplos demuestran cosas."** No. Mostrar que un enunciado funciona para 10, 100 o un millon de casos no prueba que funcione para todos los casos. Un solo contraejemplo puede destruir una conjetura que paso miles de millones de pruebas.
- **"Las demostraciones deben ser largas y complicadas."** Algunas de las demostraciones mas hermosas son cortas. La elegancia es valorada.
- **"Solo hay una forma de demostrar algo."** La mayoria de los teoremas pueden demostrarse de multiples maneras. Elegir la estrategia correcta es parte del arte.

---

## 2. Demostracion directa

Una **demostracion directa** parte de lo que sabes y razona hacia adelante, paso a paso, hasta lo que quieres mostrar.

**Estructura:**
1. Asume la hipotesis (la parte "si" del enunciado)
2. Aplica definiciones, resultados conocidos y pasos logicos
3. Llega a la conclusion (la parte "entonces")

**Ejemplo: Demuestra que la suma de dos numeros pares es par.**

*Enunciado:* Si *a* y *b* son pares, entonces *a + b* es par.

*Demostracion:*
- Como *a* es par, por definicion *a = 2m* para algun entero *m*.
- Como *b* es par, por definicion *b = 2n* para algun entero *n*.
- Entonces *a + b = 2m + 2n = 2(m + n)*.
- Como *m + n* es un entero, *a + b* es 2 veces un entero, lo cual es par por definicion.

Esa es una demostracion completa. Cada paso sigue logicamente. Sin huecos, sin ambiguedades.

**Cuando usar demostracion directa:** Cuando puedes ver claramente un camino de la hipotesis a la conclusion. Cuando las definiciones te dan formas algebraicas para manipular. Esta es tu estrategia por defecto — intentala primero.

### Ejercicio practico

Demuestra que el producto de dos numeros impares es impar. (Pista: un numero impar se puede escribir como *2k + 1* para algun entero *k*.)

> *Solucion:* Sean *a = 2m + 1* y *b = 2n + 1*. Entonces *ab = (2m+1)(2n+1) = 4mn + 2m + 2n + 1 = 2(2mn + m + n) + 1*. Como *2mn + m + n* es un entero, *ab* tiene la forma *2k + 1*, asi que es impar.

---

## 3. Demostracion por contradiccion

A veces el camino directo no es obvio. La **demostracion por contradiccion** toma un enfoque diferente: asume lo opuesto de lo que quieres demostrar, luego muestra que esa suposicion lleva a algo imposible.

**Estructura:**
1. Asume la negacion del enunciado que quieres demostrar
2. Razona logicamente a partir de esa suposicion
3. Llega a una contradiccion (algo que es claramente falso, o que contradice un hecho conocido)
4. Concluye que la suposicion debe ser incorrecta, asi que el enunciado original es verdadero

**Ejemplo: Demuestra que la raiz cuadrada de 2 es irracional.**

*Enunciado:* No existe una fraccion *p/q* (con *p, q* enteros, *q* distinto de cero, en terminos reducidos) tal que *(p/q)^2 = 2*.

*Demostracion:*
- **Asume lo opuesto:** Supongamos que raiz de 2 es racional. Entonces raiz de 2 = *p/q* donde *p* y *q* son enteros sin factores comunes (terminos reducidos).
- Elevando al cuadrado ambos lados: *2 = p^2 / q^2*, entonces *p^2 = 2q^2*.
- Esto significa que *p^2* es par, lo que implica que *p* mismo debe ser par (ya que el cuadrado de un impar es impar). Entonces *p = 2k* para algun entero *k*.
- Sustituyendo: *(2k)^2 = 2q^2*, entonces *4k^2 = 2q^2*, entonces *q^2 = 2k^2*.
- Esto significa que *q^2* es par, entonces *q* es par.
- Pero ahora tanto *p* como *q* son pares, lo que significa que comparten un factor de 2. **Esto contradice nuestra suposicion** de que *p/q* estaba en terminos reducidos.
- Por lo tanto, nuestra suposicion era incorrecta. La raiz cuadrada de 2 es irracional.

**Cuando usar contradiccion:** Cuando quieres demostrar que algo no existe, o cuando el enunciado involucra palabras como "no," "no puede" o "imposible." Tambien es util cuando el enfoque directo se enreda.

### Ejercicio practico

Demuestra por contradiccion que no existe un entero mas grande. (Pista: asume que existe un entero mas grande *N*, luego considera *N + 1*.)

> *Solucion:* Supongamos que existe un entero mas grande *N*. Entonces *N + 1* tambien es un entero (los enteros son cerrados bajo la adicion). Pero *N + 1 > N*, lo que contradice la suposicion de que *N* era el mas grande. Por lo tanto, no existe un entero mas grande.

---

## 4. Demostracion por induccion

La **induccion** es tu herramienta para demostrar enunciados sobre todos los numeros naturales (o cualquier secuencia infinita). Funciona como una cadena de dominos.

**Estructura:**
1. **Caso base:** Demuestra que el enunciado es verdadero para el primer valor (usualmente *n = 0* o *n = 1*)
2. **Paso inductivo:** Asume que el enunciado es verdadero para algun valor arbitrario *n = k* (la **hipotesis inductiva**). Luego demuestra que tambien debe ser verdadero para *n = k + 1*.
3. **Conclusion:** Como el caso base es verdadero y cada caso implica el siguiente, el enunciado es verdadero para todos los numeros naturales.

Por que funciona? Si el domino 1 cae (caso base), y cada domino que cae derriba al siguiente (paso inductivo), entonces todos los dominos caen.

**Ejemplo: Demuestra que la suma 1 + 2 + 3 + ... + n = n(n+1)/2 para todos los enteros positivos n.**

*Caso base (n = 1):*
- Lado izquierdo: 1
- Lado derecho: 1(1+1)/2 = 1
- Coinciden. El caso base se cumple.

*Paso inductivo:*
- **Hipotesis inductiva:** Asume que 1 + 2 + ... + k = k(k+1)/2 para algun entero positivo *k*.
- **Muestra que se cumple para k + 1:** Necesitamos que 1 + 2 + ... + k + (k+1) = (k+1)(k+2)/2.
- Partiendo del lado izquierdo: 1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1) (usando la hipotesis inductiva)
- = (k+1)(k/2 + 1) = (k+1)(k+2)/2
- Esto coincide con la formula para *n = k + 1*. El paso inductivo se cumple.

*Conclusion:* Por induccion, la formula se cumple para todos los enteros positivos *n*.

**Cuando usar induccion:** Cuando el enunciado es sobre todos los numeros naturales (o todos los valores a partir de algun punto de inicio). Busca formulas que involucren *n*, enunciados como "para todo *n* >= 1," o definiciones recursivas.

### Ejercicio practico

Demuestra por induccion que *2^n > n* para todos los enteros positivos *n*.

> *Solucion:*
> *Caso base (n = 1):* 2^1 = 2 > 1. Verdadero.
> *Paso inductivo:* Asume 2^k > k. Entonces 2^(k+1) = 2 * 2^k > 2k (por la hipotesis). Como 2k = k + k >= k + 1 para todo k >= 1, tenemos 2^(k+1) > k + 1.
> Por induccion, 2^n > n para todos los enteros positivos n.

---

## 5. Elegir tu estrategia

Cuando te enfrentas a un enunciado para demostrar, hazte estas preguntas:

| Pregunta | Si la respuesta es si, intenta... |
|----------|----------------------------------|
| Puedo ir de la hipotesis a la conclusion usando definiciones y algebra? | Demostracion directa |
| El enunciado dice que algo es imposible, o que algo no existe? | Contradiccion |
| El enunciado es sobre todos los numeros naturales, o tiene estructura recursiva? | Induccion |
| Estoy atascado con la demostracion directa? | Intenta contradiccion como alternativa |

En la practica, los matematicos a menudo intentan la demostracion directa primero. Si se estanca, cambian a contradiccion. Si el enunciado es sobre numeros naturales, la induccion suele ser la opcion correcta.

Algunos enunciados pueden demostrarse por cualquiera de los tres metodos. Conforme ganas experiencia, desarrollas intuicion para cual enfoque sera el mas limpio.

---

## 6. Errores comunes

- **Asumir lo que intentas demostrar.** Esto se llama "peticion de principio" o razonamiento circular. En la demostracion directa, tu punto de partida debe ser la hipotesis, no la conclusion.
- **Olvidar el caso base en la induccion.** Sin el caso base, no tienes domino inicial. El paso inductivo solo no demuestra nada.
- **No enunciar claramente la hipotesis inductiva.** Se explicito: "Asumamos que el enunciado se cumple para *n = k*." Luego usa esta suposicion para demostrar el caso *k + 1*.
- **En contradiccion, no llegar realmente a una contradiccion.** Debes llegar a algo que sea definitivamente falso — no solo extrano o inesperado.

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| **Demostracion** | Un argumento logico que establece que un enunciado matematico es verdadero en todos los casos |
| **Axioma** | Un enunciado aceptado como verdadero sin demostracion, que sirve como punto de partida |
| **Demostracion directa** | Razonar hacia adelante desde la hipotesis hasta la conclusion usando definiciones y logica |
| **Demostracion por contradiccion** | Asumir la negacion de la conclusion deseada y derivar una contradiccion |
| **Demostracion por induccion** | Demostrar un caso base y un paso inductivo para establecer un enunciado para todos los numeros naturales |
| **Hipotesis inductiva** | La suposicion de que el enunciado se cumple para *n = k*, usada en el paso inductivo |
| **Contraejemplo** | Un solo caso que muestra que un enunciado es falso — un contraejemplo refuta una afirmacion universal |

---

## Autoevaluacion

**1. Cual es la diferencia fundamental entre una demostracion y una gran coleccion de ejemplos?**
> Una demostracion establece la verdad para todos los casos mediante deduccion logica. Los ejemplos solo muestran que casos especificos funcionan y no pueden descartar un contraejemplo no examinado.

**2. En la demostracion por contradiccion, cuales son los tres pasos despues de asumir la negacion?**
> Razonar logicamente desde la suposicion, llegar a un enunciado que contradice un hecho conocido, y luego concluir que la suposicion era falsa.

**3. Cuales son los dos componentes de una demostracion por induccion?**
> El caso base (demostrar el enunciado para el primer valor) y el paso inductivo (demostrar que si el enunciado se cumple para *k*, tambien se cumple para *k + 1*).

**4. Quieres demostrar que ningun numero par mayor que 2 es primo. Que estrategia usarias?**
> Demostracion directa: por definicion, un numero par mayor que 2 se puede escribir como *2k* donde *k > 1*, asi que tiene factores 1, 2, k y 2k — lo que significa que tiene un factor distinto de 1 y de si mismo, por lo tanto no es primo.

**Criterio de aprobacion:** Aplicar exitosamente la demostracion directa, por contradiccion y por induccion a ejemplos sencillos, y explicar cuando cada estrategia es apropiada.

---

## Base de investigacion

- La demostracion es la metodologia definitoria de las matematicas, desde la antigua Grecia
- La demostracion directa, por contradiccion y por induccion cubren la gran mayoria de las tecnicas de demostracion a nivel universitario
- Los errores comunes en demostracion (razonamiento circular, caso base faltante) estan bien documentados en la investigacion en educacion matematica
- Pedagogicamente, aprender estrategias de demostracion antes del contenido matematico especifico mejora la habilidad de razonamiento a largo plazo
- Fuentes: Consenso en educacion matematica, curriculo del Departamento de Matematicas de Streeling
- Estado de creencia: T(0.92) F(0.01) U(0.05) C(0.02)
