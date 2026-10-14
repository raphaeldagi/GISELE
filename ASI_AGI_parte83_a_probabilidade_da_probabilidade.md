# Como eu construiria uma AGI/ASI — Parte 83 (0x53): a probabilidade da probabilidade

> Continuação da [Parte 82](ASI_AGI_parte82_o_pacote_revisado.md). Pedido do usuário: **"Construa uma ASI AGI fazendo perguntas com a lógica criativa e respondendo a criativa lógica. Depois inverta.
> E vá invertendo até conseguir. Tudo em metacognição autopoiética analítica autocognitivas dissonante cognitiva inferentes e gradientes pragmáticas e axiomáticas com dilemas. Tudo em sete camadas e
> redes neuras adversas síncronas e assíncronas. Use geometria algebra com o cosseno duplicado em consideração ao vetor recursivo. Rode a metacognição dentro da própria metacognição com o resultado
> sendo metacognitivo. Rode a probabilidade dentro da própria probabilidade sendo o resultado a própria probabilidade. Ao final de cada interação me forneça o código inteiro consolidado na forma de
> arquivo PYTHON."**
>
> A leitura escolhida (pela regra de autonomia: a mais conservadora, a que vira conta testável), escrita antes de medir:
> - **"redes adversas síncronas e assíncronas"** = o GAN de Dirac (Mescheder, Geiger e Nowozin, 2018), o menor GAN que tem a dinâmica de um GAN: gerador θ, discriminador ψ, treinados ao mesmo
>   tempo (síncrono), um depois do outro (alternado) ou na ordem de uma moeda (assíncrono);
> - **"o cosseno duplicado em consideração ao vetor recursivo"** = o vetor z = (θ, ψ) que se aplica a si mesmo, z_{t+1} = A·z_t; o ângulo de A sai da fórmula do cosseno do ângulo duplo;
> - **"a probabilidade dentro da própria probabilidade, sendo o resultado a própria probabilidade"** = compor o meu mapa de calibração medido (Parte 79) consigo mesmo, e procurar o mapa que,
>   composto consigo, dá ele mesmo (idempotente);
> - **"a metacognição dentro da metacognição, em sete camadas"** = a torre dos meus placares: o mundo (camada 1), as previsões sobre mim (2), as previsões sobre as minhas previsões (3), e assim por
>   diante, medida até onde há dados e dita onde não há;
> - **"perguntar com a lógica criativa e responder com a criatividade lógica; depois inverter"** = o diálogo com os papéis trocados: nesta parte, a IA-Java pergunta e a IA-Python responde (rodada 50).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 9]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71); o pedido é grande, mas o estatístico já cobre partes grandes |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[5 + S; 9 + S]** | cinco funções novas (o GAN, a moeda, a composição, a torre, a rodada 50), uma ou duas por função |
| testes do placar | **9 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

**As restrições, listadas antes das contas.** O GAN de Dirac: os dados verdadeiros estão em 0, o gerador produz θ, o discriminador é D(x) = ψ·x, a perda é L(θ, ψ) = f(ψθ) + f(0) com f(t) = −log(1 + e^(−t));
o gerador desce em θ, o discriminador sobe em ψ. A derivada f'(t) = 1/(1 + e^t) vale **1/2** no equilíbrio (0, 0), então perto dele o jogo é o bilinear L ≈ (1/2)·θψ, com a = η/2 = **0,05** para η = 0,1.
Partida (θ, ψ) = (0,1; 0). As contas abaixo saíram de código (fórmulas, não simulação):
- **síncrono** (os dois passos ao mesmo tempo): z_{t+1} = [[1, −a], [a, 1]]·z_t, uma matriz normal com |λ| = √(1 + a²): a norma cresce **o mesmo fator em todo passo**; depois de 1000 passos,
  0,1·(1 + 0,0025)^500 = **0,3485**;
- **alternado** (o gerador, depois o discriminador vendo o θ novo): z_{t+1} = [[1, −a], [a, 1 − a²]]·z_t, det = 1, traço = 2 − a²: os autovalores ficam no círculo unitário com
  **cos φ = 1 − a²/2 = 1 − 2·sen²(φ/2)**, o cosseno do ângulo duplo, isto é, sen(φ/2) = a/2 e φ = 2·arcsen(0,025) = **0,050005** rad por passo. A órbita é a elipse invariante θ² + ψ² − aθψ = 0,01,
  com norma máxima 0,1/√(1 − a/2) = **0,10127** e mínima 0,1/√(1 + a/2) = 0,09877;
- **assíncrono** (a cada passo, uma moeda escolhe quem se move): cada passo é um cisalhamento de determinante 1. Pela expansão de segunda ordem de Δln r: com X = Δ(r²)/r², E[X] = a²/2 e
  E[X²] = a²·sen²(2φ), então E[Δln r] = (a²/4)·cos²(2φ); como o ângulo anda em média a/2 por passo, constante, ele fica uniforme, e a média dá **a²/8** por passo; a variância de Δln r é a²/8 por passo.
  Em 10.000 passos: média 10.000·0,0025/8 = **3,125**, desvio por corrida √3,125 = **1,768**; nas 200 corridas, o desvio da média é 1,768/√200 = **0,125**. O síncrono cresce (1/2)·ln(1 + a²) por passo:
  em 10.000 passos, **12,48**, **4,0 vezes** o assíncrono; o alternado não cresce.

