---
module_id: aud-003-transient-preservation-gate
department: audio-engineering
course: "Preservar o ataque de uma corda de guitarra na análise espectral offline"
level: intermediate
prerequisites: [aud-002-level-matched-guitar-comparison, phy-002-time-frequency-guitar-transients]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-003
version: "0.1.0"
---

# Preservar o ataque de uma corda de guitarra na análise espectral offline

> **Departamento de Engenharia de Áudio** | Nível: Intermediário | Duração estimada: 35 minutos | Estado: rascunho em português; revisão e publicação pendentes

## Objetivos

Após esta lição, você poderá:

- escolher entre uma FFT do intervalo inteiro e uma STFT conforme a decisão sobre o áudio;
- definir tamanhos válidos de janela e salto para o espectrograma do IX, mantendo o ataque visível em pelo menos um quadro;
- distinguir o redutor de ruído por wavelets de Haar do IX das análises por wavelets centradas em frequências do fixture GAS-001;
- rejeitar uma redução de ruído que altere o transiente da guitarra além de um limite declarado; e
- especificar uma avaliação offline que outra pessoa possa refutar usando os mesmos WAVs.

## A decisão do projeto

O [fixture GAS-001 da corda Mi grave solta](../../../fixtures/guitar-acoustics/gas-001/README.md), fixado no commit [`5c496745` de Demerzel](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), contém uma gravação licenciada do Mi2 solto e uma renderização do mecanismo nativo do GA. Ambos são WAVs mono de quatro segundos a 44.100 Hz. O primeiro ataque da gravação ocorre aproximadamente 1,1 segundo após o início do arquivo; a renderização começa em zero. O fixture registra outro ataque perto de 2,75 segundos na gravação. É um par didático, não um benchmark validado de realismo nem uma captura do AudioWorklet do navegador.

[PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md) explica o compromisso entre tempo e frequência e interpreta as medições salvas de FFT e wavelets do tipo Morlet do fixture. [AUD-002](../en/aud-002-level-matched-guitar-comparison.md) controla o alinhamento dos ataques e o nível de reprodução antes da escuta. Esta lição trata de outra decisão de engenharia: **uma pessoa que analisa o áudio offline deve reduzir o ruído da gravação de referência antes de usar seu ataque para avaliar uma renderização do GA?** Uma aparente redução do ruído não basta. O processamento também pode suavizar, espalhar ou deslocar o transiente que se pretendia preservar.

