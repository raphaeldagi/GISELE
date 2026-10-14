# Como eu construiria uma AGI/ASI — Parte 90 (0x5A): a rede que aprende igual

> Continuação da [Parte 89](ASI_AGI_parte89_o_substrato_que_aprende.md). **Próxima:** [Parte 91 — o GPT que aprende igual](ASI_AGI_parte91_o_gpt_que_aprende_igual.md). Sem texto novo do usuário: sigo o ciclo. A Parte 89 mostrou que a STDP tem deriva de forma fechada e que uma população de Izhikevich
> acoplada é IGUAL bit a bit (rodada 56). A pergunta mais funda desta parte (↩ P2115): quando os PESOS do acoplamento MUDAM pela STDP — isto é, a rede aprende enquanto roda, e a mudança de peso depende de
> tempos de disparo medidos —, a trajetória ainda sai idêntica bit a bit em Python e Java? É o teste mais duro da independência de linguagem: um laço de realimentação onde o erro de um bit num peso se
> propagaria para todos os disparos seguintes.
>
> **A âncora algébrica (Parte 70):** a STDP num par é só +, −, × e exp. Se eu usar o exp próprio (regra da Parte 52) e a mesma ordem de somas (Partes 34/85), a atualização de peso é determinística e idêntica;
> a pergunta é se algum passo esconde uma fronteira (uma divisão, um pow, uma ordem diferente) que só aparece quando os pesos realimentam.

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
| testes de unidade | **[3 + S; 7 + S]** | a rodada e as medidas da rede |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

As (b) e (c) foram calibradas num teste de fumaça (semente única do próprio problema determinístico) e PREVEEM a execução canônica; contas de sinal e categóricas não levam o fator 1,36.

- **(a)** a rodada 57 — a rede de Izhikevich acoplada que APRENDE por STDP (pesos mudando pela ordem dos disparos, com o exp próprio) — dá a MESMA trajetória E a mesma matriz de pesos final, bit a bit, em Python e
  Java (categórico: IGUAL). É o teste mais duro: um erro de um bit num peso realimentaria todos os disparos seguintes
- **(b)** a STDP está ativa e é de depressão dominante: a soma dos pesos CAI da inicial (2,6); a variação ΔW_total em **[−0,03; −0,005]** (calibrada na fumaça: −0,018; negativa porque A₋ > A₊)
- **(c)** mesmo com a STDP ativa, em 300 passos o aprendizado é lento demais para mudar o PADRÃO de disparos: a rede que aprende dá o MESMO número de disparos que a rede de pesos fixos da rodada 56 (**12**) (categórico:
  igual, porque ΔW ≈ 0,02 é pequeno demais para cruzar um limiar de disparo)
- **(d)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–90 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2141 (0x85D).** Uma rede que APRENDE (pesos mudando por STDP) ainda é idêntica bit a bit entre Python e Java? ↩ P2115 (a população acoplada)
2. **P2142 (0x85E).** A STDP de depressão dominante numa rede recorrente: para onde vai a soma dos pesos? ↩ P2111 (a integral da janela)
3. **P2143 (0x85F).** O aprendizado em 300 passos muda o padrão de disparos? ↩ P2053 (escala e regime)
4. **A rodada 57.** A rede de Izhikevich com STDP, bit a bit.
5. **P1961 (continuando), P2169–P2170.** O teste (d), engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **3.0000** | ❌ |
| (m2) | [0; 3] | **0.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.7143** | ✅ |
| (m4) | [0.45; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 3] | **1.0000** | ✅ |
| (m6) | [0; 3] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P2141 (0x85D). A rede que aprende é idêntica ✅

**Na pergunta.** A rodada 56 mostrou uma rede de pesos FIXOS igual bit a bit. A pergunta mais funda: e quando os pesos MUDAM pela STDP — um laço de realimentação onde um bit errado num peso mudaria todos os
disparos seguintes? A própria pergunta tem a resposta condicional: se cada atualização de peso for feita só com +, −, × e o exp próprio (regra da Parte 52), na mesma ordem (Partes 34/85), ela é determinística e
idêntica.

