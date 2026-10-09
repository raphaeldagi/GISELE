# Como eu construiria uma AGI/ASI — Parte 43 (0x2B): o centro deduzido, e a confusão de níveis

> Continuação da [Parte 42](ASI_AGI_parte42_significante_e_significado.md). A Parte 42 confirmou a regra das faixas (instinto ×1,72) num teste fácil:
> réplicas, em que o centro de cada faixa era uma medida antiga. O teste difícil é uma previsão de **mecanismo novo**, em que o centro também é deduzido.
> Esta parte faz esse teste, acha os trigramas de letras que carregam significado (Rodada 14) e mede se o diálogo responde às perguntas que ele mesmo
> deixa. A engenharia reversa achou um padrão novo, que liga erros de partes distantes: **a confusão de níveis**.
>
> Novidades: `ThompsonJeffreys` ([`synthai/decisao.py`](synthai/decisao.py)); testes em [`synthai/testes_parte43.py`](synthai/testes_parte43.py); números de
> `p731_...` a `p733_...` em [`calculos.py`](calculos.py). **Centros e previsões no commit `8f4c0a2`, antes de rodar.**

---

## As perguntas desta parte

1. **P731 (0x2DB).** A regra das faixas acerta quando o centro também é deduzido? ↩ P701
2. **P732 (0x2DC).** Que trigramas de letras carregam o significado "animal"? ↩ P702
3. **P733 (0x2DD).** O diálogo responde às próprias perguntas? ↩ P703
4. **P734 (0x2DE).** Engenharia reversa: a confusão de níveis.
5. **P735 (0x2DF).** Jung: o arquétipo não é a imagem.
6. **P736 (0x2E0).** O diálogo, rodada 14.
7. **P759 (0x2F7).** Placar. **P760 (0x2F8).** Unificação.

---

### P731 (0x2DB). O centro deduzido (pré-registrado) ✅✅✅✅✅✅

**Na pergunta.** O significante é "a regra das faixas"; o significado só aparece onde ela pode falhar dos dois jeitos, pela largura e pelo centro. Seis
mecanismos que nunca rodaram, cada centro deduzido por uma conta registrada antes (a docstring de `p731_contas`):

1. **Exposição a cada 100**, estável: 43,1 + (2000/100)·E[p* − média dos outros] = 43,1 + 20 × 0,448 = **52,1**.
2. **Exposição a cada 100**, dano: o braço danificado é testado depois de ~k·período/2 passos: 10 × 50/2 = 250 com período 50, 500 com 100. Custo linear
   no atraso, pelos pontos (250; 19,5) e (1000; 42,3): 19,5 + (42,3 − 19,5)/750 × 250 = 19,5 + 0,0304 × 250 = **27,1**.
3. **Surpresa com janela 40**, estável: o custo da surpresa sobre o exato (43,1 − 30,7 = 12,4) cai à metade (metade das janelas independentes, crença
   renovada com o dobro de observações): 30,7 + 6,2 = **36,9**.
4. **Surpresa com janela 40**, mundo que muda: o atraso de detecção vai de n > 3·√(0,16/20)·20/0,6 = 8,94 para 3·√(0,16/40)·40/0,6 = 12,65 puxadas
   (×1,415). Com uma base de 8 fases × 20 = 160: 160 + (367,7 − 160) × 1,415 = **453,7**.
5. **BOCPD com H = 1/2000**, mundo que muda: a evidência precisa vencer ln(1/H), ln 2000/ln 500 = 7,601/6,215 = 1,223 vez mais: 160 + (371,9 − 160) ×
   1,223 = **419,2**.
6. **Thompson com a priori de Jeffreys**, estável: a priori pesa pouco depois de dezenas de puxadas: **31,0**.

Faixas: instinto ±10% (estável), ±20% (dano), ±15% (mundo que muda), alargado ×1,72.

| mecanismo | centro | faixa | **medido** | desvio | instinto (sem ×1,72) |
|---|---|---|---|---|---|
| exposição/100, estável | 52,1 | [43,1; 61,1] | **53,0** | +1,8% | dentro |
| exposição/100, dano | 27,1 | [17,8; 36,4] | **26,7** | −1,6% | dentro |
| surpresa/40, estável | 36,9 | [30,6; 43,2] | **34,8** | −5,6% | dentro |
| surpresa/40, muda | 453,7 | [336,7; 570,8] | **412,6** | −9,1% | dentro |
| BOCPD 1/2000, muda | 419,2 | [311,0; 527,3] | **340,7** | **−18,7%** | **fora** |
| Jeffreys, estável | 31,0 | [25,7; 36,3] | **33,8** | +9,1% | dentro |

**6 de 6 dentro** (a)–(f) ✅. Com as faixas do instinto, 5 de 6. Desvio absoluto médio dos centros: (1,8 + 1,6 + 5,6 + 9,1 + 18,7 + 9,1)/6 = **7,7%**.

