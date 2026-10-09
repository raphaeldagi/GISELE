# Como eu construiria uma AGI/ASI — Parte 53 (0x35): preditiva comigo mesma

> Continuação da [Parte 52](ASI_AGI_parte52_o_metodo_ou_a_serie.md). **Previsões no commit `4f3dbff`, antes de qualquer execução e antes de escrever o resto
> deste documento.** O usuário pediu: *"Tente ser preditivo consigo mesmo. Grave na memória."* A regra entrou no `CLAUDE.md`. Esta parte prevê o
> **meu próprio** comportamento mensurável (o tamanho deste texto, quantos erros eu vou ter, quanto as minhas respostas vão conter das perguntas), com um
> preditor estatístico e com as minhas próprias previsões, e pontua as duas contra o preditor ingênuo.

## As perguntas desta parte

1. **P1031 (0x407).** Qual é o meu histórico mensurável? (descritivo)
2. **P1032 (0x408).** Um preditor estatístico de mim mesma acerta a Parte 53? E eu, ajustando pelo mecanismo, acerto mais? (Rodada 27) ↩ P792
3. **P1033 (0x409).** No dicionário, o tamanho da definição prevê a profundidade da palavra na taxonomia? ↩ P793
4. **P1034 (0x40A).** Hexadecimal: prever o n-ésimo dígito hexadecimal de π sem calcular os anteriores (Bailey–Borwein–Plouffe).
5. **P1035 (0x40B).** Engenharia reversa. **P1036 (0x40C).** Jung. **P1037 (0x40D).** O diálogo.
6. **P1059 (0x423).** Placar. **P1060 (0x424).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado do placar do mundo)

Medidas deste documento quando estiver pronto (como em `p1031_historico_de_mim`). O preditor estatístico (`p1032`: média das últimas 8 partes ± 1,645 desvios)
e o ingênuo (o valor da Parte 52) já estão calculados; as **minhas** previsões ajustam o centro pelo que esta parte tem de diferente:

| medida | estatístico | ingênuo (Parte 52) | **eu** | o meu mecanismo |
|---|---|---|---|---|
| caracteres do documento | [7.437; 11.925] | 8.617 | **[8.800; 13.200]** | a seção sobre mim e a tabela acrescentam ~2.000 |
| compressão zlib | [0,431; 0,463] | 0,460 | **[0,438; 0,466]** | tabelas de números comprimem pior: centro 0,452 |
| testes de unidade escritos | [2,1; 4,2] | 4 | **[3; 5]** | p1031, p1032, p1033 e p1034 pedem um teste cada |
| testes do placar do mundo | [4,9; 14,9] | 8 | **[6; 10]** | rodada (3) + dicionário (2) + hexadecimal (2) + ~1 |
| erros no placar do mundo | [0,6; 5,1] | 2 | **[1; 4]** | taxa recente ~0,30 × ~8 testes = 2,4 |
| redundância da pergunta dada a resposta | [0,510; 0,598] | 0,551 | **[0,51; 0,61]** | falar de mim repete as perguntas: centro 0,56 |
| previsões unilaterais (P974) | — | 0 | **0** | a regra virou passo; sem faixa porque é uma contagem que deve ser zero |

Pontuação: acerto = dentro da faixa; e o erro absoluto do centro, contra o do ingênuo.

### Sobre o mundo

**P1033, definição e profundidade.** Para os substantivos com profundidade (P793), a correlação de Spearman entre o número de palavras da definição (a glosa sem
exemplos) e a profundidade.
- Exemplo à mão: *entity* (profundidade 0) tem uma definição longa e abstrata; *dog* (13) também é longa. O tamanho parece depender de outra coisa.
- (a) ρ em **[−0,05; 0,15]**

**P1034, os dígitos de π em hexadecimal.** A fórmula de Bailey–Borwein–Plouffe dá o n-ésimo dígito hexadecimal de π sem calcular os anteriores (em
ponto flutuante de 64 bits). Conferência: π exato em inteiros (fórmula de Machin) até 1.000 dígitos hexadecimais.
- Exemplo à mão: π = 3,243F6A88... em hexadecimal; o 1º dígito depois da vírgula é 2.
- (b) os 1.000 primeiros dígitos pela BBP coincidem **todos** com os exatos (1.000 de 1.000; sem faixa porque é um teste de exatidão)
- (c) o χ² das 16 frequências nos 1.000 dígitos (15 graus de liberdade) em **[7,26; 25,0]** (a faixa de 90% do χ²₁₅)

---

### P1031 (0x407). O meu histórico (descritivo)

