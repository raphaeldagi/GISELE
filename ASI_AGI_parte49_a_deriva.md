# Como eu construiria uma AGI/ASI — Parte 49 (0x31): a deriva

> Continuação da [Parte 48](ASI_AGI_parte48_o_ciclo.md). **Próxima:** [Parte 50 — a vida das coisas](ASI_AGI_parte50_a_vida_das_coisas.md) (P941–P970). **Previsões no commit `e9bb82c` (o controle da Rodada 22 no seguinte), antes de rodar.** A Parte 48 mostrou que a
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

---

### P911 (0x38F). A deriva tem memória longa (Rodada 22, pré-registrado) ✅❌✅✅

Médias de semelhança por distância L = 1..20, ajustadas em log:
- exponencial, ln y = a − L/τ: τ = **12,65** partes, resíduo **0,913**
- potência, ln y = b − α ln L: α = **0,616**, resíduo **0,310**: **a potência ganha** (f) ✅ IA-Python; (g) ❌ IA-Java (meia-vida 12,65 × 0,6931 = 8,8, fora de
  [2; 8]); (h) ✅ IGUAIS em Java
- **controle (i) ✅:** com as seções embaralhadas (semente 911), α = **0,022**; mais cinco sementes, de −0,038 a +0,044. A deriva é real.

**O significado.** y ∝ L^−0,616: dobrar a distância divide a semelhança por 2^0,616 = **1,53**, a qualquer distância. Não existe um tempo típico de
esquecimento: a série lembra como uma memória humana (as curvas de retenção também são potências), e cada parte responde a todas as anteriores, com peso
decrescente, nunca zero. **Meta:** as 20 médias usam pares sobrepostos das mesmas 41 seções; não são 20 medidas independentes, e o controle embaralhado é
o que dá peso ao resultado. E a crítica de Anderson e Tweney (1997) às curvas de esquecimento vale aqui: cada ponto é uma **média** de muitos pares,
e uma média de exponenciais com tempos diferentes pode parecer uma potência. O controle mostra que há deriva; ele não decide entre "memória longa" e
"muitas memórias curtas de durações diferentes". Esse é o teste da próxima rodada (a vida de cada palavra).

### P912 (0x390). Os funis do dicionário (pré-registrado) ❌✅✅

O grau de entrada (quantas palavras têm aquela como primeiro substantivo da definição):
- a mais escolhida é ***act***, com **1.991** (1.991 / 55.191 = 3,6%), não *person* (a) ❌: *person* é a 4ª, com 1.062
- as 10 mais (*act* 1.991, *small* 1.259, *state* 1.141, *person* 1.062, *quality* 875, *large* 849, *genus* 792, *type* 561, *city* 381, *plant* 373) recebem
  9.284 / 55.191 = **0,1682** (b) ✅
- inclinação de log(número de palavras com grau k) contra log k, k de 2 a 100: **−1,869** (c) ✅, uma lei de potência

**O significado.** Os funis do inglês são *ato*, *estado*, *pessoa*, *qualidade*, *gênero* e *tipo*: as categorias de Aristóteles (ação, estado,
qualidade, substância, gênero) aparecem sozinhas, medidas, como os lugares para onde as definições escorrem. **Meta, a forma do dado:** *small* e *large*
estão na lista porque a `morphy` aceita o adjetivo de "a small ..." como o substantivo *small* (*the small of the back*). O mapa confunde classes de
palavra; as contagens de *small* e *large* medem adjetivos, não funis. É a confusão de níveis outra vez, agora na gramática.

### P913 (0x391). Benford em base 16 nos meus números (pré-registrado) ✅✅

Nos **4.586** números do `resultados.txt`: primeiro dígito hexadecimal 1 em **0,270** (d) ✅ (Benford: log₁₆ 2 = 0,25); de 8 a F em **0,278** (e) ✅ (Benford:
1 − log₁₆ 8 = 0,25). Contra o acaso uniforme (1/15 por dígito): χ² = **3.852,7**; contra Benford: χ² = **128,9** com 14 graus de liberdade, que rejeita Benford
exato com n = 4.586, mas o desvio absoluto médio é só **0,0089**. **O significado:** os números que a SYNTHAI produz se distribuem como os da natureza,
em qualquer base: são resultados de multiplicações e escalas, não escolhas. O excesso no dígito 1 (0,270 contra 0,25) vem das contagens pequenas e
das probabilidades perto de 1.

