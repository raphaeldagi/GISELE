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

## As respostas (quatro camadas)

### P3071 — Os experimentos chegam aonde o desenho deixa?

**Na pergunta.** Um experimento honesto é aquele que PODE dar o resultado contrário. A pergunta não é se o veredito saiu certo, e sim quais vereditos o desenho permite.

**Lógica.**
- **H-M3-001 (taxa condicional contra global).**
  - O ganho de Brier na semente 0 é **0,1215** ✅ (a), contra 0,1225 da conta.
  - Mas só **4 de 5** sementes dão ACEITA: **(b) ❌**. A semente 3 tem limite inferior −0,016.
  - O erro foi meu, de conta: "passa nas cinco" pede P(passa)⁵, e eu escrevi [5; 5] sem fazê-la. Pela normal, 0,969⁵ = 0,85.
  - Em 1.000 sementes novas, a taxa de ACEITA por semente é **0,93**, e não 0,969: **(r) ❌**, por z = −7,1. A minha aproximação normal estava otimista. Com 0,93 por semente, "ACEITA nas cinco" acontece 0,93⁵ = **70%** das vezes, e o critério do cartão ("limite inferior > 0 em cada seed") rejeita um efeito real e grande (ganho de 0,12 em Brier) 30% das vezes.
  - **Hipótese (1 lote), sem mecanismo ainda:** a distribuição das diferenças tem dois pontos (+0,23 e −0,47), é assimétrica, e o percentil do bootstrap com 60 pontos fica mais baixo que o da normal. O ruído das taxas estimadas no treino também conta. Fica para um teste que separe as duas causas.
- **H-M2-001 (ângulo duplo).** O ganho médio é **0,229** ✅ (c), e o IC fica acima de zero nas **5** sementes ✅ (d). O alvo foi construído com a simetria que cos 2θ separa, e o cartão diz isso no campo "riscos".
- **H-M7-001 (reforço extraordinário).**
  - A diferença é **0,0 EXATO em 4 sementes**: os dois tipos escolhem o mesmo braço, e o avaliador reservado sorteia os mesmos 200 números para os dois.
  - Na semente 1, o extraordinário travou no braço RUIM (−0,245): **(j) ❌**. As primeiras falhas valiam −1, e o braço bom só voltou pela exploração (60 de 1.000 vezes, q₀ = 0,147 no fim contra 0,55 verdadeiro).
  - **O travamento é RARO e igual nos dois:** nas 1.000 sementes novas, **0,000** contra **0,000** ✅ (q). A semente 1 foi um caso de menos de 1 em 1.000.
  - **A conclusão sobre o desenho:** H-M7 só sai do "INCONCLUSIVA" quando um dos dois trava no braço ruim, e isso acontece em menos de 0,1% das sementes. O critério "ganho positivo nas cinco seeds" quase nunca pode ser satisfeito. O experimento mede o acaso do travamento, não o valor do diagnóstico.

**Tradução cruzada.** Três desenhos, três relações com a verdade.
- **H-M3** pergunta uma coisa verdadeira com um critério severo demais: rejeita o real 30% das vezes.
- **H-M2** pergunta uma coisa que o estímulo já responde.
- **H-M7** pergunta uma coisa que o desenho não pode responder.

É a diferença de Popper entre uma hipótese refutável e uma que o protocolo blinda, mas aqui a blindagem é involuntária: os dois tratamentos compartilham o avaliador e convergem para o mesmo braço.

### P3072 — As contas da Mega-Sena

**Lógica.**
- **As probabilidades combinatórias estão certas:** C(60, 6) = **50.063.860**.
- **As médias de acertos:**
  - aleatória **0,5867** ✅ (e), z = −0,33;
  - "quentes" (as 6 mais sorteadas nos últimos 100) **0,6267** e "frias" **0,6233**: tudo dentro do acaso.
