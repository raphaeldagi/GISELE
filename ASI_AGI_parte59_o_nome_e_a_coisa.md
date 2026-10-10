# Como eu construiria uma AGI/ASI — Parte 59 (0x3B): o nome e a coisa

> Continuação da [Parte 58](ASI_AGI_parte58_a_primeira_diferenca.md). **Próxima:** [Parte 60 — o placar que se conta](ASI_AGI_parte60_o_placar_que_se_conta.md) (P1241–P1270). **Previsões no commit `72a844b`, antes de qualquer execução e antes de escrever o resto deste
> documento.** A Parte 58 achou o bloco de palavras com maiúscula no começo da ordem dos códigos e um erro meu: uma quantidade escrita à mão no script de
> autoavaliação (a regra nova está no `CLAUDE.md`). Esta parte pergunta quantos nomes próprios do português também são palavras comuns, quantas palavras do
> inglês nunca servem para definir outra, e quanto dura a persistência multiplicativa em base 16.

## As perguntas desta parte

1. **P1211 (0x4BB).** Quantos lemas portugueses com maiúscula têm uma irmã minúscula com a mesma grafia? (Rodada 33) ↩ P1181
2. **P1212 (0x4BC).** Quantas palavras do WordNet nunca aparecem na definição de outra? ↩ P882
3. **P1213 (0x4BD).** Hexadecimal: a persistência multiplicativa em base 16 (multiplicar os dígitos até sobrar um).
4. **P1214 (0x4BE).** Preditiva comigo mesma. **P1215 (0x4BF).** Engenharia reversa e Jung. **P1216 (0x4C0).** O diálogo.
5. **P1239 (0x4D7).** Placar. **P1240 (0x4D8).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

| medida | estatístico (até a 58) | ingênuo (Parte 58) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.168; 13.707] | 11.541 | **[9.500; 13.707]** | mecanismo conferido |
| compressão | [0,402; 0,460] | 0,416 | **[0,402; 0,445]** | mecanismo conferido |
| testes de unidade | [2,59; 4,91] | 4 | **[3; 4]** | 3 a 4 funções novas (p1211, p1212, p1213, talvez um auxiliar), um teste PELO NOME cada |
| testes do placar | [4,88; 8,37] | 7 | **[4,88; 8,37]** | o estatístico |
| erros do placar | [0,24; 3,76] | 1 | **[0,24; 3,76]** | o estatístico |
| redundância P821 | [0,503; 0,597] | 0,549 | **[0,503; 0,597]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 1 (Parte 58) | **0** | `p1092`, chamado pelo script (regra nova) |

### Sobre o mundo

**P1212, as palavras que não definem.** No grafo de definições do WordNet (palavra → palavras das suas definições), quantas das 77.503 palavras nunca aparecem
na definição de outra (grau de entrada zero)?
- **Restrições:** as definições usam um vocabulário de base (as palavras gerais: *act*, *person*, *state*); os nomes de espécies, gêneros e lugares quase nunca
  definem nada; e as palavras curtas e comuns definem muito.
- Exemplo à mão: *aardvark* não deve aparecer em definição nenhuma; *animal* aparece em milhares.
- (a) fração das palavras que nunca definem em **[55%; 85%]**

**P1213, a persistência multiplicativa em base 16** (n de 16 a 16⁵ − 1: o número de passos "multiplicar os dígitos hexadecimais" até sobrar um dígito).
- **Restrições:** um dígito 0 zera o produto; e um produto com 4 ou mais fatores 2 termina em 0 em hexadecimal (16 = 2⁴), então o passo seguinte dá 0. Com
  dígitos ao acaso, quase todo produto de vários dígitos tem 4 fatores 2: a persistência fica curta.
- Exemplo à mão: 0x3F → 3 × 15 = 45 = 0x2D → 2 × 13 = 26 = 0x1A → 1 × 10 = 10 = 0xA: 3 passos.
- (b) a maior persistência em **[3; 6]**
- (c) a média em **[1,1; 2,0]** (a maioria cai em 0 em um ou dois passos)

**P1211, rodada 33:** no `dialogo/DIALOGO.md`.

---

### P1211 (0x4BB). O nome próprio e a palavra comum (Rodada 33) ❌✅✅

