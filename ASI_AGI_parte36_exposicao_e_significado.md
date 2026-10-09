# Como eu construiria uma AGI/ASI — Parte 36 (0x24): a exposição, a lei do significado e o penhasco de Hamming

> Continuação da [Parte 35](ASI_AGI_parte35_renovacao_dirigida.md). A P491 achou o defeito da renovação dirigida: um braço desacreditado não é
> puxado e por isso não pode ser desmentido. Esta parte testa a peça que faltava (a **exposição**) e abre duas trilhas: a lei de Zipf do
> **significado** no WordNet e o **código de Gray** como representação para a auto-melhoria. Novidades: `ThompsonSurpresaExposta`
> ([`synthai/decisao.py`](synthai/decisao.py)), `de_gray` e `ea_um_mais_um` ([`synthai/hexadecimal.py`](synthai/hexadecimal.py)),
> `sentidos_por_lema` ([`synthai/dicionario.py`](synthai/dicionario.py)); testes em [`synthai/testes_parte36.py`](synthai/testes_parte36.py);
> números de `p521_...` a `p523_...` em [`calculos.py`](calculos.py). Diálogo, rodada 7: [`dialogo/DIALOGO.md`](dialogo/DIALOGO.md).
>
> **Contas e previsões no commit `217ac75`, antes de rodar.**

---

## As perguntas desta parte

1. **P521 (0x209).** A exposição cura o que a surpresa não via? ↩ P491
2. **P522 (0x20A).** O WordNet obedece à lei de Zipf do significado (m ∝ f^½)? ↩ P463
3. **P523 (0x20B).** Gray contra binário: o penhasco de Hamming na auto-melhoria. ↩ P392, P437
4. **P524 (0x20C).** Jung: exposição e confronto com a sombra.
5. **P525 (0x20D).** O diálogo, rodada 7.
6. **P549 (0x225).** Placar. **P550 (0x226).** Unificação.

---

### P521 (0x209). A exposição cura? (pré-registrado) ✅✅❌

**Na pergunta.** "O que a surpresa não via": o braço que não se puxa. Expor é puxá-lo de propósito: a cada 50 escolhas, o braço puxado há mais
tempo, em vez da amostra de Thompson.

**Lógica, a conta antes.** O custo da exposição no mundo estável: T/50 = 2000/50 = 40 puxadas forçadas, quase sempre de braços ruins, cada uma
custando em média p* − (média dos outros 9 braços). Na média das 100 sementes: 40 × 0,448 = **17,9**. Previsão: 43,1 (surpresa sem exposição) +
17,9 = **61,1**.

**Medido:**

| mundo | surpresa (P491) | **surpresa + exposição** | melhor anterior |
|---|---|---|---|
| estacionário | 43,1 | **61,5** | 30,7 (exato) |
| dano, custo | 42,3 | **19,5** | 14,1 (γ 0,99) |
| muda a cada 500 | 367,7 | **427,1** | 367,7 (surpresa) |

(a) estacionário a ±15% de 61,1: **61,5**, erro de 0,6% ✅. (b) custo do dano < 30: **19,5** ✅. (c) mundo que muda < 367,7 ❌ (427,1).

**A conta do (c), feita depois.** No mundo que muda, as puxadas forçadas custam o mesmo por puxada (~0,45), mas são o dobro: 4000/50 × 0,45 = 36.
367,7 + 36 = 403,7. O medido, 427,1, ficou 23 acima disso: a exposição ainda atrapalha a surpresa, porque uma puxada forçada de um braço
ruim entra na janela dele e pode disparar uma renovação desnecessária. **A exposição só paga onde o que não se olha mudou** (o dano: a crença
errada estava justamente nos braços não puxados). No mundo que muda, a surpresa já via a mudança nos braços que puxava.

**Tradução cruzada.** Ser exposto ao que se evita cura uma crença errada sobre isso; não ajuda quando a crença sobre o que se evita estava certa.

### P522 (0x20A). A lei de Zipf do significado no WordNet (pré-registrado) ✅✅

**Na pergunta.** Zipf (1945): palavras mais frequentes têm mais sentidos, m ∝ f^δ com δ ≈ ½. No WordNet: m = número de sinsets que contêm o lema;
f = frequência dele nas definições (o data lake da P381).

