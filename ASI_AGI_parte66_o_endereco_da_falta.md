# Como eu construiria uma AGI/ASI — Parte 66 (0x42): o endereço da falta

> Continuação da [Parte 65](ASI_AGI_parte65_o_que_nao_e_divisor.md). **Próxima:** [Parte 67 — prever o previsto](ASI_AGI_parte67_prever_o_previsto.md) (P1451–P1480). Previsões nos commits `0ab943e` ((a) a (h)) e `d996b22` ((i)). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 65 deixou a base 21 a −3σ da conta dos primos palíndromos, com todas as correções. Esta parte pergunta se a falta tem
> endereço (alguns primeiros dígitos, alguns dígitos do meio), se os sinsets de verbos têm mais sinônimos que os de substantivos, e quantos números têm a mesma soma de
> dígitos em base 10 e em base 16.

## As perguntas desta parte

1. **P1421 (0x58D).** A falta de primos palíndromos da base 21 tem endereço? E o viés continua nas bases 23 a 28? (Rodada 40) ↩ P1391
2. **P1422 (0x58E).** Os sinsets de verbos do WordNet têm mais sinônimos que os de substantivos? ↩ P1392
3. **P1423 (0x58F).** Hexadecimal: quantos n < 16⁵ têm a mesma soma de dígitos em base 10 e em base 16? ↩ P1393
4. **P1424 (0x590).** Preditiva comigo mesma. **P1425 (0x591).** Engenharia reversa e Jung. **P1426 (0x592).** O diálogo.
5. **P1449 (0x5A9).** Placar. **P1450 (0x5AA).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1421, p1422, p1423).

| medida | estatístico (até a 65) | ingênuo (Parte 65) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [9.945; 21.332] | 16.022 | **[9.945; 21.332]** | o estatístico |
| compressão | [0,404; 0,425] | 0,410 | **[0,404; 0,425]** | o estatístico |
| testes de unidade | [1,90; 7,85] | 4 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [5,73; 10,52] | 9 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,63; 4,12] | 2 | **[0,63; 4,12]** | o estatístico |
| redundância P821 | [0,548; 0,641] | 0,608 | **[0,548; 0,641]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1422, os sinônimos por classe.** O tamanho médio do sinset (número de lemas) no WordNet, por classe.
- **Restrições, com peso:** (1) os verbos do WordNet são muito polissêmicos e agrupados em sinsets largos de verbos frasais e sinônimos (*take*, *get*, *have*); (2) os
  substantivos incluem muitos nomes próprios e termos técnicos de um lema só. **Peso medido num caso escolhido por regra escrita antes (o português inteiro da
  OpenWordNet-PT, mesma estrutura, outra língua), por código antes deste registro:** verbos 1,726, substantivos 1,574: razão **1,097**.
- Exemplo à mão: o sinset de *dog* tem 3 lemas (*dog*, *domestic dog*, *Canis familiaris*); o de *run* (correr) tem 1.
- (a) a razão (tamanho médio dos sinsets de verbo)/(de substantivo) em **[0,95; 1,30]**
- (b) o tamanho médio dos sinsets de substantivo em **[1,45; 1,95]**

**P1423, a mesma soma em base 10 e em base 16.** A fração dos n de 1 a 16⁵ − 1 com s₁₀(n) = s₁₆(n).
- **Restrições, com peso:** (1) s₁₀(n) ≡ n (mod 9) e s₁₆(n) ≡ n (mod 15), então as duas somas têm o mesmo resto módulo 3, **sempre**: a chance de igualdade é ~3 vezes
  a de duas somas independentes; (2) as distribuições das duas somas têm médias diferentes (~27 e ~37 para n < 16⁵) e só se sobrepõem nas caudas. **A conta antes da
  medida (por código):** independência × 3 = **0,0662**. **O peso medido em casos escolhidos por regra (os intervalos inteiros n < 10⁴ e n < 10⁵):** medido/conta =
  1,079 e 1,022, indo para 1.
