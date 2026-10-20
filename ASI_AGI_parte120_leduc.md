# Parte 120 — O pôquer Leduc: CFR, acaso e amostragem externa num jogo 48 vezes maior (0x78)

↩ Parte 119 (a amostragem externa no Kuhn) · ↩ Parte 118 (o acaso amostrado) · ↩ Parte 113 (o CFR vanilla) · → Parte 121 (o NEXUS 2.2.0, feita antes desta)

> **Continuação autônoma, retomada depois do "Pare" e do "CONTINUE" do usuário.** A Parte 119 deixou uma regra e uma pendência.
> - **A regra:** comparar métodos com o MESMO custo, com a unidade escrita.
> - **A pendência:** sortear o adversário só compensa com muitas ações, isto é, em escala.
>
> O Leduc (Southey et al., 2005) é o próximo degrau. Tem 6 cartas e uma carta pública, e são 288 conjuntos de informação contra os 12 do Kuhn. A Parte 121 foi feita antes desta, com a rodada 87, então esta usa a rodada 88.
>
> **Antes do registro (conferências, não previsões).**
> - **As regras:** foram conferidas à mão em `synthai/testes_parte120.py`, no commit fe6af21. São 144 + 144 conjuntos.
> - **A calibração** (regras das Partes 62 a 64), na unidade de custo NÓS (chamadas da recursão):
>   - **Nós por iteração:** vanilla 10.200, acaso 85, externo ~36,96.
>   - **Sementes de calibração:** 1201 e 1203.
>   - **Explorabilidade:**
>
>     | Nós | Vanilla | Acaso (1201 / 1203) | Externo (1201 / 1203) |
>     |---|---|---|---|
>     | 200 mil | 0,3669 | 0,5376 / 0,5050 | 0,3645 / 0,4844 |
>     | 2 milhões | 0,0724 | 0,1108 / 0,1114 | 0,0877 / 0,0955 |
>
>   - **Razão por década:** vanilla 5,07; acaso 4,85 e 4,53; externo 4,16 e 5,07.
>   - **Valor do jogo para o jogador 1, pelo vanilla:**
>     - −0,14785 em 20 iterações;
>     - −0,08578 em 196 iterações, com melhor resposta de cada lado em [−0,11586; −0,04348].
> - **O mecanismo da calibração está presente no teste?** Sim: o mesmo jogo, os mesmos amostradores e a mesma variável (nós). As sementes do teste são 1202 e 1204, nunca olhadas.
> - **Fumaça antes do registro, declarada:** rodei uma vez o lado Python da rodada 88 (`dialogo/rodada88.py`) e vi as primeiras e as últimas linhas da estratégia em hexadecimal. Não rodei o Java, a comparação nem nenhum experimento de 20 milhões de nós. As previsões (h) e (i) são identidades e não dependem desses números.

## As perguntas desta parte

1. **P3041 (0xBE1).** Em 20 milhões de nós, quanto cede a estratégia média de cada método (vanilla, acaso e externo)? ↩ P3012
2. **P3042 (0xBE2).** Com o MESMO custo, a amostragem externa ganha do acaso no Leduc, onde há até 3 ações? E o vanilla ganha dos dois? ↩ P3012
3. **P3043 (0xBE3).** O CFR vanilla no Leduc (cadeias, frações de pote e 288 conjuntos) acrescenta fronteira entre Python e Java? (rodada 88) ↩ P3013

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):** `synthai/leduc.py` (fe6af21), `dialogo/rodada88.py` e `dialogo/Rodada88.java`.
- **O teste:** 20.000.000 de nós por método, que dão:
  - vanilla: 1.961 iterações;
  - acaso: 235.294 árvores;
  - externo: 541.126 iterações (cada uma com uma travessia por jogador).
- **Sementes dos amostradores:** 1202 e 1204; a faixa vale para a média das duas.

