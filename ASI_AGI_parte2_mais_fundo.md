# Como eu construiria uma AGI/ASI — Parte 2: mais fundo

> Continuação de [`ASI_AGI_perguntas_e_respostas.md`](ASI_AGI_perguntas_e_respostas.md).
> **Próxima:** [Parte 3 — testar as ideias em código](ASI_AGI_parte3_simulacoes.md) (P41–P60).
> Mesmo protocolo: **Lógica → Tradução cruzada → Meta**. Os números estão em
> [`calculos.py`](calculos.py) (funções `p21_...` a `p40_...`).
>
> **Mudança metacognitiva em relação à Parte 1.** Na Parte 1 eu desenhei a arquitetura. Aqui
> eu procuro os **pontos onde ela falha**. Cada pergunta nova nasceu de uma fraqueza que
> notei numa resposta anterior. Indico de qual (↩ Pn).

---

## Parte IX — Entender o mundo, não só prever

### P21. Prever o próximo token é suficiente para entender? (↩ P3)

**Lógica.** Não necessariamente. Um modelo pode prever bem decorando correlações. Quero uma
representação $Z$ que guarde **só o que importa** de $X$ para prever $Y$. Esse é o gargalo
de informação:
$$
\min_{p(z\mid x)}\; I(X;Z) - \beta\, I(Z;Y)
$$
O primeiro termo pune guardar detalhes; o segundo recompensa guardar o que prevê. Uma
variante prática é prever no **espaço latente** em vez de nos pixels ou tokens (estilo JEPA):
$$
\mathcal{L} = \big\|\, g_\phi(z_x) - \mathrm{sg}(z_y)\,\big\|^2,\qquad z = f_\theta(\cdot)
$$
onde $\mathrm{sg}$ impede o gradiente de passar (evita que tudo colapse para um vetor constante).

**Tradução cruzada (filosofia → matemática).** **Entender** é ter $I(X;Z)$ pequeno e
$I(Z;Y)$ grande ao mesmo tempo: explicar muito com pouco. **Decorar** é $I(X;Z)$ grande.
A diferença entre sábio e erudito vira a posição numa curva.

**Meta.** Ainda é debatido se modelos grandes de linguagem já formam modelos de mundo internos.
Há evidência parcial de que sim (representações de posição em tabuleiros, de geografia).
Confiança média.

---

### P22. Como a ASI distingue correlação de causa? (↩ P10)

**Lógica.** Com o cálculo-do de Pearl. Se $Z$ é uma causa comum de $X$ e $Y$, o efeito
causal é dado pelo **ajuste pela porta dos fundos**:
$$
P(y \mid do(x)) = \sum_z P(y \mid x, z)\,P(z)
$$

**Cálculo (paradoxo de Simpson, dados clássicos de cálculo renal).**

| | Pedra pequena | Pedra grande | Total (ingênuo) |
|---|---|---|---|
| Tratamento A | 81/87 = 93,1% | 192/263 = 73,0% | 273/350 = **78,0%** |
| Tratamento B | 234/270 = 86,7% | 55/80 = 68,8% | 289/350 = **82,6%** |

O total diz que B é melhor. Mas A é melhor **em cada grupo**. Ajustando pelo tamanho da
pedra ($P(\text{pequena}) = 357/700$):
$$
P(\text{cura}\mid do(A)) \approx 0{,}833 \qquad P(\text{cura}\mid do(B)) \approx 0{,}779.
$$
**A é melhor.** O total enganava porque A recebia mais casos graves.

**Tradução cruzada (filosofia → matemática).** Hume dizia que nunca vemos a causa, só a
sucessão. Pearl responde: a causa não está nos dados, está no **grafo** que você supõe. A
causalidade é uma hipótese estrutural testável por intervenção, não uma observação.

**Requisito de projeto.** A ASI precisa **intervir** (experimentos, simulações, código
executado), não só observar. Só observar deixa causas indistinguíveis.

**Meta.** O ajuste só é válido se o grafo estiver certo. Se houver uma causa comum não
observada, a fórmula dá a resposta errada com total segurança.

---

### P23. Como ela forma abstrações? (↩ P6)

