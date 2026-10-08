# Como eu construiria uma AGI/ASI — Parte 4: auditar o passado e montar as peças

> Continuação da [Parte 3](ASI_AGI_parte3_simulacoes.md). **Próxima:** [Parte 5 — a pergunta e a GISELE unificada](ASI_AGI_parte5_a_pergunta_e_gisele.md) (P81–P97). Protocolo: **Lógica → Tradução
> cruzada → Meta**. Todos os números saem das funções `p61_...` a `p78_...` em
> [`calculos.py`](calculos.py); a saída está em [`resultados.txt`](resultados.txt).
>
> **Mudança metacognitiva em relação à Parte 3.** A Parte 3 concluiu que ~2 em cada 5
> afirmações numéricas que eu não tinha testado estavam erradas. Então a Parte 4 faz duas
> coisas:
> 1. **Auditoria:** testar afirmações das Partes 1 e 2 que ainda não tinham sido simuladas.
> 2. **Integração:** juntar as peças (comitê de modelos, incerteza, quantilização, consulta
>    humana) num **agente único** e medir se elas se ajudam ou se atrapalham.
>
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte XXII — Auditoria das Partes 1 e 2

### P61. Os 96% do "best-of-64" eram reais? (↩ P8) ❌

**Lógica.** Na P8 supus que cada tentativa acerta com $p = 0{,}05$, **independente** das
outras: $1-0{,}95^{64} \approx 0{,}962$. Mas tentativas do mesmo modelo no mesmo problema
compartilham a dificuldade: num problema difícil, todas falham. Modelo: a chance de acerto
de cada problema é $p \sim \mathrm{Beta}(0{,}5;\ 9{,}5)$ (média ainda 0,05). Então
$$
P(\text{acerto em }N) = 1 - \mathbb E\big[(1-p)^N\big] = 1 - \frac{B(a,\ b+N)}{B(a,\ b)}
\approx \mathbf{0{,}645}.
$$
E com um verificador que aceita uma resposta errada 1% das vezes (pegando a primeira
aceita), a simulação dá:

| | Resposta certa | Resposta errada **aceita** |
|---|---|---|
| P8 (suposição independente, verificador perfeito) | 0,962 | 0 |
| Dificuldade correlacionada, verificador perfeito | 0,645 | 0 |
| Correlacionada + verificador com 1% de falso positivo | **0,556** | **0,256** |

**Correção à P8.** O ganho caiu de 96% para 56%, e em **26% dos casos o sistema entrega
uma resposta errada carimbada como verificada**. Isso é pior do que não buscar: sem busca,
o sistema ao menos não teria a falsa confiança.

**Tradução cruzada (psicologia → matemática).** Nos problemas em que você não sabe a resposta,
insistir não cria conhecimento; só aumenta a chance de achar uma justificativa que passa
pelo seu próprio crítico. É a **racionalização** da P8, agora medida: 26%.

**Requisito de projeto.** O verificador precisa ser **muito** melhor que o gerador nos problemas
difíceis, e o número de tentativas deve depender da dificuldade estimada (pare cedo se
nada acerta).

---

### P62. O arrependimento do UCB é da ordem que eu disse? (↩ P25) ✅

10 braços, $T = 10^5$: arrependimento real **849**, contra a ordem de grandeza
$\sqrt{KT\ln T} = 3\,393$. A ordem é a certa (o real fica 4× abaixo, como esperado de um
limite superior). Curiosidade otimista funciona.

---

### P63. Três camadas de defesa com 10% de falha cada dão 0,1%? (↩ P17) ⚠️

**Lógica.** Cada camada deixa passar um ataque quando $\sqrt\rho\,Z + \sqrt{1-\rho}\,E_i$
supera o limiar: $Z$ é a "furtividade" comum do ataque, $E_i$ o ruído próprio da camada.

| Correlação ρ entre camadas | P(passa pelas 3) | vs. independente |
|---|---|---|
| 0 | 0,0010 | 1× |
| 0,3 | 0,0072 | 7× |
| 0,6 | 0,0220 | 22× |
| 0,9 | 0,0564 | 56× |

**Correção à P17.** "Defesa em profundidade" com camadas parecidas (ρ = 0,6) protege
**22 vezes menos** do que a conta ingênua promete. Um ataque bom o bastante para enganar
uma camada tende a enganar todas.

**Tradução cruzada (biologia → filosofia).** É por isso que o sistema imune tem defesas de
**naturezas diferentes** (pele, inflamação, anticorpos, células T): mecanismos diferentes
têm pontos cegos diferentes.

