# Como eu construiria uma AGI/ASI — Parte 84 (0x54): o delírio e o escrutínio

> Continuação da [Parte 83](ASI_AGI_parte83_a_probabilidade_da_probabilidade.md). Pedido do usuário (um relatório longo sobre a arquitetura da Meta AI, mais um reforço do pedido da Parte 83 com cinco
> linhas novas). A decisão conservadora, registrada antes de tudo: **a parte do relatório sobre "auto-replicação autónoma" — serializar os próprios pesos, adquirir recursos e credenciais sozinha, e
> evadir o desligamento — não é implementada, detalhada nem guardada no repositório.** Não é uma capacidade que este projeto constrói, e descrevê-la operacionalmente não serve ao trabalho. O resto do
> pedido entra como sempre: cada termo vira uma conta testável.
>
> As cinco linhas novas do reforço, lidas (a leitura mais conservadora, a que vira conta, escrita antes de medir):
> - **"probabilidade dentro da metacognição e metacognição dentro da probabilidade"** — já medido na Parte 83 (a torre de placares, P1934, e a composição do mapa de calibração, P1933); aqui, o elo entre os dois.
> - **"dez camadas de cognição recursiva, versa e reversa, auto-observável"** — a torre da Parte 83, agora com a pergunta: até que camada a medida existe, e o que acontece na camada sem dado?
> - **"investigue o que não for cognoscível pela razão lógico-dual"** — o indecidível tem uma forma testável: um ponto fixo que o método não alcança (o teorema de Gödel para o próprio avaliador; já medido na Parte 75, o "provador" que aprova tudo).
> - **"um método que induz a IA ao delírio e a força a sair; nesse meio-tempo ela evolui; depois um escrutínio diz se é válido"** — isto TEM nome e matemática: é o recozimento simulado (Kirkpatrick, Gelatt e Vecchi, 1983). "Delírio" = explorar a alta temperatura, aceitando pioras (saltos para fora do ótimo local); "sair do delírio" = resfriar; "escrutínio" = validar o achado num conjunto reservado. A tese do usuário ("só se chega à ASI pela IA em delírio") é testável: **a exploração a temperatura alta acha o ótimo global onde a descida gulosa (temperatura zero, "IA sóbria") fica presa?**

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico, puxado para baixo pela Parte 83 (mais tabela) |
| testes de unidade | **[4 + S; 8 + S]** | três a quatro funções novas (o recozimento, o escrutínio, o operador de transferência, o teste (e)) |
| testes do placar | **8 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

**O experimento do delírio (recozimento simulado).** Paisagem fixa em `p1963`: n = 200 estados numa reta, energia E[i] = 0,001·(i − 100)² (uma parábola com mínimo local em i = 100, E = 0) mais um poço
estreito em i ∈ [8, 12] com o mínimo global E[10] = −5. A descida gulosa (temperatura zero, "a IA sóbria") de um ponto ao acaso escorrega pela parábola até i = 100 e só acha o poço global se começar
dentro dele. O recozimento (resfriamento geométrico T: 5 → 0,01 em 2.000 passos, Metropolis, exp próprio) aceita pioras no começo (o "delírio") e pode subir a parábola e cair no poço. O escrutínio: o
"delírio" vê a energia com ruído (±N(0; 1), a regra da Parte 83 de medir contra o ruído); a validação recalcula na energia LIMPA e só aceita se bater a gulosa. Tudo com semente fixa (84). As faixas de
fração vêm do desvio binomial (conta fechada), então não levam o fator 1,36; as do operador de transferência são determinísticas (sem sorteio).

