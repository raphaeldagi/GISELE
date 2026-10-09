# Como eu construiria uma AGI/ASI — Parte 37 (0x25): o modelo certo de um mundo que muda

> Continuação da [Parte 36](ASI_AGI_parte36_exposicao_e_significado.md). Quatro partes construíram, à mão, agentes para quatro mundos (exato,
> desconto, surpresa, exposição), e nenhum dominou. O pressuposto da série diz que a resposta já existe como equação. Para um mundo que pode
> mudar, a equação é a **detecção bayesiana de mudança online** (Adams e MacKay, 2007): a crença de cada braço é uma mistura sobre "há quanto
> tempo o meu mundo mudou". Esta parte testa se o modelo certo dispensa as regras. Novidades: `ThompsonBOCPD`
> ([`synthai/decisao.py`](synthai/decisao.py)); testes em [`synthai/testes_parte37.py`](synthai/testes_parte37.py); números de `p531_...` a
> `p533_...` em [`calculos.py`](calculos.py). Diálogo, rodada 8.
>
> **Conta e previsões no commit `e54c06e`, antes de rodar.**

---

## As perguntas desta parte

1. **P531 (0x213).** O modelo bayesiano de mudança vence as regras nos três mundos? ↩ P491, P521
2. **P532 (0x214).** Quantas hipóteses por braço: um dígito hex basta?
3. **P533 (0x215).** O data lake obedece à lei da abreviação de Zipf? ↩ P522
4. **P534 (0x216).** Jung: o tempo psíquico e a renovação.
5. **P535 (0x217).** O diálogo, rodada 8.
6. **P579 (0x243).** Placar. **P580 (0x244).** Unificação.

---

### P531 (0x213). O modelo certo vence as regras? (pré-registrado) ✅❌❌

**Na pergunta.** "O modelo certo" pressupõe saber o que muda e com que frequência. Adams e MacKay: a cada passo, a "idade" do mundo de cada braço
ou cresce 1 (com chance 1 − H) ou volta a 0 (chance H). A crença é uma mistura de hipóteses [peso, a, b], uma por idade; a observação pesa cada
hipótese pela sua preditiva, a/(a + b) ou b/(a + b). Com o risco aplicado **por passo**, um braço não visto há muito tempo volta sozinho para
perto de Beta(1, 1): a exposição **sai do modelo**.

**Lógica, a conta antes (mundo estável, H = 1/500).** Um braço ruim não visto há Δt tem peso ≈ H·Δt na hipótese nova, cuja amostra passa a do
melhor braço (≈ p*) com chance 1 − p*. A espera até a próxima puxada resolve Σ_{s≤Δt} H·s·(1 − p*) = 1:
$$
\Delta t = \sqrt{\frac{2}{H(1-p^*)}} = \sqrt{\frac{2}{0{,}002 \times 0{,}09}} \approx 105\ \text{passos (com } p^* = 0{,}91).
$$
Nove braços ruins: 9/105 = 8,6% dos passos neles, a 0,45 cada: 2000 × 0,086 × 0,45 ≈ 77 (na média exata das sementes, **62,7**). Previsto:
30,7 + 62,7 = **93,5**.

**Medido:**

| mundo | exato | surpresa | surpresa + exposição | **BOCPD (H = 1/500)** |
|---|---|---|---|---|
| estacionário | 30,7 | 43,1 | 61,5 | **86,6** |
| dano, custo | 69,8 | 42,3 | 19,5 | **46,0** |
| muda a cada 500 | 808,7 | 367,7 | 427,1 | **371,9** |

(a) estacionário em [65,4; 121,5] ✅ (86,6, a 7% da conta). (b) dano < 20 ❌ (46,0). (c) mundo que muda < 367,7 ❌ (371,9: empate estatístico).

**Por que o modelo certo não venceu.**
1. **O dano não é uma mudança do mundo; é uma mudança da crença.** O BOCPD modela mundos que mudam, não memórias corrompidas. A crença de lixo é
   uma hipótese só, confiante, e a hipótese nova cresce a 0,2% por passo (H = 1/500): leva ~500 passos para pesar 63%. A exposição a cada 50
   passos testa 10 vezes antes.
2. **No mundo que muda, o modelo é o certo, mas a decisão não.** Thompson decide um passo de cada vez; o valor de testar um braço que pode ter
   mudado (informação para os próximos 500 passos) não entra na conta. A surpresa tem a mesma miopia e, com uma janela curta, chega ao mesmo lugar
   por outro caminho.

**Tradução cruzada.** Ter o modelo certo do mundo é a função **pensamento** de Jung; saber **quando** agir sobre ele é a **intuição**. A Parte 37
mostra que o pensamento certo, sem a intuição do horizonte, empata com uma boa regra.

**Meta.** Um só valor de H, o verdadeiro do mundo que muda; no mundo estável, ele está **errado** (o verdadeiro é 0), e o custo 86,6 mede o preço
de supor mudança onde não há. Um modelo hierárquico (H com distribuição a priori) aprenderia que o mundo estável não muda. É a pergunta seguinte.

### P532 (0x214). Um dígito hex de hipóteses basta? (pré-registrado) ✅

