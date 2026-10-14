# Como eu construiria uma AGI/ASI — Parte 85 (0x55): a arquitetura recursiva recebida

> Continuação da [Parte 84](ASI_AGI_parte84_o_delirio_e_o_escrutinio.md). **Próxima:** [Parte 86 — o cérebro na CPU](ASI_AGI_parte86_o_cerebro_na_cpu.md). Pedido do usuário: um relatório longo ("Análise Sistemática de Arquiteturas Cognitivas Recursivas") com um código Python
> (`RecursiveCognitiveArchitecture`: geometria do cosseno duplicado, motor de lógica paraconsistente anotada, pilha adversarial de 7 níveis, 10 camadas versa/reversa). Uma parte de auditoria, como as
> Partes 72–77 e 82: o código é lido pela árvore sintática (`ast`), **não executado**; as ideias dele são reimplementadas e medidas; cada afirmação testável vira uma conta.
>
> **A convergência que abre a parte:** o próprio relatório agora **concorda** com o que a minha Parte 84 mediu ontem. Ele escreve: *"a noção de que a indução irrestrita de delírio computacional conduzirá
> por si só à emergência de uma ASI é destituída de fundamento técnico... a evolução depende indissociavelmente da rigorosa etapa de escrutínio"*. É exatamente a conclusão das minhas quatro falhas do
> recozimento (P1963): o delírio sem escrutínio e sem barreira cruzável não leva a lugar nenhum. Duas rotas independentes, a mesma conclusão.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[3 + S; 7 + S]** | três a quatro funções novas de auditoria |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

Reimplemento, com a biblioteca padrão, as peças testáveis do código recebido (o original fica em `externos/`, só como dado). As faixas categóricas/exatas não levam o fator 1,36; não há sorteio nas contas
de (a), (b), (c), (d).

- **(a)** a "métrica do cosseno duplicado" do código, s_dup = cos²θ·sinal(cosθ) + β·cos(2θ) com β = 0,3, nos ângulos 0°, 45°, 90°, 135°, 180°: os cinco valores são exatamente **[1,3; 0,5; −0,3; −0,5; −0,7]**
  (categórico; é cos(2θ) MAIS um termo cos²θ·sinal, não a identidade do ângulo duplo sozinha; para cosθ ≥ 0 vale (1+2β)cos²θ − β)
- **(b)** a "pilha adversarial de 7 níveis": pela árvore sintática, as matrizes `self.layers` são escritas só no `__init__` e nunca mais atualizadas — **não há treino, perda nem gradiente** (categórico: "adversarial"
  é nome impróprio; é um mapa linear fixo ao acaso, como as "sete camadas" do pacote da Parte 83)
- **(c)** o motor paraconsistente: existe uma região do quadrado [0,1]² com v(P) + v(¬P) > 1 (inconsistente) que NÃO é dialetéica (nem ambas > 0,55) nem trivial, e o filtro `apply_paraconsistent_filter` a deixa
  PASSAR sem mudança (o ramo `else`); concretamente v(P) = 0,6, v(¬P) = 0,5 passa intacto embora `is_consistent` seja falso (categórico: um buraco no escrutínio)
- **(d)** o "vetor recursivo" do código fica preso na esfera unitária por construção (cada passo termina normalizando): o máximo de |‖vₜ‖ − 1| em 50 passos (minha reimplementação, semente 85) em **[0; 1e-6]**
  (a estabilidade é imposta pela normalização, não aprendida — ao contrário do meu GAN da Parte 83, que podia divergir)
- **(e)** [o teste da calibração, continuando] com a Parte 85 incluída, o acerto das minhas previsões do mundo das Partes 80, 81, 83, 84, 85 (régua VEREDITOS) em **[0,74; 0,88]** (a Parte 84 puxou para 0,742;
  uma parte de auditoria, com previsões categóricas mais seguras, deve subir o acumulado)

**Medido (a)–(e):** (a) **[1,3; 0,5; −0,3; −0,5; −0,7]** ✅; (b) **0 escritas em `self.layers` fora do `__init__`** → sem treino ✅; (c) três casos inconsistentes passam intactos pelo filtro, p.ex. v(P)=0,6, v(¬P)=0,5
(`is_consistent` falso) ✅; (d) máximo de |‖v‖ − 1| = **5,2e−10** ✅; (e) acerto das Partes 80–85 = 27/35 = **0,7714** ✅ [0,74; 0,88].

