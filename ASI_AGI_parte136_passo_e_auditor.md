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

Feita com código antes da simulação nova, a conta do ganho por modo em T = 24, 2T·log₁₀(ρ_média/ρ_fixo), dá −0,207 no modo
mais lento (λ = 1). A calibração (−0,19 a −0,24) é esse modo, porque lá ele dominava. No caso de teste o modo lento pesava pouco (o
fixo deu −4,79), e os modos do meio ganham mais por passo. A explicação é uma hipótese até o teste:

| | quantidade | faixa | procedência |
|---|---|---|---|
| (j) | em 4 partidas novas (sementes 6 a 9), \|simulado − recorrência por modo\| / recorrência, média exponencial | [0; 1e-9] | identidade: a recorrência é a mesma conta na base própria |
| (k) | em cada uma das 4, média − fixo dentro de [ganho do modo mais favorável; ganho do modo mais lento] por modo | 4 de 4 | mecanismo: f_T é uma soma de modos, e a diferença dos log fica entre os ganhos extremos se nenhum modo inverte de sinal; P(uma) ≈ 0,97 → P(4/4) ≈ 0,89 |

Registradas antes de rodar.
