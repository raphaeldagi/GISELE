# Parte 141 — O resultado da volta 8, e o reservatório e o posto efetivo bit a bit (rodada 93)

↩ Nasce da Parte 135 (o registro da volta 8) e da Parte 137 (`synthai/reservatorio.py`, de `aprendizagem_continua.py`).

## A rodada 93, prevista antes de rodar
Um fluxo de 64 vetores de 4 dimensões vem de um LCG. O reservatório de 16 é o `synthai.reservatorio.Reservatorio` REAL, com o gerador
trocado por um que tira randrange(n) = ⌊u·n⌋ do mesmo LCG; o Java faz o mesmo. Depois vem o posto efetivo da matriz 16 × 4 guardada:
centrar, ZᵀZ, autovalores por Jacobi cíclico (a mesma ordem de rotações) e exp(−Σp ln p) com o exp e o log próprios da rodada 26.

| | quantidade | faixa | procedência |
|---|---|---|---|
| H1 | os 16 índices guardados | iguais | o reservatório só compara inteiros |
| H2 | o posto efetivo | IGUAL bit a bit | o Jacobi usa só + − × ÷ e √, na mesma ordem de varredura; o posto usa o exp e o log próprios |
| H3 | o posto da tradução contra o `posto_efetivo` do módulo (math.log, sum compensado) | \|dif\| < 1e-12 | os dois diferem só no último bit |

Registrado antes da primeira execução da rodada.
