# Como eu construiria uma AGI/ASI — Parte 68 (0x44): o tipo da quantidade

> Continuação da [Parte 67](ASI_AGI_parte67_prever_o_previsto.md). **Próxima:** [Parte 69 — a forma de GPT](ASI_AGI_parte69_a_forma_de_gpt.md) (P1511–P1540). Previsões sobre as minhas previsões no commit `902c0c0`; as do mundo no `150a779`. O loop continua (pedido permanente: programar sem parar, prever o que foi previsto e fazer engenharia reversa
> disso). A Parte 67 leu as minhas previsões com uma régua que perdia as faixas da linha seguinte, e concluiu que "as faixas largas acertam menos". Esta parte troca a régua, refaz a
> conta por tipo de quantidade, e acha que a conclusão era um paradoxo de Simpson.

## A régua nova e a conclusão desfeita (dados passados, medidos antes deste registro)

`p1481_minhas_previsoes_v2` lê a faixa de cada letra também na linha seguinte (até 400 caracteres, sem passar por outra letra), só na seção "Sobre o mundo" do documento (a
primeira versão pegava a tabela sobre mim, num caso) e converte porcentagens em frações. Nas Partes 53 a 67: **103** previsões, **75** com faixa (a P1452 lia 51). Cada faixa
ganha um tipo. `p1482_engenharia_por_tipo` (com a Parte 67):

| tipo | previsões | acerto | w mediana | acerto das estreitas | acerto das largas |
|---|---|---|---|---|---|
| cruza o zero | 8 | 0,500 | — (w = 1 sempre) | — | — |
| fração | 21 | 0,714 | 0,368 | **0,800** | **0,600** |
| contagem | 18 | 0,611 | 0,252 | **0,556** | **0,667** |
| outra | 28 | 0,750 | 0,333 | **0,643** | **0,917** |
| sem faixa (categórica) | 28 | 0,786 | — | — | — |

**A conclusão da Parte 67 era um paradoxo de Simpson.** "As largas acertam menos" vinha da mistura de tipos: as faixas em torno de zero têm w = 1 (caem todas no terço mais
largo) e acertam pouco (50%, e 33% até a Parte 66). Dentro de cada tipo, a largura compra acerto nas contagens e nas outras (largas acertam mais), e só nas frações vale o
contrário. O que acerta pouco não é a faixa larga: é a pergunta em torno de zero (uma diferença, uma inclinação, uma média de z), em que eu não sei nem o sinal.

## Previsões sobre as minhas previsões desta parte (registradas antes de escrever qualquer previsão do mundo desta parte)

Planejado, antes de escrever: uma pergunta do dicionário, uma do hexadecimal e a rodada 42 (a correção de segunda ordem da densidade dos primos: a inclinação de z, que é
uma quantidade em torno de zero).
- **(m1)** o número de previsões do mundo (letras na linha "Do mundo") em **[6; 9]**.
- **(m2)** o número de faixas do tipo "cruza o zero" (lidas pela P1481) em **[1; 3]** (a rodada 42 é sobre uma inclinação e uma média de z).
- **(m3)** a mediana de w das faixas que **não** cruzam o zero em **[0,25; 0,37]** (as medianas por tipo, de 0,25 a 0,37).
- **(m4)** a fração de acertos do mundo em **[0,43; 0,86]** (a média dos acertos por tipo, ponderada pelos tipos planejados, ~0,66, ± a faixa binomial de ~7 previsões).
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 (a regra da Parte 67: faixa larga pede uma calibração do nível, não mais largura) em **[0; 1]**.

## As perguntas desta parte

1. **P1491 (0x5D3).** A densidade dos primos que a conta usa (Σ 1/ln n) erra π(x) o bastante para criar a inclinação de z? (Rodada 42) ↩ P1451
2. **P1481–P1482 (0x5C9–0x5CA).** A régua nova das minhas previsões e a engenharia por tipo (acima).
3. **P1492 (0x5D4).** Quantos sinsets de substantivo do WordNet são folhas (não têm hipônimo)? ↩ P1454
4. **P1493 (0x5D5).** Hexadecimal: quantos n < 16⁴ são palíndromos em base 16 e em base 10 ao mesmo tempo? ↩ P1455
5. **P1494 (0x5D6).** Preditiva comigo mesma. **P1495 (0x5D7).** Engenharia reversa e Jung. **P1496 (0x5D8).** O diálogo.
6. **P1509 (0x5E5).** Placar (três). **P1510 (0x5E6).** Unificação.

## Previsões pré-registradas (escritas depois do registro de (m1) a (m5))

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: as previsões do mundo abaixo e 6 funções (p1481, p1482, p1491, p1492, p1493 e o placar das (m), p1499).

