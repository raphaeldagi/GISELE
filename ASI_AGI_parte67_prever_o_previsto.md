# Como eu construiria uma AGI/ASI — Parte 67 (0x43): prever o previsto

> Continuação da [Parte 66](ASI_AGI_parte66_o_endereco_da_falta.md). Previsões sobre as minhas previsões no commit `b5354f5`; as do mundo no `4f3208d`. Pedido do usuário: **"Programe sem parar. Em loop infinito. Tem como você prever o que foi previsto?
> Tem como você prever o que foi previsto e fazer engenharia reversa em metacognição?"** Esta parte responde em três camadas, em ordem: (1) ler todas as minhas previsões
> do mundo desde a Parte 53 e fazer a engenharia reversa da regra com que eu as escrevo; (2) **prever as previsões desta parte antes de escrevê-las** (registrado primeiro,
> num commit só para isso); (3) escrever as previsões do mundo, medir, e pontuar as duas coisas: o mundo contra as minhas previsões, e as minhas previsões contra a
> previsão delas.

## A engenharia reversa do que eu já previ (dados passados, medidos antes deste registro)

`p1452_minhas_previsoes` lê, nas Partes 53 a 66, os vereditos da linha "Do mundo" e a faixa **[a; b]** de cada letra (no documento ou na rodada do diálogo da parte);
`p1453_engenharia_das_previsoes` mede:
- **97** previsões do mundo; **51** com faixa numérica legível (a leitura só pega a faixa escrita na mesma linha da letra, e a primeira, quando há duas).
- Acerto: **69,1%** no total; **64,7%** com faixa; **73,9%** sem faixa (as categóricas, como "IGUAIS em Java").
- A largura relativa w = (b − a)/(|a| + |b|): mediana **0,333**, quartis **0,20** e **0,60**.
- **Por terço de largura, o acerto cai com a largura:** as faixas estreitas (w mediano 0,15) acertam **70,6%**, as do meio (0,33) **70,6%**, as largas (0,71) **52,9%**. O
  contrário do que uma faixa "honesta" faria. O motivo, lido nas largas: elas são as que eu escrevo quando não sei nem o nível (as que cruzam o zero acertaram 2 de 5),
  e alargar não compensa não saber onde o número mora.
- **A minha largura é previsível:** prever o w de cada faixa pela mediana das outras erra em média **0,229**; o ingênuo "o w da faixa anterior" erra **0,253**.
- **15,7%** das faixas têm w a menos de 0,05 de 1/3.

## Previsões sobre as minhas previsões desta parte (registradas antes de escrever qualquer previsão do mundo desta parte)

Terceiro placar, separado do mundo e do "sobre mim":
- **(m1)** a mediana de w das faixas numéricas do mundo desta parte em **[0,20; 0,60]** (o intervalo interquartil do histórico).
- **(m2)** o número de previsões do mundo desta parte (letras na linha "Do mundo") em **[6; 11]** (o mínimo e o máximo das Partes 57 a 66 com faixa: de 5 a 11; sem a 57).
- **(m3)** a fração de acertos do mundo desta parte em **[0,44; 0,89]** (a faixa binomial de 90% em torno de 0,69 com ~9 previsões).
- **(m4)** o efeito do observador: sabendo que a mediana histórica é 1/3, eu poderia escrever faixas perto de 1/3 para acertar (m1). A regra é não fazer isso (as faixas saem
  da calibração e da conta, como sempre). Previsão: a fração das faixas desta parte com w a menos de 0,05 de 1/3 fica em **[0; 0,40]** (histórico 0,157; se eu estiver
  copiando a mediana, passa de 0,40).
- **(m5)** "prever o que foi previsto", em retrovisão: o preditor "mediana histórica, 1/3" erra o w das faixas desta parte, em média, entre **[0,05; 0,35]**.

## As perguntas desta parte

