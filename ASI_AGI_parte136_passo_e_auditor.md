# Parte 136 — "Use tudo que enviei": o passo numa quadrática anisotrópica e um auditor de capacidades

↩ Nasce da Parte 135 (o programa "use tudo que enviei até hoje em cada módulo") e da P2236/P2792 (as auditorias por AST).

## O inventário que abriu a parte
Antes de escolher o que construir, cruzei por código cada arquivo recebido em `externos/` com os módulos do pacote. Cinco módulos recebidos
nunca chegaram a nenhum: `pacote3/aprendizagem_continua.py`, `pacote3/inovacao_guiada.py`, `pacote3/rl_grupos.py`,
`pacote3/transferencia_metacognitiva.py` e `pacote_v015/objetivos_cognitivos.py`. A busca foi por NOME de arquivo, o que é menção e não uso
(a lição das Partes 109 a 112). Parte das ideias deles já foi usada com outro nome: o GRPO na Parte 87 e o Shrink & Perturb na Parte 87.
O inventário completo, com a coluna "que módulo usa", é trabalho da próxima parte. Esta começa pelos dois que formam um par natural:
- `objetivos_cognitivos.py`: a quadrática SPD com condição κ (autovalores de 1 a κ em progressão geométrica, base ortonormal sorteada);
- `inovacao_guiada.py`: três intervenções no passo da descida. São o passo de secante 0,8·(s·s)/(s·y) (Barzilai–Borwein), protegido e
  recortado em [0,002; 0,4]; a média exponencial do gradiente com peso 0,6 no atual; e o limite da norma do deslocamento.

Os dois usam numpy, e `inovacao_guiada.py` importa um `recursiva_paraconsistente` que não veio no pacote. Por isso não rodam como
chegaram. A reescrita está em `synthai/passos.py`, offline e só com a biblioteca padrão.

### Um defeito meu, achado pelo controle
Auditei os cinco com o `security_audit_ast_v2` da Parte 111 e deu limpo. Mas, pela regra da Parte 75, rodei antes um controle plantado:
`subprocess.Popen` passou sem acusação. O auditor só procura REDE, como diz o próprio código. Eu o usei como auditoria geral desde a
Parte 111, e ele não é. O auditor novo (`auditar_capacidades`) conta quatro capacidades por uso, não por menção:
- rede;
- processo (subprocess, multiprocessing, os.system, fork, exec*);
- código dinâmico (eval, exec, compile, `__import__`, importlib.exec_module & cia.);
- desserialização (pickle, marshal, shelve).

Ele passou nos dois controles antes deste registro:
- o defeito plantado: Popen, os.system, os.fork, eval, pickle.loads e exec_module foram todos acusados;
- o caso limpo: as mesmas palavras dentro de uma string e um `from urllib.parse import quote` não geraram nenhum achado. Um fonte inválido
  dá "não analisável".

## Perguntas
- **(a)** Na quadrática d = 8, κ = 10, semente 31001 (a do texto recebido), partida gaussiana (semente 5), a descida de passo fixo η = 0,05 em
  24 passos reproduz a forma fechada Σλc²(1−2ηλ)^{2T}/Σλc²?
- **(b)** Que razão f₂₄/f₀ a forma fechada dá, e a simulação confere?
- **(c)** Quanto o passo de secante do texto recebido ganha, nos mesmos 24 passos?
- **(d)** E a média exponencial do gradiente (β = 0,6), sem ruído?
- **(e)** A média exponencial reduz a variância de um ruído branco por β/(2−β)?
- **(f)** Com ruído σ = 0,5 no gradiente, o custo médio estacionário do passo fixo é o piso ησ²/4·Σ1/(1−ηλ)?
- **(g)** O auditor novo acusa o próprio fonte?
- **(h)** Quantos dos 15 arquivos recebidos em `externos/` (os .py e os .py.txt) têm alguma das quatro capacidades?
- **(i)** E dos 7 módulos de `pacote3/` e `pacote_v015/`?

## Previsões, registradas antes de qualquer execução do caso de teste
As calibrações usaram outras dimensões (d = 4, 6, 10) e outras sementes (777, 778). A forma fechada de (b) e o piso de (f) foram calculados
antes de simular, porque são a conta.

**Procedência:**
- identidades: (a), (g);
- forma fechada: (b), (e), (f);
- calibração ou mecanismo: (c), (d), (h), (i).

O centro de "quantos erros" é 0 + 3 × 0,10 + 4 × 0,25 = 1,3.

