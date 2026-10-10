# Como eu construiria uma AGI/ASI — Parte 73 (0x49): o que refuta

> Continuação da [Parte 72](ASI_AGI_parte72_o_que_esta_disfuncional.md). Nasce do terceiro texto recebido do usuário (`externos/texto_recebido_parte73.md`): ele reenvia o Módulo 002 e
> acrescenta o Módulo 003 (uma fórmula de prioridade de perguntas, o WordNet com *sparrow*, uma checklist de 8 testes) e a pergunta do Módulo 004: **"como construir um sistema que procure
> ativamente evidências capazes de demonstrar que a hipótese está errada?"**

## Previsões sobre as minhas previsões desta parte (registradas antes de pensar qualquer faixa do mundo)

Histórico (`p1481`, Partes 53 a 72): as que cruzam o zero acertam ~56%, as contagens ~67%, a taxa geral ~74%. Na Parte 72, as duas que erraram eram de memória ou de nível.
- **(m1)** o número de previsões do mundo em **[5; 10]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,50]**
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), registradas antes de escrever a parte e antes das do mundo

Planejadas: 6 previsões do mundo e 6 funções novas (a comparação do reenvio, a prioridade de perguntas contra o valor da informação, a rodada 47, o motor de contradições, a busca de
contraexemplos, os sentidos). E = número de erros do mundo, S = número de surpresas, ambos contados pelo script; pela regra da Parte 71, cada erro de mecanismo abre um teste novo.

| medida | estatístico (até a 71) | ingênuo (Parte 71) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.039; 22.082] | 22.290 | **[13.039; 22.082]** | o estatístico |
| compressão | [0,397; 0,422] | 0,418 | **[0,397; 0,422]** | o estatístico |
| testes de unidade | [2,87; 8,63] | 6 | **[5 + S; 8 + S]** | 6 funções, uma por teste |
| testes do placar | [5,67; 10,33] | 8 | **6 + E ± 1** | as 6 letras, mais uma por erro de mecanismo |
| erros do placar | [0; 3,33] | 2 | **[0; 3,33]** | o estatístico |
| redundância P821 | [0,563; 0,651] | 0,588 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

## Previsões do mundo (registradas depois das (m) e das previsões sobre mim, antes de medir)

**O reenvio (P1631).** A primeira metade do texto novo reenvia o código do Módulo 002, e a regra da Parte 50 manda comparar com a cópia guardada antes de auditar de novo.
- **(a)** o bloco de código do texto novo é **idêntico** ao segundo bloco guardado na Parte 72 (categórica)

**A prioridade de perguntas contra o valor da informação (P1632).** O texto propõe S(q) = w_u U + w_i I + w_t T (incerteza, impacto, testabilidade). A teoria da decisão tem a resposta
exata para "quanto vale perguntar": o valor da informação perfeita, VOI = E[max_a u(a, s)] − max_a E[u(a, s)]. O mundo: 2.000 problemas de decisão com 2 ações e 2 estados, prior p ~ U(0, 1),
utilidades u(a, s) ~ U(0, 1) independentes, semente 73; a pergunta é observar o estado. U = entropia binária de p, I = max_s |u(0, s) − u(1, s)|, T = 1, pesos 1.
- **A conta antes da medida:** VOI = 0 quando a mesma ação é a melhor nos dois estados (dominância). O sinal de u(0, s) − u(1, s) é uma moeda justa e independente em cada estado, e os dois
  sinais iguais têm chance 1/2. Com n = 2.000, o desvio é √(0,25/2.000) = 0,0112.
- **(b)** a fração de perguntas com VOI = 0 em **[0,482; 0,518]** (0,5 ± 1,645 · 0,0112)
- **A conta para (c):** S não vê a dominância. U depende só de p, que é independente das utilidades. I depende de |u(0, s) − u(1, s)|, e para diferenças simétricas o módulo é independente
  do sinal. Então as 200 perguntas de maior S (os 10% do topo) também têm VOI = 0 com chance 1/2: o desvio é √(0,25/200) = 0,0354.