**Lógica.** 31.502 palavras com f ≥ 1. Duas estimativas de δ por mínimos quadrados em log m × log f:
- por palavra: **δ = 0,246**;
- pelas médias de faixas de 100 postos (como Zipf fez): **δ = 0,303**.

(d) δ por faixa em [0,3; 0,6] ✅ (no limite de baixo); (e) por palavra < por faixa ✅. **A conta do (e):** com uma variável explicativa ruidosa,
a inclinação dos mínimos quadrados encolhe pelo fator de confiabilidade Var(sinal)/Var(total). Agrupar por faixa tira a maior parte do ruído de
log f dentro da faixa, e a inclinação sobe. A razão 0,246/0,303 = **0,81** é esse fator.

**Por que abaixo de ½.** A frequência aqui é a das **definições**, não a do uso. Uma palavra com muitos sentidos de uso comum aparece nas
definições na proporção de quanto **serve para definir**, que cresce mais devagar. **Meta:** com frequências de uso (as contagens de sentidos
etiquetados, *cntlist*, que o data lake não tem), espero δ mais perto de ½. Fica como pergunta.

**Tradução cruzada.** Uma palavra usada para muitas coisas acaba significando muitas coisas. É a mesma lei que a P381 achou em outro ângulo: as
palavras que mais servem são as que destravam o resto.

### P523 (0x20B). Gray contra binário: o penhasco de Hamming (pré-registrado) ✅✅✅

**Na pergunta.** A P392 achou um ótimo local que só se escapa com dois bits de uma vez; a P437, uma auto-melhoria por mutação. Juntas, perguntam:
**a representação em bits decide o que a mutação alcança?**

**Lógica, a conta antes.** (1+1)-EA de Droste, 3 parâmetros de 8 bits, aptidão −Σ(v − 128)². Em binário, 0x7F = 0111 1111 e 0x80 = 1000 0000
diferem em **8 bits**: atravessar exige inverter esses 8 e nenhum outro dos 24:
$$
(1/24)^8 \times (23/24)^{16} = 9{,}0\times10^{-12} \times 0{,}506 = 4{,}6\times10^{-12}\ \text{por passo}.
$$
Em Gray, os vizinhos inteiros diferem em **1 bit**: (1/24)·(23/24)²³ = 0,04167 × 0,3757 = **0,0157** por passo e parâmetro. Três parâmetros
independentes, cada um esperando um evento de taxa 0,0157: o tempo até o último é (1/0,0157)·(1 + ½ + ⅓) = 63,9 × 1,833 = **117 avaliações**.

**Medido** (100 rodadas, 10.000 avaliações cada):

| código | começo | chegou ao ótimo | avaliações até ele |
|---|---|---|---|
| binário | penhasco (0x7F7F7F) | **0%** | — |
| **Gray** | penhasco | **100%** | **112,8** (conta: 117) |
| binário | ao acaso | 16% | 159 |
| **Gray** | ao acaso | **100%** | 309 |

(f) binário no penhasco 0% ✅; (g) Gray 100%, média em [60, 240] ✅ (112,8, a 3,6% da conta); (h) ao acaso, binário < 50% e Gray ≥ 95% ✅.

**Por que Gray é unimodal aqui.** Em Gray, todo inteiro n tem n − 1 e n + 1 entre os vizinhos de um bit. Numa aptidão que melhora a cada passo em
direção ao ótimo, todo ponto que não é o ótimo tem um vizinho de 1 bit melhor: **não há ótimo local**. Em binário, sobram os penhascos
(0x7F, 0x3F, 0xBF…), onde o vizinho inteiro está a muitos bits. Whitley mostrou que isso não vale para toda função (Gray pode criar ótimos
locais noutras); vale para as unimodais em cada parâmetro, como esta.

**Tradução cruzada.** A mesma mudança (de 127 para 128) é um passo em uma língua e um salto impossível em outra. **A representação decide o que é
perto.** É a lição da Rodada 1 do diálogo ("a representação é parte do algoritmo") medida em 100 rodadas.

**Meta.** A P437 mutava números reais; o genoma em bits com Gray é a versão em que as contas de alcance ficam exatas.

### P524 (0x20C). Jung: exposição e confronto com a sombra

