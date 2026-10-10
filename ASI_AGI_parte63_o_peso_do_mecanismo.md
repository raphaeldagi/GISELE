# Como eu construiria uma AGI/ASI — Parte 63 (0x3F): o peso do mecanismo

> Continuação da [Parte 62](ASI_AGI_parte62_o_ultimo_digito.md). **Próxima:** [Parte 64 — o fator do final](ASI_AGI_parte64_o_fator_do_final.md) (P1361–P1390). Previsões nos commits `fb55f1b` ((a) a (g)) e `abbb6da` ((h)). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 62 pediu uma regra: todo mecanismo deduzido ganha uma conta do seu peso num caso fora do teste, antes do registro.
> Esta parte é a primeira com essa regra. Pergunta se o fator de congruência efetivo explica a base 8, quanto a glosa portuguesa é mais longa que a inglesa,
> e quantos primos palíndromos há em hexadecimal.

## As perguntas desta parte

1. **P1331 (0x533).** O fator de congruência efetivo explica a base 8? (Rodada 37) ↩ P1301
2. **P1332 (0x534).** A glosa portuguesa da OpenWordNet-PT é mais longa que a inglesa do mesmo sinset? ↩ P1302
3. **P1333 (0x535).** Hexadecimal: quantos primos palíndromos há até 16⁵? ↩ P1303
4. **P1334 (0x536).** Preditiva comigo mesma. **P1335 (0x537).** Engenharia reversa e Jung. **P1336 (0x538).** O diálogo.
5. **P1359 (0x54F).** Placar. **P1360 (0x550).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1331, p1332, p1333).

| medida | estatístico (até a 62) | ingênuo (Parte 62) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [7.432; 20.719] | 15.473 | **[7.432; 20.719]** | o estatístico |
| compressão | [0,405; 0,434] | 0,411 | **[0,405; 0,434]** | o estatístico |
| testes de unidade | [1,34; 7,91] | 5 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [4,02; 10,23] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,83; 4,67] | 3 | **[0,83; 4,67]** | o estatístico |
| redundância P821 | [0,505; 0,620] | 0,582 | **[0,505; 0,620]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1332, a glosa portuguesa e a inglesa.** Nos sinsets que têm glosa na OpenWordNet-PT (7.945), a razão (palavras da glosa portuguesa)/(palavras da definição
inglesa, sem os exemplos), e a sua mediana.
- **Restrições, com peso:** (1) o português usa mais palavras funcionais (contrações *do*, *na*, artigos antes de possessivos), o que alonga; (2) mas as glosas
  portuguesas não são traduções literais: algumas são notas curtas ("(geralmente seguido de 'de')"); (3) o português começa a definição sem artigo
  ("entidade que…" contra "an entity that…"), o que encurta em uma palavra. Peso: sem medida externa; a literatura de tradução fala em ~10–20% a mais de
  palavras do inglês para as línguas românicas (não conferido por mim).
- Exemplo à mão: "an entity that has physical existence" (6) contra "entidade que tem existência física" (5): razão 0,83.
- (a) mediana da razão em **[0,85; 1,30]**
- (b) fração dos sinsets em que a glosa portuguesa é mais longa que a inglesa em **[0,35; 0,70]**

**P1333, os primos palíndromos em base 16** (n de 1 a 16⁵ cujos dígitos hexadecimais formam um palíndromo, e primo).
- **Restrições, com peso (calculadas por código antes do registro):** (1) todo palíndromo de comprimento par é divisível por 17 = 0x11 (como os de base 10 por
  11): conferido para os de 2 e 4 dígitos; só o 0x11 sobra; (2) um primo > 2 é ímpar, então o primeiro dígito também é ímpar; (3) entre os ímpares, a densidade
  dos primos é 2/ln n.
- **A conta:** 1 dígito: os primos 2, 3, 5, 7, 0xB, 0xD (6, exatos); 2 dígitos: só 0x11 (1); 3 e 5 dígitos: Σ 2/ln n sobre os palíndromos ímpares = **350,5**.
  Total: 6 + 1 + 350,5 = **357,5**.
- Exemplo à mão: 0x101 = 257, primo (é um primo de Fermat); 0x111 = 273 = 3 × 7 × 13: não.
- (c) quantidade em **[320; 400]** (a conta ± ~11%: a densidade 2/ln n é a do teorema dos números primos, e os palíndromos de 3 dígitos são pequenos)

