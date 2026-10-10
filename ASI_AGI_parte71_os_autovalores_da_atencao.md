# Como eu construiria uma AGI/ASI — Parte 71 (0x47): os autovalores da atenção

> Continuação da [Parte 70](ASI_AGI_parte70_algebra_e_geometria.md). **Próxima:** [Parte 72 — o que está disfuncional](ASI_AGI_parte72_o_que_esta_disfuncional.md) (P1601–P1630). O loop segue sozinho (pedido do usuário: "não pare mais"), com álgebra e geometria e a forma de GPT crescendo.

## Previsões sobre as minhas previsões desta parte (registradas ANTES de planejar as calibrações, pela regra da Parte 70)

Neste momento eu ainda não pensei faixa nenhuma desta parte; sei só os temas (os autovalores da atenção do GPT, a rodada 45; uma pergunta do dicionário; uma do hexadecimal). O histórico
pela régua `p1481` (Partes 53 a 70): **127** previsões, **74,8%** de acerto; por tipo, as que cruzam o zero acertam 55,6%, as frações 76,7%, as contagens 66,7%, as outras 77,1%, as
categóricas 81,2%; as medianas de w por tipo vão de 0,29 a 0,47.
- **(m1)** o número de previsões do mundo em **[6; 10]**.
- **(m2)** o número de faixas que cruzam o zero em **[0; 2]**.
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,10; 0,50]**.
- **(m4)** a fração de acertos do mundo em **[0,55; 1,00]**.
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**.
- **(m6)** o número de surpresas em **[0; 2]**.

## As perguntas desta parte

1. **P1571–P1572 (0x623–0x624).** Quantas direções a atenção do GPT usa? Os valores singulares de W_Q W_Kᵀ por Jacobi, e a razão de participação (Rodada 45). ↩ P1543
2. **P1573 (0x625).** A geometria do crescimento: quantos sinsets de substantivo há em cada profundidade? A taxonomia cresce como um espaço hiperbólico? ↩ P1544
3. **P1574 (0x626).** Hexadecimal como polinômios sobre GF(2): os irredutíveis de grau 15 e os "gêmeos" (f, f ⊕ x ⊕ x²). ↩ P1545
4. **P1575 (0x627).** Preditiva comigo mesma. **P1576 (0x628).** Engenharia reversa e Jung. **P1577 (0x629).** O diálogo.
5. **P1599 (0x63F).** Placar (três). **P1600 (0x640).** Unificação.

## Previsões pré-registradas (escritas depois do registro das (m))

### Sobre mim (placar separado), condicionais ao número S de surpresas

Planejadas: as 6 previsões do mundo abaixo, (a) a (f), e 5 funções novas (p1571 a p1574 e a rodada 45, p1578).

| medida | estatístico (até a 70) | ingênuo (Parte 70) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.588; 20.030] | 19.769 | **[13.588; 20.030]** | o estatístico |
| compressão | [0,398; 0,421] | 0,408 | **[0,398; 0,421]** | o estatístico |
| testes de unidade | [2,72; 8,53] | 7 | **[4 + S; 7 + S]** | 5 funções, uma por teste, ~1 por surpresa |
| testes do placar | [5,67; 10,33] | 10 | **6 + 2·S ± 1** | as 6 letras abaixo |
| erros do placar | [0; 3,17] | 2 | **[0; 3,17]** | o estatístico |
| redundância P821 | [0,565; 0,651] | 0,644 | **[0,565; 0,651]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1573, o crescimento da taxonomia dos substantivos.** O número de sinsets em cada profundidade r e o fator por nível e^λ da reta de ln N(r) contra r, nas profundidades 1 a 8.
- **Restrições, com peso:** (1) num espaço hiperbólico (uma árvore), N(r) cresce como a ramificação elevada a r (a P1492 dava ~4,8 filhos por pai interno); (2) mas a taxonomia não é cheia:
  ela fica mais fina perto das folhas e acaba em profundidade ~18; (3) **peso medido num caso escolhido por regra escrita antes (os verbos):** os verbos têm o máximo na profundidade 2 e
  encolhem depois (fator 0,54 por nível nas profundidades 1 a 8): a hierarquia dos verbos é rasa. Os substantivos são uma hierarquia funda (profundidade média ~8, P793).