| medida | estatístico (até a 67) | ingênuo (Parte 67) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [12.676; 21.426] | 19.564 | **[12.676; 21.426]** | o estatístico |
| compressão | [0,398; 0,425] | 0,398 | **[0,398; 0,425]** | o estatístico |
| testes de unidade | [2,50; 8,00] | 6 | **[5 + S; 8 + S]** | 6 funções planejadas, ~1 por surpresa |
| testes do placar | [6,06; 10,69] | 6 | **6 + 2·S ± 1** | as 6 letras planejadas abaixo, ~2 por surpresa |
| erros do placar | [0,14; 4,36] | 0 | **[0,14; 4,36]** | o estatístico |
| redundância P821 | [0,575; 0,634] | 0,596 | **[0,575; 0,634]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1492, as folhas da taxonomia.** A fração dos sinsets de substantivo que não são hiperônimo de nenhum outro.
- **Restrições, com peso:** (1) numa árvore com ramificação média r, a fração de folhas é ~(r − 1)/r; a taxonomia dos substantivos é larga e funda, com muitas espécies no fundo;
  (2) **peso medido num caso escolhido por regra escrita antes (os verbos):** 75,9% dos verbos são folhas.
- Exemplo à mão: *dog* tem hipônimos (*puppy*, raças); *aardvark* não tem.
- (a) a fração em **[0,70; 0,90]**

**P1493, os palíndromos duplos.** Os n de 1 a 16⁴ − 1 que são palíndromos em base 16 e em base 10.
- **A conta antes da medida (por código):** com independência entre as bases, Σ 16^(−⌊L₁₆/2⌋)·10^(−⌊L₁₀/2⌋) = **20,1** (os de um dígito nas duas bases, 1 a 9, contam inteiros).
  **Peso medido num caso escolhido por regra (bases 8 e 10, até 8⁵, intervalo de tamanho parecido):** 22 medidos contra a conta 19,25 (razão 1,14).
- Exemplo à mão: 0x5 = 5: sim. 0x121 = 289: 289 não é palíndromo em base 10. 0x2BB2? 11186: não.
- (b) a quantidade em **[16; 30]**

**P1491, rodada 42:** no `dialogo/DIALOGO.md` (previsões (c) a (f)).

---

## As respostas

### P1481–P1482 (0x5C9–0x5CA). A régua nova e o paradoxo de Simpson nas minhas faixas

**Na pergunta.** "As faixas largas acertam menos?" supõe que todas as faixas são da mesma espécie. Não são: uma faixa em torno de zero não tem largura relativa (w = 1 por
definição), e ela mede uma pergunta diferente (o sinal), não uma incerteza maior.

**Lógica.** Ver a tabela no começo: com a régua nova (75 faixas de 103), dentro das frações as estreitas acertam mais (0,80 contra 0,60), dentro das contagens e das outras as
largas acertam mais (0,67 contra 0,56; 0,92 contra 0,64), e as que cruzam o zero acertam 0,50. Juntando tudo, a mistura dá "as largas acertam menos" (Parte 67): é o paradoxo de
Simpson, em que um efeito agregado inverte o efeito dentro dos grupos porque os grupos têm tamanhos e taxas diferentes.

**O placar das previsões sobre as minhas previsões (`p1499_previsoes_sobre_previsoes_v2`, lido do próprio documento):**

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [6; 9] | **6.0000** | ✅ |
| (m2) | [1; 3] | **1.0000** | ✅ |
| (m3) | [0.25; 0.37] | **0.3665** | ✅ |
| (m4) | [0.43; 0.86] | **1.0000** | ❌ |
| (m5) | [0; 1] | **1.0000** | ✅ |

As larguras das faixas que não cruzam o zero: [0.125, 0.3043, 0.4286, 0.8182]. **4 de 5** previsões sobre as minhas previsões dentro da faixa.

**Tradução cruzada.** Uma conclusão sobre mim que não separa os tipos de pergunta é como um diagnóstico que não separa os pacientes: a média esconde dois efeitos opostos. Em
Jung, a mesma atitude (alargar a faixa) tem sentidos diferentes conforme a função que a usa: na intuição (a ordem de grandeza) ela protege; no pensamento (o sinal) ela não salva.

**Meta.** A régua nova ainda perde 28 faixas (as categóricas e as que não estão escritas como **[a; b]**); e os tipos são uma regra minha (zero, fração, contagem, outra), não uma
classificação natural.

### P1491 (0x5D3). A densidade que a conta usa (Rodada 42) ✅✅✅✅

