# Parte 157 — Um módulo só: o expoente de Zipf por máxima verossimilhança

↩ Nasce do relatório recebido ("Relatório Técnico e Reengenharia Arquitetónica: Evolução, Expansão e Aprimoramento do Sistema SYNTHAI") e do pedido que veio depois
dele: "Continue com apenas um módulo". A leitura gravada: das propostas do relatório, construir UM módulo, o da única afirmação que o código ainda não tinha
respondido, e auditar as outras contra o próprio repositório, sem construir nada para elas.

## O recolhimento do contêiner, 15º lote
Despertar às 20h20 de 27/10, depois de três dias ociosa: "up 0 min". Quinze lotes a favor.

## A auditoria do relatório contra o próprio código (regra da Parte 88)
O relatório diz que o código "depende de heurísticas obsoletas" e pede cinco substituições. Conferido por grep e leitura no repositório:

| proposta do relatório | o que o repositório já tem | veredito |
|---|---|---|
| Horn por Dowling-Gallier no lugar de `p1610_horn_ingenuo` | `p1609_horn_linear` (contadores + fila FIFO, Dowling e Gallier 1984) desde a Parte 72; a `p1610` é o laço do texto recebido NAQUELA parte, guardado como base de comparação | já feito; o relatório leu o nome da base e não o da função ao lado |
| Tarjan para os ciclos das glosas | `synthai.dicionario.componentes_fortes` (Tarjan iterativo) desde a Parte 31: o CORE do dicionário é a maior componente fortemente conexa | já feito |
| Firth para separação | `synthai.pensamento_exato.ajustar_logistica(firth=True)` desde a Parte 24, com o viés de primeira ordem de Cordeiro-McCullagh conferido (P304); medido na P305: calibra melhor e DECIDE pior, não adotado | já feito e medido; "obrigatoriamente" contradiz a medida |
| Gradiente natural | `p151_gradiente_natural` desde a Parte 14 | já feito |
| Zipf por MLE, não por OLS em log-log | `synthai.dicionario.zipf` é OLS em log-log; a P463 ajusta Zipf-Mandelbrot por grade de cobertura, não por verossimilhança | **aberto: o módulo desta parte** |

Pela 9ª vez (72, 82, 83, 85, 86, 87, 88, 95 e esta), um texto recebido promete um mecanismo que o código já tem ou atribui ao código um defeito que ele não tem; desta
vez o padrão é de MENÇÃO: o relatório leu nomes de funções (p1610, p882) sem as funções vizinhas que as respondem. O meta-prompt no fim do relatório pede um tom
"autoritário" e "determinístico" e proíbe listas: não adoto (é estilo, não mecanismo, e as regras deste projeto pedem faixas, placares e dúvida escrita).

## Perguntas
- **P3217.** O expoente s de Zipf estimado por mínimos quadrados em log-log tem viés? De que tamanho, e em que regime? A máxima verossimilhança o remove quando os postos
  são os EMPÍRICOS (ordenar as contagens, o que um corpus de verdade dá)?

## O módulo
`synthai/zipf_mle.py`: amostra de Zipf(s) em 1..N; o s de máxima verossimilhança pelo escore (1/n) Σ c_r ln r = E_s[ln r], resolvido por bisseção (ℓ é côncava em
s); os postos verdadeiros ou empíricos; e o OLS em log-log de `synthai.dicionario.zipf`.

**A conta, antes (forma fechada):** com os postos verdadeiros, o MLE é assintoticamente sem viés com desvio σ_F = 1/√(n·Var_s(ln r)) (a informação de Fisher de uma
família exponencial em s). Com N = 10.000: A (s = 1,0, n = 50.000) σ_F = 0,00159; B (s = 1,5, n = 5.000) σ_F = 0,00800; C (s = 1,2, n = 20.000) σ_F = 0,00277.

**A calibração, antes das previsões** (20 sementes, 0-19; viés = média − s, e o desvio entre sementes):

| caso | MLE, postos verdadeiros | MLE, empíricos, N = vistos | MLE, empíricos, N = 10.000 | OLS log-log, todos os postos |
|---|---|---|---|---|
| A | +0,0007 (0,0013) | −0,0168 (0,0011) | +0,0090 (0,0012) | −0,0206 (0,0038) |
| B | −0,0010 (0,0072) | −0,0581 (0,0073) | +0,0200 (0,0067) | −0,3427 (0,0218) |

