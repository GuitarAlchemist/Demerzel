---
module_id: gas-003-decay-calibration-open-e
department: guitar-acoustics
course: "Calibrar um teste de decaimento do mi solto para o motor de guitarra da GA"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-12-003
version: "0.1.0"
---

# Calibrar um teste de decaimento do mi solto para o motor de guitarra da GA

> **Departamento de Acústica e Síntese de Guitarra** | Intermediário | 40 minutos | Rascunho traduzido por IA; revisão pendente

## Objetivos

Você distinguirá uma *medição* de decaimento de um *parâmetro* Rust, calculará a diferença do par fixado de mi solto, seguirá o coeficiente de realimentação do motor e definirá um experimento nativo com apenas um parâmetro, um critério de refutação e salvaguardas. [GAS-001](../en/gas-001-open-string-audio-evidence.md) estabelece o par gravado/renderizado. [GAS-002](../en/gas-002-brightness-control-and-evaluation-gate.md) testa uma hipótese de brilho para uma razão harmônica local. Aqui perguntamos: **uma mudança controlada no ajuste de decaimento da GA pode aproximar a queda de nível do mi solto da gravação sem prejudicar o ataque, a altura ou outras notas?** Nenhum candidato de decaimento foi renderizado para esta aula.

## 1. Comece pelo envelope medido, não pelo controle

O [fixture GAS-001](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) fixado contém dois WAV mono de quatro segundos a 44.100 Hz: uma gravação acústica separada, rotulada como mi2 solto pelo conjunto de dados, e um render **nativo** do motor Rust da GA no commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. O render usa o perfil de guitarra 0 padrão e `engine_note_on(82.4069 Hz, velocity 0.1)`. Não é uma captura do AudioWorklet do navegador. O [README do fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md) informa hashes, limites de proveniência, crédito e atribuição CC BY-SA 4.0 do arquivo gravado.

O [JSON de medições](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) traz a mudança de RMS tardio menos inicial de **−3.9 dB** para a gravação e **−1.1 dB** para o render. O [script de medição](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) usa janelas de 0.2–0.4 s e 1.0–1.2 s **após o primeiro ataque de cada arquivo**. O primeiro ataque gravado ocorre por volta de 1.1 s, com outro perto de 2.75 s; o render começa em zero. Assim, as janelas da gravação ficam aproximadamente em **1.3–1.5** e **2.1–2.3 s** no arquivo, antes do segundo ataque. Não são constantes de decaimento do arquivo inteiro.

A queda selecionada do render é **2.8 dB menos negativa**: `−1.1 − (−3.9) = +2.8 dB`. O erro absoluto em relação à mudança gravada é `|−1.1 − (−3.9)| = 2.8 dB`. Esses valores já foram arredondados para décimos. Os WAV diferem em nível inicial, instrumento, microfone, ambiente e palhetada; comparar *mudanças* dentro de cada arquivo é mais útil aqui do que comparar diretamente RMS absolutos em dBFS. Mesmo assim, a diferença não identifica o parâmetro responsável nem a preferência dos ouvintes.

### Exercício 1 — Leia a diferença

Com os valores salvos, calcule a diferença com sinal entre render e gravação na mudança tardia menos inicial e o erro absoluto. Erro de 2.8 dB significa que o render inteiro é 2.8 dB mais alto?

> **Resposta:** `−1.1 − (−3.9) = +2.8 dB`; o erro absoluto é `2.8 dB`. O nível do render cai menos entre as duas janelas RMS relativas ao ataque. Isso não compara a sonoridade dos arquivos inteiros nem demonstra preferência auditiva.

### Exercício 2 — Deixe o segundo ataque de fora

Em que instantes do arquivo caem as duas janelas da gravação se o primeiro ataque está aproximadamente em 1.1 s? Por que uma janela tardia iniciada em 2.8 s é inadequada para a primeira nota?

> **Resposta:** A inicial é aproximadamente `1.1 + [0.2, 0.4] = 1.3–1.5 s`; a tardia, `1.1 + [1.0, 1.2] = 2.1–2.3 s`. Uma janela iniciada em 2.8 s ocorre após o ataque adicional perto de 2.75 s e mistura outro evento à suposta medida de decaimento. Como o início é aproximado, repita a análise com pequena variação antes de concluir com firmeza.

## 2. Siga o parâmetro Rust e o coeficiente efetivo

