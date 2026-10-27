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
