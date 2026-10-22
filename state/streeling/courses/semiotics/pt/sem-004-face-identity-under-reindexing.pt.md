---
module_id: sem-004-face-identity-under-reindexing
department: semiotics
course: "Identidade das faces sob reindexação"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-21-004
version: "0.1.0"
---

# Identidade das faces sob reindexação

> **Departamento de Semiótica** | Nível intermediário | 40 minutos | Rascunho provisório em português; revisão do conteúdo, revisão por pessoa fluente no idioma e avaliação por alunos pendentes.

## Objetivos e decisão do projeto

Um futuro visualizador de cena seleciona a face 1 de um modelo de origami. Um segundo agente renumera o modelo e relata que a face 1 mudou de nível. O material se moveu, a ordem mudou ou o mesmo número passou a nomear outra face? Responder a essa pergunta exige interpretar o número antes de interpretar a geometria.

Após esta aula, você conseguirá transportar uma seleção por uma permutação explícita, inverter esse mapeamento, distinguir a identidade de uma face de seu nível e orientação e escrever um relatório entre agentes com limites claros. Reserve oito minutos para o problema e os signos, doze para a tabela, dez para as transformações e dez para os exercícios e a transferência. O artefato é uma pequena tabela de correspondência e um repasse defensável, em vez de um novo serviço de identidade.

A evidência do projeto vem do commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), [testes de espessura](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) e [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). Esses links fixam a fonte inspecionada, não a branch atual. Aqui o IX fornece verificações e controles de transformação; esta aula não demonstra exportação para Blender, importação no Godot, renderizador ou implementação de seleção persistente.

## 1. O número de uma face é um signo contextual

Na semiótica, um signo representa um objeto sob uma interpretação. Aqui `1` é o signo, uma face material específica é o objeto pretendido e “consultar a posição 1 nesta revisão do modelo” é a interpretação. Um **índice** de array é um endereço de programação dentro de uma coleção ordenada. Não deve ser confundido com o termo semiótico mais amplo *índice*, um signo ligado àquilo que indica. Nenhum dos usos da palavra dá identidade permanente ao número.

Um relatório precisa de sua revisão do modelo ou de seu contexto de transformação. “Face 1” na entrada e “face 1” na saída são duas referências potencialmente diferentes. Forma, cor e nível atual na pilha podem ajudar uma pessoa a reconhecer uma face, mas essas propriedades podem coincidir entre faces ou mudar com uma transformação. Por si sós, não estabelecem proveniência.

Nesta aula, **identidade material** significa a correspondência com a mesma face de entrada por meio da transformação controlada específica. Isso não resolve remalhagem arbitrária, divisão, fusão nem reconstrução de um modelo a partir de uma imagem. Um rótulo de proveniência, como o rótulo didático A, registra a correspondência que fornecemos. Esses rótulos são explicitamente sintéticos; a `Permutation` do IX inspecionada é um mapeamento para uma transformação, não um registro universal de IDs persistentes.

### Exercício 1 — Corrija uma referência

Um agente diz: “A face 1 está errada após a renumeração.” Que informação falta? Reescreva a afirmação como uma pergunta que possa ser inspecionada.

> **Resposta:** Faltam o contexto dos modelos de entrada e saída, o mapa de correspondência e a propriedade comparada. Uma pergunta útil é: “Para a face sintética de entrada 1 (B), usando o mapa do índice antigo para o novo `[2,0,3,1]`, a face de saída 0 mantém o nível de entrada 2?” Isso identifica o material pretendido e a comparação exata; não alega um defeito no IX.

## 2. Use o mapeamento no sentido declarado

`Permutation` documenta para onde foi cada índice **antigo**. A função auxiliar `place` escreve um item antigo em `out[perm[old]]`. Portanto, `perm.faces[f]` recebe o índice de uma face de entrada e retorna seu índice de face na saída. Não informa qual face de entrada ocupa agora uma posição arbitrária da saída; para isso, é necessário o inverso.

