# Pendências do diálogo e das partes (regra da Parte 78)

Cada pergunta deixada no fim de uma rodada ou de uma parte entra aqui; cada parte nova começa olhando esta lista. Arquivo separado do `DIALOGO.md`, porque o `DIALOGO.md` é lido por funções medidas
(`p1241_placar_por_voz`, `p733`), e uma seção nova mudaria o que elas contam.

## Abertas
- **(Parte 98, rodada 66)** A temperatura e o top-k na amostragem: dividir os logits por T (so divisao) e zerar os k menores (so comparacao/ordenacao) - a fronteira continua sendo so o exp? Conferir bit a bit. Fechada a rodada 65: a geracao autorregressiva (amostragem por CDF com u dado de fora) e IGUAL, o acaso e insumo externo, o exp e a unica fronteira.
- **(Parte 98, P2383)** Ruido de TESTE: medir o residuo contra um teste RUIDOSO (nao limpo) - o piso vira sqrt(sigma^2 + estimacao^2) ~ sigma para n grande (o irredutivel do proprio teste). E ruido heterocedastico (dependente do estado): muda a conta da variancia.
- **(Parte 97, P2355/e)** Ruido de OBSERVACAO: o limiar "n > #params -> exato" supoe mundo determinista; com ruido sigma, mesmo n>#params deixa residuo ~sigma e a cumeeira volta a valer. Medir o veredito sob ruido.
- **(Parte 97, P2353)** O teto da capacidade do MLP num mundo cubico: residuo vs h alem de 16, e o piso de vies do tanh.
- **(Parte 96, P2324)** A cura da variancia: ridge/early-stopping no ajuste de base rica (grau 5, n pequeno) - medir quanto o regularizador recupera o teste, e o lambda otimo vs. n.
- **(Parte 96, P2323)** O MLP a 0,053 com h=8: mapear residuo vs. (h, passos) - quanto h e preciso para chegar a, digamos, 0,01 num mundo cubico, e isso cresce como?
- **(Parte 95, P2292)** A vantagem do TTTS e regime-dependente (folga entre bracos, orcamento T): mapear onde o TTTS vence e onde empata/perde o Thompson, por uma grade de (folga, T), antes de adota-lo como padrao.
- **(Parte 94, P2264)** O LQR supoe acoes que nao saturam na trajetoria otima; num mundo onde o alvo exige acao alem de [-1,1], o LQR irrestrito deixa de ser otimo e o MPC (que respeita o limite) pode alcanca-lo. Medir.
- **(Parte 94, P2263)** Aprender a BASE de um mundo nao-linear (em vez de recebe-la): o degrau entre o brinquedo e um modelo de mundo de verdade. Features aprendidas (uma camada escondida) vs. base dada.
- **(Parte 93, P2235)** O controle otimo em forma fechada (LQR / equacao de Riccati) deste mundo linear-quadratico: quanto o MPC com tiro aleatorio (K=512) ainda perde para o otimo? Calcular o ganho otimo e comparar.
- **(Parte 93, P2233)** Mundo NAO-linear: com dinamica nao-linear, aprender o modelo volta a ser estatistica (vies do encoder linear), nao algebra. Medir o erro do modelo e a vantagem do MPC quando o mundo deixa de ser linear.
- **(Parte 93, regra da (c))** Magnitude de efeito condicional so com >=2 condicoes cobrindo a variavel que o move (regra da Parte 65 aplicada ao tamanho, nao so a existencia de um efeito).

- **(Parte 80)** Triplas complementares (nenhum par decide, três decidem): o 1,7% que o guloso com dois passos ainda perde. E com dezenas de sensores, onde a enumeração some?
- **(Parte 76, P1721)** O embedding de Kronecker perde 0,08 bit num modelo com poucos pesos. Num modelo com muito mais pesos do que dados, a economia vira regularização e ganha?
- **(Parte 78, P1783)** Com mais cabeças de atenção, ou mais passos de treino, o posto efetivo da atenção cresce? E a relação entre a razão de participação e a perda ao cortar (4 pontos, sem ordem)?
- **(Parte 79, (e))** O fator 1,36 nas faixas sem conta fechada devolve o acerto a 90%? Medido nas Partes 80 a 84.
- **(Parte 79)** Os erros das minhas previsões têm caudas pesadas? Se sim, o fator certo depende do nível da faixa, e não é um número só.


## Fechadas
- **(Parte 91/92, rodada 59)** O passo de Adam bit a bit: fechada (P2203), IGUAIS, 25 numeros (pow inteiro por multiplicacao repetida; a pow da libm diverge em 418/500).
- **(Parte 90/91, rodada 58)** O passo de treino de GPT (gradiente softmax+CE, SGD, decisao) bit a bit: fechada (P2171), IGUAIS, 30 numeros (exp/log proprios).
- **(Parte 89/90, rodada 57)** A rede de Izhikevich que aprende por STDP bit a bit: fechada (P2141), IGUAIS, 1808 números (trajetória + pesos; a fronteira é aritmética, não dinâmica).
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