- **A diferença quentes − aleatória:** **+0,040** ✅ (f), com IC [−0,073; 0,153], INCONCLUSIVA como deve ser em sorteios uniformes.
- **O qui-quadrado das frequências:** **57,25** ✅ (g), contra a esperança fechada **54**, e não 59. Cada dezena está em 1/10 dos sorteios, então cada termo vale em média 1 − 1/10. O arquivo deixa o p-valor em branco ("sem teste p"), e é bom que deixe: a referência χ²₅₉ estaria errada.
- **Dois defeitos reais no IC**, ambos por usar ÍNDICES FIXOS [24] e [974] em vez de quantis do número de réplicas:
  - com `bootstrap = 500` (a configuração aceita), **IndexError** ✅ (h);
  - com `bootstrap = 2.000`, o "limite superior" (0,0367) fica **abaixo da mediana** (0,04) ✅ (i), um intervalo que exclui a própria estimativa.
  - A correção (`ic_por_quantis`) usa os índices 49 e 1.949 para 2.000 réplicas.

### P3073 — Jogos e dinâmica

**Lógica.**
- **Os tabuleiros alcançáveis do jogo da velha:** **5.478** pela busca do arquivo e **5.478** pela minha contagem por camadas ✅ (k).
- **O valor do jogo:** **0** (empate) pela negamax com poda alfa-beta ✅ (l). O controle passa: com "XX.OO....", o X ganha (valor 1).
- **O expoente de Lyapunov em r = 4:** **0,69310**, a 5·10⁻⁵ de ln 2 ✅ (n).

As contas que o arquivo marca como [MEDIDO] conferem.

### P3074 — rodada 87

**Lógica.** As duas logísticas do ângulo duplo, com o exp próprio, em Python × Java: **IGUAIS, 3 linhas e 8 números bit a bit** ✅ (o).
- Só com u (o papel de cos θ), o Brier é **0,203**. Com 2u² − 1, cai para **0,021**, e o peso do atributo duplo é **7,43**.
- O ângulo duplo entra como 2u² − 1, a identidade, sem chamar cos: não acrescenta fronteira. O verificador confere 87 rodadas com par Python/Java (P2984).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ❌ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (q) ✅ (r) ❌. Parte 121: **16 testes, 3 erros**. Acumulado (mundo), sem a Parte 120 que segue aberta: **229 erros em 959 testes**. Calibração (P1961, Partes 80–121 sem a 120): **274/300 = 0,913**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4; conta as 2 do adendo).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [14; 16] | 16 | ✅ |
| (m2) | [4; 7] | 5 | ✅ |
| (m3) | [0; 0,25] | 0,012 | ✅ |
| (m4) | [0,70; 1,00] | 0,81 | ✅ |
| (m5) | [0; 1] | 0 | ✅ |
| (m6) | [0; 2] | 3 | ❌ |

Previsões sobre previsões: **5 de 6**. As três surpresas: (b) e (j), faixas de largura zero erradas por 1, e (r), errada por 0,027 com largura 0,024.

### Sobre mim

**"[0; 3] erros, centro 1,4": ✅ (3, no limite).** A regra da Parte 117 pôs o centro no lugar certo de ordem de grandeza. Os três erros vieram todos de faixas de MECANISMO (o centro previa 1,0 delas) e nenhum de forma fechada.

## Engenharia reversa (metacognição)

**O padrão: escrevi [k; k] para "acontece em todas as unidades" sem multiplicar as probabilidades.** (b) e (j) são a mesma forma de erro: uma propriedade que vale com probabilidade alta por semente virou uma identidade sobre 5 sementes. A Parte 110 já tinha a regra "[x; x] só com a identidade escrita ao lado", e eu a contornei chamando de "mecanismo" o que era uma probabilidade. **Significado:** eu leio "quase sempre" como "sempre" quando o caso individual parece óbvio (o ganho é grande, os braços são bem separados). A conta pⁿ derruba essa intuição: 0,97⁵ = 0,85. **Regra:** uma previsão sobre "todas as k unidades" escreve ao lado P(uma unidade) e P(todas) = pᵏ. A faixa [k; k] só existe se pᵏ ≥ 0,90; senão, a faixa é a binomial.

