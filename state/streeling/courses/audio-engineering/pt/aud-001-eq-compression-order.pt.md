---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Testar a ordem da EQ e da compressão num sinal de guitarra"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-004
version: "1.1.0"
---

# Testar a ordem da EQ e da compressão num sinal de guitarra

> **Departamento de Engenharia de Áudio** | Nível: Intermediário | Duração: 35 minutos | Rascunho revisto em português; revisão técnica, pedagógica e linguística e publicação pendentes

## Objetivos e pergunta do projeto

Você distinguirá um filtro de um processador dependente do nível, demonstrará com um pequeno cálculo que a ordem importa e projetará uma comparação offline que uma futura implementação de compressor poderia refutar. **Pergunta do projeto:** se o GA avaliar o processamento de uma gravação da corda E2 solta ou de sua renderização pelo motor de guitarra, colocar uma EQ escolhida antes da compressão altera o ataque e o comportamento do nível em comparação com colocar a *mesma* EQ depois? A decisão exige saídas medidas com a mesma entrada, não uma regra genérica sobre qual ordem soa mais natural.

A [fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) oferece um par concreto: um WAV mono gravado da E2 solta e um WAV mono E2 renderizado nativamente pelo GA, cada um com quatro segundos a 44.100 Hz. O primeiro ataque gravado começa **aproximadamente em 1.1 s**, com outro perto de **2.75 s**; a renderização começa no instante zero do arquivo. As [medições da fixture](../../../fixtures/guitar-acoustics/gas-001/measurements.json) mostram diferenças de parciais e decaimento em janelas escolhidas, mas não classificam o realismo nem indicam que qualquer arquivo precise de compressão. Preserve os WAVs originais. Nesta lição, a gravação é a primeira entrada proposta; a renderização serviria para uma repetição posterior e separadamente identificada. Não atribua à ordem uma diferença entre áudio processado e não processado.

