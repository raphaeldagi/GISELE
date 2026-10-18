# Parte 116 — O NEXUS-RAPHAEL "v2": dez camadas no nome, o que o código faz de fato (0x74)

↩ Parte 109 (o NEXUS v0.1.0 colado, synthai/nexus.py) · ↩ Parte 111 (o verificador lê capacidades, não nomes) · ↩ Parte 75 (um verificador só vale com um caso de controle de cada lado) · ↩ Parte 88 (comparar o texto com o SEU PRÓPRIO código)

> **Recebido sem pedido escrito:** um texto colado que abre com "Vou implementar o NEXUS–RAPHAEL como uma arquitetura experimental consolidada em Python, … real, mensurável e auditável". Segue um código de "10 camadas" (ingestão, linguística, numérica, geométrica, inferência, criatividade, …, metacognição, auditoria e memória). Ele vem **truncado em dois pontos**: no meio de `divergent_exploration` ("Vou continuar o código a partir de onde parou:") e no fim de `evaluate_and_decide`.
>
> **A leitura escolhida (regras das Partes 83, 109 e 111, escrita ANTES de medir).** O pedido implícito é o do próprio texto: implementar o que ele descreve, de forma "mensurável e auditável". Faço como na Parte 109:
> - O texto fica **arquivado** intacto em `externos/nexus_raphael/nexus_raphael_v2_colado.txt` (`.txt`: não fecha como Python e não é importável).
> - É auditado pela **árvore sintática**, sem executar.
> - O que serve vira `synthai/nexus_v2.py`, escrito do zero, offline e só com a biblioteca padrão.
>   - O **dicionário** sai da API `dictionaryapi.dev`, que é rede (12ª recusa da família), e passa a ser o WordNet local.
>   - A **memória SQLite** sai do disco e vai para `':memory:'`.
> - Cada afirmação de mecanismo do texto é medida contra o **próprio código dele** (Parte 88): as funções puras são transcritas como `recebido_*` e medidas ao lado da versão corrigida.
>
> **Antes do registro (condições, não resultados).**
> - Os dados são as 77.340 palavras a-z do WordNet (Parte 111).
> - A comparação com a cópia guardada da Parte 109 (regra da Parte 50) e a contagem por AST ficam para depois do registro.
> - Não as previ, porque já li os dois textos: o que eu leio não vira previsão (regra da Parte 60).

## As perguntas desta parte

1. **P2921 (0xB69).** O texto é o mesmo da Parte 109, reenviado, ou um texto novo? E o que a árvore sintática acha nele (rede, disco, nomes usados e nunca definidos)? ↩ P2711
2. **P2922 (0xB6A).** A "semelhança semântica" por hash mede significado? Os sinônimos ficam mais perto que os pares ao acaso? ↩ P2532
3. **P2923 (0xB6B).** O `random.seed` dentro de `word_to_vector` reinicia o gerador GLOBAL. O que isso faz com o resto do agente (a exploração ε-gulosa, a criatividade)? ↩ P2922
4. **P2924 (0xB6C).** As codificações numéricas da camada 3 (posicional, alfanumérica, numerológica) são injetivas? Quantas palavras colidem, e por qual mecanismo? ↩ P2894
5. **P2925 (0xB6D).** A avaliação metacognitiva ("melhoria média > 0,1 confirma") decide o que sob a hipótese NULA? E a confiança por coeficiente de variação? ↩ P2741
6. **P2926 (0xB6E).** O intervalo de confiança recebido cobre a média com a confiança pedida? ↩ P2925
7. **P2927 (0xB6F).** A auditoria de entrada da camada 10 pode reprovar alguma coisa? ↩ P2711
8. **P2928 (0xB70).** O vetor corrigido (gerador local) é o mesmo vetor do texto? ↩ P2923
9. **P2929 (0xB71).** A avaliação pareada que substitui a do texto acrescenta fronteira entre Python e Java? (rodada 83) ↩ P2897

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (todas em `synthai/nexus_v2.py`, neste commit).**
- **Pares:** `pares_aleatorios(lemas, 2000)` (semente 1161) e `pares_de_sinonimos(2000)` (semente 1160, dois lemas a-z do mesmo sinset).
- **Vetores:** dimensão 10.
- **Nula:** `avaliacao_nula()`, 20.000 tentativas, valor e linha de base iid N(10, 2), 1 experimento.
- **Nula pareada:** `avaliacao_nula_pareada()`, n = 5, t crítico unilateral de 95% com 4 graus de liberdade.
- **Cobertura:** `cobertura(f, c)`, 20.000 amostras N(0, 1) de n = 30.
- **Contaminação:** `contaminacao("synthai", 1000)`.

