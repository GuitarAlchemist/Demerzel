---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: Fundamentos de Ciência da Computação
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Pensando Algoritmicamente

> **Departamento de Ciência da Computação** | Estágio: Nigredo (Iniciante) | Duração: 25 minutos

## Objetivos

Após esta aula, você será capaz de:
- Definir o que é um algoritmo e identificar algoritmos na vida cotidiana
- Aplicar quatro técnicas-chave de resolução de problemas: decomposição, reconhecimento de padrões, abstração e divisão e conquista
- Distinguir entre abordagens gulosas e exaustivas
- Desenvolver intuição para a notação Big-O e por que eficiência importa

---

## 1. O Que É um Algoritmo?

Um **algoritmo** é uma sequência finita de passos bem definidos que recebe uma entrada e produz uma saída. Só isso. Não precisa de computadores.

Você segue algoritmos todos os dias:
- Uma receita de cozinha é um algoritmo (entrada: ingredientes, saída: uma refeição)
- Direções para um destino são um algoritmo (entrada: localização atual, saída: destino)
- O processo de dar troco no caixa é um algoritmo (entrada: valor devido, saída: menor número de moedas)

O que separa um algoritmo de instruções vagas é **precisão**. "Cozinhe até ficar pronto" não é um algoritmo — é ambíguo. "Aqueça a 180°C por 25 minutos, depois verifique a temperatura interna; se estiver abaixo de 74°C, continue em incrementos de 5 minutos" é um algoritmo. Cada passo é inequívoco e o processo termina.

Três propriedades de um algoritmo válido:
1. **Finitude** — deve eventualmente parar
2. **Definição** — cada passo deve ser precisamente definido
3. **Efetividade** — cada passo deve ser algo que pode realmente ser executado

### Exercício Prático

Escreva um algoritmo (em português simples, em passos numerados) para procurar uma palavra em um dicionário físico. Seja preciso o suficiente para que alguém que nunca usou um dicionário possa seguir seus passos. Compare o seu com a abordagem descrita na Seção 5 (divisão e conquista) — são iguais?

---

## 2. Decomposição — Quebrando Problemas em Partes

A habilidade mais poderosa do pensamento algorítmico é a **decomposição**: dividir um problema complexo em subproblemas menores e gerenciáveis.

**Exemplo:** Você quer organizar um show.

Isso é esmagador como uma tarefa única. Mas decomponha:
1. Encontrar um local
2. Contratar artistas
3. Definir uma data
4. Vender ingressos
5. Providenciar equipamento de som
6. Divulgar o evento

Cada subproblema ainda é complexo, mas agora você pode enfrentá-los individualmente. E alguns subproblemas se decompõem ainda mais: "Vender ingressos" se torna escolher uma plataforma, definir preços, fazer o design do ingresso, abrir as vendas.

A decomposição é recursiva — você continua quebrando até que cada pedaço seja simples o suficiente para resolver diretamente. É assim que todo grande sistema de software é construído: não como um programa gigante, mas como milhares de peças pequenas e combináveis.

**Insight principal:** Se você não consegue resolver um problema, provavelmente não o decompôs o suficiente.

### Exercício Prático

Decomponha o seguinte problema em subproblemas: "Construir um site que permita aos usuários buscar acordes de violão." Continue decompondo até que cada subproblema seja algo que uma pessoa possa completar em um dia ou menos. Quantos níveis de decomposição você precisou?

---

## 3. Reconhecimento de Padrões

**Reconhecimento de padrões** é a habilidade de perceber semelhanças entre problemas que você já resolveu e novos problemas que enfrenta.

**Exemplo:** Ordenar uma mão de cartas de baralho e ordenar uma lista de nomes de alunos são o mesmo problema — organizar itens em ordem de acordo com alguma regra de comparação. Uma vez que aprende um algoritmo de ordenação, pode aplicá-lo a qualquer coisa que possa ser comparada.

