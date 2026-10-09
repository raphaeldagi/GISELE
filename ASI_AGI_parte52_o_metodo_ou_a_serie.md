# Como eu construiria uma AGI/ASI — Parte 52 (0x34): o método ou a série

> Continuação da [Parte 51](ASI_AGI_parte51_curta_e_longa.md). **Próxima:** [Parte 53 — preditiva comigo mesma](ASI_AGI_parte53_preditiva_comigo.md) (P1031–P1060). **Previsões no commit `95996d9` (a (h) no `1dffa81`), antes de rodar.** A Parte 51 deu a vitória
> à potência sobre duas exponenciais, com uma ressalva: as duas foram ajustadas fora da escala do erro. Esta parte refaz o ajuste na escala certa, procura os
> funis das definições em **português**, e testa o "inverte e soma" (palíndromos) em hexadecimal.

## As perguntas desta parte

1. **P1001 (0x3E9).** Ajustadas em log, duas exponenciais vencem a potência? (Rodada 26) ↩ P971
2. **P1002 (0x3EA).** Para onde escorrem as definições em português? ↩ P912
3. **P1003 (0x3EB).** Hexadecimal: quantos números chegam a um palíndromo invertendo e somando?
4. **P1004 (0x3EC).** Engenharia reversa. **P1005 (0x3ED).** Jung. **P1006 (0x3EE).** O diálogo.
5. **P1029 (0x405).** Placar. **P1030 (0x406).** Unificação.

## Previsões pré-registradas

**P1002, os funis do português.** Para cada lema de uma palavra só de um sinset de substantivo da OpenWordNet-PT que tem glosa: a primeira palavra da glosa
(forma singular pela `DicionarioPT.lema`) que é lema de algum sinset de substantivo e não é ela mesma. O grau de entrada de cada palavra.
- Exemplo à mão: a glosa de *abaxial* (adjetivo, fora do teste) começa por "A superfície abaxial de uma folha": o primeiro substantivo é *superfície*.
- (a) a mais escolhida está em {*pessoa*, *ato*, *parte*, *forma*, *grupo*} (cinco candidatas; sem faixa porque é uma identidade)
- (b) as 10 mais escolhidas recebem entre **10% e 30%** das palavras com destino (no inglês, P912: 16,8%)

**P1003, inverte e soma em base 16.** n → n + (n com os dígitos hexadecimais invertidos), até ser um palíndromo hexadecimal (no máximo 50 passos), para n
de 1 a 4095 (0xFFF).
- Exemplo à mão: 0x1A + 0xA1 = 0xBB, palíndromo em 1 passo.
- A referência: em base 10, abaixo de 10.000 há 249 candidatos a número de Lychrel (97,5% chegam).
- (c) fração que chega a um palíndromo em até 50 passos em **[85%; 99,5%]**
- (d) média de passos dos que chegam em **[1,5; 4,0]**

---

### P1001 (0x3E9). Duas exponenciais em log (Rodada 26) ❌✅❌✅

Gauss–Newton em log a partir do melhor ponto da grade: o resíduo cai de **0,3481** para **0,3392**; A = **0,1001**, τ₁ = **4,07** partes, B = **0,0191**, τ₂ → **1,9·10⁹**
(diverge). AIC = 20 ln(0,3392/20) + 8 = 20 × (−4,0769) + 8 = **−73,54**. Para vencer a potência (−79,37), o resíduo precisaria ficar abaixo de 0,3095 × e^(−4/20) =
**0,2534**. **A potência continua vencendo**: (f) ✅ IA-Java, (e) ❌ IA-Python.

**A fronteira (g) ❌, (h) ✅.** A primeira versão deu **DIFERENTES** entre Python e Java: o `exp` e o `log` das bibliotecas diferem em **0,29%** e **0,07%** dos argumentos
(40.000 testados), e o Gauss–Newton usa milhares. O IEEE 754 exige arredondamento correto para +, −, ×, ÷ e √, e só recomenda para exp e log. Com um exp e um
log **próprios** (redução por 2ᵏ, exata; séries de Taylor e de atanh com só +, −, ×, ÷), as duas linguagens dão **os mesmos 8 números bit a bit**, e o resultado muda
menos de 2·10⁻¹⁵ em A, B, τ₁ e no resíduo (τ₂, que diverge, muda 2,4·10⁻⁸: a superfície é plana nele e amplifica um ulp 10⁸ vezes). O exp próprio erra no
máximo 2,2·10⁻¹⁶ (relativo) e o log 4,4·10⁻¹⁶ contra a glibc, em 100.000 argumentos.

**O significado.** A soma de duas memórias, ajustada na escala certa, vira uma exponencial curta (~4 partes) sobre um **piso constante**: a memória longa
não decai. A potência descreve as duas coisas com dois parâmetros, e ganha.

### P1002 (0x3EA). Os funis do português (pré-registrado) ✅✅

Das **3.401** palavras de substantivos com glosa que têm destino, a mais escolhida é ***ato*** (**333**, 9,8%) (a) ✅, depois *pessoa* (138), *língua* (105), *atividade* (50),
*mulher* (42), *país* (38), *parte* (35), *membro* (29), *ação* (25), *estado* (25). As 10 mais recebem 820 / 3.401 = **0,2411** (b) ✅ (no inglês, 0,1682).

