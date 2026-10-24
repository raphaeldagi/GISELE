# Parte 147 — Dois módulos recebidos, juntos: a GRPO no jogo de palavras do dicionário

↩ Nasce da Parte 137 (a GRPO de `rl_grupos.py`, num bandido) e da Parte 111 (o jogo de palavras de `word_rl_lab`, com Q-learning). O pedido
"use tudo que enviei em cada módulo" pede também a combinação: a GRPO como aprendiz no jogo do dicionário.

## O recolhimento do contêiner, de novo
Este despertar (22h50) veio depois de cerca de 62 minutos de ociosidade, e o contêiner estava "up 0 min". É o 5º lote a favor da hipótese
da Parte 145, e o primeiro registrado com a condição escrita: o contêiner é recolhido quando a sessão fica ociosa por algum tempo.

## O desenho
`synthai/grpo_palavras.py`: uma política softmax tabular por prefixo. Cada grupo são G episódios na MESMA grade e com o MESMO início (o
"mesmo enunciado" da GRPO). A vantagem vem da Parte 137, e o passo é o gradiente REINFORCE de log π. Não há crítico nem tabela de valor.
O ambiente, as ações, a recompensa e o avaliador são os de `synthai.palavras_rl`, reusados.

**O caso mínimo, rodado antes (regra da Parte 84),** com as sementes 5 e 6:
- com 1.000 episódios: Q-learning 0,018 e 0,016 de palavras válidas no avaliador guloso; GRPO 0,04 a 0,096;
- com 5.000 episódios (sementes 5, 6 e 7): Q-learning média 0,162 (desvio 0,015), GRPO com G = 2 média 0,168 (0,018) e GRPO com G = 8
  média 0,195 (0,034); grupos sem contraste 0,984 (G = 2) e 0,932 (G = 8).

**O mecanismo, escrito antes:** quase todo grupo é só de fracassos (recompensa −1 em todos) e não tem contraste. Mas um grupo com UM acerto
em G dá ao acerto a vantagem √(G − 1): √7 = 2,65 para G = 8. A GRPO aprende só com os raros acertos, e com força. O Q-learning aprende com
todos os passos, devagar. Com poucos episódios, a força dos raros acertos ganha; com muitos, os dois se aproximam.

**O teste:** as sementes 43, 44 e 45, que não aparecem na calibração nem na Parte 111 (a 42, cujo Q-learning deu 0,130 na Parte 111, ficaria
contaminada). São 5.000 episódios, avaliação de 1.000, e a medida é a média das três sementes.

## Previsões, registradas antes de qualquer execução do caso de teste
A faixa de cada média de três sementes é 1,645·√(desvio²/3 + desvio²/3)·1,36, isto é, o erro do centro mais o da medida.

**Procedência:**
- forma fechada binomial: (d), (e);
- calibração: (a), (b), (c), (f).

O centro de "quantos erros" é 2 × 0,10 + 4 × 0,25 = 1,2.

- **(a)** Q-learning, média das três sementes, em **[0,135; 0,188]**
- **(b)** GRPO com G = 2 em **[0,136; 0,200]**
- **(c)** GRPO com G = 8 em **[0,133; 0,257]**
- **(d)** fração de grupos sem contraste com G = 2 em **[0,9815; 0,9873]**. O binomial com 2.500 grupos dá desvio 0,0025 por semente, 0,0014 na média
  de três, e o erro do centro é 0,0010; 1,645·√(0,0014² + 0,0010²).
- **(e)** fração de grupos sem contraste com G = 8 em **[0,912; 0,953]**. O binomial com 625 grupos dá 0,010 por semente; o mesmo cálculo,
  vezes 1,36 pela dispersão entre sementes, que é maior que a binomial.
- **(f)** GRPO com G = 8 menos Q-learning em **[−0,051; 0,118]**. A diferença na calibração foi 0,0333 ± 0,0463. A faixa cruza o zero:
  P(G = 8 > Q) ≈ Φ(0,0333/0,0378) = 0,81 (regra da Parte 145), abaixo de 0,9, então registro a diferença e não a ordem.

### Previsões sobre as previsões (m), registradas (régua: P2837)
**Regra da Parte 120.** A régua rodou sobre o rascunho. A primeira rodada deu m1 = 0, porque o arquivo se chamava `ASI_AGI_parte147.md`, sem o
tema, e a régua procura `parte147_*`. Renomeado, deu m1 = 6, m2 = 1, m3 = 0,164 e m5 = 0. E = 1,2, então m1 fica em [6; 8].
- **(m1)** nº de previsões do mundo em **[6; 8]**
- **(m2)** nº que cruzam ou tocam o zero em **[1; 2]**
- **(m3)** mediana de w em **[0,13; 0,20]**
- **(m4)** fração de acertos em **[0,67; 1,00]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, com centro 1,2.