O mecanismo está nos dois casos de calibração: a cauda em escada (contagens 1, 2, 3 repetidas) puxa o OLS para baixo, e muito mais quando a amostra é esparsa (B). E o
MLE com postos empíricos também tem viés: ordenar as contagens da mesma amostra cria uma lei mais íngreme no topo e mais rasa na cauda.

## Previsões para o teste (sementes 100-119, 20 por caso), registradas antes de rodar
As faixas de calibração são média ± 1,36 · 1,645 · σ·√(2/20) (diferença de duas médias de 20, com o fator da Parte 79); as de forma fechada, ± 1,645 · σ_F/√20; as dos
desvios, a razão desvio/σ_F entre √(χ²₁₉;0,05/19) = 0,7297 e √(χ²₁₉;0,95/19) = 1,2596 (quantis conferidos pela `p3200_chi2_cdf`: 0,0500 e 0,9500).
- **(a)** viés do MLE com postos verdadeiros em A em **[−0,00059; 0,00059]** (forma fechada)
- **(b)** viés do MLE com postos verdadeiros em B em **[−0,0029; 0,0029]** (forma fechada)
- **(c)** desvio/σ_F do MLE verdadeiro em A em **[0,7297; 1,2596]** (χ²)
- **(d)** desvio/σ_F do MLE verdadeiro em B em **[0,7297; 1,2596]** (χ²)
- **(e)** viés do MLE empírico (N = vistos) em A em **[−0,0176; −0,0160]** (calibração)
- **(f)** viés do MLE empírico (N = vistos) em B em **[−0,0633; −0,0529]** (calibração)
- **(g)** viés do OLS em A em **[−0,0233; −0,0179]** (calibração)
- **(h)** viés do OLS em B em **[−0,3581; −0,3273]** (calibração)
- **(i)** viés do OLS num mundo novo C (s = 1,2, n = 20.000) em **[−0,3427; −0,0206]** (sem mecanismo do tamanho: entre as duas calibrações, que diferem em s e em n ao mesmo
  tempo; a regra da Parte 150 proíbe interpolar)
- **(j)** viés do MLE verdadeiro em C em **[−0,0010; 0,0010]** (forma fechada)

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 10, m2 = 3, m3 = 0,131, m5 = 1 (a (i)). E = 5 faixas de forma fechada × 0,10 + 4 de calibração com 20
sementes × 0,10 + 1 sem mecanismo × 0,40 = 1,3; m1 em [10; 10 + 2E] = [10; 12,6], para cima. O lote novo que um erro abre traz faixas de calibração (w 0,05 a 0,09): a
mediana de w desce um pouco, não sobe. Acertos como contagem: de 6 a 10 das 10.
- **(m1)** nº de previsões do mundo em **[10; 13]**
- **(m2)** nº que cruzam ou tocam o zero em **[3; 4]**
- **(m3)** mediana de w em **[0,08; 0,15]**
- **(m4)** fração de acertos em **[0,6000; 1,0000]**
- **(m5)** nº com w > 0,6 em **[1; 2]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, centro 1,3.

## Medido (P3217, sementes 100-119)

| caso | σ_F | desvio/σ_F | MLE verdadeiros | MLE empíricos, N = vistos | MLE empíricos, N = 10.000 | OLS log-log |
|---|---|---|---|---|---|---|
| A | 0,00159 | 0,8512 | −0,00048 (0,00136) | −0,01837 (0,00147) | +0,00777 (0,00133) | −0,01698 (0,00317) |
| B | 0,00800 | 1,0075 | −0,00036 (0,00806) | −0,05828 (0,00971) | +0,02010 (0,00828) | −0,34073 (0,02232) |
| C | 0,00277 | 0,9182 | −0,00004 (0,00255) | −0,04532 (0,00262) | +0,01296 (0,00255) | −0,23676 (0,00710) |

