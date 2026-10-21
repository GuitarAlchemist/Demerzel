---
module_id: psy-024-the-single-actor
department: psychohistory
course: "El actor único: cuando un solo remitente es todo el conjunto"
level: intermediate
prerequisites: ["psy-004-how-large-is-large", "psy-009-concentration-and-heavy-tails"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-024
version: "0.1.0"
---

# El actor único: cuando un solo remitente es todo el conjunto

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo contará los actores que nombra un registro, medirá lo concentrada que está su actividad, acotará esa medida cuando se ha perdido parte del registro y dirá qué establece el resultado sobre quién actuó. **Pregunta de proyecto:** las leyes del agregado suponen muchos actores independientes. ¿Quién generó realmente los eventos registrados?

[PSY-002](psy-002-governance-phase-transitions.es.md) interpreta el comportamiento agregado del ecosistema como sujeto a leyes estadísticas; [PSY-004](psy-004-how-large-is-large.es.md) muestra a cuán pocos agentes independientes equivalen catorce agentes correlacionados. Este módulo plantea una pregunta previa: ¿cuántos actores contienen los registros? [PSY-009](psy-009-concentration-and-heavy-tails.es.md) mide la concentración del mismo registro por días; este, por actores.

## 1. Un solo remitente, y lo que significa «sender»

**Observado.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-024/extract.py) lee los 594 archivos de [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) en el commit `4b03838` y sustituye cada identidad por una etiqueta antes de escribir [`observed-input.json`](../../../fixtures/psychohistory/psy-024/observed-input.json). Los **594** eventos archivados, del 2026-03-20 al 2026-07-16, llevan todos el mismo `sender`, etiquetado como *cuenta A* (*account A* en los datos), y el mismo `repo`. Lo mismo ocurre con 8 eventos posteriores que quedaron en la carpeta superior: 602 eventos con un remitente legible, una sola cuenta.

El [archivo del flujo de trabajo en el commit fijado](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L75), una versión posterior de la que escribió estos archivos (no se leyeron las versiones anteriores), asigna a `sender` el valor `github.actor`, que GitHub [define](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts) como «The username of the user that triggered the initial workflow run» (el nombre de usuario de quien desencadenó la ejecución inicial del flujo de trabajo), y a `repo`, el nombre del repositorio en el que se ejecuta. Por tanto:

- `repo` no puede variar: el registrador se instaló en un solo repositorio. «Un solo repositorio» dice dónde estaba el instrumento, no que los demás repositorios estuvieran inactivos.
- `sender` nombra una *cuenta*: las credenciales con las que un *push*, una incidencia o una discusión llegó a la plataforma. El archivo de propietarios del código (*code owners*) nombra a un mantenedor, el único propietario en sus 7 líneas de reglas; `extract.py` confirma que es la cuenta A.
- Una cuenta no es ni una persona ni un agente. [`AGENTS.md`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/AGENTS.md) define un equipo de 5 roles de agente, pero ninguna de las 9 claves de un evento nombra un rol, una *persona* (un perfil de agente), una sesión o un modelo: todo lo que actúa con las credenciales del mantenedor queda registrado como cuenta A.

«Un solo actor» es, por tanto, un enunciado sobre el poder de resolución del registro: distingue cuentas, y encontró una.

Para medir la concentración, asigne a cada uno de los k actores su *proporción* s de los eventos:

```text
H = s_1² + s_2² + … + s_k²    índice de concentración: 1/k para k actores iguales, 1 para uno solo
N = 1 / H                      número efectivo de actores: actores iguales que dan esta H
```

H es la suma de los cuadrados de las proporciones (el índice de Simpson; los economistas lo llaman índice de Herfindahl–Hirschman). Para los eventos archivados, H = 1 y N = 1.

**Lo archivado es un conjunto de supervivientes. Calculado** a partir de commits y árboles: en total se añadieron 615 eventos de disparador (más un archivo de programación), 603 siguen presentes en el commit fijado y **12** se eliminaron sin haberse archivado. El `sender` de un archivo está en su contenido, que este clon no puede leer. El historial solo muestra que 11 de ellos los añadieron commits con la identidad del flujo de trabajo, cuyos asuntos (la primera línea del mensaje) nombran un tipo de evento y el mismo repositorio (en los 602 eventos supervivientes, asunto y archivo coinciden), y que el duodécimo, un disparador `self_initiated` y no un evento del repositorio, lo añadió otro commit con la cadena del autor A, cuyo asunto anuncia el primer ciclo autónomo del *driver* (el agente autónomo que trabaja por ciclos). Sus remitentes pueden acotarse, no conocerse.

