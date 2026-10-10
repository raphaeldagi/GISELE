# Como eu construiria uma AGI/ASI — Parte 74 (0x4A): o que vale testar

> Continuação da [Parte 73](ASI_AGI_parte73_o_que_refuta.md). **Próxima:** [Parte 75 — o que se prova](ASI_AGI_parte75_o_que_se_prova.md) (P1691–P1720). Nasce do quarto texto recebido do usuário (`externos/texto_recebido_parte74.md`): os Módulos 004 a 007 de outra conversa, sem código,
> com resultados declarados ("8/8 testes"; "corrigi a expectativa: o histórico tinha quatro eventos, não cinco") e duas propostas para escolher o próximo experimento: U(a) = E[ΔK | a]/Custo(a)
> e o "ganho esperado de informação".

## Previsões sobre as minhas previsões desta parte (registradas antes de pensar qualquer faixa do mundo)

- **(m1)** o número de previsões do mundo em **[4; 9]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,03; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~5 previsões do mundo e ~4 funções novas. E = erros do mundo, S = surpresas, contados pelo script.

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[4 + S; 7 + S]** | 4 funções, uma por teste |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (registradas depois das (m) e das sobre mim, antes de medir)

**O ganho de informação (P1661).** No mundo da P1632 (semente 73), observar o estado reduz a entropia em H(p) bits, qualquer que seja a utilidade. Escolher pelo "ganho esperado de
informação" é escolher por H(p). **A conta:** H depende só de p, e p é independente da dominância; então os 200 de maior H têm VOI = 0 com chance 1/2 (desvio 0,0354).
- **(a)** a fração com VOI = 0 entre os 200 de maior ganho de informação em **[0,442; 0,558]**
- **Calibração (sementes 730 a 733, regra escrita antes: as quatro seguintes à 73 × 10):** a razão entre o VOI médio dos 200 de maior H e o dos 200 de maior VOI deu 0,277, 0,326, 0,290 e 0,283.
  A faixa de previsão de 90% para um lote novo é a média ± t₃ · desvio · √(1 + 1/4), com t₃ = 2,353.
- **(b)** essa razão na semente 73 em **[0,236; 0,352]**

**O orçamento (P1662).** A U(a) = E[ΔK | a]/Custo(a) do texto: 300 instâncias, 30 experimentos cada, custos inteiros em 1..20, orçamento de 20% do custo total; valor = VOI. O ótimo é exato (mochila
0-1 por programação dinâmica). **Calibração (sementes 740 a 743, mesma geometria do teste):** guloso por VOI/custo = 0,9924, 0,9928, 0,9925, 0,9938 do ótimo; guloso por H/custo = 0,581, 0,555, 0,565,
0,561; o guloso por VOI foi ótimo em 0,627, 0,667, 0,657, 0,640 das instâncias. Faixas pela mesma regra (t₃ = 2,353). Teste: semente 74.
- **(c)** guloso por VOI/custo, em fração do ótimo, em **[0,9912; 0,9946]**
- **(d)** guloso por ganho de informação/custo, em fração do ótimo (em VOI), em **[0,5364; 0,5943]**
- **(e)** a fração de instâncias em que o guloso por VOI é ótimo em **[0,6009; 0,6941]**

**Medido (a) a (e):** (a) **0,510** ✅; (b) **0,251** ✅ (0,0426/0,1696); (c) **0,9922** ✅; (d) **0,568** ✅; (e) **0,573** ❌ (0,028 abaixo do piso; não é surpresa).

**Previsão nova, nascida de (e), registrada antes de rodar.** A faixa de (e) usou o desvio de 4 lotes de calibração (0,0177), e uma fração em 300 instâncias tem um desvio binomial conhecido,
√(p(1 − p)/300) ≈ 0,028: havia uma conta melhor que a estimativa de 4 amostras. Com os 5 lotes (os 4 de calibração e o do teste), p = 0,6327, desvio 0,0278, e a faixa de 90% para um lote novo
é p ± 1,645 · 0,0278 · √(1 + 1/5).
- **(f)** a fração de instâncias em que o guloso por VOI é ótimo, semente 75, em **[0,5825; 0,6828]**

**Medido (f):** **0,620** ✅ (e (c), (d) replicaram: 0,9924 e 0,568).