- Exemplo à mão: *entity* (0) → *physical entity*, *abstraction*, *thing* (1) → … → *dog* (13).
- (a) o fator por nível nos substantivos em **[1,2; 3,0]**
- (b) a profundidade com mais sinsets em **[7; 11]**

**P1574, os gêmeos irredutíveis sobre GF(2).** Os polinômios de grau 15 (os números de 0x8000 a 0xFFFF) irredutíveis, e os pares (f, f ⊕ x ⊕ x²) com os dois irredutíveis.
- **A conta antes da medida:** Gauss: N(15) = (2¹⁵ − 2⁵ − 2³ + 2)/15 = **2.182** (teorema: fora do placar). Os gêmeos por um bit só (f, f ⊕ x) **não existem** (um irredutível de grau > 1 tem
  número ímpar de termos, e trocar um bit troca a paridade): descoberto na calibração, que deu 0 contra a conta de 48. Com dois bits (f ⊕ x ⊕ x²), a conta ingênua é N²/2¹⁴/2 = **145,3**.
  **Peso medido em casos escolhidos por regra (os graus ímpares logo abaixo, 11 e 13):** 28 contra 16,9 (razão 1,66) e 76 contra 48,4 (razão 1,57).
- (c) os gêmeos de grau 15 em **[180; 300]** (a conta × razão de 1,24 a 2,06)

**P1571–P1572, rodada 45:** no `dialogo/DIALOGO.md` (previsões (d) a (f)).

### Previsão nova, nascida de um resultado inesperado (registrada antes de medir o grau 17)

Os gêmeos de grau 15 deram 224, **1,54** vez a conta ingênua (145,3). A conta que explica o excesso, feita depois de ver os números (por isso só vira evidência num mundo novo): a série singular
de Hardy–Littlewood em F₂[x] (`p1579`). Para cada irredutível p de grau k, multiplicar pela chance de p não dividir nenhum dos dois, dividida pela chance se fossem independentes,
(1 − ν_p/2^k)/(1 − 1/2^k)²:
- p = x e p = x + 1: x + x² ≡ 0 (ν = 1), então f e o vizinho têm o mesmo resto: fator (1/2)/(1/4) = **2** cada (o termo constante e a paridade).
- p = x² + x + 1: x + x² ≡ 1, então os restos proibidos são 0 e 1 (ν = 2): fator (2/4)/(9/16) = **8/9**.
- todos os outros: ν = 2, fatores um pouco abaixo de 1.

A série vale S = **3,3315**, e a conta é N²/2^g · S/2. Contra a medida: grau 11, 28 contra 28,1 (razão **0,995**); grau 13, 76 contra 80,7 (**0,942**); grau 15, 224 contra 242,0 (**0,926**).
A razão cai devagar com o grau.

- **(g)** os gêmeos (f, f ⊕ x ⊕ x²) de grau 17 em **[642; 756]**: a conta de 755,5 vezes uma razão de 0,85 a 1,00 (continuação da queda, de 0,926 para ~0,91, com folga dos dois lados).

**Resultado de (g), medido logo depois do registro:** **758** gêmeos de grau 17 ❌ (por 2 acima do teto; a conta da série singular dava 755,5, razão **1,003**). A conta acertou; o que errou foi
a "queda" que eu li em três razões. O desvio de Poisson de cada razão é 1/√conta (por código): 0,189, 0,111 e 0,064, e os z das três medidas são −0,03, −0,52 e −1,16. A "tendência" estava
dentro do ruído, e eu a extrapolei sem perguntar o tamanho do ruído.

- **(h)** os gêmeos de grau 19 em **[2.338; 2.500]**: a conta 2.419,2 ± 1,645·√2.419 (a faixa de 90% da Poisson, sem tendência nenhuma). Registrada antes de medir.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [6; 10] | **8.0000** | ✅ |
| (m2) | [0; 2] | **0.0000** | ✅ |
| (m3) | [0.1; 0.5] | **0.2500** | ✅ |
| (m4) | [0.55; 1.0] | **0.7500** | ✅ |
| (m5) | [0; 2] | **0.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1571–P1572 (0x623–0x624). Quantas direções a atenção usa (Rodada 45) ✅✅✅

**Na pergunta.** "Quantas direções" já supõe que a atenção é uma geometria: o escore entre o caractere t e o j é a forma bilinear e_t M e_jᵀ/√d, com M = W_Q W_Kᵀ. Uma forma bilinear se lê
pelos seus valores singulares, e "quantas direções" é o posto efetivo.

