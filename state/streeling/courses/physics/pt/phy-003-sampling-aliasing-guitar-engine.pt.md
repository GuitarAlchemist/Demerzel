---
module_id: phy-003-sampling-aliasing-guitar-engine
department: physics
course: Amostragem e aliasing na fronteira do motor de guitarra GA
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-003
version: "0.1.0"
---

# Amostragem e aliasing na fronteira do motor de guitarra GA

> **Departamento de Física** | Nível intermédio | 35 minutos | Rascunho em português; revisão e publicação pendentes

## Objetivos

Vai calcular o limite de Nyquist e uma frequência de alias, identificar a taxa de amostragem que o motor Rust da GA realmente recebe e conceber um teste offline capaz de revelar aliasing sem confundir um risco calculado com um defeito medido. [PHY-001](../pt/phy-001-science-of-guitar-sound.pt.md) apresenta os harmónicos da guitarra. [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) escolhe janelas de análise para notas variáveis. Aqui a pergunta surge antes na cadeia: **que frequências contínuas uma amostragem pode representar e o que deve acontecer antes da captação, síntese ou conversão de taxa?**

## 1. Associar a taxa ao artefacto, não ao nome da nota

A [fixture GAS-001 fixada](../../../fixtures/guitar-acoustics/gas-001/README.md) contém um Mi2 solto gravado durante quatro segundos e uma renderização nativa de quatro segundos do motor Rust da GA. Ambos os ficheiros são mono a **44 100 amostras por segundo**. A renderização chama `engine_note_on(82.4069 Hz, 0.1)`; a identidade E2 da gravação é uma etiqueta do conjunto de dados, não uma medição de frequência. A renderização veio de uma compilação nativa, **não** de uma captura do AudioWorklet no navegador. Esta distinção importa ao investigar um artefacto sonoro.

No commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), a [ponte de áudio do navegador](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) envia `audioContext.sampleRate` ao [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js). O worklet chama `engine_init(srToUse)` e copia as amostras mono calculadas para os canais de saída. O [motor Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) guarda essa taxa e usa-a nos coeficientes dos ressonadores e no comprimento da linha de atraso. Portanto, o WAV fixado a 44,1 kHz **não** demonstra que todos os usos no navegador operem a 44,1 kHz. Registe a taxa real do contexto e o percurso de captação antes de comparar uma gravação do navegador com GAS-001.

Para uma duração `T`, o número de amostras é `N = f_s T`. Quatro segundos a 44 100 Hz dão **176 400 amostras** por canal mono; a 48 000 Hz seriam **192 000**. Nenhum desses totais revela se a entrada analógica foi filtrada corretamente ou se o sintetizador evitou aliases.

### Exercício prático 1

Uma pessoa vê a renderização GAS-001 a 44,1 kHz e escreve: «O motor GA no navegador funciona sempre a 44,1 kHz.» O que é que as fontes realmente sustentam e o que deve registar um teste no navegador?

> **Resposta:** GAS-001 fixa **o seu WAV renderizado nativamente** a 44 100 Hz. A ponte do navegador passa `audioContext.sampleRate` ao worklet e ao motor Rust; o valor real deve ser observado nessa sessão. Registe a taxa do contexto, a taxa e o codec da saída ou gravação, a revisão do motor e o percurso de captação. Um WAV nativo não é uma captura do navegador.

## 2. Calcular a banda representável antes dos harmónicos

Para um sinal real amostrado uniformemente à taxa `f_s`, a frequência de Nyquist é `f_N = f_s/2`: **22 050 Hz** a 44 100 Hz e **24 000 Hz** a 48 000 Hz. Uma entrada contínua ideal, limitada em banda a frequências estritamente inferiores a `f_N`, pode em princípio ser reconstruída a partir das amostras. A captação real precisa de um filtro anti-alias **antes** da amostragem, com banda de transição abaixo de Nyquist. `f_N` é uma fronteira matemática, não a promessa de um filtro abrupto no microfone, conversor, motor ou exportação.

