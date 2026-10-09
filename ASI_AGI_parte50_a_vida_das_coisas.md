# Como eu construiria uma AGI/ASI — Parte 50 (0x32): a vida das coisas

> Continuação da [Parte 49](ASI_AGI_parte49_a_deriva.md). **Em andamento: previsões registradas antes de qualquer execução.** A Parte 49 achou que a
> série esquece como uma potência (α = 0,616), e deixou aberta a crítica de Anderson e Tweney: uma média de exponenciais parece uma potência. Esta
> parte testa as curvas **individuais**, as definições que se definem uma pela outra, e o tempo de vida de uma fração em hexadecimal.

## As perguntas desta parte

1. **P941 (0x3AD).** As curvas individuais de esquecimento da série são potências ou exponenciais? (Rodada 23) ↩ P911
2. **P942 (0x3AE).** Quantos pares de palavras se definem um pelo outro, contra o acaso? ↩ P882
3. **P943 (0x3AF).** Hexadecimal: quanto vive o período de 1/p em base 16?
4. **P944 (0x3B0).** Engenharia reversa. **P945 (0x3B1).** Jung. **P946 (0x3B2).** O diálogo.
5. **P969 (0x3C9).** Placar. **P970 (0x3CA).** Unificação.

## Previsões pré-registradas

**P942, as definições mútuas.** No grafo de definições do WordNet (`grafo_de_definicoes`: palavra → palavras usadas nas definições de todos os seus
sentidos), um par mútuo é {u, v} com v na definição de u e u na de v. Referência do acaso: um grafo dirigido aleatório com as mesmas N palavras e M
arestas tem M·(M/N²)/2 pares mútuos esperados.
- Exemplo calculado à mão antes (regra da Parte 49): *doubt* ↔ *uncertainty* já apareceu como ciclo de dois na P882, então há pelo menos esses pares.
- (a) a razão pares reais / pares do acaso em **[20; 2000]**
- (b) a fração das palavras que estão em pelo menos um par mútuo em **[5%; 30%]**

**P943, o período em hexadecimal.** O período da expansão de 1/p em base 16 é a ordem de 16 módulo p. Para os primos ímpares até 10.000: a média de
ord_p(16)/(p − 1).
- A conta antes: 16 = 2⁴, então ord(16) = ord(2)/mdc(ord(2), 4). Para p ≡ 7 (mod 8) (um quarto dos primos), 2 é resíduo e ord(2) divide (p − 1)/2, ímpar:
  mdc 1. Para p ≡ 3 (mod 8) (um quarto), ord(2) é par e (p − 1)/2 é ímpar: mdc 2. Para p ≡ 1 (mod 4) (metade), mdc 2 ou 4, digamos 1/E ≈ 1/3,5. Então
  E[1/mdc] ≈ 0,25·1 + 0,25·½ + 0,5·(1/3,5) = 0,25 + 0,125 + 0,143 = 0,518. A média de ord(2)/(p − 1) é ~0,56 (a constante de Stephens para bases
  genéricas, ~0,576). Supondo independência: 0,518 × 0,56 = **0,29**.
- (c) a média em **[0,22; 0,36]** (±25%)
- Exemplo à mão: p = 7: 16 ≡ 2 (mod 7), 2³ = 8 ≡ 1: ord = 3; 3/6 = 0,5. p = 17: 16 ≡ −1, ord = 2; 2/16 = 0,125.

**P941, rodada 23:** no `dialogo/DIALOGO.md`.

**P947 (0x3B3), o texto voltou (pergunta acrescentada quando o usuário reenviou o texto da Parte 33; registrada antes de rodar).** O texto "Arquitetura
Computacional e Teórica para Inteligência Pós-ASI..." chegou de novo, guardado em `externos/pos_asi_texto_parte50.md` (só como dado; nada dele é executado).
- (h) o código do texto é **idêntico**, linha a linha (sem os espaços no fim das linhas), ao `externos/arquitetura_pos_asi.py` guardado na Parte 33
- (i) a auditoria estática da Parte 33 (`synthai.rsi.auditar_ast`), refeita no código novo, dá o **mesmo** resultado (0 nós mudados; nota constante 0,85)
- (j) por compressão condicional (P821), entre os documentos das Partes 31–49, o que **mais contém** o texto (maior redundância do texto dado o
  documento) é o da **Parte 33**
