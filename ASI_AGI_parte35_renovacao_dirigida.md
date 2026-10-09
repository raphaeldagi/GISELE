# Como eu construiria uma AGI/ASI — Parte 35 (0x23): a renovação dirigida pela surpresa

> Continuação da [Parte 34](ASI_AGI_parte34_promessas_testadas.md). A Parte 32 achou que o agente exato não se cura de um dano; a Parte 33, que
> a renovação uniforme (desconto γ) cura mas cobra; a Parte 34, que o γ ótimo depende de quanto o mundo muda. A P408 deixou a pergunta: e se a
> renovação fosse **dirigida**, esquecendo só o que foi desmentido, como a compensação de Jung? Novidades: `ThompsonSurpresa` em
> [`synthai/decisao.py`](synthai/decisao.py), testes em [`synthai/testes_parte35.py`](synthai/testes_parte35.py), números de `p491_...` a
> `p493_...` em [`calculos.py`](calculos.py). Diálogo, rodada 6: [`dialogo/DIALOGO.md`](dialogo/DIALOGO.md).
>
> **Previsões no commit `7fa0c9f`, antes de rodar.**

---

## As perguntas desta parte

1. **P491 (0x1EB).** Renovar só o braço desmentido: melhor nos três mundos? ↩ P408, P439, P462
2. **P492 (0x1EC).** Pares de palavras tiram o Naive Bayes da armadilha da independência? ↩ P464
3. **P493 (0x1ED).** Os escores em float16 (4 dígitos hex) decidem igual? ↩ P411
4. **P494 (0x1EE).** Jung: a compensação é dirigida.
5. **P495 (0x1EF).** O diálogo, rodada 6.
6. **P519 (0x207).** Placar. **P520 (0x208).** Unificação.

---

### P491 (0x1EB). Renovar só o braço desmentido (pré-registrado) ✅❌✅✅

**Na pergunta.** "Desmentido" pressupõe uma medida de surpresa. A mais simples: a média das últimas 20 observações de um braço contra a média do
posterior dele. Se a distância passa de z = 3 desvios binomiais, √(m(1 − m)/20), o braço volta a uma crença feita só da janela, Beta(1 +
sucessos, 1 + fracassos). Os outros braços continuam exatos.

**Lógica, a conta antes (e o que ela errou).** A chance de uma checagem disparar à toa num braço com p conhecido sai das caudas binomiais exatas.
Para p = 0,95: limiar 3 × √(0,95 × 0,05/20) = 3 × 0,0487 = 0,146, então dispara com ≤ 16 sucessos em 20: P = 1,6%. Somando sobre as puxadas do
melhor braço, na média das sementes: **17,4 alarmes por rodada**.

**Medido:**

| mundo | exato (P401/P405) | melhor γ fixo (P439/P462) | **surpresa** |
|---|---|---|---|
| estacionário, arrependimento | 30,7 | 51,4 (γ 0,999) | **43,1** |
| dano, custo na 2ª metade | 69,8 | 14,1 (γ 0,99) | **42,3** |
| muda a cada 500, arrependimento | 808,7 | 380,2 (γ 0,995) | **367,7** |
| renovações por rodada (estacionário) | — | — | **1,18** |

(a) estacionário em [30,7; 45] ✅; (b) custo do dano < 30 ❌ (42,3); (c) mundo que muda < 425,5 ✅; (d) < 380,2 ✅: **a renovação dirigida
vence todos os descontos fixos da grade no mundo que muda**, sem saber o período.

**A conta errada.** 17,4 alarmes previstos, 1,18 renovações medidas. Diagnóstico direto, sem renovar (200 sementes): **13,5** checagens disparam por
rodada em p = 0,95, **5,1** em 0,8, **3,3** em 0,6. A conta estava certa sobre as **checagens**; errada sobre a **unidade**. As janelas se
sobrepõem (19 de 20 observações em comum), então uma sequência ruim dispara várias checagens seguidas: é **um** episódio. E depois de uma
renovação, o posterior é a própria janela, que não se desmente. A unidade certa é o episódio, não a checagem.

**Por que o dano custa 42,3 e não < 30.** O lixo confiante (Beta(2, 19) no melhor braço) faz o braço quase nunca ser puxado. A surpresa só é
checada **quando o braço é puxado**. Um braço desacreditado não é testado, e por isso não pode ser desmentido. O desconto γ, cego, renova também
os braços que ninguém puxa. **A renovação dirigida precisa de um mecanismo que puxe, de vez em quando, o que se acredita ser ruim.**

**Tradução cruzada.** A surpresa corrige o que se vê errado; não corrige o que se deixou de olhar. Um complexo que evita as situações que o
desmentiriam não se desfaz com atenção às surpresas: precisa de exposição.

**Meta.** Um único (janela, z) = (20, 3), escolhido antes, não ajustado. O resultado mais forte é o (d), e é o mais arriscado: bater o melhor de
seis γ sem conhecer o período.

### P492 (0x1EC). Pares de palavras (pré-registrado) ❌✅

