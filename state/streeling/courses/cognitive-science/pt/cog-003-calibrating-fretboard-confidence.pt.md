---
module_id: cog-003-calibrating-fretboard-confidence
department: cognitive-science
course: "Calibrar a confiança ao identificar notas no braço da guitarra"
level: intermediate
prerequisites: [cog-002-feedback-integrity-fretboard-recall]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-12-003
version: "0.1.0"
---

# Calibrar a confiança ao identificar notas no braço da guitarra

> **Departamento de Ciências Cognitivas** | Nível intermediário | 40 minutos | Rascunho em português; revisão e publicação pendentes

## Objetivos

Você transformará “tenho certeza” em uma probabilidade anotada **antes** do feedback, calculará uma pontuação Brier binária com um gabarito GA verificado, distinguirá seis exemplos inventados de resultados medidos com alunos e planejará um teste capaz de refutar uma hipótese de calibração. [COG-002 (em inglês)](../en/cog-002-feedback-integrity-fretboard-recall.md) verifica o próprio gabarito exibido. Aqui perguntamos: **a confiança declarada corresponde à frequência com que as notas escolhidas estão corretas?**

## A decisão do projeto

Imagine um exercício GA de “diga o nome desta nota” no braço SVG. Dois guitarristas acertam quatro de seis posições. Um tem baixa confiança nas duas respostas erradas; o outro tem certeza delas. A acurácia bruta os iguala, mas talvez precisem de orientações diferentes. Para decidir, precisamos de um evento definido, gabarito confiável e teste que verifique se o feedback ajuda alunos reais.

No commit GA [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), a [página de demonstração](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) declara seis posições. O [componente SVG](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) usa `string: 0` para a corda E aguda, traste 0 para corda solta e afinação padrão `E, B, G, D, A, E` de agudo a grave. A página não muda essa afinação. A sexta posição mostra **C** na corda 5, traste 3, embora três semitons acima do E grave resultem em **G**. Trata-se de divergência no código, não de observação de usuários. A sequência corrigida é `E, C, G, E, C, G`.

A página se identifica como teste de um componente SVG legado. O [tratador de clique](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) envia somente corda e traste. Essas fontes não mostram entrada de confiança, sessão pontuada, painel de calibração ou curso implantado. **Todas as respostas de alunos a seguir são dados sintéticos para ensino.**

## 1. Defina a previsão antes de revelar a resposta

Em cada tentativa, peça uma nota `a_i` para certa corda e traste. Depois peça `p_i`, entre 0 e 1: “Qual a probabilidade de que **a nota que escolhi** coincida com o gabarito verificado independentemente?” A previsão trata da correção da escolha, não da possibilidade de a guitarra soar nem da confiabilidade do rótulo da demonstração. Registre `a_i` e `p_i` antes de revelar a nota; depois defina `y_i=1` se a escolha concordar com o gabarito e `y_i=0` caso contrário.

Para construir o gabarito, guarde ordem das cordas, afinação, traste e revisão do código. O E grave é a corda 5; E tem classe de altura 4. No traste 3, `(4+3) mod 12=7`, ou G. O C exibido não pode ser usado como resposta sem a correção explicada em COG-002.

A interface precisaria de entradas **novas** para nota e confiança. O clique atual fornece uma coordenada, não uma previsão. Um registro proposto é `{source_sha, tuning, string, fret, chosen_note, confidence_before_feedback, verified_note, answer_time, feedback_time}`: projeto de estudo, **não** uma API GA existente. É preciso ocultar a resposta antes de captar `p_i`, pois os marcadores atuais já trazem rótulos visíveis.

### Exercício 1 — Defina o evento

Um aluno escolhe C na corda 5, traste 3, com `p=0.9`. Qual nota é verificada, quanto vale `y` e o clique atual registra `p`?

> **Resposta:** A corda 5 é o E grave. `(4+3) mod 12=7` dá G, portanto, para C, `y=0`. O clique envia apenas `{string, fret}`, sem nota escolhida ou confiança. O `p=0.9` é hipotético.

