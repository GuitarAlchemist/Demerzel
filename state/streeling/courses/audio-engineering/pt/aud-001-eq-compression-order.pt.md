---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Fundamentos de compressão — ratio, threshold, attack, release"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ e Compressão: Por Que a Ordem do Sinal Importa

> **Departamento de Engenharia de Áudio** | Nível: Intermediário | Duração: 35 minutos

## Objetivos
- Compreender as diferenças técnicas entre as cadeias de sinal Comp→EQ e EQ→Comp
- Identificar quando cada ordem produz melhores resultados em vocais
- Aplicar a técnica do sanduíche EQ→Comp→EQ para máximo controle
- Reconhecer artefatos de compressão dependentes de frequência e como preveni-los

---

## 1. A Pergunta Central

Faz diferença comprimir antes ou depois de equalizar? **Sim** — de forma mensurável. A ordem muda como o compressor reage ao conteúdo de frequência, o que afeta a naturalidade da dinâmica e a clareza do timbre.

O motivo é simples: um compressor responde ao *nível*. Se certas frequências estão mais altas (ex.: efeito de proximidade reforçando 100-200 Hz, ou sibilância com pico em 4-10 kHz), o compressor reage a *essas frequências*, não apenas à performance vocal como um todo.

---

## 2. Compressão Antes do EQ (Comp→EQ)

```
Vocal → [Compressor] → [EQ] → Bus de Mixagem
```

**O que acontece:**
- O compressor recebe o sinal bruto — incluindo frequências problemáticas
- Se a sibilância é alta (picos de 4-10 kHz), ela pode acionar a compressão nesses transientes
- O compressor "bombeia" nas frequências problemáticas em vez de controlar a dinâmica geral
- O EQ depois molda o sinal já comprimido

**Quando usar:**
- Quando o vocal está bem gravado, com mínimos problemas de frequência
- Quando você quer que o compressor reaja ao sinal completo e natural
- Quando usa compressão suave (ratio 2:1, attack lento) para "cola"

**Risco:** Bombeamento dependente de frequência. O compressor não sabe que você não quer que ele reaja ao acúmulo de 200 Hz — ele só enxerga nível.

---

## 3. EQ Antes da Compressão (EQ→Comp)

```
Vocal → [EQ] → [Compressor] → Bus de Mixagem
```

**O que acontece:**
- O EQ corretivo remove problemas primeiro: corta proximidade em 200 Hz, doma sibilância em 6 kHz
- O compressor recebe um sinal mais limpo e equilibrado
- A compressão responde à *performance musical*, não a artefatos de frequência
- Resultado: compressão mais natural e transparente

**Quando usar:**
- Quando o vocal tem problemas de frequência perceptíveis (proximidade, ressonância de sala, aspereza)
- Quando você quer que o compressor responda à dinâmica, não a picos de frequência
- Quando a qualidade da gravação é variável

**Este é geralmente o padrão mais seguro** — corrija os problemas de frequência antes de pedir ao compressor para gerenciar a dinâmica.

---

## 4. O Sanduíche: EQ→Comp→EQ

```
Vocal → [EQ Corretivo] → [Compressor] → [EQ Tonal] → Bus de Mixagem
```

Este é o padrão profissional por um bom motivo:

1. **Primeiro EQ (corretivo):** Filtro passa-alta em 80-100 Hz, corte de lama em 200-300 Hz, notch em ressonâncias da sala. Isto é cirúrgico — você está removendo problemas, não moldando timbre.

2. **Compressor:** Agora reage a um sinal limpo. Ajuste ratio (3:1 a 4:1 é típico para vocais), threshold para capturar ~6 dB de redução de ganho, attack médio (10-30ms) para preservar transientes, release médio (50-100ms).

3. **Segundo EQ (tonal):** Agora molde o som criativamente. Reforce o "ar" em 10-12 kHz, adicione presença em 3-5 kHz, aqueça os médios-graves. Este EQ vem depois da compressão, então seus boosts não vão acionar o compressor.

**Por que funciona:** Separação de responsabilidades. O EQ corretivo previne artefatos no compressor. O compressor gerencia a dinâmica de um sinal limpo. O EQ tonal molda o caráter final sem afetar a dinâmica.

---

## 5. Artefatos Dependentes de Frequência a Observar

| Problema | Causa | Solução |
|----------|-------|---------|
| Bombeamento em plosivas | Rajadas de baixa frequência acionando o compressor | HPF antes do compressor (EQ→Comp) |
| Sibilância amplificada | Compressor reduz corpo, sibilância permanece | De-esser antes do compressor, ou corte de EQ em 6 kHz primeiro |
| Som abafado após compressão | Attack rápido esmagando transientes | Attack lento (15-30ms), ou compressão paralela |
| Timbre inconsistente | Compressor reagindo diferentemente a trechos suaves vs altos | Use 2 estágios de compressão suave em vez de 1 estágio pesado |

---

## 6. EQ Dinâmico: A Alternativa Moderna

O EQ dinâmico combina EQ e compressão em um único processador. Cada banda de EQ só é ativada quando a frequência ultrapassa um threshold — como um compressor que só funciona em frequências específicas.

**Caso de uso:** Sibilância que varia ao longo da performance. Um corte estático em 6 kHz abafaria o vocal inteiro, mas um corte de EQ dinâmico só é ativado quando a sibilância ultrapassa o threshold.

Isto não substitui a questão Comp→EQ — é uma ferramenta especializada para problemas de dinâmica dependentes de frequência.

---

## Exercício Prático

### Exercício 1: Compare A/B a Ordem
Pegue uma gravação vocal. Monte duas cadeias paralelas:
- Cadeia A: Compressor (4:1, -6 dB GR) → EQ (boost 3 kHz +3 dB, corte 250 Hz -4 dB)
- Cadeia B: Mesmo EQ → Mesmo Compressor

Ouça ambas. Onde você percebe a diferença? Foque em:
- Consistência das baixas frequências (tratamento do efeito de proximidade)
- Nível de sibilância
- "Naturalidade" geral da compressão

### Exercício 2: Monte um Sanduíche
Monte: HPF em 100 Hz + corte em 250 Hz → Compressor (3:1) → Boost de presença em 4 kHz + Ar em 12 kHz. Compare com uma cadeia de EQ único seguido de compressão.

---

## Principais Conclusões
- **A ordem importa** — o compressor responde a quaisquer frequências que estejam mais altas na entrada
- **EQ→Comp é o padrão mais seguro** — corrija problemas antes de comprimir para resultados mais naturais
- **O sanduíche EQ→Comp→EQ é o padrão profissional** — corretivo primeiro, tonal por último
- **Não existe uma ordem universalmente "correta"** — depende da gravação, do gênero e da intenção
- **EQ Dinâmico** é uma ferramenta moderna para problemas de dinâmica dependentes de frequência
- O objetivo é sempre: controlar a dinâmica sem destruir o caráter natural da performance

## Leitura Complementar
- Departamento de Física: Acústica — frequência, amplitude e relações harmônicas
- Departamento de Música: Como a percepção de timbre afeta decisões de mixagem
- Departamento de Ciência da Computação: Algoritmos DSP por trás do EQ e da compressão
- AES (Audio Engineering Society): Padrões para medição de loudness (ITU-R BS.1770)

---
*Produzido pelo Ciclo de Pesquisa Seldon audio-engineering-2026-03-23-001 em 2026-03-23.*
*Pergunta de pesquisa: A ordem de compressão antes do EQ versus EQ antes da compressão produz resultados mensuravelmente diferentes em vocais?*
*Crença: T (confiança: 0.80)*
