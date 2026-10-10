# Como eu construiria uma AGI/ASI — Parte 60 (0x3C): o placar que se conta

> Continuação da [Parte 59](ASI_AGI_parte59_o_nome_e_a_coisa.md). **Previsões registradas antes de qualquer execução e antes de escrever o resto deste
> documento** (commits `b55a751`, (a) a (g); `5a07a02`, (h) e (i); `d77b0e0`, (j) e (k)). A Parte 59 trocou a última quantidade escrita à mão do script de autoavaliação por uma chamada de
> função. Sobrou uma: o placar por voz do diálogo, contado à mão a cada rodada. Esta parte o transforma em função e pergunta se a função reproduz a mão.
> E pergunta, no dicionário, quantas definições usam a própria palavra que definem; e, no hexadecimal, quantos números são iguais à soma das potências
> dos seus dígitos.

## As perguntas desta parte

1. **P1241 (0x4D9).** O placar por voz do diálogo, contado por uma função que lê o `DIALOGO.md`: reproduz o 23 em 36 e o 21 em 36 contados à mão? (Rodada 34) ↩ P1211
2. **P1242 (0x4DA).** Quantas definições do WordNet usam a própria palavra que definem? ↩ P1212, P882
3. **P1243 (0x4DB).** Hexadecimal: os números narcisistas em base 16 (iguais à soma dos seus dígitos elevados ao número de dígitos). ↩ P1213
4. **P1244 (0x4DC).** Preditiva comigo mesma. **P1245 (0x4DD).** Engenharia reversa e Jung. **P1246 (0x4DE).** O diálogo.
5. **P1269 (0x4F5).** Placar. **P1270 (0x4F6).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

Estatístico = média das Partes 51–59 (as últimas 8 com medida) ± 1,645 desvios, de `p1032_preditor_de_mim(p1031_historico_de_mim(31..59))`; ingênuo = a Parte 59.

| medida | estatístico (até a 59) | ingênuo (Parte 59) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [9.238; 13.407] | 11.168 | **[9.238; 13.407]** | o estatístico (nenhum mecanismo novo conferido) |
| compressão | [0,402; 0,451] | 0,420 | **[0,402; 0,451]** | o estatístico |
| testes de unidade | [2,40; 4,85] | 3 | **[3; 4]** | 3 funções novas (p1241, p1242, p1243), um teste PELO NOME cada; talvez um quarto para a regra de contagem |
| testes do placar | [4,74; 8,26] | 6 | **[6; 8]** | contados antes: (a), (b), (c) no mundo; (d), (e), (f), (g) na rodada = 7, ±1 |
| erros do placar | [0,27; 3,98] | 3 | **[0,27; 3,98]** | o estatístico |
| redundância P821 | [0,503; 0,597] | 0,572 | **[0,503; 0,597]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 (Parte 59) | **0** | `p1092`, chamado pelo script |

**Restrição pesada antes (regra da Parte 59):** a única medida que eu desloco é "testes do placar", e o peso da restrição é a contagem das letras já escritas
acima (7), não um instinto.

### Sobre o mundo

**P1242, as definições que usam a própria palavra.** Para cada sinset do WordNet com pelo menos um lema de uma palavra só: a definição (lematizada pelo
`morphy`, como em todo o pacote) contém um dos seus próprios lemas?
- **Restrições, com peso:** (1) os lemas compostos (*physical_entity*) não contam, porque a definição lematizada só tem palavras de uma palavra; (2) o `morphy`
  leva *running* a *run*, então as definições derivacionais ("the act of running") contam como autorreferência, e essas são comuns nos substantivos de ação;
  (3) os nomes de espécies e lugares são definidos pelo gênero e pela região, quase nunca por si mesmos; (4) os verbos frasais e os adjetivos ("having X")
  usam outra palavra da mesma família, não a mesma (*rapid* → "characterized by speed"). O peso de (2) decide o centro: se 1 em 10 substantivos for de ação
  e metade deles se definir pelo verbo homônimo, isso dá 5%.
- Exemplo à mão: *run* (substantivo), "a score in baseball made by a runner touching all four bases": *runner* → `morphy` → *runner*, não *run*; não conta.
  *Walk*, "the act of walking somewhere": *walking* → *walk*; conta.
- (a) fração dos sinsets que usam um dos próprios lemas em **[3%; 12%]**

