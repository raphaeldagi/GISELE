# Parte 158 — Mais um módulo: o expoente pelas frequências (e a última parte deste ciclo)

↩ Nasce da Parte 157 (a pendência 1: ajustar pela distribuição das FREQUÊNCIAS, à maneira de Clauset, Shalizi e Newman, que não precisa ordenar a amostra) e do pedido
"Mais um módulo! E pare!". A leitura gravada: um módulo novo, a parte fechada com todas as regras, e depois parar (sem agendar a continuação).

## O recolhimento do contêiner, 16º lote
Despertar às 10h39 de 28/10: "up 0 min". Dezesseis lotes a favor.

## Perguntas
- **P3219.** Estimar o expoente de Zipf pela lei de potência das frequências dos tipos (α = 1 + 1/s, máxima verossimilhança com x_min) remove o viés dos postos
  empíricos que a Parte 157 mediu?

## O módulo
`synthai/zipf_frequencias.py`: a lei de potência discreta p(x) = x^−α/ζ(α, x_min) nas frequências ≥ x_min; o ζ de Hurwitz e a sua derivada por soma direta até
x_min + 2.000 e o resto de Euler–Maclaurin (conferido: ζ(2, 1) − π²/6 = 3,1e−15); o α pelo escore (1/m) Σ ln x = E_α[ln x], por bisseção; s = 1/(α − 1).

**A calibração, antes das previsões** (sementes 0-19, os casos A e B da Parte 157; viés de s e desvio entre sementes):

| caso | x_min = 1 | x_min = 2 | x_min = 5 |
|---|---|---|---|
| A (s = 1,0, n = 50.000) | +0,2835 (0,0056) | −0,0547 (0,0075) | −0,0624 (0,0118) |
| B (s = 1,5, n = 5.000) | −0,4229 (0,0305) | −0,1780 (0,0506) | −0,1134 (0,0647) |

O mecanismo está nos dois casos: a relação α = 1 + 1/s é ASSINTÓTICA (vale para um vocabulário infinito); com N = 10.000 tipos, a cauda das frequências é cortada
pelo fim do vocabulário e pela amostragem (frequências 1 e 2 em excesso), e o x_min só desloca o viés, não o remove. Na calibração, o método das frequências erra MAIS
que o MLE com postos empíricos da Parte 157 (A: −0,017; B: −0,058).

## Previsões para o teste (sementes 100-119), registradas antes de rodar
Faixas = média ± 1,36 · 1,645 · σ · √(2/20) (por código).
- **(a)** viés com x_min = 2 em A em **[−0,0600; −0,0494]**
- **(b)** viés com x_min = 5 em A em **[−0,0707; −0,0541]**
- **(c)** viés com x_min = 2 em B em **[−0,2138; −0,1422]**
- **(d)** viés com x_min = 5 em B em **[−0,1592; −0,0676]**
- **(e)** viés com x_min = 2 num mundo novo C (s = 1,2, n = 20.000) em **[−0,1780; −0,0547]** (sem mecanismo do tamanho: entre as duas calibrações, que diferem em s e em
  n ao mesmo tempo)
- **(f)** nº de casos (A, B, C) em que o viés com x_min = 2 é MAIOR em módulo que o do MLE com postos empíricos da Parte 157 (A −0,0184, B −0,0583, C −0,0453) em **[3; 3]**
  (mecanismo; P(uma) estimada pela calibração, com folgas de 3σ ou mais em A e B; C sem calibração, P(todas) ≈ 0,9)

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 6, m2 = 0, m3 = 0,167, m5 = 0. E = 4 faixas de calibração × 0,10 + 1 sem mecanismo × 0,40 + 1 contagem de mecanismo
× 0,20 = 1,0; m1 em [6; 6 + 2E] = [6; 8]. Um lote novo traria faixas de calibração de w 0,1 a 0,2: a mediana fica perto. Acertos como contagem: de 3 a 6 das 6.
- **(m1)** nº de previsões do mundo em **[6; 8]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 0]**
- **(m3)** mediana de w em **[0,12; 0,25]**
- **(m4)** fração de acertos em **[0,5000; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 1]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, centro 1,0.

## Medido (sementes 100-119)

| caso | x_min | viés | desvio |
|---|---|---|---|
| A | 2 | −0,0480 | 0,0067 |
| A | 5 | −0,0636 | 0,0149 |
| B | 2 | −0,1755 | 0,0470 |
| B | 5 | −0,0792 | 0,0751 |
| C | 2 | −0,1640 | 0,0171 |

- **(a)** **−0,0480**, acima de [−0,0600; −0,0494]. ❌
- **(b)** −0,0636 em [−0,0707; −0,0541]. ✅
- **(c)** −0,1755 em [−0,2138; −0,1422]. ✅
- **(d)** −0,0792 em [−0,1592; −0,0676]. ✅
- **(e)** −0,1640 em [−0,1780; −0,0547]. ✅
- **(f)** o viés pelas frequências é maior que o do MLE com postos empíricos nos 3 casos (0,048 > 0,018; 0,176 > 0,058; 0,164 > 0,045). ✅