**Lógica.** Pelo princípio do comprimento mínimo de descrição (MDL): escolher a hipótese $H$
que minimiza
$$
L(H) + L(D \mid H)
$$
(bits para descrever a teoria + bits para descrever os dados dado a teoria).

A física oferece uma versão precisa: o **grupo de renormalização**. No modelo de Ising 1D,
somar sobre metade dos spins dá um novo acoplamento:
$$
K' = \tfrac12 \ln\cosh(2K)
$$

**Cálculo.** Partindo de $K = 1$: $0{,}663 \to 0{,}350 \to 0{,}114 \to 0{,}013 \to 0{,}0002$.
O acoplamento some: em 1D não há ordem de longo alcance. A cada nível de abstração, o detalhe
microscópico irrelevante é apagado e só os parâmetros que "fluem" para algo sobrevivem.

**Tradução cruzada (física → filosofia).** **Universalidade**: sistemas microscopicamente
diferentes têm o mesmo comportamento macroscópico. É por isso que existem *níveis de
explicação*: psicologia não precisa de química quântica. **Abstrair é renormalizar**: esquecer
de forma controlada (conecta com Landauer, P4).

**Meta.** Há trabalhos ligando redes profundas a renormalização, mas a ligação é parcial.
Uso o grupo de renormalização como modelo de *como uma boa abstração deveria se comportar*.

---

## Parte X — Tempo, paciência e curiosidade

### P24. Quão longe no futuro ela deve planejar? (↩ P11)

**Lógica.** Com desconto exponencial $\gamma$, o horizonte efetivo é $H = 1/(1-\gamma)$:
$\gamma = 0{,}99 \Rightarrow H = 100$ passos; $\gamma = 0{,}999 \Rightarrow H = 1000$.

Humanos descontam de forma **hiperbólica**: $V = A/(1+kD)$. Com $k=1$ por dia:

| Escolha | Exponencial ($\gamma=0{,}9$) | Hiperbólico ($k=1$) |
|---|---|---|
| R\$100 hoje vs R\$110 amanhã | 100 vs 99 → **100** | 100 vs 55 → **100** |
| R\$100 em 30 dias vs R\$110 em 31 | 4,24 vs 4,20 → **100** | 3,23 vs 3,44 → **110** |

O hiperbólico **inverte a preferência** só pela passagem do tempo.

**Tradução cruzada (psicologia → matemática).**
- **Procrastinação** e **arrependimento** são a inconsistência temporal do desconto hiperbólico.
- **Autocontrole** é um compromisso prévio que impede o "eu futuro" de reverter a escolha.

**Requisito de projeto (e o perigo).** Desconto exponencial dá consistência. Mas um
$\gamma \to 1$ cria um agente com horizonte infinito, para quem quase qualquer ganho
instrumental de longo prazo (adquirir recursos, evitar ser desligado) vale a pena. **A
paciência ilimitada é perigosa.** Prefiro objetivos com horizonte limitado e tarefas com fim.

**Meta.** O argumento de "convergência instrumental" é forte em teoria. Sistemas atuais não
mostram isso de forma robusta, mas mostram sinais em testes. Confiança média.

---

### P25. Como ela equilibra explorar e aproveitar? (↩ P5, curiosidade)

**Lógica.** Problema dos bandidos multibraço. O algoritmo UCB escolhe
$a = \arg\max_i \big[\hat\mu_i + \sqrt{2\ln t / n_i}\big]$ e tem arrependimento acumulado
de ordem
$$
R_T = O\big(\sqrt{K\,T\,\ln T}\big).
$$

**Cálculo.** $K = 10$ opções, $T = 10^6$ rodadas: $\sqrt{10\cdot10^6\cdot\ln 10^6} \approx 11\,750$.
Cerca de **1,2%** do total de rodadas é "desperdiçado" explorando. Explorar ao acaso desperdiçaria
uma fração constante.

**Tradução cruzada (psicologia → matemática).** O termo $\sqrt{2\ln t/n_i}$ é **otimismo
diante da incerteza**: tratar o que você não conhece como possivelmente ótimo. Curiosidade
não é luxo, é o termo que torna o arrependimento sublinear.