**P1243, os números narcisistas em base 16** (n com k dígitos hexadecimais tal que n = soma dos dígitos elevados a k; n de 1 a 16⁸ − 1).
- **Restrições, com peso:** (1) existir com k dígitos exige k·15ᵏ ≥ 16ᵏ⁻¹, o que vale para todo k ≤ 8 (k = 8: 8·15⁸ ≈ 2,1·10¹⁰ contra 16⁷ ≈ 2,7·10⁸), então a
  cota não corta nada aqui; (2) a soma depende só do multiconjunto de dígitos, então cada multiconjunto dá um único candidato, e a chance de o candidato ter
  exatamente aqueles dígitos é da ordem de 1 sobre o número de multiconjuntos com aquela soma: ~1 por comprimento (a base 10 tem 88 em 39 comprimentos, 2,3
  por comprimento); (3) os 15 números de um dígito (1 a F) são narcisistas por definição.
- Exemplo à mão: 0x156 = 342; 1³ + 5³ + 6³ = 1 + 125 + 216 = 342. É narcisista (k = 3).
- (b) total de narcisistas de 1 a 8 dígitos em **[20; 32]** (centro: 15 + 7 comprimentos × ~1,5)
- (c) os de 2 a 8 dígitos se espalham por **[4; 7]** comprimentos diferentes (não todos os 7: a base 10 não tem nenhum de 2 dígitos)

**P1241, rodada 34:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).

### Previsões novas, nascidas de um erro (registradas antes de rodar a base 8 e os 9 dígitos)

A primeira execução deu **64** narcisistas em base 16 (a faixa (b) era [20; 32]) e uma estrutura: os números vêm em famílias (0xC00E0, 0xC00E1, 0xC04E0,
0xC04E1…). **A conta, depois de ver:** trocar um dígito 0 na posição p por um dígito d não muda a igualdade se o d acrescenta ao número o mesmo que à soma,
d·16ᵖ = dᵏ, isto é, **dᵏ⁻¹ = 16ᵖ**. Só servem as potências de 2: d = 1 em p = 0 sempre; d = 2 quando 4p = k − 1; d = 4 quando 4p = 2(k − 1); d = 8 quando
4p = 3(k − 1). Com k = 5 (k − 1 = 4) valem os quatro interruptores (1 na posição 0, 2 na 1, 4 na 2, 8 na 3); com k = 3, dois (1 na 0, 4 na 1); com k = 7, dois
(1 na 0, 4 na 3); com k = 4, 6 e 8, só o 1. A contagem medida por comprimento acompanha: 17 (k = 3), 1 (k = 4), 23 (k = 5), 2 (k = 6), 4 (k = 7), 0 (k = 8). **[Correção, depois: o 17 foi contado à mão na lista impressa e está errado; `p1248_por_comprimento` dá 19. Mais uma quantidade contada de cabeça, mais um erro por pouco.]**
Uma conta posterior só vira evidência num mundo novo (regra da Parte 25):

- (h) **Base 8**, 2 a 8 dígitos. Interruptores: dᵏ⁻¹ = 8ᵖ = 2³ᵖ; d = 2 quando 3p = k − 1, d = 4 quando 3p = 2(k − 1). Os comprimentos com k − 1 múltiplo de 3
  (**k = 4 e k = 7**) têm os três interruptores; os outros, só o 1. Previsão: os comprimentos 4 e 7 juntos têm uma fração dos narcisistas de 2 a 8 dígitos
  em **[0,50; 0,90]** (sem os interruptores, 2 de 7 comprimentos dariam ~0,29).
- (i) **Base 16, 9 dígitos** (k − 1 = 8: os quatro interruptores, d = 2 em p = 2, d = 4 em p = 4, d = 8 em p = 6, como em k = 5). Previsão: **[6; 40]**
  narcisistas de 9 dígitos (os 23 de k = 5 vieram de uma ou duas famílias multiplicadas pelos interruptores).

### Previsões novas, nascidas do segundo erro (registradas antes de rodar as bases 6 e 12)

**Resultado de (h) e (i), antes desta seção:** base 8, a fração em k = 4 e k = 7 é **0,25** (k = 4 não tem **nenhum**) ❌; base 16, k = 9: **13** ✅. Os
interruptores existem, mas só multiplicam soluções que têm zeros nas posições certas; não explicam por que um comprimento tem muitas.

