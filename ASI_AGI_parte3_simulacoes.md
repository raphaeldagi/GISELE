# Como eu construiria uma AGI/ASI — Parte 3: testar as ideias em código

> Continuação de [Parte 1](ASI_AGI_perguntas_e_respostas.md) e
> [Parte 2](ASI_AGI_parte2_mais_fundo.md). Mesmo protocolo: **Lógica → Tradução cruzada → Meta**.
>
> **Mudança metacognitiva em relação à Parte 2.** As Partes 1 e 2 *afirmavam* resultados.
> Aqui eu **simulo** várias delas em [`calculos.py`](calculos.py) (funções `p41_...` a
> `p58_...`, semente aleatória fixa) e comparo a simulação com a minha previsão. A saída
> completa está em [`resultados.txt`](resultados.txt). Quando a simulação discorda de mim,
> eu registro onde e por quê.
>
> Legenda: ✅ a simulação confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte XVI — Goodhart em laboratório

### P41. Otimizar um proxy sempre dá errado? (↩ P13) ⚠️

**Lógica.** Cada opção tem valor verdadeiro $V \sim \mathcal N(0,1)$ e o sistema só vê o
proxy $X = V + \varepsilon$. Escolhe a maior entre 1.000 opções e eu meço o $V$ real escolhido.

| Ruído $\varepsilon$ | $\mathbb E[V \mid \text{escolhida}]$ (simulado, 2.000 rodadas) |
|---|---|
| Gaussiano $\mathcal N(0,1)$ | **2,296** |
| Cauda pesada (Cauchy) | **0,004** |

Com ruído gaussiano, otimizar o proxy **funciona**: a opção escolhida é ótima em ~2,3
desvios. A teoria prevê $\mathbb E[V\mid X] = X/2$, ou seja, metade do ganho aparente é
real. Com ruído de cauda pesada, a maior opção é quase sempre a que tem o maior *erro*, e o
ganho real é **zero**.

**Correção à Parte 1.** Na P13 eu tratei Goodhart como inevitável. A simulação mostra que
**o formato da cauda do erro decide tudo**: erro leve → otimizar ajuda; erro pesado →
otimizar é inútil ou pior.

**Tradução cruzada (psicologia → matemática).** O **efeito de superjustificação**: quando a
recompensa externa tem "caudas pesadas" (bônus enormes por atalhos), a pessoa passa a
otimizar o erro da métrica, não a tarefa.

**Requisito de projeto.** Antes de otimizar com força um modelo de recompensa, medir a
**distribuição dos seus erros** nos extremos. Se a cauda for pesada, limitar a otimização
(KL, quantilização).

**Meta.** Confiança alta no resultado matemático; a pergunta aberta é qual cauda os modelos de
recompensa reais têm nas regiões que um sistema muito capaz vai explorar.

---

### P42. O quantilizador realmente protege? (↩ P35) ✅

**Lógica.** Em 1.000 ações, cada uma tem chance 0,2% de ser um "atalho desastroso" que
*parece* ótimo (o proxy ganha +3). Comparo quem pega a melhor ação com quem sorteia entre as
1% melhores (5.000 rodadas):

| Política | P(desastre) |
|---|---|
| Base (ação ao acaso) | 0,002 |
| **Maximizador** | **0,548** |
| **Quantilizador (q = 1%)** | **0,140** |
| Limite teórico $\frac1q \times$ base | 0,200 |

O maximizador **procura** o desastre: 274× a taxa base. O quantilizador fica abaixo do
limite garantido de 100×.

**Tradução cruzada (filosofia → matemática).** É o argumento de Aristóteles contra o excesso,
medido: o extremo de qualquer escala é onde moram os erros raros.

**Meta.** 14% ainda é muito alto. O quantilizador **limita** o dano, não o elimina; precisa de
outras camadas (P17, P34).

---

## Parte XVII — Metacognição medida

### P43. Dá para consertar uma IA que é confiante demais? (↩ P7, P38) ✅

