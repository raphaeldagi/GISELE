# Parte 143 — Os testes da Parte 140 num segundo mundo (o português e outras potências), e a memória congelada bit a bit

↩ Nasce da Parte 140, cujos resultados vieram de um lote só: o reservatório só tinha sido medido no WordNet inglês, e Benford-16 só em 3ⁿ.
Pela regra da Parte 66, um efeito visto num lote é hipótese até se replicar. Nasce também da pendência da rodada 94.

## Perguntas
**O dicionário em português.** As 53.058 glosas da OpenWordNet-PT (CC BY 4.0), na ordem do arquivo, com as vazias contando 0 palavras,
num reservatório de 500 (`synthai/reservatorio.py`), 300 vezes:
- **(a)** O desvio das 300 médias é o da amostra sem reposição?
- **(b)** A média das médias é não viesada?
- **(c)** A fração da amostra vinda da primeira metade do arquivo é ½?

**O hexadecimal**, à parte do dicionário:
- **(d)** O posto efetivo dos bits do primeiro dígito hexadecimal de 5ⁿ, n = 1 a 5.000, é o de Benford-16?
- **(e)** E o de 7ⁿ?
- **(f)** O de 2ⁿ, cujo primeiro dígito hexadecimal percorre o ciclo 2, 4, 8, 1, é exatamente 3?

**O diálogo (rodada 94).** O retrocesso e a memória congelada de `synthai/memoria_congelada.py` atravessam o Java bit a bit?
- **(g)** a rodada 94 é IGUAL?
- **(h)** a razão de custo da tradução contra a do módulo, nas mesmas tarefas, difere menos de 1e-12?

## Previsões, registradas antes de qualquer execução
**Procedência:**
- identidades: (f), (h);
- forma fechada: (a) a (e);
- mecanismo: (g).

O centro de "quantos erros" é 0 + 0,10 × 5 + 0,25 × 1 = 0,75.

- **(a)** razão dos desvios em **[0,933; 1,067]**. O desvio relativo de um desvio-padrão de 300 amostras é 1/√598 = 0,041, vezes 1,645.
- **(b)** z da média das médias em **[−1,645; 1,645]**.
- **(c)** fração da primeira metade em **[0,4979; 0,5021]**. N = 53.058 é par, então p = ½ exato; ½ ± 1,645·√(¼·(N − 500)/(N − 1)/500)/√300.
- **(d)** \|posto de 5ⁿ − Benford-16\| em **[0; 0,01]**. log₁₆ 5 é irracional; a discrepância é da ordem de log N/N.
- **(e)** \|posto de 7ⁿ − Benford-16\| em **[0; 0,01]**. Idem.
- **(f)** posto de 2ⁿ em **[2,999999999; 3,000000001]**. Identidade: em 5.000 = 4 × 1.250 potências, os dígitos 2, 4, 8 e 1 aparecem 1.250 vezes
  cada. Os bits são one-hot de 4 com probabilidade ¼, e a covariância ¼·I − (1/16)·11ᵀ tem autovalores ¼, ¼, ¼ e 0.
- **(g)** a rodada 94 em **[1; 1]** (1 = IGUAIS). Mecanismo: só + − × ÷ e √, e comparações de valores iguais.
- **(h)** \|razão da tradução − razão do módulo\| em **[0; 1e-12]**. Identidade de desenho: a tradução é o mesmo código, com as somas em laço.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua rodou sobre o rascunho e deu m1 = 8, m2 = 4, m3 = 0,0021 e m5 = 0. E = 0,75, então m1 fica em [8; 9].
- **(m1)** nº de previsões do mundo em **[8; 9]**
- **(m2)** nº que cruzam ou tocam o zero em **[4; 5]**
- **(m3)** mediana de w em **[0,001; 0,03]**
- **(m4)** fração de acertos em **[0,75; 1,00]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, com centro 0,75.

➡ Anterior: [Parte 142](ASI_AGI_parte142_enantiodromia.md).

## Medido (P3195, P3196)
- **(a)** razão dos desvios: 0,9844. ✅
- **(b)** z = −0,893. ✅
- **(c)** fração da primeira metade: **0,49766** (z = −1,82). ❌
- **(d)** \|5ⁿ − Benford-16\| = 0,00030. ✅
- **(e)** \|7ⁿ − Benford-16\| = 0,00008. ✅
- **(f)** posto de 2ⁿ: 3,000000000. ✅

(A média das glosas em português é 1,74 palavra: a maioria dos sinsets da OWN-PT não tem glosa.)

### A régua da metade: o terceiro lote fora da faixa
Os lotes de (c) até aqui deram z = +1,81 e +2,38 (Parte 140, inglês), −0,76 (1.000 reservatórios), +0,97 (`random.sample`) e agora −1,82
(português). São três de cinco fora de faixas de 90%. A chance de isso acontecer sem defeito é cerca de C(5,3)·0,1³·0,9² + … ≈ 0,009.
A média não sai de ½ para um lado só, então o defeito provável não é um viés. É a LARGURA: o desvio de uma fração por reservatório pode
ser maior que o hipergeométrico. Um caminho de medida novo, registrado antes de rodar: o desvio-padrão das 300 frações por reservatório
(português e inglês, as mesmas sementes de (c) e da Parte 140) dividido por √(¼·(N − k)/(N − 1)/k), em **[0,933; 1,067]** em cada um.

**O teste da largura:** português 1,005, inglês 1,041, os dois dentro de [0,933; 1,067]: ✅ ✅. A largura por reservatório está certa.

