---
module_id: phi-001-how-to-argue-well
department: philosophy
course: "Fundamentos de Filosofia"
level: beginner
prerequisites: []
estimated_duration: "25 minutes"
produced_by: philosophy
version: "1.0.0"
---

# Como argumentar bien — Logica y pensamiento critico

> **Departamento de Filosofia** | Nivel: Principiante | Duracion: 25 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Identificar la estructura de un argumento (premisas y conclusion)
- Distinguir entre validez y solidez
- Reconocer falacias logicas comunes
- Detectar malos argumentos en la conversacion cotidiana
- Construir un argumento bien estructurado por tu cuenta

---

## 1. Que es un argumento?

En filosofia, un "argumento" no es un pleito a gritos. Es un conjunto estructurado de afirmaciones:

- **Premisas** — enunciados ofrecidos como evidencia o razones
- **Conclusion** — el enunciado que las premisas supuestamente sustentan

**Ejemplo:**
- Premisa 1: Todas las guitarras tienen cuerdas.
- Premisa 2: Este instrumento es una guitarra.
- Conclusion: Por lo tanto, este instrumento tiene cuerdas.

Eso es todo. Un argumento es solo premisas que llevan a una conclusion. Todo lo demas — retorica, emocion, volumen, confianza — es decoracion.

### Como encontrar el argumento

En la conversacion cotidiana, los argumentos rara vez estan presentados de forma ordenada. Busca palabras indicadoras:

| Indicadores de premisa | Indicadores de conclusion |
|---|---|
| Porque, ya que, dado que, como | Por lo tanto, entonces, asi que, en consecuencia |
| La razon es, se sigue de | Esto significa, lo cual muestra que |
| Considerando que, debido a | Podemos concluir que, de ahi que |

**Ejemplo en la vida real:** "Deberiamos cambiar de framework porque el actual no tiene soporte de comunidad y tiene tres vulnerabilidades sin parche."

- Premisa 1: El framework actual no tiene soporte de comunidad.
- Premisa 2: Tiene tres vulnerabilidades sin parche.
- Conclusion: Deberiamos cambiar de framework.

Ahora puedes evaluar cada pieza por separado. Son verdaderas las premisas? Se sigue la conclusion?

### Ejercicio practico

Encuentra un articulo de opinion, un tuit o un mensaje de Slack que haga una afirmacion. Identifica las premisas y la conclusion. Escribelas en el formato de arriba.

---

## 2. Validez vs solidez

Estas dos palabras son la distincion mas importante en logica:

### Validez

Un argumento es **valido** si la conclusion *debe* ser verdadera siempre que las premisas sean verdaderas. Se trata de la *estructura*, no del contenido.

**Valido (pero absurdo):**
- Premisa 1: Todos los gatos estan hechos de queso.
- Premisa 2: Bigotes es un gato.
- Conclusion: Bigotes esta hecho de queso.

La estructura es perfecta. Si los gatos *estuvieran* hechos de queso, Bigotes efectivamente seria de queso. El argumento es valido aunque la Premisa 1 es obviamente falsa.

### Solidez

Un argumento es **solido** si es valido Y todas las premisas son realmente verdaderas.

**Solido:**
- Premisa 1: Todos los humanos son mortales.
- Premisa 2: Socrates es un humano.
- Conclusion: Socrates es mortal.

Estructura valida + premisas verdaderas = argumento solido. Este es el estandar de oro.

### Por que importa

Cuando alguien presenta un argumento, tienes dos preguntas separadas:
1. **Es valida la estructura?** Se sigue la conclusion de las premisas?
2. **Son verdaderas las premisas?** Es la evidencia realmente correcta?

Un mal argumento puede fallar en cualquiera de los dos niveles. Muchos desacuerdos del mundo real son en realidad sobre premisas (los hechos), no sobre logica (el razonamiento).

---

## 3. Falacias comunes — La galeria de pillos

Una **falacia** es un patron de razonamiento que parece convincente pero esta logicamente roto. Aqui estan las que encontraras con mas frecuencia:

### Ad Hominem (Atacar a la persona)

**Como se ve:** "No puedes confiar en su analisis del codigo — ella solo lleva seis meses en el equipo."

