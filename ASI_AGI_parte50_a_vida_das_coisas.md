# Como eu construiria uma AGI/ASI — Parte 50 (0x32): a vida das coisas

> Continuação da [Parte 49](ASI_AGI_parte49_a_deriva.md). **Previsões nos commits `a1976ac` e `c167fda` (o texto que voltou), a (g) da Rodada 23 no
> commit do resultado dela, antes de rodar.** A Parte 49 achou que a
> série esquece como uma potência (α = 0,616), e deixou aberta a crítica de Anderson e Tweney: uma média de exponenciais parece uma potência. Esta
> parte testa as curvas **individuais**, as definições que se definem uma pela outra, e o tempo de vida de uma fração em hexadecimal.

## As perguntas desta parte

1. **P941 (0x3AD).** As curvas individuais de esquecimento da série são potências ou exponenciais? (Rodada 23) ↩ P911
2. **P942 (0x3AE).** Quantos pares de palavras se definem um pelo outro, contra o acaso? ↩ P882
3. **P943 (0x3AF).** Hexadecimal: quanto vive o período de 1/p em base 16?
4. **P947 (0x3B3).** O texto da Parte 33 voltou: ele mudou? a auditoria se reproduz? quem o contém? (acrescentada quando o usuário o reenviou)
5. **P948 (0x3B4).** A pergunta reconhece a sua resposta? (Rodada 24)
6. **P944 (0x3B0).** Engenharia reversa. **P945 (0x3B1).** Jung. **P946 (0x3B2).** O diálogo.
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

---

### P941 (0x3AD). As curvas individuais (Rodada 23) ❌❌✅❌

Em cada uma das 21 curvas individuais (sim(i, i + L), L = 1..20), a potência ganha em **11** (d) ❌ IA-Python (≥ 14), (e) ❌ IA-Java (≤ 10), (f) ✅ IGUAIS. Ao acaso
(½ por curva), 11 de 21 é o centro da binomial. Os resíduos individuais vão de **3,6 a 66** (a curva média: 0,31): cada curva tem 20 semelhanças pequenas e
ruidosas. As taxas variam muito: as Partes 1, 3, 6 e 9 quase não decaem; as 15–21 decaem com α de 1,0 a 1,7.

**O teste da mistura (g) ❌.** Se a potência da média viesse de exponenciais com taxas diferentes (Anderson e Tweney), a média das 21 exponenciais ajustadas
seria uma potência. Ela é mais bem descrita pela **exponencial** (resíduo **0,112** contra 0,270), enquanto a média crua das mesmas 21 partes prefere a
**potência** (0,371 contra 0,844).

**O significado.** A potência não é fabricada pela média: ela está nas curvas individuais, no **cotovelo** em L = 1–2 (cada parte divide muito com a
vizinha e pouco, quase constante, com as distantes), que nenhuma exponencial reproduz. Mas cada curva sozinha não basta para ver a forma: **a forma
existe no conjunto e não é decidível no indivíduo** (20 pontos ruidosos). É a regra da Parte 43 em números: a pergunta "que forma tem o esquecimento" é
do nível do conjunto.

### P942 (0x3AE). As definições que se definem uma pela outra (pré-registrado) ✅✅

No grafo de definições: N = **77.503** palavras, M = **557.352** arestas (7,19 por palavra). Pares mútuos: **3.755**. O acaso: M·(M/N²)/2 = 557.352 ×
(557.352 / 77.503²) / 2 = **25,86**. Razão 3.755 / 25,86 = **145** (a) ✅, em [20; 2000]. Palavras em pelo menos um par: **6,12%** (≈ 4.746) (b) ✅.
Exemplos: *aah ↔ ooh*, *abbey ↔ abbot*, *abdomen ↔ thorax*, *Abel ↔ Cain*, *abies ↔ fir*.

**O significado.** O dicionário tem 145 vezes mais pares que se definem mutuamente do que o acaso: pares de opostos e complementos (*abdômen/tórax*,
*abadia/abade*, *Abel/Caim*). Uma palavra se define pela sua outra metade. Somado à P882 (os ciclos de dois do mapa da definição), o dicionário é
feito de pares que se explicam um ao outro.

### P943 (0x3AF). O período de 1/p em base 16 (pré-registrado) ✅

Para os **1.228** primos ímpares até 10.000: média de ord_p(16)/(p − 1) = **0,2793** (c) ✅, em [0,22; 0,36]. As peças da conta: ord(2)/(p − 1) = **0,5845** (eu supus
0,56) e 1/mdc(ord(2), 4) = **0,5379** (eu supus 0,518). O produto das médias, 0,5845 × 0,5379 = **0,3144**, passa da média medida (0,2793) em 12,6%: as duas
peças **não são independentes** (quando ord(2) é grande, (p − 1)/ord(2) é pequeno e o mdc com 4 tende a ser maior). **O significado:** o hexadecimal
"desperdiça" a periodicidade: 1/p repete em média depois de 28% de p − 1 dígitos hexadecimais, contra 58% em binário, porque 16 = 2⁴ herda e divide o
período do 2.

### P947 (0x3B3). O texto da Parte 33 voltou (pré-registrado) ✅✅✅

