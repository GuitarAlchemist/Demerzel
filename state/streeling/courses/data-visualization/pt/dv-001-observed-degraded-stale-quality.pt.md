---
module_id: dv-001-observed-degraded-stale-quality
department: data-visualization
course: Medições, execuções degradadas e dados desatualizados
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-04-001
version: "0.1.0"
---

# Medições, execuções degradadas e dados desatualizados

> **Departamento de Visualização de Dados** | Nível: iniciante | Duração estimada: 35 minutos | Estado: revisão pendente

## Objetivos

Ao terminar esta lição, você poderá:

- distinguir uma taxa de aprovação medida de uma execução indisponível e de um valor histórico reapresentado;
- desenhar uma linha do tempo sem transformar uma medição ausente em falha nem unir silenciosamente pontos através de uma interrupção;
- verificar o denominador, a data da observação e o ambiente antes de comparar duas medições;
- oferecer uma descrição e uma tabela acessíveis como alternativas ao gráfico.

## A pergunta do projeto

O GA guarda resultados de controle de qualidade do chatbot em `state/quality/chatbot-qa/`. Quem olha o painel pergunta: “O chatbot piorou?” A visualização deve responder somente até onde os registros permitem. Esta lição usa quatro **registros históricos** fixados no commit do GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). Eles são dados para um exercício, não uma afirmação sobre o chatbot de hoje.

| Data do registro | `total_prompts` | `pass_pct` | `degraded` | O que o registro permite dizer |
|---|---:|---:|---|---|
| [2026-06-08](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-08.json) | 52 | `null` | `true` | O backend estava indisponível; nenhuma taxa de aprovação foi informada. |
| [2026-06-15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) | 52 | 75,00 | `false` | Uma taxa de aprovação foi informada para essa execução. |
| [2026-06-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-19.json) | 52 | 7,69 | `false` | Uma taxa baixa foi informada; o registro sozinho não explica a causa. |
| [2026-07-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) | 52 | 98,08 | `false` | Uma taxa maior foi informada em uma execução posterior. |

### Exercício prático

Classifique cada linha como taxa observada ou execução indisponível. Qual delas pode ser colocada em 0% no eixo das taxas?

> **Resposta:** As execuções de 15 de junho, 19 de junho e 19 de julho têm taxas informadas. A de 8 de junho ficou indisponível. Nenhuma linha informa 0%; colocar 8 de junho em zero inventaria uma medição.

## 1. Três estados diferentes dos dados

Uma **observação** é um valor realmente informado por uma execução. Uma **execução indisponível** indica que a medição não pôde ser feita ou considerada confiável nas condições registradas. Um **valor histórico reapresentado** é uma observação anterior mostrada para dar contexto; não é uma nova medição na data em que aparece no painel.

O arquivo de 8 de junho contém `pass_pct: null`, `degraded: true` e `degraded_reason: "backend_unavailable"`. Ele também contém `last_known_good_pass_pct: 94.0`, uma data anterior e `last_known_good_source: "carryforward"`. Esse 94% pertence à observação anterior. Desenhá-lo como ponto de 8 de junho faria a interrupção parecer desempenho estável. Desenhar `null` como zero faria a interrupção parecer uma falha do chatbot. As duas opções mudam a interpretação dos dados.

Mantenha dois campos no modelo da visualização: `quality_value` para a taxa medida e `run_status` para o estado observado, degradado ou desconhecido. Guarde a data de origem de qualquer referência histórica separada da data de exibição. Não deduza uma taxa a partir de `total_prompts`: a nota de 8 de junho relata erros do backend, não respostas do chatbot avaliadas.

### Exercício prático

Um cartão mostra “94% de aprovação em 8 de junho” porque o arquivo contém `last_known_good_pass_pct: 94.0`. Reescreva o cartão em uma frase.

> **Resposta:** “Controle de qualidade indisponível em 8 de junho: backend indisponível; último valor bom conhecido, 94% em 16 de maio.” A data da medição histórica deve estar visível; a taxa de 8 de junho continua desconhecida.

## 2. Desenhe qualidade e disponibilidade separadamente

Use o eixo de taxas somente para valores medidos. Deixe uma lacuna quando `pass_pct` for `null`, em vez de ligar pontos através dela. Uma segunda faixa alinhada às datas pode marcar a execução de 8 de junho como degradada com um ícone **e um rótulo textual**. Assim, quem lê recebe duas respostas distintas: qual qualidade foi medida e se havia uma medição disponível.

Para os quatro registros, basta este esboço em texto:

```text
Data          Faixa de qualidade     Faixa de disponibilidade
2026-06-08    sem ponto              DEGRADADO: backend indisponível
2026-06-15    75,00%                 observado
2026-06-19     7,69%                 observado; investigar
2026-07-19    98,08%                 observado
```

