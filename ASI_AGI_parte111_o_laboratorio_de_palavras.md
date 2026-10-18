# Parte 111 — O laboratório de palavras: Q-learning, a ação certa e o dicionário como data lake (0x6F)

↩ Parte 110 (a dúvida calculada: o reforço) · ↩ Parte 109 (o NEXUS anexado: a auditoria por AST) · ↩ Parte 30 (o DICIONÁRIO como data lake) · ↩ Parte 103 (o dicionário convertido em números) · ↩ Parte 88 (auditar o texto contra o PRÓPRIO código)

> Texto recebido no meio do ciclo, sem pedido escrito: duas versões de um programa, `word_rl_lab.py`. São um Q-learning tabular num jogo de palavras (uma grade de letras, estilo Boggle), um dicionário (API pública, WordNet ou lista embutida), um "estimador de confiança" e a avaliação guloso × aleatório. O próprio texto se apresenta como "o projeto real... sem backdoors, sem alegação de consciência". Pela regra das Partes 72/102/109, o tratamento é: as cópias verbatim vão para `externos/word_rl_lab/` (nunca importadas); a auditoria é pela AST, sem executar; e a reescrita é só com a biblioteca padrão, offline (`synthai/palavras_rl.py`), com as afirmações do texto testadas por previsões registradas antes.
>
> **A auditoria de segurança (feita antes desta parte, passo de segurança).**
> - A **v1** usa a rede por PADRÃO: se o `requests` estiver instalado, toda palavra vai primeiro à API, e o construtor faz `nltk.download`.
> - A **v2** só usa a rede se pedida (`--dicionario api` ou `--baixar-wordnet`); o padrão é a lista embutida, offline.
> - Nenhuma das duas se reexecuta, abre processos ou desserializa dados. Não é a família recusada; a rede simplesmente fica fora da reescrita.
>
> **Um defeito MEU, achado nessa auditoria.** O auditor AST da Parte 109 (`nexus.security_audit_ast`) errou nos dois sentidos aqui. Ele NÃO viu `requests.get` nem `nltk.download` na v1 (devolveu `[]`). E acusou na v2 só `import:urllib`, que ali é `urllib.parse.quote`, formatação de texto e não rede. Ele lê NOMES de módulo, não CAPACIDADES. A `security_audit_ast_v2` (nova; a antiga fica intacta) conta imports de módulos de rede (urllib.request sim, urllib.parse não) e chamadas de rede sobre bases de rede. Ela acha `requests.get` e `nltk.download` nas duas versões, e `[]` no próprio fonte.
>
> **As afirmações do texto que viram teste.** (1) "O agente supera o aleatório" (a avaliação da v2). (2) "Como a ação é a *letra*, o que se aprende vale em qualquer grade" — a razão da v2 para trocar o desenho da v1, em que a ação é a DIREÇÃO. (3) "O estimador de confiança supera a linha de base" (Brier). E uma pergunta do projeto: (4) o que muda quando o dicionário embutido (493 palavras) vira o DATA LAKE do WordNet 3.0 (77.340 lemas de letras a-z, `dados/`)?
>
> **A calibração, rodada ANTES deste registro (regras das Partes 63/64/84).** O mesmo desenho do teste (5.000 episódios de treino, 1.000 de avaliação, grade 5×5) nas sementes **7, 8 e 9**, escolhidas pela regra "as três sementes logo depois da do NEXUS (7)", antes de olhar. O teste usa a semente **42** (a padrão da v2) e um lote de replicação, as sementes **10 a 14**; nenhuma das duas rodou antes deste commit. Na calibração:
>
> | | s=7 | s=8 | s=9 |
> |---|---|---|---|
> | v2, embutido, guloso | 0,160 | 0,085 | 0,081 |
> | v2, embutido, aleatório | 0,010 | 0,010 | 0,010 |
> | v2, WordNet, guloso | 0,323 | 0,354 | 0,300 |
> | v2, WordNet, aleatório | 0,054 | 0,043 | 0,047 |
> | v1 (ação = direção), letras uniformes, guloso | 0,000 | 0,001 | 0,001 |
> | v1, letras por frequência, guloso − aleatório | +0,001 | +0,002 | −0,001 |
> | Brier do estimador / linha de base, embutido | 0,50 | 0,78 | 0,70 |
> | Brier do estimador / linha de base, WordNet | 0,47 | 0,49 | 0,45 |