**A Rodada 48, registrada antes de rodar:** o Python grava as 300 instâncias da semente 74 (valores em hexadecimal, custos inteiros); Java e Python calculam o ótimo da mochila por programação
dinâmica e os dois gulosos (ordenação por razão, empates pelo índice). Só + e comparações sobre os valores, e divisões para as razões: tudo arredondado corretamente pelo IEEE 754.
- **(g)** IGUAIS (categórica)

## As perguntas desta parte

1. **P1661 (0x67D).** O "ganho esperado de informação" escolhe as perguntas que valem? ↩ P1632
2. **P1662–P1663 (0x67E–0x67F).** A U(a) = E[ΔK | a]/Custo(a) com orçamento: quanto do ótimo ela alcança, e o que importa mais, a razão ou o ΔK? E o verificador em Java que o texto diz não
   ter implementado (Rodada 48). ↩ P1632
3. **P1664 (0x680).** "Corrigi a expectativa e confirmei o resultado": quando mudar um teste depois de vê-lo falhar é correção, e quando é apagar a evidência? ↩ a regra da Parte 22
4. **P1665 (0x681).** Preditiva comigo mesma. **P1666 (0x682).** Engenharia reversa e Jung. **P1689 (0x699).** Placar. **P1690 (0x69A).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 9] | **7.0000** | ✅ |
| (m2) | [0; 2] | **0.0000** | ✅ |
| (m3) | [0.03; 0.4] | **0.0756** | ✅ |
| (m4) | [0.45; 1.0] | **0.8571** | ✅ |
| (m5) | [0; 2] | **0.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1661 (0x67D). O ganho de informação não é o valor da informação ✅✅

**Na pergunta.** "Ganho esperado de informação" mede quanto a incerteza cai, e "valor" mede quanto a decisão melhora. São a mesma coisa só quando toda incerteza importa para a decisão.

**Lógica.** No mundo da P1632, observar o estado tira H(p) bits de incerteza. Escolher pelo ganho de informação é escolher por H(p), que não depende das utilidades.
- **A conta:** os 200 de maior ganho têm VOI = 0 com chance 1/2, e o medido foi **0,510** (a) ✅.
- **O valor médio** desses 200 é **0,0426**, contra **0,1696** dos 200 de maior VOI: a razão é 0,0426/0,1696 = **0,251** (b) ✅ [0,236; 0,352].

**O ganho de informação escolhe perguntas que valem um quarto das melhores.** Pior que a S(q) da Parte 73 (0,394), porque a S ao menos olhava o impacto.

**Geometria.** H(p) é uma tenda sobre [0, 1] com o pico em p = 1/2; o VOI é o afastamento entre a envoltória das retas e a corda dos extremos. A tenda é a mesma para todos os problemas, e
as envoltórias não: o ganho de informação mede a forma da dúvida, e o valor mede onde ela toca a escolha.

**Tradução cruzada.** É a curiosidade pura, saber por saber. Ela tem valor, mas não o valor que um orçamento de experimentos deve pagar: quem tem tempo para 30 experimentos e escolhe
pela entropia gasta metade em perguntas cujas respostas não mudam nada.

### P1662–P1663 (0x67E–0x67F). O orçamento: a razão quase ótima, o ΔK decisivo ✅✅❌✅✅

**Lógica.** 300 instâncias com 30 experimentos, custos inteiros de 1 a 20 e orçamento de 20% do custo total. O ótimo é exato (mochila 0-1 por programação dinâmica). A U(a) do texto é o guloso
pela razão valor/custo.
- **Com ΔK = VOI:** o guloso alcança **0,9922** do ótimo (c) ✅ (semente 75: 0,9924). É quase ótimo, mas é ótimo de fato em só **0,573** das instâncias (e) ❌.
- **(f) depois do erro de (e):** a faixa com o desvio binomial deu **0,620** ✅.
- **Com ΔK = ganho de informação:** o mesmo guloso alcança **0,568** do ótimo (d) ✅ (semente 75: 0,568).
- **O que importa mais:** a forma da regra (razão por custo) perde menos de 1%; a escolha do ΔK perde 43%. Por isso, definir o ΔK pelo valor da decisão vem antes de qualquer refinamento da
  regra.

**Por que o guloso não é sempre ótimo (a conta).** A mochila 0-1 é NP-difícil; o guloso por razão é ótimo na versão fracionária (Dantzig, 1957), e na 0-1 perde no máximo o valor do primeiro
item que não coube. Com 30 itens e orçamento de 20% do custo total, essa perda é pequena em média (1 − 0,9922 = 0,8%), mas frequente (1 − 0,573 = 43% das instâncias).

