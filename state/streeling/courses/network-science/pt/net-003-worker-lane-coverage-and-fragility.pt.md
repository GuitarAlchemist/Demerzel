---
module_id: net-003-worker-lane-coverage-and-fragility
department: network-science
course: "Medir a cobertura das vias de trabalho após uma mudança de modo"
level: intermediate
prerequisites: [net-002-capability-graphs-and-projections]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-003
version: "0.1.0"
---

# Medir a cobertura das vias de trabalho após uma mudança de modo

> **Departamento de ciência de redes** | Nível intermediário | 35 minutos | Rascunho em português; revisão e publicação pendentes

## Objetivos e pergunta do projeto

Você construirá um grafo entre trabalhadores e classes de trabalho a partir de uma política de vias do Demerzel fixada em um commit. Medirá a cobertura, o efeito de remover um trabalhador e as informações que o grafo perde sobre funções e decisões. **Pergunta do projeto:** quando muda o modo consultivo de distribuição ou uma via fica indisponível, quais *classes de trabalho declaradas* ainda têm um caminho nominal? O cálculo pode orientar a escolha de uma via ou uma pergunta de revisão. Ele não prova que um agente está online, tem autorização para agir ou concluiu uma tarefa.

[NET-002](../en/net-002-capability-graphs-and-projections.md) liga *repositórios* a famílias de capacidades. Esta lição liga *trabalhadores* às funções atribuídas e respectivas classes de trabalho. As arestas vêm da [política de vias do Demerzel no commit `ecdc6c2`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) e são filtradas pelo modo solicitado. O grafo não inclui rota MCP nem situação atual dos agentes.

## 1. Defina o grafo antes de medi-lo

A política fixada declara cinco trabalhadores: `jules`, `claude`, `gemini`, `codex` e `augment`. Cada um tem uma função `primary`, uma lista de funções `secondary` e outra lista `forbidden` ([definições dos trabalhadores](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L54-L79)). Cada função nomeada aponta para uma `work_class` ([definições das funções](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L19-L51)). A própria política se declara **consultiva e de simulação**. Ela propõe encaminhamento, não fornece recibo de trabalho realizado.

Construa um grafo dirigido de três camadas `trabalhador → função atribuída → classe de trabalho`. Desenhe a primeira aresta somente para uma função primária ou secundária; uma função proibida não cria caminho. A segunda aresta segue `work_class`. Para um modo solicitado, oculte os caminhos cuja classe apareça em [`mode_blocks`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L81-L86). Na projeção em duas camadas, existe uma aresta trabalhador-classe quando ao menos um caminho de função atribuída sobrevive. Várias funções da mesma classe contam como **uma** aresta trabalhador-classe. Contamos trabalhadores distintos por classe, não capacidade ou tarefas concluídas.

O dicionário `work_classes` completo contém 13 nomes, inclusive ações proibidas. Apenas cinco classes aparecem em atribuições primárias ou secundárias: `fix`, `groom`, `navigate`, `net_new_feature` e `review`. Chame esse conjunto de `A`. Defina **cobertura** `C(m) = |{c in A: degree_m(c) > 0}| / |A|` e **quantidade de classes redundantes** `R(m) = |{c in A: degree_m(c) >= 2}|`. São medidas descritivas: dois trabalhadores ligados à mesma classe não são necessariamente substitutos para a mesma função.

### Exercício prático 1: não conte funções duas vezes

Em NORMAL, `claude` tem `draft_to_ready_helper`, `test_author` e `review_feedback_applier`, todos da classe `fix`, além de `builder_fixer` em `net_new_feature` e `lightweight_groomer` em `groom`. Qual é o grau de `claude` na projeção trabalhador-classe? Quantos caminhos para funções atribuídas ele possui? Por que os números diferem?

> **Resposta:** Seu grau projetado é **3**: `fix`, `net_new_feature` e `groom`. Ele tem **5** caminhos para funções atribuídas, uma primária e quatro secundárias. As três funções `fix` viram uma única aresta trabalhador-classe. Tratar cinco funções como cinco trabalhadores alternativos inflaria falsamente a redundância.

## 2. Meça o corte de um modo

As atribuições primárias e secundárias geram a projeção abaixo em NORMAL. Um `1` indica que ao menos um caminho de função atribuída sobrevive ao filtro da classe:

| Trabalhador | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 1 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

