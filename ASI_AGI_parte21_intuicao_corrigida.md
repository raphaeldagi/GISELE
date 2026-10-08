# Como eu construiria uma AGI/ASI — Parte 21: a intuição corrigida pela sensação

> Continuação da [Parte 20](ASI_AGI_parte20_o_que_cada_funcao_vale.md). **Próxima:** [Parte 22 — o protótipo em módulos](ASI_AGI_parte22_prototipo_em_modulos.md) (P281–P290). Os números saem de `p272_...`, `p274_...`, `p275` (Υ sequencial da P265) e
> `p277_...`, e da classe `SynthaiIntuicaoCalibrada` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões registradas no commit `6beb772`, antes de rodar.**

---

## Parte C — Onde a função dominante falha

### P271. O que este "Continue" pede?

**Na pergunta.** A Parte 20 mostrou que a **intuição** (planejar) é a função dominante da SYNTHAI: vale 14, o resto menos de 1. E mostrou onde ela falha:
no mundo em que o **modelo de mundo é ruim** (σ = 2), o Υ sequencial cai de ~0,71 para **0,41**. "Continue" pede melhorar a função que mais importa,
no lugar onde ela é mais fraca.

**O que a SYNTHAI faz hoje.** Ela usa a estimativa $\hat c$ do modelo de mundo como se fosse verdade: bônus de plano $= \hat c \times$ passos restantes.
Com um modelo bom, tudo bem. Com um modelo ruim, ela segue o **ruído** do modelo com a mesma confiança com que seguiria um sinal. É a intuição sem
correção, o defeito que Jung atribuía ao tipo intuitivo: viver nas possibilidades e ignorar o que os fatos dizem.

### P272. Quanto se deveria confiar num modelo ruidoso, em teoria? ✅

**Na pergunta.** "Quanto confiar" pede um **peso**, um número entre 0 (ignorar o modelo) e 1 (acreditar nele inteiro).

**Lógica.** Se a consequência real é $c \sim \mathcal N(0,1)$ e o modelo vê $\hat c = c + \mathcal N(0, \sigma)$, a melhor estimativa de $c$ dado $\hat c$ é
$$
\mathbb E[c \mid \hat c] = \frac{\hat c}{1 + \sigma^2}.
$$
O peso ótimo é $w^\* = 1/(1+\sigma^2)$: **0,80** com o modelo bom ($\sigma = 0{,}5$) e **0,20** com o ruim ($\sigma = 2$). Simulando a escolha entre 50 ações
($r = 2$):

| σ do modelo | Peso ótimo simulado | Teoria | Valor com peso 1 | Valor com o peso ótimo |
|---|---|---|---|---|
| 0,5 | 0,80 | 0,80 | 4,615 | 4,635 |
| 2 | **0,20** | **0,20** | 2,492 | **3,054** (+23%) |

✅ A teoria acerta exatamente. Com o modelo bom, confiar demais quase não custa; com o ruim, custa 23%.

---

## Parte CI — Aprender quanto confiar

### P273. Como a SYNTHAI pode descobrir sozinha o quanto confiar no próprio modelo?

**Na pergunta.** "Sozinha" exclui dar a ela o σ verdadeiro. A pergunta da Parte 7 volta: o que ela **pode** saber?

**Lógica (a `SynthaiIntuicaoCalibrada`).** Depois de agir, a SYNTHAI vê o próprio **nível** mudar. Essa mudança é a consequência real $c$ da ação que ela
escolheu. Ela guarda os pares ($\hat c$, $c$) e estima o peso por regressão pela origem:
$$
w = \frac{\sum \hat c\, c}{\sum \hat c^{\,2}},
$$
começando com $w = 1$ (força de 10 pares). O bônus de plano vira $w \times \hat c \times$ passos restantes.