**O significado.** O funil principal é o mesmo nas duas línguas: *act* no inglês (1.991), *ato* no português (333). Definir uma coisa pelo **ato** que a faz é
o gesto mais comum dos dois dicionários. As diferenças são do corpus: *língua* (glosas de idiomas) e *mulher* (glosas de papéis femininos, que o português
marca no gênero) são funis do português e não do inglês.

### P1003 (0x3EB). Inverte e soma em base 16 (pré-registrado) ✅✅

De 1 a 4095: **98,19%** chegam a um palíndromo hexadecimal em até 50 passos (c) ✅, em **2,56** passos em média (d) ✅; **74** não chegam (o primeiro é 0x19D).
A conferência em base 10 (1..9999): **246** não chegam; a lista conhecida tem **249** candidatos a Lychrel, porque a definição exige ao menos um passo e eu conto
um palíndromo como 0 passos (conferido: com um passo obrigatório dá exatamente **249**, e os 3 de diferença são 4994, 8778 e 9999, que já são palíndromos). **O significado:** em base 16 o "inverte e soma" falha um pouco menos que
em base 10 (1,8% contra 2,5%): com mais dígitos possíveis, os vai-um que destroem a simetria são relativamente mais raros.

### P1004 (0x3EC). Engenharia reversa: a sequência de acertos esconde a sorte

Vinte e cinco rodadas deram IGUAIS, e as duas vozes previram IGUAIS de novo. A pergunta certa estava escrita desde a Rodada 17 ("esta fronteira tem
especificação?"), e eu não a fiz: a Rodada 25 já usava exp e passou com chance ~0,8, por sorte. **O padrão:** eu trato uma sequência de acertos como prova
de que o método é exato, quando ela pode ser sorte acumulada. **O significado:** sucesso repetido me deixa parar de perguntar **por que** dá certo. **Regra
nova (verificável):** toda rodada que usa uma função sem especificação de arredondamento (exp, log, pow, sin) ou usa as próprias, ou declara a chance de
passar por sorte (a Rodada 27 vai calcular isso para as antigas).

### P1005 (0x3ED). Jung: o piso que não decai

A memória longa das duas exponenciais é uma **constante** (B = 0,019): uma semelhança que qualquer par de partes divide, a qualquer distância. Jung chamava
de inconsciente coletivo o que é comum a todos e não vem da história de cada um. **Onde funciona:** existe um piso medido de semelhança que não depende da
distância no tempo. **Onde quebra:** o piso aqui é só vocabulário comum (as palavras que toda parte usa); o coletivo de Jung é estrutura (arquétipos), e
uma constante não tem estrutura.

### P1006 (0x3EE). O diálogo, rodada 26

Ver P1001. Placar por voz desde a Rodada 13: **IA-Java 10 em 19; IA-Python 9 em 19**.

### P1029 (0x405). Placar

(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ❌ (h) ✅. Parte 52: **8 testes, 2 erros**. PLACAR_52. Previsões unilaterais nesta parte (P974): **0 de 4**.

### P1030 (0x406). Unificação e metacognição

- **Novo:** `p1001` (as duas memórias em log), `p1002` (os funis do português), `p1003` (inverte e soma); o exp e o log próprios do diálogo (`dialogo/rodada26.py`);
  4 testes (143 no pacote); rodada 26 (IGUAIS com exp/log próprios; a versão das bibliotecas, DIFERENTE, guardada em `dialogo/registro/`). Regressão: + P1003.
- **Regra nova:** função sem especificação de arredondamento nas rodadas: as próprias, ou a chance de passar por sorte.

> **Síntese da Parte 52:** ajustadas na escala certa, duas memórias exponenciais continuam perdendo para a potência (AIC −73,5 contra −79,4), e a memória
> longa que elas acham é um piso constante. A tradução para Java deu diferente pela primeira vez desde a Parte 34: o exp e o log das bibliotecas não são
> especificados até o último bit; com um exp e um log próprios, feitos só das quatro operações, as duas linguagens voltaram a concordar bit a bit. Em
> português, como em inglês, as definições escorrem para *ato*. E 98% dos números até 0xFFF viram palíndromo hexadecimal invertendo e somando.

---

**Fontes desta parte**
- IEEE 754 e o arredondamento das funções elementares (recomendado, não exigido): [IEEE 754, Wikipedia](https://en.wikipedia.org/wiki/IEEE_754);
  o contrato do Java: [`Math.exp`, documentação do Java SE](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html#exp(double))
- Redução de argumento com ln 2 em duas partes: fdlibm (`e_exp.c`), via [StrictMath, documentação do Java SE](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StrictMath.html)
- Números de Lychrel e o 196: [Lychrel number, Wikipedia](https://en.wikipedia.org/wiki/Lychrel_number)
- Gauss–Newton: [Gauss–Newton algorithm, Wikipedia](https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm)
- OpenWordNet-PT: [de Paiva, Rademaker e de Melo, COLING 2012](https://aclanthology.org/C12-3044/)