### Ejercicio práctico 1

Tome el peor caso para «un solo remitente»: cada uno de los 12 archivos eliminados procede de una cuenta distinta, ninguna de ellas la cuenta A. Calcule H y N para los 606 eventos. Suponga después que los 12 proceden de una misma cuenta distinta de la A.

> **Respuesta:** Doce remitentes nuevos: `H = (594² + 12 × 1²) / 606² = 352,848 / 367,236 = 0.960821` y `N = 1.0408`. Un solo remitente nuevo: `H = (594² + 12²) / 606² = 352,980 / 367,236 = 0.961180` y `N = 1.0404`. La cuenta A conserva al menos `594 / 606 = 98.02%`. Cualquier asignación da un N entre 1 y 1.0408: un remitente nuevo por archivo es lo que menos añade a la suma de los cuadrados de los recuentos, y asignarlos todos a la cuenta más grande, lo que más. Estos remitentes son supuestos: la pérdida no puede convertir a un solo remitente en un conjunto.

## 2. Una escala para N

**Sintético.** [`scenarios.json`](../../../fixtures/psychohistory/psy-024/scenarios.json) define conjuntos imaginarios de 14 actores, el número que da el principio clave del departamento; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-024/analyze.py) calcula:

| Conjunto imaginario | H | N | Número de media cobertura | Dispersión relativa |
|---|---|---|---|---|
| 14 actores iguales | 0.071429 | 14 | 8 | 0.2673 |
| 14 actores; el de rango r tiene 1/r de los eventos del primero | 0.149063 | 6.7086 | 3 | 0.3861 |
| 14 actores, cada uno con la mitad que el anterior | 0.333374 | 2.9996 | 1 | 0.5774 |
| 14 actores, uno de ellos con el 90% | 0.810769 | 1.2334 | 1 | 0.9004 |
| 1 actor | 1 | 1 | 1 | 1 |

El *número de media cobertura* es el menor número de actores que reúnen entre todos más de la mitad de los eventos: un pariente, basado en recuentos, del «factor autobús» (*bus factor* o *truck factor*), que Avelino y sus colegas estiman a partir de quién escribió qué archivos.

N importa para una ley estadística por lo que hace el promedio. Suponga que un agregado promedia sobre los eventos, de modo que cada actor pesa según su proporción, y que los actores se comportan de forma independiente con la misma variabilidad:

```text
varianza del agregado = H × varianza de un actor
dispersión relativa   = sqrt(H) = 1 / sqrt(N)
```

El agregado fluctúa como una media de N actores iguales. La ley de los grandes números necesita un N grande; con N = 1, el «agregado» es el actor y no se promedia nada. Una simulación con semilla fija de 20,000 ocasiones por conjunto da N = 14.08, 6.72, 2.98, 1.24 y 1.00 para las cinco filas.

### Ejercicio práctico 2

Un registro de 100 eventos tiene tres actores, con 50, 30 y 20 eventos. Calcule H, N, el número de media cobertura y la dispersión relativa.

> **Respuesta:** `H = 0.5² + 0.3² + 0.2² = 0.38` y `N = 1 / 0.38 = 2.6316`. El actor más grande reúne exactamente la mitad, que no es más de la mitad, así que el número de media cobertura es 2. Dispersión relativa: `sqrt(0.38) = 0.6164`, alrededor del 62% de la de un actor si los tres son independientes.

### Ejercicio práctico 3

Clasifique cada afirmación como observada, calculada, sintética o no respaldada, y dé la razón: (a) los 594 eventos archivados llevan un solo remitente; (b) contando los archivos eliminados, N vale como mucho 1.0408; (c) 14 actores iguales dan una dispersión relativa de 0.2673; (d) una sola persona generó todos los eventos.

> **Respuesta:** (a) Observada: un recuento sobre los archivos fijados. (b) Calculada, a partir de un recuento observado y de un supuesto de peor caso. (c) Sintética: vale para actores imaginarios e independientes. (d) No respaldada: `sender` nombra la cuenta que desencadenó una ejecución; ningún campo registra la persona, la sesión o el agente que hay detrás.

## 3. Un segundo registro: los autores de los commits

