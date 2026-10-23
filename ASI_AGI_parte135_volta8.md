# Parte 135 — Volta 8, sem pausa, e o começo de "use tudo que enviei em cada módulo"

↩ Nasce da Parte 134 e do pedido novo do usuário: "Continue e não pare nunca mais sem precisar interagir comigo. A cada avanço me envie o
arquivo consolidado. Use tudo que enviei até hoje em cada módulo."

## O pedido muda a decisão da Parte 134
A Parte 134 decidiu espaçar as voltas e deixou a escolha com o usuário. O usuário escolheu: **não parar**. A partir daqui:
1. **As voltas rodam sem pausa**, em segundo plano, uma atrás da outra. Elas são a verificação contínua de que tudo ainda reproduz.
2. **O trabalho de frente volta a ser construir.** O pedido "use tudo que enviei até hoje em cada módulo" vira um programa de partes. Cada
   coisa recebida (os textos em `externos/`, os pacotes em `synthai/revisado/` e `entregas/`, os pedidos gravados no CLAUDE.md) é
   inventariada por código, e cada módulo diz quais dessas peças ele usa. O que ainda não é usado vira trabalho das próximas partes.
3. **O `SYNTHAI_completo.py` vai a cada avanço** (cada commit de parte), não só no fim da mensagem.
4. **"Tudo" respeita a fronteira que vale desde a Parte 84.** Rede, auto-replicação (subprocess de si mesmo, fork, exec_module) e
   eval/exec de código recebido continuam recusados, como nas doze recusas anteriores. Do que foi enviado com essas capacidades, entra a
   ideia segura, reescrita offline em biblioteca padrão, como sempre.

## Previsões da volta 8, registradas antes de lançá-la
**Procedência:**
- identidades: R1, R4, R6;
- conta lida no código: R7, R8;
- mecanismo: R2, R3, R5.
O centro de "quantos erros" é 3 × 0 + 2 × 0,10 + 3 × 0,25 ≈ 0,95.

| | quantidade | faixa | procedência |
|---|---|---|---|
| R1 | partes sem exceção | todas | identidade |
| R2 | a unificação: regressão | [174; 174] | a entrada P3176v7 entrou no commit da 134 |
| R3 | linhas da volta 7 que mudam na volta 8 | [6; 11] | P143, P213, P913, P1692 (+1, a `_parte_134`), P1872 (o arquivo de nome novo da volta 7), P433, P434 e a linha da P3175 na Parte 131: 8. P2446 não muda (nenhuma pNN nova antes de lançar) |
| R4 | dessas, do mundo | [0; 0] | identidade |
| R5 | testes que falham | [0; 1] | sete voltas com 0 |
| R6 | rodadas DIFERENTES | [0; 0] de 90 | identidade |
| R7 | P1871 | [0; 2] | o mecanismo das Partes 130–133: só o arquivo de nome único da volta 7 fica sem irmão, e eu não escrevo o nome dele |
| R8 | P3175 no commit deste registro | [706; 734] | 586 + 137 arquivos da volta 7 − 3 (os nomes `unificacao.txt` e os de testes são citados nos documentos, como na volta 6: 136 arquivos deram +133) = 720; ±10, ×1,36 |

**Sobre mim:** erros no mundo em [0; 3], com centro 0,95.

➡ Anterior: [Parte 134](ASI_AGI_parte134_volta7.md).

## Medido (P3176; as saídas ficam em `reproducao/volta8/`)
| | medido | faixa | |
|---|---|---|---|
| R1 | 131 de 131 partes sem exceção | todas | ✅ |
| R2 | a unificação: 174/174 | [174; 174] | ✅ |
| R3 | 8 de 1.888 linhas mudaram | [6; 11] | ✅ (exatamente as 8 nomeadas: P143, P213, P913, P1692, P1872, P433, P434 e a P3175 da Parte 131) |
| R4 | 0 do mundo (6 do projeto, 2 da máquina) | [0; 0] | ✅ |
| R5 | 0 falhas: 730 + 27 + 40 + 72 + 55 testes | [0; 1] | ✅ |
| R6 | 0 DIFERENTES; as 90 rodadas IGUAIS | [0; 0] | ✅ |
| R7 | P1871: 1 (a saída de nome novo da volta 7) | [0; 2] | ✅ |
| R8 | P3175: 720 | [706; 734] | ✅ (a conta dava 720, exato) |

**Mundo: 8 de 8.** **Sobre mim:** 0 erros, em [0; 3]: ✅. A volta 8 morreu duas vezes com reinícios do contêiner (às 15h35 e às 16h37) e foi
retomada parte a parte nas duas: o procedimento da Parte 131 funcionou exatamente para isso.

➡ Próxima: [Parte 136](ASI_AGI_parte136_passo_e_auditor.md).