**A semelhança por hash (P2922).** Os vetores são gaussianos N(0, 1)¹⁰ sorteados a partir do md5 da palavra, então o cosseno entre duas palavras diferentes tem média 0 e variância 1/d. Para gaussianos isso é exato: E[c²] = 1/d, E[c⁴] = 3/(d(d+2)), curtose 3d/(d+2) = 2,5.
- **(a)** O desvio do cosseno sobre os 2.000 pares aleatórios. Centro 1/√10 = 0,3162. O desvio do desvio é 0,3162·√((2,5 − 1)/(4·2000)) = 0,00433, faixa ±1,645 × 0,00433 = **[0,309; 0,323]**. Forma fechada com variância conhecida (sem o fator 1,36).
- **(b)** A média do cosseno nos 2.000 pares de SINÔNIMOS menos a média nos 2.000 aleatórios. O md5 não vê significado, então o centro é 0. O desvio da diferença é √(0,1/2000 + 0,1/2000) = 0,0100, faixa **[−0,0165; 0,0165]**. Se der fora, o hash vê alguma coisa (por exemplo, sinônimos que são variantes de grafia).

**O gerador global (P2923).**
- **(c)** Depois de cada um dos 1.000 vetores da mesma palavra, a próxima chamada do gerador "global" dá quantos valores DISTINTOS? **[1; 1]**. Identidade: `seed(h)` seguido de 10 `gauss` deixa o gerador sempre no mesmo estado. Consequência: todo `random.random() < ε` depois de um vetor tem sempre o mesmo resultado, e a exploração ε-gulosa vira uma constante.
- **(d)** O mesmo com o vetor corrigido (gerador local): **[1.000; 1.000]**. Identidade: o gerador global não é tocado, e 1.000 floats de 53 bits colidem com probabilidade ≈ 10⁶/2⁵⁴ ≈ 0.

**As codificações (P2924).**
- **(e)** A posicional recebida usa A = 0, e um "a" à esquerda é um zero à esquerda. Então valor(w) = valor(w sem os "a" iniciais), e esta é a ÚNICA fonte de colisão (a base 26 com dígitos 0..25 é única a menos dos zeros à esquerda). Previsão: os pares que colidem na posicional, menos os pares que o mecanismo conta (Σ C(g, 2) nos grupos pela palavra sem os "a" iniciais): **[0; 0]**.
- **(f)** Quantos pares colidem na posicional? Mecanismo esperado: palavras "a" + palavra ("abed"/"bed", "afoot"/"foot", "awake"/"wake", "ajar"/"jar"). Das ~77 mil palavras, umas 4 a 5 mil começam com "a", e uma fração de 3% a 20% delas tem o resto no dicionário. Faixa **[150; 900]** (larga, com o mecanismo escrito: um acerto com outro mecanismo não conta como acerto do raciocínio).
- **(g)** Valores distintos da alfanumérica (soma A = 1 … Z = 26). Mecanismo: a soma vai de 1 a ~26·L, e as palavras têm ~2 a ~25 letras com média de letra ~10 a 13, então os valores enchem densamente de ~5 a ~250 e ficam ralos acima. Faixa **[200; 340]**.
- **(h)** A numerológica (soma dos códigos reduzida a um algarismo, que é a soma mod 9, com 9 no lugar do 0). O maior |fração − 1/9| entre os 9 valores. A soma de várias letras mistura bem mod 9, então os valores são quase uniformes. O desvio binomial é √(1/9 · 8/9 / 77.340) = 0,00113, e o máximo de 9 desvios fica perto de 2,5σ. Faixa **[0; 0,004]**.

