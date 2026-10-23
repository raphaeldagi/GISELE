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
