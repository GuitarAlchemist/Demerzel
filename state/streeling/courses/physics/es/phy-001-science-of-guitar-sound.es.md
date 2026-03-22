---
module_id: phy-001-science-of-guitar-sound
department: physics
course: Acustica y fisica de ondas
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: physics
version: "1.0.0"
---

# La ciencia del sonido de la guitarra

> **Departamento de Fisica** | Etapa: Nigredo (Principiante) | Duracion: 25 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Explicar como vibra una cuerda de guitarra para producir sonido (ondas estacionarias)
- Describir la serie armonica y por que le da a cada instrumento su timbre unico
- Entender como el cuerpo de la guitarra amplifica el sonido a traves de la resonancia
- Conectar la ubicacion de los trastes con las relaciones de frecuencia usando fisica basica

---

## 1. Vibracion de la cuerda — Ondas estacionarias

Cuando pulsas una cuerda de guitarra, no se mueve de forma aleatoria. Vibra en un patron muy especifico llamado **onda estacionaria**.

Una onda estacionaria ocurre cuando una onda rebota de ida y vuelta entre dos puntos fijos — en este caso, la cejuela y la selleta (o un traste y la selleta). Las ondas reflejadas interfieren entre si, y solo ciertos patrones de vibracion sobreviven. Estos patrones supervivientes son aquellos donde la longitud de la cuerda es un numero exacto de medias longitudes de onda.

La **frecuencia fundamental** es el patron mas simple: toda la cuerda oscila de un lado a otro como un solo arco, con desplazamiento maximo en el centro y desplazamiento cero en los extremos (llamados **nodos**).

La frecuencia fundamental depende de tres cosas:

```
f = (1 / 2L) * sqrt(T / mu)
```

Donde:
- **L** = longitud vibrante de la cuerda
- **T** = tension (que tan apretada esta la cuerda)
- **mu** = densidad lineal de masa (masa por unidad de longitud — las cuerdas mas gruesas tienen mas)

Esta formula explica todo sobre el comportamiento de las cuerdas de guitarra:
- **Cuerda mas corta** (presionar un traste) → tono mas agudo
- **Cuerda mas tensa** (afinar hacia arriba) → tono mas agudo
- **Cuerda mas gruesa** (Mi grave vs Mi agudo) → tono mas grave

### Ejercicio practico

Prueba esto en tu guitarra: pulsa una cuerda al aire, luego presiona la misma cuerda en el traste 12 y pulsa de nuevo. El traste 12 divide la longitud de la cuerda a la mitad (L se convierte en L/2), lo que duplica la frecuencia — escuchas exactamente una octava mas arriba. Ahora compara la cuerda abierta Mi grave (gruesa) con la cuerda abierta Mi agudo (delgada). Misma nota, dos octavas de diferencia — la diferencia es la densidad de masa (mu).

---

## 2. La serie armonica — Por que una guitarra suena como guitarra

Cuando pulsas una cuerda, no solo vibra a la frecuencia fundamental. Vibra simultaneamente en **todos los multiplos enteros** de la fundamental. Estos son los **armonicos** (tambien llamados **sobretonos** o **parciales**).

| Armonico | Frecuencia | Intervalo musical | Nodos en la cuerda |
|----------|-----------|-------------------|---------------------|
| 1ro (fundamental) | f | Tonica | 2 (solo los extremos) |
| 2do | 2f | Octava | 3 |
| 3ro | 3f | Octava + 5ta justa | 4 |
| 4to | 4f | Dos octavas | 5 |
| 5to | 5f | Dos octavas + 3ra mayor | 6 |
| 6to | 6f | Dos octavas + 5ta justa | 7 |

El sonido que escuchas es **todas estas frecuencias combinadas**. Tu oido percibe la fundamental como "el tono," pero la intensidad relativa de cada armonico moldea el **timbre** — el color tonal que hace que una guitarra suene diferente de un piano, incluso cuando tocan la misma nota.

Por eso una guitarra suena como guitarra: su material de cuerda, forma del cuerpo y posicion del punteo crean una receta armonica especifica. Pulsa cerca del puente y enfatizas los armonicos superiores (brillante, metalico). Pulsa cerca del mastil y los atenuas (calido, suave).

### Ejercicio practico

