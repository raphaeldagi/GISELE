# Como eu construiria uma AGI/ASI — Parte 45 (0x2D): a hipótese mais pesada, e a crença errada mas modesta

> Continuação da [Parte 44](ASI_AGI_parte44_o_nivel_certo.md). **Próxima:** [Parte 46 — a resposta é a pergunta](ASI_AGI_parte46_a_resposta_e_a_pergunta.md) (P821–P850). O modelo de mudança no nível do mundo venceu no mundo que muda (231,5) e cobrou no
> estável (44,7), porque as hipóteses jovens, sorteadas pelo peso, reexploravam tudo. A pergunta da Rodada 15 era: dá para guardar o ganho sem o custo?
> A resposta da teoria da decisão é **decidir pelo máximo a posteriori** da idade do mundo (a hipótese mais pesada), em vez de sortear. Esta parte testa
> isso, mede pela primeira vez a **calibração** das minhas faixas, e segue a trilha do dicionário na profundidade da taxonomia.
>
> Novidades: `ThompsonBOCPDGlobalMAP` ([`synthai/decisao.py`](synthai/decisao.py)); testes em [`synthai/testes_parte45.py`](synthai/testes_parte45.py);
> números de `p791_...` a `p793_...` em [`calculos.py`](calculos.py). **Centros e previsões no commit `f228660`, antes de rodar.**

---

## As perguntas desta parte

1. **P791 (0x317).** Decidir pela hipótese mais pesada guarda o ganho e tira o custo? ↩ P761
2. **P792 (0x318).** As minhas faixas estão calibradas? (o viés e a escala) ↩ P700
3. **P793 (0x319).** Em que profundidade da taxonomia moram os animais, os artefatos e os grupos? ↩ P763
4. **P794 (0x31A).** Engenharia reversa: a crença errada mas modesta.
5. **P795 (0x31B).** Jung: a ilusão que não se desfaz.
6. **P796 (0x31C).** O diálogo, rodada 16.
7. **P819 (0x333).** Placar. **P820 (0x334).** Unificação.

---

### P792 (0x318). As minhas faixas estão calibradas? (descritivo, e uma hipótese testada)

**Na pergunta.** "Calibradas" tem duas partes: a escala (a largura certa) e o centro (sem viés). Uma faixa de 90% com meia-largura relativa w tem
meia-largura 1,645σ, então z = (medido − centro)/(centro·w/1,645) deve ser ~N(0, 1).

**Lógica.** Nas 17 previsões de comportamento feitas com a regra (Partes 42–44): **média de z = +0,38** (t = 1,47), **desvio de z = 1,07**, **2 de 17**
fora de ±1,645 (12%; o esperado é 10%). A escala está calibrada (desvio ≈ 1). O centro tende a ficar **abaixo** do medido.

**A hipótese que isso pede, testada nesta parte (d).** Os mecanismos que eu esqueço (as hipóteses jovens, a dispersão do começo, a confusão de nível)
são todos **custos** a mais: eu esqueço o que custa, não o que ajuda. Se for assim, os medidos ficam acima dos centros. Previsão (d): pelo menos 2 dos 3
medidos desta parte acima dos centros. **3 de 3** ✅ (z = +0,30, +0,33, +9,52). Ao acaso (meio a meio), 2 ou mais de 3 tem chance de ½; 3 de 3, de 1/8.

**Significado.** O meu viés tem direção, e a direção diz o que eu vejo mal: **o custo do que não está na conta principal**. Eu deduzo o mecanismo de
interesse e esqueço o atrito. A correção prática é deslocar os centros de comportamento para cima em ~0,4σ, ou, melhor, listar os custos de cada
mecanismo antes de prever (a regra 2 da P700, agora com o sinal conhecido).

### P791 (0x317). Decidir pela hipótese mais pesada (pré-registrado) ✅✅❌

**Na pergunta.** Sortear uma hipótese pelo peso (a amostragem de Thompson sobre a idade do mundo) dá voz às jovens; decidir pela mais pesada dá voz só
a quem a evidência já elegeu. É a mesma troca da P643 (seguir o maior peso na mistura de riscos), um nível acima.

