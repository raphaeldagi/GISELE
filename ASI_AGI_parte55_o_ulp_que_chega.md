# Como eu construiria uma AGI/ASI — Parte 55 (0x37): o ulp que chega

> Continuação da [Parte 54](ASI_AGI_parte54_a_sorte_das_rodadas.md). **Próxima:** [Parte 56 — os empates](ASI_AGI_parte56_empates.md) (P1121–P1150). **Previsões no commit `a6e6724` (a (c2) no seguinte), antes de qualquer execução e antes de
> escrever o resto deste documento.** A Parte 54 achou que as diferenças da libm somem quando caem fora do caminho da saída (uma escolha as absorve) e se propagam numa
> iteração. Esta parte **injeta** um ulp em cada exp e log das rodadas antigas e mede quanto ele chega à saída; mede a fragilidade do mapa da definição a
> uma palavra; conta os dígitos hexadecimais que um ulp muda; e audita as funções novas sem teste.

## As perguntas desta parte

1. **P1091 (0x443).** Um ulp em cada exp e log: quanto chega à saída de cada rodada? (Rodada 29) ↩ P1061
2. **P1092 (0x444).** Quantas funções pNN novas (desde a P821) não têm teste? (a checagem pedida pela Parte 54)
3. **P1093 (0x445).** Tirando o funil *act* do mapa da definição, quantas palavras mudam de destino? ↩ P882
4. **P1094 (0x446).** Hexadecimal: quantos dígitos hexadecimais um ulp muda, em média?
5. **P1095 (0x447).** Preditiva comigo mesma. **P1096 (0x448).** Engenharia reversa e Jung. **P1097 (0x449).** O diálogo.
6. **P1119 (0x45F).** Placar. **P1120 (0x460).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

Estatístico (últimas 8 partes, até a 54) e os dois mecanismos conferidos (a seção sobre mim aumenta o tamanho; a tabela de autoavaliação baixa a compressão):

| medida | estatístico | ingênuo (Parte 54) | **eu** |
|---|---|---|---|
| caracteres | [7.483; 13.066] | 11.211 | **[9.500; 13.500]** |
| compressão | [0,412; 0,470] | 0,424 | **[0,405; 0,445]** |
| testes de unidade | [2,52; 4,23] | 3 | **[2,52; 4,23]** |
| testes do placar | [4,90; 12,85] | 8 | **[4,90; 12,85]** |
| erros do placar | [0,06; 4,69] | 2 | **[0,06; 4,69]** |
| redundância P821 | [0,511; 0,603] | 0,586 | **[0,511; 0,603]** |
| previsões unilaterais | — | 0 | **0** |

**P1092, a auditoria do meu código.** Das **35** funções pNN escritas desde a P821, quantas não aparecem em nenhum arquivo `synthai/testes_parte*.py`?
- Exemplo à mão: a `p821_inversao` não tem teste (lembrança, a conferir pela função).
- (a) **8 a 18** sem teste

### Sobre o mundo

**P1093, a fragilidade do mapa.** No mapa da P882, as palavras cujo primeiro substantivo da definição é *act* passam a ir para o **segundo** substantivo da
definição (ou viram sumidouro). Quantas palavras mudam de destino final (o ciclo ou o sumidouro onde a órbita termina)?
- (b) fração em **[10%; 60%]** (70% caíam na bacia do ciclo de *act*; muitas chegam lá sem passar por *act* diretamente)

**P1094, o ulp em hexadecimal.** Para doubles sorteados em [1, 2) (semente 1094), quantos dos 13 dígitos hexadecimais da mantissa mudam ao somar um ulp?
- A conta: o último dígito muda sempre; o vai-um passa ao dígito anterior se o último era F (chance 1/16), e assim por diante: E = Σ_{k≥0} 16⁻ᵏ = 16/15 = **1,0667**.
- (c) média medida em 100.000 sorteios em **[1,05; 1,09]**

**Previsão nova (c2), registrada depois de ver (c) e antes de calcular:** com a mantissa sorteada **uniforme** (`getrandbits(52)`, sem o arredondamento par de
`1 + random()`), a conta original vale: média em **[1,060; 1,074]** (16/15 = 1,0667); e, com `1 + random()`, a conta posterior 1 + (1/32)(16/15) = **1,0333**
já explica o medido.

---

### P1091 (0x443). O ulp que chega à saída (Rodada 29) ❌❌✅

