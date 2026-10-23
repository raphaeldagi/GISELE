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

## Medido (P3176; as saídas ficam em `reproducao/volta7/`)
| | medido | faixa | |
|---|---|---|---|
| Q1 | 130 de 130 partes sem exceção | todas | ✅ |
| Q2 | a unificação: **173/173** | [173; 173] | ✅ |
| Q3 | **9** de 1.886 linhas mudaram | [6; 12] | ✅ (exatamente as 9 listadas no registro) |
| Q4 | **0** do mundo (7 do projeto, 2 da máquina) | [0; 0] | ✅ |
| Q5 | **0** falhas: 729 + 27 + 40 + 72 + 55 | [0; 1] | ✅ |
| Q6 | **0** DIFERENTES; as 90 IGUAIS | [0; 0] | ✅ |
| Q7 | P1871: **1** (a saída de nome novo da volta 6) | [0; 2] | ✅ (a conta dava 1) |
| Q8 | P3175: **586** | [575; 597] | ✅ (a conta dava 586, exato) |

**Mundo: 8 de 8.** **Sobre mim: 1 de 1.** Previ de 0 a 3 erros e tive 0.

### A volta inteira foi prevista linha por linha
As nove linhas que mudaram são EXATAMENTE as nove que o registro nomeou: P143, P213, P913, P1692, P2446, P1872, P433, P434 e a linha da
P3175 na Parte 131. Não há nenhuma a mais nem a menos, e as duas contagens de arquivos deram o número da conta. Pela primeira vez no
loop, o efeito de um commit sobre as medidas do projeto foi previsto inteiro antes de rodar. A volta 7 não descobriu nada: confirmou,
linha a linha, um modelo do próprio projeto que eu montei ao longo das voltas 1 a 6.

### O que isso diz, e o que eu proponho
- **O loop chegou ao ponto fixo do que ele consegue medir.** As voltas não acham mais diferenças do mundo (sete voltas, 0), e as do projeto
  agora são previstas inteiras. É a contração da Parte 101 no meu próprio procedimento: repetir a mesma operação converge para um ponto
  fixo, e ali cada volta nova acrescenta só a confirmação.
- **O que continua valendo:** cada volta prova de novo, do zero, que o projeto inteiro roda e reproduz. Isso tem valor como verificação,
  mas o custo é de cerca de 1,5 h de relógio e 4 h de processador por volta, e o ganho de informação de cada uma já é quase nulo.
- **A decisão conservadora** (Parte 70: quando a pergunta seria para o usuário, decidir pela regra mais conservadora e escrever a decisão)
  é seguir o pedido "loop infinito" enquanto ele não for revogado. Mas a partir daqui as voltas são espaçadas: uma volta nova só começa
  depois que o commit da anterior mudou algo além do próprio registro da volta, ou a cada 6 horas no máximo. Uma volta que só confirmaria
  o mesmo ponto fixo gasta processador sem medir nada novo. Escrevo isto para que quem lê possa dizer "pare", "continue igual" ou
  "volte ao ciclo de partes novas" sabendo o que cada uma custa.

## Funções e testes
- **Funções:** `_parte_134`. A entrada `P3176v7` foi para a regressão, que agora tem 174 entradas.
- **Testes:** `test_volta7_regressao`.

➡ Anterior: [Parte 133](ASI_AGI_parte133_volta6.md).
