# Parte 121 — O NEXUS–RAPHAEL 2.2.0: um laboratório que se audita, auditado (0x79)

↩ Parte 116 (o NEXUS "v2" colado, truncado) · ↩ Parte 109 (o v0.1.0) · ↩ Parte 74 (uma expectativa só muda com justificativa de fora do código) · ↩ Parte 75 (um verificador só vale com um caso de controle de cada lado)

> **Recebido:** o arquivo `nexus_raphael.py`, anexado, e na mesma mensagem um texto colado (o "NEXUS-RAPHAEL v2.0", também truncado, no meio de `MemoriaOperacional`). Não houve pedido escrito novo; o anterior foi "Mande-me em PYTHON o arquivo aprimorado, estendido, expandido, recalculado, corrigido". A Parte 120 (o Leduc) continua ABERTA: um texto recebido no meio do trabalho entra como parte nova, sem abandonar a que estava aberta (regra da Parte 75). Por isso esta é a 121.
>
> **A leitura escolhida (escrita ANTES de medir).**
> - **O arquivo anexado e o texto colado são DOIS textos diferentes.**
>   - **O arquivo** (cabeçalho "NEXUS–RAPHAEL 2.2.0", `VERSAO = "2.2.0"`, 1.744 linhas, sha256 `bfcdab0e…`) fecha como Python. Está arquivado intacto em `externos/nexus_raphael_v2_0/nexus_raphael_v2_0.py.txt` (`.txt`: não é importável). Nunca é importado nem executado.
>   - **O texto colado** não foi guardado por inteiro: é longo e está truncado. Ficam registradas só as duas linhas que eu medi dele (abaixo).
> - **Pela árvore sintática (sem executar):**
>   - **Rede:** existe (`urllib.request.urlopen`, para a API dictionaryapi.dev), mas DESLIGADA por padrão (`permitir_rede=False`; liga só com `--online`), com espera de 1 s entre consultas e limite de 250 kB.
>   - **`importlib`:** só `find_spec` (não carrega nada).
>   - **Disco:** escreve só dentro de um diretório de trabalho (`raiz`).
>   - **O resto:** nada de `exec`, `eval` ou `subprocess`.
>   - É de longe o texto recebido mais cuidadoso da série: tem divisão treino/teste, bootstrap, cartões de hipótese com critérios escritos antes e testes de unidade próprios. A rede desligada por padrão é a primeira vez que um texto recebido faz o que eu teria feito.
> - **O que se mede:** as afirmações que o próprio arquivo faz sobre os seus experimentos, numa transcrição com o mesmo comportamento (`synthai/nexus_v2_2.py`, funções `recebido_*`, a mesma ordem de sorteios), conferidas por contas fechadas e por algoritmos independentes (regra da Parte 88).
>
> **Antes do registro (conferências, não previsões).**
> - **A calibração do experimento do ângulo** (H-M2-001): semente 99, escolhida por regra (fora das sementes 0 a 4 do teste), modo "rápido". Brier da base 0,2558, do transformado 0,0177, ganho 0,2381.
> - **Do texto colado (lido, não medido por execução):** `GerenciadorSeeds.obter_seed` faz `hash_obj.digest[:4]`, isto é, fatia o MÉTODO `digest`, não o resultado de `digest()`. Isso levanta TypeError na primeira chamada.

## As perguntas desta parte

1. **P3071 (0xBFF).** Os experimentos do arquivo (H-M3, H-M2, H-M10, H-M7) chegam aos vereditos que o desenho deles permite? E o desenho permite chegar a outro? ↩ P2925
2. **P3072 (0xC00).** As contas do laboratório da Mega-Sena (as probabilidades, o qui-quadrado, o IC do bootstrap) estão certas? ↩ P3071
3. **P3073 (0xC01).** Os números de jogos e dinâmica do arquivo (estados do jogo da velha, valor do jogo, expoente de Lyapunov) conferem com algoritmos independentes? ↩ P2384
4. **P3074 (0xC02).** A logística do ângulo duplo, com o exp próprio, é IGUAL em Java? (rodada 87) ↩ P2956

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):**
- **As transcrições e contas independentes:** `synthai/nexus_v2_2.py`.
- **A rodada 87:** `dialogo/rodada87.py`, semente 1210, N = 200.
- **Modo e sementes:** todas as medições no modo "rápido" do arquivo, com as sementes dele (0 a 4; a Mega-Sena usa 42).

