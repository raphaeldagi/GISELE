# Parte 144 — Volta 9, a primeira depois dos módulos novos

↩ Nasce da volta 8 (Partes 135 e 141) e do pedido de não parar. É a primeira volta que reproduz, num clone limpo, as Partes 136 a 143: os
módulos tirados do que foi recebido, o leitor v5 e as rodadas 91 a 94.

## O que muda entre o commit da volta 8 (4363101) e este
- 8 partes novas (136 a 143), com 20 funções pNN e 4 módulos novos;
- 4 rodadas novas do diálogo (91 a 94), com 8 arquivos (`rodadaNN.py` e `RodadaNN.java`);
- as saídas da volta 8 (`reproducao/volta8/`, 139 arquivos);
- o CLAUDE.md, o `resultados.txt` e a regressão, que passa de 174 para 191 entradas.

**O mecanismo novo:** as Partes 140, 142 e 143 têm a linha de placar que a régua v4 lê. As funções ANTIGAS que leem uma faixa crescente de
partes (a P1961 e as que a usam: os 28 rótulos da Parte 128) vão ver previsões novas e mudar de valor. A P1961 está na lista do projeto da
P3176. As outras eu não li uma a uma, e por isso R3 tem faixa larga e R4 vem com o aviso de que uma linha de projeto pode ser classificada
como "mundo".

## Previsões, registradas antes de lançar a volta
**Procedência:**
- identidades: R1, R6;
- conta lida no código: R2, R7, R8;
- mecanismo pouco conhecido: R3, R4, R5.

O centro de "quantos erros" é 0 + 3 × 0,10 + 3 × 0,25 = 1,05.

| | quantidade | faixa | procedência |
|---|---|---|---|
| R1 | partes sem exceção | todas | identidade |
| R2 | a unificação: regressão | [191; 191] | 190 entradas até a Parte 143, mais a P3176v8 |
| R3 | linhas da volta 8 que mudam na volta 9 | [9; 40] | as 8 de sempre (P143, P213, P913, P1692, P1872, P433, P434, a P3175), mais P2446 (pNN novas) e as réguas de faixa crescente, de 0 a cerca de 28 |
| R4 | dessas, classificadas como "mundo" pela P3176 | [0; 3] | 0 de mundo real; uma régua antiga de faixa crescente fora da lista do projeto apareceria aqui |
| R5 | testes que falham | [0; 1] | oito voltas com 0 |
| R6 | rodadas DIFERENTES | [0; 0] de 94 | identidade |
| R7 | P1871 | [0; 2] | só o arquivo de nome único da volta 8 fica sem irmão, e eu não escrevo o nome dele |
| R8 | P3175 no commit deste registro | [850; 878] | 720 + (139 arquivos da volta 8 − 3 citados nos documentos) + 8 arquivos das rodadas 91 a 94 (o verificador os acha por glob, ninguém os cita pelo nome) = 864; ±10, ×1,36 |

**Sobre mim:** erros no mundo em [0; 3], com centro 1,05.

➡ Anterior: [Parte 143](ASI_AGI_parte143_replicas.md).

**R8, medida no commit do registro (236a5e6): 858**, dentro de [850; 878] ✅, mas 6 abaixo do centro da conta (864). A conferência por código
explica 2 dos 6:
- das 8 rodadas novas, 7 ficaram sem uso, porque `dialogo/Rodada91.java` é citado pelo nome no texto da Parte 136;
- da volta 8 ficaram 135 sem uso, e não 136.

Os 4 restantes saem de 720 + 135 + 7 = 862 contra 858: arquivos que já eram acusados antes e que os textos novos (Partes 136 a 143) passaram a
citar. A conta pela imagem do que eu escrevi, de novo, não incluiu o meu próprio texto como leitor (a lição da Parte 132).