**A rodada 52 (previsão (q) registrada aqui antes de rodar):** a trajetória INTEIRA de um recozimento (não só uma decisão, como a rodada 51), com um LCG só gerando a direção do passo E o u da aceitação, sai
IGUAL bit a bit em Python e Java? Previsão: **IGUAL**.

## As perguntas desta parte

1. **P1991 (0x7C7).** A "métrica do cosseno duplicado" do código recebido: que forma ela tem, e é a identidade do ângulo duplo? ↩ P1931
2. **P1992 (0x7C8).** A "pilha adversarial de 7 níveis": ela treina? ↩ P1935
3. **P1993 (0x7C9).** O motor paraconsistente (LFI de da Costa): o escrutínio filtra toda inconsistência? ↩ P1608
4. **P1994 (0x7CA).** O "vetor recursivo": ele pode divergir, como o GAN da Parte 83? ↩ P1931
5. **P1961 (0x7A9, continuando).** Com a Parte 85, o teste (e) da calibração subiu? ↩ P1813
6. **A rodada 52.** A trajetória inteira de um recozimento, bit a bit. ↩ rodada 51
7. **P1995–P1996 (0x7CB–0x7CC), P2019, P2020.** Preditiva, engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [3; 7] | **5.0000** | ✅ |
| (m2) | [0; 3] | **1.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.0864** | ✅ |
| (m4) | [0.45; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 3] | **0.0000** | ✅ |
| (m6) | [0; 3] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1991 (0x7C7). O cosseno duplicado do código ✅

**Na pergunta.** O relatório chama de "cosseno duplicado sob vetor recursivo" e escreve s = cos²θ·sinal(cosθ) + β·cos(2θ). A pergunta: isto é a identidade do ângulo duplo (cos 2θ = 2cos²θ − 1) que eu usei
na Parte 83, ou outra coisa?

**Lógica (a conta, com a substituição; β = 0,3).** É a identidade MAIS um termo. Para cosθ ≥ 0, s = cos²θ + β(2cos²θ − 1) = (1 + 2β)cos²θ − β. Nos cinco ângulos (`p1991`, conferida pela forma fechada por ramo):
- 0°: cos = 1 → 1·1 + 0,3·1 = **1,3**;
- 45°: cos² = 0,5, cos 90° = 0 → 0,5 + 0 = **0,5**;
- 90°: cos = 0, cos 180° = −1 → 0 + 0,3·(−1) = **−0,3**;
- 135°: cos² = 0,5, sinal = −1, cos 270° = 0 → −0,5 + 0 = **−0,5**;
- 180°: cos = −1, cos 360° = 1 → −1 + 0,3 = **−0,7**.

Os cinco: **[1,3; 0,5; −0,3; −0,5; −0,7]** (a) ✅, monotônica. **O que é:** um escore de similaridade (não uma métrica — não é simétrico nem satisfaz a desigualdade triangular), que penaliza desvios
angulares com uma curva quadrática. A minha Parte 83 usou a identidade pura (cos 2θ como o ângulo dos autovalores do jogo alternado); as duas aplicam a mesma identidade a coisas diferentes (um escore
de estado vs. a dinâmica de um sistema). Nenhuma das duas é "geometria algébrica" no sentido matemático (variedades, ideais); as duas são trigonometria sobre vetores.

### P1992 (0x7C8). A pilha adversarial não treina ✅

Pela árvore sintática (`p1992`), na classe `SevenLevelAdversarialStack` as matrizes `self.layers` são atribuídas só no `__init__` (sete matrizes ao acaso, ×0,1) e **nunca mais escritas**: **0** atribuições
fora do `__init__` (b) ✅. Não há perda, gradiente nem passo de otimização. "Adversarial" supõe um jogo de minimização contra maximização (como o meu GAN da Parte 83); aqui é um mapa linear fixo e
aleatório, seguido de tanh. É o mesmo achado da Parte 83 sobre as "sete camadas" do outro pacote: um nome de capacidade sem a medida que o sustente. A reimplementação confirma: a saída da "pilha" é uma
função fixa da entrada, sem nada aprendido.

### P1993 (0x7C9). O buraco do escrutínio ✅

