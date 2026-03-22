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

# Tu cerebro te miente — Sesgos cognitivos que todos deberian conocer

> **Departamento de Ciencia Cognitiva** | Nivel: Principiante | Duracion: 25 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Nombrar y explicar siete sesgos cognitivos principales
- Reconocer cada sesgo en un ejemplo del mundo real
- Aplicar al menos una estrategia correctiva por sesgo
- Explicar por que los sesgos cognitivos importan para la gobernanza de IA

---

## 1. Por que tu cerebro miente

Tu cerebro no es una maquina logica. Es una maquina de supervivencia. A lo largo de cientos de miles de anos, la evolucion lo optimizo para velocidad, no para precision. El resultado: un conjunto de atajos mentales (heuristicas) que funcionan razonablemente bien la mayor parte del tiempo, pero fallan sistematicamente de maneras predecibles.

Estas fallas predecibles se llaman **sesgos cognitivos**. No son senales de estupidez — afectan a todos, incluidos los expertos. La diferencia entre un pensador ingenuo y un pensador cuidadoso no es la ausencia de sesgo. Es la conciencia de el.

Este curso cubre siete sesgos que causan el mayor dano en la toma de decisiones, especialmente en contextos de tecnologia y gobernanza.

---

## 2. Sesgo de confirmacion

### Que es

La tendencia a buscar, interpretar y recordar informacion que confirma lo que ya crees — mientras ignoras o descartas informacion que lo contradice.

### Ejemplo vivido

Un desarrollador esta convencido de que el Framework X es la mejor opcion. Lee cinco articulos que lo elogian y uno que lo critica. Despues, recuerda los cinco articulos positivos con claridad pero tiene solo un recuerdo vago de la critica. Cuando le preguntan, dice: "Todo lo que he leido dice que es genial." No esta mintiendo. El cerebro genuinamente filtro la informacion de forma asimetrica.

### Como contrarrestarlo

- **Busca activamente evidencia que desconfirme.** Antes de tomar una decision, pregunta: "Que me haria cambiar de opinion?" Luego ve a buscar exactamente eso.
- **Haz un red team de tus propias ideas.** Asigna a alguien (o a ti mismo) el rol de encontrar cada razon por la que la idea esta equivocada.
- **Analisis pre-mortem.** Imagina que la decision fallo. Que salio mal? Esto te obliga a considerar el escenario negativo.

### Relevancia para gobernanza

El sesgo de confirmacion es la razon por la que la logica tetravalente de Demerzel incluye el estado **C (Contradictorio)**. Cuando la evidencia entra en conflicto, el sistema no lo resuelve silenciosamente a favor de la creencia existente — senala la contradiccion para investigacion.

---

## 3. Anclaje

### Que es

La tendencia a depender excesivamente del primer dato que encuentras (el "ancla") al tomar decisiones, incluso si esa informacion es irrelevante.

### Ejemplo vivido

En un experimento clasico, los investigadores giraron una ruleta frente a los participantes. La ruleta "aleatoriamente" caia en 10 o 65. Luego les preguntaron: "Que porcentaje de paises africanos estan en las Naciones Unidas?" Las personas que vieron 65 en la ruleta estimaron significativamente mas alto que quienes vieron 10 — aunque una ruleta no tiene absolutamente nada que ver con la pregunta.

En la practica: si alguien dice "este proyecto tomara seis meses" al inicio de una reunion, cada estimacion posterior orbitara alrededor de seis meses, sin importar la evidencia.

### Como contrarrestarlo

- **Genera tu propia estimacion antes de escuchar las de otros.** Escribela en privado, luego compara.
- **Considera el rango, no solo el punto.** Pregunta: "Cual es el mejor caso? El peor? El mas probable?" Esto rompe el patron de ancla unica.
- **Desconfia de los numeros redondos.** "Alrededor de un millon de usuarios" o "seis meses" son casi con certeza anclas, no analisis.

### Relevancia para gobernanza

Los umbrales de confianza en el marco de Demerzel (0.9 / 0.7 / 0.5 / 0.3) fuerzan una calibracion explicita en lugar de permitir que una sola ancla domine. No puedes simplemente decir "estoy bastante seguro" — debes asignar un numero que se mapea a una accion especifica.

