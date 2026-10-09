# Como eu construiria uma AGI/ASI — Parte 51 (0x33): a memória curta e a longa

> Continuação da [Parte 50](ASI_AGI_parte50_a_vida_das_coisas.md). **Previsões no commit `3ce8f41`, antes de rodar.** A Parte 50 achou
> que a memória longa da série vem do **cotovelo** (cada parte divide muito com a vizinha). Esta parte testa se o cotovelo é uma memória curta somada a uma
> longa, mede que parte da taxonomia inglesa o português cobre, e procura a constante de Kaprekar do hexadecimal.

## As perguntas desta parte

1. **P971 (0x3CB).** Duas exponenciais (curta e longa) explicam a deriva melhor que a potência, cobrando os parâmetros (AIC)? (Rodada 25) ↩ P941
2. **P972 (0x3CC).** O português (OpenWordNet-PT) cobre mais os conceitos gerais que os específicos? ↩ P793
3. **P973 (0x3CD).** Hexadecimal: a rotina de Kaprekar com 4 dígitos hexadecimais tem um ponto fixo, como o 6174 do decimal?
4. **P974 (0x3CE).** Engenharia reversa: a regra das faixas, como passo verificável. **P975 (0x3CF).** Jung. **P976 (0x3D0).** O diálogo.
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

---

### P971 (0x3CB). Duas memórias ou uma potência (Rodada 25) ✅❌✅

Na curva média (n = 20), AIC = n ln(SSE/n) + 2k:
- exponencial: SSE 0,9128, AIC = 20 ln(0,9128/20) + 4 = 20 × (−3,0869) + 4 = **−57,74**
- potência: SSE 0,3095, AIC = 20 ln(0,3095/20) + 4 = 20 × (−4,1687) + 4 = **−79,37**
- duas exponenciais (τ₁ = 3,5; τ₂ = 110; A = 0,109; B = 0,023): SSE 0,3481, AIC = 20 ln(0,3481/20) + 8 = 20 × (−4,0509) + 8 = **−73,02**

**A potência ganha** por 6,4 unidades de AIC (e) ✅ IA-Java, (f) ❌ IA-Python, (g) ✅ IGUAIS (as exponenciais do Java e da glibc deram os mesmos bits). **Meta:** A e B
saem de mínimos quadrados na escala original e o erro é medido em log; por isso as duas exponenciais têm resíduo **maior** que a potência mesmo antes da
cobrança. Um ajuste em log (a pergunta da Rodada 26) pode mudar o vencedor; até lá, o resultado vale para este método.

**O significado.** A memória curta que existe dura ~3,5 partes, não uma (τ₁ = 3,5), e a longa, ~110 partes, mais que a série inteira: na prática, ela não
esquece. Uma potência faz as duas coisas com dois parâmetros.

### P972 (0x3CC). O português cobre os conceitos gerais (pré-registrado) ✅✅

Dos substantivos do WordNet com profundidade, **43,3%** têm lema em português (a) ✅. Por profundidade: 3 → 0,689; 5 → 0,554; 7 → 0,441; 9 → 0,435; 11 → 0,297; 13 →
0,280; 16 → 0,267. Profundidade ≤ 4: **0,5435**; ≥ 12: **0,2796**; diferença 0,5435 − 0,2796 = **0,2639** (b) ✅ (≥ 0,15).

**O significado.** A tradução começa pelo geral: *entidade*, *objeto*, *ato*, *pessoa* têm nome em português; o gênero de planta a 14 níveis da raiz,
quase nunca. Um dicionário bilíngue cresce de cima para baixo, como uma criança aprende (as categorias de nível básico primeiro). Para a SYNTHAI, isso diz
onde o português pode substituir o inglês (no topo) e onde ele ainda depende do inglês (nas folhas).

### P973 (0x3CD). Kaprekar em base 16 (pré-registrado) ✅❌

Com 4 dígitos hexadecimais (65.520 números sem dígitos todos iguais), **não há ponto fixo**: há **4 ciclos** (c) ✅:
- 1FFE → E0E2 → EB32 → C774 → 7FF8 → 8688: atrai **48,1%** (d) ❌ (previ ≥ 50%)
- 30ED → E952 → C3B4 → 9687: **22,8%** (o meu exemplo à mão, 0x1234, cai aqui)
- 3FFC → C2C4 → A776: **19,1%**
- 52CB → A596: **10,0%**

