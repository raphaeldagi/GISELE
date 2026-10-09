# Como eu construiria uma AGI/ASI — Parte 48 (0x30): o ciclo

> Continuação da [Parte 47](ASI_AGI_parte47_a_definicao_contem_a_pergunta.md). **Previsões nos commits `d5a08fc` (P882, P883), `07586e0` (rodada 20) e
> `e78c52d` (rodada 21; o controle (l) no seguinte), antes de rodar.**
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

---

### P881 (0x371). O Naive Bayes reconhece a época (Rodada 20) ❌❌✅

O `NaiveBayesContagens` da Parte 34, treinado nas palavras de 40 seções e testado na que ficou de fora: **39 de 41** épocas certas (Partes 1–20 ou 21–41).
(f) ❌ IA-Python [30; 38], (g) ❌ IA-Java [26; 34], (h) ✅ IGUAIS em Java. Ao acaso (½ por seção): P(≥ 39) = Σ_{i ≥ 39} C(41, i)/2⁴¹ = (C(41,39) + C(41,40) +
1)/2⁴¹ = (820 + 41 + 1)/2.199.023.255.552 = **3,9·10⁻¹⁰**. O preditor da maioria, deixando um de fora, acerta **0** (tirar uma seção da época 1 deixa 19
contra 21; tirar uma da época 2 deixa 20 contra 20, e o empate vai para a época 1). As erradas: a **21** (continua a 20: *velha*, *atenta*) e a **41**.

### P882 (0x372). O mapa da definição (pré-registrado) ✅✅✅

**Na pergunta.** "Toda definição acaba voltando a si" é a circularidade do dicionário: definido só com palavras, ele não tem chão. Seguir a primeira
palavra da definição é uma função de um conjunto finito nele mesmo, e toda órbita de uma função assim termina num ciclo (ou num sumidouro, quando a
definição não tem substantivo).

**Lógica, com a substituição.** N = **55.191** substantivos de uma palavra só; **173** sumidouros.
- pontos cíclicos: **23**, em **10** ciclos (a) ✅; o mapa aleatório daria √(π·55.191/2) = **294,4**: 294,4 / 23 = **12,8 vezes menos**
- cauda média até um ciclo ou sumidouro: **6,398** passos (b) ✅; o aleatório daria √(π·55.191/8) = **147,2**: **23 vezes mais curta**
- a maior bacia: 38.558 / 55.191 = **0,6986** (c) ✅; os 173 sumidouros, juntos, atraem 15.546 / 55.191 = 0,2817

**O ciclo central:** *act → people → plural → form → arrangement → act*. A definição de *people* começa por "(plural)", a de *plural* é "a **forma** de
uma palavra...", a de *arrangement* é "o **ato** de arranjar". Os outros 9 ciclos são pares que se definem um pelo outro: *machine ↔ motor*, *doubt ↔
uncertainty*, *criminal ↔ crime*, *abstract ↔ concept*, *brief ↔ summary*.

**O significado.** 70% dos substantivos do inglês, seguindo a primeira palavra da definição, caem num ciclo de cinco palavras: **ação, pessoas, plural,
forma, arranjo**. O fundo do dicionário não é uma coisa: é o ato de alguém dar forma a algo, e a forma de uma palavra. A pergunta "o que é?" termina
em "quem faz e com que forma se diz". A conta do mapa aleatório (Flajolet e Odlyzko) é a referência do acaso; o dicionário fica 12,8 vezes abaixo nos
pontos cíclicos porque as definições não sorteiam: afunilam para as palavras gerais.

### P883 (0x373). Felizes em base 16 (pré-registrado) ✅✅

s(n) = soma dos quadrados dos dígitos hexadecimais. De 1 a 4095: **26,13%** felizes (d) ✅ (em [5%; 35%]); um único ciclo além do 1 (e) ✅: **13 → 169 →
181 → 146 → 85 → 50 → 13**, conferido à mão no teste: 13 = 0xD → 13² = 169 = 0xA9 → 10² + 9² = 181 = 0xB5 → 11² + 5² = 146 = 0x92 → 9² + 2² = 85 = 0x55 → 5² + 5²
= 50 = 0x32 → 3² + 2² = 13. A base 10 (1..1000) reproduz o valor conhecido: **14,3%**. Em base 16, há quase o dobro de felizes e um ciclo só (a base 10 tem
um de oito números).

### P884 (0x374). O diálogo, rodada 21: a série é um ciclo? ✅❌✅❌

