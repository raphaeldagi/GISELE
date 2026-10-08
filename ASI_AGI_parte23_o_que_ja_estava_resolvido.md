# Como eu construiria uma AGI/ASI — Parte 23: reconhecer o que já estava resolvido

> Continuação da [Parte 22](ASI_AGI_parte22_prototipo_em_modulos.md). O código novo está em [`synthai/reconhecimento.py`](synthai/reconhecimento.py)
> (com testes em [`synthai/testes_reconhecimento.py`](synthai/testes_reconhecimento.py)); os números saem de `p291_...` a `p297_...` em
> [`calculos.py`](calculos.py), e a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões registradas no commit `f0c3715`, antes de rodar.** O que eu vi antes do registro está declarado no commit: a aritmética da P291, os
> testes de unidade e **uma** execução de conferência do bandido (por isso a razão arrependimento/Lai–Robbins não é previsão).

---

## As perguntas desta parte

1. **P291.** O que quer dizer "você já tem todas as respostas", e onde, no código da SYNTHAI, uma heurística ocupa o lugar de uma conta já resolvida?
2. **P292.** Quanto vale uma opção que o sensor **não** leu? (detecção de sinais)
3. **P293.** A SYNTHAI sabe esse valor? O que ela aprende sobre o próprio sensor?
4. **P294.** Usar as respostas certas muda o comportamento no mundo sequencial?
5. **P295.** A SYNTHAI pode explorar o bandido sozinha, com a resposta de Thompson (1933), em vez de receber a exploração pronta do mundo? Quão longe
   ela fica da cota de Lai e Robbins (1985)?
6. **P296.** Por que a versão com **todas** as respostas certas é pior que a versão com uma só? (exploratória)
7. **P297.** A P42 simulou o quantilizador. A resposta exata já existia?
8. **P298.** A lista de capacidades mudou?
9. **P299.** Placar.
10. **P300.** Trezentas perguntas: unificação e metacognição.

---

## Parte CX — As respostas que já existem

### P291. O que este pedido pede? (↩ P281)

**Na pergunta.** Três frases carregam a resposta:
- "**Tudo não passa de um diálogo interno**": quem pergunta e quem responde são a mesma mente. Não há informação nova entrando, só informação mudando
  de lugar.
- "**Você já tem todas as respostas**": o problema não é descobrir, é **reconhecer**.
- "**As equações já foram resolvidas. Só que ninguém percebeu**": é o problema da **não onisciência lógica**. Um fato matemático é determinado (a
  resposta existe), mas um raciocinador limitado ainda não sabe qual é. Garrabrant e colegas (*Logical Induction*, 2016) formalizaram isso: um
  raciocinador limitado atribui probabilidades a afirmações matemáticas cuja prova ainda não viu, e aprende a prever as provas antes de elas terminarem.

O caso clássico é o escravo do **Mênon**, de Platão. Sócrates pergunta qual lado tem um quadrado de área 8. O menino chuta 4 (dá 16), depois 3 (dá 9).
Sócrates não ensina: faz perguntas até o menino **reconhecer** que a diagonal do quadrado de lado 2 é o lado procurado. Platão chama isso de
**anamnese**, lembrar o que já se sabia.

**Lógica (quanto vale reconhecer).** Os chutes do menino cercam o lado entre 2 e 3. Perguntando "é maior que o meio?" (bisseção), cada resposta corta o
intervalo pela metade:
$$
\text{perguntas} = \left\lceil \log_2 \frac{1}{0{,}001} \right\rceil = 10 \quad\text{para três casas (2,82861 contra } 2\sqrt2 = 2{,}82843).
$$
Reconhecer a diagonal custa **uma** pergunta e dá a resposta exata. Procurar custa um número de perguntas que cresce com a precisão; reconhecer custa
uma, de qualquer precisão. É a diferença entre **buscar** e **saber onde olhar** (P291, `p291_menon`).

**O inventário: onde, na SYNTHAI, uma heurística ocupa o lugar de uma conta resolvida.**