A frequência alvo da corda Mi grave solta é `f_0 = 82.4069 Hz`. O parcial inteiro ideal `k` estaria em `k f_0`, mas uma guitarra física ou sintetizada não tem obrigatoriamente todos os parciais nem os mantém em múltiplos exatos. A 44,1 kHz, `267 f_0 = 22,002.6423 Hz` fica abaixo de Nyquist; `268 f_0 = 22,085.0492 Hz` fica acima. A 48 kHz, a fronteira separa o parcial **291** (`23,980.4079 Hz`) do **292** (`24,062.8148 Hz`). São *limites teóricos de índice* para esta fundamental, não uma contagem de parciais audíveis ou medidos. Uma margem prática deve ficar abaixo da fronteira exata, porque os filtros precisam de transição e a implementação importa.

### Exercício prático 2

Para o mesmo E2 ideal, calcule o harmónico inteiro mais alto estritamente abaixo de Nyquist a 44,1 e 48 kHz. Isso prova que a fixture contém esses harmónicos?

> **Resposta:** `floor(22,050 / 82.4069) = 267` e `floor(24,000 / 82.4069) = 291`. Os parciais adjacentes 268 e 292 excedem os respetivos limites de Nyquist. Esta aritmética não prova que exista um 267.º ou 291.º parcial detetável nos WAV. Medir níveis exige os ficheiros, uma janela apropriada, um patamar de ruído e limites de análise explícitos.

## 3. Calcular um alias à mão

Amostrando um seno contínuo de `f` Hz obtemos `sin(2π f n / f_s)` nos índices inteiros `n`. Somar ou subtrair um múltiplo inteiro de `f_s` dá as mesmas amostras, salvo uma diferença de sinal ou fase. Para a magnitude da frequência de alias, dobre `f` por múltiplos de `f_s` para `[0, f_s/2]`; equivalentemente, escolha um inteiro `m` que coloque `|f - m f_s|` nesse intervalo. É um cálculo **sintético de tom único**, não uma observação de GAS-001.

Considere um seno contínuo de **23 000 Hz**. A 44,1 kHz está 950 Hz acima de Nyquist e dobra para `|23,000 - 44,100| = 21,100 Hz`. A sequência amostrada equivale a um seno de 21 100 Hz com sinal ou fase diferente. A 48 kHz, 23 000 Hz fica abaixo dos 24 000 Hz e não se dobra. Converter depois a gravação de 44,1 para 48 kHz não recupera a entrada original a 23 000 Hz: as amostras não distinguem as duas origens contínuas.

Num motor de guitarra, uma excitação de ataque de banda larga, processamento não linear e parciais agudos são motivos para **testar** a fronteira. A [excitação Rust fixada](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) usa ruído filtrado numa linha de atraso e processamento por amostra. A inspeção não prova um alias audível ou mensurável na saída. Uma taxa maior pode deslocar a fronteira de aliasing, mas muda também buffers e custo de cálculo; não substitui a limitação de banda controlada nem medições.

### Exercício prático 3

Uma excitação proposta tem uma componente contínua a 30 000 Hz. Onde colocaria um amostrador ideal o seu alias a 44,1 e a 48 kHz?

> **Resposta:** A 44,1 kHz, `|30,000 - 44,100| = 14,100 Hz`. A 48 kHz, `|30,000 - 48,000| = 18,000 Hz`. Estes são dobramentos de um seno ideal, não picos espectrais previstos do motor GA. Um filtro anti-alias a montante pode atenuar a componente antes da captação; um gerador digital deve evitar criar conteúdo fora de banda ou controlar o seu dobramento.

### Exercício prático 4

Uma pessoa converte para 48 kHz uma gravação a 44,1 kHz com um pico a 21,1 kHz e afirma: «Agora que Nyquist é 24 kHz, o tom original de 23 kHz voltou.» Explique o erro.

