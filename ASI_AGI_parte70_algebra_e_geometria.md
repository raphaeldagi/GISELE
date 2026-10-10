# Como eu construiria uma AGI/ASI — Parte 70 (0x46): álgebra e geometria

> Continuação da [Parte 69](ASI_AGI_parte69_a_forma_de_gpt.md). Previsões no commit `bb89374` ((a) a (i) e as (m)) e no `a7cef31` ((j)). Pedido do usuário, gravado no `CLAUDE.md`: **"Continue ao máximo que puder! Use álgebra e geometria! Grave na
> memória!"** Esta parte lê a forma de GPT e o dicionário como geometria e os resolve por álgebra: a lei de escala do GPT por mínimos quadrados em forma fechada; a geometria dos
> embeddings (ângulos entre letras, a componente principal por iteração de potência); a taxonomia do WordNet como espaço hiperbólico (o δ de Gromov); e os dígitos hexadecimais
> como vetores de GF(2)⁴.

## Previsões sobre as minhas previsões desta parte (prever o previsto)

**Uma observação de metacognição antes de prever:** ao planejar as calibrações desta parte eu já esbocei de cabeça as faixas das previsões do mundo. Prever agora o número delas e a
largura delas (as (m1), (m2), (m3) e (m5) das partes anteriores) seria prever o que eu já sei: não é teste. **"Prever o previsto" degenera quando o previsor já pensou as previsões.**
Registro só o que eu não posso saber ainda, e o resto fica fora do placar desta vez:
- **(m4)** a fração de acertos do mundo em **[0,56; 1,00]** (117 previsões das Partes 53 a 69 pela régua `p1481`: 74,4% de acerto; com 9 previsões, a faixa binomial de 90% vai de
  5/9 a 9/9).
- **(m6)** o número de surpresas (erros maiores que a largura da faixa) em **[0; 2]**.

## As perguntas desta parte

1. **P1541–P1542 (0x605–0x606).** A lei de escala da forma de GPT, por álgebra: quantos passos até empatar com o trigrama? E o dobro de d ajuda? (Rodada 44) ↩ P1513
2. **P1543 (0x607).** A geometria dos embeddings do GPT: o modelo descobre as vogais? ↩ P1513
3. **P1544 (0x608).** A taxonomia dos substantivos do WordNet é quase uma árvore? O δ de Gromov (a geometria hiperbólica). ↩ P1492, P1454
4. **P1545 (0x609).** Hexadecimal como álgebra: quantas janelas de 4 dígitos de π formam uma base de GF(2)⁴? ↩ P1515
5. **P1546 (0x60A).** Preditiva comigo mesma. **P1547 (0x60B).** Engenharia reversa e Jung. **P1548 (0x60C).** O diálogo.
6. **P1569 (0x621).** Placar (três). **P1570 (0x622).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: as 9 previsões do mundo abaixo, (a) a (i), e 5 funções novas (p1541 a p1545) mais a rodada 44 (p1549).

| medida | estatístico (até a 69) | ingênuo (Parte 69) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.680; 18.864] | 16.374 | **[13.680; 18.864]** | o estatístico |
| compressão | [0,398; 0,421] | 0,411 | **[0,398; 0,421]** | o estatístico |
| testes de unidade | [2,60; 8,15] | 9 | **[5 + S; 8 + S]** | 6 funções planejadas, uma por teste, ~1 por surpresa |
| testes do placar | [5,83; 9,67] | 8 | **9 + 2·S ± 1** | as 9 letras abaixo |
| erros do placar | [0; 3,52] | 0 | **[0; 3,52]** | o estatístico |
| redundância P821 | [0,563; 0,638] | 0,564 | **[0,563; 0,638]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1544, o δ de Gromov da taxonomia dos substantivos** (grafo não dirigido dos hiperônimos, a maior componente; 300 quádruplos sorteados com semente 70; distâncias por busca em largura).
- **Restrições, com peso:** (1) numa árvore, δ = 0 exatamente (os quatro pontos estão sobre uma árvore e as duas maiores somas empatam); (2) a herança múltipla cria ciclos e afasta δ
  de zero; os substantivos têm 2,7% de sinsets com dois pais (P1454), os verbos 0,23%; (3) **peso medido num caso escolhido por regra escrita antes (os verbos, 300 quádruplos):** δ
  máximo **2,0**, δ médio 0,038, **3,3%** dos quádruplos com δ > 0.