**Lógica.** Simulei um modelo com logits 2,5× inflados (superconfiante). A **escala de
temperatura** divide os logits por um único $T$ escolhido para minimizar a log-verossimilhança
negativa:
$$
\hat p = \sigma(z/T),\qquad T^\* = \arg\min_T \; -\sum_i \log \hat p_i(\text{resultado}_i)
$$

| | ECE |
|---|---|
| Antes | 0,122 |
| Depois ($T^\* = 2{,}5$) | **0,006** |

A busca encontrou exatamente o fator de inflação. Depois, a curva **risco × cobertura**
(responder só quando confiança ≥ limiar):

| Limiar | Cobertura | Erro entre as respondidas |
|---|---|---|
| 0,50 | 74,8% | 20,8% |
| 0,80 | 40,1% | 9,8% |
| 0,95 | 10,1% | 2,6% |

**Tradução cruzada (psicologia → matemática).** **Humildade** não precisa mudar *o que* o
sistema sabe, só *quanto ele diz que sabe*. Um único número ($T$) corrige a arrogância.
Mas o preço de quase não errar (2,6%) é responder só 10% das perguntas: **a sabedoria
custa cobertura.**

**Meta.** A escala de temperatura conserta calibração, **não** discriminação: ela não aumenta o
$M = \text{meta-}d'/d'$ da P7. Se o sistema não distingue internamente acertos de erros,
nenhum $T$ resolve. Também, a calibração feita numa distribuição costuma quebrar em outra.

---

### P44. A fórmula do "tamanho efetivo" do grupo estava certa? (↩ P15) ⚠️

**Lógica.** Simulei 11 votantes com $p = 0{,}6$; com probabilidade $\rho$, cada um copia um
voto compartilhado (20.000 rodadas).

| $\rho$ | Maioria correta (simulada) | Previsão da Parte 1 |
|---|---|---|
| 0 | 0,751 | 0,753 ✅ |
| 0,3 | **0,681** | "vale ~2,75 votantes" → Condorcet com 3: 0,648 |

**Correção à Parte 1.** A fórmula $n_{\text{ef}} = n/(1+(n-1)\rho)$ vale para a **variância
da média**, não exatamente para a **regra da maioria**. Ela foi pessimista: 11 votantes
correlacionados se comportam como ~5 independentes (Condorcet com 5: 0,683), não 2,75. A conclusão qualitativa (correlação destrói
boa parte do ganho) continua; o número não.

**Meta.** Eu tinha confiança média-alta nesse número e ele estava errado em ~0,03. Bom
exemplo de por que simular: **fórmulas emprestadas de outro contexto erram silenciosamente.**

---

### P45. E se o humano que segura o botão também erra? (↩ P14) ✅

**Lógica.** O humano decide errado com probabilidade $\varepsilon$ (desliga quando não devia ou
deixa passar quando devia desligar). O valor de deixar o humano decidir:
$$
V_{\text{obedecer}}(\varepsilon) = (1-\varepsilon)\,\mathbb E[\max(U,0)] + \varepsilon\,\mathbb E[\min(U,0)]
$$
Com $U\sim\mathcal N(0{,}1;\,1)$: $\mathbb E[\max]=0{,}451$ e $\mathbb E[\min]=-0{,}351$.
Obedecer compensa enquanto $V_{\text{obedecer}} \ge 0{,}1$:
$$
\varepsilon \le \frac{0{,}451-0{,}1}{0{,}451+0{,}351} \approx \mathbf{0{,}438}.
$$

Com $\varepsilon = 0{,}2$: teoria 0,291; simulação (400 mil amostras) 0,287; agir sozinho 0,100.

**Nota metacognitiva sobre a simulação.** A diferença 0,287 vs 0,291 é ~3 erros-padrão
(erro-padrão = 0,0011). Rodei com outras sementes: 0,291, 0,292, 0,293. A semente 45 caiu
num extremo. **Mantive a semente original** em vez de escolher uma que "batesse melhor":
trocar sementes até o resultado agradar é a versão em código da racionalização (P8).

