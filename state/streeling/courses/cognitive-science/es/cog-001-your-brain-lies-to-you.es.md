---
module_id: cog-001-your-brain-lies-to-you
department: cognitive-science
course: "Fundamentos de Ciencia Cognitiva"
level: beginner
prerequisites: []
estimated_duration: "25 minutes"
produced_by: cognitive-science
version: "1.0.0"
---

# Tu cerebro te miente — Sesgos cognitivos que todos deberían conocer

> **Departamento de Ciencia Cognitiva** | Nivel: Principiante | Duración: 25 minutos

## Objetivos

Al terminar esta lección, serás capaz de:
- Nombrar y explicar siete sesgos cognitivos principales
- Reconocer cada sesgo en un ejemplo del mundo real
- Aplicar al menos una estrategia correctiva por sesgo
- Explicar por qué los sesgos cognitivos importan para la gobernanza de IA

---

## 1. Por qué tu cerebro miente

Tu cerebro no es una máquina lógica. Es una máquina de supervivencia. A lo largo de cientos de miles de años, la evolución lo optimizó para velocidad, no para precisión. El resultado: un conjunto de atajos mentales (heurísticas) que funcionan razonablemente bien la mayor parte del tiempo, pero fallan sistemáticamente de maneras predecibles.

Estas fallas predecibles se llaman **sesgos cognitivos**. No son señales de estupidez — afectan a todos, incluidos los expertos. La diferencia entre un pensador ingenuo y un pensador cuidadoso no es la ausencia de sesgo. Es la conciencia de él.

Este curso cubre siete sesgos que causan el mayor daño en la toma de decisiones, especialmente en contextos de tecnología y gobernanza.

---

## 2. Sesgo de confirmación

### Qué es

La tendencia a buscar, interpretar y recordar información que confirma lo que ya crees — mientras ignoras o descartas información que lo contradice.

### Ejemplo vivido

Un desarrollador está convencido de que el Framework X es la mejor opción. Lee cinco artículos que lo elogian y uno que lo critica. Después, recuerda los cinco artículos positivos con claridad pero tiene solo un recuerdo vago de la crítica. Cuando le preguntan, dice: "Todo lo que he leído dice que es genial." No está mintiendo. El cerebro genuinamente filtró la información de forma asimétrica.

### Cómo contrarrestarlo

- **Busca activamente evidencia que desconfirme.** Antes de tomar una decisión, pregunta: "¿Qué me haría cambiar de opinión?" Luego ve a buscar exactamente eso.
- **Haz un red team de tus propias ideas.** Asigna a alguien (o a ti mismo) el rol de encontrar cada razón por la que la idea está equivocada.
- **Análisis pre-mortem.** Imagina que la decisión falló. ¿Qué salió mal? Esto te obliga a considerar el escenario negativo.

### Relevancia para gobernanza

El sesgo de confirmación es la razón por la que la lógica tetravalente de Demerzel incluye el estado **C (Contradictorio)**. Cuando la evidencia entra en conflicto, el sistema no lo resuelve silenciosamente a favor de la creencia existente — señala la contradicción para investigación.

---

## 3. Anclaje

### Qué es

La tendencia a depender excesivamente del primer dato que encuentras (el "ancla") al tomar decisiones, incluso si esa información es irrelevante.

### Ejemplo vivido

En un experimento clásico, los investigadores giraron una ruleta frente a los participantes. La ruleta "aleatoriamente" caía en 10 o 65. Luego les preguntaron: "¿Qué porcentaje de países africanos están en las Naciones Unidas?" Las personas que vieron 65 en la ruleta estimaron significativamente más alto que quienes vieron 10 — aunque una ruleta no tiene absolutamente nada que ver con la pregunta.

En la práctica: si alguien dice "este proyecto tomará seis meses" al inicio de una reunión, cada estimación posterior orbitará alrededor de seis meses, sin importar la evidencia.

### Cómo contrarrestarlo

- **Genera tu propia estimación antes de escuchar las de otros.** Escríbela en privado, luego compara.
- **Considera el rango, no solo el punto.** Pregunta: "¿Cuál es el mejor caso? ¿El peor? ¿El más probable?" Esto rompe el patrón de ancla única.
- **Desconfía de los números redondos.** "Alrededor de un millón de usuarios" o "seis meses" son casi con certeza anclas, no análisis.

