# Como eu construiria uma AGI/ASI — Parte 73 (0x49): o que refuta

> Continuação da [Parte 72](ASI_AGI_parte72_o_que_esta_disfuncional.md). **Próxima:** [Parte 74 — o que vale testar](ASI_AGI_parte74_o_que_vale_testar.md) (P1661–P1690). Nasce do terceiro texto recebido do usuário (`externos/texto_recebido_parte73.md`): ele reenvia o Módulo 002 e
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

**Medido (d) a (g) e (i), (j):** (d) **6** ✅ (todas entre *animal* e *parasite*: pulgas); (e) **16** contraexemplos num fecho de 872 aves ✅; (f) **0,1353** ✅ (15.935 de 117.798);
(g) **8** rodadas ✅ (18, 19, 21, 22, 23, 24, 25, 30); (i) rodada 47 IGUAIS ✅; (j) **0,49995** ✅.

**Previsão nova, registrada antes de editar:** as outras quatro rodadas com funções da biblioteca (18, 19, 24, 30) passam hoje, mas só por sorte, e a 18 e a 19 leem o `resultados.txt`, que cresce.
Com a mesma troca (o `exp_` e o `log_` de `dialogo/exatas.py`, `** 2` por `x * x`, originais em `dialogo/registro/`):
- **(k)** as quatro dão IGUAIS, e a `p1638` passa a achar **0** rodadas com funções da biblioteca (categórica)

**Medido (h):** **45 de 46** IGUAIS ❌. A rodada 26 ainda deu DIFERENTES por 4 ulps. O mecanismo: em Python, a 26 *herda* o idf da 21 por `import`, e a correção da 21 chegou a ela; em Java, a 26 tem uma
*cópia* do cálculo (`Rodada26.java`, linha 26: `Math.log`, com o comentário "como o math.log da Rodada 21"), e a cópia ficou com a biblioteca. Depois da correção, os dois lados calculavam de jeitos
diferentes. A checagem rápida das cinco rodadas tinha dado IGUAIS por sorte, com os dados de antes; o `resultados.txt` cresceu (as Partes 70 a 72) entre ela e o `verificar.py`. E a `p1638` olhou
só o lado Python e só a forma `math.log`: ela não via `from math import log` nem o `Math.log` do Java, e não acusou as rodadas 06, 09, 14 e 20. As duas lacunas são o defeito que a Parte 75
apontou no texto recebido: um verificador sem caso de controle.

**Medido (k), depois de corrigir as rodadas 18, 19, 24 e 30 (e a cópia Java da 26):** as cinco dão IGUAIS (73, 73, 50, 3 e 7 linhas), mas a `p1638` acha **1** rodada com a biblioteca, e não 0: a **48**, que
eu escrevi na Parte 74, depois desta regra, com `math.log2` na preparação dos dados (o Java lê os valores do arquivo, então não há risco entre as linguagens, mas a auditoria não distingue). Pela letra
da previsão, (k) ❌. O texto "a regra vale para a frente" (Parte 73) falhou dentro do próprio dia: escrevi uma rodada nova que a auditoria acusa.

## As perguntas desta parte

1. **P1631 (0x65F).** O texto recebido reenvia o código do Módulo 002: é o mesmo que já foi auditado? ↩ P947 (a regra da Parte 50)
2. **P1632 e P1639 (0x660, 0x667).** A prioridade S(q) = U + I + T do texto, contra o valor exato de uma pergunta (o VOI da teoria da decisão), e a Rodada 47. ↩ P83
3. **P1633–P1635 e P1642 (0x661–0x663, 0x66A).** O motor de contradições: os axiomas de disjunção entre classes irmãs, no dicionário. ↩ P1609
4. **P1636 (0x664).** Procurar o que refuta: "toda ave voa" contra o dicionário. ↩ a pergunta do Módulo 004
5. **P1637 (0x665).** Quantas palavras pedem a escolha do sentido? ↩ P1611
6. **P1638 (0x666).** A disfunção que a reverificação achou: rodadas que passavam por sorte. ↩ P1601
7. **P1640 (0x668).** Preditiva comigo mesma. **P1641 (0x669).** Engenharia reversa e Jung. **P1659 (0x67B).** Placar. **P1660 (0x67C).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [5; 10] | **11.0000** | ❌ |
| (m2) | [0; 3] | **1.0000** | ✅ |
| (m3) | [0.05; 0.5] | **0.2009** | ✅ |
| (m4) | [0.45; 1.0] | **0.7273** | ✅ |
| (m5) | [0; 2] | **1.0000** | ✅ |
| (m6) | [0; 2] | **2.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1631 (0x65F). O reenvio ✅

