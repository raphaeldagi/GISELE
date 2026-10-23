# Parte 145 — Os grupos úteis da GRPO num segundo mundo, e o recolhimento do contêiner medido

↩ Nasce de duas pendências de `dialogo/PENDENCIAS.md`:
- a da Parte 139: os grupos úteis da GRPO só foram vistos num mundo, um lote;
- a (2) da Parte 131: a hipótese de que o contêiner é recolhido quando a sessão fica ociosa.

## A pendência da Parte 131, medida pelo que já aconteceu
Nos últimos quatro despertares agendados (15h35, 16h37, 17h25 e 18h16), o contêiner estava "up 0 min": ele tinha sido recolhido entre os
turnos e recriado para entregar o lembrete. A volta 9 ficou parada em 30 arquivos entre as 17h25 e as 18h16, embora o processo tivesse sido
relançado. A Parte 133 tinha dado a hipótese como refutada, porque houve reinícios com tarefas ativas. As duas coisas são compatíveis: uma
tarefa em segundo plano NÃO impede o recolhimento, mas um TURNO em andamento, sim. O que avança a volta é trabalhar no turno, e não deixar
algo rodando. Fica registrado como hipótese de 4 lotes, com uma previsão abaixo (j).

## Perguntas
GRPO num mundo novo: 128 contextos de treino (semente 145) e 128 de teste (semente 146), sementes de treino 31 a 33, 4.096 ações, G = 2, 4, 8, 16:
- **(a)** A ordem dos retornos é a ordem dos grupos úteis U?
- **(b)** a **(d)** As diferenças ret(G) − ret(2) seguem b·ln(U_G/U_2), com o b do mundo antigo?
- **(e)** a **(h)** Os grupos úteis U do mundo novo ficam perto dos do antigo?
- **(j)** No próximo despertar agendado, o contêiner estará recém-criado?

## Previsões, registradas antes de qualquer execução do mundo novo
**A conta, feita com o mundo antigo (31/32).** Pontos (U, retorno): (385, 0,9086), (355, 0,9058), (255, 0,8987) e (179, 0,8825). O ajuste
linear do retorno contra ln U dá b = 0,0330, com resíduos de até 0,003. No mundo novo, ret(G) − ret(2) = 0,0330·ln(U_G/U_2), calculado com os
U medidos no próprio mundo novo. Isso testa a relação, e não o nível.

A faixa: o desvio entre sementes da média de 3 réplicas é 0,0093/√3 = 0,0054; uma diferença de duas médias tem desvio 0,0054·√2 = 0,0076;
1,645·0,0076·1,36 = 0,017.

**Procedência:**
- hipótese de 1 lote: (a) a (h);
- hipótese de 4 lotes: (j).

O centro de "quantos erros" é 0,25 × 9 = 2,25.

- **(a)** a ordem dos 4 retornos é a ordem dos 4 U em **[1; 1]** (1 = sim). Por acaso, 1/24.
- **(b)** ret(4) − ret(2) − 0,0330·ln(U₄/U₂) em **[−0,017; 0,017]**
- **(c)** ret(8) − ret(2) − 0,0330·ln(U₈/U₂) em **[−0,017; 0,017]**
- **(d)** ret(16) − ret(2) − 0,0330·ln(U₁₆/U₂) em **[−0,017; 0,017]**
- **(e)** U de G = 2 em **[340; 430]**. O Poisson sozinho daria ±1,645·√(385·0,19)·1,36 = ±19. A variação ENTRE MUNDOS de U não foi calibrada (um mundo só), e por isso alargo para ±45, pela regra da Parte 138: uma condição sem calibração de dispersão leva a faixa mais larga. A primeira versão desta linha escrevia a fórmula sem fazer a conta.
- **(f)** U de G = 4 em **[310; 400]**
- **(g)** U de G = 8 em **[220; 290]**
- **(h)** U de G = 16 em **[150; 210]**
- **(j)** minutos de "up" no próximo despertar agendado em **[0; 5]**

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua rodou sobre o rascunho e deu m1 = 9, m2 = 4, m3 = 0,127 e m5 = 0. E = 2,25, então m1 fica em [9; 11].
- **(m1)** nº de previsões do mundo em **[9; 11]**
- **(m2)** nº que cruzam ou tocam o zero em **[4; 6]**
- **(m3)** mediana de w em **[0,10; 0,16]**
- **(m4)** fração de acertos em **[0,55; 1,00]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 2]**

### Sobre mim, registrado
Erros no mundo em **[0; 5]**, com centro 2,25.

➡ Anterior: [Parte 144](ASI_AGI_parte144_volta9.md).

## Medido (P3197)
| G | retorno | U (grupos úteis) | desvio de b·ln(U_G/U₂) |
|---|---|---|---|
| 2 | 0,8756 | 362,0 | — |
| 4 | 0,8805 | 339,0 | +0,0071 |
| 8 | 0,8632 | 263,0 | −0,0018 |
| 16 | 0,8467 | 175,3 | −0,0050 |

- **(a)** a ordem dos retornos é a dos U: **não** (G = 4 ficou acima de G = 2). ❌
- **(b)** +0,0071. ✅
- **(c)** −0,0018. ✅
- **(d)** −0,0050. ✅
- **(e)** 362. ✅
- **(f)** 339. ✅
- **(g)** 263. ✅
- **(h)** 175,3. ✅
- **(j)** fica para o próximo despertar.

### (a): uma previsão de ordem que valia uma moeda
A relação passou: as três diferenças ficaram a menos de 0,0071 de b·ln U, com o b do outro mundo, e os U se replicaram (362, 339, 263 e 175
contra 385, 355, 256 e 179). Mas a ORDEM entre G = 2 e G = 4 não tinha como ser prevista. A diferença esperada era 0,0330·ln(362/339) = 0,0022,
e o ruído de uma diferença de duas médias é 0,0076. P(ordem certa) ≈ Φ(0,0022/0,0076)·Φ(0,0084/0,0076)·Φ(0,0134/0,0076)
= 0,612·0,865·0,961 = 0,51. Escrevi "1/24 por acaso", que é a chance de uma ordem ALEATÓRIA, e registrei como faixa de 90% uma previsão
cuja chance era a de uma moeda. É o piso do caos da Parte 30 (não prever diferenças abaixo do ruído) aplicado a uma ORDEM: cada par vizinho
é uma diferença.
