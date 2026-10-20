---
module_id: psy-020-goodhart-and-reflexivity
department: psychohistory
course: "Cuando la medida se convierte en objetivo: las citas como indicador sustituto"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "psy-011-measurement-change-or-system-change"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-020
version: "0.1.0"
---

# Cuando la medida se convierte en objetivo: las citas como indicador sustituto

> **Departamento de Psicohistoria** | Intermedio | 40 minutos | Traducción al español del borrador en inglés; revisión de fondo y prueba con aprendices pendientes

## Objetivos y pregunta de proyecto

En este módulo leerá una regla de recuento y dirá lo que no puede ver, calculará el efecto de un archivo añadido sobre los recuentos, dirá cuándo recompensar un indicador sustituto lo degrada y corregirá un pronóstico que mueve su propio objetivo. **Pregunta de proyecto:** la tendencia de calidad cuenta citas con `git grep`; ¿qué le ocurre a un indicador sustituto así cuando los agentes saben que se vigila?

Un *indicador sustituto* (*proxy*) se mide en lugar de un *objetivo* que no puede medirse. [PSY-001](psy-001-intro-fractal-compounding.es.md) contrapone LOLLI, «artifact count without regard to quality» (recuento de artefactos sin atender a su calidad), a ERGOL, «real productive capacity» (capacidad productiva real), y enumera «Citations per artifact» (citas por artefacto) como el ERGOL que hay que optimizar. [PSY-011](psy-011-measurement-change-or-system-change.es.md) se pregunta si el instrumento cambió; aquí está fijo, y la pregunta es qué puede hacerle aquello que se mide. No se ha observado a nadie en el proyecto inflando este recuento: el tema es un mecanismo y el momento en que empieza a actuar.

## 1. Lo que el recuento puede ver

**Observado.** Un *artefacto* de gobernanza (una política, una constitución, un esquema, una habilidad) tiene un registro de evolución que enumera sus *rutas de citación*. El *productor*, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), [define](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) `citation_count` como los «tracked files that mention any of the artifact's citation paths (`git grep -lF`)» (los archivos rastreados que mencionan alguna de las rutas de citación del artefacto), menos los archivos del propio artefacto y [cuatro ubicaciones excluidas](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L43). [La búsqueda](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L80-L82) es la de una cadena literal; [el feeder](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L76) (el «alimentador») copia el resultado en la tendencia de calidad diaria. Una «cita» es un archivo en el que una ruta aparece como texto.

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-020/extract.py) aplica la regla a los 2,062 archivos del commit `4b03838` y escribe [`observed-input.json`](../../../fixtures/psychohistory/psy-020/observed-input.json): 18 registros, 16 artefactos medibles (dos de ellos [marcados como alojados](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23) fuera del repositorio), 19 rutas de citación distintas. **Calculado:** el nuevo recuento coincide con el recuento registrado en 16 de 16 artefactos. En orden decreciente, los recuentos son 65, 47, 45, 44, 29, 29, 23, 17, 15, 14, 13, 6, 6, 5, 1, 0; suman 359, aportados por 200 archivos.

La regla es ciega por dos lados.

- **Mención sin uso.** De los 200 archivos contados, 123 son Markdown y 9 son programas Python, aunque el tipo de un archivo no distingue el uso de la mención; 92 nombran dos o más artefactos. Nueve archivos de cursos, tres lecciones en tres idiomas, aportan 12 de las 359 citas contadas, 8 de ellas procedentes de traducciones.
- **Uso sin mención.** Un artefacto tiene un recuento de 0, del que su [registro](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution/2026-04-30-the-sentinel.evolution.json) dice que «reads as 'nothing uses this spec'» (se lee como «nada usa esta especificación»), y añade: «That is true only inside Demerzel: the metric cannot see sibling repositories.» (eso solo es cierto dentro de Demerzel: la métrica no ve los repositorios hermanos).

En la tendencia, 20 filas tienen un `delta_citations` distinto de cero (enumeradas en [`results.json`](../../../fixtures/psychohistory/psy-020/results.json)): 16 primeros recuentos registrados y cuatro subidas de 2 el 2026-10-03, para `policies / alignment-policy.yaml`, `contracts / galactic-protocol.md` y los dos artefactos que comparten una misma ruta de política. Una subida indica que los archivos cambiaron, no cuáles ni por qué: aquí no se atribuye ninguna causa.

### Ejercicio práctico 1

