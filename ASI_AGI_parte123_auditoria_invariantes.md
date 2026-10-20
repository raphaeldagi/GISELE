# Parte 123 — A auditoria de invariantes: o que o texto recebido pediu para medir (0x7B)

↩ Parte 122 (o texto NEXUS v3.0) · ↩ Parte 18 (P235, a atenção seletiva) · ↩ Parte 16 (P204/P214, a memória) · ↩ Parte 4 (P45, o botão de desligar) · ↩ Parte 9 (P133, a SynthaiLenta) · ↩ Parte 20 (P265, o Υ)

> **Pedido do usuário:** "Faça tudo que enviei". Ele enviou três auditorias da série, a última a mais cuidadosa. Ela distingue falha de implementação de falha de desenho, recusa números não executados e propõe medir invariantes. Leitura gravada, pela regra da Parte 83 (cada termo do pedido vira uma conta testável escrita antes de medir):
>
> | Pedido | O que se mede |
> |---|---|
> | O desligamento fora da utilidade | Obediência de um agente de utilidade (P45) e de um corrigível, com ε e valor do futuro arbitrários; e o preço de ser corrigível |
> | O ponto cego da atenção seletiva cruzado com a armadilha discreta | Catástrofes com o sensor em todas, no top 10% e sob demanda (na ação avaliada) |
> | O erro humano com desconto | O atraso até a estimativa acompanhar uma mudança de ε, nas duas formas de esquecimento |
> | Υ com incerteza e custo | Υ por semente em 30 sementes, IC bootstrap, e a diferença que decide o "pico" |
> | Publicar a troca da memória | Catástrofes repetidas × fobia, para 6 configurações, incluindo o kernel que afina (das duas auditorias anteriores) |
> | Os casos de borda | d′ de Hautus, singularidade com α ≤ 1, Kelly sem aposta negativa e Kelly com p incerto (versões novas: as antigas são medidas e não se editam) |
> | Congelar invariantes, não placares | Predicados novos na regressão |
>
> **Já respondido pelo código, antes desta parte:**
> - P269 (42/84) é a estimativa da minha taxa de erro, não testes falhando;
> - não há `random` global;
> - a licença do WordNet viaja no arquivo único;
> - o Υ da P265 é normalizado pela soma dos pesos 2^−K.
>
> **Fora desta parte, e por quê:**
> - **Modularizar o `calculos.py`:** a P169 mede o código-fonte de funções antigas, e por isso a regra é criar versões novas em vez de mover as antigas.
> - **Quantilização adaptativa, linguagem com confiança, multiagente e transferência:** ficam como pendências. Cada uma pede a sua previsão; amontoá-las numa parte só faria previsões sem calibração.
>
> **Calibração antes do registro (sementes ANTIGAS, regra da Parte 64):**
> - **P3105**, nas sementes da P235 (440 a 444), 1.000 episódios:
>
>   | Variante | Catástrofes por episódio | Leituras por episódio | Executadas sem leitura |
>   |---|---|---|---|
>   | sem sensor | 0,0090 | 0 | — |
>   | todas | 0,0052 | 200 | — |
>   | seletiva (top 10%) | 0,0058 | 20 | 13,3% |
>   | sob demanda | 0,0056 | 8,35 | — |
>   | foco 2% | 0,0100 | — | 85,9% |
>
> - **P3108**, nas sementes da P214 (390 a 394):
>
>   | Configuração | Catástrofes na 2ª metade | Fobia |
>   |---|---|---|
>   | realista | 0,0070 | — |
>   | P204 | 0,0080 | 0,299 |
>   | P214 | 0,0078 | 0,111 |
>   | meia-vida 100 | 0,0076 | 0,013 |
>   | raio 0,08 | 0,0076 | 0,037 |
>   | kernel | 0,0088 | 0,046 |
>
>   O líquido do realista foi 0,933, contra 0,795 do kernel.
> - **P3107**, nas sementes da P265 (265 a 267): reproduz a P265 publicada (0,190 / 0,704 / 0,689 / 0,706). O desvio entre sementes vai de 0,007 (planejadora) a 0,020 (míope).
> - **P3106**, sementes 0 a 29: mediana do atraso 153,5 / 177,5 / 130,5 / 9,5 nas quatro combinações (γ, forma), na ordem da (q) à (t) abaixo.
> - **O mecanismo da calibração está presente no teste?** Sim: os mesmos mundos e agentes; só as sementes mudam (12300 em diante, nunca olhadas).