A matriz contém **9** arestas trabalhador-classe. Os graus são `fix:2`, `groom:2`, `navigate:1`, `net_new_feature:1` e `review:3`. Portanto, `C(NORMAL)=5/5` e `R(NORMAL)=3`. CONSTRAINED bloqueia `net_new_feature` e `broad_architecture`; DRAINING bloqueia também `workflow_policy_change`. Dessas classes, só `net_new_feature` tem caminho atribuído: **ambos** os modos mantêm 8 arestas e quatro classes cobertas, com `C=4/5` e `R=3`. HALTED ainda bloqueia `fix`, `groom` e `navigate`, mas não `review`. Restam três arestas, todas para `review`: `C(HALTED)=1/5`, `R(HALTED)=1`. Essa razão não libera operações em um sistema parado; apenas descreve declarações sobreviventes ao filtro.

### Exercício prático 2: calcule o corte, não uma indisponibilidade real

Em DRAINING, qual aresta de NORMAL desaparece, quanto valem `C` e `R`, e o cálculo prova que um agente Claude realmente parou de trabalhar?

> **Resposta:** Apenas `claude → net_new_feature` desaparece, pois é a única aresta atribuída da classe bloqueada. Oito das nove arestas permanecem; quatro das cinco classes estão cobertas, logo `C=4/5`. `fix`, `groom` e `review` ainda têm grau ao menos dois, logo `R=3`. Isso é um corte do grafo da política, não evidência de um agente em execução ou de um encaminhamento real.

## 3. Teste a fragilidade à perda de um trabalhador

Para o modo `m` e trabalhador removido `w`, defina `L_m(w)` como a quantidade de classes cobertas antes da remoção e descobertas depois. Apague `w` e seus caminhos e recalcule os graus. Em DRAINING, só `augment` possui aresta para `navigate`. Removê-lo muda o grau de `navigate` de 1 para 0; assim, `L_DRAINING(augment)=1` e a cobertura cai de `4/5` para `3/5`. Remover qualquer um dos outros quatro não perde **nenhuma classe inteira**, porque outra via nominal permanece. Essa é uma análise de sensibilidade por remoção de vértice, não previsão de probabilidade de falha. O JSON não registra todas as causas de indisponibilidade, e compartilhar uma classe não garante a função exata necessária à tarefa.

Redundância por classe difere de redundância por função. `review` tem três trabalhadores vizinhos em DRAINING, mas `read_only_critic`, função primária de `gemini`, `architecture_summarizer`, função secundária de `jules`, e as funções secundárias de revisão de `codex` são atribuições diferentes. O grafo mantém uma rota para a classe ampla `review` após perder um trabalhador. Não garante três substitutos para cada função pedida; talvez seja preciso redistribuir ou escalar a decisão.

### Exercício prático 3: remova um vértice

Compare remover `augment` e remover `codex` do grafo DRAINING. Quais classes são perdidas e qual cobertura resta em cada caso? O grafo permite julgar se as notas de revisão substitutas teriam a mesma qualidade?

> **Resposta:** Remover `augment` perde `navigate`; permanecem `fix`, `groom` e `review`, logo `C=3/5`. Remover `codex` não perde classe inteira: `claude` ainda tem `fix`, e `jules` e `gemini` ainda têm `review`; `C=4/5`. Nenhum resultado mede qualidade, permissões, equivalência exata de funções, disponibilidade ou conclusão da tarefa.

## 4. Mantenha a semântica do seletor junto ao grafo

O [seletor consultivo fixado](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L1-L19) usa a política. Ele verifica, nessa ordem, trabalhador desconhecido, modo desconhecido, funções proibidas, pertencimento da função solicitada à via e bloqueio da classe ([ordem de decisão](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L77-L154)). Uma função primária atribuída e não bloqueada produz `allow`; uma secundária produz `recommend`, não `allow`. Uma função proibida produz `block` **antes** da verificação de pertencimento. Uma função ausente da via produz `warn`. Uma classe bloqueada produz `block` com código de backpressure. São respostas construídas pelo código, não permissões para alterar estado. O código de saída 0 significa **avaliado**; a decisão está no JSON. Erro de entrada ou da política pode retornar 2.

