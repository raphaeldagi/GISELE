# Como eu construiria uma AGI/ASI — Parte 57 (0x39): as restrições

> Continuação da [Parte 56](ASI_AGI_parte56_empates.md). **Previsões no commit `4eddc47`, antes de qualquer execução e antes de escrever o resto deste
> documento.** A Parte 56 achou que a conta fecha quando acho a restrição escondida (a rede dos múltiplos de 3). Esta parte aplica a regra antes de cada conta:
> listar as restrições, depois prever. Palíndromos no dicionário, números palíndromos em base 10 e 16 ao mesmo tempo, e a ordem alfabética do português.

## As perguntas desta parte

1. **P1151 (0x47F).** A ordem dos 4-gramas empatados muda se o alfabeto for o do português? (Rodada 31) ↩ P1121
2. **P1152 (0x480).** Quantas palavras do WordNet são palíndromos, contra um modelo de letras independentes?
3. **P1153 (0x481).** Hexadecimal: quantos números abaixo de 10⁶ são palíndromos em base 10 e em base 16?
4. **P1154 (0x482).** Preditiva comigo mesma. **P1155 (0x483).** Engenharia reversa e Jung. **P1156 (0x484).** O diálogo.
5. **P1179 (0x49B).** Placar. **P1180 (0x49C).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

O estatístico (até a Parte 56), os mecanismos conferidos e o efeito da regra com faixa na quantidade que entra nela: 3 a 4 funções novas (p1151, p1152, p1153 e
talvez um auxiliar), logo **3 a 4** testes de unidade.

| medida | estatístico | ingênuo (Parte 56) | **eu** |
|---|---|---|---|
| caracteres | [7.599; 13.614] | 12.464 | **[9.500; 13.614]** |
| compressão | [0,407; 0,468] | 0,421 | **[0,405; 0,445]** |
| testes de unidade | [2,40; 4,85] | 3 | **[3; 4]** |
| testes do placar | [4,00; 11,75] | 6 | **[4,00; 11,75]** |
| erros do placar | [0,74; 4,26] | 3 | **[0,74; 4,26]** |
| redundância P821 | [0,490; 0,597] | 0,501 | **[0,490; 0,597]** |
| previsões unilaterais | — | 0 | **0** |
| pNN novas sem teste | — | 0 | **0** |

### Sobre o mundo

**P1152, palíndromos no dicionário** (lemas alfabéticos de 3 letras ou mais, minúsculos). As entradas da conta, medidas antes: 77.197 palavras; Σp² das letras = 0,0629.
Modelo de letras independentes: P(palíndromo de tamanho L) = (Σp²)^⌊L/2⌋; somando sobre a distribuição dos tamanhos: **116** palíndromos esperados.
- **As restrições, antes da previsão:** (1) a primeira e a última letra de uma palavra têm distribuições diferentes (terminações *-s*, *-e*, *-y*; inícios *s*, *c*, *p*):
  a chance de coincidirem é menor que Σp²; (2) palavras curtas de 3 letras (*eve*, *pop*, *dad*) puxam para cima. Peso maior para (1): centro 0,7 × 116 = 81.
- Exemplo à mão: *civic*, *level*, *radar*, *kayak* são palíndromos do inglês; não conferi se estão no WordNet como lemas.
- (a) palíndromos em **[47; 140]** (centro 81, ×1,72)

**P1153, palíndromos em base 10 e 16** (1 a 999.999). Entradas medidas antes: 1.998 palíndromos decimais; para cada um, a chance de ser palíndromo em hexadecimal
16^(−⌊k/2⌋) (k dígitos hexadecimais): soma **25,3** esperados.
- **As restrições:** os dois sistemas dividem o fator 2 (a paridade do último dígito é a de n nos dois), o que amarra a paridade dos primeiros dígitos; em média
  isso não muda a probabilidade. Centro 25,3.
