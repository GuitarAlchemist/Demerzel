---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Fundamentos de compresion — ratio, threshold, attack, release"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ y compresion: por que importa el orden en la cadena de senal

> **Departamento de Ingenieria de Audio** | Nivel: Intermedio | Duracion: 35 minutos

## Objetivos
- Entender las diferencias tecnicas entre las cadenas Comp→EQ y EQ→Comp
- Identificar cuando cada orden produce mejores resultados en voces
- Aplicar la tecnica sandwich EQ→Comp→EQ para maximo control
- Reconocer artefactos de compresion dependientes de frecuencia y como prevenirlos

---

## 1. La pregunta central

Importa si comprimes antes o despues del EQ? **Si** — de forma medible. El orden cambia como reacciona el compresor al contenido frecuencial, lo que afecta la naturalidad de la dinamica y la claridad del tono.

La razon es simple: un compresor responde al *nivel*. Si ciertas frecuencias son mas fuertes (por ejemplo, el efecto de proximidad reforzando 100-200 Hz, o la sibilancia con picos en 4-10 kHz), el compresor reacciona a *esas frecuencias*, no solo a la interpretacion vocal general.

---

## 2. Compresion antes de EQ (Comp→EQ)

```
Voz → [Compresor] → [EQ] → Bus de mezcla
```

**Que ocurre:**
- El compresor recibe la senal cruda — incluyendo frecuencias problematicas
- Si la sibilancia es fuerte (picos en 4-10 kHz), puede disparar la compresion en esos transitorios
- El compresor "bombea" en frecuencias problematicas en vez de controlar la dinamica general
- El EQ posterior moldea la senal ya comprimida

**Cuando usarlo:**
- Cuando la voz esta bien grabada con minimos problemas de frecuencia
- Cuando quieres que el compresor reaccione a la senal completa y natural
- Cuando usas compresion suave (ratio 2:1, ataque lento) para "cohesion"

**Riesgo:** Bombeo dependiente de frecuencia. El compresor no sabe que no quieres que reaccione al abultamiento de 200 Hz por proximidad — solo ve nivel.

---

## 3. EQ antes de compresion (EQ→Comp)

```
Voz → [EQ] → [Compresor] → Bus de mezcla
```

**Que ocurre:**
- El EQ correctivo elimina problemas primero: cortar proximidad a 200 Hz, atenuar sibilancia a 6 kHz
- El compresor recibe una senal mas limpia y equilibrada
- La compresion responde a la *interpretacion musical*, no a artefactos de frecuencia
- Resultado: compresion mas natural y transparente

**Cuando usarlo:**
- Cuando la voz tiene problemas de frecuencia notables (proximidad, resonancias del cuarto, aspereza)
- Cuando quieres que el compresor responda a la dinamica, no a picos de frecuencia
- Cuando la calidad de grabacion es variable

**Esta es generalmente la opcion mas segura por defecto** — corrige los problemas de frecuencia antes de pedirle al compresor que maneje la dinamica.

---

## 4. El sandwich: EQ→Comp→EQ

```
Voz → [EQ correctivo] → [Compresor] → [EQ tonal] → Bus de mezcla
```

Este es el estandar profesional por una buena razon:

1. **Primer EQ (correctivo):** Filtro pasa-altos a 80-100 Hz, corte de barro en 200-300 Hz, muescas en resonancias del cuarto. Esto es quirurgico — estas eliminando problemas, no moldeando el tono.

2. **Compresor:** Ahora reacciona a una senal limpia. Configura ratio (3:1-4:1 tipico para voces), threshold para captar ~6 dB de reduccion de ganancia, ataque medio (10-30ms) para preservar transitorios, release medio (50-100ms).

3. **Segundo EQ (tonal):** Ahora moldea el sonido de forma creativa. Realza aire en 10-12 kHz, agrega presencia en 3-5 kHz, calienta los medios-bajos. Este EQ va despues de la compresion, asi que tus realces no disparan el compresor.

**Por que funciona:** Separacion de responsabilidades. El EQ correctivo previene artefactos del compresor. El compresor maneja la dinamica sobre una senal limpia. El EQ tonal moldea el caracter final sin afectar la dinamica.

---

## 5. Artefactos dependientes de frecuencia a vigilar

| Problema | Causa | Solucion |
|----------|-------|----------|
| Bombeo en plosivas | Rafagas de baja frecuencia disparando el compresor | Filtro pasa-altos antes del compresor (EQ→Comp) |
| Sibilancia amplificada | El compresor reduce el cuerpo, la sibilancia permanece | De-esser antes del compresor, o corte de EQ a 6 kHz primero |
| Sonido opaco tras compresion | Ataque rapido aplastando transitorios | Ataque lento (15-30ms), o compresion paralela |
| Tono inconsistente | El compresor reacciona diferente a secciones suaves vs fuertes | Usar 2 etapas de compresion suave en vez de 1 etapa pesada |

---

## 6. EQ dinamico: la alternativa moderna

El EQ dinamico combina EQ y compresion en un solo procesador. Cada banda de EQ solo se activa cuando la frecuencia supera un umbral — como un compresor que solo trabaja en frecuencias especificas.

**Caso de uso:** Sibilancia que varia a lo largo de la interpretacion. Un corte estatico a 6 kHz apagaria toda la voz, pero un corte de EQ dinamico solo se activa cuando la sibilancia supera el umbral.

Esto no reemplaza la pregunta Comp→EQ — es una herramienta especializada para problemas de dinamica dependientes de frecuencia.

---

## Ejercicio practico

### Ejercicio 1: A/B del orden
Toma una grabacion vocal. Configura dos cadenas paralelas:
- Cadena A: Compresor (4:1, -6 dB GR) → EQ (realce 3 kHz +3 dB, corte 250 Hz -4 dB)
- Cadena B: Mismo EQ → Mismo Compresor

Escucha ambas. Donde notas la diferencia? Concentrate en:
- Consistencia de baja frecuencia (manejo del efecto de proximidad)
- Nivel de sibilancia
- "Naturalidad" general de la compresion

### Ejercicio 2: Construye un sandwich
Configura: Filtro pasa-altos a 100 Hz + corte a 250 Hz → Compresor (3:1) → Realce de presencia a 4 kHz + Aire a 12 kHz. Compara contra una cadena simple de EQ-luego-comprimir.

---

## Puntos clave
- **El orden importa** — el compresor responde a las frecuencias que sean mas fuertes en la entrada
- **EQ→Comp es la opcion segura por defecto** — corrige problemas antes de comprimir para resultados mas naturales
- **El sandwich EQ→Comp→EQ es el estandar profesional** — correctivo primero, tonal al final
- **No hay un orden universalmente "correcto"** — depende de la grabacion, el genero y la intencion
- **El EQ dinamico** es una herramienta moderna para problemas de dinamica dependientes de frecuencia
- El objetivo siempre es: controlar la dinamica sin destruir el caracter natural de la interpretacion

## Lecturas complementarias
- Departamento de Fisica: Acustica — frecuencia, amplitud y relaciones armonicas
- Departamento de Musica: Como la percepcion del timbre afecta las decisiones de mezcla
- Departamento de Ciencias de la Computacion: Algoritmos DSP detras del EQ y la compresion
- AES (Audio Engineering Society): Estandares de medicion de sonoridad (ITU-R BS.1770)

---
*Producido por el Ciclo de Investigacion Seldon audio-engineering-2026-03-23-001 el 2026-03-23.*
*Pregunta de investigacion: El orden de compresion antes de EQ versus EQ antes de compresion produce resultados mediblemente diferentes en voces?*
*Creencia: T (confianza: 0.80)*
