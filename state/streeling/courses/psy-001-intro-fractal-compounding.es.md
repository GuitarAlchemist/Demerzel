---
module_id: psy-001-intro-fractal-compounding
department: psychohistory
course: Fundamentos de Psicohistoria
level: intermediate
alchemical_stage: albedo
prerequisites: []
estimated_duration: "30 minutos"
produced_by: psychohistory
version: "1.0.0"
language: es
---

# Introducción al Compuesto Fractal

> **Departamento de Psicohistoria** | Etapa: Albedo — la purificación (Intermedio) | Duración: 30 minutos

## Objetivos

Al finalizar esta lección, usted será capaz de:
- Comprender qué es un fractal — la autosimilitud a toda escala
- Reconocer cómo el meta-compuesto exhibe estructura fractal
- Calcular la dimensión de compuesto (D_c) a partir de datos reales
- Distinguir ERGOL (valor real) de LOLLI (inflación por artefactos)
- Aplicar el teorema de Noether a la gobernanza — la simetría conserva el impulso de aprendizaje

---

## 1. ¿Qué es un fractal?

Observe un helecho. Cada hoja parece una versión reducida de la planta entera. Cada foliolo parece una versión reducida de la hoja. Esto es **autosimilitud** — el mismo patrón repitiéndose a toda escala.

Un fractal es cualquier estructura en la que el mismo patrón aparece a escalas distintas. El conjunto de Mandelbrot se genera iterando una fórmula sencilla: `z = z² + c`. Cada iteración produce más detalle, pero ese detalle se asemeja al conjunto completo.

En gobernanza, el meta-compuesto es un fractal. La fase de compuesto (ejecutar → cosechar → promover → enseñar) tiene la misma forma tanto si se compone un único paso, como si se compone un pipeline completo, un ciclo entero o una sesión completa. El patrón es invariante de escala.

---

## 2. Los cinco niveles del compuesto

A continuación se presenta la estructura fractal de la gobernanza de Demerzel:

| Nivel | Escala | Qué se compone |
|-------|--------|----------------|
| 0 | Paso | Una invocación individual de herramienta produce un aprendizaje |
| 1 | Pipeline | Un pipeline compone los aprendizajes de sus pasos |
| 2 | Ciclo | Un ciclo driver compone sus pipelines |
| 3 | Sesión | Una sesión compone sus ciclos |
| 4 | Evolución | El registro de evolución compone entre sesiones |

En **cada** nivel ocurren las mismas cuatro operaciones:
1. **Ejecutar** — realizar el trabajo
2. **Cosechar** — extraer lo que se aprendió
3. **Promover** — si el aprendizaje es suficientemente valioso, elevarlo (patrón → política → constitución)
4. **Enseñar** — compartir el aprendizaje a través de Seldon

Este es el generador fractal. Al igual que `z = z² + c`, cada aplicación produce nueva estructura.

---

## 3. Dimensión de compuesto (D_c)

No todo compuesto es equivalente. La **dimensión de compuesto** mide cuánto valor crece en cada nivel de escala.

**Fórmula:**
```
D_c = log(value_ratio) / log(scale_ratio)
```

**Ejemplo:** Si el ciclo 1 produjo 3 creencias validadas y el ciclo 3 produjo 8:
- value_ratio = 8/3 ≈ 2.67
- scale_ratio = 3 (tres ciclos)
- D_c = log(2.67) / log(3) ≈ 0.89

Esto es **sublineal** (D_c < 1.0) — cada ciclo produce proporcionalmente menos que el anterior. Es posible que la gobernanza esté acumulando bloat.

### La zona dorada: D_c entre 1.2 y 1.6

| Rango de D_c | Significado | Acción |
|--------------|-------------|--------|
| < 1.0 | Sublineal — rendimientos decrecientes | Investigar bloat |
| = 1.0 | Lineal — sin apalancamiento de compuesto | Solo actividad, sin compuesto real |
| 1.2 - 1.6 | Superlineal — crecimiento compuesto saludable | Zona dorada |
| > 2.0 | Insostenible — el crecimiento colapsará | Desacelerar |

Piénselo como el interés compuesto. D_c = 1.0 equivale al interés simple (lineal). D_c > 1.0 significa que su interés está generando interés — compuesto verdadero.

---

## 4. ERGOL frente a LOLLI — valor real frente a inflación