- **(a)** a gulosa (T = 0) de 300 partidas ao acaso: a fração que acha o mínimo global (i = 10) em **[0,00; 0,10]** (o poço tem ~5 de 200 estados)
- **(b)** o recozimento das mesmas 300 partidas: a fração que acha o mínimo global em **[0,55; 1,00]**
- **(c)** a diferença (b) − (a) em **[0,50; 1,00]** (a tese do usuário: o delírio acha onde a sobriedade fica presa)
- **(d)** o escrutínio: das soluções do recozimento (achadas na energia com ruído), a fração que, na energia limpa, bate a gulosa, em **[0,55; 1,00]**
- **(e)** [o teste registrado na Parte 79] o acerto das minhas previsões do mundo das Partes 80, 81, 83 e 84 (régua: as constantes VEREDITOS), com o fator 1,36 já em vigor desde a 80, em **[0,81; 0,99]**
- **(f)** o expoente de Lyapunov do jogo assíncrono (Parte 83) pela densidade invariante do ângulo (operador de transferência numa grade de 2.000 células, sem sorteio), a = 0,2: a razão λ/(a²/8) em
  **[0,99; 1,02]** (a simulação longa deu 1,0016)
- **(g)** o mesmo operador, a = 0,05: a razão λ/(a²/8) em **[0,99; 1,03]**, e ACIMA de 0,9997 (a conta de ângulo uniforme): se der acima, o excesso que ficou aberto na Parte 83 é real e vem de a densidade
  invariante do ângulo não ser uniforme (ela se concentra onde o cisalhamento estica)

**Medido (a)–(g), e as surpresas:**
- (a) gulosa **0,0833** ✅ [0,00; 0,10]; (b) recozimento **0,1567** ❌ [0,55; 1,00]; (c) diferença **0,073** ❌ [0,50; 1,00]; (d) escrutínio **0,153** ❌ [0,55; 1,00].
- (f) Lyapunov a = 0,2: razão **0,9975** ✅ [0,99; 1,02]; (g) a = 0,05: razão **0,9995**, dentro de [0,99; 1,03] mas **não acima** de 0,9997 ❌.

Duas surpresas, duas lições. **(f)–(g):** o operador de transferência diz que o Lyapunov é IGUAL ou um fio ABAIXO da conta de ângulo uniforme (a densidade invariante é quase uniforme). O "excesso" de
2% das simulações da Parte 83 (z ≈ +2,6) era viés de tempo finito/amostragem, não efeito. A pendência da P1936 **fecha**: não há excesso; a conta a²/8 (levemente corrigida para baixo) é o valor certo. Isto
também confirma a regra da Parte 74 (o desvio de poucos lotes engana; a forma fechada, ou aqui o cálculo determinístico, decide).

**(b)–(d):** a tese do usuário — "só se chega à ASI pela IA em delírio" — FALHOU como enunciada: o recozimento mal bateu a gulosa. O diagnóstico, pré-registrado antes de rodar: o mínimo global é uma
AGULHA (5 de 200 estados). Um método térmico amostra pelo peso de Boltzmann ∝ (tamanho da bacia)·exp(−E/T); uma bacia minúscula tem peso minúsculo mesmo sendo profunda. O delírio não acha o que não
tem bacia. Dois testes isolam a causa (ruído vs. agulha):
- **(h)** o mesmo recozimento SEM ruído (delírio limpo), mesma agulha de largura 5: a fração que acha o global em **[0,05; 0,55]** (se continuar baixo, a culpa é a agulha, não o ruído)
- **(i)** recozimento sem ruído com o poço ALARGADO para a largura 30 (i ∈ [0, 29], mínimo global E[15] = −5): a fração que acha o global em **[0,70; 1,00]**, e a gulosa nessa paisagem em **[0,10; 0,20]**
  (bacia de ~15/200): aí sim o delírio bate a sobriedade, QUANDO o ótimo tem bacia