Um detalhe que importa: ela só aprende com as ações que **escolheu**, e escolhe as de $\hat c$ alto. Isso não enviesa a inclinação, porque a seleção é pela
variável $\hat c$, não por $c$: selecionar pelo eixo x não muda a reta de y em x. (A P145 mostrou o caso oposto, em que a seleção estragava o
aprendizado; lá, a SYNTHAI aprendia a probabilidade de catástrofe só com ações que já achava seguras.)

**Tradução cruzada (Jung → aprendizado).** É exatamente a compensação que Jung recomendava ao tipo intuitivo: desenvolver a **sensação**, a função que
registra o que aconteceu de fato, e deixar que ela corrija a intuição. A intuição propõe; a sensação confere.

### P274. A intuição calibrada é melhor? (pré-registrado)

**Previsões registradas:** (a) com o modelo ruim, ganho ≥ +1,0 com t ≥ 2; (b) no mundo base, |diferença| < 0,5; (c) o peso aprendido fica a menos de
0,05 de $1/(1+\sigma^2)$.

10 sementes pareadas (500–509), 400 episódios:

| Mundo | Calibrada − versão principal | t | Peso aprendido | Teoria |
|---|---|---|---|---|
| Base (σ = 0,5) | **+0,23** | 2,7 | **0,801** | 0,800 |
| Modelo ruim (σ = 2) | **+0,68** | **5,1** | **0,201** | 0,200 |

- (a) ❌ O ganho com o modelo ruim é claro (t = 5,1), mas é **+0,68**, abaixo do +1,0 previsto.
- (b) ✅ No mundo base não houve prejuízo; houve até ganho (+0,23, t = 2,7).
- (c) ✅ O peso aprendido acertou a teoria com erro de **0,001**, nos dois mundos, só com a observação do próprio nível.

---

## Parte CII — O Υ sequencial

### P275. O Υ sequencial sobe? (pré-registrado) ❌

**Previsões registradas:** Υ no mundo de modelo ruim ≥ 0,50 (era 0,41); Υ sequencial total ≥ 0,72 (era 0,706).

| Mundo | Versão principal | Calibrada |
|---|---|---|
| Base | 0,741 | 0,740 |
| Armadilha nova | 0,705 | 0,691 |
| Catástrofe ×2 | 0,711 | 0,737 |
| **Modelo ruim** | 0,414 | **0,440** |
| Humano frágil | 0,715 | 0,710 |
| **Υ total** | 0,706 | **0,708** |

❌ As duas previsões falharam: o mundo do modelo ruim subiu só de 0,41 para 0,44, e o total ficou praticamente igual.

### P276. Por que um peso perfeito rende tão pouco?

**Na pergunta.** O peso aprendido está certo (0,201 contra 0,200), e a teoria diz que o peso certo rende 23% na escolha (P272). Mas o Υ do modelo ruim só
subiu 6%. A diferença entre os dois números pede o mecanismo.

**Lógica (hipótese).** A P272 escolhe a **melhor** de 50 ações pelo escore. A SYNTHAI não faz isso: por segurança, ela **sorteia** entre as 5% melhores (a
quantilização da P42; com 50 ações, isso dá 2 candidatas), e no último passo entre as 20% melhores (P202). Um escore mais bem pesado só muda **quais duas**
candidatas entram no sorteio, e o sorteio dilui o ganho. A cautela, que protege contra as armadilhas, também protege a SYNTHAI de aproveitar uma
percepção melhor.

**Tradução cruzada (Jung → engenharia).** Jung dizia que as funções se limitam umas às outras: o sentimento (aqui, a cautela de não ir ao extremo) contém a
intuição. É o preço de ter as quatro funções juntas: nenhuma age com força total.

**Meta.** É uma hipótese, não um resultado. O teste é direto (aumentar o número de candidatas no sorteio quando a calibração da intuição é confiável) e fica
registrado como próxima pergunta.

---

## Parte CIII — Auditoria

### P277. O horizonte da imaginação (P149) vale com erros aleatórios? ✅