**Rodada 48 (P1663) (g) ✅.** O ótimo e os dois gulosos em Java: **IGUAIS em 301 linhas e 903 números**. Pelas somas: guloso por VOI = 0,9923 do total ótimo, guloso por H = 0,585 (as faixas
(c) e (d) usam a média das razões por instância: 0,9922 e 0,568). O verificador em Java que o texto diz "não implementado nem executado" está aqui, e concorda bit a bit.

**Meta.** Os itens são independentes. Com dependências entre experimentos (uma pergunta do texto), o valor de um conjunto não é a soma dos valores, e nem o guloso nem a mochila simples servem:
é preciso o VOI do conjunto. Fica como pergunta.

### P1664 (0x680). "Corrigi a expectativa e confirmei o resultado"

**Na pergunta.** O texto diz: "o teste inicial encontrou uma condição excessivamente restritiva: o histórico tinha quatro eventos, não cinco. Corrigi a expectativa e confirmei o resultado", e
depois relata **8/8**.

**O problema.** Um teste que falha e é ajustado ao valor que o código produziu deixa de testar o código: passa a descrevê-lo. Se a expectativa "5" estava errada, a pergunta é **por quê**, e a
resposta tem que vir de fora do código (a especificação: quantos eventos o cenário deveria gerar). Sem isso, "4" é só o que o programa fez, e o teste passaria com qualquer número.
**A contagem honesta é 7 de 8 na primeira execução, com 1 expectativa corrigida e a justificativa escrita**, e não 8/8.

**Como este projeto faz o mesmo de outro jeito.** Aqui também há expectativas que se mostram erradas, e a regra é registrar o erro no placar, nunca reescrever a previsão:
- (k) da Parte 72 errou por nível (contou verificações e chamou de `assert`) e ficou ❌;
- (e) desta parte errou pelo desvio de 4 lotes e ficou ❌, e a correção virou uma previsão nova, (f), testada num mundo novo (semente 75) antes de ser aceita.

O acumulado está em 199 erros em 625 testes. Uma correção de expectativa só vale como evidência quando prevê um mundo que ela não viu (a regra da Parte 25).

**Tradução cruzada.** Mudar a expectativa depois de ver o resultado é a racionalização. Jung diria que o ego protege a imagem de competência ("8/8"). A formalização é seca: um teste que não
pode falhar tem informação zero (a probabilidade de passar é 1, e −log₂ 1 = 0 bits).

**As outras afirmações do texto, conferidas:**
- 256 ÷ 4 = 64 caracteres hexadecimais no SHA-256 ✅.
- "Duas páginas que repetem a mesma notícia não são duas confirmações" ✅, com a conta: uma evidência de razão de verossimilhança 4 leva a crença de 1/2 a 4/(1 + 4) = **0,80**; contada duas vezes
  como independente, leva a 16/(1 + 16) = **0,941**. É a regra da Parte 32 deste projeto (unidades que falham juntas).
- "Como impedir que o sistema otimize a própria pontuação": a resposta medida na Parte 33 é o avaliador fora do alcance da mutação e a reavaliação do pai e do filho juntos em sementes novas. A regra
  ingênua "nota > nota guardada" piorou o agente real: 232,8 contra 159,9 (maldição do vencedor).
- As quatro limitações declaradas (contraexemplos, confiança não calibrada, contexto, histórico não imutável) ✅: declarar limites é o que o texto faz de melhor.

### P1665 (0x681). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 1)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **17208** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 352 | 5082 |
| compressão | **0.3963** | [0.3973; 0.4221] | ❌ | [0.3970; 0.4220] | ❌ | 0.4177 | 0.0132 | 0.0214 |
| testes de unidade | **3** | [2.87; 8.63] | ✅ | [4.00; 7.00] | ❌ | 6 | 2.50 | 3.00 |
| testes do placar | **7** | [5.67; 10.33] | ✅ | [5.00; 7.00] | ✅ | 8 | 1.00 | 1.00 |
| erros do placar | **1** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 0.67 | 1.00 |
| redundância P821 | **0.6659** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0589 | 0.0782 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 4 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 4 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **15543**, compressão **0.4016**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 1 erros.
- **Erros de processo nesta parte:** 1 (escrevi de cabeça "orçamento para ~6" itens; trocado pela definição antes do commit).

