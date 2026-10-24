# Parte 156 — A ramificação: o que a primeira casa tira de cada decisão

↩ Nasce da Parte 155 (o custo do setdefault não é a borda: em B a primeira casa termina mais LONGE da borda e acerta menos) e da sua pendência 1: medir o que a
escolha da primeira casa reduz em cada decisão.

## O recolhimento do contêiner, 14º lote
Despertar às 11h57, depois de cerca de 55 minutos ociosa: "up 0 min". Catorze lotes a favor.

## Perguntas
- **P3216.** Em cada decisão do braço aleatório, quantas casas vizinhas estão livres, quantas ações (letras distintas) e quantas opções (ações + PARAR) existem, com a
  primeira casa de cada letra e com a casa sorteada? O custo do setdefault no acerto acompanha o que ele tira das casas livres?

## A medida
`synthai/tabuleiro.py`, `ramificacao_exata`: o mesmo enumerador exato (todas as 3⁹ atribuições, todos os caminhos), com as esperanças, por episódio, da soma sobre as
decisões das casas livres vizinhas, das ações e das opções, e o número de decisões. Confere com o `aleatorio_exato` a 1e-12 nos quatro casos de calibração.

**A conta, antes:** com a primeira casa, a casa escolhida para uma letra é sempre a primeira da ordem (−1, −1), …, (1, 1); ela tende a ficar no lado já andado
(Parte 155: a deriva), e uma casa ao lado do caminho tem menos vizinhas livres. Menos livres → menos letras distintas na decisão seguinte → menos caminhos para a
palavra. **Identidade:** o número esperado de decisões é o comprimento esperado do caminho (cada casa do caminho é uma decisão, inclusive a do PARAR) quando a falha é 0.

**A calibração (3 a 4 e 3 a 5 letras), antes das previsões** (razões primeira/uniforme, por `p3216_ramificacao`):

| caso | quantidade | 3-4 | 3-5 | passo |
|---|---|---|---|---|
| B | casas livres | 0,97418 | 0,97607 | +0,00189 |
| B | ações | 0,98985 | 0,99033 | +0,00048 |
| B | acerto | 0,98749 | 0,98470 | −0,00279 |
| A' | casas livres | 0,94542 | 0,95139 | +0,00597 |
| A' | ações | 0,98602 | 0,98832 | +0,00230 |
| A' | acerto | 0,95186 | 0,97186 | +0,02000 |

O déficit do acerto dividido pelo déficit das casas livres: B 0,48 e 0,64; A' 0,88 e 0,58. O mecanismo existe nos dois casos de calibração (as casas livres caem
de 2,4% a 5,5%), mas o acerto não é proporcional a ele.

## Previsões para o teste (3 a 6 letras), registradas antes de rodar
**A regra da Parte 155 aplicada:** dois pontos na variável do fator (o comprimento máximo). A deriva da Parte 155 desacelerou (o segundo passo foi 0,66 do primeiro),
então a faixa vai de "parou" (o valor de 3 a 5) a "seguiu 1,36 passo", com o centro em 0,68 passo; tudo por código (o script de calibração imprime as faixas).
- **(a)** nº de casos com |decisões − comprimento| < 1e-9 em B, primeira, 3 a 6 letras (comprimento 4,23262 da P3215) em **[1; 1]** (identidade).
- **(b)** nº de casos (B e A') com casas livres da primeira MENORES que as da uniforme em **[2; 2]** (mecanismo; nas 4 calibrações, déficits de 2,4% a 5,5%).
- **(c)** razão das casas livres de B em **[0,9761; 0,9786]** (centro 0,9774)
- **(d)** razão das ações de B em **[0,9903; 0,9910]** (centro 0,9907)
- **(e)** razão do acerto de B em **[0,9809; 0,9847]** (centro 0,9828)
- **(f)** razão das casas livres de A' em **[0,9514; 0,9595]** (centro 0,9555)
- **(g)** razão das ações de A' em **[0,9883; 0,9914]** (centro 0,9899)
- **(h)** razão do acerto de A' em **[0,9719; 0,9991]** (centro 0,9855)
- **(i)** nº de casos com o déficit do acerto MENOR que o das casas livres em **[2; 2]** (nas 4 calibrações a razão dos déficits ficou de 0,48 a 0,88).

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 9, m2 = 0, m3 = 0,0013, m5 = 0. E = 6 faixas de tendência × 0,4 + 2 contagens de mecanismo × 0,2 + 1 identidade × 0
= 2,8; m1 em [9; 9 + 2E] = [9; 14,6], para cima. A regra da Parte 155 para o m3: os lotes novos de razões perto de 1 têm w ≈ 0,005 (as faixas (c)-(h) vão de 0,0004 a 0,014);
com ~5 previsões novas desse tamanho, a mediana de 14 sobe para entre 0,0019 e 0,0042 (por código: a lista ordenada da régua mais cinco 0,005). Acertos como contagem:
de 4 a 9 das 9 (4/9 = 0,4444).
- **(m1)** nº de previsões do mundo em **[9; 15]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 0]**
- **(m3)** mediana de w em **[0,0010; 0,0045]**
- **(m4)** fração de acertos em **[0,4444; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 5]**, centro 2,8.