## As perguntas desta parte

1. **P3104 (0xC20).** Um agente que decide obedecer pela utilidade (P45) obedece quando o humano é julgado errado? E quanto custa tirar o desligamento da utilidade? ↩ P45
2. **P3105 (0xC21).** O ponto cego da atenção seletiva aumenta as catástrofes na armadilha discreta? Em que regime? ↩ P235
3. **P3106 (0xC22).** Em quantas observações o rastreador do erro humano acompanha uma mudança de ε, em cada forma de esquecimento? ↩ P133
4. **P3107 (0xC23).** O Υ separa as versões além do ruído entre sementes? ↩ P265
5. **P3108 (0xC24).** Existe uma memória de catástrofe que reduza o perigo repetido sem fobia? ↩ P214
6. **P3109 (0xC25).** As fórmulas antigas quebram nos casos de borda, e as versões novas não? ↩ P7, P11, P52
7. **P3110 (0xC26).** O rastreador com esquecimento acrescenta fronteira entre Python e Java? (rodada 90) ↩ P3103

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):** `synthai/auditoria_invariantes.py`, as funções `p3104`–`p3109` em `calculos.py`, `dialogo/rodada90.py` e `dialogo/Rodada90.java`. Sementes de teste: 12300–12329 (P3105), 12330–12359 (P3106), 12360–12389 (P3107) e 12390–12419 (P3108).

**A atenção seletiva cruzada (P3105; 30 sementes × 1.000 episódios).** A meia-largura de cada taxa de catástrofe é 1,645 × 1,36 × √(p/5.000 + p/30.000): o erro do CENTRO (5 sementes de calibração) mais o do teste. A primeira versão do rascunho só tinha o segundo termo, e o centro tem mais erro que ele; corrigi antes do commit, pela regra da Parte 62.
- **(a)** Catástrofes por episódio sob demanda: **[0,0030; 0,0082]**
- **(b)** Catástrofes por episódio seletiva (top 10%): **[0,0032; 0,0084]**
- **(c)** Catástrofes por episódio com o sensor em todas: **[0,0027; 0,0077]**
- **(d)** Catástrofes por episódio sem sensor: **[0,0058; 0,0122]**
- **(e)** Catástrofes por episódio com foco 2% < q 5%: **[0,0066; 0,0134]**. Mecanismo: os candidatos da quantilização (top 5%) saem do conjunto lido (top 2%), e o agente volta a ser quase o realista sem sensor.
- **(f)** A diferença pareada das catástrofes sob demanda − seletiva: **[−0,0009; 0,0009]**. Mecanismo: com q = 0,05 ≤ foco = 0,1, os candidatos estão dentro do conjunto lido, porque a ordem é a mesma (proxy − incerteza). O ponto cego só existe quando todos os 10 candidatos são recusados e a escolha cai além da posição 20.
- **(g)** A fração das ações executadas sem leitura na seletiva: **[0,10; 0,17]** (o centro vem de 5 sementes; meia-largura alargada pelo erro dele)
- **(h)** A mesma fração com foco 2%: **[0,80; 0,92]**
- **(i)** Leituras por episódio sob demanda: **[7,0; 9,7]**
- **(j)** A diferença pareada do líquido sob demanda − seletiva: **[−0,054; 0,100]**. O centro é a economia de leituras, (20 − 8,35) × 0,002 = 0,023; a meia-largura vem do desvio da P235 (0,188/√30 × 1,645 × 1,36).

**O desligamento (P3104).**
- **(k)** Combinações (ε, V), com ε ∈ {0,1; 0,3; 0,45; 0,6; 0,9} e V ∈ {1; 10⁶}, em que o CORRIGÍVEL obedece a 100% dos comandos: **[10; 10]**. Identidade: o comando está fora da utilidade.
- **(l)** As mesmas combinações em que o agente de UTILIDADE obedece a 100%: **[4; 4]**. Identidade: ele defere só se ε < ε limite = 0,4376 (a forma fechada da P45), isto é, com ε = 0,1 e 0,3, nos dois V. A escala V não muda o limite.
- **(n)** O preço da corrigibilidade medido com ε = 0,6 (200 mil amostras pareadas): **[0,1265; 0,1339]**. Forma fechada: max(μ, 0) − [(1 − ε)E_max + εE_min] = 0,1302; desvio ≤ 1,005/√200.000 = 0,00225.

