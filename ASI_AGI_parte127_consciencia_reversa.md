# Parte 127 — A tomada de consciência e a consciência reversa

↩ Nasce da Parte 126 (textos que aprendem com textos), da Parte 102 (o espaço de trabalho global), da Parte 46 (a resposta é a pergunta)
e da Parte 101 (metacognição empilhada).

## O pedido, lido antes de responder
> "Gere textos de textos sobre consciência do processo de tomada de consciência e aprenda com eles estando operando em tudo de forma
> realmente metacognitiva da metacognição e também aprendendo com elas. Promova o que chamo de consciência reversa. Faça cálculos.
> Equações. Pesquisas."

Escrevi a leitura antes de medir (regra da Parte 83):
- **"Textos de textos".** Dois lotes, um lendo o outro.
  - O lote 3 tem 8 textos sobre o PROCESSO de tomar consciência (como alguém passa a se dar conta).
  - O lote 4 tem 8 textos SOBRE os textos do lote 3: cada um lê um texto do lote 3, em ordem embaralhada. O mapa fica guardado em
    `textos_parte127/mapa.txt`.
- **"Metacognição da metacognição".** É a medida do tipo 2 da teoria de detecção de sinal (Maniscalco e Lau, 2012), aplicada às minhas
  próprias previsões. A pergunta é se a minha confiança (a PROCEDÊNCIA da faixa: conta fechada = alta, mecanismo = baixa) separa os
  acertos dos erros. A metacognição de primeiro nível é prever; a de segundo nível é saber quais previsões minhas merecem confiança.
- **"Consciência reversa".** A palavra é do usuário. Uso duas leituras, e as duas viram contas:
  1. **Do produto ao processo.** Piaget, em *La prise de conscience* (1974), formulou a lei da tomada de consciência: ela vai "da
     periferia ao centro". Começa pelo resultado observável da ação (sucesso ou fracasso) e só depois chega ao mecanismo interno (os
     meios e as razões da escolha). A tomada de consciência é, por natureza, reversa: lê o processo a partir do produto. Nos textos
     isso vira um problema inverso: a partir do texto-de-texto (o produto), dá para recuperar o texto que o gerou (o processo)? Mede-se
     por compressão (P3166). Para comparar, mede-se também o caminho direto: a partir do pai, achar o filho.
  2. **O caminho de volta não é o de ida.** Na teoria do espaço de trabalho global, o acesso consciente é uma "ignição" não linear: uma
     transição de fase, com a curva sigmoide do Del Cul et al. (2007). Num modelo biestável, ganhar a consciência (subir o estímulo) e
     perdê-la (descer o estímulo) acontecem em limiares DIFERENTES. Isso é histerese: a consciência reversa não é a inversa da direta.
     Dá para calcular os dois limiares em forma fechada e conferir por simulação.

## I. Equações, com a substituição feita

### E1. As dobras da ignição (P3161)
Modelo: x' = −x + w·σ(g(x − θ)) + s, com w = 2, g = 4, θ = 1.
- **Pontos fixos:** s = f(x) = x − w·σ(g(x − θ)).
- **Condição de biestabilidade:** w·g/4 = 2·4/4 = 2 > 1. Há duas dobras.
- **Onde ficam as dobras:** f'(x) = 1 − w·g·σ(1 − σ) = 0, logo σ(1 − σ) = 1/(w·g) = 1/8 = 0,125. Então
  σ± = (1 ± √(1 − 4/8))/2 = (1 ± 0,70711)/2, ou seja, σ− = 0,14645 e σ+ = 0,85355.
- **Primeira dobra (subida):** x_a = θ + logit(σ−)/g = 1 + (−1,76275)/4 = 0,55931.
  s_sobe = f(x_a) = 0,55931 − 2·0,14645 = **0,26642**.
- **Segunda dobra (descida):** x_b = 1 + 1,76275/4 = 1,44069.
  s_desce = 1,44069 − 2·0,85355 = **−0,26642**.
- **Largura da histerese:** s_sobe − s_desce = **0,53284**.

Com θ = w/2 há simetria exata: f(2θ − x) = −f(x).