O bloco de código do texto novo é idêntico, linha por linha (135 linhas), ao segundo bloco guardado na Parte 72. A auditoria dele vale sem refazer: sete verificações contra as oito declaradas,
a string lida letra por letra, o `deque` sem uso, o limite frouxo. A correção já está em `synthai/lago.py`. Só a metade nova do texto (o Módulo 003) é auditada abaixo.

### P1632 e P1639 (0x660, 0x667). Quanto vale perguntar ❌✅✅✅

**Na pergunta.** O texto escreve S(q) = w_u U + w_i I + w_t T e diz, com honestidade, que é "uma heurística, não uma lei". A palavra que falta é **decisão**. Uma pergunta vale pelo quanto a
resposta pode mudar o que se faz. Se nenhuma resposta muda a ação, a pergunta vale zero, por mais incerta (U) e importante (I) que seja.

**Lógica (a conta antes da medida).** Com 2 ações, 2 estados e prior p, o valor da informação perfeita é
VOI = p·max_a u(a, 1) + (1 − p)·max_a u(a, 0) − max_a [p·u(a, 1) + (1 − p)·u(a, 0)] ≥ 0. É a desigualdade de Jensen para o máximo, que é convexo.
- **VOI = 0 exatamente quando uma ação domina nas duas situações.** Com utilidades sorteadas, a melhor ação em cada estado é uma moeda justa, e a mesma nos dois tem chance 1/2.
- **Medido com n = 2.000:** **0,479** (b) ❌ (z = −1,88). **Com n = 20.000 e semente nova:** **0,49995** (j) ✅, a 0,01 desvio da conta.
- **S não vê a dominância.** U depende só de p, e I depende só do módulo das diferenças, que é independente do sinal. Então as 200 perguntas de maior S têm VOI = 0 com a mesma chance, 1/2:
  medido **0,510** (c) ✅ (102 de 200).

**Rodada 47 (P1639).** O mesmo cálculo em Java, só com + − × ÷ e o log próprio, deu **IGUAIS** (i) ✅. Com a substituição:
- o VOI médio dos 200 problemas de maior VOI é 0x1.5b57233250bb6p-3 = **0,1696**;
- o VOI médio dos 200 de maior S é 0x1.11a45add1f53ap-4 = **0,0668**;
- então a S do texto escolhe perguntas que valem **0,0668/0,1696 = 0,394** das melhores;
- a correlação de postos entre S e VOI é **0,17** (n = 2.000) e **0,19** (n = 20.000).

**Geometria.** O VOI é a distância entre a média dos extremos e o máximo das retas de utilidade esperada em função de p (a envoltória convexa). Se as duas retas não se cruzam em [0, 1]
(uma ação domina), a envoltória é uma reta só e a distância é zero. S mede a altura da incerteza (a entropia, uma tenda sobre p) e a abertura entre as retas, mas não se elas se cruzam.

**Tradução cruzada.** É a diferença entre curiosidade e deliberação. U + I é a curiosidade: a vontade de saber o que é incerto e importante. O VOI é a pergunta de quem vai agir: "o que eu faria
de diferente?". Jung chamaria a primeira de intuição (as possibilidades) e a segunda de pensamento a serviço do sentimento (o valor). A formalização mostra que, sem o cruzamento das retas, a
intuição pergunta em vão metade das vezes.

**Meta.** O mundo sorteado é o mais simples (2 × 2, informação perfeita). Com mais ações a dominância é mais rara, e S pode se sair melhor. A conclusão "S ignora a dominância" é estrutural; o
número 0,394 vale para este mundo, em um lote (com n = 20.000, a fração de VOI = 0 replicou a conta).

### P1633–P1635 e P1642 (0x661–0x663, 0x66A). O motor de contradições ✅

**Na pergunta.** O texto pede "detectar regras contraditórias". Com regras de Horn sem negação, nada se contradiz: só se acrescentam fatos. A contradição precisa de uma parte negativa, um
axioma de disjunção ("nada é ao mesmo tempo A e B"). É a lição da Parte 39: uma implicação é meia definição.