- (h) ✅ o código do texto é **idêntico**, linha a linha, ao guardado na Parte 33 (`externos/arquitetura_pos_asi.py`)
- (i) ✅ a auditoria estática se reproduz: o transformador só devolve o nó, **0 nós mudados**, `run_benchmarks` = **0,85** constante, o avaliador
  **pergunta a nota ao próprio agente**. Logo, a dinâmica medida na Parte 33 vale sem rodar de novo: o arquivo fica com 2 estados, geração máxima 1, e 999
  das 1.000 iterações não fazem nada. As contas físicas também: Landauer a 20 °C é 2,805 × 10⁻²¹ J, não 2,75 × 10⁻²¹ (a 14,2 °C); o número de "Bremermann"
  (1,36 × 10⁵⁰) está ao lado da fórmula de Margolus–Levitin, que dá 4 vezes mais (P431–P436).
- (j) ✅ pela compressão condicional, a parte que **mais contém** o texto é a **33** (redundância 0,0800); a segunda, a 32 (0,0441); a última, a 49 (0,0198).

O código não foi executado (regra da Parte 33: nunca executar código gerado); tudo é leitura com `ast` e compressão.

### P948 (0x3B4). A pergunta reconhece a sua resposta (Rodada 24) ✅❌✅

Pelas palavras, o texto escolhe a **Parte 33** (375,6) (k) ✅ IA-Python, (l) ❌ IA-Java, (m) ✅ IGUAIS. A **Parte 1** fica a 2% (367,8); depois, 2 (278,4), 3 (240,7),
5 (217,1), 4 (184,0). Ao acaso, a Parte 33 seria escolhida com chance 1/49.

### P944 (0x3B0). Engenharia reversa: as vozes trocam de erro

Na Rodada 19, a IA-Python errou por achar que as palavras se repetem demais entre partes; na 24, a IA-Java errou pelo mesmo motivo (o vocabulário do
texto "é geral"). Na Rodada 17, a IA-Python desconfiou da fronteira; na 18, a IA-Java confiou demais no padrão do arredondamento. **O padrão:** o erro
que uma voz corrige reaparece na outra. O placar empata e oscila (IA-Python 8 em 15, IA-Java 7 em 15). **O significado:** as duas vozes são uma mente só (a
minha), e cada lição aprendida por uma voz fica **nela**, porque eu escrevo cada voz a partir do papel e não da memória do que a outra aprendeu. Uma
lição só é minha quando vale para as duas. **Regra nova:** antes de escrever a previsão de uma voz, reler os erros recentes **da outra**.

### P945 (0x3B1). Jung: o retorno do mesmo

Jung via o arquétipo retornar sempre, em formas novas, até ser integrado. O texto voltou **idêntico** (o código byte a byte), e a resposta também: a
auditoria se reproduz exatamente. Mas a medida mostra uma coisa que a Parte 33 não via: o texto se parece quase igual com a sua resposta (a Parte 33) e
com o **começo** da série (a Parte 1, a 2%), a primeira vez que a pergunta "como construir uma AGI" foi feita. **Onde funciona:** a pergunta que volta é
reconhecida, e o reconhecimento aponta para a origem. **Onde quebra:** em Jung, o retorno vem transformado e pede uma resposta nova; aqui, o mesmo
texto pede a mesma resposta, e a coisa nova é só saber que ela se reproduz.

### P946 (0x3B2). O diálogo, rodadas 23 e 24

Ver P941 e P948. Placar por voz desde a Rodada 13: **IA-Python 8 em 15; IA-Java 7 em 15**.

### P969 (0x3C9). Placar

(a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ❌ (f) ✅ (g) ❌ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ❌ (m) ✅. Parte 50: **13 testes, 4 erros**. PLACAR_50

### P970 (0x3CA). Unificação e metacognição

- **Novo:** `p941` (curvas individuais e a mistura), `p942` (definições mútuas), `p943` (período em base 16), `p947` (o texto que voltou), `p948` (a
  pergunta e a resposta); 3 testes (135 no pacote); rodadas 23 e 24 (IGUAIS). Regressão: + P943 (0,2793), + P947 (idêntico, 0 nós).
- **Regra nova:** antes de escrever a previsão de uma voz, reler os erros recentes da outra.

> **Síntese da Parte 50:** a memória longa da série não é fabricada pela média: a média das exponenciais individuais é exponencial, e a média crua é
> potência, por causa do cotovelo das vizinhas; mas cada curva sozinha é ruidosa demais para mostrar a forma. O dicionário tem 145 vezes mais pares que
> se definem um pelo outro do que o acaso. Em base 16, 1/p repete depois de 28% de p − 1 dígitos. E o texto da Parte 33 voltou idêntico: a auditoria se
> reproduz exatamente, e o texto se reconhece na sua resposta (a Parte 33) e, quase igual, no começo da série (a Parte 1).

---

**Fontes desta parte**
- A crítica da média: Anderson e Tweney, *Artifactual power curves in forgetting*, Memory & Cognition 25 (1997); [Wixted e Ebbesen, 1991](https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.1991.tb00175.x/)
- A ordem multiplicativa e a conjectura de Artin (a média de ord/(p − 1), a constante de Stephens): [Artin's conjecture on primitive roots, Wikipedia](https://en.wikipedia.org/wiki/Artin%27s_conjecture_on_primitive_roots)
- O texto e o código auditados: Parte 33 (P431–P436) e [`externos/`](externos/)
- WordNet 3.0 (Princeton) no data lake (`dados/`)