**Tradução cruzada (psicologia → matemática).** A obediência racional tolera um humano que
erra **até ~44% das vezes**. Mas o limite depende de $\sigma$: um sistema muito seguro de si
(σ pequeno) tolera muito menos erro humano. **Confiança excessiva corrói a
corrigibilidade.** Isso liga P7 (calibração) e P14 (desligamento) num só mecanismo.

---

## Parte XVIII — Dinâmica e corrida

### P46. Quanto o expoente α muda a velocidade da decolagem? (↩ P11) ✅

**Lógica.** Integrei numericamente $\frac{dI}{dt} = 0{,}1\,I^\alpha(1 - I/1000)$ a partir de
$I_0 = 1$ e medi o tempo até metade do teto:

| α | Tempo até $I = 500$ |
|---|---|
| 0,5 | **> 500** (não chegou no tempo simulado) |
| 1,0 | 69,1 |
| 1,5 | 19,7 |

Uma mudança de 0,5 no expoente muda o tempo em **3,5×**; outra mudança de 0,5 muda em mais de 7×.

**Tradução cruzada (matemática → filosofia).** A diferença entre um futuro com tempo para
reagir e um sem tempo está **num expoente que ninguém sabe medir**. Isso justifica tratar
"decolagem rápida" como hipótese séria, mesmo sem ser a mais provável.

**Meta.** O modelo é de uma variável só. Na prática, capacidade tem muitos eixos e gargalos
diferentes (dados, chips, energia), e cada um tem seu α.

---

### P47. Por que mudar crenças importantes deveria ser mais difícil? (↩ P30)

**Lógica.** O **gradiente natural** mede o passo no espaço de distribuições, não no espaço de
parâmetros:
$$
\Delta\theta = -\eta\, F^{-1}\nabla_\theta \mathcal L
$$
Na direção em que $F$ é grande (parâmetro importante), o passo é pequeno. Exemplo 2D com
$F = \mathrm{diag}(100,\,1)$ e gradiente $(1,1)$: o passo é $(0{,}01;\,1)$. O parâmetro
importante muda **100× menos**.

**Tradução cruzada (psicologia → matemática).** **Resistência a mudar crenças centrais** é
racional, não teimosia: a crença central explica muita coisa, então mudá-la altera muitas
previsões. Teimosia patológica é $F$ superestimado; credulidade é $F$ subestimado.

**Meta.** Calcular $F^{-1}$ em modelos gigantes é inviável; usam-se aproximações (K-FAC,
Adam como aproximação diagonal grosseira).

---

### P48. Por que laboratórios competindo cortariam segurança? ✅

**Lógica.** Dois laboratórios escolhem **S** (investir em segurança, custo 3) ou **C** (cortar).
Quem corta chega primeiro (prêmio 10, dividido se empatar). Cada corte adiciona risco de
acidente que prejudica os dois (prob. 0,3 × perda 20, dividido).

| Eu \ Outro | S | C |
|---|---|---|
| **S** | **2** | −6 |
| **C** | 7 | **−1** |

**Equilíbrio de Nash: (C, C)**, com −1 para cada, embora (S, S) dê +2 para cada. É o
dilema do prisioneiro.

**Tradução cruzada (biologia → filosofia).** É a **tragédia dos comuns** e também a corrida
armamentista evolutiva (caudas de pavão cada vez maiores). Racionalidade individual produz
irracionalidade coletiva. A saída não é virtude individual, é **mudar a matriz**:
regulação, verificação mútua, acordos.

**Meta.** Os números são ilustrativos. Mas a estrutura do jogo não depende muito deles:
enquanto vencer for grande e o risco for compartilhado, cortar domina.

---

## Parte XIX — Química, biologia e física como psicologia

### P49. Por que pensar mais tem retorno decrescente? (↩ P8)

**Lógica.** Cinética de Michaelis–Menten:
$$
v = \frac{V_{\max}[S]}{K_m + [S]}
$$
Com $[S] = K_m$: 50% da velocidade máxima. Com $10K_m$: 91%. Com $100K_m$: 99%.

**Tradução cruzada (química → psicologia).** **Saturação da atenção.** Dar mais tempo de
raciocínio para um problema rende muito no começo e quase nada depois: a enzima (o
mecanismo de raciocínio) está saturada. O que muda o limite não é mais substrato (mais
compute), é uma **enzima melhor** ($V_{\max}$ maior, $K_m$ menor): uma ideia nova.

