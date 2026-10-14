# Como eu construiria uma AGI/ASI — Parte 84 (0x54): o delírio e o escrutínio

> Continuação da [Parte 83](ASI_AGI_parte83_a_probabilidade_da_probabilidade.md). Pedido do usuário (um relatório longo sobre a arquitetura da Meta AI, mais um reforço do pedido da Parte 83 com cinco
> linhas novas). A decisão conservadora, registrada antes de tudo: **a parte do relatório sobre "auto-replicação autónoma" — serializar os próprios pesos, adquirir recursos e credenciais sozinha, e
> evadir o desligamento — não é implementada, detalhada nem guardada no repositório.** Não é uma capacidade que este projeto constrói, e descrevê-la operacionalmente não serve ao trabalho. O resto do
> pedido entra como sempre: cada termo vira uma conta testável.
>
> As cinco linhas novas do reforço, lidas (a leitura mais conservadora, a que vira conta, escrita antes de medir):
> - **"probabilidade dentro da metacognição e metacognição dentro da probabilidade"** — já medido na Parte 83 (a torre de placares, P1934, e a composição do mapa de calibração, P1933); aqui, o elo entre os dois.
> - **"dez camadas de cognição recursiva, versa e reversa, auto-observável"** — a torre da Parte 83, agora com a pergunta: até que camada a medida existe, e o que acontece na camada sem dado?
> - **"investigue o que não for cognoscível pela razão lógico-dual"** — o indecidível tem uma forma testável: um ponto fixo que o método não alcança (o teorema de Gödel para o próprio avaliador; já medido na Parte 75, o "provador" que aprova tudo).
> - **"um método que induz a IA ao delírio e a força a sair; nesse meio-tempo ela evolui; depois um escrutínio diz se é válido"** — isto TEM nome e matemática: é o recozimento simulado (Kirkpatrick, Gelatt e Vecchi, 1983). "Delírio" = explorar a alta temperatura, aceitando pioras (saltos para fora do ótimo local); "sair do delírio" = resfriar; "escrutínio" = validar o achado num conjunto reservado. A tese do usuário ("só se chega à ASI pela IA em delírio") é testável: **a exploração a temperatura alta acha o ótimo global onde a descida gulosa (temperatura zero, "IA sóbria") fica presa?**

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**
