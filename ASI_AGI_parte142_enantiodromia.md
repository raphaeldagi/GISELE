# Parte 142 — Jung calculado nos módulos novos: a enantiodromia do heavy-ball e a compensação do grupo

↩ Nasce da Parte 136 (a média exponencial do gradiente É o heavy-ball de Polyak) e da Parte 137 (a vantagem da GRPO). Jung é a base
psicológica da série desde a Parte 6: cada conceito vira conta, e a parte diz onde a formalização funciona e onde quebra.

## As duas leituras, escritas antes das contas
- **Enantiodromia** (Jung, *Tipos psicológicos*, definições): tudo o que vai ao extremo se converte no oposto. Na descida com memória (a média
  exponencial, β = 0,6, η = 0,05), cada modo próprio segue c_{t+1} = (2 − β − 2ηβλ)·c_t − (1 − β)·c_{t−1}. Se as raízes são complexas, a
  coordenada passa do ponto de equilíbrio e muda de sinal: o impulso que leva ao alvo leva além dele. As raízes são complexas quando
  (2 − β − 2ηβλ)² < 4(1 − β), isto é, para λ entre (2 − β − 2√(1 − β))/(2ηβ) = 2,251 e (2 − β + 2√(1 − β))/(2ηβ) = 44,4. O módulo das raízes é
  √(1 − β) = 0,632, e o ângulo é θ = arccos((2 − β − 2ηβλ)/(2√(1 − β))). Em T passos, a coordenada muda de sinal perto de Tθ/π vezes.
- **Compensação** (o inconsciente compensa a atitude consciente): na GRPO, a vantagem de cada resposta é a sua recompensa menos a média do
  grupo, dividida pelo desvio. A soma das vantagens de um grupo é zero, exatamente. O que um acerto ganha, os erros do mesmo grupo perdem.

## Perguntas
Na quadrática da Parte 136 (d = 8, κ = 10, semente 31001, partida da semente 5), com a média exponencial e T = 24:
- **(a)** Quantos dos 8 modos mudam de sinal pelo menos uma vez?
- **(b)** a **(f)** Quantas vezes muda de sinal cada um dos 5 modos oscilantes, λ = 2,683, 3,728, 5,179, 7,197 e 10?
- **(g)** Os 3 modos de raízes reais (λ = 1, 1,389 e 1,931) mudam de sinal?
- **(h)** Em 10.000 grupos aleatórios da GRPO (G de 2 a 16, recompensas em [0, 1]), qual é o máximo de |Σ vantagens|?

## Previsões, registradas antes de qualquer execução
Os ângulos foram calculados por código antes deste registro: θ = 0,2026, 0,3764, 0,5333, 0,6991 e 0,8861. Logo Tθ/π = 1,55, 2,88, 4,07, 5,34 e
6,77. A contagem de travessias de uma senoide amortecida em T passos é ⌊Tθ/π⌋ ou ⌈Tθ/π⌉, conforme a fase.

**Procedência:**
- identidade: (h);
- forma fechada: (a) a (f);
- mecanismo: (g).

O centro de "quantos erros" é 0 + 0,10 × 6 + 0,25 × 1 = 0,85.

- **(a)** modos que mudam de sinal pelo menos uma vez em **[5; 5]**. Os 5 de raízes complexas; os reais têm duas raízes positivas.
- **(b)** travessias do modo λ = 2,683 em **[1; 2]** (Tθ/π = 1,55).
- **(c)** do modo λ = 3,728 em **[2; 3]** (2,88).
- **(d)** do modo λ = 5,179 em **[4; 5]** (4,07).
- **(e)** do modo λ = 7,197 em **[5; 6]** (5,34).
- **(f)** do modo λ = 10 em **[6; 7]** (6,77).
- **(g)** travessias somadas dos 3 modos reais em **[0; 0]**. Mecanismo: duas raízes reais positivas, e o primeiro passo (m₀ = g₀) leva
  na direção do alvo sem passar dele, porque 2ηλ < 1 nesses modos. A coordenada pode cruzar o zero no máximo uma vez, mas não deve.
- **(h)** máximo de \|Σ vantagens\| em **[0; 1e-12]**. Identidade: Σ(rᵢ − r̄) = 0, a menos do arredondamento.