> **Resposta:** A sequência a 44,1 kHz é compatível tanto com um tom a 21,1 kHz como com outro a 23 kHz, com diferença de sinal ou fase. A conversão pode interpolar ou filtrar os dados disponíveis, mas não inferir a origem contínua. Impeça o dobramento **antes** da amostragem original com filtragem analógica anti-alias, ou gere conteúdo digital limitado em banda à taxa pretendida.

## 4. Transformar o risco num teste refutável para GA

As [medições GAS-001](../../../fixtures/guitar-acoustics/gas-001/measurements.json) apresentam picos perto de E2 e alguns parciais graves, não uma análise de aliases agudos. Um gráfico dos dois WAV a 44,1 kHz não identifica sozinho a frequência original de um alias: um pico abaixo de Nyquist pode ter várias causas. A gravação tem ainda um primeiro ataque aproximado aos 1,1 s e outro perto de 2,75 s; a renderização começa em zero. Preserve intervalos alinhados aos ataques antes de comparar espectros; [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) explica este problema de seleção temporal.

Um ensaio offline começaria por uma **referência sintética conhecida**: gerar um seno a 23 kHz numa taxa de referência superior, amostrá-lo a 44,1 e 48 kHz com a escolha de filtragem documentada e procurar o dobramento previsto a 21,1 kHz apenas no braço a 44,1 kHz intencionalmente sem filtro. Depois renderize a mesma fonte GA fixada, com nota, velocidade, perfil e duração iguais, nas duas taxas por chamadas **nativas**, ou capture ambas no **navegador** registando a taxa; não misture silenciosamente os percursos. Guarde parâmetros, compilação exata, hashes dos WAV, taxa, nível de pico e janelas espectrais. Compare com uma referência controlada e de taxa correspondente em várias notas e velocidades. Se um tom inesperado se deslocar de acordo com o dobramento previsto quando a taxa muda, investigue a etapa que o gera; se persistir na mesma frequência física, a hipótese simples de alias enfraquece. Confirme com uma mudança de código dirigida à etapa suspeita e repita a escuta a nível igualado. O protocolo é **proposto**: essas renderizações, capturas e escutas adicionais **não** foram realizadas para esta lição.

Para futuras conversões de taxa, documente taxas de origem e destino, bandas passante e de rejeição do filtro, atraso, verificações de clipping e se a referência foi captada antes ou depois de codificação com perdas. A ponte do navegador inclui uma [via MediaRecorder opcional](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js); não presuma que o blob é um WAV bruto a 44,1 kHz. Mantenha essa via separada do render nativo da fixture.

### Exercício prático 5

Surge um pico a 21,1 kHz numa renderização do motor a 44,1 kHz. Basta para afirmar que há um alias de síntese proveniente de 23 kHz? Indique a comparação decisiva seguinte e um controlo.

> **Resposta:** Não. O pico pode ser uma componente na banda, um alias de outra componente fora da banda ou um artefacto de captação. Renderize a mesma configuração fixada do motor a 48 kHz e compare espectros agudos alinhados pelo ataque: uma fonte perto de 23 kHz deveria aparecer aí perto de 23 kHz, ao passo que o alias a 44,1 kHz estaria perto de 21,1 kHz. Controle revisão do motor, nota, velocidade, perfil e percurso de captação; examine a etapa de sinal ou introduza uma mudança dirigida de limitação de banda antes de atribuir uma causa. O movimento previsto é um **teste**, não um resultado observado.

## Fontes e limites atuais

- [Fixture GAS-001 fixada, origem e taxas](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), com o [README local](../../../fixtures/guitar-acoustics/gas-001/README.md). A gravação é atribuída aí a **collegefishiesd** sob CC BY-SA 4.0; esta lição não reproduz o áudio.
- Commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo): [ponte do navegador](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) e [motor Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs).
- As contagens de amostras, os limites dos índices harmónicos e os exemplos de seno único resultam diretamente das taxas e frequências indicadas. Não foram realizadas para PHY-003 novas medições de aliases agudos em GAS-001, captação do navegador, revisão independente do conteúdo, teste com estudantes, revisão linguística ou leitura pública.