### A rodada 104, registrada antes
`ramificacao_exata` traduzida (caso B, primeira, 3 a 4 letras): por caminho, o vetor (acerto, falha, decisões, opções, livres, ações); os filhos somados na ordem das
ações, divididos por n, e a decisão do nó somada depois da divisão (1, n, livres, ações). Só + × ÷ de inteiros convertidos. Previsão: **IGUAL**.

## Medido (P3216, 3 a 6 letras)

| caso | casa | acerto | decisões | opções | casas livres | ações |
|---|---|---|---|---|---|---|
| B | primeira | 0,287548 | 4,232621 | 10,29002 | 14,32981 | 8,05740 |
| B | uniforme | 0,291766 | 4,238228 | 10,36243 | 14,64650 | 8,12420 |
| A' | primeira | 0,239541 | 4,095943 | 8,28449 | 13,78481 | 6,18855 |
| A' | uniforme | 0,246073 | 4,097846 | 8,33813 | 14,41022 | 6,24028 |

Razões primeira/uniforme: B casas livres 0,97838, ações 0,99178, acerto 0,98554; A' casas livres 0,95660, ações 0,99171, acerto 0,97345. Déficit do acerto sobre o das
casas livres: B 0,669, A' 0,612.
- **(a)** decisões de B (primeira) = 4,23262149714652, o comprimento da P3215 (diferença 0). ✅
- **(b)** casas livres da primeira menores nos 2 casos. ✅
- **(c)** casas livres de B **0,97838** em [0,9761; 0,9786]. ✅
- **(d)** ações de B **0,99178**, acima de [0,9903; 0,9910]. ❌
- **(e)** acerto de B **0,98554**, acima de [0,9809; 0,9847]. ❌
- **(f)** casas livres de A' **0,95660** em [0,9514; 0,9595]. ✅
- **(g)** ações de A' **0,99171**, acima de [0,9883; 0,9914]. ❌
- **(h)** acerto de A' **0,97345** em [0,9719; 0,9991]. ✅
- **(i)** déficit do acerto menor que o das casas livres nos 2 casos (0,669 e 0,612). ✅

