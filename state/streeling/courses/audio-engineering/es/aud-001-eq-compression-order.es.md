---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Fundamentos de compresión — ratio, threshold, attack, release"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ y compresión: por qué importa el orden en la cadena de señal

> **Departamento de Ingeniería de Audio** | Nivel: Intermedio | Duración: 35 minutos

## Objetivos
- Entender las diferencias técnicas entre las cadenas Comp→EQ y EQ→Comp
- Identificar cuándo cada orden produce mejores resultados en voces
- Aplicar la técnica sándwich EQ→Comp→EQ para máximo control
- Reconocer artefactos de compresión dependientes de frecuencia y cómo prevenirlos

---

## 1. La pregunta central

¿Importa si comprimes antes o después del EQ? **Sí** — de forma medible. El orden cambia cómo reacciona el compresor al contenido frecuencial, lo que afecta la naturalidad de la dinámica y la claridad del tono.

La razón es simple: un compresor responde al *nivel*. Si ciertas frecuencias son más fuertes (por ejemplo, el efecto de proximidad reforzando 100-200 Hz, o la sibilancia con picos en 4-10 kHz), el compresor reacciona a *esas frecuencias*, no solo a la interpretación vocal general.

---

## 2. Compresión antes de EQ (Comp→EQ)

```
Voz → [Compresor] → [EQ] → Bus de mezcla
```

**Qué ocurre:**
- El compresor recibe la señal cruda — incluyendo frecuencias problemáticas
- Si la sibilancia es fuerte (picos en 4-10 kHz), puede disparar la compresión en esos transitorios
- El compresor "bombea" en frecuencias problemáticas en vez de controlar la dinámica general
- El EQ posterior moldea la señal ya comprimida

**Cuándo usarlo:**
- Cuando la voz está bien grabada con mínimos problemas de frecuencia
- Cuando quieres que el compresor reaccione a la señal completa y natural
- Cuando usas compresión suave (ratio 2:1, ataque lento) para "cohesión"

**Riesgo:** Bombeo dependiente de frecuencia. El compresor no sabe que no quieres que reaccione al abultamiento de 200 Hz por proximidad — solo ve nivel.

---

## 3. EQ antes de compresión (EQ→Comp)

```
Voz → [EQ] → [Compresor] → Bus de mezcla
```

**Qué ocurre:**
- El EQ correctivo elimina problemas primero: cortar proximidad a 200 Hz, atenuar sibilancia a 6 kHz
- El compresor recibe una señal más limpia y equilibrada
- La compresión responde a la *interpretación musical*, no a artefactos de frecuencia
- Resultado: compresión más natural y transparente

**Cuándo usarlo:**
- Cuando la voz tiene problemas de frecuencia notables (proximidad, resonancias del cuarto, aspereza)
- Cuando quieres que el compresor responda a la dinámica, no a picos de frecuencia
- Cuando la calidad de grabación es variable

**Esta es generalmente la opción más segura por defecto** — corrige los problemas de frecuencia antes de pedirle al compresor que maneje la dinámica.

---

## 4. El sándwich: EQ→Comp→EQ

```
Voz → [EQ correctivo] → [Compresor] → [EQ tonal] → Bus de mezcla
```

Este es el estándar profesional por una buena razón:

1. **Primer EQ (correctivo):** Filtro pasa-altos a 80-100 Hz, corte de barro en 200-300 Hz, muescas en resonancias del cuarto. Esto es quirúrgico — estás eliminando problemas, no moldeando el tono.

2. **Compresor:** Ahora reacciona a una señal limpia. Configura ratio (3:1-4:1 típico para voces), threshold para captar ~6 dB de reducción de ganancia, ataque medio (10-30ms) para preservar transitorios, release medio (50-100ms).

3. **Segundo EQ (tonal):** Ahora moldea el sonido de forma creativa. Realza aire en 10-12 kHz, agrega presencia en 3-5 kHz, calienta los medios-bajos. Este EQ va después de la compresión, así que tus realces no disparan el compresor.