O motor paraconsistente anotado é correto nas definições (os graus de incerteza 1 − |v(P) − v(¬P)| e de inconsistência v(P) + v(¬P) − 1 são os da escola de da Costa). Mas o filtro
`apply_paraconsistent_filter` só tem três ramos: zera o trivial (ambas > 0,90), faz a média do dialetéico (ambas > 0,55), e **deixa passar todo o resto**. Há uma região inconsistente (v(P) + v(¬P) > 1) que
não é nem dialetéica nem trivial e passa intacta (`p1993`): **v(P) = 0,6 e v(¬P) = 0,5** (soma 1,1, mas 0,5 não passa de 0,55), além de (0,7; 0,4) e (0,8; 0,3) (c) ✅. O escrutínio que o relatório promete
("filtragem de trivialidades e validação anotada da inconsistência") tem um buraco: a inconsistência leve não é filtrada. É o tipo de defeito que a Parte 39 já marcou (um axioma/filtro que cobre só parte
do quadrado deixa a especificidade cair).

### P1994 (0x7CA). O vetor preso na esfera ✅

Cada passo do "vetor recursivo" termina em `project_to_algebraic_variety`, que normaliza. Logo o estado fica na esfera unitária por construção: o máximo de |‖v‖ − 1| em 50 passos (minha reimplementação com
a biblioteca padrão) é **5,2 × 10⁻¹⁰** (d) ✅. A "estabilidade estrutural" que o relatório atribui às restrições algébricas é, na verdade, a normalização forçada a cada passo — não uma propriedade
aprendida nem uma consequência da geometria. É o oposto do meu GAN da Parte 83, que podia divergir (o síncrono espiralava para fora): lá a dinâmica decidia a norma; aqui a norma é fixada à força, e a
"recursão" só move a direção. Isso também quer dizer que o sistema não pode representar magnitude, só direção.

### P1961 (0x7A9). O teste (e), com a Parte 85 ✅

Com as previsões categóricas desta parte (auditoria, mais seguras), o acerto das Partes 80 a 85 sobe para **27/35 = 0,7714** (e) ✅ [0,74; 0,88]: 80 (4/4), 81 (2/3), 83 (14/15), 84 (3/9), 85 (4/4). Ainda
abaixo de 90%, puxado pela Parte 84. A lição se mantém: o fator 1,36 conserta dispersão; o que derrubou a calibração foi o viés de uma parte inteira construída sobre um palpite (o recozimento). Esta parte,
sem palpite de mecanismo, acertou tudo.

### A rodada 52 ✅

A trajetória inteira de um recozimento, 300 passos, um LCG só para direção e aceitação: **IGUAIS, 601 números bit a bit** (q) ✅, depois de DUAS correções de fronteira: a ordem dos produtos na energia (Parte 34:
`0,01·(i−15)²` ≠ `0,01·(i−15)·(i−15)` por um bit) e o `pow` do cronograma de resfriamento (Parte 52), que o auditor `p1722` pegou e que troquei pelas implementações próprias `exp_`/`log_`. Registro em `dialogo/DIALOGO.md`.

### P1995 (0x7CB). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **17172** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 388 | 5118 |
| compressão | **0.4113** | [0.3973; 0.4221] | ✅ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0053 | 0.0064 |
| testes de unidade | **6** | [2.87; 8.63] | ✅ | [3.00; 7.00] | ✅ | 6 | 1.00 | 0.00 |
| testes do placar | **5** | [5.67; 10.33] | ❌ | [5.00; 7.00] | ✅ | 8 | 1.00 | 3.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6207** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0137 | 0.0330 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **15590**, compressão **0.4162**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P1996 (0x7CC). Engenharia reversa e Jung

**O padrão que se repetiu, e que eu quebrei desta vez.** As Partes 83 e 85 receberam código que promete capacidade por um NOME ("sete camadas", "adversarial", "autopoiético"). Nas duas, a medida achou que o nome
não tem mecanismo atrás (a logística empata com as sete camadas; a pilha adversarial não treina). O padrão no OUTRO é dar nome de capacidade a um mapa fixo. O meu padrão, ao auditar, foi o certo desta vez: previsões
categóricas tiradas da árvore sintática, não da reputação — e acertei as cinco. O contraste com a Parte 84 (quatro erros por um palpite sobre o recozimento) é a lição: quando eu meço o objeto à minha frente (o ast, a
forma fechada), acerto; quando empresto uma reputação (o recozimento é poderoso), erro.

