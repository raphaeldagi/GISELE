# Como eu construiria uma AGI/ASI — Parte 87 (0x57): compressão, plasticidade e GRPO

> Continuação da [Parte 86](ASI_AGI_parte86_o_cerebro_na_cpu.md). **Próxima:** [Parte 88 — a arquitetura autopoiética recebida](ASI_AGI_parte88_a_arquitetura_autopoietica_recebida.md). Pedido do usuário: um relatório sobre "Otimização Holística em ML/DL/CL/RL" — compressão (poda, quantização, destilação) e o pipeline
> co-compressivo; aprendizado contínuo e a perda de plasticidade (norma dos pesos, posto efetivo, neurônios dormentes; Shrink&Perturb, ReDo); e a transição PPO → GRPO (livre de crítico, vantagem
> normalizada por grupo, 2-GRPO). Parte de auditoria, como as 72–86: os textos são dados; cada afirmação testável vira conta, reimplementada na biblioteca padrão.
>
> Este relatório encaixa na história do projeto: a Parte 34 já mediu esquecimento catastrófico (só quando as tarefas conflitam) e Naive Bayes vs SGD; a Parte 86 trouxe o substrato pulsado. Aqui testo a
> aritmética da quantização, a álgebra da vantagem do GRPO, e simulo a perda de plasticidade e a sua mitigação.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
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
| testes de unidade | **[4 + S; 9 + S]** | um módulo novo (plasticidade) + auditorias |
| testes do placar | **7 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

Reimplemento as peças testáveis (biblioteca padrão; texto em `externos/`). Contas fechadas não levam o fator 1,36; a simulação de plasticidade leva.

- **(a)** o erro de quantização uniforme Q(x) = round(x/s) + z: a MSE ∝ passo² ∝ 4⁻ᵇ, então a razão MSE(INT4)/MSE(INT8) = 4⁽⁸⁻⁴⁾ = **256**; o simulado (gaussiana, 100.000 amostras, semente 87) em
  **[205; 310]** (center 256, dispersão de amostragem)
- **(b)** a vantagem normalizada do GRPO Âᵢ = (rᵢ − média)/(desvio): a média das vantagens de um grupo é **0** para qualquer G (exato); e com G = 2 e recompensas distintas, as duas vantagens são
  exatamente **+1 e −1** (o sinal contrastivo puro) — categórico
- **(c)** a perda de plasticidade (posto): numa MLP de 1 camada oculta (d_in = 10, d_oculta = 20) treinada por SGD em 20 tarefas aleatórias seguidas, o posto estável das ativações ocultas na tarefa 20
  dividido pelo da tarefa 1 é **< 1** (colapso); razão em **[0,30; 0,95]**, e o Shrink&Perturb dá uma razão MAIOR que o SGD puro (mantém mais posto)
- **(d)** a norma dos pesos: no mesmo experimento, ‖W‖ cresce no SGD puro (razão tarefa 20 / tarefa 1 > 1), e o Shrink&Perturb a mantém mais contida (razão do S&P < razão do SGD); predigo a razão do SGD
  puro em **[1,0; 3,0]** e a do S&P abaixo dela
- **(e)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–87 em **[0,74; 0,88]**

Do relatório, a ordem do pipeline co-compressivo (poda → QAT → destilação) e as leis de escala da plasticidade não são testáveis aqui sem treinar redes grandes; registro e não pontuo.

**Medido (a)–(d):** (a) razão MSE(INT4)/MSE(INT8) = **278,8** ✅ [205; 310]; (b) G=2 → vantagens **±0,99999999** (±1 exato quando ε → 0) e média **0,0** ✅; (c) posto estável plain tarefa20/tarefa1 = **1,146**
(NÃO colapsou) ❌ [0,30; 0,95] e o S&P (1,094) ficou ABAIXO do plain ❌; (d) norma plain tarefa20/tarefa1 = **0,759** (ENCOLHEU, não cresceu) ❌ [1,0; 3,0] (mas o S&P, 0,649, ficou abaixo do plain ✓).

