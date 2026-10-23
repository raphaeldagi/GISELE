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

## Medido (P3176; as saídas ficam em `reproducao/volta9/`)
| | medido | faixa | |
|---|---|---|---|
| R1 | 137 de 137 partes sem exceção | todas | ✅ |
| R2 | a unificação: **189/191**, com falhas P3188 e P3191 | [191; 191] | ❌ |
| R3 | 17 de 1.890 linhas mudaram | [9; 40] | ✅ |
| R4 | 0 do mundo (15 do projeto, 2 da máquina) | [0; 3] | ✅ |
| R5 | 0 falhas: 731 + 27 + 40 + 72 + 55 testes | [0; 1] | ✅ |
| R6 | 0 DIFERENTES; as 94 rodadas IGUAIS | [0; 0] | ✅ |
| R7 | P1871: **8** (7 rodadas novas achadas por glob + 1 arquivo da volta 8) | [0; 2] | ❌ |
| R8 | P3175: 858 | [850; 878] | ✅ |

**Mundo: 6 de 8.** **Sobre mim:** 2 erros, em [0; 3]: ✅.

### R2: a volta achou uma regressão vermelha no repositório
A P3188 e a P3191 fixavam contagens sobre as Partes 128 a 138, que eu tinha chamado de fechadas na Parte 141. Mas depois de fixá-las escrevi
a tabela de vereditos da volta 8 DENTRO da Parte 135, para a régua lê-la. A 135 ganhou 8 previsões com veredito, e as duas entradas passaram
a falhar: (83, 76) virou (91, 84), e (472, 425) virou (480, 433). Ninguém viu, porque depois disso eu não rodei a regressão inteira no
repositório. O loop de reprodução viu. É a primeira vez em nove voltas que o loop acha um defeito do projeto que a rotina deixou passar. As
duas entradas e o teste da Parte 140 foram atualizados, com a justificativa de fora do código (os 8 vereditos da 135), e as falhas continuam
neste placar (regra da Parte 74).

**A regra da Parte 141, revista:** uma parte só é FECHADA quando todas as previsões que ela registrou têm veredito, inclusive as de uma volta
que ainda roda. Uma parte que registra uma volta fica aberta até a volta terminar.

### R7: o mesmo mecanismo, aplicado a uma previsão e esquecido na outra
Na conta de R8 contei que as rodadas novas não são citadas pelo nome (o verificador as acha por glob). Na de R7, a mesma P1871 das voltas
anteriores, esqueci isso: as 7 rodadas novas aparecem na lista. As duas previsões dependiam do mesmo fato, e eu o apliquei a uma só.
**Regra (Parte 144):** quando duas previsões do mesmo registro dependem do mesmo mecanismo, o mecanismo é escrito UMA vez, antes das duas, e
as duas o citam.

➡ Próxima: [Parte 145](ASI_AGI_parte145_grupos_uteis.md).
