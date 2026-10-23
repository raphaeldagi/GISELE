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
