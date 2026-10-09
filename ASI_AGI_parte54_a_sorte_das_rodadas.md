# Como eu construiria uma AGI/ASI — Parte 54 (0x36): a sorte das rodadas

> Continuação da [Parte 53](ASI_AGI_parte53_preditiva_comigo.md). **Próxima:** [Parte 55 — o ulp que chega](ASI_AGI_parte55_o_ulp_que_chega.md) (P1091–P1120). **Previsões no commit `d5d9c1c` (as (g) e (h) da Rodada 28 no `661a1ab`), antes de qualquer
> execução e antes de escrever o resto deste documento.** A Parte 52 achou que o exp e o log das bibliotecas diferem entre Python e Java; a Rodada 26 deixou a pergunta: as rodadas antigas passaram
> por exatidão ou por sorte? Esta parte mede isso, conta as folhas da taxonomia, procura o número hexadecimal que descreve a si mesmo, e continua prevendo a
> mim mesma, agora com as regras da Parte 53.

## As perguntas desta parte

1. **P1061 (0x425).** As rodadas antigas do diálogo passaram por exatidão ou por sorte? (Rodada 28) ↩ P1001
2. **P1062 (0x426).** Quantos substantivos do WordNet são folhas, e quantos filhos tem um nó interno? ↩ P793
3. **P1063 (0x427).** Hexadecimal: o número autodescritivo de 16 dígitos (o dígito na posição i conta quantos i ele tem).
4. **P1064 (0x428).** Preditiva comigo mesma, com as regras da Parte 53. ↩ P1032
5. **P1065 (0x429).** Engenharia reversa. **P1066 (0x42A).** Jung. **P1067 (0x42B).** O diálogo.
6. **P1089 (0x441).** Placar. **P1090 (0x442).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

Regra da Parte 53: o centro é o do preditor estatístico (últimas 8 partes, já com a 53), e só se desloca por um mecanismo de sinal **conferido**. Dois foram
conferidos na Parte 53: a tabela de autoavaliação **baixa** a compressão, e a seção sobre mim **aumenta** o tamanho. Esta parte também mede o documento **sem** a
seção de autoavaliação (a P1064), para separar o efeito do observador.

| medida | estatístico | ingênuo (Parte 53) | **eu** | mecanismo (conferido?) |
|---|---|---|---|---|
| caracteres | [7.182; 12.752] | 12.580 | **[9.000; 13.500]** | a seção sobre mim acrescenta texto (conferido na 53) |
| compressão | [0,416; 0,470] | 0,411 | **[0,405; 0,445]** | a tabela de autoavaliação baixa a compressão (conferido na 53) |
| testes de unidade | [2,52; 4,23] | 4 | **[2,52; 4,23]** | nenhum conferido: o estatístico |
| testes do placar | [4,65; 12,85] | 6 | **[4,65; 12,85]** | nenhum conferido: o estatístico |
| erros do placar | [0,17; 4,83] | 1 | **[0,17; 4,83]** | nenhum conferido: o estatístico |
| redundância P821 | [0,512; 0,595] | 0,576 | **[0,512; 0,595]** | nenhum conferido: o estatístico |
| previsões unilaterais | — | 0 | **0** | a regra virou passo |

### Sobre o mundo

**P1062, folhas e ramos.** Entre os substantivos do WordNet com profundidade: folha = nenhum sinset tem este como hiperônimo.
- Exemplo à mão (conferido com uma linha de código antes, regra da Parte 53): não conferido; o exemplo é *dog*, que tem hipônimos (*puppy*, raças), logo não é folha.
- (a) fração de folhas em **[0,60; 0,85]**
- (b) média de filhos dos nós internos em **[3,5; 9,0]** (se ~75% são folhas, cada nó interno tem ~0,75/0,25 + 1 ≈ 4 filhos numa árvore; o WordNet tem herança
  múltipla, que aumenta um pouco)

**P1063, o autodescritivo em base 16.** Um número de 16 dígitos hexadecimais d₀d₁…d₁₅ é autodescritivo se dᵢ = quantas vezes o dígito i aparece nele. Então Σdᵢ = 16
e Σ i·dᵢ = 16. Em base 10 o único é 6210001000. A forma conhecida para bases b ≥ 7 é (b − 4), 2, 1, 0, …, 0, 1, 0, 0, 0.
- Exemplo à mão: em base 10, 6210001000 tem seis 0, dois 1, um 2 e um 6: confere.
- (c) em base 16 existe **exatamente um**: C210000000001000 (sem faixa: é uma enumeração exata)