**A avaliação sob a nula (P2925).** Com 1 experimento, "confirmed" ⇔ v > 1,1·b (b > 0 quase sempre). v − 1,1b ~ N(10 − 11, 4 + 1,21·4) = N(−1; 8,84), então P(confirmed) = 1 − Φ(1/√8,84) = 1 − Φ(0,3363) = 0,3683. E v − 0,9b ~ N(1; 4 + 0,81·4) = N(1; 7,24), então P(rejected) = Φ(−1/√7,24) = Φ(−0,3716) = 0,3551.
- **(i)** Fração de "confirmed" sob a nula. Desvio binomial √(0,3683·0,6317/20.000) = 0,00341, faixa **[0,3627; 0,3739]**.
- **(j)** Fração de "rejected" sob a nula. Desvio 0,00338, faixa **[0,3495; 0,3607]**. Juntas: sob a nula, o avaliador recebido decide (confirma ou rejeita) em ~72% das vezes.
- **(k)** A avaliação pareada corrigida (n = 5, t crítico unilateral de 95%) sob a mesma nula. As diferenças são normais e a t é exata, então P(confirmed) = 0,05. Desvio √(0,05·0,95/20.000) = 0,00154, faixa **[0,0475; 0,0525]**.
- **(l)** A confiança recebida para os valores [−1, −100, 50] (média −17, desvio 61): **[0,9; 0,9]**. Identidade: CV = 61/(−17) < 0,1 cai no primeiro degrau, a confiança máxima com a maior dispersão.

**O intervalo de confiança (P2926).** O recebido usa a variância populacional e z = 2,576 para QUALQUER confiança ≠ 0,95. A cobertura é P(|T₂₉| < z·√(29/30)).
- **(n)** Pedida 0,90 (vem z = 2,576): 2·F₂₉(2,5327) − 1 = 0,9830. Desvio 0,00091, faixa **[0,9815; 0,9845]**. Mais largo que o pedido: 98% em vez de 90%.
- **(o)** Pedida 0,95 (z = 1,96 com a variância populacional): 2·F₂₉(1,9271) − 1 = 0,9362. Desvio 0,00173, faixa **[0,9334; 0,9390]**. Mais estreito que o pedido.
- **(p)** O corrigido (`ic_t`, a t com n − 1) pedido a 0,90: centro 0,90, desvio √(0,09/20.000) = 0,00212, faixa **[0,8965; 0,9035]**.

**A auditoria e o vetor (P2927/P2928).**
- **(q)** A auditoria recebida com um tratador que DEVOLVE A ENTRADA sem escapar (o XSS e o caminho "../" voltam intactos): "passed" **[7; 7]**. Identidade: os dois ramos somam "passed".
- **(r)** A auditoria com oráculo (`auditoria_com_oraculo`) com o mesmo tratador: as falhas **[3; 3]**. Identidade pela definição do oráculo: a aspa da injeção SQL, o "<script" e o "..". E o controle limpo, um tratador que escapa ("<" → "&lt;", "." → "", "'" → ""), tem que dar 0 falhas: **[0; 0]** (registrado como parte de (r): as duas metades têm que valer).
- **(s)** O vetor corrigido contra o recebido, para as 2.000 primeiras palavras em ordem alfabética: o número de vetores que diferem em algum bit, **[0; 0]**. Identidade: `random.Random(int)` e `random.seed(int)` passam pelo mesmo `init_by_array` do Mersenne Twister.

**Diálogo (P2929).**
- **(t)** A avaliação pareada (rodada 83) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷, √, com as somas em laço na mesma ordem.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

- **(m1)** nº de previsões do mundo em **[16; 20]** (18 agora: a até t sem m)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[3; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,10]**
- **(m4)** fração de acertos do mundo em **[0,70; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Os riscos estão onde não há conta fechada:
- **(f) e (g):** contagens no dicionário com o centro chutado pelo mecanismo.
- **(h):** a mistura mod 9 supõe que as palavras curtas pesam pouco.
- **(b):** se houver sinônimos que são a mesma grafia em caixas diferentes, o md5 os vê como iguais? Não: eu tiro as maiúsculas antes, e os pares do mesmo sinset são palavras diferentes.

Espero **1 a 3 erros**, em (f), (g) ou (h). As identidades (c), (d), (e), (l), (q), (r), (s), (t) só erram se eu tiver lido o código errado, e isso aconteceu duas vezes desde a Parte 109.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