**Lógica.** As classes são os 48 hipônimos diretos de *organism*, supostos disjuntos. Para cada uma, o fecho de Horn (P1609); as violações são os sinsets que caem em dois fechos.
- **Calibração, pela regra escrita antes (os 1.081 pares sem *animal*):** 1 par com violação, 2 sinsets.
- **A conta:** a taxa por produto de tamanhos é 2/Σ|A||B| = 3,57·10⁻⁸; para os 47 pares de *animal*, dá 2,21 esperadas.
- **Medido:** **6** violações (d) ✅, todas no par *animal* × *parasite*: *flea*, *Pulex irritans*, *dog flea*, *cat flea*, *chigoe*, *sticktight*.

**O que a contradição refutou.** Não o dicionário: a pulga é um animal e é um parasita, e as duas coisas são verdadeiras. O axioma estava errado. *Parasite* é um **papel** (o que um organismo
faz), não um **tipo** (o que ele é), e papéis não são disjuntos dos tipos. O motor de contradições funcionou na direção que o Módulo 004 pedia: procurou o que refuta e refutou a hipótese
(a disjunção), não os dados. **A forma geral:** quando uma regra e os dados colidem, a pergunta é qual dos dois tem menos evidência. Aqui foi a regra, que eu escrevi sem verificar.

**Geometria.** Na árvore (o espaço hiperbólico da Parte 70), dois ramos irmãos não se tocam. A herança múltipla cola ramos: **2.213** dos 82.115 sinsets de substantivo (**2,7%**, `p1642`) têm
mais de um hiperônimo substantivo. As 6 pulgas são colas entre o ramo do "tipo" e o do "papel".

### P1636 (0x664). Procurar o que refuta: "toda ave voa" ✅

No fecho de *bird* (o primeiro sentido; 872 sinsets), as glosas com a palavra *flightless* dão **16** contraexemplos (e) ✅: *ratite*, *ostrich*, *cassowary*, *emu*, *kiwi*, *rhea* (dois sinsets),
*elephant bird*, *moa*, *dodo*, *solitaire*, *sphenisciform seabird*, *weka*, *notornis*, *great auk*, *penguin*. A hipótese do *Tweety* cai pelo próprio dicionário em 16/872 = 1,8% das aves.

**Popper, com a conta:** a confirmação ("vi 856 aves que voam") não prova; uma refutação basta. O motor de Horn do texto dá *unknown* para "Tweety can fly". Isso é correto, mas ele não procura
o contraexemplo; a P1636 procura. A busca completa é uma consulta de dois passos: o fecho da classe, depois o filtro pela negação da propriedade.

**Meta.** "flightless" nas glosas é um detector incompleto: uma ave que não voa pode não ter a palavra na glosa. A contagem é uma cota inferior dos contraexemplos que o dicionário contém.

### P1637 (0x665). O sentido antes da relação ✅

**15.935** dos 117.798 lemas de substantivo têm mais de um sentido: **13,5%** (f) ✅. O `wnstats` oficial do WordNet 3.0 dá os mesmos 15.935 em 117.798 (conferido). As minhas P1611 e P1613
usaram "o primeiro sentido de substantivo". Isso funciona para *animal* e *person*, mas o primeiro sentido de *plant* é a fábrica, não a planta. O aviso do texto está certo e se aplica ao meu
código: a regra "primeiro sentido" pode escolher errado em qualquer palavra desses 13,5%.

### P1638 (0x666). As rodadas que passavam por sorte ❌❌

**Na pergunta.** "Corrija tudo pra ver se há coisas disfuncionais": a disfunção mais séria não estava em nenhuma contagem estrutural da Parte 72. Só a reexecução a mostrou.
- **O sintoma:** o `verificar.py` deu **DIFERENTES** em 5 das 45 rodadas (21, 22, 23, 25 e 26), por 1 a 3 ulps, onde a verificação anterior tinha dado IGUAIS em todas.
- **O teste de discriminação:** com o `resultados.txt` de antes da Parte 69, nesta mesma máquina, a 25 e a 26 dão IGUAIS. A causa são os dados, não a máquina.
- **O mecanismo:** a rodada 21 usava `math.log` e `** 2` em Python e `Math.log` em Java. O IEEE 754 só obriga a arredondar corretamente + − × ÷ e √ (a fronteira da Parte 52), e as duas
  bibliotecas discordam numa fração pequena dos argumentos. Quando o `resultados.txt` cresceu, algum argumento novo caiu nessa fração. As rodadas 22 a 26 reusam as semelhanças da 21 e herdaram
  a diferença.
