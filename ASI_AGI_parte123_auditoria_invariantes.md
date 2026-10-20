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

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