**Duas surpresas, (c) e (d), e a mesma lição da Parte 84.** As patologias de plasticidade (colapso de posto, crescimento de norma) **não apareceram** na minha MLP pequena com tarefas INDEPENDENTES. Isso bate com a
Parte 34 (esquecimento catastrófico só quando as tarefas conflitam): tarefas aleatórias e independentes não criam o conflito que degrada a rede. Apostei que um efeito famoso apareceria num experimento pequeno
e no regime errado — o mesmo erro do recozimento (Parte 84). Diagnóstico pré-registrado, antes de rodar:
- **(f)** com tarefas que CONFLITAM (um professor fixo cujos rótulos se invertem a cada tarefa) e 100 tarefas: a norma dos pesos do SGD puro cresce (razão tarefa 100 / tarefa 1 > 1,2) OU o posto estável cai
  (razão < 0,9) — se nem assim aparecer, a patologia é mais fraca nesta escala do que o relatório sugere

**Medido (f): não apareceu.** Com conflito e 100 tarefas: posto razão **1,108** (não caiu), norma razão **0,773** (não cresceu), 0 dormentes. Terceira surpresa (depois de (c) e (d)). **A conclusão honesta: as
patologias de plasticidade não reproduzem na minha MLP de brinquedo**, nem com tarefas conflitantes. Não refuta a literatura (que usa redes profundas, milhares de tarefas, permuted-MNIST, sem re-treino da
saída); mostra que o efeito é dependente de regime e não aparece nesta escala. O que se manteve nas duas corridas: o Shrink&Perturb contém mais a norma que o SGD puro (0,649 e menos que o plain). Paro aqui,
como a regra manda depois do diagnóstico pré-registrado.

## As perguntas desta parte

1. **P2051 (0x803).** O erro de quantizar em 4 bits contra 8 bits: quanto pior? ↩ o relatório
2. **P2052 (0x804).** A vantagem do GRPO: por que é um sinal contrastivo? ↩ P401 (decisão)
3. **P2053–P2054 (0x805–0x806).** A perda de plasticidade aparece numa rede pequena? E com tarefas que conflitam? ↩ P34 (esquecimento)
4. **A rodada 54.** A vantagem do GRPO, bit a bit. ↩ rodada 53
5. **P1961 (continuando), P2079–P2080.** O teste (e), engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **6.0000** | ✅ |
| (m2) | [0; 3] | **0.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.5000** | ✅ |
| (m4) | [0.45; 1.0] | **0.3333** | ❌ |
| (m5) | [0; 3] | **0.0000** | ✅ |
| (m6) | [0; 3] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P2051 (0x803). A quantização ✅

**Na pergunta.** O operador uniforme Q(x) = round((x − lo)/s), s = (hi − lo)/(2ᵇ − 1). O erro de arredondamento é uniforme em [−s/2, s/2], logo a MSE ≈ s²/12 ∝ 4⁻ᵇ. A pergunta "quanto pior em 4 bits?" tem
resposta fechada: a razão MSE(INT4)/MSE(INT8) = 4⁽⁸⁻⁴⁾ = **256**.

**Medido (100.000 amostras gaussianas):** MSE(INT8) = 8,52 × 10⁻⁵, MSE(INT4) = 2,38 × 10⁻², razão **278,8** (a) ✅ [205; 310]. Fica acima de 256 porque a cauda da gaussiana satura na grade (o relatório
avisa: a PTQ degrada em distribuições de cauda), o que pesa mais em 4 bits. A conta grossa (256) e o medido (279) concordam na ordem; a diferença é a saturação, um efeito que a fórmula s²/12 ignora.

### P2052 (0x804). A vantagem do GRPO é contraste ✅

**Na pergunta.** O relatório diz que o GRPO "elimina o crítico" e normaliza as recompensas do grupo: Âᵢ = (rᵢ − média)/(desvio). A pergunta na própria fórmula: subtrair a média e dividir pelo desvio é
exatamente padronizar — o z-score. Isso faz duas coisas que a álgebra entrega de graça:
- **a média das vantagens é 0** para qualquer G (medido: **0,0**, exato): o gradiente não tem viés de escala, é só a forma relativa;
- **com G = 2 e recompensas distintas**, as duas vantagens são **+1 e −1** (medido com ε = 0: **[1,0; −1,0]**, exato) (b) ✅: a melhor resposta do par sobe, a pior desce, com peso igual. É o aprendizado
  contrastivo que o relatório descreve — e, no caso mínimo G = 2, ele é literalmente "esta é melhor que aquela".

