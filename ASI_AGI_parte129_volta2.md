# Parte 129 — Volta 2 do loop: refazer tudo de novo e comparar com a volta 1

↩ Nasce da Parte 128 (a volta 1) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que esta volta testa
A volta 1 comparou a reprodução com o `resultados.txt`, que guarda cada parte como ela era no dia em que foi escrita. A volta 2 compara
uma reprodução com a OUTRA: as duas foram feitas do zero, na mesma máquina, com um intervalo de poucas horas. O que muda entre elas é só o
que mudou no repositório entre os dois commits (245584a → este) e o que muda com a máquina.

Entre os dois commits mudaram:
- o `calculos.py`: as funções P3171–P3174 e a Parte 128;
- o CLAUDE.md;
- o `resultados.txt`: a seção da Parte 91 e a saída da Parte 128, no fim;
- os testes da Parte 128 e a pasta `reproducao/`.

O mecanismo, escrito antes: só as medidas que leem esses arquivos mudam. São P143 (o CLAUDE.md), P213 (a regressão, que agora tem
168 entradas), P1692 (o número de funções), P1871/P1872 (os arquivos), as que leem o `resultados.txt` inteiro (P913 e as que contam
partes) e a velocidade da máquina (P433, P434).

O procedimento é o da Parte 128: um clone limpo do GitHub no commit desta parte, 16 blocos retomáveis e a comparação pela
`p3174_comparar_voltas` (volta 1 contra volta 2).

## Previsões, registradas antes de qualquer execução da volta 2
A procedência das faixas foi contada antes do centro de "quantos erros" (regra da Parte 128):
- identidades: V1, V4 e V6;
- de mecanismo: V2, V3 e V5.
O centro de erros esperados é 3 × 0 + 3 × 0,25 ≈ 0,75.

| | quantidade | faixa | procedência |
|---|---|---|---|
| V1 | blocos sem exceção | todos (16 de 16) | identidade: o mesmo código já rodou na volta 1 |
| V2 | blocos com a regressão completa (168/168) | [15; 16] | P(um) ≈ 0,99 → P(16/16) ≈ 0,85 |
| V3 | linhas da volta 1 que mudam na volta 2 (sem a Parte 128) | [8; 30] | mecanismo: as medidas listadas acima, ~1 linha cada, mais a máquina |
| V4 | dessas, do MUNDO | [0; 0] | identidade: o mesmo código, a mesma semente e a mesma máquina dão o mesmo número; uma linha do mundo diferente seria um defeito |
| V5 | testes que falham no clone (suíte + revisado + laboratório + entregas) | [0; 1] | a volta 1 teve 0 |
| V6 | rodadas DIFERENTES | [0; 0] de 90 | identidade: nenhuma rodada mudou |

**Sobre mim:** erros no mundo em [0; 2], com centro 0,75.
