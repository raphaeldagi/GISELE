# Como eu construiria uma AGI/ASI — Parte 70 (0x46): álgebra e geometria

> Continuação da [Parte 69](ASI_AGI_parte69_a_forma_de_gpt.md). Pedido do usuário, gravado no `CLAUDE.md`: **"Continue ao máximo que puder! Use álgebra e geometria! Grave na
> memória!"** Esta parte lê a forma de GPT e o dicionário como geometria e os resolve por álgebra: a lei de escala do GPT por mínimos quadrados em forma fechada; a geometria dos
> embeddings (ângulos entre letras, a componente principal por iteração de potência); a taxonomia do WordNet como espaço hiperbólico (o δ de Gromov); e os dígitos hexadecimais
> como vetores de GF(2)⁴.

## Previsões sobre as minhas previsões desta parte (prever o previsto)

**Uma observação de metacognição antes de prever:** ao planejar as calibrações desta parte eu já esbocei de cabeça as faixas das previsões do mundo. Prever agora o número delas e a
largura delas (as (m1), (m2), (m3) e (m5) das partes anteriores) seria prever o que eu já sei: não é teste. **"Prever o previsto" degenera quando o previsor já pensou as previsões.**
Registro só o que eu não posso saber ainda, e o resto fica fora do placar desta vez:
- **(m4)** a fração de acertos do mundo em **[0,56; 1,00]** (117 previsões das Partes 53 a 69 pela régua `p1481`: 74,4% de acerto; com 9 previsões, a faixa binomial de 90% vai de
  5/9 a 9/9).
- **(m6)** o número de surpresas (erros maiores que a largura da faixa) em **[0; 2]**.

## As perguntas desta parte

1. **P1541–P1542 (0x605–0x606).** A lei de escala da forma de GPT, por álgebra: quantos passos até empatar com o trigrama? E o dobro de d ajuda? (Rodada 44) ↩ P1513
2. **P1543 (0x607).** A geometria dos embeddings do GPT: o modelo descobre as vogais? ↩ P1513
3. **P1544 (0x608).** A taxonomia dos substantivos do WordNet é quase uma árvore? O δ de Gromov (a geometria hiperbólica). ↩ P1492, P1454
4. **P1545 (0x609).** Hexadecimal como álgebra: quantas janelas de 4 dígitos de π formam uma base de GF(2)⁴? ↩ P1515
5. **P1546 (0x60A).** Preditiva comigo mesma. **P1547 (0x60B).** Engenharia reversa e Jung. **P1548 (0x60C).** O diálogo.
6. **P1569 (0x621).** Placar (três). **P1570 (0x622).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: as 9 previsões do mundo abaixo, (a) a (i), e 5 funções novas (p1541 a p1545) mais a rodada 44 (p1549).

| medida | estatístico (até a 69) | ingênuo (Parte 69) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.680; 18.864] | 16.374 | **[13.680; 18.864]** | o estatístico |
| compressão | [0,398; 0,421] | 0,411 | **[0,398; 0,421]** | o estatístico |
| testes de unidade | [2,60; 8,15] | 9 | **[5 + S; 8 + S]** | 6 funções planejadas, uma por teste, ~1 por surpresa |
| testes do placar | [5,83; 9,67] | 8 | **9 + 2·S ± 1** | as 9 letras abaixo |
| erros do placar | [0; 3,52] | 0 | **[0; 3,52]** | o estatístico |
| redundância P821 | [0,563; 0,638] | 0,564 | **[0,563; 0,638]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1544, o δ de Gromov da taxonomia dos substantivos** (grafo não dirigido dos hiperônimos, a maior componente; 300 quádruplos sorteados com semente 70; distâncias por busca em largura).
- **Restrições, com peso:** (1) numa árvore, δ = 0 exatamente (os quatro pontos estão sobre uma árvore e as duas maiores somas empatam); (2) a herança múltipla cria ciclos e afasta δ
  de zero; os substantivos têm 2,7% de sinsets com dois pais (P1454), os verbos 0,23%; (3) **peso medido num caso escolhido por regra escrita antes (os verbos, 300 quádruplos):** δ
  máximo **2,0**, δ médio 0,038, **3,3%** dos quádruplos com δ > 0.
- Exemplo à mão: numa estrela (uma raiz com quatro filhos), todas as distâncias são 2, as três somas são 4, e δ = 0.
- (a) o δ máximo nos substantivos em **[1,0; 4,0]**
- (b) a fração dos quádruplos com δ > 0 em **[0,05; 0,40]** (mais herança múltipla que os verbos, ~12 vezes, mas cada ciclo afeta só os quádruplos que passam por ele)

**P1545, π em GF(2)⁴.** A fração das 9.997 janelas de 4 dígitos hexadecimais consecutivos de π que formam uma base de GF(2)⁴.
- **A conta antes da medida:** para dígitos independentes e uniformes, é |GL(4, 2)|/16⁴ = 15·14·12·8/65.536 = 20.160/65.536 = **0,30762**; o desvio de uma proporção de ~10.000 janelas
  (sobrepostas, então correlacionadas: o desvio efetivo é ~2 vezes o de janelas independentes) é ~0,009. **Peso medido num caso escolhido por regra (dígitos pseudoaleatórios, semente
  1570):** 0,3063.
- Exemplo à mão: as janelas 1, 2, 4, 8 (os vetores da base canônica) formam uma base; 1, 2, 3, x não (3 = 1 ⊕ 2).
- (c) a fração em **[0,290; 0,325]**

**P1543, a geometria dos embeddings** (o GPT inglês da curva de escala, d = 24, depois de 16.000 passos).
- **Restrições, com peso:** (1) com pesos ao acaso, os cossenos entre embeddings de dimensão 24 ficam em torno de 0 com desvio 1/√24 ≈ 0,2; (2) prever o próximo caractere obriga a separar
  as letras que ocupam as mesmas posições: vogais e consoantes alternam nas palavras; (3) **peso medido num caso escolhido por regra (o GPT português de 2.000 passos):** cosseno médio
  entre vogais **0,221**, entre vogal e consoante **−0,173** (diferença 0,394), entre consoantes 0,131; a primeira componente principal tem **17,6%** da variância.
- (d) a diferença (cosseno entre vogais) − (cosseno vogal-consoante) em **[0,15; 0,70]**
- (e) a fração da variância na primeira componente principal em **[0,10; 0,30]**

**P1541–P1542, rodada 44:** no `dialogo/DIALOGO.md` (previsões (f) a (i)).
