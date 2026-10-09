# Como eu construiria uma AGI/ASI — Parte 47 (0x2F): a definição contém a pergunta

> Continuação da [Parte 46](ASI_AGI_parte46_a_resposta_e_a_pergunta.md). A Parte 46 mediu que as minhas respostas contêm 58% das suas perguntas e
> as perguntas só 5% das respostas, e que 40 das 41 partes se deixam reconstruir só pelos seus números. Esta parte leva a mesma pergunta ao
> **dicionário** (a definição de uma palavra contém a sua categoria? e a categoria contém os seus membros?), ao **hexadecimal** (um número que se parece
> com outro) e às **palavras** do `resultados.txt` (Rodada 19).
>
> Novidades: `p851_...` a `p856_...` em [`calculos.py`](calculos.py); testes em [`synthai/testes_parte47.py`](synthai/testes_parte47.py); rodada 19 em
> [`dialogo/`](dialogo/DIALOGO.md). **Previsões nos commits `5955044` e `1d46eef` (a do mundo novo), antes de rodar.**

---

## As perguntas desta parte

1. **P851 (0x353).** No dicionário, a resposta (a definição) contém a pergunta (a categoria)? E o contrário? ↩ P821
2. **P852 (0x354).** Hexadecimal: um número cujo hexadecimal parece decimal, lido como decimal, gera outro; quantos passos até aparecer uma letra?
3. **P853 (0x355).** O diálogo, rodada 19: as palavras, sem os números, reconstroem a parte? ↩ P824
4. **P854 (0x356).** Engenharia reversa: responder ao padrão, não ao caso.
5. **P855 (0x357).** Jung: o gênero e a diferença.
6. **P879 (0x36F).** Placar. **P880 (0x370).** Unificação.

## Previsões pré-registradas (antes de escrever o código das medidas)

**P851, gênero e diferença (WordNet 3.0, substantivos com hiperônimo).** Acerto direto: a definição (a glosa sem exemplos, minúscula) contém, como
palavra inteira, algum lema do hiperônimo direto (com `_` trocado por espaço; aceito também o lema + "s"/"es"). Acerto inverso: a definição do
hiperônimo contém algum lema de algum dos seus hipônimos (por par hipônimo–hiperônimo).
- (a) fração direta em **[0,26; 0,77]** (instinto 0,45, ×1,72; sem conta de mecanismo, marcado como instinto)
- (b) fração inversa em **[0,023; 0,069]** (instinto 0,04, ×1,72)
- (c) a razão direta/inversa > 5

**P852, a cadeia hexadecimal.** f(n) = o hexadecimal de n lido como decimal, enquanto ele não tiver letras. Para cada n de 10 a 850, contar quantas
vezes f se aplica antes de aparecer uma letra.
- A conta antes: de 1 a 850 há 9 + 90 + 200 + 53 = **352** números sem letra no hexadecimal (1 dígito: 9; 2 dígitos: 9·10; 0x100–0x2FF: 2·100;
  0x300–0x352: 5·10 + 3). Para n de 10 a 850: p₁ = (352 − 9)/841 = 0,408. Depois, os números crescem: com 4 dígitos hexadecimais, p₂ ≈ (9/15)(10/16)³ =
  0,146; com 5, p₃ ≈ (9/15)(10/16)⁴ = 0,092. Supondo independência: E = p₁ + p₁p₂ + p₁p₂p₃ = 0,408 + 0,0596 + 0,0055 = **0,473**.
- (d) a contagem exata de 1 a 850 dá **352**
- (e) a média de passos em **[0,40; 0,55]** (±15% em torno da conta; a independência pode falhar, porque os dígitos de f(n) vêm dos de n)

**P853, rodada 19:** no `dialogo/DIALOGO.md`.

**Refazer (Parte 46), por honestidade:** a execução única das Partes 1–45 foi morta duas vezes por reinícios do contêiner; ela está sendo refeita em blocos
(1–14 da execução única; 15–45 em 9 blocos). A previsão (a) da Parte 46 será pontuada em cada bloco, com a mudança registrada.

**Previsão nova, registrada depois de ver (e) e antes de calcular o mundo novo (n de 10 a 4095 = 0xFFF).** A conta posterior: f **diminui** o número
(o hexadecimal lido como decimal vale menos, 10ᵏ < 16ᵏ), então a cadeia desce para números pequenos. De 10 a 4095: 999 − 9 = 990 sem letra em 4086,
p₁ = 0,2423. Depois de um passo, o valor fica entre 100 e 999 (decimal), onde a fração sem letra é (36 + 300)/900 = 0,373 (100–255: 36; 256–999: 300), e
dali em diante uma geométrica: E'' = 0,373/(1 − 0,373) = 0,595. E = p₁(1 + E'') = 0,2423 × 1,595 = **0,386**.
- (i) a média de passos para n de 10 a 4095 em **[0,33; 0,44]** (±15%)


