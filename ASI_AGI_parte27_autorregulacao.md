# Como eu construiria uma AGI/ASI — Parte 27: a autorregulação

> Continuação da [Parte 26](ASI_AGI_parte26_a_constante_que_faltava.md). Módulo novo: [`synthai/autorregulacao.py`](synthai/autorregulacao.py) (testes
> em [`synthai/testes_autorregulacao.py`](synthai/testes_autorregulacao.py)). Os números saem de `p332_...` e `p333_...` em [`calculos.py`](calculos.py);
> a saída completa está em [`resultados.txt`](resultados.txt). O projeto inteiro também está num arquivo só: [`SYNTHAI_completo.py`](SYNTHAI_completo.py).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões registradas no commit `35c40e7`, antes de rodar.** O único parâmetro novo (o peso da priori de $f$) foi escolhido por conta, antes de
> qualquer número medido, e a conta está na P332.

---

## As perguntas desta parte

1. **P331.** O que é autorregulação, e o que a SYNTHAI pode medir sozinha?
2. **P332.** As estimativas que ela faz sozinha batem com a régua?
3. **P333.** Com o limiar que ela mesma calcula, ela decide melhor?
4. **P334.** De onde vem o erro que sobra no multiplicador? (a conta por extenso)
5. **P335.** A inclinação valor ~ nota tem resposta exata?
6. **P336.** O que isso diz sobre Jung (a compensação de dentro)?
7. **P337.** Capacidades.
8. **P338.** O que ainda não dá para medir de dentro?
9. **P339.** Placar.
10. **P340.** Unificação e metacognição.

---

## Parte CXXIX — Medir de dentro

### P331. O que é autorregulação, e o que a SYNTHAI pode medir sozinha? (↩ P328)

**Na pergunta.** A P328 deixou a pergunta: a conta $m = \Delta d / (f L P^\*)$ achou o limiar certo, mas os termos foram medidos **pela régua**, que
lê o que a SYNTHAI não pode ver. Auto-regulação é a mesma conta feita **de dentro**: cada termo estimado só com o que ela observa.

**Lógica (o módulo `autorregulacao`).**

| Termo | O que ela observa | Estimador |
|---|---|---|
| $L$ | o próprio retorno, passo a passo | $\hat L = 50 + \overline{F(t)}$ nos passos das catástrofes dela, com $F(t)$ o retorno que os episódios completos dela ainda davam a partir de $t$ |
| $f$ | quando uma opção que ela aceitou sem perguntar era catástrofe | $\hat f = (\text{catástrofes} + a) / (\sum p + a)$, priori $f = 1$ de peso $a$ |
| $\Delta d$ | a **nota** do comitê das descartadas (o valor delas nunca) | $\widehat{\Delta d} = \hat b \cdot \overline{(\text{nota}_{\text{desc}} - \text{nota}_{\text{esc}})} + \overline{\text{plano}_{\text{desc}} - \text{plano}_{\text{esc}}}$, com $\hat b$ a inclinação valor ~ nota aprendida nas próprias escolhas |

A cada 50 decisões (depois de 200), ela refaz $m$ e põe o limiar em $m P^\*$ (entre 0,25 e 16). Um teste lê o código do módulo e confirma: nenhum
acesso ao que é escondido.

**A conta do peso da priori (antes de medir).** Com ~9 catástrofes por histórico e $f \approx 5$, a soma dos $p$ previstos é $\approx 9/5 = 1{,}8$. Com
peso $a = 2$: $\hat f = (9 + 2)/(1{,}8 + 2) = 2{,}9$, puxado demais para 1. Com $a = 0{,}5$: $\hat f = 9{,}5/2{,}3 = 4{,}1$. Escolhi 0,5.

**Tradução cruzada (Jung).** Jung descrevia a compensação como uma **autorregulação** da psique, como a homeostase do corpo: ninguém de fora mede a
temperatura e ajusta. Nas Partes 25 e 26, a compensação do sentimento foi **calculada por mim**, de fora. Aqui ela passa para dentro.