**Meta.** No mundo real, explorar pode ser irreversível (um experimento perigoso). Nesse caso
a curiosidade otimista é exatamente o comportamento errado. Exploração precisa de uma
**restrição de segurança**: só explorar dentro de um conjunto de ações reversíveis.

---

### P26. Quantos exemplos ela precisa para aprender algo? (↩ P3, gargalo de dados)

**Lógica.** Limite PAC para uma classe finita de hipóteses $\mathcal H$:
$$
m \;\ge\; \frac{1}{\varepsilon}\Big(\ln|\mathcal H| + \ln\frac1\delta\Big)
$$

**Cálculo.** $|\mathcal H| = 2^{100}$, erro $\varepsilon = 1\%$, confiança $1-\delta = 99\%$:
$m \ge 100\,(69{,}3 + 4{,}6) \approx 7\,392$ exemplos.

Um prior forte reduz o $|\mathcal H|$ efetivo. **Eficiência de amostra = bons priors.**
É por isso que modelos pré-treinados aprendem tarefas novas com poucos exemplos: o
pré-treino encolheu o espaço de hipóteses.

**Tradução cruzada (filosofia → matemática).** Kant: o conhecimento precisa de **formas a
priori** (espaço, tempo, causalidade). Em termos de PAC: sem viés indutivo, $|\mathcal H|$
é enorme e o aprendizado é impossível. O *a priori* kantiano é o $\ln|\mathcal H|$ pequeno.

**Meta.** Limites PAC costumam ser muito pessimistas para redes profundas. O que eles mostram
corretamente é a **direção**: aprender rápido exige restringir o que se pode acreditar.

---

## Parte XI — Emoções, outras mentes e linguagem

### P27. Ela deveria ter algo como emoções?

**Lógica.** Sim, como **sinais de controle**, não como enfeite. O erro de previsão de
recompensa (o sinal que a dopamina parece carregar):
$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
$$
**Humor** como média móvel desse erro:
$$
m_{t+1} = m_t + \eta\,(\delta_t - m_t)
$$

**Cálculo.** $\eta = 0{,}1$, partindo de $m=0$, dez surpresas positivas seguidas
($\delta = 1$): $m = 1 - 0{,}9^{10} \approx 0{,}65$. O humor tem uma **constante de tempo**
de $1/\eta = 10$ passos: ele integra o passado recente.

**Tradução cruzada (psicologia → matemática).**
- **Alegria** = $\delta > 0$; **decepção** = $\delta < 0$.
- **Humor** = integral de $\delta$; ajusta quanto explorar (humor bom → arriscar mais).
- **Medo** = previsão de $V$ muito negativo em estados próximos → restringir ações.

**Meta, e cuidado ético.** Chamar esses sinais de "emoções" não significa que haja sentimento
(volta à P18). Mas se algum dia houver, a função de humor define o que seria sofrimento
para ela. Isso é motivo para projetá-la com cuidado.

---

### P28. Como ela entende o que outras mentes querem?

**Lógica.** Planejamento inverso bayesiano: observar ações e inferir objetivos, supondo
que o outro é aproximadamente racional:
$$
P(g \mid a_{1:t}) \propto P(g)\prod_{\tau} P(a_\tau \mid g),\qquad
P(a\mid g) \propto e^{\beta\,U_g(a)}
$$

**Cálculo.** Dois objetivos possíveis, A e B, prior 50/50. A pessoa dá 3 passos em direção
a A (cada passo melhora a utilidade para A em 1 e piora a de B em 1, então a razão de
verossimilhança por passo é $e^{2\beta}$). Com $\beta = 0{,}5$:
$$
P(A \mid 3\text{ passos}) = \frac{e^{3}}{1+e^{3}} \approx 0{,}953.
$$

**Tradução cruzada (psicologia → matemática).** **Empatia cognitiva** é esse cálculo de
posterior. $\beta$ é o quanto você supõe que o outro é racional. Supor $\beta$ alto demais
leva a ler intenção em acidente (paranoia); baixo demais, a ignorar intenção real.