- Exemplo à mão: numa estrela (uma raiz com quatro filhos), todas as distâncias são 2, as três somas são 4, e δ = 0.
- (a) o δ máximo nos substantivos em **[1,0; 4,0]**
- (b) a fração dos quádruplos com δ > 0 em **[0,05; 0,40]** (mais herança múltipla que os verbos, ~12 vezes, mas cada ciclo afeta só os quádruplos que passam por ele)

**P1545, π em GF(2)⁴.** A fração das 9.997 janelas de 4 dígitos hexadecimais consecutivos de π que formam uma base de GF(2)⁴.
- **A conta antes da medida:** para dígitos independentes e uniformes, é |GL(4, 2)|/16⁴ = 15·14·12·8/65.536 = 20.160/65.536 = **0,30762**; o desvio de uma proporção de ~10.000 janelas
  (sobrepostas, então correlacionadas: o desvio efetivo é ~2 vezes o de janelas independentes) é ~0,009. **Peso medido num caso escolhido por regra (dígitos pseudoaleatórios, semente
  1570):** 0,3063.
- Exemplo à mão: as janelas 1, 2, 4, 8 (os vetores da base canônica) formam uma base; 1, 2, 3, x não (3 = 1 ⊕ 2).
- (c) a fração em **[0,290; 0,325]**

**P1543, a geometria dos embeddings** (o GPT inglês da curva de escala, d = 24, depois de 16.000 passos).
- **Restrições, com peso:** (1) com pesos ao acaso, os cossenos entre embeddings de dimensão 24 ficam em torno de 0 com desvio 1/√24 ≈ 0,2; (2) prever o próximo caractere obriga a separar
  as letras que ocupam as mesmas posições: vogais e consoantes alternam nas palavras; (3) **peso medido num caso escolhido por regra (o GPT português de 2.000 passos):** cosseno médio
  entre vogais **0,221**, entre vogal e consoante **−0,173** (diferença 0,394), entre consoantes 0,131; a primeira componente principal tem **17,6%** da variância.
- (d) a diferença (cosseno entre vogais) − (cosseno vogal-consoante) em **[0,15; 0,70]**
- (e) a fração da variância na primeira componente principal em **[0,10; 0,30]**

**P1541–P1542, rodada 44:** no `dialogo/DIALOGO.md` (previsões (f) a (i)).

### Previsão nova, nascida de um resultado inesperado (registrada antes de treinar)

**Resultado da rodada 44, antes desta seção:** o GPT com o dobro de d (22.978 pesos) ficou **pior** que o de d = 24 em 8.000 passos (+0,090 bit; a faixa (h) era [−0,35; −0,02]), e
piorou de 4.000 para 8.000 passos (3,237 → 3,258). **Hipótese:** a taxa de aprendizado (0,005) que serve para d = 24 é alta demais para d = 48 (no Adam, o passo de cada peso tem
tamanho ~lr, e um modelo maior com o mesmo passo oscila mais perto do mínimo). Teste num mundo novo (a mesma semente, metade da taxa):
- (j) o GPT de d = 48 com lr = 0,0025, 8.000 passos: bits por caractere em **[2,95; 3,17]** (abaixo do d = 24, 3,168, se a hipótese estiver certa).

**Resultado de (j):** com a taxa de aprendizado pela metade (0,0025), o GPT de d = 48 faz **3,120** bits em 4.000 passos e **3,021** em 8.000 ✅: 0,147 bit melhor que o d = 24 nos mesmos
8.000 passos (3,168) e 0,096 melhor que o d = 24 em 16.000 (3,117). O dobro de pesos ajuda, com o passo certo: a (h) errou porque eu mudei o tamanho e não o passo.

---

## As respostas

### P1544 (0x608). A taxonomia como espaço hiperbólico: o δ de Gromov ✅❌

**Na pergunta.** "Quase uma árvore" é uma pergunta de geometria: numa árvore, quaisquer quatro pontos satisfazem a condição dos quatro pontos com igualdade (as duas maiores das três
somas d(x,y)+d(z,w), d(x,z)+d(y,w), d(x,w)+d(y,z) são iguais), e δ = 0. Gromov chamou de δ-hiperbólico o espaço em que a diferença é no máximo 2δ: as árvores são os espaços 0-hiperbólicos,
e o plano hiperbólico tem δ finito; o plano euclidiano, não.

**Lógica.** `p1544_delta_de_gromov`, 300 quádruplos (semente 70), distâncias por busca em largura no grafo não dirigido dos hiperônimos:

| classe | nós | distância média | δ máximo | δ médio | fração com δ > 0 |
|---|---|---|---|---|---|
| verbos (calibração) | 6.844 | 12,44 | 2,0 | 0,038 | 0,033 |
| substantivos | **82.115** (todos, sob *entity*) | 13,39 | **2,0** (a) ✅ | 0,397 | **0,477** (b) ❌ |

O δ máximo é o mesmo nas duas (2,0), pequeno diante da distância típica (~13): **a taxonomia é δ-hiperbólica com δ ≈ 2, e δ/distância ≈ 0,15**, uma árvore "grossa". Mas a fração de
quádruplos com δ > 0 é 10 vezes a dos verbos (0,477 contra 0,033; δ médio 10,3 vezes): com 2,7% dos substantivos com dois pais (P1454), quase todo caminho longo passa perto de algum ciclo,
e metade dos quádruplos "sente" um. Eu previ [0,05; 0,40] supondo que cada ciclo afetaria poucos quádruplos; num grafo em que todos os caminhos sobem até *entity*, um ciclo perto do topo
afeta muitos.

**Tradução cruzada.** As hierarquias de conceitos se encaixam melhor em espaços hiperbólicos (onde o volume cresce exponencialmente com o raio, como o número de conceitos com a
profundidade) que em espaços euclidianos: é por isso que os embeddings de Poincaré (Nickel e Kiela, 2017) representam o WordNet em poucas dimensões. Em Jung, os arquétipos são poucos
perto da raiz e se ramificam em imagens sem fim: a psique também cresce como uma árvore hiperbólica.

**Meta.** 300 quádruplos dão a fração com desvio ~0,03; o δ máximo é um extremo amostral e pode ser maior no grafo inteiro.

### P1545 (0x609). π como álgebra sobre GF(2) ✅

**Na pergunta.** Um dígito hexadecimal é um vetor de 4 bits; quatro dígitos formam uma base de GF(2)⁴ quando são linearmente independentes sobre o corpo de dois elementos (somar é o ou
exclusivo). A pergunta já contém a conta: a fração das quádruplas de vetores que são bases é |GL(4, 2)|/16⁴.

**Lógica, linha por linha.** O primeiro vetor: qualquer um não nulo, 16 − 1 = 15; o segundo: fora do espaço gerado pelo primeiro (2 vetores), 16 − 2 = 14; o terceiro: fora de um plano (4
vetores), 16 − 4 = 12; o quarto: fora de um espaço de dimensão 3 (8 vetores), 16 − 8 = 8. |GL(4, 2)| = 15·14·12·8 = **20.160**; 20.160/65.536 = **0,30762**. **Medido**
(`p1545_bases_gf2`, eliminação de Gauss sobre GF(2)): π, **0,30269** (c) ✅; dígitos pseudoaleatórios (calibração), 0,30629. O desvio binomial com 9.997 janelas é **0,00462**
(`p1550`); π fica a −1,07 desvio (ou −0,53 com o dobro, pelas janelas sobrepostas): compatível com dígitos independentes.

**Tradução cruzada.** Quatro testemunhas são independentes quando nenhuma é a soma das outras: a independência linear é a forma algébrica de "cada uma traz informação nova".

**Meta.** As janelas sobrepostas compartilham três dígitos; o fator 2 no desvio é uma estimativa, não uma conta exata.

### P1543 (0x607). A geometria dos embeddings: o GPT descobre as vogais ✅✅

**Na pergunta.** "O modelo descobre as vogais?" pergunta se uma categoria da fonologia aparece como geometria (um cone de vetores) sem que ninguém a tenha ensinado.

**Lógica.** `p1543_geometria_dos_embeddings`, no GPT inglês de d = 24 depois de 16.000 passos: cosseno médio entre as 5 vogais **0,214**; entre vogal e consoante **−0,139**; entre consoantes
0,128. A diferença é **0,354** (d) ✅ (o português da calibração: 0,394); a primeira componente principal (autovalor dominante da covariância 24×24 por iteração de potência, dividido pelo
traço) tem **19,8%** da variância (e) ✅. Com pesos ao acaso, os cossenos teriam desvio 1/√24 = 0,20 e média 0: as vogais formam um cone (cosseno positivo entre si) e apontam para longe
das consoantes. Nenhum rótulo de vogal entrou no treino: a separação vem só de prever o próximo caractere, porque vogais e consoantes alternam.