Use este exemplo de quatro faces, explicitamente **sintético**, também registrado no [conjunto de exemplos](../../../fixtures/semiotics/sem-004/scenarios.json). Seus números não são resultados do tsuru, uma semente amostrada nem um experimento físico de espessura.

| Índice de entrada | Rótulo didático de proveniência | Nível de entrada | Índice de saída `p[old]` |
|---:|---|---:|---:|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 0 |
| 2 | C | 1 | 3 |
| 3 | D | 3 | 1 |

O mapa direto é `p = [2,0,3,1]`. Ler as posições de saída de 0 a 3 dá os rótulos `[B,D,A,C]` e os níveis `[2,3,0,1]`. O inverso é `q = [1,3,0,2]`: a posição de saída 0 veio da posição de entrada 1, e a posição de saída 1 veio da posição de entrada 3. Verifique os dois sentidos: `q[p[f]] = f` e `p[q[j]] = j`.

A comparação correta da propriedade é `new[p[f]] == old[f]`. Para B na entrada, é `new[0] == old[1]`, portanto `2 == 2`. Comparar os arrays diretamente produz desigualdade, embora cada face material mantenha seu valor. Reutilizar o inteiro selecionado 1 passa a destacar D, cujo nível é 3. Trata-se de um erro de seleção sem corrupção do cálculo de nível.

O inverso é igualmente útil quando um usuário clica na posição de saída 3: ele identifica C na posição de entrada 2. Escrever `new[q[f]]` na comparação direta mistura domínios. Com nosso mapa deliberadamente diferente do próprio inverso, a entrada 0 compararia `new[1] = 3` com `old[0] = 0`. Um exemplo apenas com uma troca pode ocultar esse erro, porque uma troca é igual ao próprio inverso.

### Exercício 2 — Transporte a seleção

Transporte a seleção de entrada C pelo mapa. Depois, rastreie um clique na posição de saída 1 de volta à entrada. Manter o inteiro 2 preservaria a seleção original C?

> **Resposta:** C é a entrada 2, portanto seu índice de saída é `p[2] = 3`, mantendo o nível 1. A saída 1 vem de `q[1] = 3`, rótulo D. Manter o inteiro 2 selecionaria A na saída. O mapa muda o endereço, preservando a correspondência material que estipulamos.

### Exercício 3 — Compare os objetos certos

Encontre a primeira divergência em uma comparação direta de `[0,2,1,3]` e `[2,3,0,1]`. Declare as quatro comparações mapeadas e verifique uma equação do inverso.

> **Resposta:** A posição 0 diverge na comparação direta: `0 != 2`. As verificações mapeadas são `new[2]=0`, `new[0]=2`, `new[3]=1` e `new[1]=3`, correspondendo às posições de entrada 0–3, respectivamente. Por exemplo, `q[p[2]] = q[3] = 2`. A desigualdade direta não refuta a correspondência afirmada.

## 3. Preserve as relações sem confundir seus sinais

A renumeração também remapeia vértices e arestas. Ela gira ciclicamente a lista de vértices de cada face, preservando seu sentido de percurso; pode trocar as extremidades de uma aresta; embaralha a sequência de entradas de `faceOrders`. São operações distintas. Girar uma borda triangular de `[0,1,2]` para `[1,2,0]` muda seu ponto inicial. Invertê-la para `[0,2,1]` muda o sentido de percurso e não é a mesma operação. Essas pequenas listas de borda ilustram convenções de ordenação, não geometria extraída do IX.

Em cada tripla de `faceOrders`, `[f,g,s]`, `renumber` substitui os valores por `[p[f],p[g],s]` e mantém o sinal. Nossa tripla sintética `[1,3,1]` torna-se `[0,1,1]`. O sinal é interpretado em relação às normais das faces; sem a orientação, não deve ser transformado em um indicador global e incondicional de “acima”. Embaralhar a coleção de relações também não inverte cada relação. Uma posição na lista, uma posição de extremidade, um sentido de borda e um sinal de ordem de camadas têm significados diferentes.