No [motor Rust da GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) fixado, `Engine::new` começa com `decay = 0.9968`, mas seleciona em seguida o perfil 0 padrão, que define o **decaimento base como 0.9978**. A função exportada `engine_set_decay` restringe o valor solicitado a `[0.95, 0.9999]`. Selecione o perfil **antes** de aplicar o valor candidato: escolhê-lo depois reescreve o decaimento e outros controles. O [renderizador do fixture](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py) chama `engine_init` e `engine_note_on`, mas não `engine_set_decay`; um teste candidato precisa de uma extensão documentada ou de outro harness. Nenhuma execução candidata é relatada aqui.

As expressões relevantes do loop de renderização são:

```text
f_norm = clamp((voice_frequency_hz - 82) / (330 - 82), 0, 1)
voice.sustain = min(0.995 + 0.006 * (1 - f_norm), 0.9998)  # assigned at note excitation
feedback_decay = (base_decay + 0.0025 * (1 - f_norm)) * voice.sustain
```

Para os `82.4069 Hz` nominais do fixture, `f_norm ≈ 0.00164073`. O sustain sem limite é aproximadamente `1.00099016`; portanto `voice.sustain = 0.9998`. Com base `0.9978`, a expressão dá `(0.9978 + 0.0025 × (1 − 0.00164073)) × 0.9998 ≈ 1.00009584`. Uma base **proposta** de `0.9976` dá aproximadamente **0.99989588**. Ambos os valores estão dentro do limite aceito pelo setter.

Esses números são **coeficientes de realimentação calculados do código-fonte**, não taxas medidas de decaimento do envelope. O loop também combina amostras da linha de atraso, dispersão all-pass, filtro passa-baixas com estado e mistura de brilho, ruído de ataque, ressonadores e reverberação. Um coeficiente um pouco acima de um em uma expressão **não prova**, por si só, saída instável ou defeito audível. Reduzi-lo tampouco prevê determinada mudança em dB no WAV. Meça a saída com um método fixo.

O `attack_decay` separado regula o ruído de ataque; `reverb_mix` afeta a cauda; o brilho altera a mistura de realimentação. Não os mude junto com o candidato de decaimento, ou a causa de qualquer efeito ficará ambígua. GAS-002 já trata do brilho; aqui ele permanece fixo.

### Exercício 3 — Calcule e limite a inferência

Em `82.4069 Hz`, qual limite de sustain se aplica e quais coeficientes efetivos aproximados resultam das bases `0.9978` e `0.9976`? O primeiro número acima de um prova que o WAV da GA fica mais alto com o tempo?

> **Resposta:** `f_norm ≈ 0.00164073`; o sustain sem limite excede `0.9998`, logo o limite aplicado é `0.9998`. A expressão fornece aproximadamente `1.00009584` com `0.9978` e `0.99989588` com `0.9976`. Não: trata-se de um coeficiente dentro de um sistema filtrado, com estado, ressonância e reverberação. Nas janelas escolhidas, o WAV salvo apresenta `−1.1 dB`; o coeficiente sozinho não prevê seu envelope.

## 3. Declare antes um experimento de um parâmetro

Um teste nativo controlado compilaria **a mesma revisão Rust fixada** e criaria um motor novo para cada braço a 44.100 Hz. Mantenha perfil 0, frequência mi2 `82.4069 Hz`, velocidade `0.1`, quatro segundos, compilador, codificação WAV e todos os demais ajustes. O braço de referência usa `0.9978`. No candidato, chame `engine_set_decay(0.9976)` **depois** da inicialização e da seleção do perfil, **antes** de `engine_note_on`. Registre ordem e valor, hashes dos dois WAV e início escolhido. O código fixa uma semente de ruído na criação, mas motores novos e a mesma compilação ainda evitam transferência de estado. O renderizador atual não tem opção de decaimento: adapte-o ou substitua-o e revise o script antes de qualquer alegação empírica. Uma comparação nativa não certifica o AudioWorklet do navegador; teste esse caminho separadamente se for o destino de entrega.