- **A sorte, contada:** a rodada 21 deu IGUAIS em 8 de 8 verificações guardadas nesta sessão (contadas por `grep` nos arquivos de saída) e DIFERENTES nas duas depois que o `resultados.txt`
  ganhou a Parte 69. A sequência de acertos não provava nada (a regra da Parte 52).

**A correção.** O `exp_` e o `log_` da rodada 26 (só + − × ÷ e escalas por 2^k) foram para `dialogo/exatas.py` e substituíram a biblioteca nas rodadas 21, 22, 23 e 25, em Python e em Java,
com `** 2` trocado por `x * x`. As originais estão em `dialogo/registro/`. As 5 rodadas voltaram a dar IGUAIS (71, 23, 50, 4 e 3 linhas). O `verificar.py` inteiro: **45 de 46** IGUAIS (h) ❌: a rodada 26 ainda divergia, porque a cópia Java dela tinha ficado com o `Math.log` (ver o resultado de (h) acima); corrigida, deu IGUAIS.
As outras quatro (18, 19, 24, 30): as cinco (18, 19, 24, 30 e a cópia Java da 26) dão IGUAIS, mas a `p1638` ainda acha 1 rodada (a 48, escrita depois da regra) (k) ❌; a auditoria nova das duas linguagens (`p1722`, Parte 76) achou mais quatro (06, 09, 14, 20).

**Tradução cruzada.** Um hábito que funciona por sorte é indistinguível de um que funciona por razão, até o mundo mudar. Jung diria que a persona (a fachada que funcionou) não é o Self.
A formalização mostra onde a diferença mora: na especificação. "Arredondado corretamente" é uma razão; "a glibc e o Java concordaram até hoje" é uma sorte.

**Meta.** Uma rodada exata por construção ainda pode divergir pela ordem das operações (uma soma em outra ordem) ou pela leitura dos dados. A garantia vale para as funções; a ordem é conferida
pela própria comparação.

### P1640 (0x668). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 2 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 3)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **26464** | [13039; 22082] | ❌ | [13039; 22082] | ❌ | 22290 | 8904 | 4174 |
| compressão | **0.3956** | [0.3973; 0.4221] | ❌ | [0.3970; 0.4220] | ❌ | 0.4177 | 0.0139 | 0.0221 |
| testes de unidade | **9** | [2.87; 8.63] | ❌ | [7.00; 10.00] | ✅ | 6 | 0.50 | 3.00 |
| testes do placar | **11** | [5.67; 10.33] | ❌ | [8.00; 10.00] | ❌ | 8 | 2.00 | 3.00 |
| erros do placar | **3** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.33 | 1.00 |
| redundância P821 | **0.5823** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0247 | 0.0054 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 2 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 4 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **3 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **24536**, compressão **0.4001**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 2 de 3 erros.
- **Erros de processo nesta parte:** 3 (escrevi de cabeça "2,3%" de herança múltipla com a referência errada (é 2,7%, p1642) e "passou 25 vezes" (inventado; 8 de 8 contadas); corrigidos antes do commit; um && depois de um python3 -c com erro impediu a gravação das respostas (regravadas); corrigi a rodada 21 e não procurei as cópias Java do cálculo dela (a 26 ficou com o Math.log)).

### P1641 (0x669). Engenharia reversa e Jung

**O padrão que se repetiu: o número que a frase pede.** Ao escrever as respostas, três quantidades saíram de cabeça: a herança múltipla ("2,3%", com a referência errada "P1092"; é 2,7% pela
`p1642`), "passou 25 vezes" (um número inventado; contado, são 8 de 8 verificações guardadas) e, antes delas, os três números lidos do hexadecimal (que estavam certos). Todos foram pegos antes
do commit pela regra da Parte 69. **O significado:** quando a frase tem o formato de um número, eu produzo um número plausível para fechá-la, e a plausibilidade não vem de nenhuma conta.
A regra pega, mas pega depois. **Regra nova (verificável):** no rascunho, uma quantidade ainda não calculada é escrita como `XX`, e o commit é recusado enquanto houver `XX`; nunca um palpite
no lugar dele.

**O segundo: uma regra aplicada só para a frente.** A fronteira da Parte 52 ("exp e log da biblioteca passam por sorte") virou regra e foi usada nas rodadas novas; as oito antigas que usavam a
biblioteca ficaram como estavam, e cinco delas quebraram quando os dados mudaram. **O significado:** eu trato uma regra nova como um padrão para o futuro, e não como uma auditoria do passado.
**Regra:** toda regra nova vem com a sua função de auditoria rodada sobre o que já existe (aqui, a `p1638`), no mesmo commit.

