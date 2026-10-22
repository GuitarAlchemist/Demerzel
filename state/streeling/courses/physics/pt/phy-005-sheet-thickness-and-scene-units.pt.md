---
module_id: phy-005-sheet-thickness-and-scene-units
department: physics
course: Espessura da folha das coordenadas IX às unidades de cena propostas
level: intermediate
prerequisites: [basic-ratios, dimensional-analysis]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-21-005
version: "0.1.0"
---

# Espessura da folha das coordenadas IX às unidades de cena propostas

> **Departamento de Física** | 40 minutos | Rascunho provisório em português; revisão do conteúdo, revisão por pessoa fluente no idioma e avaliação por alunos pendentes.

## Objetivos e problema do projeto

Uma folha no IX pode ter coordenadas entre zero e um, enquanto a espessura do material é medida em milímetros. Um artefato proposto para Blender ou Godot precisa de outra escala de comprimento declarada. Transportar apenas o número `0.4` entre as três representações transformaria um cartão comum em uma folha 150 vezes mais espessa, ou converteria milímetros em metros de cena com um erro de fator 1000.

Após esta aula, você conseguirá deduzir a espessura e as alturas da pilha em cada representação, distinguir camadas locais de níveis de painéis paralelos, diagnosticar dois erros de escala e escrever um repasse limitado ao que a evidência sustenta. Dedique cerca de 12 minutos à leitura das deduções, 18 minutos aos exercícios antes de revelar as respostas e 10 minutos à preparação da tarefa de transferência. Esta aula trata de comprimentos geométricos e conversão de unidades. A velocidade de excitação da guitarra pertence a PHY-004; a reconstrução de um estado de dobra pertence à sequência de computação visual.