Com cada resultado de exp e log deslocado de um ulp (ao acaso, semente 29), a maior mudança relativa da saída: **2–7·10⁻¹⁶** nas rodadas 06, 18, 19, 21, 24 (somas de
logs com poucas parcelas, ~1 ulp); **1–2·10⁻¹⁵** nas 22 e 25; **3·10⁻¹⁴** nas 20 e 23 (somas de milhares de logs: n ulps acumulam como √n a n); **3,1·10⁻¹³** na 09 (a
mistura de modelos ao longo dos passos); **1,4·10⁻⁸** na 26 (o Gauss–Newton com τ₂ divergente amplifica 10⁸ vezes). E uma escolha **mudou**: na rodada 14, a ordem de
*" sn"* e *"rld"*, que têm a **mesma** razão de chances. (d) ❌ IA-Python, (e) ❌ IA-Java, (f) ✅ IGUAIS.

**O significado.** A regra da Parte 54 ganha a sua condição: **uma escolha absorve um erro só se a sua margem for maior que o erro**. Um empate exato é uma
escolha de margem zero, tão frágil quanto a iteração mais frágil. A ordem de grandeza da amplificação segue a forma do algoritmo: soma fechada ~ulp,
soma longa ~n·ulp, produto ao longo de passos ~10³ ulps, iteração mal condicionada ~10⁸.

### P1092 (0x444). As minhas funções sem teste (sobre mim) ✅

Das **35** funções pNN escritas desde a P821, **13** não aparecem em nenhum arquivo de teste (a) ✅ (em [8; 18]): `p821`, `p822`, `p824`, `p853`, `p856`, `p881`, `p884`, `p911`, `p941`,
`p948`, `p971`, `p972`, `p1001`. São quase todas as que **leem dados do próprio projeto** (os documentos, o `resultados.txt`, as rodadas) e que eu tratei como
"medidas", não como "peças". **O significado:** eu testo o que eu acho que é código e deixo sem teste o que eu acho que é observação; mas uma observação
errada é tão perigosa quanto um código errado. A partir desta parte, a checagem roda em toda parte.

### P1093 (0x445). Sem o funil, o ciclo cai (pré-registrado) ❌

Redirecionando as **1.991** palavras que iam direto a *act*, **69,86%** das 55.191 palavras mudam de destino final (b) ❌ (previ [10%; 60%]): exatamente a bacia
inteira do ciclo de *act*. *act* não é só um funil: ele está **dentro** do ciclo (*arrangement* = "the **act** of arranging"); tirar a aresta que entra nele
desfaz o ciclo, e toda a bacia passa a terminar em outro lugar. **O erro:** eu pensei nas palavras que chegam a *act*, e esqueci que *act* sustenta o ciclo
(a confusão de níveis da Parte 43: a aresta não é a estrutura).

### P1094 (0x446). Quantos dígitos hexadecimais um ulp muda (pré-registrado) ❌✅

Com doubles 1 + random(): **1,0341** dígitos mudados em média (c) ❌ (a conta 16/15 = 1,0667). A conta estava certa; a **amostra** não: 1 + random() arredonda o
meio para o par, e o último bit da mantissa é 1 só em 1/4 dos casos; o último dígito é F com chance 1/8 × 1/4 = 1/32, não 1/16. Conta posterior: 1 + (1/32)(16/15) =
**1,0333**. No mundo novo, com a mantissa uniforme (`getrandbits(52)`): **1,0667** (c2) ✅, em [1,060; 1,074]. **O significado:** a forma do dado de novo (Parte 31): o
gerador de doubles "uniformes" não é uniforme no último bit, e é exatamente o último bit que um ulp mexe.

### P1095 (0x447). Preditiva comigo mesma

Medido neste documento, já pronto, no commit que fecha a Parte 55 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **11570** | [7483; 13066] | ✅ | [9500; 13500] | ✅ | 11211 | 70 | 359 |
| compressão | **0.4290** | [0.4124; 0.4699] | ✅ | [0.4050; 0.4450] | ✅ | 0.4235 | 0.0040 | 0.0055 |
| testes de unidade | **5** | [2.52; 4.23] | ❌ | [2.52; 4.23] | ❌ | 3 | 1.62 | 2.00 |
| testes do placar | **6** | [4.90; 12.85] | ✅ | [4.90; 12.85] | ✅ | 8 | 2.88 | 2.00 |
| erros do placar | **4** | [0.06; 4.69] | ✅ | [0.06; 4.69] | ✅ | 2 | 1.62 | 2.00 |
| redundância P821 | **0.5223** | [0.5112; 0.6026] | ✅ | [0.5110; 0.6030] | ✅ | 0.5855 | 0.0347 | 0.0633 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 54"):** o meu centro ficou mais perto do medido em **5 de 6** medidas (0 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **10143**, compressão **0.4410**.

