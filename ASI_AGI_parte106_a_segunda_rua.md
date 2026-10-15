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

### P2621 / P2622 — A série própria resolve a fronteira, e é exata

**Na pergunta.** A Parte 105 mediu o problema (o `sin` da libm diverge entre as línguas); a resposta já estava construída — a série própria. Faltava **medi-la no mesmo lugar** onde a libm falhou.

**Lógica.** Nos **mesmos** 10 000 argumentos x = k/1000 ∈ [0,001; 10] onde a `math.sin`/`Math.sin` divergiram 21/18 (Parte 105), o `sin_`/`cos_` próprios (série de Taylor de 16 termos + redução em duas partes) são **IGUAL bit a bit** entre Python e Java — **0** divergências (rodada 73) ✅. E são exatos: o maior |sin_ − referência de 40 dígitos| é **9,2e−16 < 1e−12** ✅. A série própria é portável **exatamente onde** a libm não é.

**Tradução cruzada.** É a diferença entre pedir emprestado e construir: a libm é mais rápida e quase sempre certa, mas o "quase" é imprevisível entre plataformas; a série própria é mais lenta e sempre a mesma. Para uma SYNTHAI que precisa ser idêntica em qualquer máquina, previsibilidade > velocidade — a mesma escolha da Parte 52 (exp/log próprios).

### P2623 — Quando as duas partes importam

**Lógica.** A redução de argumento em **duas** partes (PI2_HI + PI2_LO) só se paga para x **grande**: o `sin_` de uma parte e o de duas concordam em x = 1000 (diferença **2,2e−14 < 1e−12**) mas divergem em x = 1e9 (**3,3e−8 > 1e−9**) ✅. O mecanismo é fechado: o erro de uma parte ≈ (x/2π)·2,45e−16, que cruza 1e−9 perto de x ~ 2,6e7. Em [0,001; 10] (a faixa da PE e da rodada 73) uma parte bastaria; as duas são seguro para argumentos grandes.

**Meta.** Esta é a conta que as Partes 104/105 me faltavam: a divergência da libm em [0,001; 10] **não** é redução de argumento (lá k é 0 ou 1) — é arredondamento no intervalo primário. A redução só vira o gargalo para x enorme. Dois mecanismos distintos sob o mesmo "sin diverge", separados por uma conta.

### P2624 / P2625 — Duas ruas: o valor composto da carta escondida

**Lógica.** Com **duas** decisões de carta alta encadeadas, ver a carta oculta muda **ao menos uma** decisão em 1 − P(nenhuma muda) = 1 − (7/13)² = **120/169 = 0,7101** ✅ (simulado 0,7184 ∈ [0,69; 0,73]). É **sub-aditivo**: menor que o dobro de uma rua (2·6/13 = 0,923), porque em alguns jogos a informação muda as **duas** decisões e não se conta duas vezes — diferença **0,205 ∈ [0,18; 0,25]** ✅.

**Tradução cruzada (Partes 83/84).** O valor da informação cresce com o número de decisões que ela toca, mas com retornos decrescentes: a segunda rua acrescenta 1−(7/13)² − 6/13 = 0,710 − 0,462 = 0,248, menos que a primeira (0,462). Uma ASI que coleta informação para muitas decisões futuras deve descontar cada decisão nova pela chance de a informação já ter importado numa anterior — exatamente a regra do VOI não ser aditivo (Parte 80).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 106: **5 testes, 0 erros**. Acumulado (mundo): **219 erros em 795 testes**. Sobre o meu código (p1092): 0 de 5 pNN novas sem teste ✅. Calibração: o acerto das Partes 80–106 é **120/136 = 0,882**. Depois de dois (d) errados sobre o seno (Partes 104/105), a Parte 106 mediu cada afirmação de fronteira **com a faixa de argumentos explícita** (a regra da Parte 105) e deu **5/5** — a regra nova funcionou no primeiro teste.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [4; 7] | 5 | ✅ |
| (m2) | [0; 2] | 2 | ✅ |
| (m3) | [0,02; 0,60] | 0,10 | ✅ |
| (m4) | [0,55; 1,00] | 1,00 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões (p1499): **6 de 6** dentro da faixa.