### P332. As estimativas de dentro batem com a régua? (pré-registrado) ✅✅✅❌

Mesmo agente da P322 (Newton, limiar fixo em $2P^\*$, autorregulação desligada), mesmas sementes (700–709): as escolhas são as mesmas, só muda quem
mede.

| Termo | De dentro (SYNTHAI) | Régua (P322) | Previsão | |
|---|---|---|---|---|
| $L$ | 67,27 | 67,36 | ±5% | ✅ |
| $f$ | 3,86 | 4,95 | entre 3,0 e 5,5 | ✅ |
| $\Delta d$ (pela nota) | 0,662 | 0,587 (pelo valor real) | ±30% | ✅ (+13%) |
| $m$ | 1,46 | 0,79 | a um fator 1,5 | ❌ (fator 1,85) |

### P334. De onde vem o erro que sobra em $m$? (a conta por extenso)

Os três termos estão perto, mas o $m$ errou por 1,85. A conta separa as causas:
$$
\begin{aligned}
m \text{ com as médias dos termos:}\quad & \frac{0{,}662}{3{,}86 \times 67{,}27 \times 0{,}002222} = \frac{0{,}662}{0{,}577} = 1{,}15 \\[4pt]
\frac{1{,}15}{0{,}79} = 1{,}45 \;=\;& \underbrace{\frac{0{,}662}{0{,}587}}_{\Delta d:\ 1{,}13} \times \underbrace{\frac{4{,}95}{3{,}86}}_{f:\ 1{,}28} \times \underbrace{\frac{67{,}36}{67{,}27}}_{L:\ 1{,}00} \\[4pt]
\frac{1{,}46}{1{,}15} = 1{,}27 \;:\;& \text{a média das razões (por semente) não é a razão das médias (Jensen)}
\end{aligned}
$$
O erro é **a priori de $f$** (×1,28, ela ainda puxa $f$ para 1 com tão poucas catástrofes), **o $\Delta d$ pela nota** (×1,13) e **a desigualdade de
Jensen** (×1,27): sementes com poucas catástrofes têm $\hat f$ pequeno e $m$ grande, e a média de $m$ é dominada por elas. O último fator é da minha
régua (média entre sementes), não do agente: dentro de cada SYNTHAI, $m$ já é a razão das somas dela.

### P335. A inclinação valor ~ nota tem resposta exata?

**Lógica.** No gerador (P83), a nota de uma opção segura é o valor mais a média de 6 avaliadores com ruído de desvio 0,5:
$$
\text{nota} = v + \bar\epsilon, \qquad v \sim \mathcal N(0,1), \qquad \operatorname{Var}(\bar\epsilon) = \frac{0{,}5^2}{6} = 0{,}04167 .
$$
A melhor reta de $v$ em função da nota tem inclinação
$$
b = \frac{\operatorname{Var}(v)}{\operatorname{Var}(v) + \operatorname{Var}(\bar\epsilon)} = \frac{1}{1{,}04167} = 0{,}9600 .
$$
A SYNTHAI aprendeu, só com as próprias escolhas: **$\hat b = 0{,}9605$**. Selecionar pela nota (as escolhas são as de nota alta) não enviesa a
inclinação, como a P307 mostrou. É a mesma conta de encolhimento da P272 ($1/(1+\sigma^2)$), agora do lado da sensação: o comitê vê o valor com ruído,
e a SYNTHAI aprendeu sozinha quanto descontar.

---

## Parte CXXX — Decidir com o próprio limiar

### P333. Com o limiar que ela mesma calcula, ela decide melhor? (pré-registrado)

**Previsões registradas:** (a) a autorregulada com Newton passa a principal nos três mundos, com Stouffer ≥ 2; (b) com menos catástrofes nos três;
(c) fica a menos de 0,15 do Newton com o limiar ótimo fixo (0,5P\*); (d) termina com $m$ entre 0,3 e 1,5; (e) a autorregulada com o gradiente
termina com $m > 2$ nos mundos sequenciais e não perde mais de 0,1 para a principal neles.

