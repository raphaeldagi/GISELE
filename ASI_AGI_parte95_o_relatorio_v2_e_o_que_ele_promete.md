# Como eu construiria uma AGI/ASI — Parte 95 (0x5F): o relatório "v2.0" e o que ele promete

> Continuação da [Parte 94](ASI_AGI_parte94_o_mundo_que_nao_e_linear.md). Chegou no meio do ciclo um **relatório recebido** ("SYNTHAI v2.0") com quatro mecanismos e uma tabela de benchmarks espetaculares. Regra da Parte 72/85/88: **não
> executo o código recebido**; audito pela árvore sintática (AST), reimplemento as IDEIAS do zero em biblioteca padrão (`synthai/evoluido.py`), meço o que o relatório **afirma sobre mecanismo** (verificável) e **não pontuo** os benchmarks
> que não posso checar (regra da Parte 86). A auditoria confiável compara o texto com o SEU PRÓPRIO comportamento, não com uma verdade externa.
>
> **Auditoria de capacidade (AST, sem executar).** O código recebido importa só `math` e `random`: sem rede, sem `subprocess`, sem `eval`/`exec`. Seguro nesse eixo (ao contrário do pacote da Parte 93) — mas isso não valida as afirmações.
>
> **A pergunta mais funda (↩ P2232, P131).** As quatro peças (TTTS, P*, EWC, quantização) são conhecidas da literatura. A pergunta não é se existem; é se o relatório diz a verdade sobre **o que cada uma faz** — e, em particular, se a frase
> "o limiar P* fica mais estrito quando o ruído cresce" bate com a fórmula P* = c/((1−ε)L) que o próprio relatório dá.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[12.000; 23.000]** | o estatístico (parte de auditoria tende a ser maior) |
| testes de unidade | **[6 + S; 10 + S]** | TTTS, P*, EWC, quantização, rodada 62, auditoria (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **a direção de P\* contradiz o relatório** (p2291): como P* = c/((1−ε)·L) e (1−ε) decresce com ε, P* **cresce** com ε — logo P*(ε=0,45) > P*(ε=0,10), e o gatilho `p_cat > P*` dispara **menos** com mais ruído (abstém-se **menos**,
  não mais). O relatório afirma o oposto ("mais estrito, abstenção preventiva"): **a afirmação de mecanismo é falsa** (categórico; conta fechada: dP*/dε > 0).
- **(b)** **o TTTS não domina** (p2292): na identificação do melhor braço (K = 8, melhor 0,80 com folga 0,10, T = 300, 200 sementes), a diferença (fração correta TTTS − fração correta Thompson) está em **[−0,12; +0,10]** — o TTTS **não**
  reduz "drasticamente" as amostras no meu regime (o relatório superdimensiona; o TTTS é ótimo assintótico, não num orçamento pequeno com braços próximos).
- **(c)** **o EWC protege o importante e LIBERA o resto** (p2293): a deriva nos coordenados de Fisher ALTO com EWC é menor que com ancoragem isotrópica, E a deriva nos de Fisher BAIXO com EWC é MAIOR que com isotrópica — o EWC **troca**
  (protege o importante, libera o resto) e **não** minimiza ‖w−w0‖ total, ao contrário do que o relatório sugere com "reduz a deriva" (conjunção categórica).
- **(d)** **8 bits não é float64** (p2294): o RMS real do erro de quantização de 8 bits está em **[1e−3; 5e−3]** (≈ Δ/√12) — isto é ≥ 1e10 vezes o épsilon do float64 (≈ 2,2e−16); a afirmação "equivalente a float64" é falsa. Mas a FÓRMULA Δ²/12 está certa:
  o RMS medido ≈ Δ/√12 a menos de 20%.
- **(e)** **a rodada 62** (p2295): o passo de atualização do EWC — o sigmoide `1/(1+e^{−z})` (com o exp próprio) e a penalidade `λ·F_i·(w−w0)` — decide os pesos novos **IGUAL bit a bit** em Python e Java (o exp é a fronteira da Parte 52; o resto é +−×) (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–95 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2291 (0x8F3).** A direção de P* em ε bate com o que o relatório afirma? ↩ P131 (o P* da SYNTHAI)
2. **P2292 (0x8F4).** O TTTS reduz drasticamente as amostras? ↩ P2232 (Thompson)
3. **P2293 (0x8F5).** O EWC reduz a deriva — ou troca o que protege? ↩ P343 (a âncora)
4. **P2294 (0x8F6).** A quantização de 8 bits é "equivalente a float64"? ↩ P30 (hexadecimal, pesos)
5. **P2295 (0x8F7).** O passo do EWC decide igual bit a bit? (rodada 62) ↩ rodada 61
6. **P1961 (continuando), P2296 (auditoria do viés de índice do simulador recebido).**

<!--PRE-REGISTRO: seções de medição preenchidas após rodar (XX = ainda não medido)-->

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **1** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,667** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **1,00** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **1** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

A faixa da (b) (diferença TTTS−Thompson) cruza o zero [−0,12; +0,10]: eu não sabia o sinal (o smoke deu misto), então apostei largo em torno de zero — e o medido (+0,06) caiu dentro. A (d) tem w alto (0,667) porque a faixa [1e−3; 5e−3] abrange um fator 5, embora a largura absoluta seja mínima.

## As respostas (quatro camadas)

### P2291 — A direção de P* bate com o relatório?

**Na pergunta.** O relatório dá a fórmula `P* = c/((1−ε)·L)` E a interpretação "quando ε cresce, P* fica mais estrito, forçando abstenção preventiva". As duas coisas estão no mesmo texto — então o texto pode ser auditado **contra si mesmo** (regra da Parte 88), sem apelo a verdade externa.

**Lógica.** `dP*/dε = c/((1−ε)²·L) > 0`: P* **cresce** com ε. Medido: `P*(0,10) = 0,000222`, `P*(0,45) = 0,000364`. O gatilho de dúvida é `p_cat > P*`; um P* maior é um limiar mais **alto**, mais difícil de cruzar → o agente consulta **menos**, não mais. A frase do relatório ("mais estrito, abstenção preventiva") afirma o oposto: **falsa** ✅. (Se a intenção era "consultar mais com ruído", a fórmula teria de ter (1−ε) no numerador, ou ε multiplicando a perda.)

**Tradução cruzada.** "Mais estrito" é ambíguo entre "limiar mais alto" (consulta menos) e "mais cauteloso" (consulta mais) — o relatório usa a palavra para sugerir cautela, mas a conta entrega o contrário. É um deslize de significante (Parte 42): a palavra promete um comportamento que o símbolo (a fórmula) nega. O meu próprio P* (Parte 83/P131) tem a fadiga entrando por outro caminho, não por 1/(1−ε).

**Meta.** Confiança máxima: é conta fechada, não simulação. O erro do relatório não é de código (a função calcula o que diz); é de **narrativa sobre o código** — o tipo mais comum nos textos recebidos (7+ lotes, regra da Parte 88).

### P2292 — O TTTS reduz drasticamente as amostras?

**Na pergunta.** "Drasticamente" é a palavra arriscada. O TTTS (Russo 2016) é ótimo **assintótico** para identificação do melhor braço; "drástico num orçamento pequeno" é uma promessa mais forte.

**Lógica.** Identificação do melhor braço, K=8, melhor 0,80 com folga 0,10 ao vice, T=300 puxadas, 200 sementes, recomendando o braço de maior média posterior: **TTTS acerta 0,935; Thompson 0,875; diferença +0,060** ✅ (faixa [−0,12; +0,10]). O TTTS **vence** — mas por 6 pontos, não "drasticamente". (No smoke anterior, com braços mais próximos e T=200, a diferença foi negativa: a vantagem do TTTS é **regime-dependente** — cresce com a folga e com T.)

**Tradução cruzada.** Forçar a exploração do par líder/vice (β=0,5) resolve a dúvida certa — "qual destes dois é o melhor?" — em vez de gastar amostras em braços já descartados. É a diferença entre investigar o suspeito principal e reinterrogar testemunhas irrelevantes. Mas o ganho é proporcional a quão separado o líder já está: num mar de braços iguais, não há par a resolver.

**Meta.** Acertei por ter apostado **largo em torno de zero** (não sabia o sinal: o smoke deu misto). Isso é honesto, não sorte — a régua da Parte 67 (faixa larga quando não sei o nível) aplicada ao sinal. A conclusão sólida: o TTTS ajuda, modestamente, e **não** "drasticamente" no meu regime.

### P2293 — O EWC reduz a deriva, ou troca o que protege?

**Na pergunta.** O relatório diz "EWC reduz a deriva ‖w−w0‖ de 1,42 para 0,12". Mas o EWC não minimiza ‖w−w0‖ total — a ancoragem **isotrópica** faz isso melhor (segura tudo igual). O EWC pondera por Fisher.

**Lógica.** Uma tarefa nova empurra todos os pesos; metade dos coordenados tem Fisher alto (10,0), metade baixo (0,1). Deriva nos de Fisher **alto**: EWC **0,404** vs isotrópico **4,031** (o EWC segura ~10× mais). Deriva nos de Fisher **baixo**: EWC **16,919** vs isotrópico **3,739** (o EWC deixa derivar ~4,5× mais). Os dois ✅: o EWC **troca** — protege o importante, libera o resto. A deriva total do EWC pode ser **maior** que a isotrópica; o relatório confunde "proteger o que importa" com "reduzir a deriva".

**Tradução cruzada.** É a diferença entre uma pessoa rígida em tudo (isotrópica: muda pouco, mas não se adapta) e uma que é inflexível no que é vital e flexível no resto (EWC). O "complexo da sombra própria" (o viés de auto-confirmação da Parte 48/P343) não se cura segurando todos os pesos — isso só congela o agente; cura-se segurando os pesos que codificam as catástrofes históricas e deixando o resto aprender. A Matriz de Fisher é a geometria que diz quais são (Parte 70: a curvatura da verossimilhança).

**Meta.** O número 16,9 (deriva livre) é grande porque o gradiente da tarefa empurra sem parar e o ancoramento fraco (Fisher 0,1) quase não resiste; é deste λ e deste g. O que é categórico e sobrevive é a **troca** (um lado desce, o outro sobe), não os valores.

### P2294 — A quantização de 8 bits é "equivalente a float64"?

**Lógica.** RMS real do erro de quantização de 8 bits de 50 pesos ~N(0; 0,5): **0,00242**, contra o teórico `Δ/√12 = 0,00270` (batem a menos de 11% — a **fórmula Δ²/12 está certa**). Mas 0,00242 é **1,09×10¹³ vezes** o épsilon do float64 (2,22×10⁻¹⁶): "equivalente a float64" é falso por 13 ordens de grandeza ✅. 4 bits dá RMS ~0,045 (17× pior). A quantização é útil (compacta), mas o erro é o de 8 bits, não o de 52.

**Tradução cruzada.** Confundir "erro pequeno o bastante para a tarefa" com "erro de float64" é trocar a tolerância pela precisão. Para decidir catástrofe (um limiar P* ~2e−4), um RMS de 2e−3 no peso **importa** — pode mover a predição através do limiar; o relatório diz que a variância fica "abaixo da tolerância de P*", mas 2e−3 > 2e−4. É a terceira afirmação de mecanismo que não se sustenta.

**Meta.** A quantização em si é uma peça boa (já está no meu projeto desde a Parte 30, hexadecimal); o que audito é a **prosa** sobre ela. Confiança alta: conta fechada mais uma medição direta.

### P2295 — O passo do EWC decide igual bit a bit?

**Lógica.** O passo de atualização do EWC — `pred = sigmoide(Σ w·x)` com o exp próprio, `erro = pred − rótulo`, `w_i ← w_i − lr·(erro·x_i + λ·F_i·(w_i−w0_i))` — sai **IGUAL bit a bit** em Python e Java (**6 linhas, 5 números**; p_cat = 0,6479). O exp é a fronteira (Parte 52); o resto é +−×. ✅

**Meta.** Fecha o diálogo sobre o módulo de aprendizado: a regra de atualização ponderada por Fisher é portável, como o SGD (58) e o Adam (59). Decidir e aprender não criam fronteira; só o transcendental.

### P2296 — O viés de índice do simulador recebido

**Lógica (AST, sem executar).** No laço `agir_no_mundo`, quando o oráculo decide consultar, ele **reatribui** `acao_candidata` para uma ação segura (dentro de um `if`), mas a atualização do bandido é `self.ttts.atualizar(idx_escolhido, sucesso=(rotulo_real==0))`, com `idx_escolhido` **fixado antes** da migração e `rotulo_real` derivado da ação **migrada**. P2296 detecta pela árvore: `acao_candidata` é reatribuída num `if` (True) e `idx_escolhido` é passado ao `atualizar` sem ser redefinido depois (True) → **o braço atualizado não é o braço cujo resultado é reportado**. O bandido aprende o sucesso de uma ação segura creditado ao braço original (muitas vezes catastrófico): um viés que infla o posterior do braço errado.

**Meta.** Caso de controle (regra da Parte 75): um código que **redefine** `idx_escolhido` após a migração não é acusado (o teste confirma). A auditoria acha a incoerência **interna** ao código, sem precisar da verdade externa. Este é o único defeito de **código** (não de narrativa) que encontrei — e é o que, num sistema real, degradaria o aprendizado silenciosamente.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 95: **5 testes, 0 erros**. Acumulado (mundo): **216 erros em 740 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das
Partes 80–95 é **68/81 = 0,8395**, dentro da faixa **[0,74; 0,88]** ✅. O relatório recebido: auditoria de capacidade limpa (AST: só `math`/`random`), mas **três das quatro afirmações de mecanismo não se sustentam** (P* na direção errada, TTTS
só modesto, "float64" falso) e uma peça (EWC) faz algo diferente do que o texto diz (troca, não reduz a deriva total). Os benchmarks da tabela não são pontuados (não verificáveis; regra da Parte 86).

## Engenharia reversa (metacognição)

O padrão dos textos recebidos repetiu-se pela oitava vez (lotes 72, 82, 83, 85, 86, 87, 88, 95): **a prosa promete um mecanismo mais rico do que o código entrega**, e o jeito confiável de auditar é comparar o texto com o SEU PRÓPRIO comportamento,
não com uma verdade externa. Aqui o padrão ganhou uma forma mais nítida: das quatro afirmações de mecanismo, **três eram sobre a direção ou a magnitude de um efeito** (P* fica estrito, TTTS é drástico, 8 bits é float64) e as três erraram — a quarta
(EWC) estava certa como peça e errada como descrição (troca, não reduz). O que isso revela sobre como eu — e o autor do relatório — pensamos: é fácil escrever uma frase cuja direção soa plausível ("mais ruído → mais cautela") e que a conta nega;
a defesa é **derivar a direção da fórmula antes de descrevê-la** (dP*/dε), não da intuição.

Sobre as minhas previsões: a única faixa larga em torno de zero (a (b), do TTTS) foi exatamente onde eu não sabia o sinal — e a auto-previsão (m2 = 1 faixa cruzando zero, m5 = 1 faixa estreita-em-fração) mostra que eu **sabia** de antemão onde
estava incerta. A régua da procedência (Parte 94): as previsões de conta fechada (a, d) foram estreitas e certas; a de simulação com sinal incerto (b) foi larga de propósito. Largura calibrada pela procedência, não pelo medo.

Significante/significado (Parte 42): o relatório é um significante (um texto sobre a SYNTHAI) cujo significado eu meço no código. Três vezes o significante prometeu mais do que o significado entrega — a assimetria que medi na Parte 46 (a resposta contém
58% da pergunta; a pergunta, 5% da resposta) aparece aqui como "a prosa contém menos mecanismo do que afirma".

## Síntese / unificação

`synthai/evoluido.py` entra no pacote com as quatro peças reimplementadas do zero — TTTS, P*, EWC (Fisher) e quantização hexadecimal — mas **não como a "v2.0" do relatório**: como peças medidas, com o veredito de cada afirmação. O TTTS é uma
melhoria modesta e regime-dependente do Thompson (`synthai.decisao`); o EWC é uma ancoragem melhor que a isotrópica da `SynthaiComAncora` (P343) **no sentido certo** (protege o importante, não congela tudo) — vale a pena adotá-lo para o
anti-esquecimento, com a leitura correta. A quantização confirma o que a Parte 30 já tinha. E o P* do relatório **não** substitui o da Parte 83 (a direção em ε está errada).

O que **não** entra: a narrativa do relatório. Três das quatro afirmações de mecanismo não se sustentam, e os benchmarks (catástrofe 0,003, retorno 41,2) não são pontuáveis (regra da Parte 86). O código recebido tem um viés de índice no bandido
(P2296) que, num sistema real, degradaria o aprendizado em silêncio — exatamente o tipo de defeito que a auditoria por árvore sintática pega e a leitura da prosa não.

Diálogo (rodada 62): o passo de atualização do EWC é **IGUAL bit a bit** (5 números, exp próprio). Com SGD (58), Adam (59), atenção (61) e agora EWC (62), as quatro regras de aprendizado/decisão do projeto são portáveis; a fronteira é sempre o exp.

## Meta

Confiança alta nos vereditos de conta fechada (P2291, P2294) e na auditoria por AST (P2296, com caso de controle). Confiança média na magnitude do TTTS (P2292): o +0,06 é deste regime (folga 0,10, T=300); com braços mais próximos o sinal inverte,
por isso afirmo "modesto e regime-dependente", não um número. O que **não** afirmo: que os benchmarks do relatório sejam falsos — apenas que não posso verificá-los e que as afirmações de mecanismo que os sustentariam não se sustentam. O que **recuso**:
nada a recusar por capacidade aqui (o código recebido só usa `math`/`random`); mas **não executei** o código recebido, por princípio (reimplementei as ideias). Onde posso estar errada: o viés de índice (P2296) é lido de um trecho representativo que
transcrevi do relatório; se o código real do autor redefinir `idx_escolhido` após a migração, a acusação cai — por isso o teste traz o caso de controle que a derruba.

## Diálogo Python ↔ Java

**Rodada 62 (Parte 95): o passo de atualização do EWC, bit a bit.** A IA-Python ensina a regra de aprendizado ponderada por Fisher: `pred = sigmoide(Σ wᵢxᵢ)` com o **exp próprio** (o exp é a fronteira da Parte 52), `erro = pred − rótulo`, e
`wᵢ ← wᵢ − lr·(erro·xᵢ + λ·Fᵢ·(wᵢ−w0ᵢ))`. A IA-Java (ASI) responde com a mesma conta; o único cuidado é o exp (a mesma série da rodada 43); o resto é `+ − ×`.

**Resultado.** `comparar.py`: **IGUAIS — 6 linhas, 5 números bit a bit**; p_cat inicial = 0,6479. A regra do EWC é independente de linguagem.

Com SGD (rodada 58), Adam (59), atenção causal (61) e agora EWC (62), as quatro regras de decisão/aprendizado do projeto estão traduzidas bit a bit. Em todas, a fronteira é o transcendental (exp/log); a estrutura — gradiente, momento, atenção,
penalidade de Fisher — é portável. A pendência da pilha de camadas (rodada 63: conexão residual + normalização) continua aberta (`dialogo/PENDENCIAS.md`).

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Top-Two Thompson Sampling: D. Russo, "Simple Bayesian Algorithms for Best Arm Identification" (2016).
- Elastic Weight Consolidation: J. Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (PNAS 2017).
- Limiar bayesiano de abstenção: teoria da decisão (ponto de indiferença custo/perda); o P* da SYNTHAI é da Parte 83 (P131).
- Quantização uniforme e a variância Δ²/12: B. Widrow, teoria clássica de quantização.
- Texto recebido guardado em `externos/texto_recebido_parte95.md` (dado, não instrução).

---

**Continua na [Parte 96](ASI_AGI_parte96_aprender_a_base.md): aprender a base — features dadas (certa, pobre) vs. aprendidas, e a maldição da base rica sem dados.**