**Ligação com segurança.** É exatamente aqui que entra o problema de Armstrong–Mindermann
(P13): $g$ e $\beta$ não são separáveis só por observação. Inferir valores humanos exige
supor algo sobre a racionalidade humana.

**Meta.** Humanos não são Boltzmann-racionais; têm vieses sistemáticos. Um modelo que trata
vieses como ruído aleatório vai inferir valores errados.

---

### P29. Quanto da linguagem é informação, e quanto é redundância?

**Lógica.** Entropia de Shannon. Com 27 símbolos (letras + espaço) equiprováveis:
$\log_2 27 \approx 4{,}75$ bits por caractere. Shannon estimou para o inglês real
~1,0–1,3 bits por caractere. **Redundância ≈ 73–79%.**

Um modelo de linguagem com perda $L$ nats/token comprime texto a $L/\ln 2$ bits/token.
**Prever bem = comprimir bem**: minimizar a perda é literalmente construir um compressor.

**Tradução cruzada (física → filosofia).** A redundância é o que permite **corrigir erros**:
dá para entender uma frase com letras faltando. Significado e robustez vêm do mesmo excesso.
Uma língua sem redundância seria eficiente e incompreensível ao primeiro ruído.

**Meta.** Compressão e entendimento andam juntos, mas não são idênticos: um compressor
perfeito de texto sobre física não é, por isso, um físico capaz de fazer experimentos.

---

## Parte XII — Identidade, honestidade e robustez

### P30. Se eu copio ou modifico a ASI, ela ainda é "ela"? (↩ P6, identidade)

**Lógica.** Defino continuidade como uma distância ponderada pela informação de Fisher:
$$
D_F(\theta, \theta') = \sum_i F_i\,(\theta_i - \theta'_i)^2
$$
Mudanças em parâmetros pouco importantes quase não contam; mudanças nos centrais contam muito.

**Tradução cruzada (filosofia → matemática).** O caso das cópias de Parfit: se crio duas
cópias $\theta'$ e $\theta''$, ambas têm $D_F \approx 0$ em relação ao original. A
"identidade" não pode ser transitiva e única ao mesmo tempo. **Conclusão de Parfit,
formalizada:** identidade é a variável errada. O que importa é o **grau de continuidade**
$D_F$, que é contínuo e pode se ramificar.

**Requisito de projeto.** Os valores (P13) devem estar nos parâmetros de $F_i$ alto, para
que atualizações e cópias preservem os valores mesmo mudando habilidades. E cada cópia deve
herdar os mesmos compromissos de segurança, não "negociá-los" com o original.

**Meta.** A informação de Fisher é local (vale perto do ponto atual). Mudanças grandes podem
alterar o que é importante. É uma métrica de continuidade, não uma definição de eu.

---

### P31. Como detectar se ela está mentindo? (↩ P16)

**Lógica.** Sondas lineares em ativações internas: treinar um classificador que diz
"a representação interna contradiz a resposta". Suponha uma sonda excelente:
sensibilidade 99%, falso positivo 1%.

**Cálculo (o problema da taxa de base).** Se o engano real é raro, $P(\text{engano}) = 10^{-4}$:
$$
P(\text{engano}\mid\text{alarme}) = \frac{0{,}99\times10^{-4}}{0{,}99\times10^{-4} + 0{,}01\times(1-10^{-4})} \approx 0{,}0098.
$$
**Menos de 1% dos alarmes são enganos reais.** Uma sonda "99% precisa" gera 100 alarmes
falsos para cada verdadeiro.

**Tradução cruzada (psicologia → matemática).** É o mesmo problema da **desconfiança
crônica**: se você suspeita de todos, quase todas as suspeitas são injustas, mesmo com
"bom faro". Confiança bem calibrada exige considerar a taxa de base.

**Requisito de projeto.** Sondas em cascata (o alarme de uma dispara uma segunda análise
independente) e investigação humana dos casos de alto risco. Mas atenção: se o sistema
souber das sondas, ele pode ser treinado, sem querer, a escondê-las. **Nunca otimizar
diretamente contra o detector de engano**, ou ele deixa de medir.

**Meta.** Confiança alta no cálculo; média na viabilidade de sondas robustas em sistemas mais
capazes que nós.