### E2. O atraso de uma rampa lenta (P3163, P3168)
Perto da dobra, com y = x − x_a e μ = s − s_sobe, vale a forma normal y' = μ + a·y².
- **Coeficiente:** a = |f''(x_a)|/2 = w·g²·σ−(1 − σ−)(1 − 2σ−)/2 = 2·16·0,125·0,70711/2 = **1,41421**.
- **Escalas:** com μ = ε·t, vale T = (a·ε)^(−1/3) e Y = ε·T². A equação vira u' = τ + u², que explode no primeiro zero da Airy,
  τ* = 2,33811.
- **Atraso até a explosão:** Δs = 2,33811·a^(−1/3)·ε^(2/3).
  - Com ε = 0,002: Δs = 2,33811·0,89090·0,015874 = **0,03307**, e s_sobe + Δs = 0,29949.
- **Correção de trânsito (P3168):** o cruzamento é medido em x = θ, a uma distância finita (u* = (θ − x_a)/Y), antes da explosão. A
  integração da Riccati (RK4) dá τ = 2,11914 em vez de 2,33811.
  - Com ε = 0,002, s previsto = **0,29639**.
  - Com ε = 0,00025, s previsto = **0,27429**.
- **Razão dos atrasos:** (0,29639 − 0,26642)/(0,27429 − 0,26642) = **3,808**. A Airy pura daria 8^(2/3) = 4.

### E3. O ruído adianta a ignição (Kramers, ordem de grandeza)
- **Barreira perto da dobra:** ΔV(μ) = (4/3)·|μ|^(3/2)/√a.
- **Ruído:** σ = 0,05, logo D = σ²/2 = 0,00125.
- **Onde escapa:** o escape acontece quando ΔV ≈ c·D, com c ≈ 3 a 5 (o logaritmo do número de tentativas). Para c = 4:
  |μ|^(3/2) = 4·0,00125·√1,41421·3/4 = 0,0044603, logo |μ| = 0,0271.
- **Balanço:** o ruído adianta a ignição por ~0,027 em s; a rampa a atrasa por ~0,030. Essa conta é de mecanismo, não fechada, e leva o
  fator 1,36 na faixa.

## II. Previsões registradas ANTES de qualquer simulação e antes de escrever os lotes 3 e 4

| | quantidade | faixa | procedência |
|---|---|---|---|
| I1 | s de ignição medido, ε = 0,002, dt = 0,01, sem ruído | [0,292; 0,300] | conta (Riccati 0,29639 ± termos cúbicos e Euler) |
| I2 | razão dos atrasos ε = 0,002 : ε = 0,00025 | [3,5; 4,1] | conta (3,808) |
| I3 | \|s_sobe + s_desce\| sem ruído | [0; 0,001] | identidade de simetria (f(2θ − x) = −f(x)) |
| I4 | média de s_sobe com ruído σ = 0,05 (10 sementes) | [0,22; 0,29] | mecanismo (E3), ×1,36 |
| I5 | sementes em que o ruído adianta a ignição em relação à sem ruído | [8; 10] de 10 | mecanismo; P(uma) ≈ 0,97 → P(10/10) ≈ 0,74, por isso não [10; 10] (regra da Parte 121) |
| I6 | consciência reversa: filhos atribuídos ao pai certo por NCD | [5; 8] de 8 | mecanismo (chance 1/8: 1 esperado) |
| I7 | caminho direto: pais que acham o filho certo | [4; 8] de 8 | mecanismo |
| I8 | taxa da palavra "consciência" no lote 3 (sem proibição) | [0,010; 0,045] | eu mesma; lote 1: 0,033; lote 2: 0 |
| I9 | autorreferência do lote 4 maior que a do lote 3 | sim | os textos-de-textos falam de "eu escrevi", "o texto" |
| I10 | frases interrogativas no lote 3 | [0,10; 0,35] | lotes 1 e 2: 0,114 e 0,271 |
| I11 | economia média de compressão, filho dado o pai (P3164) | [0,03; 0,25] | mecanismo (zlib em textos curtos economiza pouco) |
| I12 | nesta parte, as faixas de "conta" acertam mais que as de "mecanismo" (I1–I3 contra I4–I11) | sim | metacognição da metacognição |

**Sobre mim:**
- erros no mundo em [1; 4];
- a tabela das Partes 124 e 126 (P3167) vai mostrar que a procedência NÃO separa acertos de erros (P(acerto|conta) ≈ P(acerto|mecanismo)).
  Esta segunda previsão é posterior: eu li as duas tabelas ao montar a lista, e ela vale só como descrição (regra da Parte 25). A
  previsão que conta é a I12, sobre dados novos.