Sintético (`toy_rule` en [`scenarios.json`](../../../fixtures/psychohistory/psy-020/scenarios.json)). La única ruta de citación de un artefacto es `toy/rule.yaml`. (a) `docs/index.md` enumera la ruta; (b) `scripts/check.py` carga la regla con `os.path.join("toy", "rule.yaml")`; (c) el archivo de la regla nombra su propia ruta; (d) `state/evolution/toy.json` y (e) `notes/archived/2025.md` la nombran; (f) `data/labels.json` escribe `toy / rule.yaml`; (g) una lección y (h) su traducción la nombran. ¿Cuál es el recuento, y está incluido en él el archivo que usa la regla?

> **Respuesta:** El recuento es 3: los archivos a, g y h. El archivo c es del propio artefacto; d y e están excluidos; en b y en f no aparece la cadena literal. Así que b, el único archivo que usa la regla, no se cuenta, mientras que una misma lección cuenta dos veces.

## 2. Un archivo, dieciséis recuentos

**Casos hipotéticos sintéticos sobre recuentos observados.** Ninguno de estos archivos existe; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-020/analyze.py) los añade a los recuentos fijados. Una *relación de orden* dice cuál de dos artefactos tiene el recuento mayor; 16 artefactos forman 120 pares.

| Archivo añadido | Recuentos que suben | Suma | Relaciones de orden que cambian |
|---|---|---|---|
| Un catálogo de las 19 rutas | 16, en 1 cada uno | de 359 a 375 (+4.46%) | 0 de 120 |
| Un archivo que nombra una sola ruta | 1 (2 para la ruta compartida) | 359 + 1 (o + 2) | al menos 1 para 11 de las 19 rutas |

El catálogo no cambia ningún orden, ya que suma el mismo número a todos los recuentos; en una carpeta excluida, o escrito con etiquetas con barras espaciadas, no eleva ninguno. Desplaza el nivel, y con él toda proporción o todo umbral que se calcule a partir de él: el único recuento de 0 pasa a ser 1. Un archivo dirigido apenas mueve la suma y reordena a los vecinos: dos archivos de una sola ruta bastan para que cualquiera de cinco artefactos supere a su vecino inmediatamente superior.