## As perguntas desta parte

1. **P2771 (0xAD3).** O agente de Q-learning da v2 supera o aleatório, e de quanto, com o dicionário embutido? ↩ P2746
2. **P2772 (0xAD4).** A afirmação "a ação é a letra, então vale em qualquer grade" se sustenta? O desenho da v1 (ação = direção) aprende? ↩ P2771
3. **P2773 (0xAD5).** O estimador de confiança supera a linha de base, e por quê? ↩ P2742
4. **P2774 (0xAD6).** O DATA LAKE (WordNet, 77 mil lemas) no lugar da lista embutida: quanto muda o aleatório e o aprendido? ↩ P2532
5. **P2775 (0xAD7).** O auditor AST que eu uso lê capacidades ou nomes? ↩ P2712
6. **P2776 (0xAD8).** O passo de Q-learning tabular acrescenta fronteira entre Python e Java? (rodada 78) ↩ P2747

## Previsões pré-registradas (ANTES de medir — este commit)

Faixas de taxa: média ± 1,645 × desvio × 1,36 (fator da Parte 79) quando o desvio vem das 3 sementes de calibração. Quando a quantidade é binomial de forma fechada (o aleatório), uso 1,645·√(p(1−p)/1000), sem o fator (regra da Parte 74).

- **(a) P2771** v2, dicionário embutido, semente 42: a taxa de palavra válida do guloso. Média 0,109 e desvio 0,045 entre sementes; faixa **[0,03; 0,22]**. Mecanismo esperado dentro da faixa (regra da Parte 110 para faixa larga): o guloso converge para poucas palavras de pontuação alta, e QUAIS ele acha depende da semente.
- **(b) P2771** O aleatório, nas mesmas grades: binomial com p ≈ 0,010 e n = 1.000, faixa **[0,005; 0,016]**.
- **(c) P2771** Replicação nas sementes 10 a 14: número de sementes em que os ICs de Wilson do guloso e do aleatório NÃO se sobrepõem, **[4; 5]**. A calibração deu 3 de 3; a pior folga foi 0,066 contra 0,018.
- **(d) P2772** O desenho da v1 (ação = direção, estado = 3 últimas letras, letras uniformes, como na v1), semente 42: taxa do guloso **[0; 0,004]**.
- **(e) P2772, subverso.** O desenho da v1 com as letras por frequência da v2 (separa a causa "letras raras" da causa "ação = direção"): guloso − aleatório **[−0,004; 0,006]**. A ação-direção não aprende, mesmo com letras boas. A direção não é uma propriedade da palavra; numa grade nova, a mesma direção leva a outra letra.
- **(f) P2773** Razão Brier do estimador / linha de base, embutido, semente 42: **[0,35; 0,97]** (< 1: supera). Mecanismo esperado: a variável que carrega a previsão é o Q(PARAR) do próprio agente, e não o vetor da palavra.
- **(g) P2773** A mesma razão com o WordNet: média 0,472 e desvio 0,019, faixa **[0,43; 0,51]**.
- **(h) P2774** WordNet, semente 42, guloso: **[0,27; 0,39]**.
- **(i) P2774** WordNet, semente 42, aleatório: binomial com p ≈ 0,048, faixa **[0,037; 0,060]**.
- **(j) P2774** Razão aleatório WordNet / aleatório embutido, semente 42: calibração 5,4 / 4,3 / 4,7, mas o embutido tem ~10 acertos (desvio relativo ≈ 30%), faixa **[3,0; 7,5]**.
- **(k) P2775** Controles dos dois lados da `security_audit_ast_v2`, num caso plantado com as quatro formas de rede (`import requests` + `requests.get`, `nltk.download`, `urllib.request.urlopen`, `socket.create_connection`) e num caso limpo com os falsos positivos da 109 (`from urllib.parse import quote`, `re.compile`, `asyncio.run`, a string "requests.get("). Achados no plantado **[6; 6]**: os 4 de rede + `import:requests` + `import:socket`. A identidade que garante a faixa estreita: são as 6 linhas plantadas, cada uma casando uma regra. No limpo, **[0; 0]**: nenhuma regra casa uma string nem um módulo de formatação.
- **(l) P2776** O passo TD tabular (Q ← Q + α(r + γ·max Q′ − Q)), num episódio fixo de 2.000 atualizações sobre uma tabela pequena: **IGUAL** bit a bit, divergências **[0; 0]**. Identidade: só +, −, ×, max e comparação, na mesma ordem nas duas línguas.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[11; 15]** (12 agora + ~2 por surpresa esperada)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 5]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,10; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Três pontos de calibração não fixam um desvio (regra da Parte 64), e é ali que mora o risco. (a) e (f) dependem de QUAIS palavras o guloso acha numa semente. (j) é uma razão com ~10 acertos no denominador. (k) e (l) são identidades com a lista escrita ao lado. (b), (i) e (c) são binomiais. Espero **1 a 3 erros**, em (a), (f) ou (j).