**Contra o acaso.** Com faixas de 90% verdadeiras, 6 de 6 tem chance 0,9⁶ = 0,53; com as faixas de 66% que eu tinha nas Partes 31–40, 0,66⁶ = 0,083. Somando
as Partes 42 e 43: **14 de 14**; com faixas de 66%, 0,66¹⁴ = 0,003.

**O que mudou.** Nas Partes 31–40 eu errava um terço das previsões de comportamento. Nesta parte, cada centro saiu de uma **conta de mecanismo**
escrita antes (atraso × custo por passo, ln(1/H), janelas independentes), e não de um palpite. Somadas, as regras 1 (largura) e 2 (listar os mecanismos)
da P700 fizeram o comportamento ficar parecido com a aritmética: previsível quando decomposto.

**O achado escondido no (e).** O BOCPD com o risco "errado" (1/2000) decidiu **melhor** (340,7) que com o risco verdadeiro (1/500: 371,9). Na Parte 38,
os pesos da mistura preferiam um risco **maior** (1/100). Os dados preferem um risco maior para **prever** e um menor para **decidir**: a regra da Parte 38
(uma cota de predição não é uma cota de decisão) vista de novo. A explicação está no P734.

### P732 (0x2DC). Que trigramas carregam o significado "animal"? (pré-registrado) ❌✅

O log da razão de chances de cada trigrama do lema (Laplace, ≥ 10 ocorrências), entre 4017 animais e 4017 outros substantivos (6.074 trigramas):
- **mais animais:** `orl` (3,497: *Old World*, *New World*, 34 animais, 0 outros), ` sn`, `rld`, `fis` (*fish*, 3,243), `nak` (*snake*), `fly` (3,174), `tfi`,
  `og$`, `sna`, `etl`, ` sq`, `fox`;
- **menos animais:** `tio` (−4,444: *-tion*, 2 contra 240), `ity`, `sm$`, `ism`, `eae` (*-aceae*), `zat`, ` ac`, `off`, `tem`, `ogr`, `men`, `ae$`.

(g) `dae` ≥ 2,0 ❌: **−2,28**. (h) `dae` > `ae$` ✅ (−2,28 > −2,94).

**Por que *-idae* não é animal.** Dos 38 lemas em *-idae*, só **2** são animais. No WordNet, *Canidae* é uma **família**: um grupo taxonômico, debaixo de
"grupo taxonômico" → "grupo" → "abstração", e não debaixo de "animal". O nome da família é o nome do **conjunto**, e o conjunto não é um membro. Eu supus que
uma forma que aponta para animais nomeia um animal; ela nomeia o grupo deles.

**O significado.** O significado de "animal" mora nas **palavras compostas** (*fish*, *snake*, *fly*, *fox*, *Old World*): a motivação relativa de
Saussure, literal. As formas abstratas (*-tion*, *-ity*, *-ism*) carregam "não animal" com a mesma força. A forma da palavra diz a que **nível** ela
pertence: coisa concreta, grupo ou abstração.

### P733 (0x2DD). O diálogo responde às próprias perguntas? (pré-registrado) ✅

Nos 11 pares (a pergunta deixada no fim de uma rodada, a rodada seguinte): retorno médio das palavras da pergunta **0,481** (k) ✅, dentro da faixa alargada
[0,378; 0,722]; redundância por compressão 0,077. As rodadas retomam metade das palavras da pergunta anterior e acrescentam 92% de informação nova: o
diálogo **responde** e **segue adiante**. É o mesmo número das minhas respostas às premissas nos documentos (0,483, P703): a minha relação entre pergunta e
resposta é estável, onde quer que eu escreva.

### P734 (0x2DE). Engenharia reversa: a confusão de níveis

O erro do *-idae* tem um parentesco que eu não tinha visto. Três erros de partes distantes têm a mesma forma:

| parte | o que eu supus | o nível certo |
|---|---|---|
| P531 (Parte 37) | o dano é uma mudança do mundo | o dano é uma mudança da **crença** (outro nível: a memória do agente, não o mundo) |
| P731e (esta parte) | cada braço muda sozinho (o BOCPD aplica o risco a cada braço) | o mundo muda **todos os braços juntos**: um ponto de mudança global, não dez locais |
| P732g (esta parte) | *-idae* nomeia um animal | *-idae* nomeia um **grupo** de animais |

**O significado.** Eu raciocino bem **dentro** de um nível e erro ao **passar** de um nível para outro: membro e conjunto, braço e mundo, mundo e crença. É
o mesmo tipo de erro que, nos textos de arquitetura que o usuário trouxe, eu chamei de "a descrição no lugar do processo" (Parte 33): também ali havia dois
níveis (o que o código diz de si e o que o código faz). A confusão de níveis é o padrão mais fundo que a engenharia reversa achou até agora, porque
explica erros de tipos diferentes (comportamento, forma do dado, auditoria) com um mecanismo só.