## 2. Pontue seis tentativas declaradamente inventadas

A **pontuação Brier binária** é `BS=(1/n) Σ_i (p_i-y_i)^2`, entre 0 e 1; **menor é melhor**. Ao contrário da contagem simples de acertos, diferencia um erro com confiança 0.9 de outro com 0.6. Mantenha a mesma definição de resultado em todos os itens. As seis escolhas e probabilidades abaixo são **inventadas**; apenas coordenadas, afinação e gabarito corrigido vêm do GA.

| Tentativa | Corda, traste | Nota verificada | Escolha fictícia | `p_i` | `y_i` | `(p_i-y_i)^2` |
|---:|---|---|---|---:|---:|---:|
| 1 | 0, 0 | E | E | 0.9 | 1 | 0.01 |
| 2 | 1, 1 | C | C | 0.8 | 1 | 0.04 |
| 3 | 2, 0 | G | A | 0.7 | 0 | 0.49 |
| 4 | 3, 2 | E | E | 0.6 | 1 | 0.16 |
| 5 | 4, 3 | C | C | 0.9 | 1 | 0.01 |
| 6 | 5, 3 | G | C | 0.9 | 0 | 0.81 |

O aluno fictício acerta `4/6≈0.6667`. As perdas somam `0.01+0.04+0.49+0.16+0.01+0.81=1.52`, logo `BS=1.52/6≈0.2533`. Isso **não** estima a habilidade de uma pessoa real. Se o C incorreto da demonstração fosse usado para pontuar a tentativa 6, a perda cairia de 0.81 para 0.01 e a pontuação aparente viraria `(1.52-0.81+0.01)/6=0.12`. Uma boa regra de pontuação não conserta um gabarito ruim.

### Exercício 2 — Calcule a pontuação

Calcule acurácia, soma das perdas quadráticas e média Brier. Qual erro contribui com mais perda?

> **Resposta:** Quatro acertos em seis dão `4/6≈0.6667`; a soma é `1.52` e a média `1.52/6≈0.2533`. A tentativa 6 contribui `0.81`, mais que os `0.49` da tentativa 3, por trazer confiança 0.9 na resposta errada, contra 0.7.

### Exercício 3 — Examine uma faixa de confiança

Entre as tentativas com `p_i=0.9`, qual fração está correta e quanto ela fica abaixo de 0.9? Três tentativas bastam para estabelecer calibração individual estável?

> **Resposta:** Tentativas 1, 5 e 6 têm 0.9; duas estão corretas: `2/3≈0.6667`. A diferença é `0.9-2/3≈0.2333`. Três exemplos inventados e relacionados são insuficientes para uma curva individual estável.

### Exercício 4 — Detecte contaminação do gabarito

Se a tentativa 6 fosse avaliada contra o C exibido, não contra o G verificado, como mudariam resultado, perda e média? Isso mostraria melhoria do aluno?

> **Resposta:** A escolha C seria marcada `y_6=1`; a perda mudaria de `(0.9-0)^2=0.81` para `(0.9-1)^2=0.01`. A soma seria `0.72`, média `0.72/6=0.12`. Nenhuma previsão mudou: a melhoria aparente é erro do gabarito.

## 3. Por que minimizar esse erro quadrático?

Seja `q` a probabilidade real de uma resposta escolhida estar correta numa classe definida de futuras tentativas, e `p` a probabilidade relatada. A perda Brier esperada é `q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q)`. O segundo termo independe de `p`; o mínimo esperado único ocorre em `p=q`. Assim, a regra recompensa probabilidades honestas **em expectativa**, sem garantir vitória em cada amostra de seis tentativas. Ela tampouco identifica se um erro veio da ordem das cordas, esquecimento ou feedback enganoso.

