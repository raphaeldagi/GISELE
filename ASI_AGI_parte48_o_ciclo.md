# Como eu construiria uma AGI/ASI — Parte 48 (0x30): o ciclo

> Continuação da [Parte 47](ASI_AGI_parte47_a_definicao_contem_a_pergunta.md). **Em andamento: previsões registradas antes de qualquer execução.**
> A Rodada 20 achou que a última parte (a da metacognição) fala como o começo da série. Esta parte pergunta pelo ciclo: no dicionário (toda definição
> acaba voltando a si?), no hexadecimal (os números felizes em base 16) e na série (Rodada 21).

## As perguntas desta parte

1. **P881 (0x371).** O Naive Bayes reconhece a época de cada parte? (Rodada 20) ↩ P853
2. **P882 (0x372).** No dicionário, seguir "a primeira palavra da definição" sempre termina num ciclo? Quantos, e quão longe? ↩ P851
3. **P883 (0x373).** Hexadecimal: os números felizes em base 16.
4. **P884 (0x374).** O diálogo, rodada 21: a série é um ciclo?
5. **P885 (0x375).** Engenharia reversa: medir a si mesmo não se reproduz.
6. **P886 (0x376).** Jung: a circum-ambulação.
7. **P909 (0x38D).** Placar. **P910 (0x38E).** Unificação.

## Previsões pré-registradas

**P882, o mapa da definição.** Para cada substantivo de uma palavra só (lema alfabético com sentido de substantivo): o primeiro sentido de substantivo, a
sua definição, e nela a **primeira palavra** (forma-base pela `morphy`) que é um substantivo de uma palavra só e não é a própria palavra. Isso é uma
função de N palavras nelas mesmas (as que não têm essa palavra ficam como sumidouros). Toda órbita termina num sumidouro ou num ciclo.
- A conta de referência (mapa aleatório de N pontos, Flajolet e Odlyzko): pontos cíclicos ≈ √(πN/2), cauda média ≈ √(πN/8). Com N ≈ 50.000:
  √(π·50.000/2) = **280** pontos cíclicos e √(π·50.000/8) = **140** passos até o ciclo.
- O dicionário não é aleatório: as definições apontam para poucas palavras gerais (*person*, *act*, *something*), que funcionam como funis.
- (a) pontos cíclicos (em ciclos, sem contar sumidouros) em **[5; 60]**
- (b) a média de passos até um ciclo ou sumidouro em **[2,5; 12]**
- (c) a maior bacia (o ciclo ou sumidouro que atrai mais palavras) tem **≥ 30%** das palavras

**P883, felizes em base 16.** s(n) = soma dos quadrados dos dígitos hexadecimais. n é feliz se a órbita chega a 1. Em base 10, de 1 a 1000 há 143
felizes (14,3%).
- (d) fração de felizes em 1..4095 em **[5%; 35%]**
- (e) ciclos diferentes do 1 (o ponto fixo): **1 a 4**

**P884, rodada 21:** no `dialogo/DIALOGO.md`.