---

## 4. Heuristica de disponibilidad

### Que es

La tendencia a juzgar la probabilidad de algo basandose en la facilidad con que los ejemplos vienen a la mente, en lugar de la frecuencia real.

### Ejemplo vivido

Despues de ver la cobertura de un accidente aereo, las personas sobreestiman dramaticamente el riesgo de volar — aunque volar es estadisticamente mucho mas seguro que conducir. El accidente aereo es vivido, emocional y reciente, asi que viene facilmente a la mente. Los miles de vuelos sin incidentes de ese dia son invisibles.

En tecnologia: un equipo experimenta una falla catastrofica de despliegue. Durante el siguiente ano, sobreingenierian cada despliegue, agregando semanas de proceso para prevenir una recurrencia — aunque la tasa real de fallo es 0.1%.

### Como contrarrestarlo

- **Pregunta por la tasa base.** Antes de juzgar que tan probable es algo, busca con que frecuencia realmente ocurre. "Cuantos despliegues fallaron el ano pasado de cuantos en total?"
- **Desconfia de las anecdotas vividas.** Una historia convincente no es datos. Un ejemplo vivido puede superar a cien exitos silenciosos.
- **Registra la frecuencia real.** Logs, metricas y registros superan a la memoria siempre.

### Relevancia para gobernanza

Esta es la razon por la que las politicas de Demerzel requieren estados de creencia respaldados por evidencia (T/F/U/C con pesos de probabilidad) en lugar de presentimientos. Una decision de gobernanza basada en "recuerdo que algo salio mal" no es aceptable — la creencia debe estar fundamentada en evidencia con niveles de confianza explicitos.

---

## 5. Efecto Dunning-Kruger

### Que es

Las personas con baja habilidad en un dominio tienden a sobreestimar su capacidad, mientras que las personas con alta habilidad tienden a subestimarla. Cuanto menos sabes, menos sabes sobre cuanto no sabes.

### Ejemplo vivido

Un desarrollador junior que acaba de completar un tutorial en linea anuncia que "definitivamente puede construir un sistema distribuido listo para produccion." Un ingeniero senior con 20 anos de experiencia dice "creo que probablemente podemos construirlo, pero hay varias incognitas que me preocupan." El junior tiene exceso de confianza porque no puede ver la complejidad. El senior es cauteloso porque si puede.

### Como contrarrestarlo

- **Calibrate con expertos.** Cuando te sientes confiado sobre algo fuera de tu area de experiencia, pregunta a alguien que realmente trabaje en esa area.
- **Registra tus predicciones.** Escribe lo que crees que pasara, luego verifica despues. Si consistentemente te equivocas, tu confianza esta mal calibrada.
- **Abraza el "no se."** Las palabras mas peligrosas en la toma de decisiones no son "no se" — son "estoy seguro."

### Relevancia para gobernanza

El estado **U (Desconocido)** en la logica tetravalente existe precisamente para esto. Cuando un agente no tiene suficiente evidencia, la respuesta correcta no es una suposicion — es "Desconocido." Esto dispara investigacion en lugar de falsa certeza.

---

## 6. Falacia del costo hundido

### Que es

La tendencia a seguir invirtiendo en algo por lo que ya has invertido (tiempo, dinero, esfuerzo), incluso cuando la evidencia dice que deberias parar.

### Ejemplo vivido

Has pasado 8 meses construyendo una funcionalidad. Las pruebas con usuarios muestran que nadie la quiere. La opcion racional es eliminarla. Pero el equipo dice: "Ya hemos invertido tanto — no podemos parar ahora." Esos 8 meses se fueron sin importar que. No se pueden recuperar. La unica pregunta es: "Dado donde estamos ahora, es este el mejor uso de nuestro proximo mes?" La inversion pasada es irrelevante para esa pregunta.

### Como contrarrestarlo