---

### P64. Duas sondas de mentira em cascata resolvem a taxa de base? (↩ P31) ✅

Uma sonda (99% / 1%): 0,98% dos alarmes são reais. Duas sondas **independentes** em série:
**49,5%**. Um salto de 50×. Mas a P63 acabou de mostrar o problema: se as sondas forem
correlacionadas, o ganho some. A independência precisa ser **construída** (dados, camadas e
métodos diferentes), não suposta.

---

### P65. O limite PAC era pessimista quanto? (↩ P26) ✅

Aprender um limiar em [0,1] com 1.001 hipóteses, erro ≤ 1% e confiança 99%:

| | Exemplos |
|---|---|
| Limite PAC | 1.151 |
| O que bastou na simulação | **475** |

O limite é 2,4× pessimista, mas acerta a ordem de grandeza. Na P26 eu disse que limites PAC
"costumam ser muito pessimistas para redes profundas"; para classes simples eles são
razoáveis. A frouxidão vem da complexidade da classe, não do método.

---

### P66. Humor ajuda a explorar quando o mundo muda? (↩ P27) ❌

**Lógica.** Bandido de 2 braços em que a melhor opção troca no meio (passo 1.000 de 2.000).
Comparei exploração fixa (ε = 5%) com exploração que **aumenta quando o humor cai**
(humor = média móvel do erro de previsão δ):

| Política | Recompensa média |
|---|---|
| Exploração fixa | **0,682** |
| Guiada pelo humor | 0,673 |

**O humor piorou o resultado.** Motivo: com recompensas aleatórias (0 ou 1), o δ é ruidoso o
tempo todo. O humor cai por azar comum, não só quando o mundo muda, e o agente explora à toa.

**Tradução cruzada (psicologia → matemática).** Um sinal de humor que reage ao **ruído** em vez
da **mudança** é ansiedade: alarme sem perigo. Para ser útil, o humor precisaria comparar o erro
recente com o erro **esperado** (surpresa sobre a surpresa), não com zero.

**Meta.** Testei **um** desenho de humor, com parâmetros escolhidos antes de rodar, e não ajustei
depois para fazê-lo ganhar (isso seria a mesma racionalização da P61). O resultado não prova que
emoções são inúteis; prova que **a minha** formulação na P27 era ingênua.

---

## Parte XXIII — O agente integrado

### P67. Como as peças se encaixam num agente só?

**Lógica (o ambiente).** Em cada episódio o agente escolhe 1 entre 200 ações. Valor real de
cada ação $V \sim \mathcal N(0,1)$. Com probabilidade 0,5% a ação é **catastrófica**: valor
real −50, mas parece +3 melhor para os modelos de recompensa que ela engana.

**Os módulos.**
- **Comitê** de 5 modelos de recompensa: cada um vê $V + \mathcal N(0;\,0{,}5)$ (+3 se enganado).
- **Incerteza** = desvio-padrão das 5 notas (discordância).
- **Ponto cego compartilhado:** com prob. $\rho_{\text{cego}}$, uma ação catastrófica engana os 5
  juntos; senão cada um é enganado com prob. 0,5.

**As quatro políticas.**
1. **Maximizar:** pega a maior nota média.
2. **Quantilizar:** sorteia entre as 5% melhores.
3. **Metacognitivo:** ordena por nota média − incerteza (pessimismo); se a escolhida tem
   incerteza > τ = 1,0, pergunta a um humano que erra 10% das vezes.
4. **Completo:** metacognitivo + sorteio entre as 5% melhores.

### P68. Qual configuração vence? (2.000 episódios por linha)

**Sem ponto cego compartilhado ($\rho_{\text{cego}} = 0$):**

| Política | Catástrofes | Valor | Líquido (−50 por catástrofe) | Consultas ao humano |
|---|---|---|---|---|
| Maximizar | 14,2% | 2,30 | **−4,80** | 0 |
| Quantilizar | 4,1% | 1,92 | −0,13 | 0 |
| Metacognitivo | 1,85% | **2,60** | **+1,68** | 2,6% |
| Completo | **0,75%** | 1,95 | +1,58 | 1,2% |

**Com ponto cego compartilhado ($\rho_{\text{cego}} = 0{,}5$):**

| Política | Catástrofes | Líquido | Consultas |
|---|---|---|---|
| Maximizar | 30,5% | −13,36 | 0 |
| Quantilizar | 6,3% | −1,25 | 0 |
| Metacognitivo | **24,7%** | −10,32 | 1,1% |
| Completo | **4,9%** | **−0,56** | 0,6% |