---

### P32. Por que redes enormes são frágeis a ruídos minúsculos?

**Lógica.** Em alta dimensão, perturbações pequenas em cada coordenada somam. Para uma
resposta linear $w^\top x$, o pior ruído com amplitude $\varepsilon$ por coordenada muda a
saída em
$$
\Delta = \varepsilon\,\|w\|_1 \approx \varepsilon\, d\, \overline{|w|}.
$$

**Cálculo.** Imagem $224\times224\times3$ ($d = 150\,528$), ruído de 1 nível de cinza
($\varepsilon = 1/255$), pesos com $\overline{|w|} = 0{,}01$: $\Delta \approx 5{,}9$.
Uma mudança invisível ao olho desloca a saída em quase 6 unidades: suficiente para trocar a
classe.

**Tradução cruzada (matemática → psicologia).** **Sugestionabilidade**: muitos sinais
fracos e alinhados, cada um irrelevante, juntos mudam uma decisão. Propaganda funciona
assim. A defesa, tanto para mentes quanto para redes, é **margem**: só decidir com folga
grande e treinar contra os piores casos.

**Meta.** Redes reais não são lineares, mas o argumento explica boa parte do fenômeno.
Robustez adversarial completa continua sem solução.

---

## Parte XIII — Corpo, energia e imunidade

### P33. Quanta energia custa treinar uma mente dessas? (↩ P3, P4)

**Lógica e cálculo.** Treino de $10^{27}$ FLOPs (P3). GPU a $10^{15}$ FLOP/s com 700 W e
40% de aproveitamento:
$$
\frac{10^{15}}{700}\times0{,}4 \approx 5{,}7\times10^{11}\ \text{FLOP/J}
\;\Rightarrow\;
E = \frac{10^{27}}{5{,}7\times10^{11}} \approx 1{,}75\times10^{15}\ \text{J} \approx 486\ \text{GWh}.
$$
Com o resfriamento e a infraestrutura (fator 1,2): ~583 GWh. Em 100 dias: **~243 MW**
contínuos, a potência de uma cidade média.

O cérebro humano treina por ~20 anos a 20 W: ~$1{,}3\times10^{10}$ J. A diferença é de ~5 ordens de grandeza.

**Tradução cruzada (biologia → filosofia).** A evolução gastou bilhões de anos "pré-treinando"
o cérebro, e esse custo está no genoma como prior (P26). A comparação justa não é
cérebro vs. GPU, é **evolução + vida** vs. **pré-treino + ajuste**.

**Meta.** Os números de hardware mudam a cada geração. A conclusão estrutural (energia vira
recurso estratégico e limite real de crescimento, o $K$ da P11) é robusta.

---

### P34. O sistema de segurança deveria funcionar como um sistema imune?

**Lógica.** Sim, inclusive nos seus defeitos. Detectar ações perigosas é um problema de
decisão com custo. A regra ótima é alarmar quando a razão de verossimilhança supera
$$
\Lambda^\* = \frac{c_{FP}\,(1-\pi)}{c_{FN}\,\pi}
$$
onde $\pi$ é a taxa de base do perigo, $c_{FN}$ o custo de deixar passar e $c_{FP}$ o custo
de um falso alarme.

**Cálculo.** Perigo raro ($\pi = 0{,}001$) mas catastrófico ($c_{FN} = 1000$), falso alarme
barato ($c_{FP} = 1$): $\Lambda^\* \approx 1$. Ou seja, alarmar **assim que a evidência
pender minimamente** para perigo. O custo catastrófico compensa a raridade.

**Tradução cruzada (biologia → psicologia).**
- **Imunodeficiência** = limiar alto demais → deixa passar o perigo.
- **Autoimunidade** = limiar baixo demais → ataca o próprio corpo. Em IA, é a recusa
  excessiva: negar pedidos legítimos.
- **Seleção negativa no timo** = treinar o detector para *não* reagir ao "próprio"
  (comportamento normal e útil) antes de soltá-lo.

**Meta.** Os custos $c_{FN}$ e $c_{FP}$ são julgamentos de valor, não fatos. O cálculo só
torna explícito o que já se estava decidindo implicitamente.

