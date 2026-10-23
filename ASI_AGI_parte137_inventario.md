# Parte 137 — O inventário do que foi enviado, e os módulos recebidos que faltavam: GRPO num bandido e a memória por reservatório

↩ Nasce da Parte 136 (a lista dos cinco módulos recebidos que nenhuma parte usava) e do pedido "use tudo que enviei até hoje em cada módulo".

## O inventário
Tirado dos REGISTROS, por `grep`, e não da memória (a regra da Parte 136). Os itens recebidos são:
- os 31 arquivos de `externos/`;
- o pacote revisado (`synthai/revisado/`, Parte 82);
- o laboratório das sete camadas (`laboratorio/sete_camadas/`, Parte 83);
- os pedidos gravados no CLAUDE.md.

O que cada módulo do pacote reescreve, pela docstring dele:

| recebido | módulo que usa a ideia | parte |
|---|---|---|
| `arquitetura_pos_asi.py` | `synthai/rsi.py` (auto-melhoria com avaliador selado; o `exec` do original, recusado) | 33, 50 |
| `nexus_raphael_v0_1_0_colado.py` | `synthai/nexus.py` | 109 |
| `nexus_raphael_v2_colado.txt` | `synthai/nexus_v2.py` | 116 |
| `nexus_raphael_v2_0.py.txt` | `synthai/nexus_v2_2.py` | 121 |
| `nucleo_v30_transcrito.py.txt` | `synthai/nexus_v30.py` | 122 |
| `asi_metacognitivo_r37.py` | nenhum: arquivado e nunca importado (rede, subprocess, exec_module, fork) | 109 |
| `pacote3/modelo_mundo.py` (e o doc) | `synthai/mundo.py` | 93 |
| `pacote3/inovacao_guiada.py` | `synthai/passos.py` | 136 |
| `pacote3/rl_grupos.py` | **`synthai/grpo_bandido.py`** (esta parte; a vantagem vinha da Parte 87) | 87, 137 |
| `pacote3/aprendizagem_continua.py` | **`synthai/reservatorio.py`** (esta parte; o Shrink & Perturb vinha da Parte 87) | 87, 137 |
| `pacote3/transferencia_metacognitiva.py` | ainda nenhum: memória congelada e comparação pareada (Parte 138) | — |
| `pacote3/MANIFESTO_FONTES.json` | nenhum: o manifesto SHA-256 do trabalhador que se perpetua (recusado, Parte 93) | 93 |
| `pacote_v015/objetivos_cognitivos.py` | `synthai/passos.py` | 136 |
| `pacote_v015/workspace_global.py` | `synthai/workspace.py` | 102 |
| `word_rl_lab_v1/v2_recebido.py` | `synthai/palavras_rl.py` | 111 |
| os 14 textos `texto_recebido_parteNN.md` e `pos_asi_texto_parte50.md` | cada um virou a parte do seu número (auditoria, módulos `evoluido`, `autopoiese`, `plasticidade`, `pulsado`, `lago`, …) | 50–102 |
| `synthai/revisado/` e `laboratorio/` | integrados como estão, com os seus testes (Parte 82) e a comparação da sete camadas com a logística (Parte 83) | 82, 83 |

Depois desta parte, falta um módulo recebido: `transferencia_metacognitiva.py`. As recusas continuam recusas: o R37 e o manifesto do
trabalhador. "Usar tudo" não inclui o que a Parte 84 decidiu não construir.

## Perguntas
GRPO de `rl_grupos.py`:
- **(a)** Para recompensas 0/1 com k acertos em G, a vantagem do grupo é √((1 − p̂)/p̂) no acerto e −√(p̂/(1 − p̂)) no erro, com p̂ = k/G?
- **(b)** Na política uniforme inicial, que fração dos grupos não tem contraste (todas as recompensas iguais), para G = 2 e G = 8?
- **(c)** Com o MESMO orçamento de 4.096 ações, G = 2 ou G = 8 aprende mais? Que retorno exato no teste, e que fração de grupos sem
  contraste durante o treino?

Reservatório de `aprendizagem_continua.py`:
- **(d)** Num fluxo de 4 tarefas × 192 exemplos, com capacidade 128, quantos exemplos de cada tarefa ficam em média, e com que
  probabilidade o primeiro exemplo fica?
- **(e)** O posto efetivo exp(H(s/Σs)) de ativações construídas com valores singulares conhecidos bate com a fórmula?

## Previsões, registradas antes de qualquer execução do caso de teste
**Calibração da GRPO** (regra da Parte 84). Usei três mundos de contextos que não são o de teste (77/78, 79/80, 81/82), duas sementes cada,
orçamento 4.096:
- G = 2: média 0,9099, desvio 0,0093;
- G = 8: média 0,8909, desvio 0,0043;
- diferença: média 0,0190, desvio 0,0077;
- sem contraste: 0,826 com G = 2 e 0,511 com G = 8.