**O erro (a) é a regra que eu escrevi na Parte 157, desobedecida na parte seguinte:** o lote de calibração de A são as sementes 0-19, o mesmo lote cujo MLE verdadeiro
estava a z = +1,95 da forma fechada. A regra mandava conferir isso antes de centrar faixas nele; eu não conferi, e a cauda passou para o estimador novo do mesmo jeito.

## Um lote novo, registrado antes de rodar (A, x_min = 2, sementes 200-219)
Centro = média das 40 sementes já medidas; meia-largura 1,36 · 1,645 · σ · √(1/20 + 1/40) (por código).
- **(g)** viés com x_min = 2 em A em **[−0,0557; −0,0470]** (centro −0,05135)

**Medido no lote novo (P3219, sementes 200-219):** −0,05048 (g ✅).

### A rodada 106, registrada antes
`synthai.zipf_frequencias.alfa_mle` traduzido (frequências fixas, x_min = 2, K = 200 termos diretos e o resto de Euler–Maclaurin), com k^−a = e^(−a ln k) pelo exp e o log
próprios da rodada 26 e 60 passos fixos de bisseção. Previsão: **IGUAL**.

**Resultado:** `dialogo/rodada106.py` e `dialogo/Rodada106.java` dão os mesmos dois números (α = 0x1.4d2e2af1119b8p+0 = 1,3015). **IGUAL**, como previsto.

Do mundo: (a) ❌ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅

**Mundo: 6 de 7.** **Sobre mim:** 1 erro, em [0; 3]: ✅.

## O que o módulo mostrou (a resposta à P3219)
- **Não.** O método das frequências erra MAIS que o MLE com postos empíricos nos três casos (A −0,048 contra −0,018; B −0,176 contra −0,058; C −0,164 contra −0,045). A
  relação α = 1 + 1/s é assintótica: vale para um vocabulário sem fim e sem amostragem. Com 10.000 tipos e uma amostra finita, a distribuição das frequências não é uma lei de
  potência pura (há frequências 1 e 2 a mais, e a cauda alta é cortada), e mudar o x_min troca um viés por outro (A: +0,28 com x_min = 1, −0,05 com 2 e 5).
- **O que isso diz da série 157-158:** dos quatro estimadores medidos, o único sem viés é o MLE com os postos VERDADEIROS, que um corpus real não dá. Num corpus real, o melhor
  dos três disponíveis é o MLE com postos empíricos e N conhecido (+0,008 a +0,020). O método recomendado na literatura para leis de potência genéricas não é o melhor para a lei
  posto-frequência de um vocabulário finito: a recomendação de Clauset e colegas trata outro objeto (uma variável com cauda de potência), e eu a apliquei por reputação. Foi por
  isso que esta parte registrou faixas tiradas da calibração e não da reputação do método.

## Engenharia reversa
- **O padrão:** o único erro desta parte é a regra da parte anterior desobedecida no mesmo lote (as sementes 0-19 de A, com o MLE verdadeiro a z = +1,95). Uma regra escrita
  ontem e esquecida hoje não virou passo. É a lição da Parte 49 de novo: uma regra só vale quando vira um passo verificável. O passo, agora: toda calibração de uma parte
  imprime, ao lado das médias, o z da quantidade de forma fechada do mesmo lote, para a regra ser lida antes da faixa e não depois do erro.
- **O que funcionou:** a calibração antes de prever (regra das Partes 84 e 87) mostrou, antes do registro, que o método famoso era pior aqui. Sem ela, eu teria previsto pela
  reputação de "MLE de Clauset" e errado as quatro faixas.

**O placar (m) (P2837):** m1 = 7 em [6; 8] ✅, m2 = 0 ✅, m3 = 0,1330 em [0,12; 0,25] ✅, m4 = 0,8571 em [0,5000; 1,0000] ✅, m5 = 0 ✅, m6 = 0 em [0; 1] ✅. **6 de 6.**

## Fim deste ciclo
A pedido ("Mais um módulo! E pare!"), esta é a última parte do ciclo automático: não há continuação agendada. As pendências ficam em `dialogo/PENDENCIAS.md` para quando o
trabalho voltar.

## Fontes
- A. Clauset, C. R. Shalizi e M. E. J. Newman (2009), "Power-law distributions in empirical data", *SIAM Review* 51(4), 661-703 ([arXiv:0706.1062](https://arxiv.org/abs/0706.1062),
  conferido na Parte 157: máxima verossimilhança com x_min e teste de Kolmogorov-Smirnov para variáveis com cauda de potência).

## Funções e testes
- **Módulo:** `synthai/zipf_frequencias.py`.
- **Funções:** `p3219_zipf_pelas_frequencias` e `_parte_158`. Entrada P3219 na regressão.
- **Diálogo:** `dialogo/rodada106.py` e `dialogo/Rodada106.java`, IGUAL.
- **Testes:** `synthai/testes_parte158.py`.

➡ Anterior: [Parte 157](ASI_AGI_parte157_zipf_mle.md).
