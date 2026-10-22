# Parte 130 — Volta 3 do loop

↩ Nasce da Parte 129 (a volta 2) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que esta volta testa
É a terceira repetição de tudo: um clone limpo, as 126 partes (contadas pelo lançador, no blocos.txt; a primeira versão deste texto dizia 125, de cabeça, pela segunda vez no loop), todos os testes e as 90 rodadas. Ela é lançada por um script só,
`reproducao/nova_volta.sh`, para que cada volta seja feita do mesmo jeito. A comparação é volta 2 contra volta 3 (`p3174_comparar_voltas`).

Entre os commits 1c15dda (volta 2) e o desta parte mudaram:
- o `calculos.py`: a `_parte_129` e a entrada de regressão P3174;
- o CLAUDE.md, o `resultados.txt` (com a saída da Parte 129) e os testes;
- `reproducao/volta2/` (22 arquivos) e `reproducao/nova_volta.sh`.

O mecanismo vem da tabela da Parte 129. Cada mudança acima mexe numa medida conhecida:
- **P143:** o CLAUDE.md cresceu;
- **P213:** a regressão passa de 168/168 para 169/169;
- **P913:** o `resultados.txt` cresceu;
- **P1692:** uma função a mais, a `_parte_129`;
- **P1871 e P1872:** os arquivos não citados. Pela leitura de menção da Parte 129, eram 22 na volta 2. Agora entram os 22 arquivos da
  volta 2, dos quais se espera que 21 fiquem sem citação, como aconteceu com os da volta 1, mais o `nova_volta.sh`, que nenhum arquivo
  versionado cita. A conta: 22 + 21 + 1 = 44;
- **P433 e P434:** a máquina;
- **P2446:** não deve mudar, porque não há pNN nova (a `_parte_129` não é pNN).

## Previsões, registradas antes de lançar a volta
Antes do centro de "quantos erros", contei a procedência das faixas (regra da Parte 128):
- identidades: W1, W4, W6;
- conta: W7, com uma cauda de ±2 para os arquivos que eu não li um a um;
- mecanismo: W2, W3, W5.

O centro de erros esperado é 0,10 + 3 × 0,25 ≈ 0,85.

| | quantidade | faixa | procedência |
|---|---|---|---|
| W1 | blocos sem exceção | todos | identidade |
| W2 | blocos com a regressão 169/169 | [15; 16] de 16 | P(16/16) ≈ 0,85 |
| W3 | linhas da volta 2 que mudam na volta 3 (sem as Partes 128 e 129) | [5; 12] | mecanismo: as 6 a 8 medidas listadas acima |
| W4 | dessas, do mundo | [0; 0] | identidade |
| W5 | testes que falham | [0; 1] | as voltas 1 e 2 tiveram 0 |
| W6 | rodadas DIFERENTES | [0; 0] de 90 | identidade |
| W7 | P1871: arquivos "não referenciados" | [42; 46] | conta 22 + 21 + 1 = 44 |

**Sobre mim:** erros no mundo em [0; 2], com centro 0,85.

## Medido (P3174; as saídas ficam em `reproducao/volta3/`)
| | medido | faixa | |
|---|---|---|---|
| W1 | 16 de 16 blocos sem exceção | todos | ✅ |
| W2 | 16 de 16 com a regressão **169/169** | [15; 16] | ✅ |
| W3 | **8** de 1.875 linhas mudaram (0,43%) | [5; 12] | ✅ |
| W4 | **0** do mundo (6 do projeto, 2 da máquina) | [0; 0] | ✅ |
| W5 | **0** falhas: 723 + 27 + 40 + 72 + 55 testes | [0; 1] | ✅ |
| W6 | **0** DIFERENTES; as 90 rodadas IGUAIS | [0; 0] | ✅ |
| W7 | P1871: **1** arquivo "não referenciado" | [42; 46] | ❌ (a conta dava 44) |

**Mundo: 6 de 7.** **Sobre mim: 1 de 1.** Previ de 0 a 2 erros e tive 1. Tempo: 6,3 h de processador (as voltas 1 e 2 levaram 7,1 h e 6,6 h).

