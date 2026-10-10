# Como eu construiria uma AGI/ASI — Parte 75 (0x4B): o que se prova

> Continuação da [Parte 74](ASI_AGI_parte74_o_que_vale_testar.md). Nasce do quinto texto recebido do usuário (`externos/texto_recebido_parte75.md`): o relatório do Módulo 007 (um planejador com
> orçamento e um `Verifier.java`) e uma "Arquitetura Neuro-Simbólica Recursiva para AGI e Superinteligência", com código de **auto-modificação**: Python muta o próprio código pela árvore
> sintática, e um "núcleo" Java o aprova por "prova de utilidade de Gödel", num laço `while True`. O código **não é executado** (regras das Partes 33 e 72): é lido como dado, e cada afirmação
> dele é testada por uma reimplementação minha, escrita do zero.

## Previsões sobre as minhas previsões desta parte (antes de pensar qualquer faixa do mundo)

- **(m1)** o número de previsões do mundo em **[4; 9]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,03; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~5 previsões do mundo e ~4 funções novas.

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

## Previsões do mundo (antes de medir; todas pela reimplementação, nenhuma pelo código recebido)

**O laço de auto-modificação, lido.** O Python envia `json.dumps(payload)`; o Java procura cada campo com `"\"" + campo + "\":\""` e `indexOf`. O `json.dumps` do Python, por padrão, separa chave
e valor com `": "` (dois-pontos e espaço).
- **(a)** no payload que o Python realmente envia, a busca do Java **não acha** nenhum dos dois campos e devolve `""` para os dois (categórica)
- **(b)** por isso o núcleo avalia o código vazio: `verifySemanticConsistency("", "")` dá falso, `utilityDelta = −1,0`, e **toda** mutação é rejeitada, em toda geração; o laço nunca termina (só
  sai por exceção) e nunca muda o código (categórica)
- **(c)** com o defeito do separador corrigido (JSON compacto), o exemplo do texto (`x + y`) vira `x * y`, recebe utilityDelta = (42 div 4)/(2 + 1) − 0,5 = 10/3 − 0,5 = **2,8333** e é aprovado; e o
  laço chega a um **ponto fixo na geração 1**: o comentário "# Verified by Java ASI" que o núcleo acrescenta some na próxima passagem pela árvore sintática (`ast.unparse` não guarda comentários),
  e a mutação de `x * y` não muda nada. Número de códigos distintos depois da geração 1: **1** (categórica)

**A "prova de utilidade de Gödel", medida nas funções deste projeto.** Cada função de primeiro nível do `calculos.py` como "hipótese", mutada pela regra do texto (todo `+` vira `*`) e avaliada
pela fórmula do núcleo (tokens = comprimento div 4; utilidade = tokens/(linhas + 1) − 0,5 > 0), com o defeito do separador corrigido.
- **(d)** a fração das funções que o núcleo **aprova** em **[0,95; 1,00]** (linhas de ~40 a 100 caracteres dão ~10 a 25 tokens por linha, muito acima de 0,5)
- **(e)** a fração das funções cujo comportamento a mutação **muda** (as que têm pelo menos um `+` binário) em **[0,55; 0,90]**

**Medido (a) a (e):** (a) os dois campos não são achados ✅; (b) rejeitada em toda geração, delta −1,0, o código não muda ✅; (c) com o separador corrigido, delta **2,8333**, aprovado, e **1** código
distinto depois da geração 1 (o ponto fixo) ✅; (d) **584 de 584** funções aprovadas ✅; (e) **288 de 584 = 0,493** mudadas pela mutação ❌ (0,057 abaixo do piso; não é surpresa).

**Previsão nova, nascida de (e), registrada antes de medir.** A faixa de (e) veio de uma impressão do estilo do código, e o `calculos.py` deu 0,493. Mundo novo, pela regra escrita antes: as funções
e os métodos de todos os arquivos `synthai/*.py` que não são testes. Centro: a medida do `calculos.py`; a largura cobre a diferença de estilo entre um arquivo de contas e um pacote de agentes.
- **(f)** a fração das funções e métodos do `synthai/` (fora os testes) com pelo menos um `+` binário em **[0,35; 0,65]**
- **(g)** a fração deles que o núcleo aprova depois da mutação em **[0,95; 1,00]**