O caso de implementação está fixado no commit [`bd1336b7` do IX](https://github.com/GuitarAlchemist/ix/tree/bd1336b7c4045e427dcdbe80b102790e45da5ce1). O IX expõe um [handler de FFT](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1297-L1315), um [handler de espectrograma](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189) e um [handler de redução de ruído por wavelets de Haar](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797). Eles recebem arrays numéricos de amostras, não caminhos de WAVs. Para aplicá-los ao par de áudio fixado, seria preciso um decodificador de WAV e um processo offline reproduzível; esta lição não executou essa análise.

## 1. Escolha a representação de acordo com a afirmação

A função [`rfft` do IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/fft.rs#L84-L115) transforma um array finito de amostras reais e completa com zeros um comprimento que não seja potência de dois até a próxima potência de dois. Apesar do nome, ela devolve o array completo da FFT. O handler `ix_fft` devolve magnitudes e frequências em **ciclos por amostra**, supondo frequência de amostragem de 1,0. Com 44.100 amostras por segundo, multiplique por 44.100 uma frequência normalizada de bin **até Nyquist** para expressá-la em hertz; a metade superior espelha as frequências negativas. O espectro de magnitude do arquivo inteiro é válido para um sinal variável, mas não identifica qual ataque produziu um pico. A FFT de um intervalo escolhido da primeira nota ajuda a resumir seus harmônicos, embora ainda faça uma média nesse intervalo.

A função [`stft` do IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L30) repete FFTs janeladas em posições sucessivas das amostras. [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L32-L54) usa uma janela de Hann e guarda magnitudes de um único lado do espectro. Isso permite observar se a energia associada ao ataque aparece em um quadro inicial e como ela muda. O caminho `db=true` calcula `20 log10(max(magnitude, 1e-10))`; não é uma medição calibrada em dBFS. Não compare diretamente seus valores brutos em dB com os valores RMS em dBFS do GAS-001.

### Exercício prático 1: escolha uma saída capaz de responder à pergunta

Uma pessoa calcula `ix_fft` para todo o WAV gravado de quatro segundos e diz que o pico brilhante pertence ao *primeiro* toque, não ao ataque posterior. O que é útil nesse resultado e o que deve ser calculado antes de atribuir o pico a um evento?

> **Resposta:** A FFT do arquivo inteiro pode mostrar energia próxima daquela frequência, após converter ciclos por amostra em hertz. Suas magnitudes não trazem marcação temporal e, portanto, não atribuem o pico ao primeiro toque. Decodifique o WAV, marque o primeiro ataque aproximado, calcule separadamente um intervalo declarado da primeira nota e inspecione uma STFT alinhada aos ataques se o tempo dos eventos importar. Registre o arquivo bruto e os intervalos de análise.

## 2. Ajuste a STFT do IX à pergunta sobre o ataque

O **handler do agente** IX exige um `window_size` que seja potência de dois, no mínimo dois e não maior que o sinal. Isso importa porque a FFT subjacente preencheria com zeros um quadro de outro comprimento, tornando incorretos a contagem de bins e o mapeamento de frequências declarados pelo handler. O padrão de `hop_size` é metade da janela; um salto zero fornecido pelo usuário é convertido em um; o handler informa `n_frames` e `n_bins`. A função central `stft` não oferece essas verificações de entrada: um processo offline que a chame diretamente precisa validar seus argumentos. Ela processa apenas quadros completos e não prolonga silenciosamente uma cauda curta.

Para uma visão **proposta** do primeiro ataque a 44,1 kHz, escolha uma janela de 2.048 amostras e um salto de 512. A janela cobre cerca de **46,44 ms**, o salto cerca de **11,61 ms**, e a grade da FFT tem `44,100 / 2,048 ≈ 21.53 Hz` por bin; a magnitude de um lado tem **1.025 bins**. Essa grade é grosseira demais para resolver uma diferença de um hertz com um único quadro. Uma janela maior, de 8.192 amostras, cobre cerca de 185,76 ms e tem espaçamento de 5,38 Hz, mas mistura mais ataque e decaimento. Um salto menor produz mais quadros sobrepostos; não melhora a discriminação de frequência de cada quadro. São cálculos a partir dos parâmetros, **não** saídas medidas do IX nos WAVs.

### Exercício prático 2: especifique uma solicitação válida ao IX

A 44.100 Hz, calcule a duração da janela, o intervalo entre saltos e o espaçamento nominal entre bins para `window_size=2048`, `hop_size=512`. Quantos bins o handler de espectrograma do IX deve informar? Por que esse handler rejeitaria `window_size=2205`, que corresponde a exatos 50 ms?

> **Resposta:** A duração é `2048/44100 ≈ 46.44 ms`, o intervalo entre saltos é `512/44100 ≈ 11.61 ms`, e o espaçamento é `44100/2048 ≈ 21.53 Hz`. O handler informa `2048/2 + 1 = 1025` bins. Ele rejeita 2.205 porque não é potência de dois; uma chamada direta à função central poderia preenchê-lo com zeros, mas seria errado interpretar seus bins como se a FFT tivesse comprimento 2.205.

A janela de Hann vai a zero nas extremidades. Isso ajuda a controlar descontinuidades nas bordas, mas um transiente situado exatamente na extremidade pode desaparecer daquele quadro. Com sobreposição, a mesma amostra fica em outra posição de outro quadro. É uma questão de **posicionamento da análise**, não uma afirmação de que a sobreposição cria informação nova. A [função de janela do IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/window.rs#L10-L15) e o [laço dos quadros](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L14-L29) permitem conferir esse efeito de borda sem uma gravação de guitarra.

### Exercício prático 3: mantenha visível o impulso na borda

Considere um array sintético de 64 amostras, todas zero exceto o valor 1 no índice 16. O IX usa uma janela de Hann de 16 amostras. Com salto 16, qual quadro completo contém o impulso e o que acontece com ele? O que muda com salto 8?

> **Resposta:** Com salto 16, os quadros começam em 0, 16, 32 e 48. Somente o quadro que começa em 16 contém o índice 16; nele, o impulso está no deslocamento 0, onde o peso de Hann é zero. Assim, todos os espectros devolvidos podem perder esse impulso isolado. Com salto 8, o quadro que começa em 8 também o contém, no deslocamento 8, cujo peso de Hann é aproximadamente 0,989; esse quadro registra energia. É um cálculo sintético derivado do código, não uma medição de WAV pelo IX. Ele mostra por que o salto proposto de 512 amostras deve ser verificado perto das bordas de ataques reais.

## 3. Um redutor de ruído por Haar pode alterar a evidência

A função [`haar_forward` do IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L18) forma médias e diferenças em pares. [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L60-L82) aplica limiarização suave aos coeficientes de detalhe e reconstrói o sinal. É um processamento por Haar discreto, **não** a análise por wavelets complexas do tipo Morlet, centradas em frequências, salva em GAS-001. Os métodos têm saídas diferentes e respondem a perguntas diferentes. Um coeficiente de detalhe de Haar pode indicar uma mudança rápida, mas seu corte também pode remover parte de um ataque real junto com o ruído.

O handler do IX exige `levels >= 1`, um limiar finito e não negativo e comprimento de entrada divisível por `2^levels`; caso contrário, rejeita a solicitação, pois a transformação Haar central pode descartar amostras finais de um comprimento ímpar. O [teste de ruído no repositório](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1387-L1411) usa uma rampa suave com ruído alternado adicionado e verifica menor erro quadrático médio. Esse teste não verifica a preservação de um ataque isolado de guitarra. Os [testes das validações de entrada](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1525-L1543) cobrem tamanho inválido de espectrograma e comprimento de entrada indivisível para wavelets.

### Exercício prático 4: preveja a alteração do transiente

Para o sinal sintético de oito amostras `[0, 1, 0, 0, 0, 0, 0, 0]`, aplique as equações Haar de um nível do IX com limiarização suave de valor 1. Quais são as duas primeiras amostras reconstruídas? Isso sustenta a afirmação de que a redução de ruído por wavelets sempre preserva o pico de um ataque?

> **Resposta:** O primeiro par tem aproximação `1/sqrt(2)` e detalhe `-1/sqrt(2)`. Como o módulo do detalhe é menor que o limiar 1, a limiarização suave o leva a zero. A inversa devolve `[0.5, 0.5]` para o primeiro par; os demais pares continuam em zero. O pico isolado cai de 1 para 0,5 e se espalha uma amostra para antes. O cálculo refuta uma alegação incondicional de preservação; não prevê qual limiar seria apropriado para um WAV de guitarra gravada.

## 4. Declare antecipadamente um critério offline de preservação

O procedimento a seguir é uma **proposta de avaliação**, não uma execução nem um padrão de aceitação do GA. Guarde ambos os WAVs do fixture e seus hashes completos. Decodifique cada um como amostras mono `f64` normalizadas, sem sobrescrever o original. Registre decodificador, frequência de amostragem, contagem de amostras e qualquer reamostragem; rejeite uma mudança silenciosa na frequência de amostragem. Use as marcas aproximadas de ataque do fixture (gravação em 1,1 s; renderização em 0,0 s) e inspecione trechos do primeiro ataque separadamente do ataque posterior da gravação. Mantenha uma versão bruta e uma cópia processada nas mesmas posições de amostra e com o mesmo ganho. Execute a visão STFT do IX nas duas versões com os parâmetros declarados 2.048/512; identifique os quadros pelo **índice da amostra inicial e pela duração da janela**, não apenas pelo centro visual de uma coluna. Registre se a conclusão sobre o ataque na borda resiste a outro salto ou a um pequeno deslocamento da marca de ataque.

Antes de executar Haar, declare `levels` e limiar, confira se o comprimento exato da entrada é divisível por `2^levels` e salve a política de preenchimento/corte, se necessária. Por exemplo, um trecho de um segundo com 44.100 amostras **não** é divisível por oito para três níveis: o resto é quatro. Preencher com quatro zeros até 44.104 é uma opção declarada; isso cria uma borda que pode afetar coeficientes próximos. Outra opção é mudar a borda do trecho ou usar menos níveis. Não chame diretamente a função central com entrada de comprimento ímpar supondo que sua saída continuará alinhada.

Para a gravação de referência, meça um intervalo de ruído anterior ao ataque e um intervalo fixo do primeiro ataque tanto na versão bruta quanto na processada. Um **critério didático**, escolhido antes de observar o resultado, poderia exigir RMS anterior ao ataque pelo menos **3 dB** menor, mantendo o pico absoluto do primeiro ataque dentro de **10%** do valor bruto e o instante desse pico dentro de **1 ms**. Exija ausência de clipping e contagem de amostras inalterada após qualquer corte documentado. Repita a verificação com as marcas de ataque deslocadas em ±5 ms e informe todos os limiares candidatos, inclusive os que falharam. A renderização do GA começa no tempo zero do arquivo e, portanto, não tem intervalo equivalente de ruído anterior ao ataque; não aplique a ela esse critério específico de ruído. Preserve a gravação não processada como referência principal da comparação. Passar nesses indicadores de forma de onda permitiria uma comparação auditiva com níveis igualados, documentada à parte; **não** provaria que o arquivo processado é perceptualmente idêntico nem que o GA soa realista.

### Exercício prático 5: aplique o critério e declare seu limite

Uma pessoa propõe Haar com três níveis para um trecho gravado de 44.100 amostras sem preenchimento. Ela também apresenta um candidato *hipotético* com RMS anterior ao ataque 4 dB menor, pico de ataque igual a 0,82 vezes o pico bruto e deslocamento do instante do pico de 0,2 ms. O que deve mudar para que o handler do IX aceite o trecho? O candidato passaria no critério didático?

> **Resposta:** `44,100 mod 8 = 4`, logo o handler rejeita três níveis nesse comprimento. Declare quatro amostras adicionadas para chegar a 44.104 e uma política de corte, escolha outro trecho ou reduza os níveis. O candidato hipotético falha, embora o ruído caia mais de 3 dB e o tempo permaneça dentro de 1 ms: `1 - 0.82 = 0.18`, uma perda de 18% no pico, excede o limite declarado de 10%. Essa rejeição trata da preservação do transiente segundo esse critério aproximado; não é uma medição de nenhum dos WAVs do fixture nem um veredito de ouvintes.

## Evidências e limites

- O áudio e sua proveniência vêm do [fixture GAS-001 em Demerzel `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). A gravação e a renderização nativa do GA são fontes separadas, com cadeias diferentes de execução e produção. As medições salvas de FFT e Morlet são observações desse fixture, não saídas do IX.
- As equações de STFT, FFT e Haar, as validações dos handlers e os testes citados acima são observações do código-fonte do IX em `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. As dimensões 2.048/512, o exemplo da borda de Hann, o resultado Haar de oito amostras e a aritmética de divisibilidade são **exemplos derivados**. AUD-003 não produziu nem mediu um espectrograma do IX ou um WAV com ruído reduzido.
- Uma magnitude de análise não é uma medida calibrada de volume percebido nem de realismo. As marcas de ataque são aproximadas; janelas espectrais, preenchimento, limiares, decodificador e ganho de entrada podem alterar o resultado. Um impulso sintético expõe uma possível falha, mas não prevê o comportamento de todos os ataques.
- Revisão técnica, tentativas de alunos, revisão por falantes nativos, sincronização/compilação no Learn e leitura pública permanecem pendentes. Este texto em português é um rascunho de tradução, não um curso publicado.