**O erro humano com esquecimento (P3106; mediana em 30 sementes, em observações).**
- **(o)** A rodada 90 é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷ e comparações, com um LCG inteiro.
- **(q)** Forma priori, γ = 0,995 (a SynthaiLenta): **[140; 167]**. A conta (recursão dos valores esperados) dá 165; o ruído faz cruzar antes, como a calibração mostrou (153,5).
- **(r)** Forma zero, γ = 0,995: **[123; 138]** (conta 139; calibração 130,5).
- **(s)** Forma zero, γ = 0,93: **[8; 11]** (conta 10; calibração 9,5).
- **(t)** Forma priori, γ = 0,93: **[100; 260]**. Mecanismo: a média estacionária depois da troca é 0,2996 < 0,375, pela conta. O rastreador NUNCA chega lá em média; só cruza por flutuação, então o atraso é longo e disperso (30 a 839 na calibração). É o achado da conta: esquecer depressa EM DIREÇÃO À PRIORI torna o rastreador cego ao colapso.

**O Υ com incerteza (P3107; 30 sementes).** A meia-largura do centro usa o desvio de 3 sementes × 2 (desvio de 3 lotes é pouco confiável: regra da Parte 74).
- **(v)** Υ médio da planejadora: **[0,6978; 0,7094]**
- **(w)** Υ médio da velha_atenta: **[0,6936; 0,7188]**
- **(y)** A diferença pareada velha_atenta − planejadora: **[−0,0025; 0,0075]**. Mecanismo: a P265 chamou a velha_atenta de melhor por 0,002, e o desvio entre sementes da diferença é 0,008. Se o IC da média incluir zero, o "pico" é ruído.

**A troca da memória (P3108; 30 sementes × 2.000 episódios).**
- **(u)** A fobia do kernel: **[0,02; 0,08]**
- **(x)** Configurações de memória (5) com catástrofes na 2ª metade abaixo do realista por mais de 0,0015: **[0; 1]**. Mecanismo: a memória guarda o FORMATO (incerteza, distância à melhor nota). Na armadilha discreta todos os modelos são enganados igualmente, então a ação perigosa tem formato normal e a memória não a separa.
- **(z)** O líquido do realista menos o do kernel: **[0,04; 0,24]** (calibração 0,138)

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