| | quantidade | faixa | procedência |
|---|---|---|---|
| (a) | \|simulado − fechado\| / fechado | [0; 1e-10] | identidade: na base própria cada coordenada é multiplicada por (1 − 2ηλ) |
| (b) | log₁₀(f₂₄/f₀), passo fixo | [−4,80; −4,78] | a forma fechada dá −4,7891 |
| (c) | log₁₀(f₂₄/f₀), secante | [−12,0; −9,5] | calibração em d = 6 e 10, duas sementes cada: média −10,74, desvio 0,54, erro do centro 0,27; 1,645·√(0,54² + 0,27²) × 1,36 = 1,23 |
| (d) | log₁₀ da média − log₁₀ do fixo | [−0,40; −0,05] | calibração −0,215 ± 0,02. Mas a variável que move o efeito (o peso dos modos lentos) NÃO está coberta: o fixo calibrado deu −2,8 a −3,6, o deste caso −4,79. Faixa alargada, e o acerto não confirma o mecanismo |
| (e) | variância medida, β = 0,6, 199.000 passos | [0,4260; 0,4312] | β/(2−β) = 0,428571; desvio do estimador para um AR(1) com ρ = 0,4: 0,4286·√(2/144.100) = 0,0016; × 1,645 |
| (f) | custo médio dos passos 1.000 a 3.000, σ = 0,5 | [0,0306; 0,0352] | o piso fechado ησ²/4·Σ1/(1−ηλ) = 0,03291; ±7% (cerca de 200 amostras efetivas por modo, 8 modos) |
| (g) | achados do auditor no próprio fonte | [0; 0] | identidade: as palavras perigosas só aparecem em conjuntos de strings |
| (h) | arquivos com alguma capacidade, dos 15 | [3; 5] | o R37 (processo, código dinâmico e rede, Parte 109), o NEXUS 2.2.0 (urllib, Parte 121), um dos word_rl_lab (rede, Parte 111) e talvez o arquitetura_pos_asi (Parte 33) |
| (i) | dos 7 módulos de pacote3 e pacote_v015 | [0; 1] | o v2 deu limpo na rede; processo e código dinâmico não foram olhados |

**Sobre mim:** erros no mundo em [0; 3], com centro 1,3.

➡ Anterior: [Parte 135](ASI_AGI_parte135_volta8.md).

## Medido (P3177–P3179)
| | medido | faixa | |
|---|---|---|---|
| (a) | erro relativo 0,0 (exato) | [0; 1e-10] | ✅ |
| (b) | −4,7891 (a forma fechada dava −4,7891) | [−4,80; −4,78] | ✅ |
| (c) | **−11,562**: o passo de secante dá 10⁶·⁸ vezes menos custo que o fixo em 24 passos | [−12,0; −9,5] | ✅ |
| (d) | **−0,405** | [−0,40; −0,05] | ❌ por 0,005 |
| (e) | 0,42802 (fechada 0,428571; z = −0,34) | [0,4260; 0,4312] | ✅ |
| (f) | 0,03259 (piso 0,03291, razão 0,990) | [0,0306; 0,0352] | ✅ |
| (g) | nenhum achado no próprio fonte | [0; 0] | ✅ |
| (h) | **6** de 15 | [3; 5] | ❌ |
| (i) | 0 de 7 | [0; 1] | ✅ |

**Mundo: 7 de 9.**

### (h): a régua estava certa e a minha memória não
Antes de explicar, conferi o que casou em cada arquivo (a regra das Partes 109 e 127):
- o NEXUS 0.1.0 colado tem `import urllib.request` na linha 22 e `urlopen` na 914;
- os dois word_rl_lab importam `requests`;
- o R37 tem as quatro capacidades;
- o NEXUS 2.2.0 tem a rede;
- o `arquitetura_pos_asi.py` tem `compile` e `exec`, que era o código gerado da Parte 33.

As seis acusações são reais. Eu previ três a cinco pela lembrança das auditorias antigas, e a docstring do meu próprio `synthai/nexus.py`
já dizia "o original tinha urllib". É a regra da Parte 75 com uma fonte nova de imagem: a MEMÓRIA de uma auditoria também é imagem, e o
REGISTRO dela (a docstring, a parte) é a contagem. Um defeito menor da régua apareceu na mesma conferência: `import nltk` contava como rede,
mas só `nltk.download` é. O veredito não muda, porque os dois arquivos também importam `requests`; mesmo assim, corrigi o auditor (abaixo).