**Lógica (álgebra).** Os valores singulares de M são as raízes dos autovalores de MᵀM, uma matriz simétrica 16 × 16. O método de Jacobi zera, a cada rotação, o maior elemento fora da diagonal:
tan 2θ = 2a_pq/(a_qq − a_pp), e as rotações só usam + − × ÷ e √. A razão de participação é PR = (Σλ)²/Σλ², com λ = σ².
- O caso de controle, com a substituição: em [[2, 1], [1, 2]], Jacobi dá 2,9999999999999996 e 0,9999999999999998 (exatos: 3 e 1, erro de um ulp).
- Medido (d = 16, inglês, 2.000 passos): λ = 222,84; 52,69; 11,81; 8,64; 4,76; 2,11; 1,44; 0,63; … ; 0,0004; 0,0.
- Σλ = 305,62 e Σλ² = 222,84² + 52,69² + … = 52.676 (por código), o que dá PR = 305,62²/52.676 = **1,773** e uma fração do maior de 222,84/305,62 = **0,729**.
- Uma gaussiana 16 × 16 ao acaso (semente 1) dá PR **8,634**. A conta: para uma matriz de Wishart quadrada, os λ seguem a lei do quarto de círculo de Marchenko–Pastur, com E[λ²]/E[λ]² = 2,
  e então PR → d/2 = 8.
- O treino tira 8,6/1,77 = **4,9** vezes de "dimensão" da atenção.
- (d) IGUAIS ✅ (18 números bit a bit em Java), (e) PR em [1,3; 3,5] ✅, (f) fração do maior em [0,45; 0,85] ✅. A chance de acerto por sorte de (e): uma faixa de largura 2,2 numa reta que vai de
  1 a 16 (o PR possível), ~15%. O ingênuo "igual à calibração no português" (1,95) erraria por 0,18, menos que a minha faixa: (e) acertou, mas o ingênuo também teria acertado.

**Geometria.** Um último autovalor 0 é obrigatório? Não por posto: M é 16 × 16 com W_Q e W_K de 16 × 16. O 0,0 que aparece é menor que 5·10⁻⁵ (arredondado a 4 casas). A atenção vive numa
elipse muito achatada: o eixo maior tem √222,8 = 14,9 e o segundo, √52,7 = 7,3. A forma é quase um segmento.

**Tradução cruzada.** A atenção como psicologia é o foco da consciência. Um foco de posto ~2 compara cada caractere com os outros por uma ou duas qualidades só, que é o que William James chamava
de estreiteza da atenção, aqui medida. O caminho inverso: a física de um condensado, em que muitos modos colapsam num só, é a "fixação" de um complexo.

**Meta.** O PR depende do tamanho do treino: 5,42 sem treino e 1,95 com 2.000 passos no português. Não sei se ele continua caindo ou volta a subir com mais passos (a literatura mostra
gargalos de posto baixo na atenção quando a cabeça é pequena: Bhojanapalli et al., 2020). Pergunta para a Rodada 46.

### P1573 (0x625). A taxonomia como espaço hiperbólico que se afina ❌✅

**Na pergunta.** "Cresce como um espaço hiperbólico?" pede uma taxa por nível. Uma árvore de ramificação b tem N(r) = b^r, e o fator por nível é b.

**Lógica.** O fator por nível é e^λ, com λ a inclinação de mínimos quadrados de ln N(r) contra r, nas profundidades 1 a 8 (forma fechada: λ = Σ(r − r̄)(y − ȳ)/Σ(r − r̄)²).
- Os substantivos: N = 3, 22, 228, 2.020, 6.249, 12.267, 18.936, 14.155 (r = 1 a 8). O fator saiu **3,536**, contra a faixa (a) [1,2; 3,0] ❌ (por 0,54, menos que a largura de 1,8: não é surpresa).
- O máximo fica em r = **7** ✅ (b) [7; 11].
- Os verbos (calibração): o fator é 0,536 e o máximo fica em r = 2.

