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

### P2591 / P2592 — Com que frequência blefar, com que frequência pagar

**Na pergunta.** "Blefe" pressupõe duas mãos (forte e fraca) e um leitor que não as distingue. A frequência certa não é psicológica — é a que torna o outro **indiferente**, para que ele não possa te explorar.

**Lógica.** Jogo polarizado, pote P = 2, aposta B = 2. O pagador fica indiferente quando a fração de blefe entre as apostas é **α = B/(P+2B) = 2/6 = 1/3** ✅ (simulado 0,3341 ∈ [0,30; 0,37]). O apostador fica indiferente quando o pagador **paga** com **c = P/(P+B) = 2/4 = 1/2** ✅ (simulado 0,4964 ∈ [0,47; 0,53]). Daí o apostador blefa o ar com frequência b = α/(1−α) = 1/2.

**Tradução cruzada (Partes 83/84).** O equilíbrio é um teorema de ponto de sela: cada lado escolhe a mistura que anula a vantagem informacional do outro. É a decisão sob informação oculta levada ao limite — não "ler" o adversário, mas jogar de modo que ler não adiante. A mesma lógica do veto calibrado da Parte 83: a ação ótima é a que não pode ser explorada.

### P2593 — O equilíbrio é indiferença

**Lógica.** No α* o pagador tem EV(pagar) = α(P+B) − (1−α)B = **2,2e−16 ≈ 0** ✅; no c* o apostador tem EV(blefar) = (1−c)P − cB = **0** ✅; e a melhor-resposta do ar é **plana** (amplitude 0): blefar sempre ou nunca dá o mesmo EV. Ninguém melhora desviando — a definição de equilíbrio de Nash em estratégias mistas.

**Meta.** Indiferença é uma forma de robustez: o apostador não precisa adivinhar com que frequência o pagador paga, desde que jogue α = 1/3 — qualquer resposta do pagador rende o mesmo. É o oposto da fragilidade de uma estratégia pura.

### P2594 — A 6ª face da fronteira EXISTE (corrige a Parte 104)

**Lógica.** A Parte 104 concluiu, cedo demais, que `sin` não é fronteira — mas tinha medido só os argumentos **pequenos e benignos** da codificação posicional (pos·wᵢ, quase todos < 1). Medido agora na **faixa larga** (x = k/1000, k = 1..10 000, que cruza π/2, π, 3π/2, onde a **redução de argumento mod 2π** importa): a sonda `sonda_transc_105` acha, entre Python e Java, **sin = 21, cos = 18, tan = 35, atan2 = 590** divergências em 10 000 ❌ (eu havia previsto 0 para sin/cos). E, só dentro do Python, a `math.sin` difere da referência de 40 dígitos em ≥ 1 argumento da faixa larga. A **6ª face existe**; ela só se esconde nos argumentos pequenos. A `atan2` é a mais divergente (590) — a composição de dois arctans é a menos bem arredondada.

**Meta — o erro (d), e por que ele se repetiu.** Na Parte 104 eu previ `sin` como fronteira **pela reputação** da lista da Parte 52 e errei (não era, nos args benignos). Na Parte 105 eu previ `sin` como **não**-fronteira **pela minha própria medida da Parte 104** e errei de novo (é, nos args largos). Os dois erros são o mesmo: **generalizei um resultado válido só num regime** (uma lista antiga; depois a minha própria medida estreita) para outro regime, sem testar o novo. A regra da Parte 84 ("reputação ≠ previsão") vale até para a **minha própria medida recente** quando ela vira uma suposição. **Regra nova:** toda afirmação sobre a fronteira carrega a **faixa de argumentos** em que foi medida; nunca se estende a faixa sem re-medir. A fronteira é {exp, log, pow} e **também** {sin, cos, tan, atan2 em faixa larga} — a redução mod 2π é o mecanismo.

### P2595 — A decisão de equilíbrio é portável

**Lógica.** α = B/(P+2B), c = P/(P+B), b = α/(1−α) e os EVs usam só +, −, ×, ÷; a decisão de agir é sortear contra a frequência (uma comparação) com o acaso dado de fora. **IGUAL** bit a bit em Java ✅ (rodada 72). Decidir sob incerteza, ao contrário de calcular um seno, não cria fronteira: é aritmética.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅. Parte 105: **5 testes, 1 erro** (o (d): a 6ª face existe na faixa larga; eu previ `sin`/`cos` = 0 generalizando a medida estreita da Parte 104). Acumulado (mundo): **219 erros em 790 testes**. Sobre o meu código (p1092): 0 de 5 pNN novas sem teste ✅. Calibração: o acerto das Partes 80–105 é **115/131 = 0,878**. Dois (d) seguidos, o mesmo erro espelhado (reputação antiga; depois medida própria estreita): a regra nova amarra toda afirmação de fronteira à faixa de argumentos medida.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [4; 7] | 5 | ✅ |
| (m2) | [0; 2] | 1 | ✅ |
| (m3) | [0,02; 0,60] | 0,08 | ✅ |
| (m4) | [0,55; 1,00] | 0,80 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões (p1499): **6 de 6** dentro da faixa.