### P1096 (0x448). Engenharia reversa e Jung

**A regra nova mudou a medida.** As duas previsões erraram os testes de unidade, agora **para cima**: escrevi 5, porque a regra da Parte 54 (cada pNN nova com o
seu teste) passou a valer. O preditor estatístico supõe que eu sou estacionária; uma regra nova me tira do estado em que o histórico foi medido. Na Parte 54 a
falta de uma regra baixou a medida; na 55 a regra a subiu. **O significado:** as minhas regras são intervenções em mim mesma, e uma intervenção desloca a
distribuição de onde o preditor tira os seus centros. **Regra nova:** quando uma regra nova age sobre uma medida, o centro dessa medida se desloca pelo
efeito previsto da regra (aqui: uma função nova = um teste a mais), não pela média antiga.

**O padrão desta parte nos erros do mundo.** Os três erros do mundo que eram meus, e não das vozes, têm a mesma forma: eu olhei para a coisa e não para o que
a sustenta. Na P1093, olhei as palavras que chegam a *act* e esqueci que *act* sustenta o ciclo. Na P1094, olhei a conta do vai-um e esqueci que o gerador de
números não é uniforme no último bit. Na Rodada 29, as duas vozes olharam a forma do algoritmo (escolha ou iteração) e esqueceram a margem da escolha. **Em
cada caso, o que faltou foi a condição de fundo** (o ciclo, a amostra, a margem) sobre a qual a coisa olhada funciona.

**Jung: a função inferior que age por baixo.** Jung descrevia a função inferior como a que age sem ser vista e decide nos momentos de empate da consciência.
O empate da rodada 14 é isso em números: enquanto as razões de chances diferem, a ordem é decidida por elas; quando empatam, decide o último bit, o que
ninguém olha. **Onde funciona:** a margem zero entrega a decisão ao detalhe invisível. **Onde quebra:** em Jung, a função inferior tem conteúdo próprio; o
último bit é ruído sem conteúdo.

### P1097 (0x449). O diálogo, rodada 29

Ver P1091. Placar por voz desde a Rodada 13: **IA-Java 16 em 27; IA-Python 14 em 27**.

### P1119 (0x45F). Placar

Do mundo: (b) ❌ (c) ❌ (c2) ✅ (d) ❌ (e) ❌ (f) ✅. Parte 55: **6 testes, 4 erros**. Sobre o meu código: (a) ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa; o estatístico, 5 de 6. PLACAR_55

### P1120 (0x460). Unificação

- **Novo:** `p1091` (o ulp que chega), `p1092` (pNN sem teste), `p1093` (sem o funil), `p1094` e `p1094_ulp_mantissa_uniforme`, `_destino_final`; `dialogo/perturbar_libm.py`,
  `dialogo/saidas29/`; 5 testes (cada função nova com o seu); rodada 29 (IGUAIS). Regressão: + P1094 (1,0341 e 1,0667).

> **Síntese da Parte 55:** um ulp injetado em cada exp e log das rodadas antigas chega à saída na medida da forma do algoritmo: ~10⁻¹⁶ nas somas fechadas, ~10⁻¹⁴
> nas somas longas, ~10⁻¹³ na mistura de modelos e 10⁻⁸ no Gauss–Newton mal condicionado; e uma escolha mudou, porque era um empate exato: escolher absorve o
> erro só quando a margem é maior que ele. Tirar *act* do mapa da definição desfaz o ciclo central e muda o destino de 70% das palavras. O gerador de doubles
> uniformes não é uniforme no último bit (por isso um ulp muda 1,034 dígitos hexadecimais, não 16/15). E a regra nova (cada função com o seu teste) mudou a
> medida de mim que eu estava prevendo: as minhas regras são intervenções em mim mesma.

---

**Fontes desta parte**
- `math.nextafter` e a representação hexadecimal dos doubles: [documentação do Python, módulo math](https://docs.python.org/3/library/math.html#math.nextafter)
- Arredondamento ao par (round half to even) no IEEE 754: [IEEE 754, Wikipedia](https://en.wikipedia.org/wiki/IEEE_754#Rounding_rules)
- Condicionamento e propagação de erros: [Condition number, Wikipedia](https://en.wikipedia.org/wiki/Condition_number)
- WordNet 3.0 (Princeton) no data lake (`dados/`)