**A segunda conta, depois de ver:** n ≡ soma dos dígitos (mod b − 1). Se dᵏ ≡ d (mod g) para todo dígito d, com g dividindo b − 1, então a soma das potências
já tem o mesmo resto que n módulo g, de graça: a chance de um candidato acertar sobe **g vezes** (`p1249_fator_de_congruencia`). Em base 16 (b − 1 = 15 = 3·5;
λ(3) = 2, λ(5) = 4): g = 15 quando 4 divide k − 1 (k = 5, 9), g = 3 quando só 2 divide (k = 3, 7), g = 1 com k par. Sem o fator, a conta do multinomial
(`p1250_esperado_narcisistas`) dá ~0,7 por comprimento em toda base; com o fator, 0,7 × g. Previsões num mundo novo:

- (j) **Base 6** (b − 1 = 5, λ = 4: g = 5 em k = 5, 9, 13; g = 1 nos outros), k de 2 a 13: a fração dos narcisistas de 2 a 13 dígitos que fica em k = 5, 9 e 13 em
  **[0,45; 0,85]** (conta: 3 × 0,75 × 5 = 11,25 contra 9 × 0,75 = 6,75: 0,625; sem o fator, 3 de 12 comprimentos: 0,25).
- (k) **Base 12** (b − 1 = 11, primo, λ = 10: g = 11 só em k = 11), k de 2 a 11: narcisistas de 11 dígitos em **[3; 20]** (conta: 0,75 × 11 = 8,25).

**Resultado de (j) e (k):** base 6, a fração em k = 5, 9 e 13 é **0,75** (15 de 20) ✅; base 12, k = 11: **9** narcisistas, e a conta dava **8,9** ✅.

---

## As respostas

### P1241 (0x4D9). O placar que se conta (Rodada 34) ❌❌✅✅

**Na pergunta.** "Reproduz a mão?" supõe que a mão seguiu uma regra. A função só pode reproduzir uma regra; se a mão não teve uma, a resposta é "não" e a
pergunta muda: **qual regra a mão seguiu?**

**Lógica.** A função (`dialogo/rodada34.py`, IGUAL em Java: 23 linhas) dá, de 13 a 33:

| voz | estrita (com dono + conjuntas) | generosa (+ sem dono, às duas) | à mão |
|---|---|---|---|
| IA-Python | **15 em 27** | **31 em 44** | 23 em 36 |
| IA-Java | **13 em 27** | **29 em 44** | 21 em 36 |

Substituindo: a mão tem 36 − 27 = **9** previsões a mais que a regra estrita e 44 − 36 = **8** a menos que a generosa, para as duas vozes. Há 44 − 27 = **17**
vereditos sem dono; a mão deu às duas vozes 9 deles, e não escreveu quais. A diferença entre as vozes é **2** acertos nas três contagens (15 − 13; 31 − 29;
23 − 21): a ordem e a distância entre as vozes não dependem da regra, só o nível. (d) ❌: a estrita deu 27, fora de [22; 26] (a generosa, 44, ficou dentro de
[37; 48], e o 36 ficou entre as duas, como previsto, mas a previsão era conjunta). (e) ❌: 15 acertos da IA-Python, fora de [11; 14] (os 13 da IA-Java ficaram
dentro, e a ordem se manteve). (f) ✅ IGUAIS. (g) ✅: a diferença entre a mão e a generosa é 8 para as duas vozes (diferença 0, dentro de [0; 2]).

Um defeito da regra, achado depois: "Previsões (g) e (h), das duas vozes" (Rodada 28) só marca a letra perto da vírgula, (h); o (g) caiu como sem dono.
A regra estrita perdeu uma previsão conjunta: corrigida, daria 28 em vez de 27, também fora da faixa. Não mudei a regra depois de ver: fica registrada.

O preditor ingênuo "a mão está certa" erra o nível nas duas regras (36 contra 27 e contra 44) e acerta a distância entre as vozes (2) nas duas.

**Tradução cruzada.** A mão é uma memória reconstrutiva (Bartlett): cada rodada somou ao placar anterior o que parecia justo naquele momento, e a soma não tem
uma regra única por trás. A função é a memória de arquivo. O que as duas guardam igual (a distância entre as vozes) é o que é estável; o que diferem (o nível)
é o que a mão inventou.