**A convergência (P3041).**
- **(a)** A explorabilidade do vanilla em 20 milhões de nós.
  - **Centro:** 0,0724/5,07 = 0,0143.
  - **Mecanismo da faixa:** uma razão por década entre √10 (convergência a 1/√T) e 10 (a 1/T).
  - **Faixa:** **[0,0072; 0,0229]**. Abaixo dela, o vanilla converge mais rápido que 1/T; acima, mais devagar que 1/√T.
- **(b)** A explorabilidade média do acaso (sementes 1202 e 1204).
  - **Centro:** 0,1111/4,69 = 0,0237.
  - **Mecanismo da faixa:** o ruído de amostragem empurra a razão para √10; o transiente da calibração a deixa até 6,5.
  - **Faixa:** **[0,0171; 0,0352]**.
- **(c)** A explorabilidade média do externo (sementes 1202 e 1204).
  - **Centro:** 0,0916/4,6 = 0,0199.
  - **Mecanismo da faixa:** o mesmo da (b).
  - **Faixa:** **[0,0141; 0,0290]**.

**O mesmo custo (P3042).**
- **(d)** A razão externo/acaso das médias.
  - **Histórico:** 0,814 em 200 mil nós e 0,824 em 2 milhões; centro 0,82.
  - **Faixa:** o ruído das sementes (±0,18): **[0,65; 1,00]**.
  - **Mecanismo:** sortear o adversário deixa mais iterações pelo mesmo custo. Acima de 1, o Leduc não teria ações bastantes para que isso compense.
- **(e)** A razão vanilla/externo.
  - **Histórico:** 0,86 em 200 mil nós e 0,79 em 2 milhões; centro 0,72.
  - **Mecanismo:** o vanilla não tem ruído, então a vantagem dele cresce enquanto os amostradores ficam presos no piso do ruído.
  - **Faixa:** **[0,45; 0,95]**.

**O valor do jogo.**
- **(f)** O valor da estratégia média do vanilla para o jogador 1.
  - **Centro:** −0,0858. A Parte 71 proíbe extrapolar uma tendência de 2 pontos sem t, então não extrapolo.
  - **Mecanismo da faixa:** |v(σ) − v*| ≤ explorabilidade(σ). A meia-largura é 1,36 × 0,0143.
  - **Faixa:** **[−0,1052; −0,0664]**.
  - O valor publicado (−0,0856) não foi lido nesta sessão e não entra como identidade.
- **(g)** Quantas das 2 pontas do intervalo [melhor resposta do jogador 2, melhor resposta do jogador 1] em 20 milhões de nós caem dentro do intervalo de 2 milhões, [−0,11586; −0,04348].
  - **Faixa:** **[2; 2]**.
  - **Regra da Parte 121:** P(uma ponta) ≈ 0,97, porque o intervalo encolhe com a explorabilidade, de 0,072 para ~0,014. Então p² = 0,94 ≥ 0,90.

**O diálogo (P3043).**
- **(h)** A rodada 88 é **IGUAL** bit a bit entre Python e Java: **[0; 0]**.
  - **Identidade:** só inteiros (as contribuições), +, −, × e ÷ na mesma ordem dos dois lados, e chaves ASCII em ordem lexicográfica: o `sorted` do Python e o `TreeMap` do Java comparam pelo código do caractere.
- **(i)** A estratégia média da `rodada88.py` comparada com a de `synthai.leduc`, com T = 3: conjuntos que diferem em algum bit, **[0; 0]**.
  - **Identidade:** a mesma ordem das 120 distribuições (`POSTOS[a]` = a // 2), a mesma `estrategia` e as mesmas somas.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **9**.
- **(m1)** nº de previsões do mundo em **[8; 10]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,50; 0,80]**
- **(m4)** fração de acertos do mundo em **[0,67; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[3; 5]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 1]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros" é:
0 × 2 identidades + 0,10 × 0 faixas de forma fechada + 0,2 × 7 faixas de mecanismo = **1,4**, com faixa **[0; 3]**.

O risco maior é a (e). A razão vanilla/externo veio de 2 pontos, com a tendência escrita no mecanismo; é exatamente o que a regra da Parte 71 manda tratar com cuidado.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