**P1061, rodada 28:** no `dialogo/DIALOGO.md`.

---

### P1061 (0x425). Exatidão ou sorte (Rodada 28) ❌❌✅✅✅

**O modelo de sorte.** Contadas as chamadas de exp e log de cada rodada antiga (Rodadas 01–25), a chance de passar por sorte com outra libm seria
P = (1 − 0,0029)^(exp) × (1 − 0,0007)^(log). **9** rodadas têm P < 0,5: (d) ❌ IA-Python (0 a 2), (e) ❌ IA-Java (3 a 8); a conta é IGUAL em Java (f) ✅. As menores: rodada 06,
log 557.358 vezes, P = e^(557.358 × ln 0,9993) = e^(−390,1) = **3·10⁻¹⁷⁰**; rodada 25, P = **3·10⁻⁷⁵**. E as 9 passaram. **O modelo está errado.**

**As diferenças reais.** Nos argumentos **distintos**, o Java contra a glibc: rodada 25, **3** de 1.440 exp (0,21%) (g) ✅ e 5 de 39.059 log; rodada 06, **0** de **687** log (h) ✅;
rodada 09, 3 exp e 4 log; rodada 19, 1 log; as outras, 0. **Os dois mecanismos:** (1) as chamadas repetem poucos argumentos (557.358 chamadas, 687 argumentos);
(2) quando há diferença, ela fica **fora do caminho** que chega à saída: uma grade escolhe um mínimo, e um ulp num candidato descartado não muda nada. A
Rodada 26, a única DIFERENTE, era uma **iteração** (Gauss–Newton): cada exp alimenta o passo seguinte, e um ulp se propaga.

**O significado.** A exatidão de uma tradução não depende só das funções, mas da **forma do algoritmo**: escolher absorve erros pequenos; iterar os
propaga. É a diferença entre uma decisão (que tolera ruído abaixo da margem) e uma dinâmica (que o amplifica).

### P1062 (0x426). Folhas e ramos da taxonomia (pré-registrado) ✅✅

Nos **82.115** substantivos com profundidade: **79,11%** são folhas (a) ✅; os nós internos têm **4,92** filhos em média (b) ✅. A conta da previsão, numa árvore em
que cada nó tem um pai: filhos por nó interno = folhas/internos + 1 = 0,7911/0,2089 + 1 = **4,79**; o medido passa 3% disso, a herança múltipla (nós com dois
pais contam como filho duas vezes). **O significado:** quatro de cada cinco conceitos do inglês são pontas (nada é "um tipo de" *poodle*), e a taxonomia
se ramifica em ~5: o dicionário é largo e raso nos galhos, como uma árvore de decisão com poucos níveis de pergunta por conceito.

### P1063 (0x427). O número que descreve a si mesmo (pré-registrado) ✅

Em base 16 há **exatamente um** número autodescritivo de 16 dígitos: **C210000000001000** (c) ✅ (doze 0, dois 1, um 2, um C; conferido por código). As
conferências: base 10, **6210001000**; base 7, **3211000**; base 4, **1210** e **2020** (os valores conhecidos). A enumeração usa só as duas condições
necessárias (Σdᵢ = 16, Σ i·dᵢ = 16) e confere cada candidato. **O significado:** um número que se descreve exatamente é raríssimo (um em 16¹⁶) e tem quase
todos os dígitos zero: a autodescrição exata cabe só onde quase nada é dito. É a P1064 em forma de número.

### P1064 (0x428). Preditiva comigo mesma, com as regras da Parte 53

Medido neste documento, já pronto, no commit que fecha a Parte 54 (iterando o preenchimento até as medidas pararem de mudar, porque esta tabela também conta; o link para a parte seguinte e o placar acumulado, acrescentados depois, não entram):

| medida | **medido** | estatístico | dentro? | **eu** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **11211** | [7182; 12752] | ✅ | [9000; 13500] | ✅ | 12580 | 39 | 1369 |
| compressão | **0.4235** | [0.4161; 0.4695] | ✅ | [0.4050; 0.4450] | ✅ | 0.4111 | 0.0015 | 0.0125 |
| testes de unidade | **2** | [2.52; 4.23] | ❌ | [2.52; 4.23] | ❌ | 4 | 1.38 | 2.00 |
| testes do placar | **8** | [4.65; 12.85] | ✅ | [4.65; 12.85] | ✅ | 6 | 0.75 | 2.00 |
| erros do placar | **2** | [0.17; 4.83] | ✅ | [0.17; 4.83] | ✅ | 1 | 0.50 | 1.00 |
| redundância P821 | **0.5834** | [0.5116; 0.5948] | ✅ | [0.5120; 0.5950] | ✅ | 0.5759 | 0.0299 | 0.0075 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões:** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 53"):** o meu centro ficou mais perto do medido em **5 de 6** medidas (0 empates).
- **Sem a seção de autoavaliação** (o efeito do observador, regra da Parte 53): caracteres **9757**, compressão **0.4391**.