**Por que esta mal:** La calidad de un argumento no depende de quien lo hace. Un recien llegado puede tener razon; un veterano puede estar equivocado. Evalua el argumento, no a la persona.

**Cuidado con:** "Claro que *tu* dirias eso," "Que sabrian *ellos* de esto?"

### Hombre de paja (Distorsionar el argumento)

**Como se ve:** La persona A dice "Deberiamos agregar validacion de entrada a la API." La persona B responde: "Asi que quieres bloquear toda la entrada de usuarios? Eso haria el producto inutilizable."

**Por que esta mal:** La persona B esta atacando una version distorsionada del argumento de la persona A. Nadie dijo "bloquear toda la entrada." Esto facilita "ganar" contra una posicion que nadie realmente sostiene.

**Cuidado con:** "Entonces lo que *realmente* estas diciendo es..."

### Falsa dicotomia (Solo dos opciones)

**Como se ve:** "O lanzamos esta funcionalidad para el viernes o perdemos al cliente para siempre."

**Por que esta mal:** Casi siempre hay mas de dos opciones. Podrias lanzar una version parcial, negociar un nuevo plazo o abordar la preocupacion subyacente del cliente de otra manera.

**Cuidado con:** "O... o..." cuando las opciones no son genuinamente exhaustivas.

### Apelacion a la autoridad (Confiar por estatus)

**Como se ve:** "El CEO cree que deberiamos usar esta base de datos, asi que debe ser la decision correcta."

**Por que esta mal:** La autoridad no es evidencia. El CEO puede no saber nada de bases de datos. Lo que importa es el *razonamiento y la evidencia*, no quien lo dijo.

**Matiz:** La opinion de un experto *si* es evidencia cuando el experto habla dentro de su campo de experiencia. Un ingeniero de bases de datos recomendando una base de datos tiene mas peso que un CEO haciendo lo mismo. La falacia es tratar la autoridad como un *sustituto* de la evidencia en lugar de una *fuente* de ella.

### Apelacion a la popularidad (Todos piensan asi)

**Como se ve:** "Este framework de JavaScript tiene 80,000 estrellas en GitHub, asi que debe ser bueno."

**Por que esta mal:** La popularidad no es un indicador confiable de calidad. Muchas cosas populares son mediocres; muchas cosas excelentes son desconocidas.

### Pendiente resbaladiza (Si A entonces Z)

**Como se ve:** "Si permitimos trabajo remoto los viernes, pronto nadie vendra a la oficina, y la cultura de la empresa colapsara."

**Por que esta mal:** Cada paso en la cadena necesita su propia justificacion. A lleva a B solo si puedes mostrar *por que* lleva a B. Simplemente afirmar una cadena de consecuencias no es un argumento.

### Ejercicio practico

Durante las proximas 24 horas, escucha falacias en conversaciones, reuniones, noticias o redes sociales. Intenta identificar al menos un ejemplo de cada tipo mencionado arriba. Escribe lo que se dijo y que falacia representa.

---

## 4. Como detectar malos argumentos

Aqui hay una lista rapida que puedes recorrer mentalmente ante cualquier argumento:

1. **Encuentra la conclusion.** Que se esta afirmando realmente?
2. **Encuentra las premisas.** Que razones se dan?
3. **Verifica la estructura.** Se sigue la conclusion de las premisas? (Validez)
4. **Verifica las premisas.** Son realmente verdaderas? Que evidencia las respalda? (Solidez)
5. **Verifica falacias.** Se apoya el argumento en un truco logico en vez de razonamiento real?
6. **Verifica informacion faltante.** Que *no* se esta diciendo? Que suposiciones estan ocultas?

**Senales de alerta:**
- Lenguaje emocional haciendo el trabajo que la evidencia deberia hacer
- Afirmaciones vagas que no se pueden poner a prueba (ver PM-001 sobre la Prueba de BS)
- Argumentos que atacan personas en vez de ideas
- "Todos saben" o "Es obvio" usados como premisas
- Urgencia falsa ("Debemos decidir AHORA") bloqueando el analisis

---

## 5. Como construir buenos argumentos

Construir un buen argumento es el reverso de detectar uno malo:

### Paso 1: Enuncia tu conclusion con claridad

Di por que estas argumentando. Sin ambiguedades, sin enterrarlo al final.

