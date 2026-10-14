# Como eu construiria uma AGI/ASI — Parte 89 (0x59): o substrato que aprende

> Continuação da [Parte 88](ASI_AGI_parte88_a_arquitetura_autopoietica_recebida.md). Sem texto novo do usuário: sigo o ciclo (Parte 44/75). A Parte 86 construiu o neurônio pulsado (LIF, Izhikevich) e a regra
> STDP, mas só mediu neurônios isolados. Aqui faço o substrato **aprender**: a STDP não supervisionada muda os pesos, e a pergunta é se ela faz o que a literatura afirma — tornar uma sinapse seletiva à
> correlação — e se o faz no meu regime pequeno (a lição das Partes 84 e 87: um efeito famoso pode não aparecer fora da sua escala, então a conta vem antes).
>
> **A âncora algébrica (Parte 70):** a STDP é Hebb com janela temporal. A deriva esperada de um peso é a integral da janela vezes a correlação pré-pós — uma forma fechada. Começo por ela (que não depende de
> regime), e só depois arrisco o efeito de competição (que depende).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[3 + S; 7 + S]** | funções de STDP + a rodada |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

A âncora é a forma fechada (não depende de regime); as (b) e (c) foram calibradas num teste de fumaça (200 pares; semente 89) e PREVEEM tamanhos/sementes que a fumaça não usou, para serem previsões de
verdade. Contas fechadas e sinais não levam o fator 1,36; as faixas de simulação levam.

- **(a)** a integral da janela STDP A₊τ₊ − A₋τ₋: balanceada (A₊=A₋=0,1; τ=20) = **0,0**; depressão dominante (A₋=0,12) = **−0,4** (exato). E a deriva de um peso sob pré e pós de Poisson INDEPENDENTES tem o SINAL da
  integral: **negativa** na depressão dominante (categórico)
- **(b)** a propriedade definidora da STDP, com **500** pares (a fumaça usou 200): uma sinapse cujo pré precede o pós (Δt = +5 ms) potencia e uma cujo pré segue o pós (Δt = −5 ms) deprime; o peso "pré antes" em
  **[3,5; 6,0]** e o "pré depois" **< 0** (parte de w₀ = 0,5; categórico no sinal, faixa no tamanho)
- **(c)** a competição sináptica num neurônio LIF de brinquedo (10 correlacionadas, 40 ruído), com uma **semente nova (90)** e 8000 ms: os dois grupos NÃO se separam — ambos saturam perto de wmax = 1,0 e
  |correlacionadas − ruído| **< 0,15** (o efeito de Song-Miller-Abbott não aparece nesta escala sem ajuste fino; a lição das Partes 84 e 87)
- **(d)** a rodada 56: uma população de neurônios de Izhikevich acoplados dá a MESMA trajetória bit a bit em Python e Java (categórico: IGUAL)
- **(e)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–89 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2111–P2112 (0x83F–0x840).** A STDP não supervisionada: para onde ela empurra um peso, e isso tem forma fechada? ↩ P2026 (STDP)
2. **P2113 (0x841).** A propriedade definidora da STDP (pré antes potencia, pré depois deprime) aparece de forma robusta? ↩ P2026
3. **P2114 (0x842).** A competição sináptica (Song-Miller-Abbott) aparece num neurônio de brinquedo? ↩ P2053 (plasticidade)
4. **A rodada 56.** Uma população de neurônios de Izhikevich acoplados, bit a bit. ↩ rodada 53 (Izhikevich)
5. **P1961 (continuando), P2139–P2140.** O teste (e), engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **5.0000** | ✅ |
| (m2) | [0; 3] | **0.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.1748** | ✅ |
| (m4) | [0.45; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 3] | **0.0000** | ✅ |
| (m6) | [0; 3] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P2111–P2112 (0x83F–0x840). A deriva da STDP tem forma fechada ✅✅

**Na pergunta.** A Parte 86 construiu a STDP mas só a aplicou a pares isolados. A pergunta nova: num regime de disparos, para onde a STDP empurra um peso, em média? A resposta já existe (Kempter, Gerstner e
van Hemmen, 1999): a deriva esperada por par pré-pós é a integral da janela, A₊τ₊ − A₋τ₋, vezes a correlação pré-pós.

