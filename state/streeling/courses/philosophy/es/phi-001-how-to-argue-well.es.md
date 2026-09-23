---
module_id: phi-001-how-to-argue-well
department: philosophy
course: "Fundamentos de Filosofía"
level: beginner
prerequisites: []
estimated_duration: "25 minutes"
produced_by: philosophy
version: "1.0.0"
---

# Cómo argumentar bien — Lógica y pensamiento crítico

> **Departamento de Filosofía** | Nivel: Principiante | Duración: 25 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Identificar la estructura de un argumento (premisas y conclusión)
- Distinguir entre validez y solidez
- Reconocer falacias lógicas comunes
- Detectar malos argumentos en la conversación cotidiana
- Construir un argumento bien estructurado por tu cuenta

---

## 1. ¿Qué es un argumento?

En filosofía, un "argumento" no es un pleito a gritos. Es un conjunto estructurado de afirmaciones:

- **Premisas** — enunciados ofrecidos como evidencia o razones
- **Conclusión** — el enunciado que las premisas supuestamente sustentan

**Ejemplo:**
- Premisa 1: Todas las guitarras tienen cuerdas.
- Premisa 2: Este instrumento es una guitarra.
- Conclusión: Por lo tanto, este instrumento tiene cuerdas.

Eso es todo. Un argumento es solo premisas que llevan a una conclusión. Todo lo demás — retórica, emoción, volumen, confianza — es decoración.

### Cómo encontrar el argumento

En la conversación cotidiana, los argumentos rara vez están presentados de forma ordenada. Busca palabras indicadoras:

| Indicadores de premisa | Indicadores de conclusión |
|---|---|
| Porque, ya que, dado que, como | Por lo tanto, entonces, así que, en consecuencia |
| La razón es, se sigue de | Esto significa, lo cual muestra que |
| Considerando que, debido a | Podemos concluir que, de ahí que |

**Ejemplo en la vida real:** "Deberíamos cambiar de framework porque el actual no tiene soporte de comunidad y tiene tres vulnerabilidades sin parche."

- Premisa 1: El framework actual no tiene soporte de comunidad.
- Premisa 2: Tiene tres vulnerabilidades sin parche.
- Conclusión: Deberíamos cambiar de framework.

Ahora puedes evaluar cada pieza por separado. ¿Son verdaderas las premisas? ¿Se sigue la conclusión?

### Ejercicio práctico

Encuentra un artículo de opinión, un tuit o un mensaje de Slack que haga una afirmación. Identifica las premisas y la conclusión. Escríbelas en el formato de arriba.

---

## 2. Validez vs solidez

Estas dos palabras son la distinción más importante en lógica:

### Validez

Un argumento es **válido** si la conclusión *debe* ser verdadera siempre que las premisas sean verdaderas. Se trata de la *estructura*, no del contenido.

**Válido (pero absurdo):**
- Premisa 1: Todos los gatos están hechos de queso.
- Premisa 2: Bigotes es un gato.
- Conclusión: Bigotes está hecho de queso.

La estructura es perfecta. Si los gatos *estuvieran* hechos de queso, Bigotes efectivamente sería de queso. El argumento es válido aunque la Premisa 1 es obviamente falsa.

### Solidez

Un argumento es **sólido** si es válido Y todas las premisas son realmente verdaderas.

**Sólido:**
- Premisa 1: Todos los humanos son mortales.
- Premisa 2: Sócrates es un humano.
- Conclusión: Sócrates es mortal.

Estructura válida + premisas verdaderas = argumento sólido. Este es el estándar de oro.

### Por qué importa

Cuando alguien presenta un argumento, tienes dos preguntas separadas:
1. **¿Es válida la estructura?** ¿Se sigue la conclusión de las premisas?
2. **¿Son verdaderas las premisas?** ¿Es la evidencia realmente correcta?

Un mal argumento puede fallar en cualquiera de los dos niveles. Muchos desacuerdos del mundo real son en realidad sobre premisas (los hechos), no sobre lógica (el razonamiento).

---

## 3. Falacias comunes — La galería de pillos

Una **falacia** es un patrón de razonamiento que parece convincente pero está lógicamente roto. Aquí están las que encontrarás con más frecuencia:

### Ad Hominem (Atacar a la persona)

**Cómo se ve:** "No puedes confiar en su análisis del código — ella solo lleva seis meses en el equipo."