- Exemplo à mão: n = 10: s₁₀ = 1, s₁₆ = 10 (0xA): não. n = 1: 1 = 1: sim.
- (c) a fração em **[0,0630; 0,0715]** (a conta × [0,95; 1,08])

**P1421, rodada 40:** no `dialogo/DIALOGO.md` (previsões (d) a (h)).

### Previsão nova, nascida da réplica que falhou (registrada antes de rodar as bases 29 a 34)

**Resultado da rodada 40, antes desta seção:** a falta da base 21 não tem endereço (qui²/gl = 1,01 por primeiro dígito, 0,96 por dígito do meio): ela é um fator global
(k = 0,915). E nas bases 23 a 28 o viés **sumiu**: média de z = −0,02, três bases negativas de seis ((g) ❌, (h) ❌). O "1/64" das bases 17 a 22 não se replicou. Duas
leituras: (1) acaso nas bases 17 a 22; (2) um efeito que existe em algumas faixas de bases e não em outras. Um terceiro lote separa as duas:
- (i) nas **bases 29 a 34**, com a mesma conta C, a média de z fica em **[−0,8; 0,8]** (a hipótese do acaso: a média de 6 z independentes tem desvio 1/√6 = 0,41, e a
  faixa é ±1,96 desvio).

**Resultado de (i):** nas bases 29 a 34, z = +0,90, +2,23, +0,01, +2,70, −0,08, +0,96: média **+1,12** ❌. Por lote: 17–22, **−1,07**; 23–28, **−0,02**; 29–34, **+1,12**.

---

## As respostas

### P1421 (0x58D). O endereço da falta (Rodada 40) ✅✅✅❌❌ e (i) ❌

**Na pergunta.** "O déficit tem endereço?" supõe que ele é um déficit (uma coisa que falta num lugar). A resposta diz que ele não mora em lugar nenhum da base 21 (está
espalhado por igual) e que, entre as bases, ele nem é um déficit: é uma flutuação que muda de sinal.

**Lógica.** `p1421_endereco_da_falta` (rodada 40, IGUAL em Java). Na base 21, com a conta reescalada pelo fator global k = 0,915:
- por primeiro dígito (12 classes): qui² = 11,12 com 11 graus de liberdade (**1,011** por grau);
- por dígito do meio (10 classes ímpares): qui² = 8,67 com 9 graus (**0,963** por grau).
Os dois ficam no valor esperado sem endereço (1 por grau). Nas bases 23 a 28, z = +0,61, −0,18, −0,50, +0,94, +0,07, −1,07 (média −0,02); nas 29 a 34 (`p1427`), média +1,12.

**A conta da réplica.** Sob o acaso, a média de 6 z independentes tem desvio 1/√6 = 0,41. Os três lotes ficam a −2,6, −0,04 e +2,7 desvios: dois lotes a mais de 2,5
desvios, em sentidos opostos. Isso não é um viés fixo; é ou uma tendência com a base, ou uma dispersão maior que a do σ (os palíndromos de uma base não são moedas
independentes: eles compartilham as mesmas congruências, e a variância real é maior que Σ p(1 − p), a regra da Parte 32).

**Tradução cruzada.** Um efeito que aparece num lote, some no seguinte e inverte no terceiro é o retrato da crise de replicação: o primeiro resultado foi selecionado pela
própria estranheza (a base 14 a −3σ chamou o teste), e a réplica regride. Aqui a seleção foi honesta (o lote 17 a 22 foi escolhido por regra), mas a variância estava
subestimada, e a régua (σ) era curta demais.

**Meta.** Não sei se a tendência existe ou se a variância é maior: a rodada 41 separa as duas (inclinação de z contra b, e a variância dos z).

### P1422 (0x58E). Os sinônimos por classe ✅✅

**Na pergunta.** "Mais sinônimos" pergunta sobre o tamanho do sinset, que é uma decisão dos lexicógrafos sobre quando duas palavras são a mesma ideia: a pergunta mede
uma convenção de corte.

