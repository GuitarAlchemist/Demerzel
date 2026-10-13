---
module_id: sem-003-status-signs-and-evidence
department: semiotics
course: "Sinais de estado e evidências no trabalho com agentes"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-12-003
version: "0.1.0"
---

# Sinais de estado e evidências no trabalho com agentes

> **Departamento de Semiótica** | Nível: intermediário | Etapa: Albedo | Duração: 35 minutos | Rascunho em português pendente de revisão

## Objetivos

Você aprenderá a distinguir uma palavra de estado do acontecimento que ela pretende representar, ler um registro de produção Streeling sem transformar uma checagem limitada em veredito final e escrever uma passagem de trabalho entre agentes cujas afirmações possam ser verificadas contra um artefato fixado. Também distinguirá o que demonstram um esquema, uma compilação local e uma leitura pública.

## A decisão do projeto

Um agente redigiu uma aula Streeling. Outro leu a fonte e as respostas e relatou “nenhum problema encontrado”. O que o coordenador deve dizer ao agente seguinte: **rascunho**, **pronto**, **revisado** ou **publicado**? A escolha determina se um aluno será enviado ao curso público, se um revisor examinará a fonte ou se o autor fará correções. Uma palavra forte demais pode levar à omissão de uma etapa pendente.

Esta aula utiliza o [registro real de produção do SEM-002](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/course-productions/cp-semiotics-2026-10-11-002.json), seu [relato de revisão limitada por IA](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/sem-002-subject-review-2026-10-11.md), o [esquema de produção](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/schemas/course-production.schema.json) e o [relator de progresso](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py). Todos os links de fontes Demerzel fixam o commit `c453a91d1c4d913af72c28779eff826659c1d654`. A análise trata desse instantâneo; não afirma que o estado atual da produção ou do site seja igual.

## 1. O que um sinal de estado representa?

[SEM-001 (em inglês)](../en/sem-001-signs-in-governance.md) apresenta signo, objeto e interpretação. Em uma passagem entre agentes, `reviewed` é um **símbolo** cujo significado depende de uma convenção compartilhada. Um link para o relato de revisão pode funcionar como **índice** que aponta para um artefato específico. Uma marca verde também é um sinal compacto, mas precisa de sentido acordado, critério nomeado e procedência. Nenhum desses sinais executa uma revisão por si só.

As palavras da pergunta inicial são afirmações possíveis, **não** uma nova máquina de estados Streeling:

| Palavra na mensagem | Possível afirmação verificável | Evidência necessária para usá-la sem ressalva |
| --- | --- | --- |
| `draft` | Existe um arquivo fonte | Caminho e revisão exata |
| `ready` | Uma etapa de entrada definida foi concluída | Etapa, entradas, resultado e data; pronto *para quê*? |
| `reviewed` | Um revisor examinou um escopo declarado | Relato, revisor, escopo, resultado e revisões restantes |
| `published` | O aluno pode obter a versão pretendida | Rota implantada, leitura anônima e procedência da fonte correspondente |

São **testes de comunicação**, não quatro valores implementados no repositório. O esquema fixado permite `in_progress`, `review_pending`, `published`, `rejected` e `failed`, mas não `draft`, `ready` ou `reviewed`. Conforme a evidência, diga “existe um rascunho inglês” ou “pronto para revisão limitada da fonte”, sem insinuar uma transição inexistente no esquema.

### Exercício 1 — Identifique o objeto

Uma passagem diz apenas “SEM-002 está pronto”. Dê dois sentidos materialmente diferentes de `ready` e reescreva a frase para tornar um deles verificável. O esquema contém `ready`?

> **Resposta:** Pode estar pronto para revisão da fonte ou para implantação após todas as revisões. Exemplo verificável: “A fonte inglesa do SEM-002 no commit `c453a91d1c4d913af72c28779eff826659c1d654` está pronta **para uma revisão limitada da fonte e das respostas**; revisão final de produção e publicação continuam incompletas.” O esquema não possui o valor `ready`.

## 2. Leia o registro e depois o relato

