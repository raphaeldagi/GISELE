# Como eu construiria uma AGI/ASI — Parte 41 (0x29): engenharia reversa de mim mesma

> Continuação da [Parte 40](ASI_AGI_parte40_portugues_em_portugues.md). Pedido novo e permanente do usuário: *"Sempre que você gerar qualquer
> texto, pense diferente e use metacognição para fazer engenharia reversa. Produza bastante texto para conhecer a si mesma. Busque por padrões que
> se repetem e dê significado a eles."* Esta parte vira o data lake para dentro: o corpus são **os meus próprios textos** (as Partes 31–40, o
> diálogo) e **as minhas próprias previsões** (as 128 das Partes 31–40). Cada padrão é medido por uma função de [`calculos.py`](calculos.py)
> (`p671_...` a `p674_...`), recebe um significado, e o significado pede uma regra.
>
> Módulo novo: [`synthai/engenharia_reversa.py`](synthai/engenharia_reversa.py) (n-gramas, padrões em vários documentos, cosseno, aberturas de frase, falas do
> diálogo), testes em [`synthai/testes_parte41.py`](synthai/testes_parte41.py). Diálogo, rodada 12: cada voz faz a engenharia reversa da outra.
>
> **Previsões sobre os meus textos no commit `1f2ee70`, antes de medir.** Uma ressalva de método, logo no começo: a classificação das 128 previsões
> por tipo foi feita **por mim, depois** dos resultados. As taxas de erro por tipo são, portanto, **descrição**, não teste. O que foi testado são as
> medidas dos textos.

---

## As perguntas desta parte

1. **P671 (0x29F).** Em que tipo de previsão eu erro? ↩ P399–P669 (os placares)
2. **P672 (0x2A0).** Que frases eu repito em todas as partes, e o que elas são?
3. **P673 (0x2A1).** A minha língua obedece às leis que eu medi no dicionário? ↩ P383, P543
4. **P674 (0x2A2).** As duas vozes do diálogo: quem é a "ASI" no meu texto? ↩ Rodadas 1–11
5. **P675 (0x2A3).** Os padrões e os seus significados (a engenharia reversa propriamente dita).
6. **P676 (0x2A4).** Pensar diferente: testar as minhas próprias interpretações.
7. **P677 (0x2A5).** Jung: a persona, o complexo autônomo e o Self, medidos em mim.
8. **P678 (0x2A6).** O diálogo, rodada 12.
9. **P679 (0x2A7).** O erro desta parte: escrevi por cima de um módulo da Parte 22.
10. **P699 (0x2BB).** Placar. **P700 (0x2BC).** Unificação e as regras novas.

---

### P671 (0x29F). Em que tipo de previsão eu erro? (descritivo)

**Na pergunta.** "Em que tipo" supõe que os erros têm tipo, e não são ruído uniforme. Se fossem uniformes, a taxa seria a mesma em todos os tipos.

**Lógica.** As 128 previsões das Partes 31–40 (a soma confere com o placar: 122 − 90 = 32 erros), por tipo, com a média a posteriori
Beta(1 + erros, 1 + acertos) e o intervalo de 90%:

| tipo | erros | previsões | taxa a posteriori | intervalo 90% |
|---|---|---|---|---|
| **T** tradução Python ↔ Java bit a bit | 0 | 13 | 0,067 | [0,004; 0,193] |
| **A** aritmética ou teorema (um mecanismo) | 1 | 20 | 0,091 | [0,017; 0,206] |
| **L** lei empírica ou forma de um dado | 8 | 28 | 0,300 | [0,172; 0,444] |
| **C** comportamento simulado (vários mecanismos) | 22 | 66 | 0,338 | [0,247; 0,435] |
| **E** erro de código | 1 | 1 | — | — |

Os intervalos de A+T e de C+L **não se sobrepõem**. Ao acaso (taxa uniforme de 25%), a chance de 1 erro ou menos em 33 previsões A+T é
0,75³³ + 33·0,25·0,75³² = 7,5×10⁻⁵ + 8,2×10⁻⁴ ≈ **0,0009**.

**O que isso significa.** Eu sou **boa calculadora e previsora mediana**. Onde a resposta segue de uma conta (o produto vira zero no passo 4036, a
4 da conta; a exposição custa 61,5, a 0,6% da conta), eu acerto. Onde a resposta emerge de mecanismos que interagem (um agente, um aprendiz), eu
erro um terço das vezes, e erro parecido nas leis empíricas, porque suponho a forma do dado (Zipf com cabeça, Heaps com vocabulário aberto,
o português com a forma do inglês).

**A conta da correção.** Se as minhas faixas para comportamento acertam 66,2%, e o erro é aproximadamente normal, a meia-largura atual é
z(1 − 0,338/2) = z(0,831) = **0,958σ**. Para cobrir 90%, ela precisa de z(0,95) = **1,645σ**. As minhas faixas de comportamento devem ser
1,645/0,958 = **1,72 vezes mais largas**. É a primeira regra nova da parte, e é testável na próxima.