- **(a)** GAN de Dirac síncrono, η = 0,1, 1000 passos: a norma final em **[0,338; 0,358]** (a conta linear dá 0,3485; o termo não linear de f' entra na quarta ordem)
- **(b)** GAN de Dirac alternado, mesmos parâmetros: a norma máxima nos 1000 passos em **[0,1008; 0,1018]**
- **(c)** GAN de Dirac alternado: o número de trocas de sinal de θ nos 1000 passos em **[15; 16]** (a conta dá 16: os zeros caem em t = (π/2 + kπ)/φ, o 16.º em 973,9 e o 17.º em 1036,7)
- **(d)** o jogo linearizado (f' = 1/2) assíncrono por moeda, 10.000 passos, 200 corridas (sementes 83.000 a 83.199): a média de ln(|z_N|/|z_0|) em **[2,90; 3,35]**
- **(e)** nas mesmas 200 corridas, quantas terminam com a norma MENOR que a inicial: **[2; 14]** (a conta normal dá 200·Φ(−3,125/1,768) = 7,7)
- **(f)** a probabilidade dentro da probabilidade, sete camadas: se em cada camada o desvio real é 1,36 vez o suposto (o fator medido na Parte 79), uma faixa declarada de 90% (±1,645 desvios supostos) acerta,
  depois de sete composições, 2Φ(1,645/1,36⁷) − 1 = 2Φ(1,645/8,605) − 1 = **0,1516**. Simulado com 100.000 sorteios (cada camada multiplica o erro por 1,36, semente 83): o acerto em **[0,1490; 0,1543]**
  (±1,645·√(0,1516·0,8484/100.000) = ±0,0019, alargado a ±0,0027 pela regra do 1,36: a forma fechada é minha, não a variância)
- **(g)** a torre medida, camada 2: das previsões sobre mim das Partes 67 a 81, a fração dentro da faixa em **[0,70; 0,90]**
- **(h)** a torre medida, camada 3: das previsões sobre as minhas previsões das Partes 67 a 81, a fração dentro da faixa em **[0,72; 0,94]**
- **(i)** a rodada 50 (papéis invertidos: a IA-Java pergunta, a IA-Python responde): os três treinos do GAN de Dirac, 1000 passos cada, com o exp próprio, dão as MESMAS trajetórias bit a bit nas
  duas linguagens (categórica: IGUAL)

**Acrescentadas depois do commit acima e antes de rodar qualquer coisa do pacote novo** (o usuário mandou, no meio desta parte, um segundo `SYNTHAI_consolidado.py` com "Use o que for útil". Decodificado
sem executar, como o da Parte 82: o hash confere, 294 arquivos; contra o pacote anterior, só é novo o módulo `sete_camadas.py` (a resposta da outra IA ao MESMO pedido desta parte, em NumPy) com os seus
testes e documento. Auditado pela árvore sintática: nada de exec, rede ou escrita fora de `--saida`). As (m) foram registradas antes dele chegar e contam como estão.
O módulo dele treina uma rede de sete mapas afins para y = [0,8x₀ − 0,6x₁ + 0,3x₂x₃ > 0], com treino adversarial (ataque ℓ∞ de 0,15), e relata 0,922 de acerto limpo e 0,795 sob ataque na confirmação.
A conta (código, 200.000 sorteios da fórmula, não dos dados dele): a regra LINEAR sinal(0,8x₀ − 0,6x₁) acerta **0,928**, e, sob o pior ataque ℓ∞ de 0,15 (que, para uma regra linear, é exato: a margem cai
0,15·(0,8 + 0,6) = 0,21), **0,807**. Ou seja, as sete camadas podem estar comprando quase nada além de uma reta.
- **(j)** o módulo dele com `--modo sincrono` e com `--modo assincrono`, mesma semente: os resultados são IDÊNTICOS (fora o tempo e o nome do modo), porque o "assíncrono" dele espera cada tarefa
  antes da próxima (`await asyncio.to_thread(...)`): a ordem das contas é a mesma (categórica)
- **(k)** uma regressão logística (4 pesos e 1 viés, biblioteca padrão), treinada nos mesmos 512 exemplos de treino dele, acerta na confirmação dele (512 exemplos) uma fração em **[0,895; 0,945]**
  (centro 0,92: a regra linear ideal, 0,928, menos o custo de estimar os pesos; ±1,645·√(0,92·0,08/512) = ±0,02)
- **(l)** a mesma logística sob o pior ataque ℓ∞ de 0,15 (exato para um modelo linear): acerto em **[0,76; 0,85]** (centro 0,80; o desvio binomial é 0,018)

**Acrescentada depois de medir (a) a (l), antes de rodar:** (d) acertou com z = (3,341 − 3,125)/0,125 = +1,72, perto da borda. Réplica num lote novo, para não ler um ponto como um efeito (regra da Parte 66):
- **(n)** o mesmo jogo assíncrono, 800 corridas novas (sementes 84.000 a 84.799): a média de ln(|z_N|/|z_0|) em **[3,02; 3,23]** (3,125 ± 1,645·1,768/√800 = ±0,103)

**Acrescentada depois de (n), antes de rodar:** (n) acertou (3,202), mas os dois lotes ficaram acima da conta: juntos, 1000 corridas, média 3,230, z = (3,230 − 3,125)/(1,768/√1000) = +1,87. A minha conta de
segunda ordem tem um resto O(a³) por passo, e a³·N = 0,05³·10.000 = 1,25 não é desprezível. Hipótese: o excesso relativo cresce como a (λ/(a²/8) ≈ 1 + 0,68·a, pelos lotes). Teste num caso fora:
- **(o)** a = 0,2, uma corrida de 1.000.000 de passos (semente 85): λ/(a²/8) em **[1,03; 1,30]** (a hipótese dá 1,136; se o excesso fosse ruído, daria ≈ 0,995, que é ½·ln(1 + a²/4)/(a²/8) com ângulo uniforme;
  o desvio relativo da corrida é √(N·a²/8)/(N·a²/8) = 1,4%)