Na revisão fixada, o registro SEM-002 indica `status: in_progress`. Pesquisa, estrutura e conteúdo estão concluídos; tradução está incompleta com `languages: ["en"]`; revisão e publicação têm `completed: false`. O relato separado da IA registra **nenhum problema no escopo limitado de fonte e respostas**. Ele deixa explicitamente pendentes a revisão humana do assunto, o teste com alunos, a revisão por falantes fluentes e as verificações públicas do Learn. Uma inspeção delimitada ocorreu, mas a fase final de revisão permanece incompleta.

O erro semiótico é deixar `reviewed` absorver todo escopo possível. “A verificação preliminar por IA da fonte e das respostas não encontrou problemas” é precisa. “Curso revisado” pode sugerir aprovação editorial ou humana final e encaminhar mal o agente seguinte. A identidade do revisor também não basta: o relato deve indicar o que foi e não foi examinado. Um sinalizador no registro é uma afirmação escrita em arquivo; precisa de evidência rastreável antes de virar fato confiável em uma passagem.

O [relator de progresso](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py#L89-L107) conta aprovação somente quando `phases.review.completed` é verdadeiro **e** `phases.review.verdict` é `approved`. SEM-002 não satisfaz esse predicado no instantâneo. O contador lê registros; não avalia independentemente a correção do conteúdo. Mesmo se alguém escrevesse esses valores manualmente sem uma revisão confiável, o número não provaria que ela aconteceu.

### Exercício 2 — Delimite a afirmação de revisão

Para o SEM-002 fixado, escolha: (A) “Não houve revisão”; (B) “O curso passou por todas as revisões”; (C) “Uma checagem limitada por IA da fonte e das respostas não encontrou problemas; a fase de revisão de produção continua incompleta”. Por que as outras opções falham?

> **Resposta:** C. A contradiz o relato de inspeção limitada. B excede seu escopo: revisão humana do assunto, alunos, idiomas e site público continuam pendentes, e `phases.review.completed` é falso. “Nenhum problema” vale apenas para o escopo indicado, não para todo possível defeito.

## 3. Forma válida não é transição verificada

O esquema limita tipos de campos e valores permitidos de `status`. Ele exige status, pesquisa, estrutura, conteúdo e data/hora. Quando as fases de revisão e publicação aparecem, seus campos `completed` são booleanos. **Não** contém uma regra geral entre campos como “`status: published` implica `publish.completed: true`”. Portanto, um registro pode ser sintaticamente válido e fazer uma afirmação operacional contraditória. Isso descreve o alcance do esquema, não prova que exista tal registro defeituoso em produção.

A [checagem prévia dos cursos](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_preflight.py) valida esquemas, nomes de arquivos, frontmatter, arquivos de idiomas declarados, contagem de palavras em inglês e sinais de exercícios respondidos. Sua única regra explícita de consistência de estado exige que `in_progress` tenha revisão e publicação não concluídas. Ela não acessa o site público nem julga o assunto. Passar nessa checagem não significa “aprovado pelos alunos” ou “ao vivo no Learn”.

Imagine uma alteração **sintética** no registro SEM-002: somente `status` muda para `published`, mantendo `phases.publish.completed: false`. O esquema aceita cada valor e não os relaciona. Como a regra de consistência da checagem prévia só vale para `in_progress`, essa contradição fictícia escaparia daquela regra. Não a crie no repositório. Inspecione registro, comprovante de implantação e rota anônima em vez de confiar na palavra `published`.

### Exercício 3 — Separe forma e verdade

O exemplo sintético `status: published` com `phases.publish.completed: false` viola uma regra do esquema JSON fixado? Um resultado de esquema válido provaria que SEM-002 está disponível ao público?

> **Resposta:** Não há regra nesse esquema que relacione os dois campos. Sua validação comprova apenas a estrutura que ele examina; não demonstra implantação nem disponibilidade pública anônima. A contradição deve ser investigada, não anunciada como publicação.

## 4. Diferencie referentes locais e públicos

O [relato público de referência](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/public-baseline-2026-10-11.md) registra uma leitura anônima do índice Streeling em 11 de outubro de 2026, cita um commit de origem e observa que presença pública não equivale à revisão pelo autor. Na mesma data, a checagem local do Learn gerou páginas DV-001, mas requisições GET anônimas às novas rotas públicas retornaram 404. “Página gerada localmente” aponta para um artefato de compilação; “publicado” aponta para uma versão acessível publicamente. O primeiro fato não implica o segundo.

Esse relato é evidência **histórica sobre DV-001**, não teste atual de SEM-002 ou do site de hoje. Para uma publicação do SEM-003, o coordenador precisaria identificar a rota, implantar o site, consultá-la anonimamente e verificar marcador de versão ou SHA da fonte e conteúdo servido. HTTP 200 pode exibir uma versão antiga. O SHA aponta para a revisão escrita; a leitura da rota a liga ao que o aluno recebe. O relato do revisor aponta para outro evento. Um não substitui o outro.

### Exercício 4 — Identifique o observado

No exemplo DV-001 datado, a página local existe e a rota anônima retornou 404. Qual frase é sustentada: “a aula foi publicada”, “a compilação local produziu uma página, mas aquela rota pública não a serviu na data da leitura”, ou “não havia arquivo fonte”? O que verificar após uma implantação posterior?

> **Resposta:** A frase do meio. Página local e 404 dizem respeito a superfícies diferentes naquela data. Depois da implantação, consulte anonimamente a rota pública pretendida e compare conteúdo ou SHA de procedência à revisão desejada; compilação local ou comando de implantação não bastam.

## 5. Escreva uma passagem utilizável

Uma mensagem útil forma uma pequena cadeia: **artefato e revisão → checagem nomeada → resultado observado → etapa faltante → próxima ação**. Isso é um padrão de redação para o exercício, **não um novo DSL normativo**. O destinatário consegue seguir as referências e recusar uma interpretação antiga ou ampla demais. Exemplo baseado no instantâneo SEM-002:

> “A fonte inglesa do SEM-002 existe em Demerzel no commit `c453a91d1c4d913af72c28779eff826659c1d654`. Uma checagem limitada por IA da fonte e de cinco respostas não encontrou problemas. O registro segue `in_progress`, com revisão e publicação incompletas. Próximo passo: obter revisão humana do assunto e dos alunos e então verificar a implantação pretendida no Learn por leitura anônima.”

A mensagem não inventa o valor `ready`. Se uma futura revisão aprovar apenas a exatidão factual, descreva esse escopo, sem transformá-lo em aprovação linguística. Uma nova revisão do texto não fica automaticamente coberta por um relato antigo. Links a revisões imutáveis ligam revisor, fonte e leitura pública ao mesmo objeto ou mostram onde a cadeia se rompeu.

### Exercício 5 — Corrija a mensagem de um agente

Reescreva “SEM-002 foi revisado e publicado; os testes estão verdes” usando apenas o registro e o relato fixados. Declare uma próxima ação exata e uma incerteza, sem inventar teste ou implantação.

> **Resposta:** “No commit Demerzel `c453a91d1c4d913af72c28779eff826659c1d654`, SEM-002 tem um rascunho inglês e um relato de checagem limitada por IA da fonte e respostas sem problemas encontrados. O registro continua `in_progress`, com `review.completed=false` e `publish.completed=false`. Esses artefatos não estabelecem nova execução de testes nem leitura pública da rota SEM-002. Próximo passo: solicitar revisão humana do assunto e de alunos contra esta revisão.” A mensagem original amplia uma checagem limitada para revisão final e afirma publicação e testes sem prova.

## Limites e aplicação

A aula analisa arquivos Demerzel fixados e um relato público datado; não executa passagem real entre agentes, teste com alunos, validação de SEM-003 por especialista humano em semiótica ou publicação. Os cinco exercícios testam se o leitor liga cada palavra de estado ao referente e à evidência. Para avaliar se o método melhora a coordenação, compare em um experimento controlado um grupo que recebe estado sem qualificação e outro que recebe a cadeia de provas; observe se escolhem a próxima etapa correta e citam a revisão certa. **Até executar esse experimento, o benefício para a coordenação permanece uma hipótese.**