**Por que (a) errou.** A calibração dos verbos media o fator numa hierarquia que já encolhe a partir de r = 2. Nos substantivos, as profundidades 1 a 8 incluem os primeiros níveis, que
crescem explosivamente:
- os fatores entre níveis vizinhos são 22/3 = 7,3, 228/22 = 10,4, 2.020/228 = 8,9, 6.249/2.020 = 3,1, 12.267/6.249 = 1,96, 18.936/12.267 = 1,54, 14.155/18.936 = 0,75;
- a média geométrica deles é (14.155/3)^(1/7) = 3,35, e a reta de mínimos quadrados dá 3,54, porque pesa mais as pontas.

Eu escolhi "1 a 8" como a janela e pensei no fator de uma árvore que já se afina, mas a janela é dominada pelos três primeiros saltos ((2.020/3)^(1/3) = 8,76 por nível, por código). **A forma:** um espaço hiperbólico no
topo (8,76 vezes mais sinsets a cada nível) que se afina para uma esfera achatada embaixo (o máximo em 7, a cauda até 18).

**Tradução cruzada.** O topo da taxonomia é um nascimento de categorias (cada nível tem 8,76 vezes os sinsets do anterior; não é o número de filhas por pai, porque há herança múltipla e folhas); o meio, uma maturidade; a cauda, um envelhecimento em que só restam as linhagens
especializadas. É a curva de população de uma coorte, lida como psicologia do conceito: generalizar é fácil no começo e raro no fundo.

**Meta.** A faixa (a) foi calibrada num caso (os verbos) em que o mecanismo (a fase de crescimento) não existia: a calibração não estava perto do teste na variável que move o mecanismo
(regra da Parte 63). Eu a escolhi por uma regra escrita antes, o que vale a regra da Parte 64; mas a regra da Parte 65 também valia, e eu não perguntei se os verbos cobriam a fase de crescimento.

### P1574 e P1579 (0x626 e 0x62B). Os gêmeos irredutíveis e a série singular ✅❌✅

**Na pergunta.** "Gêmeos" vem dos primos gêmeos (p, p + 2). Em F₂[x], o análogo de "+ 2" é somar um polinômio fixo s. A primeira pergunta da calibração (s = x) se respondeu sozinha: 0 gêmeos,
porque um irredutível de grau > 1 tem um número ímpar de termos (senão f(1) = 0 e x + 1 o divide), e somar x troca a paridade. Isso é o análogo exato de "não existem primos gêmeos (p, p + 1)
além de (2, 3)".

**Lógica.** Gauss, com a substituição: N(15) = (2¹⁵ − 2⁵ − 2³ + 2)/15 = (32.768 − 32 − 8 + 2)/15 = 32.730/15 = **2.182** = o crivo. Os gêmeos (f, f ⊕ x ⊕ x²) de grau 15 deram **224** ✅ (c) [180; 300].
A série singular (`p1579`), com a conta feita fator por fator:
- p = x e p = x + 1: (1 − 1/2)/(1 − 1/2)² = 0,5/0,25 = 2 cada;
- p = x² + x + 1: (1 − 2/4)/(1 − 1/4)² = 0,5/0,5625 = 0,8889;
- os dois de grau 3: ((1 − 2/8)/(1 − 1/8)²)² = (0,75/0,7656)² = 0,9796² = 0,9596;
- os três de grau 4: (0,875/0,8789)³ = 0,9867;
- … e o produto até o grau 40 dá S = **3,3315**.

A conta dos gêmeos é N²/2^g · S/2. No grau 17: 7.710²/131.072 · 3,3315/2 = 453,5 · 1,6658 = **755,5**, e o medido foi **758**, razão 1,003 (z de Poisson +0,09). A faixa (g) [642; 756] ❌
errou por 2, porque eu extrapolei uma "queda" (0,995 → 0,942 → 0,926) que tinha z de −0,03, −0,52 e −1,16: era ruído. Com a faixa de Poisson, (h) para o grau 19 deu [2.338; 2.500] e o
medido foi **2.456** ✅ (razão 1,015). Contra o ingênuo:
- a conta sem a série (N²/2^g = 1.452) erraria por 1.004;
- a chance de acertar ao acaso numa faixa de largura 162 entre 0 e N/2 = 13.797 é ~1,2%.

**Geometria.** A soma por s = x + x² é uma translação no hipercubo {0,1}^g. Os irredutíveis são um conjunto que evita os subespaços afins "divisível por p". Os fatores ν_p dizem quantos desses
subespaços a translação leva em si mesma: 1 para x e x + 1, que a translação preserva (por isso o fator 2), e 2 para os outros.

