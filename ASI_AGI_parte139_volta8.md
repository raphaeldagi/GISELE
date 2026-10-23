# Parte 139 — O resultado da volta 8, e a GRPO bit a bit (rodada 92)

↩ Nasce da Parte 135 (o registro da volta 8, R1 a R8) e da Parte 137 (a GRPO de `rl_grupos.py`).

## A rodada 92, prevista antes de rodar
A tradução do passo de treino da GRPO (log-softmax, vantagem do grupo, razão de importância recortada, KL contra a uniforme e SGD) para Java:
16 contextos e as amostras de um LCG, 64 grupos de 4 e 3 passes por grupo. O log-softmax usa o exp e o log PRÓPRIOS da rodada 26. As somas
são em laço. A amostragem compara u com a CDF acumulada na mesma ordem.

| | quantidade | faixa | procedência |
|---|---|---|---|
| G1 | a rodada 92 | IGUAIS | só + − × ÷ e √ IEEE, mais o exp e o log próprios (que já deram IGUAIS em 26 rodadas); o recorte e o argmax são comparações de valores que já são iguais |
| G2 | o gradiente da tradução contra o do módulo real (math.exp, sum compensado), nos mesmos dados | \|dif\| < 1e-12 | a tradução e o módulo diferem só no último bit do exp e da soma |

Registrado antes da primeira execução da rodada.

## Medido
| | medido | faixa | |
|---|---|---|---|
| G1 | IGUAIS, 18 linhas e 16 números bit a bit | IGUAIS | ✅ |
| G2 | a asserção passou: \|dif\| < 1e-12 | < 1e-12 | ✅ |

**Mundo: 2 de 2.** O retorno exato médio depois de 256 ações foi 0,7548, contra 1/3 da política uniforme. A volta 8 ainda roda, e o resultado
dela vai para a Parte 135 (onde está o registro) e para a Parte 141.

➡ Anterior: [Parte 138](ASI_AGI_parte138_transferencia.md). ➡ Próxima: [Parte 140](ASI_AGI_parte140_leitor_dicionario_hex.md).