Padrões aparecem em todo lugar na computação:
- Buscar em uma coleção (encontrar um livro em uma biblioteca, encontrar um arquivo no disco, encontrar uma nota no braço do violão)
- Filtrar itens que atendem a critérios (filtro de spam, busca de fotos, busca de acordes)
- Transformar dados de um formato para outro (tradução, conversão de arquivo, transposição)

Programadores experientes resolvem problemas mais rápido não porque são mais inteligentes, mas porque reconhecem padrões. Eles veem um novo problema e pensam: "Isso é essencialmente um problema de busca" ou "Isso é uma travessia de grafo" — e recorrem a uma solução conhecida.

### Exercício Prático

Considere estes três problemas. Que padrão eles compartilham?
1. Encontrar a rota mais curta entre duas cidades
2. Encontrar as menores mudanças de acorde para ir de um acorde a outro
3. Encontrar o número mínimo de movimentos para resolver um quebra-cabeça

> Todos são problemas de **caminho mínimo** — encontrar a sequência de passos de menor custo entre um estado inicial e um estado final.

---

## 4. Abstração — Ignorando o Que Não Importa

**Abstração** é a arte de remover detalhes irrelevantes para focar no que importa para o problema em questão.

Quando você desenha um mapa, não inclui cada árvore, cada rachadura na calçada, cada folha de grama. Inclui ruas, pontos de referência e distâncias — os detalhes relevantes para navegação. Todo o resto é abstraído.

No pensamento algorítmico, abstração significa:
- Representar um problema do mundo real com um modelo simplificado
- Ignorar detalhes que não afetam a solução
- Definir entradas e saídas claras

**Exemplo:** Se você quer encontrar o caminho mais curto entre duas cidades, não precisa modelar a cor das placas ou o limite de velocidade em cada estrada (a menos que velocidade importe para seu problema). Você abstrai o mapa em um **grafo**: cidades são nós, estradas são arestas, distâncias são pesos. Agora pode aplicar um algoritmo de grafo sem pensar em asfalto.

Abstração é o que permite que algoritmos sejam **de propósito geral**. Um algoritmo de ordenação não se importa se está ordenando números, nomes ou acordes de violão. Ele só precisa saber como comparar dois itens. Todo o resto é abstraído.

### Exercício Prático

Você está construindo um sistema para recomendar rotinas de prática para alunos de violão. Quais detalhes sobre cada aluno são relevantes para o algoritmo? Quais detalhes podem ser abstraídos? Faça duas listas: "incluir" e "ignorar."

---

## 5. Divisão e Conquista

**Divisão e conquista** é uma estratégia algorítmica específica:

1. **Dividir** o problema em subproblemas menores do mesmo tipo
2. **Conquistar** cada subproblema (recursivamente, se necessário)
3. **Combinar** os resultados

Isso é diferente da decomposição geral. Na divisão e conquista, os subproblemas têm a **mesma estrutura** que o original — apenas menores.

**Exemplo — Busca Binária (procurar uma palavra no dicionário):**
1. Abra o dicionário na página do meio
2. A palavra está nesta página? Se sim, pronto.
3. Se a palavra vem antes desta página em ordem alfabética, repita com a primeira metade
4. Se a palavra vem depois, repita com a segunda metade
5. Continue dividindo ao meio até encontrar a palavra

Cada passo corta o espaço de busca restante pela metade. Um dicionário com 100.000 palavras requer no máximo 17 passos (já que 2^17 = 131.072 > 100.000). Compare isso com começar na página 1 e ler cada entrada — até 100.000 passos.

**Algoritmos clássicos de divisão e conquista:**
- **Busca binária** — encontrar um item em uma coleção ordenada
- **Merge sort** — ordenar dividindo, ordenando metades e depois mesclando
- **Quicksort** — ordenar escolhendo um pivô e particionando

### Exercício Prático