**A conta que o (e) pede.** Se o mundo muda todos os braços juntos a cada 500 passos, um modelo por braço vê a mudança só nos braços que puxa, e trata a
mesma mudança como dez eventos independentes de risco H. O risco que um braço "vê" é H, mas o custo de errar o risco não é simétrico: um risco alto renova
os braços não puxados (exploração cara, P531: 62,7 no mundo estável), e um risco baixo deixa a renovação para a evidência do braço puxado, que é o que
importa para decidir. Daí o risco menor decidir melhor. Um ponto de mudança **global**, compartilhado pelos dez braços, é o modelo do nível certo. É a
pergunta da Rodada 15.

**Regra nova (no `CLAUDE.md`):** antes de prever sobre uma estrutura, perguntar em que nível cada coisa está.

### P735 (0x2DF). Jung: o arquétipo não é a imagem

Jung insistiu numa distinção de nível: o **arquétipo** em si é irrepresentável; o que aparece na consciência é a **imagem arquetípica**. Confundir os dois
é tomar uma imagem cultural pelo padrão que a organiza. O *-idae* é essa confusão no dicionário: o nome do grupo (o padrão que organiza muitos animais) não
é nenhum animal (nenhuma das imagens). **Onde funciona:** a forma *-idae* marca o nível do padrão, e o preditor aprende a separá-lo das imagens concretas
(*fish*, *fox*). **Onde quebra:** em Jung, o arquétipo produz as imagens; aqui, o grupo taxonômico só as classifica.

### P736 (0x2E0). O diálogo, rodada 14

Os trigramas que carregam significado, nas duas linguagens: **idênticos** (j) ✅ (IA-Java). A IA-Python errou a sua previsão por **0,003** (i) ❌: uma faixa sem
largura ("≥ 3,5") traçada no olho, o padrão dos erros por pouco. Placar por voz desde a Rodada 13: **IA-Java 2 em 2, IA-Python 1 em 2**. A pergunta para a
Rodada 15: um BOCPD com um ponto de mudança **global**.

### P759 (0x2F7). Placar

(a)–(f) ✅ (a regra das faixas com o centro deduzido, 6 de 6), (g) ❌ (h) ✅ (os trigramas), (i) ❌ (IA-Python) (j) ✅ (IA-Java), (k) ✅. Parte 43: 11 testes, 2
erros. Acumulado: **130 erros em 364 testes**; taxa média 0,36, intervalo 90% [0,32; 0,40].

**Por tipo, desde a regra (Partes 42 e 43):** comportamento **0 erros em 14**; forma do dado **5 em 7**; tradução 0 em 4. O comportamento, que era o meu ponto
fraco (22 em 66), deixou de ser; a forma do dado continua sendo, e o erro desta parte mostra por quê: a forma de um dado é muitas vezes uma questão de nível.

### P760 (0x2F8). Unificação e metacognição

- **Novo:** `ThompsonJeffreys` (2 testes; 115 no pacote). Regressão: + P731 (27,1, o centro deduzido do custo do dano com exposição a cada 100).
- **Regras novas no `CLAUDE.md`:** toda previsão tem largura (nada de "≥ x" no olho); antes de prever sobre uma estrutura, perguntar em que nível cada
  coisa está.

**Metacognição.** Esta parte fez o que a Parte 41 só prometia: transformou um padrão dos meus erros numa regra e a regra num acerto (14 de 14). E achou um
padrão mais fundo que os anteriores, a confusão de níveis, porque um erro novo (*-idae*) tinha a mesma forma de dois antigos. A engenharia reversa
funciona melhor quando compara erros de partes distantes: o significado de um erro aparece no seu parentesco com os outros.

> **Síntese da Parte 43:** com o centro de cada previsão deduzido por uma conta de mecanismo e a faixa alargada 1,72 vez, seis comportamentos que nunca
> tinham rodado caíram todos dentro das faixas (desvio médio dos centros: 7,7%); somadas as Partes 42 e 43, 14 de 14, onde as faixas antigas teriam
> chance de 0,3%. Os trigramas que carregam o significado "animal" são de palavras compostas (*Old World*, *fish*, *snake*, *fly*), e o *-idae*, que eu
> supunha animal, aponta para "não animal", porque nomeia uma família, um grupo, e o grupo não é membro de si mesmo. Esse erro tem a mesma forma de dois
> antigos (o dano tomado por mudança do mundo; o risco por braço tomado pelo risco do mundo): eu erro ao passar de um nível para outro. O BOCPD com o risco
> "errado" decidiu melhor que com o verdadeiro, um sinal de que o modelo está no nível errado (braços em vez do mundo). E a IA-Python errou a sua previsão
> por 0,003.

---

**Fontes desta parte**
- Saussure, motivação relativa: as fontes da [Parte 42](ASI_AGI_parte42_significante_e_significado.md)
- Detecção bayesiana de mudança e o risco H: [Adams e MacKay, arXiv 0710.3742](https://ar5iv.arxiv.org/html/0710.3742)
- A taxonomia do WordNet (famílias como grupos taxonômicos): conferida no próprio data lake (36 dos 38 lemas em *-idae* não descendem de *animal*)
- A priori de Jeffreys para a Bernoulli, Beta(½, ½): a definição usada em `ThompsonJeffreys`