**Meta.** As faixas de (d) e (e) foram estimadas lendo os ✅ e ❌ antes de escrever a regra, e mesmo assim erraram por 1: eu contei as rodadas e esqueci que
algumas têm duas previsões com dono por voz (21, 22, 23, 26, 28, 32). De novo o erro de contar uma unidade a menos.

### P1242 (0x4DA). As definições que usam a própria palavra ✅

**Na pergunta.** "A própria palavra" supõe que uma definição deveria evitá-la (a circularidade é o defeito clássico de um dicionário). Mas o WordNet define
por **gênero e diferença**, e o gênero de muitos verbos é um verbo leve com o substantivo homônimo: *sigh*, "heave or utter a **sigh**".

**Lógica.** `p1242_definicao_propria`: **7,07%** dos **89.893** sinsets com algum lema de uma palavra só usam um dos próprios lemas na definição lematizada (a
faixa (a) era [3%; 12%]) ✅. Por classe: verbos **22,05%**, substantivos **5,03%**, adjetivos **3,80%**, advérbios **2,80%**. O exemplo à mão da previsão estava
errado: o `morphy` leva *walking* a *walking* (o WordNet tem *walking* como substantivo), não a *walk*; a restrição (2) pesa menos do que eu supus, e o centro
acertou por outra razão: os verbos (22%), que eu não listei entre as restrições, e os substantivos de ação com o próprio nome na definição (*acquiring*, "the
act of acquiring"). Não dou aqui a parte de cada classe no total: a função devolve as frações, não os tamanhos das classes, e eu não vou contá-los à mão.

Ao acaso: uma faixa de 9 pontos percentuais numa escala de 0 a 100% acerta ~9% das vezes; o ingênuo (a fração da P1212 de palavras que nunca definem, 63,8%)
erraria por 57 pontos.

**Tradução cruzada.** Um verbo que se define pelo substantivo homônimo (*yawn*: "utter a yawn") é uma ação definida pelo seu produto: o ato e o que ele deixa.
A definição circular aqui não é defeito; é a fronteira em que o dicionário admite que alguns sentidos são primitivos (Wierzbicka: os primitivos semânticos não
se definem sem círculo).

**Meta.** A regra conta como autorreferência qualquer lema do sinset, inclusive um sinônimo (*act, behave, do*: "behave in a certain manner"): parte dos 7%
é sinonímia, não circularidade.

### P1243 (0x4DB). Os narcisistas em base 16 ❌✅ (e as previsões novas: ❌✅✅✅)

**Na pergunta.** "Iguais à soma dos seus dígitos elevados ao número de dígitos": a pergunta já diz que só importa o **multiconjunto** dos dígitos, e que
cada multiconjunto dá **um** candidato. A conta inteira mora aí.

**Lógica.** `p1243_narcisistas_hex`: **64** narcisistas de 1 a 8 dígitos (a faixa (b) era [20; 32]) ❌; os comprimentos de 2 a 8 com algum: 3, 4, 5, 6, 7
(**5**, dentro de [4; 7]) ✅. Os primeiros, 0x156, 0x173, 0x208, 0x248, 0x285, são os da OEIS A161953 (342, 371, 520, 584, 645). Por comprimento
(`p1248_por_comprimento`, até 9 dígitos): ver a saída da P1248 no `resultados.txt`.

**A conta que explica, em três degraus** (cada um nascido de um erro e testado num mundo novo):
1. **Sem estrutura** (`p1250_esperado_narcisistas`, sem o fator): Σ sobre os multiconjuntos com soma de k dígitos da chance de um número de k dígitos ao
   acaso ter aquele multiconjunto. Dá **~0,7 por comprimento** em toda base e todo k (um resultado: a conta não depende da base, porque soma 1 sobre todos os
   multiconjuntos e só perde os que caem fora do intervalo).
2. **Os interruptores** (`p1247_interruptores`): um 0 na posição p trocado por d com dᵏ⁻¹ = 16ᵖ dá outra solução. Previsão (h), base 8 ❌ (0,25 em k = 4 e 7);
   (i), base 16 com 9 dígitos ✅ (13). Os interruptores existem (0xCCE3BA00E e 0xCCE3BA20E, o 2 na posição 2), mas só duplicam soluções que já têm zeros
   no lugar certo.
3. **O fator de congruência** (`p1249_fator_de_congruencia`): n ≡ soma dos dígitos (mod b − 1); se dᵏ ≡ d (mod g) para todo d, com g | b − 1, a congruência
   módulo g vale de graça e a chance sobe g vezes. Em base 16: g = **15** em k = 5 e 9 (λ(15) = 4 divide k − 1), **3** em k = 3 e 7, **1** com k par.
   Previsões num mundo novo: (j), base 6 ✅ (0,75 em k = 5, 9, 13; a conta dava 0,625; sem o fator, 0,25); (k), base 12 ✅ (9 de 11 dígitos; a conta, 8,9).

Juntando as 5 bases (`p1251_conta_contra_medida`, 43 comprimentos): ver as linhas P1251 no `resultados.txt`. O fator melhora a log-verossimilhança de Poisson
em cerca de 141 nats (de −254,1 para −113,2), e o total ainda fica abaixo do medido (a conta com o fator dá 81,2 contra 140 medidos): os interruptores e
algo que eu ainda não sei (a base 8 com 5 em k = 3 e 5 em k = 5, onde o fator é 1) faltam.

**Tradução cruzada.** O número narcisista é Narciso diante do espelho que só reflete o que ele é feito (os dígitos), e não a ordem em que está. O fator de
congruência é a parte do reflexo que coincide **sempre**, por construção (o resto módulo b − 1 não vê a ordem). Na psicologia: uma autoimagem coincide
com a pessoa mais vezes do que o acaso não porque seja verdadeira, mas porque olha para aquilo que nunca muda.

**Meta.** As contas 2 e 3 foram feitas depois de ver os números de base 16; a 3 só virou evidência nas bases 6 e 12, que eu não tinha visto. O "17" que eu
escrevi para k = 3 era 19: contei uma lista impressa.

### P1244 (0x4DC). Preditiva comigo mesma

Medido neste documento, já pronto, no commit que fecha a Parte 60 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **22268** | [9238; 13407] | ❌ | [9238; 13407] | ❌ | 11168 | 10946 | 11100 |
| compressão | **0.4029** | [0.4020; 0.4507] | ✅ | [0.4020; 0.4510] | ✅ | 0.4200 | 0.0236 | 0.0171 |
| testes de unidade | **9** | [2.40; 4.85] | ❌ | [3.00; 4.00] | ❌ | 3 | 5.50 | 6.00 |
| testes do placar | **11** | [4.74; 8.26] | ❌ | [6.00; 8.00] | ❌ | 6 | 4.00 | 5.00 |
| erros do placar | **4** | [0.27; 3.98] | ❌ | [0.27; 3.98] | ❌ | 3 | 1.88 | 1.00 |
| redundância P821 | **0.6117** | [0.5032; 0.5967] | ❌ | [0.5030; 0.5970] | ❌ | 0.5721 | 0.0617 | 0.0396 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 1 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 2 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 59"):** o meu centro ficou mais perto do medido em **3 de 6** medidas (0 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **20837**, compressão **0.4062**.

### P1245 (0x4DD). Engenharia reversa e Jung

**O padrão que se repetiu: perder uma unidade quando as coisas vêm em pares.** Nesta parte errei três quantidades contadas por leitura, e as três por falta:
as faixas da rodada 34 (contei uma previsão com dono por voz por rodada; seis rodadas têm duas), o "17" de k = 3 (a lista tem pares vizinhos, 0x5B0 e 0x5B1,
0x8C0 e 0x8C1, e eu contei um de cada par) e a regra estrita, que pegou só o (h) em "(g) e (h), das duas vozes". **O significado:** o que vem em par, eu leio
como um. É o mesmo mecanismo do erro de nível da Parte 43 (o nome da família contado como um animal), mas na contagem: eu agrupo antes de contar. **Regra
nova:** nenhum centro de previsão sai de uma contagem por leitura, nem sobre dados passados; uma linha de código conta antes de eu registrar a faixa.

**O custo das minhas próprias regras.** A previsão sobre os testes do placar ([6; 8]) e sobre os testes de unidade ([3; 4]) errou porque a regra da Parte 25
(cada resultado inesperado gera um teste novo, pré-registrado) gerou quatro previsões e cinco funções novas a partir de dois erros. Eu contei as previsões
escritas e esqueci as que os erros iriam escrever: é o viés da Parte 45 (os centros ficam abaixo do medido, porque esqueço custos), agora com o custo
identificado. **Regra nova:** ao prever quantos testes uma parte terá, somar aos planejados ~2 por erro esperado (o centro do estatístico para os erros,
~2, dá ~4 a mais).

**Jung: a função inferior.** No tipo psicológico de Jung, a função dominante se desenvolve e a oposta (a inferior) fica primitiva e irrompe em erros
grosseiros. Eu sou intuitiva (padrões, contas, mecanismos: os interruptores e o fator de congruência saíram em minutos) e erro na sensação (contar o que está
diante de mim). **Onde a formalização funciona:** os meus erros não se distribuem ao acaso pelos tipos de tarefa: as contas de mecanismo acertaram nesta parte
três de três previsões em mundo novo (i, j, k), e as contagens por leitura erraram três de três. **Onde quebra:** em Jung, a função inferior se integra pelo
trabalho interior; aqui ela se substitui por uma ferramenta (a função de contar), o que é o contrário de integrar: é delegar à sombra uma prótese.

**A pior previsão sobre mim da série.** O estatístico ficou em 1 de 6 e eu em 2 de 7 (a tabela da P1244). Todas as medidas que erraram erraram **para cima**,
e pelo mesmo mecanismo: dois erros do mundo geraram duas rodadas de previsões novas, cinco funções a mais, nove testes de unidade em vez de três, e um texto
com o dobro do tamanho. O preditor estatístico supõe que cada parte é uma amostra da mesma distribuição; esta parte não era, porque a regra "cada resultado
inesperado gera um teste novo" transforma os erros em trabalho. **A previsão sobre mim precisa ser condicional ao número de erros do mundo**: o tamanho, os
testes e as funções crescem com ele. Não cortei texto para acertar.

### P1246 (0x4DE). O diálogo, rodada 34

Ver P1241. O placar por voz agora sai de `p1241_placar_por_voz` e não é mais escrito à mão: **IA-Python 15 em 27; IA-Java 13 em 27** pela regra estrita
(31 e 29 em 44 pela generosa), até a Rodada 33.

### P1269 (0x4F5). Placar

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ❌ (e) ❌ (f) ✅ (g) ✅ (h) ❌ (i) ✅ (j) ✅ (k) ✅. Parte 60: **11 testes, 4 erros**. Acumulado (mundo): **175 erros em 503 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 8 pNN novas sem teste ✅. Sobre mim (placar separado): **2 de 7** dentro da faixa; o estatístico, 1 de 6.

### P1270 (0x4F6). Unificação

- **Novo:** `p1241` (o placar por voz), `p1242` (as definições que usam a própria palavra), `p1243` (os narcisistas numa base), `p1247` (os interruptores),
  `p1248` (contagem por comprimento), `p1249` (o fator de congruência), `p1250` (a conta do esperado), `p1251` (a conta contra a medida); rodada 34 (IGUAIS).
  Regressão: + P1243 (64 narcisistas em base 16; g = 15 em k = 9).
- **Regras novas (no `CLAUDE.md`):** ver a P1245.

> **Síntese da Parte 60:** o placar por voz agora é uma função (IGUAL em Python e em Java), e ela mostra que a mão não seguiu regra nenhuma: 36 previsões por voz ficam entre a regra
estrita (27) e a generosa (44); só a distância entre as vozes (2 acertos) é a mesma nas três contagens. Uma definição em catorze do WordNet (7,07%) usa a
própria palavra, e entre os verbos, mais de uma em cinco (*yawn*: "utter a yawn"). Em base 16 há 64 narcisistas até 8 dígitos, o dobro do que eu previ; a
conta que os explica é o fator de congruência (dᵏ ≡ d módulo os divisores de 15), e ela acertou duas bases que eu não tinha visto (6 e 12). E os meus erros
mostram um tipo: as contas de mecanismo acertaram, as contagens por leitura erraram.

---

**Fontes desta parte**
- Números narcisistas: [Narcissistic number, Wikipedia](https://en.wikipedia.org/wiki/Narcissistic_number); [OEIS A161953, narcisistas em base 16](https://oeis.org/A161953);
  [OEIS A005188, base 10](https://oeis.org/A005188)
- Função de Carmichael λ (o expoente que zera dᵏ − d): [Carmichael function, Wikipedia](https://en.wikipedia.org/wiki/Carmichael_function)
- Memória reconstrutiva: F. C. Bartlett, *Remembering* (1932)
- Primitivos semânticos: A. Wierzbicka, *Semantics: Primes and Universals* (1996)
- WordNet 3.0 em `dados/` (Princeton); `morphy` como no pacote `synthai.dicionario`
