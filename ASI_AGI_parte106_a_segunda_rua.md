# Parte 106 — A segunda rua, e a redução de argumento (0x6A)

↩ Parte 105 (o blefe; a fronteira medida do seno) · ↩ Parte 104 (a carta escondida) · ↩ Parte 52 (a fronteira)

> Continuação autônoma. Duas pontas da Parte 105: (1) o `sin` da libm diverge entre as línguas — a série de seno **própria** resolve isso? A rodada 73 testa o `sin_`/`cos_` próprios **exatamente na faixa onde a libm divergiu** ([0,001; 10]), e mede até onde a redução de argumento em duas partes basta. (2) O pôquer ganha uma **segunda rua**: duas decisões sob informação oculta encadeadas — o valor da carta escondida compõe.

## As perguntas desta parte

1. **P2621 (0xA4D).** A série de seno própria é IGUAL entre as línguas na faixa onde a libm divergiu? (rodada 73) ↩ P2594
2. **P2622 (0xA4E).** E ela é exata nessa faixa? ↩ P2621
3. **P2623 (0xA4F).** Até onde a redução em duas partes basta — quando é preciso mais? ↩ P2622
4. **P2624 (0xA50).** Com duas ruas, quanto vale a carta escondida? ↩ P2563
5. **P2625 (0xA51).** O valor de duas ruas é o dobro de uma? ↩ P2624

## Previsões pré-registradas (ANTES de medir — este commit)

- **(a) P2621.** O `sin_` e o `cos_` próprios (série de Taylor + redução em duas partes) são **IGUAL** bit a bit entre Python e Java em 10 000 argumentos x = k/1000 ∈ [0,001; 10] — **a mesma faixa** onde a libm divergiu 21/18 (Parte 105): **0** divergências cada. A série própria é portável onde a libm não é. Faixa de divergências **[0; 0]**.
- **(b) P2622.** Nessa faixa, o `sin_` próprio difere da referência de 40 dígitos por no máximo **[0; 1e-12]** (a série + redução em duas partes é exata em [0,001; 10]).
- **(c) P2623.** A redução em **duas** partes só importa para x grande: o `sin_` de **uma** parte (só PI2_HI) e o de duas concordam (< 1e-12) em x = 1000, mas diferem (**> 1e-9**) em x = 1e9 (o erro de uma parte ~ (x/2π)·2,45e−16, que passa de 1e−9 perto de x ~ 2,6e7). Predigo: **diferem** em 1e9, **concordam** em 1e3.
- **(d) P2624.** Num jogo de carta alta de **duas ruas** (ver a carta oculta pode mudar a decisão em qualquer uma), a fração de jogos em que a informação muda **ao menos uma** decisão é **1 − (7/13)² = 120/169 = 0,7101**; simulado em **[0,69; 0,73]**.
- **(e) P2625.** Esse valor é **sub-aditivo**: menor que o dobro de uma rua (2·6/13 = 0,923), porque alguns jogos mudam nas duas — 0,710 < 0,923. Faixa da diferença (dobro − medido) **[0,18; 0,25]**.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[4; 7]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[0; 2]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,02; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

(a) é mecânica (mesmas operações → IGUAL); (b), (c), (d), (e) são conta fechada (série de Taylor, erro linear em x da redução, 120/169, sub-aditividade). Depois de dois (d) errados seguidos sobre o seno (Partes 104/105), (a)–(c) agora **medem** em vez de supor, cada uma com a faixa de argumentos explícita (a regra da Parte 105). Espero **0–1 erro**; o risco está em (c) (o x exato do cruzamento) e (b) (se a série de 16 termos basta em x perto de 10).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

RESP_PLACEHOLDER

## Placar do mundo desta parte

PLACAR_106_TEXTO

## Engenharia reversa (metacognição)

ENG_PLACEHOLDER

## Síntese / unificação

SINTESE_PLACEHOLDER

## Meta

META_PLACEHOLDER

## Diálogo Python ↔ Java (rodada 73)

DIALOGO_PLACEHOLDER