### Adendo pré-registrado: os mecanismos de (a) e (f) postos à prova (escrito DEPOIS da 1ª medição, ANTES destes dois)

Pela regra da Parte 110, uma faixa larga que acerta não confirma o mecanismo que eu escrevi dentro dela. Os dois mecanismos viram teste.

- **(n) P2773, ablação.** Na semente 42 e com o embutido, o estimador treinado com a variável Q(PARAR) ZERADA (fixa em 0 nas features; o resto igual). Se o mecanismo de (f) estiver certo, só o vetor da palavra sobra, e ele não sabe se uma palavra de 3 a 5 letras está numa lista de 493. A razão Brier volta para perto de 1: **[0,80; 1,10]**. Se ficar abaixo de 0,80, o vetor da palavra carrega informação e o mecanismo de (f) está errado.
- **(o) P2771, o mecanismo de (a).** Na avaliação gulosa da semente 42 (1.000 episódios), o número de palavras DISTINTAS válidas: o guloso converge para poucas, **[3; 20]**, contra o treino (que explora com ε). A identidade da fixture: contam-se os `prefix` válidos distintos devolvidos por `run_episode` no modo guloso, nas mesmas grades de `evaluate`.

### Adendo 2 pré-registrado: a surpresa de (n) (escrito DEPOIS de (n), ANTES deste)

(n) deu 0,635, abaixo da faixa: sem o Q(PARAR), o estimador ainda bate a linha de base em 36%. A minha hipótese: a informação está no COMPRIMENTO (a feature `len/max_len`, que eu não listei no mecanismo de (f)). Na lista embutida há 141 palavras de 3 letras, contra muito menos combinações de 5 letras que formam palavra; uma cadeia de 5 letras quase nunca é palavra.

- **(p) P2779.** Sem o Q(PARAR) E sem o comprimento (as duas fixas em 0; sobra só o vetor das letras, normalizado, que NÃO carrega o comprimento): a razão sobe para **[0,85; 1,10]**. Se ficar abaixo de 0,85, a composição das letras (vogais, letras frequentes) carrega informação, e a minha hipótese do comprimento é insuficiente.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2771 — O agente supera o aleatório?

**Na pergunta.** "Superar o aleatório" é a régua mínima, e a v2 a escolheu bem: as MESMAS grades, os mesmos inícios e ICs de Wilson. Ela pergunta pelo que o agente aprendeu, não pelo número que ele faz.

**Lógica.** Semente 42, dicionário embutido: guloso **0,130** ✅ (a), aleatório **0,006** ✅ (b), uma razão de ~22×. ICs [0,111; 0,152] contra [0,003; 0,013], disjuntos. A replicação nas sementes 10 a 14 dá guloso 0,129 / 0,125 / 0,141 / 0,167 / 0,196 contra aleatório 0,007 a 0,011: **5 de 5** com ICs disjuntos ✅ (c). A afirmação da v2 se sustenta em 6 lotes independentes (a regra da Parte 66: um efeito visto em vários lotes).