"Creo que deberiamos reescribir el modulo de autenticacion."

### Paso 2: Proporciona premisas que realmente la sustenten

Cada premisa debe ser verificable independientemente y directamente relevante.

- "El modulo actual ha tenido 12 incidentes de seguridad en el ultimo ano."
- "El codigo fue escrito para un framework que ya no usamos."
- "Una reescritura tomaria unas 3 semanas estimadas; parchear tomaria mas tiempo en los proximos 6 meses."

### Paso 3: Aborda los contraargumentos

Los argumentos mas fuertes reconocen el mejor caso en su contra.

"El contraargumento obvio es que las reescrituras son riesgosas y a menudo toman mas tiempo del estimado. He mitigado esto limitando el alcance solo a autenticacion y agregando un buffer de tiempo del 50%."

### Paso 4: Se honesto sobre la incertidumbre

Si no estas seguro de una premisa, dilo. Esto no es debilidad — es integridad intelectual.

"Estoy seguro del conteo de incidentes de seguridad (esta en nuestros logs). La estimacion de reescritura es menos segura — asume que no habra sorpresas, lo cual es optimista."

### Ejercicio practico

Elige una decision que estes enfrentando actualmente (en el trabajo, en un proyecto, en la vida). Escribe un argumento estructurado para tu opcion preferida usando los cuatro pasos de arriba. Luego escribe el mejor contraargumento que puedas. Tu argumento original sobrevive?

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| Argumento | Un conjunto de premisas ofrecidas en apoyo de una conclusion |
| Premisa | Un enunciado ofrecido como evidencia o razon |
| Conclusion | La afirmacion que las premisas supuestamente sustentan |
| Validez | La conclusion de un argumento se sigue necesariamente de sus premisas |
| Solidez | Un argumento es valido y todas sus premisas son verdaderas |
| Falacia | Un patron de razonamiento que parece convincente pero es logicamente defectuoso |
| Ad hominem | Atacar a la persona en lugar del argumento |
| Hombre de paja | Distorsionar un argumento para hacerlo mas facil de atacar |
| Falsa dicotomia | Presentar solo dos opciones cuando existen mas |

---

## Autoevaluacion

**1. Es valido este argumento? "Todas las aves pueden volar. Los pinguinos son aves. Por lo tanto, los pinguinos pueden volar."**
> Si, es valido — la conclusion se sigue de las premisas. Pero no es solido, porque la primera premisa es falsa (no todas las aves pueden volar). Esto ilustra por que la validez sola no es suficiente.

**2. Alguien dice: "No puedes criticar esta politica — nunca has trabajado en el gobierno." Que falacia es esta?**
> Ad hominem. La calidad de la critica no depende del historial del critico. El argumento debe evaluarse por sus propios meritos.

**3. Cual es la diferencia entre un argumento valido y un argumento solido?**
> Un argumento valido tiene estructura logica correcta — si las premisas fueran verdaderas, la conclusion debe ser verdadera. Un argumento solido es valido Y tiene premisas que son realmente verdaderas. La solidez es el estandar mas alto.

**4. "O adoptamos gobernanza de IA o no tendremos gobernanza en absoluto." Que hay de malo en esto?**
> Falsa dicotomia. Hay muchas formas de gobernanza entre "gobernanza de IA" y "sin gobernanza." El argumento estrecha artificialmente las opciones.

**Criterio de aprobacion:** Puede identificar premisas y conclusiones en un argumento del mundo real, clasificar correctamente al menos cuatro falacias, y construir un argumento estructurado con reconocimiento de contraargumentos.

---

## Base de investigacion

- Estructura de argumentos y validez/solidez de Irving Copi & Carl Cohen, *Introduction to Logic* (edicion estandar)
- Taxonomia de falacias basada en las *Refutaciones sofisticas* de Aristoteles y actualizada por Douglas Walton, *Informal Logic* (1989)
- Pedagogia del pensamiento critico basada en Richard Paul & Linda Elder, *Critical Thinking* (2001)
- Relevancia para gobernanza de IA: la logica tetravalente (T/F/U/C) extiende el clasico verdadero/falso para manejar incertidumbre y contradiccion — ver directorio logic/
- Estado de creencia: T(0.88) F(0.02) U(0.07) C(0.03)
