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
