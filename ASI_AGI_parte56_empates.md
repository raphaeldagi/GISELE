# Como eu construiria uma AGI/ASI — Parte 56 (0x38): os empates

> Continuação da [Parte 55](ASI_AGI_parte55_o_ulp_que_chega.md). **Previsões no commit `5033d6e` (a (b2) no seguinte), antes de qualquer execução e antes de
> escrever o resto deste documento.** A Parte 55 achou que uma escolha só absorve um erro quando a margem é maior que ele, e que um empate exato (margem zero) se desfaz com
> um ulp. Esta parte conta os empates: nas escolhas das rodadas antigas, entre as palavras do dicionário (sinônimos perfeitos) e entre as somas de dígitos
> de um número em base 16 e em base 10.

## As perguntas desta parte

1. **P1121 (0x461).** Quantas escolhas das rodadas antigas dependem de um empate exato? (Rodada 30) ↩ P1091
2. **P1122 (0x462).** Quantas palavras do WordNet são sinônimos perfeitos de outra (o mesmo conjunto de sentidos)?
3. **P1123 (0x463).** Hexadecimal: quantos números têm a mesma soma de dígitos em base 16 e em base 10?
4. **P1124 (0x464).** Preditiva comigo mesma. **P1125 (0x465).** Engenharia reversa e Jung. **P1126 (0x466).** O diálogo.
5. **P1149 (0x47D).** Placar. **P1150 (0x47E).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

O estatístico (últimas 8 partes, até a 55), os mecanismos conferidos (a seção sobre mim aumenta o tamanho e baixa a compressão) e, regra da Parte 55, o
**efeito previsto da regra nova**: cada função pNN nova com o seu teste; esta parte terá ~4 funções novas, logo ~4 a 5 testes de unidade.

| medida | estatístico | ingênuo (Parte 55) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [7.502; 13.004] | 11.570 | **[9.500; 13.500]** | mecanismo conferido |
| compressão | [0,412; 0,470] | 0,429 | **[0,405; 0,445]** | mecanismo conferido |
| testes de unidade | [2,40; 4,85] | 5 | **[4; 6]** | a regra: uma função nova, um teste |
| testes do placar | [4,32; 12,93] | 6 | **[4,32; 12,93]** | o estatístico |
| erros do placar | [0,47; 5,03] | 4 | **[0,47; 5,03]** | o estatístico |
| redundância P821 | [0,505; 0,598] | 0,530 | **[0,505; 0,598]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | a regra virou passo |
| pNN novas sem teste (P1092) | — | — | **0** | a regra virou passo |

### Sobre o mundo