**O mecanismo (o).** O guloso forma **20** palavras distintas em 1.000 episódios ✅ (no limite da faixa [3; 20]). As de 3 letras dominam: EAT 22, ATE 17, DOT 11, HOT 11, TOT 9, EAR 9… e só 3 de 4 letras (DEAR, HOME, SAME). O agente aprendeu um REPERTÓRIO de palavras curtas feitas de letras frequentes, não o dicionário. Com 493 palavras e 5.000 episódios, achar EAT de novo vale mais do que procurar uma palavra de 5 letras.

**Tradução cruzada.** É o hábito na psicologia de Jung: a função dominante se especializa no que já deu certo, e o que não foi tentado não existe para ela. O ε da exploração é a função inferior: pequena, mas a única porta para o novo.

### P2772 — "A ação é a letra, então vale em qualquer grade"

**Lógica.** O desenho da v1 (ação = DIREÇÃO, estado = 3 últimas letras, letras uniformes): guloso **0,000** ✅ (d). Com as letras por frequência da v2: guloso − aleatório = **+0,001** ✅ (e). O desenho da v1 não aprende NADA, e não por causa das letras raras.

**O porquê, em forma fechada.** Numa grade nova e aleatória, a direção "nordeste" a partir de um E leva a qualquer letra, com a distribuição das letras: o valor Q(estado, direção) é a média sobre todas as grades, e essa média não depende da direção (por simetria, fora das bordas). A ação-direção não tem informação. A ação-LETRA tem: Q("EA", "T") aprende que EAT existe, em qualquer grade onde houver um T vizinho. A v2 tinha razão, e a razão é estatística: só se aprende sobre uma ação cuja consequência é a mesma entre os episódios.

**Tradução cruzada.** Aprender que "virar à direita" é bom só vale numa cidade fixa; aprender que "a padaria" é boa vale em qualquer cidade que tenha uma. A representação da ação é a hipótese sobre o que se repete no mundo.

### P2773 — O estimador de confiança

**Lógica.** A razão Brier do estimador / linha de base é **0,461** com o embutido ✅ (f) e **0,456** com o WordNet ✅ (g): o estimador bate a linha de base em ~54%. Mas o mecanismo que eu escrevi dentro da faixa larga de (f) ("quem carrega a previsão é o Q(PARAR)") **caiu duas vezes**:
- **(n) ❌.** Sem o Q(PARAR), a razão é **0,635**, abaixo da faixa [0,80; 1,10].
- **(p) ❌.** Sem o Q e sem o comprimento, sobra **0,762**, abaixo de [0,85; 1,10].

A cadeia medida é **0,461 (tudo) → 0,635 (sem Q) → 0,762 (só as letras)**. Cada peça carrega uma parte, e nenhuma carrega tudo.

**Meta (onde eu errei).** Duas explicações de uma causa só, e as duas falharam: primeiro o Q, depois o comprimento. O padrão é a Parte 61 em versão nova: um efeito com várias causas pequenas lido como uma causa grande. A HIPÓTESE que fica (não testada; vai para a pendência da Parte 112): as letras carregam informação porque o estimador aprende o REPERTÓRIO do próprio agente. Os vetores de EAT, ATE e HOT se repetem, e o estimador aprende "este vetor costuma ser válido" sem saber nada do dicionário. O teste é um estimador treinado sobre as palavras de uma política ALEATÓRIA (sem repertório), onde a razão deveria voltar para ~1.

**Tradução cruzada.** É a calibração que vem da familiaridade, não do conhecimento: o estimador fica confiante no que já viu dar certo. A v2 diz "calibração não é consciência", e está certa. Esta medida mostra que esta calibração nem é conhecimento do mundo: é conhecimento dos próprios hábitos do agente.

### P2774 — O dicionário como data lake

**Lógica.** O WordNet 3.0 do projeto (**77.340** lemas a-z, `dados/`), no lugar da lista embutida (493): o aleatório vai de 0,006 para **0,037** ✅ (i), uma razão de **6,17** ✅ (j), e o guloso para **0,354** ✅ (h). Com o data lake o agente acha 2,7× mais palavras válidas. Ele não ficou mais esperto: o mundo ficou mais generoso, porque o WordNet aceita cadeias que a lista embutida recusa (abreviações, nomes, termos técnicos de 3 letras).