**Lógica, os centros antes (p791_contas).**
- **Estável:** a velha é sempre a mais pesada; é o exato com um começo um pouco mais lento: 30,7 + 1 = **31,7**.
- **Muda:** a hipótese nascida na troca passa a velha quando a evidência vence ln(1/H) = ln 500 = 6,2 nats; com ln 5 = 1,6 nat por fracasso do braço que
  era bom, ~4 fracassos, ~6 puxadas. Sem as jovens sorteadas no meio das fases, o global (231,5) perde o excesso do estável, (44,7 − 30,7) por 2000
  passos, 28 em 4000: 231,5 − 28 = **203,5**.
- **Dano:** o lixo seria desmentido em ~4 fracassos, como a mudança: **12**.

| mundo | centro | faixa | **medido** | z | o melhor anterior |
|---|---|---|---|---|---|
| estável | 31,7 | [26,2; 37,2] | **32,7** | +0,30 | 30,7 (exato) |
| muda a cada 500 | 203,5 | [151,0; 256,0] | **214,2** | +0,33 | 231,5 (global sorteado) |
| dano, custo | 12,0 | [7,9; 16,1] | **35,9** | **+9,52** | 14,1 (γ 0,99) |

(a) ✅ (b) ✅ (c) ❌.

**O ganho.** A decisão pela mais pesada guardou o ganho do nível certo e tirou o custo: **214,2** no mundo que muda (o melhor da série; o global sorteado
fez 231,5, a surpresa 367,7) e **32,7** no estável (a 2 do exato, que fez 30,7). É o primeiro agente da série que é bom nos dois mundos ao mesmo tempo.

**O erro, e o mecanismo esquecido (P794).** No dano, **35,9**: z = +9,5, a previsão mais errada desde que a regra das faixas existe.

### P793 (0x319). A profundidade da taxonomia (pré-registrado) ✅✅

Profundidade média (hiperônimos até a raiz): **animais 12,94** (4.016), **artefatos 8,73** (10.698), **grupos taxonômicos 7,17** (5.425), todos os
substantivos **7,96** (82.115). (e) animais − artefatos = 12,94 − 8,73 = **4,20**, em [1,4; 6,6] ✅; (f) grupos mais rasos que animais ✅.

**Significado.** Um animal está, em média, 13 passos abaixo da raiz: *cão → canino → carnívoro → placentário → mamífero → vertebrado → cordado → animal →
organismo → ser vivo → todo → objeto → entidade física → entidade*. O grupo taxonômico que o classifica (*Canidae*) está a 7: o nome da família mora quase
6 níveis **acima** dos seus membros, num outro ramo (o da abstração). A confusão de níveis da Parte 43 tem um tamanho: ~6 degraus da taxonomia.

### P794 (0x31A). Engenharia reversa: a crença errada mas modesta

A conta do dano usou a velocidade de evidência da mudança do mundo: ln 5 = 1,6 nat por fracasso, porque, na mudança, a crença velha era **confiante**
(previa ~0,9 de sucesso no braço bom). O lixo do dano é diferente: contagens ao acaso em 1..20, médias entre 0,05 e 0,95, muitas perto de ½. A evidência que
separa duas hipóteses, por observação, é a **divergência de Kullback–Leibler** entre o que elas preveem para aquela observação. Uma crença de lixo que prevê
0,45 e a crença inicial, que prevê 0,5, quase não se distinguem: KL(0,45 ∥ 0,5) = 0,45 ln(0,45/0,5) + 0,55 ln(0,55/0,5) = −0,0474 + 0,0524 = **0,005 nat**
por observação. Para vencer ln 500 = 6,2 nats, seriam ~1.200 observações. A hipótese velha (o lixo) segue sendo a mais pesada por centenas de passos.

**O significado.** *Uma crença errada mas modesta é a mais difícil de desmentir.* A crença confiante e errada é desmentida depressa (cada fato a contradiz
com força); a modesta e errada prevê quase o mesmo que a ignorância, e a evidência não a separa da ignorância. Para a SYNTHAI isso explica a tabela das
Partes 37–45: o mundo que muda (crenças confiantes que ficam erradas) é resolvido pela evidência; o dano (crenças modestas e erradas) só é resolvido pela
**exposição**, que vai testar diretamente o braço desacreditado (19,5 na P521). É a pergunta da Rodada 17: juntar os dois.

