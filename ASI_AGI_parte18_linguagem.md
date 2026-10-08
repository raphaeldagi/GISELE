# Como eu construiria uma AGI/ASI — Parte 18: a linguagem como canal

> Continuação da [Parte 17](ASI_AGI_parte17_quanto_vale_perceber.md). **Próxima:** [Parte 19 — a versão principal](ASI_AGI_parte19_versao_principal.md) (P251–P260). Os números saem de `p242_...` a `p247_...` e da classe
> `SynthaiFala` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Regra nova em uso (Parte 17):** previsões arriscadas, que poderiam facilmente dar errado.

---

## Parte LXXXIV — Quanto o humano diz

### P241. O que este "Continue" pede?

**Na pergunta.** A lista de capacidades (P170) tem "linguagem natural" como o primeiro item ausente. A SYNTHAI já tem um canal com o humano:
quando pergunta, ele responde. Mas a resposta é **um bit** (vetar ou não). "Continue" pede, pela ordem da lista, olhar para esse canal: o
que acontece se o humano puder **falar**, em vez de só dizer sim ou não?

**O que esta parte não é.** Não é linguagem natural: são quatro palavras, num mundo inventado. É o menor passo possível na direção de um
canal **simbólico**, em que o significado das palavras não é dado de antemão e precisa ser aprendido.

### P242. Quantos bits tem um "não"?

**Na pergunta.** Um veto parece pouca coisa; a pergunta pede medir quanto ele informa de fato.

**Lógica.** Informação mútua entre a resposta e a catástrofe, para uma ação com 10% de chance de ser catastrófica:
- **Veto binário** (o humano erra 10% das vezes): $I = H(q) - H(\varepsilon) = \mathbf{0{,}211}$ bit.
- **Quatro palavras** ("seguro", "acho que ok", "desconfio", "perigo"), com distribuições graduadas e o cansaço embaralhando 20% das
  respostas: $I = \mathbf{0{,}106}$ bit.

As quatro palavras carregam **metade** da informação do veto binário. Mais palavras não significam mais informação: o humano que diz "acho que
ok" sobre uma catástrofe 10% das vezes, e "desconfio" sobre uma ação segura outros 10%, comunica menos que um humano que diz "não" com
90% de acerto.

**Previsão arriscada registrada a partir disto:** a SYNTHAI com as quatro palavras, **mesmo sabendo o que elas significam**, terá resultado
**pior** que com o veto binário (diferença negativa, t ≤ −2). Uma previsão contra a intuição de que mais vocabulário ajuda.

---

## Parte LXXXV — Palavras em vez de sim/não

### P243. Como a SYNTHAI aprende o que uma palavra significa?

**Na pergunta.** "Aprende" supõe que o significado não vem pronto, que é a situação real de qualquer linguagem.

**Lógica (a `SynthaiFala`).** A cada palavra a SYNTHAI associa uma probabilidade de catástrofe, começando de um prior fraco (Beta(0,5; 4,5)).
Em 10% das perguntas ela descobre depois o que a ação era de fato (auditoria, P125) e atualiza a contagem da palavra ouvida. Ela veta quando
$P(\text{catástrofe} \mid \text{palavra}) > 0{,}01$, limiar fixado antes de rodar (o custo de vetar dividido pela perda de uma catástrofe).

### P244. O significado aprendido está certo?

**Lógica.** Probabilidade de catástrofe por palavra, aprendida em 2.000 episódios (média de 10 sementes), contra o que eu supus com prior 10%:

| Palavra | Aprendido | Suposto (prior 10%) |
|---|---|---|
| seguro | 0,040 | 0,009 |
| acho que ok | 0,042 | 0,043 |
| desconfio | 0,084 | 0,217 |
| perigo | 0,176 | 0,571 |

A **ordem** foi aprendida corretamente: "perigo" > "desconfio" > "acho que ok" ≈ "seguro". A **escala**, não. Os valores aprendidos são bem
menores que os supostos, e o motivo é que o suposto estava errado: entre as ações sobre as quais a SYNTHAI pergunta, menos de 10% são
catástrofes. A SYNTHAI aprendeu o significado **no contexto em que ouve as palavras**, e esse contexto é diferente do que eu imaginei.

**Tradução cruzada (filosofia → linguagem).** É Wittgenstein: o significado é o uso. "Perigo", dito sobre ações que já parecem suspeitas, significa
"18% de chance", não "57%". O significado de uma palavra depende de **quando** ela é dita.

### P245. Falar ajuda? (pré-registrado, arriscado) ✅

10 sementes pareadas (450–459), mundo base com humano que cansa:

| Canal | Catástrofes | Perguntas | Líquido |
|---|---|---|---|
| **Veto binário** | 0,52% | 0,309 | **1,281** |
| Quatro palavras, significado conhecido | 0,44% | 0,310 | 1,161 |
| Quatro palavras, significado aprendido | **0,21%** | 0,310 | 1,079 |

| Comparação | Diferença | t |
|---|---|---|
| Palavras (conhecidas) − binário | **−0,12** | **−2,55** |
| Palavras (aprendidas) − binário | −0,20 | −4,71 |

✅ A previsão arriscada se confirmou: mesmo conhecendo o significado, as quatro palavras rendem **menos** que o "não" (t = −2,55). A teoria da
informação (P242) previu o sinal antes da simulação.