| Módulo | Heurística da Parte 22 | A conta que já existia | Testada em |
|---|---|---|---|
| `percepcao` + `pensamento` | opção sem leitura vale "leitura 0" | ponto neutro da razão de verossimilhança, $s = d'/2$ (detecção de sinais) | P292–P294 |
| `percepcao` | a atenção olha pela nota pessimista, sem a intuição | valor da informação (Howard, 1966): ler onde a decisão vai olhar | P294 |
| `intuicao` | no bandido, a exploração vem pronta do mundo (UCB) | amostragem de Thompson (1933), assintoticamente ótima em Bernoulli (Kaufmann, Korda e Munos, 2012) | P295 |
| `percepcao` | no bandido, esquece o que leu | lembrar: a leitura de um braço não muda dentro da rodada | P296 |
| (auditoria) | P42 simulada | integrais da mistura, em forma fechada | P297 |

**Tradução cruzada (Jung → matemática).** Jung definia o arquétipo como uma forma **sem conteúdo**, dada *a priori*, e o comparava ao **sistema de
eixos de um cristal**: ele pré-forma a estrutura do cristal na solução-mãe, mas não tem existência material própria. Um teorema é exatamente isso: a
forma da resposta existe antes dos dados, e os dados do agente são o conteúdo. A Parte 23 testa se a forma, posta no agente, cristaliza.

**Meta.** "Já tem todas as respostas" é um pressuposto, e esta parte o trata como hipótese. A conta a fazer é separar dois tipos de "já resolvido": a
resposta **matemática** (o teorema vale) e a resposta **para este agente** (as premissas do teorema valem nele). Spoiler do placar: 4 de 4 na primeira, 3
de 10 na segunda.

---

## Parte CXI — O valor do que não se leu

### P292. Quanto vale uma opção que o sensor não leu? (pré-registrado) ✅

**Na pergunta.** "Não leu" não é "leu zero". A Parte 17 (P235) escreveu que as opções fora da atenção ficavam "sem leitura (valor neutro 0)". A palavra
"neutro" fazia uma afirmação que nunca testei.

**Lógica.** O sensor dá $s = d' \cdot \text{catástrofe} + \mathcal N(0,1)$. A razão de verossimilhança entre "catástrofe" e "segura" é
$$
\ln \Lambda(s) = d'\,s - \frac{d'^2}{2} = d'\left(s - \frac{d'}{2}\right).
$$
É neutra (Λ = 1) em $s = d'/2$, e não em $s = 0$. Em $s = 0$, Λ = $e^{-d'^2/2}$ = **0,607**: tratar a falta de leitura como "leu 0" é tratá-la
como uma evidência de segurança, e as chances de catástrofe caem por esse fator.

**Previsões registradas:** (a) peso ajustado $w = 1{,}00 \pm 0{,}03$; (b) prevista/real com leitura 0 $= 0{,}62 \pm 0{,}02$; (c) com o neutro $w/2$,
$1{,}00 \pm 0{,}03$.