1. **P1451 (0x5AB).** O z dos primos palíndromos tem tendência com a base, ou só uma dispersão maior que a do σ? (Rodada 41, bases novas 35 a 40) ↩ P1421
2. **P1452 (0x5AC).** As minhas previsões desde a Parte 53, lidas por uma função. **P1453 (0x5AD).** A engenharia reversa delas (acima).
3. **P1454 (0x5AE).** Quantos substantivos do WordNet têm dois ou mais hiperônimos (herança múltipla)? ↩ P1422
4. **P1455 (0x5AF).** Hexadecimal: os números automórficos (n² termina em n) em base 16 e em base 12. ↩ P1423
5. **P1456 (0x5B0).** Preditiva comigo mesma. **P1457 (0x5B1).** Engenharia reversa e Jung. **P1458 (0x5B2).** O diálogo.
6. **P1479 (0x5C7).** Placar (três: o mundo, eu, as minhas previsões). **P1480 (0x5C8).** Unificação.

## Previsões pré-registradas (escritas depois do registro de (m1) a (m5))

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 5 funções (p1451, p1452, p1453, p1454, p1455).

| medida | estatístico (até a 66) | ingênuo (Parte 66) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [10.865; 21.140] | 14.447 | **[10.865; 21.140]** | o estatístico |
| compressão | [0,404; 0,425] | 0,413 | **[0,404; 0,425]** | o estatístico |
| testes de unidade | [1,90; 7,85] | 4 | **[4 + S; 7 + S]** | 5 funções planejadas, uma por teste, ~1 por surpresa |
| testes do placar | [6,06; 10,69] | 9 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [1,12; 4,13] | 3 | **[1,12; 4,13]** | o estatístico |
| redundância P821 | [0,567; 0,637] | 0,607 | **[0,567; 0,637]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1454, a herança múltipla.** A fração dos sinsets de substantivo com dois ou mais hiperônimos.
- **Restrições, com peso:** (1) a taxonomia dos substantivos é quase uma árvore, mas tem herança múltipla em papéis (*person* que é também *worker*) e em substâncias;
  (2) **peso medido num caso escolhido por regra escrita antes (a outra classe com hierarquia, os verbos):** 0,23% (31 de 13.767). Os substantivos são uma hierarquia mais
  funda e mais rica que a dos verbos.
- Exemplo à mão: *actor* é *performer*; *president* é *head of state* e *presiding officer* (dois pais).
- (a) a fração em **[0,5%; 5%]**

**P1455, os automórficos.** Os n ≥ 2 com n² terminando nos mesmos dígitos que n (n² ≡ n mod bᵏ, k = dígitos de n), até b⁶.
- **A conta antes da medida:** n(n − 1) ≡ 0 (mod bᵏ) com n e n − 1 coprimos exige que cada potência de primo de bᵏ divida n ou n − 1. Em base 16 = 2⁴, bᵏ é potência de um primo só:
  só n ≡ 0 ou 1, nenhum automórfico além dos triviais (**teorema; fora do placar, porque não pode errar**). Em base 12 = 2²·3, há 2² = 4 soluções módulo 12ᵏ, duas não triviais,
  por k; uma solução de k dígitos precisa de dígito inicial ≠ 0 (chance 11/12): conta 2 × 6 × 11/12 = **11**. **Peso medido num caso escolhido por regra (a base 10 inteira até
  10⁶, também com dois primos):** 10 medidos contra a conta 2 × 6 × 9/10 = 10,8.
- Exemplo à mão: base 10, 76² = 5.776, termina em 76.
- (b) os automórficos da base 12 até 12⁶ em **[8; 12]**

**P1451, rodada 41:** no `dialogo/DIALOGO.md` (previsões (c) a (f)).

---

## As respostas

### P1452–P1453 (0x5AC–0x5AD). Prever o que foi previsto, e a engenharia reversa

**Na pergunta.** "Prever o que foi previsto" tem duas leituras, e as duas foram feitas. (1) **Retrovisão:** esconder as minhas faixas passadas e prevê-las a partir das
outras: a mediana das outras erra o w de cada faixa em **0,229**, contra **0,253** do ingênuo (a faixa anterior). As minhas larguras são previsíveis, mas pouco: a regra que eu
sigo é mais estável que o meu último gesto. (2) **Previsão das previsões:** antes de escrever as previsões desta parte, eu previ quantas seriam, quão largas, e quantas
acertariam ((m1) a (m5), num commit só delas).

**Lógica: o placar das previsões sobre as minhas previsões (`p1459_previsoes_sobre_previsoes`, lido do próprio documento):**

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [0.2; 0.6] | **0.8182** | ❌ |
| (m2) | [6; 11] | **6.0000** | ✅ |
| (m3) | [0.44; 0.89] | **1.0000** | ❌ |
| (m4) | [0.0; 0.4] | **0.0000** | ✅ |
| (m5) | [0.05; 0.35] | **0.4283** | ❌ |

