# Como eu construiria uma AGI/ASI — Parte 67 (0x43): prever o previsto

> Continuação da [Parte 66](ASI_AGI_parte66_o_endereco_da_falta.md). Pedido do usuário: **"Programe sem parar. Em loop infinito. Tem como você prever o que foi previsto?
> Tem como você prever o que foi previsto e fazer engenharia reversa em metacognição?"** Esta parte responde em três camadas, em ordem: (1) ler todas as minhas previsões
> do mundo desde a Parte 53 e fazer a engenharia reversa da regra com que eu as escrevo; (2) **prever as previsões desta parte antes de escrevê-las** (registrado primeiro,
> num commit só para isso); (3) escrever as previsões do mundo, medir, e pontuar as duas coisas: o mundo contra as minhas previsões, e as minhas previsões contra a
> previsão delas.

## A engenharia reversa do que eu já previ (dados passados, medidos antes deste registro)

`p1452_minhas_previsoes` lê, nas Partes 53 a 66, os vereditos da linha "Do mundo" e a faixa **[a; b]** de cada letra (no documento ou na rodada do diálogo da parte);
`p1453_engenharia_das_previsoes` mede:
- **97** previsões do mundo; **51** com faixa numérica legível (a leitura só pega a faixa escrita na mesma linha da letra, e a primeira, quando há duas).
- Acerto: **69,1%** no total; **64,7%** com faixa; **73,9%** sem faixa (as categóricas, como "IGUAIS em Java").
- A largura relativa w = (b − a)/(|a| + |b|): mediana **0,333**, quartis **0,20** e **0,60**.
- **Por terço de largura, o acerto cai com a largura:** as faixas estreitas (w mediano 0,15) acertam **70,6%**, as do meio (0,33) **70,6%**, as largas (0,71) **52,9%**. O
  contrário do que uma faixa "honesta" faria. O motivo, lido nas largas: elas são as que eu escrevo quando não sei nem o nível (as que cruzam o zero acertaram 2 de 5),
  e alargar não compensa não saber onde o número mora.
- **A minha largura é previsível:** prever o w de cada faixa pela mediana das outras erra em média **0,229**; o ingênuo "o w da faixa anterior" erra **0,253**.
- **15,7%** das faixas têm w a menos de 0,05 de 1/3.

## Previsões sobre as minhas previsões desta parte (registradas antes de escrever qualquer previsão do mundo desta parte)

Terceiro placar, separado do mundo e do "sobre mim":
- **(m1)** a mediana de w das faixas numéricas do mundo desta parte em **[0,20; 0,60]** (o intervalo interquartil do histórico).
- **(m2)** o número de previsões do mundo desta parte (letras na linha "Do mundo") em **[6; 11]** (o mínimo e o máximo das Partes 57 a 66 com faixa: de 5 a 11; sem a 57).
- **(m3)** a fração de acertos do mundo desta parte em **[0,44; 0,89]** (a faixa binomial de 90% em torno de 0,69 com ~9 previsões).
- **(m4)** o efeito do observador: sabendo que a mediana histórica é 1/3, eu poderia escrever faixas perto de 1/3 para acertar (m1). A regra é não fazer isso (as faixas saem
  da calibração e da conta, como sempre). Previsão: a fração das faixas desta parte com w a menos de 0,05 de 1/3 fica em **[0; 0,40]** (histórico 0,157; se eu estiver
  copiando a mediana, passa de 0,40).
- **(m5)** "prever o que foi previsto", em retrovisão: o preditor "mediana histórica, 1/3" erra o w das faixas desta parte, em média, entre **[0,05; 0,35]**.