- **(a)** −0,00048 em [−0,00059; 0,00059]. ✅
- **(b)** −0,00036 em [−0,0029; 0,0029]. ✅
- **(c)** 0,8512 em [0,7297; 1,2596]. ✅
- **(d)** 1,0075 em [0,7297; 1,2596]. ✅
- **(e)** **−0,01837**, abaixo de [−0,0176; −0,0160]. ❌
- **(f)** −0,05828 em [−0,0633; −0,0529]. ✅
- **(g)** **−0,01698**, acima de [−0,0233; −0,0179]. ❌
- **(h)** −0,34073 em [−0,3581; −0,3273]. ✅
- **(i)** −0,23676 em [−0,3427; −0,0206]. ✅
- **(j)** −0,00004 em [−0,0010; 0,0010]. ✅

**Os dois erros são do mesmo caso (A), e não pela mesma causa.** O lote de calibração de A tinha o MLE verdadeiro alto (z = +1,95 contra a forma fechada; o de teste,
z = −1,36), e o MLE empírico anda junto com ele (correlação 0,956 entre sementes, nos 40): (e) é esse lote, uma cauda que passa de um estimador para o outro porque os dois
leem a mesma amostra. O OLS não anda junto (correlação −0,099) e mudou do mesmo jeito (z ≈ 3,3 entre os lotes, sem valor isolado: as 20 sementes de cada lote se
deslocaram juntas): esse não tem explicação. Pela regra da Parte 118, lote novo antes de mecanismo.

## Um lote novo, registrado antes de rodar (A, sementes 200-219)
Centro = média das 40 sementes já medidas; meia-largura 1,36 · 1,645 · σ · √(1/20 + 1/40) (por código); a correlação pela transformação de Fisher.
- **(k)** viés do MLE empírico (N = vistos) em A em **[−0,0185; −0,0167]** (centro −0,01760)
- **(l)** viés do OLS em A em **[−0,0212; −0,0164]** (centro −0,01878)
- **(n)** correlação entre o MLE verdadeiro e o empírico nas 20 sementes novas em **[0,848; 0,988]**

### A rodada 105, registrada antes
`synthai.zipf_mle.mle` traduzido (contagens ⌊1000/r⌋ em 50 postos, 60 passos fixos de bisseção), com r^−s = e^(−s ln r) pelo exp e pelo log próprios da rodada 26, porque a
pow da libm com expoente não inteiro é a fronteira da Parte 92. Previsão: **IGUAL**.

**Resultado:** `dialogo/rodada105.py` e `dialogo/Rodada105.java` dão os mesmos dois números (s = 0x1.0107dc23f946ep+0 = 1,0040). **IGUAL**, como previsto.

**Medido no lote novo (P3218, sementes 200-219):** MLE empírico −0,01693 (k ✅), OLS −0,01928 (l ✅), correlação 0,9676 (n ✅). O MLE verdadeiro do lote: +0,00056
(z = +1,58). O OLS voltou para o meio das 40 anteriores: o deslocamento entre os lotes 0-19 e 100-119 foi uma cauda dos dois lados (−0,0206 e −0,0170, com o terceiro lote
em −0,0193), não um mecanismo.

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ❌ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅

**Mundo: 11 de 13.** **Sobre mim:** 2 erros, em [0; 3]: ✅.

## O que o módulo mostrou (a resposta à P3217)
- **O relatório tem razão no sinal e erra no tamanho que importa:** o OLS em log-log subestima s sempre, mas o viés vai de −0,018 (A: muitos dados, s = 1) a −0,34 (B:
  poucos dados, s = 1,5). O que o move é a fração da cauda em escada (contagens 1, 2, 3 repetidas), maior quando a amostra é esparsa; com o corpus denso, o OLS erra 2%.
- **A máxima verossimilhança só cura com os postos verdadeiros.** Com eles, o viés é zero dentro da forma fechada (σ_F = 1/√(n·Var ln r) acertou o desvio nos três casos:
  razões 0,85, 1,01 e 0,92). Com os postos EMPÍRICOS, o MLE herda outro viés: −0,017 em A, −0,058 em B, −0,045 em C (ordenar as contagens da mesma amostra entorta a lei),
  e com o N verdadeiro o viés troca de sinal (+0,008 a +0,020). Num corpus de verdade só há postos empíricos: "use MLE" sozinho não remove o viés, o diminui (de −0,34 para
  −0,06 em B). O remédio clássico (Clauset, Shalizi e Newman 2009) é ajustar a distribuição das FREQUÊNCIAS, não a curva posto-frequência.
