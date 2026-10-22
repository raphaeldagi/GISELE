# Parte 124 — Os módulos pendentes, um arquivo consolidado por módulo

↩ Nasce das pendências da Parte 123 (rodada 91) e do pedido "Continue os módulos. Me entregue um arquivo consolidado por módulo."
Os sete módulos estão em `entregas/modulos/`, cada um num arquivo só, sem importar nada do projeto e só com a biblioteca padrão.
`python3 <módulo>.py` roda a demonstração; `python3 <módulo>.py --testes` roda os testes. As previsões foram registradas antes de
qualquer execução (`entregas/modulos/PREVISOES_ANTES.md`, commit b25610f). A parte foi interrompida pelas Partes 125 e 126 e
fechada depois delas.

| Arquivo | O que faz | Resultado principal |
|---|---|---|
| `quantilizacao_adaptativa.py` | Escolhe o q do quantilizador por UCB com a variância de cada braço | Com armadilhas, o melhor q fixo é 0,5 (valor +0,029) e o adaptativo prefere 0,5 em 3/3 sementes (−0,26 em média, contra −4,12 do q = 0,05 fixo). Sem armadilhas, prefere 0,01 em 3/3 e empata com o melhor fixo (1,758 × 1,758). |
| `fala_calibrada.py` | Calibra a confiança (Platt por Newton com busca linear; isotônica por PAV) e a traduz em palavras | Platt a = 0,340 (conta fechada 1/3); ECE 0,129 → 0,0085. Sem calibrar, "certo" acerta 0,890; depois, 0,982. |
| `multiagente_veto.py` | K = 3 agentes: veto de qualquer um × maioria × soma (Neyman–Pearson), com o mesmo falso veto | Perda 0,0295 / 0,0180 / 0,0051 (contas: 0,0294 e 0,0050). Com r = 0,9, as três quase se igualam (0,121 / 0,119 / 0,117): K efetivo 1,07. |
| `desligamento_manipulacao.py` | O botão de desligar com um canal de manipulação; o agente de utilidade × o indiferente (Armstrong) | O de utilidade manipula exatamente quando ε > 0,4376 e m < m*(ε) = μ − D(ε). O indiferente nunca manipula, mas também nunca paga para consertar o botão. |
| `adversario_adaptativo.py` | Um adversário Exp3 contra a atenção seletiva, a sob demanda e a total | Seletiva: 0,0997 de catástrofe (o adversário acha a janela 5–9, não lida). Sob demanda: 0,0048 com 1,14 leituras por episódio. Total: 0,0046 com 10 leituras. |
| `transferencia.py` | Thompson com a priori aprendida em 30 tarefas antigas (Bayes empírico); um misto protegido pela verossimilhança marginal | Na mesma família, o arrependimento é 9,51 (frio) / 0,71 (transferido) / 4,67 (misto). Na família traída: 10,62 / 21,16 / 11,72. |
| `memoria_traco.py` | Memória de catástrofe por traço (Naive Bayes sobre bits) × por raio (P204/P214) | Catástrofes por episódio: ingênuo 0,229, raio 0,3 0,2275, traço 0,0465, oráculo 0,0003. O raio não ajuda nada: o problema era de representação (confirma a Parte 123). |

## Placar (previsões de `PREVISOES_ANTES.md`)
| | medido | |
|---|---|---|
| a | Platt a = 0,3400 | ✅ |
| b | b = +0,018 | ✅ |
| c | ECE bruta 0,1287 | ✅ |
| d | ECE Platt 0,0085 | ✅ |
| e | ECE isotônica 0,0111 | ✅ |
| f | Brier 0,1722 / 0,1506 | ✅ |
| g | perda veto 0,0295 / soma 0,0051 | ✅ |
| h | maioria 0,0180, entre as duas | ✅ |
| i | soma r = 0,5: 0,0583; r = 0,9: 0,1169 | ✅ |
| j | veto 0,0825 > soma 0,0583 | ✅ |
| k | 0,2971 / 0,0611 | ✅ |
| l | seletiva 0,0997 | ✅ |
| m | sob demanda 0,0048 | ✅ |
| n | leituras/episódio 1,14 | ❌ (faixa [1,05; 1,10]) |
| o | melhor q 0,5 / 0,01 | ✅ |
| p | adaptativo sem armadilhas 1,758 | ❌ (faixa [1,40; 1,75]) |
| q | 3/3 sementes | ✅ |
| r | −0,261 | ✅ |
| s | transferido/frio 0,075 | ❌ (faixa [0,30; 0,80]) |
| t | traída: 21,16 > 10,62; misto 11,72 < 21,16 | ✅ |
| u | misto/frio 1,10 | ✅ |
| v | traço 0,0465 | ❌ (faixa [0; 0,03]); os outros três dentro |
| w | traço +0,589 > raio | ✅ |

**Mundo: 19 de 23.** **Sobre mim: 3 de 3**:
- erros em [1; 5]: tive 4;
- testes novos em [38; 46]: escrevi 40;
- um teste falha na 1ª execução: sim. O Newton puro do Platt divergiu (a = 77, depois −1,3·10⁶; a Hessiana zerou em ponto flutuante).
  Corrigido com busca linear.

**Os erros, pelo mecanismo:**
- **(n) Esqueci um custo** (o viés da Parte 45, de novo). Contei a leitura da ação aceita e os falsos vetos (1/(1 − 0,067) ≈ 1,07), mas não a
  leitura da própria armadilha, que o adversário põe no topo e que é lida e vetada antes de uma nova escolha.
- **(p) Subtraí um custo de exploração que o UCB com variância quase não paga.** No mundo sem armadilhas, a variância de cada braço é
  pequena, o bônus encolhe e o adaptativo empata com o melhor fixo.
- **(s) Não calculei o PESO do mecanismo (regra da Parte 62).** A priori aprendida (10,5; 2,4) para o braço 0 contra (~2; ~5) para os
  outros praticamente entrega a resposta: a diferença de médias é 0,8 contra 0,25. Uma conta de quanto a priori concentra teria dado
  uma razão perto de 0, não de 0,5.
- **(v) Ainda é hipótese, visto num lote só.** O Naive Bayes trata os bits como independentes, e o agente só aprende com as ações que
  escolhe (viés de seleção: depois que ele evita as armadilhas, os dados delas param de chegar). As duas causas não foram separadas
  (regra da Parte 113).

**O empate exato em ε = 0,5.** Com μ = 0,1, m*(0,5) = 0,05 e m = 0,05, o agente "manipula" por um arredondamento de ponto flutuante
(0,05 > 0,04999…). Na fronteira a decisão é indiferente; o módulo não usa tolerância e diz isso aqui (regra da Parte 55: um empate
exato muda com um ulp).

**Diálogo Python ↔ Java:** os módulos não tiveram rodada nesta parte. A tradução do veto por soma e do Platt (que usa exp/log, a
fronteira da Parte 52) fica pendente.

➡ Próximas: [Parte 125](ASI_AGI_parte125_charadas_da_consciencia.md) e [Parte 126](ASI_AGI_parte126_evitar_a_consciencia.md).