Em 1.024, 2.048 e 8.192 ações a diferença também favoreceu G = 2 (+0,046, +0,024, +0,009 a +0,025). O mecanismo que move o teste é o
número de atualizações: G = 2 tem quatro vezes mais grupos, mas desperdiça mais grupos sem contraste. Ele está presente nos casos de
calibração? Sim: é o mesmo orçamento e o mesmo desenho, mudam só os contextos.

O caso de teste é o mundo 31 (128 contextos de treino) contra o mundo 32 (128 de teste), com sementes de treino 31, 32 e 33. Mede-se a média
das três réplicas.

**Procedência:**
- identidades: (a), (e);
- forma fechada binomial: (b) × 2, (d) × 2;
- calibração: (c) × 5.

O centro de "quantos erros" é 0 + 4 × 0,10 + 5 × 0,25 = 1,65.

| | quantidade | faixa | procedência |
|---|---|---|---|
| (a) | máx \|vantagem − forma fechada\| em G = 2..16, k = 1..G−1 | [0; 2e-7] | o ε = 1e-8 no denominador: \|A\|·ε/σ ≤ 3,873·1e-8/0,242 = 1,6e-7 |
| (b1) | sem contraste, G = 2, 20.000 grupos uniformes | [0,5498; 0,5614] | 1/9 + 4/9 = 0,5556; ±1,645·√(p(1−p)/20.000) |
| (b2) | sem contraste, G = 8 | [0,0369; 0,0414] | (1/3)⁸ + (2/3)⁸ = 0,03917; ±0,00226 |
| (c1) | retorno no teste, G = 2 | [0,887; 0,932] | 0,9099 ± 1,645·√(0,0093² + 0,0093²/6)·1,36 |
| (c2) | retorno no teste, G = 8 | [0,880; 0,901] | 0,8909 ± 0,0104 |
| (c3) | G = 2 − G = 8 | [0,000; 0,038] | 0,0190 ± 0,0187 |
| (c4) | sem contraste no treino, G = 2 | [0,807; 0,845] | 0,826 ± 0,019 |
| (c5) | sem contraste no treino, G = 8 | [0,435; 0,586] | 0,511 ± 0,075 |
| (d1) | média, em 2.000 fluxos, dos exemplos da tarefa 1 no reservatório | [31,835; 32,165] | 128/4 = 32 exato; desvio hipergeométrico √(128·¼·¾·640/767) = 4,475, dividido por √2000 |
| (d2) | fração dos 2.000 fluxos em que o 1º exemplo fica | [0,153; 0,180] | 128/768 = 1/6; ±1,645·√(⅙·⅚/2000) |
| (e) | \|posto medido − exp(H)\| com s = (4, 2, 1, 0,5) em colunas de Hadamard | [0; 1e-9] | identidade: colunas ortogonais de média zero têm exatamente esses valores singulares |

**Sobre mim:** erros no mundo em [0; 4], com centro 1,65.

➡ Anterior: [Parte 136](ASI_AGI_parte136_passo_e_auditor.md).

## Medido (P3181–P3183)
| | medido | faixa | |
|---|---|---|---|
| (a) | 1,60·10⁻⁷ | [0; 2e-7] | ✅ (é a cota calculada: o ε age exatamente onde a conta dizia, k = 15 de G = 16) |
| (b1) | 0,5578 (fechada 0,5556) | [0,5498; 0,5614] | ✅ |
| (b2) | **0,0365** (fechada 0,03917; z = −1,95) | [0,0369; 0,0414] | ❌ |
| (c1) | 0,9086 | [0,887; 0,932] | ✅ |
| (c2) | 0,8987 | [0,880; 0,901] | ✅ |
| (c3) | +0,0099 | [0,000; 0,038] | ✅ |
| (c4) | 0,812 | [0,807; 0,845] | ✅ |
| (c5) | 0,501 | [0,435; 0,586] | ✅ |
| (d1) | 32,036 | [31,835; 32,165] | ✅ |
| (d2) | 0,1675 (1/6 = 0,1667) | [0,153; 0,180] | ✅ |
| (e) | erro 0,0; posto 3,117142 | [0; 1e-9] | ✅ |

**Mundo: 10 de 11.**

### (b2): um lote novo antes de qualquer mecanismo
É uma forma fechada (binomial) que errou a z = −1,95. Pela regra da Parte 117, gero um lote novo, registrado antes de rodá-lo: semente 1370,
outros 20.000 grupos, mesma faixa [0,0369; 0,0414], P(acerto) = 0,90. Se acertar, o erro de (b2) foi cauda (uma em dez faixas de 90% erra).
Se errar de novo, para o mesmo lado, a régua ou o gerador têm um defeito a procurar.

**Lote novo (semente 1370):** 0,03815, dentro da faixa: ✅. Os dois lotes juntos (40.000 grupos) dão 0,037325, z = −1,90, os dois abaixo da
forma fechada. Ainda é |z| < 2,5. Mas dois lados iguais pedem um terceiro lote, maior, registrado aqui antes de rodar: semente 13700,
100.000 grupos, faixa 0,03917 ± 1,645·√(0,0392·0,9608/100.000) = [0,03816; 0,04018].