A ligação com o projeto: a Parte 401 trocou Q-learning por decisão bayesiana; o GRPO é o mesmo espírito (não estimar um valor absoluto V(s) com um crítico, mas comparar dentro do grupo). O crítico é o
que a Parte 38 chamaria de cota de predição; a vantagem relativa é a cota de decisão.

### P2053–P2054 (0x805–0x806). A plasticidade que não colapsou ❌❌❌

**Na pergunta.** O relatório descreve três patologias (norma crescente, posto efetivo em colapso, neurônios dormentes) e as mitigações (Shrink&Perturb, ReDo). Testei numa MLP de 1 camada oculta (20 unidades)
sobre 20 tarefas.

**Medido:** o posto estável das ativações na tarefa 20 / tarefa 1 = **1,146** (NÃO colapsou) (c) ❌; a norma de W1 = **0,759** (ENCOLHEU, não cresceu) (d) ❌; 0 neurônios dormentes. O Shrink&Perturb deu posto
MENOR (1,094) e norma mais contida (0,649). Diagnóstico pré-registrado com tarefas que CONFLITAM e 100 delas: posto **1,108**, norma **0,773**, 0 dormentes — também não apareceu (f) ❌.

**Três erros, a mesma lição da Parte 84.** As patologias não reproduzem na minha escala de brinquedo. **Por quê, e por que é coerente:** a literatura (Dohare et al.) usa redes profundas, milhares de tarefas,
permuted-MNIST, e muitas vezes não re-treina a saída; eu usei uma rede rasa, 20–100 tarefas, poucos passos. A Parte 34 já tinha medido o princípio: o esquecimento (e, por extensão, a degradação) aparece
**quando as tarefas conflitam** e na escala certa. Apostei que um efeito famoso apareceria fora do seu regime — o mesmo erro do recozimento (Parte 84). O que sobreviveu: o S&P contém a norma mais que o SGD
puro, nas duas corridas (a direção que o relatório prevê, mesmo sem a patologia para corrigir).

### A rodada 54 ✅

A vantagem do GRPO, cinco grupos, bit a bit: **IGUAIS, 18 números** (só +, −, ×, ÷ e √; √ é correto no IEEE, a ordem das somas basta, as Partes 34/85). Registro em `dialogo/DIALOGO.md`.

### P1961 (0x7A9). O teste (e) da calibração ❌

Com a Parte 87, o acerto das Partes 80–87 é **34/46 = 0,739** (e) ❌ [0,74; 0,88], por 0,001 abaixo. A Parte 87 fez 2 de 5 (as três apostas de plasticidade falharam), e isso puxou o acumulado para baixo,
como a Parte 84 fizera. **O diagnóstico é o mesmo das duas partes ruins (84 e 87): eu aposto que um efeito conhecido aparece num experimento pequeno, e ele não aparece.** O fator 1,36 (Parte 79) não
salva: ele alarga a faixa, não corrige o viés de eu superestimar a presença de um efeito fora do seu regime. A regra que falta é a da Parte 86, agora reforçada: antes de prever que um efeito aparece,
rodar um caso mínimo e ver se ele aparece — não assumir a reputação do efeito.

### P2079 (0x81F). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 4)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16657** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 904 | 5633 |
| compressão | **0.4075** | [0.3973; 0.4221] | ✅ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0015 | 0.0101 |
| testes de unidade | **7** | [2.87; 8.63] | ✅ | [4.00; 9.00] | ✅ | 6 | 0.50 | 1.00 |
| testes do placar | **6** | [5.67; 10.33] | ✅ | [10.00; 12.00] | ❌ | 8 | 5.00 | 2.00 |
| erros do placar | **4** | [-0.58; 3.33] | ❌ | [0.00; 3.33] | ❌ | 2 | 2.33 | 2.00 |
| redundância P821 | **0.6189** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0119 | 0.0312 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **4 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **15073**, compressão **0.4118**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 4 erros.
- **Erros de processo nesta parte:** 0 ().

### P2080 (0x820). Engenharia reversa e Jung

