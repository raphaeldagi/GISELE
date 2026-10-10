# Como eu construiria uma AGI/ASI — Parte 77 (0x4D): as duas abertas

> Continuação da [Parte 76](ASI_AGI_parte76_a_forma_do_byte.md). **Próxima:** [Parte 78 — a atenção de posto baixo](ASI_AGI_parte78_a_atencao_de_posto_baixo.md) (P1781–P1810). Fecha os dois itens que a auditoria das duas linguagens (`p1722`) deixou abertos: as rodadas 09 e 14, em que o Java usa o log da
> biblioteca e o Python o usa dentro de peças medidas (`synthai/decisao.py` e a `p732`). Pedido permanente: "Continue sem parar."

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[2; 6]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,00; 0,40]** (previsões de igualdade têm w = 0)
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[2 + S; 5 + S]** | ~2 funções novas |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de mexer nas rodadas)

**Rodada 14.** O Python passa a calcular os pesos dentro da rodada (a mesma conta da `p732`, que fica intacta), com o `log_` de `dialogo/exatas.py`; o Java troca `Math.log` pelo mesmo `log_`.
- **(a)** IGUAIS (categórica)
- **(b)** as duas listas de 12 trigramas impressas ficam **iguais** às da versão com a biblioteca (a ordem sai de comparações de pesos; um ulp só troca a ordem se dois pesos estiverem a menos de um
  ulp um do outro: a regra da Parte 55) (categórica)

**Rodada 09.** Duas fronteiras: o log e o exp da biblioteca, e o `sum()` compensado do Python 3.12 (a regra da Parte 34) dentro da `ThompsonMistura`. O Python passa a usar uma cópia exata das duas
classes dentro da rodada (laços de soma simples, `exp_` e `log_`), e o `synthai/decisao.py` fica intacto; o Java troca `Math.exp` e `Math.log`.
- **(c)** IGUAIS (categórica)
- **(d)** a maior diferença relativa entre os números impressos pela versão nova e pela antiga do Python em **[0; 1·10⁻¹²]** (as duas diferem só por ulps de log, exp e da compensação da soma)

**A auditoria.**
- **(e)** depois das duas, a `p1722` lista só a 48 (só na preparação) (categórica)

**Medido:** (a) rodada 14 IGUAIS ✅; (b) as duas listas de 12 trigramas iguais às da versão com a biblioteca ✅; (c) rodada 09 IGUAIS (4 linhas, 13 números) ✅; (d) 6 dos 13 números mudaram, a maior
diferença relativa é **1,1·10⁻¹³** ✅; (e) a `p1722` lista só a 48 ✅. **A fronteira da Parte 52 está fechada:** nenhuma rodada depende mais do arredondamento das bibliotecas entre as duas linguagens.

**Uma suposição errada, pega antes de mexer:** eu tinha escrito que o `sum()` compensado do Python era uma segunda fronteira na rodada 09. Lendo o `Rodada09.java`, ele já reproduz a soma
compensada ("tudo o que o Python soma com sum() é somado aqui com a soma compensada (rodada 5)"). A cópia Python manteve o `sum()`. A previsão (c) não dependia disso.

## As perguntas desta parte

1. **P1751 (0x6D7).** As rodadas 09 e 14 podem ficar exatas por construção sem editar as peças medidas que elas usavam? E o que muda nos números? ↩ P1722
2. **P1752 (0x6D8).** Preditiva comigo mesma. **P1753 (0x6D9).** Engenharia reversa e Jung. **P1779 (0x6EB).** Placar. **P1780 (0x6EC).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [2; 6] | **5.0000** | ✅ |
| (m2) | [0; 2] | **0.0000** | ✅ |
| (m3) | [0.0; 0.4] | **indefinida (nenhuma faixa numérica: a p1481 não conta as categóricas como faixas)** | ❌ |
| (m4) | [0.4; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 1] | **0.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1751 (0x6D7). As duas abertas, fechadas ✅✅✅✅✅