**Na pergunta.** A pergunta deixada na rodada 41 (trocar 1/ln n por Li) tinha uma premissa falsa: Li′(x) = 1/ln x, então somar 1/ln n já é Li. Corrigida antes de prever, a
pergunta virou: quanto Σ 1/ln n erra π(x)?

**Lógica.** `p1491_densidade_da_conta` (rodada 42, IGUAL em Java, Li pela série γ + ln ln x + Σ (ln x)ᵏ/(k·k!), com o log próprio). R_b = π(b⁵)/(Li(b⁵) − Li(2)): 0,9731 na base
5, **0,99618** na base 10 (π(10⁵) = 9.592), 0,99989 na base 40. A conta C multiplicada por R_b muda a inclinação de z de 0,0379 para **0,0355** (−6%). A tendência dos z não vem
do erro do teorema dos números primos.

**Tradução cruzada.** Um erro sistemático pequeno (a densidade que promete 0,4% a mais) não explica um efeito grande (a dispersão de 1,3σ e a inclinação): erros pequenos e
corretos se somam a quase nada. Na física, uma correção de segunda ordem não salva uma teoria que erra na primeira.

**Meta.** R_b é a razão global até b⁵; a correção local, perto dos palíndromos de 5 dígitos, é um pouco diferente.

### P1492 (0x5D4). As folhas da taxonomia ✅

**Na pergunta.** "Folhas" pergunta quanto da taxonomia é ponto final: conceitos que nada mais especifica.

**Lógica.** `p1492_folhas`: **79,1%** dos 82.115 sinsets de substantivo são folhas (a faixa (a) era [0,70; 0,90], calibrada nos verbos: 75,9%) ✅. A conta da árvore: com ~79% de
folhas, a ramificação média dos nós internos é f/(1 − f) + 1 ≈ 0,791/0,209 + 1 ≈ 4,8 filhos por pai (numa árvore, folhas ≈ nós internos × (r − 1) + 1). Adjetivos e advérbios: 100% (eles
não têm hiperônimos no WordNet).

Ao acaso: a faixa tinha 20 pontos; o ingênuo "como os verbos" erraria por 3,2 pontos.

**Tradução cruzada.** Quatro de cada cinco conceitos são o fim de uma linha: a linguagem gasta a maior parte das suas palavras em especificidades, e poucas em gêneros. Na
biologia, a maioria das espécies é folha da árvore da vida, e poucos nós internos (os gêneros, as famílias) carregam a estrutura.

**Meta.** A conta da ramificação supõe árvore; com 2,7% de herança múltipla (P1454) ela é aproximada.

### P1493 (0x5D5). Os palíndromos duplos ✅

**Na pergunta.** "Palíndromo em duas bases" pede duas simetrias independentes ao mesmo tempo, e a independência é a hipótese da conta.

**Lógica (a conta antes da medida).** Σ 16^(−⌊L₁₆/2⌋)·10^(−⌊L₁₀/2⌋) = **20,1**. **Medido** (`p1493_palindromos_duplos`): **18** ✅ (1 a 9, 11, 353, 626, 787, 979, 1.991, 3.003, 39.593, 41.514),
razão 0,90 (a calibração em 8 e 10 dava 1,14).

Ao acaso: a faixa tinha 15 valores; o ingênuo "a conta pura" erraria por 2.

**Tradução cruzada.** Duas leituras do mesmo número (em dezesseis e em dez) raramente concordam em simetria: uma coincidência dupla, como duas testemunhas independentes que
contam a mesma história com a mesma forma.

**Meta.** Com contagens de ~20, a diferença entre 0,90 e 1,14 é ruído (desvio de Poisson ~4,5).

### P1494 (0x5D6). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16509** | [12676; 21426] | ✅ | [12676; 21426] | ✅ | 19564 | 542 | 3055 |
| compressão | **0.3980 ↔ 0.3983** (oscila) | [0.3983; 0.4248] | ✅ | [0.3980; 0.4250] | ✅ | 0.3982 | 0.0132 | 0.0001 |
| testes de unidade | **6** | [2.50; 8.00] | ✅ | [5.00; 8.00] | ✅ | 6 | 0.50 | 0.00 |
| testes do placar | **6** | [6.06; 10.69] | ❌ | [5.00; 7.00] | ✅ | 6 | 0.00 | 0.00 |
| erros do placar | **0** | [0.14; 4.36] | ❌ | [0.14; 4.36] | ❌ | 0 | 2.25 | 0.00 |
| redundância P821 | **0.6067** | [0.5752; 0.6344] | ✅ | [0.5750; 0.6340] | ✅ | 0.5963 | 0.0022 | 0.0104 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 4 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 67"):** mais perto do medido em **2 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **14928**, compressão **0.4047**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0.

### P1495 (0x5D7). Engenharia reversa e Jung