No exemplo hipotético `q=0.7`, informar `p=0.7` produz perda esperada `0.7(0.3)^2+0.3(0.7)^2=0.21`; informar `p=0.9` produz `0.7(0.1)^2+0.3(0.9)^2=0.25`. O excesso 0.04 é `(0.9-0.7)^2`. As seis tentativas inventadas **não** medem `q=0.7` entre guitarristas reais.

Um Brier menor, isoladamente, não significa mais conhecimento musical. Aproximar todas as respostas de 0.5 pode diminuir a punição por erros confiantes sem aumentar acertos. Relate também acurácia, desempenho por corda/traste e probabilidades originais **antes** do feedback. Alterar `p_i` depois dele invalidaria a medida da previsão original.

### Exercício 5 — Comprove o sentido da regra

Com `q=0.7` hipotético, compare a perda esperada para `p=0.7` e `p=0.9`. Qual é menor, e quanto?

> **Resposta:** Para `p=0.7`, `0.7(1-0.7)^2+0.3(0.7)^2=0.21`. Para `p=0.9`, `0.7(1-0.9)^2+0.3(0.9)^2=0.25`. A primeira é menor por 0.04. O conjunto de ensino não mediu `q`.

## 4. Projete um teste capaz de falhar

Hipótese falsificável: **mostrar feedback explícito de calibração da confiança após cada resposta verificada reduzirá o Brier em posições reservadas no dia seguinte sem reduzir acurácia das notas**, comparado a mostrar somente a nota correta. Ambos os grupos devem escolher nota e declarar confiança antes do feedback. O grupo de calibração poderia ver sua confiança, correção e pontuação acumulada; o grupo comparativo, a mesma nota e correção sem resumo de confiança. É uma proposta, não comportamento atual do GA.

Primeiro corrija o rótulo errado ou use um gabarito auditado separadamente. Prepare dois estados de pergunta sem rótulos de notas, com a mesma afinação declarada, e confirme que a resposta não aparece antes da previsão. Recrute alunos reais, registre consentimento e experiência no braço, e atribua condições antes do treino. Contrabalanceie conjuntos de itens e reserve posições para o teste no dia seguinte. Anote revisão de fonte, item, resposta, confiança, horário, feedback mostrado e intervalo exato. Reconhecer um ponto no diagrama não prova saber tocar ou ouvir aquela nota.

Declare antes o desfecho primário: média Brier no dia seguinte em posições reservadas, com acurácia como salvaguarda. A hipótese **não recebe apoio** se o grupo de calibração não reduzir o Brier frente ao grupo comparativo, ou se eventual ganho vier com menor acurácia segundo a salvaguarda prevista. Relate incerteza e números de alunos e itens. Um piloto pode revelar confusão na interface ou efeito teto, pedindo estudo revisto em vez de sucesso anunciado depois. **Nenhum** aluno, alocação, variante ou medição no dia seguinte foi realizado para esta aula.

### Exercício 6 — Especifique um resultado refutador

Um agente diz: “O Brier sintético de `0.2533` prova que nosso feedback melhora a lembrança.” Dê duas razões contra a afirmação e um resultado do estudo que faria a hipótese falhar.

> **Resposta:** As seis escolhas e probabilidades são inventadas; a página GA não tem intervenção sobre confiança nem medição posterior. A hipótese falharia se o grupo de calibração não obtivesse Brier menor em posições reservadas no dia seguinte, ou se o ganho viesse com queda de acurácia segundo a salvaguarda prevista. É necessário gabarito corrigido e probabilidades registradas antes do feedback.

## Limites da evidência

As fontes GA fixadas mostram seis coordenadas, ordem padrão das cordas, rótulos visíveis e conteúdo do clique. O gabarito corrigido e a aritmética Brier são verificáveis. As seis escolhas/probabilidades, `q=0.7`, as variantes de interface e o estudo são construções didáticas. Aqui não há confiança medida de aluno real, mudança de calibração, benefício da intervenção, execução no navegador, revisão de assunto ou idioma, build do Learn ou leitura pública. Antes de chamar esta aula de revisada ou publicada, serão necessários artefatos e revisores separados.