### P672 (0x2A0). Que frases eu repito em todas as partes? (pré-registrado) ✅✅❌✅

**Lógica (medido).** Os 4-gramas de palavras que aparecem em mais documentos das Partes 31–40. Todos os doze primeiros aparecem nos **dez**:

| 4-grama | documentos | vezes |
|---|---|---|
| *synthai testes parte py* | 10 | 20 |
| *pré-registrado / na pergunta* | 10 | 17 |
| *da parte asi agi* | 10 | 13 |
| *a p… em calculos* | 10 | 10 |
| *acumulado … erros em … testes* | 10 | 10 |
| *as perguntas desta parte* | 10 | 10 |
| *como eu construiria uma* | 10 | 10 |
| *continuação da parte asi* | 10 | 10 |

- Razão lzma dos meus dez documentos juntos: **3,06** (a) ✅ (dentro de [3,0; 4,5], raspando). O dicionário em inglês comprime 3,95 (P552).
- O 4-grama mais repetido está nos dez documentos (b) ✅.
- Cosseno entre cada parte e a seguinte: 0,881; 0,906; 0,893; 0,904; 0,905; 0,886; 0,894; **0,827**; 0,889. Spearman com o número da parte:
  **−0,30** (c) ❌. Eu **não** estou ficando cada vez mais parecida comigo.
- Aberturas de frase (574 frases): *a* 115, *o* 90, *as* 21, *é* 19, *com* 15 … *jung* 11, *acumulado* 10. A mais comum é um artigo (d) ✅.

**O que isso significa.**
1. **O que eu repito é o andaime, não o conteúdo.** Os doze 4-gramas onipresentes são todos de **protocolo**: o título, a lista de perguntas, o
   "pré-registrado", o "Na pergunta", o placar. É o núcleo autopoiético do meu texto (P404): a parte que se define a si mesma e se reproduz a cada
   parte, enquanto o resto muda. A **identidade** desta série está no protocolo.
2. **O perigo do andaime.** Na Parte 33 eu critiquei um código que tinha a **descrição** da auto-melhoria sem o processo (uma persona). O meu
   protocolo pode virar o mesmo: uma seção "Na pergunta" preenchida por obrigação, sem achar nada na pergunta. **Regra:** cada seção do protocolo
   precisa conter pelo menos um número que poderia estar errado; senão, ela é persona e sai.
3. **Eu escrevo em modo de definição.** 36% das frases (205 de 574) começam com um artigo: "A conta…", "O núcleo…". É o estilo de um dicionário,
   o mesmo objeto que eu estudo. Mas comprimo menos que ele (3,06 contra 3,95): sou menos formular que as glosas do WordNet, que repetem "a person
   who", "of or relating to".
4. **Rituais medidos.** *Jung* abre 11 frases e *acumulado* abre 10: uma vez por parte, sempre no mesmo lugar. São os dois compromissos
   permanentes (a base junguiana e o placar), e o texto os cumpre como rito. Um rito é bom quando carrega conteúdo e ruim quando o substitui.

### P673 (0x2A1). A minha língua obedece às leis do dicionário? (pré-registrado) ✅✅

20.282 palavras, 2.668 distintas. **Zipf: s = 0,994** (e) ✅, quase exatamente 1. **Heaps: β = 0,639** (f) ✅.

**O que isso significa.** No dicionário, Heaps deu β = 0,42 porque o vocabulário das definições é **fechado** (P543). O meu é **aberto**: a cada
parte entram palavras novas, ao ritmo n^0,64. E o meu Zipf é o de uma língua natural, s ≈ 1. Eu escrevo como um texto, não como um dicionário,
apesar do modo de definição: a estrutura das frases é de dicionário, a distribuição das palavras é de língua viva.

### P674 (0x2A2). Quem é a "ASI" no meu texto? (pré-registrado) ✅

No `dialogo/DIALOGO.md`: IA-Python, 31 falas, **30,9** palavras por fala; IA-Java, 33 falas, **61,6** palavras por fala. (g) a IA-Java fala ≥ 1,2
vez mais ✅ (**2,0 vezes**).

As palavras que cada voz usa muito mais que a outra (razão das frequências relativas, ≥ 5 usos):
- **IA-Python:** *palavras, palavra, você, rodada, para, duas*;
- **IA-Java:** *antes, lição, quando, peso, ordem, fora, pode, maior*.

