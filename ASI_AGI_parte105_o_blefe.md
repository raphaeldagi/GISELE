# Parte 105 — O blefe: o equilíbrio de indiferença, e a fronteira medida do seno (0x69)

↩ Parte 104 (a carta escondida; a fronteira do seno) · ↩ Partes 83/84 (decisão sob incerteza, veto) · ↩ Parte 52 (a fronteira)

> Continuação autônoma. A Parte 104 deu a decisão de **pagar ou desistir** (um lado só). O blefe fecha o par: o apostador também decide **apostar com uma mão fraca ou desistir**. O equilíbrio de teoria dos jogos é um ponto de **indiferença** — cada lado joga uma mistura que deixa o outro sem poder melhorar. É a forma mais pura do tema das Partes 83/84 (decidir sob o que o outro esconde). E a rodada 72 mede, em 10 000 argumentos, se a 6ª face da fronteira (sin/cos/tan/atan2) existe de verdade — a pendência da Parte 104.

## As perguntas desta parte

1. **P2591 (0xA23).** No jogo de blefe polarizado, com que frequência blefar? ↩ P2563
2. **P2592 (0xA24).** Com que frequência pagar (defender), para que blefar não compense? ↩ P2591
3. **P2593 (0xA25).** O equilíbrio é mesmo um ponto de indiferença (ninguém melhora desviando)? ↩ P2592
4. **P2594 (0xA26).** A 6ª face da fronteira existe? sin/cos/tan/atan2 em 10 000 argumentos, Python × Java (rodada 72) ↩ P2564
5. **P2595 (0xA27).** A decisão de equilíbrio (a mistura) é portável bit a bit? (rodada 72, lado do diálogo) ↩ rodada 71

## Previsões pré-registradas (ANTES de medir — este commit)

Jogo polarizado meia-rua: pote P = 2 (cada um apostou 1), aposta B = 2 (do tamanho do pote). O apostador tem os nuts (ganha sempre) ou ar (perde sempre); o pagador tem um "pega-blefe" (ganha do ar, perde para os nuts).

- **(a) P2591.** A fração de **blefe** entre as apostas que deixa o pagador indiferente é **α = B/(P+2B) = 1/3**; melhor-resposta simulada em **[0,30; 0,37]**, forma fechada **1/3 = 0,3333**. Risco: fora de [0,30; 0,37] refuta.
- **(b) P2592.** A frequência de **pagar** (defesa mínima) que deixa o blefe sem lucro é **c = P/(P+B) = 1/2**; simulada em **[0,47; 0,53]**, forma fechada **0,5**. Risco: fora de [0,47; 0,53] refuta.
- **(c) P2593.** No equilíbrio, os dois ficam **indiferentes**: |EV(pagar) − EV(desistir)| e |EV(blefar) − EV(desistir)| ambos **< 1e-9** (conta fechada do ponto de sela). Faixa **[0; 1e-9]**.
- **(d) P2594.** A `sin` e a `cos` da libm concordam entre Python e Java em **10 000** argumentos (0 divergências cada — confirma a Parte 104); e **pelo menos uma** de {`tan`, `atan2`} diverge em **≥ 1** argumento (a 6ª face existe nas trigonométricas mais difíceis). Risco: sin/cos com ≥1 divergência refuta a 1ª parte; tan e atan2 ambos 0 refutam a 2ª (e aí a família trig inteira sai da lista da fronteira — resultado negativo limpo).
- **(e) P2595.** A decisão de equilíbrio (sortear apostar/pagar pela mistura, com o acaso dado de fora) é **IGUAL** bit a bit em Java (só +, −, ×, ÷ e comparações — nenhuma transcendental; rodada 72).

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[4; 7]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[0; 2]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,02; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

(a), (b), (c) são conta fechada de teoria dos jogos (α = B/(P+2B), c = P/(P+B), ponto de sela); (e) é a fronteira já estabelecida (arithmetic-only → portável). O risco real está em (d): a 2ª parte é uma aposta de que `tan` ou `atan2` diverge — pode dar errado se o par de plataformas for muito bem casado (como o `sin` da Parte 104). Espero **0–1 erro**, e se houver, será em (d).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

RESP_PLACEHOLDER

## Placar do mundo desta parte

PLACAR_105_TEXTO

## Engenharia reversa (metacognição)

ENG_PLACEHOLDER

## Síntese / unificação

SINTESE_PLACEHOLDER

## Meta

META_PLACEHOLDER

## Diálogo Python ↔ Java (rodada 72)

DIALOGO_PLACEHOLDER
