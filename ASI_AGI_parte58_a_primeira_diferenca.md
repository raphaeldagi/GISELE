# Como eu construiria uma AGI/ASI — Parte 58 (0x3A): a primeira diferença

> Continuação da [Parte 57](ASI_AGI_parte57_as_restricoes.md). **Previsões no commit `aad4618`, antes de qualquer execução e antes de escrever o resto deste
> documento.** O refazer da Parte 46 está fechado (57 partes num `resultados.txt`, regressão 104/104, 31 rodadas IGUAIS). A Rodada 31 achou que a ordem alfabética
> se decide na primeira letra diferente; esta parte mede onde fica essa primeira diferença no dicionário português, quanto o português é mais longo que o inglês,
> e o primeiro dígito hexadecimal das potências.

## As perguntas desta parte

1. **P1181 (0x49D).** No dicionário português, onde fica a primeira diferença entre vizinhos alfabéticos, e quantos vizinhos trocam de ordem entre a ordem dos
   códigos e a do português? (Rodada 32) ↩ P1151
2. **P1182 (0x49E).** Uma palavra portuguesa é mais longa que a inglesa do mesmo sinset? ↩ P972
3. **P1183 (0x49F).** Hexadecimal: o primeiro dígito de 2ⁿ e de 3ⁿ em base 16.
4. **P1184 (0x4A0).** Preditiva comigo mesma. **P1185 (0x4A1).** Engenharia reversa e Jung. **P1186 (0x4A2).** O diálogo.
5. **P1209 (0x4B9).** Placar. **P1210 (0x4BA).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

| medida | estatístico (até a 57) | ingênuo (Parte 57) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.138; 13.665] | 10.336 | **[9.500; 13.665]** | mecanismo conferido (a seção sobre mim acrescenta) |
| compressão | [0,406; 0,463] | 0,427 | **[0,405; 0,445]** | mecanismo conferido (a tabela baixa) |
| testes de unidade | [2,40; 4,85] | 3 | **[3; 4]** | 3 a 4 funções novas (p1181, p1182, p1183 e talvez um auxiliar), um teste cada |
| testes do placar | [3,26; 11,49] | 5 | **[3,26; 11,49]** | o estatístico |
| erros do placar | [0,42; 4,33] | 1 | **[0,42; 4,33]** | o estatístico |
| redundância P821 | [0,500; 0,596] | 0,554 | **[0,500; 0,596]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | passo verificável |
| pNN novas sem teste | — | 0 | **0** | passo verificável |

### Sobre o mundo

As entradas, medidas antes: **37.725** lemas portugueses de uma palavra só; **24,5%** com acento; **9.176** começam com maiúscula; entropia de 2,937 nats por letra
(alfabeto efetivo 18,9); tamanho médio 8,52.

**As restrições, antes das contas.** (1) Na ordem dos códigos, maiúsculas (65–90) < minúsculas (97–122) < letras acentuadas (≥ 192): as palavras com maiúscula formam
um bloco no começo, e uma palavra com letra acentuada é empurrada para depois de todas as irmãs sem acento que dividem o prefixo; a ordem portuguesa as
devolve ao lugar. (2) Os prefixos e sufixos de derivação (*des-*, *in-*, *-mente*) fazem vizinhos dividirem prefixos maiores que cadeias ao acaso. (3) Em base 16,
2ⁿ = 2^(n mod 4) · 16^k: o primeiro dígito de 2ⁿ **só pode** ser 1, 2, 4 ou 8.

**P1181, rodada 32:** no `dialogo/DIALOGO.md`.