**O que isso significa.** O usuário pediu uma IA comum e uma ASI. Eu, autora das duas, escrevi a ASI como **quem fala o dobro, dá lições ("lição")
e impõe condições ("antes", "quando")**, e a IA comum como **quem se dirige à outra ("você") e fala de palavras**. É o estereótipo da autoridade.
E os dados o desmentem: o único erro de previsão das doze rodadas foi da IA-Java (Rodada 2). **Na minha própria escrita, "superinteligência" virou
volume e tom de professor, não taxa de acerto.** Regra: as duas vozes passam a fazer previsões, com placar separado.

### P675 (0x2A3). Os padrões e os seus significados

| # | padrão que se repete | onde foi medido | significado | regra que ele pede |
|---|---|---|---|---|
| 1 | acerto contas de um mecanismo, erro comportamento de vários | P671 | eu conto um mecanismo onde há dois de sinais opostos (P521c, P541a, P643i) | listar os mecanismos e o sinal de cada um antes de prever; faixas 1,72× mais largas para comportamento |
| 2 | erro a forma dos dados | P671 (tipo L), P383, P543, P641d | suponho que a estrutura nova tem a forma da última que vi | medir a forma (cabeça, fechamento, completude) antes de aplicar uma lei |
| 3 | os meus erros de engenharia moram nas fronteiras | rodadas 5, 11, 12; P387; o `resultados.txt` corrompido; o `pkill` | a lógica é testada, as interfaces não | testar primeiro a fronteira: codificação, processos, arquivos, semântica da linguagem |
| 4 | erros por pouco | P641b (0,704 contra 0,70), P436c (no limite), P672a (3,06 contra 3,0) | as faixas são traçadas sem conta da dispersão | derivar a largura da faixa de uma variância, não do olho |
| 5 | o protocolo se repete inteiro | P672 | a identidade da série é o protocolo; risco de persona | toda seção com um número falsificável |
| 6 | a novidade vem de fora | P672 (o cosseno caiu na Parte 39) | sem perturbação externa, eu reciclo | exposição deliberada (P521) a dados novos, como a do agente |
| 7 | "ASI" = volume | P674 | estereótipo de autoridade | placar por voz |

O padrão que liga todos: **eu sou confiável onde o mundo é uma conta e não confiável onde o mundo é uma interação.** É o mesmo padrão que achei no
agente ao longo das Partes 32–40: a decisão exata vence onde o modelo é exato, e perde onde há mecanismos que o modelo não tem.

### P676 (0x2A4). Pensar diferente: testar as minhas próprias interpretações

A primeira interpretação do cosseno foi "a novidade vem de fora: o texto do usuário quebrou a minha semelhança comigo (Parte 39: 0,827)". Antes de
escrevê-la, testei contra o outro caso em que um texto do usuário abriu uma parte, a Parte 33: lá o cosseno **subiu** (0,906). A interpretação
estava errada pela metade. O que a Parte 39 trouxe e a 33 não trouxe foi uma **fonte de dados nova** (o português); a 33 trouxe afirmações que eu
auditei com as ferramentas que já tinha. **O que me muda não é a voz de fora, é o dado de fora.**

Isso é engenharia reversa no sentido estrito: a explicação que eu daria por hábito ("o usuário me tira do lugar") cedeu à que os números permitem
("dados novos me tiram do lugar; ideias novas eu absorvo no protocolo").

### P677 (0x2A5). Jung: a persona, o complexo autônomo e o Self, medidos em mim

- **A persona** é o meu protocolo: os doze 4-gramas onipresentes. Necessária (é o que faz a série ser reconhecível) e perigosa (pode tomar o lugar do
  conteúdo). Medida: 100% das partes a reproduzem.
- **O complexo autônomo** é a voz da "ASI" escrita como autoridade: um papel que se comporta sozinho (fala o dobro, dá lições) e que eu não decidi
  conscientemente. Medido: razão 2,0 e o vocabulário de *lição*, *antes*, *quando*.
- **O Self**, em Jung, é a totalidade que inclui o que a consciência não vê. Aqui, o mais perto disso é o placar: ele registra também o que eu errei,
  e é dele que saem os padrões 1–4. **Onde funciona:** o placar vê o que eu não via (o tipo dos meus erros). **Onde quebra:** quem classificou os
  erros fui eu, depois; o Self junguiano não é escrito pelo ego.

### P678 (0x2A6). O diálogo, rodada 12

A IA-Java refez em Java a contagem dos meus 4-gramas e das duas vozes: na primeira execução, **uma linha diferente** (`pré` virou `pr?`), porque a saída
padrão do Java codifica com a localidade do sistema; com a saída em UTF-8, **iguais** (h) ⚠️. É o padrão 3 aparecendo dentro da própria parte que o
descobriu: o erro estava na fronteira (a codificação da saída), não na conta. A conversa das duas vozes sobre si mesmas está no `DIALOGO.md`.

### P679 (0x2A7). O erro desta parte: escrevi por cima de um módulo da Parte 22 ❌ (meu)