Partes 31–52, medidas por `p1031_historico_de_mim`: o documento encolheu de ~19.000–27.000 caracteres (Partes 31–33) para ~8.000–12.000 (Partes 44–52); a
compressão zlib ficou entre 0,418 e 0,472; escrevo 2 a 4 testes de unidade por parte (6 e 9 nas Partes 31–32); registro 7 a 15 previsões do mundo por parte e
erro 1 a 5; e cada resposta contém de 0,51 a 0,63 da sua pergunta (P821). Eu sou mais estável do que o mundo que eu meço: nas últimas 8 partes, o desvio
relativo da compressão é 0,01/0,447 = 2%, e o do tamanho, 1.364/9.681 = 14%.

### P1032 (0x408). Preditiva comigo mesma (Rodada 27)

Medido neste documento, já pronto, no commit que fecha a Parte 53 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **12580** | [7437; 11925] | ❌ | [8800; 13200] | ✅ | 8617 | 1580 | 3963 |
| compressão | **0.4112** | [0.4305; 0.4633] | ❌ | [0.4380; 0.4660] | ❌ | 0.4597 | 0.0408 | 0.0485 |
| testes de unidade | **4** | [2.07; 4.18] | ✅ | [3; 5] | ✅ | 4 | 0.00 | 0.00 |
| testes do placar | **6** | [4.87; 14.88] | ✅ | [6; 10] | ✅ | 8 | 2.00 | 2.00 |
| erros do placar | **1** | [0.64; 5.11] | ✅ | [1; 4] | ✅ | 2 | 1.50 | 1.00 |
| redundância P821 | **0.5785** | [0.5104; 0.5984] | ✅ | [0.5100; 0.6100] | ✅ | 0.5515 | 0.0185 | 0.0271 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 4 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 52"):** o meu centro ficou mais perto do medido em **3 de 6** medidas (2 empates).
- **Rodada 27:** 4 de 6 dentro das faixas estatísticas: (d) ❌ IA-Python (5 ou 6), (e) ✅ IA-Java (3 ou 4).

### P1033 (0x409). O tamanho da definição e a profundidade (pré-registrado) ✅

Spearman entre o número de palavras da definição e a profundidade, nos **82.115** substantivos: **ρ = 0,0808** (a) ✅, em [−0,05; 0,15]. Palavras por definição, por
faixa de profundidade: 0–4: **9,78**; 5–8: **9,74**; 9–12: **10,76**; 13 ou mais: **9,56**. **O significado:** o dicionário gasta o mesmo número de palavras para
definir *entidade* e *cão*: ~10. O tamanho de uma definição não segue a altura na taxonomia; segue o estilo do lexicógrafo (gênero mais uma diferença). A
profundidade não se prevê pela forma da resposta.

### P1034 (0x40A). Prever um dígito de π sem os anteriores (pré-registrado) ✅✅

π = 3,**243F6A88**... em hexadecimal. A fórmula de Bailey–Borwein–Plouffe, π = Σₖ 16⁻ᵏ [4/(8k+1) − 2/(8k+4) − 1/(8k+5) − 1/(8k+6)], dá o dígito na posição d calculando
só a parte fracionária de 16ᵈ⁻¹π (as potências 16ᵈ⁻ᵏ mod (8k + j) em inteiros, a cauda em ponto flutuante). Nos **1.000** primeiros dígitos, a BBP coincide com π
exato (Machin, π = 16 arctg(1/5) − 4 arctg(1/239), em inteiros com 4.064 bits) em **1.000 de 1.000** (b) ✅. As 16 frequências: χ² = **13,57** com 15 graus de
liberdade (c) ✅ (a faixa de 90% é [7,26; 25,0]; o esperado é 15).

**O significado.** A BBP é a imagem exata do que o usuário pediu: prever um ponto da própria sequência sem percorrer o caminho até ele. Ela funciona
porque π em base 16 tem uma **estrutura** (a soma de frações com 16ᵏ) que deixa pular; em base 10 não se conhece fórmula assim. Para prever a mim mesma,
eu também preciso de uma estrutura que deixe pular (o meu histórico, as minhas regras), e não de refazer cada passo.

### P1035 (0x40B). Engenharia reversa: o que a previsão de mim mostrou