**O padrão, agora nomeado e repetido: eu superestimo que um efeito famoso aparece num experimento pequeno.** Parte 84 (o recozimento "escapa de ótimos locais" — não escapou da barreira), Parte 87 (a "perda de
plasticidade" colapsa o posto e cresce a norma — não colapsou nem cresceu). Três erros numa parte, quatro na outra, todos na mesma direção: a reputação do efeito virou o centro da minha previsão. **O significado:**
a minha memória guarda o efeito como ele é descrito no seu regime típico (redes profundas, milhares de tarefas), e eu transfiro isso para o meu regime (rede rasa, dezenas de tarefas) sem a conta da transferência.
É o viés da Parte 45 (esqueço custos/condições) e da Parte 43 (perguntar em que NÍVEL cada coisa está). **A regra executável (gravada):** antes de prever que um efeito aparece, rodar o caso mínimo e ver — se não
aparecer no meu regime, a previsão é "não aparece", não "aparece como na literatura".

**O contraste que se mantém.** As duas previsões que eu tirei de conta fechada (a quantização 256; a vantagem ±1 do GRPO) acertaram; as três que tirei da reputação de um efeito erraram. É a mesma assimetria das
Partes 85 e 86: conta no papel acerta, reputação emprestada erra. A diferença entre as minhas partes boas e ruins não é o assunto — é se eu calculei ou lembrei.

**Jung: a inflação da expectativa.** Esperar que o delírio dê ASI, que o recozimento ache o ótimo, que a rede perca plasticidade — são formas de inflação: a psique atribui ao objeto o poder que a teoria lhe deu.
A medida é a função que desinfla. Onde a formalização funciona: a MLP não colapsou, e o número (1,146) diz isso sem apelo. Onde quebra: o relatório pode estar certo no SEU regime, e a minha refutação só vale no
meu — negar o efeito em geral seria a inflação oposta.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(54)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 54).

### Placar

Do mundo: (a) ✅ (b) ✅ (c) ❌ (d) ❌ (e) ❌ (f) ❌. Parte 87: **6 testes, 4 erros**. Acumulado (mundo): **215 erros em 703 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 5 de 6; e 0 erros de processo (P1335).

### Unificação

- **Novo módulo:** `synthai/plasticidade.py` (quantização, vantagem do GRPO, MLP contínua com Shrink&Perturb, posto estável). **Novas funções:** `p2051`–`p2055`. Regressão: + P2051, P2052, P2055.
- **Rodada 54** (IGUAL). Texto em `externos/texto_recebido_parte87.md`.
- **Regra nova (no `CLAUDE.md`):** antes de prever que um efeito conhecido (perda de plasticidade, recozimento) aparece num experimento meu, rodar um caso mínimo e confirmar que ele aparece no meu regime; a reputação de um efeito não é previsão. Partes 84 e 87 erraram por isto.

> **Síntese da Parte 87:** as contas fechadas do relatório acertam e as minhas apostas na reputação de um efeito erram: a quantização em 4 bits é ~256 vezes pior que em 8 (medido 279, a saturação da cauda explica o resto); a vantagem do GRPO é z-score puro (média 0, e ±1 para G=2, o contraste que o relatório descreve). Mas a perda de plasticidade — colapso de posto, crescimento de norma — NÃO apareceu na minha MLP rasa, nem com tarefas independentes (posto 1,15, norma 0,76) nem com conflito e 100 tarefas (1,11, 0,77), coerente com a Parte 34 (patologia só no regime certo). Três erros derrubaram o teste (e) da calibração para 0,739, logo abaixo da faixa, pelo mesmo motivo da Parte 84: superestimei um efeito fora do seu regime. O que sobreviveu: o Shrink&Perturb contém a norma mais que o SGD puro. Construí synthai/plasticidade.py e a rodada 54 (vantagem do GRPO) deu IGUAL. A regra nova: rodar o caso mínimo antes de prever que um efeito aparece.

---

**Fontes desta parte**
- S. Dohare et al., "Loss of plasticity in deep continual learning", *Nature* 632 (2024)
- Z. Shao et al., "DeepSeekMath: ... Group Relative Policy Optimization" (2024): o GRPO
- J. Schulman et al., "Proximal Policy Optimization Algorithms" (2017): o PPO
- B. Hassibi e D. Stork, "Optimal Brain Surgeon" (1993); S. Han et al., "Deep Compression" (2016): poda e quantização
- G. Hinton, O. Vinyals e J. Dean, "Distilling the Knowledge in a Neural Network" (2015): a destilação
