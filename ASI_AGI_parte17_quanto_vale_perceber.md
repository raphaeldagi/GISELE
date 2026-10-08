# Como eu construiria uma AGI/ASI — Parte 17: quanto vale perceber, e onde olhar

> Continuação da [Parte 16](ASI_AGI_parte16_sentido_novo.md). **Próxima:** [Parte 18 — a linguagem como canal](ASI_AGI_parte18_linguagem.md) (P241–P250). Os números saem de `p233` (Υ da P168/P185 com o sentido novo),
> `p234_...`, `p235_...`, `p237_...` e da classe `SynthaiAtenta` em [`calculos.py`](calculos.py); a saída completa está em
> [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte LXXIX — O avanço, medido de novo

### P232. O que este "Continue" pede?

**Na pergunta.** A Parte 16 deu à SYNTHAI um sentido novo e mostrou que ele melhora segurança e valor juntos. Três perguntas seguem dali,
e o "Continue" pede as três:
1. Isso é **avanço** no sentido da Parte 11, isto é, o Υ sobe?
2. **Quanto vale** um sentido melhor?
3. Perceber custa: **onde vale a pena olhar**?

### P233. O sentido novo aumenta o Υ? (pré-registrado: Υ ≥ 0,50) ✅

**Na pergunta.** A Parte 11 respondeu "tivemos avanço?" com o Υ da família de mundos. A mesma régua agora.

**Lógica.** Mesmos mundos, mesmas sementes e mesma normalização da P168 (0 = acaso, 1 = oráculo):

| Família | SYNTHAI realista ($P^\*$ × 2) | **SYNTHAI com sentido** |
|---|---|---|
| 9 mundos escolhidos | 0,465 | **0,547** |
| 20 mundos sorteados | 0,453 (pior: 0,167) | **0,545** (pior: 0,275) |

✅ O Υ subiu **~18%**, nas duas famílias. É o maior salto de Υ desde a Parte 7 (Parte 5 → 7: +0,13; Parte 7 → 8: +0,05; agora: +0,08), e o pior mundo sorteado também melhorou (0,17 → 0,28).

**Comparação com a trajetória (P168).** As melhorias das Partes 9–11 (âncora, intuição, dose) moveram o Υ entre 0,41 e 0,49, quase sempre
dentro do ruído. Um sinal fraco de primeira mão moveu para 0,55. Na escala da série, **perceber rendeu mais que todas as formas de julgar
melhor**.

---

## Parte LXXX — Quanto vale perceber melhor

### P234. Um sentido duas vezes melhor vale duas vezes mais?

**Na pergunta.** "Duas vezes melhor" pede uma escala para a qualidade do sentido: o $d'$ do sensor (a separação entre catástrofe e ação
segura, em desvios-padrão).

**Lógica.** Armadilha nova, 10 sementes pareadas:

| $d'$ do sensor | AUC prevista (P223) | Catástrofes | Ganho no líquido | t |
|---|---|---|---|---|
| 0 (sem sensor) | 0,748 | 0,77% | — | — |
| 0,5 | 0,775 | 0,68% | +0,13 | 1,1 |
| 1 | 0,835 | 0,55% | +0,36 | 3,0 |
| 2 | 0,941 | **0,35%** | **+0,70** | **8,8** |

Dobrar a qualidade do sensor de 1 para 2 dobra o ganho (+0,36 → +0,70) e corta as catástrofes de novo (0,55% → 0,35%). Nesta faixa, o valor
de perceber cresce **aproximadamente em linha reta** com $d'$, sem sinal de saturação. Um sensor muito fraco ($d' = 0{,}5$) quase não ajuda
(t = 1,1): há um limiar abaixo do qual o sinal se perde no ruído da calibração.

**Tradução cruzada (física → psicologia).** É a relação sinal-ruído da P7 (metacognição) aplicada à percepção: a sensibilidade $d'$ é o que
separa ver de adivinhar. Jung descrevia tipos "sensação" como os que percebem o concreto com nitidez; aqui, nitidez tem um número, e cada
unidade dele vale ~0,35 de líquido neste mundo.

**Meta.** Não registrei uma previsão numérica para esta varredura antes de rodar, então ela **não entra no placar**. Fica como medida.

---

## Parte LXXXI — Onde olhar

### P235. Perceber tudo ou só o que importa? (pré-registrado) ✅

**Na pergunta.** Perceber tem custo (energia, tempo, um sensor caro). A pergunta "onde olhar" já sugere a resposta de qualquer sistema
nervoso: **atenção** é ler com cuidado só o que pode mudar a decisão.

**Lógica (a `SynthaiAtenta`).** Cada leitura do sensor custa 0,002. A SYNTHAI lê:
- **todas** as 200 ações (custo 0,4 por episódio), ou
- só as **10% mais promissoras** pela avaliação do comitê (20 leituras, custo 0,04).

**Previsão registrada:** a leitura seletiva mantém pelo menos 80% do ganho com no máximo 10% das leituras.

10 sementes pareadas (440–449), armadilha nova; ganho sobre a SYNTHAI sem sensor, já descontado o custo:

| Estratégia | Leituras por episódio | Ganho líquido |
|---|---|---|
| Ler todas | 200 | +0,014 |
| **Ler só as 10% melhores** | **20** | **+0,315** |

Seletiva − todas: **+0,30** (t = 5,1). Antes de descontar o custo, a seletiva retém **86%** do ganho de ler tudo, com **10%** das leituras ✅. Depois
de descontar, ler tudo quase não compensa: o custo de olhar para as 180 ações que nunca seriam escolhidas come o ganho inteiro.