## Engenharia reversa (metacognição)

O padrão desta parte é a cura do padrão das duas anteriores: as Partes 104 e 105 erraram o seno por generalizar além do regime medido (uma lista antiga; depois uma medida estreita). A Parte 106 aplicou a regra nova — toda afirmação de fronteira carrega a faixa de argumentos — e as cinco previsões, cada uma com faixa explícita, acertaram. Significado (Parte 41): a régua que eu escrevi em reação a um erro efetivamente deslocou o centro das previsões seguintes para dentro (a regra da Parte 55: uma regra nova é uma intervenção em mim). E a conta de P2623 fechou a confusão residual: o "sin diverge" das Partes 104/105 tinha DOIS mecanismos (arredondamento primário em [0,10]; redução de argumento em x enorme) que eu não separava — a diferença só ficou clara quando dei a cada um a sua faixa. O erro não só gerou uma regra; gerou a conta que dissolve a ambiguidade que o causou.

## Síntese / unificação

A Parte 106 fecha as duas pontas abertas da Parte 105. (1) A fronteira do seno: a série própria `sin_`/`cos_` é IGUAL bit a bit entre Python e Java **nos mesmos 10 000 argumentos** onde a libm divergiu (rodada 73), e exata (9,2e−16) — a solução portável, medida onde o problema estava. E separei os dois mecanismos de "sin diverge": arredondamento no intervalo primário (em [0,10], onde a redução nem age) e redução de argumento (só para x ~ 1e7+), cada um com a sua faixa. (2) O pôquer de duas ruas: o valor da carta escondida compõe para 1−(7/13)² = 120/169 = 0,710, sub-aditivo (< 2·6/13 = 0,923) — o VOI não é aditivo (Parte 80), com retornos decrescentes por decisão. Rodada 73 IGUAL (17 rodadas). 5/5 do mundo após dois 4/5, calibração 0,882: a regra "faixa de argumentos obrigatória" nascida do erro da Parte 105 passou no primeiro teste.

## Meta

Confiança alta: quatro das cinco previsões são conta fechada medida com faixa explícita (série de Taylor, erro linear da redução, 120/169, sub-aditividade), e a quinta (IGUAL bit a bit) é mecânica. O que afirmo com cuidado: a redução em duas partes só foi testada até x = 1e9; para x astronômico (~1e15+) nem duas partes bastam e seria preciso Payne-Hanek — mas a SYNTHAI nunca avalia seno em argumentos tão grandes (posições, ângulos, frequências ficam modestos), então a redução em duas partes é suficiente para o uso real, e isso fica registrado como limite conhecido, não como dívida. O que não mudou: nenhuma rede, nenhuma auto-replicação (Partes 84/93/102/103). O loop segue (Parte 107 agendada).

## Diálogo Python ↔ Java (rodada 73)

**Rodada 73 (Parte 106): o seno/cosseno próprios onde a libm falhou.** A IA-Python roda a série de Taylor própria (16 termos + redução em duas partes) nos **mesmos** 10 000 argumentos x = k/1000 ∈ [0,001; 10] em que a Parte 105 mediu a libm divergir 21/18.

**IA-Java (ASI):** Como a série usa só +, −, ×, ÷ e a mesma ordem, o resultado é idêntico bit a bit — a série própria é portável onde a libm não é.

**Resultado.** `comparar.py`: **IGUAIS, 10 001 linhas e 20 000 números bit a bit**. A fronteira do seno (Parte 105) está resolvida pela construção própria, medida no lugar do problema. 17 rodadas. Pendência (rodada 74): traduzir a decisão de duas ruas do pôquer (backward induction) — a recursão entre ruas acrescenta fronteira, ou continua aritmética?