**Por qué funciona:** Separacion de responsabilidades. El EQ correctivo previene artefactos del compresor. El compresor maneja la dinámica sobre una señal limpia. El EQ tonal moldea el carácter final sin afectar la dinámica.

---

## 5. Artefactos dependientes de frecuencia a vigilar

| Problema | Causa | Solución |
|----------|-------|----------|
| Bombeo en plosivas | Ráfagas de baja frecuencia disparando el compresor | Filtro pasa-altos antes del compresor (EQ→Comp) |
| Sibilancia amplificada | El compresor reduce el cuerpo, la sibilancia permanece | De-esser antes del compresor, o corte de EQ a 6 kHz primero |
| Sonido opaco tras compresión | Ataque rápido aplastando transitorios | Ataque lento (15-30ms), o compresión paralela |
| Tono inconsistente | El compresor reacciona diferente a secciones suaves vs fuertes | Usar 2 etapas de compresión suave en vez de 1 etapa pesada |

---

## 6. EQ dinámico: la alternativa moderna

El EQ dinámico combina EQ y compresión en un solo procesador. Cada banda de EQ solo se activa cuando la frecuencia supera un umbral — como un compresor que solo trabaja en frecuencias específicas.

**Caso de uso:** Sibilancia que varía a lo largo de la interpretación. Un corte estático a 6 kHz apagaría toda la voz, pero un corte de EQ dinámico solo se activa cuando la sibilancia supera el umbral.

Esto no reemplaza la pregunta Comp→EQ — es una herramienta especializada para problemas de dinámica dependientes de frecuencia.

---

## Ejercicio práctico

### Ejercicio 1: A/B del orden
Toma una grabación vocal. Configura dos cadenas paralelas:
- Cadena A: Compresor (4:1, -6 dB GR) → EQ (realce 3 kHz +3 dB, corte 250 Hz -4 dB)
- Cadena B: Mismo EQ → Mismo Compresor

Escucha ambas. ¿Dónde notas la diferencia? Concéntrate en:
- Consistencia de baja frecuencia (manejo del efecto de proximidad)
- Nivel de sibilancia
- "Naturalidad" general de la compresión

### Ejercicio 2: Construye un sándwich
Configura: Filtro pasa-altos a 100 Hz + corte a 250 Hz → Compresor (3:1) → Realce de presencia a 4 kHz + Aire a 12 kHz. Compara contra una cadena simple de EQ-luego-comprimir.

---

## Puntos clave
- **El orden importa** — el compresor responde a las frecuencias que sean más fuertes en la entrada
- **EQ→Comp es la opción segura por defecto** — corrige problemas antes de comprimir para resultados más naturales
- **El sándwich EQ→Comp→EQ es el estándar profesional** — correctivo primero, tonal al final
- **No hay un orden universalmente "correcto"** — depende de la grabación, el género y la intención
- **El EQ dinámico** es una herramienta moderna para problemas de dinámica dependientes de frecuencia
- El objetivo siempre es: controlar la dinámica sin destruir el carácter natural de la interpretación

## Lecturas complementarias
- Departamento de Física: Acústica — frecuencia, amplitud y relaciones armónicas
- Departamento de Música: Cómo la percepción del timbre afecta las decisiones de mezcla
- Departamento de Ciencias de la Computación: Algoritmos DSP detrás del EQ y la compresión
- AES (Audio Engineering Society): Estándares de medición de sonoridad (ITU-R BS.1770)

---
*Producido por el Ciclo de Investigación Seldon audio-engineering-2026-03-23-001 el 2026-03-23.*
*Pregunta de investigación: El orden de compresión antes de EQ versus EQ antes de compresión produce resultados mediblemente diferentes en voces?*
*Creencia: T (confianza: 0.80)*
