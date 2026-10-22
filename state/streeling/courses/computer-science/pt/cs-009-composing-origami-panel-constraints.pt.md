---
module_id: cs-009-composing-origami-panel-constraints
department: computer-science
course: "Componha as restrições do origami antes de aceitar uma pilha rígida"
level: intermediate
prerequisites: [cs-001-thinking-algorithmically, cs-006-ixql-pipeline-composition]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-21-009
version: "0.1.0"
---

# Componha as restrições do origami antes de aceitar uma pilha rígida

> **Departamento de Ciência da Computação** | Nível intermediário | 40 minutos | Rascunho provisório em português; revisão do conteúdo, revisão por pessoa fluente no idioma e avaliação por alunos pendentes.

## Objetivos e pergunta do projeto

Você transformará juntas planas em classes de equivalência, preservará restrições dirigidas entre essas classes, distinguirá testes locais de sobreposição de uma restrição global de empilhamento e interpretará um resultado incompleto sem inventar uma disposição. A pergunta prática é: **qual resultado um agente pode encaminhar a um futuro adaptador de Blender ou Godot quando o IX verificou um estado de origami?** Um objeto artesanal visível precisa de uma interpretação declarada da análise, pois uma verificação bem-sucedida pode coexistir com uma recusa sob outro modelo.