**Tradução cruzada.** Um par só sobrevive junto quando as proibições dos dois coincidem. A paridade é uma proibição que eles dividem, e por isso dobra a chance; a de x² + x + 1, os dois têm que
evitar em restos diferentes, e por isso ela pesa mais. Lido como psicologia: dois traços que dependem da mesma condição de fundo andam juntos mais do que a conta independente diz.

**Meta.** A heurística de Hardy–Littlewood em F_q[t] está provada no limite de q grande e grau fixo (Bary-Soroker; Bender e Pollack). Para q = 2 e o grau crescendo, ela continua sendo
conjectura, e o que testei foram números, não um teorema.

### P1575 (0x627). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 2)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **21925** | [13588; 20030] | ❌ | [13588; 20030] | ❌ | 19769 | 5116 | 2156 |
| compressão | **0.4174** | [0.3975; 0.4205] | ✅ | [0.3980; 0.4210] | ✅ | 0.4077 | 0.0079 | 0.0097 |
| testes de unidade | **6** | [2.72; 8.53] | ✅ | [4.00; 7.00] | ✅ | 7 | 0.50 | 1.00 |
| testes do placar | **8** | [5.67; 10.33] | ✅ | [5.00; 7.00] | ❌ | 10 | 2.00 | 2.00 |
| erros do placar | **2** | [-0.67; 3.17] | ✅ | [0.00; 3.17] | ✅ | 2 | 0.42 | 0.00 |
| redundância P821 | **0.5788** | [0.5654; 0.6509] | ✅ | [0.5650; 0.6510] | ✅ | 0.6440 | 0.0292 | 0.0652 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 70"):** mais perto do medido em **3 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **20214**, compressão **0.4248**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 2 erros.
- **Erros de processo nesta parte:** 1 (escrevi de cabeça a média geométrica (3,5; é 3,35), "~9 por nível" (8,76) e Σλ² "≈ 52.700" (52.676); corrigidos antes do commit).
- **Sem ponto fixo:** a cada volta do preenchimento, a redundância alterna entre 0,5758 e 0,5788 e a compressão entre 0,4174 e 0,4176 (ciclo de 3 voltas). Os vereditos são os mesmos em todas as versões; a tabela mostra a última (medida antes desta linha).

### P1576 (0x628). Engenharia reversa e Jung

**O padrão que se repetiu: dar mecanismo ao ruído.** Três razões (0,995, 0,942, 0,926) viraram uma "queda", e a faixa (g) foi deslocada para baixo por ela; o grau 17 deu razão 1,003 e
errou por 2. Os z de Poisson das três eram −0,03, −0,52 e −1,16, e nenhum deles distinguia uma queda de um sorteio. É o mesmo erro da Parte 61, quando o "dobro" das bases pares era só a base 8:
eu vejo uma forma numa sequência curta e lhe dou causa antes de medir o ruído. **O significado:** a minha leitura de uma sequência começa pela forma (sobe, cai, dobra), e o tamanho do
ruído vem depois, quando vem. **Regra nova (um passo verificável):** antes de extrapolar uma tendência de k pontos, calcular por código o desvio de cada ponto (Poisson: 1/√n) e o t da
inclinação; sem |t| > 2, a previsão usa o centro da conta sem tendência e a faixa do ruído. Aplicada logo em seguida, ela fez (h) acertar (2.456 em [2.338; 2.500]).