Nosso recorte de fontes é o commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [`thickness.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), seus [testes existentes](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) e [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs). Inspecionamos essas definições e asserções. O agente coordenador executou o alvo específico de testes de espessura no HEAD IX fixado, sem alterações: 11 passaram, 0 falharam; isso não é um resultado da suíte inteira. O [conjunto de exemplos aritméticos](../../../fixtures/physics/phy-005/scenarios.json) fornece exemplos modelados, com instruções de reprodução em seu [README](../../../fixtures/physics/phy-005/README.md).

## 1. Declare uma régua antes de converter uma coordenada

Seja `C` a largura da folha expressa em unidades de coordenada do padrão de vincos, `W` sua largura física assumida em mm e `h` a espessura total do material em mm. Defina `a=W/C`, em mm por unidade de coordenada. Então:

```text
x_mm = x_cp × a
t_cp = h/a = h × C/W
H_mm = H_cp × a
```

O subscrito identifica uma representação; não afirma que o IX armazene metadados físicos. A largura `W` é uma hipótese externa fornecida para este exemplo resolvido. Um arquivo de quadrado unitário, sozinho, não informa se a folha real tem 150 mm ou 300 mm de largura. A espessura é a espessura total, não a meia espessura nem uma contagem de faces.

O teste do tsuru descreve explicitamente cartão de 0.4 mm em uma folha de 150 mm cujo padrão de vincos é o quadrado unitário. Portanto, `C=1`, `W=150`, `a=150` e `t_cp=0.4/150=0.0026666667`. A verificação da conversão de ida e volta dá `0.0026666667 × 150 ≈ 0.4 mm`. Mantenha a fração até a apresentação final para evitar desvios de arredondamento.

`lib.rs` descreve o redimensionamento das coordenadas por potências de dois antes das verificações de tolerância absoluta: a largura do padrão de vincos passa a ficar entre um e dois. Isso é condicionamento numérico. Não é uma declaração de metros nem uma medição da folha. `stack(ctx,t)` usa o `t` fornecido pelo chamador sem modificá-lo nas multiplicações que relata; não pode inferir `W` nem converter silenciosamente um valor fornecido de `0.4 mm`. Mantenha um mapeamento externo explícito para a representação de coordenadas que pretende encaminhar.

### Exercício prático 1: corrija a entrada de espessura

Um repasse para o tsuru de quadrado unitário do teste rotula `t=0.4` como “0.4 mm”. Calcule o `t_cp` necessário, a espessura física representada pelo valor errado e o fator de erro.

> **Resposta:** `t_cp=0.4/150=0.0026666667`. Com `a=150 mm/cp`, os `0.4 cp` errados significam `60 mm`. A razão para a espessura pretendida é `60/0.4=150`. Substitua o número e declare o mapeamento; mudar o rótulo do número existente não realiza uma conversão.

## 2. Mantenha separadas as duas leituras da pilha

A implementação calcula `ply` como o número máximo de faces em uma célula de sobreposição. Sua altura é `ply_height=ply × t`. Essa leitura permite que uma face ocupe alturas diferentes em células diferentes, como faria uma folha que se amolda ao apoio. É um limite inferior para pilhas que mantêm as posições planares declaradas.

Para painéis rígidos paralelos, faces conectadas por juntas planas compartilham um painel. Uma aresta dirigida conecta um painel inferior a um superior para um par sobreposto declarado. Com uma ordem acíclica e todos os pares de painéis sobrepostos determinados, `levels` é o comprimento da cadeia mais longa e `height=levels × t` é a menor altura sob essa interpretação restrita. Com ordens ausentes, a contagem de níveis relatada é um limite inferior; `levels_exact=false` e `face_levels` está ausente. Uma contagem é adimensional, enquanto uma altura tem as mesmas unidades de `t`.

O teste existente do tsuru verifica `ply=28`, `levels=36` rígidos e exatos, nenhum par indeterminado e 59 entradas de níveis por face que respeitam a ordem declarada. Ele fornece uma cadeia de 36 faces. São asserções sobre esse caso de teste e essa interpretação, não uma especificação universal de tsuru. Aplique as duas fórmulas:

```text
altura por camadas locais: 28 × (0.4/150) = 0.0746666667 cp = 11.2 mm
altura rígida:             36 × (0.4/150) = 0.096 cp        = 14.4 mm
```

Uma disposição ilustrativa que usa superfícies inferiores `z_k=k×t` tem a superfície inferior mais alta em `35t` para 36 níveis ocupados. O topo dessa última placa fica em `36t`. Isso explica a diferença entre o deslocamento de uma superfície e a extensão total da pilha; é uma convenção de desenho proposta, não geometria exportada pelo IX.

### Exercício prático 2: distinga deslocamento de extensão

O resumo da cena diz: “a espessura do tsuru é de 28 camadas, portanto a pilha rígida tem 11.2 mm; o nível rígido mais alto é 35, portanto sua altura é 35t”. Corrija as duas afirmações usando as hipóteses do teste.

> **Resposta:** A leitura de 28 camadas locais dá 11.2 mm. A leitura de painéis rígidos paralelos tem 36 níveis exatos e extensão total de `36×0.4=14.4 mm`. Na convenção proposta para a superfície inferior, o nível 35 começa em `35×0.4=14.0 mm` e termina em 14.4 mm. Um índice inteiro de nível não é a contagem de níveis ocupados.

## 3. Deduza explicitamente uma escala futura de cena

Suponha que um artefato futuro escolha `u=1 scene unit per metre`, ou seja, uma unidade de cena por metro. Essa é uma escolha didática, não uma configuração verificada do Blender ou do Godot. A conversão é `b=u/1000` unidades de cena por mm, portanto `x_scene=x_cp×a×b`. Aplique o mesmo multiplicador a todo comprimento que pertença à mesma geometria, incluindo espessura e alturas calculadas.

Para a folha de referência, uma unidade de coordenada corresponde a `150/1000=0.15` unidades de cena. Assim, `t_scene=(0.4/150)×0.15=0.0004`, a altura por camadas locais é `0.0112` e a altura rígida é `0.0144`. O caminho físico independente dá `14.4 mm × (1/1000)=0.0144 scene units`, em unidades de cena. A concordância entre os caminhos verifica a aritmética, não um pipeline de importação.

Se uma prévia didática separada escolher `u=100 scene units per metre`, ou seja, cem unidades de cena por metro, todo comprimento de cena ficará 100 vezes maior. A largura da folha será 15 unidades de cena e a altura rígida será 1.44. A espessura física continua sendo 0.4 mm. Uma escolha de escala muda a representação, não o material.

### Exercício prático 3: encontre um erro de fator 1000

Uma cena proposta na escala de metros usa largura de folha `0.15`, espessura `0.4` e altura rígida `14.4`. Calcule os dois comprimentos menores corretos e mostre uma razão que detecte a incompatibilidade sem depender da escala da cena.

> **Resposta:** A espessura deveria ser `0.0004` e a altura rígida `0.0144` unidades de cena. Os dois valores fornecidos são 1000 vezes maiores do que deveriam. As razões corretas, de espessura por largura e de altura rígida por largura, são `thickness/width=0.4/150≈0.0026666667` e `rigid height/width=14.4/150=0.096`. A cena errada tem razões de aproximadamente 2.6667 e 96. Uma escala uniforme consistente preserva essas razões adimensionais.

## 4. Mude uma hipótese por vez

Mudar o material e redimensionar a geometria respondem a perguntas diferentes. Na mesma folha de 150 mm, dobrar a espessura para 0.8 mm dobra `t_cp`, as duas alturas e seus comprimentos de cena. Isso não altera a ordem das faces na entrada. O teste existente `heights_scale_with_the_thickness` compara `t=0.25` e `0.5`, verifica que as alturas dobram e que os níveis das faces não mudam. Esses números testam álgebra; não são medições de cartão.

Manter o material de 0.4 mm, mas usar uma folha de 300 mm, reduz `t_cp` à metade em uma representação de quadrado unitário. As alturas físicas continuam sendo 11.2 e 14.4 mm para a mesma configuração combinatória declarada. Por outro lado, dobrar todo comprimento físico, incluindo a espessura do material, preserva `t_cp` e dobra as alturas físicas. Declare a qual dessas transformações você se refere ao dizer “aumentar a escala”.

Recodificar a mesma folha de 150 mm com `C=2` dá `a=75 mm/cp` e `t_cp=0.0053333333`; a altura rígida passa a `0.192 cp`. Multiplicar por 75 recupera 14.4 mm. Essa é uma dedução dimensional para uma representação recodificada de modo consistente, não uma nova execução observada do IX.

### Exercício prático 4: compare três alterações

Partindo da referência, calcule `t_cp` e a altura rígida em mm para: A, espessura de 0.8 mm com largura de 150 mm e `C=1`; B, espessura de 0.4 mm com largura de 300 mm e `C=1`; C, a folha física original representada com `C=2`. Suponha a mesma ordem exata de 36 níveis.

> **Resposta:** A: `t_cp=0.8/150≈0.0053333333`, altura `36×0.8=28.8 mm`. B: `t_cp=0.4/300≈0.0013333333`, altura de 14.4 mm. C: `t_cp=0.4×2/150≈0.0053333333`, altura de 14.4 mm. A e C compartilham uma espessura em coordenadas, mas descrevem hipóteses físicas diferentes. Valores de coordenadas exigem sua régua.

## 5. Declare o que uma altura convertida estabelece

O verificador lê um estado dobrado plano declarado. `lib.rs` diz que suas verificações locais não provam a dobrabilidade plana global e não calculam uma ordem de camadas. `thickness.rs` restringe sua interpretação rígida a painéis paralelos, cada um em uma única altura. Um ciclo recusa essa interpretação para `t` positivo; com espessura zero, ele é relatado sem recusa. A ausência de altura rígida em um ciclo não é uma medição de zero.

Mesmo uma altura acíclica exata não prova que uma dobra espessa seja fisicamente realizável: dobradiças reais, contato, flexão e uma trajetória de movimento estão fora desse cálculo. A fonte observa explicitamente que placas inclinadas podem escapar de uma recusa de painéis paralelos e que o contato exato entre vincos com espessura impõe outra limitação. Este curso não produz exportador, malha, colisor, simulação dinâmica de dobra, teste de material ou integração ativa com Blender/Godot/DLSS.

### Exercício prático 5: redija a afirmação para o repasse

Escreva três frases para uma pessoa que venha a criar um artefato visual usando o resultado de referência: uma sobre a evidência, uma sobre o mapeamento da cena e uma sobre uma afirmação física ou de integração ainda não resolvida.

> **Resposta:** “No commit IX fixado `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, as asserções inspecionadas do teste do tsuru especificam 28 camadas locais e 36 níveis exatos de painéis paralelos para `t=0.4/150`; o coordenador também relata que 11 testes específicos de espessura passaram nessa revisão sem alterações. Supondo uma folha de 150 mm e uma unidade de cena por metro, as extensões deduzidas por camadas locais e por painéis rígidos são 0.0112 e 0.0144 unidades de cena. Essas conversões não estabelecem a dobrabilidade física nem uma importação funcional no Blender/Godot.” Inclua o link para o conjunto de exemplos ao repassar essa afirmação.

## Transferência e revisão

Conclua a [tarefa separada para alunos, sem respostas](../../../reviews/phy-005-learner-task.md), com uma nova largura física e escala de cena. Uma pessoa revisora deve inspecionar a fonte fixada, recalcular as conversões e verificar a equivalência entre idiomas por meio do [roteiro de revisão](../../../reviews/phy-005-review-brief.md). Não há registro de tentativa de aluno, aprovação por pessoa fluente no idioma ou conferência da publicação. O artefato concluído aqui é um rascunho de aula e um pacote aritmético; seu benefício proposto continua sujeito a teste pela transferência sem ajuda de um aluno real.