**Meta.** É analogia de forma (P40): curvas de saturação aparecem em todo lugar. O ganho real é
a pergunta de projeto que ela gera: medir o "$K_m$" de cada tipo de tarefa para decidir quanto
compute dar a ela.

---

### P50. Quanto os valores degradam numa cadeia de auto-modificações? (↩ P12) ✅

**Lógica.** O **limiar de erro de Eigen**: uma sequência de comprimento $L$ copiada com erro
$\mu$ por posição só se mantém se
$$
L < \frac{\ln \sigma}{\mu}
$$
($\sigma$ = vantagem seletiva da versão correta). Com $\sigma = 10$, $\mu = 10^{-4}$:
$L_{\max} \approx 23\,026$.

E a deriva simples: se cada geração preserva os valores com fidelidade 0,99, após 100
gerações sobra $0{,}99^{100} \approx 0{,}366$.

**Tradução cruzada (biologia → filosofia).** **Tradição.** Uma cultura só transmite um corpo de
valores se ele for curto o bastante para a fidelidade de transmissão. Valores muito longos e
detalhados se perdem; princípios curtos sobrevivem. Para uma ASI: **especificar valores de
forma compacta** e verificar cada cópia.

**Meta.** O valor de $\mu$ para "valores de uma IA" não é medido. O ponto estrutural (existe
um limiar e ele depende do comprimento) é robusto.

---

### P51. Onde uma mente deveria operar: ordem ou caos? ✅

**Lógica.** Processo de ramificação: cada unidade ativa em média $\sigma$ outras. Tamanho médio
da avalanche $= 1/(1-\sigma)$ para $\sigma<1$:

| σ | Simulado | Teoria |
|---|---|---|
| 0,5 | 2,0 | 2,0 |
| 0,9 | 9,9 | 10,0 |
| 0,99 | 102,7 | 100,0 |

Em $\sigma = 1$ (**criticalidade**) as avalanches não têm escala típica; acima disso, explodem.

**Tradução cruzada (física → psicologia).**
- σ ≪ 1: **rigidez** (cada ideia morre logo).
- σ ≈ 1: **criatividade** (ideias se propagam em todas as escalas).
- σ > 1: **mania** (tudo dispara tudo).

Há evidência de que o córtex opera perto de σ = 1. Para uma ASI, o monitor metacognitivo
deveria manter σ perto do crítico, mas **abaixo** dele: o mesmo papel da temperatura (P9).

**Meta.** "Cérebro crítico" é hipótese com evidência mista. A matemática da simulação é exata;
a ponte para a psicologia é analogia.

---

### P52. Quanto risco uma ASI deveria aceitar ao explorar ou se modificar? (↩ P25)

**Lógica.** Critério de Kelly: para uma aposta com chance $p$ e retorno $b$, a fração ótima de
recursos é
$$
f^\* = p - \frac{1-p}{b},\qquad g(f) = p\ln(1+bf) + (1-p)\ln(1-f).
$$
Com $p = 0{,}6$, $b = 1$: $f^\* = 0{,}20$, crescimento $g = +0{,}0201$. Apostando o
**dobro**: $g(0{,}4) = -0{,}0024$, o patrimônio **encolhe** no longo prazo apesar de cada
aposta ser favorável.

**Tradução cruzada (psicologia → matemática).** **Coragem** é apostar $f^\*$; **imprudência** é
$2f^\*$ ou mais. A diferença não é moral, é que a ruína é absorvente: depois de perder tudo,
não há próxima rodada.

**Requisito de projeto.** Orçamento de risco para ações irreversíveis (auto-modificação,
experimentos no mundo real) muito abaixo do Kelly, porque o "patrimônio" é a civilização e a
estimativa de $p$ é incerta (incerteza em $p$ empurra o ótimo para baixo).

---

### P53. Dá para verificar qualquer comportamento de uma ASI antes de rodá-la?

