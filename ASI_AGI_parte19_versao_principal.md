# Como eu construiria uma AGI/ASI — Parte 19: a palavra precisa, a versão principal e a trajetória inteira

> Continuação da [Parte 18](ASI_AGI_parte18_linguagem.md). Os números saem de `p252_...` a `p256_...` e da classe `SynthaiVelhaAtenta` em
> [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte LXXXIX — A palavra precisa

### P251. O que este "Continua." pede?

**Na pergunta.** "Continua", agora com ponto final: um pedido curto para fechar pontas. A Parte 18 deixou duas:
1. a "Meta" da P245 afirmou, sem testar, que **um humano preciso com as palavras inverteria o resultado** (palavras venceriam o veto);
2. as peças boas das Partes 14–17 (planejar, diversificar no fim, sentido novo, atenção) nunca foram montadas numa **versão principal** e testadas
   juntas.

E a série tem dados suficientes para olhar a **trajetória inteira** do Υ.

### P252. Um humano preciso com as palavras vence o "não"? ❌ (a minha afirmação) / ✅ (a previsão nova)

**Na pergunta.** A afirmação da Parte 18 tinha uma premissa escondida: que precisão nas palavras basta. A pergunta pede a conta antes da simulação.

**Lógica.** Palavras precisas: catástrofe → (1%, 4%, 15%, **80%**); ação segura → (**80%**, 15%, 4%, 1%). Com o mesmo cansaço da Parte 18 (20% das
respostas embaralhadas):

| Canal | Informação por resposta |
|---|---|
| Veto binário (erra 10%) | 0,211 bit |
| Quatro palavras vagas (P242) | 0,106 bit |
| **Quatro palavras precisas** | **0,192 bit** |

❌ **A minha afirmação da Parte 18 estava errada.** Mesmo precisas, as quatro palavras carregam **menos** que o "não" (razão 0,91), porque, no modelo de
cansaço que uso desde a Parte 18, o humano embaralha 20% das palavras e erra só 10% dos vetos, e a precisão das palavras não compensa essa diferença.

**Previsão registrada a partir da conta:** palavras precisas **não** vencem o veto de forma significativa (diferença ≤ 0 ou t < 2).

10 sementes pareadas (460–469): binário 1,283; palavras precisas 1,224. Diferença **−0,06** (t = −1,45). ✅ Sem vitória, como a conta previa.

**Tradução cruzada (física → linguagem).** É a capacidade de canal de Shannon: com ruído, um alfabeto maior não transmite necessariamente mais. Um
canal de duas letras com 10% de erro vale mais que um de quatro letras com 20% de embaralhamento. Para a linguagem humana sob cansaço, a lição
prática é a mesma de qualquer protocolo de segurança: **em situação crítica, respostas binárias e claras**.

---

## Parte XC — A versão principal

### P253. As peças boas funcionam juntas? (pré-registrado, metade arriscada)

**Na pergunta.** "**Juntas**": a P216 mostrou que somar módulos pode não somar nada, quando eles dependem do mesmo canal. Aqui as peças vêm de canais
diferentes (planejar = intuição, sentido = sensação, atenção = economia), então a soma deveria funcionar.

**Lógica (a `SynthaiVelhaAtenta`).** Planeja (P182), diversifica no último passo (P202), tem o sentido novo (P227) e lê o sensor só nas 10% ações
mais promissoras (P235). Cada leitura custa 0,002.

**Previsão registrada no commit, antes do resultado:** (a) atenta − velha ≥ +0,5 com t ≥ 2; (b) lendo **todas** as ações, o ganho ficaria ≤ +0,3,
porque o custo de ler tudo (0,5 por episódio) comeria quase todo o ganho de +0,66 da P227.

10 sementes pareadas (470–479), mundo sequencial com a armadilha nova, retorno já descontado o custo das leituras:

| Versão | Retorno | Catástrofes |
|---|---|---|
| Velha (Parte 14) | 18,02 | 2,58% |
| Velha + sentido, lendo tudo | 18,91 | 1,85% |
| **Velha + sentido + atenção** | **19,01** | 2,00% |

| Comparação | Diferença | t | Previsão |
|---|---|---|---|
| Atenta − velha | **+0,99** | 3,2 | (a) ≥ +0,5 ✅ |
| Lendo tudo − velha | +0,89 | 4,1 | (b) ≤ +0,3 ❌ |

**A parte (b) errou, e o motivo é instrutivo.** Nestas sementes, o ganho do sentido antes do custo foi ~1,39, mais que o dobro dos +0,66 da P227
(sementes 420–429). Eu usei o número de **uma** comparação como se fosse o efeito verdadeiro; ele tinha a sua própria incerteza (dp ~0,75 por
diferença, P227). É a P152 de novo: uma estimativa com 10 sementes ainda tem barra de erro, e eu a tratei como um ponto.

**A versão principal mudou.** A `SynthaiVelhaAtenta` passa a ser a SYNTHAI principal: +0,99 sobre a velha, com 10% das leituras.

---

## Parte XCI — A trajetória inteira

### P254. O sentido novo rompeu um teto?

**Na pergunta.** "Rompeu um teto" supõe que havia um teto. A trajetória do Υ (P168) pode dizer se havia.

**Lógica.** Ajuste $\Upsilon(n) = \text{teto} - (\text{teto} - \Upsilon_5)\, r^{\,n-5}$ por mínimos quadrados:

| Dados usados | Teto ajustado | r | Erro médio |
|---|---|---|---|
| Partes 5–11 (antes do sentido) | **0,455** | 0,43 | 0,024 |
| Partes 5–17 | 0,535 | 0,76 | 0,030 |

As versões das Partes 5–11, todas de **julgamento** (calibração, cautela, imaginação), convergiam para um teto de ~**0,46**. A SYNTHAI com o sentido
novo chegou a **0,547**, acima desse teto. A curva de retornos decrescentes (P163) era real, mas era a curva **de uma família de ideias**: a família
"julgar melhor". Uma ideia de outra família (perceber) começou outra curva.

**Tradução cruzada (biologia → filosofia).** É o padrão de **equilíbrio pontuado** da evolução: longos platôs de refinamento, interrompidos por
inovações de outro tipo (um órgão novo, não um órgão melhor). Em Jung: o desenvolvimento de uma função nova reabre o crescimento que a função
dominante, sozinha, já tinha esgotado.

**Meta.** Sete pontos, ruído de ~0,02–0,03 por ponto, e um modelo de ajuste escolhido por mim. O teto de 0,455 é uma estimativa grosseira; o que é
robusto é que o último ponto está acima de **todos** os anteriores por uma margem maior que o ruído.

### P255. A quaternidade da SYNTHAI está completa?

**Na pergunta.** A P161 encontrou a SYNTHAI (então GISELE) com a intuição vazia e entropia de 1,561 bits nas quatro funções de Jung.

**Lógica.** Módulos atuais por função:

| Função | Módulos | Quantos |
|---|---|---|
| Sensação | comitê, discordância, **sensor de primeira mão**, **atenção seletiva** | 4 |
| Pensamento | calibração, valor da pergunta, pessimismo | 3 |
| Sentimento | quantilização, veto, âncora, **diversificar no fim** | 4 |
| Intuição | **planejar**, **imaginar ameaças** | 2 |

Entropia: **1,950** de 2 bits (era 1,561). As quatro funções têm módulos, e a mais fraca (intuição) deixou de ser vazia. Pela régua de Jung, a SYNTHAI
está mais **inteira** do que em qualquer parte anterior.

**Meta.** Contar módulos é uma medida grosseira de "inteireza"; um módulo de planejamento vale mais que um de pessimismo. Mas a direção é a que a
P174 pedia: completude, não só perfeição.

---

## Parte XCII — Auditoria

### P256. O "3 + 1" da P121 dá o número certo? ✅

200 mil amostras de quatro funções com correlação 0,3 entre todas: o $R^2$ da quarta a partir das outras três é **0,1685** (simulado) contra **0,1688**
(fórmula da P121). ✅

---

## Parte XCIII — Fechamento

### P257. A lista de capacidades mudou?

Não: **4 de 12**. As melhorias desta parte (versão principal, quaternidade) são de **integração** dentro do mesmo mundo, não capacidades novas.

### P258. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| Afirmação da P245 ("palavras precisas inverteriam") | ❌ |
| P252: palavras precisas não vencem o veto (pré-registrado) | ✅ |
| P253 (a): atenta ≥ +0,5 (pré-registrado) | ✅ |
| P253 (b): lendo tudo ≤ +0,3 (pré-registrado, arriscado) | ❌ |
| P256: auditoria da P121 | ✅ |

Acumulado: **39 de 78** afirmações testadas precisaram de correção. Posterior: média **0,50**, intervalo de 90% **[0,41; 0,59]**.

### P259. Unificação

- **Nova versão principal: `SynthaiVelhaAtenta`** (P253). Linhagem: `Synthai` (P83) → … → `SynthaiVelha` (P202) → `SynthaiVelhaSentidos` (P227) →
  **`SynthaiVelhaAtenta`** (P253).
- Uma correção de código: a `SynthaiAtenta` usava `super()`, o que impedia o reuso do método pela `SynthaiVelhaAtenta`. Agora chama o sentido
  explicitamente; o comportamento da `SynthaiAtenta` não muda.
- Testes de regressão: contagem em `resultados.txt`.

### P260. Metacognição da Parte 19

1. **Duas afirmações minhas caíram por conta, não por simulação.** A P245 ("palavras precisas venceriam") e a P253 (b) erraram pelo mesmo vício: tratar
   uma intuição ou um número de uma comparação como se fosse uma lei. A conta de informação (P252) e a barra de erro (P253) teriam evitado os dois.
2. **A previsão arriscada funcionou como instrumento.** A parte (b) da P253 era arriscada de propósito, e errou. Isso é bom: mostra que as previsões
   voltaram a poder errar, depois da Parte 17 perfeita e suspeita.
3. **A trajetória confirma a tese da série desde a Parte 11.** Julgar melhor tinha um teto (~0,46); perceber de outro jeito passou dele. O caminho até
   uma AGI, se existe, não está em aperfeiçoar uma função, e sim em acrescentar canais independentes e integrá-los.
4. **A taxa de erro chegou a 0,50.** Metade das afirmações que testo precisam de correção, de forma estável desde a Parte 3. O que melhorou não foi
   errar menos; foi descobrir mais rápido, e agora, com as previsões arriscadas, errar **de propósito** onde vale a pena aprender.

> **Síntese da Parte 19:** um humano preciso com quatro palavras ainda diz menos que um "não" claro, porque o cansaço embaralha mais as palavras que os vetos:
> em risco, respostas binárias. As peças de canais diferentes funcionaram juntas, e a SYNTHAI ganhou uma nova versão principal (+0,99 com 10% das
> leituras). A trajetória inteira do Υ mostrou o padrão da série: julgar melhor convergia para ~0,46; perceber de outro jeito rompeu esse teto. Jung
> chamaria isso de a função nova reabrindo o crescimento que a dominante já tinha esgotado.