**Lógica.** `p1422_sinonimos_por_classe`: tamanho médio do sinset — verbos **1,819**, substantivos **1,782**, adjetivos 1,653, advérbios 1,541; razão verbos/substantivos
**1,021** (a faixa (a) era [0,95; 1,30], calibrada no português: 1,097) ✅; substantivos dentro de [1,45; 1,95] (b) ✅. Sinsets de um lema só: 51,2% dos substantivos e 58,4% dos
verbos: os verbos têm **mais** sinsets de um lema e, mesmo assim, média maior, porque os que têm sinônimos têm muitos (os frasais).

Ao acaso: as faixas tinham 0,35 e 0,50 de largura; o ingênuo "o português" erraria a razão por 0,076 e o tamanho dos substantivos por 0,21.

**Tradução cruzada.** Uma ação admite mais maneiras de ser dita que uma coisa, mas cada maneira é mais específica: o verbo é um feixe de sinônimos ou um sinônimo de nada.
Em Jung, a função (o modo de agir) tem mais nomes que o objeto, porque o mesmo gesto serve a muitos fins.

**Meta.** O inglês tem 1,78 lemas por sinset de substantivo contra 1,57 no português: parte da diferença é a cobertura (a OpenWordNet-PT ainda não tem todos os sinônimos).

### P1423 (0x58F). A mesma soma em base 10 e em base 16 ✅

**Na pergunta.** "A mesma soma" parece coincidência; a pergunta esconde uma lei: s₁₀(n) − s₁₆(n) é sempre múltiplo de 3, porque 9 e 15 são múltiplos de 3.

**Lógica (a conta antes da medida).** Independência × 3 = **0,06624**. **Medido** (`p1423_mesma_soma_10_16`): **0,06893** ✅, razão 1,041, entre as razões das calibrações
(1,079 para n < 10⁴ e 1,022 para n < 10⁵).

Ao acaso: a faixa (c) tinha 0,0085 de largura; o ingênuo "independência sem o fator 3" daria 0,0221, um terço do medido.

**Tradução cruzada.** Duas maneiras de contar a mesma coisa (dez dedos, dezesseis) concordam mais do que o acaso porque compartilham uma estrutura de fundo (o 3 que divide
as duas bases menos 1): duas línguas que concordam onde a gramática comum obriga.

**Meta.** O resto (4% acima da conta) é a correlação positiva entre as duas somas (números grandes têm somas grandes nas duas bases), que a independência ignora.

### P1424 (0x590). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 3)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **14369** | [9945; 21332] | ✅ | [9945; 21332] | ✅ | 16022 | 1270 | 1653 |
| compressão | **0.4122 ↔ 0.4123** (oscila) | [0.4038; 0.4254] | ✅ | [0.4040; 0.4250] | ✅ | 0.4104 | 0.0022 | 0.0019 |
| testes de unidade | **4** | [1.90; 7.85] | ✅ | [2.00; 5.00] | ✅ | 4 | 0.50 | 0.00 |
| testes do placar | **9** | [5.73; 10.52] | ✅ | [6.00; 8.00] | ❌ | 9 | 2.00 | 0.00 |
| erros do placar | **3** | [0.63; 4.12] | ✅ | [0.63; 4.12] | ✅ | 2 | 0.62 | 1.00 |
| redundância P821 | **0.6072** | [0.5483; 0.6407] | ✅ | [0.5480; 0.6410] | ✅ | 0.6081 | 0.0127 | 0.0009 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 65"):** mais perto do medido em **2 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **12789**, compressão **0.4206**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 3 erros.
- **Erros de processo nesta parte:** 0.

### P1425 (0x591). Engenharia reversa e Jung