**O segundo: a aproximação normal de um percentil de bootstrap com 60 pontos assimétricos foi otimista por z = −7.** Não é ruído. É uma conta que eu não fiz: o bootstrap percentil de uma média de dois valores (+0,23 e −0,47) tem cauda inferior mais pesada que a normal. Fica como hipótese, com o teste que separa as causas escrito nas pendências. **Significado:** "aproximadamente normal" é uma suposição de forma (regra da Parte 31) que eu não verifiquei. Com n = 60 e um ponto em −0,47, ela não vale.

**O terceiro, sobre o texto recebido: pela primeira vez, ele é melhor do que a prosa dele promete.** Nas Partes 72 a 116, os textos prometiam mais mecanismo do que o código entregava. Este arquivo diz "não é AGI", liga a rede só com uma flag, registra os critérios antes, marca os dados como sintéticos e admite nos riscos que o estímulo favorece o efeito. Os defeitos medidos são de DESENHO (H-M7 não pode aceitar; o critério de H-M3 rejeita o real 30% das vezes) e de INDEXAÇÃO (o IC da Mega-Sena), não de honestidade. **Significado:** a série de auditorias mudou de objeto. A pergunta deixa de ser "o código faz o que diz?" e passa a ser "o experimento pode dar o resultado contrário?".

## Síntese / unificação

O NEXUS–RAPHAEL 2.2.0 anexado foi arquivado intacto (`externos/nexus_raphael_v2_0/`) e medido no próprio código, transcrito em `synthai/nexus_v2_2.py`.

**O que confere:**
- os tabuleiros do jogo da velha (5.478, por dois caminhos) e o valor do jogo (0);
- o expoente de Lyapunov (ln 2 a 5·10⁻⁵);
- as probabilidades da Mega-Sena e as médias de acertos (o acaso);
- o ganho do ângulo duplo (0,229, em 5 de 5 sementes).

**O que não se sustenta:**
- **H-M3:** o critério "IC > 0 em cada uma das 5 sementes" rejeita um efeito grande e real em 30% das vezes (0,93⁵ = 0,70).
- **H-M7:** o desenho não pode aceitar, porque os dois tratamentos compartilham o avaliador e convergem para o mesmo braço (0,0 exato em 4 de 5 sementes; travamento em menos de 0,1%).
- **O IC da Mega-Sena:** índices fixos [24] e [974] quebram com 500 réplicas (IndexError) e põem o "limite superior" abaixo da mediana com 2.000.
- **O qui-quadrado:** tem esperança 54 (60 × 0,9), não 59.
- **No texto colado:** `digest[:4]` fatia o método e levanta TypeError.

Rodada 87: a logística do ângulo duplo, IGUAL (87 rodadas). 13/16 do mundo, 5/6 (m), calibração **0,913** (sem a Parte 120, aberta).

## Meta

**Confiança.**
- **Alta:** as identidades (h, i, k, l, o) e as formas fechadas (a, e, f, g).
- **Média:** a afirmação sobre H-M7. O travamento medido é raro nas duas versões (0/1.000); que ele torne o critério quase impossível de satisfazer é uma conta (o critério pede ganho > 0 em todas as 5), mas a frequência real de "ganho > 0" não medi diretamente.

**Onde pode estar errado.** As transcrições reproduzem o comportamento das funções que eu li, não o arquivo executado. Uma diferença de transcrição mudaria os números. Mitigação: as transcrições usam a mesma ordem de sorteios e as mesmas constantes, e as contas fechadas batem com elas.

## Diálogo Python ↔ Java (rodada 87)

Ver `dialogo/DIALOGO.md`: as duas logísticas do ângulo duplo (exp próprio, 300 passos) são **IGUAIS**, com 3 linhas e 8 números bit a bit.

## Fontes

O limite semanal de buscas na web acabou no meio da Parte 120, então esta parte não cita fonte externa nova. As contas são todas fechadas e conferidas por código:
- a combinatória da Mega-Sena;
- a hipergeométrica;
- a esperança do qui-quadrado;
- o ln 2 do mapa logístico.

➡ Continua na [Parte 122 — O texto NEXUS–RAPHAEL v3.0](ASI_AGI_parte122_nexus_v3_0.md).