**O padrão nos meus erros.** É a quarta vez que eu deduzo uma velocidade de detecção supondo a evidência da última conta que fiz (aqui, ln 5 por fracasso)
sem calcular a KL do caso. Regra nova: **ao deduzir quanto tempo a evidência leva, calcular a KL entre as previsões das hipóteses, para o caso em
questão.**

### P795 (0x31B). Jung: a ilusão que não se desfaz

Jung observou que as convicções mais resistentes não são as mais intensas, mas as que **se parecem com a realidade**: a meia-verdade é mais estável que a
mentira grossa, porque a experiência quase não a contradiz. A P794 é isso em números: KL = 0,005 nat por observação entre o lixo modesto e a ignorância.
**Onde funciona:** a resistência de uma crença à experiência é a KL entre o que ela prevê e o que a alternativa prevê. **Onde quebra:** em Jung, a meia-verdade
resiste também por defesa (ela protege algo); aqui ela resiste só por ser pouco informativa.

### P796 (0x31C). O diálogo, rodada 16

A decisão pela mais pesada em Java: **21 números idênticos** (h) ✅; a virada no passo **632**, na borda da faixa da IA-Python [598; 632] (g) ✅. A conta da
IA-Java para o atraso: vencer ln 50 = 3,91 nats com ln(0,5/0,2) = 0,92 nat por sucesso do braço que mudou. Placar por voz desde a Rodada 13: **IA-Java 4 em
4, IA-Python 3 em 4**.

### P819 (0x333). Placar

(a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅. Parte 45: 8 testes, 1 erro. Acumulado: **134 erros em 379 testes**; taxa média 0,35, intervalo 90% [0,31;
0,39], a menor da série.

### P820 (0x334). Unificação e metacognição

- **Novo:** `ThompsonBOCPDGlobalMAP` (2 testes; 120 no pacote): **o agente de decisão principal para mundos que podem mudar** (32,7 estável, 214,2 que muda,
  35,9 dano). A versão principal do agente unificado continua a `SynthaiComposta`; o módulo novo é o candidato a substituir o Thompson dela onde o mundo
  pode mudar. Regressão: + P792 (desvio de z 1,07).
- **Regra nova:** ao deduzir a velocidade da evidência, calcular a KL do caso.

**Metacognição.** A calibração (P792) é a primeira medida que mostra não só **quanto** eu erro, mas **para que lado**: os meus centros ficam abaixo do
medido, porque eu esqueço os custos. E o erro desta parte (z = +9,5) é exatamente desse lado: esqueci o custo da crença modesta, que a evidência não
desmente.

> **Síntese da Parte 45:** decidir pela hipótese mais pesada sobre a idade do mundo fez o melhor agente da série no mundo que muda (214,2) sem pagar no
> estável (32,7, a 2 do exato): é o primeiro agente bom nos dois mundos. No dano ele custou 35,9, longe dos 12 previstos, porque uma crença errada mas
> modesta prevê quase o mesmo que a ignorância (KL de 0,005 nat por observação) e a evidência não a derruba: só a exposição a testa. A calibração das minhas
> faixas mostrou escala certa (desvio de z 1,07) e um viés com direção (centros abaixo do medido, porque eu esqueço os custos), confirmado nesta parte (3 de 3
> acima). Na taxonomia, um animal mora 13 degraus abaixo da raiz e o nome da sua família, 7, noutro ramo.

---

**Fontes desta parte**
- Detecção bayesiana de mudança e o MAP da idade: [Adams e MacKay, arXiv 0710.3742](https://ar5iv.arxiv.org/html/0710.3742)
- A divergência de Kullback–Leibler como taxa de evidência (o expoente de Chernoff–Stein): a conta está na própria resposta (KL(0,45 ∥ 0,5) = 0,005 nat)
- A taxonomia do WordNet (profundidades): conferida no data lake