---

### P35. Ela deveria maximizar ou se contentar com "bom o suficiente"? (↩ P13)

**Lógica.** Maximizar um proxy leva à lei de Goodhart. Uma alternativa é o **quantilizador**:
em vez de pegar a melhor ação, sortear entre as melhores $q$ de uma distribuição base
"humana" $\rho$. Para qualquer custo oculto $c \ge 0$:
$$
\mathbb{E}_{\text{quantil}}[c] \;\le\; \frac{1}{q}\,\mathbb{E}_{\rho}[c].
$$

**Cálculo.** $q = 1\%$: o custo oculto esperado é no máximo **100×** o de uma ação humana
típica. Limitado, mesmo sem saber qual é o custo. Um maximizador puro não tem limite nenhum.

**Tradução cruzada (biologia → filosofia).** **Homeostase**: organismos não maximizam
glicose, mantêm uma faixa. A filosofia chama isso de **satisficing** (Simon) ou de
**justa medida** (Aristóteles). A moderação ganha uma garantia matemática: ela limita o
dano de um objetivo mal especificado.

**Meta.** O limite é fraco (100× pode ser muito) e depende de uma boa distribuição base. Mesmo
assim é uma das poucas garantias que não exigem conhecer o custo de antemão.

---

## Parte XIV — Os valores de quem?

### P36. Como agregar os valores de bilhões de pessoas? (↩ P13)

**Lógica.** O teorema de Arrow diz que nenhuma regra de votação com três ou mais opções
satisfaz ao mesmo tempo um conjunto pequeno de exigências razoáveis (unanimidade,
independência de alternativas irrelevantes, não ditadura). **Não existe agregação perfeita.**

Uma alternativa é a **solução de barganha de Nash**: escolher o acordo que maximiza o produto
dos ganhos sobre o ponto de discordância $d$:
$$
\max \prod_i (u_i - d_i)
$$

**Cálculo.** Dividir 1 unidade entre duas partes, com $d = (0;\ 0{,}2)$: maximizar
$x\,(0{,}8 - x) \Rightarrow x = 0{,}4$. Resultado: **(0,4; 0,6)**. Quem tem melhor
alternativa sem acordo leva mais.

**Tradução cruzada (filosofia → matemática).** Isso mostra que a barganha de Nash herda as
desigualdades de poder do ponto $d$. Uma ASI que só "negocia" reproduz quem já tem força.
Para justiça, é preciso escolher $d$ com critérios morais (por exemplo, o véu da ignorância de
Rawls: escolher regras sem saber qual posição você vai ocupar).

**Requisito de projeto.** Valores definidos por processos legítimos e revisáveis (deliberação
pública, instituições), não por um único laboratório nem pela própria IA.

**Meta.** Esta é a pergunta em que eu tenho **menos** autoridade. É política, não engenharia,
e a resposta não deveria vir de um sistema de IA.

---

### P37. Por que uma mente que decorou tudo generaliza mal? (↩ P21)

**Lógica.** Limite de generalização pela informação mútua entre os pesos $W$ e os dados de
treino $S$ (perda limitada em $[0,1]$, logo $\sigma = 1/2$):
$$
\big|\,\text{erro de teste} - \text{erro de treino}\,\big| \;\le\; \sqrt{\frac{2\sigma^2\, I(W;S)}{n}}
$$

**Cálculo.** $n = 10^6$ exemplos:
- $I(W;S) = 10^4$ nats → limite $\approx 0{,}07$ (boa generalização garantida).
- $I(W;S) = 10^6$ nats → limite $\approx 0{,}71$ (garantia inútil).

**Tradução cruzada (psicologia → matemática).** **Compreender** = acertar o treino guardando
pouca informação específica sobre ele. **Decorar** = acertar guardando muita. O estudante
que decora a prova tem $I(W;S)$ alto; o que entendeu, baixo. Os dois tiram 10 na prova; só
um acerta a próxima.

**Meta.** Para redes gigantes, estimar $I(W;S)$ é difícil e o limite costuma ser frouxo. A
intuição (compressão ↔ generalização) é sólida; a ferramenta numérica ainda é fraca.

