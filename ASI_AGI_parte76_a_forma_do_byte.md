# Como eu construiria uma AGI/ASI — Parte 76 (0x4C): a forma do byte

> Continuação da [Parte 75](ASI_AGI_parte75_o_que_se_prova.md). A Parte 75 deixou uma pergunta medível, tirada do texto recebido: o embedding de um caractere como o produto de Kronecker de
> dois fatores, um para cada nibble do byte (W₁[b ≫ 4] ⊗ W₂[b & 0x0F]), serve para a forma de GPT deste projeto? Pedido do usuário, gravado no `CLAUDE.md`: **"Continue sem parar."**

## Previsões sobre as minhas previsões desta parte (num commit só delas, antes de pensar qualquer faixa)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]** (uma diferença de bits entre dois modelos pode ter qualquer sinal)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,02; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~4 previsões do mundo, ~3 funções novas e um módulo novo no pacote (`synthai/gpt_kronecker.py`).

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[4 + S; 7 + S]** | 3 funções e o módulo |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de treinar no inglês)

**O teste.** Dois GPTs iguais em tudo (d = 16, T = 16, h = 32, 2.000 passos, taxa 0,005), um com a tabela de embeddings cheia (34 × 16 = 544 pesos) e outro com o embedding de Kronecker por nibble
(d₁ = d₂ = 4; os 4 nibbles altos e os 16 baixos do vocabulário usam 4·4 + 16·4 = **80** pesos), nas mesmas sementes. A medida: bits por caractere no teste (300 janelas); a diferença Kronecker − cheio.
**O mecanismo:** caracteres com o mesmo nibble alto (as letras de *a* a *o* são todas 0x6_) compartilham o fator A, e cada embedding, visto como matriz 4 × 4, tem posto 1. Isso tira liberdade.
**Está presente na calibração?** Sim: o português sem acentos usa o mesmo alfabeto `VOCAB_GPT`.
**Calibração, pela regra escrita antes (o português, sementes 76 a 79, pareadas):** diferenças +0,0712, +0,0287, +0,0619, +0,0812; média **+0,0608**, desvio 0,0228. A faixa para a média de 4 sementes
novas pareadas é a média ± t₃ · desvio · √(1/4 + 1/4), com t₃ = 2,353.
- **(a)** a diferença média (Kronecker − cheio) no inglês, sementes 76 a 79, em **[+0,0229; +0,0986]** bit
- **(b)** o número de sementes (de 4) em que o Kronecker perde em **[3; 4]** (perdeu em 4 de 4 na calibração; dois casos não fixam um sinal, quatro fixam pouco, por isso 3 entra)

**Medido (a) e (b), logo depois do registro:** diferenças no inglês +0,1029, +0,0689, +0,0685, +0,0751; média **+0,0788** ✅; o Kronecker perde em **4 de 4** ✅.

**Previsão nova (o controle do mecanismo), registrada antes de treinar.** A perda pode vir de ter menos pesos (80 contra 544) ou da estrutura dos nibbles ASCII (as letras de *a* a *o* compartilham
um fator, as de *p* a *z* outro). O controle separa as duas: o mesmo Kronecker com os caracteres **embaralhados entre os mesmos 34 bytes** (uma permutação com a semente 1.000 + semente). Os nibbles
usados e o número de pesos ficam iguais, e só muda quem compartilha fator com quem. **A conta:** a ordem ASCII foi escolhida para máquinas de escrever e telégrafos, não pela estatística do inglês, e
por isso não deve carregar informação sobre quais letras se parecem. O desvio de uma diferença pareada entre dois Kronecker vem do mesmo ruído de semente da calibração (0,0228).
- **(c)** a diferença média (embaralhado − ASCII), no inglês, sementes 76 a 79, em **[−0,038; +0,038]** bit (0 ± 2,353 · 0,0228 · √(1/4 + 1/4))
