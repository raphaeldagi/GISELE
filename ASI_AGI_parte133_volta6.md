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
O contêiner reiniciou de novo por volta das 04h57, com 128 partes prontas: faltavam uma parte e a unificação. A volta foi retomada e
terminou às 05h00.

## Medido (P3174, P3176; as saídas ficam em `reproducao/volta6/`)
| | medido | faixa | |
|---|---|---|---|
| Z1 | 129 de 129 partes sem exceção | todas | ✅ |
| Z2 | a unificação: **172/172** | [172; 172] | ✅ |
| Z3 | **9** de 1.884 linhas mudaram | [5; 12] | ✅ |
| Z4 | **1** do "mundo" pela P3174, a régua registrada | [0; 0] | ❌ (abaixo: é do projeto, mas a régua não sabia) |
| Z5 | **0** falhas: 727 + 27 + 40 + 72 + 55 | [0; 1] | ✅ |
| Z6 | **0** DIFERENTES; as 90 IGUAIS | [0; 0] | ✅ |
| Z7 | P1871: **1** (a saída de nome novo da volta 5) | [0; 2] | ✅ (a conta dava 1, exato) |
| Z8 | P3175: **453** | [440; 466] | ✅ (a conta dava 453, exato) |

**Mundo: 7 de 8.** **Sobre mim: 1 de 1.** Previ de 0 a 3 erros e tive 1.

### Por que Z4 errou: a régua não conhecia uma medida que eu mesma criei
A linha acusada é a da Parte 131 que imprime a P3175 ("arquivos sem uso… neste repositório: 321 → 453"). Ela conta arquivos do PROJETO,
e o número cresce porque eu versionei a volta 5. Mas a lista de medidas do projeto (`_PROJETO_P128`) foi escrita na Parte 128, antes de a
P3175 existir. A P3174 classifica pelo número da pergunta e chamou-a de "mundo".
- **A falha fica no placar** (regra da Parte 74). A correção é uma versão nova que não edita a antiga: `_PROJETO_P133` (com a 3175) e
  `p3176_comparar_voltas_v2`, que reclassifica. Com ela, a volta 6 tem 0 diferenças do mundo.
- **O teste dela tem os dois controles:** a P3175 tem de sair do "mundo", e uma linha do mundo de verdade tem de continuar acusada.
- **O padrão:** toda lista escrita à mão envelhece no commit seguinte. A P3175 nasceu duas partes depois da lista, numa parte que eu mesma
  escrevi, e ninguém a acrescentou. É a regra da Parte 128 ("todo rótulo vem da mesma variável que ele mede") ainda não aplicada às
  minhas próprias listas.
- **Regra nova (Parte 133):** toda pNN nova que mede o projeto entra na lista do projeto no mesmo commit em que nasce. Na próxima volta,
  a comparação usa a P3176.

### As duas contagens de arquivos acertaram o número exato
Z7 (1) e Z8 (453) acertaram o centro exato. É a segunda vez seguida que a regra da Parte 130 (ler o código antes de prever uma contagem
de arquivos) dá o número, e não só a faixa: na volta 5 o erro foi 1, e agora 0.

### Os reinícios, contados
Houve reinícios às 04h37 e por volta das 04h57, os dois COM a espera e a vigilância ativas. A hipótese da Parte 131 (recolhimento por
inatividade) está refutada em dois lotes. Somando as voltas 4, 5 e 6, foram sete reinícios ou mortes em cerca de 8 horas, sem
relação com o que eu deixo rodando. O procedimento por parte foi o que manteve o progresso.

## Funções e testes
- **Funções:** `p3176_comparar_voltas_v2` (com `_PROJETO_P133`) e `_parte_133`. A entrada `P3176` foi para a regressão, que agora tem 173
  entradas.
- **Testes:** `test_p3176_comparar_voltas_v2` (com os dois controles) e `test_volta6_regressao`.

## Loop
A volta 7 começa no commit desta parte e compara com a P3176. Para parar, basta dizer "pare".

➡ Anterior: [Parte 132](ASI_AGI_parte132_volta5.md).
