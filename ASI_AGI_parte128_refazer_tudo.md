# Parte 128 — Refazer tudo o que fizemos

↩ Nasce da Parte 46 (P823: "refazer tudo desde o começo: um clone limpo dá os mesmos números?") e do pedido de agora.

## O pedido, lido antes de agir
> "Repita sempre tudo que fizemos. Loop infinito. TUDO QUE FIZEMOS"

A leitura vem da regra gravada na Parte 46: "de tempos em tempos, refazer tudo desde o começo (clone limpo, todas as partes numa
execução, todos os testes e rodadas) para ver se funciona". **Repetir tudo** é refazer do zero, num clone limpo do GitHub:
- as 124 partes de `calculos.py` (contadas por código no dicionário PARTES: 1–81, 83–123, 126 e 127; a primeira versão deste texto dizia 125, de cabeça);
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

## Volta 1, medida (P3172, P3173; as saídas ficam em `reproducao/volta1/`)
O clone limpo foi feito às 14h04 (UTC) e o último bloco terminou às 16h36: **2 h 32 min** de relógio e **7,1 h** de processador nos 16 blocos
(25.594 s, somando a linha FIM_OK de cada bloco). O bloco 25–32 levou 1 h 54 min sozinho; na Parte 46, esse mesmo trecho foi o que estourou
o limite de 2 horas.

| | medido | faixa | |
|---|---|---|---|
| R1 | 16 de 16 blocos sem exceção | todos | ✅ |
| R2 | 16 de 16 blocos com a regressão **167/167** | [14; 16] | ✅ |
| R3 | **85** de 1.872 linhas diferentes = **4,54%** | [0,5%; 6%] | ✅ |
| R4 | projeto **73** + máquina **2** = 75 de 85 = **88%**; as outras 10 são notas escritas à mão; **0 do mundo** | [80%; 100%] | ✅ |
| R5 | **0** falhas: 717 testes da suíte + 27 do laboratório | [0; 2] | ✅ |
| R6 | **0** DIFERENTES: as 90 rodadas IGUAIS bit a bit | [0; 1] | ✅ |
| R7 | **0** falhas: 40 (módulos) + 72 (SYNTHAI-GPT) + 55 (NEXUS 3.1.0) | [0; 1] | ✅ |

**Mundo: 7 de 7.** **Sobre mim: 0 de 1.** Previ de 1 a 3 erros e tive 0. É a terceira vez que isso acontece (Partes 116, 117, agora). Seis
das sete faixas eram identidades ou calibrações fortes; pela regra da Parte 117, o centro deveria ter sido 0,10 × as faixas de forma
fechada + a taxa histórica × as de mecanismo, perto de 0,5, e a faixa [0; 2]. **Eu continuo centrando "quantos erros" na média antiga
quando a parte é de identidades.** A regra existe e eu não a apliquei: isso pede um passo verificável (a Parte 49), não uma regra a mais.

### O que se reproduziu e o que não
- **Tudo o que mede o mundo se reproduziu bit a bit:** as 1.872 linhas de 124 partes, menos as que olham para o projeto ou para a máquina.
  Na Parte 46 foram 953 de 959 linhas; agora, 1.787 de 1.872.
- **As 73 linhas do PROJETO** são a série vista crescendo:
  - o CLAUDE.md passou de 15.272 a 87.537 caracteres (P143);
  - a regressão passou de 89/89 a 167/167 (P213);
  - as falas da IA-Python no diálogo passaram de 41 a 172 (P674);
  - as funções do `calculos.py`, de 591 a 949 (P1692);
  - as rodadas conferidas, de 35 a 90 (P1271).
  Cada uma dessas linhas é uma fotografia do projeto no dia em que a parte foi escrita, e a reprodução tira a fotografia de hoje. A regra
  da Parte 48 (separar antes as medidas que olham para o próprio projeto) foi o que permitiu dizer "0 do mundo" sem olhar linha a linha.
- **As 2 da MÁQUINA:** o laço Python fez 2,06·10⁷ adições por segundo; na época, 2,76·10⁷ (P433). A conta AIXI que depende disso andou junto
  (P434).