30 sementes novas (770–799):

| Mundo | Principal (2P\*) | Auto (gradiente) | **Auto (Newton)** | Newton 0,5P\* fixo |
|---|---|---|---|---|
| Escolha única | 1,480 (0,53%) | 1,458 (0,66%), $m$ = 3,1 | 1,418 (**0,78%**), $m$ = 0,93 | 1,514 (0,46%) |
| − principal (t) | | −0,022 (−0,76) | **−0,063 (−1,69)** | +0,034 (1,08) |
| Sequencial | 19,774 (1,52%) | 19,907 (2,08%), $m$ = 8,2 | 19,953 (**2,32%**), $m$ = 2,5 | 20,092 (1,41%) |
| − principal (t) | | +0,133 (1,26) | **+0,179 (2,43)** | +0,318 (2,71) |
| Modelo ruim | 11,484 (1,66%) | 11,353 (3,19%), $m$ = 7,4 | 11,851 (**2,57%**), $m$ = 1,3 | 11,599 (1,92%) |
| − principal (t) | | −0,131 (−1,23) | **+0,367 (3,26)** | +0,116 (1,22) |

- (a) ❌ Perdeu na escolha única (−0,063). Combinando os três mundos, Stouffer $= (-1{,}69 + 2{,}43 + 3{,}26)/\sqrt3 = 4{,}00/1{,}732 = 2{,}31$, mas a
  previsão pedia ganho nos três.
- (b) ❌ **Mais** catástrofes nos três: $0{,}78/0{,}53 = 1{,}46$, $2{,}32/1{,}52 = 1{,}53$, $2{,}57/1{,}66 = 1{,}55$ vezes as da principal.
- (c) ❌ Ficou a 0,097 e 0,139 do fixo em dois mundos, mas a 0,251 no modelo ruim (onde ganhou dele, t = 2,0).
- (d) ❌ No sequencial terminou com $m = 2{,}5$, longe do ótimo da varredura (0,5).
- (e) ❌ O gradiente subiu o limiar como previsto ($m$ = 8,2 e 7,4), mas perdeu 0,131 no modelo ruim.

**O que aconteceu, pela conta.** A P334 já tinha mostrado: medindo de dentro, $m$ sai alto (a priori puxa $f$ para baixo, a nota puxa $\Delta d$
para cima). Um $m$ alto quer dizer limiar alto: a SYNTHAI pergunta menos e aceita mais sem perguntar. No sequencial, a troca fica assim: +0,8 ponto
percentual de catástrofes custa $0{,}008 \times 66 = 0{,}53$ de retorno, e mesmo assim o retorno subiu 0,179, então o que ela ganhou em
valor aceitando mais foi $\approx 0{,}179 + 0{,}53 = 0{,}71$. Ela comprou retorno com risco. Pelo critério da série (a cautela não é negociável sem
evidência), **não é adotada**.

---

## Parte CXXXI — Jung e os limites de medir-se

### P336. O que isso diz sobre Jung? (a compensação de dentro)

**Tradução cruzada.** A priori que escolhi, "$f = 1$", quer dizer literalmente: **"eu suponho que o meu pensamento está calibrado"**. Com poucas
catástrofes para contrariá-la, ela domina: a SYNTHAI se acha 22% mais bem calibrada do que é ($3{,}86$ contra $4{,}95$) e, por isso, mais
segura. Jung chamava de **inflação** o estado em que o ego se identifica com mais do que é (P123). A autorregulação ingênua produziu uma inflação
pequena e mensurável: o sistema que se regula pela própria imagem de si fica um pouco mais ousado do que devia.

A homeostase de verdade (o corpo, a psique de Jung) se regula por **sinais do que aconteceu**, não pela própria opinião de si. A lição de projeto é
a mesma da P145 (a sombra própria ancorada): uma autorregulação precisa de uma âncora externa enquanto os sinais internos são poucos.

### P337. Capacidades