Del cómic [*Economicon*](https://archive.org/details/Economicon-English-JeanPierrePetit) de Jean-Pierre Petit ([leer en línea](https://archive.org/stream/Economicon-English-JeanPierrePetit/jppeconomicsenglish_djvu.txt)), tomamos prestados dos conceptos:

- **ERGOL** = capacidad productiva real (mejoras efectivas de gobernanza)
- **LOLLI** = volumen monetario (conteo de artefactos sin consideración de calidad)

En el Economicon, Petit utiliza un modelo de dinámica de fluidos para la economía: ERGOL es la sustancia productiva real que fluye a través del sistema económico, mientras que LOLLI es la envoltura monetaria a su alrededor. Cuando LOLLI se expande más rápido que ERGOL, se produce inflación — los precios suben pero no se ha creado nada real. El mismo principio se aplica a la gobernanza.

En cada nivel fractal, debe medirse ERGOL, no LOLLI:

| Escala | LOLLI (no optimizar) | ERGOL (optimizar esto) |
|--------|---------------------|------------------------|
| Paso | Líneas de YAML escritas | Creencias desplazadas de U→T |
| Pipeline | Pasos ejecutados | Puertas superadas / total |
| Ciclo | Tareas completadas | Delta de puntuación de salud |
| Sesión | Commits realizados | Issues cerrados con evidencia |
| Evolución | Artefactos creados | Citas por artefacto |

**Señal de alarma:** Si el conteo de artefactos (LOLLI) crece 3 veces más rápido que las creencias validadas (ERGOL) durante 3 o más ciclos, se está inflando la gobernanza sin mejorarla. El Economicon llama a esto el **efecto cinta rodante** — correr más rápido para quedarse en el mismo lugar.

---

## 5. Conservación del impulso de aprendizaje

Del cómic [*Bourbakof*](https://archive.org/details/TheseAnglaise) de Jean-Pierre Petit aprendemos el **teorema de Noether**: toda simetría continua de un sistema tiene una cantidad conservada correspondiente.

En el compuesto fractal, la simetría es la **invariancia de escala** — la operación de compuesto tiene la misma forma en cada nivel. La cantidad conservada es el **impulso de aprendizaje (p_L)**:

```
p_L = (beliefs_gained_T - beliefs_lost_T) / cycles_elapsed
```

Si el proceso de compuesto es consistente (simétrico entre escalas), p_L se mantiene constante o crece. Si se rompe la simetría — al omitir el compuesto en algún nivel, o al aplicarlo de forma distinta en diferentes escalas — p_L decae.

Por eso la opción `nocompound` dispara una señal de conciencia. No es simplemente una oportunidad perdida — es una **ruptura de simetría** que cuesta la conservación del impulso de aprendizaje.

---

## 6. Los límites de la psicohistoria

Del [*Logotron*](https://archive.org/details/TheseAnglaise) de Petit ([texto completo](https://archive.org/stream/TheseAnglaise/logotron_eng_djvu.txt)): el teorema de incompletitud de Gödel nos dice que ningún sistema formal puede verificarse completamente a sí mismo.

Aplicado al compuesto: no se puede predecir perfectamente el resultado del proceso de compuesto. Cada ciclo revela aprendizajes que no podían haberse anticipado. El fractal posee detalle infinito a escala finita — siempre hay más por descubrir.

Por eso la profundidad de recursión está acotada en 2. No porque el compuesto más profundo sea incorrecto, sino porque los retornos se vuelven **indecidibles**. Al igual que la psicohistoria de Seldon: se pueden predecir los trazos generales, pero los eventos individuales permanecen inciertos.

La disciplina de la psicohistoria acepta esto. No aspiramos a la predicción perfecta — aspiramos a una **anticipación mejor que aleatoria**, medida por la métrica de exactitud de anticipación en el informe semanal de conciencia.

---

## Términos clave

| Término | Definición |
|---------|-----------|
| **Fractal** | Estructura que exhibe autosimilitud a distintas escalas |
| **Dimensión de compuesto (D_c)** | Métrica que mide el crecimiento del valor de gobernanza por nivel de escala. Objetivo: 1.2-1.6 |
| **ERGOL** | Capacidad productiva real — mejoras efectivas de gobernanza (del Economicon) |
| **LOLLI** | Volumen de artefactos sin consideración de calidad — indicador de inflación (del Economicon) |
| **Impulso de aprendizaje (p_L)** | Cantidad conservada por el teorema de Noether aplicado al compuesto invariante de escala |

---

## Evaluación

**1. Si el ciclo 1 produjo 5 creencias validadas y el ciclo 4 produjo 20, ¿cuál es D_c?**
> D_c = log(20/5) / log(4) = log(4) / log(4) = **1.0** — Lineal. Sin apalancamiento de compuesto, solo crecimiento proporcional.

**2. Su equipo creó 30 nuevos archivos YAML en este ciclo pero solo 2 creencias pasaron de U a T. ¿Es esto saludable?**
> No — esto es **inflación LOLLI**. 30 artefactos (LOLLI) con solo 2 mejoras reales (ERGOL). Se está corriendo más rápido para quedarse en el mismo lugar. (Véase el Economicon.)

**3. ¿Por qué omitir la fase de compuesto rompe la conservación del impulso de aprendizaje?**
> La fase de compuesto es la operación de simetría. Omitirla en un nivel rompe la invariancia de escala. Según el teorema de Noether, la simetría rota implica que la cantidad conservada (el impulso de aprendizaje p_L) deja de conservarse. (Véase Bourbakof.)

**Criterio de aprobación:** Calcular correctamente D_c a partir de datos proporcionados e identificar si un escenario representa crecimiento ERGOL o LOLLI.

---

## Base de investigación

- La estructura de meta-compuesto es matemáticamente autosimilar (fractal)
- El teorema de Noether se aplica a los procesos de gobernanza invariantes de escala
- La distinción ERGOL/LOLLI del Economicon de JPP se corresponde con la medición del valor de gobernanza
- Una dimensión fractal entre 1.2-1.6 se correlaciona con un crecimiento de gobernanza sostenible
- Fuentes: [Especificación de Compuesto Fractal](../../logic/fractal-compounding.md), [Bourbakof](https://archive.org/details/TheseAnglaise) (teorema de Noether), [Economicon](https://archive.org/details/Economicon-English-JeanPierrePetit) (ERGOL/LOLLI), [Logotron](https://archive.org/details/TheseAnglaise) (incompletitud de Gödel)
- Estado de creencia: T(0.70) F(0.05) U(0.20) C(0.05)