**Tradução cruzada.** É a hipótese distribucional (Harris, 1954; Firth: "conhecerás uma palavra pela companhia que ela mantém") no nível das letras: duas letras que aparecem nos
mesmos contextos ficam próximas no espaço. Em Jung, os complexos se agrupam por afinidade de contexto emocional, não por definição.

**Meta.** Uma diferença de cossenos de 0,35 com 5 vogais é um efeito claro, mas o número de pares é pequeno (10 pares de vogais).

### P1541–P1542 (0x605–0x606). A lei de escala, por álgebra (Rodada 44) ✅✅❌✅ e (j)

**Na pergunta.** "Quantos passos até o trigrama" supõe que a curva continua igual fora dos dados: uma lei de potência extrapolada.

**Lógica.** `p1549_lei_de_escala` (rodada 44, IGUAL em Java, 7 números bit a bit). As equações normais da reta ln bits = ln A − α ln n nos 5 pontos de d = 24: **A = 5,185**, **α = 0,0541** (f) ✅;
n* = (A/2,768)^(1/α) = **1,10·10⁵** passos (g) ✅, o mesmo número que a calibração no português dava antes de medir. Para cair de 3,117 a 2,768, o dado precisa ser multiplicado por
(3,117/2,768)^(1/0,0541) = 9,0. O dobro de d (22.978 pesos), com a mesma taxa: α = 0,040, e **+0,090** bit em 8.000 passos (h) ❌; com metade da taxa, **−0,147** (j) ✅.

**Tradução cruzada.** Uma lei de potência com expoente pequeno (0,054) é a lei dos retornos decrescentes: cada dobra de esforço compra 3,7% de erro a menos. Na psicologia da prática
(a "lei da prática" de Newell e Rosenbloom), o tempo de uma tarefa cai como uma potência do número de tentativas, com o mesmo formato.

**Meta.** Cinco pontos não distinguem uma potência de uma potência com piso; a extrapolação a 10⁵ passos é uma previsão, não uma medida.

### P1546 (0x60A). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 2)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **19575** | [13680; 18864] | ❌ | [13680; 18864] | ❌ | 16374 | 3303 | 3201 |
| compressão | **0.4071** | [0.3979; 0.4208] | ✅ | [0.3980; 0.4210] | ✅ | 0.4114 | 0.0024 | 0.0043 |
| testes de unidade | **7** | [2.60; 8.15] | ✅ | [5.00; 8.00] | ✅ | 9 | 0.50 | 2.00 |
| testes do placar | **10** | [5.83; 9.67] | ❌ | [8.00; 10.00] | ✅ | 8 | 1.00 | 2.00 |
| erros do placar | **2** | [-0.77; 3.52] | ✅ | [0.00; 3.52] | ✅ | 0 | 0.24 | 2.00 |
| redundância P821 | **0.6351 ↔ 0.6440** (oscila através da borda da faixa) | [0.5628; 0.6379] | ⚠️ | [0.5630; 0.6380] | ⚠️ | 0.5637 | 0.0346 | 0.0714 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 3 ou 4 de 6 (a redundância oscila através da borda: ⚠️) dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 ou 6 de 7 (a mesma oscilação) dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 69"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **17536**, compressão **0.4162**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 2 erros.
- **Erros de processo nesta parte:** 1 (escrevi de cabeça "~7" para o fator de dado até o trigrama (é 9,0); corrigido antes do commit).

**Previsões sobre as minhas previsões:**

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m4) | [0.56; 1.0] | **0.8000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

As (m1), (m2), (m3) e (m5) ficaram fora do placar desta vez (eu já tinha pensado as faixas; ver a observação no começo). **2 de 2** previsões sobre as minhas previsões dentro da faixa.

### P1547 (0x60B). Engenharia reversa e Jung