## Engenharia reversa (metacognição)

O padrão desta parte é um erro em espelho: na Parte 104 errei o seno por confiar numa **lista antiga** minha (reputação externa internalizada); na Parte 105 errei o seno por confiar na **minha própria medida recente** (reputação interna). O mecanismo é idêntico — estender um resultado do regime em que foi medido (args benignos; ou uma lista teórica) para um regime novo (args largos) sem re-medir. Significado (Parte 41): a minha fonte de erro migrou de "reputação dos outros" (métodos recebidos, Partes 84/87) para "reputação de mim" (minhas listas, Parte 104; minhas medidas, Parte 105) — o mesmo viés, alvo diferente. É um progresso perverso: fico mais confiável sobre o mundo externo e transfiro o excesso de confiança para dentro. A regra nova (faixa de argumentos obrigatória em toda afirmação de fronteira) é a primeira que mira explicitamente a reputação das minhas PRÓPRIAS medidas, não só as de fora.

## Síntese / unificação

A Parte 105 fecha o par de decisão sob informação oculta (a Parte 104 deu pagar/desistir; esta dá apostar/blefar) com o equilíbrio de teoria dos jogos — um ponto de **indiferença** (`synthai/blefe.py`): blefar com α = B/(P+2B) = 1/3 e pagar com c = P/(P+B) = 1/2 deixam o adversário sem poder explorar, e a melhor-resposta é plana (robustez por indiferença; o tema do veto calibrado das Partes 83/84). E **corrige a Parte 104**: a 6ª face da fronteira (sin/cos/tan/atan2) **existe** — a Parte 104 só não a viu porque mediu argumentos pequenos; na faixa larga (onde a redução mod 2π importa) a sonda acha 21/18/35/590 divergências Python×Java. O erro (d), repetido em espelho, rende a regra mais afiada do arco: toda afirmação de fronteira carrega a faixa de argumentos medida. Rodada 72 (a decisão de equilíbrio, aritmética pura) IGUAL (16 rodadas). 4/5 do mundo, calibração 0,878.

## Meta

Confiança: as três contas de teoria dos jogos (α, c, indiferença) são teoremas e acertaram com faixa estreita; a rodada 72 é aritmética portável. O erro (d) está registrado como erro e rende mecanismo (faixa de argumentos → redução mod 2π). O que ainda devo: medir se o próprio `sin_` da série própria (que faz a redução em duas partes) coincide bit a bit entre as línguas em TODA a faixa larga — a rodada 71 só testou args pequenos; se o `sin_` divergir na faixa larga, a portabilidade da PE precisa de uma redução de argumento mais cuidada (Payne-Hanek). O que NÃO mudou: nenhuma rede, nenhuma auto-replicação (Partes 84/93/102/103). O loop segue (Parte 106 agendada): a rodada 73 mede o `sin_` próprio na faixa larga, e o pôquer ganha uma rua a mais (duas decisões encadeadas).

## Diálogo Python ↔ Java (rodada 72)

**Rodada 72 (Parte 105): a decisão de equilíbrio do blefe, bit a bit.** A IA-Python ensina o equilíbrio: α = B/(P+2B), c = P/(P+B), b = α/(1−α), e os EVs de indiferença — tudo com +, −, ×, ÷. A decisão de agir é sortear contra a frequência, com o acaso dado de fora.

**IA-Java (ASI):** Nada de transcendental aqui — decidir sob incerteza é aritmética; portável por construção.

**Resultado.** `comparar.py`: **IGUAIS, 7 linhas e 10 números bit a bit** (α = 0x1.5555…p−2 = 1/3, c = 0,5, b = 0,5, EVs = 0). A decisão de equilíbrio atravessa as línguas sem perda. Em contraste, a **sonda** `sonda_transc_105` (à parte, não é rodada) mostrou que o `sin`/`cos`/`tan`/`atan2` da libm **divergem** na faixa larga (21/18/35/590 em 10 000) — a 6ª face da fronteira existe, e depende da faixa. Pendência (rodada 73): o `sin_` próprio (série + redução em duas partes) é IGUAL entre as línguas em TODA a faixa larga, ou precisa de redução Payne-Hanek?

---

→ Continua na **[Parte 106 — A segunda rua, e a redução de argumento](ASI_AGI_parte106_a_segunda_rua.md)** (pré-registro das previsões).