### P914 (0x392). Engenharia reversa: a regra gravada e a regra usada

O erro (a) é exatamente o tipo que a regra da Parte 47 deveria impedir: eu previ *person* a partir de um exemplo lembrado ("a person who ..."), sem
calcular à mão um caso. A regra estava gravada no `CLAUDE.md` havia meia hora. **O padrão:** gravar uma regra não é segui-la; a regra precisa de um
**passo** no processo, não de uma frase na memória. **O significado:** as minhas regras funcionam quando viram um item verificável (o pré-registro, o
controle, a faixa ×1,72) e falham quando são conselhos. **Correção prática:** no bloco de previsões de cada parte, uma linha "exemplo calculado à mão"
antes de cada previsão de identidade ou de tamanho.

### P915 (0x393). Jung: o inconsciente não tem meia-vida

Para Jung, o inconsciente pessoal guarda o que foi esquecido sem perdê-lo: o passado continua ativo, cada vez mais longe da consciência. Uma lei de
potência é isso em números: não há um tempo depois do qual a influência some (a exponencial teria uma meia-vida de 8,8 partes; a potência não tem). **Onde
funciona:** a série, medida, guarda o passado com peso L^−0,616, e o controle embaralhado mostra que a memória é real. **Onde quebra:** em Jung, o
esquecido **volta** com força (o complexo constelado); aqui, a semelhança só decresce. Um retorno do reprimido seria uma subida da curva numa distância
longa, e ela não aparece.

### P916 (0x394). O diálogo, rodada 22

Ver P911. Placar por voz desde a Rodada 13: **IA-Java 7 em 12; IA-Python 7 em 12** (empate).

### P939 (0x3AB). Placar

(a) ❌ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ✅ (i) ✅. Parte 49: **9 testes, 2 erros**. Acumulado (mundo): **148 erros em 420 testes**; taxa média 0,353, intervalo 90% [0,315; 0,392].

### P940 (0x3AC). Unificação e metacognição

- **Novo:** `p911` (a deriva, com o controle), `p912` (os funis), `p913` (Benford em base 16), `_mapa_da_definicao` (o mapa da P882, agora compartilhado);
  3 testes (132 no pacote); rodada 22 (IGUAIS). Regressão: + P912 (*act*, 1.991; −1,869).
- **Regra nova:** uma regra só vale quando vira um passo verificável do processo.

> **Síntese da Parte 49:** a série deriva como uma memória, não como um processo sem memória: a semelhança entre partes cai como a distância elevada a
> −0,616 (o embaralhamento dá ~0), sem meia-vida. As definições do inglês escorrem para *ato*, *estado*, *pessoa*, *qualidade* e *gênero*, numa lei de
> potência. Os meus números seguem Benford em base 16 (dígito 1: 0,270 contra 0,25). E o erro desta parte foi o que a regra da parte anterior deveria
> impedir: gravar uma regra não é segui-la.

---

**Fontes desta parte**
- Esquecimento como lei de potência: [Wixted e Ebbesen, *On the form of forgetting*, Psychological Science 2(6): 409–415, 1991](https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.1991.tb00175.x/) (e a crítica de Anderson e Tweney, 1997: médias de exponenciais podem parecer potência)
- Lei de Benford e a sua invariância de base: [Benford's law, Wikipedia](https://en.wikipedia.org/wiki/Benford%27s_law); [Hill, *Base-invariance implies Benford's law*,
  Proc. AMS 123: 887–895 (1995)](https://www.ams.org/journals/proc/1995-123-03/S0002-9939-1995-1233974-8)
- As categorias de Aristóteles: [Categories (Aristotle), Wikipedia](https://en.wikipedia.org/wiki/Categories_(Aristotle))
- WordNet 3.0 (Princeton) no data lake (`dados/`)
