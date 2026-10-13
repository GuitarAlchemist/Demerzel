---
module_id: inf-003-verdict-distribution-drift
department: information-theory
course: "Medir o desvio da distribuição de veredictos com a divergência de Jensen-Shannon"
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-003
version: "0.1.0"
---

# Medir o desvio da distribuição de veredictos com a divergência de Jensen-Shannon

> **Departamento de Teoria da Informação** | Nível: Intermédio | Duração estimada: 35 minutos | Estado: rascunho em português; revisões de conteúdo, aprendizagem e língua e publicação pendentes

## Objetivos

Depois desta lição, será capaz de:

- converter contagens comparáveis de veredictos do analisador IX em vetores de probabilidade alinhados;
- calcular a divergência direcional de Kullback–Leibler (KL) e a divergência simétrica de Jensen–Shannon (JS) nas unidades devolvidas pelo IX;
- explicar porque uma categoria nova pode causar erro num dos sentidos de KL, embora JS continue finita;
- usar a divergência para decidir que provas inspecionar, controlando os limites da análise e a composição dos lotes.

## A pergunta do projeto

O [analisador de redes de Petri do IX nesta revisão fixa](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L105) serializa o resultado de uma propriedade como `holds`, `fails` ou `unknown`. `Fails` pode trazer um contraexemplo; `unknown` significa que o analisador não decidiu a propriedade dentro dos limites de exploração. A mudança na mistura desses resultados entre duas execuções pode merecer atenção. Como quantificá-la sem tomar um número por prova de regressão?

