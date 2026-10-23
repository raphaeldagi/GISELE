# Parte 134 — Volta 7 do loop

↩ Nasce da Parte 133 (a volta 6) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que muda entre a volta 6 e esta
- O `calculos.py` ganhou `p3176_comparar_voltas_v2` (uma pNN nova, que mede o PROJETO e por isso já nasce na `_PROJETO_P133`, pela regra da
  Parte 133), a `_parte_133` e a entrada P3176.
- `reproducao/volta6/` entrou: 129 saídas de parte com os mesmos nomes-base das da volta 5, mais uma de nome novo (a da Parte 132),
  além dos arquivos dos testes.

A comparação desta volta usa a P3176.

O mecanismo, lido no código:
- **P1871:** a saída de nome novo da volta 5 passa a ser citada pela P1872 da volta 6, que a listou. A da volta 6 fica sem citação.
- **P3175** (pela linha da Parte 131): cresce com as 128 saídas de parte da volta 6 que ninguém cita fora das saídas (a da Parte 1 é
  citada pelo código), mais os 5 dos testes.
- **P2446:** passa de 722 a 723 pNN.
- **P1692:** passa de 959 a 961 funções.

## Previsões, registradas antes de lançar
**Procedência:**
- identidades: Q1, Q4, Q6;
- de mecanismo: Q2, Q3, Q5, Q7, Q8.

O centro de "quantos erros" é ≈ 1,25.

| | quantidade | faixa | procedência |
|---|---|---|---|
| Q1 | partes sem exceção | todas (130) | identidade |
| Q2 | a unificação: 173/173 | [173; 173] | P ≈ 0,99 |
| Q3 | linhas da volta 6 que mudam na volta 7 | [6; 13] | P143, P213, P913, P1692, P2446, P1872, P433, P434 e a linha da P3175 na Parte 131: 9 |
| Q4 | do mundo, pela P3176 | [0; 0] | identidade |
| Q5 | testes que falham | [0; 1] | seis voltas com 0 |
| Q6 | rodadas DIFERENTES | [0; 0] | identidade |
| Q7 | P1871 na volta 7 | [0; 2] | conta: 1 |
| Q8 | P3175 neste commit | [575; 597] | conta: 453 + 128 + 5 = 586 |

**Sobre mim:** erros no mundo em [0; 3], com centro 1,25.