Em DRAINING, `builder_fixer`, função primária de `claude`, pertence a `net_new_feature`, bloqueada; `test_author`, secundária, pertence a `fix`, não bloqueada. O código prevê `block` para a primeira solicitação e `recommend` para a segunda. Isso **não** significa que `test_author` cumpra uma tarefa de construir uma funcionalidade: função solicitada e saída esperada ainda devem corresponder. `autonomous_merge_actor` é expressamente proibida para `codex`, portanto a solicitação prevê `block` mesmo com mudança de modo. Nenhuma aresta do grafo autoriza um merge.

### Exercício prático 4: diferencie caminhos e decisões

Em DRAINING, preveja as decisões para `(claude, builder_fixer)`, `(claude, test_author)` e `(codex, autonomous_merge_actor)`. Qual informação necessária à última solicitação se perde ao guardar só a projeção trabalhador-classe?

> **Resposta:** A primeira recebe `block`, pois `net_new_feature` está bloqueada; a segunda recebe `recommend`, pois `test_author` é uma função `fix` *secundária* não bloqueada; a terceira recebe `block`, pois `autonomous_merge_actor` está na lista proibida de `codex`. A projeção não registra funções proibidas nem a ordem das verificações. A falta de uma aresta de merge não equivale a mero aviso por função desconhecida nem a permissão.

## 5. Torne a medida refutável

Os números acima foram calculados do **JSON fixado**: expansão das funções primárias e secundárias, mapeamento para `work_class`, filtragem por `mode_blocks` e remoção de pares `(trabalhador, classe)` repetidos. Para verificar separadamente a interpretação do seletor, proponha uma pequena repetição offline com o mesmo script e política. Enumere os 22 pares `(trabalhador, função)` atribuídos nos quatro modos; trate `allow` e `recommend` como caminhos atribuídos não bloqueados, e `block` como caminhos cortados pelo modo. O código prevê 22 caminhos de função ativos em NORMAL, 21 em CONSTRAINED e DRAINING, e 8 em HALTED. As arestas trabalhador-classe projetadas devem ser 9, 8, 8 e 3; os caminhos **primários** sobreviventes devem ser 5, 4, 4 e 1. Essas são previsões do código fixado, **não** resultados de uma repetição executada nesta lição.

Guarde o JSON de cada decisão com o SHA e compare decisões, não códigos de saída. Inclua como controles separados uma solicitação proibida, uma função desconhecida e um modo desconhecido; nenhum pertence aos 22 pares atribuídos. Uma divergência refutaria a regra de caminhos assumida ou revelaria mudança no código repetido. Concordância validaria o modelo limitado naquela revisão, sem estabelecer escalonamento real, saúde dos trabalhadores ou correção da governança humana.

### Exercício prático 5: projete o oráculo da repetição

Suponha que `(claude, builder_fixer, DRAINING)` retorne código de saída 0 e decisão JSON `block`. Um colega conta um caminho ativo porque o processo terminou com sucesso. Qual a classificação correta? Dê uma contagem que, se divergir da previsão, refutaria a extração do grafo.

> **Resposta:** É um **caminho de função atribuída, porém bloqueado**. O código 0 indica que a solicitação consultiva foi avaliada, não autorizada. A repetição deve encontrar 21 caminhos atribuídos não bloqueados em DRAINING e 8 arestas trabalhador-classe após a projeção. Encontrar 22 caminhos ou 9 arestas, por exemplo, com a política e script fixados refutaria a extração. Isso, sozinho, não provaria incidente de produção.

## Evidências e limites

- A [política de vias](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) e o [seletor](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) estão fixados no commit Demerzel `ecdc6c27559bb1a11343cfad33687465893e9891`. As contagens são cálculos reproduzíveis daquele JSON, não medidas de agentes ativos. A repetição da seção 5 é proposta e não foi executada nesta lição.
- O grafo reúne funções atribuídas distintas em classes. Exclui funções proibidas e não codifica todas as entradas, a ordem de decisão nem a autoridade do seletor. `allow` e `recommend` são valores consultivos, não recibos de conclusão.
- Remoções de trabalhadores e cortes de modo são análises de sensibilidade de um grafo estático declarado. Antes de afirmar algo sobre encaminhamento operacional, confira a revisão atual da política, solicitação e decisão reais, presença e permissões do trabalhador, e artefato ou recibo da tarefa. Revisão técnica, tentativas de alunos, revisão da tradução, sincronização e compilação do Learn e leitura pública anônima continuam pendentes.