**H-M3-001 (taxa condicional contra global).** Com P(y = 1 | x) = 0,15 ou 0,85 e x equiprovável, o Brier da taxa global é ≈ 0,25 e o da condicional ≈ 0,15·0,85 = 0,1275. A diferença por ponto de teste vale 0,25 − 0,0225 = 0,2275 (prob. 0,85) ou 0,25 − 0,7225 = −0,4725 (prob. 0,15). Média 0,1225, desvio 0,25.
- **(a)** O ganho de Brier na semente 0 (60 pontos de teste): 0,1225 ± 1,645 × 0,25/√60 = **[0,069; 0,176]**.
- **(b)** Sementes com veredito ACEITA: **[5; 5]**. Mecanismo: o limite inferior do IC fica perto de 0,1225 − 1,96 × 0,032 = 0,06 > 0 em todas. O próprio cartão admite o risco: o estímulo foi construído para o condicionamento ganhar.

**H-M2-001 (ângulo duplo).** O alvo é 1[cos²θ > 0,49], e cos 2θ = 2cos²θ − 1 o separa linearmente; com só cos θ, a logística não separa (o alvo é simétrico em cos θ).
- **(c)** O ganho de Brier médio nas 5 sementes. Centro tirado da calibração, 0,238, com a meia-largura de ±0,03 da dispersão de um Brier de 100 pontos de teste × 1,36: **[0,19; 0,28]**.
- **(d)** Sementes com veredito ACEITA (IC acima de zero): **[5; 5]**.

**H-M10-001 (Mega-Sena sintética, 400 sorteios, 300 testados).** O número de acertos de 6 dezenas é hipergeométrico, média 6·6/60 = 0,6 e variância 6·0,1·0,9·54/59 = 0,4942.
- **(e)** A média de acertos da escolha aleatória: 0,6 ± 1,645·√(0,4942/300) = **[0,533; 0,667]**.
- **(f)** A diferença média quentes − aleatória: 0 ± 1,645·√(2·0,4942/300) = **[−0,094; 0,094]**.
- **(g)** O qui-quadrado das 60 frequências. Cada dezena está num sorteio com probabilidade 0,1, independente entre sorteios, então E[(c − n/10)²/(n/10)] = 0,9 e a soma dá **54**, não os 59 graus de liberdade de um qui-quadrado comum. A variância é ≈ 2·0,81·60 = 97, desvio 9,8: **[37,9; 70,1]**.
- **(h)** Com `bootstrap = 500` na configuração (o `Configuracao` aceita), o IC por índices fixos [24] e [974] levanta IndexError: execuções que levantam, **[1; 1]**. Identidade: a lista ordenada tem 500 réplicas.
- **(i)** Com `bootstrap = 2.000`, o "limite superior" é a réplica de índice 974, abaixo da mediana (índice 999,5): casos em que o limite superior fica ≤ a mediana das réplicas, **[1; 1]**. Identidade: as réplicas estão ordenadas e 974 < 999.

**H-M7-001 (reforço extraordinário contra ordinário).** A recompensa extraordinária é afim no acerto mais um ruído de diagnóstico. Os valores esperados por braço são 2p − 1 + 0,2(1 − p): 0,55 para o braço bom e 0,19 para o ruim, a MESMA ordem da recompensa ordinária (0,75 e 0,55). E a avaliação reservada usa o MESMO gerador (seed + 10.000) para os dois tipos.
- **(j)** Sementes com diferença extraordinário − ordinário EXATAMENTE 0,0: **[5; 5]**. Mecanismo: os dois escolhem o mesmo braço, e o avaliador sorteia os mesmos 200 números. O critério "ganho positivo nas cinco seeds" não pode ser satisfeito por este desenho, e o veredito fica INCONCLUSIVA por construção, não por evidência.