### Relevancia para gobernanza

Los umbrales de confianza en el marco de Demerzel (0.9 / 0.7 / 0.5 / 0.3) fuerzan una calibración explícita en lugar de permitir que una sola ancla domine. No puedes simplemente decir "estoy bastante seguro" — debes asignar un número que se mapea a una acción específica.

---

## 4. Heurística de disponibilidad

### Qué es

La tendencia a juzgar la probabilidad de algo basándose en la facilidad con que los ejemplos vienen a la mente, en lugar de la frecuencia real.

### Ejemplo vivido

Después de ver la cobertura de un accidente aéreo, las personas sobreestiman dramáticamente el riesgo de volar — aunque volar es estadísticamente mucho más seguro que conducir. El accidente aéreo es vivido, emocional y reciente, así que viene fácilmente a la mente. Los miles de vuelos sin incidentes de ese día son invisibles.

En tecnología: un equipo experimenta una falla catastrófica de despliegue. Durante el siguiente año, sobreingenierían cada despliegue, agregando semanas de proceso para prevenir una recurrencia — aunque la tasa real de fallo es 0.1%.

### Cómo contrarrestarlo

- **Pregunta por la tasa base.** Antes de juzgar qué tan probable es algo, busca con qué frecuencia realmente ocurre. "¿Cuántos despliegues fallaron el año pasado de cuántos en total?"
- **Desconfía de las anécdotas vividas.** Una historia convincente no es datos. Un ejemplo vivido puede superar a cien éxitos silenciosos.
- **Registra la frecuencia real.** Logs, métricas y registros superan a la memoria siempre.

### Relevancia para gobernanza

Esta es la razón por la que las políticas de Demerzel requieren estados de creencia respaldados por evidencia (T/F/U/C con pesos de probabilidad) en lugar de presentimientos. Una decisión de gobernanza basada en "recuerdo que algo salió mal" no es aceptable — la creencia debe estar fundamentada en evidencia con niveles de confianza explícitos.

---

## 5. Efecto Dunning-Kruger

### Qué es

Las personas con baja habilidad en un dominio tienden a sobreestimar su capacidad, mientras que las personas con alta habilidad tienden a subestimarla. Cuanto menos sabes, menos sabes sobre cuánto no sabes.

### Ejemplo vivido

Un desarrollador junior que acaba de completar un tutorial en línea anuncia que "definitivamente puede construir un sistema distribuido listo para producción." Un ingeniero sénior con 20 años de experiencia dice "creo que probablemente podemos construirlo, pero hay varias incógnitas que me preocupan." El junior tiene exceso de confianza porque no puede ver la complejidad. El sénior es cauteloso porque sí puede.

### Cómo contrarrestarlo

- **Calíbrate con expertos.** Cuando te sientes confiado sobre algo fuera de tu área de experiencia, pregunta a alguien que realmente trabaje en esa área.
- **Registra tus predicciones.** Escribe lo que crees que pasará, luego verifica después. Si consistentemente te equivocas, tu confianza está mal calibrada.
- **Abraza el "no sé."** Las palabras más peligrosas en la toma de decisiones no son "no sé" — son "estoy seguro."

### Relevancia para gobernanza

El estado **U (Desconocido)** en la lógica tetravalente existe precisamente para esto. Cuando un agente no tiene suficiente evidencia, la respuesta correcta no es una suposición — es "Desconocido." Esto dispara investigación en lugar de falsa certeza.

---

## 6. Falacia del costo hundido

### Qué es

La tendencia a seguir invirtiendo en algo por lo que ya has invertido (tiempo, dinero, esfuerzo), incluso cuando la evidencia dice que deberías parar.

### Ejemplo vivido

Has pasado 8 meses construyendo una funcionalidad. Las pruebas con usuarios muestran que nadie la quiere. La opción racional es eliminarla. Pero el equipo dice: "Ya hemos invertido tanto — no podemos parar ahora." Esos 8 meses se fueron sin importar qué. No se pueden recuperar. La única pregunta es: "Dado dónde estamos ahora, ¿es este el mejor uso de nuestro próximo mes?" La inversión pasada es irrelevante para esa pregunta.

### Cómo contrarrestarlo