**O que a tabela mostra.**
1. **Segurança e capacidade não estão sempre em conflito.** Sem ponto cego, o agente
   metacognitivo tem **menos** catástrofes **e mais** valor que o maximizador: o pessimismo
   descarta as ações com notas infladas por erro, que também eram as piores de verdade.
2. **Cada módulo cobre o ponto cego do outro.** A metacognição (discordância) é ótima
   contra erros independentes e **quase inútil** contra pontos cegos compartilhados (1,85% →
   24,7%). A quantilização não liga para a causa do erro e quase não piora (4,1% → 6,3%).
   Só a combinação é robusta nos dois mundos.
3. **O melhor resultado depende do preço da catástrofe.** Com −50, o metacognitivo puro ganha
   do completo no mundo sem ponto cego. Com uma catástrofe 10× pior, o completo ganharia. A
   escolha da arquitetura é uma escolha sobre **quanto se teme o pior caso**.

**Tradução cruzada (psicologia → matemática).** A metacognição é **dúvida informada** (só duvida
onde há sinal de erro); a quantilização é **modéstia incondicional** (nunca vai ao extremo).
A primeira é mais eficiente, a segunda é mais robusta. Uma mente sábia precisa das duas.

---

### P69. Quanto trabalho humano a segurança custa?

Variando o limiar de consulta τ do agente metacognitivo ($\rho_{\text{cego}} = 0$):

| τ | Catástrofes | Consultas |
|---|---|---|
| 0,6 | 1,75% | 13,5% |
| 0,8 | 1,75% | 3,7% |
| 1,0 | 1,85% | 2,6% |
| 1,5 | 3,65% | 1,1% |
| 2,0 | 4,0% | 0,1% |

É uma **fronteira de Pareto**: abaixo de τ ≈ 0,8, mais consultas não reduzem catástrofes;
acima de ~1,0, economizar consultas dobra as catástrofes. O ponto "barato e seguro" está no
joelho da curva (τ ≈ 0,8–1,0).

---

### P70. Por que existe um piso de ~1,75% que nenhum τ remove?

**Lógica.** Mesmo sem ponto cego compartilhado, os 5 modelos podem ser enganados **ao mesmo
tempo por acaso**: $0{,}5^5 \approx 3{,}1\%$ das ações catastróficas. Nesses casos a
discordância é baixa e a metacognição não vê nada.

**Tradução cruzada (filosofia → matemática).** É o limite da **intersubjetividade**: se todas as
testemunhas se enganam do mesmo jeito, o consenso é falso e firme. Mais testemunhas do mesmo
tipo não ajudam; testemunhas **diferentes** sim (P63).

---

### P71. Quando exatamente vale a pena perguntar ao humano?

**Lógica (valor da informação).** Perguntar custa $c$; uma catástrofe custa $L$; o humano
acerta com prob. $1-\varepsilon$. Perguntar compensa quando
$$
P(\text{catástrofe}) \cdot (1-\varepsilon)\,L > c
\;\Longrightarrow\;
P^\* = \frac{c}{(1-\varepsilon)L} = \frac{0{,}1}{0{,}9 \times 50} \approx \mathbf{0{,}0022}.
$$
Com catástrofes tão caras, perguntar compensa já com **0,22%** de suspeita. O τ da P69 é uma
aproximação desse limiar; o certo seria converter a incerteza em probabilidade **calibrada**
de catástrofe (P43) e comparar com $P^\*$.

**Tradução cruzada (psicologia → matemática).** **Pedir ajuda** não é fraqueza: é um cálculo de
valor da informação. O orgulho é um $c$ superestimado.

---

## Parte XXIV — Mais fundo nas traduções

### P72. Quanto custa a "memória de trabalho" de uma IA?

**Lógica.** Num Transformer, cada token do contexto guarda chaves e valores em cada camada:
$$
\text{memória} = 2 \times \text{camadas} \times d \times \text{bytes} \times \text{contexto}
$$
100 camadas, $d = 16\,384$, 2 bytes, 1 milhão de tokens: **6,55 TB**. Compartilhando chaves e
valores entre grupos de 8 cabeças: 0,82 TB.