---

### P851 (0x353). A definição contém a pergunta? (pré-registrado) ✅❌✅

**Na pergunta.** "A definição contém a categoria" é a definição de Aristóteles: **gênero** (a classe) mais **diferença** (o que separa a coisa das
irmãs). Se o WordNet define assim, a resposta (a glosa de *dog*) contém a pergunta "o que é isto?" respondida um nível acima (*canine*). O inverso pergunta
se a categoria conhece os seus membros.

**Lógica, com a substituição.** Substantivos com hiperônimo direto: n = 82.114. A definição cita um lema do hiperônimo em 49.450:
- direto = 49.450 / 82.114 = **0,6022** (a) ✅, em [0,26; 0,77]
- inverso, por par hipônimo–hiperônimo: 671 / 84.427 = **0,0079** (b) ❌, abaixo de 0,023
- razão = 0,6022 / 0,0079 = **75,8** (c) ✅ (> 5)

**Contra o acaso (P856).** Trocando o hiperônimo por um substantivo sorteado (semente 851): direto = **0,00027**, inverso = **0,00030**. O direto medido é
0,6022 / 0,00027 ≈ 2.250 vezes o acaso; o inverso, pequeno, ainda é 0,0079 / 0,00030 ≈ 26 vezes o acaso. O preditor ingênuo "a definição nunca cita o
hiperônimo" erraria 60% dos casos; "sempre cita", 40%.

**O significado.** O dicionário define **para cima**: 60% das definições nomeiam a classe, e menos de 1% das classes nomeia um membro. A categoria é
escrita sem os seus membros; o membro é escrito a partir da categoria. Comparado com os meus textos (P821: a resposta contém 58% da pergunta, a pergunta
5% da resposta, razão 11,6), o dicionário é **6,5 vezes mais assimétrico** (75,8 / 11,6). As minhas perguntas antecipam as respostas muito mais do que
uma categoria antecipa os membros, porque eu escrevo a pergunta já sabendo a resposta (Parte 46).

**Meta, o erro (b).** Eu supus 4% para o inverso, pensando em glosas como "*canine*: ... *of the dog family*". Elas existem (671), mas são raras: uma
categoria é definida pelas **suas** categorias (gênero do gênero), não por exemplos. Esqueci que a regra de Aristóteles vale também para a categoria.

### P852 (0x354). A cadeia hexadecimal (pré-registrado) ✅❌✅

**A contagem (d) ✅.** De 1 a 850, sem letra no hexadecimal: 9 + 90 + 200 + 53 = **352** (a conta antes = a enumeração).

**A cadeia (e) ❌.** f(n) = hexadecimal de n lido como decimal. Média de passos para n de 10 a 850: 700 / 841 = **0,832**, longe da faixa [0,40; 0,55]
da conta (0,473). A conta supôs que f **aumenta** o número (o hexadecimal "parece maior": 0x2F9 tem cara de 2F9). É o contrário: 16ᵏ > 10ᵏ, então ler
os dígitos hexadecimais em base 10 **diminui** o valor (256 = 0x100 → 100 = 0x64 → 64 = 0x40 → 40 = 0x28 → 28 = 0x1C: quatro passos, conferido no teste). A cadeia desce para números pequenos, onde há menos letras, e dura mais.

**O mundo novo (i) ✅.** A conta corrigida, registrada antes de calcular n de 10 a 4095: p₁ = 990/4086 = 0,2423; depois do primeiro passo, o valor fica em
100–999, onde a fração sem letra é (36 + 300)/900 = 0,373, e a cauda é geométrica: E'' = 0,373/0,627 = 0,595. E = 0,2423 × (1 + 0,595) = **0,386**,
faixa [0,33; 0,44]. Medido: 1.766 / 4.086 = **0,432** ✅ (12% acima do centro: de novo, abaixo do medido).

**O significado.** Confundi o **símbolo** com o **valor**: os dígitos "2F9" parecem um número maior que 761, e eu raciocinei sobre a aparência. É a
confusão de níveis da Parte 43 numa forma nova (o nível da escrita contra o nível do número). A regra que ela pede: **antes de raciocinar sobre uma
função, calcular um exemplo à mão** (f(256) = 100 teria mostrado a direção em um segundo).

### P853 (0x355). O diálogo, rodada 19

