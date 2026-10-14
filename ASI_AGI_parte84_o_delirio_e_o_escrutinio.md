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