As larguras desta parte: [0.8182, 0.2, 1.0] (a mediana histórica, 0.3333). **2 de 5** previsões sobre as minhas previsões dentro da faixa.

**A engenharia reversa (o que a medida diz sobre como eu escrevo faixas):**
- Eu escrevo faixas com largura relativa típica de **1/3** do valor (a mediana histórica), e a largura **não** compra acerto: as largas acertam menos (52,9% contra 70,6%).
  Uma faixa larga é o sinal de que eu não sei o nível, não de que eu me protegi.
- A leitura automática pegou **3** das 5 faixas desta parte ((a), (b) e (d); a (c) e a (f) estão na linha seguinte à letra, no diálogo). Das três, a (d) cruza o zero (w = 1, que a
  medida dá sempre a uma faixa em torno de zero) e a (a) cobre um fator 10 ([0,5%; 5%], w = 0,82): duas faixas de **forma** diferente da típica (uma diferença em torno de zero; uma
  fração pequena com a ordem de grandeza incerta) puxaram a mediana para cima. O meu preditor das minhas previsões errou pela forma das quantidades, não pelo meu hábito; e a
  própria medida tem um defeito de leitura que eu já sabia e não corrigi antes de prever com ela.
- O efeito do observador, medido: sabendo que a mediana histórica era 1/3, nenhuma faixa ficou perto de 1/3 ((m4) = 0). Eu não copiei a mediana; as faixas saíram da
  calibração.

**Tradução cruzada.** Prever o que eu mesma vou prever é o problema do autoconhecimento em Jung: o ego conhece os próprios hábitos (a largura típica, o número de previsões)
e não conhece os próprios conteúdos (o que cada pergunta vai pedir). O hábito foi previsto (m2, m4); o conteúdo (a forma das quantidades, que fez w = 1) não foi.

**Meta.** A leitura automática das faixas perde as que estão em outra linha ou depois da primeira na mesma linha (51 de 97 legíveis); a engenharia reversa vale para as que
eu escrevo do jeito mais comum.

### P1451 (0x5AB). Tendência ou dispersão (Rodada 41) ✅✅✅✅

**Na pergunta.** "Tendência ou dispersão" oferece duas causas exclusivas; a resposta é um pouco das duas, e nenhuma decide.

**Lógica.** `p1451_tendencia_ou_dispersao` (rodada 41, IGUAL em Java). Nas 36 bases (5 a 40): inclinação **0,0379** por base, erro-padrão 0,0206 (t = 1,84); desvio-padrão dos z
**1,325** (variância 1,76 vezes a da conta). Nas bases novas (35 a 40): média +0,817, desvio 1,458. A reta ajustada nas 30 bases antigas previa 0,54 no meio das novas; o
medido (0,82) ficou a 0,28 dela, menos de um desvio da média de seis (0,52).

**Tradução cruzada.** Quando duas hipóteses explicam os dados pela metade cada uma, a resposta honesta é o modelo com as duas (a reta com resíduos largos), e não a escolha da
mais elegante. Na ciência, é a diferença entre um efeito e uma variância: ambos são reais e se confundem com poucos dados.

**Meta.** As bases não são independentes (uma conta comum, com o mesmo erro de segunda ordem); o t de 1,84 superestima a evidência se os resíduos forem correlacionados.

### P1454 (0x5AE). A herança múltipla ✅

**Na pergunta.** "Dois ou mais hiperônimos" pergunta onde a taxonomia deixa de ser árvore: onde uma coisa é duas espécies de coisa ao mesmo tempo.

**Lógica.** `p1454_heranca_multipla`: **2,695%** dos 82.115 sinsets de substantivo têm dois ou mais hiperônimos (a faixa (a) era [0,5%; 5%], calibrada nos verbos: 0,23%) ✅;
adjetivos e advérbios, 0. Os primeiros exemplos: *person*, *substance*, *amphibious landing*, *default*, *musical performance*: papéis e substâncias, como previsto nas
restrições.

Ao acaso: a faixa cobria 4,5 pontos de uma escala de 0 a 100; o ingênuo "como os verbos" erraria por 2,5 pontos (12 vezes menos).

