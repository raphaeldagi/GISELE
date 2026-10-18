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