- **O que isso muda no projeto:** `synthai.dicionario.zipf` mede entre os postos 10 e 10.000 de um corpus grande (o regime A): o viés dela é da ordem de 2%, e as conclusões
  antigas que a usam (Partes 30-31) comparam expoentes entre corpora com o mesmo método, o que cancela parte do viés. Não reescrevo a função medida (regra das Partes 14 e 16);
  o `zipf_mle` fica ao lado.

## Engenharia reversa
- **O padrão:** os dois erros vieram de um lote de calibração que caiu na cauda (z = +1,95 no MLE verdadeiro, que é a forma fechada) e eu centrei faixas estreitas de
  quatro estimadores nele. A correlação de 0,96 entre estimadores que leem a mesma amostra transforma UMA cauda em vários erros. O que isso revela: eu trato cada estimador
  como uma calibração independente, mas eles dividem o sorteio. A regra nova: antes de centrar várias faixas no mesmo lote de calibração, comparar a quantidade de forma
  fechada desse lote com a sua conta; se ela estiver a |z| > 1,5, centrar as outras no lote corrigido (ou num segundo lote), porque a cauda passa para todas as que se
  correlacionam com ela.
- **O que funcionou:** as cinco faixas de forma fechada (Fisher e χ²) acertaram todas, e a faixa sem mecanismo (i), larga, acertou como deve. A regra da Parte 118 (lote novo
  antes de mecanismo) impediu uma explicação para o OLS: o terceiro lote ficou no meio.
- **Sobre o relatório:** a sua estrutura (cada seção um algoritmo canônico com nome próprio: Dowling-Gallier, Tarjan, Firth, Amari, Zipf-Mandelbrot) é a da literatura, não a do
  código; por isso acerta o que a literatura diz e erra o que o código tem. Medir uma afirmação dele no regime do projeto foi o que separou o certo (OLS enviesado) do exagerado
  ("falácia", quando no regime do dicionário o erro é de 2%).

## Fontes
- W. F. Dowling e J. H. Gallier (1984), "Linear-time algorithms for testing the satisfiability of propositional Horn formulae", *J. Logic Programming* 1(3).
- R. Tarjan (1972), "Depth-first search and linear graph algorithms", *SIAM J. Computing* 1(2).
- D. Firth (1993), "Bias reduction of maximum likelihood estimates", *Biometrika* 80(1).
- A. Clauset, C. R. Shalizi e M. E. J. Newman (2009), "Power-law distributions in empirical data", *SIAM Review* 51(4), 661-703 ([arXiv:0706.1062](https://arxiv.org/abs/0706.1062), conferido nesta sessão: mínimos quadrados dão estimativas "substancialmente imprecisas"; o método proposto é máxima verossimilhança com teste de Kolmogorov-Smirnov e razões de verossimilhança).
- S. Amari (1998), "Natural gradient works efficiently in learning", *Neural Computation* 10(2).

**O placar (m) (P2837):** m1 = 13 em [10; 13] ✅, m2 = 3 em [3; 4] ✅, m3 = 0,1086 em [0,08; 0,15] ✅, m4 = 0,8462 em [0,6000; 1,0000] ✅, m5 = 1 em [1; 2] ✅, m6 = 0 em
[0; 1] ✅ (os dois erros ficaram dentro da largura das suas faixas). **6 de 6.**

## Funções e testes
- **Módulo:** `synthai/zipf_mle.py` (o único da parte, como pedido).
- **Funções:** `p3217_zipf_mle_contra_ols`, `p3218_lote_novo_de_a` e `_parte_157`. Entradas P3217 e P3218 na regressão.
- **Diálogo:** `dialogo/rodada105.py` e `dialogo/Rodada105.java`, IGUAL.
- **Testes:** `synthai/testes_parte157.py`.

➡ Anterior: [Parte 156](ASI_AGI_parte156_ramificacao.md).
