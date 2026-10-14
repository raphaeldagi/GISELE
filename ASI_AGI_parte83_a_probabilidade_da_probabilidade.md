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