**Na pergunta.** "Sem editar as peças medidas" é a restrição que tornava as duas rodadas difíceis: o log do Python morava na `p732` e na `synthai/decisao.py`, que as regras das Partes 14 e 22 não
deixam mudar. A saída é a de sempre neste projeto: uma versão nova ao lado da antiga. A rodada passa a ter a sua própria cópia exata da conta, e a peça medida fica intacta.

**Lógica.**
- **Rodada 14:** os pesos log((c_animal + 1)/(N_animal + V)) − log((c_outro + 1)/(N_outro + V)) dos 6.074 trigramas, calculados dentro da rodada com o `log_` de `dialogo/exatas.py`, e o
  Java com o mesmo `log_`. IGUAIS (a) ✅. As duas listas de 12 trigramas não mudaram (b) ✅: a ordem sai de comparações, e nenhum par de pesos vizinhos estava a menos de um ulp (a regra da Parte 55:
  escolher absorve um erro quando a margem é maior que ele).
- **Rodada 09:** a média bayesiana de quatro detectores de mudança, com cópias exatas da `ThompsonBOCPD` e da `ThompsonMistura` (só `atualizar` e `pesos`), `exp_` e `log_`. IGUAIS em 13 números (c) ✅.
  Contra a versão com a biblioteca, 6 dos 13 números mudaram, e a maior diferença relativa foi **1,1·10⁻¹³** (d) ✅: o tamanho de uns poucos ulps acumulados em 1.200 passos de log e exp.
- **A auditoria:** a `p1722` lista só a 48, que usa `log2` só para preparar dados que o Java lê (e) ✅.

**O balanço final da fronteira da Parte 52:** das 14 rodadas que usavam exp ou log da biblioteca, as 12 com risco entre as linguagens estão corrigidas, e as 2 restantes nunca tiveram risco.
Nenhuma rodada do diálogo depende mais de as bibliotecas do Python e do Java arredondarem igual.

**Geometria.** Um ulp é a distância entre dois doubles vizinhos; a diferença relativa de 1,1·10⁻¹³ é ~500 ulps (o ulp relativo de um double é 2⁻⁵² ≈ 2,2·10⁻¹⁶), acumulados em 1.200 passos.
Uma ordem (a lista dos trigramas) é estável quando a menor distância entre vizinhos é maior que essa nuvem; um número contínuo (os log-pesos) nunca é.

**Tradução cruzada.** O que se corrigiu aqui não foi um erro de conta, foi uma dependência: duas pessoas que concordam porque leram o mesmo jornal não confirmam uma à outra. As rodadas concordavam
porque as duas bibliotecas, por acaso, arredondavam igual nos argumentos que apareciam. Agora concordam porque fazem a mesma conta com as operações que o IEEE 754 obriga a arredondar igual.

**Meta.** "500 ulps" é uma conversão de ordem de grandeza (1,1·10⁻¹³/2,2·10⁻¹⁶ = 500), não uma contagem: os ulps de cada número dependem do expoente dele.

### P1752 (0x6D8). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **12485** | [13039; 22082] | ❌ | [13039; 22082] | ❌ | 22290 | 5076 | 9805 |
| compressão | **0.4017** | [0.3973; 0.4221] | ✅ | [0.3970; 0.4220] | ✅ | 0.4177 | 0.0078 | 0.0160 |
| testes de unidade | **2** | [2.87; 8.63] | ❌ | [2.00; 5.00] | ✅ | 6 | 1.50 | 4.00 |
| testes do placar | **5** | [5.67; 10.33] | ❌ | [4.00; 6.00] | ✅ | 8 | 0.00 | 3.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.5618** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0452 | 0.0259 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 2 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **10785**, compressão **0.4114**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 1 (supus, sem ler o Java, que o sum() compensado era uma segunda fronteira na rodada 09; corrigido lendo, antes de mexer).

### P1753 (0x6D9). Engenharia reversa e Jung