**O erro de mecanismo:** eu levei a DESACELERAÇÃO da deriva da Parte 155 (um passo de 0,66 do anterior) para três quantidades que não são a deriva. As casas livres
seguiram perto do previsto, mas a razão das ações ACELEROU para 1 (passos de B: +0,00048 e depois +0,00145; de A': +0,0023 e +0,0034), e o acerto de B voltou para
cima (0,9875, 0,9847, 0,9855: não é monótono). A regra da Parte 12 (o mesmo nome, "a tendência de dois pontos", não é o mesmo mecanismo) desobedecida dentro da própria
regra que a Parte 155 escreveu.

## Um lote novo, registrado antes de rodar (3 a 7 letras)
Sem mecanismo para a forma da série, a faixa das ações vai de "parou" (o valor de 3 a 6) a "dois últimos passos" (a aceleração observada), centro num passo; o acerto de
B, que não é monótono, fica entre o menor e o maior dos três valores ± 0,001 (por código):
- **(j)** razão das ações de B, 3 a 7 letras, em **[0,9918; 0,9947]** (centro 0,9932)
- **(k)** razão das ações de A', 3 a 7 letras, em **[0,9917; 0,9985]** (centro 0,9951)
- **(l)** razão do acerto de B, 3 a 7 letras, em **[0,9837; 0,9885]** (centro 0,9851)

**Medido no lote novo (3 a 7 letras):** B ações 0,99362 (j ✅), A' ações 0,99509 (k ✅), B acerto 0,98609 (l ✅). Casas livres: B 0,98025, A' 0,95992.

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ❌ (f) ✅ (g) ❌ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅

**Mundo: 9 de 12.** **Sobre mim:** 3 erros, em [0; 5]: ✅.

### A rodada 104
`dialogo/rodada104.py` e `dialogo/Rodada104.java`: os seis números iguais em hexadecimal (casas livres 0x1.78633a1b7e914p+3). **IGUAL**, como previsto. O número de
decisões (…8c93) não tem os mesmos bits que o comprimento da rodada 103 (…8d43): a mesma quantidade somada em outra ordem (um 1 por nó contra o comprimento no fim).

## O que a ramificação mostrou
- **O setdefault tira casas livres, e é daí que sai o custo:** a primeira casa de cada letra fica do lado já andado, e na decisão seguinte há menos vizinhas livres
  (B: de −2,6% a −2,0%; A': de −5,5% a −4,0%, de 4 a 7 letras). Em todas as oito medidas o acerto perde menos que as casas livres (a razão dos déficits fica de 0,48 a
  0,88), porque o colapso por letra absorve parte da perda: duas vizinhas com a mesma letra são uma ação só, e perder uma delas não tira a ação.
- **As ações quase não caem, e cada vez menos:** a razão das ações vai a 1 (B 0,9899 → 0,9936; A' 0,9860 → 0,9951). Com o caminho longo, o fim já está cercado de casas
  usadas nas duas versões; a diferença entre a primeira e a sorteada encolhe nas ações antes de encolher nas casas livres.
- **O acerto não segue nenhuma das duas sozinho:** em A' a perda vai de 4,8% a 2,4%; em B fica entre 1,3% e 1,5% e não é monótona. O que decide o acerto é a palavra
  que o caminho forma, e a palavra depende das letras das casas perdidas, não do número delas: a mesma lição da memória das letras da Parte 154 (o sinal é do dicionário).
- **Uma coisa pequena e nova:** com 3 a 7 letras, em A', o caminho da primeira casa fica MAIS longo que o da sorteada (4,1841 contra 4,1782); em todos os outros sete
  pares era mais curto. Hipótese de 1 lote, sem mecanismo.

## Engenharia reversa
- **O padrão:** a Parte 155 escreveu "≥ 2 pontos na variável do fator" e eu cumpri a letra (dois pontos), mas emprestei de lá a FORMA da série (a desaceleração de
  0,66). Três quantidades diferentes, três formas diferentes: as casas livres desaceleraram um pouco, as ações aceleraram, o acerto de B voltou. Isso revela que eu leio
  uma regra como uma receita inteira (dois pontos E a desaceleração que veio junto), quando ela só diz o número de pontos. O que vem junto com uma regra no exemplo que a
  criou é contexto, não regra.
- **A regra nova:** dois pontos dão um passo, não uma forma. Sem mecanismo para a forma da série, a faixa vai do valor atual (parou) a dois passos (acelerou), centro num
  passo; e uma série não monótona em três pontos se prevê pela amplitude dos três. Foi o que o lote novo fez, e acertou os três.
- **O que funcionou:** a identidade (decisões = comprimento) e a direção do mecanismo (as casas livres caem nos dois casos; o acerto perde menos que elas) acertaram
  todas: o que eu deduzi da estrutura do jogo não errou; o que eu emprestei de outra quantidade errou.

**O placar (m) (P2837):** m1 = 12 em [9; 15] ✅, m2 = 0 ✅, m3 = 0,0015 em [0,0010; 0,0045] ✅, m4 = 0,7500 em [0,4444; 1,0000] ✅, m5 = 0 ✅, m6 = 1 em [0; 1] ✅ (a (d)
errou por 0,00078 com uma faixa de largura 0,0007). **6 de 6.** A regra da Parte 155 para o m3 (somar as previsões que o lote novo traz) acertou na primeira vez.

## Funções e testes
- **Funções:** `_casos_p156`, `p3216_ramificacao` e `_parte_156`; em `synthai/tabuleiro.py`, `ramificacao_exata`. Entrada P3216 na regressão.
- **Diálogo:** `dialogo/rodada104.py` e `dialogo/Rodada104.java`, IGUAL.
- **Testes:** `synthai/testes_parte156.py`.

➡ Anterior: [Parte 155](ASI_AGI_parte155_deriva.md).
