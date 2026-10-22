# Parte 128 — Refazer tudo o que fizemos

↩ Nasce da Parte 46 (P823: "refazer tudo desde o começo: um clone limpo dá os mesmos números?") e do pedido de agora.

## O pedido, lido antes de agir
> "Repita sempre tudo que fizemos. Loop infinito. TUDO QUE FIZEMOS"

A leitura vem da regra gravada na Parte 46: "de tempos em tempos, refazer tudo desde o começo (clone limpo, todas as partes numa
execução, todos os testes e rodadas) para ver se funciona". **Repetir tudo** é refazer do zero, num clone limpo do GitHub:
- as 125 partes de `calculos.py`;
- todos os testes de unidade (as suítes do CLAUDE.md, o pacote revisado e o laboratório);
- todas as rodadas do diálogo Python ↔ Java;
- os testes das três entregas (os sete módulos, o SYNTHAI-GPT e o NEXUS-RAPHAEL 3.1.0).

Depois, confiro se o que sai é o que está publicado. **Loop infinito** quer dizer que, ao terminar uma volta, começa a seguinte. Os
pedidos de "pare" das Partes 120–123 foram substituídos por este; a continuação volta a ser agendada (send_later), e o usuário pode
parar a qualquer momento dizendo "pare".

A Parte 46 mostrou que repetir não é copiar. O que mede o MUNDO se reproduziu bit a bit (953 de 959 linhas); o que mede o PRÓPRIO
PROJETO mudou, porque o projeto cresceu (o tamanho da memória, a regressão, as falas do diálogo), e a máquina também mudou (a
velocidade). Pela regra da Parte 48, essas medidas são separadas ANTES de comparar.

## O procedimento (escrito antes de rodar)
1. Clone limpo de `https://github.com/raphaeldagi/GISELE`, ramo `claude/asi-agi-technical-questions-duan00`, no commit `245584a`, numa
   pasta vazia fora do repositório de trabalho.
2. As partes rodam em blocos retomáveis (regra da Parte 46: o contêiner reinicia e mata processos):
   - um processo por bloco, cada um no seu arquivo de saída e com marca de concluído;
   - três processos de cada vez (a máquina tem 4 núcleos);
   - cada bloco termina com a sua própria unificação e regressão.
3. Comparação com o `resultados.txt` commitado:
   - parte por parte, linha por linha, só até a unificação de cada bloco;
   - as linhas da regressão e da contagem de funções contam à parte, porque olham para o projeto.
4. Os testes rodam no clone limpo, e as rodadas do diálogo também (`python3 dialogo/verificar.py`).

## Previsões, registradas antes de qualquer execução no clone
O centro sai da Parte 46 (a única reprodução anterior): 0 exceções, regressão completa em todos os blocos, 6 de 959 linhas diferentes
(0,6%), 120 de 120 testes, 16 de 16 rodadas. As faixas de mecanismo levam o fator 1,36 (Parte 79).

| | quantidade | faixa | procedência |
|---|---|---|---|
| R1 | blocos que terminam sem exceção | todos | Parte 46: 13 de 13 |
| R2 | blocos com a regressão completa (167/167) | [14; 16] de 16 | P(um) ≈ 0,98 → P(16/16) ≈ 0,72, por isso não [16; 16] (regra da Parte 121) |
| R3 | fração de linhas de partes diferentes do `resultados.txt` (sem as unificações) | [0,5%; 6%] | Parte 46: 0,6%. Hoje há muito mais funções que medem o próprio projeto (Partes 41–127: os textos, o CLAUDE.md, o diálogo, as previsões), por isso a faixa sobe |
| R4 | das linhas diferentes, as que vêm de medidas do próprio projeto ou da máquina | [80%; 100%] | Parte 46: 6 de 6 |
| R5 | testes de unidade que falham no clone limpo | [0; 2] | Parte 46: 0 de 120 |
| R6 | rodadas do diálogo com DIFERENTES | [0; 1] de 90 | as 90 deram IGUAL na última conferência |
| R7 | testes das três entregas que falham | [0; 1] | 40 + 72 + 55 passaram nas suas partes |

**Sobre mim:**
- erros no mundo em [1; 3];
- a reprodução não vai cumprir "numa execução só": vai em blocos, como na Parte 46. É uma previsão sobre o procedimento: escolhi blocos
  de propósito, então ela acerta por construção e não conta no placar.