**Jogos e dinâmica (P3073).**
- **(k)** Os tabuleiros alcançáveis do jogo da velha: a contagem do arquivo (busca em profundidade com memória) menos a minha por camadas, **[0; 0]**. Identidade: as duas contam o mesmo conjunto, por caminhos diferentes.
- **(l)** O valor do jogo da velha com jogo perfeito, pela minha negamax com poda alfa-beta: **[0; 0]** (empate). Identidade: o resultado da minimax não depende da poda.
- **(n)** O expoente de Lyapunov do mapa logístico em r = 4, pela função do arquivo (20.000 iterados): ln 2 = 0,6931, com o ruído de uma média ergódica de 20.000 termos correlacionados: **[0,67; 0,72]**.

**O diálogo (P3074).**
- **(o)** A rodada 87 (as duas logísticas com o exp próprio, 300 passos) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: o LCG é exato, cos 2θ entra como 2u² − 1 (sem cosseno), e o resto é +, −, ×, ÷ e o exp próprio.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **14**, mais até 2 de um adendo.
- **(m1)** nº de previsões do mundo em **[14; 16]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[4; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,25]**
- **(m4)** fração de acertos do mundo em **[0,70; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros vou ter" = 0 × identidades + 0,10 × faixas de forma fechada de 90% + ~0,2 × faixas de mecanismo.
- **Identidades:** 5 ((h), (i), (k), (l), (o)).
- **Formas fechadas:** 4 ((a), (e), (f), (g)), que dão 0,4.
- **Mecanismo:** 5 ((b), (c), (d), (j), (n)), que dão 1,0.

Isso dá centro **1,4** e faixa **[0; 3]**. O risco maior está em (j): se, numa semente, o ordinário escolher o braço ruim no começo e não sair, a diferença deixa de ser 0.

### Adendo pré-registrado (escrito DEPOIS da 1ª medição, ANTES destes testes)

Duas faixas [5; 5] erraram: a (b) deu 4 ACEITA e a (j) deu 4 diferenças zero.

- **(b): o meu erro de mecanismo.** "Passa em todas" pede a probabilidade POR SEMENTE elevada a 5, e eu não fiz essa conta. Pela normal, P(limite inferior > 0) = P(Z > (0,063 − 0,1225)/0,032) = 0,969 por semente, e 0,969⁵ = 0,85: a faixa [5; 5] tinha 15% de chance de errar.
- **(j): o mecanismo que eu NÃO previ.** Na semente 1, o reforço EXTRAORDINÁRIO terminou no braço RUIM: as primeiras falhas valem −1, e o braço bom só voltou a ser visto pela exploração (60 de 1.000 vezes). A conta do sinal-ruído dos dois tipos de recompensa diz que esse travamento deveria ser IGUALMENTE provável nos dois tipos:
  - ordinária: diferença de 0,20 entre os braços, desvio ~0,47 (razão 0,43);
  - extraordinária: diferença de 0,36, desvio ~0,86 (razão 0,42).

Dois testes novos, nas sementes 100 a 1.099 (1.000 sementes nunca usadas):
- **(q)** A fração de sementes em que o EXTRAORDINÁRIO termina no braço ruim, menos a do ORDINÁRIO. Se a razão sinal-ruído decide, o centro é 0. Com p ~0,05 em cada um, o desvio é √(2·0,05·0,95/1.000) = 0,0097, e a faixa é ±1,645 × 0,0097 × 1,36 = **[−0,022; 0,022]**. Se der positivo além disso, a recompensa negativa trava mais do que a razão sinal-ruído explica.
- **(r)** A fração das sementes 100 a 1.099 em que H-M3-001 dá ACEITA: 0,969 ± 1,645·√(0,969·0,031/1.000) × 1,36 (a normal é aproximação) = **[0,957; 0,981]**.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