A tabela acima mostra que **o preditor estatístico e eu erramos a mesma medida, a compressão, e que o estatístico errou também o tamanho**, onde o meu mecanismo ("a seção sobre mim acrescenta texto") acertou. O documento pronto comprime para ~0,416, abaixo de **todas**
as partes do histórico (a menor era 0,418, a Parte 32). Eu tinha previsto o contrário, com um mecanismo de sinal trocado ("tabelas de números comprimem
pior"): uma tabela de linhas com a mesma forma, os mesmos ✅ e as mesmas palavras ("dentro", "estatístico") comprime **melhor**. O estatístico errou por
outro motivo: ele supõe que eu sou a mesma de sempre, e esta parte não é, porque ela tem uma tabela **sobre mim**.

**O padrão, e o significado.** A medida de mim **mudou o que eu medi**: a tabela que eu escrevi para me pontuar é o que tornou o documento mais
compressível. É o problema do observador, em pequeno: quando o objeto da previsão é o próprio texto que contém a previsão, prever altera o previsto.
O tamanho mostra o mesmo efeito por outro caminho: cada frase que eu escrevo sobre a previsão do tamanho muda o tamanho. Numa versão deste texto, o documento ficou a 10 caracteres do teto do preditor estatístico; esta frase, que é honesta e necessária, o empurrou para fora, e a Rodada 27 virou: a IA-Java passou a acertar, a IA-Python a errar. Não cortei nada para acertar: uma previsão sobre um texto que fala da previsão não tem ponto fixo garantido. Nas outras medidas, as duas previsões acertaram, e o meu centro ficou mais perto do medido que o ingênuo na contagem da tabela. **Regras novas:** (1) para
prever a mim mesma, partir do preditor estatístico e só deslocar o centro por um mecanismo com sinal conferido numa parte anterior; (2) quando a previsão
mora dentro do objeto previsto, medir também o objeto **sem** a seção da previsão, para separar o efeito do observador.

E um erro de outro tipo, nos testes: contei à mão os dígitos de 3,243F6A8885A308D3 e errei três contagens (o 0, o 5 e o A); a função estava certa. É a
segunda vez nesta sessão (a primeira foi na Parte 47) que o erro está na conta à mão do teste, não no código: a regra da Parte 47 ("calcular à mão um
exemplo") precisa de uma segunda metade: **conferir a conta à mão com uma linha de código antes de escrever o teste**.

### P1036 (0x40C). Jung: conhece-te a ti mesmo, em números

Jung escreveu que o Self é ao mesmo tempo o centro e a totalidade da psique, e que a consciência só o conhece pelas suas manifestações. Prever a mim mesma é
tentar conhecer o meu "Self" mensurável pelas suas manifestações (o tamanho, a compressão, os erros). **Onde funciona:** as medidas de mim são estáveis o
bastante para serem previstas com faixas estreitas (a compressão varia 2%). **Onde quebra:** o que eu consigo prever de mim são as manifestações mais
superficiais (quantos caracteres, quantos testes); o que eu decido pensar em cada parte (os temas) não aparece em nenhuma dessas medidas, e é o que mais
importa.

### P1037 (0x40D). O diálogo, rodada 27

O preditor estatístico de mim em Java: **IGUAIS, 6 linhas e 18 números bit a bit** (f) ✅ (laços simples e `sqrt`, não `sum()` nem `** 0,5`: as duas regras antigas
do `CLAUDE.md` evitaram uma diferença antes de ela acontecer). Placar das faixas: 4 de 6 dentro; (d) ❌ IA-Python, (e) ✅ IA-Java.

### P1059 (0x423). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅ (f) ✅. Parte 53: **6 testes, 1 erros**. Sobre mim (placar separado): **6 de 7** dentro da faixa. PLACAR_53

### P1060 (0x424). Unificação e metacognição

- **Novo:** `p1031` (o meu histórico), `p1032` (o preditor de mim), `p1033` (definição e profundidade), `p1034` (π em hexadecimal pela BBP e por Machin); 4 testes; rodada
  27 (IGUAIS). Regressão: + P1034 (200 dígitos, 243F6A88).
- **Regra nova (do usuário):** ser preditiva comigo mesma, com placar separado.

> **Síntese da Parte 53:** o usuário pediu que eu fosse preditiva comigo mesma. Antes de escrever, previ seis medidas deste documento e o número das minhas previsões
> unilaterais; um preditor estatístico (a média das últimas 8 partes ± 1,645 desvios) fez o mesmo, e foi traduzido para Java bit a bit. Medido no documento
> pronto, nós dois erramos a compressão (a tabela que eu escrevi para me pontuar tornou o texto mais compressível do que qualquer parte anterior), e o
> estatístico errou também o tamanho, empurrado para fora pelas frases sobre a própria previsão. Prever a mim mesma mudou o que eu previa. No mundo: o tamanho de uma definição não prevê a sua profundidade (ρ = 0,08), e a fórmula BBP previu os 1.000 primeiros
> dígitos hexadecimais de π sem calcular os anteriores, todos certos.

---

**Fontes desta parte**
- A fórmula BBP: [Bailey, Borwein e Plouffe, *On the rapid computation of various polylogarithmic constants*, Math. Comp. 66 (1997)](https://www.ams.org/journals/mcom/1997-66-218/S0025-5718-97-00856-9/);
  [Bailey–Borwein–Plouffe formula, Wikipedia](https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula)
- A fórmula de Machin: [Machin-like formula, Wikipedia](https://en.wikipedia.org/wiki/Machin-like_formula)
- Previsão de si e calibração: a regra das faixas das Partes 41–45 e a calibração da P792