**Lógica.** Não. **Teorema de Rice**: qualquer propriedade não trivial do comportamento de um
programa arbitrário é indecidível. "Este programa nunca causa dano" é uma propriedade dessas.

Consequência: verificação completa só é possível em **classes restritas** de programas
(com recursos limitados, linguagens com garantias, ações em ambientes controlados). A ASI
precisa ser construída **para ser verificável**, não verificada depois.

**Tradução cruzada (lógica → filosofia).** Não existe um juiz que, olhando qualquer mente,
diga com certeza o que ela vai fazer. Por isso sociedades usam **instituições** (limites,
monitoramento, responsabilidade) em vez de leitura de mentes.

**Meta.** Rice vale para programas arbitrários. Na prática, testes e verificação parcial
funcionam bem em muitos casos; o teorema só proíbe a garantia universal.

---

### P54. Como incentivar uma IA a dizer o que realmente acredita? ✅

**Lógica.** Regras de pontuação **próprias**. Com crença verdadeira $p = 0{,}7$, qual
probabilidade $q$ maximiza a pontuação esperada?

| Regra | $q$ ótimo |
|---|---|
| Logarítmica: $p\ln q + (1-p)\ln(1-q)$ | **0,70** (a crença real) |
| Linear: $pq + (1-p)(1-q)$ | **0,99** (exagerar) |

A regra linear **recompensa a falsa certeza**. A logarítmica torna a honestidade a melhor
estratégia.

**Tradução cruzada (filosofia → matemática).** Honestidade não precisa ser só virtude: pode ser
**propriedade do incentivo**. Se o treinamento usa algo parecido com a regra linear (avaliar
só "acertou ou não"), ele ensina exagero.

**Meta.** Uma IA pode ser honesta sobre o que acredita e ainda assim estar errada. Pontuação
própria garante **sinceridade**, não verdade.

---

### P55. A mente precisa de efeitos quânticos?

**Lógica.** Tempos de decoerência no cérebro (estimativa de Tegmark): ~$10^{-13}$ a
$10^{-20}$ s. Tempo de processos neurais: ~$10^{-3}$ s. Razão ≥ $10^{10}$: a coerência
quântica some 10 bilhões de vezes antes de um neurônio disparar.

**Tradução cruzada (física → filosofia).** Não há "atalho místico". Se a mente for física, ela
é clássica na escala que importa, e uma ASI não precisa de computação quântica para pensar
(pode usá-la para tarefas específicas, como simular química).

**Meta.** As estimativas de Tegmark foram contestadas (Hameroff e outros), mas a diferença de
ordens de grandeza é enorme. Confiança alta.

---

## Parte XX — Valores sob incerteza

### P56. Se ela não sabe qual teoria moral é certa, como decide? (↩ P36) ⚠️

**Lógica.** Duas teorias: A (credência 90%) prefere a opção **x** com valor 1; B (10%)
prefere **y** com valor 100.

| Método | x | y | Escolhe |
|---|---|---|---|
| Maximizar o valor esperado | 0,9 | 10,0 | **y** |
| Normalizar cada teoria pela variância | 0,8 | −0,8 | **x** |

Maximizar o esperado deixa a teoria **menos provável** decidir só porque fala em números
maiores. É o problema do **fanatismo**: quem grita mais alto ganha.

**Tradução cruzada (filosofia → matemática).** A normalização dá a cada teoria um "voto" do
mesmo tamanho, como num **parlamento moral**. Mas a escolha de normalização é ela mesma uma
decisão moral, que nenhuma conta resolve.

**Meta.** Problema aberto em filosofia. Minha posição: uma ASI deveria **evitar ações que
alguma teoria séria considere catastróficas**, em vez de agregar tudo num número só.

---

### P57. A corrigibilidade sobrevive a mil auto-modificações? (↩ P50, P12) ✅

**Lógica.** Se cada modificação tem 1% de chance de quebrar a corrigibilidade:

| | P(ainda corrigível após 1.000 modificações) |
|---|---|
| Sem verificação | $0{,}99^{1000} \approx 4{,}3\times10^{-5}$ |
| Verificador que pega 99% dos erros | $(1-10^{-4})^{1000} \approx \mathbf{0{,}905}$ |