As datas são espaçadas; não são quatro leituras diárias consecutivas. Uma linha entre 19 de junho e 19 de julho sugeriria que os dias não mostrados foram medidos e seguiram uma trajetória suave. Se a série completa tiver lacunas, interrompa a linha nelas. Use as datas reais, em vez de posições igualmente espaçadas que apaguem o tempo decorrido. O [relatório histórico de tendências do GA no commit fixado](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) também marca fontes desatualizadas; um valor chamado “mais recente” precisa mostrar sua data de observação.

### Exercício prático

Esboce duas faixas para 8 e 15 de junho, incluindo datas e estados em texto. O 94% reapresentado deve ser ligado por uma linha aos 75% de 15 de junho?

> **Resposta:** Em 8 de junho, não há ponto na faixa de qualidade, e a faixa de disponibilidade diz “backend indisponível”. Em 15 de junho, há um ponto em 75% e o estado “observado”. O 94% é anotado com sua data original, 16 de maio; não é um ponto de 8 de junho nem o início de uma linha até 15 de junho.

## 3. Um número baixo é uma pergunta, não um diagnóstico

O registro de 19 de junho informa 7,69% e `degraded: false`. O gráfico deve mostrar o número, mas esse arquivo sozinho não permite concluir se houve regressão no código do GA, troca de modelo, mudança no conjunto de perguntas ou comportamento diferente de alguma dependência. `degraded: false` é apenas a classificação do produtor daquela execução; não é um certificado completo de saúde. Examine a configuração, a identidade das perguntas, os logs do backend, as regras de avaliação e as execuções vizinhas antes de atribuir uma causa.

As três linhas observadas informam 52 perguntas cada. Isso ajuda a contextualizar, mas quantidades iguais não provam que as perguntas ou as regras de avaliação eram as mesmas. Uma comparação deveria fixar a revisão do conjunto de perguntas e do avaliador, além da quantidade. Se essas informações faltarem, marque a comparação como provisória. Um eixo de porcentagens sem denominador nem fonte pode esconder a fragilidade de uma amostra pequena.

### Exercício prático

Avalie a frase: “O GA se recuperou de uma regressão de software confirmada entre 19 de junho e 19 de julho.” O que foi observado e o que ainda exige evidência?

> **Resposta:** Os arquivos informam 7,69% em 19 de junho e 98,08% em 19 de julho. “Se recuperou” e “regressão de software” atribuem causa e continuidade que esses quatro registros não estabelecem. Compare o mesmo conjunto de perguntas, avaliador e ambiente, e examine as falhas antes de afirmar isso.

## 4. Torne o gráfico legível sem depender da cor

A cor pode ajudar, mas um marcador de indisponibilidade também precisa de rótulo ou forma. A [orientação do W3C sobre uso da cor](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) exige outro sinal visual quando a cor transmite informação. A [orientação do W3C sobre conteúdo não textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content) explica que um gráfico precisa de uma alternativa textual que comunique sua finalidade; uma tabela pode apresentar os valores exatos.

Para estes dados, uma descrição curta útil seria: “Controle de qualidade histórico do chatbot do GA: 8 de junho indisponível; as taxas informadas foram 75% em 15 de junho, 7,69% em 19 de junho e 98,08% em 19 de julho. A causa do resultado baixo de 19 de junho não foi estabelecida aqui.” Mantenha a tabela acima junto ao gráfico. Uma pessoa que usa leitor de tela deve conseguir acessar as datas, os valores e os estados sem interpretar cores nem dicas exibidas apenas ao passar o mouse.

### Exercício prático

Analise um ponto vermelho sem texto em 8 de junho. Que informação deve ser acrescentada?

> **Resposta:** Acrescente texto visível como “backend indisponível” e um rótulo disponível para tecnologias assistivas. Mantenha ausente a taxa de 8 de junho. Ofereça uma tabela ou descrição equivalente com a data e o estado.

## Principais aprendizados

- A falta de dados de qualidade não é uma taxa zero nem uma taxa de sucesso.
- Uma referência histórica conserva sua data original de observação.
- O gráfico deve mostrar a disponibilidade da medição junto da qualidade medida.
- Uma porcentagem observada baixa pode motivar investigação sem provar a causa.
- Datas, denominadores, revisões da fonte e texto acessível fazem parte da afirmação.

## Leitura adicional e evidências do projeto

- GA: [registros históricos do controle de qualidade do chatbot](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa) e [relatório de tendências de qualidade](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). O relatório é datado, não um estado em tempo real.
- W3C, [Understanding Success Criterion 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color).
- W3C, [Understanding Success Criterion 1.1.1: Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content).

*Pesquisa: `data-visualization-2026-10-04-001`. A revisão de conteúdo e de idioma está pendente; não apresente este rascunho como curso verificado.*