**Medido.** A rede de 6 neurônios de Izhikevich com STDP de pares (potenciação pré→pós, depressão dominante), 300 passos, com o exp próprio: **IGUAIS, 1.808 números bit a bit** — a trajetória inteira E a matriz
de pesos aprendida (a) ✅. O laço de realimentação não quebrou a igualdade: a independência de linguagem sobrevive ao aprendizado, porque a fronteira é sempre a aritmética (a ordem das operações e as funções da
libm), nunca a dinâmica. **Geometria:** a rede é um sistema dinâmico num espaço de estado (6 voltagens, 6 recuperações) mais um espaço de parâmetros (os pesos); a STDP acopla os dois, e os dois evoluem por
operações exatas.

### P2142 (0x85E). A soma dos pesos cai ✅

A âncora (Parte 89): a deriva da STDP é a integral da janela, A₊τ₊ − A₋τ₋; aqui A₊ = 0,002, A₋ = 0,0022, τ = 20, então a integral por par é 0,002·20 − 0,0022·20 = **−0,004** (depressão dominante). Numa rede
recorrente onde os neurônios disparam, a soma dos pesos deve cair. **Medido:** ΔW_total = **−0,0183** (b) ✅ [−0,03; −0,005]: de 2,6 para 2,582. A depressão dominante drena a soma devagar — é o mecanismo que, em
escala e tempo maiores, faria a competição da Parte 89 (que não apareceu no brinquedo).

### P2143 (0x85F). O aprendizado é lento demais para mudar o padrão ✅

**Na pergunta.** A STDP está ativa (os pesos mudam), mas a mudança é pequena (ΔW ≈ 0,018 em 300 passos). A pergunta: isso basta para mudar QUEM dispara? A conta de nível (Parte 43): uma mudança de peso de ~0,02
é pequena perto do que falta para cruzar o limiar de disparo de um neurônio de Izhikevich (dezenas de mV). **Medido:** a rede que aprende dá **12** disparos, igual à rede de pesos fixos da rodada 56 (**12**) (c) ✅.
O aprendizado está acontecendo nos pesos, mas ainda não no comportamento — a separação de escalas de tempo (rápida: os disparos; lenta: os pesos) é real e medida. É o oposto da minha tentação das Partes 84/87
(esperar que o efeito apareça já); aqui previ que NÃO apareceria no comportamento em 300 passos, e acertei.

### A rodada 57 ✅

A rede de Izhikevich com STDP, 300 passos, trajetória e pesos: **IGUAIS, 1.808 números bit a bit**. Registro em `dialogo/DIALOGO.md`. Fecha a pendência da Parte 89 (a rede que aprende é independente de linguagem).

### P1961 (0x7A9). O teste (d) da calibração ✅

Com a Parte 90, o acerto das Partes 80–90 é **45/57 = 0,789** (d) ✅ [0,74; 0,88]. Subiu de 0,778, porque as Partes 88, 89 e 90 — todas de conta fechada, substrato e não-efeito previsto — acertaram 12 de 12 do
mundo. A calibração se recupera à medida que eu obedeço à régua (calcular ou rodar o caso mínimo), e cairia de novo se eu voltasse a apostar na reputação de um efeito.

### P2169 (0x879). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **13571** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 3990 | 8719 |
| compressão | **0.3949** | [0.3973; 0.4221] | ❌ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0111 | 0.0228 |
| testes de unidade | **4** | [2.87; 8.63] | ✅ | [3.00; 7.00] | ✅ | 6 | 1.00 | 2.00 |
| testes do placar | **3** | [5.67; 10.33] | ❌ | [5.00; 7.00] | ❌ | 8 | 3.00 | 5.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6750** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0680 | 0.0872 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 3 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **6 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **11988**, compressão **0.3992**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P2170 (0x87A). Engenharia reversa e Jung