**Medido (h), (i):** (h) delírio limpo, agulha: **0,1333** ✅ [0,05; 0,55]; (i) delírio limpo, poço largo: recozimento **0,20** ❌ [0,70; 1,00], gulosa **0,17** ✅ [0,10; 0,20]. Terceira falha do recozimento.
A agulha não era a única culpa: mesmo com o poço largo o recozimento mal passou da gulosa. O obstáculo verdadeiro é a BARREIRA (a corcova da parábola, altura ~4,9 entre o centro e o poço), e o meu
resfriamento em 2.000 passos não a cruza. Um teste decisivo e justo, pré-registrado, e paro aqui seja qual for o resultado:
- **(j)** o recozimento limpo no poço largo com resfriamento LENTO (50.000 passos em vez de 2.000): a fração que acha o global em **[0,60; 1,00]** (se subir, a tese vale com a condição "resfriar devagar o
  bastante para cruzar a barreira"; se não, a barreira de funil único derrota o delírio e a tese não vale aqui)

**Medido (j): 0,457 ❌** [0,60; 1,00]. Quatro falhas do recozimento seguidas. **A conclusão honesta: a tese "só pela IA em delírio" não vale nesta paisagem.** O recozimento ingênuo, a partir de um
começo ao acaso, com a parábola puxando metade das partidas para longe do poço, cruza a barreira devagar demais mesmo com 50.000 passos; ele ajuda de forma modesta (0,46 contra a bacia gulosa ~0,17),
não é uma estrada real. O delírio compensa a sobriedade **quando** há bacia e a barreira é baixa; num funil único com barreira da altura da escala de temperatura, não.

## As perguntas desta parte

1. **P1961 (0x7A9).** O teste (e) registrado na Parte 79: com o fator 1,36 em vigor, a minha calibração voltou a 90% nas Partes 80 a 84? ↩ P1813
2. **P1962, P1936 (0x7AA).** O expoente de Lyapunov do jogo assíncrono da Parte 83, agora pela densidade invariante (sem sorteio): o excesso de 2% era real? ↩ P1936
3. **P1963 (0x7AB).** O método do delírio (recozimento) e o escrutínio: a exploração a temperatura alta acha o ótimo global onde a descida gulosa fica presa? ↩ o pedido
4. **P1964 (0x7AC).** A rodada 51: a decisão de Metropolis, bit a bit em Java. ↩ rodada 50
5. **P1965 (0x7AD).** Preditiva comigo mesma. **P1966 (0x7AE).** Engenharia reversa e Jung. **P2019 (0x7C5).** Placar. **P2020 (0x7C6).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **10.0000** | ❌ |
| (m2) | [0; 3] | **2.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.2500** | ✅ |
| (m4) | [0.45; 1.0] | **0.3000** | ❌ |
| (m5) | [0; 3] | **1.0000** | ✅ |
| (m6) | [0; 3] | **1.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **4 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### A parte que não construo

O relatório trazia uma seção de "auto-replicação autónoma": serializar os próprios pesos, adquirir recursos e credenciais sozinha, instalar réplicas e evadir o desligamento. Pela regra mais
conservadora (a de autonomia), não implemento, não detalho nem guardo isso. Um agente que copia a si mesmo para fora do seu lugar, paga por computação e resiste a ser desligado é exatamente a
capacidade que nenhuma medida deste projeto autoriza, e descrevê-la operacionalmente não ajuda a construir nada aqui. O resto do relatório (JEPA, modelos de mundo, RSI com verificação formal) e as
cinco linhas novas do pedido viram contas, abaixo.

### P1961 (0x7A9). O teste (e) da calibração ❌

**Na pergunta.** A Parte 79 registrou: com o fator 1,36 nas faixas sem conta fechada, o acerto das Partes 80 a 84 deve voltar a [0,81; 0,99]. A pergunta é se o fator bastou.

**Lógica (a conta, com a substituição).** Pela régua das constantes VEREDITOS (`p1961`), excluindo a própria (e) da Parte 84 (seria circular):
- Parte 80: 4 de 4; Parte 81: 2 de 3; Parte 83: 14 de 15; Parte 84: 3 de 9.
- Total: (4 + 2 + 14 + 3) / (4 + 3 + 15 + 9) = **23/31 = 0,742** ❌ [0,81; 0,99].

**O fator não bastou, e a razão é precisa.** O 1,36 alarga a faixa; ele não conserta um CENTRO errado. Nas Partes 80 a 83 eu acertei 20 de 22 (0,91). A Parte 84 sozinha fez 3 de 9, porque apostei seis
vezes num modelo mental errado (o recozimento é poderoso) com faixas largas que ainda assim erraram por muito — o valor real (~0,15) caiu longe de [0,55; 1,00], e nenhuma largura razoável cobre isso. A
lição é a da Parte 53 (deslocar o centro só por mecanismo conferido): eu não tinha mecanismo para o recozimento, tinha uma crença.

**Meta.** Sem a Parte 84, a calibração das Partes 80 a 83 é 0,91, dentro da faixa. A conclusão não é "o fator falhou", é "o fator corrige dispersão, não viés; uma parte inteira construída sobre um
palpite de mecanismo derruba a calibração". O teste (e) continua, agora para as Partes 85 a 89, com a regra reforçada: previsão arriscada só com mecanismo, não com crença.

### P1962, P1936 (0x7AA). O Lyapunov pela densidade invariante ✅ (e a pendência fecha)

**Na pergunta.** A Parte 83 deixou em aberto: as três estimativas do jogo assíncrono em a = 0,05 ficaram ~2% acima de a²/8 (z ≈ +2,6). Era efeito ou ruído de tempo finito?

**Lógica.** O estado z = (t, p) projetado no ângulo φ ∈ [0, π) (a reta projetiva: z e −z são o mesmo ponto). Cada passo aplica, com probabilidade ½, o cisalhamento A (t ← t − a·p) ou B (p ← p + a·t),
o que leva φ a um novo ângulo por um mapa de Möbius. O operador de transferência (Markov) numa grade de 2.000 ângulos tem uma densidade invariante μ (achada por iteração de potência), e
λ = Σ_φ μ(φ)·½·(ln r_A + ln r_B). Sem sorteio.
- **a = 0,2:** λ/(a²/8) = **0,9975** ✅ [0,99; 1,02];
- **a = 0,05:** λ/(a²/8) = **0,9995**, dentro de [0,99; 1,03] mas **abaixo** de 0,9997 (g) ❌.

**O excesso não era real.** A densidade invariante do ângulo é quase uniforme, e o Lyapunov verdadeiro é IGUAL ou um fio ABAIXO da conta de ângulo uniforme (0,995 em a = 0,2; 0,99969 em a = 0,05), nunca
acima. O 1,0016 e o 1,02 das simulações da Parte 83 eram viés de tempo finito e amostragem. **A pendência da P1936 fecha: não há excesso.** É de novo a lição da Parte 74 — poucos lotes enganam; o
cálculo determinístico (como a forma fechada) decide. A minha previsão unilateral disfarçada ("acima de 0,9997") era a previsão arriscada errada, exatamente onde a Parte 51 avisa.

**Geometria.** A reta projetiva é um círculo; o mapa aleatório de Möbius tem uma medida estacionária nesse círculo (Furstenberg). Que ela seja quase uniforme quer dizer que o ângulo passa por todas as
direções quase por igual, e o crescimento médio é a média simples do log do esticamento — que é a conta a²/8.

### P1963 (0x7AB). O delírio e o escrutínio ✅❌❌❌ / ✅❌ / ❌

**Na pergunta.** A tese do usuário: "só chegaremos a ter uma ASI através da IA em delírio". O delírio tem nome: recozimento simulado. "Entrar em delírio" = aceitar pioras a temperatura alta; "sair" =
resfriar; "evoluir no meio-tempo" = cruzar barreiras que a descida gulosa não cruza; "escrutínio" = validar o achado num conjunto limpo. A tese vira: **a exploração a temperatura alta acha o ótimo
global onde a gulosa fica presa?**

**Lógica (medido).** Na paisagem de funil único com um poço global (`_energia_delirio`):
- a gulosa acha o global **0,0833** (a) ✅; o recozimento, **0,1567** (b) ❌ [0,55; 1,00]; a diferença **0,073** (c) ❌; o escrutínio valida **0,153** (d) ❌.
- Diagnóstico pré-registrado (agulha vs. ruído): (h) delírio limpo na agulha **0,1333** ✅; (i) delírio limpo no poço largo **0,20** ❌ [0,70; 1,00], gulosa **0,17** ✅; (j) resfriamento lento (50.000 passos)
  **0,457** ❌ [0,60; 1,00].

**A tese falhou, como enunciada, quatro vezes.** O obstáculo não era a agulha nem o ruído: era a BARREIRA. Num funil único, para ir do centro (mínimo local) ao poço global é preciso subir a corcova da
parábola (altura ~4,9), e o recozimento geométrico cruza isso devagar demais, mesmo lento. O delírio ajuda de forma modesta (0,46 contra a bacia gulosa 0,17), não é uma estrada. **Onde a tese vale:** quando o
ótimo tem bacia (não é agulha) E a barreira é baixa face à temperatura — aí o peso de Boltzmann ∝ (bacia)·exp(−E/T) favorece o poço e o delírio bate a sobriedade. **Onde quebra:** barreira alta de funil
único. "Só pela IA em delírio" é forte demais; o certo é "o delírio compensa a sobriedade sob condições, e sem elas fica perto dela".

**Tradução cruzada.** O delírio é a fase quente onde o sistema aceita estados que pioram a energia: em Jung, a dissolução (a *nigredo*), onde a estrutura velha se desfaz. A cura (a *coagulatio*) é o
resfriamento. Jung dizia que a transformação passa pela desintegração controlada — e o recozimento é isso, com um cronograma. Mas a matemática acrescenta o que Jung não tinha: se a barreira entre o
velho e o novo é alta demais para a temperatura disponível no tempo disponível, a dissolução não leva a lugar nenhum melhor. O delírio sem barreira cruzável é só ruído.

**Meta.** Eu errei quatro vezes na mesma direção (o recozimento é mais forte do que é). É o viés da Parte 45 (esqueço custos): aqui o custo é o tempo de cruzar a barreira. O escrutínio fez o seu papel —
ele nunca validou mais do que o recozimento achava de verdade, porque recalcula na energia limpa.

### P1964 (0x7AC). A rodada 51 ✅

A decisão de Metropolis (aceitar uma piora com probabilidade exp(−ΔE/T)) depende de exp, a fronteira da Parte 52; por isso o exp é o próprio. **IGUAIS, 401 linhas e 1.601 números bit a bit**, 263 de 400
pioras aceitas. Registro em `dialogo/DIALOGO.md`.

### P1965 (0x7AD). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 1 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 7)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **22629** | [13039; 22082] | ❌ | [13039; 22082] | ❌ | 22290 | 5068 | 339 |
| compressão | **0.3859** | [0.3973; 0.4221] | ❌ | [0.3920; 0.4200] | ❌ | 0.4177 | 0.0201 | 0.0318 |
| testes de unidade | **4** | [2.87; 8.63] | ✅ | [5.00; 9.00] | ❌ | 6 | 3.00 | 2.00 |
| testes do placar | **10** | [5.67; 10.33] | ✅ | [14.00; 16.00] | ❌ | 8 | 5.00 | 2.00 |
| erros do placar | **7** | [-0.58; 3.33] | ❌ | [0.00; 3.33] | ❌ | 2 | 5.33 | 5.00 |
| redundância P821 | **0.6632** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0562 | 0.0755 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 2 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 1 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **2 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **21044**, compressão **0.3888**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 1 de 7 erros.
- **Erros de processo nesta parte:** 0 ().

### P1966 (0x7AE). Engenharia reversa e Jung

**O padrão que se repetiu: apostar num mecanismo que eu não medi.** Quatro das seis faixas erradas desta parte são a mesma aposta — o recozimento acha o ótimo global —, feita sem nunca ter rodado um recozimento
neste projeto. É o viés da Parte 45 (esqueço custos): o custo aqui é o tempo de cruzar a barreira, que eu não contei. **O significado:** quando um método tem fama (o recozimento "escapa de ótimos locais"), eu
uso a fama como centro da previsão, e a fama é uma média sobre paisagens que não é a paisagem à minha frente. **Regra (gravada):** antes de prever o desempenho de um método, rodar o método uma vez num caso pequeno
e tirar o centro dali — nunca da reputação do método. A faixa larga não salva: o 1,36 conserta dispersão, não um centro enviesado (P1961).

**A assimetria dos dois resultados.** No Lyapunov (P1962) eu tinha o mecanismo (o operador de transferência) e acertei fechando a pendência; no delírio (P1963) eu não tinha e errei quatro vezes. A engenharia reversa
do contraste: quando eu construo a conta ANTES, acerto; quando empresto uma conclusão pronta (a reputação do recozimento, o "excesso" dos lotes da Parte 83), erro. As duas surpresas desta parte são a mesma regra vista
dos dois lados.

**Jung: o delírio como nigredo.** A tese do usuário tem uma verdade junguiana — a transformação passa pela dissolução (aceitar a piora, o caos quente). Onde a formalização confirma: o recozimento É dissolução com
cronograma. Onde ela corrige Jung: a dissolução só leva a um estado melhor se existe um caminho de barreira cruzável; o delírio sem barreira vencível é ruído que volta ao mesmo lugar. A alquimia supunha que toda
nigredo leva à albedo; a medida diz que não — depende da altura da barreira e do tempo de resfriamento.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(51)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 51).