**P1331, rodada 37:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).

### Previsão nova num mundo novo (registrada antes de contar)

**Resultado de (c), antes desta seção:** **357** primos palíndromos em base 16 contra a conta de **357,5**: 0,1% de erro. Uma conta que acerta assim num mundo
pede outro mundo. `p1337_conta_palindromos` calcula só a conta, sem contar os primos de comprimento ímpar ≥ 3 (calculada antes deste registro):
- (h) **Base 12**, até 12⁵ = 248.832 (o 13 = 0x11 em base 12 divide todo palíndromo de comprimento par; os dígitos finais 3 e 9 são múltiplos de 3, e a média
  sobre os finais ímpares continua 2/ln n): conta **177,3**; previsão: quantidade em **[156; 199]** (± 12%).
- (controle, fora do placar) **Base 10**, até 10⁷: conta **768,5**. Eu lembro o valor da literatura (OEIS A050251: 781 primos palíndromos abaixo de 10⁷); por
  isso este não é um teste cego e não entra no placar: só confere a função contra a fonte.

**Resultado de (h):** **196** primos palíndromos em base 12 contra a conta de **177,3** ✅ (dentro de [156; 199], 10,5% acima da conta). O controle de base 10: **781**,
o valor da OEIS A050251, com a conta em 768,5 (1,6% abaixo).

---

## As respostas

### P1331 (0x533). O fator efetivo (Rodada 37) ✅✅✅❌

**Na pergunta.** "Generaliza o g" supõe que g é um caso particular de alguma coisa. É: g é o maior divisor de b − 1 em que a congruência vale para **todos** os
candidatos; F mede a fração em que ela vale, divisor a divisor juntos. Quando F = g, nada se ganha; a pergunta é onde F ≠ g.

**Lógica.** `p1331_fator_efetivo` (rodada 37, IGUAL em Java). A conta com F no lugar de g, nas células sem interruptor:
- total: conta 116,81 → **131,16**; medido 175; a razão cai de **1,498** para **1,334**;
- base 8: conta 2,983 → **3,762**; a razão cai de 4,358 para **3,455**;
- F se afasta de g mais de 10% em **42 das 84** células (0,50).

O peso medido fora do teste (k = 8: razão de 1,222 para 1,188, −3%) previu bem a direção e mal o tamanho dentro do teste (−11%), porque nos k pequenos as
células têm poucos candidatos e F oscila em torno de g. Somando as três correções (g, o último dígito, F), a base 8 continua 3,5 vezes acima: o seu excesso não
é de congruência.

**Tradução cruzada.** Um fator que vale "em média" (F) e um que vale "sempre" (g) são a diferença entre uma tendência e uma lei. Na psicologia, a diferença entre um
traço (que aparece na maioria das situações) e um reflexo (que aparece em todas).

**Meta.** A base 8 tem só 13 soluções sem interruptor; um excesso de 3,5 sobre 3,8 esperados pode ter uma parte de sorte (Poisson com média 3,762 dá 13 ou mais com
chance **1,5·10⁻⁴**, pela `p1338_contas_da_parte63`; eu tinha escrito ~0,03% de cabeça, o dobro): não é sorte, mas a medida é pequena.

### P1332 (0x534). A glosa portuguesa e a inglesa ✅✅

**Na pergunta.** "Mais longa" pressupõe que a glosa portuguesa traduz a inglesa. Não traduz sempre: algumas são notas curtas, outras são explicações longas. A
mediana mede a glosa típica, e a média mede as longas.

**Lógica.** `p1332_glosa_pt_e_en`: nos **7.945** sinsets com glosa portuguesa, a razão de palavras PT/EN tem mediana **1,000** (a faixa (a) era [0,85; 1,30]) ✅ e
média **1,634**; a portuguesa é mais longa em **43,1%** dos casos (a faixa (b) era [0,35; 0,70]) ✅. A distância entre a média e a mediana (1,63 contra 1,00) diz
que a distribuição tem uma cauda longa: há glosas portuguesas muito maiores que a inglesa (explicações), não um alongamento uniforme.

Ao acaso: a faixa (a) cobria 0,45 de uma razão plausível entre 0,5 e 2; o ingênuo "10–20% mais longa", da literatura de tradução, erraria a mediana por 0,10 a
0,20.

**Tradução cruzada.** A glosa típica tem o mesmo tamanho nas duas línguas: um conceito ocupa o mesmo espaço quando é bem conhecido. As caudas são os conceitos que
uma das línguas precisa explicar mais, como uma cultura que descreve com uma frase o que a outra diz com uma palavra.