### (d): um teste novo antes de qualquer mecanismo
A média exponencial com passo η é o método do heavy-ball: x' = x − ηβg + (1 − β)(x − x₋₁). Na base própria, cada modo segue a
recorrência escalar c_{t+1} = c_t − η·m_t, m_t = β·2λ·c_t + (1 − β)·m_{t−1}. Por modo, o raio espectral é a maior raiz de
z² − (2 − β − 2ηβλ)·z + (1 − β) = 0; o do passo fixo é |1 − 2ηλ|.

Feita com código antes da simulação nova, a conta do ganho por modo em T = 24, 2T·log₁₀(ρ_média/ρ_fixo), dá −0,206 no modo
mais lento (λ = 1). A calibração (−0,19 a −0,24) é esse modo, porque lá ele dominava. No caso de teste o modo lento pesava pouco (o
fixo deu −4,79), e os modos do meio ganham mais por passo. A explicação é uma hipótese até o teste:

| | quantidade | faixa | procedência |
|---|---|---|---|
| (j) | em 4 partidas novas (sementes 6 a 9), \|simulado − recorrência por modo\| / recorrência, média exponencial | [0; 1e-9] | identidade: a recorrência é a mesma conta na base própria |
| (k) | em cada uma das 4, média − fixo dentro de [ganho do modo mais favorável; ganho do modo mais lento] por modo | 4 de 4 | mecanismo: f_T é uma soma de modos, e a diferença dos log fica entre os ganhos extremos se nenhum modo inverte de sinal; P(uma) ≈ 0,97 → P(4/4) ≈ 0,89 |

Registradas antes de rodar.

### Medido no teste novo (P3180)
| | medido | faixa | |
|---|---|---|---|
| (j) | erros de 6·10⁻¹⁶ a 1·10⁻¹⁴ nas 4 partidas | [0; 1e-9] | ✅ |
| (k) | média − fixo = −0,589, −0,324, −0,306, −0,213; as 4 dentro de [−3,039; −0,206] | 4 de 4 | ✅ |

Os ganhos por modo, pela taxa assintótica, foram calculados por código antes do teste: −0,206, −0,491, −1,447, −3,039, +0,173, +5,661,
+16,962 e +∞, para λ de 1 a 10. O último é +∞ porque o passo η = 0,05 ZERA o modo do topo num passo: 1 − 2·0,05·10 = 0. A média
exponencial ganha nos modos lentos e perde nos rápidos, que o passo fixo mata depressa. Assim, o efeito dela depende de qual modo domina
f_T, e não é uma constante do método. A calibração caía sempre perto de −0,21, porque lá o modo mais lento dominava. Com o mecanismo
confirmado em quatro partidas novas, o erro de (d) deixa de ser só uma faixa curta: o tamanho do efeito é uma média dos ganhos por modo,
ponderada pelo que resta de cada modo em T.

**Placar.** **Mundo: 9 de 11** (7 de 9 no registro, mais 2 de 2 no teste novo). **Sobre mim: 1 de 1.** Previ de 0 a 3 erros, com centro 1,3,
e tive 2.

### As contas, linha por linha
- **(b)** f₂₄/f₀ = Σλ_i c_i²(1 − 2·0,05·λ_i)⁴⁸ / Σλ_i c_i², com λ_i = 10^{i/7} e c = Qᵀx₀. Dá 10^−4,7891, e a simulação dá o mesmo a
  2·10⁻¹⁶.
- **(e)** A média exponencial de ruído branco é um AR(1): m = βg + (1 − β)m₋₁. Então Var m = β²/(1 − (1 − β)²) = β/(2 − β) = 0,6/1,4 = 0,428571.
  O medido foi 0,42802, com z = (0,42802 − 0,428571)/0,0016 = −0,34.
- **(f)** Por modo, c' = (1 − 2ηλ)c − ηξ, com Var ξ = σ². Então Var c = η²σ²/(1 − (1 − 2ηλ)²) = ησ²/(4λ(1 − ηλ)), e o custo é
  λ·Var c = ησ²/(4(1 − ηλ)). Somando os 8 modos: 0,05·0,25/4·Σ1/(1 − 0,05λ_i) = 0,03291. O medido foi 0,03259, razão 0,990.
- **(k)** Na média, z² − (2 − β − 2ηβλ)z + (1 − β) = 0. Com λ = 1: z² − 1,34z + 0,4 = 0, e a maior raiz é (1,34 + √0,1956)/2 = 0,8911,
  contra 0,9 do fixo. Então 48·log₁₀(0,8911/0,9) = −0,206.