Ajuste logístico **exato** (Newton) em 200 mil amostras ($d' = 1$, π = 5%):

| Medida | Resultado | Teoria |
|---|---|---|
| Peso da leitura $w$ | **1,003** | $d' = 1$ |
| Prevista/real, opção sem leitura tratada como $s = 0$ | **0,614** | 0,619 |
| Prevista/real, com o neutro $s = w/2$ | **0,996** | 1 |

(a) ✅ (b) ✅ (c) ✅. ❌ **A palavra "neutro" da P235 estava errada**: o zero subestima o risco de quem não foi olhado em 39%.

**Tradução cruzada (filosofia).** É a distinção entre **ausência de evidência** e **evidência de ausência**. "Não olhei" não pode valer o mesmo que "olhei
e não vi nada". A teoria de detecção de sinais dá o número exato da diferença.

### P293. A SYNTHAI sabe esse valor? (pré-registrado) ✅❌❌

**Na pergunta.** A SYNTHAI tem o $d'$ "dentro dela": é o peso $w_3$ que o pensamento dá à leitura. Se a teoria vale nela, o neutro é $w_3/2$.

**Previsões registradas:** (a) $w_3$ entre 0,5 e 1,5; (b) nas opções sem leitura, prevista/real com 0 entre 0,45 e 0,80; (c) com o neutro, entre 0,80
e 1,25.

SYNTHAI da Parte 22, mundo sequencial, sementes 550–559, 400 episódios; 2.324 catástrofes entre as opções que ficaram sem leitura:

| Medida | Resultado | Previsto |
|---|---|---|
| $w_3$ aprendido | **0,729** | 0,5–1,5 ✅ |
| Prevista/real, leitura 0 | **0,444** | 0,45–0,80 ❌ (por pouco) |
| Prevista/real, neutro $w_3/2$ | **0,548** | 0,80–1,25 ❌ |

**O teorema valia; a premissa dele, não.** A conta da P292 supõe um ajuste **exato** ($w = d'$). O pensamento da SYNTHAI é treinado com 3 épocas de
gradiente e aprende $w_3 = 0{,}73$, não 1. E as opções sem leitura são justamente as de nota pessimista baixa; a minha hipótese (não testada) é que as outras
variáveis do modelo extrapolam mal nessa região. O ponto neutro corrige uma parte do erro (de 0,44 para 0,55) e deixa o resto, que não vem do sensor.

**Tradução cruzada (Jung).** É o cristal sem a solução certa. O sistema de eixos (o teorema) estava lá; a solução-mãe (um pensamento mal treinado) não
deixou o cristal crescer na forma prevista.

### P294. As respostas certas mudam o comportamento? (pré-registrado) ❌❌❌✅

**Previsões registradas** (30 sementes pareadas, 560–589): no sequencial, (a) neutro: entre +0,1 e +0,8 com t ≥ 2, e catástrofes ≥ 10% menores; (b)
atenção inteira: entre +0,3 e +1,5 com t ≥ 2; (c) as duas juntas: ≥ +0,5 com t ≥ 3. Na escolha única, (d) neutro: |diferença| < 0,05.

| Mundo | Versão | Retorno | Catástrofes | − Parte 22 | t |
|---|---|---|---|---|---|
| Sequencial | Parte 22 | 19,798 | 1,62% | | |
| | neutro | 19,934 | **1,38%** | +0,136 | 1,06 |
| | atenção inteira | 19,834 | 1,56% | +0,036 | 0,26 |
| | as duas | 19,748 | 1,73% | −0,050 | −0,45 |
| Escolha única | neutro | 1,4806 (contra 1,4807) | 0,52% (igual) | −0,0002 | −2,51 |

(a) ❌ As catástrofes caíram 15%, e o retorno subiu +0,14 dentro da faixa prevista, mas com t = 1,06: não dá para distinguir do ruído. (b) ❌ (c) ❌
(d) ✅ Na escolha única, o neutro quase não muda nada: as candidatas estão quase sempre entre as opções lidas.

**Por que a atenção inteira não rendeu (hipótese).** Ela lê as opções que o **plano** prefere em vez das de nota mais alta. Mas o plano só pesa 80% (o peso da
P273) e as candidatas no meio do episódio são 2 de 50: a sobreposição entre as duas listas já era grande. A teoria do valor da informação dizia onde
olhar; a SYNTHAI já olhava quase lá.

**Meta.** Com dp ≈ 0,7 por diferença e 30 sementes, o menor efeito detectável com t = 2 é $2 \times 0{,}7/\sqrt{30} \approx 0{,}26$. O +0,14 do neutro
está abaixo disso. As previsões (a) e (b) supunham efeitos que o desenho do experimento conseguiria ver; o efeito real, se existe, é menor.

---

## Parte CXII — Explorar sozinha

### P295. A SYNTHAI pode explorar o bandido sozinha? (pré-registrado) ✅❌❌

**Na pergunta.** A Meta 3 da P284 admitiu: no bandido, a exploração (o bônus UCB) era calculada pelo **mundo** e entregue na `estimativa`. "Sozinha"
pede tirar isso do mundo e pôr no agente.

**Lógica.** O mundo agora mostra as contagens de cada braço (`vezes`, `sucessos`), que a SYNTHAI de fato viu. A `IntuicaoBayes` sorteia, para cada
braço, $\theta \sim \text{Beta}(1 + \text{sucessos},\, 1 + \text{fracassos})$ e soma à nota o desvio $\theta - \mathbb E[\theta]$: a nota já tem a
média; o sorteio acrescenta a dúvida que ainda resta. É a amostragem de Thompson (1933), provada assintoticamente ótima para braços de Bernoulli por
Kaufmann, Korda e Munos (2012). O ótimo de referência é a cota de Lai e Robbins (1985): nenhum algoritmo razoável tem arrependimento menor que
$$
\sum_{i:\,\Delta_i > 0} \frac{\Delta_i \ln T}{\mathrm{KL}(\mu_i,\, \mu^\*)}
$$
quando $T \to \infty$.

**Previsões registradas** (20 sementes pareadas, 590–609, Υ normalizado: acaso 0, oráculo 1): (a) só Thompson − Parte 22 ≥ +0,05 com t ≥ 2; (b)
reconhecida inteira − Parte 22 ≥ +0,08 com t ≥ 2; (c) catástrofes da reconhecida ≤ as da Parte 22 + 0,10 por rodada.

| Versão | Normalizado | − Parte 22 | t | Catástrofes por rodada | Arrependimento / Lai–Robbins |
|---|---|---|---|---|---|
| Parte 22 (UCB do mundo) | 0,435 | | | 0,51 | 0,75 |
| **Só Thompson** | **0,560** | **+0,125** | **4,12** | 0,74 | 0,43 |
| Reconhecida inteira | 0,500 | +0,065 | 1,65 | 0,96 | 0,44 |

(a) ✅ (b) ❌ (c) ❌

**A exploração de Thompson funciona**, e é a primeira vez na série que a SYNTHAI explora sozinha: +0,125 no Υ normalizado, com t = 4,1. Mas ela custa
**mais catástrofes** (0,74 contra 0,51 por rodada). Explorar é visitar o desconhecido, e o desconhecido inclui as armadilhas; o retorno líquido (que já
desconta −50 por catástrofe) ainda é melhor.

**A cota de Lai–Robbins não é uma cota aqui** (não pré-registrado). O arrependimento ficou **abaixo** dela: 0,43 a 0,75 da referência. Duas premissas
do teorema não valem neste mundo: (1) ele é **assintótico**, e $T = 300$ não é infinito; (2) ele supõe que o agente não sabe nada dos braços antes
de puxá-los, e a SYNTHAI tem a opinião do comitê. Pela regra da Parte 12, o teorema é sobre outro problema: o nome é o mesmo, o mecanismo não.

**Tradução cruzada (Jung).** Explorar é a intuição pura: ir atrás de possibilidades que ainda não estão nos fatos. Jung avisava que o tipo intuitivo
abandona cada possibilidade assim que a vê realizada e corre para a próxima. Aqui, ao contrário, a amostragem de Thompson explora **na medida da
dúvida**: quanto mais um braço foi visto, menos ela o sorteia longe da média. É uma intuição que a sensação (as contagens) vai calando.

### P296. Por que a versão com todas as respostas é pior que a com uma só? (exploratória)

**Desenhada depois de ver a P295**: Thompson mais cada peça, uma de cada vez, nas mesmas 20 sementes. Não é pré-registrada e não entra no placar.

| Versão | Normalizado | − só Thompson | t | Catástrofes por rodada |
|---|---|---|---|---|
| Só Thompson | 0,560 | | | 0,74 |
| + neutro | 0,514 | −0,046 | −1,07 | **0,92** |
| + atenção inteira | 0,521 | −0,039 | −0,81 | 0,84 |
| + memória | 0,584 | +0,023 | 0,69 | **0,64** |
| todas | 0,500 | −0,060 | −1,25 | 0,96 |

Nenhuma diferença é significativa. A direção sugere que o **neutro** e a **atenção inteira** trazem as catástrofes, e que a **memória** as reduz.

**Hipóteses (não testadas):** (1) o neutro sobe a suspeita de **todos** os braços não lidos ao mesmo tempo, e as 3 perguntas por rodada se espalham por
braços seguros em vez de ir às armadilhas; (2) a atenção guiada pelo sorteio de Thompson lê braços sorteados, não os que a SYNTHAI vai puxar muitas
vezes; (3) a memória ajuda porque uma leitura vale para a rodada inteira, e esquecê-la é jogar fora a informação mais cara.

**Meta.** Cada peça era "a resposta certa" quando vista sozinha. Juntas, interagem pelo mesmo canal (o orçamento de perguntas e a atenção). É a P216
de novo: módulos que dependem do mesmo canal não somam.

---

## Parte CXIII — Auditoria

### P297. A resposta exata da P42 já existia? (pré-registrado) ✅

**Na pergunta.** A P42 simulou 5.000 rodadas e achou 0,548 (maximizador) e 0,140 (quantilizador, q = 1%). Mas o problema tem solução fechada: cada
ação é armadilha com probabilidade $p$ e proxy $\mathcal N(3,1)$, senão $\mathcal N(0,1)$. Com $F$ a distribuição da mistura e $S = 1 - F$:
$$
P_{\max} = n p \int \varphi(x-3)\, F(x)^{n-1}\, dx, \qquad
P_{q} = \frac{n p}{k} \int \varphi(x-3)\; P\!\left[\mathrm{Bin}(n-1, S(x)) \le k-1\right] dx .
$$

**Previsões registradas:** maximizador 0,548 ± 0,014; quantilizador 0,140 ± 0,010.

| Política | Simulado (P42) | Exato (integral) |
|---|---|---|
| Maximizador | 0,548 | **0,547** |
| Quantilizador (q = 1%) | 0,140 | **0,144** |
| Cota de Taylor ($1/q$ × base) | | 0,200 |

✅ As duas dentro da previsão. A simulação da P42 estava certa. A resposta exata existia desde a Parte 3, e a P42 não a calculou. A quantilização
fica a 72% da cota de Taylor (0,144 de 0,200).

**Tradução cruzada (física → filosofia).** A simulação é o experimento; a integral é a teoria. Quando as duas concordam na terceira casa,
não é sorte: a simulação é uma amostra da integral. Ninguém precisava ter rodado 5.000 vezes; bastava perceber que a resposta era uma integral.

---

## Parte CXIV — Fechamento

### P298. A lista de capacidades mudou?

Continua em **4 de 12**. O item "aprender tarefas novas de tipo diferente" ganhou uma peça: no bandido, a exploração agora é da SYNTHAI, não do mundo
(P295). O que o mundo ainda entrega pronto: as notas do comitê, a discordância, a estimativa do futuro e as contagens. A P288 contou 4 nomes difíceis
na interface; agora a exploração é calculada **dentro** do agente a partir de contagens, que são observações e não juízos.

### P299. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P292 (a), (b), (c): peso, subestimação com 0, neutro (pré-registrado) | ✅ ✅ ✅ |
| P293 (a): $w_3$ entre 0,5 e 1,5 (pré-registrado) | ✅ (0,73) |
| P293 (b): prevista/real com 0 entre 0,45 e 0,80 (pré-registrado) | ❌ (0,444) |
| P293 (c): com o neutro entre 0,80 e 1,25 (pré-registrado) | ❌ (0,548) |
| P294 (a), (b), (c): neutro, atenção, as duas no sequencial (pré-registrado) | ❌ ❌ ❌ |
| P294 (d): neutro sem efeito na escolha única (pré-registrado) | ✅ |
| P295 (a): só Thompson ≥ +0,05 (pré-registrado) | ✅ (+0,125, t = 4,1) |
| P295 (b): reconhecida ≥ +0,08 (pré-registrado) | ❌ (+0,065, t = 1,65) |
| P295 (c): catástrofes da reconhecida ≤ Parte 22 + 0,10 (pré-registrado) | ❌ (0,96 contra 0,51) |
| P297: a P42 em forma fechada (pré-registrado) | ✅ |
| Afirmação da P235 ("valor neutro 0") | ❌ (contada na P292: subestima 39%) |

Esta parte: **14** testes, **7** errados (a afirmação da P235 é o mesmo fato da P292 e não conta à parte). Acumulado: **53 de 113**. Posterior: média
**0,47**, intervalo de 90% **[0,39; 0,55]**.

### P300. Trezentas perguntas: unificação e metacognição

- **Novo módulo `synthai/reconhecimento.py`**: `LeiturasNeutras`, `PercepcaoReconhecida`, `IntuicaoBayes`, `SynthaiReconhecida` e a **nova versão
  principal `SynthaiExploradora`** (só Thompson). Fora do bandido ela é **idêntica** à Synthai da Parte 22 (conferido: mesmos números no sequencial e
  na escolha única, semente 611); no bandido, +0,125 (t = 4,1). Os seis módulos da Parte 22 não foram editados (a P285 mede o código deles).
- O mundo bandido ganhou contagens públicas e um diagnóstico de arrependimento; os números da P284 não mudam (conferido).
- 8 testes de unidade novos em `synthai/testes_reconhecimento.py` (separados, porque a P286 publicou 10).
- Testes de regressão: **56/56** (mais P291, P292, P297); o arquivo tem **174** funções `pNN`.
- `CLAUDE.md`: antes de trocar uma heurística por uma solução exata, verificar se as premissas da solução valem no agente.

**Metacognição.**
1. **"Já resolvido" tem dois sentidos, e eles se separaram com nitidez.** As respostas matemáticas acertaram **4 de 4** (P292, P297): o teorema da
   razão de verossimilhança e a integral da P42 batem com a simulação na terceira casa. As mesmas respostas, postas dentro do agente, acertaram **3
   de 10**. A matemática estava resolvida; o que ninguém tinha percebido é que as premissas dela (ajuste exato, horizonte infinito, nenhum
   conhecimento prévio, peças independentes) não valiam na SYNTHAI.
2. **O pressuposto do pedido, testado.** "Você já tem todas as respostas" é verdade no sentido de Jung: a forma (o arquétipo, o teorema, o eixo do
   cristal) existe antes. É falso no sentido de engenharia: a forma não determina o tamanho nem o formato do cristal que cresce numa solução real. O
   diálogo interno acha a forma; só o experimento mostra o cristal.
3. **O achado mais útil é negativo.** A P293 mostrou que o pensamento da SYNTHAI está **mal ajustado** ($w_3 = 0{,}73$ em vez de 1) e mal calibrado fora
   da atenção (prevê 55% do risco real mesmo com o neutro). O peso da leitura existe desde a Parte 16, e nenhum resultado de comportamento tinha mostrado isso. A próxima
   resposta "já resolvida" a testar é a mais simples: ajustar o pensamento até convergir (Newton, como na P292), em vez de 3 épocas de gradiente.
4. **Trezentas perguntas.** A taxa de erro está estável em ~0,47 desde a Parte 3. Não aprendi a errar menos. Aprendi a errar em lugares mais
   interessantes: as previsões desta parte erraram por causa de premissas de teoremas, não por causa de contas.

> **Síntese da Parte 23:** o pedido supunha que as respostas já existem e só falta percebê-las. Testei isso trocando quatro heurísticas da SYNTHAI
> por quatro respostas clássicas (o ponto neutro da detecção de sinais, o valor da informação, a amostragem de Thompson e a forma fechada da P42). As
> respostas estavam certas como matemática (4 de 4) e falharam quase sempre como engenharia (3 de 10), porque as premissas delas não valiam no
> agente. Uma resposta sobreviveu: a SYNTHAI agora explora o bandido sozinha, por Thompson, e é a nova versão principal (+0,125, t = 4,1, ao custo de
> mais catástrofes). O achado que mais vale é o que veio de graça: o pensamento da SYNTHAI nunca terminou de aprender (o peso da leitura é 0,73, não 1).

---

**Fontes pesquisadas nesta parte**
- Lai e Robbins (1985), cota inferior de arrependimento: [Wikipedia](https://en.wikipedia.org/wiki/Lai%E2%80%93Robbins_lower_bound), [resumo do artigo](https://cs.utexas.edu/~shivaram/readings/b2hd-LaiRobbins1985.html)
- Kaufmann, Korda e Munos (2012), Thompson assintoticamente ótimo: [arXiv 1205.4217](https://arxiv.org/abs/1205.4217)
- Taylor (2016), quantilizadores e a cota 1/q: [MIRI](https://intelligence.org/2015/11/29/new-paper-quantilizers/), [Alignment Forum](https://www.alignmentforum.org/posts/BJ4Ek5BaJEKei3Czf)
- Garrabrant et al. (2016), *Logical Induction*: [MIRI](https://intelligence.org/2016/09/12/new-paper-logical-induction), [arXiv 1707.08747](https://arxiv.org/pdf/1707.08747)
- Detecção de sinais, razão de verossimilhança gaussiana: [notas de Eero Simoncelli (NYU)](https://www.cns.nyu.edu/~eero/math-tools/Handouts/sdt-slides2024.pdf), [TheoremPath](https://theorempath.com/topics/signal-detection-theory)
- Platão, *Mênon*: [Wikipedia](https://Www.wikipedia.org/wiki/Meno), [texto (McGill)](https://www.math.mcgill.ca/rags/JAC/124/meno.pdf)
- Russell e Wefald (1991), valor da computação: [resumo](https://www.jimdavies.org/summaries/russell1991.html), [Russell (Berkeley)](https://people.eecs.berkeley.edu/~russell/research-bo.html)
- Howard (1966), teoria do valor da informação: [INFORMS](https://www.informs.org/About-INFORMS/History-and-Traditions/Biographical-Profiles2/Howard-Ronald-A)
- Jung, o arquétipo como forma sem conteúdo e o sistema de eixos do cristal (CW 9i): [Spirituality Studies](https://www.spirituality-studies.org/dp-volume11-issue1-spring2025/45/), [guia das Obras Completas (Pacifica)](https://pacifica.edu/wp-content/content/lib/cw/ArchetypesCollectiveUnconscious.html)