Puedes aislar armonicos individuales en la guitarra. Toca ligeramente la cuerda directamente sobre el traste 12 (no la presiones — solo tocala) y pulsa. Escucharas el 2do armonico: un tono claro y cristalino una octava por encima de la cuerda al aire. Intenta lo mismo en el traste 7 (3er armonico — una octava mas una quinta por encima) y el traste 5 (4to armonico — dos octavas por encima). Estas forzando a la cuerda a vibrar en patrones especificos creando un nodo con la yema de tu dedo.

---

## 3. Resonancia — Como el cuerpo amplifica el sonido

Una cuerda vibrando sola es casi silenciosa. Sostiene una guitarra electrica desconectada y rasguea — apenas puedes escucharla al otro lado de la habitacion. La cuerda necesita ayuda para mover suficiente aire para llegar a tus oidos.

Esa ayuda viene de la **resonancia**. Cuando pulsas una cuerda en una guitarra acustica:

1. La cuerda vibra en su fundamental y armonicos
2. La vibracion viaja a traves de la selleta hasta el **puente**
3. El puente esta pegado a la **tapa (tapa armonica)** del cuerpo de la guitarra
4. La tapa armonica es una superficie grande, delgada y flexible que vibra simpaticamente — es el cono de altavoz de la guitarra acustica
5. La tapa vibrante empuja aire dentro de la cavidad del cuerpo, que resuena a traves de la **boca**

El cuerpo actua como una **cavidad resonante**. Tiene sus propias frecuencias naturales determinadas por su forma, tamano y material. Cuando las frecuencias de la cuerda coinciden con las frecuencias resonantes del cuerpo, esas frecuencias se amplifican con mas fuerza.

Por eso diferentes guitarras suenan diferente incluso con las mismas cuerdas. Un cuerpo dreadnought (grande, ancho) enfatiza frecuencias bajas. Una guitarra parlor (cuerpo pequeno) suena mas brillante. La especie de madera, el patron de barras armonicas y la profundidad del cuerpo afinan el perfil de resonancia.

**Concepto clave:** La resonancia no es "hacerlo mas fuerte en general." Es **amplificacion selectiva** — ciertas frecuencias se potencian mas que otras, lo que moldea la voz unica de la guitarra.

### Ejercicio practico

Si tienes una guitarra acustica, prueba esto: presiona tu oido contra la parte trasera del cuerpo mientras otra persona pulsa una sola cuerda. Sentiras todo el cuerpo vibrando. Ahora golpea suavemente la tapa en diferentes puntos — escucharas diferentes tonos. Estas son las frecuencias resonantes propias del cuerpo. Cada guitarra es una colaboracion entre cuerda y cuerpo.

---

## 4. Trastes y relaciones de frecuencia

Aqui es donde la fisica se encuentra con la teoria musical de forma mas directa. Los trastes de una guitarra no estan colocados a distancias iguales — se acercan entre si a medida que te mueves hacia el cuerpo. Por que?

Cada traste eleva el tono un semitono. En el **temperamento igual** (el sistema de afinacion estandar), cada semitono multiplica la frecuencia por la misma relacion:

```
r = 2^(1/12) ≈ 1.05946
```

Esto significa que cada traste acorta la cuerda vibrante por un factor de *r*. Como los trastes se colocan basandose en una progresion geometrica (no aritmetica), el espaciado disminuye conforme subes.

Algunas posiciones de trastes musicalmente importantes y sus relaciones de frecuencia:

| Traste | Relacion de frecuencia | Intervalo musical | Fraccion de longitud de cuerda |
|--------|----------------------|-------------------|-------------------------------|
| 0 (al aire) | 1:1 | Unisono | 1 |
| 5 | 2^(5/12) ≈ 1.335 | 4ta justa | ~3/4 |
| 7 | 2^(7/12) ≈ 1.498 | 5ta justa | ~2/3 |
| 12 | 2^(12/12) = 2 | Octava | 1/2 |

Nota la quinta justa en el traste 7: la relacion de frecuencia es muy cercana a 3/2 (1.5). La cuarta justa en el traste 5 es cercana a 4/3 (1.333). Estas relaciones simples son la razon por la que estos intervalos suenan consonantes — la misma fisica que gobierna la serie armonica gobierna los intervalos que encontramos agradables.