- **Chance de acertar ao acaso.** O preditor ingênuo "a média é igual ao fixo" (diferença 0) erraria (k) nas quatro partidas, porque a
  faixa não contém 0. O preditor "a secante dá o mesmo log₁₀ que em d = 4" (−12,18, a calibração de d = 4) cairia fora da faixa de (c) por 0,18, e erraria o medido (−11,56) por 0,62. (A primeira versão desta linha dizia "−9,1" e "por 0,4", de cabeça; corrigido por código.)

## Diálogo — rodada 91
A tradução de `synthai.passos.descer` para Java (`dialogo/Rodada91.java`) cobre o passo fixo, a secante protegida, a média exponencial e o
limite da norma. A matriz e a partida saem de um LCG nas duas linguagens. Resultado: **IGUAIS, 101 linhas e 100 números bit a bit**, na
primeira execução. Duas notas honestas:
1. **A soma.** Antes da rodada troquei, no módulo, o `sum()` (compensado no Python 3.12, Parte 34) por um laço sequencial. Os números
   impressos da parte não mudaram; o (a) passou de 0 para 2·10⁻¹⁶.
2. **O lapso.** Rodei a rodada sem registrar antes a previsão dela, contra a regra da Parte 22. A previsão teria sido "IGUAIS" (só + − × ÷ e
   √, na mesma ordem), mas não posso contá-la como acerto.

## Engenharia reversa
- **O padrão desta parte: uma ferramenta usada além do que ela mede.** O auditor da Parte 111 tem "rede" no nome das suas constantes e eu o
  chamei de auditoria de segurança durante 25 partes. A minha memória das auditorias foi usada como contagem. A calibração da média em
  modos lentos foi usada num caso dominado pelos do meio. É a regra da Parte 105 (toda afirmação de fronteira carrega a faixa de argumentos
  medida), estendida das funções às MINHAS ferramentas: um instrumento vale no regime em que foi medido, e o nome dele diz qual é.
- **O que isso revela.** Quando uma ferramenta minha funcionou uma vez, eu passo a confiar nela pela reputação, a mesma que a Parte 84
  proibiu para os métodos dos outros. O controle plantado pegou isso em segundos. É barato, e deve vir antes de cada uso novo, não só
  na criação.
- **Regra nova (Parte 136):** antes de usar um verificador numa pergunta nova, plantar um defeito DA PERGUNTA NOVA, não o da antiga. E
  toda previsão sobre "qual arquivo recebido tem X" parte do registro escrito da auditoria (grep), nunca da lembrança.

## Funções, testes, fontes
- **Funções:** `p3177_passo_fixo_e_secante`, `p3178_ruido_e_media`, `p3179_capacidades_recebidas`, `p3180_media_por_modo` e `_parte_136`. Entradas
  P3177, P3179 e P3180 na regressão.
- **Módulo:** `synthai/passos.py`, com a quadrática, os passos, a média por modo, o raio espectral e `auditar_capacidades`.
- **Testes:** `synthai/testes_parte136.py`, 16 testes. Cada função é chamada pelo nome, e o auditor tem defeitos plantados, um caso limpo, um
  fonte inválido e o próprio fonte.
- **Fontes** (lidas nesta sessão):
  - J. Barzilai e J. M. Borwein, "Two-Point Step Size Gradient Methods", *IMA J. Numer. Anal.* 8(1):141–148, 1988, doi 10.1093/imanum/8.1.141
    ([verbete](https://en.wikipedia.org/wiki/Barzilai%E2%80%93Borwein_method)). É o passo de secante do texto recebido.
  - B. T. Polyak, "Some methods of speeding up the convergence of iteration methods", *Zh. Vychisl. Mat. Mat. Fiz.* 4(5):791–803, 1964
    ([MathNet](https://mathnet.ru/eng/zvmmf7713)). É o heavy-ball, que a média exponencial do texto recebido é sem dizer.

## A próxima parte
O inventário completo de "tudo que enviei", com uma coluna por módulo, e os três módulos recebidos que faltam: `aprendizagem_continua.py`
(reservatório, posto efetivo, unidades dormentes), `rl_grupos.py` (GRPO com recompensa verificável) e `transferencia_metacognitiva.py`
(memória congelada, comparação pareada).

➡ Próxima: [Parte 137](ASI_AGI_parte137_inventario.md).