O estudo de caso é o [módulo de espessura implementado no IX](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) e seus [testes de integração](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), ambos fixados em `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. O módulo lê uma espessura de material nas unidades de coordenada do padrão de vincos. Examina um estado dobrado plano declarado; não planeja o movimento de dobra nem exporta uma cena. O [conjunto de exemplos do curso](../../../fixtures/computer-science/cs-009/README.md) contém pequenas deduções de grafos, claramente separadas dos resultados reais dos testes Rust.

## 1. Primeiro componha as faces em painéis

Uma face é um polígono na descrição do estado dobrado. Neste modelo, um painel é um conjunto de faces conectadas por juntas planas que precisam manter uma única altura. A função `panels` da implementação une seus conjuntos e mapeia cada face para a face de menor índice em seu componente conexo. Esse representante é um rótulo algorítmico. Não é um identificador permanente de objeto, e renumerar a entrada pode alterá-lo, preservando o painel representado.

Considere as faces 0, 1 e 2. As faces 0 e 1 compartilham uma junta plana. As relações declaradas colocam 2 acima de 0 e 1 acima de 2. Como grafo de faces, os arcos de baixo para cima são `0 → 2 → 1`, sem ciclo. Se atribuirmos a cada face sua própria altura, a resposta aparente é os níveis 0, 1 e 2. Isso viola o modelo: as faces 0 e 1 pertencem a um mesmo painel rígido e não podem assumir alturas diferentes.

Após unir as faces conectadas por juntas planas, o mapa de painéis é `[0, 0, 2]`. As duas restrições tornam-se `panel 0 → panel 2` e `panel 2 → panel 0`. O ciclo agora fica visível. Essa é uma construção quociente: primeiro agrupe os objetos que precisam se mover juntos e depois aplique as restrições de ordem a esses grupos. Verificar cada parte antes da composição deixa de captar a exigência introduzida por sua identidade compartilhada.

### Exercício 1: corrija o grafo enganoso

Use o caso de teste `pierced-flat-joint`. Forneça os representantes dos painéis e os dois arcos entre painéis. Explique por que a ordem topológica do grafo de faces não pode justificar uma disposição rígida. Que decisão adicional de implementação seria necessária se um adaptador quisesse um ID permanente de painel?

> **Resposta:** Os representantes são `[0, 0, 2]`; os arcos são `0 → 2` e `2 → 0`. A ordem das faces permite duas alturas diferentes para o mesmo painel conectado por juntas planas, portanto resolve o sistema de restrições errado. Um ID permanente de painel precisaria de um mapeamento declarado de volta à identidade do material ou da fonte, mantido entre edições ou permutações. O representante de índice mínimo, sozinho, não oferece essa garantia.

## 2. O sucesso local pode coexistir com uma recusa global

O teste fixado `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` constrói quatro tiras. Cada uma sobrepõe a seguinte em um canto diferente. Toda célula local de sobreposição pode ter uma ordem consistente, mas as declarações combinadas dizem que a tira 0 está acima da 1, a 1 acima da 2, a 2 acima da 3 e a 3 acima da 0. Usando arcos de baixo para cima, temos `0 → 3 → 2 → 1 → 0`. Nenhuma altura única por tira satisfaz as quatro desigualdades para uma espessura de material positiva.

Isso é diferente de [VC-007](../../visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), cujo verificador sintético detecta o reinício da paridade em limites repetidos de ladrilhos. Aqui, o problema é um ciclo que atravessa diferentes regiões de sobreposição na implementação existente do IX. Uma textura, uma prévia de cruzamento local ou uma análise básica bem-sucedida do origami não resolvem a questão global dos painéis paralelos.

O teste verifica que `analyse(&weave()).unwrap().ok` é verdadeiro. Também verifica a leitura opcional de espessura com `t = 0`, um `t` positivo muito pequeno e `t = 0.5`. O grafo continua cíclico, mas `rigid.refused` é verdadeiro apenas para `t` positivo. Com zero, a implementação ainda retorna `levels`, `height` e `face_levels` como ausentes para essa leitura cíclica. Não substitua uma altura rígida ausente por zero apenas porque o valor separado de `ply_height` é zero.

### Exercício 2: interprete o caso zero

O entrelaçamento tem `ply = 2` e uma ordem cíclica de painéis. Quais são `ply_height` e `rigid.refused` com `t = 0` e `t = 0.5`? Algum dos resultados fornece uma atribuição rígida de níveis às faces?

> **Resposta:** Com zero, `ply_height = 0` e `rigid.refused = false`; com 0.5, `ply_height = 1` e há recusa. Os dois relatórios cíclicos têm níveis rígidos, altura e atribuição de níveis às faces ausentes. A ausência de recusa com espessura zero não fornece a configuração testemunha que falta, e a recusa com espessura positiva diz respeito a esse modelo de painéis paralelos.

## 3. Restrições acíclicas permitem calcular o caminho mais longo

Quando o grafo de painéis tem uma ordem topológica, a implementação inicia todos os níveis em zero. Para cada aresta dirigida de um painel inferior `u` a um painel superior `v`, atualiza `level[v] = max(level[v], level[u] + 1)`. Processar em ordem topológica garante que o nível de cada predecessor esteja disponível. O maior nível, contado a partir de zero, mais um é o comprimento da cadeia em painéis. Multiplicar pela espessura total `t` dá a altura da pilha para uma ordem totalmente determinada.

O `face_levels` relatado é uma configuração testemunha produzida por essa recorrência. Outras pilhas válidas podem existir; os valores por face não são uma rotulagem canônica de toda pilha admissível.

O DAG sintético do conjunto de exemplos tem os arcos `P → R`, `Q → R` e `R → S`. P e Q podem compartilhar o nível zero porque o exemplo não fornece uma relação que exija separação entre eles; R precisa estar acima de ambos, e S acima de R. São dados abstratos de grafo, não geometria FOLD exportada nem uma afirmação sobre sobreposição espacial. Seu propósito é praticar a recorrência antes de ler o teste maior do tsuru.

### Exercício 3: calcule a cadeia

Atribua os quatro níveis do DAG sintético, conte os painéis da cadeia mais longa e calcule a altura para `t = 0.2`. Por que relatar apenas o nível mais alto causaria um erro de uma unidade? Para comparação, quais duas contagens o teste real do tsuru distingue?

> **Resposta:** P e Q são 0, R é 1 e S é 2. A cadeia tem três painéis, portanto a altura é `3 × 0.2 = 0.6` em unidades do padrão de vincos. O índice máximo 2 omite um nível ocupado. O teste real do tsuru distingue o máximo de 28 camadas locais de 36 níveis necessários de painéis paralelos; ocupação local e uma cadeia que atravessa regiões respondem a perguntas diferentes.

## 4. A ordem ausente faz parte do resultado

A implementação conta os pares de faces sobrepostas em painéis diferentes cuja ordem não está declarada. Se houver qualquer par assim, `levels_exact` é falso. Ela relata `max(chain, ply)` como limite inferior e não fornece `face_levels`. Restrições declaradas acíclicas, sozinhas, não podem certificar que uma disposição proposta respeita uma relação que a entrada nunca especificou.

O teste fixado `an_unstated_overlap_gives_a_lower_bound` usa duas folhas sobrepostas sem ordem declarada. Espera um par indeterminado, dois níveis como limite inferior e nenhuma atribuição de níveis às faces. Quem chama a função precisa manter o indicador de exatidão junto ao número. Se o resumo de um agente o descartar, uma etapa posterior pode transformar um limite inferior em uma suposta disposição completa sem que ninguém tome essa decisão explicitamente.

### Exercício 4: preserve a incerteza em um repasse

A ficha sintética de ordem incompleta tem cadeia 2, 3 camadas locais, um par indeterminado e `t = 0.2`. Que altura numérica o algoritmo pode relatar e como ela precisa ser descrita? Um adaptador de cena pode usá-la para posicionar todas as faces?

> **Resposta:** Ele relata `max(2, 3) = 3` níveis e um limite inferior de altura de 0.6, com `levels_exact = false` e `face_levels = null`. Não pode fornecer uma disposição completa. Um repasse deve preservar a indicação de limite inferior, a contagem de pares sem ordem, a identidade da fonte e a ausência da configuração testemunha, em vez de prometer coordenadas deduzidas de uma ordem não observada.

## 5. Transforme o resultado em uma decisão que possa ser inspecionada

Uma composição de agentes pode carregar juntas a análise básica e a leitura rígida. A [decisão de projeto fixada](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/docs/adr/0007-origami-thickness-as-parallel-rigid-panels.md) mantém explicitamente a leitura de espessura ao lado do veredito básico. Uma recusa significa que não há pilha sob as hipóteses de painéis rígidos paralelos. Não prova que um objeto material seja impossível com painéis inclinados, vincos modificados ou outros métodos de construção. Inversamente, a ausência de recusa não prova que a fabricação seja viável.

Para um teste proposto no Godot, preserve a revisão FOLD de origem, a conversão da espessura total e das unidades, ambos os resultados de análise, qualquer testemunho de ciclo, a exatidão e o mapa de faces para objetos. Dê a uma pessoa que observa a cena uma tarefa específica, como encontrar a relação responsável por uma recusa. Compare sua resposta com a obtida usando um diagrama simples de grafo na mesma tarefa. Esse é um experimento proposto de transferência; o curso não registra renderizador, exportação, teste com alunos ou ganho de desempenho. Uma nova DSL só justificaria seu custo se melhorasse essa tarefa em comparação com um relatório tipado mais simples e o verificador existente.

### Exercício 5: decida o que encaminhar à próxima etapa

Um futuro agente relata: “a análise básica passou; houve recusa rígida com espessura positiva; faces do ciclo `[0,3], [3,2], [2,1], [1,0]`”. Propõe rotular o artefato como “fisicamente impossível” e omitir o ciclo porque a cena parece plausível. Escreva uma afirmação corrigida voltada ao usuário e identifique a próxima evidência necessária para uma demonstração em cena.

> **Resposta:** “O estado declarado passou nas verificações básicas, mas sua ordem declarada tem um ciclo que impede uma pilha de painéis rígidos paralelos com essa espessura positiva.” Mantenha o ciclo e as hipóteses. Uma demonstração em cena precisa de uma importação vinculada à fonte e de um mapa de faces para objetos, de uma exibição do ciclo verificável de forma independente e de uma tarefa registrada para quem observa a cena. Uma captura de tela, sozinha, não pode estabelecer o resultado do grafo, a impossibilidade física ou o benefício de aprendizagem.

## Reexecução e limites

Execute `cargo test -p ix-origami --test thickness` no IX no commit fixado. O coordenador reexecutou todos os 11 testes de integração de espessura em 2026-10-21: 11 passaram, 0 falharam. O README do conjunto de exemplos registra os blobs da fonte e dos testes. As fichas de grafos são dados didáticos deduzidos à mão; não se introduz nenhum analisador adicional nem runtime de consumidor. A aprovação desses testes sustenta os casos descritos da implementação, enquanto a correção do conteúdo, a fluência da tradução, o sucesso dos alunos, a importação de cena e a publicação no Learn conferida sem autenticação continuam sendo trabalhos separados.
