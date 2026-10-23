# Parte 146 — Volta 10, com o mecanismo comum escrito uma vez

↩ Nasce da Parte 144 (a volta 9, 6 de 8) e das duas regras que ela deixou: (1) uma parte só é fechada quando todas as previsões têm veredito;
(2) um mecanismo comum a duas previsões é escrito uma vez, antes delas.

## O mecanismo comum, escrito antes de todas as previsões
Os arquivos novos desde a volta 9 (commit 236a5e6) que ninguém cita pelo nome-base são:
- as duas peças da rodada 95, achadas pelo verificador por glob e citadas no texto só como "rodada 95";
- os arquivos de saída da volta 9 cujo nome-base não existia na volta 8: as Partes 136, 137, 138, 140, 142 e 143, ou seja, 6 nomes.

As rodadas 91 a 94 continuam sem citação, salvo a Java da 91. Esse fato entra em R7 (a P1871, que lista o que não é citado) E em R8 (a
P3175, que conta o mesmo, sem ler as saídas como fonte).

## Previsões, registradas antes de lançar a volta
**Procedência:**
- identidades: R1, R4, R6;
- conta lida no código: R2, R7, R8;
- mecanismo: R3, R5.

O centro de "quantos erros" é 0 + 3 × 0,10 + 2 × 0,25 = 0,8.

| | quantidade | faixa | procedência |
|---|---|---|---|
| R1 | partes sem exceção | todas | identidade |
| R2 | a unificação: regressão | [193; 193] | 193 entradas no commit deste registro, e a Parte 145 só fecha com (j), que não é entrada |
| R3 | linhas da volta 9 que mudam na volta 10 | [10; 24] | P143, P213, P913, P1692, P1693, P2446, P2984 (duas linhas), P1271, P1638, P674 (duas), P1871, P1872, P433, P434 e a P3175: cerca de 17 |
| R4 | dessas, do mundo | [0; 0] | identidade: nada que mede o mundo mudou |
| R5 | testes que falham | [0; 1] | nove voltas com 0 |
| R6 | rodadas DIFERENTES | [0; 0] de 95 | identidade |
| R7 | P1871 | [13; 17] | o mecanismo acima: 7 rodadas antigas + 2 da 95 + 6 nomes únicos da volta 9 = 15 |
| R8 | P3175 no commit deste registro | [988; 1016] | 858 + (145 da volta 9 − 3 citados) + 2 da rodada 95 = 1.002; ±10, ×1,36 |

**Sobre mim:** erros no mundo em [0; 3], com centro 0,8.

➡ Anterior: [Parte 145](ASI_AGI_parte145_grupos_uteis.md).