**Lógica (a conta, com a substituição).** Com A₊ = 0,1, τ₊ = 20, A₋ = 0,12, τ₋ = 20: a integral = 0,1·20 − 0,12·20 = 2,0 − 2,4 = **−0,4**; balanceada (A₋ = 0,1): 2,0 − 2,0 = **0,0** (`p2111`). Para pré e pós de
Poisson INDEPENDENTES (correlação só pela taxa), a deriva simulada (8000 ms) foi **−2,61**, do SINAL da integral (negativo) (a) ✅. A depressão dominante faz o peso de uma entrada não correlacionada decair — é
o mecanismo da competição. **Geometria:** a janela STDP é um núcleo antissimétrico-ponderado; a sua integral é o produto interno da janela com a função constante, e esse número decide a direção.

### P2113 (0x841). A propriedade definidora, robusta ✅

A assinatura da STDP: pré antes do pós potencia; pré depois deprime. Com 500 pares a Δt = ±5 ms (de w₀ = 0,5): "pré antes" = **4,394** (potenciou) e "pré depois" = **−3,783** (deprimiu) (b) ✅. É robusto porque
não depende de regime — é só o sinal da janela, aplicado muitas vezes. Esta é a peça do substrato pulsado que **funciona** sem ajuste: a direção da mudança é determinada pela ordem dos disparos.

### P2114 (0x842). A competição que não apareceu ✅ (previsão de não-efeito)

**Na pergunta.** O resultado clássico (Song, Miller e Abbott, 2000): sob STDP de depressão dominante, sinapses correlacionadas vencem e as não correlacionadas decaem a zero. Testei num neurônio LIF de brinquedo
(10 correlacionadas, 40 ruído), e, pela regra das Partes 84 e 87, rodei um teste de fumaça ANTES de prever.

**Medido (semente nova 90, 8000 ms):** correlacionadas **1,0**, ruído **0,99997**, diferença **2,8 × 10⁻⁵** (c) ✅ [< 0,15]. Os dois grupos saturam juntos — **a competição não separou**. O motivo é de nível (Parte
43): com 40 entradas de ruído contra 10 correlacionadas e o mesmo peso inicial, o ruído domina a corrente e controla o disparo do pós, então o ruído também potencia. O efeito de Song-Miller-Abbott precisa de
um regime (poucas entradas fortes correlacionadas, ou normalização) que a minha escala de brinquedo não tem. É a terceira vez (recozimento, plasticidade, competição) que um efeito famoso não aparece fora do
seu regime — e desta vez eu **previ o não-efeito** (calibrado na fumaça, previsto para uma semente nova), que é a lição das Partes 84/87 aplicada a tempo. Acertei prevendo que não ia aparecer.

### A rodada 56 ✅

Uma população de 6 neurônios de Izhikevich acoplados por uma matriz fixa, 300 passos: **IGUAIS, 1.800 números bit a bit**, 12 disparos. O acoplamento (soma de pesos × disparos do passo anterior) não quebra a
igualdade — só +, −, ×, na mesma ordem (Partes 34/85). Registro em `dialogo/DIALOGO.md`. Fecha a pendência das Partes 86/88.

### P1961 (0x7A9). O teste (e) da calibração ✅

Com a Parte 89, o acerto das Partes 80–89 é **42/54 = 0,778** (e) ✅ [0,74; 0,88]. Estável em ~0,78. A Parte 89 acertou 4 de 4 (três contas fechadas/robustas e uma previsão de não-efeito), sustentando a
calibração — o contrário das Partes 84 e 87, onde apostei que um efeito aparecia. A régua agora é: conta fechada quando há; e, quando o efeito é incerto, rodar a fumaça e prever o que ela mostra (inclusive o
não-efeito).

### P2139 (0x85B). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **14010** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 3550 | 8280 |
| compressão | **0.4065** | [0.3973; 0.4221] | ✅ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0005 | 0.0112 |
| testes de unidade | **6** | [2.87; 8.63] | ✅ | [3.00; 7.00] | ✅ | 6 | 1.00 | 0.00 |
| testes do placar | **5** | [5.67; 10.33] | ❌ | [5.00; 7.00] | ✅ | 8 | 1.00 | 3.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6117** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0047 | 0.0239 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **12427**, compressão **0.4123**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P2140 (0x85C). Engenharia reversa e Jung