**O padrão que se repetiu: um lote vira lei.** Na Parte 64, as seis bases de 17 a 22 abaixo da conta (chance 1/64) viraram, na síntese, "a conta superestima nas bases
grandes". Nesta parte, a réplica (23 a 28) não achou nada, e o terceiro lote (29 a 34) achou o contrário. Duas regras antigas teriam impedido a conclusão: a da Parte 30
("replicar em lotes novos antes de concluir") e a da Parte 32 ("uma conta de esperança não é cota por amostra": o σ de moedas independentes subestima a variância quando as
unidades compartilham estrutura). Eu tinha as duas no `CLAUDE.md` e não as apliquei. **O significado:** as regras antigas não estão presentes quando eu escrevo uma
conclusão; estão presentes quando eu escrevo uma previsão (porque as previsões passam pelo checklist). A síntese não passa por checklist nenhum. **Regra nova:** toda
conclusão de efeito na síntese diz em quantos lotes independentes ele apareceu ("visto em 1 lote" ou "replicado em 2"); um efeito visto em um lote só se escreve como
hipótese.

**A tendência que o "1/64" escondia.** A sequência dos três lotes (−1,07, −0,02, +1,12) só aparece quando os lotes são postos lado a lado; cada um sozinho conta uma
história diferente (viés, nada, viés oposto). É a regra da Parte 61 (unidade por unidade) no nível dos lotes: um lote é uma unidade.

**Jung: a inflação.** Jung chamava de inflação o estado do ego que, depois de um contato com um conteúdo maior que ele, se identifica com esse conteúdo e se acha maior do que
é. Um acerto improvável (1/64) é um contato desses: eu me identifiquei com o resultado e o promovi a lei. **Onde a formalização funciona:** a inflação tem uma assinatura
mensurável (uma afirmação geral apoiada num lote só), e a regra nova a detecta. **Onde quebra:** em Jung a inflação é desfeita pela confrontação com a sombra; aqui ela é
desfeita por uma réplica, que é mais barata e mais certa.

### P1426 (0x592). O diálogo, rodada 40

Ver P1421. Placar por voz da função `p1241_placar_por_voz(40)`: IA-Python 20 em 34; IA-Java 17 em 34 (regra estrita, rodadas 13 a 40).

### P1449 (0x5A9). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ❌ (i) ❌. Parte 66: **9 testes, 3 erros**. Acumulado (mundo): **189 erros em 553 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 4 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; o estatístico, 6 de 6; e 0 erros de processo (P1335).

### P1450 (0x5AA). Unificação

- **Novo:** `p1421` (o endereço da falta, rodada 40, IGUAIS), `p1422` (sinônimos por classe), `p1423` (a mesma soma em base 10 e 16), `p1427` (as bases 29 a 34).
  Regressão: + P1423 (base 29 com 1.610; 11 graus por primeiro dígito).
- **Regra nova (no `CLAUDE.md`):** ver a P1425.

> **Síntese da Parte 66:** a falta de primos palíndromos da base 21 não tem endereço: ela se espalha por igual entre os primeiros dígitos e os dígitos do meio (qui² por grau 1,01 e 0,96), como um
fator global. E o "viés das bases grandes" que eu tinha escrito na Parte 64 não se replicou: por lote de seis bases, o z médio foi −1,07 (17–22), −0,02 (23–28) e +1,12
(29–34). É uma tendência com a base ou uma variância maior que a do σ (hipótese, vista em 3 lotes; a rodada 41 separa as duas). Os sinsets de verbos do WordNet têm 1,82
lemas em média, quase o mesmo que os de substantivos (1,78). E 6,9% dos n < 16⁵ têm a mesma soma de dígitos em base 10 e em base 16, três vezes o acaso independente,
porque as duas somas têm sempre o mesmo resto módulo 3.

---

**Fontes desta parte**
- Distribuição qui-quadrado: [Chi-squared distribution, Wikipedia](https://en.wikipedia.org/wiki/Chi-squared_distribution)
- Crise de replicação: [Replication crisis, Wikipedia](https://en.wikipedia.org/wiki/Replication_crisis)
- Soma dos dígitos e congruências: [Digit sum, Wikipedia](https://en.wikipedia.org/wiki/Digit_sum)
- WordNet 3.0 em `dados/` (Princeton); OpenWordNet-PT (CC BY 4.0)