➡ Anterior: [Parte 146](ASI_AGI_parte146_volta10.md).
➡ Próxima: [Parte 148](ASI_AGI_parte148_grpo_dicionario_grande.md).

## Medido (P3198; sementes 43 a 45)
- **(a)** Q-learning: 0,1533. ✅
- **(b)** GRPO com G = 2: **0,2017**. ❌ (acima do teto 0,200 por 0,0017)
- **(c)** GRPO com G = 8: 0,1707. ✅
- **(d)** sem contraste com G = 2: **0,9795**. ❌
- **(e)** sem contraste com G = 8: 0,9376. ✅
- **(f)** G = 8 − Q: +0,0173. ✅

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ❌ (e) ✅ (f) ✅

**Mundo: 4 de 6.** **Sobre mim:** 2 erros, em [0; 3]: ✅.

### Os dois erros são um só, e o segundo é um erro de procedência
Nas sementes de teste, a GRPO com G = 2 aprendeu mais que na calibração (0,2017 contra 0,168). Uma política que acha mais palavras forma mais
grupos com contraste, e a fração sem contraste cai: (d) desceu junto com a subida de (b). Os dois erros vêm do mesmo fato e não são
independentes.

O erro de método está em (d). Chamei a faixa de "forma fechada binomial", mas o p de um grupo sem contraste, p^G + (1 − p)^G com p = a
chance de acertar, depende da POLÍTICA APRENDIDA, que varia de semente para semente. O binomial dá só a variância do sorteio com p fixo;
a variância do aprendizado ficou de fora. Pela calibração (desvio 0,0017 entre sementes, contra 0,0025 do binomial por semente), as duas
pareciam iguais, mas três sementes não medem um desvio.

**Regra (Parte 147):** uma proporção cujo p depende de algo aprendido NÃO é forma fechada. A faixa soma a variância do sorteio e a do
aprendizado, e tem procedência "calibração", com o fator 1,36.

### O que a medida diz sobre os dois métodos
Com o mesmo número de episódios (5.000), a GRPO, sem crítico e sem tabela de valor, empata com o Q-learning ou ganha dele: G = 8 ficou +0,017
acima, e G = 2 +0,048. Isso com 94% a 98% dos grupos sem contraste, isto é, aprendendo com 2% a 6% dos episódios. A conta do mecanismo: um
grupo com um acerto em G dá ao acerto a vantagem √(G − 1), e todo o sinal de aprendizado vem desses grupos raros. Isso se viu em 2 lotes (a
calibração e o teste): a GRPO ganhou com 1.000 episódios nas duas sementes e empatou ou ganhou com 5.000 nas seis.

## Engenharia reversa
- **O padrão: chamar de "forma fechada" uma conta que tem uma parte aprendida dentro.** É a mesma família de erro da Parte 138 (juntar a
  dispersão de duas condições): eu atribuo ao sorteio uma variância que também vem do treino. A Parte 137 tinha a mesma estrutura (os grupos
  sem contraste da GRPO no bandido), e lá a faixa larga de calibração acertou. Aqui a binomial estreita errou.
- **Regra:** antes de dar procedência "forma fechada", perguntar se TODOS os parâmetros da fórmula são fixos ou se algum é aprendido.

## Funções e testes
- **Funções:** `p3198_grpo_no_jogo_de_palavras` e `_parte_147`. Entrada P3198 na regressão.
- **Módulo:** `synthai/grpo_palavras.py`, que reusa a vantagem da Parte 137 e o ambiente e o avaliador da Parte 111.
- **Testes:** `synthai/testes_parte147.py`.

**O placar (m):** m1 = 6 em [6; 8] ✅, m2 = 1 em [1; 2] ✅, m3 = 0,164 em [0,13; 0,20] ✅, **m4 = 0,667 em [0,67; 1,00] ❌** (4/6 = 0,6667, abaixo do
piso por 0,003), m5 = 0 ✅ e m6 = 0 ✅ (os dois erros foram menores que as larguras). **5 de 6.** O piso 0,67 de m4 era o de "no máximo 2 erros
em 6", e 2 erros dão exatamente 0,6667: a faixa em fração tinha de ser escrita como contagem (4 a 6 acertos), não arredondada para cima.