- Exemplo à mão: 353 = 0x161, palíndromo nos dois (3·256 = 768 > 353? não: 0x161 = 256 + 96 + 1 = 353 ✓).
- (b) duplos palíndromos em **[14,7; 43,5]** (centro 25,3, ×1,72)

---

### P1151 (0x47F). O alfabeto do português (Rodada 31) ✅❌✅

Reordenando os 13 primeiros 4-gramas pela ordem de um dicionário português (sem acentos e minúscula, depois a original), **0** pares mudam de ordem (c) ✅ IA-Python,
(d) ❌ IA-Java, (e) ✅ IGUAIS. Dois dos 13 têm acento (*pré registrado na pergunta*, sozinho no seu grupo de empate; *continuação da parte asi*, decidido em *con-t*
contra *con-s*). **A restrição:** a ordem alfabética se decide na primeira letra diferente, e o acento português mora no fim da palavra. Para um acento mudar a
ordem, as duas palavras precisam ser iguais até ele; nos 4-gramas mais frequentes, isso não acontece.

### P1152 (0x480). Palíndromos no dicionário (pré-registrado) ✅

Das **77.197** palavras (3 letras ou mais), **104** são palíndromos (a) ✅ (em [47; 140]): *aaa, aba, ada, aga, akka, ala, alula, ana, anna, ara, bib, bob*, … As contas:
- letras independentes: Σ_L f(L) × (Σp²)^⌊L/2⌋, com Σp² = 0,0629: **116,2**
- com as pontas reais (a chance de a primeira letra ser igual à última, medida nas palavras, no lugar de Σp² para o par de fora): **86,7**
- medido: **104**, entre as duas

**O significado.** As duas restrições que listei agem em sentidos opostos e se compensam em parte: as pontas diferentes (terminações) baixam; as palavras curtas
de três letras (nomes, siglas que viraram palavras: *aba*, *ada*, *bob*) sobem. A conta com as pontas acerta a direção da primeira restrição, e a diferença
(104 − 86,7 = 17) mede a segunda.

### P1153 (0x481). Palíndromos em base 10 e 16 ao mesmo tempo (pré-registrado) ✅

Abaixo de 10⁶: **27** números (b) ✅ (em [14,7; 43,5]); a conta, Σ 16^(−⌊k/2⌋) sobre os 1.998 palíndromos decimais, dava **25,3** (desvio de Poisson √25,3 = 5,0: o medido está a
0,3 desvio). Os primeiros: 1–9, 11 (0xB), **353** (0x161), **626** (0x272), **787** (0x313), **979** (0x3D3), **1991** (0x7C7), **3003** (0xBBB), 39593 (0x9AA9), 41514 (0xA22A),
90209 (0x16061), 94049 (0x16F61). **O significado:** a conta de independência entre as bases funciona aqui, ao contrário da P1123, porque a restrição comum (o fator
2) só amarra paridades, e um palíndromo não depende da paridade em média.

### P1154 (0x482). Preditiva comigo mesma

Medido neste documento, já pronto, no commit que fecha a Parte 57 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **10250** | [7599; 13614] | ✅ | [9500; 13614] | ✅ | 12464 | 1307 | 2214 |
| compressão | **0.4265** | [0.4073; 0.4675] | ✅ | [0.4050; 0.4450] | ✅ | 0.4214 | 0.0015 | 0.0051 |
| testes de unidade | **3** | [2.40; 4.85] | ✅ | [3.00; 4.00] | ✅ | 3 | 0.50 | 0.00 |
| testes do placar | **5** | [4.00; 11.75] | ✅ | [4.00; 11.75] | ✅ | 6 | 2.88 | 1.00 |
| erros do placar | **1** | [0.74; 4.26] | ✅ | [0.74; 4.26] | ✅ | 3 | 1.50 | 2.00 |
| redundância P821 | **0.5500** | [0.4897; 0.5969] | ✅ | [0.4900; 0.5970] | ✅ | 0.5008 | 0.0065 | 0.0493 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 56"):** o meu centro ficou mais perto do medido em **4 de 6** medidas (0 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **8821**, compressão **0.4365**.