Você tem uma lista ordenada de 1.000 músicas. Usando busca binária, qual é o número máximo de comparações necessárias para encontrar uma música específica? (Dica: quantas vezes você pode dividir 1.000 ao meio antes de chegar a 1?)

> log2(1000) = ~10. No máximo 10 comparações — comparado a 1.000 para uma busca linear.

---

## 6. Abordagens Gulosa vs Exaustiva

Duas grandes famílias de algoritmos representam filosofias diferentes:

**Algoritmos gulosos** fazem a escolha localmente ótima em cada passo, esperando que isso leve a uma solução globalmente ótima.

*Exemplo — Dar troco com o menor número de moedas:*
- Valor: R$ 0,67
- Abordagem gulosa: pegue a maior moeda que cabe. 50 centavos → 10 centavos → 5 centavos → 1+1 centavos. Resultado: 50+10+5+1+1 = 5 moedas.
- Isso funciona para a moeda brasileira. Mas para uma moeda com valores de 1, 3 e 4 centavos, a abordagem gulosa falha: para 6 centavos, a gulosa dá 4+1+1 (3 moedas), mas o ótimo é 3+3 (2 moedas).

**Algoritmos exaustivos** verificam toda solução possível e escolhem a melhor. Sempre encontram a resposta ótima, mas podem ser lentos.

*Exemplo — O caixeiro-viajante:*
- Visite 10 cidades e retorne pelo caminho mais curto
- Exaustivo: tente todas as ordenações possíveis (10! = 3.628.800 rotas), meça cada uma, escolha a mais curta
- Isso garante a rota ótima, mas é computacionalmente caro

| Abordagem | Vantagem | Desvantagem | Usar Quando |
|-----------|----------|-------------|-------------|
| Gulosa | Rápida, simples | Pode perder a solução ótima | Bom o suficiente é bom o suficiente |
| Exaustiva | Ótimo garantido | Lenta para problemas grandes | Correção é crítica e a entrada é pequena |

Muitos algoritmos do mundo real combinam ambas: usam heurísticas gulosas para podar o espaço de busca, depois verificam exaustivamente os candidatos restantes.

### Exercício Prático

Você está arrumando uma mala com itens de diferentes pesos e valores, e a mala tem um limite de peso. Descreva uma abordagem gulosa e uma exaustiva. Qual você usaria se tivesse 5 itens? 500 itens?

> *Gulosa:* Ordene os itens pela razão valor/peso, adicione itens da maior razão até a mala encher. *Exaustiva:* Tente toda combinação possível, calcule o valor total para aquelas dentro do limite de peso, escolha a melhor. Para 5 itens (32 combinações), exaustiva é viável. Para 500 itens (2^500 combinações), exaustiva é impossível — use gulosa ou um algoritmo mais inteligente.

---

## 7. Intuição Big-O — Quão Rápido É Rápido o Suficiente?

Nem todos os algoritmos são criados iguais. A **notação Big-O** descreve como o tempo de execução de um algoritmo cresce conforme o tamanho da entrada aumenta.

Você não precisa calcular Big-O com precisão agora. Precisa de **intuição** para o que as categorias significam:

| Big-O | Nome | Exemplo | 1.000 itens | 1.000.000 itens |
|-------|------|---------|-------------|-----------------|
| O(1) | Constante | Acessar um elemento de array por índice | 1 passo | 1 passo |
| O(log n) | Logarítmico | Busca binária | ~10 passos | ~20 passos |
| O(n) | Linear | Percorrer cada item uma vez | 1.000 passos | 1.000.000 passos |
| O(n log n) | Linearítmico | Merge sort, quicksort | ~10.000 passos | ~20.000.000 passos |
| O(n^2) | Quadrático | Comparar cada par | 1.000.000 passos | 1.000.000.000.000 passos |
| O(2^n) | Exponencial | Busca exaustiva de subconjuntos | ~10^301 passos | Esqueça |