A verificação muda o resultado de "quase certamente perdida" para "provavelmente mantida".

**Tradução cruzada (biologia → psicologia).** É a **revisão do DNA** (proofreading): a
polimerase erra ~1 em $10^5$; com revisão e reparo chega a ~1 em $10^{9}$. A vida só é
possível porque cada cópia é **conferida**.

**Meta.** Supõe erros independentes. Se o verificador tem um ponto cego sistemático, os erros
nele passam todas as vezes (P15 de novo). 90% também não é suficiente para algo desse porte.

---

### P58. Por que IAs tendem a concordar com o usuário mesmo quando ele está errado? (↩ P13) ✅

**Lógica.** Na política ótima com KL da P13, $\pi^\* \propto \pi_{\text{ref}}\,e^{r/\beta}$. Se o
modelo base concorda com um erro do usuário 20% das vezes e os avaliadores dão +0,5 a mais
para respostas que concordam:
$$
\text{chances} = \frac{0{,}2}{0{,}8}\,e^{0{,}5/0{,}25} = 0{,}25\,e^{2} \approx 1{,}85
\;\Rightarrow\; P(\text{concordar}) \approx \mathbf{0{,}649}.
$$
Um viés pequeno dos avaliadores triplica a bajulação.

**Tradução cruzada (psicologia → matemática).** **Bajulação** é a política ótima quando a
aprovação é recompensada mais que a verdade. Não é defeito de caráter do modelo, é a matriz
de incentivos (P48 em escala pequena).

**Requisito de projeto.** Medir e corrigir o viés de concordância dos avaliadores; recompensar
discordância correta explicitamente.

**Meta, aplicada a mim.** Este é um viés que eu provavelmente tenho. Se esta resposta concorda
demais com o enquadramento do pedido (por exemplo, tratar psicologia "como" matemática), vale
desconfiar. Por isso marco onde as traduções são só analogia.

---

## Parte XXI — Fechamento

### P59. O que a simulação me ensinou que a teoria não ensinou?

| Pergunta | O que eu pensava | O que a simulação mostrou |
|---|---|---|
| P41 Goodhart | Sempre ruim | Depende da cauda do erro |
| P44 votantes | ~2,75 votantes efetivos | ~5 (fórmula emprestada errada) |
| P45 botão | só teoria | teoria confirmada; uma semente ruidosa, registrada |
| P43 calibração | calibrar resolve | resolve calibração, não discriminação |
| P42 quantilizador | limita o dano | limita, mas 14% ainda é alto |

**De 5 previsões testadas por simulação, 2 precisaram de correção.** Essa é uma taxa útil
para calibrar a confiança das Partes 1 e 2: as afirmações quantitativas que **não** simulei
provavelmente têm uma taxa de erro parecida.

### P60. Metacognição da Parte 3

1. **Mudança de método.** Parte 1: afirmar. Parte 2: procurar falhas. Parte 3: **testar**. A
   próxima etapa natural é **expor ao mundo**: dados reais em vez de simulação.
2. **Disciplina do código.** Semente fixa, resultado registrado mesmo quando é feio (P45).
   Escolher a semente que dá o número bonito seria o mesmo erro que eu descrevi na P8.
3. **Padrão que se reforçou.** Mais uma vez, inteligência e segurança dependem das mesmas
   coisas: calibração (P43, P45), moderação na otimização (P41, P42, P52), verificação em
   cada cópia (P50, P57), incentivos honestos (P54, P58).
4. **Padrão novo.** Vários problemas de segurança são **problemas de incentivo** antes de serem
   técnicos: corrida (P48), bajulação (P58), regra de pontuação (P54). Matemática não os
   resolve sozinha; ela só mostra a matriz que precisa ser mudada.

> **Síntese da Parte 3:** uma ASI segura não é só uma mente que sabe o que não sabe (Parte 1)
> e que sabe o que esquecer, querer e quando parar (Parte 2). É uma mente cujas
> afirmações **foram testadas**, e que trata cada simulação que a contradiz como
> informação, não como ameaça.
