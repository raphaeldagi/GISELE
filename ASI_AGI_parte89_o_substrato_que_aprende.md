# Como eu construiria uma AGI/ASI — Parte 89 (0x59): o substrato que aprende

> Continuação da [Parte 88](ASI_AGI_parte88_a_arquitetura_autopoietica_recebida.md). Sem texto novo do usuário: sigo o ciclo (Parte 44/75). A Parte 86 construiu o neurônio pulsado (LIF, Izhikevich) e a regra
> STDP, mas só mediu neurônios isolados. Aqui faço o substrato **aprender**: a STDP não supervisionada muda os pesos, e a pergunta é se ela faz o que a literatura afirma — tornar uma sinapse seletiva à
> correlação — e se o faz no meu regime pequeno (a lição das Partes 84 e 87: um efeito famoso pode não aparecer fora da sua escala, então a conta vem antes).
>
> **A âncora algébrica (Parte 70):** a STDP é Hebb com janela temporal. A deriva esperada de um peso é a integral da janela vezes a correlação pré-pós — uma forma fechada. Começo por ela (que não depende de
> regime), e só depois arrisco o efeito de competição (que depende).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[3 + S; 7 + S]** | funções de STDP + a rodada |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

A âncora é a forma fechada (não depende de regime); as (b) e (c) foram calibradas num teste de fumaça (200 pares; semente 89) e PREVEEM tamanhos/sementes que a fumaça não usou, para serem previsões de
verdade. Contas fechadas e sinais não levam o fator 1,36; as faixas de simulação levam.

- **(a)** a integral da janela STDP A₊τ₊ − A₋τ₋: balanceada (A₊=A₋=0,1; τ=20) = **0,0**; depressão dominante (A₋=0,12) = **−0,4** (exato). E a deriva de um peso sob pré e pós de Poisson INDEPENDENTES tem o SINAL da
  integral: **negativa** na depressão dominante (categórico)
- **(b)** a propriedade definidora da STDP, com **500** pares (a fumaça usou 200): uma sinapse cujo pré precede o pós (Δt = +5 ms) potencia e uma cujo pré segue o pós (Δt = −5 ms) deprime; o peso "pré antes" em
  **[3,5; 6,0]** e o "pré depois" **< 0** (parte de w₀ = 0,5; categórico no sinal, faixa no tamanho)
- **(c)** a competição sináptica num neurônio LIF de brinquedo (10 correlacionadas, 40 ruído), com uma **semente nova (90)** e 8000 ms: os dois grupos NÃO se separam — ambos saturam perto de wmax = 1,0 e
  |correlacionadas − ruído| **< 0,15** (o efeito de Song-Miller-Abbott não aparece nesta escala sem ajuste fino; a lição das Partes 84 e 87)
- **(d)** a rodada 56: uma população de neurônios de Izhikevich acoplados dá a MESMA trajetória bit a bit em Python e Java (categórico: IGUAL)
- **(e)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–89 em **[0,74; 0,88]**
