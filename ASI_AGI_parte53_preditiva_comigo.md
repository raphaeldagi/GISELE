# Como eu construiria uma AGI/ASI — Parte 53 (0x35): preditiva comigo mesma

> Continuação da [Parte 52](ASI_AGI_parte52_o_metodo_ou_a_serie.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o
> resto deste documento.** O usuário pediu: *"Tente ser preditivo consigo mesmo. Grave na memória."* A regra entrou no `CLAUDE.md`. Esta parte prevê o
> **meu próprio** comportamento mensurável (o tamanho deste texto, quantos erros eu vou ter, quanto as minhas respostas vão conter das perguntas), com um
> preditor estatístico e com as minhas próprias previsões, e pontua as duas contra o preditor ingênuo.

## As perguntas desta parte

1. **P1031 (0x407).** Qual é o meu histórico mensurável? (descritivo)
2. **P1032 (0x408).** Um preditor estatístico de mim mesma acerta a Parte 53? E eu, ajustando pelo mecanismo, acerto mais? (Rodada 27) ↩ P792
3. **P1033 (0x409).** No dicionário, o tamanho da definição prevê a profundidade da palavra na taxonomia? ↩ P793
4. **P1034 (0x40A).** Hexadecimal: prever o n-ésimo dígito hexadecimal de π sem calcular os anteriores (Bailey–Borwein–Plouffe).
5. **P1035 (0x40B).** Engenharia reversa. **P1036 (0x40C).** Jung. **P1037 (0x40D).** O diálogo.
6. **P1059 (0x423).** Placar. **P1060 (0x424).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado do placar do mundo)

Medidas deste documento quando estiver pronto (como em `p1031_historico_de_mim`). O preditor estatístico (`p1032`: média das últimas 8 partes ± 1,645 desvios)
e o ingênuo (o valor da Parte 52) já estão calculados; as **minhas** previsões ajustam o centro pelo que esta parte tem de diferente:

| medida | estatístico | ingênuo (Parte 52) | **eu** | o meu mecanismo |
|---|---|---|---|---|
| caracteres do documento | [7.437; 11.925] | 8.617 | **[8.800; 13.200]** | a seção sobre mim e a tabela acrescentam ~2.000 |
| compressão zlib | [0,431; 0,463] | 0,460 | **[0,438; 0,466]** | tabelas de números comprimem pior: centro 0,452 |
| testes de unidade escritos | [2,1; 4,2] | 4 | **[3; 5]** | p1031, p1032, p1033 e p1034 pedem um teste cada |
| testes do placar do mundo | [4,9; 14,9] | 8 | **[6; 10]** | rodada (3) + dicionário (2) + hexadecimal (2) + ~1 |
| erros no placar do mundo | [0,6; 5,1] | 2 | **[1; 4]** | taxa recente ~0,30 × ~8 testes = 2,4 |
| redundância da pergunta dada a resposta | [0,510; 0,598] | 0,551 | **[0,51; 0,61]** | falar de mim repete as perguntas: centro 0,56 |
| previsões unilaterais (P974) | — | 0 | **0** | a regra virou passo; sem faixa porque é uma contagem que deve ser zero |

Pontuação: acerto = dentro da faixa; e o erro absoluto do centro, contra o do ingênuo.

### Sobre o mundo

**P1033, definição e profundidade.** Para os substantivos com profundidade (P793), a correlação de Spearman entre o número de palavras da definição (a glosa sem
exemplos) e a profundidade.
- Exemplo à mão: *entity* (profundidade 0) tem uma definição longa e abstrata; *dog* (13) também é longa. O tamanho parece depender de outra coisa.
- (a) ρ em **[−0,05; 0,15]**

**P1034, os dígitos de π em hexadecimal.** A fórmula de Bailey–Borwein–Plouffe dá o n-ésimo dígito hexadecimal de π sem calcular os anteriores (em
ponto flutuante de 64 bits). Conferência: π exato em inteiros (fórmula de Machin) até 1.000 dígitos hexadecimais.
- Exemplo à mão: π = 3,243F6A88... em hexadecimal; o 1º dígito depois da vírgula é 2.
- (b) os 1.000 primeiros dígitos pela BBP coincidem **todos** com os exatos (1.000 de 1.000; sem faixa porque é um teste de exatidão)
- (c) o χ² das 16 frequências nos 1.000 dígitos (15 graus de liberdade) em **[7,26; 25,0]** (a faixa de 90% do χ²₁₅)
