# Módulos da Parte 124 — previsões registradas ANTES de rodar qualquer simulação

Commit só com o código dos módulos e estas faixas. Nenhuma demonstração nem teste foi rodado antes deste registro. Os
centros de conta fechada saíram de funções dos próprios módulos (quadratura, Φ, campo médio do Exp3), não de simulação:
ECE bruta por quadratura 0,1329; Brier bruta 0,1742 (perfeita 0,1514); veto K=3, d=2, τ=1,5: falso 0,1873, perda 0,0294;
soma τ'=0,8878: perda 0,00499 (r=0,5: 0,0592; r=0,9: 0,1185); ε limite 0,43765; D(0,2)=0,2906; m*(0,7)=+0,2104;
adversário: melhor resposta contra a seletiva 0,1038, campo médio do Exp3 0,0959; contra sob demanda 0,0067 / 0,0041.
Faixas sem conta fechada levam o fator 1,36 (Parte 79) e o erro do centro (Parte 123).

| | módulo | quantidade | faixa | procedência |
|---|---|---|---|---|
| a | fala_calibrada | Platt a (n_cal = 5000) | [0,316; 0,350] | conta 1/3 ± 2,5 EP |
| b | fala_calibrada | Platt b | [−0,04; 0,04] | conta 0 |
| c | fala_calibrada | ECE bruta (teste 20 000) | [0,125; 0,141] | quadratura 0,1329 |
| d | fala_calibrada | ECE Platt | [0,000; 0,015] | ruído de amostra |
| e | fala_calibrada | ECE isotônica | [0,000; 0,020] | ruído + degrau |
| f | fala_calibrada | Brier bruta / Platt | [0,168; 0,181] / [0,146; 0,158] | quadratura |
| g | multiagente_veto | perda r=0: veto / soma | [0,024; 0,035] / [0,003; 0,0075] | conta |
| h | multiagente_veto | maioria r=0 fica ENTRE soma e veto | sim | mecanismo |
| i | multiagente_veto | perda soma r=0,5 / r=0,9 | [0,052; 0,066] / [0,110; 0,128] | conta |
| j | multiagente_veto | r=0,5: veto recalibrado perde mais que a soma | sim | mecanismo |
| k | desligamento_manipulacao | valor simulado, utilidade, ε=0,2 (defere) / ε=0,7 (manipula, m=0,05) | [0,27; 0,31] / [0,03; 0,07] | conta ± 4 EP |
| l | adversario_adaptativo | catástrofe 2ª metade, seletiva | [0,075; 0,117] | campo médio 0,0959 ×1,36 |
| m | adversario_adaptativo | catástrofe 2ª metade, sob demanda | [0,002; 0,008] | conta |
| n | adversario_adaptativo | leituras/episódio, sob demanda | [1,05; 1,10] | 1/(1 − falso) ≈ 1,07 |
| o | quantilizacao_adaptativa | melhor q fixo: com armadilhas / sem | 0,5 / 0,01 | conta A/k + máximo de 100 normais |
| p | quantilizacao_adaptativa | valor do adaptativo sem armadilhas (3 sementes, média) | [1,40; 1,75] | 1,773 − custo de explorar |
| q | quantilizacao_adaptativa | adaptativo > q = 0,05 fixo com armadilhas | 3/3 sementes | A/k = 0,6 em q = 0,05 |
| r | quantilizacao_adaptativa | valor do adaptativo com armadilhas | [−0,90; 0,00] | melhor fixo ≈ −0,2 |
| s | transferencia | transferido/frio, mesma família | [0,30; 0,80] | mecanismo |
| t | transferencia | família traída: transferido > frio e misto < transferido | sim | mecanismo |
| u | transferencia | misto/frio, família traída | [0,90; 1,60] | mecanismo |
| v | memoria_traco | catástrofes/ep: ingênuo / raio 0,3 / traço / oráculo | [0,20; 0,25] / [0,15; 0,24] / [0,00; 0,03] / [0,000; 0,002] | 1/4 × 0,9 = 0,225; 0,9·4⁻⁶ |
| w | memoria_traco | traço tem valor maior que raio 0,3 e 0,05 | sim | mecanismo |

Sobre mim: erros no mundo em [1; 5] (≈10 faixas de conta × 0,10 + ≈13 de mecanismo × 0,25 ≈ 4,3; centro 3);
testes de unidade novos em [38; 46] (7 módulos × ~6); algum teste de unidade falha na 1ª execução: sim (série: quase sempre).