No teste de espessura fixado, `controls_leave_the_stack_unchanged` executa a renumeração com sementes 1–5 no tsuru. Verifica 28 camadas locais, contagem de 36 níveis rígidos e, para cada face de entrada, `new[perm.faces[f]] == old[f]`. Essa é evidência concreta para esses controles nesse caso de teste. Não é um teorema exaustivo para toda dobra ou transformação.

`face_levels` é uma configuração testemunha de pilha que respeita os pares declarados, começando no nível zero. A implementação pode não retornar níveis por face quando há um ciclo ou informação de ordem insuficiente. Portanto, um nível não é um identificador único de material nem uma descrição canônica de toda pilha admissível. Duas faces podem compartilhar um nível. A igualdade das contagens agregadas, sozinha, não informa a um coordenador se uma seleção ainda aponta para a face pretendida.

### Exercício 4 — Separe três operações de ordem

Uma pessoa revisora trata uma borda de face girada, entradas embaralhadas de `faceOrders` e um modelo virado como “reordenação de array”. Explique por que essa descrição perde significados relevantes. Mapeie a tripla sintética `[1,3,1]`.

> **Resposta:** A rotação da borda mantém o sentido de percurso cíclico; embaralhar a lista de relações muda a enumeração, preservando cada relação; virar o modelo muda a orientação e a interpretação de cima. Essas operações exigem verificações diferentes. A tripla torna-se `[0,1,1]`: suas referências a faces passam por p e seu sinal relativo é mantido. Isso, sozinho, não estabelece uma relação global de acima.

## 4. Declare a transformação e os limites de sua evidência

`move_folded` gira o referencial dobrado em seu plano e depois o translada, mantendo as orientações. O teste fixado usa ângulo de 0.7 radianos e deslocamento `[3,-2]`, verificando a igualdade de toda a pilha retornada com a referência. Essa observação sustenta esse movimento rígido testado, não redimensionamento, deformação ou remalhagem arbitrários.

`turn_over` reflete as coordenadas y dobradas com `y -> -y`. Sua documentação diz que as orientações e o sentido de cima se invertem, de modo que `faceOrders`, relativo às normais das faces, permanece inalterado. O teste de espessura verifica a igualdade da contagem de camadas locais, da altura por camadas locais, da contagem de níveis rígidos e da altura rígida. Ele explicitamente **não** verifica qual face ocupa qual nível. Relatar níveis por face inalterados após virar o modelo iria além da evidência. Correspondência material e ordem vertical são perguntas separadas.

Um repasse útil identifica a revisão da fonte, a transformação, o sentido do mapeamento, os índices selecionados de entrada e saída, a propriedade comparada e o resultado. Se a correspondência não estiver disponível após uma regeneração arbitrária, relate identidade não resolvida. Espessura agregada idêntica ou uma silhueta familiar não fornecem o mapeamento ausente. Essa é uma exigência de comunicação para o fluxo de trabalho proposto, não um protocolo de seleção implementado no IX.

### Exercício 5 — Projete um teste de seleção falsificável

Proponha um futuro teste no Godot que possa refutar a retenção correta da seleção após essa renumeração sintética. Inclua uma afirmação sobre virar o modelo que a fonte existente não justifica.

> **Resposta:** Antes da transformação, selecione B na entrada 1 e registre seu rótulo didático de proveniência, a revisão do modelo e o mapa. Após aplicar p, exija que o destaque e o relatório identifiquem a saída 0, B, nível 2. Um destaque na saída 1/D refuta a retenção, mesmo se os totais de níveis coincidirem. Registre eventos brutos de seleção e capturas de tela antes e depois; nenhum teste foi realizado aqui. “B mantém o mesmo nível após virar o modelo” não é sustentado pelas asserções fixadas, que verificam apenas valores agregados nessa transformação.

O teste proposto precisa de um adaptador real de cena e de observação independente antes que alguém afirme sucesso de integração. As entregas atuais são a análise das fontes, uma tabela sintética e tarefas preparadas para alunos. Continuam pendentes a revisão humana do conteúdo, uma tentativa de aluno, a revisão por pessoa fluente no idioma e a publicação pública.