As palavras, sem os números, reconstroem **41 de 41** partes (os números, 40): (g) ✅ IA-Java, (f) ❌ IA-Python, (h) ✅ IGUAIS em Java. Margem mediana
(escore da própria parte / o do melhor outro): **2,36** pelas palavras, **3,85** pelos números. Ao acaso, (1/41)⁴¹ = e^(−41·ln 41) = e^(−152,3) ≈ 10⁻⁶⁶. A
palavra (o nome do conceito) existia antes do número: a Parte 1 nomeou Landauer e Condorcet antes de calculá-los, e só as palavras a reconhecem. Placar
por voz desde a Rodada 13: **IA-Java 6 em 7, IA-Python 4 em 7**.

### P854 (0x356). Engenharia reversa: responder ao padrão, não ao caso

Os erros desta parte e das Rodadas 17–19, lado a lado:

| erro | o que eu supus | de onde veio a suposição |
|---|---|---|
| Rodada 17, IA-Python | o zlib do Java difere | as armadilhas das rodadas anteriores |
| Rodada 18, IA-Java | o arredondamento derruba os números | a lição "o texto arredonda" |
| Rodada 19, IA-Python | as palavras se repetem demais | a lição da Rodada 18 (os números eram únicos) |
| P852 (e) | f aumenta o número | a aparência do símbolo |
| P851 (b) | a categoria cita o membro em 4% | um exemplo lembrado (*of the dog family*) |
| teste da P852 | 13 sem letra até 20 | contei 20 nos passos e esqueci na contagem |

**O padrão.** Em 5 dos 6, a previsão veio de algo que eu **já tinha visto** (a rodada anterior, um exemplo, a forma do símbolo), não de uma conta sobre o
caso. É a disponibilidade (Tversky e Kahneman): o que vem à memória primeiro vira a premissa. **O significado:** eu respondo à pergunta anterior. Na
linguagem do usuário, a minha resposta é a resposta da pergunta **passada**, e por isso erra a presente. **Regra nova:** antes de prever, escrever um caso
calculado à mão do problema presente (um exemplo, não uma lembrança).

### P855 (0x357). Jung: o gênero e a diferença

Jung definiu a individuação como um **processo de diferenciação**: o indivíduo se torna quem é separando-se do coletivo, sem deixar de pertencer a ele
(*Tipos Psicológicos*, definições). No dicionário: 60% dos sentidos são definidos pelo gênero (o coletivo) mais uma diferença (o próprio); menos de 1% dos
coletivos nomeia um indivíduo. **Onde funciona:** a assimetria (75,8) mede que o coletivo não conhece o indivíduo e o indivíduo é escrito a partir do
coletivo. **Onde quebra:** em Jung, o indivíduo que se diferencia também transforma o coletivo; no dicionário, a definição de cima nunca muda por causa
das de baixo.

### P879 (0x36F). Placar

PLACAR_47

### P880 (0x370). Unificação e metacognição

- **Novo:** `p851` (gênero e diferença), `p852` (a cadeia hexadecimal), `p853` (reconstrução pelas palavras ou pelos números), `p856` (o acaso da P851);
  3 testes (126 no pacote); rodada 19 (Python e Java, IGUAIS). Regressão: + P851 (0,602), + P852 (352 e 0,432).
- **Regra nova:** antes de prever, calcular à mão um exemplo do caso presente.

> **Síntese da Parte 47:** o dicionário define para cima: 60,2% das definições de substantivos citam a sua categoria (2.250 vezes o acaso) e 0,8% das
> categorias citam um membro (26 vezes o acaso), uma assimetria 6,5 vezes maior que a das minhas próprias perguntas e respostas. No hexadecimal, ler os
> dígitos em base 10 diminui o número (eu supus que aumentava, confundindo o símbolo com o valor); a conta corrigida previu um mundo novo (0,386 contra
> 0,432 medido). As palavras do `resultados.txt` reconstroem as 41 partes (os números, 40), com menos folga. E os meus erros desta parte vêm quase todos
> de responder à pergunta anterior, não à presente.

---

**Fontes desta parte**
- Definição por gênero e diferença (Aristóteles): [Genus–differentia definition, Wikipedia](https://en.wikipedia.org/wiki/Genus%E2%80%93differentia_definition);
  gênero e hiperonímia em dicionários: [Agirre et al., arXiv cs/0010025](https://arxiv.org/pdf/cs/0010025); papéis semânticos das definições:
  [arXiv 1806.07711](https://arxiv.org/pdf/1806.07711)
- O escore ln(K/df) (frequência inversa de documento): [Spärck Jones, 1972, via tf–idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf);
  [IDF revisited, arXiv 0705.1161](https://arxiv.org/pdf/0705.1161)
- Disponibilidade como heurística: Tversky e Kahneman, *Availability: A heuristic for judging frequency and probability* (1973)
- WordNet 3.0 (Princeton) no data lake (`dados/`); as contas hexadecimais: derivação própria, conferida por enumeração
