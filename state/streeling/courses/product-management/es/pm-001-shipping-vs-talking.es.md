---
module_id: pm-001-shipping-vs-talking
department: product-management
course: "Fundamentos de gestion de producto"
level: beginner
prerequisites: []
estimated_duration: "20 minutes"
produced_by: product-management
version: "1.0.0"
---

# Entregar vs hablar — Como saber si realmente estas construyendo algo

> **Departamento de Gestion de Producto y Proyectos** | Nivel: Principiante | Duracion: 20 minutos

## Objetivos

Al terminar esta leccion, seras capaz de:
- Aplicar la Prueba de BS a cualquier pitch de producto, roadmap o documento de estrategia
- Distinguir comunicacion real de relleno de palabras de moda
- Escribir un one-pager claro que un desconocido pueda ejecutar
- Separar metricas que importan de metricas de vanidad

---

## 1. El problema

Aqui hay una oracion de un documento de producto real (nombres cambiados):

> *"Estamos apalancando nuestras capacidades sinergicas de plataforma para crear una solucion best-in-class impulsada por IA que empodera a los stakeholders a traves de innovacion digital transformativa."*

Pregunta rapida: Que hace realmente esta empresa?

Si tu respuesta es "no tengo idea," felicidades — tu detector de BS esta funcionando. Esa oracion no dice absolutamente nada. Contiene cero informacion. Podrias pegarla en el sitio web de cualquier empresa y encajaria, que es exactamente el problema.

La mayoria del trabajo de producto no fracasa porque la gente sea tonta. Fracasa porque la gente habla en lugar de entregar, y nadie se da cuenta porque hablar *suena* productivo.

Este curso trata sobre distinguir la diferencia.

---

## 2. La prueba de BS

Cada afirmacion, plan o estrategia puede evaluarse en cuatro dimensiones:

### Especificidad
**Nombra cosas concretas?** Nombres, numeros, fechas, funcionalidades, usuarios.

- Reprobada: "Estamos mejorando la experiencia de usuario."
- Aprobada: "Estamos reduciendo el tiempo de carga de la pagina de pago de 4.2s a menos de 1.5s para el 15 de marzo."

### Falsificabilidad
**Se podria demostrar que es falsa?** Si un enunciado no puede ser falso de ninguna manera, no contiene informacion.

- Reprobada: "Estamos comprometidos con la excelencia." (Como se veria la no-excelencia? Como lo sabrias?)
- Aprobada: "Entregaremos el MVP a 50 usuarios beta para el viernes." (O lo hiciste o no.)

### Densidad
**Cual es la proporcion de informacion a palabras?** Cada palabra debe ganarse su lugar.

- Reprobada: "Con el fin de facilitar el proceso continuo de mejora continua en nuestro ciclo de vida de desarrollo de producto..." (18 palabras, cero informacion)
- Aprobada: "Entregamos semanalmente." (2 palabras, compromiso claro)

### Compromiso
**Obliga a alguien a algo?** Las intenciones vagas son gratis. Los compromisos tienen consecuencias.

- Reprobada: "Probablemente deberiamos investigar eso en algun momento."
- Aprobada: "Tendre la especificacion revisada para el jueves. Si no esta lista, posponemos el sprint."

### Ejercicio practico

Busca el ultimo correo, mensaje de Slack o documento que escribiste sobre un proyecto. Evalualo en las cuatro dimensiones. Se honesto. Si reprueba dos o mas, reescribelo.

---

## 3. El salon de la vergüenza de las palabras de moda

Estas palabras y frases no son inherentemente malas, pero casi siempre se usan para evitar decir algo concreto. Cuando te descubras escribiendolas, detente y pregunta: "Que quiero decir realmente?"

| Palabra de moda | Lo que la gente suele querer decir | Que decir en su lugar |
|----------------|-----------------------------------|----------------------|
| Apalancar | Usar | "Usar" |
| Sinergia | Dos cosas funcionan juntas | Nombra las dos cosas y como |
| Transformativo | Cambia cosas | Di que cambia, para quien |
| Best-in-class | Bueno, supuestamente | Comparado con que? Segun que metrica? |
| Empoderar | Darle a alguien la capacidad | Nombra la capacidad y a quien |
| Holistico | Consideramos mas de una cosa | Enumera las cosas que consideraste |
| Alinear | Ponerse de acuerdo | "Acordamos que..." |
| Deep dive | Examinar cuidadosamente | "Analizamos X y encontramos Y" |
| Mover la aguja | Mejorar una metrica | Nombra la metrica y el objetivo |
| Ecosistema | Un grupo de cosas relacionadas | Nombra las cosas |

La regla es simple: si puedes reemplazar una palabra con una mas especifica y no pierdes nada, hazlo. Si no puedes pensar en una palabra mas especifica, tal vez aun no sabes de que estas hablando — y eso esta bien, pero di *eso*.

---

## 4. Como escribir un one-pager claro

Un one-pager es el documento minimo viable para cualquier decision de producto. Si no cabe en una pagina, o no entiendes el problema o estas resolviendo demasiados problemas a la vez.

### La plantilla

**Titulo:** [Lo que estas construyendo, en lenguaje sencillo]

**Problema:** [1-2 oraciones. Quien tiene este problema? Que tan grave es? Como lo sabes?]

**Solucion:** [1-2 oraciones. Que construiras. No como — que.]

**Metrica de exito:** [Un numero que te dice si funciono. Se especifico.]

**Alcance:** [Que esta INCLUIDO. Que esta explicitamente EXCLUIDO.]