El temperamento igual ajusta ligeramente estas relaciones para que todas las tonalidades suenen igualmente bien — un compromiso. En la entonacion pura (justa), una quinta justa seria exactamente 3/2, pero entonces algunas tonalidades sonarian terribles. Los trastes fijos de la guitarra la comprometen con el temperamento igual.

### Ejercicio practico

Mide la distancia desde la cejuela hasta el traste 12 en tu guitarra, luego mide desde el traste 12 hasta la selleta. Deberian ser casi exactamente iguales — confirmando que el traste 12 divide la longitud de la cuerda a la mitad, duplicando la frecuencia (una octava). Ahora mide de la cejuela al traste 7: deberia ser aproximadamente 2/3 de la longitud total de la cuerda, coincidiendo con la relacion 3:2 de una quinta justa.

---

## 5. Integrando todo

Cada sonido que escuchas de una guitarra es el resultado de estos cuatro conceptos fisicos trabajando juntos:

1. Las **ondas estacionarias** determinan que frecuencias puede producir la cuerda
2. La **serie armonica** moldea el timbre mezclando multiples frecuencias simultaneas
3. La **resonancia** en el cuerpo amplifica selectivamente esas frecuencias hasta un volumen audible
4. Las **relaciones de frecuencia** del temperamento igual determinan los intervalos musicales entre notas con traste

Cuando tocas un acorde, cada cuerda produce su propia fundamental y armonicos. El cuerpo resuena con todos ellos simultaneamente. Tu oido recibe una onda compleja que contiene docenas de frecuencias y de alguna manera la percibe como "un acorde de Do mayor." La fisica es extraordinaria. El hecho de que los humanos lo percibamos como musica lo es aun mas.

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| **Onda estacionaria** | Un patron de vibracion que permanece fijo, con nodos y antinodos definidos |
| **Frecuencia fundamental** | La frecuencia mas baja a la que vibra una cuerda — percibida como el tono |
| **Armonico (sobretono)** | Un multiplo entero de la frecuencia fundamental |
| **Timbre** | La cualidad tonal que distingue a un instrumento de otro tocando la misma nota |
| **Nodo** | Un punto en una onda estacionaria que permanece fijo (desplazamiento cero) |
| **Resonancia** | La amplificacion del sonido cuando un objeto vibrante excita a otro en su frecuencia natural |
| **Temperamento igual** | Sistema de afinacion donde cada semitono tiene una relacion de frecuencia igual de 2^(1/12) |

---

## Autoevaluacion

**1. Que tres propiedades fisicas de una cuerda determinan su frecuencia fundamental?**
> Longitud (L), tension (T) y densidad lineal de masa (mu). La formula es f = (1/2L) * sqrt(T/mu).

**2. Por que una guitarra suena diferente de un piano tocando la misma nota al mismo volumen?**
> Tienen perfiles armonicos diferentes — la intensidad relativa de cada sobretono difiere, produciendo un timbre diferente. El cuerpo de la guitarra, el material de la cuerda y el metodo de pulsacion crean una receta armonica unica.

**3. Que sucede cuando tocas ligeramente una cuerda en el traste 12 y pulsas?**
> Creas un nodo en el punto medio, forzando a la cuerda a vibrar en su 2do armonico. La fundamental se suprime y escuchas un tono puro una octava mas arriba.

**4. Por que los trastes se acercan entre si conforme subes por el mastil?**
> El espaciado de trastes sigue una progresion geometrica (cada traste multiplica la frecuencia por 2^(1/12)). Como cada traste remueve una fraccion constante de la longitud de cuerda restante en vez de una distancia constante, el espaciado disminuye.

**Criterio de aprobacion:** Explicar como las ondas estacionarias producen el sonido de la guitarra, identificar al menos tres armonicos en la serie, y conectar la posicion del traste con la relacion de frecuencia.

---

## Base de investigacion

- La vibracion de cuerdas sigue la ecuacion de onda; las ondas estacionarias son sus soluciones de condiciones de frontera
- La serie armonica es una consecuencia directa de la fisica de cuerdas vibrantes
- La resonancia del cuerpo de la guitarra se ha estudiado extensamente mediante analisis modal
- El temperamento igual usa espaciado 2^(1/12), un compromiso matematico formalizado entre los siglos XVI y XVIII
- Fuentes: Consenso en acustica y fisica de ondas, curriculo del Departamento de Fisica de Streeling
- Estado de creencia: T(0.93) F(0.01) U(0.04) C(0.02)