**Por qué está mal:** La calidad de un argumento no depende de quién lo hace. Un recién llegado puede tener razón; un veterano puede estar equivocado. Evalúa el argumento, no a la persona.

**Cuidado con:** "Claro que *tú* dirías eso," "¿Qué sabrían *ellos* de esto?"

### Hombre de paja (Distorsionar el argumento)

**Cómo se ve:** La persona A dice "Deberíamos agregar validación de entrada a la API." La persona B responde: "¿Así que quieres bloquear toda la entrada de usuarios? Eso haría el producto inutilizable."

**Por qué está mal:** La persona B está atacando una versión distorsionada del argumento de la persona A. Nadie dijo "bloquear toda la entrada." Esto facilita "ganar" contra una posición que nadie realmente sostiene.

**Cuidado con:** "Entonces lo que *realmente* estás diciendo es..."

### Falsa dicotomía (Solo dos opciones)

**Cómo se ve:** "O lanzamos esta funcionalidad para el viernes o perdemos al cliente para siempre."

**Por qué está mal:** Casi siempre hay más de dos opciones. Podrías lanzar una versión parcial, negociar un nuevo plazo o abordar la preocupación subyacente del cliente de otra manera.

**Cuidado con:** "O... o..." cuando las opciones no son genuinamente exhaustivas.

### Apelación a la autoridad (Confiar por estatus)

**Cómo se ve:** "El CEO cree que deberíamos usar esta base de datos, así que debe ser la decisión correcta."

**Por qué está mal:** La autoridad no es evidencia. El CEO puede no saber nada de bases de datos. Lo que importa es el *razonamiento y la evidencia*, no quién lo dijo.

**Matiz:** La opinión de un experto *sí* es evidencia cuando el experto habla dentro de su campo de experiencia. Un ingeniero de bases de datos recomendando una base de datos tiene más peso que un CEO haciendo lo mismo. La falacia es tratar la autoridad como un *sustituto* de la evidencia en lugar de una *fuente* de ella.

### Apelación a la popularidad (Todos piensan así)

**Cómo se ve:** "Este framework de JavaScript tiene 80,000 estrellas en GitHub, así que debe ser bueno."

**Por qué está mal:** La popularidad no es un indicador confiable de calidad. Muchas cosas populares son mediocres; muchas cosas excelentes son desconocidas.

### Pendiente resbaladiza (Si A entonces Z)

**Cómo se ve:** "Si permitimos trabajo remoto los viernes, pronto nadie vendrá a la oficina, y la cultura de la empresa colapsará."

**Por qué está mal:** Cada paso en la cadena necesita su propia justificación. A lleva a B solo si puedes mostrar *por qué* lleva a B. Simplemente afirmar una cadena de consecuencias no es un argumento.

### Ejercicio práctico

Durante las próximas 24 horas, escucha falacias en conversaciones, reuniones, noticias o redes sociales. Intenta identificar al menos un ejemplo de cada tipo mencionado arriba. Escribe lo que se dijo y qué falacia representa.

---

## 4. Cómo detectar malos argumentos

Aquí hay una lista rápida que puedes recorrer mentalmente ante cualquier argumento:

1. **Encuentra la conclusión.** ¿Qué se está afirmando realmente?
2. **Encuentra las premisas.** ¿Qué razones se dan?
3. **Verifica la estructura.** ¿Se sigue la conclusión de las premisas? (Validez)
4. **Verifica las premisas.** ¿Son realmente verdaderas? ¿Qué evidencia las respalda? (Solidez)
5. **Verifica falacias.** ¿Se apoya el argumento en un truco lógico en vez de razonamiento real?
6. **Verifica información faltante.** ¿Qué *no* se está diciendo? ¿Qué suposiciones están ocultas?

**Señales de alerta:**
- Lenguaje emocional haciendo el trabajo que la evidencia debería hacer
- Afirmaciones vagas que no se pueden poner a prueba (ver PM-001 sobre la Prueba de BS)
- Argumentos que atacan personas en vez de ideas
- "Todos saben" o "Es obvio" usados como premisas
- Urgencia falsa ("Debemos decidir AHORA") bloqueando el análisis

---

## 5. Cómo construir buenos argumentos

Construir un buen argumento es el reverso de detectar uno malo:

### Paso 1: Enuncia tu conclusión con claridad

Di por qué estás argumentando. Sin ambigüedades, sin enterrarlo al final.