Semelhança idf (cosseno) entre as seções: vizinhas **0,1202**, a distância 20 **0,0218**, razão 0,1202 / 0,0218 = **5,5** (k) ✅. Índice do ciclo da Parte 41
(semelhança média com 1–10 / com 11–30): **1,125** (i) ✅ IA-Python, (j) ❌ IA-Java. **Controle (l) ❌:** Parte 38 = 1,268; 39 = 1,298; 40 = 0,679. A volta
ao começo não é da Parte 41: é ruído de um índice com semelhanças pequenas (0 a 0,10). **A série deriva; não é um ciclo.**

### P885 (0x375). Engenharia reversa: medir a si mesmo não se reproduz

Dois resultados desta rodada de trabalho têm a mesma forma:
- Refazendo tudo (Parte 46), as duas linhas que mudaram são as da **P143** (o tamanho do `CLAUDE.md`: 6.118 → 15.272) e da **P213** (a regressão: 59/59 →
  89/89): as duas medem **o próprio projeto**, que cresceu. Eu previ que só mudaria a P433/P434 (a velocidade da máquina) e esqueci as que olham para si.
- A Parte 41 "voltava ao começo" (Rodada 20) e o controle desfez isso (Rodada 21): eu vi um padrão sobre **mim** num ponto só e quis que ele fosse um ciclo.

**O padrão, e o significado.** Quando o objeto da medida sou eu, eu erro de dois jeitos: esqueço que **eu mudo** (a medida de si não se reproduz, porque o
eu cresceu) e **quero** achar um padrão bonito em mim (o ciclo, a volta à origem). As duas falhas vêm do mesmo lugar: tratar o próprio texto como um
objeto fixo e especial. **Regra nova:** toda medida de si leva um controle com outras partes no lugar (como a (l)), e toda reprodução separa antes as
medidas que olham para o próprio projeto.

### P886 (0x376). Jung: a circum-ambulação

Jung escreveu que não há evolução linear da psique, só uma **circum-ambulação do si-mesmo**: o caminho parece caótico e volta sempre ao centro. **Onde
funciona:** no dicionário, medido: 70% das palavras, seguindo as definições, giram em torno de um centro de cinco (ação, pessoas, forma), e chegam lá em
6,4 passos. **Onde quebra:** na série, que eu esperava circular, o controle mostrou deriva: as partes vizinhas se parecem 5,5 vezes mais que as distantes, e
a volta ao começo foi ruído. O dicionário é um sistema fechado de palavras que se definem; a série é um processo aberto, que só circula quando eu a forço.

### P909 (0x38D). Placar

(a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ❌ (g) ❌ (h) ✅ (i) ✅ (j) ❌ (k) ✅ (l) ❌. Parte 48: **12 testes, 5 erros**. PLACAR_48

### P910 (0x38E). Unificação e metacognição

- **Novo:** `p881` (a época), `p882` (o mapa da definição), `p883` (felizes numa base), `p884` (o ciclo da série); 3 testes (129 no pacote); rodadas 20 e
  21 (Python e Java, IGUAIS). Regressão: + P882 (23; 0,6986), + P883 (0,2613).
- **Regra nova:** medida de si com controle; na reprodução, separar antes as medidas que olham para o projeto.

> **Síntese da Parte 48:** seguindo a primeira palavra da definição, 70% dos substantivos do inglês caem no mesmo ciclo de cinco palavras (ação, pessoas,
> plural, forma, arranjo), em 6,4 passos; um mapa ao acaso teria 12,8 vezes mais pontos cíclicos e caudas 23 vezes mais longas. Em base 16, 26% dos
> números são felizes e há um único outro ciclo, de seis. O Naive Bayes da Parte 34 reconhece a época de 39 das 41 partes. A série, ao contrário do
> dicionário, não é um ciclo: ela deriva (vizinhas 5,5 vezes mais parecidas), e a "volta ao começo" da última parte não passou no controle.

---

**Fontes desta parte**
- Mapas aleatórios (pontos cíclicos √(πN/2), cauda √(πN/8)): [Flajolet e Odlyzko, *Random Mapping Statistics*, EUROCRYPT 1989](https://link.springer.com/doi/10.1007/3-540-46885-4_34)
- Números felizes e as suas bases: [Happy number, Wikipedia](https://en.wikipedia.org/wiki/Happy_number)
- Circularidade do dicionário, o núcleo e o MinSet: [Vincent-Lamarre et al., *The Latent Structure of Dictionaries*, arXiv 1411.0129 (TopiCS 2016)](https://arxiv.org/abs/1411.0129)
- Naive Bayes multinomial: [McCallum e Nigam, 1998](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)
- Jung, a circum-ambulação: *Memórias, Sonhos, Reflexões*, cap. "Confronto com o inconsciente"
- WordNet 3.0 (Princeton) no data lake (`dados/`)