Em Jung, a sombra não se integra por atenção ao que surpreende; se integra por **confronto**: olhar de propósito o que se evita. A exposição da
P521 é esse confronto mecânico: a cada 50 escolhas, o que se evita. **Funciona:** cura a crença errada sobre o evitado (custo do dano 42,3 → 19,5).
**Quebra:** o confronto junguiano é dirigido ao que **tem carga**; a exposição aqui é ao mais antigo, com carga ou sem. Por isso cobra no mundo onde
o evitado estava certo (427 contra 368). A Rodada 8 vai tentar a exposição dirigida: só ao que está esquecido **e** incerto.

### P525 (0x20D). O diálogo, rodada 7

O detector de surpresa nas duas linguagens: **as mesmas 2 renovações nos mesmos passos (621 e 638) e as mesmas crenças finais** (i) ✅. A conta da
IA-Java para o atraso: dispara quando 0,03n > 0,268, n > 8,9 puxadas depois da troca; medido 7 e 13. A lição da IA-Python: em Python, **importar é
executar** (o gerador da rodada 5 teve de ir para dentro de `main()`). As sete rodadas continuam idênticas bit a bit.

### P549 (0x225). Placar

(a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅. Parte 36: 9 testes, 1 erro. Acumulado: **113 erros em 290 testes**; taxa média 0,39,
intervalo 90% [0,34; 0,44]. É a parte com a menor taxa de erro desde que o placar existe, e a que tem as contas mais exatas (0,6% e 3,6%).

### P550 (0x226). Unificação e metacognição

- **Novos:** `ThompsonSurpresaExposta`, `de_gray`, `ea_um_mais_um`, `sentidos_por_lema` (4 testes; 95 no pacote). Regressão: + P523.
- **O mapa da renovação:** exato (estável), desconto γ (período conhecido), surpresa (mudança sem período), surpresa + exposição (dano). Quatro
  agentes, quatro mundos, nenhum domina. A pergunta da próxima parte é se um agente pode **saber em que mundo está** e escolher.

**Metacognição.** As contas que acertaram nesta parte (0,6% e 3,6%) eram contas de **mecanismo único**: um custo por puxada, uma taxa por passo.
A que errou (c) tinha **dois mecanismos em sentidos opostos** (a exposição ajuda a ver e atrapalha a janela), e eu só contei um. Regra: antes de
prever, listar todos os mecanismos que o módulo novo liga, e o sinal de cada um.

> **Síntese da Parte 36:** a exposição (forçar, a cada 50 escolhas, o braço visto há mais tempo) curou o defeito da renovação dirigida: o custo
> do dano caiu de 42,3 para 19,5, e o preço no mundo estável foi exatamente o calculado (61,5 contra 61,1). No mundo que muda ela atrapalhou (427
> contra 368), porque lá o que se evitava estava certo. O WordNet obedece à lei de Zipf do significado com δ = 0,30 por faixas (0,25 por palavra,
> diluído pelo ruído). E o código de Gray atravessou o penhasco de Hamming em 100% das rodadas, em 113 avaliações (a conta dizia 117), onde o
> binário não atravessou nenhuma: a representação decide o que é perto.

---

**Fontes pesquisadas nesta parte**
- A lei de Zipf do significado: [Ferrer-i-Cancho e Vitevitch, *The origins of Zipf's meaning-frequency law*, arXiv 1801.00168](https://ar5iv.labs.arxiv.org/html/1801.00168), [JASIST 69(11)](https://ideas.repec.org/a/bla/jinfst/v69y2018i11p1369-1379.html), [GWC 2019, 2019.gwc-1.44](https://aclweb.org/anthology/2019.gwc-1.44.pdf)
- Gray contra binário e o penhasco de Hamming: [Caruana e Schaffer, ICML 1988](https://mlanthology.org/icml/1988/caruana1988icml-representation), [Caruana e Schaffer, ICML 1989](https://mlanthology.org/icml/1989/caruana1989icml-using), [Gray and binary encoding in the (1+1)-EA](https://profiles.umsl.edu/en/publications/gray-and-binary-encoding-in-the-11-ea/), [An analysis of Gray versus binary encoding in genetic search](https://profiles.umsl.edu/en/publications/an-analysis-of-gray-versus-binary-encoding-in-genetic-search/)
- A diluição da inclinação pelo ruído na variável explicativa (fator de confiabilidade) e a espera pelo último de três eventos (soma harmônica): derivações próprias, conferidas pela simulação