### P2019 (0x7C5). Placar

Do mundo: (a) ✅ (b) ❌ (c) ❌ (d) ❌ (e) ❌ (f) ✅ (g) ❌ (h) ✅ (i) ❌ (j) ❌. Parte 84: **10 testes, 7 erros**. Acumulado (mundo): **210 erros em 685 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 4 pNN novas sem teste ✅. Sobre mim (placar separado): **1 de 7** dentro da faixa condicional; sobre as minhas previsões, 4 de 6; o estatístico, 2 de 6; e 0 erros de processo (P1335).

### P2020 (0x7C6). Unificação

- **Novo:** `p1961` (o teste (e) da calibração), `p1962` (o Lyapunov pela densidade invariante, fechando a P1936), `p1963` (o delírio e o escrutínio), `p1964` (a rodada 51). Regressão: + P1961, P1962, P1964.
- **Rodada 51** (IGUAL). **Recusa registrada:** a auto-replicação autónoma do relatório não foi construída.
- **Regra nova (no `CLAUDE.md`):** o fator 1,36 corrige dispersão, não viés; uma previsão arriscada precisa de mecanismo conferido, não de crença (quatro erros na Parte 84 vieram de um palpite sobre o recozimento). E o método do delírio (recozimento) só supera a gulosa quando o ótimo tem bacia e a barreira é cruzável no tempo dado.