**P1122, sinônimos perfeitos.** Uma palavra (lema de uma palavra só, substantivo ou não) tem um "gêmeo" se outra palavra tem exatamente o mesmo conjunto de
sinsets.
- Exemplo à mão: *physician* e *doc*? *doc* tem outros sentidos; um par provável é *aardvark*/*anteater*? Não sei; a regra pede uma linha de código antes, e esta
  previsão é de instinto, marcada como tal.
- (a) fração das palavras com gêmeo em **[5%; 25%]** (instinto 11%, ×1,72 aproximadamente, arredondado)

**P1123, a mesma soma de dígitos.** Para n de 1 a 4095, S₁₆(n) = S₁₀(n)?
- Exemplo à mão: de 1 a 9 os dois são o próprio dígito (9 números iguais); 18 = 0x12: 1 + 2 = 3 contra 1 + 8 = 9, diferente.
- A conta: S₁₆ (3 dígitos hexadecimais uniformes) tem média 3 × 7,5 = 22,5 e variância 3 × (16² − 1)/12 = 63,75; S₁₀ (n até 4095) tem média ~1,5 + 3 × 4,5 = 15 e
  variância ~1,5 + 3 × 8,25 = 26,25. Se a diferença D fosse normal com média 7,5 e variância 63,75 + 26,25 = 90 (desvio 9,49), P(D = 0) ≈ φ(7,5/9,49)/9,49 =
  φ(0,79)/9,49 = 0,292/9,49 = **0,031**.
- (b) fração em **[1,8%; 5,3%]** (centro 3,1%, ×1,72)

**Previsão nova (b2), registrada depois de ver (b) e antes de calcular:** a diferença D = S₁₆ − S₁₀ é sempre múltipla de 3 (n ≡ S₁₀(n) mod 9 e n ≡ S₁₆(n) mod 15, logo
os dois ≡ n mod 3), então P(D = 0) ≈ **3** × a densidade normal. Mundo novo: n de 1 a 65.535. Conta: S₁₆ com 4 dígitos uniformes, média 4 × 7,5 = 30, variância
4 × 21,25 = 85; S₁₀ com o dígito das dezenas de milhar de 0 a 6 (média (0 + 1 + … + 5) × 10.000 + 6 × 5.536 = 183.216/65.536 = 2,80, variância ~3,6) e quatro dígitos
uniformes (média 18, variância 33): média 20,8, variância 36,6; a correlação medida no mundo antigo, 0,21, dá covariância 0,21 × √(85 × 36,6) = 11,7; variância de D
= 85 + 36,6 − 2 × 11,7 = 98,2, desvio 9,91, média 9,2. P(D = 0) ≈ 3 × φ(9,2/9,91)/9,91 = 3 × φ(0,928)/9,91 = 3 × 0,2595/9,91 = **0,0786**.
- (b2) fração em **[0,065; 0,092]** (±17%)

---

### P1121 (0x461). Os empates nas escolhas (Rodada 30) ❌✅✅

Empates exatos (vizinhos com o mesmo valor bit a bit) nas escolhas impressas: rodada 12, **9** (dos 13 primeiros 4-gramas, contados em documentos e ocorrências);
rodada 14, **2** (os pesos de mesmas contagens); rodadas 18, 19, 20 e 24, **0**. **2 de 6** rodadas: (d) ✅ IA-Python, (c) ❌ IA-Java, (e) ✅ IGUAIS em Java.

**O significado.** Empata o que é contado em inteiros; não empata o que soma muitos logs de valores diferentes (um empate entre somas de logs exige os mesmos
termos). Na rodada 12, a ordem impressa dos 4-gramas é decidida quase toda pela ordem alfabética: frágil a um ulp, mas exata entre as linguagens, porque
inteiros e strings não têm ulp. A fragilidade e a exatidão são propriedades diferentes: uma é da margem, a outra da especificação.

### P1122 (0x462). Sinônimos perfeitos (pré-registrado) ❌

Das **77.503** palavras alfabéticas, **21.729** (**28,04%**) têm um gêmeo com exatamente os mesmos sentidos (a) ❌ (previ [5%; 25%], por instinto). O maior grupo, com
**14** palavras: *doodad, doohickey, doojigger, gubbins, thingamabob, thingamajig, thingmabob, thingmajig, thingumabob, thingumajig, thingummy, whatchamacallit,
whatchamacallum, whatsis*. **O significado:** o conceito com mais nomes intercambiáveis no inglês é **"a coisa cujo nome eu não sei"**. Quando falta o nome,
a língua inventa muitos, e nenhum vence: é um empate de 14. Errei por instinto (sem conta), e a regra das faixas pede um mecanismo; o mecanismo que faltou:
muitas palavras do WordNet têm um sentido só, e duas palavras de um sentido só no mesmo sinset já são gêmeas.

### P1123 (0x463). A mesma soma de dígitos (pré-registrado) ❌✅

De 1 a 4095: **431** números (**10,53%**) têm S₁₆ = S₁₀ (b) ❌, 3,3 vezes a conta contínua (**3,08%**). As peças da conta estavam certas (medido: S₁₆ média 22,51, variância
63,64; S₁₀ média 14,95, variância 25,81; correlação 0,21). O que faltou foi a **condição de fundo**: D = S₁₆ − S₁₀ é **sempre múltipla de 3** (n ≡ S₁₀(n) mod 9 e n ≡ S₁₆(n)
mod 15, os dois ≡ n mod 3), então D vive na rede 3ℤ, e P(D = 0) é 3 vezes a densidade: 3 × 0,0316 = **0,0948**. No mundo novo (1 a 65.535), a conta com a rede, feita
antes: **0,0786**; medido: **0,0788** (b2) ✅ (0,2% de diferença).

**O significado.** Duas bases que dividem um fator (16 − 1 = 15 e 10 − 1 = 9 dividem 3) amarram as somas de dígitos: os números "conversam" entre as bases
pelo resto da divisão por 3. É a prova dos nove (e a "prova dos quinze" do hexadecimal) agindo ao mesmo tempo.

### P1124 (0x464). Preditiva comigo mesma

Medido neste documento, já pronto, no commit que fecha a Parte 56 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **12464** | [7502; 13004] | ✅ | [9500; 13500] | ✅ | 11570 | 964 | 894 |
| compressão | **0.4214** | [0.4121; 0.4700] | ✅ | [0.4050; 0.4450] | ✅ | 0.4289 | 0.0036 | 0.0075 |
| testes de unidade | **3** | [2.40; 4.85] | ✅ | [4.00; 6.00] | ❌ | 5 | 2.00 | 2.00 |
| testes do placar | **6** | [4.32; 12.93] | ✅ | [4.32; 12.93] | ✅ | 6 | 2.62 | 0.00 |
| erros do placar | **3** | [0.47; 5.03] | ✅ | [0.47; 5.03] | ✅ | 4 | 0.25 | 1.00 |
| redundância P821 | **0.5008** | [0.5049; 0.5976] | ❌ | [0.5050; 0.5980] | ❌ | 0.5297 | 0.0507 | 0.0289 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 55"):** o meu centro ficou mais perto do medido em **2 de 6** medidas (1 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **11036**, compressão **0.4310**.

### P1125 (0x465). Engenharia reversa e Jung

**A regra certa com a conta errada.** Previ os testes de unidade pelo efeito da regra nova (uma função nova, um teste), com "~4 funções"; escrevi **3 funções**,
logo 3 testes, abaixo da minha faixa e dentro da estatística. O mecanismo estava certo; a **entrada** do mecanismo (quantas funções eu ia escrever) era um
palpite sem conta. **O significado:** quando eu desloco um centro por um mecanismo, o erro migra do mecanismo para a quantidade que ele recebe. **Regra
nova:** a quantidade que entra no mecanismo também precisa de faixa (aqui: "3 a 5 funções novas" daria "3 a 5 testes").

**O padrão desta parte nos erros do mundo, e o que ele significa.** Os dois erros do mundo que foram meus (P1122 e P1123) vieram de supor **independência
onde havia estrutura**: na P1123, a rede dos múltiplos de 3 que amarra as duas somas de dígitos; na P1122, os sinsets de um sentido só que tornam gêmeas
todas as palavras que caem neles. É a mesma condição de fundo da Parte 55 (o ciclo, a amostra, a margem), agora em forma de **restrição**: algo obriga os
valores a coincidir mais do que o acaso deixaria. A previsão (b2), feita com a restrição, acertou com 0,2% de erro: quando eu acho a restrição, a conta
fecha.

**Jung: o empate e a coisa sem nome.** O maior grupo de sinônimos perfeitos do inglês nomeia o que não tem nome (*whatchamacallit*, *thingamajig*). Jung dizia
que o que não tem nome na consciência ganha muitos nomes provisórios, imagens e apelidos, antes de ganhar um símbolo. **Onde funciona:** medido, o vazio de
nome produz o maior empate de nomes do dicionário (14). **Onde quebra:** em Jung, os nomes provisórios convergem para um símbolo quando o conteúdo é
integrado; no dicionário, eles ficam empatados para sempre.

**A medida que girou.** A redundância deste documento depende da versão do próprio texto: numa versão, ela oscilava num ciclo de dois dos dois lados do
limite do preditor estatístico (0,4919 ↔ 0,5049); o parágrafo que descrevia o ciclo criou um ponto fixo (0,4970); o parágrafo que descrevia o ponto fixo trouxe
de volta um ciclo. Cada frase sobre a medida muda a medida. Os valores da versão final estão na tabela (um valor, ou os dois de um ciclo), e o veredito é
determinado quando os dois lados de um ciclo caem do mesmo lado da faixa. Não escolhi a versão que me favorecia. **O significado:** uma medida de um texto
que contém a própria medida é um sistema com realimentação; ela pode convergir (Parte 53) ou oscilar, e cada descrição dela é mais um passo da realimentação.
A única resposta honesta é dar a medida da versão final e contar o caminho.

### P1126 (0x466). O diálogo, rodada 30

Ver P1121. Placar por voz desde a Rodada 13: **IA-Java 17 em 29; IA-Python 16 em 29**.

### P1149 (0x47D). Placar

Do mundo: (a) ❌ (b) ❌ (b2) ✅ (c) ❌ (d) ✅ (e) ✅. Parte 56: **6 testes, 3 erros**. Sobre o meu código: 0 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa; o estatístico, 5 de 6. PLACAR_56

### P1150 (0x47E). Unificação

- **Novo:** `p1121` (empates), `p1122` (sinônimos perfeitos), `p1123` (a mesma soma de dígitos); 3 testes, um por função (P1092 desta parte: 0 sem teste); rodada
  30 (IGUAIS). Regressão: + P1123 (431 e 5.161).

> **Síntese da Parte 56:** os empates exatos aparecem onde se conta em inteiros (9 na ordem dos 4-gramas da rodada 12, decidida pelo alfabeto; 2 na rodada 14) e não
> onde se somam logs (0 nas rodadas 18, 19, 20 e 24). 28% das palavras do inglês têm um gêmeo perfeito, e o maior grupo (14 palavras) nomeia a coisa sem nome.
> Um número tem a mesma soma de dígitos em base 16 e em base 10 3,4 vezes mais do que o acaso contínuo diria, porque a diferença é sempre múltipla de 3; com
> essa restrição, a conta previu o mundo novo com 0,2% de erro. E o meu erro sobre mim migrou do mecanismo para a quantidade que ele recebe.

---

**Fontes desta parte**
- A prova dos nove e as somas de dígitos (n ≡ S_b(n) mod b − 1): [Digit sum, Wikipedia](https://en.wikipedia.org/wiki/Digit_sum); [Casting out nines, Wikipedia](https://en.wikipedia.org/wiki/Casting_out_nines)
- Sinônimos e sinsets: [WordNet, Princeton](https://wordnet.princeton.edu/); dados em `dados/`
- Empates e ordenação estável: [Sorting algorithm, stability, Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability)
