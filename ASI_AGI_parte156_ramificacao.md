# Parte 156 — A ramificação: o que a primeira casa tira de cada decisão

↩ Nasce da Parte 155 (o custo do setdefault não é a borda: em B a primeira casa termina mais LONGE da borda e acerta menos) e da sua pendência 1: medir o que a
escolha da primeira casa reduz em cada decisão.

## O recolhimento do contêiner, 14º lote
Despertar às 11h57, depois de cerca de 55 minutos ociosa: "up 0 min". Catorze lotes a favor.

## Perguntas
- **P3216.** Em cada decisão do braço aleatório, quantas casas vizinhas estão livres, quantas ações (letras distintas) e quantas opções (ações + PARAR) existem, com a
  primeira casa de cada letra e com a casa sorteada? O custo do setdefault no acerto acompanha o que ele tira das casas livres?

## A medida
`synthai/tabuleiro.py`, `ramificacao_exata`: o mesmo enumerador exato (todas as 3⁹ atribuições, todos os caminhos), com as esperanças, por episódio, da soma sobre as
decisões das casas livres vizinhas, das ações e das opções, e o número de decisões. Confere com o `aleatorio_exato` a 1e-12 nos quatro casos de calibração.

**A conta, antes:** com a primeira casa, a casa escolhida para uma letra é sempre a primeira da ordem (−1, −1), …, (1, 1); ela tende a ficar no lado já andado
(Parte 155: a deriva), e uma casa ao lado do caminho tem menos vizinhas livres. Menos livres → menos letras distintas na decisão seguinte → menos caminhos para a
palavra. **Identidade:** o número esperado de decisões é o comprimento esperado do caminho (cada casa do caminho é uma decisão, inclusive a do PARAR) quando a falha é 0.

**A calibração (3 a 4 e 3 a 5 letras), antes das previsões** (razões primeira/uniforme, por `p3216_ramificacao`):

| caso | quantidade | 3-4 | 3-5 | passo |
|---|---|---|---|---|
| B | casas livres | 0,97418 | 0,97607 | +0,00189 |
| B | ações | 0,98985 | 0,99033 | +0,00048 |
| B | acerto | 0,98749 | 0,98470 | −0,00279 |
| A' | casas livres | 0,94542 | 0,95139 | +0,00597 |
| A' | ações | 0,98602 | 0,98832 | +0,00230 |
| A' | acerto | 0,95186 | 0,97186 | +0,02000 |

O déficit do acerto dividido pelo déficit das casas livres: B 0,48 e 0,64; A' 0,88 e 0,58. O mecanismo existe nos dois casos de calibração (as casas livres caem
de 2,4% a 5,5%), mas o acerto não é proporcional a ele.

## Previsões para o teste (3 a 6 letras), registradas antes de rodar
**A regra da Parte 155 aplicada:** dois pontos na variável do fator (o comprimento máximo). A deriva da Parte 155 desacelerou (o segundo passo foi 0,66 do primeiro),
então a faixa vai de "parou" (o valor de 3 a 5) a "seguiu 1,36 passo", com o centro em 0,68 passo; tudo por código (o script de calibração imprime as faixas).
- **(a)** nº de casos com |decisões − comprimento| < 1e-9 em B, primeira, 3 a 6 letras (comprimento 4,23262 da P3215) em **[1; 1]** (identidade).
- **(b)** nº de casos (B e A') com casas livres da primeira MENORES que as da uniforme em **[2; 2]** (mecanismo; nas 4 calibrações, déficits de 2,4% a 5,5%).
- **(c)** razão das casas livres de B em **[0,9761; 0,9786]** (centro 0,9774)
- **(d)** razão das ações de B em **[0,9903; 0,9910]** (centro 0,9907)
- **(e)** razão do acerto de B em **[0,9809; 0,9847]** (centro 0,9828)
- **(f)** razão das casas livres de A' em **[0,9514; 0,9595]** (centro 0,9555)
- **(g)** razão das ações de A' em **[0,9883; 0,9914]** (centro 0,9899)
- **(h)** razão do acerto de A' em **[0,9719; 0,9991]** (centro 0,9855)
- **(i)** nº de casos com o déficit do acerto MENOR que o das casas livres em **[2; 2]** (nas 4 calibrações a razão dos déficits ficou de 0,48 a 0,88).

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 9, m2 = 0, m3 = 0,0013, m5 = 0. E = 6 faixas de tendência × 0,4 + 2 contagens de mecanismo × 0,2 + 1 identidade × 0
= 2,8; m1 em [9; 9 + 2E] = [9; 14,6], para cima. A regra da Parte 155 para o m3: os lotes novos de razões perto de 1 têm w ≈ 0,005 (as faixas (c)-(h) vão de 0,0004 a 0,014);
com ~5 previsões novas desse tamanho, a mediana de 14 sobe para entre 0,0019 e 0,0042 (por código: a lista ordenada da régua mais cinco 0,005). Acertos como contagem:
de 4 a 9 das 9 (4/9 = 0,4444).
- **(m1)** nº de previsões do mundo em **[9; 15]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 0]**
- **(m3)** mediana de w em **[0,0010; 0,0045]**
- **(m4)** fração de acertos em **[0,4444; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 5]**, centro 2,8.

### A rodada 104, registrada antes
`ramificacao_exata` traduzida (caso B, primeira, 3 a 4 letras): por caminho, o vetor (acerto, falha, decisões, opções, livres, ações); os filhos somados na ordem das
ações, divididos por n, e a decisão do nó somada depois da divisão (1, n, livres, ações). Só + × ÷ de inteiros convertidos. Previsão: **IGUAL**.