O [motor de áudio do navegador GA no commit fixado `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) carrega o motor WASM em um [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), liga-o à saída e oferece um caminho MediaRecorder. O render GAS-001 veio de uma **compilação nativa da mesma fonte Rust**, não de uma captura do worklet. A fonte documenta o percurso do sinal de guitarra, não uma cadeia EQ/compressor implementada no demo. No [commit IX `bd1336b`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs), `FirFilter` fornece projeto passa-baixas e passa-altas e um método `apply` no domínio das amostras. Pode ser um bloco de construção para filtragem offline. Esses artefatos fixados não estabelecem uma implementação de compressor; antes de um A/B real ela precisa ser especificada e revisada.

## 1. Defina precisamente as duas operações

Um filtro FIR é linear: com coeficientes `h`, a saída é `E(x)[n] = Σ_k h[k] x[n-k]`, com regra explícita para as bordas. O `FirFilter::apply` do IX inicia uma saída zerada e só inclui termos com índice de entrada não negativo. Um filtro passa-baixas ou passa-altas pode mudar o nível que chega a um detector posterior. A resposta exata depende dos coeficientes, e o filtro também pode deslocar ou espalhar o ataque. Chamar qualquer ajuste de filtro de “EQ corretiva” não demonstra melhora no sinal de guitarra.

Um compressor **depende do nível**. Seu ganho depende da entrada e, em um projeto convencional, de uma envoltória do detector com estado de ataque e soltura. A forma de onda pode mudar conforme limiar, razão, tipo de detector, constantes de tempo, ligação entre canais, ganho de compensação e inicialização. Registre esses detalhes. Um compressor não é automaticamente seletivo em frequência: um detector de banda inteira responde ao nível da forma de onda, que pode ser afetado por várias parciais. Dizer que ele “ouve 200 Hz” é uma simplificação, não uma identificação comprovada da componente que acionou a redução de ganho. Filtragem do sidechain, compressão multibanda e EQ dinâmica seriam outros experimentos.

Seja `E` a EQ escolhida e `C` o compressor. As duas cadeias propostas são `A = E(C(x))` (**Comp→EQ**) e `B = C(E(x))` (**EQ→Comp**). Use o mesmo `x`, coeficientes de EQ, parâmetros do compressor, taxa de amostragem e formato de canais nas duas. `C` recebe o `x` bruto em A e o `E(x)` filtrado em B. A EQ final de A não desfaz uma decisão já tomada pelo detector. Em B, o compressor pode reagir a picos criados ou removidos pela EQ. Nenhuma ordem é padrão universal; a intenção sonora e os compromissos medidos guiam a escolha.

### Exercício prático 1: identifique a entrada do detector

O que entra em `C` nas cadeias A e B? Se a EQ aumenta uma parcial da guitarra, qual cadeia *poderia* mudar a redução de ganho por causa disso?

> **Resposta:** Em A, `C` recebe o `x` sem filtragem; em B, recebe `E(x)`. O aumento da parcial pode afetar diretamente o detector de banda inteira em B. Em A, a EQ vem depois e não pode mudar a decisão anterior de ganho. É uma afirmação sobre o caminho causal, não uma previsão de audibilidade ou do tamanho da redução.

## 2. Demonstre a dependência da ordem com uma fixture sintética

Use um sinal de quatro amostras deliberadamente **sintético**, `x=[0,2,0,0]`, com histórico anterior zero. Defina o FIR `E` por `h=[0.5,0.5]`, de modo que `E(x)[n]=0.5x[n]+0.5x[n-1]` para amostras disponíveis. Essa média de dois termos é um exemplo matemático de passa-baixas, **não** uma EQ recomendada para guitarra nem o resultado do projetista `lowpass` do IX. Defina um compressor didático sem memória, com limiar `T=1`, razão `R=2:1`, sem ganho de compensação e sem ataque/soltura: `C(v)=sign(v) × (|v| if |v|<=1 else 1+(|v|-1)/2)`. Ele mapeia a amostra positiva `2` para `1.5`. Um compressor real de envoltória teria estado adicional e poderia dar outros valores.

Calcule A: `C(x)=[0,1.5,0,0]` e então `E(C(x))=[0,0.75,0.75,0]`. Calcule B: `E(x)=[0,1,1,0]` e então `C(E(x))=[0,1,1,0]`, pois as duas amostras filtradas não excedem o limiar. As saídas diferem em `0.25` nas posições 1 e 2. É um contraexemplo exato a `E∘C = C∘E` para esses operadores. **Não** mede a gravação GAS-001, não prevê um plugin não especificado e não prova que B soa melhor.

Os picos diferentes, `0.75` em A e `1` em B, alertam contra julgar a ordem com volumes de reprodução distintos. Para escuta, declare um ajuste de nível aplicado **depois** de cada cadeia completa e registre os ganhos usados. Não ajuste limiares diferentes para forçar reduções de ganho parecidas: isso mudaria a pergunta experimental. Se ambas as cadeias ficarem abaixo do limiar em uma passagem real, podem ser idênticas ou quase idênticas apesar deste contraexemplo.

### Exercício prático 2: calcule as duas cadeias

Com `x`, `h` e `C` declarados, escreva A e B. Quanto vale `B[1]-A[1]` e o que o cálculo permite concluir?

> **Resposta:** `A=[0,0.75,0.75,0]`; `B=[0,1,1,0]`; `B[1]-A[1]=0.25`. Os operadores especificados não comutam nessa entrada sintética. Só esse cálculo não oferece veredito de escuta nem resultado para um compressor real de envoltória ou para o WAV de guitarra.

### Exercício prático 3: trate a borda

Com histórico zero e `h=[0.5,0.5]`, quais são `E([2,0])[0]` e `E([2,0])[1]`? Por que um procedimento offline precisa documentar bordas e latência?

> **Resposta:** Ambos valem `1`. No índice 0, a amostra anterior ausente contribui zero; no índice 1, a amostra anterior vale `2`. Outro preenchimento ou aquecimento mudaria as amostras de ataque. Filtros FIR práticos mais longos podem adicionar atraso de grupo; alinhe as saídas e registre a regra de borda antes de interpretar diferença no instante de pico.

## 3. Projete um teste A/B de guitarra falseável

O procedimento a seguir é um **experimento offline proposto, não executado**. Comece com a gravação `deb-low-e-open.wav` do [diretório da fixture](../../../fixtures/guitar-acoustics/gas-001/README.md), cujo SHA-256 é `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`. Decodifique suas amostras WAV mono float32 uma vez e preserve os bytes originais. Registre decodificador, taxa, hash e primeiro ataque aproximado; inspecione a forma de onda antes de escolher uma janela que exclua o segundo ataque. Uma segunda execução pode usar `ga-engine-e2-open-4s.wav`, mas deve ser relatada separadamente: sua origem é um render nativo com outro início e outra proveniência.

Antes de implementar o compressor futuro, escreva seu contrato de parâmetros: limiar em dBFS, razão, unidades de ataque/soltura, detector de pico ou RMS, lookahead, knee, ganho de compensação, reinicialização do estado e comportamento da primeira amostra. Fixe sua revisão de código e testes. Use uma EQ determinística: publique coeficientes FIR literais ou fixe a [fonte de filtragem IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) e registre corte, ordem, coeficientes e tratamento das bordas. Nas duas cadeias, use as *mesmas* configurações e reinicialize o estado do compressor antes de cada render. Exporte WAVs A e B sem perdas, na mesma taxa, e salve traço de redução de ganho, número de amostras e manifesto de processamento. Não afirme que GA ou IX já oferece a cadeia combinada.

Defina a janela do primeiro toque em relação ao ataque gravado, **aproximadamente em 1.1 s**, e anote no manifesto o índice de amostra escolhido. Para cada cadeia, informe amostra e instante do pico, RMS de janela curta ou envoltória no ataque, RMS posterior e traço de redução de ganho. Na escuta, iguale o nível de saída e registre o ajuste para não confundir medições brutas com ajustadas. Evite clipping após compensação ou ajuste de nível. Se a latência do FIR diferir da de um caminho sem filtro, alinhe as saídas por atraso documentado ou correlação cruzada antes de comparar os instantes de pico. Um teste de ouvintes aprovado futuramente deve ocultar rótulos, aleatorizar a ordem e permitir “nenhuma diferença perceptível”; ele não substitui a verificação numérica.

O **falseador** da hipótese restrita “a posição da EQ altera esta passagem sob estes ajustes fixados” é A e B permanecerem iguais amostra a amostra dentro de tolerância numérica pré-declarada, ou a diferença aparente desaparecer após corrigir alinhamento, reinicialização ou tratamento do nível. Se houver diferença, examine entrada do detector e traços de ganho para atribuir o mecanismo. Diferença não prova que uma ordem seja mais natural. EQ neutra ou compressor que nunca cruza o limiar tornam plausível um resultado nulo. Afirmar que uma ordem preserva melhor o ataque exigiria métrica de ataque, direção, tolerância e checagem por ouvintes se a percepção integrar a afirmação.

### Exercício prático 4: mantenha a fixture válida

Um procedimento proposto processa a gravação no tempo de arquivo `0.0–1.0 s`, compara-a com o render no mesmo intervalo e conclui que EQ→Comp preservou melhor o ataque. Cite dois problemas independentes.

> **Resposta:** O primeiro ataque gravado só ocorre perto de `1.1 s`; o intervalo `0.0–1.0 s` fica sobretudo antes do ataque, enquanto o render começa em zero. As janelas não estão alinhadas ao ataque. Além disso, comparar arquivos de origem diferentes não isola a ordem: A e B precisam usar o **mesmo WAV de origem**. Nenhuma fixture é um benchmark validado de realismo.

### Exercício prático 5: escolha a próxima verificação

Uma execução futura encontra diferença de `0.2 dB` no RMS da primeira janela, mas as saídas não foram alinhadas e falta o manifesto de ajustes do compressor. Isso favorece uma ordem? Que provas você pediria?

> **Resposta:** Não. Preserve hash e janela de entrada, publique versão e parâmetros do compressor, confira reinicializações independentes, alinhe latência e início, confirme coeficientes iguais de EQ e ausência de clipping; depois repita e compare medições brutas e traços de redução de ganho. Ajuste o nível de reprodução após o processamento para uma verificação cega separada se a afirmação envolver qualidade sonora. `0.2 dB` sozinho não identifica a etapa responsável nem estabelece preferência.

## Evidências e limites

- O [README da fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) registra arquivos E2 gravado e renderizado nativamente, hashes, atribuição, inícios aproximados e limites das medições. A [lição GAS-001](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) e os resultados salvos tratam da comparação *bruta*, não de um teste EQ/compressão.
- O [roteamento no navegador GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) e o [worklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) fixados documentam o caminho do demo; o [código FIR IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) documenta uma filtragem disponível. Não estabelecem compressor implementado, teste da ordem, nem WAV processado.
- O cálculo de quatro amostras é sintético. O procedimento A/B, parâmetros e métricas são propostas. Nenhum compressor foi construído ou executado nesta lição; não há WAV de guitarra processado, veredito cego nem decisão de roteamento em produção. Revisões técnica, pedagógica e linguística, implantação do Learn e leitura pública anônima continuam pendentes. O registro de pesquisa de 2026-03-23 permanece um artefato histórico sobre voz; esta revisão usa o novo ciclo.