**Tradução cruzada.** O mesmo comportamento parece mais inteligente num mundo mais permissivo. A régua de "inteligência" de um agente inclui o dicionário que o julga: medir a mesma política com dois juízes separa o agente do juiz (a regra da Parte 20: nenhum módulo aprovado só pela própria métrica).

### P2775 — O auditor que eu uso

**Lógica.** O auditor da Parte 109, que lê NOMES, devolveu **[]** na v1, que tem `requests.get` e `nltk.download` (um falso negativo), e **["import:urllib"]** na v2, que ali é `urllib.parse.quote` (um falso positivo). O auditor por CAPACIDADE (`security_audit_ast_v2`) acha `requests.get`, `nltk.download` e o import de `requests` nas duas versões, e **[]** no próprio fonte e no caso limpo. No caso plantado ele acha **7**, contra os 6 da faixa: **(k) ❌**. A fixture tinha `import urllib.request` (que o `urlopen` exige), e eu não contei esse import na identidade escrita, porque a fixture ainda não existia quando escrevi a previsão.

**Meta.** Uma previsão de contagem "por identidade" só é uma identidade se o objeto contado existe no momento da previsão. **Regra nova:** a fixture de um teste de contagem vai NO commit do pré-registro.

### P2776 — rodada 78

**Lógica.** O passo de Q-learning tabular (5 × 3, 2.000 transições de um LCG inteiro), Python × Java: **IGUAIS, 6 linhas e 15 números bit a bit** ✅ (l). 22 rodadas: o aprendizado por reforço tabular é aritmética portável, como o GD (77), o Adam (59) e a indução reversa (74).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ❌ (l) ✅ (n) ❌ (o) ✅ (p) ❌. Parte 111: **15 testes, 3 erros**:
- (k): a fixture fora da conta;
- (n) e (p): o mecanismo do estimador, errado duas vezes.

As afirmações do TEXTO recebido passaram todas: o agente supera o aleatório (6 lotes), a ação-letra aprende e a ação-direção não, e o estimador supera a linha de base. Os três erros são MEUS, de mecanismo. Acumulado (mundo): **224 erros em 850 testes**. Calibração (P1961, Partes 80–111): **170/191 = 0,890**.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [11; 15] | 15 | ✅ |
| (m2) | [2; 5] | 3 | ✅ |
| (m3) | [0,10; 0,60] | 0,21 | ✅ |
| (m4) | [0,60; 1,00] | 0,80 | ✅ |
| (m5) | [0; 3] | 1 | ✅ |
| (m6) | [0; 3] | 1 | ✅ |

Previsões sobre previsões (p1499): **6 de 6**. A (m1) acertou no limite porque somei ~2 por surpresa esperada (a regra que a 109 esqueceu e a 110 aplicou): as surpresas geraram (n), (o) e (p). O leitor `p1481` perdeu de novo as faixas de (n) e (o) (o defeito medido na 110, rótulo em negrito); a correção segue pendente.

## Engenharia reversa (metacognição)

**O padrão: os textos recebidos acertaram, e eu errei nos mecanismos.** É a primeira vez numa série longa de partes de auditoria (72, 82, 83, 85–88, 95, 102, 109) em que TODAS as afirmações medidas de um texto recebido se sustentaram. E os três erros desta parte são todos MEUS: uma fixture fora da conta, e duas explicações de causa única para um efeito de causas múltiplas. **Significado:** a minha régua de auditoria carregava um preconceito aprendido em oito lotes. Eu esperava que a prosa prometesse mais do que o código entrega, e por isso pus o esforço em procurar defeitos no texto e quase nenhum em testar as minhas próprias explicações. Este texto foi escrito para ser auditado (ele mesmo traz as linhas de base, os ICs, a avaliação nas mesmas grades), e a auditoria virou contra quem audita. **Regra nova:** a expectativa sobre um texto recebido vem do texto, não da série: medir primeiro se ele traz os próprios controles (linha de base, mesma amostra, IC). Se traz, o risco maior está nas minhas explicações, não nas dele.