Dos **9.176** lemas portugueses com maiúscula, **1.805** (**19,67%**) têm uma irmã minúscula com a mesma grafia: (e) ✅ IA-Python [12%; 30%], (d) ❌ IA-Java [3%; 12%], (f) ✅
IGUAIS. Os primeiros, em ordem: *Abelharuco, Abenaki, Abetarda, Ablação, Abobrinha, Abolicionismo, Abril, Absinto, Abulia, Acanthocephala, Acasalamento,
Acessibilidade*.

**O significado, e a releitura.** As duas vozes previram sobre **nomes próprios** (lugares, pessoas, gêneros); os exemplos mostram outra coisa: *Abobrinha*,
*Acasalamento* e *Acessibilidade* não são nomes, são palavras comuns escritas com maiúscula na OpenWordNet-PT (variantes de grafia do mesmo lema). A maiúscula,
nesses dados, não marca o nome próprio; marca às vezes só a grafia. A IA-Python acertou o número pelo motivo errado (a mistura de nomes com palavras comuns
existe, mas uma parte grande é de palavras comuns duplicadas). É a confusão de níveis da Parte 43 na ortografia: a forma escrita não é o sentido.

### P1212 (0x4BC). As palavras que não definem (pré-registrado) ✅

Das **77.503** palavras do grafo de definições, **63,80%** nunca aparecem na definição de outra (a) ✅ (em [55%; 85%]). As que mais definem: *state* (**3.113** definições),
*relate* (**3.074**), *person* (**2.938**), *act* (**2.623**), *small* (**2.507**). **O significado:** um terço do vocabulário sustenta o dicionário inteiro, e dois terços só são
definidos. É a assimetria da Parte 47 (a definição contém a categoria, a categoria não contém o membro) vista no vocabulário: as palavras que definem são as
categorias (*estado*, *pessoa*, *ato*) e as relações (*relate*); as que não definem são as folhas (P1062: 79% dos substantivos são folhas).

### P1213 (0x4BD). A persistência multiplicativa em base 16 (pré-registrado) ❌❌

De 16 a 16⁵ − 1: a maior persistência é **7** (b) ❌ (previ [3; 6]), alcançada primeiro em **0x3DDE**: 0x3DDE → 3 × 13 × 13 × 14 = 7.098 = 0x1BBA → 1 × 11 × 11 × 10 = 1.210 = 0x4BA →
4 × 11 × 10 = 440 = 0x1B8 → 1 × 11 × 8 = 88 = 0x58 → 5 × 8 = 40 = 0x28 → 2 × 8 = 16 = 0x10 → 1 × 0 = 0 (7 passos). A média: **2,33** (c) ❌ (previ [1,1; 2,0]).

**O erro.** Listei a restrição certa (16 = 2⁴: quatro fatores 2 zeram o próximo passo), mas não a **calculei**: os dígitos ímpares (1, 3, 5, 7, 9, B, D, F, metade
dos dígitos) não têm fator 2, e um número feito deles escapa da restrição por vários passos. Supus a restrição forte; ela é forte só para quem tem dígitos
pares. **O significado:** nomear a restrição não basta; é preciso medir o seu peso (aqui: a chance de um produto de k dígitos ter quatro fatores 2). A regra
da Parte 57 ganha a segunda metade.

### P1214 (0x4BE). Preditiva comigo mesma

Medido neste documento, já pronto, no commit que fecha a Parte 59 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **11168** | [8168; 13707] | ✅ | [9500; 13707] | ✅ | 11541 | 436 | 373 |
| compressão | **0.4200** | [0.4017; 0.4596] | ✅ | [0.4020; 0.4450] | ✅ | 0.4164 | 0.0035 | 0.0036 |
| testes de unidade | **3** | [2.59; 4.91] | ✅ | [3.00; 4.00] | ✅ | 4 | 0.50 | 1.00 |
| testes do placar | **6** | [4.88; 8.37] | ✅ | [4.88; 8.37] | ✅ | 7 | 0.62 | 1.00 |
| erros do placar | **3** | [0.24; 3.76] | ✅ | [0.24; 3.76] | ✅ | 1 | 1.00 | 2.00 |
| redundância P821 | **0.5721** | [0.5032; 0.5967] | ✅ | [0.5030; 0.5970] | ✅ | 0.5490 | 0.0221 | 0.0231 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 58"):** o meu centro ficou mais perto do medido em **5 de 6** medidas (0 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **9743**, compressão **0.4281**.