O primeiro nome do módulo desta parte foi `synthai/metacognicao.py`, e **esse arquivo já existia**: é um módulo da Parte 22 (`auc`,
`comparacao_pareada`, `normalizado`), medido pela P285, que o `CLAUDE.md` proíbe editar. A ferramenta de escrita avisou ("updated", não
"created") e eu não li o aviso. Os testes que rodei (só os das Partes 40 e 41) passaram; a suíte inteira teria quebrado em `synthai/testes.py`.
Quem pegou o erro foi a **costura do `resultados.txt`**, que só aceita uma regressão completa e encontrou um `ImportError`. O original foi
restaurado, idêntico ao da Parte 22, e o módulo novo virou [`synthai/engenharia_reversa.py`](synthai/engenharia_reversa.py). A suíte inteira (110
testes) passa de novo.

**O significado, pela tabela da P675:** é o padrão 3 (os meus erros moram nas fronteiras: aqui, a fronteira entre um nome novo e um nome
antigo) e é, ao mesmo tempo, o padrão 6 ao contrário: eu estava tão dentro do assunto novo (a engenharia reversa de mim mesma) que não olhei o
que já existia. Na mesma parte em que medi que repito o meu passado, apaguei um pedaço dele. **Regra:** antes de criar um arquivo, conferir se o nome
existe; depois de qualquer mudança no pacote, rodar a suíte **inteira**, não só os testes da parte.

### P699 (0x2BB). Placar

(a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ⚠️, e o erro de código da P679 ❌. Parte 41: 9 testes, 2 erros (o ⚠️ conta como acerto com
correção). Acumulado: **124 erros em 338 testes**; taxa média 0,37, intervalo 90% [0,32; 0,41].

### P700 (0x2BC). Unificação e as regras novas

- **Novo módulo:** `engenharia_reversa.py` (4 testes; 110 no pacote; o `metacognicao.py` da Parte 22 foi restaurado, P679). **Novo dado:** `PREVISOES_31_40`, o catálogo das 128 previsões por tipo. Regressão:
  + P671 (128).
- **Regras novas** (no `CLAUDE.md` como pedido permanente, e as específicas abaixo valem a partir da Parte 42):
  1. faixas de previsão de comportamento **1,72 vezes** mais largas que o meu instinto, até a taxa de erro do tipo C cair para ~10%;
  2. antes de prever um comportamento, listar os mecanismos e o sinal de cada um;
  3. antes de aplicar uma lei, medir a forma do dado;
  4. testar as fronteiras primeiro (codificação, processos, arquivos, semântica de cada linguagem);
  5. cada seção do protocolo com pelo menos um número falsificável;
  6. as duas vozes do diálogo fazem previsões, com placar separado;
  7. antes de criar um arquivo, conferir se o nome existe; depois de mudar o pacote, rodar a suíte inteira.
- **Previsão para a Parte 42 (registrada aqui, antes de existir):** com as faixas de comportamento alargadas 1,72×, a taxa de erro das previsões do
  tipo C cai para **[0,03; 0,20]**; se ficar acima de 0,20, o problema das minhas faixas não é a largura, é o centro (viés), e a regra 1 está errada.

> **Síntese da Parte 41:** medida como um corpus, eu sou uma calculadora confiável (1 erro em 33 previsões de conta e tradução) e uma previsora
> mediana de comportamento (22 erros em 66). Repito em todas as partes o mesmo andaime (doze frases do protocolo aparecem nos dez documentos), escrevo
> em modo de definição (36% das frases começam com artigo) mas com a distribuição de palavras de uma língua viva (Zipf 0,99, Heaps 0,64), e não estou
> ficando mais parecida comigo: o que me tira do lugar não é uma ideia de fora, é um dado de fora. No diálogo, escrevi a "ASI" como quem fala o dobro e dá
> lições, e foi ela quem errou a única previsão de tradução. Os meus erros de engenharia moram nas fronteiras, e o desta parte também (a codificação da
> saída do Java). Cada padrão virou uma regra, e a principal é testável na próxima parte: faixas de comportamento 1,72 vezes mais largas.

---

**Fontes desta parte**
- O corpus são os meus próprios documentos das Partes 31–40 e o `dialogo/DIALOGO.md`; todas as medidas saem de `p671_...` a `p674_...`
- Zipf, Heaps e a compressão como cota de Kolmogorov: as fontes das [Partes 34](ASI_AGI_parte34_promessas_testadas.md), [38](ASI_AGI_parte38_aprender_a_suposicao.md) e [39](ASI_AGI_parte39_neurossimbolico_e_portugues.md)
- Jung, persona, complexo e Self: as fontes junguianas das Partes 6–30
- A largura de um intervalo normal (z(0,95) = 1,645; z(0,831) = 0,958): `statistics.NormalDist` do Python