**Una medición externa al *fixture* (la carpeta de datos y scripts que reproduce las cifras de esta lección).** La descripción de la *pull request* [GuitarAlchemist/Demerzel#1217](https://github.com/GuitarAlchemist/Demerzel/pull/1217) registra que, con la regla del productor, los archivos de datos de los dos primeros módulos de este itinerario, que se limitaban a enumerar rutas de artefactos, habrían elevado once de los dieciséis recuentos entre 4 y 6 en la siguiente ejecución nocturna, sobre una punta de rama anterior, `fb6c317`, y ninguno sobre `b938cc3`, una vez que los nombres pasaron a ser etiquetas. Como no puede reproducirse a partir del commit fijado, aquí no sustenta ninguna conclusión; es la razón por la que esta lección escribe sus etiquetas con barras espaciadas.

### Ejercicio práctico 2

A partir de los dieciséis recuentos: (a) añada un catálogo; dé la nueva suma y su variación relativa. (b) En su lugar, añada un archivo que nombre solo la ruta del artefacto que tiene 44. ¿Qué relaciones de orden cambian?

> **Respuesta:** (a) `359 + 16 = 375`, `16 / 359 = 4.46%`; no cambia ninguna relación de orden (0 de 120). (b) 44 pasa a 45 y empata con el artefacto que tiene 45: una relación pasa de «por detrás» a «empate».

## 3. Cuando se recompensa el indicador sustituto

Goodhart (1975), a propósito de los objetivos monetarios, tal como lo citan Manheim y Garrabrant (2018): «any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes» (toda regularidad estadística observada tenderá a desmoronarse en cuanto se ejerza presión sobre ella con fines de control). Campbell (1979), a propósito de los indicadores sociales, citado también allí: «The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures and the more apt it will be to distort and corrupt the social processes it is intended to monitor.» (cuanto más se usa un indicador social cuantitativo para tomar decisiones sociales, más expuesto queda a presiones que lo corrompen y más tiende a distorsionar y corromper los procesos sociales que debía vigilar). El título sigue a Strathern (1997): «When a measure becomes a target, it ceases to be a good measure.» (cuando una medida se convierte en objetivo, deja de ser una buena medida). Cada una nombra una condición, la presión o el uso para decidir, no un destino.

**Observado: ¿se usa el recuento para tomar decisiones?** Sobre el papel. La [política anti-LOLLI](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml) calcula [`ratio_n = LOLLI_n / max(ERGOL_n, 1)`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L69), cuenta como ERGOL el [«citation_count delta»](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L305) y [congela la creación de artefactos](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L97) cuando el cociente se mantiene por encima de 3.0 durante 3 ciclos consecutivos; su [archivo de historial](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json) contiene un solo ciclo, con fecha 2026-03-23. Una [regla de detección](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56) juzga también los recuentos: «If the top 20% of governance artifacts account for more than 60% of citations, a power law is present. This is healthy» (hay una ley de potencia, y eso es saludable). `policies / compounding-metrics-policy.yaml` la repite, toma sus datos del `citation_count` de los registros (líneas 117–122) y fija para esa proporción un «target» (objetivo) de «0.60–0.85» (líneas 219–222). Con los recuentos introducidos a mano antes del 2026-09-13, [PSY-007](psy-007-power-law-or-not.es.md) llega al veredicto opuesto, que cambió cuando cambió el instrumento. **Esta muestra no permite decir si el recuento orienta hoy alguna decisión.**

**Sintético: lo que haría la presión.** Cada agente supuesto dedica una unidad de esfuerzo al trabajo (valor `a`, que se refleja uno a uno en el indicador sustituto) o a la inflación (`g` puntos de indicador, ningún valor).

```text
indicador  = valor + inflación + error
recompensa = (1 - w) x valor + w x indicador
```

El trabajo rinde `a` sea cual sea `w`, y la inflación rinde `w x g`, así que un agente infla cuando `w x g > a`. `scenarios.json` supone `a` y `g` de 1 a 10 y un error de -1, 0 o 1: 300 casos equiprobables, enumerados de forma exacta.

| Peso `w` del indicador en la recompensa | 0 | 1/2 | 1 |
|---|---|---|---|
| Indicador medio | 5.50 | 6.60 | 7.15 |
| Valor real medio | 5.50 | 5.10 | 3.85 |
| Correlación entre indicador y valor | 0.9619 | 0.4374 | 0.2785 |

De `w = 0` a `w = 1`, el indicador medio sube un 30% mientras el valor medio baja un 30%: el indicador mejora a medida que se reduce aquello que representaba. En el modelo, cuanto más se optimiza el indicador, menos dice sobre el valor. El efecto necesita las tres cosas: una recompensa sobre el indicador, una manera de inflarlo y un trabajo que rinda menos que inflarlo.

### Ejercicio práctico 3

La regla de detección, aplicada a los 18 recuentos registrados (los dieciséis anteriores, más 55 y 0 fuera del repositorio; suma 414). El 20% de 18 artefactos es 3.6; tome los 4 primeros. (a) ¿Considera la regla saludables los recuentos fijados? (b) Sintético: cada archivo añadido nombra las rutas de citación de los tres artefactos medibles que hay entre los 4 primeros. ¿Cuántos archivos hacen que la proporción supere el 60%? (c) ¿Qué hace en cambio un único catálogo de todas las rutas? (d) ¿Qué dice (b) sobre el veredicto?

> **Respuesta:** (a) `65 + 55 + 47 + 45 = 212`, y `212 / 414 = 51.21%`: no (los 3 primeros reúnen el 40.34%). (b) Cada archivo suma 3 a los dos términos de la proporción: `212 + 3n > 0.6 x (414 + 3n)` da `1.2n > 36.4`, así que `n = 31`, y `305 / 507 = 60.16%` (30 archivos dan el 59.92%). (c) Eleva en 1 los dieciséis recuentos medibles: `215 / 430 = 50.00%`, aún más lejos de «saludable». (d) Treinta y un archivos de menciones, sin ningún cambio en el uso, invertirían el veredicto: la regla juzga dónde están escritas las rutas. No se ha observado a nadie escribiendo archivos así.

### Ejercicio práctico 4

Sintético. El trabajo de un agente produce 3 puntos de valor; la inflación produciría 8 puntos de indicador. (a) Para `w` = 0, 1/2 y 1, ¿trabaja o infla, y cuáles son su valor y su indicador (error 0)? (b) ¿Por encima de qué peso cambia de conducta?

> **Respuesta:** (a) Infla cuando `w x 8 > 3`. Con 0 trabaja: valor 3, indicador 3. Con 1/2, `4 > 3`: infla, valor 0, indicador 8; con 1, `8 > 3`, lo mismo. (b) `w x 8 > 3` se cumple para `w > 3 / 8 = 0.375`. El agente es supuesto, no observado.

## 4. Pronósticos que mueven su propio objetivo

Un pronóstico es *reflexivo* cuando publicarlo cambia el resultado que predice. Aquí, uno de los canales es mecánico: un pronóstico del recuento de un artefacto, guardado mediante un commit en un archivo que nombra la ruta del artefacto, es un archivo contado.

```text
resultado = línea de base + self_mentions + reacción x (pronóstico - línea de base)
```

**Sintético, a partir de un recuento observado.** `policies / alignment-policy.yaml` tiene un recuento de 44. Pronostique 44 fuera del repositorio, sin reacción, y el pronóstico se cumple; guárdelo con un commit en un archivo que nombre la ruta y falla por construcción: el resultado es 45. Si además los lectores añaden media mención por cada punto que el pronóstico supere la línea de base (reacción 1/2), el pronóstico que se cumple es 46, y volver a publicar el último resultado se desvía sucesivamente en 1, 0.5, 0.25, 0.125. Grunberg y Modigliani (1954) dieron condiciones en las que un pronóstico público puede seguir siendo correcto.

### Ejercicio práctico 5

Sintético. Su pronóstico del recuento que hoy vale 44 se guardará con un commit en un archivo que nombra la ruta del artefacto. (a) Sin reacción, ¿qué ocurre con un pronóstico de 44? (b) Con una reacción de 1/2, ¿qué pronóstico es igual a su resultado? (c) ¿Cómo publicaría usted para eliminar el efecto, y con qué criterio?

> **Respuesta:** (a) El resultado es `44 + 1 = 45`: un error de 1 causado por el propio pronóstico. (b) `f = 44 + 1 + (f - 44) / 2` da `f / 2 = 23`, así que `f = 46`. (c) Escriba el artefacto como una etiqueta con barras espaciadas, o publique fuera de los archivos rastreados: `self_mentions` pasa a 0 y 44 es su propio resultado. Criterio: un pronóstico no debe ser una entrada de aquello que pronostica.

**La objeción más fuerte a la lectura de esta lección** es que reprocha al recuento algo que su productor nunca afirmó: el docstring promete menciones, y un archivo que nombra una política suele tener un motivo para hacerlo. El fixture no clasifica ningún archivo como uso o como mención, así que **esta muestra no permite distinguir un recuento honesto de uno inflado**, y nada en ella muestra que se haya inflado ningún recuento. Para zanjarlo, clasifique a mano los 200 archivos contados como uso (el archivo carga, prueba o hace cumplir el artefacto) o mención, y compruebe si el orden de los artefactos se mantiene.

**Qué detectaría la inflación.** Hoy pueden calcularse dos señales: los recuentos aportados por cada archivo (16 para un catálogo, 7 como máximo en el commit fijado) y la proporción procedente de archivos que repiten otro, como las traducciones (8 de 359, el 2.23%).

## Fuentes, límites y próxima comprobación

**Observado, fijado en Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** los archivos enlazados o nombrados más arriba y la tendencia de calidad. El [README](../../../fixtures/psychohistory/psy-020/README.md) del fixture da los comandos, las autocomprobaciones y los controles negativos.

**Referencias de método.** Goodhart, C. A. E. (1975), «Problems of Monetary Management: The U.K. Experience», *Papers in Monetary Economics*, vol. I, Reserve Bank of Australia; reimpreso en Goodhart (1984), *Monetary Theory and Practice: The UK Experience*, Macmillan, 91–121. Campbell, D. T. (1979), «Assessing the Impact of Planned Social Change», *Evaluation and Program Planning* 2(1), 67–90. Strathern, M. (1997), «'Improving Ratings': Audit in the British University System», *European Review* 5(3), 305–321. Manheim, D., y Garrabrant, S. (2018), «Categorizing Variants of Goodhart's Law», [arXiv:1803.04585](https://arxiv.org/abs/1803.04585). Grunberg, E., y Modigliani, F. (1954), «The Predictability of Social Events», *Journal of Political Economy* 62(6), 465–478.

**No realizado.** No se observó el esfuerzo ni el motivo de ningún agente; los dos modelos son supuestos. Los 200 archivos contados no se clasificaron. Las frases de Goodhart y de Campbell no se cotejaron con los textos de 1975 y 1979; la de Strathern se leyó en la página 308 de un escaneo alojado en gwern.net. Ninguna persona ha revisado el fondo de esta lección y ningún aprendiz la ha probado.

**Próxima comprobación.** La clasificación a mano descrita más arriba. Si el orden por uso coincide con el orden por recuento, la conclusión se estrecha de «el recuento no distingue el uso de la mención» a «hoy no necesita hacerlo»; seguiría sin decir nada sobre un recuento que se ha convertido en recompensa.