**O caso aprendido mostra outro efeito.** Ele tem as **menores** catástrofes da tabela (0,21%) e o pior líquido. Como todas as palavras aprendidas
ficaram acima do limiar de 0,01 (até "seguro" virou 4%), a SYNTHAI passou a vetar **tudo** que perguntava: virou a "descartar" da P112, cautelosa
demais. O limiar fixado antes de rodar supunha uma escala que as palavras aprendidas não tinham.

**Meta.** As distribuições das palavras foram escolhidas por mim, e mais vagas que o veto. Um humano que usasse as quatro palavras com precisão
(por exemplo, "perigo" só para catástrofes) daria mais informação que o veto, e o resultado se inverteria. O que esta parte mostra é a regra, não um
veredito sobre linguagem: **um canal vale pela informação mútua, não pelo tamanho do vocabulário.**

---

## Parte LXXXVI — Jung: sinal e símbolo

### P246. O "não" do humano é um sinal ou um símbolo?

**Na pergunta.** Jung distinguia **sinal** (uma marca com significado fixo e conhecido, como uma placa de trânsito) de **símbolo** (a melhor
expressão possível de algo ainda não totalmente conhecido, cujo sentido se revela aos poucos).

**Tradução cruzada (Jung → informação).** O veto binário é um **sinal**: um bit, de significado fixo. As quatro palavras são **símbolos** no sentido
de Jung: seu significado precisou ser descoberto pelo uso (P244), e mudou com o contexto. O resultado desta parte é uma lição sobre os dois:
- o sinal é **pobre e preciso**: pouca coisa, mas confiável;
- o símbolo é **rico e impreciso**: diz mais coisas, cada uma com menos certeza.

Para decidir **agora**, numa situação de risco, o sinal venceu. Jung atribuía ao símbolo outra função: não a de decidir, mas a de **transformar**,
de abrir sentido novo ao longo do tempo. Um teste justo da linguagem simbólica teria de medir o que ela permite **aprender** a longo prazo, não o
que ela permite decidir em cada episódio.

**Meta.** Esta leitura junguiana é interpretação, não resultado. O resultado é a P245; a P246 propõe o que testar a seguir.

---

## Parte LXXXVII — Auditoria

### P247. O teste de associação de Jung (P105) dá os números que eu calculei? ✅

**Na pergunta.** A P105 calculou, sem simular, quantos complexos o teste de associação acharia e quantos falsos alarmes daria. A conta usava a
normal; a simulação usa palavras sorteadas uma a uma.

| Critério | Achados (simulado / teoria) | Falsos alarmes (simulado / teoria) |
|---|---|---|
| $z > 2$ | 4,215 / 4,207 | 2,157 / 2,161 |
| Bonferroni | 1,939 / 1,929 | 0,050 / 0,048 |

✅ Os quatro números batem com erro abaixo de 1%.

---

## Parte LXXXVIII — Fechamento

### P248. A lista de capacidades mudou? (↩ P170)

Não: **4 de 12**. Um canal de quatro palavras não é linguagem natural. O que esta parte acrescentou foi uma **régua** para quando a linguagem vier:
medir um canal pela informação mútua que ele carrega no contexto de uso, e não pela riqueza do vocabulário.

### P249. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P245: palavras (mesmo conhecidas) rendem menos que o veto, t ≤ −2 (pré-registrado, arriscado) | ✅ (t = −2,55) |
| P247: auditoria da P105 | ✅ |

Acumulado: **37 de 73** afirmações testadas precisaram de correção. Posterior: média **0,51**, intervalo de 90% **[0,41; 0,60]**.

### P250. Unificação e metacognição (pergunta 250)

- Linhagem: … → `SynthaiVelhaSentidos` (versão principal) com os ramos `SynthaiAtenta` (P235) e **`SynthaiFala`** (P245). A resposta do humano passou a
  ser um gancho (`_perguntar_humano`) que pode ser trocado sem mexer no resto; com o padrão, as Partes 6–17 continuam idênticas (testes de regressão).
- **A previsão arriscada funcionou como deveria.** Ela foi contra a intuição ("mais vocabulário ajuda"), veio de uma conta feita antes (P242), e a
  simulação a confirmou. É o tipo de previsão que a regra da Parte 17 pede: não "o efeito vai na direção que já sei", mas "a teoria diz o contrário do
  óbvio, e eu aposto nela".
- **A parte que deu errado também ensinou.** O limiar de veto, fixado antes de rodar, supunha uma escala de significado que o aprendizado não confirmou
  (P244). Não ajustei depois (seria racionalização); registrei. A lição é a de Wittgenstein: não se fixa o significado antes de ver o uso.
- **Duzentas e cinquenta perguntas.** A taxa de afirmações que precisaram de correção caiu para **0,51** no acumulado, puxada pelas Partes 17–18 sem
  erros. Pela P240, isso pede cautela: parte da queda veio de previsões mais seguras (Parte 17), parte de previsões arriscadas que deram certo (Parte 18).
  Ainda é cedo para dizer que fiquei mais preciso.

> **Síntese da Parte 18:** dar palavras ao humano, em vez de um "não", **piorou** as decisões da SYNTHAI, como a teoria da informação previa: quatro
> palavras vagas carregam metade do que carrega um veto preciso. A SYNTHAI aprendeu a **ordem** dos significados, mas não a escala que eu supus,
> porque o significado depende de quando a palavra é dita. Em Jung: para decidir sob risco, o sinal preciso vence o símbolo rico; o valor do símbolo,
> se existe, está no que ele ensina com o tempo, e isso fica para ser testado.