**O padrão desta parte: uma suposição sobre a outra linguagem, sem ler a outra linguagem.** Escrevi, na previsão, que o `sum()` compensado era uma segunda fronteira na rodada 09; o `Rodada09.java`
já o reproduzia, e dizia isso no comentário da segunda linha. É o mesmo padrão da Parte 76 (eu penso pelo Python e imagino o Java), agora pego antes do erro, porque a regra nova (ler os dois
lados antes de mexer) foi aplicada antes da edição. **O significado:** a regra funciona quando é executada no momento certo (antes de editar), e não quando é lembrada depois.

**O que funcionou:** as cinco previsões acertaram, e todas eram categóricas ou de faixa estreita, com a conta antes. Uma parte de correção, com o mecanismo conhecido, é uma parte de previsões fáceis;
o placar de 5 de 5 diz pouco sobre a minha calibração, e por isso não deve subir o centro das próximas (m4).

**Jung: o fechamento.** Fechar uma série de correções (12 de 12 rodadas) dá a sensação de completude, que Jung associava ao mandala, o círculo que contém. **Onde a formalização funciona:** "fechado"
aqui tem uma definição verificável (a `p1722` lista só o que não tem risco, e um teste guarda isso). **Onde quebra:** o círculo só contém o que a auditoria sabe olhar (exp e log da biblioteca);
uma diferença de ordem de soma, ou de leitura de dados, ficaria fora dele, e a única guarda contra isso continua sendo a comparação bit a bit de cada rodada.

**A (m3) indefinida.** Previ a mediana de w "em [0,00; 0,40] (previsões de igualdade têm w = 0)", e a régua `p1481` não conta previsões categóricas como faixas: sem nenhuma faixa numérica, a mediana
não existe. Errei a forma da minha própria régua (a regra da Parte 31, verificar a forma antes de usar, aplicada a uma ferramenta que eu mesma escrevi). **Regra:** numa parte só de categóricas,
a (m3) se registra como "indefinida" e não com uma faixa.

### O diálogo

As rodadas 09 e 14 reescritas foram o diálogo desta parte: o mesmo `exp_` e `log_` nas duas línguas. Placar por voz da função `p1241_placar_por_voz(48)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 48).

### P1779 (0x6EB). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 77: **5 testes, 0 erros**. Acumulado (mundo): **201 erros em 641 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 1 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 2 de 6; e 1 erros de processo (P1335).

### P1780 (0x6EC). Unificação

- **Novo:** `p1751` (a rodada 09 nova contra a original); as rodadas 09 e 14 exatas por construção, com as originais em `dialogo/registro/`. Regressão: + P1751; a entrada P1722 passa a esperar
  ["48"] (a Parte 77 mudou o objeto que ela mede, e o comentário no código diz isso).

> **Síntese da Parte 77:** as duas últimas rodadas que dependiam do arredondamento das bibliotecas (09 e 14) ficaram exatas por construção, com cópias exatas das peças medidas que elas usavam (que ficaram intactas): IGUAIS nas duas, as listas de trigramas iguais às de antes, e os números da média bayesiana mudaram no máximo 1,1·10⁻¹³. Das 14 rodadas que usavam exp ou log da biblioteca, as 12 com risco estão corrigidas e as 2 restantes nunca tiveram risco: nenhuma rodada do diálogo depende mais de o Python e o Java arredondarem igual. Uma suposição minha sobre o Java (o sum() compensado) estava errada e foi pega lendo o arquivo antes de mexer.

---

**Fontes desta parte**
- Arredondamento correto e as funções da biblioteca: J.-M. Muller et al., *Handbook of Floating-Point Arithmetic* (2018), cap. 10; [IEEE 754, Wikipedia](https://en.wikipedia.org/wiki/IEEE_754)
- A soma compensada: A. Neumaier, "Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen", *ZAMM* 54 (1974); [What's New In Python 3.12 (sum)](https://docs.python.org/3/whatsnew/3.12.html)