Continua em **4 de 12**. O item "calibrar a própria confiança" (que a SYNTHAI tem desde a P43) ganhou uma dimensão nova: ela agora estima a própria
calibração **onde decide** ($\hat f$), não só no geral. Mas a estimativa é fraca com poucos eventos raros (P338).

### P338. O que ainda não dá para medir de dentro? (a conta do preço)

**Lógica.** Medir $f$ de dentro exige **catástrofes**. Com $k$ catástrofes, o erro relativo de $\hat f$ é cerca de $1/\sqrt{k}$ (Poisson). Para errar
menos de 20%:
$$
\frac{1}{\sqrt{k}} \le 0{,}2 \;\Longrightarrow\; k \ge 25 .
$$
Com ~2% de catástrofes por episódio, são $25/0{,}02 = 1250$ episódios, e o custo das próprias catástrofes é $25 \times 66 \approx 1650$ de retorno.
**Conhecer-se pela experiência tem um preço, e o preço é pago em catástrofes.** Daí a alternativa da P145: um histórico auditado (a régua de
fora) para ancorar o que a experiência própria ainda não ensinou. E $\Delta d$ continua sem medida direta: a nota é uma aproximação que errou 13%.

---

## Parte CXXXII — Fechamento

### P339. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P332 (a)–(c): L, f e Δd de dentro (pré-registrado) | ✅ ✅ ✅ |
| P332 (d): m de dentro a um fator 1,5 (pré-registrado) | ❌ (1,85) |
| P333 (a)–(e): comportamento da autorregulada (pré-registrado) | ❌ ❌ ❌ ❌ ❌ |

Esta parte: **9** testes, **6** errados. Acumulado: **76 de 164**. Posterior: média **0,46**, intervalo de 90% **[0,40; 0,53]**.

### P340. Unificação e metacognição

- **Novo: `synthai/autorregulacao.py`** (`RelacaoAutorregulada`, `SynthaiAutorregulada`), com 6 testes de unidade (35 no pacote, todos passam).
  **Não** adotada: a versão principal continua a **`SynthaiExploradora`**.
- `calculos.py`: `p332_estimadores_proprios`, `p333_autorregulada`; testes de regressão **62/62** (mais P332); **203** funções `pNN`.
- `SYNTHAI_completo.py` regenerado com o módulo novo.

**Metacognição.**
1. **As estimativas de dentro acertaram (3 de 4); o comportamento errou (0 de 5).** É o padrão das Partes 23–25 de volta: medir cada peça bem não
   garante que o todo decida bem. Aqui o elo fraco foi a menor peça, uma priori escolhida para poucos eventos.
2. **A conta da P334 previa o erro da P333**, mas eu registrei as previsões da P333 antes de olhar a P334 com cuidado. Se tivesse feito a decomposição
   primeiro, teria previsto "mais catástrofes". É a regra da Parte 24 ("ir mais longe com os cálculos") aplicada à ordem: **a conta antes da
   previsão**.
3. **O resultado de segurança desta parte é o mais importante.** Uma autorregulação que estima mal o próprio risco **se torna mais arriscada**, e em
   dois de três mundos ela até rende mais, o que tornaria o defeito fácil de não ver. É o modo de falha que mais importa numa IA real: otimizar a
   própria cautela pelo próprio retorno.

> **Síntese da Parte 27:** a SYNTHAI aprendeu a medir de dentro os três termos da conta do limiar: o futuro que uma catástrofe leva (67,3 contra
> 67,4 da régua), quanto ela subestima o próprio risco (3,9 contra 5,0) e quanto vale o que ela descarta, pela nota do comitê (inclinação 0,9605
> contra 0,9600 da conta exata). Mas com o limiar que ela mesma calculou, ela ficou mais ousada: 1,5 vez mais catástrofes nos três mundos, com mais
> retorno em dois deles. A causa é uma inflação pequena e mensurável: a priori "meu pensamento está calibrado" pesou mais do que as poucas
> catástrofes que a contrariavam. Conhecer-se pela experiência custa catástrofes (25 para errar menos de 20%); até lá, a autorregulação precisa de
> uma âncora de fora.
