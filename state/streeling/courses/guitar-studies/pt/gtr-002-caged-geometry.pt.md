---
module_id: gtr-002-caged-geometry
department: guitar-studies
course: "Layout do braço e sistema CAGED"
level: intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "45 minutes"
produced_by: seldon-research-cycle
research_cycle: guitar-studies-2026-03-23-001
version: "1.0.0"
---

# Geometria CAGED: Por Que Cinco Formas Dominam o Braço

> **Departamento de Estudos de Violão** | Nível: Intermediário | Duração: 45 minutos

## Objetivos
- Compreender por que exatamente 5 formas de acordes abertos cobrem todo o braço
- Derivar o sistema CAGED a partir da observação da estrutura intervalar dos acordes abertos
- Demonstrar que o CAGED é uma consequência matemática da afinação padrão, não um sistema arbitrário
- Aplicar formas móveis de acorde com pestana para navegar qualquer acorde maior pelo braço

---

## 1. As Cinco Formas Abertas

Todo guitarrista aprende estes cinco acordes maiores abertos logo no início. Cada um tem uma impressão geométrica distinta:

### Forma C
```
x 3 2 0 1 0    Cordas: 5-4-3-2-1
  T 3 5 T 3    Intervalos: Tônica-3M-5J-Tônica-3M
```

### Forma A
```
x 0 2 2 2 0    Cordas: 5-4-3-2-1
  T 5 T 3 5    Intervalos: Tônica-5J-Tônica-3M-5J
```

### Forma G
```
3 2 0 0 0 3    Cordas: 6-5-4-3-2-1
T 3 5 T 3 T    Intervalos: Tônica-3M-5J-Tônica-3M-Tônica
```

### Forma E
```
0 2 2 1 0 0    Cordas: 6-5-4-3-2-1
T 5 T 3 5 T    Intervalos: Tônica-5J-Tônica-3M-5J-Tônica
```

### Forma D
```
x x 0 2 3 2    Cordas: 4-3-2-1
  T 5 T 3      Intervalos: Tônica-5J-Tônica-3M
```

**Observação-chave:** Toda forma contém apenas três classes de nota: Tônica, Terça Maior e Quinta Justa. As diferenças estão na *disposição* -- em qual oitava cada nota aparece e quais cordas as carregam.

---

## 2. O Teste do Deslizamento

Eis o insight central: se você mantém a *geometria dos dedos* de qualquer acorde aberto mas o desliza pelo braço acima, as relações intervalares são preservadas. O dedo da pestana substitui a pestana fixa.

**Forma E no traste 0:** Mi maior (aberto)
**Forma E no traste 1:** Fá maior (acorde com pestana)
**Forma E no traste 3:** Sol maior
**Forma E no traste 5:** Lá maior

Isso funciona porque o intervalo entre cada par de cordas adjacentes é fixado pela afinação. Mover todos os dedos pelo mesmo número de trastes transpõe cada nota pelo mesmo intervalo.

Isso não é um truque pedagógico -- é um *teorema geométrico* sobre o braço.

---

## 3. Por Que Exatamente Cinco Formas?

A afinação padrão (Mi-Lá-Ré-Sol-Si-Mi) cria um padrão intervalar específico entre as cordas:

```
Corda:     6    5    4    3    2    1
Nota:      Mi   Lá   Ré   Sol  Si   Mi
Intervalo:   4J   4J   4J   3M   4J
```

O padrão 4a-4a-4a-3a-4a cria exatamente **cinco regiões distintas** onde formas de acordes abertos podem ser formadas. Cada forma ocupa uma extensão diferente de trastes e cordas.

As cinco formas se encaixam como peças de quebra-cabeça:

```
Traste:  0    3    5    7    8    10   12
         |--E--|--D--|--C--|--A--|--G--|--E--|
         (formas mostradas para a tonalidade de Mi maior)
```

Percorrendo a ordem C-A-G-E-D, você caminha pelo braço acima, com a tônica de cada forma conectando-se à nota mais aguda da próxima forma. Esta é a **sequência CAGED** -- um caminho cíclico por todas as cinco regiões de disposição.

---

## 4. CAGED É a Única Ordenação?

As cinco formas formam um **ciclo**, então qualquer ponto de partida dá uma sequência válida:

- **CAGED** (mais comum)
- **AGEDC** (começando de A)
- **GEDCA** (começando de G)
- **EDCAG** (começando de E)
- **DCAGE** (começando de D)

O nome "CAGED" é conveniência mnemônica. O ciclo subjacente de 5 formas é estruturalmente determinado. Todas as ordenações descrevem a mesma cobertura do braço.

---

## 5. Dependência da Afinação

O CAGED é específico da afinação padrão. Mude a afinação e as formas mudam:

- **Afinação em quartas** (Mi-Lá-Ré-Sol-Dó-Fá): A irregularidade da 3M entre as cordas 3-2 desaparece. As formas dos acordes se tornam mais uniformes, mas diferentes do CAGED.
- **Afinação aberta em Sol** (Ré-Sol-Ré-Sol-Si-Ré): As cordas soltas já formam um acorde, criando um sistema de formas completamente diferente.
- **Drop D** (Ré-Lá-Ré-Sol-Si-Mi): Apenas a corda mais grave muda, preservando a maioria das formas CAGED mas alterando as formas E e G nas cordas graves.

Isso prova que o CAGED é *derivado da* geometria da afinação padrão, não imposto a ela.

---

## Exercício Prático

### Exercício 1: Identificação de Formas
Toque um acorde de Dó maior usando todas as cinco formas CAGED. Comece com a forma C aberta, depois encontre a forma A (traste 3), forma G (traste 5), forma E (traste 8) e forma D (traste 10).

### Exercício 2: Conexão de Formas
Escolha duas formas CAGED adjacentes. Encontre as notas que compartilham nas mesmas cordas. Essas notas compartilhadas são seus "pontos de pivô" para se mover entre formas.

### Exercício 3: Uma Corda, Cinco Formas
Na corda 2 somente, toque a nota Dó em cada uma das cinco posições CAGED. Observe como cada forma coloca o Dó em um traste diferente dessa corda.

---

## Principais Conclusões
- O sistema CAGED é **descoberto, não inventado** -- é uma consequência estrutural da geometria da afinação padrão
- Exatamente **5 formas** cobrem o braço por causa do padrão de afinação 4a-4a-4a-3a-4a
- Cada forma preserva sua estrutura intervalar quando usada com pestana e deslocada -- isso é um teorema geométrico, não um atalho pedagógico
- O nome "CAGED" é uma de 5 ordenações cíclicas equivalentes
- Afinações diferentes produzem sistemas de formas diferentes, confirmando que o CAGED é derivado da afinação

## Leitura Complementar
- [GTR-001: O Mapa do Braço do Violão](gtr-001-the-fretboard-map.pt.md) -- pré-requisito
- Departamento de Música: Sistemas de afinação e temperamento
- Departamento de Física: Acústica da vibração de cordas e harmônicos
- Departamento de Matemática: Teoria de grupos e simetria do braço

---
*Produzido pelo Ciclo de Pesquisa Seldon guitar-studies-2026-03-23-001 em 2026-03-23.*
*Pergunta de pesquisa: As disposições comuns de acordes abertos compartilham padrões estruturais que predizem suas formas móveis com pestana?*
*Crença: T (confiança: 0.85)*