**Meta.** Contei palavras por espaços; contrações (*do*, *na*) contam como uma palavra, como no inglês "of the" contam duas: isso puxa o português para baixo.

### P1333 (0x535). Os primos palíndromos em base 16 ✅ (e (h) ✅)

**Na pergunta.** "Palíndromo" e "primo" parecem independentes; a pergunta já tinha a restrição escondida: um palíndromo de comprimento par é múltiplo de
b + 1 (em base 16, de 0x11 = 17), então o comprimento decide a metade da resposta antes de qualquer conta de primos.

**Lógica (a conta antes da medida).** 6 primos de 1 dígito, 1 de 2 dígitos (0x11), e Σ 2/ln n sobre os palíndromos ímpares de 3 e 5 dígitos = 350,5: conta
**357,5**. **Medido** (`p1333_primos_palindromos`): **357** ✅, a **0,1%** da conta (36 de 3 dígitos, 314 de 5). A base 12 (h), num mundo novo: conta 177,3,
medido **196** ✅ (10,5% acima). A base 10, como controle: 781 (a OEIS A050251), conta 768,5.

Ao acaso: a faixa (c) tinha 80 de largura numa escala em que qualquer número de 0 a ~4.000 (os palíndromos) seria possível; o ingênuo "a fração dos primos
entre todos os números, π(16⁵)/16⁵ ≈ 0,078, vezes os 4.350 palíndromos" daria **340,3** (`p1338`), a 4,7% do medido: perto por acaso, porque erra duas vezes em sentidos opostos (ignora o fator 17 que mata os pares e o fator 2 que favorece os ímpares).

**Tradução cruzada.** O palíndromo é uma simetria; a simetria par carrega um divisor (b + 1) e mata a primalidade, e a simetria ímpar, com um centro, não. Na
física, uma simetria impõe uma lei de conservação; aqui, impõe uma divisibilidade.

**Meta.** A conta acertou a 0,1% em base 16 e a 10% em base 12: a precisão da base 16 tem uma parte de sorte: sob a conta, o desvio da contagem é **4,8%** dela (`p1338`: Σ p(1 − p) nos palíndromos ímpares), e 0,1% é muito
menos que um desvio; a base 12, a 10,5%, fica a ~2 desvios.

### P1334 (0x536). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 1)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16208** | [7432; 20719] | ✅ | [7432; 20719] | ✅ | 15473 | 2132 | 735 |
| compressão | **0.4112 ↔ 0.4113** (ciclo de dois) | [0.4050; 0.4335] | ✅ | [0.4050; 0.4340] | ✅ | 0.4111 | 0.0082 | 0.0002 |
| testes de unidade | **5** | [1.34; 7.91] | ✅ | [2.00; 5.00] | ✅ | 5 | 1.50 | 0.00 |
| testes do placar | **8** | [4.02; 10.23] | ✅ | [6.00; 8.00] | ✅ | 8 | 1.00 | 0.00 |
| erros do placar | **1** | [0.83; 4.67] | ✅ | [0.83; 4.67] | ✅ | 3 | 1.75 | 2.00 |
| redundância P821 | **0.5966** | [0.5051; 0.6203] | ✅ | [0.5050; 0.6200] | ✅ | 0.5817 | 0.0341 | 0.0149 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 62"):** mais perto do medido em **1 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **14468**, compressão **0.4205**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 1 erros.
- **Erros de processo nesta parte:** 2 (um `ps aux | grep` com kill matou o próprio shell (ver a P1335); uma cauda de Poisson escrita de cabeça, errada por um fator 2, pega pela `p1338` antes do commit).

### P1335 (0x537). Engenharia reversa e Jung

**A regra da Parte 62 funcionou, e mostrou o seu limite.** Esta foi a primeira parte em que cada mecanismo deduzido teve o seu peso medido fora do teste antes do
registro, e 7 das 8 previsões do mundo acertaram (a melhor parte desde que o placar existe por letra). A que errou, (g), errou exatamente onde o caso de fora
**não parecia** o de dentro: com k = 8, cada célula tem milhares de candidatos e o fator efetivo fica colado em g; com k = 2 ou 3, poucos candidatos e muita
oscilação. **O significado:** "fora do teste" não basta; o caso de calibração precisa estar perto do teste na variável que move o mecanismo. **Regra ampliada:**
antes de usar um caso de calibração, dizer qual variável move o mecanismo e conferir que o caso tem valores dessa variável parecidos com os do teste (aqui, o
número de candidatos por célula); se não tiver, alargar a faixa.