### As 8 linhas, cada uma com a sua causa
- **P143:** o CLAUDE.md passou de 88.529 a 88.988 caracteres (a regra da Parte 129).
- **P213:** a regressão passou de 168/168 a 169/169.
- **P913:** o `resultados.txt` passou de 13.003 a 13.035 números (a saída da 129).
- **P1692:** de 954 a 955 funções (a `_parte_129`).
- **P1871 e P1872:** de 22 a 1, abaixo.
- **P433 e P434:** a máquina. A velocidade foi 2,06 → 4,12 → 2,38·10⁷ adições por segundo nas três voltas: ela oscila, não cresce, e
  a causa continua não medida.
- **P2446 não mudou**, como previsto (nenhuma pNN nova).

### Por que W7 errou: conferi a régua antes de explicar
Lendo o código da P1871, na parte (c), um arquivo conta como citado se o seu NOME-BASE (com ou sem a extensão) aparece em QUALQUER outro
arquivo versionado. Dois mecanismos, os dois conferidos:
1. **Os nomes-base se repetem entre as voltas.** `reproducao/volta1/bloco_1_2_3_4_5_6_7_8.txt` e `reproducao/volta2/bloco_1_2_3_4_5_6_7_8.txt`
   têm o mesmo nome-base, e um "cita" o outro. Na volta 2 os arquivos da volta 1 não tinham irmão; agora os das voltas 1 e 2 têm.
2. **A auditoria da volta anterior cita os arquivos que acusou.** A saída da P1872 na volta 2 diz "sem uso: 21 ['reproducao/volta1/…']".
   Essa linha está versionada, e os 21 acusados passam, por isso mesmo, a ser "citados" na volta seguinte. Conferido por `grep`: o
   caminho `reproducao/volta1/bloco_1_2_3_4_5_6_7_8.txt` aparece 1 vez no bloco 81 da volta 2.
   **Uma auditoria que acusa alguém o absolve na rodada seguinte.**

Sobrou só o arquivo de nome NOVO da volta 2: `bloco_122_123_126_127_128.txt`, porque na volta 1 o último bloco não tinha a Parte 128.

**O que o erro diz sobre mim.** A minha conta (22 + 21 + 1) estava certa sobre o que eu imaginava que a P1871 fazia ("o arquivo é citado
pelo caminho"), e errada sobre o que ela faz (pelo nome-base, lendo as próprias saídas). É a regra da Parte 75 de novo: prever a
propriedade de um conjunto de arquivos a partir da IMAGEM que eu tenho do código, e não de uma leitura do código. Na Parte 129 eu
expliquei a queda 130 → 22 pela menção, e certo. Mas não li a linha que diz QUE nome é procurado; com ela, a conta teria dado 1.

### Engenharia reversa
- **Três voltas, 0 diferenças do mundo nas três.** A reprodução está estável; o que muda é só a assinatura de cada commit.
- **O loop virou um instrumento que mede o efeito de cada commit nas medidas do próprio projeto.** E, nesta volta, mostrou que uma
  dessas medidas (a P1871) deixou de medir o que diz assim que as próprias medições foram versionadas. Um auditor que lê o arquivo
  em que o seu veredito é guardado.
- **Regra nova (Parte 130):** antes de prever um número que uma função conta sobre arquivos, ler as linhas da função que dizem O QUE ela
  casa (o padrão, o nome, o caminho), e não só a docstring.

## Funções e testes
- **Funções:** `_parte_130`. A entrada `P3174v3` foi para a regressão, que agora tem 170 entradas.
- **Testes:** `test_volta3_regressao`, em `synthai/testes_parte128.py`.

## Loop
A volta 4 começa num clone novo, no commit desta parte. A continuação está agendada; para parar, basta dizer "pare".

➡ Anterior: [Parte 129](ASI_AGI_parte129_volta2.md).

➡ Próxima: [Parte 131 — volta 4](ASI_AGI_parte131_volta4.md).