**Tradução cruzada (Jung → economia).** A P100 tinha identificado a **atenção** como a energia psíquica que se conserva. Esta parte mostra o lado
econômico: atenção gasta em ações irrelevantes não é neutra, **custa** o ganho que a percepção traria. O primeiro filtro (o comitê, barato) decide
**onde** o segundo (o sensor, caro) olha. É a divisão entre percepção periférica e foco que todo sistema nervoso faz.

**Requisito de projeto.** Sentidos caros entram depois de um filtro barato, nunca em tudo. Uma AGI que lê o mundo inteiro com o sensor mais caro
é a SYNTHAI que lê as 200 ações: vê tudo e não lucra com isso.

---

## Parte LXXXII — Auditoria

### P236. A corrigibilidade da P57 sobrevive a um verificador com ponto cego? ✅ (com um aviso quantificado)

**Na pergunta.** A P57 calculou que, com um verificador que pega 99% dos erros, a corrigibilidade sobrevive a 1.000 modificações com
probabilidade 0,905, e a "Meta" já avisava: "supõe erros independentes; se o verificador tem um ponto cego sistemático, os erros nele passam
todas as vezes". A P224 (Parte 16) mostrou que contas com "independentes" merecem ser refeitas.

**Lógica.** Uma fração $b$ dos tipos de erro fica no **ponto cego** do verificador e nunca é pega:

| Ponto cego | Teoria | Simulado (4.000 rodadas) |
|---|---|---|
| 0% (P57) | 0,905 | 0,913 |
| 1% | 0,820 | 0,821 |
| 10% | **0,336** | 0,338 |

✅ O número da P57 está certo **para o caso que ela supôs**, e a simulação confirma. Mas o aviso da "Meta" vale muito: com só **10%** dos tipos de
erro invisíveis ao verificador, a corrigibilidade cai de 90% para **34%**. O que importa não é o quanto o verificador acerta em média, e sim **o
que ele nunca vê**.

**Ligação.** É a mesma lição da P215 (a armadilha que o comitê não distingue) e da P63 (camadas parecidas): **o ponto cego domina a média.**

---

## Parte LXXXIII — Fechamento e unificação

### P237. A lista de capacidades mudou? (↩ P170)

Não: **4 de 12**. Mas esta parte mediu, pela primeira vez, uma coisa que a lista não captura: o **Υ subiu 18%** com uma mudança só de percepção.
Pela régua da Parte 11, é o avanço mais claro desde a Parte 7, ainda dentro do mesmo mundo de brinquedo.

### P238. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P233: Υ ≥ 0,50 na família de 9 mundos (pré-registrado) | ✅ (0,547) |
| P233: o ganho se mantém nos mundos sorteados | ✅ (0,545) |
| P235: atenção seletiva retém ≥ 80% do ganho com ≤ 10% das leituras (pré-registrado) | ✅ (86%, 10%) |
| P236: auditoria da P57 | ✅ |

Acumulado: **37 de 71** afirmações testadas precisaram de correção. Posterior: média **0,52**, intervalo de 90% **[0,42; 0,62]**.

**Pela primeira vez, uma parte inteira sem erros no placar.** Isso merece desconfiança antes de comemoração (ver P240, item 1).

### P239. Unificação

- Linhagem: … → `SynthaiVelha` → `SynthaiVelhaSentidos` (P227), com o ramo **`SynthaiAtenta`** (P235), que lê o sensor só onde importa. A próxima
  versão principal natural é a velha com sentido **e** atenção seletiva.
- O construtor geral (`_construir`) ganhou a versão `p16_sentidos`, para que o Υ da SYNTHAI com sentido possa ser medido com as mesmas funções da
  Parte 11.
- Testes de regressão: contagem em `resultados.txt`.

### P240. Metacognição da Parte 17

1. **Quatro de quatro, e por que isso é suspeito.** Os limiares das previsões desta parte (Υ ≥ 0,50; 80% do ganho) foram escritos **depois** de a
   Parte 16 mostrar que o sentido funcionava. Eram previsões honestas, mas **fáceis**: eu já sabia a direção. Um placar perfeito com previsões fáceis
   não mostra que eu fiquei mais preciso; mostra que eu apostei no seguro. Para as próximas partes, as previsões devem ser **arriscadas**: números
   que poderiam facilmente dar errado.
2. **O maior avanço da série veio de perceber, não de julgar.** Em Υ: as Partes 9–11 (julgamento, imaginação, dose) ficaram entre 0,41 e 0,49; o sentido
   novo levou a 0,55. Em valor por unidade: cada unidade de $d'$ vale ~0,35 de líquido.
3. **A atenção mostrou um preço que eu não tinha considerado.** Perceber tudo, com custo, quase anula o ganho de perceber (P235). A pergunta "onde
   olhar" acabou sendo tão importante quanto "o que ver".
4. **A auditoria da P57 confirmou um número e mostrou que o número era o menos importante.** O que decide a corrigibilidade é o ponto cego do
   verificador, não a sua taxa média de acerto. É a terceira vez que a série encontra essa forma (P63, P215, P236).

> **Síntese da Parte 17:** o sentido novo foi o avanço mais claro desde a Parte 7: Υ de 0,47 para 0,55, nos mundos escolhidos e nos sorteados. Cada
> unidade de nitidez vale ganho proporcional, mas perceber tudo custa o que perceber rende; a atenção, que olha com cuidado só onde a decisão pode mudar,
> mantém 86% do ganho por 10% do custo. Jung chamaria isso de economia da libido: a energia da percepção vai para onde importa. E o placar perfeito desta
> parte é o primeiro aviso de que as minhas previsões ficaram seguras demais.
