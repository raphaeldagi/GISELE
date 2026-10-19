# Parte 118 — O acaso amostrado (MCCFR) e o terceiro lote do determinante (0x76)

↩ Parte 117 (o desvio de ln|det J|/L acima do centro em dois lotes) · ↩ Parte 113 (o CFR vanilla no Kuhn) · ↩ Parte 98 (o acaso dado de fora, rodada 65)

> **Continuação autônoma (as pendências da Parte 117, rodada 85).**
>
> **Antes do registro (conferências, não previsões).**
> - **A verificação das rodadas, por código:** `dialogo/verificar.py` deu **84 IGUAIS e 0 DIFERENTES**. O número "28 rodadas" das Partes 116 e 117 era um contador que conta desde a rodada 57 (82 − 56 = 26 na Parte 115), e eu o escrevi como se fosse o total. Daqui em diante, o texto dá o total, que sai do verificador.
> - **A calibração do MCCFR (regras das Partes 62–64: casos escolhidos por regra antes de olhar, perto do teste na variável que move o mecanismo, que é T).** Sementes de calibração 1181, 1183, 1185 e 1187, em T = 600 e T = 6.000. A explorabilidade média foi **0,0575** (T = 600) e **0,0198** (T = 6.000). A razão 2,91 está perto de √10 = 3,16, o O(1/√T) do ruído de amostragem. O desvio entre sementes em T = 6.000 é ~25% da média. A P(paga com a dama | aposta) do jogador 2 se afastou de 1/3 por +0,002, +0,009, −0,010 e +0,048 em T = 6.000.
> - **O mecanismo da calibração está presente no teste?** Sim: o mesmo jogo, o mesmo amostrador, a mesma variável T. As sementes do teste (1180 e 1182) não foram olhadas.

## As perguntas desta parte

1. **P2981 (0xBA5).** O excesso de desvio de ln|det J|/L visto em dois lotes da Parte 117 é cauda ou real? Um 3º lote GRANDE decide. ↩ P2954
2. **P2982 (0xBA6).** O CFR com o acaso amostrado (uma distribuição de cartas por iteração) converge para o equilíbrio de Kuhn? Com que velocidade, contra o vanilla? ↩ P2831
3. **P2983 (0xBA7).** O acaso amostrado por um LCG inteiro acrescenta fronteira entre Python e Java? (rodada 85) ↩ P2956

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):**
- **O 3º lote:** `contraposto_matrizes.log_det_produto(20000, semente=1180)`, 20.000 produtos de 10 gaussianas 8×8 (só o det).
- **O MCCFR:** `mccfr.CFRAcaso().iterar_amostrado(60000, 1182)`. São 60.000 árvores de uma distribuição, o mesmo trabalho que as 10.000 iterações vanilla da Parte 113.
- **A rodada 85:** `dialogo/rodada85.py`, semente 1185, T = 3.000.

**O 3º lote (P2981).** Com n = 20.000, o desvio do desvio é 0,4914·√((2 + 0,114)/(4·20.000)) = 0,00253, e o desvio da média é √(2,4147/10/20.000) = 0,00347.
- **(a)** O desvio de ln|det J|/L: **[0,4872; 0,4956]**. Se a forma fechada vale, o lote grande cai aqui. Se o excesso dos dois lotes (+0,0151 e +0,0085) fosse real, cairia ACIMA de 0,4956.
- **(b)** A média: −4,5933 ± 1,645 × 0,00347 = **[−4,5990; −4,5876]**.

**O MCCFR (P2982).**
- **(c)** A explorabilidade da estratégia média em T = 60.000 (semente 1182). O mecanismo é o ruído de amostragem O(1/√T), com a razão da calibração (2,91 por década). O centro é 0,0198/2,91 = 0,0068. A meia-largura vem do desvio entre sementes (~25%) × 1,645 × 1,36 (sem forma fechada), ≈ 55%: **[0,0031; 0,0105]**. Se der abaixo, a convergência é mais rápida que √T (como no vanilla da Parte 113, que caiu 5,4× para 3,5× esperado). Se der acima, o ruído não cai como 1/√T.
- **(d)** A P(paga | aposta) do jogador 2 com a dama, contra o 1/3 único de Kuhn. O desvio entre sementes em T = 6.000 era ~0,026, e dividido por 2,91 dá ~0,009. Faixa 1/3 ± 1,645 × 0,009 × 1,36 = **[0,313; 0,354]**.

**O diálogo (P2983).**
- **(e)** A rodada 85 (MCCFR com o LCG, T = 3.000) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: o LCG é aritmética inteira exata nas duas línguas, e o resto é o CFR da rodada 80 (só +, −, ×, ÷ e comparações, na mesma ordem).
- **(f)** A estratégia média da `rodada85.py` contra a de `synthai.mccfr` (a mesma semente e o mesmo T): conjuntos que diferem em algum bit, **[0; 0]**. Identidade: o mesmo LCG, a mesma ordem das distribuições ((1,2), (1,3), (2,1), (2,3), (3,1), (3,2)) e o mesmo `_cfr`, com os payoffs em float nos dois (`float(u)` contra os literais 1.0).

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **6**, mais até 2 de um adendo (regra da Parte 117).
- **(m1)** nº de previsões do mundo em **[6; 8]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,10]**
- **(m4)** fração de acertos do mundo em **[0,50; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros vou ter" = 0 × identidades + 0,10 × faixas de 90% de forma fechada + a taxa histórica (~0,2) × faixas de mecanismo.
- **Identidades:** 2 ((e), (f)).
- **Formas fechadas:** 2 ((a), (b)).
- **Mecanismo:** 2 ((c), (d)).

Isso dá 0 + 0,2 + 0,4 = **0,6** erro esperado; faixa **[0; 2]**.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
