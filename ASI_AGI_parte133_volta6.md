# Parte 133 — Volta 6 do loop

↩ Nasce da Parte 132 (a volta 5) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que muda entre a volta 5 e esta
- O `calculos.py` ganhou a `_parte_132` e a entrada P3174v5.
- O CLAUDE.md, o `resultados.txt` e os testes cresceram.
- `reproducao/volta5/` entrou: 128 saídas de parte com os MESMOS nomes-base das da volta 4, mais uma nova (a da Parte 131), a unificação e
  os 6 dos testes.

O mecanismo, lido no código da P1871 (regras das Partes 130 e 131):
- **As saídas das voltas 4 e 5 se citam umas às outras:** os nomes-base são iguais, e a saída da P1872 da volta 5 lista as da volta 4.
- **Fica sem citação só a saída de parte de nome novo da volta 5.** Não escrevo o nome dela aqui, pela regra da Parte 131.
- **A da Parte 1 é citada pelo meu código.**

## Previsões, registradas antes de lançar a volta e antes de rodar a P3175 neste commit
**Procedência:**
- identidades: Z1, Z4, Z6;
- de mecanismo, com a leitura do código: Z2, Z3, Z5, Z7, Z8.

O centro de "quantos erros" é 5 × 0,25 ≈ 1,25.

| | quantidade | faixa | procedência |
|---|---|---|---|
| Z1 | partes sem exceção | todas (129) | identidade |
| Z2 | a unificação: 172/172 | [172; 172] | P ≈ 0,99 |
| Z3 | linhas da volta 5 que mudam na volta 6 | [5; 12] | P143, P213, P913, P1692 (+1), P1871 e P1872 (126 → ~1), P433/P434 |
| Z4 | dessas, do mundo | [0; 0] | identidade |
| Z5 | testes que falham | [0; 1] | cinco voltas com 0 |
| Z6 | rodadas DIFERENTES | [0; 0] de 90 | identidade |
| Z7 | P1871 na volta 6 | [0; 2] | conta: 1 (a saída de nome novo da volta 5) |
| Z8 | P3175 neste commit | [440; 466] | conta: 321 + 127 saídas de parte da volta 5 (a da Parte 1 é citada pelo código) + 5 dos testes = 453 |

**Sobre mim:** erros no mundo em [0; 3], com centro 1,25.

## Nota de procedimento (04h37 UTC, antes de qualquer resultado da volta)
O contêiner reiniciou às 04h37 (uptime 0 min), no meio da volta 6, COM a espera em segundo plano e a vigilância ativas. Isso derruba a
hipótese da Parte 131 ("o contêiner é recolhido por inatividade entre turnos"). Ela era de um lote só e foi refutada no segundo. Os
reinícios acontecem também com tarefas ativas; a causa é do ambiente e eu não a conheço. O que funcionou foi o procedimento por parte,
não a espera: 73 partes sobreviveram ao reinício e a volta continuou de onde parou. A regra da Parte 66 se cumpriu ao pé da letra:
escrevi como hipótese, e por isso não precisei desdizer uma conclusão.