Use o mesmo procedimento de medição nos dois braços. Uma **regra didática proposta** exige reduzir o erro absoluto pelo menos **1.0 dB** em relação ao erro arredondado de referência de `2.8 dB`: objetivo `≤ 1.8 dB` a partir dos `−3.9 dB` gravados. Nos valores arredondados, a queda candidata deve ficar entre **−5.7 e −2.1 dB**. Para decidir de fato, use medições WAV não arredondadas e documente uma tolerância, sem decidir no limite de um décimo com base no JSON arredondado. O limite é uma escolha didática antecipada, **não** um padrão de produto da GA nem previsão de aprovação de `0.9976`.

Proteja a comparação: sem clipping ou quase clipping (pico absoluto proposto **abaixo de 0.95**), fundamental mi2 próxima à linha de base com a mesma busca de pico de um segundo, e verificação do ataque inicial e dos traços do segundo e quarto parciais. Um RMS agregado melhor pode esconder transiente ou cauda espectral prejudicados. Repita em outras cordas, notas e velocidades antes de generalizar. Considere julgamentos de escuta cegos e com níveis igualados: correspondência numérica com uma guitarra externa não demonstra realismo percebido. Se o candidato falhar em `≤1.8 dB` ou em uma salvaguarda, rejeite **essa configuração candidata nesse teste** e relate o resultado. Uma falha não prova que toda mudança de decaimento seja inútil.

### Exercício 4 — Aplique a regra proposta

Com os valores de referência arredondados, qual o erro absoluto máximo permitido para melhoria de 1.0 dB? Qual intervalo de queda candidata isso implica ao redor de `−3.9 dB`? Um candidato dentro do intervalo, mas com pico `0.98`, passa em todas as salvaguardas?

> **Resposta:** `2.8 − 1.0 = 1.8 dB`; `|candidate − (−3.9)| ≤ 1.8` dá `−5.7 ≤ candidate ≤ −2.1 dB`. Pico `0.98` reprova na salvaguarda proposta `<0.95`, mesmo que o decaimento passe. Isso é aritmética de uma regra proposta, não resultado medido de um candidato.

### Exercício 5 — Formule uma refutação

Um agente afirma que baixar a base para `0.9976` melhora o amortecimento do mi2 na GA. Quais artefatos controlados mínimos e qual resultado refutariam a afirmação segundo esta regra? O que continuaria desconhecido após aprovação com apenas um mi2?

> **Resposta:** Guarde revisão e compilação exatas do motor, ordem das chamadas, WAV nativos de referência e candidato de motores novos e seus hashes, medição alinhada ao ataque e checagens de pico, parciais e ataque. Se o erro absoluto não arredondado não diminuir pelo menos 1.0 dB, ou uma salvaguarda falhar, o candidato reprova. Mesmo após aprovação, saída do navegador, outras notas e velocidades, diferenças de gravação e preferência dos ouvintes continuam sem verificação.

## 4. Separe melhoria de calibração

A gravação é uma **sonda de calibração**, não alvo físico exato para todas as guitarras. O conjunto de dados a rotula como mi2 solto, mas sala, instrumento, microfone e instrumentista diferem do render. Uma mudança global em `decay` pode afetar muitas notas; a fórmula dependente de frequência torna especialmente arriscado extrapolar a partir do mi2. Se o candidato aproximar o envelope da referência, diga apenas que aproximou **a medida tardia menos inicial especificada** no render testado. Se falhar, guarde o artefato para a próxima hipótese sobre ruído de ataque, reverberação, realimentação dependente de frequência ou sensibilidade às janelas, sem reescrever o histórico.

O [loop de iteração offline](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) existente e o crítico espectral podem apoiar experimentos repetidos, mas não dão veredito automático de escuta. Um futuro candidato processado por ComfyUI seria **um braço offline separado**, não prova de sucesso do setter Rust. Mantenha propostas de agentes, renders, referências, hashes, medições, revisão e publicação distintos.

## Fontes e limites

- [Proveniência GAS-001](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md), [medições](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json), [método](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) e [renderizador nativo](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py), em Demerzel `5c4967454ddc740ed937c87719ca4d71a3522e4b`.
- [Código Rust da GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) e [script de iteração offline](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), em GA `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Só o par GAS-001 salvo foi medido antes desta aula. Os coeficientes e o intervalo de aceitação são cálculos. Uma revisão independente do conteúdo e da coerência das traduções por IA não encontrou problemas relevantes. Permanecem pendentes o render candidato `0.9976`, a extensão do harness nativo, a captura no navegador, os testes com várias notas, o painel de escuta, a revisão humana, o teste com estudantes, a revisão linguística e a publicação.