**Observado**, con comandos de git que solo leen commits y árboles: 1,599 commits conducen al commit fijado, con **2** cadenas de autor, *autor A* con 860 y *autor B* con 739 (*author A* y *author B* en los datos). **Calculado:**

| Registro | Una identidad es | Identidades | Mayor proporción | H | N |
|---|---|---|---|---|---|
| Disparadores archivados | el `sender` | 1 | 100% | 1 | 1 |
| Disparadores archivados más los 12 archivos eliminados, cada uno de un remitente nuevo (supuesto) | el `sender` | 13 | 98.02% | 0.960821 | 1.0408 |
| Commits | la cadena de autor | 2 | 53.78% | 0.502863 | 1.9886 |
| Commits | la dirección del autor | 3 | 46.22% | 0.387065 | 2.5835 |
| Commits sin los 613 que llevan el asunto de los disparadores | la cadena de autor | 2 | 87.22% | 0.777082 | 1.2869 |

N = 1.99 dice «dos actores del mismo peso». Cuatro propiedades del registro dicen otra cosa; cada una es un límite del instrumento, no un juicio sobre el trabajo de nadie.

- **Un autor es una cadena configurada.** El autor B es el nombre que [cuatro flujos de trabajo configuran antes de hacer un commit](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L85). 613 de sus 739 commits llevan el asunto del flujo de trabajo de los disparadores, uno por archivo de disparador. Sin ellos, 860 frente a 126 dan N = 1.2869 (una lectura elegida después de ver los recuentos).
- **Un colaborador, varios identificadores.** El autor A hace commits con dos direcciones (622 y 238). Git registra quién escribió un cambio (el autor) y quién lo registró (el *committer*): una cadena de *committer* que nunca figura como autor, con una dirección *no-reply* en el dominio de la plataforma de alojamiento, creó 215 de los 238, lo que es compatible con commits hechos en la propia plataforma. Contar direcciones da tres «autores» y N = 2.5835; el `.mailmap` del repositorio, que hace corresponder direcciones con identidades, fusiona las dos.
- **Un identificador, varios colaboradores.** 615 de los 860 commits del autor A (71.51%) llevan un [*trailer*](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors) `Co-authored-by` (una línea de coautoría al final del mensaje): 620 líneas, 610 con una dirección *no-reply* de un mismo dominio, 4 con un nombre terminado en `[bot]`, 4 que nombran a la propia cuenta A. Los recuentos por autor ignoran los *trailers*.
- **Fusiones *squash*.** 279 asuntos terminan con el número de una *pull request*, una solicitud de integración (9 son commits de fusión, no *squash*), y esa cadena de *committer* creó 228 de esos commits. Una fusión *squash* [combina todos los commits de una *pull request* en un único commit](https://docs.github.com/en/pull-requests/reference/pull-request-merges), con un solo campo de autor.

### Ejercicio práctico 4

Calcule H y N para los autores de los commits (860 y 739) y, después, sin los 613 commits que llevan el asunto del flujo de trabajo de los disparadores. ¿Cuál es el número correcto?

> **Respuesta:** `H = (860² + 739²) / 1,599² = 1,285,721 / 2,556,801 = 0.502863` y `N = 1.9886`. Sin los 613, al autor B le quedan `739 − 613 = 126`: `H = (860² + 126²) / 986² = 755,476 / 972,196 = 0.777082` y `N = 1.2869`. Ninguno es «el» número: N mide etiquetas según una regla de recuento. Indique la regla junto con él, y fíjela antes de mirar los datos.

## 4. Lo que respalda un conjunto de uno

Todos los eventos con un remitente legible se desencadenaron a través de una sola cuenta, en un solo repositorio; los commits llegan con una cadena de autor principal y una identidad de flujo de trabajo. Estos registros describen el ritmo de trabajo de una cuenta. Las ráfagas de [PSY-008](psy-008-bursts-are-not-rates.es.md) y la concentración de PSY-009 son propiedades de ese ritmo, no leyes sobre una población de agentes: no hay ninguna población registrada.

**La objeción más fuerte a esta lectura** es que el instrumento hacía probable la uniformidad: `sender` registra quién desencadenó una ejecución, en un solo repositorio, para tres tipos de evento. Una persona que trabajara sola produciría este registro; también lo producirían muchas sesiones de agentes que actuaran con las credenciales del mantenedor. El flujo de trabajo subió (*push*) 613 commits con el autor B, y sin embargo solo se escribieron en total 214 disparadores `push`: si cada ejecución iniciada por un *push* hubiera dejado uno en el historial, al menos 399 de esos *push* no iniciaron ninguna. Más tarde, el commit [`eb230fb`](https://github.com/GuitarAlchemist/Demerzel/commit/eb230fb8d66c48b39a0b01eac99a738791f59e9f) pasó a hacer sus *push* «to master over a write deploy key, not GITHUB_TOKEN» (a master mediante una clave de despliegue con permiso de escritura, no con GITHUB_TOKEN); los *push* hechos con ese token no inician ninguna ejecución, como [documenta](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) GitHub. **Este registro no permite distinguir a un solo actor de muchos agentes detrás de una sola cuenta.** Los *trailers* de la sección 3 apuntan a la segunda posibilidad, pero no permiten contar esos agentes; leer los 12 archivos eliminados solo zanjaría si existe una segunda cuenta.

Datos que describirían a muchos actores independientes: un identificador del agente o de la sesión que actúa, en cada evento, escrito por la herramienta que actúa y no deducido de las credenciales; eventos de todos los repositorios; un número efectivo muy superior a 1 (cuentan las proporciones, no las cabezas); y pruebas de independencia (PSY-004). Literatura, no evidencia: en *Foundation and Empire* (*Fundación e Imperio*), de Asimov, el plan se desvía de su curso cuando un solo individuo, el Mulo, queda fuera de la estadística; aquí no hay registrada ninguna multitud de la que destacar.

### Ejercicio práctico 5

Un registro nuevo etiqueta cada evento con un identificador de *persona*: 1,400 eventos, una *persona* con 1,010 y otras trece con 30 cada una. El criterio se fijó de antemano: para hablar de un agregado de «unos 14 actores», N debe valer al menos 10. (a) Decida. (b) Decida de nuevo si las trece duplican su producción. (c) ¿Qué quedaría por demostrar si N llegara a superar el criterio?

> **Respuesta:** (a) `H = (1,010² + 13 × 30²) / 1,400² = 1,031,800 / 1,960,000 = 0.526429` y `N = 1.8996`: no. (b) `H = (1,010² + 13 × 60²) / 1,790² = 1,066,900 / 3,204,100 = 0.332980` y `N = 3.0032`: sigue siendo no; catorce *personas* iguales darían 14. (c) Que un identificador de *persona* corresponde a un decisor distinto, y no a una etiqueta sobre un mismo modelo que lee un mismo contexto, y que las decisiones de las *personas* no están fuertemente correlacionadas (PSY-004). El registro es imaginario.

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los archivos enlazados o nombrados más arriba y los 1,599 commits que conducen al commit fijado. `extract.py` se detiene si un valor fijado difiere.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-024/extract.py`, y después `analyze.py`; `--check` compara una ejecución nueva con [`results.json`](../../../fixtures/psychohistory/psy-024/results.json). El [README](../../../fixtures/psychohistory/psy-024/README.md) da la regla de etiquetado, los comandos de git y las comprobaciones.

**Referencias de método.** Simpson, E. H. (1949), «Measurement of Diversity», *Nature* 163, 688 (la suma de los cuadrados de las proporciones). Laakso, M., y Taagepera, R. (1979), «'Effective' Number of Parties: A Measure with Application to West Europe», *Comparative Political Studies* 12(1), 3–27 (N = 1/H). Avelino, G., Passos, L., Hora, A., y Valente, M. T. (2016), «A Novel Approach for Estimating Truck Factors», *24th IEEE International Conference on Program Comprehension*, 1–10.

**No realizado.** No se leyó ningún archivo eliminado. No se asoció ningún remitente ni ninguna cadena de autor a una persona, y los dos registros no se cruzaron: un nombre de usuario de la plataforma y una cadena de autor son identificadores distintos. Los nombres de los *trailers* se contaron, no se clasificaron ni se autenticaron. No se leyó ningún otro repositorio, no se observó ninguna decisión de un agente y no se estimó ningún *truck factor*. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** En un clon completo, leer el `sender` de los 12 archivos eliminados: otra cuenta entre ellos cambiaría «un solo remitente» por «N como mucho 1.0408», y nada más. La conclusión solo cambiaría con un registro que identificara al agente que actúa en cada evento: entonces podría calcularse N sobre los agentes.
