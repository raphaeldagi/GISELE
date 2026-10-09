# Como eu construiria uma AGI/ASI — Parte 51 (0x33): a memória curta e a longa

> Continuação da [Parte 50](ASI_AGI_parte50_a_vida_das_coisas.md). **Em andamento: previsões registradas antes de qualquer execução.** A Parte 50 achou
> que a memória longa da série vem do **cotovelo** (cada parte divide muito com a vizinha). Esta parte testa se o cotovelo é uma memória curta somada a uma
> longa, mede que parte da taxonomia inglesa o português cobre, e procura a constante de Kaprekar do hexadecimal.

## As perguntas desta parte

1. **P971 (0x3CB).** Duas exponenciais (curta e longa) explicam a deriva melhor que a potência, cobrando os parâmetros (AIC)? (Rodada 25) ↩ P941
2. **P972 (0x3CC).** O português (OpenWordNet-PT) cobre mais os conceitos gerais que os específicos? ↩ P793
3. **P973 (0x3CD).** Hexadecimal: a rotina de Kaprekar com 4 dígitos hexadecimais tem um ponto fixo, como o 6174 do decimal?
4. **P974 (0x3CE).** Engenharia reversa. **P975 (0x3CF).** Jung. **P976 (0x3D0).** O diálogo.
5. **P999 (0x3E7).** Placar. **P1000 (0x3E8).** Unificação.

## Previsões pré-registradas

**P972, a cobertura do português por profundidade.** Para os sinsets de substantivo do WordNet com profundidade (P793), a fração que tem lema em
português na OpenWordNet-PT.
- Exemplo à mão (regra da Parte 49): *entity* (profundidade 0) tem lema em português (*entidade*); um gênero de planta a 14 níveis provavelmente não.
- (a) cobertura geral dos substantivos em **[0,25; 0,60]**
- (b) cobertura na profundidade ≤ 4 menos cobertura na profundidade ≥ 12: **≥ 0,15**

**P973, Kaprekar em base 16.** K(n) = (dígitos em ordem decrescente) − (dígitos em ordem crescente), com 4 dígitos hexadecimais (zeros à esquerda contam),
para todo n de 1 a 0xFFFF que não tem os 4 dígitos iguais; itera-se até repetir.
- Exemplo à mão: n = 0x1234: 0x4321 − 0x1234 = 17185 − 4660 = 12525 = 0x30ED; depois 0xED30 − 0x03DE = 60720 − 990 = 59730 = 0xE952...
- (c) **não** há um ponto fixo único que atraia todos (como o 6174): há **2 a 6** ciclos terminais
- (d) o ciclo que atrai mais números atrai **≥ 50%** deles

**P971, rodada 25:** no `dialogo/DIALOGO.md`.
