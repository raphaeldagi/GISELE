# Como eu construiria uma AGI/ASI — Parte 49 (0x31): a deriva

> Continuação da [Parte 48](ASI_AGI_parte48_o_ciclo.md). **Em andamento: previsões registradas antes de qualquer execução.** A Parte 48 mostrou que a
> série não volta ao começo: ela deriva (partes vizinhas 5,5 vezes mais parecidas que partes a 20 de distância). Esta parte mede a forma da deriva, os
> funis do dicionário e a lei de Benford em base 16 nos meus próprios números.

## As perguntas desta parte

1. **P911 (0x38F).** A deriva da série tem meia-vida (exponencial) ou memória longa (potência)? (Rodada 22) ↩ P884
2. **P912 (0x390).** No mapa da definição, para que palavras as definições afunilam? ↩ P882
3. **P913 (0x391).** Hexadecimal: o primeiro dígito hexadecimal dos números do `resultados.txt` segue Benford em base 16?
4. **P914 (0x392).** Engenharia reversa. **P915 (0x393).** Jung. **P916 (0x394).** O diálogo.
5. **P939 (0x3AB).** Placar. **P940 (0x3AC).** Unificação.

## Previsões pré-registradas

**P912, os funis.** No mapa da P882 (cada substantivo → o primeiro substantivo da sua definição), o grau de entrada de cada palavra é quantas palavras
a escolhem.
- (a) a palavra mais escolhida é ***person***
- (b) as 10 mais escolhidas recebem, juntas, entre **8% e 25%** das 55.191 palavras
- (c) o grau de entrada segue uma lei de potência na cauda: a inclinação de log(frequência das palavras com grau k) contra log k, para k de 2 a 100,
  em **[−2,6; −1,4]** (instinto −2, ×1,3)

**P913, Benford em base 16.** Para cada número decimal do `resultados.txt` (com ponto ou inteiro, positivo, sem os rótulos Pnnn), o primeiro dígito
hexadecimal do valor (escalado por potências de 16 para [1, 16)). Benford em base 16: P(d) = log₁₆(1 + 1/d): P(1) = 0,25; P(d ≥ 8) = 1 − log₁₆ 8 = 0,25.
- (d) fração com primeiro dígito 1 em **[0,20; 0,30]**
- (e) fração com primeiro dígito de 8 a F em **[0,17; 0,33]**

**P911, rodada 22:** no `dialogo/DIALOGO.md`.