- **(c)** a fração de VOI = 0 entre as 200 de maior S em **[0,442; 0,558]**

**O motor de contradições (P1633, P1634).** Um axioma de disjunção ("nada é ao mesmo tempo A e B") entre classes irmãs é a metade negativa que a Parte 39 mostrou faltar. As classes são os 48
hipônimos diretos de *organism*. **Calibração por regra escrita antes de olhar:** todos os pares que não envolvem *animal* (a classe do teste). Deram 1.081 pares, 1 com violação, 2 violações
no total. **O mecanismo (a herança múltipla) está presente na calibração? Sim, mas o peso depende do tamanho dos fechos:** a taxa por produto de tamanhos é 2/Σ|A||B| = 3,57·10⁻⁸, e para os
47 pares de *animal* (4.017 sinsets; os irmãos maiores têm 10.297 e 4.488) a conta dá **2,21** violações esperadas. A taxa vem de 2 eventos: o fator de Poisson de 90% para 2 é [0,18; 3,15].
- **(d)** o número de sinsets que violam a disjunção entre *animal* e algum dos seus 47 irmãos em **[0; 10]**

**Procurar o que refuta (a pergunta do Módulo 004).** A hipótese "toda ave voa" (o *Tweety* do texto) refutada pelo próprio dicionário: os sinsets no fecho de *bird* (o primeiro sentido)
cuja glosa contém *flightless*. Sem calibração possível sem olhar: a faixa vem da memória (avestruz, emu, casuar, ema, kiwi, pinguim, dodô, moa…) e por isso é larga.
- **(e)** os contraexemplos em **[3; 25]**

**Os sentidos (o aviso do texto: identificar o sentido antes da relação).** As minhas P1611 e P1613 usam "o primeiro sentido de substantivo". O risco medido:
- **(f)** a fração dos lemas de substantivo com mais de um sentido de substantivo em **[0,10; 0,18]** (de memória das estatísticas do WordNet 3.0)

**A disfunção que a reverificação achou: 5 rodadas DIFERENTES (21, 22, 23, 25, 26).** Com o `resultados.txt` antigo, nesta máquina, as rodadas 25 e 26 dão IGUAIS: a causa são os dados
novos. A rodada 21 usa `math.log` e `** 2` (Python) e `Math.log` (Java), funções que o IEEE 754 não obriga a arredondar corretamente, e as 22 a 26 herdam as semelhanças dela.
- **(g)** o número de rodadas Python (de 46) que chamam uma função transcendental da biblioteca (`math.exp`, `log`, `log2`, `log10`, `pow`, `sin`, `cos`, `tan`, `atan`, `atan2`, `erf`) em
  **[5; 20]**
- **(h)** depois de trocar, nas rodadas que divergiram (21, 22, 23 e 25, em Python e em Java), as funções da biblioteca pelo `exp_` e `log_` da rodada 26 e `** 2` por `x * x`, o `verificar.py`
  dá **46 de 46 IGUAIS** (categórica)
- **(i)** a rodada 47 (o VOI e o S(q) da P1632 em Java, só com + − × ÷ e √) dá IGUAIS (categórica)

**Medido (a) a (c):** (a) idêntico, 135 linhas ✅. (b) **0,479** ❌ (z = (0,479 − 0,5)/0,0112 = −1,88: por 0,003 fora da faixa de 90%, que erra 10% das vezes). (c) **0,510** ✅.

**Previsão nova, nascida de (b), registrada antes de rodar:** se a conta (1/2 exato) está certa, um mundo maior a confirma. Semente 74, n = 20.000: desvio √(0,25/20.000) = 0,00354.
- **(j)** a fração com VOI = 0 em **[0,4942; 0,5058]**