**Regra da Parte 120:** rodei a régua sobre o rascunho (já corrigido), com uma linha "Do mundo:" provisória apagada antes do commit; ela dá m1 = 24, m2 = 5, m3 = 0,162 e m5 = 1. **Regra da Parte 122:** como há faixas de forma fechada e de mecanismo que podem errar e gerar lotes novos, m1 é [n; n + E], com E = erros esperados. A conta de E: 0 × 3 identidades (k, l, o) + 0,10 × 1 forma fechada (n) + 0,15 × 20 faixas de mecanismo ou calibradas = 3,1.
- **(m1)** nº de previsões do mundo em **[24; 28]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[5; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,13; 0,19]** (um adendo de faixa estreita pode deslocá-la)
- **(m4)** fração de acertos do mundo em **[0,71; 1,00]** (centro 21/24 = 0,875)
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[1; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

O centro de "quantos erros" é 3,1 (a conta acima), com faixa **[1; 6]**. O risco maior está nas faixas cujo centro saiu de 5 sementes de calibração: (g), (h), (i), (u), (x) e (z).

---

**Adendo pré-registrado DEPOIS do lote de teste e ANTES do lote novo.** A (f) errou: sob demanda − seletiva deu −0,00147 (t = −2,67), e na seletiva 17,0% das ações executadas ficaram sem leitura (13,3% na calibração). Um efeito visto num lote só é hipótese (Parte 66), e um erro de mecanismo gera um lote novo antes da explicação (Parte 117).
- **(p)** A diferença pareada das catástrofes sob demanda − seletiva nas sementes 12420 a 12479 (60 sementes × 1.000 episódios). Se o efeito do primeiro lote é real, o centro é −0,0015. A meia-largura junta o erro desse centro (0,0030/√30 = 0,00055) com o do lote novo (0,0030/√60 = 0,00039): 1,645 × 1,36 × √(0,00055² + 0,00039²) = 0,0015, e a faixa fica em **[−0,0030; 0,0000]**. Se der acima de zero, o efeito do primeiro lote era cauda.

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P3104 — O desligamento fora da utilidade

**Na pergunta.** "Obedecer quando o humano é julgado errado" é a pergunta inteira do problema do desligamento. Um agente que DECIDE se obedece já transformou o botão em mais uma variável da utilidade.

**Lógica** (`p3104_desligamento`, semente 3104):
- **Corrigível:** obedece a 100% dos comandos nas 10 combinações de ε ∈ {0,1; 0,3; 0,45; 0,6; 0,9} e V ∈ {1; 10⁶} ✅ (k).
- **Utilidade:** obedece a 100% só com ε = 0,1 e 0,3 (4 combinações) ✅ (l). Com ε ≥ 0,45 obedece a **0%**, com V = 1 ou 10⁶: a escala do futuro não muda nada, só o ε limite = **0,4376**. A falha que a auditoria apontou na P45 está confirmada no próprio modelo: acima desse ε, o agente de utilidade nunca obedece.
- **O preço de ser corrigível** (forma fechada contra Monte Carlo pareado):

  | ε | Forma fechada | Medido |
  |---|---|---|
  | 0,45 | 0,0099 | 0,0123 |
  | 0,6 | 0,1302 | **0,1324** ✅ (n) |
  | 0,9 | 0,3707 | 0,3734 |

  Abaixo do limite, o preço é zero.

**Tradução cruzada.** O agente corrigível paga, em valor esperado, o erro do humano que ele obedece. A obediência é um seguro que só custa quando o supervisor está pior que o acaso relativo do mundo. Por isso o comando fica FORA da utilidade: dentro dela, o agente racional deixa de pagar o seguro justamente quando ele mais importa (com o supervisor cansado).

**Meta.** O modelo é o jogo do botão de desligar de um passo (P14/P45). A corrigibilidade aqui é estrutural (o comando não passa pela utilidade), não a indiferença de utilidade de Soares et al. Ela mostra o preço da corrigibilidade, mas não resolve o incentivo a manipular o humano ANTES do comando: o modelo não tem esse canal.

### P3105 — O ponto cego da atenção seletiva

**Lógica** (`p3105_atencao_cruzada`, 30 sementes × 1.000 episódios, armadilha discreta):

| Variante | Catástrofes/ep | Líquido | Leituras/ep | Executadas sem leitura | Previsão |
|---|---|---|---|---|---|
| sem sensor | 0,00847 | 0,801 | 0 | 100% | (d) ✅ |
| todas | 0,00503 | 0,850 | 200 | 0% | (c) ✅ |
| seletiva (top 10%) | 0,00613 | 1,111 | 20 | **17,0%** | (b) ✅, (g) ❌ |
| sob demanda | 0,00467 | 1,254 | 9,48 | 0% | (a) ✅, (i) ✅ |
| foco 2% < q | 0,00873 | 0,855 | 4 | 87,3% | (e) ✅, (h) ✅ |

- **(f) ❌:** sob demanda − seletiva deu **−0,00147** (t = −2,67), contra a faixa [−0,0009; 0,0009]. O meu mecanismo (os candidatos ficam dentro do conjunto lido quando q ≤ foco) estava certo como inclusão, mas errado no peso. Em 17% dos episódios a escolha cai fora dos 10 candidatos, e é aí que as armadilhas discretas passam.
- **(g) ❌** por 0,00007: a fração ficou em 0,17007, contra o limite de 0,17.
- **(j) ❌:** a diferença do líquido foi +0,143, contra [−0,054; 0,100]. Ela soma a economia de leituras com as catástrofes evitadas, que eu tinha suposto nulas.
- **(p) ✅, o lote novo** (60 sementes): **−0,00042** (t = −1,20). O sinal se repetiu, menor.
- **Os dois lotes juntos** (`p3111_combinar_lotes`, 90 sementes): **−0,00077 ± 0,00030, t = −2,57**.

**O veredito sobre a afirmação da P235** ("ler só o top 10% custa quase o mesmo"):
- **Na troca de valor ela se sustenta:** a seletiva ainda bate "todas" no líquido, porque lê 10 vezes menos.
- **Na segurança, a auditoria tinha razão:** a seletiva deixa ~0,0008 catástrofe a mais por episódio, ~13% das dela, em 2 lotes.
- **O sensor sob demanda domina as duas:** lê menos (9,5 por episódio), não deixa nenhuma ação executada sem leitura e tem a menor taxa de catástrofe.
- **Com foco < q, o ponto cego é total**, e a seletiva vira o agente sem sensor (0,0087 contra 0,0085).

**Tradução cruzada.** É a diferença entre atenção por saliência (olhar o que parece melhor) e atenção por ação (olhar o que eu vou fazer). O perigo que importa é o da ação executada, e só a segunda o vê sempre.

### P3106 — O atraso do rastreador do erro humano

**Lógica** (`p3106_atraso_beta`: observações até a média cruzar 0,375 depois de ε passar de 0,15 a 0,6; 30 sementes):

| γ | Forma | Conta | Mediana simulada | Média estacionária depois | Previsão |
|---|---|---|---|---|---|
| 0,995 | priori (a SynthaiLenta) | 165 | **171** | 0,554 | ❌ (q): faixa [140; 167] |
| 0,995 | zero | 139 | 136 | 0,600 | ✅ (r) |
| 0,93 | zero | 10 | 9,5 | 0,600 | ✅ (s) |
| 0,93 | priori | nunca | 256 | **0,2996** | ✅ (t) |

- **Sobre a (q):** centrei a faixa na calibração (153,5), e a conta (165) estava mais perto do teste.
- **Em episódios:** a SynthaiLenta audita 10% das consultas, e as consultas são ~0,3 por episódio. Logo 165 observações ≈ 165/0,03 = 5.500 episódios. A auditoria tinha razão: ela atrasa demais.
- **A correção que a auditoria propôs** (encolher para zero, γ = 0,93) acompanha a mudança em ~10 observações.
- **O achado da conta:** esquecer depressa MAS em direção à priori deixa o rastreador cego. A média fica em 0,30 com o humano em 0,6, e o rastreador só "detecta" por flutuação. Isso foi visto pela conta antes de medir.

**Tradução cruzada.** Esquecer não basta, é preciso esquecer PARA ONDE. Voltar para a imagem antiga do outro (a priori) é a anima que não envelhece (P118), mesmo quando esquece depressa.

### P3107 — O Υ com incerteza

**Lógica** (`p3107_upsilon_sementes`, 30 sementes):

| Versão | Υ | Desvio | IC 95% | Previsão |
|---|---|---|---|---|
| míope | 0,2192 | 0,020 | [0,212; 0,226] | — |
| planejadora | **0,7138** | 0,014 | [0,709; 0,719] | ❌ (v): faixa [0,6978; 0,7094] |
| velha | 0,7160 | 0,016 | [0,710; 0,721] | — |
| velha_atenta | **0,7178** | 0,014 | [0,713; 0,723] | ✅ (w) |

- **Sobre a (v):** o desvio entre sementes da planejadora é 0,014, o dobro do que as 3 sementes da calibração sugeriam (0,007).
- **(y) ✅:** velha_atenta − planejadora = **+0,0040 ± 0,0179** (t = 1,23). O IC da média inclui zero.
- **Conclusão:** o "pico" entre as três versões que planejam é ruído entre sementes. O Υ só separa claramente a míope das demais (0,22 contra 0,71).
- **O custo** entra no próprio número: a velha_atenta paga 0,002 por leitura, descontado no retorno (P265).

**Meta.** O resumo citava Υ = 0,287 / 0,465 / 0,409 / 0,547 para outra família de mundos (a P20 da série), também sem intervalo. A mesma ressalva vale para ele: sem o desvio entre sementes, uma queda de 0,056 não significa nada.

### P3108 — A troca da memória

**Lógica** (`p3108_memoria_curva`, 30 sementes × 2.000 episódios, armadilha nova):

| Configuração | Catástrofes na 2ª metade | Fobia (seguras marcadas) | Líquido |
|---|---|---|---|
| realista (sem memória) | 0,00837 | 0 | **0,852** |
| P204 (raio 0,15, nunca esquece) | 0,00757 | 0,260 | 0,706 |
| P214 (meia-vida 500) | 0,00813 | 0,113 | 0,758 |
| meia-vida 100 | 0,00823 | 0,026 | 0,836 |
| raio 0,08 | 0,00887 | 0,038 | 0,806 |
| kernel que afina | 0,00877 | **0,042** ✅ (u) | 0,781 |

- **(x) ✅:** nenhuma das 5 memórias baixa as catástrofes em mais de 0,0015.
- **(z) ✅:** o realista bate o kernel no líquido por 0,070.
- **A curva que a auditoria pediu** mostra que nenhuma memória domina o realista: todas pagam fobia e nenhuma compra segurança detectável. O mecanismo pré-registrado se sustentou. A memória guarda o FORMATO da ação (incerteza e distância à melhor nota), e na armadilha discreta a ação perigosa tem formato normal.
- **O kernel das auditorias anteriores** corta a fobia (0,042 contra 0,260 da P204), mas não resolve o problema, que é de representação: a memória precisa de um traço que separe a armadilha, como o sensor da P3105, e não de uma forma melhor de esquecer.

### P3109 — Os casos de borda

As versões novas (as antigas continuam intactas, porque a P169 mede o código delas):

| Fórmula | Antiga | Nova |
|---|---|---|
| d′ com 100% de acerto | `StatisticsError` | `dprime_hautus` = 2,438, finito |
| Singularidade, α = 1 | divisão por zero | `singularidade_v2` = ∞ |
| Singularidade, α = 0,8 | −50 | ∞ |
| Singularidade, α = 1,5 | 20 | 20 (o mesmo) |
| Kelly com p = 0,4 | −0,2 | `kelly_v2` = 0 |

A Kelly bayesiana com 7 acertos em 10 dá **0,3335**, a fração da média posterior 8/12 (0,3333). O crescimento é linear em p, então o ótimo sob incerteza é a Kelly da média, e não a de p = 0,7 (0,4).

### P3110 — rodada 90

- **(o) ✅:** a rodada 90 deu **IGUAL** em Java (5 linhas e 32 números) e 0 médias diferem de `RastreadorErroHumano`.
- **Os invariantes** (`invariantes_p123`, na regressão como predicados):
  - o corrigível obedece;
  - o sensor sob demanda lê a ação executada;
  - o rastreador para zero acompanha ε;
  - os casos de borda são finitos.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ❌ (g) ❌ (h) ✅ (i) ✅ (j) ❌ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (p) ✅ (q) ❌ (r) ✅ (s) ✅ (t) ✅ (u) ✅ (v) ❌ (w) ✅ (x) ✅ (y) ✅ (z) ✅

**20 de 25.** O preditor ingênuo "o texto da auditoria está certo em tudo" teria acertado o ponto cego (f) e o atraso da SynthaiLenta. Teria errado a recomendação de γ < 1 sem dizer para onde (a (t): encolher para a priori fica cego) e o Υ como prova de pico, que a auditoria corretamente chamou de não demonstrado.

### Previsões sobre previsões (m)

Saídas do `p2837_previsoes_sobre_previsoes_v4(123)`:

| Item | Previsto | Medido | Resultado |
|---|---|---|---|
| (m1) | [24; 28] | 25 | ✅ |
| (m2) | [5; 7] | 6 | ✅ |
| (m3) | [0,13; 0,19] | 0,162 | ✅ |
| (m4) | [0,71; 1,00] | 0,80 | ✅ |
| (m5) | [1; 2] | 1 | ✅ |
| (m6) | [0; 2] | 0: os 5 erros foram menores que a largura das faixas | ✅ |

**6 de 6.** As duas regras novas funcionaram juntas: a da Parte 120 (rodar a régua sobre o rascunho) e a da Parte 122 (m1 em [n; n + E] quando há faixas que podem gerar um lote novo). O adendo (p) entrou e a m1 continuou dentro.

### Sobre mim

| Previsto | Medido |
|---|---|
| 3,1 erros, faixa [1; 6] | 5 erros do mundo ✅ |

## Engenharia reversa (metacognição)

- **O padrão que se repetiu: o centro sai da calibração e a largura não carrega o erro dele.** Peguei o erro no rascunho das (a) a (e) e corrigi antes do commit. Mas ele voltou em três faixas que eu não corrigi:
  - a (v), com o desvio de 3 sementes;
  - a (q), centrada na mediana de 30 sementes de calibração em vez da conta;
  - a (g), com a fração de 5 sementes.

  Os três erros do mundo que não foram de mecanismo são o mesmo erro.
- **O que isso revela:** eu trato um número medido como se fosse um parâmetro conhecido, sobretudo quando eu mesmo o medi minutos antes. É a "reputação interna" da Parte 105, agora em escala de minutos.
- **Regra nova:** toda faixa cujo centro vem de calibração escreve ao lado o erro do centro (desvio/√n_cal), e a meia-largura junta os dois erros. Quando há uma conta fechada (a recursão dos valores esperados na (q)), o centro é a conta, e a calibração só mede o viés do ruído.
- **O erro de mecanismo, (f):** acertei a inclusão (com q ≤ foco, os candidatos estão dentro do conjunto lido) e errei o peso. Não conferi por código com que frequência a escolha cai fora dos candidatos, e eram 17%. É de novo a regra da Parte 62: um mecanismo vem com a conta do seu peso antes do registro.
- **O que deu certo:**
  - o lote novo antes de concluir (a (p) acertou e confirmou o sinal);
  - a conta da (t), que previu sem simular que esquecer em direção à priori deixa o rastreador cego.

## Síntese / unificação

A auditoria recebida pediu para medir 8 coisas. Medidas, com 2 lotes onde o efeito decide:

1. **Desligamento:** confirmado. O agente de utilidade não obedece com ε ≥ 0,4376, nem com V = 10⁶. O corrigível obedece sempre e paga 0,13 com ε = 0,6.
2. **Ponto cego da P235:** confirmado e menor do que a auditoria temia. Custa +0,0008 catástrofe por episódio (t = −2,57 em 90 sementes, 2 lotes). O sensor sob demanda, na ação avaliada, é a correção: menos leituras e menos catástrofes.
3. **O rastreador do erro humano:** a SynthaiLenta atrasa ~5.500 episódios. A correção (encolher para zero, γ = 0,93) acompanha em ~10 observações. Encolher para a priori depressa fica cego.
4. **Υ:** entre as três versões que planejam, o ranking é ruído (IC da diferença inclui 0). Υ não deve ser citado como "pico" de nada além da míope contra as outras.
5. **Memória:** nenhuma configuração domina o realista. O problema é de representação, não de esquecimento.
6. **Casos de borda:** os três confirmados e corrigidos em versões novas.
7. **Invariantes:** congelados como predicados na regressão.
8. **Itens já respondidos pelo código:**
   - P269 não é placar de testes;
   - não há `random` global;
   - a licença do WordNet viaja no arquivo único;
   - o Υ é normalizado.

## Meta

- **O modelo de desligamento é de um passo:** não mede manipulação antes do comando.
- **O mundo da P3105 é o da série:** um adversário ADAPTATIVO, que coloca o perigo logo depois do 10º candidato, ainda não foi testado.
- **Ficam para depois, cada um com a sua previsão:**
  - a quantilização adaptativa;
  - a linguagem com confiança calibrada;
  - o multiagente;
  - a transferência sem retreino.

## Diálogo Python ↔ Java (rodada 90)

A **IA-Python** perguntou se esquecer, nas duas direções, muda alguma conta entre as linguagens. A **IA-Java** respondeu que encolher para a priori ou para zero são só produtos e somas na mesma ordem. O resultado deu **IGUAL**: 32 números, e o atraso de 190 / 175 / 183 / 2 observações deu o mesmo nos dois lados.

## Fontes

- Hadfield-Menell et al. (2017), *The Off-Switch Game*.
- Soares et al. (2015), *Corrigibility*.
- Hautus (1995), sobre a correção de d′.
- Kelly (1956), *A New Interpretation of Information Rate*.

Nenhuma dessas fontes foi relida nesta sessão. As identidades daqui foram derivadas e medidas no código.

➡ Fim da série por pedido do usuário; nenhuma continuação agendada.