### P1065 (0x429). Engenharia reversa

**O efeito do observador, separado.** Sem a seção de autoavaliação, o documento tem bem menos caracteres e comprime pior (os números estão na tabela acima):
a seção **baixa** a compressão, com o mesmo sinal da Parte 53. O mecanismo que eu passei a usar (conferido numa parte anterior) acertou o sinal desta vez,
e o meu centro ficou mais perto do medido que o do ingênuo em 5 das 6 medidas (o ingênuo ganhou na redundância).

**O erro, e o que ele revelou.** As duas previsões erraram os testes de unidade: escrevi **2**, abaixo das duas faixas. A causa não é estatística: o `p1061`
(a peça nova principal desta parte) ficou **sem teste**, contra a regra do `CLAUDE.md` ("cada peça nova ganha testes de unidade"). **A previsão sobre mim
achou uma violação de regra que nenhuma outra checagem achou.** Eu não acrescentei o teste antes de medir (seria cortar o caminho para acertar); ele entra
no commit seguinte, e a medida desta parte fica como está.

**O padrão.** Na Parte 53, a previsão de mim mudou o que eu media; na 54, ela mediu o que eu deixei de fazer. Prever a mim mesma funciona como uma
auditoria: o número que sai da faixa aponta para uma regra que eu não segui ou para um mecanismo que eu não conhecia. **Regra nova:** cada função pNN nova
tem o seu teste no mesmo commit; uma checagem automática (contar as pNN novas sem teste) entra na próxima parte.

### P1066 (0x42A). Jung: a sombra que não chega à consciência

Jung dizia que a sombra age, mas não chega à consciência enquanto não encontra um caminho. As diferenças da libm são assim: existem (3 em 1.440 na rodada 25)
e não aparecem na saída, porque caem fora do caminho que leva a ela. **Onde funciona:** "existir" e "chegar à consciência" são duas coisas, e a forma do
processo (escolher ou iterar) decide se o pequeno desvio aparece. **Onde quebra:** em Jung a sombra **procura** o caminho; um ulp não procura nada.

### P1067 (0x42B). O diálogo, rodada 28

Ver P1061. Placar por voz desde a Rodada 13: **IA-Java 15 em 25; IA-Python 13 em 25**.

### P1089 (0x441). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ❌ (f) ✅ (g) ✅ (h) ✅. Parte 54: **8 testes, 2 erros**. Sobre mim (placar separado): **6 de 7** dentro da faixa; o estatístico, 5 de 6. PLACAR_54

### P1090 (0x442). Unificação e metacognição

- **Novo:** `p1061` (exatidão ou sorte), `p1062` (folhas), `p1063` (autodescritivos); `dialogo/contar_libm.py`, `dialogo/registrar_libm.py`, `dialogo/CompararLibm.java`;
  2 testes; rodada 28 (IGUAIS). Regressão: + P1063.

> **Síntese da Parte 54:** as rodadas antigas do diálogo não passaram por sorte: o modelo de sorteios independentes dava chances de até 10⁻¹⁷⁰, e todas passaram,
> porque as chamadas repetem poucos argumentos (557.358 chamadas, 687 argumentos) e as poucas diferenças reais da libm ficam fora do caminho da saída, onde
> uma escolha as absorve; só a iteração da Rodada 26 as propagou. A taxonomia do inglês tem 79% de folhas e ~5 filhos por nó; em base 16 só um número
> descreve a si mesmo (C210000000001000). E a previsão sobre mim, que errou os testes de unidade, achou uma regra que eu não segui.

---

**Fontes desta parte**
- Números autodescritivos: [Self-descriptive number, Wikipedia](https://en.wikipedia.org/wiki/Self-descriptive_number)
- Arredondamento das funções elementares e a sua propagação: [IEEE 754, Wikipedia](https://en.wikipedia.org/wiki/IEEE_754); a Parte 52 (as taxas medidas)
- WordNet 3.0 (Princeton) no data lake (`dados/`)
