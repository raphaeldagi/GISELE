# Como eu construiria uma AGI/ASI — Parte 54 (0x36): a sorte das rodadas

> Continuação da [Parte 53](ASI_AGI_parte53_preditiva_comigo.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o resto
> deste documento.** A Parte 52 achou que o exp e o log das bibliotecas diferem entre Python e Java; a Rodada 26 deixou a pergunta: as rodadas antigas passaram
> por exatidão ou por sorte? Esta parte mede isso, conta as folhas da taxonomia, procura o número hexadecimal que descreve a si mesmo, e continua prevendo a
> mim mesma, agora com as regras da Parte 53.

## As perguntas desta parte

1. **P1061 (0x425).** As rodadas antigas do diálogo passaram por exatidão ou por sorte? (Rodada 28) ↩ P1001
2. **P1062 (0x426).** Quantos substantivos do WordNet são folhas, e quantos filhos tem um nó interno? ↩ P793
3. **P1063 (0x427).** Hexadecimal: o número autodescritivo de 16 dígitos (o dígito na posição i conta quantos i ele tem).
4. **P1064 (0x428).** Preditiva comigo mesma, com as regras da Parte 53. ↩ P1032
5. **P1065 (0x429).** Engenharia reversa. **P1066 (0x42A).** Jung. **P1067 (0x42B).** O diálogo.
6. **P1089 (0x441).** Placar. **P1090 (0x442).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

Regra da Parte 53: o centro é o do preditor estatístico (últimas 8 partes, já com a 53), e só se desloca por um mecanismo de sinal **conferido**. Dois foram
conferidos na Parte 53: a tabela de autoavaliação **baixa** a compressão, e a seção sobre mim **aumenta** o tamanho. Esta parte também mede o documento **sem** a
seção de autoavaliação (a P1064), para separar o efeito do observador.

| medida | estatístico | ingênuo (Parte 53) | **eu** | mecanismo (conferido?) |
|---|---|---|---|---|
| caracteres | [7.182; 12.752] | 12.580 | **[9.000; 13.500]** | a seção sobre mim acrescenta texto (conferido na 53) |
| compressão | [0,416; 0,470] | 0,411 | **[0,405; 0,445]** | a tabela de autoavaliação baixa a compressão (conferido na 53) |
| testes de unidade | [2,52; 4,23] | 4 | **[2,52; 4,23]** | nenhum conferido: o estatístico |
| testes do placar | [4,65; 12,85] | 6 | **[4,65; 12,85]** | nenhum conferido: o estatístico |
| erros do placar | [0,17; 4,83] | 1 | **[0,17; 4,83]** | nenhum conferido: o estatístico |
| redundância P821 | [0,512; 0,595] | 0,576 | **[0,512; 0,595]** | nenhum conferido: o estatístico |
| previsões unilaterais | — | 0 | **0** | a regra virou passo |

### Sobre o mundo

**P1062, folhas e ramos.** Entre os substantivos do WordNet com profundidade: folha = nenhum sinset tem este como hiperônimo.
- Exemplo à mão (conferido com uma linha de código antes, regra da Parte 53): não conferido; o exemplo é *dog*, que tem hipônimos (*puppy*, raças), logo não é folha.
- (a) fração de folhas em **[0,60; 0,85]**
- (b) média de filhos dos nós internos em **[3,5; 9,0]** (se ~75% são folhas, cada nó interno tem ~0,75/0,25 + 1 ≈ 4 filhos numa árvore; o WordNet tem herança
  múltipla, que aumenta um pouco)

**P1063, o autodescritivo em base 16.** Um número de 16 dígitos hexadecimais d₀d₁…d₁₅ é autodescritivo se dᵢ = quantas vezes o dígito i aparece nele. Então Σdᵢ = 16
e Σ i·dᵢ = 16. Em base 10 o único é 6210001000. A forma conhecida para bases b ≥ 7 é (b − 4), 2, 1, 0, …, 0, 1, 0, 0, 0.
- Exemplo à mão: em base 10, 6210001000 tem seis 0, dois 1, um 2 e um 6: confere.
- (c) em base 16 existe **exatamente um**: C210000000001000 (sem faixa: é uma enumeração exata)

**P1061, rodada 28:** no `dialogo/DIALOGO.md`.