- **Aplica la prueba del inicio limpio.** Pregunta: "Si empezáramos desde cero hoy, sin ninguna inversión previa, eligiriamos construir esto?" Si la respuesta es no, la inversión existente no debería cambiar esa respuesta.
- **Separa al que decide del que invirtió.** La persona que aprobó la inversión original a menudo no puede evaluar objetivamente si continuar. Busca una perspectiva fresca.
- **Celebra eliminar malos proyectos.** Haz que detener algo sea una señal de buen juicio, no de fracaso.

### Relevancia para gobernanza

La política de rollback de Demerzel soporta explícitamente la reversión de decisiones sin importar la inversión previa. El Artículo 3 de la constitución (Reversibilidad) dice: prefiere acciones reversibles. La capacidad de detenerse y revertir es una característica, no un fracaso.

---

## 7. Sesgo del status quo

### Qué es

La tendencia a preferir el estado actual de las cosas simplemente porque es el actual, incluso cuando las alternativas serían mejores.

### Ejemplo vivido

Un equipo ha estado usando una herramienta particular durante tres años. Existe una alternativa claramente superior — es más rápida, más barata y tiene mejor soporte. Pero cambiar requeriría aprender algo nuevo, así que el equipo se queda donde está. Lo predeterminado gana no porque sea lo mejor, sino porque ya está ahí.

### Cómo contrarrestarlo

- **Invierte la pregunta.** En lugar de "¿Deberíamos cambiar?" pregunta "Si estuviéramos usando la alternativa hoy, ¿cambiaríamos a lo que tenemos actualmente?" Si la respuesta es no, tienes sesgo del status quo.
- **Cuantifica el costo de la inacción.** No hacer nada no es gratis. Calcula lo que la opción actual te cuesta en tiempo, dinero u oportunidad.
- **Establece puntos de revisión regulares.** Programa revisiones trimestrales de las principales decisiones de herramientas y procesos para que lo predeterminado se reconsidere periódicamente.

### Relevancia para gobernanza

La política de kaizen requiere mejora continua — buscar activamente mejores enfoques en lugar de aceptar el status quo. Los ciclos PDCA (Planificar-Hacer-Verificar-Actuar) incorporan la reevaluación en el proceso.

---

## 8. Sesgo de supervivencia

### Qué es

La tendencia a enfocarse en los éxitos (los "sobrevivientes") mientras se ignoran los fracasos que ya no son visibles, llevando a conclusiones falsas sobre qué causa el éxito.

### Ejemplo vivido

Los artículos de consejos para startups destacan fundadores que dejaron la universidad y se convirtieron en multimillonarios. Conclusión: ¡dejar la universidad lleva al éxito! Pero por cada desertor universitario multimillonario, hay miles de desertores trabajando en empleos comunes. Nunca escuchas sus historias. Los desertores exitosos son visibles; los no exitosos son invisibles.

En música: "¡Solo practica 8 horas al día como los grandes!" Pero por cada músico que practicó 8 horas y tuvo éxito, muchos más hicieron lo mismo y no lo lograron. La práctica es necesaria pero no suficiente — y el sesgo de supervivencia la hace parecer la única variable.

### Cómo contrarrestarlo

- **Pregunta: "¿Dónde están los que no lo lograron?"** Por cada historia de éxito, busca los fracasos invisibles que siguieron el mismo camino.
- **Mira la muestra completa, no solo los sobrevivientes.** Estudiar solo empresas exitosas te dice lo que hacen los ganadores, no lo que causa ganar.
- **Desconfía del consejo "solo haz lo que ellos hicieron."** La imagen completa incluye a todos los que hicieron lo mismo y fracasaron.

### Relevancia para gobernanza

La política de moneda-de-creencia de Demerzel requiere rastrear evidencia desconfirmante, no solo evidencia confirmante. Las decisiones de gobernanza deben considerar lo que falló y desapareció, no solo lo que tuvo éxito y permaneció visible.

---

## 9. El panorama general — Por qué esto importa para la gobernanza de IA

Los agentes de IA heredan sesgos humanos a través de sus datos de entrenamiento, las suposiciones de sus diseñadores y sus objetivos de optimización. Un marco de gobernanza de IA que ignora los sesgos cognitivos está construyendo sobre arena.

La arquitectura de Demerzel aborda los sesgos sistemáticamente:

| Sesgo | Contramedida de gobernanza |
|-------|---------------------------|
| Sesgo de confirmación | El estado C (Contradictorio) fuerza atención a evidencia conflictiva |
| Anclaje | Umbrales de confianza explícitos previenen el anclaje a una sola estimación |
| Heurística de disponibilidad | Estados de creencia basados en evidencia superan las anécdotas vividas |
| Dunning-Kruger | El estado U (Desconocido) previene la falsa certeza |
| Falacia del costo hundido | Política de rollback + Artículo de Reversibilidad soportan detener malas inversiones |
| Sesgo del status quo | La política de kaizen ordena mejora continua |
| Sesgo de supervivencia | La moneda-de-creencia rastrea evidencia desconfirmante |

Conocer tus sesgos no los elimina. Pero te permite construir sistemas — humanos o de IA — que los compensen.

---

## Términos clave

| Término | Definición |
|---------|-----------|
| Sesgo cognitivo | Un patrón sistemático de desviación del juicio racional |
| Heurística | Un atajo mental que permite decisiones rápidas pero puede producir errores |
| Sesgo de confirmación | Favorecer información que confirma creencias existentes |
| Anclaje | Depender excesivamente del primer dato encontrado |
| Heurística de disponibilidad | Juzgar probabilidad por facilidad de recuerdo en vez de frecuencia real |
| Efecto Dunning-Kruger | Individuos de baja habilidad sobreestiman su capacidad; los de alta habilidad la subestiman |
| Falacia del costo hundido | Continuar una inversión por el costo pasado en vez del valor futuro |
| Sesgo del status quo | Preferir el estado actual simplemente porque es el actual |
| Sesgo de supervivencia | Sacar conclusiones de los éxitos ignorando los fracasos invisibles |

---

## Autoevaluación

**1. Un equipo dice "Hemos invertido demasiado para detenernos ahora." ¿Qué sesgo está en juego, y qué pregunta deberían hacer en su lugar?**
> Falacia del costo hundido. Deberían preguntar: "Si empezáramos desde cero hoy, eligiriamos este proyecto?" La inversión pasada es irrelevante para las decisiones futuras.

**2. Después de una brecha de seguridad importante, el equipo quiere agregar cinco capas de revisión de seguridad a cada despliegue. ¿Qué sesgo podría estar impulsando esto?**
> Heurística de disponibilidad. La brecha vivida y reciente hace que el riesgo se sienta más grande de lo que es. Deberían ver la tasa base — ¿cuántos despliegues realmente han tenido problemas de seguridad? — y diseñar controles proporcionales al riesgo real.

**3. Te sientes muy confiado sobre un tema que aprendiste la semana pasada. ¿Qué debería preocuparte?**
> Efecto Dunning-Kruger. Al inicio del aprendizaje, aún no sabes lo que no sabes. Busca retroalimentación de expertos, registra tus predicciones y mantente abierto a la posibilidad de que tu confianza exceda tu competencia.

**4. ¿Por qué Demerzel usa U (Desconocido) en lugar de forzar una respuesta Verdadero/Falso?**
> Para contrarrestar el efecto Dunning-Kruger y prevenir la falsa certeza. Cuando la evidencia es insuficiente, "Desconocido" dispara investigación en lugar de una suposición. Es más honesto y lleva a mejores decisiones.

**Criterio de aprobación:** Puede nombrar y definir los siete sesgos, proporcionar un ejemplo del mundo real para al menos cinco, y explicar cómo al menos tres se conectan con conceptos de gobernanza de IA.

---

## Base de investigación

- Taxonomía de sesgos cognitivos de Daniel Kahneman, *Pensar rápido, pensar despacio* (2011)
- Efecto Dunning-Kruger de Kruger & Dunning, "Unskilled and Unaware of It" (1999)
- Investigación sobre costos hundidos de Arkes & Blumer, "The Psychology of Sunk Cost" (1985)
- Sesgo de supervivencia del análisis de blindaje de aviones de Abraham Wald en la Segunda Guerra Mundial
- Experimentos de anclaje de Tversky & Kahneman, "Judgment Under Uncertainty" (1974)
- Las contramedidas de gobernanza se mapean a la lógica tetravalente, rollback, kaizen y políticas de moneda-de-creencia de Demerzel
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