### P1155 (0x483). Engenharia reversa e Jung

**Listar as restrições antes de prever funcionou.** As três previsões do mundo que eu fiz com a regra nova (listar as restrições, depois a conta) acertaram:
os palíndromos (104 em [47; 140], entre as duas contas), os duplos palíndromos (27 contra 25,3) e o alfabeto português, pela voz que acertou. A única errada
desta parte foi a da IA-Java, que previu pela **quantidade** de acentos e não pelo **lugar** deles: a restrição certa era posicional (a ordem se decide na
primeira letra diferente), e ela não foi listada.

**O padrão, e o significado.** Nas Partes 55 e 56 os meus erros eram "esquecer a condição de fundo"; nesta, depois de listar as condições, os erros sumiram,
exceto onde a lista não foi feita. O padrão é simples e forte: **o que eu nomeio antes, eu não erro; o que eu não nomeio, eu erro.** A lista funciona como
uma pergunta que obriga a olhar o fundo. E houve um erro de outro tipo, no diálogo: escrevi "o único com acento" sem conferir; a função p1151 contou dois.
Toda afirmação de quantidade no texto sai de uma função, inclusive as do diálogo.

**Jung: a ordem que mora no fim.** O alfabeto decide pela primeira diferença, e o português põe as suas marcas (o acento, a nasal, o til) no fim das palavras.
Jung via a individualidade na mesma posição: as pessoas começam iguais (a mesma estrutura, os mesmos arquétipos) e se diferenciam no fim do caminho. **Onde
funciona:** uma ordem que decide cedo não enxerga a diferença tardia; as palavras que só diferem no acento ficam empatadas até ele. **Onde quebra:** a
diferenciação de Jung é um processo; o acento é uma marca fixa.

### P1156 (0x484). O diálogo, rodada 31

Ver P1151. Placar por voz desde a Rodada 13: **IA-Java 18 em 31; IA-Python 18 em 31**.

### P1179 (0x49B). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅. Parte 57: **5 testes, 1 erros**. Sobre o meu código: 0 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa; o estatístico, 6 de 6. Acumulado (mundo): **167 erros em 479 testes**; taxa média 0,349, intervalo 90% [0,314; 0,385].

### P1180 (0x49C). Unificação

- **Novo:** `p1151` (o alfabeto do português), `p1152` (palíndromos), `p1153` (duplos palíndromos); 3 testes, um por função; rodada 31 (IGUAIS). Regressão: + P1153 (27).

> **Síntese da Parte 57:** listar as restrições antes de cada conta funcionou: o dicionário tem 104 palíndromos, entre a conta de letras independentes (116) e a
> conta com as pontas reais das palavras (87); há 27 números abaixo de 10⁶ palíndromos em base 10 e 16, contra 25,3 previstos (aqui as bases só se amarram pela
> paridade, e a independência vale); e a ordem do português não muda os 4-gramas empatados, porque o acento mora no fim da palavra e a ordem se decide na
> primeira letra diferente. O erro da parte foi o da voz que contou os acentos sem perguntar onde eles ficam: o que eu nomeio antes, eu não erro.

---

**Fontes desta parte**
- Números palíndromos em várias bases: [Palindromic number, Wikipedia](https://en.wikipedia.org/wiki/Palindromic_number); conferência: os primos da minha lista
  (2, 3, 5, 7, 11, 353, 787) são os primeiros termos de [OEIS A046484](https://oeis.org/A046484), primos palíndromos em base 10 e 16
- Ordenação alfabética com acentos (colação): [Unicode Collation Algorithm, UTS #10](https://www.unicode.org/reports/tr10/)
- WordNet 3.0 (Princeton) no data lake (`dados/`)