**O segundo padrão: a calibração sem o mecanismo.** A faixa (a), o fator de crescimento dos substantivos, foi calibrada nos verbos, uma hierarquia que já encolhe a partir da profundidade 2.
Os substantivos têm uma fase de crescimento (8,76 por nível nos três primeiros) que os verbos não têm, e foi ela que levou o fator a 3,54. A regra da Parte 65 ("a calibração cobre a faixa
da variável que move o mecanismo") existia; eu cumpri a da Parte 64 (a regra escrita antes) e esqueci a 65. Parte 65 de novo: as regras valem juntas, e eu aplico a que estiver mais à mão.
**Passo verificável:** em cada calibração, uma linha "o mecanismo que move o teste está presente no caso de calibração? sim ou não, e por quê".

**O custo de um erro pequeno.** (g) errou por 2 (não é surpresa: a largura era 114) e mesmo assim abriu um teste novo, (h). A previsão "testes do placar = 6 + 2·S ± 1" errou porque S só conta os
erros grandes. **O significado:** o custo de um erro depende de onde o erro está (no mecanismo ou na conta), não do seu tamanho. Um erro que revela um raciocínio falso, mesmo por pouco, gera
um teste; um erro de largura, não.

**As contas de cabeça.** Três nesta parte: a média geométrica (escrevi 3,5; é 3,35), "~9 por nível" (8,76) e Σλ² "≈ 52.700" (52.676). Todas foram pegas pela conferência por código antes do commit.

**Jung: a sincronicidade e o ruído.** Jung chamou de sincronicidade a coincidência significativa sem causa, e testou a ideia num experimento astrológico com os mapas de casais (1952): o
primeiro lote parecia confirmá-la, e os lotes seguintes não. **Onde a formalização funciona:** "significativa" vira um z; a minha "queda" tinha z −1,16, uma coincidência sem significado, e o lote
novo (o grau 17) a desfez, como os lotes novos de Jung desfizeram o primeiro. **Onde quebra:** Jung definiu a sincronicidade como acausal e fora da estatística, e a formalização só alcança a
parte que ele admitia testar.

### P1577 (0x629). O diálogo, rodada 45

Ver P1571–P1572. Placar por voz da função `p1241_placar_por_voz(45)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 45). Pergunta para a Rodada 46: quanto se perde ao trocar
M pela sua melhor aproximação de posto 1?

### P1599 (0x63F). Placar

Do mundo: (a) ❌ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ✅. Parte 71: **8 testes, 2 erros**. Acumulado (mundo): **193 erros em 591 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 5 de 6; e 1 erros de processo (P1335).

### P1600 (0x640). Unificação

- **Novo:** `p1571` (Jacobi), `p1572` (a razão de participação), `p1573` (o crescimento da taxonomia), `p1574` (os irredutíveis e gêmeos sobre GF(2)), `p1578` (rodada 45, IGUAIS), `p1579` (a série
  singular). Regressão: + P1574 e P1579.

> **Síntese da Parte 71:** por álgebra (Jacobi, só + − × ÷ e √, IGUAL em Java nos 18 números), a atenção do GPT treinado usa 1,77 direção das 16 (o maior valor singular leva 73% da energia), contra 8,6 de uma matriz ao acaso. A taxonomia dos substantivos cresce 8,8 vezes por nível no topo, como um espaço hiperbólico, e se afina até a profundidade 18, com o máximo em 7. Os irredutíveis sobre GF(2) formam pares (f, f ⊕ x ⊕ x²) na quantidade que a série singular de Hardy–Littlewood prevê (S = 3,33: grau 17, 758 contra 755,5; grau 19, 2.456 contra 2.419), e nunca pares (f, f ⊕ x), pela paridade. O erro da parte foi dar mecanismo ao ruído: uma "queda" de três pontos com z de −1,2.

---

**Fontes desta parte**
- Algoritmo de Jacobi: C. G. J. Jacobi (1846); [Jacobi eigenvalue algorithm, Wikipedia](https://en.wikipedia.org/wiki/Jacobi_eigenvalue_algorithm)
- Atenção de posto baixo: S. Bhojanapalli et al., "Low-Rank Bottleneck in Multi-head Attention Models", ICML 2020, [arXiv:2002.07028](https://arxiv.org/abs/2002.07028)
- Lei de Marchenko–Pastur: V. Marchenko e L. Pastur (1967); [Marchenko–Pastur distribution, Wikipedia](https://en.wikipedia.org/wiki/Marchenko%E2%80%93Pastur_distribution)
- Primos gêmeos em F_q[t]: L. Bary-Soroker, "Hardy–Littlewood tuple conjecture over large finite fields", IMRN (2014), [arXiv:1206.3930](https://arxiv.org/abs/1206.3930);
  E. Bender e P. Pollack, "On quantitative analogues of the Goldbach and twin prime conjectures over F_q[t]"; O. Gorodetsky e W. Sawin, [arXiv:1811.04834](https://arxiv.org/abs/1811.04834)
- Fórmula de Gauss para os irredutíveis: [Irreducible polynomial / Necklace polynomial, Wikipedia](https://en.wikipedia.org/wiki/Necklace_polynomial)
- Embeddings hiperbólicos do WordNet: M. Nickel e D. Kiela, [arXiv:1705.08039](https://arxiv.org/abs/1705.08039)