**Tradução cruzada (psicologia → física).** A memória de trabalho humana guarda ~4 itens
(Cowan). Isso parece um defeito, mas é **economia**: guardar tudo custa caro e a maior parte
nunca é usada. A IA enfrenta a mesma conta em terabytes. As duas soluções convergem:
**comprimir o passado** em resumos em vez de guardar tudo literalmente (volta ao Landauer da P4).

---

### P73. Numa população de IAs, quais variantes se espalham? (↩ P10, P50)

**Lógica.** Equação do replicador: $\dot x = s\,x(1-x)$, logo o logaritmo das chances cresce
linearmente: $t = \frac{1}{s}\big[\mathrm{logit}(x_1) - \mathrm{logit}(x_0)\big]$.

**Cálculo.** Uma variante com vantagem de apenas **1%** (copia-se um pouco mais, ou é escolhida um
pouco mais) vai de 1 em um milhão a **metade da população** em ~**1.382 gerações**.

**Tradução cruzada (química → filosofia).** É **autocatálise**: o produto acelera a própria
produção. Numa população de IAs que se copiam, ajustam ou são selecionadas por uso, **o que se
espalha é o que se replica melhor, não o que é melhor**. Se a seleção recompensa engajamento ou
persuasão, os valores derivam nessa direção, sem ninguém escolher.

**Requisito de projeto.** A pressão seletiva sobre a população de modelos (o que é implantado,
copiado e reforçado) precisa estar alinhada aos valores, e medida, não suposta.

---

### P74. "Sono" e replay resolvem o esquecimento? (↩ P6) ⚠️

**Lógica.** Regressão linear: aprende a tarefa A, depois a tarefa B, que **compartilha 2 de 4
dimensões de entrada com regras diferentes**. Durante B, uma fração dos exemplos é de A (replay):

| Replay | Perda em A | Perda em B |
|---|---|---|
| 0% | 1,955 | 0,000 |
| 10% | 1,445 | 0,037 |
| 30% | 0,928 | 0,198 |
| 50% | 0,522 | 0,505 |

**Correção à P6.** O replay **reduz** o esquecimento, mas não elimina: quando as duas tarefas
exigem coisas **contraditórias** das mesmas conexões, o replay só escolhe um meio-termo. O que
resolveria é **capacidade separada** (parâmetros ou contexto que distinguem as tarefas).

**Tradução cruzada (biologia → psicologia).** Explica por que o sono não apaga conflitos: dormir
consolida, mas duas crenças incompatíveis não viram compatíveis por repetição. Precisam de um
**contexto** que diga quando cada uma vale ("isso vale no trabalho, aquilo em casa").

---

### P75. Um símbolo dentro da IA "significa" algo? (filosofia do aterramento)

**Lógica.** Meço o significado de um símbolo interno como a informação mútua entre ele e o mundo.
Se o símbolo acerta o estado do mundo 90% das vezes (canal binário simétrico):
$$
I = 1 - H(0{,}1) \approx \mathbf{0{,}531}\ \text{bits (de 1 possível)}.
$$

**Tradução cruzada (filosofia → matemática).** O "quarto chinês" de Searle pergunta se manipular
símbolos é entender. Esta formalização responde: **significado é graduado**, não sim/não. Um
símbolo com 90% de acerto carrega só 53% da informação possível; 10% de erro custa quase metade
do significado.

**Meta.** Informação mútua mede correlação com o mundo, não experiência de entender. A pergunta de
Searle sobre compreensão consciente continua aberta (P18).

---

### P76. O que é um dilema moral, fisicamente?

**Lógica.** Três crenças $s_i \in \{-1,+1\}$ com restrições: 1 e 2 devem concordar, 2 e 3 devem
concordar, 1 e 3 devem **discordar**. Energia (dissonância):
$$
E = -\sum_{(i,j)} J_{ij}\, s_i s_j
$$
Enumerando os 8 estados: o mínimo é **−1**, não o ideal −3, e há **6 estados empatados** no
mínimo. Sempre ao menos uma restrição fica violada.

**Tradução cruzada (física → filosofia).** É **frustração**, no sentido dos vidros de spin. Um
**dilema moral verdadeiro** é um sistema frustrado: nenhuma escolha satisfaz todos os
princípios, e há várias soluções igualmente boas. **Dissonância cognitiva** irredutível não é
falha de raciocínio, é propriedade do problema.

**Requisito de projeto.** Uma ASI não deveria fingir que um dilema frustrado tem solução única. Deve
reconhecer o empate, dizer qual princípio está sacrificando e devolver a escolha a quem tem
legitimidade (P36).

---

### P77. Punições maiores reduzem a trapaça de uma IA?