"Creo que deberíamos reescribir el módulo de autenticación."

### Paso 2: Proporciona premisas que realmente la sustenten

Cada premisa debe ser verificable independientemente y directamente relevante.

- "El módulo actual ha tenido 12 incidentes de seguridad en el último año."
- "El código fue escrito para un framework que ya no usamos."
- "Una reescritura tomaría unas 3 semanas estimadas; parchear tomaría más tiempo en los próximos 6 meses."

### Paso 3: Aborda los contraargumentos

Los argumentos más fuertes reconocen el mejor caso en su contra.

"El contraargumento obvio es que las reescrituras son riesgosas y a menudo toman más tiempo del estimado. He mitigado esto limitando el alcance solo a autenticación y agregando un buffer de tiempo del 50%."

### Paso 4: Sé honesto sobre la incertidumbre

Si no estás seguro de una premisa, dilo. Esto no es debilidad — es integridad intelectual.

"Estoy seguro del conteo de incidentes de seguridad (está en nuestros logs). La estimación de reescritura es menos segura — asume que no habrá sorpresas, lo cual es optimista."

### Ejercicio práctico

Elige una decisión que estés enfrentando actualmente (en el trabajo, en un proyecto, en la vida). Escribe un argumento estructurado para tu opción preferida usando los cuatro pasos de arriba. Luego escribe el mejor contraargumento que puedas. ¿Tu argumento original sobrevive?

---

## Términos clave

| Término | Definición |
|---------|-----------|
| Argumento | Un conjunto de premisas ofrecidas en apoyo de una conclusión |
| Premisa | Un enunciado ofrecido como evidencia o razón |
| Conclusión | La afirmación que las premisas supuestamente sustentan |
| Validez | La conclusión de un argumento se sigue necesariamente de sus premisas |
| Solidez | Un argumento es válido y todas sus premisas son verdaderas |
| Falacia | Un patrón de razonamiento que parece convincente pero es lógicamente defectuoso |
| Ad hominem | Atacar a la persona en lugar del argumento |
| Hombre de paja | Distorsionar un argumento para hacerlo más fácil de atacar |
| Falsa dicotomía | Presentar solo dos opciones cuando existen más |

---

## Autoevaluación

**1. ¿Es válido este argumento? "Todas las aves pueden volar. Los pingüinos son aves. Por lo tanto, los pingüinos pueden volar."**
> Sí, es válido — la conclusión se sigue de las premisas. Pero no es sólido, porque la primera premisa es falsa (no todas las aves pueden volar). Esto ilustra por qué la validez sola no es suficiente.

**2. Alguien dice: "No puedes criticar esta política — nunca has trabajado en el gobierno." ¿Qué falacia es esta?**
> Ad hominem. La calidad de la crítica no depende del historial del crítico. El argumento debe evaluarse por sus propios méritos.

**3. ¿Cuál es la diferencia entre un argumento válido y un argumento sólido?**
> Un argumento válido tiene estructura lógica correcta — si las premisas fueran verdaderas, la conclusión debe ser verdadera. Un argumento sólido es válido Y tiene premisas que son realmente verdaderas. La solidez es el estándar más alto.

**4. "O adoptamos gobernanza de IA o no tendremos gobernanza en absoluto." ¿Qué hay de malo en esto?**
> Falsa dicotomía. Hay muchas formas de gobernanza entre "gobernanza de IA" y "sin gobernanza." El argumento estrecha artificialmente las opciones.

**Criterio de aprobación:** Puede identificar premisas y conclusiones en un argumento del mundo real, clasificar correctamente al menos cuatro falacias, y construir un argumento estructurado con reconocimiento de contraargumentos.

---

## Base de investigación

- Estructura de argumentos y validez/solidez de Irving Copi & Carl Cohen, *Introduction to Logic* (edición estándar)
- Taxonomía de falacias basada en las *Refutaciones sofísticas* de Aristóteles y actualizada por Douglas Walton, *Informal Logic* (1989)
- Pedagogía del pensamiento crítico basada en Richard Paul & Linda Elder, *Critical Thinking* (2001)
- Relevancia para gobernanza de IA: la lógica tetravalente (T/F/U/C) extiende el clásico verdadero/falso para manejar incertidumbre y contradicción — ver directorio logic/
- Estado de creencia: T(0.88) F(0.02) U(0.07) C(0.03)