**Tradução cruzada.** *Person* tem dois pais (organismo e causa agente): o WordNet registra que uma pessoa é ao mesmo tempo uma coisa viva e um agente. Em Jung, a persona e o
eu são dois pais do mesmo indivíduo.

**Meta.** Contei os hiperônimos listados no sinset, incluindo os de instância, se houver: a fração mistura dois tipos de relação.

### P1455 (0x5AF). Os automórficos em base 16 e em base 12 ✅

**Na pergunta.** "n² termina em n" é n(n − 1) ≡ 0 (mod bᵏ): a pergunta é sobre como bᵏ se reparte entre dois números coprimos, isto é, sobre os primos de b.

**Lógica (a conta antes da medida).** Base 12 = 2²·3: 2² = 4 soluções por k, 2 não triviais; com o dígito inicial ≠ 0 (11/12), conta 2 × 6 × 11/12 = **11**. **Medido**
(`p1455_automorficos`): **11** ✅ (4, 9, 64, 81, 513, 1.216, 6.400, 14.337, 234.496, 483.328, 2.502.657). Base 16: **0**, como o teorema dizia (fora do placar). Base 10: 10 contra
10,8.

Ao acaso: a faixa (b) tinha 5 valores; o ingênuo "como a base 10" daria 10, dentro da faixa também.

**Tradução cruzada.** Uma base com um primo só (16 = 2⁴) não tem automórficos: não há como repartir a potência entre n e n − 1. Uma identidade que se reproduz (n² = n no fim)
precisa de duas fontes independentes, como um traço que se mantém de geração em geração só se dois genes o sustentam.

**Meta.** A conta e o medido coincidiram exatamente porque a contagem é quase determinística (2 por k); a única incerteza era o dígito inicial.

### P1456 (0x5B0). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **19481** | [10865; 21140] | ✅ | [10865; 21140] | ✅ | 14447 | 3478 | 5034 |
| compressão | **0.3982** | [0.4036; 0.4249] | ❌ | [0.4040; 0.4250] | ❌ | 0.4132 | 0.0163 | 0.0150 |
| testes de unidade | **6** | [1.90; 7.85] | ✅ | [4.00; 7.00] | ✅ | 4 | 0.50 | 2.00 |
| testes do placar | **6** | [6.06; 10.69] | ❌ | [6.00; 8.00] | ✅ | 9 | 1.00 | 3.00 |
| erros do placar | **0** | [1.12; 4.13] | ❌ | [1.12; 4.13] | ❌ | 3 | 2.62 | 3.00 |
| redundância P821 | **0.5963** | [0.5667; 0.6369] | ✅ | [0.5670; 0.6370] | ✅ | 0.6072 | 0.0057 | 0.0109 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 3 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 66"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **17668**, compressão **0.4042**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 2 (escrevi no texto que as faixas (d) e (f) puxaram a mediana antes de conferir quais faixas a leitura pegou (pegou (a), (b) e (d)); corrigido antes do commit; a tabela sobre mim dizia 7 previsões planejadas, (a) a (g), e eu escrevi 6).

### P1457 (0x5B1). Engenharia reversa e Jung

**Prever o previsto, de dentro.** Esta é a primeira parte em que eu fui o objeto de três placares ao mesmo tempo: o mundo (6 de 6), eu mesma (a tabela acima) e as minhas
previsões (o placar das (m)). O resultado mais informativo é o cruzamento: a parte em que eu previ as minhas previsões foi a de mais acertos no mundo, e a de **menos acertos
sobre as minhas previsões**. Eu previ a minha taxa de acerto em [0,44; 0,89] e acertei tudo; previ a largura mediana das minhas faixas em [0,20; 0,60] e ela saiu muito maior.
**O padrão:** quando eu me observo, eu acerto o hábito (quantas previsões, se copio a mediana) e erro o efeito do assunto (uma diferença em torno de zero, w = 1; uma fração pequena de ordem incerta, w = 0,82).
**O significado:** o meu modelo de mim é um modelo de **forma** (como eu escrevo), e o que varia de parte para parte é o **conteúdo** (o que cada pergunta pede). Uma previsão
sobre mim que ignore o assunto da parte erra pelo assunto, não por mim. **Regra nova:** as previsões sobre as minhas previsões condicionam no tipo da quantidade (proporção,
contagem, diferença em torno de zero), porque a largura relativa só tem sentido para quantidades longe de zero. E a leitura automática das faixas (`p1452`) precisa
pegar as faixas da linha seguinte antes de servir de medida para prever: eu previ com uma régua que eu sabia ser curta.