A base 10 dá o resultado conhecido: um só ponto fixo, **6174**, que atrai os 9.990 números. **O significado:** a constante de Kaprekar é uma propriedade da
base 10 com 4 dígitos, não da rotina; em base 16 a mesma rotina se divide em quatro destinos.

### P974 (0x3CE). Engenharia reversa: a regra das faixas, como passo verificável

O erro (d) é do tipo que o `CLAUDE.md` proíbe desde a Parte 43 ("toda previsão tem largura; nada de ≥ x traçado no olho: a P732 errou por 0,003"): previ
"≥ 50%" e o medido foi 48,1%. Pela regra da Parte 49 (uma regra só vale como passo verificável), ela virou uma função: `p974_previsoes_sem_largura` lê o
bloco de previsões de cada documento e conta as unilaterais. Partes 47–51: **4 unilaterais em 26 previsões** (47 c, 48 c, 51 b, 51 d); a única errada das
quatro é a 51 d, por 1,9 ponto. **O significado:** as unilaterais são as que eu escrevo quando acho que o resultado é óbvio (uma razão "> 5", uma bacia
"≥ 30%"); elas acertam quase sempre porque são fáceis, e quando erram, erram na borda que eu tracei no olho. A partir desta parte, a função roda em toda
parte, e uma previsão unilateral precisa de uma justificativa escrita (por que não há faixa).

### P975 (0x3CF). Jung: a função inferior aprende de baixo

Jung dizia que a função inferior (a menos desenvolvida) é a porta do inconsciente e cresce devagar, pelos casos concretos. O português na SYNTHAI é uma
função inferior medida: cobre 54% dos conceitos gerais e 28% dos específicos. **Onde funciona:** a cobertura cai com a profundidade, como uma função que
só alcança o que é geral e repetido. **Onde quebra:** em Jung, a função inferior cresce **de baixo** (do concreto); a OpenWordNet-PT cresceu de cima
(traduzindo o geral primeiro), ao contrário de uma criança e de Jung.

### P976 (0x3D0). O diálogo, rodada 25

Ver P971. Placar por voz desde a Rodada 13: **IA-Python 8 em 16; IA-Java 8 em 16**.

### P999 (0x3E7). Placar

(a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅ (f) ❌ (g) ✅. Parte 51: **7 testes, 2 erros**. PLACAR_51

### P1000 (0x3E8). Unificação e metacognição

- **Novo:** `p971` (duas memórias pelo AIC), `p972` (o português por profundidade), `p973` (Kaprekar numa base), `p974` (as previsões sem faixa); 4 testes
  (139 no pacote); rodada 25 (IGUAIS). Regressão: + P973 (4 ciclos; 6174).
- **Regra nova (verificável):** `p974` roda em toda parte; previsão unilateral só com justificativa escrita.
- A pergunta número **1000** desta série é a unificação da Parte 51.

> **Síntese da Parte 51:** a deriva da série é mais bem descrita por uma potência do que por duas memórias exponenciais (AIC −79,4 contra −73,0), com a
> ressalva de que o ajuste das duas foi feito fora da escala do erro. O português da OpenWordNet-PT cobre 54% dos conceitos gerais e 28% dos específicos:
> a tradução desce do topo da taxonomia. Em base 16, a rotina de Kaprekar não tem constante: quatro ciclos dividem os números (o maior com 48%). E a regra
> das faixas, que eu violei de novo, virou uma função que conta as minhas previsões unilaterais.

---

**Fontes desta parte**
- Critério de informação de Akaike: [Akaike information criterion, Wikipedia](https://en.wikipedia.org/wiki/Akaike_information_criterion)
- A rotina de Kaprekar e o 6174: [Kaprekar's routine, Wikipedia](https://en.wikipedia.org/wiki/Kaprekar%27s_routine)
- OpenWordNet-PT: [de Paiva, Rademaker e de Melo, *OpenWordNet-PT*, COLING 2012 (demo)](https://aclanthology.org/C12-3044/); dados em `dados/` (CC BY 4.0)
- Categorias de nível básico: Rosch et al., *Basic objects in natural categories*, Cognitive Psychology 8 (1976)