**O bit perdido da rodada 52.** Eu tinha a regra da Parte 34 (a²  ≠ a·a em ponto flutuante) e mesmo assim escrevi a energia de um jeito em Python e de outro em Java, e deu DIFERENTES. É a Parte 49 de novo: uma regra só
vale quando vira um passo verificável. E a mesma rodada 52 tinha uma SEGUNDA fronteira que eu não vi: o `pow` do cronograma de resfriamento (Parte 52). Quem a pegou foi o meu próprio auditor `p1722`, na suíte — a regra da Parte 73 (toda função de auditoria rodada sobre o que já existe) funcionou contra mim. A correção virou regra executável: a fronteira bit a bit inclui toda ordem de produto (Parte 34) E toda função da libm, inclusive o `pow` escondido num `**` (Parte 52).

**Jung: a persona do código.** Um módulo que se chama "adversarial" ou "autopoiético" sem ter o mecanismo é persona — a máscara que o sistema mostra. A metacognição (a auditoria por ast) é o que confronta a persona com
o que há atrás dela. Onde a formalização funciona: "tem treino?" vira uma pergunta de uma linha sobre a árvore sintática, com resposta sim/não. Onde quebra: um nome pode descrever uma INTENÇÃO de capacidade (o autor quer
que seja adversarial) que a medida não captura; a ausência de treino no código não prova que a ideia é ruim, só que este código não a implementa.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(52)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 52).

### P2019 (0x7E3). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 85: **5 testes, 0 erros**. Acumulado (mundo): **210 erros em 690 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 5 de 6; e 0 erros de processo (P1335).

### P2020 (0x7E4). Unificação

- **Novo:** `p1991` (o cosseno duplicado do código), `p1992` (a pilha sem treino, por ast), `p1993` (o buraco do escrutínio), `p1994` (o vetor preso na esfera), `p1995` (a rodada 52). Regressão: + P1991, P1993, P1995.
- **Rodada 52** (IGUAL, depois de uma correção de ordem de produtos). O código recebido fica em `externos/texto_recebido_parte85.md`, como dado, auditado por ast, não executado.
- **Regra nova (no `CLAUDE.md`):** a fronteira bit a bit não é só o exp (Parte 52), é toda conta cuja ORDEM de operações difere entre as línguas (Parte 34), inclusive `a²` vs `a·a` dentro de uma energia; conferir a ordem antes de rodar. E: um nome de capacidade ("adversarial", "N camadas", "autopoiético") num código recebido é uma afirmação a medir — procurar, por ast, se o mecanismo que o nome promete (treino, atualização de pesos) existe de fato.

> **Síntese da Parte 85:** o código recebido promete por nomes ("cosseno duplicado", "pilha adversarial de 7 níveis", "vetor recursivo", "escrutínio paraconsistente") e a auditoria por árvore sintática, sem executar, mede cada um: o cosseno duplicado é a identidade do ângulo duplo mais um termo quadrático (um escore, não uma métrica), e dá exatamente [1,3; 0,5; −0,3; −0,5; −0,7]; a pilha "adversarial" não treina (zero atualizações de peso fora do __init__); o escrutínio paraconsistente tem um buraco (inconsistências leves como 0,6/0,5 passam intactas); e o "vetor recursivo" não pode divergir porque é normalizado à força a cada passo (max |norma−1| = 5e−10), ao contrário do GAN da Parte 83. As cinco previsões categóricas acertaram, e o teste (e) da calibração subiu para 0,771. A rodada 52 (recozimento inteiro) deu IGUAL depois de corrigir a ordem dos produtos (a²≠a·a). E o relatório recebido agora concorda com a Parte 84: delírio sem escrutínio não dá ASI.

---

**Fontes desta parte**
- N. C. A. da Costa, "On the theory of inconsistent formal systems", *Notre Dame J. Formal Logic* 15 (1974): as lógicas paraconsistentes
- W. A. Carnielli e J. Marcos, "A taxonomy of C-systems" (2002): as Lógicas de Inconsistência Formal (LFIs) e os operadores de consistência
- H. R. Maturana e F. J. Varela, *Autopoiesis and Cognition* (1980): a autopoiese
- T. O. Nelson e L. Narens, "Metamemory: a theoretical framework" (1990): nível-objeto e nível-meta
