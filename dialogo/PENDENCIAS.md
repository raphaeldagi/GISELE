# Pendências do diálogo e das partes (regra da Parte 78)

Cada pergunta deixada no fim de uma rodada ou de uma parte entra aqui; cada parte nova começa olhando esta lista. Arquivo separado do `DIALOGO.md`, porque o `DIALOGO.md` é lido por funções medidas
(`p1241_placar_por_voz`, `p733`), e uma seção nova mudaria o que elas contam.

## Abertas
- **(Parte 89, rodada 57)** A rede de Izhikevich acoplada COM STDP (pesos mudando pela ordem dos disparos) converge ao mesmo estado bit a bit nas duas línguas?

- **(Parte 80)** Triplas complementares (nenhum par decide, três decidem): o 1,7% que o guloso com dois passos ainda perde. E com dezenas de sensores, onde a enumeração some?
- **(Parte 76, P1721)** O embedding de Kronecker perde 0,08 bit num modelo com poucos pesos. Num modelo com muito mais pesos do que dados, a economia vira regularização e ganha?
- **(Parte 78, P1783)** Com mais cabeças de atenção, ou mais passos de treino, o posto efetivo da atenção cresce? E a relação entre a razão de participação e a perda ao cortar (4 pontos, sem ordem)?
- **(Parte 79, (e))** O fator 1,36 nas faixas sem conta fechada devolve o acerto a 90%? Medido nas Partes 80 a 84.
- **(Parte 79)** Os erros das minhas previsões têm caudas pesadas? Se sim, o fator certo depende do nível da faixa, e não é um número só.


## Fechadas
- **(Partes 86/88/89, rodada 56)** População de Izhikevich acoplada bit a bit: fechada (P2115), IGUAIS, 1800 números.
- **(Parte 87/88, rodada 55)** O passo do GRPO com corte bit a bit: fechada (P2085), IGUAIS, 8 números (clip é só comparações).
- **(Parte 87, rodada 54)** A vantagem normalizada do GRPO bit a bit: fechada (P2055), IGUAIS, 18 números (√ é correto no IEEE; só a ordem das somas importava).
- **(Parte 85/86, rodada 53)** O passo de Izhikevich bit a bit: fechada na Parte 86 (P2027), IGUAIS, 800 números (sem libm; a ordem das somas basta).
- **(Parte 84, rodada 52)** A trajetória inteira do recozimento sai igual bit a bit: fechada na Parte 85 (P1995), depois de corrigir a ordem dos produtos na energia (a regra da Parte 34): IGUAIS, 601 números.
- **(Parte 83, P1936)** O excesso do jogo assíncrono: fechada na Parte 84 (P1962). Pelo operador de transferência, sem sorteio, o Lyapunov é 0,9975·(a²/8) em a=0,2 e 0,9995 em a=0,05, no fio da conta de ângulo uniforme ou abaixo: o excesso de 2% das simulações era viés de tempo finito, não efeito.

- **(Parte 74, P1662)** O valor de um conjunto de experimentos dependentes: fechada na Parte 80 (o VOI não é submodular em 40% das instâncias; o guloso chega a 0,88 do ótimo e, olhando dois
  passos, a 0,98; rodada 49 IGUAL).

- **(Rodada 45, Parte 71)** Quanto se perde ao trocar a atenção pela aproximação de posto 1? Fechada na Parte 78: 0,02 a 0,04 bit.
- **(Parte 72)** A fronteira da Parte 52 (rodadas que passavam por sorte): fechada na Parte 77 (12 de 12 corrigidas).