**O segundo padrão, que repete a Parte 109: o meu próprio verificador falhou de novo pelo NOME.** A auditoria da 109 lia nomes de módulo, e aqui errou nos dois sentidos. A regra da 109 ("todo verificador roda primeiro sobre o próprio fonte") não pegaria isso, porque o próprio fonte da 109 não tem `requests`. **Regra:** um verificador novo roda também sobre os ÚLTIMOS textos recebidos antes de ser usado num novo, porque o caso que ele não conhece é sempre o próximo.

## Síntese / unificação

A Parte 111 anexa o word_rl_lab à SYNTHAI (`synthai/palavras_rl.py`: biblioteca padrão, offline, os autotestes da v2 portados). As três afirmações do texto passaram:
- o Q-learning supera o aleatório (0,130 contra 0,006, replicado em 5 de 5 sementes);
- a ação-LETRA aprende e a ação-DIREÇÃO não (0,000; +0,001 mesmo com letras boas);
- o estimador de confiança supera a linha de base (Brier 0,46 da base).

Juntou-se o DATA LAKE do projeto (77.340 lemas do WordNet): o mundo mais generoso multiplica o aleatório por 6,2 e o guloso por 2,7, o que separa o agente do juiz. Os meus erros foram de mecanismo. O estimador não é carregado por uma causa só (0,461 → 0,635 → 0,762); a hipótese do repertório fica para a Parte 112. A auditoria ganhou a versão por CAPACIDADE (`security_audit_ast_v2`), que corrige o falso negativo e o falso positivo da versão por nome. Rodada 78: o Q-learning tabular é IGUAL bit a bit (22 rodadas). 12/15 do mundo, 6/6 (m), calibração 0,890.

A SYNTHAI ganha a sua 5ª forma de agente, depois da decisão bayesiana, do GPT, do pulsado e do modelo de mundo: um agente de reforço sobre o dicionário. A lição da Parte 110 se confirma no caso real: o Q-learning funciona quando a ação tem consequência estável entre episódios (a letra), e não aprende nada quando não tem (a direção).

## Meta

Confiança alta nas afirmações do texto (6 lotes, ICs disjuntos) e nas identidades (rodada 78, controles do auditor). Média na explicação do estimador: três medidas, nenhuma causa única, e a hipótese do repertório sem teste. Onde é brinquedo: uma grade 5×5, palavras de 3 a 5 letras, 5.000 episódios e uma tabela Q de ~15 mil entradas. O que não mudou: nenhuma rede (os backends `api` e `--baixar-wordnet` da v2 não existem na reescrita) e nenhum código recebido executado.

## Diálogo Python ↔ Java (rodada 78)

Ver `dialogo/DIALOGO.md`: o passo de Q-learning tabular, com as transições geradas por um LCG inteiro (sem o `random` de cada língua), é **IGUAL**: 6 linhas e 15 números bit a bit.

## Fontes

- Q-learning tabular e a prova de convergência: [Watkins e Dayan, "Technical Note: Q-Learning", Machine Learning 8 (1992)](https://www.springerprofessional.de/en/technical-note/13819926); [Tsitsiklis (1994), convergência assíncrona](https://www.mit.edu/people/jnt/Papers/J052-94-jnt-q.pdf).
- O intervalo de Wilson (1927), "Probable inference, the law of succession, and statistical inference", JASA 22: [notas de Cousins, arXiv 1807.05996](https://arxiv.org/pdf/1807.05996); [Boost, wilson_interval](https://www.boost.org/doc/libs/master/boost/histogram/utility/wilson_interval.hpp).
- O escore de Brier (1950), "Verification of forecasts expressed in terms of probability", Monthly Weather Review 78: [scores, tutorial do Brier Score](https://scores.readthedocs.io/en/latest/tutorials/Brier_Score.html); [NOAA, repositório](https://repository.library.noaa.gov/view/noaa/33800).

---

➡ Continua na [Parte 112 — O Kuhn completo](ASI_AGI_parte112_o_kuhn_completo.md).