A pergunta falseável é: **para uma propriedade, o mesmo conjunto de identidades de redes, a mesma revisão do analisador e os mesmos limites, quanto mudou a distribuição das categorias depois de alterar as redes?** O IX já fornece [funções KL e JS](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L222), também expostas como [funções escalares do DuckDB](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-duck/src/inference.rs#L186-L210). Calculamos aqui uma resposta reproduzível para contagens **sintéticas**. Não medimos um lote de produção do IX nem uma mudança de qualidade para utilizadores.

INF-001 aplicou entropia a uma distribuição de tokens de políticas. INF-002 mostrou distinções que o mapeamento compacto OPTIC-K do GA perde entre vetores. Aqui comparamos **duas distribuições sobre as mesmas categorias de veredictos**. A pontuação resume frequências agregadas; não revela qual rede mudou, porquê ou se a mudança é boa.

## 1. Escolher uma observação com significado estável

O [enum `Verdict<T>`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L95) tem três etiquetas. O método `holds()` só devolve verdadeiro para `Holds`; `Unknown` não se torna implicitamente aprovação. O relatório `Analysis` contém propriedades **diferentes**, incluindo `deadlock_free`, `bounded`, `quasi_live`, `live` e `reversible`. Somá-las misturaria questões com condições de prova distintas. Escolhemos apenas `deadlock_free`, um veredicto por rede, na ordem `[holds, fails, unknown]`.

O [ramo de ausência de bloqueios](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L465-L491) dá significado operacional às etiquetas. Encontrar uma marcação morta produz `Fails`, mesmo que a enumeração seja depois truncada; `max_reported_deadlocks` limita as testemunhas comunicadas e pode valer zero. Se não for encontrada uma marcação morta, `Holds` exige exploração completa; caso contrário, resulta `Unknown`. Esta observação é específica desta propriedade, não de todas as propriedades do analisador.

O lote seguinte, com dez redes, é **inventado** para este exercício numérico:

| Execução | Holds | Fails | Unknown | Total |
|---|---:|---:|---:|---:|
| Referência | 8 | 0 | 2 | 10 |
| Candidata | 6 | 2 | 2 | 10 |

Dividindo cada linha pelo respetivo total, obtemos `p = [0.8, 0, 0.2]` e `q = [0.6, 0.2, 0.2]`. Ambos os vetores precisam da mesma ordem. A função aceitaria arrays com etiquetas trocadas, mas compararia acontecimentos errados. Guarde as etiquetas com as contagens e valide a ordem.

### Exercício 1: formar vetores comparáveis

Escreva os dois vetores normalizados na ordem `[holds, fails, unknown]`. Que metadados devem acompanhar uma comparação real?

> **Resposta:** `p=[8/10,0/10,2/10]=[0.8,0,0.2]`; `q=[6/10,2/10,2/10]=[0.6,0.2,0.2]`. Guarde a propriedade, as identidades das redes, a ordem das categorias, o commit do analisador, os limites de exploração e o total de cada execução. O cálculo não confirma sozinho estas condições.

## 2. Ler o que o IX calcula

A implementação de [`normalize`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L173) divide cada componente de um vetor não negativo pela sua soma. Rejeita vetor vazio, valores negativos ou NaN e soma nula. O nosso protocolo também exige contagens finitas antes da chamada: o código não rejeita explicitamente infinito positivo. As duas divergências exigem vetores do mesmo comprimento e usam logaritmos naturais, logo os resultados são em **nats**. Divida por `ln(2)` para expressar o resultado em bits. No DuckDB, `ix_kl(p,q)` e `ix_js(p,q)` recebem `DOUBLE[]`; uma lista SQL `NULL` propaga `NULL`, enquanto um erro matemático passa a erro SQL. A existência do wrapper não demonstra uma tarefa agendada de comparação.

KL é direcional:

`D_KL(p || q) = Σ_i p_i ln(p_i / q_i)`.

Só contribuem categorias com `p_i > 0`. Neste exemplo, `D_KL(p || q)=0.8 ln(0.8/0.6)+0.2 ln(0.2/0.2)=0.23014565796142483` nats. No sentido inverso, a categoria `fails` exige `0.2 ln(0.2/0)`: matematicamente diverge, e o [IX devolve um erro](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L185-L209), não infinito. Trocar os argumentos muda a pergunta. Não oculte a nova categoria substituindo o erro por zero.

### Exercício 2: explicar a direção de KL

Calcule `D_KL(p || q)`. `D_KL(q || p)` devolve o mesmo número no IX?

> **Resposta:** `D_KL(p || q)=0.8 ln(4/3)=0.23014565796142483` nats. Em `D_KL(q || p)`, `q_fails=0.2` enfrenta `p_fails=0`; depois da troca de argumentos, o IX devolve o erro de parâmetro « q is zero where p is positive ». KL é assimétrica: aqui só o sentido referência-para-candidata tem suporte finito.

## 3. Usar JS como indicador finito e simétrico

JS forma o ponto médio `m=(p+q)/2` e faz a média de duas divergências KL: `D_JS(p,q)=0.5 D_KL(p||m)+0.5 D_KL(q||m)`. Neste exemplo, `m=[0.7,0.1,0.2]`. O ponto médio tem massa positiva em qualquer categoria presente num dos vetores, pelo que JS permanece finita neste par. O [código e comentário](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L210-L222) afirmam que JS é simétrica e limitada por `ln(2)` nats. Zero significa distribuições **normalizadas** iguais, não execuções nem tamanhos de lote iguais.

Um cálculo independente da fórmula dá `D_KL(p||m)=0.10682511409961822` e `D_KL(q||m)=0.04613902821563412`; a semissoma é `D_JS=0.07648207115762617` nats, ou `0.1103403047760241` bits. Estes resultados pertencem ao exemplo sintético, não a medições do IX em produção. Os [testes unitários fixados](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L568-L580) cobrem o máximo para vetores unitários disjuntos e zero para entradas iguais; não executámos essa suite aqui.

### Exercício 3: calcular e limitar JS

Calcule o ponto médio e JS. Trocar as execuções muda o valor? Qual é o máximo teórico em nats?

> **Resposta:** `m=[0.7,0.1,0.2]`; `D_JS=0.5(0.10682511409961822+0.04613902821563412)=0.07648207115762617` nats. A troca mantém o ponto médio e permuta os termos de igual peso; JS não muda. O máximo é `ln(2)=0.6931471805599453` nats para suportes disjuntos.

### Exercício 4: o que a normalização esconde

Compare `[80,0,20]` e `[8,0,2]` com `ix_js`. O que prova o resultado?

> **Resposta:** Ambos normalizam para `[0.8,0,0.2]`, portanto `ix_js` devolve `0`, sujeito à representação de vírgula flutuante. Isso prova apenas proporções iguais. Um lote tem 100 observações, o outro 10; JS perde esta diferença e não informa se as mesmas redes receberam os mesmos veredictos. Preserve totais e identidades emparelhadas fora da pontuação.

## 4. Decidir o que uma alteração deve desencadear

Suponha uma futura regra QA, aprovada separadamente, que assinala `JS > 0.05` nats para investigação. O valor **ilustrativo** ultrapassa esse limiar inventado. É um motivo para examinar dados, não prova de um controlo já implementado nem motivo automático para rejeitar uma alteração. Primeiro confirme as dez identidades de redes e a propriedade `deadlock_free`. Depois, confira a revisão do analisador e os `Limits`: o [relatório expõe truncamento e causa](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L161-L175). Aumentar `max_states` pode mudar `unknown` para `holds` ou `fails` sem alterar uma rede. Emparelhe os veredictos por ID e inspecione testemunhas de falha e razões de incerteza. Para rever testemunhas, escolha `max_reported_deadlocks` acima de zero e repita a execução se faltar uma. O histograma não identifica as redes alteradas nem valida os contraexemplos para a propriedade pretendida.

Num lote pequeno e estável, a tabela de três colunas e as alterações individuais podem ser mais claras do que um número. A pontuação pode ajudar a priorizar muitos lotes consistentes, desde que a tabela e as provas por rede permaneçam disponíveis. É uma hipótese de desenho, não substitui a revisão das testemunhas. Um falseador seria encontrar alertas repetidos causados sobretudo por composição ou orçamentos de exploração diferentes; nesse caso, reveja o protocolo em vez de ajustar o limiar até os alertas desaparecerem.

### Exercício 5: interpretar um alerta

O limiar hipotético é `0.05` nats e JS vale `0.07648207115762617`. Alguém afirma: « A candidata regrediu; há duas novas falhas. » Qual é o resultado aritmético verificável e o que deve ser confirmado antes de aceitar a alegação?

> **Resposta:** `0.07648207115762617 > 0.05`, logo o exemplo sintético acionaria a regra inventada de investigação. A tabela mostra dois `fails` na candidata e nenhum na referência, mas não identifica as redes alteradas. Confirme IDs, propriedade, revisão e limites iguais; emparelhe resultados; leia as testemunhas de falha disponíveis e as razões de `unknown`. Exija `max_reported_deadlocks > 0` e repita a execução se faltar uma testemunha necessária. Uma mudança de limite ou de lote pode explicar o desvio sem regressão no código. A pontuação não prova causalidade nem significância estatística.

## Limites e próximo passo

Verificámos a fórmula numa tabela sintética por um pequeno cálculo independente e lemos o código IX no commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Não executámos o analisador em dez redes, não consultámos uma tabela DuckDB real, não executámos a suite de testes IX, não estimámos incerteza amostral e não validámos um limiar de produção. Lotes repetidos mas diferentes exigiriam um plano de amostragem e emparelhamento. Uma próxima experiência limitada registaria uma propriedade por ID estável em duas revisões fixas com limites iguais, calcularia JS e inspecionaria manualmente cada veredicto alterado. Mantenha contagens, resultados por rede e testemunhas junto da pontuação. Esta tradução é um rascunho de IA: revisão humana, sincronização e build do Learn e leitura pública continuam pendentes.