**As contas de cabeça, de novo, e a regra que as pegou.** Três números do texto (uma cauda de Poisson, um desvio, um ingênuo) eu escrevi por estimativa; ao passá-los
por uma função (`p1338`), dois estavam certos e um errado por um fator 2 (0,03% contra 0,015%). A regra "todo número sai de uma função" pegou o erro antes do
commit. **O padrão:** eu estimo bem a ordem de grandeza e mal o fator; uma estimativa de cabeça é uma previsão, e deveria ser registrada como tal ou trocada por
código.

**O processo que matou o shell pela quarta vez.** Depois da regra da Parte 62 (usar `[c]alculos` na busca), um comando matou o próprio shell de novo: a busca
`ps aux | grep "[c]alculos.py 63"` não casa com a linha do grep, mas casa com a linha do **shell**, que continha "calculos.py 63" mais adiante (no reinício que eu
pus no mesmo comando). **O significado:** eu corrigi o sintoma (a linha do grep) e não o mecanismo (qualquer processo cuja linha de comando contenha o padrão,
inclusive o shell que roda o meu comando). **Regra ampliada:** matar e reiniciar em comandos separados; o comando que mata não contém, em lugar nenhum, o texto
do processo que reinicia.

**Jung: o peso de um complexo medido de fora.** No experimento de associação, Jung media a força de um complexo pelo atraso na resposta a palavras neutras, que
não tocavam o complexo diretamente: o peso medido fora do assunto. **Onde a formalização funciona:** é a minha regra da Parte 62 (medir o mecanismo num caso de
fora) e funcionou nesta parte. **Onde quebra:** Jung sabia que a palavra neutra precisava estar perto do complexo para revelar o atraso (as palavras "neutras"
eram escolhidas na mesma vizinhança semântica); eu escolhi um caso de fora longe demais (k = 8) na variável que importava.

### P1336 (0x538). O diálogo, rodada 37

Ver P1331. Placar por voz da função `p1241_placar_por_voz(37)`: IA-Python 17 em 31; IA-Java 15 em 31 (regra estrita, rodadas 13 a 37).

### P1359 (0x54F). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ✅. Parte 63: **8 testes, 1 erros**. Acumulado (mundo): **182 erros em 527 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; o estatístico, 6 de 6; e 2 erros de processo (P1335).

### P1360 (0x550). Unificação

- **Novo:** `p1331` (o fator efetivo, rodada 37, IGUAIS), `p1332` (glosa portuguesa contra inglesa), `p1333` (primos palíndromos numa base, com a conta), `p1337`
  (só a conta). Regressão: + P1333 (357; 42 de 84 células).
- **Regra nova (no `CLAUDE.md`):** ver a P1335.

> **Síntese da Parte 63:** o fator de congruência efetivo, com o peso medido fora do teste antes, explica um pouco mais do excesso dos narcisistas (a razão total cai de 1,498 para 1,334), e
não explica a base 8, que continua 3,5 vezes acima: o excesso dela não é de congruência. A glosa portuguesa típica da OpenWordNet-PT tem o mesmo tamanho que a inglesa
(mediana 1,00), com uma cauda de explicações longas (média 1,63). Os primos palíndromos em base 16 são 357, a 0,1% da conta feita antes (357,5), porque todo
palíndromo de comprimento par é múltiplo de 0x11; em base 12, 196 contra 177. Sete de oito previsões do mundo acertaram, a primeira parte com a regra do peso.

---

**Fontes desta parte**
- Primos palíndromos: [Palindromic prime, Wikipedia](https://en.wikipedia.org/wiki/Palindromic_prime); [OEIS A050251](https://oeis.org/A050251) (quantidade de
  primos palíndromos abaixo de 10ⁿ)
- Teorema dos números primos (a densidade 1/ln n): [Prime number theorem, Wikipedia](https://en.wikipedia.org/wiki/Prime_number_theorem)
- Experimento de associação de Jung: C. G. Jung, *Studies in Word Association* (1904–1910)
- OpenWordNet-PT: [de Paiva, Rademaker e de Melo, COLING 2012](https://aclanthology.org/C12-3044/); WordNet 3.0 em `dados/`