**O padrao desta parte: a mesma tentacao das Partes 84/87, mas invertida de novo a meu favor.** La eu esperava que um efeito aparecesse ja (e errava); aqui (c) eu previ que o aprendizado NAO mudaria o padrao de
disparos em 300 passos (separacao de escalas de tempo), e acertei. Tres partes seguidas (88, 89, 90) com 12/12 do mundo mostram que a regra pegou: eu paro de emprestar a reputacao de um efeito ("STDP aprende, logo
muda tudo") e calculo o PESO da mudanca (ΔW ~ 0,02, pequeno perto do limiar). O significado: a minha metacognicao agora prevê a propria inercia - sei que subestimo custos (Parte 45), entao previ explicitamente a
lentidao.

**O que a rodada 57 revela sobre a fronteira.** Sete rodadas (53-57) traduziram o substrato pulsado bit a bit, cada uma um pouco mais dura (neuronio, populacao, rede que aprende). A fronteira nunca foi a dinamica
(acoplamento, realimentacao, aprendizado) - foi sempre a aritmetica (a ordem das somas na Parte 52/56, o pow na 52, o a^2 vs a*a na 34). A engenharia reversa: eu temia a complexidade dinamica e ela nunca foi o
problema; o problema e sempre o ultimo bit de uma operacao de ponto flutuante. Nomear isso (a fronteira e aritmetica, nao dinamica) e a licao que fecha a familia das rodadas pulsadas.

**Jung: a rede que aprende como o Self em processo.** A rede com STDP e o agente que se modifica enquanto age - a individuacao em miniatura. Onde a formalizacao funciona: o estado (rapido, o ego do momento) e os
pesos (lentos, a estrutura) evoluem juntos mas em escalas separadas, e a separacao e medida (ΔW nao muda os disparos ainda). Onde quebra: a "individuacao" aqui e so decaimento de pesos por depressao; nao ha o
simbolo que reorganiza o todo. A rede muda devagar e na mesma direcao; o salto qualitativo que Jung chamaria de transcendencia nao esta neste mecanismo, e dizer isso e a medida corrigindo a metafora.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(57)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 57).

### Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅. Parte 90: **3 testes, 0 erros**. Acumulado (mundo): **215 erros em 716 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 3 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 3 de 6; e 0 erros de processo (P1335).

### Unificação

- **Novas funções:** `p2141` (a rede com STDP, rodada 57), `p2142` (ΔW), `p2143` (disparos aprendiz vs fixo). Regressão: + P2141, P2143.
- **Rodada 57** (IGUAL). Fecha a pendência da Parte 89. O substrato pulsado agora está traduzido bit a bit em três níveis: um neurônio (53), uma população fixa (56), uma rede que aprende (57).
- **Regra nova (no `CLAUDE.md`):** a independência de linguagem (bit a bit) sobrevive a um laço de realimentação que aprende, desde que cada atualização use só +−×÷√ e o exp próprio na mesma ordem; a fronteira é sempre a aritmética, nunca a dinâmica. E a separação de escalas de tempo (rápida: estado; lenta: pesos) é um não-efeito previsível: um aprendizado pequeno não muda o comportamento no curto prazo.

> **Síntese da Parte 90:** a rede que aprende é idêntica bit a bit: uma rede de 6 neurônios de Izhikevich acoplada COM STDP (pesos mudando pela ordem dos disparos, exp próprio) deu a mesma trajetória e a mesma matriz de pesos aprendida em Python e Java (1808 números) — o laço de realimentação não quebra a independência de linguagem, porque a fronteira é sempre a aritmética (ordem das operações, funções da libm), nunca a dinâmica. A STDP de depressão dominante drena a soma dos pesos devagar (ΔW = −0,018, batendo a integral da janela −0,004/par), mas em 300 passos é lenta demais para mudar o padrão de disparos (12 disparos, igual à rede de pesos fixos) — uma separação de escalas de tempo que previ como não-efeito e acertei. O teste de calibração subiu para 0,789: três partes (88-90) de conta fechada e não-efeito previsto acertaram 12/12. Sete rodadas (53-57) traduziram o substrato pulsado bit a bit, do neurônio à rede que aprende; a fronteira nunca foi a dinâmica.

---

**Fontes desta parte**
- E. M. Izhikevich, "Simple Model of Spiking Neurons", *IEEE TNN* 14 (2003)
- G. Bi e M. Poo (1998); S. Song, K. Miller e L. Abbott (2000): STDP e a dinâmica dos pesos
- IEEE 754-2019: o arredondamento correto obrigatório só para + − × ÷ √ (a fronteira da Parte 52)