**A hipótese que sobra**, ainda sem crédito: sementes CONSECUTIVAS dariam reservatórios correlacionados, e o lote inteiro andaria junto. Isso
desloca a média do lote sem mexer no desvio dentro dele. O teste, num mundo pequeno, para ter muitos lotes, registrado antes de rodar:
N = 2.000, k = 100, 60 lotes de 300 sementes consecutivas (o lote b começa em 10.000·b). Os 60 valores de z da média de cada lote devem ter
desvio em [0,85; 1,15], que é 1 ± 1,645/√118. Um desvio acima de 1,15 confirma a correlação entre sementes consecutivas.

**O teste das sementes consecutivas:** desvio dos 60 z = 1,092, dentro de [0,85; 1,15]: ✅. A média dos z foi 0,17; 9 de 60 lotes ficaram fora
de ±1,645, contra 6 esperados. Não há correlação entre sementes consecutivas. **Veredito:** o reservatório é uniforme e a largura está
certa, e os três lotes fora da faixa foram cauda. A sequência de lotes começou DEPOIS do primeiro erro, e daí em diante foram 2 fora em 4
(chance de cerca de 5%), não 3 em 5 (0,9%). Contar o lote que disparou a investigação como evidência dela é a falácia do olhar repetido.

**Rodada 94:** IGUAIS, 12 linhas e 11 números bit a bit: (g) ✅. O lado Python é o próprio `executar` do módulo, então (h) é 0: ✅. A memória
congelada viu 192 tentativas, todas no contexto "baixo" e nenhuma rejeitada; o fator dela é 1 − 0,6·1/194 = 0,99691.

Do mundo: (a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅

**Mundo: 7 de 8**, mais 3 de 3 nos testes do caminho novo (as duas larguras e as sementes consecutivas): 10 de 11.

## As contas, linha por linha
- **(c)** N = 53.058, k = 500. O desvio por reservatório é √(¼·(52.558/53.057)/500) = 0,022254, o de 300 reservatórios 0,0012848, e
  z = (0,49766 − 0,5)/0,0012848 = −1,82.
- **(f)** Em 2ⁿ, o primeiro dígito hexadecimal percorre o ciclo 2, 4, 8, 1, porque multiplicar por 2 desloca 1 bit e 16 = 2⁴. Os bits são
  one-hot, com média ¼ cada. A covariância é ¼·δᵢⱼ − 1/16, com autovalores ¼ (três vezes) e 0, e os três valores singulares iguais dão posto 3.
- **(d), (e)** Os postos de 5ⁿ (3,95651) e de 7ⁿ (3,95689) ficam a 0,0003 e a 0,0001 de Benford-16, como o 3ⁿ da Parte 140 (0,0012). Com três
  bases, a réplica conta: o primeiro dígito hexadecimal de bᵐ segue Benford-16 sempre que log₁₆ b é irracional.

## O placar (m)
m1 = 8 em [8; 9], m2 = 4 em [4; 5], m3 = 0,0021 em [0,001; 0,03], m4 = 0,875 em [0,75; 1,00], m5 = 0 em [0; 0] e m6 = 0 em [0; 1] (o erro de (c),
0,00024, é menor que a largura 0,0042). **(m): 6 de 6.** **Sobre mim:** 1 erro, em [0; 3]: ✅.

**Uma correção de (f), achada pelo teste de unidade.** Com n = 2.000 o posto de 2ⁿ dá 3,00000017. O autovalor nulo sai do Jacobi com cerca de
10⁻¹⁵, e a raiz o leva a 10⁻⁸, que entra na entropia. Com n = 5.000 o autovalor saiu negativo, o `max(0)` o zerou, e (f) acertou por SORTE DE
SINAL. A faixa [2,999999999; 3,000000001] estava estreita demais para uma identidade que passa por √ de um autovalor nulo: a tolerância honesta
é √ε ≈ 1e-8 na raiz, e cerca de 1e-7 no posto. O veredito de (f) fica ✅, porque o número caiu na faixa registrada, mas a faixa era frágil.
O teste e a regressão agora usam 1e-6. **Regra (Parte 143, complemento):** uma identidade que passa por √, log ou divisão perto de zero leva a
tolerância propagada (√ε, ε/x), não ε.

## Engenharia reversa
- **O padrão: uma régua honesta que erra três vezes parece um defeito.** Gastei quatro testes procurando um defeito no reservatório: outro
  caminho, outra largura, a correlação entre sementes. Os quatro passaram. A regra da Parte 137 (trocar o caminho, não só a semente) separou
  bem a cauda do defeito, mas não me disse quando PARAR de procurar.
- **O que isso revela.** Depois do primeiro erro, cada lote novo é ao mesmo tempo um teste e uma chance a mais de ver um erro, e eu conto os
  erros sem descontar as chances. É o olhar repetido (a "garden of forking paths") dentro de uma investigação honesta.
- **Regra nova (Parte 143):** quando uma investigação de cauda abre lotes novos, o placar dela conta os lotes DEPOIS do que a disparou, com a
  probabilidade binomial escrita, e para quando um caminho independente e um teste de largura passam. Dois caminhos limpos encerram a
  investigação; um terceiro erro isolado vira pendência, não mecanismo.

## Funções, testes, diálogo
- **Funções:** `p3195_fluxo_em_portugues`, `p3196_benford16_potencias` e `_parte_143`. Entradas P3195 e P3196 na regressão.
- **Testes:** `synthai/testes_parte143.py`.
- **Diálogo:** a rodada 94 (o retrocesso e a memória congelada) deu IGUAIS. Com ela, os quatro módulos tirados do que foi recebido passaram
  pelo Java: passos (91), GRPO (92), reservatório (93) e memória congelada (94).

➡ Próxima: [Parte 144](ASI_AGI_parte144_volta9.md).
