# Parte 138 — O último módulo recebido: a memória congelada de falhas, e o teste dos grupos úteis da GRPO

↩ Nasce da Parte 137: `transferencia_metacognitiva.py` era o único módulo recebido sem uso, e a hipótese dos grupos úteis ficou para testar.

## O módulo recebido
`externos/pacote3/transferencia_metacognitiva.py` otimiza quadráticas de quatro famílias (suave, anisotrópica, rígida e ruidosa) por
retrocesso. Cada rejeição divide o passo por 2, e cada ganho o multiplica por 1,06. No treino, uma memória conta as rejeições por
"contexto do gradiente": baixo, médio e alto, pela razão |g|/√f com cortes 3 e 6. Antes do teste a memória é congelada, e ela só mexe
no PRIMEIRO passo de cada tarefa: passo·(1 − 0,6·(r + 1)/(n + 2)). O próprio texto escreve a pergunta que o refuta: "Que observação refutaria
a utilidade da memória? A política selecionada sem memória igualar ou superar o resultado com memória em tarefas reservadas."

A reescrita está em `synthai/memoria_congelada.py`, offline e na biblioteca padrão. Ela reusa a quadrática e as somas em laço de
`synthai/passos.py`. A geometria restrita e o "motor de evidências" do original vinham de um `recursiva_paraconsistente` que não estava no
pacote. Por isso aqui a otimização é sem restrição, e o conflito da família ruidosa é uma rejeição sorteada com a chance declarada (0,1).

**O contexto é uma curvatura.** Numa quadrática f = dᵀAd, g = 2Ad. Então |g|²/f = 4·dᵀA²d/dᵀAd, que é 4 vezes um quociente de Rayleigh
de A. Logo |g|/√f fica entre 2√λ_min e 2√λ_max: o "contexto" mede a curvatura vista na direção atual. Os cortes 3 e 6 correspondem a λ =
2,25 e λ = 9.

## Perguntas
- **(a)** |g|/√f fica sempre em [2√λ_min, 2√λ_max]?
- **(b)** A memória congelada melhora a razão de custo média das tarefas de teste?
- **(c)** Em quantas das 32 tarefas de teste ela piora?
- **(d)** O critério de refutação do próprio texto se cumpre, isto é, o intervalo do bootstrap da diferença contém 0?
- **(e), (f)** Os grupos úteis da Parte 137 preveem a GRPO com G = 4 e G = 16 no mesmo orçamento?

## Previsões, registradas antes de qualquer execução do caso de teste
**Calibração da memória** (regra da Parte 84). Usei as sementes 77 e 78, que não são a de teste, e os passos 0,05 e 0,2:
- diferença média +0,0002, +0,0001, −0,0001 e 0,0000 (média 0,00005, desvio 0,00013);
- tarefas em que a memória piora: 27, 27, 28 e 23 de 32 (média 26,25, desvio 2,2);
- o intervalo do bootstrap contém 0 nas 4.

O mecanismo, escrito antes. No contexto "baixo", que tem quase todas as tentativas, a taxa é (1 + 1)/(249 + 2) e o fator 0,995. O primeiro
passo encolhe meio por cento em quase toda tarefa, o que custa um pouco onde nada seria rejeitado e salva as poucas tarefas em que o passo
cheio seria rejeitado. Ele está presente no caso de teste? Sim: o mesmo desenho, só mudam as tarefas.

O teste é a semente 31: 12 tarefas de treino (fase 1) e 32 de teste (fase 3), com os passos 0,05 e 0,2.

**GRPO.** A hipótese da Parte 137 diz que conta o número de grupos úteis, com contraste. G = 4 deve ficar entre G = 2 e G = 8, e G = 16
abaixo de G = 8. No mesmo mundo (31/32), com as sementes 31 a 33 e 4.096 ações. A chance de acertar as duas por sorte, se o retorno de G = 4
e G = 16 caísse uniformemente na faixa observada até aqui (0,88 a 0,92), seria cerca de 0,25 × 0,5.

**Procedência:**
- identidade: (a);
- calibração: (b) × 2, (c) × 2, (d) × 2;
- hipótese de 1 lote: (e), (f).

O centro de "quantos erros" é 0 + 6 × 0,25 + 2 × 0,25 = 2,0.

| | quantidade | faixa | procedência |
|---|---|---|---|
| (a) | pontos, das 4 famílias × 2.500 direções gaussianas, com \|g\|/√f em [2√λ_min, 2√λ_max] | 10.000 de 10.000 | identidade (Rayleigh) |
| (b1) | média de (sem memória − com memória), passo 0,05 | [−0,00028; 0,00038] | 0,00005 ± 1,645·√(0,00013² + 0,00013²/4)·1,36 |
| (b2) | idem, passo 0,2 | [−0,00028; 0,00038] | idem |
| (c1) | tarefas em que a memória piora, passo 0,05 | [21; 31] | 26,25 ± 1,645·√(2,2² + 2,2²/4)·1,36 = ±5,5 |
| (c2) | idem, passo 0,2 | [21; 31] | idem |
| (d1) | o intervalo 95% do bootstrap contém 0, passo 0,05 | sim | 4 de 4 na calibração |
| (d2) | idem, passo 0,2 | sim | idem |
| (e) | retorno de G = 4 | entre G = 8 e G = 2: [0,8987; 0,9086] | hipótese dos grupos úteis |
| (f) | retorno de G = 16 | abaixo de G = 8: [0,85; 0,8987] | idem; o piso 0,85 é só para dar largura |

**Sobre mim:** erros no mundo em [0; 5], com centro 2,0.

➡ Anterior: [Parte 137](ASI_AGI_parte137_inventario.md).

## Medido (P3184–P3186)
| | medido | faixa | |
|---|---|---|---|
| (a) | 10.000 de 10.000 | 10.000 | ✅ |
| (b1) | +0,00035 | [−0,00028; 0,00038] | ✅ |
| (b2) | **+0,00067** | [−0,00028; 0,00038] | ❌ |
| (c1) | 27 | [21; 31] | ✅ |
| (c2) | **19** | [21; 31] | ❌ |
| (d1) | IC (−0,00036; 0,00117), contém 0 | sim | ✅ |
| (d2) | IC (−0,00055; 0,00195), contém 0 | sim | ✅ |
| (e) | G = 4: 0,9058, com 355 grupos úteis | [0,8987; 0,9086] | ✅ |
| (f) | G = 16: 0,8825, com 179 grupos úteis | [0,85; 0,8987] | ✅ |

**Mundo: 8 de 10.**

**Os grupos úteis.** Nos quatro G, o retorno segue a ordem dos grupos úteis:

| G | grupos úteis | retorno |
|---|---|---|
| 2 | 385 | 0,9086 |
| 4 | 355 | 0,9058 |
| 8 | 256 | 0,8987 |
| 16 | 179 | 0,8825 |

A hipótese da Parte 137 previu dois casos novos e passou nos dois. Ainda é um mundo só, ou seja, um lote (Parte 66).

**Os dois erros do passo 0,2 apontam para o mesmo lado:** a memória ajudou mais e piorou menos tarefas do que na calibração. O mecanismo
candidato é que, com o passo maior, o primeiro passo cheio é rejeitado mais vezes, e o encolhimento da memória salva mais tarefas. Antes de
lhe dar crédito, um teste com sinal, registrado aqui antes de rodar. Nas sementes 32, 33 e 34, em cada uma, as tarefas em que a memória
piora com o passo 0,2 devem ser MENOS que com o passo 0,05: 3 de 3. Por acaso, com a ordem sorteada, isso sai com chance cerca de (½)³ = 1/8.