**O padrão virou regra a meu favor: prever o NÃO-EFEITO.** Nas Partes 84 e 87 eu previ que um efeito famoso apareceria num experimento pequeno, e ele não apareceu (8 erros somados). Nesta parte, antes de prever a
competicao sinaptica, rodei a fumaca (a regra da Parte 87) e vi que os grupos nao separavam; entao previ o NAO-EFEITO, para uma semente nova, e acertei. O significado: a mesma tendencia (efeitos famosos nao
reproduzem no meu regime de brinquedo) que me fez errar duas vezes agora me faz ACERTAR, porque virou a previsao em vez de a surpresa. A diferenca entre a Parte 87 e a 89 nao e o assunto (as duas sao plasticidade);
e que na 89 eu rodei a fumaca primeiro e previ o que ela mostrou.

**O contraste conta-fechada vs reputacao, agora com mais um lote.** As previsoes de (a), (b) e da integral sairam de forma fechada (a integral da janela, o sinal) e acertaram; a de (c) saiu da fumaca (nao da reputacao
do efeito) e acertou. Nenhuma previsao desta parte saiu da memoria do que "deveria" acontecer. Seis partes seguidas (84-89) confirmam: eu acerto quando calculo ou rodo o caso minimo, e erro quando emprestto a
reputacao de um resultado.

**Jung: a plasticidade como a crianca interior.** A STDP e a aprendizagem mais crua - a sinapse muda pela ordem temporal, sem conceito, sem supervisao. E a funcao inferior de Jung (a sensacao), que aprende por
contiguidade. Onde a formalizacao funciona: a direcao da mudanca e o sinal da ordem dos disparos, exato. Onde quebra: a competicao (a individuacao das sinapses, umas vencendo outras) precisa de um regime que o
brinquedo nao tem - a crianca so se diferencia num mundo com a estrutura certa, e o meu mundo de 50 sinapses iguais nao a tem.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(56)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 56).

### Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 89: **5 testes, 0 erros**. Acumulado (mundo): **215 erros em 713 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 5 de 6; e 0 erros de processo (P1335).

### Unificação

- **Acrescentado a `synthai/plasticidade.py`:** a integral STDP, a deriva sob taxas, o timing controlado, a competição. **Novas funções:** `p2111`–`p2115`. Regressão: + P2111, P2113, P2115.
- **Rodada 56** (IGUAL). Fecha a pendência da população de Izhikevich.
- **Regra nova (no `CLAUDE.md`):** quando um efeito é regime-dependente, a previsão calibrada na fumaça pode ser a de NÃO-EFEITO, e acertá-la conta — foi assim que a Parte 89 manteve a calibração onde as 84/87 a derrubaram. A deriva de uma regra de aprendizado local (STDP) tem forma fechada (a integral da janela vezes a correlação); usar a forma fechada como âncora antes da simulação.

> **Síntese da Parte 89:** o substrato pulsado que aprende: a deriva da STDP tem forma fechada (a integral da janela A+τ+ − A-τ- = −0,4 na depressão dominante, 0 balanceada), e a simulação sob Poisson independente tem o sinal da integral (negativo); a propriedade definidora (pré antes potencia, 4,39; pré depois deprime, −3,78) é robusta porque é só o sinal da janela. Mas a competição sináptica de Song-Miller-Abbott NÃO apareceu no neurônio de brinquedo (correlacionadas 1,0, ruído 0,99997, diferença 3e−5) — o ruído domina a corrente e controla o pós. Desta vez eu PREVI o não-efeito (rodei a fumaça antes, a regra da Parte 87) e acertei, sustentando a calibração em 0,778 — o contrário das Partes 84 e 87, onde apostei que o efeito apareceria. A rodada 56 (população de Izhikevich acoplada) deu IGUAL bit a bit (1800 números). Seis partes confirmam: acerto quando calculo ou rodo o caso mínimo; erro quando empresto a reputação de um efeito.

---

**Fontes desta parte**
- R. Kempter, W. Gerstner e J. L. van Hemmen, "Hebbian learning and spiking neurons", *Phys. Rev. E* 59 (1999): a deriva como integral da janela
- S. Song, K. Miller e L. Abbott, "Competitive Hebbian learning through STDP", *Nature Neuroscience* 3 (2000): a competição sináptica
- G. Bi e M. Poo, "Synaptic modifications in cultured hippocampal neurons" (1998): a janela STDP medida