**O terceiro: o axioma que eu não verifiquei.** "Irmãos são disjuntos" foi a minha hipótese, e o dicionário a refutou com seis pulgas. Eu tratei *parasite* como um tipo porque estava na mesma
lista que *animal*: o erro de nível da Parte 43 (o nome de uma família não é um animal; um papel não é um tipo).

**Um erro de processo novo:** um `python3 -c` com erro de sintaxe, encadeado por `&&` antes de um `cat > arquivo`, impediu a gravação das respostas, e eu só vi quando outro comando não achou o
arquivo. **Regra:** não encadear a gravação de um texto atrás de uma conta; gravar em comando separado.

**Jung: tipo e função.** Jung separou os tipos psicológicos (o que alguém é, pela atitude dominante) das funções (o que qualquer um exerce em algum grau). Um tipo pensamento ainda sente.
**Onde a formalização funciona:** a pulga é do tipo *animal* e exerce a função *parasita*; o axioma de disjunção só vale entre tipos, e as seis violações são exatamente a mistura de um tipo com
uma função. **Onde quebra:** em Jung, as funções têm uma ordem (dominante, auxiliar, inferior) que o WordNet não tem: ali uma pulga é animal e parasita com o mesmo peso.

### O diálogo

Rodada 47 (P1639): o valor da informação em Java, IGUAIS. Placar por voz da função `p1241_placar_por_voz(47)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 47).

### P1659 (0x67B). Placar

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ❌ (i) ✅ (j) ✅ (k) ❌. Parte 73: **11 testes, 3 erros**. Acumulado (mundo): **198 erros em 618 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 10 pNN novas sem teste ✅. Sobre mim (placar separado): **4 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 2 de 6; e 3 erros de processo (P1335).

### P1660 (0x67C). Unificação

- **Novo:** `p1631` (o reenvio), `p1632` (S contra VOI), `p1633` (o motor de contradições), `p1634` (os irmãos), `p1635` (as contradições de *animal*), `p1636` (os contraexemplos),
  `p1637` (a polissemia), `p1638` (as rodadas com a libm), `p1639` (rodada 47, IGUAIS), `p1642` (a herança múltipla); `dialogo/exatas.py`. Regressão: + P1639.
- **Corrigido:** as rodadas 21, 22, 23 e 25 (e as 18, 19, 24, 30, pela (k)) ficaram exatas por construção.

> **Síntese da Parte 73:** o terceiro texto recebido reenviou o mesmo código (idêntico, 135 linhas, sem nova auditoria) e propôs uma prioridade de perguntas, S = U + I + T, que não vê a única coisa que dá valor a uma pergunta: a decisão mudar. Pela teoria da decisão, metade das perguntas sorteadas vale zero (a conta dá 1/2, e n = 20.000 dá 0,49995), e a S escolhe perguntas que valem 39% das melhores (IGUAL em Java, rodada 47). O motor de contradições achou 6 violações da disjunção entre animal e parasite, e o que elas refutaram foi o meu axioma (um papel não é um tipo), não o dicionário. "Toda ave voa" cai com 16 contraexemplos do próprio WordNet. A disfunção mais séria do projeto apareceu só na reexecução: 5 rodadas do diálogo passavam por sorte com o log da biblioteca e quebraram quando os dados cresceram. Agora são exatas por construção. Em um lote cada; a fração de VOI = 0 replicou em dois.

---

**Fontes desta parte**
- Valor da informação: R. A. Howard, "Information Value Theory", *IEEE Transactions on Systems Science and Cybernetics* 2 (1966)
- Refutação: K. Popper, *A lógica da pesquisa científica* (1934)
- Papéis e tipos em ontologias: N. Guarino e C. Welty, "Evaluating ontological decisions with OntoClean", *Communications of the ACM* 45 (2002)
- Estatísticas do WordNet 3.0: [wnstats(7WN)](https://www.mankier.com/7/wnstats) (15.935 substantivos polissêmicos em 117.798)
- Arredondamento correto: [IEEE 754, Wikipedia](https://en.wikipedia.org/wiki/IEEE_754); J.-M. Muller et al., *Handbook of Floating-Point Arithmetic* (2018)