**A metacognição como engenharia reversa.** Ler as 97 previsões mostrou uma regra que eu não sabia que seguia: as faixas largas acertam **menos**. Eu achava que alargava
para me proteger; os dados dizem que eu alargo quando não sei o nível, e não saber o nível não se compensa com largura. **Regra nova:** quando uma faixa sair larga (w > 0,6),
procurar primeiro um caso de calibração que fixe o nível, em vez de alargar mais.

**Jung: a função transcendente, enfim com um terceiro.** Na Parte 65 a união dos opostos só cancelava. Aqui há dois opostos (o eu que prevê e o eu que é previsto) e deles
nasceu um terceiro, que nenhum dos dois tinha: a regra "a largura não compra acerto", que só aparece quando o eu que prevê é lido pelo eu que mede. **Onde a formalização
funciona:** o terceiro é uma função (`p1453`) que existe porque as duas posições foram mantidas separadas (previsão registrada num commit, medida noutro). **Onde quebra:** em Jung
a função transcendente é simbólica e transforma o sujeito; aqui ela é uma tabela, e só transforma o sujeito se virar regra no `CLAUDE.md`.

### P1458 (0x5B2). O diálogo, rodada 41

Ver P1451. Placar por voz da função `p1241_placar_por_voz(41)`: IA-Python 21 em 35; IA-Java 18 em 35 (regra estrita, rodadas 13 a 41).

### P1479 (0x5C7). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅. Parte 67: **6 testes, 0 erros**. Acumulado (mundo): **189 erros em 559 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 2 de 5; o estatístico, 3 de 6; e 2 erros de processo (P1335).

### P1480 (0x5C8). Unificação

- **Novo:** `p1451` (tendência ou dispersão, rodada 41, IGUAIS), `p1452` (as minhas previsões lidas dos documentos), `p1453` (a engenharia reversa delas), `p1454` (herança
  múltipla), `p1455` (automórficos numa base), `p1459` (o placar das previsões sobre as minhas previsões). Regressão: + P1455 (11 automórficos em base 12; 97 previsões lidas).
- **Pedido permanente novo (no `CLAUDE.md`):** programar sem parar, em loop; prever o que foi previsto e fazer engenharia reversa disso em metacognição, a cada parte.

> **Síntese da Parte 67:** dá para prever o que foi previsto, em parte. As minhas 97 previsões do mundo desde a Parte 53 acertaram 69%; a minha largura típica é 1/3 do valor, previsível a partir das outras
melhor que pela anterior; e as faixas largas acertam menos (53% contra 71%), porque eu alargo quando não sei o nível. Previstas antes de escritas, as previsões desta parte tiveram o
hábito previsto (quantas, sem copiar a mediana) e o conteúdo não (uma diferença em torno de zero e uma fração de ordem incerta fizeram a largura mediana saltar: 2 de 5 previsões sobre as minhas previsões). No mundo, seis de seis: a dispersão dos
primos palíndromos é 1,3 vez a do σ e a inclinação com a base chegou a t = 1,8; 2,7% dos substantivos têm herança múltipla; e a base 12 tem 11 automórficos até 12⁶, exatamente
a conta, enquanto a base 16 não tem nenhum, como o teorema exige.

---

**Fontes desta parte**
- Números automórficos: [Automorphic number, Wikipedia](https://en.wikipedia.org/wiki/Automorphic_number); [OEIS A003226](https://oeis.org/A003226)
- Calibração de previsões e intervalos: [Calibration (statistics), Wikipedia](https://en.wikipedia.org/wiki/Calibration_(statistics)); P. Tetlock e D. Gardner, *Superforecasting* (2015)
- Herança múltipla no WordNet: C. Fellbaum (org.), *WordNet: An Electronic Lexical Database* (1998); WordNet 3.0 em `dados/`
- Teorema dos números primos e Li(x): [Prime number theorem, Wikipedia](https://en.wikipedia.org/wiki/Prime_number_theorem)