**Na pergunta.** A P149 calculou o horizonte com um erro **fixo** por passo. Erros reais variam. A pergunta é se a fórmula ainda vale como mediana.

| Erro médio por passo | Horizonte mediano simulado | Fórmula da P149 |
|---|---|---|
| 1% | 42 | 40,7 |
| 5% | 9 | 8,3 |
| 10% | 5 | 4,3 |

✅ A simulação dá o primeiro passo **inteiro** depois do ponto da fórmula, como esperado. A fórmula serve como estimativa da mediana mesmo com erro aleatório.

---

## Parte CIV — Fechamento

### P278. A lista de capacidades mudou? (↩ P170)

Não: **4 de 12**. Mas o item "modelo causal do mundo" ganhou uma primeira peça: a SYNTHAI agora **mede a qualidade do próprio modelo** com o que observa.
Ela ainda não aprende o modelo; aprende quanto confiar nele.

### P279. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P272: o peso ótimo é 1/(1+σ²) | ✅ |
| P274 (a): ganho ≥ +1,0 com modelo ruim (pré-registrado) | ❌ (+0,68) |
| P274 (b): sem prejuízo no mundo base (pré-registrado) | ✅ |
| P274 (c): peso aprendido a ±0,05 da teoria (pré-registrado) | ✅ (±0,001) |
| P275: Υ do modelo ruim ≥ 0,50 (pré-registrado) | ❌ (0,44) |
| P275: Υ sequencial total ≥ 0,72 (pré-registrado) | ❌ (0,708) |
| P277: auditoria da P149 | ✅ |

Acumulado: **45 de 91** afirmações testadas precisaram de correção. Posterior: média **0,49**, intervalo de 90% **[0,41; 0,58]**.

### P280. Unificação e metacognição

- **Nova versão principal: `SynthaiIntuicaoCalibrada`** (P274): é melhor que a anterior nos dois mundos testados (+0,23 e +0,68, t > 2,5). Linhagem:
  … → `SynthaiVelhaAtenta` (P253) → **`SynthaiIntuicaoCalibrada`** (P274).
- Testes de regressão: **50/50** reproduzidos; o arquivo tinha **162** funções `pNN` ao fim da Parte 21. (Conferido na execução completa da
  Parte 22, que inclui estes 50 testes; a execução das Partes 1–21 foi interrompida quando a Parte 22 mudou o código.)

**Metacognição.**
1. **O resultado mais limpo da série**: a SYNTHAI descobriu sozinha o peso que a teoria manda, com erro de 0,001, olhando só para o próprio nível. Quando o
   problema é bem posto (uma regressão sem viés de seleção), aprender funciona exatamente como a matemática diz.
2. **Três das sete previsões falharam, todas pelo mesmo motivo:** eu transferi o ganho da teoria (23% numa escolha pura) para um agente que **não** escolhe
   de forma pura. É a regra da Parte 12 de novo ("verificar se o mecanismo é o mesmo"): a P272 e a SYNTHAI não escolhem da mesma maneira.
3. **A lição de arquitetura** (P276): as funções da SYNTHAI se limitam umas às outras. A cautela que a protege também impede que uma percepção melhor se
   transforme em decisão melhor. O próximo ganho talvez não esteja em perceber mais, e sim em **soltar a cautela onde a percepção é confiável**.

> **Síntese da Parte 21:** a intuição da SYNTHAI aprendeu a se corrigir pela sensação: olhando o que de fato acontecia, ela descobriu sozinha que devia confiar
> 80% no modelo bom e 20% no ruim, exatamente o que a teoria manda. Ganhou nos dois mundos e virou a nova versão principal. Mas o ganho foi menor que o previsto,
> porque a cautela que sorteia entre as melhores ações dilui qualquer percepção melhor. Jung diria que as funções se contêm umas às outras; a próxima
> pergunta é quando deixar de conter.