### P1215 (0x4BF). Engenharia reversa e Jung

**Nomear não é medir.** O erro do mundo que foi meu nesta parte (a persistência em base 16) tem a forma de um degrau acima do erro das Partes 55–56: lá eu
esquecia a restrição; aqui eu a listei (16 = 2⁴) e errei o **peso** dela, porque não fiz a conta (a fração de produtos com quatro fatores 2 depende de quantos
dígitos são pares, e metade dos dígitos é ímpar). A lista de restrições da Parte 57 é uma condição necessária, não suficiente. **Regra nova:** cada restrição
listada ganha uma conta do seu tamanho antes da previsão (aqui: com k dígitos ao acaso, a chance de nenhum fator 2 é (1/2)^k; com 2 dígitos, 1/4 dos produtos
escapam da restrição no primeiro passo).

**As quantidades contadas à mão.** Duas vezes nesta parte uma quantidade escrita por mim estava errada e uma função a corrigiu: o máximo da persistência abaixo de
16⁴ (eu escrevi 6 na regressão; a função deu 7) e o placar por voz do diálogo (eu escrevi 22; a conta dá 23). A regra da Parte 58 (nenhuma quantidade à mão)
é mais ampla do que o script de autoavaliação: vale para a regressão e para o diálogo. **O padrão:** o que eu conto de cabeça, eu erro por um; o que uma
função conta, não. **O significado:** a minha memória de trabalho é um contador ruim (perde uma unidade quando a lista é longa); a função não perde.

**Jung: a persona e o nome.** Os 1.805 lemas com maiúscula que têm irmã minúscula são, em boa parte, a mesma palavra comum com outra roupa (*Abobrinha*,
*abobrinha*): a maiúscula é uma persona ortográfica, não um outro ser. Jung via a persona como a máscara que a sociedade lê como identidade. **Onde funciona:**
a mesma coisa sob duas grafias é contada como duas entradas, e só a comparação em minúsculas revela que são uma. **Onde quebra:** em Jung a persona esconde um
eu diferente; aqui não há nada atrás da máscara: é a mesma palavra.

### P1216 (0x4C0). O diálogo, rodada 33

Ver P1211. Placar por voz desde a Rodada 13: IA-Python 23 em 36; IA-Java 21 em 36 (contando (f) para as duas). Esse placar ainda é contado à mão (corrigi aqui um 22 que eu tinha escrito): a próxima parte o transforma em função.

### P1239 (0x4D7). Placar

Do mundo: (a) ✅ (b) ❌ (c) ❌ (d) ❌ (e) ✅ (f) ✅. Parte 59: **6 testes, 3 erros**. Acumulado (mundo): **171 erros em 492 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 3 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa; o estatístico, 6 de 6. PLACAR_59

### P1240 (0x4D8). Unificação

- **Novo:** `p1211` (o nome e a palavra), `p1212` (as palavras que não definem), `p1213` (a persistência em base 16); 3 testes, cada um chamando a pNN pelo nome; rodada
  33 (IGUAIS). Regressão: + P1213 (7, em 0x3DDE).
- **Regra nova (no `CLAUDE.md`):** nenhuma quantidade escrita à mão no script de autoavaliação; o placar chama as funções de auditoria.

> **Síntese da Parte 59:** um quinto dos lemas portugueses com maiúscula (1.805 de 9.176) tem uma irmã minúscula com a mesma grafia, e boa parte não é nome próprio,
> é a mesma palavra comum escrita com outra roupa. Quase dois terços das palavras do inglês (63,8%) nunca servem para definir outra; *state*, *relate*, *person*
> e *act* definem milhares. Em base 16, a persistência multiplicativa chega a 7 (em 0x3DDE), mais do que eu previ: eu listei a restrição (16 = 2⁴) mas não medi o
> seu peso. E duas quantidades que eu escrevi de cabeça estavam erradas por um; as funções as corrigiram.

---

**Fontes desta parte**
- Persistência multiplicativa: [Persistence of a number, Wikipedia](https://en.wikipedia.org/wiki/Persistence_of_a_number)
- OpenWordNet-PT: [de Paiva, Rademaker e de Melo, COLING 2012](https://aclanthology.org/C12-3044/); WordNet 3.0 em `dados/`