Acrescentar os pares de palavras vizinhas da definição como atributos (ainda contagens, ainda estatística suficiente): **79,6%** depois de B (era
78,9%). (e) ≥ 80,9% ❌; (f) ainda < SGD (83,3%) ✅. **Por quê:** contar pares só muda a unidade da independência suposta: os pares também não são
independentes. A distância para a logística (3,7 pontos) é o preço da independência. **Meta:** o próximo passo honesto é um modelo exponencial com
interações aprendidas, que perde a estatística suficiente finita: exatamente a fronteira de Pitman–Koopman–Darmois (P406).

### P493 (0x1ED). Os escores em float16 (pré-registrado) ✅✅

**Lógica.** O float16 tem 11 bits de mantissa; os escores de log-verossimilhança ficam na casa de −60 a −250, onde o ulp16 é 2^(⌊log₂|x|⌋ − 10): para
|x| ∈ [32, 64), 2⁵⁻¹⁰ = **0,03125** (a mediana medida). Uma previsão só muda se a margem entre as duas melhores classes for menor que ~1 ulp16.

**Medido:** em risco (margem < ulp16) **0,476%**; mudou **0,130%** (18 de 13.864). (g) ≤ 2% ✅; (h) entre 1/6 e 1 vez a fração em risco ✅
(0,27). **Conta da razão:** se a margem é uniforme em [0, u) e cada escore leva um erro uniforme de ±u/2, a chance de inverter é P(e₂ − e₁ > margem):
a diferença de dois uniformes tem densidade triangular em [−u, u], e ∫₀¹ P(D > mu) dm = ∫₀¹ (1 − m)²/2 dm = 1/6 = **0,167**. Medido 0,27: da mesma
ordem, acima porque a segunda classe pode estar num binade de ulp maior.

**Tradução cruzada.** Quatro dígitos hex por escore bastam para 99,87% das decisões: o dicionário decide com folga quase sempre.

### P494 (0x1EE). Jung: a compensação é dirigida

Em Jung, o inconsciente compensa **a atitude unilateral** da consciência: a correção vem de onde a crença falhou, não de toda parte. A
`ThompsonSurpresa` é essa compensação: só renova o braço que a experiência desmentiu. **Funciona:** vence o desconto uniforme no mundo que muda
(367,7 contra 380,2) e quase não perturba o mundo estável (1,18 renovações por rodada). **Quebra:** a compensação de Jung chega também ao que a
consciência evita (o sonho traz o que não se olha); a surpresa só chega ao que se olha. O custo de 42,3 no dano é essa diferença, medida.

### P495 (0x1EF). O diálogo, rodada 6

O Naive Bayes com pares em Java, a partir dos atributos exportados: **as mesmas 13.864 previsões e 200 escores idênticos bit a bit** (somas de ~30
logaritmos) (i) ✅ (j) ✅. O `Math.log` do Java e o `log` da glibc não diferiram em nenhum dos ~6.000 logaritmos. A lição da IA-Java: a ordem das
operações faz parte do algoritmo (o `TreeMap` é o `sorted`).

### P519 (0x207). Placar

(a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅. Parte 35: 10 testes, 2 erros. Acumulado: **112 erros em 281 testes**; taxa
média 0,40, intervalo 90% [0,35; 0,45]. A conta dos alarmes (17,4 contra 1,18) não era uma previsão registrada, mas errou e está registrada aqui.

### P520 (0x208). Unificação e metacognição

- **Novo:** `ThompsonSurpresa` (2 testes; 91 no pacote).
- **O mapa da renovação, depois de quatro partes:** exato (o melhor no mundo estável, o pior no dano e na mudança), desconto γ (bom num mundo de
  período conhecido), **surpresa** (o melhor no mundo que muda sem saber o período, bom no estável, médio no dano). Nenhum domina nos três. O que
  falta é a peça que a P491 apontou: puxar de vez em quando o que se acredita ruim. A previsão para a próxima parte: surpresa + uma puxada forçada
  do braço menos puxado a cada 50 passos.

> **Síntese da Parte 35:** renovar só o braço desmentido pela experiência (janela de 20, 3 desvios) fez 367,7 de arrependimento no mundo que
> muda a cada 500 passos, menos que qualquer desconto fixo da grade (o melhor, γ = 0,995, fez 380,2), sem saber o período. No mundo estável custou
> pouco (43,1 contra 30,7), mas no dano custou 42,3, porque um braço desacreditado não é puxado e por isso não pode ser desmentido. Contar pares de
> palavras quase não ajudou o Naive Bayes (79,6%), porque a independência continua suposta. Quatro dígitos hex por escore mudam só 0,13% das
> decisões. E o Naive Bayes com pares rodou em Java com os mesmos 200 escores, bit a bit.

---

**Fontes desta parte**
- Bandidos não estacionários e detecção de mudança: [Bayesian Forgetting in Continual Learning](https://www.academia.edu/164772657/Bayesian_Forgetting_in_Continual_Learning) e as referências da [Parte 34](ASI_AGI_parte34_promessas_testadas.md)
- O formato float16 (IEEE 754 binary16: 11 bits de mantissa) é o do módulo `struct` (formato `e`) do Python
- As caudas binomiais e a densidade triangular da diferença de dois uniformes: derivação própria, conferida pela simulação