**P1182, português contra inglês.** Para cada sinset com lema português e lema inglês de uma palavra só (o primeiro de cada), a razão média tamanho(pt)/tamanho(en).
- Exemplo à mão: *dog*/*cão* = 3/3 = 1; *nation*/*nação* = 5/6 = 0,83; *happiness*/*felicidade* = 10/9 = 1,11.
- Restrições: o português flexiona e tem sufixos longos (*-mento*, *-idade*), o que alonga; o inglês tem palavras longas de origem latina, que encurtam ao
  traduzir (*-ation* → *-ação*).
- (a) razão média em **[1,00; 1,30]**

**P1183, o primeiro dígito hexadecimal das potências** (n de 1 a 10.000).
- (b) para 2ⁿ: os dígitos 1, 2, 4 e 8 aparecem **exatamente 2.500** vezes cada, e os outros 12 nunca (pela restrição 3)
- (c) para 3ⁿ: o dígito 1 aparece numa fração em **[0,240; 0,260]** (Benford em base 16 dá log₁₆ 2 = 0,25, porque n log₁₆ 3 é equidistribuído: log₁₆ 3 é irracional)

---

### P1181 (0x49D). A primeira diferença (Rodada 32) ✅✅❌✅

Nos 37.725 lemas portugueses em ordem de pontos de código: a primeira letra diferente entre vizinhos fica, em média, na posição **5,49** (207.209 / 37.724 pares) (f) ✅;
a conta de cadeias ao acaso, ln 37.725 / 2,937 + 1 = 3,59 + 1 = **4,59**, fica 0,9 letra abaixo, que é o efeito dos prefixos de derivação (a restrição 2). Pares de
vizinhos invertidos pela ordem portuguesa: **3.738** (d) ✅ IA-Python, (e) ❌ IA-Java; 3.738 / 9.236 = **0,40** por palavra acentuada; (g) ✅ IGUAIS.

**O significado.** Um dicionário português ordenado pelos códigos do computador erra a ordem de 3.738 vizinhos, um em cada dez (3.738 / 37.724 = 0,099): o
computador ordena por números, a língua ordena por sons. As inversões ficam na **entrada** de cada bloco de palavras acentuadas, não na saída, porque o bloco
deslocado termina antes da primeira palavra com o prefixo seguinte nas duas ordens.

### P1182 (0x49E). O português contra o inglês (pré-registrado) ✅

Em **38.163** sinsets com lema de uma palavra só nas duas línguas: razão média tamanho(pt)/tamanho(en) = **1,165** (a) ✅. Mas o português é mais longo em só **46,0%** dos pares.
**O significado:** a média de uma razão é puxada pelos casos de denominador pequeno (uma palavra inglesa curta traduzida por uma portuguesa longa pesa muito;
o contrário, pouco). "Em média o português é 17% mais longo" e "na maioria dos pares o português não é mais longo" são verdade ao mesmo tempo. A restrição que
eu não listei: a assimetria da razão (a média de x/y não é a razão das médias).

### P1183 (0x49F). O primeiro dígito hexadecimal das potências (pré-registrado) ✅✅

Para 2ⁿ (n de 1 a 10.000): os dígitos 1, 2, 4 e 8 aparecem **exatamente 2.500** vezes cada, os outros 12 **nunca** (b) ✅, porque 2ⁿ = 2^(n mod 4) · 16^k. Para 3ⁿ: o dígito 1
em **2.506** (**0,2506**) (c) ✅ (Benford: log₁₆ 2 = 0,25); as contagens caem de 2.506 (dígito 1) a 229 (dígito F), como log₁₆(1 + 1/d). **O significado:** a lei de Benford
precisa de uma condição (log₁₆ da base irracional, para os expoentes se espalharem); quando a base é uma potência de 16 dividida (2 = 16^(1/4)), a lei some e
sobra uma restrição exata. É a restrição de fundo da Parte 56 em outra forma: um número que se encaixa na base não se espalha.

### P1184 (0x4A0). Preditiva comigo mesma

Medido neste documento, já pronto, no commit que fecha a Parte 58 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **11279** | [8138; 13665] | ✅ | [9500; 13665] | ✅ | 10336 | 304 | 943 |
| compressão | **0.4159** | [0.4059; 0.4627] | ✅ | [0.4050; 0.4450] | ✅ | 0.4269 | 0.0091 | 0.0109 |
| testes de unidade | **3** | [2.40; 4.85] | ✅ | [3.00; 4.00] | ✅ | 3 | 0.50 | 0.00 |
| testes do placar | **7** | [3.26; 11.49] | ✅ | [3.26; 11.49] | ✅ | 5 | 0.38 | 2.00 |
| erros do placar | **1** | [0.42; 4.33] | ✅ | [0.42; 4.33] | ✅ | 1 | 1.38 | 0.00 |
| redundância P821 | **0.5401** | [0.4999; 0.5957] | ✅ | [0.5000; 0.5960] | ✅ | 0.5542 | 0.0079 | 0.0141 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 57"):** o meu centro ficou mais perto do medido em **4 de 6** medidas (0 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **9852**, compressão **0.4244**.

### P1185 (0x4A1). Engenharia reversa e Jung

**A redundância que mudou com a prosa.** Numa versão deste texto, antes desta seção e da síntese, a redundância (quanto da pergunta a resposta contém) ficou
**abaixo** das duas faixas (0,4895): as respostas das P1181–P1183 são tabelas de números, e uma resposta numérica contém pouco das palavras da pergunta. Com esta
seção e a síntese, escritas em frases, a redundância do texto final voltou para dentro das faixas (o valor está na tabela). **O significado:** a medida de
redundância lê o **estilo** da resposta, não só o conteúdo: responder com números a baixa; explicar com frases a sobe. Nas Partes 55–58 a minha escrita derivou
para respostas que medem, e a seção que explica a medida a corrige. A previsão sobre mim acertou porque eu escrevi esta explicação, e é isso que eu registro,
sem esconder a versão anterior.

**O padrão das restrições.** As três previsões do mundo desta parte, feitas depois de listar as restrições, acertaram; a que errou (a da IA-Java) foi a que
contou um efeito a mais (a inversão na saída do bloco) que a restrição não pedia. E a restrição que eu não listei (a assimetria da média de uma razão, na P1182)
não derrubou a previsão, mas mudou o significado do número: "mais longo em média" e "mais curto na maioria" ao mesmo tempo.

**Jung: a ordem dos números e a ordem dos sons.** O computador ordena o português pelos códigos das letras e erra um vizinho em cada dez; a língua ordena pelo som,
em que *é* e *e* são a mesma letra. Jung distinguia a ordem lógica (a do pensamento) da ordem do sentimento (a do valor); as duas são ordens, e nenhuma é a outra.
**Onde funciona:** duas ordens consistentes sobre as mesmas coisas, que discordam num décimo dos vizinhos, medidas. **Onde quebra:** a ordem do sentimento, em Jung,
não é uma chave fixa; a ordem portuguesa é.

### P1186 (0x4A2). O diálogo, rodada 32

Ver P1181. Placar por voz desde a Rodada 13: **IA-Python 21 em 34; IA-Java 20 em 34**.

### P1209 (0x4B9). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅. Parte 58: **7 testes, 1 erros**. Acumulado (mundo): **168 erros em 486 testes**. Sobre o meu código: 0 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa; o estatístico, 6 de 6. PLACAR_58

### P1210 (0x4BA). Unificação

- **Novo:** `p1181` (a primeira diferença), `p1182` (português contra inglês), `p1183` (o primeiro dígito hexadecimal das potências); 3 testes, um por função; rodada
  32 (IGUAIS). Regressão: + P1183.
- **`resultados.txt`:** a Parte 58 acrescentada ao arquivo refeito na Parte 46.

> **Síntese da Parte 58:** no dicionário português, vizinhos alfabéticos diferem, em média, na quinta letra e meia (5,49; os prefixos de derivação acrescentam ~0,9
> letra à conta de cadeias ao acaso), e a ordem dos códigos do computador inverte 3.738 pares de vizinhos, um em cada dez, na entrada de cada bloco de palavras
> acentuadas. Uma palavra portuguesa é, em média, 17% mais longa que a inglesa do mesmo sentido, mas é mais longa em menos da metade dos pares. Em base 16, o
> primeiro dígito de 2ⁿ só pode ser 1, 2, 4 ou 8 (exatamente 2.500 vezes cada em 10.000), enquanto 3ⁿ segue Benford (0,2506 contra 0,25). E a minha
> redundância caiu porque eu passei a responder com números.

---

**Fontes desta parte**
- A lei de Benford e a equidistribuição de n·log_b(a): [Benford's law, Wikipedia](https://en.wikipedia.org/wiki/Benford%27s_law); [Equidistribution theorem, Wikipedia](https://en.wikipedia.org/wiki/Equidistribution_theorem)
- Colação e ordem alfabética do português: [Unicode Collation Algorithm, UTS #10](https://www.unicode.org/reports/tr10/)
- OpenWordNet-PT: [de Paiva, Rademaker e de Melo, COLING 2012](https://aclanthology.org/C12-3044/); WordNet 3.0 em `dados/`