O insight principal: **a diferença entre categorias de algoritmos cresce enormemente com o tamanho da entrada.** Um algoritmo O(n) e um O(n^2) podem ambos parecer instantâneos em 10 itens. Em um milhão de itens, um termina em um segundo e o outro leva dias.

É por isso que o pensamento algorítmico importa. Escolher o algoritmo certo pode ser a diferença entre um programa que funciona e um que nunca termina.

### Exercício Prático

Você tem dois algoritmos para buscar em uma biblioteca musical:
- Algoritmo A: verifica cada música uma por uma (O(n))
- Algoritmo B: usa um índice ordenado e busca binária (O(log n))

Para uma biblioteca de 10 milhões de músicas, aproximadamente quantos passos cada um leva?
> A: 10.000.000 passos. B: log2(10.000.000) = ~23 passos. O Algoritmo B é mais de 400.000 vezes mais rápido.

---

## Termos-Chave

| Termo | Definição |
|-------|-----------|
| **Algoritmo** | Uma sequência finita de passos bem definidos que transforma entrada em saída |
| **Decomposição** | Dividir um problema complexo em subproblemas menores e gerenciáveis |
| **Reconhecimento de padrões** | Identificar semelhanças entre um novo problema e problemas previamente resolvidos |
| **Abstração** | Remover detalhes irrelevantes para focar no que importa para a solução |
| **Divisão e conquista** | Dividir um problema em instâncias menores do mesmo problema, resolvendo recursivamente |
| **Algoritmo guloso** | Fazer a escolha localmente ótima em cada passo |
| **Algoritmo exaustivo** | Verificar toda solução possível para garantir encontrar a melhor |
| **Notação Big-O** | Uma classificação da eficiência de algoritmos por como o tempo de execução cresce com o tamanho da entrada |

---

## Autoavaliação

**1. Quais três propriedades um algoritmo válido deve ter?**
> Finitude (ele termina), definição (cada passo é inequívoco) e efetividade (cada passo pode ser realmente executado).

**2. Você precisa buscar um nome em uma lista não ordenada de 1.000 nomes. Qual o melhor Big-O que pode alcançar?**
> O(n) — busca linear. Sem ordenação ou indexação, você deve potencialmente verificar cada item. Se a lista fosse ordenada, poderia usar busca binária para O(log n).

**3. Um algoritmo guloso para dar troco dá a resposta errada para moedas de 1, 3 e 4 centavos ao dar troco de 6 centavos. Por quê?**
> A abordagem gulosa escolhe a maior moeda primeiro (4), depois precisa de 1+1 para o restante (3 moedas no total). Mas 3+3 usa apenas 2 moedas. A gulosa falha porque a escolha localmente ótima (maior moeda) não leva à solução globalmente ótima.

**4. Por que O(n log n) é considerado eficiente para ordenação?**
> Foi matematicamente provado que nenhum algoritmo de ordenação por comparação pode ser melhor que O(n log n) no pior caso. Merge sort e quicksort atingem esse limite, tornando-os ótimos entre as ordenações por comparação.

**Critério de aprovação:** Decompor um problema dado em subproblemas, identificar qual abordagem algorítmica (gulosa, exaustiva, divisão e conquista) se adapta a um cenário dado, e explicar diferenças de Big-O usando exemplos concretos.

---

## Base de Pesquisa

- Pensamento algorítmico (decomposição, reconhecimento de padrões, abstração) é reconhecido como uma habilidade central do pensamento computacional
- Divisão e conquista, guloso e busca exaustiva são os três paradigmas algorítmicos fundamentais
- Notação Big-O fornece uma medida de eficiência de algoritmo independente de hardware
- Ensinar intuição algorítmica antes da análise formal melhora a transferência de resolução de problemas
- Fontes: Consenso da educação em ciência da computação, currículo do Departamento de Ciência da Computação de Streeling
- Estado de crença: T(0.91) F(0.02) U(0.05) C(0.02)
