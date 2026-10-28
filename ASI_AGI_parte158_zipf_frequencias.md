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