- **Aplica la prueba del inicio limpio.** Pregunta: "Si empezaramos desde cero hoy, sin ninguna inversion previa, eligiriamos construir esto?" Si la respuesta es no, la inversion existente no deberia cambiar esa respuesta.
- **Separa al que decide del que invirtio.** La persona que aprobo la inversion original a menudo no puede evaluar objetivamente si continuar. Busca una perspectiva fresca.
- **Celebra eliminar malos proyectos.** Haz que detener algo sea una senal de buen juicio, no de fracaso.

### Relevancia para gobernanza

La politica de rollback de Demerzel soporta explicitamente la reversion de decisiones sin importar la inversion previa. El Articulo 3 de la constitucion (Reversibilidad) dice: prefiere acciones reversibles. La capacidad de detenerse y revertir es una caracteristica, no un fracaso.

---

## 7. Sesgo del status quo

### Que es

La tendencia a preferir el estado actual de las cosas simplemente porque es el actual, incluso cuando las alternativas serian mejores.

### Ejemplo vivido

Un equipo ha estado usando una herramienta particular durante tres anos. Existe una alternativa claramente superior — es mas rapida, mas barata y tiene mejor soporte. Pero cambiar requeriria aprender algo nuevo, asi que el equipo se queda donde esta. Lo predeterminado gana no porque sea lo mejor, sino porque ya esta ahi.

### Como contrarrestarlo

- **Invierte la pregunta.** En lugar de "Deberiamos cambiar?" pregunta "Si estuvieramos usando la alternativa hoy, cambiariamos a lo que tenemos actualmente?" Si la respuesta es no, tienes sesgo del status quo.
- **Cuantifica el costo de la inaccion.** No hacer nada no es gratis. Calcula lo que la opcion actual te cuesta en tiempo, dinero u oportunidad.
- **Establece puntos de revision regulares.** Programa revisiones trimestrales de las principales decisiones de herramientas y procesos para que lo predeterminado se reconsidere periodicamente.

### Relevancia para gobernanza

La politica de kaizen requiere mejora continua — buscar activamente mejores enfoques en lugar de aceptar el status quo. Los ciclos PDCA (Planificar-Hacer-Verificar-Actuar) incorporan la reevaluacion en el proceso.

---

## 8. Sesgo de supervivencia

### Que es

La tendencia a enfocarse en los exitos (los "sobrevivientes") mientras se ignoran los fracasos que ya no son visibles, llevando a conclusiones falsas sobre que causa el exito.

### Ejemplo vivido

Los articulos de consejos para startups destacan fundadores que dejaron la universidad y se convirtieron en multimillonarios. Conclusion: dejar la universidad lleva al exito! Pero por cada desertor universitario multimillonario, hay miles de desertores trabajando en empleos comunes. Nunca escuchas sus historias. Los desertores exitosos son visibles; los no exitosos son invisibles.

En musica: "Solo practica 8 horas al dia como los grandes!" Pero por cada musico que practico 8 horas y tuvo exito, muchos mas hicieron lo mismo y no lo lograron. La practica es necesaria pero no suficiente — y el sesgo de supervivencia la hace parecer la unica variable.

### Como contrarrestarlo

- **Pregunta: "Donde estan los que no lo lograron?"** Por cada historia de exito, busca los fracasos invisibles que siguieron el mismo camino.
- **Mira la muestra completa, no solo los sobrevivientes.** Estudiar solo empresas exitosas te dice lo que hacen los ganadores, no lo que causa ganar.
- **Desconfia del consejo "solo haz lo que ellos hicieron."** La imagen completa incluye a todos los que hicieron lo mismo y fracasaron.

### Relevancia para gobernanza

La politica de moneda-de-creencia de Demerzel requiere rastrear evidencia desconfirmante, no solo evidencia confirmante. Las decisiones de gobernanza deben considerar lo que fallo y desaparecio, no solo lo que tuvo exito y permanecio visible.

---

## 9. El panorama general — Por que esto importa para la gobernanza de IA

Los agentes de IA heredan sesgos humanos a traves de sus datos de entrenamiento, las suposiciones de sus disenadores y sus objetivos de optimizacion. Un marco de gobernanza de IA que ignora los sesgos cognitivos esta construyendo sobre arena.

La arquitectura de Demerzel aborda los sesgos sistematicamente:

| Sesgo | Contramedida de gobernanza |
|-------|---------------------------|
| Sesgo de confirmacion | El estado C (Contradictorio) fuerza atencion a evidencia conflictiva |
| Anclaje | Umbrales de confianza explicitos previenen el anclaje a una sola estimacion |
| Heuristica de disponibilidad | Estados de creencia basados en evidencia superan las anecdotas vividas |
| Dunning-Kruger | El estado U (Desconocido) previene la falsa certeza |
| Falacia del costo hundido | Politica de rollback + Articulo de Reversibilidad soportan detener malas inversiones |
| Sesgo del status quo | La politica de kaizen ordena mejora continua |
| Sesgo de supervivencia | La moneda-de-creencia rastrea evidencia desconfirmante |

Conocer tus sesgos no los elimina. Pero te permite construir sistemas — humanos o de IA — que los compensen.

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| Sesgo cognitivo | Un patron sistematico de desviacion del juicio racional |
| Heuristica | Un atajo mental que permite decisiones rapidas pero puede producir errores |
| Sesgo de confirmacion | Favorecer informacion que confirma creencias existentes |
| Anclaje | Depender excesivamente del primer dato encontrado |
| Heuristica de disponibilidad | Juzgar probabilidad por facilidad de recuerdo en vez de frecuencia real |
| Efecto Dunning-Kruger | Individuos de baja habilidad sobreestiman su capacidad; los de alta habilidad la subestiman |
| Falacia del costo hundido | Continuar una inversion por el costo pasado en vez del valor futuro |
| Sesgo del status quo | Preferir el estado actual simplemente porque es el actual |
| Sesgo de supervivencia | Sacar conclusiones de los exitos ignorando los fracasos invisibles |

---

## Autoevaluacion

**1. Un equipo dice "Hemos invertido demasiado para detenernos ahora." Que sesgo esta en juego, y que pregunta deberian hacer en su lugar?**
> Falacia del costo hundido. Deberian preguntar: "Si empezaramos desde cero hoy, eligiriamos este proyecto?" La inversion pasada es irrelevante para las decisiones futuras.

**2. Despues de una brecha de seguridad importante, el equipo quiere agregar cinco capas de revision de seguridad a cada despliegue. Que sesgo podria estar impulsando esto?**
> Heuristica de disponibilidad. La brecha vivida y reciente hace que el riesgo se sienta mas grande de lo que es. Deberian ver la tasa base — cuantos despliegues realmente han tenido problemas de seguridad? — y disenar controles proporcionales al riesgo real.

**3. Te sientes muy confiado sobre un tema que aprendiste la semana pasada. Que deberia preocuparte?**
> Efecto Dunning-Kruger. Al inicio del aprendizaje, aun no sabes lo que no sabes. Busca retroalimentacion de expertos, registra tus predicciones y mantente abierto a la posibilidad de que tu confianza exceda tu competencia.

**4. Por que Demerzel usa U (Desconocido) en lugar de forzar una respuesta Verdadero/Falso?**
> Para contrarrestar el efecto Dunning-Kruger y prevenir la falsa certeza. Cuando la evidencia es insuficiente, "Desconocido" dispara investigacion en lugar de una suposicion. Es mas honesto y lleva a mejores decisiones.

**Criterio de aprobacion:** Puede nombrar y definir los siete sesgos, proporcionar un ejemplo del mundo real para al menos cinco, y explicar como al menos tres se conectan con conceptos de gobernanza de IA.

---

## Base de investigacion

- Taxonomia de sesgos cognitivos de Daniel Kahneman, *Pensar rapido, pensar despacio* (2011)
- Efecto Dunning-Kruger de Kruger & Dunning, "Unskilled and Unaware of It" (1999)
- Investigacion sobre costos hundidos de Arkes & Blumer, "The Psychology of Sunk Cost" (1985)
- Sesgo de supervivencia del analisis de blindaje de aviones de Abraham Wald en la Segunda Guerra Mundial
- Experimentos de anclaje de Tversky & Kahneman, "Judgment Under Uncertainty" (1974)
- Las contramedidas de gobernanza se mapean a la logica tetravalente, rollback, kaizen y politicas de moneda-de-creencia de Demerzel
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