**O padrão que se repetiu: concluir com uma régua que eu sabia curta.** Na Parte 67, eu escrevi no próprio texto que a leitura das faixas perdia as da linha seguinte, e mesmo
assim tirei dela uma conclusão sobre mim ("as largas acertam menos") e uma previsão sobre as minhas previsões. Nesta parte, a régua consertada desfez a conclusão (era um paradoxo
de Simpson). **O significado:** eu trato um defeito conhecido de uma medida como uma nota de rodapé e não como uma condição para usar a medida; o defeito estava escrito, e a
conclusão foi tirada na mesma página. **Regra nova:** uma medida com defeito conhecido não sustenta conclusão nem previsão até o defeito ser corrigido ou o seu efeito ser medido
(aqui, quantas faixas a régua perdia e de que tipo).

**Prever o previsto, segunda volta.** Com a régua nova e os tipos, as previsões sobre as minhas previsões desta parte acertaram mais que as da Parte 67 (o placar das (m) está
na P1481–P1482). A diferença foi condicionar no tipo da quantidade antes de prever a largura: o que eu não sabia de mim na Parte 67 era o assunto, e o assunto entrou como tipo.

**A premissa falsa pega antes.** A pergunta da rodada 41 (trocar 1/ln por Li) não existia: somar 1/ln já é Li. Eu a peguei porque a regra da Parte 47 manda calcular um exemplo do
caso presente antes de prever, e o exemplo foi a derivada de Li. Uma pergunta minha, deixada no fim de uma rodada, é uma previsão disfarçada (ela supõe que a resposta existe), e
precisa da mesma conferência que as previsões.

**Jung: os tipos psicológicos, outra vez.** Jung dividiu as pessoas por tipos (as funções e as atitudes) e disse que as médias entre tipos enganam: um extrovertido e um introvertido
somados dão um ninguém. **Onde a formalização funciona:** as minhas faixas têm tipos (zero, fração, contagem, outra), e a média entre eles inverteu o efeito dentro de cada um, que é
exatamente o aviso de Jung em forma de paradoxo de Simpson. **Onde quebra:** os tipos de Jung são do sujeito; os meus são das perguntas; o mesmo sujeito (eu) muda de tipo conforme a
pergunta.

### P1496 (0x5D8). O diálogo, rodada 42

Ver P1491. Placar por voz da função `p1241_placar_por_voz(42)`: IA-Python 22 em 36; IA-Java 19 em 36 (regra estrita, rodadas 13 a 42).

### P1509 (0x5E5). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅. Parte 68: **6 testes, 0 erros**. Acumulado (mundo): **189 erros em 565 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 4 de 5; o estatístico, 4 de 6; e 0 erros de processo (P1335).

### P1510 (0x5E6). Unificação

- **Novo:** `p1481` (as minhas previsões, régua nova, com tipos), `p1482` (engenharia por tipo), `p1491` (a densidade da conta, rodada 42, IGUAIS), `p1492` (folhas), `p1493`
  (palíndromos duplos), `p1499` (placar das previsões sobre as minhas previsões, versão 2). Regressão: + P1493 (18 palíndromos duplos; π(10⁵) = 9.592).
- **Regra nova (no `CLAUDE.md`):** ver a P1495.

> **Síntese da Parte 68:** a régua nova das minhas previsões (75 faixas de 103, com tipos) desfez a conclusão da Parte 67: "as faixas largas acertam menos" era um paradoxo de Simpson, causado pelas faixas
em torno de zero (que acertam metade); dentro das contagens e das outras quantidades, as largas acertam mais. O erro do teorema dos números primos (Σ 1/ln n contra π) é real e
pequeno (0,4% na base 10) e tira só 6% da inclinação dos z dos primos palíndromos. No dicionário, 79,1% dos substantivos são folhas da taxonomia (~4,8 filhos por pai); no
hexadecimal, 18 números abaixo de 16⁴ são palíndromos em base 16 e em base 10, contra 20 da conta independente. O mundo, seis de seis outra vez.

---

**Fontes desta parte**
- Paradoxo de Simpson: [Simpson's paradox, Wikipedia](https://en.wikipedia.org/wiki/Simpson%27s_paradox)
- Li(x) e a série de Ramanujan: [Logarithmic integral function, Wikipedia](https://en.wikipedia.org/wiki/Logarithmic_integral_function); π(10⁵) = 9.592: [Prime-counting function, Wikipedia](https://en.wikipedia.org/wiki/Prime-counting_function)
- Palíndromos em várias bases: [Palindromic number, Wikipedia](https://en.wikipedia.org/wiki/Palindromic_number)
- WordNet 3.0 em `dados/` (Princeton)