### Previsões sobre as previsões (m), registradas (régua: P2837)
**Regra da Parte 120.** A régua rodou sobre o rascunho, com uma linha de placar provisória apagada antes do commit, e deu m1 = 8, m2 = 2,
m3 = 0,101 e m5 = 0.

**Regra da Parte 122.** E = 0,85, o que leva m1 a [8; 9].
- **(m1)** nº de previsões do mundo em **[8; 9]**
- **(m2)** nº de faixas que cruzam ou tocam o zero em **[2; 3]**
- **(m3)** mediana de w em **[0,08; 0,13]**
- **(m4)** fração de acertos em **[0,75; 1,00]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, com centro 0,85.

➡ Anterior: [Parte 141](ASI_AGI_parte141_volta8_resultado.md).

## Medido (P3193, P3194)
Pelos iterados reais da `synthai.passos.descer`, projetados nos autovetores:

| λ | travessias | Tθ/π | faixa | |
|---|---|---|---|---|
| 1,000 | 0 | (real) | (g) | ✅ |
| 1,389 | 0 | (real) | (g) | ✅ |
| 1,931 | 0 | (real) | (g) | ✅ |
| 2,683 | 1 | 1,55 | (b) [1; 2] | ✅ |
| 3,728 | 3 | 2,88 | (c) [2; 3] | ✅ |
| 5,179 | 4 | 4,07 | (d) [4; 5] | ✅ |
| 7,197 | 5 | 5,34 | (e) [5; 6] | ✅ |
| 10,000 | 7 | 6,77 | (f) [6; 7] | ✅ |

(a) 5 modos mudam de sinal ✅. (h) máximo de \|Σ vantagens\| = 3,6·10⁻¹³ ✅.

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅

**Mundo: 8 de 8.** **(m):** m1 = 8, m2 = 2, m3 = 0,101, m4 = 1,0, m5 = 0, m6 = 0, os seis dentro: **6 de 6**. **Sobre mim:** 0 erros, em [0; 3]: ✅.

## Tradução cruzada: onde a formalização funciona e onde quebra
- **Funciona:** a enantiodromia tem uma condição exata. O "oposto" aparece só quando há MEMÓRIA do impulso (β < 1) e o impulso é forte o
  bastante (λ > 2,251). Sem memória, com β = 1 e o passo fixo, a coordenada só cruza o zero se 1 − 2ηλ < 0, isto é, λ > 10. Aqui nenhum
  modo passa disso: o de λ = 10 vai a zero em um passo e para. A conta diz, então, que a conversão no oposto nasce da inércia, não da força.
  Uma força grande sem memória chega ao alvo; uma força média COM memória passa dele. É uma conta posterior sobre o caso β = 1; não
  foi registrada como previsão.
- **Funciona:** a compensação de Jung é a soma zero do grupo. A GRPO não tem crítico: o "inconsciente" que avalia cada resposta é o
  próprio grupo. O que um acerto ganha, os erros do mesmo grupo perdem, e o que se compensa sai exato, a 10⁻¹³.
- **Quebra:** para Jung, a enantiodromia é uma reviravolta da energia psíquica ao longo da vida, uma vez, irreversível. Aqui ela é uma
  oscilação amortecida e simétrica: o módulo √(1 − β) = 0,632 por passo faz cada travessia menor que a anterior. A conta tem a forma da
  reviravolta, mas não tem a irreversibilidade. Para tê-la, seria preciso um sistema com histerese, como a ignição biestável da
  Parte 127, e não um linear.

## Engenharia reversa
- **O que deu certo, e por quê:** as oito faixas saíram de forma fechada, com o mecanismo (a fase) dentro da largura. É o padrão das Partes
  88 a 99: uma faixa de conta acerta e uma faixa de reputação erra.
- **O padrão que se repetiu desde a Parte 136:** os módulos reescritos do que o usuário mandou escondiam contas clássicas com outro nome:
  - a "média do gradiente" era o heavy-ball;
  - o "contexto" era um quociente de Rayleigh;
  - a "vantagem de grupo" era a compensação de soma zero.
  Dar o nome clássico tornou cada um previsível. O texto recebido não é obscuro; ele não diz a conta que já faz.

## Funções e testes
- **Funções:** `p3193_enantiodromia`, `p3194_compensacao` e `_parte_142`. Entradas P3193 e P3194 na regressão.
- **Módulo:** `synthai.passos.descer` ganhou `guardar=` (os iterados).
- **Testes:** `synthai/testes_parte142.py`.