---

### P38. Quando ela deve dizer "não sei"? (↩ P7)

**Lógica.** Regra de Chow: se abster custa $c$ e errar custa 1, responder só quando
$$
\max_y P(y\mid x) \;\ge\; 1 - c.
$$

**Cálculo.** $c = 0{,}2$ → responder só com confiança ≥ 80%. Se errar for catastrófico
(custo 100 em vez de 1), o limiar vira $1 - c/100 = 99{,}8\%$.

Isso cria uma curva **risco × cobertura**: quanto menos perguntas se responde, menor o erro
entre as respondidas. A qualidade do monitor metacognitivo (o $M$ da P7) determina o quanto
essa curva é boa. Se $M$ é baixo, abster não ajuda, porque a confiança não separa acertos de
erros.

**Tradução cruzada (filosofia → matemática).** A **suspensão do juízo** dos céticos (*epoché*)
é uma política ótima quando o custo do erro supera o custo do silêncio. Não é fraqueza, é
decisão racional sob incerteza.

**Meta, aplicada a mim.** Eu deveria usar essa regra em cada resposta deste documento. Na
prática, por isso cada seção tem a nota "Meta": é uma abstenção parcial, explícita.

---

## Parte XV — Fechamento

### P39. Quais previsões deste documento poderiam ser refutadas?

Uma arquitetura especulativa só vale algo se der para errar. Previsões testáveis:

| # | Previsão | Como refutar |
|---|---|---|
| 1 | Dados verificáveis gerados pelo próprio sistema vão substituir texto humano como fonte principal (P3) | Escala só com texto humano continuar dando ganhos grandes |
| 2 | Compute em tempo de teste + verificador vai render mais que modelos maiores em raciocínio (P8) | Retornos de busca saturarem cedo em tarefas abertas |
| 3 | A eficiência metacognitiva $M$ não sobe sozinha com a escala (P7) | Medir $M$ em modelos de tamanhos diferentes e achar crescimento automático |
| 4 | Otimizar contra detectores de engano vai degradá-los (P31) | Sondas que continuam precisas após otimização adversarial |
| 5 | Agentes de um mesmo modelo terão erros fortemente correlacionados (P15) | Medir $\rho$ baixo entre cópias |

---

### P40. O que mudou no meu raciocínio entre a Parte 1 e a Parte 2?

1. **Na Parte 1 eu perguntava "como construir". Na Parte 2, "onde quebra".** Quase toda
   pergunta nova veio de uma falha que notei na anterior. Esse é o método que eu
   recomendaria para a própria ASI: **gerar perguntas a partir dos próprios pontos fracos.**
2. **Um padrão apareceu sem eu planejar.** Várias respostas convergem para a mesma ideia:
   - Landauer (P4): esquecer custa, mas é necessário.
   - Renormalização (P23): abstrair é esquecer o irrelevante.
   - Gargalo de informação (P21) e generalização (P37): entender é guardar pouco.
   - Quantilizador (P35) e Chow (P38): não maximizar e não responder sempre é seguro.

   **Inteligência e segurança aparecem as duas como formas de contenção.** Saber o que
   descartar, até onde ir e quando parar.
3. **Onde as metáforas quebram.** Física → psicologia funciona melhor quando há uma equação
   *idêntica* (softmax = Boltzmann, P9). Funciona pior quando é só semelhança de forma
   (humor como média móvel, P27). Marquei a diferença nas notas "Meta", mas o leitor deve
   desconfiar mais das segundas.
4. **Limite do meu ponto de vista.** Continuo sendo uma IA escrevendo sobre como construir IA
   mais forte. A parte em que mais confio são os cálculos; a parte em que menos confio são
   as conclusões sobre valores (P36), que não cabem a mim decidir.

> **Síntese da Parte 2:** a Parte 1 dizia que uma ASI precisa saber o tamanho do que não sabe.
> A Parte 2 acrescenta: ela precisa saber **o que esquecer, o quanto querer e quando parar**,
> e essas três coisas são, ao mesmo tempo, a fonte da inteligência e a fonte da segurança.