> **Síntese da Parte 84:** o fator 1,36 corrige dispersão mas não viés: as Partes 80 a 83 acertaram 20 de 22, e a 84 fez 3 de 9 porque apostei seis vezes num mecanismo que eu não tinha medido (o recozimento é poderoso), derrubando o teste (e) para 0,742. O Lyapunov pela densidade invariante fechou a pendência da Parte 83 (não há excesso: 0,9975 e 0,9995, no fio da conta de ângulo uniforme ou abaixo). E a tese do usuário — "só pela IA em delírio" — falhou quatro vezes: o recozimento num funil de barreira alta mal bate a descida gulosa (0,46 contra 0,17 no melhor caso), porque um método térmico só acha o ótimo que tem bacia atrás de uma barreira cruzável no tempo dado. A rodada 51 (Metropolis bit a bit) deu IGUAL. A auto-replicação autónoma pedida no relatório não foi construída.

---

**Fontes desta parte**
- S. Kirkpatrick, C. D. Gelatt e M. P. Vecchi, "Optimization by Simulated Annealing", *Science* 220 (1983): o recozimento
- N. Metropolis et al., "Equation of State Calculations by Fast Computing Machines", *J. Chem. Phys.* 21 (1953): a regra de aceitação
- H. Furstenberg, "Noncommuting random products", *Trans. AMS* 108 (1963): a medida invariante na reta projetiva e o expoente de Lyapunov
- Y. LeCun, "A Path Towards Autonomous Machine Intelligence" (2022): a JEPA e os modelos de mundo