**Cronograma:** [Cuando se entrega. No "T3" — una fecha.]

**Preguntas abiertas:** [Lo que aun no sabes. Esta es la seccion mas honesta.]

### La prueba

Entrega tu one-pager a alguien que nunca ha oido de tu proyecto. Puede responder estas preguntas despues de leerlo?

1. Que problema resuelve esto?
2. Para quien?
3. Como sabras si funciono?
4. Cuando estara listo?

Si la respuesta a cualquiera de estas es "no esta claro," revisa.

### Ejercicio practico

Elige algo en lo que estes trabajando actualmente. Escribe un one-pager usando la plantilla de arriba. Cronometrate — deberia tomar 15 minutos o menos. Si toma mas, eso es diagnostico: quizas no tienes claridad sobre el problema todavia.

---

## 5. Metricas que importan vs metricas de vanidad

Una metrica de vanidad te hace sentir bien. Una metrica real te ayuda a tomar decisiones.

### La prueba

Pregunta: **"Si esta metrica cambia, hare algo diferente?"**

Si la respuesta es si, es una metrica real. Si no, es vanidad.

### Ejemplos

| Metrica de vanidad | Por que es vanidad | Alternativa real |
|-------------------|-------------------|-----------------|
| Usuarios registrados totales | Solo sube. Nunca te dice si la gente realmente usa el producto. | Usuarios activos semanales |
| Visitas a la pagina | Mucho trafico no significa nada si nadie convierte. | Tasa de conversion |
| Lineas de codigo | Mas codigo no es mejor codigo. | Tasa de defectos por funcionalidad |
| Numero de funcionalidades entregadas | Entregar basura rapido no es un logro. | Tasa de adopcion de funcionalidad (% de usuarios que la usan) |
| Seguidores en redes sociales | Los seguidores no pagan cuentas. | Ingreso por cliente |
| Reuniones realizadas | Actividad no es progreso. | Decisiones tomadas e implementadas |

### La prueba del olor del dashboard

Mira el dashboard de tu equipo. Para cada metrica, pregunta:
1. Cuando fue la ultima vez que este numero cambio una decision?
2. Si este numero se duplicara de la noche a la manana, que harias diferente?
3. Si este numero cayera a cero, alguien se daria cuenta en una semana?

Si no puedes responder estas, la metrica es decoracion.

---

## 6. La mentalidad de entregar

Los que hablan optimizan para sonar inteligentes. Los que entregan optimizan para aprender rapido.

| Patron del que habla | Patron del que entrega |
|---------------------|----------------------|
| "Agendemos una reunion para discutir el roadmap." | "Aqui esta la especificacion. Comentarios para el jueves, entregamos el lunes." |
| "Necesitamos investigar mas." | "Entregaremos un v1 a 10 usuarios y veremos que pasa." |
| "Esto necesita ser perfecto antes de lanzar." | "Cual es lo minimo que podemos entregar que nos ensene algo?" |
| "Tengo preocupaciones sobre el enfoque." | "Aqui hay tres riesgos especificos y mis mitigaciones propuestas." |
| "Alineemonos en la vision." | "Aqui esta el one-pager. Estas de acuerdo o en desacuerdo con la metrica de exito?" |

La diferencia no es inteligencia ni esfuerzo. Es la disposicion a ser especifico, comprometerse y aceptar que te demuestren que estabas equivocado.

---

## Terminos clave

| Termino | Definicion |
|---------|-----------|
| Prueba de BS | Evaluacion en cuatro dimensiones: especificidad, falsificabilidad, densidad, compromiso |
| One-pager | Un documento de una pagina que captura problema, solucion, metrica, alcance y cronograma |
| Metrica de vanidad | Un numero que se siente bien pero no informa decisiones |
| Falsificabilidad | La propiedad de una afirmacion que hace posible demostrar que es falsa |
| Entregar (shipping) | Poner producto funcional en manos de usuarios reales (no hacer demos, no presentar, no planificar) |

---

## Autoevaluacion

**1. Un colega dice "Necesitamos apalancar nuestra plataforma para impulsar resultados sinergicos." Que haces?**
> Pregunta: "Que estamos construyendo especificamente, para quien, y como sabremos si funciono?" No aceptes una respuesta que repruebe la Prueba de BS.

**2. Tu dashboard muestra "Usuarios totales: 50,000" y ha subido cada mes. Es buena senal?**
> No necesariamente. Los usuarios totales solo suben (la gente rara vez se desregistra). No te dice nada sobre engagement, retencion o valor. Pide usuarios activos semanales o tasa de retencion en su lugar.

**3. Tienes una gran idea de producto pero tu one-pager tiene tres paginas. Que sugiere esto?**
> Probablemente estas resolviendo mas de un problema, o aun no tienes claridad sobre cual problema importa mas. Dividelo o afina tu enfoque.

**Criterio de aprobacion:** Puede aplicar la Prueba de BS a un documento real, escribir un one-pager en menos de 15 minutos, y explicar por que al menos dos metricas de vanidad son enganosas.

---

## Base de investigacion

- El marco de falsificabilidad se basa en la filosofia de la ciencia de Karl Popper, aplicada al pensamiento de producto
- El concepto de metricas de vanidad popularizado por Eric Ries, *The Lean Startup* (2011)
- El formato de one-pager influenciado por la cultura de documentos "Working Backwards" de Amazon
- Los principios de densidad de informacion de George Orwell, "La politica y el idioma ingles" (1946)
- Estado de creencia: T(0.80) F(0.03) U(0.14) C(0.03)