No mundo que muda: 16 hipóteses por braço **371,9**; 256 hipóteses **361,6**; diferença 10,4, dp 92,6, **t = 0,79** (d) ✅. A conta: com H = 1/500,
a hipótese de idade s tem peso a priori ∝ (1 − H)^s; as 16 de maior peso cobrem as idades que a preditiva ainda distingue (depois de ~16
observações, duas idades vizinhas preveem quase igual). Um dígito hex de hipóteses é o tamanho da memória que o mundo deixa usar.

### P533 (0x215). A lei da abreviação no data lake (pré-registrado) ✅✅

Spearman(comprimento em letras, frequência nas definições), 31.502 palavras: **−0,237** (e) ✅, dentro de [−0,45; −0,15] e perto do τ de Kendall
de −0,20 medido no inglês do corpus PUD (para dados contínuos, ρ ≈ 1,5τ = −0,30). As 1000 mais frequentes têm **6,03** letras em média; as
outras, **8,20** (f) ✅.

**Tradução cruzada.** As palavras que mais servem são curtas **e** polissêmicas (P522): o dicionário comprime o que mais usa. É o princípio da
estatística suficiente na língua: o mais usado ganha a forma mais curta.

### P534 (0x216). Jung: o tempo psíquico e a renovação

Jung distingue a mudança da **situação** (que pede adaptação) da mudança da **atitude** (que pede transformação). O BOCPD formaliza a primeira:
"o mundo deste braço pode ter mudado". Não formaliza a segunda: "a minha crença pode estar corrompida". A P531 separou as duas com números: o
modelo da mudança do mundo empata no mundo que muda (371,9) e falha no dano (46,0); a exposição, que é uma desconfiança da **própria crença**,
cura o dano (19,5). **Funciona:** o risco H é um tempo psíquico (a meia-vida de uma convicção). **Quebra:** em Jung, a transformação da atitude
vem de dentro (o Self); aqui, ainda vem de uma regra externa.

### P535 (0x217). O diálogo, rodada 8

A ThompsonBOCPD em Java: **144 números idênticos bit a bit** (g) ✅, com a soma compensada do Python e a ordenação estável. O que se aprendeu
nas rodadas 5 e 6 virou hábito: "acumular, não repetir". A pergunta para a Rodada 9: a SYNTHAI mora num arquivo, ou na igualdade dos bits entre
as duas linguagens?

### P579 (0x243). Placar

(a) ✅ (b) ❌ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅. Parte 37: 7 testes, 2 erros. Acumulado: **115 erros em 297 testes**; taxa média 0,39, intervalo
90% [0,34; 0,43].

### P580 (0x244). Unificação e metacognição

- **Novo:** `ThompsonBOCPD` (3 testes; 98 no pacote). Regressão: + P531 (o custo da exposição natural, 62,7).
- **O mapa da renovação, completo:**

| agente | estável | dano | muda | o que ele supõe |
|---|---|---|---|---|
| exato | **30,7** | 69,8 | 808,7 | nada muda |
| desconto γ 0,99 | 163,2 | **14,1** | 425,5 | tudo muda devagar |
| surpresa | 43,1 | 42,3 | **367,7** | muda o que surpreende |
| surpresa + exposição | 61,5 | 19,5 | 427,1 | e o que não se olha pode estar errado |
| BOCPD | 86,6 | 46,0 | 371,9 | o mundo muda com risco H |

Nenhum domina. Cada linha é uma **suposição sobre o mundo**, e cada coluna premia uma. O agente que vence as três colunas teria de **aprender a
suposição**: um posterior sobre H, ou um bandido sobre os agentes. É a pergunta da próxima parte.

**Metacognição.** Eu esperava que o modelo certo vencesse (c). O que eu não tinha separado era "o modelo certo do mundo" de "a decisão certa
dado o modelo". As duas falhas desta parte vêm daí.

> **Síntese da Parte 37:** o modelo bayesiano de um mundo que muda (Adams e MacKay), com o risco verdadeiro, empatou com a regra da surpresa no
> mundo para o qual foi feito (371,9 contra 367,7) e não curou o dano (46,0), porque o dano é uma crença corrompida, não um mundo mudado, e porque
> Thompson decide sem horizonte. A conta da sua exposição natural no mundo estável acertou a 7% (86,6 contra 93,5). Um dígito hex de hipóteses
> basta (t = 0,79 contra 256). O data lake obedece à lei da abreviação (ρ = −0,24; as palavras frequentes têm 6,0 letras, as outras 8,2). E a
> ThompsonBOCPD rodou em Java com 144 números idênticos bit a bit.

---

**Fontes pesquisadas nesta parte**
- Detecção bayesiana de mudança online: [Adams e MacKay, arXiv 0710.3742](https://ar5iv.arxiv.org/html/0710.3742), [PDF em Princeton](https://www.cs.princeton.edu/~rpa/pubs/adams2007changepoint.pdf), [notas do fast-bocpd](https://fast-bocpd.readthedocs.io/en/latest/theory/bayesian_changepoint.html), [arXiv 2407.16376](https://arxiv.org/pdf/2407.16376)
- A lei da abreviação: [Petrini et al., arXiv 2303.10128](https://arxiv.org/pdf/2303.10128) (τ de Kendall do inglês ≈ −0,20 no PUD), [Ferrer-i-Cancho et al., arXiv 1504.04884](https://arxiv.org/pdf/1504.04884), [Casas et al., arXiv 1904.00812](https://arxiv.org/pdf/1904.00812), [Bentz e Ferrer-i-Cancho, Tübingen](https://ub01.uni-tuebingen.de/xmlui/handle/10900/68639)