**O padrão que se repetiu: mudar uma coisa e esquecer a que depende dela.** A previsão (h) errou porque eu dobrei o tamanho do GPT e mantive a taxa de aprendizado, como se o passo
fosse independente do tamanho; a (j), nascida do erro, corrigiu o passo e acertou. É a regra antiga da Parte 24 ("mudar uma função desloca o ótimo das outras: ao trocar um módulo, rever
os limiares calibrados com o módulo antigo"), e eu não a apliquei porque ela estava escrita para módulos da SYNTHAI e não para hiperparâmetros de um modelo. **O significado:** eu leio
as minhas regras pelo nome do objeto (módulo, limiar), não pelo mecanismo (um ótimo calibrado com uma coisa que mudou). **Regra ampliada:** toda mudança de escala (pesos, dados,
contexto) revê os parâmetros calibrados na escala anterior (a taxa, o número de passos), e a previsão diz quais foram revistos.

**Prever o previsto degenera, e eu disse antes.** Nesta parte eu notei, antes de registrar, que já tinha pensado as faixas do mundo ao planejar as calibrações, e por isso só registrei sobre
as minhas previsões o que eu não podia saber (a taxa de acerto e as surpresas). A engenharia reversa disso: o protocolo "prever as minhas previsões" só testa alguma coisa se o registro
vier antes de eu pensar as previsões; quando o planejamento das calibrações já as esboça, a ordem certa é registrar o "sobre as minhas previsões" antes de planejar as calibrações.

**As contas de cabeça que sobraram.** Uma ("~7", que era 9,0), pega pela regra da Parte 69 antes do commit. A regra funciona quando eu a executo; a estimativa continua aparecendo, e
continua sendo pega.

**Jung: a enantiodromia do tamanho.** Mais pesos deviam ser melhores e foram piores (h); com o passo menor, foram melhores (j). Jung via na enantiodromia o excesso de uma tendência que se
converte no oposto. **Onde a formalização funciona:** um passo grande demais para um modelo maior é literalmente um excesso que faz o treino oscilar em volta do mínimo e piorar com mais
passos (3,237 → 3,258). **Onde quebra:** não há conversão no oposto por necessidade; há um parâmetro mal ajustado, e a correção é uma conta (metade da taxa), não uma transformação.

### P1548 (0x60C). O diálogo, rodada 44

Ver P1541–P1542. Placar por voz da função `p1241_placar_por_voz(44)`: IA-Python 24 em 38; IA-Java 20 em 37 (regra estrita, rodadas 13 a 44).

### P1569 (0x621). Placar

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ❌ (i) ✅ (j) ✅. Parte 70: **10 testes, 2 erros**. Acumulado (mundo): **191 erros em 583 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 7 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 2 de 2; o estatístico, 4 de 6; e 1 erros de processo (P1335).

### P1570 (0x622). Unificação

- **Novo:** `p1541` (a escala do GPT), `p1542` (a lei de potência em forma fechada), `p1543` (a geometria dos embeddings), `p1544` (o δ de Gromov), `p1545` (GF(2)⁴), `p1549` (rodada 44,
  IGUAIS), `p1550` (contas auxiliares); `dialogo/escala44.tsv` (os pontos medidos). Regressão: + P1549 (α = 0,0541; π em GF(2)⁴ = 0,30269).
- **Pedidos permanentes novos (no `CLAUDE.md`):** álgebra e geometria; autonomia.

> **Síntese da Parte 70:** por álgebra e geometria: a taxonomia dos substantivos do WordNet é um espaço hiperbólico com δ de Gromov 2 (uma árvore grossa: δ/distância ≈ 0,15), mas metade dos quádruplos sente a
herança múltipla; os dígitos de π formam bases de GF(2)⁴ em 30,3% das janelas, como a conta |GL(4,2)|/16⁴ = 30,8% prevê para dígitos independentes; o GPT descobre sozinho as vogais
(um cone de vetores, cosseno +0,21 entre elas e −0,14 com as consoantes); e a lei de escala ajustada em forma fechada (α = 0,054, IGUAL em Java) prevê o empate com o trigrama em 1,1·10⁵
passos, como a calibração dizia. O dobro de pesos piorou com o mesmo passo e melhorou com metade dele (3,02 bits): o tamanho e o passo andam juntos.

---

**Fontes desta parte**
- δ de Gromov e espaços hiperbólicos: M. Gromov, "Hyperbolic groups" (1987); [Hyperbolic metric space, Wikipedia](https://en.wikipedia.org/wiki/Hyperbolic_metric_space)
- Embeddings hiperbólicos do WordNet: M. Nickel e D. Kiela, "Poincaré Embeddings for Learning Hierarchical Representations", [arXiv:1705.08039](https://arxiv.org/abs/1705.08039)
- GL(n, q) e a sua ordem: [General linear group, Wikipedia](https://en.wikipedia.org/wiki/General_linear_group)
- Leis de escala dos modelos de linguagem: J. Kaplan et al., "Scaling Laws for Neural Language Models", [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)
- Hipótese distribucional: Z. Harris, "Distributional structure", *Word* 10 (1954)
- Lei da prática: A. Newell e P. Rosenbloom, "Mechanisms of skill acquisition and the law of practice" (1981)