### Três achados que nenhuma previsão pedia
1. **A Parte 91 nunca esteve no `resultados.txt`.** A reprodução a rodou (8 linhas, as do GPT que aprende bit a bit), e o arquivo commitado
   pulava da 90 para a 92. A auditoria do repositório (P1601) diz "partes fora do resultados: 0" e não a acusou. O motivo eu NÃO sei:
   a primeira versão deste texto dava um ("olhava os números, não as linhas"), escrito sem conferir, e eu o tirei pela regra da
   Parte 127 (nenhum número surpreendente ganha mecanismo antes de conferir a régua). Ficou como pendência.
2. **28 rótulos mentem.** Nas Partes 85 a 119, a linha da calibração diz "Partes 80-X" e imprime o total da faixa padrão CRESCENTE: hoje
   todas dizem 317/350, a calibração das Partes 80 a 123. Na época em que cada parte rodou, o número era o certo para aquela data; hoje o
   rótulo e o número não falam da mesma coisa. A Parte 109 percebeu isso numa função (P2446) e criou a regra "toda função 'das Partes A-B'
   passa A-B explícito", mas só para a frente. A volta 1 mostrou o tamanho do que ficou para trás (P3173: 28 de 39 linhas).
3. **O `resultados.txt` tinha 10 linhas escritas à mão**, nas Partes 92 a 101 ("Regressão: confirmada verde pela suíte de testes de
   unidade…"). Elas não saem de nenhum código e sumiram na reprodução. Um arquivo de resultados que mistura saída de código com notas
   minhas não pode ser conferido por código.

### O que mudou no repositório
- **O `resultados.txt` agora é a saída da volta 1:** os 16 blocos em ordem, sem notas. A Parte 91 entrou, e as linhas do projeto mostram o
  projeto de hoje. O arquivo anterior está guardado em `reproducao/resultados_antes_volta1.txt` (e no histórico do git), porque a P3172 o
  usa como referência. Foi o mesmo procedimento da Parte 46.
- **Em `reproducao/`:** os scripts da volta (`rodar_tudo.sh`, `rodar_bloco.sh`, `rodar_testes.sh`, `comparar.py`, `blocos.txt`) e as 22
  saídas da volta 1. A volta 2 vai comparar com a volta 1.

## Engenharia reversa
- **O padrão desta parte é o de toda reprodução:** o que eu calculo sobre o mundo é estável, e o que eu digo sobre mim muda. A SYNTHAI
  refeita do zero é a mesma; o que ela diz sobre si é uma fotografia datada.
- **O significado dos 28 rótulos é mais incômodo:** uma frase minha pode ter sido verdadeira quando a escrevi e ficar falsa sem que uma
  letra mude, porque o número que ela cita é uma função do tempo. A cura não é corrigir as frases antigas (são registros), é escrever as
  novas com o argumento explícito, para que o número não possa andar.
- **Regra nova (Parte 128):**
  - um arquivo de resultados só contém saída de código;
  - todo rótulo de faixa ("Partes A-B") é gerado da mesma variável que a função recebe, nunca escrito separado dela;
  - antes de prever "quantos erros", contar por código quantas faixas da parte são identidades, de forma fechada ou de mecanismo, e
    aplicar a regra da Parte 117 a essa contagem.

## Funções e testes
- **Funções:** `p3171_partes_de_saida`, `p3172_comparar_reproducao`, `p3173_rotulo_que_mente` e `_parte_128`. A entrada `P3172` foi para a
  regressão, que agora tem 168 entradas.
- **Testes:** `synthai/testes_parte128.py`, com 4 testes. O teste da comparação tem as quatro categorias diferentes de zero (regra da
  Parte 30).
- **Diálogo:** nesta parte, a rodada foi conferir as 90 rodadas existentes, todas IGUAIS no clone limpo. Não houve tradução nova.

## Loop
A volta 2 começa num clone novo, no commit desta parte, e compara com a volta 1. Uma continuação está agendada (send_later). Para parar,
basta dizer "pare".

Fonte da regra de reprodutibilidade (citada na Parte 46, não relida nesta sessão): Sandve et al., *Ten Simple Rules for Reproducible
Computational Research*, PLoS Comput. Biol. 9(10): e1003285, 2013.

➡ Anterior: [Parte 127](ASI_AGI_parte127_consciencia_reversa.md).