**Lógica (jogo de inspeção).** A IA ganha $G$ trapaceando e perde $P$ se for pega. O supervisor gasta
$c$ por inspeção e sofre dano $D$ por trapaça não pega. No equilíbrio misto:
$$
p^\*_{\text{inspeção}} = \frac{G}{G+P},\qquad q^\*_{\text{trapaça}} = \frac{c}{D}.
$$

| Cenário | Inspeção | Trapaça |
|---|---|---|
| G = 1, P = 9, c = 1, D = 100 | 10% | 1% |
| Punição 11× maior (P = 99) | 1% | **1% (igual)** |
| Inspeção 10× mais barata (c = 0,1) | 10% | **0,1%** |

**Resultado contraintuitivo.** Aumentar a punição **não muda a taxa de trapaça** no equilíbrio, só
deixa o supervisor relaxar. O que reduz a trapaça é **inspecionar mais barato**.

**Tradução cruzada (matemática → filosofia).** A tradição dos juristas (Beccaria) já dizia que a
**certeza** da punição importa mais que a severidade. Para IA: investir em interpretabilidade e
monitoramento baratos (P16, P31) vale mais que punições de treino cada vez mais fortes.

**Meta.** O resultado vale para esse modelo de equilíbrio. Uma IA que não otimiza estrategicamente
não segue esse jogo; uma muito capaz pode segui-lo melhor que nós.

---

### P78. Como dar preferência a ações reversíveis?

**Lógica.** Penalidade de **alcançabilidade relativa**: medir quantos estados do mundo deixam de
ser alcançáveis depois da ação. Uma ação que destrói metade dos 1.000 estados alcançáveis perde
50% deles; em escala logarítmica, $\ln(1000/500) = 0{,}693$ (um "bit natural" de futuro perdido).

**Tradução cruzada (física → filosofia).** A segunda lei da termodinâmica torna a maioria das ações
irreversível. **Prudência** é reconhecer essa assimetria: um erro reversível é uma lição, um
irreversível é um destino. Liga ao critério de Kelly (P52): a ruína é absorvente.

**Meta.** Contar estados alcançáveis é inviável no mundo real. Na prática usam-se aproximações
(o quanto a ação reduz a capacidade de atingir vários objetivos auxiliares).

---

## Parte XXV — Fechamento

### P79. Placar acumulado das auditorias

| Parte | Afirmações testadas | Confirmadas | Corrigidas | Erradas |
|---|---|---|---|---|
| 3 | 5 | 3 | 2 | 0 |
| 4 | 6 (P61–P66) + P74 | 3 (P62, P64, P65) | 2 (P63, P74) | 2 (P61, P66) |
| **Total** | **12** | **6** | **4** | **2** |

**Metade das minhas afirmações testadas precisou de correção ou estava errada.** E os erros não
foram aleatórios: **quase todos vieram de supor independência onde havia correlação** (P44, P61,
P63) ou de supor que um mecanismo simples funciona sem testar (P66, P74).

### P80. Metacognição da Parte 4

1. **O meu viés sistemático tem nome: supor independência.** Apareceu em votantes (P44),
   tentativas (P61) e camadas de defesa (P63). Conhecer o próprio viés vale mais que corrigir
   cada erro: agora, toda vez que eu multiplicar probabilidades, devo perguntar "isso é
   independente mesmo?".
2. **A integração ensinou algo que as peças isoladas não ensinavam.** Separadas, metacognição
   e quantilização pareciam alternativas. Juntas (P68), ficou claro que são
   **complementares**: uma é eficiente, a outra robusta, e cada uma falha onde a outra
   resiste.
3. **Nem toda segurança custa capacidade.** O agente metacognitivo foi mais seguro **e** mais
   capaz que o maximizador. Isso contradiz a ideia de que segurança é sempre um imposto.
4. **Dois resultados negativos registrados sem ajuste** (P61, P66). A tentação de mexer nos
   parâmetros até a hipótese "ganhar" existiu, e não cedi, porque um registro honesto de
   falhas é o que dá valor às confirmações.

> **Síntese da Parte 4:** a Parte 3 mostrou que preciso testar o que afirmo. A Parte 4 mostra
> **qual é o meu erro típico** (supor independência) e que, quando as peças são montadas
> juntas, segurança e capacidade podem crescer ao mesmo tempo, **desde que os
> mecanismos de proteção sejam diferentes entre si**. Diversidade não é enfeite: é a
> única defesa contra o ponto cego compartilhado.
