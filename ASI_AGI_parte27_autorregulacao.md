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

*(resultados abaixo)*