### P1666 (0x682). Engenharia reversa e Jung

**O padrão que se repetiu: confiar no desvio de poucos lotes.** A faixa de (e) usou o desvio de 4 lotes de calibração (0,0177), quando o desvio de uma fração em 300 instâncias tem forma fechada
(√(p(1 − p)/300) ≈ 0,028). Com 4 lotes, o próprio desvio estimado tem um erro relativo de ~40%, e eu o usei como se fosse exato. É o parente do erro da Parte 71 (uma tendência lida em três
pontos): **eu trato a dispersão que vi como a dispersão que existe.** **Regra:** quando a quantidade tem um desvio de forma fechada (binomial, Poisson), a faixa usa a forma fechada; o
desvio de poucos lotes só entra quando não há conta, e então com o t de poucos graus de liberdade, que foi o que eu fiz, mas não basta.

**O texto recebido mostra o mesmo padrão em espelho.** "Corrigi a expectativa e confirmei o resultado": diante de um teste que falhou, ele mudou o teste. Eu, diante de uma faixa que falhou,
mantenho o ❌ e abro um teste novo. A diferença não é errar menos; é onde a correção mora: lá, no passado (o teste reescrito); aqui, no futuro (a previsão nova, (f), num mundo que ela não viu).

**O que funcionou:** a conta antes da medida acertou as três previsões que tinham conta ((a): 1/2 por independência; (c) e (d) pela calibração de mesma geometria). As que dependiam só de
dispersão estimada erraram uma em duas.

**Jung: a persona do "8/8".** O relatório do texto mostra a persona: 8/8, todos os testes aprovados. A sombra é o 7/8 da primeira execução, que o relatório transforma em virtude ("o teste
revelou um erro nos critérios"). **Onde a formalização funciona:** um teste que se ajusta ao resultado tem probabilidade 1 de passar e informação zero; a persona do 8/8 não carrega bit nenhum
sobre o código. **Onde quebra:** às vezes a expectativa estava mesmo errada, e corrigi-la é honesto. Jung diria que a sombra integrada (o 7/8 escrito ao lado do 8/8) é o que separa uma
correção de uma racionalização; a formalização só consegue exigir que as duas contagens apareçam.

### O diálogo

Rodada 48 (P1663): a mochila e os gulosos em Java, IGUAIS. Placar por voz da função `p1241_placar_por_voz(48)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 48).

### P1689 (0x699). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅. Parte 74: **7 testes, 1 erros**. Acumulado (mundo): **199 erros em 625 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 3 pNN novas sem teste ✅. Sobre mim (placar separado): **4 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 4 de 6; e 1 erros de processo (P1335).

### P1690 (0x69A). Unificação

- **Novo:** `p1661` (ganho de informação contra VOI), `p1662` (o orçamento: ótimo e gulosos), `p1663` (rodada 48, IGUAIS). Regressão: + P1663.

> **Síntese da Parte 74:** escolher experimentos pelo "ganho esperado de informação" seleciona perguntas que valem um quarto das melhores (0,251; metade delas vale zero, como a conta de 1/2 prevê), porque a entropia não vê a decisão. Com orçamento, a regra do texto (valor/custo) é quase ótima quando o valor é o VOI (0,992 do ótimo exato da mochila, em dois lotes) e perde 43% quando o valor é a entropia (0,568, em dois lotes): o ΔK importa mais que a regra. O verificador em Java que o texto diz não ter implementado concorda bit a bit em 903 números (rodada 48). "Corrigi a expectativa e confirmei" transforma um 7/8 num 8/8: um teste ajustado ao resultado tem informação zero, e a correção honesta é uma previsão nova num mundo novo, como (f) depois do erro de (e).

---

**Fontes desta parte**
- Valor da informação: R. A. Howard, "Information Value Theory" (1966); ganho de informação contra valor de decisão: D. V. Lindley, "On a measure of the information provided by an experiment",
  *Annals of Mathematical Statistics* 27 (1956)
- A mochila e o guloso por razão: G. B. Dantzig, "Discrete-variable extremum problems", *Operations Research* 5 (1957); [Knapsack problem, Wikipedia](https://en.wikipedia.org/wiki/Knapsack_problem)
- SHA-256: NIST FIPS 180-4
- Lei de Goodhart: C. Goodhart (1975); maldição do vencedor: Parte 33 deste projeto
